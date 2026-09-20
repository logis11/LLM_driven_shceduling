# Handoff — task 9.5 Interactive and typing (2026-09-20, 11:25 UTC)

Reopened by 9.6 D10 and 9.7 D3 (`_dev/TODO.md` 9.5's two `[WIP]` sub-items: same-machine repeats, and Thunderbird re-observed with a `send` operation). Branch `jioh/dataset-rebuild`; everything below is committed and pushed. Decision record `_dev/research/jioh/task-9.5-interactive-typing/changelog.md` (now D1–D58), method `campaign/method.md` (§9 carries every amendment), workflow `_dev/research/jioh/measurement-campaign-workflow.md`, record `_dev/research/jioh/measurement-campaign-record.md`.

## Where the nine archetypes stand

| application | archetype | repeats | rule | pool |
|---|---|---|---|---|
| `soffice` | `office-writer` | 14 | **holds** | `--since 38` |
| `gimp` | `image-editor` | 5 | **holds** | `--since 10` |
| `kdenlive` | `video-editor` | 20 | **holds** | `--since 10` |
| `mpv-video` | `video-player` | 24 | **holds** | `--since 10` |
| `mpv-audio` | `audio-player` | 31 | **holds** | `--since 10` |
| `thunderbird-send` | `mail-client` | 43 | **holds** | `--since 150 --exclude 29 --exclude-why "…"` |
| `chrome` | `web-browser` | 5 | not yet | `--since 269 -- --exclude-roles renderer` |
| `code` | `code-editor` | 7 | not yet | `--since 245` |
| `webrtc` | `video-call` | 12 | not yet | `--since 245` |

The six that hold are pooled into `campaign/results-same-machine/` with `campaign/results-same-machine.md` rendered over them, and their rows are in `measurement-campaign-record.md`. The three that do not are the 2026-09-20 campaign, launched after three long-phase probes changed their protocol.

## What the probes changed (D50–D58)

- `chrome` (D51, D56, D58): settle 30 → 270 → **420 s**, idle phase 120 → **600 s**. Its ~880 ms `ThreadPoolForeground` launch run lands 95–300 s after the window over seven sessions; at 270 s one repeat of five still caught it (95.4 ms/s in one slice). Its earlier repeats are superseded whole, driven values included (D55).
- `code` (D53): settle stays 30 s, idle phase 120 → **900 s**. A 25–40 ms/s episode recurs every ~320 s, anchored to launch, so a 120 s phase read idle CPU 15.5 % high in every repeat.
- `webrtc` (D54): settle 30 → **210 s**, play phase 300 → **480 s**. Its call saturates one CPU for ~30 s every 240 s to the call's end; the old 300 s phase sat in the ramp-up and read play CPU **78 %** above the steady call. Its CPU share is now 0.226–0.255 against the superseded 0.4084.

## Two exceptions to the stability rule, beside 9.6 D29's

- **D46** — `thunderbird-send`'s operation and per-input values pool its eight full repeats and state their half-widths, past the recording's window limit.
- **D57** — a component whose rate varies between sessions rather than within a run is carried with its half-widths: `code`'s `libuv-worker` (`SESSION_SPREAD` in `campaign/pool.py`). The test that placed it: the rate moves ±8.7 % within the probe's run against 5.09–9.24 a second across repeats. Its projection fell from 107 repeats to 29. The sensitivity question is on 9.14's TODO line.

## The loop, as run

Per landing: pool (`loop/pool_runs.py <family>/<app> --since N` with the arguments in the table), read the D35 slice profile where a settle applies, then `loop/launch.py added <family>/<app>:<k>` once and check the commit reached origin. One added repeat per application at a time; a **first batch's** gated indices go back in one push (`launch.py retried …`, 인지오's 2026-09-20 amendment, workflow step 2, commit `a95a9a9`). Before every launch check `.github/campaign.json` has `"mode": "full"`. Watch with `loop/watch.py <targets> --since <run of the latest launch> --poll 60`; it exits at the first landing, so restart it after each.

## In flight at 11:25 UTC

`chrome` 6 (interactive run #278), `code` 8 not yet launched (its repeat 7 pool was running at the cutoff), `webrtc` 13 (playback run #282).

## What is open

1. **`webrtc` may not converge.** Its projection has gone 24 → 39 → 53 → 55 over four repeats. The driver is the audio path: `AudioOutputDevi` wakes 105–120 a second in nine repeats and 156 in two, `AudioProcessing` 106–178. Within the D52 probe's single call those rates move ±4.6 % and ±2.8 %, so the spread is between sessions — the D57 shape. It is **not** exempted: those two threads are ~12 % of the phase's wakes and they are what a video call does, where `libuv-worker` was peripheral. Decision taken: keep running, and bring the exception to 인지오 with this evidence if the projection is still climbing at about 30 repeats. A longer play phase is not an option — the within-call variation is already small.
2. **The releases and the fold-in wait for all three** (D55). Two releases, one per campaign: 2026-09-18/-09-19 for the six, 2026-09-20 for the three. Both are outward-facing — ask 인지오 first. Then one fold-in (`campaign/fold_in.py`), then `make -C dataset dataset lint test check PY=python3.12` (five `-single` files fail the demand-window lint until 9.14 — state it).
3. **At the fold-in**, `mail-client`'s notes must carry the runner's attachment figures — 41,555,063 B and 56,946,735 B at the peer — not D31's container build (9.7's D49).

## Pitfalls met

- **A repeat launched without its window cut** runs the driven branch against a missing file, skips `driven-alt` and runs the operation from another application state: that is `thunderbird-send` repeat 29, excluded under **D47** (`pool_runs.py --exclude K --exclude-why TEXT`, artifact moved to `<pool folder>-excluded`). Cut windows first (`loop/cut_windows.sh N`) for any recorded-input application.
- **Superseded repeats share indices with new ones.** Pool from the new campaign's first run (`chrome`: `--since 269`), never by excluding indices.
- **The shared working tree** holds 9.6, 9.7 and 9.8 sessions. `push_trigger` and `cut_windows.sh` now commit only their own paths (`903a76b`, `75d873c`), but a session's unpushed commits are replayed by whoever pulls next — one such rebase conflict in `_dev/TODO.md` landed here and was resolved by taking 9.8's rewrite whole.
- **`launch.py` is never retried in a loop**: its push can succeed while the run listing after it fails.
- **The detached loop** (`~/.cache/meas-loop/overnight-9.5/loop.py`, its state in `state.json`, log `loop.log`) survives the session but not a reboot — the Mac restarted at 22:59 UTC on 2026-09-19 and killed it. Before reusing it for `chrome` it needs pool passthrough arguments, since `chrome` pools with `--exclude-roles renderer`.

## 인지오's working rules

Questions one at a time in plain chat, each with a recommendation and its reference; every label explained where it appears; no number without a reference; decisions framed on research reliability, not effort. Report applications as name, repeats, whether the rule holds — numbers only when they are the basis of a decision. The loop's added repeats and relaunches are approved standing; a new campaign or a release is asked first.
