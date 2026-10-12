"""The generated layer's cells (9.19 spec; 9.20 spec): the grid definition, the sixteen modes, the 240 ordered pairs,
and each set's cells — id, placements (which task set holds which segment and how long its tasks live), grid
coordinates, split, seed. Every seed and every split is a keyed SHA-256 draw from the cell's or the pair's id;
nothing is chosen by hand except the ladder's tier-4 name table (spec invariants).

A placement is `(mode, start_us, end_us, alive_until_us)`: the mode's C1 task set labels the segment
[start, end) and its tasks live to `alive_until` — the segment's end where they depart at the boundary, the file's
end where they stay (9.19 decision 2's `focus` form; the distractor grid's A).

A distractor cell (9.20 decisions 1–3) carries one placement, A over the first segment with its tasks alive to the
file's end, and `arrival` — the mode whose task set, or the program, arrives at the boundary. A ladder cell (9.20
decisions 5–7) carries `rename`, the real name -> substitute map applied to the mode's C1 file.
"""

import hashlib
import pathlib
import re

import yaml

from wlc.grid import NAME_TIERS
from wlc.linter import BOUND_LABELS, _check_tag
from wlc.units import parse_us

SETS = ("transition-grid", "return-grid", "flap-stress", "distractor-grid", "familiarity-ladder")
RELATIONS = ("cross-mode", "out-of-vocabulary")
CARRIERS = ("all", "focus", "others")   # `all` first: the cell the others collapse into when their name sets coincide
COMPILER_NAMES = ("wineserver",)   # named by the compiler, not the timeline (the chain's member; 9.20 decision 7)


def load_definition(path):
    return yaml.safe_load(pathlib.Path(path).read_text())


def modes_of(timelines_dir):
    """The sixteen modes, from the C1 files' names (`c1-<mode>.timeline.yaml`), sorted."""
    names = sorted(p.name for p in pathlib.Path(timelines_dir).glob("c1-*.timeline.yaml"))
    return [n[len("c1-"):-len(".timeline.yaml")] for n in names]


def ordered_pairs(modes):
    """Every ordered pair (A, B) of distinct modes, in sorted order: 16 × 15 = 240."""
    return [(a, b) for a in modes for b in modes if a != b]


def keyed_hex(*parts):
    return hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()


def seed_of(set_name, cell_id):
    """The cell's seed: the first four bytes of SHA-256 over `seed|<set>|<cell id>`."""
    return int.from_bytes(hashlib.sha256(f"seed|{set_name}|{cell_id}".encode()).digest()[:4], "big")


def ranked_pairs(pairs, *key):
    """The pairs in keyed-hash order: a split or a draw that no one chose."""
    return sorted(pairs, key=lambda ab: keyed_hex(*key, f"{ab[0]}-to-{ab[1]}"))


def names_of(c1):
    """Every process name a C1 timeline sets: the tasks' names, an orchestrator's child name, a chain's member names;
    sorted, each once."""
    names = set()
    for task in c1["tasks"]:
        names.add(task["name"])
        bind = task.get("bind") or {}
        if "child_name" in bind:
            names.add(bind["child_name"])
        names.update(bind.get("member_names") or [])
    return sorted(names)


def focus_name(c1):
    """The process name of the task holding the focus, None when no window does (`c1-idle`)."""
    focus = c1.get("focus") or []
    if not focus:
        return None
    task_id = focus[0]["task"]
    return next(task["name"] for task in c1["tasks"] if task["id"] == task_id)


def _cell(set_name, cell_id, a, b, placements, grid, split=None):
    cell = {"id": cell_id, "set": set_name, "a": a, "b": b, "placements": placements, "grid": dict(grid),
            "seed": seed_of(set_name, cell_id)}
    if split is not None:
        cell["split"] = split
    return cell


def transition_cells(defn, pairs):
    """9.19 decision 2. `departs`: A's tasks leave at the boundary, B's arrive. `focus`: B's arrive and take the
    focus, A's stay to the end of the file. Two segments of `segment_length`."""
    L = parse_us(defn["segment_length"])
    out = []
    for a, b in pairs:
        for form in defn["sets"]["transition-grid"]["forms"]:
            a_until = L if form == "departs" else 2 * L
            out.append(_cell("transition-grid", f"tr-{a}-to-{b}-{form}", a, b,
                             [(a, 0, L, a_until), (b, L, 2 * L, 2 * L)], {"a": a, "b": b, "form": form}))
    return out


