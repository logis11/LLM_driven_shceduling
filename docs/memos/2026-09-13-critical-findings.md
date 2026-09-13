# Critical findings from reading the archetype sources against their primary texts

> Status: memo · Created 2026-09-13 · Updated 2026-09-13

Findings from checking `dataset/archetypes.yaml` and its grounding documents against the primary sources and against the compiler, measurement summary and raw measurement release. Each finding gives what the repository states (with file and line), what the primary text or artifact shows (with the copy read and the date), and what it affects. Nothing in the repository was changed; resolution is left to the owners of each file.

## Summary

| # | Finding | Affects |
|---|---|---|
| A1 | `ocallahan-atc17`'s 2,430 processes come from a DynamoRio 6.1.0 build, not a Linux kernel build | eight documents; `build-orchestrator` default `spawn_count` |
| A2 | The 16.7 ms frame budget attributed to `lavd-ossna24` does not appear in the slides | `game-task-chain.frame_period`, which sets the chain's cadence in every gaming file |
| A3 | Roeser's 158 ms is a log-scale location, stored and sampled as a mean; the paper's own pause component (~253 ms) is not used | `desktop-interactive.input_gap` |
| A4 | Coetzee's short-lived kernel-build processes are `cp` and `mkdir`, not compilers | the "corroborates" claim for `compiler-child` |
| A5 | `ananicy-rules` `type` classes group by prescription, not behaviour; the same catalogue has classes matching two of the three `meas` entries | the Tier-1 harvest claim; `category_source` consistency |
| B1 | Two `game-task-chain` params are never read by the compiler; the tail params carry a slide tag but are placeholders | gaming workloads |
| B2 | `compiler-child.disk_wait` `sigma_log: 0.8` is a pre-measurement placeholder under a measurement tag | `compiler-child` |
| B3 | Measured peak concurrency is 16 compiler-family processes at `-j8`; the archetype caps children at 8 | `compiler-child` / `build-orchestrator` validation |
| B4 | `per-iteration` sampling declared on unbounded loops compiles to `per-task`; the measured spreads are between-process | `background-crawler`, `electron-comms`, `system-daemon` |
| B5 | `desktop-interactive` bursts average half of each input gap, so a focused editor runs at ~50% CPU | load of every file with a focused interactive task |
| B6 | `gnome-shell`, `Xorg`, `pipewire` bind to `system-daemon`, whose values come from server daemons | `c1-idle` and files with those names |
| B7 | Smaller consistency gaps between plan, linter, timelines and data | see list |
| C | Stale prose after the measurement fold-in | four documents |
| D | Sources not read against their primary text | `chang-chi21`, `cpsmark-tbench23` |

## A. Primary text contradicts the repository's description

### A1. The 2,430-process workload is a DynamoRio build

**Repository.** Every description places the figure on a Linux kernel build:

- `dataset/sources.yaml:70–71` — "(sec-4.3, Linux kernel-build workload; written "2430" in the paper)"
- `docs/references.md:107` — "(§4.3, kernel-build workload; …)"
- `dataset/archetypes.yaml:247` — "the kernel-build default is 2,430 (ocallahan-atc17 sec-4.3)"
- `docs/workload/archetype-plan.md:53`, `docs/workload/building-plan.md:61` ("2,430 procs per kernel build"), `docs/workload/scenario-catalog.md:22`, `docs/workload/source-vetting.md:70, 95, 123`
- `docs/simulator/interpretation-contract.md:56` uses "2,430 compiler children" as its spawn-table example

**Primary text.** USENIX ATC '17 proceedings PDF (usenix.org/system/files/conference/atc17/atc17-o_callahan.pdf) and the extended report arXiv:1705.05937, both read 2026-09-13. §4.1 and §4.3 are on proceedings p. 383.

> "make builds DynamoRio [8] (version 6.1.0) with make -j8 (-j8 omitted when restricting to a single core). This tests potentially-parallel execution of many short-lived processes." (§4.1)

> "Also, make forks and execs 2430 processes, mostly short-lived. (The next most prolific workload is sambatest with 89.)" (§4.3)

> "All tests run on a Dell XPS15 laptop with a quad-core Intel Skylake CPU (8 SMT threads), 16GB RAM and a 512GB SSD using Btrfs in Fedora Core 23 Linux." (§4.1)

