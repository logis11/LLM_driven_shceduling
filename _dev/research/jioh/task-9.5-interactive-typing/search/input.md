# Reader input — task 9.5 interactive and typing, stage 2 search

Given to each class reader verbatim. Readers do not see the repository's current values.

## Topics

- **T1 Input inter-arrival.** Observations of the time between successive input events reaching a desktop application during real use — keystrokes and pointer events — as distributions, not only means: by task (free composition, transcription, code editing, form filling), including pauses between bursts of typing; public datasets carrying raw per-event timestamps, their populations, tasks, and licences.
- **T2 CPU per input.** Observations of the CPU work a desktop application performs per input event (keystroke echo, redraw, reflow): per-wake CPU-time distributions for text editors or IDEs, office suites, browsers, mail clients, image and video editors, preferably on Linux; how that work relates to the interval before the event; how often one event's work exceeds 1 ms, 10 ms, 100 ms.
- **T3 Wake structure of a focused GUI application.** Whether a GUI application's wakeups are input-driven only or also timer-, compositor- or frame-callback-driven (repaint cadence, cursor blink, autosave, language servers, spell-check); how its threads are organised (UI thread vs render, worker, IO threads); per-schedule runtime and wake-gap distributions of such applications in scheduler traces; how a toolkit (GTK, Qt, Electron/Chromium, LibreOffice VCL) schedules work after an input event.
- **T4 Audio playback cadence.** Observations or primary documentation of the wake period and per-wake CPU of an audio playback path on a Linux desktop: player thread, PipeWire or PulseAudio server quanta and default buffer or period sizes, ALSA period sizes; whether any documented default or trace matches a fixed wake interval with a fixed CPU share, and what values.
- **T5 Video playback and conferencing cadence.** Observations or primary documentation of the frame cadence and per-frame CPU of a software-decoding video player (mpv, VLC, GStreamer) and of a video-conference client's capture, encode and decode threads on a Linux desktop; what drives the cadence (content frame rate, display refresh, presentation timer); CPU share per frame period as measured.
- **T6 Application classes.** Whether any observation distinguishes the input inter-arrival, CPU per input or wake structure of a text editor, an office writer, a mail client, a browser, an image editor and a video editor from one another — evidence for or against one behaviour model serving all six.
- **T7 CI observability.** Whether a GitHub Actions runner can drive a GUI application (a code editor, LibreOffice Writer, a browser, GIMP, Kdenlive, mpv, an audio player) under Xvfb with synthetic input replayed at recorded inter-key intervals (xdotool, ydotool, Playwright, LibreOffice macros), and what a `/proc` sidecar or `perf sched` could observe of per-wake CPU, thread population and wake gaps; what it cannot (real display refresh, an audio device's timing, human pauses).

## Classes

- S1 — peer-reviewed and preprint literature (T1–T6).
- S2 — primary project and vendor documentation and source code (T3, T4, T5; T1 and T2 where a project documents its own measurements).
- S3 — public traces and datasets (T1–T5).
- S4 — own measurement on a CI runner (T7).

## Record format

Each reader writes `search/S<k>-<class>.md`:

1. **Search log** — one row per query: date, engine or venue, query terms, hits followed, dead ends (with the HTTP status).
2. **Candidates** — per candidate: a provisional id; full citation; copy read (URL or commit, version, date accessed, local path under `sources/<id>/`, SHA-256); verbatim passages with locators (page, section, table, `file:line` at a commit); coverage per topic T1–T7 — covers (naming the object, unit, statistic, scope and population) or does not cover; whether it is one observation (one population, trace or run) and whether machine, application, subject and window are named.
3. **Not found** — topics with no candidate, with the searches that established it.

Source copies go to `sources/<id>/` (gitignored; the folder will not survive this clone, so the record must be self-sufficient — every fact a reader needs is in the quoted passages and the copy identification, never "see the local file"). Verbatim means verbatim; a passage that cannot be quoted is not a passage.
