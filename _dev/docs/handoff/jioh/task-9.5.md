# Handoff — task 9.5 Interactive and typing (2026-09-21, 22:45 UTC)

Same-machine repeats sub-item. Branch `jioh/dataset-rebuild`; everything below is committed and pushed. Decision record `_dev/research/jioh/task-9.5-interactive-typing/changelog.md` (now D1–D63), method `campaign/method.md` (§9 carries every amendment), workflow `_dev/research/jioh/measurement-campaign-workflow.md`.

## Where the nine archetypes stand

| application | archetype | repeats | rule | pool |
|---|---|---|---|---|
| `soffice`, `gimp`, `kdenlive`, `mpv-video`, `mpv-audio`, `thunderbird-send` | six archetypes | — | **hold** | filed in `campaign/results-same-machine/` |
| `webrtc` | `video-call` | 35 | **holds** (D59) | `playback/webrtc --since 245` |
| `code` | `code-editor` | 17 valid (windows 1–4, 6–18; window 5 left out, D63) | not yet, projection 22 | `interactive/code --since 376 --exclude 5 --exclude-why "D63: …"` |
| `chrome` | `web-browser` | 16 | not yet, projection over 200 (the `MemoryInfra` residual) | `interactive/chrome --since 379 -- --exclude-roles renderer` |

## What changed on 2026-09-21

- **D59** — `webrtc`'s audio path (`AudioProcessing` whole; run means of `AudioOutputDevi`, `AudioInputDevic`, `FakeAudioInput`, residual) carried with half-widths under D57: within one call ±0.7–3.0 %, across repeats ±26–41 %. Rule holds at 35. All 35 repeats reviewed: one protocol (210/480), gate open, every Chrome row on CPU 3, two saturation episodes at 130–150 and 370–390 s in every play phase. Sensitivity question on 9.14's TODO line.
- **D60 → D62** — `chrome`'s 136M phase starts from a fixed state: page at the top, text box focused and emptied (the page as generated). The SWELL-KW window before it had left the box scrolled away in 10 of 15 repeats (keys to a page that takes no text) and, under D60, holding the stream's text. Both earlier campaigns superseded whole; `chrome` restarted from window 1 at run #379.
- **D61, D63** — `code`'s 136M phase starts from the committed `index.ts` (pristine copy restored, buffer reverted with a bound File: Revert File key, caret at the end); the SWELL-KW window had left 36–142 errors in the file. 18 repeats superseded, restarted from window 1 at run #376. Window 5 left out under D47 (caret on line 16 after the prelude); the prelude's keys now carry `--clearmodifiers`, Escape again, Ctrl+End twice.
- `run.sh` records `app.affinity` from the window owner's process (`app.affinity_pid`) — read at launch it could catch `taskset` before the mask applied.

## Per-landing checks (beyond `pool_runs.py`'s validity lines)

- `chrome`: `after-altprelude.png` — box at the page top, focused, empty; idle slice profile (D58 guard) — no ~95 ms/s launch run.
- `code`: `after-altprelude.png` status bar — Ln 28, Col 1, 0 errors; idle profile starts 17–19 ms/s, peaks ~40 (D53's episode, expected).

## Decided 2026-09-21, not yet applied

1. **`MemoryInfra`'s heavy pass is carried as its own stated event** (인지오, option (b)): the archetype states the pass's rate and size with their counts (so far 9 passes in 20 sessions × 600 s, 54–61 ms), and `chrome`'s idle residual is read without it so it can converge. To apply: a changelog entry (D64), the pass's extraction in `campaign/pool.py`, its place in `fold_in.py`, method §9.

## Open for 인지오

**`chrome`'s idle residual run mean (±69 % at 6 repeats, projection over 200).** It is one thread, `MemoryInfra`. In every one of 20 sessions (both superseded and current campaigns) it runs ~7.7 ms at 180–183 s and 480–483 s into the idle phase, a fixed 300 s cadence. In 7 of 20 sessions it also runs a heavy pass of 54–61 ms at no fixed time (43, 57, 165, 217, 473, 474, 503, 572, 593 s) — 9 passes in 20 × 600 s, about one per 22 minutes. A rare random event within the run, not a harness defect nor a between-session spread; at that rarity the mean needs over 200 repeats. Options to decide: a longer idle phase; carry the heavy pass as its own stated event (rate and size); or an exception. Repeats continue meanwhile. (Script: the session scratchpad's `memoryinfra.py`; analysis reproducible with `analyze_run` on the idle phase, `comm == "MemoryInfra"`, run > 5 ms.)

