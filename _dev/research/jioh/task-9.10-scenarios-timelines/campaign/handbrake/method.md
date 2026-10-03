# Task 9.10 — the HandBrakeCLI transcode campaign: method (2026-10-03)

The observation behind the transcode of `c1-transcode`, `c7-transcode` and `c3-creation`'s last segment (changelog D11, D91–D95), run on GitHub-hosted runners under `../../../measurement-campaign-workflow.md`, pinned to one CPU. Amended only by a dated entry in §8. Tooling: `dataset/tools/meas/background/` — the `handbrake` job of `run.sh`, which reuses the upgrade job's state build (`upgrade-layer.txt`), `analyze.py` and `pool.py` — workflow `.github/workflows/meas-background.yml`, trigger `.github/campaign-background.json`, loop family `background`, app `handbrake`.

## 1. Runs

- **Machine.** The AMD EPYC 7763 only; `machine_gate.sh` stops a job that drew another model before any install or measurement, and a gated job is not a repeat.
- **Tag.** `meas-ci:background:<YYYY-MM-DD>`, the launch date of the first batch, lettered if the workflow already has a campaign of that date (D76); each repeat's run id in the pooled record.
- **Repeat.** One job per repeat index: the state built, the clip placed, the warm start run, the encode measured (§3). Identical work — one clip, one preset — so an added repeat is the next index. Artifact `meas-background-handbrake-r<k>-<mode>`.
- **Modes.** `probe` — two 30 s cuts of the clip at four of HandBrake's H.265 presets, never a repeat (D93); `dry` — the tooling checked on one job, its `perf.data` kept; `full` — the campaign.
- **The list** (the workflow's stability rule, every value the fold-in carries): over the job (§5), the run between voluntary blocks and the block per run, each tested by its mean as the table carries it (the ratio estimator), and the CPU total, tested by its per-repeat values (D17). Fixed with the entry's form after the dry run, by a dated entry in §8.
- **Tolerance.** The workflow's 5 % of the mean, and 1 µs for time tables where larger.
- **First batch.** Repeats 1–5: the rule's minimum (`kalibera-ismm13` §11). Then one repeat at a time, or a batch up to the pool's projection (9.7 D26), the rule read after each landing.
- **Validity** (the workflow's step 4, with this job's own checks): the gate open on the EPYC 7763; every recorded return code zero (perf record's 130 is its SIGINT stop); the layer built with no package missing, the packages added being `handbrake-cli`'s 67 (the probe, run #151); `/run/systemd/system` absent in the chroot; `handbrake-cli` 1.7.2+ds1-1build2 and `libx264-164` 2:0.164.3108+git31e19f9-1; the zip and the clip each matching its SHA-256; the clip at least 0.99 cached at the start (D94); the kernel's transparent huge pages `[always] madvise never` before the phase (D94); the encode done by `libx264` at the preset's "fast" and RF 22, its picture stored 1920 × 1080 at a pixel aspect of 1 : 1; the video track the muxer wrote — its frames and bytes — one across the pooled repeats.
- **Recorded per job.** As the upgrade campaign's (`../upgrade/method.md` §1), and: the user's creation and XDG folders; HandBrakeCLI's version, help and preset list; the versions of `handbrake-cli`, `libx264-164`, `libx265-199` and `libavcodec60`; the zip's and the clip's SHA-256 and size; the scan's output and duration; the cached fractions of the clip and of HandBrakeCLI and its codec libraries; the kernel's transparent-hugepage settings and counters before and after the phase; the encode's own log (its progress lines dropped), its output geometry, the encoder's setup, the decoder's and the muxer's frame counts; the output's size and SHA-256.

## 2. Inputs (D91–D95)

- **The state.** The upgrade campaign's chroot (`../upgrade/method.md` §2: the 1,445 packages of `upgrade-layer.txt`, `mmdebstrap --variant=apt`, components `main restricted universe multiverse`, `LANG=en_US.UTF-8`) built from Ubuntu's snapshot service at T0 = `20260922T170000Z` (D64), with `handbrake-cli` in the same build: HandBrakeCLI 1.7.2 with x264 0.164.3108 and FFmpeg 6.1.1 (S2-56; D94, D95).
- **The user.** A non-root user with a home under `/home`, its XDG folders made by the layer's `xdg-user-dirs-update`, as the Tracker campaign's.
- **The clip.** `bbb_sunflower_2160p_30fps_normal.mp4` from `https://download.blender.org/demo/movies/BBB/bbb_sunflower_2160p_30fps_normal.mp4.zip`, fetched and unzipped on the harness CPUs; the zip's SHA-256 `750b255c…ae151` and the clip's `37f0ff25…55520` checked; placed as `~/Videos/bbb_sunflower_2160p_30fps_normal.mp4`, owned by the user (S2-53; D91). H.264 High, 3840×2160, 30 fps, 19,036 frames, 634.5 s, MP3 and AC-3 audio, in MP4.
- **The settings.** HandBrake 1.7.2's default preset unchanged: `--preset "Fast 1080p30"` — x264 "fast" at RF 22, profile main, level 4.0, 1920×1080 at most (D92), a peak frame rate of 30, the first audio track as AAC stereo at 160 kb/s, in MP4 (S2-55). H.264 is the codec of CpsMark+'s own code (S2-58; D95).
- **The chroot's mounts.** As the upgrade campaign's: `/run/systemd/system` absent, `ischroot` holds.

## 3. Phases

In this order within each job:

| Step | Command | CPUs | Instruments |
|---|---|---|---|
| build | `mmdebstrap` (§2) | harness | none |
| state | the user, its folders, the clip fetched, checked and placed (§2) | harness | none |
| warm start | the clip read whole; `HandBrakeCLI -i bbb_sunflower_2160p_30fps_normal.mp4 --scan` as the user in `~/Videos` (D94) | harness | none |
| cache check | `fincore` over the clip and over HandBrakeCLI and its codec libraries | harness | none |
| `handbrake-transcode` | `HandBrakeCLI -i bbb_sunflower_2160p_30fps_normal.mp4 -o bbb_sunflower_2160p_30fps_normal.out.mp4 --preset "Fast 1080p30"` as the user in the chroot, in `~/Videos`, `taskset` placing it on the measured CPU. The phase ends when the command exits; no cap of its own (the workflow's 330-minute job limit) | measured | §4 |

The kernel's transparent-hugepage settings (`enabled`, `defrag`, `khugepaged/defrag`, `khugepaged/scan_sleep_millisecs`, `khugepaged/alloc_sleep_millisecs`, `khugepaged/pages_to_scan`) and `/proc/vmstat`'s `thp_collapse_alloc`, `thp_collapse_alloc_failed`, `thp_fault_alloc` and `thp_fault_fallback` are recorded before and after the phase.

## 4. Instruments

As the upgrade campaign's (`../upgrade/method.md` §4).

## 5. Analysis rules

- **The job (D94).** Every process of the tree rooted at the process `taskset` executed into `chroot` (`launched_root`), from its first schedule-in on the measured CPU to its exit; the whole phase. The CPU total is perf's, the sum of the program's runs on the measured CPU: for a multi-threaded process taskstats' thread-group row overstates it on this kernel (the probe, D93), and the per-thread rows are reported beside it.
- **Form.** Fixed after the dry run by a dated entry in §8: `cpu-batch`'s `HandBrakeCLI` program re-measured, or an entry of its own, by 9.6 D7's criterion — a program is `cpu-batch` when it is runnable for the whole of its lifetime on one dominant thread; sustained I/O waits or several equal threads give it its own entry.
- **Wake.** As the upgrade campaign's §5.
- **Also reported.** The job's process and thread counts and CPU by thread; the job's span; the job's block-I/O delay and its `sched_stat_iowait` rows.

## 6. Scope, written into the entry

Runner spec (4 vCPU Azure VM, `ubuntu-24.04`, kernel and CPU model as recorded, the AMD EPYC 7763); one CPU, the rest of the machine idealised; the runner's agent processes share the measured CPU and are outside the tree; no desktop session; the kernel's transparent huge pages in the runner's `always` mode. HandBrakeCLI 1.7.2 as Ubuntu 24.04 packages it, its default preset unchanged, encoding Big Buck Bunny's 4K H.264 edition whole to 1920×1080 H.264 in MP4 — CpsMark+'s HandBrake workload, its codec and 1080p "2K" from the benchmark's own code, its clip and preset settings not (D11, D91, D92, D95) — in D37's chroot built at 2026-09-22T17:00Z, from a warm start with the clip local (D94). No hardware encoder.

## 7. Release

Raw records per job are released as a GitHub release named in the registry entry at fold-in. The release is outward-facing and is published on 인지오's go-ahead.

## 8. Amendments

- 2026-10-03, the probe (run #151, two jobs on the EPYC 7763; run #150 stopped at the gate; changelog D93), never a repeat — 30 s of the clip from its start and from 300 s at four of HandBrake's H.265 presets, the 4K ones held to `--maxWidth 2048 --maxHeight 1080`: 2.41–5.83 s of CPU per source second, the whole clip 1,530–3,700 s; x265's pool 4 threads under the pin (S2-57). Amending §1 "Modes" with `probe`.
- 2026-10-03, D95 — amending §2 "The settings" and §3: HandBrake's default preset unchanged, x264, H.264 the codec of CpsMark+'s own code (S2-58); the output `bbb_sunflower_2160p_30fps_normal.out.mp4`. The dry run of D93's settings (run #152) is superseded and not pooled.
- 2026-10-03, dry run (run 37105339193, #153; changelog D97) — amending §1 "The list" and "Validity", and §5 "Form". Recorded from the run: the layer plus `handbrake-cli`'s 67 packages; the clip and the libraries cached at 1.0000; the encoder `libx264` at fast, RF 22, Main 4.0, the picture 1920 × 1080 at 1 : 1; the decoder's 19,036 frames with no error, 19,038 frames muxed, the video track 276,311,652 B; the job one process of 23 threads, 2,974.0 s and 2,972.35 s of CPU, saturation 0.9994, the busiest thread 0.335 of the CPU; the block per run mean 0.602 µs; 3 uninterruptible waits, each ended by `khugepaged`. Form: a new entry in the batch-loop form, `cpu-batch`'s `HandBrakeCLI` tables leaving at fold-in, by 9.6 D7's criterion (D97). The list: over the job, the run between voluntary blocks and the block per run, each tested by its mean as the table carries it, and the CPU total, tested by its per-repeat values. Validity adds: the decoder's 19,036 frames with no decoder error.
- 2026-10-03, the campaign (runs #154–#156; `meas-ci:background:2026-10-03b`, lettered after the MNIST campaign's date, D76). Repeats 1–5, every one valid, each landing once; 4 jobs stopped at the gate (AMD EPYC 9V74). At five landings the rule holds on all three values: the run between voluntary blocks 4.002 ms ±1.8 %, the block per run 0.605 µs within the 1 µs floor, the CPU total 2,970.871 s ±2.6 % (2,863.5–3,023.8 s). The same video track, 19,038 frames and 276,311,652 B, in every landing.
