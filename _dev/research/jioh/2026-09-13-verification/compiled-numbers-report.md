# Audit: statements about compiled workload behaviour vs the current build

Audited 2026-09-13 against `main` at `e3d3c9a`. Read-only on the repo. All figures are from `dataset/build/coreset-single/` (what the RQ0 runner reads: `harness/runner.example.yaml:14`) unless marked native.

## 0. Ground truth state

- `python3 dataset/tools/compile.py --check` (run in a scratchpad venv with PyYAML + jsonschema, which the system Python lacks): **no drift, "manifest verified (100 artifacts)"**. `derive.py --check --require-coverage`: verified, 64 segments, 0 empty cells.
- In-process recompile of all 50 timelines × 2 modes with `compile_timeline`: **0 byte mismatches** with `dataset/build/` (`analyze.py` §1).
- SHA-256 of `dataset/build.manifest.json`, `scoring-spec.yaml`, `guard-spec.yaml`, `prior.yaml` all equal the pins in `harness/experiments/rq0-gate.yaml:223–226`. The dataset has not changed since Phase 7 (2026-09-10); `network-bulk.net_wait` has been 16,700 µs since `8416025` (2026-08-28), so the "~5.7 ms" figure was never a compiled value in any build these documents were written against.
- Slice context used for batch-class and MLFQ judgements: every prior-table row and the boot default use 10,000 µs (`prior.yaml` params; boot-default memo 2026-09-11 §4, which moved MLFQ `timeslice_us`, EDF `residual_timeslice_us` and LOTTERY `timeslice_us` from 2,000 to 10,000). Schema bounds for all three slice fields: 500–100,000 µs (`daemon/tools/drivertable/config_schema.py:44,49,53`). The boot-default sweep re-runs only `fixed` (cap null) at other slices.
- Batch-class rule used (batch-class memo §3): **B1** — a task enters the batch class once it has consumed one full slice of CPU since it last blocked voluntarily (a WAIT that has to wait, a SLEEP, a TIMER not yet due) and leaves at its next voluntary block; **B2** — a task with a TIMER, and every task reachable from one by WAKE, is never batch-class.

Reproduction (all in `_dev/research/jioh/2026-09-13-verification/`): `analyze.py` (recompile, per-task demand, chains, interactive bursts vs slices, IO jobs vs slices and completion, wineserver, c3-creation wakes, C2 identity), `extra.py` (compiler children, renderer ranges, uncontended keystroke overlap, batch-C1 turnaround feasibility, single-vs-native), `deliverable.py` (static vs deliverable-if-alone demand), `pairs.py` (C2 diffs), `misc_checks.py` (query points, baselines, child exposure, last-tick arithmetic), `mlfq_media.py` (minimal MLFQ replay of c1/c7-media and c1/c7-meeting), `dump.py` (per-task summaries).

### Verdict legend

- **HOLDS** — the stated number/behaviour matches the build.
- **STALE** — short for STALE-NUMBER-CONCLUSION-HOLDS: the number or supporting fact is wrong (stale or never true), but the conclusion drawn from it still stands against the current build.
- **WRONG** — the conclusion, or the stated ground of the decision it supports, does not survive the current build.
- **UNCHECKABLE** — depends on an executor rule that is not written yet (rule named).

---

## 1. Summary — WRONG and STALE items grouped by the decision they touch

### 1.1 RQ0 judging set / reporting-only classification

**WRONG**
- **J1 — c2-p2a fails the same test that moved c7-meeting and c7-media out of the judging set.** `rq0-gate.yaml:120–125` (`judging-set`) removes c7-meeting/c7-media because "their two EDF rows tie on every term". c2-p2a's two rows (gaming/true: EDF cap 0.333; gaming/false: EDF cap 0.05) differ only by cap, and in c2-p2a no task ever enters the batch class at the 10 ms slice: download chunks max 6,944 µs with a SLEEP after each; tails ≤ 699 µs then SLEEP; chain members are B2-periodic; steam/wineserver ≤ 455 µs. The cap has no target, so the two rows give the same schedule on c2-p2a. c2-p2a is still listed as judging (`rq0-gate.yaml:37`). The pair review's finding 1 knew the cap was inert on p2a (2026-09-09); the inconsistency arises from the 2026-09-12 application of the rule to c7-meeting/c7-media only.
- **J2 — c1-backup: "wanted LOTTERY share is what a random row removes, the turnaround term registers it"** (`phase-7 spec:72`, `building-plan.md:86`, `rq0-preparation-notes.md:541–543`, harness guide `:1132`). borg reaches a full 10 ms slice on 162 of 8,447 chunks (1.9%; 1.49% of its CPU), so backup/true's LOTTERY share and cap barely touch it; and borg cannot finish inside the file even alone (uncontended finish 132.2 s vs file end 60 s; ≤ 13.4 s of its 30 s by 60 s), so `bulk` turnaround is censored at `T_end − arrival` = 58 s under every condition (metrics doc §9: an unfinished job is scored on that censored bound) — the term cannot register any row difference.

**STALE**
- c1-gaming separate line (`rq0-gate.yaml:98–103`; `rq0-preparation-notes.md:597–603, 625–634`; `coreset-guide.md:530`): "demand 1.46, the highest in the coreset" (now c7-gaming 2.46, c7-mail 1.53, c7-office 1.50 are higher) and "no pair, so no attribute variation" (c7-gaming has been its label-flipped counterpart since 2026-09-10). Reporting-only still holds by the other half of the rule: c1-gaming has no batch-class task at 10 ms, so its cap-only row pair ties on it.

### 1.2 Expected "no headroom" statements

**WRONG**
- **H1 — c7-meeting and c7-media: "fixed ties too"** (`scoring-spec.yaml:25–30`; `rq0-gate.yaml:108–112` and `:123–125`; pair review `:72` item (2) and its last sentences; boot-default memo `:83`, `:103`, `:105`; pre-registration memo `:12`; `rq0-preparation-notes.md:577–585`; `coreset-guide.md:941`). The addendum's argument is that under `fixed` the only exposure is "the 100 ms boost lifting the scan to Q0 with a fresh slice, the same 10 ms worst case". The compiled phases add a second task: music/voice tick every 50,000 µs from t = 0, so a music/voice tick lands on **every** 100 ms boost instant, and the video tick lands 2k µs after boost k (6k × 16,667 = 100,002k). Under the MLFQ rule the repo states (switch memo, restated in boot-default memo §5: a wake into a higher queue preempts at once, into the same or a lower queue waits for the slice boundary) and the addendum's own "fresh slice" reading, video waits the scan's 10,000 µs plus music/voice's 2,500 µs and misses. Minimal replay (`mlfq_media.py`, both same-µs orders): `fixed` misses **600 of 3,600 video jobs** in c7-media and in c7-meeting; 0 in c1-media and c1-meeting. The EDF rows under the pending assumption (1) (deadline task preempts residual at once) miss none, so the video term (weight 0.5) has headroom against `fixed`. The two EDF rows still tie with each other, so the reporting-only classification itself is unaffected; the "no headroom on every term" expectation is not.
- **H2 — c1-backup's `bulk` turnaround is a guaranteed no-headroom term not listed** in the scoring spec's block "Expected 'no headroom' … stated here so it is not discovered later" (`scoring-spec.yaml:20–31`). See J2.

**UNCHECKABLE**
- c1-ml-train and c1-transcode turnaround: editor demand 28.34 s / 28.23 s + job 30 s against 58 s of lane between job arrival (2 s) and 60 s — the job can finish only if ≥ 0.34 s / 0.23 s of the editor's demand is left unserved at depart (simulator guide §9.4, depart mid-work, undecided). c1-indexing (+0.70 s) and c1-render (+3.88 s) are feasible; c1-compile has +25.7 s.
- c2-p2a download progress "expected no headroom" (`scoring-spec.yaml:112–114`): depends on EDF residual-class round-robin vs MLFQ; the ceiling is 3.38 s of the 25 s demand (progress ≤ 0.135).

**STALE**
- `scoring-spec.yaml:112` "runs ~1 ms then waits ~5.7 ms per chunk": compiled net_wait median 16,712 µs (mean 18,954); "never enters the executor's batch class and no row's cap acts on it" holds at 10 ms.

### 1.3 Driver-table rows (algorithm choice, cap and share derivations)

**WRONG**
- **T1 — "a keystroke-driven task blocks before its slice ends and stays on top under MLFQ"** — office/true `prior.yaml:67`; "the editor blocks on every keystroke and stays on top" dev/true `:119`; "the mail client's short bursts stay in the top queue" mail/true `:93`; the same premise in browsing/true `:41` ("serves the interactive job first and sinks CPU-bound work by observed behaviour") and in the unwanted-batch rows "one CPU-bound job under an interactive editor is MLFQ's textbook case" ml-train/false `:313`, indexing/false `:391` (and by the header rule `:12–13`). Compiled: 95.3% of c1-office writer bursts, 95.8% of c1-dev editor bursts, 96.2% of c1-mail mailer bursts are ≥ 10 ms (medians 89.7, 87.6, 84.3 ms); 91.4–92.5% of every editor's CPU lies past the first 10 ms of its bursts; and even with the lane to itself, 31–42% of keystrokes arrive before the previous burst has finished (c1-office 84/234, c1-dev 99/237, c1-ml-train 88/232, c2-p1a 254/774), so those WAITs never block. By OSTEP rule 4a the editor is demoted on nearly every burst and sinks with the CPU-bound job; the stated reason for MLFQ does not describe these files. (photo/true `:145` and video-edit/true `:249` state the long-burst reading and hold.)
- **T2 — borg is not what the backup rows and the p3 pair say it is.** backup/true `:399` "its share is a fifth — wanted, never starved" and `:405` "states a small guaranteed rate exactly"; backup/false `:411` "sink it and hold it to the floor" and `:417` "MLFQ sinks the CPU-bound job by demotion"; pair review §B p3 `:38` "the borg backup's 3 ms bursts outrun a 2 ms slice, so both are batch-class and both shares act"; pair review §C backup `:60` "so it is batch-class and both knobs act"; batch-class memo §4 `:55` "Run 3 ms, sleep 2 ms … batch for the last third of every burst — the cap bites, partially"; 2026-09-10 memo `:137`. Compiled borg: RUN median 2,995 µs (c1/c7-backup) / 2,968 µs (c2-p3b), SLEEP median 9,854 / 10,022 µs, duty 0.23. At the 10 ms slice 1.9% / 2.1% of chunks reach a full slice and 1.5% / 1.7% of borg's CPU is batch-class. So: the LOTTERY 0.2 share and cap govern almost none of borg (the batch class in these files is mostly the kdenlive editor's burst tails, 91.4–92.1% of its CPU); under MLFQ borg stays in Q0 by rule 4b while the editor (≥ 10 ms on 92.5–94.8% of bursts) is demoted, so backup/false does not sink borg or hold it to the floor; in p3 only render/true's share acts on its job.

