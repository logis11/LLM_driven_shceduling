# Task 9.13 — changelog

One entry per change applied in the rebuild (`dataset/archetypes.yaml`, `dataset/schema/workload.schema.json`, `dataset/tools/`, `dataset/timelines/coreset/`, `dataset/build.manifest.json`, `dataset/coverage-grid.json`, `dataset/README.md`, `docs/data-contracts.md`): what changed, old state, new state, the decision it applies (spec `_dev/docs/spec/jioh/task-9.13-rebuild.md`) or the label, commit. Each entry names what it hands to 9.14, 9.15 or 9.16. The reads 9.13 made with no value changed are in `reads.md`.

## D1 — the native compile mode dropped (2026-10-09)

Spec decision 5 (9.5 spec decision 14). `dataset/tools/wlc/compiler.py`: the mode list `("native", "single")` → `("single",)`; the lane-scaling pass is the only pass, and a request for `native` is refused. The compiler, the lint and the manifest know one mode; the directory keeps the name `coreset-single`. Tests: the native/single comparison tests of `tests/test_invariants.py` replaced by the single-mode test and the lane-share test; `tests/test_canonical.py` and `tests/test_lint.py` iterate the mode list and drop the native exemption. No value changed.

Hands to 9.15: every doc naming `coreset-native` (`docs/workload/coreset-guide.md:298`, `docs/workload/building-plan.md:28`, `_dev/docs/rq0-preparation-notes.md:47`, the TODO's Phase 1–2 lines are history).

## D2 — `declared_class` on every library entry and every task record (2026-10-09)

Spec decisions 2 and 8 (9.11 D4–D6, D16, D18, D34). `dataset/archetypes.yaml`: every entry gains `declared_class` after `category_source` — `idle` on `file-indexer` and `incremental-backup`, `normal` on the other 26 (and on no entry by default); the header states the encoding rule. `dataset/schema/workload.schema.json`: a closed enum `declared_class` (`normal`, `idle`), required on `arrive_event` and on `spawn_entry`. `dataset/tools/wlc/compiler.py`: the build carries the bound entry's class onto each `arrive` event; the object jobs of `build-orchestrator` and the tree jobs of `module-build-orchestrator` carry their child entry's; the chain members carry `game-task-chain`'s. `dataset/tools/wlc/linter.py`: `declared_class` is a required entry field, its value checked against the closed set. Tests: `test_repo_lint_requires_declared_class`, `test_library_declared_classes` (`tests/test_lint.py`); `test_tasks_carry_their_entrys_declared_class`, `test_schema_requires_declared_class_on_every_task_record` (`tests/test_canonical.py`). Every compiled file's bytes change (the field, and the library hash in `meta.sampled.archetypes`); no measured value changed.

Hands to 인경민 (through 9.15's final memo): the field's name and place, the run file carries it with the events, the strict idle rule under every algorithm (9.11 D5, D18). Hands to 박이안 (the same memo): the visible projection shows the class per task (spec decision 3). Hands to 9.14: the six files that hold idle work read against the strict class (9.11 D16's list). Hands to 9.16: the class census (`_dev/research/jioh/task-9.11-scheduler-constants/classes/audit.md`) is the source of every entry's value.

## D3 — the TIMER-first canonical lint (2026-10-09)

Spec decision 8 (9.11 D11, D33). `dataset/tools/wlc/linter.py`, `lint_canonical`: over every task record — `arrive` events and spawn-table entries — a program that contains a TIMER anywhere must execute a TIMER first, descending LOOP heads; the error names the task and the op the program opens with instead. Tests: `test_timer_first_invariant` (six programs) and `test_timer_first_invariant_covers_spawned_tasks` (`tests/test_lint.py`). The current set passes (`reads.md` R2: 22 TIMER-carrying tasks, 7 through a LOOP head, 15 literally). No value changed.

Hands to 9.14: the harness reader's t₀ (`harness/tools/harness/reader.py`, `_task_info`) now rests on an enforced invariant (9.11 D11's pointer).

## D4 — `game-download-idle` and `c2-p2a-idle`, the bounding check's idle half (2026-10-09)

Spec decision 4 (9.11 D6, D20, D21). `dataset/archetypes.yaml`: a YAML anchor on `game-download` and a new entry `game-download-idle` that merges it — tables, lifetime, binding, scaling rule and validation record the same objects — overriding `declared_class: idle` and a modelling note stating its purpose. `dataset/timelines/coreset/c2-pairs.variant.yaml`: a variant `c2-p2a-idle` from `c2-p2a` by one op, the `download` task's archetype → `game-download-idle`; the deriver writes `c2-p2a-idle.timeline.yaml` (generated, committed) and `dataset/coverage-grid.json` (66 segments, all 32 cells still instanced). Sampling is keyed by task id, so the compiled file equals `c2-p2a` in every event, wake and ground-truth segment except the `download` task's class — `test_idle_download_variant_differs_in_the_class_alone` (`tests/test_coreset.py`); the scenario map of `test_every_segment_tags_the_scenarios_of_the_programs_it_shows` places the entry at S10, the download during play, as its base. No measured value changed.

Hands to 9.14: `c2-p2a-idle` is in the manifest and outside the judging set (`harness/experiments/rq0-gate.yaml:38` lists the set explicitly); the bounding check pre-registered on `c2-p2a` and `c2-p2a-idle`, each verdict reported, the difference the reach of 9.11 D6's limitation with D20's numbers. Hands to 9.15: `game-download`'s nice-10 limitation in the dataset docs names the pair.

## D5 — the indexer's and the backup's modelling notes restated to the declared class (2026-10-09)

Spec decision 11 (9.11 D16, D33). `dataset/archetypes.yaml`, `file-indexer` and `incremental-backup` `modeling_notes`: "the task model carries no declared class (9.11's)" → the entry carries `idle`, the executor's strict rule, nice not carried; the indexer's with its `background.slice` placement on the depicted desktop, where its slice gets about 23 % against the editor's, so the simulated indexer interferes less than the depicted one and the indexer files' headroom is understated; the backup's with its placement in the editor's own group, where the strict class matches the desktop; both with the idle I/O class not carried, the simulator scheduling one CPU lane. No value changed.

Hands to 9.14: the three indexer files' expected no-headroom reading is a consequence of the rule, not of the depicted desktop (9.11 D16). Hands to 9.15: the dataset docs describing the two entries.

## D6 — the contract doc, the memo and the dataset README (2026-10-09)

Spec decisions 6, 9 and 11. `docs/data-contracts.md`: §2 the archetype contract at v0.2 with the field stated and the two example entries carrying it; §4 the file path `coreset-single` alone, the three example `arrive` events and the spawn entry carrying the field, a paragraph on the field and the executor's rule, the run file carrying it to the simulator, the visible projection showing it per task with the example; §14 the dated entry naming the change, the agreement and the grounds; header `Updated` 2026-10-09. `docs/memos/2026-10-08-declared-scheduling-class.md`: one dated line under §1 naming the field and pointing to §14; `Updated` bumped. `dataset/README.md`: the layout (one compiled set of 51 files, the library at v0.2), the pipeline, the canonical-format example and its `declared_class` bullet, the coresets section (one set, 66 segments, the C2 count and the `c2-p2a-idle` paragraph), the generalsets' name, the tools map, two rules (declared class, TIMER first). The §2 archetype list and every other doc under `docs/` are left to 9.15.

Hands to 9.15: `docs/data-contracts.md` §2's "There are twelve (…)" list of archetypes, stale since the slices; `docs/README.md` needs no index change (no doc added, renamed or re-statused).
