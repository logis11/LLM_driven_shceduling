# 9.16 compiled-number audit — statements about compiled workload behaviour against the final build

This is task 9.16 (the Phase 9 exit audits), the compiled-number audit of `_dev/docs/spec/jioh/task-9.16-exit-audits.md`, decisions 5 and 6. Audited 2026-10-17 on `jioh/dataset-rebuild` at `928aa8fd`, read-only outside this folder. Model: `_dev/research/jioh/2026-09-13-verification/compiled-numbers-report.md`.

## 0. Ground truth

- **Build bytes.** All 51 core files and all 78 variant files in `dataset/build/coreset-single/` hash to their entries in `dataset/build.manifest.json` and `dataset/build.variants.manifest.json` (0 mismatches; `out/pins.out`). No `make` target was run.
- **RQ0 gate spec pins** (`harness/experiments/rq0-gate.yaml:505–511`). The SHA-256 of each pinned file equals the committed file (`out/pins.out`). **HOLDS.**
  - `harness/scoring/scoring-spec.yaml` `2ad757b6…`
  - `harness/guards/guard-spec.yaml` `24ccb875…`
  - `daemon/driver-table/prior.yaml` `0fba4b3c…`
  - `dataset/build.manifest.json` `0f0af422…`
  - `dataset/build.variants.manifest.json` `cdc14319…`
- **Slice context.** Every prior-table row and the primary boot default (`harness/boot-defaults/ostep.json`) use a 10,000 µs top slice. The boot default's `batch_bandwidth_cap` is `null`.
- **Batch class.** Read by the batch-class memo's rule B1, as the reference simulator implements it (`simulator/src/sim.cpp:38–39, 412, 665–692`):
  - A non-periodic task is batch class once it has received one full slice of CPU since its last voluntary block.
  - Every SLEEP, every blocking WAIT and every not-yet-due TIMER resets that count.
  - "Batch CPU share" below means the share of a task's CPU that lies past the first 10 ms of a burst, with the task alone on the lane (`scripts/facts.py`).
- **Measured tables vs compiled files.** A measured table carries ten percentile knots: p1, p5, p10, p25, p50, p75, p90, p95, p99 and p99.9 (`dataset/tools/wlc/sampling.py:75`). Several statements below read those ten knots as if they were deciles.
- **Reference-simulator runs.**
  - What was run: `simulator/src/sim.cpp` at commit `6bf9d850`, compiled into the scratchpad because the committed binary is x86-64.
  - Schedules: single entries — the boot MLFQ (`fixed`), and EDF at a 10 ms residual slice, both with cap `null`.
  - Files: c1-meeting, c7-meeting, c1-media, c7-media, c2-p2a, c2-p2b, c7-gaming and c3-evening (`scripts/sim/`, `out/sim.out`).
  - Limits: the simulator runs the TIMER backlog rule, not the skip rule (conformance item (b)), and does not read the cap (conformance item (d)). Each use below says why neither changes the reading.
- **Scripts and outputs.** Scripts are in `scripts/`; they ran from the scratchpad with its venv, and `facts.py` caches per-file facts in `facts/`. Outputs are in `out/`.

### Verdict legend (as 2026-09-13)

- **HOLDS** — the stated number or behaviour matches the build.
- **STALE** — the number or supporting fact is wrong, but the conclusion drawn from it still stands on the final build.
- **WRONG** — the conclusion, or the stated ground of the decision it supports, does not survive the final build.
- **UNCHECKABLE** — its truth depends on an executor rule the reference simulator does not implement yet. The conformance items are (a)–(h) of statement `simulator-conformance`, `rq0-gate.yaml:325–357`.
  - **NAMED** — the document names the RQ0 gate spec conformance item it waits on.
  - **UNNAMED** — it does not.
  - All are listed by item in `uncheckable-by-item.md`.

A memo's dated record of what was true then is not audited as stale. A statement it presents as current is.

## 1. Facts the verdicts use

