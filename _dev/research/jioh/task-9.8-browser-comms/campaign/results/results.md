# 9.8 desktop campaign — pooled results (meas-ci:desktop:2026-09-20)

Machine: EPYC 7763. Repeats pooled per subject; `probe` jobs are never repeats.

## chrome-hidden

Repeats: [1, 2, 3, 4, 5, 6, 7, 8, 9, '10@35585759158', '10@35585978825', '10@35586404781', '10@35586632429', 11, 12, 13, 14, 15, 16]  ·  mode full  ·  renderers measured {1: 12, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 12, 9: 12, '10@35585759158': 12, '10@35585978825': 12, '10@35586404781': 12, '10@35586632429': 12, 11: 12, 12: 12, 13: 12, 14: 12, 15: 12, 16: 12} (observed {1: '16', 2: '16', 3: '16', 4: '16', 5: '16', 6: '16', 7: '16', 8: '16', 9: '16', '10@35585759158': '16', '10@35585978825': '16', '10@35586404781': '16', '10@35586632429': '16', 11: '16', 12: '16', 13: '16', 14: '16', 15: '16', 16: '16'})  ·  builds Google Chrome 152.0.7977.82 (14 repeats), Google Chrome 153.0.8010.52 (5: 12, 13, 14, 15, 16)

| quantity | k | mean | half-width | passes |
|---|---|---|---|---|
| steady HangWatcher wakes/s | 19 | 0.0998 | ±0.1% | yes |
| steady HangWatcher gap mean (ms) | 19 | 10022.0127 | ±0.1% | yes |
| steady HangWatcher run mean (ms) | 19 | 0.0267 | ±4.8% | yes |
| steady chrome wakes/s | 19 | 0.0389 | ±1.5% | yes |
| steady chrome gap mean (ms) | 19 | 25724.0454 | ±1.5% | yes |
| steady chrome run mean (ms) | 19 | 0.0955 | ±4.0% | yes |
| steady Chrome_ChildIOT wakes/s | 19 | 0.007 | ±18.5% | no |
| steady Chrome_ChildIOT gap mean (ms) | 19 | 142352.2096 | ±18.5% | no |
| steady Chrome_ChildIOT run mean (ms) | 19 | 0.029 | ±6.9% | no |
| steady PerfettoTrace wakes/s | 19 | 0.0065 | ±18.9% | no |
| steady PerfettoTrace gap mean (ms) | 19 | 154054.5871 | ±18.9% | no |
| steady PerfettoTrace run mean (ms) | 19 | 0.0192 | ±6.3% | no |
| steady Compositor wakes/s | 19 | 0.0065 | ±19.0% | no |
| steady Compositor gap mean (ms) | 19 | 154228.2676 | ±19.0% | no |
| steady Compositor run mean (ms) | 19 | 0.0202 | ±5.1% | no |
| steady ThreadPoolServi wakes/s | 19 | 0.0065 | ±18.8% | no |
| steady ThreadPoolServi gap mean (ms) | 19 | 154228.2676 | ±18.8% | no |
| steady ThreadPoolServi run mean (ms) | 19 | 0.0198 | ±4.3% | yes |
| steady residual wakes/s | 19 | 0.0033 | ±14.8% | no |
| steady residual gap mean (ms) | 19 | 302655.8761 | ±14.8% | no |
| steady residual run mean (ms) | 19 | 0.1883 | ±6.0% | no |

## chrome-visible

Repeats: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  ·  mode full  ·  renderers measured {1: 12, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 12, 9: 12, 10: 12, 11: 12} (observed {1: '13', 2: '13', 3: '13', 4: '13', 5: '13', 6: '13', 7: '13', 8: '13', 9: '14', 10: '13', 11: '13'})  ·  builds Google Chrome 152.0.7977.82 (11 repeats)

