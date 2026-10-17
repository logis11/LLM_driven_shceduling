# 9.16 claim audit — dataset side: inventory and trace

The claim audit of task 9.16 (the Phase 9 exit audits; its spec `_dev/docs/spec/jioh/task-9.16-exit-audits.md`, decision 1: every claim traced to a slice read record, plus a blind re-read of a sample), for the workload dataset side, on the final repository at `928aa8fd` (branch `jioh/dataset-rebuild`), run 2026-10-17. The standard is phase spec decision 1 (`_dev/docs/spec/jioh/phase-9-workload-dataset-rebuild.md`): a claim taken from a source is verified when it is recorded with the verbatim passage, its locator and the copy read (URL or commit, version, date), and the repository's wording stays within the passage's object, unit, statistic, scope and population; a value no source states carries no source tag and is labelled convention, arithmetic, placeholder or design.

## Scope and method

- Files read for claims: `dataset/archetypes.yaml` (source tags, `category_source`, `modeling_notes`), `dataset/sources.yaml`, `dataset/grids.yaml`, `dataset/variants.yaml`, `dataset/timelines/coreset/*` (56 files), `dataset/README.md`, `docs/workload/*.md` (seven docs), and the `docs/references.md` entry (cite, role and status lines) of every id those files cite.
- Claim unit: one fact asserted about one source, with every location that states it; distinct wordings are quoted verbatim.
- Inventory and trace were run as five source groups in parallel (F1 to F5), plus two rows by the lead (X). Each group's record shorthands are defined in its part header below.
- Records accepted: the slices 9.4 (gaming) to 9.10 (scenarios and timelines) under `_dev/research/jioh/task-9.<n>-*/search/` and their `changelog.md` decisions, and, where a claim's record lives there, the 9.11 (scheduler-side constants), 9.12 (related-work prose), 9.15 (docs and memos sweep) and 9.19 (generator and the C3 grids) records and the persisted 2026-09-13 verification reads (`_dev/research/jioh/2026-09-13-verification/reads/`), each when it carries the verbatim passage, locator and copy.
- One rule applied across groups by the lead: a passage held only in a `docs/references.md` entry (the citation index) is not a slice read record. Ten claims fall under it (D-F5-01 to -05, -07, -08, -10; D-F4-33; D-F4-39) and are RECORD-BELOW-STANDARD, one shared finding (F-RBS-1 in `dataset-findings.md`).
- "Changed after read": the claim's own wording was committed after its record's read date (`git blame` of the primary line, then `git log -L` / `-S` to tell a wording change from a neighbouring edit).
- Merged rows: D-F5-18 duplicates D-F1-48 (the kernel task-name buffer length); D-F5-19 shares D-F1-49's root (no record of the v6.17 comment passage). Both are kept below for their locations and counted once.

## Verdict counts

| group | TRACED | WORDING-OUTSIDE-PASSAGE | RECORD-BELOW-STANDARD | NO-RECORD | LABELLED | claims |
|---|---|---|---|---|---|---|
| F1 — gaming (Steam, LAVD, game modes, flap-stress daemons, kernel task name) | 35 | 6 | 3 | 0 | 7 | 51 |
| F2 — interactive, typing, HCI and community benchmark tools | 42 | 3 | 0 | 0 | 2 | 47 |
| F3 — compile, background and IO | 38 | 3 | 2 | 1 | 2 | 46 |
| F4 — browser, comms, session, scenario benchmarks, bound programs | 38 | 4 | 2 | 2 | 5 | 51 |
| F5 — measurement method and statistics, runner, related work | 11 | 3 | 8 | 0 | 2 | 24 |
| X — the negative-result table, rows no group covered | 0 | 0 | 0 | 1 | 1 | 2 |
| **all** | **164** | **19** | **15** | **4** | **19** | **221** |

LABELLED: 19 claims; 5 of them carry a finding (label missing, inconsistent or of a kind decision 1 does not allow: D-F1-11, D-F3-08, D-F4-49, D-F5-11, D-X-02), the rest are present and honest. Claims with a finding: 43 (`dataset-findings.md`). Blind re-read sample: 133 claims (`dataset-blind-topics.md`).

## `meas-ci` values — listed, not audited here

The measurement audit (9.16 decision 2) covers them. Tags in the dataset files (`archetypes.yaml`, `grids.yaml`, the 43 timeline and variant files that carry one), by campaign (`meas-ci:<workflow>:<campaign launch date>`), occurrences: background 2026-09-19 (8), 2026-10-01 (25), 2026-10-02 (63), 2026-10-02b (9), 2026-10-03 (11), 2026-10-03b (8), 2026-10-03c (11), 2026-10-04 (10); build 2026-09-18 (24); desktop 2026-09-20 (36), 2026-10-04 (16), 2026-10-04b (13), 2026-10-05 (2), 2026-10-05b (14); interactive 2026-09-18 (23), 2026-09-19 (32), 2026-09-20 (42), 2026-09-25 (20), 2026-09-27 (28), 2026-10-05 (5); playback 2026-09-18 (5), 2026-09-20 (3); session 2026-09-24 (13). The workload docs carry further `meas-ci` mentions (archetype-plan 11 lines, building-plan 32, coreset-guide 54, scenario-catalog 20, measurement-overview 28, grounding-sources 3, source-vetting 3). Statements tagged `meas-ci` that describe third-party software (its threads, defaults, versions) were inventoried below where the groups found them.

## Index

Sample: `a` = wording changed after the read (LABELLED claims excluded: no source passage to re-read); `b (9.n)` = the seeded spot check for slice 9.n (seed 20261017, `random.Random(seed).sample` of two per slice over TRACED claims not in `a`, the slice being the first one the row names).

