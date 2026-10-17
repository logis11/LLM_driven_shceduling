# Carried phases in time windows — desktop

## renderer-hidden (`chrome-hidden`, steady)

5 repeats, 6 whole windows of 100 s. Per component, pooled over the repeats: each window's wake rate over the component's mean over the windows, each window's run mean (ms), its share of the phase's CPU, and the CPU its windows hold above its median window as a share of the phase's CPU.

| component | wakes/s | wake rate per window, over its mean | run mean per window (ms) | share of CPU | above its median window |
|---|---|---|---|---|---|
| `ALL` | 2.529 | 1.13 · 0.78 · 1.06 · 1.09 · 0.89 · 1.06 | 0.043 · 0.035 · 0.037 · 0.036 · 0.038 · 0.040 | 100.0 % | 5.2 % |
| `Chrome_ChildIOT` | 0.2113 | 1.25 · 0.62 · 1.14 · 1.14 · 0.72 · 1.14 | 0.031 · 0.035 · 0.032 · 0.032 · 0.034 · 0.032 | 7.1 % | 0.2 % |
| `Compositor` | 0.1 | 1.10 · 0.58 · 0.96 · 1.20 · 1.20 · 0.96 | 0.023 · 0.022 · 0.022 · 0.022 · 0.022 · 0.024 | 2.3 % | 0.1 % |
| `HangWatcher` | 1.2 | 1.00 · 1.00 · 1.00 · 1.00 · 1.00 · 1.00 | 0.028 · 0.027 · 0.025 · 0.026 · 0.025 · 0.027 | 32.5 % | 0.6 % |
| `PerfettoTrace` | 0.1 | 1.16 · 0.58 · 0.90 · 1.20 · 1.20 · 0.96 | 0.020 · 0.020 · 0.021 · 0.021 · 0.021 · 0.023 | 2.2 % | 0.1 % |
| `chrome` | 0.803 | 1.22 · 0.59 · 1.19 · 1.20 · 0.63 · 1.17 | 0.068 · 0.060 · 0.058 · 0.057 · 0.072 · 0.063 | 51.8 % | 2.9 % |
| `residual` | 0.115 | 1.51 · 0.50 · 0.77 · 1.03 · 1.36 · 0.83 | 0.045 · 0.021 · 0.020 · 0.021 · 0.053 · 0.023 | 4.1 % | 2.0 % |

## chat-client (`element`, idle)

18 repeats, 6 whole windows of 100 s. Per component, pooled over the repeats: each window's wake rate over the component's mean over the windows, each window's run mean (ms), its share of the phase's CPU, and the CPU its windows hold above its median window as a share of the phase's CPU.

| component | wakes/s | wake rate per window, over its mean | run mean per window (ms) | share of CPU | above its median window |
|---|---|---|---|---|---|
| `ALL` | 12.32 | 0.88 · 1.14 · 0.88 · 0.96 · 1.15 · 0.99 | 0.085 · 0.086 · 0.088 · 0.084 · 0.083 · 0.082 | 100.0 % | 6.5 % |
| `Chrome_ChildIOT` | 1.484 | 0.84 · 1.18 · 0.85 · 0.98 · 1.18 · 0.97 | 0.070 · 0.072 · 0.069 · 0.070 · 0.069 · 0.073 | 10.0 % | 0.7 % |
| `Chrome_IOThread` | 1.853 | 0.80 · 1.18 · 0.88 · 1.00 · 1.18 · 0.97 | 0.025 · 0.025 · 0.029 · 0.024 · 0.024 · 0.024 | 4.5 % | 0.2 % |
| `ThreadPoolForeg` | 4.229 | 0.85 · 1.19 · 0.82 · 0.90 · 1.22 · 1.02 | 0.036 · 0.043 · 0.044 · 0.037 · 0.039 · 0.041 | 16.2 % | 1.6 % |
| `ThreadPoolServi` | 0.3844 | 0.89 · 1.04 · 0.98 · 1.04 · 1.09 · 0.97 | 0.054 · 0.053 · 0.048 · 0.045 · 0.052 · 0.054 | 1.9 % | 0.1 % |
| `element-desktop` | 3.9 | 0.95 · 1.08 · 0.96 · 0.98 · 1.07 · 0.96 | 0.173 · 0.185 · 0.169 · 0.175 · 0.183 · 0.168 | 65.8 % | 3.9 % |
| `residual` | 0.4695 | 0.94 · 1.01 · 0.79 · 0.96 · 1.21 · 1.09 | 0.025 · 0.027 · 0.051 · 0.025 · 0.039 · 0.045 | 1.6 % | 0.3 % |

