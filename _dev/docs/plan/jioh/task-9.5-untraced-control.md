# 9.5 untraced control — collection tooling, implementation plan

**Goal:** Control jobs for 9.5, 9.8 and 9.9 that run each carried phase as a traced and an untraced run and record every thread's CPU and switches at each run's edges, ready for the six dry runs.

**Architecture:** One new mode per family's `run.sh` — `control` (full's lengths) and `control-dry` (dry's) — which maps onto the existing `full`/`dry` branches and adds a `CONTROL` flag. `phase()` stays the traced run; a new `quiet()` is its untraced twin (same snapshots, driver and length, no `perf`); `pair()` runs the two adjacent in the job's order (odd index traced first). `probe/snapshot.py` gains per-thread counters (`schedstat`, `status`, start time) and each process's cgroup, so the snapshots every run already takes carry decision 9's instrument. The ratios, the D36 reading, the shares of decisions 10 and 22, the workload check and the reporting are the analysis plan's, written once the dry runs' artifacts exist.

**Tech stack:** bash, Python 3.12 (tests), pytest; `dataset/tools/meas/` (campaign, desktop, session, probe); GitHub Actions workflows `meas-interactive.yml`, `meas-playback.yml`, `meas-desktop.yml`, `meas-session.yml`.

**Spec:** `_dev/docs/spec/jioh/task-9.5-untraced-control.md` (decisions 1–22).

## Global constraints

- Branch `jioh/dataset-rebuild`; no worktree. Commits by explicit paths, `<type>(jioh/phase-9): …`.
- Tests from `dataset/`: `python3.12 -m pytest tools/tests -q` (baseline at `1f824ae`: 281 passed, 1 skipped, 1 xfailed).
- The campaign modes (`dry`, `full`, `probe`) behave as before, apart from the per-thread fields in every snapshot, the `sysctl.sched_schedstats` record, and 9.9's snapshots at each phase's edges.
- A control artifact is named `…-control` or `…-control-dry`: the campaign pools' name patterns and `POOLED_MODES` never pool it (decision 15).
- Every dry run and launch waits on 인지오's approval.

## Review focus

- A prelude that does not reach its designed state (the Writer close-and-reopen, GIMP's bound Revert, Kdenlive's bound Revert) — read on the dry run's `after-ctrlprelude-*` screenshots against `after-postlaunch`/`after-settle`.
- A tid reused between a run's two edges — the snapshot records each thread's start time, which the analysis compares.
- The window id after a prelude that reopens the document — `ctrl_prelude` re-reads it and records it.
- The untraced operation run's log — its own `ops-untraced.jsonl`; the SMTP peer's rows are shared, and `ops_driver` offsets by the rows present before each send.
- The longest 9.5 control job against the interactive workflow's timeout — `web-browser`: settle 420 s + 2 × 600 + 2 × 605 + 2 × 605 + gaps ≈ 68 min of phases; the timeout goes 90 → 150 min.

---

### Task 1: per-thread counters in the snapshot

**Files:** Modify `dataset/tools/meas/probe/snapshot.py`; Test `dataset/tools/tests/test_meas_control.py` (new).

**Produces:** `snapshot.snapshot(pattern, exclude) -> dict`; each `procs[]` entry gains `cgroup` and `tasks: [{tid, comm, start_ticks, run_ns, wait_ns, slices, vol, invol}]`; `snapshot.PROC` (the `/proc` root, for tests).

- [ ] Tests over a fake `/proc` in `tmp_path` (`monkeypatch.setattr(snapshot, "PROC", …)`): each thread's `run_ns`, `wait_ns`, `slices` from `task/<tid>/schedstat`, `vol`/`invol` from `task/<tid>/status`, `start_ticks` from field 22 of `task/<tid>/stat`; the process's `cgroup` from the `0::` line; a thread whose `schedstat` vanished is skipped; the tree sums (`vol_switches`, `n_threads`) unchanged.
- [ ] Run them: fail (`snapshot` has no `snapshot()` / `PROC`).
- [ ] Implement: `PROC = "/proc"` used by every read; `task_counters(pid, tid)`; `cgroup(pid)`; `snapshot()` built from the old `main()`, which prints it.
- [ ] Run: pass. Commit.

### Task 2: 9.5 control mode

**Files:** Modify `dataset/tools/meas/campaign/run.sh`, `dataset/tools/meas/probe/appdefs.sh`, `.github/workflows/meas-interactive.yml`; Test `test_meas_control.py`.

- [ ] Text tests (the desktop and session tests' form): the mode map `control → full`, `control-dry → dry`, `rec mode "$MODE_ARG"`; `ORDER` by the index's parity; `quiet()` holds no `perf` and snapshots both edges; `pair()` runs `ctrl_prelude` before `phase`/`quiet` inside its loop; `control_phases()` pairs idle, driven (stream and pointer, with the prelude), play and op, and holds no `driven-alt`/`aalto`; the untraced driven and op runs write `replay-untraced.jsonl` and `ops-untraced.jsonl`; `op_driver` writes `${OPS_OUT:-$OUT/ops.jsonl}`; `CTRLPRELUDE` set in the `soffice`, `gimp` and `kdenlive` arms and defaulting to `ALTPRELUDE`; GIMP's `menurc` binds `file-revert`, Kdenlive's kxmlgui stub binds `file_revert`; `rec sysctl.sched_schedstats`; `meas-interactive.yml` `timeout-minutes: 150`.
- [ ] Run: fail.
- [ ] Implement in `run.sh`:
  - `MODE_ARG="${3:-full}"; CONTROL=0; MODE="$MODE_ARG"`, then `case "$MODE_ARG" in control) CONTROL=1; MODE=full ;; control-dry) CONTROL=1; MODE=dry ;; esac`; `rec mode "$MODE_ARG"; rec control "$CONTROL"`.
  - `rec sysctl.sched_schedstats "$(cat /proc/sys/kernel/sched_schedstats …)"`; `ORDER` = `traced untraced` for an odd index, `untraced traced` for an even one, recorded as `control.order` in a control job.
  - `phase_summary <name>` factored out of `phase()` (the snapshots' deltas into `report.kv`); `quiet <name> <secs> <driver>`: `snap before`, `sleep secs &`, the driver after 1 s, `wait`, `snap after`, screenshot, `phase_summary`.
  - `ctrl_prelude <label>`: activate the window, run `CTRLPRELUDE`, record its rc, re-read the window (`wait_window "$CLASS" 60`), screenshot `after-ctrlprelude-<label>`, 5 s.
  - `pair <name> <secs> <builder> [prelude]`: for each run in `ORDER`, 10 s between runs, the prelude if asked, then `phase <name>` (traced) or `quiet <name>-untraced` with `$(<builder> <run>)`.
  - Builders: `no_driver`; `stream_driver <run>` (the job's window of `STREAM` into `$WID`, `replay.jsonl` / `replay-untraced.jsonl`); `pointer_loop` (the existing loop, factored out and reused by the campaign branch); `op_run_driver <run>` (`OPS_OUT` → `ops.jsonl` / `ops-untraced.jsonl`). `window_state` factored out of the stream branch.
  - `control_phases()`: idle pair (stream, pointer); for stream, a window other than `ok` records `control.stopped` and ends the sequence; driven pair with the prelude; play pair (`none`); op pair when `OP` is set, with both runs' counts recorded. The existing `case "$DRIVER"` and op block run only when `CONTROL` is 0.
- [ ] Implement in `appdefs.sh`: `CTRLPRELUDE=""` in the defaults; the three preludes —
  - `soffice`: Escape, Ctrl+W, Alt+D (Don't Save), reopen `/tmp/doc/large.odt` through the running instance, 30 s, Ctrl+End — the document as converted, the caret at its end (the postlaunch's state);
  - `gimp`: a `menurc` line binding `<Actions>/file/file-revert` to Ctrl+Shift+Alt+R; Escape, the key, Return on the confirmation, 20 s, Escape — the image as loaded;
  - `kdenlive`: `file_revert` → Ctrl+Shift+F8 in the stub; Escape, the key, Return on the confirmation, 20 s, Escape — the project as generated;
  - `op_driver` writes `${OPS_OUT:-$OUT/ops.jsonl}`.
- [ ] `meas-interactive.yml`: `timeout-minutes: 150`.
- [ ] Run: pass; `bash -n` on `run.sh` and `appdefs.sh`. Commit.

### Task 3: 9.8 control mode

**Files:** Modify `dataset/tools/meas/desktop/run.sh`; Test `test_meas_control.py`.

- [ ] Text tests: the mode map and `rec mode "$MODE_ARG"`; `quiet()` without `perf`, with both edges' snapshots and `edge` marks; `pair()` in `ORDER`; in a control job `chrome-hidden` pairs `steady`, `chrome-visible` pairs `steady-notimer` and runs no `steady-timer` phase (its time kept as an unmeasured wait, so the page's own schedule reaches the no-timer step), `element` pairs `idle` and runs no `traffic`, `steam` pairs `shown` and runs no `minimised`; `rec sysctl.sched_schedstats`; `test_the_renderer_subjects_drive_no_input` still passes.
- [ ] Run: fail. Implement (the 9.5 pieces without preludes; `pair <name> <secs>`). Run: pass; `bash -n`. Commit.

### Task 4: 9.9 control mode

**Files:** Modify `dataset/tools/meas/session/run.sh`; Test `test_meas_control.py`.

- [ ] Text tests: the mode map and `rec mode "$MODE_ARG"`; `phase()` and `quiet()` take a whole-system snapshot (`snapshot.py '.'` under sudo) after `census "$name.start"` and before `edge "$name" start`, and after `edge "$name" end` and before `census "$name.end"`; `quiet()` holds no `perf`; a control job runs `pair steady "$STEADY"`; `rec sysctl.sched_schedstats`; `test_run_sh_carries_the_decisions` still passes.
- [ ] Run: fail. Implement. Run: pass; `bash -n`. Commit.

### Task 5: the whole suite, then the dry runs

- [ ] From `dataset/`: `python3.12 -m pytest tools/tests -q` — the baseline plus the new tests.
- [ ] On 인지오's approval, the six dry runs (decision 19), each by setting the family's trigger `mode` to `control-dry` with the app and index, pushing, and resetting to `full` with no apps after it lands (precedent `930ac89`, `0b86bff`):
  1. 9.5 family — `chrome` (`web-browser`), index 1 (traced first): the idle, driven (existing prelude) and op pairs.
  2. `soffice` (`office-writer`), index 2 (untraced first): the new prelude.
  3. `gimp` (`image-editor`), index 2: the new prelude.
  4. `kdenlive` (`video-editor`), index 2: the new prelude.
  5. 9.8 family — `chrome-visible`, index 2: the timer wait and the `steady-notimer` pair.
  6. 9.9 family — `session`, index 2: the `steady` pair.
- [ ] Read each: `control.order`, `sysctl.sched_schedstats`, perf files for the traced runs only, both runs' snapshots carrying `tasks` with nonzero `run_ns`, equal replay counts for the two driven runs, both op logs, gates open; each prelude's screenshots against the designed state. A prelude that misses its state is amended and its dry run repeated.
