# Measured values — campaign record

Every campaign behind a measured archetype value: per archetype the repeats, the values the rule covers, the widest margin among them, why it stopped, and the machine draws it took. Method: `measurement-campaign-workflow.md`. Each row regenerates with `dataset/tools/meas/loop/pool_runs.py <family>/<app> --since 10` (`soffice`: `--since 38`; `thunderbird-send`: `--since 150 --exclude 29`; the `desktop` family: `--since 21`); the `session` family's rows with `dataset/tools/meas/session/pool.py` over the 24 repeats of release `meas-ci-session-2026-09-24`, since `pool_runs.py` lists only the first 30 artifacts of a run and each session job uploads about 30; job counts are the campaign runs' jobs, read from their job lists. Recorded 2026-09-20, the 9.8 rows 2026-09-22, the 9.9 rows 2026-09-24; the 9.5 rows were first recorded a day earlier against one headline median per archetype, which D29 and D30 replaced.

## Campaigns

All on GitHub-hosted `ubuntu-24.04` runners, 4 vCPU, pinned to one CPU, AMD EPYC 7763 only (machine gate); kernel `6.17.0-1022-azure` in every repeat of the build campaign and of all six 9.5 applications whose rule holds (their pooled records carry it per repeat). Stability rule (D29, D30): for every value the fold-in carries, each table by its per-repeat mean, the 95 % confidence half-width of the across-repeat mean is at most 5 % of it or 1 µs, whichever is larger, over at least five same-machine repeats (`dataset/tools/meas/stability.py`). A value whose phase holds the recorded input's last window is reported with its half-width instead, and left out of the rule (D32, D46).

| tag | slice | workflow | runs | first launch |
|---|---|---|---|---|
| `meas-ci:build:2026-09-18` | 9.6 | `meas-build.yml` | #10–#37; the 13 holding a landed repeat are #10, #11, #12, #15, #16, #22, #25, #26, #27, #29, #30, #32, #34 | 2026-09-18 09:09 UTC |
| `meas-ci:interactive:2026-09-18` | 9.5 | `meas-interactive.yml` | #10–#100 | 2026-09-18 09:56 UTC |
| `meas-ci:playback:2026-09-18` | 9.5 | `meas-playback.yml` | #10–#84 | 2026-09-18 09:56 UTC |
| `meas-ci:interactive:2026-09-19` | 9.5 | `meas-interactive.yml` | #150–#244, `thunderbird-send` alone (the `send` re-observation) | 2026-09-19 11:18 UTC |
| `meas-ci:background:2026-09-19` | 9.7 | `meas-background.yml` | #19–#58; `borg`'s repeats are in #24–#40, `steamcmd`'s pooled repeats in #47–#57 | 2026-09-19 23:16 UTC |
| `meas-ci:interactive:2026-09-20` | 9.5 | `meas-interactive.yml` | #245–, `chrome` and `code` re-measured under D51 and D53 | 2026-09-20 08:04 UTC |
| `meas-ci:playback:2026-09-20` | 9.5 | `meas-playback.yml` | #245–, `webrtc` re-measured under D54 | 2026-09-20 08:04 UTC |
| `meas-ci:desktop:2026-09-20` | 9.8 | `meas-desktop.yml` | #21–#50 | 2026-09-20 11:03 UTC |
| `meas-ci:session:2026-09-24` | 9.9 | `meas-session.yml` | #16–#22; the four holding a landed repeat are #16, #20, #21, #22 | 2026-09-23 23:35 UTC (2026-09-24 KST) |

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
| `renderer-hidden` | `chrome-hidden` | 14 (1–9, 11, and 10 four times) | 12 | 5 | `chrome` run mean ±4.44 % | the rule | 25 (11) | none |
| `renderer-visible` | `chrome-visible` | 11 (1–11) | 15 | 4 | `chrome` gap mean ±3.68 % | the rule | 18 (7) | none |
| `chat-client` | `element` | 18 (1–16, and 17 twice) | 18 | 18 | `ThreadPoolForeg` gap mean ±4.56 % | the rule | 32 (14) | none |
| `game-client` | `steam` | 12 (1–12) | 33 | 25 | `ThreadPoolForeg` run mean ±4.99 % | the rule | 21 (9) | none |

