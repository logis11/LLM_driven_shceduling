#!/usr/bin/env python3
"""Generate the measured archetype entries (9.5 fold-in) from pool.py output.

fold_in.py <results-dir> <out.yaml> [--tag interactive=meas-ci:interactive:<campaign> --tag playback=meas-ci:playback:<campaign> --tag <app>=meas-ci:interactive:<campaign>]
(<campaign>: the launch date, D27; a run number for a one-run campaign from before it)

One entry per campaign run, per the 9.5 changelog: D2/D11 ids, D9 shape,
D13 per-input run (window rule), D16 timer components with a pooled
residual, D17 quantile tables in µs, D18 replayed stimulus, D14 tree scope,
D15 rasteriser exclusion (applied upstream in analyze.py). The output is a
YAML fragment to splice into dataset/archetypes.yaml under `archetypes:`.
"""

import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pool import build_census  # noqa: E402  — D69: one definition of the build census
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from distribution import quantile_table, yaml_table  # noqa: E402

RUN_TAG = {"interactive": "meas-ci:interactive:3", "playback": "meas-ci:playback:3"}  # the D3 campaign; --tag overrides

# the observed setup per run — `{version}` is filled from the run's recorded application version (report.json)

ARCHETYPES = {
    # id: (run, program observed, kind, stimulus stream, stimulus tag, bound names by approximation)
    "office-writer": ("soffice", "{version} (Ubuntu 24.04 apt), a generated document of about 76 pages (100 sections of five 100-word paragraphs, ten 1024×768 pictures; design — no source states a length, S7) with the stream typing at its end", "input",
                      "swell-word-c1", "swell-icmi14:word-c1", []),
    "code-editor": ("code", "Visual Studio Code {version} (vendor .deb), the TypeScript project sindresorhus/got at commit 64f21e2a (tag v16.0.0, dependencies installed; design) open on source/index.ts with the built-in TypeScript language server running", "input",
                    "swell-word-c1", "swell-icmi14:word-c1", []),
    # 9.7 D3 and D31, D36: mail-client is re-observed whole as thunderbird-send — the same application with a send
    # operation, its values replacing the compose-only entry's
    "mail-client": ("thunderbird-send", "{version} (vendor .deb), a compose window over a local account whose SMTP server is a loopback peer (aiosmtpd, no authentication or TLS, on the harness CPUs); operation send: a reply with a short body and one Word document attached — the Writer setup state's document (100 sections of five 100-word paragraphs, ten 1024×768 pictures; design after CpsMark+ §CA's attachment kinds, no source stating a size) saved as .docx, 41,555,063 B on the runner and 56,946,735 B as the peer receives it, the same size in every repeat and not the same bytes (D49); completion when the copy into the Sent folder lands, the peer's own stamp recorded beside it", "input",
                    "swell-outlook-c23", "swell-icmi14:outlook-c23", []),
    "web-browser": ("chrome", "{version} (preinstalled), a local page with a text area and 400 paragraphs; the browser process, GPU and utility processes — renderer processes excluded (renderer-hidden, renderer-visible); operation page-load: the scripted feed page feed.html (300 posts, thirty 1600×1200 pictures, a 200 000-record sort; design after PCMark 10 pp. 52–53 and CpsMark+ §4.3.3) from a local server, completion by the page's title after first paint", "input",
                    "swell-ie-c1", "swell-icmi14:ie-c1", []),
    "image-editor": ("gimp", "{version} (apt), a 4952×3288 image open (PCMark 10 Photo Editing's interactive image size, Technical Guide p. 71; synthetic content, imported as 16-bit; design); driven by a scripted pointer loop (drag, click, wheel; design); operation unsharp-mask: plug-in-unsharp-mask std-dev 4.0, amount 0.32, threshold 8 (PCMark 10's batch unsharp parameters mapped onto GIMP's PDB, p. 74; design) through the Script-Fu server, completion by its reply", "cadence", None, None, []),
    "video-editor": ("kdenlive", "Kdenlive 23.08.5 (Ubuntu 24.04 apt), a project with one 20 s 1920×1080 30 fps H.264 clip (PCMark 10 Video Editing's 1080p H.264, p. 76; synthetic content, design) on V1 with an avfilter.unsharp effect at PCMark 10's sharpening parameters (p. 76); driven by a scripted pointer loop that scrubs the clip monitor (design); llvmpipe software-rasteriser threads excluded (D15); operation preview-render: the whole-clip timeline preview rendered by Kdenlive's external kdenlive_render process (part of the tree), completion when it exits", "cadence", None, None, []),
    "video-player": ("mpv-video", "{version}, --vo=x11 --ao=null, a 1280×720 30 fps H.264 file with AAC audio, looped", "play", None, None,
                     ["zoom (video) → video-call instead (D12)", "gamescope: compositor, not a decoder (9.4's record)"]),
    "audio-player": ("mpv-audio", "{version}, --no-video --ao=null, the same file's AAC audio, looped", "play", None, None,
                     ["spotify: streaming client with network fetch, decode and a Chromium-based interface (S2-18: no documentation)"]),
    "video-call": ("webrtc", "{version}, a loopback WebRTC call in one page with a synthetic 1280×720 30 fps camera and microphone (--use-fake-device-for-media-stream); encode and decode at ~20 fps", "play", None, None,
                   ["zoom voice and video: a proprietary client with capture, encode, network and playback threads (S2-17; S6: whole-client CPU only)"]),
}

