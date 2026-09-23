# Handoff — task 9.9 Daemons and session processes (2026-09-23)

Stage 3's decisions D1–D10 were the 2026-09-22 session's. This one built the session tooling, took D11–D18 on what the runner forced, ran the dry runs and the long-phase probe. Work is on `jioh/dataset-rebuild` (worktree `../LLM_driven_shceduling-9.9`, branch `jioh/phase-9/9-session-tooling`, merged up to date); the main checkout still holds someone else's uncommitted `dataset/` edits — never stage, test against or push them.

## Next session: launch the first batch

Trigger `.github/campaign-session.json`: `mode` `full`, `cpu_model` `EPYC 7763`, `repeats` `{"session": [1..5]}` — the method's first batch of five, ~30 min a job. Then the campaign loop as 9.5–9.8 ran it: `dataset/tools/meas/loop/` (family `session`), gated indices relaunched together, repeats added one at a time until every value on the method §6 list holds, `pool_runs.py session/session` to pool.

**Decide first (from the dry runs of 2026-09-23, run 35814510341):** the probe's own 10 s state polls ran inside its recording, and they dominate what it measured — at idle the entries wake 0.1–0.9 /s in a dry run's steady phase against 15.06, 4.25, 3.67 and 2.17 /s in the probe. D18's steady edge (420 s) rests on the shield and blank timings, which the polls read directly and which hold; its 900 s steady length rests on window spreads of the poll-dominated signal and does not. Either re-run the probe with the polls off during the recording (~4 h), or keep 900 s and let the stability rule add repeats.

## Decisions this session (changelog `_dev/research/jioh/task-9.9-daemons-session/changelog.md`)

- D11 the login, D12 the sweep and the zero gate, D13 the phases and checks, D14 the cpuset delegation and kernel threads, D15 the pinned units' other processes, D16 GDM's automatic login (correcting D11), D17 the placement as a slice default, D18 the phase lengths.
- Sources added: S2-33 (GDM 46.2 stops its login screen once a user session takes over), S2-34 (GNOME Shell 46.0 locks only when a display manager answers on the system bus).

## What the runner forced, and what verified it

- **Runner losses.** The first five dry jobs lost their runner with no log, in the install's last service starts and `needrestart` pass. The install now blocks both, and the units `graphical.target` wants start one at a time afterwards (D16). Every job since completed.
- **No shield without a display manager.** With GDM masked the session never locked or blanked (S2-34). GDM's automatic login reaches the state; a stand-in on the bus does not (run 35795764108). The session now holds seat0 and a virtual terminal, so D9's seatless ground is no longer needed.
- **The runner image's `XDG_*` lines** went to every login and sent the session's settings to `/home/runner`; they are removed from `/etc/environment` (D16).
- **Verified clean** (run 35814510341, both jobs): entries in `meas.slice`, other slices on the harness CPUs, no pin failures, nothing left in the pinned units, the edge check passing, and zero foreign user-space work on the measured CPU.

## Held and open

- **Held: a display-server entry for the idle desktop.** The probe and every census found no display server at idle; Xwayland ran only during login and start-up. The share of X11 sessions is still unverified.
- At fold-in: entry ids (whether `system-daemon` survives), `meas-ci` registry relabel (scope card item 17), `category_source`, `validation_stats`, the header form (item 18); `meas-gui.yml` retires.
- `docs/references.md` carries no entry for the 9.9 source-code readings; S2-33 and S2-34 live in the slice's search log, and whether either becomes a citation is a fold-in question.

## Tooling (all on `jioh/dataset-rebuild`)

`dataset/tools/meas/session/` — `run.sh` (modes `dry`, `probe`, `full`; stage checkpoints with a dry-only stop point), `census.py`, `analyze.py`, `pool.py`, `dm_stub.py` (the rejected stand-in, kept as the `stub` login mode); `.github/workflows/meas-session.yml` (partial upload per stage, so a lost runner still leaves a trace), trigger `.github/campaign-session.json`, loop family `session`, validity arm in `loop/pool_runs.py`, 9 tests in `dataset/tools/tests/test_meas_session.py`.
