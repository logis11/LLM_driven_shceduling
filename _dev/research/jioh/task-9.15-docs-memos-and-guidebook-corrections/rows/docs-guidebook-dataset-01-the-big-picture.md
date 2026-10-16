# Work-list rows — `docs/guidebook/dataset/01-the-big-picture.md`

Chunk K11, Dataset guidebook, volumes 1-2 (wave 3). 24 open rows. The file has 1631 lines at `d5cc7711`.

### W-0483 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §1.1 line 49 (the claim quotation '이름 whitelist는 되찾지 못한다'); §1.3 the conditions table line 83 and line 87; §1.5 line 134 (RQ2's '`fixed`, `whitelist`'); §2.10 line 440; §5.2 line 939 (C1 quoting the building plan); §9.2 glossary lines 1494 and 1496
- Change: Restate every `whitelist` mention to the two conditions, `shipped_catalogue` and `strongest_name_table`: the conditions table (line 83) gets the two rows and loses '오늘의 OS가 하는 일(Game Mode)'; RQ2 (research question 2) is answered against the shipped catalogue; the glossary's `condition` list and its `whitelist` entry follow. The quotations at line 49 (`docs/research-claims.md`) and line 939 (the building plan's C1, the calibration group) follow their source docs' restated sentences.
- Final word: 9.12 D6 as amended by D91, D105, D109 and D115: the `whitelist` condition becomes two. The shipped-catalogue condition (`shipped_catalogue`) reproduces the CachyOS catalogue (`ananicy-rules` at `03ef03fb`) as CachyOS installs and enables it with ananicy-cpp, matched by the basename of each process's `argv[0]`, untruncated (D105); on that key the catalogue keys 19 of the 35 bound names and every name in only 7 of 50 files (D109); it answers RQ2 (research question 2, whether the reading beats what shipping systems do). The strongest-name-table condition (`strongest_name_table`) is a rule list in the catalogue's design covering the software the dataset presents as known, with no rule for Family 3's unregistered software or the invented names of familiarity tiers 4–5; it carries the paper's claim (D115), is the condition expected to score perfectly on the C1 (the single-situation calibration group) files, and fails structurally on world knowledge. 'A faithful reproduction of what shipping systems do today' and 'the whitelist approach real operating systems currently use' are restated to the two conditions (D91).
- Sources: S12-048 (9.12 D6, `task-9.12-related-work-prose/changelog.md:114`); SX-0150 (TODO 9.15 line (from 9.12 D6), `_dev/TODO.md:179`)
- Cross-ref: W-0535
- Notes: Condition ids in code: `harness/tools/harness/evaluator.py:47` (`CONDITIONS`) and `harness/guards/guard-spec.yaml:126` (the raw rows' `:116` is stale). Line 87 ('`whitelist`를 넘는가') carries the same change though no raw row names it. Write in Korean.

### W-0484 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §1.4 recognizer의 답은 어떤 모양인가, open note line 128
- Change: Close the note once `docs/recognition-vocabulary.md` §1 lists `session` among `initiated`'s values (9.10 D79's value for `c2-p1b` and `c7-indexing`, 'work the desktop session itself starts, unasked, at login'); line 126 already names `session`.
- Final word: 9.10 D79 (2026-10-03): `initiated: session`, 'work the desktop session itself starts, unasked, at login', used by `c2-p1b` and `c7-indexing`; its addition to the recognition vocabulary was handed to 9.15.
- Sources: SX-0845 (guidebook dataset vol-01 open note (§1.4), `dataset/01-the-big-picture.md:128`)
- Cross-ref: W-0533
- Notes: Apply after the recognition-vocabulary `initiated` row (W-0430). At HEAD `docs/recognition-vocabulary.md:50` still reads '`initiated` (`user` | `scheduled`)'.

### W-0485 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §1.5 RQ0: 아무 모델도 없이 먼저 여는 문지기 실험, the pin bullet line 143
- Change: Restate the quoted pins to 9.23 D17's: `pins.dataset` `81d3213d…` and `pins.variants.all` `7079e677…` (were `fad7192d…` and `03f14b2c…`); the sentence that the volume recomputed both and found them equal to the pins still holds at HEAD.
- Final word: 9.23 D17 (2026-10-15): the dataset manifest `81d3213d0443283a0eb456e19dee2b4216305db4e0c134f18ddd66ca74031ae0` and the variants manifest `7079e677bab864d21ef4a674079ac9ec2fa9758ba3a53a87879f77542cb282d9`, both carried by the RQ0 gate spec (RQ0, the gate experiment); the scoring spec stays at 9.23 D10's `2ad757b6…`.
- Sources: SX-0623 (9.23 D17, `task-9.23-guidebook-findings/changelog.md:157`)
- Notes: Checked at HEAD: `harness/experiments/rq0-gate.yaml:488–490`; `shasum -a 256` of `dataset/build.manifest.json` and `dataset/build.variants.manifest.json` gives the two pins. Not named by 9.23's hand-offs. vol-04 §11.6 line 1949 quotes `pins.variants.all` `03f14b2c…` as '2026-10-14의 값' — the same staleness; no raw row names it.

