# Class-read findings

Task 9.16 (the Phase 9 exit audits), spec decision 2, the class-read half. Read 2026-10-17 at `928aa8fd`. Every class read is in `class-table.md`: 300 measured, 4 derived, 0 convention. Below are the mismatches it raised, then the check of the 2026-09-13 audit's X items (the mismatches that audit found in the library as it stood then).

No raw release data was needed. Every doubt was settled from the pooled records committed under `_dev/research/jioh/task-9.*`, or from the library itself.

## Findings

### F1 — `renderer-hidden`'s CPU share is the 12 measured renderers' total, but it is stated as one renderer's (code and data; then a doc line)

**What the entry says.** The entry describes one renderer (scope, `dataset/archetypes.yaml:738`: "Values describe one renderer, the 12 page renderers a job measures pooled as its samples"). Its `validation_stats` pairs a per-renderer wake rate with a CPU share (`archetypes.yaml:736`):

`["steady wakes/s per renderer 0.2082–0.2152", "steady cpu-share 0.00009–0.00011"]`

The scope then says (`archetypes.yaml:738`): "the renderer's wakes 0.211 against 0.169/s, its CPU share 9.6 against 9.2 × 10⁻⁵".

**What was measured.**

- The pooled record holds `cpu_share` [9e-05, 9e-05, 0.00011, 0.0001, 9e-05] beside `wakes_per_s` 2.50–2.58, which is all 12 renderers, and `wakes_per_s_per_renderer` 0.208–0.215 (`_dev/research/jioh/task-9.10-scenarios-timelines/campaign/renderer-hidden/results/pooled.json`, `runs.chrome-hidden.phases.steady`). So the stat is the 12 renderers' total CPU share.
- The carried components give one renderer 8.05 × 10⁻⁶: Σ wakes_per_s × run-table mean (`class-share-check.py`). That is 9.6 × 10⁻⁵ / 12.
- 9.8's figure is the same kind of total: 9.16 × 10⁻⁵ / 12 = 7.6 × 10⁻⁶ (`task-9.8-browser-comms/campaign/results/pooled.json`).

**Cause.** `dataset/tools/meas/desktop/fold_in.py:285-286` writes the wake rate per renderer for the renderer subjects but the CPU share from `ph['cpu_share']` unconditionally. The same total, called "its CPU share", is in:

- `desktop/fold_in.py:111` (the scope text);
- `_dev/research/jioh/measurement-campaign-record.md:510`;
- `task-9.10-scenarios-timelines/campaign/renderer-hidden/results/results.md:15`.

The ratio between the two campaigns (9.6 against 9.2) is unaffected.

**Proposed fix.**

- In `fold_in.py:286`, divide by `renderers_measured` for `RENDERER_APPS` and label it "cpu-share per renderer". Re-run the desktop fold-in; the stat becomes about 0.0000075–0.0000092.
- In `fold_in.py:111`, the record line and `results.md`, state "its CPU share 8.0 against 7.6 × 10⁻⁶". Alternatively, keep the totals and call them "the 12 renderers' CPU share".

### F2 — the stopping record is stale for `video-editor`, and the tool now reads only its idle pool (code and data)

**What the committed record shows.** `_dev/research/jioh/task-9.5-interactive-typing/campaign/results-stopping.md` (and `results-stopping/stopping.json`) carries `video-editor`'s row as "driven kdenlive run mean, 20 repeats, ±5.00 %, coverage 91.3 · 91.4 %".

**What the tool now computes.** Since `626c27a6` (9.10 D146), `control_report.IDLE_FROM_95` (`dataset/tools/meas/control_report.py:32-34`) points `kdenlive` at the idle campaign's pool, and `stopping.entries` (`stopping.py:83-89`) then reads only the `idle` phase. Re-run on 2026-10-17 (`python -m meas.stopping`), the row becomes "idle kdenlive run mean, 16, ±4.45 %, 92.3 · 91.3 %". The driven phase's value — the one `video-editor`'s scope caveat (`archetypes.yaml:607`, text in `campaign/fold_in.py:125`) rests on — is no longer computed at all.

**Consequence.** Regenerating the record would make `tests/test_meas_stopping.py:34-35` fail: `video-editor` drops out of the entries within half a point (4.45 % < `NEAR`), while `fold_in.STOPPING_STATED` still lists it. So the test passes only because the record is stale.

