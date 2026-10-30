"""fixed_check.py OUT — under fixed at 10 000 µs: for c7-meeting's call and c7-media's two
players, the share of boost intervals holding a demotion (table.py's reading) and the job miss
rate by the aggregates' rule (a job late past its period, or skipped); for the editors whose
input_latency terms the scoring spec scores, their demotions."""
import csv, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from table import shares

out = sys.argv[1]
print("| file | task | boost intervals with a demotion | jobs | missed (skipped) | miss rate |")
print("|---|---|---|---|---|---|")
for f, tasks in (("c7-meeting", ("voice",)), ("c7-media", ("video", "music"))):
    s = shares(f"{out}/{f}.10000.jsonl", tasks)
    rows = [r for r in csv.DictReader(open(f"{out}/{f}.10000.records.csv")) if r["metric"] == "job"]
    for task in tasks:
        jobs = [r for r in rows if r["entity"] == task]
        skipped = sum(r["skipped"] == "1" for r in jobs)
        late = sum(r["skipped"] != "1" and float(r["value"]) > float(r["period_us"]) for r in jobs)
        print(f"| {f} | {task} | {s[task]:.2f} | {len(jobs)} | {late + skipped} ({skipped}) | {(late + skipped) / len(jobs):.3f} |")
print()
print("| file | editor | boost intervals with a demotion | demotions |")
print("|---|---|---|---|")
for f, task in (("c7-office", "writer"), ("c7-browsing", "browser"), ("c1-mail", "mailer"), ("c7-dev", "editor")):
    trace = f"{out}/{f}.10000.jsonl"
    n = sum(1 for line in open(trace)
            if (d := json.loads(line)).get("event") == "x_mlfq_demote" and d["task"] == task)
    print(f"| {f} | {task} | {shares(trace, (task,))[task]:.2f} | {n} |")
