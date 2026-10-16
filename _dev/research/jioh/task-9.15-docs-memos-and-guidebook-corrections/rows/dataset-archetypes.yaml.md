# Work-list rows — `dataset/archetypes.yaml`

No chunk: a data file, outside the sweep; its rows are applied in a batched rebuild. 1 open row. The file has 1946 lines at `221e25b5`.

### W-0948 · open
- At: `dataset/archetypes.yaml`, the measured entries' scopes on the trace: `renderer-hidden`, `chat-client` and `game-client` ("perf sched record on that CPU", the text `dataset/tools/meas/desktop/fold_in.py:43` writes); the build, batch and background entries ("`perf sched record` … on the measured CPU"); the session entries say "on every CPU"
- Change: 인지오's call: (a) leave it — the record does cover the measured CPU; (b) restate the scopes to the run scripts' recording at the next library rebuild: every run script records with `perf sched record -a`, started on the harness CPUs, the subject pinned to the measured CPU. Under (b) the desktop fold-in's text changes with the library, or `test_meas_desktop.py`'s regeneration test fails.
- Final word: the run scripts: `dataset/tools/meas/campaign/run.sh:152`, `dataset/tools/meas/desktop/run.sh:127`, `dataset/tools/meas/background/run.sh:212`, `dataset/tools/meas/build/run.sh:106`, `dataset/tools/meas/session/run.sh:116` (F2's decision 2; the code first, 9.15 spec decision 3).
- Sources: `logs/F2.md` ## Rows for other chunks (X2), ## Decisions 2
- Cross-ref: W-0884
- Notes: found in F2. No value moves either way. A manifest input: under (b) every manifest re-blessed and the RQ0 gate spec's `pins.dataset` and `pins.variants` re-pinned.
