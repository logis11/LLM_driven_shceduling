# The stability rule's stopping, simulated

Each entry's widest value the rule is read on, its repeats drawn at the value's per-repeat spread and the rule run on it alone, 4000 simulated campaigns per distribution: the stopped mean's bias, the share of stopped 95 % intervals covering the true mean, the mean count at the stop. Where the count at the stop falls well short of the repeats obtained, other values set the count, and the value's own stopping does not describe how the campaign stopped.

| entry | widest value | repeats | spread (CV) | half-width | mean bias (normal · lognormal) | coverage (normal · lognormal) | count at the stop (normal · lognormal) |
|---|---|---|---|---|---|---|---|
| `office-writer` | input_run mean, 136M (ms) | 14 | 8.59 % | 4.96 % | +0.12 % · -0.02 % | 92.7 % · 91.3 % | 12.8 · 12.8 |
| `code-editor` | idle renderer/ThreadPoolForeg run mean (ms) | 44 | 12.17 % | 3.70 % | stopped at its recording's last window | | |
| `web-browser` | idle renderer/chrome run mean (ms) | 38 | 13.30 % | 4.37 % | stopped at its recording's last window | | |
| `mail-client` | idle WebExtensions/StreamTrans run mean (ms) | 77 | 20.93 % | 4.75 % | +0.20 % · -0.04 % | 93.8 % · 93.2 % | 68.2 · 67.8 |
| `image-editor` | op script-fu run mean (ms) | 5 | 3.54 % | 4.40 % | -0.01 % · -0.02 % | 94.8 % · 94.8 % | 5.4 · 5.4 |
| `video-editor` | driven kdenlive run mean (ms) | 20 | 10.68 % | 5.00 % | +0.14 % · -0.08 % | 91.3 % · 91.4 % | 18.3 · 18.4 |
| `audio-player` | play CPU share | 31 | 12.75 % | 4.68 % | +0.20 % · -0.09 % | 92.4 % · 92.1 % | 25.5 · 25.5 |
| `video-player` | play CPU share | 24 | 6.77 % | 2.86 % | +0.09 % · -0.06 % | 93.2 % · 93.5 % | 9.1 · 9.1 |
| `video-call` | play CPU share | 45 | 5.07 % | 1.52 % | +0.04 % · -0.01 % | 94.2 % · 94.3 % | 6.7 · 6.7 |
