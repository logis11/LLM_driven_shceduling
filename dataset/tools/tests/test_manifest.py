"""The build manifest carries each artifact's static demand estimate, per file and per segment."""

import importlib

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
