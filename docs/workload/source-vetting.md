# Source Vetting for the Synthetic Desktop Workload Dataset — rev. 2
> Status: record — append-only · Created 2026-08-25 · Updated 2026-10-17

> rev. 2 (2026-08-25): CpsMark+ upgraded from CONDITIONALLY USABLE to USABLE after full-text review — verdict, extracted content, role assignment, and recommendations revised accordingly. All other sections carried over from the original research report unchanged except where marked [rev.2].
>
> rev. 3 (2026-08-26): citation corrections from the verification pass (marked [rev.3]) — the task-switching study's authors, the true home of the Gloria Mark figures, and the identities of the two kernel-build arXiv papers. Final citations live in **docs/references.md**, which supersedes this document for citation strings; this document remains the vetting/extraction record.

## TL;DR
- Of the ~20 candidate sources, the strongest numeric grounding comes from the community scheduler tools (interbench, rt-app, schbench, hackbench) and the LAVD gaming characterization. The scenario-taxonomy sources (PCMark 10, SYSmark 30/25, CpsMark+) provide named scenario/application lists.
- [rev.2] CpsMark+ is now fully vetted and is the confirmed ACADEMIC ANCHOR: peer-reviewed, **open-source** (MCP at github.com/wanghong3116/CpsMarkPLUS; resource packages at the National Metrology Data Center of China), with a named-application taxonomy, ordered cooperative workflows, and per-workload hardware-sensitivity data. It contributes to Roles A, B (partially), and C (workflow ordering) — not Role A only.
- The highest-risk role remains Role C (segment/switching statistics): Gloria Mark's line gives averages ("~3 min per task, ~2 min per tool, ~12 min per working sphere") and the CNNIC 15M-log study gives power-law shapes, but no source provides sampled per-user segment-duration distributions.

## Key Findings
- Citing community open-source tools is normal practice; SchedCP (arXiv 2509.01245, MLforSystems @ NeurIPS 2025) cites schbench by git URL; interbench/hackbench/rt-app/stress-ng have LWN-documented or peer-reviewed usage precedents.
- interbench encodes reusable interactive constants: audio = 50 ms interval @ 5% CPU; video = 60 Hz (16.7 ms) @ 40% CPU; X = 0–100% variable; gaming = unbounded CPU.
- rt-app provides the canonical JSON task-model precedent (run/runtime, period, sleep, timer, deadline, loop, instance) in microseconds.
- LAVD (Changwoo Min, OSS NA 2024): ~300 tasks/game, ~90% long-lived, top 30–40 tasks = 95% of scheduling, per-schedule runtimes few-hundred-µs to few-ms (wineserver ~260 µs, worker ~1.65 ms), 70–75% of switches from waiting syscalls, 16.7 ms frame deadline / 15 ms targeted latency.
- [rev.2] The taxonomy sources converge on the same scenario families the team proposes, with one nuance: CpsMark+ itself criticizes SYSmark/PCMark methodology (subjective grouping, no cross-task cooperation, opaque scoring). The convergence claim must therefore be scoped to *scenario categories*, not methodology — e.g. "scenario-oriented desktop benchmarks, both academic [CpsMark+] and industry-standard [PCMark 10, SYSmark 30], converge on these scenario categories (while differing on methodology)."

## Details

### ROLE A — Scenario Taxonomy

#### A1. CpsMark+ — ACADEMIC ANCHOR — Verdict: USABLE [rev.2 — upgraded]
- **Accessibility [rev.2]:** Full text reviewed. Peer-reviewed in *BenchCouncil Transactions on Benchmarks, Standards and Evaluations* (Tbench), DOI 10.1016/j.tbench.2023.100084. **Open-source**: Master Control Program source at github.com/wanghong3116/CpsMarkPLUS; resource + third-party application packages at the National Metrology Data Center of China (jc.nmdc.ac.cn). Windows 10 only. The paper positions open-source vendor-neutrality as a design criterion, explicitly against the opacity of SYSmark/PCMark — strengthening its standing as the anchor citation.
- **Citation-ready:** Zhang, Y., & Wu, T. (2023). CpsMark+: A scenario-oriented benchmark system for office desktop performance evaluation in centralized procurement via simulating user experience. BenchCouncil Transactions on Benchmarks, Standards and Evaluations, 100084.
- **Extracted taxonomy [rev.2]:**
  - **Four usage scenarios**, merged into two modules: *Comprehensive Application* (CA = document manipulation + Internet service; light/middleweight, task & knowledge workers) and *Comprehensive Calculation* (CC = graphic design + multimedia processing; heavyweight, power users).
  - **User-profile tiers (Table 1):** Task workers / Knowledge workers / Power users, each with stated performance requirements — usable to stratify "whose machine is this" in workload authoring.
  - **Named applications with versions (Table 2):** PowerPoint/Word/Excel/Outlook 2016, Acrobat DC, WinRAR 5.91, Chrome 73, Photoshop CC 2019, AutoCAD 2018, 3ds Max 2018, Premiere Pro CC 2019, After Effects CC 2019, HandBrake CLI 1.3.0 — market-research-selected real process names for office/creation segment authoring.
