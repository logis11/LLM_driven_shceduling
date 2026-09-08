"""The corpus gate (dataset/build.manifest.json).

The workload files are build output and are not committed, so "the daemon ran
against the right inputs" is a claim that needs checking rather than assuming.
A sweep that quietly consumed a stale build would emit recognition logs nobody
can reproduce — the failure the manifest exists to prevent.
"""

import hashlib
import json

import pytest
from conftest import needs_corpus

from daemon.corpus import CORESET_SIZE, Corpus, open_corpus
from daemon.errors import CorpusError


def _fake_build(tmp_path, files, digest_of=None):
    """A miniature build tree plus its manifest."""
    build = tmp_path / "build"
    (build / "coreset-single").mkdir(parents=True)
    artifacts = {}
    for name, content in files.items():
        path = build / "coreset-single" / name
        path.write_text(content)
        artifacts[f"coreset-single/{name}"] = (
            digest_of or (lambda c: hashlib.sha256(c.encode()).hexdigest()))(content)
    artifacts["coreset-native/ignored.workload.json"] = "0" * 64
    manifest = tmp_path / "build.manifest.json"
    manifest.write_text(json.dumps({"artifacts": artifacts}))
    return build, manifest


class TestVerification:
    def test_clean_build_has_no_problems(self, tmp_path):
        build, manifest = _fake_build(tmp_path, {"a.workload.json": "{}"})
        problems = Corpus(build, manifest).verify()
        assert [p for p in problems if "sha256" in p or "missing" in p] == []

    def test_modified_file_is_caught(self, tmp_path):
        build, manifest = _fake_build(tmp_path, {"a.workload.json": "{}"})
        (build / "coreset-single" / "a.workload.json").write_text('{"changed": 1}')
        assert any("sha256" in p for p in Corpus(build, manifest).verify())

    def test_missing_file_names_the_fix(self, tmp_path):
        build, manifest = _fake_build(tmp_path, {"a.workload.json": "{}"})
        (build / "coreset-single" / "a.workload.json").unlink()
        problems = Corpus(build, manifest).verify()
        assert any("missing" in p and "make -C dataset dataset" in p
                   for p in problems)

    def test_wrong_file_count_is_a_problem(self, tmp_path):
        """A manifest with the wrong number of coreset files is a build the
        experiment should not run on, even if every hash matches."""
        build, manifest = _fake_build(tmp_path, {"a.workload.json": "{}"})
        assert any(f"expected the {CORESET_SIZE}-file coreset" in p
                   for p in Corpus(build, manifest).verify())

    def test_only_the_selected_variant_is_considered(self, tmp_path):
        """`coreset-native` is built but unused; its rows must not leak in."""
        build, manifest = _fake_build(tmp_path, {"a.workload.json": "{}"})
        assert Corpus(build, manifest).workload_ids == ("a",)

    def test_unknown_variant_refused(self, tmp_path):
        build, manifest = _fake_build(tmp_path, {"a.workload.json": "{}"})
        with pytest.raises(CorpusError, match="no artifacts for variant"):
            Corpus(build, manifest, variant="nope")

    def test_missing_manifest_names_the_fix(self, tmp_path):
        with pytest.raises(CorpusError, match="make -C dataset dataset"):
            Corpus(tmp_path / "build", tmp_path / "absent.json")


@needs_corpus
class TestRealCorpus:
    def test_the_build_matches_the_manifest(self, corpus):
        assert corpus.verify() == []

    def test_twenty_four_workloads(self, corpus):
        assert len(corpus.workload_ids) == CORESET_SIZE

    def test_pin_covers_every_file(self, corpus):
        pin = corpus.pin()
        assert len(pin) == CORESET_SIZE
        assert all(len(digest) == 64 for digest in pin.values())

    def test_default_variant_is_the_single_lane_build(self, repo_root):
        """Experiments run on the single-lane compile mode
        (workload/building-plan §2)."""
        assert open_corpus(repo_root).variant == "coreset-single"