def return_cells(defn, pairs):
    """9.19 decision 10: A -> B -> A, every task set departing at its boundary; the middle length a variant.
    Decision 6: the pairs ranked by keyed hash, the first `tuning` of them the tuning half, a pair's variants
    together."""
    spec = defn["sets"]["return-grid"]
    L = parse_us(defn["segment_length"])
    tuning = set(ranked_pairs(pairs, "split", "return-grid")[:spec["split"]["tuning"]])
    out = []
    for a, b in pairs:
        split = "tuning" if (a, b) in tuning else "measurement"
        for middle in spec["middle_lengths"]:
            M = parse_us(middle)
            out.append(_cell("return-grid", f"rt-{a}-to-{b}-{middle}", a, b,
                             [(a, 0, L, L), (b, L, L + M, L + M), (a, L + M, 2 * L + M, 2 * L + M)],
                             {"a": a, "b": b, "middle": middle}, split))
    return out


def flap_cells(defn, pairs):
    """9.19 decision 7: a lead-in on A, then `alternations` segments of one interval each, B and A in turn, every
    task set departing at its boundary; `pairs` ordered pairs drawn by keyed hash; each file under two seeds, one
    per split name (decision 6)."""
    spec = defn["sets"]["flap-stress"]
    lead, k = parse_us(spec["lead_in"]), spec["alternations"]
    chosen = ranked_pairs(pairs, "pairs", "flap-stress")[:spec["pairs"]]
    out = []
    for a, b in chosen:
        for interval in spec["intervals"]:
            T = parse_us(interval["length"])
            placements = [(a, 0, lead, lead)]
            for i in range(1, k + 1):
                mode = b if i % 2 else a
                start = lead + (i - 1) * T
                placements.append((mode, start, start + T, start + T))
            for split in spec["split"]["names"]:
                out.append(_cell("flap-stress", f"flap-{a}-to-{b}-{interval['length']}-{split}", a, b, placements,
                                 {"a": a, "b": b, "interval": interval["length"],
                                  "interval_source": interval["source"]}, split))
    return out


def distractor_cells(defn, pairs, modes, sets):
    """9.20 decisions 1–3. The user stays in A: A's task set holds the first segment and lives to the file's end; at
    the boundary B's whole task set (`cross-mode`, the 240 pairs) or one measured program outside every mode
    (`out-of-vocabulary`, over the sixteen modes) arrives and stays. Where A's and B's focus holders share a name the
    cell's telemetry equals the transition grid's `focus` form's, so the record says so (`focus_name_shared`)."""
    spec = defn["sets"]["distractor-grid"]
    L = parse_us(defn["segment_length"])
    out = []
    if "cross-mode" in spec["relations"]:
        for a, b in pairs:
            holder = focus_name(sets[a])
            shared = holder is not None and holder == focus_name(sets[b])
            cell = _cell("distractor-grid", f"dx-{a}-with-{b}", a, b, [(a, 0, L, 2 * L)],
                         {"relation": "cross-mode", "a": a, "b": b, "focus_name_shared": shared})
            cell["arrival"] = {"mode": b}
            out.append(cell)
    if "out-of-vocabulary" in spec["relations"]:
        for a in modes:
            for program in spec["programs"]:
                cell = _cell("distractor-grid", f"dx-{a}-with-{program['name']}", a, program["name"],
                             [(a, 0, L, 2 * L)],
                             {"relation": "out-of-vocabulary", "a": a, "b": program["name"],
                              "focus_name_shared": False})
                cell["arrival"] = {"program": dict(program)}
                out.append(cell)
    return out


def known_names(defn, sets):
    """Every process name the dataset knows to be real or already taken: the C1 files' names, the compiler's, the
    coverage tool's name table, and the tier-4 table's — a tier-5 draw equal to one of these is redrawn."""
    names = set(COMPILER_NAMES)
    for c1 in sets.values():
        names.update(names_of(c1))
    for tier_names in NAME_TIERS.values():
        names.update(tier_names)
    names.update(defn["sets"]["familiarity-ladder"]["tier4_names"].values())
    return names


