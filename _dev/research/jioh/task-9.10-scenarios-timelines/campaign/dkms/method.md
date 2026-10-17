# Task 9.10 — the DKMS campaign: method (2026-10-02)

The observation behind `c7-compile`'s unwanted job (changelog D4, D46–D50), run on GitHub-hosted runners under `../../../measurement-campaign-workflow.md`, pinned to one CPU. Amended only by a dated entry in §8. Tooling: `dataset/tools/meas/background/` — the `dkms` job of `run.sh`, which reuses the `upgrade` job's state build (`upgrade-layer.txt`), `analyze.py` and `pool.py` — workflow `.github/workflows/meas-background.yml`, trigger `.github/campaign-background.json`, loop family `background`, app `dkms`.

## 1. Runs

- **Machine.** The AMD EPYC 7763 only; `machine_gate.sh` stops a job that drew another model before any install or measurement, and a gated job is not a repeat.
- **Tag.** `meas-ci:background:<YYYY-MM-DD>`, the launch date of the first batch; each repeat's run id in the pooled record.
- **Repeat.** One job per repeat index: the state built, the download stage run, the install stage measured (§3). Identical work, so an added repeat is the next index. Artifact `meas-background-dkms-r<k>-<mode>`.
- **Modes.** `dry` — the tooling checked on one job, its `perf.data` kept; `full` — the campaign.
- **The list** (the workflow's stability rule, every value the fold-in carries; D52–D56): each job kind's per-(member, step) CPU table (D53: 56 tables over the four trees), make's dispatch run, the serial tail's run between voluntary blocks and its block per run (D54) — each tested by its mean as the table carries it (the ratio estimator) — and the CPU total the entry carries (jobs, make, tail), tested by its per-repeat values (D17, D56's C). The job counts and the job order are reported.
- **Tolerance.** The workflow's 5 % of the mean, and 1 µs for time tables where larger.
- **First batch.** Repeats 1–5: the rule's minimum (`kalibera-ismm13` §11). Then one repeat at a time, or a batch up to the pool's projection (9.7 D26), the rule read after each landing.
- **Validity** (the workflow's step 4, with this job's own checks): the gate open on the EPYC 7763; every recorded return code zero (perf record's 130 is its SIGINT stop); the layer built with no package missing or extra; the state's kernel `7.0.0-31-generic` and `nvidia/595.91.07` installed for it; the stage installed the kernel `7.0.0-34` and `xdg-desktop-portal`, its log reading "All upgrades installed"; `nvidia/595.91.07` installed for `7.0.0-34-generic` after it, its five modules present; the change set the same in every repeat; `/run/systemd/system` absent in the chroot.
- **Recorded per job.** As the upgrade campaign's (`../upgrade/method.md` §1), and: the state's kernel and driver installs' logs, `dkms status` before and after the stage, `dkms`'s version, the compiler, the foreign architectures, the `make.log` of the build for `7.0.0-34-generic` and the module files it installed.

## 2. Inputs (D48, D49)

- **The state.** The upgrade campaign's chroot (`../upgrade/method.md` §2: the 1,445 packages of `upgrade-layer.txt`, `mmdebstrap --variant=apt`, components `main restricted universe multiverse`, `LANG=en_US.UTF-8`) built from Ubuntu's snapshot service at T0 = `20260922T170000Z` (D51). Then, on the harness CPUs, with the stock deb822 sources pointed at T0: `apt-get install -y linux-generic-hwe-24.04` (the kernel the installer adds, S2-33; `7.0.0-31` at T0) and `apt-get install -y nvidia-driver-595-open` (D46's user), which pulls in `dkms` and `nvidia-dkms-595-open` 595.91.07 and builds the module for `7.0.0-31-generic`. Both with apt's defaults, recommended packages included; apt's package cache then cleaned, so the download stage's count is the day's.
- **The sources.** The stock deb822 pair pointed at the snapshot of T1 = `20260924T000000Z`, as the upgrade campaign's.
- **The chroot's mounts.** As the upgrade campaign's: `/run/systemd/system` absent, `ischroot` holds.
- **The build's parallelism** (D4, D50). `OMP_NUM_THREADS=8` in the measured stage's environment: `nproc` returns it (S2-40), and NVIDIA's `dkms.conf` builds with `make -j` of `nproc` (S2-39), as `dkms`'s own default does (S2-03) — D4's eight-thread desktop on the one measured CPU. Design.

## 3. Phases

In this order within each job:

| Step | Command | CPUs | Instruments |
|---|---|---|---|
| build | `mmdebstrap` (§2) | harness | none |
| state | `apt-get install` of the kernel, then of the driver package (§2) | harness | none |
| download stage | `apt.systemd.daily update` in the chroot, the environment reduced to `PATH` and `LANG`, stdin from `/dev/null` | harness | none |
| `dkms-install` | `apt.systemd.daily install` in the chroot, the environment `PATH`, `LANG` and `OMP_NUM_THREADS=8`; `sudo` on the harness CPUs, `taskset` placing the chroot's command on the measured CPU; `apt-helper wait-online` not run (D38) | measured | §4 |

## 4. Instruments

As the upgrade campaign's (`../upgrade/method.md` §4).

## 5. Analysis rules

- **Phase read.** `dkms-install`, the whole phase.
- **The stage's tree.** Rooted at the process `taskset` executed into `chroot` (`launched_root`).
- **The job (D50).** Every process rooted at a process that executed `/etc/kernel/postinst.d/dkms`, `/etc/kernel/header_postinst.d/dkms` or `/usr/lib/dkms/dkms_autoinstaller`, and its descendants by the fork rows (`hook_subtrees`). Each hook run is reported apart: its processes, CPU, span and CPU by executed program. The rest of the stage is reported, not carried.
- **Form (D52–D55).** Within the hook run that built the module (the one with the most CPU), the make jobs are 9.6's (`jobs_of`), a job's members stopping at a nested `make` (`modbuild.jobs_of`). Object jobs are 9.6's (a job with `fixdep`); probe jobs whose root shell starts a shell are `conftest` tests — variant `b` when the test runs `as`, else `a` — and the other probe jobs kbuild's probes. Each job is fitted to its kind's tree (`modbuild.TREES`) by role, children in fork order; a further process of a role the tree has there adds its CPU to that member step by step, and any other process its subtree's CPU to its parent member's step in which it was forked (D53's fold). A member's step is its CPU on the measured CPU between the exits of its own children (9.6 D20). Dispatch is make's run between consecutive forks (9.6). The tail is the hook run's rows from the last object or link job's end, outside any job and `make`, as the batch loop's runs between voluntary blocks and blocks (D54). Helper and link jobs, the work before the `make` and the second hook run are the unmodelled remainder, reported (D54).
- **Wake.** As the upgrade campaign's §5.
- **Also reported.** The stage's CPU and process count; which hook built; the `make.log`'s object lines; the installed set's change.

## 6. Scope, written into the entry

Runner spec (4 vCPU Azure VM, `ubuntu-24.04`, kernel and CPU model as recorded, the AMD EPYC 7763); one CPU, the rest of the machine idealised; the runner's agent processes share the measured CPU and are outside the tree; no desktop session. DKMS's autoinstall of `nvidia-dkms-595-open` 595.91.07 for the security kernel `7.0.0-34-generic`, run by the stock unattended upgrade of 2026-09-23 (D48), in the upgrade campaign's chroot with the HWE kernel and `nvidia-driver-595-open` added (D49): the build runs at `-j8` through `OMP_NUM_THREADS` (D50); no boot loader and no `shim-signed`, so `dkms` finds no `update-secureboot-policy` and signs no module (`dkms:965–976`, S2-03), where a Secure Boot desktop signs the five; the sources point at the snapshot service.

## 7. Release

Raw records per job are released as a GitHub release named in the registry entry at fold-in. The release is outward-facing and is published on 인지오's go-ahead.

## 8. Amendments

- 2026-10-02, the dry run (run 36980404122, #106; changelog D51) — amending §2 "The state": T0 is `20260922T170000Z`, not `20260923T000000Z`. At the latter the updates pocket already held the kernel `7.0.0-34`, the state was on it, and the stage installed `xdg-desktop-portal` alone.
- 2026-10-02, the first batch (runs #108–#109, repeats 1–5, the gated index 4 relaunched once) — every repeat valid; the same change set, job counts (200 object, 1,125 kbuild probes, 145 and 87 `conftest` tests) and carried share (98.2 %) in every repeat; the rule held on 23 of the 60 values, the carried CPU total ±6.0 % (210.6–236.1 s); the pool projected 23 repeats, and repeats 6–23 were added as one batch (9.7 D26, run #110).
