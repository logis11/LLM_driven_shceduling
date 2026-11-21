# K8 review — workload, contracts, daemon, dataset READMEs

**FINDINGS** — 2 in the docs, 1 in the editor's log; one missed passage outside the chunk.

Read: the task spec, the work list (R1–R7, Q1–Q7, the "Rows by file" table), `rows/g7-workload-contracts-simulator-daemon.md`, g0-15 – g0-17 in `rows/g0-index-memos-todo-plan.md`, `logs/K8.md`, the editor brief, and `git diff` of the eight files.

## Coverage and scope

All 27 rows due are applied (g7-01 – g7-14 but g7-15 and g7-16; g7-21 – g7-29; g7-31; g0-15 – g0-17). The rows to be left (g7-15, g7-16, g7-30) are untouched. Every hunk maps to a row, plus the `Updated 2026-11-21` headers. The overview's header already read 2026-11-21, and the two READMEs have no header.

## Records checked

- `docs/data-contracts.md` Example A matches `dataset/archetypes.yaml` lines 1257 and 1259 digit by digit. `python3_run`: `p` [14, 141, 155, 191, 1223, 20473778, 204750672, 334780629, 759669393, 1177733035], min 7, max 1297955204. `python3_block`: `p` [9, 71, 102, 330, 446, 521, 591, 629, 713, 799], min 1, max 1109. Both have source `meas-ci:background:2026-11-20`, and the `kdenlive_render` lines are unchanged.
- `dataset/build/coreset-single/c2-p1a.workload.json` has SHA-256 `0678efa68cef…`, which equals `dataset/build.manifest.json`'s pin. The hog program in it has RUN 48 and SLEEP 47. Its first values are RUN 191 and SLEEP 472, and its last is RUN 15491555 followed by EXIT. The RUN total is 1,389,885,000 µs, and the demand is 14.505 (35.7721 in segment 1). The coreset guide (lines 354, 440–441, 768, 772) and `dataset/README.md:88` agree with all of these.
- In the coreset guide, 55.27 s ±5.89 % over 107 repeats matches `archetypes.yaml` `validation_stats.stats` and `docs/rq0-run-record.md` (Corrections 2026-11-21, the campaign table). Line 5's three files and "no demand moves" match `harness/CHANGELOG.md` 2026-11-21, "The second bless".
- Measurement overview:
  - Line 73's 15.7 % matches `measurement-campaign-record.md:564` (680 jobs, 107 on the EPYC 7763). The 9.12 costs campaign (31.3 %) holds no archetype value, as overview line 167 says, so the lower bound is 11.3's.
  - Line 79's 107 matches the run record's 2026-11-21 "The campaign".
  - Line 9 matches `cpu-batch`'s `scope`.
  - Chapter 6 of the dataset guidebook, at lines 961 ("5 to 107") and 967 ("Over the campaigns behind the dataset's values, 15.7–83 % of a campaign's jobs drew it"), now quotes the overview word for word.
- `dataset/README.md` lines 30 and 128 are correct:
  - The pin `pins.variants.all` is `de9802e7…`. It was set by `db2fda65` (2026-10-31), the 2026-10-31 changelog's pin.
  - The committed manifest is `3438be7f…`, committed at `2e3fade3` (2026-11-21).
  - `harness/experiments/rq0-gate/runs.sha256.csv` is present, and the 2026-11-20 lint entry turns the pin into a note.
- Building-plan ladder: the integration gate's versions come from CHANGELOG 2026-11-14. The run's dates and the verdict, 5 of 19 against K = 10, come from the run record. The route is from "The failure procedure". Phase 12 is from the Phase 11 spec, decision 1.
- The coreset guide's conformance item (g), the `fix-object` and `fix-tree` fixtures and `test_spawn_children.py` match the RQ0 gate spec's `simulator-conformance` statement.
- The daemon guide's 19,425 runs with the schedule and log compared byte for byte match `_dev/research/jioh/task-10.2-integration-gate/README.md` line 9. Its hold-time sentence matches the Phase 11 spec, decision 10.

## Findings

