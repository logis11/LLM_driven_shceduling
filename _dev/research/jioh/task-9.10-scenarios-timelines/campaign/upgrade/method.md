# Task 9.10 — the unattended-upgrade campaign: method (2026-10-01)

The observation behind the unwanted job of the ten interactive attribute counterparts and `c2-p2b` (changelog D3, D36–D40), run on GitHub-hosted runners under `../../../measurement-campaign-workflow.md`, pinned to one CPU. Amended only by a dated entry in §8. Tooling: `dataset/tools/meas/background/` — the `upgrade` job of `run.sh`, the package list `upgrade-layer.txt`, `analyze.py` and `pool.py` — workflow `.github/workflows/meas-background.yml`, trigger `.github/campaign-background.json`, loop family `background`, app `upgrade`.

## 1. Runs

- **Machine.** The AMD EPYC 7763 only; `machine_gate.sh` stops a job that drew another model before any install or measurement, and a gated job is not a repeat.
- **Tag.** `meas-ci:background:<YYYY-MM-DD>`, the launch date of the first batch; each repeat's run id in the pooled record.
- **Repeat.** One job per repeat index: the state built, the download stage run, the install stage measured (§3). Identical work, so an added repeat is the next index. Artifact `meas-background-upgrade-r<k>-<mode>`.
- **Modes.** `dry` — the tooling checked on one job, its `perf.data` kept; `full` — the campaign.
- **The list** (the workflow's stability rule, every value the fold-in carries): from `upgrade-install`, the run between voluntary blocks and the block per run, each tested by its mean as the table carries it (the ratio estimator), and the CPU total, tested by its per-repeat values (D17, D39). The process count is reported, not carried.
- **Tolerance.** The workflow's 5 % of the mean, and 1 µs for the two time tables where larger; this campaign reports no comparison of carried values, so the 5 % rests on the workflow's ground alone.
- **First batch.** Repeats 1–5: the rule's minimum (`kalibera-ismm13` §11); the dry run is one job and gives no spread to project from. Then one repeat at a time, or a batch up to the pool's projection (9.7 D26), the rule read after each landing.
- **Validity** (the workflow's step 4, with this job's own checks): the gate open on the EPYC 7763; every recorded return code zero (perf record's 130 is its SIGINT stop); the layer built with no package missing or extra; the download stage fetched four packages; the stage changed four, 2.39-0ubuntu8.7 → 2.39-0ubuntu8.8, and its log reads "All upgrades installed"; the change set the same in every repeat; `/run/systemd/system` absent in the chroot (`pool_runs.py`).
- **Recorded per job.** `spec.json` (runner spec), `report.kv`, CPU model and kernel, `df` of `/` and `/mnt`, `lsblk`, the kernel-config lines for taskstats, delay accounting, schedstats and `HZ` (`kconfig.txt`), mmdebstrap's version and log, the chroot's installed set before and after the stage, the logs the stages write.

## 2. Inputs (D36, D37)

- **The state.** The default layer of an English install — the 1,445 packages of `upgrade-layer.txt`, the image's `casper/minimal.manifest` less the 43 its `minimal.en.manifest` removes (S2-01, S2-33) — built by `mmdebstrap --variant=apt` into a directory from Ubuntu's snapshot service at T0 = `20260727T000000Z`, the `noble`, `noble-updates` and `noble-security` suites, components `main restricted universe multiverse`. The packages are taken at their versions at T0. The installed set is recorded and compared with the list (missing, extra).
- **The system locale.** `LANG=en_US.UTF-8` in `/etc/default/locale`, the English install's (design, D37).
- **The sources.** The stock deb822 pair (`noble noble-updates noble-backports`; `noble-security`) pointed at the snapshot of T1 = `20260728T000000Z` for both hosts; mmdebstrap's own sources and options removed. The release files carry the archive's own `Origin` and `Suite`, which the unattended upgrade's allowed origins match.
- **The chroot's mounts.** `proc`, `sysfs`, the runner's `/dev` and `/dev/pts`, and a fresh tmpfs on `/run` holding only the resolver's stub file: `/run/systemd/system` is absent, so no package script reaches the runner's systemd, and `ischroot` holds (S2-32).

## 3. Phases

In this order within each job:

| Step | Command | CPUs | Instruments |
|---|---|---|---|
| build | `mmdebstrap` (§2) | harness | none |
| download stage | `apt.systemd.daily update` in the chroot, the environment reduced to `PATH` and `LANG`, stdin from `/dev/null` | harness | none |
| `upgrade-install` | `apt.systemd.daily install`, `apt-daily-upgrade.service`'s `ExecStart` (S2-03), in the chroot, the same environment; `sudo` on the harness CPUs, `taskset` placing the chroot's command on the measured CPU. The unit's `ExecStartPre`, `apt-helper wait-online`, is not run (D38) | measured | §4 |

## 4. Instruments

As 9.7's method §4 for the phases without `perf trace`: `perf sched record -k CLOCK_MONOTONIC -a` with the exec rows, as root on the harness CPUs over the whole phase; `perf sched timehist --state`, `-w` and `perf script` for the fork, wakeup-new, exit, exec and `sched_stat_iowait` rows; `kernel.sched_schedstats=1` and `kernel.task_delayacct=1` before the phase; the taskstats listener registered on the measured CPU; `phase.sh`, `edges.jsonl`, `clock.json`.

## 5. Analysis rules

- **Phase read.** `upgrade-install`, the whole phase.
- **The tree.** Rooted at the process `taskset` executed into `chroot` (`launched_root`); every process of the tree is the program's (D39).
- **Form (D39).** `cpu-batch`'s batch loop over the tree: the runs between voluntary blocks pooled over every process, and the block after each run — the tree's off-CPU time from that run's voluntary block, zero when another of its processes runs on or is runnable (9.7 D29; `shapes`). The CPU total is the sum of the tree's perf run segments on the measured CPU, taskstats' CPU beside it as the cross-check, and is carried (D17).
- **Wake.** As 9.7's method §9 (D21): a schedule-in is a wake when the thread's previous switch-out state is a sleep state, a resume after preemption when it is R; the wakeup rows the cross-check.
- **Also reported.** The process count; CPU by executed program; the stages' times; the installed set's change; the logs.
- **The entry (D40).** `package-upgrade`; its one task shows `unattended-upgr`, the observed `comm` of `/usr/bin/unattended-upgrade`.

## 6. Scope, written into the entry

Runner spec (4 vCPU Azure VM, `ubuntu-24.04`, kernel and CPU model as recorded, the AMD EPYC 7763); one CPU, the rest of the machine idealised; the runner's agent processes share the measured CPU and are outside the tree; no desktop session. The stock unattended upgrade's install stage on 2026-07-27's security updates (D36), in a chroot of the default layer of an English install, built from Ubuntu's snapshot service: no running init, so `libc6`'s postinst skips `systemctl daemon-reexec` and the reboot-required notice (S2-32); the layer holds no kernel and no boot loader (S2-33); the sources point at the snapshot service; the unit's `apt-helper wait-online` step is not carried — on an online desktop it is a `systemctl is-active` query per network manager and the active manager's waiter, returning once online (S2-34, D38).

## 7. Release

Raw records per job are released as a GitHub release named in the registry entry at fold-in, with `upgrade-layer.txt`. The release is outward-facing and is published on 인지오's go-ahead.

## 8. Amendments

- 2026-10-01, the dry run (run 36843481310, #99; changelog D38) — amending §3: the unit's `apt-helper wait-online` is not run; the phase is `apt.systemd.daily install` alone.
- 2026-10-01, the first batch and the added batch (runs #100–#105; changelog D45) — amending §1 "First batch": repeats 1–5 held the block per run and not the run between voluntary blocks (±6.31 %) or the CPU total (±7.72 %); the pool projected nine, and repeats 6–9 were added as one batch (9.7 D26). At nine the rule holds on all three values.