### W-0486 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §1.5 RQ0: 아무 모델도 없이 먼저 여는 문지기 실험, open note line 147
- Change: Close the note once `docs/terminology.md`'s 'RQ0 gate spec' entry says 19 judging files and K = 10.
- Final word: 9.14 decision 2 as amended (`c7-mail` reporting-only): the RQ0 gate spec's judging set is 19 files and K = 10 (`harness/experiments/rq0-gate.yaml` `files.judging`, `criterion.k`); before 2026-10-09 it was 25 files and K = 13.
- Sources: SX-0847 (guidebook dataset vol-01 open note (§1.5), `dataset/01-the-big-picture.md:147`)
- Notes: Apply after the terminology row (W-0424). At HEAD `docs/terminology.md:229–230` still reads '25 judging files, K = 13'.

### W-0487 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §1.5 RQ0: 아무 모델도 없이 먼저 여는 문지기 실험, line 149 and open note line 151
- Change: Close the note once `docs/research-claims.md` and the building plan §3 C2 (C2, the intent pair group) carry the rebuilt pair's wording (the unwanted side is its own measured job, name and behaviour both different); state 9.23 D9 beside it: P1 stays the load-bearing pair — it carries the recognition claim and `c2-p1a`'s scheduling headroom; RQ0, the gate experiment, judges `c2-p1a` and reports `c2-p1b` (9.14 decision 2), the indexer's declared idle class settling its side.
- Final word: The 2026-10-11 audit's C2 direction: the C2 pair sentences restated to the rebuilt state — the unwanted side is its own measured job, name and behaviour both different. 9.23 D9 (2026-10-14): P1 stays the load-bearing pair, stated as it stands — it carries the recognition claim (the wanted training run against the unwanted indexer, which a whitelist cannot tell apart) and its scheduling headroom on `c2-p1a`'s side; RQ0 judges `c2-p1a` and reports `c2-p1b` (9.14 decision 2), the indexer's declared idle class settling its side.
- Sources: SX-0849 (guidebook dataset vol-01 open note (§1.5), `dataset/01-the-big-picture.md:151`)
- Cross-ref: W-0540
- Notes: Apply after the research-claims row (W-0400) and the building plan's C2 rows. 9.23 D9 also corrects a quotation: `docs/research-claims.md` says 'behaviour is identical', not 'behaviourally identical'.

### W-0488 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §2.5 program 네 개를 손으로 따라가기, open note line 320
- Change: Close the note once `docs/data-contracts.md` §4 and `dataset/README.md`'s canonical example mark the editor program as a simplification or carry current values (in `c1-dev` the timer wakes outnumber the keystrokes 6,456 to 186; `desktop-interactive`, `23439` and `253642` are pre-rebuild).
- Final word: Record-gaps audit §2 item 13: in every compiled interactive file the timer-component wakes outnumber the keystroke wakes by one to two orders of magnitude (`c1-dev` 6,456 vs 186), so the README and data-contracts picture of an editor as alternating WAIT(input)/RUN pairs is a simplification; the examples predate the rebuild (§2 item 8).
- Sources: SX-0854 (guidebook dataset vol-01 open note (§2.5), `dataset/01-the-big-picture.md:320`)
- Notes: Apply after the data-contracts row (W-0255) and the README row (W-0199).

