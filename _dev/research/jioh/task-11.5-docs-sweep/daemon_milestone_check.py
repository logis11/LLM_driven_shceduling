"""The daemon guide's first milestone, checked on the whole core set: daemon.py against the harness's mock daemon
(byte for byte, schedule and log) and against its own rerun, for every core file under fixed, oracle and random
(seed 1) and both telemetry shapes. Uses the integration gate's comparison as written."""
import concurrent.futures, json, pathlib, subprocess, sys, tempfile, threading, time, types

REPO = pathlib.Path("/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling")
sys.path.insert(0, str(REPO / "harness" / "tools"))
from harness.integration import compare_daemon_run, daemon_argv  # noqa: E402

PY = "python3.12"
real = types.SimpleNamespace(command=[PY, str(REPO / "daemon" / "daemon.py")])
mock = types.SimpleNamespace(command=[PY, str(REPO / "harness" / "tools" / "tests" / "mocks" / "mock_daemon.py")])
table = REPO / "daemon" / "driver-table" / "prior.yaml"
boot = REPO / "harness" / "boot-defaults" / "ostep.json"
files = sorted(p for p in (REPO / "dataset" / "build" / "coreset-single").glob("*.workload.json") if "@" not in p.name)
runs = []
for f in files:
    for cond, seed in (("fixed", None), ("oracle", None), ("random", "1")):
        for tel in ("focus", "names"):
            runs.append(types.SimpleNamespace(workload_id=f.name.split(".")[0], name=f"{cond}/{tel}",
                                              workload_file=f, table_file=None, boot_file=boot,
                                              condition=cond, seed=seed, telemetry=tel))


def rerun_identical(run, tmp_root):
    outs = []
    for i in range(2):
        with tempfile.TemporaryDirectory(dir=tmp_root) as d:
            out = pathlib.Path(d)
            p = subprocess.run(daemon_argv(real.command, run, table, out), stdout=subprocess.DEVNULL,
                               stderr=subprocess.PIPE, text=True)
            if p.returncode:
                return f"exit {p.returncode}: {p.stderr.strip()[-200:]}"
            outs.append({n: (out / n).read_bytes() for n in ("schedule.json", "log.json")})
    return None if outs[0] == outs[1] else "rerun differs"


t0 = time.time()
big = threading.Semaphore(2)
vs_mock, rerun = [], []
with tempfile.TemporaryDirectory() as tmp:
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        a = [pool.submit(compare_daemon_run, real, mock, r, table, tmp, big) for r in runs]
        b = [pool.submit(rerun_identical, r, tmp) for r in runs]
        for r, fa, fb in zip(runs, a, b):
            ident, what = fa.result()
            if what:
                vs_mock.append((ident, what))
            w = fb.result()
            if w:
                rerun.append((f"{r.workload_id}/{r.name}", w))
result = {"files": len(files), "runs": len(runs), "identical_to_mock": len(runs) - len(vs_mock),
          "rerun_identical": len(runs) - len(rerun), "differing_from_mock": vs_mock[:20],
          "rerun_differing": rerun[:20], "wall_seconds": round(time.time() - t0, 1),
          "daemon_version": subprocess.run(["make", "-s", "-C", str(REPO / "daemon"), "version"],
                                           capture_output=True, text=True).stdout.strip()}
print(json.dumps(result, indent=1))
