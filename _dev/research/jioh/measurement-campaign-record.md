# Measured values — campaign record

Every campaign behind a measured archetype value: per archetype the repeats, the values the rule covers, the widest margin among them, why it stopped, and the machine draws it took. Method: `measurement-campaign-workflow.md`. Each row regenerates with `dataset/tools/meas/loop/pool_runs.py <family>/<app> --since 10` (`soffice`: `--since 38`; `thunderbird-send`: `--since 150 --exclude 29`; the `desktop` family: `--since 21`; the `session` family: `--since 16 -- --tag meas-ci:session:2026-09-24`); job counts are the campaign runs' jobs, read from their job lists. Recorded 2026-09-20, the 9.8 rows 2026-09-22, the 9.9 rows 2026-09-24, the three re-measured 9.5 rows 2026-09-24; the 9.5 rows were first recorded a day earlier against one headline median per archetype, which D29 and D30 replaced. Every gap mean and wake rate re-read on 2026-09-24 under 9.5 D71 (gaps over merged wake times, wrapped round the span; rates from exact counts); the 9.8 renderer residuals re-classed as sparse components on 2026-09-25 (9.8 D27); the 9.9 pool rebuilt the same day with sysstat's jobs outside and two sparse components (9.9 D32, D33).

## Campaigns

All on GitHub-hosted `ubuntu-24.04` runners, 4 vCPU, pinned to one CPU, AMD EPYC 7763 only (machine gate); kernel `6.17.0-1022-azure` in every repeat of the build campaign and of all six 9.5 applications whose rule holds (their pooled records carry it per repeat). Stability rule (D29, D30): for every value the fold-in carries, each table by its per-repeat mean, the 95 % confidence half-width of the across-repeat mean is at most 5 % of it or 1 µs, whichever is larger, over at least five same-machine repeats (`dataset/tools/meas/stability.py`). A value whose phase holds the recorded input's last window is reported with its half-width instead, and left out of the rule (D32, D46).

| tag | slice | workflow | runs | first launch |
|---|---|---|---|---|
| `meas-ci:build:2026-09-18` | 9.6 | `meas-build.yml` | #10–#37; the 13 holding a landed repeat are #10, #11, #12, #15, #16, #22, #25, #26, #27, #29, #30, #32, #34 | 2026-09-18 09:09 UTC |
| `meas-ci:interactive:2026-09-18` | 9.5 | `meas-interactive.yml` | #10–#100 | 2026-09-18 09:56 UTC |
| `meas-ci:playback:2026-09-18` | 9.5 | `meas-playback.yml` | #10–#84 | 2026-09-18 09:56 UTC |
| `meas-ci:interactive:2026-09-19` | 9.5 | `meas-interactive.yml` | #150–#244, `thunderbird-send` alone (the `send` re-observation) | 2026-09-19 11:18 UTC |
| `meas-ci:background:2026-09-19` | 9.7 | `meas-background.yml` | #19–#58; `borg`'s repeats are in #24–#40, `steamcmd`'s pooled repeats in #47–#57 | 2026-09-19 23:16 UTC |
| `meas-ci:interactive:2026-09-20` | 9.5 | `meas-interactive.yml` | #245–#565, `chrome` and `code` re-measured under D51 and D53; `code` restarted at #376 under D61 and `chrome` at #438 under D65; `code` restarted keys only at #566 under D72 (its campaign is the row below) | 2026-09-20 08:04 UTC |
| `meas-ci:playback:2026-09-20` | 9.5 | `meas-playback.yml` | #245–#565, `webrtc` re-measured under D54 | 2026-09-20 08:04 UTC |
| `meas-ci:desktop:2026-09-20` | 9.8 | `meas-desktop.yml` | #21–#50 | 2026-09-20 11:03 UTC |
| `meas-ci:interactive:2026-09-25` | 9.5 | `meas-interactive.yml` | #566–#599, `code` keys only under D72; 34 runs, 102 jobs (57 gated), every window of the recording landed (D73) | 2026-09-25 00:19 UTC |
| `meas-ci:session:2026-09-24` | 9.9 | `meas-session.yml` | #16–#22; the four holding a landed repeat are #16, #20, #21, #22 | 2026-09-23 23:35 UTC (2026-09-24 KST) |

## 9.5 — nine archetypes measured

### The six measured first (D26, D29, D30)

