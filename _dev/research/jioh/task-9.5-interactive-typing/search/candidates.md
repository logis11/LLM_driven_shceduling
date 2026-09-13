# Task 9.5 — candidates per scope-card item

Stage 2 result. Each item of `../scope-card.md` with the candidates the four class records found (`S1-literature.md`, `S2-project-docs.md`, `S3-traces-datasets.md`, `S4-ci-observability.md`), what each covers, and what no class found. Candidate ids are the records' own. Written by the research routine; every number below is quoted or derived in the record named, and stage 3 decides nothing here.

## Observations that exist

Observations (a population, trace or run with numbers), as distinct from documentation and source defaults:

| Id | What | Machine / application / subject / window | Kind of data |
|---|---|---|---|
| S1-dhakal2018 = S3-aalto136m (`dhakal-chi18`) | 136M Keystrokes study and its released dataset | participants' own devices (98 % laptop or desktop keyboard) / a web typing test / 168 960 volunteers / 15 sentences each | paper: per-participant aggregates (mean IKI 238.66 ms, SD 111.6 across participants, skew 1.98, ≥60 ms floor, hold 116 ms); dataset: raw press/release ms timestamps per keystroke (1.57 GB), non-commercial with attribution. S3's six-participant sample: within-sentence press-to-press p50 171 ms, p90 396, p99 934, share > 1 s 0.7 %; between-sentence gaps p50 2.8 s; per-participant `AVG_IKI` over all 168 594 rows p50 208.8 ms, p90 381 |
| S1-roeser2021 = S3-osf-y3p4d (`roeser-rw24`) | Inputlog copy-task mixture study and its OSF data | participants' browsers / Inputlog copy task / 250 Dutch 18–25-year-olds fitted (the OSF `ct.csv` holds 1 662 subjects, 1.45 M IKIs, CC0) / one copy of each string | paper: two-component log-normal, LF-bigrams fluent 158 ms [139, 180], slowdown 95 ms, θ 0.34; consonants 429 ms, 414 ms, 0.73. S3's computation on `ct.csv`: LF p50 235 ms, p90 648, p99 1 736, share > 1 s 3.7 %; Sentence p50 136, p90 226; Consonants p50 389, share > 1 s 17 %; all rows p50 126, p90 261, p99 1 120 |
| S3-howwetype = S1-feit2016 | How-We-Type lab study | one lab keyboard / transcription / 30 participants / 50 sentences each, 2015 | raw keypress timestamps, `iki` per keypress (CC-BY-NC); S3: p50 155 ms, p90 342, p99 842, share > 1 s 0.5 %; clock quantised at ~31 ms |
| S3-cmu-keystroke = S1-killourhy2009 | CMU password benchmark | one Windows XP laptop, ±200 µs reference clock / one password / 51 subjects / 400 repetitions | down-down latencies: p50 191 ms, p90 462, p99 1 040 |
| S3-keyrecs | KeyRecs transcription exercise | unnamed / unnamed / 99–100 participants / two sessions | digraph latencies: p50 174 ms, p90 528, p99 1 649 (CC-BY) |
| S3-swell-kw | SWELL Knowledge Work uLog | Windows PCs, Word 2010 / Outlook 2010 / IE / 25 participants / ~3 h each, 2012 | per-keystroke timestamps with the focused application, free composition; S3 on one file: Word p50 191 ms, p90 1 577, share > 1 s 15 %; Outlook p50 172; IE p50 228 (CC-BY-NC-SA) |
| S1-chukharev2014 | chat composition study | participants' own PCs / web chat / 36 participants / 34 games | per-participant ex-Gaussian IKI fits: μ ≈ 99 ms, σ ≈ 42, τ ≈ 268; pause threshold ≈ 492 ms; no data release |
| S1-gonzalez2021 | three free-text keystroke datasets | unnamed / free text and transcription / per-dataset | distribution-family ranking (log-logistic best, log-normal second, ex-Gaussian poor); per-key CSVs released; no parameter values |
| S3-balabit, S3-dfl, S3-shen-mouse | pointer traces | RDP monitoring, 10 users; 21 personal computers, 2018; a fixed pattern, 56 subjects | per-event mouse timestamps; Balabit move→move p50 109 ms at ~15.6 ms ticks; DFL p50 8 units (ms) |
| S1-lorch2003 | VTrace UI-event traces | eight named Windows NT/2000 machines / real use / 8 users / 83–504 h each over 2–19 months | per-event CPU-time CDFs (keystroke, mouse move, click) above the 90th percentile; UI events 20.3 % of CPU, timer messages 35.1 %; mouse moves > 99 % under 10 Mc (≈ 50 ms at 200 MHz); keystroke knee ≈ 10.5 Mc; applications differ significantly |
| S1-flautner2000, S1-flautner2001 | interactive-episode traces | Dell Precision 410, dual 450 MHz PII, Linux 2.3.99, X11/GNOME 1.2 / Xemacs, FrameMaker, Netscape 4.7, GIMP 1.1, Acroread, Ghostview / one user / seven runs | episode-length buckets: Xemacs 65 % of episodes < 1 ms, 34 % in 1–10 ms, 0 % ≥ 100 ms; GIMP 88 % < 1 ms but 91 % of time in ≥ 100 ms episodes; keystroke echo "sub millisecond"; mpg123 + esd ≈ 5 % CPU |
| S1-flautner2002 | Vertigo traces | Sony Vaio Crusoe 5600 300–600 MHz, Linux 2.4.4 / Emacs, Netscape News, Konqueror, Acrobat, plaympeg / one user | Emacs episodes met at the lowest clock 95.6 % of the time; plaympeg idle 22–54 % per clip |
| S1-tsafrir2003 = S1-etsion2004 = S1-etsion2006 | klogger traces | 664 MHz P3, Linux 2.4.8 at 100/1000 Hz / Emacs and OpenOffice at 8 char/s, Xine, MPlayer, Quake / single runs | per-schedule runtime (effective quantum) CDFs; Emacs 22–35 quanta/s, ≈ 0.2 % CPU; OpenOffice 2.6 %; Xine 4 ms alarm displayer, 39–40 % CPU + X 20 %, ≈ 470–700 wakeups/s; voluntary switches: editors 99 %, Xine 83 % |
| S1-endo1996 | idle-loop latency traces | 100 MHz Pentium, Windows NT 3.51/4.0/95 / Notepad, Word, PowerPoint / scripted and hand-typed | Notepad keystrokes < 10 ms, Word 32 ms typical (hand) vs 80–100 ms (scripted), carriage returns > 200 ms; 10 ms clock-aligned bursts |
| S1-endo2000 | TIPME | 100 MHz Pentium, BSD/OS / xterm, Netscape 3.0 | xterm character 2.0 ms, mouse move 0.3 ms, Netscape menu 470 ms (typical values) |
| S1-lee1998 | Windows NT instruction traces | dual Pentium Pro 200 / Word, PowerPoint, Netscape, Photoshop, Acrobat / scripted | thread counts 3–8, primary thread 79–99.9 % of instructions |
| S3-firefox-profiles | six public Firefox Profiler profiles | five Linux x86_64 (2–6 cores), one Windows / Firefox 70, 71, 85, 80 / Discord, Slack, Twitter, Facebook, one unnamed page / one user each / 1–23 s | wall-clock handler durations per key event: keypress p50 4 ms (2019) to 24–55 ms (Firefox 85 web apps), 100 % > 10 ms on those; keydown inter-start p50 48–73 ms bursting, 200 ms "typing slowly"; refresh-driver ticks ≈ 16.7 ms when painting; setTimeout and GC wakeups; no CPU deltas |
| S3-sysprof-gnome | two sysprof captures | Ryzen 9 5900X, Fedora 35, GNOME Wayland; Fedora 33 / gnome-text-editor scrolling, gtk4-demo resizing / 17 s, 11 s | main thread on-CPU bursts every ~6–9 ms with ~5–30 ms per burst (perf-sample approximation); gnome-shell every 3–7 ms; pulseaudio, Zoom, Discord threads sampled |
| S3-perfetto-chrome | Perfetto example Chrome trace | Pixel 6, Android 13 / Wikipedia scrolling / 29 s | Chromium thread population; `CrRendererMain` per-task CPU p50 0.02 ms, p90 2.4, p99 6.7 — off-platform |
| S3-pipewire-pwtop | pw-top snapshots in PipeWire issues | reporters' machines (some named) / Firefox, Kodi, Chromium, Wine, gst-launch / one refresh each | quanta 64–2048 frames (1.3–42.7 ms periods); client `BUSY` 3–30 µs per cycle; sink `BUSY` 4.5–62.6 µs |
| S1-cucinotta2011 | JACK on one PC | Intel E8400, Terratec EWX24/96 / synthetic clients / 1-minute runs | JACK period 667–2 666 µs = buffer/rate; ≈ 7 % CPU per synthetic client |
| S3-webrtc-internals | one 2015 Chrome WebRTC dump | unknown / simplewebrtc.com / 54 s | camera 7–8 fps, `googAvgEncodeMs` 4–14; screen share 3 fps |
| S1-chang2021, S1-kumar2022, S1-macmillan2021 | conferencing measurements | two Android phones; two Windows 10 laptops; two Ubuntu 20.04 laptops | whole-client CPU (150–200 %; 15–35 % sender); FPS only on Ubuntu |

