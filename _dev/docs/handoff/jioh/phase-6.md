# Handoff — start of Phase 6, carrying Phase 5's metrics and records decisions

Written 2026-09-08 at the end of the Phase 5 session. For a fresh session that will pick up **Phase 6 — Driver table v0 and the scoring spec** in `_dev/TODO.md` (인지오's section). Repo: `LLM_driven_shceduling`.

## Where things stand

- **Branch**: Phase 5 was done on `jioh/primitive-metrics` (the user's call — `_dev/` edits went there, not `main`). **Nothing is pushed and no PR is open at handoff time.** Check `git log main..jioh/primitive-metrics` and GitHub before branching for Phase 6. If the branch has been merged, start Phase 6 from `main`; if not, ask the user which base to use and whether to open the PR first (Phase 4's precedent: PR against `main`, merged by the user).
- **Phase 5 is `[done]`** (all four sub-tasks ticked). Phase 6 is fresh: no spec, no `[WIP]`. `daily-work-harness:pick-up-task` routes it to the spec track: grill → `grill-to-spec` → inline `6.M` sub-tasks.
- **Records to read first** (do not re-derive):
  - Phase 5 archive, one document for the whole phase: `_dev/archive/2026-09-07-phase-5-primitive-metrics.md`
  - Phase 5 spec: `_dev/docs/spec/jioh/phase-5-primitive-metrics-and-records.md`
  - **The metrics doc** — normative, the one Phase 6 builds on: `docs/harness/metrics.md` (§8 aggregates, §9 normalisation and floors, §10 constants are the parts the scoring spec consumes)
  - Phase 4 archive and spec (the driver-table contract Phase 6 fills): `_dev/archive/2026-09-07-phase-4-driver-table-format.md`, `_dev/docs/spec/jioh/phase-4-driver-table-format.md`; the contract itself: `docs/data-contracts.md` §10; the schema and lint: `daemon/driver-table/schema/driver-table.schema.json`, `daemon/tools/drivertable/`
  - The working plan Phase 6 implements: `_dev/docs/rq0-preparation-notes.md` Stage 3 (§9 items 3.1–3.5) and §6 (per-file metric inventory, the three places a real decision is required, the files with no Layer-2 information)
  - Study guides (Korean, the user's own, draft): `docs/workload/coreset-guide.md` (every coreset file with its compiled numbers), `docs/harness/harness-and-records-guide.md` (records and what sits on top of them)

## What Phase 6 must do (from the tracker)

Stage 3. Scope the rows C1–C4 exercise; write the prior table (v0) with one-sentence justifications; the scoring spec (C2 pair weighting, `c1-compile`'s trade-off, `c1-media`'s audio/video weighting); fill the remaining rows with defaults; pair review of same-mode `wanted=true/false` rows for distinctness. Two artifacts feed back into each other — expect to alternate.

## Phase 5 decisions Phase 6 must carry (details in the archive and the metrics doc)

1. **What the scoring spec operates on.** Records are raw observations — one CSV row per observation with an anchor time `t`, an `entity`, a `metric`, a `value`, and per-metric attributes — never aggregates. The scoring spec therefore names, per file: which **entity** (a task id from the trace, or `lane`/`schedule`), which **primitive** (`ready_wait`, `job`, `cpu_delivered`, `demand`, `completed`, `turnaround`, `preempt_count`, `config_interval`, `busy`), which **filter** (`cause = wake` for keystrokes; a time window on `t`), which **aggregate** from the fixed list (§8: count, mean, P50, P95, P99, max, `over_threshold` for `ready_wait`; count, miss rate, latency P50/P99 for `job`; progress = `cpu_delivered / demand`; …), a **direction**, and a **weight**. The named entities are task ids as compiled: `editor`, `hog`, `writer`, `game.chain.1` (the chain head is the entity of `job` rows), `video`, `music`, `build`, `build.cN`. Read them from `dataset/build/coreset-single/*.workload.json` or the coreset guide; do not guess.
2. **Normalisation is per aggregate**, `(fixed − condition)/(fixed − oracle)` with the sign following the aggregate's direction, applied before weights; each aggregate has an absolute floor in its own units (1 000 µs latency-type, 0.01 fractions — stated assumptions) below which the share is undefined and raw values are reported as "no headroom". Weights combine unit-free shares. The floors may be revised by the gate spec with a changelog entry in the metrics doc.
3. **Windows are a scoring-time filter on `t`**, never a primitive. `c2-p1a`'s interesting stretch is 60–180 s (the dev-only first minute dilutes a whole-file P95). The primitives never read `ground_truth`.
4. **The judging set's batch tasks cannot finish inside their files** (verified from compiled RUN totals: `c2-p1a` hog 130 s in 120 s, `c2-p3a` ffmpeg 75 s in 60 s, `c2-p2a` download needs 42% of the lane). "Batch progress" is `cpu_delivered / demand`, not turnaround. The C3 batch/build tasks cannot finish either (coreset guide §12).
5. **Frame latency for the game chain is reconstructed by the harness** — `job` rows sit on the chain head (`game.chain.1`), value = tail iteration end − tick; the simulator's `deadline` line for the head is *not* frame latency. `c2-p2a/b` have no compositor, so the pair's frame metric rests on the chain. Miss = `value > period_us`.
6. **`T_interaction` = 100 ms** (Miller 1968; Nielsen 1993) is the `over_threshold` constant for interaction latency and one *input* to the `c1-media` audio/video weighting question — not its answer. Shneiderman 1984 (reporting Long 1976) says 0.1–0.5 s echo delays already hurt typists, so 100 ms is the loose end. Card et al. 1991 was dropped as unreadable; do not cite it.
7. **Familiarity tier** is carried through compilation into `ground_truth` (only where authored: the three C5 files) and onto recognition records rows; it is a split key for reporting, never a Layer-2 input. Whether `c1-media` gets a tier-1 annotation is open.
8. **Files with no Layer-2 information** (notes §6): C5 (identical to `c1-media` but for names; a differing Layer-2 number is a bug signal), `c1-idle` (no performance metric), C6 (diagnostic), C4 (meaningful as a delta against its C1 base). Declare exclusions in advance.
9. **Driver-table facts** (Phase 4, frozen): rows keyed `(mode, background_wanted)`, 32; per-row `batch_bandwidth_cap` and `default`; the **prior table** has exactly one entry per row, `basis: theory`, a justification sentence on every row; the lint fails a same-mode `wanted=true/false` pair whose default configurations are byte-identical ("far enough apart" is Phase 6's pair review); LOTTERY `batch_share ≤ cap`; `daemon/tools/drivertable/config_schema.py` is the machine copy of the config schema (16 modes, per-algorithm fields with ranges and defaults). `make -C daemon lint` reports "nothing to lint" until the table lands in `daemon/driver-table/`.
10. **Boot default = seven stated assumptions** (recognition-vocabulary §2); the `fixed` floor rests on it; the sensitivity pair is pre-registered for Phase 7's gate spec.

## What exists in code now

- `harness/` — Python package `tools/harness/` (`reader.py`, `primitives.py`, `records.py`), CLI `tools/records.py` (one run-file + trace pair → one records CSV; guard messages on stderr, exit 2 when any fired), machine schema `records/schema/records.schema.json`, fixtures `tools/tests/fixtures/{mock-office,mock-media,mock-p1a,mock-chain}/` each with `run.json`, `trace.jsonl`, `expected.csv`, `worked.md`. `make -C harness lint|test` (43 tests). CI: `.github/workflows/harness.yml`.
- The harness assumes three simulator behaviours sent to 인경민 as a memo (`docs/memos/2026-09-07-trace-clarifications-for-the-simulator.md`): a `ready` line at every blocking-primitive completion (zero wait if it did not block), wakes queued with depth, a written tie-break; plus TIMER `t₀` = arrival (metrics doc §11 item 4 — the `job` primitive's tick grid depends on it). No reply yet at handoff time.
- Dataset: compiled `ground_truth` segments may carry `familiarity`; the three C5 artifacts' hashes changed on 2026-09-08 (`dataset/build.manifest.json`); 52 dataset tests, `make -C dataset check` verified.

## Open items carried forward (not Phase 6's, but don't lose them)

- Memo replies: 인경민 on the trace clarifications and §9.1/§9.2; 박이안 on the repeat index for run-to-run consistency (`docs/memos/2026-09-07-repeat-samples-for-the-daemon.md`).
- Proposal §8.2's three signatures on metric definitions vs 인지오 deciding (the metrics doc is normative already).
- C1-derived files' inherited `demand: calibration` (Phase 3 archive); C6 mixed demand classes need a paper footnote.
- The word "familiarity" (the user finds it vague; a rename would touch ratified docs — a Phase 7 sweep candidate).
- Gate spec (Phase 7): threshold; `random` draw definition + seed count (with 박이안); boot-default sensitivity pair; `c1-gaming` separate reporting line; guard exemptions; full guard-list audit; L1 grader.
- "Config search before workload redesign" failure procedure (notes §4.3) still needs team agreement.
- Proposal and related-work remain `draft`; the two Korean study guides are `draft` and the user's own.

## How the user works (observed across Phases 4–5, follow it)

- **One question per message** in grills; plain chat, never AskUserQuestion. Number as ❓ **Qn** with a ➡️ recommendation. They answer "(A)" style and sometimes restate the decision in their own words — record those words verbatim in the archive.
- **Condition names always** (`llm_vocab`, `llm_algo`, `llm_full`), never bare A/B/C.
- **Straight to implementation, no plan doc, no worktree; TDD** — write the failing test first, show it failing, then implement. They check.
- **Don't invent.** Nothing goes into code or docs that is not a field or rule in the contracts or the metrics doc; when a convenience field was added (a `spawned` flag) it was removed on review. Nothing gets a name the docs don't already use.
- **Sources**: never an unverified citation; if a primary source cannot be read, drop it rather than carry a marked entry. PDFs: `pypdf` in the scratchpad venv (`pdftoppm` is not installed; the Read tool cannot render PDFs).
- **Archive once per phase**, at phase end, one document — not per sub-task. Docs: no chat-derived justification in normative docs; bump `Updated`; update stale docs immediately ("there's no reason not to change"), including their own study guides.
- Presents review points one at a time after a sub-task; expects each acted on and recorded in the archive at phase end. Says "wrap up" to close.
- Wants member-facing notes (memos to 인경민/박이안) **detailed, descriptive, and in easy terms**, with worked examples.

## Environment notes

- Python deps are not installed system-wide. Create a venv in the session scratchpad and `pip install -r dataset/tools/requirements.txt -r daemon/tools/requirements.txt -r harness/tools/requirements.txt pypdf`. The scratchpad is session-specific; recreate the venv each session.
- `make -C dataset lint|test|check|dataset`, `make -C daemon lint|test`, `make -C harness lint|test` — pass `PY=<venv>/bin/python`.
- ACM DL returns 403 to the fetch tool; web.archive.org is blocked; DuckDuckGo/Bing searches are unusable. OpenAlex and Crossref APIs work for coordinates; scanned PDFs on other hosts often carry an OCR text layer.

## Suggested skills

- `daily-work-harness:pick-up-task` — start Phase 6 (spec track).
- `grilling` — the Phase 6 spec session (row scope; prior-table authorship rules; the scoring spec's shape over records; the three §6 decisions; pair review).
- `daily-work-harness:grill-to-spec` — write `_dev/docs/spec/jioh/phase-6-*.md` and inline sub-tasks.
- `superpowers:test-driven-development` — for any code (scoring-spec lint, table authorship checks).
- `daily-work-harness:wrap-up` — end of each sub-task; archive at phase end only.