def tier5_name(cell_id, real, letters, taken):
    """The keyed draw for one real name in one cell: `letters` lowercase letters from SHA-256 over
    `name|familiarity-ladder|<cell id>|<real name>|<attempt>`, the first attempt not in `taken`."""
    for attempt in range(10_000):
        digest = hashlib.sha256(f"name|familiarity-ladder|{cell_id}|{real}|{attempt}".encode()).digest()
        name = "".join(chr(ord("a") + byte % 26) for byte in digest[:letters])
        if name not in taken:
            return name
    raise ValueError(f"{cell_id}: no free tier-5 name for {real!r}")


def _carrier_of(renamed, holder, all_names):
    if set(renamed) == set(all_names):
        return "all"
    return "focus" if set(renamed) == {holder} else "others"


def ladder_cells(defn, modes, sets):
    """9.20 decisions 5–7. Per mode and tier (4, 5), one cell per carrier form — every name, the focus holder's
    name alone, the other names alone — with cells whose name set coincides collapsed into the `all` cell (its
    record lists every carrier it stands for); a form renaming nothing has no cell. Tier 3: the definition's cells,
    the real opaque name with its source. One real name maps to one substitute within a file."""
    spec = defn["sets"]["familiarity-ladder"]
    L = parse_us(defn["segment_length"])
    table, letters = spec["tier4_names"], spec["tier5_letters"]
    known = known_names(defn, sets)
    out = []
    for mode in modes:
        c1 = sets[mode]
        all_names = [n for n in names_of(c1) if n not in COMPILER_NAMES]
        holder = focus_name(c1)
        by_carrier = {"all": all_names,
                      "focus": [holder] if holder else [],
                      "others": [n for n in all_names if n != holder]}
        for tier in spec["tiers"]:
            by_names = {}
            for carrier in CARRIERS:
                names = by_carrier[carrier]
                if not names:
                    continue
                key = tuple(names)
                if key in by_names:
                    by_names[key]["grid"]["carriers"].append(carrier)
                    continue
                cell_id = f"fl-{mode}-t{tier}-{carrier}"
                if tier == 4:
                    missing = [n for n in names if n not in table]
                    if missing:
                        raise ValueError(f"{cell_id}: no tier-4 name for {missing}")
                    rename = {n: table[n] for n in names}
                else:
                    rename, taken = {}, set(known)
                    for n in names:
                        rename[n] = tier5_name(cell_id, n, letters, taken)
                        taken.add(rename[n])
                cell = _cell("familiarity-ladder", cell_id, mode, None, [(mode, 0, L, L)],
                             {"mode": mode, "tier": tier, "carrier": carrier, "carriers": [carrier],
                              "renamed": rename})
                cell["rename"] = rename
                by_names[key] = cell
                out.append(cell)
        for real, entry in (spec.get("tier3") or {}).get(mode, {}).items():
            cell_id = f"fl-{mode}-t3"
            existing = next((c for c in out if c["id"] == cell_id), None)
            if existing is None:
                existing = _cell("familiarity-ladder", cell_id, mode, None, [(mode, 0, L, L)],
                                 {"mode": mode, "tier": 3, "carrier": None, "carriers": [], "renamed": {},
                                  "sources": {}})
                existing["rename"] = {}
                out.append(existing)
            if real not in all_names:
                raise ValueError(f"{cell_id}: {real!r} is not a name of c1-{mode}")
            existing["rename"][real] = entry["name"]
            existing["grid"]["renamed"][real] = entry["name"]
            existing["grid"]["sources"][real] = entry["source"]
            existing["grid"]["carrier"] = _carrier_of(existing["rename"], holder, all_names)
            existing["grid"]["carriers"] = [existing["grid"]["carrier"]]
    return out


def cells(defn, modes, sets=None):
    """{set name: [cells]} for every set the definition names. The distractor grid and the ladder read the C1
    timelines (`sets`, as `compose.c1_sets` loads them)."""
    pairs = ordered_pairs(modes)
    out = {}
    for name in defn["sets"]:
        if name in ("distractor-grid", "familiarity-ladder") and sets is None:
            raise ValueError(f"{name}: the C1 timelines are needed to build its cells")
        if name == "transition-grid":
            out[name] = transition_cells(defn, pairs)
        elif name == "return-grid":
            out[name] = return_cells(defn, pairs)
        elif name == "flap-stress":
            out[name] = flap_cells(defn, pairs)
        elif name == "distractor-grid":
            out[name] = distractor_cells(defn, pairs, modes, sets)
        elif name == "familiarity-ladder":
            out[name] = ladder_cells(defn, modes, sets)
        else:
            raise ValueError(f"unknown set {name!r}")
    return out