VENUE_BOUND = {
    'web-browser': "Venue bound (D24, S8): without display vsync Chromium drives its compositor from a default 60 Hz timer (Chromium docs, life of a frame; BeginFrameArgs::DefaultInterval), so the compositor cadence has a 60 Hz display's period but not its phase; rasterisation and compositing run on CPU threads under --disable-gpu, so those threads' run lengths overcount what a GPU desktop would show, by an amount no source states.",
    'video-call': "Venue bound (D24, S8): without display vsync Chromium drives its compositor from a default 60 Hz timer (Chromium docs, life of a frame; BeginFrameArgs::DefaultInterval), so the compositor cadence has a 60 Hz display's period but not its phase; rasterisation and compositing run on CPU threads under --disable-gpu, so those threads' run lengths overcount what a GPU desktop would show, by an amount no source states.",
    'code-editor': "Venue bound (D24, S8): without display vsync Chromium drives its compositor from a default 60 Hz timer (Chromium docs, life of a frame; BeginFrameArgs::DefaultInterval), so the compositor cadence has a 60 Hz display's period but not its phase; rasterisation and compositing run on CPU threads under --disable-gpu, so those threads' run lengths overcount what a GPU desktop would show, by an amount no source states.",
    'video-editor': "Venue bound (D24, S8): Qt Quick's render loop paces on a blocking buffer swap; the runner's software rasteriser does not block, so the rendering path's wake rate overcounts a vsync-throttled display (Qt 5.15 qsgthreadedrenderloop.cpp); the excluded llvmpipe threads carried 93 % of the driven phase's CPU (D15).",
    'video-player': "Venue bound (D24, S8): mpv's default --video-sync=audio paces frames on the audio clock, not the display (mpv 0.37 manual), so the missing refresh does not change its cadence; the x11 output copies frames on the CPU, work a GPU output would move.",
}

# D69: the build is pinned where the vendor serves a version of its own, so an archetype describes that build and not
# whatever the repository serves later; where the build moved under the campaign, what it leaves out is stated.
BUILD_BOUND = {
    'code-editor': "Build bound (D69): the campaign is pinned to the build named above, which ships no assistant runtime. "
                   "VS Code 1.139.0, released during the campaign, runs a copilot-runtime process that woke 49.7 times a "
                   "second in the idle phase against the 115 a second of this build's whole tree — a different workload, "
                   "and whether a code editor should describe an assistant-bearing one is the archetype's own question, "
                   "not this campaign's.",
}


