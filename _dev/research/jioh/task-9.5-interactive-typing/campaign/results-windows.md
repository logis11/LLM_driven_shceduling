# Carried phases in time windows — campaign

## office-writer (`soffice`, idle)

14 repeats, 6 whole windows of 20 s. Per component, pooled over the repeats: each window's wake rate over the component's mean over the windows, each window's run mean (ms), its share of the phase's CPU, and the CPU its windows hold above its median window as a share of the phase's CPU.

| component | wakes/s | wake rate per window, over its mean | run mean per window (ms) | share of CPU | above its median window |
|---|---|---|---|---|---|
| `ALL` | 3.457 | 0.99 · 1.01 · 0.98 · 1.00 · 1.00 · 1.01 | 0.166 · 0.167 · 0.168 · 0.164 · 0.166 · 0.164 | 100.0 % | 0.5 % |
| `soffice.bin` | 3.457 | 0.99 · 1.01 · 0.98 · 1.00 · 1.00 · 1.01 | 0.166 · 0.167 · 0.168 · 0.164 · 0.166 · 0.164 | 100.0 % | 0.5 % |

## code-editor (`code`, idle)

44 repeats, 7 whole windows of 100 s. Per component, pooled over the repeats: each window's wake rate over the component's mean over the windows, each window's run mean (ms), its share of the phase's CPU, and the CPU its windows hold above its median window as a share of the phase's CPU.

| component | wakes/s | wake rate per window, over its mean | run mean per window (ms) | share of CPU | above its median window |
|---|---|---|---|---|---|
| `ALL` | 112.4 | 1.01 · 1.01 · 1.00 · 1.00 · 1.00 · 0.99 · 0.99 | 0.124 · 0.136 · 0.123 · 0.125 · 0.137 · 0.125 · 0.126 | 100.0 % | 2.8 % |
| `code` | 3.369 | 1.00 · 1.03 · 1.01 · 0.96 · 1.01 · 1.02 · 0.96 | 0.063 · 0.064 · 0.064 · 0.064 · 0.064 · 0.063 · 0.064 | 1.5 % | 0.0 % |
| `gpu/Chrome_ChildIOT` | 20.17 | 1.00 · 1.00 · 1.00 · 1.00 · 0.99 · 1.00 · 1.01 | 0.024 · 0.024 · 0.024 · 0.024 · 0.024 · 0.024 · 0.024 | 3.4 % | 0.0 % |
| `gpu/VizCompositorTh` | 23.12 | 0.99 · 1.01 · 1.00 · 1.00 · 0.99 · 1.01 · 1.01 | 0.242 · 0.240 · 0.241 · 0.242 · 0.244 · 0.241 · 0.242 | 38.9 % | 0.1 % |
| `renderer/Compositor` | 22.81 | 1.00 · 1.01 · 1.00 · 0.99 · 0.99 · 1.00 · 1.00 | 0.081 · 0.081 · 0.081 · 0.082 · 0.082 · 0.082 · 0.083 | 12.9 % | 0.1 % |
| `renderer/ThreadPoolForeg` | 3.432 | 1.05 · 1.01 · 1.08 · 0.99 · 1.03 · 0.93 · 0.92 | 0.075 · 0.353 · 0.037 · 0.043 · 0.377 · 0.037 · 0.035 | 3.3 % | 2.4 % |
| `renderer/code` | 19.54 | 1.00 · 0.99 · 0.99 · 1.00 · 1.01 · 1.00 · 1.01 | 0.256 · 0.273 · 0.252 · 0.253 · 0.268 · 0.252 · 0.251 | 35.1 % | 0.7 % |
| `residual` | 3.094 | 1.18 · 1.00 · 0.93 · 1.01 · 0.99 · 0.92 · 0.98 | 0.055 · 0.046 · 0.038 · 0.054 · 0.037 · 0.038 · 0.053 | 1.0 % | 0.1 % |
| `utility/code` | 11.46 | 1.08 · 1.04 · 1.01 · 1.00 · 0.98 · 0.95 · 0.94 | 0.046 · 0.043 · 0.043 · 0.047 · 0.044 · 0.044 · 0.048 | 3.6 % | 0.1 % |
| `utility/libuv-worker` | 5.382 | 1.07 · 1.05 · 0.97 · 0.98 · 1.10 · 0.89 · 0.94 | 0.010 · 0.010 · 0.010 · 0.010 · 0.010 · 0.011 · 0.010 | 0.4 % | 0.0 % |

## web-browser (`chrome`, idle)

38 repeats, 6 whole windows of 100 s. Per component, pooled over the repeats: each window's wake rate over the component's mean over the windows, each window's run mean (ms), its share of the phase's CPU, and the CPU its windows hold above its median window as a share of the phase's CPU.

