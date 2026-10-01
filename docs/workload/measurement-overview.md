# How the Workload Dataset Is Measured
> Status: draft · Created 2026-09-29 · Updated 2026-09-29

> The 23 archetypes of §2 take every value from our own measurement of the real program on a CI runner. This document covers them: which programs they are, what each measurement job runs and why it resembles real use, how a run becomes a carried value, when the repeats stop, the exceptions, the checks, the literature behind the method, and what the values claim. The operational rules are in `_dev/research/jioh/measurement-campaign-workflow.md`; every campaign's repeats, values and machine draws are in `_dev/research/jioh/measurement-campaign-record.md`.

## 1. Principles

- **Verification standard.** A value taken from a source is recorded with its verbatim passage, its locator and the copy read. A value no source states carries no source tag and is labelled for what it is: convention, arithmetic, placeholder or design.
- **One observation per archetype.** Every number of one archetype comes from one observation. For a measured archetype that observation is one measurement campaign of one program.
- **Our own measurement runs on CI runners only.** What a runner cannot observe comes from literature or public traces, or is labelled design. The venue is a stated limitation of every measured value (§11).

## 2. The measured archetypes

| domain | archetypes | subject |
|---|---|---|
| interactive applications | `office-writer`, `code-editor`, `mail-client`, `web-browser`, `image-editor`, `video-editor` | LibreOffice Writer, VS Code, Thunderbird, Google Chrome, GIMP, Kdenlive |
| playback and calls | `video-player`, `audio-player`, `video-call` | mpv playing a video file, mpv playing its audio, a WebRTC call in Chrome |
| builds and batch programs | `build-orchestrator`, `compiler-child`, `cpu-batch` | GNU make and gcc building a Linux kernel; `clamscan`, `ffmpeg`, `HandBrakeCLI`, a PyTorch training loop, `tracker-miner-fs-3` |
| background I/O | `file-backup`, `file-archiver`, `game-download` | borg, 7-Zip, SteamCMD |
| browser renderers and comms clients | `renderer-hidden`, `renderer-visible`, `chat-client`, `game-client` | a Chrome renderer in a background tab, one in a visible window, Element Desktop, the Steam client |
| session processes | `compositor-shell`, `audio-server`, `service-manager`, `message-bus` | GNOME Shell with Mutter, the PipeWire stack, systemd, dbus-daemon — in one idle Ubuntu 24.04 desktop session |

