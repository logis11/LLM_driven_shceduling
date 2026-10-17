# Blind reader B1 — Phase 2 comparison (source groups 1–15 of the dataset blind-topics file)

Reader B1's comparison for task 9.16 (the Phase 9 exit audits). It sets the repository's wording of 48 claims against B1's Phase 1 passages. The Phase 1 file is `reads/B1-reads.md`: sha256 `777db35099223de6ef6a8f4b2e153659a1e0b15a86acdb9ef6a800b23e0793ec`, closed before `claims/dataset-inventory.md` was opened and not edited since. The repository was read at `928aa8fd`, working tree on 2026-10-17. Each claim is compared over object, unit, statistic, scope and population.

Verdicts:
- SUPPORTED: the wording stays within B1's passage.
- WORDING-FIX: the object is right, but the wording goes beyond the passage or misplaces it.
- CONTRADICTED: the passage says otherwise.
- NOT IN SOURCE: the cited source does not state it.
- UNVERIFIABLE: B1's reading cannot decide it.

After Phase 1 closed, three checks were made with the repository's wording in view. Each is marked "post-blind" where it is used:
- (a) Slide 16's embedded graph image was extracted from the PDF.
- (b) The SWELL-KW (the SWELL Knowledge Work dataset) Word gap share was recomputed with the stimulus stream's scope: condition 1 only, all keys.
- (c) The 9.10 (scenarios and timelines slice) record's focus-episode definition was read so the dwell figures could be compared.

## Summary

| verdict | count |
|---|---|
| SUPPORTED | 34 |
| WORDING-FIX | 11 |
| NOT IN SOURCE | 2 |
| UNVERIFIABLE | 1 |
| CONTRADICTED | 0 |
| **claims compared** | **48** |

| claim | object | verdict | one-line fix |
|---|---|---|---|
| D-F1-01 | LAVD talk identity, 30 slides | SUPPORTED | — |
| D-F1-02 | ~300 tasks scheduled while a game runs | SUPPORTED | — |
| D-F1-03 | ~90 % long-living | SUPPORTED | — |
| D-F1-04 | top 30–40 tasks = 95 % of scheduling; split | SUPPORTED | — |
| D-F1-06 | per-schedule runtimes, wineserver 260 µs, worker 1.65 ms | SUPPORTED | — |
| D-F1-08 | execution time stable, predictable by average | SUPPORTED | — |
| D-F1-09 | slide 13 plot ~128 tasks, median ~0.04 ms | SUPPORTED | — |
| D-F1-10 | 70–75 % waiting syscalls, preemption 25–30 %, sched_preempt 28.78 % | SUPPORTED | — |
| D-F1-12 | "the deck's slice example 1.5 ms" | NOT IN SOURCE | attribute 15 ms ÷ 10 tasks to scx_lavd's `main.bpf.c` comment (`scx`), not the deck |
| D-F1-13 | slide 16 thread names | SUPPORTED | (optional) say the head `Troy.exe` is in the clipped part of slide 16's embedded graph |
| D-F1-14 | six chain members named `Troy.exe` under the s16 tag | WORDING-FIX | say six members carry the process `comm` by the repository's rule; the slide shows one `Troy.exe` node |
| D-F1-16 | task sequence serves one job; periodic | SUPPORTED | — |
| D-F1-17 | no frame period/budget; 15 ms is a targeted latency | SUPPORTED | — |
| D-F1-18 | games and machine unnamed | SUPPORTED | — |
| D-F1-19 | deck's traces "collected with perf sched record" | NOT IN SOURCE | cite `edge-lwn26` (VaporMark on "perf sched record", LPC 2025) or drop the tool from the deck's description |
| D-F1-20 | at least three process trees; slides 12–14 trace unstated | SUPPORTED | — |
| D-F1-26 | download check box; default pause at launch | SUPPORTED | — |
| D-F1-27 | per-game setting attributed to FAQ 4F9E | WORDING-FIX | put the per-game setting under FAQ 71AB-698D-57EB-178C |
| D-F1-28 | updates queued automatically | SUPPORTED | — |
| D-F1-29 | user-started install proceeds during play | SUPPORTED | — |
| D-F1-30 | SteamOS 3.8: user-selected, not default | UNVERIFIABLE | none from B1; the release note supports "user selects", and "not enabled by default" rests on the image read B1 did not repeat |
| D-F1-31 | "Valve sponsors LAVD" | WORDING-FIX | "Valve holds the copyright of scx_lavd, developed by Igalia's Min for SteamOS" |
| D-F1-32 | scx_lavd motivated by gaming, reduce stutter | SUPPORTED | — |
| D-F1-33 | Corbet's LPC 2024 report | SUPPORTED | — |
| D-F1-34 | Edge's LPC 2025 report | SUPPORTED | — |
| D-F1-35 | Meta: candidate default fleet scheduler | SUPPORTED | — |
| D-F1-36 | Windows Game Mode design | SUPPORTED | — |
| D-F1-37 | `SetProcessDefaultCpuSets` not a header function | SUPPORTED | — |
| D-F1-38 | Game Mode holds back Windows Update driver installs/restart notifications | SUPPORTED | — |
| D-F1-39 | macOS Game Mode | SUPPORTED | — |
| D-F1-40 | GameMode request model; `[filter]` whitelist | SUPPORTED | — |
| D-F1-46 | 5/10/30 s called "debounce" values | WORDING-FIX | GameMode check interval, tuned update interval (dynamic tuning off by default), systemd-oomd sustain duration |
| D-F1-48 | process names ≤ 15 characters | SUPPORTED | — |
| D-F2-01 | SWELL-KW population, setting, size | SUPPORTED | — |
| D-F2-02 | uLog: per-keystroke app; pointer "no motion" | WORDING-FIX | pointer events carry cursor position and distance moved since the last event; special-key events carry no application |
| D-F2-03 | DANS licence and access | SUPPORTED | — |
| D-F2-06 | dwell median 9.1 s; A→B→A 83.4 % | WORDING-FIX | name the filtered focus sequence (logger window and shell surfaces dropped); the raw sequence gives a median of ~5 s |
| D-F2-07 | 136M Keystrokes file, fields, rows, licence | WORDING-FIX | quote readme.txt:21 exactly: "You are free to use this data for non-commercial use …" |
| D-F2-08 | Dhakal paper population and IKI statistics | SUPPORTED | — |
| D-F2-09 | gap shares 0.7 % vs 5.5 %; the decision not taken | WORDING-FIX | "D6's" → 9.5 D4's; flag that 0.7 % is a six-participant figure (B1's 2,000-participant sample: 2.1 %) |
| D-F2-10 | 3 min 08 s per event, scope | WORDING-FIX | "formal meetings, unknown and personal events excluded" |
| D-F2-11 | 11 min 28 s sphere segment and companions | SUPPORTED | — |
| D-F2-12 | spheres/day, time per tool, statistics, population | WORDING-FIX | "14 shadowed information workers"; "means and SDs, with ANOVAs" |
| D-F2-14 | Mark 2005: 11 min 4 s; 24 informants incl. CHI 2004's 14 | SUPPORTED | — |
| D-F2-15 | internal/external split; Table 3 inconsistency | SUPPORTED | — |
| D-F2-16 | same-day resumption 77.2 %, 25 min 26 s; 23 min 15 s absent | SUPPORTED | — |
| D-F2-17 | Czerwinski diary study | SUPPORTED | — |
| D-F2-18 | Roeser task, sample, model, Table 3 | WORDING-FIX | "fluent spread 0.29" → "fluent-typing variance σ²e 0.29 (log scale)" |

