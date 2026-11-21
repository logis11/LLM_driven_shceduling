# K6 · Research docs — review

Reviewed: `git diff -- docs/research-claims.md docs/research-proposal.md docs/terminology.md docs/background-guide.md docs/related-work.md` against `rows/g5-research-guidebook-and-claims.md` (g5-28 – g5-43), the work list (R1–R7, Q1–Q7, Rows by file), the editor brief and `logs/K6.md`.

**FINDINGS — 1**

## Findings

### 1. `docs/research-claims.md:91–93`, g5-28: the link 2 post hoc reading has no "not a verdict" label

- **What is wrong.** The passage gives two post hoc readings. Link 1's reading is labelled: "the post hoc reading gives 4 of 19, not a verdict" (line 77). Link 2's is not: "the post hoc reading of the run's scores, a term whose oracle is worse than `fixed` by the floor or more read as no headroom, gives 12 of 19 (2026-11-18)." The sentence sits right after "and link 2 stands". Without the label, a reader cannot tell whether 12 of 19 is a second reading of link 2 or only the post hoc count. The record labels the whole of that reading as not a verdict.
- **Record.** `docs/rq0-run-record.md`, Corrections, 2026-11-18, line 121: "**The post hoc reading**, not a verdict", which includes "**12 of 19** have headroom" (line 124). `harness/CHANGELOG.md`, 2026-11-18, says a post hoc report is rendered as "the reading's count, never as a verdict".
- **Fix.** Add the label, as link 1's sentence has it. For example: "…read as no headroom, gives 12 of 19, not a verdict (2026-11-18)." Nothing else in the sentence changes.

## Checked and in order

- **Coverage.**
  - Applied: g5-28, g5-29, g5-32 (its overtaken clause only), g5-33, g5-34, g5-35, g5-40 (its overtaken clause only), g5-41, g5-42 and g5-43.
  - Left, with their passages untouched: g5-30 (Q3), g5-31 (D), g5-36 (D), g5-37 and g5-38 (Q3), and g5-39 (Q4). `docs/terminology.md` has no diff, and its header is unchanged.
- **Scope.** Each hunk maps to one row. The only other changes are the four header lines, each set to `Updated 2026-11-21`.
- **g5-28, the link 1 and link 2 passage, checked word for word against `docs/rq0-run-record.md`.**
  - **The verdict as run is kept as the run's own.** The passage reads "stands as run: fail, 6 of the 19 … g = 0.5 against K = 10, and provisional", and the contingency "fired". This matches "The outcome" and the 2026-11-18 correction ("The verdict above stands as run: fail, 6 of 19, provisional"). It also matches decision 2 of the Phase 11 spec.
  - **The ranges are labelled "As run".** g goes from 10 at 0.25 to 4 at 0.67, pass at 0.25 and fail above. The ranges are boot-default sweep 3–9, floor band 4–6, cap band 6–7, venue factor 5–7, first segment's length 6–7 and carried half-widths 5–6. The chain scale and the sweep's 100 ms point are not read. Every count matches the table in "The reporting lines".
  - **No g band or line range is given for the final verdict.** The record gives none.
  - **The final verdict matches the 2026-11-21 correction.** The passage names `cpu-batch`'s `python3`, 107 repeats and the campaign `meas-ci:background:2026-11-20`. It says the entry was folded in by a changelog entry and a second bless. It gives the result as "final in place of provisional (2026-11-21): fail, 5 of the 19 … against K = 10", on the re-measured library and the run's programs. The record's sources are "The finding", "The campaign", "The closing" and the verdict line.
  - **The post hoc 4 of 19 is labelled "not a verdict".** It is read on the fixed programs: the scorer with its sign and `simulator@841dc81131cb`. This matches the 2026-11-21 "post hoc reading at the re-measured value" (4 of 19), which is also the count of the 2026-11-18 and 2026-11-20 readings. The 2026-11-20 correction, the fork-slot wait, enters only through the fixed simulator's version, as the post hoc reading's programs. That is true.
  - **The route matches "The failure procedure", 2026-11-21.** The passage says "the prior driver table is rewritten". It says 8 of 10 files have spread the prior table missed (finding 3), and `c7-transcode` and `c7-gaming` have spread the row holds (finding 2).
  - **Phase 12 is described only as far as decision 1 of the Phase 11 spec goes.** That decision names three things for Phase 12: the route's fix, the second RQ0 gate spec pinned before its run, and the second RQ0 run with its new verdict. The passage names the same three, says "come next", and cites the spec by path. Nothing beyond that is said.
  - **Link 2.** "17 of 19 … and link 2 stands" is stated "as run". The 12 of 19 matches the 2026-11-18 correction and decision 2 of the Phase 11 spec ("on the RQ0 run's scores … 12 of 19 have headroom"). The rule "by the floor or more" is the record's own wording. The missing label is finding 1.
  - **"If link 1 fails, no model recovers the paper" is kept.** This follows the row's flag b, which leaves it to 인지오.
- **g5-29, g5-34, g5-41 and g5-43.** Each gives 55.27 s ±5.89 %, or 55.27 s alone in the background guide. This matches the 2026-11-21 campaign table in the run record and `dataset/archetypes.yaml` line 1272.
- **g5-32 and g5-35.** They match the statement `failure-procedure` in `harness/experiments/rq0-gate.yaml` (lines 634–643): the search comes before any workload change, no spread found means workload redesign, and spread the prior table missed means the table is rewritten. g5-32 adds no outcome (Q3).
- **g5-33.** It matches `harness/CHANGELOG.md` for 2026-11-01: the cap band over three tables, each moving every unwanted row's cap to 0.2, 0.333 or 0.5, and the new headroom-count line for link 2. "last re-pinned 2026-11-14" is correct. The entries of 2026-11-15 say "no pin moves". The entries of 2026-11-18, 2026-11-20 and 2026-11-21 do not edit the spec. The pins comment at `rq0-gate.yaml:652` names 2026-11-14 as the latest re-pin.
- **g5-40.** "will run" becomes "ran", with the run's dates from "The run": started 2026-11-16T08:57:02, finished 2026-11-18T06:23:03. The dates say when the run happened, not what it found, so the sentence still adds no outcome (Q3). "The experiment is dead …" stays.
- **g5-42.** Checked against `dataset/build/coreset-single/c2-p1a.workload.json`. Its SHA-256 is `0678efa6…b317c`, the same as its entry in `dataset/build.manifest.json`. In the file:
  - `archetypes.yaml@a25178d113f0…`, which is `dataset/archetypes.yaml`'s blob at HEAD; that file has no uncommitted changes.
  - The hog's lines RUN 191 and SLEEP 472, its RUNs summing to 1,389.885 s, and `EXIT`.
  - Seed 201, and `derived_from` `@a0effee…`.
  - The editor's 11,293 wakes: 10,740 timer, 525 input and 28 event. The first timer wake is at 2,470 and the first input wake at 2,090,485.
- **Form.**
  - English prose in each doc's own register, with no new section and no sentence about the sweep.
  - Citing a `_dev/` path in the claims doc follows existing use: the doc already cites `_dev/archive/…` at line 212.
  - The claims doc's "Phase 1's committed spec" uses the phase numbering of Part 9 of the proposal. "Phase 12" uses the TODO's phase numbering. Part 9 runs from Phase 0 to Phase 7, so the two cannot collide, and the spec path the passage cites tells the reader which one is meant.

## Main session, 2026-11-21

The finding applied at `docs/research-claims.md:93`: "gives 12 of 19, not a verdict (2026-11-18)".
