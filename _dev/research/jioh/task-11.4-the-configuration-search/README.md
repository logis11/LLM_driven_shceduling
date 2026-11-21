# The configuration search (11.4)

The record of sub-task 11.4 (`_dev/docs/spec/jioh/task-11.4-the-configuration-search.md`): the configuration search the RQ0 gate spec's statement `failure-procedure` names, run by the search tool (`harness/tools/search.py`) on the committed search spec (`harness/experiments/rq0-config-search.yaml`), its report committed beside the spec (`harness/experiments/rq0-config-search/`). The paths in the files are relative to the repository root; each script runs from there.

## Before the search

| file | what it holds |
|---|---|
| `picks.py`, `picks.json` | decisions 1 and 2 read again from the corrected runs' scores — 11.2's rerun on the fixed simulator for sixteen judging files, 11.3's runs on the current programs for `c2-p1a`, `c1-ml-train` and `c7-ml-train`: per judging file the gap, whether it meets g, its terms against the floor, the oracle's improvement over fixed as a fraction of fixed's value weighted over its terms; the three picks by the statement's rule and the seven files with no headroom on every term |
| `boost_test.py`, `boost-test.json` | the evidence behind the search spec's `checks.restarted_boost`: on `c1-compile` and `c1-ml-train`, outside the search, whose oracle applies its row again at 2 s, the boot default applied where the oracle applies its row, run on the pinned simulator and read line by line against the corrected fixed run — strict, and with the `x_mlfq_boost` line at the re-applied entry's instant set aside |

**The boost test** (2026-11-21): strict, both files differ from the corrected fixed run by one line — `c1-compile` 848,612 lines against 848,613, `c1-ml-train` 773,663 against 773,664, the first difference the `x_mlfq_boost` line at 2,000,000 µs; with that line set aside, both equal. A same-algorithm MLFQ entry restarts the boost timer (`docs/harness/metrics.md` §11 item 9), so the boost due at the re-applied entry's instant is voided and the next falls one boost interval later, the fixed run's phase. 인지오 decided on 2026-11-21 to set that line aside in decision 10's check of the boot default's point.

## The search

| file | what it holds |
|---|---|
| `run/search.log` | the search tool's progress lines, one per run, the twenty checks and the route |
| `run/run-times.csv` | each run's seconds, records built or from the results cache, peak RSS and bytes |
| `run/checks.json` | decision 10's twenty checks as the tool wrote them before reading the grid |
| `hash_manifest.py` | every run's trace hash and records hash, uncompressed, to `harness/experiments/rq0-config-search/runs.sha256.csv` — the same columns as 10.5's manifest of the RQ0 run, the point in place of the table |
| `read_search.py`, `summary.json` | the points read for the record and the memo: per file, the row's quantity, the best read point per algorithm and per cap, how many read points are above the row and how many beat it by the floor on a term, the ten best points and each term's range; each quantity computed again from the points file's values by the tool's own rule, the tie rule of the search spec applied |

**The run** (2026-11-21 10:20:08 to 15:41:35, 5 h 21 min), on `79608bff`, the search spec's SHA-256 `a849e4dc453b…`: the home M1 Pro, a machine configuration of its own — `simulator@841dc81131cb`, `daemon@62c71f0d2de0`, the core set's build `dataset/build/coreset-single`, an execution cache of its own (`runs/rq0-config-search.cache`), `workers` 4, `heavy_workers` 3, `heavy_mb` 50. The twenty check runs first, all reproduced by 10:22; then the other 4,680. 4,700 runs, every one built, none from the results cache; no failed run. The runs' seconds summed, 71,112 s: `c1-transcode` 9.37 h, `c7-transcode` 4.98 h, `c7-compile` 2.55 h, `c7-ml-train` 1.77 h, the other six 1.09 h together — the three picks 14.68 h and the seven files 5.08 h, against the spec's estimate of about 12 and 3.5. Peak RSS 2,960 MB.

**The disk**: `runs/rq0-config-search` 31 GB, its execution cache 9.8 GB; 110 GB free after the search.

**The summary's check against the report**: on every file the best point `read_search.py` ranks first is the report's.