| quantity | k | mean | half-width | passes |
|---|---|---|---|---|
| steady-notimer HangWatcher wakes/s | 11 | 0.0998 | ±0.1% | yes |
| steady-notimer HangWatcher gap mean (ms) | 11 | 10020.2789 | ±0.1% | yes |
| steady-notimer HangWatcher run mean (ms) | 11 | 0.032 | ±6.0% | no |
| steady-notimer chrome wakes/s | 11 | 0.0227 | ±3.8% | yes |
| steady-notimer chrome gap mean (ms) | 11 | 44147.3158 | ±3.8% | yes |
| steady-notimer chrome run mean (ms) | 11 | 0.1493 | ±6.0% | no |
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

Repeats: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, '17@35597073549', '17@35597185904']  ·  mode full  ·  builds Element 1.12.28 (18 repeats)

| quantity | k | mean | half-width | passes |
|---|---|---|---|---|
| idle element-desktop wakes/s | 18 | 2.6121 | ±0.2% | yes |
| idle element-desktop gap mean (ms) | 18 | 382.8307 | ±0.2% | yes |
| idle element-desktop run mean (ms) | 18 | 0.1418 | ±4.2% | yes |
| idle ThreadPoolForeg wakes/s | 18 | 2.151 | ±2.6% | yes |
| idle ThreadPoolForeg gap mean (ms) | 18 | 464.8977 | ±2.6% | yes |
| idle ThreadPoolForeg run mean (ms) | 18 | 0.0389 | ±3.9% | yes |
| idle ThreadPoolServi wakes/s | 18 | 0.3785 | ±0.8% | yes |
| idle ThreadPoolServi gap mean (ms) | 18 | 2641.8879 | ±0.8% | yes |
| idle ThreadPoolServi run mean (ms) | 18 | 0.0512 | ±3.8% | yes |
| idle Chrome_ChildIOT wakes/s | 18 | 0.2858 | ±1.1% | yes |
| idle Chrome_ChildIOT gap mean (ms) | 18 | 3498.5545 | ±1.1% | yes |
| idle Chrome_ChildIOT run mean (ms) | 18 | 0.0391 | ±3.1% | yes |
| idle Chrome_IOThread wakes/s | 18 | 0.2129 | ±3.0% | yes |
| idle Chrome_IOThread gap mean (ms) | 18 | 4697.7111 | ±3.0% | yes |
| idle Chrome_IOThread run mean (ms) | 18 | 0.0488 | ±7.7% | no |
| idle ThreadPoolForeg [event] wakes/s | 18 | 2.0778 | ±1.7% | yes |
| idle ThreadPoolForeg [event] gap mean (ms) | 18 | 481.2851 | ±1.7% | yes |
| idle ThreadPoolForeg [event] run mean (ms) | 18 | 0.0412 | ±2.4% | yes |
| idle Chrome_IOThread [event] wakes/s | 18 | 1.6398 | ±0.8% | yes |
| idle Chrome_IOThread [event] gap mean (ms) | 18 | 609.8271 | ±0.8% | yes |
| idle Chrome_IOThread [event] run mean (ms) | 18 | 0.0221 | ±1.7% | yes |
| idle element-desktop [event] wakes/s | 18 | 1.2878 | ±1.7% | yes |
| idle element-desktop [event] gap mean (ms) | 18 | 776.5342 | ±1.7% | yes |
| idle element-desktop [event] run mean (ms) | 18 | 0.245 | ±2.0% | yes |
| idle Chrome_ChildIOT [event] wakes/s | 18 | 1.1982 | ±1.0% | yes |
| idle Chrome_ChildIOT [event] gap mean (ms) | 18 | 834.5598 | ±1.0% | yes |
| idle Chrome_ChildIOT [event] run mean (ms) | 18 | 0.0781 | ±3.3% | yes |
| idle residual wakes/s | 18 | 0.275 | ±2.4% | yes |
| idle residual gap mean (ms) | 18 | 3636.3758 | ±2.4% | yes |
| idle residual run mean (ms) | 18 | 0.0261 | ±3.6% | yes |
| idle residual [event] wakes/s | 18 | 0.2005 | ±3.3% | yes |
| idle residual [event] gap mean (ms) | 18 | 4988.4693 | ±3.3% | yes |
| idle residual [event] run mean (ms) | 18 | 0.0474 | ±7.2% | no |

