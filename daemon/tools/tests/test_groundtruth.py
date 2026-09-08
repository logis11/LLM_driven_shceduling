"""The answer-key reader (data-contracts §4, recognition-vocabulary §1).

The load-bearing tests are the ones about `c6-dual`: the oracle's *semantics*
on an off-menu label are deferred, but its *survival* is not. A reader that
raises on `mode: ambiguous` or on a missing `background_wanted` would kill a
24-file sweep at its last stage (daemon-guide §4).
"""

import pytest
from conftest import needs_corpus

from daemon.errors import GroundTruthError
from daemon.groundtruth import read_ground_truth


class TestReading:
    def test_segments_and_attributes(self, fixtures):
        key = read_ground_truth(fixtures / "mini.workload.json")
        assert key.workload_id == "mini"
        assert [(s.t_start, s.t_end, s.mode) for s in key.segments] == [
            (0, 1000000, "dev"), (1000000, 2000000, "compile")]
        assert key.segments[0].attributes == {"background_wanted": True}
        assert key.segments[0].familiarity == 2
        assert key.segments[1].familiarity is None

    def test_grading_annotations_are_carried_not_stripped(self, fixtures):
        """`background` and `initiated` are grading split keys; the reader keeps
        them, and it is the recognizer side that never sees any of this."""
        key = read_ground_truth(fixtures / "mini.workload.json")
        assert key.segments[1].attributes["initiated"] == "user"

    def test_covering_is_half_open(self, fixtures):
        key = read_ground_truth(fixtures / "mini.workload.json")
        assert key.covering(0).mode == "dev"
        assert key.covering(999999).mode == "dev"
        assert key.covering(1000000).mode == "compile"

    def test_past_the_end_is_none_not_an_error(self, fixtures):
        """The terminal snapshot lands here (data-contracts §5, rule 4) and the
        grader skips it; the oracle must get None, not an exception."""
        assert read_ground_truth(fixtures / "mini.workload.json").covering(2000000) is None


class TestOffMenuLabels:
    def test_ambiguous_mode_is_returned_not_refused(self, fixtures):
        """c6-dual's shape. `ambiguous` is not on the recognizer's menu; the
        reader reports it faithfully and lets the validator reject downstream."""
        key = read_ground_truth(fixtures / "ambiguous.workload.json")
        assert key.covering(0).mode == "ambiguous"

    def test_missing_background_wanted_is_not_defaulted(self, fixtures):
        """Substituting a value here would put our judgment inside the oracle's
        answer — the one thing the oracle must not contain."""
        key = read_ground_truth(fixtures / "ambiguous.workload.json")
        assert "background_wanted" not in key.covering(0).attributes


class TestRefusals:
    def test_not_a_canonical_file(self, tmp_path):
        path = tmp_path / "x.json"
        path.write_text('{"meta": {"id": "x"}, "events": []}')
        with pytest.raises(GroundTruthError, match="no ground_truth"):
            read_ground_truth(path)

    def test_inverted_interval(self, tmp_path):
        path = tmp_path / "x.json"
        path.write_text('{"meta": {"id": "x"}, "events": [], "ground_truth": '
                        '[{"t_start": 10, "t_end": 5, "mode": "dev"}]}')
        with pytest.raises(GroundTruthError, match="at or before its start"):
            read_ground_truth(path)


@needs_corpus
class TestRealCorpus:
    def test_every_coreset_file_has_a_readable_key(self, corpus):
        for workload_id in corpus.workload_ids:
            key = read_ground_truth(corpus.path(workload_id))
            assert key.segments

    def test_c6_dual_survives(self, corpus):
        """The real file, not a fixture: the sweep must not die here. c6-dual is
        one `ambiguous` segment carrying `dual_active` and no
        `background_wanted` (recognition-vocabulary §1)."""
        key = read_ground_truth(corpus.path("c6-dual"))
        segment = key.covering(0)
        assert segment.mode == "ambiguous"
        assert segment.attributes == {"dual_active": True}
