# Task 9.10 — Scenarios and timelines: scope card

Stage 1 of `_dev/research/jioh/research-slice-workflow.md`. Unit: each timeline's realism claims — task sets, co-occurrence, order, counts, typical durations, process names, scenario rows — not archetype values. Repository state: `b7894ab` on `jioh/dataset-rebuild`. Files: the 23 authored timelines and 5 variant recipes under `dataset/timelines/coreset/` (27 derived files are generated from them), the scenario catalog `docs/workload/scenario-catalog.md:12–29` whose `scenario:` tags the timelines carry, and the registry entries that ground scenario or timeline claims. Drawn from `../2026-09-13-verification/claims.md` (Part 1 scenario-side entries, the three timeline sections of Part 1/Part 2(b), Part 3), `compare/K2.md` (CpsMark+ and LAVD scenario rows), `compare/K3.md` (Game Mode, Steam, ananicy, DKMS), `compare/K4.md` (task switching, tabs), `compare/K5.md` (PCMark, SYSmark, Procyon, FOCAL, plain-text claims), `compiled-numbers-report.md` §1.6, §1.7, §2, §3.12–3.14, `meas-report.md` §4, the memo `docs/memos/2026-09-13-critical-findings.md` (B1, B6, B7, C, D), the phase spec's six added findings, and every hand-off to 9.10 in the six domain slices' changelogs and scope cards (`grep -n '9\.10' ../task-9.*/changelog.md ../task-9.*/scope-card.md`, 83 lines), with the manifest `dataset/build.manifest.json` for compiled demand.

Verdict vocabulary is the K files': SUPPORTED / WORDING-FIX / MISATTRIBUTED / CONTRADICTED / NOT IN SOURCE / OURS-UNDER-SOURCE-TAG / UNVERIFIABLE; "no source" where no citation is made. Kind is phase decision 1's labelling, applied to timeline content by decision 3: source claim / convention / arithmetic / placeholder / design. Under decision 3 the experiment's own interventions and calibration sizes (label flips, injections, renames, file length, `lane_share`) are design and carry no tag; they are listed in group K so the card is complete, and are not searched.

## Boundary

**In 9.10**

- Every realism claim in the timelines: which tasks a situation carries, which run together, in what order, how many, how long, under which names, and which catalog row (S1–S18) the segment claims.
- Counts that left the archetypes by the domain slices' decisions: game threads (9.4 D3), renderer counts as sites (9.8 D2, D25), `spawn_count` (9.6 D31), `total_work` of every finite job (9.6 D7, 9.7 D29(v)), a DKMS module's object count and run length (9.6 D6, D32).
- Placement of operations (9.5 follow-ups decisions 8–9; 9.5 D22): the GIMP filter, the Kdenlive preview render, the Chrome page load, and the Thunderbird `send` (9.7 D3, 9.5 D31, D37) — start, count, inside focus or not.
- Which state of a measured archetype a timeline depicts where a slice measured two: warm or cold (9.6 D5, 9.7 D8), first backup or repeat (9.7 D6), fresh install or update (9.7 D12), visible or hidden renderer (9.8 D4), idle or under traffic (9.8 D11), launch work or settled (9.5 D34).
- The scenario catalog's rows as timeline claims (their Processes and Taxonomy-source columns), and the registry entries that ground only scenario or timeline claims: `cpsmark-tbench23`, `pcmark10`, `sysmark30`, `sysmark25`, `procyon`, `gamemode-docs`, `steam-downloads`, `dkms-man`/`dkms-debian` (the C7 rename's premise), `zhang-chb15`, `gonzalez-chi04`, `mark-chi05`, `mark-chi08`, `mark-chi14`, `czerwinski-chi04`, `mark-gallup06`, `swell-icmi14`, `dubroy-chi10`, `chang-chi21`, `mozilla-testpilot10`, `singervine-slate10`, `focal-arxiv26`, `videogui-arxiv24`, and the plain-text claims C-plain-2…7.
- The binding (not the values) of `gnome-shell`, `Xorg`, `pipewire` in `c1-idle` (memo B6), and which of the five S18 names a file carries.

**Out of 9.10**