---

## Group 1 — Min 2024 slides (`lavd-ossna24`)

### D-F1-01 — SUPPORTED
- location: docs/references.md:733
- repo: "Min, C. (2024). "Optimizing Scheduler for Linux Gaming." Talk, Open Source Summit North America 2024, Seattle, 2024-04-17. Slides: … (30 slides; SHA-256 `e62d69cd…`)"
- B1: slide 1 "Changwoo Min … April 17, 2024"; session page "Wednesday April 17, 2024"; the site header "Seattle, WA, USA"; 30 pages. The sha256 of B1's copy is identical.
- fix: none.

### D-F1-02 — SUPPORTED
- location: dataset/sources.yaml:63-64 (also archetypes.yaml:1803-1805, docs/workload/source-vetting.md:144)
- repo: "Around 300 tasks scheduled system-wide while running a game (system tasks included)"
- B1: slide 12 "Around 300 tasks are scheduled while running a game." The slide has no "system tasks included" sentence, but the inclusion follows from slide 12 itself. Its top 30–40 tasks are a subset of the ~300, and "around half of them are system tasks". "System-wide" is the same inference.
- fix: none (the parenthetical is a sound inference from slide 12).

### D-F1-03 — SUPPORTED
- location: dataset/sources.yaml:64; archetypes.yaml:1807-1809
- repo: "~90% long-lived"; "Around 90% are long-living tasks; only 10% of tasks are terminated" (s12, window unstated)
- B1: slide 12, verbatim the same.
- fix: none.

### D-F1-04 — SUPPORTED
- location: dataset/sources.yaml:64-67; c1-gaming.timeline.yaml:2-4 (the omission)
- repo: "the top 30-40 tasks 95% of scheduling, around half of them system tasks (especially wine, graphics and audio servers) taking 30-40%, 15-20 game-specific tasks 60-70% (s12)"; "describes none outside them"
- B1: slide 12 has the same figures. B1 noted that tasks outside the top group are not described.
- fix: none.

