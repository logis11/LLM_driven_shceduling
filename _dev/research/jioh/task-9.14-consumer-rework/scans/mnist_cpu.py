import sys, os, json
sys.path.insert(0, "/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/dataset/tools")
from meas.campaign.analyze import load_rows, load_all_wakeups, merge_resumes
for D in sys.argv[1:]:
    ts = [l.split("\t") for l in open(os.path.join(D, "taskstats.mnist-train.tsv")) if not l.startswith("#") and not l.startswith("recv")] if os.path.exists(os.path.join(D, "taskstats.mnist-train.tsv")) else []
    pids = {int(r[5]) for r in ts if r[8] == "python"}
    if not pids:
        # find python pid from the timehist itself
        import gzip, re
        pids=set()
        with gzip.open(os.path.join(D,"perf.mnist-train.timehist.txt.gz"),"rt") as h:
            for line in h:
                m = re.search(r"\s(python)\[(\d+)(?:/(\d+))?\]\s", line)
                if m: pids.add(int(m.group(3) or m.group(2)))
    rows, (t0, t1), extra = load_rows(os.path.join(D, "perf.mnist-train.timehist.txt.gz"), pids)
    wakes, merged = merge_resumes(rows, load_all_wakeups(os.path.join(D, "perf.mnist-train.wakeups.txt.gz"), pids))
    print(os.path.basename(D.rstrip('/')), "pids", sorted(pids), "segments", len(rows), "wakes", len(wakes), "merged", merged,
          "perf CPU s %.3f" % (sum(r.run for r in rows)/1000), "span %.1f s" % (t1-t0), "threads", len({r.tid for r in rows}))
