# Reader input — task 9.10 scenarios and timelines, stage 2 search

Given to each class reader verbatim. Readers do not see the repository's current values.

The subject is how real desktop computers are used and composed, situation by situation: which applications and processes run together, in what order, how many, for how long, under which process names, and what starts in the background without the user. The situations are: office work (a word processor, a browser, a mail client), web browsing, email, software development and compiling, local ML training or inference, photo editing, video editing, rendering and transcoding, backup and archiving, file indexing, malware scanning, gaming (Steam, native or Proton), media playback, video calls, and an idle logged-in session. A candidate may cover any number of situations; record which.

Every candidate's platform (OS, version), population (who, how many), year and collection method is recorded. Nothing is excluded for being on another OS, from another year, or self-reported — say which it is.

## Topics

- **T1 Application co-occurrence.** Logged or traced observations of which applications and processes run at the same time on real desktop computers (any OS; Linux preferred), per activity where available: how many applications are open, which combinations occur during office work, browsing, email, software development, gaming, media playback and video calls, and what runs in the background during them. Record population, OS, year, logging method, and whether process names are given.
- **T2 Focus and switching.** Observations of foreground-application sequences: dwell time per application or window, switch rates, sequences across applications, and session lengths, with distributions where published; logged data sets that contain window-activation or focus events with application names and timestamps.
- **T3 Activity order.** Observations or documented workflow definitions of the order in which desktop activities follow one another in a session (e.g. searching, writing, building software, sending mail; editing photos, editing video, exporting) — including benchmark suites' own workload orders, and whether any observation of real users supports an order.
- **T4 Browser windows, tabs and processes.** Logged numbers of browser windows, tabs and distinct sites per session; how many renderer processes Chromium-based browsers run on Linux for a given set of tabs and sites (documentation, source, measurements); how often a user loads a page or switches tabs per minute of browsing.
- **T5 Gaming session composition on Linux.** What processes run on a Linux desktop while a game runs through Steam (native or Proton): the Steam client and its helpers and their state, a compositor (gamescope or the desktop's), overlays, voice-chat clients available on Linux; the number and names of a Proton game's processes and threads; whether and how the Steam client downloads or updates while a game is running on Linux (defaults, documentation, observations).
- **T6 Unrequested background jobs on stock Linux desktops.** What distributions and desktop environments start without the user: timers and services enabled by default (antivirus scans, signature-database updates, file indexers, `updatedb`, package-database backups, update checks, DKMS rebuilds on kernel updates), their process names by distribution and version, how often they run and for how long; for DKMS, how many objects a typical out-of-tree module (e.g. an NVIDIA, VirtualBox, ZFS or Wi-Fi module) compiles and how long an autoinstall takes.
- **T7 Size of user-started jobs.** Observed or documented typical sizes and durations of batch work users start on desktops: builds of a software project (objects per build, build times), video render and transcode lengths, backup runs (first vs incremental, data sizes), archive creation, ML training jobs on a desktop CPU; and the relation of a typical project build's size to a Linux kernel build.
- **T8 Session baseline.** Which session and system processes a stock desktop runs at idle and in use, by distribution and session type (GNOME/KDE, Wayland/X11): display-server presence (Xorg, Xwayland), compositor and shell, audio-stack processes, message-bus implementation and instances, per-user service manager, other always-on services — names as they appear in `/proc/<pid>/comm`.
- **T9 Operations within applications.** How often users perform heavy operations inside an application — applying an image filter, rendering a video-editor preview, loading a web page, sending an email with or without attachment — per minute or per session of use, and whether they happen while the user is interacting or idle.
- **T10 Application launches within a session.** How often applications are started during a session, and how long launch work takes on Linux (CPU and wall time until the application settles).
- **T11 Video calls and media.** Process structure of Linux video-conferencing clients (Zoom, Teams, browser-based) during a call; whether users play music and video at the same time, or media alongside other work.
- **T12 Public traces of desktop process activity.** Public data sets or traces recording desktop process creation, execution or foreground state with process names and timestamps (any OS): population, time span, licence and access — security-telemetry sets, HCI logging sets, energy or mobile data sets that record several running applications, OS-vendor telemetry publications.
- **T13 CI observability.** What a GitHub Actions hosted runner (ubuntu-24.04, 4 vCPU, no GPU, no display) can observe of a desktop situation: running a full desktop session (GNOME or KDE under Xvfb, headless or nested) and listing the processes and default timers it starts; listing default-enabled systemd timers and services of distribution images (Ubuntu, Fedora, Arch; containers or VMs); building a real DKMS module and counting its compiled objects and duration; and what it cannot observe (real users, real GPUs and displays, a real game session, a logged-in Steam client).

## Classes

- S1 — peer-reviewed and preprint literature (T1–T4, T6, T7, T9–T12; HCI, systems, measurement, security venues).
- S2 — primary project and vendor documentation and source code (T4, T5, T6, T8, T10, T11; distribution packaging, systemd units, upstream source, vendor support pages).
- S3 — public traces and datasets (T1, T2, T4, T5, T7, T9, T12; data repositories, trace archives, public logs, bug-tracker and forum attachments that are data).
- S4 — own measurement on a CI runner (T13, and what a runner can contribute to T5, T6, T8, T10).

## Record format

Each reader writes `search/S<k>-<class>.md`:

1. **Search log** — one row per query: date, engine or venue, exact query terms, hits followed, dead ends with the HTTP status.
2. **Candidates** — per candidate: a provisional id `S<k>-NN`; full citation; copy read (URL or commit, version, date accessed, local path under `../sources/<id>/`, SHA-256 of the fetched file); verbatim passages with locators (page, section, table, slide, `file:line` at a commit); coverage per topic T1–T13 — covers (naming the object, unit, statistic, scope and population) or does not cover; whether it is one observation (one population, trace or run) and whether machine or platform, subjects and window are named.
3. **Not found** — each topic with no candidate, with the searches that established it.

Source copies go to `_dev/research/jioh/task-9.10-scenarios-timelines/sources/<id>/` (gitignored; it will not survive this clone). The record must be self-sufficient: everything a reader needs is in the quoted passages and the copy identification, never "see the local file". Verbatim means verbatim; a passage that cannot be quoted is not a passage.
