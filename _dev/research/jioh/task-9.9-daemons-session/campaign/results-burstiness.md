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

24 repeats; wakes/s, median over the streams: measured 0.009, compiled 0.008. Dispersion (variance over mean of the wake counts per bin), median (least–largest) over the streams; the ratio measured over compiled, per stream.

| bin | measured | compiled | measured / compiled |
|---|---|---|---|
| 1 ms | 1 (1–1) | 1 (1–1) | 1 (1–1) |
| 10 ms | 0.9999 (0.9999–0.9999) | 0.9999 (0.9998–1) | 1 (0.9999–1) |
| 100 ms | 0.9991 (0.9988–1.11) | 0.9992 (0.9984–1.082) | 0.9999 (0.9233–1.111) |
| 1 s | 1.928 (1.461–2.226) | 2.221 (1.33–4.32) | 0.8564 (0.3655–1.498) |

## service-manager (`session`, steady)

24 repeats; wakes/s, median over the streams: measured 0.07, compiled 0.069. Dispersion (variance over mean of the wake counts per bin), median (least–largest) over the streams; the ratio measured over compiled, per stream.

| bin | measured | compiled | measured / compiled |
|---|---|---|---|
| 1 ms | 0.9999 (0.9999–1.23) | 0.9999 (0.9999–1.018) | 1 (0.9827–1.23) |
| 10 ms | 1.015 (0.9993–1.575) | 1.016 (0.9993–1.069) | 0.9999 (0.9464–1.576) |
| 100 ms | 1.087 (0.993–2.028) | 1.048 (0.9931–1.091) | 1.026 (0.9099–2.042) |
| 1 s | 1.068 (0.93–2.016) | 1.03 (0.9433–1.157) | 1.045 (0.8266–2.025) |

## message-bus (`session`, steady)

24 repeats; wakes/s, median over the streams: measured 0.013, compiled 0.012. Dispersion (variance over mean of the wake counts per bin), median (least–largest) over the streams; the ratio measured over compiled, per stream.

| bin | measured | compiled | measured / compiled |
|---|---|---|---|
| 1 ms | 3.708 (3.055–5.286) | 3.518 (1.4–4.636) | 1.09 (0.7765–2.183) |
| 10 ms | 5.873 (4.647–9.286) | 7.115 (1.8–18.05) | 1.043 (0.3097–2.963) |
| 100 ms | 6.999 (5.888–12.5) | 7.114 (1.8–19.89) | 1.115 (0.3164–5.277) |
| 1 s | 7.093 (6.285–12.48) | 7.814 (1.797–19.87) | 0.9701 (0.3162–5.275) |
