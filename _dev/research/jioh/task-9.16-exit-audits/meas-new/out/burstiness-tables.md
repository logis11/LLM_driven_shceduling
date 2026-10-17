# Compiled burstiness — 9.16 re-run

## renderer-hidden (`chrome-hidden`, steady)

60 streams, one per renderer, over 5 repeats; wakes/s, median over the streams: measured 0.21, compiled 0.209. Dispersion (variance over mean of the wake counts per bin), median (least–largest) over the streams; the ratio measured over compiled, per stream.

| bin | measured | compiled | measured / compiled |
|---|---|---|---|
| 1 ms | 1.405 (1.343–1.523) | 1.103 (1.017–1.333) | 1.256 (1.05–1.454) |
| 10 ms | 1.478 (1.411–1.574) | 1.147 (1.032–1.398) | 1.282 (1.03–1.428) |
| 100 ms | 1.594 (1.42–2.055) | 1.159 (1.018–1.448) | 1.435 (0.9804–1.819) |
| 1 s | 1.864 (1.765–2.03) | 1.096 (0.9651–1.395) | 1.709 (1.265–1.944) |

## video-editor (`kdenlive`, idle)

16 repeats; wakes/s, median over the streams: measured 1.264, compiled 1.261. Dispersion (variance over mean of the wake counts per bin), median (least–largest) over the streams; the ratio measured over compiled, per stream.

| bin | measured | compiled | measured / compiled |
|---|---|---|---|
| 1 ms | 1.339 (1.082–1.707) | 1.083 (1.035–1.135) | 1.22 (0.9964–1.649) |
| 10 ms | 1.465 (1.154–1.828) | 1.101 (1.042–1.166) | 1.315 (1.049–1.738) |
| 100 ms | 1.407 (1.045–2.378) | 1.048 (0.9596–1.091) | 1.319 (0.991–2.478) |
| 1 s | 0.6401 (0.3–1.416) | 0.2169 (0.1611–0.2732) | 2.757 (1.116–7.964) |
