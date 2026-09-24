# 9.8 desktop campaign — pooled results (meas-ci:desktop:2026-09-20)

Machine: EPYC 7763. Repeats pooled per subject; `probe` jobs are never repeats.

## chrome-hidden

Repeats: [1, 2, 3, 4, 5, 6, 7, 8, 9, '10@35585759158', '10@35585978825', '10@35586404781', '10@35586632429', 11]  ·  mode full  ·  renderers measured {1: 12, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 12, 9: 12, '10@35585759158': 12, '10@35585978825': 12, '10@35586404781': 12, '10@35586632429': 12, 11: 12} (observed {1: '16', 2: '16', 3: '16', 4: '16', 5: '16', 6: '16', 7: '16', 8: '16', 9: '16', '10@35585759158': '16', '10@35585978825': '16', '10@35586404781': '16', '10@35586632429': '16', 11: '16'})

| quantity | k | mean | half-width | passes |
|---|---|---|---|---|
| steady HangWatcher wakes/s | 14 | 0.1 | ±0.0% | yes |
| steady HangWatcher gap mean (ms) | 14 | 10000.035 | ±0.0% | yes |
| steady HangWatcher run mean (ms) | 14 | 0.0274 | ±5.3% | no |
| steady chrome wakes/s | 14 | 0.039 | ±2.0% | yes |
| steady chrome gap mean (ms) | 14 | 25664.3246 | ±2.0% | yes |
| steady chrome run mean (ms) | 14 | 0.0977 | ±4.4% | yes |
| steady Chrome_ChildIOT wakes/s | 14 | 0.0071 | ±20.9% | no |
| steady Chrome_ChildIOT gap mean (ms) | 14 | 172501.6939 | ±35.0% | no |
| steady Chrome_ChildIOT run mean (ms) | 14 | 0.0321 | ±14.1% | no |
| steady Compositor wakes/s | 14 | 0.0065 | ±21.9% | no |
| steady Compositor gap mean (ms) | 14 | 194286.3971 | ±39.8% | no |
| steady Compositor run mean (ms) | 14 | 0.0207 | ±6.3% | no |
| steady PerfettoTrace wakes/s | 14 | 0.0065 | ±21.9% | no |
| steady PerfettoTrace gap mean (ms) | 14 | 194286.3971 | ±39.8% | no |
| steady PerfettoTrace run mean (ms) | 14 | 0.0202 | ±5.8% | no |
| steady ThreadPoolServi wakes/s | 14 | 0.0065 | ±21.9% | no |
| steady ThreadPoolServi gap mean (ms) | 14 | 194286.3971 | ±39.8% | no |
| steady ThreadPoolServi run mean (ms) | 14 | 0.0199 | ±4.8% | yes |
| steady residual wakes/s | 14 | 0.0035 | ±18.3% | no |
| steady residual gap mean (ms) | 14 | 308923.3851 | ±15.6% | no |
| steady residual run mean (ms) | 14 | 0.1924 | ±8.8% | no |

## chrome-visible

Repeats: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  ·  mode full  ·  renderers measured {1: 12, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 12, 9: 12, 10: 12, 11: 12} (observed {1: '13', 2: '13', 3: '13', 4: '13', 5: '13', 6: '13', 7: '13', 8: '13', 9: '14', 10: '13', 11: '13'})

| quantity | k | mean | half-width | passes |
|---|---|---|---|---|
| steady-notimer HangWatcher wakes/s | 11 | 0.1 | ±0.0% | yes |
| steady-notimer HangWatcher gap mean (ms) | 11 | 10001.3003 | ±0.0% | yes |
| steady-notimer HangWatcher run mean (ms) | 11 | 0.0318 | ±6.0% | no |
| steady-notimer chrome wakes/s | 11 | 0.0227 | ±3.8% | yes |
| steady-notimer chrome gap mean (ms) | 11 | 44213.0045 | ±3.4% | yes |
| steady-notimer chrome run mean (ms) | 11 | 0.1489 | ±5.8% | no |
| steady-notimer Chrome_ChildIOT wakes/s | 11 | 0.006 | ±26.4% | no |
| steady-notimer Chrome_ChildIOT gap mean (ms) | 11 | 196533.0305 | ±33.8% | no |
| steady-notimer Chrome_ChildIOT run mean (ms) | 11 | 0.0408 | ±10.7% | no |
| steady-notimer PerfettoTrace wakes/s | 11 | 0.0054 | ±26.2% | no |
| steady-notimer PerfettoTrace gap mean (ms) | 11 | 227163.6253 | ±40.0% | no |
| steady-notimer PerfettoTrace run mean (ms) | 11 | 0.0241 | ±5.1% | no |
| steady-notimer residual wakes/s | 11 | 0.0068 | ±10.9% | no |
| steady-notimer residual gap mean (ms) | 11 | 149880.0265 | ±9.0% | no |
| steady-notimer residual run mean (ms) | 11 | 0.1434 | ±11.0% | no |

| comparison | wakes/s a | wakes/s b | ratio | reading | cpu share a | cpu share b | ratio | reading |
|---|---|---|---|---|---|---|---|---|
| timer against no timer | 10.235327272727273 | 0.1408818181818182 | 72.652 | difference | 0.007834545454545453 | 9.545454545454547e-05 | 82.076 | difference |

## element

Repeats: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, '17@35597073549', '17@35597185904']  ·  mode full

