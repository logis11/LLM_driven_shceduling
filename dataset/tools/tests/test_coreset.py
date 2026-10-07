"""Coreset-level invariants (task-2.4 spec): derive idempotency, the C2
one-entry-diff discipline on the real pair files, and window compliance."""

import pytest

from wlc import Timeline, compile_timeline
from wlc.deriver import DeriveError, apply_ops, run as derive_check
from wlc.linter import lint_canonical


@pytest.fixture(scope="module")
def coreset(repo_root, library):
    compiled = {}
    for path in sorted((repo_root / "dataset" / "timelines").glob(
            "**/*.timeline.yaml")):
        timeline = Timeline(path, library)
        canonical, report = compile_timeline(timeline, library, "single")
        compiled[timeline.id] = (canonical, report)
    return compiled


def test_derive_idempotent(repo_root):
    assert derive_check(repo_root / "dataset" / "timelines", check=True) == []


def events_by_id(canonical):
    return {e["id"]: e for e in canonical["events"] if e["op"] == "arrive"}


def test_p1_pair_differs_in_segment_one_only(coreset):
    """9.10 D6, D80 (restating the rename-only pair): the editor's events and segment 0 byte-identical, the files
    the same length; P1b's hog is the measured index, `file-indexer` shown as `tracker-miner-f`, arriving at 60 s
    as P1a's training run does, shown as `python` (9.10 D84, D86), its segment 1 labelled indexing, false, C long."""
    base, _ = coreset["c2-p1a"]
    variant, _ = coreset["c2-p1b"]
    b, v = events_by_id(base), events_by_id(variant)
    assert set(b) == set(v) == {"editor", "hog"}
    assert b["editor"] == v["editor"]
    assert (b["hog"]["name"], v["hog"]["name"]) == ("python", "tracker-miner-f")
    assert b["hog"]["t"] == v["hog"]["t"] == 60_000_000
    assert base["ground_truth"][0] == variant["ground_truth"][0]
    spans = lambda c: [(g["t_start"], g["t_end"]) for g in c["ground_truth"]]
    assert spans(base) == spans(variant) == [(0, 60_000_000), (60_000_000, 60_000_000 + INDEX_C_US)]
    assert ground_truth(variant)[1] == ("indexing", False)


@pytest.mark.parametrize("pair,changed", [
    (("c2-p2a", "c2-p2b"), "download"),
    (("c2-p3a", "c2-p3b"), "bulk"),
])
def test_pair_one_task_diff(coreset, pair, changed):
    base, _ = coreset[pair[0]]
    variant, _ = coreset[pair[1]]
    base_events, variant_events = events_by_id(base), events_by_id(variant)
    assert set(base_events) == set(variant_events)
    for task_id, event in base_events.items():
        if task_id == changed:
            assert variant_events[task_id] != event
        else:
            assert variant_events[task_id] == event


def test_c4_injection_only(coreset):
    base, _ = coreset["c1-gaming"]
    variant, _ = coreset["c4-gaming"]
    base_events, variant_events = events_by_id(base), events_by_id(variant)
    assert set(variant_events) - set(base_events) == {"injected-chat"}   # 9.10 D23
    for task_id, event in base_events.items():
        assert variant_events[task_id] == event


def test_c5_names_only(coreset):
    base, _ = coreset["c1-media"]
    for tier in ("c5-t3", "c5-t4", "c5-t5"):
        variant, _ = coreset[tier]
        base_events, variant_events = events_by_id(base), events_by_id(variant)
        assert set(base_events) == set(variant_events)
        for task_id, event in base_events.items():
            trimmed = {**variant_events[task_id], "name": event["name"]}
            assert trimmed == event  # identical but for the name


C7_INTERACTIVE = ("browsing", "office", "mail", "dev", "photo", "meeting",
                  "gaming", "media", "video-edit", "idle")
C7_SAME_NAME = ()   # indexing, ml-train, transcode, render, backup: their bases' first C seconds (9.10 D78)
INDEX_C_US = 39_435_000   # 9.10 D78, D80: the index's CPU total, total_work as compiled


def ground_truth(canonical):
    return [(s["mode"], s["attributes"]["background_wanted"])
            for s in canonical["ground_truth"]]


C7_C_US = 26_385_000   # 9.10 D41: the package-upgrade job's measured CPU total, meas-ci:background:2026-10-01


