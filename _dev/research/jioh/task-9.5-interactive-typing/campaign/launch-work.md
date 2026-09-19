# Launch work in the idle and play phases

The pooled repeats of `meas-ci:interactive:2026-09-18` and `meas-ci:playback:2026-09-18` read through `analyze.analyze_run` (wakeup-defined wakes; `chrome` without its renderer processes, D14), the idle phase (the play phase for the playback runs) cut into 10 s slices from its start, which is 30 s after the application's window appears (method §2). Per slice: the process tree's CPU (ms per second) and wakes per second. Changelog D34. Recorded 2026-09-19.

## Mean over the repeats, CPU ms/s per 10 s slice

| application | repeats | slices from the phase start |
|---|---|---|
| `soffice` (idle) | 1, 2, 3, 4, 5 | 0.6 0.6 0.6 0.6 0.6 0.6 0.6 0.6 0.6 0.6 0.6 0.6 |
| `code` (idle) | 1, 2, 3, 4, 5, 6, 7, 8 | 17.9 15.0 14.3 14.1 14.2 28.6 40.0 14.5 14.0 14.0 13.9 13.9 |
| `thunderbird` (idle) | 1, 2, 3, 4, 5, 6, 7, 8 | 2.7 9.3 10.3 0.1 0.4 0.1 0.5 19.7 4.4 0.1 0.2 0.1 |
| `chrome` (idle) | 1, 2, 3, 4, 5 | 2.5 1.2 12.6 49.9 2.3 1.5 20.5 1.6 21.0 1.4 1.5 1.3 |
| `kdenlive` (idle) | 1, 2, 3, 5 | 0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.1 |
| `mpv-video` (play) | 1, 2, 4 | 121.3 121.7 124.0 122.5 123.5 122.3 122.7 123.4 122.6 123.1 123.5 122.1 123.8 124.8 124.4 123.0 123.9 125.8 123.4 124.2 122.0 125.2 124.2 124.2 123.5 124.4 122.3 123.6 124.3 124.9 |
| `mpv-audio` (play) | 1, 2, 3, 4, 5, 6, 7, 8 | 7.6 7.7 7.6 7.8 7.9 7.5 7.4 7.5 7.7 7.5 7.6 7.5 7.3 7.3 7.3 7.6 7.7 7.8 7.6 7.6 7.6 7.5 7.4 7.5 7.3 7.4 7.1 7.2 7.2 7.1 |
| `webrtc` (play) | 1, 2, 3, 4, 5 | 1005.5 997.8 973.6 954.7 283.1 150.7 878.7 996.0 675.7 172.0 144.1 160.7 162.6 144.5 626.6 998.8 924.5 182.4 151.3 151.7 151.3 151.2 151.7 150.4 167.1 151.6 148.4 147.5 149.6 148.2 |
| `gimp` (idle) | 1, 2, 3, 5 | no wakes in the idle phase |

## Per repeat, the four applications with launch work

`chrome`:

- repeat 1: 2 1 5 54 4 1 1 1 2 1 1 1
- repeat 2: 4 1 13 51 2 2 1 2 2 1 1 1
- repeat 3: 3 1 15 51 2 2 2 2 3 2 2 2
- repeat 4: 2 1 15 47 1 1 97 2 2 1 2 1
- repeat 5: 2 1 14 45 1 2 1 1 96 1 1 1

`thunderbird`:

- repeat 1: 0.0 11.6 10.2 0.0 0.5 0.1 0.0 20.1 4.9 0.0 0.2 0.0
- repeat 2: 0.0 12.9 10.9 0.0 0.5 0.1 0.0 20.4 4.1 0.1 0.2 0.1
- repeat 3: 10.4 1.0 10.3 0.3 0.1 0.1 1.3 18.7 3.9 0.0 0.2 0.0
- repeat 4: 0.1 11.3 10.1 0.0 0.4 0.2 0.0 20.3 4.8 0.0 0.2 0.1
- repeat 5: 0.1 14.2 11.5 0.0 0.7 0.1 0.0 20.3 4.8 0.1 0.3 0.0
- repeat 6: 9.2 2.0 9.8 0.2 0.1 0.0 1.3 18.8 3.9 0.0 0.2 0.0
- repeat 7: 0.0 11.6 9.3 0.0 0.4 0.2 0.0 20.1 4.5 0.0 0.2 0.1
- repeat 8: 1.5 10.0 10.5 0.2 0.3 0.1 1.4 19.1 4.3 0.0 0.2 0.0

`code`:

- repeat 1: 20 18 16 16 16 21 53 16 16 16 16 16
- repeat 2: 17 14 13 13 13 27 39 13 13 13 13 13
- repeat 3: 20 15 14 14 14 27 39 14 14 14 14 14
- repeat 4: 18 16 15 15 15 38 35 15 15 15 15 15
- repeat 5: 18 15 15 14 15 36 34 15 15 14 14 14
- repeat 6: 17 14 13 13 13 26 40 13 13 13 13 13
- repeat 7: 15 13 12 12 12 25 37 12 12 12 12 12
- repeat 8: 18 16 15 15 15 29 42 16 15 15 15 15

`webrtc`:

- repeat 1: 1004 999 969 955 159 183 1004 1012 532 153 153 151 148 148 605 1005 971 152 153 147 150 150 149 142 150 157 148 147 142 141
- repeat 2: 1005 1001 971 953 144 129 1023 979 569 135 124 122 124 134 573 1012 984 176 165 168 160 148 153 142 234 144 135 130 136 128
- repeat 3: 1005 997 983 940 233 140 911 998 680 150 153 148 159 152 929 981 676 140 140 139 138 139 142 151 138 139 143 145 146 145
- repeat 4: 1009 994 977 944 694 158 474 987 1003 283 151 243 147 149 466 999 996 269 148 145 144 143 144 144 141 146 144 145 148 146
- repeat 5: 1004 998 968 982 186 143 982 1004 594 138 139 139 235 139 560 997 995 174 150 159 165 176 171 173 172 171 170 170 175 181

## Once-per-session runs

- `chrome`: the browser process's `ThreadPoolForeground` runs about 880 ms once per session (877, 879, 883, 886, 876 ms) at 152, 166, 180 s from the idle phase's start in repeats 1–3 (inside the driven phase) and at 65 and 85 s in repeats 4–5 (inside the idle phase); no run of that size recurs in the remaining phases of any repeat. The burst 29–39 s into the idle phase (runs of about 23, 80 and 67 ms) recurs in none either. In repeats 1–3 the window rule (D13) charges the 880 ms run to one input: per-repeat `input_run` means 2.42, 3.43, 2.85 ms against 0.31, 0.14 ms in repeats 4–5.
- `thunderbird`: a pool thread runs 142–145 ms at 70–74 s in every repeat, named `BgIOThr~Pool #1`, `#2` or `#3` by repeat (D33).