- Archetype values, tags and `modeling_notes`: the domain slices (9.4–9.9). Where a timeline question depends on a value still being decided, the item says which slice.
- To 9.11: whether simulated baselines honour a task's declared class (9.6 D17; the `tracker-miner-fs-3` `SCHED_IDLE` fact is recorded here only as a pair difference, item 32).
- To 9.12: related-work and proposal prose (the `updatedb` sentence, 9.6 D17; the `python3` wording, 9.6 D32), C-lavd-18/20, C-plain-7's use in the proposal's motivation.
- To 9.13: schema — an `operations` field and its compile path (9.5 D22), any declared-class field, the rebuild.
- To 9.14: the demand-window rule, the judging set and every compiled-number statement in consumer specs; this card lists compiled effects only as inputs.
- To 9.15: the docs' prose (`coreset-guide.md`, `building-plan.md`, `scenario-catalog.md` wording, `dataset/README.md:86`), including the stale "~5.7 ms" download sleep (`coreset-guide.md:205, :642`, memo C) and CpsMark+ Table 4 as support for "time-shared compositions" (`archetype-plan.md:69`, K2 C-cpsmark-6). The catalog rows' *content* is this slice's; their prose form is 9.15's.
- Slices still in decision sessions at this card's commit, which may add hand-offs after it: 9.5 (the Thunderbird re-observation with `send`, D31–D46), 9.7 (release upload after D34), 9.9 (session campaign, D8–D18: the display-server entry is open, D3). 9.4, 9.6 and 9.8 are closed.

## Items

Current values are read from the authored files at `b7894ab`; line numbers refer to that commit. "Compiled effect" is from the manifest (single set, `utilization`) or the audit where it still holds.

### A. Arc order and composition (source claims today)

| # | Item | Current | Tag / citation | Verdict | Kind today | Compiled effect |
|---|---|---|---|---|---|---|
| 1 | `c3-workday` order: browsing 0–60 s → office 60–120 s → compile 120–360 s → mail 360–420 s | `c3-workday.timeline.yaml:1–3, :9–16` | `cpsmark-tbench23` (comment) | WORDING-FIX (K2 C-cpsmark-5) — browsing → document → mail follows CpsMark+'s CA order (Chrome → PowerPoint → Word → Excel → Acrobat → WinRAR → Outlook, §4.3.4); the compile segment, the longest, has no CpsMark+ counterpart; CpsMark+ is a benchmark's scripted serial order, not observed user behaviour | source claim (3 of 4 stages) + design (compile) | segment boundaries; demand 4.84 (9.6 D31) |
| 2 | `c3-creation` order photo 0–120 s → video-edit 120–240 s → transcode 240–420 s, a "batch handoff" | `c3-creation.timeline.yaml:1–2, :8–13` | `cpsmark-tbench23` CC; `sysmark30` ACC (comment) | WORDING-FIX both — CC order Photoshop → AutoCAD → 3ds Max → Premiere → After Effects → HandBrake contains it as a subsequence, no output handoff stated (K2 C-cpsmark-12); SYSmark 30's guide gives the photo/video switch with no order, its whitepaper a Premiere encode backgrounded while Photoshop edits in front (K5 C-sysmark30-3) | source claim, partly design | demand 0.78 |
| 3 | `c3-evening` arc browsing → gaming (+ `discord`) → media | `c3-evening.timeline.yaml:1–2` | none | no source | design | demand 0.87 |
| 4 | Segment and file lengths: every C1 file 60 s; C2 120–180 s; C3 420 s; c6-dual 240 s | all files | none ("compressed event-time", building-plan §3) | no source; file length is design by decision 3 | design | every file |
| 5 | Focus windows: 2–58 s in every C1 base, 2 s after every segment start elsewhere; `c1-gaming`, `c1-media`, `c1-meeting`, `c1-idle` carry `focus: []`; `c3-creation` has none after 240 s | all files | none | no source; the stimulus replay cuts SWELL-KW per focus window (9.5 D18), the windows are 9.10's | design | the input stream of every focused task |
| 6 | Co-occurrence in `c1-office`: writer (focused) + browser + renderers 1 + 7 + `thunderbird` mail client | `c1-office.timeline.yaml:11–24` | S1+S2+S4 tags only | no source for the combination; 9.8 D9 hands on whether an office file holds a mail task at all | design presented as realism | demand 0.05 |
| 7 | `c1-media` plays a video (`mpv`) and music (`spotify`) at once | `c1-media.timeline.yaml:13–18` | S13 | no source for concurrent video and music | design presented as realism | demand 0.13; C5 inherits it |
| 8 | `c1-meeting` carries two `video-call` tasks (`zoom` "video" and "voice") for one call | `c1-meeting.timeline.yaml:16–21` | S3 | 9.5 D19 flag: the two tasks double one call measured as one loopback WebRTC call (9.5 D25); the helper task was retired (9.8 D8) | design error flagged | demand 0.22 |
| 9 | `c6-dual`: gaming while actively awaiting a compile, both foreground | `c6-dual.timeline.yaml:1–3` | S9+S11 | no source; shipped as a pre-committed ambiguity | design (resolution limit) | demand 1.26 |

### B. Gaming situation (hand-offs from 9.4, 9.7, 9.8)