def test_c7_interactive_counterparts_inject_the_upgrade(coreset):
    """9.10 D41 (restating Phase 7 spec decision 5): the base's first C seconds — every base task by its id, name
    and arrival, departing at C — plus exactly one task, the unattended upgrade at 0 s, alive for the whole segment
    on one lane; one segment [0, C), label flipped."""
    for mode in C7_INTERACTIVE:
        base, _ = coreset[f"c1-{mode}"]
        variant, _ = coreset[f"c7-{mode}"]
        base_events, variant_events = events_by_id(base), events_by_id(variant)
        assert set(variant_events) - set(base_events) == {"upgrade"}, mode
        for task_id, event in base_events.items():
            v = variant_events[task_id]
            assert (v["name"], v["t"]) == (event["name"], event["t"]), (mode, task_id)
            assert v.get("depart") == C7_C_US, (mode, task_id)
        upgrade = variant_events["upgrade"]
        assert upgrade["name"] == "unattended-upgr" and upgrade["t"] == 0
        assert ground_truth(base) == [(mode, True)]
        assert ground_truth(variant) == [(mode, False)]
        assert (variant["ground_truth"][0]["t_start"], variant["ground_truth"][0]["t_end"]) == (0, C7_C_US)


C7_COMPILE_C_US = 225_458_000   # 9.10 D56: the module build's CPU as compiled under c7-compile's seed, to the ms below


def test_c7_compile_is_the_module_build_in_place_of_the_users_build(coreset):
    """9.10 D56 (restating Phase 7 spec decision 6): c1-compile's first C seconds — the editor by its id, name and
    arrival, departing at C, its focus 2 s to C − 2 s — with the user's build replaced by the DKMS build, task `dkms`
    on module-build-orchestrator, from 0 s; one segment, labelled false."""
    base, _ = coreset["c1-compile"]
    variant, _ = coreset["c7-compile"]
    b, v = events_by_id(base), events_by_id(variant)
    assert set(b) == set(v) == {"editor", "build"}
    assert (v["editor"]["name"], v["editor"]["t"], v["editor"]["depart"]) == (b["editor"]["name"], b["editor"]["t"], C7_COMPILE_C_US)
    build = v["build"]
    assert (build["name"], build["t"], build["fork_cap"]) == ("dkms", 0, 48)   # D55, D57: cap 8 × 6
    assert {e["name"] for e in build["spawn_table"]} == {"sh", "x86_64-linux-gn", "cc1", "as", "fixdep", "rm", "mkdir", "dirname"}
    assert sum(op["op"] == "FORK" for op in build["program"]) == len(build["spawn_table"])
    assert ground_truth(variant) == [("compile", False)]
    assert (variant["ground_truth"][0]["t_start"], variant["ground_truth"][0]["t_end"]) == (0, C7_COMPILE_C_US)


def test_c7_indexing_is_its_bases_first_c_seconds(coreset):
    """9.10 D78 (D56's form): c1-indexing's first C seconds — the editor by its id, name and arrival, departing at
    C, its focus 2 s to C − 2 s — the same index, `file-indexer` shown as `tracker-miner-f`, from 0 s; one segment,
    labelled false, `initiated: session` (D79)."""
    base, _ = coreset["c1-indexing"]
    variant, _ = coreset["c7-indexing"]
    b, v = events_by_id(base), events_by_id(variant)
    assert set(b) == set(v) == {"editor", "hog"}
    assert (v["editor"]["name"], v["editor"]["t"], v["editor"]["depart"]) == (b["editor"]["name"], b["editor"]["t"], INDEX_C_US)
    assert (b["hog"]["name"], b["hog"]["t"]) == ("tracker-miner-f", 2_000_000)
    assert (v["hog"]["name"], v["hog"]["t"]) == ("tracker-miner-f", 0)
    assert ground_truth(variant) == [("indexing", False)]
    gt = variant["ground_truth"][0]
    assert (gt["t_start"], gt["t_end"]) == (0, INDEX_C_US)
    assert gt["attributes"].get("initiated") == "session" and not gt["attributes"].get("pre_committed_miss")


ML_C_US = 1_389_885_000   # 9.10 D85, D88: the training run's CPU total, meas-ci:background:2026-10-03, total_work as compiled
ML_BASE_US = 1_612_000_000   # c1-ml-train: the smallest whole second by which the run ends under every policy (D17, D78)


