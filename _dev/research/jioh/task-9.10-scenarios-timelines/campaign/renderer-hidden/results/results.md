# Task 9.10 — `renderer-hidden` past its page thread's settling: results

The campaign of `../method.md` (changelog D152, D155, D156), `meas-ci:desktop:2026-10-05b`, on the AMD EPYC 7763. Pooled records beside this page: `pooled.json` (`desktop/pool.py --tag meas-ci:desktop:2026-10-05b`) and `launch-chrome-hidden-pooled.json` (`desktop/pool.py`, the launch landings as D155 re-analysed them).

## The steady repeats

- **Runs.** Repeats 1–5, each landing once: repeat 4 in 37281764593 (#105), repeats 1, 3 and 5 in 37281847886 (#106), repeat 2 in 37282164033 (#107).
- **Every repeat valid**: the gate open on the EPYC 7763; Google Chrome 154.0.8037.57 and kernel `6.17.0-1022-azure` in each; 12 origins and 16 renderers observed, 12 measured; the control tab identified at 10.19–10.20 wakes/s against 0.210–0.217 for the next renderer; none left out by the throttling check.
- **The rule holds at 5** under 9.8's per-value treatments, as `desktop/pool.py` applies them (D155):
  - within the tolerance: `HangWatcher`, wakes 0.1/s and gap mean 10.000 s, ±0.00 %; the page's own thread `chrome`, wakes 0.0669/s and gap mean 14.94 s, ±1.59 %.
  - run means following the runner's speed (9.8 D17): `HangWatcher` 0.0262 ms ±18.08 % (0.0211–0.0310 per repeat); `chrome` 0.0624 ms ±11.42 % (0.0558–0.0700).
  - components varying between sessions (9.5 D57; 9.8 D21, D24, D26): `Chrome_ChildIOT`, 0.0176 wakes/s ±6.47 % (0.0168–0.0186), gap mean 56.8 s (53.7–59.5 s), run mean 0.0324 ms ±7.46 % (0.0293–0.0340); `Compositor` and `PerfettoTrace`, which wake together, 0.0083 wakes/s ±17.56 % (0.0067–0.0100), gap mean 120.0 s (100.0–150.0 s), 4–6 wakes per renderer a phase, run means 0.0226 ms ±12.28 % and 0.0209 ms ±9.26 %.
  - the sparse residual (9.8 D27): `ThreadPoolServi` and `MemoryInfra`, 0.0096 wakes/s ±20.20 % (0.0083–0.0121), gap mean 104.3 s, run mean 0.0346 ms ±61.28 %, 5.0–7.2 wakes per renderer a phase. `ThreadPoolServi`, a component of its own in 9.8, wakes with `Compositor` and `PerfettoTrace` here too; the components taken in descending wake rate until 95 % of the wakes (9.5 D16) reach that share at `PerfettoTrace`, the page thread and `Chrome_ChildIOT` waking more than in 9.8.
  - projected repeats to hold the tolerance outright, from this pool: `HangWatcher`'s run mean 36, `chrome`'s 16; `Chrome_ChildIOT` 7–9; `Compositor` and `PerfettoTrace` 12–34; the residual's wake rate 44.
- **Against 9.8's 19 repeats** (`meas-ci:desktop:2026-09-20`, Google Chrome 152 and 153, the 630 s grace-settle; D156): the page's own thread wakes 1.72 times as often (0.0669 against 0.0389 per renderer a second), its runs 35 % shorter (0.062 against 0.096 ms); `Chrome_ChildIOT` 2.51 times as often (0.0176 against 0.0070); `Compositor` and `PerfettoTrace` 1.28 times (0.0083 against 0.0065); `HangWatcher` holds at 0.100/s. The renderer wakes 0.211 against 0.169/s (0.208–0.215 across the repeats), its CPU share 9.6 against 9.2 × 10⁻⁵.
- **The scope's statements, read on this campaign** (D156). In 100 s windows over the 5 repeats (`meas/windows.py`): the page thread 0.068 ms in the first 100 s and 0.057–0.072 after; the residual waking at 3.6 times its phase rate in the first 100 s; the windows holding 5.2 % of the CPU above the median window (9.8: 13.3 %). Within one run, on D149's 3,600 s probe from 400 s, 600 s windows every 60 s (`desktop/within_run.py`): `Chrome_ChildIOT` ±8.1 % (9.8: ±17.7 %); `Compositor` and `PerfettoTrace` ±30.6 % (9.8: ±10.8 %); the residual, 1–4 wakes per renderer a window, ±64.0 %.

## The launch re-trace

- **Runs.** Repeats 1–5: repeats 1, 3, 4 and 5 in 37281764593 (#105); index 2 gated once (Intel Xeon 6973P-C), landing in 37282164033 (#107). Every one valid by the launch campaign's checks (`../../launch/method.md` §1).
- **The streams** (D155). Repeats 2 and 5 carried a plain renderer, `--renderer-client-id=21`, started some 2 s after the tabs' renderers (client ids 6–18) and before the gate's listing 20 s after launch: 13 renderer streams against the 12 background tabs'. The five landings re-analysed locally with `launch.py analyze`, the tabs' renderers the lowest client ids: repeats 1, 3 and 4 reproduce the runner's streams byte for byte, repeats 2 and 5 carry 12 streams, their reports marked `launch.reanalysed`.
- **The launch phase** runs from the exec to the end of the 1,030 s grace-settle, 1,051.219–1,051.227 s; Chrome's whole tree 4,096.8–5,123.3 ms of CPU and 32,317–34,529 wakes per repeat, the first 10 s at 259.8 ms/s on average. The 651.2 s phases of `meas-ci:desktop:2026-10-04b` held 3,996–4,494 ms and 25,646–27,482 wakes, the first 10 s at 274.1 ms/s.

## The pool's table

`desktop/pool.py --md` over the five steady repeats; `passes` is the tolerance alone, before 9.8's per-value treatments.

| quantity | k | mean | half-width | passes |
|---|---|---|---|---|
| steady HangWatcher wakes/s | 5 | 0.1 | ±0.0% | yes |
| steady HangWatcher gap mean (ms) | 5 | 10000.0351 | ±0.0% | yes |
| steady HangWatcher run mean (ms) | 5 | 0.0262 | ±18.1% | no |
| steady chrome wakes/s | 5 | 0.0669 | ±1.6% | yes |
| steady chrome gap mean (ms) | 5 | 14944.0126 | ±1.6% | yes |
| steady chrome run mean (ms) | 5 | 0.0624 | ±11.4% | no |
| steady Chrome_ChildIOT wakes/s | 5 | 0.0176 | ±6.5% | no |
| steady Chrome_ChildIOT gap mean (ms) | 5 | 56782.5337 | ±6.5% | no |
| steady Chrome_ChildIOT run mean (ms) | 5 | 0.0324 | ±7.5% | no |
| steady Compositor wakes/s | 5 | 0.0083 | ±17.6% | no |
| steady Compositor gap mean (ms) | 5 | 120000.4213 | ±17.6% | no |
| steady Compositor run mean (ms) | 5 | 0.0226 | ±12.3% | no |
| steady PerfettoTrace wakes/s | 5 | 0.0083 | ±17.6% | no |
| steady PerfettoTrace gap mean (ms) | 5 | 120000.4213 | ±17.6% | no |
| steady PerfettoTrace run mean (ms) | 5 | 0.0209 | ±9.3% | no |
| steady residual wakes/s | 5 | 0.0096 | ±20.2% | no |
| steady residual gap mean (ms) | 5 | 104348.1739 | ±20.2% | no |
| steady residual run mean (ms) | 5 | 0.0346 | ±61.3% | no |
