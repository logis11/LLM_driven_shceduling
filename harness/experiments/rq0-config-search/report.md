# rq0-config-search — report

Search spec `harness/experiments/rq0-config-search.yaml`, SHA-256 `a849e4dc453b0dfa301a80ba56a195fc5bb15d8160925e9d12466df7379a65e4`; read 2026-11-21T15:41:35+0900. 470 configurations (MLFQ 288, EDF 66, LOTTERY 110, FIFO 6) on 10 files, 4700 runs; g = 0.5, the band 0.25, 0.33, 0.5, 0.67; floors 1000 µs and 0.01. Fixed is the boot default's point `mlfq-s10000-b100000-q3-x2-cnone`.

**Route: the table is rewritten.** Files at finding 3: `c1-transcode`, `c7-dev`, `c7-video-edit`, `c7-compile`, `c1-render`, `c7-photo`, `c7-ml-train`, `c7-render`.

## Findings

| file | kind | finding | under the g band | under the boot defaults | row's quantity | best point | best's quantity | out of the reading | LOTTERY removed |
|---|---|---|---|---|---|---|---|---|---|
| `c7-transcode` | pick | 2 | 2 | 2–3 | 0.865175 | `fifo-c0.2` | 0.987614 | 20 | no change |
| `c7-gaming` | pick | 2 | 2 | 2 | 1.000000 | `edf-s10000-c0.05` | 1.000000 | 0 | no change |
| `c1-transcode` | pick | 3 | 3 | 3 | 0.005390 | `mlfq-s20000-b10000-q3-x2-c0.5` | 0.562098 | 16 | no change |
| `c7-dev` | no_headroom | 3 | 3 | 3 | -2.200282 | `mlfq-s10000-b10000-q3-x2-c0.95` | 0.683748 | 0 | no change |
| `c7-video-edit` | no_headroom | 3 | 3 | 3 | -0.703213 | `mlfq-s10000-b10000-q3-x2-c0.333` | 0.809428 | 0 | no change |
| `c7-compile` | no_headroom | 3 | 3 | 3 | -0.495088 | `mlfq-s100000-b100000-q3-x2-cnone` | 0.973678 | 32 | no change |
| `c1-render` | no_headroom | 3 | 3 | 2–3 | -0.010827 | `mlfq-s30000-b10000-q3-x2-c0.95` | 0.052574 | 0 | no change |
| `c7-photo` | no_headroom | 3 | 3 | 2–3 | 0.000000 | `fifo-c0.333` | 0.355833 | 0 | no change |
| `c7-ml-train` | no_headroom | 3 | 3 | 3 | 0.000000 | `fifo-c0.95` | 0.897907 | 7 | no change |
| `c7-render` | no_headroom | 3 | 3 | 3 | 0.000000 | `mlfq-s10000-b10000-q3-x2-c0.05` | 0.944258 | 0 | no change |

Finding 1 — no spread; finding 2 — spread the prior table's row holds; finding 3 — spread the prior table missed.

## Checks