### D-F1-06 — SUPPORTED
- location: dataset/archetypes.yaml:1774-1778; sources.yaml:68-70
- repo: "a coordination task (wineserver, 260 us) and a work task (a task worker, 1.65 ms), spanning its stated "a few 100s usec on average to a few msec maximum" (s13)"
- B1: slide 13, the same passages. B1's Phase 1 noted one more thing: the 1.65 ms example exceeds the plot's maximum (~1.38 ms). The repo's "the statistic behind the two examples is not labelled" fits that.
- fix: none.

### D-F1-08 — SUPPORTED
- location: dataset/archetypes.yaml:1784-1785; sources.yaml:70-71
- repo: "Task execution time is very stable and is predictable using its average" (s13)
- B1: slide 13, verbatim.
- fix: none.

### D-F1-09 — SUPPORTED
- location: dataset/archetypes.yaml:1778-1780
- repo: "the slide's plot of per-task runtime averages (one game, ~128 tasks, median ~0.04 ms)"
- B1: the caption reads "Distribution of task's runtime average per schedule in a game". The curve covers about 128 tasks and reads ≈ 0.04 ms around the middle task.
- fix: none.

### D-F1-10 — SUPPORTED
- location: dataset/archetypes.yaml:1788-1789, :1809-1811; sources.yaml:71-72
- repo: "preemption 25-30 % of scheduling events, sched_preempt 28.78 % on the pie"; ""70-75% of scheduling is initiated by waiting system calls" against 25-30% preemption (s14)"
- B1: slide 14 text, and the pie label "sched_preempt (28.78%)".
- fix: none. The "about 1.4 schedules per wake" in the same sentence is D-F1-11, outside B1's sample.

### D-F1-12 — NOT IN SOURCE
- location: dataset/archetypes.yaml:1791-1792
- repo: "(s13: 1.65 ms worker; the deck's slice example 1.5 ms)"
- B1: the deck's only example is slide 27: "a targeted latency (e.g., 15 msec)", divided "as per task's nice priority". No slide gives 1.5 ms. The 1.5 ms is implied, not stated, by scx_lavd v1.1.3 `main.bpf.c:71-72`: "if a targeted latency is 15 msec and 10 tasks are runnable, the scheduler equally divides 15 msec of CPU time into 10 tasks". The v1.1.3 code constant is 10 ms (`lavd.bpf.h:73`), with slices of 0.5–5 ms.
- fix: "(… ; scx_lavd's source-comment example, 15 ms shared by 10 tasks, `scx`)", or drop the comparison.

### D-F1-13 — SUPPORTED
- location: dataset/sources.yaml:73-74; c1-gaming.timeline.yaml:20-21 (`member_names`, tag `lavd-ossna24:s16`); docs/workload/grounding-sources.md:30
- repo: "tasks tightly linked in waiter-waker graphs, with the thread names of s16"; names `Task worker thr` ×4, `dxvk-cs`, `dxvk-submit`, `winepulse_mainl`, `winepulse_timer`, `FAudio_AudioCli`, `Troy.exe`
- B1: in Phase 1, all nine thread names were read from the displayed slide 16. `Troy.exe` was not visible there. Post-blind (a): slide 16's graph is one embedded 2048 × 211 image, drawn wider than the slide and clipped to its central ~36 %. The full image (`$B/lavd/img16/p-008.png`, sha256 `552f4616…`) also shows `Troy.exe[7781/0]`, `wineserver[7256/0]`, `explorer.exe[7301/0]` and the full label `CSteamControlle[4908/4788]`. So all ten names are in slide 16's content. `Troy.exe` sits only in the part a viewer of the slide does not see.
- fix: none required; optionally "slide 16's embedded graph (its clipped left part names `Troy.exe`)", so a reader of the displayed slide can find it.

### D-F1-14 — WORDING-FIX
- location: c1-gaming.timeline.yaml:20-21 (and the seven other gaming files' `member_names`); docs/workload/coreset-guide.md:252; docs/workload/scenario-catalog.md:36
- repo: `member_names: [… FAudio_AudioCli, Troy.exe, Troy.exe, Troy.exe, Troy.exe, Troy.exe, Troy.exe]`, `source: {member_names: "lavd-ossna24:s16"}`; coreset-guide "slide 16이 보여주는 game thread 이름" ("the game thread names slide 16 shows"); scenario-catalog "the game chain's thread names from `lavd-ossna24` slide 16"
- B1: slide 16 (with its clipped part, post-blind a) has one `Troy.exe` node. Each other name appears once, except `Task worker thr` (×4). For the six repeats, B1 checked Wine wine-11.20. `env.c:485-503` sets the process's comm to the executable's base name (`prctl(PR_SET_NAME, …)`). `thread.c:2057-2091` writes a thread's comm only when the program names the thread. So Wine itself gives an unnamed thread no name, and it keeps the comm it inherits (kernel behaviour, not read by B1). The six `Troy.exe` are therefore the repository's rule applied to Wine, not slide 16.
- fix: add one sentence in `game-task-chain`'s modeling_notes and at coreset-guide.md:252: "six members carry the process `comm` `Troy.exe` (a Wine thread that sets no name keeps its process's name; our rule, 9.10 D26); slide 16 names the other nine".

