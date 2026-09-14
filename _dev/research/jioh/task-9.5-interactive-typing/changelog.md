# Task 9.5 — changelog

One entry per decision applied to `dataset/archetypes.yaml` (and the registry lines it owns). Parameter, old value, new value, source id and locator or the label, commit. References are the search records' candidate ids (`search/candidates.md`).

## D1 — boundary (2026-09-14)

`audio-playback` and `video-playback` stay in 9.5, by 인지오's decision: scope-card items 24–33 and search topics T4–T5 are this slice's. The `zoom` helper's `electron-comms` archetype remains 9.8's; only the `zoom` voice and video tasks' binding to the two playback archetypes is 9.5's. No value changed by this entry.

## D2 — `desktop-interactive` splits per application (2026-09-14)

By 인지오's decision: `desktop-interactive` is replaced by one archetype per bound application — `code`, `kdenlive`, `chrome` (the browser task; its renderers stay `electron-comms`, 9.8's), `soffice.bin`, `thunderbird`, `gimp` — each grounded on one observation of that application under phase decision 2. An application with no obtainable observation binds to the nearest observed archetype, and its `modeling_notes` record that as a limitation. Grounds: S1-lorch2003 §4.7 ("different applications have very different CPU requirements, even when handling the same type of user interface event"), S1-flautner2000 Table 3 (Xemacs 0 % of episodes ≥ 100 ms; GIMP 91 % of time in such episodes), S1-endo1996 (Notepad < 10 ms vs Word ≈ 32 ms per keystroke), S1-tsafrir2003 (Emacs ≈ 0.2 % CPU at 8 char/s); no observation covers all six classes and none covers a video editor (candidates §13). The archetype ids, each archetype's observation and its parameters are decided in the entries that follow; no value changed by this entry. Hands to 9.10: every `desktop-interactive` binding in the C1, C2, C3 and C7 timelines rebinds. Hands to 9.14: the prior table's editor rows and the H1 lines rest on per-application numbers.