**STALE**
- gaming/true `:191` "so the batch class gets a third": c2-p2a has no batch-class task at 10 ms (see J1); already disclosed by pair review finding 1; cap value unchanged.
- gaming/false `:203` "the only scored term being the chain's miss rate": c7-gaming also scores `compositor` miss rate 0.5 (`scoring-spec.yaml:229`); the "tightest cap" reasoning still holds (both terms are frames).
- office/false `:73` "(c4-office's 7z burst is the shape of it)": 7z is io-stream, duty 0.237, 2.6% of chunks reach 10 ms, so it is not the CPU-bound shape the floor cap acts on; the row is about c7-office's clamscan, which is.
- compile/false `:287` "MLFQ demotes each CPU-bound compiler child within a few slices": 37 of c7-compile's 100 children never run 10 ms at a stretch (never demoted, never batch-class); 68 never reach Q2. 72.0% of child CPU is past the first 10 ms, so the bulk of the build is demoted and capped.
- p2a download batch-class arguments — pair review finding 1 `:67`, batch-class memo §4 `:53` and §5 `:68`: "~1 ms of RUN per ~5.7 ms" (16.7 ms); "never consumes a 2 ms slice" (at 2 ms, 1,882 of 22,072 chunks do, 4.2% of CPU); "the conclusion holds under any rule, since a 1 ms chunk is shorter than every legal slice" (the legal minimum is 500 µs; 91.6% of chunks are ≥ 500 µs, 49.5% ≥ 1 ms; it holds only for slices ≥ 6,945 µs). Every row and the boot default use 10 ms, where 0 chunks reach a slice, so the decision (cap inert on p2a) holds for the pinned table.

**UNCHECKABLE**
- LOTTERY wanted rows "the editor keeps the other half / the rest": compile/true `:269`, ml-train/true `:295`, render/true `:321`, pair review §B p1 `:36` ("while the editor keeps two thirds"). Under B1 at 10 ms, 91.4–92.1% of the editors' CPU is batch-class, so during most of a burst the editor and the job are both batch; how LOTTERY splits tickets inside the batch class while the non-batch class is empty is not written (batch-class memo §7 item 3 leaves the cap-accounting window to the simulator).
- gaming pair "the chain's woken stages sit in the residual class beside the scan" (pair review §C `:52`, finding 5 `:71`): the recognition vocabulary §2 says the deadline class is "the TIMER-driven tasks"; batch-class memo B2 says the periodic class (TIMER tasks and everything WAKE-reachable) "is exactly the set EDF treats as its deadline class". The two rules disagree on chain stages 2–16; no executor rule settles it.
- EDF meeting/media rows "frames keep their deadlines … so it never steals one" (`:177`, `:235`): memo 2026-09-11 §5 questions 1–2 (EDF preemption of a residual slice; same-µs slice boundary vs TIMER).

### 1.4 Boot-default sweep point placement

**WRONG**
- **S1 — the 831 µs "frame slack" is not a behavioural step of the compiled files.** `rq0-gate.yaml:72` (750 µs "also below the C2 gaming pair's 831 µs frame slack"), `:73` (900 µs "between the 831 µs frame slack (c2-p2a, c2-p2b) and the 1 ms point"), `:197` ("frame slack"), pre-registration memo `:16`. 16,667 − 15,836 = 831 µs is chain-only arithmetic and correct, but the same lane carries the 284 tails at 0.1338 lanes (≈ 2,230 µs per frame, ≈ 632 wakes per second) plus steam and wineserver: average per-frame work is 18,066 µs against a 16,667 µs period already in the first minute, before the background task arrives. No frame has 831 µs of idle time, so a slice below or above 831 µs does not separate "fits in the slack" from "does not". 750 µs keeps its backbone reason (Linux base slice); 900 µs has no other reason.

**HOLDS** (numbers): 1,470 µs (c7-gaming chain.5), 2,176 µs (c2-p2a/p2b chain.14), 6,667 µs (compositor). Note beside 1,200 µs: c7-gaming's second-longest stage is 1,218 µs, also above the point, and 9 of its 16 stages lie between 1,016 and 1,470 µs, so the point sits inside a cluster rather than beside one step.

### 1.5 Guard validity (behaviour the guard spec's structural guards imply on compiled timing)

**WRONG**
- **G1 — the `tick_count` chain check fires by construction on c2-p2a and c2-p2b, and almost surely on c7-gaming.** `guard-spec.yaml:70–75, 159–168` ("the primitives' consistency checks (metrics doc §6.2 guard: a chain tail's iteration count equals its head's tick count …) … Any message is a fail"); metrics doc §6.2 "a shortfall means a wake was lost"; implemented `harness/tools/harness/primitives.py:257–274` (message whenever tail iterations ≠ head ticks consumed by `T_end`). c2-p2a/p2b: the head consumes its 7,200th tick at 119,985,733 µs, 14,267 µs before `T_end`, and a frame needs 15,836 µs of stage CPU, so that frame can never reach the tail inside the window; counts can match only if the head is kept off the lane for the whole last 14.3 ms while the chain is otherwise fully drained. c7-gaming: chain 14,999 + compositor 6,667 = 21,666 µs of periodic work per 16,667 µs period, so one of them backlogs under any policy; the check can pass only if the compositor, the scan and the tails are the ones starved and the chain finishes its last frame within the 468 µs margin (last tick 59,984,533 µs + 14,999 µs). `tick_count` applies to every condition with no exemption, and `harness/tools/harness/evaluator.py:314–336` makes the RQ0 verdict `invalid` when any non-exempt guard fails on a primary-boot run feeding a judging file. A shortfall here is load, not a lost wake.

