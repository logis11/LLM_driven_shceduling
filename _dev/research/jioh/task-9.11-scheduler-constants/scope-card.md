# Task 9.11 — Scheduler-side constants and groundings: scope card

Stage 1 of `_dev/research/jioh/research-slice-workflow.md`. Produced by the nightly research routine from issue #16. Repository state: `b29d1ec` on `jioh/dataset-rebuild`. Drawn from `docs/harness/metrics.md` §8–§11, `docs/recognition-vocabulary.md` §2, `harness/guards/guard-spec.yaml`, `harness/experiments/rq0-gate.yaml`, `harness/boot-defaults/*.json`, `docs/simulator/interpretation-contract.md:31`, `docs/memos/2026-09-11-boot-default-from-ostep.md`, `docs/memos/2026-09-12-rq0-pre-registration.md`, `docs/memos/2026-09-13-dataset-rebuild-heads-up.md`, `docs/references.md`, and from `../2026-09-13-verification/claims.md` (C-interbench-11, C-corbet-1…2, C-scx-1, C-schbench-1…2, C-hackbench-1…2, C-stress-ng-1, C-rt-app-2), `compare/K1.md`, `compare/K2.md`, `compiled-numbers-report.md` §1.4–1.5, §3.1, §3.3, §3.7–3.8, and `docs/memos/2026-09-13-critical-findings.md` (B7).

Verdict vocabulary is K1/K2's: SUPPORTED / WORDING-FIX / MISATTRIBUTED / NOT IN SOURCE / OURS-UNDER-SOURCE-TAG / CONTRADICTED / UNVERIFIABLE; the compiled audit's HOLDS / STALE / WRONG / UNCHECKABLE where the item is a statement about compiled behaviour. **NOT READ** marks an item 9.1 never read against its source: 9.1's claim inventory covered the dataset side and skipped `docs/memos/`, `harness/` and `docs/harness/` (`claims.md` Conventions), so every scheduler-side citation below except the Role B registry entries carries only its own `docs/references.md` status line, written by the author at the time of use. Kind is decision 1's labelling: source claim / convention / arithmetic / placeholder / design.

## Boundary

**In 9.11**

- Every constant of `docs/harness/metrics.md` §10, the arithmetic identities of §6.9–§6.10 (`W_single`, the boost grid), the statistics citations of §8, and the simulator behaviours §11 assumes.
- The boot default's provenance: the seven defaults of `recognition-vocabulary.md` §2 with their groundings, the allotment and same-granularity statements, the config schema's value ranges, and the comparison points memo 2026-09-11 §3 cites; the registry entries `ostep`, `illumos-ts`, `linux-sched-fair`, `linux-sched-ext`, `linux-sched-bwc`, `waldspurger-osdi94`.
- The boot-default sweep's backbone citations: the five points that rest on a source or a schema bound (`rq0-gate.yaml:70–79`, `harness/boot-defaults/`).
- Every `grounding` of `harness/guards/guard-spec.yaml`.
- The Role B registry entries named by the issue: `corbet-lwn24`, `scx`, `schbench`, `hackbench`, `stress-ng`, and interbench's reported statistics and jitter threshold (C-interbench-11).
- The TIMER primitive's backlog semantics as attributed to `rt-app` (`interpretation-contract.md:31`, C-rt-app-2), because the hand-off from 9.5 (below) lands on it.
- Hand-offs from 9.5 D11 and 9.6 D17 (below).

**Out of 9.11**

