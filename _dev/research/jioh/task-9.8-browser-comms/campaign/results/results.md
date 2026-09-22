# 9.8 desktop campaign — pooled results (meas-ci:desktop:2026-09-20)

Machine: EPYC 7763. Repeats pooled per subject; `probe` jobs are never repeats.

## chrome-hidden

Repeats: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  ·  mode full  ·  renderers measured {1: 12, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 12, 9: 12, 10: 12, 11: 12} (observed {1: '16', 2: '16', 3: '16', 4: '16', 5: '16', 6: '16', 7: '16', 8: '16', 9: '16', 10: '16', 11: '16'})

| quantity | k | mean | half-width | passes |
|---|---|---|---|---|
| steady HangWatcher wakes/s | 11 | 0.1 | ±0.0% | yes |
| steady HangWatcher gap mean (ms) | 11 | 10000.1292 | ±0.0% | yes |
| steady HangWatcher run mean (ms) | 11 | 0.0275 | ±6.4% | no |
| steady chrome wakes/s | 11 | 0.04 | ±0.0% | yes |
| steady chrome gap mean (ms) | 11 | 24438.1205 | ±3.2% | yes |
| steady chrome run mean (ms) | 11 | 0.0995 | ±5.0% | yes |
| steady residual wakes/s | 11 | 0.0104 | ±20.3% | no |
| steady residual gap mean (ms) | 11 | 70329.9897 | ±19.1% | no |
| steady residual run mean (ms) | 11 | 0.0923 | ±19.9% | no |

## chrome-visible

Repeats: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  ·  mode full  ·  renderers measured {1: 12, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 12, 9: 12, 10: 12, 11: 12} (observed {1: '13', 2: '13', 3: '13', 4: '13', 5: '13', 6: '13', 7: '13', 8: '13', 9: '14', 10: '13', 11: '13'})

| quantity | k | mean | half-width | passes |
|---|---|---|---|---|
| steady-notimer HangWatcher wakes/s | 11 | 0.1 | ±0.0% | yes |
| steady-notimer HangWatcher gap mean (ms) | 11 | 10000.1372 | ±0.0% | yes |
| steady-notimer HangWatcher run mean (ms) | 11 | 0.0318 | ±6.0% | no |
| steady-notimer chrome wakes/s | 11 | 0.0204 | ±3.0% | yes |
| steady-notimer chrome gap mean (ms) | 11 | 42965.8358 | ±3.7% | yes |
| steady-notimer chrome run mean (ms) | 11 | 0.1489 | ±5.8% | no |
| steady-notimer Chrome_ChildIOT wakes/s | 11 | 0.0047 | ±62.0% | no |
| steady-notimer Chrome_ChildIOT gap mean (ms) | 11 | 163506.0193 | ±19.5% | no |
| steady-notimer Chrome_ChildIOT run mean (ms) | 11 | 0.0408 | ±10.7% | no |
| steady-notimer ThreadPoolForeg wakes/s | 11 | 0.0043 | ±29.1% | no |
| steady-notimer ThreadPoolForeg gap mean (ms) | 11 | 1050.9345 | ±27.8% | no |
| steady-notimer ThreadPoolForeg run mean (ms) | 11 | 0.0254 | ±10.3% | no |
| steady-notimer residual wakes/s | 11 | 0.0108 | ±17.9% | no |
| steady-notimer residual gap mean (ms) | 11 | 76035.483 | ±13.6% | no |
| steady-notimer residual run mean (ms) | 11 | 0.1026 | ±14.5% | no |

| comparison | wakes/s a | wakes/s b | ratio | reading | cpu share a | cpu share b | ratio | reading |
|---|---|---|---|---|---|---|---|---|
| timer against no timer | 10.235327272727273 | 0.1408818181818182 | 72.652 | difference | 0.007834545454545453 | 9.545454545454547e-05 | 82.076 | difference |

## element

Repeats: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]  ·  mode full

| quantity | k | mean | half-width | passes |
|---|---|---|---|---|
| idle ThreadPoolForeg wakes/s | 17 | 4.2282 | ±1.9% | yes |
| idle ThreadPoolForeg gap mean (ms) | 17 | 1930.0934 | ±4.8% | yes |
| idle ThreadPoolForeg run mean (ms) | 17 | 0.0401 | ±2.8% | yes |
| idle element-desktop wakes/s | 17 | 3.8976 | ±0.5% | yes |
| idle element-desktop gap mean (ms) | 17 | 1788.0855 | ±0.5% | yes |
| idle element-desktop run mean (ms) | 17 | 0.1763 | ±3.1% | yes |
| idle Chrome_IOThread wakes/s | 17 | 1.8482 | ±0.6% | yes |
| idle Chrome_IOThread gap mean (ms) | 17 | 521.7188 | ±0.6% | yes |
| idle Chrome_IOThread run mean (ms) | 17 | 0.0252 | ±2.4% | yes |
| idle Chrome_ChildIOT wakes/s | 17 | 1.4835 | ±1.0% | yes |
| idle Chrome_ChildIOT gap mean (ms) | 17 | 2260.0 | ±2.5% | yes |
| idle Chrome_ChildIOT run mean (ms) | 17 | 0.0708 | ±3.3% | yes |
| idle ThreadPoolServi wakes/s | 17 | 0.3829 | ±1.0% | yes |
| idle ThreadPoolServi gap mean (ms) | 17 | 11532.4598 | ±2.7% | yes |
| idle ThreadPoolServi run mean (ms) | 17 | 0.0511 | ±3.8% | yes |
| idle residual wakes/s | 17 | 0.4698 | ±2.0% | yes |
| idle residual gap mean (ms) | 17 | 2068.1913 | ±2.1% | yes |
| idle residual run mean (ms) | 17 | 0.0353 | ±4.6% | yes |

