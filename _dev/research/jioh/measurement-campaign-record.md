# Measured values — campaign record

Every campaign behind a measured archetype value: per archetype the repeats, the values the rule covers, the widest margin among them, why it stopped, and the machine draws it took. Method: `measurement-campaign-workflow.md`. Each row regenerates with `dataset/tools/meas/loop/pool_runs.py <family>/<app> --since 10` (`upgrade`: `--since 100`; `soffice`: `--since 38`; `chrome`: `--since 438 --exclude 16@35712250969`; `code`: `--since 566 --exclude 42@36126168885`; `thunderbird-send`: `--since 150 --exclude 29`, its keys-only campaign `--since 604`; the `desktop` family: `--since 21`, its `chrome-tabs`: `--since 74`, its `launch-*`: `--since 81` for `soffice`, `mpv-video`, `mpv-audio`, `kdenlive` and `element`, `--since 84` for the rest, `launch-kdenlive`'s re-trace of 2026-10-05: `--since 100`, `chrome-hidden`'s and `launch-chrome-hidden`'s campaign of 2026-10-05: `--since 105`; `kdenlive`'s idle repeats of 2026-10-05: `--since 664` with `MEAS_LOOP_MODE=idle`; the `session` family: `--since 16 -- --tag meas-ci:session:2026-09-24`); job counts are the campaign runs' jobs, read from their job lists. Recorded 2026-09-20, the 9.8 rows 2026-09-22, the 9.9 rows 2026-09-24, the three re-measured 9.5 rows 2026-09-24, `mail-client`'s keys-only row 2026-09-27, `code-editor`'s row re-read with its idle phase from 200 s 2026-09-28 (9.5 D83), `web-browser`'s with its renderers the same day (9.5 D84), `mail-client`'s two with each Gecko pool's shortened spelling folded into the pool and the 04:00 `glean.mps` run out of the idle residual the same day (9.5 D90, D91), `code-editor`'s stop re-read against the Word recording's 57 windows 2026-09-29 (9.5 D99); the 9.5 rows were first recorded a day earlier against one headline median per archetype, which D29 and D30 replaced. Every gap mean and wake rate re-read on 2026-09-24 under 9.5 D71 (gaps over merged wake times, wrapped round the span; rates from exact counts); the 9.8 renderer residuals re-classed as sparse components on 2026-09-25 (9.8 D27); the 9.9 pool rebuilt the same day with sysstat's jobs outside and two sparse components (9.9 D32, D33); every table's mean re-read on 2026-09-26 as the table carries it, count-weighted over the repeats (9.5 D78).

## Campaigns

All on GitHub-hosted `ubuntu-24.04` runners, 4 vCPU, pinned to one CPU, AMD EPYC 7763 only (machine gate); kernel `6.17.0-1022-azure` in every repeat of the build campaign and of all six 9.5 applications whose rule holds (their pooled records carry it per repeat). Stability rule (D29, D30, D78): for every value the fold-in carries — a rate or share by its per-repeat values, a table by its mean as the table carries it, count-weighted over the repeats (the ratio estimator's half-width, `cochran-st77`) — the 95 % confidence half-width is at most 5 % of it or 1 µs, whichever is larger, over at least five same-machine repeats (`dataset/tools/meas/stability.py`). A value whose phase holds the recorded input's last window is reported with its half-width instead, and left out of the rule (D32, D46).

| tag | slice | workflow | runs | first launch |
|---|---|---|---|---|
| `meas-ci:build:2026-09-18` | 9.6 | `meas-build.yml` | #10–#37; the 13 holding a landed repeat are #10, #11, #12, #15, #16, #22, #25, #26, #27, #29, #30, #32, #34 | 2026-09-18 09:09 UTC |
| `meas-ci:interactive:2026-09-18` | 9.5 | `meas-interactive.yml` | #10–#100 | 2026-09-18 09:56 UTC |
| `meas-ci:playback:2026-09-18` | 9.5 | `meas-playback.yml` | #10–#84 | 2026-09-18 09:56 UTC |
| `meas-ci:interactive:2026-09-19` | 9.5 | `meas-interactive.yml` | #150–#244, `thunderbird-send` alone (the `send` re-observation), and #651–#663, the 34 idle-only repeats added under D94 on 2026-09-28; `mail-client`'s idle phase since D80 | 2026-09-19 11:18 UTC |
| `meas-ci:background:2026-09-19` | 9.7 | `meas-background.yml` | #19–#98; `borg`'s repeats are in #24–#40, `steamcmd`'s pooled repeats in #47–#98 (repeats 24–34 from #59) | 2026-09-19 23:16 UTC |
| `meas-ci:interactive:2026-09-20` | 9.5 | `meas-interactive.yml` | #245–#565, `chrome` and `code` re-measured under D51 and D53; `code` restarted at #376 under D61 and `chrome` at #438 under D65; `code` restarted keys only at #566 under D72 (its campaign is the row below) | 2026-09-20 08:04 UTC |
| `meas-ci:playback:2026-09-20` | 9.5 | `meas-playback.yml` | #245–#565, `webrtc` re-measured under D54 | 2026-09-20 08:04 UTC |
| `meas-ci:desktop:2026-09-20` | 9.8 | `meas-desktop.yml` | #21–#50 | 2026-09-20 11:03 UTC |
| `meas-ci:interactive:2026-09-25` | 9.5 | `meas-interactive.yml` | #566–#599, `code` keys only under D72; 34 runs, 102 jobs (57 gated), windows 1–44 landed, the recording holding 57 (D73, D99) | 2026-09-25 00:19 UTC |
| `meas-ci:interactive:2026-09-27` | 9.5 | `meas-interactive.yml` | #604–#610, `thunderbird-send` keys only under D79; 7 runs, 20 jobs (12 gated), every window of the recording landed (D80); the dry checks #600 and #602 are not repeats | 2026-09-27 00:04 UTC |
| `meas-ci:session:2026-09-24` | 9.9 | `meas-session.yml` | #16–#22; the four holding a landed repeat are #16, #20, #21, #22 | 2026-09-23 23:35 UTC (2026-09-24 KST) |
| `meas-ci:background:2026-10-01` | 9.10 | `meas-background.yml` | #100–#105, app `upgrade`; the dry run #99 is not a repeat | 2026-10-01 10:07 UTC |
| `meas-ci:background:2026-10-02` | 9.10 | `meas-background.yml` | #108–#114, app `dkms`; the dry runs #106 and #107 are not repeats | 2026-10-02 08:36 UTC |

## 9.5 — nine archetypes measured

### The six measured first (D26, D29, D30)

Pooled in `task-9.5-interactive-typing/campaign/results-same-machine/` and rendered in `campaign/results-same-machine.md`. Every repeat on one AMD EPYC 7763, kernel `6.17.0-1022-azure` in all of them. `values` counts what the rule covers; `widest` is the largest half-width among them.

| archetype | application | repeats | values | widest | stopped by | jobs (gated) | recorded input covered |
|---|---|---|---|---|---|---|---|
| `office-writer` | `soffice` | 14 (windows 1–14) | 5 | `input_run` mean under 136M ±4.96 % | the rule | 19 (5) | SWELL-KW Word, participants 1–6 |
| `mail-client` | `thunderbird-send` | 77 (windows 1–28, 30–78) | 45 + 39 reported at the window limit (the 39 superseded by the keys-only campaign, D80) | idle `WebExtensions/StreamTrans` run mean ±4.75 % | the rule | 134 (55) | SWELL-KW Outlook, all 25 participants; windows 9 on are past the recording |
| `image-editor` | `gimp` | 5 (1, 2, 3, 5, 6) | 10 | op `script-fu` run mean ±4.40 % | the rule | 8 (3) | scripted pointer loop |
| `video-editor` | `kdenlive` | 20 (1–3, 5–21) | 22 | driven `kdenlive` run mean ±4.997 % | the rule | 30 (10) | scripted pointer loop |
| `video-player` | `mpv-video` | 24 (1, 2, 4, 6–26) | 3 since D75 (16 before) | play cycle run mean ±2.86 % (before D75: play `vo` wakes/s ±4.98 %) | the rule | 51 (27) | none |
| `audio-player` | `mpv-audio` | 31 (1–31) | 3 since D75 (16 before) | play cycle run mean ±4.68 % (before D75: play `ao` run mean ±4.93 %) | the rule | 55 (24) | none |

The typing-driven applications also replay the 136M Keystrokes windows 1…k of their own repeats in the `driven-alt` phase (the pre-registered stimulus check). Read per repeat (D81, as 9.7 D36 reads a check), the per-input run mean under 136M against SWELL-KW: `office-writer` 1.123 (95 % interval 1.045–1.200) and `web-browser` 1.338 (1.284–1.392; 1.160 before its renderers were carried, D84), differences; `code-editor` 1.029 (0.968–1.090), not resolved; `mail-client` 0.909 (0.824–0.994) over its keys-only pool, a difference, where its pooled medians move the other way (+8 %).

**What the half-widths do and do not claim** (noted 2026-09-24, in self-review; no decision taken, and it is 9.14's and 9.16's to resolve). The loop adds one repeat at a time and stops when every value the rule covers is inside the tolerance, so the value that stopped an application sat at the boundary by construction: `soffice` 4.93 %, `mpv-audio` 4.93 %, `kdenlive` 4.94 %, `webrtc` 4.95 %, `mpv-video` 4.98 %, `thunderbird-send` 5.00 %, `gimp` 4.59 %. In the pools as they stand on 2026-09-26 — read as 9.5 D71 reads them, `code` re-measured (D73), the playback entries one job per cycle (D75), the multiplier exact past twenty repeats (9.6 D35), each table's mean read as it carries it (D78) — each application's widest value the rule is read on is `kdenlive` 4.997 %, `soffice` 4.96 %, `mpv-audio` 4.68 %, `code` 4.46 %, `gimp` 4.40 %, `thunderbird-send` 3.87 %, `chrome` 2.89 %, `mpv-video` 2.86 %, `webrtc` 1.52 %; three of the nine sit within half a point of the line. Dropping any single repeat moves the mean of each application's widest value by 0.30–1.49 % (`leave_one_out` in each pooled record). Stopping at the first crossing cannot bias a mean, so the values themselves stand; it does make the stated precision of that one value per application optimistic, because the count was chosen by the estimate it produced. Across the library 7 of the 133 values the rule is read on — every value of the pooled records neither at a recording's window limit nor carried under an exception — have half-widths of 4.5 % or more, beside two held by the 1 µs floor (`7z`'s and `steamcmd`'s block per run); the rest cleared it with room. `chrome` is the exception — it stopped at its recording's last window, not at the rule, and its widest value the rule is read on is 2.89 %. So is `code` since its keys-only campaign (D73): stopped at window 44, then read as its recording's last — the recording holds 57 (D99) — its widest value the rule is read on 4.46 %, `libuv-worker`'s wake rate, the component on the rule since D78. `gimp` rests on the five-repeat minimum.

Reported precision would be clean rather than caveated if the binding values were re-measured at a count fixed in advance and their half-widths read once, without re-testing: about three hours for `webrtc`, `mpv-video` and `mpv-audio` at some twelve minutes a repeat, about a day for `chrome` and `code`.

**Decided 2026-09-28 (9.5 D88):** the stated precision is reported with a caveat. Simulated at each entry's widest value the rule is read on (`meas/stopping.py`, `campaign/results-stopping.md`), the rule's stated 95 % interval covers the true mean in 91–93 % of campaigns where that value sits within half a point of the tolerance (`office-writer`, `video-editor`, `audio-player`, stated in their scopes), and the stopped mean leans by at most 0.2 % — the tolerance is relative to the mean, so the stop depends on it.

- `office-writer`: the first design's five repeats (the stream's clicks, scrolls and drags replayed with the keys; `input_run` p50 8.67, 3.99, 5.91, 4.53, 4.21 ms, ±44 %) are superseded by D28 and not pooled; their 11 jobs, 6 of them gated, are not in the count above.
- `mail-client`: it took 43 repeats against the 29 first projected, because its idle phase holds a ~60 s `StreamTrans` episode that comes out big 6 to 9 times per 600 s window against 10 cycles, which kept the idle `StreamTrans` gap mean at the top of the tolerance. Window 29 is left out of the pool (D47), its Outlook window having been launched uncut; 77 jobs counted here exclude that repeat's job, one cancelled duplicate and one dry check. The 39 values of the phases that replay a window — the two per-input means and 37 of the operation's — are reported with their half-widths over the eight full repeats, the recording's last window (D32, D46). Under D94 a Gecko child's threads are components of their own, and the idle pool's rule needed 77: the main process's `JS Watchdog` wake rate ±6.38 % and `WebExtensions/StreamTrans`' values ±6.67–6.75 % at 43. 34 idle-only repeats, windows 45–78, were added as one batch at that projection (runs #651–#663, 2026-09-28; 57 jobs, 23 stopped by the gate), and the rule holds at 77.
- `video-player`: its `vo` thread's projection swung between 24 and 31 repeats over ten repeats before settling; the rule held at 24.
- The three playback entries since D75 (2026-09-26): each carries one periodic job per medium cycle — its period the mean interval between cycle starts read off a reference thread, its run the process tree's whole CPU per cycle — in place of its components, so the values the rule covers are the play-phase CPU share, the cycle length mean and the cycle run mean: `audio-player` 49.635 ms, run mean 0.352 ms (±4.79 %); `video-player` 33.348 ms, 4.062 ms (±2.89 %); `video-call` 10.001 ms, 2.371 ms (±1.58 %); cycle lengths ±0.00–0.02 %. Read from the pools the campaigns closed, no repeat added; none of them is a value that stopped a campaign.
- `image-editor`, `video-editor`, `video-player`: the windows the gate stopped (4; 4; 3 and 5) were not retried once the rule held.