Everything else found is documentation or source (S2-01…S2-20; S4-01…S4-25), dataset pointers without obtained data (S3-clarkson2, S3-buffalo, S3-inputlog-ct-corpus aggregates, S1-csedm2023, S1-leinonen2019, S3-imc21-vca), or off-platform (S1-palin2019, S3-aalto-typing37k, S1-herglotz2016, S1-kraenzler2020).

## Per item

### 1–8. `input_gap` (dist, fluent location and spread, pause probability, pause location and spread, overall mean) and `input_gap_family`

- Two sources, two observations, as the card says. S1-dhakal2018 / S3-aalto136m: the paper reports per-participant aggregates only (S1: "Average inter-key interval is 238.656 ms (SD = 111.6)", skew 1.98, floor ≈ 60 ms); the dataset carries raw timestamps, so a keystroke-level distribution is computable (S3's sample: p50 171 ms, p90 396, p99 934 within sentences; between-sentence gaps p50 2.8 s, which mix reading time with the test's transition). S1-roeser2021 / S3-osf-y3p4d: the fitted set is per task (LF bigrams 158 / 95 / 0.34; consonants 429 / 414 / 0.73), fluent spread 0.29 in both tasks; the OSF data (CC0) give per-bigram IKIs for 1 662 subjects across five task components with medians 101–389 ms.
- Alternative shapes and populations for the same quantity: S1-chukharev2014 (free composition in chat, ex-Gaussian μ 99 / σ 42 / τ 268 ms, pause threshold ≈ 500 ms); S1-gonzalez2021 (free text: log-logistic fits best, log-normal second, ex-Gaussian poor); S3-howwetype (transcription, 30 typists, p50 155 ms); S3-cmu-keystroke (password, p50 191 ms); S3-keyrecs (p50 174 ms); S3-swell-kw (free composition in Word with pauses retained: p50 191 ms, share > 1 s 15 %); S1-feit2016 Table 1 second-hand prior figures (easy prose 140 ms, random strings 326 ms).
- Pointer inter-arrival: S3-balabit (RDP-side, ~15.6 ms ticks, move→move p50 109 ms), S3-dfl (local, p50 ≈ 8 ms); no dataset logs pointer events per local application (S3 §3).
- No project documents an inter-arrival statistic (S2 §3 T1; Qt's 400 ms `KeyboardInputInterval` is a UI threshold, S2-02).
- Not observable on a runner: human inter-arrival is replay input, not a measurement (S4).

### 9. `burst_fraction` — CPU per input

- The source behind the tag remains a benchmark emulation (card item 9). Observations of CPU per input event: S1-lorch2003 (Windows NT/2000, eight users, months: per-event CPU CDFs; mouse moves > 99 % under 10 Mc ≈ 50 ms at 200 MHz; keystroke knee ≈ 10.5 Mc; UI events 20.3 % of CPU, timers 35.1 %; "different applications have very different CPU requirements, even when handling the same type of user interface event"); S1-flautner2000/2001 (Linux 2000: keystroke echo and mouse moves are sub-millisecond episodes; per-application episode-length buckets in Table 3; Xemacs 0 % of episodes ≥ 100 ms; GIMP/Ghostview/Acroread > 78 % of time in ≥ 100 ms episodes); S1-endo1996 (Notepad < 10 ms, Word 32 ms per keystroke by hand, 80–100 ms scripted, on a 100 MHz Pentium); S1-tsafrir2003/S1-etsion2004 (Emacs at 8 char/s ≈ 0.2 % CPU, OpenOffice 2.6 %, effective quanta "very short", 22–35 quanta/s); S1-endo2000 (xterm character 2.0 ms).
- Wall-clock, not CPU: S3-firefox-profiles (per-keypress handler p50 4–55 ms on Linux Firefox 70–85; 100 % > 10 ms on the 2021 web-app profiles, 0 % on the 2019 one; paint-phase sum after a keydown p50 8–17 ms). Off-platform CPU per task: S3-perfetto-chrome (`CrRendererMain` p50 0.02 ms, p90 2.4 ms, Android).
- No project publishes a measured per-keystroke CPU figure (S2-19 Zed: an 8.33 ms budget; S2-20 Alacritty: names a tool; S2-03 Chromium: an unattributed scrolling example).
- Runner: per-schedule CPU is observable with `perf sched timehist` (S4-17, root; `linux-tools-azure` packaged, S4-25) or ftrace (S4-19); `/proc` gives cumulative CPU and switch counts only (S4-15, S4-16).
- Not found in any class: a per-input CPU-time distribution for a Linux editor, office suite, mail client, browser or video editor newer than the 2000–2004 traces (S1 §3 T2, S3 §3 T2).

### 10–11. Pattern: input-driven WAIT/RUN, burst coupled to the preceding gap

- Whether GUI wakeups are input-driven only: no. S1-lorch2003 Table 2: timer messages 35.1 % of non-idle CPU vs UI messages 20.3 % on average (per user 6.8–68.1 % timers); S1-endo1996: blinking cursors and spell checkers named as background computation; 10 ms clock-aligned bursts. S3-firefox-profiles: refresh-driver ticks ≈ 16.7 ms when painting, setTimeout callbacks (a 100 ms timer on Facebook; 342 callbacks in 18 s on Slack), GC slices. S3-sysprof-gnome: a GTK4 editor scrolling wakes every ~6–9 ms (paint cadence), not per input.
- Toolkit documentation (S2): an idle GTK 4 app "will stay in the Events phase forever" with no repaint wakeups; repaint is compositor-driven at the output refresh ("roughly every 16 milliseconds" at 60 Hz) with a 60 Hz timer fallback; motion events compressed to one per clock cycle; cursor blink 1 200 ms cycle stopping after 10 s (S2-01). Qt: cursor 1 000 ms, coarse timers coalesced within 5 %, animation tick 16 ms, threaded render loop throttled to vsync (S2-02). Chromium/Electron: input tasks highest priority on the Blink main thread; frames driven by BeginFrame from the display compositor; separate compositor thread (S2-03, S2-04). VS Code: cursor blink on a 500 ms JavaScript interval; view updates at the next animation frame (S2-04). LibreOffice: single-threaded, single-system-timer cooperative scheduler; autosave 10 min; Writer idle jobs after 1 000 ms; EditEngine spell timer 100 ms, status timer 200 ms (S2-05). Gecko/Thunderbird: refresh driver on vsync, 60 Hz guess, 1 fps throttled when hidden; caret blink from GTK settings; mail check default 10 (S2-06). GIMP: canvas rendering as GLib idles at a 1/15 s iteration target (S2-07). Kdenlive/MLT: read-ahead and worker threads (S2-08). Wayland frame callbacks are one-shot and only requested by a client that draws (S2-14).
- Coupling of burst to the preceding gap: no class found a source stating or measuring it. S1-lorch2003 measures CPU per event independent of the interval; S1-flautner2000 finds episodes "very CPU bound, with zero or close zero idle time" but does not relate length to arrival gap.
- Whether a burst outlasts a slice: S1-flautner2000 Table 3 (share of episodes ≥ 10 ms: Xemacs 0.6 %, FrameMaker 8.6 % + 1.7 %, GIMP 0.3 % + 1.6 %); S1-tsafrir2003 Fig. 6 (Emacs quanta "well under 10 ms"); S3-firefox-profiles (100 % of keypress handlers > 10 ms wall-clock on Discord/Slack/Twitter, Firefox 85).

### 12. `sampling: per-iteration`

- No finding; the compile is consistent (card). No class was asked.

### 13. One archetype for six applications

- Evidence that classes differ: S1-lorch2003 §4.7 ("different applications have very different CPU requirements, even when handling the same type of user interface event"; keystroke CDF slopes differ across users); S1-flautner2000 Table 3 (Xemacs vs GIMP vs Netscape vs FrameMaker episode distributions); S1-flautner2002 Fig. 8 (Emacs 95.6 % of episode time at the lowest clock vs Acrobat bimodal vs Konqueror spread); S1-endo1996 (Notepad vs Word an order of magnitude apart); S1-lee1998 Table 3 (thread counts 3–8); S3-swell-kw (Word p50 191 ms vs Outlook 172 vs IE 228 inter-keystroke, one participant file); S3-firefox-profiles (Twitter 30 ms vs Discord 24 vs Slack 55 per keypress); S2 defaults differ per toolkit (cursor 1 200 / 1 000 / 500 ms; autosave; mail check; idle render).
- No source covers all six classes; none read covers a video editor at all (S1 §3 T6, S3 §3 T6). Union available: editor + document editor + browser + image editor (S1-flautner2000), editor + mail/news + browser (S1-flautner2002), word processor + presentation + browser + image editor (S1-lee1998), word processor + mail + browser (S3-swell-kw).

### 14. Scope statement (intra-burst, no think-pauses, no mouse)

- S3-aalto136m confirms what the dataset holds: within-sentence intervals up to 5 s stay in (share > 1 s 0.7 % in the sample); between-sentence gaps exist in the raw files (p50 2.8 s) and are not IKIs by the paper's rule; mouse editing was allowed and not logged (S1-dhakal2018, R08). Pause-bearing alternatives: S3-swell-kw (Word share > 1 s 15 %), S1-chukharev2014 (pause threshold ≈ 500 ms derived from ex-Gaussian fits), S3-osf-y3p4d (LF share > 1 s 3.7 %, consonants 17 %).

### 15–16. `modeling_notes` wording

- Item 15: Roeser's fluent spread is 0.29 in both tasks (S1-roeser2021 Table 3 via R08; card). Item 16: interbench's own words are quoted in K1 and R01; no new source.

### 17. `validation_stats: referee: none`

- What a runner can do (S4): drive VS Code under Xvfb with Playwright, as VS Code's own CI does on `ubuntu-24.04` (S4-09: `Xvfb :10 -ac -screen 0 1024x768x24`, `_electron.launch`, typing at a constant 50 ms delay; AppArmor sysctl needed for Chromium's sandbox); browsers headless or headed (S4-08, S4-14); LibreOffice Writer through the UI-test `TYPE` action (whole strings, no per-key timing; S4-10); KDE apps under Xvfb through the AT-SPI WebDriver (S4-12); mpv with `--ao=null --vo=x11` (S4-13). GIMP's own CI is batch-only (S4-11).
- Replaying recorded inter-key intervals: xdotool `type`/`key --delay` and ydotool `--key-delay` and Playwright `type({delay})` each document one constant delay; per-event replay only via xdotool script `sleep` chaining ("not fully fleshed out", S4-05) or `evemu-play` (recorded µs timestamps through uinput, root; S4-07). Replay sources with raw timestamps: S3-aalto136m, S3-howwetype, S3-swell-kw.
- Observing: `perf sched timehist` gives per-schedule run time, wait time and delay per thread (S4-17), root required (S4-18), `linux-tools-azure` matches the runner kernel ABI (S4-25); ftrace/trace-cmd (S4-19), strace fallback (S4-20), bcc/bpftrace (S4-21); `/proc/<pid>/task/<tid>/{stat,status,schedstat}` cumulative only (S4-15, S4-16).
- Not observable: display refresh (Xvfb has "no display hardware", documents no refresh, S4-03); audio device timing (null sinks are timerfd/rtclock-driven with zero delay, S4-22, S4-23; the azure kernel module packages ship no sound modules, S4-25); GPU (llvmpipe rasterises on CPU threads, S4-24); human pauses.
- Not established by any document: whether hosted runners have a sound device or `/dev/uinput`; the runner's `perf_event_paranoid` and tracefs state; whether Xvfb accepts uinput input (S4 §3).

