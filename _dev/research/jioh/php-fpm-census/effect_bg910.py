#!/usr/bin/env python3
"""census_bg910.py's outputs read against the pooled records: the check (each carried value reconstructed from the
census's own reading against the pooled record's mean), the outside-cause wakes by cause group (`by_cause.py`'s
groups) and every class's total, and how far each carried value would move.

The move is read two ways. The bound, as `effect_extra.py` reads it: removing an outside-cause wake removes at most
its run from a sum — the CPU total, a member step, the runs' sum — and at most one run from a count-based mean, so a
mean's shift is bounded by the larger of the outside-cause wakes' run over the run it sums and their count over the
runs it averages (a member step's count is its jobs', which no wake removes: its run share alone). And recomputed:
census_bg910.py's values with the outside-cause wakes' segments taken out of the rows. Both under the rule as written
(every outside-cause wake) and with only the wakes whose own row names the outside waker (the inherited put back);
against each value's 95 % half-width (the pooled record's) and the ±5 % tolerance. For a block mean the bound counts
runs only, while a removed run leaves its time to the program's gap when no other thread of it runs on: the
recomputation is the reading that holds there. A CPU total is also the timelines' `total_work` for the campaigns whose
files bind it.

  python3 -I effect_bg910.py <out dir holding census_bg910 outputs> <campaign dir holding <job>/results/pooled.json>
      > effect-bg910.json        (--md: the tables in the record's form)
"""

import collections
import json
import os
import sys

GROUPS = (("php-fpm", ("php8.3-fpm",)), ("PHP session cleanup", ("phpsessionclean", "PHP's session cleanup")),
          ("podman", ("podman",)), ("sphinxsearch", ("sphinxsearch",)),
          ("runner agent / provisioner", ("runner agent", "runner provisioner")), ("tracer (perf)", ("(tracer)",)),
          ("workflow step / run.sh", ("workflow step", "(run.sh)", "input driver")),
          ("Azure VM daemons", ("hyperv-daemons",)),
          ("other runner-only services", ("containerd", "docker.io", "multipath-tools", "chrony", "runc", "haveged",
                                          "walinuxagent", "irqbalance", "systemd-networkd", "clamav", "mono", "at (")))
LABEL = {"run": "run between voluntary blocks (µs)", "block": "block per run (µs)", "cpu": "CPU total (µs)"}
POOLDIR = {"upgrade": "upgrade", "dkms": "dkms", "tracker": "tracker", "mnist": "mnist", "handbrake": "handbrake",
           "kdenlive": "kdenlive", "dejadup": "dejadup"}


def group(label):
    for g, keys in GROUPS:
        if any(k in label for k in keys):
            return g
    return "other: " + label


def rel(a, b):
    return (a - b) / b if b else None


def dkms_rows(sec, e, R, q, ph, tot):
    """The DKMS build's tables: a member step against the outside-cause run of its kind's member role, make's
    dispatch run against make's, the tail's runs and blocks against the tail's, the carried CPU total against every
    carried category's."""
    from meas.background import modbuild
    out = []
    V = {tag: [r["values"][tag] for r in R.values()] for tag in ("base", "rule", "direct")}

    def val(tag, key, per_repeat=False):
        if per_repeat:
            return sum(x[key][0] for x in V[tag]) / len(V[tag])
        n = sum(x[key][1] for x in V[tag] if key in x)
        return sum(x[key][0] for x in V[tag] if key in x) / n if n else None
    carried_cats = {cat for r in R.values() for cat in r["tally"] if cat.startswith("job ") or cat in ("make", "tail")}
    items = []
    for kind, tree in modbuild.TREES.items():
        for mid, role, n in modbuild.members(tree):
            for i in range(1, n + 1):
                items.append((f"{kind} {mid} step {i}/{n} (µs)", f"step:{kind} {mid} {i}/{n}", {f"job {kind} {role}"}, None))
    items += [("make dispatch (µs)", "dispatch", {"make"}, "dispatch"), ("tail run between voluntary blocks (µs)",
              "tail_run", {"tail"}, "tail_run"), ("tail block per run (µs)", "tail_block", {"tail"}, "tail_block"),
              ("CPU total carried (µs)", "carried_cpu_us", carried_cats, None)]
    for label, key, cats, count_key in items:
        Q = q.get(f"{ph} {label}", {})
        per = key == "carried_cpu_us"
        base = val("base", key, per)
        if base is None:
            continue
        s_sum = sum(x[key][0] for x in V["base"] if key in x)
        n_sum = sum(x[key][1] for x in V["base"] if key in x)
        line = {"section": sec, "campaign": e["campaign"], "value": label, "k": len(R), "pooled_mean": Q.get("mean"),
                "reconstructed": base, "check": rel(base, Q["mean"]) if Q.get("mean") else None,
                "half_width": Q.get("half_width"),
                "carried_as": "passes" if Q.get("passes") else ("excepted (half-width carried)" if Q.get("excepted")
                                                                else Q.get("carried")),
                "wakes": sum(t["n"] for r in R.values() for c, t in r["tally"].items() if c in cats)}
        for tag in ("rule", "direct"):
            on, orun = tot(cats, tag, "n"), tot(cats, tag, "run") * 1000.0
            run_share = orun / s_sum if s_sum else 0.0
            count_share = on / n_sum if count_key and n_sum else 0.0
            line[f"outside_{tag}"] = int(on)
            line[f"run_share_{tag}"] = run_share
            line[f"count_share_{tag}"] = count_share
            line[f"bound_{tag}"] = (count_share if key == "tail_block" else max(run_share, count_share))
            new = val(tag, key, per)
            line[f"recomputed_{tag}"] = rel(new, base) if new is not None else None
        out.append(line)
    return out


