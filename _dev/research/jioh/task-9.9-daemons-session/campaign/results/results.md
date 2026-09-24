# 9.9 session campaign — pooled results (meas-ci:session:2026-09-24)

Machine: EPYC 7763. `probe` jobs are never repeats.

Repeats: [47, 48, 49, 51, 58, 60, 61, 62, 63, 68, 69, 71, 72, 73, 74, 75, 76, 77, 79, 83, 85, 86, 87, 88]  ·  mode full

Kernel-thread schedule-ins on the measured CPU per repeat (D14, reported): {47: 15087, 48: 14091, 49: 14623, 51: 13546, 58: 14136, 60: 14520, 61: 15115, 62: 12005, 63: 13553, 68: 15472, 69: 12645, 71: 13416, 72: 12197, 73: 13040, 74: 13207, 75: 14602, 76: 13090, 77: 11608, 79: 13244, 83: 13927, 85: 11644, 86: 14226, 87: 11982, 88: 12104}

## gnome-shell

Components ['gnome-shell/JS Helper', 'gnome-shell/gmain', 'gnome-shell/gnome-shell'] cover 0.9997 of 0.587 wakes/s; residual False; sporadic [{'comm': 'residual', 'comms': ['gnome-shell/gnome-s:disk$0'], 'repeats': [47, 48, 49, 51], 'wakes_per_s': 0.0002}]

Left the components by cause (D27), wakes over the pooled repeats: outside — php8.3-fpm.service (php8.3-fpm) 4

## pipewire

Components ['wireplumber/gmain'] cover 1.0 of 0.009 wakes/s; residual False; sporadic []

Left the components by cause (D27), wakes over the pooled repeats: outside — hosted-compute-agent.service (the harness) 8657; outside — job phpsessionclean (php-common) 94; outside — job podman (podman) 8; event — job anacron (anacron) 32; event — job sysstat-daily-sample (sysstat) 8; event — job sysstat-summary (sysstat) 6; event — job motd-news (base-files) 4; event — job fstrim (util-linux) 1

## systemd

Components ['pid1/systemd'] cover 1.0 of 0.075 wakes/s; residual False; sporadic []

Left the components by cause (D27), wakes over the pooled repeats: outside — php8.3-fpm.service (php8.3-fpm) 4425; outside — job podman (podman) 26; outside — job phpsessionclean (php-common) 24; event — anacron.service (anacron) 14; event — job anacron (anacron) 12; event — job sysstat-summary (sysstat) 4; event — job man-db (man-db) 4; event — job motd-news (base-files) 2; event — job fstrim (util-linux) 1

## dbus-daemon

Components ['system-bus/dbus-daemon'] cover 1.0 of 0.014 wakes/s; residual False; sporadic []

Left the components by cause (D27), wakes over the pooled repeats: outside — php8.3-fpm.service (php8.3-fpm) 4989; outside — job phpsessionclean (php-common) 149; outside — job podman (podman) 92; event — job sysstat-summary (sysstat) 22; event — anacron.service (anacron) 13; event — job anacron (anacron) 11; event — job motd-news (base-files) 10; event — job fstrim (util-linux) 7; event — job man-db (man-db) 7

| quantity | k | mean | half-width | passes |
|---|---|---|---|---|
| gnome-shell gnome-shell/JS Helper wakes/s | 24 | 0.3025 | ±0.7% | yes |
| gnome-shell gnome-shell/JS Helper gap mean (ms) | 24 | 3306.7344 | ±0.7% | yes |
| gnome-shell gnome-shell/JS Helper run mean (ms) | 24 | 0.0137 | ±1.5% | yes |
| gnome-shell gnome-shell/gmain wakes/s | 24 | 0.2498 | ±0.1% | yes |
| gnome-shell gnome-shell/gmain gap mean (ms) | 24 | 4002.606 | ±0.1% | yes |
| gnome-shell gnome-shell/gmain run mean (ms) | 24 | 0.0497 | ±2.2% | yes |
| gnome-shell gnome-shell/gnome-shell wakes/s | 24 | 0.0347 | ±1.5% | yes |
| gnome-shell gnome-shell/gnome-shell gap mean (ms) | 24 | 28813.9483 | ±1.5% | yes |
| gnome-shell gnome-shell/gnome-shell run mean (ms) | 24 | 5.7035 | ±2.8% | yes |
| pipewire wireplumber/gmain wakes/s | 24 | 0.0093 | ±4.5% | yes |
| pipewire wireplumber/gmain gap mean (ms) | 24 | 108583.7999 | ±4.4% | yes |
| pipewire wireplumber/gmain run mean (ms) | 24 | 0.0351 | ±3.0% | yes |
| systemd pid1/systemd wakes/s | 24 | 0.075 | ±2.0% | yes |
| systemd pid1/systemd gap mean (ms) | 24 | 13368.8769 | ±1.9% | yes |
| systemd pid1/systemd run mean (ms) | 24 | 0.1676 | ±7.8% | carried (D29) |
| dbus-daemon system-bus/dbus-daemon wakes/s | 24 | 0.0141 | ±11.9% | carried (D29) |
| dbus-daemon system-bus/dbus-daemon gap mean (ms) | 24 | 76135.7654 | ±11.3% | carried (D29) |
| dbus-daemon system-bus/dbus-daemon run mean (ms) | 24 | 0.1173 | ±11.0% | carried (D29) |

