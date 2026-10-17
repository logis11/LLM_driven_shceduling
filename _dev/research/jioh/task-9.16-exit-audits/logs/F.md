# 9.16 closing docs chunk F

On top of the W, P, R and G chunks' uncommitted edits and the data chunk's commit `17f28d7f`. Not committed. Line numbers are the files as they stand after this chunk. Every changed `docs/` file with a status header reads `Updated 2026-10-17` (all already did); the research guidebook carries none. `dataset/` and `harness/` untouched except the one-word connective in `dataset/README.md:150`, which the "For F" list names.

## Pins and manifest hashes

Grepped `docs/` and `dataset/README.md` for the old dataset `0f0af422…`, variants `cdc14319…`, generated `d84fb68a…` `a6980482…` `92676677…` `1d129a51…` `8c38e7a8…`, scoring spec `2ad757b6…` and `cbd64d5c…` (no occurrence), guard spec 1.1 `24ccb875…`, driver table `0fba4b3c…` (the two from `git show 3fbb7c25 -- harness/experiments/rq0-gate.yaml`), and the library's old SHA-256 `7de087da…` and git blob `803395dc…` (manifest inputs and artifact `meta`). New values checked by `shasum -a 256` / `git rev-parse` on the tree: dataset `8e1eb753…`, variants `8e2948b1…`, the five generated as `harness/CHANGELOG.md`'s 9.16 data entry, scoring spec `f7d1df4c…`, guard spec 1.2 `c2dad06f…`, driver table `e1155a72…`, library SHA-256 `1e308606…`, blob `c78d8cf9…`; artifact and variant hashes read from the manifests and `build/`.

- `docs/guidebook/dataset/01-the-big-picture.md:144` pins → `8e1eb753…`/`8e2948b1…` (9.16's re-pin). `:665` library blob → `c78d8cf9…`, "두 번 더" → "세 번 더" with the 9.16 change. `:717` 9.16's bless added; the CI sentence restated to `gh run list` now: 9.15's last state (`2b080333`) green in dataset run 39014790007, its two earlier states never run, 9.16's (`17f28d7f`) run 39030123144 still in progress. `:1344` the pin history ends at `8e1eb753…`.
- `03-timeline-to-canonical-workload.md:863`, `:1093` (`meta` examples), `:867` → `c78d8cf9…`.
- `04-the-coreset.md:1966` variants pin → `8e2948b1…` in full; 9.16 added to the re-pin history.
- `05-the-generated-layer.md:1649` "여덟 번" → "아홉 번"; `:1661` a 9.16 row (hashes, what moved: library hash everywhere, `derived_from` 60/90/0/32/6 by the `parallelism_cap` relabel, `inputs` library, `grids.yaml`, `c1-compile`); `:1663` "마지막 줄(9.16, …)"; `:1711` scoring spec now `f7d1df4c…` after 9.16's `c2-p3b` term and `c7-meeting` reason.
- `06-grounding-measurement-verification.md:1676` the current pins restated to 9.16's (both entries), 9.15's second rebuild moved into the history.
- `07-build-gate-manifests-ci-tests.md:94` (c1-dev `meta`), `:255–256` (the two library hashes), `:267` a 9.16 row in the library-hash table, `:269` "네 번" → "다섯 번 … 문장과 꼬리표", `:289` inputs row, `:342–343` the first two artifacts, `:392–393` variants `inputs`, `:403–417` the three variant records, `:543–550` the pins block (guard spec "1.2"), `:566–571` the Merkle sketch, `:588` changelog count, `:595`, `:602–603` example lint lines, `:646` a 9.16 row in the pin history, `:648` scoring/guard/driver pin chains, `:652–658` a 9.16 column in the generated table, `:660` the 9.16 rebuild's generated changes, `:838` case 2's lint line.
- `08-decision-chronicle.md:1799` 9.15's second re-pin now history; 9.16's harness and data re-pins current (the three harness decisions said by what they decided). `:1609`, `:1863` (dated history) left.
- `docs/workload/coreset-guide.md:397`, `docs/background-guide.md:132`, `docs/data-contracts.md:215`: library blob in the `meta` examples → `c78d8cf…`. The data contracts' changelog takes contract changes only; no entry.
- Left as dated records: the pair review's revision notes `:7`, `:9`; vol 08 `:1609`, `:1863`; vol 07's history rows.

## The stability-ledger script path

- `docs/workload/measurement-overview.md:97` and `docs/guidebook/dataset/06-grounding-measurement-verification.md:1555` → `dataset/tools/meas/stability_ledger.py`.
- The validity memo `:4` and the final memo's 정정 `:422` already named it (P). `docs/README.md:98` names no path; unchanged.

## The new release and the corrected figures

- `measurement-overview.md:166`: the session campaign's long-phase probes 36, 41, 44 (three runs) and what rests on them, in `meas-ci-probes-2026-09-23`.
- vol 06 `:1075` release count 33 → 34 (`gh release list`), `:1112` a row for the release (title as GitHub gives it).
- vol 08 `:1817` 9.16 D5's entry names the release.
- vol 02 `:1226` CPU share named the 12 renderers' (9.6 × 10⁻⁵; one renderer about 8 × 10⁻⁶, the 9.10 results page); `:1245` −7.2 % → −7.8 % with the first-placement origin. No doc quoted `MemoryInfra`'s 3.6/2.4 sentence (grepped); vol 07 `:267` lists it among 9.16's library changes.

## Review R/G, blocking

- research vol-06 `:1332` → "관례로 정한 값(8 thread 데스크톱에 적용한 `nproc` 규칙)".
- G/02 `:437` box restated: 9.6 D4 labels the cap convention ("Label: convention, grounds cited for the choice"), 9.10 D160's listing wrote design citing 9.6 D4, the label follows 9.6 D4 (`decisions.md`'s item taken without a question); `:435` the example `source` map → `convention`.
- G/03 `:451` recounted on the tree (`dataset/timelines/**/*.timeline.yaml`, 131 tasks, 53 with `source`): `design` 16 → 11, `convention` 5; `:721` quote → `convention`.
- G/02 `:712`, G/06 `:1319` (the finding's `:1318`), G/02 `:1333`: equal to `archetypes.yaml:1750–1755` and `:1832–1838` as committed; unchanged.
- research vol-01 `:2094` and `:3338`: kept, with a read record added — `reads/C-10-windows-priority-class.md`, the priority-class and priority-level passages of S2-54's own copy (`sources/S2-54/win-scheduling-priorities.html`, SHA-256 equal to S2-54's). They state that a program sets its process's class (`SetPriorityClass`, `CreateProcess`) and its threads' levels (`SetThreadPriority`).
- The same relabel elsewhere (D-F3-08), found by grep: G/04 `:773`, `:1741`, `:1762` (the module build's `-j8`); G/05 `:889`, `:922`, `:1508` (the generator carries the C1 label, `gen/compose.py`, `tests/test_generated.py:71`); G/06 `:1428` (its quote of 9.6 D4, "design: the eight-thread desktop", is not in 9.6 D4 — restated to the rule and the decision's own label); G/07 `:1553`, `:1556`; `docs/workload/coreset-guide.md:607`, `:889`, `:1089`; `docs/workload/archetype-plan.md:124`.

