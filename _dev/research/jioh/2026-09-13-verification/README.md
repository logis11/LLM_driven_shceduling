# 2026-09-13 verification

Verification of the workload dataset and what it feeds, at repo commit `e3d3c9a`. Spec: `_dev/docs/spec/jioh/task-9.1-verification-records.md`.

## Committed records

### Claim inventory and reader inputs

- `claims.md` — every claim the repository takes from an external source: Part 1 by source, Part 2 numeric values with their tags, Part 3 scenario rows.
- `topics.md` — the neutral topics (`C-<source>-<n>`) each reader answered, without the repository's wording.
- `bib.md` — the bibliographic entries given to the readers.
- `inputs/R01–R11` — what each reader received: the entries and topics for its sources.

### Independent reads

Each read lists the copies it used (URL or commit, version, date, local path), then the verbatim passages with locators and a reading per topic.

| Read | Sources |
|---|---|
| `reads/R01-interbench-rtapp-benchtools.md` | interbench, rt-app, hackbench, schbench, stress-ng, kernel build |
| `reads/R02-lavd.md` | lavd-ossna24, corbet-lwn24, scx |
| `reads/R03-build-papers.md` | ocallahan-atc17, coetzee-arxiv12, schedcp-mlsys25 |
| `reads/R04-cpsmark.md` | cpsmark-tbench23 |
| `reads/R05-vendor-benchmarks.md` | pcmark10, sysmark30, sysmark25, procyon |
| `reads/R06-ananicy.md` | ananicy-rules, ananicy (working data and scripts in `r06/`) |
| `reads/R07-gamemode-steam-dkms.md` | gamemode-docs, steam-downloads, dkms-man, dkms-debian |
| `reads/R08-typing.md` | dhakal-chi18, roeser-rw24 |
| `reads/R09-tabs.md` | dubroy-chi10, chang-chi21, mozilla-testpilot10, singervine-slate10, tabshared |
| `reads/R10-task-switching.md` | zhang-chb15, gonzalez-chi04, mark-chi05, mark-chi08, mark-chi14, czerwinski-chi04, mark-gallup06, swell-icmi14 |
| `reads/R11-focal-plain.md` | focal-arxiv26, videogui-arxiv24, the unattributed plain-text claims C-plain-1–9 (part files in `reads/R11-parts/`) |

### Comparisons

Reads against the repository's claims, per location, with a summary table at the top of each: SUPPORTED / WORDING-FIX / MISATTRIBUTED / CONTRADICTED / NOT IN SOURCE / OURS-UNDER-SOURCE-TAG / UNVERIFIABLE.

| Comparison | Reads |
|---|---|
| `compare/K1.md` | R01, R03 |
| `compare/K2.md` | R02, R04 |
| `compare/K3.md` | R06, R07 |
| `compare/K4.md` | R08, R09, R10 (Crossref records and a blocked ACM page capture in `compare/K4-crossref/`) |
| `compare/K5.md` | R05, R11 |

Known input errors, corrected in the comparisons: R11 answered C-plain-9 for the wrong tools (K5 re-judges it); R01's "premise" verdict on C-hackbench-2 (K1 corrects it); one C-plain-7 line misplaced in `claims.md` (K5 notes it).

### Measurement audit

- `meas-report.md` — reproduction of `dataset/meas/summary.json` from release `meas-ci-2026-08-28`, the method audit, and each `meas-ci` param classed M / D / C / X, with the X items at the top.
- `meas/` — the audit's scripts and their outputs (`out_cli3.json`, `out_cli1.json`, `*.txt`); the file list is in the report's "Working files" section.
- `meas/names2/` — the `meas-ci:names:2` artifacts (`names-<distro>.json` and `spec.json` for arch, fedora, ubuntu) from Actions run 34466009254, which are in no release.

### Compiled-number audit

- `compiled-numbers-report.md` — every compiled-number statement in the prior table, pair review, scoring, guard and RQ0 gate specs, memos and specs, checked against the build: HOLDS / STALE / WRONG / UNCHECKABLE, grouped by the decision each touches.
- `analyze.py`, `extra.py`, `deliverable.py`, `pairs.py`, `mlfq_media.py`, `misc_checks.py`, `dump.py` — its scripts; `analysis.txt`, `single.txt`, `single_f.txt`, `native_f.txt` — their outputs. The scripts read the repository at its absolute path on the home machine.
- `r01_xsim.py`, `xsim.py` — ideal-machine models of interbench's `periodic_schedule()` + `emulate_x()`; R01 cites `r01_xsim.py`.
- `extract_learn.py` — HTML text extraction helper.

## Local only (gitignored)

| Path | Origin |
|---|---|
| `sources/` | The primary copies the reads and comparisons opened; each read's "Copies used" table gives URL or commit, version, retrieval date and local path. |
| `meas/release/` | The four zips of GitHub release `meas-ci-2026-08-28`: `meas-cli3.zip` (cli:3), `meas-gui.zip` (gui:2), `meas-names.zip` (names:1), `meas-cli.zip` (cli:1). |
| `meas/cli3/`, `meas/gui/`, `meas/names/`, `meas/cli1/` | Extracted from those zips. |
| `meas/run_cli3/`, `meas/run_cli1/` | Symlinks pairing `cli3` or `cli1` with `gui`, the layout the rerun used. |
| `meas/array.c`, `meas/tar_create.c`, `meas/tar_buffer.c`, `meas/tar_NEWS` | Linux v6.17 `fs/proc/array.c`; GNU tar `src/create.c` and `NEWS`; `tar_buffer.c` is a cgit page that returned no repository. |