The values outside the tolerance, each carried over its repeats with its half-width and range. Run means whose spread is the machine (D17; the Steam client's by D18):

- hidden renderer: `HangWatcher` run mean 0.0274 ms ±5.3 % (0.024–0.033).
- visible renderer: `HangWatcher` run mean 0.0318 ms ±6.0 % (0.029–0.037); `chrome` run mean 0.1489 ms ±5.8 % (0.133–0.181).
- Steam client: `steam` run mean 0.0555 ms ±10.2 % (0.044–0.068); `IPC:CSteamEngin` 0.0573 ms ±8.8 % (0.047–0.068); `CJobMgr::m_Work` 0.0176 ms ±6.2 % (0.015–0.020); `VizCompositorTh` 0.0819 ms ±5.5 % (0.066–0.089); `CHTTPClientThre` 0.0312 ms ±46.0 % (0.014–0.064).

Components whose spread lies between sessions, their three values together (D21; the hidden renderer's `Chrome_ChildIOT` by D24, the Steam client's by D23, all under 9.5 D57):

- hidden renderer, `Chrome_ChildIOT`: 0.0065 wakes/s ±38.1 % (0–0.010); gap mean 137.4 s ±25.7 % (96.9–309.1 s); run mean 0.0321 ms ±14.1 % (0.025–0.056).
- hidden renderer, residual (`ThreadPoolServi`, `MemoryInfra`): 0.0100 wakes/s ±15.6 % (0.0042–0.0140); gap mean 88.3 s ±15.9 % (38.0–132.3 s); run mean 0.0842 ms ±19.0 % (0.057–0.143).
- visible renderer, `Chrome_ChildIOT`: 0.0047 wakes/s ±62.0 % (0–0.010); gap mean 163.5 s ±19.5 % (97.1–254.5 s); run mean 0.0408 ms ±10.7 % (0.030–0.053).
- visible renderer, `ThreadPoolForeg`: 0.0043 wakes/s ±29.1 % (0.003–0.007); gap mean 1051 ms ±27.8 % (472–1653 ms); run mean 0.0254 ms ±10.3 % (0.019–0.034).
- visible renderer, residual: 0.0108 wakes/s ±17.9 % (0.0060–0.0158); gap mean 76.0 s ±13.6 % (46.3–94.3 s); run mean 0.1026 ms ±14.5 % (0.070–0.141).
- Steam client, `steamwebhelper`: gap mean 32.44 ms ±10.2 % (28.51–42.16); run mean 0.0696 ms ±5.3 % (0.063–0.082); its wake rate passes.
- Steam client, `ThreadPoolForeg`: gap mean 511.6 ms ±9.0 % (415.9–616.1); its wake rate and run mean pass.

- Repeat indices that landed more than once: the retry driver relaunched the hidden renderer's repeat 10 in runs #33, #34, #36 and #37 and the chat client's repeat 17 in #49 and #50, and every launch landed on the AMD EPYC 7763 with the gate open. Every landing is pooled, keyed `<index>@<run id>` (D24).
- No gated window was left once the rule held: every index 1…k of each entry landed.

Full tables: `task-9.8-browser-comms/campaign/results/results.md`, `campaign/results/pooled.json`.

## 9.9 — four entries, one campaign

One subject, the Ubuntu 24.04 desktop session, carries the four entries that replace `system-daemon` — `compositor-shell` (GNOME Shell), `audio-server` (the PipeWire stack), `service-manager` (`systemd`) and `message-bus` (`dbus-daemon`), folded in at D26 — so every job observes all four and the repeats and jobs are shared. 24 repeats — 47–49, 51, 58, 60–63, 68, 69, 71–77, 79, 83, 85–88 — every one on the AMD EPYC 7763, kernel `6.17.0-1022-azure` in all of them, none excluded, one set of package versions in every repeat (`gnome-shell` 46.0-0ubuntu6~24.04.14, `pipewire` and `pipewire-pulse` 1.0.5-1ubuntu3.3, `wireplumber` 0.4.17-1ubuntu4.1, `systemd` 255.4-1ubuntu8.17, `dbus-daemon` 1.14.10-4ubuntu4.1). Each entry reads the `steady` phase, 1800 s (D22): the session idle past `idle-delay`, the shield up and locked, the monitor blanked (method §3). No display server in any repeat's census. `values` counts what the rule covers; `widest` is the largest half-width among them.

| entry | components | repeats | values | pass | widest | stopped by | jobs (gated) | recorded input covered |
|---|---|---|---|---|---|---|---|---|
| `compositor-shell` | `JS Helper`, `gmain`, `gnome-shell` | 24 | 9 | 9 | `gnome-shell` run mean ±2.81 % | the rule | 42 (18), shared | none |
| `audio-server` | `wireplumber/gmain` | 24 | 3 | 3 | run mean ±3.71 % | the rule | shared | none |
| `service-manager` | `pid1/systemd` | 24 | 3 | 3 | run mean ±3.55 % | the rule | shared | none |
| `message-bus` | `system-bus/dbus-daemon` | 24 | 3 | 3 | wakes/s ±3.02 % | the rule | shared | none |

| component | wakes/s | gap mean | run mean | widest of the three |
|---|---|---|---|---|
| `gnome-shell/JS Helper` | 0.3025 | 13.05 s | 0.0137 ms | ±1.51 % |
| `gnome-shell/gmain` | 0.2499 | 4.00 s | 0.0497 ms | ±2.20 % |
| `gnome-shell/gnome-shell` | 0.0348 | 28.75 s | 5.7007 ms | ±2.81 % |
| `wireplumber/gmain` | 0.2132 | 4.68 s | 0.0383 ms | ±3.71 % |
| `pid1/systemd` | 0.1792 | 5.57 s | 0.2460 ms | ±3.55 % |
| `system-bus/dbus-daemon` | 0.1368 | 7.33 s | 0.2784 ms | ±3.02 % |

- Coverage (method §5, the 95 % cut): GNOME Shell 99.97 % of 0.587 wakes/s, the PipeWire stack 100 % of 0.213, `systemd` 99.9 % of 0.179, `dbus-daemon` 100 % of 0.137; no entry carries a residual. `pipewire` and `pipewire-pulse` recorded no wake in the phase of any repeat, nor did the session bus. The user manager and GNOME Shell's `gnome-s:disk$0` woke only in repeats 47, 48, 49 and 51, 0.0002 wakes/s each over the pool, and are reported as sporadic, not carried.
- A cron job's session (D23): repeats 47, 48, 49 and 51, the first batch, met one 317–365 s into the phase; the rows inside its window left each component — `systemd` 201, `dbus-daemon` 245, the PipeWire stack 37, GNOME Shell 12 — and are stated per repeat in `pooled.json` (`cron_event`). No other repeat met one.
- Foreign work on the measured CPU: 18–43 user-space schedule-ins per repeat outside the four entries, 0.00097–0.0022 % of the phase against the 2 × 10⁻⁴ bound (D22); none by a pinned unit's other process. Kernel threads 11,608–15,472 schedule-ins per repeat, reported and not gated (D14).
- Batches: the first batch of five in run #16 (repeat 50 gated); relaunches and added repeats in #17–#21; then 24 jobs to the pool's projection in #22 (D25), 15 of them landing. Every landing is pooled.

Full tables: `task-9.9-daemons-session/campaign/results/results.md`, `campaign/results/pooled.json`; every job's model: `campaign/machine-draws.md`.

## Machine draws

The build campaign, complete: 28 jobs, 14 on the AMD EPYC 7763 (50.0 %), 12 stopped by the machine gate — Intel Xeon Platinum 8573C 4, AMD EPYC 9V74 4, AMD EPYC 9V45 2, Intel Xeon Platinum 8370C 1, Intel Xeon 6973P-C 1 — and 2 cancelled.

The 9.5 campaigns of 2026-09-18 and 2026-09-19, over the six applications whose rule holds and complete for them: 252 jobs — 144 landed on the AMD EPYC 7763 (57.1 %, one of them `thunderbird-send`'s dry check), 107 stopped by the gate, 1 cancelled. The model is recorded for 104 of those stops, the reports the loop read: AMD EPYC 9V74 47, Intel Xeon Platinum 8573C 19, AMD EPYC 9V45 18, Intel Xeon 6973P-C 12, Intel Xeon Platinum 8370C 8. Per application, gate stops: `thunderbird-send` 32, `mpv-video` 27, `mpv-audio` 24, `soffice` 11 (5 of them in the pooled campaign, 6 in the superseded first design), `kdenlive` 10, `gimp` 3. The 2026-09-20 campaign re-measuring `chrome`, `code` and `webrtc` is still running.

The 9.8 desktop campaign, complete: 96 jobs — 55 landed on the AMD EPYC 7763 (57.3 %, all pooled), 41 stopped by the machine gate: AMD EPYC 9V74 19, Intel Xeon Platinum 8573C 9, AMD EPYC 9V45 7, Intel Xeon 6973P-C 4, Intel Xeon Platinum 8370C 2. Per entry, gate stops: `element` 14, `chrome-hidden` 11, `steam` 9, `chrome-visible` 7.

The 9.9 session campaign, complete: 42 jobs — 24 landed on the AMD EPYC 7763 (57.1 %, all pooled), 18 stopped by the machine gate: AMD EPYC 9V74 6, Intel Xeon Platinum 8573C 5, AMD EPYC 9V45 3, Intel Xeon 6973P-C 3, Intel Xeon Platinum 8370C 1. With the tooling's dry runs and the long-phase probes, neither of them a repeat, 38 of 77 jobs drew the EPYC 7763 (`task-9.9-daemons-session/campaign/machine-draws.md`).
