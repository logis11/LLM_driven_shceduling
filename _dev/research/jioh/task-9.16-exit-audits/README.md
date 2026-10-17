# Task 9.16 — exit audits

The claim, measurement and compiled-number audits re-run on the final repository state, and their findings fixed (spec `_dev/docs/spec/jioh/task-9.16-exit-audits.md`). 인지오's answers: `decisions.md` (D1–D6, and the items taken under the spec).

## What ran and what it found

| Audit | Records | Result |
|---|---|---|
| Claim audit, the dataset side (spec decision 1) | `claims/dataset-inventory.md`, `dataset-findings.md`, `dataset-blind-topics.md` | 221 claims: 164 traced, 19 wording outside the passage, 15 record below the standard, 4 no record, 19 labelled |
| Claim audit, outside the dataset | `claims/outside-inventory.md`, `outside-findings.md`, `outside-blind-topics.md` | 353 claims: 270 traced, 41 wording outside, 23 record below the standard, 11 no record, 8 labelled |
| Blind re-reads (the sample of decision 1, plus the sources whose only passage sat in `docs/references.md`, `claims/extra-blind-topics.md`) | `reads/B1`–`B4` `-reads.md` (written before comparison) and `-compare.md` | 188 claims compared: 131 supported, 41 wording fixes, 3 contradicted, 4 not in source, 9 unverifiable (the CpsMark+ full text, Field & Welsh 2007 and three clauses unreachable; their earlier records stand) |
| Measurement audit, reproduction (decision 2) | `meas/repro-table.md`, `repro-findings.md` | 60 rows; every value reproduces from its release after the data chunk, the session within-run spreads from the release D5 published |
| Measurement audit, class read | `meas/class-table.md`, `class-repeat-counts.md`, `class-findings.md` | 304 values: 300 measured, 4 derived, 0 convention; every 2026-09-13 mismatch item resolved |
| 9.15's two computations (decision 3) | `meas-new/burstiness.md`, `stability-ledger.md` | burstiness re-run on `renderer-hidden` and `video-editor`'s idle pool; the ledger (406 values, 369 met the tolerance, 37 carried under an exception class, 0 unresolved) in `dataset/tools/meas/stability_ledger.py` |
| Compiled-number audit (decision 5) | `compiled/report.md`, `findings.md` | 88 hold, 45 stale, 3 wrong findings (the `tick_count` guard on `c7-gaming`, `c2-p3b`'s backup, the batch-class memo's example) |
| Handed-over checks (decision 3) | `handed/checks.md`, `findings.md` | 6 pass, 3 fail (the sweep's quantile labels, the `systemd-oomd` tag, `game-task-chain`'s class label); the intermediate pins closed by the gate |
| Dataset gate and CI | `gate/` | home gate 372 s at `2b080333`; CI 39014790007 green (9.15's last state) and 39030123144 green on `17f28d7f` (about 17 min) |

## Fixes, in order

- `3fbb7c25` — H1, the harness (`logs/H1.md`): the `tick_count` guard by the window rule (D3), guard spec 1.2; `c2-p3b`'s turnaround (D4); the sweep's figures and `c7-meeting`'s reason (D1); scoring spec, guard spec and driver table re-pinned.
- `17f28d7f` — D, code and data (`logs/D.md`): the measurement tools, the regenerated records (the 9.8 control on its own phase, D6), the library and sources text, `parallelism_cap` as convention; the one rebuild (dataset `8e1eb753…`, variants `8e2948b1…`); release `meas-ci-probes-2026-09-23` (D5).
- `1a092508` — the docs (`logs/W.md`, `P.md`, `R.md`, `G.md`, `F.md`), one combined review.

## Statements waiting on the simulator

`compiled/uncheckable-by-item.md` lists them by the RQ0 gate spec's conformance item: (b) the TIMER skip rule, (d) `batch_bandwidth_cap` as a work-conserving ceiling, (e) the strict idle class, (g) `WAIT children:<id>` completing when every child it spawned has ended. Each now names its item in its document (H1, P); the list is the check 인경민 runs once each item lands (spec decision 6).

## The full smoke (9.23 D15's hand-off)

`make -C harness smoke` on the final build, at `a4b6a9da` (the data as `17f28d7f` built it), started detached 2026-10-17 21:50 KST, ended 2026-10-18 02:22 KST: exit 0, 16,313 s (4 h 32 min). 392 invocations over the 49 scored core files, 142 executed and 250 from the cache earlier runs on the same inputs had filled, so the time is not a cold run; the cold figure stays 9.14 D14's 4 h 50 min. Verdict `invalid`, 0 of 49 judging files meeting the criterion — the mocks' verdict, `invalid` by construction (`harness/tools/smoke.py`'s docstring); the smoke checks the plumbing. Start, end and the log's tail: `gate/smoke-status.txt`.