| comparison | wakes/s a | wakes/s b | ratio | reading | cpu share a | cpu share b | ratio | reading |
|---|---|---|---|---|---|---|---|---|
| idle against scripted traffic (D11; feeds no archetype) | 12.319444444444445 | 49.14994444444444 | 0.251 | difference | 0.0010422222222222222 | 0.004336111111111111 | 0.24 | difference |

## steam

Repeats: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  ·  mode full  ·  builds Steam client build 1788652215 (12 repeats)

| quantity | k | mean | half-width | passes |
|---|---|---|---|---|
| shown steamwebhelper wakes/s | 12 | 70.6581 | ±0.2% | yes |
| shown steamwebhelper gap mean (ms) | 12 | 14.1527 | ±0.2% | yes |
| shown steamwebhelper run mean (ms) | 12 | 0.0695 | ±5.3% | no |
| shown steam wakes/s | 12 | 69.3653 | ±0.1% | yes |
| shown steam gap mean (ms) | 12 | 14.4164 | ±0.1% | yes |
| shown steam run mean (ms) | 12 | 0.0554 | ±10.1% | no |
| shown IPC:CSteamEngin wakes/s | 12 | 43.856 | ±0.8% | yes |
| shown IPC:CSteamEngin gap mean (ms) | 12 | 22.8019 | ±0.8% | yes |
| shown IPC:CSteamEngin run mean (ms) | 12 | 0.0578 | ±8.8% | no |
| shown CJobMgr::m_Work wakes/s | 12 | 35.5449 | ±0.6% | yes |
| shown CJobMgr::m_Work gap mean (ms) | 12 | 28.1335 | ±0.6% | yes |
| shown CJobMgr::m_Work run mean (ms) | 12 | 0.0175 | ±5.8% | no |
| shown Compositor wakes/s | 12 | 18.5727 | ±0.9% | yes |
| shown Compositor gap mean (ms) | 12 | 53.8424 | ±0.9% | yes |
| shown Compositor run mean (ms) | 12 | 0.0563 | ±4.3% | yes |
| shown Chrome_ChildIOT wakes/s | 12 | 13.4063 | ±0.6% | yes |
| shown Chrome_ChildIOT gap mean (ms) | 12 | 74.5916 | ±0.6% | yes |
| shown Chrome_ChildIOT run mean (ms) | 12 | 0.031 | ±3.1% | yes |
| shown VizCompositorTh wakes/s | 12 | 10.5286 | ±2.0% | yes |
| shown VizCompositorTh gap mean (ms) | 12 | 94.9796 | ±2.0% | yes |
| shown VizCompositorTh run mean (ms) | 12 | 0.0818 | ±5.6% | no |
| shown CNet Encrypt:0 wakes/s | 12 | 8.0279 | ±0.2% | yes |
| shown CNet Encrypt:0 gap mean (ms) | 12 | 124.5657 | ±0.2% | yes |
| shown CNet Encrypt:0 run mean (ms) | 12 | 0.0161 | ±3.9% | yes |
| shown CHTTPClientThre wakes/s | 12 | 8.0158 | ±0.2% | yes |
| shown CHTTPClientThre gap mean (ms) | 12 | 124.7535 | ±0.2% | yes |
| shown CHTTPClientThre run mean (ms) | 12 | 0.016 | ±3.5% | yes |
| shown ThreadPoolForeg wakes/s | 12 | 6.0843 | ±4.2% | yes |
| shown ThreadPoolForeg gap mean (ms) | 12 | 164.3578 | ±4.2% | yes |
| shown ThreadPoolForeg run mean (ms) | 12 | 0.018 | ±5.1% | yes |
| shown CSystemManager: [event] wakes/s | 12 | 1.0037 | ±0.1% | yes |
| shown CSystemManager: [event] gap mean (ms) | 12 | 996.2673 | ±0.1% | yes |
| shown CSystemManager: [event] run mean (ms) | 12 | 0.0662 | ±1.7% | yes |
| shown IPC:CSteamEngin [event] wakes/s | 12 | 0.64 | ±4.5% | yes |
| shown IPC:CSteamEngin [event] gap mean (ms) | 12 | 1562.5052 | ±4.5% | yes |
| shown IPC:CSteamEngin [event] run mean (ms) | 12 | 0.0291 | ±5.6% | no |
| shown steam [event] wakes/s | 12 | 0.1018 | ±30.0% | no |
| shown steam [event] gap mean (ms) | 12 | 9822.679 | ±30.0% | no |
| shown steam [event] run mean (ms) | 12 | 0.0428 | ±12.3% | no |
| shown steamwebhelper [event] wakes/s | 12 | 0.0908 | ±23.9% | no |
| shown steamwebhelper [event] gap mean (ms) | 12 | 11009.2106 | ±23.9% | no |
| shown steamwebhelper [event] run mean (ms) | 12 | 0.0688 | ±7.6% | no |
| shown ThreadPoolForeg [event] wakes/s | 12 | 0.0889 | ±2.4% | yes |
| shown ThreadPoolForeg [event] gap mean (ms) | 12 | 11250.0371 | ±2.4% | yes |
| shown ThreadPoolForeg [event] run mean (ms) | 12 | 0.0157 | ±7.3% | no |
| shown CJobMgr::m_Work [event] wakes/s | 12 | 0.0839 | ±9.7% | no |
| shown CJobMgr::m_Work [event] gap mean (ms) | 12 | 11920.5691 | ±9.7% | no |
| shown CJobMgr::m_Work [event] run mean (ms) | 12 | 0.0579 | ±5.3% | no |
| shown Compositor [event] wakes/s | 12 | 0.0283 | ±36.0% | no |
| shown Compositor [event] gap mean (ms) | 12 | 35294.2339 | ±36.0% | no |
| shown Compositor [event] run mean (ms) | 12 | 0.0397 | ±18.1% | no |
| shown Chrome_ChildIOT [event] wakes/s | 12 | 0.0229 | ±24.3% | no |
| shown Chrome_ChildIOT [event] gap mean (ms) | 12 | 43636.5074 | ±24.3% | no |
| shown Chrome_ChildIOT [event] run mean (ms) | 12 | 0.0603 | ±11.6% | no |
| shown residual wakes/s | 12 | 13.1088 | ±0.8% | yes |
| shown residual gap mean (ms) | 12 | 76.2844 | ±0.8% | yes |
| shown residual run mean (ms) | 12 | 0.0268 | ±5.5% | no |
| shown residual [event] wakes/s | 12 | 0.0872 | ±39.4% | no |
| shown residual [event] gap mean (ms) | 12 | 11465.0064 | ±39.4% | no |
| shown residual [event] run mean (ms) | 12 | 0.0427 | ±16.3% | no |

Rare event in the shown phase (D33): `CHTTPClientThre`'s runs of 1 ms or more, 62 over 7200 s (0.008611 a second), left out of the component; per repeat {1: 0, 2: 0, 3: 0, 4: 15, 5: 17, 6: 18, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 12}.

Rare event in the minimised phase (D33): `CHTTPClientThre`'s runs of 1 ms or more, 89 over 7200 s (0.012361 a second), left out of the component; per repeat {1: 0, 2: 4, 3: 11, 4: 0, 5: 0, 6: 0, 7: 11, 8: 10, 9: 17, 10: 8, 11: 17, 12: 11}.

| comparison | wakes/s a | wakes/s b | ratio | reading | cpu share a | cpu share b | ratio | reading |
|---|---|---|---|---|---|---|---|---|
| shown against minimised (D5) | 299.31641666666667 | 244.3855 | 1.225 | difference | 0.015060833333333334 | 0.011855 | 1.27 | difference |