| component | wakes/s | wake rate per window, over its mean | run mean per window (ms) | share of CPU | above its median window |
|---|---|---|---|---|---|
| `ALL` | 43.21 | 1.00 · 1.01 · 1.00 · 0.99 · 1.00 · 1.00 | 0.065 · 0.067 · 0.066 · 0.065 · 0.068 · 0.065 | 100.0 % | 1.3 % |
| `chrome` | 0.8004 | 0.94 · 1.17 · 1.01 · 0.77 · 1.11 · 1.00 | 0.164 · 0.151 · 0.154 · 0.159 · 0.156 · 0.154 | 4.4 % | 0.2 % |
| `gpu/Chrome_ChildIOT` | 7.593 | 1.00 · 1.00 · 1.00 · 1.00 · 1.00 · 1.00 | 0.029 · 0.029 · 0.030 · 0.030 · 0.030 · 0.030 | 7.9 % | 0.0 % |
| `gpu/VizCompositorTh` | 12.1 | 1.00 · 1.00 · 1.00 · 1.00 · 1.00 · 1.01 | 0.072 · 0.072 · 0.073 · 0.073 · 0.073 · 0.073 | 30.9 % | 0.0 % |
| `renderer/Compositor` | 12.73 | 1.00 · 1.00 · 1.00 · 1.00 · 1.00 · 1.01 | 0.067 · 0.067 · 0.067 · 0.068 · 0.067 · 0.067 | 30.0 % | 0.0 % |
| `renderer/chrome` | 7.386 | 1.01 · 1.00 · 1.01 · 1.00 · 1.00 · 0.98 | 0.075 · 0.075 · 0.074 · 0.075 · 0.076 · 0.071 | 19.3 % | 0.1 % |
| `residual` | 1.804 | 0.98 · 1.09 · 0.96 · 0.92 · 1.11 · 0.95 | 0.075 · 0.111 · 0.074 · 0.065 · 0.114 · 0.070 | 5.4 % | 1.1 % |
| `utility/chrome` | 0.803 | 1.00 · 1.01 · 0.99 · 1.00 · 1.01 · 0.99 | 0.080 · 0.076 · 0.079 · 0.077 · 0.079 · 0.079 | 2.2 % | 0.0 % |

## mail-client (`thunderbird-send`, idle)

43 repeats, 6 whole windows of 100 s. Per component, pooled over the repeats: each window's wake rate over the component's mean over the windows, each window's run mean (ms), its share of the phase's CPU, and the CPU its windows hold above its median window as a share of the phase's CPU.

| component | wakes/s | wake rate per window, over its mean | run mean per window (ms) | share of CPU | above its median window |
|---|---|---|---|---|---|
| `ALL` | 1.992 | 0.84 · 1.08 · 1.06 · 1.04 · 0.97 · 1.00 | 0.329 · 0.345 · 0.526 · 0.431 · 0.254 · 0.550 | 100.0 % | 13.3 % |
| `IPC I/O Child` | 0.04 | 1.00 · 1.14 · 1.36 · 1.00 · 1.00 · 0.50 | 0.025 · 0.026 · 0.038 · 0.024 · 0.025 · 0.024 | 0.1 % | 0.0 % |
| `IPC I/O Parent` | 0.04236 | 1.13 · 1.26 · 0.57 · 1.27 · 1.18 · 0.60 | 0.035 · 0.033 · 0.034 · 0.033 · 0.036 · 0.037 | 0.2 % | 0.0 % |
| `IPDL Background` | 0.2405 | 1.22 · 1.00 · 0.74 · 1.20 · 1.08 · 0.75 | 0.021 · 0.023 · 0.020 · 0.021 · 0.021 · 0.019 | 0.6 % | 0.0 % |
| `Indexed~ IO` | 0.07279 | 0.00 · 0.54 · 1.27 · 1.29 · 1.69 · 1.21 | — · 0.248 · 0.150 · 0.218 · 0.162 · 0.155 | 1.6 % | 0.3 % |
| `JS Watchdog` | 0.1698 | 1.09 · 1.07 · 0.92 · 1.03 · 0.95 · 0.93 | 0.022 · 0.022 · 0.023 · 0.021 · 0.021 · 0.021 | 0.4 % | 0.0 % |
| `StreamTrans` | 0.1303 | 0.75 · 0.62 · 1.48 · 0.86 · 0.80 · 1.48 | 3.838 · 6.233 · 4.740 · 6.064 · 2.907 · 4.759 | 75.7 % | 15.1 % |
| `Timer` | 0.2831 | 0.80 · 1.23 · 1.08 · 0.97 · 1.09 · 0.84 | 0.038 · 0.034 · 0.033 · 0.041 · 0.034 · 0.039 | 1.3 % | 0.1 % |
| `WebExtensions` | 0.2072 | 0.49 · 1.18 · 1.16 · 1.17 · 1.14 · 0.86 | 0.257 · 0.108 · 0.078 · 0.096 · 0.093 · 0.090 | 2.7 % | 0.2 % |
| `glean.dispatche` | 0.05678 | 0.70 · 1.24 · 1.19 · 0.86 · 0.99 · 1.02 | 0.037 · 0.033 · 0.040 · 0.039 · 0.033 · 0.041 | 0.3 % | 0.0 % |
| `gmain` | 0.25 | 1.00 · 1.00 · 1.00 · 1.00 · 1.00 · 1.00 | 0.047 · 0.047 · 0.047 · 0.047 · 0.047 · 0.047 | 1.4 % | 0.0 % |
| `residual` | 0.09434 | 1.24 · 1.56 · 1.31 · 0.62 · 0.45 · 0.83 | 0.175 · 0.094 · 0.059 · 0.040 · 0.040 · 0.045 | 1.0 % | 0.5 % |
| `thunderbird-bin` | 0.4054 | 0.70 · 1.12 · 1.08 · 1.05 · 0.76 · 1.29 | 0.337 · 0.332 · 0.283 · 0.295 · 0.363 · 0.210 | 14.7 % | 0.9 % |

