# Measured values — campaign record

Every campaign behind a measured archetype value: per archetype the repeats, the values the rule covers, the widest margin among them, why it stopped, and the machine draws it took. Method: `measurement-campaign-workflow.md`. Each row regenerates with `dataset/tools/meas/loop/pool_runs.py <family>/<app> --since 10` (`soffice`: `--since 38`; `thunderbird-send`: `--since 150 --exclude 29`); job counts are the campaign runs' jobs, read from their job lists. Recorded 2026-09-20; the 9.5 rows were first recorded a day earlier against one headline median per archetype, which D29 and D30 replaced.

## Campaigns

All on GitHub-hosted `ubuntu-24.04` runners, 4 vCPU, pinned to one CPU, AMD EPYC 7763 only (machine gate); kernel `6.17.0-1022-azure` in every repeat of the build campaign and of all six 9.5 applications whose rule holds (their pooled records carry it per repeat). Stability rule (D29, D30): for every value the fold-in carries, each table by its per-repeat mean, the 95 % confidence half-width of the across-repeat mean is at most 5 % of it or 1 µs, whichever is larger, over at least five same-machine repeats (`dataset/tools/meas/stability.py`). A value whose phase holds the recorded input's last window is reported with its half-width instead, and left out of the rule (D32, D46).

| tag | slice | workflow | runs | first launch |
|---|---|---|---|---|
| `meas-ci:build:2026-09-18` | 9.6 | `meas-build.yml` | #10–#37; the 13 holding a landed repeat are #10, #11, #12, #15, #16, #22, #25, #26, #27, #29, #30, #32, #34 | 2026-09-18 09:09 UTC |
| `meas-ci:interactive:2026-09-18` | 9.5 | `meas-interactive.yml` | #10–#100 | 2026-09-18 09:56 UTC |
| `meas-ci:playback:2026-09-18` | 9.5 | `meas-playback.yml` | #10–#84 | 2026-09-18 09:56 UTC |
| `meas-ci:interactive:2026-09-19` | 9.5 | `meas-interactive.yml` | #150–#244, `thunderbird-send` alone (the `send` re-observation) | 2026-09-19 11:18 UTC |
| `meas-ci:background:2026-09-19` | 9.7 | `meas-background.yml` | #19–; `borg`'s repeats are in #24–#40 | 2026-09-19 23:16 UTC |
| `meas-ci:interactive:2026-09-20` | 9.5 | `meas-interactive.yml` | #245–, `chrome` and `code` re-measured under D51 and D53 | 2026-09-20 08:04 UTC |
| `meas-ci:playback:2026-09-20` | 9.5 | `meas-playback.yml` | #245–, `webrtc` re-measured under D54 | 2026-09-20 08:04 UTC |

## 9.5 — six archetypes measured, three being re-measured

The six whose rule holds, pooled in `task-9.5-interactive-typing/campaign/results-same-machine/` and rendered in `campaign/results-same-machine.md`. Every repeat on one AMD EPYC 7763, kernel `6.17.0-1022-azure` in all of them. `values` counts what the rule covers; `widest` is the largest half-width among them.

| archetype | application | repeats | values | widest | stopped by | jobs (gated) | recorded input covered |
|---|---|---|---|---|---|---|---|
| `office-writer` | `soffice` | 14 (windows 1–14) | 5 | idle `soffice.bin` run mean ±4.93 % | the rule | 19 (5) | SWELL-KW Word, participants 1–6 |
| `mail-client` | `thunderbird-send` | 43 (windows 1–28, 30–44) | 36 + 39 reported at the window limit | idle `StreamTrans` gap mean ±5.00 % | the rule | 77 (32) | SWELL-KW Outlook, all 25 participants; windows 9 on are past the recording |
| `image-editor` | `gimp` | 5 (1, 2, 3, 5, 6) | 10 | op `gimp` wakes/s ±4.59 % | the rule | 8 (3) | scripted pointer loop |
| `video-editor` | `kdenlive` | 20 (1–3, 5–21) | 22 | driven `kdenlive` run mean ±4.94 % | the rule | 30 (10) | scripted pointer loop |
| `video-player` | `mpv-video` | 24 (1, 2, 4, 6–26) | 16 | play `vo` wakes/s ±4.98 % | the rule | 51 (27) | none |
| `audio-player` | `mpv-audio` | 31 (1–31) | 16 | play `ao` run mean ±4.93 % | the rule | 55 (24) | none |

