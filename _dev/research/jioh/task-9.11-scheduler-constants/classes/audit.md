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
| `game-download` | `meas-ci-background-2026-09-19`, `meas-background-steamcmd-r32-full.zip` | `taskstats.steam-fresh-shaped.tsv` | NORMAL, nice 10: `CGenericAsyncFi` ×55, `COfflineMessage` ×2, `CContentUpdateC` ×2; NORMAL, nice 0: `CHTTPClientThre`, `steamcmd` and the rest, 37 tasks |
| `cpu-batch` (`python`) | `meas-ci-background-2026-10-03`, `…-mnist-r1-full-37091275421.zip` | `taskstats.mnist-train.tsv` | NORMAL, nice 0 |
| `cpu-batch` (`kdenlive_render`) | `meas-ci-background-2026-10-03c`, `…-kdenlive-r16-full-37126535233.zip` | `taskstats.kdenlive-export.tsv` | NORMAL, nice 0: `melt-7`, `kdenlive_render` |
| `video-transcoder` | `meas-ci-background-2026-10-03b`, `…-handbrake-r3-full-37109133562.zip` | `taskstats.handbrake-transcode.tsv` | NORMAL, nice 0: `HandBrakeCLI` ×23 |
| `cpu-batch` (the 9.6 programs) | `meas-ci-build-2026-09-18`, `meas-build-r17.zip` | `taskstats.{clamscan,ffmpeg,handbrake,train,tracker}.tsv` | NORMAL, nice 0, except Tracker: IDLE, nice 19 (9.6 D17) |

`.NET …` threads are the runner agent's; `journal-offline` (nice 255 as printed) is journald's.

Not readable from the records: `office-writer`, `code-editor`, `mail-client`, `web-browser`, `image-editor`, `video-editor`, `video-player`, `audio-player`, `video-call` (9.5), `renderer-hidden`, `chat-client`, `game-client` (9.8), `compositor-shell`, `audio-server`, `service-manager`, `message-bus` (9.9). `game-task-chain` (9.4) is no measurement.