### W-0489 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §3.6 compile 한 번을 손으로 따라가기: `c1-dev`, step 2 line 662
- Change: Restate the example's library hash to HEAD's `archetypes.yaml@46e10504…` (the git blob since 9.23 D8's library change), or mark the walk-through as the 2026-10-14 build; `derived_from`'s `c1-dev.timeline.yaml@cbf1349a…` is unchanged.
- Final word: At HEAD every artifact's `meta.sampled.archetypes` is `archetypes.yaml@46e10504eb48ef6c720d5efb39d7ce17b477c775` (`git rev-parse HEAD:dataset/archetypes.yaml`; SHA-256 `50b0f4b6…`), changed by 9.23 D8's restated `code-editor` clause and rebuilt in 9.23 D10; `a2cc1957…` was the blob before (its SHA-256 `c6af7623…`, which 9.13 D7 calls a 'blob', record-gaps audit §1 item 5).
- Sources: SX-0768 (record-gaps §1 item 5, `jioh/2026-10-14-record-gaps-and-doc-staleness-for-9.15.md:15`)
- Cross-ref: W-0521
- Notes: Checked at HEAD: `dataset/build/coreset-single/c1-dev.workload.json` meta — derived_from `…c1-dev.timeline.yaml@cbf1349a49dc…` (unchanged), sampled archetypes `@46e10504…`, seed 107. In the same walk-through, step 4 (line 666) counts 6,642 WAIT/RUN pairs: since 9.23 D16 the editor's program ends with a trailing WAIT (13,285 instructions, the 6,642 wakes unchanged); step 5 (line 668) lists the canonical lints before 9.23 D14's three (a spawned child's WAKE targets, the 15-character comm limit, a program's end). Same hash fix in vol-03 (W-0521).

### W-0490 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §3.8 building plan의 '세 layer'와 scenario 목록, open note line 704
- Change: Close the note once `docs/workload/scenario-catalog.md` carries the current process names and the replaced S17 row (S17, now the unattended upgrade, in place of the malware scan).
- Final word: 9.10 D3: `clamscan` replaced by the unattended upgrade, handing 'scenario catalog S17 row replaced' to 9.15; 9.10 D33: the scenario catalog states what the dataset binds, each line an existence claim.
- Sources: SX-0857 (guidebook dataset vol-01 open note (§3.8), `dataset/01-the-big-picture.md:704`)
- Notes: Apply after the scenario-catalog row (W-0136).

### W-0491 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §3.9 결정론은 실제로 어떻게 지켜지나, open note line 716
- Change: Restate the note as settled: the 2026-10-10 audit's cross-platform libm risk (rated PLAUSIBLE) was closed by 9.20 D11's Linux run, CI run 38243554308 (2026-10-12), which reproduced the seven manifests; add that the manifests re-blessed at 9.23 D10 and D17 have not yet run on a CI runner. Keep or drop the remark that the run log was not opened.
- Final word: 9.20 D11: CI run 38243554308 on a Linux runner reproduced the seven manifests (the core set, the variants, the five generated sets), closing the 2026-10-10 audit's cross-platform libm risk; 9.23's TODO line (`_dev/TODO.md:187`): the D10 and D17 re-blesses 'not yet run on a CI runner'.
- Sources: SX-0858 (guidebook dataset vol-01 open note (§3.9), `dataset/01-the-big-picture.md:716`)
- Notes: The 9.16 line (`_dev/TODO.md:180`) lists CI run 38243554308's reproduction among the exit audit's reads.

### W-0492 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §4.2 맨 위의 데이터 파일들, open note line 761
- Change: Restate the note to the outcome of the outside-sweep row on `dataset/archetypes.yaml:1`: closed if the header is bumped to v0.2, or stating that the header stays at v0.1 while `dataset/README.md` and `docs/data-contracts.md` §2 say v0.2.
- Final word: 9.13 spec decision 9 (2026-10-09): the library's stated version goes from v0.1 to v0.2, naming `docs/data-contracts.md` §2 and `dataset/README.md`; the 2026-10-10 audit listed `dataset/archetypes.yaml:1`'s '(v0.1)' for 9.15. At HEAD the header still reads 'Layer 1 archetype library (v0.1)'.
- Sources: SX-0861 (guidebook dataset vol-01 open note (§4.2), `dataset/01-the-big-picture.md:761`)
- Notes: Waits on 인지오's call on the outside-sweep row on `dataset/archetypes.yaml` (W-0778): the library is an input of every manifest, so even a comment edit re-blesses the seven manifests and re-pins the RQ0 gate spec's `pins.dataset` and `pins.variants` (and moves the blob `46e10504…` / SHA-256 `50b0f4b6…` the dataset guidebook quotes).

### W-0493 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §4.4 입력 흐름과 측정 자료: stimulus/, launch/, replay/, meas/, open note line 788; §4.5 build/, manifest, coverage-grid.json, lines 809 (the core manifest's `inputs` 23) and 811 (the generated manifests' `inputs` 45)
- Change: Close the note with 9.23 D11: `compile.py`'s `input_files` pins `launch/*.json.gz`, so the core manifest's inputs are 33 (the library, the schema, 12 compiler sources, 3 stimulus streams, 6 replay streams, 10 launch streams) and a changed launch stream shows in them; restate line 809 (23 → 33) and line 811 (45 → 55).
- Final word: 9.23 D11 (2026-10-15): the compiler reads the ten launch streams `dataset/launch/launch-<entry>.json.gz` for every task a file starts after 0 s; `compile.py`'s `input_files` adds `launch/*.json.gz` (`dataset/tools/compile.py:64`), so the core manifest's inputs are 33 and each generated manifest's 55; the variants manifest pins the core manifest's bytes; `test_every_stream_directory_the_tools_open_is_pinned` requires every stream file the compiler and the linter open pinned.
- Sources: SX-0631 (9.23 D11, `task-9.23-guidebook-findings/changelog.md:108`); SX-0862 (guidebook dataset vol-01 open note (§4.4), `dataset/01-the-big-picture.md:788`)
- Cross-ref: W-0523
- Notes: Checked at HEAD: `dataset/build.manifest.json` `inputs` 33 (archetypes.yaml, 10 launch, 6 replay, the schema, 3 stimulus, `compile.py` and 11 `wlc/*.py`); each `dataset/build.<set>.manifest.json` 55; `dataset/build.variants.manifest.json` 3. 9.23 D11's hand-off names vol-07 only.

### W-0494 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §4.6 tools/: 도구 지도, table row line 827 (`check_build.py`); §4.7 pipeline: make 명령 여섯 개, the gate figure line 851 and step 6 line 861
- Change: State that since 9.23 D12 `check_build.py` holds every manifest, every derived timeline and `coverage-grid.json` to its committed bytes (`git show HEAD:<path>`), beside `build/` equal to the manifests' union: the table row, the figure's `make check` box and step 6's (a) add the derived timelines and the grid to the seven manifests.
- Final word: 9.23 D12 (2026-10-15): `check_build.py`'s `rewritten` names every derived timeline a variant spec names and `coverage-grid.json`; `check_committed` holds them to their committed bytes as it holds the manifests, so a derived timeline regenerated and left uncommitted fails `make check`; the dataset README's `make check` and `check_build.py` lines restated.
- Sources: SX-0634 (9.23 D12, `task-9.23-guidebook-findings/changelog.md:116`)
- Cross-ref: W-0496; W-0528; W-0548
- Notes: Code at HEAD: `dataset/tools/check_build.py:43–52` (`rewritten`), `:61–65` (`check_committed`); the `dataset/Makefile` check target; `dataset/README.md:151`. 9.23 D12's hand-off names vol-07 only. Step 1 of the same list is W-0496.

### W-0495 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §4.6 tools/: 도구 지도, line 836 and open note line 838
- Change: Close the note: `dataset/README.md:130` now names PyYAML, jsonschema-rs, pytest and numpy, each at the exact version `tools/requirements.txt` pins (9.23 D15); line 836 may add the exact pins (PyYAML 6.0.1, jsonschema-rs 0.29.1, pytest 8.3.4, numpy 1.26.4).
- Final word: 9.23 D15 (2026-10-15): `dataset/tools/requirements.txt` and `harness/tools/requirements.txt` pin the six direct dependencies exactly at the home machine's versions (the dataset's: PyYAML 6.0.1, jsonschema-rs 0.29.1, pytest 8.3.4, numpy 1.26.4); the dataset README's requirements line restated (`dataset/README.md:130`).
- Sources: SX-0864 (guidebook dataset vol-01 open note (§4.6), `dataset/01-the-big-picture.md:838`)
- Notes: The README fix the note waited on (the 2026-10-10 audit's 'README:99 omits numpy') is applied at HEAD; another row records it already-applied (W-0222).

### W-0496 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §4.7 pipeline: make 명령 여섯 개, step 1 line 855
- Change: Add to step 1's list that `make lint` runs `lint.py --freeze`, rejecting any `meas-pending` source tag (9.23 D13).
- Final word: 9.23 D13 (2026-10-15): `make lint` runs `lint.py --freeze`, which rejects a `meas-pending` tag ('meas-pending after freeze', `wlc/linter.py`); `test_lint.py::test_repo_is_freeze_clean` stays; no `meas-pending` tag in the library (one comment names it, `archetypes.yaml:38`); the README's `make lint` and `lint.py` lines name it.
- Sources: SX-0638 (9.23 D13, `task-9.23-guidebook-findings/changelog.md:124`)
- Cross-ref: W-0494
- Notes: Code at HEAD: `dataset/tools/wlc/linter.py:142–143`; `dataset/README.md:136`, `:152`. 9.23 D13's hand-off names vol-07 only. The same fact sits in the group's other volumes with no raw row: vol-02 §2.10 line 558 and its glossary line 1585 ('freeze … `make test`가 실제 repository에 적용', stale since D13) and vol-03 line 2001 (`--freeze`, still true); vol-01 §4.9 line 880 ('linter가 그 상태를 지킵니다') holds.

### W-0497 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §4.9 tree의 규칙, open note line 884
- Change: Close the note once `dataset/README.md`'s Rules of the tree (`:170`) and Coresets table (`:92`) state the demand window as a reported figure, not a rule.
- Final word: 9.14 decision 4 (2026-10-09): the ~100–150 % demand window retired as a gate; every file's demand is a measured fact the manifest reports and no build fails on it (`dataset/tools/wlc/estimate.py` docstring; `docs/workload/building-plan.md` §5a).
- Sources: SX-0866 (guidebook dataset vol-01 open note (§4.9), `dataset/01-the-big-picture.md:884`)
- Cross-ref: W-0536
- Notes: Apply after the README demand-window row (W-0202). At HEAD `dataset/README.md:170` still reads 'Files outside it get redesigned' and `:92` '(~100–150%)'.

### W-0498 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §5.1 전체를 숫자로, table line 912, line 917, open note line 919; §9.4 집합과 label 용어, glossary line 1563
- Change: Restate the core set's segment count to 67 — 66 on the 32-cell grid and `c6-dual`'s `ambiguous` one outside (`segments_total: 67`) — in the table, line 917 and the glossary; restate the note's own numbers (51 files, 67 segments; C6, the resolution-limit group, 6 segments since 9.23 D2 split `c6-spoof` at 20 s) and close it once `docs/workload/building-plan.md` §0/§3 and `docs/background-guide.md` §5/§7 say 51 files.
- Final word: 9.23 D10 (2026-10-14): the coverage grid's browsing/`false` cell gains `c6-spoof`'s second segment; 67 segments (66 before); 51 files since 9.13 added `c2-p2a-idle` (2026-10-09).
- Sources: SX-0600 (9.23 D10, `task-9.23-guidebook-findings/changelog.md:97`); SX-0870 (guidebook dataset vol-01 open note (§5.1), `dataset/01-the-big-picture.md:919`)
- Cross-ref: W-0501; W-0537
- Notes: Checked at HEAD: `dataset/coverage-grid.json` `segments_total` 67, 66 on cells, `outside` one (`c6-dual`). The note's 9.13 history (64 → 66; C2 14 segments) stays as history. Closing waits on the building-plan row (W-0086) and the background-guide row (W-0414). The generated layer's 3,946 segments are unaffected. Not named by 9.23's hand-off.

### W-0499 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §5.2 core set의 일곱 group, the C6 paragraph line 951 and open note line 953
- Change: Close the note with 9.23 D1: a query fires at 30 s on the count change `{chrome: 5} → {chrome: 6}`, nothing in the snapshot says call, and the meeting segment carries `pre_committed_miss: true`, excluded from the Layer-1 (recognition-accuracy) headline; the building plan's 'no query fires' is restated by its own row. Line 951 may say which C6 segments are pre-committed misses (`c6-alias` whole, `c6-fold` from 30 s, `c6-spoof` from 20 s).
- Final word: 9.23 D1 (2026-10-14): since 9.10 D30 a `chrome` task on `video-call` arrives at 30 s, so the snapshot goes from `chrome ×5` to `chrome ×6`; telemetry rule 1 makes a count-only change a set change, so a query fires at 30 s and D30's 'the canonical set does not change at the boundary' did not hold; nothing in the snapshot says call, so `c6-fold`'s meeting segment (30–60 s) carries `pre_committed_miss: true`; the browsing segment keeps its graded 0 s point; the file joins the RQ0 gate spec's `layer1_exclusions`.
- Sources: SX-0587 (9.23 D1, `task-9.23-guidebook-findings/changelog.md:13`); SX-0872 (guidebook dataset vol-01 open note (§5.2), `dataset/01-the-big-picture.md:953`)
- Cross-ref: W-0501; W-0543
- Notes: The building plan's C6 fold sentence is the row W-0111. Recipe at HEAD: `dataset/timelines/coreset/c6.variant.yaml:45–58`; `harness/experiments/rq0-gate.yaml:94`.

### W-0500 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §5.2 core set의 일곱 group, open note line 959
- Change: Close the note once `dataset/README.md`'s C7 row and the building plan §3 C7 (C7, the attribute counterpart group) restate 'one-diff pair' (length, window and operation times differ by design; the keystrokes are the base's over the slice since 9.18 D1).
- Final word: 9.18 (D1, D2) hand-off on the 9.15 TODO line: `dataset/README.md`'s C7 row and `docs/workload/building-plan.md` §3 C7 — 'one-diff pair': length, window and operation times differ; the keystrokes are now the base's over the slice; the 2026-10-10 audit A1.
- Sources: SX-0875 (guidebook dataset vol-01 open note (§5.2), `dataset/01-the-big-picture.md:959`)
- Notes: Apply after the README C7 row (W-0208) and the building-plan C7 row (W-0115).

