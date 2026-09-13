# Reader input R11-focal-plain

## focal-arxiv26
### Bibliographic entry
- cite: Yin, H., Wen, Z., Cao, J., Yuan, B., & Yang, R. (2026). FOCAL: Filtered On-device Continuous Activity Logging for Efficient Personal Desktop Summarization. arXiv:2604.19541 (v2, 2026-07-18). **Preprint — no venue.**
### Topics
- C-focal-1: in the FOCAL paper's DesktopBench description, the interruption split — number of sessions, the structure of a session, what the primary and interrupting activities are.
- C-focal-2: the multitask split — number of sessions, number of templates, and what fields each recorded action carries.
- C-focal-3: how DesktopBench sessions were produced (recorded natural use vs constructed from another dataset) and from which dataset.
- C-focal-4: where DesktopBench is released, its version, the data licence terms and the script licence; whether per-action timestamps are included.
- C-focal-5: authors, title, arXiv number, version and date, venue status.

## videogui-arxiv24
### Bibliographic entry
- cite: Lin et al. (2024). VideoGUI. arXiv:2406.10227.
### Topics
- C-videogui-1: the VideoGUI paper's identity and whether DesktopBench derives from it.

## plain
### Bibliographic entry
- (no single source; see topics)
### Topics
- C-plain-1: Chromium's documented process model — which processes a browser session runs, how renderer processes map to tabs or sites, and their process name on Linux.
- C-plain-2: whether ClamAV packages ship a scheduled scan by default (timer/cron) and which process performs it (clamscan, clamd, freshclam).
- C-plain-3: whether GNOME ships tracker-miner-fs(-3), KDE ships baloo_file, and plocate ships an updatedb timer enabled by default; the process names each runs under.
- C-plain-4: the executable/process name Jellyfin uses for transcoding on Linux (and whether it ships a renamed build).
- C-plain-5: for scheduled/automatic ML training, media rendering, transcoding and backup jobs that distributions or vendors start without the user, the process names they run under.
- C-plain-6: the process names under which Windows games run through Proton/Wine on Linux, and whether all game threads/processes share one name.
- C-plain-7: whether public traces of desktop process activity with process names exist; what process-identity fields Azure/Google cluster traces carry.
- C-plain-8: what Phoronix Test Suite and UnixBench measure; whether mobile app-usage datasets record concurrent foreground apps.
- C-plain-9: examples of peer-reviewed papers citing these tools by repository URL.
