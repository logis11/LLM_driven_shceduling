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
| `ALL` | 0.002894 | 7.20 · 0.86 · 0.86 · 0.00 · 0.29 · 0.00 · 0.00 · 2.30 · 2.88 · 1.58 · 0.00 · 0.29 · 0.29 · 0.29 · 0.58 · 0.00 · 0.58 · 0.00 | 0.031 · 0.035 · 0.042 · — · 0.041 · — · — · 0.039 · 0.041 · 0.040 · — · 0.036 · 0.041 · 0.032 · 0.041 · — · 0.031 · — | 100.0 % | 78.7 % |
| `wireplumber/gmain` | 0.002894 | 7.20 · 0.86 · 0.86 · 0.00 · 0.29 · 0.00 · 0.00 · 2.30 · 2.88 · 1.58 · 0.00 · 0.29 · 0.29 · 0.29 · 0.58 · 0.00 · 0.58 · 0.00 | 0.031 · 0.035 · 0.042 · — · 0.041 · — · — · 0.039 · 0.041 · 0.040 · — · 0.036 · 0.041 · 0.032 · 0.041 · — · 0.031 · — | 100.0 % | 78.7 % |

## service-manager (`session`, steady)

24 repeats, 18 whole windows of 100 s. Per component, pooled over the repeats: each window's wake rate over the component's mean over the windows, each window's run mean (ms), its share of the phase's CPU, and the CPU its windows hold above its median window as a share of the phase's CPU.

| component | wakes/s | wake rate per window, over its mean | run mean per window (ms) | share of CPU | above its median window |
|---|---|---|---|---|---|
| `ALL` | 0.06866 | 1.00 · 0.96 · 0.96 · 0.98 · 1.06 · 1.00 · 1.01 · 1.02 · 0.98 · 1.09 · 0.97 · 0.96 · 0.97 · 1.01 · 0.94 · 1.06 · 1.06 · 0.96 | 0.110 · 0.154 · 0.188 · 0.133 · 0.115 · 0.097 · 0.098 · 0.164 · 0.171 · 0.132 · 0.114 · 0.098 · 0.096 · 0.128 · 0.131 · 0.132 · 0.147 · 0.097 | 100.0 % | 9.8 % |
| `pid1/systemd` | 0.06866 | 1.00 · 0.96 · 0.96 · 0.98 · 1.06 · 1.00 · 1.01 · 1.02 · 0.98 · 1.09 · 0.97 · 0.96 · 0.97 · 1.01 · 0.94 · 1.06 · 1.06 · 0.96 | 0.110 · 0.154 · 0.188 · 0.133 · 0.115 · 0.097 · 0.098 · 0.164 · 0.171 · 0.132 · 0.114 · 0.098 · 0.096 · 0.128 · 0.131 · 0.132 · 0.147 · 0.097 | 100.0 % | 9.8 % |

## message-bus (`session`, steady)

24 repeats, 18 whole windows of 100 s. Per component, pooled over the repeats: each window's wake rate over the component's mean over the windows, each window's run mean (ms), its share of the phase's CPU, and the CPU its windows hold above its median window as a share of the phase's CPU.

| component | wakes/s | wake rate per window, over its mean | run mean per window (ms) | share of CPU | above its median window |
|---|---|---|---|---|---|
| `ALL` | 0.005602 | 0.00 · 1.64 · 2.68 · 1.12 · 0.67 · 0.00 · 0.00 · 2.53 · 2.31 · 1.04 · 0.60 · 0.15 · 0.00 · 1.19 · 1.04 · 1.12 · 1.93 · 0.00 | — · 0.145 · 0.138 · 0.167 · 0.246 · — · — · 0.162 · 0.155 · 0.156 · 0.152 · 0.472 · — · 0.134 · 0.149 · 0.142 · 0.137 · — | 100.0 % | 31.6 % |
| `system-bus/dbus-daemon` | 0.005602 | 0.00 · 1.64 · 2.68 · 1.12 · 0.67 · 0.00 · 0.00 · 2.53 · 2.31 · 1.04 · 0.60 · 0.15 · 0.00 · 1.19 · 1.04 · 1.12 · 1.93 · 0.00 | — · 0.145 · 0.138 · 0.167 · 0.246 · — · — · 0.162 · 0.155 · 0.156 · 0.152 · 0.472 · — · 0.134 · 0.149 · 0.142 · 0.137 · — | 100.0 % | 31.6 % |