Pooled in `task-9.5-interactive-typing/campaign/results-same-machine/` and rendered in `campaign/results-same-machine.md`. Every repeat on one AMD EPYC 7763, kernel `6.17.0-1022-azure` in all of them. `values` counts what the rule covers; `widest` is the largest half-width among them.

| archetype | application | repeats | values | widest | stopped by | jobs (gated) | recorded input covered |
|---|---|---|---|---|---|---|---|
| `office-writer` | `soffice` | 14 (windows 1–14) | 5 | idle `soffice.bin` run mean ±4.93 % | the rule | 19 (5) | SWELL-KW Word, participants 1–6 |
| `mail-client` | `thunderbird-send` | 43 (windows 1–28, 30–44) | 36 + 39 reported at the window limit | idle `JS Watchdog` gap mean ±4.52 % | the rule | 77 (32) | SWELL-KW Outlook, all 25 participants; windows 9 on are past the recording |
| `image-editor` | `gimp` | 5 (1, 2, 3, 5, 6) | 10 | op `gimp` wakes/s ±4.38 % | the rule | 8 (3) | scripted pointer loop |
| `video-editor` | `kdenlive` | 20 (1–3, 5–21) | 22 | driven `kdenlive` run mean ±4.94 % | the rule | 30 (10) | scripted pointer loop |
| `video-player` | `mpv-video` | 24 (1, 2, 4, 6–26) | 3 since D75 (16 before) | play cycle run mean ±2.89 % (before D75: play `vo` wakes/s ±4.98 %) | the rule | 51 (27) | none |
| `audio-player` | `mpv-audio` | 31 (1–31) | 3 since D75 (16 before) | play cycle run mean ±4.79 % (before D75: play `ao` run mean ±4.93 %) | the rule | 55 (24) | none |

The typing-driven applications also replay the 136M Keystrokes windows 1…k of their own repeats in the `driven-alt` phase (the pre-registered stimulus check).

**What the half-widths do and do not claim** (noted 2026-09-24, in self-review; no decision taken, and it is 9.14's and 9.16's to resolve). The loop adds one repeat at a time and stops when every value the rule covers is inside the tolerance, so the value that stopped an application sat at the boundary by construction: `soffice` 4.93 %, `mpv-audio` 4.93 %, `kdenlive` 4.94 %, `webrtc` 4.95 %, `mpv-video` 4.98 %, `thunderbird-send` 5.00 %, `gimp` 4.59 %. Read as 9.5 D71 reads them — gap means over merged wake times, rates from exact counts — two widest values move: `thunderbird-send`'s is the idle `JS Watchdog` gap mean at 4.52 %, `gimp`'s its op wake rate at 4.38 %; seven of the nine sit within half a point of the line. Dropping any single repeat moves the mean of each application's widest value by up to 0.67–1.44 % (`leave_one_out` in each pooled record). Stopping at the first crossing cannot bias a mean, so the values themselves stand; it does make the stated precision of that one value per application optimistic, because the count was chosen by the estimate it produced. Across the library 17 of the 188 values the rule covers have half-widths of 4.5 % or more; the rest cleared it with room. `chrome` is the exception — it stopped at its recording's last window, not at the rule, and its widest value inside the rule is 2.99 %. So does `code` since its keys-only campaign (D73): stopped at its last window, its widest value inside the rule 4.63 %. `gimp` rests on the five-repeat minimum.

Reported precision would be clean rather than caveated if the binding values were re-measured at a count fixed in advance and their half-widths read once, without re-testing: about three hours for `webrtc`, `mpv-video` and `mpv-audio` at some twelve minutes a repeat, about a day for `chrome` and `code`.

