import json, sys, statistics as st, glob, os, collections
ROOT = "/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/dataset/build"

def flat(prog):
    for s in prog:
        if s["op"] == "LOOP":
            yield from flat(s["body"])
        else:
            yield s

def summarize(path, detail=False):
    d = json.load(open(path))
    out = []
    out.append(f"== {os.path.basename(path)}  gt={[(g['t_start'],g['t_end'],g['mode'],g['attributes']) for g in d['ground_truth']]}")
    arr = [e for e in d["events"] if e["op"] == "arrive"]
    wakes = collections.Counter(e["target"] for e in d["events"] if e["op"] == "wake")
    # group by prefix for chains/tails/renderers
    groups = collections.OrderedDict()
    for e in arr:
        key = e["id"]
        if ".tail." in key: key = key.split(".tail.")[0] + ".tail.*"
        groups.setdefault(key, []).append(e)
    for key, es in groups.items():
        if key.endswith(".tail.*"):
            runs = [s["us"] for e in es for s in flat(e["program"]) if s["op"] == "RUN"]
            sl = [s["us"] for e in es for s in flat(e["program"]) if s["op"] == "SLEEP"]
            out.append(f"  {key} x{len(es)} name={es[0]['name']} RUN min/med/max={min(runs)}/{int(st.median(runs))}/{max(runs)} SLEEP min/med/max={min(sl)}/{int(st.median(sl))}/{max(sl)}")
            continue
        for e in es:
            ops = list(flat(e["program"]))
            c = collections.Counter(s["op"] for s in ops)
            runs = [s["us"] for s in ops if s["op"] == "RUN"]
            sl = [s["us"] for s in ops if s["op"] == "SLEEP"]
            tm = [s["period_us"] for s in ops if s["op"] == "TIMER"]
            waits = sorted(set(s["channel"] for s in ops if s["op"] == "WAIT"))
            wk = [s["target"] for s in ops if s["op"] == "WAKE"]
            loop = e["program"][0]["op"] == "LOOP" if e["program"] else False
            line = f"  {e['id']} name={e['name']} t={e['t']} depart={e.get('depart')} loop={loop} ops={dict(c)}"
            if runs: line += f" RUN n={len(runs)} sum={sum(runs)} min/med/mean/max={min(runs)}/{st.median(runs):.0f}/{st.mean(runs):.0f}/{max(runs)}"
            if sl: line += f" SLEEP n={len(sl)} min/med/max={min(sl)}/{st.median(sl):.0f}/{max(sl)}"
            if tm: line += f" TIMER={sorted(set(tm))}"
            if waits: line += f" WAIT={waits[:3]}"
            if wk: line += f" WAKE={wk}"
            if e["id"] in wakes: line += f" ext_wakes={wakes[e['id']]}"
            if "spawn_table" in e:
                ch = e["spawn_table"]
                cr = [s["us"] for x in ch for s in x["program"] if s["op"] == "RUN"]
                out.append(line)
                line = f"    spawn_table n={len(ch)} fork_cap={e['fork_cap']} child RUN sum={sum(cr)} med={st.median(cr):.0f} max={max(cr)} name={ch[0]['name']}"
            out.append(line)
    return "\n".join(out)

if __name__ == "__main__":
    for mode in ("coreset-single", "coreset-native"):
        for p in sorted(glob.glob(f"{ROOT}/{mode}/*.workload.json")):
            if len(sys.argv) > 1 and not any(a in p for a in sys.argv[1:]):
                continue
            print(mode, summarize(p))
