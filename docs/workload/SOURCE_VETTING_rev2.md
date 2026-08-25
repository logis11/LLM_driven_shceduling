# Source Vetting for the Synthetic Desktop Workload Dataset — rev. 2

> rev. 2 (2026-08-25): CpsMark+ upgraded from CONDITIONALLY USABLE to USABLE after full-text review — verdict, extracted content, role assignment, and recommendations revised accordingly. All other sections carried over from the original research report unchanged except where marked [rev.2].

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
- Record-and-replay study (arXiv 1705.05937): kernel build forks/execs **2,430 mostly short-lived processes** (next workload: 89). Build-systems paper (arXiv 1203.2704): "enormous number of short-lived processes." Kernel docs: sched_child_runs_first, SCHED_AUTOGROUP motivated by make -j. SchedCP benchmarks make -j172 on Linux 6.14. Grounds compile family: fork-heavy burst of short-lived cc1/ld/as + few long-lived make/linker.

### ROLE C — Segment Structure & Switching Statistics (highest risk)

#### C1. Task-switching log studies — Verdict: CONDITIONALLY USABLE
- **CNNIC study identified:** Yun et al., "A look at task-switching and multi-tasking behaviors…", Computers in Human Behavior, 2015. 31 days, 3,000 subjects, 15M+ records, 16,406 distinct processes; power-law switching, hub/star task structure; dataset not released.
- **Gloria Mark line:** CHI 2005 (~12 min per working sphere, ~10 spheres); CHI 2008 "The Cost of Interrupted Work" — "about three minutes on a task, somewhat more than two minutes using any electronic tool" before switching; CHI 2014 rhythm-of-attention (~half of switches self-initiated); Czerwinski/Horvitz/Wilhite CHI 2004 diary study. **The "23 min 15 s to resume" figure traces to a 2006 Gallup interview, not a peer-reviewed paper — cite the interview explicitly or omit.**
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
