"""The build manifest carries each artifact's static demand estimate, per file and per segment."""

import importlib
import json

compile_tool = importlib.import_module("compile")


def test_manifest_records_demand_per_artifact(repo_root):
    manifest, artifacts, errors, reports = compile_tool.build_all(repo_root)
    assert errors == []
    assert set(manifest["demand"]) == set(artifacts)
    for timeline_id, mode, report in reports:
        entry = next(v for k, v in manifest["demand"].items()
                     if k.endswith(f"-{mode}/{timeline_id}.workload.json"))
        assert entry["utilization"] == round(report["utilization"], 4)
        assert entry["demand_class"] == report["demand_class"]
        # 9.14 decision 4: demand per ground-truth segment, each task's demand spread over its lifetime
        assert [s["index"] for s in entry["segments"]] == list(range(len(report["per_segment"])))
        for seg, rep in zip(entry["segments"], report["per_segment"]):
            assert (seg["t_start_us"], seg["t_end_us"]) == (rep["t_start_us"], rep["t_end_us"])
            assert seg["utilization"] == round(rep["utilization"], 4) >= 0
    # 9.18 spec, decision 8: the compile report beside each artifact, pinned by hash
    assert set(manifest["reports"]) == {compile_tool.report_path(rel) for rel in artifacts}
    for timeline_id, mode, report in reports:
        rel = next(k for k in artifacts if k.endswith(f"-{mode}/{timeline_id}.workload.json"))
        digest = compile_tool.sha256(compile_tool.report_bytes(report))
        assert manifest["reports"][compile_tool.report_path(rel)] == digest


def test_manifest_pins_the_compile_inputs_by_content(repo_root):
    """9.18 spec, decision 5: the library, the schema, the compiler's sources and the streams, each path → sha256."""
    pinned = {p.relative_to(repo_root).as_posix() for p in compile_tool.input_files(repo_root)}
    assert {"dataset/archetypes.yaml", "dataset/schema/workload.schema.json", "dataset/tools/compile.py",
            "dataset/tools/wlc/compiler.py", "dataset/tools/wlc/sampling.py"} <= pinned
    assert any(p.startswith("dataset/stimulus/") and p.endswith(".jsonl") for p in pinned)
    assert any(p.startswith("dataset/replay/") and p.endswith(".json.gz") for p in pinned)
    assert not any("__pycache__" in p for p in pinned)
    manifest = json.loads((repo_root / "dataset" / "build.manifest.json").read_text())
    assert set(manifest["inputs"]) == pinned
    for rel, digest in manifest["inputs"].items():
        assert compile_tool.sha256((repo_root / rel).read_bytes()) == digest, rel
