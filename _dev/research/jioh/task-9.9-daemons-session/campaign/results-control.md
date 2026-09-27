# Untraced control — session

## message-bus (`session`)

6 jobs (3 traced untraced, 3 untraced traced); builds: dbus-daemon 1.14.10-4ubuntu4.1 (1, 2, 3, 4, 5, 6).
2 intervals read; at 95 % chance alone gives about 0.1 differences; differences found: 0.

| value | traced median | untraced median | medians' ratio | per-job mean | 95 % interval | reading | by order | n | exited (CPU, wakes) | left out (CPU, wakes) |
|---|---|---|---|---|---|---|---|---|---|---|
| dbus-daemon system-bus/dbus-daemon run mean (ms) | 0.2619 | 0.2625 | 1.0024 | 0.9913 | 0.8897–1.0929 | not resolved | traced first 0.9565; untraced first 1.0261 | 6 | 0, 0 | 0.964, 0.931 |
| dbus-daemon system-bus/dbus-daemon wakes/s | 0.1395 | 0.1352 | 0.9695 | 0.9938 | 0.8967–1.0908 | not resolved | traced first 1.0342; untraced first 0.9533 | 6 | 0, 0 | 0.964, 0.931 |

The traced runs against the carried pool (decision 17): largest |z| 1.19 over 18 values.

## compositor-shell (`session`)

6 jobs (3 traced untraced, 3 untraced traced); builds: gnome-shell 46.0-0ubuntu6~24.04.15 (1, 2, 3, 4, 5, 6).
6 intervals read; at 95 % chance alone gives about 0.3 differences; differences found: 1 (gnome-shell gnome-shell/JS Helper run mean (ms)).

| value | traced median | untraced median | medians' ratio | per-job mean | 95 % interval | reading | by order | n | exited (CPU, wakes) | left out (CPU, wakes) |
|---|---|---|---|---|---|---|---|---|---|---|
| gnome-shell gnome-shell/JS Helper run mean (ms) | 0.0149 | 0.0131 | 0.8784 | 0.864 | 0.8414–0.8865 | difference | traced first 0.8486; untraced first 0.8793 | 6 | 0, 0 | 0, 0 |
| gnome-shell gnome-shell/JS Helper wakes/s | 0.3028 | 0.3086 | 1.0192 | 1.0186 | 0.9946–1.0426 | not resolved | traced first 1.0235; untraced first 1.0137 | 6 | 0, 0 | 0, 0 |
| gnome-shell gnome-shell/gmain run mean (ms) | 0.0734 | 0.0733 | 0.9986 | 1.0015 | 0.9514–1.0516 | not resolved | traced first 0.9977; untraced first 1.0053 | 6 | 0, 0 | 0, 0 |
| gnome-shell gnome-shell/gmain wakes/s | 0.2501 | 0.25 | 0.9996 | 1.0001 | 0.9989–1.0013 | not resolved | traced first 0.9993; untraced first 1.0009 | 6 | 0, 0 | 0, 0 |
| gnome-shell gnome-shell/gnome-shell run mean (ms) | 5.7492 | 5.5954 | 0.9732 | 0.977 | 0.9296–1.0245 | not resolved | traced first 0.9503; untraced first 1.0038 | 6 | 0, 0 | 0, 0 |
| gnome-shell gnome-shell/gnome-shell wakes/s | 0.0349 | 0.0339 | 0.9713 | 0.9921 | 0.9594–1.0248 | not resolved | traced first 0.9819; untraced first 1.0023 | 6 | 0, 0 | 0, 0 |

The traced runs against the carried pool (decision 17): largest |z| 1.19 over 18 values.

## audio-server (`session`)

6 jobs (3 traced untraced, 3 untraced traced); builds: pipewire 1.0.5-1ubuntu3.3, wireplumber 0.4.17-1ubuntu4.1 (1, 2, 3, 4, 5, 6).
2 intervals read; at 95 % chance alone gives about 0.1 differences; differences found: 0.

| value | traced median | untraced median | medians' ratio | per-job mean | 95 % interval | reading | by order | n | exited (CPU, wakes) | left out (CPU, wakes) |
|---|---|---|---|---|---|---|---|---|---|---|
| pipewire wireplumber/gmain run mean (ms) | 0.0555 | 0.0571 | 1.0289 | 1.0175 | 0.966–1.069 | not resolved | traced first 1.0202; untraced first 1.0147 | 6 | 0, 0 | 0.984, 0.984 |
| pipewire wireplumber/gmain wakes/s | 0.213 | 0.2133 | 1.0014 | 0.9971 | 0.9879–1.0064 | not resolved | traced first 0.9911; untraced first 1.0031 | 6 | 0, 0 | 0.984, 0.984 |

The traced runs against the carried pool (decision 17): largest |z| 1.19 over 18 values.

## service-manager (`session`)

6 jobs (3 traced untraced, 3 untraced traced); builds: systemd 255.4-1ubuntu8.17 (1, 2, 3, 4, 5, 6).
2 intervals read; at 95 % chance alone gives about 0.1 differences; differences found: 0.

| value | traced median | untraced median | medians' ratio | per-job mean | 95 % interval | reading | by order | n | exited (CPU, wakes) | left out (CPU, wakes) |
|---|---|---|---|---|---|---|---|---|---|---|
| systemd pid1/systemd run mean (ms) | 0.2723 | 0.2553 | 0.9378 | 0.9671 | 0.9011–1.0331 | not resolved | traced first 0.9938; untraced first 0.9405 | 6 | 0, 0 | 0.748, 0.611 |
| systemd pid1/systemd wakes/s | 0.178 | 0.1775 | 0.9969 | 0.9903 | 0.9763–1.0044 | not resolved | traced first 0.9973; untraced first 0.9833 | 6 | 0, 0 | 0.748, 0.611 |

The traced runs against the carried pool (decision 17): largest |z| 1.19 over 18 values.
