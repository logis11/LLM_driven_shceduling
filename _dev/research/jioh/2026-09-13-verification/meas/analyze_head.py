#!/usr/bin/env python3
"""Fold-in analysis: downloaded meas-ci artifacts -> fitted parameters.

Usage: analyze.py <dir> [--json OUT]
  <dir> contains cli/meas-cli-r{1..5}/ and gui/meas-gui-r{1..5}/ as
  downloaded by `gh run download`.

Per parameter target it reports median / sigma_log fits with per-repeat
values (the N-run spread the scope package requires). Structural/shape
claims only; absolutes carry the runner spec recorded in each repeat's
spec.json (building-plan §7).
"""

import argparse
import datetime
import json
import math
import pathlib
import re
import statistics
import sys

TICK_US = 10_000  # USER_HZ=100 on the runners (spec.json corroborates)

COMPILER_NAMES = {"cc1", "cc1plus", "gcc", "g++", "as", "ld", "collect2",
                  "objtool", "fixdep", "objcopy", "genksyms", "modpost"}
DAEMON_NAMES = {"systemd", "systemd-journal", "systemd-udevd", "systemd-resolve",
                "systemd-network", "systemd-logind", "dbus-daemon", "cron",
                "rsyslogd", "polkitd", "chronyd", "multipathd", "agetty",
                "packagekitd", "udisksd", "acpid"}

_DUR = re.compile(r"(?:(\d+)h)?(?:(\d+)m)?([\d.]+)s")
_EXIT = re.compile(
    r"^(\d\d:\d\d:\d\d)\s+exit\s+(\d+)\s+\S+\s+(\S+)\s+(.*)$")
_EXEC = re.compile(r"^(\d\d:\d\d:\d\d)\s+exec\s+(\d+)\s+(.*)$")


def parse_duration_us(text):
    m = _DUR.fullmatch(text)
    if not m:
        return None
    hours, minutes, seconds = m.groups()
    total = (int(hours or 0) * 3600 + int(minutes or 0) * 60 + float(seconds))
    return round(total * 1e6)


def hms_us(epoch_us):
    dt = datetime.datetime.fromtimestamp(epoch_us / 1e6, datetime.timezone.utc)
    return dt.hour * 3600 + dt.minute * 60 + dt.second


def hms_str(text):
    hours, minutes, seconds = text.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds)


def load_phases(repeat_dir):
    phases = {}
    for line in (repeat_dir / "phases.jsonl").open():
        rec = json.loads(line)
        phases[rec["phase"]] = (hms_us(rec["start_us"]), hms_us(rec["end_us"]),
                                rec["end_us"] - rec["start_us"], rec["rc"])
    return phases


def good(phases, name):
    """Phase window iff it ran and exited 0 — failed phases are excluded
    from analysis (e.g. cli:2 r1's transient download failure)."""
    entry = phases.get(name)
    return entry if entry and entry[3] == 0 else None


def moment_matched(median_us, mean_us_value):
    """Lognormal sigma from the median/mean pair: mean = median·e^{σ²/2}."""
    if not median_us or not mean_us_value or mean_us_value <= median_us:
        return None
    return round(math.sqrt(2 * math.log(mean_us_value / median_us)), 3)


def lognormal_fit(values_us):
    logs = [math.log(v) for v in values_us if v > 0]
    if len(logs) < 2:
        return None
    median = math.exp(statistics.mean(logs))
    return {"n": len(logs), "median_us": round(median),
            "sigma_log": round(statistics.stdev(logs), 3),
            "p90_us": round(sorted(values_us)[int(len(values_us) * 0.9)])}


def in_phase(t, window):
    return window[0] <= t <= window[1]


# ---- lifecycle (forkstat) ---------------------------------------------------

def exits_in_window(repeat_dir, window, names=None):
    """Exit durations (µs) for processes whose *birth* fell in the window."""
    durations = []
    for line in (repeat_dir / "lifecycle.log").open(errors="replace"):
        m = _EXIT.match(line)
        if not m:
            continue
        t, _pid, dur_text, cmdline = m.groups()
        dur = parse_duration_us(dur_text)
        if dur is None:
            continue
        birth = hms_str(t) - dur / 1e6
        if not (window[0] <= birth <= window[1]):
            continue
        if names is not None:
            base = pathlib.PurePath(cmdline.split()[0]).name if cmdline else ""
            if base not in names:
                continue
        durations.append(max(dur, 1000))  # forkstat floor: 1 ms resolution
    return durations


def count_execs(repeat_dir, window, names):
    count = 0
    for line in (repeat_dir / "lifecycle.log").open(errors="replace"):
        m = _EXEC.match(line)
        if not m:
            continue
        t, _pid, cmdline = m.groups()
        if not in_phase(hms_str(t), window):
            continue
        base = pathlib.PurePath(cmdline.split()[0]).name if cmdline else ""
        if base in names:
            count += 1
    return count


# ---- /proc samples ----------------------------------------------------------

