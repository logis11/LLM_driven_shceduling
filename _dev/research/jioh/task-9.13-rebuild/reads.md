# Task 9.13 — reads

Facts established for the rebuild with no value changed, each with its method and the copy read. All on branch `jioh/dataset-rebuild` at `27a80abb` (2026-10-09), compiled in memory with the dataset's own compiler (`dataset/tools/wlc/`) under Python 3.12.4 on an Apple M1 Pro; the scan scripts are in `scans/` and take the repository root as their one argument.

## R1 — `network-bulk` is gone (2026-10-09)

9.7 D30's condition for the rebuild: `network-bulk` leaves the library before 9.13. A search for the id over `dataset/archetypes.yaml` and `dataset/timelines/` finds no occurrence. Condition met; nothing to do.

## R2 — every TIMER-carrying task is TIMER-first (2026-10-09)

9.11 D11 and D33 hand 9.13 a lint: a program that contains a TIMER anywhere has a TIMER as its first executed instruction, a LOOP head counting when its body begins with TIMER. `scans/timer_scan.py` compiles every timeline in the single-lane mode, walks each top-level program and each spawn-table program, and reports the first executed instruction (descending LOOP heads) of every program that contains a TIMER.

| Quantity | Value |
|---|---|
| Arrive events | 270 |
| Spawn-table tasks | 79,772 |
| Tasks carrying a TIMER | 22 |
| — opening with a LOOP whose body begins with TIMER | 7 (`Troy.exe`, the gaming chain heads) |
| — opening with TIMER literally | 15 (`mpv` 6, `chrome` 3, `tracker-miner-f`, `baloo_file`, `audio-stream-he`, `video-playback-`, `xkrr`, `qzvd`, 1 each) |
| First executed instruction not TIMER | 0 |

The lint guards against regressions; the current set passes it.

## R3 — `module-build-orchestrator`'s tables hold no `apt-check` or `dpkg` work (2026-10-09)

9.11 D20 asked whether the entry's tables hold the nice-19 `apt-check` and `dpkg` work of a DKMS landing, 0.85 % of landing 10's CPU. Settled from the pooling code, 9.10's changelog and the committed pooled results, without the raw release.

- **The job's definition.** 9.10 changelog D50 (`_dev/research/jioh/task-9.10-scenarios-timelines/changelog.md:957`): "The job is every process rooted at a `dkms_autoinstaller` run the kernel install causes." and "The rest of the stage is recorded and reported, not carried: `unattended-upgrade`, dpkg, the initramfs rebuild and `xdg-desktop-portal`…". The entry's scope (`dataset/archetypes.yaml:1105`): "The job is every process under the two DKMS kernel hooks of that stage (D50)".
- **The filter in code.** `dataset/tools/meas/background/analyze.py:72` names the three hook files (`/etc/kernel/postinst.d/dkms`, `/etc/kernel/header_postinst.d/dkms`, `/usr/lib/dkms/dkms_autoinstaller`); `hook_subtrees` (`:141–161`) takes as a root every pid that executed one of them and collects its descendants through the fork rows, downward only; `:437–441` intersects the hook's tids with the stage tree; `:585–591` feeds the hook run with the most CPU to the orchestrator's build; `dataset/tools/meas/background/modbuild.py:179` keeps only segments whose tid is in that set. `dpkg` and `unattended-upgrade` are the hook's ancestors (dpkg runs the postinst, which runs `run-parts`, which runs the hook); `apt-check` runs outside the hook. None passes a downward walk.
- **The pooled results agree.** The pooled tail's CPU by process name over all 26 landings (`_dev/research/jioh/task-9.10-scenarios-timelines/campaign/dkms/results/pooled.json`, `tail_cpu_by_comm_ms`, every landing) names only `cp`, `depmod`, `dkms`, `dkms_autoinstal`, `find`, `grep`, `ln`, `mkdir`, `mv`, `readlink`, `rm`, `sleep`, `strip`, `zstd`.
- **Where D20's 0.85 % came from.** It was summed over the whole stage's `taskstats.dkms-install.tsv` (237.033 s; the entry's row in `_dev/research/jioh/task-9.11-scheduler-constants/classes/audit.md:10` lists the stage's nice-19 tasks, `dpkg` ×15 and `apt-check` ×3; 9.11 changelog D20), which includes the upgrade tree the tables do not carry.
- **Caveat.** `hook_subtrees` matches by thread id and does not guard against id reuse within a stage of about 17,000 tasks. A check on the raw records, if ever wanted: release `meas-ci-background-2026-10-02`, asset `…-dkms-r10-full-36987468347.zip`, the pids of the nice-19 `apt-check` and `dpkg` rows of `taskstats.dkms-install.tsv` against the header hook's subtree from `perf.dkms-install.forks.txt.gz`; the nice-19 CPU inside the subtree should be 0.