The typing-driven applications also replay the 136M Keystrokes windows 1…k of their own repeats in the `driven-alt` phase (the pre-registered stimulus check).

- `office-writer`: the first design's five repeats (the stream's clicks, scrolls and drags replayed with the keys; `input_run` p50 8.67, 3.99, 5.91, 4.53, 4.21 ms, ±44 %) are superseded by D28 and not pooled; their 11 jobs, 6 of them gated, are not in the count above.
- `mail-client`: it took 43 repeats against the 29 first projected, because its idle phase holds a ~60 s `StreamTrans` episode that comes out big 6 to 9 times per 600 s window against 10 cycles, which kept the idle `StreamTrans` gap mean at the top of the tolerance. Window 29 is left out of the pool (D47), its Outlook window having been launched uncut; 77 jobs counted here exclude that repeat's job, one cancelled duplicate and one dry check. The operation's 39 values are reported with their half-widths over the eight full repeats, the recording's last window (D46).
- `video-player`: its `vo` thread's projection swung between 24 and 31 repeats over ten repeats before settling; the rule held at 24.
- `image-editor`, `video-editor`, `video-player`: the windows the gate stopped (4; 4; 3 and 5) were not retried once the rule held.

Three applications are re-measured under the campaign launched 2026-09-20, their present values superseded (D55):

| archetype | application | why | replaces |
|---|---|---|---|
| `web-browser` | `chrome` | its 30 s settle left the launch burst in the idle phase, about 35 times the steady level; settle now 270 s (D51) | 5 repeats, page-load duration p50 472.7 ms |
| `code-editor` | `code` | a launch-anchored episode every ~320 s put its idle CPU 15.5 % above the long-run level at the placement every repeat takes; idle phase now 900 s (D53) | 22 repeats, `input_run` p50 74.69 ms |
| `video-call` | `webrtc` | the call's saturation recurs every 240 s, so a 300 s play phase measured the ramp-up and read CPU 78 % above the steady call; settle 210 s, play phase 480 s (D54) | 5 repeats, play-phase CPU share 0.4084 |

