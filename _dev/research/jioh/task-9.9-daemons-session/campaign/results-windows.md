# Carried phases in time windows — session

## compositor-shell (`session`, steady)

24 repeats, 18 whole windows of 100 s. Per component, pooled over the repeats: each window's wake rate over the component's mean over the windows, each window's run mean (ms), its share of the phase's CPU, and the CPU its windows hold above its median window as a share of the phase's CPU.

| component | wakes/s | wake rate per window, over its mean | run mean per window (ms) | share of CPU | above its median window |
|---|---|---|---|---|---|
| `ALL` | 0.5873 | 1.25 · 0.95 · 1.01 · 1.02 · 0.95 · 1.01 · 1.00 · 0.94 · 1.00 · 1.02 · 0.95 · 1.00 · 1.01 · 0.93 · 1.00 · 1.01 · 0.95 · 1.00 | 0.481 · 0.347 · 0.353 · 0.414 · 0.412 · 0.351 · 0.357 · 0.350 · 0.353 · 0.356 · 0.341 · 0.350 · 0.351 · 0.345 · 0.345 · 0.350 · 0.342 · 0.349 | 100.0 % | 5.7 % |
| `gnome-shell/JS Helper` | 0.3025 | 1.46 · 0.92 · 1.02 · 1.04 · 0.91 · 1.01 · 1.00 · 0.88 · 1.01 · 1.04 · 0.91 · 1.00 · 1.02 · 0.88 · 1.01 · 1.02 · 0.90 · 0.99 | 0.014 · 0.014 · 0.014 · 0.014 · 0.014 · 0.014 · 0.014 · 0.013 · 0.014 · 0.014 · 0.014 · 0.014 · 0.014 · 0.013 · 0.014 · 0.014 · 0.013 · 0.014 | 1.9 % | 0.1 % |
| `gnome-shell/gmain` | 0.2498 | 1.00 · 1.00 · 1.00 · 0.99 · 1.00 · 1.00 · 1.00 · 1.00 · 1.00 · 1.00 · 1.00 · 1.00 · 1.00 · 1.00 · 1.00 · 1.00 · 1.00 · 1.00 | 0.049 · 0.048 · 0.049 · 0.051 · 0.051 · 0.051 · 0.050 · 0.051 · 0.051 · 0.049 · 0.049 · 0.050 · 0.050 · 0.050 · 0.049 · 0.049 · 0.050 · 0.049 | 5.8 % | 0.0 % |
| `gnome-shell/gnome-s:disk$0` | 0.0001852 | 0.00 · 0.00 · 0.00 · 9.00 · 9.00 · 0.00 · 0.00 · 0.00 · 0.00 · 0.00 · 0.00 · 0.00 · 0.00 · 0.00 · 0.00 · 0.00 · 0.00 · 0.00 | — · — · — · 0.242 · 0.211 · — · — · — · — · — · — · — · — · — · — · — · — · — | 0.0 % | 0.0 % |
| `gnome-shell/gnome-shell` | 0.03475 | 1.20 · 0.96 · 0.97 · 0.98 · 0.96 · 0.98 · 1.02 · 1.00 · 0.97 · 1.01 · 0.94 · 1.02 · 1.04 · 0.95 · 0.98 · 1.03 · 0.98 · 1.01 | 8.030 · 5.354 · 5.677 · 6.746 · 6.408 · 5.575 · 5.465 · 5.112 · 5.647 · 5.615 · 5.347 · 5.332 · 5.288 · 5.259 · 5.481 · 5.333 · 5.100 · 5.369 | 92.3 % | 5.7 % |

## audio-server (`session`, steady)

24 repeats, 18 whole windows of 100 s. Per component, pooled over the repeats: each window's wake rate over the component's mean over the windows, each window's run mean (ms), its share of the phase's CPU, and the CPU its windows hold above its median window as a share of the phase's CPU.

