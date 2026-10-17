# Task 9.10 — the entries held past their observed phases: probe method (2026-10-05)

The long-phase probes of the states the core-set files hold longer than their entries' observed phases (changelog D143, D144), run on GitHub-hosted runners under `../../../measurement-campaign-workflow.md`'s machine rule. A probe is never a repeat, is pooled into nothing and changes no value (D143). Amended only by a dated entry in §6. Tooling: `dataset/tools/meas/campaign/run.sh` (modes `probe` and `probe-driven`), workflow `.github/workflows/meas-long-probe.yml`, trigger `.github/campaign-long-probe.json`, loop family `long-probe`; the hidden renderer's through `dataset/tools/meas/desktop/run.sh` mode `probe`, `meas-desktop.yml`, `campaign-desktop.json`, loop family `desktop`; the readings `dataset/tools/meas/campaign/span_probe.py`.

## 1. Probes

- **Machine.** The AMD EPYC 7763 only; `machine_gate.sh` stops a job that drew another model before any install or measurement, and the same index is relaunched.
- **Indices.** 10 for an idle or steady probe, 11 for a driven probe, clear of 9.5's and 9.8's probe indices.
- **Phases.** Each probe runs its campaign's own phases up to the long one, so the long phase opens where every repeat's phase opened.

| probe | entry, state | family, subject, index | mode | phases | the file's span it covers |
|---|---|---|---|---|---|
| Writer idle | `office-writer`, idle | `long-probe`, `soffice`, 10 | `probe` | 30 s settle, 1,500 s idle | 1,429 s, `c3-workday` |
| Kdenlive idle | `video-editor`, idle | `long-probe`, `kdenlive`, 10 | `probe` | 30 s settle, 3,000 s idle | 2,976 s, `c3-creation` |
| Kdenlive driven | `video-editor`, driven | `long-probe`, `kdenlive`, 11 | `probe-driven` | 30 s settle, 120 s idle, 10 s, 8 driven windows | 4,758 s, `c1-transcode` |
| VS Code driven | `code-editor`, driven | `long-probe`, `code`, 11 | `probe-driven` | 30 s settle, 900 s idle, 10 s, 21 driven windows | 12,068 s, `c6-dual` |
| hidden renderer | `renderer-hidden` | `desktop`, `chrome-hidden`, 10 | `probe` | 20 s launch-settle, 630 s grace-settle, 1,800 s steady | 1,545 s, `c3-workday` |

## 2. The driven windows

- **A window** is one 9.5 driven phase: `perf sched record` over 605 s with the driver inside it from 1 s, the 600 s of input it drove. The next window opens when the previous one's trace stops; that trace is converted to its timehist and wakeup rows in the background, at the lowest priority on the harness CPUs, and its `perf.data` deleted. Consecutive windows are about 6 s apart, with no input in between, as a 9.5 driven phase's own tail.
- **VS Code.** Window k replays `swell-word-c1`'s window k (`dataset/meas/streams/word-r<k>.jsonl`), the window 9.5's repeat k replayed, keys only (9.5 D72), into the document the earlier windows typed: no prelude between windows. Build 1.138.0, the appdef's pin (9.5 D69).
- **Kdenlive.** Every window runs the campaign's scripted pointer loop (`campaign/run.sh`, `pointer_loop`).
- **Dry run.** `probe-driven` at three 60 s windows of each driven subject, the gate open on any model, never read.

## 3. Readings

- **Idle, steady and Kdenlive driven (D143).** From the 10 s slice profile of the long phase (`campaign/slices.py`; the driven windows' slices end to end, the gaps between windows left out), the level over the file's span from the phase's opening, CPU ms/s and wakes/s, against the observed phase's window at the placement every repeat takes, the phase's first 120 s (idle) or 600 s (driven, steady). A difference over 5 % in either is a phase that does not hold over the span. The worst placement of a window of the phase's length inside the span, stepped by 10 s, is reported beside it (9.5 D53, D56). `span_probe.py level`; for the hidden renderer `span_probe.py level-desktop` on the renderer rows `desktop/analyze.py` keeps.
- **VS Code driven (D144).** Each window's per-input run mean — the window rule's `run_ms_minus_idle`, read by `campaign/analyze.py` as the pool reads a repeat, the idle rate from the probe's idle phase read from 200 s (9.5 D83) — divided by 9.5's repeat k's (`task-9.5-interactive-typing/campaign/results-re-measured/pool-code.json`). The 21 ratios read as 9.5 D81's check reads its per-repeat ratios: their mean with its 95 % t interval, a difference where it excludes 1; and their least-squares slope on k with its 95 % t interval. The ratios' mean carries the probe's one session against each repeat's own, its idle rate among them — read on another repeat's idle rate, 9.5's window 5 comes out 1.0 % above its own repeat's mean — and their slope the session's age. `span_probe.py paired`.
- **Validity**, before a probe is read: the gate open on the EPYC 7763; every phase and window present with its trace stopped cleanly; each VS Code window's replay sending every key of its window; screenshots showing the typing landing in `source/index.ts` and Kdenlive's window holding the project; for the hidden renderer, the desktop family's renderer gate.

## 4. What follows

A probe changes no value (D143). A state whose phase does not hold over its span is a decision of its own, recorded in the changelog.

## 5. Records

Each probe's run id and artifact, and its reading, go into `results/` and `results/results.md`. A release of the probes' raw records only on 인지오's go-ahead.

## 6. Amendments

- 2026-10-05, the method written (D145).
- 2026-10-05, the first probes (runs 37263321218, 37264950064, 37264996600; the dry run 37263264550; changelog D145); the readings in `results/results.md`.
- 2026-10-05, D149 — amending §1 "Probes": the hidden renderer probed again, `chrome-hidden` 11, its steady phase 3,600 s past the 630 s grace-settle (`desktop/run.sh`'s probe mode), to show where the page thread's decline ends. Run 37273691029; 37273549541 and 37273631811 stopped at the gate.
- 2026-10-05, D150 — amending §1 "Probes": Kdenlive driven probed again, `kdenlive` 12, as `kdenlive` 11, to see whether the step about 1,200 s into the input recurs. Run 37274214398.
- 2026-10-05, D154 — amending §1 "Probes" and §2 "VS Code": VS Code driven probed again, `code` 12, mode `probe-driven-reset`, the committed file restored before every window past the first by 9.5's untraced-control prelude (`campaign/run.sh`, `ctrl_prelude`), so no line outgrows one window's typing. The dry run 37287429163, three 60 s windows; the probe, run 37289898127, read under D158.
