# S3 — public traces and datasets (T1–T4)

Reader class S3. Access date for everything below: 2026-09-13. Source copies under `sources/S3-*/`, each folder carrying a `SHA256SUMS.txt`.

Every number in this record that is not a verbatim quote is a computation and says which file and what computation. The scheduler-sample logs are *sampled*, not complete traces; the sampling rule is quoted from source under S3-03 and governs how every derived count must be read.

## 1. Search log

| # | date | engine / venue | query (exact) | followed | dead ends |
|---|------|----------------|---------------|----------|-----------|
| 1 | 2026-09-13 | WebSearch | `scx_lavd --monitor output sample "run_freq" "wake_freq" game` | sched-ext/scx issue #234 (gist with `scx_lavd` output during Helldivers 2) → S3-01 | lib.rs / deepwiki / docs.rs hits were derivative summaries, not data |
| 2 | 2026-09-13 | WebSearch | `MangoHud benchmark log CSV format columns "frametime" "cpu_load" log file` | MangoHud README, then `src/logging.cpp` raw → S3-05 | mangohud.com, deepwiki: paraphrase only |
| 3 | 2026-09-13 | WebSearch | `openbenchmarking.org "frame time" game Linux Proton result file per-frame data` | wbasile/Open-Game-Benchmarks (2016, Heroku; no data reachable), ValveSoftware/voglperf → S3-08, linuxgamebench.com (counters all 0) | Open-Game-Benchmarks README only; linuxgamebench.com empty |
| 4 | 2026-09-13 | WebSearch | `CapFrameX capture file format JSON "MsBetweenPresents" columns` | CXWorld/CapFrameX README | Windows x64 only — see Not-found |
| 5 | 2026-09-13 | WebSearch | `Steam Deck perf sched record trace game Proton threads "wineserver" "dxvk-cs" trace` | nothing usable | news/guide pages only |
| 6 | 2026-09-13 | WebSearch | `Perfetto trace example game Android sample trace file threads "RenderThread" ui.perfetto.dev example game trace download` | androidperformance.com article → Gracker/SystraceForBlog (files: `demo_app_aosp_scroll.perfetto-trace`, `微信朋友圈滑动卡顿.perfetto-trace`) | not games |
| 7 | 2026-09-13 | WebSearch | `zenodo dataset frame time game Linux Proton trace scheduler` | none relevant | datacenter traces, patents |
| 8 | 2026-09-13 | WebSearch | `Proton game thread count "threads" wine "dxvk-submit" "winepulse" ftrace sched_switch trace github` | Proton issue #5927 (WINE_CPU_TOPOLOGY launch failures) | no thread-population data |
| 9 | 2026-09-13 | WebSearch | `github repository raw traces game scheduling Linux paper "sched_switch" dataset frame time gaming CFS` | slideshare copy of the OSS NA 2024 talk (class S1, not followed) | — |
| 10 | 2026-09-13 | WebSearch | `"scx_lavd" "monitor-sched-samples" OR "--monitor" output "comm=" issue github` | scx_lavd README/source (S3-03) | — |
| 11 | 2026-09-13 | WebSearch | `MangoHud log csv "Steam Deck" frametime github raw log "os,cpu,gpu,ram,kernel,driver"` | mdeguzis/MangoHudPy (tool only), **Igalia/vapormark** → S3-04 | MangoHudPy README has no format spec |
| 12 | 2026-09-13 | WebSearch | `Android GPU Inspector sample trace download game system profiler trace example threads` | developer.android.com/agi pages | AGI ships a sample Vulkan *app*, no sample game trace |
| 13 | 2026-09-13 | WebSearch | `kaggle OR huggingface dataset "frame time" OR "frametime" game benchmark per-frame log` | Kaggle "FPS Benchmark" (ulrikthygepedersen) — aggregate FPS per hardware/game/setting, no per-frame data (see Not-found) | HF hits are LLM benchmarks named "frames" |
| 14 | 2026-09-13 | WebSearch | `gamescope OR "steam deck" perfetto OR ftrace trace game stutter "sched_switch" capture attached` | gamescope wiki "Tracing" → S3-06 | gamescope issues #1056/#575: no attached traces |
| 15 | 2026-09-13 | WebSearch | `flightlessmango.com benchmark log upload compare CSV columns "fps,frametime,cpu_load,gpu_load"` | flightlessmango.com/logs/6181, MangoHud issue #287 | flightlessmango.com returned HTTP 500/502 on every attempt (curl and WebFetch, 3 tries); copy of the 500 page in `S3-x-dead-ends/fm_log6181.html` |
| 16 | 2026-09-13 | WebSearch | `Linux game "number of threads" wine proton "ps -T" OR "htop" thread count game process observed wineserver threads` | none | generic how-to pages |
| 17 | 2026-09-13 | gh api (GitHub issues search) | `repo:sched-ext/scx "monitor" lavd game` | #3750, #3130, #330 fetched; none contain sample tables (grep for `comm=`, `run_freq`, `MSEQ`, `dxvk-`, `wineserver` = 0 hits each) | — |
| 18 | 2026-09-13 | gh api | `repo:sched-ext/scx wineserver` / `"dxvk-cs" OR "dxvk-submit"` / `winepulse` | 3 / 0 / 0 hits; none with traces | — |
| 19 | 2026-09-13 | gh api | `repo:ValveSoftware/Proton "perf sched"` | #9593, #4125 fetched; grep for `perf sched|perf record|sched_switch|trace-cmd` = 0 lines in either body+comments | search index false positives |
| 20 | 2026-09-13 | gh api | `repo:ValveSoftware/Proton gpuvis` / `"trace-cmd record"`; `repo:doitsujin/dxvk "trace-cmd" OR "perf sched" OR "sched_switch"`; `repo:ValveSoftware/gamescope "sched_switch"` | 0 / 0 / 1 (unrelated) / 0 | — |
| 21 | 2026-09-13 | gh api | `repo:sched-ext/scx "mangohud" lavd` | **#296** (Diablo 3 / StarCraft 2 sample logs) → S3-02 | #2496, #3170, #237 no data |
| 22 | 2026-09-13 | gh api | `repo:sched-ext/scx "perf sched" game` | #3512 (Elden Ring) → S3-10 | #3412, #2519, #330 no traces |
| 23 | 2026-09-13 | HuggingFace API `/api/datasets?search=` | `mangohud`, `frametime`, `frame time`, `perfetto`, `sched_switch`, `steam deck`, `proton game`, `ftrace game` | 0 results each | — |
| 24 | 2026-09-13 | Zenodo API `/api/records?q=` | `mangohud`, `frame time linux game`, `perfetto game trace`, `sched_switch game`, `steam deck`, `proton wine game trace`, `ftrace game thread` | HTTP 403 for every query (with and without browser UA) | API blocked; fell back to #25 |
| 25 | 2026-09-13 | WebSearch restricted to zenodo.org | `dataset game frame times OR frametime OR "frame time" Linux OR Android trace threads`; `perfetto OR ftrace OR "sched_switch" trace dataset mobile game Android scheduling` | records 14712442, 6464808, 4470320, 3632184, 10262075, 5032028 — syscall/app-call/failure/metadata datasets, none with game scheduler traces or frame times | — |
| 26 | 2026-09-13 | gh api code search | `repo:phoronix-test-suite/test-profiles mangohud` / `frametime` | 0 / 71 → `pts/libframetime-1.0.0`, `pts/metro2033-redux-1.0.0` → S3-09 | openbenchmarking.org pages: HTTP 403 (WebFetch) and Cloudflare "Just a moment" (curl), copy in `S3-x-dead-ends/ob_metro.html` |
| 27 | 2026-09-13 | gh api code search | `repo:google/perfetto example_android_trace` | `ui/src/core_plugins/dev.perfetto.ExampleTraces/index.ts` → downloaded `storage.googleapis.com/perfetto-misc/example_android_trace` (58,215,373 B) | `strings` on it shows `droid.launcher3`, `ndroid.calendar`, `com.google.usf`, `surfaceflinger`; no game — not saved |
| 28 | 2026-09-13 | WebSearch | `gpuvis sample trace "trace-cmd" game trace download example dat file wine dxvk` | mikesart/gpuvis `traces/amdgpu_trace.zip` → S3-07 | — |
| 29 | 2026-09-13 | WebSearch | `"perf sched" OR "perf record -e sched" wine OR proton game trace "wineserver" analysis blog latency threads` | Level1Techs thread 134714 (compositor discussion, no measurements); Proton #10007 (WINEDEBUG winsock trace, no scheduler data) | — |
| 30 | 2026-09-13 | WebSearch | `Perfetto trace game "Unity" OR "Unreal" Android sample perfetto-trace github download "GameThread" OR "RenderThread" open dataset` | none with a downloadable game trace | Meta Quest docs are how-tos |
| 31 | 2026-09-13 | WebFetch | arxiv.org/abs/2604.27830 (WOOTdroid) | abstract: Pixel 9 / Android 16 Binder tracing; "does not mention any released traces, datasets, repositories" | class S1 anyway |
| 32 | 2026-09-13 | curl | flightlesssomething.ambrosia.one/ and /benchmarks | HTTP 200 but page body is a JS shell ("FlightlessSomething" only) | no server-rendered listing to quote |
| 33 | 2026-09-13 | Steam store API | `appdetails?appids=1172470` | `Apex Legends™` (resolves the filename `1172470_stamps.log` in S3-01) | — |