def lint_grids(path, registry):
    """The definition's form; every source a registry tag or a label (the bound-value rule, 9.18); every name the
    definition sets within the `comm` limit."""
    path = pathlib.Path(path)
    errors = []
    try:
        defn = load_definition(path)
    except (OSError, yaml.YAMLError) as exc:
        return [f"{path.name}: unreadable ({exc})"]
    for key in ("segment_length", "no_input_below"):
        try:
            parse_us(defn[key])
        except (KeyError, ValueError, TypeError):
            errors.append(f"{path.name}: {key} missing or not a duration")
    limit = defn.get("comm_limit") or {}
    chars = limit.get("chars")
    if not isinstance(chars, int) or chars < 1:
        errors.append(f"{path.name}: comm_limit.chars missing or not a positive integer")
        chars = None
    if not isinstance(limit.get("source"), str):
        errors.append(f"{path.name}: comm_limit carries no source tag")
    else:
        errors.extend(_check_tag(f"{path.name}: comm_limit", limit["source"], registry))

    def check_name(where, name):
        if not isinstance(name, str) or not name:
            errors.append(f"{where}: not a name: {name!r}")
        elif chars is not None and len(name) > chars:
            errors.append(f"{where}: {name!r} exceeds the {chars}-character comm limit")

    sets = defn.get("sets") or {}
    unknown = sorted(set(sets) - set(SETS))
    if unknown:
        errors.append(f"{path.name}: unknown sets {unknown}")
    for name, spec in sets.items():
        where = f"{path.name}: {name}"
        for interval in spec.get("intervals") or []:
            source = interval.get("source")
            if not isinstance(source, str):
                errors.append(f"{where}: interval {interval.get('length')!r} carries no source tag or label")
            elif source not in BOUND_LABELS:
                errors.extend(_check_tag(f"{where}: interval {interval.get('length')}", source, registry))
        split = spec.get("split")
        if split and split.get("by") not in ("pair", "seed"):
            errors.append(f"{where}: split must be by pair or by seed")
        if name == "distractor-grid":
            bad = sorted(set(spec.get("relations") or []) - set(RELATIONS))
            if bad:
                errors.append(f"{where}: unknown relations {bad}")
            for program in spec.get("programs") or []:
                for key in ("name", "archetype", "scenario"):
                    if key not in program:
                        errors.append(f"{where}: program {program.get('name')!r} lacks {key}")
                check_name(f"{where}: program", program.get("name"))
                if "total_work" in program and program["total_work"] != "span":
                    errors.append(f"{where}: program {program['name']!r}: total_work must be `span`")
        if name == "familiarity-ladder":
            if not set(spec.get("tiers") or []) <= {4, 5}:
                errors.append(f"{where}: tiers must be among 4 and 5 (tier 3 is the `tier3` table's)")
            if not set(spec.get("carriers") or []) <= set(CARRIERS):
                errors.append(f"{where}: carriers must be among {sorted(CARRIERS)}")
            letters = spec.get("tier5_letters")
            if not isinstance(letters, int) or letters < 1 or (chars is not None and letters > chars):
                errors.append(f"{where}: tier5_letters must be a positive integer within the comm limit")
            table = spec.get("tier4_names") or {}
            for real, fake in table.items():
                check_name(f"{where}: tier4_names[{real!r}]", fake)
                if fake in table:
                    errors.append(f"{where}: tier-4 name {fake!r} is a real name")
            if len(set(table.values())) != len(table):
                errors.append(f"{where}: tier-4 names are not distinct")
            for mode, entries in (spec.get("tier3") or {}).items():
                for real, entry in entries.items():
                    check_name(f"{where}: tier3[{mode}][{real!r}]", entry.get("name"))
                    source = entry.get("source")
                    if not isinstance(source, str):
                        errors.append(f"{where}: tier3[{mode}][{real!r}] carries no source tag")
                    else:
                        errors.extend(_check_tag(f"{where}: tier3[{mode}][{real!r}]", source, registry))
    return errors