- `office-writer`: the first design's five repeats (the stream's clicks, scrolls and drags replayed with the keys; `input_run` p50 8.67, 3.99, 5.91, 4.53, 4.21 ms, ±44 %) are superseded by D28 and not pooled; their 11 jobs, 6 of them gated, are not in the count above.
- `mail-client`: it took 43 repeats against the 29 first projected, because its idle phase holds a ~60 s `StreamTrans` episode that comes out big 6 to 9 times per 600 s window against 10 cycles, which kept the idle `StreamTrans` gap mean at the top of the tolerance. Window 29 is left out of the pool (D47), its Outlook window having been launched uncut; 77 jobs counted here exclude that repeat's job, one cancelled duplicate and one dry check. The 39 values of the phases that replay a window — the two per-input means and 37 of the operation's — are reported with their half-widths over the eight full repeats, the recording's last window (D32, D46).
- `video-player`: its `vo` thread's projection swung between 24 and 31 repeats over ten repeats before settling; the rule held at 24.
- The three playback entries since D75 (2026-09-26): each carries one periodic job per medium cycle — its period the mean interval between cycle starts read off a reference thread, its run the process tree's whole CPU per cycle — in place of its components, so the values the rule covers are the play-phase CPU share, the cycle length mean and the cycle run mean: `audio-player` 49.635 ms, run mean 0.352 ms (±4.79 %); `video-player` 33.348 ms, 4.062 ms (±2.89 %); `video-call` 10.001 ms, 2.371 ms (±1.58 %); cycle lengths ±0.00–0.02 %. Read from the pools the campaigns closed, no repeat added; none of them is a value that stopped a campaign.
- `image-editor`, `video-editor`, `video-player`: the windows the gate stopped (4; 4; 3 and 5) were not retried once the rule held.

### The three re-measured (D51, D53, D54), finished 2026-09-24; `code` again, keys only, finished 2026-09-25 (D72, D73)

Pooled in `task-9.5-interactive-typing/campaign/results-re-measured/` and rendered in `campaign/results-re-measured.md`. Every repeat on one AMD EPYC 7763, kernel `6.17.0-1022-azure`. Components are identified by process role and comm (D67), so a comm naming a thread of several processes is several components.

| archetype | application | repeats | values | widest | stopped by | jobs (gated) | recorded input covered |
|---|---|---|---|---|---|---|---|
| `web-browser` | `chrome` | 38 (windows 1–38) | 18 + 30 reported at the window limit | idle `utility/HangWatcher` run mean ±2.99 % | the recording's last window (D32, D68) | 71 (31) | SWELL-KW Internet Explorer c1, every window the recording holds |
| `code-editor` | `code` | 44 (windows 1–44; 43 idle only, no event recorded) | 26 + 1 carried (D57) + 2 at the window limit | `input_run` mean under SWELL-KW ±5.17 % at the limit | the recording's last window (D32, D68) | 102 (57) | SWELL-KW Word c1, every window the recording holds |
| `video-call` | `webrtc` | 45 | 3 since D75 (39 + 7 carried (D57) before) | play cycle run mean ±1.58 % (before D75: play `gpu/Chrome_ChildIOT` gap mean ±4.95 %) | the rule | 102 (57) | none |

- `web-browser`: its 30 values at the window limit are the operation phase's 27 (D46), the operation's duration mean and the two per-input means; the widest is the `input_run` mean under SWELL-KW, 1.701 ms ±8.33 %, whose spread follows how densely each participant typed — the recording's tail is sparse, windows 29, 35, 36, 37 and 38 replaying 47, 53, 80, 61 and 27 events against 200–1,300 earlier (D32). The 136M check's mean is ±4.09 % over the same repeats. One job was cancelled mid-measurement (window 31, cancelled with the `code` job that shared its run) and is not counted.
- `code-editor`: the keys-only campaign (D72, D73): 44 repeats, VS Code 1.138.0 in every one; window 43 records no event and ran the idle phase alone; window 42's later copy (#599) left out under D66. Its two per-input values are reported at the recording's limit — SWELL-KW 105.4 ms ±5.17 %, 136M 106.1 ms ±3.92 % — the SWELL-KW mean having projected 47 repeats at 41 against 44 windows; `utility/libuv-worker`'s gap mean ±5.13 % is carried under D57, its wake rate ±4.63 % the widest value inside the rule. Every repeat's screenshot after the SWELL-KW phase was read: the letters at the file's end, no view opened. The superseded D61 campaign (41 repeats, pointer events replayed) read 92.31 ms under SWELL-KW and +15 % under 136M; keys only, the two streams agree within 3 %.
- `video-call`: the seven values carried under D57 are the audio path (D59), widest ±5.82 %; `play gpu/Chrome_ChildIOT`'s gap mean took 45 repeats, its wake rate taking discrete levels between sessions — 64.3–65.2 a second in 34 repeats, ~54 in four, ~46.6 in five, 36.5 in one. Since D75 the entry carries the call's 10 ms audio-frame cycle, not its components, so these seven values leave it; they stay in the pooled record.
- The builds are stated per repeat (D69): `code` 1.138.0 in all 44; `chrome` 152.0.7977.82 in 29 and 153.0.8010.52 in 9 (windows 18, 20, 22, 27, 31, 33, 34, 37, 38); `webrtc` 152.0.7977.82 in 42 and 153.0.8010.52 in 3 (windows 37, 40, 45). Google's repository serves only its current version, so the mix is carried and stated: over `chrome`'s 38 repeats every carried value agrees between the two builds within 0.18–1.09 standard deviations of the 152 repeats' own spread, the operation duration within 0.38 and the 136M mean within 0.13.

