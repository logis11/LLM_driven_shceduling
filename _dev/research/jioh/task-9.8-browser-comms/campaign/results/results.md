# 9.8 desktop campaign — pooled results (meas-ci:desktop:2026-09-20)

Machine: EPYC 7763. Repeats pooled per subject; `probe` jobs are never repeats.

## chrome-hidden

Repeats: [1, 2, 3, 4, 5, 6, 7, 8, 9, '10@35585759158', '10@35585978825', '10@35586404781', '10@35586632429', 11, 12, 13, 14, 15, 16]  ·  mode full  ·  renderers measured {1: 12, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 12, 9: 12, '10@35585759158': 12, '10@35585978825': 12, '10@35586404781': 12, '10@35586632429': 12, 11: 12, 12: 12, 13: 12, 14: 12, 15: 12, 16: 12} (observed {1: '16', 2: '16', 3: '16', 4: '16', 5: '16', 6: '16', 7: '16', 8: '16', 9: '16', '10@35585759158': '16', '10@35585978825': '16', '10@35586404781': '16', '10@35586632429': '16', 11: '16', 12: '16', 13: '16', 14: '16', 15: '16', 16: '16'})  ·  builds Google Chrome 152.0.7977.82 (14 repeats), Google Chrome 153.0.8010.52 (5: 12, 13, 14, 15, 16)

| quantity | k | mean | half-width | passes |
|---|---|---|---|---|
| steady HangWatcher wakes/s | 19 | 0.1 | ±0.0% | yes |
| steady HangWatcher gap mean (ms) | 19 | 10000.0346 | ±0.0% | yes |
| steady HangWatcher run mean (ms) | 19 | 0.0267 | ±4.8% | yes |
| steady chrome wakes/s | 19 | 0.0389 | ±1.5% | yes |
| steady chrome gap mean (ms) | 19 | 25714.3747 | ±1.5% | yes |
| steady chrome run mean (ms) | 19 | 0.0955 | ±4.0% | yes |
| steady Chrome_ChildIOT wakes/s | 19 | 0.007 | ±18.5% | no |
| steady Chrome_ChildIOT gap mean (ms) | 19 | 142352.2096 | ±18.5% | no |
| steady Chrome_ChildIOT run mean (ms) | 19 | 0.029 | ±6.9% | no |
| steady Compositor wakes/s | 19 | 0.0065 | ±18.9% | no |
| steady Compositor gap mean (ms) | 19 | 154054.5871 | ±18.9% | no |
| steady Compositor run mean (ms) | 19 | 0.0202 | ±5.1% | no |
| steady PerfettoTrace wakes/s | 19 | 0.0065 | ±18.9% | no |
| steady PerfettoTrace gap mean (ms) | 19 | 154054.5871 | ±18.9% | no |
| steady PerfettoTrace run mean (ms) | 19 | 0.0192 | ±6.3% | no |
| steady ThreadPoolServi wakes/s | 19 | 0.0065 | ±18.9% | no |
| steady ThreadPoolServi gap mean (ms) | 19 | 154054.5871 | ±18.9% | no |
| steady ThreadPoolServi run mean (ms) | 19 | 0.0198 | ±4.3% | yes |
| steady residual wakes/s | 19 | 0.0033 | ±14.8% | no |
| steady residual gap mean (ms) | 19 | 302655.8761 | ±14.8% | no |
| steady residual run mean (ms) | 19 | 0.1883 | ±6.0% | no |

## chrome-visible

Repeats: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  ·  mode full  ·  renderers measured {1: 12, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 12, 9: 12, 10: 12, 11: 12} (observed {1: '13', 2: '13', 3: '13', 4: '13', 5: '13', 6: '13', 7: '13', 8: '13', 9: '14', 10: '13', 11: '13'})  ·  builds Google Chrome 152.0.7977.82 (11 repeats)

