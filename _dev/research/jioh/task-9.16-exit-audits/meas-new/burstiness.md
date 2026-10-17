# 9.16 — the burstiness and window readings on the two pools handed over

9.15 handed 9.16 (its `_dev/TODO.md` line, 2026-10-16) the burstiness and window readings re-run on the two pools the library now carries but those readings never read: `renderer-hidden`'s steady phase from `meas-ci:desktop:2026-10-05b` (9.10 D156, the hidden renderer folded from that campaign on Google Chrome 154; D156 hands "the burstiness and window readings re-run on this entry's pool" to 9.16) and `video-editor`'s idle phase from `meas-ci:interactive:2026-10-05` (9.10 D146, the idle phase re-measured past Kdenlive's launch work: a 240 s settle, a 180 s phase, 16 repeats). Read 2026-10-17.

## How it was run

- **Raw data.** The two releases' landings the pools carry, downloaded and checked against `dataset/meas-releases.yaml`'s SHA-256 (21 assets, 0 mismatches): `meas-ci-desktop-2026-10-05b`'s `meas-desktop-chrome-hidden-r{1..5}-full` and `meas-ci-interactive-2026-10-05`'s `meas-interactive-kdenlive-r{1..16}-idle`, unpacked under the shared raw root as `<raw-root>/<release>/<landing>` and linked as `<run id>/<landing>` for the tools' lookup.
- **Tools.** The committed `dataset/tools/meas/burstiness.py` and `windows.py`, called through their own entry functions by `readings.py` (beside this page) with two adjustments, both stated in its docstring: the idle landings' lookup (the finding below), and `windows.py`'s campaign family kept to `video-editor`'s idle phase (its driven and operation phases still come from 9.5's pool `meas-ci:interactive:2026-09-18` and were read there).
- **Output.** `out/burstiness.json`, `out/burstiness-tables.md`, `out/windows.json`, `out/windows-tables.md`. Run time 40 s.
- **Cross-check against the recorded readings of the same pools.** `renderer-hidden`'s window reading reproduces 9.10 D156's figures: the page thread `chrome` 0.068 ms a wake in the first 100 s and 0.057–0.072 ms after, the windows holding 5.2 % of the phase's CPU above the median window. `video-editor`'s measured tree wake rate, 1.264/s (median over the 16 streams), agrees with the kdenlive-idle results page's 1.2637/s.

## Burstiness: dispersion, measured over compiled

Dispersion is the variance over the mean of the wake counts in whole bins; 1 for a Poisson stream, above it bursty. The ratio is measured over compiled per stream (one stream per renderer for `renderer-hidden`, 12 renderers a repeat); median (least–largest) over the streams.

| entry, pool | streams | 1 ms | 10 ms | 100 ms | 1 s |
|---|---|---|---|---|---|
| `renderer-hidden`, `meas-ci:desktop:2026-10-05b` | 60 over 5 repeats | 1.256 (1.05–1.454) | 1.282 (1.03–1.428) | 1.435 (0.9804–1.819) | 1.709 (1.265–1.944) |
| `video-editor` idle, `meas-ci:interactive:2026-10-05` | 16 | 1.22 (0.9964–1.649) | 1.315 (1.049–1.738) | 1.319 (0.991–2.478) | 2.757 (1.116–7.964) |

Against the figures the measurement overview states (read 2026-09-27 on the earlier pools; `_dev/research/jioh/task-9.8-browser-comms/campaign/results-burstiness.md`, `_dev/research/jioh/task-9.5-interactive-typing/campaign/results-burstiness.md`):

- `renderer-hidden`: 1–100 ms medians 1.06–1.15× on 9.8's `meas-ci:desktop:2026-09-20` (228 streams over 19 repeats, Chrome 152 and 153, a 630 s grace-settle); **1.26–1.44×** now. Measured dispersion rose (1.41–1.59 against 1.08–1.19) while compiled stayed near 1.1. At 1 s, 1.24× then, 1.71× now.
- `video-editor` idle: 1–100 ms medians 1.255–1.395× (stated 1.3–1.4×) on 9.5's 20 repeats; **1.22–1.32×** now. At 1 s, 2.56× then, 2.76× now.

