# Reader output R06-ananicy

## Copies used

| source id | canonical location | local copy | commit (full hash) | commit date | notes |
|---|---|---|---|---|---|
| ananicy-rules | https://github.com/CachyOS/ananicy-rules | `_dev/research/jioh/2026-09-13-verification/sources/ananicy-rules` | `03ef03fbf7e834385377432ccecaedd32e3414bb` | 2026-09-08 19:11:25 -0300 | Pre-existing clone, detached at 03ef03fb, working tree clean. `git ls-remote origin` (2026-09-13): `refs/heads/master` = `03ef03fbf7e834385377432ccecaedd32e3414bb` = HEAD, so **the pinned commit is the latest master commit; nothing differs at latest**. (Other branch: `refs/heads/Backup` = 8966e319…, not used.) GitHub API: not archived, license GPL-3.0, pushed_at 2026-09-08T22:11:56Z. |
| ananicy (upstream) | https://github.com/Nefelim4ag/Ananicy | `_dev/research/jioh/2026-09-13-verification/sources/ananicy` (cloned 2026-09-13) | `1e2cc9a62ba3b6793e59da66aa0039f89e1ad49f` (HEAD of master; `git describe` = 2.2.1-70-g1e2cc9a) | 2023-03-21 16:03:42 +0100 | GitHub API: `archived: True`, license GPL-3.0, pushed_at 2023-03-21. Last tag 2.2.1 = `7c0656c0ceea81760cdf7c58ec5c0c46bb31e5a2` (2021-01-29). |
| ananicy-cpp | https://gitlab.com/ananicy-cpp/ananicy-cpp | `_dev/research/jioh/2026-09-13-verification/sources/ananicy-cpp` (cloned 2026-09-13) | `3554447c1ca495478bd00e002078847dfd2205d6` (HEAD of master; `git describe` = v1.2.0-3-g3554447) | 2026-08-18 04:33:16 +0400 | Tag v1.2.0 = `cf5ac2eb7b9660794f26f274975066f33359c63e` (2026-03-26). GitLab releases API: latest release v1.2.0 released 2026-03-26T22:29:58Z. GitLab API license: "GNU General Public License v3.0 or later" (gpl-3.0+); LICENSE file is GPLv3 text; fedora/ananicy-cpp.spec:5 `License:        GPLv3`. |
| ArchWiki "Improving performance" | https://wiki.archlinux.org/title/Improving_performance | `_dev/research/jioh/2026-09-13-verification/sources/wikis/archwiki-improving-performance.wikitext` | revid 885186 | 2026-09-07T06:47:21Z | Fetched via MediaWiki API. |
| ArchWiki "Restic" | https://wiki.archlinux.org/title/Restic | `_dev/research/jioh/2026-09-13-verification/sources/wikis/archwiki-restic.wikitext` | revid 883621 | — | Fetched via MediaWiki API. |
| CachyOS wiki "Gaming" | https://wiki.cachyos.org/configuration/gaming/ | `_dev/research/jioh/2026-09-13-verification/sources/wikis/cachyos-configuration-gaming.{html,txt}` | — (fetched 2026-09-13) | — | Also fetched general_system_tweaks, cachyos_settings, faq (0 "ananicy" hits each). |

Analysis scripts (read-only against the clones): `_dev/research/jioh/2026-09-13-verification/r06/parse.py` (parses every non-blank, non-`#` line of each tracked `.rules` file as JSON), `stats.py`, `perfile.py`; intermediate `cachy.json`, `mixed.json`, `perfile.md`. The repo's own `lint.py` was also run with a scratch venv (`fastjsonschema` 2.22.2).

Line-parsing conventions matter for counts, so both are stated:
- **ananicy-cpp loader** (ananicy-cpp `src/rules.cpp:36-65` @3554447): a line is skipped if empty or its first non-space/tab/CR character is `#`; otherwise the substring from the first `{` to the last `}` is JSON-parsed ("Remove trailing characters.").
- **CachyOS `lint.py`** (`lint.py:25-28` @03ef03fb): skips only lines where `line.startswith('#') or line.strip() == ""`; everything else must be valid JSON as-is.
- My parse.py skips blank lines and lines whose stripped form starts with `#`, and requires strict JSON (like lint.py for JSON validity, like ananicy-cpp for comments).

---

## ananicy-rules (CachyOS) @ 03ef03fbf7e834385377432ccecaedd32e3414bb

### C-ananicy-rules-1 — defined rule `type` names and what each type sets

(a) Verbatim, `00-types.types` (entire file):
```
     1	# Type: Game
     2	# Use more CPU time if possible
     3	# Games do not always need more IO, but in most cases can be hungry for CPU
     4	{ "type": "Game", "nice": -5, "ioclass": "best-effort", "sched": "normal" }
     5	
     6	# Type: Player Audio/Video
     7	# Try to add more CPU power to decrease latency/lags
     8	# Try to add real time io for avoiding lags
     9	{ "type": "Player-Audio", "nice": -4 }
    10	{ "type": "Player-Video", "nice": -4 }
    11	
    12	# Must have more CPU/IO time, but not so much as other apps
    13	{ "type": "Image-View", "nice": -4 }
    14	{ "type": "Doc-View",   "nice": -4 }
    15	
    16	# Type: Low Latency Realtime Apps
    17	# In general case not so heavy, but must not lag
    18	{ "type": "LowLatency_RT", "nice": -12, "ioclass": "best-effort" }
    19	
    20	# Type: BackGround CPU/IO Load
    21	# Background CPU/IO it's needed, but it must be as silent as possible
    22	{ "type": "BG_CPUIO", "nice": 16, "ioclass": "idle", "sched": "idle" }
    23	
    24	# Type: Background CPU but demands more I/O, One example: File Synchronization
    25	{ "type": "BG_CPU", "nice": 14, "ioclass": "best-effort", "sched": "idle" }
    26	
    27	# Type: Background Launcher
    28	# Runs quietly but may spawn foreground or latency-sensitive workloads
    29	{ "type": "Launcher", "nice": 16, "ioclass": "idle", "sched": "normal" }
    30	
    31	# Type: Heavy CPU Load
    32	# It must work fast enough but must not create so much noise
    33	{ "type": "Heavy_CPU", "nice": 9, "ioclass": "best-effort", "ionice": 7 }
    34	
    35	# Type: Chat
    36	{ "type": "Chat", "nice": -3, "ioclass": "best-effort", "ionice": 7 }
    37	
    38	# Type: Service
    39	{ "type": "Service", "nice": 10, "ioclass": "best-effort", "ionice": 6 }
    40	
    41	# Type: Indifference
    42	{ "type": "IN_DIFF", "nice": 0, "ioclass": "best-effort", "ionice": 7 }
    43	
    44	# Type: Adj OOM Score
    45	{ "type": "OOM_KILL", "oom_score_adj": 1000 }
    46	{ "type": "OOM_NO_KILL", "oom_score_adj": -1000 }
```
Only `.types` file in the repo: `git ls-files | grep '\.types$'` → `00-types.types`.

(b) Locator: `00-types.types:1-46` @03ef03fb.

(c) Reading: 15 type names: Game, Player-Audio, Player-Video, Image-View, Doc-View, LowLatency_RT, BG_CPUIO, BG_CPU, Launcher, Heavy_CPU, Chat, Service, IN_DIFF, OOM_KILL, OOM_NO_KILL. What each sets is exactly the fields on its line (see table in topic 2). No type sets `latency_nice`, `rtprio`, `cpuset` or `cgroup`, even though the repo's `ananicy.schema.json` allows those keys. How a type is applied (ananicy-cpp `src/rules.cpp:198-206` @3554447): the type's fields are copied and the rule's own fields are merged over them ("overriding parameters from the type with those explicitly specified in the rule"). Comment-vs-field notes: the Player comment (line 8) says "Try to add real time io for avoiding lags" but neither Player type sets `ioclass` (git history: commit ce23ff5c, 2023-01-08, "Remove realtime io, seems to cause issues"); the "Low Latency Realtime Apps" type sets only nice −12 and ioclass best-effort — no realtime `sched` and no realtime ioclass.

(d) Verdict: **FOUND**.

### C-ananicy-rules-2 — nice / ioclass / sched / oom_score_adj per type in `00-types.types`, including the audio-player type

(a) Verbatim: see topic 1 (full file).

(b) Locator: `00-types.types:4,9,10,13,14,18,22,25,29,33,36,39,42,45,46` @03ef03fb.

(c) Reading (blank = field not set by the type, i.e. the daemon leaves that attribute as is unless the rule sets it):

| type (line) | nice | ioclass | ionice | sched | oom_score_adj |
|---|---|---|---|---|---|
| Game (4) | -5 | best-effort | | normal | |
| Player-Audio (9) | -4 | | | | |
| Player-Video (10) | -4 | | | | |
| Image-View (13) | -4 | | | | |
| Doc-View (14) | -4 | | | | |
| LowLatency_RT (18) | -12 | best-effort | | | |
| BG_CPUIO (22) | 16 | idle | | idle | |
| BG_CPU (25) | 14 | best-effort | | idle | |
| Launcher (29) | 16 | idle | | normal | |
| Heavy_CPU (33) | 9 | best-effort | 7 | | |
| Chat (36) | -3 | best-effort | 7 | | |
| Service (39) | 10 | best-effort | 6 | | |
| IN_DIFF (42) | 0 | best-effort | 7 | | |
| OOM_KILL (45) | | | | | 1000 |
| OOM_NO_KILL (46) | | | | | -1000 |

Naming note: there is no type literally named "audio-player"; the audio-player type is `Player-Audio`, which sets **only** `nice: -4` — no ioclass, no sched, no oom_score_adj. (Upstream Ananicy HEAD instead has a type `music-player`, which sets nothing; see C-ananicy-2.) `sched` is set by only four types (Game normal, BG_CPUIO idle, BG_CPU idle, Launcher normal); `oom_score_adj` only by OOM_KILL / OOM_NO_KILL. Git history for these values: be1add6e (2026-07-19) "removed sched: normal from majority of types"; b0b20597 (2026-07-11) had "added explicit \"sched\": \"normal\" to types. this will pervent unintended SCHED_* inheritance."

(d) Verdict: **FOUND** (with the naming note: type is `Player-Audio`).

### C-ananicy-rules-3 — how Proton/Wine games are separated from Linux-native games

(a) Verbatim, `README.md:27-29`:
```
3. Navigate to the desired folder depending on:
	- Game is meant to be ran under with Proton: [`wine_proton`](https://github.com/CachyOS/ananicy-rules/tree/master/00-default/Games/wine_proton) → *Open the corresponding file depending on the letter.*
	- Provides a native version for Linux: [`linux-native`](https://github.com/CachyOS/ananicy-rules/tree/master/00-default/Games/linux-native) → *Open the corresponding file depending on the letter.*
```
Directory listing (`ls 00-default/Games/wine_proton 00-default/Games/linux-native …/non-latin`): `wine_proton/` holds `common.rules`, `wine_proton_a.rules` … `wine_proton_z.rules`, `wine_proton_numerical.rules`, `wine_proton_the.rules`, `non-latin/{wine_proton_chinese,wine_proton_japanese,wine_proton_non-latin}.rules`; `linux-native/` holds `common.rules`, `linux-native_a.rules` … `_z`, `_numerical`, `_the`, `non-latin/{linux-native_chinese,linux-native_non-latin}.rules`. Top-level `00-default/Games/` also has `asf.rules, emulators.rules, gaming-tools.rules, launchers.rules, mednaffe.rules, steam-shader-compilation.rules, ue4.rules, waydroid.rules, wine.rules, wineserver.rules`.

Examples: `README.md:44-45` `# Just Cause 2 https://store.steampowered.com/app/8190/Just_Cause_2/` / `{ "name": "JustCause2.exe", "type": "Game" }` (actual location at pin: `00-default/Games/wine_proton/wine_proton_j.rules:206-207`); `00-default/Games/linux-native/common.rules:338` `# Portal 2 https://store.steampowered.com/app/620/Portal_2/` … `:341` `{ "name": "portal2_linux", "type": "Game" }`.
`00-default/Games/wineserver.rules:1-3`:
```
# Reschedule Wineserver for better performance
# https://gitlab.winehq.org/wine/wine/-/wikis/Man-Pages/wineserver
{ "name": "wineserver", "type": "LowLatency_RT" }
```

(b) Locators: `README.md:27-29`; directory tree `00-default/Games/{wine_proton,linux-native}` @03ef03fb; `00-default/Games/wineserver.rules:1-3`.

(c) Reading: separation is **by directory only**. Both directories use the same type `Game` for game executables; there is no Proton-specific or native-specific type. Entry-type counts per directory (parse.py/stats.py):
- `Games/wine_proton` 12722 entries: Game 11280, BG_CPUIO 1383, Service 56, Doc-View 1, Launcher 1, Heavy_CPU 1.
- `Games/linux-native` 2241 entries: Game 2196, BG_CPUIO 23, Service 21, LowLatency_RT 1.
- Top-level `Games/*.rules` 130 entries: Game 52, BG_CPUIO 47, Launcher 11, Doc-View 8, LowLatency_RT 5, Service 3, Image-View 2, IN_DIFF 1, Chat 1.
A practical difference visible in names: every wine_proton entry name ends in `.exe` (`grep -rn '"name"' 00-default/Games/wine_proton | grep -vci '\.exe"'` → `0`); linux-native has 2 `.exe` names (`linux-native/common.rules:500` `WreckRunners.exe` BG_CPUIO, `:504` `WreckRunners-Win64-Shipping.exe` Game). Wine infrastructure processes are in top-level files: `wine.rules` (tabtip.exe, explorer.exe, plugplay.exe, services.exe → BG_CPUIO) and `wineserver.rules` (LowLatency_RT). Files in both directories open with `# Ordered based on executable name` (common.rules) or `# Add games in alphabetical order.` (letter files).

