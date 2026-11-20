# The RQ0 run

> Status: record · Created 2026-11-18 · Updated 2026-11-20

The record of the RQ0 run: the full matrix of the RQ0 gate spec (`harness/experiments/rq0-gate.yaml`) on the gated simulator and the real daemon, run once, cold, and its verdict read after the blind reading (sub-task 10.5, `_dev/docs/spec/jioh/task-10.5-the-rq0-run.md`). A rerun is appended below.

## The outcome

- **Verdict: fail, provisional.** At the primary, 6 of the 19 judging files met the criterion — a gap of at least g = 0.5 between the `random` seeds' mean and the `oracle` reference — against K = 10. The runner's exit code was 2.
- **A range over g.** The count moves inside the g band: 10 of 19 at g = 0.25 (pass), 8 at 0.33, 6 at 0.5 and 4 at 0.67 (fail). The verdict is reported as a range over g (the RQ0 gate spec's statement `g-grounding`).
- **The re-measurement contingency fired.** The carried-half-width line at the lower bound moves `c7-ml-train` across g (gap 2.512 at the primary, 0.000 at the bound), 5 of 19 met; at the upper bound 6. The verdict over that axis is the range 5 to 6, fail. The entry whose value moved it is re-measured at the count the statement `re-measurement-contingency` fixes, by a harness changelog entry and a second bless, in a later phase; the corner line moves every carried value the file holds at once, and which entry moved it is not yet identified. The result is not final until that re-measurement.
- **Link 2 stands.** Under the primary, 17 of the 19 judging files have headroom; the headroom-count line falsifies link 2 at 0.

## The run

| | |
|---|---|
| machine | the home M1 Pro, 16 GB; `workers` 4, `heavy_workers` 1, `heavy_mb` 50 (the smoke's) |
| commit | `6086e7e1` |
| RQ0 gate spec | SHA-256 `9cfad697e75b…`; the pins as the report lists them |
| programs | `simulator@0d323c84470a`, `daemon@62c71f0d2de0` — the integration gate's (2026-11-14) |
| N | 100 seeds per drawing condition |
| runs | 19,425; 37,863 program invocations executed, 987 from the execution cache, cold |
| started | 2026-11-16T08:57:02+0900 |
| the last run | 2026-11-18T03:10:48+0900 — 152,010 s of runs |
| the end stages | aggregates and scores 3,657 s, guards 2,491 s, grades 3,310 s, report 2,076 s |
| finished | 2026-11-18T06:23:03+0900 — **45 h 26 min** of wall time, against the projection's upper 50.33 h and the phase's budget of 80 h |
| disk | 325.9 GB free at the start, 71.5 GB at the finish (254.4 GB fewer), against the projection's mean 243.7 GB and upper 273.5 GB; `runs/rq0-gate` and `runs/.cache` 229 GB; `aggregates.csv` 73.37 GB against 73.19 GB projected |
| the blind reading | 06:23 to 06:58, clear |
| opened | 2026-11-18T11:14:21+0900 |

The projection is the 10.4 record's (`_dev/research/jioh/task-10.4-cold-smoke-and-cost-response/README.md`).

**N and the changelog entries behind the run.** N = 100 by the statement `n-grounding` — the worst-case sampling error of the seed mean, 0.05, one tenth of g; a single-row configuration undrawn in N seeds below 5 % from N = 95. The harness changelog's entries of 2026-11-15: the end stages reading the aggregates a run at a time; the cost response — the cost carried at N = 100, the C2 pair guard exempt on the C2 pairs' `oracle` runs under the cap band's tables, the longest-wait line's reopen condition leaving `ostep-slice-100000us` out, the starvation guard's two causes stated; before the RQ0 run — the wait check's rule in the statement `sensitivity-lines` and the `random` reading and N confirmed by 박이안 (statement `random-reading`).

**Starts and stops.** One start and one stop, the finish; no failed run, no run flagged slow, no interruption.

**Beside the run.** VS Code with the conversation the run was started from, and Spotify, throughout; a second VS Code window from about 22:11 on 2026-11-17, the swap in use rising from none at the start to 2.58 GB, 38 % of memory free, at 22:18 (1.86 GB and 66 % at 03:59 on 2026-11-18); AhnLab V3's `v3svc` at about a third of one core; a `docker-sandbox daemon` from about 12:00 on 2026-11-17, not started by 인지오, near zero CPU. At the start 78 % of memory was free and no swap in use.

## The blind reading

Read before the report, the verdict line and the exit code (`_dev/research/jioh/task-10.5-the-rq0-run/blind_reading.py`).

- **The guard table on the 1,938 runs the criterion reads** — each judging file's `fixed` run under the primary, its `oracle` run and its 100 `random` seeds: no non-exempt failure.
- **The longest-wait line's reopen condition**: no judging file's run past 15 s under a boot default it reads.
- **`simulator/tools/wait_check.py` on every trace** (2,110 s): on the criterion's runs no unread wait past 15 s.

Outside the criterion's runs, recorded with their runs: 110 `starvation_floor` failures — 4 on judging files' `fixed` runs under `ostep-slice-100000us` (`c1-ml-train`, `c1-transcode`, `c7-ml-train`, `c7-transcode`), 105 on the chain-scaled variants of `c2-p2a` and `c2-p2b` and on `c3-evening` (the `oracle` run and 20 `random` seeds each), 1 on `c3-creation` under `ostep-slice-100000us`; 101 `tick_count` failures on `c4-compile` (44 seeds) and `c6-dual` (57); the 9 exempt rows, 8 `c2_pair` and 1 `provenance_share`; 225 unread waits past 15 s — 98 after a preemption on `c6-dual` (16.0–22.7 s), 104 open at the end on the chain-scaled variants of `c2-p2a`, `c2-p2b` and `c7-gaming` (26.4 s), 21 on `c3-evening` (240.0 s), and two on `fixed` runs under `ostep-slice-100000us` (`c2-p1a` 38.7 s, `c7-ml-train` 205.0 s).

## The verdict's files

Under the primary; the reference is the `oracle` file score, the mean the `random` seeds', the gap one minus the mean over the reference.

| judging file | reference | `random` mean | gap | meets g | headroom |
|---|---|---|---|---|---|
| `c2-p1a` | 1.500 | 0.935 | 0.377 | no | yes |
| `c2-p2a` | 1.500 | 0.700 | 0.533 | yes | yes |
| `c2-p2b` | 1.000 | 0.200 | 0.800 | yes | yes |
| `c2-p3a` | 1.500 | 2.890 | −0.927 | no | yes |
| `c1-compile` | 2.000 | 2.272 | −0.136 | no | yes |
| `c1-ml-train` | 1.500 | 0.585 | 0.610 | yes | yes |
| `c1-render` | 1.500 | 1.724 | −0.149 | no | yes |
| `c1-transcode` | 1.500 | 4.616 | −2.078 | no | yes |
| `c7-browsing` | 1.000 | −0.121 | 1.121 | yes | yes |
| `c7-office` | 1.000 | −0.176 | 1.176 | yes | yes |
| `c7-dev` | 1.000 | 0.746 | 0.254 | no | yes |
| `c7-photo` | 1.000 | 1.000 | 0.000 | no | no term |
| `c7-meeting` | 1.000 | 0.721 | 0.279 | no | yes |
| `c7-gaming` | 1.000 | 0.573 | 0.427 | no | yes |
| `c7-video-edit` | 1.000 | 0.905 | 0.095 | no | yes |
| `c7-compile` | 1.000 | 0.931 | 0.069 | no | yes |
| `c7-ml-train` | 1.000 | −1.512 | 2.512 | yes | yes |
| `c7-render` | 1.000 | 1.000 | 0.000 | no | no term |
| `c7-transcode` | 1.000 | 0.877 | 0.123 | no | yes |

`random_beats_oracle` flags the four files whose gap is negative: `c2-p3a`, `c1-compile`, `c1-render`, `c1-transcode`.

## The reporting lines

The verdict count beside the primary's 6 of 19:

| line | values | count of 19 | verdict |
|---|---|---|---|
| boot-default sweep | the top slice at 0.5, 0.7, 1.2, 2, 5, 7, 12, 20, 30 ms | 4, 5, 5, 6, 3, 4, 9, 3, 6 | fail at every point |
| | 100 ms | — | not read: failed guards on the runs it reads |
| g band | 0.25, 0.33, 0.5, 0.67 | 10, 8, 6, 4 | pass at 0.25, fail above |
| floor band | 500, 1,000, 2,000, 5,000 µs | 6, 6, 6, 4 | fail |
| cap band | the unwanted rows' cap at 0.05, 0.2, 0.333, 0.5 | 6, 6, 7, 7 | fail |
| venue factor | ×0.8, ×1.25 | 7, 5 | fail |
| chain scale | ×1.2, ×1.4 | — | not read: `starvation_floor` failing on `c2-p2a@chain-x1.2`'s and `c2-p2a@chain-x1.4`'s `oracle` runs |
| first segment's length | 30 s, 120 s | 6, 7 | fail |
| carried half-widths | the lower bound, the upper bound | 5, 6 | fail; the re-measurement contingency fired |

- **Headroom count**: 17 of 19; `c7-photo` and `c7-render` have no headroom on their one term.
- **Seed standard error**, as a share of the reference: 0 to 0.337; above 0.05 on `c7-ml-train` 0.337, `c1-transcode` 0.219, `c7-browsing` 0.195, `c7-office` 0.141, `c2-p3a` 0.071, `c1-ml-train` 0.052.
- **Trace replay**: agreement false, tolerance 0.17 — `c2-p1a` 0.377 against 0.367 and `c7-meeting` 0.279 against 0.261 agree; `c7-browsing` 1.121 against 0.475 crosses g, `c7-dev` 0.254 against 0.000 differs past the tolerance. Stated beside the verdict as the compiled streams' ordering threat (the statement `sensitivity-lines`).
- **Bounding pair**: `c2-p2a` 0.533, meets g; `c2-p2a-idle` 0.000, no headroom on every term; the difference −0.533.
- **Longest wait**: 320.3 s, `c1-ml-train`'s `fixed` run under `ostep-slice-100000us`; no judging file's run past the reopen point under the boot defaults the condition reads.
- **Layer 1** (the grades file): `oracle` balanced accuracy 1.000 on the attribute, 177 graded queries over 114 files; `random` 0.508 on the attribute, 0.163 configuration correct, 0.066 mode accuracy, pre-committed misses excluded.
- **Input wake count**: the observations an interaction-latency P99 rests on, 49 (`c7-dev`) to 1,014,792 (`c1-transcode`).

## The files

- The report: `harness/experiments/rq0-gate/report.json.gz` (its uncompressed bytes' SHA-256 `309a13b4158454fbf2d0b64c5634176e964acfa19681bafaef05f76b01070206`) and `report.md` (`4a7ba21b736bd5de51b5c911ae9e571f61f0f1db28c7a0b7a7ce564b802b59ee`).
- The hash manifest: `harness/experiments/rq0-gate/runs.sha256.csv` — every run's trace hash and records hash, 19,425 lines.
- The run's operational record: `_dev/research/jioh/task-10.5-the-rq0-run/` — the launcher, the blind reading and the hash manifest's scripts; under `run/`, the start and the stop, the log, the run and stage times, the verdict line and the exit code, the blind reading's output, the opening.
- The run's outputs stay on disk, `runs/rq0-gate` and `runs/.cache`, through Phase 10's close.

## Reruns

None.

## Corrections

### 2026-11-18 — the scorer's sign (sub-task 11.1)

The run was scored with the oracle's improvement over `fixed` taken without its sign: a term was no headroom only when that improvement was under the aggregate's floor in size, so a term whose oracle was worse than `fixed` by the floor or more formed a share of inverted sign, and a condition better than `fixed` there scored below zero (`harness/CHANGELOG.md`, 2026-11-18). 58,140 of the run's 182,784 term rows are such terms; at the primary, a term of nine judging files. On `c7-ml-train` the editor's input-latency P99 is 7.194 s under `fixed` and 8.021 s under `oracle`; the `random` seeds' mean of −1.512 and the gap of 2.512 that met g are the inversion, `random` beating `oracle` there. On `c1-ml-train` the hog's turnaround is 2.958 s longer under `oracle` than under `fixed`.

The verdict above stands as run: fail, 6 of 19, provisional (`_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, decision 2). The re-measurement contingency fired under the scorer as run, and the entry that moved `c7-ml-train` is found under that rule (the same spec, decision 6).

**The post hoc reading**, not a verdict: `harness/experiments/rq0-gate/post-hoc/` — `report.json.gz` (its uncompressed bytes' SHA-256 `b4bc62393cd06e1497bd3d31d41fdf2503292e7496fb6e8ae945d6e933737753`) and `report.md` (`85469416ae6e0d4b5e5200668d8483cb2f495d5980280cd5bb3d197a07eb6a16`). The run's aggregates are re-scored under the fixed rule — a term whose oracle is worse than `fixed` by the floor or more is no headroom, at share 1, marked *oracle worse than fixed* — and the whole report rendered again with the run's own guards and grades.

- **4 of 19** judging files meet g at the primary: `c2-p2a`, `c2-p2b`, `c7-browsing`, `c7-office`. `c7-ml-train` has no headroom, gap 0.000; `c1-ml-train`'s gap is 0.468, its hog term at share 1.
- **12 of 19** have headroom. `c7-dev`, `c7-video-edit`, `c7-compile` and `c7-ml-train` have their one term oracle worse than fixed, and `c1-render` one of its two, the other under the floor; with `c7-photo` and `c7-render`, seven files have no headroom on any term.
- `c2-p3a`, `c1-compile`, `c1-transcode` and `c1-ml-train` have one term oracle worse than fixed beside one with headroom. `random` still beats `oracle` on the first three — gaps −0.613, −0.071, −2.011; `c1-render` is no longer flagged.

| line | the run | post hoc |
|---|---|---|
| g band, 0.25, 0.33, 0.5, 0.67 | 10, 8, 6, 4 | 8, 7, 4, 3 — fail at every point |
| boot-default sweep, 0.5, 0.7, 1.2, 2, 5, 7, 12, 20, 30 ms | 4, 5, 5, 6, 3, 4, 9, 3, 6 | 4, 5, 5, 5, 3, 3, 7, 3, 3; 100 ms not read, as in the run |
| floor band, 500, 1,000, 2,000, 5,000 µs | 6, 6, 6, 4 | 4, 4, 4, 2 |
| cap band, 0.05, 0.2, 0.333, 0.5 | 6, 6, 7, 7 | 4, 4, 4, 5 |
| venue factor, ×0.8, ×1.25 | 7, 5 | 5, 4 |
| chain scale, ×1.2, ×1.4 | not read | not read, the same failed guards |
| first segment's length, 30 s, 120 s | 6, 7 | 4, 5 |
| carried half-widths, the lower bound, the upper bound | 5, 6 | 4, 4 — neither bound moves the count |
| headroom count | 17 of 19 | 12 of 19 |
| `random` beats `oracle` | `c2-p3a`, `c1-compile`, `c1-render`, `c1-transcode` | `c2-p3a`, `c1-compile`, `c1-transcode` |
| trace replay | agreement false; `c7-dev` 0.254 against 0.000 | agreement false; `c7-dev` 0.000 against 0.000; `c7-browsing` 1.121 against 0.475, crossing g, as in the run |
| seed standard error above 0.05, as a share of the reference | `c7-ml-train` 0.337, `c1-transcode` 0.219, `c7-browsing` 0.195, `c7-office` 0.141, `c2-p3a` 0.071, `c1-ml-train` 0.052 | `c1-transcode` 0.214, `c7-browsing` 0.195, `c7-office` 0.141, `c2-p3a` 0.072 |

Unchanged: the guards, the longest wait, Layer 1, the exclusion accuracy and the input wake count, which read no score; the bounding pair (0.533, 0.000, −0.533), whose two files have no term oracle worse than fixed. The script and its summary: `_dev/research/jioh/task-11.1-the-scorers-sign-rule/`.

### 2026-11-20 — the fork-slot wait (sub-task 11.2)

The run's simulator, `simulator@0d323c84470a`, kept rule B1's counter across a fork-slot wait — B1 puts a task in the batch class from one full slice of CPU since its last voluntary block to its next one. A FORK that found `fork_cap` reached blocked its task without resetting that count, where a WAIT on its children resets it (`docs/memos/2026-09-09-batch-class-rule-for-the-simulator.md`, its 2026-11-19 correction). An orchestrator stayed in the batch class across those waits — `make` in `c1-compile` and `c7-compile`, 17,004 and 5,639 of them in the two files' `oracle` runs. Fixed as the simulator's stage AF, `simulator@841dc81131cb` (`docs/memos/2026-11-19-simulator-changes-by-jioh.md`). None of 11.2's fifteen cases — a judging file's term on which `oracle` is worse than `fixed` by the floor or more — is a defect; each is a property of the configuration (`_dev/research/jioh/task-11.2-the-degraded-oracle/cases.md`).

The verdict above stands as run.

**The criterion's 1,938 runs on the fixed simulator**, not a rerun of this run: a throwaway copy of the RQ0 gate spec pinning `simulator@841dc81131cb`, the criterion's runs with `c2-p1b` and `c2-p3b` beside them, which the C2 pair guard on `c2-p1a` and `c2-p3a` reads, scored under the fixed sign rule.

- `c1-compile` and `c7-compile` change, 101 of each file's 102 runs — the `oracle` run and the 100 `random` seeds. Their `fixed` runs and the other 17 files' runs are identical to this run's: the traces with the header line left out, the records with `sim` and `source_sha256` left out.
- At the primary the same nine terms have `oracle` worse than `fixed`; none new, none vanished. `c1-compile`'s editor input-latency P99 under `oracle` is 363.144 s against 361.025 s.
- 4 of 19 meet g, the post hoc reading's four. Every gap is the post hoc reading's but `c1-compile`'s, −0.069 against −0.071.

The comparison: `_dev/research/jioh/task-11.2-the-degraded-oracle/rerun-compare.json`.
