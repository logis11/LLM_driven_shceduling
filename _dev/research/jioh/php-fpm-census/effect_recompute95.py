#!/usr/bin/env python3
"""census_recompute95.py's outputs read against the pooled records: for each per-input run and each playback cycle
value, the value reconstructed from the census's own reading against the pooled record's mean (the check), and the
value recomputed under each reading — its shift against the pooled half-width and the ±5 % tolerance, with the
recomputed half-width (`ratio_stability`, as campaign/pool.py's `add_table` reads a table: Σ / Σ n over the repeats);
and `page-load`'s components, in the census's order and traced in time order (effect_split.py's shifts).

  python3 -I effect_recompute95.py <input.json> <cycle.json> > effect-recompute95.json   (--md: the tables)
"""

import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/dataset/tools")
from meas.stability import ratio_stability  # noqa: E402
import effect_split as es  # noqa: E402

P95 = "/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/_dev/research/jioh/task-9.5-interactive-typing/campaign"
POOL = {"video-player": ("results-same-machine/pool-mpv-video.json", "mpv-video"),
        "audio-player": ("results-same-machine/pool-mpv-audio.json", "mpv-audio"),
        "video-call": ("results-re-measured/pool-webrtc.json", "webrtc"),
        "office-writer": ("results-same-machine/pool-soffice.json", "soffice"),
        "code-editor": ("results-re-measured/pool-code.json", "code"),
        "web-browser": ("results-re-measured/pool-chrome.json", "chrome"),
        "mail-client": ("results-re-measured/pool-thunderbird-send.json", "thunderbird-send")}
FLOOR_MS = 0.001   # campaign/pool.py ABS_FLOOR_MS
MIN_K = 5          # campaign/pool.py MIN_REPEATS


def quantities(entry):
    path, app = POOL[entry]
    return json.load(open(os.path.join(P95, path)))["runs"][app]["stability"]["quantities"]


def table(R, tags, s_key, n_key, label, q):
    Q = q[label]
    line = {"value": label, "pooled_mean": Q["mean"], "pooled_half_width": Q["half_width"], "k": len(R)}
    for tag in tags:
        sums = {k: r["values"][tag][s_key] for k, r in R.items()}
        cnts = {k: r["values"][tag][n_key] for k, r in R.items()}
        st = ratio_stability(sums, cnts, FLOOR_MS, MIN_K)
        line[tag] = {"mean": sum(sums.values()) / sum(cnts.values()), "half_width": st["half_width"],
                     "passes": st["passes"]}
    base = line["base"]["mean"]
    line["check"] = (base - Q["mean"]) / Q["mean"]
    for tag in tags:
        if tag != "base":
            line[tag]["shift"] = (line[tag]["mean"] - base) / base
    return line


def main():
    inp, cyc = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
    out = {"input_run": [], "cycle": [], "page_load": None}
    for entry, e in inp.items():
        R = {k: r for k, r in e["repeats"].items() if r.get("values")}
        q = quantities(entry)
        tags = ("base", "rule", "rule_idle_only", "rule_driven_only", "direct")
        line = table(R, tags, "corr_sum", "n", "input_run mean, SWELL-KW (ms)", q)
        line.update(entry=entry, repeats_without_driven=[k for k, r in e["repeats"].items() if not r.get("values")],
                    idle_removed={t: [sum(r["idle"]["removed"][t]["n"] for r in R.values()),
                                      sum(r["idle"]["removed"][t]["run_ms"] for r in R.values())] for t in ("rule", "direct")},
                    driven_removed={t: [sum(r["driven"]["removed"][t]["n"] for r in R.values()),
                                        sum(r["driven"]["removed"][t]["run_ms"] for r in R.values())] for t in ("rule", "direct")},
                    idle_rate_shift={t: sum(r["idle"]["rate"][t] for r in R.values()) / sum(r["idle"]["rate"]["base"] for r in R.values()) - 1
                                     for t in ("rule", "direct")},
                    clamped={t: sum(r["values"][t]["clamped"] for r in R.values()) for t in tags},
                    idle_wakes=sum(r["idle"]["wakes"] for r in R.values()))
        out["input_run"].append(line)
        if entry == "web-browser":
            out["page_load"] = page_load(e)
    for entry, e in cyc.items():
        R = e["repeats"]
        q = quantities(entry)
        for s_key, label in (("length_sum", "play cycle length mean (ms)"), ("work_sum", "play cycle work mean (ms)")):
            line = table(R, ("base", "rule", "direct"), s_key, "n", label, q)
            line.update(entry=entry,
                        cycles={t: sum(r["values"][t]["n"] for r in R.values()) for t in ("base", "rule", "direct")},
                        ref_removed={t: sum(r["values"][t]["ref_removed"] for r in R.values()) for t in ("rule", "direct")},
                        ref_removed_starts={t: sum(r["values"][t]["ref_removed_starts"] for r in R.values())
                                            for t in ("rule", "direct")},
                        removed={t: sum(r["values"][t]["removed"]["n"] for r in R.values()) for t in ("rule", "direct")},
                        repeats_with_removed_starts={t: sum(1 for r in R.values() if r["values"][t]["ref_removed_starts"])
                                                     for t in ("rule", "direct")},
                        ref_labels={t: dict(sum((collections.Counter(r["values"][t]["ref_removed_labels"]) for r in R.values()),
                                                collections.Counter()).most_common()) for t in ("rule", "direct")})
            out["cycle"].append(line)
    if "--md" in sys.argv:
        render(out)
    else:
        json.dump(out, sys.stdout, indent=1)