### W-0501 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §5.3 coverage grid와 pre-committed miss, line 963, line 969 and its table lines 971–978, line 980, open note line 982
- Change: Restate to 9.23 D1, D2 and D10: 66 grid segments, 19 of them `background_wanted: false` (`c6-spoof`'s 20–60 s segment added); pre-committed misses on eight cells, one segment each — add browsing/`false` (`c6-spoof` from 20 s) and meeting/`true` (`c6-fold` from 30 s); `layer1_exclusions` is eight files. Close the note: three C6 files (C6, the resolution-limit group) now carry `pre_committed_miss` — `c6-alias` whole, `c6-fold` from the call's arrival, `c6-spoof` from the spoof's — so terminology's 'three C6 files' holds once it names them.
- Final word: 9.23 D1 (2026-10-14): `c6-fold`'s meeting segment (30–60 s) carries `pre_committed_miss: true`; 9.23 D2: `c6-spoof` split at 20 s — 0–20 s browsing/`true`, 20–60 s browsing/`false`, `spoof: true`, `pre_committed_miss: true`; both join the RQ0 gate spec's `layer1_exclusions`; 9.23 D10: each of browsing/`false` and meeting/`true` carries one pre-committed miss; `c6-dual` stays `ambiguous` and unannotated.
- Sources: SX-0593 (9.23 D2, `task-9.23-guidebook-findings/changelog.md:23`); SX-0877 (guidebook dataset vol-01 open note (§5.3), `dataset/01-the-big-picture.md:982`)
- Cross-ref: W-0498; W-0499; W-0534
- Notes: Checked at HEAD: `dataset/coverage-grid.json` cells — 66 segments on the grid, 19 `false`, eight cells with one miss; `dataset/tools/tests/test_grid.py:27–29` `MISS_CELLS` holds the eight; `harness/experiments/rq0-gate.yaml:94` `layer1_exclusions: [c1-indexing, c6-alias, c6-fold, c6-spoof, c7-backup, c7-ml-train, c7-render, c7-transcode]`. The terminology row (W-0426) names the three files; `docs/terminology.md:252` already says 'the three C6 files'.

### W-0502 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §5.5 수요 class와 utilization, open note line 998
- Change: Close the note: the manifest's `demand` for a job that outlives its file (`c2-p1a`, `c2-p2a`) is offered demand — the job's whole CPU spread to the file's end — and the docs say so in a scoping sentence; the estimate is not clipped.
- Final word: TODO 9.15 line (`_dev/TODO.md:179`, from the 2026-10-11 audit): 'the manifest's `demand` for a job outliving its file (`c2-p1a`, `c2-p2a`) scoped in a sentence or clipped'; no record chooses. Record-gaps audit §2 item 5: the static estimate spreads the job's whole `total_work` (1,389.885 s for `c2-p1a`, 727.170 s for `c2-p2a`) over its lifetime to the file's end — not an error, but any text quoting these as oversubscription needs the caveat.
- Sources: SX-0879 (guidebook dataset vol-01 open note (§5.5), `dataset/01-the-big-picture.md:998`)
- Cross-ref: W-0526; the for-인지오 rows W-0773, same question; W-0773
- Notes: Checked at HEAD: `dataset/build.manifest.json` `c2-p1a` 14.505 (segments 0.5272, 35.7721). Under 9.15 spec decision 2 an editing agent may take option (a) and log it (another row's notes say the same). The question is answered at merge (the docs describe the code, 9.15 spec decisions 2–3): the scoping-sentence route; the `dataset/README.md` and building-plan rows carry the sentence.

### W-0503 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §5.5 수요 class와 utilization, open note line 1004
- Change: Close the note once `docs/workload/building-plan.md` §0 and §5 and `docs/terminology.md`'s 'Workload variants' entry drop `-native` (the dataset ships `coreset-single` alone).
- Final word: 9.5 spec decision 14 dropped `-native`; 9.13 D1 (2026-10-09) removed it from the compiler — the dataset ships the single-lane set alone (`docs/data-contracts.md` §14, 2026-10-09).
- Sources: SX-0882 (guidebook dataset vol-01 open note (§5.6), `dataset/01-the-big-picture.md:1004`)
- Notes: Apply after the building-plan row (W-0087) and the terminology row (W-0419). At HEAD `docs/terminology.md:64` still names `-native`.

### W-0504 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §6.3 출처의 등급, open note line 1145
- Change: Close the note once `docs/references.md` types `lavd-ossna24` as a talk (9.12 D113's talk, abstract or news-report type); the 2026-10-11 resolution ('the figures stand as the talk's reported values; the `chain-x1.2` and `chain-x1.4` variants are the sensitivity check') stays as a 왜 이렇게 정했나 statement.
- Final word: 9.12 D113: `docs/references.md` gains a talk, abstract or news-report type and `lavd-ossna24` is re-typed as a talk (also on the 9.15 TODO line from the 2026-10-11 audit); the 2026-10-11 audit resolution keeps the talk's figures, the chain variants being the sensitivity check.
- Sources: SX-0885 (guidebook dataset vol-01 open note (§6.3), `dataset/01-the-big-picture.md:1145`)
- Notes: Apply after the references row (W-0072).

### W-0505 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §6.6 재구축: 왜 한 번 다시 만들었나, line 1189
- Change: Restate '13건의 문제' to the memo's fourteen summary rows (A1–A5, B1–B7, C, D), or drop the count.
- Final word: `docs/memos/2026-09-13-critical-findings.md`'s summary table has fourteen rows (A1–A5, B1–B7, C, D; lines 11–24); the Phase 9 spec and the 2026-10-10 audit count '13 findings' (record-gaps audit §1 item 6).
- Sources: SX-0771 (record-gaps §1 item 6, `jioh/2026-10-14-record-gaps-and-doc-staleness-for-9.15.md:16`)
- Cross-ref: W-0529
- Notes: Checked at HEAD: the memo's lines 11–24. Same fix in vol-03 line 2143 (W-0529).

### W-0506 · carried (after the final memo, with W-0580 and W-0602; its decided part applied in K11)
- At: `docs/guidebook/dataset/01-the-big-picture.md` §7.2 simulator: run file, open note line 1252
- Change: Once the final memo to 인경민 and 박이안 is committed, restate the note: the memo reports the loader's refusal of child-targeted WAKEs for the five core files and every generated file holding a compile (9.23 D3), with 인지오's answer on whether the simulator or the dataset changes; the note stays open until the simulator accepts the files.
- Final word: TODO 9.15 line (`_dev/TODO.md:179`, from the 2026-10-11 audit): the final memo carries the simulator loader's refusal of child-targeted WAKEs (`simulator/src/sim.cpp:874-904`; `c1-compile`, `c7-compile`, `c3-workday`, `c4-compile`, `c6-dual`; 9.6 D19, six processes per object job waking each other); 9.23 D3 adds the generated files holding a compile (the 212 jobs in them could not be run); 9.23 D14 lints that a spawned child's WAKE targets resolve, which leaves the simulator's refusal as it was.
- Sources: SX-0889 (guidebook dataset vol-01 open note (§7.2), `dataset/01-the-big-picture.md:1252`)
- Cross-ref: W-0547; the final-memo row W-0718 and the for-인지오 row W-0774
- Notes: Checked at HEAD: `simulator/src/sim.cpp:876` dies with 'WAKE target is not a top-level task' (the file last changed 2026-10-10, `6bf9d850`). Apply with or after the final memo: the final-memo row W-0718 and the for-인지오 row W-0774 (; it asks 인지오 to confirm the simulator, not the dataset, changes). Same matter as vol-04 §10.7's note (W-0547).

### W-0865 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §3.8 building plan의 "세 layer"와 scenario 목록, the diagram lines 695–697 ("Layer 1/2/3") and line 700 ("scenario 목록이 Layer 2입니다" and the "Layer 1" name note); the open notes on the name collision, §1.3 line 93 and §9.8 line 1630; the glossary preamble line 1461; §4.2 line 761 (quoting `dataset/archetypes.yaml:1`)
- Change: Name the dataset's layers as W-0742's answer does — the archetype library, the scenario catalog, the timelines — and keep "Layer 1/2" for the evaluation layers alone; close the notes at lines 93 and 1630 with the answer (the research-claims chain's links "link 1"–"link 7", C1–C7 the core set's file groups). Line 761's quotation follows W-0853 (the header's "Layer 1", in the batched rebuild after wave 4) with W-0492.
- Final word: 인지오's answer to W-0742 (2026-10-16, (a)); K02 renamed the building plan's §1 diagram (ARCHETYPE LIBRARY, SCENARIO CATALOG, TIMELINES) and its headings §2–§4.
- Sources: `logs/K02.md` ## Rows for other chunks (X6, restated in fix round 2)
- Cross-ref: W-0742; W-0492; W-0853
- Notes: found in K02. W-0742 blocks "the dataset guidebook vol-01 §1.4 note and any rename sweep; also the open note at :93"; no row of this file carried them.

### W-0917 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §1.5 RQ0: 아무 모델도 없이 먼저 여는 문지기 실험, line 132 ("LLM 없이 `random`과 `oracle`만 돌려 봅니다"); the open notes at lines 93 and 1630–1631 (W-0865's) and line 151 (W-0487's)
- Change: (1) Line 132: RQ0 runs `fixed`, `random` and `oracle`. (2) When applying W-0865 and W-0487, close the notes on what K08 applied: the name-collision notes (`:93`, `:1630–1631`) on W-0742 (a) — the dataset's layers named, the chain's links "link 1"–"link 7"; the `:151` note ("행동이 똑같다") on W-0392 and W-0400 — the P1 pair two real jobs, differing in behaviour and declared class.
- Final word: `harness/experiments/rq0-gate.yaml` `conditions: [fixed, random, oracle]`; 인지오's answer to W-0742 (2026-10-16, (a)); W-0392 and W-0400, applied in K08.
- Sources: `logs/K08.md` ## Rows for other chunks (X4)
- Cross-ref: W-0865; W-0487; W-0742; W-0392; W-0400
- Notes: found in K08.

### W-0925 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §4.1, line 754 ("`dataset/.gitignore`가 `dataset/build/`와 `dataset/generated/`를 무시하도록 적고")
- Change: Name the repository root's `.gitignore` (lines 2–3) as the file holding the two rules.
- Final word: K11's last review (round 2, minor finding 2): no `dataset/.gitignore` exists or ever did (`git log --all -- dataset/.gitignore`); the two rules are the root `.gitignore`'s lines 2–3 (`git check-ignore -v`).
- Sources: `logs/K11.md` ## Review round 2, minor finding 2
- Cross-ref: —
- Notes: found in K11's last review. K11's file: a follow-up chunk.

### W-0958 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §8.1's heading, line 1378 ("## 8.1 2권 · Archetype library: process 하나를 scheduler의 눈으로 적기"); chapter 8's opening (line 1376) copies each volume's title verbatim ("각 권의 제목과 … 그대로 옮기고")
- Change: Restate the heading to vol-02's current title: "## 8.1 2권 · Archetype library: 프로그램 한 종류를 scheduler의 눈으로 적기".
- Final word: W-0957, applied in H2: vol-02's H1 reads "# 2권 · Archetype library: 프로그램 한 종류를 scheduler의 눈으로 적기", and `docs/guidebook/dataset/README.md:14`'s link text with it (the archetype plan's §1, "one kind of program as the scheduler sees it", since `18127cc9`). No link targets the heading's anchor (H2's grep over `docs/`).
- Sources: `logs/H2.md` ## Rows for other chunks (X1); W-0957
- Cross-ref: W-0957; W-0959
- Notes: found in H2. K11's file: a follow-up chunk.

### W-0959 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §3.1's 용어 box, line 494 ("`archetype`은 한 종류의 process가 scheduler에게 어떻게 보이는지를 적은, 출처가 붙은 생성 모델"); §3.2, line 498 ("항목 하나가 process 행동의 한 종류입니다"); §9.3's glossary `archetype` row, line 1543 ("한 종류의 process가 scheduler에게 어떻게 보이는지를 적은, 출처가 붙은 생성 모델")
- Change: Restate "한 종류의 process" (lines 494, 1543) and "process 행동의 한 종류" (line 498) to "프로그램 한 종류" in each, nothing else. In the volume's Korean.
- Final word: `docs/workload/archetype-plan.md` §1 (`:8`) reads "a **generative model of one kind of program as the scheduler sees it**" since `18127cc9` (2026-10-16, K04): most entries merge a measured application's whole process tree into one task (`dataset/archetypes.yaml`'s measured entries: "one task carries the whole process tree merged (D14)"); `compiler-child` is six tasks. H2 restated vol-02's title (W-0957) and its two definitions (its N1: `:9` and the glossary's `archetype` row `:1543`) to "프로그램 한 종류"; K18 restated `docs/README.md`'s archetype-plan line and its Full-index row to "one kind of program" (its N6).
- Sources: `logs/H2.md` ## Rows for other chunks (X2); W-0957; `logs/H2.md` ## New rows found and applied (N1); `logs/K18.md` ## Fix round 1 (N6); `docs/workload/archetype-plan.md` §1
- Cross-ref: W-0957; W-0958; W-0960; W-0961; W-0962; W-0963
- Notes: found in H2. K11's file: a follow-up chunk. Line 494 is the archetype plan's sentence before `18127cc9` nearly word for word.

### W-0965 · applied
- At: `docs/guidebook/dataset/01-the-big-picture.md` §3.8's diagram, line 694 ("ARCHETYPE LIBRARY   한 process가 어떻게 행동하나            (archetypes.yaml)"), which §3.8 presents as the building plan §1's (line 691)
- Change: Restate "한 process가 어떻게 행동하나" to "프로그램 한 종류가 어떻게 행동하나", the path column re-padded, nothing else; in the same change as W-0964 (the building plan's line 35). In the volume's Korean.
- Final word: As W-0964. I1 restated the volume's other definitions of an archetype to "프로그램 한 종류" (W-0958, W-0959; its N2, §3.1's archetype bullet, line 490).
- Sources: `logs/I1.md` ## Found in these files, carried (N4); ## Rows for other chunks (X1)
- Cross-ref: W-0964; W-0959; W-0968
- Notes: found in I1 (its N4, carried: the diagram renders the building plan's, whose line 35 still reads "how one process behaves"; I1's decision 5). K11's file: a follow-up chunk, with W-0964.

## Also on this file, not for editing from this list

- W-0507 · blocked, simulator TIMER (outside the spec's list) — §2.4 여섯 개의 primitive, open note line 288
- W-0508 · closed, carried — `_dev/TODO.md:190` (Phase 10: swap mocks for the real simulator … judge per the RQ0 gate spec, whose `simulator-conformance` statement lists item (e)) and the…
- W-0509 · closed, carried — `_dev/TODO.md:200` (Backlog: 'Unwanted jobs to measure — how many the attribute's `false` side needs is decided in the RQ1 experiment spec's session …') carrie…
- W-0510 · closed, carried — `_dev/TODO.md:180` (9.16 Exit audits — the claim, measurement and compiled-number audits re-run on the final state) carries it.
- W-0742 · waits on 인지오 — Are the two name collisions resolved? What the docs say: 'Layer 1' is the recognition-accuracy measurement (`docs/terminology.md:198`) and also the archetype library, the dataset's first layer (`docs/terminology.md:55`,… Blocks: The dataset guidebook vol-01 §1.4 note and any rename sweep.; also the open note at docs/guidebook/dataset/01-the-big-picture.md:93