## Quoted library wording in the guidebooks

Every English quotation of 25+ characters in `docs/guidebook/**` was checked against the committed `archetypes.yaml` (its strings and comments, whitespace folded; scan script `<scratch>/f916/quotes.py`). The 44 near-misses were read one by one: all but the ones below quote a decision, record or earlier library and say so. Changed:
- G/02 `:995` `compiler-child`'s note → the current sentence (D-F3-02); the history adds 9.16's rebuild; the "존재만" gloss restated to what O'Callahan's count is.
- research vol-06 `:3540` the same note's opening and the count's meaning.
- G/02 `:1207` "production branch 595" → NVIDIA's 595 branch, `XB-Support: PB` (D-F3-29).
- G/02 `:732` and research vol-05 `:2063`: the six `Troy.exe` members by our comm rule, slide 16 showing one node (D-F1-14; G/02 quotes the library's sentence).
- Left: research vol-06 `:1753` ("into a chain …") quotes the library before 9.4 D8 changed it (`git log -S`), in a section on the 2026-09-13 library; G/02 `:720` and G/08 `:936` quote 9.4 D2's record (`task-9.4-gaming/changelog.md`), not the library.

## Review R/G, non-blocking

- G/08 `:1809–1819`: the six 9.16 headings carry ", 2026-10-17"; `:1819` D6 glosses untraced control (each job runs the phase traced and untraced; 7.5절).
- G/04 `:241`: "산술: 1 − 0.95¹⁰, cycle을 서로 독립으로 보고 boost 구간 하나에 cycle 열".
- Superlatives: vol-02 `:3208`, vol-05 `:1866`, `:2004` "널리 쓰이는" → the catalogue named (`ananicy-rules`, which CachyOS ships).
- vol-01 `:3077`: the tools listed as vol-06 `:460` has them — interbench, the ROS 2 executor and Lipari and Palopoli's thread skip; rt-app's default re-anchors.
- vol-06 `:1735` "슬라이드 30장 어디에도" → "30장의 슬라이드 어디에도".
- vol-02 `:3362` the guide named (UL's PCMark 10); the duplicate paragraph before the bold `:3484` removed (its programs are in the bold sentence).
- G/02 `:1333` the class audit's full path.
- Work-list ids: G/04 `:1917`, `:1932` and G/07 `:125`, `:177`, `:382`, `:986`, `:1004`, `:1006`, `:1067`, `:1256`, `:1292`, `:1525`, `:1537`, `:1604`, `:1614` now say what each item asked (each read in the 9.15 work list). G/01 `:96`, `:843`, `:1005` and G/07 `:1570` already said; unchanged.

## Review W/P, non-blocking

- pair review `:61`, `:81`: "arithmetic:" on the 1 − 0.95¹⁰.
- measurement-overview `:108`: 9.8 D15 glossed as the long-phase probe decision, which records the alignment (9.8 changelog `:147–199`, the 243/32 bins at `:190`).
- trace-clarifications memo `:97`: "(`c2-p2a` and `c2-p2b`)".
- grounding-sources `:59`: the row restated to S3-08's columns (CPU utilisation, CPI and MAI, cache misses, disk I/O; no context-switch or scheduling-latency field).
- Redundancies: measurement-overview `:51` (one "did not test"), source-vetting `:162` ("unsourced" + "without a source" → one), harness guide `:517` (the running-at-`T_end` clause stated once).
- `dataset/README.md:150`: "5, 10 and 30 s are …, and 2 s is a point below them".
- references `:239`: the overlap is with `sysmark30`; `pcmark10` names open-source programs; two vendors UL and BAPCo.

## Coverage gaps

- B-02 `docs/harness/metrics.md:258`: "derive values for those cases" (the finding's wording). B-05 `:264`: the numpy/R parenthetical dropped (no record); no metrics changelog entry, which takes primitive, aggregate, constant and floor changes only.
- B-25 (`harness/experiments/rq0-gate.yaml:170`, label "about 1.4 schedules per wake" arithmetic): **not done** — `harness/` is outside this chunk. For the lead.
- A-64: `reads/A-64-scx-lavd-slice-boost.md` — `lavd.bpf.h:74–77` and `main.rs:220–222` (and the clamp at `main.bpf.c:340–352`) at scx `c8728c6b` = tag `v1.1.3`, from the clone at `task-9.12-related-work-prose/sources/S2-09/audit-2026-10-09/scx/` (not `sources/S2-09/scx/` as the finding has it); the proposal's wording holds.
- `fiedler-gaffer04`, `mpv`, `chromium` status lines (`docs/references.md:558`, `:563`, `:578`) → `reads/B4-reads.md` §T-02 (1)–(3), each saying which files the blind read covered and which it did not.

## Record-only (R's D-25, D-44, D-46)

No B1–B4 read holds these passages (grepped). Restated to the records:
- D-25, research vol-06 `:1983–1987`: slide 10's quotation → the sentence 9.4 S1-01 records ("We collect and analyze all scheduling activities while playing games."); the "공통 특성" sentence now leads to slide 17.
- D-44, vol-06 `:2049`: the 확인함 box → what R06 holds — rule lines for `baloo_file`, `rsync`, `borg`, `transmission-daemon`, `clamd`, `discord`, `zoom`; `wget`, `curl`, `aria2c`, `element-desktop`, `slack`, `thunderbird` in its reader's summary.
- D-46, vol-06 `:2053`: "(`dbus-daemon`이 여기 들어 있음)" dropped; `:3027` `Xorg` dropped from the catalogue's `LowLatency_RT` sentence (9.12 S3 records `gnome-shell` and `pipewire`).

## For the lead

- B-25 in `harness/experiments/rq0-gate.yaml:170` (harness, not this chunk).
- Dataset run 39030123144 on `17f28d7f` was in progress at writing; vol 01 `:717` says so and needs its result once it lands.
- New files: `reads/A-64-scx-lavd-slice-boost.md`, `reads/C-10-windows-priority-class.md`, this log.

## After F (the lead)

- B-25 applied: `harness/experiments/rq0-gate.yaml:171` labels "about 1.4 on average" as arithmetic on `lavd-ossna24` slide 14's preemption share (9.4 D9).
- Dataset guidebook vol-01 :717: CI run 39030123144 on `17f28d7f` green (about 17 min); the box retitled from an open item.
- Combined review (one round, docs W/P/R/G/F): FAIL on six items, all fixed — research vol-06 :2624 and :3720 `parallelism_cap` convention; `docs/workload/archetype-plan.md:44` convention; dataset guidebook vol-02 :1187 convention; vol-05 :694, :776 `derived_from` blob `c002ee56…`; `docs/harness/harness-and-records-guide.md:1354` guard spec 1.2. Non-blocking: vol-01 :717's source named as `gh run list`.
