"""Linter behavior: repo lints on the real repo, the freeze gate, the
registry subset rule, timeline structural rules, and the demand window."""

import pytest
import yaml

from wlc import Timeline, TimelineError, compile_timeline
from wlc.linter import lint_canonical, lint_repo


def test_real_repo_lint_clean(repo_root):
    errors = lint_repo(repo_root / "dataset" / "archetypes.yaml",
                       repo_root / "dataset" / "sources.yaml",
                       repo_root / "docs" / "references.md")
    assert errors == []


def test_repo_is_freeze_clean(repo_root):
    """All meas-pending placeholders have been folded in (cli:3/gui:2)."""
    errors = lint_repo(repo_root / "dataset" / "archetypes.yaml",
                       repo_root / "dataset" / "sources.yaml",
                       repo_root / "docs" / "references.md", freeze=True)
    assert errors == []


PROBE_ENTRY = (
    "archetypes:\n"
    "  probe:\n"
    "    category_source: meas\n"
    "    declared_class: {declared_class}\n"
    "    pattern: {{program: []}}\n"
    "    params:\n"
    "      x: {{dist: constant, value_us: 1, sampling: per-task,\n"
    "          source: {source}}}\n"
    "    lifetime: finite\n"
    "    binding_params: []\n"
    "    scalable: []\n"
    "    validation_stats: {{}}\n"
    "    modeling_notes: probe\n")


def test_freeze_rejects_meas_pending(repo_root, tmp_path):
    archetypes = tmp_path / "archetypes.yaml"
    archetypes.write_text(PROBE_ENTRY.format(declared_class="normal", source="meas-pending"))
    sources = repo_root / "dataset" / "sources.yaml"
    references = repo_root / "docs" / "references.md"
    assert lint_repo(archetypes, sources, references, freeze=False) == []
    errors = lint_repo(archetypes, sources, references, freeze=True)
    assert errors == ["probe.x: meas-pending after freeze"]


def test_repo_lint_requires_declared_class(repo_root, tmp_path):
    """9.13 spec decisions 2 and 8: every entry carries `declared_class` from the closed set; no default."""
    sources = repo_root / "dataset" / "sources.yaml"
    references = repo_root / "docs" / "references.md"
    archetypes = tmp_path / "archetypes.yaml"
    text = PROBE_ENTRY.format(declared_class="normal", source="meas-ci:background:2026-09-19")
    archetypes.write_text(text.replace("    declared_class: normal\n", ""))
    assert lint_repo(archetypes, sources, references) == ["probe: missing field 'declared_class'"]
    archetypes.write_text(PROBE_ENTRY.format(declared_class="nice", source="meas-ci:background:2026-09-19"))
    assert lint_repo(archetypes, sources, references) == ["probe: bad declared_class 'nice'"]
    archetypes.write_text(PROBE_ENTRY.format(declared_class="idle", source="meas-ci:background:2026-09-19"))
    assert lint_repo(archetypes, sources, references) == []


def canonical_of(program, spawned=None):
    """A minimal schema-valid file around one task's program — with `spawned`, the task forks one child carrying it."""
    task = {"t": 0, "op": "arrive", "id": "a", "name": "x", "declared_class": "normal", "program": program}
    if spawned is not None:
        task["program"] = [{"op": "FORK"}, {"op": "WAIT", "channel": "children:a"}, {"op": "EXIT"}]
        task["spawn_table"] = [{"id": "a.c", "name": "y", "declared_class": "normal", "program": spawned}]
        task["fork_cap"] = 1
    else:
        task["depart"] = 1_000_000
    return {"meta": {"id": "t", "derived_from": "t.timeline.yaml@abcdef1",
                     "sampled": {"seed": 1, "archetypes": "archetypes.yaml@abcdef1"}},
            "ground_truth": [], "events": [task]}


TIMER, RUN = {"op": "TIMER", "period_us": 10}, {"op": "RUN", "us": 5}


