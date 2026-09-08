# Repeat samples for the daemon — what run-to-run consistency needs from the recognition log

> Status: memo · Created 2026-09-07 · Updated 2026-09-07
> From 인지오 to 박이안. Written at the end of the Phase 5 spec session, where the metric definitions were fixed. One item concerns the daemon. It is not urgent for your Phase 1 milestone (`fixed`/`random`/`oracle` through the validator), but it shapes how the LLM-facing record mode should be designed, so it is better known now than discovered at integration.

## 1. The metric, in plain terms

RQ1 asks whether a model can read the situation from process names. One of its reported numbers is **run-to-run consistency**: given the *identical* telemetry snapshot, does the model give the same answer every time? The proposal says why this matters (§5.4): a component that answers differently on identical input is not deployable at any accuracy, and a single good answer means nothing on its own.

The harness computes it the same way it computes everything else about recognition: one row per graded query point (each `queries[]` entry in the recognition log that a non-`ambiguous` ground-truth segment covers), with whether the mode was right, whether `background_wanted` was right, what the validator did, and how long the answer took. Accuracy is the average of those rows. Consistency is the *spread* of those rows across several independent samples of the same query point.

## 2. What the log can and cannot express today

The recognition log envelope (`data-contracts.md` §8) is one file per workload × condition, with one entry per query point. That is exactly right for accuracy. For consistency it is one sample short: there is no place in the envelope to say "this is the third of five independent answers to the same snapshot".

Two things follow.

**The record/replay cache collapses samples.** Record mode stores `(prompt hash → response, measured latency)` and replay serves from it (proposal §4.8, `daemon-guide` §7). If record mode queries the model once per distinct snapshot, every replay of that snapshot returns the one stored answer, and consistency is 100% by construction — a measurement of the cache, not of the model. To measure consistency, record mode has to draw the model N times for the same snapshot and keep all N.

**The harness needs to know which sample it is reading.** With N samples per query point, the harness needs a repeat index to group them. It does not care where the index lives.

## 3. What the harness will accept

Either of these works, and it is your design call:

- **N log files per workload × condition**, each a complete log in today's envelope, with the repeat index in the file name or in a top-level field such as `repeat`.
- **One log file** with a top-level `repeat` field per file, produced by running the daemon N times against N distinct record-mode samples.

What the harness will *not* do is guess: if a log carries no repeat index, it is treated as sample 0 of 1, and consistency is simply not computed for that condition. Nothing else about the log changes: `proposal.system`, `validation`, `latency_us`, `t_set_change`, and the embedded `telemetry` snapshot are read exactly as the contract says. The non-LLM conditions are unaffected, because `fixed`, `oracle`, and `whitelist` are deterministic and `random` already carries its `seed` at the top level (its "repeats" are seeds).

## 4. Two things worth deciding together with this

- **Latency per sample.** Each sample has its own measured latency at record time. If several samples are kept, each should keep its own `latency_us`, not an average; the harness reports latency distributions, not means.
- **The two caches stay separate.** The archive's Q7 record distinguishes the record/replay cache (the instrument; on during measurement) from the deployment cache keyed on the canonical set (off during measurement). Drawing N samples belongs to the first; nothing here touches the second.

## 5. Not in this memo

The oracle's behaviour on `c6-dual`'s off-menu labels (the no-crash contract in `daemon-guide`) is unchanged and still deferred. The algorithm-choice accuracy metric for `llm_algo` (proposal §4.6) is computed by the harness from the log's `proposal.subsystems.cpu_scheduler.algorithm` against the calibrated driver table's default for the true row; it needs nothing from the daemon beyond what the log already carries.

When you settle the repeat index, a one-line addition to `data-contracts.md` §8 plus a changelog entry is enough; the harness's log reader will follow it. The full session record is `_dev/archive/2026-09-07-phase-5-primitive-metrics.md`.
