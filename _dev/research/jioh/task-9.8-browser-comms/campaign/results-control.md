# Untraced control — desktop

## renderer-hidden (`chrome-hidden`)

6 jobs (3 traced untraced, 3 untraced traced); builds: Google Chrome 153.0.8010.52 (1, 2, 3, 4, 5, 6).
14 intervals read; at 95 % chance alone gives about 0.7 differences; differences found: 2 (steady HangWatcher run mean (ms), steady HangWatcher wakes/s).

| value | traced median | untraced median | medians' ratio | per-job mean | 95 % interval | reading | by order | n | exited (CPU, wakes) | left out (CPU, wakes) |
|---|---|---|---|---|---|---|---|---|---|---|
| steady Chrome_ChildIOT run mean (ms) | 0.0309 | 0.0303 | 0.9825 | 0.945 | 0.8473–1.0426 | not resolved | traced first 0.9481; untraced first 0.9418 | 6 | 0, 0 | — |
| steady Chrome_ChildIOT wakes/s | 0.0074 | 0.0077 | 1.0473 | 1.1577 | 0.7382–1.5772 | not resolved | traced first 1.0626; untraced first 1.2528 | 6 | 0, 0 | — |
| steady Compositor run mean (ms) | 0.0266 | 0.026 | 0.9796 | 1.0443 | 0.8383–1.2503 | not resolved | traced first 0.9818; untraced first 1.1068 | 6 | 0, 0 | — |
| steady Compositor wakes/s | 0.0066 | 0.0066 | 1 | 1.1563 | 0.7222–1.5903 | not resolved | traced first 1.0796; untraced first 1.2329 | 6 | 0, 0 | — |
| steady HangWatcher run mean (ms) | 0.0405 | 0.0389 | 0.9613 | 0.974 | 0.95–0.9981 | difference | traced first 0.9778; untraced first 0.9703 | 6 | 0, 0 | — |
| steady HangWatcher wakes/s | 0.0997 | 0.1 | 1.003 | 1.0027 | 1.0021–1.0032 | difference | traced first 1.0027; untraced first 1.0027 | 6 | 0, 0 | — |
| steady PerfettoTrace run mean (ms) | 0.0257 | 0.0247 | 0.9597 | 0.9211 | 0.8169–1.0254 | not resolved | traced first 0.9697; untraced first 0.8726 | 6 | 0, 0 | — |
| steady PerfettoTrace wakes/s | 0.0066 | 0.0066 | 1 | 1.1563 | 0.7222–1.5903 | not resolved | traced first 1.0796; untraced first 1.2329 | 6 | 0, 0 | — |
| steady ThreadPoolServi run mean (ms) | 0.0255 | 0.0243 | 0.9531 | 0.9463 | 0.8144–1.0783 | not resolved | traced first 1.0447; untraced first 0.8479 | 6 | 0, 0 | — |
| steady ThreadPoolServi wakes/s | 0.0066 | 0.0066 | 1 | 1.1563 | 0.7222–1.5903 | not resolved | traced first 1.0796; untraced first 1.2329 | 6 | 0, 0 | — |
| steady chrome run mean (ms) | 0.0881 | 0.0892 | 1.0131 | 1.1511 | 0.6592–1.643 | not resolved | traced first 0.7269; untraced first 1.5753 | 6 | 0, 0 | — |
| steady chrome wakes/s | 0.0373 | 0.0368 | 0.9879 | 1.0296 | 0.8448–1.2144 | not resolved | traced first 0.875; untraced first 1.1842 | 6 | 0, 0 | — |
| steady residual run mean (ms) | 0.1864 | 0.1456 | 0.781 | 0.7164 | 0.369–1.0637 | not resolved | traced first 0.7935; untraced first 0.5621 | 3 | 0, 0 | — |
| steady residual wakes/s | 0.0024 | 0.0034 | 1.4255 | 2.9695 | -5.9487–11.8878 | not resolved | traced first 0.9017; untraced first 7.1053 | 3 | 0, 0 | — |

The workload check under the carried pool's selection, read by hand: the control's six repeats put `ThreadPoolServi`, the slowest carried component, past the coverage cut (9.5 D16) into the residual; under the carried selection `ThreadPoolServi`'s wake rate is 0.0056 against 0.0065 /s (z −0.37) and its run mean 0.0197 against 0.0198 ms (z −0.07), the residual (`MemoryInfra`) 0.0034 against 0.0033 /s (z +0.10) and 0.193 against 0.188 ms (z +0.19) — no disagreement.

