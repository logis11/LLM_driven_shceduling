# Phase 3 — Verification and protocol freeze

Stage 0 of `_dev/docs/rq0-preparation-notes.md`, as decided in the 2026-09-06 spec session. Parent: `_dev/TODO.md`, (jioh, 3).

## Scope

- Settle C1's demand class question by reading the per-file static demand estimates, and make those estimates a committed build artifact.
- Check `c6-dual`'s out-of-vocabulary labels (`mode: ambiguous`, `dual_active`) against oracle and validator behaviour; record the finding.
- Protocol freeze: harden the draft data contracts that do not depend on the driver-table format.
- Vocabulary and status sweep across `docs/`: fix lines that lag the vocabulary freeze or the contract freeze; list design divergences for Phase 4.

Out of scope: the variant-B corrections in `research-proposal` §5.2/§4.6 and `daemon-guide` §5, and the proposal contract's freeze — both belong to Phase 4.

## Locked decisions

### 1. Sweep scope

The sweep is a vocabulary and status audit bounded by the two freezes: grep every doc under `docs/` for the retired vocabulary (five-mode menu, `has_realtime_encoder`, `background_is_wanted`) and check every `> Status:` header and every per-contract `draft`/`frozen` label against what is settled.

### 2. Stale lines are fixed in this phase; design divergences are listed

Anything purely stale against a ratified freeze is corrected here: `terminology.md`'s five-mode paragraph and attribute list, the proposal's Part 9 Phase 1 milestone row ("modes only, no attributes"), the proposal's Part 5 tables that assign `interactive` as a mode value, and building-plan's C1 description, which names the calibration role but not the `demand: calibration` class the timelines declare. Anything whose correct text depends on the driver-table decision is listed in the session archive as Phase 4 input and left unedited.

### 3. Contracts frozen

Five contracts flip to `frozen`: run file, visible projection, telemetry, config schedule, recognition log. The proposal contract stays `draft`, carrying a one-line note that it hardens with the driver-table contract in Phase 4.

### 4. Frozen by ratified decision

The five freeze by ratified decision, following the config-schema and trace precedent. No schemas or enforcing code are written in this phase. The data-contracts glossary's definition of `frozen` is amended so that it reads: the format is fixed and changing it is a team decision; schema and CI enforcement follow when the consumer lands.

### 5. Changelog lives in data-contracts

A changelog section is added to `docs/data-contracts.md`, a dated entry list, with the protocol freeze as its first entry. Other docs touched by the sweep get their `Updated` date bumped only; the corrections are not contract changes and get no entry.

### 6. Demand estimate becomes a build artifact

The compiler writes each file's `utilization` and `demand_class` into `dataset/build.manifest.json`. The six C1 values and the resulting judging-set conclusion (6 files or 12) are recorded in the session archive for Phase 8's RQ0 gate spec to consume.

### 7. `c6-dual` finding gets a normative home

One sentence in `daemon-guide` where the oracle recognizer is specified: a segment whose ground-truth label is outside the recognizer's menu is undefined for the oracle and deferred past RQ0. The full finding goes to the session archive.

## Invariants

- `_dev/` edits stay on `main`; the manifest change is the phase's only code and runs in a worktree.
- Every doc edited bumps its `Updated` date in the same commit.