Neither version calls the workload a kernel build. The quoted sentence itself is verbatim-correct; the workload attribution is not.

**What it affects.**

- The existence claim for the compile class stands: the authors chose the workload to test "many short-lived processes".
- The 2,430 default for `spawn_count` is not a kernel-build figure. The measured kernel build (`meas-ci:cli:3`, linux-6.6 defconfig, `make -j8`, 5 repeats) produced a median of 11,883 compiler-family processes (`dataset/meas/summary.json`, `across_repeats.compiler_children`).
- The paper also ran `make -j8`, which the `-j8` convention (`archetype-plan.md:86`, justified as "between interbench's documented `-j4` and desktop `nproc` conventions") does not cite.
- No coreset timeline uses 2,430 (`c1-compile` 100, `c6-dual` 85, `c3-workday` 4,200), so no compiled artifact changes; the error is in citations and the documented default.

### A2. The 16.7 ms frame budget is not in the LAVD slides

**Repository.**

- `dataset/archetypes.yaml:361–363` — `frame_period: {dist: constant, value_us: 16667, …, source: "lavd-ossna24"}`
- `dataset/sources.yaml:59` — "16.7 ms frame budget, 15 ms targeted latency"
- `docs/references.md:170`, `docs/workload/archetype-plan.md:61`, `docs/workload/building-plan.md:59`, `docs/workload/source-vetting.md:17, 64`

**Primary text.** Slides PDF (static.sched.com/hosted_files/ossna2024/9b/scx-lavd-oss-na24.pdf, 30 slides), read 2026-09-13: text extracted from every slide and the embedded figures inspected as images. No slide contains 16.7, 16.67, 60 fps or "frame budget". The only time budget is slide 27:

> "The LAVD scheduler tries to schedule all runnable tasks at least once within a predefined time window, which is called a targeted latency (e.g., 15 msec)."

That is a scheduling window, not a frame period. The example game on slide 6 runs at an average of 41.3 FPS. The paired prose source `corbet-lwn24` (lwn.net/Articles/991205) and the later LWN article listed in `references.md:175` (lwn.net/Articles/1051430), both read 2026-09-13, do not contain the figure either.

**What it affects.** `frame_period` is the `TIMER` period of the first chain member (`dataset/tools/wlc/compiler.py:314, 329`) and the denominator of the `-single` lane-scaling factor (`compiler.py:321`). It sets the cadence and the scaled demand of every gaming workload. The value is 60 Hz arithmetic with no located source.

### A3. Roeser's 158 ms is a log-scale location, and its pause component is not used

**Repository.**

- `dataset/archetypes.yaml:109–113` — `fluent_mean_us: 158000`, `pause_probability: 0.34`, `pause_mean_us: 395235`
- `dataset/tools/wlc/sampling.py:55–59` treats `fluent_mean_us` as a mean and converts it to a median (`mean / exp(sigma²/2)`), giving ≈148,613 us
- `archetypes.yaml:134–136` — `pause_mean_us` is "our arithmetic closing the mixture on dhakal's overall mean"

**Primary text.** Author manuscript, Nottingham Trent University repository (irep.ntu.ac.uk, eprint 43931, 44 pp.), read 2026-09-13. The publisher's copy was not reachable, so page numbers refer to the manuscript.

- Model (manuscript pp. 16–17): the fluent component is `LogNormal(β + u_i + w_j, σ²_e)` and the disfluent component `LogNormal(β + δ + u_i + w_j, σ²_e′)`.
- The paper converts log-scale values to milliseconds by exponentiation: "distributed around a value of 5 log msecs (i.e. ≈150 msecs)" (p. 14). For a log-normal that value is the median, not the mean.
- Results (p. 25; Table 3 on p. 27):

> "After accounting for process disfluencies, keystroke intervals were longer for the consonants task (429 msecs, PI: 356 – 515) compared to the LF-bigrams task (158 msecs, PI: 139 – 180). … For the LF-bigrams task, the model determined a slowdown of 95 msecs (PI: 76 – 116) with a probability of 0.34 (PI: 0.31 – 0.38)"

**What it affects.**

