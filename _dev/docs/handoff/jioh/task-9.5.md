# Handoff — task 9.5 Interactive and typing (2026-09-15)

Branch `jioh/dataset-rebuild` (all of 9.5 lives there, `_dev/` included). The slice's records: `_dev/research/jioh/task-9.5-interactive-typing/` — `changelog.md` (D1–D20, the decision record), `campaign/method.md`, `campaign/probe.md`, `campaign/results.md`, `campaign/results/` (pooled JSON, per-run reports).

## Where it stands

- **Stage 3 decisions done and applied (D1–D20).** `desktop-interactive`, `audio-playback`, `video-playback` are gone; nine measured per-application archetypes are in `dataset/archetypes.yaml` (`office-writer`, `code-editor`, `mail-client`, `web-browser`, `image-editor`, `video-editor`, `video-player`, `audio-player`, `video-call`), each one observation from the 9.5 campaign (`meas-ci:interactive:3`, `meas-ci:playback:3`; Thunderbird repeats 2–3 from `interactive:4`), quantile tables (D17), per-thread timer components (D16), replayed SWELL-KW stimulus under `dataset/stimulus/` (D18), one explicit event stream per task (D9). Timelines rebound (30 bindings), derived files regenerated, grid unchanged, registry edited (`swell-icmi14` in; `dhakal-chi18`, `roeser-rw24` out; interbench trimmed).
- **Campaign**: workflows `meas-interactive.yml` / `meas-playback.yml` driven by `.github/campaign.json` (push-triggered; dispatch is unavailable off `main`); tools under `dataset/tools/meas/campaign/` (`run.sh`, `analyze.py`, `pool.py`, `fold_in.py`, `render_results.py`, `build_windows.py`) and `dataset/tools/meas/probe/` (appdefs, replay drivers, extractor). Raw data: release `meas-ci-2026-09-14` (D20).
- **Build state on the branch**: `make -C dataset lint/test` green (90 passed, 1 xfailed: the window test); `compile.py --allow-window` writes; CI's window gate and the harness's RQ0 pin check fail by design until 9.14 (D19). Compile ≈ 5 min, compiled set 112 MB.

## Next — follow-ups 인지오 took on 2026-09-15 (in this order)

1. **Single-core campaign.** The runner has 4 vCPUs and the simulator one lane; the measured trees ran their threads in parallel. Re-run the campaign with the application's process tree pinned to one CPU (`taskset` in `run.sh`), same phases and stimulus. Decision to take first: whether the pinned run *replaces* the unpinned one as the archetypes' observation or is carried beside it; then re-pool, `fold_in.py`, re-splice, rebuild. Changelog entry.
2. **Heavy-operation driven phases.** Scripted phases whose trigger is design and whose cost is measured, per application: VS Code with a project open and a language server; a GIMP filter; a Kdenlive preview render; Chrome loading a page with scripts; Writer with a large document. Grill: which operations, how they enter the archetype (further `focus_components` or a separate operation kind), and how a timeline invokes them (9.10 boundary). Then campaign, pool, fold-in.
3. **Stimulus sensitivity.** Replay the 136M Keystrokes data (S3-aalto136m; transcription) as a second stream for the typing-driven runs and compare per-input distributions with the SWELL-KW ones; state whether the stimulus choice moves the values. Needs an extraction tool for that dataset (raw press/release timestamps, non-commercial licence) and one campaign batch.
4. **Display and GPU — discuss in depth** (no decision yet): recovering a real display server, compositor and GPU means a self-hosted runner or a volunteer machine, which touches phase decision 5 (CI runners only). Bring the options with what each recovers (paint cadence at refresh, rasterisation off the CPU) and costs.
- **Deferred**: real-desktop validation traces (volunteer `perf sched` captures, comm names and timing only) — needs a decision-5 exception; not now.

## Open threads and hand-offs (also in the changelog entries)

- 9.10: `c1-meeting` carries two `video-call` tasks (zoom voice + video), doubling one call (D19); VS Code's helper processes as named tasks for recognition realism (D14); **SWELL-KW's `Window Activated` events give real per-participant sequences of application focus and durations over ~3 h — a source for task sets, focus windows and switching from a recording the dataset already cites** (noted 2026-09-15).
- 9.14: demand-window rule (eight `-single` files at 0.63–0.90), `tick_count`'s stimulus-count part (image-editor and video-editor emit no input wakes), prior-table editor rows and H1, the RQ0 gate's dataset pin.
- 9.13: compile time and compiled size (explicit event streams; a faster sampler or compact timer encoding).
- 9.15: docs for the nine entries and the retired three; the seven docs citing the two typing studies.
- 9.8: Chrome renderer rows from the campaign as an observation of renderers on a static page (D14). 9.11: TIMER backlog vs players' frame skipping (D11).
