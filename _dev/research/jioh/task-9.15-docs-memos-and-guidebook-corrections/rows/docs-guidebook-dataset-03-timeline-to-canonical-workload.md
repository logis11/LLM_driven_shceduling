# Work-list rows — `docs/guidebook/dataset/03-timeline-to-canonical-workload.md`

Chunk K12, Dataset guidebook, volumes 3-4 (wave 3). 14 open rows. The file has 2404 lines at `d5cc7711`.

### W-0518 · applied
- At: `docs/guidebook/dataset/03-timeline-to-canonical-workload.md` §3.4 `count`: 같은 이름의 여러 instance, the 왜 이렇게 정했나 note on `count: 4`, line 418
- Change: Add 9.10 D126's stated floor to the count's grounds, in Korean: the four renderers are a floor — a real page's cross-site iframes take renderers this count leaves out.
- Final word: 9.10 D131 (2026-10-04) hands 9.10 D126's stated floor to 9.15 'wherever the docs state the renderer count: a real page's cross-site iframes take renderers this count leaves out'.
- Sources: S10-134 (9.10 D131, `task-9.10-scenarios-timelines/changelog.md:2417`)
- Cross-ref: W-0538
- Notes: Same row on vol-04 §4.5 lines 574–576 (W-0538).

### W-0519 · applied
- At: `docs/guidebook/dataset/03-timeline-to-canonical-workload.md` §3.6 이름의 규칙, 코드로 note line 468; §7.10 schema가 말하지 못하는 것, line 1244; §13.2 `lint_canonical`이 보는 것, lines 1893–1911 (check 7, line 1909); §13.3 lint가 보지 않는 것, lines 1925 and 1927; §16.1 the schema list, line 2217; §16.2 item 6, line 2263
- Change: Restate to 9.23 D14 and D16: `lint_canonical` now resolves a spawned child's WAKE targets as a top-level task's, holds every name, top-level and spawned, to 15 characters (the comm limit), and checks every program's end — a task without a pinned depart ends with EXIT, a segment-bound task with WAIT, TIMER or an unbounded LOOP, the compiler appending its loop's next blocking step. Add the three checks to §13.2, drop the two now-checked items from §13.3, restate line 468, line 1244 (the schema's `program` sentence now holds) and §16.1's schema entry, and close §16.2 item 6.
- Final word: 9.23 D14 (2026-10-15): three canonical lints in `wlc/linter.py` — a spawned child's WAKE targets resolve as a top-level task's; every name, top-level and spawned, within 15 characters (`TASK_COMM_LEN` 16 less the terminator, `linux-sched-h`); every program ends as its lifetime requires. 9.23 D16: no program runs out — a wake-driven segment-bound program ends with a WAIT on its last wake's channel (an interactive task's on its input), a timer-driven one with the next TIMER, whose tick falls at or past the depart, the resident single WAIT unchanged; a task without a pinned depart, top-level or spawned, ends with EXIT; the depart removes a segment-bound task. The schema is unchanged; its `program` sentence is now held.
- Sources: SX-0640 (9.23 D14, `task-9.23-guidebook-findings/changelog.md:134`); SX-0647 (9.23 D16, `task-9.23-guidebook-findings/changelog.md:148`); SX-0963 (guidebook dataset vol-03 ch.16 open list (§16.2) item 6, `dataset/03-timeline-to-canonical-workload.md:2263`)
- Cross-ref: W-0531
- Notes: Code at HEAD: `dataset/tools/wlc/linter.py:25` (`COMM_LIMIT = 15`), `:325` (spawned WAKE), `:332–337` (comm limit), `:339–348` and `:406–412` (programs' ends). Line 1244 also says the compiler always gives a segment-bound task a depart so no violation arises — since D16 a segment-bound program ends with a trailing WAIT or TIMER that the depart removes; check vol-03's worked compile examples that show a program's last instruction against D16 (e.g. `c1-dev`'s editor: 13,285 instructions, 6,642 WAIT/RUN pairs and a trailing WAIT). The schema description itself has another row. 9.23 D14's hand-off names vol-07 only.

