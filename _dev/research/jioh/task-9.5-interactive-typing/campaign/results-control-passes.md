# The untraced control's operation passes, by operation

## web-browser (`chrome`, the `page-load` operation's two passes)

Each control job traces one of its two passes; the traced pass's rows inside the operations, pooled over the jobs that traced it. `utility/ThreadPoolForeg` read under their own names, every other thread as `other`.

### The first pass traced (jobs 1, 3, 5)

6 whole windows of 100 s, each holding the operations triggered in it, read over their time. Per thread: each window's wake rate over the thread's mean over the windows, each window's run mean (ms), its share of the pass's CPU, and the CPU its windows hold above its median window as a share of the pass's CPU.

| component | wakes/s | wake rate per window, over its mean | run mean per window (ms) | share of CPU | above its median window |
|---|---|---|---|---|---|
| `ALL` | 2251 | 0.99 · 1.01 · 1.00 · 1.02 · 1.00 · 0.98 | 0.289 · 0.313 · 0.317 · 0.312 · 0.316 · 0.327 | 100.0 % | 0.3 % |
| `other` | 2217 | 0.96 · 1.02 · 1.01 · 1.02 · 1.01 · 0.99 | 0.302 · 0.315 · 0.319 · 0.316 · 0.318 · 0.328 | 99.8 % | 0.3 % |
| `utility/ThreadPoolForeg` | 33.93 | 3.16 · 0.43 · 0.43 · 1.11 · 0.49 · 0.39 | 0.035 · 0.035 · 0.036 · 0.031 · 0.034 · 0.039 | 0.2 % | 0.1 % |

By operation, in blocks of 6 (56 operations a pass, the last block the remaining 2), each block read over its operations' time. Per thread: each block's wake rate over the thread's mean over the blocks, each block's run mean (ms), its share of the pass's CPU, and the CPU its blocks hold above its median block as a share of the pass's CPU.

| component | wakes/s | wake rate per block, over its mean | run mean per block (ms) | share of CPU | above its median block |
|---|---|---|---|---|---|
| `ALL` | 2247 | 1.01 · 0.98 · 1.01 · 1.01 · 1.02 · 1.01 · 0.99 · 1.01 · 0.98 · 0.99 | 0.269 · 0.317 · 0.319 · 0.312 · 0.318 · 0.313 · 0.319 · 0.310 · 0.330 · 0.327 | 100.0 % | 1.0 % |
| `other` | 2215 | 0.96 · 0.99 · 1.02 · 1.01 · 1.01 · 1.02 · 0.99 · 1.02 · 0.99 · 1.00 | 0.287 · 0.319 · 0.321 · 0.314 · 0.324 · 0.315 · 0.321 · 0.312 · 0.332 · 0.328 | 99.8 % | 1.0 % |
| `utility/ThreadPoolForeg` | 32.04 | 4.90 · 0.41 · 0.46 · 0.47 · 1.56 · 0.42 · 0.56 · 0.47 · 0.44 · 0.32 | 0.034 · 0.039 · 0.034 · 0.034 · 0.031 · 0.036 · 0.031 · 0.037 · 0.036 · 0.052 | 0.2 % | 0.1 % |

`utility/ThreadPoolForeg` per job: its wakes in each of the pass's first 3 operations, and its wake rate over the rest (/s).

| job | wakes in operations 1–3 | wakes/s after |
|---|---|---|
| 1 | 545 · 7 · 7 | 19.8 |
| 3 | 556 · 10 · 12 | 16.9 |
| 5 | 417 · 11 · 9 | 19.1 |

### The second pass traced (jobs 2, 4, 6)

6 whole windows of 100 s, each holding the operations triggered in it, read over their time. Per thread: each window's wake rate over the thread's mean over the windows, each window's run mean (ms), its share of the pass's CPU, and the CPU its windows hold above its median window as a share of the pass's CPU.

| component | wakes/s | wake rate per window, over its mean | run mean per window (ms) | share of CPU | above its median window |
|---|---|---|---|---|---|
| `ALL` | 2299 | 1.04 · 0.99 · 0.99 · 1.01 · 0.98 · 0.99 | 0.299 · 0.307 · 0.304 · 0.298 · 0.311 · 0.305 | 100.0 % | 0.6 % |
| `other` | 2276 | 1.03 · 1.00 · 0.99 · 1.00 · 0.99 · 0.99 | 0.304 · 0.309 · 0.306 · 0.303 · 0.312 · 0.307 | 99.9 % | 0.5 % |
| `utility/ThreadPoolForeg` | 22.49 | 1.91 · 0.57 · 0.60 · 1.78 · 0.57 · 0.58 | 0.023 · 0.034 · 0.030 · 0.025 · 0.031 · 0.032 | 0.1 % | 0.0 % |

By operation, in blocks of 6 (56 operations a pass, the last block the remaining 2), each block read over its operations' time. Per thread: each block's wake rate over the thread's mean over the blocks, each block's run mean (ms), its share of the pass's CPU, and the CPU its blocks hold above its median block as a share of the pass's CPU.

