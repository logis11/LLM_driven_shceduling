# Handoff — task 10.4 The cold smoke and the cost response (2026-11-15) — the second rerun recorded, 10.4's work done

Spec `_dev/docs/spec/jioh/task-10.4-cold-smoke-and-cost-response.md` (decisions 1–21; 12 and 16 restated 2026-11-15). Research folder `_dev/research/jioh/task-10.4-cold-smoke-and-cost-response/`, its README the record. On `main`, not pushed: `df0b9348`, `a0cbe2d1`, `a3aadfe9`, `3d949345`, `5c434017`, `251eb50f`, `dd03f515`, and the second rerun's record.

## Where it stands

- **Smokes:** the first stopped at 1,151 runs (the cap band's schema check; the boost-window scan); the second finished its 1,197 runs, stopped in the guards stage; the rerun (`runs/smoke-rerun`, from `5c434017`) and the second rerun (`runs/smoke-rerun-2`, from `dd03f515`, the harness with the cost response) finished, aggregates, scores, guards and grades identical byte for byte.
- **The cost is carried** (decision 13): upper 50.33 h of 80 on the rerun's end stages, 50.35 h on the second rerun's; 273.5 GB of 319.6 — 200.1 GB runs, 73.4 GB the experiment's own files (decision 12 restated).
- **The starvation net was reopened and settled the same day** (decisions 17, 20, 21): the 100 ms boot default's failures are the point's own; 인경민 confirmed the boost resetting the running task's allotment is what the simulator means. On the second rerun nothing reopens; only the 100 ms count and the two chain-scale lines are unavailable; the cap band's `c2_pair` rows exempt; the longest-wait line does not reopen.
- **Harness change** `251eb50f`; suite 390 passed; both lints clean. Memo `docs/memos/2026-11-15-integration-gate-and-cold-smoke.md` to 인경민.
- **The second rerun's runs took 16.5% more run-seconds than the rerun's** for the same work, spread through the run; still 0.94 of the second smoke's. The cause is not established.

## Next

1. 10.5 (the RQ0 run): its spec session decides whether it starts from the smoke's cache, and what of the smoke's 38.9 GB on disk goes before it — free is 271.5 GB, under the upper disk projection's 273.5 GB, while they stay.

## Facts worth not rediscovering

- The results-cache key carries the harness package's own source (`harness_version`): any change under `harness/tools/harness/` rebuilds every run's records and aggregates; the second rerun's rebuilt set took `runs/.cache` from 18.6 GB to 24.9 GB.
- A run directory holds links into the cache: measured alone, each smoke experiment is 12.9 GB; beside `runs/.cache`, 4.7 GB.
- End stages about 580 s on 1,197 runs; at the full run's 740,818,977 aggregate rows, `aggregates.csv` is about 73 GB.
- The evaluator alone on a smoke's outputs takes about 2 min 20 s; `starvation.py` with 6 workers about 3 min 35 s; the harness suite about 16 min.