**`code`'s idle compositor rate in window 10 (watch, not yet a question).** Window 10's `VizCompositorThread` wakes 16.2 a second over its idle phase against 22.3–24.4 in the other eight pooled repeats, `Chrome_ChildIOT` 15.7 against 20.2–22.7; lower from launch through the whole phase (about 18 a second per minute against 24 in window 9, dipping to 13 on the ~320 s cadence of D53's episode). Same VS Code 1.138.0, Node, machine; screenshots before and after idle identical to the other repeats. It moved the projection from 21 to 40. The D57 shape (a rate varying between sessions) on one repeat of nine; the loop keeps adding repeats — if more sessions show it, it is a D57 question for 인지오.

**`chrome`'s SWELL-KW per-input value and the page state the replayed browsing leaves (a D12 design question).** D12 keeps Internet Explorer's clicks, drags and wheel turns with the keys for `web-browser`; on this page (a text box over 400 paragraphs) they can move focus off the box or select page text, and the keys then cost differently. Window 12 (run 35634845510) ended its SWELL-KW phase with paragraphs 24–28 selected (3,055 highlighted pixels in `after-driven.png`, against 0–146 in windows 1–11) and gave 3.02 ms per input against 1.49–2.38 — moving the value's projection from 43 to 89. Across windows 1–11 the value does not split by whether the box is in view (1.77–2.38 with it, 1.49–2.30 without), so until window 12 it read as a spread the input makes. Kept pooled — valid under the present design; whether `web-browser`'s typing phase should replay keys only (as D28 did for `office-writer`) or keep browsing's pointer events is 인지오's.

**`chrome`'s idle `Chrome_ChildIOT` gap mean (an analysis question, D33's kind).** Over 15 repeats its wake rate holds at 7.45–7.96 a second while its gap mean spans 247–455 ms (projection 35 at 15). The component is four threads and the gap mean pools each thread's own gaps, so the same wakes split differently across the four move the mean without any change in the component's work. Whether the component's gap should be read over its merged wake times (as the residual's is) is 인지오's.

## Still to do at the end (unchanged)

The releases (2026-09-18/-19 for the six, 2026-09-20 for the three) and one fold-in wait for all three (D55); both releases are outward-facing — ask first. `mail-client`'s notes carry the runner's attachment figures (41,555,063 B and 56,946,735 B at the peer). `dataset/tools/meas/desktop/run.sh` line 162 still reads `app.affinity` at launch — 9.8's file.

## Resume point (the Mac may go down)

In flight at 22:45 UTC: `chrome` window 17 (run #437, 35663725760) and `code` window 19 (run #436, 35662756973; its first attempt, run #435, was gated and then failed a 403 on the artifact upload — nothing measured). Both land on GitHub whatever the Mac does. On resume: `status.py interactive --since 436 --app chrome:437 --app code:436`, pool and check each landing (the per-landing checks above; the session scratchpad's `check.sh` does not survive a restart — its steps are `pool_runs.py` with the pool arguments in the table, `report.json`'s `altprelude.rc`, the `after-altprelude.png` test, and `campaign/slices.py <run dir> --phase idle`), then launch `chrome` 18 and `code` 20.

## Running the loop

In-session, no detached loop. Watch with `loop/watch.py interactive/chrome interactive/code --since <latest launch run> --app chrome:<run> --app code:<run> --poll 60`; it exits at the first landing. One added repeat per application at a time; a first batch's gated windows go back in one push (`launch.py retried …`). Check `.github/campaign.json` is `"mode": "full"` before each launch; push with `git pull --rebase --autostash` (other sessions keep unstaged edits in the shared tree). Only one session may run this loop — on 2026-09-21 the original session survived a lost terminal and two copies ran at once until one stood down.
