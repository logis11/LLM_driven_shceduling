# Declared scheduling classes — audit of the measured entries

D4's step (1): each measured entry's observed scheduling policy and nice value, read from its campaign's raw records. Taskstats rows (`ac_sched`, `ac_nice`, one per exiting thread on the measured CPU, `type = pid`) exist for the build and background families only; the interactive, playback, desktop and session families kept `perf sched timehist` text, which carries neither policy nor priority (`campaign/run.sh:156–162`, `desktop/run.sh`, `session/run.sh`: `perf.data` is removed after `timehist` in full mode).

One full repeat per subject, its taskstats files read from the release by HTTP range reads of the zip (2026-10-07). Policy codes per `include/uapi/linux/sched.h`: 0 NORMAL, 3 BATCH, 5 IDLE. A `SCHED_IDLE` task's nice value has no effect (`sched(7)`).

| entry | release, asset | phase file | observed |
|---|---|---|---|
| `compiler-child`, `build-orchestrator` | `meas-ci-build-2026-09-18`, `meas-build-r17.zip` | `taskstats.build-j8-warm.tsv` | NORMAL, nice 0: all 29 037 tasks (`sh`, `rm`, `gcc`, `cc1`, `as`, …) |
| `module-build-orchestrator`, `module-compiler-child` | `meas-ci-background-2026-10-02`, `…-dkms-r10-full-36987468347.zip` | `taskstats.dkms-install.tsv` | NORMAL, nice 0: 16 795 tasks; NORMAL, nice 19: `dpkg` ×15, `apt-check` ×3 |
| `package-upgrade` | `meas-ci-background-2026-10-01`, `…-upgrade-r3-full-36847096521.zip` | `taskstats.upgrade-install.tsv` | NORMAL, nice 0: 913 tasks; NORMAL, nice 19: `dpkg` ×5, `apt-check` ×1 |
| `file-indexer` | `meas-ci-background-2026-10-02b`, `…-tracker-r3-full-37014118970.zip` | `taskstats.tracker-index.tsv` | IDLE, nice 19: all 68 Tracker threads (`pool-tracker-mi`, `single`, `pool-tracker-ex`, `gmain`, `pool-spawner`, …); NORMAL: `systemd-tmpfile`, a kworker |
| `incremental-backup` | `meas-ci-background-2026-10-04`, `…-dejadup-r25-full-37180238545.zip` | `taskstats.dejadup-incremental.tsv` | IDLE: `duplicity` ×23, `gpg` ×15 and Déjà Dup's own threads, 103 tasks; NORMAL, nice 0: the session's `dbus-daemon` ×16, `gsettings`, `gnome-keyring-d` and others, 48 tasks |
| `file-archiver` | `meas-ci-background-2026-09-19`, `meas-background-7z-r6-full.zip` | `taskstats.7z-mmt8-warm.tsv` | NORMAL, nice 0: `7z` ×34 |
| `game-download` | `meas-ci-background-2026-09-19`, `meas-background-steamcmd-r32-full.zip` | `taskstats.steam-fresh-shaped.tsv` | NORMAL, nice 10: `CGenericAsyncFi` ×55, `COfflineMessage` ×2, `CContentUpdateC` ×2; NORMAL, nice 0: `CHTTPClientThre`, `steamcmd` and the rest of SteamCMD's thread group, 25 threads; 12 other tasks, not the entry's (the runner agent's `.NET` threads ×3, `bash` ×2, `uname` ×2, `dirname`, `basename`, `run-parts`, `cron`, a kworker) |
| `cpu-batch` (`python`) | `meas-ci-background-2026-10-03`, `…-mnist-r1-full-37091275421.zip` | `taskstats.mnist-train.tsv` | NORMAL, nice 0 |
| `cpu-batch` (`kdenlive_render`) | `meas-ci-background-2026-10-03c`, `…-kdenlive-r16-full-37126535233.zip` | `taskstats.kdenlive-export.tsv` | NORMAL, nice 0: `melt-7`, `kdenlive_render` |
| `video-transcoder` | `meas-ci-background-2026-10-03b`, `…-handbrake-r3-full-37109133562.zip` | `taskstats.handbrake-transcode.tsv` | NORMAL, nice 0: `HandBrakeCLI` ×23 |
| `cpu-batch` (the 9.6 programs) | `meas-ci-build-2026-09-18`, `meas-build-r17.zip` | `taskstats.{clamscan,ffmpeg,handbrake,train,tracker}.tsv` | NORMAL, nice 0, except Tracker: IDLE, nice 19 (9.6 D17) |

`.NET …` threads are the runner agent's; `journal-offline` (nice 255 as printed) is journald's.

Not readable from the records: `office-writer`, `code-editor`, `mail-client`, `web-browser`, `image-editor`, `video-editor`, `video-player`, `audio-player`, `video-call` (9.5), `renderer-hidden`, `chat-client`, `game-client` (9.8), `compositor-shell`, `audio-server`, `service-manager`, `message-bus` (9.9). `game-task-chain` (9.4) is no measurement.

## Part two — the class census (2026-10-07)

The entries above not readable from their records, observed again in their campaigns' venues: one dry job per subject (`campaign/run.sh`, `desktop/run.sh`, `session/run.sh` in mode `dry`, the machine gate open on any model, `.github/campaign*.json` at `7cd13b4f`), each running `dataset/tools/meas/sched/classes.py` (`025b50af`) through the whole job — every thread's policy, real-time priority and nice from `/proc/<pid>/task/<tid>/stat`, read every 2 s and logged when a thread is first seen and on each change. A thread living under 2 s can be missed. A declared class is configuration, not timing, so one job per subject and no machine gate. The venues are headless runners: a program that asks RTKit or a desktop session for a real-time thread gets what the venue grants, which is stated per entry where it matters.

| entry | subject, run | machine | observed |
|---|---|---|---|
| `office-writer` | `soffice`, 37605116943 | EPYC 7763 | NORMAL, nice 0: every `soffice.bin` and `oosplash` thread |
| `code-editor` | `code`, 37605116943 | EPYC 7763 | NORMAL, nice 0: all 242 `code` threads |
| `mail-client` | `thunderbird-send`, 37605116943 | EPYC 7763 | NORMAL, nice 0: every `thunderbird-bin`, `RDD Process` and `crashhelper` thread |
| `web-browser` | `chrome`, 37605116943 | EPYC 9V74 | NORMAL, nice 0: all 169 `chrome` threads |
| `image-editor` | `gimp`, 37605116943 | EPYC 7763 | NORMAL, nice 0: `gimp`, `script-fu`, `python3` |
| `video-editor` | `kdenlive`, 37605116943 | EPYC 7763 | NORMAL, nice 0: 33 `kdenlive` threads and 72 `kdenlive_render`; NORMAL, nice 19: SDL's `SDLHotplugALSA`; BATCH, nice 19: `kdenliv:disk$0` |
| `video-player` | `mpv-video`, 37605116900 | EPYC 7763 | NORMAL, nice 0: every `mpv` thread |
| `audio-player` | `mpv-audio`, 37605116900 | EPYC 7763 | NORMAL, nice 0: every `mpv` thread but `mpv:disk$0`, BATCH, nice 19 |
| `video-call` | `webrtc`, 37605116900 | EPYC 7763 | NORMAL, nice 0: all 198 `chrome` threads, the audio worker included (no RTKit in the venue) |
| `renderer-hidden` | `chrome-hidden`, 37605116858 | EPYC 7763 | NORMAL, nice 0: all 160 `chrome` threads |
| (the visible renderer, 9.8) | `chrome-visible`, 37605116858 | EPYC 9V74 | NORMAL, nice 0: all 149 `chrome` threads |
| `chat-client` | `element`, 37605116858 | EPYC 7763 | NORMAL, nice 0: all 88 `element-desktop` threads |
| `game-client` | `steam`, 37605116858 | EPYC 9V45 | NORMAL, nice 0: `steam`, `steamwebhelper`, the runtime's `pressure-vessel`, `srt-*`; BATCH, nice 19: `steam:disk$0`, `steamwe:disk$0` |

| `compositor-shell` | `session` 96, 37605116929 | Xeon 8370C | NORMAL, nice 0: every carried `gnome-shell` thread — main, `JS Helper`, `gmain` — and the rest; RR, real-time priority 20: mutter's `KMS thread`; BATCH, nice 19: `gnome-s:disk$0`, `gnome-s:disk$1` |
| `audio-server` | `session` 96, 37605116929 | Xeon 8370C | `pipewire`, `pipewire-pulse`, `wireplumber`: RR, real-time priority 20, each `pw-data-loop` thread; NORMAL, nice −11, each main thread; NORMAL, nice 0, the rest — `wireplumber`'s carried `gmain` among them. `rtkit-daemon` ran in the session (its own thread RR 99) |
| `service-manager` | `session` 96, 37605116929 | Xeon 8370C | NORMAL, nice 0: `systemd` |
| `message-bus` | `session` 96, 37605116929 | Xeon 8370C | NORMAL, nice 0: every `dbus-daemon` |
No thread of any subject changed its policy, real-time priority or nice during its job.

Raw records: release `meas-ci-probes-2026-10-07b` at `07af2d92`, the fourteen jobs' final artifacts as `<artifact>-<run id>.zip`.

`…:disk$0` is Mesa's shader disk-cache queue (`src/util/disk_cache.c:89`, `util_queue_init(&cache->cache_queue, "disk$", …, UTIL_QUEUE_INIT_USE_MINIMUM_PRIORITY …)`), whose threads set nice 19 and `SCHED_BATCH` on themselves (`src/util/u_queue.c:270–272`, `:348–359`, read at tag `mesa-24.0.0`): a library thread in any program that uses OpenGL, the same `deja-du:disk$0` in Déjà Dup's census above, there inheriting the idle class.


The session's real-time threads are present but none is carried: 9.9's entries carry `gnome-shell`'s main thread, `JS Helper` and `gmain`, `wireplumber`'s `gmain`, pid 1 and the system bus (`dataset/archetypes.yaml`), all NORMAL at nice 0; in the idle session neither the KMS thread nor a data loop is among the carried components. The playback venue has no audio server (`--ao=null`, 9.5 D11), so no carried audio work passes through one.

## By class, the work the dataset carries

- **`SCHED_IDLE`:** `file-indexer` — every Tracker thread (nice 19, which the idle policy ignores); `incremental-backup` — `deja-dup`, `duplicity` and `gpg`.
- **NORMAL at a nice other than 0:** `game-download` — SteamCMD's content-update threads (`CContentUpdateC`, nearly all the nice-10 CPU) and async threads (`CGenericAsyncFi`, `COfflineMessage`) at nice 10, its HTTP and main threads at nice 0, inside one program's tables; `package-upgrade` — `apt-check` and `dpkg` at nice 19, 2.67 % of its pooled CPU, inside the tables that pool every process of the upgrade (D20); `module-build-orchestrator` — `apt-check` and `dpkg` at nice 19, 0.85 % of landing 10's CPU, whether its tables hold them not settled (D20).
- **Real-time:** none carried.
- **`SCHED_BATCH`:** none carried; Mesa's disk-cache threads only, in any program using OpenGL.
- **NORMAL at nice 0:** every other measured entry, whole.