## video-editor (`kdenlive`, idle)

20 repeats, 6 whole windows of 20 s. Per component, pooled over the repeats: each window's wake rate over the component's mean over the windows, each window's run mean (ms), its share of the phase's CPU, and the CPU its windows hold above its median window as a share of the phase's CPU.

| component | wakes/s | wake rate per window, over its mean | run mean per window (ms) | share of CPU | above its median window |
|---|---|---|---|---|---|
| `ALL` | 1.363 | 1.08 · 0.96 · 1.08 · 0.97 · 0.95 · 0.96 | 0.050 · 0.062 · 0.054 · 0.058 · 0.058 · 0.057 | 100.0 % | 2.1 % |
| `Qt bearer threa` | 0.1 | 1.00 · 1.00 · 1.00 · 1.00 · 1.00 · 1.00 | 0.414 · 0.406 · 0.405 · 0.411 · 0.401 · 0.410 | 53.0 % | 0.3 % |
| `kdenlive` | 1.26 | 1.08 · 0.96 · 1.09 · 0.97 · 0.95 · 0.95 | 0.023 · 0.033 · 0.029 · 0.029 · 0.029 · 0.028 | 46.6 % | 2.1 % |
| `residual` | 0.002917 | 6.00 · 0.00 · 0.00 · 0.00 · 0.00 · 0.00 | 0.091 · — · — · — · — · — | 0.3 % | 0.3 % |

## video-player (`mpv-video`, play)

24 repeats, 3 whole windows of 100 s. Per component, pooled over the repeats: each window's wake rate over the component's mean over the windows, each window's run mean (ms), its share of the phase's CPU, and the CPU its windows hold above its median window as a share of the phase's CPU.

| component | wakes/s | wake rate per window, over its mean | run mean per window (ms) | share of CPU | above its median window |
|---|---|---|---|---|---|
| `ALL` | 832.2 | 1.00 · 1.00 · 1.00 | 0.147 · 0.147 · 0.146 | 100.0 % | 0.1 % |
| `demux` | 146.7 | 1.00 · 1.01 · 1.00 | 0.009 · 0.009 · 0.009 | 1.1 % | 0.0 % |
| `lua/osc` | 106.6 | 1.00 · 1.00 · 1.00 | 0.031 · 0.031 · 0.032 | 2.7 % | 0.0 % |
| `mpv` | 235 | 1.00 · 1.00 · 1.00 | 0.140 · 0.139 · 0.139 | 26.8 % | 0.0 % |
| `residual` | 33.66 | 1.00 · 0.99 · 1.01 | 0.022 · 0.022 · 0.022 | 0.6 % | 0.0 % |
| `vo` | 310.2 | 1.01 · 0.99 · 1.01 | 0.269 · 0.274 · 0.267 | 68.7 % | 0.1 % |

## audio-player (`mpv-audio`, play)

31 repeats, 3 whole windows of 100 s. Per component, pooled over the repeats: each window's wake rate over the component's mean over the windows, each window's run mean (ms), its share of the phase's CPU, and the CPU its windows hold above its median window as a share of the phase's CPU.

