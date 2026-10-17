# 9.16 data chunk D — dataset code and data, one rebuild

Nothing staged or committed. Every change is in the working tree on `jioh/dataset-rebuild`, read against HEAD `b51df8a4`. The `docs/` edits already in the tree (the docs chunks') are left alone; `dataset/README.md` is the W chunk's and is not touched here. Python: the session's venv (`<scratch>/venv/bin/python`, `PY=` for make). `<scratch>` is `/private/tmp/claude-501/-Users-jiohin-Desktop-future-of-sw-LLM-driven-shceduling/43e369a1-b5c7-40a2-b57d-cc4fcdb568dc/scratchpad`; this chunk's working files are in `<scratch>/d916/`. Line numbers are the files as they stand after this chunk.

## Items

### meas-new C1 / repro M10 — the readers find `video-editor`'s idle landings

- `dataset/tools/meas/control_report.py:35–36`: `IDLE_MODE_95 = {"kdenlive": "idle"}` beside `IDLE_FROM_95`, the mode the idle campaign's artifacts are named by (`meas-interactive-kdenlive-r<k>-idle`).
- `dataset/tools/meas/burstiness.py:93`, `:101`, `:182–183`: `campaign_streams(..., mode="full")` passes the mode to `artifact_dir`; `campaign_entries` calls it with `cr.IDLE_MODE_95.get(app, "full")`.
- `dataset/tools/meas/windows.py:168–169`: the `PHASES_95` loop looks an idle repeat up under `IDLE_MODE_95` (the driven and operation loops read 9.5's `full` landings, unchanged).
- Tests: `tests/test_meas_burstiness.py` `test_an_idle_repeat_is_found_under_the_mode_its_campaign_landed_it_in`, `test_every_idle_pool_s_mode_is_the_one_the_readers_look_its_landings_up_by` (each `IDLE_FROM_95` pool's recorded `mode` equals `IDLE_MODE_95`'s, `full` for `thunderbird-send`).
- Run: `windows.py campaign <scratch>/r916/views/win95 … --app kdenlive` and `burstiness.py campaign … --app kdenlive`, unpatched, exit 0 (they stopped at "kdenlive repeat 1 of run 37273046929: 0 artifacts" before).

### repro M5 — `windows.py desktop` (and `burstiness.py desktop`) read the folded set

- `dataset/tools/meas/windows.py:235–240`, `dataset/tools/meas/burstiness.py:134–140`: `desktop_entries` iterates `desktop/fold_in.FOLDED`, not `CARRIED` (which keeps `chrome-visible`, out of the library since 9.10 D16). `burstiness.py` had the same `KeyError: 'renderer-visible'`.
- Tests: `test_the_desktop_reading_takes_only_the_entries_the_library_folds` in `tests/test_meas_windows.py` and `tests/test_meas_burstiness.py` (the pool lookup stubbed; the apps read equal `FOLDED`).
- Regenerated: `_dev/research/jioh/task-9.8-browser-comms/campaign/results-windows/windows.json` and `results-windows.md` (`windows.py desktop <scratch>/r916/views/win-desk …`, no `--app`): `renderer-visible` gone; `chat-client` and `game-client` byte-equal to the committed entries; `renderer-hidden` the 5-repeat reading of `meas-ci:desktop:2026-10-05b` (equal leaf for leaf to the audit's `<scratch>/r916/out/win-desktop.json`).
- Also regenerated, the burstiness half of the same reader (9.15's hand-off of the burstiness and window readings on the two current pools): `_dev/research/jioh/task-9.8-browser-comms/campaign/results-burstiness/burstiness.json` and `results-burstiness.md` (`burstiness.py desktop`, all three folded entries; `chat-client` and `game-client` unchanged, `renderer-visible` gone, `renderer-hidden` equal to `meas-new/out/burstiness.json`'s entry: 1–100 ms medians 1.26–1.44×).

### repro M10 / M11 — the 9.5 window record's `video-editor` idle entry

- Regenerated with the fixed tool: `windows.py campaign <scratch>/r916/views/win95 <scratch>/d916/win95-kdenlive.json --app kdenlive`, exit 0. Its `video-editor/driven` and `video-editor/preview-render` entries equal the committed ones; its `video-editor` idle entry (16 repeats of `kdenlive-idle/results/pool-kdenlive.json`, nine 20 s windows) replaces the record's; the page re-rendered with `windows.render`. `_dev/research/jioh/task-9.5-interactive-typing/campaign/results-windows/windows.json` and `results-windows.md` equal the audit's `win95-ordered.json` / `.md` leaf for leaf and byte for byte. Only that entry's table moves (all wakes 1.363 → 1.264/s; `kdenlive` 46.6 % → 41.5 % of the phase's CPU; above the median window 2.1 % → 2.7 %). No library statement rests on it (`WINDOWS_STATED` holds `mail-client` and `web-browser`).
- The burstiness half: `_dev/research/jioh/task-9.5-interactive-typing/campaign/results-burstiness/burstiness.json` and `results-burstiness.md`, the `video-editor` entry replaced by `burstiness.py campaign … --app kdenlive` (equal to `meas-new/out/burstiness.json`'s: 1–100 ms medians 1.22–1.32×); the other four entries unchanged (the committed page equals `render` of the committed record, checked first).

### repro M4 — `renderer-hidden`'s window sentence

- `dataset/tools/meas/desktop/fold_in.py:95–97` (`WINDOWS_1005B`): "`MemoryInfra`, one of the residual's two comms, wakes at 3.6 times its phase rate in the first 100 s and 2.4 times 400–500 s in" in place of "the residual (`MemoryInfra`, `ThreadPoolServi`) wakes at …". The library's `renderer-hidden` scope (`dataset/archetypes.yaml:738`) carries it.
- The reading committed beside `renderer-hidden/results/`: `windows.py` gains `--split-residual` (desktop family; `dataset/tools/meas/windows.py:8–9`, `:13`, `:235`, `:252–253`, `:336–341`), each residual comm read apart as `residual/<comm>`. `_dev/research/jioh/task-9.10-scenarios-timelines/campaign/renderer-hidden/results/windows-split-residual.json` / `.md` (`--app chrome-hidden --split-residual`): `residual/MemoryInfra` 3.60 · 0 · 0 · 0 · 2.40 · 0 of its mean, `residual/ThreadPoolServi` 0.58–1.20; and `windows.json` / `windows.md` (`--app chrome-hidden`): the residual whole 1.51 · 0.50 · 0.77 · 1.03 · 1.36 · 0.83, the page thread 0.068 / 0.057–0.072 ms, 5.2 % above the median window.
- `_dev/research/jioh/task-9.10-scenarios-timelines/campaign/renderer-hidden/results/results.md:16`: the sentence restated the same way, with the residual's own 1.51 and 1.36 and the two records named, marked as the 2026-10-17 correction.

### repro M9 — `renderer-hidden`'s 3,600 s span: the CPU's lower bound

- `dataset/tools/meas/campaign/span_probe.py`: `level_reading` reports `least` and `largest`, the signed least and largest window over every placement (`:66–68`, `:80`); `level-desktop` takes `--from S`, the phase's first S seconds left out (`:10–13`, `:189`, `:203–206`). Test: `tests/test_meas_span_probe.py` `test_the_range_a_window_holds_is_its_least_and_largest_placement`.
- The reading, `span_probe.py level-desktop <scratch>/r916/views/probes/rh11 chrome-hidden 600 3000 --from 600` (release `meas-ci-probes-2026-10-05`, run 37273691029), committed as `_dev/research/jioh/task-9.10-scenarios-timelines/campaign/spans/results/renderer-hidden-past600.level.json`: over 600–3,600 s at 10 s steps, CPU least −7.80 %, largest +10.44 %, at the first placement (600 s in) −7.19 %; wakes −3.50 % to +3.71 %. So the stated −7.2 % was the first placement's reading, not the bound; the bound is −7.8 %.
- `dataset/tools/meas/desktop/fold_in.py:105` (`SPAN_1005B`): "the CPU within −7.8 % and +10.4 %"; the library's scope carries it. `_dev/research/jioh/task-9.10-scenarios-timelines/campaign/spans/results/results.md:34`: corrected, the record and the −7.2 % origin named.

### class F1 — `renderer-hidden`'s CPU share is the 12 renderers'

- Taken the second way the finding offers (name it the renderers' share): the pooled `cpu_share` is rounded to 5 decimals (9e-05, 9e-05, 0.00011, 0.0001, 9e-05), so a per-renderer division would state a precision the record does not hold.
- `dataset/tools/meas/desktop/fold_in.py:285–293`: a renderer entry's stat reads "steady cpu-share of the 12 renderers 0.00009–0.00011" (the count from `renderers_measured`); `:111–112` (`SPAN_1005B`): "the 12 renderers' CPU share 9.6 against 9.2 × 10⁻⁵". Library: `dataset/archetypes.yaml:736`, `:738`.
- `_dev/research/jioh/measurement-campaign-record.md:510` and `_dev/research/jioh/task-9.10-scenarios-timelines/campaign/renderer-hidden/results/results.md:15` likewise (the results page also gives one renderer's, about 8.0 against 7.6 × 10⁻⁶, from the class read).

### class F2 / repro M3 — the stopping record reads both of `video-editor`'s pools

- `dataset/tools/meas/stopping.py:77–123`: an entry whose idle phase has a pool of its own reads that pool's idle values and its main pool's other phases, the main pool left out when it stopped at its recording's last window (`thunderbird-send`'s keys-only pool); the widest of the two is the entry's. `pool` lists both pools where both are read, and `widest.pool` names the one the widest value came from.
- Regenerated `_dev/research/jioh/task-9.5-interactive-typing/campaign/results-stopping/stopping.json` (`stopping.py <out> --md <page>`, n 4,000, seed 1): every value equal to the committed record; only `video-editor`'s `pool` (now the two pools) and its `widest.pool` (`results-same-machine`) added. Its widest value stays `driven kdenlive run mean (ms)` ±5.00 % over 20 repeats, coverage 91.35 % · 91.4 %; `results-stopping.md` byte-identical.
- Test: `tests/test_meas_stopping.py` `test_each_entry_s_widest_value_is_the_record_s_read_over_every_pool_the_fold_in_carries` (`stopping.entries(1)` against the committed record's pools, repeats and widest value per entry; `video-editor` two pools, driven, from the main pool).

### class F6 — `batch_fold_in.py` writes `tail_work`

- `dataset/tools/meas/batch_fold_in.py:70–78` (`CONSTANTS`, `tail_work_us`, `CONSTANT_LINE`), `:96–107` (the rewrite), `:119`, `:10–11` (docstring), `:133`: `module-build-orchestrator.tail_work` written as the mean over the 26 landings of `tail_cpu_by_comm_ms` summed, in µs — 10,027,983, the library's value. `--check` exit 0; with the value moved by 1 µs, exit 1.
- Test: `tests/test_measured_fidelity.py` `test_the_module_build_s_tail_work_is_the_landings_mean_tail_cpu`.

### repro M1 — four records re-pooled with HEAD's `background/pool.py` (schema fields only)

- `7z-pooled.json` (`task-9.7-background-io/campaign/results/`), `upgrade`, `tracker`, `mnist` `pooled.json` (`task-9.10-scenarios-timelines/campaign/<app>/results/`): the audit's re-pools (`<scratch>/r916/out/bg-<app>-pooled.json`, HEAD's pool over each release) with the committed records' `path` leaves and `gated_out` kept (`<scratch>/d916/merge_keep.py`; the re-pools ran on the release root, and the 7z release's gated reports are not the record's list, M7). Against the committed records every leaf is equal (30,817 / 437,329 / 60,041 / 1,350); added are `perf_over_taskstats_threads` per process and, for `7z` and `upgrade`, `stability.excepted` and each excepted quantity's `carried` / `excepted`. No `excluded_repeats` in any of the four.
- Their pages regenerated with `background/pool.render` on the merged record, the repeat keys restored to ints (`<scratch>/d916/render_bg.py`; `render` of each committed record so restored equals its committed page past the title line): `task-9.7-background-io/campaign/results-7z.md`, `task-9.10-scenarios-timelines/campaign/{upgrade,tracker,mnist}/results/results.md`. The title becomes HEAD's pool title; each process line gains "(thread rows …)"; the stability table marks the excepted values "carried (9.6 D29; 9.10 D58)".
- `batch_fold_in.py --check` unaffected (exit 0).

### `game-download` — the SteamCMD re-pool finished from the cache

- The re-pool the audit stopped at 43 of 90 phase analyses resumed from its cache: `<scratch>/r916/bin/bgpool.sh steamcmd meas-ci:background:2026-09-19 _dev/research/jioh/task-9.7-background-io/campaign/results/steamcmd-pooled.json` (HEAD's `background/pool.py`, `--jobs 3`), run in the background beside this chunk: rc 0, 4,750 s, all 90 analyses. Against the committed record: 350,924 leaves equal, none differing in value — `total_work: 727.170s` (`program_cpu_us`, 30 repeats) reproduced. Added at HEAD (finding M1's kind): `perf_over_taskstats_threads` for every process (90), `stability.excepted` and two quantities' `carried` / `excepted`. The re-pool's `gated_out` is the release's gated reports (46 against the record's 42) and it has no `excluded_repeats` (the loop adds that key): both kept from the record (`merge_keep.py … --keep /gated_out --keep /runs/steamcmd/excluded_repeats`).
- Written: `_dev/research/jioh/task-9.7-background-io/campaign/results/steamcmd-pooled.json`, and `results-steamcmd.md` re-rendered as the other four, its "Left out of this pool" section (pool_runs.py's, repeats 21, 23, 32, 33) kept. `batch_fold_in.py --check` exit 0; the stability ledger re-run after it equal to `meas-new/out/` (5,902 leaves).
- `meas/repro-table.md:38` (row B, `game-download`) and `:54` (the `total_work` binds) record the result.

### repro M2 / D6 — the 9.8 untraced control read against 9.8's pool

- `dataset/tools/meas/control_report.py:419–421`: every desktop subject's control read against 9.8's pooled record (`POOL_98`), the hidden renderer's included, not the 9.10 campaign its entry is now folded from.
- Control pools re-pooled at HEAD (`desktop/pool.py <view> --cpu-model "EPYC 7763" --control`): `chrome-hidden` and `chrome-visible` equal the committed pools (not rewritten); `element` and `steam` gain each job's build (`Element 1.12.29`, `Steam client build 1788652215`), `element`'s `excluded_repeats` kept from the committed record. Written: `_dev/research/jioh/task-9.8-browser-comms/campaign/results-control/pool-element.json`, `pool-steam.json`.
- `control_report.py desktop <scratch>/r916/views/ctl-desktop … --control-pool` (the four pools): `results-control/control.json` equal leaf for leaf (1,205) to the committed record plus an empty `no_ratio` per archetype; `results-control.md` byte-identical (not rewritten). `renderer-hidden`'s reading stays 14 intervals, about 0.7 by chance, largest |z| 5.12. The library's notes unchanged (desktop fold-in regeneration test passes).

### repro M6 / D5 — the three session probes released

- **Release**: tag `meas-ci-probes-2026-09-23`, "meas-ci probes 2026-09-23 — 9.9 session long-phase probes", target `b51df8a4` (HEAD, on `origin/jioh/dataset-rebuild`: it holds `session/within_run.py`, `size_steady.py`, `within-run.json` and the 9.9 record), published 2026-10-17T10:51:05Z, https://github.com/logis11/LLM_driven_shceduling/releases/tag/meas-ci-probes-2026-09-23. Notes: `<scratch>/d916/rel/notes.md`.
- **Form**, as `meas-ci-probes-2026-09-20` and `-10-05` (looked at with `gh release view`): each landed job's final artifact re-zipped with its files at the archive's root, as `<artifact>-<run id>.zip`; the gated jobs' `report.json` and `report.kv` in `gated-reports.zip`, one folder `<artifact>-<run id>/` each; notes with the observation and a probe | archive | phases table, builds, what each archive holds, machine draws, reading them; not repeats, no campaign tag, the tooling commit named. The tag date is the day the probes ran (2026-09-23 in UTC and KST alike: 08:53, 12:33 and 12:53 UTC).
- **Artifacts** (runs 35839696453, 35861267312, 35863364163, `meas-session.yml`, commits `2077d902`, `1de44e78`, `137bb904`), downloaded through `gh api …/actions/artifacts/<id>/zip`, each local SHA-256 equal to the API's digest: landed `meas-session-session-r36-probe` (id 10750770783, 84,741,770 B, `d2c92c08…`), `-r41-probe` (10762689712, 86,887,632 B, `ba8ef9c9…`), `-r44-probe` (10763703557, 84,499,143 B, `e7c9fca6…`); gated r37, r38, r39, r40, r42, r43, r45, r46 (1,668–1,711 B each; all `wrong-machine`: AMD EPYC 9V74 ×4, Intel Xeon Platinum 8573C, AMD EPYC 9V45 ×2, Intel Xeon 6973P-C). Each landed artifact's 74 files are identical (`diff -r`) to the audit's copy; the intermediate `…-at-<step>` uploads are not released.
- **Check**: `session/within_run.py <9.9 pooled.json> <the three extracted archives> --json` reproduces `_dev/research/jioh/task-9.9-daemons-session/campaign/results/within-run.json` leaf for leaf (50 leaves, exit 0).
- **Assets** (each re-extracted and `diff -r` equal to the artifact; local SHA-256 and size equal to GitHub's `digest` and `size`): `meas-session-session-r36-probe-35839696453.zip` 84,537,886 B `b5b1cd51de88873c2cb4dc7203f312606faabcbbd69e85ca197f24e0f6b1ee4e`; `meas-session-session-r41-probe-35861267312.zip` 86,682,025 B `66f3e7588b1f4bfc2a23c8df19631e839c85ae04a6a6fd885582ad6ed24e5fad`; `meas-session-session-r44-probe-35863364163.zip` 84,297,785 B `285a9014759fcf6d3c234d79fbe414c990854e59de123720664d70ceebfdd0e1`; `gated-reports.zip` 8,512 B `e19e2057ea6a6d8065bf64f3314b032234e3425f0f3a1040aa241fd5bc22b184`.
- **Named in the 9.9 record**: `_dev/research/jioh/task-9.9-daemons-session/campaign/method.md:95` (a dated amendment line) and `changelog.md` (a closing entry, "The long-phase probes released (2026-10-17, 9.16 decision D5)", no new 9.9 decision). `dataset/meas-releases.yaml` maps campaign tags only and holds no probe release (as for the other probe releases), so it is not changed. The other places probe releases are listed are under `docs/` (`docs/workload/measurement-overview.md`'s release paragraph, the dataset guidebook vol-06): F's.

### repro M7 — the 9.7 release's gated reports (bookkeeping)

- `_dev/research/jioh/task-9.7-background-io/campaign/machine-draws.md:13`: a paragraph stating that `7z-pooled.json`'s `gated_out` lists 8 jobs (35475673566 r1, r2, r3, r6; 35475892675 r1, r2; 35475946669 r1, r2) while `meas-ci-background-2026-09-19`'s `gated-reports.zip` holds 7 `7z` reports (35475673566 r1, r2, r3, r6, and the dry-run and probe jobs 35425404685 r1, 35425432178 r1, 35431588969 r2), the four of runs 35475892675 and 35475946669 not in it; `gated_out` is bookkeeping and the re-pool keeps the record's list. The release was not changed.

### repro M8 — the 9.5 control's `code` pool

- `_dev/research/jioh/task-9.5-interactive-typing/campaign/results-control/pool-code.json`: HEAD's `campaign/pool.py --control` over the control release (`<scratch>/r916/out/ctl-pool-code.json`; `campaign/pool.py` and `analyze.py` unchanged since 2026-10-05): one leaf moves, `stability.window_limit` 44 → 57 (9.5 D99); 9,406 of 9,407 equal.

### meas-new C3 — the stability ledger script committed

- `_dev/research/jioh/task-9.16-exit-audits/meas-new/stability_ledger.py` moved to `dataset/tools/meas/stability_ledger.py` (docstring's `_repo` line restated for the one place it now runs from); `dataset/tools/meas/README.md:25`, the row after `stopping.py`. Run from `<scratch>/d916` with the moved script: its JSON equals `meas-new/out/stability-ledger.json` leaf for leaf (5,902) and its page equals `meas-new/out/stability-ledger-output.md` — the re-pools of M1 move no count (406 values, 369 met, 37 carried under a class, largest ±61.3 %). `meas-new/stability-ledger.md:3` notes the move. The docs chunk's citation of the research-folder path (measurement overview §7) is F's to update.

### `archetypes.yaml` text

Hand-written entries, edited in the library; generated ones changed in their fold-in tool and checked by the regeneration tests.

- `game-task-chain` (hand-written): `validation_stats.reason` (`:1754–1755`) "Proton is documented only as a tool for use with the Steam client" (the guidebook's quoted words); D-F1-19 (`:1758–1760`) "the deck names no trace tool (perf sched record is what Min's later analysis tool, VaporMark, reads, as edge-lwn26 reports his LPC 2025 session)"; D-F1-12 (`:1793–1795`) "scx_lavd's source comment divides a 15 ms targeted latency among 10 runnable tasks, 1.5 ms each, scx" (R02:96, `main.bpf.c:69–72` at scx `8b24795`) in place of "the deck's slice example 1.5 ms"; D-F1-14 and handed F3 (`:1828–1835`): six members carry the process name `Troy.exe` by our rule (a Wine thread that sets no name keeps its process's comm, 9.10 D26), slide 16 showing one node; `declared_class normal` is design — the 9.13 rebuild's default, `lavd-ossna24` recording no class and the 9.11 census no measurement.
- `compiler-child` (hand-written), D-F3-02 (`:1034–1037`): the literature grounds only that a parallel build forks and execs many processes, mostly short-lived; O'Callahan's count is every process a `make -j8` DynamoRio build forks and execs, not what they run.
- `module-build-orchestrator`, `module-compiler-child` (hand-written), D-F3-29 (`:1128`, `:1298`): "the open kernel module of NVIDIA's 595 branch (`XB-Support: PB` in Ubuntu's control file; D47)"; D-F3-08 (`:1135–1136`, `:1305–1306`): "9.6 D4's `nproc` rule applied to an eight-thread desktop, convention" in place of "D4's eight-thread desktop, design" (the bare "D4" in a 9.10 scope read as 9.10 D4, which is the module rebuild's decision).
- `renderer-hidden` (generated, `desktop/fold_in.py` `GRACE` `:88–92`), D-F4-43: "330 s of the documented grace (five minutes while loading, 60 s once loaded)" in place of "the documented five-minute default"; `:738`. M4, M9, F1 above.
- The four typing scopes (generated, `campaign/fold_in.py:457–459`), class F3: "minus the idle rate, bounded below by zero (a window quieter than the idle rate carries no input work)"; `:111`, `:184`, `:355`, `:494`.
- Fold-in regeneration tests (`test_meas.py`, `test_meas_desktop.py`, `test_meas_session.py`, `test_measured_fidelity.py`, `-k regenerat`): 4 passed on the edited library.

### `dataset/sources.yaml`

- `swell-kw` (`:49–52`), D-F2-04: `outlook-c23` "blocks 2 and 3 — the e-mail-interruption and time-pressure conditions, in counterbalanced order; no block-1 keystrokes".
- `ocallahan-atc17` (`:88–91`), D-F3-02: grounds only that a parallel `make` build forks and execs many processes, mostly short-lived (a DynamoRio build; the paper does not say what they run).
- `steam-downloads` (`:144–148`), D-F1-27: the check box and the default pause at FAQ 4F9E-6328-E9B8-47F9, the per-game setting at FAQ 71AB-698D-57EB-178C.
- `gonzalez-chi04` (`:165–166`, `:171`), D-F2-12: "14 shadowed information workers"; and D-F2-10, which the W chunk left to this chunk ("formal meetings, unknown and personal events excluded", B1's WORDING-FIX).

### `dataset/grids.yaml` — "debounce" (D-F1-46)

- `:56–61`: the flap-stress comment names the three intervals as GameMode's reaper check interval, tuned's dynamic-tuning update interval (dynamic tuning off by default) and systemd-oomd's pressure sustain duration, in place of "the debounce values". No other "debounce" in `dataset/` or `harness/` outside `docs/`.

### Timelines and `bound-values.md`

- `dataset/timelines/coreset/c2-p3a.timeline.yaml:5–8` and `c2-pairs.variant.yaml:62–65` (the `c2-p3b` recipe comment), D4: the backup, 165.7 s of CPU in the about 166 s of lane the editor leaves, finishes about 0.3 s before the segment's end and is scored by its turnaround (9.14 decision 6's header rule; 9.16 D4), in place of "does not end inside it and is scored by progress". The derived `c2-p3b.timeline.yaml` carries no comment and does not change.
- D-F3-08: `source: {parallelism_cap: design}` → `convention` in `c1-compile.timeline.yaml:22`, `c3-workday.timeline.yaml:40`, `c6-dual.timeline.yaml:30`, `c7.variant.yaml:241`; the derived `c4-compile.timeline.yaml:40` and `c7-compile.timeline.yaml:43` follow through `derive.py`; the generated layer copies the label (`tests/test_generated.py:71` now expects `convention`). `_dev/research/jioh/task-9.10-scenarios-timelines/bound-values.md:27`: "convention: the `nproc` rule applied to an eight-thread desktop (9.6 D4's label; relabelled 2026-10-17)".
- Also the timeline comments the W chunk left to this chunk: `c3-evening.timeline.yaml:2` "The order is design; no source defines it." (D-F4-49); `c3-creation.timeline.yaml:3` points the background encode to BAPCo's whitepaper v1.2 §2.2 in `sysmark30` (D-F4-21); `c6-dual.timeline.yaml:32–33` "the 2026-09-13 verification's C-gonzalez-1, cited by 9.10 D35" (the pointer slip).

## Rebuild

The build on disk verified against the committed manifests before the rebuild (`tools/check_build.py`: "build verified (3304 files, 7 manifests)"), then cloned with `dataset/generated/` and the manifests to `<scratch>/d916/before/`.

`make -C dataset lint PY=…`: "lint clean" (before and after). `make -C dataset dataset variants generated PY=…`: exit 0, 6 min 30 s (the SteamCMD re-pool running beside it): 51 core artifacts, 78 variants, 480 / 720 / 24 / 272 / 66 generated. `derive.py` rewrote the derived `c4-compile` and `c7-compile` timelines (the `parallelism_cap` label).

Manifest SHA-256, before → after:

| manifest | before | after |
|---|---|---|
| `build.manifest.json` | `0f0af422d4dd92282903342b51cd6617d704d3cad9488d350388a47d7ff3417f` | `8e1eb7530b32378e3c5c76e449bf367b4962b9138b62dc7404c6df4b8d525837` |
| `build.variants.manifest.json` | `cdc143191fcd28aec80595e3060f4f391c91ba52c341e076043589124bb579f6` | `8e2948b18812a546375ccd1f67d61604ee06c51d87060b8a1a48f5aa6cd0f1a4` |
| `build.transition-grid.manifest.json` | `d84fb68af6fdd27baa08ec66739261747c195d2cf870ac9cb07b821c6353083d` | `01e539eec0a6761c677be3c981b7e45833941e9027393c15f19d2075e0167d68` |
| `build.return-grid.manifest.json` | `a6980482dd548f9fe8d4459ce4f5791ec348fac4f9b4fb7901301a1c83312512` | `2d80cff9e9d85cc4fda97953c09a98f9ff12018914455582b6ad42b95646b683` |
| `build.flap-stress.manifest.json` | `92676677007174e875ea68013c1f5e435ef8cba0f8a574888534d917c177bbdf` | `53420ed5f5d1c205c55c56585c6fb2dd69ff13b64444991c2278f2aa786ed707` |
| `build.distractor-grid.manifest.json` | `1d129a51621f1f40094d247013f794c28caaab7fea3d404730e8a205c4984fe5` | `21502219709c9d5832f495702ad938dcd0b880d06960f4b7d6d243d9b373348e` |
| `build.familiarity-ladder.manifest.json` | `8c38e7a87c391b88819f9f72e1a6d0eea04f44e954b44fa06a83e58b68e2d6ca` | `1dd08130d242334a6fa26f7afc8149b8d69f6b1c9da6c384429054cd44f5f954` |

`dataset/coverage-grid.json` unchanged (`4c35216ebb97222195afa84332b78845b385a0feb826cca5a1598f7caace9950`).

**Which artifacts' bytes changed** (each changed artifact loaded before and after, `meta` set aside and compared; every manifest section compared; `<scratch>/compare_build.py`, output `<scratch>/d916/compare.txt`): every artifact's bytes change, all in `meta` alone — no compiled workload (tasks, events, ground truth) changes anywhere.

- Core (51): `meta.sampled.archetypes` (the library's hash) in all 51; `meta.derived_from` in the 8 whose timeline's bytes moved (`c1-compile`, `c2-p3a`, `c3-creation`, `c3-evening`, `c3-workday`, `c4-compile`, `c6-dual`, `c7-compile`). Changed `inputs`: `dataset/archetypes.yaml`. `demand` and `reports` unchanged.
- Variants (78): `sampled.archetypes` in all, `derived_from` in 12 (the variants of those files). Changed `inputs`: `archetypes.yaml`, `build.manifest.json`.
- Generated: `sampled.archetypes` in all; `derived_from` where the composed timeline carries the compile set's relabelled `parallelism_cap` — transition grid 60 of 480, return grid 90 of 720, distractor grid 32 of 272, familiarity ladder 6 of 66, flap-stress 0 of 24. Changed `inputs` of each: `archetypes.yaml`, `grids.yaml` (the comment), `timelines/coreset/c1-compile.timeline.yaml`. `grid`, `demand`, `reports` unchanged.

## Re-pin and bless

- `harness/experiments/rq0-gate.yaml:516` `pins.dataset` → `8e1eb753…`, `:518` `pins.variants.all` → `8e2948b1…`; `:510`'s comment "the 9.16 entries". The scoring spec (`f7d1df4c…`), guard spec 1.2 (`c2dad06f…`) and driver table (`e1155a72…`) pins unchanged. The RQ0 gate spec pins no generated manifest; the five are in the changelog entry.
- `harness/CHANGELOG.md`: one 2026-10-17 entry at the top, in the 9.15 rebuild entries' form — the core set, the measurement tools and records, the pins and the five generated manifests' hashes, what moved in the artifacts, pointers.
- The bless is the seven manifests and the two derived timelines committed as they now stand. No separate dataset changelog exists: the earlier rebuilds (9.15's B1, B4; 9.18; 9.17) recorded the bless in the harness changelog entry and their logs, and this chunk does the same. The dataset guidebook vol-07's re-pin tables are `docs/` (F's).

## Checks

- `make -C dataset lint`: "lint clean", exit 0.
- `make -C dataset test`: 551 passed, 1 skipped, exit 0 (2 min 36 s) — 9.15 B4's 544 and this chunk's seven new tests.
- `make -C dataset check`: exit 2, as before every bless: `derive.py --check --require-coverage` passes (67 segments on the grid, no derived-timeline drift against the working tree, coverage grid equal); `check_build.py` reports exactly 9 "differs from the committed one — re-bless" errors, the seven manifests and the derived `c4-compile.timeline.yaml` and `c7-compile.timeline.yaml`. No hash, missing-file or unpinned-file error. It passes once these nine are committed.
- `make -C harness lint`: exit 0 (3 min 29 s) — `lint.py`, `scoring_lint.py` (49 files, 75 terms; generated terms 1,320 / 2,865 / 248 / 374 / 104, as before), `guards_lint.py` (guard spec 1.2), `experiment_lint.py` (`rq0-gate.yaml`: 3 conditions, 19 judging + 32 reporting files, `k_of_n_gap`) all clean.
- Fold-in check modes: `batch_fold_in.py --check` exit 0; `replay_fold_in.py <scratch>/raw --check` exit 0; `desktop/launch_fold_in.py --check` exit 0 on `meas-ci:desktop:2026-10-04b` (the eight subjects' view), `-10-05` and `-10-05b` (the re-analysed landings, 9.10 D155); the desktop, campaign, session and measured-fidelity regeneration tests pass inside `make test`.

## Not done here, for F or later

- The docs that quote the moved pins and hashes, the ledger script's research-folder path, the new release and the corrected figures (−7.8 %, `MemoryInfra`'s 3.6 / 2.4, the 12 renderers' share) — `docs/`, F's list.
- `dataset/README.md:150` already carries the W chunk's interval wording; not touched.
- `c3-creation.timeline.yaml:3` was left one long comment line (the whitepaper pointer) rather than re-filled after the rebuild had compiled it.
- The repro notes' launch-stream remark (a README line on re-running `launch.py analyze` for `renderer-hidden`'s repeats 2 and 5) and the cosmetic `tag: ''` of the control pools: not findings, not done.

## Paths changed by this chunk (for an explicit-path commit)

Not in this list, and not to be staged with it: the `docs/` edits, `dataset/README.md` and `harness/guards/README.md` (the docs chunks'), and `_dev/research/jioh/task-9.16-exit-audits/{decisions.md, meas/repro-findings.md, docs-brief.md, followups.md, logs/G.md, logs/P.md, logs/R.md, logs/W.md}` (the lead's and the other chunks'). `meas/repro-table.md` was already modified before this chunk; this chunk changed its rows 38 and 54.

Dataset and harness:

```
dataset/archetypes.yaml
dataset/sources.yaml
dataset/grids.yaml
dataset/build.manifest.json
dataset/build.variants.manifest.json
dataset/build.transition-grid.manifest.json
dataset/build.return-grid.manifest.json
dataset/build.flap-stress.manifest.json
dataset/build.distractor-grid.manifest.json
dataset/build.familiarity-ladder.manifest.json
dataset/timelines/coreset/c1-compile.timeline.yaml
dataset/timelines/coreset/c2-p3a.timeline.yaml
dataset/timelines/coreset/c2-pairs.variant.yaml
dataset/timelines/coreset/c3-creation.timeline.yaml
dataset/timelines/coreset/c3-evening.timeline.yaml
dataset/timelines/coreset/c3-workday.timeline.yaml
dataset/timelines/coreset/c4-compile.timeline.yaml
dataset/timelines/coreset/c6-dual.timeline.yaml
dataset/timelines/coreset/c7-compile.timeline.yaml
dataset/timelines/coreset/c7.variant.yaml
dataset/tools/meas/README.md
dataset/tools/meas/batch_fold_in.py
dataset/tools/meas/burstiness.py
dataset/tools/meas/campaign/fold_in.py
dataset/tools/meas/campaign/span_probe.py
dataset/tools/meas/control_report.py
dataset/tools/meas/desktop/fold_in.py
dataset/tools/meas/stability_ledger.py
dataset/tools/meas/stopping.py
dataset/tools/meas/windows.py
dataset/tools/tests/test_generated.py
dataset/tools/tests/test_meas_burstiness.py
dataset/tools/tests/test_meas_span_probe.py
dataset/tools/tests/test_meas_stopping.py
dataset/tools/tests/test_meas_windows.py
dataset/tools/tests/test_measured_fidelity.py
harness/CHANGELOG.md
harness/experiments/rq0-gate.yaml
```

Research records:

```
_dev/research/jioh/measurement-campaign-record.md
_dev/research/jioh/task-9.5-interactive-typing/campaign/results-burstiness.md
_dev/research/jioh/task-9.5-interactive-typing/campaign/results-burstiness/burstiness.json
_dev/research/jioh/task-9.5-interactive-typing/campaign/results-control/pool-code.json
_dev/research/jioh/task-9.5-interactive-typing/campaign/results-stopping/stopping.json
_dev/research/jioh/task-9.5-interactive-typing/campaign/results-windows.md
_dev/research/jioh/task-9.5-interactive-typing/campaign/results-windows/windows.json
_dev/research/jioh/task-9.7-background-io/campaign/machine-draws.md
_dev/research/jioh/task-9.7-background-io/campaign/results-7z.md
_dev/research/jioh/task-9.7-background-io/campaign/results-steamcmd.md
_dev/research/jioh/task-9.7-background-io/campaign/results/7z-pooled.json
_dev/research/jioh/task-9.7-background-io/campaign/results/steamcmd-pooled.json
_dev/research/jioh/task-9.8-browser-comms/campaign/results-burstiness.md
_dev/research/jioh/task-9.8-browser-comms/campaign/results-burstiness/burstiness.json
_dev/research/jioh/task-9.8-browser-comms/campaign/results-control/control.json
_dev/research/jioh/task-9.8-browser-comms/campaign/results-control/pool-element.json
_dev/research/jioh/task-9.8-browser-comms/campaign/results-control/pool-steam.json
_dev/research/jioh/task-9.8-browser-comms/campaign/results-windows.md
_dev/research/jioh/task-9.8-browser-comms/campaign/results-windows/windows.json
_dev/research/jioh/task-9.9-daemons-session/campaign/method.md
_dev/research/jioh/task-9.9-daemons-session/changelog.md
_dev/research/jioh/task-9.10-scenarios-timelines/bound-values.md
_dev/research/jioh/task-9.10-scenarios-timelines/campaign/mnist/results/pooled.json
_dev/research/jioh/task-9.10-scenarios-timelines/campaign/mnist/results/results.md
_dev/research/jioh/task-9.10-scenarios-timelines/campaign/tracker/results/pooled.json
_dev/research/jioh/task-9.10-scenarios-timelines/campaign/tracker/results/results.md
_dev/research/jioh/task-9.10-scenarios-timelines/campaign/upgrade/results/pooled.json
_dev/research/jioh/task-9.10-scenarios-timelines/campaign/upgrade/results/results.md
_dev/research/jioh/task-9.10-scenarios-timelines/campaign/renderer-hidden/results/results.md
_dev/research/jioh/task-9.10-scenarios-timelines/campaign/renderer-hidden/results/windows.json
_dev/research/jioh/task-9.10-scenarios-timelines/campaign/renderer-hidden/results/windows.md
_dev/research/jioh/task-9.10-scenarios-timelines/campaign/renderer-hidden/results/windows-split-residual.json
_dev/research/jioh/task-9.10-scenarios-timelines/campaign/renderer-hidden/results/windows-split-residual.md
_dev/research/jioh/task-9.10-scenarios-timelines/campaign/spans/results/results.md
_dev/research/jioh/task-9.10-scenarios-timelines/campaign/spans/results/renderer-hidden-past600.level.json
_dev/research/jioh/task-9.16-exit-audits/meas-new/stability_ledger.py   (deleted: moved to dataset/tools/meas/)
_dev/research/jioh/task-9.16-exit-audits/meas-new/stability-ledger.md
_dev/research/jioh/task-9.16-exit-audits/meas/repro-table.md   (rows 38, 54)
_dev/research/jioh/task-9.16-exit-audits/logs/D.md
```