- **Beyond Role A [rev.2]:**
  - **Role C contribution — ordered cooperative workflows:** CA workloads execute as a coherent user-behavior sequence (resource preparation via Internet → content creation → document processing → email delivery), with earlier workloads' outputs feeding later workloads' inputs (Office docs → Acrobat PDF conversion → WinRAR archive → Outlook attachment). Citable precedent for realistic *segment ordering* in Q7's workload-as-segment-list design.
  - **Role B contribution — resource-mix signatures (Table 4):** per-workload hardware sensitivity: CC workloads up to 1.77× sensitive to GPU while CA workloads are GPU-insensitive (~1.0×); Excel/WinRAR sensitive to CPU frequency and storage. Not burst-level timing, but quantitative grounding for assigning CPU-/GPU-/IO-bound resource mixes to synthetic processes — partially filling the office/web/creation parameter gap.
- **Caveats [rev.2]:** No gaming scenario (office-only) — gaming grounding still rests on PCMark Gaming + Game Mode + LAVD. No process-level burst/period numbers. Windows 10 applications — decide once whether the simulator's process names adopt these verbatim or map to Linux equivalents, and state the choice.

#### A2. PCMark 10 (UL Solutions) — Verdict: USABLE
- Public Technical Guide PDF (UL/Futuremark S3). Scenario groups: Essentials (Web Browsing, Video Conferencing, App Start-up), Productivity (Spreadsheets, Writing), Digital Content Creation (Photo Editing [ImageMagick], Video Editing, Rendering & Visualization), Gaming (2× GPU, Physics CPU, Combined). Applications benchmark uses Microsoft Edge and Office. Grounds five of six proposed families; documents activity composition, not per-process timing.

#### A3. SYSmark 30 / SYSmark 25 (BAPCo) — Verdict: USABLE (taxonomy only)
- Public User Guides/whitepapers; benchmark itself commercial. Scenario/application lists documented separately from scoring methodology, so taxonomy can be cited without touching contested scoring. **SYSmark 30 primary** (2022, User Guide v1.1 2024): Office Applications (Word/Excel/PowerPoint/Outlook 2021), General Productivity (Acrobat, Audacity 2.3.2, WinZip 26, Chrome 106; OCR, browsing, app install, archiving), Photo Editing (Lightroom Classic 11, Photoshop CC 23), Advanced Content Creation (Photoshop + Premiere CC 22; includes a multitasking workload switching between photo and video editing). **SYSmark 25 secondary**: adds software development (code compilation) and a Responsiveness scenario. 2011 AMD/Nvidia/VIA departure concerned scoring weights, not scenario lists — state this explicitly in the paper.

#### A4. UL Procyon — Verdict: CONDITIONALLY USABLE
- Adds a local AI-inference desktop scenario beyond PCMark 10. Public docs are light on internals; scenario-existence citation only.