### The three re-measured (D51, D53, D54), finished 2026-09-24; `code` again, keys only, finished 2026-09-25 (D72, D73); `mail-client`'s phases with or after the input, keys only, finished 2026-09-27 (D79, D80)

Pooled in `task-9.5-interactive-typing/campaign/results-re-measured/` and rendered in `campaign/results-re-measured.md`. Every repeat on one AMD EPYC 7763, kernel `6.17.0-1022-azure`. Components are identified by process role and comm (D67), so a comm naming a thread of several processes is several components.

| archetype | application | repeats | values | widest | stopped by | jobs (gated) | recorded input covered |
|---|---|---|---|---|---|---|---|
| `web-browser` | `chrome` | 38 (windows 1–38) | 21 + 39 reported at the window limit | idle `renderer/chrome` run mean ±4.37 %; at the limit, `input_run` mean under SWELL-KW ±5.90 % | the recording's last window (D32, D68) | 71 (31) | SWELL-KW Internet Explorer c1, every window the recording holds |
| `code-editor` | `code` | 44 (windows 1–44; 43 idle only, no event recorded) | 26 + 3 carried (D57) | `input_run` mean under SWELL-KW ±4.84 % | window 44, then read as the recording's last; the recording holds 57 (D99) | 102 (57) | SWELL-KW Word c1, windows 1–44 of 57 |
| `mail-client` | `thunderbird-send` | 8 (windows 1–8); the idle phase the 77 of `meas-ci:interactive:2026-09-19` | 39 reported at the window limit; the idle phase's 45 from the 77 | idle `WebExtensions/StreamTrans` run mean ±4.75 % (from the 77); at the limit, op `StreamTrans` run mean ±18.42 % | the recording's last window (D32, D46) | 20 (12) | SWELL-KW Outlook c2 and c3, every window the recording holds |
| `video-call` | `webrtc` | 45 | 3 since D75 (39 + 7 carried (D57) before) | play cycle run mean ±1.52 % (before D75: play `gpu/Chrome_ChildIOT` gap mean ±4.95 %) | the rule | 102 (57) | none |

- `web-browser`: its renderers are carried since D84 — the typed-into page's, the spare renderer the page load takes over and Chrome's own WebUI renderer; other tabs' and windows' renderers are the renderer entries'. Its 39 values at the window limit are the operation phase's 36 (D46), the operation's duration mean and the two per-input means; the widest is the `input_run` mean under SWELL-KW, 4.274 ms ±5.90 %, outside the rule at the recording's last window (the rule would need 52 repeats) — ±5.46 % by its per-repeat means, whose spread follows how densely each participant typed: the recording's tail is sparse, windows 29, 35, 36, 37 and 38 replaying 47, 53, 80, 61 and 27 events against 200–1,300 earlier (D32), and the carried mean weighs each window by its inputs. The 136M check's mean, 5.415 ms, is ±3.37 % over the same repeats. Before D84 the two per-input means were 1.671 ms ±4.72 % and 1.903 ms ±3.93 %, the renderers holding 59 % and 65 % of each key's CPU and 74 % of each page load's. One job was cancelled mid-measurement (window 31, cancelled with the `code` job that shared its run) and is not counted.
- `code-editor`: the keys-only campaign (D72, D73): 44 repeats, VS Code 1.138.0 in every one; window 43 records no event and ran the idle phase alone; window 42's later copy (#599) left out under D66. The idle phase is read from 200 s past its start (D83): the main thread's and the residual's runs carry two launch episodes 50–75 s and 150–175 s into the phase that never recur over the D52 probe's 1,400 s. Its two per-input values hold the rule — SWELL-KW 99.26 ms ±4.84 %, 136M 103.9 ms ±3.01 %, read as carried (D78; by their per-repeat means 105.8 ms ±5.01 % and 106.4 ms ±3.79 %) — the SWELL-KW mean having projected 47 repeats at 41; the campaign stopped at window 44, then read as the Word recording's last; the recording holds 57 windows, 56 with input (D99); `utility/libuv-worker`'s wake rate and gap mean are carried under D57 again at ±5.63 % (read over the whole 900 s they held the rule at ±4.46 % from D78), its run mean ±2.36 % within the rule. Every repeat's screenshot after the SWELL-KW phase was read: the letters at the file's end, no view opened. The superseded D61 campaign (41 repeats, pointer events replayed) read 92.31 ms under SWELL-KW and +15 % under 136M by their per-repeat means; keys only, the two streams' medians are 79.71 and 82.29 ms (+3 %), their carried means 99.26 and 103.9 ms (+4.7 %).
- `mail-client`: the keys-only campaign (D79, D80): 8 repeats, windows 1–8, Thunderbird 156.0.1 in every one; its SWELL-KW phase replays the Outlook stream's keys into the message body and its 136M phase starts from the empty body in the Paragraph format (two dry runs, #600 and #602, checked the prelude). Every repeat's screenshots were read: after the SWELL-KW phase the letters in the body and To empty, after the prelude the body empty in the Paragraph format, after the 136M phase its letters in the body. Its 39 values at the window limit: `input_run` mean under SWELL-KW 6.052 ms ±10.41 % (the rule would need 27 repeats), under 136M 5.644 ms ±4.79 %; the send's duration mean 2,971 ms ±2.11 %; 8 of the operation's 36 component values outside the rule, widest `StreamT~ns` run mean ±18.71 %. The 43-repeat campaign, the stream's clicks and drags replayed, read 6.867 ms ±8.57 %, 6.296 ms ±6.90 % and 3,074 ms ±2.76 %; the sensitivity check reads +8 % on the p50 where it read +9 %. The idle phase stays the 43 repeats' (it runs before any input); the eight repeats' own idle phases select the same eleven components and every idle value within 0.86 standard deviations of the 43 repeats' spread (median 0.21).
- `video-call`: the seven values carried under D57 are the audio path (D59), widest ±5.82 %; `play gpu/Chrome_ChildIOT`'s gap mean took 45 repeats, its wake rate taking discrete levels between sessions — 64.3–65.2 a second in 34 repeats, ~54 in four, ~46.6 in five, 36.5 in one. Since D75 the entry carries the call's 10 ms audio-frame cycle, not its components, so these seven values leave it; they stay in the pooled record.
- The builds are stated per repeat (D69): `code` 1.138.0 in all 44; `chrome` 152.0.7977.82 in 29 and 153.0.8010.52 in 9 (windows 18, 20, 22, 27, 31, 33, 34, 37, 38); `webrtc` 152.0.7977.82 in 42 and 153.0.8010.52 in 3 (windows 37, 40, 45); `mail-client` Thunderbird 156.0 in 43 of the idle phase's 77, 156.0.1 in the 34 added under D94 and in the keys-only 8; read by build against the 156.0 repeats' own spread (D94), 43 of the 45 idle values within 0.78 standard deviations, and `WebExtensions/IPC I/O Child`'s wake rate and gap mean, 22 wakes a phase in every 156.0 repeat and in 33 of the 34 156.0.1 repeats, differing by 0.1 %; Thunderbird's snap store serves its channels' current revisions, 156.0's revision 1259 in none of them (D96), so that mix too is carried and stated. Google's repository serves only its current version, so the mix is carried and stated: over `chrome`'s 38 repeats every carried value agrees between the two builds within 0.18–1.09 standard deviations of the 152 repeats' own spread, the operation duration within 0.38 and the 136M mean within 0.13; re-read with its renderers (D84, 2026-09-28), the 23 idle values within 0.04–1.54, the SWELL-KW mean within 0.49 and the 136M mean within 0.22; read over all 60 carried values (D93, the same day), 59 within 1.80 and the page load's `gpu/VizCompositorTh` run mean at −2.31, 16.0 % lower under 153 with 8 of its 9 repeats below every 152 repeat, stated in the scope.

They replaced these values (D55):

| archetype | application | why | replaces |
|---|---|---|---|
| `web-browser` | `chrome` | its 30 s settle left the launch burst in the idle phase, about 35 times the steady level; settle now 270 s (D51) | 5 repeats, page-load duration p50 472.7 ms |
| `code-editor` | `code` | a launch-anchored episode every ~320 s put its idle CPU 15.5 % above the long-run level at the placement every repeat takes; idle phase now 900 s (D53) | 22 repeats, `input_run` p50 74.69 ms |
| `video-call` | `webrtc` | the call's saturation recurs every 240 s, so a 300 s play phase measured the ramp-up and read CPU 78 % above the steady call; settle 210 s, play phase 480 s (D54) | 5 repeats, play-phase CPU share 0.4084 |

