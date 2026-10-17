# 9.16 — items for the data chunk (D) and the closing docs chunk (F)

## For D (dataset code and data, one rebuild)

- meas-new: `burstiness.py` and `windows.py` find the idle landings (`meas-interactive-kdenlive-r<k>-idle`; an `IDLE_MODE_95` entry in `control_report.py`).
- meas-new / repro M4: `renderer-hidden`'s window sentence (`desktop/fold_in.py` `WINDOWS_1005B`): 3.6× and 2.4× are `MemoryInfra` alone — state it as `MemoryInfra`, one of the residual's two comms.
- class F1: `renderer-hidden`'s CPU share is the 12 renderers' total (`desktop/fold_in.py:285–286`, `:111`): give one renderer's share (divide by `renderers_measured`) or name it the 12 renderers' share; the same in `measurement-campaign-record.md:510` and the 9.10 renderer `results.md:15`.
- class F2 / repro M3: `stopping.py` reads both of `video-editor`'s pools (idle values from the idle pool, other phases from the main pool); regenerate `results-stopping`; update `tests/test_meas_stopping.py`.
- class F6: `batch_fold_in.py` writes `tail_work`.
- repro M1: re-pool the four records with HEAD's `background/pool.py` (schema fields only).
- repro M5: `windows.py desktop_entries` iterates the folded set; regenerate 9.8 `results-windows`.
- D6 / repro M2: `control_report.py`'s `renderer-hidden` control reads 9.8's pool; regenerate the 9.8 `control.json`, `results-control.md`, the two control pools.
- D5 / repro M6: publish probes 36, 41, 44 as a `meas-ci-probes-…` release (form of the other probe releases); name it in the 9.9 record.
- the rest of `repro-findings.md` (M7 on) once the resumed audit reports.
- meas-new C3: move `stability_ledger.py` to `dataset/tools/meas/`, a row in its README.
- `archetypes.yaml` text (through the fold-in code where generated): D-F1-12 (1.5 ms from `scx_lavd`'s source comment), D-F1-19 (`perf sched record` from the later report, `edge-lwn26`), D-F1-14 (six `Troy.exe` members by the naming rule), `game-task-chain`'s reason exactly "Proton is documented only as a tool for use with the Steam client" (the guidebook quotes these words), `game-task-chain`'s `declared_class: normal` labelled design (the 9.13 default; its source records no class), D-F3-02 (O'Callahan counts all processes `make -j8` forks), D-F3-29 ("production branch" undefined in the read copies), D-F4-43 (the grace: five minutes while loading, 60 s once loaded), class F3 (the `input_run` zero floor in the four typing scopes) where in the library.
- `dataset/sources.yaml`: D-F1-27 (FAQ 71AB), D-F2-04 (one interruption block, one time-pressure block), D-F2-12 ("information workers"), D-F3-02.
- `dataset/grids.yaml` and anything else carrying "debounce" for the 5/10/30 s intervals (D-F1-46).
- timelines: `c2-p3a.timeline.yaml` head comment and `c2-p3b`'s recipe comment (the backup finishes; turnaround, D4); every `source: {parallelism_cap: design …}` → convention (decisions.md, D-F3-08) and `_dev/research/jioh/task-9.10-scenarios-timelines/bound-values.md` likewise.
- rebuild, re-bless, re-pin (RQ0 gate spec dataset/variants pins), harness CHANGELOG entry, home gate, CI.

## For F (after D)

- pins and manifest hashes everywhere they are quoted (dataset, variants, generated sets, scoring spec now `f7d1df4c…`, guard spec 1.2 `c2dad06f…`, driver table `e1155a72…`).
- the stability-ledger script path → `dataset/tools/meas/stability_ledger.py` (measurement-overview §7, the validity memo, `docs/README.md`, the final memo's 정정, dataset guidebook vol-06:1554).
- review R/G blocking: vol-06:1332 → 관례 (the `nproc` rule); G/02:437 box restated (9.6 D4 labels it convention, 9.10 D160's listing had design); G/03:451 label counts and :721 quote after the relabel; G/02:712, G/06:1318, G/02:1333 checked against D's exact words; vol-01:2094 and the :3338 cell cut back to what S2-54 records (0–31 levels, round-robin within a level, boosts) unless a read record of the priority-class passage is added.
- review R/G non-blocking: vol-08 9.16 entry headings carry the date; D6 glosses "untraced control"; G/04:241 labels the 4-in-10 arithmetic; superlatives at vol-02:3208, vol-05:1866, :2004; vol-01:3077 rt-app's default re-anchors (vol-06:460); vol-06:1735 "30장의 슬라이드"; vol-02:3484/:3486 duplicate, :3362 wording; G/02:1333 full path; the dataset guidebook's remaining work-list ids (G/01:96, :843, :1005; G/04:1917, :1932; nine in G/07).
- review W/P non-blocking: pair review :61, :81 "arithmetic"; measurement-overview :108 (9.8 D15 is the long-phase probe decision); trace-clarifications memo :97 names `c2-p2a`/`c2-p2b`; grounding-sources :59 to S3-08's columns; the three redundancies (overview :51, source-vetting :162, harness guide :517); `dataset/README.md:150` connective; references.md :239 PCMark 10's open-source programs.
- coverage gaps: B-02, B-05 (`docs/harness/metrics.md:258`, `:264`); B-25 (`rq0-gate.yaml:170` "about 1.4 schedules per wake" labelled arithmetic on slide 14's share); A-64 read record (`lavd.bpf.h:77` `LAVD_SLICE_BOOST_MAX`, `main.rs:220–222` at scx `c8728c6b`) saved under this folder's `reads/`; `fiedler-gaffer04`, `mpv`, `chromium` status lines → `reads/B4-reads.md` T-02.
- record-only: R's D-25 (slide-10 quote), D-44 (six ananicy rule lines), D-46 (`Xorg`/`dbus-daemon` rules) — cite B1/B2 reads where they hold the passage, else restate to what a record holds.