@pytest.mark.parametrize("program,ok", [
    ([TIMER, RUN], True),                                                   # TIMER literally first
    ([{"op": "LOOP", "count": "unbounded", "body": [TIMER, RUN]}], True),   # a LOOP head whose body begins with TIMER
    ([RUN, TIMER], False),                                                  # a run before the first tick
    ([{"op": "LOOP", "count": "unbounded", "body": [RUN, TIMER]}], False),
    ([{"op": "WAIT", "channel": "timer:a"}, RUN, TIMER], False),            # a wait before the first tick
    ([{"op": "WAIT", "channel": "timer:a"}, RUN], True),                    # no TIMER: the rule does not apply
])
def test_timer_first_invariant(schema, program, ok):
    """9.11 D11, D33 (9.13 spec decision 8): a program that contains a TIMER anywhere has a TIMER as its first
    executed instruction, descending LOOP heads, so TIMER's t₀ — its first execution — is the task's arrival."""
    errors = lint_canonical(canonical_of(program), schema)
    assert (errors == []) == ok, errors
    if not ok:
        assert len(errors) == 1 and errors[0].startswith("a: TIMER") and "first executed" in errors[0]


def test_timer_first_invariant_covers_spawned_tasks(schema):
    errors = lint_canonical(canonical_of(None, spawned=[RUN, TIMER, {"op": "EXIT"}]), schema)
    assert len(errors) == 1 and errors[0].startswith("a.c: TIMER")
    assert lint_canonical(canonical_of(None, spawned=[TIMER, RUN, {"op": "EXIT"}]), schema) == []


def test_library_declared_classes(library):
    """9.13 spec decisions 2 and 4: `idle` on `file-indexer` and `incremental-backup` and on the bounding check's
    `game-download-idle`, `normal` on every other entry; the variant shares its base's tables by reference."""
    classes = {aid: library.entry(aid)["declared_class"] for aid in library.entries}
    assert {aid for aid, c in classes.items() if c == "idle"} == {"file-indexer", "incremental-backup",
                                                                   "game-download-idle"}
    assert set(classes.values()) <= {"normal", "idle"}
    base, idle = library.entry("game-download"), library.entry("game-download-idle")
    for field in ("params", "pattern", "lifetime", "binding_params", "scalable", "validation_stats"):
        assert idle[field] == base[field]


def test_registry_subset_rule(repo_root, tmp_path):
    sources = tmp_path / "sources.yaml"
    sources.write_text((repo_root / "dataset" / "sources.yaml").read_text()
                       + "\n  ghost-source:\n    type: scholarly\n"
                         "    notes: not in references\n")
    errors = lint_repo(repo_root / "dataset" / "archetypes.yaml", sources,
                       repo_root / "docs" / "references.md")
    assert errors == ["registry id 'ghost-source' has no docs/references.md "
                      "entry (subset lint)"]


BASE = {
    "meta": {"id": "bad", "seed": 1, "demand": "calibration"},
    "segments": [{"from": "0s", "to": "10s", "mode": "office",
                  "attributes": {"background_wanted": True}}],
    "tasks": [{"id": "player", "name": "mpv", "archetype": "audio-player",
               "arrive": "0s", "depart": "10s"}],
}


def load_bad(tmp_path, mutate):
    data = {"meta": dict(BASE["meta"]),
            "segments": [dict(s) for s in BASE["segments"]],
            "tasks": [dict(t) for t in BASE["tasks"]], "focus": []}
    mutate(data)
    path = tmp_path / "bad.timeline.yaml"
    path.write_text(yaml.safe_dump(data))
    return path