### W-0520 · applied
- At: `docs/guidebook/dataset/03-timeline-to-canonical-workload.md` §5.4 seed와 id는 바꿀 수 없다, 왜 이렇게 정했나 note line 737; §16.1 '결정 기록과 코드', line 2247
- Change: Restate both: the deriver has refused a seed change since its first commit (`63c677dc`, 2026-08-28), the day task 2.4 decision 4 recorded 'warns' — the code never warned, so nothing changed later; no record says why it refuses rather than warns.
- Final word: Task 2.4 decision 4 (`_dev/docs/spec/jioh/task-2.4-core-timelines.md:26`, 2026-08-28): 'the deriver warns on an explicit override'; the deriver (`dataset/tools/wlc/deriver.py`) has raised `DeriveError(… 'variants may not change the seed')` since its first commit `63c677dc` (2026-08-28); no recorded reason for the difference (record-gaps audit §1 item 8).
- Sources: SX-0779 (record-gaps §1 item 8, `jioh/2026-10-14-record-gaps-and-doc-staleness-for-9.15.md:18`)
- Cross-ref: W-0531; the for-인지오 row W-0769
- Notes: Checked: `git show 63c677dc:dataset/tools/wlc/deriver.py` lines 81–84 refuse. The reason is asked in the for-인지오 row W-0769; this row describes the code meanwhile (9.15 spec decision 3).

### W-0521 · applied
- At: `docs/guidebook/dataset/03-timeline-to-canonical-workload.md` §6.1 단순한 파일: `c1-office`, the `meta` example line 861 and line 865; §7.2 `meta`: 출처, the example line 1084
- Change: Restate the examples' `sampled.archetypes` to HEAD's `archetypes.yaml@46e10504eb48ef6c720d5efb39d7ce17b477c775` (lines 861, 1084) and line 865's '`a2cc1957…`은 그 시점 … blob hash' to `46e10504…`, or mark the examples as the 2026-10-14 build; the `derived_from` blobs (`c1-office` `a0fd4543…`, `c2-p1a` `ba4dd1df…`) are unchanged.
- Final word: At HEAD every artifact's `meta.sampled.archetypes` is `archetypes.yaml@46e10504eb48ef6c720d5efb39d7ce17b477c775` (`git rev-parse HEAD:dataset/archetypes.yaml`; SHA-256 `50b0f4b6…`), changed by 9.23 D8's restated `code-editor` clause and rebuilt in 9.23 D10; `a2cc1957…` was the blob before (its SHA-256 `c6af7623…`, which 9.13 D7 calls a 'blob', record-gaps audit §1 item 5).
- Sources: SX-0767 (record-gaps §1 item 5, `jioh/2026-10-14-record-gaps-and-doc-staleness-for-9.15.md:15`)
- Cross-ref: W-0489
- Notes: Checked at HEAD: `dataset/build/coreset-single/c1-office.workload.json` and `c2-p1a.workload.json` meta — derived_from unchanged, sampled archetypes `@46e10504…`. Same fix in vol-01 (W-0489).