`mail-client` was `thunderbird` (8 windows, `input_run` p50 4.325 ms, ±8.47 %, stopped by the input's end) until the `send` re-observation replaced it whole (9.7 D3, D36).

### The untraced control (D82), finished 2026-09-27

Each carried phase run twice in every job, traced under `perf sched record` and untraced, each thread's CPU time and switches read from `/proc` at both edges of each run; each value's per-job ratios, untraced over traced, read by their 95 % interval (the 9.5 untraced-control spec). Six jobs per subject, three in each order, every one on the AMD EPYC 7763; the carried values unchanged, each entry's notes carrying its reading. Runs `meas-ci:interactive` and `meas-ci:playback` #620–#649; `video-player`'s window 2 landed twice and its later copy is left out (D66).

| archetype | subject | jobs | build | intervals | differences (chance) | traced against carried, largest \|z\| |
|---|---|---|---|---|---|---|
| `web-browser` | `chrome` | 6 | Google Chrome 153.0.8010.52 | 40 | 10 (2.0) | 3.11 since D84 (6.31 before) — disagrees: the second page-load pass (stated) |
| `code-editor` | `code` | 6 | VS Code 1.138.0 | 19 | 3 (1.0) | 3.24 since D83 (10.83 before) — disagrees: the second idle run's residual run mean (stated) |
| `image-editor` | `gimp` | 6 | GIMP 2.10.36 | 7 | 3 (0.4) | 51.72 — disagrees: the prelude's state (stated) |
| `video-editor` | `kdenlive` | 6 | Kdenlive `4:23.08.5-0ubuntu4` | 13 | 2 (0.7) | 0.98 — agrees |
| `audio-player` | `mpv-audio` | 6 | mpv 0.37.0 | 1 | 1 (0.1) | 0.11 — agrees |
| `video-player` | `mpv-video` | 6 | mpv 0.37.0 | 1 | 1 (0.1) | 1.41 — agrees |
| `office-writer` | `soffice` | 6 | LibreOffice 24.2.7.2 | 3 | 2 (0.2) | 0.8 — agrees |
| `mail-client` | `thunderbird-send` | 6 | Thunderbird 156.0.1 | 48 | 16 (2.4) | 8.96 — disagrees: the second send pass (stated) |
| `video-call` | `webrtc` | 6 | Google Chrome 153.0.8010.52 | 1 | 1 (0.1) | 0.37 — agrees |

The differences, each value's per-job mean ratio, untraced over traced, and its 95 % interval:

- `web-browser` (its renderers carried since D84): idle gpu/Chrome_ChildIOT run mean (ms) 0.863 (0.850–0.877); idle gpu/VizCompositorTh run mean (ms) 0.954 (0.929–0.978); idle gpu/VizCompositorTh wakes/s 0.977 (0.960–0.993); idle renderer/Compositor run mean (ms) 0.928 (0.917–0.938); op Chrome_IOThread run mean (ms) 0.861 (0.818–0.903); op Chrome_IOThread wakes/s 1.037 (1.014–1.060); op chrome run mean (ms) 0.963 (0.933–0.993); op gpu/Chrome_ChildIOT run mean (ms) 0.889 (0.859–0.920); op renderer/Chrome_ChildIOT run mean (ms) 0.856 (0.843–0.870); op renderer/Compositor run mean (ms) 0.942 (0.902–0.982). `utility/HangWatcher`, in the residual since D84, read 0.936 (0.911–0.962) on its run mean and 1.003 (1.002–1.003) on its wake rate.
- `code-editor`: idle gpu/Chrome_ChildIOT run mean (ms) 0.884 (0.836–0.932); idle renderer/Compositor run mean (ms) 0.948 (0.925–0.970); idle utility/libuv-worker run mean (ms) 0.716 (0.639–0.792).
- `image-editor`: op gimp run mean (ms) 0.981 (0.970–0.992); op gimp wakes/s 1.021 (1.007–1.034); op script-fu wakes/s 0.972 (0.964–0.979).
- `video-editor`: driven QXcbEventQueue run mean (ms) 0.861 (0.815–0.907); op operation duration mean (ms) 0.988 (0.978–0.997).
- `audio-player`: play CPU share 0.860 (0.834–0.886).
- `video-player`: play CPU share 0.976 (0.964–0.988).
- `office-writer`: driven per-input run (ms) 0.984 (0.969–0.998); idle soffice.bin wakes/s 1.003 (1.001–1.005).
- `mail-client`: driven per-input run (ms) 0.895 (0.853–0.937); idle IPDL Background run mean (ms) 0.883 (0.824–0.941); idle Timer run mean (ms) 0.854 (0.769–0.939); idle WebExtensions/IPC I/O Child run mean (ms) 0.875 (0.819–0.930); idle WebExtensions/IPC I/O Child wakes/s 1.003 (1.003–1.003); idle WebExtensions/JS Watchdog wakes/s 1.003 (1.003–1.003); idle WebExtensions/Timer run mean (ms) 0.812 (0.656–0.969); idle glean.dispatche run mean (ms) 0.791 (0.721–0.861); idle residual run mean (ms) 0.932 (0.882–0.982); op Compositor run mean (ms) 0.817 (0.782–0.852); op Renderer run mean (ms) 0.970 (0.944–0.995); op Socket Thread run mean (ms) 0.825 (0.668–0.981); op Softwar~cThread run mean (ms) 0.745 (0.725–0.766); op Timer run mean (ms) 0.814 (0.757–0.871); op WRRende~ckend#0 run mean (ms) 0.911 (0.828–0.994); op glean.dispatche run mean (ms) 0.738 (0.689–0.786).
- `video-call`: play CPU share 0.952 (0.934–0.971).

Full tables: `task-9.5-interactive-typing/campaign/results-control.md`, `campaign/results-control/control.json`.

## 9.6 — three archetypes, one campaign

Repeats 4, 5, 7, 8 and 9–18 on the AMD EPYC 7763 (14 repeats; repeats 1, 2, 3, 6 gated). 28 jobs: 14 landed, 12 stopped by the machine gate, 2 cancelled (repeat 19, launched before the campaign ended, measured nothing). Every value is an across-repeat mean, each table by its mean as it carries it, count-weighted over the repeats (D26; 9.5 D78). Two conditions changed mid-campaign: `clamscan` reads a fixed signature database from repeat 9 (D27) and `python3` starts warm from repeat 11 (D28), so those two pool fewer repeats.

| archetype | program | headline | repeats | mean | spread (cv) | 95 % half-width | stopped by |
|---|---|---|---|---|---|---|---|
| `build-orchestrator` | `make` | dispatch run, warm `-j8` | 14 | 690.8 µs | 1.6 % | ±0.94 % | the rule |
| `compiler-child` | `cc1` | step CPU of the object job, warm `-j8` | 14 | 439.1 ms | 1.4 % | ±0.78 % | the rule |
| `cpu-batch` | `clamscan` | runs between voluntary blocks | 10 | 8.893 ms | 2.1 % | ±1.47 % | the rule |
| `cpu-batch` | `ffmpeg` | runs between voluntary blocks | 14 | 1.520 ms | 0.9 % | ±0.53 % | the rule |
| `cpu-batch` | `HandBrakeCLI` | runs between voluntary blocks | 14 | 1.087 ms | 0.8 % | ±0.47 % | the rule |
| `cpu-batch` | `python3` | runs between voluntary blocks | 8 | 1.595 s | 13.4 % | ±11.23 % | carried (D29) |
| `cpu-batch` | `tracker-miner-fs-3` | runs between voluntary blocks | 14 | 406.4 µs | 1.5 % | ±0.84 % | the rule |

The rule holds over 29 of the 33 values. Four are carried with their half-widths under the rule's exception for a value whose spread follows the machine (D29), all of them `cpu-batch` blocks on the runner's disk: `clamscan` block per run 218.1 µs ±9.5 % over 10 repeats (182–274), `python3` block per run 223.2 µs ±14.5 % over 8 (170–286) and its runs between blocks above, `tracker-miner-fs-3` block per run 17.6 µs ±15.1 % over 14 (13.3–30.4).

Also within the rule: the object job's other 10 per-step CPU tables (±0.63–2.00 %), CPU per process of the six roles, reported (±0.62–1.40 %), each bound program's share of CPU past the boot slice (±0.02–1.4 %), and the encoders' block means, which sit inside the trace's 1 µs floor (`ffmpeg` 0.35 µs, `HandBrakeCLI` 8.90 µs).

Full tables: `task-9.6-compile/campaign/results.md`, `campaign/results/pooled.json`.

## 9.7 — `file-backup`, `file-archiver` and `game-download`

Repeats 1–31 on the AMD EPYC 7763, repeat 3 left out of the pool: it landed, but its 10 GB set fetched as a 12,108 B file in place of the 3.70 GB archive (`set.archive_pin` mismatch, extract rc 2, 0 files), so its phases ran on an empty tree and the validity step fails it (the loop, step 4). 55 jobs: 31 landed, 24 stopped by the machine gate on another model (EPYC 9V74 8, EPYC 9V45 7, Xeon Platinum 8573C 7, Xeon 6973P-C 2). The rule is read over the other 30 repeats, and holds on both of `file-backup`'s values.

Each archetype carries two tables (D29): the program's runs between voluntary blocks, pooled over its threads, and the block after each run — the program's off-CPU time, zero when another of its threads runs on — each tested by its mean as it carries it, count-weighted over the repeats (9.5 D78).

| archetype | program | value | repeats | mean | spread (cv) | 95 % half-width | stopped by |
|---|---|---|---|---|---|---|---|
| `file-backup` | `borg` | run between voluntary blocks, warm first backup | 30 | 15.028 ms | 10.2 % | ±3.82 % | the rule |
| `file-backup` | `borg` | block per run, warm first backup | 30 | 3.091 ms | 12.6 % | ±4.71 % | the rule |
| `file-archiver` | `7z` | run between voluntary blocks, warm eight-thread run | 6 | 4.187 ms | 2.1 % | ±2.18 % | the rule |
| `file-archiver` | `7z` | block per run, warm eight-thread run | 6 | 0.16 µs | 38.6 % | ±0.06 µs | the rule (1 µs floor) |
| `game-download` | `steamcmd` | run between voluntary blocks, shaped fresh install | 30 | 162.7 µs | 5.9 % | ±2.21 % | the rule |
| `game-download` | `steamcmd` | block per run, shaped fresh install | 30 | 9.31 µs | 25.9 % | ±0.90 µs (±9.67 %) | the rule (1 µs floor) |

The per-wake tables of the first list are reported beside them: `borg` wait per wake 3.091 ms ±4.71 %, disk wait 3.119 ms ±4.68 %; `7z` wait per wake 32.235 ms ±2.41 %; `steamcmd` network wait 220.6 µs ±4.18 %, bytes per wake 3,937 B ±3.56 %, run per wake 162.7 µs.

`file-archiver`'s first batch of six repeats holds the rule, every repeat valid: 14 jobs, 6 landed, 8 stopped by the machine gate on another model (EPYC 9V74 3, EPYC 9V45 2, Xeon 6973P-C 2, Xeon Platinum 8370C 1). Its D15 check, the single-thread run against the eight-thread run, is reported by its CPU per byte (0.91–0.96 of the eight-thread run in every repeat); the check's per-wake parts split into two modes of the same thread, 906–941 wakes at a 0.361–0.385 s median gap in repeats 1, 2 and 6 against 1,246–1,575 wakes at 0.382–0.742 ms in repeats 3, 4 and 5, and both are stated in the archetype's notes.

`game-download`'s repeats 1–34 ran in runs #47–#98 under the `fq_codel` leaf (D25): repeats 6–12 and 14–22 as batches, then one at a time (D26). Four are left out: 21 ran unshaped — its runner had no accelerated-networking VF and 490 B of its 10.5 GB download went through the shaper (D27); 23 was wrongly launched on the pool that still held 21 (D27); 32's untraced and unshaped phases did not complete, SteamCMD reporting FAILED (No Connection) (D32); 33's unshaped phase's `perf.data` is truncated, its timehist report exiting 242 (D33). 76 jobs: 34 landed, 35 stopped by the machine gate on another model (Xeon Platinum 8573C 13, EPYC 9V74 13, EPYC 9V45 5, Xeon 6973P-C 4) and 7 stopped on the AMD EPYC 7763 by the network gate added after repeat 21 — runners with no accelerated-networking VF, where the shaper cannot sit (D27). The rule is read over the other 30 repeats (1–20, 22, 24–31, 34) and holds on both carried tables, every repeat valid. The repeats split by the Steam site the runner drew — 14 west, 13 east, 3 central — and the region holds 64 % of the variance of network wait and 45 % of the block per run. Its D15 check, read against its own interval since D36, resolves the tracing's cost: without `perf trace` the program spends 0.975 of the CPU (0.970–0.981, 29 of 30 repeats below 1) and 0.991 of the time (0.988–0.995), stated in the archetype's notes.

Full tables: `task-9.7-background-io/campaign/results-borg.md`, `campaign/results-7z.md` and `campaign/results-steamcmd.md`, `campaign/results/borg-pooled.json`, `results/7z-pooled.json` and `results/steamcmd-pooled.json`; every job's model: `campaign/machine-draws.md`; the shaping rate's source, D11's Valve snapshot with `rate.py`: release `meas-ci-background-2026-09-19`, asset `steam-download-stats-09-19-2026-04.zip` (D41).

## 9.8 — four archetypes, one campaign

Every repeat on the AMD EPYC 7763, kernel `6.17.0-1022-azure` in all of them, none excluded or superseded; the renderer entries on Google Chrome 152.0.7977.82 in every repeat but the hidden renderer's 12–16, added at D31, which ran 153.0.8010.52 — Google's repository serving only its current build, the census stated with the values (9.5 D69) — 12 renderers measured of 16 observed (hidden) and of 13–14 (visible). Each entry reads one phase (method §10): the hidden renderer `steady`, the visible renderer `steady-notimer` (D16), the chat client `idle`, the Steam client `shown`. The renderer entries' values are per renderer, the renderers pooled as samples (D14). `values` counts what the rule covers; `widest` is the largest half-width among the values that pass it.

| archetype | subject | repeats | values | pass | widest | stopped by | jobs (gated) | recorded input covered |
|---|---|---|---|---|---|---|---|---|
| `renderer-hidden` | `chrome-hidden` | 19 (1–9, 11–16, and 10 four times) | 21 | 7 | `HangWatcher` run mean ±4.79 % | the rule | 34 (15) | none |
| `renderer-visible` | `chrome-visible` | 11 (1–11) | 15 | 4 | `chrome` wake rate ±3.76 % | the rule | 18 (7) | none |
| `chat-client` | `element` | 18 (1–16, and 17 twice) | 18 | 18 | residual run mean ±4.35 % | the rule | 32 (14) | none |
| `game-client` | `steam` | 12 (1–12) | 33 | 29 (28 before D33) | `CJobMgr::m_Work` run mean ±5.69 % (the 1 µs floor) | the rule | 21 (9) | none |

Rates are one renderer's, the mean over every renderer measured from exact counts; gaps are over each component's merged wake times, wrapped round the phase — the renderers laid end to end for a renderer entry — so a gap mean is the span over the wakes (9.5 D71; this slice's D26).

The values outside the tolerance, each carried over its repeats with its half-width and range. Run means whose spread is the machine (D17; the Steam client's by D18):

- hidden renderer: none since D31 — `HangWatcher`'s run mean, carried here at 0.0274 ms ±5.3 % over 14 repeats, holds the rule at 19, 0.0267 ms ±4.79 % (0.024–0.033). The two Chrome builds agree on every carried value within 0.09–1.27 standard deviations of the 152 repeats' spread, every run mean lower under 153 by 0.22–1.27 of them.
- visible renderer: `HangWatcher` run mean 0.0320 ms ±5.9 % (0.029–0.037); `chrome` run mean 0.1493 ms ±6.1 % (0.133–0.181).
- Steam client: `steam` run mean 0.0554 ms ±10.1 % (0.044–0.068); `IPC:CSteamEngin` 0.0574 ms ±8.8 % (0.047–0.068); `VizCompositorTh` 0.0818 ms ±5.6 % (0.066–0.089); `steamwebhelper` 0.0695 ms ±5.3 % (0.063–0.082), its wake rate and gap mean within the tolerance since D26 — its and `ThreadPoolForeg`'s gap means, carried between sessions under D23 until then at ±10.2 % and ±9.0 %, read ±0.18 % and ±4.19 % over merged wake times. `CJobMgr::m_Work`'s run mean, 0.0176 ms ±5.7 % (0.015–0.020), holds within the 1 µs floor since 9.5 D78 (±6.2 % by its per-repeat means).

Components whose spread lies between sessions, their three values together (D21; the hidden renderer's `Chrome_ChildIOT` by D24, the four quiet threads by D26, all under 9.5 D57; the Steam client's two, by D23, until D26; the Steam client's `CHTTPClientThre`, its run mean alone, by D30, until D33):

- hidden renderer, `Chrome_ChildIOT`: 0.0070 wakes/s ±18.5 % (0.0019–0.0106); gap mean 142.4 s ±18.5 % (94.7–514.3 s); run mean 0.0290 ms ±6.9 % (0.024–0.056).
- hidden renderer, `Compositor`, `PerfettoTrace` and `ThreadPoolServi`, which wake together: 0.0065 wakes/s ±18.9 % (0.0017–0.0100); gap mean 154.1 s ±18.9 % (100.0–600.0 s); run means 0.0202 ms ±5.1 % and 0.0192 ms ±6.3 %, `ThreadPoolServi`'s 0.0198 ms within the tolerance (±4.35 %); within one run ±10.8 % against ±64.2 % across the repeats.
- visible renderer, `Chrome_ChildIOT`: 0.0060 wakes/s ±26.4 % (0.0022–0.0094); gap mean 165.3 s ±26.4 % (105.9–450.0 s); run mean 0.0386 ms ±10.8 % (0.030–0.053).
- visible renderer, `PerfettoTrace`: 0.0054 wakes/s ±26.2 % (0.0017–0.0085); gap mean 186.4 s ±26.2 % (118.0–600.0 s); run mean 0.0241 ms ±5.1 % (0.022–0.028); within one run ±4.0 % against ±63.4 % across.
- Steam client, `CHTTPClientThre`, until D33 (2026-09-28): run mean 0.0313 ms ±46.2 % in two modes, 8 of the 12 repeats at 0.0137–0.0170 ms and 4 (repeats 4, 5, 6, 12) at 0.0572–0.0639 ms, against ±0.2 % within one run (0.01454–0.01459 ms); its per-repeat run mean moves with none of the other threads' (correlations −0.12 to +0.28, theirs with each other a median +0.76); its wake rate, 8.05 a second, and gap mean within the tolerance (±0.41 %); 2.7 % of the shown phase's wakes, 1.7 % of its CPU. The pooled table mixes the two modes wake by wake. Read per repeat in time windows (D33), the upper "mode" is one burst: 12–18 runs of 2.0–50.2 ms within 1.8–2.8 s, 201–228 ms of CPU, in each of repeats 4, 5, 6 and 12, 1.5–594.9 s into the phase, every repeat at 0.014–0.017 ms outside it; the minimised phase measured beside it caught the same burst in 9 of the 12 repeats. Since D33 the runs of 1 ms or more leave the component as a rare event within a run (9.5 D64) — 62 runs over 7,200 s, 0.0086 a second, carried as the entry's `heavy_events` — and the component, read without them, holds the rule: run mean 0.0162 ms ±3.7 %, wake rate 8.038 a second and gap mean ±0.3 %.

Sparse components, waking a few times per renderer per phase, their three values together with their half-widths and their count (D27; carried between sessions from D21 to D26):

- hidden renderer, residual (`MemoryInfra`): 0.0033 wakes/s ±14.8 % (0.0021–0.0057); gap mean 302.7 s ±14.8 % (175.6–480.0 s); run mean 0.1883 ms ±6.0 % (0.152–0.265); 1.2–3.4 wakes per renderer per 600 s phase. A 600 s window of the probe catches 0–2 of its wakes — ±134.2 % within one run against ±54.6 % across the repeats — the count's own spread, which the within-run test cannot place.
- visible renderer, residual (`MemoryInfra`, `Compositor`, `ThreadPoolForeg`, `ThreadPoolServi`): 0.0068 wakes/s ±10.9 % (0.0060–0.0092); gap mean 146.9 s ±10.9 % (109.1–167.4 s); run mean 0.1459 ms ±12.9 % (0.116–0.200); 3.6–5.5 wakes per renderer per 600 s phase. The probe does not reproduce its comms, 0.0009 against 0.0068 wakes/s (±181.3 % within one run against ±23.5 % across), so the within-run test does not apply.

- Repeat indices that landed more than once: the retry driver relaunched the hidden renderer's repeat 10 in runs #33, #34, #36 and #37 and the chat client's repeat 17 in #49 and #50, and every launch landed on the AMD EPYC 7763 with the gate open. Every landing is pooled, keyed `<index>@<run id>` (D24).
- No gated window was left once the rule held: every index 1…k of each entry landed.

- **When each exception was decided** (D28, 2026-09-25; git and the runs' launch times, UTC). Every exception followed a value seen failing. D17, the run means of the renderers and the chat client as machine speed, was committed 2026-09-21 09:44 on the first batch of five, before the hidden renderer's windows 6–11 and the visible's 7–11 were launched (runs #31–#40, 09:48–10:15); D18, the Steam client's run means, at 11:04, before its windows 6–12 (#43–#45, 11:13–11:18); D21, the renderers' quiet threads, at 11:48, after the renderers' last launch; D23, the Steam client's two components, 22:51, and D24, every landing pooled, 2026-09-22 02:46, after the campaign's last run (#50, 12:01); D30, `CHTTPClientThre`'s run mean between sessions in place of D18, 2026-09-26, on the review of 9.5–9.9. The workflow's class-wide wording for the machine-speed exception landed 2026-09-22 09:53, after the fold-in (04:21). Projected repeats to pass, from the pool as it stands: hidden `HangWatcher` run mean 16 at 14 landed, then 18 at 16 and 19 at 18 — held at 19 (D31, 2026-09-26: D17 no longer applied to it); visible `HangWatcher` 15 and `chrome` 16 (11); Steam `steamwebhelper` 14, `VizCompositorTh` 15, `IPC:CSteamEngin` 32, `steam` 42, `CHTTPClientThre` none (12; within the rule since D33), `CJobMgr::m_Work` within the rule since 9.5 D78. The machine-speed ground — run times moving together across every thread of a repeat while wake rates hold — is a mechanism the record shows independently of the pass, and the exceptions stand on it; whether their half-widths are re-measured at a count fixed in advance is 9.14's, after its sensitivity check. Qualification on the within-run test: the probe's 600 s windows every 60 s overlap and are correlated, so a within-run figure understates that spread against the independent repeats it is compared with.

Full tables: `task-9.8-browser-comms/campaign/results/results.md`, `campaign/results/pooled.json`; every job's model: `campaign/machine-draws.md`.

### The untraced control (D32), finished 2026-09-27

Each carried phase run twice in every job, traced under `perf sched record` and untraced, each thread's CPU time and switches read from `/proc` at both edges of each run; each value's per-job ratios, untraced over traced, read by their 95 % interval (the 9.5 untraced-control spec). Six jobs per subject, three in each order, every one on the AMD EPYC 7763; the carried values unchanged, each entry's notes carrying its reading. Runs `meas-ci:desktop` #60–#69; `chat-client`'s windows 1 and 2 landed twice and their later copies are left out (9.5 D66).

| archetype | subject | jobs | build | intervals | differences (chance) | traced against carried, largest \|z\| |
|---|---|---|---|---|---|---|
| `renderer-hidden` | `chrome-hidden` | 6 | Google Chrome 153.0.8010.52 | 14 | 2 (0.7) | 5.12 — agrees under the carried selection, read by hand |
| `renderer-visible` | `chrome-visible` | 6 | Google Chrome 153.0.8010.52 | 10 | 0 (0.5) | 1.98 — agrees |
| `chat-client` | `element` | 6 | Element 1.12.29 | 12 | 4 (0.6) | 3.35 — disagrees: the second idle run (stated, with the build) |
| `game-client` | `steam` | 6 | Steam client build 1788652215 | 22 | 10 (1.1) | 1.27 — agrees |

The differences, each value's per-job mean ratio, untraced over traced, and its 95 % interval:

- `renderer-hidden`: steady HangWatcher run mean (ms) 0.974 (0.950–0.998); steady HangWatcher wakes/s 1.003 (1.002–1.003).
- `chat-client`: idle Chrome_ChildIOT run mean (ms) 0.931 (0.910–0.952); idle Chrome_IOThread run mean (ms) 0.843 (0.809–0.877); idle ThreadPoolForeg run mean (ms) 0.909 (0.861–0.958); idle ThreadPoolServi run mean (ms) 0.880 (0.807–0.952).
- `game-client`: shown CJobMgr::m_Work run mean (ms) 0.857 (0.778–0.935); shown Chrome_ChildIOT run mean (ms) 0.871 (0.844–0.899); shown Chrome_ChildIOT wakes/s 0.996 (0.993–1.000); shown Compositor run mean (ms) 0.952 (0.915–0.988); shown Compositor wakes/s 0.979 (0.973–0.985); shown ThreadPoolForeg run mean (ms) 0.816 (0.746–0.886); shown ThreadPoolForeg wakes/s 1.076 (1.013–1.139); shown VizCompositorTh run mean (ms) 0.972 (0.947–0.998); shown VizCompositorTh wakes/s 0.988 (0.977–0.998); shown steamwebhelper wakes/s 0.996 (0.993–0.999).

Full tables: `task-9.8-browser-comms/campaign/results-control.md`, `campaign/results-control/control.json`.

## 9.9 — four entries, one campaign

One subject, the Ubuntu 24.04 desktop session, carries the four entries that replace `system-daemon` — `compositor-shell` (GNOME Shell), `audio-server` (the PipeWire stack), `service-manager` (`systemd`) and `message-bus` (`dbus-daemon`), folded in at D26, again, re-analysed, at D30, and again with sysstat's collector kept at D47 and D48 (2026-10-01) — so every job observes all four and the repeats and jobs are shared. 24 repeats — 47–49, 51, 58, 60–63, 68, 69, 71–77, 79, 83, 85–88 — every one on the AMD EPYC 7763, kernel `6.17.0-1022-azure` in all of them, none excluded, one set of package versions in every repeat (`gnome-shell` 46.0-0ubuntu6~24.04.14, Mutter's `libmutter-14-0` 46.2-1ubuntu0.24.04.16 read from each repeat's install log (D45), `pipewire` and `pipewire-pulse` 1.0.5-1ubuntu3.3, `wireplumber` 0.4.17-1ubuntu4.1, `systemd` 255.4-1ubuntu8.17, `dbus-daemon` 1.14.10-4ubuntu4.1). Each entry reads the `steady` phase, 1800 s (D22): the session idle past `idle-delay`, the shield up and locked, the monitor blanked (method §3). No display server in any repeat's census. Every wake is read by its cause (D27): wakes owed to a package Ubuntu 24.04's desktop manifest does not hold, or to the harness, and desktop jobs bound to a clock time leave the components and are stated. `values` counts what the rule covers; `widest` is the largest half-width among those that pass.

| entry | components | repeats | values | pass | widest | stopped by | jobs (gated) | recorded input covered |
|---|---|---|---|---|---|---|---|---|
| `compositor-shell` | `JS Helper`, `gmain`, `gnome-shell` | 24 | 9 | 9 | `gnome-shell` run mean ±2.8 % | the rule | 42 (18), shared | none |
| `audio-server` | `wireplumber/gmain` | 24 | 3 | 3 | `wireplumber/gmain` wake rate ±4.5 % | the rule | shared | none |
| `service-manager` | `pid1/systemd` | 24 | 3 | 2 | carried (D29, D48) | the rule, with D29 and D48 | shared | none |
| `message-bus` | `system-bus/dbus-daemon` | 24 | 3 | 0 | carried (D48) | the rule, with D48 | shared | none |

| component | wakes/s | gap mean | run mean | half-widths (rate · gap · run) |
|---|---|---|---|---|
| `gnome-shell/JS Helper` | 0.3025 | 3.31 s | 0.0137 ms | ±0.7 · ±0.7 · ±1.0 % |
| `gnome-shell/gmain` | 0.2498 | 4.00 s | 0.0497 ms | ±0.1 · ±0.1 · ±2.2 % |
| `gnome-shell/gnome-shell` | 0.0347 | 28.78 s | 5.6996 ms | ±1.5 · ±1.5 · ±2.8 % |
| `wireplumber/gmain` | 0.0093 | 107.46 s | 0.0350 ms | ±4.5 · ±4.5 · ±2.8 % |
| `pid1/systemd` | 0.0702 | 14.24 s | 0.1710 ms | ±1.9 · ±1.9 · ±7.8 %, run mean carried (D29, D48) |
| `system-bus/dbus-daemon` | 0.0140 | 71.64 s | 0.1210 ms | ±11.1 · ±11.1 · ±10.7 %, carried (D48); 16–38 wakes a phase |

Gap means are over each component's merged wake times, wrapped round the phase (9.5 D71; this slice's D31), so a gap mean is the phase over the wakes.

- Causes that left (D27), per phase: `php-fpm` (PHP 8.3's FastCGI service, which the runner image ships) 180–188 wakes of pid 1 and 185–225 of the system bus through pid 1; the workflow's "wait for the run" loop 355–362 of WirePlumber's worker, each with the worker's own timer 100.2 ms later; PHP's session cleanup and `podman` a few each. Sysstat's jobs: D32 (2026-09-25) put them outside on the ground that a stock install leaves sysstat's timers disabled; D47 (2026-10-01) reverted it — the desktop image is built with no systemd running, so the postinst's disable step never runs and its default install layer holds the timers enabled (`sysstat-debian`) — so the collector, every 10 minutes, is a desktop job again, 277 of `audio-server`'s 402 kept wakes, 361 of `message-bus`'s 609 and 68 of `service-manager`'s 3,238 before D37. Desktop jobs bound to a clock time (`logrotate`, `man-db`, `fstrim`, `motd-news`, `anacron`, sysstat's summary and 23:59 sample) are stated as events. Before D27 the three entries read 0.179, 0.137 and 0.213 wakes/s; from D32 to D47, 0.0687, 0.0056 and 0.0029 (with D37); since D47, 0.0702, 0.0140 and 0.0093. `systemd-networkd` (D37, 2026-09-26) is outside on the same ground: Ubuntu 24.04's `systemd` enables it on no install, the desktop image hands every device to NetworkManager and netplan starts networkd only for networkd configuration, so a stock desktop leaves it inactive where the runner image runs it — 5–15 of pid 1's wakes a phase and 0–6 of the bus's; before D37, `service-manager` 0.0734 and `message-bus` 0.0057 wakes/s. D47 completed that ground: the image's `90-systemd.preset` enables networkd, but PID 1 applies presets only on a first boot, which neither an empty `/etc/machine-id` nor an installed desktop is — the installer writes the live session's machine ID into the target (`systemd-ubuntu`, `ubuntu-desktop-bootstrap`).
- Carried between sessions (9.5 D57 as 9.8 D21 extended it; D28, D29, D48): `pid1/systemd`'s run mean, 114–139 wakes a phase, ±10.7–18.4 % within one run against ±30.0 % across the repeats; `system-bus/dbus-daemon`'s three values, 16–38 wakes a phase in every repeat, its wake rate ±23.4–28.4 % within one run against ±43.8 % across — each its entry's whole activity once the outside causes are out. Sparse components (D33) from D32 to D47: `wireplumber/gmain`, 2–12 wakes a phase, and the bus, 0–30 and none in six repeats; with the collector kept, the worker holds the rule and the bus is carried between sessions (D48).
- Coverage (method §5, the 95 % cut): GNOME Shell 99.97 % of 0.587 wakes/s, every other entry 100 % of its one component; no residual. `pipewire` and `pipewire-pulse` recorded no wake in the phase of any repeat. The session bus woke 26–29 times in each of repeats 47, 48, 49 and 51 and in no other — all at 00:00 UTC, from Evolution's calendar and alarm daemons, inside the cron session's window — and the user manager 8 times in the same four; D23 and D27 took every one out, so the entries carry none. GNOME Shell's `gnome-s:disk$0` woke only in those four repeats, 0.0002 wakes/s over the pool, reported as sporadic, not carried.
- WirePlumber's midnight split (D38): in repeats 47, 48, 49 and 51, which crossed midnight UTC and met the cron session, `wireplumber/gmain` woke 0.0110 times a second against 0.0090 in the other 20 (D47, the collector kept; from D32 to D47, 0.0057 against 0.0023). The extra wakes are pairs of its own timer 100 ms apart, 496–1205 s into the phase, 14 of the 15 starting within 0.2 s of one of the runner's `dockerd` bursts; the trace names no waker, so no rule of D23 or D27 moves them and the scope states the split.
- A cron job's session (D23): repeats 47, 48, 49 and 51, the first batch, met the `sphinxsearch` indexer's at 00:00 UTC, 317–365 s into the phase; the rows inside its window left each component — `service-manager` 201, `message-bus` 245, `audio-server` 37, `compositor-shell` 12 — and are stated per repeat in `pooled.json` (`cron_event`). No other repeat met one.
- Foreign work on the measured CPU: 18–43 user-space schedule-ins per repeat outside the four entries, 0.00097–0.0022 % of the phase against the 2 × 10⁻⁴ bound (D22); none by a pinned unit's other process. Kernel threads 11,608–15,472 schedule-ins per repeat, reported and not gated (D14).
- Batches: the first batch of five in run #16 (repeat 50 gated); relaunches and added repeats in #17–#21; then 24 jobs to the pool's projection in #22 (D25), 15 of them landing. Every landing is pooled.

- **When the exception was decided and where the campaign stopped** (D34, 2026-09-25; UTC). The campaign's last run, #22, was launched 2026-09-24 02:47; it was closed at 24 repeats at 05:55 (`55944a5`, "the rule holds, widest 3.7 %") on the values it carried then; D27's re-analysis by cause (10:56, `60c50ba`) moved three components off the rule and D29 carried them, so the exception followed values seen failing after the campaign had stopped, and no repeat was added. The projections then: 58 for pid 1's run mean, 96–138 for the system bus; under D47's causes, 55 for pid 1's run mean and 102–108 for the bus's three values, both carried between sessions by D48 (2026-10-01), on the pool the campaign closed, no repeat added. Whether they are re-measured at a count fixed in advance is 9.14's, after its sensitivity check.

Full tables: `task-9.9-daemons-session/campaign/results/results.md`, `campaign/results/pooled.json`; the placement of D28, re-read under D32's causes at D35 and under D47's at D48, `campaign/results/within-run.json`; every job's model: `campaign/machine-draws.md`.

### The untraced control (D40), finished 2026-09-27

Each carried phase run twice in every job, traced under `perf sched record` and untraced, each thread's CPU time and switches read from `/proc` at both edges of each run; each value's per-job ratios, untraced over traced, read by their 95 % interval (the 9.5 untraced-control spec). Six jobs per subject, three in each order, every one on the AMD EPYC 7763; the carried values unchanged, each entry's notes carrying its reading. Runs `meas-ci:session` #25–#28. The check against the carried pool reads each entry's own values (9.9 D41).

| archetype | subject | jobs | build | intervals | differences (chance) | traced against carried, largest \|z\| |
|---|---|---|---|---|---|---|
| `message-bus` | `session` | 6 | dbus-daemon 1.14.10-4ubuntu4.1 | 2 | 0 (0.1) | 1.15 — agrees (0.68 before D47) |
| `compositor-shell` | `session` | 6 | gnome-shell 46.0-0ubuntu6~24.04.15 | 6 | 1 (0.3) | 0.74 — agrees |
| `audio-server` | `session` | 6 | pipewire 1.0.5-1ubuntu3.3, wireplumber 0.4.17-1ubuntu4.1 | 2 | 0 (0.1) | 0.91 — agrees (0.6 before D47) |
| `service-manager` | `session` | 6 | systemd 255.4-1ubuntu8.17 | 2 | 0 (0.1) | 1.29 — agrees (1.19 before D47) |

The differences, each value's per-job mean ratio, untraced over traced, and its 95 % interval:

- `compositor-shell`: gnome-shell gnome-shell/JS Helper run mean (ms) 0.864 (0.841–0.886).

Full tables: `task-9.9-daemons-session/campaign/results-control.md`, `campaign/results-control/control.json`.

## 9.10 — `package-upgrade`

Repeats 1–9 on the AMD EPYC 7763, every repeat valid (the method's checks: the layer built with no package missing or extra, the four packages downloaded and installed 2.39-0ubuntu8.7 → 8.8 with the same change set, "All upgrades installed"). 15 jobs: 9 landed, 6 stopped by the machine gate (EPYC 9V45 2, EPYC 9V74 2, Xeon Platinum 8370C 1, Xeon Platinum 8573C 1; `task-9.10-scenarios-timelines/campaign/upgrade/machine-draws.md`). The first batch was repeats 1–5, the rule's minimum; at five the run mean (±6.31 %) and the CPU total (±7.72 %) failed and the pool projected nine, so repeats 6–9 were added as a batch (9.7 D26); at nine the rule holds on all three values.

The entry carries `cpu-batch`'s batch loop over the whole process tree (9.10 D39) and its CPU total, the job's measured whole (D17):

| archetype | program | value | repeats | mean | spread (cv) | 95 % half-width | stopped by |
|---|---|---|---|---|---|---|---|
| `package-upgrade` | `unattended-upgrade`'s tree | run between voluntary blocks | 9 | 1.798 ms | 4.0 % | ±3.10 % | the rule |
| `package-upgrade` | `unattended-upgrade`'s tree | block per run | 9 | 8.90 µs | 7.8 % | ±0.53 µs (±5.97 %) | the rule (1 µs floor) |
| `package-upgrade` | `unattended-upgrade`'s tree | CPU total | 9 | 26.385 s | 4.9 % | ±3.78 % | the rule |

Reported beside them: 916 processes in every repeat; CPU over the stage's wall time 0.990–0.994; `locale-gen`'s 18 `localedef` runs 72.8–76.5 % of the CPU; taskstats over perf 0.980–0.982. The CPU total ranges 25.25–29.16 s: repeats 4, 5 and 9 ran 6–14 % above the mean of the other six (25.61 s), `unattended-upgrade`'s own Python 21–50 % above them (repeats 4 and 5), in identical work. Pooled in `task-9.10-scenarios-timelines/campaign/upgrade/results/` (`pooled.json`, `results.md`).

## 9.10 — `module-build-orchestrator` and `module-compiler-child`

Repeats 1–23 on the AMD EPYC 7763, 26 landings, every one valid (the method's checks: the layer built with no package missing or extra; the state on the kernel `7.0.0-31-generic` with `nvidia/595.91.07` built for it; the stage installing the kernel `7.0.0-34` and `xdg-desktop-portal` with the same change set, "All upgrades installed"; `nvidia/595.91.07` installed for `7.0.0-34-generic`, its five modules present). One push started runs #111 and #112 together, so repeats 7, 10 and 11 landed twice; every landing is pooled, keyed `<index>@<run id>` (9.8 D24; 9.10 D58). 37 jobs: 26 landed, 11 stopped by the machine gate (EPYC 9V74 6, Xeon Platinum 8573C 3, EPYC 9V45 1, Xeon 6973P-C 1; `task-9.10-scenarios-timelines/campaign/dkms/machine-draws.md`). The first batch was repeats 1–5, the rule's minimum; at five 37 of the 60 values failed and the pool projected 23, so repeats 6–23 were added as a batch (9.7 D26). Over the 26 landings the rule holds on 59 values; the serial tail's block per run is carried with its half-width, its spread the machine's (9.6 D29; 9.10 D58).

The entries carry the build's spawn form (9.10 D52–D57): four job kinds over their process trees — 200 object jobs, 1,125 kbuild probes, 145 and 87 `conftest` tests without and with `as`, the same counts in every landing — each member's CPU per structural step (56 tables), make's dispatch run, the serial tail's batch loop, and the CPU total they carry:

| archetype | value | landings | mean | spread (cv) | 95 % half-width | stopped by |
|---|---|---|---|---|---|---|
| `module-compiler-child` | 56 per-(kind, member, step) CPU tables | 26 | `object` `cc1` 721.9 ms, `conftest` `cc1` 171.7 and 240.0 ms, kbuild probe `cc1` 4.55 ms | – | ±0.67 % to ±4.13 % | the rule |
| `module-build-orchestrator` | make's dispatch run | 26 | 754.3 µs | 1.8 % | ±0.72 % | the rule |
| `module-build-orchestrator` | the tail's run between voluntary blocks | 26 | 6.151 ms | 4.5 % | ±1.82 % | the rule |
| `module-build-orchestrator` | the tail's block per run | 26 | 44.4 µs | 20.7 % | ±8.35 % | carried, the machine's spread (9.10 D58) |
| both | CPU total carried (jobs, make, tail) | 26 | 224.627 s | 3.6 % | ±1.46 % | the rule |

Reported beside them: the build's hook run (`/etc/kernel/header_postinst.d/dkms` in every landing) 214.5–243.2 s of CPU over its span at 0.997; the carried share 0.9818–0.9825, the unmodelled remainder 3.89–4.32 s (helper and link jobs, the `dkms` script before the `make`, the kernel image's second hook run of 0.13–0.145 s); the tail 9.29–11.14 s. The job order differs between landings only by adjacent swaps. Pooled in `task-9.10-scenarios-timelines/campaign/dkms/results/` (`pooled.json`, `results.md`).

## 9.10 — `file-indexer`

Repeats 1–18 on the AMD EPYC 7763, 18 landings, every one valid (the method's checks: the layer built with no package missing or extra; Tracker at 3.7.1-1ubuntu0.1; HippoCamp's Bei tree whole, 875 files and 40,662,407,070 B, each checked by its SHA-256; no GStreamer registry and no database in the home before the phase; the cached fraction 0.0000 after the page cache was dropped; the initial sleep 14.91–15.73 s on the miner's status trace; the extractor's last status `Idle` after `Extracting metadata`; "Currently indexed: 875 files, 92 folders"). Each index landed once. 38 jobs: 18 landed, 20 stopped by the machine gate. Before them, a first batch run with the page cache as the download left it and a cold batch whose cached fraction went unrecorded were not pooled (9.10 D75; the method's §8).

The entry carries the batch-loop form over the miner's tree (9.10 D65, D70) — the miner, the three extractor runs and the GStreamer registry scan, five processes in every landing — with the initial sleep left out of the block table as the task's arrival (D71):

| archetype | value | landings | mean | spread (cv) | 95 % half-width | stopped by |
|---|---|---|---|---|---|---|
| `file-indexer` | run between voluntary blocks | 18 | 1.876 ms | 2.3 % | ±1.12 % | the rule |
| `file-indexer` | block per run | 18 | 227.0 µs | 7.2 % | ±3.58 % | the rule |
| `file-indexer` | CPU total | 18 | 39.435 s | 0.6 % | ±0.28 % | the rule |

Reported beside them: the job 58.3–60.3 s from the miner's first schedule-in to the extractor's end; the initial sleep's block 14.40–15.23 s; the extractor 37.47–38.35 s of CPU, the miner 1.53–1.62 s, the registry scan 93–106 ms; saturation 0.655–0.676 over the job, 0.891–0.919 from the miner's `Initializing`; the dominant thread (the extractor's `single`) 0.556–0.559 of the CPU; the share of CPU past the 10 ms boot slice 0.844–0.849. In every landing the extractor's 5 s per-file deadline ended `Book/TenYearsInJapan.pdf` and `Book/IslandOfBali.pdf`, each followed by the miner's 1 s grace and a new extractor (D72); Tracker recorded ten failures. Pooled in `task-9.10-scenarios-timelines/campaign/tracker/results/` (`pooled.json`, `results.md`).

## 9.10 — `cpu-batch`'s `python3`, PyTorch's basic MNIST example

Repeats 1–6 on the AMD EPYC 7763, 6 landings, every one valid (the method's checks: the layer built with no package missing and `python3-venv`'s four packages added; the example's three files each matching its SHA-256 at `acc295d`; `torch` 2.14.0+cpu and `torchvision` 0.29.0+cpu, one installed set; the dataset's files cached at 1.0000 after the warm start; the kernel's transparent huge pages `always`; 14 test passes; the checkpoint written, the same SHA-256 in every landing). Each repeat landed once. 8 jobs: 6 landed, 2 stopped by the machine gate.

The entry carries `cpu-batch`'s batch-loop form for the program `python3` (9.10 D85), one process with one thread, shown as `python`:

| archetype | value | landings | mean | spread (cv) | 95 % half-width | stopped by |
|---|---|---|---|---|---|---|
| `cpu-batch` (`python3`) | run between voluntary blocks | 6 | 69.49 s | 26.0 % | ±27.3 % | carried with its half-width, its spread `khugepaged`'s (D87) |
| `cpu-batch` (`python3`) | block per run | 6 | 311.5 µs | 10.3 % | ±10.8 % | carried with its half-width, its spread `khugepaged`'s (D87) |
| `cpu-batch` (`python3`) | CPU total | 6 | 1,389.885 s | 3.9 % | ±4.04 % | the rule |

Reported beside them: the job 1,294.0–1,455.9 s, saturation 0.9999; 11–24 voluntary blocks a landing, every one but the two sleeps at the start (99–110 µs) ended by `khugepaged` under the runner's `always` mode; 168k–249k huge pages fault-allocated and 133–145 collapsed in each phase. The check under the desktop kernel's `madvise` mode (D87, D88), five jobs, pooled apart: CPU total 1,589.654 s ±2.01 %, ×1.144 the campaign's (95 % Welch interval ×1.102–×1.185), no block but the two start sleeps. Pooled in `task-9.10-scenarios-timelines/campaign/mnist/results/` (`pooled.json`, `results.md`; the check's `madvise-pooled.json`, `madvise-results.md`).

## 9.10 — `video-transcoder`, HandBrakeCLI on CpsMark+'s transcode

Repeats 1–5 on the AMD EPYC 7763, 5 landings, every one valid. The method's checks:

- the layer built with no package missing and `handbrake-cli`'s 67 packages added;
- `handbrake-cli` 1.7.2+ds1-1build2 and `libx264-164` 2:0.164.3108+git31e19f9-1;
- Big Buck Bunny's 4K 30 fps clip and its zip each matching its SHA-256, the clip cached at 1.0000 after the warm start;
- the kernel's transparent huge pages `always`;
- HandBrake's default preset as run, `libx264` at fast and RF 22, the picture 1920 × 1080 at 1 : 1;
- the clip's 19,036 frames decoded with no error, and the same video track, 19,038 frames and 276,311,652 B, in every landing.

Each repeat landed once. 9 jobs: 5 landed, 4 stopped by the machine gate.

The entry is `video-transcoder`, a batch-loop entry of its own (9.10 D97, D98): one process, `HandBrakeCLI`, of 23 threads.

| archetype | value | landings | mean | spread (cv) | 95 % half-width | stopped by |
|---|---|---|---|---|---|---|
| `video-transcoder` | run between voluntary blocks | 5 | 4.002 ms | 1.4 % | ±1.8 % | the rule |
| `video-transcoder` | block per run | 5 | 0.605 µs | 29.1 % | ±36.1 % | the rule's 1 µs floor |
| `video-transcoder` | CPU total | 5 | 2,970.871 s | 2.1 % | ±2.6 % | the rule |

Reported beside them:

- **The job.** 2,865.0–3,025.5 s, saturation 0.99938–0.99947.
- **The threads.** The busiest holds 0.334–0.338 of the CPU, the next 0.205–0.208, the third 0.101–0.103.
- **The blocks.** 733k–746k runs a landing, about 2 in 100,000 followed by a block, 0.26–0.60 s of blocks a job; 2–12 uninterruptible waits a landing, 0–1 disk wait.

Before the campaign:

- **The probe of HandBrake's H.265 presets** (D93): 2.41–5.83 s of CPU per source second.
- **A dry run of D93's x265 settings,** superseded by D95: 2,483.81 s of CPU, 29 threads.

Pooled in `task-9.10-scenarios-timelines/campaign/handbrake/results/` (`pooled.json`, `results.md`).

## 9.10 — `cpu-batch`'s `kdenlive_render`, Kdenlive's export of the `video-editor` project

Repeats 1–30 on the AMD EPYC 7763, 30 landings, every one valid. The method's checks:

- the layer built with no package missing and the 427 packages `apt-get install kdenlive ffmpeg` added, one set across the landings;
- `kdenlive` 4:23.08.5-0ubuntu4, `melt` and `libmlt7` 7.22.0-1build6, `libavcodec60` 7:6.1.1-3ubuntu5, `libx264-164` 2:0.164.3108+git31e19f9-1 and `frei0r-plugins` 1.8.0-1build3;
- 9.5's clip, one SHA-256 across the landings, cached at 1.0000 with the render stack's libraries;
- the kernel's transparent huge pages `always`;
- the render dialog opened by its shortcut in every landing, `kdenlive_render delivery /usr/bin/melt-7 <playlist>`, the playlist's consumer Kdenlive 23.08.5's default profile (x264 `veryfast`, CRF 23);
- the same output in every landing: 600 H.264 frames at 1920 × 1080 and 938 AAC frames, 966,107 B, one SHA-256, one x264 options string.

Each repeat landed once. 56 jobs: 30 landed, 26 stopped by the machine gate.

The program is `cpu-batch`'s `kdenlive_render` (9.10 D105, D106): the tree of `kdenlive_render` and the `melt-7` it starts, pooled.

| archetype | value | landings | mean | spread (cv) | 95 % half-width | stopped by |
|---|---|---|---|---|---|---|
| `cpu-batch` (`kdenlive_render`) | run between voluntary blocks | 30 | 1.932 ms | 2.1 % | ±0.8 % | the rule |
| `cpu-batch` (`kdenlive_render`) | block per run | 30 | 4.593 µs | 35.2 % | ±13.1 % | the rule's 1 µs floor, at the projection (D109) |
| `cpu-batch` (`kdenlive_render`) | CPU total | 30 | 16.545 s | 2.1 % | ±0.8 % | the rule |

Reported beside them:

- **The job.** 16.181–17.427 s, 16.055–17.305 s of CPU, saturation 0.9920–0.9946; 14 threads, `melt-7`'s 9 holding 99.6 % of the CPU.
- **The threads.** The busiest holds 0.682–0.691 of the CPU, the next 0.183–0.192.
- **The blocks.** 8,454–8,641 runs a landing; 1.8–50.5 ms of blocks a job, 26 of the 30 jobs ending on one 40 ms block, melt's progress sleep (D109); 47 disk waits over the 30 landings (0.03–0.86 ms) and 3 uninterruptible waits.
- **Beside the job.** Kdenlive's window held 66.9–78.7 ms of the measured CPU during the job.

Before the campaign, five dry runs, three on the EPYC 7763: #157, whose shortcut opened no dialog, and #160 and #161, the fixed driver's (D105).

Pooled in `task-9.10-scenarios-timelines/campaign/kdenlive/results/` (`pooled.json`, `results.md`).

## 9.10 — `incremental-backup`, Déjà Dup's scheduled weekly incremental

Repeats 1–30 on the AMD EPYC 7763, 30 landings, 28 valid; repeats 12 and 25 left out — the set's fetch returned a 12 KB page from mattmahoney.net in place of the archive, and their backups ran on an empty tree. The method's checks:

- the layer built with no package missing and the 9 packages `apt-get install deja-dup` added, one set across the landings;
- `deja-dup` 45.2-1build2, `duplicity` 2.1.4-3ubuntu2 and `librsync2t64` 2.3.4-1.1ubuntu2;
- Mahoney's set, its archive and manifest matching their pins, verified where Déjà Dup reads it as `~/10gb`;
- the first backup by Déjà Dup's own assistant, one full chain of 24 volumes on the loop-mounted drive, the password in the keyring;
- the change set, seven days of Cumulus's rates, one plan across the landings: 9,729 changed files of 883.1 MB and 304.2 MB of new files;
- the set cached at 0.9915–1.0000 at the start;
- the kernel's transparent huge pages `always`;
- `deja-dup --backup --auto` started by the monitor 120.0–121.0 s after the session's start, in `SCHED_IDLE` and the idle I/O class; `last-backup` advanced; the drive's chain one full backup and one incremental of four volumes.

Each repeat landed once. 56 jobs: 30 landed, 26 stopped by the machine gate.

The entry is `incremental-backup` (9.10 D119–D121): the tree of the `deja-dup` the monitor starts, pooled.

| archetype | value | landings | mean | spread (cv) | 95 % half-width | stopped by |
|---|---|---|---|---|---|---|
| `incremental-backup` | run between voluntary blocks | 28 | 1.966 ms | 11.3 % | ±4.4 % | the rule |
| `incremental-backup` | block per run | 28 | 3.730 µs | 16.0 % | ±6.2 % | the rule's 1 µs floor |
| `incremental-backup` | CPU total | 28 | 165.668 s | 1.4 % | ±0.56 % | the rule |

Reported beside them:

- **The job.** 162.5–174.9 s, 161.7–174.0 s of CPU, saturation 0.9935–0.9952; 52 processes of 115–118 threads. `duplicity` holds 0.569–0.576 of the CPU over eight runs, `deja-dup` 0.283–0.291, `gpg` 0.134–0.140.
- **The threads.** The busiest holds 0.320–0.333 of the CPU, the next 0.283–0.291, the third 0.223–0.239.
- **The stages.** duplicity's dry run 59.9–64.1 s, the incremental 96.9–106.4 s, the verify 4.1–4.3 s. Every backup runs the dry run: `ToolJob.Flags` is a plain enum (9.10 D119).
- **The blocks.** 80,712–118,619 runs a landing; 0.24–0.45 s of blocks a job; 246–362 disk waits a job (0.12–0.33 s) and 85–117 uninterruptible waits. In the dry run `deja-dup` reads duplicity's log after nearly every write in 2 of the 28 landings and in batches in 26, the run between voluntary blocks 1.40–1.41 ms against 1.99–2.09 ms (9.10 D122).

At the first batch's five landings the run between voluntary blocks stood at ±26.3 %, the two modes 2 to 3; the batch to 30 repeats (D122) brought it within the rule, and no exception was taken.

Before the campaign, eight dry runs, four on the EPYC 7763: #176 and #177, whose drivers met a black window and an unread button; #180, the whole job on the 100 MB subset; #182, the job on the 10 GB set, read for D119.

Pooled in `task-9.10-scenarios-timelines/campaign/dejadup/results/` (`pooled.json`, `results.md`).

## 9.10 — Chrome's renderer count for five tabs (`renderer-hidden`'s count in the Chrome files)

Repeats 1–5 on the AMD EPYC 7763, each landing once, all valid. Google Chrome 154.0.8037.57 as the runner image ships it, one window of five tabs at five loopback addresses serving 9.8's idle page, the first selected (9.10 D126, D129); two launches per job in fresh profiles, the spare renderer off and on, their order alternating (D128); Chrome's tree listed every 10 s through a 20 s launch settle, the 630 s grace and the 600 s steady phase, no `perf`. The method's checks: both launches run with a window; five page loads in each launch; the measured tree holding no harness process; each launch's steady phase listed.

9 jobs: 5 landed, 4 stopped by the machine gate.

A count is not on the stability rule's list; it is carried as observed, and the count holds when every repeat gives one (D129).

| value | landings | observed | stopped by |
|---|---|---|---|
| `renderer-hidden` tasks: page renderers beyond the page in use, the spare off, the steady phase (D127) | 5 | 4 in every repeat | one count in every repeat, at the workflow's five |
| the spare: the spare-on launch's plain renderers beyond the spare-off launch's (D128) | 5 | 1 in every repeat | as above |

Reported beside them:

- **The plain renderers** held their count from each launch's first listing, 0.6–9.0 s after the launch, to the steady phase's end, one pid set through the steady phase: five with the spare off, six with it on.
- **Chrome's own renderers.** One WebUI renderer in every listing. Four extension renderers in each launch's first 12 s, two at a time, gone by 22–40 s after the launch, except one in the spare-on launch of repeat 3 and one in the spare-off launch of repeat 4, started 10.7 s after the launch and alive at the steady phase's end. Both kinds are `web-browser`'s (9.5 D84; 9.10 D127).

Before the campaign, two dry runs: #72, whose listing read every process as the browser, Chrome rewriting its children's process titles; #73 on the EPYC 7763, the tooling holding.

Pooled in `task-9.10-scenarios-timelines/campaign/chrome-tabs/results/` (`pooled.json`, `results.md`).

## 9.10 — the launch phases of the applications started mid-file (ten entries' `launch`)

Repeats 1–5 of each of ten subjects on the AMD EPYC 7763, each landing once, all valid. Each subject is an entry's own campaign's launch (9.10 D133): LibreOffice 24.2.7.2 on the generated document (`office-writer`), Thunderbird 157.0 with its compose window (`mail-client`), Kdenlive 23.08.5 on 9.5's project (`video-editor`), `mpv` 0.37.0 on the video and the audio (`video-player`, `audio-player`), Element Desktop 1.12.30 signed in to the local homeserver (`chat-client`), the Steam client build 1788652215 logged out (`game-client`), Google Chrome 154.0.8037.57 on 9.5's typed page (`web-browser`) and on 9.8's hidden-tab window (`renderer-hidden`), and the loopback call opened in a Chrome running past `web-browser`'s settle (`video-call`, D134). Each job launches the subject once unmeasured through its settle, quits it by the program's own command, reads the files it mapped whole, and traces the next launch with `perf sched record` from the exec (the call: its opening) to the end of the entry's settle (D132, D135). The method's checks: the tree's exit within 60 s of the quit (120 s for the Steam client); the mapped files' cached fraction at least 0.99 before the traced launch (1.0000 in every repeat, over the files the host can read); the traced tree holding no harness process; the trace stopped cleanly with no lost events; Element signed in, the Steam client logged out, the call connected, the hidden-tab window's 13 tab renderers at the gate.

86 jobs: 50 landed, 36 stopped by the machine gate.

A launch phase is replayed (D136): no value is on the stability rule's list, and each repeat is carried as observed. Per entry, over the five repeats:

| entry | subject | phase, s | CPU, ms | wakes | first 10 s, ms/s (mean) |
|---|---|---|---|---|---|
| `office-writer` | `launch-soffice` | 40.8 | 1,641–1,709 | 838–863 | 162.8 |
| `mail-client` | `launch-thunderbird-send` | 408.9 | 3,217–3,386 | 13,083–13,176 | 227.9 |
| `video-editor` | `launch-kdenlive` | 30.6 | 2,096–2,259 | 1,836–1,893 | 217.6 |
| `video-player` | `launch-mpv-video` | 30.6–30.7 | 3,671–4,488 | 23,809–26,888 | 138.5 |
| `audio-player` | `launch-mpv-audio` | 30.6 | 437–479 | 6,849–6,991 | 32.3 |
| `chat-client` | `launch-element` | 53.2–53.7 | 3,096–3,355 | 9,745–9,768 | 296.0 |
| `game-client` | `launch-steam` | 905.8–916.7 | 21,367–25,352 | 309,067–315,165 | 423.9 |
| `web-browser` | `launch-chrome` | 420.6 | 2,760–3,300 | 24,628–25,898 | 153.0 |
| `renderer-hidden` | `launch-chrome-hidden`, Chrome's whole tree | 651.2 | 3,996–4,494 | 25,646–27,482 | 274.1 |
| `video-call` | `launch-webrtc` | 210.1 | 121,142–124,276 | 414,509–418,464 | 171.0 |

Reported beside them:

- **`renderer-hidden`'s streams.** The 12 background tabs' renderers of each launch, the control tab's identified at 10.8–11.0 wakes/s against 0.88–1.10 for the next renderer: 52.4–65.0 ms of CPU and 528–714 wakes each over the phase. No renderer started after the gate in any repeat.
- **The warm state.** The fraction is over the mapped files the host can read: Thunderbird's snap maps 160 of its 211 files from content snaps mounted in its own namespace, and the Steam client's web helpers 131–134 of 399–418 from their pressure-vessel container; Element 1 of 160. In the traces, the launched tree's waits in uninterruptible sleep total 0.004–0.115 s per traced launch (Thunderbird 0.045–0.068 s, the Steam client 0.066–0.112 s).
- **The quits.** LibreOffice, Thunderbird and Element by Ctrl+Q, Element's confirmation answered; `mpv` by `q`; Kdenlive, Chrome and the Steam client by their main window's own close. Every tree exited in 1–5 s, Element's in 5 s after its confirmation; the Steam client's fallback, `steam -shutdown`, never ran.
- **The builds.** The vendors' repositories serve the current build: Thunderbird 157.0 against `mail-client`'s 156.0 and 156.0.1, Element 1.12.30 against `chat-client`'s 1.12.28, Google Chrome 154.0.8037.57 against the 152 and 153 `web-browser`, `renderer-hidden` and `video-call` were measured on.

Before the campaign, four dry runs (#77–#80), the gate open on any model, their findings amending the method (§8): `fincore` installed for the warm check; Kdenlive's and Chrome's shortcuts ignored under Xvfb with no window manager, both closed by their window's own close; Kdenlive's first window by class a secondary one; Thunderbird's quit sent to its main window; Element's confirmation answered; the Steam client's `steam -shutdown` replaced by its sign-in window's close; the hidden tabs' renderers taken at the gate, a later renderer reported and not a stream.

Pooled in `task-9.10-scenarios-timelines/campaign/launch/results/` (`launch-<subject>-pooled.json`, `results.md`); the streams in `dataset/launch/`.

## 9.10 — `video-editor`'s idle phase past Kdenlive's launch work, and its launch re-traced to the new settle

Two campaigns (9.10 D146, D147): the idle repeats, `meas-ci:interactive:2026-10-05`, runs #664–#674; the launch re-trace, `meas-ci:desktop:2026-10-05`, runs #100–#101. Every repeat on the AMD EPYC 7763, kernel `6.17.0-1022-azure`, Kdenlive 23.08.5 (Ubuntu's `4:23.08.5-0ubuntu4`) on 9.5's project, each index landing once, all valid.

The idle repeats run 9.5's `kdenlive` subject in mode `idle`, the window, a 240 s settle and a 180 s idle phase alone (D146). They replace `video-editor`'s idle values; its driven and operation values stay those of 9.5's 20 repeats (`meas-ci:interactive:2026-09-18`), the fold-in's `--idle-from`. 32 jobs: 16 landed, 16 stopped by the machine gate.

| archetype | subject | repeats | values | pass | widest | stopped by | jobs (gated) | recorded input covered |
|---|---|---|---|---|---|---|---|---|
| `video-editor`, its idle phase | `kdenlive`, mode `idle` | 16 (1–16) | 6 | 6 | `kdenlive` run mean ±4.45 % | the rule | 32 (16) | none (the idle phase replays no input) |

The first batch, repeats 1–5, held the main thread's three values at ±5.7 %; repeats 6, 7–8 and 9–16 were added as the projection grew to 6, 8 and 16 (9.7 D26). The main thread `kdenlive` wakes 1.1611/s ±1.71 %, its gap mean 861.3 ms ±1.71 %, its run mean 0.0261 ms ±4.45 %; `Qt bearer threa` wakes 0.1/s ±0.00 %, its run mean 0.4237 ms ±1.77 %. The main thread's run mean turns on how many of its rare long runs, 200–260 µs against a mean near 25 µs, a 180 s phase catches. Against 9.5's 20 repeats, the phase 120 s from a 30 s settle: the main thread's wakes 1.2604/s then, 1.1611/s now; the tree's 1.3625/s then, 1.2637/s now, against D145's probe level of 1.212/s past the settle.

The launch re-trace runs `launch-kdenlive` from the exec to the end of the 240 s settle (D133, D146): 6 jobs, 5 landed, 1 stopped by the machine gate. Its phase runs 240.637–240.645 s; its CPU 2,136.6–2,302.3 ms, its wakes 2,141–2,196 per repeat, the first 10 s at 219.8 ms/s on average — against the 30 s phases' 2,096–2,259 ms in `meas-ci:desktop:2026-10-04b`, the launch's CPU falling almost wholly in its first seconds. Its 5 repeats replace `launch-video-editor`'s stream (D136).

Pooled in `task-9.10-scenarios-timelines/campaign/kdenlive-idle/results/` (`pool-kdenlive.json`, `launch-kdenlive-pooled.json`, `results.md`).

## 9.10 — `renderer-hidden` past its page thread's settling, and its launch re-traced to the new grace-settle

One campaign (9.10 D152, D155, D156), `meas-ci:desktop:2026-10-05b`, runs #105–#107. Every repeat on the AMD EPYC 7763, kernel `6.17.0-1022-azure`, Google Chrome 154.0.8037.57 as the runner image ships it, against the 152 and 153 9.8 and `web-browser` ran (D156); each index landing once, all valid.

The steady repeats run 9.8's `chrome-hidden` subject unchanged but for the grace-settle, 20 s after launch, 1,030 s of grace-settle and the 600 s steady phase (D152); 12 renderers measured of 16 observed. They replace `renderer-hidden`'s values. 10 jobs: 5 landed, 5 stopped by the machine gate.

| archetype | subject | repeats | values | pass | widest | stopped by | jobs (gated) | recorded input covered |
|---|---|---|---|---|---|---|---|---|
| `renderer-hidden` | `chrome-hidden` | 5 (1–5) | 18 | 4 | `chrome` wake rate ±1.59 % | the rule, under 9.8's per-value treatments (D155) | 10 (5) | none |

The values outside the tolerance, each carried over its repeats with its half-width and range (`campaign/renderer-hidden/results/results.md`):

- run means following the runner's speed (9.8 D17): `HangWatcher` 0.0262 ms ±18.08 % (0.0211–0.0310); `chrome` 0.0624 ms ±11.42 % (0.0558–0.0700).
- components varying between sessions (9.5 D57; 9.8 D21, D24, D26): `Chrome_ChildIOT`, 0.0176 wakes/s ±6.47 % (0.0168–0.0186), gap mean 56.8 s, run mean 0.0324 ms ±7.46 %; `Compositor` and `PerfettoTrace`, which wake together, 0.0083 wakes/s ±17.56 % (0.0067–0.0100), gap mean 120.0 s, run means 0.0226 ms ±12.28 % and 0.0209 ms ±9.26 %; within one run, on D149's 3,600 s probe, ±30.6 %.
- the sparse residual (9.8 D27): `ThreadPoolServi` and `MemoryInfra`, 0.0096 wakes/s ±20.20 % (0.0083–0.0121), gap mean 104.3 s, run mean 0.0346 ms ±61.28 %, 5.0–7.2 wakes per renderer a phase; within one run ±64.0 %. `ThreadPoolServi`, a component of its own in 9.8, falls below the 95 % coverage cut (9.5 D16), the page thread and `Chrome_ChildIOT` waking more.

Against 9.8's 19 repeats the page's own thread wakes 1.72 times as often with runs 35 % shorter, `Chrome_ChildIOT` 2.51 times as often, `Compositor` and `PerfettoTrace` 1.28 times; the renderer's wakes 0.211 against 0.169/s, its CPU share 9.6 against 9.2 × 10⁻⁵. The entry is folded with the build split from `web-browser` stated (D156, by 인지오's decision).

The launch re-trace runs `launch-chrome-hidden` from the exec to the end of the 1,030 s grace-settle (D133, D152): 6 jobs, 5 landed, 1 stopped by the machine gate. Repeats 2 and 5 carried a plain renderer started before the gate's listing, and the five landings were re-analysed locally, the tabs' renderers the lowest client ids (D155): 12 streams in each. Its phase runs 1,051.219–1,051.227 s; Chrome's whole tree 4,096.8–5,123.3 ms of CPU and 32,317–34,529 wakes per repeat, the first 10 s at 259.8 ms/s on average, against the 651.2 s phases' 3,996–4,494 ms in `meas-ci:desktop:2026-10-04b`. Its 5 repeats replace `launch-renderer-hidden`'s stream (D136).

Pooled in `task-9.10-scenarios-timelines/campaign/renderer-hidden/results/` (`pooled.json`, `launch-chrome-hidden-pooled.json`, `results.md`).

## Machine draws

The build campaign, complete: 28 jobs, 14 on the AMD EPYC 7763 (50.0 %), 12 stopped by the machine gate — Intel Xeon Platinum 8573C 4, AMD EPYC 9V74 4, AMD EPYC 9V45 2, Intel Xeon Platinum 8370C 1, Intel Xeon 6973P-C 1 — and 2 cancelled.

The 9.5 campaigns of 2026-09-18 and 2026-09-19, over the six applications whose rule holds and complete for them: 252 jobs — 144 landed on the AMD EPYC 7763 (57.1 %, one of them `thunderbird-send`'s dry check), 107 stopped by the gate, 1 cancelled. The model is recorded for 104 of those stops, the reports the loop read: AMD EPYC 9V74 47, Intel Xeon Platinum 8573C 19, AMD EPYC 9V45 18, Intel Xeon 6973P-C 12, Intel Xeon Platinum 8370C 8. Per application, gate stops: `thunderbird-send` 32, `mpv-video` 27, `mpv-audio` 24, `soffice` 11 (5 of them in the pooled campaign, 6 in the superseded first design), `kdenlive` 10, `gimp` 3. The 2026-09-20 campaign re-measuring `chrome`, `code` and `webrtc` is still running. The batch D94 added to the 2026-09-19 campaign on 2026-09-28 (runs #651–#663, `thunderbird-send`'s windows 45–78): 57 jobs, 34 landed on the AMD EPYC 7763, 23 stopped by the gate — AMD EPYC 9V74 18, AMD EPYC 9V45 2, Intel Xeon 6973P-C 2, Intel Xeon Platinum 8370C 1.

The 9.7 background campaign, complete: 145 jobs — 78 drew the AMD EPYC 7763 (53.8 %): 71 landed (66 pooled; `borg`'s repeat 3 and `steamcmd`'s 21, 23, 32 and 33 left out) and 7 were stopped by the network gate; 67 stopped by the machine gate: AMD EPYC 9V74 24, Intel Xeon Platinum 8573C 20, AMD EPYC 9V45 14, Intel Xeon 6973P-C 8, Intel Xeon Platinum 8370C 1. Per program, machine-gate stops: `steamcmd` 35, `borg` 24, `7z` 8. With the tooling's dry runs, the probes and the SteamCMD diagnostics, none of them a repeat, 105 of 190 jobs drew the EPYC 7763 (`task-9.7-background-io/campaign/machine-draws.md`).

The 9.8 desktop campaign, complete: 105 jobs, the hidden renderer's added repeats (D31, runs #51–#57) included — 60 landed on the AMD EPYC 7763 (57.1 %, all pooled), 45 stopped by the machine gate: AMD EPYC 9V74 20, Intel Xeon Platinum 8573C 11, AMD EPYC 9V45 8, Intel Xeon 6973P-C 4, Intel Xeon Platinum 8370C 2. Per entry, gate stops: `chrome-hidden` 15, `element` 14, `steam` 9, `chrome-visible` 7. With the tooling's dry runs and the long-phase probes, neither of them a repeat, 76 of 141 jobs drew the EPYC 7763 (`task-9.8-browser-comms/campaign/machine-draws.md`).

The 9.9 session campaign, complete: 42 jobs — 24 landed on the AMD EPYC 7763 (57.1 %, all pooled), 18 stopped by the machine gate: AMD EPYC 9V74 6, Intel Xeon Platinum 8573C 5, AMD EPYC 9V45 3, Intel Xeon 6973P-C 3, Intel Xeon Platinum 8370C 1. With the tooling's dry runs and the long-phase probes, neither of them a repeat, 41 of the 82 jobs whose model is recorded drew the EPYC 7763; 8 more dry jobs ended without a report, 90 in all (`task-9.9-daemons-session/campaign/machine-draws.md`).

The 9.10 unattended-upgrade campaign, complete: 15 jobs — 9 landed on the AMD EPYC 7763 (60.0 %, all pooled), 6 stopped by the machine gate: AMD EPYC 9V45 2, AMD EPYC 9V74 2, Intel Xeon Platinum 8370C 1, Intel Xeon Platinum 8573C 1. Its dry run (#99) drew the EPYC 7763.

The 9.10 DKMS campaign, complete: 37 jobs — 26 landed on the AMD EPYC 7763 (70.3 %, all pooled, three of them second landings of one push's two runs), 11 stopped by the machine gate: AMD EPYC 9V74 6, Intel Xeon Platinum 8573C 3, AMD EPYC 9V45 1, Intel Xeon 6973P-C 1. Its two dry runs (#106, #107) drew the EPYC 7763.

The untraced control of 9.5, 9.8 and 9.9, complete (9.5 D82, 9.8 D32, 9.9 D40): 148 jobs — 87 landed on the AMD EPYC 7763 (58.8 %; 84 pooled, three later copies of a window that landed twice left out under 9.5 D66), 61 stopped by the machine gate: AMD EPYC 9V74 25, AMD EPYC 9V45 13, Intel Xeon Platinum 8573C 12, Intel Xeon 6973P-C 7, Intel Xeon Platinum 8370C 4. By family: interactive 61 jobs, 36 landed; playback 31, 19; desktop 46, 26; session 10, 6.

The 9.10 Tracker campaign, complete: 38 jobs — 18 landed on the AMD EPYC 7763 (47.4 %, all pooled), 20 stopped by the machine gate: AMD EPYC 9V74 16, Intel Xeon Platinum 8573C 1, Intel Xeon Platinum 8370C 1, AMD EPYC 9V45 1, Intel Xeon 6973P-C 1. Its three dry runs (#118, #119, #121) drew the EPYC 7763 after four stops; its first batch (12 jobs, 7 landed) and its cold batch (8 jobs, 5 landed) were not pooled.

The 9.10 MNIST campaign, complete: 8 jobs — 6 landed on the AMD EPYC 7763 (75.0 %, all pooled), 2 stopped by the machine gate: Intel Xeon 6973P-C 1, AMD EPYC 9V45 1. Its dry run (#142) drew the EPYC 7763 after one stop (AMD EPYC 9V45). Its `madvise` check (D87), never a repeat: 9 jobs, 5 landed, 4 stopped (AMD EPYC 9V45 2, AMD EPYC 9V74 2).

The 9.10 HandBrakeCLI campaign, complete: 9 jobs — 5 landed on the AMD EPYC 7763 (55.6 %, all pooled), 4 stopped by the machine gate: AMD EPYC 9V74 4. Its probe (D93), never a repeat, took 3 jobs, 2 landed and 1 stopped (Intel Xeon Platinum 8370C). Its two dry runs (#152, superseded by D95; #153) drew the EPYC 7763.

The 9.10 Kdenlive export campaign, complete: 56 jobs — 30 landed on the AMD EPYC 7763 (53.6 %, all pooled), 26 stopped by the machine gate: AMD EPYC 9V74 14, AMD EPYC 9V45 7, Intel Xeon Platinum 8370C 3, Intel Xeon Platinum 8573C 2. Its five dry runs (#157–#161): 3 drew the EPYC 7763, 2 stopped (AMD EPYC 9V74, AMD EPYC 9V45).

The 9.10 Déjà Dup backup campaign, complete: 56 jobs — 30 landed on the AMD EPYC 7763 (53.6 %; 28 pooled, repeats 12 and 25 left out), 26 stopped by the machine gate: AMD EPYC 9V74 11, AMD EPYC 9V45 7, Intel Xeon Platinum 8573C 4, Intel Xeon 6973P-C 3, Intel Xeon Platinum 8370C 1. Its eight dry runs (#175–#182): 4 drew the EPYC 7763, 4 stopped (AMD EPYC 9V74 3, AMD EPYC 9V45 1).

The 9.10 Chrome tab-set campaign, complete: 9 jobs — 5 landed on the AMD EPYC 7763 (55.6 %, all pooled), 4 stopped by the machine gate: AMD EPYC 9V74 2, AMD EPYC 9V45 1, Intel Xeon 6973P-C 1. Its two dry runs, the gate open on any model: #72 on an Intel Xeon Platinum 8370C, #73 on the EPYC 7763 (`task-9.10-scenarios-timelines/campaign/chrome-tabs/machine-draws.md`).

The 9.10 launch campaign, complete: 86 jobs — 50 landed on the AMD EPYC 7763 (58.1 %, all pooled), 36 stopped by the machine gate: AMD EPYC 9V45 14, AMD EPYC 9V74 12, Intel Xeon Platinum 8370C 4, Intel Xeon Platinum 8573C 3, Intel Xeon 6973P-C 3. Its four dry runs (#77–#80), the gate open on any model: 18 jobs, 11 on the EPYC 7763 (`task-9.10-scenarios-timelines/campaign/launch/machine-draws.md`).

The 9.10 Kdenlive idle campaign, complete: 32 jobs — 16 landed on the AMD EPYC 7763 (50.0 %, all pooled), 16 stopped by the machine gate: AMD EPYC 9V45 5, AMD EPYC 9V74 4, Intel Xeon Platinum 8573C 4, Intel Xeon 6973P-C 2, Intel Xeon Platinum 8370C 1. Its launch re-trace (`launch-kdenlive`, runs #100–#101): 6 jobs, 5 landed (83.3 %), 1 stopped (AMD EPYC 9V45). Neither campaign took a dry run.

The 9.10 hidden-renderer campaign, complete (runs #105–#107): 16 jobs — 10 landed on the AMD EPYC 7763 (62.5 %, all pooled), 6 stopped by the machine gate: AMD EPYC 9V74 3, AMD EPYC 9V45 1, Intel Xeon Platinum 8370C 1, Intel Xeon 6973P-C 1. Per subject: `chrome-hidden` 10 jobs, 5 landed; `launch-chrome-hidden` 6 jobs, 5 landed. It took no dry run; the hidden renderer's span probes before it, run #99 (D143) and runs #102–#104 (D149's 3,600 s probe), are not repeats.
