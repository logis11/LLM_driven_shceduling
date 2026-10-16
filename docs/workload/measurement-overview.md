# How the Workload Dataset Is Measured
> Status: draft · Created 2026-09-29 · Updated 2026-10-17

> The 28 measured archetypes of §2 — every entry of the library but the game chain (`game-task-chain`, built on `lavd-ossna24`'s reported figures) — take every value from our own measurement of the real program on a CI runner. This document covers them: which programs they are, what each measurement job runs and why it resembles real use, how a run becomes a carried value, when the repeats stop, the exceptions, the checks, the literature behind the method, and what the values claim. The operational rules are in `_dev/research/jioh/measurement-campaign-workflow.md`; every campaign's repeats, values and machine draws are in `_dev/research/jioh/measurement-campaign-record.md`.

## 1. Principles

- **Verification standard.** A value taken from a source is recorded with its verbatim passage, its locator and the copy read. A value no source states carries no source tag and is labelled for what it is: design, convention or arithmetic. A value awaiting measurement carries `meas-pending`, which `make lint`'s freeze rejects, so none enters the dataset.
- **One observation per archetype.** Every number of one archetype comes from one observation: for a measured archetype, the measurement of one program in one state — for `cpu-batch`, of each of its two programs, each in its own campaign. Where a phase was measured again, the entry's scope names the campaign each phase's values come from (`mail-client` and `video-editor`: the idle phase from one campaign, the phases with or after the input from another); a launch phase comes from its own campaign (§4, §5).
- **Our own measurement runs on CI runners only.** What a runner cannot observe comes from literature or public traces, or is labelled design. The venue is a stated limitation of every measured value (§11).

## 2. The measured archetypes

| domain | archetypes | subject |
|---|---|---|
| interactive applications | `office-writer`, `code-editor`, `mail-client`, `web-browser`, `image-editor`, `video-editor` | LibreOffice Writer, VS Code, Thunderbird, Google Chrome, GIMP, Kdenlive |
| playback and calls | `video-player`, `audio-player`, `video-call` | mpv playing a video file, mpv playing its audio, a WebRTC call in Chrome |
| builds | `build-orchestrator`, `compiler-child`; `module-build-orchestrator`, `module-compiler-child` | GNU make and gcc building a Linux kernel (linux-6.6, `-j8`); DKMS rebuilding NVIDIA's open kernel module for a security kernel, run by the stock unattended upgrade |
| batch programs | `cpu-batch`, `video-transcoder` | PyTorch's basic MNIST example trained on the CPU (`python3`, its process shown as `python`) and Kdenlive's export of the `video-editor` project (`kdenlive_render`, its `melt-7` doing the work); HandBrakeCLI transcoding a 4K clip to 1080p at its default preset |
| background jobs | `package-upgrade`, `file-indexer`, `incremental-backup`, `file-archiver`, `game-download`, `game-download-idle` | the stock Ubuntu 24.04 unattended upgrade installing a published glibc security update; Tracker's first index of a home; Déjà Dup's scheduled weekly incremental backup; 7-Zip; SteamCMD installing a game depot; the download's tables under the declared class `idle` |
| browser renderers and comms clients | `renderer-hidden`, `chat-client`, `game-client` | a Chrome renderer in a background tab, Element Desktop, the Steam client |
| session processes | `compositor-shell`, `audio-server`, `service-manager`, `message-bus` | GNOME Shell with Mutter, the PipeWire stack, systemd, dbus-daemon — in one idle Ubuntu 24.04 desktop session |

The interactive, renderer, comms and session entries carry per-thread components (a wake rate plus gap and run tables) and, where their observation holds them, a replayed input stream, operations and rare events; the playback and call entries carry one periodic job per media cycle; the build, batch and background entries carry run tables (make's dispatch, each compile step, the runs between blocks) and block tables. The compiler turns these into one explicit event stream per task (`docs/simulator/interpretation-contract.md`).

Three entries carry the declared class `idle`; every other entry carries `normal`. `file-indexer` and `incremental-backup` take it from what their programs declare: Tracker's threads run SCHED_IDLE at nice 19, and Déjà Dup's monitor starts the backup under `chrt --idle 0 ionice -c3`. `game-download-idle` is `game-download` with its tables shared by reference and the class `idle` in place of the measured download's `normal`; only `c2-p2a-idle` binds it (§11).

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

- **The job.** A GitHub-hosted `ubuntu-24.04` runner, 4 vCPU. The measured process tree is pinned to one CPU; the harness, the tracer, the input driver and any peer server (a page server, a mail peer, a Matrix homeserver) run on the others. `perf sched record` on `CLOCK_MONOTONIC` traces whole phases; the build, batch and background jobs add a taskstats listener on the measured CPU, which reads each process's CPU at its exit.
- **A repeat** is one full job on a fresh runner — the level at which the largest random variation enters, and so the unit the rule counts.
- **A campaign** is every repeat of one measurement, tagged `meas-ci:<workflow>:<launch date of its first batch>`, a letter added for a second campaign of the same workflow launched that date (`meas-ci:background:2026-10-02b`). Its raw records are one or more GitHub releases (§9), made by hand when the campaign is pooled, before GitHub deletes a workflow's artifacts after 90 days (`gh-artifact-retention`). `dataset/meas-releases.yaml` maps every campaign tag the data carries to its releases, with each asset's SHA-256, and `make lint` fails a tag without one.
- **The fold-in** writes the pooled values into the archetype, with its scope (the program, build, machine, repeats and every stated limit) and its `validation_stats` (the runs, the per-repeat ranges); a launch phase's fold-in writes its streams under `dataset/launch/` (§5).

## 4. How a job resembles real use

- **The real program.** The stock build with its installed defaults. The build is pinned where the vendor allows it (VS Code; the upgrade, DKMS, indexer, training, transcode, export and backup jobs, each run in a chroot of Ubuntu 24.04's default desktop layer built from Ubuntu's snapshot service as the archive stood on a stated date); otherwise it is recorded per repeat and the mix is stated with the values (Chrome, Thunderbird).
- **Recorded human input where it exists.** The typing entries replay SWELL-KW (`swell-icmi14`: 25 students and interns doing knowledge-work tasks in a lab, about three hours each, keystrokes timestamped with the focused application) at the recorded times: the Word stream into LibreOffice and VS Code, the Outlook stream into Thunderbird's message body, the Internet Explorer stream into a page's text box. Keys only: the recorded pointer events are not replayed. Each repeat replays the next 600 s window of the recording.
- **Stimulus timing may come from any platform, the response only from Linux.** SWELL-KW was recorded on Windows in 2012; what the program does in response to each key is measured on Linux.
- **Benchmark-defined operations where no recording exists.** An operation is triggered repeatedly through a phase and carried as the mean over its run of operations: GIMP's unsharp mask on PCMark 10's image size and settings (`pcmark10`), Kdenlive's preview render of a 1080p H.264 clip, Chrome's page load of a built feed page (page kind from `pcmark10` and `cpsmark-tbench23`, sizes design), Thunderbird's send of a reply with a Word attachment (kind from `cpsmark-tbench23`, size design). GIMP and Kdenlive, for which no observed input exists, are driven by a scripted pointer loop (design).
- **Documented mechanisms fix unattended states.** Background tabs are measured past Chromium's documented intensive-throttling grace; the Steam client is measured with its window shown, which a game covering it would not change, since Linux Chromium tracks no cross-application occlusion (its minimised state measured beside it); the chat client idles on the Matrix 30 s `/sync` long poll; the session is left untouched until its 300 s idle delay locks the screen and blanks the monitor.
- **Real inputs and links where the work depends on them.** Déjà Dup's incremental and 7-Zip read Matt Mahoney's 10 GB benchmark set, 79,431 files from one laptop (`mahoney-10gb`), the incremental after seven days of Cumulus's personal-machine change rates (`vrable-fast09`); Tracker indexes HippoCamp's Bei profile placed as a home's `~/Documents` (`hippocamp`); HandBrakeCLI transcodes Big Buck Bunny's 4K edition (`big-buck-bunny`) to 1080p at its default preset (`handbrake`), CpsMark+'s transcode with the codec and target its code names (`cpsmarkplus`); the training run is PyTorch's basic MNIST example at its defaults (`pytorch-examples`); Kdenlive exports the `video-editor` project at its shipped default profile (`kdenlive`); the unattended upgrade installs the glibc security update Ubuntu published on 2026-07-27 (`unattended-upgrades`, `glibc`); DKMS rebuilds NVIDIA's open module for the security kernel of 2026-09-23 (`dkms`, `nvidia-open-kernel-modules`); SteamCMD installs a 10.4 GB depot over a link shaped to 121.0 Mbps, the byte-weighted median of Valve's per-country download rates (`steam-download-stats`), with an `fq_codel` queue (`fqcodel-rfc18`). The kernel build and the DKMS rebuild run `-j8`: the build tools' documented defaults follow `nproc`, here for an eight-thread desktop.
- **Steady behaviour, with the launch measured apart.** A settle precedes each measured idle or play phase. Where the traces cannot tell launch work from behaviour that recurs, one long probe of the phase (1,400–3,600 s) runs first: episodes that stop set the settle, episodes that recur lengthen the phase to hold them. Chrome settles 420 s, Thunderbird 390 s, the call 210 s, Kdenlive 240 s before a 180 s idle phase, the Steam client 900 s, the hidden renderers 1,030 s past the tabs' backgrounding; VS Code's idle phase is read from 200 s past its start. The launch itself is measured for ten entries — `office-writer`, `mail-client`, `video-editor`, `video-player`, `audio-player`, `chat-client`, `game-client`, `web-browser`, `renderer-hidden`, `video-call`: a warm relaunch traced from exec to the end of the entry's settle, carried per pooled repeat as replayed streams (§5). A task a file starts mid-file replays one of its entry's launch repeats, drawn by the file's seed, then runs its steady state; a task at 0 s starts steady, as the game chain always does, its source holding no launch data.
- **What no source states is labelled design** — the document length, the clip, the twelve renderers, the chat message rate, the attachment size, the home the indexer reads — and the scope says so.

## 5. What a run is turned into

- **Wake.** A schedule-in preceded by a wakeup of that thread since its last sleep. A resume after preemption is folded into the wake it continues.
- **Run.** The CPU time of one wake.
- **Gap.** Taken over a component's merged wake times and wrapped round the span observed, so a gap mean is exactly the span over the wakes and the rate a gap table implies is the rate measured.
- **Component.** One thread comm within one process role (`gpu/Chrome_ChildIOT`, `pid1/systemd`). Components are kept in descending wake rate until they cover 95 % of the phase's wakes; the rest is pooled as one residual. A component that does not wake at least twice in every repeat is reported as sporadic, not carried, unless it is carried as a sparse component (§7).
- **Table.** The ten pooled quantiles p1 … p99.9, the sample's minimum and maximum, and the measured mean of the samples in each interval, so a draw keeps both the quantiles and the sample's mean.
- **Per kind of entry.** A typing entry carries its per-input run: the tree's CPU from one input to the next, less the idle rate over that span. An operation carries its duration table and its components. A playback or call entry carries one periodic job per media cycle — its period and its per-cycle CPU. A build, batch or background program carries its runs between voluntary blocks and the block after each run.
- **Streams carried as recorded.** Beside the tables, three directories hold measured streams the compiler replays instead of drawing from a table; all 19 stream files are inputs of the core and generated manifests.
  - `dataset/stimulus/` — the three SWELL-KW streams (`swell-word-c1`, `swell-outlook-c23`, `swell-ie-c1`): every input event's time and kind of the named conditions in participant order, a segment or file boundary counted as one 2,000 ms gap, the rule and the source files recorded in `streams.json`; CC-BY-NC-SA-4.0, the DANS record's licence. The typing entries' input windows replay their keys. Written by `dataset/tools/stimulus/build_streams.py`.
  - `dataset/launch/` — the ten launch phases, one file per entry, five pooled repeats each, a repeat holding the whole tree's wakes or, for `renderer-hidden`, one stream per measured renderer: from `meas-ci:desktop:2026-10-04b`, `video-editor`'s from `meas-ci:desktop:2026-10-05` and `renderer-hidden`'s from `meas-ci:desktop:2026-10-05b`. Written by `dataset/tools/meas/desktop/launch_fold_in.py`, whose `--check` rebuilds them from the landings.
  - `dataset/replay/` — the `replay` sensitivity variants' six streams (§8), each one pooled repeat over its entry's carried phase, read from a named asset of its release: the wakes of `code-editor`, `web-browser` and `renderer-hidden`, `video-call`'s cycles, and the runs with the block after each of `cpu-batch`'s training run and `package-upgrade`, for a batch job the nearest repeat whose CPU covers the file's bind. Written by `dataset/tools/meas/replay_fold_in.py`, whose `--check` rebuilds them from the raw releases.

## 6. The stability rule

| element | what it says | ground |
|---|---|---|
| One CPU model | Only the AMD EPYC 7763 counts. A job that draws another model stops within about 20 s, before installing anything, and is not a repeat. Over the campaigns behind the dataset's values, 40–83 % of a campaign's jobs drew it. | `maricq-osdi18`: servers "with supposedly identical parts" differ run to run. Measured here: an Intel Xeon Platinum 8573C ran `cc1` at 0.72× and `fixdep` at 0.50× the EPYC's time. |
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
| Spread follows the machine | The value moves with the runner — its disk, its speed or its kernel's housekeeping — not the program: e.g. its run times move together across every thread of a repeat while wake rates hold within about 1 %. | `cpu-batch`'s `python3` runs between blocks and block per run (±27.3 %, ±10.8 %; the runner's `khugepaged`); `module-build-orchestrator`'s tail block per run (±8.35 %; dkms's progress loop and the runner's disk); `renderer-hidden`'s and `game-client`'s run means (±5.3–18.1 %) | With its half-width, range and count, over at least five repeats; only for a value no reported effect rests on |
| Varies between sessions | A window of the phase's length slid along one long run moves the value far less than it moves across repeats. | `code-editor`'s `utility/libuv-worker` (within one run ±10.6 %, across repeats ±39 %); `renderer-hidden`'s quiet threads `Chrome_ChildIOT`, `Compositor` and `PerfettoTrace` (±6.5–17.6 %); `service-manager`'s pid 1 run mean (±7.8 %); `message-bus`'s system bus (±11 %) | Its wake rate, gap mean and run mean together, with both spreads |
| Sparse component | It wakes only a few times a phase, so the spread is its count's own. | `renderer-hidden`'s residual (5.0–7.2 wakes per renderer per phase) | Its three values together, with its wake count stated |
| Rare event within a run | An event a repeat catches none, one or two times. | Chrome's `MemoryInfra` heavy pass (8 over 22,800 s of idle phase, about one per 47 min); the Steam client's HTTP burst | The event's runs above a stated threshold leave the component and are carried as separate events at their pooled rate |
| Recording runs out | A phase replays recorded input and the recording has no further window. | `mail-client`'s input and send (the Outlook recording's 8 windows; per-input mean under SWELL-KW ±10.4 %, the send's `StreamTrans` run mean ±18.4 %); `web-browser`'s per-input mean (38 windows, ±5.9 %) | With its half-widths, every window the recording holds pooled |

Values of a few microseconds pass by the 1 µs floor rather than the 5 %: the block per run of `file-archiver`, `game-download`, `package-upgrade`, `video-transcoder` and `incremental-backup`, `kdenlive_render`'s in `cpu-batch`, the Steam client's `CJobMgr::m_Work` run mean. The exception-carried values are carried with their half-widths, not re-measured: the RQ0 gate spec's corner variants (`corner-low`, `corner-high`) set the values `dataset/variants.yaml` lists under `carried_values` to the bounds of their stated intervals on the judging files that hold them, and if that moves a judging file across the gate's threshold, the entry is re-measured at a count fixed in advance before the result is reported (the RQ0 gate spec's statement `re-measurement-contingency`).

## 8. Checks and controls

- **Validity per repeat**, before a repeat counts: the replay sent every event of its window; every operation completed; screenshots show the input landed where designed; the steady phase's 10 s profile shows no launch work; no harness process is in the measured tree; a shaped download went through the shaper. A failing repeat is left out with its reason, and the rule is read over the rest.
- **Wakes traced to their cause** (the session processes). Each wake of the four session entries is traced through its wakers; wakes caused by the harness or by software a stock Ubuntu 24.04 desktop does not run (`ubuntu-desktop-manifest`, `systemd-ubuntu`, `livecd-rootfs`, `netplan`) leave the components and are stated. Jobs bound to a clock time are stated as events, not carried.
- **The untraced control** (the interactive, playback, renderer, comms and session entries), finished 2026-09-27. Each phase those entries carried at that date ran twice in six jobs per subject, traced and untraced in alternating order, each thread's CPU time and switches read from `/proc`. Where a difference is resolved, a wake rate's ratio, untraced over traced, lies in 0.97–1.08, and a run mean's in 0.72–0.98: tracing lengthens some threads' runs. Each difference is stated in the archetype's notes; the carried values stay the traced ones. Three sets of carried phases were measured later, and the control did not run them: the ten launch phases (`meas-ci:desktop:2026-10-04b`, `meas-ci:desktop:2026-10-05`, `meas-ci:desktop:2026-10-05b`), `renderer-hidden`'s steady phase (`meas-ci:desktop:2026-10-05b`) and `video-editor`'s idle phase (`meas-ci:interactive:2026-10-05`). `renderer-hidden`'s stated ratios were read by the control on Google Chrome 153, on the steady phase `meas-ci:desktop:2026-09-20` measured (a 630 s grace-settle), not on the phase it now carries (Chrome 154, 1,030 s). The build campaign cross-checks perf against taskstats (1.005 for `cc1`); the download reads the cost of its socket tracing (0.975 of the CPU without it).
- **The stimulus-sensitivity check.** Each typing entry also replays transcription typing from the 136M Keystrokes data (`dhakal-chi18`) and compares per-input means, repeat by repeat: `office-writer` 1.12, `web-browser` 1.34, `mail-client` 0.91, `code-editor` not resolved. The archetypes carry SWELL-KW whatever the check shows; the ratio is stated in each scope.
- **Build mix.** Where the build cannot be pinned, the two builds' repeats are compared value by value against the first build's own spread; the few that differ are stated.
- **Time windows.** Every phase the interactive, playback, renderer, comms and session entries carry as components, operations or a periodic job is also read in 100 s windows (20 s for a phase under 300 s); where part of the work happens only in part of the phase, the scope says so. The carried values stay the phase means. `video-editor`'s idle phase is the exception: it was read on `meas-ci:interactive:2026-09-18`, and its current pool, `meas-ci:interactive:2026-10-05`, is not yet read.
- **Spans longer than the phase.** Where a core file holds an entry longer than its measured phase, a long-phase probe reads the entry over that span: `office-writer`'s idle phase over 1,429 s (`c3-workday`), `video-editor`'s pointer loop over 4,758 s (`c1-transcode`), `code-editor` over 12,068 s (`c6-dual`), the hidden renderers over 3,600 s. `video-editor`'s idle phase is read over 2,790 s past its 240 s settle, 61 s short of the 2,851 s `c3-creation` holds it past its launch phase (from 360.6 s to 3,212 s). Each reading is stated in the entry's scope; the probes are never repeats. `web-browser`'s idle phase in `c3-workday` rests on the probe that set its 420 s settle, which holds 1,610 s past that settle.
- **Compile fidelity.** Tests check that a table's draws keep its mean, that each component's gap table implies its measured wake rate within 2 %, and that each measured archetype compiles at the wake rate it carries, within 5 % or four standard errors of the count (`feller-ipta50`). The compiled streams keep each component's rate, gap and run distributions, but not the order of its gaps, its components waking together, or a rare event's clustering: a rare event's runs are placed one by one at their rate, so `game-client`'s `CHTTPClientThre` burst of 12–18 runs within about 3 s is not carried. A stated threat to validity: at 1–100 ms, measured wake counts are more dispersed than compiled ones. The dispersion ratio, measured over compiled, median over the carried repeats (`dataset/tools/meas/burstiness.py`, read 2026-09-27): `chat-client` 3.3–11×, `code-editor` 2.6–3.4×, `web-browser` 2.8–3.4×, `mail-client` 1.9–3.0×, `game-client` 1.9–3.0×, `video-editor` 1.3–1.4×, `renderer-hidden` 1.06–1.15×; about 1 for `audio-server`, `service-manager` and `message-bus`; below 1, the compiled stream the burstier, for `compositor-shell` (0.86–0.97) and `office-writer` (0.60–0.91). `video-editor`'s figure was read on its idle phase of `meas-ci:interactive:2026-09-18` and `renderer-hidden`'s on `meas-ci:desktop:2026-09-20`; their current pools, `meas-ci:interactive:2026-10-05` and `meas-ci:desktop:2026-10-05b`, are not yet read. The `replay` sensitivity variants (`dataset/variants.yaml`) rebuild four judging files on one pooled repeat's measured sequence in place of the compiled streams, and the RQ0 gate spec's trace-replay check reads whether each file's verdict holds under both.

## 9. Campaigns at a glance

A repeat index relaunched in more than one run can land more than once, and every landing is pooled: `chat-client`'s 18 hold repeat 17 twice, the DKMS pair's 26 landings hold repeats 7, 10 and 11 twice.

| archetype | repeats | stopped by | carried under an exception |
|---|---|---|---|
| `office-writer` | 14 | the rule | — |
| `code-editor` | 44 | window 44 of the Word recording's 57; every value the rule is read on holds at 44 | `utility/libuv-worker` (between sessions) |
| `mail-client` | idle 77; input and send 8 | idle: the rule; input and send: the Outlook recording's last window | input and send values (recording runs out) |
| `web-browser` | 38 | the Internet Explorer recording's last window | per-input mean under SWELL-KW (recording runs out); `MemoryInfra` (rare event) |
| `image-editor` | 5 | the rule, at the minimum | — |
| `video-editor` | driven 20; idle 16 | the rule | — |
| `video-player` | 24 | the rule | — |
| `audio-player` | 31 | the rule | — |
| `video-call` | 45 | the rule | — |
| `build-orchestrator`, `compiler-child` | 14 | the rule | — |
| `module-build-orchestrator`, `module-compiler-child` | 26 landings of 23 repeats | the rule | the tail's block per run (machine) |
| `cpu-batch` | `python3` 6; `kdenlive_render` 30 | the rule | `python3`'s two block values (machine) |
| `video-transcoder` | 5 | the rule, at the minimum | — |
| `package-upgrade` | 9 | the rule | — |
| `file-indexer` | 18 | the rule | — |
| `incremental-backup` | 28 (of 30; repeats 12 and 25 fetched no input set) | the rule | — |
| `file-archiver` | 6 | the rule | — |
| `game-download`, `game-download-idle` | 30 | the rule | — |
| `renderer-hidden` | 5 | the rule, at the minimum | two run means (machine); quiet threads (between sessions); residual (sparse) |
| `chat-client` | 18 | the rule | — |
| `game-client` | 12 | the rule | four run means (machine); the HTTP burst (rare event) |
| `compositor-shell`, `audio-server`, `service-manager`, `message-bus` | 24, shared | the rule | pid 1's run mean and the system bus (between sessions) |

Raw records: the GitHub releases holding the campaigns whose values the library and the timelines carry, and the untraced control's. `dataset/meas-releases.yaml` maps each campaign tag to its releases, with each asset's SHA-256.

| release | holds |
|---|---|
| `meas-ci-2026-09-18` | `office-writer`, `image-editor`, `video-editor`'s phases with or after the input, `video-player`, `audio-player`; `mail-client`'s first 43 idle repeats |
| `meas-ci-2026-09-20` | `web-browser`, `video-call` |
| `meas-ci-2026-09-25` | `code-editor` |
| `meas-ci-2026-09-27` | `mail-client`'s input and send repeats |
| `meas-ci-2026-09-28` | `mail-client`'s 34 added idle repeats |
| `meas-ci-build-2026-09-18` | `build-orchestrator`, `compiler-child` |
| `meas-ci-background-2026-09-19` | `file-archiver`, `game-download` (and so `game-download-idle`) |
| `meas-ci-desktop-2026-09-20` | `chat-client`, `game-client` |
| `meas-ci-session-2026-09-24` | the four session entries |
| `meas-ci-control-2026-09-27` | the untraced control |
| `meas-ci-background-2026-10-01` | `package-upgrade` |
| `meas-ci-background-2026-10-02` | `module-build-orchestrator`, `module-compiler-child` |
| `meas-ci-background-2026-10-02b` | `file-indexer` |
| `meas-ci-background-2026-10-03` | `cpu-batch`'s `python3`, with the `madvise` check (§11) |
| `meas-ci-background-2026-10-03b` | `video-transcoder` |
| `meas-ci-background-2026-10-03c` | `cpu-batch`'s `kdenlive_render` |
| `meas-ci-background-2026-10-04` | `incremental-backup` |
| `meas-ci-desktop-2026-10-04` | the Chrome tab set: the number of hidden-tab renderers the files showing Chrome bind |
| `meas-ci-desktop-2026-10-04b` | the launch phases of the ten entries but `video-editor` and `renderer-hidden` |
| `meas-ci-interactive-2026-10-05` | `video-editor`'s idle phase |
| `meas-ci-desktop-2026-10-05` | `video-editor`'s launch phase |
| `meas-ci-desktop-2026-10-05b` | `renderer-hidden` and its launch phase |

The long-phase probes of §8 are in `meas-ci-probes-2026-10-05` and the upgrade probe beside the session in `meas-ci-probes-2026-10-07`; probes are never repeats and carry no value. `meas-ci-probes-2026-10-07b` is the class census: every thread's scheduling policy, real-time priority and nice over one dry job of each interactive, playback, desktop and session subject, never a repeat; those entries' declared class rests on it (§2; `_dev/research/jioh/task-9.11-scheduler-constants/classes/audit.md`). The runner's scheduler tunables (`meas-ci-sched-2026-10-07`) and the kernel-cost and LLM-latency campaign (`meas-ci-costs-2026-10-08`) hold no archetype value.

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
| `gh-artifact-retention` | why a campaign's release is made before 90 days pass |

The drive and the states:

| id | what it grounds |
|---|---|
| `swell-icmi14` | the replayed typing |
| `dhakal-chi18` | the sensitivity check's transcription typing only |
| `pcmark10`, `cpsmark-tbench23` | the operations' kinds, sizes and settings |
| `mahoney-10gb` | the backup and archive input set; its set check against `fm-results-tables` (GNU/Linux users' median file size) and `meyer-fast11` (half of the bytes in files over 30 MB, Windows, 2009) |
| `vrable-fast09` | the size of the change set before the incremental backup |
| `deja-dup`, `duplicity` | what the scheduled backup runs and its defaults |
| `hippocamp`, `tracker-miners` | the indexed home and what the indexer does |
| `pytorch-examples` | the training job |
| `kdenlive`, `mlt` | the export and its progress loop |
| `big-buck-bunny`, `handbrake`, `cpsmarkplus` | the transcode's clip, preset, codec and target |
| `unattended-upgrades`, `apt`, `glibc` | the unattended upgrade and the update it installs |
| `dkms`, `nvidia-open-kernel-modules` | the module rebuild and the module |
| `steam-download-stats`, `fqcodel-rfc18` | the download's link rate and why its queue is `fq_codel` |
| `glam` | one browser window and its five tabs, the tab-set campaign's drive |
| `ubuntu-desktop-manifest`, `systemd-ubuntu`, `livecd-rootfs`, `netplan` | what a stock Ubuntu 24.04 desktop holds and runs |
| `glean` | Thunderbird's daily 04:00 metrics thread, stated as a clock event |

Vendor and project documentation (Chromium's process model and throttling, the Matrix client-server spec, GNOME's idle defaults, the kbuild, GCC and make sources, Steam's content system) is cited in each measurement's search records. No literature value is carried as an archetype number: literature grounds the method, the drive and the states, and the numbers are the campaigns'.

## 11. What the values claim

Every measured value is this software on this machine: a GitHub-hosted runner, one pinned AMD EPYC 7763 core shared with the runner's own agent, no GPU, no display refresh, no sound device, no human, one CPU model over one period. The values are not desktop truth. The precision stated is precision on that configuration — reproducibility, a separate property from representativeness. Real-desktop validation is deferred.

- **The display.** The application entries were measured as X11 clients of Xvfb (Kdenlive's `QXcbEventQueue`, mpv with `--vo=x11`); the session entries in a Wayland session whose compositor is the display server, Xwayland started only on demand and not running at idle. No core file carries the desktop session beside an application (in the generated layer 62 files place the idle session's names beside applications as design composition, `docs/workload/building-plan.md` §3a); how each program would run on a Wayland desktop, natively or through Xwayland, is not observed.
- **Huge pages.** The runner's kernel runs transparent huge pages in `always` mode; Ubuntu 24.04's desktop kernel defaults to `madvise`. Under `madvise` the MNIST training run takes ×1.144 the CPU (95 % interval ×1.102–×1.185) and blocks only at its start — a venue effect measured on one entry; the other entries' sensitivity to the mode is unmeasured.
- **The CPU model.** Another CPU model changes each program's speed by its own factor: in the build campaign an Intel Xeon Platinum 8573C ran `cc1` at 0.72× and `fixdep` at 0.50× the EPYC 7763's time. A common factor does not represent such per-program ratios. The venue variants (`venue-x0.8`, `venue-x1.25`) scale every RUN but the game chain's by one factor, 0.8 (1/1.25) or 1.25 — a bracket holding the huge-page ratio above and the tracing overhead (×1.02–1.16), not another CPU model.
- **No GPU.** The training run is an actual training run on the CPU, not a claim that desktop users train MNIST; GPU training is unobservable on the runner.
- **Nice is not carried; the declared class is.** Over `game-download`'s 30 pooled repeats SteamCMD's content-update threads, at nice 10, do 75 % of its CPU (73.6–77.6 % per repeat), carried at full standing, so the simulated download interferes with the game in `c2-p2a` more than a stock desktop's would and the headroom there is inflated, in the hypothesis's favour. The pair `c2-p2a` (the download as measured, class `normal`) and `c2-p2a-idle` (the same tables under `game-download-idle`, class `idle`) bounds the limitation, the two bracketing a stock desktop; the RQ0 gate spec's bounding check reads them. `package-upgrade`'s nice-19 work (`apt-check` nearly all of it, 2.7 % of its CPU) is likewise carried at full standing.
- **The idle class and CPU groups.** On the depicted desktop the indexer's unit runs in `background.slice`, which gets about 23 % of the CPU against the editor's slice while both are runnable, since the idle policy acts only among siblings of one group: the simulated indexer, in the strict idle class, interferes with the editor less than the depicted one, and the headroom the indexer files can show is understated. The backup runs in the editor's own group, where the strict class matches the desktop. Neither carries the idle I/O class: the simulator schedules one CPU lane.
- **The compositions.** The core set's compositions are design, so the scheduling-benefit result holds on these compositions, which are not shown to be typical.

## Where to go deeper

| question | where |
|---|---|
| the rules a campaign follows, in full | `_dev/research/jioh/measurement-campaign-workflow.md` |
| every campaign's repeats, values, exceptions and machine draws | `_dev/research/jioh/measurement-campaign-record.md` |
| one domain's method and decisions | `_dev/research/jioh/task-9.<5–10>-*/campaign/` (`method.md`; 9.10's per campaign) and the slice's `changelog.md` |
| which tool runs, analyses, pools or folds in a campaign | `dataset/tools/meas/README.md` |
| where a campaign's raw records are | `dataset/meas-releases.yaml` |
| what one archetype carries and its stated limits | its entry in `dataset/archetypes.yaml` (`validation_stats.scope`, `modeling_notes`) |
| where a cited source says what | `docs/references.md` |