def iter_samples(repeat_dir):
    for line in (repeat_dir / "proc_samples.jsonl").open():
        yield json.loads(line)


def phase_cpu(repeat_dir, window, match):
    """Aggregate cpu-tick delta and peak concurrent count for matching procs."""
    first, last = {}, {}
    peak = 0
    for rec in iter_samples(repeat_dir):
        t = hms_us(rec["t"])
        if not in_phase(t, window):
            continue
        live = 0
        for proc in rec["procs"]:
            if not match(proc["comm"]):
                continue
            live += 1
            key = (proc["pid"], proc["starttime"])
            ticks = proc["utime"] + proc["stime"]
            first.setdefault(key, ticks)
            last[key] = ticks
        peak = max(peak, live)
    ticks = sum(last[k] - first[k] for k in last)
    # short-lived procs missed between 1 s samples contribute first==last
    return ticks * TICK_US, peak


def per_proc_duty(repeat_dir, window, match):
    """Median per-process duty (cpu-seconds / wall) among matching procs
    observed >= 3 s — the single-stream ratio the io archetypes bind."""
    first, last, seen = {}, {}, {}
    for rec in iter_samples(repeat_dir):
        t = hms_us(rec["t"])
        if not in_phase(t, window):
            continue
        for proc in rec["procs"]:
            if not match(proc["comm"]):
                continue
            key = (proc["pid"], proc["starttime"])
            ticks = proc["utime"] + proc["stime"]
            first.setdefault(key, (t, ticks))
            last[key] = (t, ticks)
            seen[key] = proc["comm"]
    duties = []
    for key in last:
        span_s = last[key][0] - first[key][0]
        if span_s < 3:
            continue
        duties.append((last[key][1] - first[key][1]) * TICK_US
                      / (span_s * 1e6))
    return round(statistics.median(duties), 3) if duties else None


def wake_stats(repeat_dir, window, match):
    """Per-process voluntary-wakeup rate and cpu-per-wake from ctxt samples."""
    series = {}
    for rec in iter_samples(repeat_dir):
        t = hms_us(rec["t"])
        if not in_phase(t, window):
            continue
        for proc in rec["procs"]:
            if not match(proc["comm"]) or proc.get("vctxt") is None:
                continue
            key = (proc["pid"], proc["starttime"])
            entry = series.setdefault(
                key, {"comm": proc["comm"], "t0": t, "v0": proc["vctxt"],
                      "c0": proc["utime"] + proc["stime"]})
            entry.update(t1=t, v1=proc["vctxt"],
                         c1=proc["utime"] + proc["stime"])
    out = []
    for entry in series.values():
        span_s = entry["t1"] - entry["t0"]  # window times are seconds-of-day
        wakes = entry["v1"] - entry["v0"]
        if span_s < 5 or wakes < 5:
            continue
        out.append({"comm": entry["comm"], "wakes": wakes,
                    "gap_us": span_s * 1e6 / wakes,
                    "work_us": (entry["c1"] - entry["c0"]) * TICK_US / wakes})
    return out


# ---- per-repeat extraction --------------------------------------------------

def analyze_cli_repeat(repeat_dir):
    phases = load_phases(repeat_dir)
    out = {"phase_rc": {k: v[3] for k, v in phases.items()},
           "phase_wall_us": {k: v[2] for k, v in phases.items()}}

    for build_phase, prefix in (("kernel-build-j8", "compiler"),
                                ("kernel-build-cold", "compiler_cold")):
        build = good(phases, build_phase)
        if build is None:
            continue
        lifetimes = exits_in_window(repeat_dir, build, COMPILER_NAMES)
        out[f"{prefix}_lifetime"] = lognormal_fit(lifetimes)
        out[f"{prefix}_children"] = len(lifetimes)
        cpu_us, peak = phase_cpu(repeat_dir, build,
                                 lambda c: c in COMPILER_NAMES)
        if lifetimes:
            out[f"{prefix}_cpu_mean_us"] = round(cpu_us / len(lifetimes))
            out[f"{prefix}_life_mean_us"] = round(
                sum(lifetimes) / len(lifetimes))
        out[f"{prefix}_peak_concurrent"] = peak
        if prefix == "compiler":
            make_cpu, _ = phase_cpu(repeat_dir, build, lambda c: c == "make")
            forks = count_execs(repeat_dir, build, COMPILER_NAMES)
            out["make_dispatch_us"] = round(make_cpu / forks) if forks else None
            out["fork_rate_hz"] = round(forks / (build[2] / 1e6), 1)

    for phase_name, comms, key in (
            ("rsync-copy", {"rsync"}, "rsync"),
            ("untar", {"tar", "xz"}, "untar"),
            ("clamscan", {"clamscan"}, "clamscan"),
            ("updatedb", {"updatedb.plocate", "updatedb"}, "updatedb"),
            ("network-bulk", {"wget"}, "wget"),
            ("tar-read-cold", {"tar"}, "tar_cold"),
            ("rsync-copy-cold", {"rsync"}, "rsync_cold"),
            ("clamscan-cold", {"clamscan"}, "clamscan_cold"),
            ("updatedb-cold", {"updatedb.plocate", "updatedb"},
             "updatedb_cold")):
        window = good(phases, phase_name)
        if window is None:
            out[f"{key}_duty"] = out[f"{key}_proc_duty"] = None
            continue
        cpu_us, _ = phase_cpu(repeat_dir, window, lambda c, s=comms: c in s)
        out[f"{key}_duty"] = round(cpu_us / window[2], 3)
        out[f"{key}_proc_duty"] = per_proc_duty(repeat_dir, window,
                                                lambda c, s=comms: c in s)

    tracker = good(phases, "tracker-daemon")
    out["tracker_wakes"] = wake_stats(
        repeat_dir, tracker,
        lambda c: c.startswith(("tracker", "localsearch"))) \
        if tracker else []
    return out


