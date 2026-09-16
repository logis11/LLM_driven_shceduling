#!/usr/bin/env python3
"""Generate the measured archetype entries (9.5 fold-in) from pool.py output.

fold_in.py <results-dir> <out.yaml>

One entry per campaign run, per the 9.5 changelog: D2/D11 ids, D9 shape,
D13 per-input run (window rule), D16 timer components with a pooled
residual, D17 quantile tables in µs, D18 replayed stimulus, D14 tree scope,
D15 rasteriser exclusion (applied upstream in analyze.py). The output is a
YAML fragment to splice into dataset/archetypes.yaml under `archetypes:`.
"""

import json
import os
import sys

RUN_TAG = {"interactive": "meas-ci:interactive:3", "playback": "meas-ci:playback:3"}

ARCHETYPES = {
    # id: (run, program observed, kind, stimulus stream, stimulus tag, bound names by approximation)
    "office-writer": ("soffice", "LibreOffice Writer 24.2.7.2 (Ubuntu 24.04 apt), a new document", "input",
                      "swell-word-c1", "swell-icmi14:word-c1", []),
    "code-editor": ("code", "Visual Studio Code 1.137.0 (vendor .deb), a text file open", "input",
                    "swell-word-c1", "swell-icmi14:word-c1", []),
    "mail-client": ("thunderbird", "Mozilla Thunderbird 155.0.1 (snap via apt), a compose window over a pre-seeded local account", "input",
                    "swell-outlook-c23", "swell-icmi14:outlook-c23", []),
    "web-browser": ("chrome", "Google Chrome 152.0.7977.82 (preinstalled), a local page with a text area and 400 paragraphs; the browser process, GPU and utility processes — renderer processes excluded (electron-comms)", "input",
                    "swell-ie-c1", "swell-icmi14:ie-c1", []),
    "image-editor": ("gimp", "GIMP 2.10.36 (apt), an 800×600 image open; driven by a scripted pointer loop (drag, click, wheel; design)", "cadence", None, None, []),
    "video-editor": ("kdenlive", "Kdenlive (Ubuntu 24.04 apt), a new project; driven by a scripted pointer loop that scrubs the clip monitor (design); llvmpipe software-rasteriser threads excluded (D15)", "cadence", None, None, []),
    "video-player": ("mpv-video", "mpv 0.37.0, --vo=x11 --ao=null, a 1280×720 30 fps H.264 file with AAC audio, looped", "play", None, None,
                     ["zoom (video) → video-call instead (D12)", "gamescope: compositor, not a decoder (9.4's record)"]),
    "audio-player": ("mpv-audio", "mpv 0.37.0, --no-video --ao=null, the same file's AAC audio, looped", "play", None, None,
                     ["spotify: streaming client with network fetch, decode and a Chromium-based interface (S2-18: no documentation)"]),
    "video-call": ("webrtc", "Google Chrome 152.0.7977.82, a loopback WebRTC call in one page with a synthetic 1280×720 30 fps camera and microphone (--use-fake-device-for-media-stream); encode and decode at ~20 fps", "play", None, None,
                   ["zoom voice and video: a proprietary client with capture, encode, network and playback threads (S2-17; S6: whole-client CPU only)"]),
}

VENUE_BOUND = {
    'web-browser': "Venue bound (D24, S8): without display vsync Chromium drives its compositor from a default 60 Hz timer (Chromium docs, life of a frame; BeginFrameArgs::DefaultInterval), so the compositor cadence has a 60 Hz display's period but not its phase; rasterisation and compositing run on CPU threads under --disable-gpu, so those threads' run lengths overcount what a GPU desktop would show, by an amount no source states.",
    'video-call': "Venue bound (D24, S8): without display vsync Chromium drives its compositor from a default 60 Hz timer (Chromium docs, life of a frame; BeginFrameArgs::DefaultInterval), so the compositor cadence has a 60 Hz display's period but not its phase; rasterisation and compositing run on CPU threads under --disable-gpu, so those threads' run lengths overcount what a GPU desktop would show, by an amount no source states.",
    'code-editor': "Venue bound (D24, S8): without display vsync Chromium drives its compositor from a default 60 Hz timer (Chromium docs, life of a frame; BeginFrameArgs::DefaultInterval), so the compositor cadence has a 60 Hz display's period but not its phase; rasterisation and compositing run on CPU threads under --disable-gpu, so those threads' run lengths overcount what a GPU desktop would show, by an amount no source states.",
    'video-editor': "Venue bound (D24, S8): Qt Quick's render loop paces on a blocking buffer swap; the runner's software rasteriser does not block, so the rendering path's wake rate overcounts a vsync-throttled display (Qt 5.15 qsgthreadedrenderloop.cpp); the excluded llvmpipe threads carried 93 % of the driven phase's CPU (D15).",
    'video-player': "Venue bound (D24, S8): mpv's default --video-sync=audio paces frames on the audio clock, not the display (mpv 0.37 manual), so the missing refresh does not change its cadence; the x11 output copies frames on the CPU, work a GPU output would move.",
}

