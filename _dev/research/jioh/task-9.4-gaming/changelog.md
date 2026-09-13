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