Google Dataset Search was not queried: it has no non-JS interface reachable from this environment.

## 2. Candidates

### S3-01 — sched-ext/scx issue #234: `scx_lavd` scheduling-sample logs during Helldivers 2 and Apex Legends

**Citation.** ChrisLane, "[scx_lavd] Getting large pauses and stutters in-game", sched-ext/scx issue #234, opened 2024-04-18, https://github.com/sched-ext/scx/issues/234. Attachments: (a) gist https://gist.github.com/ChrisLane/1945f66b5d8a2f36a530ca9ac8abcfa1, revision `568222751f86166f2a56375bd8d91447a974deee`, updated 2024-04-18T22:23:31Z, file `gistfile1.txt` 118,045 B; (b) Galcian79 comment 2024-04-30T17:32:51Z, files `inxi.log` (https://github.com/sched-ext/scx/files/15168677/inxi.log) and `1172470_stamps.log` (https://github.com/sched-ext/scx/files/15168678/1172470_stamps.log, 3,166,871 B).

**Copy.** `sources/S3-01-scx-issue-234/` — `issue234_body.md`, `issue234_comments.md` (via `gh api`, 2026-09-13), `gist_ChrisLane.txt` (SHA-256 `05e1a6d1…e41a94`), `inxi.log` (`6fab1f97…3a04a`), `1172470_stamps.log` (`2158b8a5…d7454f`).

**Passages.**

Issue body (ChrisLane):
> I have observed that I am able to quite reliably reproduce stutters and pauses, sometimes several seconds long while running around my ship in Helldivers 2.
> Here's the output from `sudo scx_lavd` while I was running the game with several stutters in the period (not sure on exact timestamps:
> …
> Distro: Arch Linux / Kernel: 6.8.7-1-cachyos / GPU: AMD Radeon RX 6800 XT (RADV NAVI21) / CPU: AMD Ryzen 9 5900X 12-Core Processor / RAM: 36GB

Gist, lines 1–5 (header row of the sample table; the `|`-separated columns are what every row carries):
> `chris@chrispc% sudo scx_lavd`
> `22:14:16 [INFO] scx_lavd scheduler is initialized`
> `22:14:17 [INFO] | mseq | pid | comm | cpu | vtmc | vddln_ns | elglty_ns | slice_ns | grdy_rt | lat_prio | lat_cri | min_lc | avg_lc | max_lc | static_prio | lat_bst | slice_bst | run_freq | run_tm_ns | wait_freq | wake_freq | cpu_util | sys_ld |`

Gist, line 210 (a game-side row, verbatim):
> `22:17:33 [INFO] |       197 |    41402 | renderer          |   18 |   -1 |   2460000 |         0 |    3000000 |       226 |       15 |      50 |      38 |      43 |      51 |           17 |      -2 |         0 |         3 | 5736565658 |      1935 |    280469 |        5 |      6 |`

multics69 (LAVD author), comment 2024-04-23T02:25:20Z:
> @All -- When collecting the log, if you can run `sudo scx_lavd -s $(nproc)`, it would be super helpful.

Galcian79, comment 2024-04-30T17:32:51Z (the Apex Legends log):
> I started the game with fps unlocked, all graphic settings set to max. I played on the training ground waiting for dxvk to compile the shaders. Didn't notice any stutter. Then i started lavd and took the logs while playing a 10 mins match. I didn't notice any stutter either.

`inxi.log`, lines 1–3 and CPU block:
> `Host: ArchPC Kernel: 6.8.8-273-tkg-sched_ext arch: x86_64 bits: 64`
> `Desktop: KDE Plasma v: 6.0.4 Distro: Arch Linux`
> `Info: 8-core model: AMD Ryzen 7 5800X3D bits: 64 type: MT MCP cache: L2: 4 MiB`

`1172470_stamps.log`, first data rows (verbatim, ANSI colour codes stripped):
> `16:50:02 [INFO] | mseq      | pid      | comm              | cpu  | vtmc | vddln_ns  | elglty_ns | slice_ns   | grdy_rt   | lat_prio | lat_cri | min_lc  | avg_lc  | max_lc  | static_prio  | lat_bst | slice_bst | run_freq  | run_tm_ns | wait_freq | wake_freq | cpu_util | sys_ld |`
> `16:50:02 [INFO] |         4 |    99759 | r5apex.exe        |    8 |   -1 |         0 |         0 |      75000 |         0 |       20 |       0 |       0 |       0 |       0 |           20 |       0 |         0 |         1 |  15000000 |         0 |         0 |        0 |      0 |`