### W-0522 · applied
- At: `docs/guidebook/dataset/03-timeline-to-canonical-workload.md` §10.6 manifest와 대조해 확인하기, open note line 1552; §16.2 item 7, line 2265
- Change: Restate the note and §16.2 item 7 with 9.23 D15: the six direct dependencies are now pinned exactly at the home versions (the dataset's PyYAML 6.0.1, jsonschema-rs 0.29.1, pytest 8.3.4, numpy 1.26.4), CI runs Python 3.12 (`.github/workflows/dataset.yml:16`), and the Python version itself is not pinned ('Python 3.12+', `dataset/README.md:130`); keep the remaining question open with its owner, 인지오, unless 인지오's answer closes it.
- Final word: 9.23 D15 (2026-10-15): exact requirements — `dataset/tools/requirements.txt` and `harness/tools/requirements.txt` pin the six direct dependencies at the home machine's versions, their own dependencies unpinned; the Python version is not pinned; whether builds under another Python version produce the same bytes is unchecked.
- Sources: SX-0951 (guidebook dataset vol-03 open note (§10.6), `dataset/03-timeline-to-canonical-workload.md:1552`)
- Cross-ref: the for-인지오 row W-0745
- Waits on: W-0745 (인지오's answer; the row applies once it is given, or is logged as waiting)
- Notes: The open part is asked in the for-인지오 row W-0745: pin the Python version, or build under another version and compare with the manifests.

### W-0523 · applied
- At: `docs/guidebook/dataset/03-timeline-to-canonical-workload.md` §11.3 중간에 시작하는 앱의 launch phase, open note line 1604; §13.5 manifest: 무엇을 고정하나, table line 1946, paragraph line 1951 and open note line 1957; §16.1 the README entry, line 2225; §16.2 item 1, line 2253
- Change: Close the launch-stream notes (lines 1604, 1957), §16.1's README entry (line 2225; the README's 'inputs (library, schema, compiler sources, streams)' is now true) and §16.2 item 1 with 9.23 D11, and restate the counts and the list: the core manifest's `inputs` are 33 (the 23 plus the ten `dataset/launch/*.json.gz` streams), each generated manifest's 55 (45 before).
- Final word: 9.23 D11 (2026-10-15): the compiler reads the ten launch streams `dataset/launch/launch-<entry>.json.gz` for every task a file starts after 0 s; `compile.py`'s `input_files` adds `launch/*.json.gz` (`dataset/tools/compile.py:64`), so the core manifest's inputs are 33 and each generated manifest's 55; the variants manifest pins the core manifest's bytes; `test_every_stream_directory_the_tools_open_is_pinned` requires every stream file the compiler and the linter open pinned.
- Sources: SX-0630 (9.23 D11, `task-9.23-guidebook-findings/changelog.md:108`); SX-0953 (guidebook dataset vol-03 open note (§11.3), `dataset/03-timeline-to-canonical-workload.md:1604`); SX-0954 (guidebook dataset vol-03 open note (§13.5), `dataset/03-timeline-to-canonical-workload.md:1957`)
- Cross-ref: W-0493; W-0531
- Notes: Checked at HEAD: `dataset/tools/compile.py:55–66` (`input_files`, launch at :64); `dataset/build.manifest.json` inputs 33; the five generated manifests 55 each. 9.23 D11's hand-off names vol-07 only.

### W-0524 · applied
- At: `docs/guidebook/dataset/03-timeline-to-canonical-workload.md` §11.4 키 입력 재생: 위치를 뽑고 잘라 붙이기, the table's lead-in line 1628, the table lines 1630–1638, open note line 1642; §16.1 '결정 기록의 숫자와 tree의 숫자', line 2249
- Change: Close the note and §16.1's paragraph with 9.23 D7: 9.18 D6's figures count distinct keystroke times; for indexing, compile and ml-train its base figures (46, 2,354, 1,844) are the whole base file's, and over the counterpart's span they are 28, 358 and 1,629; browsing, office, dev and mail match the span. Say in the table's lead-in that its columns count input wake events, not distinct times (or add the distinct counts, as vol-04 §10.5's table does).
- Final word: 9.23 D7 (2026-10-14; forward note at 9.18 D6, `_dev/research/jioh/task-9.18-compiler-schema-and-build-gate/changelog.md:41`): for indexing, compile and ml-train 9.18 D6 gave the whole base file's distinct keystroke times, 46, 2,354 and 1,844; over the counterpart's span they are 28, 358 and 1,629; browsing, office, dev and mail match the span; the subset relation holds either way; the six artifacts were unchanged since D6 (their manifest hashes identical at `71a57a23` and `27340c3d`).
- Sources: SX-0357 (TODO 9.15 line (from 9.23 D7), `_dev/TODO.md:179`); SX-0609 (9.23 D7, `task-9.23-guidebook-findings/changelog.md:72`); SX-0955 (guidebook dataset vol-03 open note (§11.4), `dataset/03-timeline-to-canonical-workload.md:1642`)
- Cross-ref: W-0546; W-0531
- Notes: Named by 9.23 D7's hand-off ('vol-03 `:1642` with its table (about `:1630`, which counts events, not distinct times)'); also on the 9.15 TODO line. vol-04 §10.5's table (lines 1658–1666) gives events with distinct times in brackets. 9.23 D16's trailing WAIT adds no wake, so the counts stand. Write the closure in Korean.

