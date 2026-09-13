# Reader input — task 9.4 gaming, stage 2 search

Given to each class reader verbatim. Readers do not see the repository's current values.

## Topics

- **T1 Frame cadence.** For a game running through Proton on a Linux desktop or Steam Deck: what governs the frame period (display refresh, frame limiter, uncapped), what values are documented or observed, and whether any observation ties the frame cadence to the game's task wake structure.
- **T2 Task structure.** Any observation (trace, dataset, paper, tool output) of a Linux game's process and thread population: counts, which threads are the game's and which are Wine/DXVK/audio components, how they wake one another, and per-schedule runtime distributions. Includes the roles of `wineserver`, `dxvk-cs`, `dxvk-submit`, `winepulse_*` as their projects document them.
- **T3 Non-dominant tasks.** Any observation of what the tasks outside the most frequently scheduled set do (periodic, sleeping, terminated), with numbers.
- **T4 Lifetime and termination.** Any observation of how many of a game's tasks terminate during play and over what window.
- **T5 Platform of the LAVD characterisation.** Whether any document (later talks, LWN article 1051430, the sched-ext/scx repository, a "Lessons from creating a gaming-oriented scheduler" talk or paper) states the machine, core count or game behind the task-characterisation slides (12–14) of Changwoo Min's talk "Optimizing Scheduler for Linux Gaming", Open Source Summit North America 2024, slides at static.sched.com/hosted_files/ossna2024/9b/scx-lavd-oss-na24.pdf.
- **T6 CI observability.** Whether a GitHub Actions runner can run a game at all: an open-source native Linux game under Xvfb with software rendering, or Proton without a GPU; what a `/proc` sidecar could observe of it (thread population, wake gaps, per-schedule CPU), and what it cannot (the Proton/Wine structure, real frame cadence).

## Classes

- S1 — peer-reviewed and preprint literature (T1–T5).
- S2 — primary project and vendor documentation and source code (T1, T2, T5).
- S3 — public traces and datasets (T1–T4).
- S4 — own measurement on a CI runner (T6).

## Record format

Each reader writes `search/S<k>-<class>.md`:

1. **Search log** — one row per query: date, engine or venue, query terms, hits followed, dead ends.
2. **Candidates** — per candidate: a provisional id; full citation; copy read (URL or commit, version, date accessed, local path under `sources/<id>/`, SHA-256); verbatim passages with locators (page, section, slide, line); coverage per topic T1–T6 — covers (naming the object, unit, statistic, scope and population) or does not cover; whether it is one observation (one population, trace or run) and whether machine, game and window are named.
3. **Not found** — topics with no candidate, with the searches that established it.

Source copies go to `sources/<id>/` (gitignored). Verbatim means verbatim; a passage that cannot be quoted is not a passage.
