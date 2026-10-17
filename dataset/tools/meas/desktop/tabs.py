"""The tab-set subject's process listings (9.10 changelog D126–D129; method
_dev/research/jioh/task-9.10-scenarios-timelines/campaign/chrome-tabs/method.md).

    tabs.py list --arm <off|on> --phase <name> --t0 <ns> [--pattern chrome-data]
        one listing of Chrome's tree, a TSV row per process, appended by run.sh to tabs.tsv every 10 s
    tabs.py summary <run-dir>
        the counts per launch and phase, as report keys (key=value lines run.sh appends to report.kv)

A renderer is a page renderer, Chrome's WebUI renderer or an extension renderer by its command line, as 9.8's
analysis reads it (`analyze.NOT_PAGE_RENDERER`). With the spare on, the spare is a renderer whose command line is a
page renderer's (D128), so the role a row carries is `plain`: in the spare-off launch every plain renderer hosts a
page; in the spare-on launch the plain renderers beyond that count are the spare.
"""

import argparse
import collections
import os
import sys
import time

COLUMNS = ("arm", "phase", "t_s", "pid", "ppid", "type", "role", "client_id", "start_ticks", "threads", "cpu_ticks")
OWN = (("--top-chrome-webui", "webui"), ("--extension-process", "extension"))


def role_of(argv):
    """(type, role) of one Chrome process from its argv: type is --type= or `browser`; role names a renderer's kind."""
    typ = next((a.split("=", 1)[1] for a in argv if a.startswith("--type=")), None)
    if typ is None:
        name = os.path.basename(argv[0]) if argv else ""
        return ("crashpad" if "crashpad" in name else "browser"), ""
    if typ != "renderer":
        return typ, ""
    return typ, next((r for flag, r in OWN if flag in argv), "plain")


def listing(pattern, proc="/proc"):
    """Every process whose command line holds `pattern`: (pid, ppid, argv, start_ticks, threads, cpu_ticks)."""
    out, me = [], str(os.getpid())   # this listing's own command line holds the pattern too
    for d in os.listdir(proc):
        if not d.isdigit() or d == me:
            continue
        try:
            raw = open(os.path.join(proc, d, "cmdline"), "rb").read()
            stat = open(os.path.join(proc, d, "stat")).read()
        except OSError:
            continue
        # Chrome rewrites a child's process title: its cmdline is then one string, the arguments joined by spaces
        # (dry run #72), so the arguments are split on both
        argv = raw.replace(b"\0", b" ").decode(errors="replace").split()
        if not any(pattern in a for a in argv):
            continue
        f = stat[stat.rindex(")") + 2:].split()   # fields from state on: field 3 is f[0]
        out.append((int(d), int(f[1]), argv, int(f[19]), int(f[17]), int(f[11]) + int(f[12])))
    return sorted(out)


def rows(arm, phase, t0_ns, procs, now_ns):
    t = f"{(now_ns - t0_ns) / 1e9:.1f}"
    for pid, ppid, argv, start, threads, cpu in procs:
        typ, role = role_of(argv)
        cid = next((a.split("=", 1)[1] for a in argv if a.startswith("--renderer-client-id=")), "")
        yield (arm, phase, t, pid, ppid, typ, role, cid, start, threads, cpu)


def read_tsv(path):
    out = []
    for line in open(path):
        parts = line.rstrip("\n").split("\t")
        if len(parts) != len(COLUMNS) or parts[0] == "arm":
            continue
        out.append(dict(zip(COLUMNS, parts)))
    return out


def summary(rs):
    """Report keys from tabs.tsv rows: per launch, each phase's renderer counts by role (min and max over its
    listings), whether the steady phase's plain renderers are one pid set from its first listing to its last, the
    first listing time at which the plain count reached the steady phase's, and, when both launches held one count
    through the steady phase, the spare (on − off) and the hidden tabs' renderers (off − the page in use)."""
    keys = {}
    by = collections.defaultdict(lambda: collections.defaultdict(list))   # arm -> phase -> [(t, Counter, plain pids)]
    for t in sorted({(r["arm"], r["phase"], float(r["t_s"])) for r in rs}, key=lambda x: x[2]):
        here = [r for r in rs if (r["arm"], r["phase"], float(r["t_s"])) == t]
        c = collections.Counter(r["role"] for r in here if r["type"] == "renderer")
        by[t[0]][t[1]].append((t[2], c, frozenset(r["pid"] for r in here if r["role"] == "plain")))
    steady = {}
    for arm, phases in sorted(by.items()):
        for ph, ls in phases.items():
            keys[f"tabs.{arm}.{ph}.listings"] = len(ls)
            for role in ("plain", "webui", "extension"):
                ns = [c[role] for _, c, _ in ls]
                keys[f"tabs.{arm}.{ph}.{role}_min"] = min(ns)
                keys[f"tabs.{arm}.{ph}.{role}_max"] = max(ns)
        st = phases.get("steady")
        if not st:
            continue
        keys[f"tabs.{arm}.steady.plain_pids_stable"] = int(len({p for _, _, p in st}) == 1)
        lo, hi = keys[f"tabs.{arm}.steady.plain_min"], keys[f"tabs.{arm}.steady.plain_max"]
        if lo == hi:
            steady[arm] = lo
            first = min(t for ls in phases.values() for t, c, _ in ls if c["plain"] == lo)
            keys[f"tabs.{arm}.plain_reached_s"] = first
    if "off" in steady:
        keys["tabs.hidden"] = steady["off"] - 1       # D127: beyond the page in use
    if "off" in steady and "on" in steady:
        keys["tabs.spare"] = steady["on"] - steady["off"]
    return keys


