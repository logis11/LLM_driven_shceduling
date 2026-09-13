# Handoff — task 9.5 Interactive and typing, stages 1–2 (research routine, 2026-09-13)

Stages 1 and 2 of `_dev/research/jioh/research-slice-workflow.md` are done on `jioh/dataset-rebuild`; stage 3 (decisions) is 인지오's. Issue #8.

## Files

- `_dev/research/jioh/task-9.5-interactive-typing/scope-card.md` — 33 items: `desktop-interactive` (params 1–9, structure and bindings 10–18, registry lines 19–23) and, by this run's boundary assumption, `audio-playback` and `video-playback` (24–33).
- `…/search/input.md` — topics T1–T7 in neutral form, classes, record format.
- `…/search/S1-literature.md` (27 sources read), `S2-project-docs.md` (20 candidates, 20 shallow clones), `S3-traces-datasets.md` (19 entries, computations labelled), `S4-ci-observability.md` (25 candidates).
- `…/search/candidates.md` — observations that exist, per-item findings, not-found across classes.
- Source copies under `…/sources/` were local to the routine's clone and are gone; every record is self-sufficient (URL or commit, SHA-256, verbatim passages with locators).

## Boundary assumption to confirm first

The routine took `audio-playback` and `video-playback` into 9.5 because the library files them with `desktop-interactive` under one interbench family header and no other slice name covers them. If they belong elsewhere, items 24–33 and topics T4–T5 move with them; nothing else on the card depends on them.

## The one-observation situation

No single observation covers `desktop-interactive`. The archetype is a montage: wake gaps from two typing studies (Roeser's LF-bigram parameter set sits under Dhakal's tag), CPU per wake from interbench's timer-driven window-drag emulation, and the coupling of burst to gap ours. What the search found:

- **Gaps.** Two observations with raw data that could each ground the whole gap parameter alone: the 136M Keystrokes dataset (S3-aalto136m; keystroke-level p50 171 ms, p90 396, p99 934 in a six-participant sample; transcription; non-commercial licence) and Roeser's OSF `ct.csv` (S3-osf-y3p4d; 1 662 subjects, per-component IKIs, CC0). Free-composition alternatives with pauses retained: SWELL-KW (S3-swell-kw, Word/Outlook/IE per keystroke, Windows 2012) and Chukharev-Hudilainen's ex-Gaussian chat fits (S1-chukharev2014). Free-text distribution shape: log-logistic best, log-normal second (S1-gonzalez2021).
- **CPU per input.** No Linux observation newer than 2004. The candidates are Lorch & Smith's VTrace study (S1-lorch2003: eight Windows NT/2000 users over months; per-event CPU CDFs; UI events 20 % of CPU, timers 35 %; applications differ significantly), Flautner's interactive-episode traces (S1-flautner2000/2001: six Linux X11 apps; keystroke echo sub-millisecond; per-application episode buckets), Etsion/Tsafrir's klogger traces (S1-tsafrir2003/S1-etsion2004: Emacs at 8 char/s ≈ 0.2 % CPU, OpenOffice 2.6 %, quanta well under 10 ms), and Firefox Profiler profiles (S3-firefox-profiles: wall-clock per-keypress 4–55 ms on Linux Firefox 70–85, no CPU deltas). All contradict the compiled editors' 74–96 ms bursts on 90–96 % of keystrokes.
- **Wake structure.** Every observation and every toolkit document says GUI wakeups are not input-only: timer messages exceed UI messages in CPU share (S1-lorch2003), cursor blink (1 200 / 1 000 / 500 ms), autosave, spell timers, refresh-driver ticks at ~16.7 ms when painting, compositor frame callbacks (S2-01…S2-08, S3-firefox-profiles, S3-sysprof-gnome).
- **Audio and video.** No observation of a desktop audio player's wake period with per-wake CPU; PipeWire's default period is 21.3 ms (1 024 at 48 kHz), PulseAudio's adaptive with a 10 ms minimum sleep (S2-09, S2-10); pw-top snapshots show client `BUSY` of 3–30 µs per cycle (S3-pipewire-pwtop). Video: Xine on Linux 2.4 is the only player measurement (4 ms content-clock pacing, ≈ 40 % CPU + X 20 %; S1-tsafrir2003); mpv times to the audio clock by default (S2-12); conferencing CPU exists only whole-client on Windows and Android.
- **Own measurement.** A runner can drive VS Code under Xvfb (VS Code's own CI does, S4-09), browsers, LibreOffice through its UI-test framework, mpv with null audio; `perf sched timehist` gives per-schedule run time and wake gaps (root; S4-17, S4-25). It cannot observe display refresh, device audio timing or GPU work, and per-key interval replay is documented only via xdotool script sleeps or evemu-play (S4-05, S4-07). Whether the runner has `/dev/uinput`, a sound device, or a permissive `perf_event_paranoid` is not established by any document.

## Stage 3's first question

Whether `desktop-interactive` keeps one archetype for six applications at all, or splits — every observation found says applications differ by an order of magnitude in CPU per input, and none covers a video editor — and, under decision 2, which single observation grounds the gap side (136M Keystrokes raw data; Roeser's CC0 data; SWELL-KW with pauses) given that no observation grounds gap and CPU together. Only after that: whether the CPU side is re-sourced from a runner measurement (a `perf sched` capture of an editor under replayed intervals, S4) or from the 2000–2004 literature.

## Flags from the readers

- Unreachable on 2026-09-13: github.com issue pages and `api.github.com` (403 through the proxy; the GitHub MCP is scoped to this repository), so VS Code typing-latency `.cpuprofile` attachments and mpv issue bodies were not read; gitlab.freedesktop.org wikis and uploads (Anubis / 401 / 404); freedesktop.org PulseAudio wiki (418); dl.acm.org (403); web.eecs.umich.edu (TLS; Wayback used); Zoom support (JS shell; Wayback used).
- Paywalled and unread: Blake et al. ISCA 2010 (desktop TLP), Wong et al. 2008, Wimmer et al. CHI EA 2023 (X11 toolkit latency), Salthouse 1986.
- Request-only datasets: Clarkson II, Buffalo CUBS, IMC 2021 conferencing data.
- S3's numbers are the reader's own computations on samples (six of 168 593 participant files; one of 919 SWELL files); they locate candidates, they are not values.