APPROX_BY = {"video-player": ["gamescope"], "audio-player": ["spotify"], "video-call": ["zoom"]}


def us(ms_list):
    return [int(round(v * 1000)) for v in ms_list]


def rng(vals, nd=4):
    return f"{min(vals):.{nd}f}–{max(vals):.{nd}f}"


def dist(q_ms, tag, sampling="per-iteration"):
    return "{dist: quantiles, p: [" + ", ".join(str(v) for v in us(q_ms)) + f"], sampling: {sampling}, source: \"{tag}\"}}"


def component_lines(comp_name, comp, tag, indent, extra=None):
    lines = [f"{indent}- comm: {json.dumps(comp_name)}"]
    if extra:
        lines += [f"{indent}  {k}: {v}" for k, v in extra]
    lines.append(f"{indent}  threads: {min(comp['threads'])}" if min(comp["threads"]) == max(comp["threads"]) else f"{indent}  threads: [{min(comp['threads'])}, {max(comp['threads'])}]")
    lines.append(f"{indent}  wakes_per_s: {sum(comp['wakes_per_s']) / len(comp['wakes_per_s']):.3f}")
    lines.append(f"{indent}  gap: {dist(comp['gap_ms']['q'], tag)}")
    lines.append(f"{indent}  run: {dist(comp['run_ms']['q'], tag)}")
    return lines


def components_block(ph, tag, key, indent="      "):
    sel = ph["components"]
    if not sel["selected"] and not sel["residual"]:
        return [f"{indent}# {key}: none — no wake in the {'idle' if key == 'components' else 'driven'} phase (GIMP idles silently)"]
    lines = [f"{indent}{key}:"]
    for comm in sel["selected"]:
        c = ph["threads"][comm]
        if c["gap_ms"]["q"] is None:
            continue
        lines += component_lines(comm, c, tag, indent + "  ")
    if sel["residual"] and sel["residual"]["gap_ms"]["q"]:
        r = sel["residual"]
        lines += component_lines("residual", r, tag, indent + "  ",
                                 extra=[("comms", "[" + ", ".join(json.dumps(x) for x in r["comms"]) + "]")])
    lines.append(f"{indent}  # {len(sel['selected'])} comms cover {(sel['covered_share'] or 0) * 100:.1f} % of {sel['total_wakes_per_s']:.1f} wakes/s (D16, target {sel['coverage'] * 100:.0f} %); the rest pooled as `residual`")
    return lines


