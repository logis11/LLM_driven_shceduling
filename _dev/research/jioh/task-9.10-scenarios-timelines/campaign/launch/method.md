# Task 9.10 — the launch phases of applications started mid-file: method (2026-10-04)

The observation behind the launch phase an entry runs first when a file starts it mid-file — `c3-workday`, `c3-evening`, `c3-creation`, `c4.variant.yaml`'s `c4-compile` and `c4-gaming` injections and `c6.variant.yaml`'s `c6-fold` call (changelog D21, D30, D132–D135) — run on GitHub-hosted runners under `../../../measurement-campaign-workflow.md`. Amended only by a dated entry in §8. Tooling: `dataset/tools/meas/desktop/` — the `launch-*` subjects of `run.sh`, their sequences in `launch.sh`, the analysis `launch.py`, and `pool.py`'s launch branch — workflow `.github/workflows/meas-desktop.yml`, trigger `.github/campaign-desktop.json`, loop family `desktop`.

## 1. Runs

- **Machine.** The AMD EPYC 7763 only; `machine_gate.sh` stops a job that drew another model before any install or measurement, and a gated job is not a repeat.
- **Tag.** `meas-ci:desktop:<YYYY-MM-DD>`, the launch date of the first batch, lettered if the workflow already has a campaign of that date; each repeat's run id in the pooled record.
- **Repeat.** One job per subject and repeat index: the subject's sequence run twice, the first unmeasured and quit by the program's own command, the second traced (D132, D135). Identical work, so an added repeat is the next index. Artifact `meas-desktop-launch-<subject>-r<k>-<mode>`.
- **Subjects** (D133, D134): each entry's own campaign's launch.

| subject | entry | its campaign's subject | after the window | settle |
|---|---|---|---|---|
| `launch-soffice` | `office-writer` | 9.5's `soffice` | 10 s, Ctrl+End | 30 s |
| `launch-thunderbird-send` | `mail-client` | 9.5's `thunderbird-send` | the compose window opened, its body clicked | 390 s |
| `launch-kdenlive` | `video-editor` | 9.5's `kdenlive` | none | 30 s |
| `launch-mpv-video` | `video-player` | 9.5's `mpv-video` | none | 30 s |
| `launch-mpv-audio` | `audio-player` | 9.5's `mpv-audio` | none | 30 s |
| `launch-element` | `chat-client` | 9.8's `element` | the restored session's first `/sync` | 30 s + 20 s |
| `launch-steam` | `game-client` | 9.8's `steam` | the client's web helpers running | 900 s |
| `launch-chrome` | `web-browser` | 9.5's `chrome` | none | 420 s |
| `launch-chrome-hidden` | `renderer-hidden` | 9.8's `chrome-hidden` | none | 20 s, then the 630 s grace |
| `launch-webrtc` | `video-call` | 9.5's `webrtc`, the call opened in a running Chrome (D134) | Chrome's 420 s, then the call page opened | 210 s from the opening |

- **Modes.** `dry` — the tooling checked on one job per subject at the campaign's lengths, the gate open on any model, never pooled (D135); `full` — the campaign.
- **What is carried.** Fixed after the dry run by 9.6 D7's criterion — the launch phase's form in each entry and the values the stability rule tests — and written into §8 before the first batch. Until then each job records everything in "Recorded per job".
- **First batch.** Repeats 1–5 of each subject, the workflow's floor (`kalibera-ismm13` §11).
- **Validity** (the workflow's step 4, with this job's own checks): the gate open on the EPYC 7763; the version recorded; both launches reaching their window and their post-launch steps; the first launch's tree exiting within 60 s of its quit; the cached fraction of the files the first launch mapped at least 0.99 before the traced launch; the traced tree holding no harness process (`check_tree`); the trace stopped cleanly with no lost events. Per subject: Element's relaunched client signed in (its `/sync` reaching the homeserver); the Steam client running logged out (`steamid` 0); `chrome-hidden`'s renderer gate (13 renderers); the call connected (the page's title reporting encoded and decoded frames); Thunderbird's compose window open.
- **Recorded per job.** The runner spec, pin and kernel; the program's version; each launch's command line, affinity, exec-to-window time and quit time; the mapped files and each one's cached fraction; the traced launch's `perf` timehist, wakeup rows and fork, exec and exit rows; every phase's edges; screenshots after each step; the tree's snapshot at the settle's end.