**Proposed fix.** Make `stopping.entries` emit both of `video-editor`'s pools as separate rows — the driven pool from `POOL_95` (`meas-ci:interactive:2026-09-18`) and the idle pool from `KDENLIVE_IDLE` (`meas-ci:interactive:2026-10-05`). Then regenerate `results-stopping.md`/`.json`. The test should match the stated caveat to the driven row. The idle row (±4.45 %) is under the half-point line, so no new scope sentence is required by `measurement-overview.md` §6.

### F3 — the typing entries' `input_run` is floored at zero, and no scope says so (doc)

**The arithmetic.** `input_run` (class D) is the process tree's CPU from one input to the next, minus the idle rate × the window, bounded below by zero (`dataset/tools/meas/campaign/analyze.py:425-428`; decided as the zero bound in 9.5 D13, named at 9.5 changelog line 154).

**What the scopes say.** The four scopes state the subtraction but not the floor: "Per-input run is the window rule (D13): all run time of the process tree until the next input minus the idle rate" (`archetypes.yaml:111`, the `code-editor`, `mail-client` and `web-browser` scopes alike).

**Why it matters.** The floor raises the carried mean by the clipped negative mass. `web-browser`'s table has p1 = 0 and p5 = 2,686 µs (`archetypes.yaml:371`), so roughly 1–2 % of its inputs sit at the bound. The other three have p1 > 0.

**Proposed fix.** Add "bounded below by zero, a window quieter than the idle rate carrying no input work (D13)" to the window-rule sentence of the four scopes (in `campaign/fold_in.py`, then re-fold). The mean's lean is not quantified here. The pooled records keep only the floored samples, so quantifying it needs the raw windows; it is listed, not run.

### F4 — `measurement-overview.md` §5 defines a component as one comm within one process role, but `chat-client`'s and `game-client`'s components are comms merged across the tree's processes (doc)

**The definition.** `docs/workload/measurement-overview.md` §5: "Component. One thread comm within one process role (`gpu/Chrome_ChildIOT`, `pid1/systemd`)."

**What the desktop slice does.** For its non-renderer subjects it calls `per_thread(kept, span, None, t0)` with no roles (`dataset/tools/meas/desktop/analyze.py:232`; see the docstring at `campaign/analyze.py:289-291`). So `chat-client`'s `element-desktop` (37 threads), `Chrome_ChildIOT` (4) and `ThreadPoolForeg` (11–13), and `game-client`'s `Chrome_ChildIOT` and `ThreadPoolForeg`, each merge that comm's threads across Element's and the Steam client's processes.

**The values are sound.** Each gap is over the merged wake times, its table mean gives back the carried rate (`class-rate-check.py`), and the compiler emits one stream per component. The entries' own notes say "per thread comm" (`archetypes.yaml:796`), which matches. Only the overview's definition overstates.

**Proposed fix.** In §5, add: "for `chat-client` and `game-client`, one thread comm across the tree's processes (the 9.8 desktop slice's rule)".

### F5 — the hidden renderers wake together across processes; the 4 bound `renderer-hidden` tasks are compiled independently, and neither fact is stated (judgement → one question for 인지오)

**What was measured, and left open.** 9.8 measured, on its 2026-09-20 probe, that the 12 throttled renderers' wakes coincide: all twelve woke in the same 1 s bin 243 times and in the same 10 ms bin 32 times, against none under independent draws (`task-9.8-browser-comms/changelog.md:189-196`, D15; `dataset/tools/meas/desktop/wake_alignment.py:13-14`). It left open "what the alignment above does to the pooling of N renderers as N samples"; no later entry closes it.

**What the dataset does.** The entry pools the renderers as samples of one renderer (`archetypes.yaml:738`). The Chrome files bind 4 renderer tasks (the tab-set campaign `meas-ci:desktop:2026-10-04`), each compiled from its own seeded draw. `measurement-overview.md` §8's compile-fidelity list names what the compiled streams do not keep — gap order, components waking together, a rare event's clustering — but not wakes coinciding across tasks of one entry. The `renderer-hidden` scope does not state the alignment either. The alignment has not been re-read on the current pool (Chrome 154, `meas-ci:desktop:2026-10-05b`).

**Proposed fix** (judgement, for 인지오):

- either state it — in the scope and in §8: "the measured renderers' wakes coincide across processes (9.8 D15); the bound renderer tasks wake independently";
- or re-read `wake_alignment.py` on one `meas-ci:desktop:2026-10-05b` landing first and state that reading.

### F6 — `module-build-orchestrator.tail_work` is written by hand, outside every fold-in's check mode (code)

