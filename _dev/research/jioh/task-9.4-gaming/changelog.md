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