def analyze_gui_repeat(repeat_dir):
    phases = load_phases(repeat_dir)
    out = {"phase_rc": {k: v[3] for k, v in phases.items()}}

    chromium = phases["chromium-10-tabs"]
    is_chrome = lambda c: c.startswith(("chrom", "chrome"))
    _, peak = phase_cpu(repeat_dir, chromium, is_chrome)
    out["chromium_peak_procs"] = peak
    out["chromium_wakes"] = wake_stats(repeat_dir, chromium, is_chrome)

    element = phases["element-idle"]
    is_element = lambda c: c.lower().startswith("element")
    out["element_wakes"] = wake_stats(repeat_dir, element, is_element)
    out["daemon_wakes"] = wake_stats(repeat_dir, element,
                                     lambda c: c in DAEMON_NAMES)
    return out


def spread(values):
    clean = [v for v in values if v is not None]
    if not clean:
        return None
    return {"n_repeats": len(clean), "median": statistics.median(clean),
            "min": min(clean), "max": max(clean)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir")
    parser.add_argument("--json")
    args = parser.parse_args()
    base = pathlib.Path(args.dir)

    cli = {d.name: analyze_cli_repeat(d)
           for d in sorted((base / "cli").iterdir()) if d.is_dir()}
    gui = {d.name: analyze_gui_repeat(d)
           for d in sorted((base / "gui").iterdir()) if d.is_dir()}

    summary = {"cli_repeats": cli, "gui_repeats": gui, "across_repeats": {}}
    across = summary["across_repeats"]
    for prefix in ("compiler", "compiler_cold"):
        across[f"{prefix}_lifetime_median_us"] = spread(
            [r[f"{prefix}_lifetime"]["median_us"] for r in cli.values()
             if r.get(f"{prefix}_lifetime")])
        across[f"{prefix}_lifetime_sigma_log"] = spread(
            [r[f"{prefix}_lifetime"]["sigma_log"] for r in cli.values()
             if r.get(f"{prefix}_lifetime")])
        for key in ("children", "cpu_mean_us", "life_mean_us"):
            across[f"{prefix}_{key}"] = spread(
                [r.get(f"{prefix}_{key}") for r in cli.values()])
    across["make_dispatch_us"] = spread(
        [r.get("make_dispatch_us") for r in cli.values()])
    across["fork_rate_hz"] = spread(
        [r.get("fork_rate_hz") for r in cli.values()])
    for key in ("rsync", "untar", "clamscan", "updatedb", "wget", "tar_cold",
                "rsync_cold", "clamscan_cold", "updatedb_cold"):
        across[f"{key}_duty"] = spread(
            [r.get(f"{key}_duty") for r in cli.values()])
        across[f"{key}_proc_duty"] = spread(
            [r.get(f"{key}_proc_duty") for r in cli.values()])

    tracker_gaps = [w["gap_us"] for r in cli.values()
                    for w in r.get("tracker_wakes", [])]
    tracker_work = [w["work_us"] for r in cli.values()
                    for w in r.get("tracker_wakes", [])]
    across["tracker"] = {
        "procs": sum(len(r.get("tracker_wakes", [])) for r in cli.values()),
        "gap": lognormal_fit(tracker_gaps), "work": lognormal_fit(tracker_work)}
    across["chromium_peak_procs"] = spread(
        [r["chromium_peak_procs"] for r in gui.values()])

    def wake_summary(key):
        gaps, works = [], []
        for repeat in gui.values():
            gaps += [w["gap_us"] for w in repeat[key]]
            works += [w["work_us"] for w in repeat[key]]
        return {"procs": sum(len(r[key]) for r in gui.values()),
                "gap": lognormal_fit(gaps), "work": lognormal_fit(works)}

    across["element"] = wake_summary("element_wakes")
    across["chromium"] = wake_summary("chromium_wakes")
    across["daemons"] = wake_summary("daemon_wakes")

    text = json.dumps(summary["across_repeats"], indent=2)
    print(text)
    if args.json:
        pathlib.Path(args.json).write_text(json.dumps(summary, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