def page_load(e):
    """The operation's components in effect_split.py's form, in the census's order and in time order."""
    res = {"deep": {}, "deep_become": collections.Counter(), "components": []}
    for order in ("census", "time"):
        reps = {k: r["page_load"][order]["tally"] for k, r in e["repeats"].items() if r.get("page_load")}
        res["deep"][order] = sum(r["page_load"][order]["deep"] for r in e["repeats"].values() if r.get("page_load"))
        dreps = es.direct_only(reps)
        for comp in sorted({c for t in reps.values() for c in t}):
            cs = [t[comp] for t in reps.values() if comp in t]
            line = {"order": order, "component": comp, "k": len(cs), "wakes": sum(c["n"] for c in cs),
                    "outside": sum(c["classes"].get("outside", {}).get("n", 0) for c in cs),
                    "direct": sum(c["split"]["direct"]["n"] for c in cs),
                    "unknown": sum(c["classes"].get("unknown", {}).get("n", 0) for c in cs),
                    "classes": dict(sum((collections.Counter({x: v["n"] for x, v in c["classes"].items()}) for c in cs),
                                        collections.Counter()))}
            for tag, rr in (("out", reps), ("direct", dreps)):
                for k, v in es.shifts(rr, comp, ("outside",)).items():
                    line[f"{k}_{tag}" if k.endswith("_shift") else k] = v
            res["components"].append(line)
    for r in e["repeats"].values():
        if r.get("page_load"):
            res["deep_become"].update(r["page_load"].get("deep_become", {}))
    res["deep_become"] = dict(res["deep_become"].most_common())
    return res


def render(out):
    pc = lambda x: "—" if x is None else f"{100 * x:+.3f} %"
    print("| entry | value | k | pooled | reconstructed (check) | half-width | rule as written | idle only | driven only "
          "| direct only | idle/driven removed (rule) |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for L in out["input_run"]:
        print(f"| {L['entry']} | input_run | {L['k']} | {L['pooled_mean']} | {L['base']['mean']:.4f} ({pc(L['check'])}) | "
              f"±{100 * L['pooled_half_width']:.2f} % | {pc(L['rule']['shift'])} | {pc(L['rule_idle_only']['shift'])} | "
              f"{pc(L['rule_driven_only']['shift'])} | {pc(L['direct']['shift'])} | {L['idle_removed']['rule'][0]} "
              f"({L['idle_removed']['rule'][1]:.1f} ms) / {L['driven_removed']['rule'][0]} ({L['driven_removed']['rule'][1]:.1f} ms) |")
    print()
    print("| entry | value | k | pooled | reconstructed (check) | half-width | rule as written | direct only | cycles base → "
          "rule → direct | reference wakes removed (cycle starts), rule · direct |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for L in out["cycle"]:
        print(f"| {L['entry']} | {L['value']} | {L['k']} | {L['pooled_mean']} | {L['base']['mean']:.5f} ({pc(L['check'])}) | "
              f"±{100 * L['pooled_half_width']:.2f} % (recomputed {L['base']['half_width']}) | {pc(L['rule']['shift'])} "
              f"(hw {L['rule']['half_width']}) | {pc(L['direct']['shift'])} | {L['cycles']['base']} → {L['cycles']['rule']} → "
              f"{L['cycles']['direct']} | {L['ref_removed']['rule']} ({L['ref_removed_starts']['rule']}) · "
              f"{L['ref_removed']['direct']} ({L['ref_removed_starts']['direct']}) |")
    for L in out["cycle"][::2]:
        print(f"{L['entry']} reference labels: rule {L['ref_labels']['rule']}; direct {L['ref_labels']['direct']}; "
              f"repeats with removed starts {L['repeats_with_removed_starts']}")
    for L in out["input_run"]:
        print(f"{L['entry']}: idle rate shift {L['idle_rate_shift']}, clamped {L['clamped']}, no driven {L['repeats_without_driven']}")
    p = out["page_load"]
    if p:
        print()
        print("page-load deep:", p["deep"], "become:", p["deep_become"])
        print("| order | component | k | wakes | outside (direct) | unknown | rate shift / hw | gap | run | direct only rate |")
        print("|---|---|---|---|---|---|---|---|---|---|")
        for c in p["components"]:
            print(f"| {c['order']} | {c['component']} | {c['k']} | {c['wakes']} | {c['outside']} ({c['direct']}) | {c['unknown']} | "
                  f"{pc(c.get('rate_shift_out'))} / ±{100 * (c.get('rate_hw') or 0):.2f} % | {pc(c.get('gap_shift_out'))} / "
                  f"±{100 * (c.get('gap_hw') or 0):.2f} % | {pc(c.get('run_shift_out'))} / ±{100 * (c.get('run_hw') or 0):.2f} % | "
                  f"{pc(c.get('rate_shift_direct'))} |")


if __name__ == "__main__":
    main()
