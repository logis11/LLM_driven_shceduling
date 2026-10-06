#!/usr/bin/env python3
"""Generate the four 9.8 archetype entries from the desktop campaign's pooled record (changelog D10, D25).

  fold_in.py <pooled.json> <out.yaml> [--control <record>] [--only <subject>[,<subject>...]]

One entry per subject, in 9.5's measured per-application form (D10): `components`, one per thread comm of the
carried phase, each with its `wakes_per_s` and its pooled `gap` and `run` quantile tables, and the residual; no
`focus_components`, no `stimulus`. The scope states what method §7 and the changelog require of each entry: the
machine, the program's version, the state and what it is not, the values carried under an exception with their
half-widths and ranges (D17, D18, D21, D23, D24), the spreads within and between runs (D20, D22, D24), the sparse
residuals with their counts (D27), a rare event within a run stated beside its component (D33), the renderer population (D14) and the share `HangWatcher` holds (D16). The output
is a YAML fragment for `dataset/archetypes.yaml`.
"""

import json
import os
import statistics
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)
from meas.distribution import quantile_table, yaml_table  # noqa: E402
from meas.desktop.pool import _cp  # noqa: E402  — campaign/pool.py, for its build census (9.5 D69)

TAG = "meas-ci:desktop:2026-09-20"
# the campaigns an entry may be folded from: 9.8's, and 9.10 D152's for the hidden renderer past its page thread's
# settling, whose entry 9.8's record no longer writes (9.10 D156). The pooled record's tag picks the campaign; its
# subjects alone are folded (--only narrows them further).
CAMPAIGNS = {"meas-ci:desktop:2026-09-20": ("element", "steam"),
             "meas-ci:desktop:2026-10-05b": ("chrome-hidden",)}
CARRIED = {"chrome-hidden": "steady", "chrome-visible": "steady-notimer", "element": "idle", "steam": "shown"}
CONTROL = {}   # archetype id -> the untraced control's reading for its notes
# the entries the library carries: chrome-visible's values stay in the pooled record, its entry `renderer-visible`
# left the library when no timeline bound it (9.10 D16)
FOLDED = ("chrome-hidden", "element", "steam")
IDS = {"chrome-hidden": "renderer-hidden", "chrome-visible": "renderer-visible", "element": "chat-client",
       "steam": "game-client"}
LABEL = {"wakes/s": "wake rate", "gap mean (ms)": "gap mean", "run mean (ms)": "run mean"}

MACHINE = ("a GitHub-hosted ubuntu-24.04 runner (4 vCPU AMD EPYC 7763, kernel 6.17.0-1022-azure), the subject pinned "
           "to one CPU and the harness, page server and homeserver pinned away from it, perf sched record on that CPU")

OBSERVED = {
    "chrome-hidden": ("{build}, launched as web-browser was (--no-sandbox --disable-gpu, plus "
                      "--disable-features=SpareRendererForSitePerProcess), one window holding a foreground control tab "
                      "and 12 background tabs at 12 loopback origins of one local page whose setInterval callback only "
                      "increments a counter; observed past Chromium's intensive-wake-up-throttling grace (launch-settle "
                      "{grace}), a 600 s steady phase, under Xvfb with no window manager"),
    "chrome-visible": ("{build}, launched as the hidden entry, the same page at the same 12 origins "
                       "opened as 12 windows of one tab each, nothing interacting with them; the steady phase with the "
                       "page's timer removed (D16), 600 s, under Xvfb with no window manager, where Chromium tracks no "
                       "cross-application occlusion (D4)"),
    "element": ("Element Desktop 1.12.28 (unauthenticated apt repository; --no-sandbox --disable-gpu "
                "--disable-gpu-sandbox --disable-software-rasterizer --disable-dev-shm-usage --password-store=basic), "
                "signed in to one room on a Synapse 1.161.0 homeserver installed on the runner, idle with no message "
                "sent (D11); launch-settle 20 s, a 600 s idle phase, under Xvfb"),
    "steam": ("the Steam desktop client, build 1788652215 (steam-installer), logged out — no account is used, and "
              "none may be (D6) — its window shown; launch-settle 900 s (D15), a 600 s shown phase, under Xvfb with "
              "openbox so the window can be minimised"),
}