@pytest.mark.parametrize("expect,mutate", [
    ("unknown archetype",
     lambda d: d["tasks"][0].update(archetype="nonesuch")),
    ("not in 'audio-player' binding_params",
     lambda d: d["tasks"][0].update(bind={"burst_len": 5})),
    ("missing bind keys",
     lambda d: d["tasks"].append({"id": "job", "name": "7z",
                                  "archetype": "file-archiver", "arrive": "0s"})),
    ("depart missing but archetype lifetime is 'segment-bound'",
     lambda d: d["tasks"][0].pop("depart")),
    ("depart present but archetype lifetime is 'finite'",
     lambda d: d["tasks"].append({"id": "job", "name": "python3",
                                  "archetype": "cpu-batch", "arrive": "0s",
                                  "depart": "5s",
                                  "bind": {"total_work": "1s", "program": "python3"}})),
    ("spawned-only",
     lambda d: d["tasks"].append({"id": "kid", "name": "cc1",
                                  "archetype": "compiler-child", "arrive": "0s"})),
    ("duplicate task id",
     lambda d: d["tasks"].append(dict(d["tasks"][0]))),
    ("segments overlap",
     lambda d: d["segments"].append({"from": "5s", "to": "15s", "mode": "x",
                                     "attributes": {"background_wanted": True}})),
    ("no input channel",
     lambda d: d["focus"].append({"from": "1s", "to": "2s", "task": "player"})),
    ("focus windows overlap",
     lambda d: (d["tasks"].append({"id": "ed", "name": "code",
                                   "archetype": "code-editor",
                                   "arrive": "0s", "depart": "10s"}),
                d["focus"].extend([{"from": "1s", "to": "5s", "task": "ed"},
                                   {"from": "4s", "to": "6s", "task": "ed"}]))),
    ("outside task",
     lambda d: (d["tasks"].append({"id": "ed", "name": "code",
                                   "archetype": "code-editor",
                                   "arrive": "2s", "depart": "10s"}),
                d["focus"].append({"from": "1s", "to": "5s", "task": "ed"}))),
    ("meta.demand",
     lambda d: d["meta"].update(demand="whatever")),
    ("segment 'office': background_wanted missing",
     lambda d: d["segments"][0].pop("attributes")),
    ("segment 'office': background_wanted must be a boolean",
     lambda d: d["segments"][0].update(attributes={"background_wanted": "yes"})),
    ("segment 'ambiguous': background_wanted must be absent",
     lambda d: d["segments"][0].update(
         mode="ambiguous", attributes={"background_wanted": True})),
])
def test_timeline_rules(tmp_path, library, expect, mutate):
    with pytest.raises(TimelineError, match=expect):
        Timeline(load_bad(tmp_path, mutate), library)


def test_demand_window_enforced(tmp_path, library, schema):
    """An underloaded default-class file fails -single lint; the calibration
    class is exempt."""
    data = {"meta": {"id": "under", "seed": 1},
            "segments": [{"from": "0s", "to": "60s", "mode": "office",
                          "attributes": {"background_wanted": True}}],
            "tasks": [{"id": "job", "name": "python3", "archetype": "cpu-batch",
                       "arrive": "0s",
                       "bind": {"total_work": "20s", "program": "python3"}}]}
    path = tmp_path / "under.timeline.yaml"
    path.write_text(yaml.safe_dump(data))
    timeline = Timeline(path, library)

    canonical, report = compile_timeline(timeline, library, "single")
    errors = lint_canonical(canonical, schema, report=report, mode="single")
    assert len(errors) == 1 and "outside" in errors[0]

    data["meta"]["demand"] = "calibration"
    path.write_text(yaml.safe_dump(data))
    timeline = Timeline(path, library)
    canonical, report = compile_timeline(timeline, library, "single")
    assert lint_canonical(canonical, schema, report=report, mode="single") == []


def test_a_heavy_event_states_its_runs_and_no_gap(tmp_path):
    # 9.5 D64: chrome's MemoryInfra pass is carried as its own stated event — its runs, their count and the span they
    # were counted over. It states no interval, because no repeat held two of them to measure one.
    import yaml
    from wlc import linter
    ev = {"comm": "MemoryInfra", "run_floor_ms": 30, "count": 8, "span_s": 22800.1, "rate_per_s": 0.000351,
          "run": {"dist": "quantiles", "p": [50939, 50939, 52001, 53255, 54695, 55068, 59377, 59997, 59997, 59997],
                  "sampling": "per-iteration", "source": "meas-ci"}}
    lib = {"archetypes": {"web-browser": {"category_source": "meas", "lifetime": "segment-bound",
                                          "pattern": {"program": []}, "params": {"heavy_events": [ev]}}}}
    a = tmp_path / "archetypes.yaml"; a.write_text(yaml.safe_dump(lib))
    src = tmp_path / "sources.yaml"; src.write_text(yaml.safe_dump({"sources": {"meas-ci": {"type": "measurement"}}}))
    refs = tmp_path / "references.md"; refs.write_text("- `meas-ci` — the campaign's own runs\n")
    errs = linter.lint_repo(str(a), str(src), str(refs))
    assert not [e for e in errs if "heavy_events" in e], errs

    ev_gap = dict(ev, gap=ev["run"])
    lib["archetypes"]["web-browser"]["params"]["heavy_events"] = [ev_gap]
    a.write_text(yaml.safe_dump(lib))
    errs = linter.lint_repo(str(a), str(src), str(refs))
    assert any("states no gap" in e for e in errs), errs