APPROX_BY = {"video-player": ["gamescope"], "audio-player": ["spotify"], "video-call": ["zoom"]}

# D75: where each playback archetype's medium cycle starts, as the scope states it (the rule itself: pool.py CYCLES)
CYCLE_START = {
    "video-player": ("frame", "each frame copy — a run of 1 ms or more by the video output thread `vo`, 30.0 a second"),
    "audio-player": ("audio", "the first wake of the audio output thread `ao` after 5 ms of silence"),
    "video-call": ("audio-frame", "each wake of the audio worker thread `utility/AudioWorkerThre`, once per 10 ms audio frame"),
}
MASSES = (0.01, 0.04, 0.05, 0.15, 0.25, 0.25, 0.15, 0.05, 0.04, 0.009, 0.001)   # the eleven intervals of a D17 table


def table_mean(table):
    """A pooled table's mean: the interval means weighted by their masses (9.5 D71), the sample's own mean."""
    return sum(m * x for m, x in zip(MASSES, table["means"]))


def share_above(table, x):
    """The share of a pooled table's samples above x, read off its knots (minimum, ten quantiles, maximum) with straight
    lines between them — how many of a periodic job's cycles carry more work than the period itself (D75)."""
    knots = [table["min"], *table["p"], table["max"]]
    probs = [0.0, 0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99, 0.999, 1.0]
    if x >= knots[-1]:
        return 0.0
    for (a, pa), (b, pb) in zip(zip(knots, probs), zip(knots[1:], probs[1:])):
        if a <= x < b:
            return 1.0 - (pa + (pb - pa) * (x - a) / (b - a))
    return 1.0


# The stability rule as the scope states it (the campaign workflow; D26, D30): the rule over the repeats obtained, and
# each value it was not held to — at the recording's window limit (D32) or carried under D57 — with its half-width.
LABEL = {"wakes/s": "wake rate", "gap mean (ms)": "gap mean", "run mean (ms)": "run mean"}
# where each entry's window limit is decided: D32 the rule, D46 the send's operation phase, D68 chrome's and code's limits
WINDOW_LAW = {"code-editor": "D32, D68", "web-browser": "D32, D68", "mail-client": "D32, D46"}
# D57's second finding: a between-sessions component's spread within one run, read on the D52 probe
WITHIN = {("code-editor", "utility/libuv-worker"): "its schedule-in rate ±8.7 % (7.81–9.31 a second over 900 s "
                                                   "windows slid along the D52 probe)"}


def value_name(key):
    """(name, unit) of a stability-block value as the scope writes it."""
    if key.startswith("input_run mean, "):
        return f"the per-input run mean under {key[len('input_run mean, '):-len(' (ms)')]}", "ms"
    if key == "operation duration mean (ms)":
        return "the operation's duration mean", "ms"
    phase, rest = key.split(" ", 1)
    label = next(lb for lb in LABEL if rest.endswith(" " + lb))
    whose = "the operation's " if phase == "op" else ""
    return f"{whose}`{rest[:-len(label) - 1]}` {LABEL[label]}", ("wakes/s" if label == "wakes/s" else "ms")


def held(c, unit):
    return f"{c['mean']:.4g} {unit} ±{c['half_width'] * 100:.2f} %"


