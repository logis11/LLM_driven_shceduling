# Handoff — task 9.7 Background and IO, and 9.5's Thunderbird send re-observation (2026-09-19)

Branch `jioh/dataset-rebuild` (Phase 9 works on this branch only). Stage 3 of `_dev/research/jioh/research-slice-workflow.md` is decided for 9.7: D1–D17 in `_dev/research/jioh/task-9.7-background-io/changelog.md`. The campaign method draft `…/task-9.7-background-io/campaign/method.md` was reviewed by 인지오 ("looks good"); it is the spec for the tooling. `_dev/TODO.md` carries the summary, the open sub-items and every hand-off to other slices (commit `93a7ec7`).

## The next session's work, as 인지오 set it

1. **Build 9.7's campaign tooling** per `campaign/method.md` — header, §1–§4, §8: `dataset/tools/meas/background/` (`run.sh <app> <repeat> <dry|probe|full>` for apps `borg`, `7z`, `steamcmd`; `analyze.py` and `pool.py` implementing §5), `.github/workflows/meas-background.yml`, trigger `.github/campaign-background.json`, the `background` family in `dataset/tools/meas/loop/common.py`; `meas-cli.yml` removed (§8). Model it on 9.6's: `dataset/tools/meas/build/run.sh` (the machine gate, pins, instruments, recording), `build/taskstats_listen.c` (reuse), `.github/workflows/meas-build.yml`, `.github/campaign-build.json`, and the dry-run lessons in 9.6's `campaign/method.md` §8.
2. **Build the tooling of 9.5's added task** — the `_dev/TODO.md` 9.5 sub-item "Thunderbird re-observed whole with a `send` operation" (9.7 D3): a `send` operation in Thunderbird's setup (`dataset/tools/meas/probe/appdefs.sh`, `ops_driver.py`, the `op` phase of `dataset/tools/meas/campaign/run.sh`), an SMTP server in the profile pointing at a local peer on the harness CPUs, the send's scripted repeats and completion signal. This is the reading of "the added task for 9.5 about campaign run"; confirm it with 인지오 before building. Its choices — message and attachment (9.5 follow-ups spec decision 10: benchmark documentation first, else design), the peer, the completion signal — are 9.5 decisions: bring them one at a time, record them in 9.5's changelog and a dated entry of 9.5's `campaign/method.md`. The re-observation runs only after 9.5's current campaign ends; do not touch that campaign's trigger file, windows or runs.
3. **Report to 인지오** when both toolings are built and checked locally. Do not push a trigger file, launch a dry run or publish a release without 인지오's go-ahead — each starts or publishes something outward.

## Facts the tooling needs that are not in the method

- Thunderbird cannot send headlessly: `-compose` opens a window and does not send, no Mozilla source documents a command-line send (search record `S4-ci-observability.md`, S4-17); the send is triggered in the GUI under Xvfb, as 9.5's campaign drives Thunderbird. Local SMTP peers: `python3 -m aiosmtpd -n` (`python3-aiosmtpd`, noble universe) or Mailpit (S4-29). Thunderbird holds one SMTP connection per server (S4-17).
- Noble packages checked 2026-09-19: `p7zip-full` is transitional to `7zip` 23.01 (D9, copy in `sources/D9/`); `zpaq` 7.15 is in universe; `fincore` ships in `util-linux-extra`, not `util-linux`. `steamcmd` is multiverse and needs i386 multiarch and a non-root user (S4-16, S4-32).
- The D11 rate snapshot and `rate.py` are in `_dev/research/jioh/task-9.7-background-io/sources/D11/` (gitignored, local only); `python3.12 rate.py` prints 121.0 Mbps.
- Local Python: `python3.12` has PyYAML, jsonschema and pytest (`python3` does not). `make -C dataset check PY=python3.12` fails on five files below the demand window — pre-existing, until 9.14; `compile.py --allow-window` writes despite it. The full test suite runs longer than ten minutes.
- D5 left one thing untraced: removing an unbound archetype changed the bytes of every compiled file while the compile report stayed identical.

## Working in the shared tree

Other sessions (9.5's campaign, 9.6, 9.8) work in the same directory and branch. Commit named paths only, never `git add -A`; check `git status` before each commit; leave other slices' TODO lines, archetypes and trigger files alone. The loop tools' watcher reads only runs since the latest launch (`measurement-campaign-workflow.md`, the loop).

## After the tooling (9.7's remaining sub-items)

Dry run → amendments in `method.md` §9 (disk location, depot size, 7-Zip time and the 1 GB fallback, the network-wait matching) → probe batch of three repeats per program → first batch → repeats until the 5 % rule holds → pool → fold-in (remove `io-stream`, `network-bulk`; add `file-backup`, `file-archiver`, `game-download`; rebind the timelines so the dataset compiles, as 9.5's fold-in rebound its bindings; the registry changes of D17) → hand-offs. The desktop Steam client probe runs only if 인지오 provides an account (D4).

## Suggested skills

- `daily-work-harness:pick-up-task` — resume 9.7 (`[WIP]`) and brief the tooling work.
- `superpowers:test-driven-development` — for `analyze.py`/`pool.py` (§5's rules against hand-made fixtures before real records).
- `superpowers:verification-before-completion` — before reporting the tooling as done.
- `daily-work-harness:wrap-up` — at session end.