| Fact | Value | Source |
|---|---|---|
| Gaming chains (17 members: 16 stages + wineserver) | c1/c4/c7-gaming: sum 14,999 µs, slack 1,668 µs per 16,667 µs frame, 0.90 lanes, head 631 µs, longest stage 1,436 µs; nine stages at 992–1,436 µs, eight of them at 992–1,191 µs. c2-p2a/p2b: sum 15,833 µs, slack 834 µs, 0.95 lanes, head 225 µs; stages ≥ 1,200 µs are 1,220, 1,733, 2,099 and 2,131. c3-evening: 24,166 µs, 1.45 lanes. c6-dual: 10,002 µs, 0.60 lanes | `out/summary.txt` |
| Steam client per C2 frame | 1.310 s of CPU over 86.385 s = 253 µs per 16,667 µs frame | `out/summary.txt` |
| Call (`voice`, period 10,001 µs) | Compiled: cycles ≥ 10 ms in 5.5 % (c1-meeting 330/6,000; c7-meeting 146/2,639); p90 7.48 / 7.68 ms; p95 10.17 / 10.11 ms; p99 12.23 ms; max 15.2 / 14.3 ms; cycles ≥ 14 ms in 0.03–0.04 %. Measured table (`dataset/archetypes.yaml:675`): p90 7,379, p95 9,992, p99 12,221, max 18,851 µs | `out/cycles.out` |
| Video player (period 33,348 µs) | Compiled c1-media: p10 2.80, p50 3.94, p90 5.33, max 11.46 ms; c7-media max 7.28 ms; cycles ≥ 3 ms in 82–83 %, ≥ 5 ms in 17–20 %. Measured table (`archetypes.yaml:619`): p1 2,281, p10 2,800, p50 3,982, p90 5,376, p99.9 7,519, max 16,020 µs. Music: table max 2,381 µs, compiled max 823 µs, period 49,635 µs | `out/cycles.out` |
| Simulator, boot MLFQ vs EDF | c7-meeting voice missed 837/2,639 (31.7 %) vs 151/2,639 (5.7 %). c1-meeting 5.7 % under both. c1-media and c7-media missed 0 under both. c7-gaming head deadlines missed 337/1,583 vs 0. c2-p2a download CPU inside T_end 3.04 s vs 1.06 s; c2-p2b's upgrade 3.45 s vs 1.23 s | `out/sim.out` |
| Download (c2-p2a, SteamCMD, 727.17 s of CPU) | Whole program: 74 % batch CPU share. Its first 2 s of CPU are about 4,500 short runs (longest 11.6 ms), with 0.1 % batch CPU share over the first 1.3 s. EDF delivers 1.06 s of it inside the file | `scripts/alone.py`, `out/sim.out` |
| Unattended upgrade (26.385 s of CPU) | 88–92 % batch CPU share in every file holding it | `out/summary.txt` |
| Keystroke cost (CPU after an input WAIT) | VS Code median 78.6–81.4 ms, ≥ 10 ms in 98–99 %. Office writer median 3.2 ms, mean 4.9 ms, ≥ 10 ms in 15/270. Mail client median 4.8 ms, mean 7.4 ms, 1/35. Browser median 4.0 ms, mean 4.4 ms, 2/123 | `out/summary.txt` |
| Editors' batch CPU share | VS Code 76–87 %; GIMP 93 %; Kdenlive 2–37 % | `out/summary.txt` |
| Counterpart keystrokes | c7-browsing 84 = c1-browsing's 90 before 26.385 s, less 6 at 24.73–25.74 s. c7-office 101 = 112 less 11 at 24.66–26.05 s. c7-dev 49 = 49. c7-indexing 27 = 28 less 1 at 38.96 s. c7-mail 0 (c1-mail's 35 fall at 45.94–53.07 s). c3-workday browser 7. The dropped wakes lie past 24.385 s, the counterpart's focus-window end (`dataset/timelines/coreset/c7.variant.yaml:18`); none lies inside an operation (c7-browsing's page load is at 13.19–13.66 s) | `out/check2.out` |
| Idle lane and job margins (editor replayed alone) | c2-p3b: editor 99.8 s of CPU in 60–326 s, so 166.2 s of idle lane against the backup's 165.67 s of CPU plus 0.19 s of sleeps. c1-backup: 166.5 s vs 165.98 s. c7-backup: 98.9 s vs 165.67 s. Work-conserving finish margins: c1-compile 0.82 s, c1-ml-train 0.88 s, c1-transcode 0.70 s, c1-render 14.0 s, c2-p3a 149.6 s. c3-creation's Kdenlive after 240 s: 0.22 s of CPU in 2,972 s | `out/alone.out` |
| Last frame vs T_end | The frame of the last tick before T_end fits with 468 µs to spare (c1/c4-gaming) and 773 µs (c2-p2a, c2-p2b, c2-p2a-idle). It cannot fit in c7-gaming (tick at 26,383,861 µs, 1,139 µs before T_end, chain 14,999 µs), c3-evening, c6-dual, any c7-gaming variant, or c2-p2a/p2b @chain-x1.2, @chain-x1.4, @seg1-30s, @seg1-120s | `out/lastframe.out` |
| Variants | venue ×0.8 and ×1.25 scale every non-chain RUN and leave the chain untouched. Chain ×1.2: C2 1.14, c7-gaming 1.08 lanes. Chain ×1.4: C2 1.33, c7-gaming 1.26 lanes | `out/variants.out` |
| Demand (manifest) | c2-p1a 14.505, segment 1 35.77; c2-p1b 1.53; c2-p2a 9.383, segment 1 28.53; c2-p2b 1.97; c2-p3a 0.45; c2-p3b 1.01. C7 / C1 pairs: browsing 1.0268 / 0.0164, office 1.0251 / 0.0270, mail 1.0545 / 0.0287, dev 1.2129 / 0.3319, photo 1.0967 / 0.0442, meeting 1.2400 / 0.2387, gaming 1.9149 / 0.9153, media 1.1267 / 0.1280, video-edit 1.5618 / 0.4586, compile 1.1866 / 0.9982, ml-train 1.1405 / 0.9982, render 1.6189 / 0.7339, transcode 1.3727 / 0.9993, indexing 1.0937 / 0.7477, backup 1.4032 / 0.9897, idle 1.0007 / 0.0004 | `out/check2.out` |
| Grid | 67 segments: 1 ambiguous, 19 `false`, 47 `true`, on 32 cells. 8 `pre_committed_miss` segments, one per cell | `out/check2.out` |
| Child-to-child WAKE | 201 of 1,691 files (core 5, variants 8, transition 60, return 90, distractor 32, familiarity 6); 43,620 in c1-compile, 855,150 in all | `out/wakes201.out` |

## 2. Per-document audit

### 2.1 `harness/experiments/rq0-gate.yaml` (the RQ0 gate spec)