| id | source | object | verdict | record (first locator; shorthand per part header) | changed after read | sample |
|---|---|---|---|---|---|---|
| D-F1-01 | `lavd-ossna24` | identity of the LAVD talk and its slide deck | TRACED | R02:172-174 | yes | a |
| D-F1-02 | `lavd-ossna24` | number of tasks scheduled while a game runs | TRACED | 9.4-S1:55 | yes | a |
| D-F1-03 | `lavd-ossna24` | share of long-lived tasks | TRACED | 9.4-S1:55 | yes | a |
| D-F1-04 | `lavd-ossna24` | concentration of scheduling (top 30–40 tasks, system tasks, 15–20 game tasks) and the omission of the game's other threads | TRACED | 9.4-S1:55 | yes | a |
| D-F1-05 | `lavd-ossna24:s12` (label: design within a source range) | chain length 16 as a point inside 15–20 | LABELLED | 9.4-S1:55 | no |  |
| D-F1-06 | `lavd-ossna24:s13` | per-schedule runtimes and the two named examples | TRACED | 9.4-S1:56 | yes | a |
| D-F1-07 | none (label: ours) | lognormal family, p05/p95 reading, one draw per member | LABELLED | 9.4 changelog D6 (label decision) | no |  |
| D-F1-08 | `lavd-ossna24:s13` | task execution time stable and predictable by its average | TRACED | 9.4-S1:56 | yes | a |
| D-F1-09 | `lavd-ossna24:s13` | slide 13's runtime plot (one game, ~128 tasks, median ~0.04 ms) | TRACED | 9.4-S2:95 | no | b (9.4) |
| D-F1-10 | `lavd-ossna24:s14` | what initiates scheduling: waiting system calls vs preemption, and the pie's sched_preempt share | TRACED | 9.4-S1:57 | yes | a |
| D-F1-11 | `lavd-ossna24:s14` (a derived figure) | "about 1.4 schedules per wake" attributed to slide 14 | LABELLED | 9.4-S2:93 | yes |  |
| D-F1-12 | `lavd-ossna24` (attributed) | "the deck's slice example 1.5 ms" | WORDING-OUTSIDE-PASSAGE | R02:91-93 | yes | a |
| D-F1-13 | `lavd-ossna24:s16` | the waiter–waker graph and its thread names (slide 16) | TRACED | 9.4-S2:91 | yes | a |
| D-F1-14 | `lavd-ossna24:s16` (attributed) | the six chain members named `Troy.exe` under the slide-16 tag | WORDING-OUTSIDE-PASSAGE | 9.4-S2:91 | yes | a |
| D-F1-15 | `lavd-ossna24:s11`, `s16` | the graph's shapes and wineserver's edges | TRACED | 9.4-S2:91 | no |  |
| D-F1-16 | `lavd-ossna24:s17` | a sequence of tasks serves one job; most game tasks periodic | TRACED | 9.4-S1:60 | yes | a |
| D-F1-17 | `lavd-ossna24` | the deck states no frame period or frame budget; its 15 ms is a targeted latency | TRACED | R02:91-97 | yes | a |
| D-F1-18 | `lavd-ossna24` | traces collected while playing games; game and machine unnamed | TRACED | 9.4-S1:53 | yes | a |
| D-F1-19 | `lavd-ossna24` (attributed) | the deck's traces collected with `perf sched record` | WORDING-OUTSIDE-PASSAGE | 9.4-S1:53 | yes | a |
| D-F1-20 | `lavd-ossna24` | the deck's figures draw on at least three process trees | TRACED | 9.4-S2:98 | no | b (9.4) |
| D-F1-21 | none tagged (scx issues #234, #296; stated "not a source her | public scx_lavd logs of four other games show tens of µs per schedule | TRACED | 9.4-S3:49 | no |  |
| D-F1-22 | none tagged (Proton README; runner docs) | why no runner measurement referees the chain: no GPU, Proton only under Steam | WORDING-OUTSIDE-PASSAGE | 9.4-S4:262 | no |  |
| D-F1-23 | none tagged (Wine source) | Wine calls are a request write and a blocking reply read | TRACED | 9.4-S2:211-212 | no |  |
| D-F1-24 | `steamos-refresh` | Steam Deck LCD default refresh and frame-limit setting | TRACED | 9.4-S2:162-167 | no |  |
| D-F1-25 | `steamos-refresh` (label: design + arithmetic) | frame period 16,667 µs: display-paced design, 1/60 s arithmetic | LABELLED | task-9.4-gaming/changelog.md:11 | no |  |
| D-F1-26 | `steam-downloads` | Steam's download check box and the default pause at game launch | TRACED | R07:141-160 | yes | a |
| D-F1-27 | `steam-downloads` | the per-game download setting attributed to FAQ 4F9E | WORDING-OUTSIDE-PASSAGE | R07:161-169 | yes | a |
| D-F1-28 | `steam-downloads` | Steam's automatic update queue | TRACED | R07:163 | yes | a |
| D-F1-29 | `steam-for-linux-8821` | a user-started install proceeds at once during play (issue #8821) | TRACED | 9.10-S3:474-480 | yes | a |
| D-F1-30 | `steamos-lavd` | SteamOS 3.8 adds LAVD as a user-selected scheduler, not enabled by default | TRACED | 9.12-S2:266 | yes | a |
| D-F1-31 | `steamos-lavd`, `scx` | Valve sponsors LAVD | TRACED | 9.12-S2:188 | yes | a |
| D-F1-32 | `scx` | scx_lavd motivated by gaming, to reduce stuttering; pinned at v1.1.3 | TRACED | 9.12-S2:186 | yes | a |
| D-F1-33 | `corbet-lwn24` | Corbet's LWN report of the LPC 2024 talks | TRACED | 9.12-S2:226-238 | yes | a |
| D-F1-34 | `edge-lwn26` | Edge's LWN report of Min's LPC 2025 session | TRACED | 9.12-S2:241-252 | yes | a |
| D-F1-35 | `dai-lpc25` | Meta's speakers present scx_lavd as a candidate default fleet scheduler | TRACED | 9.12-S2:220 | yes | a |
| D-F1-36 | `gamemode-docs` | Windows Game Mode: the category and Microsoft's documented design | TRACED | 9.12-S2:277 | yes | a |
| D-F1-37 | `gamemode-docs` | `SetProcessDefaultCpuSets` is not an `<expandedresources.h>` function | TRACED | K3:108 | yes | a |
| D-F1-38 | `xbox-gamemode` | Game Mode holds back Windows Update driver installs and restart notifications | TRACED | 9.12-S2:607 | yes | a |
| D-F1-39 | `apple-gamemode` | macOS Game Mode's documented behaviour | TRACED | 9.12-S2:287-296 | yes | a |
| D-F1-40 | `feral-gamemode` | Feral GameMode's request model and the `[filter]` whitelist | TRACED | 9.12-S2:299-312 | yes | a |
| D-F1-41 | `feral-gamemode` | GameMode's 5 s reaper interval | TRACED | 9.19-P:18 | no |  |
| D-F1-42 | `tuned` | tuned's 10 s dynamic-tuning update interval | TRACED | 9.19-P:17 | no |  |
| D-F1-43 | `tuned` | tuned entry's further quotations | RECORD-BELOW-STANDARD | 9.19-P:17 | no |  |
| D-F1-44 | `systemd-oomd` | systemd-oomd's 30 s pressure duration and the 60 % / 10 s limit | TRACED | 9.19-P:19 | no |  |
| D-F1-45 | `systemd-oomd` | systemd-oomd entry's further quotation | RECORD-BELOW-STANDARD | 9.19-P:19 | no |  |
| D-F1-46 | `feral-gamemode`, `tuned`, `systemd-oomd` | the flap-stress intervals called the three daemons' "debounce" values | WORDING-OUTSIDE-PASSAGE | 9.19-P:17-19 | yes | a |
| D-F1-47 | none (label: design) | 2 s flap-stress interval | LABELLED | task-9.19-generator-and-the-c3-grids/changelog.md:25 | no |  |
| D-F1-48 | `linux-sched-h` | Linux process names are at most 15 characters | TRACED | 9.10-S4:1500 | yes | a |
| D-F1-49 | `linux-sched-h` | the linux-sched-h cite's quotations "at v6.17", read 2026-10-12 | RECORD-BELOW-STANDARD | 9.10-S4:1500 | n |  |
| D-F1-50 | none (label: design) | lane_share values in the gaming files | LABELLED | task-9.4-gaming/changelog.md:22 | n |  |
| D-F1-51 | none (label: design), except `comm_limit` and three interval | the grid definition's own values | LABELLED | task-9.20-c4-and-c5-grids/changelog.md:64 | n |  |
| D-F2-01 | `swell-icmi14` | SWELL-KW population, setting and size | TRACED | 910S3:214 | yes | a |
| D-F2-02 | `swell-icmi14` | SWELL-KW log content: per-keystroke timestamps with focused application, pointer as click/drag/wheel only | TRACED | 95S3:256-262 — `<ControlApplication>iexp | yes | a |
| D-F2-03 | `swell-icmi14` | SWELL-KW licence and access | TRACED | R10:240 | yes | a |
| D-F2-04 | `swell-icmi14:outlook-c23` (also `word-c1`, `ie-c1`) | Which SWELL-KW blocks each replayed stream comes from | WORDING-OUTSIDE-PASSAGE | 910S3:234 | no |  |
| D-F2-05 | `swell-icmi14` | SWELL-KW timestamps quantised at the 15.6 ms Windows tick | TRACED | 95CL:63 (D12) — "timestamps quantised at | no |  |
| D-F2-06 | `swell-icmi14` | SWELL-KW focus-sequence figures (dwell median 9.1 s, A → B → A returns 83.4 %) | TRACED | 910S3:244 | yes | a |
| D-F2-07 | `dhakal-chi18` | 136M Keystrokes data artifact: file, fields, rows, licence | TRACED | readme.txt:21 | yes | a |
| D-F2-08 | `dhakal-chi18` | 136M Keystrokes paper figures and population | TRACED | R08:45-46 | yes | a |
| D-F2-09 | `dhakal-chi18` / `swell-icmi14` | Gap shares: 136M sample 0.7 % over 1 s vs SWELL-KW Word stream 5.5 % | TRACED | 95S3:86 — "Within-sentence press-to-pres | yes | a |
| D-F2-10 | `gonzalez-chi04` | González & Mark 2004: ~3 min per event, its unit and scope | TRACED | R10:89 | yes | a |
| D-F2-11 | `gonzalez-chi04` | González & Mark 2004: 11 min 28 s mean working-sphere segment and its companions | TRACED | R10:74 | yes | a |
| D-F2-12 | `gonzalez-chi04` | González & Mark 2004: spheres per day, time per tool, statistics, population | WORDING-OUTSIDE-PASSAGE | R10:83 | yes | a |
| D-F2-13 | `gonzalez-chi04` (value); design (the rest) | c6-dual's focus alternation: 688 s, and the parts labelled design | LABELLED | R10:74 | yes |  |
| D-F2-14 | `mark-chi05` | Mark, González & Harris 2005: ~11 min per sphere segment, informants | TRACED | R10:136 | yes | a |
| D-F2-15 | `mark-chi05` | Mark et al. 2005: internal/external interruption split and the Table 3 inconsistency | TRACED | R10:147 | yes | a |
| D-F2-16 | `mark-chi05`; untagged (the 2006 Gallup interview; CHI 2008  | Same-day resumption (CHI 2005) and the 23 min 15 s figure | TRACED | R10:222 | yes | a |
| D-F2-17 | `czerwinski-chi04` | Czerwinski, Horvitz & Wilhite 2004: what the study is | TRACED | R10:209 | yes | a |
| D-F2-18 | `roeser-rw24` | Roeser et al.: task, sample, model and Table 3 values | TRACED | R08:226 | yes | a |
| D-F2-19 | `killourhy-dsn09` | CMU keystroke benchmark (Killourhy & Maxion): what the dataset is | TRACED | 95S3:131-147 — "51 subjects (typists), e | no | b (9.5) |
| D-F2-20 | `behacom-dib20` | BEHACOM: users, platforms, period, fields, deposit | TRACED | 910S3:292 | yes | a |
| D-F2-21 | `focal-arxiv26` | DesktopBench: sessions composed from templates, the A → B → A split, session counts | TRACED | 910S3:325 | yes | a |
| D-F2-22 | `focal-arxiv26` | DesktopBench release: fixed 6.0 s per action, HuggingFace v0.1.0, terms, preprint | TRACED | R11F:344 — `scripts/prepare_videogui_raw | yes | a |
| D-F2-23 | `interbench` | interbench pin, version and licence | TRACED | R01:9 | yes | a |
| D-F2-24 | `interbench` | interbench: what it emulates and measures | TRACED | R01:106 | no |  |
| D-F2-25 | `interbench` | interbench's interactive constants and the Video wording | TRACED | R01:57 | yes | a |
| D-F2-26 | `interbench` | interbench: missed-period handling (cited for the TIMER memo) | TRACED | 911S2:649-667 | yes | a |
| D-F2-27 | `interbench` | interbench Burn default and the ~7 ms jitter figure | TRACED | R01:127-136 | yes | a |
| D-F2-28 | `interbench`; LWN 725238 and 1051430 (untagged here) | interbench packaging and usage precedents | TRACED | R01:272 | yes | a |
| D-F2-29 | `interbench` | interbench's Burn/Write/Read/Memload/Hack/Custom loads as the vetting body lists them (left standing) | WORDING-OUTSIDE-PASSAGE | R01:150 | no |  |
| D-F2-30 | `rt-app` | rt-app pin and licence | TRACED | 911S2:614 | no |  |
| D-F2-31 | `rt-app` | rt-app's JSON task model as the schema precedent | TRACED | R01:307-313 | no |  |
| D-F2-32 | `rt-app`; LWN 725238 (untagged) | rt-app users and documentation references | TRACED | R01:407 | yes | a |
| D-F2-33 | `schbench` | schbench pin, authorship and licence | TRACED | 911S2:728 | yes | a |
| D-F2-34 | `schbench` | schbench's printed percentiles and its request | TRACED | 911S2:733-736 | yes | a |
| D-F2-35 | `schbench` (the SchedCP reference list) | SchedCP cites schbench at kernel.googlesource.com | TRACED | R03:218 | yes | a |
| D-F2-36 | `hackbench` | hackbench pin, purpose, defaults and output | TRACED | 911S2:749-755 | yes | a |
| D-F2-37 | `hackbench` (LWN 725238, untagged) | LWN on hackbench | TRACED | R01:440 | yes | a |
| D-F2-38 | `stress-ng` | stress-ng pin, licence, `--workload`, `--cyclic`, README disclaimer | TRACED | 911S2:759-766 | yes | a |
| D-F2-39 | `ananicy` | Ananicy and ananicy-cpp: status, licences, versions, self-description, fields, lineage | TRACED | 912S2:387-389 | yes | a |
| D-F2-40 | `ananicy` | ananicy-cpp's rule lookup key | TRACED | 912A:229-237 | yes | a |
| D-F2-41 | `cachyos-settings` | CachyOS installs and enables ananicy-cpp with the catalogue | TRACED | 912S2:481-499 | yes | a |
| D-F2-42 | `ananicy-rules` | The CachyOS catalogue at `03ef03fb`: counts, types, values, maintainers | TRACED | R06:338-450 | yes | a |
| D-F2-43 | `ananicy-rules` | What the catalogue holds for audio, indexers and compilers; no wanted/unwanted distinction | TRACED | R06:37 | yes | a |
| D-F2-44 | `ananicy-rules` (with `ananicy`'s lookup key) | How much of the core set the shipped catalogue keys | TRACED | 912A:240-246 | yes | a |
| D-F2-45 | `darpa-optc` | DARPA OpTC: what its release documents | TRACED | README.md:12 | yes | a |
| D-F2-46 | `carat-top1000` | Carat: several running apps per sample | TRACED | R11P:290 "processName (App Android packa | yes | a |
| D-F2-47 | `dhakal-chi18`, `swell-icmi14`; labels | The 136M Keystrokes check's role and the typing entries' stimulus labels | LABELLED | 95CL:93 (D18), 95CL:21 (D4); the gap rul | n |  |
| D-F3-01 | `ocallahan-atc17` | the build workload behind O'Callahan et al.'s process count | TRACED | 2026-09-13-verification/reads/R03-build-papers.md:42 | yes | a |
| D-F3-02 | `ocallahan-atc17` | what the O'Callahan count grounds: "compiler children" | WORDING-OUTSIDE-PASSAGE | R03-build-papers.md:50 | yes | a |
| D-F3-03 | `coetzee-arxiv12` | Coetzee et al. on the Linux kernel build's short-lived processes | TRACED | R03-build-papers.md:104 | yes | a |
| D-F3-04 | `coetzee-arxiv12` | the reach of Coetzee's corroboration | WORDING-OUTSIDE-PASSAGE | R03-build-papers.md:104 | yes | a |
| D-F3-05 | `schedcp-mlsys25` (related-work id; untagged compile claim i | SchedCP's kernel-compilation workload and its "short-lived processes" | TRACED | R03-build-papers.md:149 | yes | a |
| D-F3-06 | `ocallahan-atc17`, Linux kernel v6.6 (untagged) | the source-vetting correction of the kernel-build row (sambatest, kernel docs, autogroup) | TRACED | R03-build-papers.md:50 | yes | a |
| D-F3-07 | GNU make 4.4.1, dkms (untagged; 9.6 D4's reads) | the build tools' documented default parallelism | WORDING-OUTSIDE-PASSAGE | task-9.6-compile/search/S2-project-docs.md:407 | yes | a |
| D-F3-08 | none (labelled value) | `parallelism_cap` 8 (the make build's job cap) | LABELLED | task-9.6-compile/changelog.md:21 | yes |  |
| D-F3-09 | GNU make 4.4.1 (untagged) | make's jobserver counts jobs, not processes | TRACED | task-9.6-compile/search/S2-project-docs.md:618 | no | b (9.6) |
| D-F3-10 | Brendan Gregg, "perf Examples" (untagged) | Gregg's perf sched capture as corroboration of role weights | TRACED | task-9.6-compile/search/S3-traces-datasets.md:51-57 | no |  |
| D-F3-11 | Linux v6.6 kbuild, GCC 13 (untagged) | the kernel's Makefile passes no `-pipe`, so `cc1` and `as` run in sequence | RECORD-BELOW-STANDARD | task-9.6-compile/changelog.md:51 | no |  |
| D-F3-12 | `liu-jacm73` | Liu and Layland's deadline at the next request | TRACED | task-9.12-related-work-prose/search/S1-literature.md:237 | no |  |
| D-F3-13 | `meyer-fast11` | Meyer and Bolosky's 30 MB half of bytes | TRACED | task-9.7-background-io/search/T9-S1-literature.md:234 | yes | a |
| D-F3-14 | `fm-results-tables` | the GNU/Linux users' median file size, 4.60 KB | TRACED | task-9.7-background-io/search/T9-S3-datasets.md:298 | yes | a |
| D-F3-15 | `vrable-fast09` | Cumulus's personal-machine daily change rates, seven days | TRACED | task-9.7-background-io/search/T9-S1-literature.md:563 | yes | a |
| D-F3-16 | `deja-dup` | how Déjà Dup's monitor starts the scheduled backup | TRACED | task-9.10-scenarios-timelines/search/S2-project-docs.md:3940 | yes | a |
| D-F3-17 | `deja-dup`, `duplicity` | what every Déjà Dup backup runs | TRACED | S2-project-docs.md:3940 | no |  |
| D-F3-18 | `deja-dup` | Déjà Dup's defaults (weekly once turned on, encryption on, 200 MB volumes, password not remembered) | TRACED | S2-project-docs.md:3940 | yes | a |
| D-F3-19 | `deja-dup`, `ubuntu-desktop-manifest` | Déjà Dup is in Ubuntu 24.04's extended install, not the default | TRACED | S2-project-docs.md:3962 | yes | a |
| D-F3-20 | `deja-dup` | the two-monthly restore test | TRACED | S2-62 — "with a fresh cache and no saved | no |  |
| D-F3-21 | systemd 255.4, tracker-miners 3.7.1, deja-dup 45.2, gnome-se | the CPU groups the indexer and the backup run in on the depicted desktop | TRACED | task-9.11-scheduler-constants/changelog.md:216-224 | yes | a |
| D-F3-22 | `apt` | how the stock unattended upgrade starts (apt's units) | TRACED | task-9.10-scenarios-timelines/search/S2-project-docs.md:326 | no | b (9.10) |
| D-F3-23 | `unattended-upgrades`, `ubuntu-desktop-manifest` | unattended-upgrades is in the default install and enabled by default | TRACED | S2-project-docs.md:346-348 | yes | a |
| D-F3-24 | `glibc` | the update the upgrade installs (glibc, 2026-07-27, four binaries) | TRACED | S2-project-docs.md:3627-3629 | yes | a |
| D-F3-25 | Ubuntu's security pocket (S3-58; reader's own computation) | the pending-set day rule (median working day) | TRACED | task-9.10-scenarios-timelines/changelog.md:763-765 | no |  |
| D-F3-26 | `glibc` | what glibc's maintainer scripts run (18 English locales; chroot skips) | TRACED | S2-project-docs.md:3627 | no |  |
| D-F3-27 | `apt` (apt-helper) | the unit's wait-online step | TRACED | S2-project-docs.md:3651 | no |  |
| D-F3-28 | `dkms` | DKMS's kernel hooks and the build's `nproc` | TRACED | S2-project-docs.md:1053 | yes | a |
| D-F3-29 | `nvidia-open-kernel-modules` | the module: NVIDIA's 595 open module, production branch, five modules | TRACED | S2-project-docs.md:3659 | yes | a |
| D-F3-30 | Ubuntu archive (S3-60, S2-33; untagged) | the kernels: 7.0.0-34 published to security 2026-09-23; HWE 7.0.0-31 added by the installer | TRACED | task-9.10-scenarios-timelines/changelog.md:932 | yes | a |
| D-F3-31 | DKMS / Ubuntu's Secure Boot route (untagged) | module signing on a Secure Boot desktop | NO-RECORD | task-9.10-scenarios-timelines/search/S2-project-docs.md:3512 | no |  |
| D-F3-32 | `ubuntu-desktop-manifest`, `tracker-miners` | Tracker 3.7.1 in the default install | TRACED | S2-project-docs.md:3734 | yes | a |
| D-F3-33 | `tracker-miners` | Tracker's shipped behaviour (initial sleep, extractor deadline and restart, reset, user unit) | TRACED | S2-project-docs.md:3734 | no |  |
| D-F3-34 | `tracker-miners` | Tracker's threads declare SCHED_IDLE at nice 19 | TRACED | task-9.6-compile/changelog.md:95 | no | b (9.6) |
| D-F3-35 | `handbrake` | HandBrake 1.7.2's default preset and its settings | RECORD-BELOW-STANDARD | task-9.10-scenarios-timelines/search/S2-project-docs.md:3879-3886 | yes | a |
| D-F3-36 | `handbrake` | HandBrakeCLI as Ubuntu 24.04 packages it | TRACED | S2-project-docs.md:3887 | yes | a |
| D-F3-37 | `big-buck-bunny` | Big Buck Bunny's 4K 30 fps edition | TRACED | S2-project-docs.md:3858 | no |  |
| D-F3-38 | `cpsmarkplus` | CpsMark+'s HandBrake workload: H.264 to a 1080p "2K" | TRACED | S2-project-docs.md:3903 | yes | a |
| D-F3-39 | `cpsmarkplus`, `cpsmark-tbench23` | CpsMark+'s source has no licence | TRACED | 2026-09-13-verification/reads/R04-cpsmark.md:284-300 | yes | a |
| D-F3-40 | `steam-download-stats` | the shaped link's rate, 121.0 Mbps | TRACED | task-9.7-background-io/changelog.md:61 | yes | a |
| D-F3-41 | SteamCMD (untagged; 9.7 D4) | SteamCMD, its anonymous depot and the desktop client's account | TRACED | task-9.7-background-io/changelog.md:27 | no |  |
| D-F3-42 | Ubuntu `7zip` / `p7zip-full` (untagged) | 7-Zip 23.01 is Ubuntu 24.04's `7z`, at its default format and level | TRACED | task-9.7-background-io/changelog.md:49 | no | b (9.7) |
| D-F3-43 | `ubuntu-desktop-manifest` | what Ubuntu 24.04's desktop image holds (the package rule) | TRACED | task-9.9-daemons-session/changelog.md:444 | no |  |
| D-F3-44 | Jellyfin 12.0, Plex Media Server 1.43.4 (untagged; 2026-09-1 | no distro or vendor starts an ML-training, render or transcode job unasked; the transcoders' names | TRACED | 2026-09-13-verification/reads/R11-focal-plain.md:1538-1652 | yes | a |
| D-F3-45 | dpkg 1.22.6ubuntu6.6; a Mint 22.1 journal (untagged; 9.10 D9 | the one unasked backup under its own name, dpkg's daily database backup | TRACED | task-9.10-scenarios-timelines/changelog.md:165 | no |  |
| D-F3-46 | none (labelled values) | design and arithmetic labels in the compile, backup, indexing and transcode timelines | LABELLED | task-9.10-scenarios-timelines/changelog. | n |  |
| D-F4-01 | `cpsmark-tbench23` | what CpsMark+ calls its usage scenarios, and which applications each one runs | TRACED | R04:23-30 | yes | a |
| D-F4-02 | `cpsmark-tbench23` | whether CpsMark+ includes an archiving workload, and what it works on | TRACED | R04:130 | yes | a |
| D-F4-03 | `cpsmark-tbench23` | CpsMark+'s modules, its user-profile table and its application table | TRACED | R04:29-30 | no |  |
| D-F4-04 | `cpsmark-tbench23` | the user-behaviour stages of CpsMark+'s CA workflow, cited only for the existence of the transitions between them | TRACED | R04:143 | yes | a |
| D-F4-05 | `cpsmark-tbench23` | the order of CpsMark+'s CC module (photo editing, then video, then transcode) and whether any workload's output feeds the next | TRACED | R04:427 | yes | a |
| D-F4-06 | `cpsmark-tbench23` | CpsMark+'s hardware sensitivity: the graphics-card figure for each module | TRACED | R04:237 | yes | a |
| D-F4-07 | `cpsmark-tbench23` | CpsMark+'s target operating system, whether it has a gaming scenario, and whether it times processes | TRACED | R04:257 | no |  |
| D-F4-08 | `cpsmark-tbench23` | which benchmarks CpsMark+ compares itself against | TRACED | R04:339 | no |  |
| D-F4-09 | `cpsmark-tbench23` | how CpsMark+ serves its browsing workload's pages, and what the pages contain (the input of the Chrome page-load operation) | TRACED | 9.5-S7:38 | no |  |
| D-F4-10 | `cpsmark-tbench23` | CpsMark+'s mail workload: what it attaches and whether it replies (the input of the Thunderbird send operation) | TRACED | R04:113 | no |  |
| D-F4-11 | `cpsmark-tbench23` | CpsMark+'s bibliographic details | TRACED | R04:449 | no |  |
| D-F4-12 | `pcmark10` | PCMark 10's test groups and the workloads in each | TRACED | R05:37-43 | no |  |
| D-F4-13 | `pcmark10` | the application PCMark 10's Writing workload runs | TRACED | 9.5-S7:43 | no | b (9.5) |
| D-F4-14 | `pcmark10` | whether PCMark 10's guide documents per-task or per-process timing | TRACED | R05:150-157 | yes | a |
| D-F4-15 | `pcmark10` | what PCMark 10's video-playback battery test is, and where it sits in the product | WORDING-OUTSIDE-PASSAGE | R05:110 | yes | a |
| D-F4-16 | `pcmark10` | the inputs PCMark 10 gives its photo, video and browsing workloads (image size and filter, clip and sharpening, page kinds) | TRACED | 9.5-S7:21 | no |  |
| D-F4-17 | `pcmark10` | which edition of PCMark 10's guide was read, and the online guide that replaced it | TRACED | R05:10-11 | no |  |
| D-F4-18 | `sysmark30` | SYSmark 30's four scenarios and what each one models | TRACED | R05:165-170 | yes | a |
| D-F4-19 | `sysmark30` | the applications SYSmark 30 names for each scenario (used for the scenario catalog's Windows → Linux rows) | TRACED | R05:218-223 | yes | a |
| D-F4-20 | `sysmark30` | SYSmark 30's archiving workload | TRACED | R05:181-185 | yes | a |
| D-F4-21 | `sysmark30` | whether SYSmark 30 runs photo editing beside a background video encode, and whether it keeps Outlook open through the office scenario | WORDING-OUTSIDE-PASSAGE | R05:206 | yes | a |
| D-F4-22 | `sysmark30` | which copy of SYSmark 30's user guide was read, and when | NO-RECORD | R05:12 | n |  |
| D-F4-23 | `sysmark25` | whether SYSmark 25 includes code compilation, and in what form | TRACED | R05:319 | yes | a |
| D-F4-24 | `sysmark25` | which SYSmark versions define Productivity, Creativity and Responsiveness | TRACED | R05:342-370 | yes | a |
| D-F4-25 | `sysmark25` | which copy of SYSmark 25's user guide was read | TRACED | R05:15 | no |  |
| D-F4-26 | `procyon` | how many benchmarks UL Procyon lists, and how many of them run AI inference locally | WORDING-OUTSIDE-PASSAGE | R05:414-421 | yes | a |
| D-F4-27 | `procyon` | the applications behind Procyon's office, photo and video benchmarks | TRACED | R05:431-440 | yes | a |
| D-F4-28 | `teams-pwa-linux` | how Microsoft Teams runs on Linux | TRACED | 9.10-S2:3383-3389 | no |  |
| D-F4-29 | `glam` | what Firefox's tab-count telemetry probe measures, and the population GLAM serves | TRACED | 9.10-S3:639 | yes | a |
| D-F4-30 | `glam` | the Linux median per-client peak of open tabs and of open windows in Firefox release 152 | TRACED | 9.10-S3:647-651 | yes | a |
| D-F4-31 | `glam` | whether Firefox's telemetry counts tabs per window | WORDING-OUTSIDE-PASSAGE | 9.10-S3:639 | yes | a |
| D-F4-32 | `glam` | whether Firefox's tab count stands for Chrome's, and how 4.67 becomes five | LABELLED | changelog.md:291 | n |  |
| D-F4-33 | `glean` | when Glean's metrics-ping thread wakes in Thunderbird | RECORD-BELOW-STANDARD | _dev/research/jioh/task-9.5-interactive-typing/changelog.md:753 | no |  |
| D-F4-34 | `mahoney-10gb` | what Matt Mahoney's 10 GB benchmark set holds and where it came from | TRACED | _dev/research/jioh/task-9.7-background-io/search/T9-S2-project-docs.md:339 | no | b (9.7) |
| D-F4-35 | `hippocamp` | HippoCamp's Bei profile: the revision, the file count and how the profile was built | TRACED | 9.10-S3:937-942 | no |  |
| D-F4-36 | `pytorch-examples` | PyTorch's Basic MNIST example: its commit, how it is run and its defaults | TRACED | 9.10-S2:3617-3622 | yes | a |
| D-F4-37 | `kdenlive` | how Kdenlive 23.08.5 exports: the processes it starts and its default render profile | TRACED | 9.10-S2:3916-3922 | yes | a |
| D-F4-38 | `mlt` | what melt's progress loop does between progress reports | TRACED | 9.10-S2:3936 | no |  |
| D-F4-39 | `systemd-ubuntu`, `netplan`, `livecd-rootfs` | whether a stock Ubuntu 24.04 desktop runs `systemd-networkd` | RECORD-BELOW-STANDARD | _dev/research/jioh/task-9.9-daemons-session/changelog.md:341-349 | no |  |
| D-F4-40 | none tagged (vendor source code cited in the 9.9 search reco | GNOME's default idle delay, and what the session does when it is reached | TRACED | 9.9-S2:348 | no | b (9.9) |
| D-F4-41 | none (ours) | mapping the benchmarks' Windows applications to Linux programs | LABELLED | none | n |  |
| D-F4-42 | none tagged (measurement and Mutter's source) | whether the Ubuntu 24.04 GNOME 46 session at idle runs an X server | TRACED | _dev/research/jioh/task-9.9-daemons-session/changelog.md:196 | no | b (9.9) |
| D-F4-43 | none tagged (Chromium source cited in the 9.8 search record) | how long Chromium waits before it throttles a background page's timer wake-ups, by default | TRACED | 9.8-S2:157 | no | b (9.8) |
| D-F4-44 | none tagged (Chromium documentation) | how Chromium on desktop Linux assigns renderer processes to pages | TRACED | 9.8-S2:77 | no |  |
| D-F4-45 | none tagged (Chromium source) | whether Chromium on Linux marks a window covered by another application as occluded | TRACED | 9.8-S2:487-493 | yes | a |
| D-F4-46 | none tagged (the Matrix spec and matrix-js-sdk) | how long an idle Matrix client's `/sync` request waits | TRACED | 9.8-S2:270 | no | b (9.8) |
| D-F4-47 | none tagged | what Chromium's `HangWatcher` thread does | NO-RECORD | changelog.md:222 | n |  |
| D-F4-48 | none tagged (Qt source) | how Qt Quick's threaded render loop paces frames | TRACED | _dev/research/jioh/task-9.5-interactive-typing/search/S8-display-gpu.md:30 | no |  |
| D-F4-49 | none (design) | the order of the evening arc (browsing → gaming → media playback) | LABELLED | none | n/a |  |
| D-F4-50 | none (design) | the other design labels in the F4 timelines and their variant recipes | LABELLED | none | n/a |  |
| D-F4-51 | none external, except `lavd-ossna24` s14 on chain-x1.2 (F1's | the factors and lengths of the sensitivity variants | LABELLED | none | n/a |  |
| D-F5-01 | `maricq-osdi18` | whether machines of one nominal type give different results run to run | RECORD-BELOW-STANDARD | docs/references.md:124 | no |  |
| D-F5-02 | `maricq-osdi18` | what interval the paper recommends | RECORD-BELOW-STANDARD | docs/references.md:124 | no |  |
| D-F5-03 | `kalibera-ismm13` | at which level repetition is done and the interval taken | RECORD-BELOW-STANDARD | docs/references.md:119 | no |  |
| D-F5-04 | `kalibera-ismm13` | whether the count is set on-line, and the smallest count | RECORD-BELOW-STANDARD | _dev/research/jioh/task-9.6-compile/campaign/method.md:71 | no |  |
| D-F5-05 | `georges-oopsla07` | the paper's construction: interval over runs, runs added to a precision | RECORD-BELOW-STANDARD | docs/references.md:114 | no |  |
| D-F5-06 | `georges-oopsla07`, `kalibera-ismm13` | whether the stopping rule has a ceiling (the row's ground column) | WORDING-OUTSIDE-PASSAGE | _dev/research/jioh/task-9.5-interactive-typing/changelog.md:204 | no |  |
| D-F5-07 | `cochran-st77` | the half-width of a count-weighted mean over repeats | RECORD-BELOW-STANDARD | docs/references.md:134 | no |  |
| D-F5-08 | `cochran-st77` | the ratio variance as a large-sample result | RECORD-BELOW-STANDARD | docs/references.md:134 | no |  |
| D-F5-09 | `chow-aoms65` | what stopping at the first passing count guarantees | WORDING-OUTSIDE-PASSAGE | docs/references.md:129 | no |  |
| D-F5-10 | `feller-ipta50` | the standard error of a compiled wake count | RECORD-BELOW-STANDARD | docs/references.md:139 | no |  |
| D-F5-11 | none (values no source states) | the compile-fidelity tolerances | LABELLED | docs/references.md:139 | n |  |
| D-F5-12 | none (convention) | the stability tolerance and floor as the project's rule | LABELLED | _dev/research/jioh/task-9.6-compile/campaign/method.md:69 | n |  |
| D-F5-13 | `liu-jacm73` | a periodic job's deadline at its next request | TRACED | _dev/research/jioh/task-9.12-related-work-prose/search/S1-literature.md:237 | no |  |
| D-F5-14 | `fqcodel-rfc18` | what the RFC grounds for the download's queue | WORDING-OUTSIDE-PASSAGE | docs/references.md:144 | no |  |
| D-F5-15 | `gh-artifact-retention` | how long GitHub keeps a workflow's artifacts | TRACED | _dev/research/jioh/task-9.15-docs-memos-and-guidebook-corrections/logs/K01.md:89 | no |  |
| D-F5-16 | `gh-hosted-runners` | the standard Linux runner's CPU count and storage | TRACED | _dev/research/jioh/task-9.10-scenarios-timelines/search/S4-ci-observability.md:225-231 | no |  |
| D-F5-17 | `gh-actions-limits` | the job execution-time limit | TRACED | _dev/research/jioh/task-9.10-scenarios-timelines/search/S4-ci-observability.md:278 | no |  |
| D-F5-18 | `linux-sched-h` | the kernel's task-name buffer length at v6.17 | TRACED (merged) | _dev/research/jioh/task-9.10-scenarios-timelines/search/S4-ci-observability.md:1499-1500 | no |  |
| D-F5-19 | `linux-sched-h` | the name NUL-terminated and padded, so at most 15 characters, at v6.17 | RECORD-BELOW-STANDARD (merged) | _dev/research/jioh/task-9.10-scenarios-timelines/search/S2-project-docs.md:1786-1787 | no |  |
| D-F5-20 | Linux kernel source (no id; 9.10 D25 rule) | how a process's `comm` is derived (basename cut, scripts, renames) | TRACED | _dev/research/jioh/task-9.10-scenarios-timelines/search/S2-project-docs.md:1719-1800 | no |  |
| D-F5-21 | Ubuntu kernel package (no id in the doc) | Ubuntu 24.04's desktop kernel transparent-hugepage default | TRACED | _dev/research/jioh/task-9.10-scenarios-timelines/search/S2-project-docs.md:3834-3838 | no | b (9.10) |
| D-F5-22 | SchedCP (`schedcp-mlsys25`, docs/references.md:816, related  | SchedCP's kernel-compilation workload and its reported gain | TRACED | _dev/research/jioh/2026-09-13-verification/reads/R03-build-papers.md:149 | yes | a |
| D-F5-23 | SchedCP (related work only; untagged) | where SchedCP's "short-lived processes" comes from | TRACED | R03-build-papers.md:159 | yes | a |
| D-F5-24 | SchedCP (related work only; untagged) | that SchedCP cites schbench, and how | TRACED | R03-build-papers.md:218 | yes | a |
| D-F5-25 | SchedCP (related work only; untagged) | SchedCP's venue | TRACED | R03-build-papers.md:224-226 | no |  |
| D-F5-26 | SchedCP (related work only; untagged) | what SchedCP says about the completeness of its benchmark | TRACED | R03-build-papers.md:236-238 | no |  |
| D-X-01 | none tagged (Azure traces, Google cluster traces, "VDI chara | what enterprise, VDI and cloud workload traces record about processes | NO-RECORD | _dev/research/jioh/task-9.12-related-work-prose/search/S3-traces-datasets.md:327-336 | n |  |
| D-X-02 | none (labelled "unsourced: no study is named") | what older desktop trace studies released | LABELLED | none | n |  |

---

# Part F1 — gaming source group (dataset side), inventory and trace

Scope: every in-scope location citing `lavd-ossna24`, `steamos-refresh`, `steam-downloads`, `steam-for-linux-8821`, `steamos-lavd`, `gamemode-docs`, `xbox-gamemode`, `apple-gamemode`, `feral-gamemode`, `tuned`, `systemd-oomd`, `linux-sched-h`, `scx`, `corbet-lwn24`, `dai-lpc25`, `edge-lwn26`, plus untagged game / Steam / Proton / LAVD claims, and the design labels of `dataset/grids.yaml`, `game-task-chain` and the gaming timelines. `steamdeck-store` is cited by no in-scope file (not inventoried). `scx`'s slice and watchdog-timeout statements (docs/references.md:195) are scheduler-side constants no dataset file cites; not inventoried here.

Record shorthands (all under `_dev/research/jioh/`):
- 9.4-S1 = `task-9.4-gaming/search/S1-literature.md` (OSS NA 2024 slides, copy `static.sched.com/hosted_files/ossna2024/9b/scx-lavd-oss-na24.pdf`, SHA-256 `e62d69cd…`, read 2026-09-13)
- 9.4-S2 = `task-9.4-gaming/search/S2-project-docs.md` (same deck with figure labels, S2-03; Valve refresh docs, S2-08; Wine, S2-11; read 2026-09-13)
- 9.4-S3 = `task-9.4-gaming/search/S3-traces-datasets.md`; 9.4-S4 = `task-9.4-gaming/search/S4-ci-observability.md`; 9.4-cand = `task-9.4-gaming/search/candidates.md`
- R02 = `2026-09-13-verification/reads/R02-lavd.md`; R07 = `2026-09-13-verification/reads/R07-gamemode-steam-dkms.md`; K3 = `2026-09-13-verification/compare/K3.md` (all read 2026-09-13)
- 9.10-S2 / -S3 / -S4 = `task-9.10-scenarios-timelines/search/S2-project-docs.md` / `S3-traces-datasets.md` / `S4-ci-observability.md` (read 2026-10-01); 9.10-CL = its `changelog.md`
- 9.12-S2 = `task-9.12-related-work-prose/search/S2-project-docs.md` (read 2026-10-07 to 2026-10-09); 9.12-A = its `A-audit.md`; 9.12-CL = its `changelog.md`
- 9.19-P = `task-9.19-generator-and-the-c3-grids/changelog.md`, section P (the precedent search, read 2026-10-11: verbatim passage, file at tag, URL, date)

"Line last changed" is `git blame` of the primary location. Where it is later than the read, the claim's final wording was compared with the record (that is the trace below); the 9.15 sweep (commits 69c16f54, c59b6a89, 34b09357, 18127cc9, 4b966f84, 37c2e233, 2f9f8a0b, 166a4bd3; 2026-10-16/17) restated most doc lines after their reads.

---

### D-F1-01 — identity of the LAVD talk and its slide deck
- source: `lavd-ossna24` (docs/references.md:732, talk, conference abstract or news report)
- repo: docs/references.md:733 — "Min, C. (2024). "Optimizing Scheduler for Linux Gaming." Talk, Open Source Summit North America 2024, Seattle, 2024-04-17. Slides: static.sched.com/hosted_files/ossna2024/9b/scx-lavd-oss-na24.pdf (30 slides; SHA-256 `e62d69cd…`)"; also scenario-catalog.md:20 ("Min's reported trace, 2024-04-17"), building-plan.md:99, grounding-sources.md:30
- record: R02:172-174 — schedule page "April 16-18, 2024" / "Seattle, Washington"; "date Wednesday 17 April 2024"; 9.4-S1:48-49 — "Slides, Open Source Summit North America, April 17, 2024. 30 slides"; copy as above, SHA-256 `e62d69cd…`, read 2026-09-13 (re-read 9.12-S2:195-198, 2026-10-07)
- slice: 9.4 (and 2026-09-13 verification, 9.12)
- dates: line last changed 2026-10-16 (69c16f54); read 2026-09-13 / 2026-10-07; changed-after-read: yes (SHA and S2-10 pointer added; identity unchanged)
- verdict: TRACED

### D-F1-02 — number of tasks scheduled while a game runs
- source: `lavd-ossna24` (docs/references.md:734)
- repo: dataset/sources.yaml:61-63 — "Around 300 tasks scheduled system-wide while running a game (system tasks included)"; also docs/references.md:734 ("around 300 tasks scheduled while running a game"), dataset/archetypes.yaml:1803-1805 ("the source counts ~300 tasks scheduled system-wide while a game runs (s12, including system tasks)"), archetype-plan.md:102, grounding-sources.md:30, source-vetting.md:144, coreset-guide.md:254
- record: 9.4-S1:55 — Slide 12: "Around 300 tasks are scheduled while running a game."; 9.4-S1:63 coverage "all tasks system-wide, not only the game process"; read 2026-09-13
- slice: 9.4
- dates: line last changed 2026-10-17 (166a4bd3); read 2026-09-13; changed-after-read: yes (notes restated to the slide's words)
- verdict: TRACED

### D-F1-03 — share of long-lived tasks
- source: `lavd-ossna24`
- repo: dataset/sources.yaml:64 — "~90% long-lived"; also docs/references.md:734, dataset/archetypes.yaml:1807-1809 ("Around 90% are long-living tasks; only 10% of tasks are terminated" (s12, window unstated))
- record: 9.4-S1:55 — "Around 90% are long-living tasks; only 10% of tasks are terminated."; 9.4-S1:66 "Window not stated"; read 2026-09-13
- slice: 9.4
- dates: line last changed 2026-10-17 (166a4bd3); read 2026-09-13; changed-after-read: yes (wording restated; within passage)
- verdict: TRACED

### D-F1-04 — concentration of scheduling (top 30–40 tasks, system tasks, 15–20 game tasks) and the omission of the game's other threads
- source: `lavd-ossna24`
- repo: dataset/sources.yaml:64-67 — "the top 30-40 tasks 95% of scheduling, around half of them system tasks (especially wine, graphics and audio servers) taking 30-40%, 15-20 game-specific tasks 60-70% (s12)"; also docs/references.md:734; dataset/archetypes.yaml:1806-1814; archetype-plan.md:102; dataset/README.md:124; scenario-catalog.md:20; the omission statement "the source puts 95% of scheduling in its top 30-40 tasks and describes none outside them (lavd-ossna24 s12; 9.10 D19)" in c1-gaming.timeline.yaml:2-4, c2-p2a.timeline.yaml:10-12, c3-evening.timeline.yaml:11-13, c6-dual.timeline.yaml:9-11, c2-pairs.variant.yaml:27-29 and :47-49, c4.variant.yaml:11-13, c7.variant.yaml:169-171; coreset-guide.md:254
- record: 9.4-S1:55 — "Top 30-40 most frequently scheduled tasks take 95% of scheduling. ○ Around half of them are system tasks -- especially, wine, graphics, and audio servers , taking 30--40% of scheduling. ○ There are 15-20 game-specific tasks, which takes 60-70% scheduling."; 9.4-S1:65 — "No per-task statistic for the non-dominant set"; read 2026-09-13
- slice: 9.4 (omission decision 9.10-CL:378, D19)
- dates: line last changed 2026-10-17 (sources.yaml) / 2026-10-16 (c1-gaming:4, 37c2e233); read 2026-09-13; changed-after-read: yes (restated; within passage)
- verdict: TRACED

### D-F1-05 — chain length 16 as a point inside 15–20
- source: `lavd-ossna24:s12` (label: design within a source range)
- repo: dataset/archetypes.yaml:1739-1741 (`chain_length` constant 16, source "lavd-ossna24:s12"); :1797-1800 "chain_length 16 is a point chosen inside the source's "15-20 game-specific tasks" (s12) — design within a source range"; building-plan.md:99, archetype-plan.md:102, coreset-guide.md:250
- record: 9.4-S1:55 (the 15–20 band, as D-F1-04); 9.4 changelog D5 (label)
- slice: 9.4
- dates: line last changed 2026-09-13; read 2026-09-13; changed-after-read: no
- verdict: LABELLED (label present and honest)

### D-F1-06 — per-schedule runtimes and the two named examples
- source: `lavd-ossna24:s13`
- repo: dataset/archetypes.yaml:1730-1735 (`wineserver_run` constant 260 µs; `per_schedule_run` lognormal anchors 260 / 1650 µs, both "lavd-ossna24:s13"); :1774-1778 "the anchors are the source's two named per-schedule runtimes, a coordination task (wineserver, 260 us) and a work task (a task worker, 1.65 ms), spanning its stated "a few 100s usec on average to a few msec maximum" (s13); the statistic behind the two examples is not labelled"; dataset/sources.yaml:68-70; docs/references.md:734; building-plan.md:99; archetype-plan.md:102; source-vetting.md:144; coreset-guide.md:250
- record: 9.4-S1:56 — "roughly a few 100s usec on average to a few msec maximum … Some coordination tasks run very shortly (e.g., wineserver:260 usec) but some work tasks (e.g., a task worker: 1.65 msec) run longer than average."; read 2026-09-13
- slice: 9.4
- dates: line last changed 2026-09-13 (archetypes:1732) / 2026-10-17 (sources.yaml); read 2026-09-13; changed-after-read: yes for sources.yaml (restated to the slide's words)
- verdict: TRACED

### D-F1-07 — lognormal family, p05/p95 reading, one draw per member
- source: none (label: ours)
- repo: dataset/archetypes.yaml:1781-1783 — "Reading the anchors as a p05/p95 span, the lognormal family (OQ-5 convention; the compiler derives median/sigma from the span) and the one draw per member are ours"; building-plan.md:99, coreset-guide.md:250 ("p05/p95로 읽은 lognormal")
- record: 9.4 changelog D6 (label decision)
- slice: 9.4
- dates: line last changed 2026-09-13; changed-after-read: no
- verdict: LABELLED (honest)

### D-F1-08 — task execution time stable and predictable by its average
- source: `lavd-ossna24:s13`
- repo: dataset/archetypes.yaml:1784-1785 — "the source's "Task execution time is very stable and is predictable using its average" (s13)"; dataset/sources.yaml:70-71
- record: 9.4-S1:56 — "Task execution time is very stable and is predictable using its average."; read 2026-09-13
- slice: 9.4
- dates: line last changed 2026-09-13 (archetypes) / 2026-10-17 (sources.yaml); changed-after-read: yes for sources.yaml (quote added; verbatim)
- verdict: TRACED

### D-F1-09 — slide 13's runtime plot (one game, ~128 tasks, median ~0.04 ms)
- source: `lavd-ossna24:s13`
- repo: dataset/archetypes.yaml:1778-1780 — "the slide's plot of per-task runtime averages (one game, ~128 tasks, median ~0.04 ms) is a different population … and is not used"
- record: 9.4-S2:95 — "Slide 13 histogram … ordered `runtime_avg` curve has x-axis 0–~128 tasks, y up to 1.4 (msec)"; 9.4-cand:38 — "read in K2 as ≈0.02 ms at the low end, ≈0.04 ms at task 60 …"; read 2026-09-13
- slice: 9.4
- dates: line last changed 2026-09-13; changed-after-read: no
- verdict: TRACED

### D-F1-10 — what initiates scheduling: waiting system calls vs preemption, and the pie's sched_preempt share
- source: `lavd-ossna24:s14`
- repo: dataset/archetypes.yaml:1788-1789 — "s14 bounds the size (preemption 25-30 % of scheduling events, sched_preempt 28.78 % on the pie)"; :1809-1811 ""70-75% of scheduling is initiated by waiting system calls" against 25-30% preemption (s14)"; dataset/sources.yaml:71-72; docs/references.md:734; source-vetting.md:144
- record: 9.4-S1:57 — "Preemption (e.g., timer interrupt) takes only 25-30% of scheduling. ● 70-75% of scheduling is initiated by waiting system calls"; 9.4-S2:93 — pie "`sched_preempt (28.78%)`"; read 2026-09-13
- slice: 9.4
- dates: line last changed 2026-09-17 (archetypes:1789, 6be95713) / 2026-10-17 (sources.yaml); read 2026-09-13; changed-after-read: yes (restated; within passage)
- verdict: TRACED

### D-F1-11 — "about 1.4 schedules per wake" attributed to slide 14
- source: `lavd-ossna24:s14` (a derived figure)
- repo: dataset/archetypes.yaml:1789-1790 — "about 1.4 schedules per wake on average"; dataset/variants.yaml:53 — "(9.4 D9; lavd-ossna24 s14, about 1.4 on average)"; dataset/README.md:133 — "(the per-schedule runtime read as the per-wake RUN understates a wake; `lavd-ossna24` s14)"
- record: 9.4-S2:93 (28.78 %); 9.4 changelog D9 (`task-9.4-gaming/changelog.md:66`) states the 1.4 as derived ("Not taken: scaling the anchors by 1/0.71"). The slide states no per-wake figure.
- slice: 9.4
- dates: line last changed 2026-09-17 (archetypes) / 2026-10-09 (variants.yaml, bbe95e7c); read 2026-09-13; changed-after-read: yes (variants.yaml written after; wording unchanged in kind)
- verdict: LABELLED
- finding: label missing — 1.4 is our arithmetic, 1/(1 − 0.2878), assuming every non-preemption scheduling event is a wake; the repo states it beside the s14 tag with no arithmetic label. Fix: add "(our arithmetic: 1/(1 − 0.2878))" at archetypes.yaml:1789 and variants.yaml:53.

### D-F1-12 — "the deck's slice example 1.5 ms"
- source: `lavd-ossna24` (attributed)
- repo: dataset/archetypes.yaml:1791-1792 — "(s13: 1.65 ms worker; the deck's slice example 1.5 ms)"
- record: R02:91-93 (C-lavd-9) — slide 27: "a targeted latency (e.g., 15 msec)" / "The scheduler proportionally divides the targeted latency as per task's nice priority"; R02:96 — the 15 ms over 10 tasks example is scx's `main.bpf.c` header comment, "Context from scx at 8b24795 (not the talk)"; slide 27 image (`2026-09-13-verification/sources/lavd-ossna24/pages/slide-27.png`) shows no 1.5 ms
- slice: 2026-09-13 verification (R02)
- dates: line last changed 2026-09-17 (6be95713); read 2026-09-13; changed-after-read: yes (the sentence was written after the read; 9.4 D9)
- verdict: WORDING-OUTSIDE-PASSAGE
- finding: the deck gives only a 15 ms targeted latency (slide 27); 1.5 ms is 15 ms / 10 tasks from scx_lavd's source comment, not the deck. Fix: "scx_lavd's source-comment example, 15 ms shared by 10 tasks (`scx`)" or drop the comparison.

### D-F1-13 — the waiter–waker graph and its thread names (slide 16)
- source: `lavd-ossna24:s16`
- repo: dataset/sources.yaml:73-74 — "tasks tightly linked in waiter-waker graphs, with the thread names of s16"; docs/references.md:734; grounding-sources.md:30 ("tasks tightly linked in waiter–waker chains (Wine components, DXVK threads, PipeWire audio servers, task workers)"); scenario-catalog.md:20 ("`lavd-ossna24` slide 16 … names the threads"); the nine named members `Task worker thr` ×4, `dxvk-cs`, `dxvk-submit`, `winepulse_mainl`, `winepulse_timer`, `FAudio_AudioCli` and the head `Troy.exe` in every gaming file's `member_names` (c1-gaming:20-21, c2-p2a:30-31, c3-evening:37-38, c6-dual:24-25, c2-p2a-idle:34-55, c2-p2b:33-54, c4-gaming:26-47, c7-gaming:27-48); coreset-guide.md:297
- record: 9.4-S2:91 — slide 16 figure nodes "`Troy.exe[7781/0]`, `wineserver[7256/0]`, … `Task worker thr[7826/7781]` (×4), `dxvk-cs[7922/7781]`, `dxvk-submit[7920/7781]`, `winepulse_mainl[7991/7781]`, `winepulse_timer[7993/7781]`, `FAudio_AudioCli[7992/7781]`, `pipewire-pulse…`, `pipewire…`"; SHA-256 of the image `bdaa20d5…`; read 2026-09-13
- slice: 9.4 (binding decision 9.10-CL:550, D26)
- dates: line last changed 2026-10-17 (sources.yaml) / 2026-10-11 (c1-gaming:21, b5678087); read 2026-09-13; changed-after-read: yes (tag form only)
- verdict: TRACED

### D-F1-14 — the six chain members named `Troy.exe` under the slide-16 tag
- source: `lavd-ossna24:s16` (attributed)
- repo: c1-gaming.timeline.yaml:20-21 — `member_names: [… FAudio_AudioCli, Troy.exe, Troy.exe, Troy.exe, Troy.exe, Troy.exe, Troy.exe]`, `source: {… member_names: "lavd-ossna24:s16"}`; the same in c2-p2a:30-31, c3-evening:37-38, c6-dual:24-25, c2-p2a-idle:55, c2-p2b:54, c4-gaming:47, c7-gaming:48; coreset-guide.md:252 — "멤버 이름은 timeline이 `member_names`로 줘요(slide 16이 보여주는 game thread 이름 …)"; scenario-catalog.md:36 — "the game chain's thread names from `lavd-ossna24` slide 16"
- record: 9.4-S2:91 — slide 16 shows one `Troy.exe[7781/0]` node; 9.10-CL:558 (D26) — "the six members slide 16 does not name keep the process's `comm`, `Troy.exe`", grounded on Wine's naming (9.10 S2-18), not on the slide
- slice: 9.4 / 9.10
- dates: line last changed 2026-10-11 (b5678087) / 2026-10-16 (coreset-guide); read 2026-09-13; changed-after-read: yes (tag added 2026-10-11)
- verdict: WORDING-OUTSIDE-PASSAGE
- finding: the tag and the two docs present all 15 names as slide 16's; the slide names nine of them, and the six repeated `Troy.exe` come from 9.10 D26's rule (a Wine thread without its own name carries its process's `comm`), stated in no dataset file. Fix: one sentence in `game-task-chain`'s modeling_notes (and coreset-guide.md:252) that six members carry the process `comm` `Troy.exe` by that rule, ours.

### D-F1-15 — the graph's shapes and wineserver's edges
- source: `lavd-ossna24:s11`, `s16`
- repo: dataset/archetypes.yaml:1768-1772 — "the source's graphs are a fan-in (four task workers -> dxvk-cs), a two-step chain (dxvk-cs -> dxvk-submit), 2-cycles among the audio threads and a hub around wineserver (s11, s16)"; :1815-1821 — "draws it as the hub of the game's dispatcher threads (s11), and gives its edges to and from the game process the largest counts in the s16 graph (epoll from wineserver to the game, pipe_read from the game to wineserver)"
- record: 9.4-S2:91 — "`wineserver→Troy.exe epoll (134200)`, `Troy.exe→wineserver pipe_read (58134)`, … `Task worker thr[7826]→dxvk-cs futex_wait (10438)` … `dxvk-cs→dxvk-submit futex_wait (30970)`, `winepulse_mainl→winepulse_timer poll (20102)`, `winepulse_timer→winepulse_mainl futex_wait (10145)`"; 9.4-S2:92 — slide 11 "`redDispatcher1→wineserver pipe_read (91195)`, `wineserver→redDispatcher1 epoll (114702)`"; R02:86 (C-lavd-8) "slide 11 has a hub-and-spoke around `wineserver`"; read 2026-09-13
- slice: 9.4
- dates: line last changed 2026-09-13; changed-after-read: no
- verdict: TRACED

### D-F1-16 — a sequence of tasks serves one job; most game tasks periodic
- source: `lavd-ossna24:s17`
- repo: dataset/sources.yaml:75-76 — "a sequence of tasks serving a single job, e.g. from a user input to display update (s17)"; dataset/archetypes.yaml:1764-1768 ("standing in for the source's "from a user input to display update" (s17); no intermediate stage is named by the source"), :1772-1773 ("s17 says the majority of game tasks are individually periodic")
- record: 9.4-S1:60 — "Majority of game tasks shows periodic behavior … A sequence of tasks serves for a single job (e.g., from a user input to display update)."; R02:86-89 (C-lavd-8) "no intermediate stages between input and output are named"; read 2026-09-13
- slice: 9.4
- dates: line last changed 2026-09-13 (archetypes) / 2026-10-17 (sources.yaml); changed-after-read: yes for sources.yaml (within passage)
- verdict: TRACED

### D-F1-17 — the deck states no frame period or frame budget; its 15 ms is a targeted latency
- source: `lavd-ossna24`
- repo: dataset/sources.yaml:76-77 — "The slides state no frame period or frame budget."; docs/references.md:734-735; dataset/archetypes.yaml:1759-1760 ("frame_period is not in the deck"); source-vetting.md:144 — "the deck states no frame period, frame budget or deadline — its 15 ms is an example scheduler targeted latency for time slices"; grounding-sources.md:30
- record: R02:91-97 (C-lavd-9) — slide 27 "targeted latency (e.g., 15 msec)"; "(d) PREMISE NOT IN SOURCE — no frame time budget or frame-rate correspondence is stated"; 9.4-S1:63 "T1: does not cover (no frame period …)"; read 2026-09-13
- slice: 2026-09-13 verification, 9.4
- dates: line last changed 2026-10-17 (source-vetting, c59b6a89); read 2026-09-13; changed-after-read: yes (correction section new; within passage)
- verdict: TRACED

### D-F1-18 — traces collected while playing games; game and machine unnamed
- source: `lavd-ossna24`
- repo: dataset/sources.yaml:59-60 — "from traces collected while playing games, the games and the machine unnamed"; docs/references.md:734; dataset/archetypes.yaml:1756-1757 ("one observation of an unnamed game on an unnamed machine")
- record: 9.4-S1:53 — Slide 10: "We collect and analyze all scheduling activities while playing games."; 9.4-S1:67 — "T5: does not name the machine, core count or game behind slides 12–14"; read 2026-09-13
- slice: 9.4
- dates: line last changed 2026-10-17 (166a4bd3); changed-after-read: yes (within passage)
- verdict: TRACED

### D-F1-19 — the deck's traces collected with `perf sched record`
- source: `lavd-ossna24` (attributed)
- repo: dataset/archetypes.yaml:1756-1757 — "Source: lavd-ossna24 slides 12-17 taken as one observation of an unnamed game on an unnamed machine, collected with perf sched record"; coreset-guide.md:242 — "이름 모를 game을 이름 모를 machine에서 `perf sched record`로 본 관찰 하나로 읽어요"
- record: 9.4-S1:53 — the deck says only "We collect and analyze all scheduling activities while playing games"; the tool is named in Min's LPC 2025 slides, 9.4-S2:118 (S2-05 (a) Slide 6): "VaporMark collects all the scheduling activities during a period using "perf sched record"" (and the VaporMark README, 9.4-S2:145-153); the link to the 2024 deck is 9.4 D1's reading (`task-9.4-gaming/changelog.md:7`)
- slice: 9.4
- dates: line last changed 2026-09-13 (archetypes) / 2026-10-16 (coreset-guide); read 2026-09-13; changed-after-read: yes for coreset-guide (wording kept)
- verdict: WORDING-OUTSIDE-PASSAGE
- finding: the collection tool is attributed to `lavd-ossna24`, which does not name it; it comes from Min's later LPC 2025 slides / VaporMark, which have no registry entry. Fix: "collected, by 9.4 D1's reading of Min's LPC 2025 slides, with `perf sched record`", or cite that source.

### D-F1-20 — the deck's figures draw on at least three process trees
- source: `lavd-ossna24`
- repo: dataset/archetypes.yaml:1758-1759 — "the deck's figures draw on at least three process trees and the text does not say which feeds slides 12-14 (recorded decision)"
- record: 9.4-S2:98 — "No — slides 12–14 aggregate over unstated traces; the figures name three distinct process trees (tgids 7781, 6340, 4727)"; read 2026-09-13
- slice: 9.4
- dates: line last changed 2026-09-13; changed-after-read: no
- verdict: TRACED

### D-F1-21 — public scx_lavd logs of four other games show tens of µs per schedule
- source: none tagged (scx issues #234, #296; stated "not a source here")
- repo: dataset/archetypes.yaml:1794-1796 — "Sampled scheduler logs of four other games under scx_lavd show game threads at tens of us per schedule (different accounting; not a source here)"
- record: 9.4-S3:49, :107 (issues #234 Helldivers 2 and Apex Legends, #296 Diablo III and StarCraft II); 9.4-cand:40 — "`r5apex.exe` 19 974 ns, `Worker 2` 17 376 … (EWMA runtime per schedule, under `scx_lavd`)"; read 2026-09-13
- slice: 9.4
- dates: line last changed 2026-09-13; changed-after-read: no
- verdict: TRACED

### D-F1-22 — why no runner measurement referees the chain: no GPU, Proton only under Steam
- source: none tagged (Proton README; runner docs)
- repo: dataset/archetypes.yaml:1750-1754 — "a CI runner cannot observe a Proton game's Wine, DXVK or audio structure (no GPU; Proton runs only under the Steam client)"
- record: 9.4-S4:262 — Proton README L4–6 "**Proton** is a tool for use with the Steam client …"; L8 "**Most users should use Proton provided by the Steam Client itself.**"; 9.4-S4:263 "the README documents no standalone run path"; read 2026-09-13
- slice: 9.4
- dates: line last changed 2026-09-13 (8a4eb6e0); changed-after-read: no
- verdict: WORDING-OUTSIDE-PASSAGE
- finding: the README presents Proton as a Steam-client tool and documents no other run path; "runs only under the Steam client" states an exclusivity it does not. Fix: "Proton is documented only as a tool for use with the Steam client".

### D-F1-23 — Wine calls are a request write and a blocking reply read
- source: none tagged (Wine source)
- repo: dataset/archetypes.yaml:1821-1823 — "Those edges are a request/reply round trip (each Wine call is a request write and a blocking reply read)"
- record: 9.4-S2:211-212 — `dlls/ntdll/unix/server.c` "send_request * * Send a request to the server." … "wait_reply * * Wait for a reply"; 9.4-S2:220 coverage "each client thread has its own request/reply fds"; read 2026-09-13
- slice: 9.4
- dates: line last changed 2026-09-13; changed-after-read: no
- verdict: TRACED

### D-F1-24 — Steam Deck LCD default refresh and frame-limit setting
- source: `steamos-refresh` (docs/references.md:303, deployed-system)
- repo: dataset/sources.yaml:146-153 — "the Steam Deck LCD's 60 Hz default refresh and the in-game refresh / frame-limit setting (default 60 Hz limited to 60, 30 or 15 fps; slider down to 40 Hz; "60hz = 16.66ms/frame")"; docs/references.md:304-305; dataset/archetypes.yaml:1736-1738, 1760-1762; archetype-plan.md:102; building-plan.md:99; grounding-sources.md:30; source-vetting.md:144; coreset-guide.md:250
- record: 9.4-S2:162-167 — (a) "The default is 60Hz (which can be frame-limited to 60, 30, and 15fps), but you can now slide it down to 40Hz (with frame limits at 40, 20, and 10fps)"; footnote "60hz = 16.66ms/frame"; (b) "1:1, 1:2, 1:4, or uncapped"; (e) "Refresh rate | 60Hz"; copy ISteamNews API JSON SHA-256 `d2dd337c…`, read 2026-09-13
- slice: 9.4
- dates: line last changed 2026-09-13; changed-after-read: no
- verdict: TRACED

### D-F1-25 — frame period 16,667 µs: display-paced design, 1/60 s arithmetic
- source: `steamos-refresh` (label: design + arithmetic)
- repo: dataset/archetypes.yaml:1759-1762 — "the game is modelled as display-paced at the Steam Deck LCD default refresh with the 1:1 frame limit (steamos-refresh: 60 Hz; 16667 us is 1/60 s arithmetic) — design, ours"; building-plan.md:99 ("`steamos-refresh`, design"); archetype-plan.md:102 ("a design value"); coreset-guide.md:250
- record: 9.4 changelog D2 (`task-9.4-gaming/changelog.md:11`)
- slice: 9.4
- dates: line last changed 2026-09-13; changed-after-read: no
- verdict: LABELLED (honest)

### D-F1-26 — Steam's download check box and the default pause at game launch
- source: `steam-downloads` (docs/references.md:293, deployed-system)
- repo: dataset/sources.yaml:139-142 — "Establishes the "Allow Downloads During Gameplay" check box (Steam -> Settings -> Downloads), that downloads pause during gameplay by default"; docs/references.md:295; scenario-catalog.md:21 ("Steam pauses queued downloads when a game launches"); grounding-sources.md:18; c2-p2a.timeline.yaml:1-4; coreset-guide.md:794
- record: R07:141-160 (C-steam-1, C-steam-2) — "check the [i]Allow Downloads During Gameplay[/i] box"; "Steam automatically pauses your downloads when a game is launched in order to prioritize the network activity for the game itself."; reading "so it is the default"; copy help.steampowered.com/en/faqs/view/4F9E-6328-E9B8-47F9, FAQ JSON version 3 (R07:21), read 2026-09-13; restated in 9.10-CL:125 (D7)
- slice: 2026-09-13 verification, 9.10
- dates: line last changed 2026-10-07 (sources.yaml, 723bda39) / 2026-10-16 (references, scenario-catalog); read 2026-09-13; changed-after-read: yes (restated; within passage)
- verdict: TRACED

### D-F1-27 — the per-game download setting attributed to FAQ 4F9E
- source: `steam-downloads`
- repo: docs/references.md:295 — "existence of the "Allow Downloads During Gameplay" check box …, of the default pause of downloads when a game launches, and of a per-game setting the article leaves unnamed (FAQ 4F9E-6328-E9B8-47F9)"; dataset/sources.yaml:142 — "and a per-game setting the article leaves unnamed"
- record: R07:161-169 (C-steam-3) — the sentence "There's also a per-game setting to allow/prevent the downloading of other updates while you're playing" is in FAQ 71AB-698D-57EB-178C; R07:167 — "The 4F9E article does not mention a per-game setting."; 9.10-S2:2924-2936 (S2-20) the same passage in 71AB, read 2026-10-01
- slice: 2026-09-13 verification, 9.10
- dates: line last changed 2026-10-16 (69c16f54); read 2026-09-13 / 2026-10-01; changed-after-read: yes
- verdict: WORDING-OUTSIDE-PASSAGE
- finding: the locator is wrong — the per-game setting is in FAQ 71AB-698D-57EB-178C, not in 4F9E. Fix: move "(FAQ 4F9E…)" before "and of a per-game setting" and give the per-game setting "(FAQ 71AB-698D-57EB-178C)"; in sources.yaml say "the second article".

### D-F1-28 — Steam's automatic update queue
- source: `steam-downloads`
- repo: docs/references.md:295 — ""Games are automatically put into your download queue when a game releases an update" (FAQ 71AB-698D-57EB-178C)"
- record: R07:163 — "Games are automatically put into your download queue when a game releases an update."; read 2026-09-13
- slice: 2026-09-13 verification
- dates: line last changed 2026-10-16; changed-after-read: yes (quote added; verbatim)
- verdict: TRACED

### D-F1-29 — a user-started install proceeds at once during play (issue #8821)
- source: `steam-for-linux-8821` (docs/references.md:298, deployed-system)
- repo: docs/references.md:299 — "with "Allow downloads during gameplay" off, Steam pauses queued downloads when a game launches, "But if you have a game launched and during gameplay press "Install" for another game that game will start downloading immediately." … confirmed by Valve's triager as "not specific to SteamOS or the Steam Deck" … one user's Steam Deck"; scenario-catalog.md:21; coreset-guide.md:794; c2-p2a.timeline.yaml:1-4
- record: 9.10-S3:474-480 (S3-27) — "When "Allow downloads during gameplay" is turned off Steam Deck won't download scheduled games and also will pause download when you launch game."; "But if you have a game launched and during gameplay press "Install" for another game that game will start downloading immediately."; comment 1 (kisak-valve) "this is not specific to SteamOS or the Steam Deck."; copy API JSON SHA-256 `ccb01df5…`, read 2026-10-01
- slice: 9.10
- dates: line last changed 2026-10-16; read 2026-10-01; changed-after-read: yes (within passage)
- verdict: TRACED

### D-F1-30 — SteamOS 3.8 adds LAVD as a user-selected scheduler, not enabled by default
- source: `steamos-lavd` (docs/references.md:308, deployed-system)
- repo: grounding-sources.md:30 — "Valve … ships it in SteamOS 3.8 as a scheduler the user selects, not enabled by default (`steamos-lavd`)"; docs/references.md:309-310
- record: 9.12-S2:266 (S2-15) — "Initial support for LAVD CPU scheduler via `steamosctl set-cpu-scheduler lavd`" (read 2026-10-07); 9.12-S2:535 (S2-49) — `power.rs` LAVD / None, setting LAVD starts `scx.service` (read 2026-10-08); 9.12-S2:538-548 (S2-50) — 3.8.14 image, `SCX_SCHEDULER=scx_lavd`, `scx.service` linked in no `*.wants` (read 2026-10-08)
- slice: other (9.12)
- dates: line last changed 2026-10-17 (grounding-sources, c59b6a89); read 2026-10-07/08; changed-after-read: yes (within passage)
- verdict: TRACED

### D-F1-31 — Valve sponsors LAVD
- source: `steamos-lavd`, `scx`
- repo: grounding-sources.md:30 — "Valve sponsors LAVD"; docs/references.md:309 — "Valve sponsors LAVD's development: scx_lavd's `lat_cri.bpf.c` reads "Copyright (c) 2023-2025 Valve Corporation. Author: Changwoo Min …""
- record: 9.12-S2:188 (S2-09) — `lat_cri.bpf.c:3-4`: "Copyright (c) 2023-2025 Valve Corporation. Author: Changwoo Min"; 9.12-S2:246 (S2-13) "developing LAVD as part of his work at Igalia on SteamOS and the Steam Deck"; reading recorded as 9.12 D9 (9.12-CL:152-156); read 2026-10-07
- slice: other (9.12)
- dates: line last changed 2026-10-17; changed-after-read: yes (the reading's wording kept)
- verdict: TRACED (the copyright line and the author's work statement; "sponsors" is 9.12 D9's recorded reading of them)

### D-F1-32 — scx_lavd motivated by gaming, to reduce stuttering; pinned at v1.1.3
- source: `scx` (docs/references.md:194, deployed-system)
- repo: grounding-sources.md:30 — "scx_lavd's source and README at `v1.1.3`, `scx` … scx_lavd motivated by reducing stutter"; docs/references.md:195-196
- record: 9.12-S2:186 (S2-09) — `scx_lavd/README.md:20-23`: "`scx_lavd` is initially motivated by gaming workloads. It aims to improve interactivity and reduce stuttering while playing games on Linux."; copy tag v1.1.3, commit c8728c6b, read 2026-10-07
- slice: other (9.12)
- dates: line last changed 2026-10-17; changed-after-read: yes (within passage)
- verdict: TRACED

### D-F1-33 — Corbet's LWN report of the LPC 2024 talks
- source: `corbet-lwn24` (docs/references.md:737, news report)
- repo: docs/references.md:738-739 — "Corbet, J. "Sched_ext at LPC 2024." LWN.net, 2024-09-26 …"; "Its "typically no more than 100µs at a time" differs from `lavd-ossna24` slide 13's …"; grounding-sources.md:30; source-vetting.md:166 ("Jonathan Corbet's report of the LPC 2024 talks (`corbet-lwn24`, LWN 991205, 2024-09-26)")
- record: 9.12-S2:226-238 (S2-12) — Jonathan Corbet, 26 September 2024; "tasks tend to run quickly, typically no more than 100µs at a time"; "a virtual deadline calculated for it, which is a function of both its waking and waiting frequencies"; copy lwn.net/Articles/991205/, SHA-256 `9421ec52…`, read 2026-10-07
- slice: other (9.12)
- dates: line last changed 2026-10-16 / 2026-10-17; changed-after-read: yes (within passage)
- verdict: TRACED

### D-F1-34 — Edge's LWN report of Min's LPC 2025 session
- source: `edge-lwn26` (docs/references.md:757, news report)
- repo: docs/references.md:758 — "LAVD developed "as part of his work at Igalia on SteamOS and the Steam Deck" … "there are often 20 or 30 tasks in a chain …""; source-vetting.md:166 ("Jake Edge's (`edge-lwn26`, LWN 1051430, 2026-01-07)"); grounding-sources.md:30
- record: 9.12-S2:241-252 (S2-13) — Jake Edge, 7 January 2026; "there are often 20 or 30 tasks in a chain that all need to collaborate"; "including one about adapting LAVD to be the default scheduler for Meta's production fleet"; copy SHA-256 `bd65bcac…`, read 2026-10-07
- slice: other (9.12)
- dates: line last changed 2026-10-16/17; changed-after-read: yes (within passage)
- verdict: TRACED

### D-F1-35 — Meta's speakers present scx_lavd as a candidate default fleet scheduler
- source: `dai-lpc25` (docs/references.md:752, conference abstract)
- repo: grounding-sources.md:30 — "Meta's speakers presented it as a candidate default fleet scheduler (`dai-lpc25`)"; docs/references.md:753
- record: 9.12-S2:220 (S2-11) — contribution 2099 (David Dai, Ryan Newton), 2025-12-12: "There exists a need for a "default" fleet scheduler that "just works" … SCX_LAVD is one such candidate"; copy lpc.events/export/timetable/19.json, SHA-256 `3157aac9…`, read 2026-10-07
- slice: other (9.12)
- dates: line last changed 2026-10-17; changed-after-read: yes (within passage)
- verdict: TRACED

### D-F1-36 — Windows Game Mode: the category and Microsoft's documented design
- source: `gamemode-docs` (docs/references.md:247, deployed-system)
- repo: grounding-sources.md:18 — "The *gaming* category (`gamemode-docs`, `apple-gamemode`, `feral-gamemode`)"; docs/references.md:248-250 ("works by default for most Windows games …"; ""granted on a per-title basis; contact your account manager …""; "The app must be in the foreground and have focus …"; "memory resources, once granted, will never be revoked"; deprecation note); source-vetting.md:152
- record: 9.12-S2:277 (S2-16) — "Game Mode works by default for most Windows games, requiring no action or opt-in by the customer, and no work by the game developer."; R07:37-55, :102 — "memory resources, once granted, will never be revoked", "This capability is granted on a per-title basis; contact your account manager for more information", "returns 0 if … opted out of Game Mode via the Settings in Windows 10"; copies Learn pages, read 2026-09-13 / 2026-10-07
- slice: 2026-09-13 verification, 9.12
- dates: line last changed 2026-10-16/17; changed-after-read: yes (within passage)
- verdict: TRACED

### D-F1-37 — `SetProcessDefaultCpuSets` is not an `<expandedresources.h>` function
- source: `gamemode-docs`
- repo: source-vetting.md:157 — "`SetProcessDefaultCpuSets` is not an `<expandedresources.h>` function (the header documents three, the function only in a remark)"
- record: K3:108 — "grep for `SetProcessDefaultCpuSets` over the saved copies finds only "As with SetProcessDefaultCpuSets, ReleaseExclusiveCpuSets applies to the whole process." … The header index lists only the three functions"; R07:75 header page "expandedresources.h contains the following programming interfaces"; read 2026-09-13
- slice: 2026-09-13 verification
- dates: line last changed 2026-10-17; changed-after-read: yes (correction section new; within passage)
- verdict: TRACED

### D-F1-38 — Game Mode holds back Windows Update driver installs and restart notifications
- source: `xbox-gamemode` (docs/references.md:253, deployed-system)
- repo: grounding-sources.md:18 — "Windows Update's driver installs and restart notifications while a game runs in Game Mode (`xbox-gamemode`, dated by the Xbox Wire post of 2018-10-02)"; source-vetting.md:157; docs/references.md:254
- record: 9.12-S2:607 (S2-58) — "When you're running a game, Game Mode: Prevents Windows Update from performing driver installations and sending restart notifications" … "Game Mode is turned on by default." (read 2026-10-09); 9.12-A:158-161 (A2-19) — Xbox Wire `datePublished` "2018-10-02T21:44:22Z", "Game Mode suppresses Windows Update driver installs and blocks Windows Update interruptions such as restart notifications while you're gaming." (read 2026-10-09)
- slice: other (9.12)
- dates: line last changed 2026-10-16/17; changed-after-read: yes (within passage)
- verdict: TRACED

### D-F1-39 — macOS Game Mode's documented behaviour
- source: `apple-gamemode` (docs/references.md:258, deployed-system)
- repo: grounding-sources.md:18 (the gaming category); docs/references.md:259 — "When your game enters full screen, Game Mode automatically turns on …"; "highest priority access to your CPU and GPU, lowering usage for background tasks"; "Mac with Apple silicon and macOS Sonoma 14 or later …"
- record: 9.12-S2:287-296 (S2-18) — the three passages verbatim; copy support.apple.com/en-us/105118, "Published Date: September 14, 2026", SHA-256 `10857702…`, read 2026-10-07
- slice: other (9.12)
- dates: line last changed 2026-10-16; changed-after-read: yes (within passage)
- verdict: TRACED

### D-F1-40 — Feral GameMode's request model and the `[filter]` whitelist
- source: `feral-gamemode` (docs/references.md:580, deployed-system)
- repo: docs/references.md:581 — "a game enters GameMode by its own request — the library call (`gamemode_request_start()`, `gamemoded.8.in:49–56`) or a launcher that integrates it — or by being launched under `gamemoderun` (`README.md:23–28`); the optional `[filter]` whitelist rejects requesters not on it (`gamemode.ini:49–55`, commented out in the example)"; grounding-sources.md:18 (the gaming category)
- record: 9.12-S2:299-312 (S2-19) — `README.md:23-28` "For games/launchers which integrate GameMode support, simply running the game will automatically activate GameMode … launching the game through `gamemoderun`"; `gamemoded.8.in:49-56`; `gamemode.ini:49-55` "[filter] ; If "whitelist" entry has a value(s) ; gamemode will reject anything not in the whitelist ;whitelist=…"; copy master a74b8106, read 2026-10-07
- slice: other (9.12)
- dates: line last changed 2026-10-16; changed-after-read: yes (within passage)
- verdict: TRACED

### D-F1-41 — GameMode's 5 s reaper interval
- source: `feral-gamemode`
- repo: dataset/grids.yaml:68 — `{length: 5s, source: feral-gamemode}`; dataset/sources.yaml:239-247 — "release 1.8.2: the shipped example configuration's `reaper_freq=5`, "the reaper thread will check every 5 seconds for exited clients, for config file changes, and for the CPU/iGPU power balance""; docs/references.md:580-581
- record: 9.19-P:18 — "`reaper_freq`: "The reaper thread will check every 5 seconds for exited clients, for config file changes, and for the CPU/iGPU power balance" | 5 s | github.com/FeralInteractive/gamemode, `example/gamemode.ini` at tag 1.8.2 (release 2024-08-19) and `master`, identical"; read 2026-10-11
- slice: other (9.19)
- dates: line last changed 2026-10-11 (0880ba89); read 2026-10-11; changed-after-read: no
- verdict: TRACED

### D-F1-42 — tuned's 10 s dynamic-tuning update interval
- source: `tuned` (docs/references.md:585, deployed-system)
- repo: dataset/grids.yaml:69 — `{length: 10s, source: tuned}`; dataset/sources.yaml:249-257 — "release v2.28.0: `tuned-main.conf`'s dynamic tuning `update_interval = 10` ("Update interval for dynamic tunings (in seconds)") over a `sleep_interval = 1`; dynamic tuning itself ships off (`dynamic_tuning = 0`)"
- record: 9.19-P:17 — "dynamic tuning `update_interval` ("Update interval for dynamic tunings (in seconds)"), `sleep_interval` ("higher number means lower overhead but longer response time"); `dynamic_tuning = 0` ships off | 10 s / 1 s | … `tuned-main.conf` at tag v2.28.0 (release 2026-08-22) and `master`, identical"; read 2026-10-11
- slice: other (9.19)
- dates: line last changed 2026-10-11; changed-after-read: no
- verdict: TRACED

### D-F1-43 — tuned entry's further quotations
- source: `tuned`
- repo: docs/references.md:586 — "Update interval for dynamic tunings (in seconds). It must be multiply of the sleep_interval"; ("How long to sleep before checking for events (in seconds); higher number means lower overhead but longer response time"); "`dynamic_tuning = 0`, "if disabled only static tuning will be used""
- record: 9.19-P:17 holds only "Update interval for dynamic tunings (in seconds)", "higher number means lower overhead but longer response time" and "`dynamic_tuning = 0` ships off"; no record holds "It must be multiply of the sleep_interval", "How long to sleep before checking for events (in seconds)" or "if disabled only static tuning will be used" (grep over `_dev/research/jioh`)
- slice: other (9.19)
- dates: line last changed 2026-10-11; read 2026-10-11; changed-after-read: no
- verdict: RECORD-BELOW-STANDARD
- finding: three quotations in the role line have no verbatim record. Fix: add the three `tuned-main.conf` lines (tag v2.28.0) to the 9.19 precedent record, or cut the quotations to the recorded words.

### D-F1-44 — systemd-oomd's 30 s pressure duration and the 60 % / 10 s limit
- source: `systemd-oomd` (docs/references.md:590, deployed-system)
- repo: dataset/grids.yaml:70 — `{length: 30s, source: systemd-oomd}`; dataset/sources.yaml:259-267 — "`DefaultMemoryPressureDurationSec=` "sets the amount of time a unit's control group needs to have exceeded memory pressure limits" before systemd-oomd acts, "defaults to 30 seconds"; the limit a 60 % fraction of a 10 s window"
- record: 9.19-P:19 — "`DefaultMemoryPressureDurationSec=` "the amount of time a unit's control group needs to have exceeded memory pressure limits … Defaults to 30 seconds when unset or 0"; `DefaultMemoryPressureLimit=` "the fraction of time in a 10 second window … Defaults to 60%" | 30 s | github.com/systemd/systemd, `man/oomd.conf.xml` at `main` (263~devel)"; read 2026-10-11
- slice: other (9.19)
- dates: line last changed 2026-10-11; changed-after-read: no
- verdict: TRACED

### D-F1-45 — systemd-oomd entry's further quotation
- source: `systemd-oomd`
- repo: docs/references.md:591 — ""Must be set to 0, or at least 1 second. Defaults to 30 seconds when unset or 0""; "represents the fraction of time in a 10 second window in which all tasks in the control group were delayed"
- record: 9.19-P:19 elides the middle ("… Defaults to 30 seconds"; "the fraction of time in a 10 second window … Defaults to 60%"); "Must be set to 0, or at least 1 second" and "in which all tasks in the control group were delayed" are in no record (grep)
- slice: other (9.19)
- dates: line last changed 2026-10-11; changed-after-read: no
- verdict: RECORD-BELOW-STANDARD
- finding: two quoted fragments have no verbatim record. Fix: record the full `oomd.conf.xml` passages (with the commit of `main` read) in the 9.19 precedent record, or cut the quotations to the recorded words.

### D-F1-46 — the flap-stress intervals called the three daemons' "debounce" values
- source: `feral-gamemode`, `tuned`, `systemd-oomd`
- repo: dataset/grids.yaml:56-60 — "5 s, 10 s and 30 s are the debounce values of the daemon-level switches comparable to ours — GameMode's reaper interval, tuned's dynamic-tuning update interval, systemd-oomd's pressure duration"; dataset/README.md:150 — "the debounce intervals of GameMode's reaper, tuned's dynamic tuning and systemd-oomd"; building-plan.md:185 — "the debounce intervals of the daemon-level switches comparable to ours"; coreset-guide.md:588 — "간격 5·10·30 s는 GameMode, tuned, systemd-oomd의 debounce 값"
- record: 9.19-P:17-19 — GameMode "will check every 5 seconds" (a check interval), tuned "Update interval for dynamic tunings" (an update interval), systemd-oomd "the amount of time … needs to have exceeded memory pressure limits" (a sustain duration); tuned's "`dynamic_tuning = 0` ships off"
- slice: other (9.19)
- dates: line last changed 2026-10-11 (grids, building-plan) / 2026-10-16 (README) / 2026-10-17 (coreset-guide); read 2026-10-11; changed-after-read: yes for README and coreset-guide (wording kept)
- verdict: WORDING-OUTSIDE-PASSAGE
- finding: two of the three passages state a polling interval, not a debounce; only systemd-oomd's is a sustain-before-acting duration; and tuned's dynamic tuning, which docs/references.md:586 says to "carry with it", ships disabled. Fix: use sources.yaml's words — GameMode's check interval, tuned's update interval (dynamic tuning off by default), systemd-oomd's sustain duration — at the four locations.

### D-F1-47 — 2 s flap-stress interval
- source: none (label: design)
- repo: dataset/grids.yaml:59-60, :67 — "2 s is a point below that range, design"; `{length: 2s, source: design}`; README.md:150, building-plan.md:185, coreset-guide.md:588
- record: 9.19-P reading (`task-9.19-generator-and-the-c3-grids/changelog.md:25`)
- slice: other (9.19)
- dates: line last changed 2026-10-11; changed-after-read: no
- verdict: LABELLED (honest)

### D-F1-48 — Linux process names are at most 15 characters
- source: `linux-sched-h` (docs/references.md:384, deployed-system)
- repo: dataset/grids.yaml:29-32 — "TASK_COMM_LEN is 16 bytes including the terminating NUL (`include/linux/sched.h`), so 15 characters"; `comm_limit: {chars: 15, source: linux-sched-h}`; dataset/sources.yaml:233-235; docs/references.md:386; scenario-catalog.md:36; building-plan.md
- record: 9.10-S4:1500 (S4-09) — `v6.17__include_linux_sched.h` line 320 "TASK_COMM_LEN = 16,"; copy raw.githubusercontent.com torvalds/linux tag v6.17, SHA-256 `d7a2b1e7…`, read 2026-10-01; 9.10-S2:1735-1742, :1780-1791 (S2-11) — v6.8 / v7.0 `char comm[TASK_COMM_LEN];`, "strscpy_pad() to ensure it is always NUL-terminated and zero-padded" (read 2026-10-01)
- slice: 9.10
- dates: line last changed 2026-10-12 (021ca129); read 2026-10-01; changed-after-read: yes (entry written after; within passage)
- verdict: TRACED

### D-F1-49 — the linux-sched-h cite's quotations "at v6.17", read 2026-10-12
- source: `linux-sched-h`
- repo: docs/references.md:385 — "tag v6.17: `enum { TASK_COMM_LEN = 16, };` ("Define the task command name length as enum, then it can be visible to BPF programs"); `struct task_struct`'s `char comm[TASK_COMM_LEN];` — "executable name, excluding path", set with `set_task_comm()`, "strscpy_pad() to ensure it is always NUL-terminated and zero-padded" … (accessed 2026-10-12)"; :387 status "verified (2026-10-12; the header read at the tag)"
- record: no record of a 2026-10-12 read. The v6.17 record (9.10-S4:1500) quotes line 320 only; the comment quotations are recorded at v6.8 (9.10-S2:1735-1738, "Define the task command name length as enum, then it can be visible to BPF programs") and v7.0 (9.10-S2:1780-1791, "executable name, excluding path" … "strscpy_pad() …"), read 2026-10-01. (The local v6.17 copy, `task-9.10-scenarios-timelines/sources/S4-09/v6.17__include_linux_sched.h:1156, :1160`, holds the same words; that copy is not a record.)
- slice: 9.10
- dates: line last changed 2026-10-12; changed-after-read: n/a
- verdict: RECORD-BELOW-STANDARD
- finding: the read the status names (2026-10-12, v6.17) has no record; the quotations are recorded at other tags. Fix: point the cite and status to 9.10 S4-09 (v6.17:320) and S2-11 (v6.8/v7.0) with their 2026-10-01 date, or record the v6.17 lines 1156-1160.

### D-F1-50 — lane_share values in the gaming files
- source: none (label: design)
- repo: c1-gaming.timeline.yaml:19-21 (`lane_share: 0.9`, `source: {lane_share: design, …}`); c2-p2a:29-31 (0.95); c6-dual:23-25 (0.6); c3-evening:36-38; derived c2-p2a-idle:54, c2-p2b:53, c4-gaming:46, c7-gaming:47; archetypes.yaml:1745-1747, 1811-1814 ("scaling the chain's RUN values so its per-frame demand equals lane_share is our calibration, not the source's")
- record: 9.4 changelog D3 (`task-9.4-gaming/changelog.md:22`)
- slice: 9.4
- dates: line last changed 2026-10-11 (tags); changed-after-read: n/a
- verdict: LABELLED (honest)

### D-F1-51 — the grid definition's own values
- source: none (label: design), except `comm_limit` and three intervals (above)
- repo: dataset/grids.yaml:8-9 — "Every generated file is design: it composes the C1 task sets and claims nothing about how often or in what order desktops see the modes"; :27-28 (`segment_length: 60s`, `no_input_below: 4s`), :45-46 (`middle_lengths`), :62-64 (`lead_in`, `alternations`, `pairs`), :117 ("The tier-4 table is design"), :119-145 (tier-4 names)
- record: 9.19 decisions 1, 6, 7; 9.20 changelog Q6 (`task-9.20-c4-and-c5-grids/changelog.md:64`)
- slice: other (9.19, 9.20)
- dates: line last changed 2026-10-11 / 2026-10-12; changed-after-read: n/a
- verdict: LABELLED (honest)


# Part F2 — interactive, typing, HCI and community-tool sources

Group: swell-icmi14, dhakal-chi18, gonzalez-chi04, mark-chi05, czerwinski-chi04, roeser-rw24, killourhy-dsn09, behacom-dib20, focal-arxiv26, interbench, rt-app, schbench, hackbench, stress-ng, ananicy, ananicy-rules, cachyos-settings, darpa-optc, carat-top1000, plus untagged claims on typing data, HCI studies and these tools.

Record abbreviations (all paths under `_dev/research/jioh/`):
- `R01` = `2026-09-13-verification/reads/R01-interbench-rtapp-benchtools.md` (read 2026-09-13)
- `R06` = `2026-09-13-verification/reads/R06-ananicy.md` (read 2026-09-13)
- `R08` = `2026-09-13-verification/reads/R08-typing.md` (read 2026-09-13)
- `R10` = `2026-09-13-verification/reads/R10-task-switching.md` (read 2026-09-13)
- `R11F` = `2026-09-13-verification/reads/R11-focal-plain.md` (read 2026-09-13); `R11P` = `2026-09-13-verification/reads/R11-parts/plain-7-8-9.md`
- `K3` = `2026-09-13-verification/compare/K3.md` (its "[K3 check]" reads of the copies, 2026-09-13)
- `95S3` = `task-9.5-interactive-typing/search/S3-traces-datasets.md` (read 2026-09-13); `95CL` = `task-9.5-interactive-typing/changelog.md`
- `910S3` = `task-9.10-scenarios-timelines/search/S3-traces-datasets.md` (read 2026-10-01)
- `911S2` = `task-9.11-scheduler-constants/search/S2-project-docs.md` (read 2026-09-24)
- `912S2` = `task-9.12-related-work-prose/search/S2-project-docs.md`; `912S3` = `…/search/S3-traces-datasets.md`; `912A` = `…/search/A-audit.md`; `912CL` = `…/changelog.md`
- `915G2` = `task-9.15-docs-memos-and-guidebook-corrections/logs/G2.md` (read 2026-10-17)
- `R03` = `2026-09-13-verification/reads/R03-build-papers.md` (read 2026-09-13)

`docs/workload/source-vetting.md` is a record (append-only): lines 1–127 are the 2026-08-25/26 body, lines 129–198 its `## Correction (2026-10-17)`. A body statement the correction names is inventoried as corrected; a body statement it leaves standing is inventoried as a current claim (D-F2-30, D-F2-40).

---

### D-F2-01 — SWELL-KW population, setting and size
- source: `swell-icmi14` (docs/references.md:67, scholarly)
- repo: dataset/sources.yaml:44-46 — "25 students and interns doing knowledge-work tasks in a lab, ~3 h each, free composition on Windows (2012)"; also docs/references.md:69 — "25 students and interns doing knowledge-work tasks in a Windows 7 lab, 2012: ~3 h each … Sept–Nov 2012"; docs/workload/grounding-sources.md:43 — "25 students and interns doing knowledge-work tasks, Windows 7, 2012, about three hours each"; docs/workload/building-plan.md:205; docs/workload/measurement-overview.md:48-49 — "SWELL-KW was recorded on Windows in 2012"; docs/workload/source-vetting.md:176
- record: 910S3:214 — CaRR 2014 "We collected data from 25 participants … recruited among university students and interns at TNO"; :210 ICMI §3.4 "Windows 7 Professional … Office 2010"; :199/:284 Sept–Nov 2012; R10:233 ICMI §3.7 "25 students participated … interns from TNO and students from Delft"; manual "25 participants (~3 hours each)" (910S3:210); copy: DANS doi:10.17026/DANS-X55-69ZP v4.1, papers inside the deposit, read 2026-10-01 (910S3); paper PDF sha256 a10bffe9…, read 2026-09-13 (R10)
- slice: 9.10 (and the 2026-09-13 verification)
- dates: dataset/sources.yaml:44 last changed 2026-09-15 (9514b5e3); references.md:69 2026-10-16 (69c16f54); grounding-sources.md:43 2026-10-17 (c59b6a89); read 2026-09-13 / 2026-10-01; changed-after-read: yes (references.md:69 and grounding-sources.md:43 rewritten in 9.15 K01/K06; sources.yaml no)
- verdict: TRACED

### D-F2-02 — SWELL-KW log content: per-keystroke timestamps with focused application, pointer as click/drag/wheel only
- source: `swell-icmi14`
- repo: dataset/sources.yaml:40-42 — "per-keystroke and per-click/drag/wheel timestamps with the focused application"; :52-53 — "motion between pointer events not recorded"; also docs/references.md:69 — "Per-keystroke `TimeStamp` (100 ns digits) with `ControlApplication` and window title; mouse as click/drag/wheel only, no motion"; docs/workload/measurement-overview.md:48 — "keystrokes timestamped with the focused application"
- record: 95S3:256-262 — `<ControlApplication>iexplore</ControlApplication>` …; "Timestamps carry 100 ns digits … Mouse motion is not logged (only clicks/drags/wheel)" (reader's reading of the uLog files); copy: DANS v4, two uLog XML files with SHA-256, read 2026-09-13
- slice: 9.5
- dates: sources.yaml:40 2026-09-15; read 2026-09-13; changed-after-read: yes for references.md:69 (2026-10-16, 69c16f54); no for sources.yaml
- verdict: TRACED

### D-F2-03 — SWELL-KW licence and access
- source: `swell-icmi14`
- repo: dataset/sources.yaml:39-40 — "DANS doi:10.17026/dans-x55-69zp v4, CC-BY-NC-SA-4.0"; also docs/references.md:68 — "version 4 (2025-06-04), CC-BY-NC-SA-4.0, no access request"; grounding-sources.md:43, :89 — "the DANS record open access under CC BY-NC-SA 4.0"; source-vetting.md:176 — "open access … no request or registration needed"; building-plan.md:205; dataset/README.md:218; measurement-overview.md:65
- record: 95S3:250 — "licence CC-BY-NC-SA-4.0 … No access request was required (`fileAccessRequest: False`)"; R10:240 — `"license": {"name": "CC-BY-NC-SA-4.0"…}`, `"fileAccessRequest": false`, DataCite "openAccess"; copy: DANS Dataverse API v4 (releaseTime 2025-06-04), read 2026-09-13
- slice: 9.5
- dates: references.md:68 2026-09-14 (0cd74d3e); read 2026-09-13; changed-after-read: yes (references.md:68 written the day after the read, from it; source-vetting.md:176 2026-10-17)
- verdict: TRACED

### D-F2-04 — Which SWELL-KW blocks each replayed stream comes from
- source: `swell-icmi14:outlook-c23` (also `word-c1`, `ie-c1`)
- repo: dataset/sources.yaml:48-50 — "word-c1 (Word, neutral condition), outlook-c23 (Outlook, interruption conditions; no c1 keystrokes), ie-c1 (Internet Explorer, neutral)"
- record: 95CL:63 (D12, 2026-09-14) — "c2 and c3 for Outlook, which has no keystrokes in c1 (the e-mail task belongs to the interruption conditions)"; the primary: 910S3:234 (reader's parsing, from the deposit's per-minute sheets) — "the reader therefore reads `c` as the block number … block 1 is always condition N"; R10:232 ICMI §3.1 — "• Neutral … • Stressor 'Time pressure' … • Stressor 'Interruptions': 8 emails were sent", "The neutral condition was always the first condition", the other two "in counterbalanced order" (R10 C-swell-1 reading)
- slice: 9.5 (D12) against 9.10 (S3-01) and the 2026-09-13 verification
- dates: sources.yaml:49 last changed 2026-09-15 (9514b5e3); read 2026-09-14 (D12), 2026-10-01 (S3-01); changed-after-read: no
- verdict: WORDING-OUTSIDE-PASSAGE
- finding: the repo calls blocks c2 and c3 "interruption conditions"; the paper's three conditions are neutral, e-mail interruptions and time pressure, and per 9.10 S3-01 `c` is the block number, block 1 always neutral and blocks 2 and 3 one interruption block and one time-pressure block in counterbalanced order. Fix: "outlook-c23 (Outlook, blocks 2 and 3 — the e-mail-interruption and time-pressure conditions, in counterbalanced order; no block-1 keystrokes)". The 9.5 D12 wording carries the same slip.

### D-F2-05 — SWELL-KW timestamps quantised at the 15.6 ms Windows tick
- source: `swell-icmi14`
- repo: dataset/sources.yaml:52 — "Timestamps quantised at the 15.6 ms Windows tick"; also dataset/archetypes.yaml:111, :184, :355, :494 — "the recordings' timestamps are quantised at 15.6 ms"
- record: 95CL:63 (D12) — "timestamps quantised at the 15.6 ms Windows timer tick (82 % of Word gaps on a multiple), 7 % zero gaps … (all 76 logs, `swell_streams.py`)" — the reader's computation over the copy
- slice: 9.5
- dates: sources.yaml:52 2026-09-15; archetypes.yaml:111 2026-10-05 (626c27a6, a re-fold, sentence unchanged); read 2026-09-14; changed-after-read: no (the sentence)
- verdict: TRACED (a computation over the data, recorded with its method; the repo drops the record's "82 % of Word gaps on a multiple")

### D-F2-06 — SWELL-KW focus-sequence figures (dwell median 9.1 s, A → B → A returns 83.4 %)
- source: `swell-icmi14`
- repo: docs/workload/building-plan.md:205 — "a dwell median of 9.1 s per focus episode, A → B → A returns after 83.4 % of middle episodes (the reader's computations)"; also grounding-sources.md:43; references.md:69
- record: 910S3:244 — "Dwell per focus episode, pooled … median 9.1"; :246 — "5,124 of 6,147 middle episodes (83.4 %) are followed by a return to the preceding application"; labelled "Reader's own computations" (:242); copy: DANS v4.1, 76 raw uLog files, read 2026-10-01
- slice: 9.10
- dates: building-plan.md:205 2026-10-16 (34b09357); read 2026-10-01; changed-after-read: yes (9.15 K02 wrote it)
- verdict: TRACED (labelled as the reader's computation — the label is present and honest)

### D-F2-07 — 136M Keystrokes data artifact: file, fields, rows, licence
- source: `dhakal-chi18` (docs/references.md:37, scholarly)
- repo: docs/references.md:38 — "`data/Keystrokes.zip` (1 572 785 433 bytes, Last-Modified 2018-03-29, ETag …); per-keystroke PRESS_TIME/RELEASE_TIME in ms, 15 transcribed sentences per participant — … the released `metadata_participants.txt` 168 594 rows; licence per readme.txt line 21, 'free to use for non-commercial use in your own research or projects with attribution to the authors'"; also dataset/README.md:218 — "free for non-commercial use in research or projects with attribution to its authors"
- record: 95S3:70 — "`Content-Length: 1572785433`, `Last-Modified: Thu, 29 Mar 2018 …`"; :77 `readme.txt:21` "You are free to use this data for non-commercial use in your own research or projects with attribution to the authors."; :78 PRESS_TIME/RELEASE_TIME "(in ms)"; :89 "168,594 rows"; copy: userinterfaces.aalto.fi/136Mkeystrokes, range-fetched, SHA-256 listed, read 2026-09-13
- slice: 9.5
- dates: references.md:38 2026-10-16 (69c16f54); README.md:218 2026-10-16 (7172a1a4); read 2026-09-13; changed-after-read: yes
- verdict: TRACED (references.md:38's quoted licence words paraphrase readme.txt:21 inside quotation marks: "free to use for non-commercial use" vs the file's "You are free to use this data for non-commercial use" — see pointer notes)

### D-F2-08 — 136M Keystrokes paper figures and population
- source: `dhakal-chi18`
- repo: docs/references.md:39 — "self-selected online volunteers transcribing 15 memorised English sentences on their own devices; the mean of per-participant average inter-key intervals, 238.66 ms, SD 111.60 across participants; skew 1.98 and kurtosis 7.1 describe that across-participant distribution … IKIs over 5 000 ms dropped, so within-sentence pauses up to 5 s remain; mouse editing allowed but not logged"; :38 "the paper's final dataset 168 960 participants"
- record: R08:45-46 — "Average inter-key interval is 238.656 ms (SD = 111.6) … skewness of 1.98 and kurtosis measure of 7.1"; :48 "we removed keystrokes that were typed more than 5000 ms after the previous keystroke"; :50 "136,857,600 keystrokes from 168,960 participants"; :59 dataset check: the statistics are across participants; :125 "first read through and memorise a sentence"; :132 "they allowed use of the mouse … From log data it is difficult to assess"; copy: CHI 2018 PDF sha256 e5e72fac…, read 2026-09-13
- slice: other (the 2026-09-13 verification)
- dates: references.md:39 2026-10-16 (69c16f54); read 2026-09-13; changed-after-read: yes
- verdict: TRACED

### D-F2-09 — Gap shares: 136M sample 0.7 % over 1 s vs SWELL-KW Word stream 5.5 %
- source: `dhakal-chi18` / `swell-icmi14`
- repo: docs/references.md:39 — "(D6's alternative not taken: transcription of memorised sentences, share of gaps over 1 s 0.7 % on a six-participant sample against 5.5 % between the keys of SWELL-KW's Word stream, `dataset/stimulus/swell-word-c1.jsonl`)"
- record: 95S3:86 — "Within-sentence press-to-press: n=4173 … share>1 s 0.0072" (six participants, reader's computation); 95CL:827-829 (D98, 2026-09-29) — "5.5 % of the 78,013 gaps between keys"; the alternative not taken is 95CL:21 (D4) — "Alternatives not taken: the 136M Keystrokes data (S3-aalto136m; transcription of memorised sentences, share > 1 s 0.7 %)"
- slice: 9.5
- dates: references.md:39 2026-10-16; read 2026-09-13 / 2026-09-29; changed-after-read: yes
- verdict: TRACED (values); pointer slip — see pointer notes ("D6" is 9.5 D4)

### D-F2-10 — González & Mark 2004: ~3 min per event, its unit and scope
- source: `gonzalez-chi04` (docs/references.md:42, scholarly)
- repo: dataset/sources.yaml:160-162 — "~3 min (3 min 08 s) per event — one continuous use of a device or one interaction with a person, formal meetings excluded"; also references.md:44; building-plan.md:203; grounding-sources.md:40; source-vetting.md:139
- record: R10:89 — Table 2 (p. 116) row "All events except 'Formal meetings' and 'Other'": "0:03:08 (0:02:27)"; p. 115 event definition "any continuous use of a device or engagement in an interaction with other individuals"; copy: ics.uci.edu/~gmark/CHI2004.pdf sha256 988981bf…, read 2026-09-13
- slice: other (2026-09-13 verification; 9.10 D35 adopts it)
- dates: sources.yaml:161 2026-10-17 (7b024003); read 2026-09-13; changed-after-read: yes (9.15 rewrote "~3 min per task" to "per event")
- verdict: TRACED (the repo names "formal meetings excluded"; the row also excludes "Other")

### D-F2-11 — González & Mark 2004: 11 min 28 s mean working-sphere segment and its companions
- source: `gonzalez-chi04`
- repo: dataset/sources.yaml:162-166 — "11 min 28 s, the mean continuous segment in a working sphere before switching, central and peripheral spheres only (13 min 49 s over all spheres; 12 min 18 s when switches shorter than 2 min are ignored; the paper's average time per working sphere is 33 min 32 s)"; also references.md:44; building-plan.md:203; grounding-sources.md:40; source-vetting.md:139, :174; dataset/timelines/coreset/c6-dual.timeline.yaml:32-33; docs/workload/coreset-guide.md:1091
- record: R10:74 — Table 4 "Central and Peripheral WS only" … "Avg. Time / segment (sd) '0:11:28 (0:10:54)'", "All / All" "0:13:49"; :75 "about 33 min. 32 sec. per working sphere"; :76 Table 5 "Both / All" "0:12:18"; copy as D-F2-10
- slice: other (2026-09-13 verification, C-gonzalez-1; 9.10 D35)
- dates: sources.yaml:163 2026-10-17; c6-dual:33 2026-10-11 (39d8d815); read 2026-09-13; changed-after-read: yes
- verdict: TRACED

### D-F2-12 — González & Mark 2004: spheres per day, time per tool, statistics, population
- source: `gonzalez-chi04`
- repo: dataset/sources.yaml:166-169 — "Also ~10 spheres per person-day and ~2 min 11 s per tool/document before switching. Means and SDs only, 14 shadowed knowledge workers."; grounding-sources.md:40 — "A shadowing study of information workers; means and SDs"
- record: R10:83 — "each person worked on an average of ten working spheres per day"; :95 "People spent an average of 2 min. 11 sec. working with any device or paper"; :101 "Twenty-five information workers form the team …"; :103 "N = 14 … Every table gives means with SDs"
- slice: other (2026-09-13 verification)
- dates: sources.yaml:168-169 2026-10-17 (7b024003; "knowledge workers" carried over from the 2026-08 text); read 2026-09-13; changed-after-read: yes (the sentence was rewritten; the population word was not)
- verdict: WORDING-OUTSIDE-PASSAGE
- finding: sources.yaml:169 says "knowledge workers"; the paper's population word is "information workers" (R10:101), which grounding-sources.md:40 uses. Fix: "14 shadowed information workers".

### D-F2-13 — c6-dual's focus alternation: 688 s, and the parts labelled design
- source: `gonzalez-chi04` (value); design (the rest)
- repo: dataset/timelines/coreset/c6-dual.timeline.yaml:32-34 — "the focus alternates between the editor and the game every 688 s — the mean continuous segment in a working sphere before switching, 11 min 28 s (gonzalez-chi04; 9.10 C-gonzalez-1); the regular alternation, the editor first and the typing's 2 s lead-in are design"; also coreset-guide.md:1091; grounding-sources.md:36, :40; building-plan.md:256; source-vetting.md:174, :188; references.md:44
- record: R10:74 (11 min 28 s = 688 s, arithmetic); 9.17 changelog D1 (task-9.17-focus-in-the-telemetry/changelog.md:11) records the design parts
- slice: other (2026-09-13 verification; 9.17)
- dates: c6-dual:33 2026-10-11; read 2026-09-13; changed-after-read: yes (9.17 wrote it)
- verdict: LABELLED (the regular alternation, the editor first and the 2 s lead-in carry "design"; label present and honest; 688 s = 11 × 60 + 28)
- note: "9.10 C-gonzalez-1" names the 2026-09-13 verification's claim id that 9.10 D35 cites — see pointer notes.

### D-F2-14 — Mark, González & Harris 2005: ~11 min per sphere segment, informants
- source: `mark-chi05` (docs/references.md:47, scholarly)
- repo: docs/references.md:49 — "about 11 min (11 min 4 s, SD 18 min 9 s) in a central or peripheral working sphere before switching or being interrupted (p. 324); its 24 informants include CHI 2004's 14 (p. 323)"; also building-plan.md:203; grounding-sources.md:41; source-vetting.md:76
- record: R10:136 — p. 324 "The average length of time that the informants spent in central and peripheral working spheres was 11 min. 4 sec., (sd=18 min. 9 sec.) before switching to another working sphere or being interrupted"; :138 p. 323 "Fourteen members from the JEB team were shadowed and in the second phase ten members of the AUG team"; copy: ics.uci.edu/~gmark/CHI2005.pdf sha256 ec8ae49c…, read 2026-09-13
- slice: other (2026-09-13 verification)
- dates: references.md:49 2026-10-16; grounding-sources.md:41 2026-10-17; read 2026-09-13; changed-after-read: yes
- verdict: TRACED

### D-F2-15 — Mark et al. 2005: internal/external interruption split and the Table 3 inconsistency
- source: `mark-chi05`
- repo: docs/references.md:49 — "Internal and external interruptions are roughly equal overall and for analysts and developers; managers 59.2 % external, 40.8 % internal (p. 326). The printed column split, 52.0 % internal / 48.0 % external, conflicts with Table 3's own cells, which imply about 48/52; this 52.0 % is a self-initiated share of interruptions, not of switches."
- record: R10:147 — Table 3 "Column avg. 52.0% | 48.0% | 100%"; :148 "Managers are more likely to experience external interruptions (59.2%) than internal interruptions (40.8%), whereas analysts and developers experience internal and external interruptions about equally"; :153 reader's arithmetic "imply about 48% internal and 52% external"; :159 "no self-initiated share of all working-sphere switches"
- slice: other (2026-09-13 verification)
- dates: references.md:49 2026-10-16; read 2026-09-13; changed-after-read: yes
- verdict: TRACED

### D-F2-16 — Same-day resumption (CHI 2005) and the 23 min 15 s figure
- source: `mark-chi05`; untagged (the 2006 Gallup interview; CHI 2008 and CHI 2014 papers)
- repo: docs/references.md:49 — "Interrupted work resumed the same day 77.2 % of the time, after 25 min 26 s on average (SD 54 min 48 s) (p. 326)"; docs/workload/source-vetting.md:173 — "the 23 min 15 s figure is absent from the four Mark et al. CHI papers searched … and CHI 2005 reports a comparable 25 min 26 s"; source-vetting.md:76 (body) — "CHI 2008 … contains neither figure"; "The CHI 2014 rhythm-of-attention paper does not contain the '~half of switches self-initiated' claim"
- record: R10:222 — p. 326 "77.2% of interrupted work was resumed on the same day." "… an average length of time of 25 min. 26 sec (sd=54 min. 48 sec.)"; :224 "This figure is not in any of the four Mark et al. CHI papers read here" (search terms listed); mark-chi08 and mark-chi14 sections of R10 (from :160, :181)
- slice: other (2026-09-13 verification)
- dates: source-vetting.md:173 2026-10-17 (c59b6a89); :76 2026-08-26; read 2026-09-13; changed-after-read: yes (:173)
- verdict: TRACED

### D-F2-17 — Czerwinski, Horvitz & Wilhite 2004: what the study is
- source: `czerwinski-chi04` (docs/references.md:52, scholarly)
- repo: docs/workload/grounding-sources.md:42 — "A one-week self-report diary of user-defined tasks (10 people analysed), reporting means and SDs | Task-switch and interruption means; it is not a log study of app-switching distributions"; also references.md:54; source-vetting.md:173
- record: R10:209 — "Self-report diary kept for one work week by 11 people, analysed for 10. The unit is a user-defined task … mean 53 min (SD 90.9) … 40% of switches self-initiated. Mean 0.7 interruptions per task"; copy: interruptions.net PDF pp. 175–182 sha256 42aebba4…, read 2026-09-13
- slice: other (2026-09-13 verification)
- dates: grounding-sources.md:42 2026-10-17; read 2026-09-13; changed-after-read: yes
- verdict: TRACED

### D-F2-18 — Roeser et al.: task, sample, model and Table 3 values
- source: `roeser-rw24` (docs/references.md:57, scholarly)
- repo: docs/references.md:59 — "Inputlog copy task: 250 Dutch participants aged 18 to 25 fitted; data and code on OSF (osf.io/y3p4d, 1 662 subjects, CC0). A two-component log-normal mixture fixed by assumption … only one- versus two-component models compared. Table 3 … LF bigrams fluent location 158 ms [139, 180] as the posterior mean of the back-transformed log location, disfluency slowdown 95 ms, disfluency probability 0.34; consonants 429 ms, 414 ms, 0.73; fluent spread 0.29 in both tasks"; building-plan.md:256 — "`roeser-rw24` ground[s] no dataset value"
- record: R08:226 "Fixed at two by the authors … Only one-component models (M1, M2) and two-component models (M3, M4) were compared"; :230 "250 participants aged 18–25 doing the Dutch Inputlog copy task"; :244-248 Table 3 "β (fluent typing) 158 [139, 180] 429 [356, 515]", "δ … 95 … 414", "θ … 0.34 … 0.73", "σ²e (fluent typing) 0.29 … 0.29"; :268 "Table 3 nevertheless reports β in milliseconds, so a back-transformation was applied"; :392 OSF "CC0 1.0 Universal"; 95S3:189 "1,662 distinct `subj`"; copy: Springer VoR via Wayback 2021-08-25 + author manuscript, read 2026-09-13
- slice: other (2026-09-13 verification) and 9.5
- dates: references.md:59 2026-09-14 (647f477d); read 2026-09-13; changed-after-read: yes (written the day after the read, from it)
- verdict: TRACED ("fluent spread 0.29" is the table's σ²e, a variance on the log scale — see pointer notes)

### D-F2-19 — CMU keystroke benchmark (Killourhy & Maxion): what the dataset is
- source: `killourhy-dsn09` (docs/references.md:62, scholarly)
- repo: docs/references.md:64 — "public raw per-keystroke latency dataset (cs.cmu.edu/~keystroke) for direct empirical fits if needed. Caveat: single practiced password, lab setting." (No dataset doc cites it.)
- record: 95S3:131-147 — "51 subjects (typists), each typing a password (.tie5Roanl) 400 times"; "feature table only (no raw timestamps): hold, down-down and up-down latencies"; copy: cs.cmu.edu/~keystroke page + `DSL-StrongPasswordData.csv` sha256 b11d2353…, read 2026-09-13
- slice: 9.5
- dates: references.md:64 2026-08-26 (b0ff9cb1); read 2026-09-13; changed-after-read: no
- verdict: TRACED (latencies per keystroke; "raw" stretches a feature table with no timestamps — see pointer notes)

### D-F2-20 — BEHACOM: users, platforms, period, fields, deposit
- source: `behacom-dib20` (docs/references.md:72, scholarly)
- repo: docs/workload/grounding-sources.md:44 — "Per-minute application-usage vectors of 12 users on their own computers (eight on Windows, three on Linux, one on both), 2019–2020: the foreground executable name and the switches between applications per minute"; also :62 — "BEHACOM per minute from natural use on Linux and Windows"; building-plan.md:205; references.md:73-74 (Mendeley v2, CC BY 4.0, 37 414 157 bytes, SHA-256 92e1b44b…; `current_app`, `changes_between_apps`; "No window titles, no sub-minute timestamps"); source-vetting.md:187
- record: 910S3:292 §2.1 "Eight of them use Windows as operating system, three Linux, and one both", first/last timestamps Nov 2019 – Jan 2020; Table 5 `current_app`, `changes_between_apps`; :289 zip size and SHA-256; :303 "real users' own Windows and Linux (X11) computers … no window titles … no sub-minute timestamps"; R11P:193 "twelve different individuals interacting for fifty-five consecutive days with their personal computers"; copy: Mendeley Data v2 + PMC7270191, read 2026-10-01
- slice: 9.10
- dates: grounding-sources.md:44 2026-10-17; references.md:74 2026-10-16; read 2026-10-01; changed-after-read: yes
- verdict: TRACED

### D-F2-21 — DesktopBench: sessions composed from templates, the A → B → A split, session counts
- source: `focal-arxiv26` (docs/references.md:77, scholarly preprint)
- repo: docs/workload/grounding-sources.md:45 — "Multitask and interruption sessions with app names and window titles, composed from templates over VideoGUI's single-task actions, not observed"; also building-plan.md:204; references.md:79 (quotes p. 5 and §4.1; "320 multitask + 100 interruption sessions"); source-vetting.md:84 (body: "Multitask (320 sessions, 20 interleaved cross-app templates) and Interruption (100 sessions …)"), :177
- record: 910S3:325 — §4.1 "We therefore augment each action with the foreground application name (app) and window title (title)" / "Sessions are assembled through template-based composition grounded in realistic creative workflows"; p. 5 "an 𝐴→𝐵→𝐴 split in which a long-running creative task 𝐴 is interrupted by a short YouTube browsing task 𝐵"; §4.3 "320 in DesktopBench-Multitask and 100 in DesktopBench-Interruption"; R11F:285 "sampling one of 20 family patterns"; copy: arXiv:2604.19541 v2 PDF sha256 fb5742cf…, read 2026-10-01
- slice: 9.10
- dates: grounding-sources.md:45 2026-10-17; read 2026-10-01; changed-after-read: yes
- verdict: TRACED

### D-F2-22 — DesktopBench release: fixed 6.0 s per action, HuggingFace v0.1.0, terms, preprint
- source: `focal-arxiv26`
- repo: docs/references.md:79 — "the release's only timestamps are synthetic, a fixed 6.0 s per action, dropped before use … released on HuggingFace `HaoranYin/desktopbench` v0.1.0; data terms restrictive — research inspection only, no redistribution; scripts MIT"; also grounding-sources.md:45, :87; building-plan.md:204 — "its inter-action timings are a fixed 6.0 s"; source-vetting.md:177; references.md:78 "(v2, 2026-07-18). Preprint — no venue."
- record: R11F:344 — `scripts/prepare_videogui_raw_from_hf.py` line 212 `duration = 6.0`; `rebuild_desktopbench.py` `DROP_FIELDS = {"timestamp", "duration", …}`; :314-323 "Scripts are MIT licensed … available for research inspection … no redistribution, sublicensing, or republication license"; :15 HF commit 49c36830 = tag v0.1.0; copy read 2026-09-13
- slice: other (2026-09-13 verification)
- dates: references.md:79 2026-10-16; building-plan.md:204 2026-10-17 (2f9f8a0b); read 2026-09-13; changed-after-read: yes
- verdict: TRACED

### D-F2-23 — interbench pin, version and licence
- source: `interbench` (docs/references.md:169, deployed-system)
- repo: docs/references.md:170 — "master commit e612a65 (2016-10-24), version string 0.31; its load defaults differ from tag v0.31. Licence GPL-2.0-or-later per the source headers; COPYING is GPLv2 and a GPLv3 LICENSE file also ships, which GitHub reports"; also source-vetting.md:162, :182
- record: R01:9 — master `e612a65…` "commit 2016-10-24"; :264 `interbench.c:7-10` "either version 2 of the License, or (at your option) any later version"; :265 COPYING GPLv2, LICENSE GPLv3; :268 GitHub API `gpl-3.0`; copy: git clone, read 2026-09-13
- slice: other (2026-09-13 verification)
- dates: references.md:170 2026-09-14 (c21bb817); read 2026-09-13; changed-after-read: yes (written the day after the read, from it)
- verdict: TRACED

### D-F2-24 — interbench: what it emulates and measures
- source: `interbench`
- repo: docs/workload/grounding-sources.md:27 — "Emulates interactive tasks (audio, video, X, gaming) under background loads (Burn: CPU-bound threads; Write: streaming disk writes; compile-like), measuring latency, jitter, missed deadlines … its gaming load uses as much CPU as it can get, with no deadlines"
- record: R01:106 `interbench.8:95-101` "This load simply uses as much cpu as it can get. It does not return deadlines met as there are no deadlines"; :127 Burn "A configurable number of threads fully cpu bound"; Write C-interbench-6 (:140-153) sequential streaming writes; :189 Compile "Simulating a heavy 'make -j4' compilation by running Burn, Write and Read concurrently"; :234-236 reported latency, "standard deviation of the latency", "Percentage of deadlines met"; copy as D-F2-23
- slice: other (2026-09-13 verification)
- dates: grounding-sources.md:27 last changed 2026-10-17 (c59b6a89) in its third column only; the "what it is" cell unchanged since 2026-08; read 2026-09-13; changed-after-read: no (the claim's wording)
- verdict: TRACED

### D-F2-25 — interbench's interactive constants and the Video wording
- source: `interbench`
- repo: docs/references.md:171 — "Its Audio (50 ms @ 5%), Video (16.7 ms @ 40%) and X (0–100% variable) interactive emulations are no longer cited by the dataset"; also source-vetting.md:142 — "(audio 50 ms at 5 %, video 16.7 ms at 40 %, X 0–100 %)"; :162 — "the Video task 'tries to receive cpu 60 times per second'"
- record: R01:57 reading "Period 50 ms … the docs express as '5% cpu'"; :63 `interbench.8:89-93` "Video is simulated as a thread that tries to receive cpu 60 times per second and uses 40% cpu"; :79 "X is simulated as a thread that uses a variable amount of cpu ranging from 0 to 100%"; also 911S2:692 (S2-15 coverage, copy at e612a65, read 2026-09-24)
- slice: other (2026-09-13 verification); 9.11
- dates: references.md:171 2026-10-16; source-vetting.md:142/162 2026-10-17; read 2026-09-13; changed-after-read: yes
- verdict: TRACED

### D-F2-26 — interbench: missed-period handling (cited for the TIMER memo)
- source: `interbench`
- repo: docs/references.md:171 — "how those emulations treat a missed period — counted as missed deadlines, the deadline moved past the current time by whole periods, the burn bypassed (`interbench.c:398–436` at `e612a65`)"
- record: 911S2:649-667 — `interbench.c:398-411`, `:418-436` verbatim; :692 coverage "a missed period is counted as missed deadline(s) and the deadline is advanced by whole intervals past 'now' … if missed before running, the burn is skipped"; copy: git clone at e612a65, SHA-256 of interbench.c a381b940…, read 2026-09-24
- slice: 9.11
- dates: references.md:171 2026-10-16; read 2026-09-24; changed-after-read: yes
- verdict: TRACED

### D-F2-27 — interbench Burn default and the ~7 ms jitter figure
- source: `interbench`
- repo: docs/workload/source-vetting.md:162 — "Burn defaults to the online CPU count, 4 being the man page's … Its '~7 ms' jitter figure is the program's own, stated without a source in its man page, readmes and code — not a human-perception threshold"
- record: R01:127-136 — `interbench.8:120-121` "(4 by default)"; `interbench.c:1520` `ud.cpu_load = sysconf(_SC_NPROCESSORS_ONLN);`; 911S2:690 `interbench.8:206-209` "Average humans' limit of perception for jitter is in the order of 7ms"; :692 "with no source cited in the man page, readme or code (grep of `readme`, …)"
- slice: other (2026-09-13 verification); 9.11
- dates: source-vetting.md:162 2026-10-17; read 2026-09-13 / 2026-09-24; changed-after-read: yes
- verdict: TRACED

### D-F2-28 — interbench packaging and usage precedents
- source: `interbench`; LWN 725238 and 1051430 (untagged here)
- repo: docs/workload/source-vetting.md:181 — "interbench's packaging is Gentoo, FreeBSD ports, AUR, GNU Guix, openSUSE Leap, Void, AOSC and LiGurOS — no Debian package was found"; :141 — "The precedent holds for hackbench and rt-app (LWN 725238) and as an LWN mention for stress-ng (LWN 1051430); none was found for interbench"
- record: R01:272 — Repology lists `aosc`, `aur`, `freebsd`, `gentoo`, `gnuguix`, `liguros_*`, `opensuse_leap_*`, `void_x86_64`; :407 LWN 725238 "Today, ARM and Linaro are using rt-app"; :440 LWN 725238 on hackbench; :442 LWN 1051430 "(e.g. stress-ng and hackbench)"
- slice: other (2026-09-13 verification)
- dates: source-vetting.md:181 2026-10-17; read 2026-09-13; changed-after-read: yes
- verdict: TRACED

### D-F2-29 — interbench's Burn/Write/Read/Memload/Hack/Custom loads as the vetting body lists them (left standing)
- source: `interbench`
- repo: docs/workload/source-vetting.md:52 (body; not named by the correction's line-52 item beyond Burn, Video, the ~7 ms figure and the licence) — "Background loads: None; Video; X; **Burn** (4 CPU-bound threads default); **Write** (streaming write, RAM-sized file); **Read** (RAM-sized file, cache-defeating); **Compile** (…); **Memload** (110% RAM); Hack (hackbench 50) … 30 s default duration"
- record: R01:150 (C-interbench-6) "master code sets `filesize = 1000000` kB … effectively always capped at ~1 GB, regardless of RAM size"; :170 (C-interbench-7) "at master the file size is `ud.filesize` = 1 000 000 kB … at tag v0.31 it was MemTotal"; R01 C-interbench-10 (:197-231) "at master it uses `ud.cpu_load` groups … the `Hack` entry has `.load = 0, .rtload = 0` … so it never runs"; "Ring: present in code at master, enabled, but absent from the man page and readme"
- slice: other (2026-09-13 verification)
- dates: source-vetting.md:52 2026-08-25 (9313c284); read 2026-09-13; changed-after-read: no
- verdict: WORDING-OUTSIDE-PASSAGE
- finding: the body's Write/Read "RAM-sized file", "Hack (hackbench 50)" and the load list without Ring are the man page's and tag v0.31's; at the pinned master `e612a65` (the pin the correction states at :162, :182) Write and Read cap their file at about 1 GB, Hack runs `cpu_load` groups and never runs, and an undocumented Ring load exists. Fix: extend the correction's line-52 item: "the load list and sizes are the man page's; at `e612a65` Write and Read use a file capped at about 1 GB, Hack is never run, and a Ring load the docs omit exists".

### D-F2-30 — rt-app pin and licence
- source: `rt-app` (docs/references.md:174, deployed-system)
- repo: docs/references.md:175 — "commit `d6f8be41…` (2026-06-10) … every `src/` file that carries a header grants GPL version 2 'or (at your option) any later version' … `libdl/dl_syscalls.h` grants version 2 only; `src/rt-app_taskgroups.c`, `src/rt-app_taskgroups.h` and `libdl/dl_syscalls.c` carry no header; `COPYING.in` is the GPL version 2 text"; also source-vetting.md:182, :198
- record: 911S2:614 — clone at `d6f8be41…` (committed 2026-06-10), read 2026-09-24; 915G2:1-15, :50 — per-file licence read at `d6f8be4` on 2026-10-17 ("Version 2 only: `libdl/dl_syscalls.h` (lines 6–7 …)"; `git get-tar-commit-id`)
- slice: 9.11; 9.15 (the licence read)
- dates: references.md:175 2026-10-17 (6f508a59); read 2026-10-17; changed-after-read: no (written from that day's read)
- verdict: TRACED

### D-F2-31 — rt-app's JSON task model as the schema precedent
- source: `rt-app`
- repo: docs/references.md:176 — "JSON task-model precedent (run/period/deadline in µs); schema-shape citation for archetypes and the TIMER primitive (`timer{ref,period}`)"; also archetype-plan.md:10 — "rt-app cited as the schema precedent, including `timer{ref,period}` for TIMER"; building-plan.md:52 — "Format follows the rt-app JSON task model as explicit precedent"; grounding-sources.md:26 — "Reproducible workload simulator; JSON specs of periodic tasks (period, runtime, deadline)"; source-vetting.md:143, :163 (loop/instance are counts; policy set omits SCHED_BATCH/SCHED_IDLE; `period`/`deadline` legacy spellings of `dl-period`/`dl-deadline`)
- record: R01:307-313 — policy values "SCHED_OTHER", "SCHED_BATCH", "SCHED_IDLE", …; `dl-period … The unit is usec`; reading "`run`, `runtime`, `sleep`, timer `period` … in microseconds"; K1:349 `tutorial.txt:229-235` "For backward compatibility, the key 'period' will also be checked"; 911S2:617 `tutorial.txt:447-452` the timer event
- slice: other (2026-09-13 verification); 9.11
- dates: references.md:176 2026-08-26 (b0ff9cb1); archetype-plan.md:10 2026-08-27; building-plan.md:52 2026-10-17 (97b6e29d, the sentence kept); read 2026-09-13; changed-after-read: no
- verdict: TRACED

### D-F2-32 — rt-app users and documentation references
- source: `rt-app`; LWN 725238 (untagged)
- repo: docs/workload/grounding-sources.md:26 — "rt-app (scheduler-tools; used by ARM and Linaro, per LWN)"; source-vetting.md:87 (body) — "rt-app: referenced in kernel deadline docs"; source-vetting.md:55 (body, left standing) — "doc/examples/template.json: wake every 100 ms, run 10 ms, SCHED_OTHER, 6 s"
- record: R01:407 — LWN 725238 "Today, ARM and Linaro are using rt-app to trigger specific scheduler code paths"; :409 "Kernel documentation references rt-app: yes, `Documentation/scheduler/sched-deadline.rst` Appendix A"; :394 template "run 10 000 µs … timer with 100 000 µs period … SCHED_OTHER … 6 s global duration"
- slice: other (2026-09-13 verification)
- dates: grounding-sources.md:26 2026-10-17; source-vetting.md:55/87 2026-08-25; read 2026-09-13; changed-after-read: yes (:26)
- verdict: TRACED

### D-F2-33 — schbench pin, authorship and licence
- source: `schbench` (docs/references.md:179, deployed-system)
- repo: docs/references.md:180 — "git.kernel.org/…/mason/schbench.git, tag `v1.0` (commit `ab22f3f8`, 2023-04-17), its only tag; github.com/masoncl/schbench continues the same history without tags. 'Copyright (C) 2016 Facebook', GPLv2"; also grounding-sources.md:28 "(Mason, 2016)"; source-vetting.md:164, :182
- record: 911S2:728 — "only tag `v1.0` → `ab22f3f8…` (2023-04-17)"; :737 `schbench.c:1-7` "Copyright (C) 2016 Facebook … GPLv2"; :743 GitHub "`git ls-remote --tags` returned no tags; kernel.org HEAD 6300b8f is an ancestor"; read 2026-09-24
- slice: 9.11
- dates: references.md:180 2026-10-08 (232ae0ed); read 2026-09-24; changed-after-read: yes (written from the read)
- verdict: TRACED

### D-F2-34 — schbench's printed percentiles and its request
- source: `schbench`
- repo: docs/references.md:181 — "at v1.0 it prints wakeup and request latency at p50/p90/p99/p99.9, p99 marked in its output, and requests per second at p20/p50/p90 … its 2016 first version printed p50/75/90/95/99/99.5/99.9"; also grounding-sources.md:28; source-vetting.md:164 — "v1.0 does one `usleep(100)` per request"; source-vetting.md:58 (body, left standing) — "Message threads + worker threads; … matrix math; per-CPU spinlock"
- record: 911S2:733-736 `schbench.c:59@36d859a` "{ 50.0, 75.0, 90.0, 95.0, 99.0, 99.5, 99.9 }"; `schbench.c:101-104@v1.0` PLIST_FOR_LAT / PLIST_FOR_RPS; R01:485 "A request … = `usleep(100)` … followed by `do_work`: take a per-CPU lock … matrix math"
- slice: 9.11; other (2026-09-13 verification)
- dates: references.md:181 2026-10-07 (8a3e7489); read 2026-09-24; changed-after-read: yes
- verdict: TRACED

### D-F2-35 — SchedCP cites schbench at kernel.googlesource.com
- source: `schbench` (the SchedCP reference list)
- repo: docs/references.md:181 — "Cited in SchedCP's references by kernel.googlesource.com/pub/scm/linux/kernel/git/mason/schbench"; also grounding-sources.md:28 "a citation precedent (SchedCP cites it)"; source-vetting.md:141, :164, :181
- record: R03:218 — "[12] Chris Mason. schbench: Scheduler benchmark. https://kernel.googlesource.com/pub/scm/linux/kernel/git/mason/schbench, 2016."; read 2026-09-13
- slice: other (2026-09-13 verification)
- dates: references.md:181 2026-10-07; read 2026-09-13; changed-after-read: yes
- verdict: TRACED

### D-F2-36 — hackbench pin, purpose, defaults and output
- source: `hackbench` (docs/references.md:184, deployed-system)
- repo: docs/references.md:185-186 — "tag `v2.11` (commit `62da2bef`) … Purpose in the man page's words: 'Hackbench is both a benchmark and a stress test …' Defaults read from the source: `datasize = 100`, `loops = 100`, `num_groups = 10`, `num_fds = 20` … 10 × 20 × 2 = 400. Reports a single completion time"; also grounding-sources.md:29; source-vetting.md:61 (body: "10 groups × 40 fds = 400 tasks, 100 msgs × 100 B"), :165
- record: 911S2:749-755 — clone HEAD `62da2bef…` = tag v2.11; `hackbench.c:37-40`; `hackbench.8:18-22`; banner "10 groups using 40 file descriptors each (== 400 tasks)"; `printf("Time: …")`; read 2026-09-24; R01:432 GPL-2.0-or-later per SPDX
- slice: 9.11
- dates: references.md:185-186 2026-10-07 (8a3e7489); read 2026-09-24; changed-after-read: yes (written from the read)
- verdict: TRACED

### D-F2-37 — LWN on hackbench
- source: `hackbench` (LWN 725238, untagged)
- repo: docs/workload/grounding-sources.md:29 — "LWN notes it is most often used for load-balancing changes"; source-vetting.md:87 (body) — "'a stalwart of kernel scheduler testing' (LWN survey, Articles/725238)"
- record: R01:440 — LWN 725238 "This benchmark is a stalwart of kernel scheduler testing … it is most often used by developers who are making changes to the scheduler's load-balancing code"; copy: lwn.net/Articles/725238 html sha256 6fb8023d…, read 2026-09-13
- slice: other (2026-09-13 verification)
- dates: grounding-sources.md:29 2026-10-17; read 2026-09-13; changed-after-read: yes
- verdict: TRACED

### D-F2-38 — stress-ng pin, licence, `--workload`, `--cyclic`, README disclaimer
- source: `stress-ng` (docs/references.md:189, deployed-system)
- repo: docs/references.md:190-191 — "commit `3ac9d7a8` (2026-09-23; newest tag V0.22.01), GPL-2.0-or-later … `--workload` stressor 'emulates bursty scheduled compute' — work items of 1 ms quanta at random times in a 100 ms slice, 30 % load by default … `--cyclic` stressor reports wake-latency percentiles p25 to p99.99 … 'it has never been intended to be used as a precise benchmark test suite, so do NOT use it in this manner'"; also grounding-sources.md:31; source-vetting.md:167, :182
- record: 911S2:759-766 — sparse clone at `3ac9d7a8…` (2026-09-23); `stress-ng.1:11793-11809`, `stress-workload.c:536-539`, `stress-ng.1:2744-2752`, `stress-cyclic.c:928-938`, `README.md:32-35`; read 2026-09-24; licence: R01:508 header "GPL version 2 or later" (at `3e6ae045`, 2026-09-13)
- slice: 9.11
- dates: references.md:190 2026-10-08 (232ae0ed), :191 2026-10-07; grounding-sources.md:31 2026-10-17; read 2026-09-24; changed-after-read: yes
- verdict: TRACED

### D-F2-39 — Ananicy and ananicy-cpp: status, licences, versions, self-description, fields, lineage
- source: `ananicy` (docs/references.md:200, deployed-system)
- repo: docs/references.md:201-203 — archived, last commit `1e2cc9a6` 2023-03-21; ananicy-cpp GPL-3.0, `v1.2.0` (`cf5ac2eb`, 2026-03-26), README at `3554447c`; self-description quote; `name` the only required field "used for match processes by exec bin name"; upstream's lowercase types with the capitalized ones under "Depricated types"; source-vetting.md:158 — "upstream Ananicy is GPL-3.0 and archived (its last commit 2023-03-21)"; :182 — "ananicy-cpp at `v1.2.0`"; source-vetting.md:47 (body, left standing for the field list and the gcc example)
- record: 912S2:387-389 (S2-30, clone `1e2cc9a6`, read 2026-10-07) README:22 self-description, :68 the gcc example, :71-79 "`name` used for match processes by exec bin name"; 912S2:393 (S2-31, `3554447c`); R06:8 "license GPL-3.0"; :849 upstream `LICENSE:1-2` "Version 3"; R06 C-ananicy-2 (:714-818) "### Depricated types ###"; R06:819-… ananicy-cpp v1.2.0 tagged 2026-03-26
- slice: other (9.12; 2026-09-13 verification)
- dates: references.md:201-202 2026-10-16 (69c16f54); :203 2026-09-12; source-vetting.md:158 2026-10-17; read 2026-09-13 / 2026-10-07; changed-after-read: yes
- verdict: TRACED

### D-F2-40 — ananicy-cpp's rule lookup key
- source: `ananicy`
- repo: docs/references.md:202 — "ananicy-cpp looks a rule up by the basename of the process's first `/proc/<pid>/cmdline` argument (`argv[0]`), untruncated — failing that the `/proc/<pid>/exe` link's basename, then `/proc/<pid>/comm` — and sets a matched rule's nice value on every thread"
- record: 912A:229-237 (A3-07, 2026-10-09) — at `v1.2.0`: `process.cpp:193` `get_command_from_pid`, `:197` "// Cmdline method", `:201` `cmdline[0].find_last_of('/')`, `:217` "// Exe method", `:250` "// Comm method"; `rules.cpp:184`
- slice: other (9.12)
- dates: references.md:202 2026-10-16 (69c16f54); read 2026-10-09; changed-after-read: yes (9.15 K01 restated the line)
- verdict: TRACED

### D-F2-41 — CachyOS installs and enables ananicy-cpp with the catalogue
- source: `cachyos-settings` (docs/references.md:206, deployed-system)
- repo: docs/references.md:207-208 — both install paths put `cachyos-settings` on the system (`pacstrap.conf:23`; live image list); depends on `ananicy-cpp` and `cachyos-ananicy-rules`; install hook runs `systemctl enable`; ISO 2026-08-09: ananicy-cpp 1.2.0, cachyos-ananicy-rules 1.1.47, 15 794 entries, unit linked; dataset/README.md:114 — "CachyOS's ananicy-cpp rules"; building-plan.md:121 — "ananicy-cpp's rules as CachyOS ships them"; coreset-guide.md:790
- record: 912S2:481-499 (S2-45, read 2026-10-08) — calamares `5f098957…`, PKGBUILDS `03924f78…` with SHA-256; 912S2:500-… (S2-46) ISO sha256 `959f6577…`, observed live root
- slice: other (9.12)
- dates: references.md:207 2026-10-16; README.md:114 2026-10-16 (18127cc9); read 2026-10-08; changed-after-read: yes
- verdict: TRACED

### D-F2-42 — The CachyOS catalogue at `03ef03fb`: counts, types, values, maintainers
- source: `ananicy-rules` (docs/references.md:211, deployed-system)
- repo: docs/references.md:212-215 — commit `03ef03fb…` (2026-09-08), tag `1.1.49`; "361 `.rules` files; 15 813 rule entries; 13 528 … `Game`" and the other type counts; `00-types.types` values; fifteen types defined, thirteen used, `TODO`, one invalid line; "maintained 'by the CachyOS team and the community'"; source-vetting.md:158 — "it holds 15,811 distinct names, not hundreds"
- record: R06:338-450 (C-ananicy-rules-9, -10) counts per type and file; :334 "15813 strictly-parsed entries, 15811 distinct names"; R06:25-112 (-1, -2) type values; 912S2:401 (S2-32) README:3 "maintained by the CachyOS team and the community"; 912S3:488-499 (S3-19) tag `1.1.49` resolves to `03ef03fb`; copies read 2026-09-13 / 2026-10-07 / 2026-10-08
- slice: other (2026-09-13 verification; 9.12)
- dates: references.md:212-213 2026-10-16; read 2026-09-13 / 2026-10-08; changed-after-read: yes
- verdict: TRACED

### D-F2-43 — What the catalogue holds for audio, indexers and compilers; no wanted/unwanted distinction
- source: `ananicy-rules`
- repo: docs/workload/source-vetting.md:158 — "`Player-Audio` is nice −4, nice −11 having existed only in 2022–2025 commits, on audio-server rules; only KDE's Baloo and Recoll are typed `BG_CPUIO` (nice 16, ioclass idle, sched idle), GNOME's Tracker and `updatedb` having no entry; 'compilers batch/idle' is ananicy-cpp's README example `gcc` rule, the catalogue holding no compiler entries … No type, comment or README text draws a wanted/unwanted-background distinction"; grounding-sources.md:18 — "a per-name priority catalogue (`ananicy-rules`). None of them draws a wanted/unwanted-background distinction"
- record: R06:37 `{ "type": "Player-Audio", "nice": -4 }`; K3:210-211 ([K3 check]) `git log -S'"nice": -11'` → `6474a905` (2022-10-01) added the audio-server rules with nice −11, `2223eefd` (2025-02-03) replaced them; R06:212 "Baloo (3 process names) and Recoll's indexer are BG_CPUIO … tracker … and updatedb … have no entries"; :266 "compiler assignments NOT FOUND at the pinned commit"; 912S2:393 ananicy-cpp README:176-183 the `gcc` example with `"sched": "batch", "ioclass": "idle"`; R06:169 "No type, comment, README text or issue template states a distinction between user-wanted and unwanted background work"
- slice: other (2026-09-13 verification; 9.12)
- dates: source-vetting.md:158 2026-10-17; grounding-sources.md:18 2026-10-17; read 2026-09-13; changed-after-read: yes
- verdict: TRACED

### D-F2-44 — How much of the core set the shipped catalogue keys
- source: `ananicy-rules` (with `ananicy`'s lookup key)
- repo: dataset/README.md:114 — "the shipped catalogue (`shipped_catalogue`, CachyOS's ananicy-cpp rules) matches none of its rules to several names the files bind — `kdenlive`, `make`, `python`, `HandBrakeCLI`, `deja-dup` among them (9.12 D109)"; docs/workload/building-plan.md:121 — "which on ananicy-cpp's key keys every bound name of a file in only 7 of the 50 core files it was counted on (9.12 D109)"
- record: 912A:240-246 (A3-09, 2026-10-09) — `python3 -I SCR/G-argv0/perfile.py dataset/build/coreset-single` → "strict 19 … files whole … strict 7"; 912CL:1625-1640 (D109) "Not keyed: … `python`; `systemd`; `make`; `kdenlive`; `kdenlive_render`; `HandBrakeCLI`; `deja-dup`"; catalogue copy `03ef03fb`
- slice: other (9.12)
- dates: README.md:114 2026-10-16; building-plan.md:121 2026-10-16; read 2026-10-09; changed-after-read: yes
- verdict: TRACED (a count over the 2026-10-09 build; whether it still holds on the final build is the compiled-number audit's)

### D-F2-45 — DARPA OpTC: what its release documents
- source: `darpa-optc` (docs/references.md:545, deployed-system)
- repo: docs/workload/grounding-sources.md:60 — "Process-create events with image paths, from Windows 10 enterprise endpoints, not personal desktops"; also references.md:547; source-vetting.md:187
- record: R11P:167 `README.md:12` "Each Windows 10 endpoint is equipped with an endpoint sensor that monitors host events"; :172 `ecar.md:33` "an 'image_path' entry in Event.properties will also typically be present"; :200 "hosts in an instrumented enterprise exercise with red-team activity"; copy: FiveDirections/OpTC-data `5b108604…`, read 2026-09-13
- slice: other (2026-09-13 verification; 9.10 D35)
- dates: grounding-sources.md:60 2026-10-17 (6f508a59); read 2026-09-13; changed-after-read: yes
- verdict: TRACED

### D-F2-46 — Carat: several running apps per sample
- source: `carat-top1000` (docs/references.md:550, deployed-system)
- repo: docs/workload/grounding-sources.md:69 — "Carat, whose samples list several running apps (`carat-top1000`), is noted and not used"; also references.md:552
- record: R11P:290 "processName (App Android package name)"; :293 "every time the battery level changed by 1%"; :295 reading "each sample … lists several running apps, each with an Android importance label"; copy: the data-sharing page sha256 a3f3e5fe…, read 2026-09-13
- slice: other (2026-09-13 verification; 9.10 D35)
- dates: grounding-sources.md:69 2026-10-17; read 2026-09-13; changed-after-read: yes
- verdict: TRACED

### D-F2-47 — The 136M Keystrokes check's role and the typing entries' stimulus labels
- source: `dhakal-chi18`, `swell-icmi14`; labels
- repo: dataset/archetypes.yaml:111 (and :184, :355, :494) — "Stimulus: SWELL-KW stream swell-word-c1, its keystrokes replayed … and its clicks, scrolls and drags left out … (D28 …)"; "Stimulus sensitivity (pre-registered, method §3): under a 136M Keystrokes transcription stream (dhakal-chi18) …"; :111 "a generated document of about 76 pages (… design — no source states a length, S7)"; docs/workload/measurement-overview.md:65 — "a segment or file boundary counted as one 2,000 ms gap"
- record: 95CL:93 (D18), 95CL:21 (D4); the gap rule is the campaign's own (`dataset/stimulus/streams.json`, written by `dataset/tools/stimulus/build_streams.py`)
- slice: 9.5
- dates: archetypes.yaml:111 2026-10-05; read n/a (no source states these values); changed-after-read: n/a
- verdict: LABELLED (the document length carries "design — no source states a length"; the left-out pointer events and the 2,000 ms boundary gap are stated as the method's rule, not a source's; the sensitivity ratios are `meas-ci`, the measurement audit's)

---

## Pointer notes (not findings under decision 1; for the lead)

- docs/references.md:39 — "(D6's alternative not taken: …)": the alternative not taken is 9.5 D4's (95CL:21); 9.5 D6 is the platform rule (95CL:29). Fix: "9.5 D4's alternative not taken".
- dataset/timelines/coreset/c6-dual.timeline.yaml:33 — "(gonzalez-chi04; 9.10 C-gonzalez-1)": C-gonzalez-1 is the 2026-09-13 verification's claim id (R10:70), which 9.10 D35 cites; 9.17 D1 wrote the same form. Fix: "the 2026-09-13 verification's C-gonzalez-1, as 9.10 D35 reads it".
- docs/references.md:38 — the licence words in quotation marks ("free to use for non-commercial use in your own research …") merge the page's "free to use for research and non-commercial use" with readme.txt:21's "You are free to use this data for non-commercial use in your own research or projects with attribution to the authors" (95S3:77). Fix: quote readme.txt:21 exactly.
- docs/references.md:59 — "fluent spread 0.29" is Table 3's σ²e (fluent typing), a log-scale variance (R08:248); "spread" is loose. Optional: "fluent-component variance σ²e 0.29".
- docs/references.md:64 — `killourhy-dsn09`'s "raw per-keystroke latency dataset": the CSV is a per-repetition feature table of hold, down-down and up-down latencies, no raw timestamps (95S3:142). No dataset doc cites the entry.

## Outside F2 (noted, not traced)

- docs/workload/grounding-sources.md:59 — "Enterprise / VDI / cloud workload traces (Azure, Google cluster traces, VDI characterization studies) | Server/VM granularity; no consumer applications; process identity absent or hashed": untagged claims about named traces; no record found in the 9.10 D35 restatement (which covers OpTC, BEHACOM, Carat only).
- docs/workload/source-vetting.md:64 (LAVD body), :70 (kernel build; SchedCP's `make -j172`) and grounding-sources.md:32 (SchedCP's "make -j 172" … "1.79× over EEVDF") belong to the gaming, compile and SchedCP groups.


# Part F3 — compile, background and IO sources (9.16 dataset claim audit)

Scope read: `dataset/archetypes.yaml` (compile, file, download, system-job entries), `dataset/sources.yaml`, `dataset/grids.yaml`, `dataset/variants.yaml`, `dataset/timelines/coreset/*` (compile, backup, indexing, transcode files and `c7.variant.yaml`, `c2-pairs.variant.yaml`), `dataset/README.md`, `docs/workload/*.md`, and the `docs/references.md` entries of the F3 ids. Record paths are relative to `_dev/research/jioh/`.

Ids in the F3 list that no in-scope file cites (only their own `docs/references.md` entry exists, so they carry no dataset claim): `borg`, `restic`, `baloo`, `plocate-ubuntu`, `plocate-debian`, `findutils-debian`, `locate-ubuntu`, `clamav`, `sysstat-debian`, `debian-sid-indexes`, `debian-code-search`, `dci-dcss` (its content enters D-F3-38 through 9.10 D92), `cargo-book`. `dkms-man` and `dkms-debian` no longer exist (removed by 9.10 D34).

"changed-after-read" = the claim's current wording was committed by a later task than the slice that read the source (git `log -S` on the claim's key phrase), not the slice's own fold-in a few days after the read.

### D-F3-01 — the build workload behind O'Callahan et al.'s process count
- source: `ocallahan-atc17` (docs/references.md:82, scholarly)
- repo: dataset/sources.yaml:85-87 — "\"make forks and execs 2430 processes, mostly short-lived\" (sec-4.3; written \"2430\" in the paper). The workload is a `make -j8` build of DynamoRio 6.1.0 (sec-4.1), not a Linux kernel build."; also dataset/archetypes.yaml:1035-1036; docs/references.md:84; docs/workload/grounding-sources.md:32; docs/workload/building-plan.md:101; docs/workload/source-vetting.md:168 (the correction of :70's "kernel build forks/execs 2,430", an append-only record corrected in place)
- record: 2026-09-13-verification/reads/R03-build-papers.md:42 — "make builds DynamoRio [8] (version 6.1.0) with make -j8"; :50 — "make forks and execs 2430 processes, mostly short-lived. (The next most prolific workload is sambatest with 89.)"; copy: usenix.org atc17-o_callahan.pdf, SHA-256 589ec379…, read 2026-09-13 (:9). Also task-9.6-compile/search/S1-literature.md:83 (read 2026-09-16)
- slice: other (2026-09-13 verification) and 9.6
- dates: line last changed 2026-10-17 (archetypes, 7b024003), 2026-10-16 (references, 69c16f54); read 2026-09-13; changed-after-read: yes (9.15 reworded the kernel-build attribution to DynamoRio in archetypes, references, grounding-sources, building-plan)
- verdict: TRACED

### D-F3-02 — what the O'Callahan count grounds: "compiler children"
- source: `ocallahan-atc17` (docs/references.md:82, scholarly)
- repo: dataset/sources.yaml:87-88 — "Grounds only the existence and short-lived character of compiler children"; also docs/references.md:84 — "Grounds only the existence and short-lived character of compiler children (`compiler-child`'s modeling notes …)"; docs/workload/building-plan.md:101 — "`ocallahan-atc17` only for the existence and short-lived character of compiler children"; dataset/archetypes.yaml:1034 — "The literature grounds the class's existence and short-lived character only" (the class = `compiler-child`)
- record: R03-build-papers.md:50 (passage above) and :62 — "Unit of the count: processes forked and exec'd by the whole *make*"; task-9.6-compile/changelog.md:13 (D2) — "`category_source` corrects to what S1-01 and S1-02 say: a parallel make build spawns many short-lived processes; the kernel-build attribution and \"compiler children\" leave"; references.md:84 itself: "The paper does not say what the 2430 processes run"
- slice: other (2026-09-13 verification) and 9.6
- dates: line last changed 2026-10-16 (sources.yaml 3e6c6351; references 69c16f54; building-plan 34b09357), archetypes 2026-10-17 (7b024003); read 2026-09-13 / 2026-09-16; changed-after-read: yes
- verdict: WORDING-OUTSIDE-PASSAGE
- finding: the repo says the paper grounds "compiler children"; the passage counts every process a DynamoRio `make -j8` forks and execs, says nothing of what they run, and 9.6 D2 removed "compiler children" for that reason. Fix: "grounds only that a parallel `make` build forks and execs many processes, mostly short-lived (a DynamoRio build; the paper does not say what they run)" in sources.yaml:87-88, references.md:84, building-plan.md:101; archetypes.yaml:1034 "the class's existence" → "that a parallel make build spawns many short-lived processes".

### D-F3-03 — Coetzee et al. on the Linux kernel build's short-lived processes
- source: `coetzee-arxiv12` (docs/references.md:87, scholarly preprint)
- repo: dataset/sources.yaml:95-97 — "\"the Linux kernel build's enormous number of short-lived processes\" (sec-9). The characterization is specific to the Linux kernel build"; also dataset/archetypes.yaml:1036-1037 — "names the Linux kernel build's many short-lived processes, its examples `cp` and `mkdir`, with no count (sec-9)"; docs/references.md:89 (first two sentences); docs/workload/source-vetting.md:70
- record: R03-build-papers.md:104 — "…due to the Linux kernel build's enormous number of short-lived processes like cp and mkdir."; :120 — "It gives no count"; copy arxiv 1203.2704v1, SHA-256 637cbce6…, read 2026-09-13 (:14). Also task-9.6-compile/search/S1-literature.md:117 (read 2026-09-16)
- slice: other (2026-09-13 verification) and 9.6
- dates: sources.yaml 2026-08-26; archetypes 2026-10-17 (7b024003); read 2026-09-13; changed-after-read: yes (archetypes and references wording added by 9.15)
- verdict: TRACED

### D-F3-04 — the reach of Coetzee's corroboration
- source: `coetzee-arxiv12` (docs/references.md:87)
- repo: docs/references.md:89 — "so beside `ocallahan-atc17` it corroborates only that builds spawn many short-lived processes"
- record: R03-build-papers.md:104 (the passage names "the Linux kernel build's" processes); :120 — "It is specific to that build in that it names \"the Linux kernel build's\" processes"
- slice: other (2026-09-13 verification)
- dates: line last changed 2026-10-16 (69c16f54); read 2026-09-13; changed-after-read: yes
- verdict: WORDING-OUTSIDE-PASSAGE
- finding: "builds" widens the passage's scope; the same entry says to cite it for the Linux kernel build only. Fix: "corroborates only that the Linux kernel build spawns many short-lived processes".

### D-F3-05 — SchedCP's kernel-compilation workload and its "short-lived processes"
- source: `schedcp-mlsys25` (related-work id; untagged compile claim in a dataset doc)
- repo: docs/workload/grounding-sources.md:32 — "(kernel compilation, \"make -j 172\" on 6.14 tinyconfig, 1.79× over EEVDF) … SchedCP's \"short-lived processes\" is its Observation Agent's generated profile text"
- record: R03-build-papers.md:149 — "For kernel compilation (tinyconfig, \"make -j 172\" on 6.14 source) … reaching 1.79× total improvement over EEVDF"; :159; copy arxiv 2509.01245v4, SHA-256 cce49d3c…, read 2026-09-13; task-9.6-compile/search/S1-literature.md:140 — "The Observation Agent begins by analyzing the Linux kernel source tree … This observation produces a Workload Profile: “CPU-intensive parallel compilation task with short-lived processes…”" (v1, read 2026-09-16)
- slice: other (2026-09-13 verification) and 9.6
- dates: line last changed 2026-10-17 (c59b6a89); read 2026-09-13/16; changed-after-read: yes (9.15 K06 restated the row)
- verdict: TRACED

### D-F3-06 — the source-vetting correction of the kernel-build row (sambatest, kernel docs, autogroup)
- source: `ocallahan-atc17`, Linux kernel v6.6 (untagged)
- repo: docs/workload/source-vetting.md:168 — "89 is the next most prolific workload's (sambatest). `sched_child_runs_first` is in no kernel Documentation file; SCHED_AUTOGROUP's Kconfig help says \"build jobs\", not \"make -j\". \"Short-lived cc1/ld/as + few long-lived make/linker\" is in no cited source."
- record: R03-build-papers.md:50 (sambatest 89); task-9.6-compile/search/S2-project-docs.md:1202 — "of workloads isolates aggressive CPU burners (like build jobs) from"; :1246-1251 (`sysctl_sched_child_runs_first` in source); search log row 18 (`Documentation/…` read); copy torvalds/linux v6.6, read 2026-09-16
- slice: other and 9.6
- dates: line last changed 2026-10-17 (c59b6a89); read 2026-09-13/16; changed-after-read: yes
- verdict: TRACED

### D-F3-07 — the build tools' documented default parallelism
- source: GNU make 4.4.1, dkms (untagged; 9.6 D4's reads)
- repo: docs/workload/measurement-overview.md:52 — "The kernel build and the DKMS rebuild run `-j8`: the build tools' documented defaults follow `nproc`, here for an eight-thread desktop."
- record: task-9.6-compile/search/S2-project-docs.md:407 — "@code{make} will execute only one recipe at a time, waiting for it to finish" (make 4.4.1 manual, commit d66a65ad, read 2026-09-16); task-9.6-compile/changelog.md:21 (D4) — "every vendor default found is `nproc` or a memory-capped variant (make 1, S2-03; ninja processors + 2 …; dkms `-j$(nproc)` …)"; task-9.10-scenarios-timelines/search/S2-project-docs.md:3717 (S2-39, NVIDIA's `dkms.conf` `PROCS_NUM=`nproc``)
- slice: 9.6, 9.10
- dates: line last changed 2026-10-17 (c59b6a89), the phrase written 2026-10-01 (1abb56ba, the measurement overview); read 2026-09-16; changed-after-read: yes
- verdict: WORDING-OUTSIDE-PASSAGE
- finding: the kernel build's tool is GNU make, whose documented default is one job; only DKMS's NVIDIA build (and ninja, cargo, dpkg, Gentoo) follow `nproc`. Fix: "run `-j8`, the `nproc` rule applied to an eight-thread desktop (9.6 D4; DKMS's NVIDIA build reads `nproc`, GNU make defaults to one job)".

### D-F3-08 — `parallelism_cap` 8 (the make build's job cap)
- source: none (labelled value)
- repo: dataset/timelines/coreset/c1-compile.timeline.yaml:22 — "parallelism_cap: design"; also c4-compile.timeline.yaml:40, c7-compile.timeline.yaml:43; docs/workload/building-plan.md:101 — "`parallelism_cap` binds 8, design (9.6 D4's `nproc` rule on an eight-thread desktop)"; dataset/archetypes.yaml:1076-1077 (no label word); dataset/archetypes.yaml:1134 "(D4's eight-thread desktop, design; D50)"
- record: task-9.6-compile/changelog.md:21 (D4) — "Label: convention, grounds cited for the choice, overridable at binding time"
- slice: 9.6
- dates: label "design" written 2026-10-11 (b5678087, 9.18) and 2026-10-16 (34b09357); D4 2026-09-17; changed-after-read: yes
- verdict: LABELLED
- finding: label present but differs from the slice's decision — 9.6 D4 labels the 8 "convention" (vendor defaults cited); the timelines and building-plan say "design". Fix: one label, "convention" per D4, in the three timelines' `source:` maps, building-plan.md:101 and archetypes.yaml:1134 — or a recorded re-decision to "design".

### D-F3-09 — make's jobserver counts jobs, not processes
- source: GNU make 4.4.1 (untagged)
- repo: dataset/archetypes.yaml:1075 — "`parallelism_cap` counts jobs, as make's jobserver counts them"
- record: task-9.6-compile/search/S2-project-docs.md:618 — "\"there are only N jobs running at the same time between them all\", recursive makes not counted; each job may be a shell plus its children"; copy commit d66a65ad, read 2026-09-16
- slice: 9.6
- dates: 2026-09-20 (9.6 fold-in 2df5653b); read 2026-09-16; changed-after-read: no
- verdict: TRACED

### D-F3-10 — Gregg's perf sched capture as corroboration of role weights
- source: Brendan Gregg, "perf Examples" (untagged)
- repo: dataset/archetypes.yaml:1037-1038 — "Gregg's one-second perf sched capture of a build corroborates that the same roles carry the same relative weight on Linux, no number transcribed (D2)"
- record: task-9.6-compile/search/S3-traces-datasets.md:51-57 (S3-01; brendangregg.com/perf.html, SHA-256 a60d1276…, read 2026-09-16); task-9.6-compile/changelog.md:13 — "`cc1` 6 013 ms against `gcc` 44, `as` 122, `sh` 107, `fixdep` 81, `make` 54 ms in one second"
- slice: 9.6
- dates: phrase 2026-09-20 (2df5653b); read 2026-09-16; changed-after-read: no
- verdict: TRACED

### D-F3-11 — the kernel's Makefile passes no `-pipe`, so `cc1` and `as` run in sequence
- source: Linux v6.6 kbuild, GCC 13 (untagged)
- repo: dataset/archetypes.yaml:1017-1018 — "no `-pipe` in the kernel's Makefile so `cc1` and `as` run in sequence"
- record: task-9.6-compile/changelog.md:51 states it among what the run exhibits ("no `-pipe` in the kernel's Makefile, so `cc1` and `as` run in sequence"); task-9.6-compile/search/S2-project-docs.md:311-313, :356 (GCC: `cc1` then `as`, piped only with `-pipe`). No passage of the kernel's Makefile flags is recorded (S2-01, :55-293, holds no `-pipe` line)
- slice: 9.6
- dates: 2026-09-20 (2df5653b); read 2026-09-16; changed-after-read: no
- verdict: RECORD-BELOW-STANDARD
- finding: the sequence is observed in the run and GCC's rule is quoted, but the claim about the kernel's Makefile has no recorded passage or search. Fix: add to 9.6 S2-01 a grep of linux-6.6's `Makefile` and `arch/x86/Makefile` for `-pipe` (none) with the tag; or reword to "`cc1` and `as` run in sequence in the run (GCC pipes them only under `-pipe`)".

### D-F3-12 — Liu and Layland's deadline at the next request
- source: `liu-jacm73` (docs/references.md:877, scholarly)
- repo: docs/workload/measurement-overview.md:178 — "`liu-jacm73` | the periodic jobs' deadline at the next period's start"
- record: task-9.12-related-work-prose/search/S1-literature.md:237 — "(A2) Deadlines consist of run-ability constraints only--i.e, each task must be completed before the next request for it occurs." (printed p. 48; cs.ru.nl liu-layland.pdf, SHA-256 de9fb725…, read 2026-10-07, :236)
- slice: other (9.12)
- dates: 2026-10-01 (1abb56ba); read 2026-10-07 (first verified 2026-09-09); changed-after-read: no
- verdict: TRACED

### D-F3-13 — Meyer and Bolosky's 30 MB half of bytes
- source: `meyer-fast11` (docs/references.md:157, scholarly)
- repo: docs/workload/measurement-overview.md:188 — "`meyer-fast11` (half of the bytes in files over 30 MB, Windows, 2009)"; also dataset/archetypes.yaml:1357 — "share of bytes in files over 30 MB 0.606 against the 2009 Windows population's half"; docs/references.md:159
- record: task-9.7-background-io/search/T9-S1-literature.md:234 — "half of all bytes are in files larger than 30MB (this figure was 2MB in 2000)"; :263 (population: 597 computers, Windows 7/Vista/Server, 18 Sep–16 Oct 2009); copy usenix.org Meyer.pdf, read 2026-09-19; task-9.7-background-io/changelog.md:37-39 (D7, corrected by D40)
- slice: 9.7
- dates: 2026-10-01 (measurement overview), 2026-10-04 (archetypes c9f5f724, 9.10); read 2026-09-19; changed-after-read: yes (written by 9.10 and the overview from 9.7's record)
- verdict: TRACED

### D-F3-14 — the GNU/Linux users' median file size, 4.60 KB
- source: `fm-results-tables` (docs/references.md:535, deployed-system data)
- repo: docs/workload/measurement-overview.md:188 — "`fm-results-tables` (GNU/Linux users' median file size)"; dataset/archetypes.yaml:1357 — "median file 2 891 B against the GNU/Linux users' 4.60 KB (4,707 B)"; docs/references.md:537
- record: task-9.7-background-io/search/T9-S3-datasets.md:298 — "\"linux,4.596679688,2236.45735,…\"", header "Median file size (in KB)"; :274 (commit 1a5a2436, read 2026-09-19)
- slice: 9.7
- dates: 2026-10-01 / 2026-10-04 (c9f5f724); read 2026-09-19; changed-after-read: yes
- verdict: TRACED

### D-F3-15 — Cumulus's personal-machine daily change rates, seven days
- source: `vrable-fast09` (docs/references.md:162, scholarly)
- repo: docs/workload/measurement-overview.md:52 — "the incremental after seven days of Cumulus's personal-machine change rates (`vrable-fast09`)"; dataset/archetypes.yaml:1682-1683 — "after seven days of Cumulus's personal-machine change rates — 9,729 changed files of 883.1 MB and 304.2 MB of new files, the changed part an upper bound (D115)"; docs/workload/measurement-overview.md:189; docs/references.md:164
- record: task-9.7-background-io/search/T9-S1-literature.md:563 — "Update Rates New data/day 9.50 GB 10.3 MB · Changed data/day 805 MB 29.9 MB"; :574 (one personal computer, 223 days); copy usenix.org vrable.pdf, read 2026-09-19 (:555); task-9.10-scenarios-timelines/changelog.md:2088-2098 (D115, the seven-day arithmetic, labelled upper bound)
- slice: 9.7, 9.10
- dates: archetypes 2026-10-04 (9.10 fold-in); overview 2026-10-17 (c59b6a89); read 2026-09-19; changed-after-read: yes (overview)
- verdict: TRACED

### D-F3-16 — how Déjà Dup's monitor starts the scheduled backup
- source: `deja-dup` (docs/references.md:469, deployed-system)
- repo: dataset/archetypes.yaml:1680-1681 — "started by its own monitor through `chrt --idle 0 ionice -c3`"; also :1708; docs/workload/coreset-guide.md:220 — "monitor가 `chrt --idle 0 ionice -c3`로 시작"; docs/references.md:471
- record: task-9.10-scenarios-timelines/search/S2-project-docs.md:3940 (S2-62) — "`CommonUtils.vala:107–131`, `nice_prefix`: `cmd = \"ionice -c3 \" + cmd; // idle class` … `cmd = \"chrt --idle 0 \" + cmd;`"; `monitor.vala:119` `var delay_time = 120;`; copy tag 45.2, commit 585b723d, read 2026-10-04
- slice: 9.10
- dates: archetypes 2026-10-04 (c9f5f724, fold-in); coreset-guide 2026-10-16 (4b966f84, 9.15 K03); read 2026-10-04; changed-after-read: yes (coreset-guide)
- verdict: TRACED

### D-F3-17 — what every Déjà Dup backup runs
- source: `deja-dup`, `duplicity`
- repo: dataset/archetypes.yaml:1685-1687 — "duplicity's collection-status, its dry-run sizing pass, which every backup runs (D119), the incremental with one gpg per volume, and the verify's restore"; docs/references.md:471, :476
- record: S2-project-docs.md:3940 (S2-62) — "`ToolJob.vala:43–46` declares `public enum Flags { NO_PROGRESS, NO_CACHE, }`, a plain enum, so `NO_PROGRESS` is 0 … every backup runs the `--dry-run` pass"; `OperationBackup.vala:54` verify chained; S2-project-docs.md:3954 (S2-63) — "`gpg.py:134–160`: a `GnuPG()` per file … `--symmetric`, `--force-mdc`"; read 2026-10-04
- slice: 9.10
- dates: 2026-10-04 (fold-in); changed-after-read: no
- verdict: TRACED

### D-F3-18 — Déjà Dup's defaults (weekly once turned on, encryption on, 200 MB volumes, password not remembered)
- source: `deja-dup`
- repo: dataset/archetypes.yaml:1679-1680 — "at Déjà Dup's defaults with its password remembered (D117) — encrypted by gpg, 200 MB volumes — making its scheduled weekly incremental"; docs/workload/building-plan.md:85 — "Déjà Dup's scheduled weekly incremental"; docs/workload/scenario-catalog.md:26 — "a periodic backup every 7 days once turned on"
- record: S2-62 (S2-project-docs.md:3940) — "`periodic-period` `7` (`:53–54`)", "`AssistantOperation.vala:345`: `encrypt_enabled.active = true; // always default to encrypted`", "volumes of `200` MB", "Remember password … `active` is `false`"; read 2026-10-04
- slice: 9.10
- dates: archetypes 2026-10-04; scenario-catalog 2026-10-16 (34b09357); building-plan 2026-10-16; changed-after-read: yes (catalog, plan)
- verdict: TRACED

### D-F3-19 — Déjà Dup is in Ubuntu 24.04's extended install, not the default
- source: `deja-dup`, `ubuntu-desktop-manifest`
- repo: docs/workload/scenario-catalog.md:26 — "Déjà Dup in Ubuntu 24.04's extended install"
- record: S2-project-docs.md:3962 (S2-64) — "the versions of the 24.04.5.1 image's extended layer (S2-01)"; task-9.10-scenarios-timelines/changelog.md D49 ("It has no DKMS…"); dataset/archetypes.yaml:1689 states `apt-get install deja-dup` added it to the default layer (measured state); read 2026-10-04
- slice: 9.10
- dates: 2026-10-16 (34b09357); changed-after-read: yes
- verdict: TRACED

### D-F3-20 — the two-monthly restore test
- source: `deja-dup`
- repo: dataset/archetypes.yaml:1713-1714 — "The two-monthly restore test, with a fresh cache and the password asked, about one weekly run in nine, is not depicted (9.10 D118)"
- record: S2-62 — "with a fresh cache and no saved password only at \"nag\" time, every 60 days (`CommonUtils.vala:341–373`, `span = TimeSpan.DAY * 30 * 2`)"; "one in nine" is arithmetic (60 / 7 ≈ 8.6)
- slice: 9.10
- dates: 2026-10-04; changed-after-read: no
- verdict: TRACED

### D-F3-21 — the CPU groups the indexer and the backup run in on the depicted desktop
- source: systemd 255.4, tracker-miners 3.7.1, deja-dup 45.2, gnome-session 46.0 (untagged; 9.11 D16)
- repo: dataset/archetypes.yaml:1592-1594 — "the miner's unit runs in `background.slice` … where the slice weights give it about 23 % of the CPU"; :1710-1712 — "the monitor's autostart scope under `app.slice` … an idle weight of 3 against 1 024"
- record: task-9.11-scheduler-constants/changelog.md:216-224 (D16) — "`app.slice` sets `CPUWeight=100`, `background.slice` 30"; "`src/miners/fs/tracker-miner-fs.service.in:14`, `Slice=background.slice`"; "the monitor is an XDG autostart entry … `gnome-session/gsm-autostart-app.c:953`"; source packages read 2026-10-08 from archive.ubuntu.com, each matching its `.dsc` SHA-256
- slice: other (9.11)
- dates: 2026-10-09 (1dc4af4d, 9.13); read 2026-10-08; changed-after-read: yes (written by 9.13 from 9.11's read)
- verdict: TRACED (23 % = 30 / 130, arithmetic stated in the record)

### D-F3-22 — how the stock unattended upgrade starts (apt's units)
- source: `apt` (docs/references.md:479, deployed-system)
- repo: dataset/archetypes.yaml:1495-1496 — "the stock Ubuntu 24.04 unattended upgrade's install stage, `apt.systemd.daily install` (apt-daily-upgrade.service's ExecStart)"; docs/references.md:481
- record: task-9.10-scenarios-timelines/search/S2-project-docs.md:326 — "ExecStart=/usr/lib/apt/apt.systemd.daily install"; :308-309 — "OnCalendar=*-*-* 6:00" / "RandomizedDelaySec=60m"; copy apt 2.8.3 .deb, SHA-256 c9ace99e…, read 2026-10-01 (S2-03, :267)
- slice: 9.10
- dates: 2026-10-01 (7942ecfe, fold-in); changed-after-read: no
- verdict: TRACED

### D-F3-23 — unattended-upgrades is in the default install and enabled by default
- source: `unattended-upgrades`, `ubuntu-desktop-manifest`
- repo: docs/workload/scenario-catalog.md:28 — "The stock unattended upgrade, in Ubuntu 24.04's default install and enabled by default"; also dataset/README.md:120; dataset/timelines/coreset/c7.variant.yaml:10-11; docs/references.md:486
- record: S2-project-docs.md:346-348 — "Template: unattended-upgrades/enable_auto_updates" … "Default: true"; task-9.10-scenarios-timelines/changelog.md:41 (D3) — "`unattended-upgrades` is in the default layer of the stock Ubuntu 24.04.5.1 desktop (S2-01)"; read 2026-10-01
- slice: 9.10
- dates: catalog 2026-10-16, README 2026-10-16 (18127cc9); changed-after-read: yes
- verdict: TRACED

### D-F3-24 — the update the upgrade installs (glibc, 2026-07-27, four binaries)
- source: `glibc` (docs/references.md:489)
- repo: dataset/archetypes.yaml:1496-1498 — "installing the security update Ubuntu published on 2026-07-27 — glibc 2.39-0ubuntu8.7 to 2.39-0ubuntu8.8, four binaries: `libc-bin`, `libc6`, `libc6-dbg`, `locales`"; docs/workload/measurement-overview.md:52; docs/workload/coreset-guide.md:217
- record: S2-project-docs.md:3627-3629 (S2-32) — "`libc6` and `libc-bin` 2.39-0ubuntu8.8 (amd64) and `locales` 2.39-0ubuntu8.8 (all), published 2026-07-27 (S3-58)"; task-9.10-scenarios-timelines/changelog.md:759 (D36) — "`glibc` 2.39-0ubuntu8.8, four binaries of the default layer (`libc-bin`, `libc6`, `libc6-dbg`, `locales`)"; search/S3-traces-datasets.md:807 (S3-58, Launchpad, read 2026-10-01)
- slice: 9.10
- dates: archetypes 2026-10-01; overview 2026-10-17; coreset-guide 2026-10-16; changed-after-read: yes (overview, guide)
- verdict: TRACED

### D-F3-25 — the pending-set day rule (median working day)
- source: Ubuntu's security pocket (S3-58; reader's own computation)
- repo: dataset/archetypes.yaml:1498 — "the latest day at the past year's median count of binaries a working run installs (D36)"
- record: task-9.10-scenarios-timelines/changelog.md:763-765 (D36) — "4 binaries, the count apt reports, is the median of the 125 non-kernel days … Of the year's eight days at 4 binaries, 2026-07-27 is the latest"; S3-traces-datasets.md:807 (S3-58, "reader's own")
- slice: 9.10
- dates: 2026-10-01; changed-after-read: no
- verdict: TRACED (a computation over archive records, labelled the reader's own in the record)

### D-F3-26 — what glibc's maintainer scripts run (18 English locales; chroot skips)
- source: `glibc`
- repo: dataset/archetypes.yaml:1501-1502 — "In a chroot no init runs: `libc6`'s postinst skips `systemctl daemon-reexec` and the reboot-required notice"; :1513, :1523-1524 — "`locale-gen`'s 18 `localedef` runs" / "18 for English (9.10 D37)"
- record: S2-project-docs.md:3627 (S2-32) — "`libc6` `postinst:151–170`: … `if ischroot 2>/dev/null; then` / \"# Don't bother trying to re-exec init from a chroot:\""; "`language-pack-en-base` … whole file, 18 entries"; read 2026-10-01
- slice: 9.10
- dates: 2026-10-01; changed-after-read: no
- verdict: TRACED

### D-F3-27 — the unit's wait-online step
- source: `apt` (apt-helper)
- repo: dataset/archetypes.yaml:1502-1504 — "the unit's `apt-helper wait-online` step is not carried — on an online desktop it is a `systemctl is-active` query per network manager and the active manager's waiter"
- record: S2-project-docs.md:3651 (S2-34) — "`apt-helper.cc:216–221`: … `{\"systemctl\", \"is-active\", \"-q\", service, nullptr};` … `if (ServiceIsActive(task[0]))`"; salsa tag 2.8.3, read 2026-10-01
- slice: 9.10
- dates: 2026-10-01; changed-after-read: no
- verdict: TRACED

### D-F3-28 — DKMS's kernel hooks and the build's `nproc`
- source: `dkms` (docs/references.md:494)
- repo: dataset/archetypes.yaml:1132-1135 — "every process under the two DKMS kernel hooks … The build runs at -j8 through `OMP_NUM_THREADS=8`, `nproc` being what NVIDIA's `dkms.conf` and dkms read"; docs/workload/scenario-catalog.md:22 — "DKMS's kernel hooks in Ubuntu's dkms package (`dkms`)"; docs/references.md:496
- record: S2-project-docs.md:1053 — "exec /usr/lib/dkms/dkms_autoinstaller start \"$inst_kern\"" (S2-03, read 2026-10-01); :3717 (S2-39) — "``PROCS_NUM=`nproc` `` / `[ $PROCS_NUM -gt 16 ] && PROCS_NUM=16`"; :3726 (S2-40) — "`nproc` without options returns `OMP_NUM_THREADS` when it is set"
- slice: 9.10
- dates: archetypes 2026-10-02 (18fec3f5); catalog 2026-10-16; changed-after-read: yes (catalog)
- verdict: TRACED

### D-F3-29 — the module: NVIDIA's 595 open module, production branch, five modules
- source: `nvidia-open-kernel-modules` (docs/references.md:499)
- repo: dataset/archetypes.yaml:1126-1127 — "DKMS's autoinstall of `nvidia-dkms-595-open` 595.91.07, the open kernel module of NVIDIA's production branch (D47)"; docs/workload/building-plan.md:93, :162; docs/workload/coreset-guide.md:238; docs/references.md:501
- record: S2-project-docs.md:3659 (S2-35) — "595 (production branch)", "`nvidia-driver-595` … \"Support: PB\""; :3717 (S2-39) — "`BUILT_MODULE_NAME[0..4]` `nvidia`, `nvidia-modeset`, `nvidia-drm`, `nvidia-uvm`, `nvidia-peermem`; `:14` `AUTOINSTALL=\"yes\"`"; read 2026-10-01/02
- slice: 9.10
- dates: archetypes 2026-10-02; building-plan 2026-10-16/17; coreset-guide 2026-10-16; changed-after-read: yes (docs)
- verdict: TRACED

### D-F3-30 — the kernels: 7.0.0-34 published to security 2026-09-23; HWE 7.0.0-31 added by the installer
- source: Ubuntu archive (S3-60, S2-33; untagged)
- repo: dataset/archetypes.yaml:1127-1130 — "for the security kernel `7.0.0-34-generic`, run by the stock Ubuntu 24.04 unattended upgrade's install stage of 2026-09-23 … with the HWE kernel the installer adds (`7.0.0-31`)"; docs/workload/building-plan.md:162; docs/workload/coreset-guide.md:238
- record: task-9.10-scenarios-timelines/changelog.md:932 (D48) — "`7.0.0-34` reached security on 2026-09-23T15:49:46, replacing `7.0.0-31`" (S3-60, S3-traces-datasets.md:826, read 2026-10-02); S2-project-docs.md:3648 (S2-33) — "`linux-generic-hwe-24.04`, `linux-image-7.0.0-31-generic` … reach an installed system through the installer"
- slice: 9.10
- dates: archetypes 2026-10-02; building-plan 2026-10-16; changed-after-read: yes (docs)
- verdict: TRACED

### D-F3-31 — module signing on a Secure Boot desktop
- source: DKMS / Ubuntu's Secure Boot route (untagged)
- repo: dataset/archetypes.yaml:1135-1136 — "No boot loader or `shim-signed` in the chroot, so no module is signed, where a Secure Boot desktop signs the five."; same at :1305-1306
- record: none found. Searched 9.10 changelog, search/*.md and campaign/dkms/*.md for "sign", "Secure Boot", "shim", "mok". The one passage, task-9.10-scenarios-timelines/search/S2-project-docs.md:3512 (S2-28, Ubuntu Server docs, read 2026-10-01): "the DKMS drivers are not signed with Canonical's key and thus do not support secure boot" — which does not state that DKMS signs the modules it builds.
- slice: 9.10
- dates: 2026-10-02 (18fec3f5); changed-after-read: no
- verdict: NO-RECORD
- finding: the repo states DKMS's signing behaviour on a Secure Boot desktop with no read passage; the nearest record reads the other way. Fix: read dkms 3.0.11's signing step (`/usr/sbin/dkms`'s `sign_file` with the MOK key that `shim-signed` creates) into a 9.10 record, or drop "where a Secure Boot desktop signs the five" at both lines.

### D-F3-32 — Tracker 3.7.1 in the default install
- source: `ubuntu-desktop-manifest`, `tracker-miners`
- repo: docs/workload/scenario-catalog.md:25 — "Tracker 3.7.1 in Ubuntu 24.04's default install (`ubuntu-desktop-manifest`) and its crawl rule (`tracker-miners`; 9.10 D5)"
- record: S2-project-docs.md:3734 (S2-41) — "`iso-casper-minimal.manifest:1379–1381`: `+tracker 3.7.1-1build1`, `+tracker-extract 3.7.1-1ubuntu0.1`, `+tracker-miner-fs 3.7.1-1ubuntu0.1`"; S2-04 (:1141; `crawling-interval` rule); read 2026-10-01/02
- slice: 9.10
- dates: 2026-10-16 (34b09357); changed-after-read: yes
- verdict: TRACED

### D-F3-33 — Tracker's shipped behaviour (initial sleep, extractor deadline and restart, reset, user unit)
- source: `tracker-miners` (docs/references.md:504)
- repo: dataset/archetypes.yaml:1562 — "Its settings as shipped, the 15 s initial sleep included"; :1577-1578 — "the extractor's stock 5 s per-file deadline ends two scanned books' extraction, and the miner restarts it after a 1 s grace each time"; :1586-1587 (`tracker3 reset --filesystem`); docs/references.md:506
- record: S2-project-docs.md:3734 (S2-41) — "`initial-sleep` `<default>15</default>`"; :3761 (S2-43) — "`tracker-reset.c:186–205` … `tracker_process_stop (SIGKILL);`"; task-9.10-scenarios-timelines/changelog.md:1287 (D72) — "`DEFAULT_DEADLINE_SECONDS 5` (`tracker-extract.c:46`) … The miner restarts the extractor after its 1 s grace (`tracker-miner-files.c:244–245`)", copy S2-04 commit eae431ef, read 2026-10-01 (the deadline passage sits in the changelog, not in the S2 entry)
- slice: 9.10
- dates: 2026-10-03 (99368c44, fold-in); changed-after-read: no
- verdict: TRACED

### D-F3-34 — Tracker's threads declare SCHED_IDLE at nice 19
- source: `tracker-miners`
- repo: dataset/archetypes.yaml:1588-1589 — "Every thread of the miner and the extractor declares itself background work, SCHED_IDLE at nice 19 (9.6 D17)"
- record: task-9.6-compile/changelog.md:95 (D17) — "every thread of the miner and the extractor exits with policy `SCHED_IDLE` at nice 19 in all four repeats … the miner's debug log, Tracker 3.7.1: \"Set scheduler policy to SCHED_IDLE\" … the source, S2-22, tracker-miners 3.7.3 `tracker-main.c:199–219`"; task-9.11-scheduler-constants/changelog.md:222 (D16, 3.7.1: `tracker-sched.c:46`, `tracker-main.c:219`)
- slice: 9.6, 9.11
- dates: phrase 2026-09-20 (6f0f28fc); changed-after-read: no
- verdict: TRACED

### D-F3-35 — HandBrake 1.7.2's default preset and its settings
- source: `handbrake` (docs/references.md:444)
- repo: dataset/archetypes.yaml:1625-1627 — "running its default preset unchanged, \"Fast 1080p30\" (x264 at fast, RF 22, profile main, level 4.0, AAC stereo at 160 kb/s, MP4)"; docs/workload/measurement-overview.md:52 — "to 1080p at its default preset (`handbrake`)"; docs/references.md:446
- record: task-9.10-scenarios-timelines/search/S2-project-docs.md:3879-3886 (S2-55, preset_builtin.json at tag 1.7.2, SHA-256 5fb29a61…, read 2026-10-03) quotes the H.265 presets' fields and says only "The 1080p presets in MP4 (\"Fast 1080p30\" and the rest) encode with `x264`"; the default mark and Fast 1080p30's fields are asserted in task-9.10-scenarios-timelines/changelog.md:1622 (D93, "the preset HandBrake 1.7.2 marks `Default` (S2-55)") and campaign/handbrake/method.md:22 without a verbatim passage. (This audit read the local copy `sources/S2-55/preset_builtin.json-1.7.2`: Fast 1080p30 has `"Default": true`, `VideoEncoder` "x264", `VideoPreset` "fast", `VideoQualitySlider` 22.0, `VideoProfile` "main", `VideoLevel` "4.0", AAC stereo 160, `FileFormat` "mp4" — the repo's wording holds.)
- slice: 9.10
- dates: archetypes 2026-10-03 (17789d68, fold-in); overview 2026-10-17; changed-after-read: yes (overview)
- verdict: RECORD-BELOW-STANDARD
- finding: the record carries no verbatim passage for the default mark or the preset's settings. Fix: add Fast 1080p30's stanza fields (`Default`, `VideoEncoder`, `VideoPreset`, `VideoQualitySlider`, `VideoProfile`, `VideoLevel`, `AudioList`, `FileFormat`) verbatim to S2-55.

### D-F3-36 — HandBrakeCLI as Ubuntu 24.04 packages it
- source: `handbrake`
- repo: dataset/archetypes.yaml:1625-1626 — "HandBrakeCLI 1.7.2 as Ubuntu 24.04 packages it (`handbrake-cli` 1.7.2+ds1-1build2, x264 0.164.3108, FFmpeg 6.1.1)"; docs/workload/scenario-catalog.md:19
- record: S2-project-docs.md:3887 (S2-56) — "`Package: handbrake-cli` / `Version: 1.7.2+ds1-1build2` / `Depends: … libavcodec60 (>= 7:6.1), … libx264-164 (>= 2:0.164.3108+git31e19f9)`"; :3924 (S2-60) — "`libavcodec60` … 7:6.1.1-3ubuntu5"; read 2026-10-03
- slice: 9.10
- dates: archetypes 2026-10-03; catalog 2026-10-16; changed-after-read: yes (catalog)
- verdict: TRACED

### D-F3-37 — Big Buck Bunny's 4K 30 fps edition
- source: `big-buck-bunny` (docs/references.md:439)
- repo: dataset/archetypes.yaml:1627-1628 — "the Blender Foundation's Big Buck Bunny in its 4K 30 fps H.264 edition, whole (19,036 frames, 634.5 s)"; docs/workload/measurement-overview.md:52
- record: S2-project-docs.md:3858 (S2-53) — "one video track, `avc1` 3840×2160, `avcC` profile 100 (High) level 51, 19,036 samples of 1,000 at timescale 30,000 — 30 fps, 634.533 s" (the reader's reading of the file's boxes; zip SHA-256 750b255c…, read 2026-10-03)
- slice: 9.10
- dates: 2026-10-03; changed-after-read: no
- verdict: TRACED

### D-F3-38 — CpsMark+'s HandBrake workload: H.264 to a 1080p "2K"
- source: `cpsmarkplus` (docs/references.md:454), `cpsmark-tbench23`, with `dci-dcss` for "2K"
- repo: dataset/archetypes.yaml:1629-1630 — "CpsMark+'s HandBrake workload, its H.264 codec and its 1080p \"2K\" from the benchmark's own code, its clip and its preset's settings not"; docs/workload/scenario-catalog.md:19 — "read from the benchmark's own code as H.264 to 1080p"; docs/workload/measurement-overview.md:52; docs/references.md:456
- record: S2-project-docs.md:3903 (S2-58) — "`SW_PRESET_NAME = _T(\"fast_1080p_h264_sw\")` … logged as \"Handbrake:4K->2K视频转码进行中...\""; "the preset's settings are not read beyond its name"; copy commit bf24434, read 2026-10-03; :3871 (S2-54, DCI: "A 2K distribution – the resolution of the DCDM*[3] container is 2048x1080")
- slice: 9.10
- dates: archetypes 2026-10-03; catalog 2026-10-16; overview 2026-10-17; changed-after-read: yes (docs)
- verdict: TRACED

### D-F3-39 — CpsMark+'s source has no licence
- source: `cpsmarkplus`, `cpsmark-tbench23`
- repo: docs/workload/source-vetting.md:137 — "the paper publishes its control program's source and its resource packages and names open source as a design criterion, but states no software licence, and the GitHub repository has no licence file"
- record: 2026-09-13-verification/reads/R04-cpsmark.md:284-300 (C-cpsmark-8) — "The benchmark should be open-source and vendor-neutral"; "no LICENSE file in the tree; GitHub API reports `license: null`"; read 2026-09-13
- slice: other (2026-09-13 verification)
- dates: 2026-10-17 (c59b6a89); changed-after-read: yes
- verdict: TRACED

### D-F3-40 — the shaped link's rate, 121.0 Mbps
- source: `steam-download-stats` (docs/references.md:509)
- repo: docs/workload/measurement-overview.md:52 — "over a link shaped to 121.0 Mbps, the byte-weighted median of Valve's per-country download rates (`steam-download-stats`)"; dataset/archetypes.yaml:1411; docs/references.md:511
- record: task-9.7-background-io/changelog.md:61 (D11) — "121.0 Mbps — the median, weighted by bytes downloaded, of the per-country \"Average Download Rate\" … version `09-19-2026-04` … fetched 2026-09-19 04:44 UTC … country table SHA-256 03af9f1d…; Computation (ours)", corrected by D38, D40
- slice: 9.7
- dates: archetypes 2026-09-23 (fold-in); overview 2026-10-01 / 2026-10-17; changed-after-read: yes (overview)
- verdict: TRACED (the statistic is labelled the project's own)

### D-F3-41 — SteamCMD, its anonymous depot and the desktop client's account
- source: SteamCMD (untagged; 9.7 D4)
- repo: dataset/archetypes.yaml:1409-1410 — "SteamCMD (build 1788292693) logged in anonymously, installing the Team Fortress 2 Dedicated Server depot (app 232250 …)"; :1436-1438 — "the desktop client was not observed — it needs a logged-in account … SteamCMD's own connection limit is undocumented"
- record: task-9.7-background-io/changelog.md:27 (D4) — "the desktop client needs a logged-in account … SteamCMD, Valve's command-line client, logged in anonymously and fetching a free dedicated-server depot that Valve's list marks anonymous (S4-16; e.g. Team Fortress 2 Dedicated Server, app 232250) … SteamCMD's own connection limit is undocumented, S4 Not found 4"; builds are the run's records
- slice: 9.7
- dates: 2026-09-23 (884b3ef6, fold-in); changed-after-read: no
- verdict: TRACED

### D-F3-42 — 7-Zip 23.01 is Ubuntu 24.04's `7z`, at its default format and level
- source: Ubuntu `7zip` / `p7zip-full` (untagged)
- repo: dataset/archetypes.yaml:1354-1355 — "7-Zip 23.01 (Ubuntu 24.04's `7zip`) at its default format and level with eight threads (`-mmt8`, the `nproc` rule on an eight-thread desktop, D9)"
- record: task-9.7-background-io/changelog.md:49 (D9) — "on noble `p7zip-full 16.02+transitional.1` only depends on `7zip (>= 23.01+dfsg-4~)` (packages.ubuntu.com/noble/p7zip-full, read 2026-09-19, local `sources/D9/p7zip-full-noble.html`, SHA-256 81984122…6794) … at its default format and level, read from its own help on the runner"
- slice: 9.7
- dates: 2026-09-22 (b2f19712); changed-after-read: no
- verdict: TRACED

### D-F3-43 — what Ubuntu 24.04's desktop image holds (the package rule)
- source: `ubuntu-desktop-manifest` (docs/references.md:514)
- repo: docs/references.md:515-518 (1,836 lines, 1,823 debs and 13 snaps; holds `sysstat`, `systemd` …, no `php8.3-fpm`, `podman`); docs/workload/measurement-overview.md:199 — "what a stock Ubuntu 24.04 desktop holds and runs"; the session entries' scopes "a package Ubuntu 24.04's desktop manifest does not hold"
- record: task-9.9-daemons-session/changelog.md:444 — "`ubuntu-24.04.5.1-desktop-amd64.manifest` at releases.ubuntu.com/24.04/, SHA-256 6c200933…f8ff … its 1,836 lines are 1,823 deb packages and 13 snaps"; task-9.10-scenarios-timelines/search/S2-project-docs.md:75-81 (S2-01, the layers' manifests verbatim, read 2026-10-01)
- slice: 9.9, 9.10
- dates: overview 2026-10-01 (1abb56ba); read 2026-09-29 / 2026-10-01; changed-after-read: no
- verdict: TRACED

### D-F3-44 — no distro or vendor starts an ML-training, render or transcode job unasked; the transcoders' names
- source: Jellyfin 12.0, Plex Media Server 1.43.4 (untagged; 2026-09-13 verification C-plain-4, C-plain-5)
- repo: dataset/timelines/coreset/c7.variant.yaml:67-70 — "No distro or vendor was found starting an ml-train, render or transcode job unasked (the 2026-09-13 verification: Jellyfin runs its transcoder as plain `ffmpeg` and Plex as `Plex Transcoder`, neither found converting media on a schedule)"
- record: 2026-09-13-verification/reads/R11-focal-plain.md:1538-1652 (C-plain-4, FOUND); :1692 — "No distribution-default ML **training** job was found"; :1752-1753 (render, PARTIAL: no distribution-started scheduled rendering job); :1755-1800 (Jellyfin's daily `AudioNormalization` runs ffmpeg with `-f null` — analysis, not conversion; `Plex Transcoder` in the .deb file list); copies with tags and commits at :58-70, read 2026-09-13
- slice: other (2026-09-13 verification)
- dates: 2026-10-06 (a157d47b, 9.10 D162); read 2026-09-13; changed-after-read: yes (written by 9.10 from the 2026-09-13 record)
- verdict: TRACED

### D-F3-45 — the one unasked backup under its own name, dpkg's daily database backup
- source: dpkg 1.22.6ubuntu6.6; a Mint 22.1 journal (untagged; 9.10 D9)
- repo: dataset/timelines/coreset/c7.variant.yaml:56-58 — "the one unasked backup under its own name, dpkg's daily `dpkg-db-backup`, finished in the second it started on the one desktop observed"; :71
- record: task-9.10-scenarios-timelines/changelog.md:165 (D9) — "`dpkg` enables `dpkg-db-backup.timer` (`OnCalendar=daily`, `Persistent=true`) … It finished in the second it started on one Mint 22.1 desktop (S3-35a)"; search/S3-traces-datasets.md:584-587 (S3-35a, GitHub issue copy SHA-256 01680a6b…, read 2026-10-01, reader's own computation at 1-s journal resolution)
- slice: 9.10
- dates: 2026-10-06 (a157d47b, 9.10's own later rebind restating D9); changed-after-read: no
- verdict: TRACED

### D-F3-46 — design and arithmetic labels in the compile, backup, indexing and transcode timelines
- source: none (labelled values)
- repo: c1-compile.timeline.yaml:4-6, c1-backup.timeline.yaml:5-6, c1-transcode.timeline.yaml:7-10 — "The segment is the smallest whole second by which the build ends under every policy (9.10 D78's arithmetic, D90's form)"; c1-indexing.timeline.yaml:2-8 — the user's own reset, "a pre-committed miss"; c2-pairs.variant.yaml:61-62 — "the length is 9.10 D123's, set on a shared lane"; c7.variant.yaml:65-72 — the batch counterparts' label flip, "Each file ships as a pre-committed miss"; every `total_work` tagged `meas-ci` (out of scope)
- record: task-9.10-scenarios-timelines/changelog.md (D78, D90, D123 cited by number in each file)
- slice: 9.10
- dates: 2026-10-06 to 2026-10-11; changed-after-read: n/a
- verdict: LABELLED (labels present and honest; `parallelism_cap` is D-F3-08)


# F4 — browser, comms, session, scenario benchmarks, bound programs

Scope: the F4 ids as cited in dataset/archetypes.yaml, dataset/sources.yaml, dataset/grids.yaml, dataset/variants.yaml, dataset/timelines/coreset/*, dataset/README.md, docs/workload/*.md and their docs/references.md entries. F4 ids that no in-scope file cites, so no rows: `mpv`, `chromium` (cited only by docs/simulator/simulator-guide.md), `vulkan`, `gstreamer`, `pipewire-conf`, `jackd-man`, `ardour-manual`, `obs-studio`, `obs-kb-encoding`, `llamacpp`, `vllm-docs`, `ollama-docs`, `localscore`, `artificialanalysis`, `ubuntu-desktop-bootstrap` (it grounds 9.9 decision D47, but no dataset file or workload doc names it). `meas-ci` values are not listed.

Record abbreviations, with the copy each one read:
- R04 = `_dev/research/jioh/2026-09-13-verification/reads/R04-cpsmark.md`: the publisher's PDF in a Wayback capture taken 2023-01-14, SHA-256 04d9f106…, read 2026-09-13 and re-fetched byte-identical 2026-10-01 (9.10 decision D1).
- R05 = `_dev/research/jioh/2026-09-13-verification/reads/R05-vendor-benchmarks.md`: the copies table at R05:9-22, all read 2026-09-13.
- 9.5-S7 = `_dev/research/jioh/task-9.5-interactive-typing/search/S7-benchmark-inputs.md`: R05's copies, read 2026-09-16.
- 9.10-S2 / 9.10-S3 = `_dev/research/jioh/task-9.10-scenarios-timelines/search/S2-project-docs.md` / `S3-traces-datasets.md`.
- 9.8-S2 = `_dev/research/jioh/task-9.8-browser-comms/search/S2-project-docs.md`; 9.9-S2 = `_dev/research/jioh/task-9.9-daemons-session/search/S2-project-docs.md`.

"Line last changed" is from `git blame` on the primary line. "Changed-after-read: yes" means the claim's own wording changed after the read date (checked with `git log -L` / `--word-diff`), not just a neighbouring word on the same line.

### D-F4-01 — what CpsMark+ calls its usage scenarios, and which applications each one runs
- source: `cpsmark-tbench23` (docs/references.md:32-35, scholarly)
- repo: docs/workload/scenario-catalog.md:12 — "CpsMark+ document manipulation, Word → LibreOffice Writer (`cpsmark-tbench23`), which lists products, not process names"; also :13 "CpsMark+ Internet service (`cpsmark-tbench23`)", :15 "CpsMark+ Internet service, Outlook → Thunderbird", :17 "CpsMark+ graphic design, Photoshop → GIMP", :33 "CpsMark+'s scenarios S1, S2, S4, S6 and S8"; dataset/sources.yaml:104-106 "Establishes the existence of the office, browsing, mail, photo, transcode and archive scenarios (S1, S2, S4, S6, S8, S16)"; docs/workload/grounding-sources.md:17 "the existence of the office, browsing, mail, photo, transcode and archive scenarios"; docs/references.md:34
- record: R04:23-30 — "we cluster the usage models into four groups of common office scenarios … i.e., document manipulation, Internet service, graphic design, and multimedia processing"; R04:100-127, the applications in each scenario ("Internet service (CA): Chrome, Outlook"); copy: R04's.
- slice: other (the 2026-09-13 verification read, re-checked by 9.10 decision D1)
- dates: line last changed 2026-10-17 (6f508a59); read 2026-09-13; changed-after-read: yes (6f508a59 added the "Word → LibreOffice Writer" mappings; 34b09357 rewrote the row on 2026-10-16)
- verdict: TRACED

### D-F4-02 — whether CpsMark+ includes an archiving workload, and what it works on
- source: `cpsmark-tbench23`
- repo: docs/references.md:34 — "the existence of archiving — its WinRAR workload, under document manipulation, compresses and decompresses \"mixed files in multiple formats\" (Table 2, §4.3.4)"; also dataset/sources.yaml:104-105 (S16)
- record: R04:130 — "WinRAR is placed under \"document manipulation\" in Table 2"; R04:156 — "WinRAR (its inputs are \"mixed files in multiple formats\")"
- slice: other (the 2026-09-13 verification read)
- dates: line last changed 2026-10-17 (6f508a59); read 2026-09-13; changed-after-read: yes
- verdict: TRACED

### D-F4-03 — CpsMark+'s modules, its user-profile table and its application table
- source: `cpsmark-tbench23`
- repo: dataset/sources.yaml:107-109 — "four office usage scenarios merged into two modules (CA light/middleweight, CC heavyweight); user-profile tiers (table-1); named applications with versions (table-2)"
- record: R04:29-30 — "Comprehensive Application (CA) module … light and middleweight use"; "Comprehensive Calculation (CC) module … heavy-weight use"; R04:44-64 (Table 1, Table 2)
- slice: other (the 2026-09-13 verification read)
- dates: line last changed 2026-10-07 (723bda39); read 2026-09-13; changed-after-read: no (723bda39 re-wrapped these lines; this clause's wording is the same)
- verdict: TRACED

### D-F4-04 — the user-behaviour stages of CpsMark+'s CA workflow, cited only for the existence of the transitions between them
- source: `cpsmark-tbench23`
- repo: dataset/sources.yaml:109-111 — "the CA cooperative workflow's order (Internet -> creation -> document processing -> email delivery), cited for its transitions' existence (9.10 D29)"; also docs/workload/building-plan.md:133 "CpsMark+'s CA cooperative workflow (`cpsmark-tbench23`) defines the browsing → office → mail transitions"; dataset/timelines/coreset/c3-workday.timeline.yaml:2-3 "The order is design; CpsMark+'s CA workflow defines the browsing -> office -> mail transitions (existence)"; docs/workload/grounding-sources.md:17; docs/references.md:34
- record: R04:143 — "the workloads of the CA module simulate the following coherent user behaviors: resource preparation via the Internet, content creation, document processing, and email delivery"; R04:154 — the CA order "Chrome → PowerPoint → Word → Excel → Acrobat → WinRAR → Outlook"
- slice: other (the 2026-09-13 verification read)
- dates: line last changed 2026-10-07 (723bda39); read 2026-09-13; changed-after-read: yes ("cited for its transitions' existence" added on 2026-10-07)
- verdict: TRACED

### D-F4-05 — the order of CpsMark+'s CC module (photo editing, then video, then transcode) and whether any workload's output feeds the next
- source: `cpsmark-tbench23`
- repo: docs/workload/building-plan.md:135 — "CpsMark+ holds photo → video → transcode only as a subsequence, no handoff stated"
- record: R04:427 — "fixed order Photoshop → AutoCAD → 3ds Max → Premiere → After Effects → HandBrake … No output→input chain is stated for any CC workload"
- slice: other (the 2026-09-13 verification read)
- dates: line last changed 2026-10-16 (34b09357); read 2026-09-13; changed-after-read: yes
- verdict: TRACED

### D-F4-06 — CpsMark+'s hardware sensitivity: the graphics-card figure for each module
- source: `cpsmark-tbench23`
- repo: dataset/sources.yaml:112-115 — "the CC module's best graphics-card configuration performing 1.77 times its base configuration and the CA module showing no significant difference (sec-4.7.2)"; also docs/references.md:34; docs/workload/archetype-plan.md:121 "CpsMark+ Table 4's hardware sensitivity per workload remains a citation about resource mixes"
- record: R04:237 — "The CC module has a significantly higher sensitivity to the graphics card, the best configuration performs 1.77 times better than the base configuration, while there is no significant difference in the performance of …"
- slice: other (the 2026-09-13 verification read)
- dates: line last changed 2026-10-07 (723bda39); read 2026-09-13; changed-after-read: yes (the wording was "CC up to 1.77x GPU-sensitive, CA ~1.0x")
- verdict: TRACED

### D-F4-07 — CpsMark+'s target operating system, whether it has a gaming scenario, and whether it times processes
- source: `cpsmark-tbench23`
- repo: dataset/sources.yaml:115-117 — "Scope limits: Windows 10 applications — the Linux name mapping is ours; no gaming scenario; no process-level burst timing."; also docs/references.md:34
- record: R04:257 — "Note that CpsMark+ only supports Microsoft Windows 10."; R04:280 — "Gaming scenario: NOT FOUND … Per-process timing: NOT FOUND"
- slice: other (the 2026-09-13 verification read)
- dates: line last changed 2026-10-07 (723bda39, re-wrapped); read 2026-09-13; changed-after-read: no
- verdict: TRACED

### D-F4-08 — which benchmarks CpsMark+ compares itself against
- source: `cpsmark-tbench23`
- repo: docs/workload/grounding-sources.md:17 — "compares itself against SYSmark 2018 and PCMark 10 as state of the art"
- record: R04:339 — "CpsMark+ exhibits the highest repeatability against state-of-the-art commercial benchmarks, i.e., SYSmark 2018 and PCMark 10"
- slice: other (the 2026-09-13 verification read)
- dates: line last changed 2026-10-17 (c59b6a89); read 2026-09-13; changed-after-read: no (only "itself" was added)
- verdict: TRACED

### D-F4-09 — how CpsMark+ serves its browsing workload's pages, and what the pages contain (the input of the Chrome page-load operation)
- source: `cpsmark-tbench23`
- repo: docs/workload/measurement-overview.md:50 — "Chrome's page load of a built feed page (page kind from `pcmark10` and `cpsmark-tbench23`, sizes design)"; also docs/references.md:34 ("pages \"accessed through locally configured network services\" that \"contain text, pictures, JS (JavaScript) scripts\"")
- record: 9.5-S7:38 — "Webpages are accessed through locally configured network services. The webpages contain text, pictures, JS (JavaScript) scripts, and flash."; copy: R05's copies, read 2026-09-16
- slice: other (9.5 interactive/typing)
- dates: line last changed 2026-10-01 (1abb56ba); read 2026-09-16; changed-after-read: no
- verdict: TRACED

### D-F4-10 — CpsMark+'s mail workload: what it attaches and whether it replies (the input of the Thunderbird send operation)
- source: `cpsmark-tbench23`
- repo: docs/workload/measurement-overview.md:50 — "Thunderbird's send of a reply with a Word attachment (kind from `cpsmark-tbench23`, size design)"
- record: R04:113 — "Microsoft Outlook. Simulate users to receive, browse email contents and attachments offline, including Word, Excel, and PowerPoint files. Upload new attachments, edit the body of the email, and reply."
- slice: other (the 2026-09-13 verification read)
- dates: line last changed 2026-10-01; read 2026-09-13; changed-after-read: no
- verdict: TRACED

### D-F4-11 — CpsMark+'s bibliographic details
- source: `cpsmark-tbench23`
- repo: docs/references.md:33 — "*BenchCouncil Transactions on Benchmarks, Standards and Evaluations*, 2(4), 100084 (the October 2022 issue; available online 2023-01-05). DOI 10.1016/j.tbench.2023.100084"; also docs/workload/grounding-sources.md:17
- record: R04:449 — "Available online 5 January 2023"; R04:10-11 (Crossref: volume 2, issue 4, article 100084, published-print 2022-10; Elsevier coverDate 2022-10-31)
- slice: other (the 2026-09-13 verification read)
- dates: line last changed 2026-10-16 (69c16f54); read 2026-09-13; changed-after-read: no (the details match R04)
- verdict: TRACED

### D-F4-12 — PCMark 10's test groups and the workloads in each
- source: `pcmark10` (docs/references.md:222-225, deployed-system)
- repo: dataset/sources.yaml:122-126 — "the scenario groups and their application lists — Essentials (web browsing, video conferencing, app start-up), Productivity (spreadsheets, writing), Digital Content Creation (photo/ video editing, rendering), Gaming"; also docs/references.md:224; docs/workload/grounding-sources.md:14; docs/workload/scenario-catalog.md:13, :14, :17, :18 (Web Browsing, Video Conferencing, Photo Editing, Video Editing)
- record: R05:37-43 — "The Essentials test group … 1. App Start-up 2. Web Browsing 3. Video Conferencing"; "Productivity … 1. Writing 2. Spreadsheets"; "Digital Content Creation … 1. Photo Editing 2. Video Editing 3. Rendering and Visualization"; "Gaming test group uses a modified version of the Fire Strike test"; copy: R05:10, Technical Guide of 2021-02-11, SHA-256 d7603a6c…
- slice: other (the 2026-09-13 verification read)
- dates: line last changed 2026-10-07 (723bda39); read 2026-09-13; changed-after-read: no (the group list is unchanged; "Existence only (9.10 D33)" was added)
- verdict: TRACED

### D-F4-13 — the application PCMark 10's Writing workload runs
- source: `pcmark10`
- repo: docs/workload/scenario-catalog.md:12 — "PCMark 10 Productivity runs LibreOffice Writer (`pcmark10`)"; also :33 "S1 (Productivity's Writing)"
- record: 9.5-S7:43 — "pcmark10, p. 63 (Writing) … Implemented on LibreOffice Writer (p. 63)"; also 9.10-S2:2146 (the 2018 edition) — "The test uses LibreOffice Writer application"
- slice: other (9.5 interactive/typing); 9.10
- dates: line last changed 2026-10-17 (6f508a59); read 2026-09-16; changed-after-read: no (this clause was already present before 6f508a59)
- verdict: TRACED

### D-F4-14 — whether PCMark 10's guide documents per-task or per-process timing
- source: `pcmark10`
- repo: dataset/sources.yaml:125-126 — "The guide times each workload's scripted tasks; it documents no per-process timing."; also docs/references.md:224
- record: R05:150-157 — "Per-task timing: documented." … "Per-process timing: not documented."
- slice: other (the 2026-09-13 verification read)
- dates: line last changed 2026-10-07 (723bda39); read 2026-09-13; changed-after-read: yes ("Activity composition only; no per-process timing" was reworded to the current text)
- verdict: TRACED

### D-F4-15 — what PCMark 10's video-playback battery test is, and where it sits in the product
- source: `pcmark10`
- repo: docs/workload/scenario-catalog.md:24 — "PCMark 10's Video playback battery-life profile (`pcmark10`)"; also :33 "PCMark 10's groups define S1 (…), … and S13 (Video playback)"; docs/references.md:224 "the scenario catalog's rows cite its Productivity, Web Browsing, Video Conferencing, Photo Editing, Video Editing and Video-playback battery groups"
- record: R05:110 — "PCMark 10 Battery Life Profile provides a broad view of battery life across five common scenarios: modern office, applications, video, gaming, and idle time"; R05:66 — "Battery Life and Storage are separate profiles and benchmarks, not test groups"
- slice: other (the 2026-09-13 verification read)
- dates: line last changed 2026-10-16 (34b09357, :33); read 2026-09-13; changed-after-read: yes (note 1 at :33 was rewritten to "PCMark 10's groups define … S13" on 2026-10-16)
- verdict: WORDING-OUTSIDE-PASSAGE
- finding: The row at :24 is within the passage. Note 1 at :33 and the role line at docs/references.md:224 call video playback one of PCMark 10's "groups". R05:66 records that Battery Life is a separate profile, not a test group, and the video test is a "scenario" inside it. Fix: at :33, write "PCMark 10's groups define S1 …, S7 (Video Editing), and its Battery Life profile's Video scenario S13"; at references.md:224, change "Video-playback battery groups" to "the Battery Life profile's Video scenario".

### D-F4-16 — the inputs PCMark 10 gives its photo, video and browsing workloads (image size and filter, clip and sharpening, page kinds)
- source: `pcmark10`
- repo: docs/workload/measurement-overview.md:50 — "GIMP's unsharp mask on PCMark 10's image size and settings (`pcmark10`)"; also dataset/archetypes.yaml:538 "a 4952×3288 image open (PCMark 10 Photo Editing's interactive image size, Technical Guide p. 71 …); … (PCMark 10's batch unsharp parameters mapped onto GIMP's PDB, p. 74; design)"; :607 "PCMark 10 Video Editing's 1080p H.264, p. 76 … at PCMark 10's sharpening parameters (p. 76)"; :933; docs/references.md:224; docs/workload/grounding-sources.md:14
- record: 9.5-S7:21 — "INTERACTIVE RAW Fujifilm X-E1 24.9 MB 4952 × 3288" … "UnsharpMaskImage(radius 8, sigma 4, amount 32, threshold 3)"; 9.5-S7:29 — "Sharpens the 1080p H.264 video … unsharp=…lx=7:ly=7:la=0.56:cx=7:cy=7:ca=0.28"; 9.5-S7:37 — "The content is served with a local lightweight web server"
- slice: other (9.5 interactive/typing)
- dates: line last changed 2026-10-01 (measurement-overview.md:50); archetypes.yaml:607 changed 2026-10-17 (57342aab); read 2026-09-16; changed-after-read: no (the PCMark clauses are the same; 57342aab changed the trace-scope sentences on line 607)
- verdict: TRACED (the mapping of PCMark's parameters onto GIMP's is labelled design at archetypes.yaml:538)

### D-F4-17 — which edition of PCMark 10's guide was read, and the online guide that replaced it
- source: `pcmark10`
- repo: docs/references.md:223 — "*PCMark 10 Technical Guide*, updated February 11, 2021 (application 2.1.2508), 141 pp. … SHA-256 d7603a6c… The PDF has since been replaced by UL's online user guide (… application 2.3.2912), whose test-group structure is the same."
- record: R05:10-11 (the copies table); R05:66 — "current app 2.3.2912 raised the System/Express/Extended benchmarks to 2.0; the group structure in the online guide is unchanged"
- slice: other (the 2026-09-13 verification read)
- dates: line last changed 2026-10-16; read 2026-09-13; changed-after-read: no
- verdict: TRACED

### D-F4-18 — SYSmark 30's four scenarios and what each one models
- source: `sysmark30` (docs/references.md:227-230, deployed-system)
- repo: docs/references.md:229 (each scenario quoted); dataset/sources.yaml:131-135 — "four scenarios and their application lists — Office Applications, General Productivity (incl. archiving and unpacking a mixed file set, OCR, browsing), Photo Editing, Advanced Content Creation (incl. a multitasking workload switching photo<->video editing)"; docs/workload/grounding-sources.md:15
- record: R05:165-170 — "The General Productivity scenario models OCR of documents, web browsing, application installation, and archiving and unpacking a mixed file data set." … "A multitasking workload switches between photo editing and video editing workloads."; copy: R05:12, the Wayback capture 20250821210035 of the user guide v1.2
- slice: other (the 2026-09-13 verification read)
- dates: line last changed 2026-10-16 (69c16f54); read 2026-09-13; changed-after-read: yes (the role line was rewritten 2026-10-16; sources.yaml was reworded 2026-10-07)
- verdict: TRACED

### D-F4-19 — the applications SYSmark 30 names for each scenario (used for the scenario catalog's Windows → Linux rows)
- source: `sysmark30`
- repo: docs/references.md:229 — "Microsoft Excel / Outlook / PowerPoint / Word 2021 Professional Plus VL; … Corel WinZip 26.0, Google Chrome 106.0.5249.103; … Photoshop CC 23 and Premiere CC 22"; also docs/workload/scenario-catalog.md:12 ("Word → LibreOffice Writer"), :18 ("Premiere → Kdenlive"), :27 ("WinZip → 7-Zip")
- record: R05:218-223 (the user guide v1.2, p.34, the application list per scenario)
- slice: other (the 2026-09-13 verification read)
- dates: line last changed 2026-10-17 (6f508a59, the mappings added to the catalog); read 2026-09-13; changed-after-read: yes
- verdict: TRACED (the mapping to a Linux program is ours; see D-F4-41)

### D-F4-20 — SYSmark 30's archiving workload
- source: `sysmark30`
- repo: docs/workload/scenario-catalog.md:27 — "SYSmark 30 General Productivity's archive workload, WinZip → 7-Zip (`sysmark30`)"; also :33
- record: R05:181-185 — "General Productivity • … Corel WinZip 26.0 …"; "archiving and unpacking a mixed file data set"
- slice: other (the 2026-09-13 verification read)
- dates: line last changed 2026-10-17 (6f508a59); read 2026-09-13; changed-after-read: yes
- verdict: TRACED

### D-F4-21 — whether SYSmark 30 runs photo editing beside a background video encode, and whether it keeps Outlook open through the office scenario
- source: `sysmark30`
- repo: docs/workload/building-plan.md:135 — "SYSmark 30 Advanced Content Creation (`sysmark30`) defines photo editing beside a background encode"; also dataset/timelines/coreset/c3-creation.timeline.yaml:2-3 "SYSmark 30 ACC defines photo editing beside a background encode (existence)"; docs/workload/scenario-catalog.md:15 "SYSmark 30 keeps Outlook open (`sysmark30`)"; :33 "Office Applications, Outlook open beside it for S4"; docs/references.md:229 "its multitasking workload is an overlap, not a sequence"
- record: R05:206 (whitepaper v1.2 §2.2, PDF p.11) — "A video encode is started in Adobe Premiere and sent to the background while Adobe Photoshop is launched and used to manipulate photos in the foreground"; R05:229 — "The whitepaper adds that Outlook \"is launched and remains open throughout the scenario for ambient load\" (PDF p.10)"; R05:209 — the user guide "gives no order … The order is NOT FOUND in the user guide and FOUND only in the separate whitepaper"; also 9.10-S2:2378 (the same whitepaper, read 2026-10-01)
- slice: other (the 2026-09-13 verification read); 9.10
- dates: line last changed 2026-10-16 (34b09357); read 2026-09-13; changed-after-read: yes
- verdict: WORDING-OUTSIDE-PASSAGE
- finding: The repository states both facts as `sysmark30`'s, and that entry's cite (docs/references.md:228) is the User Guide v1.2 alone. Both passages are in BAPCo's separate whitepaper v1.2 ("SYSmark 30 – An Overview of SYSmark 30"). The user guide says only that the multitasking workload "switches between photo editing and video editing", and it lists Outlook without saying it stays open. Fix: add the whitepaper v1.2 (Wayback 20251031005630, SHA-256 4111c36e…) to the `sysmark30` cite, with its locators (p.10, p.11), or give it its own entry and cite that at building-plan.md:135, c3-creation.timeline.yaml:2, scenario-catalog.md:15 and :33.

### D-F4-22 — which copy of SYSmark 30's user guide was read, and when
- source: `sysmark30`
- repo: docs/references.md:228 — "(accessed 2026-09-12)"; :230 — "the guide was read from the Internet Archive's capture of BAPCo's own URL (snapshot 2025-04-23)"
- record: R05:12 — "Copy taken from https://web.archive.org/web/20250821210035id_/https://bapco.com/wp-content/uploads/2025/04/bapco-sysmark30-user-guide-v1.2.pdf", retrieved 2026-09-13 (R05:3)
- slice: other (the 2026-09-13 verification read)
- dates: line last changed 2026-10-16; read 2026-09-13; changed-after-read: n/a (no record of the stated copy)
- verdict: NO-RECORD
- finding: No read record holds a 2025-04-23 snapshot or a 2026-09-12 access (a search of `_dev/research` for 20250423 finds only unrelated files). The persisted read is the 2025-08-21 capture, retrieved 2026-09-13. Fix: state the R05 copy (capture 20250821210035, retrieved 2026-09-13) in the cite and status lines.

### D-F4-23 — whether SYSmark 25 includes code compilation, and in what form
- source: `sysmark25` (docs/references.md:232-235, deployed-system)
- repo: docs/references.md:234 — "The Productivity scenario's description names \"software development (code compilation)\" (p. 32); no compiler or IDE appears in any application list (p. 31)"; also docs/workload/scenario-catalog.md:22 "SYSmark 25 names compilation only in a scenario description (`sysmark25`)"; :33; docs/workload/grounding-sources.md:15
- record: R05:319 — "Productivity — The Productivity scenario models office environment like usage including … software development (c[ode compilation])"; R05:336-340 — "\"Software development (code compilation)\" appears only in the Productivity scenario description … no compilation application is identified"
- slice: other (the 2026-09-13 verification read)
- dates: line last changed 2026-10-07 (723bda39); read 2026-09-13; changed-after-read: yes (it was "grounds compile as a mainstream desktop scenario" before 723bda39)
- verdict: TRACED (grounding-sources.md:15 labels "that it is a mainstream desktop scenario is our inference")

### D-F4-24 — which SYSmark versions define Productivity, Creativity and Responsiveness
- source: `sysmark25`
- repo: docs/references.md:234 — "SYSmark 2018 already defines the same three scenarios, Productivity, Creativity and Responsiveness, its Productivity naming software development; SYSmark 30 carries neither"; also docs/workload/grounding-sources.md:15
- record: R05:342-370 (C-sysmark25-2: the SYSmark 2018 user guide, revision 1.3); R05:161-175 (SYSmark 30's four scenarios)
- slice: other (the 2026-09-13 verification read)
- dates: line last changed 2026-10-07; read 2026-09-13; changed-after-read: yes
- verdict: TRACED

### D-F4-25 — which copy of SYSmark 25's user guide was read
- source: `sysmark25`
- repo: docs/references.md:233 — "Revision 1.9, 37 pp. … Internet Archive's capture of that URL (2024-05-24 …) … SHA-256 865081c8… Revision 1.4 (2020-09) carries the same scenario text"
- record: R05:15 (the copies table: "Revision: 1.9", 37 pp., SHA-256 865081c8…, v1.4 "Its scenario text is the same")
- slice: other (the 2026-09-13 verification read)
- dates: line last changed 2026-10-07; read 2026-09-13; changed-after-read: no
- verdict: TRACED

### D-F4-26 — how many benchmarks UL Procyon lists, and how many of them run AI inference locally
- source: `procyon` (docs/references.md:237-240, deployed-system)
- repo: docs/workload/grounding-sources.md:16 — "UL's suite of ten benchmarks, three of them local-AI inference (text generation, image generation, computer vision)"; also docs/references.md:239 "of the ten benchmarks the overview page lists, three are AI workloads … The other seven: … and \"AI Inference Benchmark for Android\""
- record: R05:414-421 — "The landing page lists 10 benchmarks. Built around local on-device AI inference (four): … AI Inference for Android (NNAPI; MobileNet V3, …)"; also "Procyon Essentials, whose background video call uses SAM 2.1-tiny via Windows ML"; re-read byte-identical 2026-10-09 (9.12 search record V60, `_dev/research/jioh/task-9.12-related-work-prose/search/V60-vol02-quotations.md:456`)
- slice: other (the 2026-09-13 verification read; 9.12)
- dates: line last changed 2026-10-17 (c59b6a89); read 2026-09-13; changed-after-read: yes (c59b6a89 wrote the "three of them" wording)
- verdict: WORDING-OUTSIDE-PASSAGE
- finding: The record counts four benchmarks built around on-device AI inference, including AI Inference for Android, which the repository's "three" (and references.md's "other seven") puts among the non-AI ones. Fix: "ten benchmarks, four of them on-device AI inference (text generation, image generation, computer vision, and inference on Android)". If only desktop is meant, say "three desktop AI inference benchmarks, beside one for Android".

### D-F4-27 — the applications behind Procyon's office, photo and video benchmarks
- source: `procyon`
- repo: docs/references.md:239 — "Office Productivity (Word, Excel, PowerPoint, Outlook), Photo Editing (Adobe Lightroom, Adobe Photoshop), Video Editing (Adobe Premiere Pro)"; also docs/workload/grounding-sources.md:16
- record: R05:431-440 — "The benchmark workloads are built on relevant, real-world tasks using Microsoft Word, Excel, PowerPoint and Outlook." (C-procyon-2)
- slice: other (the 2026-09-13 verification read)
- dates: line last changed 2026-10-16; read 2026-09-13; changed-after-read: yes (role line rewritten)
- verdict: TRACED

### D-F4-28 — how Microsoft Teams runs on Linux
- source: `teams-pwa-linux` (docs/references.md:242-245, deployed-system)
- repo: docs/workload/scenario-catalog.md:14 — "Teams on Linux runs as a web app in the browser (`teams-pwa-linux`)"; also docs/references.md:244
- record: 9.10-S2:3383-3389 — "general availability of support for the Microsoft Teams progressive web app (PWA) as a feature of our current web client for Linux customers … The PWA experience is available for both Edge and Chrome browsers running on Linux"; copy: the techcommunity URL, SHA-256 67a9c24c…, accessed 2026-10-01
- slice: 9.10
- dates: line last changed 2026-10-17 (6f508a59, the tag `teams-pwa-linux` replaced "(9.10 D24)"); read 2026-10-01; changed-after-read: no (only the cited tag changed; the wording was the same before)
- verdict: TRACED

### D-F4-29 — what Firefox's tab-count telemetry probe measures, and the population GLAM serves
- source: `glam` (docs/references.md:540-543, deployed-system)
- repo: dataset/sources.yaml:195-198 — "probe browser_engagement_max_concurrent_tab_count (versions 137-156, Linux, Windows and Darwin): the per-subsession maximum of open tabs across all windows"; also docs/references.md:541-542
- record: 9.10-S3:639 — "The count of maximum number of tabs open during a subsession, across all windows, including tabs in private windows and restored at startup."; copy: 9.10-S3:635-636 (GLAM API, metrics.yaml at cf519493…, accessed 2026-10-01, SHA-256 b302a119…)
- slice: 9.10
- dates: line last changed 2026-10-11 (b5678087, entry added); read 2026-10-01; changed-after-read: yes (the entry was written after the read)
- verdict: TRACED

### D-F4-30 — the Linux median per-client peak of open tabs and of open windows in Firefox release 152
- source: `glam`
- repo: docs/references.md:542 — "Linux, release 152, 7,535,303 clients: the median per-client peak of concurrent tabs 4.67, so five tabs; windows, the median per-client peak 1. The Linux median of the tab peak holds at 3.4–5.0 across releases 137–156"; also docs/workload/building-plan.md:116 "five the median per-client peak of concurrent tabs and one window the median peak of windows in Firefox's Linux telemetry"; dataset/timelines/coreset/c1-browsing.timeline.yaml:4, c1-office.timeline.yaml:3, c3-workday.timeline.yaml:5, c3-evening.timeline.yaml:4 ("five tabs from Firefox's Linux telemetry"); c4.variant.yaml:47; docs/workload/grounding-sources.md:51; docs/workload/measurement-overview.md:198
- record: 9.10-S3:647-651 — "Columns: p25 / p50 / p75 / p95 / p99"; "Max concurrent tabs, Linux, v152 — `max`: 1.98 / 4.67 / …(total_users 7,535,303)"; "Max concurrent windows … `max`: 1 / 1 / 1.93 …"; "Linux `max` median 3.4–5.0 tabs across the 20 versions"; 9.10 changelog.md:291, :313 (decisions D15 and D16)
- slice: 9.10
- dates: line last changed 2026-10-04 (references.md:542); building-plan.md:116 changed 2026-10-17 (2f9f8a0b); read 2026-10-01; changed-after-read: yes (building-plan.md:116 was reworded on 2026-10-17)
- verdict: TRACED

### D-F4-31 — whether Firefox's telemetry counts tabs per window
- source: `glam`
- repo: docs/workload/coreset-guide.md:197 — "Firefox Linux telemetry의 창당 탭 다섯(`glam`)" ("five tabs per window, from Firefox's Linux telemetry")
- record: 9.10-S3:639 — the probe counts tabs "during a subsession, across all windows"; the window count is a separate probe (9.10-S3:640); 9.10 changelog.md:309 (decision D16) composes "one browser window" from the window median
- slice: 9.10
- dates: line last changed 2026-10-16 (4b966f84); read 2026-10-01; changed-after-read: yes
- verdict: WORDING-OUTSIDE-PASSAGE
- finding: "Five tabs per window" attributes a per-window figure to the telemetry. The probe counts tabs across all windows, and the one window is a second statistic composed by decision D16. Fix: "Firefox Linux telemetry의 탭 다섯과 창 하나(`glam`)" (five tabs and one window), as building-plan.md:116 states it.

### D-F4-32 — whether Firefox's tab count stands for Chrome's, and how 4.67 becomes five
- source: `glam`
- repo: dataset/sources.yaml:199-201 — "Firefox's distribution read for Chrome's tab count is our modeling (archetypes.yaml `renderer-hidden`)"; docs/references.md:542 "A user-side value from Firefox, not Chromium; … the median of a per-client peak errs high for a random instant (D15's stated choice)"
- record: 9.10 changelog.md:291 (decision D15: "4.67 … so 5 tabs"); 9.10-S3:651 ("it is Firefox, not Chromium")
- slice: 9.10
- dates: 2026-10-11; read 2026-10-01; changed-after-read: n/a (a label)
- verdict: LABELLED (the label is present and honest)

### D-F4-33 — when Glean's metrics-ping thread wakes in Thunderbird
- source: `glean` (docs/references.md:419-422, deployed-system)
- repo: docs/workload/measurement-overview.md:200 — "Thunderbird's daily 04:00 metrics thread, stated as a clock event"; also docs/references.md:421 ("`const SCHEDULED_HOUR: u32 = 4;` … spawned as `\"glean.mps\"` … reschedules for the next day's 04:00")
- record: `_dev/research/jioh/task-9.5-interactive-typing/changelog.md:753` (decision D91) — "`glean.mps` is Glean's metrics-ping scheduler, which waits until 04:00 local time … (`glean`)", which paraphrases and points to the docs/references.md entry. The verbatim `scheduler.rs` passages and their commit (25b0fb2, 2026-09-28) are only in docs/references.md:420-421. A search of `_dev/research` for `SCHEDULED_HOUR` / `scheduler.rs` finds no slice record. 9.10-S3:645 (the Glean book, read 2026-10-01) — "the collection is scheduled daily at 04:00" covers the ping schedule but not the thread.
- slice: other (9.5); 9.10
- dates: line last changed 2026-10-01; read 2026-09-28; changed-after-read: no
- verdict: RECORD-BELOW-STANDARD
- finding: The thread-level claim (`glean.mps`, 04:00 local, daily reschedule) has its passage, locator and copy only in the citation index. No slice read record holds them. Fix: persist the 2026-09-28 read of `glean-core/src/scheduler.rs` at 25b0fb2 (the passages references.md:421 quotes, with line numbers) as a 9.5 search record, and point decision D91 to it.

### D-F4-34 — what Matt Mahoney's 10 GB benchmark set holds and where it came from
- source: `mahoney-10gb` (docs/references.md:424-427, deployed-system)
- repo: docs/workload/measurement-overview.md:52 — "Matt Mahoney's 10 GB benchmark set, 79,431 files from one laptop (`mahoney-10gb`)"; also docs/references.md:426
- record: `_dev/research/jioh/task-9.7-background-io/search/T9-S2-project-docs.md:339` — "It consists of exactly 10 GB (10^10) bytes in 79,431 files in 4006 directories from my Windows laptop collected from 2009 to 2013"; copy: :335 (mahoney-10gb.html, SHA-256 72df2093…), search log date 2026-09-19
- slice: 9.7 (background/IO)
- dates: line last changed 2026-10-17 (c59b6a89); read 2026-09-19; changed-after-read: no (the Mahoney clause predates c59b6a89, which replaced "borg" with "Déjà Dup's incremental")
- verdict: TRACED

### D-F4-35 — HippoCamp's Bei profile: the revision, the file count and how the profile was built
- source: `hippocamp` (docs/references.md:429-432, deployed-system)
- repo: dataset/archetypes.yaml:1559 — "The home holds HippoCamp's Bei profile (`hippocamp`, revision ff212ff7, `Bei/Fullset/Bei`: 875 files"; also docs/workload/measurement-overview.md:52; docs/references.md:430-431
- record: 9.10-S3:937-942 — revision ff212ff7…; README "`bei_fullset` 875"; reader's own reading of the API listing, "Bei 875 files, 40.66 GB"; README "built from anonymized archetypal personal-computing environments rather than a verbatim dump of a single person's machine"; re-read 2026-10-02
- slice: 9.10
- dates: line last changed 2026-10-03 (references.md:431); read 2026-10-02; changed-after-read: no
- verdict: TRACED (placing the tree as `~/Documents` is decision D68's design)

### D-F4-36 — PyTorch's Basic MNIST example: its commit, how it is run and its defaults
- source: `pytorch-examples` (docs/references.md:434-437, deployed-system)
- repo: dataset/sources.yaml:175-180 — "PyTorch's \"Basic MNIST Example\" at commit acc295d … run as the README's `python main.py` with `--save-model` at the defaults"; also docs/references.md:436 ("14 epochs of batch 64 … a test pass of batch 1,000 … the checkpoint written (`main.py:75–137`)"); dataset/archetypes.yaml:923-925; docs/workload/scenario-catalog.md:23; dataset/timelines/coreset/c1-ml-train.timeline.yaml:2-3
- record: 9.10-S2:3617-3622 — "`mnist/README.md:1–5`: \"# Basic MNIST Example\" / … / \"python main.py\""; "`--batch-size` … default=64", "`--test-batch-size` … default=1000", "`--epochs` … default=14", "`--save-model`"; copy: a shallow clone at acc295dc…, accessed 2026-10-01
- slice: 9.10
- dates: line last changed 2026-10-11 (b5678087); read 2026-10-01; changed-after-read: yes (the entry was written after the read)
- verdict: TRACED

### D-F4-37 — how Kdenlive 23.08.5 exports: the processes it starts and its default render profile
- source: `kdenlive` (docs/references.md:459-462, deployed-system)
- repo: dataset/sources.yaml:185-188 — "the render dialog starts `kdenlive_render`, which runs `melt-7` on the project's playlist with the shipped default MP4-H264/AAC profile"; also docs/references.md:461; dataset/archetypes.yaml:929-935 ("x264 `veryfast`, CRF 23, a GOP of 15, AAC at 160 kb/s, one processing thread"); docs/workload/scenario-catalog.md:18; dataset/timelines/coreset/c1-render.timeline.yaml:3-6
- record: 9.10-S2:3916-3922 — "`renderwidget.cpp:717`: … \"delivery\" … `:790`: `QProcess::startDetached(…)`"; "`renderjob.cpp:59`: `m_args << \"-progress\" << scenelist;`"; "`mltconnection.cpp:106`: `appName = QStringLiteral(\"melt-7\");`"; "`kdenlivesettings.kcfg:966–969`: … `<default>MP4-H264/AAC</default>`"; the profiles.xml defaults (veryfast, quality 23, g=15, audio 160); copy: clone of tag v23.08.5 (f027dc70…), accessed 2026-10-03
- slice: 9.10
- dates: line last changed 2026-10-11 (sources.yaml); read 2026-10-03; changed-after-read: yes (the entry was written after the read)
- verdict: TRACED

### D-F4-38 — what melt's progress loop does between progress reports
- source: `mlt` (docs/references.md:464-467, deployed-system)
- repo: docs/references.md:466 — "with `-progress`, melt's `transport` loop prints the frame and percentage and sleeps 40 ms, `struct timespec tm = {0, 40000000}`"; also docs/workload/measurement-overview.md:193 "the export and its progress loop"; dataset/archetypes.yaml:918 "melt's progress sleep"
- record: 9.10-S2:3936 — "`melt.c:407–413` … `struct timespec tm = {0, 40000000};` … `if (silent || progress) nanosleep(&tm, NULL);`"; copy: raw melt.c at v7.22.0 (4b427bfa…), accessed 2026-10-03
- slice: 9.10
- dates: line last changed 2026-10-04; read 2026-10-03; changed-after-read: no
- verdict: TRACED

### D-F4-39 — whether a stock Ubuntu 24.04 desktop runs `systemd-networkd`
- source: `systemd-ubuntu`, `netplan`, `livecd-rootfs` (docs/references.md:399-417, deployed-system)
- repo: docs/workload/measurement-overview.md:100 — "wakes caused by the harness or by software a stock Ubuntu 24.04 desktop does not run (`ubuntu-desktop-manifest`, `systemd-ubuntu`, `livecd-rootfs`, `netplan`) leave the components"; also :199; docs/references.md:401, :406, :416
- record: `_dev/research/jioh/task-9.9-daemons-session/changelog.md:341-349` (decision D37) — "Read in the primary texts, entered in `docs/references.md`:" followed by paraphrases. Decision D47 (changelog.md:454) quotes one passage verbatim, "If /etc/machine-id exists and is empty, a boot is not considered the first boot" (`man/machine-id.xml`). The other verbatim passages (`if (any_networkd) enable_networkd(...)`, "# Let NetworkManager manage all devices on this system", the postinst's "by default on new installs") are only in docs/references.md:401-416. `netplan`'s copy there is "branch `ubuntu/noble-updates` (accessed 2026-09-26)", with no commit. No 9.9 search record holds them (a search of `_dev/research` for `any_networkd` / `01-network-manager-all` finds only 9.10's untracked source copies and the 9.12 audit's copies of references.md).
- slice: 9.9 (daemons/session)
- dates: line last changed 2026-10-01; read 2026-09-26 and 2026-10-01; changed-after-read: no
- verdict: RECORD-BELOW-STANDARD
- finding: The slice record paraphrases and defers to the citation index. The verbatim passages and their copies live only there, and `netplan`'s copy is not pinned to a commit. Fix: persist the 2026-09-26 and 2026-10-01 reads (postinst, rules, links, 90-systemd.preset, main.c, manager.c, machine-id.xml; netplan's generate.c and parse.c; livecd-rootfs' functions) as a 9.9 search record with line locators and commits, pinning netplan's commit.

### D-F4-40 — GNOME's default idle delay, and what the session does when it is reached
- source: none tagged (vendor source code cited in the 9.9 search record)
- repo: docs/workload/measurement-overview.md:51 — "the session is left untouched until its 300 s idle delay locks the screen and blanks the monitor"
- record: 9.9-S2:348 — "`<key name=\"idle-delay\" type=\"u\">` / `<default>300</default>` / `<summary>Time before session is considered idle</summary>`"; 9.9-S2:333-336 (screenShield.js: the fade when the session goes idle); `_dev/research/jioh/task-9.9-daemons-session/campaign/method.md:31` — "the session goes idle at `idle-delay` (300 s, S2-14), the shield fades in over 10 s and locks with no delay (S2-13, S2-31)"; the dry run observed the blank (method.md:33)
- slice: 9.9
- dates: line last changed 2026-10-17 (c59b6a89); read 2026-09-22; changed-after-read: no (this clause is unchanged by c59b6a89)
- verdict: TRACED (caveat: S2-13 and S2-14 read GNOME 51.0's sources, while the measured session is GNOME 46; the runner's dry run observed the lock and the blank)

### D-F4-41 — mapping the benchmarks' Windows applications to Linux programs
- source: none (ours)
- repo: docs/workload/scenario-catalog.md:4 — "Where a taxonomy source names a Windows application, the mapping is recorded in the Source column"; rows :12, :15, :17, :18, :27 ("Word → LibreOffice Writer", "Outlook → Thunderbird", "Photoshop → GIMP", "Premiere → Kdenlive", "WinZip → 7-Zip"); dataset/sources.yaml:116 "the Linux name mapping is ours"
- record: n/a (design)
- dates: 2026-10-17; changed-after-read: n/a
- verdict: LABELLED (sources.yaml:116 calls the mapping ours; the catalog's arrow notation says it is a mapping, not the source's)

### D-F4-42 — whether the Ubuntu 24.04 GNOME 46 session at idle runs an X server
- source: none tagged (measurement and Mutter's source)
- repo: docs/workload/scenario-catalog.md:29 — "Ubuntu 24.04's GNOME 46 Wayland session at idle, blanked, which runs no X server"; also dataset/timelines/coreset/c1-idle.timeline.yaml:1-3
- record: `_dev/research/jioh/task-9.9-daemons-session/changelog.md:196` (decision D26) — "no `Xorg` or `Xwayland` process existed in any repeat's census or in any probe"; :206 (Mutter 46.2's defaults, S2-35)
- slice: 9.9
- dates: line last changed 2026-10-16; read 2026-09-24; changed-after-read: no
- verdict: TRACED (rests on the campaign's census, `meas-ci:session:2026-09-24`)

### D-F4-43 — how long Chromium waits before it throttles a background page's timer wake-ups, by default
- source: none tagged (Chromium source cited in the 9.8 search record)
- repo: docs/workload/measurement-overview.md:51 — "Background tabs are measured past Chromium's documented intensive-throttling grace"; dataset/archetypes.yaml:738 — "observed past Chromium's intensive-wake-up-throttling grace (… 330 s of the documented five-minute default …)"
- record: 9.8-S2:157 — "features.h:40–41: \"constexpr int kIntensiveWakeUpThrottling_GracePeriodSeconds_Default = 5 * 60;\""; copy: 9.8-S2:154 (chromium/src 999361f1…, gitiles, 2026-09-19)
- slice: 9.8 (browser/comms)
- dates: archetypes.yaml:738 last changed 2026-10-17 (57342aab); read 2026-09-19; changed-after-read: no (the throttling clause is unchanged)
- verdict: TRACED

### D-F4-44 — how Chromium on desktop Linux assigns renderer processes to pages
- source: none tagged (Chromium documentation)
- repo: dataset/archetypes.yaml:740 — "under Chromium's site-per-process model one renderer is one site, not one tab (S2-01)"
- record: 9.8-S2:77 — "### Full Site Isolation (site-per-process) / _Used on: Desktop platforms (Windows, Mac, Linux, ChromeOS)._ / In (one-)site-per-process mode, each process is locked to documents from a single site"; copy: 9.8-S2:75 (999361f1…, 2026-09-19)
- slice: 9.8
- dates: line last changed 2026-10-17 (7b024003); read 2026-09-19; changed-after-read: no (this clause is unchanged)
- verdict: TRACED

### D-F4-45 — whether Chromium on Linux marks a window covered by another application as occluded
- source: none tagged (Chromium source)
- repo: docs/workload/measurement-overview.md:51 — "the Steam client is measured with its window shown, which a game covering it would not change, since Linux Chromium tracks no cross-application occlusion"
- record: 9.8-S2:487-493 — "Chromium tracks cross-application occlusion on Windows only"; "Every body in `native_window_occlusion_tracker.cc` is wrapped in `#if BUILDFLAG(IS_WIN)`"; "On Linux a Chromium or CEF window covered by another application's window is not marked occluded"; copy: chromium/src 30010bf0…, 2026-09-20
- slice: 9.8
- dates: line last changed 2026-10-17 (c59b6a89); read 2026-09-20; changed-after-read: yes ("no occlusion" became "no cross-application occlusion", and the Steam clause was added)
- verdict: TRACED

### D-F4-46 — how long an idle Matrix client's `/sync` request waits
- source: none tagged (the Matrix spec and matrix-js-sdk)
- repo: docs/workload/measurement-overview.md:51 — "the chat client idles on the Matrix 30 s `/sync` long poll"
- record: 9.8-S2:270 — "`sync.ts:185–190`: … `pollTimeout: 30 * 1000,`" (matrix-js-sdk, the library Element uses); 9.8-S2:254 — "`sync.yaml:107–118`: … name: timeout … example: 30000"; copies: 9.8-S2:251, :267, 2026-09-19
- slice: 9.8
- dates: line last changed 2026-10-17; read 2026-09-19; changed-after-read: no
- verdict: TRACED

### D-F4-47 — what Chromium's `HangWatcher` thread does
- source: none tagged
- repo: dataset/archetypes.yaml:738 — "The entry is majority `HangWatcher`, Chromium's hang-detection thread"
- record: none found. 9.8 changelog.md:222 states it without a source ("`HangWatcher` — Chromium's hang-detection thread, which polls whatever the page does"). A grep of `_dev/research/jioh/*/search` for HangWatcher / hang_watcher finds no Chromium source passage (only a Perfetto trace's metadata in 9.5's S3 record).
- slice: 9.8
- dates: line last changed 2026-10-17; changed-after-read: n/a
- verdict: NO-RECORD
- finding: What the thread does is stated without a read source. Fix: read `base/threading/hang_watcher.h` at the Chrome tag that was measured (152.0.7977.82 or 154.0.8037.57) and record its passage, or reduce the wording to the thread's name.

### D-F4-48 — how Qt Quick's threaded render loop paces frames
- source: none tagged (Qt source)
- repo: dataset/archetypes.yaml:607 — "Venue bound (D24, S8): Qt Quick's render loop paces on a blocking buffer swap; the runner's software rasteriser does not block … (Qt 5.15 qsgthreadedrenderloop.cpp)"
- record: `_dev/research/jioh/task-9.5-interactive-typing/search/S8-display-gpu.md:30` — "`qsgthreadedrenderloop.cpp` … line 878: the render thread ends a frame with `gl->swapBuffers(window)`; lines 803–805: only when nothing changed does it sleep `vsyncDelta - elapsed`"; copy: S8:16 (Qt 5.15 at code.qt.io), searched 2026-09-16
- slice: other (9.5)
- dates: line last changed 2026-10-17 (57342aab); read 2026-09-16; changed-after-read: no (this sentence is unchanged)
- verdict: TRACED (the copy names branch 5.15 and code.qt.io but no commit or file hash, the minimum decision 1 accepts)

### D-F4-49 — the order of the evening arc (browsing → gaming → media playback)
- source: none (design)
- repo: dataset/timelines/coreset/c3-evening.timeline.yaml:1-2 — "C3 — evening arc (building-plan §3 C3): browsing -> gaming (+chat client) -> media playback."; docs/workload/building-plan.md:134 — "No source defines it."; :132 "Each arc's order is design"; :136 "Role (restated 2026-10-11): existence cases — transitions of these shapes, in these orders, occur."
- record: n/a
- dates: c3-evening.timeline.yaml:1 last changed 2026-10-01; building-plan.md:136 changed 2026-10-16
- verdict: LABELLED
- finding (the label is missing in one place and contradicted in another): The c3-evening file carries no design label for its order, while its siblings do (c3-workday.timeline.yaml:2 and c3-creation.timeline.yaml:2, "The order is design"). building-plan.md:136's "transitions of these shapes, in these orders, occur" reads as a claim about real desktops, which no source makes for the evening arc, and it contradicts :132. Fix: add "The order is design; no source defines it." to c3-evening.timeline.yaml's header; reword :136 to "existence cases — the dataset holds transitions of these shapes, in these orders".

### D-F4-50 — the other design labels in the F4 timelines and their variant recipes
- source: none (design)
- repo: c3-workday.timeline.yaml:2 and c3-creation.timeline.yaml:2 ("The order is design"); c1-mail.timeline.yaml:4 ("One send … (design)"); c4.variant.yaml:25 ("the 7z burst's 6 s is design, the injection's size (phase decision 3)"); c5.variant.yaml and c6.variant.yaml (invented tier-4/5 names and spoofs, scenario-catalog.md:36 "design"); the bound-value labels `total_work: design`, `program: design`, `parallelism_cap: design`, `lane_share: design` in the timelines
- record: n/a
- verdict: LABELLED (labels present and honest)

### D-F4-51 — the factors and lengths of the sensitivity variants
- source: none external, except `lavd-ossna24` s14 on chain-x1.2 (F1's id)
- repo: dataset/variants.yaml:42 — "the venue factor's lower edge, 1/1.25 (9.6 D32 …)"; :66 "the C2 pairs' first segment, the one authored length a judging file has (60 s, design, 9.10 D31), halved (9.10 D169)"; :54 "(9.4 D9; lavd-ossna24 s14, about 1.4 on average)"; carried_values :100-137 (each a `meas-ci` half-width with the decision that carried it)
- record: n/a (decision-referenced design values; carried half-widths are `meas-ci`)
- verdict: LABELLED (each set's reason names the decision it comes from; no external source is claimed except chain-x1.2's `lavd-ossna24` s14, left to the gaming fork, F1)


# Part F5 — measurement method, statistics, runner, kernel-name and related-work claims

Scope searched: dataset/archetypes.yaml, sources.yaml, grids.yaml, variants.yaml, timelines/coreset/*, dataset/README.md, docs/workload/*.md, and the docs/references.md entries of the ids found. Not cited anywhere in scope (nothing to inventory): `field-jrssb07`, `dietterich-neco98`, `brodersen-icpr10`, `chicco-bmcg20`, `villamizar-rfc98`, `dinneen-asist21`, `ubuntu-hwe-config`, every `linux-sched-*` but `linux-sched-h`, `man-sched*`, and every "Related work only" id but `liu-jacm73` (SchedCP appears untagged, by name). Runner facts read from our own jobs (CPU model, kernel, nproc, the 40–83 % gate share, the Xeon 8573C ratios) are measurement, not listed.

Record kind: for `maricq-osdi18`, `georges-oopsla07`, `kalibera-ismm13`, `chow-aoms65`, `cochran-st77`, `feller-ipta50` and `fqcodel-rfc18` no slice search record holds the passage; the verbatim passages, locators and copies are held only in their docs/references.md entries, the slice changelogs attesting the reads. The lead's rule, applied to every group (F4's D-F4-33 and D-F4-39 too): a passage held only in the citation index is not a slice read record (the 9.16 spec's decision 1, the claim audit, traces each claim "to a slice's read record"), and nothing shows that read was made without the repository's wording (phase spec decision 1, the verification standard). Those rows are RECORD-BELOW-STANDARD, one shared finding (dataset-findings.md, F-RBS-1).

"changed-after-read": yes only where the claim's own words were written or rewritten after the read; a location first written after the read and not edited since is "no (first written <date>)".

### D-F5-01 — whether machines of one nominal type give different results run to run
- source: `maricq-osdi18` (docs/references.md:122, scholarly)
- repo: docs/workload/measurement-overview.md:73 — "`maricq-osdi18`: servers "with supposedly identical parts" differ run to run."; also measurement-overview.md:172 — "holding one CPU model and reading the repeat count on it"
- record: docs/references.md:124 — "software run repeatedly on the same server (or a different server with supposedly identical parts) can produce performance results that differ with each execution" (abstract); "results in a 2.1–5.9× increase in the recommended number of repetitions" (§5); copy: usenix.org/system/files/osdi18-maricq.pdf, OSDI '18, read 2026-09-19. Read attested by _dev/research/jioh/task-9.6-compile/changelog.md:131 (9.6 D24, "read in full against their primary texts")
- slice: 9.6 (changelog) — TRACED (record = docs/references.md entry)
- dates: line last changed 2026-10-17 (c59b6a8, measured clause only; maricq clause unchanged since 1abb56b 2026-10-01); read 2026-09-19; changed-after-read: no (first written 2026-10-01)
- verdict: RECORD-BELOW-STANDARD (lead's re-verdict from the fork's TRACED: the passage, locator and copy are held only in the docs/references.md entry; finding F-RBS-1)

### D-F5-02 — what interval the paper recommends
- source: `maricq-osdi18` (docs/references.md:122, scholarly)
- repo: docs/workload/measurement-overview.md:79 — "`maricq-osdi18` recommends nonparametric intervals of the median unless normality is shown; the rule's is a t interval."
- record: docs/references.md:124 — "it recommends nonparametric intervals of the median "unless normality can be demonstrated" (§2)"; copy as D-F5-01; also 9.6 changelog:131
- slice: 9.6 — TRACED (record = docs/references.md entry)
- dates: line last changed 2026-10-01; read 2026-09-19; changed-after-read: no
- verdict: RECORD-BELOW-STANDARD (lead's re-verdict from the fork's TRACED: the passage, locator and copy are held only in the docs/references.md entry; finding F-RBS-1)

### D-F5-03 — at which level repetition is done and the interval taken
- source: `kalibera-ismm13` (docs/references.md:117, scholarly)
- repo: measurement-overview.md:74 — "The interval is taken over independent repeats, never over samples within a run. | `kalibera-ismm13` §3, §9.3"; also measurement-overview.md:173 — "repetition at the highest level of variation, the t interval over repeats"
- record: docs/references.md:119 — repetition "must be done at the highest level that has random variation to avoid bias" (§3); a t interval "with ν = rₙ − 1 degrees of freedom" (§9.3, Eq. 4); copy: kar.kent.ac.uk/33611/45/p63-kaliber.pdf (author's accepted manuscript), read 2026-09-19; 9.6 changelog:131 (D24)
- slice: 9.6 — TRACED (record = docs/references.md entry)
- dates: line last changed 2026-10-01; read 2026-09-19; changed-after-read: no
- verdict: RECORD-BELOW-STANDARD (lead's re-verdict from the fork's TRACED: the passage, locator and copy are held only in the docs/references.md entry; finding F-RBS-1)

### D-F5-04 — whether the count is set on-line, and the smallest count
- source: `kalibera-ismm13` (docs/references.md:117, scholarly)
- repo: measurement-overview.md:76 — "At least five repeats. Repeats are added one at a time … until every value holds. … | `kalibera-ismm13` §11"; also measurement-overview.md:173 — "on-line stopping, the minimum of five"
- record: _dev/research/jioh/task-9.6-compile/campaign/method.md:71 — `kalibera-ismm13` §11: "We do not show counts of fewer than 5 executions as they could hardly be used to get the variance estimate right"; docs/references.md:119 — count "can be established on-line, by adding repetitions until the confidence interval is sufficiently narrow" (§11); copy as D-F5-03
- slice: 9.6
- dates: line last changed 2026-10-01; read 2026-09-19; changed-after-read: no
- verdict: RECORD-BELOW-STANDARD (lead's re-verdict from the fork's TRACED: the passage, locator and copy are held only in the docs/references.md entry; finding F-RBS-1)

### D-F5-05 — the paper's construction: interval over runs, runs added to a precision
- source: `georges-oopsla07` (docs/references.md:112, scholarly)
- repo: measurement-overview.md:174 — "the same construction: an interval over independent runs, runs added until a set precision"
- record: docs/references.md:114 — "If the confidence interval achieves a desired level of precision, i.e., the confidence interval is within 1% or 2% of the sample mean, the script stops the experiment" (§4.3); independence across invocations (§4.2); copy: dri.es/files/oopsla07-georges.pdf, read 2026-09-19; _dev/research/jioh/task-9.5-interactive-typing/changelog.md:204 (9.5 D33, quoting §4.3, "author copy, dri.es, p. 10 of 20, read in full 2026-09-19")
- slice: 9.5 / 9.6 — TRACED (record = docs/references.md entry)
- dates: line last changed 2026-10-01; read 2026-09-19; changed-after-read: no
- verdict: RECORD-BELOW-STANDARD (lead's re-verdict from the fork's TRACED: the passage, locator and copy are held only in the docs/references.md entry; finding F-RBS-1)

### D-F5-06 — whether the stopping rule has a ceiling (the row's ground column)
- source: `georges-oopsla07`, `kalibera-ismm13`
- repo: measurement-overview.md:76 — "Minimum and stopping | At least five repeats. … until every value holds. No ceiling. | `kalibera-ismm13` §11; `georges-oopsla07` §4"
- record: _dev/research/jioh/task-9.5-interactive-typing/changelog.md:204 (9.5 D33, "no ceiling on repeats") — "`kalibera-ismm13` §11 sets none … `georges-oopsla07` §4.3 stops after "a preset number of runs, e.g., 30 runs""; docs/references.md:114 — georges' "stopping rule has a cap of about thirty runs"
- slice: 9.5
- dates: line last changed 2026-10-01; read 2026-09-19; changed-after-read: no
- verdict: WORDING-OUTSIDE-PASSAGE
- finding: the row's ground column names `georges-oopsla07` §4 beside "No ceiling", while §4.3 stops at a preset count (e.g. 30); no ceiling is the project's (9.5 D33). Fix: "No ceiling (9.5 D33; `georges-oopsla07` §4.3 caps at a preset count)" or move georges to the "added until a set precision" clause only.

### D-F5-07 — the half-width of a count-weighted mean over repeats
- source: `cochran-st77` (docs/references.md:132, scholarly)
- repo: measurement-overview.md:75 — "The table's half-width is the ratio estimator's (`cochran-st77`)."; also measurement-overview.md:175 — "the half-width of a count-weighted table mean (the ratio estimator)"
- record: docs/references.md:134 — the cluster mean "a ratio estimate in which Mᵢ is taken as the auxiliary variate xᵢ", variance "By theorem 6.1, assuming that the number of clusters in the sample is large" (§9A.1, p. 250), v₂(R̂) (6.13) (§6.4, p. 155); copy: archive.org/details/in.ernet.dli.2015.121816 (Wiley Eastern reprint, 3rd ed.), read 2026-09-26; _dev/research/jioh/task-9.5-interactive-typing/changelog.md:539 (9.5 D78)
- slice: 9.5 — TRACED (record = docs/references.md entry)
- dates: line last changed 2026-10-01; read 2026-09-26; changed-after-read: no
- verdict: RECORD-BELOW-STANDARD (lead's re-verdict from the fork's TRACED: the passage, locator and copy are held only in the docs/references.md entry; finding F-RBS-1)

### D-F5-08 — the ratio variance as a large-sample result
- source: `cochran-st77` (docs/references.md:132, scholarly)
- repo: measurement-overview.md:79 — "`cochran-st77`'s ratio variance is a large-sample result, and the campaigns' counts are 5 to 77."
- record: docs/references.md:134 — "the large-sample results may be used if the sample size exceeds 30 and is also large enough so that the coefficients of variation of x̄ and ȳ are both less than 10%" (§6.3, p. 153); copy as D-F5-07
- slice: 9.5 — TRACED (record = docs/references.md entry)
- dates: line last changed 2026-10-01; read 2026-09-26; changed-after-read: no
- verdict: RECORD-BELOW-STANDARD (lead's re-verdict from the fork's TRACED: the passage, locator and copy are held only in the docs/references.md entry; finding F-RBS-1)

### D-F5-09 — what stopping at the first passing count guarantees
- source: `chow-aoms65` (docs/references.md:127, scholarly)
- repo: measurement-overview.md:77 — "`chow-aoms65`: first-crossing coverage reaches the nominal level only asymptotically, with a lower bound near .929"; also measurement-overview.md:176 — "what stopping at the first passing count guarantees"
- record: docs/references.md:129 — (5) "lim_{d→0} P(μ ε I_N) = α"; Starr's numerical results "for α = .95 the lower bound for all d > 0 of P(…), where N is the smallest odd integer k ≥ 3 …, is about .929 if the values a_k are taken from the t-distribution" (p. 461), "the normal population"; copy: DOI 10.1214/aoms/1177700156 (Project Euclid, JSTOR scan), read 2026-09-25; _dev/research/jioh/measurement-campaign-workflow.md:27 — "at finite counts the normal case with a t rule has a coverage lower bound of "about .929""; 9.8 changelog:575 (9.8 D28)
- slice: 9.8 — TRACED (record = docs/references.md entry)
- dates: line last changed 2026-10-01; read 2026-09-25; changed-after-read: no
- verdict: WORDING-OUTSIDE-PASSAGE (its record is also held only in the docs/references.md entry, F-RBS-1)
- finding: the .929 bound is Starr's computation for a normal population with a t rule and odd k ≥ 3, reported by Chow and Robbins; measurement-overview.md:77 states it unqualified (and the campaigns' run means are not normal, docs/references.md:129). Fix: "… with a lower bound near .929 in the normal case with a t rule (Starr's computations, p. 461)".

### D-F5-10 — the standard error of a compiled wake count
- source: `feller-ipta50` (docs/references.md:137, scholarly)
- repo: measurement-overview.md:106 — "within 5 % or four standard errors of the count (`feller-ipta50`)"; also measurement-overview.md:177 — "the standard error of a compiled wake count"
- record: docs/references.md:139 — §12.4 theorem, N_r "asymptotically normally distributed", reduced variable (N_r − r/μ)/(σr^½μ^−3/2) (p. 248–249); copy: archive.org/details/dli.ernet.5666 (second printing), read 2026-09-27; _dev/research/jioh/task-9.5-interactive-typing/changelog.md:673 (9.5 D86)
- slice: 9.5 — TRACED (record = docs/references.md entry)
- dates: line last changed 2026-10-17 (c59b6a8; the feller clause unchanged since 2026-10-01); read 2026-09-27; changed-after-read: no
- verdict: RECORD-BELOW-STANDARD (lead's re-verdict from the fork's TRACED: the passage, locator and copy are held only in the docs/references.md entry; finding F-RBS-1)

### D-F5-11 — the compile-fidelity tolerances
- source: none (values no source states)
- repo: measurement-overview.md:106 — "each component's gap table implies its measured wake rate within 2 %, and … compiles at the wake rate it carries, within 5 % or four standard errors of the count (`feller-ipta50`)"
- record: 9.5 changelog:675 (D86) — "the test's tolerance unchanged"; feller grounds the standard error only (docs/references.md:139)
- slice: 9.5
- dates: line last changed 2026-10-17 (clause unchanged since 2026-10-01); changed-after-read: n/a
- verdict: LABELLED
- finding: label missing — 2 %, 5 % and four standard errors are the project's test tolerances, unlabelled, with the `feller-ipta50` tag beside "four standard errors". Fix: "within 2 %, and … within 5 % or four standard errors of the count (tolerances ours; the standard error `feller-ipta50`'s)".

### D-F5-12 — the stability tolerance and floor as the project's rule
- source: none (convention)
- repo: measurement-overview.md:75 — "5 % is design: half the smallest effect reported as a comparison of carried values (the kernel build's 10 % between `-j8` and `-j1`). 1 µs is the trace's resolution."; also dataset/sources.yaml:219-221 (`meas-ci` notes, "Our CI measurement campaigns … within 5 % of it or 1 us, over at least five same-machine repeats"); docs/workload/building-plan.md:254
- record: _dev/research/jioh/task-9.6-compile/campaign/method.md:69 — "the larger of 5 % of the mean (D10) and 1 µs, the trace's resolution (`perf sched timehist` times in whole microseconds)"; method.md:66 — "The tolerance is half the smallest systematic effect this campaign reports, the 10 % `-j8` against `-j1` difference (D4)"; docs/references.md:119 — "the campaigns' 5 % is the project's own"
- slice: 9.6
- dates: measurement-overview.md:75 2026-10-01; sources.yaml:219 2026-09-22; changed-after-read: n/a
- verdict: LABELLED (label present and honest in measurement-overview.md:75; sources.yaml and building-plan.md:254 state it as the campaigns' own rule)

### D-F5-13 — a periodic job's deadline at its next request
- source: `liu-jacm73` (docs/references.md:877, related work only; cited in prose, not as a registry tag)
- repo: dataset/archetypes.yaml:632 — "its deadline is the next cycle's start (period-implicit, liu-jacm73 (A2))"; same at archetypes.yaml:657, :682; measurement-overview.md:178 — "the periodic jobs' deadline at the next period's start"
- record: _dev/research/jioh/task-9.12-related-work-prose/search/S1-literature.md:237 — "(A2) Deadlines consist of run-ability constraints only--i.e, each task must be completed before the next request for it occurs." (PDF p.3 / printed p.48); copy: cs.ru.nl/~hooman/DES/liu-layland.pdf, SHA-256 de9fb725…, read 2026-10-07 (:234)
- slice: other (9.12)
- dates: archetypes.yaml:632 clause first written 2026-09-26 (cc51eb8), line last changed 2026-09-28; measurement-overview.md:178 2026-10-01; read 2026-10-07; changed-after-read: no (the record post-dates the wording)
- verdict: TRACED

### D-F5-14 — what the RFC grounds for the download's queue
- source: `fqcodel-rfc18` (docs/references.md:142, scholarly)
- repo: measurement-overview.md:52 — "a link shaped to 121.0 Mbps … with an `fq_codel` queue (`fqcodel-rfc18`)"; measurement-overview.md:197 — "`steam-download-stats`, `fqcodel-rfc18` | the download's link rate and why its queue is `fq_codel`"
- record: docs/references.md:144 — abstract: "a powerful tool for fighting bufferbloat and reducing latency"; "provides isolation for low-rate traffic …"; role: "why an active queue management leaf is the candidate tried … the claim it supports is that flow isolation and queue-length control are what this discipline is for, which is why it is the arm tested"; copy: rfc-editor.org/rfc/rfc8290.txt, RFC 8290 (Experimental), read 2026-09-20; _dev/research/jioh/task-9.7-background-io/campaign/method.md:92 ("cited for the discipline's stated purpose only"); the adoption: 9.7 changelog:131-135 (9.7 D25, the coefficient-of-variation test)
- slice: 9.7 — record = docs/references.md entry
- dates: both lines first written 2026-10-01 (1abb56b); read 2026-09-20; changed-after-read: no
- verdict: WORDING-OUTSIDE-PASSAGE (measurement-overview.md:197 only; :52 TRACED) (its record is also held only in the docs/references.md entry, F-RBS-1)
- finding: ":197 "why its queue is `fq_codel`" makes the RFC the reason for the choice; the RFC states the discipline's purpose and grounds why it was the arm tried, the adoption resting on 9.7 D25's test. Fix: "why `fq_codel` was the queue tried (its adoption: 9.7 D25)".

### D-F5-15 — how long GitHub keeps a workflow's artifacts
- source: `gh-artifact-retention` (docs/references.md:379, deployed-system)
- repo: measurement-overview.md:42 — "before GitHub deletes a workflow's artifacts after 90 days (`gh-artifact-retention`)"; also measurement-overview.md:179; docs/workload/building-plan.md:250 — "before the 90 days after which a workflow's artifacts are deleted"; dataset/README.md:219 — "before GitHub deletes a workflow's artifacts at 90 days"
- record: _dev/research/jioh/task-9.15-docs-memos-and-guidebook-corrections/logs/K01.md:89 — "By default, checks, workflow runs, commit statuses, and the artifacts and log files generated by workflows are retained for 90 days before they are automatically deleted."; copy: docs.github.com/api/article/body?pathname=…/managing-github-actions-settings-for-a-repository, SHA-256 3708ce22…, read 2026-10-16
- slice: other (9.15)
- dates: lines first written 2026-10-16/17; read 2026-10-16; changed-after-read: no
- verdict: TRACED

### D-F5-16 — the standard Linux runner's CPU count and storage
- source: `gh-hosted-runners` (docs/references.md:369, deployed-system)
- repo: dataset/README.md:175 — "On the standard Linux runner (4 vCPU; `gh-hosted-runners` …) … The two ceilings are the runner's 14 GB of storage (`gh-hosted-runners`)"
- record: _dev/research/jioh/task-9.10-scenarios-timelines/search/S4-ci-observability.md:225-231 — `github-hosted-runners.md` lines 48–60, "Linux / 4 / 16 GB / 14 GB" in the public-repository table (:221, line 24 "For public repositories …"); copy: docs.github.com/en/actions/reference/runners/github-hosted-runners, SHA-256 2537c22a… (md), read 2026-10-01 (:204, :3)
- slice: 9.10
- dates: 14 GB clause first written 2026-10-13 (d4b5acc), line last changed 2026-10-16; read 2026-10-01; changed-after-read: no
- verdict: TRACED

### D-F5-17 — the job execution-time limit
- source: `gh-actions-limits` (docs/references.md:374, deployed-system)
- repo: dataset/README.md:175 — "the 6 h a job may run before it is terminated (`gh-actions-limits`)"
- record: _dev/research/jioh/task-9.10-scenarios-timelines/search/S4-ci-observability.md:278 — "Each job in a workflow can run for up to 6 hours of execution time. If a job reaches this limit, the job is terminated and fails."; copy: actions-limits.md, SHA-256 6041828e…, read 2026-10-01
- slice: 9.10
- dates: first written 2026-10-16 (18127cc); read 2026-10-01 (re-fetched byte-identical 2026-10-16, 9.15 K01.md:88); changed-after-read: no
- verdict: TRACED

### D-F5-18 — the kernel's task-name buffer length at v6.17
- source: `linux-sched-h` (docs/references.md:384, deployed-system)
- repo: dataset/sources.yaml:233-234 — "include/linux/sched.h at v6.17: `TASK_COMM_LEN = 16`"; also dataset/grids.yaml:30-31 — "TASK_COMM_LEN is 16 bytes including the terminating NUL (`include/linux/sched.h`)"
- record: _dev/research/jioh/task-9.10-scenarios-timelines/search/S4-ci-observability.md:1499-1500 — `sources/S4-09/v6.17__include_linux_sched.h` line 320: "TASK_COMM_LEN = 16,"; copy written 2026-10-01 (record header :3)
- slice: 9.10
- dates: first written 2026-10-12 (021ca12); read 2026-10-01; changed-after-read: no
- verdict: TRACED — duplicate of D-F1-48 (the same claim, found by two groups); counted there, not here

### D-F5-19 — the name NUL-terminated and padded, so at most 15 characters, at v6.17
- source: `linux-sched-h` (docs/references.md:384, deployed-system)
- repo: dataset/sources.yaml:233-234 — "at v6.17: … the comm field NUL-terminated and zero-padded, so a process name is at most 15 characters"; also grids.yaml:30-32 ("so 15 characters"); dataset/README.md:152, building-plan.md:150 ("the kernel's 15-character `comm` field"), scenario-catalog.md:36 ("fails a name over 15 bytes")
- record: _dev/research/jioh/task-9.10-scenarios-timelines/search/S2-project-docs.md:1786-1787 — "strscpy_pad() to ensure it is always NUL-terminated and zero-padded" — v7.0 sched.h:1160–1169; :1750 v6.8 exec.c `strscpy_pad(tsk->comm, buf, sizeof(tsk->comm));`; copy: raw.githubusercontent.com/torvalds/linux/<tag>/…, read 2026-10-01
- slice: 9.10
- dates: first written 2026-10-12; read 2026-10-01; changed-after-read: no
- verdict: RECORD-BELOW-STANDARD — the same root as D-F1-49 (no record of the v6.17 comment passage); counted there, not here, one finding
- finding: the repo pins the padding clause to v6.17; the records quote it at v7.0 and v6.8 only (9.10's local v6.17 copy holds the same comment at sched.h:1160–1161, unquoted). Fix: record the v6.17 passage sched.h:1160–1161 (the 9.16 claims record can carry it), or cite the clause to v6.8/v7.0.

### D-F5-20 — how a process's `comm` is derived (basename cut, scripts, renames)
- source: Linux kernel source (no id; 9.10 D25 rule)
- repo: docs/workload/scenario-catalog.md:36 — "its process's kernel `comm` — the exec'd basename cut to 15 bytes, a script its own name, a `prctl` rename its new name"
- record: _dev/research/jioh/task-9.10-scenarios-timelines/search/S2-project-docs.md:1719-1800 (S2-11) — v6.8 exec.c:1380 "__set_task_comm(me, kbasename(bprm->filename), true);", v6.8 binfmt_script.c:121–136, sys.c:2504–2511; copy: raw.githubusercontent.com/torvalds/linux/<tag>/…, read 2026-10-01
- slice: 9.10
- dates: first written 2026-10-16 (34b0935); read 2026-10-01; changed-after-read: no
- verdict: TRACED

### D-F5-21 — Ubuntu 24.04's desktop kernel transparent-hugepage default
- source: Ubuntu kernel package (no id in the doc)
- repo: measurement-overview.md:209 — "Ubuntu 24.04's desktop kernel defaults to `madvise`"; also dataset/archetypes.yaml:929, :942, :1638 ("the desktop kernel's default is `madvise`")
- record: _dev/research/jioh/task-9.10-scenarios-timelines/search/S2-project-docs.md:3834-3838 (S2-50) — `config:1288–1291` "# CONFIG_TRANSPARENT_HUGEPAGE_ALWAYS is not set / CONFIG_TRANSPARENT_HUGEPAGE_MADVISE=y"; copy: snapshot.ubuntu.com/…/linux-buildinfo-7.0.0-31-generic_7.0.0-31.31~24.04.1_amd64.deb, read 2026-10-03
- slice: 9.10
- dates: measurement-overview.md:209 first written 2026-10-17 (c59b6a8); read 2026-10-03; changed-after-read: no
- verdict: TRACED

### D-F5-22 — SchedCP's kernel-compilation workload and its reported gain
- source: SchedCP (`schedcp-mlsys25`, docs/references.md:816, related work only; untagged in the doc)
- repo: docs/workload/grounding-sources.md:32 — "A compile workload SchedCP's evaluation uses (kernel compilation, "make -j 172" on 6.14 tinyconfig, 1.79× over EEVDF)"
- record: _dev/research/jioh/2026-09-13-verification/reads/R03-build-papers.md:149 — "For kernel compilation (tinyconfig, "make -j 172" on 6.14 source), SchedCP achieves … reaching 1.79× total improvement over EEVDF (Figure 2a)." (v4 §5 p. 4); copy: arxiv.org/pdf/2509.01245v4, SHA-256 cce49d3c…, read 2026-09-13 (:21); also task-9.6-compile/search/S1-literature.md:151 (read 2026-09-16)
- slice: other (2026-09-13 verification) and 9.6
- dates: rewritten 2026-10-17 (c59b6a8, from "The de facto standard compile workload in every scheduler evaluation"); read 2026-09-13; changed-after-read: yes (c59b6a8)
- verdict: TRACED

### D-F5-23 — where SchedCP's "short-lived processes" comes from
- source: SchedCP (related work only; untagged)
- repo: grounding-sources.md:32 — "SchedCP's "short-lived processes" is its Observation Agent's generated profile text"
- record: R03-build-papers.md:159 — v4 §4, p. 4: "For kernel compilation, it produces profiles like "CPU-intensive parallel compilation with short-lived processes, inter-process dependencies, targeting makespan minimization.""; copy as D-F5-22
- slice: other (2026-09-13 verification)
- dates: added 2026-10-17 (c59b6a8); read 2026-09-13; changed-after-read: yes (c59b6a8)
- verdict: TRACED

### D-F5-24 — that SchedCP cites schbench, and how
- source: SchedCP (related work only; untagged)
- repo: grounding-sources.md:28 — "a citation precedent (SchedCP cites it)"; source-vetting.md:14 — "SchedCP … cites schbench by git URL"; source-vetting.md:87 — "schbench: cited by SchedCP (MLforSystems @ NeurIPS 2025) by git URL — confirmed"; correction source-vetting.md:141 — "SchedCP cites schbench at kernel.googlesource.com, not by its GitHub URL"
- record: R03-build-papers.md:218 — "[12] Chris Mason. schbench: Scheduler benchmark. https://kernel.googlesource.com/pub/scm/linux/kernel/git/mason/schbench, 2016." (v4 p. 5); copy as D-F5-22
- slice: other (2026-09-13 verification)
- dates: grounding-sources.md:28 clause added 2026-10-17 (c59b6a8); source-vetting.md:14, :87 written 2026-08-25 (before the read); read 2026-09-13; changed-after-read: yes (grounding-sources.md:28, c59b6a8); no (source-vetting)
- verdict: TRACED

### D-F5-25 — SchedCP's venue
- source: SchedCP (related work only; untagged)
- repo: source-vetting.md:14 — "SchedCP (arXiv 2509.01245, MLforSystems @ NeurIPS 2025)"; source-vetting.md:87
- record: R03-build-papers.md:224-226 — OpenReview "venue":{"value":"MLForSys2025"}, "NeurIPS.cc/2025/Workshop/MLForSys"; arXiv journal-ref "MLforSystem 2025"; read 2026-09-13
- slice: other (2026-09-13 verification)
- dates: written 2026-08-25; read 2026-09-13; changed-after-read: no
- verdict: TRACED

### D-F5-26 — what SchedCP says about the completeness of its benchmark
- source: SchedCP (related work only; untagged)
- repo: grounding-sources.md:64 — "(SchedCP's own evaluation notes that a complete benchmark remains future work)"
- record: R03-build-papers.md:236-238 — "All experiments successfully created working custom scheduler configurations or eBPF programs. Future evaluation requires a complete benchmark." (v4 §5, p. 4; v3/v4 only); copy as D-F5-22
- slice: other (2026-09-13 verification)
- dates: line last changed 2026-10-17 (c59b6a8 removed the neighbouring clause "which no prior work in the LLM-scheduling line has done"; the SchedCP clause unchanged); read 2026-09-13; changed-after-read: no
- verdict: TRACED


# Part X — the lead's own rows: the negative-result table in docs/workload/grounding-sources.md, which no source group covered

### D-X-01 — what enterprise, VDI and cloud workload traces record about processes
- source: none tagged (Azure traces, Google cluster traces, "VDI characterization studies", named in the row)
- repo: docs/workload/grounding-sources.md:59 — "Enterprise / VDI / cloud workload traces (Azure, Google cluster traces, VDI characterization studies) | Server/VM granularity; no consumer applications; process identity absent or hashed"
- record: none found for the claim. The one read of these traces, `_dev/research/jioh/task-9.12-related-work-prose/search/S3-traces-datasets.md:327-336` (S3-08, Google 2011/2019 and Alibaba schemas, read 2026-10-07), checks only for a context-switch field ("None of the schemas has a context-switch count or a scheduling-latency field", :336) and quotes no passage on task or process identity. No record names an Azure trace or a VDI characterization study (grep of `_dev/research/jioh/*/search` and the 2026-09-13 reads for "Azure", "VDI"; 9.10 S1-literature.md:1849 mentions VDI benchmarks only as "reportedly" including virus scan and 7-Zip).
- slice: none
- dates: line last changed 2026-08-25 (9313c284, under the doc's earlier name); no read; changed-after-read: n/a
- verdict: NO-RECORD
- finding: the row states what three trace families record with no read behind it. Fix: quote the Google schema's identity fields from the S3-08 copy (`sources/S3-08/`) and cite S3-08, and drop Azure and VDI or mark them "unsourced", as the row two lines below does.

### D-X-02 — what older desktop trace studies released
- source: none (labelled "unsourced: no study is named")
- repo: docs/workload/grounding-sources.md:61 — "Desktop trace studies (older workload characterization literature) | Aggregate statistics survive; raw timelines with names were never released, largely for privacy (unsourced: no study is named)"
- record: n/a
- slice: none
- dates: line last changed 2026-10-17; changed-after-read: n/a
- verdict: LABELLED
- finding: the label is present, but it labels a statement of fact about a body of literature ("never released, largely for privacy"), not a value of convention, arithmetic, placeholder or design, which are the kinds phase spec decision 1 (the verification standard) allows an unsourced value. Fix: reword as the project's reading — "no raw timeline with names was found in the studies searched" — with the search it rests on (9.10 S3, 9.12 S3), or drop the cause "largely for privacy".
