# Work-list rows — `docs/workload/archetype-plan.md`

Chunk K04, Dataset README, archetype plan and licences (wave 1). 13 open rows. The file has 88 lines at `d5cc7711`.

### W-0226 · applied · full pass
- At: `docs/workload/archetype-plan.md` the whole file (§1–§6)
- Change: Full pass against the code: check every statement about the dataset in the whole file (§1–§6) against `dataset/` (the timelines, `archetypes.yaml`, the manifests, `coverage-grid.json`, the tools) and correct what is stale; each correction not already a row is logged as a new row in the chunk log.
- Final word: 9.15 spec decision 4: the docs that explain the dataset — `docs/workload/`, `dataset/README.md`, `docs/data-contracts.md`, the harness guide's records and dataset chapters — get a full pass against the code; staleness an agent notices outside its rows becomes a new row. Precedence by decision 3: the code and data as they stand (`dataset/`, `harness/`, `simulator/`, the committed manifests) first.
- Sources: 9.15 spec decision 4 (`jioh/task-9.15-docs-memos-and-guidebook-corrections.md:30`)
- Notes: —

### W-0227 · applied
- At: `docs/workload/archetype-plan.md` §1 What an archetype is: item 1 line 23 (interbench's "wakes every 50 ms, needs 5% CPU" example) and item 3 line 25 ("`desktop-interactive` has no full behavioral referee"); §4 Periodic-interactive family lines 46–49; Spanning check line 69
- Change: Replace §1's interbench example with one taken from a measured entry and line 25's `desktop-interactive` limit with the measured entries' referee; replace §4's three interbench-harvested entries (`audio-playback`, `video-playback`, `desktop-interactive` with its `dhakal-chi18`/`roeser-rw24` input-gap grounding) by the nine measured per-application entries `office-writer`, `code-editor`, `mail-client`, `web-browser`, `image-editor`, `video-editor`, `video-player`, `audio-player`, `video-call` (`category_source: meas`); restate the spanning check without "these 12" and without creative apps as `desktop-interactive` + `cpu-batch`.
- Final word: 9.5 D2 (the desktop-interactive entry split per application) and D19 (the fold-in), superseded by D25 and then D70 (the nine entries regenerated whole from the same-machine campaigns `meas-ci:interactive:2026-09-18/19/20` and `meas-ci:playback:2026-09-18/20`): the nine measured per-application entries replace `desktop-interactive`, `audio-playback` and `video-playback`. 9.5 D7 as amended by D23: `dhakal-chi18` and `roeser-rw24` ground no dataset value, `dhakal-chi18` only the stimulus-sensitivity check's alternate stream; the interactive values come from the measured campaigns under the SWELL-KW streams (9.5 D4, D18). 9.5 D11: interbench's Audio/Video/X emulations are no longer cited.
- Sources: SX-0396 (9.5 scope card, Out of 9.5 (To 9.15), `task-9.5-interactive-typing/scope-card.md:26`); SX-0413 (9.5 D19, `task-9.5-interactive-typing/changelog.md:110`); SX-0422 (9.5 D25, `task-9.5-interactive-typing/changelog.md:160`); SX-0406 (9.5 D7, `task-9.5-interactive-typing/changelog.md:37`)
- Cross-ref: W-0231
- Notes: SX-0422 (9.5 D25) duplicates the 9.5 D19 row. The interactive entries' compiled form at HEAD: per-thread components, a replayed SWELL-KW input stream for the four typing applications, operations and rare events (dataset/archetypes.yaml office-writer…video-call). The whole §4 restatement is W-0231; the editing agent may fold this row into it.

### W-0228 · applied
- At: `docs/workload/archetype-plan.md` §2 Two-tier grounding, "Tier 1 — existence of each archetype: closed by harvesting", line 31
- Change: Restate Tier 1: each entry's existence is grounded by the program its campaign measured (`category_source: meas`, a behaviour class observed in our measurement of a named program) for 28 of the library's 29 entries, a published taxonomy surviving only for `game-task-chain` (`lavd-ossna24`); drop the harvest from interbench's menus, the kernel-build literature and `ananicy-rules`' `type` field ("literally a community-maintained archetype taxonomy", with its nonexistent `Player` type), and the sentence "Three entries (network-bulk, electron-comms, system-daemon) have no literature taxonomy".
- Final word: 9.5 D19 → D25 → D70 (the nine measured entries carry `category_source: meas`), extended the same way by 9.6–9.10: at HEAD 28 of the 29 entries carry `category_source: meas` and `game-task-chain` keeps `lavd-ossna24` (dataset/archetypes.yaml). Scope-card items 66, 68 and 69 of 9.12 (the 9.7, 9.8 and 9.9 hand-offs, passed through by 9.12 D47): K3 (a comparison report of the 2026-09-13 claim verification) C-ananicy-rules-1, OURS-UNDER-SOURCE-TAG — the `ananicy-rules` types are priority-treatment profiles, not a behaviour class or archetype taxonomy, and `Player` does not exist; the critical-findings memo's A5 (docs/memos/2026-09-13-critical-findings.md:15, :103): the types group by prescription and the harvest rule was applied unevenly.
- Sources: SX-0007 (TODO 9.15 line (from 9.5), `_dev/TODO.md:179`); S12-218 (9.12 D47, `task-9.12-related-work-prose/changelog.md:748`)
- Cross-ref: W-0229; W-0231; W-0235; W-0236; W-0237
- Notes: S12-218 is the items-66/68/69 pass-through over :31, :40, :56–58, :64–66, :85; its other lines are carried by W-0230 (:40), W-0232 (:57), W-0233 (:58), W-0235 (:64), W-0236 (:65, :85) and W-0237 (:66). The kernel-build harvest phrase in this sentence is item 63's (W-0229); restating the sentence covers it. Verified: 29 keys under `archetypes`, 28 `category_source: meas`, `game-task-chain` `lavd-ossna24`; `game-download-idle` reuses `game-download`'s tables under `declared_class: idle`.

### W-0229 · applied
- At: `docs/workload/archetype-plan.md` §2 line 31 (the kernel-build literature's compile fork-burst, restated with W-0228); §3 Emergent multiplicity line 39 ("Parallelism cap: `-j8` by stated convention"); §4 Compute/batch family lines 51–54 (`cpu-batch`, `compiler-child`, `build-orchestrator`); §6 OQ-4 line 86
- Change: Restate the three entries to their measured form, each `category_source: meas`: `compiler-child` the six-member object job (`sh`, `gcc`, `cc1`, `as`, `fixdep`, `rm`) with one quantile table per (role, structural step), `build-orchestrator` the measured `dispatch_overhead` table with six spawn-table entries per object job and `fork_cap` = `parallelism_cap` × 6, `cpu-batch` a batch loop over the bound program's measured runs and blocks (`python3` and `kdenlive_render`); drop the interbench Burn and `ananicy-rules` `Heavy_CPU` category source, the `ocallahan-atc17` 2,430-process kernel-build attribution (a DynamoRio 6.1.0 build) and its interbench-Compile cross-confirmation, `meas-pending`, and the consumers list naming `clamscan`.
- Final word: 9.6 D19–D22 and D25 (D19 amended by D20, D22 corrected by D25; folded in at D31), with D2: `compiler-child` is the six-member object job with (role, step) tables tagged `meas-ci:build:2026-09-18`; `build-orchestrator` carries `dispatch_overhead` and six spawn-table entries per job, the compiled `fork_cap` = parallelism_cap × 6 (dataset/tools/wlc/compiler.py:699); `cpu-batch` is a batch loop (RUN a measured run, SLEEP the block after it) whose tables the `program` binding chooses (dataset/archetypes.yaml:884); all three `category_source: meas`, no `meas-pending`. 9.6 D4: `parallelism_cap` 8 is the `nproc` convention on an eight-thread desktop; 9.6 D37: the DKMS job has seven members (`objtool` too). 9.12 D103 (item 63 of its scope card, 9.6's verdicts): K1 (a comparison report of the 2026-09-13 claim verification) C-ocallahan-1 MISATTRIBUTED — O'Callahan et al.'s 2,430 mostly short-lived processes are a DynamoRio build, cited for the class's existence and short-lived character only; C-interbench-9 CONTRADICTED — interbench's Compile load runs three threads in one process and forks none. 9.10 D3: no timeline binds `clamscan`; the C7 counterparts' unwanted job is `package-upgrade` (`unattended-upgr`).
- Sources: SX-0021 (TODO 9.15 line (from 9.6, the three archetypes), `_dev/TODO.md:179`); SX-0434 (9.6 scope card, Out of 9.6 (To 9.15), `task-9.6-compile/scope-card.md:38`); SX-1120 (guidebook dataset vol-08 ch.12 §12.8 mismatch table row 7, `dataset/08-decision-chronicle.md:1857`); SX-0167 (TODO 9.15 line (from 9.12 audit D103), `_dev/TODO.md:179`); S12-223 (9.12 D103, `task-9.12-related-work-prose/changelog.md:1559`)
- Cross-ref: W-0228; W-0231
- Notes: At HEAD `c1-compile` binds 2,908 object jobs at `parallelism_cap: 8` (dataset/timelines/coreset/c1-compile.timeline.yaml:19–20); `cpu-batch`'s tables are `python3` and `kdenlive_render` only. The label on :39 and :86 ("by stated convention") waits on the for-인지오 row on record-gaps §1 item 4 (W-0767): 9.6 D4 and `build-orchestrator`'s `modeling_notes` say convention, `c1-compile.timeline.yaml:20`'s source map says `parallelism_cap: design`. OQ-4's "between interbench's documented `-j4`" leans on interbench, which grounds no dataset value since 9.5 D11.

### W-0230 · applied
- At: `docs/workload/archetype-plan.md` §3 Multiplicity, Static multiplicity bullet, line 40
- Change: Keep "binding-time parameters with a source tag" (now true: each bound value of a timeline carries a `source:` entry) and replace the named grounds: drop "discord helpers" and the tab-count literature (`dubroy-chi10`, `mozilla-testpilot10`, `chang-chi21`, "defined against the Chromium process model"), and name the hidden tabs' renderer count's sources, `glam` and `meas-ci:desktop:2026-10-04` (the Chrome tab-set campaign).
- Final word: 9.10 D32 with 9.18 D2 (the field and its lint landed): each bound value of a timeline — count, spawn_count, parallelism_cap, total_work, lane_share, member_names, the bound program — carries a `source:` entry (a registry tag, a list of tags, or design / convention / arithmetic), linted against dataset/sources.yaml; the renderer count's sources are `glam` and `meas-ci:desktop:2026-10-04`. 9.12 D102 under 9.10 D34: `dubroy-chi10`, `chang-chi21` and `mozilla-testpilot10` (with `dkms-man`, `dkms-debian`) leave docs/references.md and the lines citing them are restated in the same edit. Item 68 of 9.12's scope card (9.8): K4 MISATTRIBUTED on the tab-study multiplicity.
- Sources: S12-270 (9.12 D102, `task-9.12-related-work-prose/changelog.md:1545`); S10-073 (9.10 D32, `task-9.10-scenarios-timelines/changelog.md:677`); SX-0173 (TODO 9.15 line (from 9.12 audit D102), `_dev/TODO.md:179`); SX-0329 (TODO 9.15 line (from 9.18 D2), `_dev/TODO.md:179`)
- Cross-ref: W-0228
- Notes: Code: dataset/timelines/coreset/c1-browsing.timeline.yaml:20–21 `count: 4, source: {count: [glam, "meas-ci:desktop:2026-10-04"]}`. The three entries are still in docs/references.md (:80, :85, :295) and dataset/sources.yaml (:210, :217, :225) at HEAD; their removal is the references chunk's (a references removal of an id still in the registry fails `make lint`, dataset/tools/wlc/linter.py:36–42).

### W-0231 · applied
- At: `docs/workload/archetype-plan.md` header line 2 (Updated 2026-09-10); §4 The inventory (12 entries), lines 44–70; §6 Open questions — resolutions, lines 81–88 (OQ-2 line 84: "S3 stays bound to `video-playback`")
- Change: Replace the twelve-entry inventory with the library as it stands — 29 entries in dataset/archetypes.yaml, 28 measured (`category_source: meas`) and `game-task-chain` the one literature-grounded entry — keeping §1–§3 and §5–§6's rules, and check §6's resolutions against the measured library (OQ-2: meetings bind the measured `video-call`); bump `Updated`.
- Final word: The library rebuilt in Phase 9: 29 entries in dataset/archetypes.yaml, 28 with `category_source: meas` and `game-task-chain` from `lavd-ossna24`; the pre-rebuild names `desktop-interactive`, `audio-playback`, `video-playback`, `io-stream`, `background-crawler`, `network-bulk`, `electron-comms` and `system-daemon` are gone (9.5 D19→D70, 9.6, 9.7 D1/D5/D31, 9.8 D25, 9.9 D26, 9.10 D13). The plan's rules in §1–§3 and §5–§6 are what authoring follows (dataset/README.md:166).
- Sources: SX-0793 (record-gaps §2 item 2, `jioh/2026-10-14-record-gaps-and-doc-staleness-for-9.15.md:27`); SX-0837 (record-gaps §2 item 15, `jioh/2026-10-14-record-gaps-and-doc-staleness-for-9.15.md:40`); SX-0890 (guidebook dataset vol-02 ch.11 (§11.5) mismatch list item 1, `dataset/02-the-archetype-library.md:1456`); SX-0659 (handoff task-9.5, `jioh/task-9.5.md:43`)
- Cross-ref: W-0227; W-0229; W-0232; W-0233; W-0234; W-0235; W-0236; W-0237
- Resolved at merge: The rows offer "replace" or "mark §4 superseded". The doc is normative and a docs/workload/ doc gets a full pass against the code (9.15 spec decision 4); the public docs describe the final state and carry no account of prior values (_dev/research/jioh/research-slice-workflow.md:23) — so §4 is replaced by the current library, not kept as a marked history.
- Notes: Verified at HEAD: 29 keys under `archetypes`; 28 `category_source: meas`. Per-entry replacements: W-0227 (the interactive three), W-0229 (compute/batch), W-0232 (`io-stream`), W-0233 (`background-crawler`), W-0234 (`game-task-chain`), W-0235 (`network-bulk`), W-0236 (`electron-comms`, OQ-3 at :85), W-0237 (`system-daemon`). §6 OQ-4 is W-0229's.

### W-0232 · applied
- At: `docs/workload/archetype-plan.md` §4 IO family item 7 `io-stream`, line 57
- Change: Remove the `io-stream` entry with its "category_source + params: `interbench:man-write` / `interbench:man-read`"; where the plan needs the streaming I/O work, name the measured `file-archiver` and `incremental-backup`.
- Final word: 9.7 D1 and D31: `io-stream` leaves the library for the measured `file-archiver` and (through 9.10 D119–D125) `incremental-backup`; interbench states no timing parameter for its Write/Read loads (K1, a comparison report of the 2026-09-13 claim verification), so "params: interbench" was MISATTRIBUTED (9.7 scope card item 9).
- Sources: SX-0456 (9.7 scope card item 9, `task-9.7-background-io/scope-card.md:59`)
- Cross-ref: W-0231
- Notes: —

### W-0233 · applied
- At: `docs/workload/archetype-plan.md` §4 IO family item 8 `background-crawler`, line 58; §5 binding note, line 77 ("P1 binds tracker-miner-fs-3 to `cpu-batch`, not `background-crawler` … the everyday low-intensity indexer remains `background-crawler` elsewhere (C4/S14)")
- Change: Remove the `background-crawler` entry and the binding note; where the plan needs the indexer, name the measured `file-indexer` (Tracker's miner, declared class `idle`), which P1b (the indexer pair of C2, the policy-pair group) binds as `tracker-miner-f`.
- Final word: 9.7 D5 (2026-09-19): `background-crawler` leaves the library — no timeline bound it, its values mixed an idle miner's housekeeping with `updatedb.plocate`'s duty. 9.10 D65–D71 re-created the everyday indexer from its own measurement as `file-indexer`, declared class `idle` (9.13), bound as `tracker-miner-f` in `c1-indexing`, `c2-p1b` and `c7-indexing`.
- Sources: SX-0008 (TODO 9.15 line (from 9.7 D5), `_dev/TODO.md:179`); SX-0442 (9.7 D5, `task-9.7-background-io/changelog.md:31`)
- Cross-ref: W-0231
- Notes: Item 66 of 9.12's scope card (9.7) also reads "BG_CPUIO/indexer class" at :58 as OURS-UNDER-SOURCE-TAG (K3); the line leaves with the entry.

### W-0234 · applied
- At: `docs/workload/archetype-plan.md` §4 Structural-special family item 9 `game-task-chain`, line 61; §5 binding note, line 76 ("wineserver → `system-daemon` is a provisional approximation")
- Change: Restate item 9 to the entry as it stands: a chain of 16 members (`chain_length` 16, inside the source's 15–20 frame-critical band) plus a `wineserver` member (`wineserver_run` 260 µs), `per_schedule_run` anchored on the slide's two named examples 260 µs and 1.65 ms (not a range), the 16,667 µs frame period a design value on `steamos-refresh` (the Steam Deck's 60 Hz refresh), with no ~300-task count, no ~90 % long-lived or 70–75 % wakeups-from-waiting parameter and no "16.7 ms frame budget"; replace the wineserver binding note with 9.4 D4's resolution (wineserver is a chain member).
- Final word: 9.4 D2 (the deck states no frame period or budget; 16.7 ms is a design frame period on `steamos-refresh`), D3 (slide 12's ~300 tasks are scheduled system-wide; no task-count parameter), D4 (`wineserver` a chain member), D6 (260 µs and 1.65 ms two named examples; 70–75 % of scheduling events initiated by waiting syscalls), D7 (`frac_long_lived` and `frac_wakeups_from_wait` removed as inert, kept as notes).
- Sources: SX-0391 (9.4 scope card, Out of 9.4 (To 9.15), `task-9.4-gaming/scope-card.md:22`)
- Cross-ref: W-0231; W-0237
- Notes: Code: dataset/archetypes.yaml `game-task-chain` — `wineserver_run` 260 µs (`lavd-ossna24:s13`), `per_schedule_run` lognormal anchors 260/1650 µs, `frame_period` 16667 µs `source: steamos-refresh`, `chain_length` 16 (`lavd-ossna24:s12`), `binding_params: [lane_share, member_names]`. The concentration statistics (top 30–40 tasks = 95 %; 15–20 take 60–70 %) still defend the lane scaling. The :76 note is also W-0237's.

### W-0235 · applied
- At: `docs/workload/archetype-plan.md` §2 line 31 (names `network-bulk`); §4 meas family item 10 `network-bulk`, line 64
- Change: Remove the `network-bulk` entry; the mail sends it last bound are the `mail-client` send operation.
- Final word: 9.10 D13, unamended: `network-bulk` left the library; its last bindings, the mail sends, became the `mail-client` send operation.
- Sources: S10-033 (9.10 D13, `task-9.10-scenarios-timelines/changelog.md:268`)
- Cross-ref: W-0228; W-0231
- Notes: Line 31's sentence is restated by W-0228.

### W-0236 · applied
- At: `docs/workload/archetype-plan.md` §2 line 31 (`electron-comms` in the Tier-1 sentence); §4 meas family item 11 `electron-comms`, line 65; §6 OQ-3 line 85 ("referee re-pointed to `meas-ci`")
- Change: Remove the `electron-comms` entry with its `meas-pending` and OQ-3 text; name the measured `renderer-hidden`, `chat-client` and `game-client` where the plan needs them, and restate OQ-3 as decided (no heartbeat TIMER; one renderer per hidden tab's site).
- Final word: 9.8 D1 and D25 (amended by D26, D31 and 9.5 D84): `electron-comms` is split per bound program into measured entries — `renderer-hidden` (a hidden tab's renderer, one per site under Chromium's site-per-process model), `chat-client` (Element Desktop), `game-client` (the Steam client) — with no heartbeat TIMER period; the `steamwebhelper` and `zoom` helper tasks retired. 9.10 D16 retired `renderer-visible` (the page in use is `web-browser`'s renderer); 9.10 D15 set the hidden tabs' `count: 4` in `c1-browsing`.
- Sources: SX-0030 (TODO 9.15 line (from 9.8 D25), `_dev/TODO.md:179`); SX-0464 (9.8 D25, `task-9.8-browser-comms/changelog.md:524`)
- Cross-ref: W-0228; W-0231
- Notes: OQ-3 (renderer reuse) was decided by 9.8 D1–D4. Line 31's sentence is restated by W-0228. At HEAD the library holds `renderer-hidden`, `chat-client`, `game-client`.

### W-0237 · applied
- At: `docs/workload/archetype-plan.md` §2 line 31 (`system-daemon` in the Tier-1 sentence); §4 meas family item 12 `system-daemon`, line 66; §5 binding note, line 76 ("wineserver → `system-daemon`")
- Change: Remove the `system-daemon` entry and the wineserver binding note; name the four measured session entries — `compositor-shell` (GNOME Shell), `audio-server` (the PipeWire stack), `service-manager` (systemd) and `message-bus` (dbus-daemon) — where the plan needs them.
- Final word: 9.9 D26 (amended by D30, D31; corrected by D27, D30, D43): `system-daemon` is removed; four measured entries replace it, each a set of per-thread components with wake rates and gap/run quantile tables (`meas-ci:session:2026-09-24`), no lognormal SLEEP/RUN; the `xorg` task leaves `c1-idle` and `c7-idle` (no Xorg or Xwayland on the GNOME 46 Wayland session at idle). `wineserver` is a member of the game chain since 9.4 D4 (`wineserver_run` 260 µs).
- Sources: SX-0036 (TODO 9.15 line (from 9.9 D26), `_dev/TODO.md:179`); SX-0472 (9.9 D26, `task-9.9-daemons-session/changelog.md:206`)
- Cross-ref: W-0228; W-0231; W-0234
- Notes: Code: dataset/timelines/coreset/c1-idle.timeline.yaml:11–17 binds `gnome-shell`, `pipewire`, `systemd`, `dbus-daemon` to the four entries. The :76 note is also W-0234's; line 31 is W-0228's.

### W-0238 · applied
- At: `docs/workload/archetype-plan.md` new
- Change: State once, at the library level, that the library's entries come from more than one observation venue (28 entries measured on the CI runner, `category_source: meas`; `game-task-chain` from the `lavd-ossna24` talk slides), that their relative scales are not calibrated to each other, and that a timeline composing a runner-measured task with the literature-grounded one carries that limitation; a scale bridge may be written into scope as a ratio, never applied to a value. Name its sensitivity check: the venue variants `venue-x0.8` and `venue-x1.25`, every RUN but the frame chain's scaled by 0.8 and 1.25 (`dataset/variants.yaml:35–44`; 9.14 decision 12).
- Final word: The 9.5 follow-ups spec decision 13 (scale limitation at the composition seam, `_dev/docs/spec/jioh/task-9.5-interactive-typing-follow-ups.md:67`), unamended: "The library's archetypes come from more than one observation venue, and their relative scales are not calibrated to each other; a timeline composing a runner-measured task with a literature-grounded one carries that limitation. It is stated once at the library level." A scale bridge, one benchmark figure both machines report, may be written into scope as the ratio, never applied to a value. 9.10 D87 reads it with 9.5 D10: every measured value in the library is the CI runner's (one venue); the one literature-grounded entry left is `game-task-chain` (`lavd-ossna24`, lane-scaled). 9.14 decision 12's venue variants (`venue-x0.8`, `venue-x1.25`) are the sensitivity check the decision handed to 9.14.
- Sources: SX-0662 (handoff task-9.5 (9.5 follow-ups spec decision 13), `jioh/task-9.5.md:43`); SX-0006 (TODO 9.15 line (from 9.5, follow-ups spec decision 13), `_dev/TODO.md:179`); SX-0751 (record-gaps §1 item 2, `jioh/2026-10-14-record-gaps-and-doc-staleness-for-9.15.md:12`); SX-0915 (guidebook dataset vol-02 open note (§12.1), doc mismatch, `dataset/02-the-archetype-library.md:1468`)
- Cross-ref: W-0231
- Resolved at merge: The extraction agents placed it in `dataset/README.md`, in this plan, or in measurement-overview §11. 9.5's decision says "once at the library level": the library is `dataset/archetypes.yaml`, whose header is a pinned input of all seven manifests (an edit forces their re-bless and the RQ0 gate spec's re-pin); among the docs, this plan is the one whose subject is the library ("Archetype Library — Writing Plan", normative for it), while the README describes the dataset as a whole and measurement-overview §11 the runner's limits on each measured value. So the statement goes here, once.
- Notes: 28 entries carry `category_source: meas` (`game-download-idle` reusing `game-download`'s tables); the raw "27" is corrected. Not stated anywhere at HEAD (grep of `dataset/archetypes.yaml`, `dataset/README.md`, `docs/`). The dataset guidebook vol-02 §12.1 open note asks for it (`docs/guidebook/dataset/02-the-archetype-library.md:1468`). `dataset/README.md` and measurement-overview §11 do not restate it ("stated once").

### W-0837 · applied
- At: `docs/workload/archetype-plan.md` §3 Multiplicity, Static multiplicity bullet, line 40 ('renderer counts from the tab-count literature (`dubroy-chi10`, `mozilla-testpilot10`, `chang-chi21` — defined against the Chromium process model)')
- Change: Drop the three removed ids; the renderer count's sources are `glam` and `meas-ci:desktop:2026-10-04`.
- Final word: 인지오's answer to W-0071 (2026-10-15, (a)), applied in K01: the three entries left `docs/references.md`. 9.10 D15: the renderer count follows Firefox's Linux tab telemetry (`glam`) and an observed Chrome.
- Sources: W-0071; `logs/K01.md` ## Rows for other chunks
- Cross-ref: W-0230
- Notes: found in K01. W-0230 carries the full restatement of the bullet; the removal it waited on is done.

### W-0887 · open
- At: `docs/workload/archetype-plan.md` §5, the field list, line 110 ("`sampling` (per-instance | per-task | per-iteration — interpretation-contract §5)", listed as a field of the entry)
- Change: Move `sampling` into the numeric params' description: it is a key of each numeric param (312 params carry it), no entry has a top-level `sampling`, and the linter checks it per param (`dataset/tools/wlc/linter.py:145`); the plan's own linter sentence (`:117`) already treats it so.
- Final word: K04's fifth review (passed 2026-10-16), its one nit.
- Sources: `logs/K04.md` ## Review round 2 (fifth review)
- Cross-ref: W-0226
- Notes: found in K04's review. K04's file: a follow-up chunk.