1. **`docs/daemon/daemon-guide.md:145` and `:151`: `fixed` is said to pass through the validator and the mapper.**
   - **What is wrong.** Line 145 says "`daemon/daemon.py` runs `fixed`, `oracle` and `random` through the validator and the mapper and writes their config schedules". Line 151 says "*`daemon/daemon.py` emits these for `fixed`, `oracle` and `random`, through the config mapper (§5).*" Both are false for `fixed`.
   - **Records.**
     - `daemon/daemon.py` `run()` lines 289–290 return `fixed`'s one-entry schedule, the boot default with provenance `fallback`, before any query point. No `validate` or `compose` is called.
     - `recognize_fixed`'s docstring (lines 196–199) says "It never reaches here".
     - `daemon/README.md` line 36 describes `fixed` as "the boot default alone, one schedule entry, no query points".
     - The guide's own §4 table (line 105) says the same.
   - **Fix.** At 145: "… `daemon/daemon.py` runs `oracle` and `random` through the validator and the mapper and writes the config schedules of all three model-free conditions, `fixed`'s the boot default alone; …". At 151: "*`daemon/daemon.py` emits these for `fixed` (the boot default alone), `oracle` and `random` (through the config mapper, §5).*"
   - **For 인지오 (spec decision 11; logged, not resolved).** `daemon/README.md` line 59, "The validator seat exists and they pass through it", says the same of all three, and the code disagrees for `fixed`.
2. **`docs/daemon/daemon-guide.md:131`, minor: the §5 heading is overtaken by item 2, like the sentence g7-22 replaced.**
   - **What is wrong.** The heading reads "## 5. The driver table — 인지오's piece, and where the pipeline currently ends". Its last clause pointed at "until it is, the pipeline runs up to and including the validator", which g7-22 replaced. The section now says the pipeline runs through the mapper. Nothing in it says where the pipeline "currently ends", so the heading announces content the section no longer has.
   - **Record.** `daemon/README.md`, "`daemon.py` — the running skeleton".
   - **Fix.** Drop the clause ("## 5. The driver table — 인지오's piece"), or write "and where the pipeline stands". No link or anchor anywhere names the heading.
3. **`logs/K8.md:45` and `:70`, the note for 인지오: "no record shows `daemon.py` run under `names`" is wrong.**
   - **Records.**
     - `daemon/README.md` lines 62–64 say: "Verified (2026-10-20): byte-identical to the harness's reference mock … over 25 workloads × 3 conditions × 2 telemetry shapes, 150/150 — schedules and logs both".
     - `daemon/daemon.py`'s docstring (lines 36–38) says the check ran "over the core set under all three conditions and both telemetry shapes".
   - **What is actually open.** The milestone names all 51 core files. The README says 25 workloads, while the docstring says the core set, and that mismatch is for 인지오.
   - **Fix.** Restate the log's note to that. The doc edit stands: the milestone is left unmarked, and §8 is true as written.

## Outside this chunk (no row; for the main session)

- **`docs/references.md`, two citation roles that should be a new row.** Line 129, `chow-aoms65`'s role, says "a count of 5 to 77". Line 134, `cochran-st77`'s role, says "The campaigns' counts run 5 to 77, most below its 30".
  - Item 10 overtakes both, exactly as it did the overview's line 79 (g0-16). The record is 11.3's 107 repeats, `docs/rq0-run-record.md`, Corrections 2026-11-21, "The campaign"; the counts become "5 to 107".
  - g7 read `references.md` and listed no row. `references.md` is in no chunk, and the sweep's search terms do not match "5 to 77", so the second search will not find these lines.

## Notes, not findings

- `docs/workload/measurement-overview.md:97`, the ledger paragraph, still gives ±27.3 % as `python3`'s widest value. It is dated ("read 2026-10-17") and so is left under Q1's rule that dated passages stay. The second search will hit it on `python3`.
- `docs/daemon/daemon-guide.md:178` puts `(../rq0-run-record.md)` after the Phase 12 clause. The run record holds the verdict and the route but not Phase 12, which comes from the Phase 11 spec, decision 1. Nothing is false; the citation could sit after "rewritten".

## Main session, 2026-11-21

- F1 applied at `docs/daemon/daemon-guide.md:145` and `:151` as the review gives it: `fixed`'s schedule the boot default alone, `oracle` and `random` through the validator and the mapper (`daemon/daemon.py` lines 286–290).
- F2 applied: the §5 heading's clause dropped ("## 5. The driver table — 인지오's piece"); no link names the old heading.
- F3: the editor's note for 인지오 in `logs/K8.md` is superseded by the review's reading — `daemon/README.md` lines 62–64 record a `names` run (2026-10-20, 25 workloads × 3 conditions × 2 telemetry shapes); what is open is that the milestone names the 51 core files while the README says 25 workloads and `daemon.py`'s docstring says the core set. The milestone stays unmarked.
- The two `docs/references.md` lines are new rows g7-33 and g7-34, applied in this chunk; the doc's header set to Updated 2026-11-21.
- `daemon/README.md` line 59 ("they pass through it" of all three conditions) disagrees with `daemon.py` for `fixed` — 박이안's tree, outside the sweep, for 인지오.