def main():
    out_dir, camp = sys.argv[1], sys.argv[2]
    rows, causes, classes, roots, checks = [], [], {}, [], []
    for f in sorted(os.listdir(out_dir)):
        if not f.endswith(".json") or f.startswith("effect"):
            continue
        for sec, e in json.load(open(os.path.join(out_dir, f))).items():
            job, R = e["job"], e["repeats"]
            pooled = json.load(open(os.path.join(camp, POOLDIR[job], "results", "pooled.json")))
            q = list(pooled["runs"].values())[0]["stability"]["quantities"]
            ph = e["phase"]
            # by cause, the classes, the roots
            c, cl, n = collections.Counter(), collections.Counter(), 0
            for k, r in R.items():
                for cat, t in r["tally"].items():
                    n += t["n"]
                    for x, v in t["classes"].items():
                        cl[x] += v["n"]
                    for lab, x in t["labels"].items():
                        if lab.startswith("outside: "):
                            c[group(lab[len("outside: "):])] += x
                for g in r["roots"]["largest"]:
                    roots.append({"section": sec, "repeat": k, **g})
            causes.append({"section": sec, "campaign": e["campaign"], "k": len(R), "wakes": n, "outside": sum(c.values()),
                           **{g: c.get(g, 0) for g, _ in GROUPS},
                           "other": {g: x for g, x in c.items() if g.startswith("other: ")}})
            classes[sec] = dict(cl)
            checks.append({"section": sec, "check_differ": sum(r["check_differ"] for r in R.values()),
                           "check_wakes": sum(r["check_wakes"] for r in R.values())})

            def tot(cats, what, key):
                """Σ over the repeats and the given categories of the outside wakes' count or run (ms)."""
                s = 0.0
                for r in R.values():
                    for cat, t in r["tally"].items():
                        if cats is None or cat in cats:
                            if what == "rule":
                                s += t["classes"].get("outside", {}).get(key, 0)
                            else:
                                s += t["split"]["direct"][key]
                return s

            if job != "dkms":
                B = {tag: [r["values"][tag] for r in R.values()] for tag in ("base", "rule", "direct")}
                cpu = sum(x["cpu_us"] for x in B["base"])
                runs = sum(x["run_n"] for x in B["base"])
                blocks = sum(x["block_n"] for x in B["base"])
                for v, (s_key, n_key) in (("run", ("run_sum", "run_n")), ("block", ("block_sum", "block_n")),
                                         ("cpu", ("cpu_us", None))):
                    label = f"{ph} {LABEL[v]}"
                    Q = q.get(label, {})

                    def val(tag):
                        if n_key is None:
                            return sum(x[s_key] for x in B[tag]) / len(B[tag])
                        return sum(x[s_key] for x in B[tag]) / sum(x[n_key] for x in B[tag])
                    base = val("base")
                    line = {"section": sec, "campaign": e["campaign"], "value": LABEL[v], "k": len(R),
                            "pooled_mean": Q.get("mean"), "reconstructed": base,
                            "check": rel(base, Q["mean"]) if Q.get("mean") else None,
                            "half_width": Q.get("half_width"), "carried_as": "passes" if Q.get("passes") else
                            ("excepted (half-width carried)" if Q.get("excepted") else Q.get("carried")),
                            "wakes": sum(t["n"] for r in R.values() for t in r["tally"].values())}
                    for tag in ("rule", "direct"):
                        on, orun = tot(None, tag, "n"), tot(None, tag, "run") * 1000.0
                        run_share = orun / cpu if cpu else 0.0
                        count_share = on / (runs if v == "run" else blocks) if v != "cpu" else 0.0
                        line[f"outside_{tag}"] = int(on)
                        line[f"run_share_{tag}"] = run_share
                        line[f"count_share_{tag}"] = count_share
                        line[f"bound_{tag}"] = run_share if v == "cpu" else (max(run_share, count_share) if v == "run"
                                                                             else count_share)
                        line[f"recomputed_{tag}"] = rel(val(tag), base)
                    rows.append(line)
                continue

            rows.extend(dkms_rows(sec, e, R, q, ph, tot))
    out = {"checks": checks, "causes": causes, "classes": classes, "values": rows,
           "roots": sorted(roots, key=lambda g: -g["wakes"])[:30]}
    if "--md" in sys.argv:
        render(out)
    else:
        json.dump(out, sys.stdout, indent=1)