Hands to 9.15: nothing — the dataset docs' nice-19 line (9.11 D20) names `package-upgrade`, whose pool does carry `apt-check`, not this entry.

## R4 — the single-lane set's size and wake-event count (2026-10-09)

The 9.13 line carries 9.5 D74's figures of 2026-09-26: 531,740 exogenous wake events, 84 MB. `scans/size_scan.py` compiles every timeline in the single-lane mode and sums the canonical bytes and the wake events.

| Quantity | 2026-09-26 (9.5 D74) | 2026-10-09 |
|---|---|---|
| Single-lane files | 50 | 50 |
| Exogenous wake events | 531,740 | 4,496,190 |
| Canonical bytes | 84 MB | 665,836,426 (666 MB) |

The eight largest files:

| File | Size | Wake events |
|---|---|---|
| `c6-dual` | 189.8 MB | 1,391,059 |
| `c1-transcode` | 152.8 MB | 1,015,553 |
| `c7-transcode` | 95.1 MB | 632,587 |
| `c4-compile` | 31.1 MB | 189,792 |
| `c1-compile` | 29.7 MB | 181,026 |
| `c1-ml-train` | 24.2 MB | 184,363 |
| `c7-ml-train` | 20.8 MB | 158,521 |
| `c3-workday` | 18.3 MB | 92,827 |

The growth follows 9.10's bindings after D74 — the kernel build whole in `c6-dual` (12,072 s, D141), the transcode whole (4,762 s, D91–D100), four `renderer-hidden` tasks per Chrome file (D131), the launch replays (D140) — with every measured wake of every component carried as its own event (D74). Compiling the 50 files took 129 s (`scans/window_scan.py`'s timing); the full dataset lint, which also validates every file against the JSON Schema, ran past 28 minutes on the same machine.

Hands to 9.14: the per-file size and event count as the run's cost over files × conditions × seeds. Hands to 9.15: the final memo tells 인경민 the simulator loads files up to 190 MB.

## R5 — the demand window today (2026-10-09)

`scans/window_scan.py` applies the compiler's window rule (`dataset/tools/wlc/estimate.py`: a single-lane file's demand in [1.00, 1.50] lanes unless its demand class is `calibration`) to every file's compile report.

| Demand class | Files |
|---|---|
| `calibration` (exempt) | 40 |
| `oversubscribed` | 10 |

Nine of the ten oversubscribed-class files are outside the window:

| File | Demand (lanes) |
|---|---|
| `c2-p1a` | 14.51 |
| `c2-p2a` | 9.38 |
| `c6-dual` | 1.00 |
| `c2-p1b` | 0.92 |
| `c2-p3b` | 0.90 |
| `c3-evening` | 0.90 |
| `c3-creation` | 0.94 |
| `c3-workday` | 0.89 |
| `c2-p3a` | 0.44 |

`c2-p1a`'s and `c2-p2a`'s demands follow the training run and the download bound whole at their CPU totals (9.10 D17, D90, D142) inside short files. The research-slice workflow (`_dev/research/jioh/research-slice-workflow.md`, "CI on the branch") already states the window check may fail on this branch until 9.14 redoes the rule; the bless uses the compiler's allowance that reports violations as warnings (spec decision 10).

Hands to 9.14: these nine files and demands as the state the demand-window redo inherits; the dataset CI gate stays red on the window until then.
