# Compiled burstiness — desktop

## renderer-hidden (`chrome-hidden`, steady)

60 streams, one per renderer, over 5 repeats; wakes/s, median over the streams: measured 0.21, compiled 0.209. Dispersion (variance over mean of the wake counts per bin), median (least–largest) over the streams; the ratio measured over compiled, per stream.

| bin | measured | compiled | measured / compiled |
|---|---|---|---|
| 1 ms | 1.405 (1.343–1.523) | 1.103 (1.017–1.333) | 1.256 (1.05–1.454) |
| 10 ms | 1.478 (1.411–1.574) | 1.147 (1.032–1.398) | 1.282 (1.03–1.428) |
| 100 ms | 1.594 (1.42–2.055) | 1.159 (1.018–1.448) | 1.435 (0.9804–1.819) |
| 1 s | 1.864 (1.765–2.03) | 1.096 (0.9651–1.395) | 1.709 (1.265–1.944) |

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