STATE_NOT = {
    "chrome-hidden": ("Values are floors: a page that does nothing but stay alive, on a runner without a GPU or display "
                      "vsync (method §7); a renderer showing live content does more. Not covered: a tab just switched "
                      "away from, before the grace (D3)."),
    "chrome-visible": ("Values are floors, as the hidden entry's (method §7), and unlike its wake rate they depend on "
                       "the stated page, which nothing throttles (D12). Not covered: a page being interacted with."),
    "element": ("It carries no message-traffic wakes: the traffic phase each repeat also ran (a stated scripted rate, "
                "design) stays in the campaign results and feeds no archetype (D11)."),
    "steam": ("Not covered: a client that is logged in, holds a library, downloads, or runs behind a game — the state "
              "the gaming timelines depict (D6)."),
}

# 9.10 D24: every file shows the observed program's name, `element-desktop` for the chat client, so no entry is bound
# by stated approximation (discord left the notes)
APPROX = {}

# D20, D22, D24: where a between-sessions component's spread lies — within one run (the probe, 600 s windows every
# 60 s) against across the repeats. Across-repeat figures for the renderer entries are recomputed from the pooled
# record; the within-run figures are the changelog's, measured on the probes — each regenerates (D38) with
# `desktop/within_run.py <probe> <phase> <analysis.json> 600 60 <comms> <skip-s>`, the hidden probe (run 35501749098,
# `steady`) from 300 s, the visible (run 35501680255, `steady-notimer`) from 0.
# 9.10 D156: the hidden renderer's own, re-read on 9.10's 3,600 s probe (run 37273691029) past its 1,030 s settle —
# `within_run.py <probe> steady <analysis.json> 600 60 <comms> 400`
GRACE = {"meas-ci:desktop:2026-09-20": ("20 s, grace-settle 630 s: 330 s of the documented five-minute default and 300 s "
                                       "read from the probe, D15"),
         "meas-ci:desktop:2026-10-05b": ("20 s, grace-settle 1,030 s: 330 s of the documented five-minute default, 300 s "
                                        "read from the probe (D15) and 400 s past the page thread's settling read from "
                                        "9.10's 3,600 s probe (9.10 D152)")}
WINDOWS_1005B = {
    "renderer-hidden": ("Read in 100 s windows over the 5 repeats (9.10 D156): the page's own thread `chrome` runs "
                        "0.068 ms in the first 100 s and 0.057–0.072 ms after, its settling past; the residual "
                        "(`MemoryInfra`, `ThreadPoolServi`) wakes at 3.6 times its phase rate in the first 100 s and "
                        "2.4 times 400–500 s in; the phase's windows hold 5.2 % of its CPU above its median window. The "
                        "carried values are the phase's means."),
}
SPAN_1005B = {
    "renderer-hidden": ("Read over 3,600 s in one long-phase probe past the 630 s grace-settle (9.10 D149, D152): the "
                        "page's own thread runs 0.106, 0.083, 0.077 and 0.080 ms a wake in its first four minutes and "
                        "0.055–0.060 ms from the seventh, the settling the 1,030 s settle now covers; past it a 600 s "
                        "window holds the wakes within 3.7 % of the probe's level at every placement and the CPU within "
                        "−7.2 % and +10.4 %, an episode recurring some 1,800 s apart — the page thread at 0.072–0.075 ms, "
                        "`Chrome_ChildIOT` waking 0.243–0.247/s against 0.200–0.210. The probe ran Google Chrome "
                        "154.0.8037.57, the build these repeats ran. That build is not the 152 and 153 9.8's campaign "
                        "and `web-browser` ran, Google's repository serving only its current build (9.5 D69; 9.10 "
                        "D156): against 9.8's 19 repeats the page's own thread wakes 1.72 times as often and "
                        "`Chrome_ChildIOT` 2.51 times, the renderer 0.211 against 0.169 wakes/s, while the page "
                        "thread's runs, its settling past, are 35 % shorter and the CPU share 9.6 against 9.2 × 10⁻⁵; "
                        "`web-browser` stays 152 and 153's, the two halves of one browser on two builds."),
}
WITHIN_1005B = {("chrome-hidden", "Chrome_ChildIOT"): "±8.1 % (9.10 D156)",
                ("chrome-hidden", "Compositor"): "±30.6 % (9.10 D156)",
                ("chrome-hidden", "PerfettoTrace"): "±30.6 % (9.10 D156)"}
