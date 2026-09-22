# Task 9.9 — measurement campaign method (draft, 2026-09-22)

The observation behind the four entries that replace `system-daemon` — the compositor and shell, the audio stack, `systemd` and `dbus-daemon` (changelog D3–D8) — measured in the terminal idle state of an Ubuntu desktop session (D9), run on GitHub-hosted runners (phase decision 5) under `../../measurement-campaign-workflow.md`, pinned to one CPU (9.5 follow-ups decision 3). Written before any measurement; amended only by a dated entry in §10.

Tooling: a tool tree `dataset/tools/meas/session/` (`run.sh`, `analyze.py`, `pool.py`), workflow `.github/workflows/meas-session.yml`, trigger `.github/campaign-session.json`, and a loop family `session` in `dataset/tools/meas/loop/common.py` with one app, `session`. `meas-gui.yml` retires once the four entries carry this campaign's values (D8; 9.8 D13).

## 1. Runs

- **Machine.** The AMD EPYC 7763 only; `machine_gate.sh` stops a job that drew another model before any install or measurement, and a gated job is not a repeat (campaign workflow).
- **Tag.** `meas-ci:session:<YYYY-MM-DD>`, the launch date of the first batch (9.5 D27); each repeat's run id in the pooled record and in each archetype's `validation_stats.run`.
- **Repeat.** One job per repeat index: install, log in, settle, steady (§3). The work is identical in every repeat and nothing is driven by recorded input, so an added repeat is the next index.
- **Modes.** `dry` — one job on shortened phases, to verify the session comes up as §2 states and reaches the blank (§3), not pooled; `probe` — the long-phase probe of §3, never a repeat, excluded from the pooled set (9.5 D35); `full` — the campaign.
- **Recorded per job.** `spec.json` (runner spec), the report with `gate` and `machine.model`, CPU model and kernel, the installed version of every observed package (`gnome-shell`, `mutter`, `pipewire`, `wireplumber`, `pipewire-pulse`, `systemd`, the bus implementation), the kernel-config lines for `PERF_EVENTS`, `SCHED_TRACER`, `TASKSTATS`, `TASK_DELAY_ACCT` and `HZ`, and the session census of §2.

## 2. The subject: one Ubuntu desktop session

One subject, since the four entries are observed in one session (D8).

1. **Install.** `ubuntu-desktop-minimal` from the runner's own archive (noble), which carries GNOME Shell 46.0 and Mutter 46.2 (D3), PipeWire 1.0.5 with WirePlumber 0.4.17 (D4), and the Ubuntu session defaults of `ubuntu-settings` (S2-30). No setting is changed from the installed defaults except where this section says so. `gdm.service` is stopped and masked after the install (D11): there is no display manager, and the login of item 2 takes its place.
2. **Log in.** A dedicated user, logged in through PAM so that logind creates a session for it and pid 1 starts its user manager (`user@.service`, S2-29). The session leader is a transient system unit, `systemd-run -p PAMName=login -p User=<user>` with `XDG_SESSION_TYPE=wayland`, `XDG_SESSION_CLASS=user` and `XDG_SESSION_DESKTOP=ubuntu`, running `gnome-session --session=ubuntu`, which starts the session's units in the user manager (D11). The session has no seat; logind counts a seatless session as active (S2-31). GNOME Shell runs inside `org.gnome.Shell@wayland.service` and Mutter keeps Xwayland on demand (S2-28). The user logs in twice (D11): a priming login, which does the account's first-login work and is not measured, then a logout and the measured login. If the install ships a first-run wizard, it is dismissed by its done stamp in the user's home, the one change to the user's state.
3. **Headless.** The runner has no display device, so GNOME Shell runs with `--headless --virtual-monitor 1920x1080@60`, added by a user drop-in on `org.gnome.Shell@wayland.service` that changes `ExecStart=` and nothing else. This is the one departure from the shipped unit, and it is stated in every entry's scope. The audio stack runs with no sound device (the Azure kernel has no `CONFIG_SND`, S4-15); WirePlumber creates its null sink as it does on a machine without one.
4. **Census, recorded outside the `perf` recording (D13): at the steady edge before `perf` starts, and after it stops.** The process tree with each process's cgroup and command line; `systemctl list-units` for the system and the user manager; `loginctl show-session`; whether any `Xwayland` or `Xorg` process exists (the held display-server question); whether the buses are `dbus-daemon` or `dbus-broker` (D6); whether a greeter process exists; gnome-session's `SessionIsActive`, the power daemon's idle mode, Mutter's `PowerSaveMode` and the shield's state at the start and the end of the steady phase (S2-30, S2-31). The census is released with the raw records.
5. **Pinning.** Only the four entries' processes are confined to the measured CPU, at run time (D10): pid 1 by `systemctl set-property --runtime init.scope AllowedCPUs=`, the system bus by the same on `dbus.service`, and in the user manager the session bus, GNOME Shell and the three PipeWire services by `systemctl --user set-property --runtime … AllowedCPUs=` on their units, with the user manager itself by `cpuset.cpus` on its `init.scope` cgroup (S4-05, S4-07). The user manager is given the cpuset controller by a system drop-in on `user@.service`, `Delegate=pids memory cpu cpuset`, written before the priming login (D14); the shipped unit delegates `pids memory cpu` (S2-29). Every other process — the other session processes (settings daemons, portals, the indexer), the other system services, and everything the harness runs (`perf`, the driver, the runner's agents) — stays on the other CPUs (D12): every loaded service and scope of both managers other than the four entries' units and the slices above them is set to `AllowedCPUs=` the other CPUs, and the harness's processes are moved by `taskset`. The pin and a first sweep run once the measured login is up; a second sweep runs at the steady edge, before `perf` starts. The census records each process's allowed CPUs at the start and the end of the steady phase.

