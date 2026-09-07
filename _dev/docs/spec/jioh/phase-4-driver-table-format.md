# Phase 4 — Driver table format

Stage 0.5 of `_dev/docs/rq0-preparation-notes.md`, as decided in the 2026-09-07 spec session. Parent: `_dev/TODO.md`, (jioh, 4). Work lands on `jioh/driver-table-v0`.

## Scope

- Ground the frozen config schema's default values (the boot default) in primary sources, or mark them as stated assumptions with a sensitivity check planned.
- Fix the driver table's format so the prior table and the calibrated table are instances of one schema; promote it to a data contract with a JSON schema and a lint.
- Freeze the proposal contract with the `llm_algo` read-scope rule.
- Correct the documents that describe the table and the `llm_algo` condition.

Out of scope: the prior table's content (Phase 6); the held-out-rows arm (recorded, deferred until after the main experiments).

## Locked decisions

### 1. `llm_algo` draws from the table

Every scored condition passes through the driver table; `llm_full` stays a subset diagnostic. `llm_algo` reads the situation and names the algorithm; the table supplies the configuration for that algorithm.

### 2. Row structure

The table is keyed by `(mode, background_wanted)`, 32 rows. A row holds: a `batch_bandwidth_cap` shared by all its entries; one `default` algorithm; one to four entries, one per algorithm, each carrying that algorithm's `params`, a `basis` of `theory` / `schema-default` / `tuned`, and a one-sentence justification. `system`-only conditions receive the default entry; `llm_algo` receives the entry for the algorithm it named.

### 3. Prior table and calibrated table

`v0` is the **prior table**: written from theory before any measurement, exactly one entry per row (`basis: theory`), used for the RQ0 gate and as the baseline of RQ5's fragility check. `v1` is the **calibrated table**: tuned on the disjoint throwaway pool, lint-required to carry all four entries per row, used for every reported result. The names replace v0/v1 everywhere.

### 4. Missing-entry rule

When `llm_algo` names an algorithm the row has no entry for, the mapper composes the configuration from the schema defaults for that algorithm with the row's cap. Nothing is rejected on this path. `llm_algo` runs on the calibrated table only, so the rule is not exercised on the prior table.

### 5. The delegation rung

`llm_algo` versus `llm_vocab` cannot show a gain against a calibrated default when the situation reading is correct. The rung is scored as: algorithm-choice accuracy against the calibrated table's default (a Layer-1 style metric, no simulator); the cost of delegation as a non-inferiority number; and, deferred, delegation under vocabulary gaps. The proposal states this rather than the previous "improvement stops around B".

### 6. Read scope before validation

The condition's read scope is applied first; the validator's rules run on the composed configuration, which is what the simulator receives. Under `llm_algo` the proposal's `cpu_scheduler` block is `{algorithm}`; anything else in it is unread and logged. `llm_full` is the only condition whose raw block is validated as such. The proposal contract freezes with this rule.

### 7. Placement

The table lives in the daemon tree as YAML, two files named by role, with a JSON schema and a lint beside them, run in CI. Ownership is stated in that tree's README.

### 8. Lint scope

Structure and legality: 32 rows; exactly one default naming a present entry; each entry's `params` exactly the algorithm's fields, in range; cap in range; LOTTERY `batch_share ≤ cap`; `basis` from the enum; a justification on every row; the calibrated table full. Plus one distinctness check: a same-mode `wanted=true` / `wanted=false` pair whose default configurations are byte-identical fails. "Far enough apart" stays with Phase 6's pair review.

### 9. Boot default grounding

The schema's per-field defaults have no source. Each is traced to a primary source with a `docs/references.md` entry, or marked an unverified stated assumption with the sensitivity check (run `fixed` under alternative boot defaults) written down. Recorded in the vocabulary doc's changelog. Done first.

### 10. Documents corrected

`data-contracts` (new driver-table section, proposal contract frozen, changelog); `recognition-vocabulary` (variant row for `llm_algo`; grounding changelog); `research-proposal` §5.2, §4.6/RQ3, §8.2 decision 3; `daemon-guide` §5 (the mapper's actual steps; stale encoder example removed); `terminology` (row count, the two table names). Archive Q4's row shape is superseded by the frozen envelope, noted in this phase's archive.

## Open items

- Held-out-rows arm (blank rows to schema defaults, compare `llm_vocab` and `llm_algo` on the affected files): recorded in the proposal as a proposal, run after the main experiments. The format does not carry a "no default" field now.