**What a row is (from S3-03, quoted there).** Each row is one scheduling event (`ops.running`) of one task, chosen as "the first N tasks scheduled after the per-interval request"; N = `-s` value (default 1 per second; `-s $(nproc)` shortens the interval). It is not a complete trace, and the selection is biased toward tasks that are scheduled soon after each request.

**Computed (file `1172470_stamps.log`; parse every `[INFO] |` row that is not a header, split on `|`, 23 columns).** 10,480 rows; first row `16:50:02`, last `17:00:56` (10 min 54 s); exactly 16 rows per wall-clock second (min = max = 16, consistent with `-s 16` on an 8-core/16-thread 5800X3D). Distinct `comm`: 72; distinct `pid`: 95. Row counts by comm (top): `r5apex.exe` 2593 (14 distinct pids), `tee` 654, `konsole` 629, `kworker/u32:7` 567, `kworker/u32:0` 546, `wineserver` 529 (1 pid), `Worker 2` 425, `Worker 4` 298, `dxvk-queue` 138, `winedevice.exe` 127 (3 pids), `miles_job_sched` 96, `dxvk-submit` 84 (2 pids), `pipewire-pulse` 40, `audio_client_ti` 38 (3 pids), `audio_client_ma` 32, `IPC:CSteamEngin` 32, `dxvk-cs` 30, `wine_sechost_se` 30, `Xwayland` 21, `WSI swapchain q` 17, `dxvk-frame` 14, `SteamNetworking` 13, `gameoverlayui` 11, `CQueuedPacketSe` 8, `systemd` 7. Full comm set: `CHTTPClientThre, CJobMgr::m_Work, CQueuedPacketSe, CSteamControlle, FAudio_AudioCli, IPC:CSteamEngin, NetLib, QSGRenderThread, SteamNetworking, VizCompositorTh, WSI swapchain q, WaylandEventThr, Worker 2, Worker 4, Xwayland, ananicy-cpp, audio_client_ma, audio_client_ti, baloo_file, baloo_file_extr, dxvk-cs, dxvk-frame, dxvk-queue, dxvk-shader-l, dxvk-submit, fs_async_stream, gameoverlayui, konsole, ksoftirqd/4, ksoftirqd/7, kwin_wayla:cs0, kworker/* (24 names), miles_job_sched, pipewire-pulse, plasmashel:gl0, plasmashell, r5apex.exe, steam, steamwebhelper, systemd, tee, wine_dsound_cap, wine_sechost_se, winedevice.exe, wineserver`.

Per-comm medians over that comm's rows (columns `run_freq` = "scheduling frequency in a second", `run_tm_ns` = "average runtime per schedule", `wake_freq`, `wait_freq`, per S3-03): `r5apex.exe` run_freq 22,038 (max 105,624), run_tm_ns 19,974, wake_freq 169,367, wait_freq 46,373; `wineserver` 54,146 / 8,642 / 84,989 / 60,849; `Worker 2` 23,690 / 17,376 / 173,453 / 41,340; `dxvk-queue` 6,198 / 29,381 / 1,630 / 8,188; `dxvk-submit` 4,160 / 52,134 / 21,510 / 3,204; `dxvk-cs` 514 / 1,183,292 / 9,522 / 2,139; `dxvk-frame` 249 / 4,294 / 788,350 / 248; `winedevice.exe` 944 / 8,111 / 45,407 / 944; `audio_client_ti` 12,065 / 8,540 / 140,894 / 9,438; `pipewire-pulse` 9,764 / 8,729 / 2,675 / 11,254; `gameoverlayui` 372 / 21,965 / 241,180 / 365; `CQueuedPacketSe` 99 / 6,458 / 157,928 / 99; `systemd` 86 / 42,214 / 355,141 / 85. Over all 10,480 rows: `run_tm_ns` p10/p50/p90/p99/max = 2,712 / 8,375 / 125,222 / 1,291,584 / 85,691,669; `run_freq` p10/p50/p90/p99/max = 362 / 28,329 / 95,671 / 186,182 / 381,719; `sys_ld` median 12, max 23.

Family shares of the 10,480 sampled schedules (my own grouping by comm name): kernel/systemd (`kworker*`, `ksoftirqd*`, `systemd`) 4,517 = 43.1%; game-named (`r5apex.exe`, `Worker 2`, `Worker 4`, `miles_job_sched`, `fs_async_stream`) 3,414 = 32.6% over 18 distinct pids; desktop/other (`tee`, `konsole`, `Xwayland`, `kwin_wayla:cs0`, `plasmashell`, `baloo_*`, `ananicy-cpp`, …) 1,383 = 13.2%; wine infra (`wineserver`, `winedevice.exe`, `wine_sechost_se`) 690 = 6.6%; dxvk/vulkan (`dxvk-*`, `WSI swapchain q`) 285 = 2.7%; audio (`pipewire-pulse`, `audio_client_*`, `FAudio_AudioCli`, `wine_dsound_cap`) 113 = 1.1%; steam/launcher 78 = 0.7%. The `tee`/`konsole` rows are the logging pipeline itself.

**Computed (file `gist_ChrisLane.txt`, same parse).** 408 rows, `22:14:17`–`22:21:03`, 1 row per second (default `-s 1`). Distinct comm 41, distinct pid 62. Top comms: `sudo` 56 (the logging shell), `kworker/u66:52` 38, `kworker/u66:26` 35, `kworker/u65:57` 34, `thread pool wor` 33 (11 pids), `kworker/u66:3` 31, `kworker/u65:63` 24, `ad pool !LP wor` 23 (10 pids), `main` 13, `wineserver` 9, `winedevice.exe` 4 (2 pids), `dxvk-queue` 4, `pipewire-pulse` 2, `Window & Input` 2, `audio_client_ma` 2, `renderer` 1. Family shares: kernel/systemd 248 = 60.8%; game-named (`thread pool wor`, `ad pool !LP wor`, `main`, `Window & Input`, `renderer`, `WRRende~ckend#1`, `x67`, `01c0a57c917d2da`) 77 = 18.9% over 28 pids; desktop/other 58; wine infra 14; audio 5; dxvk 4; steam 2. Medians: `thread pool wor` run_freq 26,617, run_tm_ns 11,033; `main` 29,262 / 22,173; `wineserver` 43,871 / 9,573; `dxvk-queue` 3,882 / 37,206. The `renderer` row above carries `run_tm_ns` 5,736,565,658 (5.7 s) with `run_freq` 3 — an outlier as recorded.

