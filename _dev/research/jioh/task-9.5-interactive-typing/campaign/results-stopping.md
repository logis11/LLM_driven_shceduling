# The stability rule's stopping, simulated

Each entry's widest value the rule is read on, its repeats drawn at the value's per-repeat spread and the rule run on it alone, 4000 simulated campaigns per distribution: the stopped mean's bias, the share of stopped 95 % intervals covering the true mean, the mean count at the stop. Where the count at the stop falls well short of the repeats obtained, other values set the count, and the value's own stopping does not describe how the campaign stopped.

| entry | widest value | repeats | spread (CV) | half-width | mean bias (normal · lognormal) | coverage (normal · lognormal) | count at the stop (normal · lognormal) |
|---|---|---|---|---|---|---|---|
| `office-writer` | input_run mean, 136M (ms) | 14 | 8.59 % | 4.96 % | +0.12 % · -0.02 % | 92.7 % · 91.3 % | 12.8 · 12.8 |
| `code-editor` | input_run mean, SWELL-KW (ms) | 43 | 15.73 % | 4.84 % | stopped at window 44, short of its recording's 57, not by the rule | | |
| `web-browser` | idle renderer/chrome run mean (ms) | 38 | 13.29 % | 4.37 % | stopped at its recording's last window | | |
| `mail-client` | idle WebExtensions/StreamTrans run mean (ms) | 77 | 21.14 % | 4.80 % | +0.19 % · -0.04 % | 93.7 % · 94.1 % | 69.5 · 69.3 |
| `image-editor` | driven gimp run mean (ms) | 5 | 4.01 % | 4.98 % | -0.00 % · -0.00 % | 94.8 % · 94.4 % | 5.7 · 5.7 |
| `video-editor` | driven kdenlive wakes/s | 20 | 7.93 % | 3.71 % | +0.11 % · -0.07 % | 92.9 % · 92.1 % | 11.3 · 11.3 |
| `audio-player` | play CPU share | 31 | 12.75 % | 4.68 % | +0.20 % · -0.09 % | 92.4 % · 92.1 % | 25.5 · 25.5 |
| `video-player` | play CPU share | 24 | 6.77 % | 2.86 % | +0.09 % · -0.06 % | 93.2 % · 93.5 % | 9.1 · 9.1 |
| `video-call` | play CPU share | 45 | 5.07 % | 1.52 % | +0.04 % · -0.01 % | 94.2 % · 94.3 % | 6.7 · 6.7 |
