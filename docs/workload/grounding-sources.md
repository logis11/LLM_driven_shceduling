# Workload Grounding — Sources by Role
> Status: normative · Created 2026-08-25 · Updated 2026-10-17

> Companion to the open-questions record's Q7 (segments, canonicalization, caches) and to the research proposal's §5.5 (Workloads). The suite is synthetic by necessity (see "The negative result" below); this document lists what grounds each layer of the synthesis. Each source is annotated with *what it is allowed to justify* — do not cite a source outside its role.
>
> **Normative homes (2026-08-26):** citation strings, tiers, and per-entry role lines live in **docs/references.md**; the machine registry is **dataset/sources.yaml**; the measurement campaign is **meas-ci** (docs/workload/building-plan.md §7). The A–D role letters remain this document's vocabulary for *what kind of grounding* a source provides.

## Role A — Scenario taxonomy: "these situations are standard, not imagined"

Grounds the *existence* of the scenarios behind the Families and modes: each source shows that a scenario exists in a shipped benchmark or system — never how common it is, nor which programs share a segment (the core set's compositions are design). The scenario catalog's Source column cites them per scenario (`docs/workload/scenario-catalog.md`). None of them provides process timelines.

| source | what it is | what it justifies |
|---|---|---|
| PCMark 10 (UL Solutions; `pcmark10`) | Scenario benchmark: Essentials (web browsing, video conferencing, app start-up), Productivity (spreadsheets, writing), Digital Content Creation (photo/video editing, rendering), Gaming; its Technical Guide documents each scenario's applications | The existence of the office, browsing, call, photo-editing, video-editing and video-playback scenarios; and the choice of the measured operations' inputs — GIMP's image and filter, the Kdenlive clip, the page kinds (`docs/workload/measurement-overview.md` §4) |
| SYSmark 30 / 25 (BAPCo; `sysmark30`, `sysmark25`) | Scenario benchmarks built from real commercial applications: SYSmark 30's Office Applications, General Productivity (OCR, browsing, application install, archiving), Photo Editing (filters, HDR, facial detection to group people) and Advanced Content Creation; SYSmark 25's (and SYSmark 2018's) Productivity, Creativity and Responsiveness, its Productivity description naming software development (code compilation) | A second, independent industry taxonomy beside PCMark 10, existence only; SYSmark 25's inclusion of *software development* is the compile Family's scenario precedent — that it is a mainstream desktop scenario is our inference |
| UL Procyon (`procyon`) | UL's suite of ten benchmarks, three of them local-AI inference (text generation, image generation, computer vision), beside office productivity and photo and video editing | A scenario-existence precedent only: local-AI inference scenarios exist in a shipped commercial benchmark. No dataset scenario rests on it; the training job is PyTorch's basic MNIST example (`pytorch-examples`) |
| CpsMark+ (Zhang & Wu, *BenchCouncil Transactions on Benchmarks, Standards and Evaluations* 2(4), the October 2022 issue, online 2023; `cpsmark-tbench23`) | Academic scenario-oriented office desktop benchmark; compares itself against SYSmark 2018 and PCMark 10 as state of the art | The *methodological* precedent: "scenario-oriented workload definition for desktop evaluation" is an accepted academic move, not just industry practice; the existence of the office, browsing, mail, photo, transcode and archive scenarios, and the transcode's definition with its HandBrake workload (`cpsmarkplus`); its CA workflow grounds the existence of the browsing → office → mail transitions, not an order |
| Game-mode systems (Windows Game Mode, macOS Game Mode, Feral GameMode), Steam's download setting, the CachyOS ananicy catalogue | Shipping systems' own categories and rules: a gaming mode; background work held back during play; a priority class per process name | The *gaming* category (`gamemode-docs`, `apple-gamemode`, `feral-gamemode`); background work held back during play by vendor rule — Windows Update's driver installs and restart notifications while a game runs in Game Mode (`xbox-gamemode`, dated by the Xbox Wire post of 2018-10-02), Steam's downloads pausing when a game launches (`steam-downloads`); and a per-name priority catalogue (`ananicy-rules`). None of them draws a wanted/unwanted-background distinction |

## Role B — Process behavior parameters: precedents, and LAVD's reported figures for the game chain

The library's per-process values are our own measurement (Role D), but for the game chain's, which are `lavd-ossna24`'s reported figures (the LAVD row). The other community tools below are precedents for the form of the task model and the metrics, existence only: none of them grounds a dataset value.

| source | what it is | what it justifies |
|---|---|---|
| rt-app (scheduler-tools; used by ARM and Linaro, per LWN) | Reproducible workload simulator; JSON specs of periodic tasks (period, runtime, deadline) | Our `pattern` schema is near-isomorphic to rt-app's task model — cite as the precedent for JSON-specified synthetic task behavior |
| interbench (Kolivas) | Emulates interactive tasks (audio, video, X, gaming) under background loads (Burn: CPU-bound threads; Write: streaming disk writes; compile-like), measuring latency, jitter, missed deadlines | The precedent for the *foreground-interactive + background-bulk* structure of Family 2 (same process set, different intent) only; it supplies no parameter values — its Audio/Video/X emulations are no longer cited by the dataset, and its gaming load uses as much CPU as it can get, with no deadlines |
| schbench (Mason, 2016) | Wakeup-latency benchmark reporting tail percentiles (P99): at v1.0 wakeup and request latency at p50/p90/p99/p99.9 and requests per second at p20/p50/p90 | Precedent for our latency metrics (tail-focused, not mean), and a citation precedent (SchedCP cites it); it grounds no archetype |
| hackbench | A benchmark and a stress test for the Linux kernel scheduler (many communicating tasks; LWN notes it is most often used for load-balancing changes); it reports one completion time | Existence only, cited for the contrast with schbench; it grounds no archetype |
| LAVD (Changwoo Min's OSS NA 2024 slides, `lavd-ossna24`; scx_lavd's source and README at `v1.1.3`, `scx`; LWN's reports of the LPC 2024 and 2025 talks, `corbet-lwn24`, `edge-lwn26`) | Min's reported characterization of gaming workloads (2024-04-17): around 300 tasks scheduled while a game runs, most long-lived; per-schedule runtimes of a few hundred µs on average to a few ms; tasks tightly linked in waiter–waker chains (Wine components, DXVK threads, PipeWire audio servers, task workers); scx_lavd motivated by reducing stutter | The game chain's reported values — per-schedule runtimes, chain length and member names (`game-task-chain`) — stated as Min's report with its date, the chain's form design; the chain's 16,667 µs frame period is the Steam Deck's 60 Hz refresh (`steamos-refresh`), not LAVD's. Also that desktop and gaming scheduling is a live production concern: Valve sponsors LAVD and ships it in SteamOS 3.8 as a scheduler the user selects, not enabled by default (`steamos-lavd`), and Meta's speakers presented it as a candidate default fleet scheduler (`dai-lpc25`) |
| stress-ng | A stress tool: its `--workload` stressor emulates bursty scheduled compute and its `--cyclic` stressor reports wake-latency percentiles; its README disclaims precise benchmarking | Existence only; it grounds no archetype |
| kernel build (make -jN) | A compile workload SchedCP's evaluation uses (kernel compilation, "make -j 172" on 6.14 tinyconfig, 1.79× over EEVDF) | The compile Family's short-lived structure: `ocallahan-atc17`'s "make forks and execs 2430 processes, mostly short-lived" (a `make -j8` build of DynamoRio 6.1.0, not a kernel build), otherwise the dataset's measured build (a warm `-j8` linux-6.6 build: 5,957 forks under 719 make processes, 2,857 six-member object jobs; `cc1_step_1` p50 367.6 ms; `meas-ci:build:2026-09-18`); SchedCP's "short-lived processes" is its Observation Agent's generated profile text. Also our canonicalization example (hundreds of cc1 children folding into one canonical app) |

## Role C — Segment structure and switching statistics: observed human timelines

Grounds the *Q7 layer*: how long segments last, how often labels change, what within-segment churn looks like. This is HCI territory, not systems territory — these sources have app names and human timelines, which no systems trace provides. The core set's segments are design or follow their measured jobs; of its segment and focus timing only `c6-dual`'s 688 s focus alternation inside its one segment rests on these sources (`gonzalez-chi04`). Otherwise they serve the naturalistic set (`docs/workload/building-plan.md` §4), whose generator is open. Hub-and-spoke switching is unsourced. No source gives sampled per-user segment-duration distributions.

| source | what it is | what it justifies |
|---|---|---|
| González & Mark, CHI 2004 (`gonzalez-chi04`) | A shadowing study of information workers; means and SDs | Segment durations in their units: about 3 min per event (one continuous use of a device or one interaction with a person) and 11 min 28 s as the mean continuous segment in a working sphere before switching, central and peripheral spheres only. `c6-dual`'s 688 s focus alternation is the 11 min 28 s |
| Mark, González & Harris, CHI 2005 (`mark-chi05`) | Its 24 informants include CHI 2004's 14; means and SDs | The companion figure, about 11 min (11 min 4 s) in a central or peripheral working sphere before switching or being interrupted; not an independent sample |
| Czerwinski, Horvitz & Wilhite, CHI 2004 (`czerwinski-chi04`) | A one-week self-report diary of user-defined tasks (10 people analysed), reporting means and SDs | Task-switch and interruption means; it is not a log study of app-switching distributions |
| SWELL-KW (`swell-icmi14`) | A lab dataset: computer logging with application names of 25 students and interns doing knowledge-work tasks, Windows 7, 2012, about three hours each; open under CC BY-NC-SA 4.0 | The typing entries' replayed keystroke stimulus (`docs/workload/measurement-overview.md` §4); a candidate observation for the naturalistic generator — its focus sequences (a dwell median of 9.1 s per focus episode, A → B → A returns after 83.4 % of middle episodes, the reader's computations) |
| BEHACOM (`behacom-dib20`) | Per-minute application-usage vectors of 12 users on their own computers (eight on Windows, three on Linux, one on both), 2019–2020: the foreground executable name and the switches between applications per minute | A candidate observation for the naturalistic generator, at minute resolution; existence and candidacy only |
| DesktopBench (in FOCAL, arXiv 2026, preprint; `focal-arxiv26`) | Multitask and interruption sessions with app names and window titles, composed from templates over VideoGUI's single-task actions, not observed; a fixed 6.0 s per action | The precedent for an evaluation shape only: the A → B → A interruption split, in which the interruption is a separately labelled task (a task switch), not a distractor inside one segment |

## Role D — Our own measurement: "this software on this machine"

Grounds every value of the 28 measured archetypes (`docs/workload/measurement-overview.md`). No external source: our own measurement campaigns, **meas-ci** — scripted re-enactments on public CI runners, the workflow files in the repository so anyone can re-run them, the raw records released (docs/workload/building-plan.md §7). A measured value is a source claim about this software on this machine — a GitHub-hosted runner pinned to one CPU of the AMD EPYC 7763 — never desktop truth.

User-behavioral parameters are not measured from users: the keystroke timing is a replayed SWELL-KW stream (Role C); the tab count and the one browser window are `glam`'s, a figure Firefox's Linux telemetry publishes; the core set's segment durations are design or the bound job's measured length (`docs/workload/building-plan.md` §3), Role C's figures serving `c6-dual`'s focus alternation and the naturalistic set. **Live-usage validation was not performed and is a stated limitation** (`docs/workload/measurement-overview.md` §11).

## The negative result — why the suite is synthetic (write this into §5.5's preamble)

State it as a finding, not an apology: **no public trace gives desktop process trees with names over time.** The nearest data that exists, and why each falls short:

| candidate | why it falls short for us |
|---|---|
| Enterprise / VDI / cloud workload traces (Azure, Google cluster traces, VDI characterization studies) | Server/VM granularity; no consumer applications; process identity absent or hashed |
| DARPA OpTC | Process-create events with image paths, from Windows 10 enterprise endpoints, not personal desktops |
| Desktop trace studies (older workload characterization literature) | Aggregate statistics survive; raw timelines with names were never released, largely for privacy (unsourced: no study is named) |
| HCI logging datasets (SWELL-KW, BEHACOM) | Foreground application names over time — SWELL-KW per keystroke in a lab, BEHACOM per minute from natural use on Linux and Windows — without the process-level detail (children, cgroups, background processes) the executor needs |

The absence is structural: process names are exactly the field privacy review strips, and process names are exactly what this research is about. One paragraph stating this converts "why is your dataset synthetic?" from a weakness into the motivation for the four-role grounding above — and for releasing our suite as an artifact (SchedCP's own evaluation notes that a complete benchmark remains future work).

## Anti-roles — sources that look relevant but must not be used as grounding

- **Phoronix Test Suite / UnixBench**: performance measurement of a machine, not scenario definitions; citing them as scenario grounding invites "you benchmarked the wrong thing."
- **Mobile app-usage datasets (launch prediction, screen-time)**: tempting for switching statistics, but mobile foreground-exclusivity makes the concurrency structure disanalogous to desktop multitasking; a reviewer who knows the dataset will catch it. Carat, whose samples list several running apps, is noted and not used.
- **The SchedCP evaluation workloads**: cite as related-work context, not as grounding — reusing them would concede the desktop framing.

## Citation-tier rule (style for the paper)

> Normative home now **docs/references.md** (each entry carries its tier and role line); the rule is restated here for the scope-discipline sentence.

Sources in this document fall into three citation tiers, and the paper must keep them visually and functionally separate:

1. **Scholarly citations** (numbered bibliography): peer-reviewed papers and archived preprints — CpsMark+, the Gloria Mark line, Czerwinski et al., SWELL-KW, BEHACOM, SchedCP, FOCAL, kernel-build characterizations.
2. **Deployed-system citations** (footnotes, URL + accessed date + pinned version/commit): product and artifact documentation — Windows Game Mode (Microsoft Learn, Xbox Support), macOS Game Mode, Feral GameMode, Steam client settings (Valve), the ananicy catalogue, SteamOS's release notes, sched_ext kernel docs, the scx repository, interbench/rt-app/schbench/hackbench/stress-ng repos, PCMark/SYSmark guides, UL Procyon's overview page, Firefox's telemetry (GLAM).
3. **Talk, conference abstract or news report** (footnotes, URL + accessed date): LAVD's OSS NA 2024 slides, LWN's reports, the LPC slides and abstracts.

Scope discipline: a deployed-system citation supports existence claims ("this scenario/setting/category exists in shipped software"); the system's own documented design or behaviour, stated as that source's at its pinned version or accessed date; and a figure the source publishes, stated as its report with the date read, the window and how it is computed — never a behavioural or statistical claim stated as the paper's own or as a population's. A talk's, conference abstract's or news report's claims are the speaker's or reporter's, a number stated only as its report with its date. If a sentence makes a claim about how often, how much, or how users behave, it needs a scholarly source or our own Role D measurement. This is the same artifact-scope rule as for interbench ("the community *models* interactivity this way", not "desktops *behave* this way"), applied uniformly.

## Standing verification tasks — resolved (2026-08-26)

1. ~~Task-switching study citation~~ — the task-switching log study (Zhang, Sun, Chai and Aghajan, 2015) was dropped on 2026-10-01 for want of a reachable copy; it has no docs/references.md entry.
2. ~~DesktopBench license/venue~~ — resolved: released on HuggingFace, restrictive data terms (research inspection only, no redistribution), MIT scripts; FOCAL still a preprint (`focal-arxiv26`).
3. Version pins — no docs/references.md entry these roles cite carries the `to-pin` status; `sysmark30` and `sysmark25` were read from the Internet Archive's capture of bapco.com's URL, their live URL to be pinned before submission.
4. ~~SWELL-KW~~ — `swell-icmi14` is in the registry: its keystroke streams are the typing entries' replayed stimulus (`dataset/stimulus/`), the DANS record open access under CC BY-NC-SA 4.0.
5. ~~Valve coordinates~~ — resolved: `steam-downloads` (Steam Support article 4F9E-6328-E9B8-47F9, accessed 2026-08-26).
