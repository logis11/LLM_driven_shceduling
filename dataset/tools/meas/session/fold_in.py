#!/usr/bin/env python3
"""Generate the four 9.9 archetype entries from the session campaign's pooled record (changelog D2–D7, D26–D30).

  fold_in.py <pooled.json> <out.yaml>     (reads `within-run.json` beside the pooled record)

One entry per program of the Ubuntu desktop session, in 9.5's measured form: `components`, one per process instance
and thread comm of the `steady` phase (D4, D6, D7), each with its `wakes_per_s` and its pooled `gap` and `run`
quantile tables; no residual, no `focus_components`, no `stimulus`. The scope states what method §7 and the changelog
require of each entry: the machine, the package versions, the state and what it is not, the limits of the
observation, the instances that never woke or woke only sporadically, the wakes that left the components by cause
(D27) and the cron session (D23, D26), each stated and not carried, the components carried with their half-widths
under D29 with both spreads (D28), and the foreign work on the measured CPU (D20, D22). The output is a YAML fragment
for `dataset/archetypes.yaml`.
"""

import json
import os
import statistics
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # dataset/tools
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)
from meas.distribution import yaml_table  # noqa: E402

TAG = "meas-ci:session:2026-09-24"
PHASE = "steady"
IDS = {"gnome-shell": "compositor-shell", "pipewire": "audio-server", "systemd": "service-manager",
       "dbus-daemon": "message-bus"}
LABEL = {"wakes/s": "wake rate", "gap mean (ms)": "gap mean", "run mean (ms)": "run mean"}

OBSERVED = ("an Ubuntu 24.04 desktop session — ubuntu-desktop-minimal from the runner's own archive, a dedicated user "
            "logged in by GDM's automatic login after a 300 s priming login and a logout (D16) — in its terminal idle "
            "state: nobody present past idle-delay, the shield up and locked, the monitor blanked by the power daemon, "
            "each checked at the steady edge 420 s after the measured login (D9, D13, D18); a 1800 s steady phase "
            "(D22)")

MACHINE = ("a GitHub-hosted ubuntu-24.04 runner (4 vCPU AMD EPYC 7763, kernel 6.17.0-1022-azure), the four entries' "
           "processes confined to one CPU and every other process of the session, the system and the harness kept on "
           "the others, the placement read from the processes after the pin and at the steady edge (D10, D21), perf "
           "sched record on every CPU")

LIMITS = ("Limits of the observation (method §7): GNOME Shell started with --headless --virtual-monitor 1920x1080@60 by "
          "a unit drop-in, on a seat with no display device and no vblank; no sound device, WirePlumber's null sink; "
          "the cpuset controller delegated to the user manager by a drop-in on user@.service (D14); the four entries' "
          "units in a slice of their own and the other slices defaulted to the other CPUs (D17), the system bus "
          "restarted into that slice before any login (D21); the pinned units' other processes moved into a scope of "
          "their own (D15); per-CPU kernel threads sharing the measured CPU; a server VM with its own agents, off the "
          "measured CPU.")

PROGRAM = {
    "gnome-shell": ("GNOME Shell {gnome-shell} — Mutter and the shell in one process (D3)",
                    ["gnome-shell"]),
    "pipewire": ("the PipeWire stack — pipewire {pipewire}, wireplumber {wireplumber}, pipewire-pulse "
                 "{pipewire-pulse} — its three user services in one task (D4)",
                 ["pipewire", "wireplumber", "pipewire-pulse"]),
    "systemd": ("systemd {systemd} — pid 1 and the user manager in one task (D7)", ["pid1", "user-manager"]),
    "dbus-daemon": ("dbus-daemon {dbus-daemon} — the system bus and the session bus in one task (D6)",
                    ["system-bus", "session-bus"]),
}

STATE_NOT = {
    "gnome-shell": ("Not covered: drawing. The monitor is off, and Mutter's frame clock is inhibited while the output "
                    "is off (S2-12); no source states a compositor's per-frame CPU cost on a GPU desktop (9.5 D24). "
                    "Nor a session in use — an application open, the screen on, a notification — nor the session's "
                    "start-up (D9)."),
    "pipewire": "Not covered: playback or capture, nor the session's start-up (D9).",
    "systemd": "Not covered: unit starts and stops of a session in use, nor boot and login (D9).",
    "dbus-daemon": "Not covered: the bus traffic of a session in use, nor the session's start-up (D9).",
}

BINDING = {
    "gnome-shell": "the timelines' `gnome-shell` task",
    "pipewire": "the timelines' `pipewire` task, which stands for the three services (D4)",
    "systemd": "the timelines' `systemd` task, which stands for both managers (D7)",
    "dbus-daemon": "the timelines' `dbus-daemon` task, which stands for both buses (D6)",
}

