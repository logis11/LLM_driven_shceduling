# Task 9.3 — Measurement tools fixed

Fix the meas-ci measurement tools and preserve the `meas-ci:names:2` run. Parent: `_dev/TODO.md`, (jioh, 9.3); phase spec `_dev/docs/spec/jioh/phase-9-workload-dataset-rebuild.md`, which leaves how the measurement tools are fixed to this task. The defects are those of the 2026-09-13 measurement audit, `_dev/research/jioh/2026-09-13-verification/meas-report.md`.

## Scope

- The instruments `proc_sampler.py` and `verify_names.py` and the analyzer `analyze.py` in `dataset/tools/meas/`.
- The `meas-ci:names:2` run (Actions run 34466009254), whose artifacts expire on 2026-12-09.
- One re-analysis of release `meas-ci-2026-08-28`.

## Locked decisions

### 1. names:2 in the release

The names:2 artifacts are added as an asset to release `meas-ci-2026-08-28`. In the same edit the release title and notes are corrected: the summary comes from cli:3, not cli:1; names:2 is added; cli:1 is cited by `system-daemon`. Publishing is confirmed with 인지오 first.

### 2. Defects fixed

Where a tool reports a wrong number for what actually ran, it is fixed:

- `proc_sampler.py` — voluntary context switches counted for the main thread only (audit #3).
- `verify_names.py` — the verification level logic and the 15-character comm truncation (#14).
- `analyze.py` — the compiler-family unit taken as the compiler child (#1), the Chromium renderer set (#5), zero values dropped by the fit (#9), the `dispatch_overhead` divisor (#12).

### 3. Defects handed to the research slices

Quantities no instrument measures — I/O wait (#2), per-wake distributions (#8), network throughput (#11) — and workflow setups that do not produce the behaviour their phase names — no Element renderer (#4), tabs not loaded (#6), tracker not indexing (#7), `tar -cf /dev/null` reading no contents (#16) — are not fixed here. They are recorded as known limitations of the current tools.

### 4. One re-analysis, no new CI runs

The fixed analyzer is run once on the raw data of release `meas-ci-2026-08-28`. No new measurement runs.

### 5. Location of the re-analysis

The output lives in `_dev/research/jioh/<date>-meas-reanalysis/`: the corrected summary and a comparison against the current `dataset/meas/summary.json` showing which values moved and by how much. `dataset/` is unchanged.

### 6. Done check

Every fixed number agrees with the audit's independent computation where one exists; every field no fix touches is byte-identical to the current `dataset/meas/summary.json`. The `proc_sampler.py` and `verify_names.py` fixes each pass a test on a constructed case.

### 7. Limitations recorded

The re-analysis folder's index lists each handed-off limitation with the parameters it affects and the research slice that owns it.
