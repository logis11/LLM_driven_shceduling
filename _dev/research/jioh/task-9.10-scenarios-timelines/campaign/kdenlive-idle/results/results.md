# Task 9.10 — `video-editor`'s idle phase past Kdenlive's launch work: results

The campaigns of `../method.md` (changelog D146, D147), on the AMD EPYC 7763: `meas-ci:interactive:2026-10-05`, the idle repeats; `meas-ci:desktop:2026-10-05`, the launch re-trace. Pooled records beside this page: `pool-kdenlive.json` (`campaign/pool.py`) and `launch-kdenlive-pooled.json` (`desktop/pool.py`).

## The idle repeats

- **Runs.** The first batch, repeats 1–5 (runs 37272192539, 37272322853, 37273046929; indices 3–5 gated once and index 1 three times, each relaunched), every one valid: the main thread's three values at ±5.7 %, the pool projecting six. Repeat 6 (37274147650): the run mean ±6.19 %, projecting eight. Repeats 7–8 (37275048679): the run mean ±7.64 %, projecting sixteen. Repeats 9–16 (37276032133, 37276104518, 37276412197, 37276716093), added as one batch up to that projection (9.7 D26).
- **The rule holds at 16** on every value on the list: the main thread `kdenlive`, wakes 1.1611/s ±1.71 %, gap mean 861.3 ms ±1.71 %, run mean 0.0261 ms ±4.45 %; `Qt bearer threa`, wakes 0.1/s ±0.00 %, run mean 0.4237 ms ±1.77 %. The main thread's run mean turns on how many of its rare long runs, 200–260 µs against a mean near 25 µs, a 180 s phase catches: one in most repeats, three in repeat 8.
- **Every repeat valid**: the gate open on the EPYC 7763; mode `idle`, the settle 240 s and the phase 180 s; the trace stopped cleanly; the project open after the settle; the idle phase flat from its start, 12 wakes in each 10 s slice of repeat 2 but one of 13.
- **Against 9.5's 20 repeats** (`meas-ci:interactive:2026-09-18`, the phase 120 s from a 30 s settle): the main thread's wakes 1.2604/s then, 1.1611/s now (−7.9 %); its run mean 0.0284 ms then, 0.0261 now; the tree's wakes 1.3625/s then, 1.2637/s now, 1.20–1.34 across the repeats, against the span probe's level of 1.212/s past the settle.

## The launch re-trace

- **Runs.** Repeats 1–5 (37272194466; index 1 gated once, landing in 37272498504), every one valid by the launch campaign's checks (`pool_runs.py`).
- **The launch phase** runs from the exec to the end of the 240 s settle, 240.637–240.645 s; its CPU 2,136.6–2,302.3 ms and its wakes 2,141–2,196 per repeat, the first 10 s at 219.8 ms/s on average. The 30 s phases of `meas-ci:desktop:2026-10-04b` held 2,096–2,259 ms: the launch's CPU falls almost wholly in its first seconds.