WITHIN = {("chrome-hidden", "Chrome_ChildIOT"): "±17.7 % (D24)",
          ("chrome-visible", "Chrome_ChildIOT"): "±18.6 % (D20)",
          ("chrome-visible", "ThreadPoolForeg"): "barely present in the probe (D20)",
          ("chrome-hidden", "Compositor"): "±10.8 % (D26)", ("chrome-hidden", "PerfettoTrace"): "±10.8 % (D26)",
          ("chrome-hidden", "ThreadPoolServi"): "±10.8 % (D26)", ("chrome-visible", "PerfettoTrace"): "±4.0 % (D26)"}

# D34: where a carried phase does part of its work only in part of it, read in 100 s windows over the carried repeats
# (meas/windows.py, `campaign/results-windows.md`) — stated beside the values, which stay the phase's means
WINDOWS_STATED = {
    "renderer-hidden": ("Read in 100 s windows over the 19 repeats (D34): the page's own thread `chrome` runs longer "
                        "early in the phase than late, its run mean 0.107 ms in the first 100 s and 0.057 ms in the "
                        "last, and the residual (`MemoryInfra`) wakes at 5.2 times its phase rate 200–300 s into the "
                        "phase; the phase's windows hold 13.3 % of its CPU above its median window. The carried values "
                        "are the phase's means."),
    "renderer-visible": ("Read in 100 s windows over the 11 repeats (D34): every residual wake falls in the phase's "
                         "first 200 s, and `chrome`'s run mean is 0.179 and 0.231 ms there against 0.092–0.123 ms "
                         "after; the residual holds 12.5 % of the entry's CPU and the phase's windows 29.4 % of it "
                         "above its median window. The carried values are the phase's means."),
}

# D27: the renderer residuals are sparse — a few wakes per renderer per phase — so the within-run test (D26 re-read
# them on the probes) cannot place their spread; why, per entry, from D26's re-read.
SPARSE_WHY_1005B = {("chrome-hidden", "residual"): ("a 600 s window of 9.10's probe catches 1–4 of its wakes per renderer "
                                                    "(±64.0 % within one run, 9.10 D156)")}
SPARSE_WHY = {("chrome-hidden", "residual"): ("a 600 s window of the probe catches 0–2 of its wakes (±134.2 % within "
                                              "one run, D26)"),
              ("chrome-visible", "residual"): ("the probe does not reproduce its comms, 0.0009 against 0.0068 wakes/s "
                                               "(±181.3 % within one run, D26)")}


def fmt(v, label, unit=True):
    if label == "wakes/s":
        return f"{v:.4g}" + (" wakes/s" if unit else "")
    if label.startswith("gap") and v >= 10000:
        return f"{v / 1000:.1f}" + (" s" if unit else "")
    return f"{v:.4g}" + (" ms" if unit else "")


def span(vals, label, ref):
    """A range in the unit its mean is written in."""
    if label.startswith("gap") and ref >= 10000:
        return f"{min(vals) / 1000:.1f}–{max(vals) / 1000:.1f} s"
    return f"{fmt(min(vals), label, False)}–{fmt(max(vals), label, False)}{' wakes/s' if label == 'wakes/s' else ' ms'}"