| quantity | k | mean | half-width | passes |
|---|---|---|---|---|
| steady-notimer HangWatcher wakes/s | 11 | 0.1 | ±0.0% | yes |
| steady-notimer HangWatcher gap mean (ms) | 11 | 10001.2987 | ±0.0% | yes |
| steady-notimer HangWatcher run mean (ms) | 11 | 0.032 | ±5.9% | no |
| steady-notimer chrome wakes/s | 11 | 0.0227 | ±3.8% | yes |
| steady-notimer chrome gap mean (ms) | 11 | 44098.154 | ±3.8% | yes |
| steady-notimer chrome run mean (ms) | 11 | 0.1493 | ±6.1% | no |
| steady-notimer Chrome_ChildIOT wakes/s | 11 | 0.006 | ±26.4% | no |
| steady-notimer Chrome_ChildIOT gap mean (ms) | 11 | 165345.0618 | ±26.4% | no |
| steady-notimer Chrome_ChildIOT run mean (ms) | 11 | 0.0386 | ±10.8% | no |
| steady-notimer PerfettoTrace wakes/s | 11 | 0.0054 | ±26.2% | no |
| steady-notimer PerfettoTrace gap mean (ms) | 11 | 186353.6108 | ±26.2% | no |
| steady-notimer PerfettoTrace run mean (ms) | 11 | 0.0241 | ±5.1% | no |
| steady-notimer residual wakes/s | 11 | 0.0068 | ±10.9% | no |
| steady-notimer residual gap mean (ms) | 11 | 146939.2653 | ±10.9% | no |
| steady-notimer residual run mean (ms) | 11 | 0.1459 | ±12.9% | no |

| comparison | wakes/s a | wakes/s b | ratio | reading | cpu share a | cpu share b | ratio | reading |
|---|---|---|---|---|---|---|---|---|
| timer against no timer | 10.235327272727273 | 0.1408818181818182 | 72.652 | difference | 0.007834545454545453 | 9.545454545454547e-05 | 82.076 | difference |

## element

Repeats: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, '17@35597073549', '17@35597185904']  ·  mode full  ·  builds ? (18 repeats)

| quantity | k | mean | half-width | passes |
|---|---|---|---|---|
| idle ThreadPoolForeg wakes/s | 18 | 4.2288 | ±1.8% | yes |
| idle ThreadPoolForeg gap mean (ms) | 18 | 236.4747 | ±1.8% | yes |
| idle ThreadPoolForeg run mean (ms) | 18 | 0.04 | ±2.7% | yes |
| idle element-desktop wakes/s | 18 | 3.8999 | ±0.5% | yes |
| idle element-desktop gap mean (ms) | 18 | 256.4172 | ±0.5% | yes |
| idle element-desktop run mean (ms) | 18 | 0.1759 | ±2.9% | yes |
| idle Chrome_IOThread wakes/s | 18 | 1.8527 | ±0.6% | yes |
| idle Chrome_IOThread gap mean (ms) | 18 | 539.759 | ±0.6% | yes |
| idle Chrome_IOThread run mean (ms) | 18 | 0.0252 | ±2.2% | yes |
| idle Chrome_ChildIOT wakes/s | 18 | 1.4841 | ±0.9% | yes |
| idle Chrome_ChildIOT gap mean (ms) | 18 | 673.8232 | ±0.9% | yes |
| idle Chrome_ChildIOT run mean (ms) | 18 | 0.0706 | ±3.2% | yes |
| idle ThreadPoolServi wakes/s | 18 | 0.3844 | ±0.9% | yes |
| idle ThreadPoolServi gap mean (ms) | 18 | 2601.1652 | ±0.9% | yes |
| idle ThreadPoolServi run mean (ms) | 18 | 0.0508 | ±3.9% | yes |
| idle residual wakes/s | 18 | 0.4695 | ±1.9% | yes |
| idle residual gap mean (ms) | 18 | 2129.7645 | ±1.9% | yes |
| idle residual run mean (ms) | 18 | 0.0352 | ±4.3% | yes |

| comparison | wakes/s a | wakes/s b | ratio | reading | cpu share a | cpu share b | ratio | reading |
|---|---|---|---|---|---|---|---|---|
| idle against scripted traffic (D11; feeds no archetype) | 12.319444444444445 | 49.14994444444444 | 0.251 | difference | 0.0010422222222222222 | 0.004336111111111111 | 0.24 | difference |

## steam

Repeats: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  ·  mode full  ·  builds ? (12 repeats)