They replaced these values (D55):

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

## 9.7 — `file-backup`, `file-archiver` and `game-download`

Repeats 1–31 on the AMD EPYC 7763, repeat 3 left out of the pool: it landed, but its 10 GB set fetched as a 12,108 B file in place of the 3.70 GB archive (`set.archive_pin` mismatch, extract rc 2, 0 files), so its phases ran on an empty tree and the validity step fails it (the loop, step 4). 55 jobs: 31 landed, 24 stopped by the machine gate, none on another model. The rule is read over the other 30 repeats, and holds on both of `file-backup`'s values.

Each archetype carries two tables (D29): the program's runs between voluntary blocks, pooled over its threads, and the block after each run — the program's off-CPU time, zero when another of its threads runs on — each tested by its per-repeat mean.

| archetype | program | value | repeats | mean | spread (cv) | 95 % half-width | stopped by |
|---|---|---|---|---|---|---|---|
| `file-backup` | `borg` | run between voluntary blocks, warm first backup | 30 | 15.182 ms | 10.2 % | ±3.91 % | the rule |
| `file-backup` | `borg` | block per run, warm first backup | 30 | 3.128 ms | 12.8 % | ±4.87 % | the rule |
| `file-archiver` | `7z` | run between voluntary blocks, warm eight-thread run | 6 | 4.187 ms | 2.1 % | ±2.17 % | the rule |
| `file-archiver` | `7z` | block per run, warm eight-thread run | 6 | 0.16 µs | 38.5 % | ±0.06 µs | the rule (1 µs floor) |
| `game-download` | `steamcmd` | run between voluntary blocks, shaped fresh install | 30 | 163.4 µs | 6.3 % | ±2.42 % | the rule |
| `game-download` | `steamcmd` | block per run, shaped fresh install | 30 | 9.43 µs | 27.2 % | ±0.98 µs (±10.38 %) | the rule (1 µs floor) |

The per-wake tables of the first list are reported beside them: `borg` wait per wake 3.128 ms ±4.87 %, disk wait 3.157 ms ±4.84 %; `7z` wait per wake 32.232 ms ±2.40 %; `steamcmd` network wait 223.1 µs ±4.51 %, bytes per wake 3,973 B ±3.84 %, run per wake 163.4 µs.

`file-archiver`'s first batch of six repeats holds the rule, every repeat valid: 14 jobs, 8 gated draws, none on another model. Its D15 check, the single-thread run against the eight-thread run, is reported by its CPU per byte (0.91–0.96 of the eight-thread run in every repeat); the check's per-wake parts split into two modes of the same thread, 940 wakes at a 0.36–0.38 s median gap in repeats 1, 2 and 6 against 1,246–1,575 wakes at 0.4–0.7 ms in repeats 3, 4 and 5, and both are stated in the archetype's notes.

`game-download`'s repeats 1–34 ran in runs #47–#98 under the `fq_codel` leaf (D25): repeats 6–12 and 14–22 as batches, then one at a time (D26). Four are left out: 21 ran unshaped — its runner had no accelerated-networking VF and 490 B of its 10.5 GB download went through the shaper (D27); 23 was wrongly launched on the pool that still held 21 (D27); 32's untraced and unshaped phases did not complete, SteamCMD reporting FAILED (No Connection) (D32); 33's unshaped phase's `perf.data` is truncated, its timehist report exiting 242 (D33). 76 jobs: 34 landed, 35 stopped by the machine gate on another model (Xeon Platinum 8573C 13, EPYC 9V74 13, EPYC 9V45 5, Xeon 6973P-C 4) and 7 stopped on the AMD EPYC 7763 by the network gate added after repeat 21 — runners with no accelerated-networking VF, where the shaper cannot sit (D27). The rule is read over the other 30 repeats (1–20, 22, 24–31, 34) and holds on both carried tables, every repeat valid. The repeats split by the Steam site the runner drew — 14 west, 13 east, 3 central — and the region holds 64 % of the variance of network wait and 45 % of the block per run.

