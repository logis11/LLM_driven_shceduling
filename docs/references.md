# REFERENCES — master citation index
> Status: normative · Created 2026-08-26 · Updated 2026-09-12

The single index answering "what do we cite, in what form, for what claim." One id namespace across the whole project: these ids are the `source:` tag prefixes in the dataset (via `dataset/sources.yaml`) and the bibkeys in the paper. This file owns every citation string and every citation-constituent field (`url`, `accessed`, `pinned_version`); the yaml registry holds machine/derivation fields only and must be a subset of this index (lint: every yaml id has an entry here; entries here without a yaml counterpart are paper-only references).

## Id-minting rule

**Entry unit: one citable artifact** — the thing that gets exactly one citation, one URL, one accessed date. A project with several citable artifacts (paper + slides + repo) gets several entries.

Id derivation by `type`:

- **scholarly** → `<label>-<venue><yy>` — label is the first-author surname, or the system name when the work is universally known by it (`cpsmark-tbench23`, `lavd-ossna24`). arXiv-only works use `arxiv` in the venue slot (`focal-arxiv26`). Raw arXiv numbers are banned as ids — they live in the citation.
- **deployed-system** → project name, no year; `pinned_version` carries freshness (`interbench`, `rt-app`, `steam-downloads`).
- **measurement** → `meas-ci`, with run identification in the locator (`meas-ci:<workflow>:<run>`).

**Contributor recipe:** (1) read this rule and mint the id; (2) add the entry here; (3) add a `dataset/sources.yaml` entry *only if the dataset derives values or structure from it*.

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
- status: verified (source-vetting full-text review, 2026-08-25)

