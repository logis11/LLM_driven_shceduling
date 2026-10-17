# Work-list rows — `dataset/archetypes.yaml`

No chunk: a data file, outside the sweep; its rows are applied in a batched rebuild. 2 open rows. The file has 1946 lines at `221e25b5`.

### W-0948 · applied (2026-10-17, the second data rebuild; `logs/B4-data-rebuild.md`)
- At: `dataset/archetypes.yaml`, the measured entries' scopes on the trace: `renderer-hidden`, `chat-client` and `game-client` ("perf sched record on that CPU", the text `dataset/tools/meas/desktop/fold_in.py:43` writes); the build, batch and background entries ("`perf sched record` … on the measured CPU"); the session entries say "on every CPU"
- Change: 인지오's call: (a) leave it — the record does cover the measured CPU; (b) restate the scopes to the run scripts' recording at the next library rebuild: every run script records with `perf sched record -a`, started on the harness CPUs, the subject pinned to the measured CPU. Under (b) the desktop fold-in's text changes with the library, or `test_meas_desktop.py`'s regeneration test fails.
- Final word: the run scripts: `dataset/tools/meas/campaign/run.sh:152`, `dataset/tools/meas/desktop/run.sh:127`, `dataset/tools/meas/background/run.sh:212`, `dataset/tools/meas/build/run.sh:106`, `dataset/tools/meas/session/run.sh:116` (F2's decision 2; the code first, 9.15 spec decision 3).
- Sources: `logs/F2.md` ## Rows for other chunks (X2), ## Decisions 2
- Cross-ref: W-0884
- Notes: found in F2. No value moves either way. A manifest input: under (b) every manifest re-blessed and the RQ0 gate spec's `pins.dataset` and `pins.variants` re-pinned.

### W-0989 · applied (2026-10-17, the second data rebuild; `logs/B4-data-rebuild.md`)
- At: `dataset/archetypes.yaml` `video-editor`'s scope, the idle phase's probe sentence, line 607 ("over 2,790 s of one long-phase probe past that settle, a 180 s phase holds its CPU within 1.1 % and its wakes within 0.7 % … within 4.6 % and 3.9 % at the worst")
- Change: Restate to the 9.15 probe: `kdenlive` 13 of the `long-probe` family, run 38976976741, release `meas-ci-probes-2026-10-17`; 3,100 s past a 30 s settle and 2,890 s past the 240 s settle, read over the 2,851 s `c3-creation` holds the idle state (2,860 s in whole 10 s slices); at the placement every repeat takes, CPU within 0.3 % and wakes within 2.9 %; at the worst, 4.5 % and 3.8 %.
- Final word: 인지오's answer (a) of 2026-10-17 to K06 (M6) (re-measure; the scope restated); `logs/M6-reprobe.md`; this folder's `campaign/spans/results/video-editor-idle.level.json` (`held_past_settle_s` 2890, `span_s` 2860; CPU placement −0.0029, worst +0.0448; wakes placement +0.0292, worst +0.0383); `dataset/timelines/coreset/c3-creation.timeline.yaml` (arrive 120 s, depart 3,212 s) with the 240.6 s launch replay (`dataset/tools/wlc/compiler.py:307`). The 180 s phase holds, so 9.10 D146's phase length does not reopen and no value changes.
- Sources: `logs/N4.md` ## Rows for other chunks (X1), ## Code-versus-decision mismatches (M1)
- Cross-ref: W-0948; W-0990; W-0991
- Notes: found in N4 (its X1 and M1, one row). A manifest input: in the library rebuild with W-0948 — every manifest re-blessed, the RQ0 gate spec's `pins.dataset` and `pins.variants` re-pinned, `make check` passing.
