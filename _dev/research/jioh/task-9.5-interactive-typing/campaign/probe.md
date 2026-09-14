# Runner probe — result (2026-09-14)

Workflow `.github/workflows/meas-probe.yml`; the run read here is 34837008757 (the fifth push; runs 34835910916, 34836100266, 34836193163 were cancelled for script bugs, 34836453623 had the process-group and snapshot bugs fixed after it). Per-job `report.json`, `timing.json` and `spec.json` are copied under `probe/`. These are probe numbers — 20 s idle and 20–35 s driven phases, one repeat — never values; they establish what a run can drive and observe (method §1, §4, §5).

## Runner

`ubuntu-24.04`, kernel 6.17.0-1022-azure, 4 vCPU AMD EPYC 7763, Xvfb preinstalled. `linux-tools-6.17.0-1022-azure` installs (perf version 6.17.13). `perf_event_paranoid` = 4: `perf sched record` fails for the runner user (rc 129) and works as root (`-a`, 3 s: 2 638 timehist rows). tracefs mounted and readable as root. `/dev/uinput` present (`CONFIG_INPUT_UINPUT=y`), `/dev/input` has event0, event1, mice. No `/dev/snd`, no `snd` module loaded, `modprobe snd-dummy` fails (rc 1). PulseAudio (`--start`) and PipeWire + WirePlumber + pipewire-pulse start as user-space servers; `pactl info` and `pw-top` answer. `apt-cache policy` finds xdotool, ydotool, evemu-tools, python3-xlib, trace-cmd, bpftrace.

## Replay fidelity (timing job)

120 keys replayed through `replay.py` (per-event xdotool, monotonic clock) into an X client logging KeyPress times: 120 delivered; requested gaps p50 189 ms, p90 445 ms; absolute error per gap p50 0.30 ms, p90 0.75 ms, p99 1.24 ms, max 1.41 ms; mean error −0.006 ms. `xdotool type --delay 100` delivered 60 of 60. Method §5's W can be set at 5 ms with margin.

## Applications (one repeat, idle 20 s, driven 35 s typing / 30 s pointer / 20 s none)

| run | version installed | window (wait) | threads | idle CPU share | idle switches/s | driven CPU share | driven switches/s | timehist rows of the app in 5 s driven | evidence input landed |
|---|---|---|---|---|---|---|---|---|---|
| code | VS Code 1.137.0 (vendor .deb) | 3.1 s | 161 | 0.017 | 226 | 0.111 | 598 | 1 636 | title "● sample.txt" (modified) |
| soffice | LibreOffice 24.2.7.2 (apt) | 10.2 s | 6 | 0.0009 | 3.4 | 0.013 | 61 | 443 | screenshot: 120 characters in the document, "5 words, 120 characters" |
| thunderbird | Thunderbird 155.0.1 (snap via apt) | 2.1 s | 127 | 0.010 | 55 | 0.028 | 283 | 178 | screenshot: text typed into the account-setup dialog's "Full name" field; no compose window (no account in the profile) |
| chrome | Google Chrome 152.0.7977.82 (preinstalled) | 10.9 s | 110 | 0.030 | 227 | 0.031 | 341 | 626 | title "page.html"; textarea focused |
| gimp | GIMP 2.10.36 (apt) | 4.2 s | 13 | 0.000 | 0 | 0.006 | 21 | 124 | screenshot: crop tool selected by the clicks, image open |
| kdenlive | Kdenlive (apt, noble; `--version` needs a display) | 0.6 s | 29 | 0.0009 | 4.4 | 0.85 | 3 331 | 3 603 | screenshot: editing layout, a clip region dragged on V2; MLT's SDL audio consumer fails (no device) |
| webrtc | Chrome, loopback call, fake camera | 10.9 s | 134 | 0.167 | 2 168 | 0.231 | 1 938 | 615 | title "enc=914 dec=913 fps=20" after ~45 s |
| mpv-video | mpv 0.37.0, `--vo=x11 --ao=null`, 1280×720 30 fps H.264 | 2.8 s | 18 | 0.256 | 790 | 0.257 | 779 | 2 825 | steady playback; threads `vo`, `mpv`, `worker`, `demux`, `ao`, `av:h264:*`, `lua/osc` |
| mpv-audio | mpv 0.37.0, `--no-video --ao=null` | 3.4 s | 19 | 0.009 | 183 | 0.009 | 178 | 761 | steady playback |

`perf sched timehist` reports per-thread comm, run time, wait time and scheduling delay per schedule-in for every thread of every application (e.g. `Compositor`, `Chrome_ChildIOT`, `VizCompositorTh`, `ThreadPoolForeg` for Electron and Chrome; `vo`, `ao`, `demux` for mpv). Xvfb itself and the replay driver appear as separate comms and are excluded by name.

## What the probe settles for the method

- Instruments: `perf sched record -a` as root over each phase; `/proc` snapshots; screenshots. (§4 open item closed.)
- Replay: per-event xdotool holds intervals to ~1 ms; W = 5 ms. (§5 open item closed.)
- Drivable: all six applications and mpv in both modes. Thunderbird needs a profile pre-seeded with a local account and identity so `-compose` opens a compose window; to be verified in the campaign dry run. GIMP and Kdenlive take pointer input; Kdenlive's driven phase is CPU-heavy under drags.
- Conferencing: a Chrome WebRTC loopback call with a synthetic camera runs on the runner (encode and decode at 20 fps). A `webrtc` run enters the campaign (D11's probe item), giving `zoom` a measured conferencing archetype instead of an approximation, with the loopback and synthetic camera as its stated scope.
- Audio: no device; mpv's null output and the user-space servers are the only audio paths. (Scope, §8.)
- Idle wakes are real and application-specific already at 20 s: Writer 3.4 switches/s, GIMP ≈ 0, Kdenlive 4.4, Thunderbird 55, VS Code and Chrome ≈ 226, an idle WebRTC call 2 168; this is what D9's idle phase measures.

## Not settled

- Thunderbird compose with a pre-seeded local account (campaign dry run).
- Whether Chrome's `--disable-gpu` and Xvfb change the paint cadence relative to a compositor-driven desktop: known scope limit (§8), not measurable here.
- Playback of longer content and mpv's frame-drop statistics (`--msg-level`): campaign, not probe.