### W-0525 · applied
- At: `docs/guidebook/dataset/03-timeline-to-canonical-workload.md` §12.3 ~100–150 % window: 관문에서 기록으로, open note line 1798
- Change: Close the note once `dataset/README.md` (`:92`, the Coresets table; `:170`, Rules of the tree), `docs/simulator/interpretation-contract.md` §7 ('Demand budget') and `docs/background-guide.md` §5 state the window as a reported figure; the note's quoted TODO lines `:77,131` are now `:92` and `:170`.
- Final word: 9.14 decision 4 (2026-10-09): the ~100–150 % demand window retired as a gate; demand is reported per file and per segment in the manifest and no build fails on it (`dataset/tools/wlc/estimate.py`; `docs/workload/building-plan.md` §5a).
- Sources: SX-0956 (guidebook dataset vol-03 open note (§12.3), `dataset/03-timeline-to-canonical-workload.md:1798`)
- Notes: Apply after the README demand-window row (W-0202), the interpretation-contract §7 row and the background-guide §5 row (W-0415).

### W-0526 · applied
- At: `docs/guidebook/dataset/03-timeline-to-canonical-workload.md` §12.4 job이 파일보다 오래 살 때, open note line 1808; §16.2 item 3, line 2257
- Change: Close the note and §16.2 item 3: the manifest's `demand` for a job that outlives its file is offered demand, stated in a scoping sentence in the docs; the estimate is not clipped.
- Final word: TODO 9.15 line (`_dev/TODO.md:179`, from the 2026-10-11 audit): 'the manifest's `demand` for a job outliving its file (`c2-p1a`, `c2-p2a`) scoped in a sentence or clipped'; no record chooses. Record-gaps audit §2 item 5: the static estimate spreads the job's whole `total_work` (1,389.885 s for `c2-p1a`, 727.170 s for `c2-p2a`) over its lifetime to the file's end — not an error, but any text quoting these as oversubscription needs the caveat.
- Sources: SX-0957 (guidebook dataset vol-03 open note (§12.4), `dataset/03-timeline-to-canonical-workload.md:1808`)
- Cross-ref: W-0502; the for-인지오 rows W-0773, same question; W-0773
- Notes: Under 9.15 spec decision 2 an editing agent may take option (a) and log it. Answered at merge as for the vol-01 note (the scoping-sentence route).

