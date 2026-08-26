# REFERENCES — master citation index

The single index answering "what do we cite, in what form, for what claim." One id namespace across the whole project: these ids are the `source:` tag prefixes in the dataset (via `workload-dataset-sources.yaml`) and the bibkeys in the paper. This file owns every citation string and every citation-constituent field (`url`, `accessed`, `pinned_version`); the yaml registry holds machine/derivation fields only and must be a subset of this index (lint: every yaml id has an entry here; entries here without a yaml counterpart are paper-only references).

## Id-minting rule

**Entry unit: one citable artifact** — the thing that gets exactly one citation, one URL, one accessed date. A project with several citable artifacts (paper + slides + repo) gets several entries.

Id derivation by `type`:

- **scholarly** → `<label>-<venue><yy>` — label is the first-author surname, or the system name when the work is universally known by it (`cpsmark-tbench23`, `lavd-ossna24`). arXiv-only works use `arxiv` in the venue slot (`focal-arxiv26`). Raw arXiv numbers are banned as ids — they live in the citation.
- **deployed-system** → project name, no year; `pinned_version` carries freshness (`interbench`, `rt-app`, `steam-downloads`).
- **measurement** → `meas-ci`, with run identification in the locator (`meas-ci:<workflow>:<run>`).

**Contributor recipe:** (1) read this rule and mint the id; (2) add the entry here; (3) add a `workload-dataset-sources.yaml` entry *only if the dataset derives values or structure from it*.

## Citation-tier rule

- **scholarly** → numbered bibliography. May support empirical, behavioral, and statistical claims within its stated role.
- **deployed-system** → footnote with URL + accessed date + pinned version. Supports **existence claims only** ("this scenario/setting/category exists in shipped software") — never behavioral or statistical claims.
- An entry's `role:` line states what claims it may support; do not cite outside the role.

Status legend: `verified` (coordinates confirmed against primary sources, date given) · `to-pin` (identification certain; exact URL/version to pin before submission) · `provisional` (identification incomplete — do not cite until resolved).

---

## Grounding — scholarly

### `cpsmark-tbench23`
- cite: Zhang, Y., & Wu, T. (2023). CpsMark+: A scenario-oriented benchmark system for office desktop performance evaluation in centralized procurement via simulating user experience. *BenchCouncil Transactions on Benchmarks, Standards and Evaluations*, 100084. DOI 10.1016/j.tbench.2023.100084.
- role: Role A academic anchor — scenario taxonomy, named app lists (Table 2), CA workflow ordering (Role C), resource-mix sensitivity (Table 4, Role B). Open-source artifact: github.com/wanghong3116/CpsMarkPLUS (pin commit) + NMDC resource package.
- status: verified (SOURCE_VETTING_rev2 full-text review, 2026-08-25)

