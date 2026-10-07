# Task 9.10 — the desktop session beside the unattended upgrade: the probe's reading

The probe of `../method.md` (changelog D165–D167), session 95, run 37579102734, on the AMD EPYC 7763. Never a repeat; it changes no value. The reading beside this page: `upgrade-probe-95.json` and `upgrade-probe-95.txt` (`session/upgrade_probe.py`). The raw records are release `meas-ci-probes-2026-10-07` (D174).

## Validity (method §5)

- **The run.** The gate opened on the EPYC 7763. Every glibc binary was at 8.7 before the login, and 8.8 after the job.
- **The pending set** was glibc's seven binaries: `libc-bin`, `libc-dev-bin`, `libc6`, `libc6-dbg`, `libc6-dev`, `libc6-i386` and `locales`. The runner image's PPA `firefox` was held (method §8). The default install's set is four of them (D37): the runner image adds `libc-dev-bin`, `libc6-dev` and `libc6-i386`.
- **The session** passed the edge check: shield active, monitor off, session active, the four entries alone on the measured CPU.
- **The unit** `apt-daily-upgrade.service` returned `success`, "All upgrades installed", and the reboot notice was raised. The recording stopped cleanly.

## The windows

`pre` 300.0 s of the blanked session; `job` 11.62 s, from the start command to the unit leaving the active states; `post` 600.0 s. The job ran on the harness CPUs, as `system.slice` places it (9.9 D17): 945 processes and 10.12 s of CPU, its tree read from PID 1's two forks that executed `apt-helper` and `apt.systemd.daily`.

## New processes

Outside the before-census, the job's tree, the harness and the kernel. The runner agent's 207 processes (`hosted-compute-agent.service`, the workflow's own steps) are counted apart.

- **In `pre` and `post`, the runner image's timed jobs**, the same kinds in both windows: `cron` and its `sh`, sysstat's `debian-sa1` and `sadc`, `anacron`'s monthly run, and the Azure agent's `iptables` (`walinuxagent.service`).
- **In `job`, under PID 1, two kinds**:
  - **PackageKit's daemon.** `packagekitd` (`packagekit.service`) is D-Bus-activated by apt's PackageKit hook 8.99 s into the job. It used 42.8 ms of CPU in the window and was alive at the job's end and gone by the recording's end. Its one `dpkg` child appeared in the dry runs.
  - **PID 1's generators.** 31 processes in 63 ms, 6.19–6.25 s into the job, 69.9 ms of CPU: the system and environment generators PID 1 runs on re-executing (`systemd-fstab-generator`, `systemd-getty-generator`, `netplan`, `snapd-generator`, `cloud-init-generator` and the rest, with their `mkdir`, `ln`, `sed`, `ls`, `cat`, `uname`). Around them are 106 of PID 1's own helpers, `(sd-close)`, `(sd-exec-strv)` and `(sd-gens)`, 31.5 ms in all.
- **In the session, none.** No process in the measured user's session started during the recording.

## The four entries' work

CPU and runs over the job, against the instance's own rate over `pre`:

| instance | `pre` | `job` | above the `pre` rate | `post` against the `pre` rate |
|---|---|---|---|---|
| PID 1 | 0.037 ms/s, 0.19 runs/s | 372.7 ms, 464 runs | +372.3 ms | 25.2 ms against 22.3 ms |
| system bus | 0.034 ms/s, 0.11 runs/s | 99.2 ms, 482 runs | +98.8 ms | 22.5 ms against 20.5 ms |
| GNOME Shell | 0.250 ms/s, 0.93 runs/s | 1.9 ms, 80 runs | −1.0 ms | 143.9 ms against 149.9 ms |
| WirePlumber | 0.010 ms/s, 0.23 runs/s | 2.8 ms, 94 runs | +2.7 ms | 4.7 ms against 6.2 ms |
| `pipewire`, `pipewire-pulse`, the user manager, the session bus | no run | no run | — | no run |

Beyond the four entries, the session's `update-notifier` used 7.2 ms in the job against 0.2 ms at its `pre` rate. It started no process.