| file | check | point | reference | pinned | trace | terms | reproduced |
|---|---|---|---|---|---|---|---|
| `c7-transcode` | fixed | `mlfq-s10000-b100000-q3-x2-cnone` | `runs/rq0-gate-rerun/c7-transcode/fixed~focus` | True | True | video-editor 11127962.000000 / 11127962.000000 | True |
| `c7-transcode` | oracle | `mlfq-s10000-b100000-q3-x2-c0.05` | `runs/rq0-gate-rerun/c7-transcode/oracle~focus` | True | True | video-editor 1500322.000000 / 1500322.000000 | True |
| `c7-gaming` | fixed | `mlfq-s10000-b100000-q3-x2-cnone` | `runs/rq0-gate-rerun/c7-gaming/fixed~focus` | True | True | game.chain.1 1.000000 / 1.000000 | True |
| `c7-gaming` | oracle | `edf-s10000-c0.05` | `runs/rq0-gate-rerun/c7-gaming/oracle~focus` | True | True | game.chain.1 0.000000 / 0.000000 | True |
| `c1-transcode` | fixed | `mlfq-s10000-b100000-q3-x2-cnone` | `runs/rq0-gate-rerun/c1-transcode/fixed~focus` | True | True | video-editor 447969.180000 / 447969.180000; batch 3894612815.000000 / 3894612815.000000 | True |
| `c1-transcode` | oracle | `lottery-s10000-w0.333-c0.333` | `runs/rq0-gate-rerun/c1-transcode/oracle~focus` | True | True | video-editor 430531.080000 / 430531.080000; batch 4134853844.000000 / 4134853844.000000 | True |
| `c7-dev` | fixed | `mlfq-s10000-b100000-q3-x2-cnone` | `runs/rq0-gate-rerun/c7-dev/fixed~focus` | True | True | editor 1750097.400000 / 1750097.400000 | True |
| `c7-dev` | oracle | `mlfq-s10000-b100000-q3-x2-c0.05` | `runs/rq0-gate-rerun/c7-dev/oracle~focus` | True | True | editor 5600806.080000 / 5600806.080000 | True |
| `c7-video-edit` | fixed | `mlfq-s10000-b100000-q3-x2-cnone` | `runs/rq0-gate-rerun/c7-video-edit/fixed~focus` | True | True | editor 4750232.680000 / 4750232.680000 | True |
| `c7-video-edit` | oracle | `mlfq-s10000-b100000-q3-x2-c0.05` | `runs/rq0-gate-rerun/c7-video-edit/oracle~focus` | True | True | editor 8090656.020000 / 8090656.020000 | True |
| `c7-compile` | fixed | `mlfq-s10000-b100000-q3-x2-cnone` | `runs/rq0-gate-rerun/c7-compile/fixed~focus` | True | True | editor 58431291.000000 / 58431291.000000 | True |
| `c7-compile` | oracle | `mlfq-s10000-b100000-q3-x2-c0.05` | `runs/rq0-gate-rerun/c7-compile/oracle~focus` | True | True | editor 87359931.000000 / 87359931.000000 | True |
| `c1-render` | fixed | `mlfq-s10000-b100000-q3-x2-cnone` | `runs/rq0-gate-rerun/c1-render/fixed~focus` | True | True | editor 535735.060000 / 535735.060000; bulk 21394289.000000 / 21394289.000000 | True |
| `c1-render` | oracle | `lottery-s10000-w0.333-c0.333` | `runs/rq0-gate-rerun/c1-render/oracle~focus` | True | True | editor 535735.060000 / 535735.060000; bulk 22089192.000000 / 22089192.000000 | True |
| `c7-photo` | fixed | `mlfq-s10000-b100000-q3-x2-cnone` | `runs/rq0-gate-rerun/c7-photo/fixed~focus` | True | True | photo-editor 2978927.880000 / 2978927.880000 | True |
| `c7-photo` | oracle | `mlfq-s10000-b100000-q3-x2-c0.05` | `runs/rq0-gate-rerun/c7-photo/oracle~focus` | True | True | photo-editor 2978927.880000 / 2978927.880000 | True |
| `c7-ml-train` | fixed | `mlfq-s10000-b100000-q3-x2-cnone` | `runs/rq0-gate-11-3-current/c7-ml-train/fixed~focus` | True | True | editor 8020850.480000 / 8020850.480000 | True |
| `c7-ml-train` | oracle | `mlfq-s10000-b100000-q3-x2-c0.05` | `runs/rq0-gate-11-3-current/c7-ml-train/oracle~focus` | True | True | editor 8020875.920000 / 8020875.920000 | True |
| `c7-render` | fixed | `mlfq-s10000-b100000-q3-x2-cnone` | `runs/rq0-gate-rerun/c7-render/fixed~focus` | True | True | editor 5750294.660000 / 5750294.660000 | True |
| `c7-render` | oracle | `mlfq-s10000-b100000-q3-x2-c0.05` | `runs/rq0-gate-rerun/c7-render/oracle~focus` | True | True | editor 5750451.470000 / 5750451.470000 | True |

## Route under the g band and the boot defaults

| g | route |
|---|---|
| 0.25 | the table is rewritten |
| 0.33 | the table is rewritten |
| 0.5 | the table is rewritten |
| 0.67 | the table is rewritten |

| boot default | route |
|---|---|
| ostep | the table is rewritten |
| ostep-slice-500us | the table is rewritten |
| ostep-slice-700us | the table is rewritten |
| ostep-slice-1200us | the table is rewritten |
| ostep-slice-2000us | the table is rewritten |
| ostep-slice-5000us | the table is rewritten |
| ostep-slice-7000us | the table is rewritten |
| ostep-slice-12000us | the table is rewritten |
| ostep-slice-20000us | the table is rewritten |
| ostep-slice-30000us | the table is rewritten |
| ostep-slice-100000us | the table is rewritten |

## `c7-transcode`

pick: the failing file with headroom and the largest oracle improvement in the nine-file duplicate-heavy class: 0.865, gap 0.123. The row `mlfq-s10000-b100000-q3-x2-c0.05`; 450 of 470 points read.

Finding 2 — spread the prior table's row holds. The row's quantity 0.865175; the best point `fifo-c0.2` at 0.987614; better than the row by the floor or more on video-editor.

Of the prior table's 8 distinct configurations, 1 of the 8 read have a quantity at least the row's.

| term | fixed | row | best | spread (min – max) | floor |
|---|---|---|---|---|---|
| video-editor | 11127962.000000 | 1500322.000000 | 137833.000000 | 137833.000000 – 29435008.000000 | 1000.000000 |

| g | 0.25 | 0.33 | 0.5 | 0.67 |
|---|---|---|---|---|
| finding | 2 | 2 | 2 | 2 |