## 3. Phases

`install` → `priming` → `login` → `session-settle` → `idle-settle` → `steady`, edges written to `phases.jsonl` and `edges.jsonl`. Only `steady` is carried.

- **`priming`.** The priming login of §2.2, a fixed length from the probe, then the logout (D13).
- **`session-settle`.** The session's own start-up work after login — the shell starting, the settings daemons, first-login services such as a file indexer's initial crawl or a software-catalogue refresh — ends before the idle state is counted, as 9.5 D34 requires of launch work. Its length comes from the long-phase probe.
- **`idle-settle`.** Nobody touches the session from login on, so the idle timer runs from the first moment: the session goes idle at `idle-delay` (300 s, S2-14), the shield fades in over 10 s and locks with no delay (S2-13, S2-31), the power daemon blanks once the shield is active (S2-30), and the audio node is suspended 5 s after anything stops playing (S2-19). `steady` begins at a fixed offset from the measured login, after the later of the two settles (D13). At the edge the job checks that the shield is active, Mutter's `PowerSaveMode` reports the monitor off and `SessionIsActive` holds; a job that fails the check is not a repeat.
- **`steady` length.** Open, set from the probe before the first batch (§9). Several components are sparse — pid 1 woke about every 5.5 s and the system bus about every 7.5 s on the Phase 2 VM (scope card items 14, 15) — so the phase must be long enough that each carried table has samples enough for its per-repeat mean to converge.
- **The dry run.** One job in `dry` mode runs a shortened priming login, then the measured login idle past `idle-delay` and the blank, the edge check, and a short `steady` (D13).
- **The probe.** One job in `probe` mode runs a 30 min priming login and a measured login with one 3 h idle phase, both read per 10 s slice for each entry's CPU and wakes (D13). It polls the shield and blank state every 10 s during the recording; the polls are stated in its record. It shows where start-up work ends, whether the shield and the blank are reached, whether the compositor's wakes stop once the shield is up and nothing draws (a lock-screen clock may still draw about once a minute, S2-32), and the yield of each sparse component.

## 4. Instruments

`perf sched record -k CLOCK_MONOTONIC -a` on every CPU with `perf sched timehist --state` and wakeups, the campaign instrument of 9.5–9.8, so every thread's schedule-ins and wakeups are recorded, including processes the workflow did not launch (S4 §4 T7.4). Process instances are told apart by pid from the census: pid 1 against the user manager (D7), the system bus against the session bus by their command lines (`--system`, `--session`; D6), and the three PipeWire services by comm (D4).

## 5. Analysis rules, fixed before the run