## 2. Inputs

- **Each subject's campaign's inputs, unchanged** (D133). `probe/appdefs.sh`'s arms `soffice`, `thunderbird-send`, `kdenlive`, `mpv-video`, `mpv-audio`, `chrome`, `chrome-hidden` (12 background tabs, the 100 ms timer page) and `webrtc`; `desktop/run.sh`'s Element (Synapse on the harness CPUs, one account, one room) and Steam client (`steam-installer`, logged out, under openbox). The builds are the runner's or the vendors' at the job, recorded per job beside the entries' builds.
- **The call** (D134). Chrome with the `webrtc` arm's flags on the `chrome` arm's page, `/tmp/page.html`; the call page `probe/webrtc-loopback.html` opened by `google-chrome --user-data-dir=/tmp/chrome-data file://…/webrtc-loopback.html` from the harness CPUs, which hands the address to the running browser and exits.
- **The display.** Xvfb `:99`, 1280×800×24, on the harness CPUs; openbox for the Steam client only (9.8's).

## 3. Phases

Each launch, the first and the traced one alike:

| Step | Length | CPUs | Instruments (traced launch) |
|---|---|---|---|
| launch | to the window, at most 120 s (Element 180 s; the Steam client to its web helpers, at most 900 s) | measured (the application); harness (the rest) | `perf` from 2 s before the exec |
| after the window | the subject's (§1) | the drivers on the harness | `perf` |
| settle | the subject's (§1) | as above | `perf`, stopped at its end |
| quit | the first launch only: its own command, at most 60 s for the tree to exit | harness | none |

The call: Chrome's launch and 420 s untraced in both launches, then the call page opened and 210 s, traced in the second. Between the quit and the traced launch, the warm check.

## 4. Instruments

- `perf sched record -k CLOCK_MONOTONIC -a -e sched:sched_process_exec` on the harness CPUs, stopped by SIGINT at the settle's end; then `perf sched timehist --state`, `perf sched timehist -w` (the wakeup rows), and `perf script`'s fork, exec and exit rows.
- The mapped files: every file-backed mapping in `/proc/<pid>/maps` of every process of the first launch's tree at its settle's end; after the quit, each read whole on the harness CPUs, then `fincore` on each, the fraction the pages cached over the pages.
- For the call, Chrome's threads at the opening, read from `/proc`.

## 5. Analysis rules

- **The tree** (D135). The process the job launched and every descendant by the fork rows; for the call, Chrome's threads at the opening and their descendants. Rows on the measured CPU outside the tree are counted by comm, never folded in.
- **Wakes.** A timehist row is a segment; a segment is a wake when a wakeup row for its thread lies between the thread's previous schedule-out and this schedule-in, else a resume merged into the preceding wake (9.5 follow-ups spec decision 4; 9.7 D21).
- **The phase** runs from the exec (the call: the opening) to the settle's end. Each wake's time from the phase's start, its run, its thread, its process and the process's role (`--type=`) are written out per job.
- **The slice profile.** CPU ms per second and wakes per second per 10 s slice from the phase's start (`task-9.5-interactive-typing/campaign/launch-work.md`'s form).
- **`renderer-hidden`.** The page renderers by `renderers.tsv`'s command lines (D127), the control tab dropped as the fastest renderer (`desktop/analyze.drop_control_tab`); each of the 12 measured renderers its own stream.
- **Also reported.** The exec-to-window time, the steps' times, the phase's length and the tree's CPU over it.

## 6. Scope, written into the files' notes

Runner spec (4 vCPU Azure VM, `ubuntu-24.04`, kernel and CPU model as recorded, the AMD EPYC 7763); each subject's campaign's scope; a warm relaunch after an unmeasured first launch and the program's own quit (D132, D135); each entry's own campaign's launch (D133), the call opened in a running Chrome (D134).

## 7. Release

Raw records per job are released as a GitHub release named in the record at fold-in. The release is outward-facing and is published on 인지오's go-ahead.

## 8. Amendments

