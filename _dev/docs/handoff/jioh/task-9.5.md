# Handoff — task 9.5 Interactive and typing (2026-09-24, 11:20 UTC) — done

9.5 is closed. Nine measured per-application archetypes, every value from a same-machine campaign on one AMD EPYC 7763 under the machine gate. Decision record `_dev/research/jioh/task-9.5-interactive-typing/changelog.md` (D1–D69), method `campaign/method.md` (§9 carries every amendment), workflow `_dev/research/jioh/measurement-campaign-workflow.md`. Branch `jioh/dataset-rebuild`; everything below is committed and pushed.

## Where the nine archetypes ended

| archetype | application | repeats | rule |
|---|---|---|---|
| `office-writer` | `soffice` | 14 | holds |
| `mail-client` | `thunderbird-send` | 43 | holds; the operation's 39 values reported at the recording's window limit (D46) |
| `image-editor` | `gimp` | 5 | holds |
| `video-editor` | `kdenlive` | 20 | holds |
| `video-player` | `mpv-video` | 24 | holds |
| `audio-player` | `mpv-audio` | 31 | holds |
| `web-browser` | `chrome` | 38 | holds; 30 values reported at the window limit, the widest being the SWELL-KW `input_run` mean, 1.701 ms ±8.33 % (D32, D68) |
| `code-editor` | `code` | 41 | holds; three values carried under D57 (its `utility/libuv-worker` component) |
| `video-call` | `webrtc` | 45 | holds; seven carried under D57 (the audio path, D59) |

Pools and rendered results: `campaign/results-same-machine/` + `results-same-machine.md` (the six), `campaign/results-re-measured/` + `results-re-measured.md` (the three). Rows in `_dev/research/jioh/measurement-campaign-record.md`.

## The last four decisions

- **D66** — a window measured twice by a duplicated run; the original launch's copy is kept (`pool_runs.py --exclude K@RUNID`).
- **D67** — a component is identified by its process role and comm together. `chrome`'s `Chrome_ChildIOT` names one thread in the GPU process (4,400–4,700 wakes per 600 s idle phase) and one in each of three utility processes (0–75); pooled by comm alone, the rare threads' gaps of minutes moved the component's gap mean 40 % and the rule would not close. Split by role it is 131.9 ms ±0.9 %. A single-process tree keeps plain comm names. `SESSION_SPREAD`'s keys carry the role with it — an exception keyed by the old name stops applying silently.
- **D68** — the recording's window limit entered for `chrome` (38) and `code` (44), and `mark_limited` reads the highest window the phase reached rather than how many repeats it holds: a window left out under D47, or one whose recording holds no event (`word-r43`), leaves the count short while the recording is just as exhausted.
- **D69** — the application build is pinned where the vendor serves a version of its own (`code` at 1.138.0, gated like the CPU model), recorded per repeat and stated where it is not (`chrome`, `webrtc`). VS Code 1.139.0 landed mid-campaign and runs a `copilot-runtime` process at 49.7 wakes/s in the idle phase; `chrome` holds 152.0.7977.82 in 29 repeats and 153.0.8010.52 in 9, the two builds agreeing within 0.18–1.09 standard deviations on every carried value.

## Released

Both outward-facing, on 인지오's 2026-09-24 approval, screenshots omitted:

- `meas-ci-2026-09-18` — the six (`meas-interactive-six.zip` 1.37 GB, `meas-playback-six.zip` 314 MB).
- `meas-ci-2026-09-20` — the three (`meas-interactive-chrome.zip` 1.47 GB, `meas-interactive-code-windows-1-22.zip` 1.39 GB, `…-23-42.zip` 1.26 GB, `meas-playback-webrtc.zip` 1.31 GB). `code` is split because a release asset is capped at 2 GiB.

## Folded in

All nine entries in `dataset/archetypes.yaml` regenerated from the pooled records (`fold_in.py` + `splice.py`), replacing the five-repeat values of the 2026-09-16 campaign. `mail-client` folds from `thunderbird-send`, the send re-observation that replaced it whole (9.7 D3; D31, D36, D49). `web-browser` carries D64's heavy event as a `heavy_events` block — `MemoryInfra`'s pass, its run quantiles over 8 observations, the count and the 22,800 s counted over, and no interval, none having been measured; the linter takes the block and rejects one that states a gap.

State of the gates at close: `make -C dataset dataset lint check PY=python3.12` stops on five errors, all of them the `-single` demand window (`c2-p3a`, `c2-p3b`, `c3-creation`, `c3-evening`, `c3-workday`), which is 9.14's. `make -C dataset test` passes 213; its one intermittent failure is the 9.9 session slice's fold-in test, which asserts that slice's entries match its pooled record byte for byte while another session has that record open.

## What 9.5 hands on

Already written into the TODO items that own them: 9.10 (the timeline questions, SWELL-KW's window-activation data as a source for task sets and focus windows, whether a timeline models an application's launch work), 9.14 (the demand-window and prior-table sensitivity checks; whether a scheduling outcome moves with the values carried under D57), 9.15 (the docs naming the retired entries, the library-level scale limitation), 9.16 (the venue mix per timeline; reproduction from the two releases).

Two loose ends belonging to other slices: `dataset/tools/meas/desktop/run.sh` line 162 still reads `app.affinity` at launch (9.8's file), and `.github/workflows/meas-gui.yml` retires when `system-daemon`'s own measurement replaces its values (9.9's).
