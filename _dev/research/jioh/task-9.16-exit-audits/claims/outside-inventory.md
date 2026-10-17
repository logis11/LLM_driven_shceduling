# 9.16 claim audit — claims outside the workload dataset: inventory

Task 9.16 (the Phase 9 exit audits), decision 1 (the claim audit), for the citations outside the workload dataset — the Phase 9 scope's third group. Repository at `928aa8fd` (`jioh/dataset-rebuild`), read 2026-10-17. Standard: the Phase 9 spec's decision 1 (a claim is verified when a record holds the verbatim passage, its locator and the copy read — URL or commit, version, date — and the repository's wording stays within the passage's object, unit, statistic, scope and population).

Files covered: `docs/related-work.md`, `docs/research-proposal.md`, `docs/research-claims.md` (part A); `docs/harness/*.md`, `harness/experiments/rq0-gate.yaml`, `harness/guards/guard-spec.yaml`, `harness/scoring/scoring-spec.yaml`, `harness/boot-defaults/`, `docs/recognition-vocabulary.md`, `docs/background-guide.md`, `docs/terminology.md`, `docs/simulator/*.md`, `docs/daemon/*.md` (part B); the research guidebook's volumes 1–5 (part C) and volume 6 (part D); the dataset guidebook's volumes 01–04 (part E) and 05–08 (part F) — for the guidebooks, only statements that cite a `docs/references.md` id or name a source. Not covered: the role lines of the `docs/references.md` entries themselves (see `outside-findings.md`, Boundary).

Not inventoried (left to the measurement audit, decision 2): statements resting on our own measurements (`meas-ci`, `meas-local`, `meas-pending`) — about 280 across the six parts. Also not inventoried: references to our own documents and decisions, and our own design stated as such.

## Verdicts

TRACED — a record meets the standard and the wording is within its passage. WORDING-OUTSIDE-PASSAGE — a record exists; the wording goes beyond it. NO-RECORD — no record holds a passage for the claim. RECORD-BELOW-STANDARD — the only record lacks the passage, the locator or the copy identification, or is the registry author's own read (not independent). LABELLED — a value no source states, labelled as convention, arithmetic, placeholder or design.

Counts: 353 claims — TRACED 270, WORDING-OUTSIDE-PASSAGE 41, RECORD-BELOW-STANDARD 23, NO-RECORD 11, LABELLED 8. Every non-TRACED, non-LABELLED claim is in `outside-findings.md`.

## Columns and path abbreviations