Full tables: `task-9.7-background-io/campaign/results-borg.md`, `campaign/results-7z.md` and `campaign/results-steamcmd.md`, `campaign/results/borg-pooled.json`, `results/7z-pooled.json` and `results/steamcmd-pooled.json`.

## 9.8 — four archetypes, one campaign

Every repeat on the AMD EPYC 7763, kernel `6.17.0-1022-azure` in all of them, none excluded or superseded; the renderer entries on Google Chrome 152.0.7977.82 in every repeat, 12 renderers measured of 16 observed (hidden) and of 13–14 (visible). Each entry reads one phase (method §10): the hidden renderer `steady`, the visible renderer `steady-notimer` (D16), the chat client `idle`, the Steam client `shown`. The renderer entries' values are per renderer, the renderers pooled as samples (D14). `values` counts what the rule covers; `widest` is the largest half-width among the values that pass it.

| archetype | subject | repeats | values | pass | widest | stopped by | jobs (gated) | recorded input covered |
|---|---|---|---|---|---|---|---|---|
| `renderer-hidden` | `chrome-hidden` | 14 (1–9, 11, and 10 four times) | 21 | 6 | `ThreadPoolServi` run mean ±4.82 % | the rule | 25 (11) | none |
| `renderer-visible` | `chrome-visible` | 11 (1–11) | 15 | 4 | `chrome` wake rate ±3.76 % | the rule | 18 (7) | none |
| `chat-client` | `element` | 18 (1–16, and 17 twice) | 18 | 18 | residual run mean ±4.32 % | the rule | 32 (14) | none |
| `game-client` | `steam` | 12 (1–12) | 33 | 27 | `ThreadPoolForeg` run mean ±4.99 % | the rule | 21 (9) | none |