# D26: the rows a cron session's window held left each component (D23); what caused them, read from the four repeats'
# journals: the runner image's sphinxsearch indexer job at 00:00 UTC, no package of the desktop install.
CRON_CAUSE = ("the session of the sphinxsearch indexer's cron job at 00:00 UTC — a package of the runner image, not of "
              "the desktop install —")


def thread_count(t):
    lo, hi = min(t), max(t)
    return str(lo) if lo == hi else f"[{lo}, {hi}]"


def component(comm, t, tab, indent="        "):
    return [f"{indent}- comm: {json.dumps(comm)}",
            f"{indent}  threads: {thread_count(t['threads'])}",
            f"{indent}  wakes_per_s: {statistics.fmean(t['wakes_per_s']):.5g}",
            f"{indent}  gap: {yaml_table(tab['gap_ms']['table'], TAG)}",
            f"{indent}  run: {yaml_table(tab['run_ms']['table'], TAG)}"]


def within_figures(w):
    """D28, D35: where a carried component's spread lies — `within_run.py`'s record beside the pooled one: within one
    run, the unpolled region of the long-phase probes 36, 41 and 44 read under the pool's causes, a window of the
    phase's 1800 s every 60 s, against across the 24 repeats; half the range over the mean. Its three values' ranges
    within, then their spreads across."""
    pct = lambda x: f"{x * 100:.1f}"
    within = [[probe[label] for probe in w["within"].values()] for label in LABEL]
    return (tuple(f"±{pct(min(v))}–{pct(max(v))} %" for v in within)
            + tuple(f"±{pct(w['across'][label])} %" for label in LABEL))


def split_list(prog, stab):
    """The entry's values: (passing [(half-width, component, label)], the components carried under D29). A carried
    component's three values are carried together (9.5 D57), those that pass on their own with them."""
    rows = []
    for key, c in stab["quantities"].items():
        if key.startswith(prog + " "):
            rest = key[len(prog) + 1:]
            label = next(lb for lb in LABEL if rest.endswith(" " + lb))
            rows.append((rest[:-len(label) - 1], label, c))
    carried = [comp for comp, _l, c in rows if not c["passes"] and c.get("carried")]
    carried = list(dict.fromkeys(carried))
    ok = [(c["half_width"], comp, label) for comp, label, c in rows if comp not in carried]
    return ok, carried


def fmt_value(v, label, unit=True):
    if label == "wakes/s":
        return f"{v:.4f}" + (" wakes/s" if unit else "")
    if label.startswith("gap") and v >= 10000:
        return f"{v / 1000:.1f}" + (" s" if unit else "")
    return (f"{v:.1f}" if label.startswith("gap") else f"{v:.3f}") + (" ms" if unit else "")


def stability_text(prog, e, stab, k, within):
    ok, carried = split_list(prog, stab)
    text = ""
    if ok:
        hw, comp, label = max(ok)
        text = (f"Stability rule (9.5 D78): {'all ' if not carried else ''}{len(ok)} value{'s' if len(ok) > 1 else ''} "
                f"on the list — a table read by the mean it carries, over every repeat's samples — "
                f"hold{'s' if len(ok) == 1 else ''} within 5 % or 1 µs over the {k} repeats, the widest `{comp}` "
                f"{LABEL[label]} ±{hw * 100:.2f} %. ")
    for comp in carried:
        th, parts = e["threads"][comp], []
        for i, label in enumerate(LABEL):
            q = stab["quantities"][f"{prog} {comp} {label}"]
            vals = th["wakes_per_s"] if label == "wakes/s" else [x["mean"] for x in th[
                "gap_ms" if label.startswith("gap") else "run_ms"] if x]
            parts.append(f"{LABEL[label]} {fmt_value(q['mean'], label)} ±{q['half_width'] * 100:.1f} % "
                         f"({fmt_value(min(vals), label, False)}–{fmt_value(max(vals), label)}"
                         + (f" over the {len(vals)} repeats it woke in" if len(vals) != k else "") + ")")
        n = [round(r * statistics.fmean(e["span_s"])) for r in th["wakes_per_s"]]
        if stab["quantities"][f"{prog} {comp} wakes/s"].get("sparse"):
            without = next((x["repeats_without"] for x in e["components"].get("sparse", []) if x["comm"] == comp), [])
            text += (f"`{comp}` is carried as a sparse component, its three values together with their half-widths "
                     f"and its count (9.8 D27; D33): {'; '.join(parts)}. It wakes {min(n)}–{max(n)} times a phase"
                     + (f", none at all in {len(without)} of the {k} repeats — its gap table is over the {k} repeats "
                        f"laid end to end and wrapped round, the silent ones adding their time (9.5 D71), so the entry "
                        f"compiles at the rate it carries" if without else "")
                     + ", and is the entry's whole activity once the wakes owed to outside causes are out (D27, D32); "
                       "its spread is the count's own, which the within-run test cannot place. ")
            continue
        w = within_figures(within[f"{prog} {comp}"])
        text += (f"`{comp}`'s three values are carried together with their half-widths under 9.5 D57 as 9.8 D21 "
                 f"extended it (D28, D29): {'; '.join(parts)}. Within one run (the long-phase probes 36, 41 and 44, "
                 f"a window of the phase every 60 s) they move by {w[0]}, {w[1]} and {w[2]} of their mean, against "
                 f"{w[3]}, {w[4]} and {w[5]} across the repeats (half the range over the mean): the spread lies in "
                 f"part within a run. It wakes {min(n)}–{max(n)} times a phase and is the entry's whole activity once "
                 f"the wakes owed to outside causes are out (D27). ")
    return text


