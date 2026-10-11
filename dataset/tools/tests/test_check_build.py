"""`check_build.py` (9.18 spec, decision 6; 9.19 decision 9): build/ equals the union of every manifest — the core
set's, the variants' and one per generated set the grid definition names."""

import hashlib
import importlib
import json

check_build = importlib.import_module("check_build")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def make_repo(tmp_path):
    dataset = tmp_path / "dataset"
    build = dataset / "build" / "coreset-single"
    build.mkdir(parents=True)
    files = {"coreset-single/a.workload.json": b"A\n", "coreset-single/a.report.json": b"RA\n",
             "coreset-single/a@venue-x0.8.workload.json": b"V\n"}
    for rel, data in files.items():
        (dataset / "build" / rel).write_bytes(data)
    (dataset / "build.manifest.json").write_text(json.dumps({
        "inputs": {}, "artifacts": {"coreset-single/a.workload.json": sha(b"A\n")},
        "reports": {"coreset-single/a.report.json": sha(b"RA\n")}, "demand": {}}))
    (dataset / "build.variants.manifest.json").write_text(json.dumps({
        "inputs": {}, "artifacts": {"coreset-single/a@venue-x0.8.workload.json": {"sha256": sha(b"V\n"), "set": "venue-x0.8"}}}))
    return tmp_path


def test_a_build_equal_to_the_manifests_passes(tmp_path):
    assert check_build.check(make_repo(tmp_path)) == []


def test_a_missing_build_fails(tmp_path):
    root = make_repo(tmp_path)
    import shutil
    shutil.rmtree(root / "dataset" / "build")
    assert check_build.check(root) == ["dataset/build: missing (run `make dataset variants generated` first)"]


def test_a_missing_pinned_file_an_unpinned_file_and_a_drifted_file_are_each_named(tmp_path):
    root = make_repo(tmp_path)
    build = root / "dataset" / "build" / "coreset-single"
    (build / "a.report.json").unlink()
    (build / "stale.workload.json").write_bytes(b"S\n")
    (build / "a@venue-x0.8.workload.json").write_bytes(b"V2\n")
    errors = check_build.check(root)
    assert [e.split(":")[0] for e in errors] == ["build/coreset-single/a.report.json",
                                                 "build/coreset-single/stale.workload.json",
                                                 "build/coreset-single/a@venue-x0.8.workload.json"]
    assert "missing on disk" in errors[0] and "pinned by no manifest" in errors[1] and "differs" in errors[2]


def test_a_generated_sets_manifest_joins_the_union_when_the_grid_definition_names_it(tmp_path):
    root = make_repo(tmp_path)
    dataset = root / "dataset"
    assert check_build.manifests(root) == list(check_build.FIXED_MANIFESTS)
    (dataset / "grids.yaml").write_text(json.dumps({"sets": {"transition-grid": {}}}))
    assert check_build.manifests(root) == [*check_build.FIXED_MANIFESTS, "dataset/build.transition-grid.manifest.json"]
    assert check_build.check(root) == []          # a manifest not yet written pins nothing
    grid = dataset / "build" / "transition-grid-single"
    grid.mkdir()
    (grid / "tr-a-to-b-departs.workload.json").write_bytes(b"G\n")
    (grid / "tr-a-to-b-departs.report.json").write_bytes(b"RG\n")
    assert [e.split(":")[0] for e in check_build.check(root)] == ["build/transition-grid-single/tr-a-to-b-departs.report.json",
                                                                  "build/transition-grid-single/tr-a-to-b-departs.workload.json"]
    (dataset / "build.transition-grid.manifest.json").write_text(json.dumps({
        "inputs": {}, "artifacts": {"transition-grid-single/tr-a-to-b-departs.workload.json": sha(b"G\n")},
        "reports": {"transition-grid-single/tr-a-to-b-departs.report.json": sha(b"RG\n")}, "demand": {}, "grid": {}}))
    assert check_build.check(root) == []
