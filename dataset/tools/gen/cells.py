"""The generated layer's cells (9.19 spec): the grid definition, the sixteen modes, the 240 ordered pairs, and each
set's cells — id, placements (which task set holds which segment and how long its tasks live), grid coordinates,
split, seed. Every seed and every split is a keyed SHA-256 draw from the cell's or the pair's id; nothing is chosen
by hand (spec invariants).

A placement is `(mode, start_us, end_us, alive_until_us)`: the mode's C1 task set labels the segment
[start, end) and its tasks live to `alive_until` — the segment's end where they depart at the boundary, the file's
end where they stay (decision 2's `focus` form).
"""

import hashlib
import pathlib
import re

import yaml

from wlc.linter import BOUND_LABELS, _check_tag
from wlc.units import parse_us

SETS = ("transition-grid", "return-grid", "flap-stress")


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


def _cell(set_name, cell_id, a, b, placements, grid, split=None):
    cell = {"id": cell_id, "set": set_name, "a": a, "b": b, "placements": placements, "grid": dict(grid),
            "seed": seed_of(set_name, cell_id)}
    if split is not None:
        cell["split"] = split
    return cell


def transition_cells(defn, pairs):
    """Decision 2. `departs`: A's tasks leave at the boundary, B's arrive. `focus`: B's arrive and take the focus,
    A's stay to the end of the file. Two segments of `segment_length`."""
    L = parse_us(defn["segment_length"])
    out = []
    for a, b in pairs:
        for form in defn["sets"]["transition-grid"]["forms"]:
            a_until = L if form == "departs" else 2 * L
            out.append(_cell("transition-grid", f"tr-{a}-to-{b}-{form}", a, b,
                             [(a, 0, L, a_until), (b, L, 2 * L, 2 * L)], {"a": a, "b": b, "form": form}))
    return out


def return_cells(defn, pairs):
    """Decision 10: A -> B -> A, every task set departing at its boundary; the middle length a variant. Decision 6:
    the pairs ranked by keyed hash, the first `tuning` of them the tuning half, a pair's variants together."""
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
    """Decision 7: a lead-in on A, then `alternations` segments of one interval each, B and A in turn, every task set
    departing at its boundary; `pairs` ordered pairs drawn by keyed hash; each file under two seeds, one per split
    name (decision 6)."""
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


def cells(defn, modes):
    """{set name: [cells]} for every set the definition names."""
    pairs = ordered_pairs(modes)
    builders = {"transition-grid": transition_cells, "return-grid": return_cells, "flap-stress": flap_cells}
    return {name: builders[name](defn, pairs) for name in defn["sets"]}


def lint_grids(path, registry):
    """The definition's form, and every interval's `source` a registry tag or a label (the bound-value rule, 9.18)."""
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
    return errors