| component | wakes/s | wake rate per window, over its mean | run mean per window (ms) | share of CPU | above its median window |
|---|---|---|---|---|---|
| `ALL` | 0.009306 | 3.13 · 0.81 · 0.99 · 0.54 · 0.72 · 0.63 · 0.90 · 1.25 · 1.61 · 1.30 · 0.63 · 0.72 · 0.99 · 0.63 · 0.90 · 0.90 · 0.76 · 0.63 | 0.031 · 0.035 · 0.036 · 0.041 · 0.035 · 0.030 · 0.032 · 0.038 · 0.040 · 0.039 · 0.034 · 0.032 · 0.033 · 0.034 · 0.039 · 0.038 · 0.033 · 0.030 | 100.0 % | 27.4 % |
| `wireplumber/gmain` | 0.009306 | 3.13 · 0.81 · 0.99 · 0.54 · 0.72 · 0.63 · 0.90 · 1.25 · 1.61 · 1.30 · 0.63 · 0.72 · 0.99 · 0.63 · 0.90 · 0.90 · 0.76 · 0.63 | 0.031 · 0.035 · 0.036 · 0.041 · 0.035 · 0.030 · 0.032 · 0.038 · 0.040 · 0.039 · 0.034 · 0.032 · 0.033 · 0.034 · 0.039 · 0.038 · 0.033 · 0.030 | 100.0 % | 27.4 % |

## service-manager (`session`, steady)

24 repeats, 18 whole windows of 100 s. Per component, pooled over the repeats: each window's wake rate over the component's mean over the windows, each window's run mean (ms), its share of the phase's CPU, and the CPU its windows hold above its median window as a share of the phase's CPU.

| component | wakes/s | wake rate per window, over its mean | run mean per window (ms) | share of CPU | above its median window |
|---|---|---|---|---|---|
| `ALL` | 0.07023 | 0.97 · 0.97 · 0.99 · 1.00 · 1.04 · 0.98 · 0.98 · 1.02 · 1.01 · 1.12 · 0.96 · 0.94 · 0.95 · 1.01 · 0.97 · 1.10 · 1.05 · 0.94 | 0.110 · 0.199 · 0.273 · 0.197 · 0.141 · 0.097 · 0.098 · 0.208 · 0.260 · 0.238 · 0.136 · 0.098 · 0.096 · 0.173 · 0.226 · 0.234 · 0.169 · 0.097 | 100.0 % | 15.1 % |
| `pid1/systemd` | 0.07023 | 0.97 · 0.97 · 0.99 · 1.00 · 1.04 · 0.98 · 0.98 · 1.02 · 1.01 · 1.12 · 0.96 · 0.94 · 0.95 · 1.01 · 0.97 · 1.10 · 1.05 · 0.94 | 0.110 · 0.199 · 0.273 · 0.197 · 0.141 · 0.097 · 0.098 · 0.208 · 0.260 · 0.238 · 0.136 · 0.098 · 0.096 · 0.173 · 0.226 · 0.234 · 0.169 · 0.097 | 100.0 % | 15.1 % |

## message-bus (`session`, steady)

24 repeats, 18 whole windows of 100 s. Per component, pooled over the repeats: each window's wake rate over the component's mean over the windows, each window's run mean (ms), its share of the phase's CPU, and the CPU its windows hold above its median window as a share of the phase's CPU.

| component | wakes/s | wake rate per window, over its mean | run mean per window (ms) | share of CPU | above its median window |
|---|---|---|---|---|---|
| `ALL` | 0.01396 | 0.00 · 1.07 · 2.30 · 1.19 · 0.54 · 0.00 · 0.00 · 1.49 · 2.30 · 2.36 · 0.54 · 0.06 · 0.00 · 0.99 · 1.91 · 2.21 · 1.04 · 0.00 | — · 0.142 · 0.116 · 0.147 · 0.180 · — · — · 0.154 · 0.121 · 0.094 · 0.126 · 0.472 · — · 0.125 · 0.097 · 0.100 · 0.126 · — | 100.0 % | 32.8 % |
| `system-bus/dbus-daemon` | 0.01396 | 0.00 · 1.07 · 2.30 · 1.19 · 0.54 · 0.00 · 0.00 · 1.49 · 2.30 · 2.36 · 0.54 · 0.06 · 0.00 · 0.99 · 1.91 · 2.21 · 1.04 · 0.00 | — · 0.142 · 0.116 · 0.147 · 0.180 · — · — · 0.154 · 0.121 · 0.094 · 0.126 · 0.472 · — · 0.125 · 0.097 · 0.100 · 0.126 · — | 100.0 % | 32.8 % |
