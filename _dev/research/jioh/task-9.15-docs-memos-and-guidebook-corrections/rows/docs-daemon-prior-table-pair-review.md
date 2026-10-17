# Work-list rows — `docs/daemon/prior-table-pair-review.md`

Chunk K09, Simulator and daemon docs (wave 2). 5 open rows. The file has 84 lines at `d5cc7711`.

### W-0458 · applied
- At: `docs/daemon/prior-table-pair-review.md` ## B. The C2 row-pairs, the p1 row (`c2-p1a` / `c2-p1b`), line 42 ('… the 0.333 share carries `hog` progress (weight 0.5) while the editor keeps two thirds of what it contends for.')
- Change: Scope 'the editor keeps two thirds of what it contends for' to the simulator's LOTTERY draw: two thirds while the editor's run since its last voluntary block is within one 10 ms slice; past it the editor is batch class too (batch-class memo rule B1), the non-batch class is empty, and it shares the batch class's draws evenly with the training run (`simulator/src/sim.cpp:328–333`, `:362–366`).
- Final word: The heads-up memo's LOTTERY question (2026-09-13 heads-up memo §4 question 1, which names 'pair review p1' among the sentences its answer bears on) is answered by the reference simulator's code: only runnable tasks hold tickets; the class is drawn by `batch_share` only when both classes are runnable, otherwise the runnable class takes every draw, uniform inside it (`simulator/src/sim.cpp:328–333`, `:362–366`); batch class per the 2026-09-09 batch-class memo's rule B1 (`sim.cpp:410–413`).
- Sources: merge finding (`docs/daemon/prior-table-pair-review.md:42`)
- Cross-ref: W-0777; W-0702; W-0761; the pair review's p1-row rows (W-0464)
- Notes: Raised by resolving the for-인지오 row on the LOTTERY question (W-0761). Describe the rule; do not assert how often the editor's runs pass one slice on `c2-p1a` (not measured). Another chunk's rows on the same line (W-0464, already applied, the p1 row's training-run wording) touch the same cell with a different change.

### W-0459 · applied
- At: `docs/daemon/prior-table-pair-review.md` §A Same-mode pairs, browsing row, line 19 ("in `c6-spoof` the oracle reads `browsing/true`, so the 0.5 cap is the one that holds the miner")
- Change: Restate the clause: in `c6-spoof` the oracle reads browsing/`true` to 20 s and browsing/`false` from the spoof's arrival at 20 s, so from then the 0.05 cap holds the miner under the oracle; a name-based recognizer answering browsing/`true` leaves it the 0.5 cap, the row the driver table's browsing/`true` justification describes.
- Final word: 9.23 D2 (`c6-spoof` split at the spoof's arrival, 2026-10-14): 0–20 s browsing, `background_wanted: true`; 20–60 s browsing, `background_wanted: false`, `spoof: true`, `pre_committed_miss: true`; the oracle reads browsing/`false` from 20 s and applies that row (cap 0.05) to the miner; the driver table's browsing/`true` justification (`daemon/driver-table/prior.yaml:58`, the miner held to half the lane) describes the row a name-based recognizer applies to the spoof and stays.
- Sources: SX-0349 (TODO 9.15 line (from 9.23 D2), `_dev/TODO.md:179`); SX-0591 (9.23 D2, `task-9.23-guidebook-findings/changelog.md:23`)
- Notes: Checked at HEAD: `dataset/timelines/coreset/c6-spoof.timeline.yaml:19–35` (the two segments as above); `daemon/driver-table/prior.yaml:53–58` (browsing/`true` cap 0.5, its justification naming c6-spoof's miner); the browsing/`false` row is MLFQ, cap 0.05 (the same table row, line 19). The pair review is Status: record and has been revised in place under dated revision notes at its top (9.14, 9.18): follow that form and bump Updated.

### W-0460 · applied
- At: `docs/daemon/prior-table-pair-review.md` ## B. The C2 row-pairs, line 38 ("each task's demand spread over its lifetime") and the table's demand column, lines 42–43 ("35.77 / 1.53", "28.53 / 1.97")
- Change: Add the caveat that in `c2-p1a` and `c2-p2a` the batch job outlives the file, so the static estimate counts the job's whole `total_work` (1,389.885 s and 727.170 s) inside the second segment (39.435 s and 26.385 s): 35.77 and 28.53 are not a lane count of contention.
- Final word: 9.14 decision 4 (the demand window retires as a gate; demand per segment in the manifest, 2026-10-09): the static demand record (`dataset/tools/wlc/estimate.py`) spreads each task's demand over its arrival to its depart or the file's end; a batch job that outlives its file has its whole `total_work` counted inside the file — `c2-p1a` 14.505 (segment 1: 35.7721), `c2-p2a` and `c2-p2a-idle` 9.3829 (segment 1: 28.5251) in `dataset/build.manifest.json`.
- Sources: SX-0809 (record-gaps §2 item 5, `jioh/2026-10-14-record-gaps-and-doc-staleness-for-9.15.md:30`)
- Notes: Verified at HEAD in `dataset/build.manifest.json` `demand`: segment 1 of `c2-p1a` 35.7721 (60–99.435 s), `c2-p1b` 1.5272, `c2-p2a` 28.5251 (60–86.385 s), `c2-p2b` 1.9651, `c2-p3a` 0.4515, `c2-p3b` 1.0122; `total_work` at `dataset/timelines/coreset/c2-p1a.timeline.yaml:23` (1389.885 s) and `c2-p2a.timeline.yaml:29` (727.170 s). The dataset guidebook states the caveat (`docs/guidebook/dataset/04-the-coreset.md:384`); the TODO 9.15 line's 2026-10-11 audit segment asks for the same ("scoped in a sentence or clipped"). Record status: revision-note form as in W-0459.

### W-0461 · applied
- At: `docs/daemon/prior-table-pair-review.md` the C7 counterpart table's mail row, line 54 ("the base's 33 keystrokes"); ## Findings, item 8 "`c7-mail`'s slice holds no keystroke", line 80 ("33 input wakes on the rebuilt file")
- Change: Restate both counts to 35: `c1-mail`'s 35 input wakes fall between 45.9 s and 53.1 s, past the 26.385 s cut.
- Final word: 9.14 D6 (`c7-mail` reporting-only, 2026-10-09, 인지오's option A of three, amending the 9.14 spec's decision 2): `c7-mail` is `c1-mail`'s first 26.385 s and its mailer has no input-channel wake — `c1-mail`'s 35 keystrokes all fall between 45.9 s and 53.1 s; `c7-mail` is reporting-only, its term reading the mailer's own wakes (`channel: timer`) with no `base`; the mail pair's attribute is unmeasured. Still true after 9.18 made a counterpart's keystrokes its base's over the slice (the base holds none in its first 26.385 s).
- Sources: SX-0269 (TODO 9.15 line (from 9.14 D6), `_dev/TODO.md:179`)
- Cross-ref: W-0463
- Resolved at merge: The raw row read the target as already applied; the target's mechanism is current (row W-0463) but its count is not. `dataset/build/coreset-single/c1-mail.workload.json` (SHA-256 `4363abe5…`, equal to `dataset/build.manifest.json`'s entry) carries 35 `input:mailer` wakes, the first at 45,936,397 µs and the last at 53,065,597 µs (beside 5,371 `timer:mailer`), as 9.14 D6 and record-gaps §2 item 13 say. The doc's 33 is 9.18's sanity count made with the 9.17 build's compiler before the rebuild (`_dev/research/jioh/task-9.18-compiler-schema-and-build-gate/changelog.md:9`). The data wins.
- Notes: Record status: revision-note form as in W-0459. The dataset guidebook says 35 (`docs/guidebook/dataset/04-the-coreset.md:232`, `:1701`).

### W-0462 · applied
- At: `docs/daemon/prior-table-pair-review.md` ## Findings, item 4 "All 32 cells are instanced (Phase 7)", line 76 ("Of the 66 segments on the grid … 18 are `false`, so an always-`true` answer scores about 73 percent"; "Five segments are pre-committed misses on the attribute side")
- Change: Restate to 67 segments on the grid file (66 on cells, `c6-dual`'s ambiguous segment outside), 19 of them `false`, so an always-`true` answer scores about 72 percent by segment count; and say eight segments are pre-committed misses, one per cell — the five on the attribute side and three in C6, the resolution-limit group (`c6-alias` whole on media/`true`, `c6-fold`'s meeting segment from 30 s on meeting/`true`, `c6-spoof`'s second segment from 20 s on browsing/`false`).
- Final word: 9.23 D1 and D2 with D10's rebuild (C6's limit segments marked; `c6-spoof` split at 20 s, 2026-10-14): the coverage grid holds 67 segments (66 on cells, `c6-dual` outside), 19 on `false` cells; browsing/`false` gains `c6-spoof`'s second segment and meeting/`true` `c6-fold`'s; eight cells carry one pre-committed-miss segment each — five on the attribute side (`indexing/true`; `ml-train`, `render`, `transcode`, `backup` `false`) and three in C6 (browsing/`false`, meeting/`true`, media/`true`).
- Sources: SX-0598 (9.23 D10, `task-9.23-guidebook-findings/changelog.md:97`)
- Notes: Counted at HEAD from `dataset/coverage-grid.json`: `segments_total` 67; on cells 47 `true`, 19 `false`; outside 1 (`c6-dual`, mode ambiguous); `pre_committed_miss` 1 on each of the eight cells named; per_file: `c6-alias` media/`true`, `c6-fold` browsing/`true` then meeting/`true`, `c6-spoof` browsing/`true` then browsing/`false`. 48/67 = 71.6 % counts the outside segment with the non-`false` ones, as the text's old 48/66 = 73 % did; 47/66 = 71.2 % over the cells alone. Not named by 9.23's hand-off. Record status: revision-note form as in W-0459.

## Also on this file, not for editing from this list

- W-0463 · closed, already-applied — Line 80 (finding 8) says the counterpart's window, 2 s to 24.385 s, is a slice of `c1-mail`'s 2–58 s window at the base's stimulus offset (9.18 spec, decisions…
- W-0464 · closed, already-applied — Line 42 already says "the measured PyTorch example" with no desktop-frequency claim.