REPORT_KEYS = ("version", "kernel", "tabs.tabs", "tabs.order",
               "tabs.off.page_loads", "tabs.on.page_loads", "tabs.off.exit_s", "tabs.on.exit_s",
               "tabs.off.steady.plain_min", "tabs.off.steady.plain_max", "tabs.on.steady.plain_min",
               "tabs.on.steady.plain_max", "tabs.off.steady.plain_pids_stable", "tabs.on.steady.plain_pids_stable",
               "tabs.off.plain_reached_s", "tabs.on.plain_reached_s",
               "tabs.off.steady.webui_max", "tabs.on.steady.webui_max",
               "tabs.off.steady.extension_max", "tabs.on.steady.extension_max",
               "tabs.off.launch-settle.extension_max", "tabs.on.launch-settle.extension_max",
               "tabs.off.grace.extension_max", "tabs.on.grace.extension_max",
               "tabs.hidden", "tabs.spare")


def pool(reps):
    """The repeats' counts side by side (D129): a count is carried as observed, not by the stability rule, and the
    record says whether every repeat held one count — the hidden tabs' renderers (D127) and the spare (D128)."""
    per = {str(k): {key: info["report"].get(key) for key in REPORT_KEYS}
           | {"run_id": str((info["spec"].get("github_run") or {}).get("GITHUB_RUN_ID") or "")}
           for k, info in reps.items()}
    hidden = sorted({v["tabs.hidden"] for v in per.values()}, key=str)
    spare = sorted({v["tabs.spare"] for v in per.values()}, key=str)
    one = len(hidden) == 1 and hidden[0] is not None and len(spare) == 1 and spare[0] is not None
    return {"repeats": sorted(per, key=lambda x: (int(str(x).split("@")[0]), str(x))),
            "mode": sorted({info["mode"] for info in reps.values()}),
            "version": {k: v["version"] for k, v in per.items()},
            "per_repeat": per, "hidden": hidden, "spare": spare,
            "stability": {"quantity": "renderer-hidden tasks (page renderers beyond the page in use, spare off, "
                                      "steady phase) and the spare (on − off)",
                          "k": len(per), "half_width": 0 if one else None,
                          "tolerance": "one count in every repeat", "passes": one and len(per) >= 5,
                          "values": {"hidden": hidden, "spare": spare}}}


def render(app, e):
    L = [f"## {app}", "", f"Repeats: {e['repeats']}  ·  mode {e['mode']}", "",
         f"`renderer-hidden` tasks (D127): {e['hidden']}  ·  the spare (D128): {e['spare']}  ·  "
         f"{'one count in every repeat' if e['stability']['half_width'] == 0 else 'the repeats disagree'}", "",
         "| repeat | build | order | page loads off/on | plain off (steady) | plain on (steady) | pids stable off/on "
         "| WebUI off/on | extension launch off/on | extension steady off/on | hidden | spare |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in e["repeats"]:
        v = e["per_repeat"][k]
        g = lambda key: v.get(key) if v.get(key) is not None else "—"   # noqa: E731
        L.append(f"| {k} | {g('version')} | {g('tabs.order')} | {g('tabs.off.page_loads')}/{g('tabs.on.page_loads')} "
                 f"| {g('tabs.off.steady.plain_min')}–{g('tabs.off.steady.plain_max')} "
                 f"| {g('tabs.on.steady.plain_min')}–{g('tabs.on.steady.plain_max')} "
                 f"| {g('tabs.off.steady.plain_pids_stable')}/{g('tabs.on.steady.plain_pids_stable')} "
                 f"| {g('tabs.off.steady.webui_max')}/{g('tabs.on.steady.webui_max')} "
                 f"| {g('tabs.off.launch-settle.extension_max')}/{g('tabs.on.launch-settle.extension_max')} "
                 f"| {g('tabs.off.steady.extension_max')}/{g('tabs.on.steady.extension_max')} "
                 f"| {g('tabs.hidden')} | {g('tabs.spare')} |")
    return L + [""]


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    li = sub.add_parser("list")
    li.add_argument("--arm", required=True)
    li.add_argument("--phase", required=True)
    li.add_argument("--t0", type=int, required=True)
    li.add_argument("--pattern", default="chrome-data")
    su = sub.add_parser("summary")
    su.add_argument("run_dir")
    a = ap.parse_args()
    if a.cmd == "list":
        now = time.time_ns()
        for row in rows(a.arm, a.phase, a.t0, listing(a.pattern), now):
            print("\t".join(str(x) for x in row))
    else:
        for k, v in summary(read_tsv(os.path.join(a.run_dir, "tabs.tsv"))).items():
            print(f"{k}={v}")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