| Loc | Statement | Verdict | Evidence |
|---|---|---|---|
| 30–32, 121 | The primary "sits on the measured call's demotion edge: about a fifth of the call's audio-frame cycles consume a 10 ms slice" | STALE | Only 5.5 % of cycles reach 10 ms. The table's p95 is 9,992 µs; "a fifth" reads that knot as p80. The 10 ms slice still sits on the edge, at its 95th percentile, and the primary rests on OSTEP |
| 41–65 | Judging 19, reporting 32, and the reason per file | HOLDS | 19 + 32 = 51. The four batch C1 bases' jobs are normal class and batch (95–100 % batch CPU share). The six idle-class files carry `declared_class: idle`. c7-mail holds no input wake. c7-media misses nothing under either algorithm (simulator) |
| 88–96 | `layer1_exclusions` follow `pre_committed_miss`: the whole file for six, c6-fold from the call's arrival (30 s), c6-spoof from the spoof's (20 s); three judge, five report | HOLDS | `out/check2.out` |
| 102–107 | c6-dual's ground truth is `ambiguous`, with no `background_wanted` | HOLDS | `{mode: ambiguous, attributes: {dual_active: true}}` |
| 123 | 700 µs: "below the C2 gaming pair's 834 µs chain slack per frame (its chain 15 833 µs of 16 667, the Steam client taking about 250 µs of the slack on average)" | HOLDS | 834; 15,833; 253 µs |
| 124 | 900 µs: above 834, below the base's 1,668 (chain 14,999); "demotes the gaming base's nine chain stages at 992 to 1 436 µs" | HOLDS | Nine stages at 992–1,436 µs |
| 125 | 1,200 µs: above "the gaming base's cluster of stages at 992 to 1 191 µs, below its longest stage, 1 436 µs; demotes four C2 stages (1 220 to 2 131 µs)" | HOLDS | Eight stages at 992–1,191 µs; C2 stages 1,220 / 1,733 / 2,099 / 2,131 |
| 126 | 2,000 µs: above every base stage and the C2 1,733 µs stage, below 2,099 and 2,131 | HOLDS | |
| 127 | 3,000 µs: "inside the video player's cycle range (decile cuts 2.3 to 7.5 ms), demoting about seven in ten of its cycles" | STALE | 2.3 and 7.5 ms are the table's p1 and p99.9. Its deciles run 2.80–5.38 ms (compiled 2.80–5.33). 82–83 % of compiled cycles reach 3 ms. 3 ms is inside the range either way |
| 128 | 5,000 µs: "between the video player's median cycle (4.0 ms) and its upper decile (7.5 ms)"; the compositor reason left with the compositor task | STALE | The 3.98 ms median holds. The upper decile is 5.38 ms (table) or 5.33 ms (c1-media). 5 ms is still between the two. No core file has a compositor |
| 129 | 14,000 µs: "above the call's 12.2 ms ninth-decile cycle, below its 18.9 ms and the video player's 16.0 ms maxima, so the call is demoted in under a tenth of its cycles and the player almost never" | STALE | 12.2 ms is the call's p99; its p90 is 7.4–7.7 ms. 18.9 and 16.0 ms are the tables' maxima; the compiled maxima are 15.2 / 14.3 ms (call) and 11.5 / 7.3 ms (video). The call reaches 14 ms in 0.03–0.04 % of cycles, so the conclusion holds |
| 130 | 20,000 µs: "above every periodic task's longest cycle" | HOLDS | True on the judging files (c7-meeting's call 14.3 ms; chain stages ≤ 2.1 ms) and on both tables' maxima. Reporting files exceed it: c3-evening's video 59.4 ms and music 65.5 ms, c6-fold's call 324 ms |
| 148, 159 | venue ×0.8 and ×1.25: every measured RUN scaled, the chain excluded | HOLDS | `out/variants.out` |
| 170 | chain ×1.2 scales the chain's RUN values | HOLDS | |
| 176 | chain ×1.4: "the chain exceeds the lane in all three files (1.14 and 1.26 lanes)" | STALE | ×1.4 gives 1.33 (C2) and 1.26 (c7-gaming); 1.14 is the C2 pair at ×1.2. Every file does exceed the lane |
| 182 | The C2 first segment is 60 s; "every other judging length is a job's measured CPU total" | STALE | True of the C2 second segments (39.435 s, 26.385 s) and the C7 counterparts. c2-p3a's 266 s and the lengths of c1-compile, c1-ml-train and c1-transcode are a job's CPU plus the editor's (margins 0.7–0.9 s). c1-render's 60 s is neither |
| 188 | seg1-120s: "expected unchanged, the terms reading the second segment" | no separate verdict | On @seg1-120s and @seg1-30s the `tick_count` guard fails by construction (guard spec row; finding G1) |
| 210 | The trace replay rebuilds four files on six streams under `dataset/replay/` | HOLDS | Six `replay-*.json.gz` files |
| 219 | c2-p2a and c2-p2a-idle are "byte-identical but for the download task's declared class" | HOLDS | The events differ only in that field; `meta.id` differs as the file id |
| 223–228 | c7-gaming note: the chain takes 0.9 of the lane, 1,668 µs of slack, and the boost hands the upgrade a 10 ms slice inside a frame | HOLDS | Head deadlines missed 337/1,583 under the boot MLFQ, 0 under EDF |
| 232–236 | c1-gaming note: the chain at 0.9 beside the Steam client | HOLDS | c1-gaming holds the chain and `steam` only |
| 240–248 | c7-meeting note: the call's cycle run "consumes the boot slice in about a fifth of its cycles"; under EDF it "misses only its own overruns, about 5 %"; the tie with fixed is gone | STALE | 5.5 %, not a fifth. EDF misses 5.7 % (overruns are 5.5 %). Fixed misses 31.7 %, so the headroom and the judging decision hold |
| 252–257 | c7-media note: worst video cycle 16.0 ms against 33.3 ms, longest MLFQ wait 32 ms, music 2.4 ms against 49.6 ms, 1.3 ms margin, no headroom | HOLDS | Stated on the measured tables, whose maxima these are. The compiled file's worst video cycle is 7.28 ms. Nothing missed under either algorithm |
| 261–266 | c7-mail note: c1-mail's 35 keystrokes fall at 45.9–53.1 s, past the cut | HOLDS | 35 at 45.94–53.07 s; c7-mail holds 0 |
| 274–291 | Statement `judging-set`: membership; the two EDF rows tie on the chain or call term | HOLDS | The chain and the call are periodic class (rule B2), which the cap never reaches |
| 294–311 | Statement `idle-class-files`: the six files hold Tracker's indexer and Déjà Dup's backup | HOLDS | Names and `declared_class: idle` |
| 296–304 | "no row's share or cap reaches the background task: its turnaround or progress is identical under every row and the editor's wait is untouched by it" | UNCHECKABLE, UNNAMED | Waits on conformance item (e), the strict idle class |
| 366–378 | Statement `prior-table-structure`: 32 rows, 8 configurations, 13 rows on MLFQ with cap 0.05, nine judging files map there (41 %), the other ten to rows shared by at most three | HOLDS | `prior.yaml` configurations: 7 + 13 + 2 + 1 + 3 + 2 + 3 + 1 |
| 413–417 | Statement `boot-default-sweep`: slack 834 / 1,668 µs, longest stages 1,436 / 2,131 µs; "the video player's cycle range (2.3 to 7.5 ms at the decile cuts, 16.0 ms at most) and the call's demotion edge (about a fifth of its cycles above 10 ms, its ninth decile 12.2 ms, its maximum 18.9 ms)" | STALE | The chain numbers hold. The decile labels and "a fifth" are wrong, as in rows 30–32 and 127–129 |
| 442–444 | "a 26 s counterpart holds about a hundred keystrokes and c3-workday's browser seven" | STALE | 49 (c7-dev) to 101 (c7-office); c3-workday's browser has 7. The point — a P99 over so few wakes is the top one or two waits — holds |
| 445–448 | A counterpart's input wakes "are those of the base's first 26.385 s less the ones inside its own operations" | STALE | They are the base's wakes before 24.385 s, where the counterpart's input window ends. c7-browsing drops 6 and c7-office 11 past it; none lies inside an operation |
| 505–511 | Pins | HOLDS | §0 |

### 2.2 `harness/scoring/scoring-spec.yaml`

| Loc | Statement | Verdict | Evidence |
|---|---|---|---|
| 9–10 | The `timer` channel is "on the fourteen terms of the video editor (kdenlive) and the image editor (GIMP)" | HOLDS | 15 timer-channel terms, one of them c7-mail's mailer |
| 36–43 | The six idle-class files: "no row reaches the background task; its turnaround or progress is identical under every row and the editor's wait is untouched by it" | UNCHECKABLE, UNNAMED | Waits on item (e), the strict idle class. The file list and classes hold |
| 44–46 | c1-media, C5 (c5-t4, c5-t5) and c1-meeting: the jobs miss only their own overruns, the call in about 5 % of its cycles, under any row | HOLDS | c1-meeting 5.7 % under both algorithms; media 0 |
| 47–50 | c7-media: worst video cycle 16.0 ms vs 33.3 ms, longest wait 32 ms, music 2.4 vs 49.6 ms, 1.3 ms margin | HOLDS | As gate spec 252–257 |
| 51–54 | c2-p2a's download is "batch class now (the measured SteamCMD runs back to back)"; the chain takes 0.95 under EDF, so the residual is below any cap; the boot MLFQ hands it more; the oracle's improvement is negative | STALE | The part of the download the file delivers under EDF (1.06 s) is its launch phase of short runs, at 0.1 % batch CPU share, so the cap does not reach it there either. The 0.95 lanes holds. The download gets 3.04 s under the boot MLFQ vs 1.06 s under EDF, so "no headroom" holds |
| 55–56 | c3-creation's transcode is uncontended after 240 s but for the editor's idle wakes | HOLDS | Kdenlive takes 0.22 s of CPU in 240–3,212 s |
| 57–61 | c7-mail: the slice holds none of c1-mail's 35 keystrokes | HOLDS | |
| 62–65 | c3-evening: 1.45 lane share; "under the TIMER skip rule the term reads the policies' ordering above a floor of about 0.31 missed under every policy" | HOLDS (floor); UNCHECKABLE, UNNAMED (ordering) | 1 − 16,667/24,166 = 0.310, a lane-capacity bound under any rule. The ordering waits on item (b), the TIMER skip rule: under the backlog rule the simulator misses 99.8 % (MLFQ) and 99.97 % (EDF) |
| 66–68 | c7-meeting: the call's cycle run "consumes the boot slice in about a fifth of its cycles and is demoted, so the tie with fixed … is gone" | STALE | 5.5 %. Fixed misses 31.7 % vs EDF 5.7 %, so the tie is gone |
| 90–96 | Generated layer: "no job is sure to outlive its file under every row (arrival, its own CPU and its own blocks fit inside the file)" | HOLDS | 1,456 batch jobs in 1,562 generated files. One exceeds by 1 µs: the `7z` distractor in `dx-gaming-with-7z` (60 s of CPU arriving at 60 s, one 1 µs sleep, T_end 120 s). It carries no term (lines 82–84) (`out/genjobs.out`) |
| 96–98 | The idle-class placements' job ends at the same time under every row | UNCHECKABLE, UNNAMED | Item (e) |
| 114 | c1-gaming: the 17-member chain, the compositor retired | HOLDS | No core file has a compositor |
| 125–130 | The call is one task, one job per 10 ms audio frame; the mode weights | HOLDS | `voice`, period 10,001 µs |
| 30–32, applied at 112 and 238 | c1-compile's and c4-compile's `build` turnaround: "a job that finishes under every row" | HOLDS (finishing); UNCHECKABLE, UNNAMED (turnaround) | The build fits with 0.82 s to spare under any work-conserving row. Its turnaround is `make`'s exit, which waits on item (g), `WAIT children:<id>`. Without (g), `make` never exits and every row reads the same censored value (final memo §6.2) |
| 168–172 | The C2 files end at 99.435 s, 86.385 s and 326 s; "Progress terms unwindowed (the batch task arrives at 60 s and does not finish inside the file)"; the P3 render finishes under every row | WRONG (c2-p3b); HOLDS (rest) | The c2-p3b backup finishes inside the file (row 204–205). The P1 training run (1,389.885 s) and the P2 download (727.17 s) do not. The render fits with 149.6 s to spare |
| 181–183 | c2-p2a comment: the download is batch class | STALE | As lines 51–54 |
| 198–199 | c2-p3a: Kdenlive's export, 16.5 s of CPU in a 266 s segment, finishes under every row | HOLDS | 16.545 s; margin 149.6 s |
| 204–205 | c2-p3b: "the idle-class backup gets the editor's idle lane only, about 162 s of its 165.7 s, and does not finish: progress" | WRONG | Replayed alone, the editor takes 99.8 s of 60–326 s. That leaves 166.2 s of idle lane against the backup's 165.67 s of CPU and 0.19 s of sleeps, so the backup finishes about 0.3 s before T_end. (The 162 s is the manifest's even spread of the editor's 126.9 s over its 326 s life.) By the header's own rule (lines 30–32) the term would be turnaround. The file stays no headroom and reporting-only |
| 276–279 | "the renamed or flipped batch job carry no term, so the false row's floor cap is free to act" | STALE | The injected upgrade is batch class (88–92 %), and so are the DKMS jobs (89 %). For c7-indexing and c7-backup the flipped job is idle class, which no cap reaches; both files are reporting-only |
| 289–293 | c7-mail comment: window 2–24.385 s; c1-mail's 35 keystrokes at 45.9–53.1 s | HOLDS | |

### 2.3 `harness/guards/guard-spec.yaml`

| Loc | Statement | Verdict | Evidence |
|---|---|---|---|
| 77–82, 177–186 | `tick_count`: "a chain tail's iteration count equals its head's tick count … Any message is a fail" | WRONG (as applied to the compiled files) | See note G1 below the table |
| 101–105 | P1 Tracker's indexer in the training run's place, P2 the unattended upgrade in the game download's, P3 Déjà Dup's backup in the video render's | HOLDS | c2-p1b `tracker-miner-f`, c2-p2b `unattended-upgr`, c2-p3b `deja-dup` |
| 213–216 | `c2-p2a-idle` changes a task's entry and no label | HOLDS | |

**Note G1 (the `tick_count` row).**
- c7-gaming, a judging file, is cut at 26.385 s. The head consumes tick 1,583 at 26,383,861 µs, 1,139 µs before T_end. That frame needs 14,999 µs of chain CPU.
- So on every run the tail completes one iteration fewer than the consumed ticks that `harness/tools/harness/primitives.py:301–309` counts. The guard fails, and `harness/tools/harness/evaluator.py:369–390` makes the RQ0 verdict `invalid`.
- The shortfall comes from the file's cut, not from a lost wake.
- The same happens by construction on c3-evening and c6-dual (reporting), every c7-gaming variant, and c2-p2a/p2b @chain-x1.2, @chain-x1.4, @seg1-30s and @seg1-120s.
- Today's simulator emits no ready line for the arrival TIMER (item (a)), so its counts happen to tie: 1,583 vs 1,583 under EDF. Under the contract's reading (metrics doc §11, assumption 4: the first `ready(timer_tick)` line is at arrival) they differ by one.

### 2.4 `daemon/driver-table/prior.yaml`

| Loc | Statement | Verdict | Evidence |
|---|---|---|---|
| 30–34 | An idle-class task runs only when no other-class task is runnable, so no row's share or cap reaches it | UNCHECKABLE, UNNAMED | Item (e) |
| 39–41 | A keystroke costs the office writer and the mail client about 5 ms, "the browser next to nothing", so those block inside one 10 ms slice | STALE | Median / mean: writer 3.2 / 4.9 ms, mailer 4.8 / 7.4 ms, browser 4.0 / 4.4 ms — so the browser is not "next to nothing". 94–99 % of the three's keystrokes stay under 10 ms |
| 41–43 | A keystroke costs VS Code about 78 ms, so MLFQ demotes it within the keystroke | HOLDS | Median 78.6–81.4 ms; ≥ 10 ms in 98–99 % |
| 58, 64 | browsing/true: c6-spoof's miner named chrome; the browser's keystroke work is far below one slice | HOLDS | `spoof` is named `chrome`, 30 s of CPU from 20 s; browser median 4.0 ms |
| 70, 96, 122, 148, 174, 278, 460 | The false rows name each counterpart's unattended upgrade, the stock install stage bound whole | HOLDS | 26.385 s of CPU in each |
| 96 | office/false: c4-office's 7z archive run whole is the shape of a wanted one | HOLDS | One 6 s RUN at 30 s, under `office/true` |
| 110, 116 | mail/true: c1-mail's and c3-workday's mailer P99; a keystroke costs about 5 ms | HOLDS | |
| 136, 142 | dev/true: c2-p1's first minute; with nothing CPU-bound beside it the queue below is empty | HOLDS | The training run arrives at 60 s; c1-dev holds the editor alone |
| 162, 168 | photo/true: GIMP's own wakes; an editor whose bursts outlast a slice | HOLDS | GIMP 93 % batch CPU share |
| 188 | meeting/true: one task, a job per 10 ms audio frame; about one cycle in twenty exceeds its period | HOLDS | 5.5 % of cycles exceed 10,001 µs |
| 200 | meeting/false: the boot MLFQ demotes the call's long cycles into the upgrade's queue; the EDF rows have headroom | HOLDS | 31.7 % vs 5.7 % missed |
| 214 | gaming/true: 16.7 ms period, weights 1.0 : 0.5, "The measured download runs back to back and is batch class, but the chain takes 0.95 of the lane under EDF, so what it leaves is below any cap and the download's progress is expected no headroom" | STALE | As scoring spec 51–54 |
| 220 | c3-evening's chain at 1.45 lanes; the base and the pair fit at 0.9 and 0.95 | HOLDS | |
| 226 | gaming/false: c2-p2b's and c7-gaming's upgrade; the boost hands it a 10 ms slice inside a frame with under 1.7 ms of slack | HOLDS | Head misses 337 vs 0 (c7-gaming) and 18 vs 0 (c2-p2b) |
| 240, 252 | media: mpv's 30 fps frames and 49.6 ms audio cycles; the boot MLFQ keeps every tick on the measured tables | HOLDS | Periods 33,348 and 49,635 µs; nothing missed |
| 266, 272 | video-edit/true: Kdenlive in c2-p3's first minute and c3-creation; long edit bursts demoted | HOLDS | Kdenlive bursts reach 234 ms |
| 292 | compile/true: makespan 1.0 against 1.0; "the measured kernel build's 2,908 object jobs"; "the editor is guaranteed the other half while it is runnable" | STALE | 2,908 jobs × 6 members holds. But 83 % of c1-compile's editor CPU lies past 10 ms of a keystroke burst. There the editor is batch class and, by the LOTTERY rule this row's own entry states (line 298), holds one ticket among the batch class's runnable tasks — up to eight build members. The half holds at the keystroke's wake, where the scored wait is taken |
| 310 | compile/false: MLFQ demotes each CPU-bound compiler child within a few slices | HOLDS | 590 of c7-compile's 9,980 children reach 10 ms of a burst, and they hold 89 % of the children's CPU |
| 318 | ml-train/true: the batch class gets a third "and the editor's keystrokes the rest while they are runnable" | STALE | As line 292: 87.5 % of c2-p1a's editor CPU is batch class, shared evenly with the training run — as the pair review's p1 row already states |
| 330 | ml-train/false: c7-ml-train is the same run flipped, a pre-committed miss | HOLDS | |
| 336, 414 | ml-train/false and indexing/false: "One CPU-bound job [intruder] under an interactive editor is MLFQ's textbook case" | STALE | The editor in c7-ml-train, c2-p1b and c7-indexing is VS Code, demoted within each keystroke (header lines 41–44). In c2-p1b and c7-indexing the intruder is idle class |
| 344, 362 | render: Kdenlive's measured export in c1-render and c2-p3a; the CPU-bound render | HOLDS | 96 % batch CPU share |
| 370 | transcode/true: HandBrake in c1-transcode and c3-creation; after editing stops the cap barely bites | HOLDS | 0.22 s of editor CPU after 240 s |
| 396, 408, 422, 434 | indexing and backup rows: the indexer and the backup declare the idle class, so the share or floor never reaches them | UNCHECKABLE, UNNAMED | Item (e). The classes and files hold |
| 408 | indexing/false: Tracker in c2-p1b and c7-indexing; the only scored term is the editor's | HOLDS | |
| 422 | backup/true: Déjà Dup in c1-backup and c2-p3b, progress weight 0.25 | HOLDS | |
| 448 | idle/true: c1-idle's four session daemons | HOLDS | gnome-shell, pipewire, systemd, dbus-daemon |

### 2.5 `docs/daemon/prior-table-pair-review.md`

| Loc | Statement | Verdict | Evidence |
|---|---|---|---|
| 15, 34, 35, 44 (p1b), 46 (p3b), 67, 68, 81 | The idle-class indexer and backup: no row's share or cap reaches them, their outcome is identical under every row, the editor's wait is untouched | UNCHECKABLE, UNNAMED | Item (e) |
| 21 | browsing: c6-spoof's oracle reads `browsing/true` to 20 s and `browsing/false` from 20 s | HOLDS | Ground truth |
| 21, 24, 54, 83 | "the 0.05 cap holds the miner"; "the cap bounds the upgrade in the queue they then share"; "the floor cap bounds it"; the editors' waits "read the floor cap's effect" | UNCHECKABLE, UNNAMED | Item (d), the cap as a work-conserving ceiling |
| 22 | c4-office's 7z runs whole under `office/true` | HOLDS | |
| 24 | dev: c2-p1's first minute has no batch; VS Code's 78 ms keystroke is demoted within the keystroke | HOLDS | |
| 26, 27, 28 | meeting, gaming, media rows: the rows tie on the periodic term by design; c2-p2a's download progress has no headroom; the boot MLFQ keeps every media tick | HOLDS | Simulator: download 3.04 vs 1.06 s; media nothing missed |
| 30 | compile: `build` turnaround 1.0 in c1-compile and c4-compile | UNCHECKABLE, UNNAMED | Item (g), for reading the turnaround |
| 32, 33 | The render finishes under every row; the encode is uncontended after 240 s | HOLDS | Margins 14.0 s and 149.6 s; 0.22 s of editor CPU |
| 40 | 1,389.885 s and 727.170 s of CPU in 39.435 s and 26.385 s: 35.77 and 28.53 | HOLDS | Manifest |
| 44 | p1: 1,390 s of CPU bound whole in the 39 s segment; the LOTTERY reading; demand 35.77 / 1.53 | HOLDS | |
| 45 | p2: "the measured download is batch class now (SteamCMD runs back to back), but the chain takes 0.95 of the lane …"; the boost and under 1.7 ms of slack; 28.53 / 1.97 | STALE | The batch-class claim is wrong, as scoring spec 51–54; the rest holds |
| 46 | p3: the export (16.5 s) finishes under every row; p3b's backup "gets the editor's idle lane only, about 162 s of its 165.7 s"; 0.45 / 1.01 | STALE | The idle lane is 166.2 s (scoring spec 204–205). The conclusion — neither knob reaches it, progress cannot move — holds |
| 50 | The upgrade bound whole at 26.385 s; each counterpart is the base's first 26.385 s, "its keystroke window a slice of the base's …, so its keystrokes are the base's over those seconds"; the five flipped files are cut to the job's CPU total | STALE (keystrokes); HOLDS (rest) | The window ends at 24.385 s, dropping 6 (browsing) and 11 (office) of the base's keystrokes. Job lengths: 1,389.88, 16.545, 2,970.87, 39.435, 165.668 s |
| 54 | browsing: "79 …, the base's 85 over the same seconds less the 6 inside the counterpart's page load"; the upgrade is batch class; demand 1.02 / 0.02 | STALE | 84 = 90 less 6; the 6 lie past 24.385 s, none in the page load. Upgrade 88 % batch. Demand 1.03 / 0.02 |
| 55 | office: "91, the base's 102 …" | STALE | 101 = 112 less 11 past 24.385 s |
| 56 | mail: 35 keystrokes at 45.9–53.1 s; demand 1.05 / 0.03 | HOLDS | |
| 57 | dev: "(47, the base's 47 over the same seconds)"; 78 ms keystrokes demoted; demand 1.29 / 0.33 | STALE | 49 / 49; demand 1.21 / 0.33 |
| 58 | photo; demand 1.10 / 0.04 | HOLDS | |
| 59 | meeting: "the call's long cycles (about a fifth above 10 ms) are demoted … and miss, so the EDF rows have headroom"; 1.24 / 0.24 | STALE | 5.5 %; 31.7 % vs 5.7 % missed |
| 60 | gaming: the chain at 0.9 fits the lane, so frames miss only under the boost; 1.91 / 0.92 | HOLDS | 337 vs 0 head misses |
| 61, 62 | media 1.13 / 0.13; video-edit 1.56 / 0.46 | HOLDS | |
| 63 | compile: the DKMS jobs are the batch class the floor holds; demand 1.11 / 1.00 | STALE (demand) | The jobs' 89 % batch CPU share holds; demand is 1.19 / 1.00 |
| 64, 65, 66 | ml-train 1.14 / 1.00; render (the export's 16.5 s) 1.62 / 0.73; transcode 1.37 / 1.00 | HOLDS | |
| 67 | indexing demand 1.10 / 0.75 | STALE | 1.09 / 0.75 |
| 68, 69 | backup 1.40 / 0.99; idle 1.00 / 0.00, the upgrade alone puts it at one lane | HOLDS | |
| 71 | The interactive counterparts sit "just above one lane", c7-gaming at 1.9, c7-idle at one lane, and "the batch counterparts near their bases since a label flip adds no work" | STALE | c7-dev is 1.21, c7-meeting 1.24, c7-video-edit 1.56. The batch counterparts read 1.09–1.62 against bases of 0.73–1.00, because each is cut to its job's CPU total |
| 75 | Finding 1, 2026-10-09: the download "runs back to back with near-zero sleeps and is batch class, so the cap reaches it — but … what EDF leaves is below any cap" | STALE | The delivered part is not batch class. The conclusion — the cap cannot favour it — holds |
| 78 | Finding 4: 67 segments, 66 on cells, 19 `false`, 47 of 66, the eight pre-committed misses as listed | HOLDS | |
| 79 | Finding 5: slack 0.8 ms (pair, 0.95) and 1.7 ms (base, 0.9); c7-meeting's call "consumes the boot slice in about a fifth of its cycles"; media tolerances 17 and 47 ms; c7-media 32 ms against 33.3 ms | STALE ("a fifth"); HOLDS (rest) | 5.5 %. The tolerances come from the tables' maxima (33.3 − 16.0 and 49.6 − 2.4) |
| 82 | Finding 8 | HOLDS | |
| 83 | Finding 9: the writer and mail client about 5 ms, "next to nothing (the browser)", VS Code 78 ms; the first three stay on top | STALE | The browser's median is 4.0 ms; it still blocks inside a slice |
| 84 | Finding 10: "c7-browsing 79, c7-office 91, c7-dev 47, c7-indexing 27"; c3-workday's browser 7; "the base's over the slice … less the ones inside the counterpart's own operations" | STALE | 84, 101, 49, 27; 7. The dropped wakes lie past 24.385 s |

### 2.6 Open memos

| Memo · Loc | Statement | Verdict | Evidence |
|---|---|---|---|
| repeat-samples (2026-09-07) | — | none | No compiled-number statement |
| trace-clarifications (2026-09-07) · 38 | "The game chain is sixteen tasks" | STALE | 17 members (16 stages and wineserver) in every chain file. The body is dated but uncorrected |
| trace-clarifications · 68 | The head's deadline line answers whether the input stage finished "its 230 µs" | STALE | Heads are 225 µs (C2), 631 µs (c1/c4/c7-gaming), 746 µs (c3-evening), 911 µs (c6-dual). All are sub-millisecond, so the point holds |
| trace-clarifications · 76 | "`c2-p1a`'s training run has 130 s of work from t = 60 s in a file whose labels end at 180 s" | STALE | 1,389.885 s from 60 s; the labels end at 99.435 s. The advice holds |
| algorithm-switch (2026-09-08) | — | none | Its numbers (2,000 µs slices, `W_single` = 6,000 µs) are boot-default config, not the compiled workload; noted in `findings.md` |
| batch-class (2026-09-09) · 21–29 | The motivating table: c2-p2b's `clamscan`, c1-gaming's `compositor`, chain stages 0.2–2.2 ms | STALE | c2-p2b's background is the unattended upgrade; no core file has a compositor; stages run 0.22–2.38 ms. The rule's motivation (rule B2 keeps frames out of the batch class) holds |
| batch-class · 50, 52, 60 | "The boot slice is 2 ms throughout"; a hog enters the class "Two ms after its first dispatch"; an editor "becomes batch 2 ms into the burst" | STALE | The boot slice is 10 ms |
| batch-class · 54 | c2-p2a's download: "run about 1 ms, sleep about 5.7 ms" 22,000 times, never batch class; "The cap does not apply to it, in any row" | STALE | 422,242 operations, 74 % batch CPU share over the whole program. The part the file delivers under EDF is 0.1 % batch. The cap does not act on it in the file, for the pair review's later reason |
| batch-class · 56 | c2-p3b's `borg`: "Run 3 ms, sleep 2 ms", batch for the last third of every burst; "the cap bites, partially … that is what the row intends" | WRONG | c2-p3b's background is Déjà Dup, idle class, which no cap or share reaches (`prior.yaml:30–34`) |
| batch-class · 58 | "In `c2-p2b` the 0.05 cap therefore lands on `clamscan` alone" | STALE | It lands on the unattended upgrade (92 % batch CPU share) |
| batch-class · 60–63 | "the editors' keystroke bursts are long — a median of 80–90 ms of CPU per keystroke" (`code`, `soffice.bin`, `kdenlive`) | STALE | VS Code 79–81 ms; LibreOffice Writer 3.2 ms median; Kdenlive has no keystroke stream. The conclusion — the wake-to-run wait is protected — holds |
| batch-class · 69 | §5: c2-p2a's cap is inert because the download never enters the class; c2-p2b's cap acts "on the CPU-bound scan"; "a 1 ms chunk is shorter than every legal slice" | STALE | The download's program now holds runs up to 62.6 s; the scan is now the upgrade. The decision (keep the file, state the limit) stands on the pair review's finding 1 |
| invocation (2026-09-11) | — | none | |
| rq0-pre-registration (2026-09-12) · 52–57 | Correction: judging 19; nine judging files on the MLFQ-0.05 row (41 %); sweep reasons rewritten; random runs 12,900 = (51 + 78) × 100 | HOLDS | The body's 25 files, 831 µs slack and 6,667 µs compositor are corrected there |
| dataset-validity (2026-09-20) · 45 | Correction: c2-p1a 14.505 lanes, segment 1 35.77; c2-p2a 9.383, 28.53 | HOLDS | Manifest |
| dataset-validity · 46 | c6-dual's focus alternates every 688 s | HOLDS | 17 spans of 688 s and a last of 376 s |
| timer-skip (2026-10-07) · 45 | "The `job` miss rate is 26 of the scoring spec's 78 terms"; c3-evening's game segment at `lane_share` 1.45 | STALE (count); HOLDS (1.45) | 22 of 75 terms today |
| declared-class (2026-10-08) · 9 | `idle` "on the two entries whose programs declare it" | STALE | Since 9.13 three entries carry `idle`: `file-indexer`, `incremental-backup` and `game-download-idle` (compiled into c2-p2a-idle) |

### 2.7 Final memo, `docs/memos/2026-10-17-workload-dataset-rebuild.md`

| Loc | Statement | Verdict | Evidence |
|---|---|---|---|
| 31 | 28 of 29 archetypes measured; `game-task-chain` from `lavd-ossna24` | not audited | A library statement; belongs to the claim audit |
| 41, 113–121, 123, 129 | Generated layer 1,562 files (480 / 720 / 24 / 272 / 66), 78 variants, about 6.8 GB | HOLDS | 7.27 × 10⁹ B = 6.77 GiB |
| 58–69 | c1-indexing's indexer is `idle`, its program opening `RUN 38048`, `SLEEP 123`; seven core files hold idle-class work; three idle programs | HOLDS | |
| 71–77 | In c1-indexing the indexer yields at once to the editor's wake; this is item (e) | UNCHECKABLE, NAMED | Item (e) |
| 87–100 | c1-indexing's focus is `[{0, 60000000, editor}]`; the t = 0 snapshot is `code` × 1 | HOLDS | |
| 137–152 | c1-compile's `make` (`RUN 229`, `FORK`, `fork_cap` 48, `WAIT children:build`) and job 1's `sh` (848 µs) → `gcc` (1,731 µs) → `cc1` | HOLDS | |
| 157–161 | 201 of 1,691 files: core five, eight variants, generated 188 (60 / 90 / 32 / 6); 43,620 in c1-compile, 855,150 in all | HOLDS | `out/wakes201.out` |
| 169–178 | c1-indexing's editor ends `RUN 75`, `WAIT`; the indexer ends `EXIT` | HOLDS | |
| 277 | (g): `make` runs eight jobs at once; without (g), c1-compile's build time is the same censored value under every condition | UNCHECKABLE, NAMED | Item (g); `fork_cap` 48 = 8 × 6 |
| 290 | c1-gaming has no compositor; c2-p2b's background is `package-upgrade`, named `unattended-upgr` | HOLDS | |
| 299 | `fork_cap` = N × 6 on the kernel-build files (c1-compile 8 × 6); c7-compile's 1,557 jobs of 6 / 8 / 10 members (1,325 / 145 / 87); every spawn-table file has `fork_cap` | HOLDS | c1-compile, c3-workday, c4-compile and c6-dual each have 2,908 jobs × 6 |
| 309 | The two gaming rows tie on the frame term | HOLDS | Periodic class (rule B2) |
| 310 | The boost gives the upgrade a 10 ms slice inside a frame with under 1.7 ms of slack | HOLDS | |
| 311 | Chain 0.9 (c1-gaming), 0.95 (c2-p2a/p2b), 1.45 (c3-evening) | HOLDS | |
| 312 | "`c2-p2a`의 다운로드는 쉬지 않고 돌아서 batch class예요" (the download runs without rest and is batch class) | STALE | As scoring spec 51–54 |
| 339 | c6-dual 187,601,795 B; the core set about 678 MB | HOLDS | 678,172,716 B |

## 3. Counts

| Document | HOLDS | STALE | WRONG | UNCHECKABLE (NAMED / UNNAMED) |
|---|---|---|---|---|
| RQ0 gate spec | 20 | 10 | 0 | 1 (0 / 1) |
| scoring spec | 13 | 4 | 2 | 4 (0 / 4) |
| guard spec | 2 | 0 | 1 | 0 |
| prior table | 20 | 5 | 0 | 2 (0 / 2) |
| pair review | 17 | 14 | 0 | 3 (0 / 3) |
| open memos | 4 | 11 | 1 | 0 |
| final memo | 12 | 1 | 0 | 2 (2 / 0) |
| **total** | **88** | **45** | **4** | **12 (2 / 10)** |

A row that carries two verdicts counts once under each. The UNCHECKABLE rows are grouped by location here; `uncheckable-by-item.md` lists every location.