def causes_text(e, k):
    c = e.get("causes") or {}
    rng = lambda ns: f"{min(ns)}–{max(ns)}" if min(ns) != max(ns) else f"{min(ns)}"
    text = ""
    if c.get("outside"):
        text += ("Wakes traced to a cause outside the observed desktop — a package Ubuntu 24.04's desktop manifest "
                 "does not hold, a desktop package's unit that a stock install leaves disabled and the runner image "
                 "enabled, or the harness — left the components and are stated (D27, D32): "
                 + "; ".join(f"{lab} {rng(ns)} a phase" for lab, ns in c["outside"].items()) + ". ")
    if c.get("event"):
        text += ("Desktop jobs bound to a clock time are events of the phase, stated and not carried (D27, in D23's "
                 f"form): " + "; ".join(f"{lab} {sum(ns)} over the {k} repeats" for lab, ns in c["event"].items())
                 + ". ")
    if c.get("unknown"):
        text += ("Kept, their cause not resolved by the trace: "
                 + "; ".join(f"{lab} {sum(ns)} over the {k} repeats" for lab, ns in c["unknown"].items()) + ". ")
    desk = c.get("desktop") or {}
    if any("systemd-networkd" in lab for lab in desk):
        text += ("The wakes systemd-networkd causes are kept by the package rule; whether a stock desktop, which runs "
                 "NetworkManager, also runs networkd is unverified (D27). ")
    return text


def cron_text(e):
    ce = e["cron_event"]
    hit = [(k, n) for k, n in zip(e["repeats"], ce["count"]) if n]
    if not hit:
        return ""
    at = [x for r in ce["at_s"] for x in r]
    counts = ", ".join(str(n) for _, n in hit)
    return (f"A cron job's session is stated, not carried (D23, D26): {CRON_CAUSE} met the phase in {len(hit)} of "
            f"{len(e['repeats'])} repeats ({', '.join(str(k) for k, _ in hit)}), {min(at):.0f}–{max(at):.0f} s into "
            f"it; the {sum(n for _, n in hit)} rows it held inside two seconds of each cron wakeup ({counts} per "
            f"repeat) left the components, which are read without them. ")


