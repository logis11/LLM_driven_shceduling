# Handoff — task 9.5 Interactive and typing (2026-09-22, 12:45 UTC)

Same-machine repeats sub-item. Branch `jioh/dataset-rebuild`; everything below is committed and pushed. Decision record `_dev/research/jioh/task-9.5-interactive-typing/changelog.md` (now D1–D66), method `campaign/method.md` (§9 carries every amendment), workflow `_dev/research/jioh/measurement-campaign-workflow.md`.

## Where the nine archetypes stand

| application | archetype | repeats | rule | pool arguments (`loop/pool_runs.py`) |
|---|---|---|---|---|
| `soffice`, `gimp`, `kdenlive`, `mpv-video`, `mpv-audio`, `thunderbird-send` | six archetypes | — | **hold** | filed in `campaign/results-same-machine/` |
| `webrtc` | `video-call` | 35 | **holds** (D59) | `playback/webrtc --since 245` |
| `code` | `code-editor` | 25 (windows 1–4, 6–26; window 5 left out, D63) | **holds** (2026-09-22) | `interactive/code --since 376 --exclude 5 --exclude-why "D63: after the D61 prelude the caret stood on line 16, not at the file's end (screenshot after-altprelude), so the 136M phase typed mid-file"` |
| `chrome` | `web-browser` | 18 under D65 (windows 1–18) | not yet, projection 42 | `interactive/chrome --since 438 --exclude 16@35712250969 --exclude-why "D66: window 16 measured twice — one push started runs #474 and #475, #475's copy was gated and the watcher relaunched it as #476 while #474's copy measured; the original launch's copy (#474) is kept" -- --exclude-roles renderer` |

`chrome`'s three failing values at 18: idle `Chrome_ChildIOT` gap mean ±7.7 % (42 needed; its gap sits at 397–459 ms in 14 repeats, ~250 in windows 14–15 and 334 in window 8 — the per-thread pooling of a four-thread component, kept by 인지오's decision), SWELL-KW `input_run` ±6.9 % (34), 136M `input_run` ±5.7 % (24). Every other value passes, the `MemoryInfra` residual included (D64).

## Resume point

**In flight: `chrome` window 19, run #481 (35728483709).** Nothing else. `code` and `webrtc` add no repeats.

1. `python3 dataset/tools/meas/loop/status.py interactive --since 480 --app chrome:481` — landed / in flight / gated.
2. On its landing: pool with the arguments above and run the per-landing checks below; if valid and the rule does not hold, `launch.py added interactive/chrome:20` (check `.github/campaign.json` is `"mode": "full"` first), then watch with `watch.py interactive/chrome --since <that run> --app chrome:<that run> --poll 60`.
3. When `chrome`'s rule holds: stop launching; then the D55 end work below.

## Per-landing checks (`chrome`, beyond `pool_runs.py`'s validity lines)

Each repeat's artifact is `~/.cache/meas-loop/pool/interactive-chrome-from438/<run id>/meas-interactive-chrome-r<k>-full/`.

- `report.json`: `stream_kinds` is `key` (D65); `altprelude.rc` is `0`; `app.affinity` is `8` with `app.affinity_pid` set.
- `after-driven.png`: the text box (dark left border at x 19, y 170–340) holds the stream's text — dark pixels inside x 25–835, y 168–340.
- `after-altprelude.png`: the box at the page's top (border present) and empty (no dark pixels inside) — D60, D62.
- Idle guard (D58): `python3 dataset/tools/meas/campaign/slices.py <artifact> --phase idle --exclude-roles renderer` — every 10 s slice under ~10 ms/s (clean repeats peak 2.2–8.7; the launch run shows ~95).
- Only one copy of the window landed (`ls -d …/*/meas-interactive-chrome-r<k>-full | wc -l` is 1); a second copy is D66's case — keep the original launch's, `--exclude K@<run id>` the other.

## Decisions of 2026-09-21/22 (all applied)

- **D59** — `webrtc`'s audio path carried with its half-widths under D57 (within one call ±0.7–3.0 %, across repeats ±26–41 %); rule holds at 35; all 35 repeats reviewed.
- **D60 → D62** — `chrome`'s 136M phase starts with the page at the top and the text box focused and empty.
- **D61, D63** — `code`'s 136M phase starts from the committed `index.ts`; window 5 left out (caret mid-file); the prelude's keys hardened.
- **D64** — `MemoryInfra`'s heavy pass (runs ≥ 30 ms in `chrome`'s idle phase; 54–61 ms, about one per 30 minutes) carried as its own stated event (`HEAVY_EVENTS`, `split_events` in `campaign/pool.py`; the pooled record's `heavy_event`), so the residual converges. **Still to write: its place in `fold_in.py`.**
- **D65** — `chrome`'s SWELL-KW phase replays keys only (`KINDS="key"`), the stream's clicks and drags having moved focus or selected page text; browsing's scrolling and clicking a stated limitation. `chrome` restarted from window 1 at run #438.
- **D66** — window 16 measured twice by a duplicated run (one push started #474 and #475); the original launch's copy kept. `watch.py` no longer relaunches a gated window another run from five before holds (`holder`); `pool_runs.py --exclude K@RUNID`.
- `Chrome_ChildIOT`'s gap stays per-thread (option (a)); `code`'s window-10 compositor rate stays a watch item (one session of 25; not repeated since).
- `run.sh` records `app.affinity` from the window owner's process.

## At the end (D55)

The three re-measured applications are filed together: each pool's `pooled.json` and `results.md` into the slice's `campaign/` folder, rows into `measurement-campaign-record.md`; then the releases (2026-09-18/-19 for the six, 2026-09-20 for the three — outward-facing, ask 인지오 first); then one fold-in (`campaign/fold_in.py`, with D64's event written in first) and `make -C dataset dataset lint test check PY=python3.12` (five `-single` files fail the demand-window lint until 9.14 — state it). `mail-client`'s notes carry the runner's attachment figures (41,555,063 B and 56,946,735 B at the peer). `dataset/tools/meas/desktop/run.sh` line 162 still reads `app.affinity` at launch — 9.8's file.

## Running the loop

In-session only, one session at a time (on 2026-09-21 a lost terminal left the original session running beside its restore until one stood down). Relaunches: `watch.py` handles gated jobs itself; a first batch's gated windows go back in one push (`launch.py retried …`); a job that FAILED is relaunched by hand. Push doc edits only while no watcher runs (a watcher's relaunch push and a doc push raced once). Push with `git pull --rebase --autostash` — other sessions keep unstaged edits in the shared tree. Each `chrome` repeat is ~49 min on the runner, ~55 min per cycle with launch and gated draws.