(d) Verdict: **FOUND** (directories, not types).

### C-ananicy-rules-4 — whether background work the user wants is distinguished from background work to be deprioritized

(a) Verbatim, all type comments about background work (`00-types.types`):
```
    20	# Type: BackGround CPU/IO Load
    21	# Background CPU/IO it's needed, but it must be as silent as possible
    22	{ "type": "BG_CPUIO", "nice": 16, "ioclass": "idle", "sched": "idle" }
    23	
    24	# Type: Background CPU but demands more I/O, One example: File Synchronization
    25	{ "type": "BG_CPU", "nice": 14, "ioclass": "best-effort", "sched": "idle" }
    26	
    27	# Type: Background Launcher
    28	# Runs quietly but may spawn foreground or latency-sensitive workloads
    29	{ "type": "Launcher", "nice": 16, "ioclass": "idle", "sched": "normal" }
    30	
    31	# Type: Heavy CPU Load
    32	# It must work fast enough but must not create so much noise
    33	{ "type": "Heavy_CPU", "nice": 9, "ioclass": "best-effort", "ionice": 7 }
```
`00-default/Games/steam-shader-compilation.rules:1-2`:
```
# Give Shaders compilation less cpu power, to avoid fps spikes until they are compiled
{ "name": "fossilize_replay", "type": "BG_CPUIO" }
```

(b) Locators: `00-types.types:20-33`; `00-default/Games/steam-shader-compilation.rules:1-2` @03ef03fb.

(c) Reading: The catalogue has several low-priority types differentiated by **resource profile**, not by whether the user wants the work: BG_CPUIO (CPU+IO idle, "as silent as possible"), BG_CPU (CPU idle but IO best-effort, "demands more I/O", example file sync — but **no rule uses BG_CPU**, see topic 10), Launcher (quiet but sched normal because it "may spawn foreground … workloads"), Heavy_CPU ("must work fast enough but must not create so much noise"), Service (nice 10). No type, comment, README text or issue template states a distinction between user-wanted and unwanted background work. In practice, work a user typically starts deliberately (downloads: transmission, qbittorrent, wget, curl, yt-dlp; backups: borg, restic, rsync, rclone; syncthing, nextcloud, dropbox) is assigned the same BG_CPUIO type as unsolicited helpers (e.g. `EABackgroundService.exe`, `DiscoverNotifier`, crash reporters). Search: `grep -rniE 'want|user|foreground|background|silent|quiet|deprioriti|less cpu|lower prio|high prio|priority|noise|lag|respons|interactiv' --include='*.rules' --include='*.types' --include='*.md' --include='*.conf' .` (excluding per-game files) — hits are only the type comments above, README nice-value explanation (README.md:10), app descriptions (e.g. "spawns QtWebEngineProcess background processes", "Userspace thrash protector"), and the shader-compilation comment. (For contrast, upstream Ananicy README — not the CachyOS catalogue — says: "It's useful to use `{"ioclass": "idle"}` for IO hungry background tasks like: file indexers, Cloud Clients, Backups and etc." `README.md:105` @1e2cc9a.)

(d) Verdict: **NOT FOUND** (no user-intent distinction; searched as above). What exists instead: resource-profile background types (BG_CPUIO / BG_CPU / Launcher / Heavy_CPU / Service).

### C-ananicy-rules-5 — type for file indexers (tracker, baloo, updatedb); ioclass/nice/sched; any timing or rate values

(a) Verbatim:
`00-default/DEs-and-WMs/plasma.rules:10-14`:
```
# https://community.kde.org/Baloo
# Baloo is the file indexing and file search framework for KDE.
{ "name": "baloo_file", "type": "BG_CPUIO" }
{ "name": "baloorunner", "type": "BG_CPUIO" }
{ "name": "baloo_file_extractor", "type": "BG_CPUIO" }
```
`00-default/System Utilities & Maintenance/recoll.rules:1-2`:
```
# Recoll Desktop search tool http://www.lesbonscomptes.com/recoll/
{ "name": "recollindex", "type": "BG_CPUIO" }
```
`00-types.types:22`: `{ "type": "BG_CPUIO", "nice": 16, "ioclass": "idle", "sched": "idle" }`
`ananicy.conf:1-5`:
```
## Ananicy 2.X configuration
# Ananicy run full system scan every "check_freq" seconds
# supported values 0.01..86400
# values which have sense: 1..60
check_freq = 15
```
`00-cgroups.cgroups:1-8`:
```
# Cgroups definitions
# Currently very simple, only for group CPU intensive tasks

# cpuquota same as systemd CPUQuota,
# only difference is - meaning of N% is all CPUs, not one core.
{ "cgroup": "cpu90", "CPUQuota": 90 }
{ "cgroup": "cpu85", "CPUQuota": 85 }
{ "cgroup": "cpu80", "CPUQuota": 80 }
```

(b) Locators: as labelled, @03ef03fb.

(c) Reading: Baloo (3 process names) and Recoll's indexer are BG_CPUIO → nice 16, ioclass idle, sched idle. **tracker** (GNOME tracker/localsearch) and **updatedb** (and plocate/mlocate/locate) have **no entries**: `grep -rniE 'tracker-miner|tracker-extract|tracker3|localsearch|updatedb|plocate|mlocate|"locate"' . --exclude-dir=.git | wc -l` → `0`; the only "tracker" hits are unrelated (`gsr-game-tracker` BG_CPUIO in gpu-screen-recorder.rules:4; "Beam Eye Tracker" game in wine_proton/common.rules:216-218). Timing/rate: the types and rules carry **no timing or rate fields** (keys used across all 15813 parsed rule entries: `name` 15813, `type` 15811, `ionice` 9, `nice` 3, `ioclass` 2, `oom_score_adj` 1 — no `cgroup`, no timing). The only time/rate values in the repo are `check_freq = 15` (full-scan interval, seconds) in `ananicy.conf`, and CPUQuota 90/85/80 in `00-cgroups.cgroups`, which no type or rule references (no `cgroup` key used anywhere). Note: ananicy-cpp reads its config from `/etc/ananicy.d/ananicy.conf` by default (ananicy-cpp `src/main.cpp:136`), and the CachyOS Makefile copies `ananicy.conf` there (`Makefile:2`). The ananicy-cpp README example `{"name": "file-indexer", "cpuset": "efficiency-cores", "nice": 19, "sched": "idle"}` (ananicy-cpp README.md:197) is a documentation example, not a catalogue entry.

(d) Verdict: **PARTIAL** — baloo/recoll FOUND (BG_CPUIO); tracker and updatedb NOT IN CATALOGUE; no timing/rate values in types/rules (only daemon config check_freq and unused cgroup CPUQuota).

### C-ananicy-rules-6 — what Heavy_CPU sets and which processes get it; which type(s) compilers receive and their sched

(a) Verbatim `00-types.types:31-33`:
```
# Type: Heavy CPU Load
# It must work fast enough but must not create so much noise
{ "type": "Heavy_CPU", "nice": 9, "ioclass": "best-effort", "ionice": 7 }
```
All Heavy_CPU entries (`grep -rn '"Heavy_CPU"' --include='*.rules' .`, 33 lines):
```
00-default/Tools/ffmpeg.rules:2:{ "name": "ffmpeg", "type": "Heavy_CPU" }
00-default/Tools/vmware.rules:1:{ "name": "vmware-vmx", "type": "Heavy_CPU" }
00-default/Tools/vmware.rules:2:{ "name": "vmware", "type": "Heavy_CPU" }
00-default/Tools/fahclient.rules:2:{ "name": "FAHClient", "type": "Heavy_CPU" }
00-default/Tools/qemu.rules:2:{ "name": "qemu-system-x86", "type": "Heavy_CPU" }
00-default/Tools/qemu.rules:3:{ "name": "qemu-system-x86_64", "type": "Heavy_CPU" }
00-default/Text Editors/texteditors.rules:54:{ "name": "idea", "type": "Heavy_CPU" }
00-default/Text Editors/texteditors.rules:57:{ "name": "pycharm", "type": "Heavy_CPU" }
00-default/Text Editors/texteditors.rules:60:{ "name": "webstorm", "type": "Heavy_CPU" }
00-default/Text Editors/texteditors.rules:63:{ "name": "phpstorm", "type": "Heavy_CPU" }
00-default/Text Editors/texteditors.rules:66:{ "name": "clion", "type": "Heavy_CPU" }
00-default/Text Editors/texteditors.rules:67:{ "name": "Rider.Backend", "type": "Heavy_CPU" }
00-default/Text Editors/texteditors.rules:70:{ "name": "goland", "type": "Heavy_CPU" }
00-default/Text Editors/texteditors.rules:73:{ "name": "rider", "type": "Heavy_CPU" }
00-default/Text Editors/texteditors.rules:76:{ "name": "rubymine", "type": "Heavy_CPU" }
00-default/Text Editors/texteditors.rules:79:{ "name": "datagrip", "type": "Heavy_CPU" }
00-default/Text Editors/texteditors.rules:82:{ "name": "rustrover", "type": "Heavy_CPU" }
00-default/Audio-Video/soundkonverter.rules:2:{ "name": "soundkonverter", "type": "Heavy_CPU" }
00-default/Development & Programming/android-studio.rules:2:{ "name": "android-studio", "type": "Heavy_CPU" }
00-default/Development & Programming/android-studio.rules:3:{ "name": "android-studio-stable", "type": "Heavy_CPU" }
00-default/Development & Programming/android-studio.rules:4:{ "name": "android-studio-beta", "type": "Heavy_CPU" }
00-default/Development & Programming/android-studio.rules:5:{ "name": "android-studio-dev", "type": "Heavy_CPU" }
00-default/Development & Programming/android-studio.rules:6:{ "name": "android-studio-canary", "type": "Heavy_CPU" }
00-default/Development & Programming/android-studio.rules:7:{ "name": "avd", "type": "Heavy_CPU" }
00-default/Development & Programming/dart_flutter.rules:1:{ "name": "flutter", "type": "Heavy_CPU" }
00-default/Development & Programming/dart_flutter.rules:2:{ "name": "dart", "type": "Heavy_CPU" }
00-default/Development & Programming/unity.rules:2:{ "name": "Unity", "type": "Heavy_CPU" }
00-default/Productivity & Office/boinc.rules:2:{ "name": "boinc", "type": "Heavy_CPU" }
00-default/Productivity & Office/openscad.rules:2:{ "name": "openscad", "type": "Heavy_CPU" }
00-default/System Utilities & Maintenance/dupeguru.rules:2:{ "name": "dupeguru", "type": "Heavy_CPU" }
00-default/Creative/blender.rules:2:{ "name": "blender", "type": "Heavy_CPU" }
00-default/Creative/davinci.rules:2:{ "name": "resolve", "type": "Heavy_CPU" }
00-default/Games/wine_proton/wine_proton_p.rules:286:{ "name": "Path of Building.exe", "type": "Heavy_CPU" }
```
Build-related entries that do exist (verbatim): `00-default/Development & Programming/cmake.rules:2` `{ "name": "cmake-gui", "type": "BG_CPUIO" }`; `clang-tidy.rules:1` `{ "name": "clang-tidy", "type": "BG_CPUIO" }`; `clangd.rules:2` `{ "name": "clangd", "type": "Service" }`; `nix.rules:3-5` `nix`, `nix-daemon`, `nix-store` → BG_CPUIO; `node.rules:2` `{ "name": "node", "type": "BG_CPUIO" }`; `00-default/Games/ue4.rules:2` `{ "name": "ShaderCompileWorker", "type": "BG_CPUIO" }`; `00-default/Games/steam-shader-compilation.rules:2` `{ "name": "fossilize_replay", "type": "BG_CPUIO" }`.

(b) Locators: as listed, @03ef03fb.

