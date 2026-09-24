# 9.9 session campaign — pooled results (meas-ci:session:2026-09-24)

Machine: EPYC 7763. `probe` jobs are never repeats.

Repeats: [47, 48, 49, 51, 58, 60, 61, 62, 63, 68, 69, 71, 72, 73, 74, 75, 76, 77, 79, 83, 85, 86, 87, 88]  ·  mode full

Kernel-thread schedule-ins on the measured CPU per repeat (D14, reported): {47: 15087, 48: 14091, 49: 14623, 51: 13546, 58: 14136, 60: 14520, 61: 15115, 62: 12005, 63: 13553, 68: 15472, 69: 12645, 71: 13416, 72: 12197, 73: 13040, 74: 13207, 75: 14602, 76: 13090, 77: 11608, 79: 13244, 83: 13927, 85: 11644, 86: 14226, 87: 11982, 88: 12104}

## gnome-shell

Components ['gnome-shell/JS Helper', 'gnome-shell/gmain', 'gnome-shell/gnome-shell'] cover 0.9997 of 0.587 wakes/s; residual False; sporadic [{'comm': 'residual', 'comms': ['gnome-shell/gnome-s:disk$0'], 'repeats': [47, 48, 49, 51], 'wakes_per_s': 0.0002}]

## pipewire

Components ['wireplumber/gmain'] cover 1.0 of 0.213 wakes/s; residual False; sporadic []

## systemd

Components ['pid1/systemd'] cover 0.999 of 0.179 wakes/s; residual False; sporadic [{'comm': 'residual', 'comms': ['user-manager/systemd'], 'repeats': [47, 48, 49, 51], 'wakes_per_s': 0.0002}]

## dbus-daemon

Components ['system-bus/dbus-daemon'] cover 1.0 of 0.137 wakes/s; residual False; sporadic []

| quantity | k | mean | half-width | passes |
|---|---|---|---|---|
| gnome-shell gnome-shell/JS Helper wakes/s | 24 | 0.3025 | ±0.7% | yes |
| gnome-shell gnome-shell/JS Helper gap mean (ms) | 24 | 13049.3382 | ±0.7% | yes |
| gnome-shell gnome-shell/JS Helper run mean (ms) | 24 | 0.0137 | ±1.5% | yes |
| gnome-shell gnome-shell/gmain wakes/s | 24 | 0.2499 | ±0.0% | yes |
| gnome-shell gnome-shell/gmain gap mean (ms) | 24 | 4001.4877 | ±0.0% | yes |
| gnome-shell gnome-shell/gmain run mean (ms) | 24 | 0.0497 | ±2.2% | yes |
| gnome-shell gnome-shell/gnome-shell wakes/s | 24 | 0.0348 | ±1.5% | yes |
| gnome-shell gnome-shell/gnome-shell gap mean (ms) | 24 | 28746.3389 | ±1.6% | yes |
| gnome-shell gnome-shell/gnome-shell run mean (ms) | 24 | 5.7007 | ±2.8% | yes |
| pipewire wireplumber/gmain wakes/s | 24 | 0.2132 | ±0.3% | yes |
| pipewire wireplumber/gmain gap mean (ms) | 24 | 4679.9217 | ±0.3% | yes |
| pipewire wireplumber/gmain run mean (ms) | 24 | 0.0383 | ±3.7% | yes |
| systemd pid1/systemd wakes/s | 24 | 0.1792 | ±0.7% | yes |
| systemd pid1/systemd gap mean (ms) | 24 | 5569.7184 | ±0.7% | yes |
| systemd pid1/systemd run mean (ms) | 24 | 0.246 | ±3.5% | yes |
| dbus-daemon system-bus/dbus-daemon wakes/s | 24 | 0.1368 | ±3.0% | yes |
| dbus-daemon system-bus/dbus-daemon gap mean (ms) | 24 | 7332.5298 | ±2.7% | yes |
| dbus-daemon system-bus/dbus-daemon run mean (ms) | 24 | 0.2784 | ±2.9% | yes |