- To 9.14 (RQ0 gate spec rework): where each sweep point sits against the compiled files' behaviour — the four threshold points 900 / 1 200 / 3 000 / 5 000 µs and their reasons, the 831 µs "frame slack" (compiled audit S1, WRONG), the "1 ms post-boost point" (arithmetic on the boost, not the workload) — and every number of the RQ0 gate spec that is not a sweep citation: g = 0.5 and its band, K = 13, N = 100, the judging set, the floor band's use. They move again with 9.4–9.10's fold-ins.
- To 9.14 (guard spec rework, consumers group): the `tick_count` guard as applied to compiled files — the chain part fires by construction on c2-p2a/p2b and near-certainly on c7-gaming (compiled audit G1, WRONG); the stimulus-count part depends on the rebuilt editors and on the keystroke-during-RUN rule (heads-up memo §4 question 3; simulator guide §9.1). 9.11 records the guard's grounding only.
- To 9.14: the prior table's rows and their reasons (`daemon/driver-table/prior.yaml`, `liu-jacm73` as the EDF rows' grounding), the pair review, the scoring spec's weights and windows; the heads-up memo's executor questions 1 (LOTTERY batch share when the editor's burst tail is batch class) and 2 (whether EDF chain stages are deadline or residual class), whose answers move prior-table reasons, not constants.
- To 9.12 (prose): `corbato-sjcc62`, `eevdf-tr95`, `schedext-docs`, and the related-work entries; the research proposal's §6.3 sentence as prose (its reading as a guard threshold is item 26 here); `grounding-sources.md:74`'s citation-tier placement of the LAVD/LWN pair.
- To 9.15: `docs/workload/source-vetting.md` and `grounding-sources.md` lines carrying the Role B verdicts (schbench's percentile list at `source-vetting.md:58`, hackbench/stress-ng wording, "LWN LPC 2025 coverage" at `:64`), `harness-and-records-guide.md`.
- To 9.13 (schema): a declared-scheduling-class field in the task model, if item 38 decides the baselines honour one.
- Not 9.11: `georges-oopsla07`, `kalibera-ismm13`, `maricq-osdi18` ground the measurement campaigns' stability rule (9.6 D24, verified 2026-09-19); they are no scheduler-side constant.

**Executor questions — numbering.** The issue says the `starvation_floor` grounding waits on "executor question 3 of `docs/memos/2026-09-13-dataset-rebuild-heads-up.md`". In that memo question 3 is the keystroke-during-RUN question (§4, lines 44–47). The starvation window is question 3 of `docs/memos/2026-09-11-boot-default-from-ostep.md` §5, carried as assumption (3) of `rq0-gate.yaml` statement `executor-assumptions` (`:140–141`) and recorded as UNCHECKABLE in `compiled-numbers-report.md` §1.5 and §3.3. The card reads the issue as meaning the latter.

## Items

### Harness and metrics constants (`docs/harness/metrics.md`)

| # | Item | Current value | Tag / grounding | Verdict | Kind | Compiled effect |
|---|---|---|---|---|---|---|
| 1 | `T_interaction` (§10) | 100 000 µs | `miller-fjcc68` Topic 1 ("No more than 0.1 second"; typed echo "0.1 to 0.2 seconds"); `nielsen-ue93` excerpt ("0.1 second is about the limit…", itself citing Miller 1968); `shneiderman-csur84` reporting Long 1976 (0.1–0.5 s delays slowed typists) as the range beside it | NOT READ (references.md: verified 2026-09-08, author's read; Nielsen's book pages to-pin; Miller read from a third-party scan) | source claim | `over_threshold` aggregate on `ready_wait(cause = wake)` rows (`aggregates.py:126`); **no scored term uses `over_threshold`** (scoring-spec aggregates are p99, miss_rate, progress, turnaround); it is also the comparison point in the `starvation_floor` grounding (item 27) |
| 2 | Latency floor (§10, §9) | 1 000 µs | "stated assumption, tied to no scheduler parameter (2026-09-11)"; formerly "half the slice" (boot-default memo §4.4) | — | convention (stated assumption); the floor band 500 / 1 000 / 2 000 / 5 000 µs is its defence (`rq0-gate.yaml:81`) | marks a term *no headroom* when the oracle's improvement is below it (share 1 in the sum, §9) |
| 3 | Fraction floor (§10) | 0.01 | "stated assumption: one percentage point" | — | convention | as 2, for miss rate, progress, completion, `over_threshold` |
| 4 | Bootstrap seed and repetitions (§10) | 20260911; 10 000 | "pinned, not estimated" | — | design (determinism rule) | Layer-1 interval bounds byte-identical on rerun |
| 5 | Interval level (§10) | 95 % | "convention" | — | convention | Layer-1 intervals |
| 6 | Percentile method (§8) | linear interpolation, position `(n − 1)·p/100` (numpy `linear`, R type 7) | none | — | convention | every P50/P95/P99 term |
| 7 | `W_single` (§6.9) | `timeslice_us · Σ_{l=0}^{q−2} growth^l`; 30 000 µs at the boot default | derived from the incoming entry's params | arithmetic (identity) | arithmetic | `switch_window` / `boost_window` length; reported, not scored |
| 8 | Boost grid (§6.10, §11 item 7) | `t_apply + k · boost_interval_us`, k ≥ 1; timer restarts at `t_apply` | "Confirmed with 인경민 on 2026-09-09" | — | arithmetic on a confirmed simulator rule | `boost_window` rows |
| 9 | §8 statistics citations | balanced accuracy on the binary attribute (`brodersen-icpr10`); MCC beside it (`chicco-bmcg20`); cluster bootstrap over files (`field-jrssb07`, consistency in the number of clusters); paired comparisons (`dietterich-neco98`) | references.md: all four verified 2026-09-11 | NOT READ | source claims for method choices | Layer-1 grades and intervals |
| 10 | §11 simulator assumptions | nine items: 1–3 sent to the simulator owner as trace-contract clarifications; 4–6 "mock-local choices that fill gaps the contracts leave open"; 7–9 "Confirmed with 인경민 on 2026-09-09" | memos 2026-09-07, 2026-09-08 | — | design (1–3 pending confirmation in the text; 4–6 ours; 7–9 confirmed) | the mock traces; every primitive's reading of a real trace |
| 11 | TIMER backlog semantics (`interpretation-contract.md:31`) | "drift-free (rt-app `timer{ref,period}`). Late iterations accumulate as backlog; they are not silently skipped" | `rt-app` | C-rt-app-2 WORDING-FIX (K1): the backlog rule matches rt-app's `"mode": "absolute"` only; the default relative mode skips the missed activation and re-anchors. 9.5 card item 30: interbench skips missed periods (`interbench.c:399–411, 424–433`); 9.5 D11: every real player found skips them | design attributed to a source | miss counting under contention (c7-media / c7-meeting: 600 of 3 600 video jobs under `fixed`, compiled audit H1) |
| 12 | `schbench` as the tail-latency precedent (references.md role: "tail-latency metric precedent (P99-focused reporting)") | cited by git URL `github.com/masoncl/schbench`, v1.0 | C-schbench-1, -2 | CONTRADICTED — the percentile list (20/50/75/90/95/99/99.5/99.9) is printed by no version; v1.0 prints p50/p90/p99/p99.9 for latencies and p20/p50/p90 for RPS. WORDING-FIX — v1.0 does one `usleep(100)` per request; the v1.0 tag exists only on git.kernel.org `mason/schbench`, not GitHub; "Copyright (C) 2016 Facebook". SchedCP's URL is kernel.googlesource.com | source claim (precedent) | none (prose: why the scored latency term is P99) |

### The boot default's provenance (`recognition-vocabulary.md` §2; memo 2026-09-11)

| # | Item | Current value | Grounding as written | Verdict | Kind | Compiled effect |
|---|---|---|---|---|---|---|
| 13 | MLFQ `num_queues` | 3 | `ostep` §8.2: "a three-queue scheduler" | NOT READ (references.md: verified 2026-09-07, Version 1.10) | source claim (a worked example) | every `fixed` run; every prior-table MLFQ row |
| 14 | MLFQ `timeslice_us` | 10 000 | `ostep` §8.2 Example 1: "with a time slice of 10 ms (and with the allotment set equal to the time slice)" | NOT READ | source claim (a worked example) | the primary boot default; B1 batch-class entry after one slice; EDF/LOTTERY slices by item 17; `W_single` |
| 15 | MLFQ `timeslice_growth` | 2 | `ostep` §8.5, Fig. 8.6: 10 / 20 / 40 ms | NOT READ | source claim (a figure) | lower-level slices; `W_single` |
| 16 | MLFQ `boost_interval_us` | 100 000 | `ostep` §8.3, Fig. 8.4: "every 100 ms (which is likely too small of a value, but used here for the example)"; "voo-doo constant" after Ousterhout | NOT READ | source claim with the source's own caveat | boost grid; `boost_window` rows |
| 17 | Allotment = slice | one fully consumed slice demotes | OSTEP Rule 4 demotes on the allotment; Example 1 sets it equal to the slice, Fig. 8.6 gives the top two levels two slices each | NOT READ | design (the one stated divergence from the example) | demotion timing under `fixed` |
| 18 | EDF `residual_timeslice_us`, LOTTERY `timeslice_us` | 10 000 each | same-granularity rule, "this project's, not a source's"; "No shipped EDF has a residual round-robin slice to cite (Liu and Layland's EDF is preemptive without a quantum)" | — (the premise about shipped EDF is a claim) | design | every EDF and LOTTERY row |
| 19 | LOTTERY `batch_share` | 0.15 | "No source names a batch-class share. `waldspurger-osdi94` … gives no ratio between classes" | NOT READ (a negative claim about the paper; references.md verified 2026-09-07) | placeholder ("assumption, unbounded") | every LOTTERY row's split |
| 20 | Waldspurger's 10 ms quantum | "a coincidence, not a grounding" (memo §4.3; references.md) | `waldspurger-osdi94`: "With a scheduling quantum of 10 milliseconds (100 lotteries per second)…" | NOT READ | source fact recorded, not used | none |
| 21 | `batch_bandwidth_cap` | `null` at boot; range 0.05–0.95 | `linux-sched-bwc` for the idea (existence only); "the range, the floor, and the class rule below are ours" | NOT READ (references.md: verified 2026-09-10) | existence claim + design | the cap rows of the prior table |
| 22 | Config schema ranges | queues 2–8; top slice 500–100 000 µs; growth 1–8; boost 10 000–10 000 000 µs; EDF/LOTTERY slices 500–100 000; `batch_share` 0.01–0.90 (`config_schema.py:44, 49, 53`) | frozen 2026-08-28; no source stated | — | design | clamping (validation rule 3); the sweep's two end points (item 25) |
| 23 | Memo §3 comparison points | "no standard setting": OSTEP "no easy answers"; Arpaci-Dusseau lecture notes on the Solaris TS table ("nobody knows how to set it well"); Silberschatz and Stallings give example numbers; "papers" call per-level doubling a convention. Shipped table MLFQs: illumos/Solaris TS (60 levels, 2 ms → 20 ms at hz = 1000, aging once a second into levels 50–59) and MINIX 3 (16 levels, 200 ms, one level up every 5 s). Non-MLFQ: Linux CFS/EEVDF 0.75 ms, sched_ext 20 ms, scx lavd 0.5–5 ms, bpfland 1 ms, rusty 1–20 ms; macOS, FreeBSD, Windows decay-usage priorities with no per-level slice table | memo §3 "2026-09-11에 원문을 직접 읽어 확인한 것만"; registry ids exist only for `ostep`, `illumos-ts`, `linux-sched-fair`, `linux-sched-ext` | NOT READ; **no registry entry** for MINIX 3, the lecture notes, Silberschatz, Stallings, the "papers", the three scx per-scheduler slices, macOS, FreeBSD or Windows | source claims (the argument for choosing OSTEP whole) | none directly; they are why items 13–16 are one source |

### The boot-default sweep's backbone (`rq0-gate.yaml:70–79`, statement `boot-default-sweep`)

| # | Point | Reason as written | Grounding | Verdict | Kind |
|---|---|---|---|---|---|
| 24 | primary, 10 000 µs | "OSTEP §8's worked example whole" | items 13–16 | NOT READ | source claim |
| 25 | 500 µs, 100 000 µs | "the config schema's lower / upper bound on the top slice" | item 22 | — | design |
| 26a | 750 µs | "Linux's base slice (linux-sched-fair)" | references.md: v6.6 `sysctl_sched_base_slice = 750000ULL`, comment "default: 0.75 msec * (1 + ilog(ncpus))"; v6.5 `sysctl_sched_min_granularity` the same | NOT READ (verified 2026-09-07). The comment scales the default by CPU count; whether 0.75 ms is the value a running kernel uses on a given machine is not stated in the reason | source claim (existence) |
| 26b | 2 000 µs | "illumos TS's top-level quantum (illumos-ts)" | `ts_dptbl.c` default table, quanta in ticks at hz = 1000 | NOT READ (verified 2026-09-07) | source claim (existence) |
| 26c | 20 000 µs | "sched_ext's default slice (linux-sched-ext)" | v6.12 `include/linux/sched/ext.h`: `SCX_SLICE_DFL = 20 * 1000000, /* 20ms */` | NOT READ (verified 2026-09-12) | source claim (existence) |

The threshold points (900, 1 200, 3 000, 5 000 µs) and the second reasons on 750 and 2 000 µs are 9.14's (Boundary).

### The guard thresholds' groundings (`harness/guards/guard-spec.yaml`, v1.0)

| # | Guard | Threshold | Grounding as written | Verdict | Kind |
|---|---|---|---|---|---|
| 27 | `provenance_share` | 0.5, below | "Stated assumption: 'mostly running fallback' (research-proposal §6.3) read as a majority of the run's time" | the proposal's sentence (`research-proposal.md:718`) says "70% of its configurations were fallbacks" — a count example, not a threshold; the guard reads time-weighted share | convention (stated assumption) |
| 28 | `starvation_floor` | 1 000 000 µs, at or below | "Stated assumption pending the executor's declared window: one second of virtual time, an order of magnitude above T_interaction" | compiled audit §3.3: UNCHECKABLE — depends on memo 2026-09-11 §5 question 3, unanswered (`rq0-gate.yaml` `executor-assumptions` (3): "Confirmation is a Phase 9 prerequisite") | placeholder (awaits 인경민's executor constant) |
| 29 | `utilisation_sanity` | 1.0, at or below; > 0 where scored | "Arithmetic: busy ≤ T_end" | compiled audit: HOLDS ("every scored file has nonzero demand") | arithmetic |
| 30 | `config_age` | structural | segment attribution (data-contracts §8) | — | design (structural) |
| 31 | `determinism` | structural | simulator-guide non-negotiable 4, data-contracts §9 | — | design (structural) |
| 32 | `tick_count` | structural | metrics §6.2 guard, stimulus count, deadline cross-check, `config_applied` against the schedule | compiled audit G1: WRONG (chain part, as applied to the compiled gaming files); UNCHECKABLE (stimulus part) — both 9.14's; the grounding sentence "a shortfall means a wake was lost" (metrics §6.2) is what this slice records | design (structural) |
| 33 | `validation_matches_provenance` | structural | data-contracts §8 | — | design (structural) |
| 34 | `c2_pair` | structural | rq0-preparation-notes stage 4.2; body hash (8.6 smoke run) | compiled audit §3.3: HOLDS | design (structural) |

### Scheduler-side registry entries from the claim inventory

| # | Entry | Claim | Verdict (K1/K2) | What it grounds today |
|---|---|---|---|---|
| 35 | `corbet-lwn24` | C-corbet-1: LWN "Sched_ext at LPC 2024" (2024-09-26) as prose-citable secondary for the LAVD characterisation; C-corbet-2: the later article 1051430 | C-corbet-1 WORDING-FIX (qualitative only; its "typically no more than 100µs" differs from slide 13) and MISATTRIBUTED ("LWN LPC 2025 coverage", `source-vetting.md:64`); C-corbet-2 SUPPORTED, byline Jake Edge (2026-01-07), not Corbet. The references.md role line already carries the WORDING-FIX (9.4) | prose only |
| 36 | `scx` | C-scx-1: repository and licence | SUPPORTED; "pin commit" still open (no commit pinned in the repo text); 4 files dual-licensed | prose; the watchdog statement (references.md role) |
| 37a | `hackbench` | C-hackbench-1, -2 | SUPPORTED except: licence WORDING-FIX (GPL-2.0-or-later), `github.com/jlelli/rt-tests` UNVERIFIABLE, "load-balancing stressor" WORDING-FIX | the role "many-task IPC burst model" grounds no archetype (memo B7: no IPC archetype exists, no rejection record) |
| 37b | `stress-ng` | C-stress-ng-1 | WORDING-FIX ("no behavioral timing" too strong: the `workload` stressor emulates bursty scheduled compute); "widely cited" UNVERIFIABLE; licence WORDING-FIX | the role "fallback archetypes only" grounds no archetype |
| 37c | `interbench` C-interbench-11 | reported statistics, "~7 ms human jitter threshold", 30 s default | SUPPORTED per the man page; R01 code caveats: the mean is taken over all samples, the "SD" formula approximates RMS latency, **interbench cites no source for 7 ms**, 30 s is per benchmark/load pair rounded to 10 s | prose only; no harness or metrics constant cites it (grep of `docs/harness/`, `harness/` at `b29d1ec`) |

`schbench` is item 12.

### Hand-offs into 9.11

| # | From | Question | State |
|---|---|---|---|
| 38 | 9.6 D17 | `tracker-miner-fs-3`'s real threads run `SCHED_IDLE` at nice 19 (taskstats, all four repeats); `clamscan`, `ffmpeg`, `HandBrakeCLI`, `python3` run at the default policy. "The task model carries no declared class, so a simulated baseline cannot honour it." Whether the simulated baselines honour a task's declared class, and so whether the task model gains a field (schema: 9.13) | open; the neutral topic is what a stock Linux scheduler does with a `SCHED_IDLE` / nice-19 task beside default-policy work (T9) |
| 39 | 9.5 D11, 9.5 card item 30 | our TIMER backlogs missed periods where every real player found skips them | merged with item 11; open |
| — | 9.5 card, "To 9.11" | interbench's statistics and jitter threshold "if any harness constant cites them" | none does (item 37c) |
| — | 9.6 card, "To 9.11" | "nothing identified" | — |
| — | 9.7, 9.8, 9.9 changelogs and cards | no `9.11` hand-off (grep at `b29d1ec`) | — |

Slices that may still add hand-offs after this card's commit: 9.5 (`[WIP]`, decision session open), 9.10 (unstarted), 9.12 (unstarted). 9.4, 9.6, 9.7, 9.8, 9.9 are ticked in `_dev/TODO.md` at `b29d1ec`.

## What the sources are, as one observation

This slice has no single observation behind it. Its items are of four sorts: (a) one textbook's worked example taken whole (items 13–17, 24) — an illustration, not a measurement, and the source says so for the boost; (b) shipped-kernel constants read from source files at named tags (items 26a–c), each an existence claim about one project's default; (c) three human-factors texts behind one threshold (item 1), of which Miller 1968 is a design guideline, Nielsen 1993 a secondary restating Miller, and Shneiderman 1984 a review reporting Long 1976's experiment; (d) conventions, arithmetic and structural rules that no source is expected to ground (items 2–8, 18, 22, 25, 27, 29–34), plus two placeholders awaiting a number from outside the repository (item 19: no source exists by the entry's own words; item 28: 인경민's executor constant). Only (a)–(c) can be verified against a primary text; (d) is checked for being labelled as what it is.

No local source copies exist for (a)–(c): 9.1 read none of them, and the author's reads of 2026-09-07 to 2026-09-12 left no copy in this clone.

## Stage 2 topics

Neutral form, for the readers. Each is searched in the four classes of phase decision 4.

- **T1 Interaction-latency thresholds.** What published human-factors work states as the response-time limit below which a user perceives an interface's reaction to an input as immediate (keystroke echo, control activation, direct manipulation), with the value, the task, the population, and whether the value is an experimental measurement, a guideline, or a restatement of an earlier source. Includes Miller (AFIPS FJCC 1968), Nielsen (*Usability Engineering*, 1993, ch. 5), Shneiderman (ACM Computing Surveys 1984) and any later measured thresholds (e.g. touch or keyboard latency perception studies).
- **T2 A textbook MLFQ's worked example.** In Arpaci-Dusseau & Arpaci-Dusseau, *Operating Systems: Three Easy Pieces*, chapter "Scheduling: The Multi-Level Feedback Queue": the number of queues, the time slice, the per-level slice growth, the priority-boost period and the allotment rule used in its examples and figures, with the text's own remarks on how these values should be chosen; the version of the chapter read.
- **T3 Shipped scheduler time-slice defaults.** For each of: Linux CFS (`sched_min_granularity`, `sched_latency`) and EEVDF (`sched_base_slice`) in `kernel/sched/fair.c`; sched_ext's default slice constant; the illumos/Solaris time-sharing class's default dispatch table (levels, quanta, aging period) and its man page; MINIX 3's scheduler quanta and priority aging; the scx schedulers lavd, bpfland, rusty — the value, its unit, whether it scales with CPU count or clock rate, and the tag or commit it was read at.
- **T4 Lottery scheduling's quantum and class shares.** In Waldspurger & Weihl, OSDI 1994: the scheduling quantum used, and whether the paper states any ticket ratio between classes of work (interactive versus batch or background).
- **T5 Per-class CPU bandwidth ceilings.** Linux CFS bandwidth control (`sched-bwc`): what it limits, over what period, on what entity; any other shipped per-class CPU ceiling.
- **T6 Starvation bounds in shipped schedulers.** What bound, if any, shipped schedulers state on how long a runnable task may wait (e.g. sched_ext's watchdog timeout, Linux RT throttling `sched_rt_runtime_us` / `sched_rt_period_us`, the fair-server / deadline-server for fair tasks, illumos TS's starvation aging `ts_maxwait`), with the value and unit.
- **T7 Missed periods in periodic real-time and media tasks.** How periodic-task tools and players treat an activation that arrives after its period has passed — accumulate a backlog, skip to the next period, or re-anchor — in rt-app (`timer` event, its `mode` options), interbench's emulated audio and video loops, and at least one media player's frame scheduling (mpv, VLC, or GStreamer's sinks), with the code or documentation passage.
- **T8 Tail-latency and scheduler benchmark reporting.** What schbench (versions at the git.kernel.org repository and the GitHub repository) reports and which percentiles each version prints; what hackbench reports and its defaults; whether stress-ng has a stressor that emulates timing of real work; what interbench reports per task and whether it states a jitter perception threshold and its origin.
- **T9 Declared background scheduling classes.** How a stock Linux scheduler treats a task running under `SCHED_IDLE` or nice 19 beside default-policy tasks (weights, preemption, latency), per the kernel documentation and source; and whether desktop indexers, backup and scan tools ship with such a declared class by default.
- **T10 The statistics methods.** In Brodersen et al. (ICPR 2010), Chicco & Jurman (BMC Genomics 2020), Field & Welsh (JRSS-B 2007), Dietterich (Neural Computation 1998): the definitions and the scope limits each gives for balanced accuracy, the Matthews correlation coefficient, the cluster bootstrap, and paired comparison of two classifiers on one test set.
- **T11 CI observability.** Whether a GitHub Actions hosted runner can observe any of the above on its own kernel: the running kernel's effective `sched_base_slice` (debugfs or sysctl) and CPU count, whether sched_ext is available, the RT throttling and fair-server values, and the scheduling of a `SCHED_IDLE` task beside a default-policy CPU hog pinned to one CPU.

## Compiled numbers the decisions move

- Boot-default values (items 13–19) move every `fixed` run and, by the prior table's "params are boot values" rule, every one of its 32 rows (8 distinct configurations, `rq0-gate.yaml:153–164`, HOLDS). At 10 ms: c7-media / c7-meeting `fixed` 600 / 3 600 video misses (compiled audit H1); no C2 background task enters the batch class at 10 ms (c2-p2a download max chunk 6 944 µs; J1).
- `T_interaction` (item 1) moves no scored term; it moves `over_threshold` rows and the `starvation_floor` argument.
- The latency floor (item 2) moves which terms read *no headroom*; the floor band recomputes the verdict at 0.5 / 1 / 2 / 5 ms at scoring time.
- The TIMER rule (items 11, 39) moves every miss rate under contention; under a skip rule a late tick is dropped, under the current rule it is carried.
- `starvation_floor` (item 28) moves whether a run is `invalid` (evaluator `evaluator.py:314–336`), once the executor's window is known.
- A declared-class field (item 38) moves the indexing files and the P1 pair (`python3` default versus `tracker-miner-fs-3` `SCHED_IDLE`, 9.6 D17) — 9.10's and 9.13's once decided.