def values_of(ph, comm, label):
    field = {"wakes/s": "wakes_per_s", "gap mean (ms)": "gap_ms", "run mean (ms)": "run_ms"}[label]
    src = ph["components"]["residual"] if comm == "residual" else ph["threads"][comm]
    if field == "wakes_per_s":
        vals = src["wakes_per_s"]
    elif comm == "residual":
        vals = src[field]["repeat_mean"]
    else:
        vals = [x.get("mean") for x in src[field] if x]
    return [v for v in vals if v is not None]


def heavy_events_block(ph, phase, indent="      "):
    """D33 (9.5 D64): a rare event's runs, carried as the campaign fold-in carries chrome's MemoryInfra pass — the run
    table, the count and the span it was counted over, and the rate that follows; no interval, none being measured."""
    h = ph.get("heavy_event")
    if not h or not h.get("runs_ms"):
        return []
    runs = sorted(h["runs_ms"])
    hit = [n for n in h["count"] if n]
    return [f"{indent}heavy_events:",
            f"{indent}  - comm: {json.dumps(h['comm'])}",
            f"{indent}    run_floor_ms: {h['run_floor_ms']:g}",
            f"{indent}    count: {sum(h['count'])}",
            f"{indent}    span_s: {h['span_s_total']:.1f}",
            f"{indent}    rate_per_s: {h['rate_per_s']:g}",
            f"{indent}    run: {yaml_table(quantile_table(runs), TAG)}",
            f"{indent}  # D33 (9.5 D64): {sum(h['count'])} runs of at least {h['run_floor_ms']:g} ms over "
            f"{h['span_s_total']:.0f} s of {phase} phase, {min(runs):.1f}–{max(runs):.1f} ms, {min(hit)}–{max(hit)} in one "
            f"burst in {len(hit)} of {len(h['count'])} repeats; their runs leave the component's wakes, each placed at the "
            f"carried rate, the burst's clustering not carried."]


def heavy_sentence(ph):
    """D33: the scope's statement of the rare event — its runs, where the repeats caught it and what is not carried."""
    h = ph["heavy_event"]
    runs = h["runs_ms"]
    hit = [(ph["repeats"][i], n, ts) for i, (n, ts) in enumerate(zip(h["count"], h["at_s"])) if n]
    at = [t for _, _, ts in hit for t in ts]
    width = max(max(ts) - min(ts) for _, _, ts in hit)
    return (f"A rare event within a run (9.5 D64; D33): `{h['comm']}`'s runs of {h['run_floor_ms']:g} ms or more — "
            f"{sum(h['count'])} over the {len(h['count'])} repeats' {h['span_s_total']:.0f} s, "
            f"{min(runs):.1f}–{max(runs):.1f} ms, {min(n for _, n, _ in hit)}–{max(n for _, n, _ in hit)} in one burst "
            f"within {width:.1f} s in {len(hit)} of the repeats ({', '.join(str(k) for k, _, _ in hit)}), "
            f"{min(at):.1f}–{max(at):.1f} s into the phase — leave the component, which is read without them, and are "
            f"carried as a stated event at their rate, {h['rate_per_s']:g} a second; the burst's clustering is not "
            f"carried. ")


def component(comm, threads, wps, gap, run, extra=None, indent="        "):
    lines = [f"{indent}- comm: {json.dumps(comm)}"]
    if extra:
        lines.append(f"{indent}  comms: [" + ", ".join(json.dumps(x) for x in extra) + "]")
    lines.append(f"{indent}  threads: {threads}")
    lines.append(f"{indent}  wakes_per_s: {wps:.5g}")
    lines.append(f"{indent}  gap: {yaml_table(gap['table'], TAG)}")
    lines.append(f"{indent}  run: {yaml_table(run['table'], TAG)}")
    return lines


def thread_count(t):
    flat = [max(x) if isinstance(x, list) and x else x for x in t]
    lo, hi = min(flat), max(flat)
    return str(lo) if lo == hi else f"[{lo}, {hi}]"


