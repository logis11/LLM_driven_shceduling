# Work-list rows — `docs/guidebook/dataset/02-the-archetype-library.md`

Chunk K11, Dataset guidebook, volumes 1-2 (wave 3). 6 open rows. The file has 1699 lines at `d5cc7711`.

### W-0511 · applied
- At: `docs/guidebook/dataset/02-the-archetype-library.md` §1.6 declared_class line 157; §4.1 `game-task-chain` line 723; §6.1 `build-orchestrator` line 949; §6.3 `cpu-batch` line 1017; §7.2 `file-archiver` line 1078; §7.3 `game-download` lines 1092 and 1096; §7.5 `package-upgrade` line 1135; §7.8 `incremental-backup` line 1175; §7.9 `module-build-orchestrator` line 1205; §8.1 `renderer-hidden` line 1237; §9.2 line 1302; §10.3 line 1344
- Change: Relabel these thirteen 열린 자리 notes as decided items, keeping their content: each states a limitation a decision recorded on purpose — none is undecided (미정), unchecked (확인 필요) or unrun (미실행), the three kinds the guidebook's legend gives 열린 자리 (`docs/guidebook/dataset/README.md`, '본문 안의 표시') — so each becomes a 왜 이렇게 정했나 note naming its decision. At line 949 restate the hand-off to 9.14 as done: the venue sensitivity check is the `venue-x0.8`/`venue-x1.25` variants.
- Final word: Each limitation was decided and recorded: 9.11 D16 (the kernel's idle rule acts among siblings of one task group; the indexer's `background.slice` share about 23 %, stated in `file-indexer`'s modeling_notes) at :157; 9.4 D9 ('No value changed') with the 2026-10-10 audit's A3 'resolved as is', the `chain-x1.2`/`chain-x1.4` variants the sensitivity check, at :723; 9.6 D4/D9 (the `-j8` cost 'a stated limitation of these values') and 9.6 D32 (the venue test the consumer's), done by 9.14 decision 10's `venue-x0.8`/`venue-x1.25` variants, at :949; 9.10 D88 ('D87 kept', the ×1.144 THP ratio stated in scope) at :1017; 9.7 D15, D23 (a pre-registered check stated as a limitation; the bimodal thread 'for a cause not identified') at :1078; 9.7 D25 (`fq_codel` kept, the link model's effect stated in modeling_notes) at :1092; 9.11 D6, D20 (the nice-10 work carried at full standing, bounded by `c2-p2a`/`c2-p2a-idle`, 9.13 D4, D5) at :1096; 9.11 D20 (the nice-19 work, 2.67 %, carried at full standing) at :1135; 9.10 D118 (the restore test not depicted) at :1175; the `module-build-orchestrator` scope (modules unsigned; a Secure Boot desktop adds signing five) at :1205; `renderer-hidden`'s scope ('stated') at :1237; 9.9 D27 (the filter rule decided; real-desktop validation deferred, measurement-overview §11) at :1302; 9.11 D33 (the idle I/O class not carried) at :1344.
- Sources: SX-0897 (guidebook dataset vol-02 open note (§1.6), `dataset/02-the-archetype-library.md:157`); SX-0901 (guidebook dataset vol-02 open note (§4.1), `dataset/02-the-archetype-library.md:723`); SX-0902 (guidebook dataset vol-02 open note (§6.1), `dataset/02-the-archetype-library.md:949`); SX-0903 (guidebook dataset vol-02 open note (§6.3), `dataset/02-the-archetype-library.md:1017`); SX-0904 (guidebook dataset vol-02 open note (§7.2), `dataset/02-the-archetype-library.md:1078`); SX-0905 (guidebook dataset vol-02 open note (§7.3), `dataset/02-the-archetype-library.md:1092`); SX-0906 (guidebook dataset vol-02 open note (§7.3), `dataset/02-the-archetype-library.md:1096`); SX-0907 (guidebook dataset vol-02 open note (§7.5), `dataset/02-the-archetype-library.md:1135`); SX-0908 (guidebook dataset vol-02 open note (§7.8), `dataset/02-the-archetype-library.md:1175`); SX-0909 (guidebook dataset vol-02 open note (§7.9), `dataset/02-the-archetype-library.md:1205`); SX-0910 (guidebook dataset vol-02 open note (§8.1), `dataset/02-the-archetype-library.md:1237`); SX-0911 (guidebook dataset vol-02 open note (§9.2), `dataset/02-the-archetype-library.md:1302`); SX-0914 (guidebook dataset vol-02 open note (§10.3), `dataset/02-the-archetype-library.md:1344`)
- Cross-ref: W-0515
- Notes: The legend has three markers (왜 이렇게 정했나, 코드로, 열린 자리) and none for a stated limitation, so 왜 이렇게 정했나 fits unless a fourth marker is added to the legend. :1078's unidentified cause stays stated as the record states it (no record asks anyone to find it). The dataset docs' own statements are separate rows: the nice-10 and nice-19 limitations (9.15 TODO line, from 9.11 D6, D20 and 9.13 D4, D5) and 'the I/O class not carried' (9.13 D4, D5). Verified at HEAD: `dataset/variants.yaml:35–50` holds `venue-x0.8`, `venue-x1.25`, `chain-x1.2`, `chain-x1.4`. :157 pairs with §10.3's note at :1337–1342 (W-0515).

### W-0512 · applied
- At: `docs/guidebook/dataset/02-the-archetype-library.md` §2.8 source tag 읽는 법, open note line 430
- Change: Close the note: `parallelism_cap` 8 is labelled `design`, by 9.10 D160 (`_dev/research/jioh/task-9.10-scenarios-timelines/changelog.md:2856–2860`) and `bound-values.md:27`, later than 9.6 D4's 'convention'; the timelines carry `design` (`dataset/timelines/coreset/c1-compile.timeline.yaml:21`).
- Final word: No record settles the label: 9.6 D4 (2026-09-17) and `build-orchestrator`'s modeling_notes call `parallelism_cap` 8 'convention, grounds cited' (the desktop `nproc` rule on an eight-thread desktop); `c1-compile`'s source map says `parallelism_cap: design` (record-gaps audit §1 item 4).
- Sources: SX-0899 (guidebook dataset vol-02 open note (§2.8), `dataset/02-the-archetype-library.md:430`)
- Cross-ref: the for-인지오 row W-0767, same question; W-0767
- Notes: Checked at HEAD: `c1-compile.timeline.yaml:20–21`; compiled artifacts carry `derived_from: …timeline.yaml@<blob>` (e.g. `c1-dev`'s `@cbf1349a…`). Answered at merge by 9.10 D160.

### W-0513 · applied
- At: `docs/guidebook/dataset/02-the-archetype-library.md` §2.11 `dataset/` 안의 이웃 파일들, open note line 580
- Change: Restate the note as a plain pointer — the measurement tools are described in each slice's `campaign/method.md`, `_dev/research/jioh/measurement-campaign-workflow.md`, `docs/workload/measurement-overview.md` and vol-06 — and drop the remark about the list the volume was commissioned with; it is not an open item.
- Final word: Verified at HEAD: neither `dataset/meas/` nor `dataset/tools/meas/` holds a README; no record asks for one.
- Sources: SX-0900 (guidebook dataset vol-02 open note (§2.11), `dataset/02-the-archetype-library.md:580`)
- Notes: —

### W-0514 · applied
- At: `docs/guidebook/dataset/02-the-archetype-library.md` §5.3 `code-editor` — VS Code에 TypeScript 쓰기, the long-span bullet line 815
- Change: Restate the clause in the past, as the library now reads: `c6-dual` held VS Code focused for 12,068 s before 9.17 D1 made its focus alternate with the game every 688 s; since then its longest focused stretch is 686–688 s; the long-phase probes' length and readings are unchanged.
- Final word: 9.23 D8 (2026-10-14): the `code-editor` entry's scope reads 'Read over 12,068 s, the span `c6-dual` held it focused before its focus alternated with the game every 688 s (9.17 D1)'; since 9.17 the editor's longest focused stretch in `c6-dual` is 686–688 s; the probes' length and readings unchanged (`dataset/archetypes.yaml:181`, written by `dataset/tools/meas/campaign/fold_in.py`).
- Sources: SX-0360 (TODO 9.15 line (from 9.23 D8), `_dev/TODO.md:179`); SX-0612 (9.23 D8, `task-9.23-guidebook-findings/changelog.md:80`)
- Cross-ref: W-0545
- Notes: Named by 9.23 D8's hand-off (vol-02 `:815`; also on the 9.15 TODO line). Same clause in vol-04 §9.6 line 1552 (W-0545) and vol-06 `:1038` (another row).

### W-0515 · applied
- At: `docs/guidebook/dataset/02-the-archetype-library.md` §10.3 실제 desktop과의 차이, open note lines 1337–1342
- Change: Relabel the note as a recorded limitation: the simulator models no task-group (cgroup slice) weights; 9.11 D16 keeps the strict idle rule as design for the scheduler under test and states the indexer's `background.slice` share (about 23 % against the editor on the depicted desktop) as a limitation (`_dev/research/jioh/task-9.11-scheduler-constants/changelog.md:216–228`).
- Final word: 9.11 D16 (2026-10-08): the kernel's idle rule acts only among siblings of one task group (sched(7)); the strict idle rule stays as 'design for the scheduler under test'; the indexer's `background.slice` share (about 23 %) and what D16 could not read (snap scopes, a running Déjà Dup's backup, other `app.slice` units with CPU settings, where Steam's games run) stated as limitations; no record decides whether the simulator ever models group weights.
- Sources: SX-0912 (guidebook dataset vol-02 open note (§10.3), `dataset/02-the-archetype-library.md:1337`)
- Cross-ref: W-0511; the for-인지오 row W-0775, same question; W-0775
- Notes: Low stakes: the limitation is already stated in the library and in the scoring spec's header (`harness/scoring/scoring-spec.yaml:37–43`, 'about 23 % (9.11 D16)'). Answered at merge by 9.11 D16.

### W-0516 · applied
- At: `docs/guidebook/dataset/02-the-archetype-library.md` §12.1 library 수준의 scale 한계, open note line 1468
- Change: Close the note's first part once the library-level scale limitation is stated at the library level, naming where; keep a pointer that 9.16's 'venue mix listed per timeline' stays on the 9.16 line.
- Final word: 9.5 follow-ups spec decision 13: the scale limitation 'stated once at the library level'; the 9.15 TODO line (`_dev/TODO.md:179`, 'library-level scale limitation stated (spec decision 13)'); the record-gaps audit §1 item 2 confirms it is still missing; 9.16 (`_dev/TODO.md:180`) carries 'venue mix listed per timeline'.
- Sources: SX-0916 (guidebook dataset vol-02 open note (§12.1), `dataset/02-the-archetype-library.md:1468`)
- Notes: Apply after the row that states it — the `dataset/README.md` library-scale row (W-0238).

### W-0848 · applied
- At: `docs/guidebook/dataset/02-the-archetype-library.md` line 413 (quotes `docs/workload/grounding-sources.md`'s citation-tier rule: "a deployed-system citation may support only *existence claims* … never empirical, behavioral, or statistical claims.")
- Change: Quote the rule as it now stands — the deployed-system tier as 9.12 D112 widened it, and the talk, conference abstract or news report type — from `grounding-sources.md:77` once W-0839 lands, or from `docs/references.md`'s citation-tier rule.
- Final word: 9.12 D112 and D113, applied in K01 to `docs/references.md`'s rules (W-0002, W-0001).
- Sources: W-0002; `logs/K01.md` ## Rows for other chunks
- Cross-ref: W-0839; W-0836
- Notes: found in K01. The grounding docs (wave 2) restate line 77 before this volume's chunk (wave 3).

### W-0858 · applied
- At: `docs/guidebook/dataset/02-the-archetype-library.md` §11.5, closing paragraph line 1456 ('이 변화들 때문에, `docs/workload/archetype-plan.md` §4, `docs/data-contracts.md` §2의 "There are twelve" 문단과 예시, `docs/workload/coreset-guide.md` §4 이후, … 지금 library와 다릅니다.')
- Change: Drop `docs/workload/coreset-guide.md` §4 from the list of docs that differ from the library: since K03 the guide's §4 holds the library's 29 entries.
- Final word: K03 (wave 1, review passed 2026-10-16): W-0161 rewrote the guide's §4 to the 29 entries, grouped by kind, with §4.8's summary table of all 29.
- Sources: `logs/K03.md` ## Rows for other chunks; W-0161
- Cross-ref: W-0154; W-0161
- Notes: found in K03. `docs/data-contracts.md` §2, in the same list, now lists the 29 entries too (K05, W-0245); the paragraph's other docs land with their own chunks.

### W-0871 · applied
- At: `docs/guidebook/dataset/02-the-archetype-library.md` §12.1 library 수준의 scale 한계, open note line 1468 (W-0516's place)
- Change: When applying W-0516, name `docs/workload/archetype-plan.md` §2, "Observation venues", as where the library-level scale limitation is stated; `dataset/README.md` does not restate it. W-0516's apply-after ("the `dataset/README.md` library-scale row (W-0238)") is the archetype plan's row W-0238, applied in K04.
- Final word: K04 (wave 1, review passed 2026-10-16): W-0238 applied in the archetype plan's §2, "Observation venues", 9.5 follow-ups spec decision 13's sentence kept verbatim (K04 decision 7); the work list's "Settled at merge": the statement goes in the archetype plan, and the README does not restate it.
- Sources: `logs/K04.md` ## Rows for other chunks
- Cross-ref: W-0516; W-0238; W-0872
- Notes: found in K04.

### W-0926 · applied
- At: `docs/guidebook/dataset/02-the-archetype-library.md` line 1458 (W-0858's paragraph: "data-contracts §2는 "There are 29"로 시작하며"); line 1281 ("9.10 D28 … session process가 idle 파일에만 나오고 다른 모든 파일은 그것을 생략")
- Change: (1) `:1458` → "data-contracts §2의 그 문단은 "There are 29"라고 적으며". (2) `:1281` scoped to the core set, as vol-01 §3.3 now words it ("그 밖의 core 파일").
- Final word: K11's last review (round 2, minor findings 1 and 3). (1) `docs/data-contracts.md` §2 opens with the "Frozen (v0.2, …)" line and the `declared_class` paragraph; "There are 29" is its third paragraph (`:78`). (2) 인지오's answer to K02's M7 (2026-10-16, (a)): D28 reads as the core set's rule; the generated layer binds the four session processes in 182 files, 62 of them beside another mode's programs (vol-05 §2.6, W-0888).
- Sources: `logs/K11.md` ## Review round 2, minor findings 1 and 3
- Cross-ref: W-0858; W-0888
- Notes: found in K11's last review. K11's file: a follow-up chunk.

### W-0952 · applied
- At: `docs/guidebook/dataset/02-the-archetype-library.md` §12.3's "왜 이렇게 정했나" box, line 1497 ("여섯 항목(…)의 compile된 흐름을 pooled repeat 하나의 실제 관측 wake 순서로 바꿔 넣습니다")
- Change: The replay variant puts in each stream of its kind (wakes, runs with the block after each, cycles), not the wake order alone. The quoted reason ("one pooled repeat's measured wake sequence …") stays verbatim. In the volume's Korean.
- Final word: W-0876, applied 2026-10-17 in the batched data rebuild (`7b024003`): each `dataset/replay/*.json.gz` carries its `kind` — `wakes` (`code-editor`, `web-browser`, `renderer-hidden`), `runs` with the block after each (`package-upgrade`, `cpu-batch`'s `python3`), `cycles` (`video-call`); `dataset/tools/wlc/compiler.py` `_replay_window` checks the kind; `dataset/variants.yaml`'s `trace-replay` comment and `dataset/tools/wlc/variants.py`'s docstring name the three kinds. The variants manifest's `replay` fields: the upgrade's runs in `c7-dev`, `c7-browsing` and `c7-meeting`, `python3`'s in `c2-p1a`, the call's cycles in `c7-meeting` — every replay file replays a batch job's runs. G3 applied the same restatement in vol-04 (its N2: §11.3's table, §11.4's replay axis, the glossary's `replay` row).
- Sources: `logs/G3.md` ## Rows for other chunks (X1); `dataset/replay/*.json.gz` `kind`; `dataset/tools/wlc/compiler.py` `_replay_window`; `dataset/variants.yaml`'s `trace-replay` comment since `7b024003`
- Cross-ref: W-0876; W-0951
- Notes: found in G3. K11's file: a follow-up chunk.

### W-0957 · applied
- At: `docs/guidebook/dataset/02-the-archetype-library.md` line 1, the H1 ("# 2권 · Archetype library: process 하나를 scheduler의 눈으로 적기"); `docs/guidebook/dataset/README.md` line 14, the volume table's vol-02 row, which quotes the title verbatim
- Change: The title's "process 하나" (one process) keeps the term the archetype plan's §1 dropped; the plan now reads "one kind of program as the scheduler sees it". If the title changes, `docs/guidebook/dataset/README.md:14` follows it verbatim in the same change.
- Final word: `docs/workload/archetype-plan.md` §1 (`:8`) reads "a **generative model of one kind of program as the scheduler sees it**" since `18127cc9` (2026-10-16, K04): most entries merge a measured application's whole process tree into one task; `compiler-child` is six tasks. The research guidebook vol-06's 재구축 이후 note (`docs/guidebook/vol-06-archetypes-and-grounding.md:83`) records the change; K18 restated `docs/README.md`'s archetype-plan line and its Full-index row to "one kind of program" (K18's N6).
- Sources: `logs/K18.md` ## Fix round 1, Rows for other chunks (added) (X2); `docs/workload/archetype-plan.md` §1
- Cross-ref: W-0874; W-0924
- Notes: found in K18. K11's file: a follow-up chunk; `docs/guidebook/dataset/README.md` is K18's file, edited in the same change.

### W-0971 · applied
- At: `docs/guidebook/dataset/02-the-archetype-library.md` §2.8, line 407 ("(scholarly 5, deployed-system 12, measurement 2; python으로 세어 확인) … type은 셋입니다") and line 413 ("registry의 `type`은 셋뿐이라 `sources.yaml`에서는 `deployed-system`으로 남아 있습니다"); §4.1's `game-task-chain` "어디서 왔나" paragraph, line 684 ("registry(`sources.yaml`)에서 이 출처의 type은 deployed-system이고, notes는 "Slides are footnote-tier despite carrying numbers"라고 적습니다")
- Change: Line 407: the tally becomes scholarly 5, deployed-system 11, talk, conference abstract or news report 1, measurement 2, and the types four. Line 413: the registry has given `lavd-ossna24` the talk type since 2026-10-17. Line 684: the type clause becomes talk, conference abstract or news report since 2026-10-17; the notes clause stays (the notes are unchanged). In the volume's Korean.
- Final word: 인지오's answer (b) of 2026-10-17 to the work list's "K13 (M2), K01 (M1) · the registry's `lavd-ossna24` type", applied in L1: `dataset/sources.yaml:58` gives `lavd-ossna24` the type "talk, conference abstract or news report", and the header's `type` rule (`:14–25`) lists `docs/references.md`'s id-rule types (scholarly, deployed-system, talk, conference abstract or news report, measurement) with each tier in the citation-tier rule's wording, condensed, none for measurement. The registry's 19 ids: scholarly 5, deployed-system 11, talk, conference abstract or news report 1 (`lavd-ossna24`), measurement 2 (L1's count by `yaml.safe_load`). L1 applied the same tally in the dataset guidebook vol-06 §2.1 (its N1, `:132`). `lavd-ossna24`'s `notes` (`:60–73`) are unchanged and still end "Slides are footnote-tier despite carrying numbers" (`:72–73`); L1's M1, a question for 인지오.
- Sources: `logs/L1.md` ## Rows for other chunks (X2), ## Fix round 2 (R2); `dataset/sources.yaml:58`, `:72–73`
- Cross-ref: W-0970; W-0972
- Notes: found in L1. K11's file: a follow-up chunk, with W-0970. If 인지오's answer to L1's M1 restates the notes, line 684's account of them follows.

### W-0991 · applied
- At: `docs/guidebook/dataset/02-the-archetype-library.md` line 889 at `3ac13c42`, 890 after N5's edit ("idle 재측정(9.10 D146)")
- Change: Keep D146's 2,790 s reading on `kdenlive` 10 as history; add 9.15's span check: over `c3-creation`'s 2,851 s span, `kdenlive` 13 (`meas-ci-probes-2026-10-17`), the 180 s phase holds (CPU 0.3 %, wakes 2.9 %; at the worst 4.5 %, 3.8 %). In the volume's Korean.
- Final word: As W-0989.
- Sources: `logs/N4.md` ## Rows for other chunks (X3)
- Cross-ref: W-0989; W-0990; W-0992
- Notes: found in N4. K11's file: a follow-up chunk.

## Also on this file, not for editing from this list

- W-0517 · applied 2026-10-17 after 9.15's close in T1 (the skip rule in the guidebooks; was blocked, simulator TIMER) — §1.5 TIMER와 WAIT(timer), open note line 135
- W-0734 · waits on 인지오 — Is the collection and privacy-scrub tool still promised? What the records and code say: grill 2026-08-26 D8 (`_dev/archive/2026-08-26-workload-generation-grill.md:29`) promised it ships 'as an open falsification invitat… Blocks: `docs/workload/building-plan.md:209`, `docs/workload/grounding-sources.md:48` (W-0295), the dataset guidebook vol-02 §12.2 note and vol-06's mismatch row, the…
