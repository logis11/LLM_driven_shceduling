# Task 9.10 — the desktop session beside the unattended upgrade: probe method (2026-10-07)

The probe of changelog D165–D167: the stock unattended upgrade run once beside 9.9's blanked desktop session, with systemd as PID 1. It is read for the processes the upgrade brings into the session and for the work it causes in the four session entries. Run on GitHub-hosted runners under `../../../measurement-campaign-workflow.md`; never a repeat; it changes no value. Amended only by a dated entry in §8.

Tooling:
- `dataset/tools/meas/session/run.sh`, modes `upgrade` and `upgrade-dry`;
- workflow `.github/workflows/meas-session.yml`, trigger `.github/campaign-session.json`;
- the reading, `dataset/tools/meas/session/upgrade_probe.py`.

## 1. Runs

- **Machine.** The AMD EPYC 7763 (`machine_gate.sh`), the model 9.9's entries were measured on; the dry run on any model.
- **Indices.** `upgrade-dry` from 90 and `upgrade` after it, clear of the session family's 1–88 (amended in §8). Artifacts are `meas-session-session-r<k>-<mode>`; `session/pool.py`'s name pattern takes neither.
- **One probe after the dry run.** A probe that fails §5 is relaunched as the next index.

## 2. The venue (D166)

9.9's job (its method §2–§3) runs unchanged up to the steady edge:
- `ubuntu-desktop-minimal` from the runner's archive and the slices;
- GDM's automatic login of the measured user, GNOME Shell headless on a virtual monitor;
- the priming login and logout, then the measured login;
- the pin and the two sweeps;
- idle to the shield and the blank, then the edge check.

Three additions come before the first login, each unmeasured, on the harness CPUs, after the install:

1. **glibc back.** Every installed binary package of the `glibc` source is taken to `2.39-0ubuntu8.7` from the snapshot service at 2026-07-27T00:00Z (noble, noble-updates, noble-security). Services are held from starting (`policy-rc.d` 101), as 9.9's install holds them. Afterwards `/var/run/reboot-required` and its `.pkgs` are removed, so the measured upgrade's notice is its own.
2. **The sources.** The runner's apt sources are moved aside. The stock deb822 pair (the form of the upgrade campaign's `upg_sources`) points at the snapshot of 2026-07-28T00:00Z. If the desktop install did not bring `unattended-upgrades`, it is installed from that snapshot. `needrestart`, if the runner image holds it, is removed: it is not in the default install (`upgrade-layer.txt`), and its apt hook would restart services after the job. `20auto-upgrades` is recorded and, if it does not enable both periodic stages, written with the stock two lines. The periodic stamps are removed, so both stages are due as on a first day.
3. **The download stage.** `apt.systemd.daily update` runs against that snapshot. `apt-daily.timer` and `apt-daily-upgrade.timer` are stopped for the job's runtime, so the install stage runs once, when the probe starts it.

## 3. The recording

The recording takes the place of 9.9's steady phase: one `perf` recording on every CPU.

- `pre`: 300 s of the blanked session.
- `job`: `systemctl start apt-daily-upgrade.service`, the unit as its timer starts it through PID 1, its `ExecStartPre` included, from the start command to the unit's return.
- `post`: 600 s after the job.

The lengths are design; the dry run takes 60 s for each window. The edges are written on the trace's clock, `CLOCK_MONOTONIC` (`edges.mono.jsonl`).

## 4. Instruments

- **The trace.** `perf sched record -k CLOCK_MONOTONIC -a -e sched:sched_process_exec`, with its `--state` timehist, the wakeup rows, and the fork, exec and exit rows (`perf script`), as the upgrade campaign's method §4 records them.
- **The censuses.**
  - 9.9's census (`census.py snapshot`) and the session state (`census.py state`) before the recording and after it;
  - inside the recording, `census.py procs`, a read of `/proc` that reaches no measured process, at the job's start and end.
- **The records.** The journal, followed. `unattended-upgrades.log` and its dpkg log, and `dpkg.log`. The glibc binaries' versions before the downgrade, after it and after the job. `/var/run/reboot-required` after the job. The unit's `Result`, `ExecMainStatus` and monotonic timestamps.

## 5. Validity

- The gate is open on the EPYC 7763.
- The downgrade landed: every glibc binary is at 8.7 before the login.
- The download stage fetched the 8.8 packages.
- The edge check holds (9.9 method §3).
- The unit succeeded, `unattended-upgrades.log` reads "All upgrades installed", and the glibc binaries are at 8.8 afterwards.
- The recording stopped cleanly.

## 6. The readings (`session/upgrade_probe.py`)

- **The job's tree.** The processes PID 1 forks inside the job window that exec `apt-helper` or `apt.systemd.daily`, and their descendants by the fork rows.
- **The harness.** The run's own shell and its descendants (`harness.pid`), and the `perf` recording.
- **New names.** Each process that runs in the recording is listed with its name, its exec, its parent chain to its first ancestor in the before-census, and the window it first runs in, if it is none of these:
  - in the before-census;
  - in the job's tree;
  - the harness's;
  - a kernel thread.

  Each process in the after-census that is absent from the before-census is listed the same way.
- **The entries' work.** Per 9.9 instance — PID 1, the user manager, the system and session buses, GNOME Shell, `pipewire`, `wireplumber`, `pipewire-pulse` — the CPU (ms) and the runs in `pre`, `job` and `post`, each also as a rate.

The result decides what D165 sets out. No new name: `c7-idle`'s statement takes the sizes. A new name: a decision of its own.

## 7. Records

`results/`: the reading's JSON and `results.md`. The raw records are released on 인지오's go-ahead.

## 8. Amendments

- 2026-10-07, the method written (D165–D167).
- 2026-10-07, the first dry run (run 37566551146, session 90, on an Intel Xeon Platinum 8573C). The install and the snapshot's package lists landed. The runner then lost communication with the server during the glibc downgrade (§2.1), before any later upload, so no log of the step survived. Amending §2.1:
  - apt's plan is simulated first, and a plan that removes a package stops the job;
  - the running services and processes are recorded before the step;
  - apt's and dpkg's logs are copied every 5 s while it runs;
  - the install's checkpoint comes before the step, so the workflow's 20 s uploads carry them.

  Amending §1: the dry run is relaunched as session 92, and the probe takes the next index after a dry run that passes.
- 2026-10-07, the second dry run (run 37570816998, session 92). The downgrade landed: seven glibc binaries at 8.7, nothing removed, apt's plan as simulated. The runner was lost some 20 s after the sources moved to the day after, the last upload 432 s into the job, at the step that removes the runner's `needrestart`. That removal ran without `NEEDRESTART_SUSPEND`, so `needrestart`'s apt hook could restart every service still mapping the replaced glibc, the runner's agent among them — the loss 9.9's install guards against (`session/run.sh`, `install_session`). Amending §2.2: every apt call of the probe runs with `needrestart` suspended. The dry run is relaunched as session 93.
