# Task 9.10 — the span probes: results

The probes of `../method.md` (changelog D143–D145), each one job on the AMD EPYC 7763, never a repeat. Each reading is D143's standard — the observed phase's window at the placement every repeat takes, against the probe's level over the file's span, within 5 % — or D144's paired windows, read by `dataset/tools/meas/campaign/span_probe.py`; its output beside this page as `<entry>-<state>.level.json` or `.paired.json`. "Carried" is the entry's pooled campaign: the mean over its repeats and their coefficient of variation.

## Runs

| probe | run | job | landed | build |
|---|---|---|---|---|
| dry run, VS Code and Kdenlive driven, three 60 s windows | 37263264550 | `code` 11, `kdenlive` 11 (`mode: dry`) | 1,263 s, 456 s | VS Code 1.138.0; Kdenlive 23.08.5 (on a Xeon 6973P-C, any model) |
| hidden renderer | 37263321218 | `chrome-hidden` 10 | 2,492 s | Google Chrome 154.0.8037.57 |
| Writer idle | 37264950064 | `soffice` 10 | 1,605 s | LibreOffice 24.2.7.2 |
| Kdenlive idle | 37264996600 (37264950064 gated: EPYC 9V74) | `kdenlive` 10 | 3,159 s | Kdenlive 23.08.5 |
| Kdenlive driven | 37264950064 | `kdenlive` 11 | 5,162 s | Kdenlive 23.08.5 |
| Kdenlive driven, second (D150) | 37274214398 | `kdenlive` 12 | 5,442 s | Kdenlive 23.08.5 |
| hidden renderer, 3,600 s (D149) | 37273691029 (37273549541, 37273631811 gated: Xeon 8573C, EPYC 9V45) | `chrome-hidden` 11 | 4,309 s | Google Chrome 154.0.8037.57 |

## Readings

| entry, state | span | CPU ms/s: level, placement, worst | wakes/s: level, placement, worst | holds |
|---|---|---|---|---|
| `renderer-hidden` | 1,545 s | 0.1126, +10.1 %, −15.9 % at 590 s | 2.377, +2.5 %, +6.1 % at 250 s | wakes; not CPU |
| `office-writer`, idle | 1,429 s | 0.6147, −7.5 %, −8.8 % at 730 s | 3.454, +0.1 %, +0.6 % at 910 s | wakes; not CPU |
| `video-editor`, idle | 2,976 s | 0.0655, +10.8 %, +11.5 % at 20 s | 1.222, +12.5 %, +12.5 % at 0 s | neither |
| `video-editor`, driven | 4,758 s | 381.4, −6.0 %, −7.4 % at 610 s | 202.6, +10.9 %, +13.8 % at 610 s | neither |
| `video-editor`, driven, second probe | 4,758 s | 373.5, +0.5 %, +3.5 % at 1,280 s | 212.1, −1.0 %, −6.4 % at 1,240 s | both |
| `video-editor`, driven, the two probes averaged | 4,758 s | 377.4, −2.8 %, −4.5 % at 610 s | 207.3, +4.8 %, +8.3 % at 460 s | both |

- **`renderer-hidden`.** The twelve page renderers' CPU per 100 s scatters 0.059–0.199 ms/s with no trend, its runs 0.3–0.4 ms at a time and the renderers waking together (9.8 D15); the wakes hold. Against the carried 19 repeats — CPU share 9.16 × 10⁻⁵, cv 8.4 %, range −12.6 % to +20.1 %; wakes 2.024/s, cv 6.2 % — the probe's level sits +23 % and +17 % above: one session on Chrome 154, against 152 and 153 carried.
- **`office-writer`, idle.** Wakes 3.42–3.47/s in every minute; CPU per minute 0.56–0.66 ms/s through the length of the runs alone, the largest 0.7 ms; no AutoRecovery save in 1,500 s. Carried, 14 repeats: wakes 3.459/s, cv 0.2 %; CPU share 5.93 × 10⁻⁴, cv 8.0 %. The probe's level is −0.1 % and +3.7 % of them.
- **`video-editor`, idle.** The main thread's wakes run 81 in the phase's first minute, 72 in each of the next two and 65–67 a minute from the fourth on, `Qt bearer threa` 6 a minute throughout: work after launch that ends some 3–4 minutes past the 30 s settle. The carried 120 s phase sits inside it: carried wakes 1.363/s (20 repeats, cv 2.1 %), the probe's first 120 s 1.375/s, its level over the span 1.222/s — the carried value 11.5 % above the level.
- **`video-editor`, driven.** The eight windows step between the second and the third, about 1,200 s into the input: CPU 358.6 and 353.5 ms/s, then 384.4–394.6; wakes 224.8 and 230.4/s, then 189.2–201.1. The main thread `kdenlive` carries it — 148.0 and 153.1 wakes/s at 357.1 and 351.7 ms/s, then 125.6 and 127.7 at 384.1 and 382.7, its run per wake 2.4 ms then 3.0 — while `QXcbEventQueue`'s run per wake moves 5 %. The screenshots after each window show the same timeline and clip monitor. Carried, 20 repeats: driven wakes 191.2–230.1/s, CPU share 0.350–0.390; the probe's first window, 224.8/s at 0.359, lies inside them, its level over the span, 202.6/s at 0.381, also. One probe does not say whether the step recurs at the same point of the input (9.5 D56).
- **`renderer-hidden`, the 3,600 s probe (D149).** The page's own thread `chrome` runs 0.106, 0.083, 0.077 and 0.080 ms a wake in the steady phase's first four minutes, 0.139 in the fifth and 0.083 in the sixth, then 0.055–0.060 ms from the seventh minute to the hour's end: its settling ends about 360 s past the 630 s grace-settle, inside the carried 600 s phase. `HangWatcher` holds 0.024–0.026 ms and 1.200 wakes/s throughout, `Chrome_ChildIOT` 0.031–0.035 ms. Past the settling, an episode recurs in the 300 s windows at 1,200–1,500 s and 3,000–3,300 s — the page thread at 0.072–0.075 ms, `Chrome_ChildIOT` waking 0.243–0.247/s against 0.200–0.210 — some 1,800 s apart. Against the level over 1,545 s the 600 s phase at the placement reads CPU +11.8 % and wakes +1.7 %; over 3,600 s, +20.5 % and +2.4 %. Past 600 s into the phase, a 600 s window holds the wakes within 3.7 % at every placement and the CPU within −7.2 % and +10.4 %; 1,800 s holds the CPU within −1.0 % at the placement and −5.9 % at the worst.
- **`video-editor`, driven, the second probe (D150).** Its eight windows read 375, 368, 385, 375, 366, 370, 375 and 371 ms/s and 210, 218, 199, 207, 219, 216, 211 and 215 wakes/s. The third window, 1,200–1,800 s into the input, holds the first probe's state — the main thread at 126 wakes/s and 3.06 ms a wake — and the fourth returns to 133/s and 2.81 ms; in the first probe that state held from the third window to the eighth. Over `c7-transcode`'s 2,967 s the two probes averaged read CPU −2.1 % and wakes +3.5 % at the placement.