| # | Item | Current | Tag / citation | Verdict | Kind today | Compiled effect |
|---|---|---|---|---|---|---|
| 10 | Number of game tasks and their names: the chain's members all named `game.exe`; no other game thread | `c1-gaming:13`, `c2-p2a:14`, `c3-evening:22`, `c6-dual:13` | C-plain-6 (S9 row "<game>.exe (Proton)") | WORDING-FIX (K5 C-plain-6) — only the process short name follows the executable (15-byte `comm`); threads named by the game or by Wine carry their own `comm`. 9.4 D3 removed `n_tasks` 300 (slide 12's figure counts every scheduled task incl. system tasks) and hands the count here with references: LAVD slide 12; scx #234 (95 pids in Apex Legends over 10.9 min, 18 game-named); scx #296 (108 pids in StarCraft II over 99 s, 41 `Play Main Threa`; 95 in Diablo III, 38 `Diablo III64.ex`) | count and names without source | `game.exe` × chain length (16) in 7 files |
| 11 | The Steam client runs beside every game | `steam` → `game-client` in `c1-gaming`, `c2-p2a`, `c3-evening` (+ derived) | S9 row | 9.8 D6: `game-client` is the desktop client logged out, not behind a game; whether a gaming timeline names a `steam` process at all, and in which state, is 9.10's. `steamwebhelper` ×3 no longer bound (9.8 D25) | design presented as realism | small (≈0.0001 lanes before 9.8) |
| 12 | A compositor `gamescope` runs beside the game | `c1-gaming:17` (+ c4, c7) → `video-player` | "(ours)" | no source for gamescope on a desktop session; `gamescope` not packaged on Ubuntu (meas-report §4); the `video-player` binding is 9.5's substitution (9.5 D11) | design | ≈0.40 lanes of `c1-gaming` before 9.5 |
| 13 | A voice-chat client beside a game: `discord`, task id `overlay` (`c3-evening:24`), `injected-overlay` (`c4.variant.yaml:9`) | `chat-client` | S5 row: "ananicy (comms class)"; "LAVD gaming context (companion apps observed alongside games)" | LAVD half NOT IN SOURCE (K2 C-lavd-16); ananicy half WORDING-FIX (type `Chat`, K3); the overlay role withdrawn — Discord's overlay is Windows-only (9.8 D7); the ids still name it | source claim failing | `c3-evening`, `c4-gaming` |
| 14 | Downloads continue while a game runs (`c2-p2a` segment 2, `background: download`, wanted) | `c2-p2a.timeline.yaml:10–11, :18–19` | `steam-downloads` (S10) | setting and default pause SUPPORTED (K3 C-steam-1, -2); "wanted/unwanted toggle" OURS-UNDER-SOURCE-TAG (C-steam-4); 9.7 D4/D34: the premise rests on Valve pages the 9.7 search could not read | source claim + our label | P2 pair's wanted side |
| 15 | The download runs under the name `steam` ("steam download workers") | `c2-p2a.timeline.yaml:1, :18` | none (S10 row) | NOT IN SOURCE (K3 C-steam-6) | name without source | recognizer-visible name of the P2 pair |
| 16 | The download's size and state: `total_work: 25s`, a fresh depot install (9.7 D12, D34) | `c2-p2a:19` | none | no source (Part 2(b)); an update phase exists only if 9.7's probe succeeded | design | cannot finish in the file (audit §1.6 for the old binding) |
| 17 | `lane_share` 0.9 / 0.95 / 1.45 / 0.6 | `c1-gaming:14`, `c2-p2a:15`, `c3-evening:23`, `c6-dual:14` | none | design by decision 3 | design (label, no tag) | chain demand per file |

### C. Browsing and renderers (hand-offs from 9.8)