### 18. `category_source: interbench`

- No new source; the card's verdict stands. The only literature naming interbench's category is none (S1 found no academic use of interbench; K1 C-interbench-13).

### 19–23. Registry lines

- Items 19–21 follow from items 1–8 and 14 (S1-dhakal2018 §5 wording; S3-aalto136m dataset facts; S1-roeser2021 Table 3 per task). Item 22 SUPPORTED (no new source). Item 23: no class re-read the interbench repository (out of the topics); K1's finding stands.

### 24–25. `audio-playback.period`, `burst` (50 000 / 2 500 µs)

- Documentation of what governs an audio path's wake period on a Linux desktop (S2): PipeWire default quantum 1 024 at 48 000 Hz = 21.3 ms per period, min 32, VM override min 1 024, driver wakes on a timer, per-node `WAIT`/`BUSY` exposed by `pw-top` (S2-09); PulseAudio timer-based scheduling sleeps at least 10 ms per iteration and wakes at least 4 ms before a 2 s buffer runs empty (adaptive, not a fixed period), fragments 4 × 25 ms when used, IO threads SCHED_FIFO 5 (S2-10); ALSA raises one wakeup per period, period time in µs, no default value (S2-11); GStreamer audio sinks write in 10 ms iterations into a 200 ms buffer (S2-13); mpv keeps a 200 ms minimum audio buffer (S2-12). No project documents a CPU share.
- Observations: S3-pipewire-pwtop snapshots (client `BUSY` 3–30 µs per cycle at quanta 441–2 048; sink 4.5–62.6 µs) — graph-thread time only, not the player's decode; S1-cucinotta2011 (JACK period = buffer/rate, 667–2 666 µs, synthetic clients ≈ 7 % CPU each); S1-flautner2000 (mpg123 + esd ≈ 5 % CPU, no period); S1-flautner2001 (esd wakes periodically, qualitative); S3-sysprof-gnome (pulseaudio ≈ 0.19 s CPU in 11 s, estimate, no period).
- Not found: a measured wake period with per-wake CPU of a desktop audio player's path under PulseAudio or PipeWire (S1 §3 T4, S3 §3 T4, S2 §3 T4); anything about Spotify's Linux client (S2-18: no technical documentation).