def entry(aid, spec, d):
    run, observed, kind, stream, stim_tag, approx = spec
    tag = RUN_TAG[d["family"]]
    out = [f"  {aid}:", "    category_source: meas", "    pattern:", "      program:"]
    if kind == "play":
        out += ["        - loop:                    # measured timer components merged at compile time (D9, D16)",
                "            - TIMER: tick", "            - RUN: event"]
    else:
        out += ["        - loop:                    # merged event stream, explicit at compile time (D9): replayed stimulus in focus windows (D18) + timer components (D16)",
                "            - WAIT: input", "            - RUN: event"]
    out.append("    params:")
    ph_idle = d["phases"].get("idle") or d["phases"].get("play")
    if kind == "input":
        pi = d["phases"]["driven"]["per_input"]
        out.append("      input_run:")
        out.append(f"        {dist(pi['window']['run_ms_minus_idle']['q'], tag)}")
        out.append("      stimulus:")
        out.append(f"        {{stream: {stream}, sampling: per-task, source: \"{stim_tag}\"}}")
    out += components_block(ph_idle, tag, "components")
    if kind == "cadence":
        out += components_block(d["phases"]["driven"], tag, "focus_components")
    if "op" in d["phases"] and d["phases"]["op"].get("operation"):
        # spec decision 8: a named operation with its own components and a measured duration (trigger to completion)
        o = d["phases"]["op"]["operation"]
        out.append("      operations:")
        out.append(f"        {o['name']}:")
        out.append(f"          duration: {dist(o['duration_ms']['q'], tag)}")
        out += components_block(d["phases"]["op"], tag, "components", indent="          ")
    out += ["    lifetime: segment-bound", "    binding_params: []", "    scalable: []", "    validation_stats:",
            "      referee: meas-ci"]
    reps = d["repeats"]
    phase_names = list(d["phases"])
    run_line = f"{tag.split(':', 1)[1]}, repeats {reps}"
    if run == "thunderbird":
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
    out.append("      stats: [" + ", ".join(json.dumps(x) for x in stats) + "]")
    out.append("      scope: >-")
    scope = (f"One observation (phase decision 2; D3, D10): {observed}, on a GitHub-hosted ubuntu-24.04 runner "
             f"(4 vCPU AMD EPYC 7763, kernel 6.17.0-1022-azure) under Xvfb 1280×800 — no display refresh, no GPU, "
             f"no sound device; perf sched record on CLOCK_MONOTONIC over whole phases. ")
    if kind == "input":
        scope += (f"Stimulus: SWELL-KW stream {stream} replayed per event by xdotool at recorded gaps (error p99 1.24 ms), "
                  f"keys and pointer events together, pointer positions scaled into the content area (D5, D12); "
                  f"the recordings' timestamps are quantised at 15.6 ms. Per-input run is the window rule (D13): all run time of the "
                  f"process tree until the next input minus the idle rate. ")
        alt = d["phases"].get("driven-alt", {}).get("per_input")
        if alt:  # spec decision 11: the pre-registered sensitivity result, one sentence, no value changed
            a = pi["window"]["run_ms_minus_idle"]["p50"]; b = alt["window"]["run_ms_minus_idle"]["p50"]
            scope += (f"Stimulus sensitivity (pre-registered, method §3): under a 136M Keystrokes transcription stream (dhakal-chi18) "
                      f"the per-input run p50 is {b:.2f} ms against {a:.2f} ms under SWELL-KW ({(b - a) / a * 100:+.0f} %); "
                      f"the archetype carries SWELL-KW. ")
    elif kind == "cadence":
        scope += "Stimulus: a scripted pointer loop (design); no per-input run exists, the driven cadence is carried as focus_components. "
    else:
        scope += "No stimulus; the play phase's thread cadence is the whole behaviour. "
    scope += "Values are this software on this machine, not desktop truth (D10)."
    if aid in VENUE_BOUND:  # D24: the direction of the venue's error, from the toolkits' own sources (search log S8)
        scope += " " + VENUE_BOUND[aid]
    out += ["        " + scope]
    out.append("    modeling_notes: >-")
    notes = (f"Per-application archetype (D2): one task carries the whole process tree merged (D14)")
    if run == "chrome":
        notes += ", renderer processes excluded as electron-comms' (bound separately)"
    notes += (". Timer components are per thread comm (D16), each sampled from its measured gap and run quantiles (D17) over the "
              "task's lifetime and merged, with the input wakes, into one explicit event stream at compile time (D9); the pooled "
              "residual stands for the comms below the coverage cut.")
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
    out += ["      " + notes]
    return "\n".join(out)


def main():
    R, out = sys.argv[1], sys.argv[2]
    blocks = ["  # ---- measured per-application archetypes — 9.5 campaign (meas-ci:interactive:3, meas-ci:playback:3) ----", ""]
    for aid, spec in ARCHETYPES.items():
        d = json.load(open(os.path.join(R, f"pool-{spec[0]}.json")))["runs"][spec[0]]
        blocks.append(entry(aid, spec, d))
        blocks.append("")
    open(out, "w").write("\n".join(blocks))
    print(f"wrote {out}: {len(ARCHETYPES)} entries")


if __name__ == "__main__":
    main()
