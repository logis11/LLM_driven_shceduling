# Work-list rows — `docs/guidebook/dataset/06-grounding-measurement-verification.md`

Chunk K13, Dataset guidebook, volumes 5-6 (wave 3). 20 open rows. The file has 1847 lines at `d5cc7711`.

### W-0562 · open
- At: `docs/guidebook/dataset/06-grounding-measurement-verification.md` §2.1 두 장부, open note line 136; §14.4 table row line 1705 (`dhakal-chi18` 두 번)
- Change: Once `docs/references.md` holds one `### dhakal-chi18` entry, close the note and the §14.4 row, stating the single entry's role line instead of the duplicate.
- Final word: `docs/references.md` has two `### dhakal-chi18` entries (lines 35 and 65) with different role lines ('stimulus of the 9.5 campaign's stimulus-sensitivity check only'; 'Role C, typing study … Paper-only after Phase 9'); the 2026-10-10 audit and record-gaps §2 item 11 carry the duplicate to 9.15, whose references chunk merges them into one entry carrying the data artifact, the stimulus-check role (9.5 D23) and the paper-only note.
- Sources: SX-1054 (guidebook dataset vol-06 open note (§2.1), `dataset/06-grounding-measurement-verification.md:136`)
- Cross-ref: W-0563; W-0564; W-0565; W-0566; W-0567; W-0568; W-0571; W-0573; W-0574; W-0577; W-0578
- Notes: Waits on the references chunk's `dhakal-chi18` rows (another row: W-0005); that chunk runs first (spec decision 5).

### W-0563 · open
- At: `docs/guidebook/dataset/06-grounding-measurement-verification.md` §2.2 id를 만드는 규칙, the section body's account of the id types (lines 138–150) and open note line 152; §14.4 table row line 1706 (id 규칙 type 셋)
- Change: Once `docs/references.md`'s id-minting rule carries 9.12 D110's `meas-local` form and D113's fifth type, describe them as the current rule in §2.2 (the body as well, if it lists three types) and close the note and the §14.4 row.
- Final word: 9.12 D110 (2026-10-09, by 인지오's decision): a `meas-local:<machine>-<subject>:<date>` id form for laptop measurements (its entry `meas-local:m1pro-llm:2026-10-08`); 9.12 D113: a fifth type for talks, conference abstracts and news reports, `<label>-<venue><yy>`, footnote tier, stated only as the speaker's or reporter's claim, with `lavd-ossna24` and `corbet-lwn24` moved under it; both handed to 9.15; at HEAD `docs/references.md` holds neither (`grep meas-local` empty).
- Sources: SX-1055 (guidebook dataset vol-06 open note (§2.2), `dataset/06-grounding-measurement-verification.md:152`)
- Cross-ref: W-0562; W-0564; W-0565; W-0566; W-0567; W-0568; W-0571; W-0573; W-0574; W-0577; W-0578
- Notes: Waits on the references chunk's id-rule rows (another row: W-0055, W-0001).

### W-0564 · open
- At: `docs/guidebook/dataset/06-grounding-measurement-verification.md` §2.3 인용 등급 규칙과 상태 표시, open note line 166; §14.4 table row line 1707 (deployed-system 'existence claims only')
- Change: Once `docs/references.md`'s citation-tier rule (line 21, and the section heading at line 185) carries 9.12 D112, describe the widened deployed-system tier as the current rule and close the note and the §14.4 row.
- Final word: 9.12 D112 (2026-10-09, by 인지오's decision): the deployed-system tier admits, beside existence claims, (i) a system's documented design or behaviour, stated as that version's, and (ii) figures the source published as its own report, stated as its report with date, window and method — never a behavioural or statistical claim stated as the paper's own or a population's; handed to 9.15; `docs/references.md:21` still reads 'existence claims only'.
- Sources: SX-1056 (guidebook dataset vol-06 open note (§2.3), `dataset/06-grounding-measurement-verification.md:166`)
- Cross-ref: W-0562; W-0563; W-0565; W-0566; W-0567; W-0568; W-0571; W-0573; W-0574; W-0577; W-0578
- Notes: Waits on another row's tier-rule rows (W-0002).

### W-0565 · open
- At: `docs/guidebook/dataset/06-grounding-measurement-verification.md` §2.4 `sources.yaml`의 30개 id — heading line 168, the registry table lines 172–190 (rows 183–185 name `dkms-man`, `dkms-debian`, `dubroy-chi10`, `chang-chi21`, `mozilla-testpilot10`), the count paragraph line 192, the history paragraph line 194, open note line 196; §14.4 table rows lines 1703–1704
- Change: If `dataset/sources.yaml` drops ids (9.10 D34's seven, or any id that grounds nothing — an outside-sweep edit, 인지오's), restate §2.4's heading count, table, used and unused counts and history paragraph to the registry as it then stands, and close the note and the two §14.4 rows; if the registry stays, restate the note to that decision. The verification-round table (lines 462–474, the 2026-09-13 reads R01–R11) stays.
- Final word: 9.10 D34 (2026-10-01): `procyon`, `dkms-man`, `dkms-debian`, `gamemode-docs`, `dubroy-chi10`, `chang-chi21` and `mozilla-testpilot10` leave `dataset/sources.yaml` (handed to 9.13, not applied; all seven are in the registry at HEAD). 9.12 D102 under 9.10 D34: `dkms-man`, `dkms-debian`, `dubroy-chi10`, `chang-chi21` and `mozilla-testpilot10` are cited by none of the related-work, proposal, research-claims or background-guide prose nor guidebook vol-02, so 9.15 removes their `docs/references.md` entries and restates in the same edit the lines that still cite them (the dated memos keep their text). The TODO 9.15 line carries 'the `dataset/sources.yaml` ids that ground nothing'.
- Sources: SX-0177 (TODO 9.15 line (from 9.12 audit D102), `_dev/TODO.md:179`); SX-1057 (guidebook dataset vol-06 open note (§2.4), `dataset/06-grounding-measurement-verification.md:196`)
- Cross-ref: W-0562; W-0563; W-0564; W-0566; W-0567; W-0568; W-0571; W-0573; W-0574; W-0577; W-0578
- Resolved at merge: SX-0177 also asked to update the verification-round table (lines 470–473) 'when the entries leave docs/references.md'. Read the target: that table lists what the 2026-09-13 readers R01–R11 read — a dated record — so it stays; §2.4's table describes the registry, so it follows `sources.yaml`, not `docs/references.md`.
- Notes: `dataset/sources.yaml` is outside the sweep (another row: W-0791, W-0789): not a manifest input, but the linter (`dataset/tools/wlc/linter.py:36–42`) fails any registry id without a `### <id>` entry in `docs/references.md`, so the registry must drop an id before the references chunk removes its entry. Counted at HEAD: 30 ids, 11 used as tags (the volume's count holds).

### W-0566 · open
- At: `docs/guidebook/dataset/06-grounding-measurement-verification.md` §2.4, open note line 198 (`ocallahan-atc17`); §14.4 table row line 1702
- Change: Once `docs/references.md:107`'s role line (and, if 인지오 takes the outside-sweep row, `dataset/sources.yaml:78`'s note) say the 2,430 processes are a `make -j8` build of DynamoRio 6.1.0 (the paper's §4.3), or the id leaves the registry, close the note and the §14.4 row, naming which lines now say it; a line left unchanged stays named.
- Final word: Critical findings memo A1 (2026-09-13): `ocallahan-atc17`'s 2,430 processes come from a DynamoRio 6.1.0 build, not a Linux kernel build; at HEAD `dataset/sources.yaml:78` still says 'Linux kernel-build workload' and `docs/references.md:107` '(§4.3, kernel-build workload; …)'; the TODO 9.15 line carries both; the id grounds no value (0 tags).
- Sources: SX-1058 (guidebook dataset vol-06 open note (§2.4), `dataset/06-grounding-measurement-verification.md:198`)
- Cross-ref: W-0562; W-0563; W-0564; W-0565; W-0567; W-0568; W-0571; W-0573; W-0574; W-0577; W-0578
- Notes: Waits on another row: W-0013 (`docs/references.md`, in scope) and W-0790, W-0789 (`dataset/sources.yaml`, outside the sweep; a note edit there is not a manifest input and moves no pin).

### W-0567 · open
- At: `docs/guidebook/dataset/06-grounding-measurement-verification.md` §2.9 `grounding-sources.md`, open note line 289; §14.4 table row line 1713
- Change: Once `docs/workload/grounding-sources.md` has had 9.15's full pass (spec decision 4), close the note and the §14.4 row and restate §2.9's list of its stale lines to what the doc now says.
- Final word: The TODO 9.15 line hands `grounding-sources.md`'s stale lines to 9.15 — 9.10 D1 (`zhang-chb15` dropped; `:81`), 9.11 D12 (`:29–30` brought to the corrected precedent entries), 9.12 (`:18`, `:30`, `:32`, `:74`); as a doc that explains the dataset it gets a full pass against the code (9.15 spec decision 4).
- Sources: SX-1059 (guidebook dataset vol-06 open note (§2.9), `dataset/06-grounding-measurement-verification.md:289`)
- Cross-ref: W-0562; W-0563; W-0564; W-0565; W-0566; W-0568; W-0571; W-0573; W-0574; W-0577; W-0578
- Notes: Waits on another row's `grounding-sources.md` rows (e.g. W-0297, W-0294, W-0289–W-0292, W-0286–W-0293).

### W-0568 · open
- At: `docs/guidebook/dataset/06-grounding-measurement-verification.md` §2.10 `source-vetting.md`, open note line 311; §14.4 table row line 1714 ('append-only 기록; 9.15의 처리 방식 미정')
- Change: Close the note and the §14.4 row: `docs/workload/source-vetting.md` is 'Status: record — append-only', so its corrections are appended dated notes naming each corrected line (`:52`, `:57`, `:58`, `:61`, `:64`, `:66`, `:67`, `:87`, `:90` and the others handed), not edits in place; say so once that chunk has appended them.
- Final word: 9.11 D12 and 9.12's decisions hand corrections of `source-vetting.md`'s precedent lines (52, 57, 58, 61, 64, 66, 67, 87, 90) to 9.15; the file's header is 'Status: record — append-only', so its corrections are appended dated notes naming the corrected line, not edits in place.
- Sources: SX-1060 (guidebook dataset vol-06 open note (§2.10), `dataset/06-grounding-measurement-verification.md:311`)
- Cross-ref: W-0562; W-0563; W-0564; W-0565; W-0566; W-0567; W-0571; W-0573; W-0574; W-0577; W-0578
- Resolved at merge: The note left the method to the editing agent. Read `docs/workload/source-vetting.md:2` ('Status: record — append-only'); the docs' header rule makes a record append-only, so the method is appended dated notes.
- Notes: Waits on another row's `source-vetting.md` rows (e.g. W-0299, W-0311, W-0307–W-0306, W-0303, W-0305, W-0311).

### W-0569 · open
- At: `docs/guidebook/dataset/06-grounding-measurement-verification.md` §3.2 결정 1 — 검증 기준, open note line 366
- Change: Restate the note: the timeline lint's three labels (`BOUND_LABELS = ("design", "convention", "arithmetic")`, `dataset/tools/wlc/linter.py:199`) are 9.10 D32's, the later decision for the timelines' bound values, so Phase 9 decision 1's fourth label `placeholder` has no form there; a value awaiting measurement cannot enter the library after the freeze, which `make lint` itself enforces since 9.23 D13 (`lint.py --freeze` rejects `meas-pending`).
- Final word: Phase 9 decision 1 (2026-09-13): a value no source states carries no source tag and is labelled for what it is — convention, arithmetic, placeholder or design. 9.10 D32 (later): a bound value no source states carries one of three labels, which the timeline lint holds (`linter.py:199`). 9.23 D13 (2026-10-15): `make lint` runs `lint.py --freeze`, which rejects a `meas-pending` tag ('meas-pending after freeze'); the library holds none.
- Sources: SX-1061 (guidebook dataset vol-06 open note (§3.2), `dataset/06-grounding-measurement-verification.md:366`)
- Resolved at merge: The raw row left the note to 인지오's answer. Read `linter.py:199` (its comment cites 9.10 D32) and the 9.23 changelog's D13: the label set follows the later decision and the freeze rule now runs in `make lint`, so the note can state the rule instead of an open question.
- Notes: No placeholder remains in the dataset (the note says so). A form for future values awaiting measurement would be a new decision; no record asks for one.

### W-0570 · open
- At: `docs/guidebook/dataset/06-grounding-measurement-verification.md` §3.6 결정 5 — 측정 장소, open note line 420; §14.3 item 13, line 1688 ('library 수준의 한계로 진술할 것 … 9.15 할 일')
- Change: Once the library-level scale limitation is stated, close the note and restate §14.3 item 13, naming where the statement lives.
- Final word: 9.5 follow-ups spec decision 13 ('Scale limitation at the composition seam'): composing archetypes measured at different venues (the runner-measured editor beside the LAVD-talk game chain) is a limitation 'stated once at the library level'; the sensitivity check went to 9.14; the statement is missing at HEAD from `dataset/archetypes.yaml`, `dataset/README.md` and `docs/` (record-gaps §1 item 2).
- Sources: SX-1063 (guidebook dataset vol-06 open note (§3.6), `dataset/06-grounding-measurement-verification.md:420`)
- Notes: Waits on another row's `dataset/README.md` rows (W-0238) and another row's `docs/workload/archetype-plan.md` row (W-0238).

### W-0571 · open
- At: `docs/guidebook/dataset/06-grounding-measurement-verification.md` §4.4 critical findings memo의 발견들과, open note line 516; §14.4 table row 1, line 1701
- Change: Restate the note and the §14.4 row with 인지오's answer on the Phase 9 spec's and the 2026-10-10 audit's count of 13 (which summary row it leaves out, or a miscount); with no answer the note stays 확인 필요 (needs checking), the volume covering all fourteen rows.
- Final word: `docs/memos/2026-09-13-critical-findings.md`'s Summary table has fourteen rows (A1–A5, B1–B7, C, D; lines 11–24); the Phase 9 spec (line 7, 'The 13 findings') and the 2026-10-10 audit (line 49, 'the 13 + 6 critical findings') count 13; no record says which row the count leaves out (record-gaps §1 item 6).
- Sources: SX-1064 (guidebook dataset vol-06 open note (§4.4), `dataset/06-grounding-measurement-verification.md:516`)
- Cross-ref: W-0562; W-0563; W-0564; W-0565; W-0566; W-0567; W-0568; W-0573; W-0574; W-0577; W-0578
- Waits on: W-0749 (인지오's answer; the row applies once it is given, or is logged as waiting)
- Notes: Waits on the for-인지오 row from W-0749. Other groups restate their docs' counts to the memo's fourteen summary rows (W-0505, W-0529; W-0816); this volume already says fourteen.

### W-0572 · open
- At: `docs/guidebook/dataset/06-grounding-measurement-verification.md` §4.4, the findings table row A5, line 526 ('9.12 D1은 이것을 `whitelist` 비교 조건이 재현하는 이름 기반 카탈로그로 다룸')
- Change: Name the shipped-catalogue condition (`shipped_catalogue`, 9.12 D6 and D105) as the comparison condition that reproduces the `ananicy-rules` catalogue, in place of 'the `whitelist` comparison condition'.
- Final word: 9.12 D6, amended by D91, D105, D109 and D115: the `whitelist` condition becomes two. The shipped-catalogue condition (`shipped_catalogue`) reproduces the CachyOS catalogue (`ananicy-rules` at `03ef03fb`) as CachyOS installs and enables it with ananicy-cpp, matched by the basename of each process's `argv[0]`, untruncated (D105); on ananicy-cpp's key it keys 19 of the 35 bound names and every name in only 7 of 50 files (D109); it answers RQ2 (research question 2, value: 'does that reading beat what shipping systems do?', D115). The strongest-name-table condition (`strongest_name_table`) is a rule list in the catalogue's design covering the software the dataset presents as known, with no rule for Family 3's unregistered software or the invented names of familiarity tiers 4–5; it carries the paper's claim (D115), is the condition expected to score perfectly on the C1 (the single-situation calibration group) files, and fails structurally on world knowledge. 'A faithful reproduction of what shipping systems do today' and 'the whitelist approach real operating systems currently use' are restated to the two conditions (D91).
- Sources: S12-051 (9.12 D6, `task-9.12-related-work-prose/changelog.md:114`)
- Notes: Condition identifiers in code: `harness/tools/harness/evaluator.py:47`, `harness/guards/guard-spec.yaml:126` (S12-051's ':116' is `:126`).

### W-0573 · open
- At: `docs/guidebook/dataset/06-grounding-measurement-verification.md` §5.2 9.3, open note line 666; §14.4 table row line 1711 (`dataset/README.md:18`)
- Change: Once 인지오 has decided whether `dataset/meas/summary.json` stays as the record of the 2026-08-28 campaign (the critical findings memo cites it) or leaves the tree, and `dataset/README.md`'s `meas/` line describes it accordingly, close the note and the §14.4 row, stating the outcome and the README's current line number.
- Final word: 9.3 decision 5 left `dataset/meas/summary.json` unchanged; no current dataset value derives from it (an orphaned Phase 2 analysis, the 2026-10-10 audit); `dataset/README.md:27` still lists it ('analysis summary'); its fate is on the TODO 9.15 line.
- Sources: SX-1065 (guidebook dataset vol-06 open note (§5.2), `dataset/06-grounding-measurement-verification.md:666`)
- Cross-ref: W-0562; W-0563; W-0564; W-0565; W-0566; W-0567; W-0568; W-0571; W-0574; W-0577; W-0578
- Waits on: W-0784 (인지오's answer; the row applies once it is given, or is logged as waiting)
- Notes: Waits on the for-인지오 rows from W-0784 and another row's README `meas/` rows (W-0196). Deleting `summary.json` is a data-file edit (outside the sweep); it is no manifest input.

### W-0574 · open
- At: `docs/guidebook/dataset/06-grounding-measurement-verification.md` §6.8 이름 검증: `dataset/meas/names/`, open note line 850; §14.4 table row line 1716 (`dataset/meas/names/`)
- Change: Restate the note and the §14.4 row with 인지오's answer: the names' grounding moved to the campaign traces' comms by decision (the note states it), or a re-run of the fixed `verify_names.py` over the current names is owed (the note names its TODO line); with no answer it stays 확인 필요.
- Final word: No record re-verifies the current timeline names with the fixed `verify_names.py`; the names' grounding appears to have moved from the name-verification tables (`dataset/meas/names/`, which still hold old names such as `tracker-miner-fs-3`, `clamscan`) to the campaign traces' comms, but no decision records the move (record-gaps §1 item 6); the 9.16 TODO line names no name re-verification.
- Sources: SX-1068 (guidebook dataset vol-06 open note (§6.8), `dataset/06-grounding-measurement-verification.md:850`)
- Cross-ref: W-0562; W-0563; W-0564; W-0565; W-0566; W-0567; W-0568; W-0571; W-0573; W-0577; W-0578
- Waits on: W-0738 (인지오's answer; the row applies once it is given, or is logged as waiting)
- Notes: Waits on the for-인지오 row from W-0738.

### W-0575 · open
- At: `docs/guidebook/dataset/06-grounding-measurement-verification.md` §8.4 시간 창과 긴 탐침, line 1038 ('`c6-dual`은 12,068 s 동안 VS Code에 초점을 둡니다')
- Change: Restate the example in the past: `c6-dual` held VS Code focused for 12,068 s before 9.17 D1 alternated its focus with the game every 686–688 s — the span the code editor's span probes were read over, as the library's scope clause states it since 9.23 D8; the probes' length and readings are unchanged, so the probe's purpose still reads.
- Final word: 9.23 D8 (2026-10-14, by 인지오's decision): the `code-editor` entry's validation scope in `dataset/archetypes.yaml` (written by `dataset/tools/meas/campaign/fold_in.py`) reads 'Read over 12,068 s, the span `c6-dual` held it focused before its focus alternated with the game every 688 s (9.17 D1), in two long-phase probes …'; since 9.17 D1 cut the editor's typing into nine windows of 686–688 s following its focus turns, its longest focused stretch in `c6-dual` is 686–688 s; the probes' length and readings are unchanged; the library's bytes changed and every artifact was rebuilt (9.23 D10).
- Sources: SX-0362 (TODO 9.15 line (from 9.23 D8), `_dev/TODO.md:179`); SX-0614 (9.23 D8, `task-9.23-guidebook-findings/changelog.md:80`); SX-1053 (9.23 D8 (copy in guidebook dataset vol-06 §8.4), `dataset/06-grounding-measurement-verification.md:1038`)
- Notes: Checked at HEAD: the clause is in `dataset/archetypes.yaml` as quoted. 9.23 D8 hands the guidebook's copies of the clause: vol-02 `:815`, vol-04 `:1552`, vol-06 `:1038`.

### W-0576 · open
- At: `docs/guidebook/dataset/06-grounding-measurement-verification.md` §8.6 빌드 혼합과 RQ0의 민감도 variant, open note line 1062
- Change: Restate the note with 인지오's answer on the venue variants' bracket (keep ×0.8–1.25, its stated basis being the two measured venue effects, not the cross-CPU spread; or widen it to the measured 0.50–0.72×); with no answer it stays 미정 (undecided).
- Final word: The 2026-10-10 audit's fidelity map: the venue sweep ×0.8–1.25 is narrower than 9.6's measured cross-CPU spread (Xeon 0.50–0.72× of EPYC time); the RQ0 gate spec states the bracket's basis — 'the lower edge of a design bracket containing the two measured venue effects — the ×1.144 huge-page ratio … (9.10 D88) and the tracing overhead's ×1.02 to ×1.16' (`harness/experiments/rq0-gate.yaml:146`); no record decides whether to widen it; the venue variants first run in Phase 10.
- Sources: SX-1072 (guidebook dataset vol-06 open note (§8.6), `dataset/06-grounding-measurement-verification.md:1062`)
- Waits on: W-0752 (인지오's answer; the row applies once it is given, or is logged as waiting)
- Notes: Waits on the for-인지오 row from W-0752. A widened bracket edits `dataset/variants.yaml`: the variants manifest's re-bless and the RQ0 gate spec's `pins.variants` re-pin.

### W-0577 · open
- At: `docs/guidebook/dataset/06-grounding-measurement-verification.md` §9.2 release 목록, open note line 1118; §14.4 table row line 1708 (`dataset/README.md:167`)
- Change: Once the root `LICENSE` and `dataset/LICENSE` exist and `dataset/README.md`'s tag and raw-data sentence matches the code, restate the note — the licences in place; the release URL and asset hash beside each value and the manual releases as decided or still open — and the §14.4 row to the README's new sentence.
- Final word: Of the 2026-10-10 audit's four data-availability points: the licences are decided by 9.15 spec decision 12 — a root `LICENSE` puts the code under MIT; `dataset/LICENSE` puts the dataset's data and its release assets under CC-BY-NC-SA-4.0; both name Jioh In, Kyungmin Inn and Ian Park as the copyright holders; `dataset/LICENSE` credits SWELL-KW (Koldijk et al., 2014, DANS) for the stimulus streams; the release URL and asset hash beside values and the release automation have no decision; `dataset/README.md:167`'s 'raw data lives on the GitHub release named in the tag's registry entry' is untrue (the registry names no release; the tag is the campaign date, 9.5 D27).
- Sources: SX-1074 (guidebook dataset vol-06 open note (§9.2), `dataset/06-grounding-measurement-verification.md:1118`)
- Cross-ref: W-0562; W-0563; W-0564; W-0565; W-0566; W-0567; W-0568; W-0571; W-0573; W-0574; W-0578; W-0588
- Waits on: W-0733 (인지오's answer; the row applies once it is given, or is logged as waiting)
- Notes: Waits on another row's licence rows (W-0239, W-0240) and another row's README data-availability and tag rows (W-0218, W-0217). The release-publication question is vol-07 §1.7's (W-0588; the for-인지오 row from W-0733).

### W-0578 · open
- At: `docs/guidebook/dataset/06-grounding-measurement-verification.md` §9.3 기록이 나뉘어 있는 곳, open note line 1137; §14.4 table rows lines 1712 (`measurement-overview.md`) and 1715 (the campaign record's Campaigns table)
- Change: Once `docs/workload/measurement-overview.md` is brought to the library, close that half of the note and its §14.4 row; restate the note's last sentence ('기록의 표를 고칠지는 정해지지 않았습니다') as settled — the `_dev/` campaign record stays as dev history, untouched by 9.15 (spec decision 11) — and its §14.4 row likewise.
- Final word: `measurement-overview.md` says 'The 23 archetypes', lists `file-backup` and `renderer-visible` (not in the library), omits the seven 9.10 entries (`module-build-orchestrator`, `module-compiler-child`, `package-upgrade`, `file-indexer`, `video-transcoder`, `incremental-backup`, `game-download-idle`) and 9.10's releases; the library has 28 measured entries (`category_source: meas`); the overview is on the 9.15 line and, as a doc explaining the dataset, gets the full pass (spec decision 4). 9.15 spec decision 11: the existing files under `_dev/` are not touched — `_dev/research/jioh/measurement-campaign-record.md`'s Campaigns table stays as it is.
- Sources: SX-1076 (guidebook dataset vol-06 open note (§9.3), `dataset/06-grounding-measurement-verification.md:1137`)
- Cross-ref: W-0562; W-0563; W-0564; W-0565; W-0566; W-0567; W-0568; W-0571; W-0573; W-0574; W-0577
- Notes: Waits on another row's measurement-overview rows (W-0269, W-0267, W-0265).

### W-0579 · open
- At: `docs/guidebook/dataset/06-grounding-measurement-verification.md` §11.3 fidelity map, open note line 1347
- Change: Restate the note with 인지오's answer on the 2026-09-20 validity memo §5's two routes (the scoping carried into the paper, or one bounded comparison against a real desktop); with no answer it stays open.
- Final word: The 2026-09-20 validity memo §5 offers carrying the scoping into the paper or one bounded comparison against a real desktop with a display and a GPU; the comparison is neither decided nor run; grill 2026-08-26 D8 removed teammates' live-desktop measurement ('No teammate Linux desktops known'), unchanged since.
- Sources: SX-1077 (guidebook dataset vol-06 open note (§11.3), `dataset/06-grounding-measurement-verification.md:1347`)
- Waits on: W-0753 (인지오's answer; the row applies once it is given, or is logged as waiting)
- Notes: Waits on the for-인지오 row from W-0753. §14.3 item 1 ('실제 데스크톱 검증은 미뤄짐') follows the same answer.

### W-0580 · open
- At: `docs/guidebook/dataset/06-grounding-measurement-verification.md` §14 intro line 1628 ('9.15는 [WIP]'); §14.1 9.15: 문서, memo, guidebook 정리 — body lines 1632–1641 and open note line 1643
- Change: At 9.15's end, restate §14.1 from plan to outcome and close the note: 9.15 done; the final memo's language as decided and where the final memo lives; the licences in place (root `LICENSE` MIT, `dataset/LICENSE` CC-BY-NC-SA-4.0); the chunk logs in 9.15's research folder as its record.
- Final word: 9.15 spec (2026-10-14): the only open item is the final memo's language, decided at the memo step; 9.15 is done when spec decision 14's conditions hold — every work-list row closed, every chunk passed its reviewer and committed, 인지오 has read every chunk log and every overturned decision is applied, every logged code-versus-decision mismatch has 인지오's answer (any code work on its own `_dev/TODO.md` line), every memo carries its open or closed line, and the final memo is committed; 9.16's exit audits run on that state.
- Sources: SX-1080 (guidebook dataset vol-06 open note (§14.1), `dataset/06-grounding-measurement-verification.md:1643`)
- Cross-ref: W-0581; W-0602
- Deferred: after the final memo is committed (9.15 spec decision 13): applied by a follow-up on this file, not in the chunk's wave
- Notes: Sequencing: the final memo comes after the doc chunks (spec decision 13), so this edit runs last — with or after the final memo's commit, beside the vol-08 §12.1 row (W-0602). §14.2's note on 9.16 stays (W-0585).

### W-0581 · open
- At: `docs/guidebook/dataset/06-grounding-measurement-verification.md` §14.2 9.16: exit audits, the table of the 9.16 line's checks — row 'each sub-task's manifest and pin hashes' line 1662 (ends at 9.21) and the table's end
- Change: Add the 9.16 line's 9.23 item (9.23 D15: the full smoke at home, `make -C harness smoke`, on the final build, its time recorded) as a row, and name the current pins as 9.23 D17's — dataset `81d3213d…`, variants `7079e677…`, scoring spec `2ad757b6…`; generated transition grid `826c719c…`, return grid `392d6071…`, flap-stress `97ba813f…`, distractor grid `919bb2c0…`, familiarity ladder `b6f82df5…` — which the 2026-10-11 review's item ('the five gate pins and the generated layer's pins equal the committed bytes') checks.
- Final word: 9.23 D10 (2026-10-14) and D17 (2026-10-15) re-blessed after 9.21: D10 dataset `c5f7fa5a…`, variants `8986b58a…`, scoring spec `2ad757b6…`, generated `3035cfe3…`/`2e381b42…`/`90cc782a…`/`e61fd777…`/`1a7d35d7…`; D17 — the current pins — dataset `81d3213d…`, variants `7079e677…` (the RQ0 gate spec, `harness/experiments/rq0-gate.yaml:485–490`), the scoring spec at D10's `2ad757b6…`, generated `826c719c…`/`392d6071…`/`97ba813f…`/`919bb2c0…`/`b6f82df5…`. The 9.16 TODO line (`_dev/TODO.md:180`) carries from 9.23 only D15's full smoke at home on the final build.
- Sources: SX-0626 (9.23 D10, `task-9.23-guidebook-findings/changelog.md:98`)
- Cross-ref: W-0580; W-0604
- Resolved at merge: The raw row asked to add 9.23's D10 and D17 pins to the table. Read the 9.16 TODO line: the table mirrors it, and the line carries no 9.23 pins, only D15's smoke; D17's pins supersede D10's and are what the 2026-10-11 review's item checks. So the table gains the smoke row and names D17's pins as current.
- Notes: Checked at HEAD: `shasum -a 256` of the seven manifests and the scoring spec equals D17's values and the RQ0 gate spec's pins. The same change on vol-08 §12.2's list is W-0604.

### W-0847 · open
- At: `docs/guidebook/dataset/06-grounding-measurement-verification.md` line 144 (the id rule's scholarly bullet, examples `cpsmark-tbench23`, `lavd-ossna24`), line 159 (the tier rule: 'Supports **existence claims only**'), the §2.4 registry table lines 175–185, the §14.4 mismatch rows at lines 1703 (9.10 D34's seven ids, "9.13에서 적용되지 않음"), 1707 (the tier rule, "미반영") and 1718 (`chang-chi21`'s role)
- Change: Copy the rules as `docs/references.md` now states them — five source types, the scholarly example no longer `lavd-ossna24` (re-typed to the talk type), the deployed-system tier as 9.12 D112 widened it; the registry table to the 19 ids `dataset/sources.yaml` keeps; the three mismatch rows resolved (the seven ids left the registry, W-0791; the tier rule widened, W-0002; `chang-chi21` removed, W-0071). The 2026-09-13 reads table (lines 472–474) is history: at most a note that the ids left.
- Final word: 인지오's answers to W-0071 (a) and W-0072 (a), applied in K01; W-0789's answer as corrected in stage A (the registry keeps 19 ids; `sysmark25`, `rt-app`, `focal-arxiv26`, `mark-chi05` removed; `logs/A1-registry.md`); 9.12 D112 and D113, applied in K01 (W-0001, W-0002).
- Sources: W-0001; W-0002; W-0071; W-0789; `logs/K01.md` ## Rows for other chunks
- Cross-ref: W-0564; W-0565
- Notes: found in K01. W-0564 closes the tier-rule note and row 1707; W-0565 restates §2.4 to the registry as it stands; apply together.

## Also on this file, not for editing from this list

- W-0582 · closed, carried — Waits on Phase 10's RQ0 run, nothing owed in 9.15: the Phase 10 section line `_dev/TODO.md:190` ('… judge per the RQ0 gate spec') carries it, and the RQ0 gate…
- W-0583 · closed, carried — Waits on Phase 10, nothing owed in 9.15: the Phase 10 line `_dev/TODO.md:191` carries the trace-replay check; the note is accurate at HEAD (not run; what follo…
- W-0584 · closed, carried — Waits on the backlog, nothing owed in 9.15: `_dev/TODO.md:196` ('Naturalistic generator + generalset + full condition matrix …') carries it; the note quotes th…
- W-0585 · closed, carried — Waits on 9.16, nothing owed in 9.15: the 9.16 line `_dev/TODO.md:180` carries it; the note's sentences stay true when 9.15 ends. The row's suggestion on §14.2'…
- W-0751 · waits on 인지오 — Does `dataset/tools/meas/` get a README? What the tree says: no README under `dataset/tools/meas/`; each tool carries a docstring; the workflow document's Tooling section lists them. A new file under `dataset/tools/` is… Blocks: The dataset guidebook vol-06 §6.4 note.; also the §6.4 note at docs/guidebook/dataset/06-grounding-measurement-verification.md:783