The traced runs against the carried pool (decision 17): largest |z| 5.12 over 16 values; only in the carried pool: steady ThreadPoolServi gap mean (ms), steady ThreadPoolServi run mean (ms), steady ThreadPoolServi wakes/s.

## renderer-visible (`chrome-visible`)

6 jobs (3 traced untraced, 3 untraced traced); builds: Google Chrome 153.0.8010.52 (1, 2, 3, 4, 5, 6).
10 intervals read; at 95 % chance alone gives about 0.5 differences; differences found: 0.

| value | traced median | untraced median | medians' ratio | per-job mean | 95 % interval | reading | by order | n | exited (CPU, wakes) | left out (CPU, wakes) |
|---|---|---|---|---|---|---|---|---|---|---|
| steady-notimer Chrome_ChildIOT run mean (ms) | 0.0388 | 0.0376 | 0.9699 | 1.0341 | 0.7421–1.3261 | not resolved | traced first 0.8257; untraced first 1.2426 | 6 | 0, 0 | — |
| steady-notimer Chrome_ChildIOT wakes/s | 0.0077 | 0.0076 | 0.9806 | 0.9039 | 0.7941–1.0137 | not resolved | traced first 0.8989; untraced first 0.9088 | 6 | 0, 0 | — |
| steady-notimer HangWatcher run mean (ms) | 0.0474 | 0.0455 | 0.9614 | 0.9598 | 0.9188–1.0009 | not resolved | traced first 0.9611; untraced first 0.9585 | 6 | 0, 0 | — |
| steady-notimer HangWatcher wakes/s | 0.1 | 0.1 | 1 | 1.0003 | 0.9998–1.0009 | not resolved | traced first 1.0; untraced first 1.0007 | 6 | 0, 0 | — |
| steady-notimer PerfettoTrace run mean (ms) | 0.031 | 0.0302 | 0.9753 | 0.9377 | 0.8236–1.0519 | not resolved | traced first 0.8738; untraced first 1.0017 | 6 | 0, 0 | — |
| steady-notimer PerfettoTrace wakes/s | 0.0068 | 0.0068 | 1 | 1.0057 | 0.9836–1.0278 | not resolved | traced first 1.0124; untraced first 0.999 | 6 | 0, 0 | — |
| steady-notimer chrome run mean (ms) | 0.1525 | 0.1409 | 0.9242 | 1.0277 | 0.6643–1.3912 | not resolved | traced first 0.7546; untraced first 1.3009 | 6 | 0, 0 | — |
| steady-notimer chrome wakes/s | 0.0217 | 0.0205 | 0.9425 | 1.0029 | 0.7146–1.2913 | not resolved | traced first 0.7803; untraced first 1.2255 | 6 | 0, 0 | — |
| steady-notimer residual run mean (ms) | 0.1132 | 0.1296 | 1.1454 | 1.793 | -0.1116–3.6976 | not resolved | traced first 0.5808; untraced first 3.0053 | 6 | 0, 0 | — |
| steady-notimer residual wakes/s | 0.0067 | 0.0054 | 0.7926 | 0.998 | 0.3204–1.6755 | not resolved | traced first 0.5549; untraced first 1.441 | 6 | 0, 0 | — |

The traced runs against the carried pool (decision 17): largest |z| 1.98 over 15 values.

## chat-client (`element`)

6 jobs (3 traced untraced, 3 untraced traced); builds: Element 1.12.29 (1, 2, 3, 4, 5, 6).
12 intervals read; at 95 % chance alone gives about 0.6 differences; differences found: 4 (idle Chrome_ChildIOT run mean (ms), idle Chrome_IOThread run mean (ms), idle ThreadPoolForeg run mean (ms), idle ThreadPoolServi run mean (ms)).

