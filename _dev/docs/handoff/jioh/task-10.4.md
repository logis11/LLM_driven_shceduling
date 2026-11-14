# Handoff — task 10.4 The cold smoke and the cost response (2026-11-14) — the pre-smoke work committed, the smoke not started

Spec `_dev/docs/spec/jioh/task-10.4-cold-smoke-and-cost-response.md` (decisions 1–19). On `main`, not pushed: `cabebef5` the pre-smoke work; `c1e12a09` sub-task 10.3, which decision 8 puts before the smoke (spec `_dev/docs/spec/jioh/task-10.3-variant-lines-read-a-failed-guard.md`). Research folder `_dev/research/jioh/task-10.4-cold-smoke-and-cost-response/`, its README the record.

## Where it stands

- **Landed:** the drop count by bisection, the schema check by signature, the rows' memory (decisions 1–2); what a finished run keeps — the trace and the records gzipped, the rerun trace as its hash (decisions 4–5); each run's peak memory and bytes in `run-times.csv`, each end stage's wall time in `stage-times.csv`; the smoke's spec copy at seed count 2, 1,197 runs (decision 9); the harness changelog's pre-smoke entry.
- **Checked:** the 28 short-run runs rebuild byte for byte; the runner before and after write the same outputs on the short run's seven files, run directories 1,468 MB → 53 MB; harness suite 380 passed.
- **Worker configuration** (decision 7), in the git-ignored `harness/runner.yaml`: `workers: 4`, `heavy_workers: 1`, `heavy_mb: 50`, from the calibration (`c6-dual` 9,593 MB peak, 588 s; the largest light file `c4-compile` 672 MB). The figures and the sum against 16 GB are in the README.
- `runs/smoke` and `runs/.cache` deleted; `runs/` holds `integration-gate/` alone; 302 GB free on 2026-11-14.

## Next

1. **Start the smoke** from the repository root, through the tunnel (decision 10): `nohup bash _dev/research/jioh/task-10.4-cold-smoke-and-cost-response/cold_smoke.sh &`. It refuses to start over `runs/cold-smoke` or `runs/.cache`; writes `start.json` (commit, versions, workers, free space) and `exit.json` in the research folder, the log to `runs/cold-smoke.log`.
2. A run that fails goes through the 10.2 spec's decisions 13–14, and the smoke restarts (decision 11).
3. After a smoke in which every run finished: `project.py --smoke runs/cold-smoke --free-gb <start.json's free_gb>` (decisions 12–13), then `starvation.py --smoke runs/cold-smoke` (decisions 16–17, and the 10.3 spec's decision 8: the two chain-scale lines expected unavailable, no other line).
4. The cost response (decisions 13–15), then the second changelog entry with decision 16's restatement and the re-pin (decision 18). With the four chain-scaled runs named, the restatement adds that both chain-scale lines print unavailable under 10.3's rule.
5. A memo only if a teammate is reached (decision 19).

## Facts worth not rediscovering

- At one heavy worker the full run's 1,350 heavy runs come to about 32 h on the calibration's `fixed` times alone, `c6-dual`'s 112 about 18 h of it — not the projection; the smoke measures every condition.
- `c1-compile/random-1` took 59 s in the rebuild check against 6.6–6.8 s for the file's other runs; left for the smoke's profile.
- A calibration taken earlier on 2026-11-14 mixed code versions and was discarded; `calibration.json` is the clean pass.
