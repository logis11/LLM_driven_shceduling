# Task 9.4 — changelog

One entry per decision applied to `dataset/archetypes.yaml` (and the registry lines it owns). Parameter, old value, new value, source id and locator or the label, commit. References are the search records' candidate ids (`search/candidates.md`).

## D1 — the observation (2026-09-13)

`game-task-chain` keeps `lavd-ossna24` as its one source under phase decision 2, by 인지오's decision: the deck's slides 12–17 are taken as one observation of an unnamed game on an unnamed machine, collected with `perf sched record` (S1-05 slide 6, S2-07); the deck's figures draw on at least three process trees (S2-03) and the text does not say which feeds slides 12–14. Alternatives not taken: a public `scx_lavd` sample log (S3-01, S3-02); our own CI measurement of a native game (S4 §4). No value changed by this entry; the statement lands in `modeling_notes` with the first parameter change.

## D2 — `frame_period` (2026-09-13)

- `game-task-chain.params.frame_period`: value 16667 µs unchanged; tag `lavd-ossna24` (no locator) → `steamos-refresh`. Label: design — the game is modelled as display-paced at the Steam Deck LCD default refresh with the 1:1 frame limit; 16667 µs is 1/60 s arithmetic. The deck states no frame period (S2-03; K2 C-lavd-9); its own benchmark ran with V-Sync and the framerate lock off (slide 29 figure labels).
- New registry entry `steamos-refresh` (deployed-system, existence only): `docs/references.md` and `dataset/sources.yaml`. Primary: Valve, "The SteamOS 3.2 Update", 2022-05-26, "The default is 60Hz (which can be frame-limited to 60, 30, and 15fps) … 60hz = 16.66ms/frame" (S2-08, local copy `sources/S2-steam-news-api/news-1675200.json`, gid 4437747060827905309); secondary: Steam Deck tech specs "Refresh rate 60Hz" (`sources/S2-steamdeck-tech/tech-lcd.txt`).
- Registry lines corrected: `docs/references.md` `lavd-ossna24` role line loses "16.7 ms frame budget"; `dataset/sources.yaml` `lavd-ossna24` notes lose "16.7 ms frame budget, 15 ms targeted latency" and gain "States no frame period or frame budget".
- `modeling_notes` opens with the D1 statement and the frame-period statement.
- Build: `make lint` clean, `make dataset`, `make check` manifest verified, 82 tests pass (python3.12). All 100 manifest hashes change because compiled `meta.sampled.archetypes` carries the library file's hash; with `meta` stripped, all 100 artifacts are byte-identical to the previous build (checked by rebuilding the previous library).
- Alternatives not taken: 25000 µs (the 40 Hz mode, same Valve note); no period (the deck's uncapped benchmark).

## D3 — the archetype is the chain only (2026-09-13)

- `game-task-chain.params.n_tasks` (constant 300, `lavd-ossna24:s12`): removed. The count was held against the library's own rule (`archetypes.yaml` header: counts never carry values here); the source's figure is system-wide ("Around 300 tasks are scheduled while running a game", slide 12, including the system tasks it names). How many further game threads a timeline carries, and bound to what, is 9.10's; references handed over: slide 12; S3-01 (95 pids sampled in Apex Legends over 10.9 min, 18 game-named); S3-02 (108 pids in StarCraft II over 99 s, 41 named `Play Main Threa`; 95 in Diablo III, 38 named `Diablo III64.ex`).
- `game-task-chain.params.tail_idle_gap` (lognormal median 500000 µs σ 0.5, `lavd-ossna24:s12`) and `tail_run` (lognormal median 200 µs σ 0.5, `lavd-ossna24:s12`): removed. No observation describes the tasks outside the deck's top 30–40 (K2 C-lavd-12 NOT IN SOURCE; S1 §3 and S3 §3, T3); the values were placeholders under a source tag.
- `scalable` rule rewritten to the chain alone; `modeling_notes` state that the entry models the chain only, what the count in the source is, and that lane scaling is our calibration.
- `dataset/tools/wlc/compiler.py`: `_chain_constructor` no longer reads `n_tasks` and builds no tail tasks; header docstring updated. `dataset/tools/tests/test_invariants.py`: `test_chain_population` asserts chain only; the lane-scaling test drops its tail branch.
- `dataset/sources.yaml` `lavd-ossna24` notes: "~300 tasks per game" → "~300 tasks scheduled system-wide while running a game (including system tasks)" (K2 C-lavd-1 WORDING-FIX).
- Compiled effect: every gaming file loses its 284 `<id>.tail.<j>` tasks. Demand (`single` / `native`): c1-gaming 1.30 / 1.07 (was 1.46 / 1.22 by the compiled-numbers audit's decomposition, tails 0.155); c4-gaming 1.30 / 1.07; c7-gaming 2.30 / 2.07; c2-p2a and c2-p2b 1.16 / 0.95; c3-evening 1.03 / 0.56; c6-dual 1.13 / 1.41. `make lint` clean, `make check` manifest verified, 82 tests pass. The recognizer-visible count `game.exe ×300` is gone; the compiled name multiset now shows `game.exe` at the chain length until 9.10 decides the timelines.
- Alternative not taken: keep the tail with the count as a `binding_params` name.

## D4 — wineserver is a member of the chain (2026-09-13)

- New param `game-task-chain.params.wineserver_run`: constant 260 µs, `lavd-ossna24:s13` ("Some coordination tasks run very shortly (e.g., wineserver:260 usec)"). Source claim; the statistic is not labelled on the slide (K2 C-lavd-5).
- Structure: the constructor inserts one member with id `<iid>.wineserver`, name `wineserver`, right after the head (`chain.1` → `wineserver` → `chain.2` …), RUN = `wineserver_run`, scaled with the chain in `-single` mode. Placement rests on slide 11 (hub of the game's dispatcher threads, pipe_read / epoll), slide 13 (coordination task), slide 16 (the largest edge counts in the graph: `wineserver → Troy.exe epoll (134200)`, `Troy.exe → wineserver pipe_read (58134)`, S2-03 figure labels) and Wine's call path (request write, blocking reply read; S2-11). The linear relay in place of the round trip is our linearisation, stated in `modeling_notes`.
- Timelines: the `wineserver → system-daemon` binding removed from `c1-gaming`, `c2-p2a`, `c3-evening`, `c6-dual` (and the derived `c2-p2b`, `c4-gaming`, `c7-gaming` re-derived). `system-daemon.modeling_notes` binding note replaced by a pointer.
- `dataset/tools/wlc/grid.py`: `CONSTRUCTOR_NAMES` — the grid counts constructor-emitted names toward a segment's default tier as it already counts spawned-child names; without it the gaming segments dropped from tier 2 to tier 1 while the compiled files still carry `wineserver`. Test added. Committed grid unchanged.
- `dataset/tools/tests/test_invariants.py`: chain population is 16 game members plus one `wineserver`, wake order checked.
- Compiled effect: every gaming file has a `wineserver` task that runs each frame (c1-gaming `single`: RUN 341 µs after scaling; `native`: 260 µs) instead of one that slept 1 225 s. Demand (`single` / `native`): c1-gaming 1.30 / 1.09, c2-p2a and c2-p2b 1.16 / 0.97, c3-evening 1.03 / 0.57, c6-dual 1.13 / 1.42, c7-gaming 2.30 / 2.09. `make lint` clean, `make check` verified, 83 tests pass.
- Alternatives not taken: a separate `wine-server` archetype wired by channel; the `system-daemon` binding (contradicted by slides 11, 13, 16 and by every sampled log, S3-01/S3-02).

## D5 — `chain_length` (2026-09-13)

- `game-task-chain.params.chain_length`: value 16 unchanged; tag `lavd-ossna24` (no locator) → `lavd-ossna24:s12` ("There are 15-20 game-specific tasks, which takes 60-70% scheduling"). Label: design within a source range. `modeling_notes`: "15-20 frame-critical band" → the slide's own words; the wineserver member is stated to be outside the count (K2 C-lavd-11 WORDING-FIX and borderline OURS-UNDER-SOURCE-TAG).
- No compiled value changes (manifest hashes move with the library hash only).
- Alternative not taken: a per-instance uniform draw over 15–20.

## D6 — `per_schedule_run` (2026-09-13)

- `game-task-chain.params.per_schedule_run`: values unchanged (lognormal, anchors 260 / 1650 µs, per-task, `lavd-ossna24:s13`). Label fixed in `modeling_notes`: the anchors are the source's two named per-schedule runtimes (a coordination task, a work task) spanning its "a few 100s usec on average to a few msec maximum"; the statistic behind them is unlabelled on the slide; the slide's plot (one game, ~128 tasks, median ~0.04 ms) is a different population and is not used; the p05/p95 reading, the lognormal family and the one draw per member are ours; the per-member draw rests on "Task execution time is very stable and is predictable using its average" (K2 C-lavd-5 OURS-UNDER-SOURCE-TAG, C-lavd-6). The sampled logs' tens-of-µs game threads (S3-01, S3-02) are noted as not a source.
- `docs/references.md` `lavd-ossna24` role line: "per-schedule runtimes ~260 µs–1.65 ms" → the slide's average/maximum wording with the two examples named; "70–75% wakeups" → "70–75% of scheduling events initiated by waiting syscalls" (K2 C-lavd-5, C-lavd-7 WORDING-FIX).
- No compiled value changes.
- Alternatives not taken: fit the slide-13 plot (median ~40 µs); anchor on the text's words alone.

## D7 — the two inert parameters (2026-09-13)

- `game-task-chain.params.frac_long_lived` (constant 0.90, `lavd-ossna24:s12`) and `frac_wakeups_from_wait` (uniform 0.70–0.75, `lavd-ossna24:s14`): removed. Neither was read by any tool (memo finding B1; K2 C-lavd-2, C-lavd-7). Both facts stay in `modeling_notes` with their locators as what the encoding does not model: every member lives for the whole segment; the wake mix is fixed by the wiring.
- No compiled value changes.
- Alternatives not taken: keep them inert; make 10 % of members terminate (window unstated in the source).

## D8 — residual wording (2026-09-13)

- `modeling_notes`: "wired input -> engine -> ... -> display" → the source's "from a user input to display update" (s17) with no intermediate stage named (K2 C-lavd-8 premise not in source); the linearisation sentence now states the source's graph shapes (fan-in, two-step chain, 2-cycles, hub; s11, s16) and that s17's individually periodic tasks are encoded as one timer-driven head (K2 C-lavd-8 OURS-UNDER-SOURCE-TAG).
- `validation_stats.reason`: circularity kept; adds that a CI runner cannot observe a Proton game's structure (S4 §4).
- `docs/references.md` `corbet-lwn24` role line narrowed to the qualitative characterisation; the slide numbers are not in it and its 100 µs figure differs from slide 13 (K2 C-corbet-1 WORDING-FIX).
- No compiled value changes.

## D9 — per-schedule runtime read as the per-wake RUN: bounded limitation (2026-09-17)

By 인지오's decision, after 9.5 follow-ups decision 4 fixed the library's RUN semantics (a RUN is one wake's demand; a resume after preemption folds into the preceding wake): `game-task-chain.modeling_notes` states that the source's per-schedule runtime (s13, D6) is taken as the per-wake RUN and under-states one wake's demand wherever a schedule ended by preemption; the size is bounded from the same observation — s14: preemption 25–30 % of scheduling events, `sched_preempt` 28.78 % on the pie (the fact D7 kept as unmodelled) — about 1.4 schedules per wake on average, larger for the long-running work tasks whose runs approach the scheduler's slice (s13's 1.65 ms worker against the deck's 1.5 ms slice example), near 1 for short coordination tasks. Direction downward. Not taken: scaling the anchors by 1/0.71 (assumes preemption independent of run length and task, which the slice mechanism contradicts, and applies a population mean to two named examples); a per-wake observation (none reachable: no GPU on the runner, D8; the public scx_lavd logs report EWMA runtime per schedule; the author's raw trace is outside the citation rule). Hands to 9.14: the gaming files' sensitivity check sweeps chain-member RUNs over ×1.0–1.4 and beyond for the work tasks. No value changed; no compiled effect.

## D9 — per-schedule runtime read as the per-wake RUN: bounded limitation (2026-09-17)

By 인지오's decision, after 9.5 follow-ups decision 4 fixed the library's RUN semantics (a RUN is one wake's demand; a resume after preemption folds into the preceding wake): `game-task-chain.modeling_notes` states that the source's per-schedule runtime (s13, D6) is taken as the per-wake RUN and under-states one wake's demand wherever a schedule ended by preemption; the size is bounded from the same observation — s14: preemption 25–30 % of scheduling events, `sched_preempt` 28.78 % on the pie (the fact D7 kept as unmodelled) — about 1.4 schedules per wake on average, larger for the long-running work tasks whose runs approach the scheduler's slice (s13's 1.65 ms worker against the deck's 1.5 ms slice example), near 1 for short coordination tasks. Direction downward. Not taken: scaling the anchors by 1/0.71 (assumes preemption independent of run length and task, which the slice mechanism contradicts, and applies a population mean to two named examples); a per-wake observation (none reachable: no GPU on the runner, D8; the public scx_lavd logs report EWMA runtime per schedule; the author's raw trace is outside the citation rule). Hands to 9.14: the gaming files' sensitivity check sweeps chain-member RUNs over ×1.0–1.4 and beyond for the work tasks. No value changed; no compiled effect.