### D-F1-16 — SUPPORTED
- location: dataset/sources.yaml:75-76; archetypes.yaml:1764-1768, :1772-1773
- repo: "a sequence of tasks serving a single job, e.g. from a user input to display update (s17)"; "s17 says the majority of game tasks are individually periodic"
- B1: slide 17 has the same passages. "Individually periodic" paraphrases "Majority of game tasks shows periodic behavior … a task has a stable execution time and a stable wait time".
- fix: none.

### D-F1-17 — SUPPORTED
- location: dataset/sources.yaml:76-77; docs/workload/source-vetting.md:144
- repo: "The slides state no frame period or frame budget."; "its 15 ms is an example scheduler targeted latency for time slices"
- B1: no slide states a frame period or budget. Slide 27 gives "targeted latency (e.g., 15 msec)" for the time slice.
- fix: none.

### D-F1-18 — SUPPORTED
- location: dataset/sources.yaml:59-60; archetypes.yaml:1756-1757
- repo: "from traces collected while playing games, the games and the machine unnamed"
- B1: slide 10, "We collect and analyze all scheduling activities while playing games". No game and no tracing machine is named.
- fix: none.

### D-F1-19 — NOT IN SOURCE
- location: dataset/archetypes.yaml:1756-1757; docs/workload/coreset-guide.md:242
- repo: "lavd-ossna24 slides 12-17 taken as one observation of an unnamed game on an unnamed machine, collected with perf sched record"
- B1: the 2024 deck names no collection tool, in its text or its figure images. The tool appears in Edge's report of the LPC 2025 session (`edge-lwn26`): "he developed VaporMark … which analyzes data collected using "perf sched record"". That sentence does not tie the tool to the 2024 deck's traces.
- fix: "collected — by Min's later account (`edge-lwn26`) of his analysis tool — with `perf sched record`", or drop the tool from the deck's description.

### D-F1-20 — SUPPORTED
- location: dataset/archetypes.yaml:1758-1759
- repo: "the deck's figures draw on at least three process trees and the text does not say which feeds slides 12-14"
- B1: the game process ids are 6340 (slide 11), 4727 (slide 15) and 7781 (slide 16). No text names the trace behind slides 12–14.
- fix: none.

## Group 2 — Steam Support FAQs (`steam-downloads`)

### D-F1-26 — SUPPORTED
- location: dataset/sources.yaml:139-142; docs/references.md:295; docs/workload/scenario-catalog.md:21
- repo: "the "Allow Downloads During Gameplay" check box (Steam -> Settings -> Downloads), that downloads pause during gameplay by default"
- B1: FAQ 4F9E: "Steam automatically pauses your downloads when a game is launched … check the Allow Downloads During Gameplay box" under Steam > Settings > Downloads.
- fix: none.

### D-F1-27 — WORDING-FIX
- location: docs/references.md:295; dataset/sources.yaml:142
- repo: "and of a per-game setting the article leaves unnamed (FAQ 4F9E-6328-E9B8-47F9)"; sources.yaml "and a per-game setting the article leaves unnamed"
- B1: 4F9E mentions no per-game setting. FAQ 71AB does: "There's also a per-game setting to allow/prevent the downloading of other updates while you're playing."
- fix: give the per-game setting "(FAQ 71AB-698D-57EB-178C)" and keep 4F9E for the check box and the default pause. In sources.yaml, say "the second article".

### D-F1-28 — SUPPORTED
- location: docs/references.md:295
- repo: ""Games are automatically put into your download queue when a game releases an update" (FAQ 71AB-698D-57EB-178C)"
- B1: 71AB, verbatim.
- fix: none.

## Group 3 — steam-for-linux issue #8821

### D-F1-29 — SUPPORTED
- location: docs/references.md:299; docs/workload/scenario-catalog.md:21
- repo: "with "Allow downloads during gameplay" off, Steam pauses queued downloads when a game launches, "But if you have a game launched and during gameplay press "Install" for another game that game will start downloading immediately." … confirmed by Valve's triager as "not specific to SteamOS or the Steam Deck" … one user's Steam Deck"
- B1: the issue body and kisak-valve's first comment, both verbatim. The triager also said, personally, that the behaviour should not change. "Confirmed" fits the "not specific" sentence.
- fix: none.

## Group 4 — SteamOS 3.8 note; scx v1.1.3; Edge LWN 1051430

### D-F1-30 — UNVERIFIABLE
- location: docs/workload/grounding-sources.md:30; docs/references.md:310
- repo: "ships it in SteamOS 3.8 as a scheduler the user selects, not enabled by default (`steamos-lavd`)"
- B1: the release note's Developer list has "Initial support for LAVD CPU scheduler via `steamosctl set-cpu-scheduler lavd`". That supports "the user selects". The note says nothing about a default either way. references.md:310 rests "not enabled by default" on an image and `steamos-manager` observation, which B1 did not read.
- fix: none proposed. The part B1 can check holds, and the rest needs the image read.