### `zhang-chb15`
- cite: Zhang, T., Sun, X., Chai, Y., & Aghajan, H. (2015). A look at task-switching and multi-tasking behaviors: From the perspective of the computer usage among a large number of people. *Computers in Human Behavior*, 49, 237–244. DOI 10.1016/j.chb.2015.03.012.
- role: Role C — power-law switching, hub task structure ("star" is our paraphrase — say "hub"), ~3-min average PC-task switch (independently corroborates `gonzalez-chi04`). 31 days / 3,000 subjects / 15M+ records / 16,406 processes, CNNIC data. Dataset unreleased.
- status: verified (2026-08-26; corrects source-vetting's "Yun et al." misattribution)

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

### `brodersen-icpr10`
- cite: Brodersen, K. H., Ong, C. S., Stephan, K. E., & Buhmann, J. M. (2010). The Balanced Accuracy and Its Posterior Distribution. *Proc. 2010 20th International Conference on Pattern Recognition (ICPR)*, Istanbul, IEEE, 3121–3124. DOI 10.1109/ICPR.2010.764. Author-hosted PDF: kaybrodersen.github.io/publications/Brodersen_2010b_ICPR.pdf (accessed 2026-09-11).
- role: the definition behind the Layer-1 **attribute** headline (`harness/metrics.md` §8; sub-task 8.4) — balanced accuracy as "the average accuracy obtained on either class", "given by ½(TP/P + TN/N)" (§III) — and the reason the raw rate is not the headline there: accuracy "leads to an optimistic estimate when a biased classifier is tested on an imbalanced dataset" (abstract), so that "the classifier might assign every single test case to the large class, thereby achieving an accuracy equal to the fraction of the more frequent labels in the test set", whereas "if the conventional accuracy is high only because the classifier takes advantage of an imbalanced test set, then the balanced accuracy, as desired, will drop to chance" (§III). **Binary only** — §II "In a binary classification setting"; the measure is defined solely off a 2×2 matrix, and its single "multiclass" sentence is a Discussion gesture at future work, generalising the *posterior* "by replacing the Beta distribution by the Dirichlet distribution" (§V), with no K-class definition, formula, or evaluation. Never cite it for the sixteen-mode axis, which reports raw accuracy against a measured baseline instead. It never writes "recall", "sensitivity" or "specificity"; those are our gloss on TP/P and TN/N. Its interval machinery assumes each test case is "an independent Bernoulli experiment" (§II), so it does not license an interval over our per-file structure — that is `field-jrssb07`. It makes no small-sample claim.
- status: verified (2026-09-11; full four-page author-hosted PDF read; pages 3121–3124 confirmed against Crossref and against `chicco-bmcg20`'s own reference [83])

### `chicco-bmcg20`
- cite: Chicco, D., & Jurman, G. (2020). The advantages of the Matthews correlation coefficient (MCC) over F1 score and accuracy in binary classification evaluation. *BMC Genomics*, 21(1), Article 6. DOI 10.1186/s12864-019-6413-7. Open access, CC BY 4.0: bmcgenomics.biomedcentral.com/articles/10.1186/s12864-019-6413-7 (accessed 2026-09-11).
- role: why a majority-flattered rate is not reportable alone on a binary axis, and the all-four-cells property of the coefficient the grader reports beside balanced accuracy (`harness/metrics.md` §8; 8.4): "these statistical measures can dangerously show overoptimistic inflated results, especially on imbalanced datasets" (abstract); accuracy "provides an overoptimistic estimation of the classifier ability on the majority class" (Background); the coefficient "produces a high score only if the prediction obtained good results in all of the four confusion matrix categories (true positives, false negatives, true negatives, and false positives)" (abstract), against classwise rates which "we cannot consider fully informative because they use only two categories of the confusion matrix" (Methods). **Binary only**; its multiclass remarks point at others' work (its ref [40], Gorodkin 2004), not its own result, and this project adopts no multiclass form. **Its recommendation is the coefficient over accuracy and F1, never over balanced accuracy**, which it lists among "classwise weighted accuracy rates" and names as future work — do not cite it against our balanced-accuracy headline. Says nothing about clustered or non-independent samples.
- status: verified (2026-09-11; full text read from the CC BY version of record via Europe PMC, PMC6941312 / PMID 31898477; coordinates confirmed at Crossref)

### `field-jrssb07`
- cite: Field, C. A., & Welsh, A. H. (2007). Bootstrapping Clustered Data. *Journal of the Royal Statistical Society: Series B (Statistical Methodology)*, 69(3), 369–390. DOI 10.1111/j.1467-9868.2007.00593.x (accessed 2026-09-11).
- role: the justification for resampling **workload files rather than query points** when the harness computes a Layer-1 interval (`harness/metrics.md` §8; 8.4). "The simple cluster bootstrap is based on drawing samples of g clusters independently with replacement" (§3.3), and it "has the advantage of being non-parametric and not depending on any model", giving estimates "consistent under both models" (§3.3, and the Summary's comparison with the residual bootstrap). Carry its scope limit wherever it is cited: consistency is in the **number of clusters**, the variances being "asymptotically correct as g → ∞ with m fixed" (Corollary 4), and their own Table 2 at g = 5 shows the cluster bootstrap badly underestimating variance. Our Layer-1 set has roughly forty-nine files, well clear of that regime, but the caveat is the entry's, not the reader's to rediscover. The paper is purely statistical and says nothing about classifiers or accuracy, so applying it to a classifier metric is our extension.
- status: verified (2026-09-11; published PDF read in full; JRSS-B Vol. 69, Part 3, pp. 369–390)

### `dietterich-neco98`
- cite: Dietterich, T. G. (1998). Approximate Statistical Tests for Comparing Supervised Classification Learning Algorithms. *Neural Computation*, 10(7), 1895–1923. MIT Press. DOI 10.1162/089976698300017197. Author's preprint (dated 1997-12-30): web.engr.oregonstate.edu/~tgd/publications/nc-stats.ps.gz (accessed 2026-09-11).
- role: why Layer-1 condition comparisons are computed **paired on one test set** rather than as two separate rates (`harness/metrics.md` §8; 8.4). Its Question 3 is our case verbatim: "Given two classifiers C_A and C_B and enough data for a separate test set, determine which classifier will be more accurate on new test examples. This question can be answered by measuring the accuracy of each classifier on the separate test set and applying McNemar's test" (§2). It is also the source for what not to use: "Two widely-used statistical tests are shown to have high probability of Type I error in certain situations and should never be used … (a) a test for the difference of two proportions and (b) a paired-differences t test based on taking several random train/test splits" (abstract). Scope limits in its own words: of McNemar's test it warns "it does not directly measure variability due to the choice of the training set or the internal randomness of the learning algorithm" (§3), so cite it for a fixed-test-set paired comparison only; its conclusions are "tentative, because the experiments are based on only two learning algorithms and three data sets" (§8). Says nothing about clustered test examples, so the interval itself is `field-jrssb07`'s. Supersedes a bare McNemar (1947) citation, a psychometrics note on correlated proportions that says nothing about classifiers.
- status: verified (2026-09-11; author's preprint read in full; published coordinates — *Neural Computation* 10(7), 1895–1923 — confirmed at Crossref. The preprint, not the version of record, is what was read; re-pin the published PDF before submission if a page-level locator is needed)

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
- cite: hackbench, in rt-tests. git.kernel.org/pub/scm/utils/rt-tests/rt-tests.git (`src/hackbench/hackbench.c`, `src/hackbench/hackbench.8`), GPL-2.0. Repository HEAD `fd45df83` at access; `hackbench.c` last modified 2024-05-22, man page dated 2020-09-19 (accessed 2026-09-12).
- role: Role B — many-task IPC burst model. Existence only. Purpose in the man page's words: "Hackbench is both a benchmark and a stress test for the Linux kernel scheduler. It's main job is to create a specified number of pairs of schedulable entities (either threads or traditional processes) which communicate via either sockets or pipes and time how long it takes for each pair to send data back and forth." Defaults read from the source: `datasize = 100`, `loops = 100`, `num_groups = 10`, `num_fds = 20`. The printed banner is "Running in process mode with 10 groups using 40 file descriptors each (== 400 tasks)" because, per the man page, "the effective number will be twice the amount you set here, as the sender and receiver children will each open the given amount of file descriptors" — 10 × 20 × 2 = 400. Reports a single completion time; no latency distribution, which is the contrast `schbench` is cited for.
- status: verified (2026-09-12; repository cloned from git.kernel.org and both files read). Supersedes the GitHub-mirror reading, whose `hackbench.c` dated to 2012 — the upstream text is unchanged in every quoted part. Pin a release tag (latest v2.10) or the commit at submission.

### `stress-ng`
- cite: King, C. I. stress-ng. github.com/ColinIanKing/stress-ng, GPL-2.0.
- role: Role B fallback archetypes only; prefer specific sources.
- status: verified-in-vetting (2026-08-25)

### `scx`
- cite: sched-ext/scx repository. github.com/sched-ext/scx, GPLv2 (pin commit).
- role: existence of production sched_ext schedulers (scx_lavd, scx_rusty, scx_layered); the deployment-path claim. This repository, not the kernel documentation, is the home of the **watchdog** statement: "there are two more ways to disable a `sched_ext` scheduler - `sysrq-S` and the watchdog timer. Ignoring kernel bugs, the worst damage a `sched_ext` scheduler can do to a system is starving some threads until the watchdog timer triggers."
- **Bound on the deployment claim (checked 2026-09-12).** What the repository supports is that upstream carries sched_ext from 6.12, that "Both Meta and Google are fully committed to `sched_ext` and Meta is in the process of mass production deployment", and that "Distros are able to package and release these schedulers". It contains **no statement that any distribution or vendor enables an scx scheduler by default** — that claim needs a separate source. Note also that the C example schedulers have moved out of this repository; the Rust set now holds scx_lavd, scx_rusty, scx_layered, scx_bpfland, scx_flash and others, each with its own README and its own "Production Ready?" line.
- status: verified-in-vetting (2026-08-25); watchdog wording, deployment statements and the scheduler list re-confirmed 2026-09-12. Pin commit.

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
- role: Role A — deployed per-process priority-class daemon; rule schema. Self-description: "a shell daemon created to manage processes' IO and CPU priorities, with community-driven set of rules for popular applications … mainly for desktop usage". Matching is by executable name, optionally narrowed by command line: `name` is the only required field ("used for match processes by exec bin name"), with `cmdlines`, `type`, `nice`, `latency_nice`, `sched`, `rtprio`, `ioclass`, `ionice`, `oom_score_adj`, `cpuset` and `cgroup` optional (field list from the ananicy-cpp README).
- **Two lineages, and they no longer share a type vocabulary.** Upstream Ananicy's current `ananicy.d/00-types.types` uses lowercase types (`game`, `compiler`, `file-sync`, `service`) and carries the capitalized ones (`Heavy_CPU`, `BG_CPUIO`, `LowLatency_RT`) commented out beneath a heading reading "Depricated types". The capitalized vocabulary belongs to the ananicy-cpp / CachyOS-catalogue lineage — cite `ananicy-rules` for it, never this entry. Any claim naming `Game`, `Heavy_CPU` or `BG_CPUIO` must say which lineage it is about.
- status: verified-in-vetting (2026-08-25); the lineage split and the field list re-confirmed 2026-09-12 from both projects' READMEs and from upstream's types file at HEAD. Pin version and commit at submission.

### `ananicy-rules`
- cite: CachyOS ananicy rules catalog. github.com/CachyOS/ananicy-rules (pin commit).
- role: Role A + archetype `category_source` — a community-maintained process-name → behavior-class taxonomy (`Heavy_CPU`, `Game`, `BG_CPUIO`, …); grounds the wanted/unwanted-background distinction as deployed practice. **This catalogue, not upstream Ananicy, is where the capitalized types live** (see the lineage note on `ananicy`); it is maintained "by the CachyOS team and the community" and contributors are asked to paste the game's store URL beside each entry.
- **Measured at commit `03ef03fbf7e834385377432ccecaedd32e3414bb` (authored 2026-09-08, counted 2026-09-12):** 361 `.rules` files; 15 813 rule entries; 13 528 of them carry `"type": "Game"` (85.5 per cent), then `BG_CPUIO` 1 615, `Service` 194, `Doc-View` 160, `LowLatency_RT` 109, `Chat` 51, `Heavy_CPU` 33, `Image-View` 32, `Player-Audio` 28, `Player-Video` 24, `Launcher` 24, `IN_DIFF` 10, `OOM_NO_KILL` 2, `TODO` 1, and 2 entries with no `type` key. `00-types.types` sets `Game` nice −5 (ioclass best-effort, sched normal); `Player-Audio`, `Player-Video`, `Image-View` and `Doc-View` nice −4; `LowLatency_RT` nice −12 (ioclass best-effort); `BG_CPUIO` nice 16 (ioclass idle, sched idle); `BG_CPU` nice 14; `Launcher` nice 16; `Heavy_CPU` nice 9; `Chat` nice −3; `Service` nice 10; `IN_DIFF` nice 0; and `OOM_KILL` / `OOM_NO_KILL` set only `oom_score_adj` to 1000 / −1000. Exact spelling is `Doc-View`, hyphenated. One game can hold several entries under different types — the catalogue's own example gives one title an orchestrator executable as `BG_CPUIO` and its shipping executable as `Game`.
- **Type count, stated precisely:** `00-types.types` defines **fifteen** types; **thirteen** are used by at least one entry (`BG_CPU` and `OOM_KILL` have none). A fourteenth string, `TODO`, appears on one entry without being defined anywhere, and one entry is not valid JSON (a stray `+` at end of line, `00-default/Games/linux-native/linux-native_d.rules:315`). Say "thirteen distinctions in use" rather than "eleven types"; the earlier figure omitted `IN_DIFF` and the OOM types.
- **Counting method, required for reproducibility.** Count `.rules` files by extension; parse each file *separately*, one JSON object per non-blank, non-`#` line. Concatenating the files first fuses the last line of any file lacking a trailing newline with the first line of the next, which silently drops entries — that is the source of the earlier 15 815 / 1 614 / 110 figures, now superseded.
- The counts support the **enumeration-cost** argument (how many hand-written entries one distinction costs, and how few distinctions the used types express) and nothing else; they are existence-and-count claims, never a claim about the approach's effectiveness.
- status: verified (2026-09-12; catalogue cloned and counted at the named commit by the method stated above). Re-count and re-pin the commit at submission — the catalogue changes weekly, and any recount must carry its own commit and date.

### `pcmark10`
- cite: UL Solutions. PCMark 10 Technical Guide. [Edition/URL to pin.]
- role: Role A — scenario groups (Essentials/Productivity/DCC/Gaming) and their application lists. Taxonomy existence only.
- status: to-pin (submission-time, per standing task)

### `sysmark30`
- cite: BAPCo. *SYSmark 30 User Guide*. bapco.com/wp-content/uploads/2025/04/bapco-sysmark30-user-guide-v1.2.pdf, 40 pp. (accessed 2026-09-12). Cover reads "Revision: 1.1"; the revision history runs through 1.2 — cite the file's version, and note the cover discrepancy if a reviewer might check.
- role: Role A primary BAPCo taxonomy — existence only. Four scenarios, as the guide states them: **Office Applications** "models office environment like usage including word processing (mail merge, document comparison, and PDF conversion), spreadsheet data manipulation (data modeling, financial forecasting), presentation editing"; **General Productivity** "models OCR of documents, web browsing, application installation, and archiving and unpacking a mixed file data set"; **Photo Editing** "models editing digital photos (applying filters and creating HDR photos), cataloging digital photos (organizing catalog, use of facial detection to group people)"; **Advanced Content Creation** "encodes video with a CPU render and GPU accelerated workload for SUTs configured with a supported accelerated GPU. A multitasking workload switches between photo editing and video editing workloads." Named applications, by scenario: Microsoft Excel / Outlook / PowerPoint / Word 2021 Professional Plus VL; Adobe Acrobat Pro DC, Audacity 2.3.2 (listed "for app install" — the installation itself is the workload), Corel WinZip 26.0, Google Chrome 106.0.5249.103; Adobe Lightroom Classic 11 and Photoshop CC 23; Photoshop CC 23 and Premiere CC 22. Note in paper: the 2011 vendor departures concerned scoring, not scenario lists.
- status: verified (2026-09-12), **with a retrieval caveat to resolve before submission.** bapco.com refused every direct request from the verifying environment (HTTP 403 on the product page, the PDF and the site root), so the guide was read from the Internet Archive's capture of BAPCo's own URL (snapshot 2025-04-23); the bytes are BAPCo's PDF and the live fetch is what failed. The four scenario names and descriptions were independently corroborated against store.bapco.com/product/sysmark-30/, which was reachable. Re-download from bapco.com and pin the live URL, version and access date.

### `sysmark25`
- cite: BAPCo. SYSmark 25 documentation. [URL to pin.]
- role: Role A — adds software development (code compilation) and Responsiveness.
- status: to-pin. bapco.com refused direct requests at the 2026-09-12 check (see `sysmark30`); if the live site stays unreachable, the Internet Archive holds captures of BAPCo's own upload paths and the same retrieval caveat applies.

### `procyon`
- cite: UL Solutions. "Procyon benchmark suite." benchmarks.ul.com/procyon (accessed 2026-09-12).
- role: Role A, conditional — **the condition is met.** Local-AI desktop scenarios exist in a shipped commercial benchmark (S12 precedent): of the nine benchmarks, three are AI workloads — **AI Text Generation**, "standardized AI performance testing in a variety of local AI LLM use cases"; **AI Image Generation**, "two tests built with different versions of the Stable Diffusion models … our heaviest AI inference workload yet"; **AI Computer Vision**, "designed around a range of machine vision tasks and AI models, carefully selected based on their use case, relevance and daily impact in the modern office". The other six: Essentials ("a multitasking and browsing-focused benchmark … the standard run will not require any third-party software"), Office Productivity (Word, Excel, PowerPoint, Outlook), Photo Editing (Adobe Lightroom, Adobe Photoshop), Video Editing (Adobe Premiere Pro), Battery Life, One-Hour Battery Consumption. Existence only — supports "these scenarios ship in a commercial benchmark", never a claim about how common the workload is on real desktops. The application overlap with `pcmark10` and `sysmark30` may be cited as a convergence across three vendors' taxonomies; it may **not** be cited as evidence about user behaviour, since the vendors are not independent observers of usage.
- status: verified (2026-09-12; the suite overview page read in full). Per-benchmark technical guides were not read — cite only the overview's wording above, or pin the individual guide.

### `gamemode-docs`
- cite: Microsoft. Game Mode documentation, Microsoft Learn (+ `<expandedresources.h>` APIs). [Exact URLs to pin.]
- role: Role A — shipped foreground-game resource-priority category. Existence only. **The role has narrowed: this entry can no longer be cited as the whitelist design point we reconstruct.** The conceptual portal page has now been read, and Microsoft's documentation does not state how a game is recognised. What it states is the outcome — "Game Mode works by default for most Windows games, requiring no action or opt-in by the customer, and no work by the game developer" — beside an optional developer declaration, the `expandedResources` capability, which is "granted on a per-title basis; contact your account manager for more information". No list, no executable-name matching, no detection mechanism on any of the four pages. Cite this entry for *the mechanism is not documented*, which is a checkable claim; reconstruct the name-table design point from `ananicy-rules` instead.
- **What the documentation does state (all four pages read 2026-09-12).** Resource model: exclusive CPU sets plus "increased GPU prioritization". Background work is excluded from the reserved cores rather than throttled — opting out of exclusivity means "having to share them with other processes", at "a higher latency due to other processes and system activities being scheduled on the same cores as the game". Grant condition: "The app must be in the foreground and have focus before exclusive resources are granted" (repeated on all three function pages). Revocation differs by resource: exclusive CPUs go "when the game loses focus", whereas "memory resources, once granted, will never be revoked". User opt-out: `GetExpandedResourceExclusiveCpuCount` "returns 0 if no exclusive CPU sets are available, or if the customer opted out of Game Mode via the Settings in Windows 10". Carry the deprecation note wherever these APIs are cited: "The Game Mode APIs are deprecated in Windows 10, version 1809 and later."
- status: verified (2026-09-12; `previous-versions/windows/desktop/gamemode/game-mode-portal` plus the three `windows/win32/api/expandedresources/` function pages read in full on Microsoft Learn). **One open question, deliberately unresolved:** whether Microsoft documents that Game Mode defers Windows Update driver installs or restart/notification prompts during play. No page reachable at this check says so; the Xbox Support article that would plausibly carry it renders its body via script and could not be read. The claim is widespread in third-party coverage, which this project's tier rule does not accept. Resolve against a Microsoft-published document, or drop the claim.

### `steam-downloads`
- cite: Valve. "Downloads automatically pause when launching a game." Steam Support, help.steampowered.com/en/faqs/view/4F9E-6328-E9B8-47F9 (accessed 2026-08-26). Secondary: "Managing Steam Downloads & Updates", …/71AB-698D-57EB-178C (updated 2024-09-24).
- role: S10 — documents the "Allow Downloads During Gameplay" checkbox (Steam → Settings → Downloads), default pause-during-gameplay, and the per-game counterpart: the wanted/unwanted toggle as a real user-facing setting. Note: 2021 article title-cases the toggle; current client UI sentence-cases it.
- status: verified (2026-08-26)

### `dkms-man`
- cite: dkms(8) manual page, dkms 3.0.11. Ubuntu Manpage Repository (noble), manpages.ubuntu.com/manpages/noble/man8/dkms.8.html (accessed 2026-09-10).
- role: S11 unwanted counterpart (C7) — existence of the DKMS framework ("kernel modules to be dynamically built for each kernel on your system") and of its `autoinstall` action and `dkms_autoinstaller` service, which build and install module revisions for a newly booted kernel without user action; `dkms` as the orchestrator's process name. Existence only.
- status: verified (2026-09-10)

### `dkms-debian`
- cite: Debian package `dkms` 3.0.10-8+deb12u1 (bookworm). packages.debian.org/bookworm/dkms (accessed 2026-09-10).
- role: S11 unwanted counterpart (C7) — the package description ("very easy to rebuild modules as you upgrade kernels") and the fact that the framework is packaged in the distributions the names workflow covers. Existence only.
- status: verified (2026-09-10)

### `schedext-docs`
- cite: Linux kernel documentation. "Extensible Scheduler Class." docs.kernel.org/scheduler/sched-ext.html (accessed 2026-08-26). Merged in Linux 6.12. Rendered from `Documentation/scheduler/sched-ext.rst` in the kernel tree; quote the tagged source file when a version matters.
- role: existence and mechanism of runtime-loadable scheduling policy; the deployment path. The safety claim this document actually makes is integrity, not verification: "The system integrity is maintained no matter what the BPF scheduler does. The default scheduling behavior is restored anytime an error is detected, a runnable task stalls, or on invoking the SysRq key sequence `SysRq-S`."
- **Three constraints on citing it, from reading the source file at both tags on 2026-09-12.** (1) It makes **no general BPF-verifier guarantee**: the word appears once, inside a code comment in the example scheduler. Do not source a verifier-safety claim here. (2) It never says **watchdog** — that word is the `scx` repository's, not the kernel doc's; cite `scx` for it. (3) The sentence placing the fair class above `SCHED_EXT` in `sched_class` precedence exists in **mainline only**; the v6.12 text of the same sentence omits the precedence clause and says CFS where mainline says fair-class. Cite mainline for precedence, v6.12 for the merged-version wording.
- status: verified (2026-08-26); re-read at mainline and v6.12 on 2026-09-12 from the `.rst` source, docs.kernel.org being unreachable at that check.

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

### `linux-sched-fair`
- cite: Linux kernel source, `kernel/sched/fair.c`. Tag v6.5 (CFS): `sysctl_sched_latency = 6000000ULL` ("default: 6ms * (1 + ilog(ncpus))"), `sysctl_sched_min_granularity = 750000ULL` ("default: 0.75 msec * (1 + ilog(ncpus))"). Tag v6.6 (EEVDF): `sysctl_sched_base_slice = 750000ULL` ("Minimal preemption granularity for CPU-bound tasks: default: 0.75 msec * (1 + ilog(ncpus))"). github.com/torvalds/linux/blob/v6.5/kernel/sched/fair.c and /v6.6/kernel/sched/fair.c (accessed 2026-09-07).
- role: existence claim only — the slice magnitudes a shipped general-purpose scheduler uses (sub-millisecond base slice, single-digit-millisecond target latency). Bounded the former 2 ms boot slice (retired 2026-09-11 for OSTEP's 10 ms example); one point of the RQ0 gate spec's boot-default sensitivity sweep (`harness/boot-defaults/ostep-slice-750us.json`, 8.8); does not name our value.
- status: verified (2026-09-07; values read from the tagged source)

### `linux-sched-bwc`
- cite: Linux kernel documentation. "CFS Bandwidth Control." docs.kernel.org/scheduler/sched-bwc.html (accessed 2026-09-10): "CFS bandwidth control is a CONFIG_FAIR_GROUP_SCHED extension which allows the specification of the maximum CPU bandwidth available to a group or hierarchy"; "within each given 'period' (microseconds), a task group is allocated up to 'quota' microseconds of CPU time."
- role: existence claim only — a shipped general-purpose scheduler carries a per-class CPU bandwidth ceiling (quota per period on a cgroup). Grounds the *idea* behind `batch_bandwidth_cap` (recognition-vocabulary §2); does not name our range, floor, or class rule, and differs in what the class is (an administrator-assigned cgroup there, a behaviourally inferred batch class here).
- status: verified (2026-09-10)

### `linux-sched-ext`
- cite: Linux kernel source, `include/linux/sched/ext.h`. Tag v6.12: `enum scx_public_consts { SCX_SLICE_DFL = 20 * 1000000, /* 20ms */ SCX_SLICE_INF = U64_MAX, /* infinite, implies nohz */ }`. github.com/torvalds/linux/blob/v6.12/include/linux/sched/ext.h (accessed 2026-09-12).
- role: existence claim only — the sched_ext scheduler class's default slice constant, `SCX_SLICE_DFL`, is 20 ms in a shipped kernel. One point of the RQ0 gate spec's boot-default sensitivity sweep (`harness/boot-defaults/ostep-slice-20000us.json`); does not name our values.
- status: verified (2026-09-12)

### `illumos-ts`
- cite: illumos-gate source, `usr/src/uts/common/disp/ts_dptbl.c` (default `config_ts_dptbl[]`: 60 user-priority levels, `ts_quantum` in clock ticks, columns `glbpri qntm tqexp slprt mxwt lwt`) and `usr/src/uts/common/disp/ts.c` (`ts_update`: "Called once per second via timeout", `timeout(ts_update, NULL, hz)`). Commit de1199e40761fcb5ed5cf82b16414ce4e4840999 (2026-09-05). Man page: illumos.org/man/5/ts_dptbl ("The length of the time quantum allocated to processes at this level in ticks (hz)"). Accessed 2026-09-07.
- role: existence claim only — a shipped MLFQ (Solaris/illumos Time-Sharing class) is table-driven with per-level quanta and a once-per-second aging pass. Bounded the boot default's `num_queues` and `boost_interval_us` from the other side (60 levels; ~1 s aging) until 2026-09-11, when the boot default became OSTEP's example whole; one point of the RQ0 gate spec's boot-default sensitivity sweep (`harness/boot-defaults/ostep-slice-2000us.json`, 8.8); does not name our values. At the default `hz` of 1000 the table's quanta are 2 ms (highest priority) to 20 ms (lowest); the 20-to-200 ms figures in OSTEP §8.5 and in Arpaci-Dusseau's Solaris 2.6 handout are the same tick table at 100 Hz. For the described millisecond ranges cite `ostep` §8.5, not this source.
- status: verified (2026-09-07; source and man page read)

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
- role: mechanism line — userspace scheduling delegation. Kernel side is "implemented as a scheduling class, akin to the commonly used CFS class"; the kernel "exposes thread state to the agents via messages and status words" and agents "instruct the kernel on scheduling decisions via transactions and system calls" (§3). Transactions exist because a syscall "in theory, would suffice" only for the per-CPU case (§3.2). Safety is three layers: ghOSt's class sits at "a lower priority than the default scheduler class — typically CFS" so "most threads in the system will preempt ghOSt threads"; destroying an enclave "automatically moves all threads in the destroyed enclave back to CFS"; and "the kernel will destroy an enclave when it detects an agent has not scheduled a runnable thread within a user-configurable number of milliseconds" (§3.4). Overheads (Table 3): 265 ns message delivery to a global agent, 888 ns to schedule a thread locally, against 599 ns for a CFS context switch; "just a single ghOSt agent to schedule over 2 million threads per second" (§1). **Carry the evaluation's conditions wherever the headline number is cited**: the intro's "5-30% better tail latency than MicroQuanta" is the 64 kB case at the 99.9th percentile and above, while for 64 B messages "For 99.99% and above, ghOSt latencies are up to 1.7× worse" (§4.3); on Search, "Prior to socket- and CCX-aware optimizations, the ghOSt policy led to nearly 2x worse latency for query type A" (§4.4). Against Shinjuku it is "within 5% of Shinjuku's saturation throughput", not ahead (§4.2).
- status: verified (2026-09-12; full 17-page SOSP '21 PDF read from the first author's institutional page, cs.stanford.edu/~jhumphri/documents/ghost.pdf; pp. 588 and 604 confirmed from the printed page numbers. Supersedes the 2026-08-26 bibliographic-only check.)

### `decima-sigcomm19`
- cite: Mao, H., Schwarzkopf, M., Venkatakrishnan, S. B., Meng, Z., & Alizadeh, M. (2019). Learning Scheduling Algorithms for Data Processing Clusters. *Proc. SIGCOMM '19*, 270–288. DOI 10.1145/3341302.3342080.
- role: learned-schedulers line (RL over job DAGs). **Cite the abstract's numbers only with the body's conditions.** The 21% is over "the closest heuristic ('opt. weighted fair')" in the batched-arrival experiment — 20 unseen TPC-H jobs, six input sizes, "23% of the jobs contain 82% of the total work" (§7.2) — not over Spark's default, and that baseline is itself tuned per experiment by sweeping "α ∈ {−2,−1.9,…,2}" (§7.1). The "up to 2×" is the busy window of the continuous-arrival experiment (1,000 TPC-H jobs, Poisson arrivals at 45 s mean, ~85% cluster load), "particularly during the busy period in hours 7–9"; that experiment's overall figure is 29% (§7.2). Scope of the learning: Decima "focuses on DAG scheduling (i.e., which stage to run next) and executor allocation", leaving per-task selection to Spark (§3); actions are two-dimensional, "(i) a stage designated to be scheduled next, and (ii) an upper limit on the number of executors" (§5.2); the reward is "r_k = −(t_k − t_{k−1})J_k", justified "by Little's law" (§5.3). Training cost, for the retraining argument: "we train Decima for at least 50,000 iterations for all experiments", each "roughly 1.5 seconds" with 16 parallel workers on a Xeon E5-2640 + Tesla P100 (Appendix C) — §7.4 gives "about 5 seconds" per iteration for the continuous-arrival setting and the paper does not reconcile the two. Training runs on a simulator, validated to "within 5% of real runtime when jobs run in isolation, and within 9% when sharing a cluster" (Appendix D).
- status: verified (2026-09-12; full SIGCOMM '19 PDF read from the first author's MIT CSAIL page. Supersedes the 2026-08-26 bibliographic-only check.)

### `firm-osdi20`
- cite: Qiu, H., Banerjee, S. S., Jha, S., Kalbarczyk, Z. T., & Iyer, R. K. (2020). FIRM: An Intelligent Fine-Grained Resource Management Framework for SLO-Oriented Microservices. *Proc. OSDI '20*, 805–825.
- role: learned-schedulers line (SLO-driven microservices). The abstract's four benchmarks are DeathStarBench's Social Network, Media Service and Hotel Reservation plus Train-Ticket's Booking Service, "36, 38, 15, and 41 unique microservices, respectively" (§4.1). **The abstract's three "up to" figures are range endpoints**: against two baselines (Kubernetes autoscaling and an AIMD method) FIRM "Outperformed both baselines by up to 6× and 11×, which leads to 9× and 16× fewer SLO violations" — so 16× is against the weaker of the two — and "Lowered the overall requested CPU limit by 29–62%" (§4.4). Controlled resources are "CPU time, memory bandwidth, LLC capacity, disk I/O bandwidth, and network bandwidth" plus container count (§3.4), actuated through existing Linux facilities (cgroups `cpu.cfs_period_us`/`cpu.cfs_quota_us`, Intel MBA/CAT, the blkio subsystem, HTB queueing) (§3.5). Training needs a "performance anomaly injection framework that triggers SLO violations by generating resource contention with configurable intensity and timing" (§3).
- status: verified (2026-09-12; full OSDI '20 PDF read from usenix.org/system/files/osdi20-qiu.pdf. Supersedes the 2026-08-26 bibliographic-only check.)

### `park-neurips19`
- cite: Mao, H., et al. (17 authors). (2019). Park: An Open Platform for Learning-Augmented Computer Systems. *NeurIPS 32*, 2490–2502.
- role: learned-schedulers line (platform), and **the citation for why this project does not take a learning-based approach**. §3 enumerates four difficulty classes in the authors' own words: (3.1) the "needle-in-the-haystack problem", where "the majority of the state-action space presents little difference in reward feedback for exploration", and representation, where "finding the right representation for each problem is a central challenge, and for some domains, e.g., query optimization, remains largely unsolved"; (3.2) input-driven variance, where "the agents cannot tell whether two reward feedbacks differ due to disparate input processes, or due to the quality of the actions", and the infinite-horizon problem, since production systems "are long running and host services indefinitely"; (3.3) the simulation-reality gap — cost-model accuracy that "quickly degrades as the query gets more complex", interaction that "would take a single-threaded agent more than 10 years to complete training in reality", and live deployment that "can degrade the system performance"; (3.4) understandability, since "for system problems, many reasonable good heuristics exist" that are "easy to understand and to debug, whereas a learned approach is often not", with the suggested remedy that "a learned scheduling algorithm could fall back to a simple heuristic if it detects that the input distribution significantly drifted". Table 2 names all twelve environments (adaptive video streaming, Spark cluster job scheduling, SQL query optimization, network congestion control, network active queue management, Tensorflow device placement, circuit design, CDN memory caching, multi-dim database indexing, account region assignment, server load balancing, switch scheduling); seven use real systems, five a simulator. Title is "Learning-Augmented", not "Learned". First author is Decima's first author, so this is the lineage's own account of its limits, not an outside critique.
- status: verified (2026-09-12; full NeurIPS 32 PDF read from proceedings.neurips.cc. Supersedes the 2026-08-26 abstract-only check.)

### `asa-arxiv25`
- cite: Wang, X., Jia, S., Huang, Z., Cao, J., & Song, M. (2025). Mixture-of-Schedulers: An Adaptive Scheduling Agent as a Learned Router for Expert Policies. arXiv:2511.11628 (v1, submitted 2025-11-07; no venue).
- role: closest architectural prior — recognize-then-route atop sched_ext, behavioral channel; our difference is the identity/world-knowledge channel. **The channel is the only difference we may claim, and two earlier framings must not be used.** (1) The machine-specific mapping table is *not* hand-maintained: §4.3 builds it by running every candidate scheduler through the test scenarios and recording the best per scenario, and §4.4 ports it to new hardware "By exclusively running the 'Generalization Model Training' (Stage 3) on the target machine … resulting in the creation of a precise, hardware-specific scheduler mapping table". The abstract's "without expensive retraining" refers to the recognition model only; a per-machine measurement pass remains. (2) ASA **does** report recognition accuracy separately from end-to-end performance — "the base model correctly identifies the running workload scenario with 96.83% accuracy", rising to 99.19% after fine-tuning (§5.3, §5.5) — so "measuring recognition itself has no analogue in prior work" is true of the LLM line (`schedcp-mlsys25`) but false of this one. What ASA reads is Table 1: CPU/memory/disk/process/scheduling/network counters, including window-focus CPU and memory use and input events, from eBPF, procfs and GNOME Shell — **no process identity anywhere in the feature set**. Expert set: scx_p2dq, scx_bpfland, scx_nest, scx_lavd, scx_simple, scx_flash, scx_rusty, against EEVDF. Benchmark: 28 scenarios pairing 4 interactive applications with 7 background workloads, on 10 VMs (4 prototype, 6 unseen). Decision window W = 6 s, chosen from a U-shaped delay curve with a "Pareto-optimal range between 4s and 7s" (§5.5). **Number discrepancy — use the body's**: the abstract says top-three in 78.6% of scenarios, §5.3 says 78.9%; the body also gives top-one 45.4% and average improvement +8.83% (95% CI [7.08%, 10.59%]), neither in the abstract.
- status: verified (2026-09-12; full text read from arXiv's HTML rendering of v1; version history and the empty journal-ref/comments fields confirmed on the abstract page the same day. Still v1, still no venue — re-check before submission.)

### `schedcp-mlsys25`
- cite: Zheng, Y., Hu, Y., Zhang, W., & Quinn, A. (2025). Towards Agentic OS: An LLM Agent Framework for Linux Schedulers. arXiv:2509.01245 (v4, submitted 2025-09-30); ML for Systems 2025 (arXiv journal-ref).
- role: closest LLM-scheduling prior — agentic policy synthesis for servers; our differences: signal-not-policy contract, desktop setting, recognition measured directly. **Quote v4, and mark anything taken from the long v2 as such** — v2 is the conference-length manuscript, v3/v4 the workshop-length one, and they differ in citable ways: the manuscript source's "all AI-generated code and configure before deployment" reads "code and configurations" in v4, and the post-optimization synthesis cost is "\$0.5" in the long version against "\$0.45 synthesis cost per workload" in v4. Long-version-only sentences include "In cloud platforms, system administrators who manage schedulers are not the developers who understand application behavior", the Planning Agent's three-case hierarchy, "a scheduler not present in our repository", "zero LLM overhead in the critical path", and the schbench before-numbers (13% worse P99, 46.1 ms vs 40.3 ms; 19% lower throughput, 741 vs 910 req/s). Present in v4: the four research questions, all four on end-to-end performance and cost, with **no question on recognition accuracy**; "All experiments successfully created working custom scheduler configurations or eBPF programs. Future evaluation requires a complete benchmark."; the kernel-compilation workload as "tinyconfig, 'make -j 172' on 6.14 source"; and the motivating failure — "Of three attempts, only one succeeded … required 33 minutes, 221 LLM API calls, and 15+ iterations, costing \$6 (vs. 5 minutes typically for an expert developer)". Scope limit on the RL comparison: v4's "Pre-trained RL approaches show no improvement" cites an LWN article on ML for kernel load balancing, **not** `decima-sigcomm19` or `park-neurips19`; do not read it as a head-to-head against those.
- status: verified (2026-09-12; v4 full text read from arXiv's HTML rendering; four-version history and the "MLforSystem 2025" journal-ref read from the abstract page the same day). **Successor check, 2026-09-12: none.** Every arXiv preprint carrying an author of this paper was enumerated; the group has published since (nearest: `gpu_ext`, arXiv:2512.12615) but nothing on Linux scheduler policy. Two adjacent works by other groups appeared after the 2026-08-26 check and are now minted as `tuxbot-arxiv26` and `vulcan-arxiv25`, both `provisional` — identified from their abstract pages, bodies unread. Re-check before every submission.

### `tuxbot-arxiv26`
- cite: Liargkovas, G., et al. (2026). TuxBot: Semantic-Aware Online OS Tuning with Large Language Models. arXiv:2605.15026 (v2, submitted 2026-07-14). **Preprint — no venue.** Comments field: "18 pages, 12 figures".
- role: adjacent LLM-in-the-loop OS tuning, minted 2026-09-12 by the standing re-check on `schedcp-mlsys25`; newer than, and distinct from, `tuneagent-arxiv25` in that it tunes a *live* host online rather than a build-time kernel configuration. Nearest point of contact with this work is the gating: "every proposed change passes through typed validation before reaching kernel or sysctl interfaces", which is the same move as our vocabulary-and-range validator. Reported scope: "13 live workloads from five benchmark suites while tuning up to 41 Linux parameters", "72.5%" over defaults and "153.3% relative to the strongest non-LLM baseline", at "about \$0.20" per 30-window session.
- status: **provisional (2026-09-12)** — identification and abstract read from the arXiv abstract page; full author list and body not read. Read the paper before citing, and decide which related-work subsection it belongs to.

### `vulcan-arxiv25`
- cite: Dwivedula, R., et al. (2025). Vulcan: Instance-specialized, Verifiable Systems Heuristics Through LLM-driven Search. arXiv:2512.25065 (v2, submitted 2026-06-16). **Preprint — no venue.** Comments field: "19 pages".
- role: adjacent LLM-synthesized systems policy, minted 2026-09-12 by the standing re-check on `schedcp-mlsys25`. The architectural parallel is the output contract: "LLM-generated code is restricted to simple stateless decision functions, while trusted runtime abstractions provide rich derived statistics", and synthesis happens "in a restricted language, Anvil, that guarantees important properties by construction" — narrowing what the model may emit so that verification becomes cheap, which is the same argument we make for a fixed signal vocabulary. **Domains are spot-VM scheduling, cache eviction and tiered memory, not CPU scheduling**; do not cite it as a scheduler.
- status: **provisional (2026-09-12)** — identification and abstract read from the arXiv abstract page; full author list and body not read. Read the paper before citing.

### `kgent-ebpf24`
- cite: Zheng, Yusheng, Yang, Yiwei, Chen, Maolin, & Quinn, Andrew. (2024). Kgent: Kernel Extensions Large Language Model Agent. *Proc. SIGCOMM 2024 Workshop on eBPF and Kernel Extensions (eBPF '24)*, 30–36. DOI 10.1145/3672197.3673434. ISBN 9798400707124; Sydney, NSW, Australia.
- role: LLM-agents-for-kernel-policy line. Author list differs from SchedCP's in two slots (Yang and Chen here; Hu and Zhang there), and the shared surname is spelled differently by the two papers: **Andrew Quinn here, Andi Quinn on SchedCP**. Keep both spellings as their papers give them and do not merge the two into one bibliography author — a reference manager will otherwise split or fuse them silently.
- status: verified (2026-08-26); given names, page range, ISBN and location re-confirmed 2026-09-12 from the authors' own BibTeX entry in the `eunomia-bpf/KEN` README. ACM DL was unreachable at that check, so the DOI record itself is unchanged from the 2026-08-26 verification.

### `tuneagent-arxiv25`
- cite: Lin, H., Li, Y., Luo, H., Lin, Z., Zhang, L., Xing, M., & Wu, Y. (2025). TuneAgent: Agentic Operating System Kernel Tuning with Reinforcement Learning. arXiv:2508.12551 (v2).
- role: adjacent LLM-in-the-loop kernel tuning. **The title, one author and the venue all changed after the 2026-08-26 verification, and the cite line above is v2, not the entry as first minted.** v1 (announced 2025-08-19) is titled *OS-R1: Agentic Operating System Kernel Tuning with Reinforcement Learning* and carries Kaichun Yao in the slot v2 gives to Zhenghong Lin; v2 (announced 2026-06-02) is the TuneAgent title and the author list above. The authors' repository (`github.com/LHY-24/TuneAgent`) names **KDD 2026** as the venue, so the former "(no venue)" line is retired: cite the conference if the acceptance is confirmed, and the preprint with its version otherwise. Per-benchmark numbers on that README are described there as the camera-ready's and are not verified against any paper.
- status: **to-pin (2026-09-12)** — the preprint side is now verified, the venue is not. v1 (submitted 2025-08-18) and v2 (submitted 2026-05-31) were both read from arXiv itself the same day, confirming both titles, both author lists (the fourth slot is the only change) and the rewritten abstract; the 5.6% headline is unchanged across versions, and arXiv's journal-ref and comments fields are **empty**. The KDD 2026 claim rests solely on the authors' repository README (`github.com/LHY-24/OS-R1`, which redirects from the renamed project), which reads "**KDD 2026** [paper]". ACM DL and dblp were both unreachable at that check. Pin the proceedings entry — page range and DOI — before any submission, or cite the preprint with its version.

### `jadhav-arxiv25`
- cite: Jadhav, P., Jin, H., Deelman, E., & Balaprakash, P. (2025). Evaluating the Efficacy of LLM-Based Reasoning for Multiobjective HPC Job Scheduling. arXiv:2506.02025 (v2, submitted 2025-09-03; comments field: "work under review").
- role: adjacent LLM HPC scheduling — the only work in this line that puts the model *in* the decision path, and the citation for why that is bounded: "a trade-off between reasoning quality and computational overhead challenges real-time deployment". Evaluation scope for the scale caveat: two models across "seven real-world HPC workload scenarios", compared "against FCFS, SJF, and Google OR-Tools (on 10 to 100 jobs)". (Alternate candidate if context meant benchmarking: arXiv:2511.11612.)
- status: verified (2026-09-12; version history, comments field and abstract read from the arXiv abstract page. Still v2, still unpublished.)

### `eevdf-tr95`
- cite: Stoica, I., & Abdel-Wahab, H. (1995). Earliest Eligible Virtual Deadline First: A Flexible and Accurate Mechanism for Proportional Share Resource Allocation. Technical Report TR-95-22, Old Dominion University. Kernel doc: docs.kernel.org/scheduler/sched-eevdf.html.
- role: behavioral-heuristics line — the current CFS successor's basis, and the definitions of the four terms the kernel's own documentation uses without defining. System virtual time is V(t) = ∫₀ᵗ 1/(Σ_{j∈A(τ)} w_j) dτ, so it "increases at a rate inverse proportional to the sum of the weights of all active clients" and "when the competition increases the virtual time slows down, while when the competition decreases it accelerates" (§4). Virtual eligible time and virtual deadline are "the corresponding starting and finishing times of servicing the request in the fluid-flow model"; "A request is said to be eligible if its virtual eligible time is less than or equal to the current virtual time"; the algorithm "simply allocates a new time quantum to the client that has the eligible request with the earliest virtual deadline" (§1). Eligible time is the paper's own contribution — virtual deadline "is also employed by other proportional-share algorithms", but "the concept of eligible time is a unique feature of our algorithm" (§1). Lag is "the difference between the service time that a client should receive at a time t, and the service time it actually receives", lag_i(t) = S_i(t⁰ᵢ,t) − s_i(t⁰ᵢ,t) (§2, Eq. 3). **The guarantee carries a condition — cite it with the condition.** Theorem 1: "The lag of any active client k in a steady system is bounded as follows, −r_max < lag_k(d) < max(r_max, q)"; Corollary 2 gives −q < lag_k(t) < q when no request exceeds a quantum; Lemma 5 shows those bounds hold for *any* proportional-share algorithm, so the result is optimality, not superiority. "Steady" is Definition 2: an interval in which "all the events occurring in that interval involve only clients with zero lag". Scope: the paper guarantees allocation accuracy, never interactive responsiveness.
- status: verified (2026-09-12; full 37-page technical report read from the first author's Berkeley page, people.eecs.berkeley.edu/~istoica/papers/eevdf-tr-95.pdf). Year is 1995 (not '96); the common misdating traces to the title-page footnote "Revised January 26, 1996."

### `ostep`
- cite: Arpaci-Dusseau, R. H., & Arpaci-Dusseau, A. C. *Operating Systems: Three Easy Pieces*. Arpaci-Dusseau Books. Chapter: "Scheduling: The Multi-Level Feedback Queue" (pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-mlfq.pdf).
- role: MLFQ textbook citation, and since 2026-09-11 the single source of the boot default's four MLFQ values, taken whole from its worked example (recognition-vocabulary §2, provenance table): the worked examples use "a three-queue scheduler" with a 10 ms top slice (§8.2, Fig. 8.2); Fig. 8.6's queues run 10 ms / 20 ms / 40 ms slices ("Lower Priority, Longer Quanta", §8.5); Fig. 8.4's example boosts "every 100 ms (which is likely too small of a value, but used here for the example)" (§8.3) and S is named a "voo-doo constant" after Ousterhout; Solaris TS described as "60 queues, with slowly increasing time-slice lengths from 20 milliseconds (highest priority) to a few hundred milliseconds (lowest), and priorities boosted around every 1 second or so" (§8.5). Rules 1–5 as restated in §8.6.
- status: verified (2026-09-07; PDF read; "[VERSION 1.10]", © 2008–23). Pin Version 1.10 at submission.

### `corbato-sjcc62`
- cite: Corbató, F. J., Merwin-Daggett, M., & Daley, R. C. (1962). An Experimental Time-Sharing System. *Proc. Spring Joint Computer Conference (AFIPS '62)*, 335–344. DOI 10.1145/1460833.1460871.
- role: MLFQ original (CTSS), and the source for how the original differs from the textbook form. The algorithm's purpose is overload behaviour, not throughput: without it "there is an abrupt collapse of service", and the design goal is "a saturation procedure which gives graceful degradation of the response time and effective real-time computation speed of the large and long-running users" (p. 340). Initial placement is **by program size**, not at the top queue: "Programs are initially entered into a level ℓ₀, corresponding to their size", ℓ₀ = [log₂([w_p/w_q] + 1)], chosen so that "a program is always operated for a time greater than or equal to the swap time" and hence "the computational efficiency never falls below one-half" (p. 341). Quantum at level ℓ is 2^ℓ quanta; demotion is on failure to respond, "if the program is not completed (i.e. has not made a response to the user)"; a newly occupied lower level returns the running program to the **head** of its own queue; a memory-size change recomputes the level. I/O waiters are demoted, not favoured: "programs which become dormant at level ℓ are entered into the queue at level ℓ+1 … continuing to cascade but not operating when they reached the head of a queue" (p. 342) — the opposite of modern MLFQ's sleep handling, because the rule exists to pick eviction victims. For the automatic-classification claim: "the level classification procedure for programs is entirely automatic, depending on performance and program size rather than on the declarations (or hopes) of each user" (p. 342). Contemporary values: "q = 16 m.s. (based on 1% switching overhead)" for the IBM 7090.
- status: verified (2026-09-12; scanned AFIPS proceedings PDF read in full, pp. 335–344, cseweb.ucsd.edu/classes/wi19/cse221-a/papers/corbato62.pdf. The scan's OCR renders ℓ, ℓ₀ and 2^ℓ unreliably; those symbols were disambiguated against MIT's author-hosted transcription at larch-www.lcs.mit.edu:8001/~corbato/sjcc62/, which matches the scan word for word in the surrounding prose. Quote from the scan, not the transcription.)

### `waldspurger-osdi94`
- cite: Waldspurger, C. A., & Weihl, W. E. (1994). Lottery Scheduling: Flexible Proportional-Share Resource Management. *Proc. First Symposium on Operating Systems Design and Implementation (OSDI '94)*, USENIX. PDF: waldspurger.org/carl/papers/lottery-osdi94.pdf (accessed 2026-09-07).
- role: LOTTERY algorithm origin, and the source that names no batch-class ticket ratio (recognition-vocabulary §2, `batch_share`). Not the grounding of LOTTERY `timeslice_us`, which follows the vocabulary's same-granularity rule (2026-09-11); the quantum sentence is kept as read: "the resource consumption rates of active computations are proportional to the relative shares that they are allocated" (§1); "With a scheduling quantum of 10 milliseconds (100 lotteries per second), reasonable fairness can be achieved over subsecond time intervals. As computation speeds continue to increase, shorter time quanta can be used to further improve accuracy" (§2). Names no ticket ratio between classes.
- status: verified (2026-09-07; PDF read)


### `liu-jacm73`
- cite: Liu, C. L., & Layland, J. W. (1973). Scheduling Algorithms for Multiprogramming in a Hard-Real-Time Environment. *Journal of the ACM*, 20(1), 46–61. DOI 10.1145/321738.321743. Scan with OCR text layer: cs.ru.nl/~hooman/DES/liu-layland.pdf (accessed 2026-09-09).
- role: EDF grounding for the prior driver table's periodic-consumer rows (`daemon/driver-table/prior.yaml`): assumption (A2), "each task must be completed before the next request for it occurs" — the period-implicit deadline the config schema uses; Theorem 7, "the deadline driven scheduling algorithm is feasible if and only if (C₁/T₁) + (C₂/T₂) + … + (Cₘ/Tₘ) ≤ 1"; the abstract's contrast with an optimum fixed-priority scheduler, whose utilisation bound "may be as low as 70 percent for large task sets". Cite for periodic tasks on one processor under its assumptions (A1)–(A5); it says nothing about behaviour above utilisation 1.
- status: verified (2026-09-09; OCR text read; JACM Vol. 20, No. 1, January 1973, pp. 46–61 confirmed from the running head)

### `miller-fjcc68`
- cite: Miller, R. B. (1968). Response time in man-computer conversational transactions. *Proc. AFIPS Fall Joint Computer Conference (FJCC '68)*, 267–277. DOI 10.1145/1476589.1476628. Scan: Computer History Museum collection (yusufarslan.net/sites/yusufarslan.net/files/upload/content/Miller1968.pdf, accessed 2026-09-08).
- role: the grounding of the interaction-latency threshold `T_interaction` = 0.1 s (harness/metrics.md §10). Topic 1, "Response to control activation": the response "should be immediate and perceived as a part of the mechanical action induced by the operator. Time delay: No more than 0.1 second."; for typed-text echo, "the delay between depressing the key and the visual feedback should be no more than 0.1 to 0.2 seconds", noting "this delay in feedback may be far too slow for skilled keyboard users". Cite for these two statements only; the paper's other seventeen topics carry other values.
- status: verified (2026-09-08; PDF text read, pp. 267–277 confirmed from running heads)

### `nielsen-ue93`
- cite: Nielsen, J. (1993). *Usability Engineering*. Academic Press. Chapter 5, "Usability Heuristics", response-time section — the author's own excerpt: "Response Times: The 3 Important Limits", nngroup.com/articles/response-times-3-important-limits/ (accessed 2026-09-08).
- role: secondary grounding of `T_interaction` = 0.1 s: "0.1 second is about the limit for having the user feel that the system is reacting instantaneously" (with the 1 s and 10 s limits beside it); the excerpt cites Miller 1968 and Card et al. 1991 as its sources. Cite the excerpt text as verified; the book's page numbers are not pinned.
- status: verified (2026-09-08; the author's excerpt read; book pages to-pin)

### `shneiderman-csur84`
- cite: Shneiderman, B. (1984). Response Time and Display Rate in Human Performance with Computers. *ACM Computing Surveys*, 16(3), 265–285. DOI 10.1145/2514.2517. PDF: cs.umd.edu/users/ben/papers/Shneiderman1984Response.pdf (accessed 2026-09-08).
- role: the range beside the threshold (harness/metrics.md §10): reporting Long [1976], "delays of approximately 0.1–0.5 second in the time for a keystroke to produce a character on an impact printer … unskilled and skilled typists worked more slowly and made more errors with longer response times. Even these brief delays were distracting in the rapid process of typing." A review reporting a primary study; cite as Shneiderman's report of Long, never as Long directly.
- status: verified (2026-09-08; PDF text read; volume/issue from the running foot)
