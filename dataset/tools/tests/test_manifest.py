"""The build manifest carries each artifact's static demand estimate."""

import importlib

compile_tool = importlib.import_module("compile")


def test_manifest_records_demand_per_artifact(repo_root):
    manifest, artifacts, errors, reports = compile_tool.build_all(repo_root)
    assert not errors
    assert set(manifest["demand"]) == set(artifacts)
    for timeline_id, mode, report in reports:
        entry = next(v for k, v in manifest["demand"].items()
                     if k.endswith(f"-{mode}/{timeline_id}.workload.json"))
        assert entry == {
            "utilization": round(report["utilization"], 4),
            "demand_class": report["demand_class"],
        }