**The value is right.** `tail_work` 10,027,983 µs (`archetypes.yaml:1111`) is the mean of the 26 landings' tail CPU. Recomputed from `task-9.10-scenarios-timelines/campaign/dkms/results/pooled.json` (`module_build.tail_cpu_by_comm_ms`, summed per landing), it is 10,027.983 ms, so the class is M.

**The gap.** `batch_fold_in.py:59-68` writes `dispatch_overhead`, `tail_run` and `tail_block` but not `tail_work`. The 9.10 changelog (line 1093) records it as stated by hand. It is the only `meas-ci` value no committed fold-in `--check` reproduces; the `period` constants are written by `campaign/fold_in.py:406`.

**Proposed fix.** Have `batch_fold_in.py` write `tail_work` as `{dist: constant, value_us: round(mean over landings of Σ tail_cpu_by_comm_ms × 1000)}`, so `--check` covers it.

## The 2026-09-13 audit's X items, against the final library

| X item (2026-09-13) | now | evidence |
|---|---|---|
| X1 — the compiler "child" was a compiler-family member, not a make job or `cc1`; CPU per `cc1` understated about 4× | resolved | per-member, per-step tables (`archetypes.yaml:981-1002`, `build/shapes.py:108-133`); `cc1` step mean 439.1 ms (`archetypes.yaml` stats of `compiler-child`) |
| X2 — `disk_wait` 3.6 ms was a difference of lifetime medians | resolved | no wait param in `compiler-child`; its scope: the cold-cache disk wait is "reported beside the pool and not carried" |
| X3 — voluntary switches of the main thread only, divided into whole-process CPU | resolved | every carried wake and run comes from `perf sched` per thread (`campaign/analyze.py:166-210, 288-313`); `proc_sampler.py` feeds no fold-in (grep: only `README.md` and the Phase 2 `analyze.py`) |
| X4 — `electron-comms` had no renderer; its gap was a geometric mean between two clusters | resolved | the entry is retired; `chat-client` carries per-wake tables per comm, with no fit across per-process averages (`archetypes.yaml:752-783`). The comm merging is noted in F4. |
| X5 — "idle chromium renderers" was not a renderer set | resolved | page renderers only: the browser's own and the control tab dropped (`desktop/analyze.py:32-66, 105-123, 189-196`). Cross-renderer alignment: F5. |
| X6 — the 21–22 Chromium processes were a launch transient | resolved | no process count is carried. The renderer count comes from the tab-set campaign's steady listing (`meas-ci:desktop:2026-10-04`, 4 in every repeat). |
| X7 — the background-crawler run showed no indexing | resolved | `file-indexer`: Tracker's first index of HippoCamp's Bei home, 875 files, 39.4 s of CPU, "Currently indexed: 875 files" checked per repeat (campaign record, 9.10 `file-indexer`) |
| X8 — per-iteration params were spreads across processes | resolved | every measured param is a quantile table of individual samples (`distribution.py:24-49`). The library's only lognormal is `game-task-chain`'s literature anchor (`archetypes.yaml:1734`). |
| X9 — zero-CPU daemons were dropped from a fit | resolved | session components are per wake (`session/analyze.py:153-166`). Tables keep zeros (e.g. `sh_step_2` min 0). |
| X10 — `io-stream`'s 0.73 was a stale cli:1 number | resolved | the entry is retired |
| X11 — `network-bulk`'s "saturating the runner link" was not measured | resolved | the entry is retired; `game-download` runs a shaped 121.0 Mbps link with the payload rate measured (115.3–115.8 Mbps, `game-download` stats) |
| X12 — `dispatch_overhead` was a mean stored as a median and divided by grandchildren | resolved | a quantile table of make's CPU between consecutive forks of one make (`build/analyze.py:418-441`); forks and makes counted ("5 957 forks under 719 make processes") |
| X13 — "lifetime log-std overshot the mean 2.4×" did not reproduce | resolved | the sentence is gone (grep `2.4x`: 0) |
| X14 — name verification weaker than claimed | outside the class read | not a library value; the carried comms come from the traces |
| X15 — stale docs | resolved as far as read | `docs/references.md:15` describes `meas-ci`'s locator; `building-plan.md:103` says "No entry carries `meas-pending`"; the release map is `dataset/meas-releases.yaml` |
| X16 — `tar-read-cold` read no file contents | resolved | not carried; `file-archiver` measures 7-Zip on the 10 GB set |
