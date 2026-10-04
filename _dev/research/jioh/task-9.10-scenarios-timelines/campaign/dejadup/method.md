# Task 9.10 — the Déjà Dup backup campaign: method (2026-10-04)

The observation behind the scheduled backup of `c1-backup`, `c7-backup` and `c2-p3b`'s segment 1 (changelog D8, D9, D112–D118), run on GitHub-hosted runners under `../../../measurement-campaign-workflow.md`, pinned to one CPU. Amended only by a dated entry in §8. Tooling: `dataset/tools/meas/background/` — the `dejadup` job of `run.sh`, which reuses the upgrade job's state build (`upgrade-layer.txt`), 9.7's file-set tooling (`fileset.py`, `inputs.json`), `analyze.py` and `pool.py`; the first-backup driver `dejadup_first.py` and the session script `dejadup-session.sh` — workflow `.github/workflows/meas-background.yml`, trigger `.github/campaign-background.json`, loop family `background`, app `dejadup`.

## 1. Runs

- **Machine.** The AMD EPYC 7763 only; `machine_gate.sh` stops a job that drew another model before any install or measurement, and a gated job is not a repeat.
- **Tag.** `meas-ci:background:<YYYY-MM-DD>`, the launch date of the first batch, lettered if the workflow already has a campaign of that date (D76); each repeat's run id in the pooled record.
- **Repeat.** One job per repeat index: the state built, the set placed, the drive mounted, the first backup made, the week written and the change set applied, the warm start, the incremental measured (§3). Identical work — one set, one change set, one seed — so an added repeat is the next index. Artifact `meas-background-dejadup-r<k>-<mode>`.
- **Modes.** `dry` — the tooling checked on one job, its `perf.data` kept; `MEAS_DEJADUP_SET` names the set (`100mb`, Mahoney's published subset, for a check of the drivers; `10gb` for the campaign's own job); `full` — the campaign, always on `10gb`.
- **The list** (the workflow's stability rule, every value the fold-in carries): fixed with the entry's form after the dry run (§8).
- **Tolerance.** The workflow's 5 % of the mean, and 1 µs for time tables where larger.
- **First batch.** Repeats 1–5: the rule's minimum (`kalibera-ismm13` §11). Then one repeat at a time, or a batch up to the pool's projection (9.7 D26), the rule read after each landing.
- **Validity** (the workflow's step 4, with this job's own checks): the gate open on the EPYC 7763; every recorded return code zero (perf record's 130 is its SIGINT stop); the layer built with no package missing; `/run/systemd/system` absent in the chroot; `deja-dup` 45.2-1build2, `duplicity` 2.1.4-3ubuntu2 and `librsync2t64` 2.3.4-1.1ubuntu2 installed; the packages the install added one set across the pooled repeats; the set's archive and manifest matching their pins, and the tree verified before the first backup; the first backup finished, its chain one full backup on the drive, the password remembered; the change set's plan one SHA-256 across the pooled repeats; the set at least 0.99 cached at the start (D116); the kernel's transparent huge pages `[always] madvise never` before the phase (D118); one `deja-dup` started by the monitor in the phase, with the arguments `--backup --auto`, in the idle CPU class and the idle I/O class; `last-backup` advanced by it; the drive's chain one full backup and one incremental after it.
- **Recorded per job.** As the upgrade campaign's (`../upgrade/method.md` §1), and: the packages the install added and its log; the user's creation and XDG folders; the set's fetch, check, manifest and placement; the drive's image, loop device and mount; Déjà Dup's settings before the first backup, after it and after the phase (`gsettings list-recursively org.gnome.DejaDup`); the first backup's screenshots, duration and log; the change set's plan and its summary; the cached fractions of the set and of `~/.cache/deja-dup`; the kernel's transparent-hugepage settings and counters before and after the phase; the disks' I/O schedulers; the monitor's child's arguments, scheduling policy and I/O class; the files on the drive after the first backup and after the phase, with their sizes; the tail of `duplicity`'s log Déjà Dup keeps in its cache.

## 2. Inputs (D113–D118)

- **The state.** The upgrade campaign's chroot (`../upgrade/method.md` §2: the 1,445 packages of `upgrade-layer.txt`, `mmdebstrap --variant=apt`, components `main restricted universe multiverse`, `LANG=en_US.UTF-8`) built from Ubuntu's snapshot service at T0 = `20260922T170000Z` (D64); then, on the harness CPUs, the stock sources at T0 and `apt-get install deja-dup` with apt's defaults, recommends included (D113): Déjà Dup 45.2 with `duplicity` 2.1.4 (S2-64).
- **The user.** A non-root user with a home under `/home`, its XDG folders made by the layer's `xdg-user-dirs-update`, as the Tracker campaign's; a runtime directory `/run/user/<uid>`.
- **The set** (9.7 D7; D118). Mahoney's `10gb.zpaq`, fetched, checked against the archive's pinned SHA-256, extracted with `zpaq x` on the harness CPUs and verified against the pinned manifest (`inputs.json`); the tree `10gb/` placed as `~/10gb`, owned by the user.
- **The drive** (D114). A sparse 40 GiB image under the work directory, `mkfs.ext4` with the label `Backup`, attached by `losetup --direct-io=on` and mounted in the chroot at `/media/<user>/Backup`, owned by the user. Déjà Dup's `local` backend, `folder` `/media/<user>/Backup/$HOSTNAME`.
- **The settings** (D117). Déjà Dup's defaults; `backend` `'local'` and the folder above, written before the first backup; encryption on, "Remember password" on, at the first backup's password page; `periodic` `true`, written after it. The keyring's password and the backup's are design strings.
- **The change set** (D115). `fileset.py change --days 7`: Cumulus's daily rates over seven days, scaled to the set — new files totalling 3.042 % of its bytes and changed files totalling 8.831 % — by 9.7's seeded method and seed; applied as root on the harness CPUs, the new files then given to the user.
- **The display.** Xvfb `:99`, 1280×800×24 (9.5's), on the harness CPUs; its socket bound into the chroot's `/tmp/.X11-unix`.
- **The chroot's mounts.** As the upgrade campaign's: `/run/systemd/system` absent, `ischroot` holds; with the X socket, `/dev/shm` and the drive.

## 3. Phases

In this order within each job:

| Step | Command | CPUs | Instruments |
|---|---|---|---|
| build | `mmdebstrap` (§2) | harness | none |
| install | `apt-get install deja-dup` at T0 (§2) | harness | none |
| state | the user, its folders, the set as `~/10gb`, the drive mounted (§2) | harness | none |
| first backup | a session of the user's own (`dbus-run-session`), the keyring unlocked, the location written with `gsettings`, `deja-dup --backup`; the driver takes the folders and location pages as they open, fills the password page (the password twice, "Remember password" on) and waits for `deja-dup` to exit | harness | none |
| the week | `periodic` on; the change set applied; `last-backup` and `last-run` set 8 days back (D118) | harness | none |
| warm start | the set and `~/.cache/deja-dup` read whole (D116) | harness | none |
| cache check | `fincore` over the set and over `~/.cache/deja-dup` | harness | none |
| `dejadup-incremental` | a session of the user's own on the measured CPU (`taskset`, `dbus-run-session`), the keyring unlocked, `deja-dup-monitor` started in it; the driver on the harness CPUs waits for the `deja-dup` the monitor starts, records its arguments, policy and I/O class, and waits for it to exit. The phase ends at that exit; no cap of its own (the workflow's 330-minute job limit) | harness (the driver); measured (the session and the backup) | §4 |
| after | the session stopped; the drive and the settings read | harness | none |

The kernel's transparent-hugepage settings (`enabled`, `defrag`, `khugepaged/defrag`, `khugepaged/scan_sleep_millisecs`, `khugepaged/alloc_sleep_millisecs`, `khugepaged/pages_to_scan`) and `/proc/vmstat`'s `thp_collapse_alloc`, `thp_collapse_alloc_failed`, `thp_fault_alloc` and `thp_fault_fallback` are recorded before and after the phase.

## 4. Instruments

As the upgrade campaign's (`../upgrade/method.md` §4).

## 5. Analysis rules

- **The job (D112, D118).** Every process of the tree rooted at the first process in the phase that executed `/usr/bin/deja-dup`, from its first schedule-in on the measured CPU to its exit; a process of the tree that outlives it counts until that exit. The CPU total is perf's, the sum of the tree's runs on the measured CPU; taskstats' per-thread rows are reported beside it (the HandBrakeCLI campaign's §5).
- **Outside the job.** The monitor, the session bus, the keyring daemon, anything the bus starts, the loop device's kernel threads and anything else on the measured CPU, reported by `comm` beside the job.
- **Form.** Fixed after the dry run by 9.6 D7's criterion (§8).
- **Wake.** As the upgrade campaign's §5.
- **Also reported.** The job's process and thread counts and CPU by process and thread; the job's span; the job's block-I/O delay and its `sched_stat_iowait` rows; the time from the monitor's start to the job's first schedule-in.

## 6. Scope, written into the entry

Runner spec (4 vCPU Azure VM, `ubuntu-24.04`, kernel and CPU model as recorded, the AMD EPYC 7763); one CPU, the rest of the machine idealised; the session and the runner's agent processes share the measured CPU and are outside the tree; no desktop session beyond Xvfb, a session bus and the keyring, no system bus, no display refresh; the kernel's transparent huge pages in the runner's `always` mode. Déjà Dup 45.2 as Ubuntu 24.04 packages it, at its defaults with its password remembered (D117), making its scheduled weekly incremental through `duplicity` 2.1.4 — started by its own monitor in the idle CPU and I/O classes (D112) — of a home holding Mahoney's 10 GB set (9.7 D7) after seven days of Cumulus's personal-machine change rates, the changed part an upper bound (D115), from a warm start (D116), to an ext4 filesystem on a loop device standing in for an external drive (D114), in D37's chroot built at 2026-09-22T17:00Z (D113).

## 7. Release

Raw records per job are released as a GitHub release named in the registry entry at fold-in. The release is outward-facing and is published on 인지오's go-ahead.

## 8. Amendments

- 2026-10-04, the dry runs on the 100 MB subset, not pooled. Runs #175, #178 and #179 stopped at the gate (AMD EPYC 9V74). Run #176 (37171455182, the EPYC 7763): GTK 4's own renderer left the assistant's window black to every screenshot under Xvfb, and the job then waited on the open assistant. Amending §3's "first backup": its session, which is not measured, draws with cairo (`GSK_RENDERER=cairo`); the monitor's session keeps GTK's defaults, an automatic run presenting no window; a failed driver stops the session. Run #177 (37173423412): tesseract read every word of the folders page but the default button's, white on blue. Amending §3: the driver finds the page's default button as the blue box in the header bar and reads its label from that box alone. Run #180 (37174202662, the EPYC 7763): every step held — the first backup through the assistant (one full chain on the drive, the password in the keyring), the week, the set and Déjà Dup's cache cached at 1.0000; `deja-dup --backup --auto` seen 120.1 s after the session's start, in `SCHED_IDLE` and the idle I/O class, on the measured CPU, its parent in `/proc` `systemd`; `last-backup` advanced; the drive's chain one full backup and one incremental. The disks' I/O scheduler is `none` (`sda`, `loop0`): the idle I/O class has no effect on the runner. The job, 6.8 s on the subset, was 49 processes of 103 threads with 6.597 s of CPU: `deja-dup`; seven `duplicity` runs, each after a `sh` and `rm` that clear its lockfiles (S2-62 `DuplicityInstance.vala`); `gpg` for each volume and a `gpg-agent` one of them started, which outlives the job; and the monitor Déjà Dup's own start-up runs through `chrt` and `ionice` (`app/WidgetUtils.vala:30–47`, `start_monitor_if_needed`, which "will quickly and harmlessly bail if it can't claim the bus name"). Amending §1's "Recorded per job": the command line of every `duplicity` and `gpg` the job starts, read from `/proc` by the driver on the harness CPUs, each `duplicity` run's mode taken from it.
- 2026-10-04, dry run on the 10 GB set (run 37174980221, #182, the EPYC 7763; changelog D119–D121) — amending §1 "The list" and §5 "Form". Recorded from the run: the layer plus 9 packages; the first backup by the assistant in 526 s, 5,025,070,033 B in 24 volumes, the password in the keyring; the change set, 9,729 changed files of 883,122,363 B and 304,219,409 B new; the set cached at 0.9995, Déjà Dup's cache at 1.0000; `deja-dup --backup --auto` 121.0 s after the session's start, in `SCHED_IDLE` and the idle I/O class; the job 170.70 s with 169.686 s of CPU, saturation 0.9940, 52 processes of 115 threads; `duplicity` 0.569 of the CPU over eight runs, `deja-dup` 0.291, `gpg` 0.135; the busiest threads 0.322, 0.291 and 0.232; the block per run mean 2.77 µs; 285 disk waits, 0.204 s; the drive's chain one full backup and one incremental of four volumes. The runs, by their command lines: `duplicity --version`; `collection-status --no-encryption` and a dry run without the password, ended within 0.3 s; `collection-status`; `incremental --dry-run`, 64.5 s; `incremental`, 100.7 s; the verify's `collection-status` and `restore`, 4.2 s. Every backup runs the dry run: `ToolJob.Flags` is a plain enum (S2-62, D119). Form: a new entry in the batch-loop form over the tree, `incremental-backup`, the task showing `deja-dup` at tier 1; `file-backup` leaves at fold-in (D119–D121). The list: over the job, the run between voluntary blocks and the block per run, and the CPU total. Run #181 stopped at the gate.