| value | traced median | untraced median | medians' ratio | per-job mean | 95 % interval | reading | by order | n | exited (CPU, wakes) | left out (CPU, wakes) |
|---|---|---|---|---|---|---|---|---|---|---|
| idle Chrome_ChildIOT run mean (ms) | 0.0671 | 0.0626 | 0.9328 | 0.9308 | 0.9099–0.9516 | difference | traced first 0.9244; untraced first 0.9371 | 6 | 0, 0 | — |
| idle Chrome_ChildIOT wakes/s | 1.5879 | 1.5707 | 0.9892 | 1.0012 | 0.9588–1.0435 | not resolved | traced first 1.0336; untraced first 0.9687 | 6 | 0, 0 | — |
| idle Chrome_IOThread run mean (ms) | 0.0255 | 0.0214 | 0.8402 | 0.8432 | 0.8089–0.8774 | difference | traced first 0.8199; untraced first 0.8665 | 6 | 0, 0 | — |
| idle Chrome_IOThread wakes/s | 1.9236 | 1.9249 | 1.0006 | 0.9974 | 0.9542–1.0406 | not resolved | traced first 1.0325; untraced first 0.9623 | 6 | 0, 0 | — |
| idle ThreadPoolForeg run mean (ms) | 0.0388 | 0.0354 | 0.9121 | 0.9093 | 0.8606–0.9579 | difference | traced first 0.924; untraced first 0.8946 | 6 | 0, 0 | — |
| idle ThreadPoolForeg wakes/s | 4.6007 | 4.638 | 1.0081 | 1.0212 | 0.9503–1.0921 | not resolved | traced first 1.0282; untraced first 1.0141 | 6 | 0, 0 | — |
| idle ThreadPoolServi run mean (ms) | 0.0632 | 0.0541 | 0.8561 | 0.8798 | 0.8072–0.9523 | difference | traced first 0.9024; untraced first 0.8571 | 6 | 0, 0 | — |
| idle ThreadPoolServi wakes/s | 0.3849 | 0.3841 | 0.9982 | 1.003 | 0.9738–1.0322 | not resolved | traced first 0.9811; untraced first 1.0249 | 6 | 0, 0 | — |
| idle element-desktop run mean (ms) | 0.1758 | 0.1745 | 0.9929 | 0.9837 | 0.9451–1.0223 | not resolved | traced first 0.9574; untraced first 1.0099 | 6 | 0.004, 0.016 | — |
| idle element-desktop wakes/s | 3.8872 | 3.8913 | 1.0011 | 0.9982 | 0.9862–1.0102 | not resolved | traced first 0.9885; untraced first 1.0079 | 6 | 0.004, 0.016 | — |
| idle residual run mean (ms) | 0.032 | 0.0308 | 0.9613 | 0.9173 | 0.7816–1.0529 | not resolved | traced first 0.805; untraced first 1.0295 | 6 | 0, 0 | — |
| idle residual wakes/s | 0.4753 | 0.4633 | 0.9748 | 0.9813 | 0.9301–1.0324 | not resolved | traced first 0.96; untraced first 1.0025 | 6 | 0, 0 | — |