| boot default | point | finding |
|---|---|---|
| ostep | `mlfq-s10000-b100000-q3-x2-cnone` | 2 |
| ostep-slice-500us | `mlfq-s500-b100000-q3-x2-cnone` | 2 |
| ostep-slice-700us | `mlfq-s700-b100000-q3-x2-cnone` | 2 |
| ostep-slice-1200us | `mlfq-s1200-b100000-q3-x2-cnone` | 2 |
| ostep-slice-2000us | `mlfq-s2000-b100000-q3-x2-cnone` | 2 |
| ostep-slice-5000us | `mlfq-s5000-b100000-q3-x2-cnone` | 2 |
| ostep-slice-7000us | `mlfq-s7000-b100000-q3-x2-cnone` | 2 |
| ostep-slice-12000us | `mlfq-s12000-b100000-q3-x2-cnone` | 2 |
| ostep-slice-20000us | `mlfq-s20000-b100000-q3-x2-cnone` | 2 |
| ostep-slice-30000us | `mlfq-s30000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-100000us | `mlfq-s100000-b100000-q3-x2-cnone` | no reading |

With the 110 LOTTERY points removed: finding 2; no finding changes.

Out of the reading (20):

- `mlfq-s10000-b10000-q3-x2-cnone` — starvation_floor: video-editor: max ready_wait 167949276 exceeds 30000000; wait_check: video-editor waited 167949276 µs (ready_done)
- `mlfq-s12000-b10000-q3-x2-cnone` — starvation_floor: video-editor: max ready_wait 167949276 exceeds 30000000; wait_check: video-editor waited 167949276 µs (ready_done)
- `mlfq-s20000-b10000-q3-x2-cnone` — starvation_floor: video-editor: max ready_wait 167949276 exceeds 30000000; wait_check: video-editor waited 167949276 µs (ready_done)
- `mlfq-s30000-b10000-q3-x2-cnone` — starvation_floor: video-editor: max ready_wait 167949276 exceeds 30000000; wait_check: video-editor waited 167949276 µs (ready_done)
- `mlfq-s100000-b10000-q3-x2-cnone` — starvation_floor: video-editor: max ready_wait 167949276 exceeds 30000000; wait_check: video-editor waited 167949276 µs (ready_done)
- `mlfq-s100000-b100000-q3-x2-cnone` — starvation_floor: video-editor: max ready_wait 167949276 exceeds 30000000; wait_check: video-editor waited 167949276 µs (ready_done)
- `mlfq-s10000-b10000-q3-x2-c0.05` — wait_check: video-editor waited 167959437 µs (preempt_done)
- `mlfq-s12000-b10000-q3-x2-c0.05` — wait_check: video-editor waited 167959437 µs (preempt_done)
- `mlfq-s100000-b10000-q3-x2-c0.05` — wait_check: video-editor waited 167959437 µs (preempt_done)
- `mlfq-s100000-b100000-q3-x2-c0.05` — wait_check: video-editor waited 167959437 µs (preempt_done)
- `mlfq-s10000-b10000-q3-x2-c0.2` — wait_check: video-editor waited 167959437 µs (preempt_done)
- `mlfq-s12000-b10000-q3-x2-c0.2` — wait_check: video-editor waited 119090471 µs (preempt_done)
- `mlfq-s20000-b10000-q3-x2-c0.2` — wait_check: video-editor waited 167959437 µs (preempt_done)
- `mlfq-s10000-b10000-q3-x2-c0.333` — wait_check: video-editor waited 167959437 µs (preempt_done)
- `mlfq-s20000-b10000-q3-x2-c0.333` — wait_check: video-editor waited 167959437 µs (preempt_done)
- `mlfq-s12000-b10000-q3-x2-c0.5` — wait_check: video-editor waited 167959437 µs (preempt_done)
- `fifo-cnone` — starvation_floor: video-editor: max ready_wait 167949276 exceeds 30000000; wait_check: video-editor waited 167949276 µs (ready_done)
- `fifo-c0.333` — wait_check: video-editor waited 167959437 µs (preempt_done)
- `fifo-c0.5` — wait_check: video-editor waited 167959437 µs (preempt_done)
- `fifo-c0.95` — wait_check: video-editor waited 167959437 µs (preempt_done)

## `c7-gaming`

pick: the same in the low-duplicate class: 1.000, gap 0.427. The row `edf-s10000-c0.05`; 470 of 470 points read.

Finding 2 — spread the prior table's row holds. The row's quantity 1.000000; the best point `edf-s10000-c0.05` at 1.000000, tied with 65 more; better than the row by the floor on no term.

Of the prior table's 8 distinct configurations, 3 of the 8 read have a quantity at least the row's.

| term | fixed | row | best | spread (min – max) | floor |
|---|---|---|---|---|---|
| game.chain.1 | 1.000000 | 0.000000 | 0.000000 | 0.000000 – 1.000000 | 0.010000 |

| g | 0.25 | 0.33 | 0.5 | 0.67 |
|---|---|---|---|---|
| finding | 2 | 2 | 2 | 2 |

| boot default | point | finding |
|---|---|---|
| ostep | `mlfq-s10000-b100000-q3-x2-cnone` | 2 |
| ostep-slice-500us | `mlfq-s500-b100000-q3-x2-cnone` | 2 |
| ostep-slice-700us | `mlfq-s700-b100000-q3-x2-cnone` | 2 |
| ostep-slice-1200us | `mlfq-s1200-b100000-q3-x2-cnone` | 2 |
| ostep-slice-2000us | `mlfq-s2000-b100000-q3-x2-cnone` | 2 |
| ostep-slice-5000us | `mlfq-s5000-b100000-q3-x2-cnone` | 2 |
| ostep-slice-7000us | `mlfq-s7000-b100000-q3-x2-cnone` | 2 |
| ostep-slice-12000us | `mlfq-s12000-b100000-q3-x2-cnone` | 2 |
| ostep-slice-20000us | `mlfq-s20000-b100000-q3-x2-cnone` | 2 |
| ostep-slice-30000us | `mlfq-s30000-b100000-q3-x2-cnone` | 2 |
| ostep-slice-100000us | `mlfq-s100000-b100000-q3-x2-cnone` | 2 |

With the 110 LOTTERY points removed: finding 2; no finding changes.

## `c1-transcode`

pick: the failing file whose gap fell furthest below g: gap −2.011. The row `lottery-s10000-w0.333-c0.333`; 454 of 470 points read.

Finding 3 — spread the prior table missed. The row's quantity 0.005390; the best point `mlfq-s20000-b10000-q3-x2-c0.5` at 0.562098; better than the row by the floor or more on video-editor, batch.

| term | fixed | row | best | spread (min – max) | floor |
|---|---|---|---|---|---|
| video-editor | 447969.180000 | 430531.080000 | 57281.270000 | 52963.450000 – 26849416.310000 | 1000.000000 |
| batch | 3894612815.000000 | 4134853844.000000 | 4120378558.000000 | 3130852442.000000 – 4418992451.000000 | 1000.000000 |

| g | 0.25 | 0.33 | 0.5 | 0.67 |
|---|---|---|---|---|
| finding | 3 | 3 | 3 | 3 |

| boot default | point | finding |
|---|---|---|
| ostep | `mlfq-s10000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-500us | `mlfq-s500-b100000-q3-x2-cnone` | 3 |
| ostep-slice-700us | `mlfq-s700-b100000-q3-x2-cnone` | 3 |
| ostep-slice-1200us | `mlfq-s1200-b100000-q3-x2-cnone` | 3 |
| ostep-slice-2000us | `mlfq-s2000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-5000us | `mlfq-s5000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-7000us | `mlfq-s7000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-12000us | `mlfq-s12000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-20000us | `mlfq-s20000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-30000us | `mlfq-s30000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-100000us | `mlfq-s100000-b100000-q3-x2-cnone` | no reading |