## game-client (`steam`, shown)

12 repeats, 6 whole windows of 100 s. Per component, pooled over the repeats: each window's wake rate over the component's mean over the windows, each window's run mean (ms), its share of the phase's CPU, and the CPU its windows hold above its median window as a share of the phase's CPU.

| component | wakes/s | wake rate per window, over its mean | run mean per window (ms) | share of CPU | above its median window |
|---|---|---|---|---|---|
| `ALL` | 299.3 | 1.02 · 1.00 · 1.00 · 0.99 · 1.00 · 1.00 | 0.051 · 0.049 · 0.051 · 0.052 · 0.050 · 0.049 | 100.0 % | 1.1 % |
| `CHTTPClientThre` | 8.038 | 1.02 · 0.99 · 0.99 · 1.00 · 1.00 · 1.00 | 0.018 · 0.016 · 0.016 · 0.016 · 0.016 · 0.016 | 0.9 % | 0.0 % |
| `CJobMgr::m_Work` | 35.63 | 1.05 · 0.98 · 0.98 · 0.99 · 0.99 · 1.00 | 0.017 · 0.017 · 0.018 · 0.018 · 0.018 · 0.017 | 4.2 % | 0.0 % |
| `CNet Encrypt:0` | 8.04 | 1.02 · 0.99 · 0.99 · 0.99 · 1.00 · 1.00 | 0.016 · 0.016 · 0.016 · 0.016 · 0.016 · 0.016 | 0.9 % | 0.0 % |
| `Chrome_ChildIOT` | 13.43 | 1.04 · 1.00 · 0.99 · 0.98 · 0.99 · 1.00 | 0.031 · 0.031 · 0.031 · 0.031 · 0.031 · 0.031 | 2.8 % | 0.0 % |
| `Compositor` | 18.6 | 1.01 · 1.00 · 1.00 · 0.99 · 1.00 · 0.99 | 0.056 · 0.056 · 0.057 · 0.057 · 0.056 · 0.056 | 7.0 % | 0.0 % |
| `IPC:CSteamEngin` | 44.5 | 1.01 · 0.99 · 1.00 · 0.99 · 1.00 · 1.00 | 0.057 · 0.056 · 0.058 · 0.059 · 0.057 · 0.056 | 17.0 % | 0.1 % |
| `ThreadPoolForeg` | 6.173 | 1.08 · 1.01 · 0.98 · 0.95 · 1.00 · 0.98 | 0.024 · 0.017 · 0.017 · 0.016 · 0.017 · 0.016 | 0.7 % | 0.1 % |
| `VizCompositorTh` | 10.54 | 1.00 · 1.00 · 1.00 · 1.00 · 0.99 · 1.00 | 0.083 · 0.081 · 0.082 · 0.082 · 0.082 · 0.081 | 5.7 % | 0.0 % |
| `residual` | 14.15 | 1.07 · 0.99 · 0.98 · 0.97 · 0.99 · 1.00 | 0.031 · 0.029 · 0.030 · 0.029 · 0.029 · 0.029 | 2.8 % | 0.1 % |
| `steam` | 69.47 | 1.00 · 1.00 · 1.00 · 1.00 · 1.00 · 1.00 | 0.055 · 0.054 · 0.056 · 0.058 · 0.056 · 0.054 | 25.6 % | 0.3 % |
| `steamwebhelper` | 70.75 | 1.01 · 1.00 · 1.00 · 1.00 · 1.00 · 1.00 | 0.075 · 0.067 · 0.071 · 0.071 · 0.068 · 0.066 | 32.7 % | 0.7 % |