Rates are one renderer's, the mean over every renderer measured from exact counts; gaps are over each component's merged wake times, wrapped round the phase — the renderers laid end to end for a renderer entry — so a gap mean is the span over the wakes (9.5 D71; this slice's D26).

The values outside the tolerance, each carried over its repeats with its half-width and range. Run means whose spread is the machine (D17; the Steam client's by D18):

- hidden renderer: `HangWatcher` run mean 0.0274 ms ±5.3 % (0.024–0.033).
- visible renderer: `HangWatcher` run mean 0.0318 ms ±6.0 % (0.029–0.037); `chrome` run mean 0.1489 ms ±5.8 % (0.133–0.181).
- Steam client: `steam` run mean 0.0555 ms ±10.2 % (0.044–0.068); `IPC:CSteamEngin` 0.0573 ms ±8.8 % (0.047–0.068); `CJobMgr::m_Work` 0.0176 ms ±6.2 % (0.015–0.020); `VizCompositorTh` 0.0819 ms ±5.5 % (0.066–0.089); `CHTTPClientThre` 0.0312 ms ±46.0 % (0.014–0.064).

Components whose spread lies between sessions, their three values together (D21; the hidden renderer's `Chrome_ChildIOT` by D24, the four quiet threads by D26, the Steam client's by D23, all under 9.5 D57):

- hidden renderer, `Chrome_ChildIOT`: 0.0071 wakes/s ±20.9 % (0.0021–0.0106); gap mean 172.5 s ±35.0 % (94.7–480.0 s); run mean 0.0321 ms ±14.1 % (0.025–0.056).
- hidden renderer, `Compositor`, `PerfettoTrace` and `ThreadPoolServi`, which wake together: 0.0065 wakes/s ±21.9 % (0.0017–0.0100); gap mean 194.3 s ±39.8 % (100.0–600.0 s); run means 0.0207 ms ±6.3 % and 0.0202 ms ±5.8 %, `ThreadPoolServi`'s 0.0199 ms within the tolerance (±4.8 %); within one run ±10.8 % against ±63.6 % across the repeats.
- visible renderer, `Chrome_ChildIOT`: 0.0060 wakes/s ±26.4 % (0.0022–0.0094); gap mean 196.5 s ±33.8 % (105.9–450.0 s); run mean 0.0408 ms ±10.7 % (0.030–0.053).
- visible renderer, `PerfettoTrace`: 0.0054 wakes/s ±26.2 % (0.0017–0.0085); gap mean 227.2 s ±40.0 % (118.0–600.0 s); run mean 0.0241 ms ±5.1 % (0.022–0.028); within one run ±4.0 % against ±63.4 % across.
- Steam client, `steamwebhelper`: run mean 0.0696 ms ±5.3 % (0.063–0.082); its wake rate and gap mean pass. Its and `ThreadPoolForeg`'s gap means, carried until D26 at ±10.2 % and ±9.0 %, read ±0.18 % and ±4.15 % over merged wake times.

Sparse components, waking a few times per renderer per phase, their three values together with their half-widths and their count (D27; carried between sessions from D21 to D26):

- hidden renderer, residual (`MemoryInfra`): 0.0035 wakes/s ±18.3 % (0.0021–0.0057); gap mean 308.9 s ±15.6 % (175.6–480.0 s); run mean 0.1924 ms ±8.8 % (0.152–0.265); 1.2–3.4 wakes per renderer per 600 s phase. A 600 s window of the probe catches 0–2 of its wakes — ±134.2 % within one run against ±51.6 % across the repeats — the count's own spread, which the within-run test cannot place.
- visible renderer, residual (`MemoryInfra`, `Compositor`, `ThreadPoolForeg`, `ThreadPoolServi`): 0.0068 wakes/s ±10.9 % (0.0060–0.0092); gap mean 149.9 s ±9.0 % (109.1–167.4 s); run mean 0.1434 ms ±11.0 % (0.116–0.200); 3.6–5.5 wakes per renderer per 600 s phase. The probe does not reproduce its comms, 0.0009 against 0.0068 wakes/s (±181.3 % within one run against ±23.5 % across), so the within-run test does not apply.

- Repeat indices that landed more than once: the retry driver relaunched the hidden renderer's repeat 10 in runs #33, #34, #36 and #37 and the chat client's repeat 17 in #49 and #50, and every launch landed on the AMD EPYC 7763 with the gate open. Every landing is pooled, keyed `<index>@<run id>` (D24).
- No gated window was left once the rule held: every index 1…k of each entry landed.

- **When each exception was decided** (D28, 2026-09-25; git and the runs' launch times, UTC). Every exception followed a value seen failing. D17, the run means of the renderers and the chat client as machine speed, was committed 2026-09-21 09:44 on the first batch of five, before the hidden renderer's windows 6–11 and the visible's 7–11 were launched (runs #31–#40, 09:48–10:15); D18, the Steam client's run means, at 11:04, before its windows 6–12 (#43–#45, 11:13–11:18); D21, the renderers' quiet threads, at 11:48, after the renderers' last launch; D23, the Steam client's two components, 22:51, and D24, every landing pooled, 2026-09-22 02:46, after the campaign's last run (#50, 12:01). The workflow's class-wide wording for the machine-speed exception landed 2026-09-22 09:53, after the fold-in (04:21). Projected repeats to pass, from the pool as it stands: hidden `HangWatcher` run mean 16 (14 landed); visible `HangWatcher` 15 and `chrome` 14 (11); Steam `steamwebhelper`, `CJobMgr::m_Work` and `VizCompositorTh` 14, `IPC:CSteamEngin` 34, `steam` 46, `CHTTPClientThre` none (12). The machine-speed ground — run times moving together across every thread of a repeat while wake rates hold — is a mechanism the record shows independently of the pass, and the exceptions stand on it; whether their half-widths are re-measured at a count fixed in advance is 9.14's, after its sensitivity check. Qualification on the within-run test: the probe's 600 s windows every 60 s overlap and are correlated, so a within-run figure understates that spread against the independent repeats it is compared with.

Full tables: `task-9.8-browser-comms/campaign/results/results.md`, `campaign/results/pooled.json`.

## 9.9 — four entries, one campaign

One subject, the Ubuntu 24.04 desktop session, carries the four entries that replace `system-daemon` — `compositor-shell` (GNOME Shell), `audio-server` (the PipeWire stack), `service-manager` (`systemd`) and `message-bus` (`dbus-daemon`), folded in at D26 and again, re-analysed, at D30 — so every job observes all four and the repeats and jobs are shared. 24 repeats — 47–49, 51, 58, 60–63, 68, 69, 71–77, 79, 83, 85–88 — every one on the AMD EPYC 7763, kernel `6.17.0-1022-azure` in all of them, none excluded, one set of package versions in every repeat (`gnome-shell` 46.0-0ubuntu6~24.04.14, `pipewire` and `pipewire-pulse` 1.0.5-1ubuntu3.3, `wireplumber` 0.4.17-1ubuntu4.1, `systemd` 255.4-1ubuntu8.17, `dbus-daemon` 1.14.10-4ubuntu4.1). Each entry reads the `steady` phase, 1800 s (D22): the session idle past `idle-delay`, the shield up and locked, the monitor blanked (method §3). No display server in any repeat's census. Every wake is read by its cause (D27): wakes owed to a package Ubuntu 24.04's desktop manifest does not hold, or to the harness, and desktop jobs bound to a clock time leave the components and are stated. `values` counts what the rule covers; `widest` is the largest half-width among those that pass.

| entry | components | repeats | values | pass | widest | stopped by | jobs (gated) | recorded input covered |
|---|---|---|---|---|---|---|---|---|
| `compositor-shell` | `JS Helper`, `gmain`, `gnome-shell` | 24 | 9 | 9 | `gnome-shell` run mean ±2.8 % | the rule | 42 (18), shared | none |
| `audio-server` | `wireplumber/gmain` | 24 | 3 | 1 | carried (D33) | the rule, with D33 | shared | none |
| `service-manager` | `pid1/systemd` | 24 | 3 | 2 | carried (D29) | the rule, with D29 | shared | none |
| `message-bus` | `system-bus/dbus-daemon` | 24 | 3 | 0 | carried (D33) | the rule, with D33 | shared | none |

| component | wakes/s | gap mean | run mean | half-widths (rate · gap · run) |
|---|---|---|---|---|
| `gnome-shell/JS Helper` | 0.3025 | 3.31 s | 0.0137 ms | ±0.7 · ±0.7 · ±1.5 % |
| `gnome-shell/gmain` | 0.2498 | 4.00 s | 0.0497 ms | ±0.1 · ±0.1 · ±2.2 % |
| `gnome-shell/gnome-shell` | 0.0347 | 28.81 s | 5.7035 ms | ±1.5 · ±1.5 · ±2.8 % |
| `wireplumber/gmain` | 0.0029 | 426.70 s | 0.0360 ms | ±21.6 · ±19.8 · ±4.0 %, carried (D33) |
| `pid1/systemd` | 0.0734 | 13.66 s | 0.1274 ms | ±2.0 · ±1.9 · ±10.1 %, run mean carried (D29) |
| `system-bus/dbus-daemon` | 0.0057 | 238.56 s | 0.1882 ms | ±43.8 · ±45.7 · ±25.0 %, carried (D33); 0–36 wakes a phase, none in 6 of 24 |

Gap means are over each component's merged wake times, wrapped round the phase (9.5 D71; this slice's D31), so a gap mean is the phase over the wakes.

- Causes that left (D27), per phase: `php-fpm` (PHP 8.3's FastCGI service, which the runner image ships) 180–188 wakes of pid 1 and 185–225 of the system bus through pid 1; the workflow's "wait for the run" loop 355–362 of WirePlumber's worker, each with the worker's own timer 100.2 ms later; PHP's session cleanup and `podman` a few each. Sysstat's jobs (D32, 2026-09-25): the collector, every 10 minutes, had been kept as a desktop job — 277 of `audio-server`'s 402 kept wakes, 361 of `message-bus`'s 609, 68 of `service-manager`'s 3,238 — and is outside with the summary and the 23:59 sample, since a stock install leaves sysstat's timers disabled (Debian's `sysstat/enable` defaults to false) and the runner image enabled them. Desktop jobs bound to a clock time (`logrotate`, `man-db`, `fstrim`, `motd-news`, `anacron`) are stated as events. Before D27 the three entries read 0.179, 0.137 and 0.213 wakes/s; before D32, 0.075, 0.014 and 0.0093.
- Carried with its half-width (D28, D29): `pid1/systemd`'s run mean, its spread lying in part within one run, 123–145 wakes a phase. Sparse components (9.8 D27; D33): `wireplumber/gmain`, 2–12 wakes a phase, and `system-bus/dbus-daemon`, 0–36 a phase and none in repeats 69, 72, 74, 75, 79 and 83 — each its entry's whole activity, its three values together with their half-widths, the bus's wake rate over every repeat and its gap and run means over the 18 it woke in.
- Coverage (method §5, the 95 % cut): GNOME Shell 99.97 % of 0.587 wakes/s, every other entry 100 % of its one component; no residual. `pipewire` and `pipewire-pulse` recorded no wake in the phase of any repeat. The session bus woke 26–29 times in each of repeats 47, 48, 49 and 51 and in no other — all at 00:00 UTC, from Evolution's calendar and alarm daemons, inside the cron session's window — and the user manager 8 times in the same four; D23 and D27 took every one out, so the entries carry none. GNOME Shell's `gnome-s:disk$0` woke only in those four repeats, 0.0002 wakes/s over the pool, reported as sporadic, not carried.
- A cron job's session (D23): repeats 47, 48, 49 and 51, the first batch, met the `sphinxsearch` indexer's at 00:00 UTC, 317–365 s into the phase; the rows inside its window left each component — `service-manager` 201, `message-bus` 245, `audio-server` 37, `compositor-shell` 12 — and are stated per repeat in `pooled.json` (`cron_event`). No other repeat met one.
- Foreign work on the measured CPU: 18–43 user-space schedule-ins per repeat outside the four entries, 0.00097–0.0022 % of the phase against the 2 × 10⁻⁴ bound (D22); none by a pinned unit's other process. Kernel threads 11,608–15,472 schedule-ins per repeat, reported and not gated (D14).
- Batches: the first batch of five in run #16 (repeat 50 gated); relaunches and added repeats in #17–#21; then 24 jobs to the pool's projection in #22 (D25), 15 of them landing. Every landing is pooled.

- **When the exception was decided and where the campaign stopped** (D34, 2026-09-25; UTC). The campaign's last run, #22, was launched 2026-09-24 02:47; it was closed at 24 repeats at 05:55 (`55944a5`, "the rule holds, widest 3.7 %") on the values it carried then; D27's re-analysis by cause (10:56, `60c50ba`) moved three components off the rule and D29 carried them, so the exception followed values seen failing after the campaign had stopped, and no repeat was added. The projections then: 58 for pid 1's run mean, 96–138 for the system bus; now pid 1's run mean 99, the bus a sparse component (D33). Whether pid 1's run mean is re-measured at a count fixed in advance is 9.14's, after its sensitivity check.

Full tables: `task-9.9-daemons-session/campaign/results/results.md`, `campaign/results/pooled.json`; the placement of D28, `campaign/results/within-run.json`; every job's model: `campaign/machine-draws.md`.

## Machine draws

The build campaign, complete: 28 jobs, 14 on the AMD EPYC 7763 (50.0 %), 12 stopped by the machine gate — Intel Xeon Platinum 8573C 4, AMD EPYC 9V74 4, AMD EPYC 9V45 2, Intel Xeon Platinum 8370C 1, Intel Xeon 6973P-C 1 — and 2 cancelled.

The 9.5 campaigns of 2026-09-18 and 2026-09-19, over the six applications whose rule holds and complete for them: 252 jobs — 144 landed on the AMD EPYC 7763 (57.1 %, one of them `thunderbird-send`'s dry check), 107 stopped by the gate, 1 cancelled. The model is recorded for 104 of those stops, the reports the loop read: AMD EPYC 9V74 47, Intel Xeon Platinum 8573C 19, AMD EPYC 9V45 18, Intel Xeon 6973P-C 12, Intel Xeon Platinum 8370C 8. Per application, gate stops: `thunderbird-send` 32, `mpv-video` 27, `mpv-audio` 24, `soffice` 11 (5 of them in the pooled campaign, 6 in the superseded first design), `kdenlive` 10, `gimp` 3. The 2026-09-20 campaign re-measuring `chrome`, `code` and `webrtc` is still running.

The 9.8 desktop campaign, complete: 96 jobs — 55 landed on the AMD EPYC 7763 (57.3 %, all pooled), 41 stopped by the machine gate: AMD EPYC 9V74 19, Intel Xeon Platinum 8573C 9, AMD EPYC 9V45 7, Intel Xeon 6973P-C 4, Intel Xeon Platinum 8370C 2. Per entry, gate stops: `element` 14, `chrome-hidden` 11, `steam` 9, `chrome-visible` 7.

The 9.9 session campaign, complete: 42 jobs — 24 landed on the AMD EPYC 7763 (57.1 %, all pooled), 18 stopped by the machine gate: AMD EPYC 9V74 6, Intel Xeon Platinum 8573C 5, AMD EPYC 9V45 3, Intel Xeon 6973P-C 3, Intel Xeon Platinum 8370C 1. With the tooling's dry runs and the long-phase probes, neither of them a repeat, 38 of 77 jobs drew the EPYC 7763 (`task-9.9-daemons-session/campaign/machine-draws.md`).
