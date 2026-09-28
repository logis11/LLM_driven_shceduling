# Compiled burstiness — desktop

## renderer-hidden (`chrome-hidden`, steady)

228 streams, one per renderer, over 19 repeats; wakes/s, median over the streams: measured 0.173, compiled 0.167. Dispersion (variance over mean of the wake counts per bin), median (least–largest) over the streams; the ratio measured over compiled, per stream.

| bin | measured | compiled | measured / compiled |
|---|---|---|---|
| 1 ms | 1.08 (1.018–1.329) | 1.019 (0.9998–1.408) | 1.057 (0.7923–1.33) |
| 10 ms | 1.187 (1.036–1.443) | 1.02 (0.9982–1.445) | 1.14 (0.7708–1.417) |
| 100 ms | 1.19 (1.054–1.549) | 1.025 (0.982–1.429) | 1.149 (0.8354–1.545) |
| 1 s | 1.23 (1.009–1.873) | 0.9899 (0.8533–1.391) | 1.242 (0.9468–1.876) |

## renderer-visible (`chrome-visible`, steady-notimer)

132 streams, one per renderer, over 11 repeats; wakes/s, median over the streams: measured 0.141, compiled 0.14. Dispersion (variance over mean of the wake counts per bin), median (least–largest) over the streams; the ratio measured over compiled, per stream.

| bin | measured | compiled | measured / compiled |
|---|---|---|---|
| 1 ms | 1.101 (1.023–1.556) | 1.046 (0.9998–2.031) | 1.068 (0.5258–1.449) |
| 10 ms | 1.258 (1.096–1.702) | 1.07 (0.9986–2.917) | 1.192 (0.429–1.664) |
| 100 ms | 1.353 (1.215–1.85) | 1.08 (0.9858–3.494) | 1.225 (0.3873–1.725) |
| 1 s | 1.261 (1.085–2.006) | 1.01 (0.87–3.347) | 1.231 (0.3654–2.029) |

## chat-client (`element`, idle)

18 repeats; wakes/s, median over the streams: measured 12.35, compiled 12.206. Dispersion (variance over mean of the wake counts per bin), median (least–largest) over the streams; the ratio measured over compiled, per stream.

| bin | measured | compiled | measured / compiled |
|---|---|---|---|
| 1 ms | 11.7 (10.46–12.69) | 3.553 (3.368–3.724) | 3.275 (3.018–3.587) |
| 10 ms | 49.23 (45.29–51.37) | 7.646 (6.738–8.244) | 6.447 (6.035–7.204) |
| 100 ms | 113.4 (106.7–118.2) | 10.21 (8.831–12.23) | 11.26 (9.176–12.36) |
| 1 s | 119.2 (113.7–128.5) | 12.03 (9.649–14.12) | 10.03 (8.05–12.19) |

## game-client (`steam`, shown)

12 repeats; wakes/s, median over the streams: measured 298.992, compiled 299.515. Dispersion (variance over mean of the wake counts per bin), median (least–largest) over the streams; the ratio measured over compiled, per stream.

| bin | measured | compiled | measured / compiled |
|---|---|---|---|
| 1 ms | 3.448 (3.343–3.923) | 1.783 (1.774–1.798) | 1.938 (1.859–2.2) |
| 10 ms | 4.398 (3.614–5.394) | 2.101 (2.07–2.157) | 2.084 (1.746–2.545) |
| 100 ms | 5.418 (3.69–6.026) | 1.812 (1.734–1.857) | 2.985 (1.995–3.408) |
| 1 s | 1.369 (1.037–2.658) | 1.539 (1.386–1.698) | 0.9128 (0.716–1.917) |