- The field name and the compiler both read 158 as a mean; the source reports a location that corresponds to a median. The effect on the fluent median is ~6%.
- The paper's pause component for the same task is β + δ ≈ 253 ms. The archetype takes θ = 0.34 from that task but closes the pause component at 395 ms from `dhakal-chi18`'s overall mean. The arithmetic is disclosed; the existence of the source's own paired value is not.
- `dhakal-chi18`'s 238.66 ms (read 2026-09-13 from the authors' PDF, userinterfaces.aalto.fi/136Mkeystrokes) is a mean of per-participant averages from transcription typing, with IKIs over 5,000 ms removed. `overall_mean_us` uses it as the mean of one user's stream.

### A4. Coetzee's short-lived processes are `cp` and `mkdir`

**Repository.** `dataset/archetypes.yaml:204–205` — "coetzee-arxiv12 sec-9 corroborates, kernel-build-specific"; `docs/workload/archetype-plan.md:53` — "cross-confirmed by … `coetzee-arxiv12`".

**Primary text.** arXiv:1203.2704 v1, §9, read 2026-09-13:

> "In practice, even with caching, the system added too much overhead to be practical due to the Linux kernel build's enormous number of short-lived processes like cp and mkdir."

**What it affects.** The source supports "the kernel build spawns many short-lived processes". It does not name compilers, so the corroboration of the `compiler-child` class is weaker than stated.

### A5. `ananicy-rules` types are prescriptions, and the harvest rule is applied unevenly

**Repository.** `docs/workload/archetype-plan.md:31` — "`ananicy-rules`' `type` field — literally a community-maintained archetype taxonomy". The same paragraph says `network-bulk`, `electron-comms` and `system-daemon` "have no literature taxonomy" and marks them `category_source: meas`. `background-crawler` takes `category_source: ananicy-rules` (`BG_CPUIO`).

**Primary artifact.** github.com/CachyOS/ananicy-rules at commit `03ef03fb` (2026-09-08, the commit guidebook volume 2 counted), cloned 2026-09-13.

- `00-types.types` comments state treatments: `Game` "Use more CPU time if possible"; `BG_CPUIO` "it must be as silent as possible"; `Heavy_CPU` "It must work fast enough but must not create so much noise".
- `BG_CPUIO` holds `baloo_file` (indexer), `borg` and `rsync` (backup/sync), `wget`, `curl`, `aria2c`, `transmission-daemon` (downloads), `clamd`. These span `background-crawler`, `io-stream` and `network-bulk`.
- `Chat` holds `discord`, `element-desktop`, `slack`, `zoom`, `thunderbird`. `Service` holds `dbus-daemon`.
- No entry exists for `tracker-miner-fs-3`, `updatedb`, `cc1`, `gcc`, `make` or `clamscan`.

**What it affects.**

- The catalogue supports "shipped software distinguishes these classes as units of treatment". Reading behaviour classes from it is an interpretation.
- If `BG_CPUIO` qualifies as the harvest source for `background-crawler`, `Chat` and `Service` qualify equally for `electron-comms` and `system-daemon`. If they do not qualify because they mix behaviours, `BG_CPUIO` mixes behaviours too. No record states which rule was applied.
- `archetype-plan.md:31` lists a type `Player`; the catalogue's types are `Player-Audio` and `Player-Video`.

## B. Dataset and tooling

### B1. Declared `game-task-chain` parameters that do not reach any workload

- `frac_long_lived` (0.90, `archetypes.yaml:352`) and `frac_wakeups_from_wait` (0.70–0.75, `:358`) match slides 12 and 14. `_chain_constructor` (`compiler.py:307–350`) reads neither. All 300 tasks live for the whole segment, and the WAIT/SLEEP split is fixed at 16 : 284.
- `tail_idle_gap` (500,000 us) and `tail_run` (200 us) carry `source: "lavd-ossna24:s12"` (`:367–372`). The modeling notes call them "our placeholder encoding of near-idle". Slide 12 gives the concentration statistic ("Top 30-40 most frequently scheduled tasks take 95% of scheduling") but no values.
- The chain is a linearisation. The slide-16 graph shows separate clusters (game ↔ wineserver, task workers → dxvk-cs → dxvk-submit, winepulse, pipewire), not one 16-stage chain. The modeling notes disclose this.
- `n_tasks: 300` is a count held as an archetype parameter, against the boundary rule that counts are "excluded by construction" (`archetype-plan.md:27`) and the header rule "Counts never carry values here" (`archetypes.yaml:24`). Every gaming file therefore shows `game.exe × 300`.

