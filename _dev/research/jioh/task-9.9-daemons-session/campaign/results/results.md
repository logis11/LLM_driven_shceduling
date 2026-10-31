# 9.9 session campaign — pooled results (meas-ci:session:2026-09-24)

Machine: EPYC 7763. `probe` jobs are never repeats.

Repeats: [47, 48, 49, 51, 58, 60, 61, 62, 63, 68, 69, 71, 72, 73, 74, 75, 76, 77, 79, 83, 85, 86, 87, 88]  ·  mode full

Kernel-thread schedule-ins on the measured CPU per repeat (D14, reported): {47: 15087, 48: 14091, 49: 14623, 51: 13546, 58: 14136, 60: 14520, 61: 15115, 62: 12005, 63: 13553, 68: 15472, 69: 12645, 71: 13416, 72: 12197, 73: 13040, 74: 13207, 75: 14602, 76: 13090, 77: 11608, 79: 13244, 83: 13927, 85: 11644, 86: 14226, 87: 11982, 88: 12104}

## gnome-shell

Components ['gnome-shell/JS Helper', 'gnome-shell/gmain', 'gnome-shell/gnome-shell'] cover 0.9997 of 0.587 wakes/s; residual False; sporadic [{'comm': 'residual', 'comms': ['gnome-shell/gnome-s:disk$0'], 'repeats': [47, 48, 49, 51], 'wakes_per_s': 0.0002}]

Left the components by cause (D27), wakes over the pooled repeats: outside — php8.3-fpm.service (php8.3-fpm) 4

## pipewire

Components ['wireplumber/gmain', 'wireplumber/gmain [event]'] cover 1.0 of 0.006 wakes/s; residual False; sporadic []

Left the components by cause (D27), wakes over the pooled repeats: outside — hosted-compute-agent.service (the harness) 8657; outside — job phpsessionclean (php-common) 94; outside — job podman (podman) 8; event — job anacron (anacron) 32; event — job sysstat-daily-sample (sysstat) 8; event — job sysstat-summary (sysstat) 6; event — job motd-news (base-files) 4; event — job fstrim (util-linux) 1

## systemd

Components ['pid1/systemd [event]'] cover 0.0 of 0.0 wakes/s; residual False; sporadic [{'comm': 'pid1/systemd', 'repeats': [58, 60, 61, 77, 87, 88], 'wakes_per_s': 0.0004}]

Left the components by cause (D27), wakes over the pooled repeats: outside — php8.3-fpm.service (php8.3-fpm) 4425; outside — systemd-networkd.service (systemd) 204; outside — job podman (podman) 26; outside — job phpsessionclean (php-common) 24; event — anacron.service (anacron) 14; event — job anacron (anacron) 12; event — job sysstat-summary (sysstat) 4; event — job man-db (man-db) 4; event — job motd-news (base-files) 2; event — job fstrim (util-linux) 1

## dbus-daemon

Components ['system-bus/dbus-daemon [event]'] cover 0.0 of 0.0 wakes/s; residual False; sporadic [{'comm': 'system-bus/dbus-daemon', 'repeats': [58, 60, 77, 87, 88], 'wakes_per_s': 0.0002}]

Left the components by cause (D27), wakes over the pooled repeats: outside — php8.3-fpm.service (php8.3-fpm) 4989; outside — job phpsessionclean (php-common) 149; outside — job podman (podman) 92; outside — systemd-networkd.service (systemd) 6; event — job sysstat-summary (sysstat) 22; event — anacron.service (anacron) 13; event — job anacron (anacron) 11; event — job motd-news (base-files) 10; event — job fstrim (util-linux) 7; event — job man-db (man-db) 7

| quantity | k | mean | half-width | passes |
|---|---|---|---|---|
| gnome-shell gnome-shell/JS Helper wakes/s | 24 | 0.3025 | ±0.7% | yes |
| gnome-shell gnome-shell/JS Helper gap mean (ms) | 24 | 3305.79 | ±0.7% | yes |
| gnome-shell gnome-shell/JS Helper run mean (ms) | 24 | 0.0137 | ±1.0% | yes |
| gnome-shell gnome-shell/gmain wakes/s | 24 | 0.2498 | ±0.1% | yes |
| gnome-shell gnome-shell/gmain gap mean (ms) | 24 | 4002.6002 | ±0.1% | yes |
| gnome-shell gnome-shell/gmain run mean (ms) | 24 | 0.0497 | ±2.1% | yes |
| gnome-shell gnome-shell/gnome-shell wakes/s | 24 | 0.0347 | ±1.5% | yes |
| gnome-shell gnome-shell/gnome-shell gap mean (ms) | 24 | 28780.8556 | ±1.5% | yes |
| gnome-shell gnome-shell/gnome-shell run mean (ms) | 24 | 5.6996 | ±2.8% | yes |
| pipewire wireplumber/gmain wakes/s | 24 | 0.006 | ±8.1% | carried (D29) |
| pipewire wireplumber/gmain gap mean (ms) | 24 | 165517.4877 | ±8.1% | carried (D29) |
| pipewire wireplumber/gmain run mean (ms) | 24 | 0.0341 | ±3.2% | yes |
| pipewire wireplumber/gmain [event] wakes/s | 24 | 0.0033 | ±3.2% | yes |
| pipewire wireplumber/gmain [event] gap mean (ms) | 24 | 306383.4346 | ±3.2% | yes |
| pipewire wireplumber/gmain [event] run mean (ms) | 24 | 0.0369 | ±3.5% | yes |
| systemd pid1/systemd [event] wakes/s | 24 | 0.0698 | ±1.6% | yes |
| systemd pid1/systemd [event] gap mean (ms) | 24 | 14318.8811 | ±1.6% | yes |
| systemd pid1/systemd [event] run mean (ms) | 24 | 0.1652 | ±6.6% | carried (D29) |
| dbus-daemon system-bus/dbus-daemon [event] wakes/s | 24 | 0.0137 | ±10.3% | carried (D29) |
| dbus-daemon system-bus/dbus-daemon [event] gap mean (ms) | 24 | 72850.0241 | ±10.3% | carried (D29) |
| dbus-daemon system-bus/dbus-daemon [event] run mean (ms) | 24 | 0.1162 | ±9.8% | carried (D29) |