def stability_scope(aid, d):
    st = d["stability"]
    q = st["quantities"]
    text = (f"Stability rule (D26, D30): every value on the list holds within {st['tolerance'] * 100:g} % or "
            f"{st['abs_floor_ms'] * 1000:g} µs over the {len(d['repeats'])} repeats obtained")
    limited = {k: c for k, c in q.items() if c.get("limited")}
    session = {k: c for k, c in q.items() if c.get("session_spread") and c.get("carried")}
    if not limited and not session:
        return text + ". "
    text += ", except these, stated with their half-widths. "
    if limited:
        op = (d["phases"].get("op") or {}).get("operation")
        what = "the per-input means" + (f" and the {op['name']} operation's values"
                                        if op and any(k.startswith(("op ", "operation ")) for k in limited) else "")
        out = sorted((kc for kc in limited.items() if not kc[1]["passes"]), key=lambda kc: -kc[1]["half_width"])
        ins = [c for c in limited.values() if c["passes"]]
        text += (f"Window limit ({WINDOW_LAW[aid]}): {what} come from the repeats that replay a window of the "
                 f"recording, {max(c['k'] for c in limited.values())} repeats, every window of it that holds input")
        if out:
            text += "; outside the rule: " + "; ".join(
                f"{value_name(k)[0]} {held(c, value_name(k)[1])} (the rule needs {c['needed']} repeats)" for k, c in out)
        if len(ins) == 1:
            k = next(k for k, c in limited.items() if c["passes"])
            text += f"; {value_name(k)[0]} {held(limited[k], value_name(k)[1])} holds within it"
        elif ins:
            text += (f"; {'the other' if out else 'all'} {len(ins)} hold within it, the widest "
                     f"±{max(c['half_width'] for c in ins) * 100:.2f} %")
        text += ". "
    if session:
        comps = {}
        for k, c in session.items():
            phase, rest = k.split(" ", 1)
            label = next(lb for lb in LABEL if rest.endswith(" " + lb))
            comps.setdefault((phase, rest[:-len(label) - 1]), {})[label] = c
        parts = []
        for (phase, comm), vals in comps.items():
            t = d["phases"][phase]["threads"][comm]
            per = {"wakes/s": t["wakes_per_s"], "gap mean (ms)": t["gap_ms"]["repeat_mean"],
                   "run mean (ms)": t["run_ms"]["repeat_mean"]}
            texts = []
            for label in LABEL:
                if label in vals:
                    unit = "wakes/s" if label == "wakes/s" else "ms"
                    texts.append(f"{LABEL[label]} {held(vals[label], unit)} "
                                 f"({min(per[label]):.4g}–{max(per[label]):.4g} {unit})")
            w = t["wakes_per_s"]
            across = (max(w) - min(w)) / 2 / statistics.fmean(w) * 100
            share = statistics.fmean(w) / statistics.fmean(d["phases"][phase]["wakes_per_s"]) * 100
            parts.append(f"`{comm}` " + ", ".join(texts) + f"; within one run {WITHIN[(aid, comm)]}, across the "
                         f"repeats its wake rate ±{across:.1f} %; it holds {share:.1f} % of the {phase} phase's wakes")
        many = len(comps) > 1
        text += (f"{'Components' if many else 'A component'} whose rate varies between sessions, "
                 f"{'their' if many else 'its'} three values carried together (D57): " + "; ".join(parts) + ". ")
    return text


def rng(vals, nd=4):
    return f"{min(vals):.{nd}f}–{max(vals):.{nd}f}"


def dist(summary, tag, sampling="per-iteration"):
    """A pooled summary's table (ms) as the library's `quantiles` param: ten quantiles, extremes, interval means."""
    return yaml_table(summary["table"], tag, sampling=sampling)


def component_lines(comp_name, comp, tag, indent, extra=None):
    lines = [f"{indent}- comm: {json.dumps(comp_name)}"]
    if extra:
        lines += [f"{indent}  {k}: {v}" for k, v in extra]
    lines.append(f"{indent}  threads: {min(comp['threads'])}" if min(comp["threads"]) == max(comp["threads"]) else f"{indent}  threads: [{min(comp['threads'])}, {max(comp['threads'])}]")
    lines.append(f"{indent}  wakes_per_s: {sum(comp['wakes_per_s']) / len(comp['wakes_per_s']):.5g}")
    lines.append(f"{indent}  gap: {dist(comp['gap_ms'], tag)}")
    lines.append(f"{indent}  run: {dist(comp['run_ms'], tag)}")
    return lines