- 2026-10-04, dry run #77 (37205258362; the ten subjects, the gate open on any model). LibreOffice and both `mpv` players ran through. Kdenlive, Thunderbird, Chrome and Element stopped at the quit, their trees not ended within 60 s of it, and no job's warm check recorded a fraction. (a) The image lacks `fincore`, as the background family found (run #126): `util-linux-extra` is installed, with `python3-xlib`. The fraction is resident pages over the pages the files span, the background family's reading. (b) Kdenlive took no Ctrl+Q, Chrome no Ctrl+Shift+Q: under Xvfb with no window manager the shortcut did nothing, as the export's dry run #157 found for Kdenlive's Render shortcut. Both are closed by their window's own close, the ICCCM `WM_DELETE_WINDOW` its title bar's close sends (`close_window.py`); closing Chrome's one window ends the browser. (c) Thunderbird's Ctrl+Q went to its compose window and did nothing; it goes to the main window. (d) Element's Ctrl+Q put up its confirmation, "Are you sure you want to quit?", which the job left unanswered; a window the quit puts up is now recorded and given the program's answer, here its right-hand button, "Close Element". (e) `perf` stopped by SIGINT exits 130, as the background family's phases record it; validity reads 130. LibreOffice (EPYC 7763): window 0.56 s after the exec, phase 40.8 s, 1,646 ms of CPU, 1,600 of it in the first 2 s. The video player (EPYC 9V74): 3,764 ms over 30.6 s, 130 ms/s in the first 10 s against 118–124 after. The audio player (EPYC 7763): 453 ms, 31.8 ms/s in the first 10 s against 6.4–7.7 after.
- 2026-10-04, dry run #78 (37205626346; LibreOffice and Kdenlive). LibreOffice's warm check read 1.0000 over 253 files. Kdenlive's close went to the window `wait_window` had found, a secondary top-level titled "Kdenlive", and Kdenlive stayed open. The quit goes to the application's largest visible window, as the export's driver finds Kdenlive's main window (`kdenlive_export.py`'s `find_window`).
- 2026-10-04, dry run #79 (37205972804; Kdenlive). Closed through its main window, "project / HD 1080p 30 fps — Kdenlive", in 2 s; warm 1.0000 over 561 files; window 0.58 s after the exec, phase 30.6 s, 2,207 ms of CPU, 220.5 ms/s in the first 10 s against 0.03–0.09 after.
- 2026-10-04, dry run #80 (37206212175; Thunderbird, Chrome, the hidden tabs, the call, Element), Element's job. Ctrl+Q's confirmation was detected (a 339×81 window) and answered; the tree exited 5 s after the quit; warm 1.0000 over 160 files. The relaunch's window came 1.63 s after the exec and its first `/sync` 3 s after the window; phase 53.7 s, 3,253 ms of CPU, 304 ms/s in the first 10 s and 20.4 ms/s at 30–40 s against 0.15–0.32 otherwise.
- 2026-10-04, what is carried (D136–D138), fixed by 9.6 D7's criterion after the dry runs: each subject's entry gains a launch phase, replayed. Each pooled repeat's streams are written to `dataset/launch/launch-<entry>.json.gz` (`launch_fold_in.py`): the whole tree's wakes, or `renderer-hidden`'s twelve measured renderers', each wake its time from the phase's start, its run and its thread. No value is a distribution, so the stability rule tests no table; the repeats are carried as observed, each repeat's phase length and CPU total reported beside them (D136). The first batch is repeats 1–5 of each subject; the tag `meas-ci:desktop:2026-10-04b`.
- 2026-10-04, dry run #77, the last three jobs. The call opened in the running Chrome connected: its title read `enc=3171 dec=3171 fps=20` after its 210 s (D134). The hidden-tab launch held 14 renderers at the gate, against 13 wanted. Both stopped at Chrome's Ctrl+Shift+Q, amended above. The Steam client, logged out, sat at its sign-in window; `steam -shutdown`, run as a second `steam`, left the client's 13 processes running. Its quit becomes its main window's own close, with `steam -shutdown` sent 30 s after it if the client still runs, the one that ended it recorded; its wait is 120 s. The Steam client's first job of the campaign stands as this amendment's check: a full job on the EPYC 7763, a repeat if it holds.