| comparison | wakes/s a | wakes/s b | ratio | reading | cpu share a | cpu share b | ratio | reading |
|---|---|---|---|---|---|---|---|---|
| idle against scripted traffic (D11; feeds no archetype) | 12.315764705882353 | 49.0994705882353 | 0.251 | difference | 0.0010435294117647057 | 0.004343529411764706 | 0.24 | difference |

## steam

Repeats: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  ·  mode full

| quantity | k | mean | half-width | passes |
|---|---|---|---|---|
| shown steamwebhelper wakes/s | 12 | 70.75 | ±0.2% | yes |
| shown steamwebhelper gap mean (ms) | 12 | 32.4431 | ±10.2% | no |
| shown steamwebhelper run mean (ms) | 12 | 0.0696 | ±5.3% | no |
| shown steam wakes/s | 12 | 69.4667 | ±0.1% | yes |
| shown steam gap mean (ms) | 12 | 43.1793 | ±0.1% | yes |
| shown steam run mean (ms) | 12 | 0.0555 | ±10.2% | no |
| shown IPC:CSteamEngin wakes/s | 12 | 44.4942 | ±0.8% | yes |
| shown IPC:CSteamEngin gap mean (ms) | 12 | 44.9481 | ±0.8% | yes |
| shown IPC:CSteamEngin run mean (ms) | 12 | 0.0573 | ±8.8% | no |
| shown CJobMgr::m_Work wakes/s | 12 | 35.6283 | ±0.6% | yes |
| shown CJobMgr::m_Work gap mean (ms) | 12 | 84.1995 | ±0.6% | yes |
| shown CJobMgr::m_Work run mean (ms) | 12 | 0.0176 | ±6.2% | no |
| shown Compositor wakes/s | 12 | 18.6008 | ±0.9% | yes |
| shown Compositor gap mean (ms) | 12 | 53.7532 | ±0.9% | yes |
| shown Compositor run mean (ms) | 12 | 0.0562 | ±4.3% | yes |
| shown Chrome_ChildIOT wakes/s | 12 | 13.4275 | ±0.6% | yes |
| shown Chrome_ChildIOT gap mean (ms) | 12 | 219.692 | ±0.6% | yes |
| shown Chrome_ChildIOT run mean (ms) | 12 | 0.0312 | ±2.8% | yes |
| shown VizCompositorTh wakes/s | 12 | 10.54 | ±2.0% | yes |
| shown VizCompositorTh gap mean (ms) | 12 | 94.8866 | ±1.9% | yes |
| shown VizCompositorTh run mean (ms) | 12 | 0.0819 | ±5.5% | no |
| shown CHTTPClientThre wakes/s | 12 | 8.0458 | ±0.4% | yes |
| shown CHTTPClientThre gap mean (ms) | 12 | 248.5793 | ±0.4% | yes |
| shown CHTTPClientThre run mean (ms) | 12 | 0.0312 | ±46.0% | no |
| shown CNet Encrypt:0 wakes/s | 12 | 8.0383 | ±0.2% | yes |
| shown CNet Encrypt:0 gap mean (ms) | 12 | 248.7527 | ±0.2% | yes |
| shown CNet Encrypt:0 run mean (ms) | 12 | 0.0159 | ±4.0% | yes |
| shown ThreadPoolForeg wakes/s | 12 | 6.1717 | ±4.2% | yes |
| shown ThreadPoolForeg gap mean (ms) | 12 | 511.5989 | ±9.0% | no |
| shown ThreadPoolForeg run mean (ms) | 12 | 0.018 | ±5.0% | yes |
| shown residual wakes/s | 12 | 14.1526 | ±0.9% | yes |
| shown residual gap mean (ms) | 12 | 70.6633 | ±0.9% | yes |
| shown residual run mean (ms) | 12 | 0.0296 | ±4.5% | yes |

| comparison | wakes/s a | wakes/s b | ratio | reading | cpu share a | cpu share b | ratio | reading |
|---|---|---|---|---|---|---|---|---|
| shown against minimised (D5) | 299.325 | 244.398 | 1.225 | difference | 0.015184166666666667 | 0.012063333333333334 | 1.259 | difference |

