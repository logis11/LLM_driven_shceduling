# Task 9.10 — the unattended-upgrade campaign: method (2026-10-01)

The observation behind the unwanted job of the ten interactive attribute counterparts and `c2-p2b` (changelog D3, D36–D38), run on GitHub-hosted runners under `../../../measurement-campaign-workflow.md`, pinned to one CPU. Amended only by a dated entry in §8. Tooling: `dataset/tools/meas/background/` — the `upgrade` job of `run.sh`, the package list `upgrade-layer.txt`, `analyze.py` and `pool.py` — workflow `.github/workflows/meas-background.yml`, trigger `.github/campaign-background.json`, loop family `background`, app `upgrade`.

## 1. Runs

- **Machine.** The AMD EPYC 7763 only; `machine_gate.sh` stops a job that drew another model before any install or measurement, and a gated job is not a repeat.
- **Tag.** `meas-ci:background:<YYYY-MM-DD>`, the launch date of the first batch; each repeat's run id in the pooled record.
- **Repeat.** One job per repeat index: the state built, the download stage run, the install stage measured (§3). Identical work, so an added repeat is the next index. Artifact `meas-background-upgrade-r<k>-<mode>`.
- **Modes.** `dry` — the tooling checked on one job, its `perf.data` kept; `full` — the campaign.
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

Open until the dry run: the entry's form — how the job's process tree is carried — and the comm the job shows (D3's open items).

## 6. Scope, written into the entry

Runner spec (4 vCPU Azure VM, `ubuntu-24.04`, kernel and CPU model as recorded, the AMD EPYC 7763); one CPU, the rest of the machine idealised; the runner's agent processes share the measured CPU and are outside the tree; no desktop session. The stock unattended upgrade's install stage on 2026-07-27's security updates (D36), in a chroot of the default layer of an English install, built from Ubuntu's snapshot service: no running init, so `libc6`'s postinst skips `systemctl daemon-reexec` and the reboot-required notice (S2-32); the layer holds no kernel and no boot loader (S2-33); the sources point at the snapshot service; the unit's `apt-helper wait-online` step is not carried — on an online desktop it is a `systemctl is-active` query per network manager and the active manager's waiter, returning once online (S2-34, D38).

## 7. Release

Raw records per job are released as a GitHub release named in the registry entry at fold-in, with `upgrade-layer.txt`. The release is outward-facing and is published on 인지오's go-ahead.

## 8. Amendments