### W-0527 · applied
- At: `docs/guidebook/dataset/03-timeline-to-canonical-workload.md` §12.6 manifest의 `demand` 기록, the paragraph line 1879
- Change: Replace 'utilization의 변화 자체를 적은 기록은 찾지 못했습니다' with 9.23 D7's account: 9.13 R5's 1.00 was 0.9997 rounded and right when read; it became 0.8388 at the 9.17 re-bless, when 9.17 D1 cut the editor's typing into nine windows of 686–688 s in place of one of 12,068 s — the editor's CPU 3,460.4 s → 1,518.6 s, its input wakes 33,518 → 13,751, the build and the game chain unchanged, 0.161 lanes, the whole drop; no consumer reads the value.
- Final word: 9.23 D7 (2026-10-14; forward note at 9.17 D1): `c6-dual`'s utilization was 0.9997 (9.13 R5's 1.00, rounded, right when read) and became 0.8388 at the 9.17 re-bless — 9.17 D1 cut the editor's typing into nine windows of 686–688 s in place of one of 12,068 s; recompiled before and after `39d8d815`, the editor's CPU went 3,460.4 s → 1,518.6 s and its input wakes 33,518 → 13,751, the build and the game chain unchanged — 0.161 lanes, the whole drop; no consumer reads the value (the demand window is no gate, 9.14 decision 4; `c6-dual` reports; its guard exemption rests on its label).
- Sources: SX-0359 (TODO 9.15 line (from 9.23 D7), `_dev/TODO.md:179`); SX-0611 (9.23 D7, `task-9.23-guidebook-findings/changelog.md:72`); SX-0959 (guidebook dataset vol-03 open statement (§12.6), named by 9.23 D7, `dataset/03-timeline-to-canonical-workload.md:1879`)
- Notes: Checked at HEAD: `dataset/build.manifest.json` demand for `coreset-single/c6-dual.workload.json` 0.8388 (one segment, 0–12,072 s). Named by 9.23 D7's hand-off (vol-03 `:1879`) and the 9.15 TODO line.

### W-0528 · applied
- At: `docs/guidebook/dataset/03-timeline-to-canonical-workload.md` §13.7 `--check`와 build gate, line 1983; §14.6 lint가 맡지 않는 것, table row line 2070
- Change: Add what 9.23 D12 put in `check_build.py`: beside each manifest it holds every derived timeline a variant spec names and `coverage-grid.json` to the committed bytes (`git show HEAD:<path>`), so a derived timeline regenerated and left uncommitted fails `make check`; the table's `check_build.py` row covers the derived timelines and the grid too.
- Final word: 9.23 D12 (2026-10-15): `check_build.py`'s `rewritten` names every derived timeline a variant spec names and `coverage-grid.json`; `check_committed` holds them to their committed bytes as it holds the manifests, so a derived timeline regenerated and left uncommitted fails `make check`; the dataset README's `make check` and `check_build.py` lines restated.
- Sources: SX-0635 (9.23 D12, `task-9.23-guidebook-findings/changelog.md:116`)
- Cross-ref: W-0494; W-0548
- Notes: Code at HEAD: `dataset/tools/check_build.py:43–65`. 9.23 D12's hand-off names vol-07 only.

### W-0529 · applied
- At: `docs/guidebook/dataset/03-timeline-to-canonical-workload.md` §15.5 Phase 9의 연구 slice들: 측정이 문헌을 대체하다, line 2143
- Change: Restate '문제 13개' to the memo's fourteen summary rows (A1–A5, B1–B7, C, D), or drop the count.
- Final word: `docs/memos/2026-09-13-critical-findings.md`'s summary table has fourteen rows (A1–A5, B1–B7, C, D; lines 11–24); the Phase 9 spec and the 2026-10-10 audit count '13 findings' (record-gaps audit §1 item 6).
- Sources: SX-0772 (record-gaps §1 item 6, `jioh/2026-10-14-record-gaps-and-doc-staleness-for-9.15.md:16`)
- Cross-ref: W-0505
- Notes: Same fix in vol-01 line 1189 (W-0505).

### W-0530 · applied
- At: `docs/guidebook/dataset/03-timeline-to-canonical-workload.md` 16장 · 어긋난 문서와 열린 자리, the intro paragraph line 2198; §16.2 item 8, line 2267 (and the '9.15 목록에 있음' markers through §16.1)
- Change: Restate the status lines ('2026-10-14 현재 9.15는 진행 중(WIP)', '9.16은 시작 전') and the '9.15 목록에 있음' markers to the state after 9.15's chunks are committed: which §16.1 entries 9.15 fixed and which stay (the blocked TIMER rows; the code docstrings left to their outside-sweep rows); 9.16 still runs after.
- Final word: 9.15 spec decision 14: 9.15 is done when every work-list row is closed and every chunk committed; 9.16's exit audits run on that state (`_dev/TODO.md:179`, `:180`).
- Sources: SX-0964 (guidebook dataset vol-03 ch.16 open list (§16.2) item 8, `dataset/03-timeline-to-canonical-workload.md:2267`)
- Cross-ref: W-0531
- Notes: Apply last in the vol-03 chunk, after the §16.1 entries are settled (W-0531).

