# Task 9.10 — the HandBrakeCLI transcode campaign: method (2026-10-03)

The observation behind the transcode of `c1-transcode`, `c7-transcode` and `c3-creation`'s last segment (changelog D11, D91–D94), run on GitHub-hosted runners under `../../../measurement-campaign-workflow.md`, pinned to one CPU. Amended only by a dated entry in §8. Tooling: `dataset/tools/meas/background/` — the `handbrake` job of `run.sh`, which reuses the upgrade job's state build (`upgrade-layer.txt`), `analyze.py` and `pool.py` — workflow `.github/workflows/meas-background.yml`, trigger `.github/campaign-background.json`, loop family `background`, app `handbrake`.

## 1. Runs

- **Machine.** The AMD EPYC 7763 only; `machine_gate.sh` stops a job that drew another model before any install or measurement, and a gated job is not a repeat.
- **Tag.** `meas-ci:background:<YYYY-MM-DD>`, the launch date of the first batch, lettered if the workflow already has a campaign of that date (D76); each repeat's run id in the pooled record.
- **Repeat.** One job per repeat index: the state built, the clip placed, the warm start run, the encode measured (§3). Identical work — one clip, one preset — so an added repeat is the next index. Artifact `meas-background-handbrake-r<k>-<mode>`.
- **Modes.** `probe` — two 30 s cuts of the clip at four of HandBrake's H.265 presets, never a repeat (D93); `dry` — the tooling checked on one job, its `perf.data` kept; `full` — the campaign.
- **The list** (the workflow's stability rule, every value the fold-in carries): over the job (§5), the run between voluntary blocks and the block per run, each tested by its mean as the table carries it (the ratio estimator), and the CPU total, tested by its per-repeat values (D17). Fixed with the entry's form after the dry run, by a dated entry in §8.
- **Tolerance.** The workflow's 5 % of the mean, and 1 µs for time tables where larger.
- **First batch.** Repeats 1–5: the rule's minimum (`kalibera-ismm13` §11). Then one repeat at a time, or a batch up to the pool's projection (9.7 D26), the rule read after each landing.
- **Validity** (the workflow's step 4, with this job's own checks): the gate open on the EPYC 7763; every recorded return code zero (perf record's 130 is its SIGINT stop); the layer built with no package missing, the packages added being `handbrake-cli`'s 67 (the probe, run #151); `/run/systemd/system` absent in the chroot; `handbrake-cli` 1.7.2+ds1-1build2 and `libx265-199` 3.5-2build1; the zip and the clip each matching its SHA-256; the clip at least 0.99 cached at the start (D94); the kernel's transparent huge pages `[always] madvise never` before the phase (D94); the encode done, its picture stored 1920 × 1080 at a pixel aspect of 1 : 1; x265's summary — the frames, the stream's bitrate and average QP — one across the pooled repeats.
- **Recorded per job.** As the upgrade campaign's (`../upgrade/method.md` §1), and: the user's creation and XDG folders; HandBrakeCLI's version, help and preset list; the versions of `handbrake-cli`, `libx265-199` and `libavcodec60`; the zip's and the clip's SHA-256 and size; the scan's output and duration; the cached fractions of the clip and of HandBrakeCLI and its codec libraries; the kernel's transparent-hugepage settings and counters before and after the phase; the encode's own log (its progress lines dropped), its output geometry, x265's settings, thread pool, frame threads and summary; the output's size and SHA-256.

## 2. Inputs (D91–D94)

- **The state.** The upgrade campaign's chroot (`../upgrade/method.md` §2: the 1,445 packages of `upgrade-layer.txt`, `mmdebstrap --variant=apt`, components `main restricted universe multiverse`, `LANG=en_US.UTF-8`) built from Ubuntu's snapshot service at T0 = `20260922T170000Z` (D64), with `handbrake-cli` in the same build: HandBrakeCLI 1.7.2 with x265 3.5 and FFmpeg 6.1.1 (S2-56; D94).
- **The user.** A non-root user with a home under `/home`, its XDG folders made by the layer's `xdg-user-dirs-update`, as the Tracker campaign's.
- **The clip.** `bbb_sunflower_2160p_30fps_normal.mp4` from `https://download.blender.org/demo/movies/BBB/bbb_sunflower_2160p_30fps_normal.mp4.zip`, fetched and unzipped on the harness CPUs; the zip's SHA-256 `750b255c…ae151` and the clip's `37f0ff25…55520` checked; placed as `~/Videos/bbb_sunflower_2160p_30fps_normal.mp4`, owned by the user (S2-53; D91). H.264 High, 3840×2160, 30 fps, 19,036 frames, 634.5 s, MP3 and AC-3 audio, in MP4.
- **The settings.** HandBrake 1.7.2's default preset with the video encoder set to `x265`: `--preset "Fast 1080p30" --encoder x265` — 1920×1080 (D92), 30 fps, x265 "fast" at RF 22, profile main, level 4.0, the first audio track as AAC stereo at 160 kb/s, in MP4 (S2-55; D93).
- **The chroot's mounts.** As the upgrade campaign's: `/run/systemd/system` absent, `ischroot` holds.

## 3. Phases

In this order within each job:

| Step | Command | CPUs | Instruments |
|---|---|---|---|
| build | `mmdebstrap` (§2) | harness | none |
| state | the user, its folders, the clip fetched, checked and placed (§2) | harness | none |
| warm start | the clip read whole; `HandBrakeCLI -i bbb_sunflower_2160p_30fps_normal.mp4 --scan` as the user in `~/Videos` (D94) | harness | none |
| cache check | `fincore` over the clip and over HandBrakeCLI and its codec libraries | harness | none |
| `handbrake-transcode` | `HandBrakeCLI -i bbb_sunflower_2160p_30fps_normal.mp4 -o bbb_sunflower_2160p_30fps_normal.h265.mp4 --preset "Fast 1080p30" --encoder x265` as the user in the chroot, in `~/Videos`, `taskset` placing it on the measured CPU. The phase ends when the command exits; no cap of its own (the workflow's 330-minute job limit) | measured | §4 |

The kernel's transparent-hugepage settings (`enabled`, `defrag`, `khugepaged/defrag`, `khugepaged/scan_sleep_millisecs`, `khugepaged/alloc_sleep_millisecs`, `khugepaged/pages_to_scan`) and `/proc/vmstat`'s `thp_collapse_alloc`, `thp_collapse_alloc_failed`, `thp_fault_alloc` and `thp_fault_fallback` are recorded before and after the phase.

## 4. Instruments

As the upgrade campaign's (`../upgrade/method.md` §4).

## 5. Analysis rules

- **The job (D94).** Every process of the tree rooted at the process `taskset` executed into `chroot` (`launched_root`), from its first schedule-in on the measured CPU to its exit; the whole phase. The CPU total is perf's, the sum of the program's runs on the measured CPU: for a multi-threaded process taskstats' thread-group row overstates it on this kernel (the probe, D93), and the per-thread rows are reported beside it.
- **Form.** Fixed after the dry run by a dated entry in §8: `cpu-batch`'s `HandBrakeCLI` program re-measured, or an entry of its own, by 9.6 D7's criterion — a program is `cpu-batch` when it is runnable for the whole of its lifetime on one dominant thread; sustained I/O waits or several equal threads give it its own entry.
- **Wake.** As the upgrade campaign's §5.
- **Also reported.** The job's process and thread counts and CPU by thread; the job's span; x265's pool and frame threads; the job's block-I/O delay and its `sched_stat_iowait` rows.

## 6. Scope, written into the entry

Runner spec (4 vCPU Azure VM, `ubuntu-24.04`, kernel and CPU model as recorded, the AMD EPYC 7763); one CPU, the rest of the machine idealised; the runner's agent processes share the measured CPU and are outside the tree; no desktop session; the kernel's transparent huge pages in the runner's `always` mode. HandBrakeCLI 1.7.2 as Ubuntu 24.04 packages it, its default preset with H.265 chosen, encoding Big Buck Bunny's 4K H.264 edition whole to 1920×1080 H.265 in MP4 — CpsMark+'s HandBrake workload (D11, D91–D93) — in D37's chroot built at 2026-09-22T17:00Z, from a warm start with the clip local (D94). x265 sizes its thread pool from the machine's CPUs, not the pin (S2-57). No hardware encoder.

## 7. Release

Raw records per job are released as a GitHub release named in the registry entry at fold-in. The release is outward-facing and is published on 인지오's go-ahead.

## 8. Amendments