#### A5. Windows Game Mode + ananicy/ananicy-cpp — Verdict: USABLE
- **Game Mode:** Microsoft Learn Game Mode portal + `<expandedresources.h>` APIs (GetExpandedResourceExclusiveCpuCount, SetProcessDefaultCpuSets, ReleaseExclusiveCpuSets, HasExpandedResources). Documented: foreground game granted exclusive/priority resource access; must be foreground and focused; CPU exclusivity + GPU prioritization; background preemption reduced; updates/notifications deferred.
- **ananicy:** Original github.com/Nefelim4ag/Ananicy (GPL); ananicy-cpp at gitlab.com/ananicy-cpp/ananicy-cpp (GPL-3.0, ~1.2.0). JSON rules in /etc/ananicy.d/*.rules: name, type, nice [-20..19], latency_nice, sched {fifo,rr,normal,batch,idle}, ioclass, ionice, oom_score_adj, cgroup. Example: {"name":"gcc","type":"Heavy_CPU","nice":19,"ioclass":"best-effort","ionice":7,"cgroup":"cpu90"}. Community catalog: github.com/CachyOS/ananicy-rules (hundreds of process names; games via Proton/wine vs linux-native, compilers batch/idle, indexers ioclass idle, audio nice −11). Grounds the wanted/unwanted-background distinction and provides real process-name → priority-class mappings.

### ROLE B — Process Behavior Parameters

#### B1. interbench (Con Kolivas) — Verdict: USABLE
- github.com/ckolivas/interbench, GPL-2.0, v0.31 (pin master commit). Interactive tasks: **Audio** 50 ms intervals @ 5% CPU (also SCHED_FIFO variant); **Video** 60 receipts/s (16.7 ms) @ 40% CPU; **X** variable 0–100% (window-drag emulation); **Gaming** unbounded CPU, no deadlines; **Custom** user CPU%+interval. Background loads: None; Video; X; **Burn** (4 CPU-bound threads default); **Write** (streaming write, RAM-sized file); **Read** (RAM-sized file, cache-defeating); **Compile** (Burn+Write+Read, "heavy make -j4"); **Memload** (110% RAM); Hack (hackbench 50). Metrics: avg latency of met deadlines, jitter SD, max latency, %desired CPU, %deadlines met; ~7 ms human jitter threshold; 30 s default duration.

#### B2. rt-app (scheduler-tools) — Verdict: USABLE
- github.com/scheduler-tools/rt-app, GPLv2, libjson-c. JSON fields: instance, loop, run/runtime (µs), sleep (µs), timer{ref,period}, period, deadline; global{duration, calibration, default_policy OTHER/FIFO/RR/DEADLINE, pi_enabled, lock_pages, logdir}. doc/examples/template.json: wake every 100 ms, run 10 ms, SCHED_OTHER, 6 s. Precedent for JSON-specified synthetic task behavior.

#### B3. schbench (Chris Mason / Meta) — Verdict: USABLE
- github.com/masoncl/schbench (mirror on kernel.googlesource.com), pin v1.0. Message threads + worker threads; request = 2× usleep + matrix math; per-CPU spinlock. Reports wakeup latency, request latency, RPS as percentile distributions (20/50/75/90/95/99/99.5/99.9). Precedent for tail-focused metrics; cited by SchedCP by git URL.

#### B4. hackbench — Verdict: USABLE
- In rt-tests (github.com/jlelli/rt-tests, src/hackbench, GPL-2.0) and perf bench sched messaging. Pairs of tasks over sockets/pipes; defaults 10 groups × 40 fds = 400 tasks, 100 msgs × 100 B. Grounds many-task IPC burst archetype.

#### B5. scx_lavd / LAVD — Verdict: USABLE (richest gaming numbers)
- github.com/sched-ext/scx (GPLv2); OSS NA 2024 slides (Changwoo Min); LWN LPC 2025 coverage. ~300 tasks while gaming; ~90% long-lived; top 30–40 tasks = 95% of scheduling (15–20 game tasks take 60–70%); CPU util 65–95%; per-schedule runtime few-100 µs avg to few-ms max (wineserver ≈260 µs, worker ≈1.65 ms); 25–30% timer preemption vs 70–75% waiting syscalls (epoll, pipe_read, futex_wait); waiter–waker task chains (input→display); 16.7 ms frame budget, 15 ms targeted latency; Avg FPS ≈ throughput, Low-1% FPS ≈ p99.

#### B6. stress-ng — Verdict: USABLE (fallback archetype only)
- github.com/ColinIanKing/stress-ng, GPL-2.0. Generic CPU/VM/IO stressors; no behavioral timing.

#### B7. Kernel build (make -jN) — Verdict: USABLE
- Record-and-replay study [rev.3 — identified]: **O'Callahan et al., "Engineering Record and Replay for Deployability," USENIX ATC '17** (extended TR = arXiv 1705.05937; `ocallahan-atc17`): kernel build forks/execs **2,430 mostly short-lived processes** ("2430" in the paper, §4.3; next workload: 89). Build-systems paper [rev.3 — identified]: **Coetzee, Bhaskar & Necula** (arXiv 1203.2704, preprint/UCB TR only; `coetzee-arxiv12`): "the Linux kernel build's enormous number of short-lived processes" — kernel-build-specific, cite it that way. Kernel docs: sched_child_runs_first, SCHED_AUTOGROUP motivated by make -j. SchedCP benchmarks make -j172 on Linux 6.14. Grounds compile family: fork-heavy burst of short-lived cc1/ld/as + few long-lived make/linker.

### ROLE C — Segment Structure & Switching Statistics (highest risk)

#### C1. Task-switching log studies — Verdict: CONDITIONALLY USABLE
- **CNNIC study identified [rev.3 — authors corrected]:** **Zhang, T., Sun, X., Chai, Y., & Aghajan, H.** (not "Yun et al."), "A look at task-switching and multi-tasking behaviors…", Computers in Human Behavior 49, 237–244, 2015, DOI 10.1016/j.chb.2015.03.012 (`zhang-chb15`). 31 days, 3,000 subjects, 15M+ records, 16,406 distinct processes — all verified in the paper; power-law switching concentrated on **hub** tasks (the paper's term; "star" is our paraphrase); average PC-task switch ~every 3 minutes; dataset not released.
- **Gloria Mark line [rev.3 — attributions corrected against full texts]:** both headline figures — ~12 min per working sphere (~10 spheres/day) AND ~3 min per task / >2 min per tool — belong to **González & Mark, CHI 2004** ("Constant, Constant, Multi-tasking Craziness", `gonzalez-chi04`). CHI 2005 ("No Task Left Behind?", `mark-chi05`) carries the companion ~11-min figure and the internal/external interruption split. **CHI 2008 ("The Cost of Interrupted Work") contains neither figure** — it is the interruption-stress lab experiment; never cite it for the averages. The CHI 2014 rhythm-of-attention paper does **not** contain the "~half of switches self-initiated" claim. Czerwinski/Horvitz/Wilhite CHI 2004 diary study confirmed as stated. **The "23 min 15 s to resume" figure exists only in the 2006 Gallup interview (`mark-gallup06`) — verified absent from all the peer-reviewed papers; cite the interview explicitly or omit.**
- Use for segment-duration means and heavy-tailed switching shape; exact distribution parameters must be fitted/assumed and flagged.
- [rev.2] Supplemented by CpsMark+'s ordered cooperative workflow (see A1) as a citable precedent for *which* segment orderings are realistic, complementing these sources' *how often* statistics.

#### C2. SWELL-KW — Verdict: CONDITIONALLY USABLE (qualitative)
- Koldijk et al., ICMI 2014, DOI 10.1145/2663204.2663257; data at DANS (DOI 10.17026/dans-x55-69zp), request/registration required. 25 participants, knowledge-work tasks under interruption/time-pressure conditions; computer logging present but oriented to stress/task-recognition. Practically a qualitative citation unless raw logs are requested and reverse-engineered.

#### C3. DesktopBench (in FOCAL, arXiv 2604.19541, 2026) — Verdict: USABLE (check release/license)
- Provenance correction: DesktopBench is the benchmark inside the FOCAL paper, reconstructed from VideoGUI. Actions carry foreground app name + window title. Splits: Multitask (320 sessions, 20 interleaved cross-app templates) and Interruption (100 sessions, controlled A→B→A: long creative task interrupted by short YouTube browsing). Closest artifact to the intended app-name + A→B→A structure; arXiv preprint — verify dataset release, license, venue before depending on sessions.

### CROSS-CUTTING ITEM 1 — Citation precedents for community artifacts
- schbench: cited by SchedCP (MLforSystems @ NeurIPS 2025) by git URL — confirmed. hackbench: "a stalwart of kernel scheduler testing" (LWN survey, Articles/725238); in perf + rt-tests. rt-app: referenced in kernel deadline docs and EAS/scheduler papers. interbench: packaged in Debian/Gentoo/FreeBSD; scheduler-interactivity literature. stress-ng: widely cited in systems/energy papers. ananicy: distro-wiki documented; pair with Game Mode as the "deployed systems already act on this" citation. Verdict: citing community tools by git URL + pinned commit is established practice.

### CROSS-CUTTING ITEM 2 — Version pinning
- interbench github.com/ckolivas/interbench v0.31 GPL-2.0 · rt-app github.com/scheduler-tools/rt-app GPLv2 · schbench github.com/masoncl/schbench v1.0 · hackbench in github.com/jlelli/rt-tests GPL-2.0 · stress-ng github.com/ColinIanKing/stress-ng GPL-2.0 · ananicy-cpp gitlab.com/ananicy-cpp/ananicy-cpp GPL-3.0 (rules: github.com/CachyOS/ananicy-rules) · scx_lavd github.com/sched-ext/scx GPLv2 · [rev.2] CpsMark+ MCP github.com/wanghong3116/CpsMarkPLUS (pin commit) + NMDC resource package.

## Recommendations
1. [rev.2] **Anchor confirmed:** cite CpsMark+ as the academic anchor (peer-reviewed, open-source, deployed in a real procurement with one-year user validation), PCMark 10 + SYSmark 30 for breadth, SYSmark 25 for compile, Procyon optionally for local-AI. Scope the convergence sentence to *scenario categories*, noting methodological differences, since CpsMark+ criticizes SYSmark/PCMark methodology directly.
2. [rev.2] **Borrow CpsMark+'s named app list (Table 2)** for office/creation segment authoring, and its CA workflow ordering (Internet → creation → document processing → email) for Q7 segment sequences. Decide once whether app names are used verbatim (Windows names) or mapped to Linux equivalents, and record the decision.
3. **Process parameters:** interactive fields from interbench (50 ms/5%, 16.7 ms/40%, X 0–100%); gaming from LAVD; rt-app JSON schema as the task-spec precedent; hackbench + kernel-build (2,430 short-lived procs) for compile/IPC. [rev.2] Use CpsMark+ Table 4 sensitivity signatures to assign CPU/GPU/IO resource mixes for office/web/creation processes.
4. **Segment structure:** means from Gloria Mark (3 min / 2 min / 12 min), heavy-tailed shape from CNNIC, A→B→A interruptions per DesktopBench, ordering per CpsMark+ CA workflow. Document that these are averages/shapes, not sampled distributions.
5. **Version-pin everything** per Cross-Cutting Item 2 at submission time.
6. **Upgrade triggers:** raw SWELL-KW or CNNIC per-user logs would upgrade C1/C2 and reduce Role D's burden. [rev.2 — CpsMark+ full text obtained; its trigger is resolved.]

## Caveats and Gaps (where Role D must compensate)
- No public desktop process-timeline trace with process names exists — confirmed; synthesis justified.
- Segment-duration and switch-frequency **distributions** still unsourced (averages and power-law shapes only) — Role D must measure.
- SWELL-KW / CNNIC raw logs not turnkey — request/registration + reverse-engineering.
- Per-process burst/period numbers for office/web/creation remain undocumented; [rev.2] CpsMark+ Table 4 narrows this to *resource-mix ratios* but burst timing still requires Role D. Gaming and audio/video remain the best-covered families.
- [rev.2] CpsMark+ has no gaming scenario and is Windows-10-only — cross-platform naming decision required.

## Summary Verdict Table
| Source | Role | Verdict | Basis |
|---|---|---|---|
| CpsMark+ | A anchor (+B mix, +C ordering) | **Usable** [rev.2] | Full text reviewed; open-source; named apps; workflow ordering; sensitivity table |
| PCMark 10 | A | Usable | Public tech guide; scenario+app lists |
| SYSmark 30 | A | Usable | Public user guide (primary) |
| SYSmark 25 | A | Usable | Adds compile/responsiveness |
| UL Procyon | A | Conditionally usable | Local-AI scenario; light internals |
| Windows Game Mode | A | Usable | MS Learn API docs |
| ananicy / ananicy-cpp | A | Usable | Public rules catalog |
| interbench | B | Usable | Hard constants |
| rt-app | B | Usable | JSON task-model schema |
| schbench | B | Usable | Tail-latency model; SchedCP precedent |
| hackbench | B | Usable | IPC task model, defaults |
| scx_lavd / LAVD | B | Usable | Richest gaming numbers |
| stress-ng | B | Usable | Fallback only |
| Kernel build | B | Usable | 2,430 short-lived procs |
| CNNIC 15M-log study | C | Conditionally usable | Shapes, no sampled dists; data unreleased |
| Gloria Mark line | C | Usable | Concrete averages |
| SWELL-KW | C | Conditionally usable | Access-gated; qualitative |
| DesktopBench (FOCAL) | C | Usable | app+title, A→B→A; verify release |

## Correction (2026-10-17)

Citation strings, pins and roles are `docs/references.md`'s; the roles the sources play now are `docs/workload/grounding-sources.md`'s.

**Header and overview**

- **Line 1** ("rev. 2"): the record's last revision is rev. 3 (line 6).
- **Line 9** ("the strongest numeric grounding comes from the community scheduler tools (interbench, rt-app, schbench, hackbench) and the LAVD gaming characterization"): no community scheduler tool grounds a dataset value. The library's values are the project's own measurement campaigns (`meas-ci`), but for the game chain's per-schedule runtimes, chain length and member names, which are `lavd-ossna24`'s reported figures of 2024-04-17, the chain's form design.
- **Lines 10, 25, 93** (CpsMark+ "open-source"): the paper publishes its control program's source and its resource packages and names open source as a design criterion, but states no software licence, and the GitHub repository has no licence file (the 2026-09-13 verification, C-cpsmark-8). The source is pinned at `bf24434` (`cpsmarkplus`).
- **Line 10** ("contributes to Roles A, B (partially), and C"): CpsMark+ grounds existence only — of the office, browsing, mail, photo, transcode and archive scenarios, and of the transcode's definition with its HandBrake workload. Its CA workflow grounds the existence of the browsing → office → mail transitions, not an order, `c3-workday`'s order being design; its Table 4 grounds no dataset value.
- **Lines 11, 76, 96** (the Gloria Mark figures, "~3 min per task, ~2 min per tool, ~12 min per working sphere"): González & Mark 2004's ~3 min is per *event* — one continuous use of a device or one interaction with a person, observed by shadowing, formal meetings excluded — not per task; its ~12 min is 11 min 28 s, the mean continuous segment in a working sphere before switching, central and peripheral spheres only (13 min 49 s over all spheres; the paper's average time per working sphere is 33 min 32 s).
- **Lines 11, 96, 98, 102, 103** (the CNNIC study's power-law, heavy-tailed switching shape): the study (`zhang-chb15`, Zhang, Sun, Chai and Aghajan, *Computers in Human Behavior* 49, 2015) was dropped on 2026-10-01 for want of a reachable copy, and its registry and `docs/references.md` entries left; the switching shape these lines take from it is unsourced.
- **Line 14** ("SchedCP … cites schbench by git URL"; "interbench/hackbench/rt-app/stress-ng have LWN-documented or peer-reviewed usage precedents"): SchedCP cites schbench at kernel.googlesource.com, not by its GitHub URL. The precedent holds for hackbench and rt-app (LWN 725238) and as an LWN mention for stress-ng (LWN 1051430); none was found for interbench.
- **Line 15** (interbench's "reusable interactive constants"): interbench's interactive constants (audio 50 ms at 5 %, video 16.7 ms at 40 %, X 0–100 %) ground no dataset value: the interactive entries' parameters are the measured campaigns of the nine per-application entries (`office-writer`, `code-editor`, `mail-client`, `web-browser`, `image-editor`, `video-editor`, `video-player`, `audio-player`, `video-call`).
- **Line 16** (rt-app's "canonical JSON task-model precedent … in microseconds"): `loop` and `instance` are counts, not µs, and "canonical" is not in the source.
- **Line 17** (LAVD): the ~300 tasks are scheduled system-wide while a game runs, system tasks included, not "per game"; 260 µs (wineserver) and 1.65 ms (a task worker) are two named examples of "a few 100s usec on average to a few msec maximum", not a range's ends; 70–75 % of scheduling events are initiated by waiting system calls and 25–30 % by preemption (e.g. a timer interrupt); the deck states no frame period, frame budget or deadline — its 15 ms is an example scheduler targeted latency for time slices. The game chain's 16,667 µs frame period is the Steam Deck's 60 Hz default refresh (`steamos-refresh`), a design value.
- **Line 18** (CpsMark+'s criticism): "subjective grouping, no cross-task cooperation" is said of SYSmark 2018 only; PCMark 10's criticism is its equal-weight geometric-mean scoring; opacity is said of both.

**Role A**

- **Line 30** (Table 2 as "real process names"): Table 2 lists application product names and versions, not process names. The dataset's names are the kernel `comm`s its campaigns traced, or derived by the `comm` rule (`docs/workload/scenario-catalog.md`, note 4).
- **Line 32** (the CA workflow's handoffs; its last sentence, the workflow as a "Citable precedent for realistic *segment ordering*"): only Acrobat's input is stated as earlier outputs (PowerPoint, Word and Excel to PDF); "→ WinRAR archive → Outlook attachment" is not stated, and the paper hedges to "some specific applications". The workflow grounds the existence of the browsing → office → mail transitions, not an order (line 10).
- **Line 33** (Table 4; its last sentence, Table 4 as "quantitative grounding for assigning CPU-/GPU-/IO-bound resource mixes to synthetic processes"): the CC workloads reach 1.79× at the best graphics card (1.77× is the CC module's figure); all workloads are highly sensitive to CPU frequency and storage, Excel and WinRAR only more so. Table 4 assigns no resource mix: every per-process value of the library but the game chain's is measured (line 104).
- **Line 34** ("gaming grounding still rests on PCMark Gaming + Game Mode + LAVD"): no row of the scenario catalog cites PCMark 10's Gaming group (the catalog's note 1; `pcmark10`'s role). The catalog's gaming row cites `lavd-ossna24`'s reported trace for the game chain's threads and the measured Steam client (`meas-ci:desktop:2026-09-20`); the game-mode systems ground the gaming category (`gamemode-docs`, `apple-gamemode`, `feral-gamemode`).
- **Lines 34, 94, 105** (the naming decision left open): decided — a task's name is its process's kernel `comm`, Linux-native.
- **Line 37** ("Grounds five of six proposed families"): the fit judgement is the project's, not the guide's.
- **Line 40** (SYSmark): the 2011 departures from BAPCo concerned SYSmark 2012, not SYSmark 30, and the reasons given include its workloads, not its scoring alone — AMD's CMO (Dessau's own post, 2011-06-21) named the weighting of SM2012's scores, its neglect of GPU-accelerated work and its unrepresentative workloads; VIA said its tests "do not accurately reflect real world PC usage scenarios and workloads"; Nvidia gave no reason. "Concerned scoring weights, not scenario lists" is contradicted, and "state this explicitly in the paper" is withdrawn: the paper cites SYSmark 30 for its scenario categories only. The separation itself holds (the scenario lists are in the user guide, the formulas only in the whitepaper), but "contested scoring" does not. The pinned edition is the v1.2 file (cover "Revision: 1.1", uploaded 2025-04), the 2022 release year from BAPCo's press release. SYSmark 25 "adds" nothing: software development and the Responsiveness scenario are already in SYSmark 2018, and both are absent from SYSmark 30.
- **Line 43** (Procyon): "light on internals" holds only for the product pages — the public knowledge-base user guide gives task steps, per-step metrics, input sizes and score formulas, and no per-process timing. The overview page lists ten benchmarks. No dataset scenario rests on Procyon.
- **Line 46** (Game Mode): "updates/notifications deferred" is not on the cited Learn pages — Microsoft's Xbox Support article says Game Mode prevents Windows Update from performing driver installations and sending restart notifications, dated by the Xbox Wire post of 2018-10-02 (`xbox-gamemode`); "background preemption reduced" is not stated; and `SetProcessDefaultCpuSets` is not an `<expandedresources.h>` function (the header documents three, the function only in a remark).
- **Line 47** (ananicy): upstream Ananicy is GPL-3.0 and archived (its last commit 2023-03-21). At the catalogue's pin (`03ef03fb`): `Player-Audio` is nice −4, nice −11 having existed only in 2022–2025 commits, on audio-server rules; only KDE's Baloo and Recoll are typed `BG_CPUIO` (nice 16, ioclass idle, sched idle), GNOME's Tracker and `updatedb` having no entry; "compilers batch/idle" is ananicy-cpp's README example `gcc` rule, the catalogue holding no compiler entries; it holds 15,811 distinct names, not hundreds. No type, comment or README text draws a wanted/unwanted-background distinction; the process-name → priority-class mappings stand.

**Role B**

- **Line 52** (interbench): the licence is GPL-2.0-or-later per the source headers (a GPLv3 LICENSE file also ships); the pinned master commit `e612a65` reports 0.31 but its load defaults differ from tag v0.31 — Burn defaults to the online CPU count, 4 being the man page's; the Video task "tries to receive cpu 60 times per second". Its "~7 ms" jitter figure is the program's own, stated without a source in its man page, readmes and code — not a human-perception threshold; no harness or metrics constant cites it. Its constants ground no dataset value (line 15).
- **Line 55** (rt-app): the policy set omits SCHED_BATCH and SCHED_IDLE; `period` and `deadline` are the legacy spellings of `dl-period` and `dl-deadline`. rt-app is pinned at `d6f8be4`.
- **Lines 57, 58** (schbench): its copyright is "(C) 2016 Facebook", GPLv2 (line 57). It is cited at git.kernel.org `mason/schbench`, tag `v1.0` (commit `ab22f3f8`, 2023-04-17), its only tag, the GitHub repository continuing the history without tags. At v1.0 it prints wakeup and request latency at p50/p90/p99/p99.9 and requests per second at p20/p50/p90, its 2016 first version p50/75/90/95/99/99.5/99.9: the listed 20/50/75/90/95/99/99.5/99.9 is printed by no version; v1.0 does one `usleep(100)` per request.
- **Lines 60, 61** (hackbench): it is read in rt-tests at git.kernel.org, tag `v2.11` (commit `62da2bef`), GPL-2.0-or-later per the source headers; the `github.com/jlelli/rt-tests` mirror was not read. It is existence only — a benchmark and stress test for the Linux kernel scheduler, cited for the contrast with schbench — grounding no archetype: no IPC archetype exists.
- **Line 64** (scx_lavd / LAVD): the LWN source is Jonathan Corbet's report of the LPC 2024 talks (`corbet-lwn24`, LWN 991205, 2024-09-26), not LPC 2025 coverage, which is Jake Edge's (`edge-lwn26`, LWN 1051430, 2026-01-07); `scx` is pinned at release `v1.1.3`; "25–30 % timer preemption" narrows the deck's "preemption (e.g., timer interrupt)"; the deck's figures as line 17 states them.
- **Lines 66, 67** (stress-ng): pinned at commit `3ac9d7a8`, GPL-2.0-or-later. It has behavioural timing — its `--workload` stressor "emulates bursty scheduled compute" and `--cyclic` reports wake-latency percentiles — and its README disclaims precise benchmarking. It is existence only, grounding no archetype, not a fallback archetype source.
- **Line 70** (kernel build): O'Callahan et al.'s 2,430 mostly short-lived processes are a `make -j8` build of DynamoRio 6.1.0, not a kernel build, and 89 is the next most prolific workload's (sambatest). `sched_child_runs_first` is in no kernel Documentation file; SCHED_AUTOGROUP's Kconfig help says "build jobs", not "make -j". "Short-lived cc1/ld/as + few long-lived make/linker" is in no cited source. The compile family is grounded in the dataset's measured build — a warm `-j8` linux-6.6 build, 5,957 forks under 719 make processes, 2,857 six-member object jobs (`meas-ci:build:2026-09-18`).

**Role C**

- **Lines 75, 124** (the CNNIC study): `zhang-chb15` is no usable Role C (segment-structure) source: dropped as the item for line 11 states, its figures and "all verified in the paper" cannot be reproduced from any text read.
- **Line 76** (the Gloria Mark line): besides the figures of line 11, Czerwinski, Horvitz and Wilhite's CHI 2004 study is a one-week self-report diary of user-defined tasks (10 people analysed), reporting means and SDs, not a log study of app-switching distributions; the 23 min 15 s figure is absent from the four Mark et al. CHI papers searched — "only" and "absent from all the peer-reviewed papers" go beyond that search — and CHI 2005 reports a comparable 25 min 26 s. `mark-chi08`, `mark-chi14` and `mark-gallup06` left `docs/references.md` on 2026-10-16; `czerwinski-chi04` stays, its role corrected to the diary study as stated here.
- **Line 77** ("Use for segment-duration means and heavy-tailed switching shape"): the heavy-tailed shape's source is dropped (line 11). No segment duration of the core set is a Role C mean: they are design or the bound job's measured length, and of the Gloria Mark means only `gonzalez-chi04`'s 11 min 28 s is used, as `c6-dual`'s 688 s focus alternation inside its one segment (line 102). No distribution is fitted; the distributions are the naturalistic set's to settle (line 102).
- **Line 78** (CpsMark+'s workflow as "a citable precedent for *which* segment orderings are realistic"): it grounds the existence of the browsing → office → mail transitions only, not an order; `c3-workday`'s order is design (line 10).
- **Line 81** (SWELL-KW): the DANS record is open access under CC BY-NC-SA 4.0, no request or registration needed; its participants are 25 students and interns doing knowledge-work tasks in a lab. Its keystroke streams are the typing entries' replayed stimulus (`dataset/stimulus/`), so it is no longer a qualitative citation.
- **Line 83** (DesktopBench): released on HuggingFace (`HaoranYin/desktopbench` v0.1.0), its data terms restrictive (research inspection only, no redistribution), its scripts MIT; FOCAL is still a preprint. Its sessions are composed from templates over VideoGUI's single-task actions, not observed, with a fixed 6.0 s per action, and its interruption is a separately labelled task, not a distractor inside one segment: it is cited only as the precedent for an evaluation shape.

**Cross-cutting items, recommendations and caveats**

- **Line 87** (citation precedents): interbench's packaging is Gentoo, FreeBSD ports, AUR, GNU Guix, openSUSE Leap, Void, AOSC and LiGurOS — no Debian package was found; "scheduler-interactivity literature" (interbench), rt-app's "EAS/scheduler papers" and stress-ng's "widely cited in systems/energy papers" name no paper and are unverifiable; schbench is cited by SchedCP at kernel.googlesource.com, as line 14 states; the peer-reviewed precedents found cite a repository URL with an access date, not a pinned commit.
- **Line 90** (version pinning): interbench at master `e612a65`, GPL-2.0-or-later; rt-app at `d6f8be4`; schbench at git.kernel.org tag `v1.0`; hackbench in rt-tests at git.kernel.org tag `v2.11`, GPL-2.0-or-later; stress-ng at `3ac9d7a8`, GPL-2.0-or-later; ananicy-cpp at `v1.2.0`, the CachyOS catalogue at `03ef03fb`; scx at release `v1.1.3`; CpsMark+'s source at `bf24434`, no licence stated.
- **Line 94** (recommendation 2, Table 2's app list "for office/creation segment authoring" and "its CA workflow ordering … for … segment sequences"): the dataset's names are the traced `comm`s, not Table 2's product names (line 30); the workflow grounds the transitions' existence, not the order of any segment sequence (line 10).
- **Line 95** (recommendation 3): the interactive fields come from the measured campaigns, not interbench (line 15); the game chain takes LAVD's figures as Min's report, its form design (line 9); hackbench grounds nothing (line 61), and the 2,430 processes are a DynamoRio build (line 70); CpsMark+'s Table 4 assigns no resource mix — every per-process value but the game chain's is measured.
- **Line 96** (recommendation 4): the Gloria Mark means in their units (line 11); no heavy-tailed shape (line 11); DesktopBench grounds an evaluation shape only (line 83); CpsMark+'s CA workflow grounds the transitions' existence, not an order (line 10).
- **Line 98** (recommendation 6): SWELL-KW's raw logs are open and in use (line 81); the CNNIC trigger is void (line 11).
- **Line 101** ("No public desktop process-timeline trace with process names exists — confirmed"): only the narrower claim holds — no public trace gives desktop process trees with names over time. BEHACOM publishes foreground executable names per minute from natural use on Linux and Windows, and DARPA OpTC process-create events with image paths on Windows 10 enterprise endpoints.
- **Line 102** ("Role D must measure" the segment and switch distributions): the measurement campaigns observe software on the runner, not users. The core set's segment durations are design or the bound job's measured length (`docs/workload/building-plan.md` §3), `c6-dual`'s 688 s focus alternation `gonzalez-chi04`'s mean; the distributions stay unsourced, the naturalistic set's to settle, its generator open (§4); the switching structure is unsourced.
- **Line 103**: SWELL-KW's data is open (line 81); the CNNIC logs' source is dropped (line 11).
- **Line 104** ("Per-process burst/period numbers for office/web/creation remain undocumented … Gaming and audio/video remain the best-covered families"): every per-process value of the library but the game chain's is the project's measurement, the office, web and creation applications included (`docs/workload/measurement-overview.md`).

**Summary Verdict Table**

- **Lines 110, 113, 114, 117, 119–127**: the role and basis columns read as corrected above — CpsMark+ is a Role A anchor for existence only, its "+B mix", "+C ordering", "workflow ordering" and "sensitivity table" void (line 10); SYSmark 25 adds nothing over SYSmark 2018 (line 40); Procyon grounds no dataset scenario (line 43); interbench's constants ground no value (line 15); schbench's SchedCP citation is at kernel.googlesource.com (line 14); hackbench, stress-ng and the kernel-build row ground no archetype (lines 61, 67, 70), the 2,430 processes a DynamoRio build; LAVD's numbers are Min's reported figures of a talk, footnote tier (line 17); the CNNIC study is dropped (line 75); the Gloria Mark averages are per event and per segment (line 11); SWELL-KW is open and replayed (line 81); DesktopBench is released and cited for an evaluation shape only (line 83).

**Role B and cross-cutting item 2**

- **Lines 55, 90** (rt-app, "GPLv2"): at the pin `d6f8be4`, read file by file on 2026-10-17, the nine `src/` files that carry a licence header grant GPL version 2 "or (at your option) any later version" (GPL-2.0-or-later); `libdl/dl_syscalls.h` grants version 2 only; `src/rt-app_taskgroups.c`, `src/rt-app_taskgroups.h` and `libdl/dl_syscalls.c` carry no header; `COPYING.in` is the GPL version 2 text.