| quantity | k | mean | half-width | passes |
|---|---|---|---|---|
| idle ThreadPoolForeg wakes/s | 18 | 4.2288 | ±1.8% | yes |
| idle ThreadPoolForeg gap mean (ms) | 18 | 236.7663 | ±1.8% | yes |
| idle ThreadPoolForeg run mean (ms) | 18 | 0.04 | ±2.7% | yes |
| idle element-desktop wakes/s | 18 | 3.8999 | ±0.5% | yes |
| idle element-desktop gap mean (ms) | 18 | 256.4426 | ±0.5% | yes |
| idle element-desktop run mean (ms) | 18 | 0.176 | ±2.9% | yes |
| idle Chrome_IOThread wakes/s | 18 | 1.8527 | ±0.6% | yes |
| idle Chrome_IOThread gap mean (ms) | 18 | 539.8377 | ±0.6% | yes |
| idle Chrome_IOThread run mean (ms) | 18 | 0.0252 | ±2.3% | yes |
| idle Chrome_ChildIOT wakes/s | 18 | 1.4841 | ±0.9% | yes |
| idle Chrome_ChildIOT gap mean (ms) | 18 | 674.0543 | ±0.9% | yes |
| idle Chrome_ChildIOT run mean (ms) | 18 | 0.0706 | ±3.2% | yes |
| idle ThreadPoolServi wakes/s | 18 | 0.3844 | ±0.9% | yes |
| idle ThreadPoolServi gap mean (ms) | 18 | 2601.9065 | ±0.9% | yes |
| idle ThreadPoolServi run mean (ms) | 18 | 0.0509 | ±3.7% | yes |
| idle residual wakes/s | 18 | 0.4695 | ±1.9% | yes |
| idle residual gap mean (ms) | 18 | 2132.6326 | ±1.9% | yes |
| idle residual run mean (ms) | 18 | 0.0353 | ±4.3% | yes |

| comparison | wakes/s a | wakes/s b | ratio | reading | cpu share a | cpu share b | ratio | reading |
|---|---|---|---|---|---|---|---|---|
| idle against scripted traffic (D11; feeds no archetype) | 12.319444444444445 | 49.14994444444444 | 0.251 | difference | 0.0010422222222222222 | 0.004336111111111111 | 0.24 | difference |

## steam

Repeats: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  ·  mode full

| quantity | k | mean | half-width | passes |
|---|---|---|---|---|
| shown steamwebhelper wakes/s | 12 | 70.7489 | ±0.2% | yes |
| shown steamwebhelper gap mean (ms) | 12 | 14.1346 | ±0.2% | yes |
| shown steamwebhelper run mean (ms) | 12 | 0.0696 | ±5.3% | no |
| shown steam wakes/s | 12 | 69.4671 | ±0.1% | yes |
| shown steam gap mean (ms) | 12 | 14.3953 | ±0.1% | yes |
| shown steam run mean (ms) | 12 | 0.0555 | ±10.2% | no |
| shown IPC:CSteamEngin wakes/s | 12 | 44.496 | ±0.8% | yes |
| shown IPC:CSteamEngin gap mean (ms) | 12 | 22.4773 | ±0.8% | yes |
| shown IPC:CSteamEngin run mean (ms) | 12 | 0.0573 | ±8.8% | no |
| shown CJobMgr::m_Work wakes/s | 12 | 35.6288 | ±0.6% | yes |
| shown CJobMgr::m_Work gap mean (ms) | 12 | 28.0693 | ±0.6% | yes |
| shown CJobMgr::m_Work run mean (ms) | 12 | 0.0176 | ±6.2% | no |
| shown Compositor wakes/s | 12 | 18.601 | ±0.9% | yes |
| shown Compositor gap mean (ms) | 12 | 53.7701 | ±0.9% | yes |
| shown Compositor run mean (ms) | 12 | 0.0562 | ±4.3% | yes |
| shown Chrome_ChildIOT wakes/s | 12 | 13.4293 | ±0.6% | yes |
| shown Chrome_ChildIOT gap mean (ms) | 12 | 74.471 | ±0.6% | yes |
| shown Chrome_ChildIOT run mean (ms) | 12 | 0.0312 | ±2.8% | yes |
| shown VizCompositorTh wakes/s | 12 | 10.5416 | ±2.0% | yes |
| shown VizCompositorTh gap mean (ms) | 12 | 94.9431 | ±1.9% | yes |
| shown VizCompositorTh run mean (ms) | 12 | 0.0819 | ±5.5% | no |
| shown CHTTPClientThre wakes/s | 12 | 8.0464 | ±0.4% | yes |
| shown CHTTPClientThre gap mean (ms) | 12 | 124.2842 | ±0.4% | yes |
| shown CHTTPClientThre run mean (ms) | 12 | 0.0312 | ±46.0% | no |
| shown CNet Encrypt:0 wakes/s | 12 | 8.0401 | ±0.2% | yes |
| shown CNet Encrypt:0 gap mean (ms) | 12 | 124.3779 | ±0.2% | yes |
| shown CNet Encrypt:0 run mean (ms) | 12 | 0.0159 | ±4.0% | yes |
| shown ThreadPoolForeg wakes/s | 12 | 6.1732 | ±4.2% | yes |
| shown ThreadPoolForeg gap mean (ms) | 12 | 162.6334 | ±4.2% | yes |
| shown ThreadPoolForeg run mean (ms) | 12 | 0.018 | ±5.0% | yes |
| shown residual wakes/s | 12 | 14.1526 | ±0.9% | yes |
| shown residual gap mean (ms) | 12 | 70.6709 | ±0.9% | yes |
| shown residual run mean (ms) | 12 | 0.0296 | ±4.5% | yes |

| comparison | wakes/s a | wakes/s b | ratio | reading | cpu share a | cpu share b | ratio | reading |
|---|---|---|---|---|---|---|---|---|
| shown against minimised (D5) | 299.325 | 244.398 | 1.225 | difference | 0.015184166666666667 | 0.012063333333333334 | 1.259 | difference |

