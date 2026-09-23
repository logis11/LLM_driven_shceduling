# Task 9.10 — candidates per scope-card item

Stage 2 result. Each item group of `../scope-card.md` with the candidates the four class records found (`S1-literature.md`, `S2-project-docs.md`, `S3-traces-datasets.md`, `S4-ci-observability.md`), what each covers, and what no class found. Candidate ids are the records' own; the figures below are quoted from those records, which carry the passages, locators and copy identification. Nothing here decides a value.

## Observations that exist

Observations (a population, trace or run with numbers), as distinct from documentation. None is of a Linux desktop's full process set by activity.

| Id | What | Platform / population / window | Kind of data |
|---|---|---|---|
| S3-01 = S1-16 (SWELL-KW) | raw uLog computer-interaction logs, all 76 files opened | Windows lab laptop, Office 2010 + IE; 25 students and interns; Sept 2012; three ~45 min blocks each (neutral, time pressure, email interruption); CC BY-NC-SA 4.0, open | window-activation, process-start, URL-change events with application names and timestamps; S3 computed per-block switches (median 2.89/min, 1.95 filtered), median dwell 4.6 s (9.1 s per app visit, filtered), IE page loads 4.1 per focused minute, 68 email sends (interruption condition only); background starts seen: dllhost, SearchProtocolHost, splwow64, wuauclt |
| S3-04 = S1-17 (BEHACOM) | per-minute foreground executable, active-app count, app changes, processes of the current app | own PCs of 12 men (Spain/Italy), Windows and Debian-based Linux (article: 8 Windows, 3 Linux, 1 both; executable names suggest 5 with Linux), 20 Nov 2019 – 14 Jan 2020; 167,058 minutes; CC BY 4.0 | 90.6 % of minutes with no foreground change, mean 0.17 changes/min; Chrome 10–24 processes per user while in front; gaming minutes on Windows (CS:GO, League of Legends) with Steam, TeamSpeak; Linux foreground sets (firefox, soffice.bin, thunderbird, evince, gnome-terminal-server, plasmashell, kdenlive, spotify) |
| S3-02 (Test Pilot "A Week in the Life of a Browser" v2) | event dumps from the Wayback Machine | Firefox 3.5–4.0b, Nov 2010, ~26,000 volunteers, 159 on Linux; CC BY 3.0 | per-user median 2 tabs, weekly maximum 8 tabs and 3 windows; 78 % of samples one window; 40 tab opens/closes per user-day; Linux users median 5 tabs, max 14; no page-load or tab-switch events |
| S1-09 (Reis et al., USENIX Security 2019) | Chrome field telemetry | Chrome 69 on Windows desktops/laptops, 2 weeks from 2018-10-01, opted-in users (count not given) | p50 6.0 unique sites and 6.2 renderer processes (4.4 without Site Isolation); p99 41.9 sites, 52.7 renderers |
| S1-01 (Hutchings et al. 2004, VibeLog) | window-activation logs | 39 staff of a research organisation, Windows XP, 2004 | median window activation 3.77 s; ≥ 8 windows open 78.1 % of the time |
| S1-03, S1-13, S1-21, S1-24, S1-14 (Mark, Iqbal, Czerwinski et al.; Iqbal & Horvitz; Tak et al.) | application-switch logging | Windows (XP/7) knowledge workers: 32 (2014), 40 (2016), 27 Microsoft staff (2007), 9 users (2009) | switches/day (661 Monday vs 391 Friday; mean 219), median focus 40 s, 77 email checks/day, mean session 2 h 17 min |
| S1-05, S1-02 (Meyer et al. 2017, 2014) | developer activity logging / observation | 20 developers, Windows 7–10; 11 developers observed | 15.8 apps used per day, top-10 app shares, 0.3–2 min per activity; 47 activity switches per hour and activity-to-activity transition shares |
| S1-06 (González & Mark 2004) | shadowing | 14 information workers | ~3 min per event |
| S1-07, S1-08, S1-31 (Weinreich et al.; Huang & White; Kumar & Tomkins) | browsing logs | 25 users 2004/05; >50 M users June 2009; Yahoo toolbar March 2009 | mean 2.1 windows+tabs, median page stay 9.4 s; parallel-browsing shares; median session 17 pageviews in 16 min |
| S1-12 (Amann et al. 2016) | IDE interaction logs | 27–84 Visual Studio developers, 2015 | 13.4 builds per developer-day |
| S1-25 (Cao et al. 2021) | meeting telemetry | Microsoft staff, 2020 | email sent in ~30 % of Teams meetings |
| S1-11, S1-15 (Joo et al. FAST'11; Ryu et al. FAST'23) | launch-time benchmarks | Linux lab machines (Fedora 12, one named PC) | mean cold start 2.4 s; lab benchmark, not users |
| S3-11 (OpenBenchmarking timed compilation) | public PTS uploads, 2024–2026 | opt-in uploads, mostly many-core CPUs | build time relative to a Linux 7.0 defconfig build on the same CPU: FFmpeg 0.67, PHP 1.06, Godot 3.0, LLVM 3.4, Node.js 4.6, GCC 17.6 |
| S3-10 (Debian popcon, 2026-09-22) | install counts | ~290,000 opt-in installs, servers and desktops mixed | dbus-daemon 238,934 vs dbus-broker 612; pipewire 107,233; dkms 42,552; clamav-freshclam 11,359; gamescope 1,351 |
| S3-09 (Steam survey Aug 2026) | platform share | Steam users | Linux 3.90 % |
| S3-05 (DARPA OpTC) | endpoint process telemetry | 500 of 1,000 Windows 10 VMs, 17–25 Sept 2019; 80-minute fragment of one host read | process creates with image names; user activity scripted (Selenium, Office automation); background jobs real (Defender signature updates, Windows Search, GoogleUpdate) |
| S3-08 (gamemode issue #457) | one `ps` tree of a running Proton game | Arch Linux, Flatpak Steam, Worms Armageddon, Jan 2024; one machine | 15 processes in the game container (bwrap, pressure-vessel, python3, steam.exe, wineserver, services.exe, 2× winedevice.exe, plugplay.exe, svchost.exe, conhost.exe, explorer.exe, rpcss.exe, tabtip.exe, WA.exe) and 13 on the client side (steam, steamwebhelper ×n); read through WebFetch, not byte-verified |
| S3-13 = S1-30 (Carat) | running apps per sample | Android, 2014–2018 | median 52 running packages per sample (mobile) |
| S4-16 (local check, not a runner) | DKMS builds against the runner's kernel headers (6.17.0-1022-azure, gcc-13) in a 4-vCPU container | this session's container | v4l2loopback 1 object, 2.6–2.8 s; nvidia-580-open 214 objects + 2 prebuilt blobs → 5 `.ko`, 72.8 s wall, 216.6 s user CPU; zfs-dkms 2.2.2 fails (kernel ≤ 6.6) |
| S4-08, S4-10 (local checks, not a runner) | default-enabled timers from distribution packages | Ubuntu 24.04 apt closure of ubuntu-desktop + minimal + standard (1,572 packages); Arch packages | 22 timers across 16 packages on Ubuntu (apt-daily, man-db, dpkg-db-backup, fwupd-refresh, fstrim, snap-repair, ua-timer …); Arch ships some timers pre-linked despite `disable *` |

Everything else is documentation or source (S2-01…S2-26, S4-01…S4-07, S4-09, S4-11…S4-15), grey literature (S1-27, S1-33), studies without process data (S1-10, S1-22, S1-23, S1-26, S1-28, S1-29, S1-32), or unreachable or restricted data (S3-03, S3-06, S3-14).

## Per item

### A. Arc order and composition (items 1–9)

- **Order (items 1–3).** No observation of real users supports an order of desktop activities across applications (S1 Not found T3; S3 Not found). What exists: benchmark-defined orders — PCMark 10's workload order (S1-27), CpsMark+ (already read in the verification); activity-to-activity transition shares for developers (S1-02, observer-coded, 11 developers); SWELL-KW's sequences are within three scripted task blocks on Windows (S3-01). No candidate covers photo → video → export by real users.
- **Lengths and focus (items 4–5).** Dwell and switch observations: SWELL-KW median dwell 4.6 s / 9.1 s per app visit, 2.89 (1.95) switches/min (S3-01); VibeLog median activation 3.77 s (S1-01); median focus 40 s (S1-13/S1-21); BEHACOM 90.6 % of minutes without a foreground change (S3-04); session length 2 h 17 min (S1-24); González ~3 min per event (S1-06). All Windows except BEHACOM's Linux users; units differ (window activation, app focus, per-minute aggregate). File length is design (decision 3).
- **Co-occurrence (items 6–7, 9).** BEHACOM gives per-minute active-application counts and current + penultimate foreground application (not the full running set; `active_apps_average` definitions differ by collector: median 31 for one Linux user, 2–9 for others) (S3-04). SWELL-KW process starts give Windows background processes during office work (S3-01). S1-01: ≥ 8 windows open 78.1 % of the time (Windows XP). No observation of concurrent video + music, or gaming + compiling (S1 Not found T11; S3 Not found).
- **Meeting (item 8).** Zoom 7.2.1 `.deb` ships ZoomLauncher, zoom, ZoomWebviewHost, aomhost, cpthost; which run during a call is not documented (S2-23). Teams is "no longer supported on Linux" — a Teams call is a browser (S2-22). S1-22 (IMC 2021) measures conferencing clients' network/CPU, not process structure. S1-25: email during 30 % of meetings (Windows telemetry).

### B. Gaming (items 10–17)

- **Game process and thread names (item 10).** Steam Linux Runtime documents the chain steam-launch-wrapper → reaper → entry point → bwrap/pv-adverb → Proton (S2-18); Proton adds wineserver, steam.exe shim, services.exe, winedevice.exe; Wine sets `comm` from Windows exe and thread names (SetThreadDescription) (S2-19, Wine 11.18 / Proton 11.0). One process tree of a running Proton game: 15 processes in the container (S3-08, not byte-verified). No thread counts in any class. 9.4's handed references (scx #234, #296) could not be re-read: GitHub returned 403 to this session (S3 §unreachable).
- **Steam client beside a game (item 11).** S3-08: `steam` + steamwebhelper tree on the client side during play (one machine). S2 Not found: helper processes during play (steamwebhelper, gameoverlayui) documented nowhere.
- **Compositor (item 12).** gamescope is opt-in on a desktop (S2-20 README); popcon 1,351 installs (S3-10).
- **Voice chat (item 13).** Discord's overlay is Windows-only (S2-21, Zendesk API copy). BEHACOM shows TeamSpeak beside CS:GO on Windows (S3-04). No Linux observation.
- **Downloads during play (item 14).** Valve FAQs 4F9E and 71AB were read this time (S2-17): downloads pause by default when a game launches. No observation of the Linux client downloading during play (S3, S4 Not found). SteamCMD anonymous login installs dedicated servers only; one account can be logged in once at a time (S4-11).
- **Download process name (item 15).** No class found the process performing downloads on Linux.
- **Size and state (item 16); `lane_share` (17).** Not searched as realism (17 is design); no candidate for download sizes during play.

### C. Browsing and renderers (items 18–22)

- **Renderer counts (item 18).** Chrome 69 Windows field telemetry: p50 6.0 sites / 6.2 renderers, p99 41.9 / 52.7 (S1-09). Chromium main 156 on Linux: site-per-process, spare renderer, soft limit clamp(RAM_MiB/2/85, 3, RLIMIT_NPROC/2), removed by a default-enabled feature at that commit (S2-15). BEHACOM: Chrome 10–24 processes per user while in front (all Chrome processes, not renderers only) (S3-04). No Linux renderer-count observation.
- **Windows and tabs (item 19).** Test Pilot v2 dumps: per-user median 2 tabs, weekly max 8 tabs and 3 windows, 78 % of samples one window; Linux users median 5, max 14 (S3-02). Dubroy: tabs per navigation, max 42 (S1-04/S1-33). Weinreich: mean 2.1 windows+tabs (S1-07). Firefox defines max-tab/max-window telemetry but the Public Data Report publishes none of it (S2-16, S3-03).
- **Focused page renderer (item 20).** Page loads: SWELL-KW IE 4.1 per focused minute (S3-01); median page stay 9.4 s (S1-07); 17 pageviews in 16 min (S1-31).
- **Tab-count registry lines (item 21).** Chang et al. CHI 2021 still unreachable (ACM 403, project page 502; S1 §5).
- **VS Code helpers (item 22).** Not found.

### D. Mail and operations (items 23–26)

- **Send (items 23–24).** SWELL-KW: 68 sends, all in the email-interruption condition (S3-01); 77 email checks/day (S1-21); email in 30 % of meetings (S1-25). No observation of send frequency in natural Linux use.
- **Operations (item 25).** Page loads (above). Builds: 13.4 per developer-day in Visual Studio (S1-12). ingimp (S1-10) logged GIMP usage but the record found no per-minute filter rate. No observation of preview renders.
- **Launch work (item 26).** Launch frequency per session: not found in any class. Launch time on Linux: lab benchmarks only (S1-11 mean cold start 2.4 s; S1-15); one developer's gnome-software startup profile (S2-24); a launch measurement method (S4-12, Talos ts_paint). BEHACOM's `update-manager` foreground minutes show a stock updater prompting on Linux (S3-04).

### E. Compile and batch jobs (items 27–35)

- **`spawn_count` and build size (item 27).** Relative build times per project against a kernel defconfig build (S3-11: FFmpeg 0.67 … GCC 17.6). CI build durations (S1-23, not desktop). No object counts per desktop build in any class.
- **Child names (item 28).** `comm` truncation to 15 characters (S2-11).
- **Warm/cold (item 29).** Not found.
- **DKMS (item 30).** Mechanism: kernel-install hook and `dkms.service` run `dkms autoinstall` with `make -j$(nproc)` (S2-09, dkms 3.4.3); Fedora presets enable `dkms.service` and `akmods` (S2-05, S4-09); Arch runs DKMS rebuilds in pacman hooks (S2-07); Ubuntu reruns the autoinstaller from `/etc/kernel/postinst.d` (S4-08). Object counts from Kbuild lists: v4l2loopback 1, vboxdrv 10, Realtek 88x2bu 175, NVIDIA open kernel-interface 198 C files, ZFS ≈306 (S2's estimate) (S2-10). Measured in this container against the runner's headers: v4l2loopback 1 object 2.6–2.8 s; nvidia-580-open 214 objects, 72.8 s wall, 216.6 s user CPU (S4-16, local check, not a runner). Install base: dkms 42,552 popcon installs (S3-10). A public workflow builds and loads a DKMS module on ubuntu-24.04 (S4-13).
- **`total_work` (item 31).** Backup workloads (S1-28, Data Domain backup systems, not desktops), vbench transcode set (S1-29, clip lengths); no desktop job sizes.
- **P1 pair, ml-train stand-in (items 32–33).** Not found: no observation of desktop ML training.
- **Backup (item 34).** S1-28 (first vs incremental on backup servers). No desktop backup observation.
- **Everyday indexer (item 35).** Indexer units and names: tracker-miner-fs-3 up to 3.7, LocalSearch `localsearch-3` from 3.8 (Sept 2024) (S2-04, S2-08, S2-25); tracker-miner-fs enabled as a user service on Ubuntu 24.04 (S4-08); baloo on KDE (S2-04). No observation of an indexer's everyday activity.

### F. Background jobs and C7 (items 36–38)

- **Scan (item 36).** Ubuntu 24.04 ClamAV: `freshclam` runs as a daemon (24 checks/day), no `clamscan` timer; ClamAV is absent from every Ubuntu desktop metapackage (S2-03, S2-02). popcon clamav-freshclam 11,359 installs (S3-10). OpTC shows Windows Defender signature updates as the endpoint's scheduled AV job (S3-05, Windows).
- **Unasked jobs (item 37).** Stock Ubuntu 24.04 GNOME enables apt-daily/upgrade, dpkg-db-backup, man-db, logrotate, fstrim, e2scrub_all, motd-news, update-notifier-*, fwupd-refresh timers with their schedules and Nice/IO classes (S2-01, S2-25 for 26.04; S4-08: 22 timers across 16 packages from the desktop closure). Fedora presets: dnf-makecache (3 h), plocate-updatedb, fstrim, logrotate, raid-check, sysstat, dkms, akmods; `disable *` otherwise (S2-05, S2-06, S4-09). Arch: `disable *` presets, yet systemd-tmpfiles-clean, man-db, shadow, logrotate, plocate timers ship pre-linked (S2-07, S4-10). The runner image itself disables apt-daily, masks fwupd-refresh and turns off man-db auto-update, so a runner's timer list is not stock (S4-01). Durations of any timer job: not found.
- **Indexer names (item 38).** As item 35; plocate's timer comes only with Kubuntu on Ubuntu (S2-01).

### G. Session baseline (items 39–41)

- **Session processes and names (items 39–40).** GNOME has started Xwayland on demand since mutter 40; mutter disabled its X11 backend in 49 and removed it in 50 (S2-12); Ubuntu 24.04 still ships an Xorg session beside the GDM Wayland default, 26.04 is Wayland-only (S2-14, S2-25). Bus: dbus-daemon on Ubuntu, dbus-broker on Fedora and Arch (S2-05, S2-07, S2-14; popcon S3-10). Audio: pipewire, pipewire-pulse, wireplumber user units; `systemd --user` (S2-13, S2-26). No observed process list of a stock desktop session in any class; a runner can start `gnome-shell --headless --virtual-monitor` (S4-04, S4-06) or a full gnome-session in a systemd container (S4-05) and list processes — proposed runner step, not run (S4 §3).
- **In use or just left (item 41).** Not found.

### H. Scenario rows (items 42–56)

- S3/S11 video call: S2-22, S2-23 (above). S5: S2-21. S9/S10: S2-17…S2-20, S3-08. S12: nothing on desktop ML training. S13: nothing on concurrent media. S14: S2-04, S2-08. S15: S1-28 only (servers). S17: S2-03. S18: S2-12…S2-14. The rows' application-product vs process-name question (item 55): `comm` rules (S2-11), Wine naming (S2-19).

### I. Task-switching and focus sources (items 57–63)

- **SWELL-KW (item 61):** the raw logs are open and contain what 9.5 handed on (S3-01).
- **González & Mark, Mark et al. (58–60):** re-read independently (S1-03, S1-06, S1-13, S1-21); Zhang CHB 2015 (57) not re-found in the S1 record.
- **C-plain-7 (63):** public traces with process names exist — BEHACOM (Linux and Windows, natural use, per-minute foreground executable) (S3-04), OpTC (Windows, image paths, scripted users) (S3-05); LANL pseudonymises process names (S3-06); the 8-week Windows set of arXiv 2105.09900 is "vetted" access only (S3-14).

## Not found, all classes

- A process-level observation of real Linux desktops by activity: the full running set during office, browsing, compile, gaming, media or a call (T1).
- Any real-user order across photo editing, video editing and export, or across research → writing → build → mail (T3).
- Renderer-process counts on Linux from real users (T4); tab-switch or page-load rates after 2010 other than SWELL-KW's IE in a lab (T4, T9).
- Proton thread counts; Steam helper processes during play documented; the Linux client downloading while a game runs (T5).
- Run durations of any default timer job; an observed DKMS autoinstall on a desktop (T6).
- Desktop job sizes: object counts per build, render/transcode lengths, desktop backups, desktop ML training (T7).
- Frequency of image filters, preview renders or mail sends in natural use (T9).
- Application launches per session; launch work on Linux beyond lab benchmarks (T10).
- Linux video-call process structure during a call; logged concurrent video and music (T11).
- A published process list of a headless desktop session on a hosted runner (T13).

Unreachable or restricted (from the records): ACM DL 403 for Blake et al. ISCA 2010, Flautner et al. ASPLOS 2000, Chang et al. CHI 2021, Crichton et al. TWEB 2021; SWISH 404/403; github.com web/API 403 to this session (scx issues, gamemode issue read through WebFetch only); OpTC Google Drive quota exceeded (the corrected copy was read by range); LANL behind e-mail registration; arXiv 2105.09900 data vetted-only; Ubuntu popcon discontinued; TravisTorrent domain lapsed; src.fedoraproject.org and gitlab.winehq.org raw files behind an Anubis bot check (worked around by git clone); support.discord.com 403 (Zendesk API used); data.firefox.com needs JavaScript; developer.valvesoftware.com bot challenge (Wayback used).
