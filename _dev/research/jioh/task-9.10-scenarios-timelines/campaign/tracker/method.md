# Task 9.10 — the Tracker campaign: method (2026-10-02)

The observation behind the three indexing files, `c1-indexing`, `c7-indexing` and `c2-p1b` (changelog D5, D6, D60–D68), run on GitHub-hosted runners under `../../../measurement-campaign-workflow.md`, pinned to one CPU. Amended only by a dated entry in §8. Tooling: `dataset/tools/meas/background/` — the `tracker` job of `run.sh`, which reuses the `upgrade` job's state build (`upgrade-layer.txt`), `analyze.py` and `pool.py` — workflow `.github/workflows/meas-background.yml`, trigger `.github/campaign-background.json`, loop family `background`, app `tracker`.

## 1. Runs

- **Machine.** The AMD EPYC 7763 only; `machine_gate.sh` stops a job that drew another model before any install or measurement, and a gated job is not a repeat.
- **Tag.** `meas-ci:background:<YYYY-MM-DD>`, the launch date of the first batch; each repeat's run id in the pooled record.
- **Repeat.** One job per repeat index: the state built, the home and the file set prepared, the index measured (§3). Identical work, so an added repeat is the next index. Artifact `meas-background-tracker-r<k>-<mode>`.
- **Modes.** `dry` — the tooling checked on one job, its `perf.data` kept; `full` — the campaign.
- **The list** (the workflow's stability rule, every value the fold-in carries): over the job (§5), the run between voluntary blocks and the block per run, each tested by its mean as the table carries it (the ratio estimator), and the CPU total, tested by its per-repeat values (D17). Fixed with the entry's form after the dry run, by a dated entry in §8.
- **Tolerance.** The workflow's 5 % of the mean, and 1 µs for time tables where larger.
- **First batch.** Repeats 1–5: the rule's minimum (`kalibera-ismm13` §11). Then one repeat at a time, or a batch up to the pool's projection (9.7 D26), the rule read after each landing.
- **Validity** (the workflow's step 4, with this job's own checks): the gate open on the EPYC 7763; every recorded return code zero (perf record's 130 is its SIGINT stop); the layer built with no package missing or extra; `tracker-miner-fs` and `tracker-extract` at 3.7.1-1ubuntu0.1; the file set downloaded whole — 875 files, 40,662,407,070 B, each file's size as the revision lists it; no GStreamer registry in the home before the phase; the miner's status `Initializing` 15 s after its first `Idle` (the initial sleep); the extractor's status `Idle` after `Extracting metadata`; the job's end before the phase's cap; `/run/systemd/system` absent in the chroot.
- **Recorded per job.** As the upgrade campaign's (`../upgrade/method.md` §1), and: the miner's and the extractor's logs, the miner's settings as read in the chroot (`gsettings list-recursively`), `tracker3 status` after the phase, the files and folders the database holds under `~/Documents`, the extraction failures the extractor logged, the GStreamer registry after the phase, the dataset revision and the downloaded tree's listing.

## 2. Inputs (D61, D64, D66–D68)

- **The state.** The upgrade campaign's chroot (`../upgrade/method.md` §2: the 1,445 packages of `upgrade-layer.txt`, `mmdebstrap --variant=apt`, components `main restricted universe multiverse`, `LANG=en_US.UTF-8`) built from Ubuntu's snapshot service at T0 = `20260922T170000Z` (D64, the DKMS campaign's T0). Nothing is installed for the measurement: the layer holds Tracker 3.7.1 and its extraction stack (D61, S2-41).
- **The user.** A non-root user with a home under `/home`, its folders created by the layer's `xdg-user-dirs-update` run as that user: Desktop, Documents, Downloads, Music, Pictures, Public, Templates, Videos, and `~/.config/user-dirs.dirs` (D68).
- **The file set.** HippoCamp (`MMMem-org/HippoCamp`, Hugging Face) at revision `ff212ff7ec1a60d28023e65f7e7c4df5a87f552c`, the tree `Bei/Fullset/Bei/` — 875 files, 40,662,407,070 B, 83 directories, 76 of them holding files (D67, S3-76), every file a Git LFS object checked by its SHA-256 — downloaded on the harness CPUs and placed as the content of `~/Documents`, owned by the user (D68). The other folders are empty.
- **The settings.** As shipped (D61, D63): nothing written to the miner's or the extractor's settings, `initial-sleep` 15.
- **The session.** A session bus for the user from `dbus-run-session` in the chroot; the miner started as its user unit's `ExecStart`, `/usr/libexec/tracker-miner-fs-3` (S2-41), with the environment reduced to the user's `HOME`, `USER`, `PATH`, `LANG`, the session bus's address and `TRACKER_DEBUG=status`, the status trace the job's boundaries are read from (§5, D69). No systemd user session and no GNOME session.
- **The chroot's mounts.** As the upgrade campaign's: `/run/systemd/system` absent, `ischroot` holds.

## 3. Phases

In this order within each job:

| Step | Command | CPUs | Instruments |
|---|---|---|---|
| build | `mmdebstrap` (§2) | harness | none |
| home | the user, `xdg-user-dirs-update`, the file set downloaded and placed (§2) | harness | none |
| `tracker-index` | `dbus-run-session` as the user in the chroot, on the harness CPUs; within it the miner, `taskset` placing it and so its tree on the measured CPU. The phase ends when the extractor has exited after its job, or at a cap of 3,600 s; the miner is then stopped with SIGTERM | measured | §4 |

## 4. Instruments

As the upgrade campaign's (`../upgrade/method.md` §4).

## 5. Analysis rules

- **The job (D62, D63, D65).** Every process rooted at the miner — the miner, the extractor it starts, and their descendants by the fork rows — from the miner's first schedule-in to the extractor's last status change to `Idle` after `Extracting metadata` (D62's "Extraction finished", D69), the log's time converted to the perf clock with `edges.jsonl` (9.6 D16). The session bus is outside.
- **Form.** Fixed after the dry run by a dated entry in §8, with the form questions: the entry's form (a new entry, or `cpu-batch`'s `tracker` program re-measured, D5), how the initial sleep appears (D63), and the GStreamer registry scan's weight between the two labels (D65).
- **Wake.** As the upgrade campaign's §5.
- **Also reported.** The job's process count and CPU by executed program; the initial sleep's span; the miner's `Idle` inside the job (9.6 D16's end); the registry scan's CPU; the files and folders indexed; the extraction failures; the phase's tail after the job.

## 6. Scope, written into the entry

Runner spec (4 vCPU Azure VM, `ubuntu-24.04`, kernel and CPU model as recorded, the AMD EPYC 7763); one CPU, the rest of the machine idealised; the runner's agent processes share the measured CPU and are outside the tree; no desktop session — the miner started as its user unit's command under a session bus of its own. Tracker 3.7.1's first index of a home from an empty database, its settings as shipped (D61, D63), in the upgrade campaign's chroot built at 2026-09-22T17:00Z (D64). The file set is HippoCamp's Bei profile, a home-like file system aggregated by HippoCamp's authors from participants' files and synthetic content, not one person's set (D66, D67); placed whole as `~/Documents`, design (D68). The home holds no GStreamer registry at the start (D65).

## 7. Release

Raw records per job are released as a GitHub release named in the registry entry at fold-in. HippoCamp's licence forbids publicly mirroring its raw files (S3-76): the release carries no file of the set. Whether the logs that name the set's paths are released is decided with the release. The release is outward-facing and is published on 인지오's go-ahead.

## 8. Amendments

- 2026-10-02, dry run 1 (run 37001819621, #118) — tooling only: the set's fetch into the home was refused (the home is mode 750), so the index ran on an empty `~/Documents`; the set is fetched into the work directory and renamed into place. The session otherwise ran as §3 states.
- 2026-10-02, dry run 2 (run 37002910488, #119; changelog D69) — amending §2 "The session" and §5 "The job": the debug variables are `TRACKER_DEBUG=status` alone, and the job's end is the extractor's last status change to `Idle` after `Extracting metadata` (D62's "Extraction finished", logged in the same millisecond). Recorded from the run: the set whole (875 files, 40,662,407,070 B, fetched in 233 s); "Currently indexed: 875 files, 92 folders"; the job 58.3 s, 39.6 s of CPU — the extractor 38.0 s, the miner 1.5 s, the registry scan 94 ms; the crawl under 0.4 s; the extractor's stock 5 s per-file deadline (`tracker-extract.c:46`) ended two runs on two PDFs, each restarted by the miner after its 1 s grace (`tracker-miner-files.c:244–245`); ten recorded failures; no system bus in the chroot, so the miner reaches neither UPower nor UDisks2, and the extractor's sandbox cannot read `/proc/self/mountinfo`.