def cpu_shares(ph, comms):
    """D37: each component's share of the phase's CPU — its runs over the phase's, pooled over the repeats, the heavy
    event's runs (D33) counted in the phase — the share of the job's time the workflow asks an excepted value to state."""
    runs = lambda t: sum(x["sum"] for x in t["run_ms"] if x)
    total = sum(runs(t) for t in ph["threads"].values()) + sum((ph.get("heavy_event") or {}).get("runs_ms") or [])
    return [runs(ph["threads"][c]) / total for c in comms]


def exceptions(app, e, ph):
    machine, session, sparse = [], {}, {}
    machine_comms = []
    for key, c in e["stability"]["quantities"].items():
        if c["passes"]:
            continue
        rest = key[len(CARRIED[app]) + 1:]
        label = next(lb for lb in LABEL if rest.endswith(" " + lb))
        comm = rest[:-len(label) - 1]
        vals = values_of(ph, comm, label)
        text = (f"{LABEL[label]} {fmt(c['mean'], label)} ±{c['half_width'] * 100:.1f} % "
                f"({span(vals, label, c['mean'])})")
        if c.get("sparse"):
            sparse.setdefault(comm, []).append(text)
        elif c.get("session_spread"):
            session.setdefault(comm, []).append(text)
        else:
            machine.append(f"`{comm}` {text}")
            machine_comms.append(comm)
    return machine, session, sparse, machine_comms