### 26–27. `video-playback.period`, `burst` (16 667 / 6 667 µs)

- What drives a player's cadence (S2): mpv times frames to the audio clock by default (`--video-sync=audio`), display-refresh modes optional and requiring vsync-blocked presentation; software decode default with up to 16 decoder threads; a "vo" thread (S2-12). VLC: a "vlc-vout" thread waits for clock deadlines with an 80 ms redisplay floor, 4 ms early wake, 20 ms late threshold (S2-15). GStreamer sinks sync to the pipeline clock (S2-13). WebRTC: V4L2 capture thread at the requested rate, fallback 30 fps (15 for ≥ 800 px non-MJPEG), encoder task queue, "default 30fps" averaging window, 1 000 ms idle repeat in screen share, max-framerate constant 60 (S2-16). Zoom documents only "around 5 frames per second" screen sharing on dual-core laptops (S2-17).
- Observations: S1-tsafrir2003/S1-etsion2004 (Xine on Linux 2.4: displayer paced by a 4 ms alarm on the content clock, 39–40 % CPU + X server 20 %, ≈ 470–700 wakeups/s, frame-skip rule; MPlayer 11 %; CPU proportional to viewing scale, 15 % → 60 % at 2:1); S1-flautner2002 (plaympeg idle 22–54 % per clip on a Crusoe laptop); S3-webrtc-internals (2015 Chrome: camera 7–8 fps at 4–14 ms encode per frame; screen share 3 fps); S1-kumar2022 (Zoom/Teams/Meet whole-system CPU 15–35 % sender on Windows 10); S1-chang2021 (Android 150–200 %); S1-macmillan2021 (Ubuntu, FPS only, no CPU); S3-sysprof-gnome (Zoom threads sampled, no cadence).
- Not found: per-frame CPU of mpv, VLC or GStreamer software decode, or per-thread CPU of a Linux conferencing client (S1 §3 T5, S3 §3 T5, S2 §3 T5); IMC 2021 data are request-only (S3-imc21-vca).