Each row: claim id (its letter is the part), location, source, the repository's wording (short verbatim), the record (path:line), the verdict, when the current wording was introduced (`git log -S` on a distinctive phrase: the most recent commit adding it), and the record's date (the read's access date, or the decision or audit entry that quotes the content). Record paths use each part's abbreviations:

- Part A: `S1`, `S2`, `S3` = `_dev/research/jioh/task-9.12-related-work-prose/search/S1-literature.md`, `S2-project-docs.md`, `S3-traces-datasets.md`; `AA` = that slice's `search/A-audit.md` (the 9.12 audit re-reads of 2026-10-09); `CL12` = `task-9.12-related-work-prose/changelog.md`; `CL11` = `task-9.11-scheduler-constants/changelog.md`; `S2-11s` = `task-9.11-scheduler-constants/search/S2-project-docs.md`. File names in the location column are under `docs/`; `proposal` = `docs/research-proposal.md`.
- Part B: `R11/`, `R12/`, `R4/`, `R15/`, `R19/` = `_dev/research/jioh/task-9.11-scheduler-constants/`, `task-9.12-related-work-prose/`, `task-9.4-gaming/`, `task-9.15-docs-memos-and-guidebook-corrections/`, `task-9.19-generator-and-the-c3-grids/`; `R01` = `_dev/research/jioh/2026-09-13-verification/reads/R01-interbench-rtapp-benchtools.md`.
- Part C: `R11`, `R12`, `R10` = `_dev/research/jioh/task-9.11-scheduler-constants/`, `task-9.12-related-work-prose/`, `task-9.10-scenarios-timelines/` (written `R12search/…` for `R12/search/…`); `RV` = `_dev/research/jioh/2026-09-13-verification/`; `vol-0N` = `docs/guidebook/vol-0N-*.md`.
- Part D: `R01`…`R09` = `_dev/research/jioh/2026-09-13-verification/reads/R0N-*.md` (the 2026-09-13 independent reads); `9.N Sk` = `_dev/research/jioh/task-9.N-*/search/Sk-*.md`; `vol-06` = `docs/guidebook/vol-06-archetypes-and-grounding.md`.
- Part E: `G/` = `docs/guidebook/dataset/`; `R/` = `_dev/research/jioh/`; `9.10 S2` = `R/task-9.10-scenarios-timelines/search/S2-project-docs.md` (and likewise for S1, S3, S4); `K1`–`K4` = `R/2026-09-13-verification/compare/K1.md`…; `R02`, `R04`, `R07`, `R10`, `R11` = `R/2026-09-13-verification/reads/R02-lavd.md`, `R04-cpsmark.md`, `R07-gamemode-steam-dkms.md`, `R10-task-switching.md`, `R11-focal-plain.md`.
- Part F: `vNN` = `docs/guidebook/dataset/NN-*.md`; `R0x` = `_dev/research/jioh/2026-09-13-verification/reads/R0x-*.md`; `K2`, `K4` = that verification's `compare/K2.md`, `K4.md`; `9.N/…` = `_dev/research/jioh/task-9.N-*/…`; `refs` = `docs/references.md`; `workflow` = `_dev/research/jioh/measurement-campaign-workflow.md`.

Commits named in the date column: `f30b086b` (2026-10-14) is the dataset guidebook's first write; `ff925573` (2026-09-13) the research guidebook volume 6's; `0e3b627d`, `32a5c9dd` and the other 2026-10-17 commits are the 9.15 sweep (docs, memos and guidebook corrections).

## Claims by source

### `akts-arxiv26`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-24 | related-work.md:32, :34, :48 | `akts-arxiv26` | regime from telemetry, sub-microsecond actuator "a BPF map write"; small models at chance, 20 of 40 | S1:372 (S1-19 Table 1, §4.2), S1:494 (S1-32), AA:276 (A4-04) | TRACED | 0e3b627d 2026-10-17 | 2026-10-07/09 |
| A-65 | proposal:243 | `akts-arxiv26` | AKTS's "13.5 ms median for a single-digit answer from a 0.5B model on an A100" | S1:494 (S1-32 §4.2); CL12:793 (D50, verbatim "median decision latency is 13.5 ms (n=30, temperature 0)") | TRACED | 32a5c9dd 2026-10-17 | 2026-10-08 |
| C-37 | vol-02:2104, :2241–2247, :2609–2668 (§6.4) | AKTS v2, TuxBot v2, Vulcan v3, TuneAgent (KDD '26), Jadhav et al. | "AKTS(arXiv 2609.12276v2)"; TuxBot "최대 41개의 Linux 설정 항목"; Vulcan "Accepted for publication at EuroSys 2027"; TuneAgent build configuration; Jadhav under review | R12search/S1-literature.md:314, :326, :347, :361, :372, :494, :520 (S1-14, S1-15, S1-17, S1-18, S1-19, S1-32, S1-35); V60 inline list :410–424; R12changelog.md:390, :662, :1120 (D24, D42, D72) | TRACED | a9fd9601 2026-09-12 / 00f6a737 2026-10-17 | 2026-10-07/09 |

### `ananicy`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-25 | related-work.md:40; proposal :540 | `ananicy` | upstream archived since 2023-03-21; `name` matched against basename of `argv[0]`, untruncated; nice on every thread, I/O class, policy | S2:385 (S2-30), S2:391 (S2-31), AA:229 (A3-07); CL12:1576 (D105) | TRACED | 0e3b627d 2026-10-17 | 2026-10-07/09 |
| B-36 | docs/daemon/daemon-guide.md:107; docs/terminology.md:215–217; docs/background-guide.md:18, :60 | `ananicy`, `ananicy-rules`, `cachyos-settings` | CachyOS installs and enables ananicy-cpp with the catalogue at `03ef03fb`; ananicy-cpp "keys a rule on the basename of a process's `argv[0]`, untruncated" | R12/search/S2-project-docs.md:481–510 (S2-45, S2-46); R12/search/A-audit.md:231–232 (`process.cpp:193–250` at `v1.2.0`) | TRACED | ec4105b5 2026-10-17; 0e3b627d 2026-10-17 | 2026-10-08; 2026-10-09 |
| C-06 | vol-01:1359, :2110, :3341, :3363, :3397, :3600, :3745; vol-03:99, :117 | ananicy-cpp, CachyOS catalogue (`ananicy`, `ananicy-rules`, the CachyOS default-install entry) | "CachyOS … ananicy-cpp라는 daemon을 기본으로 설치해서 켜 둡니다 … community가 관리하는 규칙 목록 … nice 값, I/O class, scheduling policy … 게임 이름에는 priority를 올리는 규칙이, 배경 작업 이름에는 내리는" | R12search/S2-project-docs.md:385–397 (S2-30–S2-32), :481, :500 (S2-45, S2-46: install hook enables `ananicy-cpp`, ISO 2026-08-09); R12changelog.md:46 (9.12 D3, the ananicy sentence) | TRACED | 00f6a737 2026-10-17 | 2026-10-08 |
| D-45 | vol-06:2013-2015, 4129 | `ananicy` (upstream) | original Ananicy uses lower-case types (`game`, `compiler`) and keeps the upper-case ones under "Depricated types" | R06:695-703, :795-815 | TRACED | ff925573 2026-09-13 | 2026-09-13 |

### `ananicy-rules`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-26 | related-work.md:40 | `ananicy-rules` | maintained by the CachyOS team and community, PR or issue, "15 813 entries at `03ef03fb` (tag 1.1.49)", 112 authors | S2:397 (S2-32 `README.md:3`, `:63-65`), S3:196 (S3-03), S3:488 (S3-19) | TRACED | 0e3b627d 2026-10-17 | 2026-10-07/08 |
| A-34 | proposal:34, :60, :159, :195, :540, :547 | `ananicy-rules`, `cachyos-settings` | CachyOS "installs and enables by default a community-maintained catalogue" giving each listed name a priority class | as A-26, A-27 | TRACED | 32a5c9dd 2026-10-17 | 2026-10-07/08 |
| A-78 | proposal:650–652 | `ananicy-rules` | catalogue lacks `zrythm`, `qtractor`; Discord registered `Chat`; a Godot game's own name absent; "`node` is registered (`BG_CPUIO`, the idle class)"; cluster and database programs absent | AA:366 (A5-01); CL12:80 (D5) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-09 |
| A-79 | proposal:654 | `ananicy-rules`, `feral-gamemode`, `gamemode-docs`, `apple-gamemode` | no game mode's documentation addresses audio workstations; Feral's user-applied; `reaper`, `bitwig-studio`, `ArdourGUI`, `lmms`, `audacity` as `Player-Audio` | S3:488 (S3-19 audio entries, :508); S2:269, :287, :299 coverage lines; CL12:80 (D5) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-07/08 |
| A-86 | research-claims.md:159–162 | `ananicy-rules`, `ananicy` | CachyOS's catalogue at `03ef03fb` as CachyOS installs and enables it with ananicy-cpp, "matched by each process's `argv[0]` basename, untruncated" | as A-25, A-26, A-27 | TRACED | 0e3b627d 2026-10-17 | 2026-10-07/09 |
| C-07 | vol-01:3399, :3401; vol-02:3033–3069 table | `ananicy-rules` at `03ef03fb` | "2026-09-08 시점의 목록에는 규칙이 15 813개 … 13 528개(85.5퍼센트)가 게임 이름"; "2025년 말에 1 645개"; per-type counts (BG_CPUIO 1,615 …) | R12search/S3-traces-datasets.md:196–213 (S3-03, "entries per type: Game 13528, BG_CPUIO 1615, …"), :488–501 (S3-19, HEAD `03ef03fb` 2026-09-08, 1 645 at end 2025); 85.5 % is 13 528 / 15 813, arithmetic | TRACED | 00f6a737 2026-10-17 (vol-02 table cd3ba642 2026-09-12) | 2026-10-07/08 |
| C-38 | vol-02:2875–3141 (§7.3–7.4) | upstream Ananicy README; ananicy-rules README and `00-types.types` at `03ef03fb` | self-description quote; rule format; the whole types file; Just Cause 2 and Mortal Shell examples; upstream's current types file has lower-case types, the old ones commented out as "폐기된 분류" | V60-vol02-quotations.md:519–531 (types file `diff`-identical); R12search/S2-project-docs.md:385–397; RV/reads/R06-ananicy.md:815 (older type names commented out) | TRACED | cd3ba642 2026-09-12 | 2026-09-13 / 2026-10-09 |
| C-39 | vol-02:2964, :3232, :3362 | ananicy-rules; hackbench; PCMark 10 | "가장 널리 쓰이는 카탈로그 하나"; hackbench "가장 오래되고 널리 쓰이는 도구"; PCMark 10 "가장 널리 쓰이는 것 하나" | none: no record measures use of any of the three (RV/compare/K1.md:65 graded the like claim "widely cited" for `stress-ng` UNVERIFIABLE) | NO-RECORD | cd3ba642 2026-09-12 | — |
| C-45 | vol-03:1920, :1929, :2175, :2405, :2693, :3803; vol-04:451, :496, :500, :570, :614, :1816 | ananicy-rules `03ef03fb`, ananicy-cpp 1.2.0 | `shipped_catalogue` "`argv[0]` basename에 자르지 않고"; "만 오천 개가 넘는 항목"; "이름 35개 중 19개에만 규칙 … 모든 이름에 규칙이 있는 파일은 7개" | R12search/A-audit.md:240 (A3-09); R12changelog.md:97 (D6), :1576 (D105, `process.cpp:193–250` at `v1.2.0`), :1625 (D109) | TRACED | 00f6a737 / ba94cbb5 2026-10-17 | 2026-10-09 |
| C-49 | vol-04:1431 | ananicy-rules; Game Mode docs; Feral GameMode | "`reaper`, `bitwig-studio`, `ArdourGUI`, `lmms`, `audacity` … `Player-Audio`"; no game mode doc covers DAWs; Feral's can be applied by the user | R12changelog.md:80 (9.12 D5, citing S3-19 "Passages: audio entries", S2-16, S2-18, S2-19) | TRACED | ba94cbb5 2026-10-17 | 2026-10-08 |
| D-43 | vol-06:1631-1647, 1884, 2001-2011, 2025-2029, 2147 | `ananicy-rules` (at `03ef03fb`, 2026-09-08) | `BG_CPUIO` and `Heavy_CPU` type lines with comments; `baloo_file` BG_CPUIO in `plasma.rules`; no entries for `tracker-miner-fs-3`, `updatedb`, `cc1`, `gcc`, `make`, `clamscan`; `clamd` BG_CPUIO; 15 types; Game "Use more CPU time if possible" | R06:7, :25-80, :173-214, :216-266, :303-316 | TRACED | ff925573 2026-09-13 | 2026-09-13 |
| D-44 | vol-06:2033-2049 | `ananicy-rules` | entries listed: BG_CPUIO `borg`, `rsync`, `transmission-daemon`, `clamd` (verbatim in record); BG_CPUIO `wget`, `curl`, `aria2c`; Chat `discord`, `zoom` (verbatim) and `element-desktop`, `slack`, `thunderbird` | R06:270-312 (borg, rsync, transmission, clamd, zoom, discord verbatim; wget, curl, aria2c, slack, element-desktop, thunderbird only in the reader's reading line :281, :312, no rule line quoted) | RECORD-BELOW-STANDARD | ff925573 2026-09-13 | 2026-09-13 |
| D-46 | vol-06:2057, 3027 | `ananicy-rules` | `dbus-daemon` in `Service`; `gnome-shell`, `Xorg` and `pipewire` all `LowLatency_RT` | gnome-shell, pipewire: 9.12 S3:511, :514 (audioserver.rules; core-set names matched to `LowLatency_RT`). `Xorg` and `dbus-daemon`: no record; present in the copy at `00-default/DEs-and-WMs/xorg.rules:2`, `00-default/Services/dbus.rules:3` (grep, this audit) | NO-RECORD | ff925573 2026-09-13 | 2026-10-08 (partial) |
| E-52 | G/01:83, :442, :946; G/04:194; G/01:1500 | `ananicy-rules`, ananicy-cpp, CachyOS | the catalogue CachyOS installs with ananicy-cpp and enables (commit `03ef03fb`), matched on each process's `argv[0]` basename, untruncated; on that key 19 of 35 bound names, all names in 7 of 50 files | `R/task-9.12-related-work-prose/changelog.md:1576–1585` (9.12 D105: ananicy-cpp `v1.2.0` `process.cpp:193–250`, `rules.cpp:184`), `:46–60` (9.12 D3, records S2-45, S2-46), `:1625` (9.12 D109 count); `R/task-9.12-related-work-prose/search/S2-project-docs.md:481, :500` | TRACED | d62372dc / df38aa54 2026-10-17 | 2026-10-08 / 2026-10-09 |
| F-33 | v06:519; v08:749 | `ananicy-rules`, CachyOS | a `type` is a prescription (nice, ioclass, sched); CachyOS installs and enables ananicy-cpp with the catalogue at `03ef03fb`; matched on `argv[0]`'s basename | R06:32–53; 9.12/search/candidates.md:25, :50; 9.12/search/A-audit.md:232 | TRACED | v06:519 2c451543 2026-10-17 | 2026-09-13; 2026-10-08/09 |

### `apple-gamemode`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-30 | related-work.md:40, :48 | `apple-gamemode`, `apple-lssupportsgamemode` | Apple silicon, Sonoma 14+, full screen; `LSSupportsGameMode` "listed for macOS 26.0 and later" | S2:287 (S2-18), S2:314 (S2-20), AA:404 (A5-06) | TRACED | 0e3b627d 2026-10-17 | 2026-10-07/09 |
| A-51 | proposal:148 | `apple-gamemode`, `apple-lssupportsgamemode` | macOS Game Mode row (Sonoma 14+, Apple silicon, full screen; `LSSupportsGameMode` from macOS 26) | as A-30 | TRACED | 32a5c9dd 2026-10-17 | 2026-10-07/09 |

### `apple-qos`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-50 | proposal:147 | `apple-qos`, `apple-energy-guide` | four QoS classes; developer declares; "work left undeclared is treated as `default`" | S2:323 (S2-21 Tables 10-1, 10-2), S2:563 (S2-53) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-07/08 |
| C-12 | vol-01:3277–3300, :3338; vol-03:55 | Apple `QualityOfService` page; Energy Efficiency Guide (archived) | four QoS classes, "background … 색인, 동기화, 백업"; "선언하지 않으면 `default`" | R12search/S2-project-docs.md:563 (S2-53), :323 (S2-21: "Work that has no QoS information assigned is treated as default", background "such as indexing, synchronizing, and backups"); R12changelog.md:460 (D28) | TRACED | 00f6a737 2026-10-17 | 2026-10-08 |

### `ardour-manual`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-80 | proposal:654, :816 | `ardour-manual`, `jackd-man`, `pipewire-conf`, `steamdeck-store` | target below 5 ms; jackd defaults (2 periods, 48 000, 1024); 32-frame period "(arithmetic)"; studios monitor through an external console; xrun "clicks, pops and crackles"; PipeWire quantum 1024; Steam Deck LCD 60 Hz, OLED 90 Hz | AA:115 (A2-08), S2:598 (S2-57) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-07/09 |

### `asa-arxiv25`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-16 | related-work.md:24, :26, :34, :48 | `asa-arxiv25` | trained once offline, time-weighted voting, per-machine mapping table, optional fine-tuning; no process identity; 96.83 % / 99.19 % | S1:246 (ASA pp. 4, 9) | TRACED | 0e3b627d 2026-10-17 | 2026-10-07 |
| C-34 | vol-02:1967–2175 (§5.6) | ASA, arXiv:2511.11628v1 | quotations; 96.83 % / 99.19 %; per-machine mapping table | V60-vol02-quotations.md (rows 1955–2148 and the inline list at :410–424); R12search/S1-literature.md:246–261 (S1-11, p. 9); R12changelog.md:205, :356 (D12, D21) | TRACED | a9fd9601 2026-09-12 | 2026-10-08/09 |

### `atil-eval4nlp25`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-83 | proposal:736 | `atil-eval4nlp25`, `cooper-arxiv26` | hosted deterministic-configured models "varied in accuracy by up to 15 % across runs"; greedy outputs differ across GPU architectures; batched serving | AA:223 (A3-06, Atil p. 135), S1:529 (S1-36 abstract, §2) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-09 |

### `borg`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| F-44 | v08:1019 | borg 1.4.1 | one process, no worker threads, 512 KiB–8 MiB content-defined chunks | 9.7/search/candidates.md:55; 9.7/search/S2-project-docs.md:137 | TRACED | f30b086b 2026-10-14 | 2026-09-19 |

### `brodersen-icpr10`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| B-01 | docs/harness/metrics.md:258 | `brodersen-icpr10` | balanced accuracy "defined for two classes … defines it off a two-by-two matrix and gives no K-class form" | R11/search/S1-literature.md:129, :134 | TRACED | bcaebf64 2026-09-11 | 2026-09-24 |

### `build-tool-docs`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| E-36 | G/02:955 | build tools' documentation (make, ninja, cargo, dpkg, Debian kernel handbook, rpm, Gentoo, dkms, Phoronix Test Suite) | "every vendor default found is `nproc` or a memory-capped variant" | `R/task-9.6-compile/changelog.md:21` (9.6 D4, naming search records S2-03…S2-20 of `R/task-9.6-compile/search/S2-project-docs.md`) | TRACED | f30b086b 2026-10-14 | 2026-09-17 |

### `cachyos-settings`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-27 | related-work.md:40, :48; proposal :547 | `cachyos-settings` | "CachyOS's installer installs and enables ananicy-cpp with it by default" | S2:481 (S2-45), S2:500 (S2-46) | TRACED | 0e3b627d 2026-10-17 | 2026-10-08 |

### `cargo-book`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-62 | proposal:185 | `cargo-book` | `cargo build` compiles a package and its dependencies, "Cargo invoking `rustc`" | S2:592 (S2-56), AA:111 (A2-07) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-09 |

### `chambers-imc05`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-69 | proposal:309 | `chambers-imc05` | "most sessions lasted minutes — a Weibull fit with a median of about 9.6 min — and more than 99 % under 2 h" | AA:130 (A2-12, p. 4); CL12:1097 (D70: the median as arithmetic) | WORDING-OUTSIDE-PASSAGE | 32a5c9dd 2026-10-17 | 2026-10-09 |

### `chang-chi21`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| D-34 | vol-06:2681-2683 | `chang-chi21` | the registry's "median tab-overwhelm threshold 8 tabs (IQR 5-12)" quoted, the volume's own read failed | R09:78-91 (median 8, IQR 5–12, N = 103, self-reported) | TRACED | ff925573 2026-09-13 | 2026-09-13 |

### `chicco-bmcg20`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| B-02 | docs/harness/metrics.md:258 | `chicco-bmcg20` | "MCC is undefined when a whole row or column of M is zero"; "Chicco and Jurman fill those cases by convention — 1 or −1 …, otherwise 0 as a limit" | R11/search/S1-literature.md:198; R11/changelog.md:372 (9.11 decision D27, the metrics citation wording) | WORDING-OUTSIDE-PASSAGE | e6514137 2026-10-08 | 2026-10-08 |

### `chow-aoms65`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| E-45 | G/02:646 | `chow-aoms65` | a sequential interval stopped at the first pass reaches nominal coverage only asymptotically | `docs/references.md:127–130` only (author's read 2026-09-25) | RECORD-BELOW-STANDARD | f30b086b 2026-10-14 | 2026-09-25 |
| F-58 | v06:883, :944, :1688 | `chow-aoms65` | rule (3) "N = smallest k ≥ 1 such that v_k ≤ (d²k)/a_k²"; asymptotic only; Starr: "about .929" | refs:127–130 — author's read only | RECORD-BELOW-STANDARD | f30b086b 2026-10-14 | 2026-09-25 |

### `chromium`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| B-33 | docs/simulator/simulator-guide.md:136 | `chromium` | "Chromium's fake audio output runs a late callback once and moves to the next on-time interval" | none in a search or read record; `docs/references.md` `chromium` (author's read 2026-10-06); R11/changelog.md:241 restates the registry | RECORD-BELOW-STANDARD | 5479dcab 2026-10-06 | 2026-10-06 (registry) |

### `chromium-docs`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| D-35 | vol-06:2687-2691 | Chromium process model | tab sources give tabs, not processes; Chromium's process rule depends on version and settings (site isolation) | R09:240-274 (none of the four tab sources states processes per tab; `process_model_and_site_isolation.md` @2ea96871) | TRACED | ff925573 2026-09-13 | 2026-09-13 |
| D-36 | vol-06:1818 | Chromium process model | `renderer-hidden` is "사이트마다 렌더러 하나, Chromium의 site-per-process 모델" (one renderer per site) | R09:258-262 ("In (one-)site-per-process mode, each process is locked to documents from a single site"; separate instances of a site "can safely run in separate processes"; soft process limit reuses same-site processes) | WORDING-OUTSIDE-PASSAGE | ba94cbb5 2026-10-17 | 2026-09-13 |
| E-40 | G/02:780 | Chromium, Qt documentation and source | without vsync Chromium drives its compositor from a default 60 Hz timer; Qt Quick paces on a blocking buffer swap; CPU rasterisation lengthens runs "by an amount no source states" | `R/task-9.5-interactive-typing/search/S8-display-gpu.md:24–41`; `…/changelog.md` D24 | TRACED | f30b086b 2026-10-14 | 2026-09-16 |
| F-46 | v06:1303 | Chromium docs, Qt 5.15 source | compositor on a default 60 Hz timer without vsync; Qt Quick threaded loop paces on a blocking swap | 9.5/search/S8-display-gpu.md:16–30 | TRACED | f30b086b 2026-10-14 | 2026-09-16 |

### `clamav`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| E-01 | G/01:45; G/02:1137; G/04:1069, :1651 | ClamAV documentation (`clamav`) | ClamAV calls itself a toolkit "designed especially for e-mail scanning on mail gateways", "not a traditional anti-virus or endpoint security suite"; no ClamAV package ships a scheduled scan; ClamTk "no longer maintained" | 9.10 S2:3598–3605 (S2-30, commit `26dceb23`, accessed 2026-10-01) | TRACED | f30b086b 2026-10-14 | 2026-10-01 |
| F-38 | v06:1174; v08:611, :1081, :1100, :1691 | ClamAV docs, ClamTk, Debian popcon | "designed especially for e-mail scanning on mail gateways"; "ClamAV is not a traditional anti-virus or endpoint security suite"; ClamTk "is no longer maintained"; 0.11 % regular use | 9.10/search/S2-project-docs.md:3598–3612 | TRACED | f30b086b 2026-10-14 | 2026-10-01 |

### `cochran-st77`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| E-46 | G/02:640 | `cochran-st77` | the ratio estimator behind a table's half-width | `docs/references.md:132–135` only (author's read 2026-09-26) | RECORD-BELOW-STANDARD | f30b086b 2026-10-14 | 2026-09-26 |
| F-59 | v06:873, :899, :959 | `cochran-st77` | §9A.1 ratio estimate; §6.3 "exceeds 30 … less than 10%"; §6.5 "tends to give values that are too low" | refs:132–135 — author's read only | RECORD-BELOW-STANDARD | f30b086b 2026-10-14 | 2026-09-26 |

### `coetzee-arxiv12`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| D-30 | vol-06:3233-3245, 3257-3258, 3508 | `coetzee-arxiv12` | Coetzee, Bhaskar, Necula 2012; §9 paragraph quoted (Jockey; "the Linux kernel build's enormous number of short-lived processes like cp and mkdir"); arXiv:1203.2704 v1, 11 pages | R03:14, :99-130 | TRACED | ff925573 2026-09-13 | 2026-09-13 |
| E-35 | G/02:995 | `coetzee-arxiv12` | the Linux kernel build's many short-lived processes, examples `cp` and `mkdir`, no count (sec-9) | K1:610 | TRACED | f30b086b 2026-10-14 | 2026-09-13 |
| F-13 | v06:518 | `coetzee-arxiv12` | Coetzee speaks of the Linux kernel build's many short-lived processes with `cp` and `mkdir` as examples, without a count | R03:99–120 | TRACED | da39802c 2026-10-17 | 2026-09-13 |

### `corbato-sjcc62`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| C-21 | vol-02:280–428 (§2.2) | Corbató, Merwin-Daggett & Daley 1962 | 18 block quotations and the level-classification prose | R12search/V60-vol02-quotations.md:39–66 (all E); R12search/S1-literature.md:135 (S1-04); R12changelog.md:314 (D18) | TRACED | a9fd9601 2026-09-12 | 2026-10-09 |

### `corbet-lwn24`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| D-26 | vol-06:4109 | `corbet-lwn24` | "위 발표를 다룬 LWN 기사" (the LWN article covering the talk above, i.e. `lavd-ossna24`) | R02:182-190 ("covers the sched_ext microconference at the 2024 Linux Plumbers Conference (a different talk from OSS NA, April 2024, given remotely)") | WORDING-OUTSIDE-PASSAGE | ff925573 2026-09-13 | 2026-09-13 |
| F-22 | v06:280 | `corbet-lwn24`, `swell-icmi14` (history) | "Valve ships it; Meta adopted …" was MISATTRIBUTED; SWELL-KW "access-gated" CONTRADICTED | K2:43–44; K4:71 | TRACED | 2c451543 2026-10-17 | 2026-09-13 |

### `cpsmark-tbench23`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| D-41 | vol-06:2236-2246, 2456 | `cpsmark-tbench23` | the plan's "consistent with CpsMark+ Table 4's signature"; Table 4 is a hardware-sensitivity table, not a temporal alternation | R04:164-246 (Table 4 caption "The sensitivity of the workload performance to various hardware characteristics") | TRACED | ff925573 2026-09-13 | 2026-09-13 |
| D-42 | vol-06:2248 | `cpsmark-tbench23` | "인용 문서는 Table 4를 작업과 모듈마다의 하드웨어 민감도 표로 적고(1.77배는 CC 모듈에서 가장 좋은 그래픽 카드 구성을 기본 구성과 비교한 수)"; existence of office, browsing, mail, photo, transcode, archive scenarios; read 2026-09-13 from the Wayback publisher PDF | R04:7 (copy), :188-209 (Table 4 per workload), :225-237 (module values: Table 5 p. 12 and §4.7.2 text "The CC module … 1.77 times better") | WORDING-OUTSIDE-PASSAGE | ba94cbb5 2026-10-17 | 2026-09-13 |
| E-30 | G/02:1167 | `cpsmark-tbench23` | HandBrake workload: "Convert the H.264 encoded source video with 4K resolution to the H.256 [sic] encoded target video with 2K resolution, the container format is MP4"; CpsMark+'s own code uses H.264 | R04:121; 9.10 S2:3903 (S2-58, CpsMark+ source) | TRACED | f30b086b 2026-10-14 | 2026-09-13 / 2026-10-03 |
| E-31 | G/02:839 | `cpsmark-tbench23` | Outlook workload: "receive, browse email contents and attachments offline, including Word, Excel, and PowerPoint files … reply" | R04:113, :145 | TRACED | f30b086b 2026-10-14 | 2026-09-13 |
| F-34 | v06:540 | `cpsmark-tbench23` | Table 4 is per-workload hardware sensitivity; the cited 1.77× is Table 5's CC module figure | K2:55–57 | TRACED | f30b086b 2026-10-14 | 2026-09-13 |
| F-35 | v06:528; v08:763 | `cpsmark-tbench23` | read in full the same day from the Wayback-archived publisher PDF | R04:7 | TRACED | v08:763 aaec6cde 2026-10-17 | 2026-09-13 |
| F-36 | v06:1488; v08:1094, :1696, :1749 | `cpsmark-tbench23` | CpsMark+ defines the HandBrake workload; the paper writes "H.256", its code uses H.264 | 9.10/changelog.md:207 (R04's passage, p. 6), :1686 (code, S2-58) | TRACED | f30b086b 2026-10-14 | 2026-09-13; 2026-10-03 |

### `dai-lpc25`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-07 | related-work.md:8 | `dai-lpc25` | `scx_lavd` "as a candidate default fleet scheduler" | S2:211 (contribution 2099) | TRACED | 0e3b627d 2026-10-17 | 2026-10-07 |

### `darpa-optc`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-75 | proposal:589 | `darpa-optc`, `behacom-dib20` | OpTC process-create events with image paths "from Windows 10 enterprise endpoints in an instrumented exercise"; BEHACOM foreground program per minute, natural use | 2026-09-13-verification/reads/R11-parts/plain-7-8-9.md:166–205 (OpTC at `5b108604`); S3:428 (S3-16) | TRACED | 6f508a59 2026-10-17 | 2026-09-13 / 2026-10-07 |

### `deber-chi15`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-40 | proposal:111 | `deber-chi15` | "a mean detection threshold of 96 ms for tapping on an indirect touch surface", "the textbook threshold of 100 ms" | AA:91 (A2-02, pp. 1829, 1831) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-09 |
| B-08 | docs/harness/metrics.md:299 | `deber-chi15` | JNDs 69 ms touchscreen tapping, 96 ms "touchpad-like indirect surface"; 12 tapping sessions, 14 participants; key typing among indirect tapping tasks, 100 ms within their 95 % CI | R11/search/S1-literature.md:244–246; R12/search/A-audit.md:93 | TRACED | 99257433 2026-10-08 | 2026-10-08; 2026-10-09 |

### `debian-popcon`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| E-02 | G/01:45; G/02:1137; G/04:1069 | Debian popcon | ClamTk ("ClamAV GUI") in regular use 0.11 %; `clamav` 0.85 % | 9.10 S2:3608 (popcon rows: clamtk vote 314, clamav vote 2472, of 291,196 submissions) | TRACED | f30b086b 2026-10-14 | 2026-10-01 |

### `debian-sid-indexes`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-56 | proposal:158 | `debian-sid-indexes`, `debian-code-search` | "of the 1 438 Debian unstable source packages …, 56 (3.9 %)"; 40 lowering, 16 raising, mostly latency-bound daemons | S3:519 (S3-20, :546, :551); CL12:1018 (D64) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-08/09 |
| B-43 | docs/background-guide.md:18 | Debian unstable archive (count) | "of the 1 438 Debian unstable source packages that install a systemd service unit, 56 (3.9 %, a floor) … 40 only lowering … 16 only raising it (mostly latency-bound daemons)" | R12/search/S3-traces-datasets.md:533–551; R12/changelog.md:1025 | TRACED | 0e3b627d 2026-10-17 | 2026-10-08; 2026-10-09 |

### `decima-sigcomm19`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-14 | related-work.md:24 | `decima-sigcomm19`, `firm-osdi20`, `park-neurips19` | Decima RL over job DAGs; FIRM SLO-driven microservices; Park "open platform of twelve system-optimization environments"; state→action mapping | S1:166, :183, :200 (S1-06…08); AA:310 (A4-08) | TRACED | 0e3b627d 2026-10-17 | 2026-10-07/09 |
| C-33 | vol-02:1473–1966 (§5.1–5.5) | Decima, FIRM, Park | quotations; "조정 인자를 41개 값으로" (α ∈ {−2,−1.9,…,2}, arithmetic); "21퍼센트 … 가장 강한 상대와의 차이"; the learned line's limits from the papers' own statements | V60-vol02-quotations.md:259–397 (rows 1483–1926); R12search/S1-literature.md:166, :183, :200 (S1-06–S1-08); R12changelog.md:328, :341, :1240 (D19, D20, D81) | TRACED | a9fd9601 2026-09-12 | 2026-10-09 |

### `deja-dup`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| B-44 | docs/background-guide.md:18 | Tracker, Baloo, Déjà Dup, ClamAV, borg, restic | Tracker and Baloo set background classes on themselves, Déjà Dup wraps its backup in `chrt --idle 0`; ClamAV, borg, restic declare nothing | R11/search/S2-project-docs.md:769–826 (S2-22, S2-24, S2-25, S2-26, S2-27); R15/logs/F1.md:81 (restic re-read 2026-10-17) | TRACED | 0e3b627d 2026-10-17 | 2026-09-24; 2026-10-17 |
| C-11 | vol-01:2097–2102; vol-03:109, :111, :113, :317 | Debian unstable units; LocalSearch, Baloo, Déjà Dup, ClamAV, borg, restic; plocate on Ubuntu 24.04; Apple XNU scheduler doc | "1 438개 중 … 56개(3.9퍼센트) … 바닥값"; "40개는 … 낮추기만 하고, 16개는 높이기만"; "plocate 1.1.19는 I/O만 idle class로 선언"; "Déjà Dup은 백업을 `chrt --idle 0`으로 감싸"; XNU "플랫폼 전체의 priority 부풀림 … Clutch를 만든 동기" | R12search/S3-traces-datasets.md:519 (S3-20), :164 (S3-02); R11search/S2-project-docs.md:769–826 (9.11 S2-22–S2-27); R12search/A-audit.md:103 (A2-05, plocate 1.1.19-2ubuntu2); R12search/S2-project-docs.md:569–575 (S2-54, `sched_clutch_edge.md:7` at `xnu-12377.121.6`); R12changelog.md:225 (D13), :1018 (D64), :1199 (D78) | TRACED | 00f6a737 2026-10-17 | 2026-10-08/09 |
| C-50 | vol-05:508 | Déjà Dup 45.2 | "`deja-dup`은 Ubuntu에 들어 있는 백업 도구 … 켜두면 7일마다 스스로 백업" | R10search/S2-project-docs.md:3940–3948 (S2-62: `periodic-period` `7`, `app.gschema.xml.in:53–54`); R10search/candidates.md:42 (Déjà Dup in the extended install selection) | TRACED | ba94cbb5 2026-10-17 | 2026-10-04 |
| E-04 | G/02:1177; G/04:895 | Debian popcon; Ubuntu packages; `deja-dup`; BorgBackup docs | `deja-dup` installed 4.07 %, regular 2.81 %, `borgbackup` 2.78 % / 1.26 %; Déjà Dup in Ubuntu 24.04's extended install, scheduled backup off by default, every 7 days when on; borg in no Ubuntu install layer; a repeated borg backup does not read unchanged files' contents | 9.10 S3:518 (4.07 %); `R/task-9.10-scenarios-timelines/changelog.md:145` (2.81 %, 2.78 %, 1.26 %, reader's own over S3-30's rows); 9.10 S4:1987; `R/task-9.7-background-io/search/S2-project-docs.md:139` (borg FAQ) | TRACED | f30b086b 2026-10-14 | 2026-10-01 / 2026-09-17 |
| E-05 | G/02:1173, :1333; G/04:886 | `deja-dup` (`CommonUtils.vala`) | Déjà Dup's monitor starts the backup with `chrt --idle 0 ionice -c3` | R11:1864; 9.10 S2:3945–3951 | TRACED | f30b086b 2026-10-14 | 2026-09-13 / 2026-10-04 |

### `dhakal-chi18`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| D-16 | vol-06:850-880, 1162-1163, 1209, 1215, 1376 | `dhakal-chi18` | 168,000 volunteers; 136,857,600 keystrokes from 168,960 participants; mean IKI 238.656 ms (SD 111.6), Table 3 238.66 / 111.60, SD across participants' means; transcription typing; keystrokes > 5000 ms after the previous removed | R08:9 (copy), :45-50, :57, :89, :101, :108, :124, :130 | TRACED | ff925573 2026-09-13 | 2026-09-13 |
| D-17 | vol-06:850 | `dhakal-chi18` | "Dhakal 외 네 명" (Dhakal and four others) | R08:9 ("PDF metadata title/authors match the entry"); entry and copy `sources/dhakal-chi18.txt:3`: Dhakal, Feit, Kristensson, Oulasvirta — four authors | WORDING-OUTSIDE-PASSAGE | ff925573 2026-09-13 | 2026-09-13 |
| E-22 | G/02:666, :1423, :1654 | `dhakal-chi18` | 136M Keystrokes: transcription typing of memorised sentences; mean of per-participant mean IKI 238.66 ms | K4:116 (p. 5 "Average inter-key interval is 238.656 ms (SD = 111.6)", Table 3); R08:9–10 | TRACED | f30b086b 2026-10-14 | 2026-09-13 |
| F-29 | v06:1012; v08:1647 | `dhakal-chi18` | 168,960 participants transcribing memorised sentences | R08:101–103, :125, :139 | TRACED | f30b086b 2026-10-14 | 2026-09-13 |
| F-30 | v08:954 | `dhakal-chi18` (136M data) | "transcription of memorised sentences, share > 1 s 0.7 %" | 9.5/search/candidates.md:11 ("S3's six-participant sample: … share > 1 s 0.7 %") | WORDING-OUTSIDE-PASSAGE | f30b086b 2026-10-14 | 2026-09-13 |
| F-32 | v06:1117 | `dhakal-chi18` | the `aalto-*` windows follow the source's terms (non-commercial research, attribution) | 9.5/search/candidates.md:11 ("non-commercial with attribution") | TRACED | 2c451543 2026-10-17 | 2026-09-13 |

### `dietterich-neco98`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| B-04 | docs/harness/metrics.md:262 | `dietterich-neco98` | paired comparison; "names this case and rules out both a difference of two proportions and a resampled t test" | R11/search/S1-literature.md:163, :166 | TRACED | bcaebf64 2026-09-11 | 2026-09-24 |

### `dkms`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| E-08 | G/02:1205; G/04:1759 | `dkms`; Debian popcon | the DKMS hook runs `dkms autoinstall` when a kernel or headers are installed; popcon DKMS installed 14.70 %, regular 7.07 %, `nvidia-kernel-dkms` 3.76 %; DKMS not in the default layer | 9.10 S2:1048–1050 (`/etc/kernel/postinst.d/dkms:37–39`, "DKMS (not in the default install)"); 9.10 S3:507–518 (rows dkms 42793/20582, nvidia-kernel-dkms 10957; reader's 14.70 %, 3.76 %) | TRACED | f30b086b 2026-10-14 | 2026-10-01 |
| E-10 | G/02:1187 | `dkms` | NVIDIA's `dkms.conf` and dkms read `nproc` | 9.10 S2:1048 (`/usr/sbin/dkms` lines 180–188, CPU count) | TRACED | f30b086b 2026-10-14 | 2026-10-01 |

### `dkms-man`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| C-53 | vol-05:1206, :1321 | DKMS man page | "`dkms`는 리눅스 배포판이 커널을 업데이트한 뒤에 **알아서 돌리는** 모듈 재빌드 도구" | RV/reads/R07-gamemode-steam-dkms.md:219–223 (autoinstall, `AUTOINSTALL=` "will automatically try to install this module on any kernel you boot into"); the measured rebuild is `meas-ci` | TRACED | 55bc3012 2026-09-13 | 2026-09-13 |
| F-45 | v08:638 | `dkms-man`, `dkms-debian` | "kernel modules to be dynamically built for each kernel on your system" | R07:211 | TRACED | f30b086b 2026-10-14 | 2026-09-13 |

### `dubroy-chi10`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| D-32 | vol-06:2653-2667, 2699, 2761 | `dubroy-chi10` | 21 Firefox users over 2–3 weeks; most common open-tab count one, second peak 16 from two participants; no other participant's median above 6; maximum 42; recruitment of heavy tab users | R09:27-34, :55-70 | TRACED | ff925573 2026-09-13 | 2026-09-13 |

### `eevdf-tr95`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-12 | related-work.md:16 | `eevdf-tr95`, `linux-sched-eevdf`, `linux-sched-cfs` | virtual run time and lag, eligible task with earliest virtual deadline, "a sleeping task's lag decaying", sleeper handling | S2:96 (`sched-eevdf.rst:13-32`), S2:105 (`sched-design-CFS.rst:51-53`), S1:149 (TR p. 7) | TRACED | 0e3b627d 2026-10-17 | 2026-10-07 |
| C-24 | vol-02:517–664 (§2.5) | Stoica & Abdel-Wahab TR-95-22 | quotations; "lag는 … 2절 \"Assumptions\"(4쪽)에서 정의 … 3절 … (6쪽)" | V60-vol02-quotations.md:82–106; R12changelog.md:851 (D53: "defined in §2 (p. 4), virtual time formally in §3 (p. 6)"); R12search/S1-literature.md:149 (S1-05) | TRACED | a9fd9601 2026-09-12 (`:557` 00f6a737 2026-10-17) | 2026-10-09 |

### `feller-ipta50`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| E-47 | G/02:669 | `feller-ipta50` | the count standard error | `R/task-9.5-interactive-typing/changelog.md:671–676` (9.5 D86: §12.4 pp. 248–249 paraphrased, no passage, no copy); `docs/references.md:137–140` (author's read) | RECORD-BELOW-STANDARD | f30b086b 2026-10-14 | 2026-09-27 |
| F-60 | v06:1037 | `feller-ipta50` | the wake-count standard error from Feller's recurrent-event theorem | refs:137–140 — author's read only | RECORD-BELOW-STANDARD | f30b086b 2026-10-14 | 2026-09-27 |

### `feral-gamemode`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-31 | related-work.md:48 | `feral-gamemode` | "a game's request to Feral GameMode" | S2:299 (S2-19 `README.md:2`, `:23-28`) | TRACED | 0e3b627d 2026-10-17 | 2026-10-07 |
| A-53 | proposal:150 | `feral-gamemode` | request via `gamemode_request_start()`, a launcher or `gamemoderun`; whitelist "only restricts which requesters are accepted" | S2:299 (S2-19 `README.md:23-28`, `gamemoded.8.in:49-56`, `gamemode.ini:49-55`) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-07 |
| B-39 | docs/daemon/daemon-guide.md:188 | `feral-gamemode`, `tuned`, `systemd-oomd` | GameMode's reaper every 5 s; tuned dynamic tuning every 10 s, ships disabled; systemd-oomd waits out 30 s | R19/changelog.md:17–19 | TRACED | ec4105b5 2026-10-17 | 2026-10-11 |
| C-15 | vol-01:3340; vol-03:58 | Feral GameMode | "게임이 요청하거나 사용자가 `gamemoderun`으로 실행"; "허용 목록은 요청한 쪽을 거르기만 함" | R12search/S2-project-docs.md:299 (S2-19, `a74b8106`); R12changelog.md:65 (D4) | TRACED | 00f6a737 2026-10-17 | 2026-10-08 |
| F-02 | v05:396, :1131 | `feral-gamemode` | GameMode 1.8.2 `example/gamemode.ini`: `reaper_freq=5`, "The reaper thread will check every 5 seconds …" | 9.19/changelog.md:18 (precedent search P: tag 1.8.2, URL, 2026-10-11) | TRACED | f30b086b 2026-10-14 | 2026-10-11 |

### `fiedler-gaffer04`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| B-34 | docs/simulator/simulator-guide.md:136 | `fiedler-gaffer04` | "a fixed-timestep game loop catches up its simulation steps, capped, and renders once per loop" | none in a search or read record; `docs/references.md` `fiedler-gaffer04` (author's read 2026-10-06) | RECORD-BELOW-STANDARD | 5479dcab 2026-10-06 | 2026-10-06 (registry) |
| C-18 | vol-01:3059 (rest) | Fiedler "Fix Your Timestep!" (`fiedler-gaffer04`); mpv 0.37.0 (`mpv`); Chromium 152 (`chromium`) | "고정 시간 간격으로 도는 게임 loop도 … simulation step은 이렇게 따라잡고, 따라잡는 횟수에 상한을 둡니다"; "mpv는 비어 버린 audio buffer를 한 번에 다시 채우고"; "소리 장치가 없을 때 Chromium이 쓰는 가짜 audio 출력은 늦은 callback을 한 번 돌린 뒤 다음 제때 간격으로" | only `docs/references.md` entries `fiedler-gaffer04`, `mpv`, `chromium` — each "verified (2026-10-06; the files read at the tag)" / "the page read in full", the author's own read with no search record; 9.11 D3 (R11changelog.md:46) cites them back to `docs/references.md`; grep of `_dev/research/jioh/*/search` for `fake_audio_worker`, `buffer.c:198`, `fix_your_timestep` finds nothing | RECORD-BELOW-STANDARD | e4ac1624 2026-10-17 | 2026-10-06 (registry) |
| D-13 | vol-06:460 | `fiedler-gaffer04` | catching up is "고정된 시간 간격으로 도는 게임 루프가 화면은 한 번만 그리면서 시뮬레이션 단계를 따라잡는 경우" (a fixed-timestep game loop rendering once while catching up simulation steps) | none in any slice's search/read record; the only passages are the registry's own role line (`docs/references.md:577`, "accessed 2026-10-06") cited by 9.11 changelog D3 | RECORD-BELOW-STANDARD | e4ac1624 2026-10-17 | 2026-10-06 (registry only) |
| E-18 | G/02:137 | `fiedler-gaffer04` | "fixed-timestep game loop의 simulation 단계는 밀린 주기를 따라잡고" (a fixed-timestep loop's simulation steps catch up) | `docs/references.md:575–578` only (author's read 2026-10-06); cited in `R/task-9.11-scheduler-constants/changelog.md:236` without passage or copy | RECORD-BELOW-STANDARD | f30b086b 2026-10-14 | 2026-10-06 |
| F-52 | v08:1144, :1656 | `fiedler-gaffer04` | a fixed-timestep game loop's simulation steps catch up | refs:575–578 only (author's read 2026-10-06; quotes, URL, date; no search or read record) | RECORD-BELOW-STANDARD | ac67c3da 2026-10-17 | 2026-10-06 |

### `field-jrssb07`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| B-03 | docs/harness/metrics.md:262 | `field-jrssb07` | consistent "as the number of clusters grows with their size fixed"; simulations at 5 and 15 clusters of 4 "consistently underestimates …"; "we are essentially working with five and 15 observations" | R11/search/S1-literature.md:216; R11/changelog.md:373 | TRACED | e6514137 2026-10-08 | 2026-10-08 |
| B-26 | harness/experiments/rq0-gate.yaml:476–481 | Field and Welsh (`field-jrssb07`) | consistency "for balanced one-way arrays"; simulations "ran 5 and 15 clusters of equal size, where the cluster bootstrap underestimated the variance" | R11/changelog.md:373 | TRACED | 26a8320f 2026-10-09 | 2026-10-08 |

### `flautner-tsafrir`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| F-49 | v06:1400 | Flautner; Tsafrir / Etsion (9.5 S1) | "입력 하나당 CPU에 대해서는 문헌에 Linux 관찰이 있었지만 모두 2000–2004년의 100–664 MHz 기계였습니다" | 9.5/search/candidates.md:20–25 (Linux traces: 450 MHz, 300–600 MHz, 664 MHz, 2000–2006; the 100 MHz machines are Endo's Windows NT and BSD/OS) | WORDING-OUTSIDE-PASSAGE | f30b086b 2026-10-14 | 2026-09-13 |

### `gamemode-docs`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-28 | related-work.md:40 | `gamemode-docs` | Windows grants the foreground game "exclusive CPU sets and increased GPU prioritization", on by default for most games, recognition undocumented, APIs deprecated from 1809 | S2:269 (S2-16), search/V60-vol02-quotations.md:473 (portal and `ReleaseExclusiveCpuSets`), AA:334 (A4-10) | TRACED | 0e3b627d 2026-10-17 | 2026-10-07/09 |
| A-35 | proposal:34 | `gamemode-docs`, `apple-gamemode` | Windows and macOS ship a Game Mode; "how either recognises a game their documentation does not state" | S2:269 (S2-16 coverage), S2:287 (S2-18 coverage) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-07 |
| A-52 | proposal:149 | `gamemode-docs` | on by default for most games, "an optional `expandedResources` declaration", foreground and focus | S2:269 (S2-16) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-07 |
| B-40 | docs/background-guide.md:18 | `gamemode-docs`, Apple "Use Game Mode" | Game Mode gives the foreground game resources — "on Windows by default for most games, on macOS when a game goes full screen" | R12/search/S2-project-docs.md:277, :295 | TRACED | 0e3b627d 2026-10-17 | 2026-10-07 |
| B-41 | docs/background-guide.md:18 | `gamemode-docs`, Apple "Use Game Mode" | "and neither documents how it recognises a game" | R12/search/S2-project-docs.md:281 ("mechanism of recognising a game not documented on these pages"), :621 (Apple's statement only on script-rendered Developer Forums, not read) | WORDING-OUTSIDE-PASSAGE | 0e3b627d 2026-10-17 | 2026-10-07 |
| C-08 | vol-01:1361, :3280–3283, :3325–3327, :3363, :3403, :3744; vol-03:56–57; vol-04:496 | Microsoft Learn Game Mode pages, Xbox Support, Apple Support, `LSSupportsGameMode` | Windows: on by default for most games, foreground with focus, CPU cores reserved and GPU priority, Windows Update driver installs and restart notices held back, `expandedResources` per title; macOS Sonoma 14+, Apple silicon, full screen, `LSSupportsGameMode` from macOS 26; recognition undocumented | R12search/S2-project-docs.md:269 (S2-16), :287 (S2-18), :314 (S2-20), :604–608 (S2-58); V60-vol02-quotations.md:460–470; R12changelog.md:29 (D2), :709 (D45), :1433 (D94) | TRACED | 00f6a737 2026-10-17 | 2026-10-07/09 |
| C-43 | vol-02:3561–3652 (§9), :3715 | the LLM line, ASA, AKTS, ananicy, Game Mode | the landscape figure's cell placements | R12changelog.md:1274 (D83), :1714 (D116), :97 (D6) | TRACED | 00f6a737 2026-10-17 | 2026-10-09 |

### `georges-oopsla07`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| F-56 | v06:882, :916, :961 | `georges-oopsla07` | §4.3's "30 runs" an example; §6.2.1 variation across hardware platforms | refs:112–115; 9.5/changelog.md:204 — author's read only | RECORD-BELOW-STANDARD | f30b086b 2026-10-14 | 2026-09-19 |

### `gh-actions-limits`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| F-10 | v07:1065, :1254 | `gh-actions-limits` | "Each job in a workflow can run for up to 6 hours of execution time …" | 9.10/search/S4-ci-observability.md:278 | TRACED | aaec6cde 2026-10-17 | 2026-10-01 |

### `gh-artifact-retention`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| E-54 | G/01:1127; G/02:629 | `gh-artifact-retention` | GitHub deletes a workflow's artifacts after 90 days | `docs/references.md:379–382` only (author's read 2026-10-16) | RECORD-BELOW-STANDARD | d62372dc 2026-10-17 (G/01); f30b086b 2026-10-14 (G/02) | 2026-10-16 |
| F-11 | v06:1065; v07:1290 | `gh-artifact-retention` | "… retained for 90 days before they are automatically deleted" | 9.15/logs/K01.md:89 (URL, SHA-256, 2026-10-16, verbatim) | TRACED | 2c451543 / aaec6cde 2026-10-17 | 2026-10-16 |

### `gh-hosted-runners`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| E-53 | G/01:874; G/02:610 | `gh-hosted-runners`, `gh-actions-limits` | the standard Linux runner 4 vCPU, 16 GB RAM, 14 GB SSD; "Each job in a workflow can run for up to 6 hours of execution time" | 9.10 S4:231–282, :278 | TRACED | f30b086b 2026-10-14 (specs); d62372dc 2026-10-17 (6 h quote) | 2026-10-01 |
| F-08 | v05:1979; v08:1595 | `gh-hosted-runners` | the standard public-repo Linux runner is "4 vCPU, 16 GB RAM and 14 GB SSD" (in quotation marks, attributed to the GitHub page / the reference) | 9.4/search/S4-ci-observability.md:96–97 (table row "Linux \| 4 \| 16 GB \| 14 GB \| x64"); the quoted string is 9.21/changelog.md:65's paraphrase | WORDING-OUTSIDE-PASSAGE | f30b086b 2026-10-14 | 2026-09-13; 2026-10-13 |
| F-09 | v06:715; v07:1192, :1200, :1252, :1254 | `gh-hosted-runners` | processor 4, memory 16 GB, storage (SSD) 14 GB; private-repo row 2 / 8 GB / 14 GB | 9.4/search/S4-ci-observability.md:92–99; 9.10/search/S4-ci-observability.md:282 | TRACED | f30b086b 2026-10-14; v07 :1200, :1254 aaec6cde 2026-10-17 | 2026-09-13 |

### `ghost-sosp21`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-01 | related-work.md:8 | `ghost-sosp21` | "delegates kernel scheduling decisions to userspace agents … without deploying a new kernel or rebooting" | S1:76 (ghOSt pp. 1, 3, 4) | TRACED | 0e3b627d 2026-10-17 | 2026-10-07 |
| A-84 | proposal:814 | `ghost-sosp21`, `li-expcs07`, `becker-arxiv18` | "0.6–3.8 µs for the switch itself and a frequent value near 10 µs on others' machines" | S1:76 (599 ns), S1:396 (3.8 µs), S1:409 (S1-23 p. 7: "at least 3,400 cycles, with a frequent value around 30,000 cycles"); CL12:911 (D57) | WORDING-OUTSIDE-PASSAGE | 32a5c9dd 2026-10-17 | 2026-10-07/09 |
| C-29 | vol-02:852–1094 (§3.2) | ghOSt (SOSP '21) and the `ghost-userspace` README | quotations; "without deploying a new kernel or rebooting" | V60-vol02-quotations.md:123–162 (README at `9ca0a1fb`, SHA-256 given); R12search/S1-literature.md:76 (S1-01); R12changelog.md:304, :1487 (D17, D98) | TRACED | a9fd9601 2026-09-12 | 2026-10-09 |

### `glam`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| D-37 | vol-06:2647, 2766 | `glam` | "탭 다섯 개는 Firefox의 Linux 사용 통계(`glam`)에서" | 9.10 S3:634-656 (S3-40: Linux v152 `max` median 4.67 tabs; Linux median 3.4–5.0 across 137–156) | TRACED | ba94cbb5 2026-10-17 | 2026-10-01 |
| E-12 | G/02:1241; G/04:582 | `glam` | Firefox Linux telemetry, per-client maximum concurrent tabs, median 4.67, rounded to 5 | 9.10 S3:648 (`max`: p50 4.67, Linux, v152, 7,535,303 users) | TRACED | f30b086b 2026-10-14 | 2026-10-01 |
| E-13 | G/01:598; G/03:419 | `glam` | "창 하나에 tab 다섯" (five tabs in one window) / "한 브라우저 창에 탭이 다섯 개라는 것은 Firefox의 Linux telemetry(`glam`)에서" | 9.10 S3:648 (median of per-client max over all windows 4.67; windows median max 1) | WORDING-OUTSIDE-PASSAGE | f30b086b 2026-10-14 | 2026-10-01 |
| F-40 | v06:1324; v08:1120 | `glam` | Linux Firefox, median per-client peak of concurrent tabs 4.67; 7,535,303 clients | 9.10/search/S3-traces-datasets.md:648; 9.10/search/candidates.md:18 | TRACED | f30b086b 2026-10-14 | 2026-10-01 |

### `glean`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| E-42 | G/02:843 | `glean` | Thunderbird's Glean metrics-ping scheduler wakes once a day at local 04:00 | `docs/references.md:419–422` only (author's read of `scheduler.rs` at 25b0fb2, 2026-09-28); the nearest read record, 9.10 S3:644 (Glean book: "the collection is scheduled daily at 04:00"), does not state local time | RECORD-BELOW-STANDARD | f30b086b 2026-10-14 | 2026-09-28 |

### `glibc`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| E-33 | G/02:1131 | `glibc` (Ubuntu noble-security) | the 2026-07-27 update glibc 2.39-0ubuntu8.7 → 8.8, packages `libc-bin`, `libc6`, `libc6-dbg`, `locales` | 9.10 S2:3627–3630 (S2-32) | TRACED | f30b086b 2026-10-14 | 2026-10-01 |

### `gonzalez-chi04`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| E-50 | G/01:1057 | `gonzalez-chi04` | "사건 하나에 약 3분(3분 08초)", "working sphere 안에서 전환 전까지의 평균 연속 구간 11분 28초" | R10:89, :121 (Table 2, p. 116: 0:03:08 is "All events except "Formal meetings" and "Other""); K4:464–487 (11:28 covers central and peripheral spheres only) | WORDING-OUTSIDE-PASSAGE | d62372dc 2026-10-17 | 2026-09-13 |
| E-51 | G/03:603; G/04:1564 | `gonzalez-chi04` | "the mean continuous segment in a working sphere before switching, 11 min 28 s" | K4:464–487 (as E-50) | WORDING-OUTSIDE-PASSAGE | f30b086b 2026-10-14 | 2026-09-13 |
| F-26 | v06:271; v08:292, :1476 | `gonzalez-chi04` | mean continuous segment in a working sphere 11 min 28 s → 688 s | R10:74–79, :123 | TRACED | f30b086b 2026-10-14 | 2026-09-13 |
| F-27 | v08:292, :1643 | `gonzalez-chi04`, `mark-chi08`, `mark-gallup06` | ~12 min per working sphere (~10 a day) and ~3 min per event are González & Mark 2004; CHI 2008 has neither; 23:15 only in the 2006 Gallup interview | R10:74–91, :164–180, :218–224 | TRACED | f30b086b 2026-10-14 | 2026-09-13 |

### `gregg-perf`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| D-31 | vol-06:3826 | Gregg, "perf Examples" §6.7 (9.6 S3-01) | the compiler-child note's "corroborates" now "Gregg가 빌드 하나를 1초 동안 `perf sched`로 잡은 기록에 붙고, 같은 역할이 리눅스에서 같은 상대 무게를 진다는 것만 뒷받침하며 숫자는 옮기지 않습니다" | 9.6 S3:51-75 (S3-01: `perf sched record -- sleep 1`, the `perf sched latency` rows for cc1, gcc, fixdep, rm, …) | TRACED | da39802c 2026-10-17 | 2026-09-16 |

### `gstreamer`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| D-14 | vol-06:462 | GStreamer video sink (9.11 S2-17) | "GStreamer의 영상 출력 … 지금 시각이 들어 있는 frame은 바로 그리고, 그보다 앞의 frame은 버립니다" (draws the frame containing now at once, drops the frames before it) | 9.11 S2:715-722 (`gstvideosink.c:174-178` max-lateness 5 ms; `gstbasesink.c:118-129` drop only if later than max-lateness) | WORDING-OUTSIDE-PASSAGE | e4ac1624 2026-10-17 | 2026-09-24 |

### `handbrake`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| E-32 | G/02:1163, :1167 | `handbrake`; Blender Foundation; DCI | HandBrake 1.7.2's default preset "Fast 1080p30"; Big Buck Bunny 4K 30 fps, 19,036 frames; "2K" is DCI's 2048×1080 container | 9.10 S2:3879 (S2-55), :3858–3868 (S2-53), :3871–3874 (S2-54); `R/task-9.10-scenarios-timelines/changelog.md:1624` | TRACED | f30b086b 2026-10-14 | 2026-10-03 |

### `hippocamp`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| F-42 | v06:1488 | HippoCamp | the `Bei` tree, 875 files, ~40.66 GB | 9.10/search/S3-traces-datasets.md:944 (reader's own count) | TRACED | f30b086b 2026-10-14 | 2026-10-02 |

### `illumos-ts`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| B-22 | harness/experiments/rq0-gate.yaml:126 | `illumos-ts` | "illumos TS's top-level quantum" (2 ms point) | R11/search/S2-project-docs.md:484–529 (level 59 qntm 2; hz 1000 default); R11/changelog.md:185 | TRACED | 549c9ac1 2026-09-12 | 2026-09-24 |

### `interbench`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| D-01 | vol-06:540-558, 609-611, 713, 1490, 1368 | `interbench` (man page Audio, `interbench.c`) | audio "tries to run at 50ms intervals that then requires 5% cpu" quoted whole; `AUDIO_RUN (AUDIO_INTERVAL / 20)`; repo note's "wakes every 50 ms needing 5% CPU" is a summary, not the man page's words | R01:38-48 (interbench.8:81-87, interbench.c:490-492) | TRACED | ff925573 2026-09-13 | 2026-09-13 |
| D-02 | vol-06:538, 1281, 1494, 3673 | `interbench` (man page Audio) | the model "잘 만든 (소리/오디오) 프로그램이 했을 버퍼링을 무시한다" (ignores the buffering a well-made audio program would do), given in quotation marks as the manual's words | R01:41 "ignores any caching that would normally be done by well designed audio applications" | WORDING-OUTSIDE-PASSAGE | ff925573 2026-09-13 | 2026-09-13 |
| D-03 | vol-06:615-623, 1506, 3673 | `interbench` (man page Video, code) | "receive cpu 60 times per second and uses 40% cpu … quite a demanding video playback at 60fps"; code `1000000 / 60` = 16,666, `* 40 / 100` = 6,666 | R01:60-74 | TRACED | ff925573 2026-09-13 | 2026-09-13 |
| D-04 | vol-06:964-972 | `interbench` (man page X) | X "uses a variable amount of cpu ranging from 0 to 100% … a window is grabbed and then dragged" | R01:76-80 | TRACED | ff925573 2026-09-13 | 2026-09-13 |
| D-05 | vol-06:978-987 | `interbench` (`emulate_x`) | the code ramps i = 0…100, i ms run, (100 − i) ms rest; "한 바퀴가 100밀리초입니다" (one round is 100 ms); both means 50 % | R01:81-96 (each step ~100 ms; "one sweep ≈ 10.1 s wall time", `decasecond_deadlines = 100`) | WORDING-OUTSIDE-PASSAGE | ff925573 2026-09-13 | 2026-09-13 |
| D-06 | vol-06:1550-1556, 1882 | `interbench` (man page Burn) | "Burn: A configurable number of threads fully cpu bound (4 by default)" | R01:125-138 | TRACED | ff925573 2026-09-13 | 2026-09-13 |
| D-07 | vol-06:1608-1618, 1883 | `interbench` (man page Write, Read; per-block timing) | Write/Read sentences quoted; "(to avoid any caching effects)"; interbench publishes no per-block timing | R01:140-186 | TRACED | ff925573 2026-09-13 | 2026-09-13 |
| D-08 | vol-06:1937-1977, 1995, 2566-2568 | `interbench` (man page "What loads are simulated?", Gaming, Compile, Hack) | the loads list quoted; Hack runs `hackbench 50`; Gaming "uses as much cpu as it can get … only a cpu bound one"; Compile simulates "'make -j4'" by Burn+Write+Read with no forking; hackbench is tasks messaging over sockets | R01:103-124, 187-231 | TRACED | ff925573 2026-09-13 | 2026-09-13 |
| D-09 | vol-06:452-456, 464, 499 | `interbench` (`periodic_schedule`) | absolute deadline grid; a missed deadline counted, the deadline moved forward past the missed periods ("dropped frame"); re-read at `interbench.c` 398–436 | R01:48 (reading of `periodic_schedule`); 9.11 S2:644-649 (S2-15, `interbench.c:398-411`) | TRACED | ff925573 2026-09-13 (464 edited e4ac1624 2026-10-17) | 2026-09-13; 2026-09-24 |
| D-10 | vol-06:1265 | `interbench` | the model "존재하고 널리 쓰인다" (exists and is widely used) | none; R01:260-279 (author, licence, packaging in AUR, FreeBSD, Gentoo, Guix, openSUSE, Void) states no usage | NO-RECORD | ff925573 2026-09-13 | — |
| E-37 | G/02:915, :955, :1366–1369, :1405, :1656 | `interbench` | the old audio/video/X/Burn/Compile emulation models; the 50 ms "popular linux audio player" named in no release; X "a window is grabbed and then dragged across the screen"; the `-j4` labels an emulation that runs no make | K1:158, :89, :205; `R/task-9.5-interactive-typing/search/S5-kolivas-rationale.md:183, :207` | TRACED | f30b086b 2026-10-14 | 2026-09-13 / 2026-09-14 |
| E-38 | G/02:1044 | `interbench` (Burn) | "`cpu-batch`는 원래 "a process that simply computes until it is done"이라는 interbench Burn의 한 줄이었습니다" | K1:203–215 (Burn: "A configurable number of threads fully cpu bound"; "until done" is ours); the quoted phrase first appears in the repository's own `docs/data-contracts.md` at 21083b31 (2026-08-28) | WORDING-OUTSIDE-PASSAGE | f30b086b 2026-10-14 | 2026-09-13 |
| F-23 | v06:339 | `interbench` | master `e612a65c` and tag v0.31 differ in load defaults | R01:15, :31 | TRACED | f30b086b 2026-10-14 | 2026-09-13 |
| F-24 | v08:277 | `interbench` | interbench's `-j4` | R01:193 ("make -j4" is a label; Compile forks no `make`) | TRACED | f30b086b 2026-10-14 | 2026-09-13 |
| F-25 | v08:757, :820 | `interbench` | X = a window grabbed and dragged across the screen, variable CPU | R01:79 | TRACED | f30b086b 2026-10-14 | 2026-09-13 |
| F-51 | v08:1144, :1656 | `interbench`, ROS 2, Lipari & Palopoli, `rt-app`, `gstreamer` | the sources skip missed ticks by default; rt-app's "absolute" mode catches up; GStreamer's video sink drops late frames | 9.11/changelog.md:236–240; 9.11/search/S2-project-docs.md:617–642 | TRACED | ac67c3da 2026-10-17 | 2026-09-24; 2026-10-08 |

### `jadhav-arxiv25`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-21 | related-work.md:32, :34, :48 | `jadhav-arxiv25` | HPC jobs; "LLM makes the HPC job-scheduling decisions itself" | S1:326 (S1-15), AA:287 (A4-05) | TRACED | 0e3b627d 2026-10-17 | 2026-10-09 |

### `kalibera-ismm13`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| E-44 | G/02:641 | `kalibera-ismm13` | §11: "We do not show counts of fewer than 5 executions as they could hardly be used to get the variance estimate right" | `R/task-9.6-compile/changelog.md:131` (passage and §11, no copy identification); copy only in `docs/references.md:117–120` (author's read) | RECORD-BELOW-STANDARD | f30b086b 2026-10-14 | 2026-09-19 |
| F-55 | v06:869, :878, :881, :882, :891, :897, :916; v08:983, :1719 | `kalibera-ismm13` | §3 "must be done at the highest level …"; §9.3; §11 "We do not show counts of fewer than 5 executions …", "within 1%, 1.5%, 2.5% or 5%" is Table 6's columns; §12 "do not use our dimensioning results at face value" | refs:117–120; workflow:22–28; 9.6/changelog.md:131 (D24: "read in full") — author's read only | RECORD-BELOW-STANDARD | f30b086b 2026-10-14 | 2026-09-19 |

### `kgent-ebpf24`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-17 | related-work.md:32 | `kgent-ebpf24` | "Kgent synthesizes kernel extensions from natural language" | S1:503 (S1-33, abstract); CL12:369 (D22) | TRACED | 0c340f36 2026-08-27 | 2026-10-08 |
| C-36 | vol-02:2525–2608 (§6.3) | Kgent, eBPF '24 | quotations; the ablation table | V60-vol02-quotations.md (rows 2541–2597; the table finding "Human 72.5% 2.5% 25%"); R12search/S1-literature.md:303, :503 (S1-13, S1-33); R12changelog.md:369 (D22) | TRACED | 00f6a737 2026-10-17 | 2026-10-08/09 |

### `kubernetes-hpa`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| B-38 | docs/daemon/daemon-guide.md:188 | `kubernetes-hpa`, `kubernetes-cluster-autoscaler`, `ec2-autoscaling-cooldowns`, `villamizar-rfc98` | HPA 5 min stabilization; node unneeded 10 min; EC2 simple scaling "which AWS recommends against using", 300 s; RFC 2439 sample half-lives 5 / 15 min, suppression at most 15 min | R19/changelog.md:20–23; R15/logs/F1.md:120 (the AWS page as served, 2026-10-17) | TRACED | 6f508a59 2026-10-17 | 2026-10-11; 2026-10-17 |

### `lavd-ossna24`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| B-25 | harness/experiments/rq0-gate.yaml:170 | `lavd-ossna24` | per-schedule runtime understates a wake's demand "by the schedules a wake is cut into, about 1.4 on average (lavd-ossna24 s14)" | R4/search/S1-literature.md:57 (slide 14: "Preemption … takes only 25-30% of scheduling"); R4/changelog.md:66 (9.4 decision D9: "about 1.4 schedules per wake on average", from s14) | WORDING-OUTSIDE-PASSAGE | 26a8320f 2026-10-09 | 2026-09-13; 2026-09-17 |
| B-29 | docs/simulator/interpretation-contract.md:65 | `lavd-ossna24` | the frame path "from a user input to display update", "which names no intermediate stage" | R4/search/S1-literature.md:60 (slide 17); R4/search/candidates.md:73 | TRACED | ec4105b5 2026-10-17 | 2026-09-13 |
| C-32 | vol-02:1328–1386 (§4.3) | scx_lavd README; LAVD OSS NA 2024 slides | "initially motivated by gaming workloads"; mechanism; "Production Ready?" | V60-vol02-quotations.md:259–266; R12search/S2-project-docs.md:195 (S2-10); RV/reads/R02-lavd.md (copies table :5–9); R12changelog.md:168 (D10) | TRACED | cd3ba642 2026-09-12 | 2026-09-13 / 2026-10-09 |
| C-51 | vol-05:568 | LAVD OSS NA 2024 slides | "게임 workload를 분석한 발표(LAVD)가 보고한 trace의 thread 이름들" | RV/reads/R02-lavd.md:48–57 (`dxvk-cs`, `dxvk-submit`, `winepulse_*`, `wineserver`, `FAudio_AudioCli`) | TRACED | ba94cbb5 2026-10-17 | 2026-09-13 |
| D-19 | vol-06:1005, 1237, 1681-1730, 1769, 1885, 3624, 3653 | `lavd-ossna24` (slides 12, 13, 14, 16, 17) | slide 12 quoted whole (~300 tasks scheduled while running a game, ~90 % long-living, top 30–40 = 95 %, 15–20 game-specific tasks, CPU 65–95 %); slide 13 (few 100s µs to few ms; "very stable"; wineserver 260 µs, task worker 1.65 ms); slide 14 (25–30 % preemption, 70–75 % waiting syscalls); slide 17 (sequence of tasks, low 1 % FPS); 30 slides | R02:5-17 (copy, 30 slides), :24, :31, :37, :61-72, :76, :83-88; 9.4 S1:50-60 (S1-01) | TRACED | ff925573 2026-09-13 | 2026-09-13 |
| D-20 | vol-06:1237 | `lavd-ossna24` (slide 12) | "게임 하나가 task를 300개쯤 만들고" (one game creates about 300 tasks) | R02:24 slide 12 "Around 300 tasks are scheduled while running a game"; :37 "Around half of them are system tasks" | WORDING-OUTSIDE-PASSAGE | ff925573 2026-09-13 | 2026-09-13 |
| D-21 | vol-06:1108, 1126, 1247 | `lavd-ossna24` (speaker, date, slide 12) | "Min은 2024-04-17 발표에서 게임을 하는 동안 시스템 task를 포함해 약 300개의 task가 scheduling된다고 보고했다" | R02:171-174 (slide 1 "Changwoo Min … April 17, 2024"; schedule page); R02:24, :37 | TRACED | 6eebab2d 2026-10-17 | 2026-09-13 |
| D-22 | vol-06:1733-1737 | `lavd-ossna24`, `corbet-lwn24`, LWN 1051430 | "슬라이드 30장의 텍스트와 그림 속 글자 어디에도 16.7, 16.67, 60fps, frame budget이 나오지 않습니다" (no 16.7, 60fps or frame budget anywhere, image text included); slide 27 "targeted latency (e.g., 15 msec)"; slide 6 avg 41.3 FPS; the two LWN articles carry no 16.7 | R02:91-97 (slide 29 screenshot overlay "60FPS", "16.5ms", "Refresh Rate: 60"; no frame budget stated), :128 (41.3 FPS); LWN copies `sources/lwn-991205.txt`, `sources/lwn-1051430.txt` contain no "16.7" (grep, this audit) | WORDING-OUTSIDE-PASSAGE | ff925573 2026-09-13 | 2026-09-13 |
| D-23 | vol-06:1749-1751, 1863, 1889 | `lavd-ossna24` (slide 16 graph) | slide 16 shows separate loops, one of them "게임 본체와 `wineserver`가 서로 주고받는 작은 고리"; workers converge on "그래픽 제출 thread 하나"; wineserver "슬라이드 16의 그림에서 게임 본체와 계속 주고받는 고리에 있습니다" — corrected at merge: the wineserver loop is on slide 16 per 9.4 S2:91; only "그래픽 제출 thread 하나" is outside (the workers converge on `dxvk-cs`) | 9.4 S2:91 (the 9.4 gaming record's slide-16 node list: `wineserver[7256/0]`, edges `wineserver→Troy.exe epoll (134200)`, `Troy.exe→wineserver pipe_read (58134)`; four `Task worker thr` → `dxvk-cs`, then `dxvk-cs` → `dxvk-submit`); R02:43-58 omits the wineserver edges | WORDING-OUTSIDE-PASSAGE | ff925573 2026-09-13 | 2026-09-13 |
| D-24 | vol-06:1863, 3918 | `lavd-ossna24` (slide 13) | wineserver singled out as a short coordination task, 260 µs | R02:61 | TRACED | ff925573 2026-09-13 | 2026-09-13 |
| D-25 | vol-06:1983-1987 | `lavd-ossna24` (slide 10, slide 17) | slide 10 quoted: "If games have the common characteristics, which are differentiated from other general program domains (e.g., HPC, AI/ML, database), there are chance to come up with a game optimized scheduling policy."; slide 17: stable run and wait times, mostly periodic | slide 17: R02:69, 9.4 S1:60. Slide 10's sentence: no record (9.4 S1:53 records only slide 10's "We collect and analyze all scheduling activities while playing games."); present in the copy `sources/lavd-ossna24/scx-lavd-oss-na24.pypdf.txt:133-135` | NO-RECORD | ff925573 2026-09-13 | — |
| E-24 | G/01:515; G/02:689, :707–710, :1576; G/03:1035, :1715; G/04:696, :709 | `lavd-ossna24` | Min, OSS NA 2024, 2024-04-17; game and machine not named; s12 ~300 tasks, ~90 % long-living, top 30–40 take 95 %, system tasks 30–40 %, "15-20 game-specific tasks" 60–70 %; s13 "wineserver:260 usec", task worker 1.65 ms, "very stable and is predictable using its average"; s14 70–75 % from waiting system calls; s16 waker–waiter graph and names (`Troy.exe` …); s17 a chain serves one job | R02:3–17 (copy, 2026-09-13, SHA-256 `e62d69cd…`), :24–86, :106; `R/task-9.4-gaming/search/S1-literature.md:55–57`; `…/candidates.md:37, :59, :71` | TRACED | f30b086b 2026-10-14 (G/02:689 amended 166a4bd3 2026-10-17, registry notes only) | 2026-09-13 |
| E-25 | G/02:720 | `lavd-ossna24` | no slide contains 16.7 / 60 fps / frame budget; slide 27 "targeted latency (e.g., 15 msec)"; benchmark average 41.3 FPS | K2:182–190; R02:128 | TRACED | f30b086b 2026-10-14 | 2026-09-13 |
| E-27 | G/02:724 (s16 edges) | `lavd-ossna24` | slide 16: `wineserver → Troy.exe` epoll 134,200, `Troy.exe → wineserver` pipe_read 58,134; slide 11 dispatcher hub | `R/task-9.4-gaming/search/candidates.md:71, :97`; R02:55 | TRACED | f30b086b 2026-10-14 | 2026-09-13 |
| E-28 | G/04:1919 | `lavd-ossna24` s14 | "(9.4 D9; lavd-ossna24 s14, about 1.4 on average)" — a wake split into about 1.4 schedules on average | `R/task-9.4-gaming/changelog.md:66` (the 1.4 is the decision's arithmetic from s14's "Preemption … takes only 25-30% of scheduling", `sched_preempt` 28.78 %) | WORDING-OUTSIDE-PASSAGE | f30b086b 2026-10-14 | 2026-09-13 / 9.4 D9 |
| E-29 | G/02:689 | `grounding-sources.md` on LAVD | "`docs/workload/grounding-sources.md`는 gaming scheduling이 실제 문제라는 근거로 "Valve ships it"를 적음" | `docs/workload/grounding-sources.md:30` now: "Valve sponsors LAVD and ships it in SteamOS 3.8 as a scheduler the user selects, not enabled by default (`steamos-lavd`)"; K2:274–285 (old "Valve ships it" MISATTRIBUTED); `R/task-9.12-related-work-prose/changelog.md:152` (9.12 D9) | WORDING-OUTSIDE-PASSAGE | f30b086b 2026-10-14 | 2026-10-08 |
| F-07 | v05:1474; v07:1564; v08:1128, :1678 | `lavd-ossna24:s16` | the game chain's member names are the names on LAVD slide 16 (`Troy.exe` …) | 9.4/search/S2-project-docs.md:91 (slide 16 node list, image SHA-256) | TRACED | f30b086b 2026-10-14; v07 aaec6cde 2026-10-17 | 2026-09-13 |
| F-14 | v06:68; v08:746 | `lavd-ossna24` | "30장의 슬라이드를 텍스트와 그림까지 다 확인해 보니 16.7, 16.67, 60 fps, "frame budget"이라는 말이 어디에도 없었습니다" / "30장의 슬라이드 어디에도 16.7, 60 fps, "frame budget"이 없었습니다" | R02:93–97 (slide 29 screenshot overlay "60FPS", "16.5ms"; "Refresh Rate: 60") | WORDING-OUTSIDE-PASSAGE | f30b086b 2026-10-14 | 2026-09-13 |
| F-15 | v06:164, :516; v08:936, :1645 | `lavd-ossna24`, `steamos-refresh` | no frame budget on the slides, only slide 27's "targeted latency (e.g., 15 msec)"; Steam Deck LCD default refresh 60 Hz (SteamOS 3.2 note) | R02:92–97; 9.4/search/S2-project-docs.md:157–; 9.4/search/candidates.md:51 | TRACED | f30b086b 2026-10-14 | 2026-09-13 |
| F-16 | v06:539 | `lavd-ossna24` | "슬라이드 12장은 wine을 시스템 task로 분류하고, 16장의 그래프는 wineserver를 중심으로 한 구조를 보입니다" | 9.4/search/S2-project-docs.md:91 (slide 16: wineserver linked to `Troy.exe` and `explorer.exe` only), :92 (slide 11: the hub around `wineserver[5789/0]`); K2:24; R02:37 | WORDING-OUTSIDE-PASSAGE | f30b086b 2026-10-14 | 2026-09-13 |
| F-17 | v06:525, :539, :1389 | `lavd-ossna24:s13` | wineserver 260 µs per schedule (slide 13) | R02:61 | TRACED | f30b086b 2026-10-14 | 2026-09-13 |
| F-18 | v06:369, :1380; v08:934 | `lavd-ossna24` | slides 12–17's figures come from at least three process trees (`Troy.exe` tgid 7781, `GameThread`+`redDispatcher1–7` tgid 6340, `Umask: 0022` tgid 4727); collected with `perf sched record`; LPC 2024 reuses the figures; Pixel 8 Angry Birds; scx issues #234 / #296 logs | 9.4/search/S2-project-docs.md:91–98, :118; 9.4/search/candidates.md:11–15 | TRACED | f30b086b 2026-10-14; v08:934 166a4bd3 2026-10-17 | 2026-09-13 |
| F-19 | v08:226 | LAVD (LWN report) | "LAVD(Igalia의 Changwoo Min이 SteamOS·Steam Deck을 위해 만든 Linux scheduler)" | 9.12/search/S2-project-docs.md:241–246 (LWN 1051430: "developing LAVD as part of his work at Igalia on SteamOS and the Steam Deck"); R02:156 | TRACED | 556f188e 2026-10-17 | 2026-10-07 |
| F-20 | v08:259 | `lavd-ossna24` (via the 2026-08 archive) | "LAVD gaming: ~300 tasks at 65–95% of a many-core machine" (quoted from the archive) | R02:24, :119–121 (slide 12: ~300 tasks, utilization 65–95 %); R02:17 (no slide names the trace machine) | WORDING-OUTSIDE-PASSAGE | f30b086b 2026-10-14 | 2026-09-13 |
| F-21 | v08:264 | `lavd-ossna24:s12` | "top 30–40 tasks = 95% of scheduling" | R02:37, :100 | TRACED | f30b086b 2026-10-14 | 2026-09-13 |

### `li-expcs07`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-41 | proposal:111, :422 | `li-expcs07` | 4.2–8.7 µs in L2, 38.6–203.2 µs beyond, "up to 1 496 µs with a 128-byte stride"; cost depends on cache fit and access pattern | S1:396 (S1-21), AA:417 (A5-08) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-09 |
| B-47 | docs/background-guide.md:120 | Li, Ding & Shen (ExpCS 2007) | a context switch costs cache state, "nothing visible while the data fit in the cache, up to hundreds of microseconds or more when they do not" | R12/changelog.md:1425–1427 (9.12 decision D93), :915 (D57); R12/search/S1-literature.md:396 | TRACED | 0e3b627d 2026-10-17 | 2026-10-09 |

### `linux-sched-bwc`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| B-17 | docs/recognition-vocabulary.md:70 | `linux-sched-bwc` | "a per-class CPU bandwidth ceiling (`linux-sched-bwc`, existence only); the range, the floor, and the class rule below are ours" | R11/search/S2-project-docs.md:302–312 ("maximum CPU bandwidth available to a group or hierarchy"; "a task group"; "threads in the cgroup") | WORDING-OUTSIDE-PASSAGE | f150046e 2026-09-11 | 2026-09-24 |
| C-19 | vol-01:3228 | Linux CFS bandwidth control | "batch class … 상한이 이 기능과 개념적으로 같습니다 … 상한의 범위나 class를 판별하는 규칙은 이 연구가 정한 것" | R11search/S2-project-docs.md:296 (S2-03, `sched-bwc.rst`); the range and class rule labelled design | TRACED (existence) + LABELLED (design) | e247d94a 2026-09-12 | 2026-09-24 |

### `linux-sched-cfs`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-36 | proposal:79 | `linux-sched-cfs` | "Each CPU runs one task at a time" | AA:380 (A5-02, `sched-design-CFS.rst:26–27`) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-09 |

### `linux-sched-core`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| E-07 | G/02:1325 | Linux kernel (`core.c`) | under the idle policy nice 19 is ignored | `R/task-9.11-scheduler-constants/search/S2-project-docs.md:463–464` (`task_has_idle_policy(p)` → `WEIGHT_IDLEPRIO`, else `sched_prio_to_weight[prio]`, v7.2) | TRACED | f30b086b 2026-10-14 | 2026-09-24 |
| F-54 | v08:1027, :1722 | Linux `kernel/sched/core.c` v6.17 | `sched_waking` fires only for a sleeping thread, before the scheduler takes it off the CPU | 9.7/changelog.md:115 (file, function, version; no verbatim passage, no copy date or hash) | RECORD-BELOW-STANDARD | f30b086b 2026-10-14 | 2026-09-19 |

### `linux-sched-deadline`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-73 | proposal:430 | `linux-sched-deadline`, `man-sched` | `SCHED_DEADLINE` "EDF with a Constant Bandwidth Server"; `SCHED_FIFO` "without time slicing" | S2:118 (`sched-deadline.rst:41-44`), S2:144 (sched(7)) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-07 |

### `linux-sched-eevdf`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-38 | proposal:89 | `linux-sched-eevdf`, `man-sched`, `apple-qos`, `ostep`, `win-priority-boosts`, `xnu-sched` | what each scheduler acts on: fair share, declarations, requested slice, demotion, boosts, "XNU's usage decay" | S2:96, S2:144, S2:563, S2:569 (S2-54), AA:324 | TRACED | 32a5c9dd 2026-10-17 | 2026-10-07/08 |
| A-43 | proposal:113 | `linux-sched-eevdf` | earliest virtual deadline; shorter slice runs sooner; slice requested through `sched_setattr()` | S2:96 (`sched-eevdf.rst:13-22`, `:30-32`) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-07 |
| A-46 | proposal:430, :117 | `linux-sched-eevdf` | ":430 `SCHED_OTHER` EEVDF since Linux 6.6, a deterministic proportional-share algorithm (`linux-sched-eevdf`)"; ":117 Linux's default is EEVDF, proportional share (`linux-sched-eevdf`)" | S2:96 (S2-03); S1:149 (S1-05 title); CL12:442 (D26) | WORDING-OUTSIDE-PASSAGE | 32a5c9dd 2026-10-17 | 2026-10-07 |

### `linux-sched-ext`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| B-18 | docs/recognition-vocabulary.md:70; harness/guards/guard-spec.yaml:51–62, :150–154; harness/experiments/rq0-gate.yaml:321; docs/terminology.md:144; docs/harness/harness-and-records-guide.md:1279 | `linux-sched-ext` | starvation floor 30 s, design: the bound sched_ext's watchdog enforces "at most and by default"; `timeout_ms` "may not exceed the default timeout of 30 seconds"; a stalled task ejects the BPF scheduler; covers idle-class tasks | R11/changelog.md:112 (9.11 decision D7), :266 (D19); R11/search/S2-project-docs.md:269–294; R11/changelog.md:87 (D5, idle tasks under sched_ext) | TRACED | 137ee257 2026-10-08; 26a8320f 2026-10-09; 0e3b627d 2026-10-17; b8475b7d 2026-10-17 | 2026-10-08 |
| B-23 | harness/experiments/rq0-gate.yaml:130 | `linux-sched-ext` | "sched_ext's default slice, 20 ms" | R11/search/S2-project-docs.md:249; R11/changelog.md:185 | TRACED | 26a8320f 2026-10-09 | 2026-10-07 |

### `linux-sched-fair`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-63 | proposal:243, :844 | `linux-sched-fair` | "Linux's base slice 0.70 ms × (1 + log₂ of the online CPUs, counted up to 8) since v6.15, 2.1 ms on the runner's four CPUs" | S2-11s:192 (`fair.c` `700000ULL`), S2-11s:68 (`1 + ilog(ncpus)`); CL11:27–31 (D2, the tags and `update_sysctl()`) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-07 |
| B-21 | harness/experiments/rq0-gate.yaml:123 | `linux-sched-fair` | "Linux's base slice at one CPU, 0.70 ms since v6.15 … design, the one-CPU value for the simulator's one lane" | R11/changelog.md:27 (9.11 decision D2: `700000ULL` at v6.15, v6.17, v7.0), :339–345 (D25: every tag v6.6–v7.2) | TRACED | 26a8320f 2026-10-09 | 2026-10-08 |
| B-37 | docs/daemon/daemon-guide.md:188 | `linux-sched-fair`, `linux-cpufreq`, `android-cpufreq-interactive` | load balancer cache-hot "a task that last ran within 0.5 ms"; schedutil `rate_limit_us` 1 ms without driver latency; ondemand "of the order of 2 ms"; Android `interactive` at least 80 ms before ramping down | R19/changelog.md:11–15 (precedent search, 2026-10-11); R15/logs/F1.md:119 (re-read at v7.0, 2026-10-17) | TRACED | 6f508a59 2026-10-17 | 2026-10-11; 2026-10-17 |
| C-28 | vol-02:794–811 (§2.8) | Linux `fair.c` (CFS v6.5, EEVDF v6.6–v7.0), `ext.h`, illumos `ts_dptbl.c` | "목표 지연이 6밀리초, 최소 단위가 0.75밀리초 … 코어 수에 따라 늘어난다"; base slice "v6.6부터 v6.14까지 0.75밀리초, v6.15부터 0.70밀리초 … 1 + log₂(온라인 CPU 수, 8까지 셈)배"; sched_ext slice 20 ms; illumos 60 levels, 2–20 ms, once-per-second update | R11search/S2-project-docs.md:45–160 (S2-01, `fair.c:59–107@v6.5`, `:205–233@v6.6`), :238 (S2-02), :480 (S2-08); R11changelog.md:23, :339 (9.11 D2, D25, the base slice at one CPU) | TRACED (the runner's 2.1 ms is a `meas-ci` value, skipped) | 00f6a737 2026-10-17 | 2026-09-24 / 2026-10-07 |
| F-05 | v05:1125–1137 | cpufreq docs, Android `cpufreq_interactive.c`, `fair.c`, Microsoft Learn, Kubernetes, AWS, RFC 2439 | the precedent table: schedutil 1.5× transition latency or 1 ms; ondemand ~2 ms; interactive 80 ms; migration cost 0.5 ms; Windows no published default; HPA 300 s; cluster autoscaler 10 min; AWS 300 s; RFC 2439 5–15 min | 9.19/changelog.md:11–16, :20–23 | TRACED | f30b086b 2026-10-14 | 2026-10-11 |

### `linux-sched-h`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| E-14 | G/01:444; G/03:131, :469, :1918, :2069 | `linux-sched-h` | `comm` is `TASK_COMM_LEN` 16 bytes including the terminating NUL, so at most 15 visible characters | R11:1105–1113 (man-pages 6.19 `proc_pid_stat.5`: "Strings longer than TASK_COMM_LEN (16) characters (including the terminating null byte) are silently truncated"; the man page names `include/linux/sched.h`, R11:779) | TRACED | f30b086b 2026-10-14 | 2026-09-13 |
| F-01 | v05:312, :394; v07:1016, :1566 | `linux-sched-h` | `TASK_COMM_LEN = 16`, NUL included, so 15 characters; read at v6.17 | 9.10/search/S4-ci-observability.md:1499–1500 (v6.17 `sched.h:320`); 9.10/search/S2-project-docs.md:1722–1745 (v6.8, v7.0) | TRACED | f30b086b 2026-10-14; v07 aaec6cde 2026-10-17 | 2026-10-01 |

### `liu-jacm73`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-85 | proposal:820 | `liu-jacm73`, `man-sched-setattr` | EDF priority by current request's deadline (p. 55); schedules every set any algorithm can (p. 58); utilisation ≤ 1 (Theorem 7, p. 56); above 1 none (p. 56); `SCHED_DEADLINE` via `sched_setattr(2)` | AA:123 (A2-10), S2:549 (S2-51) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-09 |
| B-16 | docs/recognition-vocabulary.md:120 | `liu-jacm73` | "Liu and Layland's EDF is preemptive and priority-driven with no quantum" | R11/changelog.md:318 (9.11 decision D23: "are pre-emptive and priority driven ones", p. 48); R12/search/S1-literature.md:234–244 | TRACED | 07b736d6 2026-10-08 | 2026-10-08 |
| C-22 | vol-02:429–476 (§2.3) | Liu & Layland 1973 | quotations; optimality with its conditions | V60-vol02-quotations.md:67–74; R12search/S1-literature.md:232 (S1-10); R12changelog.md:593, :1069 (D37, D68) | TRACED | a9fd9601 2026-09-12 | 2026-10-09 |
| E-19 | G/02:133, :340; G/03:1661 | `liu-jacm73` | period-implicit deadline: "each task must be completed before the next request for it occurs" | `R/task-9.12-related-work-prose/search/S1-literature.md:237` (p. 48, (A2)); `…/V60-vol02-quotations.md:71` | TRACED | f30b086b 2026-10-14 | 2026-10-08 |

### `llamacpp`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-74 | proposal:496 | `llamacpp`, `ollama-docs`, `vllm-docs` | local servers; grammar-constrained decoding, `eos` implies completion; unread keywords "ignored without notice", unsupported `pattern` accepted as any string with a log warning, some constructs fail | S2:404, :410, :416 (S2-33…35), S2:610 (S2-59), AA:172 (A2-22); CL12:1183 (D77) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-07/09 |

### `localscore`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-66 | proposal:267 | `localscore`, `artificialanalysis` | LocalScore 0.88 s average TTFT, RTX 3060 12 GB, mean of runs of nine tests; Artificial Analysis "72-hour medians", 0.66–1.14 s | AA:166 (A2-21) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-07/09 |

### `lu-lpc25`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-06 | related-work.md:8, :12 | `lu-lpc25` | "to the entire Reality Labs GPU fleet with tens of thousands of GPUs" | S2:211 (LPC 2025 contribution 2039) | TRACED | 0e3b627d 2026-10-17 | 2026-10-07 |

### `lumos-mlsys25`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-23 | related-work.md:32 | `lumos-mlsys25` | `latency_ns`, `min_granularity_ns`, PostgreSQL p99, "5.0 % and 7.1 % below Bayesian optimisation" | AA:150 (A2-17, pp. 2–3; a draft-watermarked copy) | TRACED | 0e3b627d 2026-10-17 | 2026-10-09 |

### `mahoney-10gb`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| F-43 | v06:822, :1444 | Mahoney's 10 GB set; Valve download statistics | 79,431 files; byte-weighted median of per-country rates 121.0 Mbps | 9.7/search/T9-S2-project-docs.md:337–339; 9.7/changelog.md:61 (data file and version; the median is our arithmetic) | TRACED | f30b086b 2026-10-14 | 2026-09-19 |

### `man-proc`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| B-45 | docs/background-guide.md:20 | proc_pid_stat(5) | `tracker-miner-f` — "the 15-character name the kernel shows" | R4/search/S4-ci-observability.md:284 ("Strings longer than TASK_COMM_LEN (16) characters (including the terminating null byte) are silently truncated") | TRACED | 0e3b627d 2026-10-17 | 2026-09-13 |

### `man-sched`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-10 | related-work.md:16 | `man-sched`, `apple-qos`, `win-priority-boosts`, `gamemode-docs`, `apple-gamemode` | declared class / nice / unit; macOS QoS; "Windows' foreground and input boosts"; Game Mode's foreground or full-screen game | AA:324 (A4-09), AA:334 (A4-10), AA:340 (A4-11), AA:346 (A4-12) | TRACED | 0e3b627d 2026-10-17 | 2026-10-09 |
| A-48 | proposal:145 | `man-sched`, `man-sched-setattr` | policies incl. `SCHED_EXT` since 6.12; declared via program, unit or `chrt`; `RLIMIT_RTPRIO`; `SCHED_DEADLINE` needs `CAP_SYS_NICE` | S2:144 (S2-07), S2:549 (S2-51), S2:511 (S2-47); CL12:434 (D26) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-07/08 |
| B-42 | docs/background-guide.md:18 | sched(7), Apple QoS docs | Linux policy, nice and I/O class declared "by the program itself, its installed unit or a wrapper"; macOS "a QoS class by the developer in code" | R12/changelog.md:434–444 (9.12 decision D26), :460–466 (D28); R12/search/S2-project-docs.md:144, :323, :563 | TRACED | 0e3b627d 2026-10-17 | 2026-10-08 |
| C-09 | vol-01:2094 | Linux, macOS declarations | "scheduling class와 nice 값을 프로그램 자신이 정하거나, … systemd unit 파일에 적거나, … wrapper(`chrt` 같은 명령)가 정합니다 … macOS에는 QoS class … 개발자가 코드에서" | R12changelog.md:225 (9.12 D13, who declares: S3-02, 9.11 S2-27, S2-21) | TRACED | 00f6a737 2026-10-17 | 2026-10-08 |

### `maricq-osdi18`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| E-43 | G/02:633 | `maricq-osdi18` | "servers with supposedly identical parts" differ run to run | `docs/references.md:122–125` only (author's read 2026-09-19); `R/task-9.6-compile/changelog.md:131` paraphrases without the passage | RECORD-BELOW-STANDARD | f30b086b 2026-10-14 | 2026-09-19 |
| F-57 | v06:877, :958, :1686 | `maricq-osdi18` | §2 "nonparametric intervals of the median 'unless normality can be demonstrated'"; many VMs, many times | refs:122–125 — author's read only | RECORD-BELOW-STANDARD | f30b086b 2026-10-14 | 2026-09-19 |

### `miller-fjcc68`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-39 | proposal:111 | `miller-fjcc68` | keystroke echo 0.1–0.2 s, a control's response 0.1 s, "best calculated guesses" | AA:87 (A2-01, p. 271) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-09 |
| B-06 | docs/harness/metrics.md:292, :299 | `miller-fjcc68` | Topic 1: "Time delay: No more than 0.1 second"; echo "no more than 0.1 to 0.2 seconds"; "far too slow for skilled keyboard users"; "best calculated guesses"; "indicative rather than conclusive"; no subjects, no source for 0.1 s | R11/search/S1-literature.md:59–62, :69; R11/changelog.md:330 (9.11 decision D24) | TRACED | 99257433 2026-10-08 | 2026-10-08 |
| B-51 | docs/harness/harness-and-records-guide.md:1123 | `miller-fjcc68`, `deber-chi15` | (Korean) 0.1 s the strict end of Miller's 0.1–0.2 s echo guideline, cross-checked against Deber et al.'s measured detection threshold | R11/search/S1-literature.md:62, :245–246; R11/changelog.md:330 | TRACED | b8475b7d 2026-10-17 | 2026-10-08 |
| C-01 | vol-01:818, :820; vol-02:720 box; vol-03:3157 | Miller 1968, Nielsen 1993, Deber et al. 2015 | "Miller가 1968년에 키 입력의 화면 반응을 \"0.1~0.2초 이내\"로 권했고 … \"저자가 계산해 낸 최선의 추측\""; Nielsen "Miller와 Card 등을 인용해 다시 적은 것"; Deber "69밀리초 … 96밀리초(tapping 세션 12번)" | R11search/S1-literature.md:53 (S1-01 Miller, p. 271), :140 (S1-05 Nielsen excerpt), :239–246 (S1-11 Deber, pp. 1830–1831: "24 sessions … (12 drag and 12 tap)", "69 ms and 96 ms"); R11changelog.md:5, :326 (9.11 D1, D24, the interaction threshold) | TRACED | 00f6a737 2026-10-17 | 2026-09-24 (re-read 2026-10-07) |
| C-25 | vol-02:665–724 (§2.6) | Miller, Nielsen excerpt, Shneiderman reporting Long 1976 | quotations; "열일곱 가지 주제로 나누고(269쪽 …)"; Long "approximately 0.1–0.5 second" as Shneiderman's report | V60-vol02-quotations.md:107–122; R11search/S1-literature.md:53, :140, :173–187 (S1-01, S1-05, S1-07) | TRACED | a9fd9601 2026-09-12 (`:673` 00f6a737 2026-10-17) | 2026-09-24 / 2026-10-09 |

### `mozilla-testpilot10`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| D-33 | vol-06:2669-2679, 2698, 2761, 1233 | `mozilla-testpilot10`, `singervine-slate10` | ~27,000 Firefox users, one week; Slate: half above 2.38 average tabs, a quarter ≥ 3.59, mean of averages 3.2, 1,103 max; half maxed below 8, a quarter ≥ 11; the aggregated-data page holds only file lists and column descriptions | R09:11-14, :126-137, :212-237 | TRACED | ff925573 2026-09-13 | 2026-09-13 |

### `mpv`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| B-31 | docs/simulator/simulator-guide.md:136 | `mpv` | "mpv drops late video frames by default" | R11/search/S2-project-docs.md:698–712 (`options.rst:1248–1265`, `vo.c:955–963`) | TRACED | 5479dcab 2026-10-06 | 2026-09-24 |
| B-32 | docs/simulator/simulator-guide.md:136 | `mpv` | "its audio output refills a drained buffer in one write" | none in a search or read record; only `docs/references.md` `mpv` (author's read 2026-10-06, `buffer.c` locators) | RECORD-BELOW-STANDARD | 5479dcab 2026-10-06 | 2026-10-06 (registry) |
| B-35 | docs/simulator/simulator-guide.md:136 | `mpv`, `chromium`, `vulkan`, `fiedler-gaffer04` together | "none of them replays late iterations" | R11/changelog.md:236 (9.11 decision D17: "rt-app's 'absolute' mode and a fixed-timestep loop's simulation steps catch up"); `docs/references.md` `fiedler-gaffer04` ("more steps to catch up") | WORDING-OUTSIDE-PASSAGE | 5479dcab 2026-10-06 | 2026-10-08 |
| E-39 | G/02:915 | `mpv` | `--ao=null` "simulates timing of a perfect audio device" | `R/task-9.5-interactive-typing/search/S4-ci-observability.md:206–210` | TRACED | f30b086b 2026-10-14 | 2026-09-14 |

### `nielsen-ue93`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| B-07 | docs/harness/metrics.md:299 | `nielsen-ue93` | "0.1 second is about the limit …", citing Miller 1968 and Card et al. 1991 | R11/search/S1-literature.md:145–146 | TRACED | 1029f6eb 2026-09-08 | 2026-09-24 |
| C-26 | vol-02:697 | Nielsen 1993 | "인터페이스 설계 쪽에서 이 값이 널리 알려진 것은 이 책 덕분입니다" | none (S1-05 at R11search/S1-literature.md:140 records the excerpt's text, not its influence) | NO-RECORD | cd3ba642 2026-09-12 | — |

### `numpy-r-quantile`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| B-05 | docs/harness/metrics.md:264 | numpy, R (software, no registry id) | percentile position `(n − 1)·p/100` "(numpy's `linear` method, R's type 7)", labelled a convention | none (R11/changelog.md:187, 9.11 decision D13, labels the rule; no passage from numpy or R) | NO-RECORD | 2cbf1715 2026-09-11 | — |

### `obs-studio`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-60 | proposal:160, :176, :185 | `obs-studio`, `obs-kb-encoding` | OBS records and streams, encoding as it goes; "an encoder that falls behind skips frames, which OBS counts and reports"; "Skipped frames due to encoding lag" | S2:583 (S2-55), AA:107 (A2-06); CL12:554 (D34, locale `:58`, `:271`) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-09 |

### `ocallahan-atc17`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| D-28 | vol-06:3185-3207, 3221, 3252-3255, 3506-3508, 3527-3530, 3540, 3826 | `ocallahan-atc17` | O'Callahan and five co-authors; §4.3 paragraph quoted ("make forks and execs 2430 processes, mostly short-lived", sambatest 89, at least 80 system calls); §4.1 "make builds DynamoRio [8] (version 6.1.0) with make -j8"; Dell XPS15 machine; §4.1/§4.3 on proceedings p. 383; no lifetime distribution | R03:9-10 (copies), :36-62, :66-72, :79-89 | TRACED | ff925573 2026-09-13 | 2026-09-13 |
| D-29 | vol-06:3207 | `ocallahan-atc17` (copy described) | "확장판 기술 보고서(arXiv:1705.05937, 21쪽)" (extended report, 21 pages) | R03:10 ("arXiv 1705.05937, only version v1, 16 May 2017; 20 pages") | WORDING-OUTSIDE-PASSAGE | ff925573 2026-09-13 | 2026-09-13 |
| E-34 | G/02:995, :1394; G/02:955 | `ocallahan-atc17` | "make forks and execs 2430 processes, mostly short-lived" (§4.3) is a `make -j8` build of DynamoRio 6.1.0 (§4.1), on a Dell XPS15 8-thread laptop | K1:542–550; `R/task-9.6-compile/search/S1-literature.md:75, :101` | TRACED | f30b086b 2026-10-14 | 2026-09-13 / 2026-09-17 |
| F-12 | v06:62–66, :195, :337, :515; v08:745, :1644 | `ocallahan-atc17` | "make builds DynamoRio [8] (version 6.1.0) with make -j8 …" (§4.1); "make forks and execs 2430 processes …" (§4.3 "Observations"; the workload description is in §4.1 "Workloads") | R03:36–58, :76–85 | TRACED | f30b086b 2026-10-14 | 2026-09-13 |

### `ostep`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-11 | related-work.md:16 | `ostep`, `corbato-sjcc62` | "MLFQ classifies tasks by how they use the CPU" | S1:101 (OSTEP ch. 8 p. 2), S1:135 (Corbató printed p. 342 item 5) | TRACED | 0e3b627d 2026-10-17 | 2026-10-07 |
| A-37 | proposal:87 | `ostep` ch. 7 | SJF / STCF optimality and their conditions (§7.4–§7.6); "A general-purpose OS usually knows little" (§7.9) | S1:121 (S1-03 pp. 2, 5, 6); CL12:525 (D32, §7.9 p. 10 verbatim, same copy) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-07/09 |
| A-42 | proposal:113, :846 | `ostep` §8.5, `corbato-sjcc62` | 10 ms or less at the top, hundreds of ms at the bottom; Solaris 20 ms to a few hundred as OSTEP describes; "CTSS's 2^ℓ quanta at level ℓ" | S1:101 (pp. 8–9), S1:135 (printed p. 341) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-07 |
| A-47 | proposal:119–121 | `ostep` | Rule 4 (allotment across sleeps), Rule 4b gameable, Rule 5 boost against starvation | AA:392 (A5-04, pp. 3, 6, 8) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-09 |
| B-11 | docs/harness/metrics.md:284; docs/recognition-vocabulary.md:106; harness/experiments/rq0-gate.yaml:28–30, :121; harness/boot-defaults/README.md:9; docs/harness/harness-and-records-guide.md:633, :792 | `ostep` (ch. 8) | the boot default is "the values OSTEP chapter 8's worked examples use — three queues and a 10 ms top slice (Example 1), doubling per level (Figure 8.6), a 100 ms boost (Figure 8.4)" | R11/search/S1-literature.md:82, :86, :91; R11/changelog.md:119–124 (9.11 decision D8) | TRACED | 3795a43a 2026-10-07; 26a8320f 2026-10-09; a64e0808 2026-10-08 | 2026-10-07 |
| B-12 | docs/recognition-vocabulary.md:110–113 | `ostep` | table rows: "a three-queue scheduler"; Figs 8.2–8.6 Q2–Q0, Fig. 8.1 eight; "with a time slice of 10 ms (and with the allotment set equal to the time slice)"; Fig. 8.6 10/20/40 ms; "a priority boost every 100 ms (which is likely too small …)"; S a voo-doo constant after Ousterhout | R11/search/S1-literature.md:78, :82, :86, :87, :91 | TRACED | 3795a43a 2026-10-07; 6fa68caa 2026-09-11 | 2026-09-24 (re-read 2026-10-07) |
| B-13 | docs/recognition-vocabulary.md:117 | `ostep` | Rule 4 demotes once a job "uses up its time allotment at a given level"; "Figure 8.6 gives the top two levels two slices each" | R11/search/S1-literature.md:89, :91 | TRACED | 6fa68caa 2026-09-11 | 2026-09-24 |
| B-46 | docs/background-guide.md:112–114 | `ostep` | uses up its allotment "counted across every sleep" → demoted (Rule 4); gives up CPU early → stays, CPU still counted; boost → Rule 5 | R11/search/S1-literature.md:85, :89; R12/changelog.md:1350–1356 (9.12 decision D87) | TRACED | 0e3b627d 2026-10-17 | 2026-10-09 |
| B-48 | docs/background-guide.md:219 | `ostep`, `corbato-sjcc62`, Microsoft Learn, Apple XNU doc, `sched-eevdf.rst` | MLFQ the textbook form (OSTEP ch. 8; Corbató 1962); "Windows' priority boosts and decay are an MLFQ form, macOS's Clutch/Edge scheduler runs EDF over QoS buckets with usage-decayed priority per thread, and Linux's default, EEVDF, is a proportional-share algorithm" | R12/changelog.md:471–480 (9.12 decision D29, record S2-54), :314–322 (D18) | TRACED | 0e3b627d 2026-10-17 | 2026-10-08 |
| C-02 | vol-01:834, :2335, :2357; vol-03:2271; vol-04:231, :252, :1721 | OSTEP ch. 8 | queues three and 10 ms "Example 1(4쪽)", doubling "Figure 8.6(9쪽)", boost 100 ms "Figure 8.4(6–7쪽)"; allotment = slice per Example 1, Fig. 8.6 two slices at the top two levels | R11search/S1-literature.md:73–91 (S1-02, pp. 3–9, version 1.10, SHA-256 `96241b4e…`); R11changelog.md:119 (9.11 D8, the boot default's OSTEP grounding) | TRACED | 00f6a737 / ba94cbb5 2026-10-17 | 2026-09-24 |
| C-03 | vol-01:2329, :2564 | OSTEP ch. 8 | "voo-doo constant … 원래 이 표현을 쓴 사람의 말을 인용하면서 … 경험과 시행착오로 정한다" | R11search/S1-literature.md:87 (p. 7, Ousterhout, "black magic"), :90 (p. 8, "only some experience with workloads and subsequent tuning") | TRACED | e247d94a 2026-09-12 | 2026-09-24 |
| C-13 | vol-01:2162, :2560, :3336–3337, :3343, :3364 | Microsoft Learn "Scheduling Priorities"/"Priority Boosts"; XNU doc; OSTEP p. 10 | Windows "priority 단계 위의 Round Robin, … boost와 감쇠. MLFQ의 한 형태"; macOS "QoS bucket 사이는 EDF, thread group 사이는 FreeBSD ULE의 변형, thread 사이는 사용량만큼 깎이는 priority"; Linux EEVDF | R12search/S2-project-docs.md:569–581 (S2-54); R11search/S1-literature.md:93 (OSTEP §8.6); R12changelog.md:471 (D29, MLFQ as the baseline) | TRACED | 00f6a737 2026-10-17 | 2026-10-08 |
| C-27 | vol-02:725–793 (§2.7) | OSTEP ch. 8 | the boot default's values from three examples; the textbook's own caveats | as C-02, C-03 | TRACED | 00f6a737 2026-10-17 | 2026-09-24 |

### `pcmark10`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| C-41 | vol-02:3358–3484 (§8.4) | PCMark 10 Technical Guide (2021-02-11); SYSmark 30 User Guide v1.2; Procyon overview page | quotations; scenario and program lists; Procyon "열 개 … 넷이 인공지능 작업 … 하나는 Android" | V60-vol02-quotations.md:454, :507 (exact) and its "seen in passing" ten-benchmark note; RV/reads/R05-vendor-benchmarks.md; `docs/references.md` `procyon` status (re-read 2026-10-09, V60) | TRACED | a9fd9601 / 00f6a737 | 2026-09-12/13, 2026-10-09 |
| C-42 | vol-02:3448, :3486, :3532 | PCMark 10 (UL), SYSmark 30 (BAPCo), Procyon (UL) | "앞의 것과 같은 제조사가 내는 다른 모음" (after the SYSmark section); "**세 제조사가 독립적으로 같은 프로그램 목록에 도달했습니다.** … 업계의 합의가 있다는 뜻" | R05 and the registry: Procyon is UL's (`docs/references.md` `procyon` cite "UL Solutions"), the same maker as PCMark 10; PCMark 10's named programs are "Chromium web browser • Firefox web browser • LibreOffice Writer … GIMP" (vol-02's own quote, V60 exact), not Office/Adobe; no record on independence | WORDING-OUTSIDE-PASSAGE | a9fd9601 2026-09-12 | 2026-09-13 |

### `proton`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| D-39 | vol-06:2366 | Proton README (9.4 S4) | "Proton은 Steam 클라이언트 아래에서만 돕니다" (Proton runs only under the Steam client) | 9.4 S4:262 ("Proton is a tool for use with the Steam client"; "Most users should use Proton provided by the Steam Client itself."), :357 (README documents only Steam-client installation; no run-requirements paragraph) | WORDING-OUTSIDE-PASSAGE | ba94cbb5 2026-10-17 | 2026-09-13 |
| F-48 | v06:1318 | Proton README | "… no GPU; Proton runs only under the Steam client" (quoting `validation_stats.reason`) | 9.4/search/S4-ci-observability.md:262 ("a tool for use with the Steam client"), :357 (the README documents only Steam-client installation; no run-requirements paragraph) | WORDING-OUTSIDE-PASSAGE | f30b086b 2026-10-14 | 2026-09-13 |

### `pytorch-examples`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-76 | proposal:639, :642; related-work.md:18; research-claims.md:263 | `pytorch-examples` | "PyTorch's basic MNIST example on the CPU — an actual training run" | task-9.10-scenarios-timelines/changelog.md:224 (9.10 D12, `main.py:75–114` at the read commit) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-03 |
| C-48 | vol-03:1560, :1653, :1781; vol-04:550, :1061; vol-05:498, :594 | PyTorch examples "Basic MNIST Example"; GNOME Tracker | "PyTorch의 기본 MNIST 예제"; Tracker indexes the home folder | R10search/S2-project-docs.md:3615–3624 (S2-31, `pytorch/examples` at `acc295dc`); the Tracker job, R10search S2-43 (record list :66–68); R12changelog.md:246 (D14) | TRACED | 00f6a737 / ba94cbb5 2026-10-17 | 2026-10-01/04 |
| E-49 | G/02:1023; G/03:441 | `pytorch-examples` | the training job is PyTorch's own "Basic MNIST Example" | 9.10 S2:3615 (S2-31) | TRACED | f30b086b 2026-10-14 | 2026-10-01 |
| F-41 | v06:259, :1519 | `pytorch-examples` | the "Basic MNIST Example", commit `acc295dc` | 9.10/search/S2-project-docs.md:3615–3620 | TRACED | f30b086b 2026-10-14 | 2026-10-01 |

### `roeser-rw24`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| D-18 | vol-06:884-912, 936-948, 1163, 3587-3589 | `roeser-rw24` | mixture of fluent and disfluent transitions, two log-normal components; LF-bigrams 158 ms, disfluency 95 ms with probability 0.34, consonants 429 / 414 / 0.73; "task-specific"; 158 is a log-scale location (prior "5 log msecs (i.e. ≈150 msecs)"); disfluent component ≈ 253 ms; Table 3 variances 0.29 / 1.16 | R08:203, :242-252, :268-270, :307, :309, :341, :350-360 | TRACED | ff925573 2026-09-13 | 2026-09-13 |
| E-23 | G/02:1368, :1423 | `roeser-rw24` | the old entry's distribution shape (fluent 158 ms, pause probability 0.34) from Roeser, a different task and participants | K4:46–57 (158 ms the back-transformed location, LF-bigrams; 0.34 the LF-bigrams disfluency probability) | TRACED | f30b086b 2026-10-14 | 2026-09-13 |
| F-28 | v06:517; v08:747 | `roeser-rw24` | 158 ms is a log-scale location, stored as a mean; the paper's pause component ≈ 253 ms | R08:242–252 (Table 3: β 158, δ 95; β+δ the disfluent mean; log scale) | TRACED | f30b086b 2026-10-14 | 2026-09-13 |

### `rt-app`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| B-27 | docs/simulator/interpretation-contract.md:11 | `rt-app` | "integer microseconds throughout (rt-app precedent)" | R01:310 (tutorial: "The duration is defined in usec") | TRACED | 0c340f36 2026-08-27 | 2026-09-13 |
| B-28 | docs/simulator/interpretation-contract.md:31 | `rt-app` | TIMER: "runnable at t₀+k·period regardless of when the previous iteration finished — drift-free (rt-app `timer{ref,period}`)" | R01:348 (`"mode"` default `"relative"`); R11/search/S2-project-docs.md:616–640 (tutorial.txt:507–509, :518–522; relative mode re-anchors on an overrun) | WORDING-OUTSIDE-PASSAGE | 0c340f36 2026-08-27 | 2026-09-13; 2026-09-24 |
| C-17 | vol-01:3059 (first sentence) | rt-app | "주기 작업 도구 rt-app의 \"absolute\" mode가 이렇게 합니다" (catches up every late iteration) | R11search/S2-project-docs.md:612 (S2-14, `tutorial.txt:507–509`, `rt-app.c:589–597` at `d6f8be4`); R11changelog.md:46 (9.11 D3: "only \"absolute\" mode keeps the grid and catches up") | TRACED | e4ac1624 2026-10-17 | 2026-09-24 (re-read 2026-10-07) |
| C-40 | vol-02:3228–3357 (§8.2–8.3) | hackbench, schbench, interbench, rt-app `README.in` | quotations and defaults ("Time: 0.890") | V60-vol02-quotations.md:460–531 (52 exact; notes B hackbench pin, C rt-app `README.in`); R11search/S2-project-docs.md:612, :644, :726, :747 (S2-14, S2-15, S2-18, S2-20); RV/reads/R01-interbench-rtapp-benchtools.md | TRACED | a9fd9601 2026-09-12 | 2026-09-24 / 2026-10-09 |
| D-11 | vol-06:358-374, 390-396, 495 | `rt-app` (`doc/tutorial.txt` at `d6f8be41`, 2026-06-10) | `sleep` and `timer` event definitions quoted; the task A / task B example ("task B period stays to 19 … task A starts at 15 but increases to 19"); example values "wake every 100 ms, run 10 ms" | R01:5-27 (copy), R01:310 (sleep), :320-321 (timer, task B), :372-377 (template run 10000, timer period 100000) | TRACED | ff925573 2026-09-13 | 2026-09-13 |
| E-15 | G/01:285; G/02:100 | `rt-app` | rt-app's JSON task model and `timer` event are the TIMER primitive's precedent (run/period/deadline in µs) | K1:349–356 (`dl-period` "The unit is usec"; SUPPORTED); R01:313 | TRACED | f30b086b 2026-10-14 | 2026-09-13 |
| E-16 | G/03:244, :2397 | `rt-app` | "Linux scheduler 연구에서 널리 쓰는 workload 생성 도구로, 시간을 µs 정수로 다룹니다" (widely used; handles time as integer µs) | K1:362 ("rt-app's unit for run/sleep/timer/dl-* durations … rt-app's global duration is in seconds") | WORDING-OUTSIDE-PASSAGE | f30b086b 2026-10-14 | 2026-09-13 |
| E-17 | G/01:289; G/02:137 | interbench, ROS 2 executor (Teper et al.), Lipari & Palopoli, `rt-app`, `mpv` | periodic frameworks skip missed periods by default: interbench, ROS 2's executor, Lipari & Palopoli's thread, rt-app's default "relative" mode; mpv drops late video frames; rt-app's "absolute" mode catches up | `R/task-9.11-scheduler-constants/search/S1-literature.md:293–316` (S1-15, S1-16); `…/S2-project-docs.md:617–642` (rt-app `tutorial.txt:507–522`), `:644` (interbench), `:694–713` (mpv); changelog D17 `:232` | TRACED | c4f0ac36 2026-10-17 (G/01); f30b086b 2026-10-14 (G/02) | 2026-09-24 / 2026-10-08 |

### `runson`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| F-37 | v06:721; v08:1003 | RunsOn | 30-day sample: Xeon 6973P-C and Platinum 8573C under `ubuntu-24.04`; Passmark single-thread medians 26 % apart | 9.6/search/S4-ci-observability.md:385–395 | TRACED | f30b086b 2026-10-14 | 2026-09-16 |

### `schedcp-mlsys25`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-15 | related-work.md:24 | same + `schedcp-mlsys25` §2 | "require extensive per-workload retraining … a problem space a human has already formalized" | S1:166 (§7.4), S1:183 (pp. 3, 10, 13), S1:200 (§3.3), S1:264 (SchedCP v2–v4 §2); CL12:341 (D20) | TRACED | 0c340f36 2026-08-27 | 2026-10-07 |
| A-18 | related-work.md:32, :34, :48 | `schedcp-mlsys25` | semantic gap; tiered Workload Analysis Engine; multi-agent; synthesize or select eBPF schedulers; "1.79× total improvement over EEVDF"; Opus 8/8 quote; evaluation and motivations; a laptop | S1:264 (S1-12 v1–v4), S1:510 (S1-34), AA:249 (A4-01) | TRACED | 0e3b627d 2026-10-17 | 2026-10-07/09 |
| C-35 | vol-02:2213–2524 (§6.2) | SchedCP, arXiv:2509.01245 v1–v4 | quotations with version marking; "MLforSystem 2025"; v1/v2 8-page, v3/v4 6-page | V60-vol02-quotations.md:410–424 ("Versions and dates", journal-ref, length history); R12search/S1-literature.md:264, :510 (S1-12, S1-34); R12changelog.md:379, :1563 (D23, D104) | TRACED | 00f6a737 2026-10-17 | 2026-10-09 |

### `schedext-docs`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-02 | related-work.md:8, :59 | `schedext-docs` | "first released in Linux 6.12" | S2:511 (kernel tree v6.11 / v6.12-rc1) | TRACED | 0e3b627d 2026-10-17 | 2026-10-08 |
| A-03 | related-work.md:8 | `schedext-docs` | quotes "can be turned on and off dynamically anytime"; "The system integrity is maintained …" | S2:69 (`sched-ext.rst:14`, `:16-19` at v6.12) | TRACED | 0e3b627d 2026-10-17 | 2026-10-07 |
| A-49 | proposal:146, :840 | `schedext-docs` | "Pluggable schedulers loaded from userspace as BPF programs" | S2:69 (`sched-ext.rst:5-6`), S2:511 (`Kconfig.preempt`) | TRACED | 0c340f36 2026-08-27 | 2026-10-07/08 |
| C-20 | vol-01:3234 | sched_ext | "2024년 말에 나온 kernel 버전부터 … kernel을 다시 컴파일하지 않고, 심지어 실행 중에 갈아 끼울 수 있습니다" | R12search/S2-project-docs.md:511–515 (S2-47: first release Linux 6.12, the tree read at v6.11/v6.12-rc1/v6.12 — no release date recorded); :69 (S2-01, "turned on and off dynamically anytime"); R12changelog.md:118 (D7) | WORDING-OUTSIDE-PASSAGE (the date "2024년 말"; the rest within) | 45a3442e 2026-09-12 | 2026-10-08 |
| C-30 | vol-02:1095–1183 (§3.3) | `sched-ext.rst` v6.12 and mainline `7b63ef2d` | quotations; integrity and fallback; no verifier claim | V60-vol02-quotations.md:163–178; R12search/S2-project-docs.md:69, :83 (S2-01, S2-02); R12changelog.md:118 (D7) | TRACED | a9fd9601 2026-09-12 | 2026-10-08/09 |
| C-44 | vol-03:54 | sched_ext | table "누가 켜나": "관리자가 policy 프로그램을 올림" | none for who loads (S2-01 at R12search/S2-project-docs.md:69 and S2-47 :511 state runtime loading and the Kconfig option, not the privilege) | NO-RECORD | c312d6b3 2026-09-12 | — |

### `schedext-lpc24`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-05 | related-work.md:8, :12 | `schedext-lpc24` | maintainers' LPC 2024 slides "presented by Meta" report `scx_layered` "deployed in 1M+ machines with significant perf gains" | S2:517 (slides `:20–27`; timetable presenter David Vernet, Meta) | TRACED | 0e3b627d 2026-10-17 | 2026-10-08 |
| A-55 | proposal:152 | `schedext-lpc24`, `lu-lpc25`, `steamos-lavd` | "operators running sched_ext schedulers in production, as Meta's speakers report it"; SteamOS LAVD user-selected | as A-05, A-06, A-08 | TRACED | 32a5c9dd 2026-10-17 | 2026-10-07/08 |

### `scx`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-04 | related-work.md:8 | `scx` | "The sched-ext/scx repository ships schedulers built on it" | S2:170 (`scheds/rust/README.md:15-29`) | TRACED | 0e3b627d 2026-10-17 | 2026-10-07 |
| A-09 | related-work.md:20 | `scx` (lat_cri.bpf.c) | "Valve sponsors LAVD's development" | S2:188 (`lat_cri.bpf.c:3-4`), S2:246 (LWN 1051430) | WORDING-OUTSIDE-PASSAGE | 0e3b627d 2026-10-17 | 2026-10-07 |
| A-13 | related-work.md:16 | `scx`, `lavd-ossna24` | latency criticality from wait/wake frequencies, runtime, weight; propagated waker↔wakee; sets deadline and slice; motivated by gaming, stuttering | S2:170 (`lat_cri.bpf.c:179-217`, README `:7-12`, `:20-23`), S2:195 (slides 22, 25) | TRACED | 0e3b627d 2026-10-17 | 2026-10-07 |
| A-64 | proposal:243, :844 | `scx` | "scx_lavd 0.5–5 ms with a boost to 500 ms, scx_rusty 20 ms or 1 ms" | S2-11s:570 (`lavd.bpf.h:73-75`), S2-11s:607 (`main.rs:97-103`, `tuner.rs:173-176`) at `00fec1e`; CL11:427 (D31, re-read at v1.1.3, the boost by locator only) | RECORD-BELOW-STANDARD (the 500 ms boost); TRACED (the 0.5–5 ms and 20 / 1 ms) | 32a5c9dd 2026-10-17 | 2026-09-24 / 2026-10-08 |
| B-19 | harness/guards/guard-spec.yaml:57, :153 | `scx` | shipped scx schedulers set "30 s (lavd), 10 s (rusty) and 5 s (bpfland) at release v1.1.3" | R11/changelog.md:266 (D19: `.timeout_ms` lines at v1.1.3, tag object `b2cd800e`, read 2026-10-08) | TRACED | 137ee257 2026-10-08 | 2026-10-08 |
| C-31 | vol-02:1184–1256 (§3.4) | scx v1.1.3 README/OVERVIEW; LPC 2024 slides; LPC 2025 contributions 2039, 2099; SteamOS 3.8 | "scx_layered deployed in 1M+ machines" (slides, presenter Meta per timetable); Reality Labs GPU fleet; scx_lavd a fleet-default candidate; SteamOS 3.8 scx_lavd user-selectable, not enabled | V60-vol02-quotations.md:179–189; R12search/S2-project-docs.md:211 (S2-11), :262 (S2-15), S2-48 (after :515); R12changelog.md:134, :152, :1133 (D8, D9, D73) and D113 | TRACED | 00f6a737 2026-10-17 | 2026-10-08/09 |
| C-46 | vol-03:1101; vol-04:1272, :1334 | Linux `kernel/sched/ext.c` v6.17; scx v1.1.3 | "최대이자 기본값이 30초입니다(커널 v6.17의 `kernel/sched/ext.c`). 배포된 scx scheduler들은 30초, 10초, 5초" | R11changelog.md:107–113 (9.11 D7: `ext.c:749–757` at v6.17, "byte-identical to the S4-05 copy"), :262–266 (D19: the three timeouts with file:line at `v1.1.3`, tag `b2cd800e`, read 2026-10-08) | TRACED | 00f6a737 / ba94cbb5 2026-10-17 | 2026-10-07/08 |

### `shneiderman-csur84`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-82 | proposal:696 | `shneiderman-csur84` | modest variation tolerable; frustration when delays are "at least twice the anticipated time"; studies of second-scale responses (§5.3, p. 282) | AA:444 (A5-11) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-09 |
| B-09 | docs/harness/metrics.md:299 | `shneiderman-csur84` | reports Long 1976: "delays of approximately 0.1-0.5 second …", typists "worked more slowly and made more errors" | R11/search/S1-literature.md:180 | TRACED | 99257433 2026-10-08 | 2026-09-24 |

### `slice-search-findings`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| F-50 | v06:1420, :1436, :1454 | 9.6 / 9.7 / 9.8 search findings | Antfarm (ATC '06) 815 / 748; Gouicem et al. (ATC '20) 80-core build phases; MOSBENCH gmake; Slack/Discord/Skype 1 Hz CPU on Ubuntu 22.04; renderer reuse on Debian 8 | 9.6/search/candidates.md:12–15; 9.8/search/candidates.md:7–12; 9.7/search/candidates.md | TRACED | f30b086b 2026-10-14 | 2026-09-1x |

### `spotify`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| E-55 | G/04:732 | Spotify | "Spotify 네이티브 client는 계정이 필요하기 때문입니다" (the native client needs an account) | 9.10 S4:1981 ("reader's expectation, not documented in the sources read except for Steam"); `R/task-9.10-scenarios-timelines/changelog.md` D24 (:521) states it without a source | NO-RECORD | f30b086b 2026-10-14 | — |

### `sprague-iclr25`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-70 | proposal:346 | `sprague-iclr25`, `tam-emnlp24` | little or no gain from reasoning first on non-math questions; 7–9B models gain on math; JSON-schema decoding helped classification, hurt reasoning; answer-first turned CoT into direct answering | AA:138 (A2-14, Sprague Table 6, §4.2; Tam pp. 1220–1221, 1224); AA:223 (A3-06) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-09 |

### `steam-downloads`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-61 | proposal:185 | `steam-downloads`, `steam-for-linux-8821` | Steam queues updates itself, "by default pauses queued downloads when a game launches"; an install begun during play starts at once | 2026-09-13-verification/reads/R07-gamemode-steam-dkms.md (C-steam-2, -3); task-9.10-scenarios-timelines/search/S3-traces-datasets.md:479 (S3-27); CL12:288 (D16) | TRACED | 32a5c9dd 2026-10-17 | 2026-09-13 / 2026-10-01 |
| C-16 | vol-01:1397, :2518–2527; vol-02:3142–3161; vol-03:143, :173–217, :268–269, :319, :644, :1174; vol-04:376 | Steam FAQs; steam-for-linux #8821 | updates "스스로 줄 세우고 기본 설정에서는 게임이 시작되면 줄 세운 다운로드를 멈추며, 게임 중에 시작한 설치는 곧바로 돌린다" | RV/reads/R07-gamemode-steam-dkms.md:153–157 (FAQ 4F9E-…: "Steam automatically pauses your downloads when a game is launched"); R12changelog.md:288 (D16, quoting FAQ 71AB-… and #8821 via 9.10 S3-27) | TRACED | 00f6a737 2026-10-17 | 2026-09-13 / 2026-10-08 |
| E-11 | G/04:1040 | `steam-downloads`; steam-for-linux issue #8821 | Valve FAQ: "Steam automatically pauses your downloads when a game is launched"; issue #8821 reports Install during play starts downloading at once | R07:153; 9.10 S3:476–477 | TRACED | f30b086b 2026-10-14 | 2026-09-13 / 2026-10-01 |

### `steamcmd`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| D-40 | vol-06:2366 | SteamCMD documentation (9.4 S4) | "`steam`의 다운로드는 계정이 있어야 해서" (the Steam download needs an account) | 9.4 S4:269-270 ("game downloads need an owning, Steam-Guard-capable account") | TRACED | ba94cbb5 2026-10-17 | 2026-09-13 |

### `steamos-lavd`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-08 | related-work.md:8, :12, :20 | `steamos-lavd` | SteamOS 3.8 offers `scx_lavd` "as a CPU scheduler the user selects", "installed and configured but not enabled by default" | S2:262 (S2-15), S2:527 (S2-49), S2:538 (S2-50) | TRACED | 0e3b627d 2026-10-17 | 2026-10-07/08 |

### `steamos-refresh`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| D-27 | vol-06:1424, 1665, 3546, 3661, 3826 | `steamos-refresh` | frame period grounded on "Steam Deck LCD의 기본 화면 갱신 60 Hz", value labelled design | 9.4 S2:157-170 (S2-08: "The default is 60Hz (which can be frame-limited to 60, 30, and 15fps)"; "60hz = 16.66ms/frame") | TRACED | ba94cbb5 2026-10-17 | 2026-09-13 |
| E-26 | G/02:720; G/02:709; G/03:1715; G/01:1196 | `steamos-refresh` | Valve, "The SteamOS 3.2 Update", 2022-05-26: "The default is 60Hz … 60hz = 16.66ms/frame" | `R/task-9.4-gaming/search/S2-project-docs.md:163`; `…/candidates.md:51` | TRACED | f30b086b 2026-10-14 | 2026-09-13 |

### `swell-icmi14`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| D-38 | vol-06:828, 2366, 2464 | `swell-icmi14` | keystroke streams are SWELL-KW's (Koldijk et al., 2014) real input replayed by the campaign | 9.5 S3:246-262 (S3-swell-kw: 25 participants, per-keystroke `TimeStamp` with application) | TRACED | ba94cbb5 2026-10-17 | 2026-09-13 |
| E-20 | G/01:788; G/02:310; G/03:537, :2320; G/02 glossary | `swell-icmi14` | SWELL-KW: 25 students and interns, 2012, a Windows lab, about 3 hours each, knowledge-work tasks; per-key timestamps with the foreground application | R10:233, :244; 9.10 S1:500–505 ("25 participants (~3 hours each)"; Windows 7, Office 2010); 9.10 S3:199 (2012) | TRACED | da39802c 2026-10-17 (G/01 "약 3시간씩"); f30b086b 2026-10-14 (others) | 2026-09-13 / 2026-10-01 |
| E-21 | G/02:537 | `swell-icmi14` (registry notes) | "Timestamps quantised at the 15.6 ms Windows tick" | none found: no read record or search log states a 15.6 ms tick for SWELL-KW (grep of all slices' search logs and the 2026-09-13 reads for `15.6`, `quanti`); the only 15.6 ms passages are about the Balabit pointer traces (`R/task-9.5-interactive-typing/search/S3-traces-datasets.md:212`) | NO-RECORD | f30b086b 2026-10-14 | — |
| F-31 | v06:816, :1010, :1117, :1339, :1692; v08:954, :956 | `swell-icmi14` | 25 participants × ~3 h, free composition, per-keystroke timestamps with the focused application, 2012 Windows lab; Koldijk et al. 2014, DANS, CC-BY-NC-SA-4.0 | 9.5/search/S3-traces-datasets.md:246–262 | TRACED | f30b086b 2026-10-14; v06:1117 2c451543 2026-10-17 | 2026-09-13 |

### `sysstat-debian`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| F-53 | v08:1749 | `sysstat-debian` | sysstat's postinst: one conditional (`/run/systemd/system`) changed the conclusion | 9.10/search/S2-project-docs.md:740–794; 9.9/changelog.md:450 | TRACED | f30b086b 2026-10-14 | 2026-10-01 |

### `systemd-oomd`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| F-04 | v05:398, :1132 | `systemd-oomd` | `DefaultMemoryPressureDurationSec=` "Defaults to 30 seconds when unset or 0" | 9.19/changelog.md:19 (`man/oomd.conf.xml` at `main`, 263~devel) | TRACED | f30b086b 2026-10-14 | 2026-10-11 |

### `teper-arxiv24`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| D-12 | vol-06:460 | `teper-arxiv24` (ROS 2 executor), `lipari-arxiv15`, `rt-app` default mode | the periodic tools read on 2026-10-07 skip missed periods by default: interbench, ROS 2's executor, Lipari & Palopoli's periodic thread, rt-app's default mode | 9.11 S1:307-312 (S1-16, §II "the executor may skip timer jobs"); 9.11 S1:293-301 (S1-15, Listing 2 "Skip late instances"); 9.11 S2:612-642 (S2-14, `tutorial.txt:507-522`) | TRACED | e4ac1624 2026-10-17 | 2026-09-24 (re-read 2026-10-07, 9.11 changelog D3) |

### `thunderbird`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| E-41 | G/02:839 | Thunderbird source (`MessageSend.sys.mjs`) | after the send notification Thunderbird awaits `_doFcc()` (copy to Sent) | `R/task-9.5-interactive-typing/changelog.md:194` (changeset `787dc790d77f`, `notifyListenerOnStopSending(…)` then `await this._doFcc()`); copy `R/task-9.7-background-io/search/S2-project-docs.md:365–367` (S2-18) | TRACED | f30b086b 2026-10-14 | 2026-09-17 |

### `tracker-miners`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-57 | proposal:158, :97 | `tracker-miners`, `baloo`, `deja-dup`, `clamav`, `borg`, `restic` | LocalSearch and Baloo set background classes on themselves; Déjà Dup "`chrt --idle 0`"; ClamAV, borg, restic declare nothing, restic leaves `nice`/`ionice` to the user | S2:349 (S2-24), S2:355 (S2-25), S2:361 (S2-26), S2:367 (S2-27), S2:373 (S2-28) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-07 |
| A-77 | proposal:97, :642; related-work.md:18; research-claims.md:268 | `tracker-miners`, `deja-dup` | the indexer `SCHED_IDLE` at nice 19 with the idle I/O class, "set by the program on itself"; the backup in the idle class | S2:349 (S2-24 `tracker-main.c:84-107`), S2:367 (S2-27) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-07 |
| E-06 | G/02:1333 | `tracker-miners` (`tracker-main.c`, `tracker-sched.c`) | Tracker puts every thread at `SCHED_IDLE`, nice 19, idle I/O class | 9.10 S2:3766 (`tracker-main.c:821`, `:199–203` `tracker_sched_idle`) | TRACED | f30b086b 2026-10-14 | 2026-10-01 |
| F-47 | v06:1328 | systemd, tracker-miners (Ubuntu 24.04 packages) | Tracker in `background.slice`, apps in `app.slice`, CPUWeight 30 vs 100, ~23 % | 9.11/changelog.md:221–222 (packages, files, lines, read 2026-10-08) | TRACED | f30b086b 2026-10-14 | 2026-10-08 |

### `tuneagent-kdd26`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-20 | related-work.md:32, :48 | `tuneagent-kdd26` | "tune the kernel's build configuration" | AA:296 (A4-06), S1:314 (S1-14) | TRACED | 0e3b627d 2026-10-17 | 2026-10-09 |

### `tuned`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| F-03 | v05:397, :1130 | `tuned` | tuned v2.28.0 `tuned-main.conf`: `update_interval = 10`; `dynamic_tuning = 0` by default | 9.19/changelog.md:17 | TRACED | f30b086b 2026-10-14 | 2026-10-11 |

### `tuxbot-arxiv26`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-22 | related-work.md:32, :34 | `tuxbot-arxiv26` | "up to 41 Linux parameters", "not kernel fast-path controllers …", Gemini 2.5 Flash/Flash-Lite, typed validation | S1:347 (S1-17), AA:146 (A2-16), AA:260 (A4-02) | TRACED | 0e3b627d 2026-10-17 | 2026-10-07/09 |

### `ubuntu-desktop-manifest`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-58 | proposal:158 | `ubuntu-desktop-manifest`, `plocate-ubuntu`, `plocate-debian`, `findutils-debian`, `locate-ubuntu` | `updatedb` not installed on the depicted desktop; plocate 1.1.19 idle I/O only; Debian's units declare both; Ubuntu's `locate` cron at nice 10, idle I/O | AA:103 (A2-05); CL12:1018 (D64) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-09 |
| C-52 | vol-05:597, :605 | Ubuntu 24.04.5.1 image manifests | "Ubuntu의 기본 설치 목록에 색인기 Tracker가 들어 있다" | R10search/S2-project-docs.md:75 (S2-01, the manifests); R10search/candidates.md:42 ("Tracker 3.7.1 is in the default one") | TRACED | ba94cbb5 2026-10-17 | 2026-10 (9.10 stage 2) |

### `ubuntu-drivers`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| E-09 | G/02:1207 | Ubuntu (`ubuntu-drivers`), NVIDIA, Steam survey | ZFS and v4l2loopback ship prebuilt; `ubuntu-drivers` installs prebuilt without `--include-dkms` and picks `-open` first; NVIDIA "We recommend the use of open kernel modules on all GPUs that support it"; Steam Aug 2026 survey: 87.0 % of NVIDIA users on open-capable GPUs | 9.10 S2:3677, :3686, :3702; 9.10 S3:822 (reader's own: 21.16 of 24.32 %) | TRACED | f30b086b 2026-10-14 | 2026-10-01/02 |

### `ubuntu-hwe-config`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-54 | proposal:152 | `ubuntu-hwe-config` | HWE 7.0.0-34 "sets `CONFIG_SCHED_CLASS_EXT=y` for amd64" | S2:557 (S2-52, `debian.master/config/annotations`) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-08 |

### `unattended-upgrades`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| E-03 | G/01:45; G/02:1137; G/04:1069, :1651 | `unattended-upgrades`, `apt` (Ubuntu 24.04 packages) | in the default desktop layer, on by default, daily 06:00 with up to 60 min random delay, `Persistent=true`, AC power only | 9.10 S2:301–326 (`apt-daily-upgrade.timer`: `OnCalendar=*-*-* 6:00`, `RandomizedDelaySec=60m`, `Persistent=true`; service `ConditionACPower=true`), :339 (`20auto-upgrades`) | TRACED | f30b086b 2026-10-14 | 2026-10-01 |
| F-39 | v06:1170, :1174 | Ubuntu `unattended-upgrades` | in the 24.04 desktop's default layer, enabled, daily 06:00 with up to 60 min delay | 9.10/search/S2-project-docs.md:308–342 | TRACED | f30b086b 2026-10-14 | 2026-10-01 |

### `vrable-fast09`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| E-48 | G/02:1173, :1179 | `vrable-fast09` | Cumulus's personal-machine change rates used for the 7-day change set | `R/task-9.7-background-io/search/T9-S1-literature.md:551–560` (T9-S1-05, accessed 2026-09-19) | TRACED | f30b086b 2026-10-14 | 2026-09-19 |

### `vulcan-arxiv25`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-19 | related-work.md:32, :34 | `vulcan-arxiv25` | Anvil; spot-VM scheduling, cache eviction, tiered memory; CPU scheduling only an interface-table example | S1:361 (S1-18), AA:142 (A2-15), AA:269 (A4-03) | TRACED | 0e3b627d 2026-10-17 | 2026-10-07/09 |

### `vulkan`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-81 | proposal:654, :816 | `vulkan`, `gstreamer` | a late game frame shown at the next vertical blank under FIFO; a video sink drops a frame "later than its allowed lateness" | AA:411 (A5-07, `wsi.adoc:4418–4426`, `gstbasesink.c:118–124`) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-09 |
| B-30 | docs/simulator/simulator-guide.md:132, :136 | `vulkan` | "a frame presented in Vulkan's FIFO mode waits for the next vertical blank" | R12/search/A-audit.md:413–414 (`wsi.adoc:4418–4426`) | TRACED | 5479dcab 2026-10-06 | 2026-10-09 |
| B-50 | docs/background-guide.md:224 | `vulkan`, `gstreamer`, Ardour manual | late game frame "shown at the next vertical blank under FIFO presentation"; "a video sink drops a frame later than its allowed lateness"; "a late audio buffer is an xrun" | R12/changelog.md:1386–1394 (9.12 decision D90); R12/search/A-audit.md:414; R11/search/S2-project-docs.md:720–723; R12/search/S2-project-docs.md:598 (S2-57) | TRACED | 0e3b627d 2026-10-17 | 2026-10-09 |
| D-15 | vol-06:462 | Chromium fake audio, `vulkan` FIFO (via 9.11 D3) | for audio and games the sources read do not say which late tick is processed, so the choice is ours | 9.11 changelog D3 (Chromium: one late callback, then "the next nearest ontime interval"; FIFO frame takes the next vblank) | TRACED | e4ac1624 2026-10-17 | 2026-10-06/07 |

### `waldspurger-osdi94`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-71 | proposal:421 | `waldspurger-osdi94` | "Lottery gives shares proportional in expectation, its accuracy improving with √n of the draws, so background gets an expected 15 % (`waldspurger-osdi94`)" | S1:215 (S1-09 p. 2); docs/recognition-vocabulary.md:115 (the 15 % is `batch_share`, "No source names a batch-class share") | WORDING-OUTSIDE-PASSAGE | 32a5c9dd 2026-10-17 | 2026-10-07 |
| A-72 | proposal:428, :824 | `waldspurger-osdi94` | eventually wins, after 1/p lotteries on average, "with no bound on the wait" (§2.2); O(n) list, O(lg n) tree (§4.2) | S1:215 (S1-09), AA:119 (A2-09: "has a geometric distribution") | TRACED | 32a5c9dd 2026-10-17 | 2026-10-09 |
| B-14 | docs/recognition-vocabulary.md:115 | `waldspurger-osdi94` | "defines shares as proportional to tickets and gives no ratio between classes" | R11/search/S1-literature.md:116 (no class ratio); R12/search/S1-literature.md:220 ("The expected allocation … is proportional to the number of tickets") | WORDING-OUTSIDE-PASSAGE | 0e26b61c 2026-09-07 | 2026-09-24; 2026-10-07 |
| B-49 | docs/background-guide.md:221 | lottery scheduling (Waldspurger & Weihl, uncited) | "Gives proportional shares" | R12/search/S1-literature.md:220 ("The expected allocation … proportional"; "the actual allocated proportions are not guaranteed to match") | WORDING-OUTSIDE-PASSAGE | 11158fe4 2026-08-28 | 2026-10-07 |
| C-04 | vol-01:2602, :2680 | Waldspurger & Weihl 1994 | "1994년에 제안된 방식"; "원래 논문은 ticket 수에 비례해서 나눈다는 원리만 제시하고 class 간 비율은 말하지 않습니다" | R11search/S1-literature.md:103–116 (S1-03, "No passage states a ticket ratio between classes of work") | TRACED | 45a3442e / e247d94a 2026-09-12 | 2026-09-24 |
| C-23 | vol-02:477–516 (§2.4) | Waldspurger & Weihl 1994 | quotations; proportional in expectation, no starvation for ticket holders | V60-vol02-quotations.md:75–81; R12search/S1-literature.md:215 (S1-09); R12changelog.md:579, :1057 (D36, D67) | TRACED | a9fd9601 2026-09-12 | 2026-10-09 |

### `win-priority-boosts`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| C-14 | vol-01:3339 (table row "foreground window 우대") | Linux, Windows, macOS | Linux "부분적", Windows "있음", macOS "있음" | Windows: R12search/A-audit.md:328 ("boosts the priority class of the process associated with the foreground window"); Linux and macOS: none | NO-RECORD (Linux and macOS cells) | 45a3442e 2026-09-12 | — |

### `win-sched-priorities`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-44 | proposal:117, :826 | `win-sched-priorities`, `win-priority-boosts`, `ostep` | "Windows' priority boosts and decay are an MLFQ form"; OSTEP names Windows NT | S2:569 (S2-54), S1:101 (OSTEP p. 10) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-07/08 |
| C-10 | vol-01:2094, :3338 (table row "프로그램의 자기 선언") | Windows priority classes | "Windows에는 priority class가 있어서 프로그램이 자기를 배경 작업으로 등록할 수 있습니다" | none: R12search/S2-project-docs.md:579–580 (S2-54) quotes priority levels and boosts only; R12search/A-audit.md:328 quotes the foreground boost of `NORMAL_PRIORITY_CLASS` | NO-RECORD | 45a3442e 2026-09-12 | — |

### `wowah-mmsys11`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-68 | proposal:309 | `wowah-mmsys11` | one realm (TW-Light's Hope, Horde): median avatar's average session 1.8 h, "5th–95th percentile 0.4–5.5 h" (Table 4) | AA:134 (A2-13, pp. 124–126) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-09 |

### `xbox-gamemode`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-29 | related-work.md:40; proposal :149 | `xbox-gamemode` | "prevents Windows Update from performing driver installations and sending restart notifications" | S2:604 (S2-58), AA:158 (A2-19) | TRACED | 0e3b627d 2026-10-17 | 2026-10-09 |

### `xnu-sched`

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-45 | proposal:117 | `xnu-sched` | Clutch/Edge "EDF over QoS buckets", ULE variant across thread groups, Mach usage-decayed priority | S2:569 (S2-54, `sched_clutch_edge.md:1–12`, `:24–28`, `:72`, `:95–99`) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-08 |
| A-59 | proposal:158 | `xnu-sched` | "priority inflation across the platform", an artifact of the Mach scheduler, a motivation for Clutch | S2:569 (S2-54); CL12:771 (D49, `sched_clutch_edge.md:7` verbatim) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-08 |

### (no source: labels)

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| B-10 | docs/harness/metrics.md:290–295 | none (labels) | latency floor 1 000 µs "design"; fraction floor 0.01 "design"; seed 20260911 and 10 000 repetitions "design, pinned"; interval level 95 % "convention" | R11/changelog.md:179 (9.11 decision D13) | LABELLED | — | 2026-10-07 |
| B-15 | docs/recognition-vocabulary.md:114, :115, :116, :120 | none (labels) | EDF and LOTTERY slices equal the MLFQ slice, "design (the same-granularity rule)", "this project's, not a source's"; `batch_share` 0.15 "design, unbounded by any source" | R11/changelog.md:181–182 (9.11 decision D13, items 18–20) | LABELLED | 07b736d6 2026-10-08 | 2026-10-07 |
| B-20 | harness/guards/guard-spec.yaml:114–160 | none (labels) | `provenance_share` 0.5 "Design"; `utilisation_sanity` "arithmetic"; `config_age`, `determinism`, `tick_count`, `validation_matches_provenance`, `c2_pair` "structural" | R11/changelog.md:139 (D10), :176–187 (D13) | LABELLED | 137ee257 2026-10-08 | 2026-10-07 |
| B-24 | harness/experiments/rq0-gate.yaml:122, :131 | none (label) | 500 µs and 100 000 µs: "the config schema's lower / upper bound on the top slice" | R11/changelog.md:184 (D13, items 22 and 25: design) | LABELLED | 549c9ac1 2026-09-12 | 2026-10-07 |
| B-52 | docs/harness/harness-and-records-guide.md:1243 | none (label) | `c1-media` music 1.0 : video 0.5 "stated assumption … 문헌 검색 안 함" (no literature search) | — (a stated assumption, so labelled) | LABELLED | — | — |
| C-05 | vol-01:2680 | (none: the boot default's LOTTERY batch share) | "이 값은 근거 없는 가정이라고 문서에 명시해뒀습니다" | — | LABELLED (placeholder, "assumption") | 45a3442e 2026-09-12 | — |
| C-47 | vol-03:2259, :2686 | (none: the RQ0 gate's gap 0.5) | "이 값에 출처는 없습니다. 실험 전에 정한 … 선" | — | LABELLED (design) | c312d6b3 2026-09-12 | — |
| D-47 | vol-06:2766 | (none) | `parallelism_cap` 8 "설계로 정한 값(8 thread 데스크톱의 `nproc` 규칙)" | — (design, stated as such) | LABELLED | ba94cbb5 2026-10-17 | — |
| F-06 | v05:1143 | (the precedent search's reading) | "Three scales: hardware-state governors at 0.5 ms–80 ms …" (quoted) | 9.19/changelog.md:25 (quoted verbatim) | TRACED | f30b086b 2026-10-14 | 2026-10-11 |

### (registry forms)

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-33 | related-work.md:56–82 | registry forms | venues, versions, commits per key (e.g. arXiv 2512.25065v3 "Accepted for publication at EuroSys 2027", man-pages 6.19) | CL12:406 (D25), CL12:1563 (D104), AA:223 (A3-06), the S1/S2 candidates' citation lines | TRACED | 0e3b627d 2026-10-17 | 2026-10-07/09 |

### (search log)

| # | Location | Source | Claim (repository wording) | Record (path:line) | Verdict | Wording introduced | Record date |
|---|---|---|---|---|---|---|---|
| A-32 | related-work.md:48 | search log | "in the literature searched through 2026-10-08 — no prior work measures …"; the three nearest measurements | S1:1–75 (search log), search/candidates.md "Not found" T5; CL12:205 (D12) | TRACED | 0e3b627d 2026-10-17 | 2026-10-08 |
| A-67 | proposal:267 | search log | "no source found measures how often a desktop's process set changes" | search/candidates.md "Not found" T12; S3:381 (S3-12), S3:428 (S3-16) | TRACED | 32a5c9dd 2026-10-17 | 2026-10-07 |
