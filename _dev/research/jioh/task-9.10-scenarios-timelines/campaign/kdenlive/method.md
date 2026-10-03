# Task 9.10 — the Kdenlive export campaign: method (2026-10-03)

The observation behind the render of `c1-render`, `c7-render` and `c2-p3a`'s segment 2 (changelog D10, D101–D104), run on GitHub-hosted runners under `../../../measurement-campaign-workflow.md`, pinned to one CPU. Amended only by a dated entry in §8. Tooling: `dataset/tools/meas/background/` — the `kdenlive` job of `run.sh`, which reuses the upgrade job's state build (`upgrade-layer.txt`), `analyze.py` and `pool.py`, with 9.5's Kdenlive setup from `dataset/tools/meas/probe/` — workflow `.github/workflows/meas-background.yml`, trigger `.github/campaign-background.json`, loop family `background`, app `kdenlive`.

## 1. Runs

- **Machine.** The AMD EPYC 7763 only; `machine_gate.sh` stops a job that drew another model before any install or measurement, and a gated job is not a repeat.
- **Tag.** `meas-ci:background:<YYYY-MM-DD>`, the launch date of the first batch, lettered if the workflow already has a campaign of that date (D76); each repeat's run id in the pooled record.
- **Repeat.** One job per repeat index: the state built, the project written, Kdenlive launched and the warm start run, the export measured (§3). Identical work — one project, one profile — so an added repeat is the next index. Artifact `meas-background-kdenlive-r<k>-<mode>`.
- **Modes.** `dry` — the tooling checked on one job, its `perf.data` kept; `full` — the campaign.
- **The list** (the workflow's stability rule, every value the fold-in carries): fixed with the entry's form after the dry run, by a dated entry in §8.
- **Tolerance.** The workflow's 5 % of the mean, and 1 µs for time tables where larger.
- **First batch.** Repeats 1–5: the rule's minimum (`kalibera-ismm13` §11). Then one repeat at a time, or a batch up to the pool's projection (9.7 D26), the rule read after each landing.
- **Validity** (the workflow's step 4, with this job's own checks): the gate open on the EPYC 7763; every recorded return code zero (perf record's 130 is its SIGINT stop); the layer built with no package missing; `/run/systemd/system` absent in the chroot; `kdenlive` 4:23.08.5-0ubuntu4, `melt` and `libmlt7` 7.22.0-1build6, `libavcodec60` 7:6.1.1-3ubuntu5, `libx264-164` 2:0.164.3108+git31e19f9-1 and `frei0r-plugins` installed; the clip's SHA-256 one across the pooled repeats; the clip at least 0.99 cached at the start (D104); the kernel's transparent huge pages `[always] madvise never` before the phase (D104); one `kdenlive_render` started by the dialog, which ran the `melt` its arguments name, and exited zero; the playlist's consumer carrying D103's settings; the output an MP4 of 600 H.264 frames at 1920 × 1080, with an AAC track; x264's options string one across the pooled repeats.
- **Recorded per job.** As the upgrade campaign's (`../upgrade/method.md` §1), and: the packages the install added and its log; the user's creation and XDG folders; the clip's generation log, size and SHA-256; the project; Kdenlive's log, its window, the dialog's screenshots; Kdenlive's own settings after the export (`kdenliverc`); the cached fractions of the clip and of `melt-7`, MLT's modules and the codec libraries; the kernel's transparent-hugepage settings and counters before and after the phase; `kdenlive_render`'s arguments and the playlist it rendered; the render's own log (`<output>.log`); the output's size, SHA-256, `ffprobe` streams and x264's options string.

## 2. Inputs (D102–D104)

- **The state.** The upgrade campaign's chroot (`../upgrade/method.md` §2: the 1,445 packages of `upgrade-layer.txt`, `mmdebstrap --variant=apt`, components `main restricted universe multiverse`, `LANG=en_US.UTF-8`) built from Ubuntu's snapshot service at T0 = `20260922T170000Z` (D64); then, on the harness CPUs, the stock sources at T0 and `apt-get install kdenlive ffmpeg` with apt's defaults, recommends included (D102): Kdenlive 23.08.5 with MLT 7.22.0, FFmpeg 6.1.1 and x264 0.164.3108 (S2-60).
- **The user.** A non-root user with a home under `/home`, its XDG folders made by the layer's `xdg-user-dirs-update`, as the Tracker campaign's.
- **9.5's settings** (`dataset/tools/meas/probe/appdefs.sh`, the `kdenlive` case). The per-user UI file `~/.local/share/kxmlgui5/kdenlive/kdenliveui.rc` (the zone shortcuts, version 1) and `~/.config/kdenliverc` with `[timeline] autopreview=false`.
- **The project** (D104). The clip by the chroot's `ffmpeg`: `-f lavfi -i testsrc=size=1920x1080:rate=30 -t 20 -an -c:v libx264 -preset veryfast -pix_fmt yuv420p`, as `~/Videos/clip.mp4` (design); the project by `kdenlive_project.py ~/Videos/clip.mp4 600 30 ~/Videos/project.kdenlive`: one video track with the clip and MLT's `avfilter.unsharp` at PCMark 10's parameters, one empty audio track.
- **The profile** (D103). Kdenlive 23.08.5's default, MP4-H264/AAC as the dialog opens: `f=mp4 movflags=+faststart vcodec=libx264 crf=23 g=15 preset=veryfast acodec=aac ab=160k real_time=-1 threads=0`, the full project (S2-59).
- **The display.** Xvfb `:99`, 1280×800×24 (9.5's), on the harness CPUs; its socket bound into the chroot's `/tmp/.X11-unix`.
- **The chroot's mounts.** As the upgrade campaign's: `/run/systemd/system` absent, `ischroot` holds; with the X socket.

## 3. Phases

In this order within each job:

| Step | Command | CPUs | Instruments |
|---|---|---|---|
| build | `mmdebstrap` (§2) | harness | none |
| install | `apt-get install kdenlive ffmpeg` at T0 (§2) | harness | none |
| state | the user, its folders, 9.5's settings, the clip and the project (§2) | harness | none |
| launch | `dbus-run-session -- kdenlive ~/Videos/project.kdenlive` as the user in the chroot, `QT_QPA_PLATFORM=xcb KDE_FULL_SESSION=true DISPLAY=:99`, `taskset` placing it on the measured CPU; the window found, then 30 s to settle | measured | none |
| warm start | the clip read whole (D104) | harness | none |
| cache check | `fincore` over the clip and over `melt-7`, MLT's modules and the codec libraries | harness | none |
| `kdenlive-export` | the driver on the harness CPUs: Kdenlive's window raised, Ctrl+Return, the "Rendering" dialog found and screenshotted, "Render to File" clicked; it waits for `kdenlive_render` to start, copies the playlist its arguments name, and waits for it to exit. The phase ends at that exit; no cap of its own (the workflow's 330-minute job limit) | harness (the driver); measured (Kdenlive and the export) | §4 |
| after | the output read; Kdenlive closed | harness | none |

The kernel's transparent-hugepage settings (`enabled`, `defrag`, `khugepaged/defrag`, `khugepaged/scan_sleep_millisecs`, `khugepaged/alloc_sleep_millisecs`, `khugepaged/pages_to_scan`) and `/proc/vmstat`'s `thp_collapse_alloc`, `thp_collapse_alloc_failed`, `thp_fault_alloc` and `thp_fault_fallback` are recorded before and after the phase.

## 4. Instruments

As the upgrade campaign's (`../upgrade/method.md` §4).

## 5. Analysis rules

- **The job (D101).** Every process of the tree rooted at the first process that executed `/usr/bin/kdenlive_render` in the phase, from its first schedule-in on the measured CPU to its exit. The CPU total is perf's, the sum of the tree's runs on the measured CPU; taskstats' per-thread rows are reported beside it (the HandBrakeCLI campaign's §5).
- **Outside the job.** Kdenlive, its session bus and anything else on the measured CPU, reported by `comm` beside the job.
- **Form.** Fixed after the dry run by a dated entry in §8, by 9.6 D7's criterion: a program is `cpu-batch` when it is runnable for the whole of its lifetime on one dominant thread; sustained I/O waits or several equal threads give it its own entry.
- **Wake.** As the upgrade campaign's §5.
- **Also reported.** The job's process and thread counts and CPU by process and thread; the job's span; the job's block-I/O delay and its `sched_stat_iowait` rows; the time from the click to `kdenlive_render`'s first schedule-in.

## 6. Scope, written into the entry

Runner spec (4 vCPU Azure VM, `ubuntu-24.04`, kernel and CPU model as recorded, the AMD EPYC 7763); one CPU, the rest of the machine idealised; Kdenlive and the runner's agent processes share the measured CPU and are outside the tree; no desktop session beyond Xvfb and a session bus, no display refresh, no GPU, no sound device; the kernel's transparent huge pages in the runner's `always` mode. Kdenlive 23.08.5 as Ubuntu 24.04 packages it exporting the `video-editor` project — 9.5's 20 s 1920×1080 30 fps H.264 clip (synthetic content, design) with an unsharp effect at PCMark 10's Video Editing parameters — through its render dialog with its shipped default profile, MP4-H264/AAC (x264 `veryfast`, CRF 23) (D10, D101, D103), in D37's chroot built at 2026-09-22T17:00Z, Kdenlive open on the project (D102, D104).

## 7. Release

Raw records per job are released as a GitHub release named in the registry entry at fold-in. The release is outward-facing and is published on 인지오's go-ahead.

## 8. Amendments