def components_block(ph, tag, key, indent="      "):
    sel = ph["components"]
    if not sel["selected"] and not sel["residual"]:
        return [f"{indent}# {key}: none — no wake in the {'idle' if key == 'components' else 'driven'} phase (GIMP idles silently)"]
    lines = [f"{indent}{key}:"]
    for comm in sel["selected"]:
        c = ph["threads"][comm]
        if c["gap_ms"]["table"] is None:
            continue
        lines += component_lines(comm, c, tag, indent + "  ")
    if sel["residual"] and sel["residual"]["gap_ms"]["table"]:
        r = sel["residual"]
        lines += component_lines("residual", r, tag, indent + "  ",
                                 extra=[("comms", "[" + ", ".join(json.dumps(x) for x in r["comms"]) + "]")])
    lines.append(f"{indent}  # {len(sel['selected'])} comms cover {(sel['covered_share'] or 0) * 100:.1f} % of {sel['total_wakes_per_s']:.1f} wakes/s (D16, target {sel['coverage'] * 100:.0f} %); the rest pooled as `residual`")
    return lines


def heavy_events_block(ph, tag, indent="      "):
    """D64: a rare run the component's wakes leave out — chrome's MemoryInfra pass, 50.9–60.0 ms against its regular
    runs of at most 11.5 ms — carried as its own stated event. Only what was measured: the run quantiles, the count and
    the span they were counted over, and the rate that follows. No gap distribution, because none was measured — most
    repeats saw the event once or not at all, so no repeat holds an interval between two of them."""
    h = ph.get("heavy_event")
    if not h or not h.get("runs_ms"):
        return []
    runs = sorted(h["runs_ms"])
    return [f"{indent}heavy_events:",
            f"{indent}  - comm: {json.dumps(h['comm'])}",
            f"{indent}    run_floor_ms: {h['run_floor_ms']:g}",
            f"{indent}    count: {sum(h['count'])}",
            f"{indent}    span_s: {h['span_s_total']:.1f}",
            f"{indent}    rate_per_s: {h['rate_per_s']:g}",
            f"{indent}    run: {yaml_table(quantile_table(runs), tag)}",
            f"{indent}  # D64: {sum(h['count'])} runs of at least {h['run_floor_ms']:g} ms over {h['span_s_total']:.0f} s of idle phase, "
            f"{min(runs):.1f}–{max(runs):.1f} ms; their runs leave the components' wakes, so the residual converges. "
            f"No interval is stated: no repeat holds two of them."]


# D28, D65, D72: the stream's keys only (appdefs KINDS=key), and what each entry's scope says about it
KEYS_ONLY = {
    "office-writer": ("and its clicks, scrolls and drags left out, so the typing stays at the document's end (D28; the archetype "
                      "carries typing, not document navigation); "),
    "web-browser": ("and its clicks, scrolls and drags left out, so every key lands in the page's text box (D65; the archetype "
                    "carries typing into a page field, not browsing's scrolling and clicking — the page-load operation carries "
                    "browsing's heavy work); "),
    "code-editor": ("and its clicks, scrolls and drags left out, so the typing stays at the file's end, the file otherwise as "
                    "committed (D72; the archetype carries typing, not the editor's navigation); the keys are a fixed letter "
                    "cycle (D4: timing only), so the per-key cost is the language server re-checking a file being filled with "
                    "letter runs; "),
}