- **One wake** is a schedule-in preceded by a wakeup event for that thread since its last sleep; a resume after preemption folds into the wake it continues, decided by the thread's previous switch-out state (campaign workflow).
- **Components** are per process instance and thread comm (D4, D6, D7; 9.5 D16), each carrying `wakes_per_s` and measured `gap` and `run` quantile tables (9.5 D17), kept in descending wake rate until they cover 95 % of the entry's steady-phase wakes, the rest pooled into one residual component; the cut is stated per entry.
- **Thread counts** are carried as their observed range and are not on the stability list.
- **Foreign work on the measured CPU.** Schedule-ins on the measured CPU by any user-space process outside the four entries' are counted per repeat; a repeat with any is not pooled (D12). Kernel threads — children of `kthreadd` in the census — are counted apart on the measured CPU, schedule-ins and CPU time, and reported per repeat, not gated (D14).
- **No pooling across entries or instances.** Each entry's values come from its own processes; pid 1 and the user manager, and the two buses, are separate components; nothing is fitted across processes, the defect of the entry being replaced (scope card items 1–4).

## 6. The list, the tolerance, the first batch

1. **The list — every value the fold-in carries.** Per entry, per component: the `gap` quantile table, the `run` quantile table and `wakes_per_s`; and each entry's residual. Thread counts are excluded.
2. **The smallest effect the slice reports.** The slice reports no comparison: each entry is observed in one state (D9). The standing tolerance applies unchanged: 5 % of the mean, or 1 µs where larger (`TOLERANCE` in `stability.py`).
3. **First batch.** Five repeats, the rule's minimum, because no earlier run of this subject exists to size the batch from. Repeats are added one at a time afterwards until every value on the list holds; the gated indices of the first batch are relaunched together.
4. **What a repeat is.** The next repeat index (§1).

9.6 D29's and 9.5 D57's exceptions are available but not invoked in advance; each applies only by 인지오's decision per value.

## 7. Scope, written into every archetype

Each entry states: the runner spec, CPU model and kernel; the package versions observed; the state — the Ubuntu 24.04 desktop session idle past `idle-delay`, shield up and locked, blanked by the power daemon, nobody present, no application running — and what it is not; and the limits: a headless virtual monitor at 60 Hz with no display and no vblank, GNOME Shell started with `--headless --virtual-monitor` by a unit drop-in; the cpuset controller delegated to the user manager by a drop-in on `user@.service`; per-CPU kernel threads sharing the measured CPU; no seat; a null sink and no sound device; a server VM with its own agents present off the measured CPU; only the four entries' processes on the measured CPU, the rest of the session on the others (§2.5); no display manager, the session started by a transient PAM unit after a priming login (§2.2).

## 8. Release

The raw records, including every job's census, are one release, as 9.5–9.8 released theirs. Pooled `results.md` and `pooled.json` go in this folder; each entry's row goes into `../../measurement-campaign-record.md`. Publishing the raw records outward is asked before it is done.

## 9. Open before the first batch

- **Whether the session comes up as §2 states** — the seatless PAM login, `SessionIsActive`, the shell under its unit with the drop-in, the null sink. The dry run verifies it; a departure is a method amendment, not a silent change.
- **Whether the shield and the blank are reached headless**, and what the compositor does once they are. The dry run shows whether they are reached, the probe what follows; if the session never blanks, whether the entries are measured shield-up without the blank is a design question for 인지오.
- **`priming`, `session-settle` and `steady` lengths**, from the probe, written into §10 before the first batch.
- **Whether GDM 46's greeter keeps running after the user logs in** on a stock install, read from its source; if it does, a stated limit of §7.

## 10. Amendments

- 2026-09-22, which processes share the measured CPU (changelog D10) — §2.5: only the four entries' processes; §9's item removed.
- 2026-09-22, the login and the display manager (changelog D11) — §2.1: GDM stopped and masked; §2.2: the transient PAM unit, the priming login, the wizard's done stamp; §7: the limit stated.
- 2026-09-22, the rest kept off the measured CPU (changelog D12) — §2.5: the per-unit sweep, run twice; §5: foreign schedule-ins gate a repeat.
- 2026-09-22, the phases and the checks (changelog D13) — §2.4: census outside the recording; §3: `priming`, the fixed steady edge and its check, the dry run through the blank, the probe's lengths and polling; §9: the dry run's share and the GDM greeter question.
- 2026-09-22, the user side's pin and the kernel threads (changelog D14) — §2.5: cpuset delegated to the user manager, the user manager by its `init.scope` cgroup; §5: kernel threads counted, not gated; §7: both limits stated.