| # | Item | Current | Tag / citation | Verdict | Kind today | Compiled effect |
|---|---|---|---|---|---|---|
| 18 | Renderer counts per file, now 1 visible + N − 1 hidden: 12 (`c1-browsing` and `c6-fold`, `c6-spoof`, `c7-browsing`), 8 (`c1-office`, `c3-workday` and derived), 10 (`c3-evening`), 6 (`c4-compile` injection) | `count:` fields | C-tabs-1 (`dubroy-chi10`, `mozilla-testpilot10`, `chang-chi21`) through prose only | OURS-UNDER-SOURCE-TAG (K4 C-tabs-1): the three sources give tab counts only; 6/8/10/12 coincide with four Chang figures, three of them not open-tab counts (K4 §2.2); C-plain-1 WORDING-FIX: under site-per-process a renderer is a site, not a tab, so a count is a count of sites (9.8 D2) | count without source | the number of identically named `chrome` tasks the recognizer sees |
| 19 | One window per browsing file; one visible renderer per window | `renderer-shown` ×1 in every chrome file | 9.8 D25 from `mozilla-testpilot10` event dump (82.9 % of logged states one window; Firefox 3.5–4.0 beta, Nov. 2010) | stated there as a use pattern; files depicting several windows handed here | source claim (9.8's reading) | as 18 |
| 20 | The focused page's renderer: described by no entry; in browsing files the one visible renderer stands for it (9.8 D25) | — | — | open (9.8 hand-off) | gap | browsing files |
| 21 | Tab-count registry lines, which ground only the counts | `sources.yaml` / `references.md` entries | — | C-dubroy-2 NOT IN SOURCE ("2009", "single-process"); C-testpilot-1/2/3 MISATTRIBUTED (Slate's statistics); C-testpilot-4 CONTRADICTED (event dumps survive in the Wayback Machine); C-testpilot-5 NOT IN SOURCE; Chang "fatter modern tail" OURS-UNDER-SOURCE-TAG; `chang-chi21` never read against its primary text (memo D; ACM DL 403; article number UNVERIFIABLE) | registry | none directly |
| 22 | VS Code's helper processes as named tasks | not carried; one `code` task holds the tree (9.5 D14) | — | open (9.5 D14 hand-off): recognition realism of the name multiset | design | `code` files |

### D. Mail and operations (hand-offs from 9.5, 9.7, 9.8)

| # | Item | Current | Tag / citation | Verdict | Kind today | Compiled effect |
|---|---|---|---|---|---|---|
| 23 | A separate `thunderbird` send task on `network-bulk`, `total_work: 3s`, arriving 40 s (`c1-mail`, `c7-mail`) and 400 s (`c3-workday`) | `c1-mail.timeline.yaml:17–18`, `c3-workday:31–32` | none | 9.7 D3, D30: the send becomes an operation of `mail-client` placed by the timeline; the separate task is dropped; `network-bulk` leaves with it, before 9.13 | design pending replacement | `network-bulk` survives in the library only for these three |
| 24 | `thunderbird`'s bindings and roles: `mail-client` (c1-mail, c1-office, c3-workday and derived) and `network-bulk` (the three send tasks) | — | — | 9.5 follow-ups spec open item: each non-identity binding needs a stated role; 9.8 D9 collapsed the `electron-comms` three onto `mail-client`; the `network-bulk` three remain (item 23) | design | — |
| 25 | Operation placement: GIMP filter, Kdenlive preview render, Chrome page load, Thunderbird send — start, count, whether inside focus | no timeline places one | — | open (9.5 D22, spec decisions 8–9; 9.7 D3) | design / realism claim once placed | no compiled stream changes until placed (9.5 D25) |
| 26 | Launch work of an application that starts mid-run (`c3-workday` writer 60 s, mailer 360 s; `c3-creation` kdenlive 120 s; `c3-evening` game, steam, discord 60 s, mpv, spotify 300 s; C4 injections at 30 s) | not modelled; every archetype reads its settled phase (9.5 D34) | — | open (9.5 D34 hand-off) | gap | every arriving interactive task |

### E. Compile and batch jobs (hand-offs from 9.6, 9.7)

| # | Item | Current | Tag / citation | Verdict | Kind today | Compiled effect |
|---|---|---|---|---|---|---|
| 27 | `spawn_count` 100 (`c1-compile`, `c7-compile`), 4 200 (`c3-workday`), 85 (`c6-dual`); `parallelism_cap: 8` | `c1-compile:15`, `c3-workday:28`, `c6-dual:18` | none | no source (Part 2(b)); sized against the old per-entry cost of one ≈89 ms process, now one job of six processes ≈471 ms (9.6 D31, "hands to 9.10") | design | `c3-workday` 0.86 → 4.84; compile files 0.15 → 0.93 |
| 28 | The child's name: `child_name: cc1` | as 27 | none | 9.6 D2: a child is a job of six roles (`sh` → `gcc` → `cc1`, `as`, `objtool`, `fixdep`, `rm`); the names follow the chain, subject to availability (`cc1` seen on Ubuntu and Fedora, `gcc` on Arch; `make` only on Ubuntu, meas-report §4) | name | recognizer-visible names |
| 29 | The build's situation: warm or cold tree (9.6 D5) | archetype reads warm `-j8` | — | open: which situation a timeline depicts is 9.10's | design | compile files |
| 30 | `c7-compile`: `make` → `dkms`, `background_wanted: false`, `initiated: scheduled`, same 100 children and cap 8 | `c7.variant.yaml:127–132` | `dkms-man`, `dkms-debian`, `meas-ci:names:2` (comment) | mechanism SUPPORTED (K3 C-dkms-man-2); C-dkms-debian-1 WORDING-FIX; C-dkms-debian-2 NOT IN SOURCE; 9.6 D6/D32: a real module's object count and run duration are unobserved (the campaign's structural check ran three objects at `-j1`); the count, the cap and the parent `dkms` process are 9.10's | source claim + design | identical to `c1-compile` in every build event |
| 31 | `total_work` of every finite job: `python3` 30 / 130 s; `ffmpeg` 30 / 75 s; `HandBrakeCLI` 30 / 320 s; `tracker-miner-fs-3` 30 s; `clamscan` 25 / 60 s (×11); `borg` 30 / 75 s; `7z` 6 s; spoof `chrome` 30 s | per file (Part 2(b)) | none; C1 comments "resized … (turnaround term)" | no source; the audit found the "sized to finish" rule WRONG for `c1-backup` (132 s alone) and infeasible for `c1-ml-train`, `c1-transcode` beside the editor (compiled-numbers §1.6 D2) | design presented as realistic job sizes | every batch file |
| 32 | The P1 pair: `c2-p1b` renames `python3` → `tracker-miner-fs-3` and keeps `python3`'s tables; the real indexer declares `SCHED_IDLE`, nice 19 | `c2-pairs.variant.yaml:8–13` | none | 9.6 D16, D17, D21: keep the name on `python3`'s shape as a spoof by construction, or take the rescan's own tables — 9.10's; the declared-class difference is recorded for the pair and the indexing files (`c1-indexing`, `c7-indexing`) | design | P1 identical apart from name (its guard) |
| 33 | `c1-ml-train` (id, mode `ml-train`, S12) binds a stand-in: a loop training on synthetic images, no data read, no checkpoint (9.6 D32) | `c1-ml-train`, `c7-ml-train`, `c2-p1a` | S12 row: `procyon`; "SchedCP … desktop-class machines" | Procyon grounds local inference only, no training (K5); C-schedcp-3 NOT IN SOURCE (9.6 card); 9.6 D32: the id claims more than the stand-in supports | name/label over a stand-in | three files |
| 34 | Backup situation: `borg` reads a first backup into a new repository over a cached set (9.7 D6, D8) | c1-backup, c7-backup, c2-p3b | S15 row: ananicy (WORDING-FIX), SYSmark 30 "archiving analogue" (OURS-UNDER-SOURCE-TAG, K5) | open: a routine periodic backup would need the repeat phase (9.7 D6), a run over files not recently read the cold figures (9.7 D8) | design | backup files |
| 35 | An everyday indexer in the background | none (retired, 9.7 D5); S14 files show the full rescan only | S14 row | 9.7 D5: a timeline that is to show one gets an archetype from its own measurement | gap | — |

### F. Background-work realism and C7 counterparts

| # | Item | Current | Tag / citation | Verdict | Kind today | Compiled effect |
|---|---|---|---|---|---|---|
| 36 | `clamscan` as the stock unwanted background scan in `c2-p2b` and the ten interactive C7 files, arriving at 0 s with `total_work` equal to the segment | `c2-pairs.variant.yaml:18–26`, `c7.variant.yaml:30–121` | S17 row: "ananicy (AV/scan class)"; "ClamAV stock scheduled-scan deployment pattern" | NOT IN SOURCE (K3 C-ananicy-rules-7: no such type, `clamscan` and `freshclam` have no entry) and CONTRADICTED (K5 C-plain-2: no ClamAV package examined ships a scheduled scan; the stock background job is `freshclam`); arrival and size are design (decision 3) | source claim failing + design | +1.00 lane in every interactive C7 file; `c7-gaming` 2.03 |
| 37 | No distro or vendor runs an unasked ml-train, render, transcode or backup under a distinct name → those four C7 files ship as label-flip-only pre-committed misses | `c7.variant.yaml:19–22` | C-plain-4, C-plain-5 (no id) | C-plain-5 CONTRADICTED for backup (Debian's Essential `dpkg` enables `dpkg-db-backup.timer`, K5); holds for the others within the searched scope; C-plain-4 (Jellyfin runs `ffmpeg`) SUPPORTED as naming, but Plex ships `Plex Transcoder` and Jellyfin runs no unasked transcode (K5) | negative existence claim | four files' labels |
| 38 | Indexer names: `tracker-miner-fs-3` (c1-indexing, c7-indexing, c2-p1b, c5-t3), `baloo_file` (c5-t3) | names | S14 row: "shipped defaults (GNOME tracker-miner, KDE baloo, plocate timers)" | WORDING-FIX (K5 C-plain-3): `tracker-miner-fs-3` up to Tracker Miners 3.7, `localsearch-3` from 3.8; `comm` shows `tracker-miner-f`; plocate not in a default install; `updatedb` not `updatedb.plocate` (meas-report §4); binary absent on Arch | name | recognizer-visible names |

### G. Session baseline (hand-offs from 9.9, memo B6)

| # | Item | Current | Tag / citation | Verdict | Kind today | Compiled effect |
|---|---|---|---|---|---|---|
| 39 | `c1-idle` (and `c7-idle`) carries five tasks: `gnome-shell`, `Xorg`, `pipewire`, `systemd`, `dbus-daemon`, all on `system-daemon` | `c1-idle.timeline.yaml:10–20` | S18 row: "Canonicalization [system] scope (Q7); interbench 'None/X' baseline; present in every segment by construction" | memo B6: the three session processes bound to server-daemon values, unmarked; 9.9 D1: they rebind once the session entries exist; S18's "present in every segment by construction" is false — only `c1-idle` and `c7-idle` carry them (9.9 card); interbench "None/X" is taxonomy only (C-interbench-10) | binding + source claim | `c1-idle` 0.0004 |
| 40 | Which session processes and names a stock desktop runs: `Xorg` on a Wayland session (Xwayland or nothing), `dbus-daemon` vs `dbus-broker`, the session bus beside the system bus, `systemd --user` beside pid 1, `pipewire` with `wireplumber` and `pipewire-pulse` | names | none | 9.9 D4, D6, D7: one task stands for the three PipeWire services, both buses, both managers; D3 display server open; other always-on services (journald, udevd, logind, NetworkManager) appear in no file and take their own entry if carried (9.9 D5) | names without source | idle files |
| 41 | A desktop in use or just left: not described by 9.9's terminal-idle entries (9.9 D9) | every file with S18 names | — | open (9.9 D9 hand-off) | gap | — |

### H. Scenario catalog rows (Taxonomy-source column, as timeline claims)

Rows judged against the K files; SUPPORTED cells are omitted.

| # | Row | Cell | Verdict |
|---|---|---|---|
| 42 | S3 video conferencing | PCMark 10 Essentials (Video Conferencing) | SUPPORTED (K5); the row's processes `zoom` · `teams-for-linux` unsourced |
| 43 | S5 voice chat companion | ananicy comms class; LAVD companion apps | WORDING-FIX; NOT IN SOURCE (items 13) |
| 44 | S8 batch transcode | CpsMark+ "HandBrake CLI 1.3.0 — verbatim, cross-platform" | WORDING-FIX (K2 C-cpsmark-4) |
| 45 | S9 gaming | PCMark 10 Gaming; Game Mode; LAVD; ananicy Proton vs native | Gaming group is a windowed Fire Strike test, Extended only (K5); Game Mode SUPPORTED as a category; ananicy WORDING-FIX (directories, both `Game`); `<game>.exe` WORDING-FIX (item 10); names `steam`, `steamwebhelper`, `gamescope`, `wineserver` present in the ananicy catalogue (K3) |
| 46 | S10 game download | Steam setting; ananicy download class | items 14–15; ananicy WORDING-FIX |
| 47 | S11 dev + compile | SYSmark 25 "adds software development"; "kernel-build characterization (2,430 short-lived procs, arXiv 1705.05937)"; interbench Compile; SchedCP; dkms | WORDING-FIX (SYSmark 2018 already had it, SYSmark 30 dropped it, no compiler named, K5); MISATTRIBUTED (a DynamoRio build, memo A1); interbench SUPPORTED as an emulation; dkms item 30 |
| 48 | S12 ML training / local AI | UL Procyon; SchedCP desktop-class | inference only (K5); NOT IN SOURCE (item 33) |
| 49 | S13 media playback | PCMark 10 Battery Video profile; interbench Audio + Video; ananicy audio class (nice −11) | WORDING-FIX (Battery Life Profile, Video scenario, Professional Edition); MISATTRIBUTED (nice −11 was audio-server rules 2022–2025; `Player-Audio` is −4 at the pin, K3) |
| 50 | S14 file indexing | ananicy ioclass-idle indexer class; shipped defaults | WORDING-FIX (no indexer type; baloo is `BG_CPUIO`); item 38 |
| 51 | S15 backup / sync | ananicy backup class; SYSmark 30 archiving analogue | WORDING-FIX; OURS-UNDER-SOURCE-TAG |
| 52 | S16 archive burst | SYSmark 30; CpsMark+ WinRAR; SchedCP | SUPPORTED, but no timeline carries an S16 tag; `c4-office` injects `7z` untagged |
| 53 | S17 malware scan | ananicy AV/scan class; ClamAV scheduled-scan pattern | NOT IN SOURCE; CONTRADICTED (item 36) |
| 54 | S18 system baseline | Q7 scope; interbench None/X; "present in every segment by construction" | item 39 |
| 55 | All rows — "the grounding sources attest to process names" (`scenario-catalog.md:5`) | CpsMark+ Table 2, SYSmark lists | WORDING-FIX (K2 C-cpsmark-3, K5 C-sysmark30-4): they list application products and versions, not process names; the Linux names are the project's mapping (`sources.yaml:95–96`) |
| 56 | Catalog coverage note (`:33`) | "PCMark 10's three groups…", S15 omitted from SYSmark mapping | WORDING-FIX (K5 C-pcmark-1/4) |

### I. Task-switching and focus sources (ground the planned generator; candidates for items 4–5)

| # | Item | Verdict |
|---|---|---|
| 57 | `zhang-chb15` — power-law switching on hub tasks; ~3 min average switch | UNVERIFIABLE (no copy reachable, K4) |
| 58 | `gonzalez-chi04` — ~12 min per working sphere; ~3 min per task; ~2 min 11 s per tool | WORDING-FIX: a mean continuous *segment* in a sphere (Avg. Time/WS 33 min 32 s); 3 min 08 s per *event*, shadowing, meetings excluded (K4) |
| 59 | `mark-chi05` — ~11 min per sphere; internal vs external interruptions | WORDING-FIX (managers 59.2 % *external*; printed overall split conflicts with Table 3) |
| 60 | `czerwinski-chi04`, `mark-chi08`, `mark-chi14`, `mark-gallup06` | WORDING-FIX where cited as distributions or as "only source" (K4) |
| 61 | `swell-icmi14` — SWELL-KW computer logging | access CONTRADICTED (open, CC BY-NC-SA 4.0); 25 students and interns in a lab, Windows; raw uLog `Window Activated` events with application names (K4); 9.5 H1 hands it here as a source of focus sequences and durations (~3 h per participant) |
| 62 | `focal-arxiv26` / `videogui-arxiv24` — A→B→A interruption sessions; 320 multitask sessions | WORDING-FIX (B is a labelled task switch, not a distractor); no real inter-action timings (6.0 s fixed, K5); app names VLM-generated display names |
| 63 | C-plain-7 — "no public trace of desktop process timelines with process names exists" | WORDING-FIX (K5): DARPA OpTC publishes executable paths for process-create events on Windows 10 endpoints; BEHACOM publishes foreground executable names from natural use |

### J. Findings from the phase spec's six additions that touch timelines

| # | Finding | Where it lands |
|---|---|---|
| 64 | The "~5.7 ms" download sleep matches no version of `archetypes.yaml` | prose (9.15); the binding itself is now `game-download` (9.7 D34) — recorded, not searched |
| 65 | CpsMark+ contradicts "time-shared compositions" (S6/S7 as interactive + batch) | the composition of the creative files (items 2, 34) is 9.10's; the prose is 9.15's |
| 66 | `chang-chi21` details unread | item 21 |

### K. Design by decision 3 (labelled, not searched)

| # | Item | Where |
|---|---|---|
| 67 | Label flips and attributes (`background_wanted`, `initiated`, `pre_committed_miss`, `dual_active`, `spoof`, `familiarity`) | all segment attributes |
| 68 | Renames (C2 P1, C5 tiers, C7 `make → dkms`) and invented names (`video-playback-svc`, `audio-stream-helper`, `qzvd`, `xkrr`) | `c2-pairs`, `c5`, `c7` variants |
| 69 | Injections and their times (C4 at 30 s; C7 at 0 s; `c6-spoof` at 20 s) | `c4`, `c6`, `c7` variants |
| 70 | `lane_share` (item 17), file lengths (item 4), seeds 101–116, 201–203, 301–303, 601 | all files |

## What the source is, as one observation

No single observation covers the coreset, and none is claimed. Today the timelines cite five kinds of document, none an observation of the situation they depict:

- Benchmark designs (CpsMark+, SYSmark 30/25, PCMark 10, Procyon): each fixes a scripted workload order or list on Windows; they attest that a situation is a benchmark category and, for CpsMark+, a serial order. They are not observations of users.
- Vendor documentation (Steam support pages, Microsoft Game Mode, dkms(8)): attest a setting or mechanism, not how often or with what else it runs.
- A package catalogue (`ananicy-rules`): attests names and priority treatments, not co-occurrence.
- Human-behaviour studies (González & Mark, Mark, Zhang, Czerwinski; Dubroy; Chang; Test Pilot): each one population, on Windows desktops or Firefox, observed or self-reported — tasks and tabs, not processes. Several were read only through other documents' statistics (Test Pilot through Slate, Zhang not at all).
- One dataset with logged application focus: SWELL-KW (25 people, one lab session each of ~3 h, Windows, 2012–2014). One observation for focus sequences in knowledge work; it carries no gaming, media, compile or background jobs.

Under decision 3 each situation (office, browsing, mail, compile, gaming, media, meeting, idle session, each background job) needs its own observation for its task set, co-occurrence, order, counts and names. The domain slices' own campaigns (9.5–9.9) are observations of one application at a time on a runner, not of a desktop's composition. Stage 2 therefore searches per situation; stage 3's first question is whether any found observation can ground more than one situation, and whether a user-behaviour observation on another platform may ground a situation (issue rule; recorded, not excluded).

## Stage 2 topics

Neutral form, for the readers: what to find, never the repository's current value. Each is searched in the four classes of phase decision 4.

- **T1 Application co-occurrence.** Logged or traced observations of which applications and processes run at the same time on real desktop computers (any OS; Linux preferred), per activity where available: how many applications are open, which combinations occur during office work, browsing, email, software development, gaming, media playback and video calls, and what runs in the background during them. Record population, OS, year, logging method, and whether process names are given.
- **T2 Focus and switching.** Observations of foreground-application sequences: dwell time per application or window, switch rates, sequences across applications, and session lengths, with distributions where published; logged data sets that contain window-activation or focus events with application names and timestamps.
- **T3 Activity order.** Observations or documented workflow definitions of the order in which desktop activities follow one another in a session (e.g. searching, writing, building software, sending mail; editing photos, editing video, exporting) — including benchmark suites' own workload orders, and whether any observation of real users supports an order.
- **T4 Browser windows, tabs and processes.** Logged numbers of browser windows, tabs and distinct sites per session; how many renderer processes Chromium-based browsers run on Linux for a given set of tabs and sites (documentation, source, measurements); how often a user loads a page or switches tabs per minute of browsing.
- **T5 Gaming session composition on Linux.** What processes run on a Linux desktop while a game runs through Steam (native or Proton): the Steam client and its helpers and their state, a compositor (gamescope or the desktop's), overlays, voice chat clients available on Linux; the number and names of a Proton game's processes and threads; whether and how the Steam client downloads or updates while a game is running on Linux (defaults, documentation, observations).
- **T6 Unrequested background jobs on stock Linux desktops.** What distributions and desktop environments start without the user: timers and services enabled by default (antivirus scans, database updates, indexers, `updatedb`, package-database backups, update checks, DKMS rebuilds on kernel updates), their process names by distribution and version, how often they run and for how long; for DKMS, how many objects a typical out-of-tree module (e.g. a GPU or VirtualBox module) compiles and how long an autoinstall takes.
- **T7 Size of user-started jobs.** Observed or documented typical sizes and durations of batch work users start on desktops: builds of a project (objects per build, build times), video render and transcode lengths, backup runs (first vs incremental, data sizes), archive creation, ML training jobs on a desktop CPU; and the relation of a build's size to a kernel build.
- **T8 Session baseline.** Which session and system processes a stock desktop runs at idle and in use, by distribution and session type (GNOME/KDE, Wayland/X11): display server presence, compositor, audio stack processes, bus implementation and instances, per-user service manager, other always-on services — names as they appear in `comm`.
- **T9 Operations within applications.** How often users perform heavy operations inside an application — applying an image filter, rendering a video-editor preview, loading a web page, sending an email with or without attachment — per minute or per session of use, and whether they occur while the user is interacting or idle.
- **T10 Application launches within a session.** How often applications are started during a session and how long launch work takes on Linux (CPU and wall time until settled).
- **T11 Video calls and media.** Process structure of Linux video-conferencing clients during a call; whether users play music and video concurrently, or media alongside other work.
- **T12 Public traces of desktop process activity.** Public data sets or traces recording desktop process creation, execution or foreground state with process names and timestamps (any OS), their population, time span, licence and access; including security telemetry sets, HCI logging sets, energy/mobile data sets that record several running applications.
- **T13 CI observability.** What a GitHub Actions hosted runner can observe of a desktop situation: running a full desktop session (GNOME/KDE under Xvfb, headless, nested) and listing the processes and default timers it starts; listing the default-enabled timers and services of distribution images (Ubuntu, Fedora, Arch containers or VMs); building a real DKMS module and counting its objects; what it cannot observe (real users, real GPUs and displays, real game sessions, a logged-in Steam client).

## Compiled numbers the decisions move

From `dataset/build.manifest.json` at `b7894ab` (single set, `utilization`): C1 bases backup 0.57, browsing 0.02, compile 0.93, dev 0.38, gaming 1.03, idle 0.0004, indexing 0.59, mail 0.06, media 0.13, meeting 0.22, ml-train 0.59, office 0.05, photo 0.00, render 0.55, transcode 0.56, video-edit 0.06; C2 p1a/p1b 1.19, p2a/p2b 1.17, p3a/p3b 0.69; C3 creation 0.78, evening 0.87, workday 4.84; C4 compile 0.93, gaming 1.03, office 0.15; C5 0.13; C6 dual 1.26, fold 0.02, spoof 0.52; C7 interactive counterparts +1.00 each (clamscan), gaming 2.03.

What the items move: `spawn_count` (item 27) moves `c3-workday`, the compile files and `c6-dual`; every `total_work` (item 31) moves the batch files and whether a job finishes (turnaround term); the C7 scan (item 36) sets the +1.00 lane of ten files; renderer counts (item 18) move browsing and office files slightly and the recognizer's name multiset strongly; game task count (item 10) and the Steam/compositor/chat tasks (items 11–13) move the gaming files; operation placement (item 25) and launch work (item 26) add CPU to focused and arriving tasks where none is today; `c1-idle`'s rebinding (item 39) waits on 9.9's values. These are 9.14's inputs once 9.10's decisions land.
