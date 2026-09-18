# Task 9.5 — measurement campaign method (draft, 2026-09-14)

The observation behind the eight archetypes of changelog D2 and D11, run on GitHub-hosted runners (phase decision 5). Written before any measurement; amended only by a dated entry in §9. Items marked **open** wait on the runner probe (`.github/workflows/meas-probe.yml`, run 34835910916) or on a decision in the changelog.

## 1. Runs

One run per archetype; each run is one observation (D3, D10), tagged `meas-ci:<workflow>:<run_number>`.

| Run | Archetype for | Program | Stimulus (D4, D5) | Workflow |
|---|---|---|---|---|
| `code` | `code` | Visual Studio Code with a TypeScript project open (sindresorhus/got at 64f21e2a, dependencies installed; design) and `source/index.ts` in the editor, so the built-in TypeScript language server runs (setup state, spec decision 6; the D3 campaign opened a text file) | SWELL-KW Word stream, keys and pointer (nearest; no code-editing dataset exists) | `meas-interactive` |
| `soffice` | `soffice.bin` | LibreOffice Writer with a large document open — 100 sections of five 100-word paragraphs, about 100 pages, ten pictures (design; no source states a length, S7); the stream types at its end (setup state; the D3 campaign used a new document) | SWELL-KW Word stream, keys and pointer | `meas-interactive` |
| `thunderbird` | `thunderbird` | Thunderbird with a pre-seeded local account, a compose window open | SWELL-KW Outlook stream, keys and pointer (c2 and c3) | `meas-interactive` |
| `chrome` | `chrome` (browser task) | Google Chrome, a local page with a text area and scrollable content | SWELL-KW Internet Explorer stream, keys and pointer; operation `page-load` (§3) | `meas-interactive` |
| `gimp` | `gimp` | GIMP, a 4952 × 3288 image open (PCMark 10 Photo Editing's interactive image size, Technical Guide p. 71; synthetic content, design; the D3 campaign used 800×600) | scripted canvas edit (design); operation `unsharp-mask` (§3) | `meas-interactive` |
| `kdenlive` | `kdenlive` | Kdenlive, a project with one 1920 × 1080 H.264 clip (PCMark 10 Video Editing, p. 76; 20 s, synthetic, design) on the timeline with an unsharp effect | scripted timeline scrub (design); operation `preview-render` (§3) | `meas-interactive` |
| `mpv-video` | video playback (`mpv`, `zoom` video, `gamescope` by approximation) | mpv `--vo=x11 --ao=null`, a 1280×720 30 fps H.264 file with AAC audio | none | `meas-playback` |
| `mpv-audio` | audio playback (`spotify`, `zoom` voice by approximation) | mpv `--no-video --ao=null`, the same file | none | `meas-playback` |
| `webrtc` | conferencing (`zoom` voice and video; replaces D11's approximation for `zoom`) | Google Chrome, a loopback WebRTC call in one page with a synthetic camera and microphone (`--use-fake-device-for-media-stream`) | none | `meas-playback` |

Applications are installed from the distribution's or vendor's current package at run time; the exact version is recorded in the run's `spec.json` and becomes part of the archetype's scope (D10).

## 2. Phases

Every run has two phases, in this order, after a settle period of 30 s from the window's appearance:

1. **idle** — no input for 120 s. Gives the timer-driven wake cadence and per-tick run (D9). For the playback runs this is the whole measurement: playback proceeds with no input.
2. **driven** — the stimulus stream replayed for its length (§3). Gives the per-input run (D9). Not run for the playback runs.

3. **driven-alt** (2026-09-16; the four typing-driven runs, §3 "Stimulus sensitivity") — the driven phase again under the 136M Keystrokes stream.
4. **op** (2026-09-16; applications with an operation, §3) — the operation triggered repeatedly by `ops_driver.py` with 10 s pauses for 600 s; each trigger and completion is logged to `ops.jsonl` on the monotonic clock. Gives the operation's duration table and the components inside its window (spec decisions 8–9).

Between phases a 10 s gap; the phase boundaries are logged with `phase.sh`.

## 3. Stimulus

- **Keystroke streams.** Extracted from SWELL-KW uLog XML (`swell-icmi14`; DANS doi:10.17026/dans-x55-69zp, v4) by `swell_streams.py` (**to write**): for each file, consecutive `Keyboard` events with the same `ControlApplication` form a stream; the gap before each event is the difference of `TimeStamp` values. Application map: `WINWORD` → Word stream, `OUTLOOK` → Outlook stream, `iexplore` → IE stream. Keys are replayed as a fixed letter cycle: the recording's key values are not used, only the timing. Selection (D12): each run replays its application's whole stream, keys and pointer events together; condition c1 for Word and Internet Explorer, c2 and c3 for Outlook (no c1 keystrokes); files concatenated in participant order; repeat r replays the r-th 600 s window of recorded time (`build_windows.py` → `dataset/meas/streams/<app>-r<r>.jsonl`, committed). Timestamps are quantised at the 15.6 ms Windows tick; 7 % of gaps are zero.
- **Pointer streams.** The same files' `Mouse` events (`clicked`, `dragged`, `wheel turned`) with their timing per application. Recorded positions (a 1600×1200 screen) are scaled into the application's content area — the window minus per-application insets for tab strips, toolbars and side bars (`appdefs.sh` AREA; design, so that replayed clicks land in the document, page or editor as the recorded ones did in theirs). Motion between recorded events is design: one straight move to the next event's position, issued at the event's time; no intermediate motion cadence is added (the record has no motion; `replay_stream.py --motion-ms` exists but is off).
- **Scripted interactions** for `gimp` and `kdenlive`: a fixed script of drags, clicks and wheel turns at fixed times, committed with the workflow, labelled design.
- **Replay driver.** Per-event xdotool through `replay.py`, timing on the monotonic clock. Fidelity (probe `timing` job, 120 events): absolute gap error p50 0.30 ms, p90 0.75 ms, p99 1.24 ms, max 1.41 ms.

**Operations** (2026-09-16; spec decisions 7–10; inputs per `search/S7-benchmark-inputs.md`). Trigger and input are design, cited where a benchmark states the input; cost and duration are the observation.

- `gimp` **unsharp-mask**: `plug-in-unsharp-mask` on the open 4952 × 3288 image through GIMP's Script-Fu server (started with the GUI by `-b`), std-dev 4.0, amount 0.32, threshold 8 — PCMark 10's batch unsharp "radius 8, sigma 4, amount 32, threshold 3" (p. 74) mapped onto the PDB (std-dev ← sigma; amount ← 32 % on the percent-scaled slider; threshold ← 3 % of 255); undo disabled so memory does not grow across repeats. Completion: the server's reply.
- `kdenlive` **preview-render**: Remove All Preview Zones, Add Preview Zone (the timeline zone is the whole clip; shortcuts seeded in `kdenliverc`), Start Preview Render (Shift+Return). Kdenlive renders the 25-frame chunks in an external `kdenlive_render preview-chunks` process, part of the tree. Completion: that process has appeared and exited.
- `chrome` **page-load**: navigate to `feed.html?i=<n>` on a local server (harness CPUs): the script builds a 300-post feed with thirty 1600 × 1200 pictures and runs a 200 000-record sort-and-aggregate pass (PCMark 10's social-feed and shop pages, pp. 52–53; CpsMark+'s pages "contain text, pictures, JS scripts", §4.3.3; sizes design). Completion: the page sets its title after the first paint of the built feed.

**Stimulus sensitivity — pre-registered before the campaign runs** (2026-09-16; spec decision 11). For the four typing-driven runs a `driven-alt` phase follows `driven` with the same length, replaying a stream cut from the 136M Keystrokes data (`dhakal-chi18`; transcription of memorised sentences) instead of SWELL-KW's free composition. Streams: `dataset/meas/streams/aalto-r{1..5}.jsonl`, built by `dataset/tools/meas/probe/aalto_streams.py` from participants with a full or laptop QWERTY keyboard, shuffled with seed 20260916 and taken in order until 600 s per repeat, recorded gaps kept within a participant (sentence pauses included), 2 000 ms per participant boundary, keys not exported (D4); selection and checksums in `aalto-windows.json`. Built streams: 3–4 participants and 1 892–2 375 keys per window; gap p50 157–183 ms, p90 376–595 ms, p99 2.2–2.9 s; share of gaps over 1 s 2.4–5.6 % (SWELL-KW Word c1: p50 156 ms, p90 702 ms, p99 4 477 ms; 15 %). **What is compared**: per application, the per-input run tables under rule (b) and the driven-phase wake rate and run distributions, SWELL-KW against 136M, pooled over repeats, in `results.md`. **What may change**: nothing in the archetypes — they carry SWELL-KW whatever the result (D6's grounds were the stimulus's realism, which the comparison does not test). The result lands as one sentence per typing archetype's scope stating how far `input_run` p50 moved under the transcription stream; a large difference is a stated limitation of D6, not a re-decision. No threshold is set because no decision hangs on one.

## 4. Instruments

- `perf sched record -k CLOCK_MONOTONIC -a` as root over each whole phase (probe: `linux-tools-<kernel>` installs; `perf_event_paranoid` 4 blocks the runner user), read with `perf sched timehist` for per-schedule run time, wait time and scheduling delay of every thread, and `perf sched timehist -w` for the wakeup rows with the waker (Xvfb wakes the application when it delivers input). The two text outputs, gzipped, are the released raw record; the `perf.data` file (up to ~1 GB per 600 s phase on Kdenlive) is kept in dry runs only.
- **Single core** (from the follow-up campaign on; 9.5 follow-ups spec decisions 2, 3 and 5): the application's process tree is launched pinned to one CPU (`pin.sh`, the runner's last vCPU); `run.sh` itself, Xvfb, perf, the replay driver and the snapshots run on the other vCPUs. The observation is the tree's own serialisation on one CPU with the display server idealised; the pin is recorded in `report.kv` (`pin.*`, `app.affinity`) and per phase in `phases.jsonl`. The runner's own agent processes (containerd, the hosted-compute agent, its .NET runtime) are not ours to pin and share the measured CPU: their rows lie outside the tree and are never counted, but their CPU time is contention the application saw (dry run 35091798452: about 1 100 of their schedule rows on the measured CPU over a 60 s phase against 18 865 of the application's). The D3 campaign (`interactive:3`, `playback:3`) ran unpinned on 4 vCPUs.
- `/proc` snapshots (`snapshot.py`) at phase boundaries: thread population, CPU time, voluntary and involuntary switches.
- `runner_spec.py` for the machine record; `apt-cache policy` for the application version.
- Screenshots at phase boundaries, to show what the application displayed (first-run dialogs, focus).

## 5. Wake attribution (D9)

Two rules are computed by `analyze.py` and the choice is a changelog decision on the dry-run data: (a) first-wake — the first application wake within W = 5 ms of a replayed event's send time (replay error p99 1.24 ms) and that schedule-in's run; the dry run attributed only 14–36 % of events this way for Writer, VS Code and Thunderbird, because busy applications wake every few milliseconds on their own; (b) window — all application run time in [s_i, s_{i+1}) minus the idle phase's CPU rate over that span, bounded below at zero, which charges each input with everything the application did until the next input, net of its timer load. A third signal, the waker of each wake (Xvfb = input delivery), is recorded for the analysis.

**What one wake is** (2026-09-16; spec decision 4): a timehist row is one schedule-in and its run, a *segment*. A segment is a wake only when a wakeup event for that thread (the `-w` rows) lies between the thread's previous schedule-out and this schedule-in; a segment without one is a resume after preemption, whose run is added to the preceding wake's and whose preempted time is neither run nor gap. Wake rates and the gap and run distributions are over wakes; rule (b) sums segments and is unaffected. The check of this definition on the D3 data is `wake-check.md`.

## 6. Derived parameters per archetype

From the pooled data of the run's repeats:

- `input_run` — distribution of the per-event input-driven run (driven phase).
- `tick_gap` and `tick_run` — distribution of gaps between timer-driven schedule-ins and their run times (idle phase), per thread class (**open:** whether the archetype's single task carries the main thread only or the whole tree's timer wakes merged).
- For the playback runs: `period` and `burst` from the schedule-in cadence and run time of the decoding and output threads (**open:** which thread is the task; mpv's thread names are recorded).
- Thread population and comm strings, for the modeling notes and the recognizer-visible names.

Distribution families follow the library's convention (log-normal by median and sigma) unless the data reject it, in which case the empirical quantiles are recorded and the choice is a changelog entry.

## 7. Repeats and tags

Five repeats per run in one batch (D10; as `meas-cli` and `meas-gui` did), matrix `repeat: [1..5]`; one run id per batch; the archetype takes the pooled distribution; the method's analysis reports the across-repeat spread of every derived parameter.

## 8. Scope, written into every archetype (D10)

Runner spec (4 vCPU Azure VM, `ubuntu-24.04`, kernel as recorded); Xvfb with no display refresh, so paint cadence is the toolkit's fallback timer; software rasterisation on CPU threads; mpv's null audio output simulates a perfect device against the system clock; no human; replayed timing from recordings made on Windows in 2012 (D6).

## 9. Amendments

- 2026-09-18, same-machine repeats (changelog D26) — a deviation from §7 and §8. The observation is a new campaign on one CPU model, the AMD EPYC 7763, under the machine gate (`dataset/tools/meas/machine_gate.sh`): a job that drew another model stops before it installs or measures anything, recorded (`gate=wrong-machine`), and is not a repeat. Nothing of runs `interactive:6/8/9` and `playback:6` is pooled (their models: `machine-draws.md`); the campaign has no cross-machine check. §7: each application launches windows 1–5 first — of its SWELL-KW stream and of the 136M streams, as committed — and then adds one repeat at a time, the criterion evaluated after each, until it holds: the 95 % confidence half-width of the across-repeat mean of the application's headline median, relative to the mean, at most 5 % (`dataset/tools/meas/stability.py`). Headline medians: `input_run` p50 for `soffice`, `code`, `thunderbird`; operation duration p50 for `chrome`, `gimp`, `kdenlive`; play-phase CPU share for `mpv-video`, `mpv-audio`, `webrtc`. An added repeat of a stream-driven application replays the next window: SWELL-KW windows continue by §3's rule in participant order (`build_windows.py --repeats N`), the `driven-alt` phase takes the next 136M window in the same seeded order (`aalto_streams.py --repeats N`); windows 1–5 are unchanged by either. A job stopped by the gate leaves its window unused; it is the next one tried. `thunderbird` stops at eight repeats whatever the criterion: SWELL-KW's Outlook conditions hold 4 761 s of recorded time, the eighth window 561 s; its half-width is then stated as it is. Every same-machine repeat obtained is pooled and reported. §8: the runner line of the scope names the pooled repeats' CPU model and kernel from their `spec.json` (`fold_in.py`). Trigger: `.github/campaign.json` gains `cpu_model`, and a family's `repeats` may map each application to its own list. §7 tags: the campaign is `meas-ci:interactive:<launch date>` and `meas-ci:playback:<launch date>` (D27), each repeat's run id in the pooled record.
- 2026-09-16, stimulus sensitivity (spec decision 11): §2 the `driven-alt` phase; §3 the 136M streams and the pre-registration.
- 2026-09-16, appdefs (spec decisions 6–10): §1 setup states for `code` (project + language server) and `soffice` (large document), inputs for `gimp` and `kdenlive`; §2 the `op` phase; §3 the three operations with their triggers, completion signals and cited inputs (`search/S7-benchmark-inputs.md`). Pending the runner probe.

- 2026-09-16, follow-ups (spec `_dev/docs/spec/jioh/task-9.5-interactive-typing-follow-ups.md`): §4 single-core pin from the next campaign on; §5 the wake definition (wakeup-defined, resumes merged), checked on the D3 data (`wake-check.md`).

- 2026-09-15, fold-in (D19): the archetypes are in the library; the campaign's numbers are in `results.md`; raw data released as `meas-ci-2026-09-14` (D20).
- 2026-09-14, after dry run 1 (runs 34838057273, 34838057243): §3 content-area insets; §4 wakeup rows kept, `perf.data` dropped in full mode; §5 two attribution rules with the dry-run rates; Thunderbird's compose window opened by Escape and ctrl+n after the Account Hub.
- 2026-09-14, D12: §3 stimulus selection and motion rule settled; §1 stimulus column updated.
- 2026-09-14, after the runner probe (`probe.md`): §1 `webrtc` run confirmed and its scope stated; §4 instruments settled; §5 W = 5 ms; Thunderbird's profile must carry a local account and identity for `-compose` (dry-run item); MLT audio and every audio path run without a device (§8).