### B2. `compiler-child.disk_wait` spread is a leftover placeholder

`archetypes.yaml:189` — `{dist: lognormal, median_us: 3600, sigma_log: 0.8, …, source: "meas-ci:cli:3"}`. The history is `df2c5f5` (no values, `meas-pending`), then `349423b` (median 20,000, `sigma_log` 0.8, `meas-pending`), then `8416025` (median 3,600 from measurement, `sigma_log` unchanged, tag changed to `meas-ci:cli:3`). The modeling notes explain the median as a measured noise bound and do not mention the spread. Other entries mark unmeasured spreads "our convention"; this one carries no such note.

### B3. Concurrency unit: 16 measured versus a cap of 8

`dataset/meas/summary.json` records `compiler_peak_concurrent: 16` at `make -j8`. `dataset/tools/meas/analyze.py:25` counts as "compiler family": `cc1`, `cc1plus`, `gcc`, `g++`, `as`, `ld`, `collect2`, `objtool`, `fixdep`, `objcopy`, `genksyms`, `modpost`.

The archetype derives per-child CPU and lifetime from that whole family (per-member means), but caps concurrency at 8 (per `make` job). Its declared validation statistic is "concurrent-children time series vs make -jN run" (`archetypes.yaml:242`). As written, that comparison sets the per-member unit (peak 16) against a per-job cap (8). One of the two units needs to change before the validation can run.

### B4. Sampling granularity on unbounded loops

`sampling: per-iteration` is declared on segment-bound (unbounded) loops: `background-crawler` (`archetypes.yaml:305, 308, 311`), `electron-comms.heartbeat_work` (`:455`), `system-daemon` (`:494, 497`). `interpretation-contract.md` §5 permits per-iteration sampling "only when bounded", and `compiler.py:8` states such params "degrade to per-task draws". Each instance therefore repeats one gap and one burst for its whole life.

The measured distributions these values come from are between-process distributions of per-process mean gaps (`analyze.py` `wake_stats` computes one `gap_us` per process as span / voluntary switches; `lognormal_fit` pools those). That matches the compiled per-task behaviour and not the declared per-iteration one. Separately, `background-crawler`'s spreads come from 5 values (one miner per repeat), and `system-daemon`'s burst fit uses the 29 of 51 processes with non-zero CPU ticks (`TICK_US = 10_000`).

### B5. `desktop-interactive` runs at about half a CPU while focused

`burst_fraction` is `uniform(0, 1)` times the preceding gap (`archetypes.yaml:118`, `compiler.py:211–212`), so the expected burst is half the expected gap. In `c1-compile` (seed 103) the focused `code` task has a static demand of 28,470,806 us over its 56 s focus window. The source is interbench X, "an idle gui where a window is grabbed and then dragged across the screen"; interbench implements it as a deterministic 0→100% ramp in 1 ms chunks (`emulate_x` in `interbench.c` at commit `e612a65c`). The input gaps come from transcription typing. The archetype thus combines typing inter-arrivals with window-drag CPU cost. This is disclosed as modeling and is not an error, but the resulting load is far above an editor's, and every file with a focused interactive task inherits it.

### B6. Desktop session processes bound to server-daemon measurements

`c1-idle` binds `gnome-shell`, `Xorg` and `pipewire` to `system-daemon`. That entry's values come from stock runner daemons (`analyze.py` `DAEMON_NAMES`: `systemd` family, `dbus-daemon`, `cron`, `rsyslogd`, `polkitd`, `chronyd`, `multipathd`, `agetty`, `packagekitd`, `udisksd`, `acpid`). None of the three session processes was measured, and `ananicy-rules` classes all three as `LowLatency_RT`. The binding is not marked as an approximation anywhere. `c1-gaming`'s `wineserver` (also `system-daemon`) drew a 1,225 s sleep and never wakes in its 60 s segment, although slide 13 names wineserver as a 260 µs coordination task.

### B7. Smaller gaps

