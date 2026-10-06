# Task 9.10 — `video-editor`'s idle phase past Kdenlive's launch work: method (2026-10-05)

The re-measurement of `video-editor`'s idle values past the work Kdenlive does after launch, and the re-trace of its launch phase to the new settle (changelog D146), run on GitHub-hosted runners under `../../../measurement-campaign-workflow.md`. Amended only by a dated entry in §6. Tooling: `dataset/tools/meas/campaign/run.sh` mode `idle`, workflow `.github/workflows/meas-interactive.yml`, trigger `.github/campaign.json`, loop family `interactive`, pool `campaign/pool.py`, fold-in `campaign/fold_in.py --only video-editor --idle-from`; the launch through `dataset/tools/meas/desktop/run.sh`'s `launch-kdenlive` subject, `meas-desktop.yml`, `campaign-desktop.json`, loop family `desktop`, `desktop/launch_fold_in.py`.

## 1. The idle repeats

- **Machine.** The AMD EPYC 7763 only (`machine_gate.sh`); a gated job is not a repeat.
- **Tag.** `meas-ci:interactive:2026-10-05`, the first batch's launch date.
- **Job.** 9.5's `kdenlive` setup unchanged — Kdenlive 23.08.5 from Ubuntu 24.04's archive, 9.5's project, the application's tree pinned to one CPU under Xvfb (9.5 method §1–§4) — run in mode `idle`: the window, the settle and the idle phase, nothing after it. Artifact `meas-interactive-kdenlive-r<k>-idle`.
- **Settle and phase** (D146): 240 s from the window, then 180 s, `perf sched record` over the phase (`settle_for`, `idle_for`).
- **Repeat.** Identical work, so an added repeat is the next index.
- **The list.** Every value the fold-in carries from the idle phase: each component's wake rate, gap mean and run mean, the residual's, each table by its mean as the table carries it (the stability rule).
- **First batch.** Repeats 1–5, the workflow's floor; then repeats added under the rule.
- **Validity** (the workflow's step 4): the gate open on the EPYC 7763; the idle phase present, its trace stopped cleanly; the screenshot after the settle showing the project open; the idle phase's 10 s slice profile flat from its start.

## 2. The launch re-trace

- **Tag.** `meas-ci:desktop:2026-10-05`.
- **Job.** The launch campaign's `launch-kdenlive` subject unchanged but for its settle (`campaign/launch/method.md` §1–§5; D132, D133, D135): the first launch unmeasured and quit by the program's own command, the second traced from its exec to the end of its 240 s settle (`desktop/launch.sh`, `ln_settle_for`).
- **Repeats.** 1–5 (D139's count), every landing pooled; validity as the launch campaign's §1.

## 3. Fold-in

- **`video-editor`.** `fold_in.py --only video-editor`, its driven and operation values from 9.5's 20 repeats (`task-9.5-interactive-typing/campaign/results-same-machine/pool-kdenlive.json`, `meas-ci:interactive:2026-09-18`) and its idle phase from this campaign's pool (`--idle-from kdenlive=… --idle-tag kdenlive=meas-ci:interactive:2026-10-05`), the untraced control's reading kept (`--control`), spliced by `campaign/splice.py`, which keeps the entry's `launch` param. The same command without `--idle-from` reproduces the library's `video-editor` byte for byte.
- **The launch stream.** `launch_fold_in.py` over this campaign's landings alone, `--source meas-ci:desktop:2026-10-05`: it writes `dataset/launch/launch-video-editor.json.gz` and rewrites that entry's `launch` param; the other nine streams and params are untouched.

## 4. Rebinding

The dataset recompiled. Each file whose length rests on a job ending under every policy beside Kdenlive (D78's arithmetic) is read again: `c1-render`, `c1-backup`, `c1-transcode`, `c3-creation`, `c2-p3a` and `c2-p3b`.

## 5. Records

The pooled `results/pool-kdenlive.json` and `results/results.md`; the launch landings' pool and reading in `results/`; the record's entry in `../../../measurement-campaign-record.md`. The raw records released on 인지오's go-ahead.

## 6. Amendments

- 2026-10-05, the method written (D146, D147).
- 2026-10-05, the campaigns. The idle repeats (runs #664–#674; `meas-ci:interactive:2026-10-05`): repeats 1–16, each landing once, all valid; 16 jobs stopped at the gate; the rule holds at 16. The launch re-trace (runs #100–#101; `meas-ci:desktop:2026-10-05`): repeats 1–5, all valid; 1 job stopped at the gate. Folded in at commit `626c27a6`; released as `meas-ci-interactive-2026-10-05` and `meas-ci-desktop-2026-10-05` (D151).