**Coverage.**
- T1 Frame cadence — does not cover. No frame times; only "fps unlocked" (Apex, quoted) and no refresh/limiter setting for Helldivers 2.
- T2 Task structure — covers, partially. Object: sampled scheduling events; unit: one `ops.running` event per row; statistics: per-row EWMA `run_freq`, `run_tm_ns`, `wait_freq`, `wake_freq` (no waker identity in this 2024 format — `waker_comm` exists only in the current `SchedSample`, S3-03). Scope: whole system while the game ran; population: everything the scheduler ran, tagged by `comm` and `pid`, so game threads (`r5apex.exe`, `Worker N`, `miles_job_sched`) vs Wine (`wineserver`, `winedevice.exe`, `wine_sechost_se`) vs DXVK (`dxvk-cs/submit/queue/frame/shader-l`, `WSI swapchain q`) vs audio (`pipewire-pulse`, `audio_client_*`, `FAudio_AudioCli`, `wine_dsound_cap`) are distinguishable by name. Thread *counts* are lower bounds (only sampled tasks appear; 95 pids seen in Apex). Roles are not documented here (that is S2's domain).
- T3 Non-dominant tasks — covers weakly: low-`run_freq` comms with their sampled `run_freq`/`run_tm_ns` (e.g. `dxvk-frame` 249/s, `winedevice.exe` 944/s, `gameoverlayui` 372/s, `CQueuedPacketSe` 99/s, `systemd` 86/s, `baloo_file_extr` 12/s with run_tm_ns median 4,904,530). Periodicity is inferable from `run_freq` only; no sleep/termination state.
- T4 Lifetime/termination — does not cover. No exit events; a pid disappearing from samples is not evidence of termination.
- T5, T6 — does not cover.

**One observation?** Two independent single runs: (Helldivers 2, Ryzen 9 5900X 12c/24t, 6.8.7-cachyos, ~6.8 min) and (Apex Legends, Ryzen 7 5800X3D 8c/16t, 6.8.8-tkg-sched_ext, KDE Plasma 6.0.4 Wayland, ~10.9 min). Machine, game and window are named for both. Both are under `scx_lavd`, not EEVDF/CFS, and both are stutter bug reports — not representative runs.

---

### S3-02 — sched-ext/scx issue #296: `scx_lavd -s $(nproc)` logs for Diablo III and StarCraft II under Proton Experimental

**Citation.** pingubot, "scx_lavd: ~20% lower fps in Starcraft 2 and Diablo 3", sched-ext/scx issue #296, opened 2024-05-18, https://github.com/sched-ext/scx/issues/296 (closed). Attachments, comment 2024-05-19T10:31:13Z: `d3_lavd_2ccd.log` (files/15368993), `sc2_lavd_2ccd.log` (files/15368992), `d3_lavd_1ccd.log` (files/15369016), `sc2_lavd_1ccd.log` (files/15369017).

**Copy.** `sources/S3-02-scx-issue-296/` — `scx_296.md` (body + comments via `gh api`), four logs (SHA-256 `d3_lavd_1ccd` `7fd8b8e4974c1350513d30de8778a7845a74d465a9021871831cf61d3aba4aa6`, `d3_lavd_2ccd` `08bc68c2…b83c`, `sc2_lavd_1ccd` `ed4cde2e…9263`, `sc2_lavd_2ccd` `5a981dad…b128`).

**Passages.**

Body:
> In Starcraft 2 and Diablo 3 i get roughly 20 percent less fps compared to eevdf.
> Those games are heavily using one or two cores.
> Tested on: Endevaour OS / Ryzen 5950x ( with one CCD disabled as the readme mentioned sxc_lavd is not optimized for more than 1 ccd cpus) / 32Gb Ram

multics69, 2024-05-19T01:48:22Z:
> Could you please upload the log of lavd with `./scx_lavd -s $(nproc)` for each game?

pingubot, 2024-05-19T10:31:13Z:
> Attached find first round of logs with both ccds enabled. I was in game in campaign in d3 and sc2 for half a minute or less before leaving the game again. Hope thats enough time.
> Tested with: Linux 6.9-tkg, amd_pstate=active
> Commit: 17c0c10b4efbfe9819ba818396b1c3438fc7e45c
> What i did: Start battlenet / Start lavd / Start d3 game / Stop d3 game / Stop lavd / start lavd / Start sc2 game / Stop sc2 game / stop lavd

pingubot, 2024-05-27T17:29:30Z:
> I am using Proton Experimental for sc2 and d3. You can do that by adding battle.net as a third party application to the steam library.
> OS: EndeavourOS (Arch) / Kernel: 6.9.x TKG / DE: Plasma 6 on wayland

pingubot, 2024-06-14T14:33:03Z:
> Did with both ccds on and its 300fps (lavd) vs 380fps (6..9.4 linux-tkg cfs) in Diablo 3.

vax-r, 2024-05-19T07:46:14Z (Left 4 Dead 2, images only — no data file):
> Same issue happens for **Left 4 Dead 2** on ubuntu 24.04. I use mangohud to record the FPS for EEVDF and `scx_lavd` , the latter provide lower "low 1% FPS" .

Log header (all four files, ANSI stripped) — this build has 22 columns (`perf_cri`, `avg_pc` replace `lat_cri/min_lc/max_lc`):
> `| mseq | pid | comm | cpu | vtmc | vddln_ns | elglty_ns | slice_ns | grdy_rt | lat_prio | avg_lc | static_prio | lat_bst | slice_bst | run_freq | run_tm_ns | wait_freq | wake_freq | perf_cri | avg_pc | cpu_util | sys_ld |`

**Computed (same parse; header taken from each file).**
- `d3_lavd_2ccd.log`: 1,600 rows, `10:22:00`–`10:22:49`, 32 rows/s (5950X both CCDs = 32 threads → `-s 32`); 47 comms, 95 pids. `Diablo III64.ex` 590 rows over **38 distinct pids**, run_freq median 4,462, run_tm_ns median 55,368, p90 304,429; `wineserver` 334 (40,931 / 9,888); `http` 227 (Battle.net/CEF); `CrBrowserMain` 104; `winedevice.exe` 49; `Xwayland` 24; `dxvk-submit` 22 (run_tm_ns median 189,184, p90 1,698,807); `dxvk-queue` 14; `dxvk-cs` 5 (run_tm_ns median 241,879); `dxvk-frame` 5; `audio_client_ma` 10; `pipewire-pulse` 15. Family shares: game-named 36.9%, steam/launcher (Battle.net `Agent.exe`, `http`, `CrBrowserMain`, `BGS:0`, …) 26.1%, wine infra 24.7%, kernel 4.1%, dxvk 3.2%, desktop 3.1%, audio 1.9%.
- `d3_lavd_1ccd.log`: 1,312 rows, 16 rows/s, 45 comms, 64 pids; `wineserver` 342 rows is the most-sampled comm, `Diablo III64.ex` 245 over 13 pids (run_freq median 18,286, run_tm_ns 17,633, p90 286,205); `dxvk-cs` 20 rows run_tm_ns median 583,226.
- `sc2_lavd_2ccd.log`: 3,200 rows, `10:23:14`–`10:24:53`, 32 rows/s, 55 comms, 108 pids. `Play Main Threa` 1,004 rows over **41 pids** (run_freq median 9,676, run_tm_ns median 23,449, p90 5,083,857); `wineserver` 603; `http` 389; `Core Worker Thr` 147 (3 pids); `dxvk-queue` 105; `dxvk-submit` 79; `dxvk-cs` 75 (run_tm_ns median 147,325); `audio_client_ma` 63; `pipewire-pulse` 61; `audio_client_ti` 53; `dxvk-frame` 9 (run_freq 329). Family shares: game-named 36.1%, wine infra 22.1%, steam/launcher 20.3%, dxvk 9.0%, audio 5.6%, kernel 5.2%, desktop 1.8%.
- `sc2_lavd_1ccd.log`: 1,840 rows, 16 rows/s, 56 comms, 91 pids; `Play Main Threa` 478 over 22 pids, run_freq median 191, run_tm_ns median 627,583, p90 11,542,528.

Note: the many pids under one game comm (`Diablo III64.ex` ×38, `Play Main Threa` ×41) reflect Wine threads inheriting the process/thread name; the game-side thread population is therefore at least that many threads but the samples cannot say what each does.

**Coverage.**
- T1 — does not cover (single aggregate "300fps (lavd) vs 380fps … cfs" claim, no frame data; no refresh/limiter stated).
- T2 — covers, partially, same object/unit/statistics as S3-01; population: whole system for four ~30–110 s windows; Wine/DXVK/audio/game names distinguishable; the Battle.net launcher (`Agent.exe`, `http`, `CrBrowserMain`, `BGS:0`) is a large non-game share (20–26% of samples).
- T3 — weak, as S3-01 (e.g. `dxvk-frame` ~330/s, `winedevice.exe` ~947/s, `Agent.exe` 99/s, `steam` 4/s).
- T4 — does not cover.
- T5, T6 — does not cover.

**One observation?** One user, one machine (Ryzen 9 5950X, 16c/32t, Linux 6.9-tkg, EndeavourOS, Plasma 6 Wayland, Proton Experimental), two games, two CCD configurations; windows 49 s, 81 s, 99 s, 114 s; machine, game and window named; scx_lavd commit `17c0c10b` named. Under `scx_lavd`, not the stock scheduler.

---

### S3-03 — `scx_lavd` source: what a sample row means (supporting record for S3-01/S3-02)

**Citation.** sched-ext/scx, `scheds/rust/scx_lavd/src/main.rs` and `src/bpf/main.bpf.c`, `src/bpf/intf.h` at commit `f53c29759e60cf20ee435e7deb62790e74f63917` (2024-04-09, the last change to `main.rs` before the S3-01 gist); `main.rs` at `17c0c10b4efbfe9819ba818396b1c3438fc7e45c` (S3-02's commit); `src/stats.rs` and `README.md` at `main` = `8b2479571c0768310510c061960d2c40cb64d160` (2026-09-11). https://github.com/sched-ext/scx.

**Copy.** `sources/S3-03-scx-lavd-source/` (six files, SHA-256 in `SHA256SUMS.txt`).

**Passages.**

`main.rs` @f53c297, lines 46–49:
> `/// The number of scheduling samples to be reported every second (default: 1)`
> `#[clap(short = 's', long, default_value = "1")]`
> `nr_sched_samples: u64,`

`main.rs` @f53c297, lines 241–248:
> `let mut interval_ms = 1000;`
> `if self.intrspc.cmd == LAVD_CMD_SCHED_N && self.intrspc.arg > self.nr_cpus_onln { // More samples, shorter sampling interval. let f = self.intrspc.arg / self.nr_cpus_onln * 2; interval_ms /= f; }`

`main.bpf.c` @f53c297, lines 544–570 (sample selection; called from `lavd_running`, line 1835 `try_proc_introspec_cmd(p, taskc, LAVD_CPU_ID_HERE);`):
> `/* introspec_arg is the number of schedules remaining */`
> `cur_nr = intrspc.arg;`
> `for (i = 0; cur_nr > 0 && i < LAVD_MAX_CAS_RETRY; i++) { prev_nr = __sync_val_compare_and_swap(&intrspc.arg, cur_nr, cur_nr - 1); /* CAS success: submit a message and done */ if (prev_nr == cur_nr) { submit_task_ctx(p, taskc, cpu_id); break; } … }`

`main.bpf.c` @f53c297, lines 651–662 and 1281–1296:
> `new_freq = LAVD_TIME_ONE_SEC / interval; ewma_freq = calc_avg(old_freq, new_freq); return ewma_freq;`
> `/* Since this is the start of a new schedule for @p, we update run frequency in a second using an exponential weighted moving average. */ if (have_scheduled(taskc)) { wait_period = now - taskc->last_quiescent_clk; interval = taskc->run_time_ns + wait_period; taskc->run_freq = calc_avg_freq(taskc->run_freq, interval); }`

`intf.h` @f53c297, lines 152–157:
> `u64 acc_run_time_ns; /* accmulated runtime from runnable to quiescent state */`
> `u64 run_time_ns; /* average runtime per schedule */`
> `u64 run_freq; /* scheduling frequency in a second */`
> `u64 wake_freq; /* waking-up frequency in a second */`

`main.bpf.c` @f53c297, lines 1315–1330 (what `run_tm_ns` accumulates):
> `Update task's run_time. When a task is scheduled consecutively without ops.quiescent(), the task's runtime is accumulated for statistics. Suppose a task is scheduled 2ms, 2ms, and 2ms with the time slice exhausted. If 6ms of time slice was given in the first place, the task will entirely consume the time slice. Hence, the consecutive execution is accumulated and reflected in the calculation of runtime statistics.`

`stats.rs` @main, current `SchedSample` field docs (lines 135–176), for comparison with the 2024 columns:
> `#[stat(desc = "Waker's process ID")] pub waker_pid: i32,` / `#[stat(desc = "Waker's task name")] pub waker_comm: String,` / `#[stat(desc = "How often this task is scheduled per second")] pub run_freq: u64,` / `#[stat(desc = "Average runtime per schedule")] pub avg_runtime_wall: u64,` / `#[stat(desc = "How frequently this task waits for other tasks")] pub wait_freq: u64,` / `#[stat(desc = "How frequently this task wakes other tasks")] pub wake_freq: u64,`

`README.md` @main:
> scx_lavd is initially motivated by gaming workloads. It aims to improve interactivity and reduce stuttering while playing games on Linux.

**Coverage.** T2 — covers the *definitions* only (what `run_freq`, `run_tm_ns`, `wake_freq`, `wait_freq` mean and how rows are chosen); no observations. Current-format `--monitor-sched-samples` output (with `WKER_COMM`) was searched for (log rows 10, 17) and no published sample of it during a game was found. T1, T3–T6 — does not cover. Not an observation.

---

### S3-04 — Igalia/vapormark: the SteamOS benchmark harness (tool; no published data)

**Citation.** Igalia, *vapormark*, GitHub, default branch `main`, commit `ad0f9d6821f3c6eddad3fe298e93799809811fce` (2025-07-04). https://github.com/Igalia/vapormark. Files read: `README.md`, `bin/schedmon`, `bin/procmon`, `config/MangoHud.conf`.

**Copy.** `sources/S3-04-vapormark/` (SHA-256 in `SHA256SUMS.txt`).

**Passages.**

README lines 1–6:
> `vapormark` is a benchmark framework developed for measuring various performance metrics (e.g., throughput, latency, and tail latency) and the process states (e.g., backend stall, energy consumption) while running a program on Linux. It especially targets `SteamOS` -- a Linux-based gaming device --but most features are genetically useful in regular Linux environments.

README lines 83–92 (`procmon`):
> `procmon` collects four types of information: 1) scheduler's wakeup events, 2) CPU's c-state, 3) CPU's energy consumption, and 4) processor's performance monitoring data (e.g., instruction per cycle). … The runtime overhead is not marginal so it can be run with an application level benchmark (like game).