- `archetype-plan.md:31` says `category_source` is "machine-checkable by the linter". `wlc/linter.py` checks that the field is present, not its value.
- `archetype-plan.md:40` says static counts are "binding-time parameters with a source tag". Timeline `count` fields have no source slot (`wlc/timeline.py:123`).
- `background-crawler` is bound in no coreset timeline. `archetypes.yaml` (cpu-batch notes) says the everyday indexer "remains background-crawler elsewhere (C4/S14)"; no C4 file uses it.
- `compiler-child` notes say carrying the lifetime spread "overshot the mean 2.4x". Recomputing from `summary.json` gives ≈2.6× against the repeat median (89,997 us) and ≈2.4× against the repeat maximum (98,793 us); the note does not say which.
- `archetype-plan.md:69` cites `cpsmark-tbench23:table-4` for creative apps being time-shared compositions. The registry describes Table 4 as per-workload hardware sensitivity (GPU/CPU/storage), which does not bear on time-sharing structure. Table 4 itself was not read (see D).
- The `electron-comms` referee decision (chromium renderers kept on the entry, `archetypes.yaml` notes) rests on "close in median". The spreads (1.09 vs 1.72) and CPU per wake (289 vs 647 us) differ substantially, and no acceptance criterion is written.
- `schbench` and `hackbench` are listed as grounding a "messaging/wakeup-heavy" / "chat/IPC-heavy archetype" (`grounding-sources.md:28–29`; `source-vetting.md` B4). No such entry exists, and no record of its rejection was found.
- The privacy-scrub tool that `building-plan.md:189` says "ships in the artifact" is not in the repository.

## C. Stale prose after the measurement fold-in

The file is freeze-clean: `lint_repo(..., freeze=True)` returns no errors, and `dataset/README.md` calls it "fully measured". The prose still describes the pre-measurement state:

- `docs/references.md:280` — `meas-ci` "status: reserved (no runs yet; `meas-pending` placeholders in archetypes until freeze)"
- `docs/workload/archetype-plan.md:53, 58, 64–66` mark parameters `meas-pending`; `:57` gives `io-stream` params as interbench (the file tags `meas-ci:cli:3`). The header reads "Updated 2026-09-10".
- `docs/workload/building-plan.md:61, 65–67` mark parameters `meas-pending`; `:183` gives the `/proc` sampler as "1 s", while `.github/workflows/meas-cli.yml` uses `--interval 0.5` and `meas-gui.yml` uses `--interval 0.2`.
- `docs/workload/coreset-guide.md` gives `network-bulk` compiled SLEEP as "~5.7 ms"; the current `net_wait` median is 16,700 us (compiled `c2-p2a` download median 16,711 us).
- `dataset/README.md`'s canonical-format example uses the retired attribute name `wanted`.

## D. Not read against the primary text

- `chang-chi21` — ACM Digital Library returned HTTP 403 on 2026-09-13; no other copy located.
- `cpsmark-tbench23` — ScienceDirect refused automated retrieval on 2026-09-13.

Both are marked `verified` in `docs/references.md`. The claims above that rest on them (tab-count threshold, Table 4) were not re-checked.

## Sources read for this memo

| id | Copy read (2026-09-13) |
|---|---|
| `ocallahan-atc17` | USENIX ATC '17 proceedings PDF; arXiv:1705.05937 |
| `coetzee-arxiv12` | arXiv:1203.2704 v1 |
| `lavd-ossna24` | slides PDF, all 30 slides incl. figures |
| `corbet-lwn24` | lwn.net/Articles/991205; also lwn.net/Articles/1051430 |
| `dhakal-chi18` | authors' PDF, userinterfaces.aalto.fi/136Mkeystrokes |
| `roeser-rw24` | author manuscript, irep.ntu.ac.uk eprint 43931 |
| `dubroy-chi10` | authors' PDF, dgp.toronto.edu/~ravin/papers/chi2010_tabbedbrowsing.pdf |
| `mozilla-testpilot10` / `singervine-slate10` | testpilotweb aggregated-data page; Slate article |
| `interbench` | github.com/ckolivas/interbench at `e612a65c` (`interbench.8`, `interbench.c`) |
| `rt-app` | github.com/scheduler-tools/rt-app at `d6f8be41` (`doc/tutorial.txt`, `doc/examples/template.json`) |
| `ananicy-rules` | github.com/CachyOS/ananicy-rules at `03ef03fb` |
| `meas-ci` | `dataset/meas/summary.json`; release `meas-ci-2026-08-28` (`meas-cli3.zip` `spec.json`: `nproc` 4, AMD EPYC 9V74, 16 GB, Ubuntu 24.04.4, run number 3) |
