import sys, os, glob
sys.path.insert(0, "/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/dataset/tools")
from meas import replay_fold_in as rf
spec = rf.SOURCES["package-upgrade"]
for D in sys.argv[1:]:
    streams, comms, phase_us, reading = rf.read_runs(D, spec)
    ts = [l.split("\t") for l in open(os.path.join(D, "taskstats.upgrade-install.tsv")) if not l.startswith("#") and not l.startswith("recv")]
    tcpu = sum((float(r[15]) + float(r[16])) for r in ts if r[2] == "pid") / 1e6
    print(f"{os.path.basename(D):40s} perf CPU {reading['cpu_s']:8.3f} s  taskstats {tcpu:8.3f} s  runs {reading['runs']}  procs {reading['processes']}  span {reading['span_s']} s")