`bin/procmon`, the `--sched` command:
> `sh_cmd = "trace-cmd record -e sched_wakeup -o %s > /dev/null" % dat`

README lines 181–184 (`schedmon`):
> `schedmon` collects the detailed system-wide scheduling activities. It internally relies on `perf sched record` command.

`bin/schedmon`, the record and report commands:
> `sh_cmd = "perf sched record -ag -o %s sleep 36500d" % log`
> `sh_cmd = "perf sched latency -i %s >  %s" % (raw_log, log)` / `"perf sched map -i %s >  %s"` / `"perf sched timehist -SMVwng -i %s >  %s"`

README lines 280–301 (`schedinsight` options):
> `-s MINSCHED, --minsched MINSCHED  set the minimum number of schedules for task analysis`
> `-t TIMELIMIT, --timelimit TIMELIMIT  time limit to draw a graph in seconds`

README lines 146–178 (MangoHud on Steam Deck, and the in-game benchmarks used):
> *The game must be launched in **Desktop Mode (not in Gaming Mode)** to log FPS and other system stats.*
> Following games provide in-game benchmarks: Far Cry: New Dawn `Options -> Benchmark` / A Total War Saga: Troy `Options -> Graphics -> Advanced -> Benchmark` / Cyber Punk 2077 `Settings -> Graphics -> Quick Preset, Run Benchmark` / Factorio `factorio --benchmark … --benchmark-ticks 1000 --disable-audio`