def render(out):
    pc = lambda x: "—" if x is None else f"{100 * x:+.3f} %"
    sh = lambda x: f"{100 * x:.3f} %"
    print("| section | campaign | k | wakes | outside | " + " | ".join(g for g, _ in GROUPS) + " |")
    print("|---|---|---|---|---|" + "---|" * len(GROUPS))
    for c in out["causes"]:
        print(f"| {c['section']} | {c['campaign']} | {c['k']} | {c['wakes']} | {c['outside']} | "
              + " | ".join(str(c[g]) for g, _ in GROUPS) + " |" + (f" {c['other']}" if c["other"] else ""))
    print()
    for sec, cl in out["classes"].items():
        n = sum(cl.values())
        print(f"- {sec}: {n} wakes — " + ", ".join(f"{k} {v} ({100 * v / n:.2f} %)" for k, v in
                                                  sorted(cl.items(), key=lambda kv: -kv[1])))
    print()
    print("| entry | value | k | wakes | outside (direct) | outside run share | half-width | bound on the shift (rule as "
          "written) | bound with inherited put back | recomputed (rule as written) | recomputed (inherited put back) |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for v in out["values"]:
        if v["value"].startswith(tuple(f"{k} " for k in ("object", "kprobe", "conftest-a", "conftest-b"))) \
                and not v["outside_rule"]:
            continue    # the DKMS member steps without an outside-cause wake: one summary line below
        mark = lambda x: " **beyond**" if x is not None and v["half_width"] is not None and (
            abs(x) > v["half_width"] or abs(x) > 0.05) else ""
        print(f"| {v['section']} | {v['value']} | {v['k']} | {v['wakes']} | {v['outside_rule']} ({v['outside_direct']}) | "
              f"{sh(v['run_share_rule'])} | ±{100 * v['half_width']:.2f} % | {sh(v['bound_rule'])}{mark(v['bound_rule'])} | "
              f"{sh(v['bound_direct'])}{mark(v['bound_direct'])} | {pc(v['recomputed_rule'])}{mark(v['recomputed_rule'])} | "
              f"{pc(v['recomputed_direct'])}{mark(v['recomputed_direct'])} |")
    steps = [v for v in out["values"] if " step " in v["value"]]
    if steps:
        print(f"\n{len(steps)} DKMS member-step tables, outside-cause wakes {sum(v['outside_rule'] for v in steps)}; "
              f"half-widths ±{100 * min(v['half_width'] for v in steps):.2f}–{100 * max(v['half_width'] for v in steps):.2f} %")
    print()
    print("| section | repeat | root waker | wakes | inherited | span s | threads | max hops | comms |")
    print("|---|---|---|---|---|---|---|---|---|")
    for g in out["roots"][:15]:
        print(f"| {g['section']} | {g['repeat']} | {g['waker']} | {g['wakes']} | {g['inherited']} | {g['span_s']} | "
              f"{g['threads']} | {g['max_hops']} | {g['comms']} |")


if __name__ == "__main__":
    sys.path.insert(0, "/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/dataset/tools")
    main()
