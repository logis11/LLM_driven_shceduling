# 9.16 claim audit — dataset side: findings

Every claim of `dataset-inventory.md` whose verdict is not TRACED, and every LABELLED claim whose label is missing, inconsistent or of a kind phase spec decision 1 (the verification standard) does not allow. 43 claims, in 34 findings. Each gives the location, what the repository says, what the record says (the passage is quoted in full in the claim's inventory row), and a proposed fix. Fixes are proposals for the lead; none is applied. Record shorthands are those of the inventory's part headers. R02, R03, R05, R07 and R10 are the 2026-09-13 verification reads under `_dev/research/jioh/2026-09-13-verification/reads/`.

## Wording outside the passage (19 claims)

**D-F1-12 — the LAVD deck and the 1.5 ms slice.**
- Location: `dataset/archetypes.yaml:1791-1792`.
- Repo: "the deck's slice example 1.5 ms".
- Record: R02:91-96. Slide 27 of Min's OSS NA 2024 deck gives only "a targeted latency (e.g., 15 msec)". The 15 ms shared by 10 tasks is a comment in scx's `main.bpf.c`, marked in R02 as "(not the talk)".
- Fix: "scx_lavd's source-comment example, 15 ms shared by 10 tasks (`scx`)", or drop the comparison.

**D-F1-14 — the six `Troy.exe` chain members under the slide-16 tag.**
- Location: `member_names` with `source: lavd-ossna24:s16` in all eight gaming files (c1-gaming:20-21, c2-p2a:30-31, c2-p2a-idle:55, c2-p2b:54, c3-evening:37-38, c4-gaming:47, c6-dual:24-25, c7-gaming:48). Also `docs/workload/coreset-guide.md:252` and `scenario-catalog.md:36`.
- Repo: all 15 names are attributed to slide 16.
- Record: 9.4-S2:91. Slide 16 shows one `Troy.exe` node. The six repeats come from 9.10 decision D26 (the scenarios slice's rule that a Wine thread without its own name keeps its process's `comm`; 9.10-CL:558), which no dataset file states.
- Fix: one sentence in `game-task-chain`'s `modeling_notes` and at coreset-guide.md:252 saying that six members carry the process name `Troy.exe` by that rule, which is ours.

**D-F1-19 — the tool behind the LAVD deck's traces.**
- Location: `dataset/archetypes.yaml:1756-1757`; `coreset-guide.md:242`.
- Repo: the deck's traces were "collected with perf sched record".
- Record: 9.4-S1:53. The 2024 deck says only "We collect and analyze all scheduling activities while playing games". The tool is named in Min's LPC 2025 slides and the VaporMark README (9.4-S2:118, :145-153). Neither has a registry entry. Linking them to the 2024 deck is 9.4 decision D1 (the gaming slice's reading).
- Fix: "collected, by 9.4 D1's reading of Min's LPC 2025 slides, with `perf sched record`", or cite that source.

**D-F1-22 — Proton and the Steam client.**
- Location: `dataset/archetypes.yaml:1750-1754`.
- Repo: "Proton runs only under the Steam client".
- Record: 9.4-S4:262-263. The Proton README says "Proton is a tool for use with the Steam client" and "Most users should use Proton provided by the Steam Client itself". It documents no standalone path, and it does not say "only".
- Fix: "Proton is documented only as a tool for use with the Steam client".

**D-F1-27 — the FAQ that holds Steam's per-game download setting.**
- Location: `docs/references.md:295`; `dataset/sources.yaml:142`.
- Repo: the per-game setting is attributed to FAQ 4F9E-6328-E9B8-47F9 ("the article leaves unnamed").
- Record: R07:161-169 and 9.10-S2:2924-2936. The sentence "There's also a per-game setting to allow/prevent the downloading of other updates while you're playing" is in FAQ 71AB-698D-57EB-178C. R07:167 says "The 4F9E article does not mention a per-game setting."
- Fix: give the per-game setting its FAQ 71AB-698D-57EB-178C locator at both places.