### `zhang-chb15`
- cite: Zhang, T., Sun, X., Chai, Y., & Aghajan, H. (2015). A look at task-switching and multi-tasking behaviors: From the perspective of the computer usage among a large number of people. *Computers in Human Behavior*, 49, 237–244. DOI 10.1016/j.chb.2015.03.012.
- role: Role C — power-law switching, hub task structure ("star" is our paraphrase — say "hub"), ~3-min average PC-task switch (independently corroborates `gonzalez-chi04`). 31 days / 3,000 subjects / 15M+ records / 16,406 processes, CNNIC data. Dataset unreleased.
- status: verified (2026-08-26; corrects SOURCE_VETTING's "Yun et al." misattribution)

### `gonzalez-chi04`
- cite: González, V. M., & Mark, G. (2004). "Constant, Constant, Multi-tasking Craziness": Managing Multiple Working Spheres. *Proc. CHI 2004*, 113–120. DOI 10.1145/985692.985707.
- role: Role C — THE home of both headline figures: ~12 min per working sphere (~10 spheres/day) AND ~3 min per task / >2 min per tool. (Our earlier docs attributed these to CHI 2005/2008 — wrong; repoint here.)
- status: verified (2026-08-26, against full text)

### `mark-chi05`
- cite: Mark, G., González, V. M., & Harris, J. (2005). No Task Left Behind? Examining the Nature of Fragmented Work. *Proc. CHI 2005*, 321–330. DOI 10.1145/1054972.1055017.
- role: Role C — ~11-min working-sphere companion figure; internal vs. external interruption split (managers 59.2%/40.8%).
- status: verified (2026-08-26)

### `mark-chi08`
- cite: Mark, G., Gudith, D., & Klocke, U. (2008). The Cost of Interrupted Work: More Speed and Stress. *Proc. CHI 2008*, 107–110. DOI 10.1145/1357054.1357072.
- role: Role C — interruption/stress lab experiment ONLY. Carries neither the 3-min nor the 12-min figure; never cite it for them.
- status: verified (2026-08-26)

### `mark-chi14`
- cite: Mark, G., Iqbal, S. T., Czerwinski, M., & Johns, P. (2014). Bored Mondays and Focused Afternoons: The Rhythm of Attention and Online Activity in the Workplace. *Proc. CHI 2014*, 3025–3034. DOI 10.1145/2556288.2557204.
- role: Role C — attentional rhythms by time of day. Does NOT contain the "half of switches self-initiated" claim (that lives in `mark-chi05` / `mark-gallup06`).
- status: verified (2026-08-26)

### `czerwinski-chi04`
- cite: Czerwinski, M., Horvitz, E., & Wilhite, S. (2004). A Diary Study of Task Switching and Interruptions. *Proc. CHI 2004*, 175–182. DOI 10.1145/985692.985715.
- role: Role C — diary-study evidence on task switching and interruptions.
- status: verified (2026-08-26)

### `dhakal-chi18`
- cite: Dhakal, V., Feit, A. M., Kristensson, P. O., & Oulasvirta, A. (2018). Observations on Typing from 136 Million Keystrokes. *Proc. CHI 2018*. DOI 10.1145/3173574.3174220.
- role: Role C (former D-live substitute) — input inter-arrival: mean inter-key interval 238.66 ms (SD 111.60). Scope limit: within-burst transcription typing only — no mouse, no think-pauses; grounds intra-burst gaps, not burst/pause macro-structure. Dataset public (Aalto, research use).
- status: verified (2026-08-26)

### `roeser-rw24`
- cite: Roeser, J., De Maeyer, S., Leijten, M., & Van Waes, L. (2024). Modelling typing disfluencies as finite mixture process. *Reading and Writing*, 37, 359–384. DOI 10.1007/s11145-021-10203-z.
- role: Role C — inter-key-interval distribution family: two-component log-normal mixture (fluent ~158 ms; pause component p≈0.34, task-dependent). Cite the mixture shape, not a single parameter set. Data + code on OSF (osf.io/y3p4d).
- status: verified (2026-08-26)

### `killourhy-dsn09`
- cite: Killourhy, K. S., & Maxion, R. A. (2009). Comparing Anomaly-Detection Algorithms for Keystroke Dynamics. *Proc. DSN 2009*, 125–134. DOI 10.1109/DSN.2009.5270346.
- role: Role C — public raw per-keystroke latency dataset (cs.cmu.edu/~keystroke) for direct empirical fits if needed. Caveat: single practiced password, lab setting.
- status: verified (2026-08-26)

### `dubroy-chi10`
- cite: Dubroy, P., & Balakrishnan, R. (2010). A Study of Tabbed Browsing Among Mozilla Firefox Users. *Proc. CHI 2010*, 673–682. DOI 10.1145/1753326.1753426.
- role: Role C (former D-live substitute) — logged concurrent-tab distributions: per-user medians mostly 1–6, long tail (max 42). Caveats: N=21 recruited tab users, 2009 Firefox. No public dataset.
- status: verified (2026-08-26)

### `chang-chi21`
- cite: Chang, J. C., Hahn, N., Kim, Y., Coupland, J., Breneisen, B., Kim, H. S., Hwong, J., & Kittur, A. (2021). When the Tab Comes Due: Challenges in the Cost Structure of Browser Tab Usage. *Proc. CHI 2021*, Article 149. DOI 10.1145/3411764.3445585.
- role: Role C — modern tab-count corrector: median overwhelm threshold 8 tabs (Q1–Q3 = 5–12); ~8% had >10 open at snapshot. Self-report, not logged. Justifies a fatter modern tail over the 2010 logged data.
- status: verified (2026-08-26)

### `swell-icmi14`
- cite: Koldijk, S., Sappelli, M., Verberne, S., Neerincx, M. A., & Kraaij, W. (2014). The SWELL Knowledge Work Dataset for Stress and User Modeling Research. *Proc. ICMI 2014*. DOI 10.1145/2663204.2663257. Data: DANS, DOI 10.17026/dans-x55-69zp (registration required).
- role: Role C — qualitative citation for knowledge-worker computer logging with app names; quantitative use only if raw logs are requested and analyzed.
- status: verified-in-vetting (2026-08-25); author list to re-confirm at submission

### `focal-arxiv26`
- cite: Yin, H., Wen, Z., Cao, J., Yuan, B., & Yang, R. (2026). FOCAL: Filtered On-device Continuous Activity Logging for Efficient Personal Desktop Summarization. arXiv:2604.19541 (v2, 2026-07-18). **Preprint — no venue.**
- role: Role C — precedent for the A→B→A interruption timeline shape (DesktopBench: 320 multitask + 100 interruption sessions, released on HuggingFace `HaoranYin/desktopbench` v0.1.0; data terms restrictive — research inspection only, no redistribution; scripts MIT). Supports precedent/structure claims only (preprint); co-cite `videogui-arxiv24` for session provenance. Methodological reuse unrestricted.
- status: verified (2026-08-26)

### `videogui-arxiv24`
- cite: Lin et al. (2024). VideoGUI. arXiv:2406.10227.
- role: upstream source of DesktopBench's sessions — co-cite with `focal-arxiv26` only.
- status: provisional — full author list/title to pin before citing

### `ocallahan-atc17`
- cite: O'Callahan, R., Jones, C., Froyd, N., Huey, K., Noll, A., & Partush, N. (2017). Engineering Record and Replay for Deployability. *Proc. USENIX ATC '17*, 377–389. Extended technical report: arXiv:1705.05937.
- role: Role B — "make forks and execs 2430 processes, mostly short-lived" (§4.3, kernel-build workload; written "2430" in the paper); grounds `compiler-child`/`build-orchestrator` structure.
- status: verified (2026-08-26)

### `coetzee-arxiv12`
- cite: Coetzee, D., Bhaskar, A., & Necula, G. (2012). A model and framework for reliable build systems. arXiv:1203.2704 / UC Berkeley TR UCB/EECS-2012-27. **Preprint — no venue.**
- role: Role B secondary — "the Linux kernel build's enormous number of short-lived processes" (§9). Scope note: the quote is about the *Linux kernel build* specifically, not builds in general — cite it that way.
- status: verified (2026-08-26)

## Grounding — deployed-system (footnotes; existence claims only)

### `interbench`
- cite: Kolivas, C. interbench. github.com/ckolivas/interbench, GPL-2.0, v0.31 (pin master commit).
- role: Role B — the community's interactivity task models: audio 50 ms @ 5%, video 16.7 ms @ 40%, X 0–100% variable, Burn/Write/Read/Compile loads. Frame as "the community models interactivity this way", never "desktops behave this way".
- status: verified-in-vetting (2026-08-25); pin commit at submission

### `rt-app`
- cite: rt-app. github.com/scheduler-tools/rt-app, GPLv2.
- role: Role B — JSON task-model precedent (run/period/deadline in µs); schema-shape citation for archetypes and the TIMER primitive (`timer{ref,period}`).
- status: verified-in-vetting (2026-08-25); pin commit

### `schbench`
- cite: Mason, C. schbench. github.com/masoncl/schbench, v1.0.
- role: Role B — tail-latency metric precedent (P99-focused reporting); cited by git URL in SchedCP (citation-precedent argument).
- status: verified-in-vetting (2026-08-25)

### `hackbench`
- cite: hackbench, in rt-tests. github.com/jlelli/rt-tests (src/hackbench), GPL-2.0.
- role: Role B — many-task IPC burst model (defaults 10 groups × 40 fds).
- status: verified-in-vetting (2026-08-25); pin version

### `stress-ng`
- cite: King, C. I. stress-ng. github.com/ColinIanKing/stress-ng, GPL-2.0.
- role: Role B fallback archetypes only; prefer specific sources.
- status: verified-in-vetting (2026-08-25)

### `scx`
- cite: sched-ext/scx repository. github.com/sched-ext/scx, GPLv2 (pin commit).
- role: existence of production sched_ext schedulers (scx_lavd, scx_rusty, scx_layered); the deployment-path claim.
- status: verified-in-vetting (2026-08-25); pin commit

### `lavd-ossna24`
- cite: Min, C. (2024). "Optimizing Scheduler for Linux Gaming." Talk, Open Source Summit North America 2024, Seattle, 2024-04-17. Slides: static.sched.com/hosted_files/ossna2024/9b/scx-lavd-oss-na24.pdf; schedule page: ossna2024.sched.com/event/1aBOT (accessed 2026-08-26).
- role: Role B — richest gaming numbers: ~300 tasks, ~90% long-lived, top 30–40 tasks = 95% of scheduling (15–20 take 60–70%), per-schedule runtimes ~260 µs–1.65 ms, 70–75% wakeups from waiting syscalls, 16.7 ms frame budget. Also the concentration statistics defending our single-lane scaling of `game-task-chain`. Talk slides — footnote tier despite carrying numbers; pair with `corbet-lwn24` for prose-citable coverage.
- status: verified (2026-08-26)

### `corbet-lwn24`
- cite: Corbet, J. "Sched_ext at LPC 2024." *LWN.net*, 2024-09-26. lwn.net/Articles/991205/ (accessed 2026-08-26).
- role: prose-citable secondary for the LAVD characterization (dedicated "Higher frame rates" section on scx_lavd). Later option to evaluate: "Lessons from creating a gaming-oriented scheduler", LWN, Jan 2026 (lwn.net/Articles/1051430/ — byline unverified).
- status: verified (2026-08-26)

### `ananicy`
- cite: Nefelim4ag. Ananicy. github.com/Nefelim4ag/Ananicy (GPL); ananicy-cpp: gitlab.com/ananicy-cpp/ananicy-cpp (GPL-3.0).
- role: Role A — deployed per-process priority-class daemon; rule schema (`type`, nice, ioclass, cgroup).
- status: verified-in-vetting (2026-08-25); pin version

### `ananicy-rules`
- cite: CachyOS ananicy rules catalog. github.com/CachyOS/ananicy-rules (pin commit).
- role: Role A + archetype `category_source` — a community-maintained process-name → behavior-class taxonomy (`Heavy_CPU`, `Game`, `BG_CPUIO`, …); grounds the wanted/unwanted-background distinction as deployed practice.
- status: verified-in-vetting (2026-08-25); pin commit

### `pcmark10`
- cite: UL Solutions. PCMark 10 Technical Guide. [Edition/URL to pin.]
- role: Role A — scenario groups (Essentials/Productivity/DCC/Gaming) and their application lists. Taxonomy existence only.
- status: to-pin (submission-time, per standing task)

### `sysmark30`
- cite: BAPCo. SYSmark 30 User Guide (v1.1, 2024). [URL to pin.]
- role: Role A primary BAPCo taxonomy — Office/General Productivity/Photo/Advanced Content Creation scenario + app lists. Note in paper: the 2011 vendor departures concerned scoring, not scenario lists.
- status: to-pin

### `sysmark25`
- cite: BAPCo. SYSmark 25 documentation. [URL to pin.]
- role: Role A — adds software development (code compilation) and Responsiveness.
- status: to-pin

### `procyon`
- cite: UL Solutions. Procyon benchmark suite documentation. [URL to pin.]
- role: Role A, conditional — local-AI desktop scenario existence (S12 precedent).
- status: to-pin

### `gamemode-docs`
- cite: Microsoft. Game Mode documentation, Microsoft Learn (+ `<expandedresources.h>` APIs). [Exact URLs to pin.]
- role: Role A — shipped foreground-game resource-priority category; the whitelist design point we reconstruct.
- status: to-pin

### `steam-downloads`
- cite: Valve. "Downloads automatically pause when launching a game." Steam Support, help.steampowered.com/en/faqs/view/4F9E-6328-E9B8-47F9 (accessed 2026-08-26). Secondary: "Managing Steam Downloads & Updates", …/71AB-698D-57EB-178C (updated 2024-09-24).
- role: S10 — documents the "Allow Downloads During Gameplay" checkbox (Steam → Settings → Downloads), default pause-during-gameplay, and the per-game counterpart: the wanted/unwanted toggle as a real user-facing setting. Note: 2021 article title-cases the toggle; current client UI sentence-cases it.
- status: verified (2026-08-26)

### `schedext-docs`
- cite: Linux kernel documentation. "Extensible Scheduler Class." docs.kernel.org/scheduler/sched-ext.html (accessed 2026-08-26). Merged in Linux 6.12.
- role: existence and mechanism of runtime-loadable scheduling policy; the deployment path.
- status: verified (2026-08-26)

### `mozilla-testpilot10`
- cite: Mozilla Labs Test Pilot. "A Week in the Life of a Browser" study v2 (2010), N≈27,000, CC-BY 3.0 US; aggregate tables mirrored at github.com/mozilla/testpilotweb (testcases/a-week-life-2/aggregated-data.html).
- role: Role C — only large-N logged concurrent-tab data: mean ≈3.2 tabs, median weekly max <8, 25% of users ≥11. Caveats: 2010 opt-in enthusiasts; raw dumps no longer hosted. Honest-limitation line: no post-2010 large-scale logged tab distribution exists publicly.
- status: verified (2026-08-26)

### `singervine-slate10`
- cite: Singer-Vine, J. "Open This Story in a New Tab." *Slate*, 2010-12-05. slate.com/human-interest/2010/12/a-new-data-set-from-firefox-reveals-our-browsing-habits.html.
- role: the published analysis of `mozilla-testpilot10` — journalism, not peer review; cite only as the analysis source of those aggregates.
- status: verified (2026-08-26)

### `mark-gallup06`
- cite: Robison, J. "Too Many Interruptions at Work?" (interview with Gloria Mark). *Gallup Business Journal*, 2006-06-08. news.gallup.com/businessjournal/23146/too-many-interruptions-work.aspx (accessed 2026-08-26).
- role: the ONLY source of the "23 min 15 s to resume" figure — appears in no peer-reviewed paper (independently audited). Cite as interview or omit the figure.
- status: verified (2026-08-26)

## Grounding — measurement

### `meas-ci`
- cite: this work — CI measurement campaign; workflow files and raw outputs released in the artifact. Locator: `meas-ci:<workflow>:<run>`.
- role: structural/shape claims about software behavior only (fork structure, counts, lifetime shapes, periods, heartbeats, comm strings); machine-relative absolutes carry the runner spec and rank as convention-informed-by-measurement. Never desktop-performance claims. N-run spread reported.
- status: reserved (no runs yet; `meas-pending` placeholders in archetypes until freeze)

### `meas-pending`
- cite: none — not a source; the placeholder sentinel for parameters awaiting the CI campaign.
- role: valid as a `source:` tag only until the schema freeze; the linter rejects it after. Exists here only so the yaml-subset lint holds without exceptions.
- status: sentinel

## Related work only (never in the yaml registry)

### `ghost-sosp21`
- cite: Humphries, J. T., Natu, N., Chaugule, A., Weisse, O., Rhoden, B., Don, J., Rizzo, L., Rombakh, O., Turner, P., & Kozyrakis, C. (2021). ghOSt: Fast & Flexible User-Space Delegation of Linux Scheduling. *Proc. SOSP '21*, 588–604. DOI 10.1145/3477132.3483542.
- role: mechanism line — userspace scheduling delegation. status: verified (2026-08-26)

### `decima-sigcomm19`
- cite: Mao, H., Schwarzkopf, M., Venkatakrishnan, S. B., Meng, Z., & Alizadeh, M. (2019). Learning Scheduling Algorithms for Data Processing Clusters. *Proc. SIGCOMM '19*, 270–288. DOI 10.1145/3341302.3342080.
- role: learned-schedulers line (RL over job DAGs). status: verified (2026-08-26)

### `firm-osdi20`
- cite: Qiu, H., Banerjee, S. S., Jha, S., Kalbarczyk, Z. T., & Iyer, R. K. (2020). FIRM: An Intelligent Fine-Grained Resource Management Framework for SLO-Oriented Microservices. *Proc. OSDI '20*, 805–825.
- role: learned-schedulers line (SLO-driven microservices). status: verified (2026-08-26)

### `park-neurips19`
- cite: Mao, H., et al. (17 authors). (2019). Park: An Open Platform for Learning-Augmented Computer Systems. *NeurIPS 32*, 2490–2502.
- role: learned-schedulers line (platform). Title is "Learning-Augmented", not "Learned". status: verified (2026-08-26)

### `asa-arxiv25`
- cite: Wang, X., Jia, S., Huang, Z., Cao, J., & Song, M. (2025). Mixture-of-Schedulers: An Adaptive Scheduling Agent as a Learned Router for Expert Policies. arXiv:2511.11628 (v1, no venue).
- role: closest architectural prior — recognize-then-route atop sched_ext, behavioral channel; our difference is the identity/world-knowledge channel. status: verified (2026-08-26)

### `schedcp-mlsys25`
- cite: Zheng, Y., Hu, Y., Zhang, W., & Quinn, A. (2025). Towards Agentic OS: An LLM Agent Framework for Linux Schedulers. arXiv:2509.01245 (v4); ML for Systems @ NeurIPS 2025.
- role: closest LLM-scheduling prior — agentic policy synthesis for servers; our differences: signal-not-policy contract, desktop setting, recognition measured directly. **No conference successor exists as of 2026-08-26** (re-check before every submission). status: verified (2026-08-26)

### `kgent-ebpf24`
- cite: Zheng, Y., Yang, Y., Chen, M., & Quinn, A. (2024). Kgent: Kernel Extensions Large Language Model Agent. *Proc. SIGCOMM 2024 Workshop on eBPF and Kernel Extensions (eBPF '24)*, 30–36. DOI 10.1145/3672197.3673434.
- role: LLM-agents-for-kernel-policy line. Author list differs from SchedCP's. status: verified (2026-08-26)

### `tuneagent-arxiv25`
- cite: Lin, H., Li, Y., Luo, H., Lin, Z., Zhang, L., Xing, M., & Wu, Y. (2025). TuneAgent: Agentic Operating System Kernel Tuning with Reinforcement Learning. arXiv:2508.12551 (no venue).
- role: adjacent LLM-in-the-loop kernel tuning. status: verified (2026-08-26)

### `jadhav-arxiv25`
- cite: Jadhav, P., Jin, H., Deelman, E., & Balaprakash, P. (2025). Evaluating the Efficacy of LLM-Based Reasoning for Multiobjective HPC Job Scheduling. arXiv:2506.02025 (under review).
- role: adjacent LLM HPC scheduling. (Alternate candidate if context meant benchmarking: arXiv:2511.11612.) status: verified (2026-08-26)

### `eevdf-tr95`
- cite: Stoica, I., & Abdel-Wahab, H. (1995). Earliest Eligible Virtual Deadline First: A Flexible and Accurate Mechanism for Proportional Share Resource Allocation. Technical Report TR-95-22, Old Dominion University. Kernel doc: docs.kernel.org/scheduler/sched-eevdf.html.
- role: behavioral-heuristics line — the current CFS successor's basis. Year is 1995 (not '96). status: verified (2026-08-26)

### `ostep`
- cite: Arpaci-Dusseau, R. H., & Arpaci-Dusseau, A. C. *Operating Systems: Three Easy Pieces*. Arpaci-Dusseau Books. Chapter: "Scheduling: The Multi-Level Feedback Queue" (pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-mlfq.pdf).
- role: MLFQ textbook citation. Edition/year to pin at submission. status: to-pin (edition)

### `corbato-sjcc62`
- cite: Corbató, F. J., Merwin-Daggett, M., & Daley, R. C. (1962). An Experimental Time-Sharing System. *Proc. Spring Joint Computer Conference (AFIPS '62)*, 335–344. DOI 10.1145/1460833.1460871.
- role: MLFQ original (CTSS). status: verified (2026-08-26)
