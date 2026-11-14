# Task 10.3 — The variant lines read a failed guard

인지오's sub-task 10.3 in `_dev/TODO.md` (Phase 10, Integration and the RQ0 run), decided on 2026-11-14: a reporting line that reads a gap from a run with a failed non-exempt guard gives no reading. It carries the decision of 2026-11-13 that a variant's failed guard makes its line's count unavailable, as a boot default's and a band table's is (`simulator/memo/memo_261111.md` Part L, L3 decision 4), and lands before the cold smoke (the 10.4 spec's decision 8, `_dev/docs/spec/jioh/task-10.4-cold-smoke-and-cost-response.md`).

## Scope

- The evaluator's unavailable set (`harness/tools/harness/evaluator.py`), built today over the judging files alone.
- The lines that read a gap of a file outside the judging set: the eight `variant_set` lines, the trace replay line, the bounding pair line, and the report's gap table.
- The RQ0 gate spec's `sensitivity-lines` statement (`harness/experiments/rq0-gate.yaml`).
- The check: tests, and one reading on the cold smoke's report.
- One harness changelog entry.

Out of scope: the executor's starvation net; naming the runs that fail the starvation guard under `oracle` (the 10.4 spec's decision 16); any file under `docs/`.

## Locked decisions

### 1. The unavailable set is built over every listed file

The set is built over the judging, the reporting and the variant files, per file and boot default: a failed non-exempt guard on a run a gap reads marks that gap unavailable, whichever list its file is on. The verdict is invalid only on a judging file's failed run, as now.

### 2. A `variant_set` line whose count reads an unavailable gap gives no reading

The line's count is unavailable. The verdict stands on the primary count and is stated as not read over that axis, and the failed runs and their guards are named beside the line.

### 3. The trace replay and the bounding pair follow the same rule

A trace replay row with an unavailable gap on either side has no agreement, and the line's agreement over its four files is unavailable, the failed runs named. The bounding pair's difference is unavailable when either file's gap is.

### 4. What an unavailable line keeps

An unavailable `variant_set` line keeps the fields a boot default's row has: the met and judging numbers stay in the report, the verdict is blank, and the line is marked unavailable. A gap's value keeps printing with its mark, in the gap table and in every line that shows it.

### 5. The exemptions are unchanged

The RQ0 gate spec's guard exemptions apply to any listed file, as they do today. No exemption is added for the chain-scaled runs.

### 6. The statement carries the rule alone

The `sensitivity-lines` statement gains the rule and no run's name: a count, an agreement or a difference that reads a gap from a run with a failed non-exempt guard gives no reading, and the verdict is stated as not read over that axis. The four chain-scaled runs and `c3-evening` are named by the 10.4 spec's decision 16, once the smoke has confirmed them.

### 7. The rule is stated once, for every line that reads a gap

The sentence names the boot defaults' counts and the band tables' counts beside the variant lines, the trace replay and the bounding pair. For the first two it states what the evaluator already does; no evaluator behaviour changes for them.

### 8. The check is tests and one reading on the cold smoke

Tests hold the rule on the fixtures. After the cold smoke, the availability of every line in its report is recorded by the starvation script in the 10.4 research folder (`_dev/research/jioh/task-10.4-cold-smoke-and-cost-response/`). The expected result: the two chain-scale lines, `chain-x1.2` and `chain-x1.4`, are unavailable, naming the four chain-scaled `oracle` runs and the starvation guard, and no other line is.

### 9. The record

The harness changelog takes one entry. No pin moves.

## Invariants

- The verdict is invalid only on a judging file's failed run.
- No gap value, count or verdict of a run without a failed non-exempt guard changes.