(c) Reading: Heavy_CPU = nice 9, ioclass best-effort, ionice 7, **no sched** (so the process's policy is not changed). Its 33 processes are IDEs (JetBrains family, Android Studio), VMs (qemu, vmware), media/3D/CAD tools (ffmpeg, soundkonverter, blender, DaVinci `resolve`, openscad, Unity), distributed compute (boinc, FAHClient), dupeguru, flutter/dart, and one game helper. **Compilers**: there are no entries for compiler executables — `grep -rniE '"name": *"(gcc|g\+\+|cc|cc1|cc1plus|clang|clang\+\+|rustc|cargo|make|ninja|ld|ld\.lld|mold|javac|go|cmake|meson|ccache|sccache|zig|as|cpp|lto1|collect2|gradle|mvn|msbuild|dotnet|tsc|webpack|esbuild)"' --include='*.rules' .` returns only `00-default/Games/linux-native/linux-native_m.rules:61:{ "name": "Ninja", "type": "Game" }` (a game named Ninja). Compiler-adjacent tools present are BG_CPUIO (sched idle) or Service (no sched). History (git log, not the pinned tree): commit 5459ed81 (2024-05-10) removed `00-default/compilers.rules` and the type `{ "type":"Compiler", "nice": 13, "latency_nice": 13 }` with message "compiler: Drop them again, ananicy-cpp provides really noticeable cpu usage, when using these rules and they don't provide a real benefit at all"; earlier bf0bae3c (2024-02-25) "remove compiler processes to avoid freezes with BORE Scheduler".

(d) Verdict: **PARTIAL** — Heavy_CPU values and assignees FOUND; compiler assignments NOT FOUND at the pinned commit (removed in 2024; no compiler type exists).

### C-ananicy-rules-7 — voice/chat, download clients, backup/sync tools, antivirus scanners: type and ioclass

(a) Verbatim (selected; full `chats.rules` has 83 lines, 50 entries all `"type": "Chat"`):
`00-default/Chats/chats.rules:1-2,16-18,82-83`:
```
# Zoom: https://zoom.us
{ "name": "zoom", "type": "Chat" }
# Discord: https://discord.com/
{ "name": "Discord", "type": "Chat" }
{ "name": "discord", "type": "Chat" }
# Mumble: https://www.mumble.info/
{ "name": "mumble", "type": "Chat" }
```
(Also in chats.rules: Telegram variants, weechat, viber, vesktop/webcord/legcord etc., hexchat, teams, signal-desktop, skypeforlinux, slack, element-desktop, nheko, thunderbird, betterbird, mailspring … — all Chat.)
`00-default/Networking/linphone.rules:1-2`:
```
# rule for linphone, a SIP client. http://www.linphone.org/technical-corner/linphone/overview
{ "name": "linphon", "type": "LowLatency_RT", "nice": -15, "ioclass": "realtime" }
```
`00-default/Networking/transmission.rules:1-7`:
```
# Torrent client: https://www.transmissionbt.com
{ "name": "transgui", "type": "BG_CPUIO" }
{ "name": "transmission-cli", "type": "BG_CPUIO" }
{ "name": "transmission-daemon", "type": "BG_CPUIO" }
{ "name": "transmission-gtk", "type": "BG_CPUIO" }
{ "name": "transmission-qt", "type": "BG_CPUIO" }
{ "name": "transmission-remote", "type": "BG_CPUIO" }
```
`00-default/Tools/rsync.rules:1`: `{ "name": "rsync", "type": "BG_CPUIO" }`
`00-default/System Utilities & Maintenance/borg.rules:1-2`: `# https://www.borgbackup.org/` / `{ "name": "borg", "type": "BG_CPUIO" }`
`00-default/Networking/rclone.rules:1-2`: `# Rclone - rsync for cloud storage https://rclone.org/` / `{ "name": "rclone", "type": "BG_CPUIO" }`
`00-default/System Utilities & Maintenance/clamav.rules:1-4`:
```
# ClamAV Daemon
{ "name": "clamd", "type": "BG_CPUIO" }
# ClamUI
{ "name": "clamui", "type": "Service" }
```

(b) Locators: as labelled, @03ef03fb.

(c) Reading (type → ioclass from `00-types.types`):
- Voice/chat clients: **Chat** → nice −3, ioclass best-effort, ionice 7 (50 entries in `Chats/chats.rules` + `ArcChat.exe` in `Games/launchers.rules:14`). Exception: linphone (SIP) is LowLatency_RT overridden to nice −15, **ioclass realtime** (the rule's `"linphon"` name is truncated as written). Mumble, Discord, Zoom, Teams, Skype are Chat.
- Download clients: transmission (6 names), qbittorrent/-nox, deluge/deluge-gtk/deluged, aria2c, ktorrent, rtorrent, kget, wget, curl, amule, tixati, youtube-dl, yt-dlp → all **BG_CPUIO** → nice 16, ioclass **idle**, sched idle.
- Backup/sync: rsync, borg, rclone → **BG_CPUIO** (ioclass idle); also restic, kopia/kopia-ui, unison, syncthing/syncthing-gtk, dropbox, nextcloud → BG_CPUIO. Note BG_CPU (the type whose comment names "File Synchronization") is used by none of them.
- Antivirus: **clamscan and freshclam have no entries** (`grep -rniE 'clamscan|freshclam|clamonacc|clam' . --exclude-dir=.git` → only the 4 clamav.rules lines above). ClamAV presence is `clamd` BG_CPUIO (ioclass idle) and `clamui` Service (nice 10, ioclass best-effort, ionice 6).

(d) Verdict: **PARTIAL** — chat/voice, transmission, rsync/borg/rclone FOUND; clamscan and freshclam NOT IN CATALOGUE (catalogue has clamd and clamui instead).

### C-ananicy-rules-8 — do entries match on executable/process names; roughly how many distinct names

(a) Verbatim: `README.md:77` `## How to find out proper process name?` and `README.md:90` `**Don't use absolute paths for the executables. Process name alone is enough.**`; `README.md:8` `- **ananicy-cpp-rules** - list of rules used to assign specific nice values to specific processes.`
`ananicy.schema.json` has no `name` key; `lint.py:47-52`:
```
        if glob == "*.rules":
            schema['required'] = ["name"]
            schema["properties"]["name"] = {
                "type": "string",
                "description": "Name of the process"
            }
```
How ananicy-cpp resolves the name it matches (ananicy-cpp `src/platform/linux/process.cpp:194-262` @3554447): "Cmdline method" — basename of `cmdline[0]` (`cmdline[0].substr(exe_name_begin + 1)`); else "Exe method" — `read_symlink("/proc/<pid>/exe")` filename; else "Comm method" — `/proc/<pid>/comm`. Lookup is exact key match `m_program_rules.contains(name)` (`src/rules.cpp:184`), regex only if built with ENABLE_REGEX_SUPPORT and a rule has `name_regex` (none in the catalogue).

(b) Locators: as labelled.

(c) Reading: Yes — every entry has a `name` (lint requires it) that is a process/executable name without path. Counts (parse.py/stats.py): 15813 strictly-parsed entries, **15811 distinct names** (2 names duplicated: `spectacle`, `ds.exe`). Counting the one line that strict JSON rejects but ananicy-cpp loads (`Dungeon Drafters.x86_64`, see topic 10): 15814 active entries, 15812 distinct names. Cross-check by grep: `grep -rhoE '"name" *: *"[^"]*"' --include='*.rules' . | sed -E 's/"name" *: *//' | LC_ALL=C sort -u | wc -l` → `15813` (includes the commented-out `sxhkd` line in sxhkd.rules:3). Of the 15813 parsed names, 12780 end in `.exe` and 2491 contain a space; none contain `/`.

(d) Verdict: **FOUND** (≈15.8 thousand distinct names).

### C-ananicy-rules-9 — number of rules files, rule entries, entries per type, counted per file

(a)/(c) Commands and outputs:
```
$ git ls-files "*.rules" | wc -l
     361
$ python3 parse.py ../sources/ananicy-rules cachy.json
rules files 361
types defined 15 ['Game', 'Player-Audio', 'Player-Video', 'Image-View', 'Doc-View', 'LowLatency_RT', 'BG_CPUIO', 'BG_CPU', 'Launcher', 'Heavy_CPU', 'Chat', 'Service', 'IN_DIFF', 'OOM_KILL', 'OOM_NO_KILL']
rule entries (parsed JSON objects) 15813
malformed 1
   ('00-default/Games/linux-native/linux-native_d.rules', 315, 'JSON: Extra data: line 1 column 54 (char 53)', '{ "name": "Dungeon Drafters.x86_64", "type": "Game" }+')
other oddities 1
   ('00-default/Services/firewalld.rules', 1, 'comment with leading whitespace', ' # FirewallD ')
$ python3 stats.py cachy.json   (entries per type, all files)
  'Game': 13528
  'BG_CPUIO': 1615
  'Service': 194
  'Doc-View': 160
  'LowLatency_RT': 109
  'Chat': 51
  'Heavy_CPU': 33
  'Image-View': 32
  'Player-Audio': 28
  'Player-Video': 24
  'Launcher': 24
  'IN_DIFF': 10
  'OOM_NO_KILL': 2
  '<no type>': 2
  'TODO': 1   <-- UNDEFINED
```
Grep cross-check (counts every `"type": "..."` occurrence, including the rejected Dungeon Drafters line and the commented sxhkd line):
```
$ grep -rhoE '"type" *: *"[^"]*"' --include='*.rules' . | sed -E 's/"type" *: *//' | LC_ALL=C sort | uniq -c | sort -rn
13529 "Game"
1615 "BG_CPUIO"
 194 "Service"
 160 "Doc-View"
 110 "LowLatency_RT"
  51 "Chat"
  33 "Heavy_CPU"
  32 "Image-View"
  28 "Player-Audio"
  24 "Player-Video"
  24 "Launcher"
  10 "IN_DIFF"
   2 "OOM_NO_KILL"
   1 "TODO"
```
The grep figures exceed the parse figures by exactly those two lines (Game +1, LowLatency_RT +1). Summary: **361 rules files; 15813 strictly valid entries (15814 as loaded by ananicy-cpp)**. One file has 0 entries: `00-default/DEs-and-WMs/sxhkd.rules` (all 3 lines are comments; line 3 `# { "name": "sxhkd", "type": "LowLatency_RT" }`).

(b) Locator: all tracked `*.rules` files @03ef03fb. Full per-file table is in the Appendix at the end of this file.

(d) Verdict: **FOUND**.

### C-ananicy-rules-10 — how many types defined, which unused, undefined type strings, malformed lines

(a)/(c) Commands and outputs:
```
$ python3 stats.py cachy.json
defined but unused: ['BG_CPU', 'OOM_KILL']
undefined type entries: 1
   ('00-default/DEs-and-WMs/gnome.rules', 2, {'name': 'tumblerd', 'type': 'TODO'})
names total 15813 distinct 15811
duplicated names 2 extra occurrences 2
keys used {'name': 15813, 'type': 15811, 'nice': 3, 'ioclass': 2, 'ionice': 9, 'oom_score_adj': 1}
entries w/o type 2
schema value violations 0
$ grep -rn '"type": *"BG_CPU"' --include='*.rules' . | wc -l
       0
$ grep -rn '"type": *"OOM_KILL"' --include='*.rules' . | wc -l
       0
```
Verbatim offending lines:
- `00-default/DEs-and-WMs/gnome.rules:1-2`: `# http://live.gnome.org/ThumbnailerSpec ` / `{ "name": "tumblerd", "type": "TODO" }`
- `00-default/Games/linux-native/linux-native_d.rules:314-315`: `# Dungeon Drafters https://store.steampowered.com/app/1824580/Dungeon_Drafters/` / `{ "name": "Dungeon Drafters.x86_64", "type": "Game" }+`
- `00-default/Services/firewalld.rules:1-2`: ` # FirewallD ` (leading space) / `{"name": "firewalld", "type": "BG_CPUIO", "ionice": 1 }`
- Duplicates: `00-default/DEs-and-WMs/plasma.rules:6` `{ "name": "spectacle", "type": "LowLatency_RT" }` vs `00-default/DEs-and-WMs/screenshotter.rules:8` `{ "name": "spectacle", "type": "Image-View" }`; `00-default/Games/wine_proton/common.rules:663` and `00-default/Games/wine_proton/wine_proton_d.rules:474`, both `{ "name": "ds.exe", "type": "Game" }`.
- Entries without type (valid per schema): `plasma.rules:29` `{ "name": "plasmashell", "nice": -6 }`; `System Utilities & Maintenance/thrash-protect.rules:2` `{ "name": "thrash-protect", "nice": -12, "ioclass": "realtime" }`.

The repo's own linter, run at the pin:
```
$ ../../r06/venv/bin/python lint.py; echo "exit=$?"
Error in file 00-default/DEs-and-WMs/screenshotter.rules on line 243
Line: { "name": "spectacle", "type": "Image-View" }
Duplicate name: spectacle, present also in 00-default/DEs-and-WMs/plasma.rules

Error in file 00-default/DEs-and-WMs/gnome.rules on line 317
Line: { "name": "tumblerd", "type": "TODO" }
Invalid type: TODO

Error in file 00-default/Services/firewalld.rules on line 1644
Line:  # FirewallD
Invalid JSON: Expecting value

Error in file 00-default/Games/wine_proton/common.rules on line 13686
Line: { "name": "ds.exe", "type": "Game" }
Duplicate name: ds.exe, present also in 00-default/Games/wine_proton/wine_proton_d.rules

Error in file 00-default/Games/linux-native/linux-native_d.rules on line 36361
Line: { "name": "Dungeon Drafters.x86_64", "type": "Game" }+
Invalid JSON: Extra data

exit=1
```
(lint.py's "line" numbers are 0-based running counts across all files via `fileinput`, not per-file lines; per-file lines are given above.)

(b) Locators: as labelled @03ef03fb.

Reading: **15 types defined**; **2 unused** (BG_CPU, OOM_KILL); **1 undefined type string** (`TODO`, on tumblerd — upstream Ananicy defines `TODO` as a marker type, CachyOS does not; ananicy-cpp's `get_rule` only merges a type if `m_type_rules.contains(rule["type"])`, so tumblerd gets no settings). **Malformed lines**: 1 strictly-invalid JSON line (Dungeon Drafters, trailing `+`) — ananicy-cpp would still load it because it parses only from first `{` to last `}` (`src/rules.cpp:53-65`); 1 comment line with a leading space (firewalld.rules:1) that lint.py flags as invalid JSON but ananicy-cpp treats as a comment (`src/rules.cpp:43-45`). No schema value violations (ranges/enums) among parsed entries. Plus 2 duplicate names (lint errors; in ananicy-cpp, `insert_or_assign` means whichever file loads last wins). lint exits 1 at the pinned commit.

(d) Verdict: **FOUND**.

### C-ananicy-rules-11 — README maintainer statement; contribution instructions for game entries; example with different types for one game's executables

(a) Verbatim `README.md:1-3`:
```
# Ananicy-cpp-rules for CachyOS

This is a ananicy-cpp-rules collection for ananicy-cpp maintained by the CachyOS team and the community.
```
`README.md:20-54`:
````
## How to contribute

You can add your favorite games, apps, and more. Any help would be greatly appreciated!
**For example, let's say you want to add a game:**

1. Go to [00-default](https://github.com/CachyOS/ananicy-rules/tree/master/00-default)
2. Go to [Games](https://github.com/CachyOS/ananicy-rules/tree/master/00-default/Games)
3. Navigate to the desired folder depending on:
	- Game is meant to be ran under with Proton: [`wine_proton`](https://github.com/CachyOS/ananicy-rules/tree/master/00-default/Games/wine_proton) → *Open the corresponding file depending on the letter.*
	- Provides a native version for Linux: [`linux-native`](https://github.com/CachyOS/ananicy-rules/tree/master/00-default/Games/linux-native) → *Open the corresponding file depending on the letter.*
4. Open the corresponding file depending on the letter.
5. Follow the examples from below.

### Examples of rules

The **first example** is simple. In the **second example**, it is different because some games generate multiple processes. In such cases, you need to add all the processes related to the game.

Please also add the name of the game next to the url, which you get the name of said game from the Steam store.

If not from any store add name you think it needs.

#### 1. [Example rule for Just Cause 2](https://github.com/CachyOS/ananicy-rules/blob/b3bf685c267cdc817a7067c6c16c9725cd5c5250/00-default/Games/wine_proton/wine_proton_j.rules#L168)

```
# Just Cause 2 https://store.steampowered.com/app/8190/Just_Cause_2/
{ "name": "JustCause2.exe", "type": "Game" }
```

#### 2. [Example rules for Mortal Shell](https://github.com/CachyOS/ananicy-rules/blob/ebf4fa421e128ccb3c16e4a0cbff4a00d06aacdc/00-default/Games/wine_proton/wine_proton_m.rules#L1382)

```
# Mortal Shell https://store.steampowered.com/app/1110910/Mortal_Shell/
{ "name": "Dungeonhaven.exe", "type": "BG_CPUIO" }
{ "name": "Dungeonhaven-Win64-Shipping.exe", "type": "Game" }
```
````
Also `README.md:56-61` (Portal 2 linux-native example `{ "name": "portal2_linux", "type": "Game" }`), `README.md:63-65` (contribute by opening an issue; "Make sure the app is not already in the repository before opening an issue."), `README.md:67-75` (`make lint` "will check rules syntax and also check for duplicates"; "Games can be sorted with `sort-games.sh`"), `README.md:92-94`:
```
## [GameMode](https://github.com/FeralInteractive/gamemode) + [ananicy-cpp](https://gitlab.com/ananicy-cpp/ananicy-cpp) = bad idea

GameMode and ananicy-cpp both adjust the nice levels of processes. However, combining both tools is not recommended, and we strongly advise against doing so.
```
The Mortal Shell example exists in the pinned tree at `00-default/Games/wine_proton/wine_proton_m.rules:1456-1458` (verbatim identical to the README block); also at the README-linked commit ebf4fa42 (`git show ebf4fa42…:…/wine_proton_m.rules`, lines 1382-1384). Adjacent at the pin, `wine_proton_m.rules:1460-1462`: `# Mortal Shell II - Open Beta …` / `{ "name": "MortalShell2.exe", "type": "BG_CPUIO" }` / `{ "name": "MortalShell2-Win64-Shipping.exe", "type": "Game" }`.

(b) Locators: `README.md:1-3, 20-75, 92-94` @03ef03fb; `00-default/Games/wine_proton/wine_proton_m.rules:1456-1462` @03ef03fb.

(c) Reading: maintainer statement = "maintained by the CachyOS team and the community". Game contribution = pick `wine_proton` (runs under Proton) or `linux-native` (has a native Linux version), open the per-letter file, add a `# <Steam name> <store URL>` comment and one line per process; games that spawn several processes need all of them. The Mortal Shell example gives the launcher/bootstrap `Dungeonhaven.exe` BG_CPUIO and the actual game binary `…-Win64-Shipping.exe` Game. The README's line anchors are to older commits (Just Cause 2 now at wine_proton_j.rules:206-207; Portal 2 now in linux-native/common.rules:338-341, not linux-native_p.rules). How common the split pattern is (heuristic: consecutive entry lines under one comment header, blocks separated by blank lines, perfile.py): 12280 blocks in `00-default/Games/`, 1162 with >1 distinct type (wine_proton 1143, linux-native 11, launchers.rules 7, gaming-tools.rules 1); the most common combination is {BG_CPUIO, Game} (1132 blocks). This is an approximate count because of the block heuristic.

(d) Verdict: **FOUND**.

### C-ananicy-rules-12 — upstream Ananicy types file vs CachyOS types file

(a) Verbatim: CachyOS types — topic 1. Upstream HEAD types — C-ananicy-2 below. Upstream as of tag 2.2.1 (`git show 2.2.1:ananicy.d/00-types.types`, identical to the file just before commit 8a10460):
```
     1	# Type: Game
     2	# Use more CPU time if possible
     3	# Games do not always need more IO, but in most cases can be hungry for CPU
     4	{ "type": "Game", "nice": -5, "ioclass": "best-effort" }
     5	
     6	# Type: Player Audio/Video
     7	# Try to add more CPU power to decrease latency/lags
     8	# Try to add real time io for avoiding lags
     9	{ "type": "Player-Audio", "nice": -3, "ioclass": "realtime" }
    10	{ "type": "Player-Video", "nice": -3, "ioclass": "realtime" }
    11	
    12	# Must have more CPU/IO time, but not so much as other apps
    13	{ "type": "Image-View", "nice": -3 }
    14	{ "type": "Doc-View",   "nice": -3 }
    15	
    16	# Type: Low Latency Realtime Apps
    17	# In general case not so heavy, but must not lag
    18	{ "type": "LowLatency_RT", "nice": -10, "ioclass": "realtime" }
    19	
    20	# Type: BackGround CPU/IO Load
    21	# Background CPU/IO it's needed, but it must be as silent as possible
    22	{ "type": "BG_CPUIO", "nice": 19, "ioclass": "idle", "sched": "idle", "cgroup": "cpu80" }
    23	
    24	# Type: Heavy CPU Load
    25	# It must work fast enough but must not create so much noise
    26	{ "type": "Heavy_CPU", "nice": 19, "ioclass": "best-effort", "ionice": 7, "cgroup": "cpu90" }
    27	
    28	# Type: Chat
    29	{"type": "Chat", "nice": -1, "ioclass": "best-effort", "ionice": 7 }
    30	
    31	# Type: Adj OOM Score
    32	{ "type": "OOM_KILL", "oom_score_adj": 1000 }
    33	{ "type": "OOM_NO_KILL", "oom_score_adj": -1000 }
```

(b) Locators: CachyOS `00-types.types:1-46` @03ef03fb; upstream `ananicy.d/00-types.types` @2.2.1 (7c0656c0…) lines 1-33 and @HEAD 1e2cc9a6 lines 1-113.

(c) Reading: The CachyOS file descends from the **pre-2022 upstream** naming (CamelCase/underscore types) — every `#` comment line of upstream 2.2.1's file appears unchanged and in the same order in the CachyOS file (`diff <(grep '^#' 00-types.types) <(git show 2.2.1:ananicy.d/00-types.types | grep '^#')` shows only CachyOS-added comment lines for BG_CPU, Launcher, Service, IN_DIFF); CachyOS blame attributes those lines to the repo's "initial commit" c3efeb28, 2022-03-16. Upstream at HEAD replaced those names with 31 lowercase category types (2022-11-04, commit 8a10460 "Major Updates (#457)") and commented out Heavy_CPU, BG_CPUIO, LowLatency_RT under "Depricated types". CachyOS keeps the old names and changed values vs upstream 2.2.1: Game adds sched normal; Player-Audio/Video −3+realtime → −4 with no ioclass; Image-View/Doc-View −3 → −4; LowLatency_RT −10 realtime → −12 best-effort; BG_CPUIO 19 +cgroup cpu80 → 16, no cgroup; Heavy_CPU 19 +cgroup cpu90 → 9, no cgroup; Chat −1 → −3; OOM types unchanged. CachyOS adds BG_CPU, Launcher, Service, IN_DIFF (not in upstream 2.2.1; upstream HEAD has lowercase `service` with different values, nice 1 ionice 5). No type name is shared between CachyOS and upstream HEAD's active types except by case-insensitive coincidence (`Chat`/`chat`, `Service`/`service`, `Game`/`game`), and their values differ (upstream HEAD `game` nice −20 ionice 0; `chat` sets nothing).

(d) Verdict: **FOUND**.

---

## ananicy / ananicy-cpp

### C-ananicy-1 — documented rule fields, which are required, value ranges, rules directory, example rule for gcc

(a) Verbatim, upstream Ananicy `README.md:63-77` @1e2cc9a:
````
## Configuration
Rules files should be placed under `/etc/ananicy.d/` directory and have `*.rules` extension.
Inside .rules file every process is described on a separate line. General syntax is described below:

```
{ "name": "gcc", "type": "Heavy_CPU", "nice": 19, "ioclass": "best-effort", "ionice": 7, "cgroup": "cpu90" }
```

All fields except `name` are optional.

`name` used for match processes by exec bin name
```
~ basename $(sudo realpath /proc/1/exe)
systemd
```
````
Upstream Ananicy `README.md:13-17` (new "cmdlines" field):
````
Support for cmdline in rules added. This is particularly useful for applications that share the same name (looking at you Java). See the `freenet` rule as an example:
```
{ "name": "java", "cmdlines": ["freenet.node.NodeStarter"], "type": "service" }
```
````
Upstream Ananicy `ananicy.py:433-455` (range checks):
```
    def __check_nice(self, nice):
        if nice:
            if not -20 <= nice <= 19:
                raise Failure("Nice must be in range -20..19")
        return nice

    def __check_ionice(self, ionice):
        if ionice:
            if not 0 <= ionice <= 7:
                raise Failure("IOnice/IOprio allowed only in range 0-7")
        return ionice

    def __check_rtprio(self, rtprio):
        if rtprio:
            if not 1 <= rtprio <= 99:
                raise Failure("RTprio allowed only in range 1-99")
        return rtprio

    def __check_oom_score_adj(self, adj):
        if adj:
            if not -1000 <= adj <= 1000:
                raise Failure("OOM_SCORE_ADJ must be in range -1000..1000")
        return adj
```
and `ananicy.py:246-254` sched map: `'other': '-N', 'normal': '-N', 'rr': '-R', 'fifo': '-F', 'batch': '-B', 'iso': '-I', 'idle': '-D'` (applied via `schedtool`); `ananicy.py:388` `def __init__(self, config_dir="/etc/ananicy.d/", daemon=True):`.

ananicy-cpp `README.md:174-183` @3554447:
```
### Rules

Add rules in `/etc/ananicy.d`. This path can be overridden with `ANANICY_CPP_CONFDIR`
environment variable.
Rules are defined in files ending with `.rules`.
For instance, to add a rule for GCC, you could do the following:

- Create the `/etc/ananicy.d/10-compilers` folder.
- Create the `/etc/ananicy.d/10-compilers/gcc.rules` file
- Add `{"name": "gcc", "nice": 19, "latency_nice": 19, "sched": "batch", "ioclass": "idle"}` to the file.
```
ananicy-cpp `README.md:212-276`:
```
#### Supported attributes

- `nice: [-20-19]`: Set the nice value of the process.
A process with a higher nice value will be more "polite", and will get less
cpu time than processes with a lower nice value.
- `latency_nice: [-20-19]`: Set the latency_nice value of the process.
A process with a lower latency_nice value indicates the task to have the least
latency as compared to the task having a higher latency_nice.
A additonal kernel patch is needed see [latency_nice](https://lore.kernel.org/lkml/20221110175009.18458-1-vincent.guittot@linaro.org/)
- `sched: {"fifo", "rr", "normal", "batch", "idle"}`:
Set the scheduling policy.
  - `fifo` and `rr` (for round-robin) are realtime scheduling policies, and must only be used for
latency critical programs, like `Xorg` or `pulseaudio` for instance. Nice values are ignored,
  `rtprio` should be used instead.
  - `deadline`: Special realtime scheduling policy which _can't_ be set by `ananicy-cpp`,
  but can be reported by it.
  - `normal` is well... normal, the default behavior for the current OS.
  Specifying this option can be useful if you want to force the child of a
  realtime process to have a normal scheduling policy.
  - `batch`: Very useful for compilers or other CPU-hungry, non-interactive programs,
  like compilers for instance. It can actually improve their performance with almost no cost
  on the rest of the system.
  - `idle`: Very, very low priority, even lower than a nice value of `19`.
  Useful for background, low priority stuff, like file indexer for instance.
- `rtprio: [0, 99]`: Sets the static priority of a process. Only relevant if the actual scheduling policy
of a process is a realtime one, i.e. `fifo`, `rr` or `deadline`.
A higher value means a higher priority.
- `ioclass: {"best-effort", "realtime", "idle", "none"}`:
Define the IO scheduling policy. By default, it is `best-effort`.
**Only the CFQ I/O scheduler supports `ioclass` and `ionice`, see [ioprio_set](https://man7.org/linux/man-pages/man2/ioprio_set.2.html)**.
  - `realtime` is to be used cautiously, as the process will have the absolute priority
  above all `best-effort` processes, and can [starve][wikipedia:starvation] them.
  This could prevent you from starting a shell, for instance.
    - `ionice: [0, 7]`. Lower value is higher priority.
  - `idle`: Process gets I/O resources after all other processes.
  This could [starve][wikipedia:starvation] the process.
    - `ionice` is completely ignored.
  - `none`: Reset I/O policy to system default, `ionice` must be `0`.
  - `best-effort`: Try to fairly share I/O resources between processes.
    - `ionice: [0, 7]`. Lower value is higher priority.
- `oom_score_adj: [-999, 999]`: Adjust the **O**ut **O**f **M**emory killer score of a process.
  Negative value decrease the score of the process, making it _less_ likely to be killed if available memory
  gets very low. It is recommended to use it on critical programs which must be killed last if you lack memory.
- `cpuset`: Pin the process to the specified CPU cores using Linux cpuset notation.
  Accepts ranges (`0-7`), comma-separated lists (`0,2,4`), or mixed (`0-3,8-11`).
```
(followed by the cpuset alias table, then)
```
- `cgroup`: Put the process in the specified cgroup. This can be any cgroup, including those created outside `ananicy-cpp`.
- `type`: Set the type of the rule. All options defined in the type will be used as if written explicitly in the rule,
although you can override each option if needed.
```
ananicy-cpp `README.md:281-301` (types):
```
### Types

To avoid repeating yourself, you can add types.
It must be defined in a `.types` file.

The syntax is the following:
~~~json
{"type": "my_type", "nice": 19, "other_parameter": "value"}
~~~

It can then be used in any rule by simply adding the `type` property to the rule.
For instance, `{"name": "gcc", "type": "compiler"}`

Parameters can be overridden, for instance:
~~~json
{"type": "compiler", "nice": 19, "sched": "batch", "ioclass": "idle"}
~~~

~~~json
{"name": "gcc", "type": "compiler", "ioclass": "none", "ionice": 0}
~~~
```
ananicy-cpp required-field logic `src/rules.cpp:70-93`: a line is a program rule if `rule.contains("name") && rule["name"].is_string()`; else a type if it has string `type`; else a cgroup if it has string `cgroup`; otherwise error "Rule does not have a name, or name is not a string".

(b) Locators: Ananicy `README.md:13-17, 63-77`, `ananicy.py:246-254, 388, 433-455` @1e2cc9a6; ananicy-cpp `README.md:174-183, 212-301`, `src/rules.cpp:70-93`, `src/main.cpp:134-136` @3554447.

(c) Reading: Fields — upstream Ananicy: `name` (required), `type`, `nice` (−20..19), `ioclass`, `ionice` (0–7), `sched` (other/normal/rr/fifo/batch/iso/idle via schedtool), `rtprio` (1–99), `oom_score_adj` (−1000..1000), `cgroup`, plus `cmdlines` (list). ananicy-cpp: `nice` [−20,19], `latency_nice` [−20,19] (needs kernel patch), `sched` {fifo, rr, normal, batch, idle}, `rtprio` [0,99], `ioclass` {best-effort, realtime, idle, none}, `ionice` [0,7], `oom_score_adj` documented as [−999, 999], `cpuset`, `cgroup`, `type`; `name` required for a process rule. Rules directory: `/etc/ananicy.d/` in both (ananicy-cpp overridable with `ANANICY_CPP_CONFDIR`; code default `src/main.cpp:134`). gcc examples: upstream `{ "name": "gcc", "type": "Heavy_CPU", "nice": 19, "ioclass": "best-effort", "ionice": 7, "cgroup": "cpu90" }`; ananicy-cpp `{"name": "gcc", "nice": 19, "latency_nice": 19, "sched": "batch", "ioclass": "idle"}` in `/etc/ananicy.d/10-compilers/gcc.rules`, and in the types section `{"name": "gcc", "type": "compiler", "ioclass": "none", "ionice": 0}`. Internal inconsistencies worth noting: ananicy-cpp README gives oom_score_adj range [−999, 999] while upstream ananicy.py and the CachyOS `ananicy.schema.json` use −1000..1000 (and CachyOS OOM types use ±1000); ananicy-cpp README says global config is `/etc/ananicy.d/ananicy-cpp.conf` (README.md:131) but code defaults to `/etc/ananicy.d/ananicy.conf` (`src/main.cpp:136`); ananicy-cpp rtprio documented [0,99] vs upstream check 1..99.

(d) Verdict: **FOUND**.

### C-ananicy-2 — type names in upstream Ananicy's types file at HEAD; how older type names are marked

(a) Verbatim, `ananicy.d/00-types.types` @1e2cc9a6 (lines 27-113):
```
    27	# The `U` in `CPU_U` stands for `untouched`     -> some applications might not like messing with their niceness
    28	# The `H` in `CPU_H` stands for `high priority` -> some applications might require higher priority that the base type
    29	# The `L` in `CPU_L` stands for `low priority`  -> some applications might be less relevant / stress the system when given the priority of the base class
    30	# Same goes for `IO_U`, `IO_H` and `IO_L`
    31	
    32	### Generic Types
    33	
    34	{"type":"archiver", "nice":1, "ionice":5}
    35	
    36	{"type":"audio-server"}
    37	
    38	{"type":"chat"}
    39	
    40	{"type":"common-utility"}
    41	
    42	{"type":"compiler", "nice":1}
    43	
    44	{"type":"database"}
    45	
    46	# desktop environment, window manager or any integral part of a desktop (note: audio-server already has it's own category)
    47	{"type":"DEWM"}
    48	
    49	# TODO split into `text editor`, `document editor` and `IDE`?
    50	{"type":"document-editor"}
    51	
    52	{"type":"document-viewer"}
    53	
    54	{"type":"email-client"}
    55	
    56	{"type":"file-manager"}
    57	
    58	{"type":"file-sync", "nice":19, "ionice":7}
    59	
    60	# note: increasing some games' priority might cause a crash
    61	{"type":"game", "nice":-20, "ionice":0}
    62	
    63	{"type":"game-launcher"}
    64	
    65	{"type":"image-editor"}
    66	
    67	{"type":"image-viewer"}
    68	
    69	{"type":"music-player"}
    70	
    71	{"type":"p2p-client"}
    72	
    73	{"type":"package-manager"}
    74	
    75	{"type":"remote-desktop"}
    76	
    77	{"type":"server", "nice":1}
    78	
    79	# some services might require less resources than others
    80	{"type":"service",            "nice":1, "ionice":5}
    81	{"type":"service,CPU_U,IO_L",           "ionice":7}
    82	
    83	{"type":"screenshotter"}
    84	
    85	{"type":"terminal"}
    86	
    87	{"type":"torrent", "nice":1, "ionice":5}
    88	
    89	{"type":"video-player"}
    90	
    91	{"type":"VPN"}
    92	
    93	{"type":"VM"}
    94	
    95	{"type":"web-browser"}
    96	
    97	########################
    98	### TODO marker type ###
    99	########################
   100	
   101	{"type":"TODO"}
   102	
   103	########################
   104	### Depricated types ###
   105	########################
   106	
   107	#{"type":"Heavy_CPU", "nice":19, "ioclass":"best-effort", "ionice":7, "cgroup":"cpu90"}
   108	
   109	# BackGround CPU/IO Load
   110	# It's needed, but it must be as silent as possible
   111	#{"type":"BG_CPUIO", "nice":19, "ioclass":"idle", "sched":"idle", "cgroup":"cpu80" }
   112	
   113	#{"type":"LowLatency_RT", "nice":-10, "ioclass":"realtime"}
```
(Lines 1-26 are a comment block explaining nice/sched/ionice/ioclass.)
Count command:
```
$ python3 -c "import json; L=[l.strip() for l in open('ananicy.d/00-types.types')]; t=[json.loads(l)['type'] for l in L if l and not l.startswith('#')]; print(len(t), t)"
31 ['archiver', 'audio-server', 'chat', 'common-utility', 'compiler', 'database', 'DEWM', 'document-editor', 'document-viewer', 'email-client', 'file-manager', 'file-sync', 'game', 'game-launcher', 'image-editor', 'image-viewer', 'music-player', 'p2p-client', 'package-manager', 'remote-desktop', 'server', 'service', 'service,CPU_U,IO_L', 'screenshotter', 'terminal', 'torrent', 'video-player', 'VPN', 'VM', 'web-browser', 'TODO']
```

(b) Locator: `ananicy.d/00-types.types:1-113` @1e2cc9a62ba3b6793e59da66aa0039f89e1ad49f (last changed by 8a1046066fdbf8d374adb323f56db6f5e3ea121e, 2022-11-04, "Major Updates (#457)").

(c) Reading: 31 active type names (30 generic types + `TODO` marker; one name is the compound `service,CPU_U,IO_L`, a variant scheme with U/H/L suffixes explained in lines 27-30). Older names are marked by being **commented out** (`#{...}`) under a banner `### Depricated types ###` (spelled "Depricated"): Heavy_CPU, BG_CPUIO, LowLatency_RT. The other pre-2022 types (Game, Player-Audio, Player-Video, Image-View, Doc-View, Chat, OOM_KILL, OOM_NO_KILL — see 2.2.1 file under C-ananicy-rules-12) are simply absent at HEAD, not listed as deprecated. Rules still using an old name are grouped in a directory named `ananicy.d/00-default/depricated-Heavy_CPU/` (contains boinc, dart_flutter, dupeguru, fahclient, imagemagick, soundkonverter .rules). Many types set nothing (e.g. `music-player`, `chat`, `video-player`), so they only label.

(d) Verdict: **FOUND**.

### C-ananicy-3 — README self-description, repository locations, licenses, ananicy-cpp version; distribution wiki coverage

(a) Verbatim, upstream Ananicy `README.md:1-30` @1e2cc9a6 (excerpt):
```
# Ananicy

## Installation

* ![logo](http://www.monitorix.org/imgs/archlinux.png "arch logo") Arch: [AUR/minq-ananicy-git](https://aur.archlinux.org/packages/minq-ananicy-git). `paru -S minq-ananicy-git` or `yay -S minq-ananicy-git` should do the trick. Don't forget to start and enable the service by running `sudo systemctl start ananicy.service` and `sudo systemctl enable ananicy.service`.

For more information [click here](https://github.com/kuche1/minq-ananicy#installation-1)

## What's new?

More, updated and better organised rules.
```
```
# Old description

## Description
Ananicy (ANother Auto NICe daemon) — is a shell daemon created to manage processes' [IO](http://linux.die.net/man/1/ionice) and [CPU](http://linux.die.net/man/1/nice) priorities, with community-driven set of rules for popular applications (anyone may add their own rule via github's [pull request](https://help.github.com/articles/using-pull-requests/) mechanism). It's mainly for desktop usage.

I just wanted a tool for auto set programs nice in my system, i.e.:
* Why do I get lag, while compiling kernel and playing games?
* Why does dropbox client eat all my IO?
* Why does torrent/dc client make my laptop run slower?
* ...

Use ananicy to fix these problems!
```
Upstream `LICENSE:1-2`: `GNU GENERAL PUBLIC LICENSE` / `Version 3, 29 June 2007`. GitHub API for nefelim4ag/Ananicy: `'archived': True`, `'license': {'key': 'gpl-3.0', ... 'spdx_id': 'GPL-3.0'}`, `'description': 'Ananicy - is Another auto nice daemon, with community rules support (Use pull request please)'`.

ananicy-cpp `README.md:1-6`:
```
![Ananicy Cpp Logo](./assets/ananicy_logo.svg)

# Ananicy Cpp
[Ananicy](https://github.com/Nefelim4ag/Ananicy) rewritten in C++ for much lower CPU and memory usage.

_Beta status_
```
ananicy-cpp `README.md:57-63`:
```
### Linux
It should be a fully drop-in replacement from Ananicy.
If you detect a difference in behavior (except for bugs in Ananicy that are fixed in `ananicy-cpp`),
please create an issue.

If you want pre-made community rules, you can use the rules from the original Ananicy project.
Simply copy them to your rules directory (by default, `/etc/ananicy.d`).
```
ananicy-cpp `README.md:86` `  - \`wget https://gitlab.com/ananicy-cpp/ananicy-cpp/-/archive/v1.2.0/ananicy-cpp-v1.2.0.tar.gz\``; `README.md:124` `There is also binaries in \`cachyos\` and \`chaotic-aur\`, although \`ananicy-cpp\` is relatively fast to build.`; ananicy-cpp `LICENSE:1-2` GPLv3 text; `fedora/ananicy-cpp.spec:5` `License:        GPLv3`.

ArchWiki "Improving performance" (revid 885186, 2026-09-07), wikitext lines 287-293:
```
==== Ananicy Cpp ====

[https://gitlab.com/ananicy-cpp/ananicy-cpp Ananicy Cpp] ({{Pkg|ananicy-cpp}}) is a daemon for automatically adjusting the nice levels of processes. The nice level represents the priority of the process when allocating CPU resources.

{{Note|[[GameMode]] and Ananicy Cpp both adjust the nice levels of processes. However, combining both tools is not recommended.[https://github.com/CachyOS/ananicy-rules/blob/master/README.md#gamemode--ananicy-cpp--bad-idea]}}

{{Tip|A community-maintained list of Ananicy rules is available on GitHub at [https://github.com/CachyOS/ananicy-rules CachyOS/ananicy-rules], which is packaged as {{AUR|cachyos-ananicy-rules}}.}}
```
ArchWiki "Restic" (revid 883621) wikitext lines 199-207:
```
Alternatively if you are using {{Pkg|ananicy-cpp}} you may want to ensure that the niceness is configured in its configuration file(s) under {{ic|/etc/ananicy.d/}}.

{{hc|/etc/ananicy.d/00-types.types|
{"type":"file-sync","nice":19,"ionice":7}
}}

{{hc|/etc/ananicy.d/99-custom/file-sync/restic.rules|
{"name": "restic", "type": "file-sync"}
}}
```
CachyOS wiki "Gaming" (fetched 2026-09-13), extracted text lines 864-875:
```
Do Not Combine gamemode and ananicy-cpp
…
both trying to modify a process niceness at the same time, it can lead to conflicts and unexpected behavior. If you want to use gamemode, it’s recommended to disable or stop ananicy-cpp first.
To stop ananicy-cpp, execute the following command:
```
(followed by `systemctl stop ananicy-cpp`). ArchWiki search API for "ananicy" (text): totalhits 13 — pages include Improving performance (+ translations), GameMode, Gamescope, Init package guidelines, Restic, PCI passthrough via OVMF/Examples.

(b) Locators: as labelled; commits in the copies table.

(c) Reading: Ananicy self-describes as "ANother Auto NICe daemon … a shell daemon created to manage processes' IO and CPU priorities, with community-driven set of rules for popular applications … mainly for desktop usage" — this text sits under an `# Old description` heading at HEAD; the top of the README now points installation to the `minq-ananicy-git` AUR package / github.com/kuche1/minq-ananicy. Repository github.com/Nefelim4ag/Ananicy is **archived** (last push 2023-03-21); license **GPL-3.0** (LICENSE text is GPLv3; the bibliographic "GPL" is under-specified). ananicy-cpp at gitlab.com/ananicy-cpp/ananicy-cpp: "Ananicy rewritten in C++ for much lower CPU and memory usage", "_Beta status_", "fully drop-in replacement"; license GPLv3 (LICENSE file; GitLab's detector reports "GPL-3.0 or later"; spec says GPLv3); latest tag/release **v1.2.0** (tagged 2026-03-26), HEAD 3 commits past it (2026-08-18). Distribution wikis: ArchWiki documents **Ananicy Cpp** (package `ananicy-cpp`) in "Improving performance" and points to CachyOS/ananicy-rules (AUR `cachyos-ananicy-rules`); some non-English ArchWiki translations still describe the original Ananicy (search snippets, not fetched in full). CachyOS wiki mentions ananicy-cpp only in the gaming page (don't combine with gamemode); the general_system_tweaks, cachyos_settings and FAQ pages have 0 "ananicy" hits.

(d) Verdict: **FOUND**.

---

## Verdict summary

| topic | verdict |
|---|---|
| C-ananicy-rules-1 | FOUND |
| C-ananicy-rules-2 | FOUND (type is named `Player-Audio`; sets nice only) |
| C-ananicy-rules-3 | FOUND |
| C-ananicy-rules-4 | NOT FOUND |
| C-ananicy-rules-5 | PARTIAL (tracker, updatedb absent) |
| C-ananicy-rules-6 | PARTIAL (no compiler entries at pin) |
| C-ananicy-rules-7 | PARTIAL (clamscan, freshclam absent) |
| C-ananicy-rules-8 | FOUND |
| C-ananicy-rules-9 | FOUND |
| C-ananicy-rules-10 | FOUND |
| C-ananicy-rules-11 | FOUND |
| C-ananicy-rules-12 | FOUND |
| C-ananicy-1 | FOUND |
| C-ananicy-2 | FOUND |
| C-ananicy-3 | FOUND |

Counts: FOUND 11 · PARTIAL 3 · NOT FOUND 1 · PREMISE NOT IN SOURCE 0 · COPY UNREACHABLE 0.

---

## Appendix — per-file entry counts (C-ananicy-rules-9), @03ef03fb

Generated by `python3 perfile.py` from strictly-parsed entries (the rejected `Dungeon Drafters.x86_64` line in linux-native_d.rules is not counted; add 1 Game there for ananicy-cpp's loader).

| # | file | entries | entries per type |
|---|---|---|---|
| 1 | 00-default/Audio-Video/SVP.rules | 1 | Player-Video: 1 |
| 2 | 00-default/Audio-Video/acestream.rules | 3 | Player-Video: 3 |
| 3 | 00-default/Audio-Video/ario.rules | 1 | Player-Audio: 1 |
| 4 | 00-default/Audio-Video/audacious.rules | 1 | Player-Audio: 1 |
| 5 | 00-default/Audio-Video/audioserver.rules | 4 | LowLatency_RT: 4 |
| 6 | 00-default/Audio-Video/cava.rules | 1 | Doc-View: 1 |
| 7 | 00-default/Audio-Video/celluloid.rules | 1 | Player-Video: 1 |
| 8 | 00-default/Audio-Video/cider.rules | 1 | Player-Audio: 1 |
| 9 | 00-default/Audio-Video/clementine.rules | 2 | Player-Audio: 2 |
| 10 | 00-default/Audio-Video/cliamp.rules | 1 | Player-Audio: 1 |
| 11 | 00-default/Audio-Video/cmus.rules | 1 | Player-Audio: 1 |
| 12 | 00-default/Audio-Video/cosmic-player.rules | 1 | Player-Video: 1 |
| 13 | 00-default/Audio-Video/deadbeef.rules | 1 | Player-Audio: 1 |
| 14 | 00-default/Audio-Video/easyeffects.rules | 1 | LowLatency_RT: 1 |
| 15 | 00-default/Audio-Video/elisa.rules | 1 | Player-Audio: 1 |
| 16 | 00-default/Audio-Video/feh.rules | 1 | Image-View: 1 |
| 17 | 00-default/Audio-Video/galaxybudsclient.rules | 1 | BG_CPUIO: 1 |
| 18 | 00-default/Audio-Video/gapless.rules | 1 | Player-Audio: 1 |
| 19 | 00-default/Audio-Video/gpu-screen-recorder.rules | 3 | BG_CPUIO: 1, IN_DIFF: 1, LowLatency_RT: 1 |
| 20 | 00-default/Audio-Video/handbrake.rules | 1 | BG_CPUIO: 1 |
| 21 | 00-default/Audio-Video/haruna.rules | 1 | Player-Video: 1 |
| 22 | 00-default/Audio-Video/jellyfin.rules | 2 | Player-Video: 2 |
| 23 | 00-default/Audio-Video/melt.rules | 1 | BG_CPUIO: 1 |
| 24 | 00-default/Audio-Video/mirage.rules | 1 | Image-View: 1 |
| 25 | 00-default/Audio-Video/miru.rules | 1 | Player-Video: 1 |
| 26 | 00-default/Audio-Video/mixxx.rules | 1 | LowLatency_RT: 1 |
| 27 | 00-default/Audio-Video/mpd.rules | 2 | Player-Audio: 1, Service: 1 |
| 28 | 00-default/Audio-Video/mplayer.rules | 1 | Player-Video: 1 |
| 29 | 00-default/Audio-Video/mpv.rules | 1 | Player-Video: 1 |
| 30 | 00-default/Audio-Video/ncmpcpp.rules | 1 | Player-Audio: 1 |
| 31 | 00-default/Audio-Video/parabolic.rules | 1 | BG_CPUIO: 1 |
| 32 | 00-default/Audio-Video/playerctl.rules | 1 | Player-Video: 1 |
| 33 | 00-default/Audio-Video/plex.rules | 1 | Player-Video: 1 |
| 34 | 00-default/Audio-Video/qmmp.rules | 1 | Player-Audio: 1 |
| 35 | 00-default/Audio-Video/rhythmbox.rules | 1 | Player-Audio: 1 |
| 36 | 00-default/Audio-Video/shotwell.rules | 1 | Image-View: 1 |
| 37 | 00-default/Audio-Video/smplayer.rules | 1 | Player-Video: 1 |
| 38 | 00-default/Audio-Video/sopcast.rules | 2 | Player-Video: 2 |
| 39 | 00-default/Audio-Video/soundkonverter.rules | 1 | Heavy_CPU: 1 |
| 40 | 00-default/Audio-Video/spotify.rules | 2 | Player-Audio: 2 |
| 41 | 00-default/Audio-Video/strawberry.rules | 1 | Player-Audio: 1 |
| 42 | 00-default/Audio-Video/stremio.rules | 1 | Player-Video: 1 |
| 43 | 00-default/Audio-Video/swayimg.rules | 1 | Image-View: 1 |
| 44 | 00-default/Audio-Video/tauonmusicbox.rules | 1 | Player-Audio: 1 |
| 45 | 00-default/Audio-Video/tidal-hifi.rules | 1 | Player-Audio: 1 |
| 46 | 00-default/Audio-Video/totem.rules | 1 | Player-Video: 1 |
| 47 | 00-default/Audio-Video/vlc.rules | 1 | Player-Video: 1 |
| 48 | 00-default/Audio-Video/xviewer.rules | 1 | Doc-View: 1 |
| 49 | 00-default/Audio-Video/youtube-dl.rules | 2 | BG_CPUIO: 2 |
| 50 | 00-default/Browsers/browsers.rules | 43 | Doc-View: 41, BG_CPUIO: 2 |
| 51 | 00-default/Browsers/qtwebengine.rules | 1 | Doc-View: 1 |
| 52 | 00-default/Chats/chats.rules | 50 | Chat: 50 |
| 53 | 00-default/Creative/Affinity.rules | 1 | Image-View: 1 |
| 54 | 00-default/Creative/adobe.rules | 6 | Image-View: 3, BG_CPUIO: 2, Service: 1 |
| 55 | 00-default/Creative/ardour.rules | 1 | Player-Audio: 1 |
| 56 | 00-default/Creative/audacity.rules | 2 | Player-Audio: 2 |
| 57 | 00-default/Creative/bitwig-studio.rules | 2 | Player-Audio: 2 |
| 58 | 00-default/Creative/blender.rules | 1 | Heavy_CPU: 1 |
| 59 | 00-default/Creative/davinci.rules | 1 | Heavy_CPU: 1 |
| 60 | 00-default/Creative/gimp.rules | 1 | Image-View: 1 |
| 61 | 00-default/Creative/graphite.rules | 1 | Image-View: 1 |
| 62 | 00-default/Creative/inkscape.rules | 1 | Image-View: 1 |
| 63 | 00-default/Creative/krita.rules | 1 | Image-View: 1 |
| 64 | 00-default/Creative/lmms.rules | 1 | Player-Audio: 1 |
| 65 | 00-default/Creative/obs-studio.rules | 4 | Player-Video: 4 |
| 66 | 00-default/Creative/pixieditor.rules | 1 | Image-View: 1 |
| 67 | 00-default/Creative/reaper.rules | 3 | Player-Audio: 3 |
| 68 | 00-default/DEs-and-WMs/awesome_wm.rules | 1 | LowLatency_RT: 1 |
| 69 | 00-default/DEs-and-WMs/bspwm.rules | 3 | LowLatency_RT: 3 |
| 70 | 00-default/DEs-and-WMs/cinnamon.rules | 1 | LowLatency_RT: 1 |
| 71 | 00-default/DEs-and-WMs/compton-picom.rules | 2 | LowLatency_RT: 2 |
| 72 | 00-default/DEs-and-WMs/cosmic.rules | 30 | LowLatency_RT: 22, BG_CPUIO: 5, Doc-View: 2, OOM_NO_KILL: 1 |
| 73 | 00-default/DEs-and-WMs/dank-material-shell.rules | 2 | Service: 2 |
| 74 | 00-default/DEs-and-WMs/display-link-manager.rules | 1 | LowLatency_RT: 1 |
| 75 | 00-default/DEs-and-WMs/fluxbox.rules | 1 | LowLatency_RT: 1 |
| 76 | 00-default/DEs-and-WMs/gamescope.rules | 3 | LowLatency_RT: 3 |
| 77 | 00-default/DEs-and-WMs/gammastep.rules | 2 | BG_CPUIO: 2 |
| 78 | 00-default/DEs-and-WMs/gdm.rules | 7 | BG_CPUIO: 4, Launcher: 2, LowLatency_RT: 1 |
| 79 | 00-default/DEs-and-WMs/gnome.rules | 32 | Service: 27, LowLatency_RT: 2, BG_CPUIO: 1, Image-View: 1, TODO: 1 |
| 80 | 00-default/DEs-and-WMs/greetd.rules | 8 | BG_CPUIO: 4, Launcher: 4 |
| 81 | 00-default/DEs-and-WMs/i3.rules | 1 | LowLatency_RT: 1 |
| 82 | 00-default/DEs-and-WMs/imv.rules | 5 | Image-View: 5 |
| 83 | 00-default/DEs-and-WMs/jay.rules | 1 | LowLatency_RT: 1 |
| 84 | 00-default/DEs-and-WMs/kupfer.rules | 1 | BG_CPUIO: 1 |
| 85 | 00-default/DEs-and-WMs/lightdm.rules | 1 | Launcher: 1 |
| 86 | 00-default/DEs-and-WMs/lxde.rules | 1 | LowLatency_RT: 1 |
| 87 | 00-default/DEs-and-WMs/lxdm.rules | 2 | BG_CPUIO: 2 |
| 88 | 00-default/DEs-and-WMs/lxqt.rules | 1 | LowLatency_RT: 1 |
| 89 | 00-default/DEs-and-WMs/ly.rules | 1 | Launcher: 1 |
| 90 | 00-default/DEs-and-WMs/mangowm.rules | 1 | LowLatency_RT: 1 |
| 91 | 00-default/DEs-and-WMs/niri.rules | 2 | LowLatency_RT: 2 |
| 92 | 00-default/DEs-and-WMs/noctalia.rules | 2 | LowLatency_RT: 2 |
| 93 | 00-default/DEs-and-WMs/openbox.rules | 1 | LowLatency_RT: 1 |
| 94 | 00-default/DEs-and-WMs/plank.rules | 1 | IN_DIFF: 1 |
| 95 | 00-default/DEs-and-WMs/plasma-login-manager.rules | 2 | Launcher: 2 |
| 96 | 00-default/DEs-and-WMs/plasma.rules | 20 | BG_CPUIO: 7, LowLatency_RT: 6, Service: 5, <no type>: 1, OOM_NO_KILL: 1 |
| 97 | 00-default/DEs-and-WMs/polybar.rules | 1 | Service: 1 |
| 98 | 00-default/DEs-and-WMs/qtile.rules | 1 | LowLatency_RT: 1 |
| 99 | 00-default/DEs-and-WMs/redshift.rules | 1 | BG_CPUIO: 1 |
| 100 | 00-default/DEs-and-WMs/river.rules | 3 | LowLatency_RT: 3 |
| 101 | 00-default/DEs-and-WMs/screenshotter.rules | 10 | Image-View: 10 |
| 102 | 00-default/DEs-and-WMs/sddm.rules | 2 | Launcher: 2 |
| 103 | 00-default/DEs-and-WMs/spectrwm.rules | 1 | LowLatency_RT: 1 |
| 104 | 00-default/DEs-and-WMs/sway.rules | 4 | Service: 3, LowLatency_RT: 1 |
| 105 | 00-default/DEs-and-WMs/swww.rules | 2 | Service: 2 |
| 106 | 00-default/DEs-and-WMs/sxhkd.rules | 0 |  |
| 107 | 00-default/DEs-and-WMs/waybar.rules | 1 | Service: 1 |
| 108 | 00-default/DEs-and-WMs/weston.rules | 1 | LowLatency_RT: 1 |
| 109 | 00-default/DEs-and-WMs/widget-manager.rules | 6 | Doc-View: 6 |
| 110 | 00-default/DEs-and-WMs/wlsunset.rules | 1 | BG_CPUIO: 1 |
| 111 | 00-default/DEs-and-WMs/wpaperd.rules | 1 | BG_CPUIO: 1 |
| 112 | 00-default/DEs-and-WMs/xfce4.rules | 9 | LowLatency_RT: 9 |
| 113 | 00-default/DEs-and-WMs/xmonad.rules | 2 | LowLatency_RT: 1, Service: 1 |
| 114 | 00-default/DEs-and-WMs/xorg.rules | 1 | LowLatency_RT: 1 |
| 115 | 00-default/DEs-and-WMs/xwayland.rules | 1 | LowLatency_RT: 1 |
| 116 | 00-default/Development & Programming/android-studio.rules | 6 | Heavy_CPU: 6 |
| 117 | 00-default/Development & Programming/bruno.rules | 1 | BG_CPUIO: 1 |
| 118 | 00-default/Development & Programming/bun.rules | 1 | BG_CPUIO: 1 |
| 119 | 00-default/Development & Programming/clang-tidy.rules | 1 | BG_CPUIO: 1 |
| 120 | 00-default/Development & Programming/clangd.rules | 2 | Service: 2 |
| 121 | 00-default/Development & Programming/cmake.rules | 1 | BG_CPUIO: 1 |
| 122 | 00-default/Development & Programming/dart_flutter.rules | 2 | Heavy_CPU: 2 |
| 123 | 00-default/Development & Programming/deno.rules | 1 | BG_CPUIO: 1 |
| 124 | 00-default/Development & Programming/gitkraken.rules | 1 | Doc-View: 1 |
| 125 | 00-default/Development & Programming/gnur.rules | 1 | BG_CPUIO: 1 |
| 126 | 00-default/Development & Programming/mongodb_compass.rules | 1 | BG_CPUIO: 1 |
| 127 | 00-default/Development & Programming/mysql-workbench.rules | 2 | BG_CPUIO: 2 |
| 128 | 00-default/Development & Programming/nix.rules | 10 | BG_CPUIO: 10 |
| 129 | 00-default/Development & Programming/node.rules | 1 | BG_CPUIO: 1 |
| 130 | 00-default/Development & Programming/rstudio.rules | 2 | BG_CPUIO: 1, LowLatency_RT: 1 |
| 131 | 00-default/Development & Programming/sqlitebrowser.rules | 1 | BG_CPUIO: 1 |
| 132 | 00-default/Development & Programming/unity.rules | 1 | Heavy_CPU: 1 |
| 133 | 00-default/Document Viewers/FoxitReader.rules | 1 | Doc-View: 1 |
| 134 | 00-default/Document Viewers/okular.rules | 1 | Doc-View: 1 |
| 135 | 00-default/Document Viewers/zathura.rules | 1 | Doc-View: 1 |
| 136 | 00-default/Games/asf.rules | 1 | BG_CPUIO: 1 |
| 137 | 00-default/Games/emulators.rules | 40 | Game: 40 |
| 138 | 00-default/Games/gaming-tools.rules | 11 | BG_CPUIO: 7, Image-View: 2, LowLatency_RT: 1, Service: 1 |
| 139 | 00-default/Games/launchers.rules | 58 | BG_CPUIO: 29, Launcher: 11, Doc-View: 8, Game: 3, LowLatency_RT: 3, Service: 2, Chat: 1, IN_DIFF: 1 |
| 140 | 00-default/Games/linux-native/common.rules | 103 | Game: 92, BG_CPUIO: 8, Service: 3 |
| 141 | 00-default/Games/linux-native/linux-native_a.rules | 123 | Game: 118, BG_CPUIO: 4, Service: 1 |
| 142 | 00-default/Games/linux-native/linux-native_b.rules | 120 | Game: 119, BG_CPUIO: 1 |
| 143 | 00-default/Games/linux-native/linux-native_c.rules | 133 | Game: 125, BG_CPUIO: 5, Service: 3 |
| 144 | 00-default/Games/linux-native/linux-native_d.rules | 135 | Game: 134, Service: 1 |
| 145 | 00-default/Games/linux-native/linux-native_e.rules | 56 | Game: 56 |
| 146 | 00-default/Games/linux-native/linux-native_f.rules | 73 | Game: 73 |
| 147 | 00-default/Games/linux-native/linux-native_g.rules | 68 | Game: 68 |
| 148 | 00-default/Games/linux-native/linux-native_h.rules | 123 | Game: 122, Service: 1 |
| 149 | 00-default/Games/linux-native/linux-native_i.rules | 72 | Game: 72 |
| 150 | 00-default/Games/linux-native/linux-native_j.rules | 16 | Game: 16 |
| 151 | 00-default/Games/linux-native/linux-native_k.rules | 42 | Game: 42 |
| 152 | 00-default/Games/linux-native/linux-native_l.rules | 69 | Game: 69 |
| 153 | 00-default/Games/linux-native/linux-native_m.rules | 108 | Game: 108 |
| 154 | 00-default/Games/linux-native/linux-native_n.rules | 36 | Game: 35, Service: 1 |
| 155 | 00-default/Games/linux-native/linux-native_numerical.rules | 16 | Game: 15, Service: 1 |
| 156 | 00-default/Games/linux-native/linux-native_o.rules | 46 | Game: 46 |
| 157 | 00-default/Games/linux-native/linux-native_p.rules | 102 | Game: 101, Service: 1 |
| 158 | 00-default/Games/linux-native/linux-native_q.rules | 13 | Game: 13 |
| 159 | 00-default/Games/linux-native/linux-native_r.rules | 80 | Game: 78, LowLatency_RT: 1, Service: 1 |
| 160 | 00-default/Games/linux-native/linux-native_s.rules | 262 | Game: 257, Service: 5 |
| 161 | 00-default/Games/linux-native/linux-native_t.rules | 135 | Game: 135 |
| 162 | 00-default/Games/linux-native/linux-native_the.rules | 109 | Game: 109 |
| 163 | 00-default/Games/linux-native/linux-native_u.rules | 38 | Game: 37, Service: 1 |
| 164 | 00-default/Games/linux-native/linux-native_v.rules | 32 | Game: 28, BG_CPUIO: 2, Service: 2 |
| 165 | 00-default/Games/linux-native/linux-native_w.rules | 70 | Game: 67, BG_CPUIO: 3 |
| 166 | 00-default/Games/linux-native/linux-native_x.rules | 15 | Game: 15 |
| 167 | 00-default/Games/linux-native/linux-native_y.rules | 16 | Game: 16 |
| 168 | 00-default/Games/linux-native/linux-native_z.rules | 16 | Game: 16 |
| 169 | 00-default/Games/linux-native/non-latin/linux-native_chinese.rules | 10 | Game: 10 |
| 170 | 00-default/Games/linux-native/non-latin/linux-native_non-latin.rules | 4 | Game: 4 |
| 171 | 00-default/Games/mednaffe.rules | 1 | BG_CPUIO: 1 |
| 172 | 00-default/Games/steam-shader-compilation.rules | 1 | BG_CPUIO: 1 |
| 173 | 00-default/Games/ue4.rules | 4 | BG_CPUIO: 4 |
| 174 | 00-default/Games/waydroid.rules | 9 | Game: 9 |
| 175 | 00-default/Games/wine.rules | 4 | BG_CPUIO: 4 |
| 176 | 00-default/Games/wine_proton/common.rules | 704 | Game: 562, BG_CPUIO: 135, Service: 6, Doc-View: 1 |
| 177 | 00-default/Games/wine_proton/non-latin/wine_proton_chinese.rules | 278 | Game: 261, BG_CPUIO: 16, Service: 1 |
| 178 | 00-default/Games/wine_proton/non-latin/wine_proton_japanese.rules | 70 | Game: 69, BG_CPUIO: 1 |
| 179 | 00-default/Games/wine_proton/non-latin/wine_proton_non-latin.rules | 11 | Game: 11 |
| 180 | 00-default/Games/wine_proton/wine_proton_a.rules | 671 | Game: 612, BG_CPUIO: 57, Service: 2 |
| 181 | 00-default/Games/wine_proton/wine_proton_b.rules | 629 | Game: 554, BG_CPUIO: 75 |
| 182 | 00-default/Games/wine_proton/wine_proton_c.rules | 751 | Game: 684, BG_CPUIO: 61, Service: 6 |
| 183 | 00-default/Games/wine_proton/wine_proton_d.rules | 760 | Game: 672, BG_CPUIO: 87, Service: 1 |
| 184 | 00-default/Games/wine_proton/wine_proton_e.rules | 324 | Game: 282, BG_CPUIO: 41, Service: 1 |
| 185 | 00-default/Games/wine_proton/wine_proton_f.rules | 564 | Game: 510, BG_CPUIO: 54 |
| 186 | 00-default/Games/wine_proton/wine_proton_g.rules | 418 | Game: 364, BG_CPUIO: 52, Launcher: 1, Service: 1 |
| 187 | 00-default/Games/wine_proton/wine_proton_h.rules | 447 | Game: 393, BG_CPUIO: 51, Service: 3 |
| 188 | 00-default/Games/wine_proton/wine_proton_i.rules | 298 | Game: 273, BG_CPUIO: 24, Service: 1 |
| 189 | 00-default/Games/wine_proton/wine_proton_j.rules | 90 | Game: 84, BG_CPUIO: 6 |
| 190 | 00-default/Games/wine_proton/wine_proton_k.rules | 213 | Game: 193, BG_CPUIO: 20 |
| 191 | 00-default/Games/wine_proton/wine_proton_l.rules | 420 | Game: 368, BG_CPUIO: 52 |
| 192 | 00-default/Games/wine_proton/wine_proton_m.rules | 743 | Game: 648, BG_CPUIO: 94, Service: 1 |
| 193 | 00-default/Games/wine_proton/wine_proton_n.rules | 328 | Game: 294, BG_CPUIO: 31, Service: 3 |
| 194 | 00-default/Games/wine_proton/wine_proton_numerical.rules | 78 | Game: 69, BG_CPUIO: 8, Service: 1 |
| 195 | 00-default/Games/wine_proton/wine_proton_o.rules | 253 | Game: 232, BG_CPUIO: 21 |
| 196 | 00-default/Games/wine_proton/wine_proton_p.rules | 577 | Game: 509, BG_CPUIO: 63, Service: 4, Heavy_CPU: 1 |
| 197 | 00-default/Games/wine_proton/wine_proton_q.rules | 30 | Game: 28, BG_CPUIO: 2 |
| 198 | 00-default/Games/wine_proton/wine_proton_r.rules | 544 | Game: 482, BG_CPUIO: 57, Service: 5 |
| 199 | 00-default/Games/wine_proton/wine_proton_s.rules | 1358 | Game: 1215, BG_CPUIO: 131, Service: 12 |
| 200 | 00-default/Games/wine_proton/wine_proton_t.rules | 640 | Game: 597, BG_CPUIO: 42, Service: 1 |
| 201 | 00-default/Games/wine_proton/wine_proton_the.rules | 523 | Game: 447, BG_CPUIO: 74, Service: 2 |
| 202 | 00-default/Games/wine_proton/wine_proton_u.rules | 159 | Game: 140, BG_CPUIO: 19 |
| 203 | 00-default/Games/wine_proton/wine_proton_v.rules | 168 | Game: 134, BG_CPUIO: 32, Service: 2 |
| 204 | 00-default/Games/wine_proton/wine_proton_w.rules | 455 | Game: 395, BG_CPUIO: 60 |
| 205 | 00-default/Games/wine_proton/wine_proton_x.rules | 30 | Game: 27, BG_CPUIO: 3 |
| 206 | 00-default/Games/wine_proton/wine_proton_y.rules | 98 | Game: 91, BG_CPUIO: 4, Service: 3 |
| 207 | 00-default/Games/wine_proton/wine_proton_z.rules | 90 | Game: 80, BG_CPUIO: 10 |
| 208 | 00-default/Games/wineserver.rules | 1 | LowLatency_RT: 1 |
| 209 | 00-default/Networking/amule.rules | 1 | BG_CPUIO: 1 |
| 210 | 00-default/Networking/aria2c.rules | 1 | BG_CPUIO: 1 |
| 211 | 00-default/Networking/bind.rules | 1 | BG_CPUIO: 1 |
| 212 | 00-default/Networking/curl.rules | 1 | BG_CPUIO: 1 |
| 213 | 00-default/Networking/deluge.rules | 3 | BG_CPUIO: 3 |
| 214 | 00-default/Networking/dnsmasq.rules | 1 | Doc-View: 1 |
| 215 | 00-default/Networking/dropbox.rules | 1 | BG_CPUIO: 1 |
| 216 | 00-default/Networking/gerbera.rules | 1 | BG_CPUIO: 1 |
| 217 | 00-default/Networking/insync.rules | 1 | BG_CPUIO: 1 |
| 218 | 00-default/Networking/kbfsfuse.rules | 1 | BG_CPUIO: 1 |
| 219 | 00-default/Networking/kdeconnect.rules | 2 | BG_CPUIO: 2 |
| 220 | 00-default/Networking/kget.rules | 1 | BG_CPUIO: 1 |
| 221 | 00-default/Networking/ktorrent.rules | 1 | BG_CPUIO: 1 |
| 222 | 00-default/Networking/linphone.rules | 1 | LowLatency_RT: 1 |
| 223 | 00-default/Networking/localsend.rules | 1 | BG_CPUIO: 1 |
| 224 | 00-default/Networking/megasync.rules | 1 | BG_CPUIO: 1 |
| 225 | 00-default/Networking/mistserver.rules | 8 | LowLatency_RT: 7, BG_CPUIO: 1 |
| 226 | 00-default/Networking/nextcloud.rules | 1 | BG_CPUIO: 1 |
| 227 | 00-default/Networking/nextdns.rules | 1 | LowLatency_RT: 1 |
| 228 | 00-default/Networking/onedrive.rules | 1 | BG_CPUIO: 1 |
| 229 | 00-default/Networking/owncloud.rules | 1 | BG_CPUIO: 1 |
| 230 | 00-default/Networking/parsec.rules | 1 | LowLatency_RT: 1 |
| 231 | 00-default/Networking/qBittorrent.rules | 2 | BG_CPUIO: 2 |
| 232 | 00-default/Networking/rclone.rules | 1 | BG_CPUIO: 1 |
| 233 | 00-default/Networking/remote-viewer.rules | 1 | LowLatency_RT: 1 |
| 234 | 00-default/Networking/rtorrent.rules | 1 | BG_CPUIO: 1 |
| 235 | 00-default/Networking/sabnzbd.rules | 1 | BG_CPUIO: 1 |
| 236 | 00-default/Networking/samba.rules | 2 | LowLatency_RT: 2 |
| 237 | 00-default/Networking/soulseekqt.rules | 1 | Doc-View: 1 |
| 238 | 00-default/Networking/ssh.rules | 4 | BG_CPUIO: 4 |
| 239 | 00-default/Networking/syncthing.rules | 2 | BG_CPUIO: 2 |
| 240 | 00-default/Networking/tixati.rules | 1 | BG_CPUIO: 1 |
| 241 | 00-default/Networking/tor.rules | 1 | Service: 1 |
| 242 | 00-default/Networking/transmission.rules | 6 | BG_CPUIO: 6 |
| 243 | 00-default/Networking/virtnetworkd.rules | 1 | Service: 1 |
| 244 | 00-default/Networking/wget.rules | 1 | BG_CPUIO: 1 |
| 245 | 00-default/Productivity & Office/anki.rules | 1 | Doc-View: 1 |
| 246 | 00-default/Productivity & Office/boinc.rules | 1 | Heavy_CPU: 1 |
| 247 | 00-default/Productivity & Office/calibre.rules | 3 | Doc-View: 3 |
| 248 | 00-default/Productivity & Office/cherrytree.rules | 1 | Doc-View: 1 |
| 249 | 00-default/Productivity & Office/evince.rules | 1 | Doc-View: 1 |
| 250 | 00-default/Productivity & Office/foliate.rules | 1 | Doc-View: 1 |
| 251 | 00-default/Productivity & Office/freeoffice.rules | 3 | Doc-View: 3 |
| 252 | 00-default/Productivity & Office/joplin.rules | 1 | Doc-View: 1 |
| 253 | 00-default/Productivity & Office/keepassxc.rules | 1 | Doc-View: 1 |
| 254 | 00-default/Productivity & Office/libreoffice.rules | 4 | Doc-View: 4 |
| 255 | 00-default/Productivity & Office/logseq.rules | 1 | Doc-View: 1 |
| 256 | 00-default/Productivity & Office/notesnook.rules | 1 | Doc-View: 1 |
| 257 | 00-default/Productivity & Office/onlyoffice.rules | 1 | Doc-View: 1 |
| 258 | 00-default/Productivity & Office/openscad.rules | 1 | Heavy_CPU: 1 |
| 259 | 00-default/Productivity & Office/quiterss.rules | 1 | Doc-View: 1 |
| 260 | 00-default/Productivity & Office/zim.rules | 1 | Doc-View: 1 |
| 261 | 00-default/Services/accountsd.rules | 1 | Service: 1 |
| 262 | 00-default/Services/amazon-cloudwatch-agent.rules | 1 | LowLatency_RT: 1 |
| 263 | 00-default/Services/asusd.rules | 2 | BG_CPUIO: 2 |
| 264 | 00-default/Services/avahi.rules | 1 | BG_CPUIO: 1 |
| 265 | 00-default/Services/bluetoothd.rules | 2 | BG_CPUIO: 2 |
| 266 | 00-default/Services/coolercontrold.rules | 1 | Service: 1 |
| 267 | 00-default/Services/dbus.rules | 3 | Service: 3 |
| 268 | 00-default/Services/dmemcg-booster.rules | 3 | Service: 3 |
| 269 | 00-default/Services/firewalld.rules | 1 | BG_CPUIO: 1 |
| 270 | 00-default/Services/ghelper.rules | 1 | BG_CPUIO: 1 |
| 271 | 00-default/Services/gvfs.rules | 13 | Service: 13 |
| 272 | 00-default/Services/kde-material-you-colors.rules | 1 | Service: 1 |
| 273 | 00-default/Services/keyd.rules | 1 | LowLatency_RT: 1 |
| 274 | 00-default/Services/kubo.rules | 1 | BG_CPUIO: 1 |
| 275 | 00-default/Services/misc-services.rules | 11 | Service: 10, BG_CPUIO: 1 |
| 276 | 00-default/Services/networkmanager.rules | 1 | BG_CPUIO: 1 |
| 277 | 00-default/Services/nginx.rules | 1 | LowLatency_RT: 1 |
| 278 | 00-default/Services/openrazer.rules | 1 | BG_CPUIO: 1 |
| 279 | 00-default/Services/piri.rules | 1 | Service: 1 |
| 280 | 00-default/Services/polkit.rules | 8 | Service: 8 |
| 281 | 00-default/Services/proton-mail-bridge.rules | 2 | BG_CPUIO: 2 |
| 282 | 00-default/Services/speech-services.rules | 8 | Service: 8 |
| 283 | 00-default/Services/xdg.rules | 11 | Service: 11 |
| 284 | 00-default/Services/xmousepasteblock.rules | 1 | Service: 1 |
| 285 | 00-default/System Utilities & Maintenance/FileRoller.rules | 1 | BG_CPUIO: 1 |
| 286 | 00-default/System Utilities & Maintenance/ark.rules | 1 | BG_CPUIO: 1 |
| 287 | 00-default/System Utilities & Maintenance/bees.rules | 1 | BG_CPUIO: 1 |
| 288 | 00-default/System Utilities & Maintenance/blueman-blueberry.rules | 2 | BG_CPUIO: 2 |
| 289 | 00-default/System Utilities & Maintenance/borg.rules | 1 | BG_CPUIO: 1 |
| 290 | 00-default/System Utilities & Maintenance/clamav.rules | 2 | BG_CPUIO: 1, Service: 1 |
| 291 | 00-default/System Utilities & Maintenance/collectd.rules | 1 | BG_CPUIO: 1 |
| 292 | 00-default/System Utilities & Maintenance/damx.rules | 1 | BG_CPUIO: 1 |
| 293 | 00-default/System Utilities & Maintenance/dupeguru.rules | 1 | Heavy_CPU: 1 |
| 294 | 00-default/System Utilities & Maintenance/duperemove.rules | 1 | BG_CPUIO: 1 |
| 295 | 00-default/System Utilities & Maintenance/fail2ban-server.rules | 1 | BG_CPUIO: 1 |
| 296 | 00-default/System Utilities & Maintenance/fdupes.rules | 1 | BG_CPUIO: 1 |
| 297 | 00-default/System Utilities & Maintenance/kopia.rules | 2 | BG_CPUIO: 2 |
| 298 | 00-default/System Utilities & Maintenance/nvdock.rules | 1 | BG_CPUIO: 1 |
| 299 | 00-default/System Utilities & Maintenance/projecteur.rules | 1 | BG_CPUIO: 1 |
| 300 | 00-default/System Utilities & Maintenance/psensor.rules | 1 | BG_CPUIO: 1 |
| 301 | 00-default/System Utilities & Maintenance/recoll.rules | 1 | BG_CPUIO: 1 |
| 302 | 00-default/System Utilities & Maintenance/restic.rules | 1 | BG_CPUIO: 1 |
| 303 | 00-default/System Utilities & Maintenance/rmlint.rules | 1 | BG_CPUIO: 1 |
| 304 | 00-default/System Utilities & Maintenance/thrash-protect.rules | 1 | <no type>: 1 |
| 305 | 00-default/System Utilities & Maintenance/tiny-rdm.rules | 1 | BG_CPUIO: 1 |
| 306 | 00-default/System Utilities & Maintenance/unison.rules | 1 | BG_CPUIO: 1 |
| 307 | 00-default/System Utilities & Maintenance/xarchiver.rules | 1 | BG_CPUIO: 1 |
| 308 | 00-default/Terminals & Shells/bash.rules | 1 | Doc-View: 1 |
| 309 | 00-default/Terminals & Shells/dash.rules | 1 | Doc-View: 1 |
| 310 | 00-default/Terminals & Shells/fish.rules | 1 | Doc-View: 1 |
| 311 | 00-default/Terminals & Shells/guake.rules | 1 | Doc-View: 1 |
| 312 | 00-default/Terminals & Shells/ksh.rules | 1 | Doc-View: 1 |
| 313 | 00-default/Terminals & Shells/nu.rules | 1 | Doc-View: 1 |
| 314 | 00-default/Terminals & Shells/tcsh.rules | 1 | Doc-View: 1 |
| 315 | 00-default/Terminals & Shells/terminal.rules | 21 | Doc-View: 21 |
| 316 | 00-default/Terminals & Shells/tilix.rules | 1 | Doc-View: 1 |
| 317 | 00-default/Terminals & Shells/tmux.rules | 1 | Doc-View: 1 |
| 318 | 00-default/Terminals & Shells/tuifm.rules | 2 | Doc-View: 2 |
| 319 | 00-default/Terminals & Shells/zsh.rules | 1 | Doc-View: 1 |
| 320 | 00-default/Text Editors/texteditors.rules | 39 | Doc-View: 28, Heavy_CPU: 11 |
| 321 | 00-default/Tools/7z.rules | 4 | BG_CPUIO: 2, Doc-View: 2 |
| 322 | 00-default/Tools/alarm-clock.rules | 1 | BG_CPUIO: 1 |
| 323 | 00-default/Tools/auto-cpufreq.rules | 1 | BG_CPUIO: 1 |
| 324 | 00-default/Tools/chrony.rules | 1 | BG_CPUIO: 1 |
| 325 | 00-default/Tools/corectrl.rules | 2 | BG_CPUIO: 1, LowLatency_RT: 1 |
| 326 | 00-default/Tools/cpu-x.rules | 1 | BG_CPUIO: 1 |
| 327 | 00-default/Tools/cups.rules | 2 | BG_CPUIO: 2 |
| 328 | 00-default/Tools/distrobox.rules | 1 | Service: 1 |
| 329 | 00-default/Tools/doublecmd.rules | 1 | Doc-View: 1 |
| 330 | 00-default/Tools/fahclient.rules | 1 | Heavy_CPU: 1 |
| 331 | 00-default/Tools/ffmpeg.rules | 1 | Heavy_CPU: 1 |
| 332 | 00-default/Tools/github_copilot.rules | 1 | BG_CPUIO: 1 |
| 333 | 00-default/Tools/imgbrd-grabber.rules | 1 | BG_CPUIO: 1 |
| 334 | 00-default/Tools/meld.rules | 1 | BG_CPUIO: 1 |
| 335 | 00-default/Tools/midnight-commander.rules | 1 | Doc-View: 1 |
| 336 | 00-default/Tools/openrgb.rules | 1 | BG_CPUIO: 1 |
| 337 | 00-default/Tools/podman.rules | 1 | Service: 1 |
| 338 | 00-default/Tools/ppd.rules | 1 | BG_CPUIO: 1 |
| 339 | 00-default/Tools/qemu.rules | 2 | Heavy_CPU: 2 |
| 340 | 00-default/Tools/qimgv.rules | 1 | Image-View: 1 |
| 341 | 00-default/Tools/rsync.rules | 1 | BG_CPUIO: 1 |
| 342 | 00-default/Tools/smartd.rules | 1 | BG_CPUIO: 1 |
| 343 | 00-default/Tools/smartgit.rules | 1 | Doc-View: 1 |
| 344 | 00-default/Tools/system-monitoring.rules | 6 | Doc-View: 6 |
| 345 | 00-default/Tools/thermald.rules | 1 | BG_CPUIO: 1 |
| 346 | 00-default/Tools/thinkfan.rules | 1 | BG_CPUIO: 1 |
| 347 | 00-default/Tools/tlp.rules | 3 | BG_CPUIO: 3 |
| 348 | 00-default/Tools/tuned.rules | 2 | BG_CPUIO: 2 |
| 349 | 00-default/Tools/uptimed.rules | 1 | BG_CPUIO: 1 |
| 350 | 00-default/Tools/vmware.rules | 2 | Heavy_CPU: 2 |
| 351 | 00-default/Tools/watchman.rules | 1 | IN_DIFF: 1 |
| 352 | 00-default/Tools/wl-clipboard.rules | 2 | Service: 2 |
| 353 | 00-default/VPN/amneziavpn.rules | 1 | IN_DIFF: 1 |
| 354 | 00-default/VPN/hummingbird.rules | 1 | LowLatency_RT: 1 |
| 355 | 00-default/VPN/ivpn.rules | 2 | IN_DIFF: 2 |
| 356 | 00-default/VPN/mullvadvpn.rules | 2 | IN_DIFF: 2 |
| 357 | 00-default/VPN/openvpn.rules | 1 | LowLatency_RT: 1 |
| 358 | 00-default/VPN/protonvpn.rules | 1 | IN_DIFF: 1 |
| 359 | 00-default/VPN/tailscale.rules | 1 | LowLatency_RT: 1 |
| 360 | 00-default/VPN/wireguard.rules | 2 | LowLatency_RT: 2 |
| 361 | 00-default/VPN/zerotier-one.rules | 1 | LowLatency_RT: 1 |
