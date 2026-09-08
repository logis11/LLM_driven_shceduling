"""The parse boundary (daemon-guide §2.1, §3).

Two kinds of test here, and the first kind matters more: the *negative* tests,
which assert that behavioral information is unreachable from a Projection.
They are the machine-checked form of the experiment's central information rule
— if one of them ever fails, a result produced by that build is unpublishable,
not merely wrong.
"""

import dataclasses
import json

import pytest
from conftest import needs_corpus

from daemon.errors import ProjectionError
from daemon.projection import ChildGroup, Projection, TaskView, read_projection


def _walk(value, seen=None):
    """Every object reachable from `value`, following dataclass fields and
    containers — the search a leak would have to survive."""
    seen = set() if seen is None else seen
    if id(value) in seen:
        return
    seen.add(id(value))
    yield value
    if dataclasses.is_dataclass(value):
        for field in dataclasses.fields(value):
            yield from _walk(getattr(value, field.name), seen)
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from _walk(key, seen)
            yield from _walk(item, seen)
    elif isinstance(value, (list, tuple, set)):
        for item in value:
            yield from _walk(item, seen)


class TestParseBoundary:
    def test_nothing_behavioral_is_reachable(self, fixtures):
        """No program, no instruction, no task id, no ground-truth label — the
        projection carries names, counts and pinned times or it carries a bug."""
        projection = read_projection(fixtures / "mini.workload.json")
        forbidden = {"RUN", "SLEEP", "TIMER", "WAIT", "WAKE", "FORK", "EXIT",
                     "editor", "build", "build.c1", "build.c2", "build.c3",
                     "dev", "compile", "background_wanted", "input:editor"}
        strings = {v for v in _walk(projection) if isinstance(v, str)}
        assert not (strings & forbidden), f"leaked: {sorted(strings & forbidden)}"

    def test_no_raw_document_is_retained(self, fixtures):
        """A dict anywhere in the returned value would be a door back to the
        file. The projection is dataclasses, tuples and scalars only."""
        projection = read_projection(fixtures / "mini.workload.json")
        assert not [v for v in _walk(projection) if isinstance(v, (dict, list))]

    def test_frozen_all_the_way_down(self, fixtures):
        projection = read_projection(fixtures / "mini.workload.json")
        for obj in (projection, projection.tasks[0]):
            with pytest.raises(dataclasses.FrozenInstanceError):
                obj.workload_id = "rewritten"  # noqa: B010


class TestWhatSurvives:
    def test_mini(self, fixtures):
        projection = read_projection(fixtures / "mini.workload.json")
        assert projection == Projection(
            workload_id="mini",
            tasks=(
                TaskView(name="code", t_arrive=0, t_depart=2000000, children=()),
                TaskView(name="make", t_arrive=1000000, t_depart=None,
                         children=(ChildGroup(name="cc1", count=2),
                                   ChildGroup(name="ld", count=1))),
            ))

    def test_spawn_table_folds_to_name_counts_sorted(self, fixtures):
        make = read_projection(fixtures / "mini.workload.json").tasks[1]
        assert [(c.name, c.count) for c in make.children] == [("cc1", 2), ("ld", 1)]

    def test_missing_depart_is_none_not_zero(self, fixtures):
        """`make` ends when it finishes, and when that is depends on the
        scheduler — a result, never an input. None is the only honest value."""
        assert read_projection(fixtures / "mini.workload.json").tasks[1].t_depart is None

    def test_wake_events_are_skipped_not_refused(self, fixtures):
        """mini has a wake event; a wake changes no process's existence, so it
        contributes no task and must not refuse the file."""
        assert len(read_projection(fixtures / "mini.workload.json").tasks) == 2

    def test_to_json_matches_the_guide_shape(self, fixtures):
        assert read_projection(fixtures / "mini.workload.json").to_json() == {
            "workload_id": "mini",
            "tasks": [
                {"name": "code", "t_arrive": 0, "depart": 2000000},
                {"name": "make", "t_arrive": 1000000,
                 "children": [{"name": "cc1", "count": 2},
                              {"name": "ld", "count": 1}]},
            ]}


class TestOrdering:
    def test_sorted_by_arrival_then_name(self, tmp_path, fixtures):
        """File order must not reach the output: shuffling the events changes
        nothing, which is what makes reruns byte-identical."""
        document = json.loads((fixtures / "mini.workload.json").read_text())
        document["events"] = list(reversed(document["events"]))
        path = tmp_path / "shuffled.workload.json"
        path.write_text(json.dumps(document))
        assert read_projection(path).tasks == \
            read_projection(fixtures / "mini.workload.json").tasks


class TestRefusals:
    @pytest.mark.parametrize("mutate, message", [
        (lambda d: d.pop("ground_truth"), "not a canonical workload file"),
        (lambda d: d.pop("events"), "not a canonical workload file"),
        (lambda d: d["meta"].pop("id"), "meta.id"),
        (lambda d: d.update(events=[]), "no arrive events"),
        (lambda d: d["events"][0].update(t=-1), "non-negative integer"),
        (lambda d: d["events"][0].update(t=True), "non-negative integer"),
        (lambda d: d["events"][2].update(depart=0), "before it arrives"),
        (lambda d: d["events"][0].pop("name"), "no usable name"),
        (lambda d: d["events"][2].update(spawn_table=[{"id": "x"}]), "without a name"),
    ])
    def test_refused_with_the_file_named(self, tmp_path, fixtures, mutate, message):
        document = json.loads((fixtures / "mini.workload.json").read_text())
        mutate(document)
        path = tmp_path / "broken.workload.json"
        path.write_text(json.dumps(document))
        with pytest.raises(ProjectionError) as excinfo:
            read_projection(path)
        assert message in str(excinfo.value)
        assert "broken.workload.json" in str(excinfo.value)

    def test_not_json(self, tmp_path):
        path = tmp_path / "junk.workload.json"
        path.write_text("{not json")
        with pytest.raises(ProjectionError, match="not JSON"):
            read_projection(path)

    def test_missing_file(self, tmp_path):
        with pytest.raises(ProjectionError, match="cannot be opened"):
            read_projection(tmp_path / "absent.workload.json")


@needs_corpus
class TestRealCorpus:
    def test_every_coreset_file_projects(self, corpus):
        for workload_id in corpus.workload_ids:
            projection = read_projection(corpus.path(workload_id))
            assert projection.workload_id == workload_id
            assert projection.tasks

    def test_c1_compile_is_the_guide_example(self, corpus):
        """daemon-guide §3 prints this projection; it must still be true."""
        assert read_projection(corpus.path("c1-compile")).to_json() == {
            "workload_id": "c1-compile",
            "tasks": [
                {"name": "code", "t_arrive": 0, "depart": 60000000},
                {"name": "make", "t_arrive": 2000000,
                 "children": [{"name": "cc1", "count": 100}]},
            ]}

    def test_duplicate_names_stay_separate_tasks(self, corpus):
        """c6-spoof is thirteen `chrome` plus a fourteenth arriving later; the
        projection keeps fourteen tasks and lets the telemetry builder count
        them (data-contracts §5, rule 1)."""
        tasks = read_projection(corpus.path("c6-spoof")).tasks
        chromes = [t for t in tasks if t.name == "chrome"]
        assert len(chromes) == 14
        assert sum(1 for t in chromes if t.t_arrive > 0) == 1

    def test_reading_is_deterministic(self, corpus):
        for workload_id in corpus.workload_ids:
            first = read_projection(corpus.path(workload_id))
            assert first == read_projection(corpus.path(workload_id))