`config/MangoHud.conf` (non-comment lines):
> `gpu_stats / cpu_stats / ram / swap / fps / frametime / frame_timing / log_interval=0 / output_folder=/home/deck/mangologs-vapormark`

**Coverage.** This is the toolchain, not data: the repository tree (listed via `gh api git/trees`, 20 blobs) contains no logs, traces or results. T1 — covers the *instrument* (MangoHud with `log_interval=0` on Steam Deck, desktop mode) but no observation. T2/T3 — covers the instrument (`perf sched record -ag`, `trace-cmd record -e sched_wakeup`, a "minimum number of schedules for task analysis" threshold in `schedinsight`) but no observation. T4 — `perf sched record` output would include exits only if perf's sched events do; not stated in this repo. T5 — this is the S1/S2 readers' question; the repo names no machine or game for any published characterisation. T6 — does not cover. Not an observation.

---

### S3-05 — MangoHud: the frame-time log format (what any MangoHud/flightlessmango log records)

**Citation.** flightlessmango/MangoHud, `README.md` and `src/logging.cpp` at `master` = `1319124ac4f22fec75246f6ffbf3b912dc2a6865` (2026-09-12); issue #287 "FPS logging format is undocumented". https://github.com/flightlessmango/MangoHud.

**Copy.** `sources/S3-05-mangohud/` — `mangohud_README.md` (`e6844039…3735a`), `mangohud_logging.cpp` (`85ee78de75f984ef27aa94f8b4aab2811a163e958d9b0a59798ddd00d410b7d4`), `issue287_body.md`.

**Passages.**

`src/logging.cpp` lines 194–203 (file header rows):
> `out << "os," << "cpu," << "gpu," << "ram," << "kernel," << "driver," << "cpuscheduler" << endl;`
> `out << "fps," << "frametime," << "cpu_load," << "cpu_power," << "gpu_load," << "cpu_temp," << "gpu_temp," << "gpu_core_clock," << "gpu_mem_clock," << "gpu_vram_used," << "gpu_power," << "ram_used," << "swap_used," << "process_rss," << "cpu_mhz," << "elapsed" << endl;`

`src/logging.cpp` lines 215–230 (one data row; last column is elapsed nanoseconds since log start):
> `output_file << logArray.back().fps << ","; output_file << logArray.back().frametime << ","; … output_file << std::chrono::duration_cast<std::chrono::nanoseconds>(logArray.back().previous).count() << "\n";`

`src/logging.cpp` lines 306–324 (sampling loop — rows are time-driven, not frame-driven):
> `void Logger::logging(){ wait_until_data_valid(); while (is_active()){ try_log(); this_thread::sleep_for(std::chrono::milliseconds(log_interval)); } clear_log_data(); }`
> `void Logger::try_log() { … currentLogData.previous = elapsedLog; currentLogData.fps = fps; currentLogData.frametime = frametime; m_log_array.push_back(currentLogData); writeToFile(); …`

README, option table:
> `log_interval` | Change the default log interval in milliseconds. Default is `0`
> `log_versioning` | Adds more headers and information such as versioning to the log. This format is not supported on flightlessmango.com (yet)
> `fps_limit` | Limit the apps framerate. Comma-separated list of one or more FPS values. `0` means unlimited
> `fps_limit_method` | If FPS limiter should wait before or after presenting a frame. Choose `late` (default) for the lowest latency or `early` for the smoothest frametimes