**D-F1-46 — the flap-stress intervals called "debounce" values.**
- Location: `dataset/grids.yaml:56-60`, `dataset/README.md:150`, `docs/workload/building-plan.md:185`, `coreset-guide.md:588`.
- Repo: 5, 10 and 30 s are "the debounce values" of GameMode, tuned and systemd-oomd.
- Record: 9.19-P:17-19 (the 9.19 changelog's precedent search). The three passages say different things:
  - GameMode "will check every 5 seconds", a check interval.
  - tuned has an "Update interval for dynamic tunings", and `dynamic_tuning = 0` ships off.
  - systemd-oomd's figure is "the amount of time … needs to have exceeded memory pressure limits", a sustain duration.
- Fix: use `dataset/sources.yaml`'s words at the four places: GameMode's check interval, tuned's update interval (dynamic tuning off by default), systemd-oomd's sustain duration.

**D-F2-04 — the SWELL-KW blocks of the Outlook stream.**
- Location: `dataset/sources.yaml:48-50`.
- Repo: `outlook-c23` covers "interruption conditions".
- Record: 910S3:234 and R10:232. SWELL-KW's conditions are neutral, e-mail interruptions and time pressure. `c` is the block number. Block 1 is always neutral; blocks 2 and 3 are one interruption block and one time-pressure block, in counterbalanced order. 9.5 decision D12 carries the same slip.
- Fix: "outlook-c23 (Outlook, blocks 2 and 3 — the e-mail-interruption and time-pressure conditions, in counterbalanced order; no block-1 keystrokes)".

**D-F2-12 — González and Mark's population.**
- Location: `dataset/sources.yaml:169`.
- Repo: "14 shadowed knowledge workers".
- Record: R10:101, :103. The paper calls them "information workers", N = 14, as `grounding-sources.md:40` already says.
- Fix: "information workers".

**D-F2-29 — interbench's loads as the source-vetting body lists them.**
- Location: `docs/workload/source-vetting.md:52`. This body line is left standing by the 2026-10-17 correction.
- Repo: Write and Read use a "RAM-sized file"; Hack is "hackbench 50"; no Ring load is listed.
- Record: R01:150, :170, :197-231. At the pinned master `e612a65`, Write and Read cap their file at about 1 GB, Hack never runs, and an undocumented Ring load exists. The man page and tag v0.31 describe the older behaviour.
- Fix: extend the correction's line-52 item to say this.

**D-F3-02 — what O'Callahan et al.'s process count grounds.**
- Location: `dataset/sources.yaml:87-88`, `docs/references.md:84`, `building-plan.md:101`. `dataset/archetypes.yaml:1034` says the same in other words.
- Repo: grounds "the existence and short-lived character of compiler children".
- Record: R03-build-papers.md:50, :62. The paper counts every process a DynamoRio `make -j8` forks and execs, and it says nothing of what they run. 9.6 decision D2 (task-9.6-compile/changelog.md:13) removed "compiler children" for this reason.
- Fix: "grounds only that a parallel `make` build forks and execs many processes, mostly short-lived (a DynamoRio build; the paper does not say what they run)".

**D-F3-04 — the reach of Coetzee et al.'s corroboration.**
- Location: `docs/references.md:89`.
- Repo: "builds spawn many short-lived processes".
- Record: R03-build-papers.md:104, :120. The passage names "the Linux kernel build's" processes only.
- Fix: "the Linux kernel build spawns many short-lived processes".

**D-F3-07 — the build tools' documented default parallelism.**
- Location: `docs/workload/measurement-overview.md:52`.
- Repo: "the build tools' documented defaults follow `nproc`".
- Record: task-9.6-compile/search/S2-project-docs.md:407, the GNU make 4.4.1 manual: "make will execute only one recipe at a time". 9.6 decision D4 records "make 1". Only DKMS's NVIDIA build reads `nproc`.
- Fix: "`-j8`, the `nproc` rule applied to an eight-thread desktop (9.6 D4; DKMS reads `nproc`, GNU make defaults to one job)".

**D-F4-15 — PCMark 10's video playback.**
- Location: `docs/workload/scenario-catalog.md:33`; `docs/references.md:224`.
- Repo: video playback is one of PCMark 10's "groups".
- Record: R05:66, :110. Battery Life is a separate profile, not a test group, and video is a scenario inside it.
- Fix: "its Battery Life profile's Video scenario" at both places.

**D-F4-21 — two SYSmark 30 facts cited to the user guide.**
- Location: `building-plan.md:135`, `c3-creation.timeline.yaml:2-3`, `scenario-catalog.md:15`, `:33`.
- Repo: two facts are given as `sysmark30`'s, and that entry cites the User Guide only:
  - SYSmark 30 runs photo editing "beside a background encode".
  - SYSmark 30 "keeps Outlook open".
- Record: R05:206 and R05:229. Both passages are in BAPCo's separate whitepaper v1.2 (PDF pp. 10-11). The guide says only that the workload "switches between photo editing and video editing" (R05:209).
- Fix: add the whitepaper v1.2 to the `sysmark30` cite with its locators, or give it its own entry.

**D-F4-26 — the number of Procyon's local-AI benchmarks.**
- Location: `docs/workload/grounding-sources.md:16`; `docs/references.md:239`.
- Repo: "three of them local-AI inference".
- Record: R05:414-421. Four are built around on-device AI inference, including AI Inference for Android.
- Fix: "four of them on-device AI inference (…, and inference on Android)", or "three desktop ones, beside one for Android".

**D-F4-31 — what the GLAM tab probe counts.**
- Location: `docs/workload/coreset-guide.md:197`.
- Repo: "창당 탭 다섯" (five tabs per window).
- Record: 9.10-S3:639-640. The probe counts tabs "across all windows". The single window is a separate probe, composed by 9.10 decision D16.
- Fix: "탭 다섯과 창 하나(`glam`)" (five tabs and one window), as `building-plan.md:116` states it.

**D-F5-06 — the "No ceiling" row of the stopping rule.**
- Location: `docs/workload/measurement-overview.md:76`.
- Repo: "No ceiling", with the ground column citing `kalibera-ismm13` §11 and `georges-oopsla07` §4.
- Record: task-9.5-interactive-typing/changelog.md:204 (9.5 decision D33). Georges §4.3 stops after "a preset number of runs, e.g., 30 runs". No ceiling is the project's own decision, D33.
- Fix: "No ceiling (9.5 D33)", and cite georges only for "runs added until a set precision".

**D-F5-09 — the .929 coverage bound.**
- Location: `docs/workload/measurement-overview.md:77`.
- Repo: the bound is stated without qualification.
- Record: docs/references.md:129 (see also F-RBS-1). The figure is Starr's computation, reported by Chow and Robbins on p. 461, for a normal population with a t rule.
- Fix: add "in the normal case with a t rule (Starr's computations, p. 461)".

**D-F5-14 — what the fq_codel RFC grounds.**
- Location: `docs/workload/measurement-overview.md:197`.
- Repo: the RFC explains "why its queue is `fq_codel`".
- Record: docs/references.md:144 (see also F-RBS-1). The RFC states what the discipline is for, which is why it was the option tried. The adoption rests on 9.7 decision D25's test.
- Fix: "why `fq_codel` was the queue tried (its adoption: 9.7 D25)".

## Record below the standard (15 claims)

**F-RBS-1 — passages held only in the citation index (10 claims).**
- Claims:
  - D-F5-01, -02: `maricq-osdi18`.
  - D-F5-03, -04: `kalibera-ismm13`.
  - D-F5-05: `georges-oopsla07`.
  - D-F5-07, -08: `cochran-st77`.
  - D-F5-10: `feller-ipta50`.
  - D-F4-33: `glean`, the `glean.mps` 04:00 thread.
  - D-F4-39: `systemd-ubuntu`, `netplan` and `livecd-rootfs`, on why a stock Ubuntu 24.04 desktop runs no `systemd-networkd`.
- Locations: `measurement-overview.md:73-79, :106, :172-177, :100, :199, :200`.
- Repo: the claims are within the passages that `docs/references.md:114, :119, :124, :129, :134, :139, :401-421` quote.
- Record: no slice search record holds those passages. The slice changelogs (9.6 D24, 9.5 D33, D78, D86, D91, 9.8 D28, 9.9 D37) attest the reads but paraphrase them. `chow-aoms65` (D-F5-09) and `fqcodel-rfc18` (D-F5-14) have the same record situation; they are listed above under wording.
- Nothing shows the reads were made without the repository's wording. `netplan`'s copy has no commit.
- Fix: persist each read as a search record in its slice (verbatim passage, locator, copy, date), pin netplan's commit, and point the changelog decisions to the records.

**D-F1-43 — the tuned entry's quotations.**
- Location: `docs/references.md:586`.
- Repo: quotes three passages from tuned's `tuned-main.conf`:
  - "It must be multiply of the sleep_interval"
  - "How long to sleep before checking for events (in seconds)"
  - "if disabled only static tuning will be used"
- Record: 9.19-P:17 holds none of the three.
- Fix: add the three `tuned-main.conf` lines (v2.28.0) to the 9.19 record, or cut the quotations to the recorded words.

**D-F1-45 — the systemd-oomd entry's quotations.**
- Location: `docs/references.md:591`.
- Repo: quotes "Must be set to 0, or at least 1 second" and "in which all tasks in the control group were delayed".
- Record: 9.19-P:19 elides both with "…".
- Fix: record the full `oomd.conf.xml` passages with the commit of `main` read, or cut the quotations.

**D-F1-49 (with D-F5-19) — the kernel task-name passages "at v6.17".**
- Location: `docs/references.md:385-387`; `dataset/sources.yaml:233-234`.
- Repo:
  - The cite quotes `sched.h`'s comments at tag v6.17, "accessed 2026-10-12".
  - sources.yaml pins "NUL-terminated and zero-padded" to v6.17.
- Record: the v6.17 record (9.10-S4:1500, S4-09) quotes only `TASK_COMM_LEN = 16`. The comment passages are recorded at v6.8 and v7.0 (9.10-S2:1735-1791, S2-11), read 2026-10-01. No 2026-10-12 read is recorded. The local v6.17 copy holds the same comment at `sched.h:1156-1161`, unquoted.
- Fix: record the v6.17 lines 1156-1161 in a 9.10 record, or point the cite and the status to S4-09 and S2-11 with their 2026-10-01 date.

**D-F3-11 — the kernel Makefile and `-pipe`.**
- Location: `dataset/archetypes.yaml:1017-1018`.
- Repo: "no `-pipe` in the kernel's Makefile".
- Record: no passage of the kernel's Makefile is recorded. task-9.6-compile/search/S2-project-docs.md:311-356 holds GCC's rule (`cc1` then `as`, piped only with `-pipe`), and the run shows the sequence.
- Fix: record a grep of linux-6.6's `Makefile` and `arch/x86/Makefile` for `-pipe`. Or reword: "`cc1` and `as` run in sequence in the run (GCC pipes them only under `-pipe`)".

**D-F3-35 — HandBrake 1.7.2's default preset.**
- Location: `dataset/archetypes.yaml:1625-1627`.
- Repo: the default preset is "Fast 1080p30" (x264 fast, RF 22, main, 4.0, AAC stereo 160, MP4).
- Record: 9.10-S2:3879-3886 (S2-55) quotes other presets. It has no verbatim passage for the Default mark or for this preset's fields. F3 read the local copy, and the repository's values hold there.
- Fix: add the Fast 1080p30 stanza's fields verbatim to S2-55.

## No record (4 claims)

**D-F3-31 — module signing on a Secure Boot desktop.**
- Location: `dataset/archetypes.yaml:1135-1136`, `:1305-1306`.
- Repo: "where a Secure Boot desktop signs the five".
- Record: none. The nearest passage reads the other way: 9.10-S2:3512 (S2-28) says "DKMS drivers are not signed with Canonical's key and thus do not support secure boot".
- Fix: read DKMS 3.0.11's signing step into a 9.10 record, or drop the clause.

**D-F4-22 — the SYSmark 30 copy read.**
- Location: `docs/references.md:228`, `:230`.
- Repo: a Wayback snapshot of 2025-04-23, accessed 2026-09-12.
- Record: no read of that copy. The persisted read is the 2025-08-21 capture (20250821210035), retrieved 2026-09-13 (R05:3, :12).
- Fix: state the R05 copy in the cite and status lines.

**D-F4-47 — Chromium's `HangWatcher` thread.**
- Location: `dataset/archetypes.yaml:738`.
- Repo: "`HangWatcher`, Chromium's hang-detection thread".
- Record: none. 9.8 changelog:222 states it without a source.
- Fix: read `base/threading/hang_watcher.h` at the measured Chrome tag and record the passage, or reduce the wording to the thread's name.

**D-X-01 — what enterprise, VDI and cloud traces record.**
- Location: `docs/workload/grounding-sources.md:59`.
- Repo: "Server/VM granularity; no consumer applications; process identity absent or hashed".
- Record: none. 9.12's S3-08 read the Google and Alibaba schemas only for a context-switch field. No record names an Azure trace or a VDI study.
- Fix: quote the Google schema's identity fields from the S3-08 copy and cite it. Drop Azure and VDI, or mark them "unsourced" as line 61 does.

## Labels (5 claims)

**D-F1-11 — schedules per wake.**
- Location: `dataset/archetypes.yaml:1789-1790`; `dataset/variants.yaml:53`.
- Repo: "about 1.4 schedules per wake", beside the slide-14 tag.
- Record: 9.4-S2:93 has only the slide's 28.78 % preemption share. 9.4 decision D9 derives the 1.4.
- Fix: label it arithmetic: "(our arithmetic: 1/(1 − 0.2878))".

**D-F3-08 — the label of `parallelism_cap` 8.**
- Location: c1-compile:22, c4-compile:40, c7-compile:43, `building-plan.md:101`, `archetypes.yaml:1134`.
- Repo: labelled "design".
- Record: 9.6 decision D4 (task-9.6-compile/changelog.md:21) says "Label: convention".
- Fix: use one label, "convention" per D4, or record a re-decision. This is a judgement for 인지오.

**D-F4-49 — the order of the evening arc.**
- Location: `dataset/timelines/coreset/c3-evening.timeline.yaml:1-2`; `building-plan.md:136`.
- Repo:
  - c3-evening carries no "order is design" label, which its siblings c3-workday and c3-creation carry.
  - building-plan.md:136, "transitions of these shapes, in these orders, occur", reads as a realism claim and contradicts :132, "Each arc's order is design".
- Fix: add "The order is design; no source defines it." to c3-evening's header. Reword :136 to "existence cases — the dataset holds transitions of these shapes, in these orders".

**D-F5-11 — the compile-fidelity tolerances.**
- Location: `docs/workload/measurement-overview.md:106`.
- Repo: within 2 %, and within 5 % or four standard errors, with `feller-ipta50` beside them.
- Record: 9.5 decision D86. Feller grounds the standard error only.
- Fix: "(tolerances ours; the standard error `feller-ipta50`'s)".

**D-X-02 — what older desktop trace studies released.**
- Location: `docs/workload/grounding-sources.md:61`.
- Repo: "raw timelines with names were never released, largely for privacy (unsourced: no study is named)".
- Problem: this is a factual statement about the literature, labelled "unsourced". It is none of the four kinds decision 1 allows an unsourced value: convention, arithmetic, placeholder or design.
- Fix: "no raw timeline with names was found in the studies searched", with the search it rests on (9.10 S3, 9.12 S3). Or drop "largely for privacy".

## Other notes (not decision 1 verdicts)

- **Stale repeat-count range.** `docs/references.md:129`, `:134` (the `chow-aoms65` and `cochran-st77` role lines) and `_dev/research/jioh/measurement-campaign-workflow.md:27` say the campaigns pooled "5 to 45" repeats. `measurement-overview.md:79` says "5 to 77", which is right: `mail-client`'s idle phase pooled 77 (`measurement-campaign-record.md:63`).
- **Pointer slips** (F2):
  - `docs/references.md:39` says "D6's alternative not taken"; it is 9.5 decision D4.
  - `c6-dual.timeline.yaml:33` cites "9.10 C-gonzalez-1", which is the 2026-09-13 verification's claim id, cited by 9.10 decision D35.
  - `docs/references.md:38` puts licence wording in quotation marks that is not `readme.txt:21` verbatim.
  - `docs/references.md:59` calls a log-scale variance a "spread".
  - `docs/references.md:64` calls Killourhy and Maxion's feature table a "raw" latency dataset.
- **For the compiled-number audit.** D-F2-44 says the shipped CachyOS catalogue fully keys 7 of the 50 core files (`building-plan.md:121`, 9.12 D109). That count was taken on the 2026-10-09 build. Whether it holds on the final build is the compiled-number audit's check (9.16 decision 5).
