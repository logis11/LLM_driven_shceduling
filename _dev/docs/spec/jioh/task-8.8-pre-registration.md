# Task 8.8 — Pre-registration

The RQ0 gate spec committed as executable data, the scoring spec and the guard spec frozen, and the memo to 박이안 and 인경민. Parent: `_dev/TODO.md` (jioh, 8), sub-task 8.8; phase spec `phase-8-harness-upper-half-through-pre-registration.md` decisions 5, 12, 16, 17, 18, 19, 20, 21. Decided in the 2026-09-12 grill.

## Scope

- The RQ0 gate spec: judging and reporting files, the criterion's g and K, the seed count N, the boot-default sensitivity sweep, the executor-rule assumptions, the failure procedure with its file-selection rule, the reporting lines, the exemptions, the pins.
- The alternative boot-default files under `harness/boot-defaults/`, with a new reference entry for the sched_ext default slice.
- The freeze of the scoring spec and the guard spec in the harness tree's own changelog.
- The per-experiment spec schema and the RQ0 gate evaluator extended for the reporting lines this spec adds, recorded as a dated amendment to the 8.7 spec.
- The rename of "throwaway pool" to "driver table tuning set" outside the archives, the terminology entry, and the disjointness sentence in building plan §4.
- The vocabulary's sensitivity paragraph amended to the sweep, with a changelog entry; phase spec decision 12 amended.
- The memo to 박이안 and 인경민.

Out of scope: the driver table tuning set's composition rule and the calibrated table's tuning method (after Phase 9); any change to the metrics doc's floors, the guards' thresholds beyond the stated assumption below, or the `random` draw definition; the docs sweep (8.9).

## Locked decisions

### 1. Boot-default sensitivity is a pre-registered sweep, not a pair

The `fixed` condition is re-run under nine alternative boot defaults: the OSTEP MLFQ with only `timeslice_us` changed, at 0.5, 0.75, 0.9, 1.2, 2, 3, 5, 20, and 100 ms, the primary staying at 10 ms. The set is a backbone plus threshold points: the schema's two bounds and three shipped defaults (Linux's 0.75 ms base slice, illumos TS's 2 ms top quantum, sched_ext's 20 ms default slice) as the backbone, and one point either side of each step the judging set's periodic tasks have (the C2 gaming pair's 831 µs frame slack, c7-gaming's 1 470 µs longest stage, the C2 gaming pair's 2 176 µs longest stage, the 6 667 µs compositor burst) and of the 1 ms point where the post-boost window enters the wake-latency p99. Every point carries its reason in the RQ0 gate spec; the rendering marks the shipped values. Only the `fixed` run's MLFQ slice varies; the oracle and random runs stay on the primary and the pinned table. The sched_ext value is a new references.md entry verified against Linux v6.12's `include/linux/sched/ext.h`.

### 2. Executor rules committed as stated assumptions

The RQ0 gate spec commits, marked proposed 2026-09-11 and pending 인경민's answer: in EDF a waking deadline-class task preempts a residual task at once; when a residual slice boundary and a TIMER expiry fall on the same microsecond the wake is processed before the dispatch; the executor's starvation window is 1 000 000 µs, the starvation floor guard's threshold. The answers, when they arrive, are recorded in the spec; a changed value is a changelog entry before any run.

### 3. Judging set of 25; c7-meeting and c7-media reporting-only with a re-entry condition

Under decision 2's assumptions the two files' scored terms do not register their rows' difference by design, so by the judging rule (7.7, 2026-09-10) they leave the judging set and report as workload-bound note lines. The RQ0 gate spec states the re-entry condition: if 인경민's answers are slice-end waiting with dispatch before wake, both re-enter before any run as a changelog entry and K is restated by its reading. Phase spec decision 4 continues to govern any judging file found to have no headroom at scoring time.

### 4. g = 0.5, with its reading and a band

The per-file gap threshold is 0.5, read as: recognition accounts for at least half of the achievable improvement. It is a stated minimum effect of interest, fixed before execution; no source grounds it. A pre-registered reporting line prints the verdict count under g in {0.25, 0.33, 0.5, 0.67}, recomputed at scoring time. The RQ0 gate spec states the prior table's structure as a known property: 32 rows, 8 distinct configurations, 13 rows sharing the MLFQ cap-0.05 configuration, so on 13 judging files a uniform draw is the oracle's configuration 41% of the time and the gap there has a structural ceiling.