| component | wakes/s | wake rate per block, over its mean | run mean per block (ms) | share of CPU | above its median block |
|---|---|---|---|---|---|
| `ALL` | 2294 | 1.06 · 1.00 · 0.98 · 1.01 · 1.00 · 1.02 · 0.98 · 0.98 · 1.01 · 0.97 | 0.296 · 0.306 · 0.309 · 0.305 · 0.295 · 0.302 · 0.317 · 0.301 · 0.303 · 0.315 | 100.0 % | 0.5 % |
| `other` | 2273 | 1.04 · 1.00 · 0.99 · 1.01 · 1.00 · 1.00 · 0.98 · 0.98 · 1.01 · 0.97 | 0.303 · 0.307 · 0.311 · 0.306 · 0.296 · 0.308 · 0.319 · 0.303 · 0.305 · 0.317 | 99.9 % | 0.4 % |
| `utility/ThreadPoolForeg` | 21.79 | 2.81 · 0.63 · 0.55 · 0.59 · 0.62 · 2.42 · 0.66 · 0.54 · 0.59 · 0.58 | 0.022 · 0.029 · 0.036 · 0.031 · 0.031 · 0.025 · 0.028 · 0.034 · 0.031 · 0.034 | 0.1 % | 0.0 % |

`utility/ThreadPoolForeg` per job: its wakes in each of the pass's first 3 operations, and its wake rate over the rest (/s).

| job | wakes in operations 1–3 | wakes/s after |
|---|---|---|
| 2 | 6 · 162 · 9 | 18.4 |
| 4 | 7 · 150 · 9 | 17.8 |
| 6 | 7 · 149 · 3 | 16.9 |

## mail-client (`thunderbird-send`, the `send` operation's two passes)

Each control job traces one of its two passes; the traced pass's rows inside the operations, pooled over the jobs that traced it. `Socket Thread`, `TaskCon~ller` read under their own names, every other thread as `other`.

### The first pass traced (jobs 1, 3, 5)

6 whole windows of 100 s, each holding the operations triggered in it, read over their time. Per thread: each window's wake rate over the thread's mean over the windows, each window's run mean (ms), its share of the pass's CPU, and the CPU its windows hold above its median window as a share of the pass's CPU.

| component | wakes/s | wake rate per window, over its mean | run mean per window (ms) | share of CPU | above its median window |
|---|---|---|---|---|---|
| `ALL` | 2328 | 0.98 · 0.99 · 1.00 · 1.00 · 1.00 · 1.03 | 0.328 · 0.325 · 0.329 · 0.332 · 0.338 · 0.329 | 100.0 % | 0.9 % |
| `Socket Thread` | 732.9 | 0.87 · 0.93 · 0.98 · 1.03 · 1.05 · 1.14 | 0.024 · 0.022 · 0.022 · 0.021 · 0.021 · 0.020 | 2.0 % | 0.0 % |
| `TaskCon~ller` | 43.52 | 1.17 · 1.12 · 1.03 · 0.96 · 0.89 · 0.82 | 0.161 · 0.157 · 0.179 · 0.180 · 0.197 · 0.202 | 1.0 % | 0.0 % |
| `other` | 1551 | 1.02 · 1.02 · 1.01 · 0.99 · 0.98 · 0.98 | 0.455 · 0.460 · 0.475 · 0.489 · 0.503 · 0.502 | 96.9 % | 0.9 % |

By operation, in blocks of 3 (25 operations a pass, the last block the remaining 1), each block read over its operations' time. Per thread: each block's wake rate over the thread's mean over the blocks, each block's run mean (ms), its share of the pass's CPU, and the CPU its blocks hold above its median block as a share of the pass's CPU.

| component | wakes/s | wake rate per block, over its mean | run mean per block (ms) | share of CPU | above its median block |
|---|---|---|---|---|---|
| `ALL` | 2337 | 0.98 · 0.98 · 1.00 · 0.99 · 1.00 · 0.99 · 1.00 · 1.02 · 1.05 | 0.327 · 0.326 · 0.326 · 0.329 · 0.332 · 0.336 · 0.338 · 0.331 · 0.323 | 100.0 % | 0.7 % |
| `Socket Thread` | 740.3 | 0.87 · 0.88 · 0.94 · 0.97 · 1.03 · 1.00 · 1.06 · 1.14 · 1.12 | 0.024 · 0.022 · 0.022 · 0.021 · 0.021 · 0.022 · 0.021 · 0.020 · 0.019 | 2.0 % | 0.0 % |
| `TaskCon~ller` | 43.03 | 1.21 · 1.17 · 1.06 · 1.07 · 0.97 · 0.96 · 0.89 · 0.82 · 0.86 | 0.154 · 0.165 · 0.163 · 0.182 · 0.181 · 0.181 · 0.198 · 0.193 · 0.230 | 1.0 % | 0.0 % |
| `other` | 1554 | 1.02 · 1.02 · 1.02 · 1.00 · 0.98 · 0.99 · 0.97 · 0.97 · 1.02 | 0.455 · 0.457 · 0.464 · 0.475 · 0.491 · 0.492 · 0.506 · 0.508 · 0.484 | 96.9 % | 0.7 % |