README, "FPS logging":
> Log files can be (batch) uploaded to [FlightlessMango.com](https://flightlessmango.com/games/user_benchmarks), which will then take care of creating a frametime graph and a summary with 1% min / average framerate / 97th percentile in a table form and a horizontal bar chart form.
> - Uploaded benchmarks are public: you can share them with anyone by simply giving them the link.

`src/logging.cpp` lines 83–88 (summary file columns):
> `out << "0.1% Min FPS," << "1% Min FPS," << "97% Percentile FPS," << "Average FPS," << "GPU Load," << "CPU Load," << "Average Frame Time," …`

Issue #287 body (2020-08, reporting the then-format):
> `os,cpu,gpu,ram,kernel,driver` … `88.3473,12,100,169` … "is it time stamp from the start of logging in microseconds maybe?" … "the absence of frame time information in the log"

**Coverage.** T1 — covers the *record format* of the only widely-used Linux/Proton frame-time logger: per row `fps`, `frametime`, `elapsed` (ns), plus the `cpuscheduler` header field; rows are emitted by a logger thread every `log_interval` ms (default 0 → as fast as the loop runs), each carrying the *current* `frametime` value, so a row is not guaranteed to be one frame. The header records OS/CPU/GPU/kernel/driver/cpuscheduler but not display refresh or the `fps_limit` in force; the `fps_limit`/`fps_limit_method` options document what a limiter does. No thread-level data. T2–T6 — does not cover. Not an observation (no public log could be retrieved: flightlessmango.com returned 500/502 on all attempts, log row 15).

---

### S3-06 — gamescope wiki "Tracing": the ftrace event set Valve documents for gamescope sessions (tool)

**Citation.** ValveSoftware/gamescope wiki, page "Tracing", last commit `c0ee2ea50772c6307f09d72a06ebdff6b80d9428` (Simon Ser, 2021-06-09). https://github.com/ValveSoftware/gamescope/wiki/Tracing (cloned from `gamescope.wiki.git`).

**Copy.** `sources/S3-06-gamescope-tracing-wiki/Tracing.md` (`f8136f23…ba5`).

**Passages.**
> gamescope can take advantage of the Linux ftrace infrastructure for event tracing.
> 1. Start the tracing script below 2. Start gamescope 3. Stop the script 4. Use [gpuvis](https://github.com/mikesart/gpuvis) to visualize the resulting trace
> `trace-cmd record -i -e "sched:sched_switch" -e "sched:sched_process_exec" -e "sched:sched_process_fork" -e "sched:sched_process_exit" -e "amdgpu:amdgpu_vm_flush" -e "amdgpu:amdgpu_cs_ioctl" -e "amdgpu:amdgpu_sched_run_job" -e "*fence:*fence_signaled" -e "drm:drm_vblank_event" -e "drm:drm_vblank_event_queued" -e "i915:i915_flip_request" -e "i915:i915_flip_complete" …`

**Coverage.** T1 — instrument only: `drm_vblank_event` and flip events would tie frame presentation to the scheduler timeline, but no trace is published. T2 — instrument only (`sched_switch`). T4 — instrument only: this is the one documented Steam-side recipe that captures `sched_process_fork` / `sched_process_exit`, i.e. thread lifetimes. No observation; no machine/game.

---

### S3-07 — gpuvis sample trace `traces/amdgpu_trace.zip` (a 2017 SteamVR trace-cmd capture)

**Citation.** mikesart/gpuvis, `traces/amdgpu_trace.zip` (1,181,578 B) at `master`; wiki pages `Overview.md`, `Running.md`, `Frame-Markers.md`. https://github.com/mikesart/gpuvis.

**Copy.** `sources/S3-07-gpuvis-sample-trace/` — `amdgpu_trace.zip` (`e9a813d0…f61ee`), the three wiki pages.

**Passages.**

`Running.md`:
> Sample trace file in the gpuvis repository:
> `$ unzip -l traces/amdgpu_trace.zip` → `9469952  2017-07-19 13:57   traces_x/amdgpu.dat`

`Frame-Markers.md`:
> A simple frame marker is to use vblanks. Ie: … `$name = drm_vblank_event && $crtc = 1` … 212 frames, ~11ms apart
> For the sample trace, set: Left Frame Marker: `$buf =~ "[Compositor] Before wait query` Right Frame Marker: `$buf =~ "[Compositor] After wait query`

**Computed** (`strings -n 3 traces_x/amdgpu.dat | grep -i 'wine|dxvk|steam|vr|…' | sort | uniq -c`): `steam` 5,902; `vrmonitor` 691; `vrcompositor` 595; `vrserver` 544; `vrdashboard` 286; `[Compositor] Before wait query` 251; `[Compositor] After wait query` 250; no `wine`, `dxvk` or `.exe` strings. The traced workload is the SteamVR compositor stack, not a game; the machine is not named anywhere in the repo or wiki.

**Coverage.** T1 — one observation of *compositor* frame cadence ("212 frames, ~11ms apart" on `drm_vblank_event crtc 1`, ≈ 90 Hz) in a trace that also has `sched_switch`; not a game, not Proton. T2 — the `.dat` contains sched_switch for the whole system (could be parsed with `trace-cmd report`, not done here: no trace-cmd on this host) but the process is SteamVR. T3/T4 — the event set is unknown without parsing; not attempted. T5/T6 — does not cover. Machine unnamed; window ≈ the 212 frames.

---

### S3-08 — ValveSoftware/voglperf: per-frame frame-time log format for native Linux OpenGL games

**Citation.** ValveSoftware/voglperf, `README.md` at `master` = `05d2b254698697ff341b4b33b28243eea9698f6d` (2018-05-22). https://github.com/ValveSoftware/voglperf.

**Copy.** `sources/S3-08-voglperf/README.md` (`11448d8e…6579`).

**Passages.**
> Benchmarking tool for Linux OpenGL games. Spews frame information, logs frametimes.
> `# Feb 12 16:02:20 - glxspheres64` / `# 3414.30 fps frames:3417 time:1000.79ms min:0.23ms max:15.00ms` / `0.42` / `0.34` / `0.30` …
> (each subsequent line is one frame's duration in milliseconds)

**Coverage.** T1 — covers the format only: one line per frame, milliseconds, for OpenGL apps via `LD_PRELOAD`; the sample shown is `glxspheres64` uncapped (3414 fps). No Proton/Vulkan path, no thread data. T2–T6 — does not cover. Not a game observation.

---

### S3-09 — Phoronix Test Suite `pts/libframetime` and the game profiles that use it (OpenBenchmarking per-frame latency dumps)

**Citation.** phoronix-test-suite/test-profiles at `master` = `d2f1a150d388bd062737b445891edda0780f7e25` (2024-11-23): `pts/libframetime-1.0.0/{test-definition,results-definition,install.sh,downloads}.xml`, `pts/metro2033-redux-1.0.0/{install.sh,results-definition.xml}`; clbr/libframetime `README.asciidoc` (blob `b99156c8…`). https://github.com/phoronix-test-suite/test-profiles ; https://github.com/clbr/libframetime.

**Copy.** `sources/S3-09-pts-libframetime/`.

**Passages.**

`pts/libframetime-1.0.0/results-definition.xml`:
> `<OutputTemplate>csv-dump-frame-latencies</OutputTemplate>`

`pts/metro2033-redux-1.0.0/install.sh`:
> `HOME=$DEBUG_REAL_HOME LIBFRAMETIME_FILE=$LOG_FILE LD_PRELOAD=$TEST_EXTENDS/libframetime/libframetime.so ./metro  -benchmark benchmarks\\\\benchmark33 -bench_runs 1 -close_on_finish`

`pts/metro2033-redux-1.0.0/results-definition.xml`:
> `<OutputTemplate>libframetime-output</OutputTemplate>`

clbr/libframetime README:
> A preloadable library, able to dump the frame times of any OpenGL application on Linux, on any driver.
> `Min/avg/max frametimes (us):    166 / 625.626 / 5955` … `50/90/95/99 percentiles (us):   410 / 434 / 589 / 5018`

Code search (`repo:phoronix-test-suite/test-profiles frametime`, 71 hits) lists the game profiles built on it: `ue4-matinee`, `ue4-atlantis`, `ue4-mountains`, `ue4-elemental`, `metro2033-redux`, `metroll-redux`, `breaking-limit`, `ashes-escalation`, `basemark`, `ddnet`, `civbe`, `civilization-vi`.

**Coverage.** T1 — covers the format for *native* Linux OpenGL benchmark runs: per-frame latencies (µs) dumped by `libframetime` and stored by PTS as `csv-dump-frame-latencies`; results are uploaded to openbenchmarking.org, but every openbenchmarking.org page was blocked (HTTP 403 / Cloudflare challenge, log row 26), so no result with its machine and per-frame values could be quoted. No Proton profile uses it (no `mangohud` hit in the profile tree). No thread data. T2–T6 — does not cover. Not an observation retrieved.

---

### S3-10 — sched-ext/scx issue #3512: Elden Ring frame-cap behaviour under alternative schedulers (claim, no data file)

**Citation.** LukasF1337, "scx_cake, scx_pandemonium: inconsistent framtimes in the game Elden Ring", sched-ext/scx issue #3512, opened 2026-04-05, closed. https://github.com/sched-ext/scx/issues/3512.

**Copy.** `sources/S3-10-scx-issue-3512/scx_3512.md` (`5c86845e9052426f8d9a83b7c889af1f26722bf69d93d96839c2599ae2dcfbb4`).

**Passages.**

Body:
> If you switch the scheduler to scx_cake or scx_pandemonium with default settings you get inconsistent frametimes in the game Elden Ring. With scx_cake you get microstutter and with scx_pandemonium you get stutter.
> I made screenshots to illustrate: [https://cloud.code-rage.org/index.php/s/DW8ioLreLZywooT]

LukasF1337, 2026-04-17T17:58:25Z:
> with EEVDF it runs fine. Out of curiosity I also tested a few other schedulers and scx_lavd, scx_beerland, scx_flash, scx_bpfland, scx_cosmos in their default modes are also affected by this specific place in Elden Ring.
> I think in Elden Ring game engine there are some timing assumptions and if it exceeds some time limit it immediately switches from the default 60 fps cap to 30 fps, intentionally delaying the frame (in a way ignoring variable refresh rates). So I imagine that if the scheduler has some minor 1 ms delay somewhere compared to EEVDF it already chokes the engine.

**Coverage.** T1 — a user's unmeasured claim that Elden Ring has an engine-side 60 fps cap that falls to 30 fps, and a claim that a ~1 ms scheduling delay triggers it; screenshots only (external host, not fetched); no machine named beyond the issue's scheduler list. Not usable as a number; recorded because it is the only public statement found tying a Proton game's frame cadence to scheduler latency. T2–T6 — does not cover.

## 3. Not found

- **T1, a public per-frame frame-time dataset for a Proton game with refresh/limiter stated.** Searched: log rows 2, 3, 7, 11, 13, 15, 23, 24, 25, 26, 32. MangoHud logs are the standard instrument (S3-05) and are public on flightlessmango.com, but the site returned HTTP 500/502 for every page on 2026-09-13 and FlightlessSomething serves a JS-only shell; HuggingFace returned 0 datasets for every relevant term; the Zenodo API returned 403 and the zenodo.org web hits were syscall/app-call/failure datasets; openbenchmarking.org was Cloudflare-blocked. The Kaggle "FPS Benchmark" dataset (ulrikthygepedersen; description: "This dataset contains FPS measurement of video games executed on computers. Each row of the dataset describes the outcome of FPS measurement (outcome is attribute FPS) for a video game executed on a computer.") is one aggregate FPS per (CPU, GPU, game, resolution, setting) with no per-frame data, no OS field quoted, and no timing of any thread — it does not cover T1. CapFrameX (README: "Windows x64" only; captures via PresentMon `MsBetweenPresents`) is Windows-only and therefore out of scope for Linux/Proton.
- **T1, an observation tying frame cadence to a game's task wake structure.** Nothing found beyond the unmeasured Elden Ring claim (S3-10) and the gpuvis SteamVR compositor sample (S3-07, not a game). Rows 5, 14, 19, 20, 29.
- **T2, a complete scheduler trace (perf sched / ftrace / Perfetto) of a Proton game with thread names.** Not found. The only public scheduler-level records of Proton games are the sampled `scx_lavd` tables in S3-01/S3-02 (Helldivers 2, Apex Legends, Diablo III, StarCraft II — four games, three machines, all under `scx_lavd`, all from stutter/fps bug reports). No Steam Deck capture at all. Rows 5, 8, 17–22, 29.
- **T2/T3, Android/mobile game traces with thread-level data.** Not found: Perfetto's public example trace is a launcher/calendar session (row 27); the androidperformance.com traces are a demo scrolling app and WeChat (row 6); AGI ships a sample Vulkan app, not a trace (row 12); no Unity/Unreal game trace is published for download (row 30); WOOTdroid publishes no traces (row 31).
- **T3, numbers for what non-dominant tasks do (periodic/sleeping/terminated).** Only the sampled `run_freq`/`run_tm_ns` values in S3-01/S3-02 for low-frequency comms; nothing states sleep or termination.
- **T4, counts of a game's tasks terminating during play.** Nothing found. The only documented capture recipe that records `sched_process_exit` is the gamescope tracing script (S3-06), with no published trace. Rows 8, 14, 16, 17–20.
- **Any dataset counting threads/processes of a running Wine/Proton game.** Nothing found (rows 8, 16, 18). The sampled logs give lower bounds only (S3-01: 95 pids seen in Apex Legends over 10.9 min; S3-02: 108 pids in StarCraft II over 99 s, with 41 distinct pids named `Play Main Threa` and 38 named `Diablo III64.ex`).
- **GitHub repositories publishing raw traces alongside a gaming-scheduler paper or tool.** vapormark (S3-04) publishes the tool with no data; gpuvis publishes one SteamVR trace (S3-07); no repository with raw game scheduler traces was found (rows 9, 28).
