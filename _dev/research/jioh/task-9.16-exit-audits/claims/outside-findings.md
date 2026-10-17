# 9.16 claim audit — claims outside the workload dataset: findings

Every claim of `outside-inventory.md` that is not TRACED or LABELLED: 75 of 353 claims (WORDING-OUTSIDE-PASSAGE 41, RECORD-BELOW-STANDARD 23, NO-RECORD 11), plus one stale statement about the registry (dataset guidebook vol. 08, end of part F). Repository `928aa8fd`, read 2026-10-17. Path abbreviations are each part's, as listed in `outside-inventory.md` ("Columns and path abbreviations"). Nothing here is applied; the fixes are proposals for the lead.

## One cause, several places

The same fix applies to every claim on the line.

| Cause | Claims | Fix |
|---|---|---|
| Fiedler's fixed-timestep loop, mpv's audio refill and Chromium's fake audio worker rest only on the `docs/references.md` author's reads of 2026-10-06; no search or read record holds their passages | B-32, B-33, B-34, C-18, D-13, E-18, F-52 (and B-35's wording) | one read record of the three sources — the blind re-read topic T-02 in `outside-blind-topics.md` can serve as it |
| The measurement method's six sources (Kalibera & Jones 2013, Georges et al. 2007, Maricq et al. 2018, Chow & Robbins 1965, Cochran 1977, Feller 1950) exist only as the deciding sessions' passages in `docs/references.md`; no independent read | E-43–E-47, F-55–F-60 | an independent read recorded per source, or 인지오 decides that the registry entries count as the record for method citations (a judgement: one question in chat) |
| Other sources resting only on the registry author's read | E-42 (`glean`), E-54 (`gh-artifact-retention`), F-54 (the kernel's `sched_waking` placement: file, function and version but no passage) | a read record per source |
| Lottery scheduling's shares stated without "in expectation"; the 15 % batch share placed under Waldspurger's citation | B-14, B-49, A-71 | "proportional to tickets in expectation"; the 15 % labelled the boot default's placeholder `batch_share` |
| "About 1.4 schedules per wake" shown under the LAVD slide-14 tag; it is the 9.4 gaming slice's arithmetic (its decision D9) on the slide's 25–30 % preemption share | B-25, E-28 | label it arithmetic on slide 14's share |
| "No LAVD slide shows 60 fps": slide 29's screenshot shows an uncommented "60FPS" / "16.5ms" readout (the 2026-09-13 LAVD read, `R02-lavd.md:93`) | D-22, F-14 (and `docs/memos/2026-09-13-critical-findings.md:64`, outside this audit's files) | "no slide states a frame budget or a 60 fps target; a 60 FPS / 16.5 ms readout appears only in slide 29's screenshot" |
| LAVD slide 16's graph: wineserver is linked to the game process there, but the wineserver-centred hub is slide 11, and the worker threads converge on `dxvk-cs` | D-23 (narrowed at merge), F-16 | as each finding states |
| "Proton runs only under the Steam client": the README calls it "a tool for use with the Steam client" | D-39, F-48 (and `game-task-chain`'s `validation_stats.reason` in `dataset/archetypes.yaml`, the dataset group's) | "documented as a tool for use with the Steam client" |
| "Valve sponsors LAVD": the records hold Valve's copyright line on the code and the author's work at Igalia on SteamOS | A-09, E-29 (vol. 02 quotes a superseded line of `docs/workload/grounding-sources.md:30`, which itself now says "sponsors") | restate to the copyright and the author's statement |
| Superlatives no record supports ("widely used", "most widely used", "widely known thanks to") | C-26, C-39, D-10, E-16 | drop them |
| A value computed by us shown as the source's (arithmetic or rounding unlabelled) | A-69, A-84, E-13 | label the arithmetic or the rounding |
| The source's population or scope dropped | E-50, E-51, F-30, F-49, A-84, D-20, D-36, D-14, B-17, B-41 | add the population or scope, as each finding states |

## Judgements for 인지오