| quantity | k | mean | half-width | passes |
|---|---|---|---|---|
| shown steamwebhelper wakes/s | 12 | 70.7489 | ±0.2% | yes |
| shown steamwebhelper gap mean (ms) | 12 | 14.1345 | ±0.2% | yes |
| shown steamwebhelper run mean (ms) | 12 | 0.0695 | ±5.3% | no |
| shown steam wakes/s | 12 | 69.4671 | ±0.1% | yes |
| shown steam gap mean (ms) | 12 | 14.3953 | ±0.1% | yes |
| shown steam run mean (ms) | 12 | 0.0554 | ±10.1% | no |
| shown IPC:CSteamEngin wakes/s | 12 | 44.496 | ±0.8% | yes |
| shown IPC:CSteamEngin gap mean (ms) | 12 | 22.4739 | ±0.8% | yes |
| shown IPC:CSteamEngin run mean (ms) | 12 | 0.0574 | ±8.8% | no |
| shown CJobMgr::m_Work wakes/s | 12 | 35.6288 | ±0.6% | yes |
| shown CJobMgr::m_Work gap mean (ms) | 12 | 28.0672 | ±0.6% | yes |
| shown CJobMgr::m_Work run mean (ms) | 12 | 0.0176 | ±5.7% | yes |
| shown Compositor wakes/s | 12 | 18.601 | ±0.9% | yes |
| shown Compositor gap mean (ms) | 12 | 53.7604 | ±0.9% | yes |
| shown Compositor run mean (ms) | 12 | 0.0563 | ±4.3% | yes |
| shown Chrome_ChildIOT wakes/s | 12 | 13.4293 | ±0.6% | yes |
| shown Chrome_ChildIOT gap mean (ms) | 12 | 74.4642 | ±0.6% | yes |
| shown Chrome_ChildIOT run mean (ms) | 12 | 0.0311 | ±3.0% | yes |
| shown VizCompositorTh wakes/s | 12 | 10.5416 | ±2.0% | yes |
| shown VizCompositorTh gap mean (ms) | 12 | 94.862 | ±2.0% | yes |
| shown VizCompositorTh run mean (ms) | 12 | 0.0818 | ±5.6% | no |
| shown CNet Encrypt:0 wakes/s | 12 | 8.0401 | ±0.2% | yes |
| shown CNet Encrypt:0 gap mean (ms) | 12 | 124.3764 | ±0.2% | yes |
| shown CNet Encrypt:0 run mean (ms) | 12 | 0.0161 | ±4.0% | yes |
| shown CHTTPClientThre wakes/s | 12 | 8.0378 | ±0.3% | yes |
| shown CHTTPClientThre gap mean (ms) | 12 | 124.4129 | ±0.3% | yes |
| shown CHTTPClientThre run mean (ms) | 12 | 0.0162 | ±3.7% | yes |
| shown ThreadPoolForeg wakes/s | 12 | 6.1732 | ±4.2% | yes |
| shown ThreadPoolForeg gap mean (ms) | 12 | 161.9912 | ±4.2% | yes |
| shown ThreadPoolForeg run mean (ms) | 12 | 0.018 | ±5.1% | yes |
| shown residual wakes/s | 12 | 14.1526 | ±0.9% | yes |
| shown residual gap mean (ms) | 12 | 70.6584 | ±0.9% | yes |
| shown residual run mean (ms) | 12 | 0.0296 | ±4.5% | yes |

Rare event in the shown phase (D33): `CHTTPClientThre`'s runs of 1 ms or more, 62 over 7200 s (0.008611 a second), left out of the component; per repeat {1: 0, 2: 0, 3: 0, 4: 15, 5: 17, 6: 18, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 12}.

Rare event in the minimised phase (D33): `CHTTPClientThre`'s runs of 1 ms or more, 89 over 7200 s (0.012361 a second), left out of the component; per repeat {1: 0, 2: 4, 3: 11, 4: 0, 5: 0, 6: 0, 7: 11, 8: 10, 9: 17, 10: 8, 11: 17, 12: 11}.

| comparison | wakes/s a | wakes/s b | ratio | reading | cpu share a | cpu share b | ratio | reading |
|---|---|---|---|---|---|---|---|---|
| shown against minimised (D5) | 299.31641666666667 | 244.3855 | 1.225 | difference | 0.015060833333333334 | 0.011855 | 1.27 | difference |

