# Handoff — task 9.6 Compile: the top-up campaign in progress (2026-09-19)

Branch `jioh/dataset-rebuild` (Phase 9 works here). 9.6 stays `[WIP]`. Supersedes `/private/tmp/handoff-9.6-topup-and-fold-in-2026-09-19.md`.

## Where it stands

- Decisions D12–D28 in `_dev/research/jioh/task-9.6-compile/changelog.md`; method deviations in `campaign/method.md` §8 (nine 2026-09-19 entries). Today's:
  - D26 — the criterion is the shared stability rule (`_dev/research/jioh/measurement-campaign-workflow.md`, "The stability rule"): each carried table tested by its per-repeat mean; 33 values.
  - D27 — `clamscan` reads a fixed signature database, daily 28128 / main 63 / bytecode 339, from the Actions cache (`clamav-db-daily-28128-main-63-bytecode-339`; `dataset/tools/meas/build/clamav_db.sh`, job `clamav-db` in `meas-build.yml`); `clamscan` pools repeats 9 on, 4–8 reported beside the pool.
  - D28 — `python3` starts warm (one unmeasured `train.py 1` before the measured run, `train.warm.rc`); pools repeats 11 on, 4–10 reported beside the pool.
- Pool at the checkpoint (commit `96717bd`, `campaign/results.md`, `results/pooled.json`): repeats 4, 5, 7, 8, 9, 10, 11, 12 on the AMD EPYC 7763, all valid; 26 of 33 values within tolerance. Open: `clamscan` (4 repeats on 28128) block mean ±22.4 %; `python3` (2 warm repeats) runs ±16.5 %, block mean ±152 %; `tracker` block mean ±15.5 % (repeat 12 at 23.3 µs). Projected 35–51 repeats; the `python3` projection rests on two repeats.
- 인지오's decision at the checkpoint: keep adding repeats until every value holds (the disk-bound block means average over the runner's disk).

## Overnight loop (running detached)

- `~/.cache/meas-loop/overnight/loop.sh 14 26 12`, started 13:08 UTC under `nohup caffeinate -i`; log `~/.cache/meas-loop/overnight/loop.log`. Repeat 13 was in flight as run #26 (35443899531).
- Per repeat: `watch.py` (relaunches gated attempts) → `pool_runs.py` → launches the next index only when the job landed and the pool prints "every repeat valid". Stops on no landing, an invalid repeat, a failed launch, the rule holding, or 12 launches. Commits nothing but the trigger pushes.
- Check: `tail -40 ~/.cache/meas-loop/overnight/loop.log`; `pgrep -fl "loop.sh"`. While it runs, start no other build watcher (two would both relaunch a gated attempt).

## Next

1. Read the log. If the loop stopped, act on its STOP line; restart with `nohup caffeinate -i bash loop.sh <next index> <run number of the launch in flight> <cap> >> loop.log 2>&1 < /dev/null & disown` from `~/.cache/meas-loop/overnight/`.
2. Commit the latest pool: `pool_runs.py build --since 10 -- --title "<tag; every run id; repeats; D11, D26–D28>"`, copy `results.md` and `pooled.json` from `~/.cache/meas-loop/pool/build-build-from10/` into `campaign/`.
3. When `python3` has five warm repeats (repeat 15): bring 인지오 the values and each open value's projected count.
4. Two questions held for 인지오, one at a time: the list carries CPU per process of `sh` and `gcc` while the fold-in carries their per-step tables (D20); whether 9.6 uses `stability.py`'s `keep_zero` (a zero counted as a repeat's value) for the block means and shares.
5. When the rule holds: final pool into `campaign/`, a changelog entry, the 9.6 rows of `_dev/research/jioh/measurement-campaign-record.md`.
6. Fold-in (plan, then execute): the D19 object-job chain in `dataset/tools/wlc/compiler.py`, D20 member tables, D21/D22/D25 `cpu-batch` per-program tables with the explicit binding, D16's window for `tracker`, `build-orchestrator`'s dispatch table, the D27/D28 conditions in scope, `modeling_notes` / scope / `validation_stats` / `category_source`, timeline bindings, `make -C dataset dataset lint test check PY=python3.12` (the demand-window lint fails on five `-single` files until 9.14).
7. Release `meas-ci-build-2026-09-18` at the fold-in commit (D18; ask first): every run of the campaign; the gated attempts per run are in `~/.cache/meas-loop/gate/<run>/`; the D28 dry check (run 35431343598, `meas-build-r0-dry`) is not a repeat.
8. Wrap-up hand-offs recorded in D16–D25 (9.5, 9.10, 9.11, 9.12, 9.13, 9.14, 9.15).

## Pitfalls

- The working tree is shared with the 9.5 and 9.7 sessions: stage by path; shared files by hunk.
- The GitHub API limit (5 000 requests an hour) is shared by every session's loop tools; poll at 120 s or more. `common.py` caches completed runs' job lists.
- Read the 1 µs-floor values (`ffmpeg`, `HandBrakeCLI`, `tracker` block means) from the absolute half-width, which the loop printout now shows.
- `SSL_CERT_FILE=/etc/ssl/cert.pem` for Python HTTPS on this Mac.
