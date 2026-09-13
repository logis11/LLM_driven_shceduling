# Task 9.4 — candidates per scope-card item

Stage 2 result. Each item of `../scope-card.md` with the candidates the four class records found (`S1-literature.md`, `S2-project-docs.md`, `S3-traces-datasets.md`, `S4-ci-observability.md`), what each covers, and what no class found. Candidate ids are the records' own.

## Observations that exist

Observations (a population, trace or run with numbers), as distinct from documentation:

| Id | What | Machine / game / window | Kind of data |
|---|---|---|---|
| S1-01 = S2-03 (`lavd-ossna24`) | OSS NA 2024 slides 12–17 | unnamed / unnamed / unnamed; slide 5 names the Steam Deck (AMD Van Gogh, 8 cores) as the platform LAVD targets, not as the trace machine; figures name three process trees (`Troy.exe` tgid 7781 on slide 16, `GameThread` + `redDispatcher1–7` tgid 6340 on slide 11, `Umask: 0022` threads tgid 4727 on slide 15) | text statistics: ~300 tasks scheduled, 90 % long-living / 10 % terminated, top 30–40 tasks = 95 % of scheduling, ~half of those system tasks (wine, graphics, audio servers) at 30–40 %, 15–20 game-specific tasks at 60–70 %, per-schedule runtime "a few 100s usec on average to a few msec maximum", `wineserver` 260 µs, "a task worker" 1.65 ms, 70–75 % of scheduling from waiting syscalls; slide 13 plot of per-task runtime averages (~128 tasks, one game); slide 16 graph with edge counts; slide 14 pie of call stacks |
| S1-02 (LPC 2024 slides) | same runtime figure and same `Troy.exe` graph | as above | repeats S1-01 |
| S3-01 (scx #234) | `scx_lavd` sample tables | Helldivers 2 on Ryzen 9 5900X, 6.8.7-cachyos, ~6.8 min; Apex Legends on Ryzen 7 5800X3D, 6.8.8-tkg-sched_ext, ~10.9 min | one row per sampled `ops.running` event (biased to frequently scheduled tasks); per-row EWMA `run_freq`, `run_tm_ns`, `wake_freq`, `wait_freq`; comm and pid; under `scx_lavd`, stutter bug report |
| S3-02 (scx #296) | `scx_lavd -s $(nproc)` logs | Diablo III and StarCraft II on Ryzen 9 5950X, 6.9-tkg, Proton Experimental; four windows 49–114 s | as S3-01; 22-column format |
| S1-09 (Peri, LPC 2025) | Perfetto trace | Pixel 8 / Angry Birds / 10 s | Android: 46 % utilisation over 9 cores, `UnityMain` frame time 16.6 ms, one wake relation; no thread count, no runtime distribution |
| S3-07 (gpuvis sample) | trace-cmd capture | unnamed / SteamVR compositor, not a game / 212 frames | vblank cadence ~11 ms with `sched_switch`; no game |

Everything else found is documentation or source code (S2-06…S2-13, S3-03…S3-06, S3-08, S3-09, S4-*), talk reports (S1-03, S1-04, S1-06, S1-08), Android or Windows studies (S1-10…S1-15), or an unmeasured user claim (S3-10).

## Per item

### 1. `n_tasks` (300)

- S1-01 slide 12: "Around 300 tasks are scheduled while running a game." System-wide count including the system tasks the same slide names; game and machine unnamed.
- S3-01: 95 distinct pids sampled in Apex Legends over 10.9 min (lower bound; sampling misses rarely scheduled tasks). S3-02: 108 pids in StarCraft II over 99 s, 95 in Diablo III over 49 s; 41 pids share the comm `Play Main Threa`, 38 share `Diablo III64.ex`.
- No observation counts a game's own threads separately from the system's.
- Scope-card boundary: the count leaves the archetype; the number is 9.10's, with these references.

### 2. `frac_long_lived` (0.90)

- S1-01 slide 12: "Around 90% are long-living tasks; only 10% of tasks are terminated." Window unstated; "long-living" defined only as not terminated.
- No other observation (S1 §3, S3 §3: T4 not found). The gamescope tracing recipe (S3-06) is the only documented capture that records `sched_process_exit`; no published trace.
- Read by no tool.

### 3. `per_schedule_run` (lognormal, anchors 260 / 1 650 µs)

- S1-01 slide 13, text: "roughly a few 100s usec on average to a few msec maximum"; "wineserver:260 usec"; "a task worker: 1.65 msec". The two named values are examples; the statistic is not labelled.
- S1-01 slide 13, plot (one game, ~128 tasks, "runtime average per schedule"): read in K2 as ≈0.02 ms at the low end, ≈0.04 ms at task 60, ≈0.1 ms at task 100, ≈0.26 ms near task 116–118, ≈0.6 ms near task 124, ≈1.38 ms maximum. 1.65 ms exceeds the plot's maximum.
- Later reports disagree with each other: S1-03 (LWN, LPC 2024) "typically no more than 100µs at a time"; S1-06 (LWN, LPC 2025) "around 1ms, though there are a few that run for 2-3ms or more … tasks that run for less than 100µs".
- S3-01 Apex Legends per-comm medians of `run_tm_ns` (EWMA runtime per schedule, under `scx_lavd`): `r5apex.exe` 19 974 ns, `Worker 2` 17 376, `wineserver` 8 642, `dxvk-cs` 1 183 292, `dxvk-submit` 52 134, `dxvk-queue` 29 381, `audio_client_ti` 8 540; all rows p50 8 375 ns, p90 125 222, p99 1 291 584. S3-02 Diablo III `Diablo III64.ex` 55 368, `dxvk-submit` 189 184, `dxvk-cs` 241 879; StarCraft II `Play Main Threa` 23 449, `dxvk-cs` 147 325.
- Current encoding (lognormal, p05/p95 reading of the two examples, per-task draw) is the project's; the per-task draw rests on slide 13 "Task execution time is very stable and is predictable using its average" and slide 17 "stable execution time and a stable wait time".

### 4. `frac_wakeups_from_wait` (uniform 0.70–0.75)

- S1-01 slide 14: "70-75% of scheduling is initiated by waiting system calls – such as epoll, pipe_read, futex_wait, etc."; "Preemption (e.g., timer interrupt) takes only 25-30% of scheduling." Pie (S2-03 figure label): `sched_preempt` 28.78 %, `ioctl` 13.25 %, `futex_wait` 5.94 %, `pipe_read` 2.96 %, …
- Read by no tool.

### 5. `frame_period` (16 667 µs)

- No observation ties a Proton game's frame cadence to its task structure (S1 §3, S2 §3, S3 §3).
- Vendor documentation (S2-08): Valve, SteamOS 3.2 note — "The default is 60Hz (which can be frame-limited to 60, 30, and 15fps), but you can now slide it down to 40Hz (with frame limits at 40, 20, and 10fps). Or any number (integer) between"; "30hz = 33.33 ms/frame, and 60hz = 16.66ms/frame. Meanwhile, 40hz is 25 ms/frame"; Steam Deck LCD "Refresh rate | 60Hz", OLED "up to 90Hz"; the 2023-11 unified slider with frame tripling.
- Mechanism (S2-09): gamescope withholds the frame callback on vblanks where `vblank_idx % (refreshHz / targetFPS) != 0`; default limited cycle 16 666 666 ns; clients present FIFO under the limiter. DXVK (S2-10) and MangoHud (S2-12) document their own limiters; Proton documents no VSync knob.
- The LAVD deck's own benchmark (S2-03 slide 29 figure labels): "V-Sync: OFF Framerate Lock: OFF Refresh Rate: 60", average 33 and 40 FPS, an overlay reading "DXVK 60 FPS 16.5 ms" in one screenshot.
- Off-platform: Android studies (S1-09, S1-12, S1-13, S1-14) treat the display refresh (16.7 / 8.3 ms) as the frame deadline; a Windows course study (S1-15) measures VSync at 60 Hz against a 60 FPS cap.
- Elden Ring user claim (S3-10): engine cap 60 FPS falling to 30 FPS under ~1 ms extra delay; unmeasured.

### 6. `chain_length` (16)

- S1-01 slide 12: "There are 15-20 game-specific tasks, which takes 60-70% scheduling."
- S1-04 (OSPM 2025 report): "10-20 tasks are easily involved in finishing a single job".
- S1-06 (LPC 2025 report): "there are often 20 or 30 tasks in a chain that all need to collaborate", some of them outside the game process ("game engine, kernel, and device drivers").
- S2-03 slide 16 figure: the drawn graph has 18 nodes; the game-process tree (tgid 7781) has `Troy.exe`, four `Task worker thr`, `dxvk-cs`, `dxvk-submit`, `winepulse_mainl`, `winepulse_timer`, `FAudio_AudioCli` = 10 nodes.

### 7–8. `tail_idle_gap`, `tail_run`

- No observation of the non-dominant tasks' behaviour (S1 §3 T3, S3 §3 T3). Slide 12 implies the tasks outside the top 30–40 share ~5 % of scheduling; slide 17: "Majority of game tasks shows periodic behavior".
- S3-01 low-frequency comms (sampled `run_freq` per second, `run_tm_ns`): `dxvk-frame` 249 / 4 294 ns, `winedevice.exe` 944 / 8 111, `gameoverlayui` 372 / 21 965, `CQueuedPacketSe` 99 / 6 458, `systemd` 86 / 42 214, `baloo_file_extr` 12 / 4 904 530. Under `scx_lavd`, biased sampling.

### 9–11. Chain structure, head-only TIMER, 16 : 284 split

- S2-03 slide 16 figure, edges with counts (waker → waitee, syscall): `wineserver → Troy.exe epoll (134200)`, `Troy.exe → wineserver pipe_read (58134)`, four `Task worker thr → dxvk-cs futex_wait (~10 000 each)`, `dxvk-cs → dxvk-submit futex_wait (30970)`, `winepulse_mainl ⇄ winepulse_timer`, `winepulse_mainl ⇄ pipewire-pulse`, `pipewire-pulse ⇄ pipewire`, `winepulse_timer → FAudio_AudioCli futex_wait (10213)`, `swapper → CSteamControlle / winedevice.exe sleep`. Window unstated, so counts are not rates.
- S2-03 slide 11 figure: hub around `wineserver` with `redDispatcher1–7` and `wine_xinput_hid` (pipe_read / epoll, counts 85 900–183 350).
- Slide 17: "A sequence of tasks serves for a single job (e.g., from a user input to display update)"; slide 24: "[Task A] --> [Task B] --> [Task C]". No intermediate stage is named in any document.
- Thread roles from source (S2-10, S2-11, S2-13): `dxvk-cs` executes recorded command chunks (waits on a condition variable); `dxvk-submit` submits command lists and runs allocator tasks "somewhat periodically"; `dxvk-queue` waits for GPU completion; `wineserver` is a per-user daemon, each client call a request write and a blocking reply read over per-thread pipes; the Wine audio driver runs one main-loop thread and one timer thread per stream, the timer thread sleeping `mmdev_period_usec` per iteration at `THREAD_PRIORITY_TIME_CRITICAL` (`winepulse_mainloop` / `winepulse_timer_loop` in Proton 8.0, `audio_client_main` / `audio_client_timer` in Proton 9.0 and upstream Wine 11.17); PipeWire loop threads are named by the caller; FAudio mixes in an SDL audio-stream callback thread.
- S3-01/S3-02 confirm the same families by name under four other games (`wineserver`, `winedevice.exe`, `dxvk-cs/submit/queue/frame/shader-l`, `audio_client_ma/ti`, `FAudio_AudioCli`, `pipewire-pulse`), with `wineserver` the most or second-most sampled comm in every log.

### 12. Lane-scaling defense (C-lavd-10, 11, 15)

- Slide 12 statistics as in items 1 and 6 (a scheduling-frequency share).
- Machine of the characterisation: not stated in any of eight Min/LWN documents (S1 §3 T5, S2 §3 T5). Nearest: slide 5 "AMD Van Gogh: x86 8-core CPU" for the Steam Deck; S1-07 slide 3 "Target hardware: SteamDeck (x86 AMD CPU)"; S1-06 "work at Igalia on SteamOS and the Steam Deck"; the S2-03 slide 29 screenshots at 1280 × 800 on battery. Collection method: `perf sched record` via VaporMark (S1-05 slide 6, S2-07), run "on a target device, such as `SteamDeck`" (S2-07 README).

### 13. `validation_stats: referee: none`

- S4 §4: a native open-source game can run on a hosted runner (Xvfb preinstalled; llvmpipe and lavapipe shipped in Ubuntu; fixed input-free workloads: SuperTuxKart `--profile-laps`/`--profile-time`, OpenArena `timedemo` with per-frame `cl_timedemoLog`, 0 A.D. `-autostart … -autostart-ai`, Warzone 2100 `--autogame`, DarkPlaces `-benchmark`, Armagetron `--playback`). A `/proc` sidecar sees thread population, cumulative per-thread CPU and schedule counts (`schedstat`), context-switch counters; not per-schedule distributions or wake gaps. `sudo perf record` is reported working on x64 runners after lowering `perf_event_paranoid`; tracefs undocumented.
- Not observable on a runner: the Proton/Wine/DXVK structure (Proton is a Steam-client tool; no documented headless route), display refresh, GPU-driven wakes. Wine itself runs on a GPU-less Xorg dummy in its own CI (S4-wine-faq).

### 14. `category_source`

- The deck is conference slides (S1-01 citation); LWN reports are news articles. No peer-reviewed publication of the characterisation exists (S1 §3).

### 15. Notes wording

- "frame-critical", "pipeline", "mostly waiting": in no document. Wine linkage: slides 11, 16, 24, not 12 (S2-03).

### 16. Wineserver's place

- Slide 12 files wine among "system tasks"; slide 13 "wineserver:260 usec" as a coordination task; slide 11 hub; slide 16 `wineserver ⇄ Troy.exe` carries the largest edge counts in the graph (134 200 and 58 134).
- S3-01 Apex: `wineserver` 529 of 10 480 samples (one pid), `run_freq` median 54 146 /s, `run_tm_ns` median 8 642 ns, `wake_freq` 84 989, `wait_freq` 60 849. S3-02: `wineserver` 334 / 342 / 603 samples across the Diablo III and StarCraft II logs, the most-sampled comm in the 1-CCD Diablo III log.
- S2-11: what a wineserver call is (request write, blocking reply read), and that all Wine processes of one user share one wineserver.

### 17–21. Registry lines

- Corrected wording follows from items 1, 3, 4, 5 and from S1-03/S1-06 for the LWN entry (qualitative only; its runtime figure differs from slide 13).

## Not found, all classes

- An observation tying a Proton game's frame cadence to its task wake structure (T1).
- A complete scheduler trace of a Proton game with thread names (T2); only sampled `scx_lavd` tables exist (S3-01, S3-02).
- Numbers for the non-dominant tasks' behaviour (T3) beyond the ~5 % complement and the sampled low-frequency rows.
- Task termination counts with a window (T4) beyond slide 12's "only 10% … terminated".
- The machine, core count or game behind slides 12–14 (T5).
- A per-frame dataset for a Proton game with refresh and limiter stated (T1): flightlessmango.com returned 500/502 and openbenchmarking.org was blocked on 2026-09-13; MangoHud logs do not record refresh or the limiter.
