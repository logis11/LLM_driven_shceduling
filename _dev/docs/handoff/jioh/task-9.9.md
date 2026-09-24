# Handoff — task 9.9 Daemons and session processes (2026-09-24)

The measurement campaign is **closed**: the stability rule holds over 24 repeats, every one of the 18 carried values inside the 5 % tolerance, the widest half-width 3.7 %. Tag `meas-ci:session:2026-09-24`. Work is on `jioh/dataset-rebuild` (worktree `../LLM_driven_shceduling-9.9`, branch `jioh/phase-9/9-session-tooling`, merged up to date). Pooled `results.md` and `pooled.json` are in `_dev/research/jioh/task-9.9-daemons-session/campaign/results/`; every job's model is in `campaign/machine-draws.md`.

## Next session: the raw-record release, then the fold-in

- **The release is unasked.** Method §8 and the campaign workflow's loop step 7 put the raw records of a campaign in one release and say publishing outward is asked before it is done. 인지오 has not been asked yet — ask first.
- **The fold-in** then carries the open items the campaign did not settle: the entry ids and whether `system-daemon` survives, the `meas-ci` registry relabel (scope-card item 17), `category_source`, `validation_stats`, the header form (item 18), and `meas-gui.yml` retiring once these four entries carry their own values.
- Each entry's row still has to go into `../../measurement-campaign-record.md` — repeats, the values, the widest half-width, what stopped it, jobs and gated draws (loop step 7). Not yet written.

## The measured values (24 repeats, AMD EPYC 7763, kernel 6.17.0-1022-azure)

| entry | component | wakes/s | gap mean | run mean | widest |
|---|---|---|---|---|---|
| GNOME Shell | `JS Helper` | 0.3025 | 13.05 s | 0.0137 ms | ±1.5 % |
| | `gmain` | 0.2499 | 4.00 s | 0.0497 ms | ±2.2 % |
| | `gnome-shell` | 0.0348 | 28.75 s | 5.7007 ms | ±2.8 % |
| PipeWire stack | `wireplumber/gmain` | 0.2132 | 4.68 s | 0.0383 ms | ±3.7 % |
| `systemd` | `pid1/systemd` | 0.1792 | 5.57 s | 0.2460 ms | ±3.5 % |
| `dbus-daemon` | `system-bus/dbus-daemon` | 0.1368 | 7.33 s | 0.2784 ms | ±3.0 % |

Coverage 99.9–100 % per entry. Beside them the cron event (D23), present in 4 of the 24 repeats: `systemd` 201 rows, `dbus-daemon` 245, PipeWire 37, GNOME Shell 12.

**For the fold-in's scope text.** `pipewire` and `pipewire-pulse` never woke in an 1800 s phase — the entry carries `wireplumber` alone. The user manager and GNOME Shell's `gnome-s:disk$0` woke only in the four repeats that met a cron session, so both are reported sporadic and neither is carried. The session bus is under the coverage cut.

## Decisions this session (changelog `_dev/research/jioh/task-9.9-daemons-session/changelog.md`)

- **D19** the probe's polls stop at the steady edge — the 2026-09-22 probe's own 10 s polls dominated its signal (`systemd` 15.06 /s polled against 0.17 unpolled), so D18's 900 s steady length was withdrawn.
- **D20** the foreign-work gate is a stated bound, not an absolute: both managers' `init.scope` are on the measured CPU because both managers are entries, so every process the system starts is forked there and no window of 600 s or more is free of it.
- **D21** the system bus was never on the measured CPU — `Slice=` applies when a unit starts and that bus had run since boot. It is restarted into `meas.slice` during the install, the placement is read from the processes at the pin and at the steady edge, and the 2026-09-23 dry jobs and probes were superseded by the campaign workflow's loop step 6.
- **D22** `steady` 1800 s and the bound 2 × 10⁻⁴, from the three probes taken under the corrected placement.
- **D23** a cron job's session is an event of the phase in 9.5 D64's form, taken by cause with a ±2 s window, not by a run floor.
- **D24** the pool reads each component's exact wake count; `per_thread`'s two-decimal rounding was a ±15 % step at this slice's rates.
- **D25** 인지오 took the repeats as a batch to the pool's projection (9.7 D26's form).

## What the tooling gained

`session/size_steady.py` (the steady length from the probes, within-run and between-run, with the foreign share per run), `census.py placed` (the placement read from the processes), `analyze.py --from-s`/`from_mono` (a phase read from a cut), the cron event in `analyze.py` and `pool.py`, the exact wake count in `pool.py`, the placement and bound records in the loop's validity arm, and `dry` no longer poolable. 13 tests in `dataset/tools/tests/test_meas_session.py`; the full tool suite passed at 200 tests when last run whole.

## Held

- The display-server entry for the idle desktop: no display server at idle in any probe or census; the share of X11 sessions is unverified.
- `docs/references.md` carries no entry for the 9.9 source readings; S2-33 and S2-34 live in the slice's search log, and whether either becomes a citation is a fold-in question.
- That systemd names a pre-exec child `(name)` is read from the observed comms and their timing, not from systemd's source — the citation to add if that ground is carried further (D20).