def entry(aid, spec, d):
    run, observed, kind, stream, stim_tag, approx = spec
    tag = RUN_TAG.get(run) or RUN_TAG[d["family"]]  # --tag <app>=… overrides the family tag for one run (re-run batch)
    observed = observed.replace("{version}", build_census(d.get("version")))   # D69: the census, a mix stated
    out = [f"  {aid}:", "    category_source: meas", "    pattern:", "      program:"]
    if kind == "play":
        out += ["        - loop:                    # one periodic job per medium cycle, its deadline the next cycle's start (D74, D75)",
                "            - TIMER: period", "            - RUN: cycle_run"]
    else:
        out += ["        - loop:                    # merged event stream, explicit at compile time (D9): replayed stimulus in focus windows (D18) + timer components (D16)",
                "            - WAIT: input", "            - RUN: event"]
    out.append("    params:")
    ph_idle = d["phases"].get("idle") or d["phases"].get("play")
    if kind == "input":
        pi = d["phases"]["driven"]["per_input"]
        out.append("      input_run:")
        out.append(f"        {dist(pi['window']['run_ms_minus_idle'], tag)}")
        out.append("      stimulus:")
        kinds = ", kinds: [key]" if aid in KEYS_ONLY else ""   # D28, D65: the events the measurement replayed
        out.append(f"        {{stream: {stream}{kinds}, sampling: per-task, source: \"{stim_tag}\"}}")
    if kind == "play":   # D75: the period is the cycles' mean length, the run each cycle's whole-tree CPU
        cyc = ph_idle["cycle"]
        out.append(f"      period: {{dist: constant, value_us: {round(table_mean(cyc['length_ms']['table']) * 1000)}, "
                   f"sampling: per-task, source: \"{tag}\"}}")
        out.append(f"      cycle_run: {dist(cyc['work_ms'], tag)}")
    else:
        out += components_block(ph_idle, tag, "components")
    out += heavy_events_block(ph_idle, tag)
    if kind == "cadence":
        out += components_block(d["phases"]["driven"], tag, "focus_components")
    if "op" in d["phases"] and d["phases"]["op"].get("operation"):
        # spec decision 8: a named operation with its own components and a measured duration (trigger to completion)
        o = d["phases"]["op"]["operation"]
        out.append("      operations:")
        out.append(f"        {o['name']}:")
        out.append(f"          duration: {dist(o['duration_ms'], tag)}")
        out += components_block(d["phases"]["op"], tag, "components", indent="          ")
    out += ["    lifetime: segment-bound", "    binding_params: []", "    scalable: []", "    validation_stats:",
            "      referee: meas-ci"]
    reps = d["repeats"]
    phase_names = list(d["phases"])
    run_line = f"{tag.split(':', 1)[1]}, repeats {reps}"
    runs = sorted(set(x for x in (d.get("run_id") or {}).values() if x))
    if runs:  # D27: a campaign spans runs; each repeat's run is in the pooled record
        run_line += f", runs {', '.join(runs)}"
    if run == "thunderbird" and tag == "meas-ci:interactive:3":
        run_line += " (repeats 2 and 3 from interactive:4 after a replay-driver fix)"
    out.append(f"      run: \"{run_line}\"")
    stats = []
    for pn in phase_names:
        ph = d["phases"][pn]
        stats.append(f"{pn} wakes/s {rng(ph['wakes_per_s'], 1)}")
        stats.append(f"{pn} cpu-share {rng(ph['cpu_share'])}")
    if kind == "input":
        pi = d["phases"]["driven"]["per_input"]
        stats.append(f"input_run p50 ms per repeat {pi['window']['run_ms_minus_idle']['repeat_p50']}")
    if kind == "play":   # D75: the cycle's length and work, each repeat's mean
        cyc = ph_idle["cycle"]
        stats.append(f"cycle length ms per repeat {rng(cyc['length_ms']['repeat_mean'], 3)}")
        stats.append(f"cycle run ms per repeat {rng(cyc['work_ms']['repeat_mean'], 4)}")
    out.append("      stats: [" + ", ".join(json.dumps(x) for x in stats) + "]")
    out.append("      scope: >-")
    # D26: the machine and kernel are the pooled repeats' own records (spec.json), one CPU model per observation
    models = sorted(set((d.get("cpu_model") or {}).values())) or ["CPU model not recorded"]
    kernels = sorted(set(k for k in (d.get("kernel") or {}).values() if k)) or ["kernel not recorded"]
    scope = (f"One observation (phase decision 2; D3, D10, D26): {observed}, on a GitHub-hosted ubuntu-24.04 runner "
             f"(4 vCPU {' / '.join(models)}, kernel {' / '.join(kernels)}) under Xvfb 1280×800 — no display refresh, no GPU, "
             f"no sound device; perf sched record on CLOCK_MONOTONIC over whole phases. ")
    if kind == "input":
        if aid in KEYS_ONLY:
            scope += (f"Stimulus: SWELL-KW stream {stream}, its keystrokes replayed by xdotool at their recorded times (error p99 1.24 ms) "
                      + KEYS_ONLY[aid])
        else:
            scope += (f"Stimulus: SWELL-KW stream {stream} replayed per event by xdotool at recorded gaps (error p99 1.24 ms), "
                      f"keys and pointer events together, pointer positions scaled into the content area (D5, D12); ")
        scope += (f"the recordings' timestamps are quantised at 15.6 ms. Per-input run is the window rule (D13): all run time of the "
                  f"process tree until the next input minus the idle rate. ")
        alt = d["phases"].get("driven-alt", {}).get("per_input")
        if alt:  # spec decision 11: the pre-registered sensitivity result, one sentence, no value changed
            a = pi["window"]["run_ms_minus_idle"]["p50"]; b = alt["window"]["run_ms_minus_idle"]["p50"]
            change = f" ({(b - a) / a * 100:+.0f} %)" if a else " (the SWELL-KW median is at the zero bound, D13)"
            scope += (f"Stimulus sensitivity (pre-registered, method §3): under a 136M Keystrokes transcription stream (dhakal-chi18) "
                      f"the per-input run p50 is {b:.2f} ms against {a:.2f} ms under SWELL-KW{change}; "
                      f"the archetype carries SWELL-KW. ")
    elif kind == "cadence":
        scope += "Stimulus: a scripted pointer loop (design); no per-input run exists, the driven cadence is carried as focus_components. "
    else:   # D74, D75: one periodic job per medium cycle, read off the trace
        cyc = ph_idle["cycle"]
        what, start = CYCLE_START[aid]
        period_ms = table_mean(cyc['length_ms']['table'])
        scope += (f"No stimulus. One periodic job per {what} cycle (D74, D75): a cycle starts at {start}; the period is the "
                  f"mean interval between starts, {period_ms:.3f} ms over {sum(cyc['cycles']):,} cycles; "
                  f"each job's run is the process tree's whole CPU from one start to the next, drawn per cycle from its "
                  f"measured table, and its deadline is the next cycle's start (period-implicit, liu-jacm73 (A2)). The "
                  f"deadline is the cycle's, not the output device's: an audio server buffers ahead of the device (PulseAudio "
                  f"up to 2 s by default, 9.5 search record S2), so a late cycle is not by itself an audible gap or a dropped frame. ")
        over = share_above(cyc["work_ms"]["table"], period_ms)
        if over >= 0.001:   # measured load, not a compile effect: these jobs miss with the task alone on the CPU
            scope += (f"In about {over * 100:.1f} % of cycles the tree's own work exceeds the period"
                      + (" — the call's saturation episodes, one CPU busy for about 30 s every 240 s (D54) —" if aid == "video-call" else "")
                      + " so those jobs miss even with the task alone on the CPU. ")
        if aid == "video-call":
            scope += ("The call's video path — compositing at about 16.7 ms and the 30 fps frames — has no job of its own; its "
                      "CPU runs inside the audio frames' cycles. ")
    scope += stability_scope(aid, d)
    scope += "Values are this software on this machine, not desktop truth (D10)."
    if aid in BUILD_BOUND:   # D69: what the pinned or recorded build leaves out of the archetype
        scope += " " + BUILD_BOUND[aid]
    if aid in VENUE_BOUND:  # D24: the direction of the venue's error, from the toolkits' own sources (search log S8)
        scope += " " + VENUE_BOUND[aid]
    out += ["        " + scope]
    out.append("    modeling_notes: >-")
    notes = (f"Per-application archetype (D2): one task carries the whole process tree merged (D14)")
    if run == "chrome":
        notes += ", renderer processes excluded as renderer-hidden's and renderer-visible's (bound separately)"
    notes += (". A component is its process's role and the thread comm together (D67), so one comm naming a thread of "
              "several processes — chrome's Chrome_ChildIOT runs in the GPU process and in each utility process — is "
              "several components; a single-process tree's components carry the comm alone")
    if kind == "play":
        notes += (". The threads' own wakes are not carried one by one: the tree's CPU is summed per medium cycle into one run "
                  "per job (D75), so the compiled task wakes once per cycle; the per-thread tables stay in the pooled record.")
    else:
        notes += (". Timer components are per thread comm (D16), each sampled from its measured gap and run quantiles (D17) over the "
                  "task's lifetime and merged, with the input wakes, into one explicit event stream at compile time (D9); the pooled "
                  "residual stands for the comms below the coverage cut. Each timer wake is a WAIT on the task's timer channel, "
                  "woken at its sampled absolute time, with no deadline (D74).")
    if kind == "input":
        notes += (f" Input wakes: a contiguous slice of {stream} equal to each focus window, at a seed-drawn offset (D18); "
                  "the slice preserves the recording's burst-and-pause structure.")
    if kind == "cadence":
        notes += " Inside focus windows the driven-phase components replace the idle ones; no input wake is emitted (the stimulus was scripted)."
    if "op" in d["phases"] and d["phases"]["op"].get("operation"):
        o = d["phases"]["op"]["operation"]
        notes += (f" Operation `{o['name']}` (spec decisions 8–10): the timeline names it and a start time; the compiler draws its length "
                  f"from the measured duration table (trigger to completion) and swaps in the operation's components for that span, "
                  f"emitting no input wake; it runs to completion past the focus window.")
    if run == "code":
        notes += " Word streams drive this editor as the nearest recording: no code-editing keystroke dataset with timestamps exists (D4)."
    if run == "thunderbird":
        notes += " Outlook streams exist only in SWELL-KW's interruption conditions c2 and c3 (D12)."
    if approx:
        notes += " Bound by stated approximation, carrying these numbers unchanged (D11, D12): " + "; ".join(approx) + "."
    sporadic = [(pn, ph.get("repeats", d["repeats"]), sp) for pn, ph in d["phases"].items()
                for sp in (ph.get("components") or {}).get("sporadic", [])]
    if sporadic:  # D43: a thread whose gap and run means do not exist in every repeat is reported, not carried
        notes += " Sporadic wakes, not carried as components (D43): " + "; ".join(
            f"`{sp['comm']}`" + (f" ({', '.join(sp['comms'])})" if "comms" in sp else "")
            + f" in the {pn} phase, repeats {sp['repeats']} of {reps}, {sp['wakes_per_s']} wakes/s" for pn, reps, sp in sporadic) + "."
    out += ["      " + notes]
    return "\n".join(out)


def main():
    R, out = sys.argv[1], sys.argv[2]
    rest = sys.argv[3:]
    while rest:  # --tag interactive=meas-ci:interactive:N (repeatable)
        if rest[0] == "--tag" and len(rest) > 1 and "=" in rest[1]:
            fam, tag = rest[1].split("=", 1); RUN_TAG[fam] = tag; rest = rest[2:]
        else:
            raise SystemExit(f"unknown argument {rest[0]!r}")
    tags = ", ".join(sorted(set(RUN_TAG.values())))
    blocks = [f"  # ---- measured per-application archetypes — 9.5 same-machine campaigns ({tags}) ----", ""]
    for aid, spec in ARCHETYPES.items():
        d = json.load(open(os.path.join(R, f"pool-{spec[0]}.json")))["runs"][spec[0]]
        blocks.append(entry(aid, spec, d))
        blocks.append("")
    open(out, "w").write("\n".join(blocks))
    print(f"wrote {out}: {len(ARCHETYPES)} entries")


if __name__ == "__main__":
    main()
