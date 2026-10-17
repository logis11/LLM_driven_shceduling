# Carried phases in time windows — 9.16 re-run

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

## video-editor (`kdenlive`, idle)

16 repeats, 9 whole windows of 20 s. Per component, pooled over the repeats: each window's wake rate over the component's mean over the windows, each window's run mean (ms), its share of the phase's CPU, and the CPU its windows hold above its median window as a share of the phase's CPU.

| component | wakes/s | wake rate per window, over its mean | run mean per window (ms) | share of CPU | above its median window |
|---|---|---|---|---|---|
| `ALL` | 1.264 | 0.98 · 1.09 · 1.08 · 0.98 · 0.95 · 0.98 · 1.02 · 0.96 · 0.97 | 0.057 · 0.058 · 0.053 · 0.057 · 0.058 · 0.060 · 0.060 · 0.059 · 0.058 | 100.0 % | 2.7 % |
| `Qt bearer threa` | 0.1 | 1.00 · 1.00 · 1.00 · 1.00 · 1.00 · 1.00 · 1.00 · 1.00 · 1.00 | 0.419 · 0.422 · 0.427 · 0.412 · 0.419 · 0.433 · 0.434 · 0.427 · 0.419 | 58.1 % | 0.5 % |
| `kdenlive` | 1.161 | 0.98 · 1.09 · 1.08 · 0.98 · 0.95 · 0.98 · 1.01 · 0.96 · 0.97 | 0.025 · 0.030 · 0.023 · 0.025 · 0.026 · 0.027 · 0.027 · 0.026 · 0.026 | 41.5 % | 1.9 % |
| `residual` | 0.002778 | 0.00 · 2.25 · 0.00 · 0.00 · 0.00 · 1.12 · 5.62 · 0.00 · 0.00 | — · 0.117 · — · — · — · 0.162 · 0.086 · — · — | 0.4 % | 0.4 % |