- left out of the control's pool: 1@36303380155 — D66: windows 1 and 2 measured twice — the restarted gate loop relaunched them (#64, then #67 for window 1) after the previous loop's relaunch (#62) had already started; the original launch's copies (#62, 36300233345) are kept
- left out of the control's pool: 2@36300828888 — D66: windows 1 and 2 measured twice — the restarted gate loop relaunched them (#64, then #67 for window 1) after the previous loop's relaunch (#62) had already started; the original launch's copies (#62, 36300233345) are kept

The second idle run wakes `Chrome_IOThread` and `Chrome_ChildIOT` about 3–4 % more than the first, traced or not; the control ran Element 1.12.29, the carried pool 1.12.28.

The traced runs against the carried pool (decision 17): largest |z| 3.35 over 18 values.

## game-client (`steam`)

6 jobs (3 traced untraced, 3 untraced traced); builds: Steam client build 1788652215 (1, 2, 3, 4, 5, 6).
22 intervals read; at 95 % chance alone gives about 1.1 differences; differences found: 10 (shown CJobMgr::m_Work run mean (ms), shown Chrome_ChildIOT run mean (ms), shown Chrome_ChildIOT wakes/s, shown Compositor run mean (ms), shown Compositor wakes/s, shown ThreadPoolForeg run mean (ms), shown ThreadPoolForeg wakes/s, shown VizCompositorTh run mean (ms), shown VizCompositorTh wakes/s, shown steamwebhelper wakes/s).

| value | traced median | untraced median | medians' ratio | per-job mean | 95 % interval | reading | by order | n | exited (CPU, wakes) | left out (CPU, wakes) |
|---|---|---|---|---|---|---|---|---|---|---|
| shown CHTTPClientThre run mean (ms) | 0.036 | 0.0508 | 1.4082 | 1.5459 | 0.3968–2.6951 | not resolved | traced first 2.5423; untraced first 0.5495 | 6 | 0, 0 | — |
| shown CHTTPClientThre wakes/s | 8.0345 | 8.0559 | 1.0027 | 1.0023 | 0.9911–1.0134 | not resolved | traced first 1.0117; untraced first 0.9929 | 6 | 0, 0 | — |
| shown CJobMgr::m_Work run mean (ms) | 0.0199 | 0.0169 | 0.8531 | 0.8568 | 0.7783–0.9353 | difference | traced first 0.8793; untraced first 0.8343 | 6 | 0, 0 | — |
| shown CJobMgr::m_Work wakes/s | 35.8255 | 35.8101 | 0.9996 | 0.9987 | 0.9858–1.0117 | not resolved | traced first 1.0087; untraced first 0.9888 | 6 | 0, 0 | — |
| shown CNet Encrypt:0 run mean (ms) | 0.0288 | 0.0283 | 0.982 | 0.9727 | 0.9402–1.0051 | not resolved | traced first 0.9593; untraced first 0.986 | 6 | 0, 0 | — |
| shown CNet Encrypt:0 wakes/s | 8.0193 | 8.0434 | 1.003 | 1.0018 | 0.9962–1.0074 | not resolved | traced first 1.0061; untraced first 0.9976 | 6 | 0, 0 | — |
| shown Chrome_ChildIOT run mean (ms) | 0.0332 | 0.0289 | 0.8698 | 0.8714 | 0.8439–0.8988 | difference | traced first 0.8723; untraced first 0.8704 | 6 | 0, 0 | — |
| shown Chrome_ChildIOT wakes/s | 13.2943 | 13.2588 | 0.9973 | 0.9961 | 0.9925–0.9997 | difference | traced first 0.9942; untraced first 0.998 | 6 | 0, 0 | — |
| shown Compositor run mean (ms) | 0.0601 | 0.0578 | 0.9615 | 0.9515 | 0.9147–0.9883 | difference | traced first 0.9514; untraced first 0.9516 | 6 | 0, 0 | — |
| shown Compositor wakes/s | 18.5939 | 18.1634 | 0.9768 | 0.9792 | 0.9732–0.9852 | difference | traced first 0.9812; untraced first 0.9772 | 6 | 0, 0 | — |
| shown IPC:CSteamEngin run mean (ms) | 0.0656 | 0.0629 | 0.9583 | 0.9591 | 0.8512–1.067 | not resolved | traced first 0.9769; untraced first 0.9413 | 6 | 0, 0 | — |
| shown IPC:CSteamEngin wakes/s | 44.5012 | 44.3775 | 0.9972 | 0.9962 | 0.982–1.0105 | not resolved | traced first 1.0048; untraced first 0.9876 | 6 | 0, 0 | — |
| shown ThreadPoolForeg run mean (ms) | 0.0183 | 0.0148 | 0.81 | 0.8158 | 0.7458–0.8857 | difference | traced first 0.7697; untraced first 0.8618 | 6 | 0, 0 | — |
| shown ThreadPoolForeg wakes/s | 6.235 | 6.6594 | 1.0681 | 1.0761 | 1.0131–1.1391 | difference | traced first 1.04; untraced first 1.1122 | 6 | 0, 0 | — |
| shown VizCompositorTh run mean (ms) | 0.088 | 0.0858 | 0.9755 | 0.972 | 0.9466–0.9975 | difference | traced first 0.9683; untraced first 0.9758 | 6 | 0, 0 | — |
| shown VizCompositorTh wakes/s | 10.3654 | 10.2832 | 0.9921 | 0.9876 | 0.9768–0.9983 | difference | traced first 0.9851; untraced first 0.99 | 6 | 0, 0 | — |
| shown residual run mean (ms) | 0.0414 | 0.0397 | 0.9584 | 0.9588 | 0.915–1.0026 | not resolved | traced first 0.947; untraced first 0.9706 | 6 | 0, 0 | — |
| shown residual wakes/s | 14.048 | 14.1587 | 1.0079 | 1.0059 | 0.9887–1.0232 | not resolved | traced first 1.0206; untraced first 0.9912 | 6 | 0, 0 | — |
| shown steam run mean (ms) | 0.0669 | 0.0668 | 0.9986 | 1.0077 | 0.8791–1.1363 | not resolved | traced first 1.0281; untraced first 0.9873 | 6 | 0, 0 | — |
| shown steam wakes/s | 69.5101 | 69.6652 | 1.0022 | 1.0009 | 0.9958–1.0061 | not resolved | traced first 1.005; untraced first 0.9969 | 6 | 0, 0 | — |
| shown steamwebhelper run mean (ms) | 0.0808 | 0.0801 | 0.9911 | 1.0151 | 0.8948–1.1353 | not resolved | traced first 0.9892; untraced first 1.0409 | 6 | 0, 0 | — |
| shown steamwebhelper wakes/s | 70.5224 | 70.1952 | 0.9954 | 0.9961 | 0.9928–0.9994 | difference | traced first 0.9955; untraced first 0.9967 | 6 | 0, 0 | — |

The traced runs against the carried pool (decision 17): largest |z| 1.27 over 33 values.
