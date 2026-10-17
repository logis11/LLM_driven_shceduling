# Task 9.10 — `renderer-hidden` past its page thread's settling: method (2026-10-05)

The re-measurement of `renderer-hidden` past the settling of its page thread, and the re-trace of its launch phase to the new grace-settle (changelog D152), run on GitHub-hosted runners under `../../../measurement-campaign-workflow.md`. Amended only by a dated entry in §5. Tooling: `dataset/tools/meas/desktop/` (`run.sh`'s `chrome-hidden` and `launch-chrome-hidden` subjects, `launch.sh`, `analyze.py`, `pool.py`, `fold_in.py`, `launch_fold_in.py`), workflow `.github/workflows/meas-desktop.yml`, trigger `.github/campaign-desktop.json`, loop family `desktop`.

## 1. Runs

- **Machine.** The AMD EPYC 7763 only (`machine_gate.sh`); a gated job is not a repeat.
- **Tag.** `meas-ci:desktop:2026-10-05b`, lettered after the launch re-trace of D146.
- **The steady repeats.** 9.8's `chrome-hidden` subject (its method §2–§3: one window, a foreground control tab and 12 background tabs at 12 loopback origins of one local page, the subject pinned to one CPU under Xvfb), unchanged but for the grace-settle: 20 s after launch, 1,030 s of grace-settle, a 600 s steady phase (`GRACE_S`, D152). Mode `full`; artifact `meas-desktop-chrome-hidden-r<k>-full`. Identical work, so an added repeat is the next index.
- **The list.** Every value `renderer-hidden` carries: each component's wake rate, gap mean and run mean, the residual's, each table by its mean as the table carries it (the stability rule). A value of a class 9.8 decided — run means following the runner's speed (9.8 D17, D18), the sparse residual (D26, D27), a rare event within a run (D33) — takes 9.8's treatment, recorded as it is read.
- **First batch.** Repeats 1–5, then repeats added under the rule.
- **Validity**: the workflow's step 4 and 9.8's checks (method §7): the gate open on the EPYC 7763; the renderer gate, 13 renderers or more; the page server answering; the throttling check; one origin count across repeats.
- **The launch re-trace.** `launch-chrome-hidden`, repeats 1–5, its trace from the exec to the end of the 1,030 s grace (D133; `LN_GRACE`); validity as `../launch/method.md` §1.

## 2. Fold-in

`desktop/fold_in.py` writes `renderer-hidden` from this campaign's pool, its scope's statements read on this campaign — the build, the exceptions, the spreads within one run on D149's probe past the new settle and between the repeats; `splice.py` keeps the entry's `launch` param. `launch_fold_in.py` over this campaign's launch landings alone, `--source meas-ci:desktop:2026-10-05b`, rewrites `launch-renderer-hidden`.

## 3. Rebinding

The dataset recompiled; the files that carry `renderer-hidden` — the ten Chrome files of D131 — read again for their demand.

## 4. Records

The pooled records and `results/results.md` beside this page; the record's entry in `../../../measurement-campaign-record.md`; the raw records released as D151's.

## 5. Amendments

- 2026-10-05, the method written (D152).
- 2026-10-05, the campaign (runs #105–#107; `meas-ci:desktop:2026-10-05b`). `chrome-hidden` 1–5 and `launch-chrome-hidden` 1–5, each landing once on the AMD EPYC 7763 under Google Chrome 154.0.8037.57, all valid; 6 jobs stopped at the gate. Launch repeats 2 and 5 re-analysed, the tabs' renderers the lowest client ids (D155); the rule holds at 5 under 9.8's per-value treatments; folded with the build split from `web-browser` stated (D156); released as `meas-ci-desktop-2026-10-05b` (D157).