### 5. K = 13, a majority

The criterion reads: at least 13 of the 25 judging files show a gap of at least g. The reading is a majority of the judging files. On re-entry under decision 3 the number is restated to 14 by the same reading, before any run. K carries no band of its own; the report prints the count.

### 6. N = 100

The seed count is 100, grounded by two arguments written beside it: the worst-case sampling error of a file's mean random share is 0.05, one tenth of g, at a share spread of 0.5; and every one of the 32 rows is drawn with probability above 95%. A reporting line prints the per-file standard error of random's mean over seeds. Phase spec decision 20's clause applies: a changed N on measured simulator cost is a changelog entry before any run. N and the `random` reading are marked proposed to 박이안 and pending.

### 7. Failure procedure file selection

The configuration search of phase spec decision 17 runs on three files chosen by rule: the failing judging file with the largest oracle improvement over fixed in the duplicate-heavy class, the same in the low-duplicate class, and the failing file whose gap fell furthest below g anywhere; ties by workload id; files with no headroom are skipped for the first two picks since they already trigger the table check.

### 8. Tuning set: rename now, composition later

"Throwaway pool" is renamed "driver table tuning set" in every document outside the archives, and the terminology doc gains the entry. Building plan §4's open item 6 becomes one sentence: the driver table tuning set is disjoint from the coreset and the generalset, and its composition is fixed together with the calibrated table's tuning method, after Phase 9. Phase spec decision 18 is amended on that date to record the move. The harness's "throwaway experiment spec" of 8.6 is a different thing and is not renamed.

### 9. Reporting lines and exemptions carried

Carried as fields: the sensitivity sweep (decision 1), the floor band at 500, 1 000, 2 000, and 5 000 µs, the g band and the standard-error line (decisions 4, 6), the with-and-without-exclusion accuracy line, the Layer-1 headline, the random-beats-oracle line, the c7-gaming judging note, c1-gaming's separate line, the c7-meeting and c7-media notes, and the held-out-rows arm's "every row unless a stated reason excludes one" line. Layer-1 exclusions are the five annotated files, derived and linted. Reporting files are the preparation notes' list, with C5 and C6 run but unaggregated; a file the lint refuses for lacking scoring terms is left out with a note. The one exemption is c6-dual's provenance share under `oracle`, by construction.

### 10. Schema and evaluator extended for the new lines

The g band, the standard-error line, and per-point reasons on the sensitivity line are additions to the per-experiment spec schema and the RQ0 gate evaluator, with tests, so the three lines are in the machine-readable report. Recorded as a dated amendment to the 8.7 spec. The gate has not run, so the change is made in place.

### 11. Freeze and pins

인지오 freezes the scoring spec and the guard spec at version 1.0 in a new harness changelog. The RQ0 gate spec pins the SHA-256 of the scoring spec, the guard spec, the prior driver table, and the dataset build manifest at the freeze commit.

### 12. Vocabulary and phase spec amendments

The vocabulary's sensitivity paragraph is amended to the sweep and corrected on what varies (the `fixed` run's slice only), with a changelog entry. Phase spec decision 12 is amended on the date to the sweep.

### 13. Memo

One memo in Korean to 박이안 and 인경민, in the form of the earlier memos: the `random` reading and N pending 박이안; the three executor assumptions pending 인경민, restating the questions; the sweep as a harness-side change asking nothing of either; the invocation contract already sent on 2026-09-11.

## Invariants

- Every number in the RQ0 gate spec has its reason written beside it in the same file; every sensitivity point, threshold, and count included.
- Nothing in the RQ0 gate spec changes after execution begins except by changelog entry, and the two named pending items are the only ones expected to.

## Open items

- 인경민's three answers (decision 2) and 박이안's confirmation of the `random` reading and N (decision 6): Phase 9 prerequisites.
- The driver table tuning set's composition rule and the calibrated table's tuning method: after Phase 9.