- The six measurement-method sources (row 2 above): whether the registry entries' passages, written by the deciding sessions, count as their record, or an independent read is required.
- C-14 (research guidebook vol. 01's "foreground window favour" row): whether to read sources for the Linux and macOS cells or reduce the row to Windows' documented boost.

## Part A — related work, research proposal, research claims

#### A-09 — docs/related-work.md:20 — WORDING-OUTSIDE-PASSAGE
- Repo: "Valve sponsors LAVD's development and ships it in SteamOS 3.8 as a scheduler the user selects".
- Record: S2:188, `lat_cri.bpf.c:3-4` at scx `v1.1.3`: "Copyright (c) 2023-2025 Valve Corporation. Author: Changwoo Min <changwoo@igalia.com>"; S2:246 (LWN 1051430): "Min said that he has been developing LAVD as part of his work at Igalia on SteamOS and the Steam Deck." No read passage says Valve sponsors the work; the 9.12 decision D9 (CL12:154, "Valve shipping it") infers it from the copyright line.
- Proposed fix: "Valve holds the copyright of LAVD's code, which its author develops as part of his work at Igalia on SteamOS, and ships it in SteamOS 3.8 …".

#### A-46 — docs/research-proposal.md:430 (and :117) — WORDING-OUTSIDE-PASSAGE
- Repo: ":430 `SCHED_OTHER` EEVDF since Linux 6.6, a deterministic proportional-share algorithm (`linux-sched-eevdf`)"; ":117 Linux's default is EEVDF, proportional share (`linux-sched-eevdf`)".
- Record: the cited kernel document says "The Linux kernel began transitioning to EEVDF in version 6.6" and "EEVDF aims to distribute CPU time equally among all runnable tasks with the same priority" (S2:100–101, `sched-eevdf.rst:5-22`). It says neither "proportional share" nor "deterministic". "Proportional Share" is only in the title of `eevdf-tr95` (S1:151). In the local copy of the TR (`task-9.12-related-work-prose/sources/S1-05/eevdf-tr-95.pdf`, pdftotext), "deterministic" appears only for other schemes (Maheshwari's charge-based scheduling, stride scheduling), never for EEVDF. The 9.12 decision D26 (CL12:442) took the word from no passage.
- Proposed fix: ":430 … `SCHED_OTHER` EEVDF since Linux 6.6 (`linux-sched-eevdf`), a proportional-share algorithm (`eevdf-tr95`)"; ":117 … Linux's default is EEVDF (`linux-sched-eevdf`), proportional share (`eevdf-tr95`)". Drop "deterministic", or label it as our reading.

#### A-64 — docs/research-proposal.md:243, :844 — RECORD-BELOW-STANDARD (the boost only)
- Repo: "scx_lavd 0.5–5 ms with a boost to 500 ms".
- Record: the 0.5–5 ms is verbatim at S2-11s:570 (`lavd.bpf.h:73-75` at `00fec1e`, 2026-09-24). The 500 ms boost appears only in CL11:427 (the 9.11 decision D31, 2026-10-08): "lets a long-running task's slice reach `LAVD_SLICE_BOOST_MAX`, 500 ms (`lavd.bpf.h:77`; `src/bpf/main.bpf.c:348–351`)". That gives a locator and a value but no verbatim line, and no read record quotes the constant or the `--no-slice-boost` option (`main.rs:220–222`).
- Proposed fix: add a read record quoting `lavd.bpf.h:77` and `main.rs:220–222` at scx `v1.1.3` (`c8728c6b`). The local clone is `task-9.12-related-work-prose/sources/S2-09/scx/` (re-cloned at A2-18). The wording stays if the lines say so.

#### A-69 — docs/research-proposal.md:309 — WORDING-OUTSIDE-PASSAGE (an arithmetic value without its label)
- Repo: "on one Counter-Strike server most sessions lasted minutes — a Weibull fit with a median of about 9.6 min — and more than 99 % under 2 h (`chambers-imc05`)".
- Record: AA:130 (A2-12, p. 4): "a Weibull distribution with β = 0.5, η = 20, and γ = 0 closely fits the PDF of measured session times"; "more than 99% of all sessions last less than 2 hours". The paper states no median. The 9.12 decision D70 (CL12:1097) computes it, "Its median is η(ln 2)^(1/β) ≈ 9.6 minutes (arithmetic)", but the text presents it as the source's.
- Proposed fix: "… — a Weibull fit (β = 0.5, η = 20 min) whose median is about 9.6 min (arithmetic) — …".

#### A-71 — docs/research-proposal.md:421 — WORDING-OUTSIDE-PASSAGE
- Repo: "Lottery gives shares proportional in expectation, its accuracy improving with √n of the draws, so background gets an expected 15 % (`waldspurger-osdi94`)".
- Record: S1-09 p. 2 (S1:220–221): "The expected allocation of resources to clients is proportional to the number of tickets that they hold"; "with accuracy that improves with √n". The paper names no class share. The 15 % is the boot default's `batch_share`, which `docs/recognition-vocabulary.md:115` labels "No source names a batch-class share … design, unbounded by any source". As worded, the citation covers the 15 %.
- Proposed fix: "… so background gets, in expectation, its ticket share — `batch_share`, 15 % at the boot default, a placeholder no source names (`waldspurger-osdi94` for the proportionality)".

#### A-84 — docs/research-proposal.md:814 — WORDING-OUTSIDE-PASSAGE (unit conversion unlabelled, population widened)
- Repo: "0.6–3.8 µs for the switch itself and a frequent value near 10 µs on others' machines (`ghost-sosp21`, `li-expcs07`, `becker-arxiv18`)".
- Record: S1:415 (S1-23 p. 7): "context switches on our system take at least 3,400 cycles, with a frequent value around 30,000 cycles", on one laptop (i7-2640M @ 2.8 GHz, Table 1). The µs value is the 9.12 decision D57's conversion, labelled there "(arithmetic)" (CL12:916). The "frequent value" is one machine's, not several machines'.
- Proposed fix: "… 0.6–3.8 µs for the switch itself, and on one laptop a frequent value of about 30 000 cycles, about 10.7 µs at its nominal 2.8 GHz (arithmetic) …".

## Part B — harness, metrics, boot defaults, recognition vocabulary, background guide, terminology, simulator, daemon

#### B-02 — docs/harness/metrics.md:258 — WORDING-OUTSIDE-PASSAGE
- Repo: "Chicco and Jurman fill those cases by convention — 1 or −1 when only one cell is non-zero, otherwise 0 as a limit"
- Record: R11/search/S1-literature.md:198 "some mathematical considerations can help meaningfully fill in the gaps for these cases … MCC=1 for the former case and MCC=−1 for the latter … we proceed through a simple approximation via a calculus technique"; R11/changelog.md:372 (9.11 decision D27) the four cases "taken as a limit '→ 0'". The authors derive the values; they do not call them a convention (the convention in this sentence is the grader's choice to report undefined, which D27 labels design).
- Proposed fix: "Chicco and Jurman derive values for those cases — 1 or −1 when only one cell is non-zero, otherwise 0 as a limit — and the grader instead reports the coefficient as undefined, by design."

#### B-05 — docs/harness/metrics.md:264 — NO-RECORD
- Repo: "position `(n − 1) · p / 100` … (numpy's `linear` method, R's type 7)"
- Record: none. 9.11 decision D13 (R11/changelog.md:187) labels the rule a convention but no record quotes numpy's `percentile`/`quantile` documentation or R's `quantile` type 7 definition.
- Proposed fix: record numpy's and R's documentation passages (version, URL, date), or drop the parenthetical and keep the formula as the convention's definition.

#### B-14 — docs/recognition-vocabulary.md:115 — WORDING-OUTSIDE-PASSAGE
- Repo: "`waldspurger-osdi94` defines shares as proportional to tickets and gives no ratio between classes."
- Record: R12/search/S1-literature.md:220 "The expected allocation of resources to clients is proportional to the number of tickets that they hold … the actual allocated proportions are not guaranteed to match the expected proportions exactly"; the second half traces to R11/search/S1-literature.md:116. The statistic is an expectation; the repo drops it (9.12 decision D36 made the same correction in the proposal: "shares proportional in expectation").
- Proposed fix: "… gives shares proportional to tickets in expectation and states no ratio between classes."

#### B-17 — docs/recognition-vocabulary.md:70 — WORDING-OUTSIDE-PASSAGE
- Repo: "The idea has a shipped counterpart, a per-class CPU bandwidth ceiling (`linux-sched-bwc`, existence only)"
- Record: R11/search/S2-project-docs.md:302–312 (`sched-bwc.rst:5–18` at v7.2): "the maximum CPU bandwidth available to a group or hierarchy"; "a task group is allocated up to 'quota' microseconds"; "threads in the cgroup"; 9.11 decision D13 (R11/changelog.md:183) "quota per period on a cgroup". The object is a task group (cgroup) of `SCHED_NORMAL` tasks, not a scheduling class.
- Proposed fix: "a per-group CPU bandwidth ceiling, a quota per period on a cgroup (`linux-sched-bwc`, existence only)".

#### B-25 — harness/experiments/rq0-gate.yaml:170 — WORDING-OUTSIDE-PASSAGE
- Repo: "the deck's per-schedule runtime understates a wake's demand by the schedules a wake is cut into, about 1.4 on average (lavd-ossna24 s14)"
- Record: R4/search/S1-literature.md:57, slide 14: "Preemption (e.g., timer interrupt) takes only 25-30% of scheduling." No slide states 1.4; 9.4 decision D9 (R4/changelog.md:66) derives "about 1.4 schedules per wake on average" from that share (1/(1 − 0.28)) and itself rejects scaling by 1/0.71 as assuming preemption independent of run length. The 1.4 is our arithmetic under a source tag.
- Proposed fix: "… about 1.4 on average by arithmetic on the deck's 25–30 % preemption share (lavd-ossna24 s14; 9.4 D9)".

#### B-28 — docs/simulator/interpretation-contract.md:31 — WORDING-OUTSIDE-PASSAGE
- Repo: "absolute periodic wake: runnable at t₀+k·period regardless of when the previous iteration finished — drift-free (rt-app `timer{ref,period}`)"
- Record: R01:348 (`rt-app_parse_config.c:838–864`: `get_string_value_from(obj, "mode", TRUE, "relative")`); R11/search/S2-project-docs.md:616–640 (`tutorial.txt:507–509` "By default they work in 'relative' mode"; `:518–522` relative mode resets the reference to the end of the current phase; the 2026-09-13 verification's C-rt-app-2 WORDING-FIX). rt-app's `timer{ref,period}` without `"mode": "absolute"` re-anchors after an overrun, so it is not "regardless of when the previous iteration finished".
- Proposed fix: "(rt-app `timer` with `"mode": "absolute"`)". Note: the line sits under the simulator-side TIMER rule held for Phase 10 (9.11 decision D3); this fix touches only the attribution.

#### B-32 — docs/simulator/simulator-guide.md:136 — RECORD-BELOW-STANDARD
- Repo: "its audio output refills a drained buffer in one write (`mpv`)"
- Record: no search or read record; the only text is `docs/references.md` `mpv` (author's read 2026-10-06, v0.37.0, `buffer.c:620`, `:703–706`). 9.11's mpv record (R11/search/S2-project-docs.md:694–712) read video files only.
- Proposed fix: an independent read of mpv's `audio/out/buffer.c` at a pinned tag recorded with passages (blind topic below).

#### B-33 — docs/simulator/simulator-guide.md:136 — RECORD-BELOW-STANDARD
- Repo: "Chromium's fake audio output runs a late callback once and moves to the next on-time interval (`chromium`)"
- Record: no search or read record; `docs/references.md` `chromium` (author's read 2026-10-06); R11/changelog.md:241 restates the registry. The registry's scope ("the fallback path of a machine without a sound device") is also absent from the sentence.
- Proposed fix: an independent read recorded; add the scope ("its fallback output when no audio device opens").

#### B-34 — docs/simulator/simulator-guide.md:136 — RECORD-BELOW-STANDARD
- Repo: "a fixed-timestep game loop catches up its simulation steps, capped, and renders once per loop (`fiedler-gaffer04`)"
- Record: no search or read record; `docs/references.md` `fiedler-gaffer04` (author's read 2026-10-06, no hash).
- Proposed fix: an independent read of the article recorded with passages and the copy's hash.

#### B-35 — docs/simulator/simulator-guide.md:136 — WORDING-OUTSIDE-PASSAGE
- Repo: "Backlog is a measurement choice, not a model of the programs the TIMER tasks stand for: none of them replays late iterations."
- Record: R11/changelog.md:236 (9.11 decision D17): "rt-app's 'absolute' mode and a fixed-timestep loop's simulation steps catch up"; `fiedler-gaffer04` role: the update simulates "more steps to catch up". The same sentence's own list includes a program that replays late simulation steps.
- Proposed fix: "none of them replays a late frame or callback; a fixed-timestep loop replays its simulation steps, capped, but renders once per loop".

#### B-41 — docs/background-guide.md:18 — WORDING-OUTSIDE-PASSAGE
- Repo: "(Windows' and macOS's Game Mode … — and neither documents how it recognises a game.)"
- Record: R12/search/S2-project-docs.md:281 "mechanism of recognising a game not documented on these pages"; :621 "Apple statement of how macOS decides an app is a game … only on Apple Developer Forums, which are script-rendered and not quotable"; Microsoft's Xbox Support article was not readable then. The record covers the pages read, not all of each vendor's documentation.
- Proposed fix: "— and neither vendor's Game Mode pages read here say how a game is recognised."

#### B-49 — docs/background-guide.md:221 — WORDING-OUTSIDE-PASSAGE
- Repo: "**lottery scheduling** | … Gives proportional shares ("background gets ~15%")"
- Record: R12/search/S1-literature.md:220 "probabilistically fair. The expected allocation … is proportional to the number of tickets … the actual allocated proportions are not guaranteed to match the expected proportions exactly".
- Proposed fix: "Gives shares proportional to tickets in expectation".

## Part C — research guidebook volumes 1–5

#### C-10 — vol-01:2094 (and :3338's "priority class" cell) — NO-RECORD
- Repo: "Windows에는 priority class가 있어서 프로그램이 자기를 배경 작업으로 등록할 수 있습니다."
- Record: none. The 9.12 record S2-54 (Microsoft Learn "Scheduling Priorities", "Priority Boosts", R12search/S2-project-docs.md:579–580) quotes the 0–31 priority levels, round-robin within a level and the boosts; the 9.12 audit (R12search/A-audit.md:328) quotes only the foreground boost of `NORMAL_PRIORITY_CLASS`. No passage says a program can register itself as background work.
- Proposed fix: read Microsoft Learn's "Scheduling Priorities" priority-class passage (and `SetPriorityClass`'s `PROCESS_MODE_BACKGROUND_BEGIN`, if meant) into a record, or restate to what S2-54 states: "Windows에는 priority class와 단계가 있어서 프로그램이 자기 priority를 정할 수 있습니다".

#### C-14 — vol-01:3339 — NO-RECORD (Linux and macOS cells)
- Repo: table row "foreground window 우대 | 부분적 | 있음 | 있음" (Linux, Windows, macOS).
- Record: Windows only — R12search/A-audit.md:328, "the scheduler boosts the priority class of the process associated with the foreground window". No record covers a foreground-window preference on Linux ("부분적") or macOS ("있음").
- Proposed fix: read sources for the two cells (macOS: Apple's documentation of foreground app priority, e.g. App Nap or the QoS of the frontmost app; Linux: what, if anything, a stock desktop does — GNOME/Mutter or systemd's `app.slice` weights already recorded in 9.11 D16), or reduce the row to Windows' documented boost.

#### C-18 — vol-01:3059 — RECORD-BELOW-STANDARD
- Repo: "고정 시간 간격으로 도는 게임 loop도 화면은 한 번만 그리면서 simulation step은 이렇게 따라잡고, 따라잡는 횟수에 상한을 둡니다. … mpv는 비어 버린 audio buffer를 한 번에 다시 채우고, 소리 장치가 없을 때 Chromium이 쓰는 가짜 audio 출력은 늦은 callback을 한 번 돌린 뒤 다음 제때 간격으로 넘어갑니다."
- Record: only `docs/references.md`'s `fiedler-gaffer04` ("verified (2026-10-06; the page read in full)"), `mpv` and `chromium` ("verified (2026-10-06; the files read at the tag)") — the author's reads, with code locators and commits but no search record holding the passages; 9.11 D3 (R11changelog.md:46) cites them back to the registry. The registry's own text agrees with the wording (mpv "writes all free space at each wake", `buffer.c:620`, `:703–706`; Chromium "Even if we're late, this callback must be called" … "the next nearest ontime interval", `fake_audio_worker.cc:177–190`, "the fallback when no audio device opens"; Fiedler, catch-up "bounded by a clamp on frame time … or \"a maximum # of steps per-frame\"").
- Proposed fix: a read record (copy, commit/URL, date, verbatim passages) for the three sources — the blind re-read below can serve as it.

#### C-20 — vol-01:3234 — WORDING-OUTSIDE-PASSAGE (date only)
- Repo: "2024년 말에 나온 kernel 버전부터, scheduling policy를 kernel 밖에서 … 넣을 수 있는 기능이 들어갔습니다."
- Record: R12search/S2-project-docs.md:511–515 (S2-47) establishes "its first release is Linux 6.12" from the tree at v6.11 / v6.12-rc1 / v6.12; no record gives 6.12's release date.
- Proposed fix: "Linux 6.12부터" (the record's object), or add 6.12's release date to a record.

#### C-26 — vol-02:697 — NO-RECORD
- Repo: "인터페이스 설계 쪽에서 이 값이 널리 알려진 것은 이 책 덕분입니다."
- Record: none; S1-05 (R11search/S1-literature.md:140) records the excerpt's sentence and its citations of Miller and Card et al., not the book's influence.
- Proposed fix: drop the sentence, or "이 책도 같은 값을 적습니다".

#### C-39 — vol-02:2964, :3232, :3362 — NO-RECORD
- Repo: "가장 널리 쓰이는 카탈로그 하나를" (ananicy-rules); "가장 오래되고 널리 쓰이는 도구가 있습니다" (hackbench); "가장 널리 쓰이는 것 하나의 기술 문서를" (PCMark 10).
- Record: none measures use or age rank for any of the three; the 2026-09-13 comparison graded the like claim for stress-ng ("widely cited") UNVERIFIABLE (RV/compare/K1.md:65), and 9.12 D111 removed superlatives from related-work.
- Proposed fix: drop the superlatives ("카탈로그 하나를", "많은 task로 부하를 주는 도구가 있습니다", "한 제조사의 벤치마크 하나의 기술 문서를").

#### C-42 — vol-02:3448, :3486, :3532 — WORDING-OUTSIDE-PASSAGE
- Repo: "앞의 것과 같은 제조사가 내는 다른 모음입니다" (placed right after the SYSmark 30 section); "**세 제조사가 독립적으로 같은 프로그램 목록에 도달했습니다.** 데스크톱의 대표적 작업이 무엇인지에 대해 업계의 합의가 있다는 뜻입니다."; summary :3532 "세 제조사가 독립적으로 거의 같은 프로그램 목록에 도달했습니다 … 그 합의를 근거로".
- Record: two makers, not three — Procyon is UL's (`docs/references.md` `procyon` cite: "UL Solutions"; R05), PCMark 10 is UL's, SYSmark 30 is BAPCo's. PCMark 10's named programs are "Chromium web browser • Firefox web browser • LibreOffice Writer word processing program • GIMP image manipulation program" (quoted at vol-02 §8.4, graded exact by V60 at V60-vol02-quotations.md:507 region), not Word/Excel/Lightroom/Premiere; the shared list is SYSmark 30's and Procyon's. No record speaks to independence; the volume's own box (:3488) allows the makers may have referenced each other.
- Proposed fix: "Procyon은 PCMark 10과 같은 UL의 모음입니다"; "SYSmark 30과 Procyon의 사무·사진·영상 시나리오가 같은 상용 프로그램(Word, Excel, PowerPoint, Outlook, Lightroom, Photoshop, Premiere Pro)을 씁니다. PCMark 10은 공개 소프트웨어(Chromium, Firefox, LibreOffice Writer, GIMP)를 씁니다"; drop "독립적으로" and "업계의 합의".

#### C-44 — vol-03:54 — NO-RECORD
- Repo: mechanism table, Linux `sched_ext` row, who turns it on: "관리자가 policy 프로그램을 올림".
- Record: none for the privilege; S2-01 ("The BPF scheduler can be turned on and off dynamically anytime", R12search/S2-project-docs.md:69) and S2-47 (the Kconfig help, :511–515) do not say who loads it.
- Proposed fix: read the privilege requirement (e.g. `sched-ext.rst`'s loading section or the `bpf()` capability check) into a record, or restate as "BPF scheduler 프로그램을 실행 중에 올림".

## Part D — research guidebook volume 6

#### D-02 — vol-06:538, 1281, 1494, 3673 — WORDING-OUTSIDE-PASSAGE
- Repo: "잘 만든 오디오 프로그램이 했을 버퍼링을 무시한다" (in quotation marks as the manual's words; :538 "잘 만든 소리 프로그램이라면 했을 버퍼링은 무시한 모형").
- Record: R01:41, `interbench.8:81-87`: "This behaviour ignores any caching that would normally be done by well designed audio applications".
- Proposed fix: "버퍼링" → "캐싱(caching)" in all four places.

#### D-05 — vol-06:985 — WORDING-OUTSIDE-PASSAGE
- Repo: "무작위가 아니라 0퍼센트에서 100퍼센트까지 차례로 올라가는 경사이고, 한 바퀴가 100밀리초입니다."
- Record: R01:94-96: each step occupies "a ~100 ms window whose busy share is i%"; "one sweep ≈ 10.1 s wall time with 5 050 ms of CPU", consistent with `decasecond_deadlines = 100`.
- Proposed fix: "한 단계가 100밀리초이고, 0에서 100퍼센트까지 한 번 올라가는 데 약 10초가 걸립니다."

#### D-10 — vol-06:1265 — NO-RECORD
- Repo: "그 모형이 존재하고 널리 쓰인다는 것."
- Record: none; R01:260-279 records author, licence and distribution packaging, no statement of use.
- Proposed fix: drop "널리 쓰인다"; keep "그 모형이 존재하고 커뮤니티의 벤치마크로 배포된다" (packaging, R01:268-277).

#### D-13 — vol-06:460 — RECORD-BELOW-STANDARD
- Repo: "밀린 주기를 따라잡는 것은 … 고정된 시간 간격으로 도는 게임 루프가 화면은 한 번만 그리면서 시뮬레이션 단계를 따라잡는 경우였습니다."
- Record: only `docs/references.md:575-577` (`fiedler-gaffer04`, role line with verbatim passages, "accessed 2026-10-06"), cited by 9.11 changelog D3; no search/read record holds the passage and copy.
- Proposed fix: add a read record for Fiedler, "Fix Your Timestep!" (gafferongames.com/post/fix_your_timestep/) with the passages and copy identification; the sentence itself matches the registry's quotes.

#### D-14 — vol-06:462 — WORDING-OUTSIDE-PASSAGE
- Repo: "영상 재생에서는 GStreamer의 영상 출력이 그렇게 합니다. 지금 시각이 들어 있는 frame은 바로 그리고, 그보다 앞의 frame은 버립니다."
- Record: 9.11 S2:719-722: `gstvideosink.c:177` `gst_base_sink_set_max_lateness (…, 5 * GST_MSECOND)`; `gstbasesink.c:118-129` "If the frame is later than max-lateness, the sink will drop the buffer". A frame that ended less than 5 ms before now is still rendered.
- Proposed fix: "GStreamer의 영상 출력은 끝 시각이 지금보다 5밀리초 넘게 지난 frame을 버리고 그 뒤의 frame을 그립니다."

#### D-17 — vol-06:850 — WORDING-OUTSIDE-PASSAGE
- Repo: "Dhakal 외 네 명이 2018년 CHI에 낸 논문".
- Record: R08:9 (authors match the entry); the copy's byline (`sources/dhakal-chi18.txt:3`) and `docs/references.md:38`: Dhakal, Feit, Kristensson, Oulasvirta.
- Proposed fix: "Dhakal 외 세 명".

#### D-20 — vol-06:1237 — WORDING-OUTSIDE-PASSAGE
- Repo: "게임 하나가 task를 300개쯤 만들고, 그중 90퍼센트가 오래 살고".
- Record: R02:24 slide 12 "Around 300 tasks are scheduled while running a game"; R02:37 "Around half of them are system tasks -- especially, wine, graphics, and audio servers".
- Proposed fix: "게임을 하는 동안 시스템 task를 포함해 약 300개의 task가 scheduling되고" (the wording the volume's own :1108 and :1126 boxes already give).

#### D-22 — vol-06:1735 — WORDING-OUTSIDE-PASSAGE
- Repo: "슬라이드 30장의 텍스트와 그림 속 글자 어디에도 16.7, 16.67, 60fps, frame budget이 나오지 않습니다."
- Record: R02:93, :95, :97: slide 29's EEVDF screenshot overlay shows "60FPS", "16.5ms" and both screenshots "Refresh Rate: 60"; "No 'frame time budget' is stated anywhere in the text, and no slide relates 15 msec (or any value) to 60 FPS".
- Proposed fix: "슬라이드 어디에도 frame 예산이나 frame 주기를 말하는 문장은 없습니다. 그림 속 글자로는 슬라이드 29의 EEVDF 화면에 설명 없는 '60FPS', '16.5ms', 'Refresh Rate: 60' 표시가 있을 뿐입니다."

#### D-23 — vol-06:1749 — WORDING-OUTSIDE-PASSAGE (narrowed at merge)
- Repo: slide 16's graph has "게임 본체와 `wineserver`가 서로 주고받는 작은 고리, 여러 작업 thread가 그래픽 제출 thread 하나로 모이는 모양"; :1863 and :1889 place wineserver in slide 16's loop with the game.
- Record: the 9.4 gaming record `_dev/research/jioh/task-9.4-gaming/search/S2-project-docs.md:91` lists slide 16's nodes and edges, including `wineserver[7256/0]` with "`wineserver→Troy.exe epoll (134200)`, `Troy.exe→wineserver pipe_read (58134)`" — so the wineserver loop with the game process is on slide 16, and :1863 and :1889 are traced. The same record and the 2026-09-13 LAVD read (`reads/R02-lavd.md:45-53`) give the four `Task worker thr` → `dxvk-cs` "futex_wait" edges, then `dxvk-cs` → `dxvk-submit`: the workers converge on `dxvk-cs`, not on a submit thread. (The part's first reading — "slide 16's edges name no `wineserver`" — rested on R02's slide-16 edge list, which omits the wineserver edges; see Record defects.)
- Proposed fix: "여러 작업 thread가 DXVK의 `dxvk-cs` thread 하나로 모이는 모양" in place of "그래픽 제출 thread 하나로".

#### D-25 — vol-06:1983-1985 — NO-RECORD
- Repo: slide 10 quoted: "If games have the common characteristics, which are differentiated from other general program domains (e.g., HPC, AI/ML, database), there are chance to come up with a game optimized scheduling policy."
- Record: none; 9.4 S1:53 records only slide 10's "We collect and analyze all scheduling activities while playing games." The sentence is in the copy (`2026-09-13-verification/sources/lavd-ossna24/scx-lavd-oss-na24.pypdf.txt:133-135`).
- Proposed fix: add the slide 10 passage to a record (9.4 S1's S1-01 passages); the quotation is then traced.

#### D-26 — vol-06:4109 — WORDING-OUTSIDE-PASSAGE
- Repo: "`corbet-lwn24` | 위 발표를 다룬 LWN 기사 | deployed-system".
- Record: R02:190: the article "covers the sched_ext microconference at the 2024 Linux Plumbers Conference (a different talk from OSS NA, April 2024, given remotely)".
- Proposed fix: "Min의 LPC 2024 발표를 다룬 Corbet의 LWN 기사" (and the tier column "talk·news", as `docs/references.md:737` files it).

#### D-29 — vol-06:3207 — WORDING-OUTSIDE-PASSAGE
- Repo: "확장판 기술 보고서(arXiv:1705.05937, 21쪽)".
- Record: R03:10 "arXiv 1705.05937, only version v1, 16 May 2017; 20 pages".
- Proposed fix: "20쪽".

#### D-36 — vol-06:1818 — WORDING-OUTSIDE-PASSAGE
- Repo: "숨겨진 탭의 렌더러 `renderer-hidden`(사이트마다 렌더러 하나, Chromium의 site-per-process 모델)".
- Record: R09:258-262: "In (one-)site-per-process mode, each process is locked to documents from a single site"; separate instances of a site in unrelated tabs "can safely run in separate processes"; over the soft limit Chromium "makes an attempt to start randomly reusing same-site processes".
- Proposed fix: "(렌더러 하나는 한 사이트의 문서만 담는다, Chromium의 site-per-process 모델)".

#### D-39 — vol-06:2366 — WORDING-OUTSIDE-PASSAGE
- Repo: "Proton은 Steam 클라이언트 아래에서만 돕니다".
- Record: 9.4 S4:262 "Proton is a tool for use with the Steam client"; "Most users should use Proton provided by the Steam Client itself."; :357 the README documents only Steam-client installation, no run-requirements paragraph.
- Proposed fix: "Proton은 Steam 클라이언트와 함께 쓰는 도구로 배포되고 문서도 Steam 클라이언트 설치만 다룹니다".

#### D-42 — vol-06:2248 — WORDING-OUTSIDE-PASSAGE
- Repo: "인용 문서는 Table 4를 작업과 모듈마다의 하드웨어 민감도 표로 적고(1.77배는 CC 모듈에서 …)".
- Record: R04:188-209 Table 4 is per workload; R04:225-237 the module values are Table 5 (p. 12) and §4.7.2's text "The CC module has a significantly higher sensitivity to the graphics card, the best configuration performs 1.77 times better than the base configuration".
- Proposed fix: "Table 4는 작업마다의 하드웨어 민감도 표이고, 모듈 단위의 값은 Table 5와 §4.7.2에 있다(1.77배는 …)". The same "(Table 4)" for module sensitivity sits in `docs/references.md:34`'s role line (outside this part's files).

#### D-44 — vol-06:2033-2049 — RECORD-BELOW-STANDARD
- Repo: BG_CPUIO `wget, curl, aria2c`; Chat `discord, element-desktop, slack`, `thunderbird`.
- Record: R06:281 and :312 name them only in the reader's reading ("Also in chats.rules: … slack, element-desktop, … thunderbird … — all Chat"; "Download clients: … aria2c, … wget, curl … → all BG_CPUIO"); no rule line is quoted. The copy at `03ef03fb` holds `Networking/wget.rules:2`, `curl.rules:2`, `aria2c.rules:2`, `Chats/chats.rules:58,63,76` (grep, this audit).
- Proposed fix: add the six rule lines verbatim to the record.

#### D-46 — vol-06:2057, 3027 — NO-RECORD
- Repo: "`system-daemon`에는 `Service`(`dbus-daemon`이 여기 들어 있음)"; "`gnome-shell`과 `Xorg`와 `pipewire`를 전부 `LowLatency_RT`".
- Record: gnome-shell and pipewire at 9.12 S3:511, :514; no record for `Xorg` or `dbus-daemon`. The copy holds `00-default/DEs-and-WMs/xorg.rules:2` `{ "name": "Xorg", "type": "LowLatency_RT" }` and `00-default/Services/dbus.rules:3` `{ "name": "dbus-daemon", "type": "Service" }`.
- Proposed fix: add the two rule lines verbatim to a record.

## Part E — dataset guidebook volumes 01–04

#### E-13 — G/01:598, G/03:419 — WORDING-OUTSIDE-PASSAGE
- Repo: G/01:598 "Firefox의 Linux telemetry(`glam`)가 보여 준 "창 하나에 tab 다섯""; G/03:419 "한 브라우저 창에 탭이 다섯 개라는 것은 Firefox의 Linux telemetry(`glam`, 9.10 D15, D16)에서".
- Record: 9.10 S3:648 "Max concurrent tabs, Linux, v152 — `max`: 1.98 / 4.67 / 10.99 …" (p25/p50/p75…; the metric counts tabs "across all windows", 9.10 S3:640); windows "max: 1 / 1 / 1.93 …". The telemetry shows a median per-client maximum of 4.67 tabs across all windows; "five" is the decision's rounding and "in one window" the pairing with the windows median.
- Proposed fix: "the median client's largest number of open tabs, 4.67 across all windows (Firefox release, Linux, version 152), rounded to five, with one window (the median client's maximum of windows is 1)", as G/02:1241 already words it.

#### E-16 — G/03:244, :2397 — WORDING-OUTSIDE-PASSAGE
- Repo: "`rt-app` — Linux scheduler 연구에서 널리 쓰는 workload 생성 도구로, 시간을 µs 정수로 다룹니다."
- Record: K1:362 "Correct wording: "integer microseconds (rt-app's unit for run/sleep/timer/dl-* durations)". rt-app's global duration is in seconds." No record states rt-app is widely used.
- Proposed fix: "rt-app, a workload generator for Linux scheduler testing, whose run, sleep, timer and deadline durations are integer microseconds"; drop "널리 쓰는".

#### E-28 — G/04:1919 — WORDING-OUTSIDE-PASSAGE
- Repo: "(9.4 D9; lavd-ossna24 s14, about 1.4 on average)… wake 하나가 여러 schedule로 쪼개지는 만큼(평균 약 1.4배)".
- Record: `R/task-9.4-gaming/changelog.md:66`: s14 "preemption 25–30 % of scheduling events, `sched_preempt` 28.78 % … about 1.4 schedules per wake on average" — the 1.4 is the decision's arithmetic on s14's share, which the slide does not state.
- Proposed fix: label the factor: "about 1.4, our arithmetic from slide 14's 25–30 % preemption share (9.4 D9)".

#### E-29 — G/02:689 — WORDING-OUTSIDE-PASSAGE (stale attribution)
- Repo: "`docs/workload/grounding-sources.md`는 gaming scheduling이 실제 문제라는 근거로 "Valve ships it"를 적음".
- Record: `docs/workload/grounding-sources.md:30` now reads "Valve sponsors LAVD and ships it in SteamOS 3.8 as a scheduler the user selects, not enabled by default (`steamos-lavd`)"; K2:285 judged the old "Valve ships it" MISATTRIBUTED; 9.12 D9 (`R/task-9.12-related-work-prose/changelog.md:152`) restated it.
- Proposed fix: quote the current sentence of `grounding-sources.md:30` with `steamos-lavd`.

#### E-38 — G/02:1044 — WORDING-OUTSIDE-PASSAGE
- Repo: "`cpu-batch`는 원래 "a process that simply computes until it is done"이라는 interbench Burn의 한 줄이었습니다."
- Record: K1:203–215: interbench's Burn is "A configurable number of threads fully cpu bound (4 by default)" (`interbench.8:120–121`) that burn "continuously" until the load stops; "until done" is ours. The quoted phrase is the repository's own (`docs/data-contracts.md`, 21083b31).
- Proposed fix: "`cpu-batch` was once the repository's one-line description "a process that simply computes until it is done", grounded on interbench's Burn load (fully CPU-bound threads that run until the load is stopped)".

#### E-50, E-51 — G/01:1057; G/03:603; G/04:1564 — WORDING-OUTSIDE-PASSAGE (population dropped)
- Repo: G/01:1057 "`gonzalez-chi04`의 사건 하나에 약 3분(3분 08초)과 working sphere 안에서 전환 전까지의 평균 연속 구간 11분 28초"; G/03:603 and G/04:1564 quote "the mean continuous segment in a working sphere before switching, 11 min 28 s".
- Record: R10:89/121: 0:03:08 is Table 2's row "All events except "Formal meetings" and "Other"" (p. 116); K4:487: 11:28 "covers central and peripheral spheres only". `docs/workload/building-plan.md:203` carries both qualifiers.
- Proposed fix: add the populations, as building-plan does: "3 min 08 s per event, formal meetings and 'Other' excluded; 11 min 28 s per continuous segment in a central or peripheral working sphere". (The quote in G/03:603 and G/04:1564 is 9.17 D1's; the fix there is a gloss after the quote.)

#### E-21 — G/02:537 — NO-RECORD
- Repo: "SWELL-KW의 timestamp가 Windows tick 15.6 ms 단위로 양자화되어 … (`sources.yaml`의 `swell-icmi14` notes: "Timestamps quantised at the 15.6 ms Windows tick")".
- Record: none found (searched every slice's search logs, changelogs and the 2026-09-13 reads for `15.6` and `quanti`); the SWELL-KW reads (R10:233–244, 9.10 S1:500–522) do not state the timestamp resolution.
- Proposed fix: state it as our reading of the stream ("in the stream as we extracted it, timestamps fall on a 15.6 ms grid; 7 % of key gaps are zero", 9.5 D12), or add a read record of the uLog documentation that states the resolution.

#### E-55 — G/04:732 — NO-RECORD
- Repo: "9.10 D24가 `spotify`를 `mpv`로 바꿨습니다. Spotify 네이티브 client는 계정이 필요하기 때문입니다."
- Record: 9.10 S4:1981 "Need an account for their main function: Spotify, … (reader's expectation, not documented in the sources read except for Steam, S4-10)".
- Proposed fix: say the account need is the slice's expectation, not a documented fact, or drop the reason and keep "the program observed is mpv" (9.10 D24's first reason).

#### E-18, E-42, E-43, E-44, E-45, E-46, E-47, E-54 — RECORD-BELOW-STANDARD
- Repo: G/02:137 (`fiedler-gaffer04`: a fixed-timestep loop's simulation steps catch up); G/02:843 (`glean`: daily at local 04:00); G/02:633 (`maricq-osdi18` "servers with supposedly identical parts"); G/02:641 (`kalibera-ismm13` §11 quote); G/02:646 (`chow-aoms65`); G/02:640 (`cochran-st77`); G/02:669 (`feller-ipta50`); G/01:1127, G/02:629 (`gh-artifact-retention`, 90 days).
- Record: each is held only in its `docs/references.md` entry, written from the author's own read (lines 575, 419, 122, 117, 127, 132, 137, 379), or in a changelog paraphrase (`R/task-9.6-compile/changelog.md:131`, `R/task-9.5-interactive-typing/changelog.md:671`); no search or read record holds the passage with the copy read. The wording matches the registry quotes; what is missing is the independent read.
- Proposed fix: one read record per source (verbatim passage, locator, URL/commit, version, date), e.g. as an addendum to a slice's search log; or let the blind re-read of 9.16 serve as that record.

## Part F — dataset guidebook volumes 05–08

#### F-08 — v05:1979, v08:1595 — WORDING-OUTSIDE-PASSAGE
- Repo: "공개 저장소의 표준 Linux runner는 "4 vCPU, 16 GB RAM and 14 GB SSD"" (v05); "`gh-hosted-runners`(GitHub Docs, 2026-10-13 읽음)의 "4 vCPU, 16 GB RAM and 14 GB SSD"" (v08).
- Record: 9.4/search/S4-ci-observability.md:96 — the page is a table, "Linux | 4 | 16 GB | 14 GB | x64 | ubuntu-latest, …" under "Processor (CPU) | Memory (RAM) | Storage (SSD)". The quoted string is 9.21/changelog.md:65's paraphrase. The values match; the quotation marks attribute a paraphrase to the page.
- Proposed fix: drop the quotation marks or quote the row as `refs:370` cites it ("processor 4, memory 16 GB, storage (SSD) 14 GB").

#### F-14 — v06:68, v08:746 — WORDING-OUTSIDE-PASSAGE
- Repo: "30장의 슬라이드를 텍스트와 그림까지 다 확인해 보니 16.7, 16.67, 60 fps, "frame budget"이라는 말이 어디에도 없었습니다" (v06:68); "30장의 슬라이드 어디에도 16.7, 60 fps, "frame budget"이 없었습니다" (v08:746).
- Record: R02:93 — "Slide 29 [image], EEVDF screenshot, overlay at top-left: "100%", "60FPS", "16.5ms" …; both screenshots list "Refresh Rate: 60""; R02:97 — "an uncommented 60 FPS / 16.5 ms HUD readout in one screenshot". The figures do contain "60FPS". (The wording follows `docs/memos/2026-09-13-critical-findings.md:64`, "No slide contains 16.7, 16.67, 60 fps or "frame budget"", which has the same gap; that memo is outside this part.)
- Proposed fix: "no slide states 16.7 ms, a frame budget or a 60 fps target; a 60 FPS / 16.5 ms readout appears only, uncommented, in slide 29's benchmark screenshot".

#### F-16 — v06:539 — WORDING-OUTSIDE-PASSAGE
- Repo: "16장의 그래프는 wineserver를 중심으로 한 구조를 보입니다".
- Record: 9.4/search/S2-project-docs.md:91 — slide 16 has `wineserver[7256/0]` linked to `Troy.exe` ("epoll (134200)", "pipe_read (58134)") and to `explorer.exe`; the rest of the graph (worker threads → `dxvk-cs`, `winepulse_*` ⇄ PipeWire) does not pass through it. :92 — the hub around `wineserver[5789/0]` with `redDispatcher1–7` is slide 11. (K2:111 and R02:38 list slide 16 without wineserver; the 9.4 record's full node list has it.)
- Proposed fix: "16장의 그래프는 wineserver를 게임 process `Troy.exe`와 epoll·pipe_read로 잇고, wineserver를 중심에 둔 그림은 11장입니다".

#### F-20 — v08:259 — WORDING-OUTSIDE-PASSAGE
- Repo: quotes the 2026-08 archive, "LAVD gaming: ~300 tasks at 65–95% of a many-core machine".
- Record: R02:24, :119 — slide 12, "Around 300 tasks are scheduled while running a game"; "CPU utilization is moderately high -- around 65-95%"; R02:17 — "never name the machine/kernel on which the characterization traces … were taken"; slide 5 names the Steam Deck (8 cores) as LAVD's target (9.4/search/S2-project-docs.md:81).
- Proposed fix: keep the archive quote and add that the slides name no trace machine, so "many-core" is the archive's reading.

#### F-30 — v08:954 — WORDING-OUTSIDE-PASSAGE
- Repo: the 136M data, "transcription of memorised sentences, share > 1 s 0.7 %" (quoting 9.5 D4, 9.5/changelog.md:21).
- Record: 9.5/search/candidates.md:11 — "S3's six-participant sample: within-sentence press-to-press … share > 1 s 0.7 %". The 0.7 % is the search reader's computation on six participants, not a property stated for the dataset.
- Proposed fix: "share > 1 s 0.7 % in a six-participant sample the 9.5 search read".

#### F-48 — v06:1318 — WORDING-OUTSIDE-PASSAGE
- Repo: "(no GPU; Proton runs only under the Steam client)" (quoting `game-task-chain`'s `validation_stats.reason` in `dataset/archetypes.yaml`, which is the dataset group's).
- Record: 9.4/search/S4-ci-observability.md:262 — "**Proton** is a tool for use with the Steam client …"; :357 — "Proton README documents only Steam-client installation …; no "run requirements" paragraph exists to quote".
- Proposed fix: "Proton is documented only as a tool for use with the Steam client"; the same fix in the archetype's `validation_stats.reason`.

#### F-49 — v06:1400 — WORDING-OUTSIDE-PASSAGE
- Repo: "입력 하나당 CPU에 대해서는 문헌에 Linux 관찰이 있었지만 모두 2000–2004년의 100–664 MHz 기계였습니다(Flautner, Tsafrir/Etsion 등)".
- Record: 9.5/search/candidates.md:21–23 — the Linux traces are Flautner 2000/2001 (dual 450 MHz, Linux 2.3.99), Flautner 2002 (Crusoe 300–600 MHz, Linux 2.4.4), Tsafrir 2003 / Etsion 2004 / 2006 (664 MHz, Linux 2.4.8); :24–25 — the 100 MHz machines are Endo 1996 / 2000 on Windows NT and BSD/OS. (9.5/changelog.md:17, D4, lists Endo 1996 among "the 2000–2004 Linux traces"; the guidebook inherits that.)
- Proposed fix: "Linux 관찰은 2000–2006년의 300–664 MHz 기계였고(Flautner, Tsafrir/Etsion), 100 MHz 관찰(Endo)은 Windows NT와 BSD/OS 위였습니다".

#### F-52 — v08:1144, :1656 — RECORD-BELOW-STANDARD
- Repo: rt-app's "absolute" mode "와 fixed-timestep 게임 loop의 simulation step은 따라잡습니다(`rt-app`, `fiedler-gaffer04`)".
- Record: refs:575–578 — quotes ("the renderer produces time and the simulation consumes it in discrete dt sized steps"; "more steps to catch up"), URL, accessed 2026-10-06; no search or read record holds the passage (grep of `_dev/research/jioh/**/*.md` outside `sources/` finds `fiedler` only in 9.11/changelog.md and 9.15 logs). The wording is within the registry's quotes.
- Proposed fix: a read record for Fiedler's article (verbatim passages, URL, date, hash) in 9.11's search records, or the blind re-read below.

#### F-54 — v08:1027, :1722 — RECORD-BELOW-STANDARD
- Repo: "`sched_waking`은 잠든 thread에만 발생하고 scheduler가 그 thread를 내려놓기 전에 찍히므로 …".
- Record: 9.7/changelog.md:115 — "`kernel/sched/core.c` v6.17, `try_to_wake_up`: `trace_sched_waking` after `ttwu_state_match`" — file, function and version, but no verbatim passage and no copy (URL or hash, date). No other record holds it (`ttwu_state_match` appears only there and in the workflow).
- Proposed fix: record the `try_to_wake_up` lines at v6.17 verbatim with the copy, e.g. beside 9.11's D2-fair copies (`9.11/sources/D2-fair/core.c@v6.17` exists locally).

#### F-55 … F-60 — the measurement method's six sources — RECORD-BELOW-STANDARD
- Repo: v06 §7 (lines 869–961, 1037, 1686–1688) and v08:983, :1719 quote `kalibera-ismm13` §3, §9.3, §11, §12; `georges-oopsla07` §4.3, §6.2.1; `maricq-osdi18` §2; `chow-aoms65` (3) and Starr's .929; `cochran-st77` §6.3, §6.5, §9A.1; `feller-ipta50` §12.4. Every quoted phrase was found in the registry entry (refs:112–140) or the workflow (workflow:22–28); the wording stays within them.
- Record: refs:112–140 carry verbatim passages, sections, URLs and access dates (2026-09-19 to 2026-09-27), written by the deciding sessions (9.6 D24, 9.5 D33, D78, D86, 9.8 D28). No search or read record holds a passage for any of the six (grep of every slice's `search/`, the 2026-09-13 `reads/` and 9.12's audit), so none was read independently of the repository's description.
- Proposed fix: one independent read of the six (neutral topics, as the blind sample does), recorded with passages and copies in a slice's search records; or 인지오 accepts the registry entries as the record for method citations.

#### Other — v08:698, :1864 — stale statement about the registry (not a source claim)
- Repo: "`linux-sched-bwc` entry는 지금도 추가되지 않았습니다(12장)" (v08:698); "**`linux-sched-bwc` reference.** … the entry is "proposed, not added"" (v08:1864, listed among open items).
- Record: `docs/references.md:324` has `### \`linux-sched-bwc\``.
- Proposed fix: state the entry exists (`docs/references.md`, deployed-system, existence only) and drop the open item.

## Record defects found on the way

- The 2026-09-13 LAVD read's slide-16 edge list (`_dev/research/jioh/2026-09-13-verification/reads/R02-lavd.md:45-53`) omits the `wineserver`↔`Troy.exe` and `wineserver`↔`explorer.exe` edges that the 9.4 gaming record (`task-9.4-gaming/search/S2-project-docs.md:91`) lists for the same slide.
- The 9.5 interactive-typing changelog's decision D4 (`task-9.5-interactive-typing/changelog.md:17`) lists Endo 1996 among "the 2000–2004 Linux traces"; its own candidates (`search/candidates.md:24–25`) place Endo on Windows NT and BSD/OS (the source of F-49).
- The 9.12 related-work changelog's decision D26 (`CL12:442`, the proposal's Linux scheduling-class statements) introduced "deterministic" for EEVDF from no passage (the source of A-46).

## Boundary

- The role lines of the `docs/references.md` entries are not audited here. Known overlaps with the findings: `cpsmark-tbench23` (`docs/references.md:34`, module sensitivity attributed to Table 4, as D-42), `chromium` (its scope, the fallback without a sound device, which B-33's sentence drops), `linux-sched-bwc` (whether its role repeats B-17's "per-class").
- Outside this audit's files but carrying a finding's wording: `docs/memos/2026-09-13-critical-findings.md:64` (D-22, F-14); `docs/workload/grounding-sources.md:30` ("Valve sponsors", A-09); `dataset/archetypes.yaml` `game-task-chain` `validation_stats.reason` (D-39, F-48).
- General background in the research guidebook that names no source document, left uninventoried for the lead's call: Linux's scheduler history with years (vol-01:2694, :2716, :2874, :3212–3216 — CFS in 2007, EEVDF "in a 2023 kernel"; only EEVDF from v6.6 is in a record, `task-9.11-scheduler-constants/search/S2-project-docs.md:45`), Pathfinder 1997 (vol-01:2048), cgroups and Docker CPU quotas (vol-01:3224–3226).