`mail-client` was `thunderbird` (8 windows, `input_run` p50 4.325 ms, ±8.47 %, stopped by the input's end) until the `send` re-observation replaced it whole (9.7 D3, D36).

## 9.6 — three archetypes, one campaign

Repeats 4, 5, 7, 8 and 9–18 on the AMD EPYC 7763 (14 repeats; repeats 1, 2, 3, 6 gated). 28 jobs: 14 landed, 12 stopped by the machine gate, 2 cancelled (repeat 19, launched before the campaign ended, measured nothing). Every value is an across-repeat mean, each table by its per-repeat mean (D26). Two conditions changed mid-campaign: `clamscan` reads a fixed signature database from repeat 9 (D27) and `python3` starts warm from repeat 11 (D28), so those two pool fewer repeats.

| archetype | program | headline | repeats | mean | spread (cv) | 95 % half-width | stopped by |
|---|---|---|---|---|---|---|---|
| `build-orchestrator` | `make` | dispatch run, warm `-j8` | 14 | 690.8 µs | 1.6 % | ±0.94 % | the rule |
| `compiler-child` | `cc1` | CPU per process, warm `-j8` | 14 | 435.0 ms | 1.4 % | ±0.78 % | the rule |
| `cpu-batch` | `clamscan` | runs between voluntary blocks | 10 | 8.893 ms | 2.1 % | ±1.47 % | the rule |
| `cpu-batch` | `ffmpeg` | runs between voluntary blocks | 14 | 1.520 ms | 0.9 % | ±0.53 % | the rule |
| `cpu-batch` | `HandBrakeCLI` | runs between voluntary blocks | 14 | 1.087 ms | 0.8 % | ±0.47 % | the rule |
| `cpu-batch` | `python3` | runs between voluntary blocks | 8 | 1.616 s | 12.0 % | ±10.04 % | carried (D29) |
| `cpu-batch` | `tracker-miner-fs-3` | runs between voluntary blocks | 14 | 406.5 µs | 1.4 % | ±0.83 % | the rule |

The rule holds over 29 of the 33 values. Four are carried with their half-widths under the rule's exception for a value whose spread follows the machine (D29), all of them `cpu-batch` blocks on the runner's disk: `clamscan` block per run 218.1 µs ±9.5 % over 10 repeats (182–274), `python3` block per run 220.0 µs ±14.0 % over 8 (170–286) and its runs between blocks above, `tracker-miner-fs-3` block per run 17.6 µs ±15.1 % over 14 (13.3–30.4).

Also within the rule: the object job's 11 per-step CPU tables (±0.7–1.4 %), CPU per process of the other five roles (±0.8–1.4 %), each bound program's share of CPU past the boot slice (±0.02–1.4 %), and the encoders' block means, which sit inside the trace's 1 µs floor (`ffmpeg` 0.35 µs, `HandBrakeCLI` 8.90 µs).

Full tables: `task-9.6-compile/campaign/results.md`, `campaign/results/pooled.json`.

## 9.7 — `file-backup` and `file-archiver`

Repeats 1–31 on the AMD EPYC 7763, repeat 3 left out of the pool: it landed, but its 10 GB set fetched as a 12,108 B file in place of the 3.70 GB archive (`set.archive_pin` mismatch, extract rc 2, 0 files), so its phases ran on an empty tree and the validity step fails it (the loop, step 4). 55 jobs: 31 landed, 24 stopped by the machine gate, none on another model. The rule is read over the other 30 repeats, and holds on all three of `file-backup`'s values.

| archetype | program | value | repeats | mean | spread (cv) | 95 % half-width | stopped by |
|---|---|---|---|---|---|---|---|
| `file-backup` | `borg` | run per wake, warm first backup | 30 | 15.182 ms | 10.2 % | ±3.91 % | the rule |
| `file-backup` | `borg` | wait per wake, warm first backup | 30 | 3.128 ms | 12.8 % | ±4.87 % | the rule |
| `file-backup` | `borg` | disk wait per wake, warm first backup | 30 | 3.157 ms | 12.7 % | ±4.84 % | the rule |
| `file-archiver` | `7z` | run per wake, warm eight-thread run | 6 | 4.187 ms | 2.1 % | ±2.17 % | the rule |
| `file-archiver` | `7z` | wait per wake, warm eight-thread run | 6 | 32.232 ms | 2.3 % | ±2.40 % | the rule |

`file-archiver`'s first batch of six repeats holds the rule, every repeat valid: 14 jobs, 8 gated draws, none on another model. Its D15 check, the single-thread run against the eight-thread run, is reported by its CPU per byte (0.91–0.96 of the eight-thread run in every repeat); the check's per-wake parts split into two modes of the same thread, 940 wakes at a 0.36–0.38 s median gap in repeats 1, 2 and 6 against 1,246–1,575 wakes at 0.4–0.7 ms in repeats 3, 4 and 5, and both are stated in the archetype's notes.

`game-download` (SteamCMD) has no values yet: its operating point is open — the number of content servers its runner draws sets every value on its list (run 35475239657: 6 servers 4.73 % of packets dropped and 4,070 B a wake, one server forced 0.0005 % and 2,131 B, 6 servers again 4.97 % and 4,137 B).

Full tables: `task-9.7-background-io/campaign/results-borg.md` and `campaign/results-7z.md`, `campaign/results/borg-pooled.json` and `results/7z-pooled.json`.

## Machine draws

The build campaign, complete: 28 jobs, 14 on the AMD EPYC 7763 (50.0 %), 12 stopped by the machine gate — Intel Xeon Platinum 8573C 4, AMD EPYC 9V74 4, AMD EPYC 9V45 2, Intel Xeon Platinum 8370C 1, Intel Xeon 6973P-C 1 — and 2 cancelled.

The 9.5 campaigns of 2026-09-18 and 2026-09-19, over the six applications whose rule holds and complete for them: 252 jobs — 144 landed on the AMD EPYC 7763 (57.1 %, one of them `thunderbird-send`'s dry check), 107 stopped by the gate, 1 cancelled. The model is recorded for 104 of those stops, the reports the loop read: AMD EPYC 9V74 47, Intel Xeon Platinum 8573C 19, AMD EPYC 9V45 18, Intel Xeon 6973P-C 12, Intel Xeon Platinum 8370C 8. Per application, gate stops: `thunderbird-send` 32, `mpv-video` 27, `mpv-audio` 24, `soffice` 11 (5 of them in the pooled campaign, 6 in the superseded first design), `kdenlive` 10, `gimp` 3. The 2026-09-20 campaign re-measuring `chrome`, `code` and `webrtc` is still running.