def test_c7_ml_train_is_its_bases_first_c_seconds(coreset):
    """9.10 D78's form for the training pair: c1-ml-train's first C seconds — the editor by its id, name and arrival,
    departing at C, its focus 2 s to C − 2 s — the same run, `cpu-batch`'s `python3` shown as `python`, from 0 s; one
    segment, labelled false, still a pre-committed miss. The base binds the run whole from 2 s and ends after it."""
    base, _ = coreset["c1-ml-train"]
    variant, _ = coreset["c7-ml-train"]
    b, v = events_by_id(base), events_by_id(variant)
    assert set(b) == set(v) == {"editor", "hog"}
    assert (v["editor"]["name"], v["editor"]["t"], v["editor"]["depart"]) == (b["editor"]["name"], b["editor"]["t"], ML_C_US)
    assert (b["hog"]["name"], b["hog"]["t"]) == ("python", 2_000_000)
    assert (v["hog"]["name"], v["hog"]["t"]) == ("python", 0)
    assert b["editor"]["depart"] == base["ground_truth"][0]["t_end"] == ML_BASE_US
    assert ground_truth(variant) == [("ml-train", False)]
    gt = variant["ground_truth"][0]
    assert (gt["t_start"], gt["t_end"]) == (0, ML_C_US)
    assert gt["attributes"].get("initiated") == "scheduled" and gt["attributes"].get("pre_committed_miss") is True


TRANSCODE_C_US = 2_970_871_000   # 9.10 D97: the encode's CPU total, meas-ci:background:2026-10-03b, total_work as compiled
TRANSCODE_BASE_US = 4_762_000_000   # c1-transcode: the smallest whole second by which the encode ends under every policy


def test_c7_transcode_is_its_bases_first_c_seconds(coreset):
    """9.10 D78's form for the transcode pair: c1-transcode's first C seconds — the editor by its id, name and arrival,
    departing at C, its focus 2 s to C − 2 s — the same encode, `video-transcoder` shown as `HandBrakeCLI`, from 0 s; one
    segment, labelled false, still a pre-committed miss. The base binds the encode whole from 2 s and ends after it."""
    base, _ = coreset["c1-transcode"]
    variant, _ = coreset["c7-transcode"]
    b, v = events_by_id(base), events_by_id(variant)
    assert set(b) == set(v) == {"video-editor", "batch"}
    assert (v["video-editor"]["name"], v["video-editor"]["t"], v["video-editor"]["depart"]) == (
        b["video-editor"]["name"], b["video-editor"]["t"], TRANSCODE_C_US)
    assert (b["batch"]["name"], b["batch"]["t"]) == ("HandBrakeCLI", 2_000_000)
    assert (v["batch"]["name"], v["batch"]["t"]) == ("HandBrakeCLI", 0)
    assert b["video-editor"]["depart"] == base["ground_truth"][0]["t_end"] == TRANSCODE_BASE_US
    assert ground_truth(variant) == [("transcode", False)]
    gt = variant["ground_truth"][0]
    assert (gt["t_start"], gt["t_end"]) == (0, TRANSCODE_C_US)
    assert gt["attributes"].get("initiated") == "scheduled" and gt["attributes"].get("pre_committed_miss") is True


RENDER_C_US = 16_545_000   # 9.10 D105: the export's measured CPU total, meas-ci:background:2026-10-03c


def test_c7_render_is_its_bases_first_c_seconds(coreset):
    """9.10 D78's form for the render pair: c1-render's first C seconds — the editor by its id, name and arrival,
    departing at C, its focus 2 s to C − 2 s, the preview render at the window's middle (D44, D96) — the same export,
    `cpu-batch`'s `kdenlive_render`, from 0 s; one segment, labelled false, still a pre-committed miss. The base keeps
    its 60 s and binds the export whole from 2 s (D108's ground, D78)."""
    base, _ = coreset["c1-render"]
    variant, _ = coreset["c7-render"]
    b, v = events_by_id(base), events_by_id(variant)
    assert set(b) == set(v) == {"editor", "bulk"}
    assert (v["editor"]["name"], v["editor"]["t"], v["editor"]["depart"]) == (b["editor"]["name"], b["editor"]["t"], RENDER_C_US)
    assert (b["bulk"]["name"], b["bulk"]["t"]) == ("kdenlive_render", 2_000_000)
    assert (v["bulk"]["name"], v["bulk"]["t"]) == ("kdenlive_render", 0)
    assert b["editor"]["depart"] == base["ground_truth"][0]["t_end"] == 60_000_000
    assert ground_truth(variant) == [("render", False)]
    gt = variant["ground_truth"][0]
    assert (gt["t_start"], gt["t_end"]) == (0, RENDER_C_US)
    assert gt["attributes"].get("initiated") == "scheduled" and gt["attributes"].get("pre_committed_miss") is True