### 28–30. `validation_stats`, notes wording, TIMER semantics

- Item 30: interbench skips missed periods (K1); the players found behave likewise — Xine "skips frames that are late by more than half a frame duration" (S1-tsafrir2003), VLC thrashes pictures later than 20 ms (S2-15), WebRTC adapts frame rate (S2-16), GStreamer QoS off by default but sync on (S2-13). No source backlogs late frames.

### 31. Bindings: `spotify`, `zoom` voice → `audio-playback`; `mpv`, `zoom` video, `gamescope` → `video-playback`

- `spotify`: nothing (S2-18). `mpv`: cadence and threads documented (S2-12), no CPU. `zoom`: system requirements only (S2-17); CPU only whole-client on Windows/Android (S1-kumar2022, S1-chang2021). `gamescope`: 9.4's records (S2-09 there) — not re-searched here. Whether a conferencing client is one periodic task at 40 % CPU: the WebRTC thread structure (capture thread, encoder queue, worker and signaling threads, S2-16) is several threads; no CPU-per-frame source.

### 32–33. Registry lines (interbench audio/video; "community")

- No new source; K1's verdicts stand (SUPPORTED numbers; "community" NOT IN SOURCE).

## Not found, all classes

- An input inter-arrival distribution for desktop pointer events per local application (T1): only RDP-side or app-less mouse traces (S3-balabit, S3-dfl).
- An input inter-arrival dataset for code editing with distributions (T1): dataset pointers only (S1-csedm2023, S1-leinonen2019); form filling: no candidate.
- A per-input CPU-time distribution for a Linux text editor, office writer, mail client, browser, image editor or video editor measured after 2004 (T2): the Linux evidence is S1-flautner2000/2001 and S1-tsafrir2003/S1-etsion2004; the only long-window real-use distribution is Windows NT/2000 (S1-lorch2003); Firefox profiles give wall-clock only; VS Code and mpv issue attachments were unreachable (github.com and api.github.com returned 403 through the proxy; GitHub MCP denied for repositories outside this session).
- A scheduler trace (`sched_switch`/`sched_wakeup`) of a Linux desktop session with a focused GUI application (T3): none published; Endo/Seltzer and Flautner trace hosts are gone (redirect; TLS failure and 503); sysprof captures carry perf samples only.
- A measured account of how GTK, Qt, Electron/Chromium or LibreOffice VCL schedule work after an input event (T3): documentation of designs and defaults only (S2-01…S2-08).
- A measured wake period and per-wake CPU of a desktop audio playback path under PulseAudio or PipeWire (T4): defaults only (S2-09…S2-13); pw-top snapshots without workload description (S3-pipewire-pwtop); JACK with synthetic clients (S1-cucinotta2011).
- Per-frame CPU of a software-decoding player or per-thread CPU of a Linux conferencing client (T5): Xine on Linux 2.4 is the only Linux player measurement with CPU share and pacing (S1-tsafrir2003); conferencing CPU exists for Windows and Android only.
- One observation spanning all six application classes bound to `desktop-interactive` (T6); any observation of a video editor's input or wake behaviour.
- Whether a hosted runner has a sound device or `/dev/uinput`, its `perf_event_paranoid`, whether tracefs is mounted, whether Xvfb accepts uinput input (T7, S4 §3).
- Sites unreachable on 2026-09-13: github.com issue pages and `api.github.com` (403 via proxy), gitlab.freedesktop.org wikis and uploads (Anubis challenge; 401/404), freedesktop.org PulseAudio wiki (418), dl.acm.org and deepblue.lib.umich.edu (403), web.eecs.umich.edu (TLS chain failure; Wayback used), cs.huji.ac.il (WAF), epub.uni-regensburg.de (401), ResearchGate (403), buffalo.edu CUBS (403), Zoom support (JS shell; Wayback used), Semantic Scholar search API (429). Paywalled and unread: Blake et al. ISCA 2010, Wong et al. 2008, Wimmer et al. CHI EA 2023, Salthouse 1986, Lee et al. DTJ 1998.