| component | wakes/s | wake rate per window, over its mean | run mean per window (ms) | share of CPU | above its median window |
|---|---|---|---|---|---|
| `ALL` | 208.1 | 1.00 · 1.00 · 1.00 | 0.035 · 0.034 · 0.034 | 100.0 % | 0.5 % |
| `ao` | 44.37 | 1.00 · 1.00 · 1.00 | 0.023 · 0.023 · 0.023 | 14.3 % | 0.0 % |
| `demux` | 54 | 1.00 · 1.00 · 0.99 | 0.013 · 0.013 · 0.013 | 9.6 % | 0.0 % |
| `lua/osc` | 37.34 | 1.00 · 1.00 · 1.00 | 0.056 · 0.055 · 0.054 | 29.0 % | 0.2 % |
| `mpv` | 70.38 | 1.00 · 1.00 · 1.00 | 0.048 · 0.047 · 0.046 | 46.3 % | 0.3 % |
| `residual` | 2.026 | 1.05 · 0.90 · 1.05 | 0.028 · 0.030 · 0.028 | 0.8 % | 0.0 % |

## video-call (`webrtc`, play)

45 repeats, 4 whole windows of 100 s. Per component, pooled over the repeats: each window's wake rate over the component's mean over the windows, each window's run mean (ms), its share of the phase's CPU, and the CPU its windows hold above its median window as a share of the phase's CPU.

| component | wakes/s | wake rate per window, over its mean | run mean per window (ms) | share of CPU | above its median window |
|---|---|---|---|---|---|
| `ALL` | 2045 | 1.02 · 0.99 · 1.01 · 0.98 | 0.072 · 0.178 · 0.071 · 0.181 | 100.0 % | 20.8 % |
| `gpu/Chrome_ChildIOT` | 60.74 | 0.96 · 1.01 · 1.01 · 1.02 | 0.018 · 0.019 · 0.018 · 0.019 | 0.4 % | 0.0 % |
| `gpu/VizCompositorTh` | 97.73 | 0.94 · 1.05 · 0.95 · 1.06 | 0.119 · 0.105 · 0.122 · 0.106 | 4.3 % | 0.0 % |
| `renderer/AudioInputDevic` | 100 | 1.00 · 1.00 · 1.00 · 1.00 | 0.025 · 0.025 · 0.026 · 0.026 | 1.0 % | 0.0 % |
| `renderer/AudioOutputDevi` | 115 | 1.01 · 0.98 · 1.01 · 0.99 | 0.062 · 0.063 · 0.063 · 0.063 | 2.8 % | 0.0 % |
| `renderer/Chrome_ChildIOT` | 272 | 1.03 · 0.97 · 1.03 · 0.97 | 0.021 · 0.022 · 0.022 · 0.022 | 2.3 % | 0.0 % |
| `renderer/ThreadPoolForeg` | 191.8 | 1.00 · 0.98 · 1.02 · 1.00 | 0.243 · 1.403 · 0.239 · 1.364 | 60.6 % | 21.2 % |
| `renderer/VideoFrameCompo` | 88.73 | 1.02 · 0.98 · 1.02 · 0.98 | 0.059 · 0.062 · 0.062 · 0.064 | 2.2 % | 0.0 % |
| `renderer/WebRTC_W_and_N` | 497.5 | 1.05 · 0.99 · 1.01 · 0.95 | 0.031 · 0.031 · 0.032 · 0.033 | 6.2 % | 0.1 % |
| `renderer/chrome` | 56 | 1.07 · 0.97 · 1.05 · 0.91 | 0.038 · 0.041 · 0.038 · 0.043 | 0.9 % | 0.0 % |
| `residual` | 74.56 | 1.03 · 0.98 · 1.01 · 0.98 | 0.118 · 0.079 · 0.079 · 0.082 | 2.6 % | 0.3 % |
| `utility/AudioProcessing` | 124.1 | 1.02 · 0.97 · 1.03 · 0.98 | 0.124 · 0.129 · 0.125 · 0.130 | 6.2 % | 0.0 % |
| `utility/AudioWorkerThre` | 100 | 1.00 · 1.00 · 1.00 · 1.00 | 0.071 · 0.071 · 0.072 · 0.072 | 2.8 % | 0.0 % |
| `utility/Chrome_ChildIOT` | 107.6 | 1.02 · 0.99 · 1.01 · 0.99 | 0.082 · 0.081 · 0.084 · 0.084 | 3.5 % | 0.0 % |
| `utility/FakeAudioInput` | 100 | 1.00 · 1.00 · 1.00 · 1.00 | 0.024 · 0.024 · 0.025 · 0.025 | 1.0 % | 0.0 % |
| `utility/chrome` | 59.42 | 1.01 · 0.99 · 1.01 · 0.99 | 0.134 · 0.136 · 0.135 · 0.138 | 3.2 % | 0.0 % |