### W-0531 · applied
- At: `docs/guidebook/dataset/03-timeline-to-canonical-workload.md` §16.1 문서가 tree와 다르게 말하는 곳, lines 2200–2249
- Change: Remove or restate each §16.1 entry as its own doc's row is applied or found settled, keeping those still true: the interpretation contract's §3 TIMER row, the schema's TIMER description and data-contracts' 'missed ticks pile up as backlog' stay while the simulator-side TIMER rows are blocked; the code-docstring entries (`wlc/__init__.py`, `wlc/deriver.py`, `wlc/timeline.py`) stay unless their outside-sweep rows are applied. Settled at HEAD already: the README's requirements line (9.23 D15) and its manifest-inputs sentence (9.23 D11).
- Final word: Each §16.1 entry is a row on the doc it names (the interpretation contract, the workload schema's descriptions, `dataset/README.md`, `docs/data-contracts.md`, `docs/background-guide.md` §5, `docs/recognition-vocabulary.md` §1, the declared-class memo, the code docstrings, the decision records); settled at HEAD: the README's requirements line (9.23 D15), the README's manifest inputs (9.23 D11), the schema's `program` lint (9.23 D14, D16), 9.18 D6's counts (9.23 D7).
- Sources: SX-0965 (guidebook dataset vol-03 ch.16 mismatch table (§16.1) as a whole, `dataset/03-timeline-to-canonical-workload.md:2200`)
- Cross-ref: W-0519; W-0520; W-0523; W-0524; W-0530
- Notes: Entries with their own rows: the schema's `program` sentence (W-0519), the deriver (W-0520), the README manifest sentence (W-0523), 9.18 D6's counts (W-0524). The other entries' rows sit in, (interpretation contract) and (schema, docstrings, the memo). The README entry's quotation of `requirements.txt` ('PyYAML>=6.0, jsonschema-rs>=0.29, …') is stale since 9.23 D15's exact pins.

### W-0928 · applied
- At: `docs/guidebook/dataset/03-timeline-to-canonical-workload.md` §9.5, line 1447 ("재건으로 모든 대화형 entry가 측정된 entry가 되면서 어느 entry도 닿지 않게 되었습니다")
- Change: Say that no compiled task reached the three paths, and that `_unbounded_loop`'s two entries, `compiler-child` and `module-compiler-child`, are spawned children no timeline binds at the top level; "the interactive entries became measured" accounts for `_interactive_unroll` alone.
- Final word: K12's last review (round 3, R12, minor); W-0746's answer: in the old dispatch (`git show 37c2e233^:dataset/tools/wlc/compiler.py:141–154`) `compiler-child` and `module-compiler-child` (lifetime `spawned`) fell through to `_unbounded_loop`, and no timeline binds either as a top-level task.
- Sources: `logs/K12.md` ## Review round 3, R12
- Cross-ref: W-0746
- Notes: found in K12's last review. K12's file: a follow-up chunk. The section's table already lists the two entries as "(부모가 만듦)".

### W-0960 · applied
- At: `docs/guidebook/dataset/03-timeline-to-canonical-workload.md` §17.1's glossary `archetype` row, line 2271 ("한 종류의 process가 CPU를 어떻게 쓰는지 적은 행동 모형")
- Change: Restate "한 종류의 process" / "process 한 종류" to "프로그램 한 종류" in each definition, nothing else. In the volume's Korean.
- Final word: `docs/workload/archetype-plan.md` §1 (`:8`) reads "a **generative model of one kind of program as the scheduler sees it**" since `18127cc9` (2026-10-16, K04): most entries merge a measured application's whole process tree into one task (`dataset/archetypes.yaml`'s measured entries: "one task carries the whole process tree merged (D14)"); `compiler-child` is six tasks. H2 restated vol-02's title (W-0957) and its two definitions (its N1: `:9` and the glossary's `archetype` row `:1543`) to "프로그램 한 종류"; K18 restated `docs/README.md`'s archetype-plan line and its Full-index row to "one kind of program" (its N6).
- Sources: `logs/H2.md` ## Rows for other chunks (X2); W-0957; `logs/H2.md` ## New rows found and applied (N1); `logs/K18.md` ## Fix round 1 (N6); `docs/workload/archetype-plan.md` §1
- Cross-ref: W-0957; W-0959; W-0961; W-0962; W-0963
- Notes: found in H2. K12's file: a follow-up chunk.

