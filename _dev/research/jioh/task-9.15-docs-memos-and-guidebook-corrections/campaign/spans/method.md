# Task 9.15 — `video-editor`'s idle state over `c3-creation`'s span: probe method (2026-10-17)

One long-phase probe of `video-editor`'s idle state, at least the span `c3-creation` holds it past its launch phase, read on 9.10 D143's standard (인지오's answer (a) to K06's M6, `../../work-list.md`, 2026-10-17). It follows 9.10's span probes (`../../../task-9.10-scenarios-timelines/campaign/spans/method.md`) and runs on GitHub-hosted runners under `../../../measurement-campaign-workflow.md`'s machine rule. A probe is never a repeat, is pooled into nothing and changes no value (9.10 D143). Amended only by a dated entry in §5. Tooling unchanged: `dataset/tools/meas/campaign/run.sh` mode `probe`, workflow `.github/workflows/meas-long-probe.yml`, trigger `.github/campaign-long-probe.json`, loop family `long-probe`; the reading `dataset/tools/meas/campaign/span_probe.py`.

## 1. The probe

- **Span.** `c3-creation` holds `video-editor` idle from 360.6 s, the end of its 240.6 s launch replay from the 120 s arrival, to its 3,212 s depart: 2,851 s past the 240 s settle (9.10 D146), 3,061 s past a 30 s settle.
- **Machine.** The AMD EPYC 7763 only; `machine_gate.sh` stops a job that drew another model before any install or measurement, and the same index is relaunched.
- **Index.** `kdenlive` 13 of the `long-probe` family, the next after 9.10's 10 (idle) and 11 and 12 (driven).
- **Job.** 9.5's `kdenlive` setup unchanged — Kdenlive from Ubuntu 24.04's archive, 9.5's project, the application's tree pinned to one CPU under Xvfb — in mode `probe`: the window, the 30 s settle, then one idle phase of 3,100 s with no input, and nothing after it, as `kdenlive` 10. Artifact `meas-long-probe-kdenlive-r13-probe`.
- **Length.** 3,100 s past the 30 s settle: the 3,061 s rounded up, as 9.10 D143 set the first probes' lengths (2,976 s to 3,000 s, 1,429 s to 1,500 s). It holds 2,890 s past the 240 s settle.
- **No dry run**: mode `probe` is the mode `kdenlive` 10 ran.

## 2. The reading

- **The slice profile past the 240 s settle.** `span_probe.py`'s `phase_slices` over the idle phase at 10 s, its first 21 slices — the 210 s between the probe's 30 s settle and the 240 s settle — left out, as 9.10 D146 read `kdenlive` 10 over 2,790 s past that settle.
- **9.10 D143's standard** (`span_probe.py`'s `level_reading`) on that profile: the level over the span — 2,851 s in whole slices, 286 slices, 2,860 s — CPU ms/s and wakes/s, against the carried 180 s phase (9.10 D146) at the placement every repeat takes, the first 180 s past the settle. A difference over 5 % in either is a phase that does not hold over the span. The worst placement of a 180 s window inside the span, stepped by 10 s, is reported beside it, and with it 9.10 D146's own standard (9.5 D53): the placement and the worst placement both within 5 %.
- **Check.** The same reading on `kdenlive` 10 over its 2,790 s reproduces 9.10 D146's 180 s figures (CPU −1.1 % and +4.6 %; wakes −0.7 % and +3.9 %).
- **Validity**, before the probe is read: the gate open on the EPYC 7763; `settle_s` 30 and `idle_s` 3,100 in the report; the idle phase present, its trace stopped cleanly; the screenshots after the settle and after the phase showing Kdenlive's window holding the project; the build, Kdenlive 23.08.5 as every carried campaign's.

## 3. What follows

A probe changes no value (9.10 D143). If the 180 s phase does not hold over the span, 9.10 D146's phase length reopens.

## 4. Records

The run id, the artifact and the reading go into `../../logs/M6-reprobe.md`; `span_probe.py`'s output beside this page as `results/video-editor-idle.level.json`. The raw records are released as `meas-ci-probes-2026-10-17`, in `meas-ci-probes-2026-10-05`'s form: each artifact as `<artifact>-<run id>.zip`, the gated jobs' reports in `gated-reports.zip`. A probe belongs to no campaign tag, so `dataset/meas-releases.yaml` does not map it.

## 5. Amendments

- 2026-10-17, the method written.