### D-F1-31 — WORDING-FIX
- location: docs/workload/grounding-sources.md:30; docs/references.md:310
- repo: "Valve sponsors LAVD"; "Valve sponsors LAVD's development: scx_lavd's `lat_cri.bpf.c` reads "Copyright (c) 2023-2025 Valve Corporation. Author: Changwoo Min …""
- B1: the scx_lavd files at v1.1.3 carry "Copyright (c) … Valve Corporation" with "Author: Changwoo Min <changwoo@igalia.com>". Edge: "developing LAVD as part of his work at Igalia on SteamOS and the Steam Deck". Neither source uses "sponsor" or says Valve funds the work. The copyright line shows ownership of the code.
- fix: "Valve holds the copyright of scx_lavd, which Igalia's Min develops as part of his work on SteamOS". If "sponsors" is kept, label it the repository's reading (9.12 D9).

### D-F1-32 — SUPPORTED
- location: docs/workload/grounding-sources.md:30; docs/references.md:195
- repo: "scx_lavd motivated by reducing stutter"; "it was motivated by gaming workloads, to reduce stuttering (`scx_lavd/README.md:7–12`, `:20–23`)"
- B1: README:20-21, "initially motivated by gaming workloads. It aims to improve interactivity and reduce stuttering".
- fix: none.

### D-F1-34 — SUPPORTED
- location: docs/references.md:758; docs/workload/source-vetting.md:166
- repo: "LAVD developed "as part of his work at Igalia on SteamOS and the Steam Deck" … "there are often 20 or 30 tasks in a chain …"; a session … "about adapting LAVD to be the default scheduler for Meta's production fleet""
- B1: Edge, each quote verbatim. The article is dated January 7, 2026, and is LWN 1051430.
- fix: none.

## Group 5 — Corbet LWN 991205

### D-F1-33 — SUPPORTED
- location: docs/references.md:738-739; docs/workload/source-vetting.md:166
- repo: "Corbet, J. "Sched_ext at LPC 2024." LWN.net, 2024-09-26 …"; "short-running, tightly linked tasks, a virtual deadline from each task's waking and waiting frequencies"; "typically no more than 100µs at a time"
- B1: Corbet's "Higher frame rates" section, the same passages, dated September 26, 2024.
- fix: none.

## Group 6 — Dai & Newton LPC 2025

### D-F1-35 — SUPPORTED
- location: docs/workload/grounding-sources.md:30; docs/references.md:753
- repo: "Meta's speakers presented it as a candidate default fleet scheduler"; abstract quote
- B1: contribution 2099, "There exists a need for a "default" fleet scheduler … SCX_LAVD is one such candidate". The speakers are David Dai and Ryan Newton (Meta), on 12 Dec 2025.
- fix: none.

## Group 7 — Microsoft, Xbox, Apple Game Mode