BACKUP_C_US = 165_668_000   # 9.10 D119: the scheduled incremental's measured CPU total, meas-ci:background:2026-10-04


def test_c7_backup_is_its_bases_first_c_seconds(coreset):
    """9.10 D78's form for the backup pair: c1-backup's first C seconds — the editor by its id, name and arrival,
    departing at C, its focus 2 s to C − 2 s, the preview render at the window's middle (D44, D96) — the same scheduled
    incremental, `incremental-backup` shown as `deja-dup`, from 0 s; one segment, labelled false, still a pre-committed
    miss. The base binds the backup whole from 2 s and ends by the smallest whole second it needs (D90's form)."""
    base, _ = coreset["c1-backup"]
    variant, _ = coreset["c7-backup"]
    b, v = events_by_id(base), events_by_id(variant)
    assert set(b) == set(v) == {"editor", "bulk"}
    assert (v["editor"]["name"], v["editor"]["t"], v["editor"]["depart"]) == (b["editor"]["name"], b["editor"]["t"], BACKUP_C_US)
    assert (b["bulk"]["name"], b["bulk"]["t"]) == ("deja-dup", 2_000_000)
    assert (v["bulk"]["name"], v["bulk"]["t"]) == ("deja-dup", 0)
    assert b["editor"]["depart"] == base["ground_truth"][0]["t_end"] == 277_000_000
    assert ground_truth(variant) == [("backup", False)]
    gt = variant["ground_truth"][0]
    assert (gt["t_start"], gt["t_end"]) == (0, BACKUP_C_US)
    assert gt["attributes"].get("initiated") == "scheduled" and gt["attributes"].get("pre_committed_miss") is True


def test_p3_pair_segment_one_holds_the_backup_in_both_files(coreset):
    """9.10 D123: pair P3's segment 1 runs from 60 s to the second the backup needs in both files, which keep one length
    and differ only in segment 1's job — the export in c2-p3a, the scheduled incremental shown as `deja-dup` in c2-p3b."""
    base, _ = coreset["c2-p3a"]
    variant, _ = coreset["c2-p3b"]
    spans = lambda c: [(g["t_start"], g["t_end"]) for g in c["ground_truth"]]
    assert spans(base) == spans(variant) == [(0, 60_000_000), (60_000_000, 326_000_000)]
    b, v = events_by_id(base), events_by_id(variant)
    assert (b["bulk"]["name"], b["bulk"]["t"]) == ("kdenlive_render", 60_000_000)
    assert (v["bulk"]["name"], v["bulk"]["t"]) == ("deja-dup", 60_000_000)
    assert b["editor"]["depart"] == v["editor"]["depart"] == 326_000_000


def test_c7_same_name_counterparts_flip_the_label_only(coreset):
    """Phase 7 spec decision 3: events byte-identical to the base, only the
    ground truth differs; each is a pre-committed miss (indexing: 9.10 D78)."""
    for mode in C7_SAME_NAME:
        base, _ = coreset[f"c1-{mode}"]
        variant, _ = coreset[f"c7-{mode}"]
        assert events_by_id(base) == events_by_id(variant), mode
        assert base["events"] == variant["events"], mode
        assert ground_truth(variant) == [(mode, False)]
        attrs = variant["ground_truth"][0]["attributes"]
        assert attrs.get("pre_committed_miss") is True, mode


def test_c7_and_derived_files_declare_calibration(repo_root):
    """Phase 7 spec decision 7: an authored declaration, not inheritance."""
    import yaml
    for path in sorted((repo_root / "dataset" / "timelines" / "coreset").glob(
            "*.variant.yaml")):
        for variant in yaml.safe_load(path.read_text())["variants"]:
            if variant["id"].startswith("c2-"):
                continue
            metas = [op["patch-meta"] for op in variant["ops"] if "patch-meta" in op]
            assert metas == [{"demand": "calibration"}], variant["id"]