def entry(prog, e, run, within):
    comp = e["components"]
    k = len(e["repeats"])
    out = [f"  {IDS[prog]}:", "    category_source: meas", "    pattern:", "      program:",
           "        - loop:                    # measured timer components merged at compile time, each wake on the task's timer channel (9.5 D9, D16, D74)",
           "            - WAIT: timer", "            - RUN: event", "    params:", "      components:"]
    for comm in comp["selected"]:
        out += component(comm, e["threads"][comm], e["tables"][comm])
    if comp["residual"]:
        raise SystemExit(f"{prog}: a residual component — the generator writes none")
    n_sel = len(comp["selected"])
    out.append(f"        # {n_sel} component{'s' if n_sel > 1 else ''} cover{'' if n_sel > 1 else 's'} "
               f"{comp['covered_share'] * 100:.2f} % of {comp['total_wakes_per_s']:.3f} wakes/s (9.5 D16, target 95 %); no residual — every other wake "
               f"sporadic (modeling_notes)")
    out += ["    lifetime: segment-bound", "    binding_params: []", "    scalable: []", "    validation_stats:",
            "      referee: meas-ci"]
    runs = sorted(set(v for v in run["run_id"].values() if v))
    reps = ", ".join(str(x) for x in e["repeats"])
    out.append(f"      run: \"session:2026-09-24, repeats [{reps}], runs {', '.join(runs)}\"")
    stats = [f"{PHASE} wakes/s {min(e['wakes_per_s']):.4f}–{max(e['wakes_per_s']):.4f}",
             f"{PHASE} cpu-share {min(e['cpu_share']):.6f}–{max(e['cpu_share']):.6f}"]
    out.append("      stats: [" + ", ".join(json.dumps(s) for s in stats) + "]")

    versions = next(iter(run["versions"].values()))
    if any(v != versions for v in run["versions"].values()):
        raise SystemExit("package versions differ across repeats")
    what, instances = PROGRAM[prog]
    foreign = run["foreign"].values()
    share = [f["share_of_phase"] for f in foreign]
    kth = [f["kernel"]["schedule_ins"] for f in foreign]
    scope = (f"One observation (phase decision 2; D8): {what.format(**versions)}, in {OBSERVED}; on {MACHINE}; {k} "
             f"same-machine repeats, every landing pooled. {STATE_NOT[prog]} {LIMITS} ")
    scope += stability_text(prog, e, run["stability"], k, within)
    scope += causes_text(e, k)
    scope += cron_text(e)
    scope += (f"Foreign user-space work on the measured CPU {min(share) * 100:.5f}–{max(share) * 100:.4f} % of the "
              f"phase per repeat, under the 2 × 10⁻⁴ bound (D20, D22); per-CPU kernel threads "
              f"{min(kth):,}–{max(kth):,} schedule-ins on it per repeat, reported, not gated (D14). ")
    scope += "Values are this software on this machine, not desktop truth (9.5 D10)."
    out += ["      scope: >-", "        " + scope]

    woke = {c.split("/", 1)[0] for c in e["threads"]}
    every = e.get("instance_wakes_all") or {}
    silent = [i for i in instances if i not in woke and not sum(every.get(i, [0]))]
    left_only = [i for i in instances if i not in woke and sum(every.get(i, [0]))]
    notes = (f"Per-program archetype (D2, D5), bound by identity to {BINDING[prog]}: one task carries the program's "
             f"processes, each instance's threads its own components (D4, D6, D7; 9.5 D16), each sampled from its "
             f"measured gap and run quantiles (9.5 D17) over the task's lifetime and merged into one explicit event "
             f"stream at compile time (9.5 D9). No focus_components and no stimulus: nobody is present (D9).")
    if silent:
        notes += (" Present in every repeat and never woken in the phase: "
                  + ", ".join(f"`{i}`" for i in silent) + "; the entry carries no wake of "
                  + ("them." if len(silent) > 1 else "it."))
    for i in left_only:
        reps_with = [k for k, n in zip(e["repeats"], every[i]) if n]
        notes += (f" `{i}` woke only in repeats {', '.join(str(k) for k in reps_with)} ({sum(every[i])} wakes), every "
                  f"one of them taken out of the component by the cron session's window (D23) or by its cause (D27); "
                  f"the entry carries none.")
    spor = comp.get("sporadic") or []
    cron = {r for r, n in zip(e["repeats"], e["cron_event"]["count"]) if n}
    if spor:
        notes += " Sporadic wakes, not carried as components (9.5 D43): " + "; ".join(
            f"`{c}` in {len(s['repeats'])} of {k} repeats ({', '.join(str(x) for x in s['repeats'])}"
            + (", the repeats that met the cron session" if set(s["repeats"]) == cron else "")
            + f"), {s['wakes_per_s']} wakes/s over the pool"
            for s in spor for c in s["comms"]) + "."
    out += ["    modeling_notes: >-", "      " + notes]
    return "\n".join(out)


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    p = json.load(open(sys.argv[1]))
    if p.get("tag") != TAG:
        raise SystemExit(f"pooled record tagged {p.get('tag')!r}, expected {TAG!r}")
    run = p["runs"]["session"]
    if not run["stability"]["passes"]:
        raise SystemExit("the stability rule does not hold on this pooled record")
    entries = run["phases"][PHASE]["entries"]
    within = json.load(open(os.path.join(os.path.dirname(sys.argv[1]), "within-run.json")))
    blocks = [f"  # ---- session and system processes — 9.9 campaign ({TAG}) ----", ""]
    for prog in IDS:
        blocks += [entry(prog, entries[prog], run, within), ""]
    open(sys.argv[2], "w").write("\n".join(blocks))
    print(f"wrote {sys.argv[2]}: {len(IDS)} entries")


if __name__ == "__main__":
    main()