def entry(app, e):
    ph = e["phases"][CARRIED[app]]
    comp = ph["components"]
    k = len(e["repeats"])
    renderer = app.startswith("chrome")
    out = [f"  {IDS[app]}:", "    category_source: meas", "    pattern:", "      program:",
           "        - loop:                    # measured timer components merged at compile time, each wake on the task's timer channel (9.5 D9, D16, D74)",
           "            - WAIT: timer", "            - RUN: event", "    params:", "      components:"]
    for comm in comp["selected"]:
        t = ph["threads"][comm]
        tab = ph["tables"][comm]
        out += component(comm, thread_count(t["threads"]), statistics.fmean(t["wakes_per_s"]),
                         tab["gap_ms"], tab["run_ms"])
    r = comp["residual"]
    if r and r["gap_ms"]["table"]:
        out += component("residual", thread_count(r["threads"]), statistics.fmean(r["wakes_per_s"]),
                         r["gap_ms"], r["run_ms"], extra=r["comms"])
    unit = " per renderer" if renderer else ""
    out.append(f"        # {len(comp['selected'])} comms cover {comp['covered_share'] * 100:.1f} % of "
               f"{comp['total_wakes_per_s']:.3f} wakes/s{unit} (9.5 D16, target 95 %); the rest pooled as `residual`")
    out += heavy_events_block(ph, CARRIED[app])
    out += ["    lifetime: segment-bound", "    binding_params: []", "    scalable: []", "    validation_stats:",
            "      referee: meas-ci"]
    runs = sorted(set(v for v in e["run_id"].values() if v))
    reps = ", ".join(str(x) for x in e["repeats"])
    out.append(f"      run: \"{TAG.split(':', 1)[1]}, repeats [{reps}], runs {', '.join(runs)}\"")
    per = ph["wakes_per_s_per_renderer"] if renderer else ph["wakes_per_s"]
    stats = [f"{CARRIED[app]} wakes/s{unit} {min(per):.4f}–{max(per):.4f}",
             f"{CARRIED[app]} cpu-share {min(ph['cpu_share']):.5f}–{max(ph['cpu_share']):.5f}"]
    out.append("      stats: [" + ", ".join(json.dumps(s) for s in stats) + "]")

    machine, session, sparse, machine_comms = exceptions(app, e, ph)
    # 9.5 D69: Chrome's build recorded per repeat and its census stated, Google's repository serving only its current
    observed = OBSERVED[app].replace("{build}", _cp.build_census(e["version"])).replace("{grace}", GRACE[TAG])
    new = TAG == "meas-ci:desktop:2026-10-05b"   # 9.10 D152: the hidden renderer's own campaign
    scope = (f"One observation (phase decision 2; D10): {observed}; on {MACHINE}; {k} same-machine repeats, "
             f"every landing pooled (D24). ")
    if renderer:
        meas = sorted(set(e["renderers_measured"].values()))
        obs = sorted(set(int(v) for v in e["renderers"].values()))
        scope += (f"Values describe one renderer, the {meas[0]} page renderers a job measures pooled as its samples "
                  f"(D14), of {obs[0] if obs[0] == obs[-1] else f'{obs[0]}–{obs[-1]}'} "
                  f"--type=renderer processes observed — the control tab, Chrome's own extension and WebUI renderers "
                  f"and any renderer present for part of the phase dropped. ")
        hw = statistics.fmean(ph["threads"]["HangWatcher"]["wakes_per_s"])
        pg = statistics.fmean(ph["threads"]["chrome"]["wakes_per_s"])
        scope += (f"The entry is majority `HangWatcher`, Chromium's hang-detection thread, {hw:.3f} of "
                  f"{statistics.fmean(per):.3f} wakes/s per renderer; the page's own thread is {pg:.3f} (D16). ")
    scope += STATE_NOT[app] + " "
    scope += ("Stability rule (9.5 D78): every value on the list — a table read by the mean it carries, over every "
              "repeat's samples — holds within 5 % or 1 µs")
    if machine or session or sparse:
        scope += " except these, carried over the repeats obtained with their half-widths and ranges. "
    else:
        scope += " over the repeats obtained. "
    if machine:
        scope += ("Run means whose spread is the runner's speed, every thread of a repeat moving together while wake "
                  f"rates hold (D17{', D18' if app == 'steam' else ''}): " + "; ".join(machine) + ". ")
        shares = [f"{x * 100:.1f} %" for x in cpu_shares(ph, machine_comms)]
        listed = shares[0] if len(shares) == 1 else ", ".join(shares[:-1]) + " and " + shares[-1]
        scope += (f"{'Their runs hold' if len(shares) > 1 else 'Its runs hold'} {listed} of the phase's CPU"
                  + (f", {sum(cpu_shares(ph, machine_comms)) * 100:.1f} % together" if len(shares) > 1 else "") + " (D37). ")
    if ph.get("heavy_event"):
        scope += heavy_sentence(ph)
    if session:
        parts = []
        for comm, texts in session.items():
            w = (WITHIN_1005B if new else WITHIN).get((app, comm))
            wr = values_of(ph, comm, "wakes/s")
            across = f"±{(max(wr) - min(wr)) / 2 / statistics.fmean(wr) * 100:.1f} %" if statistics.fmean(wr) else "—"
            where = f"; within one run {w}, its wake rate across the repeats {across}" if w else ""
            parts.append(f"`{comm}` " + ", ".join(texts) + where)
        law = {"chrome-hidden": "D21, D24, D26" + ("; 9.10 D156" if new else ""), "chrome-visible": "D21, D26"}[app]
        scope += (f"Components whose rate varies between sessions, their values carried together (9.5 D57; {law}): "
                  + "; ".join(parts) + ". ")
        if renderer:
            per = [statistics.fmean(values_of(ph, comm, "wakes/s")) * statistics.fmean(ph["span_s"]) for comm in session]
            scope += f"These threads wake {min(per):.1f}–{max(per):.1f} times per renderer per 600 s phase. "
    if sparse:
        parts = []
        for comm, texts in sparse.items():
            comms = ph["components"]["residual"]["comms"] if comm == "residual" else [comm]
            per = [w * s for w, s in zip(values_of(ph, comm, "wakes/s"), ph["span_s"])]
            parts.append(f"`{comm}` (" + ", ".join(f"`{c}`" for c in comms) + ") " + ", ".join(texts)
                         + f", {min(per):.1f}–{max(per):.1f} wakes per renderer per 600 s phase; "
                         + (SPARSE_WHY_1005B if new else SPARSE_WHY)[(app, comm)])
        scope += ("Sparse components, waking a few times per renderer per phase, their values carried together with "
                  "their half-widths and their count, a spread that is the count's own and which the within-run test "
                  "cannot place (D27): " + "; ".join(parts) + ". ")
    for c in e.get("comparisons") or []:
        if c.get("ratio"):
            scope += (f"Measured beside it, {c['what']}: wake rate {c['a_wakes_per_s']:.3f} against "
                      f"{c['b_wakes_per_s']:.3f} ({c['ratio']}×)"
                      + (f", the comparison D5 rests on; the CPU share ratio, {c['cpu_share_ratio']}×, is reported with "
                         f"its spread and no effect rests on it (D18). " if app == "steam" else
                         f", CPU share {c['cpu_share_ratio']}×. "))
    windows = WINDOWS_1005B if new else WINDOWS_STATED
    if IDS[app] in windows:
        scope += windows[IDS[app]] + " "
    if new and IDS[app] in SPAN_1005B:
        scope += SPAN_1005B[IDS[app]] + " "
    scope += "Values are this software on this machine, not desktop truth (9.5 D10)."
    out += ["      scope: >-", "        " + scope]

    notes = ("Per-application archetype (9.5 D2): one task carries the "
             + ("one renderer process, the renderers of a browsing session bound as separate tasks (D2) — under "
                "Chromium's site-per-process model one renderer is one site, not one tab (S2-01); web-browser carries "
                "the rest of the browser's tree, the renderer of the page in use included (9.5 D84). " if renderer else "whole process tree merged (9.5 D14). ")
             + "Timer components are per thread comm (9.5 D16), each sampled from its measured gap and run quantiles "
               "(9.5 D17) over the task's lifetime and merged into one explicit event stream at compile time (9.5 D9); "
               "the pooled residual stands for the comms below the coverage cut. No focus_components and no stimulus: "
               "the state is unattended by construction (D10).")
    spor = comp.get("sporadic") or []
    if spor:
        notes += " Sporadic wakes, not carried as components (9.5 D43): " + "; ".join(
            f"`{s['comm']}` in {len(s['repeats'])} of {k} repeats, {s['wakes_per_s']} wakes/s" for s in spor) + "."
    if app in APPROX:
        notes += " " + APPROX[app]
    if IDS[app] in CONTROL:   # the untraced control's reading (its record's `notes`)
        notes += " " + CONTROL[IDS[app]]
    out += ["    modeling_notes: >-", "      " + notes]
    return "\n".join(out)