With the 109 LOTTERY points removed (the row's own kept): finding 3; no finding changes.

Out of the reading (16):

- `mlfq-s10000-b10000-q3-x2-cnone` — starvation_floor: video-editor: max ready_wait 167953453 exceeds 30000000; wait_check: video-editor waited 167953453 µs (ready_done)
- `mlfq-s12000-b10000-q3-x2-cnone` — starvation_floor: video-editor: max ready_wait 167953453 exceeds 30000000; wait_check: video-editor waited 167953453 µs (ready_done)
- `mlfq-s20000-b10000-q3-x2-cnone` — starvation_floor: video-editor: max ready_wait 167953453 exceeds 30000000; wait_check: video-editor waited 167953453 µs (ready_done)
- `mlfq-s30000-b10000-q3-x2-cnone` — starvation_floor: video-editor: max ready_wait 167953453 exceeds 30000000; wait_check: video-editor waited 167953453 µs (ready_done)
- `mlfq-s100000-b10000-q3-x2-cnone` — starvation_floor: video-editor: max ready_wait 167953453 exceeds 30000000; wait_check: video-editor waited 167953453 µs (ready_done)
- `mlfq-s100000-b100000-q3-x2-cnone` — starvation_floor: video-editor: max ready_wait 167953453 exceeds 30000000; wait_check: video-editor waited 167953453 µs (ready_done)
- `mlfq-s10000-b10000-q3-x2-c0.05` — wait_check: video-editor waited 140045388 µs (preempt_done)
- `mlfq-s12000-b10000-q3-x2-c0.05` — wait_check: video-editor waited 140045388 µs (preempt_done)
- `mlfq-s20000-b10000-q3-x2-c0.05` — wait_check: video-editor waited 167959437 µs (preempt_done)
- `mlfq-s12000-b10000-q3-x2-c0.2` — wait_check: video-editor waited 167959437 µs (preempt_done)
- `mlfq-s10000-b10000-q3-x2-c0.333` — wait_check: video-editor waited 167959437 µs (preempt_done)
- `mlfq-s12000-b10000-q3-x2-c0.333` — wait_check: video-editor waited 140045388 µs (preempt_done)
- `mlfq-s10000-b10000-q3-x2-c0.5` — wait_check: video-editor waited 167959437 µs (preempt_done)
- `fifo-cnone` — starvation_floor: video-editor: max ready_wait 167953453 exceeds 30000000; wait_check: video-editor waited 167953453 µs (ready_done)
- `fifo-c0.2` — wait_check: video-editor waited 140045388 µs (preempt_done)
- `fifo-c0.333` — wait_check: video-editor waited 140045388 µs (preempt_done)

## `c7-dev`

no_headroom: the row worse than the boot default by the floor or more on a term. The row `mlfq-s10000-b100000-q3-x2-c0.05`; 470 of 470 points read.

Finding 3 — spread the prior table missed. The row's quantity -2.200282; the best point `mlfq-s10000-b10000-q3-x2-c0.95` at 0.683748; better than the row by the floor or more on editor.

| term | fixed | row | best | spread (min – max) | floor |
|---|---|---|---|---|---|
| editor | 1750097.400000 | 5600806.080000 | 553471.800000 | 553471.800000 – 11539495.000000 | 1000.000000 |

| g | 0.25 | 0.33 | 0.5 | 0.67 |
|---|---|---|---|---|
| finding | 3 | 3 | 3 | 3 |

| boot default | point | finding |
|---|---|---|
| ostep | `mlfq-s10000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-500us | `mlfq-s500-b100000-q3-x2-cnone` | 3 |
| ostep-slice-700us | `mlfq-s700-b100000-q3-x2-cnone` | 3 |
| ostep-slice-1200us | `mlfq-s1200-b100000-q3-x2-cnone` | 3 |
| ostep-slice-2000us | `mlfq-s2000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-5000us | `mlfq-s5000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-7000us | `mlfq-s7000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-12000us | `mlfq-s12000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-20000us | `mlfq-s20000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-30000us | `mlfq-s30000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-100000us | `mlfq-s100000-b100000-q3-x2-cnone` | 3 |

With the 110 LOTTERY points removed: finding 3; no finding changes.

## `c7-video-edit`

no_headroom: the row worse than the boot default by the floor or more on a term. The row `mlfq-s10000-b100000-q3-x2-c0.05`; 470 of 470 points read.

Finding 3 — spread the prior table missed. The row's quantity -0.703213; the best point `mlfq-s10000-b10000-q3-x2-c0.333` at 0.809428; better than the row by the floor or more on editor.

| term | fixed | row | best | spread (min – max) | floor |
|---|---|---|---|---|---|
| editor | 4750232.680000 | 8090656.020000 | 905260.300000 | 905260.300000 – 13125307.460000 | 1000.000000 |

| g | 0.25 | 0.33 | 0.5 | 0.67 |
|---|---|---|---|---|
| finding | 3 | 3 | 3 | 3 |

| boot default | point | finding |
|---|---|---|
| ostep | `mlfq-s10000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-500us | `mlfq-s500-b100000-q3-x2-cnone` | 3 |
| ostep-slice-700us | `mlfq-s700-b100000-q3-x2-cnone` | 3 |
| ostep-slice-1200us | `mlfq-s1200-b100000-q3-x2-cnone` | 3 |
| ostep-slice-2000us | `mlfq-s2000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-5000us | `mlfq-s5000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-7000us | `mlfq-s7000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-12000us | `mlfq-s12000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-20000us | `mlfq-s20000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-30000us | `mlfq-s30000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-100000us | `mlfq-s100000-b100000-q3-x2-cnone` | 3 |

With the 110 LOTTERY points removed: finding 3; no finding changes.

## `c7-compile`

no_headroom: the row worse than the boot default by the floor or more on a term. The row `mlfq-s10000-b100000-q3-x2-c0.05`; 438 of 470 points read.

Finding 3 — spread the prior table missed. The row's quantity -0.495088; the best point `mlfq-s100000-b100000-q3-x2-cnone` at 0.973678; better than the row by the floor or more on editor.

| term | fixed | row | best | spread (min – max) | floor |
|---|---|---|---|---|---|
| editor | 58431291.000000 | 87359931.000000 | 1538056.070000 | 1538056.070000 – 103557193.620000 | 1000.000000 |

| g | 0.25 | 0.33 | 0.5 | 0.67 |
|---|---|---|---|---|
| finding | 3 | 3 | 3 | 3 |

| boot default | point | finding |
|---|---|---|
| ostep | `mlfq-s10000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-500us | `mlfq-s500-b100000-q3-x2-cnone` | 3 |
| ostep-slice-700us | `mlfq-s700-b100000-q3-x2-cnone` | 3 |
| ostep-slice-1200us | `mlfq-s1200-b100000-q3-x2-cnone` | 3 |
| ostep-slice-2000us | `mlfq-s2000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-5000us | `mlfq-s5000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-7000us | `mlfq-s7000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-12000us | `mlfq-s12000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-20000us | `mlfq-s20000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-30000us | `mlfq-s30000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-100000us | `mlfq-s100000-b100000-q3-x2-cnone` | 3 |

With the 110 LOTTERY points removed: finding 3; no finding changes.

Out of the reading (32):

- `mlfq-s10000-b10000-q3-x2-c0.05` — wait_check: build.j1393.cc1 waited 131559515 µs (preempt_open)
- `mlfq-s12000-b10000-q3-x2-c0.05` — wait_check: build.j1378.as waited 145639733 µs (preempt_open)
- `mlfq-s20000-b10000-q3-x2-c0.05` — wait_check: build.j1377.cc1 waited 149240352 µs (preempt_open)
- `mlfq-s30000-b10000-q3-x2-c0.05` — wait_check: build.j1375.cc1 waited 150924448 µs (preempt_open)
- `mlfq-s100000-b10000-q3-x2-c0.05` — wait_check: build.j1378.cc1 waited 148685057 µs (preempt_open)
- `mlfq-s100000-b100000-q3-x2-c0.05` — wait_check: build.j1378.cc1 waited 148685268 µs (preempt_open)
- `mlfq-s10000-b10000-q3-x2-c0.2` — wait_check: build.j1380.as waited 146342748 µs (preempt_open)
- `mlfq-s12000-b10000-q3-x2-c0.2` — wait_check: build.j1389.cc1 waited 137652985 µs (preempt_open)
- `mlfq-s20000-b10000-q3-x2-c0.2` — wait_check: build.j1381.cc1 waited 145019413 µs (preempt_open)
- `mlfq-s30000-b10000-q3-x2-c0.2` — wait_check: build.j1378.cc1 waited 147578312 µs (preempt_open)
- `mlfq-s100000-b10000-q3-x2-c0.2` — wait_check: build.j1403.cc1 waited 121847600 µs (preempt_open)
- `mlfq-s100000-b100000-q3-x2-c0.2` — wait_check: build.j1403.cc1 waited 121872152 µs (preempt_open)
- `mlfq-s10000-b10000-q3-x2-c0.333` — wait_check: build.j1381.cc1 waited 145390637 µs (preempt_open)
- `mlfq-s12000-b10000-q3-x2-c0.333` — wait_check: build.j1385.cc1 waited 139588160 µs (preempt_open)
- `mlfq-s20000-b10000-q3-x2-c0.333` — wait_check: build.j1374.cc1 waited 150339522 µs (preempt_open)
- `mlfq-s30000-b10000-q3-x2-c0.333` — wait_check: build.j1378.cc1 waited 149125876 µs (preempt_open)
- `mlfq-s100000-b10000-q3-x2-c0.333` — wait_check: build.j1424.cc1 waited 99810965 µs (preempt_open)
- `mlfq-s100000-b100000-q3-x2-c0.333` — wait_check: build.j1425.cc1 waited 99671784 µs (preempt_open)
- `mlfq-s10000-b10000-q3-x2-c0.5` — wait_check: build.j1372.cc1 waited 152223832 µs (preempt_open)
- `mlfq-s12000-b10000-q3-x2-c0.5` — wait_check: build.j1372.as waited 151345987 µs (preempt_open)
- `mlfq-s20000-b10000-q3-x2-c0.5` — wait_check: build.j1390.cc1 waited 133644647 µs (preempt_open)
- `mlfq-s30000-b10000-q3-x2-c0.5` — wait_check: build.j1397.cc1 waited 127761300 µs (preempt_open)
- `mlfq-s100000-b10000-q3-x2-c0.5` — wait_check: build.j1377.cc1 waited 148613959 µs (preempt_open)
- `mlfq-s100000-b100000-q3-x2-c0.5` — wait_check: build.j1377.cc1 waited 148663801 µs (preempt_open)
- `mlfq-s10000-b10000-q3-x2-c0.95` — wait_check: build.j1439.cc1 waited 86858000 µs (preempt_open)
- `mlfq-s12000-b10000-q3-x2-c0.95` — wait_check: build.j1435.cc1 waited 73807669 µs (preempt_done)
- `mlfq-s20000-b10000-q3-x2-c0.95` — wait_check: build.j1383.cc1 waited 31601057 µs (preempt_done)
- `fifo-c0.05` — wait_check: build.j1406.cc1 waited 117453603 µs (preempt_open)
- `fifo-c0.2` — wait_check: build.j1413.cc1 waited 108811790 µs (preempt_open)
- `fifo-c0.333` — wait_check: build.j1409.as waited 113639467 µs (preempt_open)
- `fifo-c0.5` — wait_check: build.j1374.cc1 waited 142042880 µs (preempt_done)
- `fifo-c0.95` — wait_check: build.j1403.as waited 124277869 µs (preempt_done)

## `c1-render`

no_headroom: the row worse than the boot default by the floor or more on a term: its turnaround term; its latency term equal. The row `lottery-s10000-w0.333-c0.333`; 470 of 470 points read.

Finding 3 — spread the prior table missed. The row's quantity -0.010827; the best point `mlfq-s30000-b10000-q3-x2-c0.95` at 0.052574; better than the row by the floor or more on bulk.

| term | fixed | row | best | spread (min – max) | floor |
|---|---|---|---|---|---|
| editor | 535735.060000 | 535735.060000 | 535735.060000 | 535735.060000 – 14364437.900000 | 1000.000000 |
| bulk | 21394289.000000 | 22089192.000000 | 18019907.000000 | 16645723.000000 – 23609692.000000 | 1000.000000 |

| g | 0.25 | 0.33 | 0.5 | 0.67 |
|---|---|---|---|---|
| finding | 3 | 3 | 3 | 3 |

| boot default | point | finding |
|---|---|---|
| ostep | `mlfq-s10000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-500us | `mlfq-s500-b100000-q3-x2-cnone` | 3 |
| ostep-slice-700us | `mlfq-s700-b100000-q3-x2-cnone` | 3 |
| ostep-slice-1200us | `mlfq-s1200-b100000-q3-x2-cnone` | 3 |
| ostep-slice-2000us | `mlfq-s2000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-5000us | `mlfq-s5000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-7000us | `mlfq-s7000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-12000us | `mlfq-s12000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-20000us | `mlfq-s20000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-30000us | `mlfq-s30000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-100000us | `mlfq-s100000-b100000-q3-x2-cnone` | 2 |

With the 109 LOTTERY points removed (the row's own kept): finding 3; no finding changes.

## `c7-photo`

no_headroom: the row changing nothing past the floor. The row `mlfq-s10000-b100000-q3-x2-c0.05`; 470 of 470 points read.

Finding 3 — spread the prior table missed. The row's quantity 0.000000; the best point `fifo-c0.333` at 0.355833, tied with 2 more; better than the row by the floor or more on photo-editor.

| term | fixed | row | best | spread (min – max) | floor |
|---|---|---|---|---|---|
| photo-editor | 2978927.880000 | 2978927.880000 | 1918927.880000 | 1918927.880000 – 7273800.880000 | 1000.000000 |

| g | 0.25 | 0.33 | 0.5 | 0.67 |
|---|---|---|---|---|
| finding | 3 | 3 | 3 | 3 |

| boot default | point | finding |
|---|---|---|
| ostep | `mlfq-s10000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-500us | `mlfq-s500-b100000-q3-x2-cnone` | 2 |
| ostep-slice-700us | `mlfq-s700-b100000-q3-x2-cnone` | 2 |
| ostep-slice-1200us | `mlfq-s1200-b100000-q3-x2-cnone` | 2 |
| ostep-slice-2000us | `mlfq-s2000-b100000-q3-x2-cnone` | 2 |
| ostep-slice-5000us | `mlfq-s5000-b100000-q3-x2-cnone` | 2 |
| ostep-slice-7000us | `mlfq-s7000-b100000-q3-x2-cnone` | 2 |
| ostep-slice-12000us | `mlfq-s12000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-20000us | `mlfq-s20000-b100000-q3-x2-cnone` | 2 |
| ostep-slice-30000us | `mlfq-s30000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-100000us | `mlfq-s100000-b100000-q3-x2-cnone` | 3 |

With the 110 LOTTERY points removed: finding 3; no finding changes.

## `c7-ml-train`

no_headroom: the row changing nothing past the floor. The row `mlfq-s10000-b100000-q3-x2-c0.05`; 463 of 470 points read.

Finding 3 — spread the prior table missed. The row's quantity 0.000000; the best point `fifo-c0.95` at 0.897907; better than the row by the floor or more on editor.

| term | fixed | row | best | spread (min – max) | floor |
|---|---|---|---|---|---|
| editor | 8020850.480000 | 8020875.920000 | 818873.400000 | 818873.400000 – 258166809.120000 | 1000.000000 |

| g | 0.25 | 0.33 | 0.5 | 0.67 |
|---|---|---|---|---|
| finding | 3 | 3 | 3 | 3 |

| boot default | point | finding |
|---|---|---|
| ostep | `mlfq-s10000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-500us | `mlfq-s500-b100000-q3-x2-cnone` | 3 |
| ostep-slice-700us | `mlfq-s700-b100000-q3-x2-cnone` | 3 |
| ostep-slice-1200us | `mlfq-s1200-b100000-q3-x2-cnone` | 3 |
| ostep-slice-2000us | `mlfq-s2000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-5000us | `mlfq-s5000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-7000us | `mlfq-s7000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-12000us | `mlfq-s12000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-20000us | `mlfq-s20000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-30000us | `mlfq-s30000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-100000us | `mlfq-s100000-b100000-q3-x2-cnone` | no reading |

With the 110 LOTTERY points removed: finding 3; no finding changes.

Out of the reading (7):

- `mlfq-s10000-b10000-q3-x2-cnone` — starvation_floor: editor: max ready_wait 287997272 exceeds 30000000; wait_check: editor waited 287997272 µs (ready_done)
- `mlfq-s12000-b10000-q3-x2-cnone` — starvation_floor: editor: max ready_wait 287997272 exceeds 30000000; wait_check: editor waited 287997272 µs (ready_done)
- `mlfq-s20000-b10000-q3-x2-cnone` — starvation_floor: editor: max ready_wait 287997272 exceeds 30000000; wait_check: editor waited 287997272 µs (ready_done)
- `mlfq-s30000-b10000-q3-x2-cnone` — starvation_floor: editor: max ready_wait 287997272 exceeds 30000000; wait_check: editor waited 287997272 µs (ready_done)
- `mlfq-s100000-b10000-q3-x2-cnone` — starvation_floor: editor: max ready_wait 287997272 exceeds 30000000; wait_check: editor waited 287997272 µs (ready_done)
- `mlfq-s100000-b100000-q3-x2-cnone` — starvation_floor: editor: max ready_wait 287997272 exceeds 30000000; wait_check: editor waited 287997272 µs (ready_done)
- `fifo-cnone` — starvation_floor: editor: max ready_wait 287997272 exceeds 30000000; wait_check: editor waited 287997272 µs (ready_done)

## `c7-render`

no_headroom: the row changing nothing past the floor. The row `mlfq-s10000-b100000-q3-x2-c0.05`; 470 of 470 points read.

Finding 3 — spread the prior table missed. The row's quantity 0.000000; the best point `mlfq-s10000-b10000-q3-x2-c0.05` at 0.944258, tied with 1 more; better than the row by the floor or more on editor.

| term | fixed | row | best | spread (min – max) | floor |
|---|---|---|---|---|---|
| editor | 5750294.660000 | 5750451.470000 | 320533.990000 | 320533.990000 – 10511331.060000 | 1000.000000 |

| g | 0.25 | 0.33 | 0.5 | 0.67 |
|---|---|---|---|---|
| finding | 3 | 3 | 3 | 3 |

| boot default | point | finding |
|---|---|---|
| ostep | `mlfq-s10000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-500us | `mlfq-s500-b100000-q3-x2-cnone` | 3 |
| ostep-slice-700us | `mlfq-s700-b100000-q3-x2-cnone` | 3 |
| ostep-slice-1200us | `mlfq-s1200-b100000-q3-x2-cnone` | 3 |
| ostep-slice-2000us | `mlfq-s2000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-5000us | `mlfq-s5000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-7000us | `mlfq-s7000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-12000us | `mlfq-s12000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-20000us | `mlfq-s20000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-30000us | `mlfq-s30000-b100000-q3-x2-cnone` | 3 |
| ostep-slice-100000us | `mlfq-s100000-b100000-q3-x2-cnone` | 3 |

With the 110 LOTTERY points removed: finding 3; no finding changes.

## Statements

**findings.** Over a file's read points. Finding 1 — no spread: no two points differ on a scored term by the term's floor or more; the floor is the value below which a difference between two configurations is not read (metrics doc §10). Finding 3 — spread the prior table missed: the row's quantity is at most (1 − g) of the quantity of the best point, g = 0.5, and the best point is better than the row on a scored term by the floor or more. The row is the configuration the oracle applies; the best point is the read point with the highest quantity. Read on the table, the row captures at most half of the improvement the best point reaches over fixed. Finding 2 — spread the prior table's row holds: neither of the two.

**route-known.** The route rule is fixed after the RQ0 run's data were seen. On the runs on disk the four files of decision 2's first kind are at finding 3 before any search run — the boot default is a point of the grid and their row is worse than it by the floor or more — so the route is known before the search: the table is rewritten. On c7-gaming the row reaches a frame miss rate of 0 against fixed's 1, so no point can beat it; on c7-transcode the row's quantity is 0.865; on c1-transcode the row's quantity is 0.005, and 62 of the file's 100 random runs exceed it by more than 0.01, the best at 0.153. The search runs as the statement failure-procedure requires, and its per-file findings are what Phase 12 is designed from.

**boot-default-limit.** The search runs at the primary alone: the blessed files, fixed at the primary boot default. Each of the gate's ten alternative boot defaults is a point of the grid, so each file's finding is recomputed with that point in place of fixed; a finding that changes is reported as a range over the boot default. No variant file was searched.

**read-only.** The search is read-only: nothing it finds is written into a table (_dev/docs/rq0-preparation-notes.md §4.3: ignore labels, sweep the configuration space, observe the spread).