Both stay inside the threat the overview states: at 1–100 ms measured wake counts are more dispersed than compiled ones (every median above 1). `renderer-hidden` now sits above `video-editor`, between `game-client` (1.9–3.0×) and `video-editor`.

## Time windows

`renderer-hidden`, 5 repeats, six 100 s windows: the tree's wake rate per window 0.78–1.13 of its mean; `HangWatcher` 1.00 in every window; `chrome` 0.59–1.24 of its mean, its run mean 0.057–0.072 ms; the windows hold 5.2 % of the phase's CPU above the median window (9.8's pool: 13.3 %).

`video-editor` idle, 16 repeats, nine 20 s windows: the tree's wake rate per window 0.95–1.09 of its mean; `kdenlive` 0.95–1.09, its run mean 0.023–0.030 ms; `Qt bearer threa` 1.00 in every window; the residual 0.0028 wakes/s, 8 wakes over the 16 repeats' 2,880 s, 5 of them in the window at 120–140 s; the windows hold 2.7 % of the phase's CPU above the median window (9.5's pool, six 20 s windows: 2.1 %). No part of the phase holds work the rest does not: the 240 s settle (9.10 D146) leaves the launch work out.

## Findings

1. **The tools cannot find `video-editor`'s idle landings (code).** `burstiness.campaign_streams` and `windows.campaign_entries` look each carried repeat up with `artifact_dir(root, app, rep, run_id)`, whose mode defaults to `full`; the idle campaign's artifacts are `meas-interactive-kdenlive-r<k>-idle` (`campaign/kdenlive-idle/method.md` §1), and the pooled record `pool-kdenlive.json` carries no mode. Unpatched, both tools stop at "kdenlive repeat 1 of run 37273046929: 0 artifacts" (`burstiness.py campaign … --app kdenlive` and `windows.py campaign … --app kdenlive`, run 2026-10-17). Proposed fix: a mode beside `IDLE_FROM_95` in `dataset/tools/meas/control_report.py` (`IDLE_MODE_95 = {"kdenlive": "idle"}`), passed by both tools wherever they read the idle phase from `IDLE_FROM_95` (`artifact_dir(..., cr.IDLE_MODE_95.get(app, "full"))`); `readings.py`'s fallback does the same from outside.
2. **`renderer-hidden`'s scope misstates the residual's windows (data).** The scope (`dataset/archetypes.yaml`, written from `dataset/tools/meas/desktop/fold_in.py` `WINDOWS_1005B`; also 9.10 D156 and `campaign/renderer-hidden/results/results.md`) says "the residual (`MemoryInfra`, `ThreadPoolServi`) wakes at 3.6 times its phase rate in the first 100 s and 2.4 times 400–500 s in". On the library's components the residual is `ThreadPoolServi` (300 wakes over the 5 repeats) and `MemoryInfra` (45 wakes, 27 in the first window, 18 in the fifth); it reads **1.51 times its phase rate in the first 100 s and 1.36 times 400–500 s in**. The 3.6 and 2.4 are `MemoryInfra` alone — the residual read with `ThreadPoolServi` counted as a component (`windows.py` re-run with `ThreadPoolServi` added to the carried list: residual 3.6 · 0 · 0 · 0 · 2.4 · 0). Proposed text in `proposed-text.md`.
3. **The overview's threat sentence and two guidebook passages name the old figures and say the current pools are not yet read** (`docs/workload/measurement-overview.md` §8 "Compile fidelity" and "Time windows"; the dataset guidebook, volume 2 line 1501 and volume 6 line 1039). Proposed text in `proposed-text.md`.