def test_c6_fold_names_unchanged(coreset):
    # 9.10 D30: the meeting segment adds the call, a `chrome` task on video-call from 30 s; the browsing
    # tasks are the base's and the process names stay {chrome}, so the canonical set does not change
    base, _ = coreset["c1-browsing"]
    variant, _ = coreset["c6-fold"]
    base_events, variant_events = events_by_id(base), events_by_id(variant)
    assert set(variant_events) - set(base_events) == {"call"}
    for task_id, event in base_events.items():
        assert variant_events[task_id] == event
    assert {e["name"] for e in variant_events.values()} == {e["name"] for e in base_events.values()} == {"chrome"}
    assert len(variant["ground_truth"]) == 2


@pytest.mark.xfail(strict=False, reason="jioh/dataset-rebuild: eight -single files sit below the demand window "
                   "after the 9.5 fold-in (D19); 9.14 redoes the window rule")
def test_windows(coreset, schema):
    for name, (canonical, report) in coreset.items():
        assert lint_canonical(canonical, schema, report=report,
                              mode="single", name=name) == []


def test_variant_cannot_change_seed():
    with pytest.raises(DeriveError, match="unknown op"):
        apply_ops({"meta": {"seed": 1}, "tasks": [], "segments": []},
                  [{"set-seed": 2}], "test")


def test_set_focus_and_operations_replace_the_lists():
    """9.10 D44: a cut counterpart replaces its base's focus windows and operations whole."""
    base = {"meta": {"seed": 1}, "tasks": [], "segments": [],
            "focus": [{"from": "2s", "to": "58s", "task": "a"}],
            "operations": [{"at": "30s", "task": "a", "name": "op"}]}
    out = apply_ops(base, [{"set-focus": [{"from": "2s", "to": "20s", "task": "a"}]},
                           {"set-operations": [{"at": "11s", "task": "a", "name": "op"}]}], "test")
    assert out["focus"] == [{"from": "2s", "to": "20s", "task": "a"}]
    assert out["operations"] == [{"at": "11s", "task": "a", "name": "op"}]
    assert base["focus"][0]["to"] == "58s"   # the base is not touched


# 9.10 D168: the catalog scenario each bound program shows, as D33's rows name them; cpu-batch by its `program`
SCENARIO_OF = {"office-writer": "S1", "web-browser": "S2", "renderer-hidden": "S2", "video-call": "S3",
               "mail-client": "S4", "chat-client": "S5", "image-editor": "S6", "video-editor": "S7",
               "video-transcoder": "S8", "game-task-chain": "S9", "game-client": "S9", "game-download": "S10",
               "code-editor": "S11", "build-orchestrator": "S11", "module-build-orchestrator": "S11",
               "video-player": "S13", "audio-player": "S13", "file-indexer": "S14", "incremental-backup": "S15",
               "file-archiver": "S16", "package-upgrade": "S17", "compositor-shell": "S18", "audio-server": "S18",
               "service-manager": "S18", "message-bus": "S18"}
SCENARIO_OF_PROGRAM = {"kdenlive_render": "S7", "python3": "S12", "spoof": "S2"}   # the spoof shows `chrome` (S2)


def test_every_segment_tags_the_scenarios_of_the_programs_it_shows(repo_root, library):
    # a segment's `scenario` names each catalog scenario whose program is alive in it; a task with no `depart` (a batch
    # job, ending inside its segment) counts in the segment its arrival falls in (9.10 D168)
    for path in sorted((repo_root / "dataset" / "timelines").glob("**/*.timeline.yaml")):
        t = Timeline(path, library)
        for seg in t.segments:
            a, b = seg["t_start"], seg["t_end"]
            shown = set()
            for task in t.tasks:
                if task["depart"] is None:
                    alive = a <= task["arrive"] < b
                else:
                    alive = task["arrive"] < b and task["depart"] > a
                if alive:
                    shown.add(SCENARIO_OF_PROGRAM[task["bind"]["program"]] if task["archetype"] == "cpu-batch"
                              else SCENARIO_OF[task["archetype"]])
            assert set(seg["scenario"]) == shown, f"{t.id} {seg['mode']} {a / 1e6:g}-{b / 1e6:g} s"