The interactive, renderer, comms and session entries carry per-thread components (a wake rate plus gap and run tables) and, where their observation holds them, a replayed input stream, operations and rare events; the playback and call entries carry one periodic job per media cycle; the build, batch and background I/O entries carry run tables (make's dispatch, each compile step, the runs between blocks) and block tables. The compiler turns these into one explicit event stream per task (`docs/simulator/interpretation-contract.md`).

## 3. From a run to a value

```
real program + realistic drive
   → one job on a fresh GitHub runner   (machine gate, one pinned core, settle, phases, perf sched record)
   → analysis per repeat                (wakes, runs, gaps, per-thread components)
   → pool across repeats                (the stability rule decides when to stop)
   → fold-in to archetypes.yaml         (quantile tables and rates; scope and half-widths stated)
   → wlc draws each task's event stream (seeded, byte-identical)
   → workload files
```

- **The job.** A GitHub-hosted `ubuntu-24.04` runner, 4 vCPU. The measured process tree is pinned to one CPU; the harness, the tracer, the input driver and any peer server (a page server, a mail peer, a Matrix homeserver) run on the others. `perf sched record` on `CLOCK_MONOTONIC` traces whole phases.
- **A repeat** is one full job on a fresh runner — the level at which the largest random variation enters, and so the unit the rule counts.
- **A campaign** is every repeat of one measurement, tagged `meas-ci:<workflow>:<launch date of its first batch>`. Its raw records are published as a GitHub release (§9).
- **The fold-in** writes the pooled values into the archetype, with its scope (the program, build, machine, repeats and every stated limit) and its `validation_stats` (the runs, the per-repeat ranges).

## 4. How a job resembles real use

- **The real program.** The stock build with its installed defaults. The build is pinned where the vendor allows it (VS Code); otherwise it is recorded per repeat and the mix is stated with the values (Chrome, Thunderbird).
- **Recorded human input where it exists.** The typing entries replay SWELL-KW (`swell-icmi14`: 25 knowledge workers, about three hours each, keystrokes timestamped with the focused application) at the recorded times: the Word stream into LibreOffice and VS Code, the Outlook stream into Thunderbird's message body, the Internet Explorer stream into a page's text box. Keys only: the recorded pointer events are not replayed. Each repeat replays the next 600 s window of the recording.
- **Stimulus timing may come from any platform, the response only from Linux.** SWELL-KW was recorded on Windows in 2012; what the program does in response to each key is measured on Linux.
- **Benchmark-defined operations where no recording exists.** An operation is triggered repeatedly through a phase and carried as the mean over its run of operations: GIMP's unsharp mask on PCMark 10's image size and settings (`pcmark10`), Kdenlive's preview render of a 1080p H.264 clip, Chrome's page load of a built feed page (page kind from `pcmark10` and `cpsmark-tbench23`, sizes design), Thunderbird's send of a reply with a Word attachment (kind from `cpsmark-tbench23`, size design). GIMP and Kdenlive, for which no observed input exists, are driven by a scripted pointer loop (design).
- **Documented mechanisms fix unattended states.** Background tabs are measured past Chromium's documented intensive-throttling grace; a visible renderer stays visible because Linux Chromium tracks no occlusion; the chat client idles on the Matrix 30 s `/sync` long poll; the session is left untouched until its 300 s idle delay locks the screen and blanks the monitor.
- **Real inputs and links where the work depends on them.** borg and 7-Zip read Matt Mahoney's 10 GB benchmark set, 79,431 files from one laptop (`mahoney-10gb`); SteamCMD installs a 10.4 GB depot over a link shaped to 121.0 Mbps, the byte-weighted median of Valve's per-country download rates (`steam-download-stats`), with an `fq_codel` queue (`fqcodel-rfc18`). The kernel build runs `-j8`: the build tools' documented defaults follow `nproc`, here for an eight-thread desktop.
- **Steady behaviour, not launch work.** A settle precedes each measured idle or play phase. Where the traces cannot tell launch work from behaviour that recurs, one long probe of the phase (1,400–3,600 s) runs first: episodes that stop set the settle, episodes that recur lengthen the phase to hold them. Chrome settles 420 s, Thunderbird 390 s, the call 210 s, the Steam client 900 s; VS Code's idle phase is read from 200 s past its start.
- **What no source states is labelled design** — the document length, the clip, the twelve renderers, the chat message rate, the attachment size — and the scope says so.

## 5. What a run is turned into

- **Wake.** A schedule-in preceded by a wakeup of that thread since its last sleep. A resume after preemption is folded into the wake it continues.
- **Run.** The CPU time of one wake.
- **Gap.** Taken over a component's merged wake times and wrapped round the span observed, so a gap mean is exactly the span over the wakes and the rate a gap table implies is the rate measured.
- **Component.** One thread comm within one process role (`gpu/Chrome_ChildIOT`, `pid1/systemd`). Components are kept in descending wake rate until they cover 95 % of the phase's wakes; the rest is pooled as one residual. A component that does not wake at least twice in every repeat is reported as sporadic, not carried, unless it is carried as a sparse component (§7).
- **Table.** The ten pooled quantiles p1 … p99.9, the sample's minimum and maximum, and the measured mean of the samples in each interval, so a draw keeps both the quantiles and the sample's mean.
- **Per kind of entry.** A typing entry carries its per-input run: the tree's CPU from one input to the next, less the idle rate over that span. An operation carries its duration table and its components. A playback or call entry carries one periodic job per media cycle — its period and its per-cycle CPU. A build or batch program carries its runs between voluntary blocks and the block after each run.

## 6. The stability rule

| element | what it says | ground |
|---|---|---|
| One CPU model | Only the AMD EPYC 7763 counts. A job that draws another model stops within about 20 s, before installing anything, and is not a repeat. About half of all jobs draw it (50–59 % by campaign). | `maricq-osdi18`: servers "with supposedly identical parts" differ run to run. Measured here: an Intel Xeon ran `cc1` at 0.72× and `fixdep` at 0.50× the EPYC's time. |
| Level of repetition | The interval is taken over independent repeats, never over samples within a run. | `kalibera-ismm13` §3, §9.3 |
| Criterion | Every value the fold-in carries, each component on its own and never averaged across components: the 95 % t half-width is at most 5 % of the mean, or 1 µs where larger. A rate or share is read by its per-repeat values; a table by the count-weighted mean it carries. | 5 % is design: half the smallest effect reported as a comparison of carried values (the kernel build's 10 % between `-j8` and `-j1`). 1 µs is the trace's resolution. The table's half-width is the ratio estimator's (`cochran-st77`). |
| Minimum and stopping | At least five repeats. Repeats are added one at a time — or one batch sized by the pool's own projection, then one at a time — until every value holds. No ceiling. | `kalibera-ismm13` §11; `georges-oopsla07` §4 |
| What the stop guarantees | Stopping at the first count that passes makes the stated half-width optimistic. Simulated at each entry's widest value, the stated 95 % interval covers the true mean in 91–94 % of campaigns where that value sits within half a point of the tolerance, and the stopped mean leans by at most 0.2 %; those entries' scopes say so. | `chow-aoms65`: first-crossing coverage reaches the nominal level only asymptotically, with a lower bound near .929 |

Qualifications carried with the rule: `maricq-osdi18` recommends nonparametric intervals of the median unless normality is shown; the rule's is a t interval. `cochran-st77`'s ratio variance is a large-sample result, and the campaigns' counts are 5 to 77.

A spread the harness, the analysis or the observation makes is not answered with repeats but with a change of design — keys-only replay, a longer phase, a component identity that survives a renamed thread.

## 7. The exceptions

A value whose spread is the machine's, a session's, a sparse count's or a rare event's, or whose recorded input runs out, is carried under one of five classes in place of the tolerance. The first four are taken per value by 인지오's decision, after the value is seen failing; the fifth follows from the recording's length. Every such value's half-width, range and repeat count are stated in the archetype's scope, and no reported result may rest on a difference smaller than a stated half-width.

| class | when it applies | carried in | how it is carried |
|---|---|---|---|
| Spread follows the machine | The value moves with the runner's disk or speed, not the program: its run times move together across every thread of a repeat while wake rates hold within about 1 %. | `cpu-batch`'s disk blocks (±9.5–15 %); `renderer-visible`'s and `game-client`'s run means (±5.3–10.1 %) | With its half-width, range and count, over at least five repeats; only for a value no reported effect rests on |
| Varies between sessions | A window of the phase's length slid along one long run moves the value far less than it moves across repeats. | `code-editor`'s `utility/libuv-worker` (within one run ±10.6 %, across repeats ±39 %); the renderers' quiet threads (±18–26 %); `service-manager`'s pid 1 run mean (±7.8 %); `message-bus`'s system bus (±11 %) | Its wake rate, gap mean and run mean together, with both spreads |
| Sparse component | It wakes only a few times a phase, so the spread is its count's own. | the renderers' residuals (1–5 wakes per renderer per phase) | Its three values together, with its wake count stated |
| Rare event within a run | An event a repeat catches none, one or two times. | Chrome's `MemoryInfra` heavy pass (about one per 22 min); the Steam client's HTTP burst | The event's runs above a stated threshold leave the component and are carried as separate events at their pooled rate |
| Recording runs out | A phase replays recorded input and the recording has no further window. | `mail-client`'s input and send (the Outlook recording's 8 windows; per-input mean under SWELL-KW ±10.4 %, the send's `StreamTrans` run mean ±18.4 %); `web-browser`'s per-input mean (38 windows, ±5.9 %) | With its half-widths, every window the recording holds pooled |

Values of a few microseconds pass by the 1 µs floor rather than the 5 %: the block per run of `file-archiver` and `game-download`, the encoders' blocks in `cpu-batch`, the Steam client's `CJobMgr::m_Work` run mean. Whether the exception-carried values are re-measured at a count fixed in advance is decided with the sensitivity check of the specs that consume the dataset — the scoring spec and the RQ0 gate spec.

## 8. Checks and controls

- **Validity per repeat**, before a repeat counts: the replay sent every event of its window; every operation completed; screenshots show the input landed where designed; the steady phase's 10 s profile shows no launch work; no harness process is in the measured tree; a shaped download went through the shaper. A failing repeat is left out with its reason, and the rule is read over the rest.
- **Wakes traced to their cause** (the session processes). Each wake of the four session entries is traced through its wakers; wakes caused by the harness or by software a stock Ubuntu 24.04 desktop does not run (`ubuntu-desktop-manifest`, `systemd-ubuntu`, `livecd-rootfs`, `netplan`) leave the components and are stated. Jobs bound to a clock time are stated as events, not carried.
- **The untraced control** (the interactive, playback, renderer, comms and session entries). Each carried phase runs twice in six jobs per subject, traced and untraced in alternating order, each thread's CPU time and switches read from `/proc`. Where a difference is resolved, a wake rate's ratio, untraced over traced, lies in 0.97–1.08, and a run mean's in 0.72–0.98: tracing lengthens some threads' runs. Each difference is stated in the archetype's notes; the carried values stay the traced ones. The build campaign cross-checks perf against taskstats (1.005 for `cc1`); the download reads the cost of its socket tracing (0.975 of the CPU without it).
- **The stimulus-sensitivity check.** Each typing entry also replays transcription typing from the 136M Keystrokes data (`dhakal-chi18`) and compares per-input means, repeat by repeat: `office-writer` 1.12, `web-browser` 1.34, `mail-client` 0.91, `code-editor` not resolved. The archetypes carry SWELL-KW whatever the check shows; the ratio is stated in each scope.
- **Build mix.** Where the build cannot be pinned, the two builds' repeats are compared value by value against the first build's own spread; the few that differ are stated.
- **Time windows.** Every carried phase is also read in 100 s windows; where part of the work happens only in part of the phase, the scope says so. The carried values stay the phase means.
- **Compile fidelity.** Tests check that a table's draws keep its mean, that each component's gap table implies its measured wake rate within 2 %, and that each measured archetype compiles at the wake rate it carries, within 5 % or four standard errors of the count (`feller-ipta50`). The compiled streams do not reproduce the order of a component's gaps nor its components waking together: at 1–100 ms, measured wake counts are 1.9–11× more dispersed than compiled ones for `chat-client`, `code-editor`, `web-browser`, `mail-client` and `game-client` — a stated threat to validity.

## 9. Campaigns at a glance

| archetype | repeats | stopped by | carried under an exception |
|---|---|---|---|
| `office-writer` | 14 | the rule | — |
| `code-editor` | 44 | window 44 of the Word recording's 57; every value the rule is read on holds at 44 | `utility/libuv-worker` (between sessions) |
| `mail-client` | idle 77; input and send 8 | idle: the rule; input and send: the Outlook recording's last window | input and send values (recording runs out) |
| `web-browser` | 38 | the Internet Explorer recording's last window | per-input mean under SWELL-KW (recording runs out); `MemoryInfra` (rare event) |
| `image-editor` | 5 | the rule, at the minimum | — |
| `video-editor` | 20 | the rule | — |
| `video-player` | 24 | the rule | — |
| `audio-player` | 31 | the rule | — |
| `video-call` | 45 | the rule | — |
| `build-orchestrator`, `compiler-child` | 14 | the rule | — |
| `cpu-batch` | 14 (`clamscan` 10, `python3` 8) | the rule | four disk-block values (machine) |
| `file-backup` | 30 | the rule | — |
| `file-archiver` | 6 | the rule | — |
| `game-download` | 30 | the rule | — |
| `renderer-hidden` | 19 | the rule | quiet threads (between sessions); residual (sparse) |
| `renderer-visible` | 11 | the rule | two run means (machine); quiet threads (between sessions); residual (sparse) |
| `chat-client` | 18 | the rule | — |
| `game-client` | 12 | the rule | four run means (machine); the HTTP burst (rare event) |
| `compositor-shell`, `audio-server`, `service-manager`, `message-bus` | 24, shared | the rule | pid 1's run mean and the system bus (between sessions) |

Raw records, one GitHub release per campaign or addition:

| release | holds |
|---|---|
| `meas-ci-2026-09-18` | `office-writer`, `image-editor`, `video-editor`, `video-player`, `audio-player`; `mail-client`'s first 43 idle repeats |
| `meas-ci-2026-09-20` | `web-browser`, `video-call` |
| `meas-ci-2026-09-25` | `code-editor` |
| `meas-ci-2026-09-27` | `mail-client`'s input and send repeats |
| `meas-ci-2026-09-28` | `mail-client`'s 34 added idle repeats |
| `meas-ci-build-2026-09-18` | `build-orchestrator`, `compiler-child`, `cpu-batch` |
| `meas-ci-background-2026-09-19` | `file-backup`, `file-archiver`, `game-download` |
| `meas-ci-desktop-2026-09-20` | `renderer-hidden`, `renderer-visible`, `chat-client`, `game-client` |
| `meas-ci-session-2026-09-24` | the four session entries |
| `meas-ci-control-2026-09-27` | the untraced control |

## 10. Literature

The method:

| id | what it grounds |
|---|---|
| `maricq-osdi18` | holding one CPU model and reading the repeat count on it |
| `kalibera-ismm13` | repetition at the highest level of variation, the t interval over repeats, on-line stopping, the minimum of five |
| `georges-oopsla07` | the same construction: an interval over independent runs, runs added until a set precision |
| `cochran-st77` | the half-width of a count-weighted table mean (the ratio estimator) |
| `chow-aoms65` | what stopping at the first passing count guarantees |
| `feller-ipta50` | the standard error of a compiled wake count |
| `liu-jacm73` | the periodic jobs' deadline at the next period's start |

The drive and the states:

| id | what it grounds |
|---|---|
| `swell-icmi14` | the replayed typing |
| `dhakal-chi18` | the sensitivity check's transcription typing only |
| `pcmark10`, `cpsmark-tbench23` | the operations' kinds, sizes and settings |
| `mahoney-10gb` | the backup and archive input set; its set check against `fm-results-tables` (GNU/Linux users' median file size) and `meyer-fast11` (half of the bytes in files over 30 MB, Windows, 2009) |
| `steam-download-stats`, `fqcodel-rfc18` | the download's link rate and why its queue is `fq_codel` |
| `mozilla-testpilot10` | one visible renderer per window |
| `ubuntu-desktop-manifest`, `systemd-ubuntu`, `livecd-rootfs`, `netplan` | what a stock Ubuntu 24.04 desktop holds and runs |
| `glean` | Thunderbird's daily 04:00 metrics thread, stated as a clock event |

Vendor and project documentation (Chromium's process model and throttling, the Matrix client-server spec, GNOME's idle defaults, the kbuild, GCC and make sources, borg's internals, Steam's content system) is cited in each measurement's search records. No literature value is carried as an archetype number: literature grounds the method, the drive and the states, and the numbers are the campaigns'.

## 11. What the values claim

Every measured value is this software on this machine: a GitHub-hosted runner, one pinned AMD EPYC 7763 core shared with the runner's own agent, Xvfb or a headless session, no GPU, no display refresh, no sound device, no human, one CPU model over one period. The values are not desktop truth. The precision stated is precision on that configuration — reproducibility, a separate property from representativeness. Real-desktop validation is deferred.

## Where to go deeper

| question | where |
|---|---|
| the rules a campaign follows, in full | `_dev/research/jioh/measurement-campaign-workflow.md` |
| every campaign's repeats, values, exceptions and machine draws | `_dev/research/jioh/measurement-campaign-record.md` |
| one domain's method and decisions | `_dev/research/jioh/task-9.<5–9>-*/campaign/method.md` and `changelog.md` |
| what one archetype carries and its stated limits | its entry in `dataset/archetypes.yaml` (`validation_stats.scope`, `modeling_notes`) |
| where a cited source says what | `docs/references.md` |
