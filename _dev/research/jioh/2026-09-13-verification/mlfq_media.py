"""Minimal MLFQ replay of the periodic consumers + scan in c7-media / c7-meeting / c1-media.

Rules used (from the repo's own statements, not invented):
- OSTEP boot default: 3 queues, top slice 10 ms, growth 2, boost every 100 ms on the grid k*100000 (boot entry at t=0).
- Allotment = slice; a task that uses its full slice is demoted; blocking keeps its level (rule 4b).
- A wake into a higher queue than the running task preempts at once; into the same or lower queue waits
  for the running task's slice boundary (switch memo, restated in memo 2026-09-11 section 5).
- TIMER ticks at t0 + k*period with t0 = arrival = 0 (interpretation contract; metrics section 11 item 4).
- Queues are FIFO by the instant a task entered them. At a boost every task moves to Q0 with a fresh slice;
  the running task keeps the lane with a fresh top slice (variant A) or the same-instant TIMER wakes are
  processed first (variant B: wake before boost). Both variants are reported.
Miss rule: job latency (tick -> completion) > period.
"""
import json, sys, heapq

R = "/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/dataset/build/coreset-single/"
SL = [10000, 20000, 40000]
BOOST = 100000


def load(fid):
    d = json.load(open(R + fid + ".workload.json"))
    tasks = {}
    for e in d["events"]:
        if e["op"] != "arrive":
            continue
        p = e["program"]
        if p[0]["op"] == "LOOP":
            body = p[0]["body"]
            per = [s["period_us"] for s in body if s["op"] == "TIMER"][0]
            run = [s["us"] for s in body if s["op"] == "RUN"][0]
            tasks[e["id"]] = ("periodic", per, run)
        else:
            tasks[e["id"]] = ("batch", None, sum(s["us"] for s in p if s["op"] == "RUN"))
    return tasks, d["ground_truth"][-1]["t_end"]


def run(fid, variant):
    tasks, T = load(fid)
    level = {t: 0 for t in tasks}
    used = {t: 0 for t in tasks}           # CPU used in current slice at this level
    remaining = {}                          # remaining RUN of current job
    tick_of_job = {}
    queues = [[], [], []]                   # FIFO lists of (enter_t, seq, task)
    seq = 0
    misses = {t: 0 for t in tasks if tasks[t][0] == "periodic"}
    jobs = {t: 0 for t in misses}
    backlog = {t: [] for t in misses}
    for t, (k, per, run_us) in tasks.items():
        if k == "batch":
            remaining[t] = run_us
    now = 0
    running = None
    run_start = 0

    def enqueue(task, when):
        nonlocal seq
        queues[level[task]].append((when, seq, task)); seq += 1

    # initial arrivals at t=0: periodic tick 0 consumed at 0, batch runnable
    events = []  # (time, order, kind, task)
    for t, (k, per, run_us) in tasks.items():
        if k == "periodic":
            heapq.heappush(events, (0, 1 if variant == "B" else 2, "tick", t))
    for t, (k, per, run_us) in tasks.items():
        if k == "batch":
            enqueue(t, 0)
    b = BOOST
    while b < T:
        heapq.heappush(events, (b, 2 if variant == "B" else 1, "boost", None)); b += BOOST

    def pick():
        for q in queues:
            if q:
                q.sort()
                return q.pop(0)[2]
        return None

    def slice_left(task):
        return SL[level[task]] - used[task]

    while now < T:
        if running is None:
            running = pick()
            run_start = now
        # next internal event: completion or slice end of running
        nxt_evt = events[0][0] if events else T
        if running is not None:
            dt = min(remaining[running], slice_left(running))
            t_done = now + dt
        else:
            t_done = T + 1
        if nxt_evt <= t_done:
            # advance to event
            if running is not None:
                d = nxt_evt - now
                remaining[running] -= d; used[running] += d
            now = nxt_evt
            tm, _, kind, task = heapq.heappop(events)
            if kind == "tick":
                per, run_us = tasks[task][1], tasks[task][2]
                heapq.heappush(events, (tm + per, 1 if variant == "B" else 2, "tick", task))
                if task in remaining:      # still working on a previous job: backlog
                    backlog[task].append(tm)
                else:
                    remaining[task] = run_us; tick_of_job[task] = tm
                    if running is None:
                        enqueue(task, tm)
                    elif level[task] < level[running]:
                        enqueue(running, now); running = None
                        enqueue(task, tm)
                    else:
                        enqueue(task, tm)
            elif kind == "boost":
                for q in queues:
                    for (_, _, x) in q:
                        pass
                moved = [x for q in queues for (_, _, x) in q]
                queues = [[], [], []]
                for x in moved:
                    level[x] = 0; used[x] = 0
                for x in moved:
                    enqueue(x, now)
                if running is not None:
                    level[running] = 0; used[running] = 0
        else:
            now = t_done
            task = running
            remaining[task] -= dt; used[task] += dt
            if remaining[task] == 0:
                del remaining[task]
                running = None
                if tasks[task][0] == "periodic":
                    jobs[task] += 1
                    if now - tick_of_job[task] > tasks[task][1]:
                        misses[task] += 1
                    used[task] = 0  # blocking keeps level; the slice count restarts (rule 4b reading used by the repo)
                    if backlog[task]:
                        tick = backlog[task].pop(0)
                        remaining[task] = tasks[task][2]; tick_of_job[task] = tick
                        enqueue(task, now)
                else:
                    pass
            else:
                # slice expired
                if level[task] < 2:
                    level[task] += 1
                used[task] = 0
                enqueue(task, now); running = None
    return {t: (misses[t], jobs[t]) for t in misses}


for fid in sys.argv[1:]:
    for v in ("A", "B"):
        print(fid, "variant", v, run(fid, v))