`Socket Thread` per job: its wakes in each of the pass's first 3 operations, and its wake rate over the rest (/s).

| job | wakes in operations 1–3 | wakes/s after |
|---|---|---|
| 1 | 2329 · 2236 · 1767 | 770.1 |
| 3 | 1993 · 1819 · 1738 | 739.5 |
| 5 | 1683 · 1715 · 1819 | 731.8 |

`TaskCon~ller` per job: its wakes in each of the pass's first 3 operations, and its wake rate over the rest (/s).

| job | wakes in operations 1–3 | wakes/s after |
|---|---|---|
| 1 | 162 · 148 · 139 | 44.7 |
| 3 | 167 · 150 · 165 | 42.9 |
| 5 | 151 · 148 · 151 | 39.5 |

### The second pass traced (jobs 2, 4, 6)

6 whole windows of 100 s, each holding the operations triggered in it, read over their time. Per thread: each window's wake rate over the thread's mean over the windows, each window's run mean (ms), its share of the pass's CPU, and the CPU its windows hold above its median window as a share of the pass's CPU.

| component | wakes/s | wake rate per window, over its mean | run mean per window (ms) | share of CPU | above its median window |
|---|---|---|---|---|---|
| `ALL` | 2426 | 0.99 · 0.97 · 0.99 · 0.99 · 1.04 · 1.02 | 0.330 · 0.343 · 0.339 · 0.343 · 0.326 · 0.335 | 100.0 % | 0.5 % |
| `Socket Thread` | 894.9 | 0.94 · 0.95 · 0.97 · 0.97 · 1.10 · 1.08 | 0.019 · 0.020 · 0.019 · 0.020 · 0.016 · 0.017 | 2.1 % | 0.0 % |
| `TaskCon~ller` | 28.34 | 1.22 · 1.21 · 1.00 · 0.87 · 0.89 · 0.82 | 0.215 · 0.217 · 0.257 · 0.271 · 0.319 · 0.326 | 0.9 % | 0.0 % |
| `other` | 1503 | 1.01 · 0.99 · 1.00 · 1.00 · 1.01 · 0.99 | 0.505 · 0.530 · 0.525 · 0.530 · 0.525 · 0.541 | 97.0 % | 0.5 % |

By operation, in blocks of 3 (25 operations a pass, the last block the remaining 1), each block read over its operations' time. Per thread: each block's wake rate over the thread's mean over the blocks, each block's run mean (ms), its share of the pass's CPU, and the CPU its blocks hold above its median block as a share of the pass's CPU.

| component | wakes/s | wake rate per block, over its mean | run mean per block (ms) | share of CPU | above its median block |
|---|---|---|---|---|---|
| `ALL` | 2432 | 0.99 · 0.98 · 0.97 · 0.98 · 0.99 · 1.01 · 1.04 · 1.01 · 1.03 | 0.331 · 0.336 · 0.343 · 0.340 · 0.341 · 0.336 · 0.326 · 0.337 · 0.329 | 100.0 % | 0.4 % |
| `Socket Thread` | 901.2 | 0.94 · 0.94 · 0.93 · 0.96 · 0.98 · 1.01 · 1.09 · 1.06 · 1.09 | 0.019 · 0.019 · 0.020 · 0.020 · 0.020 · 0.019 · 0.016 · 0.018 · 0.017 | 2.0 % | 0.0 % |
| `TaskCon~ller` | 27.77 | 1.26 · 1.34 · 1.06 · 1.00 · 0.95 · 0.87 · 0.90 · 0.83 · 0.80 | 0.210 · 0.205 · 0.249 · 0.262 · 0.254 · 0.304 · 0.315 · 0.326 · 0.347 | 0.9 % | 0.0 % |
| `other` | 1503 | 1.01 · 1.00 · 0.99 · 1.00 · 0.99 · 1.01 · 1.01 · 0.99 · 1.00 | 0.508 · 0.518 · 0.527 · 0.526 · 0.533 · 0.528 · 0.527 · 0.543 · 0.532 | 97.0 % | 0.4 % |

`Socket Thread` per job: its wakes in each of the pass's first 3 operations, and its wake rate over the rest (/s).

| job | wakes in operations 1–3 | wakes/s after |
|---|---|---|
| 2 | 2493 · 2321 · 2834 | 959.8 |
| 4 | 2563 · 2614 · 2417 | 903.6 |
| 6 | 2419 · 2562 · 2872 | 846.3 |

`TaskCon~ller` per job: its wakes in each of the pass's first 3 operations, and its wake rate over the rest (/s).

| job | wakes in operations 1–3 | wakes/s after |
|---|---|---|
| 2 | 99 · 105 · 105 | 29.4 |
| 4 | 99 · 113 · 97 | 26.7 |
| 6 | 117 · 117 · 103 | 26.0 |