### W-1014 · applied
- At: `docs/guidebook/dataset/03-timeline-to-canonical-workload.md` §7.7's channel table, line 1212 ("마지막 자식이 끝날 때"); §7.7's open note, line 1218 ("그 orchestrator가 낳은 마지막 자식이 끝날 때"); §16.2 item 2, line 2247 ("마지막 자식이 끝날 때")
- Change: "(낳은) 마지막 자식이 끝날 때" → "자식이 모두 끝났을 때".
- Final word: The final memo's review (2026-10-17): conformance item (g)'s wording, (a) — 'when every child it spawned has ended'; no rule moves. Applied in R3 to the six sources the decision names (the dataset guidebook vol-08 `:1817` in Korean: "spawn한 자식이 모두 끝났을 때").
- Sources: `logs/R3.md` ## Rows for other chunks (X3)
- Cross-ref: W-0743; W-0758; W-1012; W-1013; W-1015
- Notes: found in R3. K12's file: a follow-up chunk. Applied 2026-10-17 in S1.

### W-1019 · applied
- At: `docs/guidebook/dataset/03-timeline-to-canonical-workload.md:863`, `:867`, `:1093` (the `c1-office` and `c2-p1a` `meta` examples)
- Change: The library blob → `803395dc5462940050ba09bfe25c69d269633d9f`.
- Final word: The second data rebuild (`57342aab`, 2026-10-17): `git hash-object dataset/archetypes.yaml` = `803395dc5462940050ba09bfe25c69d269633d9f`; `harness/experiments/rq0-gate.yaml` `pins.dataset` `0f0af422…`, `pins.variants.all` `cdc143191fcd…`; `dataset/build.manifest.json` `c1-dev.workload.json` `f0f67836…`.
- Sources: `logs/S1.md` ## Found rows (W-1016–W-1020); `logs/R3.md` ## Review (the note on `818b41b…`); `logs/B4-data-rebuild.md` ## Review, finding 1
- Cross-ref: W-1016–W-1020
- Notes: found in S1. Applied 2026-10-17 in S1.

## Also on this file, not for editing from this list

- W-0532 · blocked, simulator TIMER (outside the spec's list) — §16.2 기록이 아직 정하지 않은 곳, item 4, line 2259
- W-0743 · waits on 인지오 — Who wakes an orchestrator's `WAIT children:<id>`, and when? What the code says: `dataset/tools/wlc/compiler.py:714` (`build-orchestrator`) and `:799` (`module-build-orchestrator`) append `WAIT children:<iid>` after the… Blocks: The final memo's simulator asks (beside W-0718); the dataset guidebook vol-03 §7.7 note and §16.2 item 2; the interpretation contract's FORK paragraph.; also t…
- W-0746 · waits on 인지오 — Keep or delete the unreached compiler paths? What the code says: `compiler.py`'s dispatch (`:140–155`) routes no current library entry to `_interactive_unroll`, `_finite_unroll` or `_unbounded_loop`, and nothing calls `… Blocks: The dataset guidebook vol-03 §16.2 item 5.; also §16.2 item 5 at docs/guidebook/dataset/03-timeline-to-canonical-workload.md:2261 and §9.5's paragraph on the p…