**UNCHECKABLE**
- Stimulus-count part of `tick_count` (`primitives.py:287–292`: ready(wake) lines must equal the run file's wake events). An editor with unconsumed keystrokes at depart produces fewer lines. Editors demand 0.46–0.50 lanes and, even with the lane to themselves, finish their last burst at 57.8–58.3 s of a 60 s file (c1-backup, c1-dev, c1-ml-train, c1-office; `extra.py`), so under contention (C7 interactive counterparts at ~1.5 lanes, batch C1 bases, C2 p1/p3) a mismatch is plausible. Depends on simulator guide §9.1 (a wake arriving while the task is running: remembered with depth, or lost) and §9.4 (depart mid-work).
- `starvation_floor` grounding (`guard-spec.yaml:47–56`): the executor's starvation window is memo 2026-09-11 §5 question 3, unanswered.

### 1.6 Demand regime / demand window and "sized to finish"

**WRONG**
- **D1 — "every compiled -single workload of demand class oversubscribed lands in the measurable oversubscription regime"** (`building-plan.md:168`; `dataset/README.md:131`). The static estimate (`compiler.py:193, 216, 230, 253`) counts a finite job's full `total_work` and an IO job's CPU regardless of its blocked time or the file's end. Counting per task only the CPU it could receive alone by `T_end` (`deliverable.py`): c2-p3b 1.122 → 0.610, c3-creation 1.035 → 0.702, c3-workday 1.043 → 0.920, c2-p3a 1.122 → 0.997, c2-p2a 1.293 → 1.112, c2-p1a/b 1.204 → 1.148. Four of the ten oversubscribed-class files leave [1.00, 1.50]. c2-p3b's scored segment (60–120 s) carries at most ≈ 0.50 (editor) + 0.23 (borg alone) lanes.
- **D2 — "batch jobs are sized to finish inside the segment so the base carries a turnaround term"** (`building-plan.md:85`; `phase-7 spec:52` "turnaround where the job is sized to finish and progress otherwise"; `coreset-guide.md:573`; 2026-09-10 memo `:86` "어떤 policy든 lane의 절반이면 끝나요"). c1-backup's borg cannot finish even alone (132.2 s); half a lane from 2 s delivers 29 s < 30 s; c1-ml-train and c1-transcode need more lane than exists unless editor work is dropped (see 1.2). The rule as written should have given c1-backup `progress`.

**STALE**
- `building-plan.md:87` "c1-gaming lands inside the oversubscription regime … while the other five sit well below one lane": there are fifteen other C1 files; c1-ml-train, c1-transcode, c1-backup sit at 0.97.
- `coreset-guide.md:646` and `:981` give "chain이 lane의 95%를 요구하니 못 끝나요 (lane의 42%가 필요)" as the reason the download does not finish: it cannot finish alone (duty 0.056; uncontended finish at 503.3 s; 3.38 s of 25 s by 120 s). Conclusion holds.
- `rq0-preparation-notes.md:47–49` "13 novel + 11 derived timelines, all inside the demand window" (now 23 + 27; "inside" only by the static estimate).

### 1.7 Numbers in study documents that no decision rests on

- `coreset-guide.md:205`, `:642` "SLEEP ~5.7 ms" (16.7 ms); `:694` borg "SLEEP ~2 ms" (10.0 ms median; the guide's own `:176` says ~10 ms); `:211`/`:469` c1-office renderer periods "0.7–2.5 s" (0.45–9.68 s); `:487` c1-browsing renderer periods "1.1–4.1 s" (0.29–4.88 s); `:720` c3-workday renderers "0.6–10 s" (0.16–13.07 s); `:522` tails "SLEEP ~0.3–1.2 s" (0.11–3.0 s, median 0.49 s); `:986` "gamescope (c1/c4-gaming만)" (also c7-gaming); `:981` "judging set에서 turnaround는 관측 불가" (the six batch C1 bases judge with turnaround); `:1046` "judging set … C2의 6개" (25 files).
- `dataset/README.md:86` C2 pairs "behave identically and differ only in intent — … a game download vs. a virus scan": P2 is network-bulk (duty 0.056) vs cpu-batch; P3 differs in mode (render vs backup), both wanted.
- `rq0-preparation-notes.md:180–181` and `:325–326` "C2 pairs differ only in background_wanted": P1 differs in mode and attribute (ml-train/true vs indexing/false), P3 in mode only, P2 in attribute only. Conclusion (config search before workload redesign) unaffected.
- `harness-and-records-guide.md:1179` "이 파일은 gate에 안 들어가니" (c1-compile judges since 2026-09-10).
- Batch-class memo §7 item 6(a) unit test "1 ms then sleeping 5.7 ms".
- Not workload statements but stale in a pinned file: `prior.yaml:275, 301, 327, 353, 379, 405` "2 ms quantum per the boot value" beside `timeslice_us: 10000`.

---

## 2. Recomputed facts the verdicts use

| Fact | Value (single) | How |
|---|---|---|
| Editor bursts vs 10 ms slice | ≥ 10 ms: 90.3% (c1-indexing) to 96.2% (c1-mail); median 73.7–95.5 ms; CPU past first 10 ms 90.8–92.5% | `analyze.py` §4 |
| Keystrokes arriving before previous burst ends, lane to itself | c1-office 84/234; c1-dev 99/237; c1-backup 78/255; c1-ml-train 88/232; c2-p1a 254/774 | `extra.py` |
| c2-p2a download | 22,072 chunks; RUN med 993 µs, max 6,944; SLEEP med 16,712, mean 18,954; duty 0.056; alone finishes at 503.3 s; 3.382 s of 25 s by 120 s; reaches slice: 500 µs 91.6%, 1 ms 49.5%, 2 ms 8.5%, 3 ms 1.4%, 5 ms 0.1%, 10 ms 0 | `analyze.py` §5 |
| borg c1/c7-backup | 8,447 chunks; RUN med 2,995, max 28,905; SLEEP med 9,854; duty 0.230; alone finishes 132.2 s; 13.40 s of 30 s by 60 s; reaches 2 ms 75.4%, 10 ms 1.9% (1.49% CPU) | `analyze.py` §5 |
| borg c2-p3b | 21,078 chunks; RUN med 2,968, max 38,430; SLEEP med 10,022; alone 13.55 s of 75 s by 120 s; reaches 10 ms 2.1% (1.70% CPU) | `analyze.py` §5 |
| 7z c4-office | 1,651 chunks; RUN med 3,006; SLEEP med 9,803; finishes alone 55.3 s; reaches 10 ms 2.6% (1.93% CPU) | `analyze.py` §5 |
| mail send (c1/c7-mail, c3-workday) | net_wait med 16.5 / 17.1 ms; alone finish 91.4 s (file 60 s) / 452.6 s (file 420 s); never reaches 5 ms | `analyze.py` §5 |
| Chains (single) | c1/c4/c7-gaming: sum 14,999, slack 1,668, longest 1,470 (2nd 1,218); c2-p2a/b: sum 15,836, slack 831, longest 2,176 (2nd 2,143), head 230; c3-evening: sum 24,168 (lane_share 1.45), longest 2,440; c6-dual: sum 10,000, longest 1,090. Native: c1-gaming longest 1,094, c2 1,703 | `analyze.py` §3 |
| c1-gaming 1.4557 lanes | chain 0.8999 + compositor 0.4000 + tails 0.1549 + webhelpers 0.0008 + steam 0.0001 + wineserver 0.0000. Periodic chain + compositor alone = 21,666 µs per 16,667 µs = 1.30 lanes. c7-gaming = same + scan 1.0 = 2.4557. Native c1-gaming 1.2257 | `analyze.py` §2–3 |
| wineserver | c1/c4/c7-gaming SLEEP 1,225,245,899 µs → never runs in 60 s; c2-p2a/p2b SLEEP 2,117,324 / RUN 212 → 56 runs in 120 s; c3-evening SLEEP 457,381,676 → never runs in its 240 s life; c6-dual SLEEP 2,769,255 / RUN 583 → 86 runs. Bound to system-daemon in every file, never part of the chain | `analyze.py` §6 |
| C2 pair diffs | each pair differs in exactly one arrive event (hog / download / bulk) plus segment 2's label; P1 events identical apart from the name | `pairs.py` |
| single vs native | differ only in c1-gaming, c2-p2a, c2-p2b, c3-evening, c4-gaming, c6-dual, c7-gaming, and only in the 16 chain members' RUNs | `extra.py`, inline check |
| Compiler children at 10 ms | c1/c7-compile: 63 of 100 have a RUN ≥ 10 ms, 32 ≥ 30 ms, 72.0% of child CPU past first 10 ms; c3-workday 2,650/4,200, 87.5% | `misc_checks.py` §3 |
| Query points | 134 total, 50 terminal, 2 ambiguous, 82 graded in 49 files, 10 on pre-committed-miss segments; constant `true` 69.5%, majority mode (gaming) 11.0% | `misc_checks.py` §1 |
| c7-media / c7-meeting under `fixed` | 600 of 3,600 video jobs miss (both same-µs orders); c1-media, c1-meeting 0 | `mlfq_media.py` |

---

## 3. Per-document audit

Decision abbreviations: **JS** judging set / reporting classification; **NH** no-headroom expectation; **ROW** driver-table row choice; **CAP** cap/share value; **W** scoring weight or term choice; **SW** sweep point; **WIN** window placement; **EX** exemption; **G** guard validity; **DW** demand window.

### 3.1 `harness/experiments/rq0-gate.yaml`

| Loc | Statement (verbatim) | Recomputed | Verdict | Decision |
|---|---|---|---|---|
| 29–31 | "a file judges when it is one side of a label-varying pair and its scored term registers the rows' difference by design … — the three C2 pairs, the six batch C1 bases, and the C7 counterparts with a term, less c7-meeting and c7-media" | c2-p2a: no batch-class task at 10 ms, cap-only row pair ties (J1); c1-backup: share barely reaches borg, turnaround always censored (J2) | WRONG | JS |
| 32–35 | "Reporting (25): every other coreset file — … c1-gaming on its own line, the idle pair, C3, C4, and C5 and C6" | 25 listed; classes correct | HOLDS | JS |
| 49 | `layer1_exclusions: [c1-indexing, c7-backup, c7-ml-train, c7-render, c7-transcode]` "derived from the pre_committed_miss annotation in the compiled files" | exactly these five carry `pre_committed_miss: true` | HOLDS | JS |
| 56–60 | "c6-dual's ground truth is `mode: ambiguous` with no `background_wanted`" | gt `{mode: ambiguous, attributes: {dual_active: true}}` | HOLDS | EX |
| 72 | "also below the C2 gaming pair's 831 µs frame slack" | 16,667 − 15,836 = 831 ✓; tails add 2,230 µs/frame on average, so average per-frame work is 18,066 µs (S1) | WRONG (reason); backbone reason stands | SW |
| 73 | "between the 831 µs frame slack (c2-p2a, c2-p2b) and the 1 ms point where a slice after the 100 ms boost reaches 1% of the boost interval …" | as above; the 1 ms point is arithmetic on the boost, not the workload | WRONG (reason) | SW |
| 74 | "below c7-gaming's longest chain stage (1 470 µs)" | 1,470 ✓ (2nd 1,218 µs also above 1,200) | HOLDS | SW |
| 75 | "between c7-gaming's longest stage (1 470 µs) and the C2 gaming pair's (2 176 µs)" | ✓ | HOLDS | SW |
| 76 | "above the C2 gaming pair's longest chain stage (2 176 µs), below the 6 667 µs compositor burst" | ✓ | HOLDS | SW |
| 77 | "below the 6 667 µs compositor burst (c7-gaming)" | ✓ (compositor exists in c7-gaming, not in C2) | HOLDS | SW |
| 92–94 | "the base already needs 1.46 lanes; with the scan, frames miss under every row, so only the gap between rows reads" | base 1.4557 = chain 0.90 + compositor 0.40 + tails 0.155 (+0.001); frames miss under every policy already in the base (periodic work 21,666 µs / 16,667 µs) | HOLDS | JS (note) |
| 98–103 | "single-situation file at demand 1.46, the highest in the coreset … Not judging: no pair, so no attribute variation" | 1.4557 ✓; not highest (c7-gaming 2.46); c7-gaming is its pair; reporting still holds (no batch-class task) | STALE | JS |
| 108–112 | "TIMER consumers sit in the deadline class and one 10 ms residual slice equals video's tick tolerance exactly, and fixed no longer demotes the video burst, so on the arithmetic the rows tie and fixed ties too — no headroom on every term" | 16,667 − 6,667 = 10,000 ✓; video 6,667 < 10,000 never demoted ✓; rows tie under assumption (1) ✓; fixed: 600/3,600 video misses (H1) | WRONG ("fixed ties too") | NH, JS |
| 115 | "Same as c7-meeting." | same | WRONG (same part) | NH |
| 123–125 | "under the executor assumptions below their two EDF rows tie on every term and tie with fixed" | rows tie ✓; "tie with fixed" ✗ (H1) | WRONG (fixed part); classification holds | JS, NH |
| 135–142 | executor assumptions (1)–(3) | not workload statements | — | — |
| 153–164 | "32 rows carry 8 distinct configurations … Thirteen rows share MLFQ with cap 0.05 … on the 13 judging files whose scored segment maps to that row — the twelve C7 counterparts of the interactive and batch modes other than gaming, and c2-p1b — a uniform draw is the oracle's configuration 41% of the time … The other twelve judging files map to rows shared by at most three (9% or less)" | 8 configs (7+13+2+1+3+2+3+1); 13/32 = 40.6%; ground-truth rows of the 13 files ✓; others: sharing 3 (ml-train/true group, EDF 0.05 group), 2, or 1 | HOLDS | JS (structure) |
| 176–177 | "the chance a single-row configuration is never drawn in N seeds is (31/32)^N, below 5% at N = 95" | arithmetic, not workload | — | — |
| 196–198 | "one point either side of each step the judging set's periodic tasks have (frame slack, longest chain stage, compositor burst)" | frame slack not a step (S1); others ✓ | WRONG (frame slack part) | SW |
| 216–219 | held-out rows: "the row's C1 base for a true row, its C7 counterpart for a false row" | consistent with indexing's reversal (c1-indexing = true, c7-indexing = false) | HOLDS | — |
| 221–226 | pins | all four SHA-256 match | HOLDS | — |

### 3.2 `harness/scoring/scoring-spec.yaml`

| Loc | Statement (verbatim) | Recomputed | Verdict | Decision |
|---|---|---|---|---|
| 21–23 | "c1-media and C5 — no legal configuration can miss a tick (video needs > 10 ms of wait, music can cause 2.5 ms; music needs > 47.5 ms, video can cause 6.67 ms)" | files hold exactly music 2,500/50,000 and video 6,667/16,667; any work-conserving policy bounds each one's wait by the other's burst; MLFQ replay 0 misses | HOLDS | NH |
| 23–24 | "c1-meeting by the same arithmetic (voice 2.5 ms against video's 10 ms, video 6.67 ms against voice's 47.5 ms; the helper is near-idle)" | helper RUN 508 µs every 1,640,483 µs; worst video wait 3,008 µs; replay 0 misses | HOLDS | NH |
| 25 | "c3-evening's media segment likewise" | 300–420 s holds only music and video (all other tasks depart ≤ 300 s) | HOLDS | NH |
| 25–30 | "c7-meeting and c7-media — since the 2026-09-11 boot default … the boot MLFQ no longer demotes the 6.67 ms video burst and one 10 ms residual slice equals video's tolerance exactly, so on the arithmetic no headroom against fixed and none between their two EDF rows" | no demotion ✓; 10,000 ✓; between rows ✓ (assumption 1); against fixed ✗ — 600/3,600 video misses under fixed (H1) | WRONG ("against fixed") | NH |
| 30–31 | "c3-creation's batch progress — HandBrake runs uncontended after 240 s, so the cap never bites" | last kdenlive wake 237.94 s, its burst ends 238.02 s; no wakes after; HandBrake 320 s in 180 s → progress = lane time under any work-conserving policy | HOLDS | NH |
| 20–31 (omission) | block presented as the expected no-headroom list | c1-backup `bulk` turnaround always censored (H2) | WRONG (incomplete) | NH, W |
| 58–64 | "batch-beside-editor modes the editor's P99 plus the job's turnaround at the mode's weight" | turnaround unattainable for c1-backup; at risk for c1-ml-train, c1-transcode (D2) | WRONG (c1-backup); UNCHECKABLE (ml-train, transcode) | W |
| 102–103 | "Latency and frame terms over the second segment, 60 s to T_end; progress terms unwindowed (the batch task arrives at 60 s)" | all six C2 files: segment boundary 60 s; background task arrives at 60 s; T_end 180/120/120 s | HOLDS | WIN |
| 112–114 | "The download runs ~1 ms then waits ~5.7 ms per chunk, so it never enters the executor's batch class and no row's cap acts on it; its progress is the algorithm's residual share alone and is expected 'no headroom'" | RUN med 993 ✓; wait med 16,712 ✗; max chunk 6,944 < 10,000 → never batch at 10 ms ✓; no-headroom depends on EDF residual RR vs MLFQ | STALE (number); UNCHECKABLE (no headroom) | CAP, NH |
| 116, 120 | c2-p2a/b frame term entity `game.chain.1`, window 60,000,000–120,000,000 | head of the chain in both files; T_end 120 s | HOLDS | WIN |
| 196–199 | "The injected scan and the renamed or flipped batch job carry no term, so the false row's floor cap is free to act" | clamscan (interactive C7) cpu-batch ✓; for c7-backup the flipped job is borg, outside the batch class at 10 ms (T2), so the floor cap has almost nothing to act on | HOLDS except c7-backup: WRONG | CAP |

### 3.3 `harness/guards/guard-spec.yaml`

| Loc | Statement (verbatim) | Recomputed | Verdict | Decision |
|---|---|---|---|---|
| 47–56 | "One second of virtual time is an order of magnitude above `T_interaction` …, so no interactive term's own latency can trip it, and any wait that long in a segment of tens of seconds is a broken net" | segments are 30–240 s ✓; whether a legal config produces a > 1 s ready wait depends on the executor's starvation window (memo 2026-09-11 §5 Q3) | UNCHECKABLE | G |
| 65–68 | "strictly above 0 where the scoring spec carries terms" | every scored file has nonzero demand | HOLDS | G |
| 70–75, 159–168 | "tick_count — structural. The primitives' own consistency checks (metrics doc §6.2 guard: a chain tail's iteration count equals its head's tick count; … the stimulus count against the run file's wake events …) … Any message is a fail." | chain part fires by construction on c2-p2a/b, near-certainly on c7-gaming (G1); stimulus part plausible under contention (UNCHECKABLE: simulator guide §9.1, §9.4) | WRONG (chain part, as applied to the compiled gaming files); UNCHECKABLE (stimulus part) | G |
| 88–92, 197–199 | "where their events are identical apart from the label (P1: a rename plus the label …) their traces must be identical; P2 and P3 change the background task itself, so no identity is expected" | P1 events identical apart from `hog`'s name, and traces carry task ids, not names (data-contracts §9 `task_arrive`); P2/P3 differ in one arrive event | HOLDS | G |

### 3.4 `daemon/driver-table/prior.yaml`

| Loc | Statement (verbatim) | Recomputed | Verdict | Decision |
|---|---|---|---|---|
| 12–14 | "MLFQ for the interactive-only modes, idle, and unwanted batch work: interactive first, CPU-bound work sunk by observed behaviour" | the editors are CPU-bound by that observation on 90–96% of bursts (T1) | WRONG (as applied) | ROW |
| 17–21 | "since Phase 7's C1 bases every wanted batch row has a term" | terms exist; c1-backup's can never be uncensored | HOLDS (literal) | W |
| 35 | "any CPU-bound work that appears anyway (c6-spoof's miner named chrome) is held to half the lane" | spoof = cpu-batch 30 s at 20 s, batch-class after 10 ms | HOLDS | CAP |
| 41 | "MLFQ serves the interactive job first and sinks CPU-bound work by observed behaviour" | c1-browsing browser: 93.0% of bursts ≥ 10 ms, 91.7% of CPU past first 10 ms | WRONG (premise, T1) | ROW |
| 47 | "(c7-browsing's clamscan): … so the page never waits on the indexer" | clamscan present, cpu-batch ✓; outcome depends on the cap accounting window (batch-class memo §7 item 3) | UNCHECKABLE | CAP |
| 53 | "Unwanted CPU-bound work is what MLFQ's demotion rule sinks …; the cap bounds what the bottom queue can still take" | clamscan demoted after 30 ms of CPU ✓; the browser sinks too | HOLDS (intruder); UNCHECKABLE (browser outcome) | ROW |
| 61 | "the writer's keystroke echo (c1-office's writer P99) leads" | term exists | HOLDS | W |
| 67 | "A keystroke-driven task blocks before its slice ends and stays on top under MLFQ (OSTEP ch. 8, rule 4b)" | writer ≥ 10 ms on 95.3% of bursts; 84/234 keystrokes arrive mid-burst alone | WRONG (T1) | ROW |
| 73 | "(c7-office's clamscan) … (c4-office's 7z burst is the shape of it)" | clamscan ✓; 7z IO-shaped, 2.6% of chunks reach 10 ms | STALE | ROW |
| 79 | "MLFQ demotes the CPU-bound intruder within a few slices and the floor cap keeps it there" | clamscan to Q2 after 10 + 20 ms ✓ | HOLDS | ROW |
| 87 | "the mailer's keystrokes lead (c3-workday's mailer P99)" | term exists (also c1-mail) | HOLDS | W |
| 93 | "the mail client's short bursts stay in the top queue" | c1-mail mailer median 84.3 ms, 96.2% ≥ 10 ms; c3-workday mailer 91.8% | WRONG (T1) | ROW |
| 99, 105 | "(c7-mail's clamscan) …"; "MLFQ sinks the CPU-bound job by demotion" | ✓ | HOLDS | ROW |
| 113 | "(c2-p1's first minute): the editor's keystroke echo leads" | 0–60 s editor alone | HOLDS | W |
| 119 | "The editor blocks on every keystroke and stays on top under MLFQ (OSTEP ch. 8, rule 4b)" | c1-dev 95.8% ≥ 10 ms; 99/237 keystrokes mid-burst alone; c2-p1a 254/774 | WRONG (T1) | ROW |
| 125, 131 | "(c7-dev's clamscan)"; "MLFQ demotes the intruder within a few slices" | ✓ | HOLDS | ROW |
| 139 | "(c3-creation's photo-editor P99)" | ✓ | HOLDS | W |
| 145 | "An editor whose bursts outlast a slice is demoted and boosted back every 100 ms … which keeps it responsive against CPU-bound work" | gimp 95.6% ≥ 10 ms ✓; responsiveness depends on executor | HOLDS (bursts); UNCHECKABLE (outcome) | ROW |
| 151, 157 | "(c7-photo's clamscan)"; "MLFQ sinks the CPU-bound job" | ✓ | HOLDS | ROW |
| 165 | "A live video call is a periodic producer and consumer of audio and video frames, each due at its next period" | c1-meeting voice TIMER 50,000, video TIMER 16,667 | HOLDS | ROW |
| 177, 183 | "(c7-meeting's clamscan): frames keep their deadlines and the job gets the floor so it never steals one" | EDF preemption of a residual slice unwritten (memo 2026-09-11 §5 Q1–Q2) | UNCHECKABLE | ROW |
| 191 | "Game frames are periodic deadlines (the chain's 16.7 ms period, scored as game.chain.1's miss rate) and a download … weighed 0.5 against the frames' 1.0 in c2-p2a, so the batch class gets a third" | period 16,667 ✓; weights ✓; c2-p2a has no batch-class task | STALE | CAP |
| 197 | "c1-gaming and c3-evening run above utilisation 1, outside that theorem" | c1-gaming 1.46 (periodic alone 1.30); c3-evening chain alone 1.45 lanes in its segment | HOLDS | ROW |
| 203 | "(c2-p2b's and c7-gaming's clamscan): … the only scored term being the chain's miss rate" | c7-gaming also scores compositor 0.5 | STALE | CAP |
| 209 | "the floor cap bounds the CPU-bound scan" | clamscan cpu-batch in both | HOLDS | CAP |
| 217, 223 | "two periodic consumers (60 Hz and 20 Hz ticks …)" | 16,667 and 50,000 | HOLDS | ROW |
| 229, 235 | "(c7-media's clamscan): the ticks keep their deadlines"; "keeps both players' ticks" | EDF rule unwritten | UNCHECKABLE | ROW |
| 243 | "(kdenlive's keystrokes in c2-p3's first minute and c3-creation)" | ✓ (no batch in c3-creation 120–240 s) | HOLDS | W |
| 249 | "with long edit bursts demoted and boosted back every 100 ms" | kdenlive 93.7–94.8% ≥ 10 ms | HOLDS | ROW |
| 255, 261 | "(c7-video-edit's clamscan)"; "MLFQ sinks the CPU-bound job" | ✓ | HOLDS | ROW |
| 269 | "c1-compile weighs the makespan 1.0 against the editor's 1.0, so the build's share is half — the compiler children progress at a stated rate and the editor keeps the other half" | weights ✓; build finishes (≈ 4.3 s serial wall, +25.7 s slack); 91.8% of editor CPU batch-class; 37/100 children never batch-class | UNCHECKABLE (share split) | CAP |
| 281 | "(c7-compile's dkms module rebuild …)" | build renamed `dkms`, children `cc1` | HOLDS | ROW |
| 287 | "MLFQ demotes each CPU-bound compiler child within a few slices (OSTEP ch. 8, rule 4a) and the floor cap bounds the whole class" | 63/100 children demoted at least once; 72% of child CPU past first 10 ms | STALE | ROW |
| 295 | "c2-p1a weighs its progress 0.5 against the editor's 1.0, so the batch class gets a third and the editor's keystrokes the rest" | weights ✓; editor 91.4% batch-class CPU | UNCHECKABLE | CAP |
| 307 | "(c7-ml-train, the same run flipped by intent — a pre-committed miss)" | ✓ | HOLDS | ROW |
| 313 | "One CPU-bound job under an interactive editor is MLFQ's textbook case" | editor CPU-bound by MLFQ's evidence (96.1% ≥ 10 ms) | WRONG (T1) | ROW |
| 321 | "(c2-p3a's ffmpeg): progress weighs 0.5 against the editor's 1.0, so the render's share is a third" | weights ✓; ffmpeg cpu-batch ✓ | HOLDS (facts); UNCHECKABLE (share split) | CAP |
| 333, 339 | render/false "(c7-render …)"; "MLFQ sinks the CPU-bound render" | ✓ | HOLDS | ROW |
| 347 | "(c3-creation's HandBrake) … after the user walks away no foreground is runnable and the cap no longer bites" | no kdenlive wakes after 237.94 s | HOLDS | CAP |
| 359, 365 | transcode/false | ✓ | HOLDS | ROW |
| 373 | "(c1-indexing: the reindex's turnaround weighed 1.0 against the editor's 1.0): equal shares" | weights ✓; finish feasible (+0.70 s) | HOLDS | CAP |
| 385 | "(c2-p1b's and c7-indexing's tracker-miner under an editor) … the only scored term is the editor's keystroke echo" | ✓ | HOLDS | W |
| 391 | "One CPU-bound intruder under an interactive editor is MLFQ's textbook case" | editor 93.0% (c2-p1b) / 90.3% (c7-indexing) ≥ 10 ms | WRONG (T1) | ROW |
| 399 | "(c2-p3b's borg): progress weighs 0.25 …, so its share is a fifth — wanted, never starved, below a user-initiated render" | borg 1.7% batch-class CPU; share governs editor tails (T2) | WRONG | CAP |
| 405 | "Proportional share by tickets … states a small guaranteed rate exactly" | as above | WRONG | CAP |
| 411 | "(c7-backup …): sink it and hold it to the floor" | borg stays in Q0 on 98% of chunks; cap cannot reach it | WRONG | ROW, CAP |
| 417 | "MLFQ sinks the CPU-bound job by demotion" | borg not CPU-bound (duty 0.23) | WRONG | ROW |
| 425 | "(c1-idle's five daemons)" | pipewire, dbus-daemon, systemd, gnome-shell, Xorg | HOLDS | ROW |
| 437, 443 | "(c7-idle's clamscan)"; "MLFQ sinks the CPU-bound job" | ✓ | HOLDS | ROW |
| 275, 301, 327, 353, 379, 405 | "2 ms quantum per the boot value" | params say 10000 (not a workload statement) | STALE (text) | — |

### 3.5 `docs/daemon/prior-table-pair-review.md`

| Loc | Statement (verbatim) | Recomputed | Verdict | Decision |
|---|---|---|---|---|
| 15 | browsing: "no coreset file exercises the `false` row, and in `c6-spoof` the oracle reads `browsing/true`, so the 0.5 cap is the one that holds the miner" | c7-browsing exercises false since Phase 7 (§C supersedes); c6-spoof label and cpu-batch miner ✓ | STALE (first part); HOLDS | CAP |
| 16–19 | office/mail/dev/photo: "no (coreset) file exercises the `false` row"; "`c4-office`'s 7z burst runs under `office/true`"; "`c2-p1`'s first minute, where no batch exists yet" | false rows exercised by C7; c4-office label office/true ✓; hog arrives 60 s ✓ | STALE (false rows); HOLDS | CAP |
| 20 | meeting: "no scored term: … the frames the EDF family serves have no coreset instance" | c1-meeting, c7-meeting since Phase 7 | STALE | CAP |
| 21 | gaming: "in `c2-p2a` the download blocks every millisecond, is not batch-class, and the 0.333 cap is inert" | RUN med 993 µs then SLEEP; no chunk reaches 10 ms (at the 2 ms slice in force on 09-09, 8.5% did) | HOLDS (current table) | CAP |
| 22 | media: "which no legal configuration can move (the scoring spec's stated 'no headroom')" | ✓ | HOLDS | NH |
| 23–27 | video-edit/compile/ml-train/render/transcode rows (files and terms; transcode "expected 'no headroom' because the batch runs uncontended after 240 s") | ✓ | HOLDS | W, NH |
| 28 | indexing: "`editor` P99 1.0 in `c2-p1b`, whose only term it is; … the `true` row has no coreset instance" | ✓; c1-indexing since Phase 7 | HOLDS; STALE (true row) | CAP |
| 29–30 | backup terms; idle "nothing else exercises either row" | ✓; c7-idle since Phase 7 | HOLDS; STALE | — |
| 36 | p1: "the hog is CPU-bound in both files, so both knobs act: in p1a the 0.333 share carries `hog` progress (weight 0.5) while the editor keeps two thirds" | hog cpu-batch 130 s ✓; editor 91.4% batch-class CPU | HOLDS (knobs act); UNCHECKABLE (two thirds) | CAP |
| 37 | p2: "the download is not batch-class (it blocks every ~1 ms), so the cap does not act on it" | ✓ at 10 ms | HOLDS | CAP |
| 38 | p3: "the ffmpeg render is CPU-bound and the borg backup's 3 ms bursts outrun a 2 ms slice, so both are batch-class and both shares act" | ffmpeg ✓; borg 2.1% of chunks reach 10 ms (T2) | WRONG | CAP, JS |
| 42 | "The ten interactive counterparts inject `clamscan` on `cpu-batch` for the whole segment; `compile` renames `make` to `dkms`; the other five flip the label alone" | ✓ (c7-indexing flips too) | HOLDS | — |
| 46–50, 54 | counterpart demand: browsing 1.45 (inside), office 1.50 (above), mail 1.53 (above), dev 1.46, photo 1.47, video-edit 1.46 | 1.4486, 1.5008, 1.5270, 1.4634, 1.4677, 1.4589; "the send burst is network-bulk and carries no term" ✓ | HOLDS | DW |
| 51 | meeting: "a single 2 ms slice of delay is below both tick tolerances … so the row difference is measurable only under a lottery draw" | slice now 10 ms = video tolerance (addendum) | STALE | NH |
| 52 | gaming: "the chain's woken stages sit in the residual class beside the scan, as in `c2-p2b`"; 2.46 (above) | 2.4557 ✓; class of stages 2–16: vocabulary §2 vs batch-class memo B2 conflict | HOLDS (number); UNCHECKABLE | CAP |
| 53 | media 1.45 (inside) | 1.4500 | HOLDS | DW |
| 55 | compile: "the `dkms` rebuild and its cc1 children are the batch class the floor holds"; 0.54 (below) | 0.5391 ✓; 37/100 children never batch-class | STALE | CAP |
| 56–59 | ml-train 0.97, render 0.90, transcode 0.97, indexing 0.95 (below) | 0.9723, 0.9021, 0.9705, 0.9550 | HOLDS | DW |
| 60 | backup: "borg's 3 ms bursts outrun a 2 ms slice, so it is batch-class and both knobs act"; 0.97 (below) | 0.9742 static (0.697 deliverable); borg 1.9% of chunks reach 10 ms | WRONG | CAP, JS |
| 61 | idle: "the scan alone puts the file at one lane"; 1.00 (inside) | 1.0004 | HOLDS | DW |
| 63 | "the interactive counterparts sit at or just above the regime's ceiling because a full lane of scan is added to a half-lane base, `c7-gaming` at two and a half lanes because its base already fills the lane through `lane_share`, `c7-idle` at exactly one lane, and the batch counterparts equal their bases" | ✓ | HOLDS | DW |
| 67 | finding 1: "`c2-p2a`'s download (`network-bulk`, ~1 ms of RUN per ~5.7 ms) never consumes a 2 ms slice … the conclusion holds under any rule, since a 1 ms chunk is shorter than every legal slice" | 16.7 ms; 1,882 chunks ≥ 2 ms; legal minimum 500 µs (91.6% of chunks exceed); holds at 10 ms | STALE (decision holds for the pinned table) | CAP, JS |
| 67 | "the pair's gate distance rests on p2b's CPU-bound scan, where the floor cap acts" | ✓; but c2-p2a remains judging with tied rows (J1) | HOLDS (fact); see J1 | JS |
| 68 | finding 2 counts (17 cells, "about 95 percent") | pre-Phase-7 build; superseded by finding 4 | not re-checked (historical) | — |
| 70 | finding 4: "Of the 63 segments on the grid, 18 are `false`, so an always-`true` answer still scores about 71 percent by segment count"; "Five segments are pre-committed misses" | 18/63 → 71.4% ✓; 5 ✓; per query point 69.5% | HOLDS | — |
| 71 | finding 5: "one slice of delay is below both tick tolerances"; "the boot default demotes a 6.67 ms video burst after its 2 ms slice"; "`gaming` is not in this family because the chain's woken stages are residual-class" | superseded by the 10 ms slice (addendum); stage class unwritten | STALE; UNCHECKABLE | NH |
| 72 | addendum (1): "one residual slice is now 10 ms, exactly the video consumer's tick tolerance (period 16 667 µs minus burst 6 667 µs) … the worst-case tick starts 10 000 µs late and finishes exactly at its deadline" | ✓ | HOLDS (UNCHECKABLE outcome: memo 2026-09-11 §5 Q1–Q2) | NH |
| 72 | addendum (2): "with a 10 ms slice the burst never consumes a slice and is never demoted, and the one exposure under `fixed` is the 100 ms boost lifting the scan to Q0 with a fresh slice, the same 10 ms worst case. On the arithmetic both files are expected no headroom on every scored term" | never demoted ✓; exposure is 10 ms + the coincident music/voice tick (2.5 ms) → 600/3,600 misses (H1) | WRONG | NH, JS |

### 3.6 `docs/memos/2026-09-09-batch-class-rule-for-the-simulator.md`

| Loc | Statement (verbatim) | Recomputed | Verdict | Decision |
|---|---|---|---|---|
| 24 | "`clamscan` | runs 25 s of CPU without ever stopping" | c2-p2b `download` = clamscan RUN 25,000,000 | HOLDS | — |
| 25 | "`game.chain.1 … 16` … each running 0.2–2.2 ms then handing over; the head is a TIMER at 16.7 ms | the long stages **become batch**" | 230–2,176 µs ✓; at 2 ms two stages exceed; at 10 ms none, but backlogged stages whose WAIT does not block would accumulate past 10 ms, so B2 is still needed | STALE | (rule motivation) |
| 26 | "`compositor` in `c1-gaming` (`gamescope`) | 6.7 ms of work every 16.7 ms tick | **batch**" | ✓; batch only under a 2 ms obvious rule | STALE | — |
| 49 | "The boot slice is 2 ms throughout." | 10 ms since 2026-09-11 | STALE | — |
| 51 | hog: "Two ms after its first dispatch it enters the batch class and never leaves" | 10 ms; never blocks ✓ | STALE | CAP |
| 53 | "Its program is 'run about 1 ms, sleep about 5.7 ms' 22 000 times … It never reaches a full slice before it blocks, so under B1 it never enters the batch class. **The cap does not apply to it, in any row.**" | 22,072 ✓, RUN 993 ✓, SLEEP 16,712 ✗; at 2 ms 8.5% of chunks reach the slice (claim false when written); at 10 ms none | STALE | CAP |
| 55 | "A backup (`c2-p3b`'s `borg`). 'Run 3 ms, sleep 2 ms', repeated. Two ms into each burst it enters the class; 1 ms later it blocks and leaves. So it is batch for the last third of every burst — the cap bites, partially. Under `backup / wanted: true` (cap 0.2, LOTTERY share 0.2) that is what the row intends." | SLEEP median 10,022 µs; at 10 ms 2.1% of chunks / 1.7% of CPU batch-class | WRONG (T2) | CAP |
| 57 | "In `c2-p2b` the 0.05 cap therefore lands on `clamscan` alone." | tails ≤ 699 µs, steam, wineserver never reach 10 ms; chain B2 | HOLDS | CAP |
| 59 | "the editors' keystroke bursts are long — a median of 80–90 ms of CPU per keystroke, then hundreds of ms waiting for the next key. So under B1 an editor is non-batch at the instant a keystroke wakes it, becomes batch 2 ms into the burst" | medians 73.7–95.5 ms ✓; 31–42% of keystrokes arrive before the burst ends (no wait, no block); "2 ms" → 10 ms | STALE (numbers) | CAP |
| 61 | "When the keystroke arrives, the editor is non-batch and runnable, so the cap bites on the hog and the editor gets the CPU quickly. The number the harness scores for editors is exactly this wait" | false for the 31–42% of keystrokes that find the editor still running (it never blocked, stays batch); those rows are recorded as 0 by metrics doc §6.1 (a `ready` inside the task's own occupancy has wait 0) | UNCHECKABLE (simulator guide §9.1: whether such a wake is remembered) | CAP, W |
| 68 | "The conclusion holds under any classification rule, since a 1 ms chunk is shorter than every legal slice" | legal slices start at 500 µs; median chunk 993 µs, max 6,944 µs | STALE (decision holds at 10 ms) | CAP |
| 85 | unit test (a) "a task running 1 ms then sleeping 5.7 ms in a loop is never batch-class" | synthetic; compiled download sleeps 16.7 ms | STALE (text only) | — |

### 3.7 `docs/memos/2026-09-11-boot-default-from-ostep.md`

| Loc | Statement (verbatim) | Recomputed | Verdict | Decision |
|---|---|---|---|---|
| 63 | "`video`(16.67 ms마다 깨어나 6.67 ms 일함, TIMER라서 deadline class), `music`(50 ms마다 2.5 ms, 역시 deadline class), `scan`(clamscan, 60초 내내 CPU만 쓰는 batch, TIMER가 없으니 residual class)" | c7-media exactly these three | HOLDS | — |
| 66, 72–75 | illustrative instants (scan slice at t = 100000; video TIMER "정확히 t = 100000") | video ticks are at 16,667k (100,002 µs, not 100,000); the compiled coincidence at 100,000 µs is music's tick with the MLFQ boost | illustrative, not a compiled claim | — |
| 83 | "둘 다 이렇게 정해지면 `c7-media`·`c7-meeting`의 답은 확정이에요: 어느 config에서도 `fixed`에서도 miss가 없고, 두 파일은 headroom 없음" | fixed: 600/3,600 video misses (H1); MLFQ/LOTTERY rows drawn by `random` additionally depend on the cap accounting window | WRONG (fixed); UNCHECKABLE (other configs) | NH, JS |
| 101 | "video 소비자는 16.67 ms마다 깨어나 6.67 ms 일해요. 그러니까 10 ms까지는 기다려도 마감을 맞추고, 그보다 1 µs라도 더 기다리면 miss" | ✓ | HOLDS | NH |
| 102 | "video가 scan의 slice 시작 직후에 깨어나면 10 ms를 기다리고, 6.67 ms 일하고, 마감에 정확히 맞아요" | ✓ under EDF option B | HOLDS (UNCHECKABLE outcome) | NH |
| 103 | "`fixed`(MLFQ)에서는 전에 2 ms slice가 video의 6.67 ms burst를 강등시켜서 … 10 ms slice에서는 video가 강등되지 않아요. 그래서 이 이유도 사라져요" | not demoted ✓; a different fixed-side miss mechanism remains (H1) | WRONG (conclusion) | NH |
| 105 | "deadline task가 바로 뺏거나, 경계에서 '맞춤'으로 처리하면 → cap이 얼마든, 어느 조건에서도 miss가 없고, 두 파일은 `c1-media`·`c1-meeting`처럼 'headroom 없음'이 돼요" | `fixed` misses (H1); c1-media/c1-meeting indeed 0 | WRONG | NH, JS |

### 3.8 `docs/memos/2026-09-12-rq0-pre-registration.md`

| Loc | Statement (verbatim) | Recomputed | Verdict | Decision |
|---|---|---|---|---|
| 12 | "`c7-meeting`·`c7-media`는 §4의 가정 아래에서는 두 row가 모든 term에서 비기고 `fixed`와도 비겨서" | rows tie ✓; fixed ✗ (H1) | WRONG (fixed part); classification holds | JS, NH |
| 12 | "판정 set 25개. C2 pair 여섯, batch C1 base 여섯, term이 있는 C7 counterpart 열셋" | count ✓; J1, J2 | WRONG (membership by the stated rule: c2-p2a, c1-backup) | JS |
| 16 | "gaming pair의 frame 여유 831 µs, chain stage 최대 1 470/2 176 µs, compositor burst 6 667 µs, boost 뒤 1 ms 지점" | numbers ✓; 831 µs is not idle time (S1) | WRONG (831 as a threshold); HOLDS (others) | SW |
| 18 | "32 row지만 config는 8종류뿐이고 … 그중 13 row가 같은 config(MLFQ, cap 0.05)예요. 그래서 판정 파일 25개 중 13개에서는 random이 41% 확률로 oracle과 똑같은 config를 뽑아요" | ✓ | HOLDS | JS |

### 3.9 `docs/memos/2026-09-10-coreset-before-and-after-phase-7.md`

| Loc | Statement (verbatim) | Recomputed | Verdict | Decision |
|---|---|---|---|---|
| 8, 24–27 | pre-Phase-7 counts (17 cells, 2 false segments, 95%) | previous build; not in the current build | not re-checked (historical) | — |
| 75–84 | new C1 utilizations: dev 0.46, video-edit 0.46, photo 0.47, mail 0.53, meeting 0.45, ml-train 0.97, render 0.90, transcode 0.97, indexing 0.96, backup 0.97 | 0.4634, 0.4589, 0.4677, 0.5270, 0.4503, 0.9723, 0.9021, 0.9705, 0.9550, 0.9742 | HOLDS | DW |
| 86 | "base는 job의 turnaround를 채점하니까 60 s 안에 끝나야 해요. 어떤 policy든 lane의 절반이면 끝나요." | half a lane from 2 s = 29 s < 30 s; borg cannot finish alone (132.2 s) | WRONG (D2) | W |
| 103–108 | C7 utilizations: 1.45–1.47, office 1.50, mail 1.53, gaming 2.46 "(base가 이미 1.46)", idle 1.00, batch equal to base | ✓ | HOLDS | DW |
| 124 | "tick이 기다리는 최대는 residual slice 하나, 2 ms … cap이 0.5든 0.05든 tick은 한 번도 안 늦어요" | slice now 10 ms (knife edge) | STALE (superseded by memo 2026-09-11) | NH |
| 128 | "`fixed`는 MLFQ boot default라 6.67 ms짜리 video burst를 2 ms slice 뒤에 강등시키고 scan과 경쟁시켜서 tick이 늦어요 … 이 gap은 진짜지만 algorithm 선택(EDF vs MLFQ)에서 오지" | mechanism gone at 10 ms; a fixed-side gap still exists through the boost + coincident music/voice tick | STALE (conclusion "EDF-vs-MLFQ headroom exists" holds) | NH |
| 131 | "gaming(chain의 woken stage가 residual class라 scan과 경쟁)" | stage class unwritten (vocabulary §2 vs batch-class memo B2) | UNCHECKABLE | CAP |
| 137 | "interactive counterpart 10개의 `clamscan`은 cpu-batch라 그 rule로 batch class에 들어가야 cap이 작동해요. `c7-backup`의 `borg`(io-stream, 3 ms burst)도 '한 slice를 꽉 채우면 batch'라는 rule로 batch class예요" | clamscan ✓; borg 1.9% of chunks reach 10 ms | HOLDS; WRONG (borg) | CAP |
| 138 | "residual slice는 `residual_timeslice_us`(2 ms). 이게 맞다면 `c7-meeting`·`c7-media`에서 어떤 cap에서도 miss가 0이어야 해요" | 10 ms now | STALE | NH |
| 144 | "grid 위 63 segment 중 18개가 `false` … 약 71%" | ✓ | HOLDS | — |
| 148 | judging set "27개: C2 6 + batch C1 base 6 + term 있는 C7 15"; "`c7-gaming`·`c7-meeting`·`c7-media`는 note가 붙은 채로 judging" | superseded by the RQ0 gate spec (25) | STALE | JS |
| 157–166 | summary table (segments 63+1, 32/32 cells, 18 false, ≈71%, 5 misses, 23/27 timelines, 100 artifacts) | ✓ | HOLDS | — |

### 3.10 `_dev/docs/rq0-preparation-notes.md`

| Loc | Statement (verbatim) | Recomputed | Verdict | Decision |
|---|---|---|---|---|
| 47–49 | "13 novel + 11 derived timelines, all inside the demand window" | 23 + 27 now; "inside" only by the static estimate (D1) | STALE | DW |
| 115–117 | "`c1-gaming` in particular carries a `lane_share: 0.9` game task chain plus a 40%-duty compositor" | ✓ | HOLDS | — |
| 123–125 | "five C1 files sit at 0.00–0.54 of the lane, `c1-gaming` at 1.46. Judging set = the six C2 files, all inside the demand window" | original six ✓; C2 1.12–1.29 static ✓ (superseded) | HOLDS (historical) | JS |
| 127–130 | "the ten new bases sit at 0.45–0.97 … C7 adds one counterpart per mode (interactive ones at 1.45–1.53, `c7-gaming` 2.46, batch ones equal to their bases)" | ✓ (c7-idle 1.00 sits outside the 1.45–1.53 range if counted as interactive) | HOLDS | DW |
| 150–151 | "C2 is three pairs, each a one-task diff between otherwise byte-identical files" | ✓ | HOLDS | — |
| 180–184 | "C2 pairs differ only in `background_wanted`, so the gap there rests almost entirely on how far apart the two rows' configurations sit — principally `batch_bandwidth_cap`" | P1 mode+attribute, P2 attribute, P3 mode only | STALE (failure-procedure conclusion holds) | (failure procedure) |
| 325–326 | "C2 pairs differ *only* in that attribute" | as above | STALE | — |
| 397–399 | inventory: "`c2-p1a/b` … editor latency + batch task turnaround"; "`c2-p3a/b` … editor latency + bulk turnaround" | neither job can finish in its file (hog 130 s/120 s; ffmpeg 75 s/60 s; borg ≤ 13.5 s of 75 s) — the scoring spec later used progress | STALE (superseded) | W |
| 403–407 | "`c2-p1a` and `c2-p1b` are behaviourally identical … differing only in the name" | ✓ | HOLDS | W |
| 433–434 | "`video-playback` runs 60 Hz at 40% duty, `audio-playback` 20 Hz at 5%" | ✓ | HOLDS | W |
| 442–447 | "C5 … identical to `c1-media` except for process names"; "`c1-idle` — five `system-daemon` tasks, near-idle, no contention" | ✓ (0.0004 lanes) | HOLDS | EX |
| 574–576 | c7-gaming note "Base already needs 1.46 lanes; with the scan, frames miss under every row" | ✓ (misses under every row already in the base) | HOLDS | JS |
| 577–585 | c7-meeting note: "one residual slice (10 ms since the 2026-09-11 boot default) equals video's tick tolerance exactly, and fixed no longer demotes the video burst, so on the arithmetic the rows tie and fixed ties too: expected no headroom on every term" | fixed ✗ (H1) | WRONG (fixed part) | NH |
| 597–603 | c1-gaming reason: "demand 1.46, the highest in the coreset … no pair, so no attribute variation" | as in 3.1 | STALE | JS |
| 625–627 | "`c1-gaming` single situation · demand 1.46 ← highest in the coreset / other C1 · demand < 1.0 / C2 · demand 1.12–1.29" | not highest now; other C1 < 1.0 ✓ (max 0.97); C2 static ✓ (deliverable 0.61–1.29) | STALE | JS |

### 3.11 Phase specs (decisions only)

| Loc | Statement (verbatim) | Recomputed | Verdict | Decision |
|---|---|---|---|---|
| phase-3:38 | "The six C1 values and the resulting judging-set conclusion (6 files or 12) are recorded" | no value stated here | — | — |
| phase-6:18 | "The coreset exercises 17 legal rows (16 in C1–C4)" | previous build; marked superseded | not re-checked | — |
| phase-6:42 | "Wanted batch progress 0.5 (`c2-p1a` hog, `c2-p2a` download, `c2-p3a` ffmpeg) … Scheduled wanted backup 0.25 (`c2-p3b` borg). p2's frame term is the chain (`game.chain.1`); the pair has no compositor." | ✓ (no compositor in c2-p2a/b) | HOLDS | W |
| phase-6:46 | "Every `ready_wait` and `job` term in the six C2 files is aggregated over 60 s to `T_end`. … Progress terms are unwindowed." | ✓ | HOLDS | WIN |
| phase-6:54 | "No legal configuration can produce a missed tick in this file (c1-media)" | ✓ | HOLDS | NH |
| phase-6:58 | "Chain miss rate 1.0, compositor (`gamescope`) miss rate 0.5" | entities exist | HOLDS | W |
| phase-6:66 | "`c3-creation`: … `batch` progress 0.5, expected 'no headroom' since it runs uncontended after 240 s" | ✓ | HOLDS | NH |
| phase-7:20 | "Recounted 2026-09-09 from the compiled ground truth: 17 cells exercised …" | previous build | not re-checked | — |
| phase-7:36 | "`clamscan` bound to `cpu-batch` … arriving at 0 s with `total_work` equal to the 60 s segment" | ✓; never completes before 60 s in any C7 file (other demand > 0; c7-idle's daemons take ~24 ms) | HOLDS | — |
| phase-7:48 | "batch jobs sized to the 60 s segment where the source segment was longer" | 30 s jobs ✓ | HOLDS | — |
| phase-7:52 | "batch-beside-editor modes score the editor's P99 plus the job's term, `turnaround` where the job is sized to finish and `progress` otherwise" | c1-backup got turnaround but cannot finish (D2) | WRONG (application to c1-backup) | W |
| phase-7:72 | "the six batch C1 bases (…, whose wanted LOTTERY share a random row removes) … `c7-gaming` (frames miss under every row, only the gap reads), `c7-meeting` and `c7-media` (the gap is EDF against the drawn algorithm, the cap axis unmeasured)" | c1-backup (J2); c7-gaming ✓; c7-meeting/media superseded | WRONG (c1-backup); HOLDS; STALE | JS |
| phase-7:84 | "the coreset's `false` share is 18 of 63 segments" | ✓ | HOLDS | — |
| phase-8:27, 35, 39 | "one g applies to all 27 files"; "stays in the 27" | 25 after 8.8 (not a workload statement) | STALE (count) | JS |

### 3.12 `docs/workload/coreset-guide.md`

| Loc | Statement (verbatim) | Recomputed | Verdict | Decision |
|---|---|---|---|---|
| 146 | "`c1-office`의 `writer`는 234쌍이고 RUN 중앙값 ≈ 90 ms, 총 29.8 s … fraction 평균이 0.5라서예요" | 234, 89,716 µs, 29.83 s | HOLDS | — |
| 148 | "`c1-office`의 `browser`가 그래요 … CPU는 0" | single WAIT | HOLDS | — |
| 162 | "`c1-compile`의 100개 자식은 총 3.84 s, 중앙값 18.5 ms, 최대 478 ms" | 3.8444 s; per-child median 18,522 µs; max 478,435 µs | HOLDS | — |
| 176 | io-stream "compile되면 `RUN ~3 ms, SLEEP ~10 ms`가 수천 쌍. CPU:wall 비율 약 0.23" | ✓ | HOLDS | — |
| 182 | background-crawler "현재 coreset에서는 안 쓰여요" | ✓ | HOLDS | — |
| 192–193 | chain "각 stage의 RUN은 task마다 고정(260 µs–1.65 ms 범위의 lognormal)"; tail "`SLEEP(~0.5 s) → RUN(~200 µs)`" | anchors are p05/p95 before scaling (single values reach 2,440 µs); tail medians 491–508 ms / 190–201 µs | HOLDS | — |
| 205 | network-bulk "compile되면 `SLEEP ~5.7 ms, RUN ~1 ms`가 수만 쌍. CPU:wall 약 0.06" | SLEEP median 16,712 µs; 0.056 ✓ | STALE | CAP (via pair review) |
| 211 | "`c1-office`의 renderer 8개는 period 0.7 s–2.5 s, RUN 88–749 µs" | periods 0.447–9.684 s; RUN ✓ | STALE (number, no decision) | — |
| 217 | "`c1-gaming`의 `wineserver`: SLEEP 1225 s" never wakes | ✓ | HOLDS | — |
| 270 | "focus 2–58 s → 234개 wake … 첫 wake는 2.216 s" | 2,215,828 µs | HOLDS | — |
| 274 | "`borg`의 75 s → 21,078쌍" | ✓ | HOLDS | — |
| 289 | "`-native`와 `-single`은 게임이 없는 파일에서는 byte-identical" | ✓ (7 game files differ, chain RUNs only) | HOLDS | — |
| 399, 403–423 | "`c1-gaming`은 calibration인데 1.46"; table of the original 24 ("coreset 최고" for c1-gaming among them) | all values ✓ against the manifest | HOLDS (in the table's stated 24-file context) | DW |
| 425 | "`c2-p1a`는 0–60초는 0.48이고 60–180초는 1.56이에요" | ≈0.47 and ≈1.57 (hog counts 130 s in a 120 s window) | HOLDS | DW |
| 443 | "진짜 새로 쓴 timeline은 23개 … 나머지 27개" | ✓ | HOLDS | — |
| 467–470 | c1-office table: writer 234/89.7 ms/29.8 s; "renderers.1–8 … TIMER 0.7–2.5 s"; mail TIMER 2.02 s RUN 71 µs | ✓; renderer periods 0.45–9.68 s | HOLDS; STALE | — |
| 486–487 | c1-browsing: browser 229 / 90.4 ms / 26.6 s; "renderers.1–12 … TIMER 1.1–4.1 s, RUN 86 µs–2.4 ms" | ✓; periods 0.29–4.88 s | HOLDS; STALE | — |
| 503–509 | c1-compile table; "총 일이 3.84 s라 60초 안에 여유 있게 끝나요" | ✓; serial wall ≈ 4.34 s | HOLDS | W |
| 521–526 | c1-gaming table: stage RUN 293 µs–1.47 ms sum 15.0 ms; tails "SLEEP ~0.3–1.2 s, RUN 49 µs–1 ms"; steam 3.28 s/381 µs; webhelpers 0.78/0.83/26.9 s; wine SLEEP 1225 s | ✓; tail SLEEP 0.11–3.0 s | HOLDS (tail range loose) | — |
| 530 | "**utilization 1.46, coreset 최고.** chain 0.9 + compositor 0.4 = 1.3만으로 이미 lane을 넘어요 … judging set에는 안 들어가지만(pair가 없어 attribute 변화가 없음)" | 1.3 ✓; not highest; c7-gaming pairs it | STALE | JS |
| 547 | c1-media "두 tick이 겹칠 때 하나가 최대 6.7 ms 기다림" | ✓ | HOLDS | NH |
| 559–563 | c1-idle SLEEP/RUN values | ✓ | HOLDS | — |
| 573 | "batch job은 60 s 안에 끝나도록 30 s로 줄였어요(turnaround term을 갖기 위해)" | c1-backup cannot finish (D2) | WRONG | W |
| 577–586 | ten-new-C1 table utilizations | ✓ | HOLDS | DW |
| 607–612 | c2-p1a: 774 wakes, 80.4 ms, 86.7 s; "hog는 절대 못 끝나요 … utilization 1.20 (60초 이후는 1.56)" | ✓ | HOLDS | W |
| 625 | "trace와 records가 p1a와 같아요(같은 condition이면)" | events identical apart from name; traces carry ids | HOLDS | G |
| 638–642 | c2-p2a: stage RUN 230 µs–2.18 ms; wine SLEEP 2.1 s RUN 212 µs; download "SLEEP ~5.7 ms / RUN ~1 ms × 22,072. RUN 총 25.0 s" | ✓; SLEEP 16.7 ms | HOLDS; STALE | — |
| 646 | "download는 25 s의 CPU를 60초 안에 받아야 하는데 chain이 lane의 95%를 요구하니 **못 끝나요**(lane의 42%가 필요) … compositor(`gamescope`)는 이 파일에 없어요. TIMER를 가진 task는 `game.chain.1`과 `steam`뿐" | cannot finish even alone (503.3 s); TIMER tasks ✓ | STALE (reason); HOLDS | W |
| 663 | "download는 network-bulk(CPU 6%짜리 chunk 수만 개)" | 5.6% | HOLDS | — |
| 681 | c2-p3a "75 s를 60초 안에 → 못 끝남. utilization 1.12" | ✓ (deliverable 0.997) | HOLDS | W |
| 685 | "여기서는 `background_wanted`가 둘 다 true예요 … mode(`render` vs `backup`)" | ✓ | HOLDS | JS |
| 694 | borg "RUN ~3 ms / SLEEP ~2 ms × 21,078" | SLEEP median 10,022 µs | STALE | — |
| 719–725 | c3-workday: 242/27.5 s; "renderers.1–8 TIMER 0.6–10 s"; writer 244/27.8 s; dispatch 1.1 s; children "총 349 s, 중앙값 20 ms, 최대 5.6 s"; mailer 220/27.7 s; send 3.0 s | ✓; renderer periods 0.16–13.07 s | HOLDS; STALE | — |
| 729 | "빌드는 window 안에 절대 못 끝나요. 자식 349 s의 일이 120초에 시작하고 window는 300초 남았는데" | ✓ | HOLDS | W |
| 745–755 | c3-evening chain sum 24.2 ms "혼자서도 못 따라감"; overlay 0.31 s/558 µs; wine SLEEP 457 s "안 깸"; "게임 segment 안은 1.45 이상" | ✓ | HOLDS | — |
| 769–775 | c3-creation 488/58.2 s, 510/56.6 s; "240초 이후 kdenlive는 focus가 없어요 … contention이 없어요. 320 s 일을 180초에 → 못 끝남" | ✓ | HOLDS | NH |
| 789, 793 | c4-gaming discord TIMER 1.71 s RUN 590 µs; utilization 1.46 | ✓ | HOLDS | — |
| 801 | c4-office 7z "RUN ~3 ms / SLEEP ~11 ms × 1651. RUN 총 6.0 s" | median 9.8 / mean 11.7 ms | HOLDS | — |
| 814, 818 | c4-compile injected renderers "TIMER 0.8–7 s"; 0.54 | 0.77–7.09 s | HOLDS | — |
| 898–906 | c6-dual: lane_share 0.6, stage RUN 182 µs–1.09 ms; editor 976/117.7 s; build spawn 85, 10.6 s; 1.28 | ✓ | HOLDS | — |
| 920–939 | C7 table and demand paragraph | ✓ | HOLDS | DW |
| 941 | "계산상으로는 어느 row에서도, 그리고 `fixed`에서도(10 ms slice는 video의 6.67 ms burst를 강등시키지 않아요) tick을 놓치지 않아 headroom이 없지만" | fixed ✗ (H1) | WRONG | NH |
| 979–982 | "`c3-creation`의 240초 이후 `kdenlive`" idle; wineserver 1225 s / 457 s; "C2의 batch task 셋과 C3의 batch/build 셋은 전부 window 안에 못 끝나요 … `c2-p2a` download 25 s이지만 chain이 95% 요구 … 그래서 judging set에서 `turnaround`는 관측 불가"; c3-evening backlog | none finish ✓ (download reason ✗); batch C1 bases now judge with turnaround | HOLDS; STALE (reason, judging-set scope) | W |
| 983–984 | "'행동 동일'은 p1에만 엄격히 성립"; "`c2-p3` pair는 둘 다 `background_wanted: true`" | ✓ | HOLDS | — |
| 986 | "게임 파일에서 TIMER를 가진 task는 … `gamescope`(c1/c4-gaming만)" | also c7-gaming | STALE | — |
| 1046 | "**judging set** | RQ0 gate 판정에 쓰는 파일. C2의 6개" | 25 files | STALE | JS |

### 3.13 `docs/workload/building-plan.md` §3 and §5a

| Loc | Statement (verbatim) | Recomputed | Verdict | Decision |
|---|---|---|---|---|
| 85 | "Task sets are lifted from the segment that already carried the mode …; batch jobs are sized to finish inside the segment so the base carries a turnaround term." | c1-backup cannot finish; c1-ml-train, c1-transcode infeasible unless editor work is dropped (D2) | WRONG | W |
| 86 | "In the RQ0 gate the six batch bases judge, two-sided with their C7 counterparts (a wanted LOTTERY share is what a random row removes); the ten interactive and periodic bases are reporting-only (nothing runs behind the foreground)." | J2 for c1-backup; no batch-class background task in the ten at 10 ms ✓ | WRONG (c1-backup); HOLDS | JS |
| 87 | "`c1-gaming` lands inside the oversubscription regime through its `lane_share` binding while the other five sit well below one lane" | 1.46 ✓; fifteen others, three at 0.97 | STALE | DW |
| 91–94 | P1 "behaviorally identical CPU saturation beside an editor"; P2 "same game-plus-background shape; wanted flips"; P3 "user-initiated bulk vs scheduled bulk"; "each pair is a one-segment diff between two otherwise byte-identical files" | ✓ (one arrive event + one segment label differ) | HOLDS | — |
| 104 | C4 "label-invariant process injected mid-segment" | injected at 30 s in all three | HOLDS | — |
| 113 | "all tiers bind identical archetypes" | ✓ | HOLDS | — |
| 121 | C7 "arriving at 0 s with `total_work` equal to the segment so the label holds at every instant"; "where the attribute has no scheduling consequence (the purely periodic modes under EDF) the pair review says so" | clamscan never completes before 60 s ✓; EDF rule unwritten | HOLDS; UNCHECKABLE | — |
| 124 | "50 files, 64 segments … novel … 23 …; the other 27" | ✓ | HOLDS | — |
| 167 | "CI invariant: the `-native` and `-single` variants of one timeline differ only in the declared-scalable fields" | ✓ | HOLDS | — |
| 168 | "every compiled `-single` workload of demand class `oversubscribed` … lands in the measurable oversubscription regime (~100–150% of the lane)" | by static estimate ✓; not once work undeliverable inside the file is removed (D1) | WRONG | DW |
| 168 | "For C7 that puts the interactive counterparts at the regime's ceiling and `c7-gaming` at two and a half lanes" | ✓ | HOLDS | DW |

### 3.14 `dataset/README.md`

| Loc | Statement (verbatim) | Recomputed | Verdict | Decision |
|---|---|---|---|---|
| 74 | "Two compiled variants of the same 50 workloads (64 labeled segments total)" | ✓ | HOLDS | — |
| 78 | "lane-scaled so total demand targets one CPU lane (~100–150%)" | 28 of 50 single files are below 1.00, c7-gaming 2.46 | STALE (over-general; no decision) | DW |
| 86 | "When two workloads **behave identically** and differ only in intent — an ML training run vs. an indexer nobody asked for, a game download vs. a virus scan" | P2 network-bulk vs cpu-batch; P3 differs in mode | STALE (description) | — |
| 88 | C4 "Each file is a clone of a C1/C3 file plus one injected process" | all three are C1 clones | HOLDS | — |
| 89 | C5 "Behavior is held identical across tiers" | ✓ | HOLDS | — |
| 131 | "Every compiled `-single` file of demand class `oversubscribed` must land in the ~100–150% window by the static estimate" | ✓ by the static estimate; see D1 on what the estimate counts | HOLDS (literal) | DW |

### 3.15 `docs/harness/harness-and-records-guide.md` (coreset facts only)

| Loc | Statement (verbatim) | Recomputed | Verdict | Decision |
|---|---|---|---|---|
| 497 | "`game.chain.1`의 것이고, 그건 '입력 처리 stage가 자기 몫(1 ms 미만)을 tick 안에 끝냈나'만 답해요" | heads 230–927 µs in all gaming files | HOLDS | — |
| 545 | "`c2-p1a`의 `hog`는 130초짜리 일을 60초에 시작하고 파일은 180초에 끝나요. 절대 못 끝나요" | ✓ | HOLDS | W |
| 1027 | "head는 1 ms 미만이고 나머지 15단이 십수 ms" | c1-gaming stages 2–16 = 14,353 µs | HOLDS | — |
| 1132, 1137 | "batch C1 base 6개(wanted LOTTERY share를 random row가 빼앗음)" | J2 for c1-backup | WRONG (c1-backup) | JS |
| 1138 | "`c7-gaming`은 note가 붙은 채로 judging(frame은 어떤 row에서도 miss, gap만 읽음). `c7-meeting`·`c7-media`는 … 두 EDF row가 모든 term에서 비겨서" | ✓ (rows only; no fixed claim) | HOLDS | JS |
| 1139 | "foreground 뒤에 아무것도 없어 row가 움직일 게 없음" | no batch-class background task in those ten | HOLDS | JS |
| 1144 | "`c1-idle`은 contention이 없고, `c7-idle`은 scan만 있어" | ✓ | HOLDS | — |
| 1173 | "첫 1분은 a와 b가 byte 단위로 같아서" | background task arrives at 60 s in all three pairs | HOLDS | WIN |
| 1177 | "pair의 두 파일은 raw 숫자가 같고(p1은 완전히, p2·p3는 모양이) … batch는 window 안에서 어차피 못 끝나요" | ✓ | HOLDS | W |
| 1179 | "이 파일은 gate에 안 들어가니" (c1-compile) | c1-compile judges | STALE | JS |
| 1181 | c1-media "video는 10 ms 넘게 기다려야 miss인데 music이 줄 수 있는 대기는 2.5 ms, 반대는 47.5 ms 대 6.67 ms … C5와 `c3-evening`의 media 구간도 같아요" | ✓ | HOLDS | NH |
| 1221 | "query point 134개 중 50개가 terminal, 2개가 ambiguous라 **82개**가 채점되고(49개 파일), 그중 10개가 `pre_committed_miss` segment 위에 있어요" | ✓ | HOLDS | — |

### 3.16 `docs/harness/metrics.md` (coreset numbers only)

| Loc | Statement (verbatim) | Recomputed | Verdict | Decision |
|---|---|---|---|---|
| 247 | "at the current coreset each annotated tier carries one graded query point and tiers 1 and 2 have none" | annotations only on c5-t3/t4/t5 (tiers 3, 4, 5), one graded query point each | HOLDS | — |
| 249 | "Measured on the compiled coreset on 2026-09-11, a constant answer scores 69.5 per cent on the attribute and 11.0 per cent on mode" | 57/82 = 69.5%; gaming 9/82 = 11.0% | HOLDS | — |
| 139–145 (§6.2 guard) | "For every chain, the tail's iteration count equals the head's tick count; a shortfall means a wake was lost." | shortfall is structural in c2-p2a/b and near-certain in c7-gaming (G1) | WRONG (as applied to the compiled gaming files) | G |
