# Compiled burstiness — session

## compositor-shell (`session`, steady)

24 repeats; wakes/s, median over the streams: measured 0.588, compiled 0.581. Dispersion (variance over mean of the wake counts per bin), median (least–largest) over the streams; the ratio measured over compiled, per stream.

| bin | measured | compiled | measured / compiled |
|---|---|---|---|
| 1 ms | 5.525 (4.65–6.082) | 5.379 (3.584–7.742) | 0.9724 (0.6999–1.353) |
| 10 ms | 7.013 (6.5–11.58) | 8.546 (4.792–13.9) | 0.8564 (0.6385–2.038) |
| 100 ms | 10.81 (6.452–12.06) | 12.1 (5.983–18.16) | 0.9071 (0.5074–1.75) |
| 1 s | 10.28 (9.91–11.53) | 12.67 (6.463–28.47) | 0.8156 (0.361–1.54) |

## audio-server (`session`, steady)

24 repeats; wakes/s, median over the streams: measured 0.003, compiled 0.003. Dispersion (variance over mean of the wake counts per bin), median (least–largest) over the streams; the ratio measured over compiled, per stream.

| bin | measured | compiled | measured / compiled |
|---|---|---|---|
| 1 ms | 1 (1–1) | 1 (1–1) | 1 (1–1) |
| 10 ms | 1 (0.9999–1) | 1 (0.9999–1) | 1 (0.9999–1) |
| 100 ms | 0.9997 (0.9993–0.9999) | 0.9997 (0.9991–0.9999) | 0.9999 (0.9995–1.001) |
| 1 s | 1.797 (0.9972–2.33) | 1.53 (0.9983–2.616) | 1.187 (0.4061–2) |

## service-manager (`session`, steady)

24 repeats; wakes/s, median over the streams: measured 0.068, compiled 0.067. Dispersion (variance over mean of the wake counts per bin), median (least–largest) over the streams; the ratio measured over compiled, per stream.

| bin | measured | compiled | measured / compiled |
|---|---|---|---|
| 1 ms | 0.9999 (0.9999–1.235) | 0.9999 (0.9999–1.018) | 1 (0.9821–1.235) |
| 10 ms | 0.9994 (0.9993–1.573) | 1.014 (0.9993–1.084) | 1 (0.932–1.574) |
| 100 ms | 1.056 (0.9932–2.007) | 1.026 (0.9932–1.095) | 1.032 (0.9075–2.021) |
| 1 s | 1.022 (0.9317–1.998) | 1.02 (0.9383–1.128) | 1.037 (0.8707–2.108) |

## message-bus (`session`, steady)

24 repeats; wakes/s, median over the streams: measured 0.004, compiled 0.004. Dispersion (variance over mean of the wake counts per bin), median (least–largest) over the streams; the ratio measured over compiled, per stream.

| bin | measured | compiled | measured / compiled |
|---|---|---|---|
| 1 ms | 3.542 (1–5) | 2.714 (1–4.875) | 1.235 (0.3684–3.167) |
| 10 ms | 5.314 (1–6.25) | 3.857 (1–9.312) | 1.359 (0.5091–4.167) |
| 100 ms | 7.142 (2–8.999) | 5.199 (0.9999–23.56) | 1.615 (0.3784–5.334) |
| 1 s | 7.386 (1.999–8.995) | 5.794 (0.9994–23.54) | 1.38 (0.588–5.338) |
