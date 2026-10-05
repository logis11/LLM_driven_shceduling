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

## Readings

| entry, state | span | CPU ms/s: level, placement, worst | wakes/s: level, placement, worst | holds |
|---|---|---|---|---|
| `renderer-hidden` | 1,545 s | 0.1126, +10.1 %, −15.9 % at 590 s | 2.377, +2.5 %, +6.1 % at 250 s | wakes; not CPU |
| `office-writer`, idle | 1,429 s | 0.6147, −7.5 %, −8.8 % at 730 s | 3.454, +0.1 %, +0.6 % at 910 s | wakes; not CPU |
| `video-editor`, idle | 2,976 s | 0.0655, +10.8 %, +11.5 % at 20 s | 1.222, +12.5 %, +12.5 % at 0 s | neither |
| `video-editor`, driven | 4,758 s | 381.4, −6.0 %, −7.4 % at 610 s | 202.6, +10.9 %, +13.8 % at 610 s | neither |

- **`renderer-hidden`.** The twelve page renderers' CPU per 100 s scatters 0.059–0.199 ms/s with no trend, its runs 0.3–0.4 ms at a time and the renderers waking together (9.8 D15); the wakes hold. Against the carried 19 repeats — CPU share 9.16 × 10⁻⁵, cv 8.4 %, range −12.6 % to +20.1 %; wakes 2.024/s, cv 6.2 % — the probe's level sits +23 % and +17 % above: one session on Chrome 154, against 152 and 153 carried.
- **`office-writer`, idle.** Wakes 3.42–3.47/s in every minute; CPU per minute 0.56–0.66 ms/s through the length of the runs alone, the largest 0.7 ms; no AutoRecovery save in 1,500 s. Carried, 14 repeats: wakes 3.459/s, cv 0.2 %; CPU share 5.93 × 10⁻⁴, cv 8.0 %. The probe's level is −0.1 % and +3.7 % of them.
- **`video-editor`, idle.** The main thread's wakes run 81 in the phase's first minute, 72 in each of the next two and 65–67 a minute from the fourth on, `Qt bearer threa` 6 a minute throughout: work after launch that ends some 3–4 minutes past the 30 s settle. The carried 120 s phase sits inside it: carried wakes 1.363/s (20 repeats, cv 2.1 %), the probe's first 120 s 1.375/s, its level over the span 1.222/s — the carried value 11.5 % above the level.
- **`video-editor`, driven.** The eight windows step between the second and the third, about 1,200 s into the input: CPU 358.6 and 353.5 ms/s, then 384.4–394.6; wakes 224.8 and 230.4/s, then 189.2–201.1. The main thread `kdenlive` carries it — 148.0 and 153.1 wakes/s at 357.1 and 351.7 ms/s, then 125.6 and 127.7 at 384.1 and 382.7, its run per wake 2.4 ms then 3.0 — while `QXcbEventQueue`'s run per wake moves 5 %. The screenshots after each window show the same timeline and clip monitor. Carried, 20 repeats: driven wakes 191.2–230.1/s, CPU share 0.350–0.390; the probe's first window, 224.8/s at 0.359, lies inside them, its level over the span, 202.6/s at 0.381, also. One probe does not say whether the step recurs at the same point of the input (9.5 D56).