def main():
    CONTROL.clear()   # a run without --control carries no reading, whatever a run before it read
    args = sys.argv[1:]
    if "--control" in args and args.index("--control") + 1 < len(args):
        i = args.index("--control")
        CONTROL.update({a: r["notes"] for a, r in json.load(open(args[i + 1]))["archetypes"].items()})
        del args[i:i + 2]
    only = None
    if "--only" in args and args.index("--only") + 1 < len(args):
        i = args.index("--only")
        only = set(args[i + 1].split(","))
        del args[i:i + 2]
    if len(args) != 2:
        raise SystemExit(__doc__)
    sys.argv[1:] = args
    p = json.load(open(sys.argv[1]))
    global TAG
    if p.get("tag") not in CAMPAIGNS:
        raise SystemExit(f"pooled record tagged {p.get('tag')!r}, expected one of {', '.join(CAMPAIGNS)}")
    TAG = p["tag"]
    folded = [a for a in FOLDED if a in CAMPAIGNS[TAG] and (only is None or a in only)]
    blocks = [f"  # ---- measured per-application archetypes — 9.8 campaign ({TAG}) ----", ""]
    for app in folded:
        if not p["runs"][app]["stability"]["passes"]:
            raise SystemExit(f"{app}: the stability rule does not hold on this pooled record")
        blocks += [entry(app, p["runs"][app]), ""]
    open(sys.argv[2], "w").write("\n".join(blocks))
    print(f"wrote {sys.argv[2]}: {len(folded)} entries")


if __name__ == "__main__":
    main()
