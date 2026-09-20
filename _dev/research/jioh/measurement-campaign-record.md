# Measured values — campaign record

Every campaign behind a measured archetype value: per archetype the headline median, the repeats, the margin the stability rule reached, why it stopped, and the machine draws it took. Method: `measurement-campaign-workflow.md`. Each row regenerates with `dataset/tools/meas/loop/pool_runs.py <family>/<app> --since 10` (`soffice`: `--since 38`); job counts are the campaign runs' jobs (`status.py`). Recorded 2026-09-19.

## Campaigns

All on GitHub-hosted `ubuntu-24.04` runners, 4 vCPU, pinned to one CPU, AMD EPYC 7763 only (machine gate); kernel `6.17.0-1022-azure` in every repeat of the build campaign, `code`, `soffice`, `mpv-audio` and `webrtc` (the pools read for this record; the others' kernels are in their pooled records). Stability rule: 95 % confidence half-width of the across-repeat mean of each headline median at most 5 % (`dataset/tools/meas/stability.py`).

| tag | slice | workflow | runs | first launch |
|---|---|---|---|---|
| `meas-ci:build:2026-09-18` | 9.6 | `meas-build.yml` | #10–#37; the 13 holding a landed repeat are #10, #11, #12, #15, #16, #22, #25, #26, #27, #29, #30, #32, #34 | 2026-09-18 09:09 UTC |
| `meas-ci:interactive:2026-09-18` | 9.5 | `meas-interactive.yml` | #10–#100 | 2026-09-18 09:56 UTC |
| `meas-ci:playback:2026-09-18` | 9.5 | `meas-playback.yml` | #10–#84 | 2026-09-18 09:56 UTC |
| `meas-ci:background:2026-09-19` | 9.7 | `meas-background.yml` | #19–; `borg`'s repeats are in #24–#40 | 2026-09-19 23:16 UTC |

## 9.5 — one headline median per archetype

| archetype | application | headline median | repeats (windows) | mean | spread (cv) | 95 % half-width | stopped by | jobs (gated) | recorded input covered |
|---|---|---|---|---|---|---|---|---|---|
| `office-writer` | `soffice` | `input_run` p50, keys only (D28) | 5 (1–5) | 3.327 ms | 3.13 % | ±3.89 % | the rule | 6 (1) | SWELL-KW Word, participants 1–2 |
| `code-editor` | `code` | `input_run` p50 | 22 (1–22) | 74.69 ms | 10.82 % | ±4.83 % | the rule | 35 (13) | SWELL-KW Word, participants 1–11 of 25 |
| `mail-client` | `thunderbird` | `input_run` p50 | 8 (1–8) | 4.325 ms | 10.13 % | ±8.47 % | the input's end (D26) | 11 (3) | SWELL-KW Outlook, all 25 participants |
| `web-browser` | `chrome` | page-load duration p50 | 5 (1–5) | 472.7 ms | 3.35 % | ±4.16 % | the rule | 11 (6) | SWELL-KW Internet Explorer, participants 1–5 |
| `image-editor` | `gimp` | unsharp-mask duration p50 | 4 (1, 2, 3, 5) | 2 365.0 ms | 1.14 % | ±1.81 % | the rule | 6 (2) | scripted pointer loop |
| `video-editor` | `kdenlive` | preview-render duration p50 | 4 (1, 2, 3, 5) | 11 486.4 ms | 1.02 % | ±1.62 % | the rule | 10 (6) | scripted pointer loop |
| `video-player` | `mpv-video` | play-phase CPU share | 3 (1, 2, 4) | 0.1235 | 1.59 % | ±3.96 % | the rule | 8 (5) | none |
| `audio-player` | `mpv-audio` | play-phase CPU share | 29 (1–29) | 0.0072 | 12.72 % | ±4.95 % | the rule | 53 (24) | none |
| `video-call` | `webrtc` | play-phase CPU share | 5 (1–5) | 0.4084 | 2.34 % | ±2.91 % | the rule | 7 (2) | none |

The four typing-driven applications also replay the 136M Keystrokes windows 1…k of their own repeats in the `driven-alt` phase (the pre-registered stimulus check).

- `office-writer`: five repeats of the first design (runs #10–#28, the stream's clicks, scrolls and drags replayed with the keys; `input_run` p50 8.67, 3.99, 5.91, 4.53, 4.21 ms, ±44 %) are superseded by D28 and not pooled; 11 jobs, 6 gated.
- `mail-client`: SWELL-KW's Outlook conditions hold 4 761 s of recorded time — eight windows, the eighth 561 s; the half-width is stated as it is.
- `code-editor`: windows 1–10 average 79.8 ms, windows 11–20 69.6 ms; the later participants type more keys per window.
- `audio-player`: the CPU share is 0.58–0.86 % of one CPU while the wake rate stays at 206–211 per second.
- `video-player`, `image-editor`, `video-editor`: the windows the gate stopped (3 and 5; 4; 4) were not retried once the rule held.

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

## 9.7 — `file-backup`, the campaign's first archetype

Repeats 1–31 on the AMD EPYC 7763, repeat 3 left out of the pool: it landed, but its 10 GB set fetched as a 12,108 B file in place of the 3.70 GB archive (`set.archive_pin` mismatch, extract rc 2, 0 files), so its phases ran on an empty tree and the validity step fails it (the loop, step 4). 55 jobs: 31 landed, 24 stopped by the machine gate, none on another model. The rule is read over the other 30 repeats, and holds on all three of `file-backup`'s values.

| archetype | program | value | repeats | mean | spread (cv) | 95 % half-width | stopped by |
|---|---|---|---|---|---|---|---|
| `file-backup` | `borg` | run per wake, warm first backup | 30 | 15.182 ms | 10.2 % | ±3.91 % | the rule |
| `file-backup` | `borg` | wait per wake, warm first backup | 30 | 3.128 ms | 12.8 % | ±4.87 % | the rule |
| `file-backup` | `borg` | disk wait per wake, warm first backup | 30 | 3.157 ms | 12.7 % | ±4.84 % | the rule |

`file-archiver` (7-Zip) and `game-download` (SteamCMD) have no values yet: 7-Zip's first batch of six repeats is measuring, and `game-download`'s operating point is open — the number of content servers its runner draws sets every value on its list (run 35475239657: 6 servers 4.73 % of packets dropped and 4,070 B a wake, one server forced 0.0005 % and 2,131 B, 6 servers again 4.97 % and 4,137 B).

Full tables: `task-9.7-background-io/campaign/results-borg.md`, `campaign/results/borg-pooled.json`.

## Machine draws

The build campaign, complete: 28 jobs, 14 on the AMD EPYC 7763 (50.0 %), 12 stopped by the machine gate — Intel Xeon Platinum 8573C 4, AMD EPYC 9V74 4, AMD EPYC 9V45 2, Intel Xeon Platinum 8370C 1, Intel Xeon 6973P-C 1 — and 2 cancelled.

The two 9.5 campaigns, as recorded on 2026-09-19 while they were still running: 158 jobs, 90 on the AMD EPYC 7763, 68 stopped by the gate. The model breakdown recorded then, over all three campaigns: AMD EPYC 9V74 32, Intel Xeon 6973P-C 12, Intel Xeon Platinum 8573C 12, AMD EPYC 9V45 8, Intel Xeon Platinum 8370C 8.