### D-F1-36 — SUPPORTED
- location: docs/references.md:248-250
- repo: "works by default for most Windows games, requiring no action or opt-in by the customer, and no work by the game developer"; "granted on a per-title basis …"; foreground/focus condition; "having to share them with other processes" / "a higher latency due to other processes …"; the deprecation note
- B1: the portal and the ReleaseExclusiveCpuSets page, each passage verbatim, including "deprecated in Windows 10, version 1809 and later". (B1 did not specifically re-check "memory resources, once granted, will never be revoked", though it is in B1's portal copy.)
- fix: none.

### D-F1-37 — SUPPORTED
- location: docs/workload/source-vetting.md:157
- repo: "`SetProcessDefaultCpuSets` is not an `<expandedresources.h>` function (the header documents three, the function only in a remark)"
- B1: the header page lists three functions. The name appears only in "As with SetProcessDefaultCpuSets, ReleaseExclusiveCpuSets applies to the whole process." (ReleaseExclusiveCpuSets remarks and the portal).
- fix: none.

### D-F1-38 — SUPPORTED
- location: docs/workload/grounding-sources.md:18; docs/references.md:254
- repo: "Windows Update's driver installs and restart notifications while a game runs in Game Mode"; "Game Mode is turned on by default."
- B1: Xbox Support (rendered), "Prevents Windows Update from performing driver installations and sending restart notifications" and "Note Game Mode is turned on by default."
- fix: none. B1 did not read the Xbox Wire dating.

### D-F1-39 — SUPPORTED
- location: docs/references.md:259
- repo: "When your game enters full screen, Game Mode automatically turns on for that game"; "highest priority access to your CPU and GPU, lowering usage for background tasks"; "Mac with Apple silicon and macOS Sonoma 14 or later …"
- B1: Apple 105118, verbatim, "Published Date: September 14, 2026".
- fix: none.

## Group 8 — GameMode, tuned, systemd-oomd

### D-F1-40 — SUPPORTED
- location: docs/references.md:581
- repo: "a game enters GameMode by its own request — the library call (`gamemode_request_start()`, `gamemoded.8.in:49–56`) or a launcher that integrates it — or by being launched under `gamemoderun` (`README.md:23–28`); the optional `[filter]` whitelist rejects requesters not on it (`gamemode.ini:49–55`, commented out in the example)"
- B1: at tag 1.8.2, README "For games/launchers which integrate GameMode support … simply running the game will automatically activate GameMode … launching the game through `gamemoderun`". `gamemode.ini` [filter]: "gamemode will reject anything not in the whitelist", with the example commented out. B1 did not read `gamemoded.8.in`, and the line numbers cite `master` a74b8106, not the tag B1 read.
- fix: none.

### D-F1-46 — WORDING-FIX
- location: dataset/grids.yaml:57-60; dataset/README.md:150; docs/workload/building-plan.md:185; docs/workload/coreset-guide.md:588
- repo: "5 s, 10 s and 30 s are the debounce values of the daemon-level switches comparable to ours — GameMode's reaper interval, tuned's dynamic-tuning update interval, systemd-oomd's pressure duration"
- B1: GameMode: "The reaper thread will check every 5 seconds for exited clients, for config file changes, and for the CPU/iGPU power balance", a polling interval. tuned: "Update interval for dynamic tunings (in seconds)" = 10, with `dynamic_tuning = 0`, so dynamic tuning ships off. systemd-oomd: "the amount of time a unit's control group needs to have exceeded memory pressure limits before systemd-oomd will take action", 30 s by default; only this one is a sustain-before-acting duration. None of the three uses "debounce".
- fix: at the four locations, "GameMode's 5 s reaper check interval, tuned's 10 s dynamic-tuning update interval (dynamic tuning off by default), systemd-oomd's 30 s pressure sustain duration".

## Group 9 — `include/linux/sched.h` v6.17

### D-F1-48 — SUPPORTED
- location: dataset/grids.yaml:29-31; docs/references.md:385-386
- repo: "TASK_COMM_LEN is 16 bytes including the terminating NUL (`include/linux/sched.h`), so 15 characters"
- B1: "TASK_COMM_LEN = 16"; `comm` is "always NUL-terminated and zero-padded". The sha256 of B1's copy matches the repository's `d7a2b1e7…`.
- fix: none.

## Group 10 — SWELL-KW (`swell-icmi14`)

### D-F2-01 — SUPPORTED
- location: dataset/sources.yaml:43-46; docs/references.md:69; docs/workload/grounding-sources.md:43
- repo: "25 students and interns doing knowledge-work tasks in a lab, ~3 h each, free composition on Windows (2012)"; "Windows 7 lab … Sept–Nov 2012"
- B1: paper §3.7, "25 students … interns from TNO and students from Delft University of Technology"; §3.4, Windows 7 Professional; §3.3, "about 3 hours". The uLog dates run from 2012-09-18 to 2012-11-07.
- fix: none.

### D-F2-02 — WORDING-FIX
- location: dataset/sources.yaml:42-43, :51-52; docs/references.md:69
- repo: "per-keystroke and per-click/drag/wheel timestamps with the focused application"; "motion between pointer events not recorded"; "mouse as click/drag/wheel only, no motion"
- B1: in the uLog XML, keyboard 'character' events carry `ControlApplication` and `ControlWindowText`. 'special key' events carry a `Control` with only `ControlIsPassword`, so no application. Mouse events ('clicked', 'doubleclicked', 'dragged', 'wheel turned') carry `MouseCursorX`/`Y`, `MouseRelDistance` (e.g. 764.3) and `MouseTotDistance`. So the distance moved since the previous pointer event is recorded, though no motion samples are.
- fix: "pointer events (click/drag/wheel) with cursor position and the distance moved since the previous event, no motion samples between them; character keystrokes with the focused application (special keys without it)".

### D-F2-03 — SUPPORTED
- location: dataset/sources.yaml:41-42; docs/references.md:68; docs/workload/grounding-sources.md:43
- repo: "DANS doi:10.17026/dans-x55-69zp v4, CC-BY-NC-SA-4.0"; "version 4 (2025-06-04), CC-BY-NC-SA-4.0, no access request"
- B1: the API reports versionNumber 4, minor 1, released 2025-06-04T08:57:35Z. The licence is CC-BY-NC-SA-4.0, with `fileAccessRequest: false` and every file unrestricted.
- fix: none. "Version 4" is the major version of the 4.1 release.

### D-F2-06 — WORDING-FIX
- location: docs/workload/building-plan.md:205; docs/workload/grounding-sources.md:43; docs/references.md:69
- repo: "a dwell median of 9.1 s per focus episode, A → B → A returns after 83.4 % of middle episodes (the reader's computations)"
- B1: B1's blind computation used every "Window Activated" application, the uLog window included, with consecutive repeats merged. It gave 9,575 episodes, a median of 5.47 s, a mean of 24.13 s, and immediate A→B→A returns after 54.1 % of switches. Post-blind (c): the 9.10 record (S3-01, `S3-traces-datasets.md:236-246`) states 9.1 s and 83.4 % for its "app_filtered" sequence. That sequence drops the logger's window, `dwm`, UNKNOWN and Explorer shell surfaces, and counts uncensored middle episodes. Its own "app_raw" variant gives a median of 5.1 s, which agrees with B1's 5.47 s. The figures are the record's, correctly copied. The repository wording does not say they hold only after that filtering, and the filtering moves the median ×1.8 and the return share by ~30 points.
- fix: "(the reader's computations over the focus sequence with the logger's window and shell surfaces removed; the unfiltered sequence gives a median of 5.1 s)".

## Group 11 — Dhakal et al. 2018 (`dhakal-chi18`)

### D-F2-07 — WORDING-FIX
- location: docs/references.md:38; dataset/README.md:218
- repo: "`data/Keystrokes.zip` (1 572 785 433 bytes, Last-Modified 2018-03-29 …); per-keystroke PRESS_TIME/RELEASE_TIME in ms … `metadata_participants.txt` 168 594 rows; licence per readme.txt line 21, "free to use for non-commercial use in your own research or projects with attribution to the authors""
- B1: Content-Length 1572785433 and Last-Modified 2018-03-29 match. readme:59-60 gives PRESS_TIME and RELEASE_TIME "(in ms)". The metadata has 168,594 data rows. readme.txt:21 reads "You are free to use this data for non-commercial use in your own research or projects with attribution to the authors." The repository's quotation drops "You are" and "this data" inside quotation marks.
- fix: quote readme.txt:21 exactly, or remove the quotation marks.

### D-F2-08 — SUPPORTED
- location: docs/references.md:39
- repo: "self-selected online volunteers transcribing 15 memorised English sentences …; the mean of per-participant average inter-key intervals, 238.66 ms, SD 111.60 across participants; skew 1.98 and kurtosis 7.1 describe that across-participant distribution … IKIs over 5 000 ms dropped …; mouse editing allowed but not logged"; :38 "168 960 participants"
- B1: "Average inter-key interval is 238.656 ms (SD = 111.6) … skewness of 1.98 and kurtosis measure of 7.1". Figure 2 shows the distribution "over all participants", and the fast-typist SD of 11 ms only fits per-participant means. Also: "removed keystrokes … more than 5000 ms after the previous keystroke"; "136,857,600 keystrokes from 168,960 participants". On editing, the paper says "they allowed use of the mouse and arrow keys … From log data it is difficult to assess how often this happened".
- fix: none. "Not logged" is a fair reading for mouse edits, since the files log key events only.

### D-F2-09 — WORDING-FIX
- location: docs/references.md:39
- repo: "(D6's alternative not taken: transcription of memorised sentences, share of gaps over 1 s 0.7 % on a six-participant sample against 5.5 % between the keys of SWELL-KW's Word stream, `dataset/stimulus/swell-word-c1.jsonl`)"
- B1 computations: Dhakal, 2,000 participants (seed 20261017), 1,424,638 within-sentence press-to-press gaps, 2.13 % over 1 s (2.09 % with the paper's 5 s cut). SWELL-KW Word char→char over all conditions gave 3.07 %. Post-blind (b): with the stimulus stream's scope (condition 1, all keys attributed to Word), B1 gets 77,853 gaps and 5.06 %, consistent with the repository's 5.5 % over 78,013 gaps. The 9.5 changelog (the interactive-typing slice's decision log) records "Alternatives not taken: the 136M Keystrokes data … share > 1 s 0.7 %" under D4, "the replayed typing stream is SWELL-KW". D6 is that slice's platform rule.
- fix: "9.5 D4's alternative not taken". Add that the 0.7 % comes from six participants and that a 2,000-participant sample gives about 2 %. The contrast with SWELL-KW's ~5 % holds either way.

## Group 12 — González & Mark 2004 (`gonzalez-chi04`)

### D-F2-10 — WORDING-FIX
- location: dataset/sources.yaml:160-162 (also docs/references.md:44 and docs/workload/grounding-sources.md:40, which give no exclusion)
- repo: "~3 min (3 min 08 s) per event — one continuous use of a device or one interaction with a person, formal meetings excluded"
- B1: Table 2's row is "All events except "Formal meetings" and "Other"" = 0:03:08 (0:02:27), where "Other" = "unknown, personal". The text reads "(leaving out formal meetings, unknown, and personal events)".
- fix: "formal meetings, unknown and personal events excluded".

### D-F2-11 — SUPPORTED
- location: dataset/sources.yaml:162-166; docs/references.md:44; c6-dual.timeline.yaml:32-33
- repo: "11 min 28 s … central and peripheral spheres only (13 min 49 s over all spheres; 12 min 18 s when switches shorter than 2 min are ignored; … 33 min 32 s)"; 688 s
- B1: Table 4 gives 0:11:28 (central and peripheral) and 0:13:49 (all); Table 5 gives 0:12:18; the text gives "about 33 min. 32 sec. per working sphere". 11 min 28 s = 688 s.
- fix: none.

### D-F2-12 — WORDING-FIX
- location: dataset/sources.yaml:166-169
- repo: "Also ~10 spheres per person-day and ~2 min 11 s per tool/document before switching. Means and SDs only, 14 shadowed knowledge workers."
- B1: "an average of ten working spheres per day" (Table 4 gives 9.81 central and peripheral, 12.81 all); "2 min. 11 sec. working with any device or paper", Table 3's weighted average. The abstract says "observation of information workers in three different roles". Fourteen people were observed, and the paper reports ANOVAs and Tukey tests besides the means and SDs.
- fix: "Means and SDs (with ANOVAs), 14 shadowed information workers".

## Group 13 — Mark, González & Harris 2005 (`mark-chi05`)

### D-F2-14 — SUPPORTED
- location: docs/references.md:49; docs/workload/grounding-sources.md:41
- repo: "about 11 min (11 min 4 s, SD 18 min 9 s) in a central or peripheral working sphere before switching or being interrupted (p. 324); its 24 informants include CHI 2004's 14 (p. 323)"
- B1: p. 324, the same passage. p. 323 reads "Fourteen members from the JEB team were shadowed and in the second phase ten members of the AUG team". CHI 2004 shadowed 14 of the JEB team, and 2005 says it expands "the previous study" to "almost double the number of informants".
- fix: none.

### D-F2-15 — SUPPORTED
- location: docs/references.md:49
- repo: "Internal and external interruptions are roughly equal overall and for analysts and developers; managers 59.2 % external, 40.8 % internal (p. 326). The printed column split, 52.0 % internal / 48.0 % external, conflicts with Table 3's own cells, which imply about 48/52"
- B1: Table 3's column avg. reads 52.0 % | 48.0 %. B1's arithmetic from the rows gives internal ≈ 0.480. The text gives the managers' 59.2 % / 40.8 % and says analysts and developers are "about equally".
- fix: none.

### D-F2-16 — SUPPORTED
- location: docs/references.md:49; docs/workload/source-vetting.md:173
- repo: "resumed the same day 77.2 % of the time, after 25 min 26 s on average (SD 54 min 48 s) (p. 326)"; "the 23 min 15 s figure is absent from the four Mark et al. CHI papers searched … CHI 2005 reports a comparable 25 min 26 s"
- B1: p. 326 has the same figures. A text search of the CHI 2004, 2005, 2008 and 2014 copies finds no 23-minute resumption figure. B1 did not read the 2006 interview.
- fix: none.

## Group 14 — Czerwinski et al. 2004 (`czerwinski-chi04`)

### D-F2-17 — SUPPORTED
- location: docs/workload/grounding-sources.md:42; docs/references.md:54
- repo: "A one-week self-report diary of user-defined tasks (10 people analysed), reporting means and SDs"
- B1: "The week-long study"; an Excel diary; "Eleven experienced Microsoft Windows™ users"; "One outlier participant was removed … For the ten remaining participants". The paper reports means with SD (e.g. 53 min, SD 90.9), frequency shares, F tests and a logistic regression. B1 read the author's manuscript, not the ACM typeset.
- fix: none. "Means and SDs" is incomplete but not wrong.

## Group 15 — Roeser et al. 2024 (`roeser-rw24`)

### D-F2-18 — WORDING-FIX
- location: docs/references.md:59
- repo: "250 Dutch participants aged 18 to 25 fitted …; A two-component log-normal mixture fixed by assumption … LF bigrams fluent location 158 ms [139, 180] as the posterior mean of the back-transformed log location, disfluency slowdown 95 ms, disfluency probability 0.34; consonants 429 ms, 414 ms, 0.73; fluent spread 0.29 in both tasks"
- B1: "a random sample of 250 participants … age range of 18 to 25 years" from the Dutch copy-task corpus, with Eq. 7's two-component LogNormal mixture. Table 3 has β 158 [139, 180] | 429; δ 95 | 414; θ 0.34 | 0.73. "σ²e (fluent typing) 0.29 [0.27, 0.3] | 0.29 [0.26, 0.32]" sits under "Variance estimates" and is the variance term of the fluent LogNormal component. A "spread" read as an SD would be √0.29 ≈ 0.54. B1 did not read the OSF details (osf.io/y3p4d, 1,662 subjects, CC0).
- fix: "fluent-typing variance σ²e 0.29 (log scale) in both tasks".
