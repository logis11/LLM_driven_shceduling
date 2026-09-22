# Handoff — task 9.9 Daemons and session processes (2026-09-22)

Stages 1–2 were the research routine's (2026-09-20). This session retried the blocked sources, took stage 3's decisions D1–D10, and drafted the campaign method. All on `jioh/dataset-rebuild`; last commit `92c5508`.

## Next session: build the session tooling, in a worktree

Work in a git worktree off `jioh/dataset-rebuild`, not in the main checkout: the main checkout holds someone else's uncommitted `dataset/` edits (`sources.yaml`, four coreset timelines, `wlc/compiler.py`, `wlc/deriver.py`, `tests/test_canonical.py`, `tests/test_lint.py`, `tests/fixtures/fx-mixed.timeline.yaml`) — never stage, test against or push them.

Build what `_dev/research/jioh/task-9.9-daemons-session/campaign/method.md` names, following 9.8's `desktop` family as the model:
- `dataset/tools/meas/session/` — `run.sh` (machine gate first; install `ubuntu-desktop-minimal`; seatless PAM login; `gnome-session --session=ubuntu` under the user manager with `XDG_SESSION_TYPE=wayland`; user drop-in on `org.gnome.Shell@wayland.service` adding `--headless --virtual-monitor 1920x1080@60`; pinning per method §2.5; census per §2.4; `perf sched record -k CLOCK_MONOTONIC -a`; modes `dry`, `probe`, `full`), `analyze.py` (instances by pid from the census; components per instance × thread comm; 95 % coverage cut and residual; 10 s slice profile for the probe), `pool.py` (`--cpu-model "EPYC 7763"`, `stability.py` on the method §6 list), tests.
- `.github/workflows/meas-session.yml`, trigger `.github/campaign-session.json`, loop family `session` in `dataset/tools/meas/loop/common.py`.
Then the dry run (verifies the session comes up as §2 states) and the long-phase probe — each pushes a trigger and starts runs; confirm with 인지오 before pushing.

## Decisions (changelog `_dev/research/jioh/task-9.9-daemons-session/changelog.md`)

- D1 `system-daemon` splits: system services vs session processes. D2 one archetype per session program.
- D3 compositor-and-shell = GNOME Shell 46.0 / Mutter 46.2 as Ubuntu 24.04 ships. D4 audio server = the PipeWire stack whole (pipewire, wireplumber, pipewire-pulse), one component per thread kind.
- D5 system side = one archetype per bound program, `systemd` and `dbus-daemon`. D6 `dbus-daemon` = system + session bus. D7 `systemd` = pid 1 + user manager. Components per instance.
- D8 one new pinned campaign of an Ubuntu desktop session on the runner (campaign workflow, EPYC 7763). D9 terminal idle state: nobody present past `idle-delay`, shield up and locked, blanked; settle confirmed by a long-phase probe. D10 only the four entries' processes on the measured CPU.

## Held and open

- **Held: a display-server entry for the idle desktop.** A GNOME 46 Wayland session runs Xwayland only on demand (S2-28), but whether a default Ubuntu login starts an X11 client, and the share of X11 sessions, are unverified. Settled by the campaign census (Xwayland present or not) and a verified source on session-type share. With it: whether gaming sessions need an Xwayland entry (S3-25 shows Xwayland active under Proton games).
- Method §9, settled by the dry run and the probe: session comes up as written (`SessionIsActive` for a seatless login is the key check), shield and blank reached headless, `session-settle` and `steady` lengths.
- At fold-in: entry ids (whether `system-daemon` survives), `meas-ci` registry relabel (scope card item 17), `category_source`, `validation_stats`, the header form (item 18); `meas-gui.yml` retires.

## Sources this session added

Search logs, all under `task-9.9-daemons-session/search/`: S3-25 (sched-ext/scx #296 `scx_lavd` logs), S3-26 (mutter #4622 sysprof captures), S3-27 (KDE 486214 `perf.data`), S3-28 (Gentoo topic 1152974, not 1153076), S3-29 (Columbia PowerTOP report — the only per-service idle table), S4-17, S1 §4 (Morari, Akkan, Wong dropped), S2-28…S2-32 (Xwayland policy, `user@.service`, gsd-power blank/suspend with Ubuntu's AC override, lock default and logind's seatless rule, Mutter's power-save path). Local copies in `sources/retry-2026-09-22/` (gitignored); `syscap.py` there parses sysprof captures.
