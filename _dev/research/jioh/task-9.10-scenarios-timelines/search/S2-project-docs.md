# S2 — primary project and vendor documentation and source code

Reader class S2 for task 9.10 (scenarios and timelines), stage 2. Topics of this class: T3 (browser windows, tabs and renderer processes), T4 (games and their companions on Linux), T5 (background jobs a desktop runs unasked), T7 (desktop scenario benchmarks), T8 (process names on Linux), T10 (rates of operations in real use, and a video call's processes). All searches and copies were made on 2026-10-01. Source copies are under `sources/S2-NN/` (gitignored); every passage below is quoted from those copies, so the record stands without them.

Conventions used in this record:

- **Verbatim blocks.** Each fenced block is copied byte-for-byte from the named file of the copy (tabs kept). Where a block is prefixed `N:` it is `grep -n` output: the number is the line in the file, the text after the first colon is verbatim. PDF text was extracted with `pypdf` 6.18.0 (`PdfReader(...).pages[i].extract_text()`) into a `.txt` beside the PDF; HTML pages were converted to text by stripping tags (`re.sub(r'<[^>]+>','\n', ...)` then `html.unescape`); the quoted line numbers of PDFs and HTML pages refer to those `.txt` conversions, and the page number of the PDF is given as well.
- **"Supports existence only."** A vendor page, a package or a source tree shows that a scenario, setting, timer, job or name exists and what it is configured to do; how often it runs on real machines, how long it takes and what users do needs an observation. Every coverage statement says which applies.
- **Reader's own computations** are labelled as such, with the command. They locate a candidate; they are not values.

## 1. Search log

All rows dated 2026-10-01. "200" etc. are HTTP status codes.

| # | Engine or venue | Query terms or request | Hits followed | Dead ends (status) |
|---|---|---|---|---|
| 1 | releases.ubuntu.com | directory listing `/24.04/` | `ubuntu-24.04.5.1-desktop-amd64.manifest` (200), `.list` (200) | — |
| 2 | releases.ubuntu.com | HTTP range requests (`curl -r`) into `ubuntu-24.04.5.1-desktop-amd64.iso`, Joliet directory `casper/` read by a small reader script | `casper/install-sources.yaml`, `minimal.manifest`, `minimal.standard.manifest`, `minimal.standard.live.manifest` (all fetched) | first attempt with Python `urllib` failed on TLS certificate verification (no HTTP status); switched to `curl` |
| 3 | archive.ubuntu.com pool | `pool/main/u/ubuntu-meta/` | `ubuntu-meta_1.539.2.tar.xz` (200) | — |
| 4 | packages.ubuntu.com | `noble-updates/nautilus` | dependency list (200) | — |
| 5 | archive.ubuntu.com pool | `.deb` of apt, dpkg, e2fsprogs, util-linux, fwupd, logrotate, man-db, anacron, systemd, update-notifier-common, base-files, sysstat, snapd, tracker-miner-fs, tracker-extract, unattended-upgrades, cron, apport, deja-dup, clamav, clamav-daemon, clamav-freshclam, dkms, ubuntu-settings at the versions in the 24.04.5.1 manifest | all 200 | `pool/main/p/plocate/plocate_1.1.19-2ubuntu2_amd64.deb` 404 → found in `pool/universe` (200) |
| 6 | packages.ubuntu.com | version pages `noble`/`noble-updates` for dkms, plocate, clamav-freshclam, v4l2loopback-dkms, virtualbox-dkms, zfs-dkms, nvidia-dkms-580, nvidia-dkms-570, nvidia-kernel-source-580, nvidia-dkms-580-open | versions read (200) | `noble-updates/dkms` and `noble-updates/plocate` pages carry no package (not updated) |
| 7 | gitlab.gnome.org | `GNOME/localsearch` (formerly tracker-miners), tag `3.7.1`, shallow clone | commit eae431ef | — |
| 8 | invent.kde.org | `frameworks/baloo` tags (`git ls-remote`), clone `v6.30.0` | commit a5b82987 | — |
| 9 | src.fedoraproject.org | `rpms/fedora-release` branch `f44` clone | commit 81836008 | — |
| 10 | pagure.io → forge.fedoraproject.org | fedora-comps `comps-f44.xml.in` | `forge.fedoraproject.org/releng/fedora-comps/raw/branch/main/comps-f44.xml.in` (200); repository found through the Forgejo API `repos/search?q=fedora-comps` (200) | `pagure.io/fedora-comps/raw/main/f/comps-f44.xml.in` 404; `.../raw/master/...` 404; `pagure.io/fedora-comps/tree/` 404; `git clone --depth 1 https://pagure.io/fedora-comps.git` refused ("dumb http transport does not support shallow capabilities"); a `git ls-remote` loop against pagure and forge hung on a credential prompt and was stopped |
| 11 | WebSearch | `fedora-comps repository comps-f44.xml.in` | pagure.io/fedora-comps (pointer only) | — |
| 12 | github.com | `rpm-software-management/dnf5` tag `5.4.6.0` clone; src.fedoraproject.org `rpms/dnf5/raw/f44/f/dnf5.spec` | commit 1b2de4bd; spec (200) | — |
| 13 | gitlab.gnome.org | `GNOME/gnome-software` tag `50.4` (version in Fedora 44 spec, 200) | commit eda622ea | — |
| 14 | raw.githubusercontent.com | `canonical/snapd` tag `2.76.3` `overlord/snapstate/autorefresh.go` | 200 | — |
| 15 | archlinux.org, gitlab.archlinux.org | package JSON and file lists of shadow, man-db, archlinux-keyring, systemd, plocate, logrotate, util-linux, pacman-contrib, fwupd, localsearch, baloo; raw `shadow.timer`, `shadow.service`, `archlinux-keyring-wkd-sync.timer`, man-db `PKGBUILD` at the package tags | all 200 | — |
| 16 | packages.debian.org, sources.debian.org | `trixie/task-desktop`, `trixie/task-gnome-desktop`; `api/src/<pkg>`; `data/main/t/tasksel/3.81/debian/control` | all 200 | — |
| 17 | raw.githubusercontent.com | `torvalds/linux` tags `v6.8`, `v7.0`: `include/linux/sched.h`, `fs/exec.c`; `v6.8` `fs/binfmt_script.c`, `kernel/sys.c` | all 200 | — |
| 18 | packages.ubuntu.com | `<suite>/amd64/<pkg>/filelist` for 52 packages (list in S2-12) | 200 | one connection timeout (`curl: (28)`) retried; `gamescope` has no noble package (search page shows questing and resolute only) |
| 19 | WebSearch | `PCMark 10 technical guide pdf workloads Essentials Productivity Digital Content Creation` | benchmarks.ul.com/pcmark10; s3.amazonaws.com `download-aws.futuremark.com/PCMark_10_Technical_Guide.pdf` (200, application/pdf) | the product page links only a support-site user guide |
| 20 | WebSearch | `UL Procyon office productivity benchmark technical guide pdf workloads Word Excel PowerPoint Outlook`; `"Procyon" "Office Productivity Benchmark" workloads Outlook "backing up" technical guide workload details` | benchmarks.ul.com/procyon/{office-productivity,video-editing,photo-editing,ai-text-generation,battery-life}-benchmark (200); support.benchmarks.ul.com overview articles 44002262462, 44002123509, 44002117336 (200) | no technical-guide PDF found for Procyon |
| 21 | WebSearch | `BAPCo SYSmark 30 white paper scenarios applications` | bapco.com/sysmark-30 | bapco.com 403 (curl, also with a browser user agent); WebFetch 403. Wayback `web/2026id_/https://bapco.com/sysmark-30/` 200 → `bapco-sysmark30-whitepaper-v1.2.pdf` direct 403, Wayback 200 |
| 22 | WebSearch | `SYSmark 25 whitepaper pdf bapco.com wp-content uploads` | attachment page bapco_sysmark_25_white_paper_1-1 (Wayback 200) → PDF `wp-content/uploads/2022/11/bapco_sysmark_25_white_paper_1.1.pdf` | PDF: direct 403, WebFetch 403, Wayback 404 for timestamps 2022–2026 (all resolve to capture 20240630003735, 404); user guide v1.9 PDF Wayback 404; one Wayback connection failure (`curl: (7)`); Wayback CDX API "Temporarily Offline" page. Release page `bapco-releases-sysmark-25` Wayback 200 |
| 23 | WebSearch | `SYSmark 2018 white paper pdf "Productivity" "Creativity" "Responsiveness" scenarios applications` | release page (Wayback 200); end-of-life product page (Wayback 200; links only user guides and benchmarking rules) | white paper PDF not located |
| 24 | WebSearch | `CpsMark+ benchmark scenarios`; `"CPSMark" OR "CpsMark+" PC benchmark`; extended `"CpsMark" benchmark` | the third found the defining article: BenchCouncil Transactions on Benchmarks, Standards and Evaluations, doi 10.1016/j.tbench.2023.100084 | sciencedirect.com 403 (curl with browser UA; WebFetch 403); `api.elsevier.com/...?httpAccept=text/plain` 400 (INVALID_INPUT); OpenAlex (200) lists it as open access, `pdf_url` none; Wayback capture is a captcha page; Wayback `.../pdfft` 404. Not read |
| 25 | chromiumdash.appspot.com; raw.githubusercontent.com | `fetch_releases?channel=Stable&platform=Linux` (200 → 154.0.8037.92); `chromium/chromium` tag `154.0.8037.92` files listed in S2-16 | all 200 | `services/audio/audio_manager_power_user.cc` 404; `content/browser/utility_process_host.cc` 404 (paths guessed, not needed) |
| 26 | product-details.mozilla.org; raw.githubusercontent.com | `firefox_versions.json` (200 → 157.0); `mozilla-firefox/firefox` tag `FIREFOX_157_0_RELEASE` files listed in S2-17 | all 200 | — |
| 27 | gitlab.winehq.org; github.com | Wine tags; raw `wine-11.0` `dlls/ntdll/unix/{loader,thread}.c`; sparse clone `wine-11.0` (loader, ntdll/unix); `ValveSoftware/wine` tag `proton-wine-11.0-2c`; `ValveSoftware/Proton` tag `proton-11.0-2c` `proton` | all 200 / clones ok | GitLab code search API 401 |
| 28 | gitlab.steamos.cloud | `steamrt/steam-runtime-tools` tag `v0.20260925.0`: `docs/container-runtime.md`, `docs/slr-for-game-developers.md`, `docs/steam-compat-tool-interface.md`, `pressure-vessel/wrap.1.md` | all 200 | — |
| 29 | WebSearch | `Steam client "Allow downloads during gameplay" setting help.steampowered.com` | help.steampowered.com FAQs 71AB-698D-57EB-178C, 163C-7C89-406E-2F63 (200) | — |
| 30 | WebSearch | `Steam client update notes "downloads during gameplay" default store.steampowered.com news app 593110` | nine store.steampowered.com news pages (all 200) | none of the nine contained "during gameplay" or similar; discarded |
| 31 | github.com | `ValveSoftware/gamescope` tag `3.16.31` clone | commit 6867f509 | — |
| 32 | gitlab.gnome.org | `GNOME/mutter` tag `46.2` sparse clone | commit 02050414 | — |
| 33 | WebSearch | `Firefox telemetry share of Linux users on Wayland vs X11 percentage` | phoronix.com news (403); firefoxgraphics.github.io/telemetry (200) → `analysis-output.telemetry.mozilla.org/gfx/telemetry-data/linux-statistics.json` (200) | the JSON carries driver vendors, compositors and Firefox versions but no window-protocol field; discarded. `firefoxgraphics.github.io/telemetry/data/linux-statistics.json` 404 |
| 34 | archive.ubuntu.com pool | DKMS module packages (v4l2loopback-dkms, virtualbox-dkms, zfs-dkms, nvidia-kernel-source-580, nvidia-dkms-580) | all 200 | `pool/main/z/zfs-linux/zfs-dkms_...` 404 → `pool/universe` 200 |
| 35 | github.com; packages.microsoft.com; dl.google.com | `microsoft/vscode` tag `1.140.0` raw files; Microsoft `code` Packages index; Google Chrome Packages index; both `.deb` streamed and listed | all 200; streamed SHA-256 equal to the index values | — |
| 36 | github.com (Flathub); cdn.zoom.us; repo.steampowered.com | Flathub manifests of us.zoom.Zoom, com.slack.Slack, com.discordapp.Discord, com.spotify.Client, im.riot.Riot, com.valvesoftware.Steam, com.github.IsmaelMartinez.teams_for_linux at their HEAD commits; `zoom_x86_64.tar.xz` 7.1.5.4332 streamed and listed; `steam_1.0.0.87.tar.gz` | all 200; Zoom SHA-256 equal to the manifest's | — |
| 37 | WebSearch | `Microsoft Teams Linux client retirement December 2022 progressive web app techcommunity` | techcommunity.microsoft.com blog post 3669846 (200 after redirect) | — |
| 38 | github.com | `linuxmint/timeshift` tags (newest numeric `26.09.0`); `openSUSE/snapper` tag `v0.13.2` | all 200 | first pick `v22.06.1` (lexical sort error) discarded; at that tag `files/default.json` 404. Snapper `data/snapper-*.timer` 404 (files are named `data/{timeline,cleanup,boot}.timer`, 200) |
| 39 | documentation.ubuntu.com | `server/how-to/graphics/install-nvidia-drivers/` | redirect → ubuntu.com/server/docs/how-to/graphics/install-nvidia-drivers/ (200) | — |
| 40 | WebSearch | `Chromium blog OR Mozilla blog telemetry "number of open tabs" percentile users desktop data` | blog.mozilla.org/metrics WordPress API: post 5078 (200); API searches `tab study`, `tabs`, `Test Pilot`, `windows` (200) → posts 4504, 4756, 2040 (200) | no Chromium or Google publication of tab or window counts found |

## 2. Candidates

### S2-01 — Ubuntu 24.04.5.1 desktop image: package manifests of the installable layers

- **Citation.** Canonical, *Ubuntu 24.04.5.1 LTS (Noble Numbat) desktop image* `ubuntu-24.04.5.1-desktop-amd64.iso`, files `casper/install-sources.yaml`, `casper/minimal.manifest`, `casper/minimal.standard.manifest`, `casper/minimal.standard.live.manifest`; and the release-directory files `ubuntu-24.04.5.1-desktop-amd64.manifest`, `.list`.
- **Copy read.** https://releases.ubuntu.com/24.04/ (accessed 2026-10-01); the four `casper/` files were read out of the ISO by HTTP range requests. Local `sources/S2-01/`. SHA-256: `iso-casper-install-sources.yaml` 3d3e0d097b51c21aeb8d3330de0220e33d29e694dd56c0de5797b8bbc6cb1ec9; `iso-casper-minimal.manifest` 31544e9fb82e6c7e4d8f6062f46bc2ec5d7e7061b4df1040036c061d33206a49; `iso-casper-minimal.standard.manifest` 99fce3823f2ce2f253ff92f5517f94f0779afa3ade60ff881fc8ef58adb5aa1d; `iso-casper-minimal.standard.live.manifest` d94776bd26ffd5223b271e4616fb272b0fba6a8734cfc2fa7d113f4e25694c07; `ubuntu-24.04.5.1-desktop-amd64.manifest` 6c200933618b2e382e7732b69b247aa5f63ed6600d8ee730d57b02ec74e4f8ff.
- **Passages.** `casper/install-sources.yaml`, whole file — the installer's default is the `minimal` layer:

`S2-01/iso-casper-install-sources.yaml:1–42`
```text
- default: true
  description:
    en: A minimal but usable Ubuntu Desktop.
  id: ubuntu-desktop-minimal
  locale_support: langpack
  name:
    en: Ubuntu Desktop (minimized)
  path: minimal.squashfs
  preinstalled_langs:
  - de
  - en
  - es
  - fr
  - it
  - pt
  - ru
  - zh
  - ''
  size: 4826120192
  type: fsimage-layered
  variant: desktop
- default: false
  description:
    en: A full featured Ubuntu Desktop.
  id: ubuntu-desktop
  locale_support: langpack
  name:
    en: Ubuntu Desktop
  path: minimal.standard.squashfs
  preinstalled_langs:
  - de
  - en
  - es
  - fr
  - it
  - pt
  - ru
  - zh
  - ''
  size: 6521954304
  type: fsimage-layered
  variant: desktop
```

The layer manifests are diffs (`+` = package added by the layer). `minimal.manifest` (the default install), selected lines:

`grep -n -E '^[+](anacron|apport|apt|cron|dpkg|e2fsprogs|evince|firefox|fwupd|gnome-shell|logrotate|man-db|pipewire-bin|python3|rsync|snapd|sysstat|systemd|tar|tracker-extract|tracker-miner-fs|ubuntu-desktop-minimal|ubuntu-pro-client|ubuntu-standard|unattended-upgrades|update-notifier|update-notifier-common|util-linux|whoopsie|wireplumber|xserver-xorg-core|xwayland|xz-utils|dbus-daemon|kerneloops|cloud-init|snap:firefox|snap:firmware-updater|snap:snap-store)\s' S2-01/iso-casper-minimal.manifest`
```text
11:+anacron	2.3-39ubuntu2
14:+apport	2.28.3-0ubuntu0.1
19:+apt	2.8.3
51:+cloud-init	26.1-0ubuntu1~24.04.1
64:+cron	3.0pl1-184ubuntu2
82:+dbus-daemon	1.14.10-4ubuntu4.1
107:+dpkg	1.22.6ubuntu6.6
109:+e2fsprogs	1.47.0-2.4~exp1ubuntu4.1
119:+evince	46.3.1-0ubuntu1.1
126:+firefox	1:1snap1-0ubuntu5
147:+fwupd	2.0.20-1ubuntu2~24.04.2
238:+gnome-shell	46.0-0ubuntu6~24.04.14
336:+kerneloops	0.12+git20140509-6ubuntu8
1139:+logrotate	3.21.0-2build1
1145:+man-db	2.12.0-4build2
1207:+pipewire-bin	1.0.5-1ubuntu3.3
1241:+python3	3.12.3-0ubuntu2.1
1319:+rsync	3.2.7-1ubuntu1.5
1335:+snapd	2.76.3+ubuntu24.04
1358:+sysstat	12.6.1-2
1361:+systemd	255.4-1ubuntu8.17
1369:+tar	1.35+dfsg-3ubuntu0.4
1380:+tracker-extract	3.7.1-1ubuntu0.1
1381:+tracker-miner-fs	3.7.1-1ubuntu0.1
1384:+ubuntu-desktop-minimal	1.539.2
1390:+ubuntu-pro-client	37.2ubuntu~24.04.1
1397:+ubuntu-standard	1.539.2
1404:+unattended-upgrades	2.9.1+nmu4ubuntu1
1409:+update-notifier	3.192.68.2
1410:+update-notifier-common	3.192.68.2
1417:+util-linux	2.39.3-9ubuntu6.6
1425:+whoopsie	0.2.77ubuntu0.1
1429:+wireplumber	0.4.17-1ubuntu4.1
1462:+xserver-xorg-core	2:21.1.12-1ubuntu1.6
1477:+xwayland	2:23.2.6-1ubuntu0.8
1479:+xz-utils	5.6.1+really5.4.5-1ubuntu0.3
1493:+snap:firefox	stable/ubuntu-24.04	8863
1494:+snap:firmware-updater	1/stable/ubuntu-24.04	226
1499:+snap:snap-store	2/stable/ubuntu-24.04	1390
```

`minimal.standard.manifest` (the "Ubuntu Desktop", extended selection), selected lines:

`grep -n -E '^[+](deja-dup|duplicity|libreoffice-writer|thunderbird|ubuntu-desktop|snap:thunderbird)\s' S2-01/iso-casper-minimal.standard.manifest`
```text
4:+deja-dup	45.2-1build2
5:+duplicity	2.1.4-3ubuntu2
137:+libreoffice-writer	4:24.2.7-0ubuntu0.24.04.6
188:+thunderbird	2:1snap1-0ubuntu3
210:+ubuntu-desktop	1.539.2
225:+snap:thunderbird	stable/ubuntu-24.04	1255
```

`minimal.standard.live.manifest` (live session only), selected lines:

`grep -n -E '^[+](casper|zfsutils-linux)\s' S2-01/iso-casper-minimal.standard.live.manifest`
```text
8:+casper	1.498
115:+zfsutils-linux	2.2.2-0ubuntu9.5
```

Reader's own check of absence: `grep -h -E '^[+-]?(gcc|gcc-13|make|dkms|plocate|mlocate|clamav[a-z-]*|timeshift|snapper|baloo[a-z0-9-]*|dbus-broker|localsearch|build-essential|nvidia[a-z0-9-]*|vlc|mpv|gimp|ffmpeg)\s' iso-casper-*.manifest ubuntu-24.04.5.1-desktop-amd64.manifest` returned no line; `cpp`, `linux-headers-7.0.0-31-generic` and `linux-headers-generic-hwe-24.04` are present (kernel 7.0.0-31 HWE).
- **Coverage.** T5 — covers which packages carrying timers, cron jobs and hooks are in a stock Ubuntu 24.04.5.1 desktop install: default (`minimal`) layer has anacron, apt, cron, dpkg, e2fsprogs, fwupd, logrotate, man-db, snapd, sysstat, systemd, tracker-miner-fs, unattended-upgrades, update-notifier, util-linux, apport, whoopsie; the extended layer adds deja-dup and duplicity; plocate, ClamAV, DKMS, gcc and make are in no layer. T8 — covers whether named programs are in a default install: Evince, Firefox (snap), GNOME Shell, Xorg, Xwayland, PipeWire, WirePlumber, dbus-daemon, systemd, python3, rsync, tar, xz, Tracker are default; LibreOffice Writer and Thunderbird (snap) only in the extended selection; dbus-broker, VS Code, Chrome, Chromium, GIMP, darktable, Kdenlive, Blender, mpv, VLC, Spotify, Zoom, Slack, Discord, Element, Steam, gamescope, Wine, Baloo, plocate, ClamAV, borg, rclone, 7-Zip, HandBrakeCLI, ffmpeg, make, gcc, DKMS are not in any layer. Supports existence only (what is installed, not what runs or how often). Does not cover T3, T4, T7, T10.
- **One observation?** Not an observation; one build of one image (Ubuntu 24.04.5.1 desktop amd64, image built 2026). Platform named; no machine, no window.

### S2-02 — ubuntu-meta 1.539.2 seed lists, and Ubuntu noble nautilus dependencies

- **Citation.** Canonical, source package `ubuntu-meta` 1.539.2 (Ubuntu 24.04 metapackages generated from the seeds); and packages.ubuntu.com page of `nautilus` 1:46.4-0ubuntu0.2 in noble-updates.
- **Copy read.** http://archive.ubuntu.com/ubuntu/pool/main/u/ubuntu-meta/ubuntu-meta_1.539.2.tar.xz (SHA-256 0f1b3a3f5a99273ac0787218a154d1b52f4c99aed87e84dcf0a6637620cd2cbe); https://packages.ubuntu.com/noble-updates/nautilus (SHA-256 of the HTML a0e7a7f21ab6c7739945d13f3aaeb676f6cdcc286af7d80b57f24ecb1ec35d3a). Accessed 2026-10-01. Local `sources/S2-02/`.
- **Passages.** Seed list files (one package per line):

`desktop-minimal-amd64` (Depends of ubuntu-desktop-minimal):
`grep -n -E '^(anacron|gnome-shell|nautilus|pipewire-pulse|ubuntu-drivers-common|update-notifier|wireplumber|xorg)$' S2-02/ubuntu-meta-1.539.2/desktop-minimal-amd64`
```text
3:anacron
17:gnome-shell
32:nautilus
34:pipewire-pulse
39:ubuntu-drivers-common
45:update-notifier
47:wireplumber
52:xorg
```

`desktop-minimal-recommends-amd64` (Recommends of ubuntu-desktop-minimal):
`grep -n -E '^(evince|firefox|fwupd|kerneloops|snapd|systemd-oomd|ubuntu-report|whoopsie)$' S2-02/ubuntu-meta-1.539.2/desktop-minimal-recommends-amd64`
```text
16:evince
17:firefox
23:fwupd
51:kerneloops
84:snapd
86:systemd-oomd
88:ubuntu-report
90:whoopsie
```

`desktop-recommends-amd64` (Recommends of ubuntu-desktop):
`grep -n -E '^(deja-dup|libreoffice-writer|thunderbird|rhythmbox|shotwell|totem|transmission-gtk)$' S2-02/ubuntu-meta-1.539.2/desktop-recommends-amd64`
```text
14:deja-dup
69:libreoffice-writer
94:rhythmbox
96:shotwell
101:thunderbird
102:totem
103:transmission-gtk
```

`standard-amd64` and `standard-recommends-amd64`:
`grep -n -E '^(cron|logrotate|man-db|rsync|xz-utils)$' S2-02/ubuntu-meta-1.539.2/standard-amd64`
```text
4:cron
13:logrotate
16:man-db
22:rsync
27:xz-utils
```
`grep -n -E '^(sysstat)$' S2-02/ubuntu-meta-1.539.2/standard-recommends-amd64`
```text
16:sysstat
```

nautilus page (text conversion `nautilus-noble-updates.txt`), the dependency that pulls the Tracker file indexer into the default desktop:
`S2-02/nautilus-noble-updates.txt:215–218`
```text
dep:
tracker-miner-fs
	 (>= 3)
metadata database, indexer and search tool - filesystem indexer
```
- **Coverage.** T5 — covers why the file indexer (tracker-miner-fs) is in the default install: GNOME Files (nautilus) depends on it. T8 — covers which programs the default and extended desktops pull in. Supports existence only. Does not cover T3, T4, T7, T10.
- **One observation?** Not an observation; one source package version.

### S2-03 — Ubuntu 24.04 (noble) packages: systemd timer units, cron files, hooks and defaults

- **Citation.** Ubuntu noble binary packages, at the versions recorded in S2-01 unless noted: apt 2.8.3; dpkg 1.22.6ubuntu6.6; e2fsprogs 1.47.0-2.4~exp1ubuntu4.1; util-linux 2.39.3-9ubuntu6.6; fwupd 2.0.20-1ubuntu2~24.04.2; logrotate 3.21.0-2build1; man-db 2.12.0-4build2; anacron 2.3-39ubuntu2; systemd 255.4-1ubuntu8.17; update-notifier-common 3.192.68.2; base-files 13ubuntu10.5; sysstat 12.6.1-2; snapd 2.76.3+ubuntu24.04; tracker-miner-fs and tracker-extract 3.7.1-1ubuntu0.1; unattended-upgrades 2.9.1+nmu4ubuntu1; cron 3.0pl1-184ubuntu2; apport 2.28.3-0ubuntu0.1; deja-dup 45.2-1build2; ubuntu-settings 24.04.6; and, not in any layer of the image, plocate 1.1.19-2ubuntu2 (universe), clamav / clamav-daemon / clamav-freshclam 1.5.4+dfsg-0ubuntu0.24.04.1 (noble-updates), dkms 3.0.11-1ubuntu13.
- **Copy read.** `http://archive.ubuntu.com/ubuntu/pool/<component>/<x>/<source>/<binary>_<version>_<arch>.deb`, accessed 2026-10-01, unpacked with `ar x` and `bsdtar`. Local `sources/S2-03/` (`x-<package>/` = unpacked data, `x-<package>/ctl/` = maintainer scripts). SHA-256 of each `.deb`:
  anacron 2b4142e8a0a451f4d3922dfcc8f5d04f9bc4d301bc5ef86c0321a151fd06d2c2; apport 3fb6842df77c2a60373981d2a00e25c11b3793f4301e115bcb9dd3e3b69e8847; apt c9ace99efc7726fe0035f921a9acf262a9723bbf35b861aab4f9075a0be67442; base-files 87e8c41e62f61625fb78a982d0bc0a70f40ef8375bc313b154914d1b3759c823; clamav 67e61b57e15fda1f0778cc75ac1370adbc864943193bf8ae9dea1d654be030e9; clamav-daemon e9943d5e9dc7a5b37162ad19331a960aa6713b9f74bf64074cb1ac4f210abf4d; clamav-freshclam 684b8c6fb5c50a7efb744a2e1f2998cff1e847980cc1eccd6a39cba28a8981c2; cron 5a257b6b3b05d290964f68868db8127cca7eeef64c30dc9586f46cd4f68f1b90; deja-dup 092007f597967e564b326550845ed814a06aa254cd31cc9e198a91da2e14b4e8; dkms 18d098c65e3002040afc11f80656e84377551a5d1bdcd3933cdf6ae2e58dcd75; dpkg ceb6aa4da59fbcb8a3b0549b4280c60b7d849b519859797c8668bdfbe378fb3b; e2fsprogs 1d0fb19dcf14316d04602260871dba3c1441c0ecf3c3bde54eacba35dcc5a40b; fwupd 0e04b5c0081114c080e4a3618e12e73a311f33bf061c8e53c151459a6149fcea; logrotate e609ad80a9cec135b404a84f99d9d87bc304800eb212702444a985527edba70c; man-db d7ce31173a73bd3a93b7216a837a2e8641fff3fd7ae2dfc0ca705dbabe03e92b; plocate 90375d69eda16ca5f73e6449447ef05c1a18b7b1de4092879eda9850898c04b0; snapd 9ffe7430c7769234e58c9b83a5fe6e33c7ca963976133e4a0ede4c29dcd0fa82; sysstat 40f8a528434e2816f78869b7aa71a9ff4057678e76ae3a4109b5a7a72caa1285; systemd 250345b73e42a97ee71cae7c1e470897dfad3c639eb0a7aafe4f9a3a29871cb2; tracker-extract 808d8a0eb1cd5704db56d8e7b0e9a08a51f256004d3b42356904ad1650460ccc; tracker-miner-fs 573bdac5dbd64761fe88f48bf54204f6ceb9f9c2e785e96a2e02ea0866f5ae41; ubuntu-settings 6c44f240032df2e818bdc57f54a8b2ad7cb40ae61f91c50cab14942c390396e1; unattended-upgrades 13c576c7d8184f509d5ddc4d75bec6e62ef3f745319cce60f8131f401091113b; update-notifier-common 50c3303b52aaaaadcf11750e1a0afc905bdee0d6f75aa2f1febdd4416afe7fec; util-linux 08eb17ba3b83378ed1e73d8335d0ce03b429c0bbeb07e374f536234edab02465.
- **Passages — APT.** `apt-daily.timer` and its service (`x-apt/usr/lib/systemd/system/`):

`S2-03/x-apt/usr/lib/systemd/system/apt-daily.timer:1–10`
```text
[Unit]
Description=Daily apt download activities

[Timer]
OnCalendar=*-*-* 6,18:00
RandomizedDelaySec=12h
Persistent=true

[Install]
WantedBy=timers.target
```
`S2-03/x-apt/usr/lib/systemd/system/apt-daily.service:1–10`
```text
[Unit]
Description=Daily apt download activities
Documentation=man:apt(8)
ConditionACPower=true
After=network.target network-online.target systemd-networkd.service NetworkManager.service connman.service

[Service]
Type=oneshot
ExecStartPre=-/usr/lib/apt/apt-helper wait-online
ExecStart=/usr/lib/apt/apt.systemd.daily update
```

`apt-daily-upgrade.timer` and service lines 1–12:

`S2-03/x-apt/usr/lib/systemd/system/apt-daily-upgrade.timer:1–11`
```text
[Unit]
Description=Daily apt upgrade and clean activities
After=apt-daily.timer

[Timer]
OnCalendar=*-*-* 6:00
RandomizedDelaySec=60m
Persistent=true

[Install]
WantedBy=timers.target
```
`S2-03/x-apt/usr/lib/systemd/system/apt-daily-upgrade.service:1–12`
```text
[Unit]
Description=Daily apt upgrade and clean activities
Documentation=man:apt(8)
ConditionACPower=true
After=apt-daily.service network.target network-online.target systemd-networkd.service NetworkManager.service connman.service

[Service]
Type=oneshot
ExecStartPre=-/usr/lib/apt/apt-helper wait-online
ExecStart=/usr/lib/apt/apt.systemd.daily install
KillMode=process
TimeoutStopSec=900
```

What the APT periodic jobs do on the desktop — `update-notifier-common` `/etc/apt/apt.conf.d/10periodic` (whole file) and `unattended-upgrades` `/usr/share/unattended-upgrades/20auto-upgrades` (whole file), installed as `/etc/apt/apt.conf.d/20auto-upgrades` when the debconf answer is true; the debconf template default (`x-unattended-upgrades/ctl/templates` lines 2–5):

`S2-03/x-update-notifier-common/etc/apt/apt.conf.d/10periodic:1–3`
```text
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Download-Upgradeable-Packages "0";
APT::Periodic::AutocleanInterval "0";
```
`S2-03/x-unattended-upgrades/usr/share/unattended-upgrades/20auto-upgrades:1–2`
```text
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
```
`S2-03/x-unattended-upgrades/ctl/templates:2–5`
```text
Template: unattended-upgrades/enable_auto_updates
Type: boolean
Default: true
Description: Automatically download and install stable updates?
```

- **Passages — dpkg database backup.** `dpkg-db-backup.timer`, its service, and the script `/usr/libexec/dpkg/dpkg-db-backup` lines 18–25 and 50–74:

`S2-03/x-dpkg/usr/lib/systemd/system/dpkg-db-backup.timer:1–10`
```text
[Unit]
Description=Daily dpkg database backup timer
Documentation=man:dpkg(1)

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```
`S2-03/x-dpkg/usr/lib/systemd/system/dpkg-db-backup.service:1–7`
```text
[Unit]
Description=Daily dpkg database backup service
Documentation=man:dpkg(1)

[Service]
Type=oneshot
ExecStart=/usr/libexec/dpkg/dpkg-db-backup
```
`S2-03/x-dpkg/usr/libexec/dpkg/dpkg-db-backup:18–25`
```text
PROGNAME=$(basename "$0")
ADMINDIR='/var/lib/dpkg'
BACKUPSDIR='/var/backups'
ROTATE=7

PKGDATADIR_DEFAULT='/usr/share/dpkg'
PKGDATADIR="${DPKG_DATADIR:-$PKGDATADIR_DEFAULT}"
TAR='tar'
```
`S2-03/x-dpkg/usr/libexec/dpkg/dpkg-db-backup:50–74`
```text
# Backup the N last versions of dpkg databases containing user data.
if cd $BACKUPSDIR ; then
  # We backup all relevant database files if any has changed, so that
  # the rotation number always contains an internally consistent set.
  dbchanged=no
  dbfiles="arch status diversions statoverride"
  for db in $dbfiles ; do
    if ! [ -s "dpkg.${db}.0" ] && ! [ -s "$dbdir/$db" ]; then
      # Special case the files not existing or being empty as being equal.
      continue
    elif ! cmp -s "dpkg.${db}.0" "$dbdir/$db"; then
      dbchanged=yes
      break
    fi
  done
  if [ "$dbchanged" = "yes" ] ; then
    for db in $dbfiles ; do
      if [ -e "$dbdir/$db" ]; then
        cp -p "$dbdir/$db" "dpkg.$db"
      else
        touch "dpkg.$db"
      fi
      savelog -c "$ROTATE" "dpkg.$db" >/dev/null
    done
  fi
```

- **Passages — man-db, logrotate, fstrim, e2scrub, fwupd, anacron, motd, update-notifier, tmpfiles, apport, snap-repair, sysstat, systemd-sysupdate.**

`S2-03/x-man-db/usr/lib/systemd/system/man-db.timer:1–11`
```text
[Unit]
Description=Daily man-db regeneration
Documentation=man:mandb(8)

[Timer]
OnCalendar=daily
RandomizedDelaySec=12h
Persistent=true

[Install]
WantedBy=timers.target
```
`S2-03/x-man-db/usr/lib/systemd/system/man-db.service:1–15`
```text
[Unit]
Description=Daily man-db regeneration
Documentation=man:mandb(8)
ConditionACPower=true

[Service]
Type=oneshot
# Recover from deletion, per FHS.
ExecStart=+/usr/bin/install -d -o man -g man -m 0755 /var/cache/man
# Regenerate man database.
ExecStart=/usr/bin/mandb --quiet
User=man
Nice=19
IOSchedulingClass=idle
IOSchedulingPriority=7
```
`S2-03/x-logrotate/usr/lib/systemd/system/logrotate.timer:1–11`
```text
[Unit]
Description=Daily rotation of log files
Documentation=man:logrotate(8) man:logrotate.conf(5)

[Timer]
OnCalendar=daily
AccuracySec=1h
Persistent=true

[Install]
WantedBy=timers.target
```
`S2-03/x-logrotate/usr/lib/systemd/system/logrotate.service:1–14`
```text
[Unit]
Description=Rotate log files
Documentation=man:logrotate(8) man:logrotate.conf(5)
RequiresMountsFor=/var/log
ConditionACPower=true

[Service]
Type=oneshot
ExecStart=/usr/sbin/logrotate /etc/logrotate.conf

# performance options
Nice=19
IOSchedulingClass=best-effort
IOSchedulingPriority=7
```
`S2-03/x-util-linux/usr/lib/systemd/system/fstrim.timer:1–14`
```text
[Unit]
Description=Discard unused filesystem blocks once a week
Documentation=man:fstrim
ConditionVirtualization=!container
ConditionPathExists=!/etc/initrd-release

[Timer]
OnCalendar=weekly
AccuracySec=1h
Persistent=true
RandomizedDelaySec=100min

[Install]
WantedBy=timers.target
```
`S2-03/x-util-linux/usr/lib/systemd/system/fstrim.service:1–8`
```text
[Unit]
Description=Discard unused blocks on filesystems from /etc/fstab
Documentation=man:fstrim(8)
ConditionVirtualization=!container

[Service]
Type=oneshot
ExecStart=/sbin/fstrim --listed-in /etc/fstab:/proc/self/mountinfo --verbose --quiet-unsupported
```
`S2-03/x-e2fsprogs/usr/lib/systemd/system/e2scrub_all.timer:1–11`
```text
[Unit]
Description=Periodic ext4 Online Metadata Check for All Filesystems

[Timer]
# Run on Sunday at 3:10am, to avoid running afoul of DST changes
OnCalendar=Sun *-*-* 03:10:00
RandomizedDelaySec=60
Persistent=true

[Install]
WantedBy=timers.target
```
`S2-03/x-e2fsprogs/usr/lib/systemd/system/e2scrub_all.service:1–11`
```text
[Unit]
Description=Online ext4 Metadata Check for All Filesystems
ConditionACPower=true
ConditionCapability=CAP_SYS_ADMIN
ConditionCapability=CAP_SYS_RAWIO
Documentation=man:e2scrub_all(8)

[Service]
Type=oneshot
Environment=SERVICE_MODE=1
ExecStart=/sbin/e2scrub_all
```
`S2-03/x-fwupd/usr/lib/systemd/system/fwupd-refresh.timer:1–11`
```text
[Unit]
Description=Refresh fwupd metadata regularly
ConditionVirtualization=!container

[Timer]
OnCalendar=*-*-* *:00:00
RandomizedDelaySec=1h
Persistent=true

[Install]
WantedBy=timers.target
```
`S2-03/x-fwupd/usr/lib/systemd/system/fwupd-refresh.service:24–25`
```text
SuccessExitStatus=2 101
ExecStart=/usr/bin/fwupdmgr refresh
```
`S2-03/x-anacron/usr/lib/systemd/system/anacron.timer:1–10`
```text
[Unit]
Description=Trigger anacron every hour

[Timer]
OnCalendar=*-*-* 07..23:30
RandomizedDelaySec=5m
Persistent=true

[Install]
WantedBy=timers.target
```
`S2-03/x-anacron/usr/lib/systemd/system/anacron.service:12–17`
```text
ConditionACPower=true
Documentation=man:anacron man:anacrontab

[Service]
EnvironmentFile=/etc/default/anacron
ExecStart=/usr/sbin/anacron -d -q $ANACRON_ARGS
```
`S2-03/x-base-files/usr/lib/systemd/system/motd-news.timer:1–11`
```text
[Unit]
Description=Message of the Day

[Timer]
OnCalendar=00,12:00:00
RandomizedDelaySec=12h
Persistent=true
OnStartupSec=1min

[Install]
WantedBy=timers.target
```

`base-files` `/etc/update-motd.d/50-motd-news` lines 33–37 (the job exits unless `/etc/default/motd-news` sets `ENABLED=1`; that file belongs to `motd-news-config`, which is in no layer of S2-01):

`S2-03/x-base-files/etc/update-motd.d/50-motd-news:33–37`
```text
[ -r /etc/default/motd-news ] && . /etc/default/motd-news

# Exit immediately, unless we're enabled
# This makes this script very easy to disable in /etc/default/motd-news configuration
[ "$ENABLED" = "1" ] || exit 0
```
`S2-03/x-update-notifier-common/lib/systemd/system/update-notifier-download.timer:1–10`
```text
[Unit]
Description=Download data for packages that failed at package install time
After=network.target network-online.target systemd-networkd.service NetworkManager.service connman.service

[Timer]
OnStartupSec=5m
OnUnitActiveSec=24h

[Install]
WantedBy=timers.target
```
`S2-03/x-update-notifier-common/lib/systemd/system/update-notifier-motd.timer:1–11`
```text
[Unit]
Description=Check to see whether there is a new version of Ubuntu available
After=network.target network-online.target systemd-networkd.service NetworkManager.service connman.service

[Timer]
OnCalendar=Sun *-*-* 06:00:00
RandomizedDelaySec=1w
Persistent=true

[Install]
WantedBy=timers.target
```
`S2-03/x-systemd/usr/lib/systemd/system/systemd-tmpfiles-clean.timer:10–17`
```text
[Unit]
Description=Daily Cleanup of Temporary Directories
Documentation=man:tmpfiles.d(5) man:systemd-tmpfiles(8)
ConditionPathExists=!/etc/initrd-release

[Timer]
OnBootSec=15min
OnUnitActiveSec=1d
```
`S2-03/x-systemd/usr/lib/systemd/user/systemd-tmpfiles-clean.timer:10–19`
```text
[Unit]
Description=Daily Cleanup of User's Temporary Directories
Documentation=man:tmpfiles.d(5) man:systemd-tmpfiles(8)

[Timer]
OnStartupSec=5min
OnUnitActiveSec=1d

[Install]
WantedBy=timers.target
```
`S2-03/x-systemd/usr/lib/systemd/system/systemd-sysupdate.timer:18–30`
```text
[Timer]
# Trigger the update 15min after boot, and then – on average – every 6h, but
# randomly distributed in a 2h…6h interval. In addition trigger things
# persistently once on each Saturday, to ensure that even on systems that are
# never booted up for long we have a chance to to do the update.
OnBootSec=15min
OnUnitActiveSec=2h
OnCalendar=Sat
RandomizedDelaySec=4h
Persistent=yes

[Install]
WantedBy=timers.target
```
`S2-03/x-apport/usr/lib/systemd/system/apport-autoreport.timer:1–10`
```text
[Unit]
Description=Process error reports when automatic reporting is enabled (timer based)
ConditionPathExists=/var/lib/apport/autoreport

[Timer]
OnStartupSec=1h
OnUnitActiveSec=3h

[Install]
WantedBy=timers.target
```
`S2-03/x-snapd/usr/lib/systemd/system/snapd.snap-repair.timer:1–15`
```text
[Unit]
Description=Timer to automatically fetch and run repair assertions
# don't run on classic
ConditionKernelCommandLine=|snap_core
ConditionKernelCommandLine=|snapd_recovery_mode

[Timer]
OnCalendar=*-*-* 5,11,17,23:00
RandomizedDelaySec=2h
AccuracySec=10min
Persistent=true
OnStartupSec=15m

[Install]
WantedBy=timers.target
```
`S2-03/x-sysstat/usr/lib/systemd/system/sysstat-collect.timer:7–14`
```text
[Unit]
Description=Run system activity accounting tool every 10 minutes

[Timer]
OnCalendar=*:00/10

[Install]
WantedBy=sysstat.service
```
`S2-03/x-sysstat/usr/lib/systemd/system/sysstat-summary.timer:8–15`
```text
[Unit]
Description=Generate summary of yesterday's process accounting

[Timer]
OnCalendar=00:07:00

[Install]
WantedBy=sysstat.service
```

sysstat's collection is off by default: debconf template (`x-sysstat/ctl/templates` 135–141) and `x-sysstat/ctl/postinst` 182–190 (the postinst disables the timers unless the answer is true):

`S2-03/x-sysstat/ctl/templates:135–141`
```text
Template: sysstat/enable
Type: boolean
Default: false
Description: Activate sysstat's cron job?
 If this option is enabled the sysstat package will monitor system
 activities and store the data in log files within /var/log/sysstat/.
 .
```
`S2-03/x-sysstat/ctl/postinst:182–190`
```text
if [ "$1" = "configure" ] && [ -n "$ENABLED" ]; then
    manage_systemd_services "$ENABLED"

    # execute sa1 in a subshell not to clobber the postinst script with potentially
    # unsafe values from "$DEFAULT"
    if [ "$ENABLED" = "true" ] && [ -x /usr/lib/sysstat/sa1 ] ; then
        ( set +e ; /usr/lib/sysstat/sa1 1 1 )&
    fi
fi
```

How a timer is enabled at installation (debhelper fragment, `x-apt/ctl/postinst` 40–50; the same pattern appears in the postinst of dpkg, e2fsprogs, fwupd, logrotate, man-db, anacron, base-files, update-notifier-common and util-linux):

`S2-03/x-apt/ctl/postinst:40–50`
```text
	deb-systemd-helper unmask 'apt-daily.timer' >/dev/null || true

	# was-enabled defaults to true, so new installations run enable.
	if deb-systemd-helper --quiet was-enabled 'apt-daily.timer'; then
		# Enables the unit on first installation, creates new
		# symlinks on upgrades if the unit file has changed.
		deb-systemd-helper enable 'apt-daily.timer' >/dev/null || true
	else
		# Update the statefile to add new symlinks (if any), which need to be
		# cleaned up on purge. Also remove old symlinks.
		deb-systemd-helper update-state 'apt-daily.timer' >/dev/null || true
```

cron fallbacks skip when systemd runs — `/etc/cron.daily/dpkg`, `/etc/cron.daily/man-db` lines 7–10, `/etc/cron.daily/apt-compat` lines 5–12:

`S2-03/x-dpkg/etc/cron.daily/dpkg:1–8`
```text
#!/bin/sh

# Skip if systemd is running.
if [ -d /run/systemd/system ]; then
  exit 0
fi

/usr/libexec/dpkg/dpkg-db-backup
```
`S2-03/x-man-db/etc/cron.daily/man-db:7–10`
```text
if [ -d /run/systemd/system ]; then
    # Skip in favour of systemd timer.
    exit 0
fi
```
`S2-03/x-apt/etc/cron.daily/apt-compat:5–12`
```text
# Systemd systems use a systemd timer unit which is preferable to
# run. We want to randomize the apt update and unattended-upgrade
# runs as much as possible to avoid hitting the mirrors all at the
# same time. The systemd time is better at this than the fixed
# cron.daily time
if [ -d /run/systemd/system ]; then
    exit 0
fi
```

- **Passages — file indexer (Tracker 3.7 in the default install).** User unit and XDG autostart entry (`tracker-miner-fs` package), and the settings schema shipped in `tracker-extract` (`usr/share/glib-2.0/schemas/org.freedesktop.Tracker3.Miner.Files.gschema.xml`) lines 22–26, 43–51, 65–68, 86–95, 98–109:

`S2-03/x-tracker-miner-fs/usr/lib/systemd/user/tracker-miner-fs-3.service:1–17`
```text
[Unit]
Description=Tracker file system data miner
ConditionUser=!root
ConditionUser=!gnome-initial-setup
After=gnome-session.target

[Service]
Type=dbus
BusName=org.freedesktop.Tracker3.Miner.Files
ExecStart=/usr/libexec/tracker-miner-fs-3
Restart=on-failure
# Don't restart after tracker daemon -k (aka tracker-control -k)
RestartPreventExitStatus=SIGKILL
Slice=background.slice

[Install]
WantedBy=gnome-session.target
```
`S2-03/x-tracker-miner-fs/etc/xdg/autostart/tracker-miner-fs-3.desktop:1–15`
```text
[Desktop Entry]
Name=Tracker File System Miner
Comment=Crawls and processes files on the file system
Exec=/usr/libexec/tracker-miner-fs-3
Terminal=false
Type=Application
Categories=Utility;
X-GNOME-Autostart-enabled=true
X-GNOME-HiddenUnderSystemd=true
X-KDE-autostart-after=panel
X-KDE-StartupNotify=false
X-KDE-UniqueApplet=true
NoDisplay=true
OnlyShowIn=GNOME;KDE;XFCE;X-IVI;Unity;
X-systemd-skip=true
```
`S2-03/x-tracker-extract/usr/share/glib-2.0/schemas/org.freedesktop.Tracker3.Miner.Files.gschema.xml:22–26`
```text
    <key name="initial-sleep" type="i">
      <summary>Initial sleep</summary>
      <description>Initial sleep time, in seconds.</description>
      <range min="0" max="1000"/>
      <default>15</default>
```
`S2-03/x-tracker-extract/usr/share/glib-2.0/schemas/org.freedesktop.Tracker3.Miner.Files.gschema.xml:43–51`
```text
    <key name="crawling-interval" type="i">
      <summary>Crawling interval</summary>
      <description>
        Interval in days to check whether the filesystem is up to date in the database.
	0 forces crawling anytime, -1 forces it only after unclean shutdowns, and -2
	disables it entirely.
      </description>
      <range min="-2" max="365"/>
      <default>-1</default>
```
`S2-03/x-tracker-extract/usr/share/glib-2.0/schemas/org.freedesktop.Tracker3.Miner.Files.gschema.xml:65–68`
```text
    <key name="enable-monitors" type="b">
      <summary>Enable monitors</summary>
      <description>Set to false to completely disable any file monitoring</description>
      <default>true</default>
```
`S2-03/x-tracker-extract/usr/share/glib-2.0/schemas/org.freedesktop.Tracker3.Miner.Files.gschema.xml:86–95`
```text
    <key name="index-on-battery" type="b">
      <summary>Index when running on battery</summary>
      <description>Set to true to index while running on battery</description>
      <default>true</default>
    </key>

    <key name="index-on-battery-first-time" type="b">
      <summary>Perform initial indexing when running on battery</summary>
      <description>Set to true to index while running on battery for the first time only</description>
      <default>true</default>
```
`S2-03/x-tracker-extract/usr/share/glib-2.0/schemas/org.freedesktop.Tracker3.Miner.Files.gschema.xml:98–109`
```text
    <key name="index-recursive-directories" type="as">
      <summary>Directories to index recursively</summary>
      <!-- Translators: Do NOT translate the directories names in capital. Those
      are keys used by Tracker. -->
      <description>
	List of directories to index recursively, Special values include:
	‘&amp;DESKTOP’, ‘&amp;DOCUMENTS’, ‘&amp;DOWNLOAD’, ‘&amp;MUSIC’, ‘&amp;PICTURES’,
	‘&amp;PUBLIC_SHARE’, ‘&amp;TEMPLATES’, ‘&amp;VIDEOS’.

	See /etc/xdg/user-dirs.defaults and $HOME/.config/user-dirs.default
      </description>
      <default>[ '&amp;DESKTOP', '&amp;DOCUMENTS', '&amp;MUSIC', '&amp;PICTURES', '&amp;VIDEOS' ]</default>
```

- **Passages — plocate (not in the default install; universe).** Timer, service, and the cron fallback:

`S2-03/x-plocate/usr/lib/systemd/system/plocate-updatedb.timer:1–11`
```text
[Unit]
Description=Update the plocate database daily

[Timer]
OnCalendar=daily
RandomizedDelaySec=12h
AccuracySec=20min
Persistent=true

[Install]
WantedBy=timers.target
```
`S2-03/x-plocate/usr/lib/systemd/system/plocate-updatedb.service:1–13`
```text
[Unit]
Description=Update the plocate database
ConditionACPower=true

[Service]
Type=oneshot
ExecStart=/usr/sbin/updatedb.plocate
LimitNOFILE=131072
IOSchedulingClass=idle

PrivateTmp=true
PrivateDevices=true
PrivateNetwork=true
```
`S2-03/x-plocate/etc/cron.daily/plocate:1–35`
```text
#! /bin/sh

set -e

UPDATEDB=/usr/sbin/updatedb.plocate

# Skip if systemd timer is available.
if [ -d /run/systemd/system ]; then
    exit 0
fi

[ -x $UPDATEDB ] || exit 0

if which on_ac_power >/dev/null 2>&1; then
    ON_BATTERY=0
    on_ac_power >/dev/null 2>&1 || ON_BATTERY=$?
    if [ "$ON_BATTERY" -eq 1 ]; then
        exit 0
    fi
fi

# See ionice(1).
IONICE=
if [ -x /usr/bin/ionice ] &&
    /usr/bin/ionice -c3 true 2>/dev/null; then
    IONICE="/usr/bin/ionice -c3"
fi

# See nocache(1).
NOCACHE=
if [ -x /usr/bin/nocache ]; then
    NOCACHE="/usr/bin/nocache"
fi

flock --nonblock /run/plocate.daily.lock $NOCACHE $IONICE nice $UPDATEDB
```
`grep -n -E '^(Section|Priority):' S2-03/x-plocate/ctl/control`
```text
8:Section: utils
9:Priority: optional
```

- **Passages — ClamAV (not in the default install).** Signature updater as a daemon (default method), its alternative one-shot timer, the debconf defaults, and the scanner daemon (no scheduled scan is shipped):

`S2-03/x-clamav-freshclam/usr/lib/systemd/system/clamav-freshclam.service:1–13`
```text
[Unit]
Description=ClamAV virus database updater
Documentation=man:freshclam(1) man:freshclam.conf(5) https://docs.clamav.net/
# If user wants it run from cron, don't start the daemon.
ConditionPathExists=!/etc/cron.d/clamav-freshclam
Wants=network-online.target
After=network-online.target

[Service]
ExecStart=/usr/bin/freshclam -d --foreground=true

[Install]
WantedBy=multi-user.target
```
`S2-03/x-clamav-freshclam/usr/lib/systemd/system/clamav-freshclam-once.timer:1–11`
```text
[Unit]
Description=Daily ClamAV virus database update

[Timer]
OnCalendar=daily
AccuracySec=1h
RandomizedDelaySec=1h
Persistent=true

[Install]
WantedBy=timers.target
```
`S2-03/x-clamav-freshclam/ctl/templates:2–4`
```text
Template: clamav-freshclam/autoupdate_freshclam
Type: select
Choices: daemon, ifup.d, cron, manual
```
`S2-03/x-clamav-freshclam/ctl/templates:22–23`
```text
Default: daemon
Description: Virus database update method:
```
`S2-03/x-clamav-freshclam/ctl/templates:504–507`
```text
Template: clamav-freshclam/update_interval
Type: string
Default: 24
Description: Number of freshclam updates per day:
```
`S2-03/x-clamav-freshclam/ctl/postinst:474–476`
```text
    if [ -n "$checks" ] && [ "$checks" != "true" ]; then
      echo "# Check for new database $checks times a day" >> $DEBCONFFILE
      echo "Checks $checks" >> $DEBCONFFILE
```
`S2-03/x-clamav-daemon/usr/lib/systemd/system/clamav-daemon.service:1–17`
```text
[Unit]
Description=Clam AntiVirus userspace daemon
Documentation=man:clamd(8) man:clamd.conf(5) https://docs.clamav.net/
Requires=clamav-daemon.socket
# Check for database existence
ConditionPathExistsGlob=/var/lib/clamav/main.{c[vl]d,inc}
ConditionPathExistsGlob=/var/lib/clamav/daily.{c[vl]d,inc}

[Service]
ExecStart=/usr/sbin/clamd --foreground=true
# Reload the database
ExecReload=/bin/kill -USR2 $MAINPID
TimeoutStartSec=420

[Install]
WantedBy=multi-user.target
Also=clamav-daemon.socket
```

- **Passages — DKMS (not in the default install).** Kernel hook `/etc/kernel/postinst.d/dkms` (the file `/etc/kernel/header_postinst.d/dkms` is identical) lines 37–39; `/usr/sbin/dkms` lines 180–188 (CPU count), 1113–1115 (make command), 2594–2597 (default `-j`), 2295–2300 (autoinstall installs modules one at a time in a loop):

`S2-03/x-dkms/etc/kernel/postinst.d/dkms:37–39`
```text
if [ -x /usr/lib/dkms/dkms_autoinstaller ]; then
    exec /usr/lib/dkms/dkms_autoinstaller start "$inst_kern"
fi
```
`S2-03/x-dkms/usr/sbin/dkms:178–188`
```text
# Find out how many CPUs there are so that we may pass an appropriate -j
# option to make. Ignore hyperthreading for now.
get_num_cpus()
{
    # use nproc(1) from coreutils 8.1-1+ if available, otherwise single job
    if [ -x /usr/bin/nproc ]; then
        nproc
    else
        echo "1"
    fi
}
```
`S2-03/x-dkms/usr/sbin/dkms:1113–1115`
```text
    local the_make_command="${make_command/#make/make -j$parallel_jobs KERNELRELEASE=$kernelver}"

    invoke_command "{ $the_make_command; } >> $build_log 2>&1" "$the_make_command" background || \
```
`S2-03/x-dkms/usr/sbin/dkms:2593–2597`
```text
# Default to -j<number of CPUs>
parallel_jobs=${parallel_jobs:-$(get_num_cpus)}

# Make sure we're not passing -j0 to make; treat -j0 as just "-j"
[[ "$parallel_jobs" = 0 ]] && parallel_jobs=""
```
`S2-03/x-dkms/usr/sbin/dkms:2295–2300`
```text
        # Step 2: Install modules that have an empty dependency list.
        for mv in "${to_install[@]}"; do
            IFS=/ read m v <<< "$mv"
            if [[ -z "${build_depends[$m]}" ]]; then
                (module="$m" module_version="$v" kernelver="$kernelver" arch="$arch" install_module)
                status=$?
```

- **Passages — Déjà Dup (extended install only).** Schema `org.gnome.DejaDup.gschema.xml` lines 48–56 and the autostart monitor:

`S2-03/x-deja-dup/usr/share/glib-2.0/schemas/org.gnome.DejaDup.gschema.xml:48–56`
```text
    <key name="periodic" type="b">
      <default>false</default>
      <summary>Whether to periodically back up</summary>
      <description>Whether to automatically back up on a regular schedule.</description>
    </key>
    <key name="periodic-period" type="i">
      <default>7</default>
      <summary>How often to periodically back up</summary>
      <description>The number of days between backups.</description>
```
`S2-03/x-deja-dup/etc/xdg/autostart/org.gnome.DejaDup.Monitor.desktop:4–15`
```text
[Desktop Entry]
Name=Backup Monitor
Comment=Schedules backups at regular intervals
X-Ubuntu-Gettext-Domain=deja-dup

Icon=org.gnome.DejaDup

Exec=/usr/libexec/deja-dup/deja-dup-monitor

X-GNOME-Autostart-Delay=120

StartupNotify=false
```

- **Passages — Ubuntu's mutter override (for T8).** `ubuntu-settings` `10_ubuntu-settings.gschema.override` lines 113–120 (no `experimental-features` key is set anywhere in the file: `grep -n experimental` returns nothing):

`S2-03/x-ubuntu-settings/usr/share/glib-2.0/schemas/10_ubuntu-settings.gschema.override:113–120`
```text
# Mirror G-S default experience (in overrides) compared to mutter default
# as we are using a G-S mode, the default overrides aren't used.
[org.gnome.mutter:ubuntu]
attach-modal-dialogs = true
edge-tiling = true
dynamic-workspaces = true
workspaces-only-on-primary = true
focus-change-on-pointer-rest = true
```

- **Coverage.** T5 — covers, for a stock Ubuntu 24.04 desktop, the name, schedule (`OnCalendar`, `RandomizedDelaySec`, `AccuracySec`, `Persistent`, boot and activity offsets), trigger conditions (`ConditionACPower`, path conditions) and command of each timer shipped by the packages of the default layer: apt-daily (06:00 and 18:00 plus up to 12 h random delay; `apt.systemd.daily update`), apt-daily-upgrade (06:00 plus up to 60 min; unattended upgrade enabled by default), dpkg-db-backup (daily; backs up `/var/lib/dpkg` files and alternatives to `/var/backups`, 7 rotations), man-db (daily, up to 12 h random; `mandb --quiet` at nice 19, idle I/O), logrotate (daily), fstrim (weekly, up to 100 min random), e2scrub_all (Sunday 03:10), fwupd-refresh (hourly with up to 1 h random; `fwupdmgr refresh`), anacron (07:30–23:30 hourly), motd-news (fires but exits without `motd-news-config`), update-notifier-download (5 min after start, then every 24 h), update-notifier-motd (weekly), systemd-tmpfiles-clean (system: 15 min after boot then daily; user: 5 min after start then daily), apport-autoreport (only if `/var/lib/apport/autoreport` exists), snapd.snap-repair (not on classic installs), sysstat (timers disabled by default), systemd-sysupdate (unit shipped; enablement on Ubuntu not established by these copies — no postinst enables it); the Tracker indexer (user service started with the GNOME session, 15 s initial sleep, crawl only after an unclean shutdown by default, file monitors on); for packages outside the default install: plocate updatedb (daily, up to 12 h random), ClamAV signature updates (freshclam daemon, 24 checks a day by default; no scheduled scan), DKMS autoinstall on kernel installation (hook in `/etc/kernel/postinst.d`, `make -j$(nproc)` per module, modules built one after another), Déjà Dup (periodic backup off by default; monitor autostarts 120 s after login). Does not cover typical durations, how often the jobs find work, or the DKMS module set on real desktops — those need observations. Supports existence only. T8 — covers executable paths of tracker-miner-fs-3, updatedb.plocate, freshclam, clamd, dkms, mandb, logrotate, fwupdmgr (see S2-12 for comm derivation); and that Ubuntu 24.04 does not switch on mutter's `autoclose-xwayland` experimental feature (see S2-22). Does not cover T3, T4, T7, T10.
- **One observation?** Not an observation; package versions named; platform Ubuntu 24.04 amd64; no machine, no window.

### S2-04 — Tracker Miners 3.7.1 source: when the file indexer re-crawls

- **Citation.** GNOME, *tracker-miners* (now LocalSearch) 3.7.1, files `src/miners/fs/tracker-main.c`, `src/miners/fs/tracker-miner-files.c`, `src/miners/fs/tracker-config.c`.
- **Copy read.** `git clone --depth 1 --branch 3.7.1 https://gitlab.gnome.org/GNOME/localsearch.git`, commit eae431ef23ddbf0910bc716f36b5f7512c783752 (2024-03-27), accessed 2026-10-01. Local `sources/S2-04/tracker-miners-3.7.1/`. (Ubuntu ships 3.7.1-1ubuntu0.1, S2-03.)
- **Passages.** `tracker-config.c:49`, `tracker-main.c:240–284` (whether to crawl), `tracker-main.c:964–995` (whether to check mtimes), `tracker-main.c:1033–1037` (clean shutdown), `tracker-miner-files.c:1341–1370`:

`S2-04/tracker-miners-3.7.1/src/miners/fs/tracker-config.c:49`
```text
#define DEFAULT_CRAWLING_INTERVAL                -1       /* 0->365 / -1 / -2 */
```
`S2-04/tracker-miners-3.7.1/src/miners/fs/tracker-main.c:240–284`
```text
static gboolean
should_crawl (TrackerMinerFiles *miner_files,
              TrackerConfig     *config,
              gboolean          *forced)
{
	gint crawling_interval;

	crawling_interval = tracker_config_get_crawling_interval (config);

	TRACKER_NOTE (CONFIG, g_message ("Checking whether to crawl file system based on configured crawling interval:"));

	if (crawling_interval == -2) {
		TRACKER_NOTE (CONFIG, g_message ("  Disabled"));
		return FALSE;
	} else if (crawling_interval == -1) {
		TRACKER_NOTE (CONFIG, g_message ("  Maybe (depends on a clean last shutdown)"));
		return TRUE;
	} else if (crawling_interval == 0) {
		TRACKER_NOTE (CONFIG, g_message ("  Forced"));

		if (forced) {
			*forced = TRUE;
		}

		return TRUE;
	} else {
		guint64 then, now;

		then = tracker_miner_files_get_last_crawl_done (miner_files);

		if (then < 1) {
			return TRUE;
		}

		now = (guint64) time (NULL);

		if (now < then + (crawling_interval * SECONDS_PER_DAY)) {
			TRACKER_NOTE (CONFIG, g_message ("  Postponed"));
			return FALSE;
		} else {
			TRACKER_NOTE (CONFIG, g_message ("  (More than) %d days after last crawling, enabled", crawling_interval));
			return TRUE;
		}
	}
}
```
`S2-04/tracker-miners-3.7.1/src/miners/fs/tracker-main.c:964–995`
```text
	/* Check if we should crawl and if we should force mtime
	 * checking based on the config.
	 */
	do_crawling = should_crawl (TRACKER_MINER_FILES (miner_files),
	                            config, &force_mtime_checking);

	/* Get the last shutdown state to see if we need to perform a
	 * full mtime check against the db or not.
	 *
	 * Set to TRUE here in case we crash and miss file system
	 * events.
	 */
	TRACKER_NOTE (CONFIG, g_message ("Checking whether to force mtime checking during crawling (based on last clean shutdown):"));

	/* Override the shutdown state decision based on the config */
	if (force_mtime_checking) {
		do_mtime_checking = TRUE;
	} else {
		do_mtime_checking = tracker_miner_files_get_need_mtime_check (TRACKER_MINER_FILES (miner_files));
	}

	TRACKER_NOTE (CONFIG, g_message ("  %s %s",
	                      do_mtime_checking ? "Yes" : "No",
	                      force_mtime_checking ? "(forced from config)" : ""));

	/* Set the need for an mtime check to TRUE so we check in the
	 * event of a crash, this is changed back on shutdown if
	 * everything appears to be fine.
	 */
	if (!dry_run) {
		tracker_miner_files_set_need_mtime_check (TRACKER_MINER_FILES (miner_files), TRUE);
		tracker_miner_files_set_mtime_checking (TRACKER_MINER_FILES (miner_files), do_mtime_checking);
```
`S2-04/tracker-miners-3.7.1/src/miners/fs/tracker-main.c:1033–1037`
```text

	g_debug ("Shutdown started");

	if (!dry_run && miners_timeout_id == 0 && !miner_needs_check (miner_files))
		tracker_miner_files_set_need_mtime_check (TRACKER_MINER_FILES (miner_files), FALSE);
```
`S2-04/tracker-miners-3.7.1/src/miners/fs/tracker-miner-files.c:1341–1370`
```text
gboolean
tracker_miner_files_get_need_mtime_check (TrackerMinerFiles *mf)
{
	gboolean exists;
	gchar *filename;

	filename = get_need_mtime_check_filename (mf);
	exists = g_file_test (filename, G_FILE_TEST_EXISTS);
	g_free (filename);

	/* Existence of the file means we cleanly shutdown before and
	 * don't need to do the mtime check again on this start.
	 */
	return !exists;
}

/**
 * tracker_miner_files_set_need_mtime_check:
 * @needed: a #gboolean
 *
 * If the next start of miner-fs should perform a full mtime check
 * against each directory found and those in the database (for
 * complete synchronisation), then @needed should be #TRUE, otherwise
 * #FALSE.
 *
 * Creates a file in $HOME/.cache/tracker/ if an mtime check is not
 * needed. The idea behind this is that a check is forced if the file
 * is not cleaned up properly on shutdown (i.e. due to a crash or any
 * other uncontrolled shutdown reason).
 **/
```
- **Coverage.** T5 — covers what triggers a full mtime re-check of the indexed tree in Tracker 3.7 with default settings: the miner crawls at each start, and does a full mtime comparison of every directory against the database only when the previous run did not shut down cleanly (a stamp file in `$HOME/.cache/tracker/` marks clean shutdowns), or always when `crawling-interval` is 0. Does not cover how often unclean shutdowns or re-crawls happen, or their duration. Supports existence only.
- **One observation?** Not an observation; version 3.7.1 named.

### S2-05 — KDE Baloo v6.30.0 source: first run and per-start checks; unit and executable names

- **Citation.** KDE, *Baloo* (KDE Frameworks) v6.30.0, `src/file/main.cpp`, `src/file/fileindexscheduler.cpp`, `src/file/kde-baloo.service.in`, `src/file/CMakeLists.txt`, `src/file/extractor/CMakeLists.txt`.
- **Copy read.** `git clone --depth 1 --branch v6.30.0 https://invent.kde.org/frameworks/baloo.git`, commit a5b829873849ce72eb35d2c1b48337b2d81a0593 (2026-09-04), accessed 2026-10-01. Local `sources/S2-05/baloo-v6.30.0/`.
- **Passages.** `main.cpp:59–75` (first run = no index file, or a corrupt database), `fileindexscheduler.cpp:26–38` (both checks set at construction, i.e. at every start of the daemon), `:87–104` (first-run full index), `:156–186` (stale-entry clean and unindexed-file check), `:212–224` (a configuration change sets both again), the user unit, and the executable names:

`S2-05/baloo-v6.30.0/src/file/main.cpp:59–75`
```text
    bool firstRun = !QFile::exists(path + QStringLiteral("/index"));

    Baloo::Database *db = Baloo::globalDatabaseInstance();

    /**
     * try to open, if that fails, try to unlink the index db and retry
     */
    using OpenResult = Baloo::Database::OpenResult;
    if (auto rc = db->open(Baloo::Database::CreateDatabase); rc != OpenResult::Success) {
        if (rc == OpenResult::InvalidPath) {
            return 1;
        }
        // delete old stuff, set to initial run!
        qCWarning(BALOO) << "Failed to create database, removing corrupted database.";
        QFile::remove(path + QStringLiteral("/index"));
        QFile::remove(path + QStringLiteral("/index-lock"));
        firstRun = true;
```
`S2-05/baloo-v6.30.0/src/file/fileindexscheduler.cpp:26–38`
```text
FileIndexScheduler::FileIndexScheduler(Database *db, FileIndexerConfig *config, bool firstRun, QObject *parent)
    : QObject(parent)
    , m_db(db)
    , m_config(config)
    , m_provider(db)
    , m_contentIndexer(nullptr)
    , m_indexerState(Startup)
    , m_checkUnindexedFiles(true)
    , m_checkStaleIndexEntries(true)
    , m_isGoingIdle(false)
    , m_isSuspended(false)
    , m_isFirstRun(firstRun)
    , m_inStartup(true)
```
`S2-05/baloo-v6.30.0/src/file/fileindexscheduler.cpp:87–104`
```text
    if (m_isFirstRun) {
        if (m_inStartup) {
            return;
        }

        m_isFirstRun = false;
        // Not necessary immediately after initial run
        m_checkStaleIndexEntries = false;
        m_checkUnindexedFiles = false;

        auto runnable = new FirstRunIndexer(m_db, m_config, m_config->includeFolders());
        connect(runnable, &FirstRunIndexer::done, this, &FileIndexScheduler::runnerFinished);

        m_threadPool.start(runnable);
        m_indexerState = FirstRun;
        Q_EMIT stateChanged(m_indexerState);
        return;
    }
```
`S2-05/baloo-v6.30.0/src/file/fileindexscheduler.cpp:156–186`
```text
    // This has to be above content indexing, because there can be files that
    // should not be indexed in the DB (i.e. if config was changed)
    if (m_checkStaleIndexEntries) {
        auto runnable = new IndexCleaner(m_db, m_config);
        connect(runnable, &IndexCleaner::done, this, &FileIndexScheduler::runnerFinished);

        m_threadPool.start(runnable);
        m_checkStaleIndexEntries = false;
        m_indexerState = StaleIndexEntriesClean;
        Q_EMIT stateChanged(m_indexerState);
        return;
    }

    if (auto remainingCount = m_provider.size(); remainingCount > 0) {
        m_timeEstimator.setProgress(remainingCount);
        m_threadPool.start(m_contentIndexer);
        m_indexerState = ContentIndexing;
        Q_EMIT stateChanged(m_indexerState);
        return;
    }

    if (m_checkUnindexedFiles) {
        auto runnable = new UnindexedFileIndexer(m_db, m_config);
        connect(runnable, &UnindexedFileIndexer::done, this, &FileIndexScheduler::runnerFinished);

        m_threadPool.start(runnable);
        m_checkUnindexedFiles = false;
        m_indexerState = UnindexedFileCheck;
        Q_EMIT stateChanged(m_indexerState);
        return;
    }
```
`S2-05/baloo-v6.30.0/src/file/fileindexscheduler.cpp:212–224`
```text
void FileIndexScheduler::updateConfig()
{
    // Interrupt content indexer, to avoid indexing files that should
    // not be indexed (bug 373430)
    if (m_indexerState == ContentIndexing) {
        m_contentIndexer->quit();
    }
    removeShouldNotIndex(m_newFiles, m_config);
    removeShouldNotIndex(m_modifiedFiles, m_config);
    removeShouldNotIndex(m_xattrFiles, m_config);
    m_checkStaleIndexEntries = true;
    m_checkUnindexedFiles = true;
    scheduleIndexing();
```
`S2-05/baloo-v6.30.0/src/file/kde-baloo.service.in:1–20`
```text
[Unit]
Description=Baloo File Indexer Daemon
PartOf=graphical-session.target

[Service]
ExecStart=@KDE_INSTALL_FULL_LIBEXECDIR_KF@/baloo_file
BusName=org.kde.baloo
Slice=background.slice
ExecCondition=@KDE_INSTALL_FULL_BINDIR@/kde-systemd-start-condition --condition "baloofilerc:Basic Settings:Indexing-Enabled:true"
# We'll basically only want to consume resources if they aren't needed anywhere else, hence weights are way low.
CPUWeight=1
IOWeight=1
# Used memory includes any generated data, notably any transient allocation done
# by the extractors. A too low limit will cause significant slowdown, causing the
# extractor to hold onto the memory instead of releasing it in a timely manner
# after a transaction has finished.
MemoryHigh=25%

[Install]
WantedBy=graphical-session.target
```
`grep -n -E 'add_executable' S2-05/baloo-v6.30.0/src/file/CMakeLists.txt`
```text
73:    add_executable(baloo_file ${file_SRCS})
```
`grep -n -E 'add_executable' S2-05/baloo-v6.30.0/src/file/extractor/CMakeLists.txt`
```text
25:add_executable(baloo_file_extractor ${EXTRACTOR_SRCS})
```
- **Coverage.** T5 — covers what triggers Baloo's full index (no index file or a database that fails to open) and that every start of `baloo_file` schedules a stale-entry clean and a walk for unindexed files; the daemon runs in `background.slice` with CPU and I/O weight 1. Does not cover frequency or duration. Supports existence only. T8 — executable names `baloo_file` and `baloo_file_extractor` (20 bytes; comm derivation in S2-12). Platform: KDE on any distribution; Ubuntu 24.04 packages these as `baloo-kf5` (S2-12), not in the default install.
- **One observation?** Not an observation; version named.

### S2-06 — Fedora 44 Workstation: systemd presets, package groups, dnf5 makecache timer

- **Citation.** Fedora Project, `rpms/fedora-release` branch f44 (`90-default.preset`, `80-workstation.preset`); Fedora comps `comps-f44.xml.in`; *dnf5* 5.4.6.0 `etc/systemd/dnf5-makecache.{timer,service}`; Fedora `rpms/dnf5` branch f44 `dnf5.spec`.
- **Copy read.** fedora-release: `git clone --depth 1 --branch f44 https://src.fedoraproject.org/rpms/fedora-release.git`, commit 818360081645fb80f235036073a01f080cd7eb9d (2026-05-13). comps: https://forge.fedoraproject.org/releng/fedora-comps/raw/branch/main/comps-f44.xml.in, last commit touching the file a164862aba29a914f13958343b894cfae63b3915 (2026-07-30), SHA-256 c58d2146883e47e2d30904d3e2fa74f42840ca9977ac28dbef56321e3dcf4036. dnf5: `git clone --depth 1 --branch 5.4.6.0 https://github.com/rpm-software-management/dnf5.git`, commit 1b2de4bdc2f25a6de2884fb2cf81f80a8ce2a567. dnf5.spec (f44, Version 5.4.6 by its `project_version_*` macros): https://src.fedoraproject.org/rpms/dnf5/raw/f44/f/dnf5.spec, SHA-256 c660ee24f82ad7eaea886f7c422597b992a23031e9199476f75c92f27c74ff14. All accessed 2026-10-01. Local `sources/S2-06/`.
- **Passages.** `90-default.preset` timer lines:

`grep -n -E '\.timer' S2-06/fedora-release-f44/90-default.preset`
```text
166:enable raid-check.timer
175:enable dnf-makecache.timer
178:enable rpm-ostree-countme.timer
194:enable x509watch.timer
213:enable unbound-anchor.timer
243:enable sysstat-collect.timer
244:enable sysstat-summary.timer
265:enable mlocate-updatedb.timer
268:enable plocate-updatedb.timer
271:enable sa-update.timer
294:enable snapd.refresh.timer
379:enable fstrim.timer
387:enable logrotate.timer
391:enable sa-update.timer
415:enable certbot-renew.timer
```

comps: the Workstation environment's group list (lines 5974–5995) and the `workstation-product` group's default packages (group id at line 5387):

`S2-06/comps-f44.xml.in:5974–5995`
```text
    <id>workstation-product-environment</id>
    <!-- Translators: Don't translate this product name -->
    <_name>Fedora Workstation</_name>
    <_description>Fedora Workstation is a user friendly desktop system for laptops and PCs.</_description>
    <display_order>2</display_order>
    <!-- Keep this list in sync with the list in fedora-workstation-common.ks. -->
    <grouplist>
      <groupid>base-graphical</groupid>
      <groupid>container-management</groupid>
      <groupid>core</groupid>
      <groupid>firefox</groupid>
      <groupid>fonts</groupid>
      <groupid>gnome-desktop</groupid>
      <groupid>guest-desktop-agents</groupid>
      <groupid>hardware-support</groupid>
      <groupid>libreoffice</groupid>
      <groupid>multimedia</groupid>
      <groupid>networkmanager-submodules</groupid>
      <groupid>printing</groupid>
      <groupid>workstation-product</groupid>
      <groupid>desktop-accessibility</groupid>
    </grouplist>
```
`grep -n -E '<packagereq type="default">(logrotate|mdadm|plocate|rsync|sos)</packagereq>|<id>workstation-product</id>' S2-06/comps-f44.xml.in`
```text
5387:    <id>workstation-product</id>
5449:      <packagereq type="default">logrotate</packagereq>
5455:      <packagereq type="default">mdadm</packagereq>
5471:      <packagereq type="default">plocate</packagereq>
5482:      <packagereq type="default">rsync</packagereq>
5483:      <packagereq type="default">sos</packagereq>
```
`grep -n -E '<packagereq type="(mandatory|default)">(dnf5|man-db|fwupd|localsearch|gnome-software)</packagereq>' S2-06/comps-f44.xml.in`
```text
482:      <packagereq type="mandatory">gnome-software</packagereq>
665:      <packagereq type="mandatory">dnf5</packagereq>
674:      <packagereq type="mandatory">man-db</packagereq>
695:      <packagereq type="default">fwupd</packagereq>
855:      <packagereq type="default">gnome-software</packagereq>
2299:      <packagereq type="mandatory">gnome-software</packagereq>
2345:      <packagereq type="default">localsearch</packagereq>
5396:      <packagereq type="mandatory">dnf5</packagereq>
```

Reader's own computation (Python `xml.etree` over `comps-f44.xml.in`: for each group in the `workstation-product-environment` grouplist, print `packagereq` entries in a fixed list) gave: `core dnf5 mandatory`, `core man-db mandatory`, `core fwupd default`, `gnome-desktop gnome-software mandatory`, `gnome-desktop localsearch default`, `workstation-product logrotate default`, `workstation-product mdadm default`, `workstation-product plocate default`, `workstation-product rsync default`.

dnf5 makecache units at 5.4.6.0, and the Fedora spec's renaming:

`S2-06/dnf5-5.4.6.0/etc/systemd/dnf5-makecache.timer:1–15`
```text
[Unit]
Description=dnf5 makecache
ConditionKernelCommandLine=!rd.live.image
# See comment in dnf5-makecache.service
ConditionPathExists=!/run/ostree-booted
Wants=network-online.target

[Timer]
OnBootSec=10min
OnUnitInactiveSec=3h
RandomizedDelaySec=60m
Unit=dnf5-makecache.service

[Install]
WantedBy=timers.target
```
`S2-06/dnf5-5.4.6.0/etc/systemd/dnf5-makecache.service:1–16`
```text
[Unit]
Description=dnf5 makecache
# On systems managed by either rpm-ostree/ostree, dnf is read-only;
# while someone might theoretically want the cache updated, in practice
# anyone who wants that could override this via a file in /etc.
ConditionPathExists=!/run/ostree-booted
ConditionACPower=true

After=network-online.target

[Service]
Type=oneshot
Nice=19
IOSchedulingClass=2
IOSchedulingPriority=7
ExecStart=/usr/bin/dnf5 makecache
```
`S2-06/dnf5.spec-f44:1139–1143`
```text
# Make "dnf-makecache" the "real" unit name, but keep compatibility for playbooks that refer to dnf5-makecache
mv %{buildroot}%{_unitdir}/dnf5-makecache.service %{buildroot}%{_unitdir}/dnf-makecache.service
mv %{buildroot}%{_unitdir}/dnf5-makecache.timer %{buildroot}%{_unitdir}/dnf-makecache.timer
ln -s dnf-makecache.service %{buildroot}%{_unitdir}/dnf5-makecache.service
ln -s dnf-makecache.timer %{buildroot}%{_unitdir}/dnf5-makecache.timer
```
- **Coverage.** T5 — covers the comparison distribution: on Fedora 44 Workstation the vendor preset enables dnf-makecache (10 min after boot, then 3 h after the last run, up to 60 min random; `dnf5 makecache` at nice 19, on AC power), plocate-updatedb, fstrim, logrotate and raid-check (mdadm), all for packages in the Workstation groups; the other enabled timers (sysstat, sa-update, unbound-anchor, snapd, certbot and others) belong to packages the reader's check did not find in those groups (sysstat was checked and is absent); `fwupd-refresh.timer` is enabled only by the server and IoT presets. Supports existence only. T8 — Workstation installs LocalSearch (not Tracker 3.7) and plocate by default. Does not cover T3, T4, T7, T10.
- **One observation?** Not an observation; branch and versions named.

### S2-07 — GNOME Software 50.4 source: how often the update monitor refreshes and downloads

- **Citation.** GNOME, *gnome-software* 50.4 (the version in the Fedora 44 spec), `src/gs-update-monitor.c`, `data/org.gnome.software.gschema.xml`.
- **Copy read.** `git clone --depth 1 --branch 50.4 https://gitlab.gnome.org/GNOME/gnome-software.git`, commit eda622eabcdf0cdd1b9004612f2b695211cb46e4 (2026-09-10), accessed 2026-10-01. Local `sources/S2-07/gnome-software-50.4/`.
- **Passages.**

`S2-07/gnome-software-50.4/data/org.gnome.software.gschema.xml:13–17`
```text
    <key name="download-updates" type="b">
      <default>true</default>
      <summary>Automatically download and install updates</summary>
      <description>If enabled, GNOME Software automatically downloads software updates in the background, also installing ones that do not require a reboot.</description>
    </key>
```
`S2-07/gnome-software-50.4/src/gs-update-monitor.c:1045`
```text
	monitor->randomized_hour = g_random_int_range (0, 6);
```
`S2-07/gnome-software-50.4/src/gs-update-monitor.c:1104–1123`
```text

		/* check that it is the next day */
		if (day_interval < G_TIME_SPAN_DAY) {
			g_debug ("Not getting updates, did so not more than a day ago");
			return;
		}

		/* ...and past 6-11am (with randomized hour), if interval is within 2 days */
		if (day_interval < 2 * G_TIME_SPAN_DAY && !(now_hour >= 6 + monitor->randomized_hour)) {
			g_debug ("Not getting updates, it's too early");
			return;
		}

		/* or the update has been delayed another day
		 * randomized_hour should not be used in this case
		 */
		if (day_interval >= 2 * G_TIME_SPAN_DAY && !(now_hour >= 6)) {
			g_debug ("Not getting updates, it's before 6 am");
			return;
		}
```
`S2-07/gnome-software-50.4/src/gs-update-monitor.c:1255–1263`
```text
static void
restart_updates_check (GsUpdateMonitor *monitor)
{
	stop_updates_check (monitor);
	check_updates (monitor);

	monitor->check_hourly_id = g_timeout_add_seconds (SECONDS_IN_AN_HOUR, check_hourly_cb,
							  monitor);
}
```
`S2-07/gnome-software-50.4/src/gs-update-monitor.c:1600–1602`
```text
	/* do a first check 60 seconds after login, and then every hour */
	monitor->check_startup_id =
		g_timeout_add_seconds (60, check_updates_on_startup_cb, monitor);
```
- **Coverage.** T5 — covers the package-metadata refresh and update download that GNOME Software runs unasked on Fedora Workstation (a check 60 s after login, then hourly; an actual refresh at most once per calendar day, after 06:00 plus a random 0–5 h; downloads enabled by default). Not part of Ubuntu 24.04's default install (S2-01 lists `snap:snap-store` instead). Supports existence only.
- **One observation?** Not an observation; version named.

### S2-08 — snapd 2.76.3: default snap refresh schedule

- **Citation.** Canonical, *snapd* 2.76.3, `overlord/snapstate/autorefresh.go`.
- **Copy read.** https://raw.githubusercontent.com/canonical/snapd/2.76.3/overlord/snapstate/autorefresh.go (tag 2.76.3 → commit 58163ecc3eae8d0581d893934115eb354d85f85e), accessed 2026-10-01, SHA-256 f4d485ff1d4a87aa445aba2fd9551907b2c2e84b691a13caf5f08baad110bbf6. Local `sources/S2-08/autorefresh.go-2.76.3`. (Ubuntu 24.04.5.1 ships snapd 2.76.3+ubuntu24.04, S2-01.)
- **Passages.**

`S2-08/autorefresh.go-2.76.3:50–56`
```text
const defaultRefreshScheduleStr = "00:00~24:00/4"

// cannot keep without refreshing for more than maxPostponement
const maxPostponement = 95 * 24 * time.Hour

// buffer for maxPostponement when holding snaps with auto-refresh gating
const maxPostponementBuffer = 5 * 24 * time.Hour
```
`S2-08/autorefresh.go-2.76.3:88–89`
```text
// refreshRetryDelay specified the minimum time to retry failed refreshes
var refreshRetryDelay = 20 * time.Minute
```
- **Coverage.** T5 — covers the package refresh that runs unasked for snaps (Firefox, Thunderbird, the App Center and the firmware updater are snaps on Ubuntu 24.04): four refresh windows a day by default (`00:00~24:00/4`). Supports existence only; whether a refresh finds an update, and its duration, need observation.
- **One observation?** Not an observation; version named.

### S2-09 — Arch Linux packages: timers enabled by the package itself

- **Citation.** Arch Linux packages shadow 4.20.0.arch1-1, man-db 2.13.1-2, archlinux-keyring 20260909-1, systemd 262-1, plocate 1.1.25-1, logrotate 3.22.0-1, util-linux, pacman-contrib, fwupd (file lists); packaging repository files `shadow.timer`, `shadow.service`, man-db `PKGBUILD`; archlinux-keyring `wkd_sync/archlinux-keyring-wkd-sync.timer`.
- **Copy read.** `https://archlinux.org/packages/<repo>/<arch>/<pkg>/json/` and `/files/json/`; `https://gitlab.archlinux.org/archlinux/packaging/packages/shadow/-/raw/4.20.0.arch1-1/shadow.timer` (and `shadow.service`); `.../man-db/-/raw/2.13.1-2/PKGBUILD`; `https://gitlab.archlinux.org/archlinux/archlinux-keyring/-/raw/20260909/wkd_sync/archlinux-keyring-wkd-sync.timer`; accessed 2026-10-01. Local `sources/S2-09/`. SHA-256: shadow.files.json 5bc334ce5b5898e2ec27bed199e9759cae2c793eefc495b017b272259fb1befe; man-db.files.json 6b7eb0a8966d08426a00129dd6d012c0d1b379b625a1260e2afc89fc208b843b; archlinux-keyring.files.json 97cbe952fe667a5dd610a8d4df736eeef08576007f164e77c3169a4ff9160a90; systemd.files.json 750f3fa800dabd504f8ade23da42bc1838e7610cce56e0a3162a07abce7ed889; plocate.files.json bbc96cd22273e0bf2797ad9778220650ea11925936b0dc6145f5e56df4ed4d09; logrotate.files.json 4c6d96551b7417028d490c9a29d9cf13862227098dbad8c9bfe351d309576253; util-linux.files.json 75fe6e5f24b7e6792f1cf8c2dd5f242cae7939eaf4f1223f403f2d06286b283e; pacman-contrib.files.json 7c4e9e72d124cf63e2b90c2604fe7790189e7791d415ba688d7238d36513a161; fwupd.files.json b96e1d5fece96a3525ce04cca5486829ba9617a8455ff75c83c1090b6993f5f8; shadow.timer, shadow.service, archlinux-keyring-wkd-sync.timer, PKGBUILD — see the shell hash list in §2 end note.
- **Passages.** Verbatim strings from the file-list JSON (each is one element of the `files` array): shadow `"usr/lib/systemd/system/timers.target.wants/shadow.timer"`; man-db `"usr/lib/systemd/system/timers.target.wants/man-db.timer"`; archlinux-keyring `"usr/lib/systemd/system/timers.target.wants/archlinux-keyring-wkd-sync.timer"`; systemd `"usr/lib/systemd/system/timers.target.wants/systemd-tmpfiles-clean.timer"`; plocate `"usr/lib/systemd/system/timers.target.wants/plocate-updatedb.timer"`; logrotate `"usr/lib/systemd/system/timers.target.wants/logrotate.timer"`; util-linux has `"usr/lib/systemd/system/fstrim.timer"` and no `timers.target.wants` entry; pacman-contrib has `"usr/lib/systemd/system/paccache.timer"` and `"usr/lib/systemd/system/pacman-filesdb-refresh.timer"` and no `timers.target.wants` entry; fwupd has `"usr/lib/systemd/system/fwupd-refresh.timer"` and no `timers.target.wants` entry.

`S2-09/shadow.timer:1–7`
```text
[Unit]
Description=Daily verification of password and group files

[Timer]
OnCalendar=daily
AccuracySec=12h
Persistent=true
```
`S2-09/shadow.service:5–11`
```text
[Service]
CapabilityBoundingSet=CAP_DAC_READ_SEARCH
# Always run both checks, but fail the service if either fails
ExecStart=/bin/sh -c '/usr/bin/pwck -qr || r=1; /usr/bin/grpck -r && exit $r'
Nice=19
IOSchedulingClass=best-effort
IOSchedulingPriority=7
```
`S2-09/archlinux-keyring-wkd-sync.timer:1–7`
```text
[Unit]
Description=Refresh existing PGP keys of archlinux-keyring regularly

[Timer]
OnCalendar=weekly
Persistent=true
RandomizedDelaySec=1week
```
`S2-09/PKGBUILD:56–57`
```text
  install -d -m755 "${pkgdir}/usr/lib/systemd/system/timers.target.wants"
  ln -s ../man-db.timer "${pkgdir}/usr/lib/systemd/system/timers.target.wants/man-db.timer"
```
- **Coverage.** T5 — covers the Arch comparison: shadow (daily pwck/grpck), man-db, archlinux-keyring WKD sync (weekly, up to one week random), systemd-tmpfiles-clean, and plocate and logrotate when installed, are enabled by the package itself; fstrim, paccache, pacman-filesdb-refresh and fwupd-refresh are shipped but not enabled. Which packages a "desktop" Arch install has is user-chosen; not covered. Supports existence only.
- **One observation?** Not an observation; versions named.

### S2-10 — Debian 13 (trixie) desktop task

- **Citation.** Debian, `task-desktop` and `task-gnome-desktop` (tasksel 3.81) in trixie; tasksel 3.81 `debian/control`.
- **Copy read.** https://packages.debian.org/trixie/task-desktop (SHA-256 bf0af57fbb74275add50d5f8f64ad64ebfd2a7e9492c04f83a1166a3e4e02c10), https://packages.debian.org/trixie/task-gnome-desktop (SHA-256 154aa87f200887b7a6477fcea62079f697b9c9a65a43f539c2077021117c349c), https://sources.debian.org/data/main/t/tasksel/3.81/debian/control; trixie versions from sources.debian.org API: plocate 1.1.23-1, man-db 2.13.1-1, logrotate 3.22.0-1, apt 3.0.3, sysstat 12.7.5-2. Accessed 2026-10-01. Local `sources/S2-10/`.
- **Passages.** `task-desktop-trixie.txt` (text conversion) lines 97–101 and 114–119:

`S2-10/task-desktop-trixie.txt:97–101`
```text
rec:
alsa-utils
Utilities for configuring and using ALSA
rec:
anacron
```
`S2-10/task-desktop-trixie.txt:114–119`
```text
rec:
	firefox
Package not available
or
firefox-esr
Mozilla Firefox web browser - Extended Support Release (ESR)
```
`S2-10/tasksel-3.81-control:34–46`
```text
Package: task-desktop
Architecture: all
Description: Debian desktop environment
 This task package is used to install the Debian desktop.
Depends: ${misc:Depends},
	xorg,
	xserver-xorg-video-all,
	xserver-xorg-input-all,
	desktop-base,
Recommends:
# One of the actual desktop tasks is needed to get a full desktop environment.
# The order here is significant when installing this task manually;
# when tasksel installs this task it instead selects one of these based
```
- **Coverage.** T5 — covers only that Debian's desktop task recommends anacron (and cron-like jobs then run through it); Debian's timer units for apt, dpkg, man-db, logrotate, e2fsprogs and util-linux come from the same Debian source packages Ubuntu builds on (S2-03), not read here at Debian versions. Weak; supports existence only.
- **One observation?** Not an observation.

### S2-11 — Linux kernel source: how `comm` is set and truncated

- **Citation.** Linux kernel v6.8 (Ubuntu 24.04 GA kernel series) and v7.0 (the 24.04.5.1 HWE kernel series, S2-01): `include/linux/sched.h`, `fs/exec.c`; v6.8 `fs/binfmt_script.c`, `kernel/sys.c`.
- **Copy read.** `https://raw.githubusercontent.com/torvalds/linux/<tag>/<path>`, accessed 2026-10-01. Local `sources/S2-11/`. SHA-256: v6.8 sched.h be70b3be89004663fc7a2a242d8ad38bdc9fc31a4870a42a9a8c159b214b5409; v6.8 exec.c 6df9a811b61b67caf4b48a3d55b2bf89ce46a8147563ce3fdbfaf86dccbc9838; v7.0 sched.h ee580d7e320b105ac6d699bfcf3a77baf9ea076a54fe951079bf9500fd055485; v7.0 exec.c af1d3a7298fae9c0b52b8e7017f2aa88958ad3787294bf1f1a816a3ee7a95a64; v6.8 binfmt_script.c 47b13f8fb3a11fd33c672163d2bfaa958d73be945d9770604dac808a92250a63; v6.8 sys.c a5dbbc30a1dc3cc545e72fe6652435d9923b6fa15293911b02d4fc5591481b87.
- **Passages.** v6.8 `sched.h:296–302`, `:1083–1085`; `exec.c:1245–1252`, `:1380`; v7.0 `exec.c:1222–1239`, v7.0 `sched.h:1160–1169`; v6.8 `binfmt_script.c:121–136`; `exec.c:1589–1598`; `sys.c:2504–2511`:

`S2-11/v6.8-include_linux_sched.h:296–302`
```text
/*
 * Define the task command name length as enum, then it can be visible to
 * BPF programs.
 */
enum {
	TASK_COMM_LEN = 16,
};
```
`S2-11/v6.8-include_linux_sched.h:1083–1085`
```text
	 * - lock it with task_lock()
	 */
	char				comm[TASK_COMM_LEN];
```
`S2-11/v6.8-fs_exec.c:1245–1252`
```text
void __set_task_comm(struct task_struct *tsk, const char *buf, bool exec)
{
	task_lock(tsk);
	trace_task_rename(tsk, buf);
	strscpy_pad(tsk->comm, buf, sizeof(tsk->comm));
	task_unlock(tsk);
	perf_event_comm(tsk, exec);
}
```
`S2-11/v6.8-fs_exec.c:1380`
```text
	__set_task_comm(me, kbasename(bprm->filename), true);
```
`S2-11/v7.0-fs_exec.c:1222–1239`
```text
	 * Let's fix it up to be something reasonable.
	 */
	if (bprm->comm_from_dentry) {
		/*
		 * Hold RCU lock to keep the name from being freed behind our back.
		 * Use acquire semantics to make sure the terminating NUL from
		 * __d_alloc() is seen.
		 *
		 * Note, we're deliberately sloppy here. We don't need to care about
		 * detecting a concurrent rename and just want a terminated name.
		 */
		rcu_read_lock();
		__set_task_comm(me, smp_load_acquire(&bprm->file->f_path.dentry->d_name.name),
				true);
		rcu_read_unlock();
	} else {
		__set_task_comm(me, kbasename(bprm->filename), true);
	}
```
`S2-11/v7.0-include_linux_sched.h:1160–1169`
```text
	 * executable name, excluding path.
	 *
	 * - normally initialized begin_new_exec()
	 * - set it with set_task_comm()
	 *   - strscpy_pad() to ensure it is always NUL-terminated and
	 *     zero-padded
	 *   - task_lock() to ensure the operation is atomic and the name is
	 *     fully updated.
	 */
	char				comm[TASK_COMM_LEN];
```
`S2-11/v6.8-fs_binfmt_script.c:121–136`
```text
	retval = copy_string_kernel(i_name, bprm);
	if (retval)
		return retval;
	bprm->argc++;
	retval = bprm_change_interp(i_name, bprm);
	if (retval < 0)
		return retval;

	/*
	 * OK, now restart the process with the interpreter's dentry.
	 */
	file = open_exec(i_name);
	if (IS_ERR(file))
		return PTR_ERR(file);

	bprm->interpreter = file;
```
`S2-11/v6.8-fs_exec.c:1589–1598`
```text
int bprm_change_interp(const char *interp, struct linux_binprm *bprm)
{
	/* If a binfmt changed the interp, free it first. */
	if (bprm->interp != bprm->filename)
		kfree(bprm->interp);
	bprm->interp = kstrdup(interp, GFP_KERNEL);
	if (!bprm->interp)
		return -ENOMEM;
	return 0;
}
```
`S2-11/v6.8-kernel_sys.c:2504–2511`
```text
	case PR_SET_NAME:
		comm[sizeof(me->comm) - 1] = 0;
		if (strncpy_from_user(comm, (char __user *)arg2,
				      sizeof(me->comm) - 1) < 0)
			return -EFAULT;
		set_task_comm(me, comm);
		proc_comm_connector(me);
		break;
```
- **Coverage.** T8 — covers the rule by which `comm` is formed: at exec, the basename of the path passed to `execve` (for `execveat` with an empty path in v7.0, the file's dentry name), copied into a 16-byte buffer, so at most 15 bytes plus NUL; for a `#!` script the interpreter is recorded in `bprm->interp` and `bprm->filename` stays the script, so the script's own basename becomes `comm`; `prctl(PR_SET_NAME)` (and writes to `/proc/<pid>/task/<tid>/comm`) rename a thread later, truncated the same way. Supports existence of the mechanism only; the `comm` a given program shows needs a Linux observation.
- **One observation?** Not an observation; versions named.

### S2-12 — Ubuntu package file lists: executable names of the T8 programs

- **Citation.** packages.ubuntu.com file lists, amd64, in the suite noted (noble = 24.04 release pocket; noble-updates; resolute = 26.04 LTS).
- **Copy read.** `https://packages.ubuntu.com/<suite>/amd64/<pkg>/filelist`, accessed 2026-10-01. Local `sources/S2-12/<pkg>.filelist.html`. SHA-256 (suite): 7zip 26263b1a33a8fd73f1986bdd6f6c7095bcde7b0bf6882e39085e6dd9a0091e81 (noble); baloo-kf5 89e3b7c43f32d1b499f926cf3689755dac7c8d86dd553e5d5b0f92bfa4014743 (noble); blender 9e5e06a42279067fd63a405df8061e89c1168097f099ed9b36aa15651818f486 (noble); borgbackup 67ab52a32cb3c20be0109f319c0c4f0f293bd44082a95a4f16691f9c3ee13d35 (noble); chromium-browser 017ba10ba1c4d17b03ee87d1901679ec55995860a386c3bfc28490605b44f11c (noble); clamav 34bcfc9beede8598e78ddc00be32d7af7cf5ba1a4cef27afaa221027bccc0008, clamav-daemon 5e0954e37f888a979ce45959b4457f96d397be4a737fad434b4c425f86e0df55, clamav-freshclam 7400ecf097ce7af77a637a8408230dd86ace02f519cf43a65aa6ad17d7e0e537 (noble-updates); cpp-13-x86-64-linux-gnu 0d43277b9b236a52a9b8a228f76d35e25ff42a523e85b557a84a7fcbb5382a2a (noble-updates); darktable 7e8907fbefc6589326728b1b2cb2c28909d6c6d2a8cefcf195c0e49efbec87f8 (noble); dbus-broker 3d492f5a3c00462f1bb3f9075894873d7170c18bbd221fa58db1db5db7d421dc, dbus-daemon c0048357ce63f35158986d1fb56e4bb880bec92a582cde1681dda821c274b301 (noble-updates); deja-dup 0365d4f80387f49fe28040eb183e965f1f426168ea587391bf945144b0d9bfbf (noble); dkms 91b72c4a65e753e9f333691dbdfc5c308a2058fca8a1c8120337008ed8d4a5ed (noble); evince f635365bb4ca6926f7280224c6558546fa32b3511e6f080f7ec9fbc9fd32985d (noble-updates); ffmpeg 55c13a6cdc6b75889eb4466fd308628f1f5e8fb44ee979f08645bba9889ef6ab (noble); firefox 4881dd54b6a4f4704aef8f39db4b5b929fc34c6bee68bb231dba8b71c932405c (noble); gcc-13 99fe79e1889ae2eae99059ff7cd6dafbe3960b569e7f301b54bd33496714ca30 (noble-updates); gimp 0649204bd74719fca902780449042498952ada5a0031ea87aa69ffc34a3c7c12 (noble); gnome-shell 8f3addd97bf0c0527ff4a925163f7648b6a0346a70d3f791b3d30a8edfa2a247 (noble-updates); handbrake-cli 9b121fb2bab58eb52d836a40f8231e864360a76c813558ff10fc879e9c969dcb (noble); kdenlive a19d5c1975749379fc0a41056980c87c39b1d1aac189500d8e79646e13da5e2b (noble); libreoffice-core 427dd2a72f1167ade106bf22d55cc15fdea756c7ad97a4cad18d4762b89cd473 (noble-updates); localsearch 5d1050d632894266cf7f78a47ad105a89a3b9f0382ddbc143f94f2e5cfb919f1 (resolute; package page f84a39c70f60ece7653a6f3fd16a9a539dfdf96a1890a0e380bbf0acf54d6da4 shows localsearch 3.11.0-1ubuntu1); make ba62d444d16082f0a73b6abc6a6248194198bbbe03adc89983aee24de54c34c6 (noble); mpv 6fa19d61911cda0ba7587e3df273ac45c10f574c81dc0ee5e2d257d2087e054b (noble); pipewire-bin b437bcdf0f731f8bfdbc22a18f6ba57d6db9c64d67a419a98ffc11ef023c58da, pipewire-pulse 930e7d0300b111573ee383bf78d68ab06a6faf66c6cd69cb81b87ee16c0a0146 (noble-updates); plocate 8891f2ecb153852dfdb320da0046251c216c5efa6c06cd4dade06c7337000b95 (noble); python3-minimal f08519d4781f64536b49177d0c27db383f62273559930b908aa766ab6ef8b157, python3.12-minimal daabd08064b1e910a1cc662e10910b16092c3fc8bfb4413866ccbd9f30e49437 (noble-updates); rclone 501754515b2ca99b08d8a4d726b2adc6a5bf47a65c4a42439806f8f4d4cce6b3 (noble-updates); rsync eeae56b98909c74eb22fff1dd9b034ef5a5a6c02fe29254907b741adf94b14ad (noble-updates); snapper 081e2adab0e1ea4ec96fd20fa91ce0d43806c37c7b6b49421115ed917d9e8486 (noble); steam-installer ce714890f1f9da23bb8eabe311ac99734e949e555adc1e314cc22d4c35da80ff (noble); systemd c5134586cd2b08dc0f80c8913a83f29e30e97d78e805c55881d515244fc037f3 (noble-updates); tar 8f595d746b2f965a6999e32f2897f9a612e4e9f3d26cd110a2cf99f1c9715925 (noble-updates); thunderbird 798c2848e3335bcbc9df3b8f6876203857054b50eed2ab50cffdf76f33c3e000 (noble); timeshift d68d6fae94d430001784a4416ad08d2d0fb66e7add86d17264ffe91c9caffc9c (noble); tracker-extract 88ccbdbcfb5c804a4bd4a94fc0625f317da12d35f7f4ae5a61e4b4015c9c07a7, tracker-miner-fs bff56a8ee47245f39771291602dad4b5e87e48421d75817ee136c908e99857ca (noble-updates); vlc-bin f162c333663ea18c14d85ad8cff182a0a55549a4d08d64791e65e92221abd9d0 (noble); wine 4cf5c45bd4a328d145b4f70d4dc75db6cf4fb438bde068664a2eeb69777047a7, wine64 4ab1ec4d2f9642ee6358ba4faa94263e0cb4e8b2c7e71353989ef17f62ffb736 (noble); wireplumber 05199269a8ac8994385728acec9934253e9641c4c267677517449c1bff3c0ca3 (noble-updates); xserver-xorg-core f4531532c248770179038714123f89748a4ac8440d4258f41e857de050d71394, xwayland 8c16104fa1653c1364e1fd7f4926cefa34d4e69b72a66af737fadaa9d6b6f6e8, xz-utils 490b20e41c4da6016498783c3d77146136964b56e6bde489f41da9d1d83f424f (noble-updates); gamescope search page 5b1a956e7c36621a15a2aa2b329217f888ac42f1fd6cded9d6bcd8e883dd15f0.
- **Passages.** Executable paths as listed in each file list (verbatim path strings from the `<pre>` block):

`S2-12/<pkg>.filelist.html — <pkg>: matching paths`
```text
libreoffice-core: /usr/lib/libreoffice/program/oosplash  /usr/lib/libreoffice/program/soffice.bin
evince: /usr/bin/evince  /usr/libexec/evinced
gimp: /usr/bin/gimp  /usr/bin/gimp-2.10
darktable: /usr/bin/darktable
kdenlive: /usr/bin/kdenlive  /usr/bin/kdenlive_render
blender: /usr/bin/blender
mpv: /usr/bin/mpv
vlc-bin: /usr/bin/vlc
rsync: /usr/bin/rsync
rclone: /usr/bin/rclone
7zip: /usr/bin/7z
tar: /usr/bin/tar
xz-utils: /usr/bin/xz
handbrake-cli: /usr/bin/HandBrakeCLI
ffmpeg: /usr/bin/ffmpeg
python3-minimal: /usr/bin/python3
python3.12-minimal: /usr/bin/python3.12
make: /usr/bin/make
gcc-13: /usr/bin/gcc-13
cpp-13-x86-64-linux-gnu: /usr/libexec/gcc/x86_64-linux-gnu/13/cc1
dkms: /usr/sbin/dkms
gnome-shell: /usr/bin/gnome-shell
xserver-xorg-core: /usr/lib/xorg/Xorg
xwayland: /usr/bin/Xwayland
pipewire-bin: /usr/bin/pipewire
pipewire-pulse: /usr/bin/pipewire-pulse
wireplumber: /usr/bin/wireplumber
systemd: /usr/bin/systemd
dbus-daemon: /usr/bin/dbus-daemon
dbus-broker: /usr/bin/dbus-broker  /usr/bin/dbus-broker-launch
borgbackup: /usr/bin/borg
clamav: /usr/bin/clamscan
clamav-daemon: /usr/sbin/clamd
clamav-freshclam: /usr/bin/freshclam
plocate: /usr/sbin/updatedb.plocate
tracker-miner-fs: /usr/libexec/tracker-miner-fs-3
tracker-extract: /usr/libexec/tracker-extract-3
localsearch-resolute: /usr/libexec/localsearch-3  /usr/libexec/localsearch-extractor-3
baloo-kf5: /usr/bin/baloo_file  /usr/bin/baloo_file_extractor
steam-installer: /usr/games/steam
wine64: /usr/lib/wine/wine64  /usr/lib/wine/wineserver64
thunderbird: /usr/bin/thunderbird
firefox: /usr/bin/firefox
chromium-browser: /usr/bin/chromium-browser
deja-dup: /usr/libexec/deja-dup/deja-dup-monitor
timeshift: /usr/bin/timeshift
snapper: /usr/sbin/snapperd
```

gamescope search page (text): "questing (25.10) (games): Micro-compositor for game scaling [multiverse] … 3.16.15-2" and "resolute (26.04LTS) (games): … 3.16.20+ds-1"; no noble entry.
- **Reader's own derivation (not a value).** Applying the kernel rule of S2-11 (basename of the exec'd path, first 15 bytes) to these paths and to the paths in S2-16 to S2-25 gives the candidate `comm` strings below. A program started through a symlink or a differently named path shows that name instead (e.g. `/usr/bin/gimp` vs `gimp-2.10`); a process that renames itself with `prctl(PR_SET_NAME)` shows the new name (Firefox content processes, Wine processes, see S2-17 and S2-18). Each needs a Linux observation.

| Program | Executable (source) | Derived `comm` (first 15 bytes) | Default Ubuntu 24.04 install (S2-01) |
|---|---|---|---|
| LibreOffice Writer | `/usr/lib/libreoffice/program/soffice.bin` (launcher `oosplash`) | `soffice.bin`, `oosplash` | extended only |
| Evince | `/usr/bin/evince`, `/usr/libexec/evinced` | `evince`, `evinced` | yes |
| VS Code | `/usr/share/code/code` (S2-24) | `code` | no (vendor .deb) |
| Google Chrome | `/opt/google/chrome/chrome`, `chrome_crashpad_handler` (S2-24) | `chrome`, `chrome_crashpad` | no |
| Chromium | `/usr/bin/chromium-browser` (transitional deb; the browser is a snap) | not derivable from this list | no |
| Firefox | `/usr/bin/firefox` (transitional deb; snap in S2-01); content processes renamed (S2-17) | `firefox`; `Isolated Web Co`, `Web Content`, `WebExtensions`, `Privileged Cont` | yes (snap) |
| Thunderbird | `/usr/bin/thunderbird` (transitional; snap) | `thunderbird` | extended only |
| GIMP | `/usr/bin/gimp-2.10`, `/usr/bin/gimp` | `gimp-2.10` or `gimp` | no |
| darktable | `/usr/bin/darktable` | `darktable` | no |
| Kdenlive | `/usr/bin/kdenlive`, render helper `/usr/bin/kdenlive_render` | `kdenlive`, `kdenlive_render` | no |
| Blender | `/usr/bin/blender` | `blender` | no |
| mpv / VLC | `/usr/bin/mpv`; `/usr/bin/vlc` | `mpv`; `vlc` | no |
| Spotify | Flathub `command: spotify` (S2-25) | `spotify` | no |
| Zoom | `zoom/zoom`, `zoom/ZoomWebviewHost`, `zoom/aomhost`, `zoom/cpthost` (S2-25) | `zoom`, `ZoomWebviewHost` (15 bytes exactly), `aomhost`, `cpthost` | no |
| Microsoft Teams | no Microsoft Linux client (retired; PWA in Chrome or Edge, S2-26); community `teams-for-linux` | `teams-for-linux` (15 bytes) | no |
| Slack | `usr/lib/slack` (snap contents, S2-25) | not derivable | no |
| Discord | `Discord/` tree (S2-25) | not derivable | no |
| Element | `element-desktop` tarball (S2-25) | `element-desktop` (15 bytes) if the binary is so named — not seen | no |
| Steam | `/usr/games/steam` (launcher script) → `steam.sh` → `ubuntu12_32/steam` (S2-25) | `steam`, `steam.sh` | no |
| gamescope | `gamescope`, `gamescopereaper` (S2-21) | `gamescope`, `gamescopereape` | no (not in noble) |
| Wine / Proton | `/usr/lib/wine/wine64`, `/usr/lib/wine/wineserver64`; Proton `wine-preloader`, `wine` (S2-18) | `wine64`, `wineserver64`; Wine renames each process to its `.exe` basename (S2-18) | no |
| Tracker 3.7 | `/usr/libexec/tracker-miner-fs-3`, `/usr/libexec/tracker-extract-3` | `tracker-miner-f`, `tracker-extract` | yes |
| LocalSearch 3.11 | `/usr/libexec/localsearch-3`, `/usr/libexec/localsearch-extractor-3` (resolute) | `localsearch-3`, `localsearch-ext` | n/a (24.04 has Tracker) |
| Baloo | `/usr/bin/baloo_file`, `/usr/bin/baloo_file_extractor` | `baloo_file`, `baloo_file_extr` | no |
| plocate | `/usr/sbin/updatedb.plocate` (the timer runs this path, S2-03) | `updatedb.plocat` | no (universe) |
| ClamAV | `/usr/bin/clamscan`, `/usr/sbin/clamd`, `/usr/bin/freshclam` | `clamscan`, `clamd`, `freshclam` | no |
| borg | `/usr/bin/borg` (script) | `borg` | no |
| rsync / rclone | `/usr/bin/rsync`; `/usr/bin/rclone` | `rsync`; `rclone` | rsync yes; rclone no |
| 7-Zip | `/usr/bin/7z` (package `7zip`) | `7z` | no |
| tar / xz | `/usr/bin/tar`; `/usr/bin/xz` | `tar`; `xz` | yes |
| HandBrakeCLI / ffmpeg | `/usr/bin/HandBrakeCLI`; `/usr/bin/ffmpeg` | `HandBrakeCLI`; `ffmpeg` | no |
| python3 | `/usr/bin/python3`, `/usr/bin/python3.12` | `python3` or `python3.12` | yes |
| make / gcc / cc1 | `/usr/bin/make`; `/usr/bin/gcc-13`; `/usr/libexec/gcc/x86_64-linux-gnu/13/cc1` | `make`; `gcc` or `gcc-13`; `cc1` | no |
| DKMS | `/usr/sbin/dkms` (bash script) | `dkms` | no |
| GNOME Shell | `/usr/bin/gnome-shell` | `gnome-shell` | yes |
| Xorg / Xwayland | `/usr/lib/xorg/Xorg`; `/usr/bin/Xwayland` | `Xorg`; `Xwayland` | yes |
| PipeWire | `/usr/bin/pipewire`, `/usr/bin/pipewire-pulse`, `/usr/bin/wireplumber` | `pipewire`, `pipewire-pulse`, `wireplumber` | yes |
| systemd | `/usr/bin/systemd` | `systemd` | yes |
| D-Bus | `/usr/bin/dbus-daemon`; `/usr/bin/dbus-broker`, `/usr/bin/dbus-broker-launch` | `dbus-daemon`; `dbus-broker`, `dbus-broker-lau` | dbus-daemon yes; dbus-broker no |

- **Coverage.** T8 — covers the executable names and packaging status (Ubuntu 24.04, with 26.04 for LocalSearch and gamescope) of every T8 program except Spotify, Slack, Discord, Element, VS Code, Chrome, Zoom, Steam helpers (S2-24, S2-25) and the Kdenlive render process (only the presence of `kdenlive_render` is shown, not that renders run in it). The `comm` column is the reader's derivation. Supports existence only. Does not cover the X11/Wayland share.
- **One observation?** Not an observation.

### S2-13 — UL, PCMark 10 Technical Guide (updated April 11, 2018)

- **Citation.** UL (Futuremark), *PCMark 10 Technical Guide*, "This guide updated April 11, 2018", 81 pages.
- **Copy read.** https://s3.amazonaws.com/download-aws.futuremark.com/PCMark_10_Technical_Guide.pdf (200, application/pdf, 1,897,347 bytes), accessed 2026-10-01, SHA-256 84938b9fb8d05516086c2b14ed03359950f9999fef29355f07a219d13d0dac32. Local `sources/S2-13/PCMark_10_Technical_Guide.pdf`, text `pcm10.txt`. No later edition was found from the product page (row 19).
- **Passages.** Page 2 (`pcm10.txt:22`); page 6 running times (`:129–152`, footnote `:158`); page 17 (`:451–483`); page 18 (`:488–509`); page 27 App Start-up (`:687–720`); page 29 Web Browsing (`:740–754`); page 34 Video Conferencing (`:906–942`); page 40 Writing (`:1076–1101`); page 49 Photo Editing (`:1308–1327`); page 55 Video Editing (`:1478–1501`):

`S2-13/pcm10.txt:22`
```text
This guide updated April 11, 2018 
```
`S2-13/pcm10.txt:129–152`
```text
 
How does PCMark 10 compare with PCMark 8? 
Benchmark comparison 
The first release of PCMark 10 focuses on benchmarking system performance 
with the PCMark 10, PCMark 10 Express and PCMark 10 Extended benchmarks.  
Further benchmark tests are in development and will be released as updates. 
These tests include a dedicated Storage benchmark that improves on the 
PCMark 8 test, an updated and improved Applications benchmark, and a new 
Battery Life test. 
Running time comparison 
PCMark 10 takes less time than PCMark 8. In fact, the main PCMark 10 
benchmark takes less than half the time of the equivalent test in PCMark 8.1 
PCMark 8 Creative PCMark 10 
Conventional: 56 minutes 
Accelerated: 56 minutes 26 minutes 
 
PCMark 8 Work PCMark 10 Express 
Conventional:  34 minutes 
Accelerated: 30 minutes 18 minutes 
 
PCMark 8 Home PCMark 10 Extended 
Conventional: 34 minutes 
Accelerated: 30 minutes 30 minutes 
 
```
`S2-13/pcm10.txt:158`
```text
1  Average running times based on running each benchmark on 20 different desktop and notebook PC configurations. 
```
`S2-13/pcm10.txt:451–483`
```text
Benchmarks, test  groups, 
and workloads 
PCMark 10 uses a modular approach to build relevant tests around common 
end-user scenarios. There are three levels to this approach: benchmarks, test 
groups, and workloads. 
Benchmarks 
Benchmarks are the top-level starting point in PCMark 10. A benchmark is a 
test designed to reflect the performance requirements of a defined user group.  
There are three benchmarks in the current version of PCMark 10.  
 PCMark 10 benchmark – the complete benchmark for the modern office 
 PCMark 10 Express - a shorter test focused on basic work tasks 
 PCMark 10 Extended - a longer test covering a wider range of activities 
Test groups 
Each benchmark contains a number of test groups. A test group is a collection 
of workloads that share a common theme or purpose. There are four test 
groups in PCMark 10. 
 Essentials Productivity 
Digital 
Content 
Creation 
Gaming 
PCMark 10 ● ● ● ✕ 
PCMark 10 
Express 
● ● ✕ ✕ 
PCMark 10 
Extended 
● ● ● ● 
 
Workloads 
Workloads are the low-level unit in PCMark 10. A workload is a test designed 
around a specific activity, task, or application. For example, the Web Browsing 
workload is designed to test performance while engaging in a number of 
```
`S2-13/pcm10.txt:488–509`
```text
PCMark 10 benchmark 
The PCMark 10 benchmark contains tests that cover the wide variety of work 
encountered in a modern office from everyday essentials and productivity 
applications to demanding work with digital media content. It is the ideal test 
for organizations that are evaluating PCs for a range of performance needs. 
Benchmark  Test Groups  Workloads 
 
PCMark 10 
benchmark
Essentials
App Start-up
Web Browsing
Video Conferencing
Productivity
Writing
Spreadsheets
Digital Content 
Creation (DCC)
Photo Editing
Video Editing
Rendering and 
Visualization
```
`S2-13/pcm10.txt:687–720`
```text
App Start-up 
It is frustrating when the applications you use every day are slow to start.  
The App Start-up workload measures hardware performance when launching 
a number of real applications chosen to represent the types of app that 
people use day in, day out. The apps were chosen to cover a range of 
categories – web browser, test editor, image editor - and a spectrum of 
complexity – from small, lightweight apps to complex apps with lots of DLLs to 
load. 
 Chromium web browser 
 Firefox web browser 
 LibreOffice Writer word processing program 
 GIMP image manipulation program 
The applications are included in the PCMark 10 installation package. 
Implementation 
The test has three parts: initialization, warm start, and cold start. 
For the initialization part, all the applications are started once then closed. 
For each application in the warm start part of the test: 
1. Start the application. 
2. Measure the time taken until the application is responsive.  
3. Close the application. 
4. Repeat from step 1 five times. 
5. The result is the geomean of the five runs.  
For each application in the cold start part of the test: 
1. Flush the system cache. 
2. Start the application. 
3. Measure the time taken until the application is responsive.  
4. Close the application. 
5. Repeat from step 1 five times. 
6. The result is the geomean of the five runs.  
Scoring 
 
𝐴𝑝𝑝 𝑆𝑡𝑎𝑟𝑡-𝑢𝑝 𝑠𝑐𝑜𝑟𝑒 = 𝐾 ∗ 1
𝑔𝑒𝑜𝑚𝑒𝑎𝑛(𝑅1, 𝑅2, 𝑅3, 𝑅4, 𝑅5, 𝑅6, 𝑅7, 𝑅8) 
 
```
`S2-13/pcm10.txt:740–754`
```text
Web Browsing 
This test simulates high-level use cases where the user browses common 
websites with a web browser application. The test uses the following website 
archetypes and use cases: social media, online shopping, map, video, and 
static web page. 
Implementation 
The Web Browsing test utilizes two browsers: Firefox and Google Chromium. 
Any other browsers possibly installed in the system will not affect the 
benchmark.  
The content is served with a local lightweight web server that is embedded 
into the benchmark. The content is custom made for the benchmark and 
represents common web sites. 
The web pages are shown using both browsers, except the video page that is 
only run on Chromium. All the pages are run 2 times in both browsers. 
Workloads 
```
`S2-13/pcm10.txt:906–942`
```text
Video Conferencing 
This test models use cases of video conferencing applications. The test uses 
two scenarios: a private call and a group call. 
Implementation 
The Video Conferencing test uses Windows Media Foundation for video 
playback and encoding. Face detection is implemented using library OpenCV 
(http://opencv.org).  
The Video Conferencing test supports OpenCL. The benchmark application 
selects a preferred OpenCL device to use. 
Face detection is made by using cascade classifier 
haarcascade_frontalface_alt.xml.  
Parameters for one-to-one video conferencing: scale factor 1.1, min neighbors 
10, min size 110x110 and max size 300x300. 
Parameters for group video conferencing: scale factor 1.05, min neighbors 5, 
min size 110x110 and max size 300x300. 
 Part 1: one-to-one video conferencing with basic quality video 
 Encode: 720p, 30 FPS, H.264 video, bitrate 14380 kb/s  
 Playback: 720p, 30 FPS, H.264 video, bitrate 11773 kb/s 
 Two video streams (a local and a remote one) 
 Both streams are displayed on screen downscaled to a fixed resolution 
window. 
 Face detection performed on the local stream 
 Stage 1 - CPU: 
 Code path: x86/x64 
 Runtime: 10s 
 Stage 1 - OpenCL: 
 Condition to run: a suitable OpenCL device must be available 
 Code path: OpenCL 
 Runtime: 10s 
Part 2: group video conferencing with high quality outgoing video 
 Encode: 1080p, 30 FPS, H.264 video, bitrate 12731 kb/s 
 Playbacks: 720p, 30 FPS, H.264 video, bitrate 10152 - 12251 kb/s 
 Four streams (a local and three remote ones) 
 All streams are displayed on screen downscaled to a fixed resolution 
window. 
 Face detection performed on the local stream 
 Stage 2 - CPU: 
```
`S2-13/pcm10.txt:1076–1101`
```text
Writing 
The Writing test models common use cases with text processing applications. 
Implementation  
The test uses LibreOffice Writer application and is implemented using AutoIt3 
scripts. 
In the copy and cut tests, the operation is repeated ten times to reduce 
random error. The secondary scores described in the Workload sub-chapter 
are then based on the geometric mean of the ten repeats. 
Workloads 
The Writing test simulates the work with documents. The workloads performs 
the following tasks: 
1. Load Document 1, display in a window 
2. Load Document 2, display in a window 
3. Copy a large part of Document 1 and paste into Document 2 
4. Save As with Document 2 
5. Resize Document 2 window  
6. Cut and paste parts of Document 2 around within the document 
7. Save Document 2 
8. Type some text in Document 2 
9. Save Document 2 
10. Insert some pictures from a local drive in Document 2 
11. Save Document 2 
The workloads measure the time it takes to load the documents, save the file, 
add pictures, and edit the document.  
𝐿𝑜𝑎𝑑 𝑑𝑜𝑐𝑢𝑚𝑒𝑛𝑡 = 𝑔𝑒𝑜𝑚𝑒𝑎𝑛(𝑀1, 𝑀2 ) 
Where: 
```
`S2-13/pcm10.txt:1308–1327`
```text
 
Photo Editing 
The Photo Editing test models use cases with photo editing application.  
Implementation 
The Photo Editing test uses the ImageMagick library. The test uses binaries 
built by Futuremark. 
The Photo Editing test supports OpenCL. The benchmark application selects a 
preferred OpenCL device for the ImageMagick library to use. 
 Camera   File size Resolution 
Interactive RAW Fujifilm X-E1 24.9 MB 4952 × 3288 
Batch 1 RAW Canon EOS 5D 15.8 MB 4386 × 2920 
Batch 2 RAW Nikon D600 20.5 MB 6034 × 4028 
Batch 3 RAW Nikon D800 72.2 MB 7378 × 4924 
Batch 4 RAW Canon EOS 5D 13.5 MB 4386 × 2920 
Batch 5 RAW Olympus E-PL7 14.5 MB 4640 × 3472 
Batch 6 RAW Sony ILCE-7 23.8 MB 6024 × 4024 
Batch 7 JPG Nikon D3100 6.9 MB 4608 × 3072 
Batch 8 JPG Nikon D3 5.5 MB 4256 × 2832 
Output PNG  27.8 MB 4952 × 3288 
Output JPEG  7.2–8.9 MB 4952 × 3288 
```
`S2-13/pcm10.txt:1478–1501`
```text
 
Video Editing test 
The Video Editing test use cases capture some common uses of video editing 
applications. 
Implementation 
The Video Editing test uses parts from PCMark 8 Video Editing and Media To 
Go tests. 
 
Windows Media Foundation is used with its built-in codecs to transcode video. 
Hardware acceleration is allowed to be used if the system supports it and has 
the necessary Media Foundation setup done. 
 
The Video Editing test uses FFmpeg on the sharpening and deshaking parts. 
The test uses pre-built FFmpeg binaries. 
 
The Video editing test supports OpenCL. The benchmark application selects a 
preferred OpenCL device to use. 
 
Part 1: on the go  
Stage 1: Fast downscaling 
 Code path: x86/x64 
 Uses Media Foundation Fast transcode feature to transcode video files to a 
format suitable for mobile use 
 Code path: x86/x64 and whatever is the implementation with Media 
```
- **Coverage.** T7 — covers PCMark 10's benchmarks, test groups and workloads, the applications in each (Chromium, Firefox, LibreOffice Writer and Calc, GIMP, ImageMagick, FFmpeg, Windows Media Foundation, OpenCV), the order of steps inside workloads (App Start-up: initialization, warm start, cold start, five repeats each; Writing: eleven numbered steps), input sizes (photo set with file sizes and resolutions; video-conference encode/playback bitrates and resolutions; 10 s stage runtimes), and benchmark durations (26, 18 and 30 min average over 20 PCs, footnote 1). Concurrency: inside Video Conferencing, several streams are encoded, played back and face-detected at once (two streams in the private call, four in the group call); the guide defines no job running in the background of another application. Backup, archive, malware scan, compile, game download, ML training: none defined. Platform: Windows (the workloads use Windows Media Foundation and DLLs). Supports existence (a benchmark definition), not user behaviour.
- **One observation?** The running-time comparison is one measurement set: "Average running times based on running each benchmark on 20 different desktop and notebook PC configurations"; machines not named. The rest is a definition.

### S2-14 — UL Procyon benchmark pages (Office Productivity 1.6.1449, Photo Editing 1.3.443, Video Editing 1.5.440, AI Text Generation)

- **Citation.** UL Solutions, *Procyon® Office Productivity Benchmark* (latest version 1.6.1449, Sep 18, 2026), *Procyon Photo Editing Benchmark* (1.3.443, Aug 17, 2026), *Procyon Video Editing Benchmark* (1.5.440, Aug 17, 2026), *Procyon AI Text Generation Benchmark* product pages; support article *Overview of UL Procyon Office Productivity Benchmark* (44002262462).
- **Copy read.** https://benchmarks.ul.com/procyon/office-productivity-benchmark (SHA-256 7c32e448269cdc984b23cca47103721f87325c74145eb2aa2ade2da2274412cd), .../photo-editing-benchmark (233ce416f84211b7f7ef5c23192d3e0647bf5aa9baa084300ee974d85b18ca2f), .../video-editing-benchmark (8cd64fc23bcfbc04af0eb93f08f0739c1c2862e4ebe79f15b963acf83e937cc0), .../ai-text-generation-benchmark (402408d649e4ae30b672de4517e91a57d207bef55be3a8f39e18df7a0cd61dba); https://support.benchmarks.ul.com/en/support/solutions/articles/44002262462-overview-of-ul-procyon-office-productivity-benchmark (a68ee878a52c50f6de3aab41c3e721da19cd4fbfa6b311861c82c808d50537f2). Accessed 2026-10-01. Local `sources/S2-14/` (text conversions `*.txt`).
- **Passages.**

`S2-14/procyon-office-productivity-benchmark.txt:103`
```text
The Office Productivity Benchmark is designed around common tasks and usage patterns from a typical day at the office. The benchmark performs tasks with Excel sheets, PowerPoint presentations, Word documents and Outlook emails all opened at the same time. These applications are left running in the background as the focus moves from one task to another. For example, copying charts from Excel and adding it to a PowerPoint slide or comparing and moving content between Word documents.
```
`S2-14/procyon-office-productivity-benchmark.txt:106–113`
```text
Word
The Word test features common tasks such as loading and saving, cutting, copying, pasting and editing content and images, finding and replacing text, inserting graphs from Excel, and comparing documents.
Excel
The Excel test features typical spreadsheet tasks like loading and saving, auto-calculation, inserting data, copy and paste, sorting, using a pivot table, exporting to CSV and PDF, and using common formulas.
PowerPoint
The PowerPoint test loads a document, adds images, copies images and text, adds and previews animations, merges content from other files, saves the file, and exports to PDF and video.
Outlook
The Outlook test includes tasks such as creating emails, moving emails, searching for text within an email, saving attachments, making appointments, and backing up folders.
```
`S2-14/procyon-office-productivity-benchmark.txt:162`
```text
Latest version 1.6.1449 | Sep 18, 2026
```
`S2-14/guide-44002262462-overview-of-ul-procyon-office-productivity-benchmark.txt:202`
```text
The Office Productivity Benchmark is designed around common tasks from a typical day at the office. The benchmark opens Excel sheets, PowerPoint presentations, Word documents and Outlook emails. These applications are running simultaneously as the focus moves from one task to another. For example, the benchmark copies a chart from Excel and adds it to a PowerPoint slide. It takes text from one Word document and adds it to another.  
```
`S2-14/procyon-photo-editing-benchmark.txt:89`
```text
The Procyon photo editing benchmark starts by importing Digital Negative (DNG) image files into Adobe Lightroom Classic and applying various presets. Some images are cropped, straightened and modified. In the second part of the test, multiple edits and layer effects are applied to a photograph in Adobe Photoshop. The benchmark score is a measure of how quickly the PC performs these tasks.
```
`S2-14/procyon-video-editing-benchmark.txt:83–84`
```text
Exporting video files from Premiere Pro is dead time to a creator. Even short videos can take several minutes to export. Longer sequences with layers, color grading and complex effects may take an hour or longer. A faster creator PC takes less time to export video files, giving more time back to the creator.
The benchmark starts by importing two video project files. The project timelines include various edits, adjustments and effects. The second project uses several GPU-accelerated effects. Each video project is exported in Full HD encoded with H.264 and again in 4K UHD encoded with HEVC (H.265). The benchmark score is based on the time taken to export all four videos.
```
`S2-14/procyon-ai-text-generation-benchmark.txt:98–100`
```text
With the Procyon AI Text Generation Benchmark, you can measure the performance of dedicated AI processing hardware and verify inference engine implementation quality with tests based on a heavy AI image generation workload.
Designed for Professionals
We created our Procyon AI Inference Benchmarks for engineering teams who need independent, standardized tools for assessing the general AI performance of inference engine implementations and dedicated hardware.
```
- **Coverage.** T7 — covers Procyon's scenarios and applications: Office Productivity runs Word, Excel, PowerPoint and Outlook "running simultaneously as the focus moves from one task to another" (concurrent open applications, one in focus); the Outlook test includes "backing up folders" (an in-application backup operation) and PowerPoint exports to video; Photo Editing runs Lightroom Classic then Photoshop; Video Editing exports two Premiere Pro projects at Full HD H.264 and 4K HEVC; the AI benchmarks measure inference. No order of workloads, input sizes or durations are given on these pages; no archive, malware-scan, compile, game-download or ML-training workload. Platform: Windows (and macOS for Office). Supports existence only.
- **One observation?** Not an observation; versions named.

### S2-15 — BAPCo SYSmark 30 white paper v1.2; SYSmark 25 and SYSmark 2018 release announcements

- **Citation.** BAPCo, *SYSmark® 30 — An Overview of SYSmark 30* (white paper, revision 1.2; © 2022), 40 pages; BAPCo, *BAPCo® Releases SYSmark® 25 …* (news, July 13, 2020); BAPCo, *BAPCo® RELEASES SYSmark® 2018 …* (news).
- **Copy read.** White paper: https://bapco.com/wp-content/uploads/2025/04/bapco-sysmark30-whitepaper-v1.2.pdf via the Wayback Machine capture https://web.archive.org/web/20251031005630id_/… (the direct URL returned 403), accessed 2026-10-01, SHA-256 4111c36ece1ff85f8c30de3cd0520abc3ebe96c4b91d603a296e4109f9dd7166; text `sm30.txt`. SYSmark 25 release: Wayback capture 20260207072827 of https://bapco.com/bapco-releases-sysmark-25/ (`wb-bapco-releases-sysmark-25.html`). SYSmark 2018 release: Wayback capture 20260122032828 of https://bapco.com/bapco-releases-sysmark-2018-the-latest-version-of-the-premier-pc-performance-metric-featuring-new-productivity-creativity-and-responsiveness-scenarios/ (`wb-sm2018-release.html`). Local `sources/S2-15/`. The SYSmark 25 white paper 1.1 and user guide 1.9 and any SYSmark 2018 white paper could not be read (rows 22–23).
- **Passages.** SYSmark 30 white paper: revision history (page 1, `sm30.txt:16–19`); §2.2 scenarios (pages 10–11, `:263–274`, `:289–293`); §2.3 applications (pages 12–13, `:326–330`, `:337–347`); §2.6 workload descriptions (page 18, `:488–509`); §2.8 measurement (page 20, `:562–568`):

`S2-15/sm30.txt:16–19`
```text
 Revision History:  
1.0 Initial release. 
1.1 Updated minimum requirements.  
1.2 Updated Individual results for sub scenarios are valid in scores section page 14.  
```
`S2-15/sm30.txt:263–274`
```text
Office applications  
  
The Office Applications scenario models using common Microsoft Office 
applications such as MS, Word, MS Excel, and MS PowerPoint, to accomplish tasks 
such as PDF conversion, mail merge, financial forecasting and presentation creation. 
MS Outlook is launche d and remains open throughout the scenario for ambient 
load.  
General Productivity  
  
The General Productivity scenario models productivity tasks such as application 
installation, working with OCR documents, creating and unpacking zip archives, and 
web browsing.  
```
`S2-15/sm30.txt:289–293`
```text
The Advanced Content Creation scenario includes a multitasking workload. A video 
encode is started in Adobe Premiere and sent to the background while Adobe 
Photoshop is launched and used to manipulate photos in the foreground. Due to 
the way operating systems handle multitasking events, slight run to run variation 
may be present in the Advanced Content Creation scenario score.  
```
`S2-15/sm30.txt:326–330`
```text
Office Applications  
• Microsoft® Excel® 2021 Professional Plus VL  
• Microsoft® Outlook® 2021 Professional Plus VL  
• Microsoft® PowerPoint® 2021 Professional Plus VL  
• Microsoft® Word® 2021 Professional Plus VL  
```
`S2-15/sm30.txt:337–347`
```text
General Productivity  
• Adobe® Acrobat® Pro DC  
• Audacity (v 2.3.2) (for app install)  
• Corel WinZip 26.0  
• Google Chrome (v 106.0.5249.103)  
Photo Editing  
• Adobe® Lightroom® Classic (version 11)  
• Adobe® Photoshop® CC (version 23)  
Advanced Content Creation  
• Adobe® Photoshop® CC (version 23)  
• Adobe® Premiere® CC (version 22)  
```
`S2-15/sm30.txt:488–509`
```text
2.6 Scenario Workload Descriptions  
  
The scenario workloads created at the workload development sessions for SYSmark 
30 are described below:  
  
Office Applications  
The Office Applications scenario models office environment like usage including 
word processing (mail merge, document comparison, and PDF conversion), 
spreadsheet data manipulation (data modeling, financial forecasting), presentation 
editing.  
General Productivity  
The General Productivity scenario models OCR of documents, web browsing, 
application installation, and archiving and unpacking a mixed file data set.  
Photo Editing  
The Photo Editing scenario models editing digital photos (applying filters and 
creating HDR photos), cataloging digital photos (organizing catalog, use of facial 
detection to group people).  
Advanced Content Creation  
The Advanced Content Creation scenario encodes video with a CPU render and 
GPU accelerated workload for SUTs configured with a supported accelerated GPU. 
A multitasking workload switches between photo editing and video editing 
workloads.   
```
`S2-15/sm30.txt:562–568`
```text
The fundamental performance unit upon which the SYSmark 30 Performance Rating 
is based is response time .  Response time is defined as the time it takes the 
computer to complete a task that has been initiated by the automated script.  A 
task can be initiated by a mouse click or a keystroke.  The duration of each task is 
measured by the framework.  Examples o f tasks include launching an application, 
finding text in a document, copying a file, encoding a video, and performing an 
image manipulation.  
```

SYSmark 25 release (`wb-bapco-releases-sysmark-25.txt:54`) and SYSmark 2018 release (`wb-sm2018-release.txt:66`, `:69`):

`S2-15/wb-bapco-releases-sysmark-25.txt:54`
```text
The new Productivity Scenario has updated workloads and applications geared towards office centric user activities. The new Creativity Scenario features updated workloads and applications geared toward media-centric user activities. The new Responsiveness Scenario models ‘pain points’ in the user experience. These common activities that include: application launches, file launches, web browsing with multiple tabs, multi-tasking, and background application installation.
```
`S2-15/wb-sm2018-release.txt:66`
```text
 reflects usage patterns of business users in the areas of Office Productivity, Creativity and Responsiveness. The new Productivity Scenario has updated workloads and applications geared towards office centric user activities. The new Creativity Scenario which has updated workloads and applications geared toward media centric user activities. In addition, the new Responsiveness Scenario models ‘pain points’ in the user experience when performing common activities that include: application launches, file launches, web browsing with multiple tabs, multi-tasking and background application installation.
```
`S2-15/wb-sm2018-release.txt:69`
```text
 features new and updated versions of, among others; Microsoft Office 2016, Google Chrome & the Adobe Creative Cloud.
```
- **Coverage.** T7 — covers SYSmark 30's four scenarios, their applications and versions, and two concurrency definitions: Outlook "remains open throughout the scenario for ambient load" in Office Applications, and in Advanced Content Creation "A video encode is started in Adobe Premiere and sent to the background while Adobe Photoshop is launched and used to manipulate photos in the foreground"; General Productivity defines "creating and unpacking zip archives" (WinZip 26.0) and application installation (Audacity). SYSmark 25 and SYSmark 2018 scenarios (Productivity, Creativity, Responsiveness) with "multi-tasking, and background application installation" in Responsiveness; their applications and orders are not covered (white papers not read). Not covered: workload order within a scenario, input sizes, per-scenario durations; no backup, malware-scan, compile, game-download or ML-training workload in SYSmark 30's text. Platform Windows 10/11. Supports existence only (a definition).
- **One observation?** Not an observation (definitions); the calibration system is named (Lenovo ThinkCentre M720q, Core i5 11400T) but no measured values are quoted here.

### S2-16 — Chromium 154.0.8037.92: process model, renderer process limit, spare renderer, thread names

- **Citation.** The Chromium Authors, Chromium tag 154.0.8037.92 (current Linux stable on 2026-10-01 per chromiumdash): `docs/process_model_and_site_isolation.md`; `content/browser/renderer_host/render_process_host_impl.cc`; `content/browser/renderer_host/spare_render_process_host_manager_impl.cc`; `content/common/features.cc`; `content/public/common/content_features.cc`; `base/threading/platform_thread_linux.cc`; `third_party/blink/renderer/modules/peerconnection/peer_connection_dependency_factory.cc`; `media/audio/audio_output_device.cc`; `media/audio/audio_input_device.cc`; `media/audio/audio_thread_impl.cc`.
- **Copy read.** `https://raw.githubusercontent.com/chromium/chromium/154.0.8037.92/<path>` (chromiumdash gives chromium hash 334b65d254ccc35df4fca82706d1753227b01039), accessed 2026-10-01. Local `sources/S2-16/<path with / → _>`. SHA-256: docs 5a371fa56628822f38946d32ef5ce291e07ff74c1fb5a53b1eaac0249fe41bab; render_process_host_impl.cc 6f276e9ff90c5b6aa0412c1427ef38251898f58d0f9855bba7facedbba396592; spare_render_process_host_manager_impl.cc 82909fbbf2f44ee0b76ab3d815b85d27308bc4dea10e2b084353e283b489fa5e; content/common/features.cc fe833ddd66a7f804c430b04654fb50a79d54b98f8e0d354c9e069d5289da5bdc; content_features.cc 9b93fe64843ecf819202fa6de9833597203b3f53f6572c144b76f247424e6c44; platform_thread_linux.cc f1cbba5b3d7edbe2e3561d558bcf18e7af5c0ebe1cc38335e20381f5d2dd918d; peer_connection_dependency_factory.cc d8a78b65cfe01413926408722241e7615c92bc5e1cf62660337c98d65a30a90e; audio_output_device.cc 4c347f3a792be0de30d62154709b510d255d61b410a7387aa87b5765f25ba3d5; audio_input_device.cc 033632e217122d560675b945a2b7cb5be0ee45723eddf34d745082fad39dcc7d; audio_thread_impl.cc db2fc4dececb6a346578b205004c3ead7148903c010f480ec54df9c6dabcd7f6.
- **Passages — process model.** docs `:141–150`, `:322–331`, `:476–479`:

`S2-16/docs_process_model_and_site_isolation.md:141–150`
```text
### Full Site Isolation (site-per-process)

_Used on: Desktop platforms (Windows, Mac, Linux, ChromeOS)._

In (one-)site-per-process mode, each process is locked to documents from a
single site. Sites are defined as scheme plus eTLD+1, since different origins
within a given site may have synchronous access to each other if they each
modify their document.domain. This mode provides all sites protection against
compromised renderers and Spectre-like attacks, without breaking backwards
compatibility.
```
`S2-16/docs_process_model_and_site_isolation.md:322–331`
```text
* **Soft Process Limit**: On desktop platforms, Chromium sets a "soft" process
    limit based on the memory available on a given client. While this can be
    exceeded (e.g., if Site Isolation is enabled and the user has more open
    sites than the limit), Chromium makes an attempt to start randomly reusing
    same-site processes when over this limit. For example, if the limit is 100
    processes and the user has 50 open tabs to `example.com` and 50 open tabs to
    `example.org`, then a new `example.com` tab will share a process with a
    random existing `example.com` tab, while a `chromium.org` tab will create a
    101st process. Note that Chromium on Android does not set this soft process
    limit, and instead relies on the OS to discard processes.
```
`S2-16/docs_process_model_and_site_isolation.md:476–479`
```text
* **Spare Process**: Chromium often creates a spare RenderProcessHost with a
    live but unlocked renderer process, which is used the next time a renderer
    process is needed. This avoids the need to wait for a new process to
    start.
```

- **Passages — process limit.** `render_process_host_impl.cc:1480–1492`, `:1531–1575`, `:5262–5279`:

`S2-16/content_browser_renderer_host_render_process_host_impl.cc:1480–1492`
```text

#if !BUILDFLAG(IS_ANDROID)
// static
size_t RenderProcessHostImpl::GetPlatformMaxRendererProcessCount() {
  // Set the limit to half of the system limit to leave room for other programs.
  size_t limit = GetPlatformProcessLimit() / 2;

  // If the system limit is unavailable, use a fallback value instead.
  if (limit == kUnknownPlatformProcessLimit) {
    static constexpr size_t kMaxRendererProcessCount = 82;
    limit = kMaxRendererProcessCount;
  }
  return limit;
```
`S2-16/content_browser_renderer_host_render_process_host_impl.cc:1531–1575`
```text
#else

  // On other platforms, calculate the maximum number of renderer process hosts
  // according to the amount of installed memory as reported by the OS, along
  // with some hard-coded limits. The calculation assumes that the renderers
  // will use up to half of the installed RAM and assumes that each WebContents
  // uses |kEstimatedWebContentsMemoryUsage| MB. If this assumption changes, the
  // ThirtyFourTabs test needs to be adjusted to match the expected number of
  // processes.
  //
  // Using the above assumptions, with the given amounts of installed memory
  // below on a 64-bit CPU, the maximum renderer count based on available RAM
  // alone will be as follows:
  //
  //   128 MB -> 0
  //   512 MB -> 3
  //  1024 MB -> 6
  //  4096 MB -> 24
  // 16384 MB -> 96
  //
  // Then the calculated value will be clamped by |kMinRendererProcessCount| and
  // GetPlatformMaxRendererProcessCount().

  static size_t max_count = 0;
  if (!max_count) {
    static constexpr size_t kEstimatedWebContentsMemoryUsage =
#if defined(ARCH_CPU_64_BITS)
        85;  // In MB
#else
        60;  // In MB
#endif
    max_count = base::SysInfo::AmountOfTotalPhysicalMemory().InMiB() / 2;
    max_count /= kEstimatedWebContentsMemoryUsage;

    static constexpr size_t kMinRendererProcessCount = 3;
    static const size_t kMaxRendererProcessCount =
        RenderProcessHostImpl::GetPlatformMaxRendererProcessCount();
    CHECK_LE(kMinRendererProcessCount, kMaxRendererProcessCount,
             base::NotFatalUntil::M152);

    max_count = std::clamp(max_count, kMinRendererProcessCount,
                           kMaxRendererProcessCount);
    MAYBEVLOG(1) << __func__ << ": Calculated max " << max_count;
  }
  return max_count;
```
`S2-16/content_browser_renderer_host_render_process_host_impl.cc:5262–5279`
```text
// static
bool RenderProcessHost::IsProcessLimitReached() {
  if (run_renderer_in_process())
    return true;

  // NOTE: Sometimes it's necessary to create more render processes than
  //       GetMaxRendererProcessCount(), for instance when we want to create
  //       a renderer process for a browser context that has no existing
  //       renderers. This is OK in moderation, since the
  //       GetMaxRendererProcessCount() is conservative.
  size_t process_count = RenderProcessHostImpl::GetProcessCountForLimit();
  if (process_count >= GetMaxRendererProcessCount()) {
    MAYBEVLOG(4) << __func__
                 << ": process_count >= GetMaxRendererProcessCount() ("
                 << process_count << " >= " << GetMaxRendererProcessCount()
                 << ") - will try to reuse an existing process";
    // The Finch experiment is *only* for users who go over the process limit.
    // This ensures that the experiment only measures the impact on affected
```

- **Passages — spare renderer.** `render_process_host_impl.cc:3547–3573`; `content_features.cc:1158–1161`; `spare_render_process_host_manager_impl.cc:228–236`; `content/common/features.cc:513–521`:

`S2-16/content_browser_renderer_host_render_process_host_impl.cc:3547–3573`
```text
bool RenderProcessHostImpl::IsSpareProcessKeptAtAllTimes() {
  // Spare renderer actually hurts performance on low-memory devices.  See
  // https://crbug.com/843775 for more details.
  //
  // The comparison below is using 1077 rather than 1024 because this helps
  // ensure that devices with exactly 1GB of RAM won't get included because of
  // inaccuracies or off-by-one errors.
  if (base::SysInfo::AmountOfTotalPhysicalMemory() <=
      base::MiB(base::saturated_cast<uint64_t>(
          features::kAndroidSpareRendererMemoryThreshold.Get()))) {
    return false;
  }

  bool android_spare_process_override = base::FeatureList::IsEnabled(
      features::kAndroidWarmUpSpareRendererWithTimeout);
  if (!SiteIsolationPolicy::UseDedicatedProcessesForAllSites() &&
      !android_spare_process_override) {
    return false;
  }

  if (!base::FeatureList::IsEnabled(
          features::kSpareRendererForSitePerProcess) &&
      !android_spare_process_override) {
    return false;
  }

  return true;
```
`S2-16/content_public_common_content_features.cc:1158–1161`
```text
// Controls whether SpareRenderProcessHostManager tries to always have a warm
// spare renderer process around for the most recently requested BrowserContext.
// This feature is only consulted in site-per-process mode.
BASE_FEATURE(kSpareRendererForSitePerProcess, base::FEATURE_ENABLED_BY_DEFAULT);
```
`S2-16/content_browser_renderer_host_spare_render_process_host_manager_impl.cc:228–236`
```text
// Returns the number of spare hosts that should be created. Ensures the field
// trial is not activated on excluded machines.
size_t GetSpareRPHCount() {
  // Exclude machines with less than 4gigs of ram.
  if (base::SysInfo::AmountOfTotalPhysicalMemory() < base::GiB(4)) {
    return 1u;
  }
  return features::kMultipleSpareRPHsCount.Get();
}
```
`S2-16/content_common_features.cc:513–521`
```text
// When enabled, additional spare RPHs will be warmed up when the browser is
// not busy.
BASE_FEATURE(kMultipleSpareRPHs, base::FEATURE_ENABLED_BY_DEFAULT);

BASE_FEATURE_PARAM(size_t,
                   kMultipleSpareRPHsCount,
                   &kMultipleSpareRPHs,
                   "count",
                   1u);
```

- **Passages — thread names (T8, T10).** `platform_thread_linux.cc:210–231`; `content_features.cc:160–167`; `peer_connection_dependency_factory.cc:395–396`; `audio_output_device.cc:433–434`; `audio_input_device.cc:297–298`; `audio_thread_impl.cc:18`:

`S2-16/base_threading_platform_thread_linux.cc:210–231`
```text
void PlatformThreadBase::SetName(const std::string& name) {
  SetNameCommon(name);

  // On linux we can get the thread names to show up in the debugger by setting
  // the process name for the LWP.  We don't want to do this for the main
  // thread because that would rename the process, causing tools like killall
  // to stop working.
  if (PlatformThread::CurrentId().raw() == getpid()) {
    return;
  }

  // http://0pointer.de/blog/projects/name-your-threads.html
  // Set the name for the LWP (which gets truncated to 15 characters).
  // Note that glibc also has a 'pthread_setname_np' api, but it may not be
  // available everywhere and it's only benefit over using prctl directly is
  // that it can set the name of threads other than the current thread.
  int err = prctl(PR_SET_NAME, name.c_str());
  // We expect EPERM failures in sandboxed processes, just ignore those.
  if (err < 0 && errno != EPERM) {
    DPLOG(ERROR) << "prctl(PR_SET_NAME)";
  }
}
```
`S2-16/content_public_common_content_features.cc:160–167`
```text
// Runs the audio service in a separate process.
BASE_FEATURE(kAudioServiceOutOfProcess,
#if BUILDFLAG(IS_WIN) || BUILDFLAG(IS_MAC) || BUILDFLAG(IS_LINUX)
             base::FEATURE_ENABLED_BY_DEFAULT
#else
             base::FEATURE_DISABLED_BY_DEFAULT
#endif
);
```
`S2-16/third_party_blink_renderer_modules_peerconnection_peer_connection_dependency_factory.cc:395–396`
```text
      : chrome_signaling_thread_("WebRTC_Signaling"),
        chrome_worker_thread_("WebRTC_W_and_N") {}
```
`S2-16/media_audio_audio_output_device.cc:433–434`
```text
    audio_thread_ = std::make_unique<AudioDeviceThread>(
        audio_callback_.get(), std::move(socket_handle), "AudioOutputDevice",
```
`S2-16/media_audio_audio_input_device.cc:297–298`
```text
  audio_thread_ = std::make_unique<AudioDeviceThread>(
      audio_callback_.get(), std::move(socket_handle), "AudioInputDevice",
```
`S2-16/media_audio_audio_thread_impl.cc:18`
```text
    : thread_("AudioThread"),
```
- **Coverage.** T3 — covers how Chromium on desktop Linux maps documents to renderer processes: full site isolation (one process per site, site = scheme plus eTLD+1) on desktop; cross-site iframes out of process and placed in an existing same-site process when possible; a soft process limit = installed RAM/2 ÷ 85 MB on 64-bit, clamped between 3 and half the platform process limit (fallback 82), e.g. 96 at 16 GiB per the code comment, beyond which same-site processes are reused at random; one spare renderer kept at all times in site-per-process mode on machines with more than 1077 MB (`kSpareRendererForSitePerProcess` enabled by default; `kMultipleSpareRPHs` count 1). Does not cover any observed renderer count for a set of tabs, nor how many tabs or windows users keep open. Supports existence only. T8 — covers that Chromium names threads with `prctl(PR_SET_NAME)` (truncated to 15) and never renames the main thread, so every Chromium process keeps the executable's `comm`. T10 — covers names of the WebRTC and audio threads of a call in Chromium (`WebRTC_Signaling` → derived `WebRTC_Signalin`, `WebRTC_W_and_N`, `AudioOutputDevice` → `AudioOutputDevi`, `AudioInputDevice` → `AudioInputDevic`, `AudioThread`) and that the audio service runs in a separate process on Linux by default (the derived 15-byte strings are the reader's own). A Google Meet or Jitsi call in Chrome uses these; their population needs observation.
- **One observation?** Not an observation; version named.

### S2-17 — Firefox 157.0: content-process names and process counts

- **Citation.** Mozilla, Firefox tag FIREFOX_157_0_RELEASE (current release 157.0 per product-details): `ipc/glue/ProcessUtils_linux.cpp`, `dom/ipc/ContentChild.cpp`, `modules/libpref/init/all.js`, `modules/libpref/init/StaticPrefList.yaml`, `browser/app/profile/firefox.js`.
- **Copy read.** `https://raw.githubusercontent.com/mozilla-firefox/firefox/FIREFOX_157_0_RELEASE/<path>` (tag → commit fdd757a2e09c9471cddf383e64e631e4ce178499), accessed 2026-10-01. Local `sources/S2-17/`. SHA-256: ProcessUtils_linux.cpp 0ea72a222c7fb2c8a0f22d094954d646885895692f337405219e2adca5a8e95b; ContentChild.cpp 16f524a6e533d92aa9626a468552321c9c05a76ebacf980cdfbcd4ec8aac6ee9; all.js 0c1b5652242b551ceaadb63495408325e63c1fb1c1121563ad1666efb790df53; StaticPrefList.yaml 36a84541af31ce98ccff88e820a034a0fa29fcea1e280b1e0610b8c9b9e22644; firefox.js f4da676c18c2bcebfb27b54432eb17b6f129295df0f4c4a3acc6606890047c2d.
- **Passages.**

`S2-17/ipc_glue_ProcessUtils_linux.cpp:15–17`
```text
void SetThisProcessName(const char* aName) {
  prctl(PR_SET_NAME, (unsigned long)aName, 0uL, 0uL, 0uL);
}
```
`S2-17/dom_ipc_ContentChild.cpp:2750–2780`
```text
  // Update the process name so about:memory's process names are more obvious.
  if (aRemoteType.IsFile()) {
    SetProcessName("file:// Content"_ns, nullptr, &aProfile);
  } else if (aRemoteType.IsExtension()) {
    SetProcessName("WebExtensions"_ns, nullptr, &aProfile);
  } else if (aRemoteType.IsPrivilegedAbout()) {
    SetProcessName("Privileged Content"_ns, nullptr, &aProfile);
  } else if (aRemoteType.IsPrivilegedMozilla()) {
    SetProcessName("Privileged Mozilla"_ns, nullptr, &aProfile);
  } else if (aRemoteType.IsInference()) {
    SetProcessName("Inference"_ns, nullptr, &aProfile);
  } else if (aRemoteType.IsIsolatedWeb()) {
    nsAutoCString site = mRemoteType.StringifyMeta();

    if (aRemoteType.IsWebServiceWorker()) {
      SetProcessName("Isolated Service Worker"_ns, &site, &aProfile);
    }
#ifdef NIGHTLY_BUILD
    else if (aRemoteType.IsWebCoopCoep()) {
      // NOTE: We only distinguish between isolated web sub-types on Nightly
      // builds to avoid confusing users.
      SetProcessName("WebCOOP+COEP Content"_ns, &site, &aProfile);
    }
#endif
    else {
      SetProcessName("Isolated Web Content"_ns, &site, &aProfile);
    }
  } else {
    // else "prealloc" or "web" type -> "Web Content"
    SetProcessName("Web Content"_ns, nullptr, &aProfile);
  }
```
`S2-17/dom_ipc_ContentChild.cpp:859–860`
```text
  // Requires pref flip
  if (aSite && StaticPrefs::fission_processSiteNames()) {
```
`S2-17/dom_ipc_ContentChild.cpp:893`
```text
  mozilla::ipc::SetThisProcessName(mProcessName.get());
```
`S2-17/modules_libpref_init_StaticPrefList.yaml:6774–6777`
```text
- name: fission.processSiteNames
  type: bool
  value: false
  mirror: always
```
`S2-17/modules_libpref_init_all.js:1865–1872`
```text
// Enable multi by default.
#if !defined(MOZ_ASAN) && !defined(MOZ_TSAN)
  pref("dom.ipc.processCount", 8);
#elif defined(FUZZING_SNAPSHOT)
  pref("dom.ipc.processCount", 1);
#else
  pref("dom.ipc.processCount", 4);
#endif
```
`S2-17/modules_libpref_init_all.js:1887–1892`
```text
// Maximum number of isolated content processes per-origin.
#ifdef ANDROID
pref("dom.ipc.processCount.webIsolated", 1);
#else
pref("dom.ipc.processCount.webIsolated", 4);
#endif
```
`S2-17/modules_libpref_init_StaticPrefList.yaml:3685–3693`
```text
- name: dom.ipc.processPrelaunch.fission.number
  type: uint32_t
#ifdef ANDROID
  # Bug 1999950: Prelaunch 1 process on Android due to a performance regression.
  value: 1
#else
  value: 3
#endif
  mirror: always
```
`S2-17/browser_app_profile_firefox.js:2880–2884`
```text
#ifdef FUZZING_SNAPSHOT
pref("dom.ipc.processPrelaunch.enabled", false);
#else
pref("dom.ipc.processPrelaunch.enabled", true);
#endif
```
- **Coverage.** T3 — Firefox comparison: up to 4 isolated content processes per site, 8 for non-isolated web content, 3 prelaunched processes on desktop; no observed counts. Supports existence only. T8 — covers that each Firefox content process renames itself with `prctl(PR_SET_NAME)` to "Isolated Web Content", "Web Content", "WebExtensions", "Privileged Content", "file:// Content", "Isolated Service Worker", "Inference" or "Privileged Mozilla" (site names only with a pref that is off by default); derived 15-byte `comm`: `Isolated Web Co`, `Web Content`, `WebExtensions`, `Privileged Cont`, `file:// Content`, `Isolated Servic`, `Inference`, `Privileged Mozi` (reader's own). Thunderbird shares this code base; not checked separately.
- **One observation?** Not an observation; version named.

### S2-18 — Wine 11.0 and Proton 11.0-2c: process and thread naming, how a game is launched

- **Citation.** WineHQ, Wine 11.0: `dlls/ntdll/unix/env.c`, `dlls/ntdll/unix/thread.c`, `loader/preloader.c`; Valve, Proton tag proton-11.0-2c `proton` script and `ValveSoftware/wine` tag proton-wine-11.0-2c `dlls/ntdll/unix/thread.c`.
- **Copy read.** Wine: `https://gitlab.winehq.org/wine/wine/-/raw/wine-11.0/dlls/ntdll/unix/{loader,thread}.c` and sparse clone of `wine-11.0` (commit db11d0fe6a169c457e23d007e20404643d067aa8, 2026-01-13) for `loader/preloader.c` and `dlls/ntdll/unix/env.c`; Proton: `https://raw.githubusercontent.com/ValveSoftware/Proton/proton-11.0-2c/proton`; Proton wine: `https://raw.githubusercontent.com/ValveSoftware/wine/proton-wine-11.0-2c/dlls/ntdll/unix/thread.c`. Accessed 2026-10-01. Local `sources/S2-18/`. SHA-256: wine-11.0 env.c 306a3d532a7e68a60edec7567025c7f83f4dd786a23e0fda3b6f52beb70b9b6e; preloader.c 1fbb69842686631df56da0c43e604447f4fe0113459ea9f2d31c5002c1639d7d; wine-11.0 thread.c a45209adadc2c8bea29b1f3989e682ee5922d2f6d1aae128c30feceb05cb8e2f; wine-11.0 loader.c c693dd960f0e88bba841cdb1691dda38f914ddf1b2f2ecd879e74772726a3e94; proton-wine thread.c 4346e0c41deede71e67a621e556c42db25bf976c90c5b7f9c14f67ac52ad7770; proton-wine loader.c d34f324493ef5d75a80fc4bb8a030071cd4fce4aabc5f92b3e2436102d3abcf4; proton script 787504a79bacf6b303984a9a846cf47463f36599248e8306b26d5faf78267aad.
- **Passages.** `env.c:480–503` (process renamed to the exe), `:531–532`; `preloader.c:1372–1381`, `:1500–1501`; `thread.c:1989–2024` (Windows thread names written to `/proc/<pid>/task/<tid>/comm`); Proton `proton:2055–2085`, `:543–544`:

`S2-18/wine-11.0_dlls_ntdll_unix_env.c:480–503`
```text
/***********************************************************************
 *           set_process_name
 *
 * Change the process name in the ps output.
 */
static void set_process_name( const char *name )
{
    char *p;

#ifdef HAVE_SETPROCTITLE
    setproctitle("-%s", name );
#endif
    if ((p = strrchr( name, '\\' ))) name = p + 1;
    if ((p = strrchr( name, '/' ))) name = p + 1;
#ifdef HAVE_SETPROGNAME
    setprogname( name );
#endif
#ifdef HAVE_PRCTL
#ifndef PR_SET_NAME
# define PR_SET_NAME 15
#endif
    prctl( PR_SET_NAME, name );
#endif
}
```
`S2-18/wine-11.0_dlls_ntdll_unix_env.c:531–532`
```text
    main_argv[--main_argc] = NULL;
    set_process_name( main_argv[0] );
```
`S2-18/wine-11.0_loader_preloader.c:1372–1381`
```text
/* set the process name if supported */
static void set_process_name( int argc, char *argv[] )
{
    int i;
    unsigned int off;
    char *p, *name, *end;

    /* set the process short name */
    for (p = name = argv[1]; *p; p++) if (p[0] == '/' && p[1]) name = p + 1;
    if (wld_prctl( 15 /* PR_SET_NAME */, (long)name ) == -1) return;
```
`S2-18/wine-11.0_loader_preloader.c:1500–1501`
```text
    /* get rid of first argument */
    set_process_name( *pargc, argv );
```
`S2-18/wine-11.0_dlls_ntdll_unix_thread.c:1989–2024`
```text
static void set_native_thread_name( HANDLE handle, const UNICODE_STRING *name )
{
#ifdef linux
    unsigned int status;
    char path[64], nameA[64];
    int unix_pid, unix_tid, len, fd;

    SERVER_START_REQ( get_thread_times )
    {
        req->handle = wine_server_obj_handle( handle );
        status = wine_server_call( req );
        if (status == STATUS_SUCCESS)
        {
            unix_pid = reply->unix_pid;
            unix_tid = reply->unix_tid;
        }
    }
    SERVER_END_REQ;

    if (status != STATUS_SUCCESS || unix_pid == -1 || unix_tid == -1)
        return;

    if (unix_pid != getpid())
    {
        static int once;
        if (!once++) FIXME("cross-process native thread naming not supported\n");
        return;
    }

    len = ntdll_wcstoumbs( name->Buffer, name->Length / sizeof(WCHAR), nameA, sizeof(nameA), FALSE );
    snprintf(path, sizeof(path), "/proc/%u/task/%u/comm", unix_pid, unix_tid);
    if ((fd = open( path, O_WRONLY )) != -1)
    {
        write( fd, nameA, len );
        close( fd );
    }
```
`S2-18/proton-11.0-2c_proton:543–544`
```text
        self.wine_bin = self.bin_dir + "wine"
        self.wineserver_bin = self.bin_dir + "wineserver"
```
`S2-18/proton-11.0-2c_proton:2055–2085`
```text
    def run(self):
        if shutil.which('steam-runtime-launcher-interface-0') is not None:
            adverb = ['steam-runtime-launcher-interface-0', 'proton']
        else:
            adverb = []

        if self.remote_debug_cmd:
            remote_debug_cmd = self.remote_debug_cmd
            if not os.path.isabs(remote_debug_cmd[0]):
                remote_debug_cmd[0] = g_proton.path(remote_debug_cmd[0])
            remote_debug_proc = subprocess.Popen([g_proton.wine_bin] + self.remote_debug_cmd,
                                                 env=self.env, stderr=self.log_file, stdout=self.log_file)
        else:
            remote_debug_proc = None

        # CoD: Black Ops 3 workaround
        if os.environ.get("SteamGameId", 0) in [
                    "311210",   # CoD: Black Ops 3
                    "1985810",  # CoD: Black Ops Cold War
                    "1549250",  # Undecember
                ]:
            argv = [g_proton.wine_bin, "c:\\Program Files (x86)\\Steam\\steam.exe"]
        else:
            if g_proton.host_pe_arch == "x86_64-windows":
                #run with winepreloader directly to avoid restart through start.exe
                self.env["WINELOADERNOEXEC"] = "1"
                argv = [g_proton.lib_dir + "/wine/x86_64-unix/wine-preloader", g_proton.lib_dir + "/wine/x86_64-unix/wine", "c:\\windows\\system32\\steam.exe"]
            else:
                argv = [g_proton.wine_bin, "c:\\windows\\system32\\steam.exe"]

        rc = self.run_proc(adverb + argv + sys.argv[2:] + self.cmdlineappend)
```

`grep -n set_native_thread_name` on the Proton wine thread.c shows the same function at lines 2013, 2604, 2615.
- **Coverage.** T4 — covers how Proton launches a game (Proton's built-in `steam.exe` started through `wine-preloader`/`wine`, which then starts the game exe) and that Wine and Proton turn Windows thread names (SetThreadDescription) into Linux thread `comm`. Does not cover thread counts, which threads are busy, or what runs beside the game. T8 — covers that every Wine process renames itself with `prctl(PR_SET_NAME)` to its Windows executable's basename (so `comm` = first 15 bytes of e.g. `steam.exe` or the game's `.exe`), and the `wineserver` binary. Supports existence only.
- **One observation?** Not an observation; versions named.

### S2-19 — Steam Runtime tools v0.20260925.0 documentation: reaper, pressure-vessel, launcher service

- **Citation.** Valve / Collabora, *steam-runtime-tools* v0.20260925.0: `docs/steam-compat-tool-interface.md`, `pressure-vessel/wrap.1.md`, `docs/container-runtime.md`.
- **Copy read.** `https://gitlab.steamos.cloud/steamrt/steam-runtime-tools/-/raw/v0.20260925.0/<path>`, accessed 2026-10-01. Local `sources/S2-19/`. SHA-256: steam-compat-tool-interface.md 3d1fbf262e39705ab8460ff7b352625c8764d9d1b4b5356152f5f406c54af8ea; wrap.1.md 7f0da8dee8931f0a5c91580115582ffb6e9260b56bc08fcbd085898c2c4bb4cd; container-runtime.md c4b8c587ed3c833219b52ce7d350b256118fb71d6f2f1fd4fb49b146d4025893.
- **Passages.**

`S2-19/docs_steam-compat-tool-interface.md:528–540`
```text
In recent versions of Steam, the game process is wrapped in a `reaper`
process which sets itself as a subreaper using `PR_SET_CHILD_SUBREAPER`
(see [**prctl**(2)][prctl] for details).

Version 1 compat tools are not invoked specially.

Version 2 compat tools are invoked with a `%verb%` in the `commandline`
(if any) replaced by `waitforexitandrun`.

The game is expected to run in the usual way. Conventionally, it does not
double-fork to put itself in the background, but if it does, any background
processes will be reparented to have the subreaper as their parent.

```
`S2-19/pressure-vessel_wrap.1.md:13`
```text
pressure-vessel-wrap - run programs in a bubblewrap container
```
`S2-19/pressure-vessel_wrap.1.md:28`
```text
**pressure-vessel-wrap** runs *COMMAND* in a container, using **bwrap**(1).
```
`S2-19/pressure-vessel_wrap.1.md:1757–1760`
```text
The **pressure-vessel-wrap** process replaces itself with a **bwrap**(1)
process. Fatal signals to the resulting **bwrap**(1) process will result
in `SIGTERM` being received by the **pressure-vessel-wrap** process
that runs *COMMAND* inside the container.
```
`S2-19/docs_container-runtime.md:124–127`
```text
The *Steam Linux Runtime 3.0 - sniper* compatibility tool, app ID 1628350,
will automatically be downloaded to your Steam library as
`steamapps/common/SteamLinuxRuntime_sniper` if a game or a version of
Proton requires it.
```
- **Coverage.** T4 — covers the processes Steam puts around a game: a `reaper` subreaper parent for every game, the `pressure-vessel-wrap` → `bwrap` container for games run in the Steam Linux Runtime (sniper etc.). Does not cover the Steam client's own helpers' behaviour, the overlay, voice chat or downloads. T8 — names `reaper`, `pressure-vessel-wrap` (derived `pressure-vessel`), `bwrap`/`srt-bwrap` (S2-25 lists `srt-bwrap` in the bootstrap), `steam-runtime-launcher-service` (derived `steam-runtime-l`). Supports existence only.
- **One observation?** Not an observation; version named.

### S2-20 — Steam Support, "Managing Steam Downloads & Updates" and "Setting Client Rates"

- **Citation.** Valve, Steam Support FAQ *Managing Steam Downloads & Updates* (71AB-698D-57EB-178C; embedded timestamp 1727216103 = 2024-09-24) and *Setting Client Rates (Limit Download Speed) in Steam* (163C-7C89-406E-2F63; timestamp 1727214116).
- **Copy read.** https://help.steampowered.com/en/faqs/view/71AB-698D-57EB-178C (SHA-256 of the HTML: see end note) and https://help.steampowered.com/en/faqs/view/163C-7C89-406E-2F63, accessed 2026-10-01; the article body is a JSON string in the page, decoded to `steam-faq-*.content.txt`. Local `sources/S2-20/`.
- **Passages.** `steam-faq-71AB-698D-57EB-178C.content.txt`, lines with the per-game settings and the schedule:

`grep -n -E '^Available settings|downloading of other updates while you're playing|Only auto-update games|^Steam will automatically download' S2-20/steam-faq-71AB-698D-57EB-178C.content.txt`
```text
1:Steam will automatically download updates for your games based on the Steam client's download settings. Downloads can also be manually controlled from the Download Manager within your Steam client.
10:Available settings:  [list][*]"Always keep this game updated"  [*]"Only update this game when I launch it" - will temporarily disable game updates  [*]"High Priority - Always auto-update this game before others"  [/list]
11:There's also a per-game setting to allow/prevent the downloading of other updates while you're playing.[/section]    [section id=disable]  [h4]Disabling automatic updates[/h4]If you'd like to stop Steam from automatically updating a game, select "Only update this game when I launch it" from the game's Library page > Properties > Updates.[/section]    [section id=scheduling]  [h4]Scheduling automatic updates[/h4]Your queued downloads can be manually re-ordered from your Download Manager.
13:You can also limit the times during the day when Steam updates your games. From your downloads settings ([i]Steam > Settings > Downloads[/i]) check the [i]Only auto-update games[/i] box and specify the time when Steam should perform auto-updates. For example, selecting '12AM' And '8AM' would mean that Steam will only download auto-updated games between midnight and 8 AM your local time.
```
- **Coverage.** T4 — covers that the Steam client downloads updates automatically, that a per-game setting allows or prevents other downloads while that game is played, and that auto-updates can be confined to a time window; it does not state the default of the gameplay setting or any behaviour on Linux. Supports existence only.
- **One observation?** Not an observation.

### S2-21 — gamescope 3.16.31 source: nested refresh rate, backends, executables and thread names

- **Citation.** Valve, *gamescope* 3.16.31: `src/main.cpp`, `src/Backends/WaylandBackend.cpp`, `src/Backends/SDLBackend.cpp`, `src/vblankmanager.cpp`, `src/meson.build`, `README.md`.
- **Copy read.** `git clone --depth 1 --branch 3.16.31 https://github.com/ValveSoftware/gamescope.git`, commit 6867f509874f9bc52e12d6f4c4596cdf0d5be6b4 (2026-09-27), accessed 2026-10-01. Local `sources/S2-21/gamescope-3.16.31/`. SHA-256: main.cpp 618bc9de81ab1b724b07985cdee14e6a9369fb4fc03057a896efbeac1c42e9cd; WaylandBackend.cpp 31184ad44a1488c3b18cef8fba0c16acf4b8874c845b413371184a464082c65a; SDLBackend.cpp 095847f3ef7c535913a236d69c207d529e96678c040c5f9e729433ce863c6369; vblankmanager.cpp 54aaf2098ea56a9c1a4b7313df3cfab12d7db27dbf9728c651eee35a2411e556; meson.build 2f332dbbc76b80522121492b381c12a695f1c37a641f03ee321db45eb0e53dc7; README.md 5a9130ced7900e30f62fc7a0b033d2e5d9f849e1069704483c3e396652aeff87.
- **Passages.** `README.md:3`, `:9`; `main.cpp:176`, `:299`, `:305`, `:445–453`; `WaylandBackend.cpp:1985–2005` (nested default), `:1690–1716` (follow the output's refresh); `SDLBackend.cpp:228–244`, `:842–856`; `vblankmanager.cpp:75–78`; executables `meson.build:193–194`, `:221`; thread names:

`S2-21/gamescope-3.16.31/README.md:3`
```text
In an embedded session usecase, gamescope does the same thing as steamcompmgr, but with less extra copies and latency:
```
`S2-21/gamescope-3.16.31/README.md:9`
```text
It also runs on top of a regular desktop, the 'nested' usecase steamcompmgr didn't support.
```
`S2-21/gamescope-3.16.31/src/main.cpp:176`
```text
	"  -r, --nested-refresh           game refresh rate (frames per second)\n"
```
`S2-21/gamescope-3.16.31/src/main.cpp:299`
```text
int g_nNestedRefresh = 0;
```
`S2-21/gamescope-3.16.31/src/main.cpp:305`
```text
int g_nOutputRefresh = 0;
```
`S2-21/gamescope-3.16.31/src/main.cpp:445–453`
```text
static enum gamescope::GamescopeBackend auto_select_backend()
{
	if ( getenv( "WAYLAND_DISPLAY" ) != NULL )
		return gamescope::GamescopeBackend::Wayland;
	else if ( getenv( "DISPLAY" ) != NULL )
		return gamescope::GamescopeBackend::SDL;
	else
		return gamescope::GamescopeBackend::DRM;
}
```
`S2-21/gamescope-3.16.31/src/Backends/WaylandBackend.cpp:1985–2005`
```text
    bool CWaylandBackend::Init()
    {
        g_nOutputWidth = g_nPreferredOutputWidth;
        g_nOutputHeight = g_nPreferredOutputHeight;
        g_nOutputRefresh = g_nNestedRefresh;

        // TODO: Dedupe the init of this stuff,
        // maybe move it away from globals for multi-display...
        if ( g_nOutputHeight == 0 )
        {
            if ( g_nOutputWidth != 0 )
            {
                fprintf( stderr, "Cannot specify -W without -H\n" );
                return false;
            }
            g_nOutputHeight = 720;
        }
        if ( g_nOutputWidth == 0 )
            g_nOutputWidth = g_nOutputHeight * 16 / 9;
        if ( g_nOutputRefresh == 0 )
            g_nOutputRefresh = ConvertHztomHz( 60 );
```
`S2-21/gamescope-3.16.31/src/Backends/WaylandBackend.cpp:1690–1716`
```text
    void CWaylandPlane::UpdateVRRRefreshRate()
    {
        if ( m_pParent )
            return;

        if ( !m_pConnector->HostCompositorIsCurrentlyVRR() )
            return;

        if ( m_pOutputs.empty() )
            return;

        int32_t nLargestRefreshRateMhz = 0;
        for ( wl_output *pOutput : m_pOutputs )
        {
            WaylandOutputInfo *pOutputInfo = m_pBackend->GetOutputInfo( pOutput );
            if ( !pOutputInfo )
                continue;

            nLargestRefreshRateMhz = std::max( nLargestRefreshRateMhz, pOutputInfo->nRefresh );
        }

        if ( nLargestRefreshRateMhz && nLargestRefreshRateMhz != g_nOutputRefresh )
        {
            // TODO(strategy): We should pick the largest refresh rate.
            xdg_log.infof( "Changed refresh to: %.3fhz", ConvertmHzToHz( (float) nLargestRefreshRateMhz ) );
            g_nOutputRefresh = nLargestRefreshRateMhz;
        }
```
`S2-21/gamescope-3.16.31/src/Backends/SDLBackend.cpp:228–244`
```text
		g_nOutputWidth = g_nPreferredOutputWidth;
		g_nOutputHeight = g_nPreferredOutputHeight;
		g_nOutputRefresh = g_nNestedRefresh;

		if ( g_nOutputHeight == 0 )
		{
			if ( g_nOutputWidth != 0 )
			{
				fprintf( stderr, "Cannot specify -W without -H\n" );
				return false;
			}
			g_nOutputHeight = 720;
		}
		if ( g_nOutputWidth == 0 )
			g_nOutputWidth = g_nOutputHeight * 16 / 9;
		if ( g_nOutputRefresh == 0 )
			g_nOutputRefresh = gamescope::ConvertHztomHz( 60 );
```
`S2-21/gamescope-3.16.31/src/Backends/SDLBackend.cpp:842–856`
```text
						case SDL_WINDOWEVENT_MOVED:
						case SDL_WINDOWEVENT_SHOWN:
							{
								int display_index = 0;
								SDL_DisplayMode mode = { SDL_PIXELFORMAT_UNKNOWN, 0, 0, 0, 0 };

								display_index = SDL_GetWindowDisplayIndex( m_Connector.GetSDLWindow() );
								if ( SDL_GetDesktopDisplayMode( display_index, &mode ) == 0 )
								{
									g_nOutputRefresh = ConvertHztomHz( mode.refresh_rate );
								}
							}
							break;
						case SDL_WINDOWEVENT_FOCUS_LOST:
							g_nNestedRefresh = g_nNestedUnfocusedRefresh;
```
`S2-21/gamescope-3.16.31/src/vblankmanager.cpp:75–78`
```text
	int CVBlankTimer::GetRefresh() const
	{
		return g_nNestedRefresh ? g_nNestedRefresh : g_nOutputRefresh;
	}
```
`S2-21/gamescope-3.16.31/src/meson.build:193–194`
```text
  executable(
    'gamescope',
```
`S2-21/gamescope-3.16.31/src/meson.build:221`
```text
executable('gamescopereaper', ['Apps/gamescopereaper.cpp', gamescope_core_src], gamescope_version, dependencies: [cap_dep], install:true )
```
`grep -n -E 'pthread_setname_np' S2-21/gamescope-3.16.31/src/main.cpp`
```text
1122:	pthread_setname_np( pthread_self(), "gamescope-xwm" );
```
`grep -n -E 'pthread_setname_np' S2-21/gamescope-3.16.31/src/vblankmanager.cpp`
```text
388:		pthread_setname_np( pthread_self(), "gamescope-vblk" );
```
`grep -n -E 'pthread_setname_np' S2-21/gamescope-3.16.31/src/wlserver.cpp`
```text
2399:	pthread_setname_np( pthread_self(), "gamescope-wl" );
```
`grep -n -E 'pthread_setname_np' S2-21/gamescope-3.16.31/src/steamcompmgr.cpp`
```text
1371:	pthread_setname_np( pthread_self(), "gamescope-vrmon" );
1655:	pthread_setname_np( pthread_self(), "gamescope-stats" );
3700:				pthread_setname_np( pthread_self(), "gamescope-scrsh" );
9431:			pthread_setname_np( pthread_self(), "gamescope-wait" );
9657:				pthread_setname_np( pthread_self(), "gamescope-reap" );
```
`grep -n -E 'pthread_setname_np' S2-21/gamescope-3.16.31/src/rendervulkan.cpp`
```text
1206:	pthread_setname_np( pthread_self(), "gamescope-shdr" );
```
`grep -n -E 'pthread_setname_np' S2-21/gamescope-3.16.31/src/pipewire.cpp`
```text
622:	pthread_setname_np( pthread_self(), "gamescope-pw" );
```
- **Coverage.** T4 — covers the frame cadence of nested gamescope on a desktop: the vblank timer runs at `--nested-refresh` if given, otherwise at the output refresh, which the nested backends initialise to 60 Hz and then set from the desktop display mode (SDL backend, under X11) or from the largest refresh of the outputs the window is on (Wayland backend); unfocused, `--nested-unfocused-refresh` applies. Backend selection: Wayland if `WAYLAND_DISPLAY` is set, SDL if `DISPLAY`, else DRM (the embedded, Steam Deck–style session). Does not cover observed cadence. Supports existence only. T8 — executables `gamescope`, `gamescopereaper` (+ `gamescopestream`, `gamescopectl`, `gamescope-type`) and thread names `gamescope-xwm`, `gamescope-vblk`, `gamescope-wl`, `gamescope-reap`, `gamescope-shdr`, `gamescope-pw`, `gamescope-vrmon`, `gamescope-stats`, `gamescope-scrsh`, `gamescope-wait` (all ≤ 15 bytes); packaged in Ubuntu only from 25.10 (S2-12).
- **One observation?** Not an observation; version named.

### S2-22 — mutter 46.2 source: when Xwayland starts and stops in a GNOME Wayland session

- **Citation.** GNOME, *mutter* 46.2 (the series in Ubuntu 24.04, `mutter-common 46.2-1ubuntu0.24.04.16` in S2-01): `src/core/meta-context-main.c`, `src/wayland/meta-xwayland.c`, `data/org.gnome.mutter.gschema.xml.in`.
- **Copy read.** Sparse clone `--branch 46.2` of https://gitlab.gnome.org/GNOME/mutter.git, commit 02050414855b370dbf2b08a971c8b332f7b3c9f4 (2024-05-25), accessed 2026-10-01. Local `sources/S2-22/mutter-46.2/`. SHA-256: meta-xwayland.c 42cd61caa8009c12a0e997f620d9251d8f37bc732df06932776394e45eb824a8; meta-context-main.c a559e0b970c23f9f04fce303d1077f2ec9d20196d685b61c2aae0830a6b4d2d7; gschema e950c02788bd6bd9886ad46ce6c9ccd45fa245d4b676e1f1b0433109ad449006.
- **Passages.**

`S2-22/mutter-46.2/src/core/meta-context-main.c:333–353`
```text
meta_context_main_get_x11_display_policy (MetaContext *context)
{
  MetaCompositorType compositor_type;
#ifdef HAVE_WAYLAND
  MetaContextMain *context_main = META_CONTEXT_MAIN (context);
  g_autofree char *unit = NULL;
#endif

  compositor_type = meta_context_get_compositor_type (context);
  switch (compositor_type)
    {
    case META_COMPOSITOR_TYPE_X11:
      return META_X11_DISPLAY_POLICY_MANDATORY;
    case META_COMPOSITOR_TYPE_WAYLAND:
#ifdef HAVE_WAYLAND
      if (context_main->options.no_x11)
        return META_X11_DISPLAY_POLICY_DISABLED;
      else if (sd_pid_get_user_unit (0, &unit) < 0)
        return META_X11_DISPLAY_POLICY_MANDATORY;
      else
        return META_X11_DISPLAY_POLICY_ON_DEMAND;
```
`S2-22/mutter-46.2/src/wayland/meta-xwayland.c:1104–1114`
```text
  policy = meta_context_get_x11_display_policy (context);

  if (policy == META_X11_DISPLAY_POLICY_ON_DEMAND)
    {
      manager->abstract_fd_watch_id =
        g_unix_fd_add (manager->public_connection.abstract_fd, G_IO_IN,
                       xdisplay_connection_activity_cb, manager);
      manager->unix_fd_watch_id =
        g_unix_fd_add (manager->public_connection.unix_fd, G_IO_IN,
                       xdisplay_connection_activity_cb, manager);
    }
```
`S2-22/mutter-46.2/src/wayland/meta-xwayland.c:971–989`
```text
static gboolean
xdisplay_connection_activity_cb (gint         fd,
                                 GIOCondition cond,
                                 gpointer     user_data)
{
  MetaXWaylandManager *manager = user_data;
  MetaContext *context =
    meta_wayland_compositor_get_context (manager->compositor);
  MetaDisplay *display = meta_context_get_display (context);

  meta_display_init_x11 (display, NULL,
                         (GAsyncReadyCallback) on_init_x11_cb, NULL);

  /* Stop watching both file descriptors */
  g_clear_handle_id (&manager->abstract_fd_watch_id, g_source_remove);
  g_clear_handle_id (&manager->unix_fd_watch_id, g_source_remove);

  return G_SOURCE_REMOVE;
}
```
`S2-22/mutter-46.2/src/wayland/meta-xwayland.c:896–905`
```text
  if (meta_settings_is_experimental_feature_enabled (settings,
                                                     META_EXPERIMENTAL_FEATURE_AUTOCLOSE_XWAYLAND))
#ifdef HAVE_XWAYLAND_TERMINATE_DELAY
    {
      if (x11_display_policy == META_X11_DISPLAY_POLICY_ON_DEMAND)
        {
          /* Terminate after a 10 seconds delay */
          args[i++] = "-terminate";
          args[i++] = "10";
        }
```
`S2-22/mutter-46.2/data/org.gnome.mutter.gschema.xml.in:104–107`
```text
    <key name="experimental-features"
        flags='org.gnome.mutter.MetaExperimentalFeature'>
      <default>[]</default>
      <summary>Enable experimental features</summary>
```
`S2-22/mutter-46.2/data/org.gnome.mutter.gschema.xml.in:129–131`
```text
        • “autoclose-xwayland”        — automatically terminates Xwayland if all
                                        relevant X11 clients are gone.
                                        Requires a restart.
```
- **Coverage.** T8 — covers when Xwayland starts in a GNOME 46 Wayland session run as a systemd user unit: on demand, when the first X11 client connects to the X display socket; and that terminating it when the X11 clients are gone (10 s delay) needs the experimental feature `autoclose-xwayland`, off by default upstream and not switched on by Ubuntu 24.04 (S2-03, ubuntu-settings). Whether and when Xwayland actually starts in a stock session needs observation. Does not cover the X11/Wayland session share. Supports existence only.
- **One observation?** Not an observation; version named.

### S2-23 — Ubuntu 24.04 DKMS module packages: what a build compiles

- **Citation.** Ubuntu noble-updates packages v4l2loopback-dkms 0.12.7-2ubuntu5.2, virtualbox-dkms 7.0.16-dfsg-2ubuntu1.3, zfs-dkms 2.2.2-0ubuntu9.5, nvidia-kernel-source-580 and nvidia-dkms-580 580.178.04-0ubuntu0.24.04.1.
- **Copy read.** archive.ubuntu.com pool, accessed 2026-10-01. Local `sources/S2-23/`. SHA-256: nvidia-dkms-580 33f5e345847ad14209d530169db2fbe9fde7b3e55e9d09b61167266ba3ed6d7a; nvidia-kernel-source-580 9931d75a9309a983211b4b336a899fbb0db85f57d770ffb22e4df87aa8cd1a02; v4l2loopback-dkms 236d2d8fbe8e2eac6b7ef76a5470e1b5a98205a925083575b6c4ab7d285a25e6; virtualbox-dkms ee8193da2905ebfadbb068696437b93c0775be650555d7dc719bdb16e856031a; zfs-dkms 1d095eeb3d47ee9f3e420636b6c44afff50c19127bf2a54dd23eeb68ebc8eaae.
- **Passages.** `dkms.conf` of each:

`grep -n -E 'PACKAGE_VERSION|BUILT_MODULE_NAME|AUTOINSTALL' S2-23/x-nvidia-dkms-580/usr/src/nvidia-580.178.04/dkms.conf`
```text
2:PACKAGE_VERSION="580.178.04"
4:BUILT_MODULE_NAME[0]="nvidia"
10:BUILT_MODULE_NAME[1]="nvidia-modeset"
12:BUILT_MODULE_NAME[2]="nvidia-drm"
14:AUTOINSTALL="yes"
23:BUILT_MODULE_NAME[3]="nvidia-uvm"
25:BUILT_MODULE_NAME[4]="nvidia-peermem"
```
`grep -n -E 'PACKAGE_VERSION|BUILT_MODULE_NAME|AUTOINSTALL' S2-23/x-virtualbox-dkms/usr/src/virtualbox-7.0.16/dkms.conf`
```text
2:PACKAGE_VERSION="7.0.16"
4:BUILT_MODULE_NAME[0]="vboxdrv"
7:BUILT_MODULE_NAME[1]="vboxnetadp"
10:BUILT_MODULE_NAME[2]="vboxnetflt"
13:AUTOINSTALL="yes"
```
`grep -n -E 'PACKAGE_VERSION|BUILT_MODULE_NAME|AUTOINSTALL|MAKE\[0\]' S2-23/x-zfs-dkms/usr/src/zfs-2.2.2/dkms.conf`
```text
2:PACKAGE_VERSION="2.2.2"
54:  -v ${PACKAGE_VERSION}
59:AUTOINSTALL="yes"
60:MAKE[0]="make"
69:BUILT_MODULE_NAME[0]="zfs"
72:BUILT_MODULE_NAME[1]="spl"
```
`grep -n -E 'PACKAGE_VERSION|BUILT_MODULE_NAME|AUTOINSTALL|MAKE\[0\]' S2-23/x-v4l2loopback-dkms/usr/src/v4l2loopback-0.12.7/dkms.conf`
```text
2:PACKAGE_VERSION="0.12.7"
19:MAKE[0]="make KERNEL_DIR=${kernel_source_dir} all"
22:BUILT_MODULE_NAME[0]="$PACKAGE_NAME"
25:AUTOINSTALL="yes"
```
- **Reader's own computation (locates a candidate; not a value).** `find <tree> -name '*.c' | wc -l` (and `-name '*.S'`) per source tree: nvidia-580.178.04 208 `.c` (nvidia 59, nvidia-uvm 127, nvidia-drm 19, nvidia-modeset 2, nvidia-peermem 1) plus two prebuilt objects `nv-kernel.o_binary` and `nv-modeset-kernel.o_binary`; virtualbox-7.0.16 112 `.c`; zfs-2.2.2 290 `.c` and 34 `.S`; v4l2loopback-0.12.7 1 `.c`. The NVIDIA counts equal the number of `NVIDIA*_SOURCES +=` lines in `nvidia/nvidia-sources.Kbuild` (59) and `nvidia-uvm/nvidia-uvm-sources.Kbuild` (127). Files present are not necessarily all compiled for a given kernel configuration.
- **Coverage.** T5 — locates the size of a DKMS autoinstall for modules desktops commonly build (NVIDIA, VirtualBox, ZFS, v4l2loopback): source-file counts per module, run with `make -j$(nproc)` per module and modules one after another (S2-03). On Ubuntu the default NVIDIA route is prebuilt signed modules, not DKMS (S2-28). Build durations not covered. Supports existence only.
- **One observation?** Not an observation; versions named.

### S2-24 — VS Code 1.140.0 and Google Chrome 154.0.8037.92 Linux packages

- **Citation.** Microsoft, `code_1.140.0-1790759618_amd64.deb` (packages.microsoft.com) and VS Code source tag 1.140.0 `resources/linux/bin/code.sh`, `product.json`; Google, `google-chrome-stable_154.0.8037.92-1_amd64.deb` (dl.google.com) and Chromium tag 154.0.8037.92 `chrome/installer/linux/common/wrapper`.
- **Copy read.** Both `.deb` files were streamed and their file lists written (`code_1.140.0.deb.listing`, SHA-256 d06af0a5990c02864ab1ac8a9514f08d177419fc49bb3e381367c6cfee743573; `chrome_154.0.8037.92.deb.listing`, 88f593f42f4ec1eed1b40280d5f933c73fce40fec734c06b6436b6fd933fec9b); the streamed `.deb` SHA-256 values (code e5ddfa528d68ce907c92cba18ed4edd7420874fe828cbaaf8e4484aa33530c3b; chrome 69e3f6ac0a4811f4689ca23f1fd5cc5b2c01550881928b3e196a97131165c4a2) equal those in the vendors' Packages indexes. `code.sh` efa74e76a2c10169f61fe2b7dbd5dbddbad4d59d9c91ab13b8314010ca121d5e; `product.json` 104a252a18d584b91176d24d20a12b7e08ce9225cf0cb176906928c068c1a945; wrapper 7c51f068980a9c35c30de1ea88554238ffb4fee279e18b5cfa6fd3d3bf17460f. Accessed 2026-10-01. Local `sources/S2-24/`.
- **Passages.**

`grep -n -E ' \./usr/share/code/code$| \./usr/share/code/bin/code$' S2-24/code_1.140.0.deb.listing`
```text
22:-rwxrwxr-x  0 root   root     2125 Sep 30 18:02 ./usr/share/code/bin/code
28:-rwxr-xr-x  0 root   root 223509752 Sep 19 14:59 ./usr/share/code/code
```
`S2-24/vscode-1.140.0_resources_linux_bin_code.sh:56–60`
```text
		VSCODE_PATH="/usr/share/@@APPNAME@@"
	fi
fi

ELECTRON="$VSCODE_PATH/@@APPNAME@@"
```
`grep -n -E ' \./opt/google/chrome/(chrome|chrome_crashpad_handler|google-chrome)$| \./usr/bin/google-chrome-stable' S2-24/chrome_154.0.8037.92.deb.listing`
```text
28:-rwxr-xr-x  0 root   root 294133056 Sep 29 06:07 ./opt/google/chrome/chrome
33:-rwxr-xr-x  0 root   root   1961920 Sep 29 06:07 ./opt/google/chrome/chrome_crashpad_handler
37:-rwxr-xr-x  0 root   root      1034 Sep 29 06:07 ./opt/google/chrome/google-chrome
294:lrwxrwxrwx  0 root   root         0 Sep 29 06:07 ./usr/bin/google-chrome-stable -> /opt/google/chrome/google-chrome
```
`S2-24/chromium-154_chrome_installer_linux_common_wrapper:29–30`
```text
# Note: exec -a below is a bashism.
exec -a "$0" "$HERE/@@PROGNAME" "$@"
```
- **Coverage.** T8 — covers the executables: VS Code runs the Electron binary `/usr/share/code/code` (derived `comm` `code`); Chrome's wrapper `exec -a "$0"`s `/opt/google/chrome/chrome` (argv[0] changes, `comm` derived from the file name stays `chrome`); crash handler `chrome_crashpad_handler` (derived `chrome_crashpad`). Neither is in Ubuntu's archive. Supports existence only.
- **One observation?** Not an observation; versions named.

### S2-25 — Flathub manifests, Zoom 7.1.5.4332 tarball, Steam launcher 1.0.0.87

- **Citation.** Flathub manifests at the HEAD commits of us.zoom.Zoom (7fe4ef7f), com.slack.Slack (fd890a77), com.discordapp.Discord (be1b2ec5), com.spotify.Client (a3afae11), im.riot.Riot (5c07f45e), com.valvesoftware.Steam (015e9444), com.github.IsmaelMartinez.teams_for_linux (0b942e10); Zoom `zoom_x86_64.tar.xz` 7.1.5.4332; Valve `steam_1.0.0.87.tar.gz` (steam-launcher, with `bootstraplinux_ubuntu12_32.tar.xz` and `steam.sh`).
- **Copy read.** `https://raw.githubusercontent.com/flathub/<id>/<commit>/<manifest>`; https://cdn.zoom.us/prod/7.1.5.4332/zoom_x86_64.tar.xz streamed and listed (`zoom_x86_64-7.1.5.4332.listing`), streamed SHA-256 17ec33965dace13662a563e4f2ab78281e33f39778ab4fa9fef4da90a5934140 = the manifest's; https://repo.steampowered.com/steam/archive/stable/steam_1.0.0.87.tar.gz (SHA-256 649375d2f9377f8009aaf3e2ff09978041eb9114897d9c5a3886f1d82e27ba1f), bootstrap tarball fba17e3c7550bfcd35bc7f60e04a0f7ba4dad21ce8c8a5704d257c37ce1c9c36, `steam.sh` ae655202f11a16c34594cdec6cc3f48b679b66e614e9d493f76a7474ef20254f, bootstrap listing 4bb0c22734e80b255c8d7b17693954509885a75cb962677eb08c88dc40c13910. Manifest SHA-256: Zoom 63a25060d4ef894066834c0318d2101925a91f2d47ba62112024023770b8913a; Slack a3f87862f2655cfd7135e310d084841dd9856c882f9f2159add32fbd2514d673; Discord ed561941fe6e7a30332f4f9be45c2c0bc0453ad9ed25108ee85420933d74d1a4; Spotify bba7eb591b92a2617471aeafd92c9de0c00093de8241850634fe6ea76bb59b4f; Element ffb4e65390821cd290aec7d9d1324e6f00b49a6bdb5085736026678b5f76a530; Steam f2c057c0d62cf6025bb5a8dae23577d2c6425c36c44ba90d27573896c994efd4; teams-for-linux 56e23330f53c0a9c43e9ecf9c99be9f19ef707bf3fea709408ffacb84587eadf. Accessed 2026-10-01. Local `sources/S2-25/`.
- **Passages.** Zoom tarball, executable files: whole `tar -tvf` lines whose mode starts `-rwx`, with library and data file names left out (reader's filter):

`S2-25/zoom_x86_64-7.1.5.4332.listing — lines with mode -rwx, excluding libraries and data files (reader's filter)`
```text
-rwxr-xr-x  0 zoom   zoom      213 Jul 18 17:21 zoom/getbssid.sh
-rwxr-xr-x  0 zoom   zoom  2567840 Jul 18 18:01 zoom/aomhost
-rwxr-xr-x  0 zoom   zoom 306631992 Jul 18 18:01 zoom/zoom
-rwxr-xr-x  0 zoom   zoom     19152 May  9 21:06 zoom/cef/chrome_sandbox
-rwxr-xr-x  0 zoom   zoom     18288 Jul 18 18:01 zoom/zopen
-rwxr-xr-x  0 zoom   zoom   4567216 Jul 18 18:01 zoom/ZoomWebviewHost
-rwxr-xr-x  0 zoom   zoom    598808 Jul 18 18:01 zoom/cpthost
-rwxr-xr-x  0 zoom   zoom     36160 Jul 18 18:01 zoom/ZoomLauncher
-rwxr-xr-x  0 zoom   zoom 131655680 Jul 18 18:01 zoom/ZoomClips
```

Zoom manifest lines 102–106 (`apply_extra`): 

`S2-25/us.zoom.Zoom@7fe4ef7fcc08__us.zoom.Zoom.json:102–106`
```text
                        "tar xf zoom.tar.xz --no-same-owner",
                        "rm -f zoom.tar.xz",
                        "sed -i 's,/usr/lib/xdg-desktop-portal,/app/lib/xdg-desktop-portal,g' /app/extra/zoom/zoom",
                        "mv /app/extra/zoom/ZoomWebviewHost /app/extra/zoom/ZoomWebviewHost.real",
                        "cp /app/bin/zoom-wrapper.sh /app/extra/zoom/ZoomWebviewHost"
```

Slack and Discord and Spotify and Element and teams-for-linux manifests:

`grep -n -E 'unsquashfs' S2-25/com.slack.Slack@fd890a7711f9__com.slack.Slack.yaml`
```text
88:          - unsquashfs -quiet -no-progress slack.snap usr/lib/slack
```
`grep -n -E 'brotli -cd discord.tar.br' S2-25/com.discordapp.Discord@be1b2ec53e84__com.discordapp.Discord.yaml`
```text
96:      - brotli -cd discord.tar.br | tar xf - -C /app/discord --strip-components 1
```
`grep -n -E '"command": "spotify"' S2-25/com.spotify.Client@a3afae117b34__com.spotify.Client.json`
```text
6:    "command": "spotify",
```
`grep -n -E '^command:|element-desktop-1.12.29.tar.gz' S2-25/im.riot.Riot@5c07f45e61d2__im.riot.Riot.yaml`
```text
7:command: element
67:        url: https://packages.element.io/desktop/install/linux/glibc-x86-64/element-desktop-1.12.29.tar.gz
```
`grep -n -E '^command:|teams-for-linux_2.22.0_amd64.deb' S2-25/com.github.IsmaelMartinez.teams_for_linux@0b942e1044f2__com.github.IsmaelMartinez.teams_for_linux.yml`
```text
7:command: teams-for-linux
84:        url: https://github.com/IsmaelMartinez/teams-for-linux/releases/download/v2.22.0/teams-for-linux_2.22.0_amd64.deb
```

Steam bootstrap listing (selected) and `steam.sh` lines 35, 682–686, 888, 960:

`grep -n -E 'steam\.sh$|ubuntu12_32/steam$|srt-bwrap$|steamerrorreporter$' S2-25/steam-bootstrap-1.0.0.87.listing`
```text
6:-rwxr-xr-x  0 nobody nogroup   150408 Jun 27 00:23 linux32/steamerrorreporter
7:-rwxr-xr-x  0 nobody nogroup    27066 Jun 27 00:24 steam.sh
10:-rwxr-xr-x  0 nobody nogroup 10599244 Jun 27 00:24 ubuntu12_32/steam
164:-rwxr-xr-x  0 nobody nogroup    64624 May 23 03:08 ubuntu12_32/steam-runtime/usr/libexec/steam-runtime-tools-0/srt-bwrap
```
`S2-25/steam.sh-1.0.0.87:35`
```text
  STEAMEXE=`basename "$0" .sh`
```
`S2-25/steam.sh-1.0.0.87:682–686`
```text
PLATFORM=ubuntu12_32
PLATFORM32=ubuntu12_32
PLATFORM64=ubuntu12_64
STEAMRT64=steamrt64
STEAMEXEPATH=$PLATFORM/$STEAMEXE
```
`S2-25/steam.sh-1.0.0.87:888`
```text
	log "Using custom runtime $STEAM_RUNTIME_STEAMRT for steamwebhelper (this is unsupported)"
```
`S2-25/steam.sh-1.0.0.87:960`
```text
	"$STEAMROOT/$STEAMEXEPATH" "$@"
```
- **Coverage.** T8 — covers executable names of Zoom (`zoom`, `ZoomLauncher`, `ZoomWebviewHost`, `aomhost`, `cpthost`, `zopen`, `ZoomClips`), Spotify (`spotify`), teams-for-linux, Element (tarball), Slack (unpacked from the snap's `usr/lib/slack`), Discord (`Discord/` tree), and the Steam client chain (`steam.sh` → `ubuntu12_32/steam`; `steamwebhelper` is downloaded later and only mentioned). T10 — covers, for Zoom on Linux, that the client ships separate helper executables beside `zoom` (a webview host and others); how many processes and threads a call uses needs observation. Supports existence only. T4 — Steam client file names only.
- **One observation?** Not an observation; versions named.

### S2-26 — Microsoft, "Microsoft Teams progressive web app now available on Linux" (Nov 07, 2022)

- **Citation.** Microsoft Teams Blog, techcommunity.microsoft.com, post 3669846, dated Nov 07, 2022.
- **Copy read.** https://techcommunity.microsoft.com/blog/microsoftteamsblog/microsoft-teams-progressive-web-app-now-available-on-linux/3669846 (200), accessed 2026-10-01, SHA-256 67a9c24cf44b60861e96fec2ea19a50a40b7b5f950116726a284d8374c581637. Local `sources/S2-26/` (text `teams-pwa-linux.txt`).
- **Passages.**

`S2-26/teams-pwa-linux.txt:26–29`
```text
Nov 07, 2022
We’re excited to announce the general availability of support for the Microsoft Teams progressive web app (PWA) as a feature of our current web client for Linux customers.
Linux customers who rely on Microsoft Teams for collaboration and communication needs told us they want the full richness of Teams features available for their users in a secure way. This can now be achieved using the Teams PWA.
Additionally, the PWA enables us to ship the latest Microsoft Teams features faster to our Linux customers and helps us bridge the gaps between the Teams desktop client on Linux and Windows. The PWA experience is available for both Edge and Chrome browsers running on Linux.
```
`S2-26/teams-pwa-linux.txt:32`
```text
We encourage our Teams Linux users to switch over to the PWA to get the latest Linux features and a desktop-like experience. Stay tuned for the latest news on the 
```
- **Coverage.** T10 — covers that Microsoft's Linux path for Teams is the web app as a PWA in Edge or Chrome (so a Teams call on Linux runs in the browser's processes, S2-16); the retirement date of the old desktop client is not stated in this copy. T8 — no Microsoft Teams Linux executable to name. Supports existence only.
- **One observation?** Not an observation.

### S2-27 — Timeshift 26.09.0 and Snapper v0.13.2: backup schedules

- **Citation.** Linux Mint, *Timeshift* 26.09.0 `src/Core/Main.vala`; openSUSE, *Snapper* v0.13.2 `data/timeline.timer`, `data/cleanup.timer`, `data/boot.timer`, `data/default-config`.
- **Copy read.** `https://raw.githubusercontent.com/linuxmint/timeshift/26.09.0/src/Core/Main.vala` (SHA-256 b01cfecd3475d2c7bfbdcd342c5e39e3fefc78d6b2b77355eae99de430ea5aba), `.../src/Utility/CronTab.vala` (059f24fc2e4a23cf199f44054d87da6ffb78f6ad069bcc8aa045f8efb1de61bb); `https://raw.githubusercontent.com/openSUSE/snapper/v0.13.2/data/<file>`; accessed 2026-10-01. Local `sources/S2-27/`.
- **Passages.**

`S2-27/timeshift-26.09.0_src_Core_Main.vala:87–96`
```text
	public bool schedule_monthly = false;
	public bool schedule_weekly = false;
	public bool schedule_daily = false;
	public bool schedule_hourly = false;
	public bool schedule_boot = false;
	public int count_monthly = 2;
	public int count_weekly = 3;
	public int count_daily = 5;
	public int count_hourly = 6;
	public int count_boot = 5;
```
`S2-27/timeshift-26.09.0_src_Core_Main.vala:4386–4405`
```text
		CronTab.remove_script_file("timeshift-hourly", "hourly");
			
		// start update ---------------------------
		
		if (scheduled){
			
			//hourly
			CronTab.add_script_file("timeshift-hourly", "d", "0 * * * * root timeshift --check --scripted", stop_cron_emails);
			
			//boot
			if (schedule_boot){
				CronTab.add_script_file("timeshift-boot", "d", "@reboot root sleep 10m && timeshift --create --scripted --tags B", stop_cron_emails);
			}
			else{
				CronTab.remove_script_file("timeshift-boot", "d");
			}
		}
		else{
			CronTab.remove_script_file("timeshift-hourly", "d");
			CronTab.remove_script_file("timeshift-boot", "d");
```
`S2-27/snapper-v0.13.2_data_timeline.timer:1–9`
```text
[Unit]
Description=Timeline of Snapper Snapshots
Documentation=man:snapper(8) man:snapper-configs(5)

[Timer]
OnCalendar=hourly

[Install]
WantedBy=timers.target
```
`S2-27/snapper-v0.13.2_data_cleanup.timer:1–10`
```text
[Unit]
Description=Hourly Cleanup of Snapper Snapshots
Documentation=man:snapper(8) man:snapper-configs(5)

[Timer]
OnBootSec=10m
OnUnitActiveSec=1h

[Install]
WantedBy=timers.target
```
`S2-27/snapper-v0.13.2_data_boot.timer:1–8`
```text
[Unit]
Description=Take snapper snapshot of root on boot

[Timer]
OnBootSec=1

[Install]
WantedBy=timers.target
```
`S2-27/snapper-v0.13.2_data_default-config:49–61`
```text
TIMELINE_CREATE="yes"

# cleanup hourly snapshots after some time
TIMELINE_CLEANUP="yes"

# limits for timeline cleanup
TIMELINE_MIN_AGE="3600"
TIMELINE_LIMIT_HOURLY="10"
TIMELINE_LIMIT_DAILY="10"
TIMELINE_LIMIT_WEEKLY="0"
TIMELINE_LIMIT_MONTHLY="10"
TIMELINE_LIMIT_QUARTERLY="0"
TIMELINE_LIMIT_YEARLY="10"
```
- **Coverage.** T5 — covers that Timeshift schedules nothing until the user enables a level (all `schedule_*` false), then installs an hourly `cron.d` check and optionally a boot snapshot 10 min after boot; Snapper's timeline timer is hourly and cleanup hourly after 10 min, with the default config creating timeline snapshots. Neither is in Ubuntu 24.04's default install (S2-01) nor Fedora Workstation's comps (not listed in S2-06's check). Supports existence only.
- **One observation?** Not an observation; versions named.

### S2-28 — Ubuntu Server documentation, "Install NVIDIA drivers"

- **Citation.** Canonical, *Ubuntu Server documentation — How to install NVIDIA drivers*.
- **Copy read.** https://documentation.ubuntu.com/server/how-to/graphics/install-nvidia-drivers/ → https://ubuntu.com/server/docs/how-to/graphics/install-nvidia-drivers/ (200), accessed 2026-10-01, SHA-256 c841426b229a5af153091c61cfe9d7b0ef26f21c02d626e22fe82bfd7f523f0c. Local `sources/S2-28/` (text `ubuntu-install-nvidia-drivers.txt`).
- **Passages.**

`S2-28/ubuntu-install-nvidia-drivers.txt:325`
```text
 tool is recommended if your computer uses Secure Boot, since it will, by default, only install the pre-built, signed drivers which are known to work with Secure Boot. (Refer to “Building your own kernel modules using the NVIDIA DKMS package” later in this page if you have a specific use case that requires the DKMS drivers.)
```
`S2-28/ubuntu-install-nvidia-drivers.txt:471–473`
```text
linux-modules-nvidia-${DRIVER_BRANCH}${SERVER}-${LINUX_FLAVOUR}
(e.g. 
linux-modules-nvidia-535-generic
```
`S2-28/ubuntu-install-nvidia-drivers.txt:507`
```text
Note: We don’t recommend using the DKMS modules unless you are running a custom kernel for which the prebuilt drivers are not supported. This is because the DKMS drivers are not signed with Canonical’s key and thus do not support secure boot.
```
- **Coverage.** T5 — covers that on Ubuntu the recommended NVIDIA route installs prebuilt, signed `linux-modules-nvidia-*` packages, so a kernel update does not trigger an NVIDIA DKMS build unless the user chose the DKMS packages. Supports existence only.
- **One observation?** Not an observation.

### S2-29 — Mozilla Metrics blog: Test Pilot New Tab Study (2011) and Browsing Sessions (2010)

- **Citation.** Mozilla Metrics blog, *Test Pilot New Tab Study Results* (2011-08-03, post 5078); *Browsing Sessions* (2010-12-22, post 4504).
- **Copy read.** https://blog.mozilla.org/metrics/wp-json/wp/v2/posts/5078 (SHA-256 0d1bd735117482c28bf70a6acbb1538a0a37fb8e34d565b8ee0c39ebdc89374b) and .../posts/4504 (c3220ed609674bc73fd4fbcb52f7bb20c509e4406b05ec27129793512954d59e), accessed 2026-10-01; `content.rendered` converted to text. Local `sources/S2-29/`.
- **Passages.** Post 5078 (`mozmetrics-5078.txt`) and post 4504 (`mozmetrics-4504.txt`):

`S2-29/mozmetrics-5078.txt:9–19`
```text
New Tab Study
 and will soon release a 
multivariate test on the new tab page
. Test Pilot is a platform collecting structured user feedback through Firefox. It currently has about 3 millions users and all the studies are opt in. You can help us better understand how people use their web browser and the Internet in order to build better products by participating studies. Test Pilot add-on is available 
here
.The study ran for 5 days and in all, we collected 256,282 valid submissions.
Results of the study show that on average each user daily:
opens 11 new blank tabs
loads 7 pages
visits 2 unique domains
visits 2 pages in a new tab before they leave or close it
```
`S2-29/mozmetrics-5078.txt:34`
```text
Globally, we check the visit frequencies of all domains, and find that globally only 17.38% domains (461,133 unique domains in total) take 80% of the total page loads (8,291,541 pageloads in total). It verifies the famous “20-80” law of long tail phenomena.
```
`S2-29/mozmetrics-5078.txt:36–43`
```text
Time Spent on New Tabs
According to the study results, on average, users open 
2 pages
 in a new tab before they leave or close it. They load the first web page in 
6 seconds
 (median) after they open new tabs, and stay on the tab for 
1 minute
 (median) once they start browsing. The distributions of these two types of reaction timings display broad tails. The actually mean values are much higher than the medians: users load the first web page in 45 seconds (mean) after they open new tabs, and stay on the tab for 7 minute (mean) once they start browsing, since the outliners and expected noises can vary the mean value a lot.
```
`S2-29/mozmetrics-4504.txt:5–14`
```text
The tl;dr version: users who have more “sessions” (defined below) tend to browse longer, more diversely, and over a broader swath of the day than more casual users.
Preliminaries
Before we begin, the unit of analysis is the “browser session.”  Here is our working definition:  
a browser session is a continuous period of user activity in the browser, where successive events are separated by no more than 30 minutes.
Despite its rudimentary nature, this definition of a session is still fairly common in the 
web analytics
 literature.
The median browser session, median number of sessions
As the graph indicates, the median session is only about 30 minutes long, with a very long tail.  The first quartile is about 9 minutes long, while the third is about an hour.
The median number of sessions per user, on the other hand, is about 2 a day.  Approximately 25% of users actively use the browser only once a day, while the 75th percentile has around 3 sessions a day.
```
`S2-29/mozmetrics-4504.txt:20`
```text
More frequent users tend to use the browser over a wider swath of the day as well.  This is fairly intuitive – more and longer sessions should span a larger part of the day.  It is striking, however, how large the range is for users with many sessions.  This might be a consequence of the sample bias inherent in the Beta population.  Most of our Test Pilot users are tech-savvy young men, so the wide range in which they browse is a little more understandable.
```
- **Coverage.** T3 — covers new blank tabs opened per user per day (mean 11), from one opt-in Firefox Test Pilot study, 5 days, 256,282 submissions, 2011, all platforms; not open-tab or window counts. T10 — covers page loads in that study ("on average each user daily: … loads 7 pages"; the post does not say whether only pages loaded in new tabs are counted; 8,291,541 page loads in total) and, from the week-long Test Pilot session study (2010, Firefox 4 Beta users, "mostly … tech-savvy young men"), session length (median ~30 min, quartiles ~9 min and ~1 h) and sessions per day (median ~2). User-side values, so any platform; platform not stated, population Firefox Test Pilot opt-in users. Old (2010–2011).
- **One observation?** Each post is one observation (one study): post 5078 one 5-day study; post 4504 one week-long study. Machine not named; population and period named.

End note — SHA-256 of small files not listed above: S2-09 `shadow.timer`, `shadow.service`, `archlinux-keyring-wkd-sync.timer`, `PKGBUILD`, and S2-20 HTML pages:

`shasum -a 256`
```text
736eb7b16fc2fff9c902d4823641114338f290a6825e66831f41c5474e994207  S2-09/shadow.timer
31d12e406d0cfda69f50c8b4477ba97eb98c5c636eac64048542fb8c5e9d51ac  S2-09/shadow.service
b8840122040d6e12e780b5b625eb83b3f7cd2448a0296edaa40c3149c9aa4aab  S2-09/archlinux-keyring-wkd-sync.timer
f40aa5498b84fe98be7d9da4cb172710de4dc00786f08041f62fa23043376c82  S2-09/PKGBUILD
c5dd827d5a776789ffd9e425f237e315a1fda561a9495b80df3a35859b44e246  S2-20/steam-faq-71AB-698D-57EB-178C.html
2f9f21a127583b5a4aaf9baff8660ee203b3e9a885962b27deca358c156f670c  S2-20/steam-faq-163C-7C89-406E-2F63.html
3291176669a948b54e27e4337c496b506122d88959d918558f478ab0bf032769  S2-15/wb-bapco-releases-sysmark-25.html
a77819313f1acef8b19c5903218978151f7013393a91286585c1a00b3f589a09  S2-15/wb-sm2018-release.html
3ccb02556ba85dbd314be5fe00c81219a82c83e1f6bbe6d4668002ace902638e  S2-15/bapco-sysmark-30.wayback.html
5a77d8eb8e0cee5196b3fa1866b69c2fa9d19bbe73d0f35543d159eefb08969a  S2-13/pcm10.txt
2b818f49c37434f3f5286cfebb7c91f6b400ebe8d9f293d5f71ce0b0e97f64dc  S2-15/sm30.txt
1d41ebae4a396e3c0579aba9db5516e1e412172bacae31ec9ed43b4ddb1ae25f  S2-06/fedora-release-f44/90-default.preset
1ce567980e6c1c282d5249ec618ced99aa0620a4960e8c3f2a4b10abb9aa3345  S2-10/tasksel-3.81-control
9fb3e8041e7e95b028f5629069295fb079e93499f55ce2c88901afc087895ad2  S2-01/ubuntu-24.04.5.1-desktop-amd64.list
65e764bd14eb7f94a4e6ebb2c2023870bb9e7eeb333b00c47169b7d81aba90e4  S2-24/ms-code-Packages
```

### S2-30 — ClamAV documentation and ClamTk source: what scanning ClamAV provides and how a scheduled scan arises (read at stage 3, 2026-10-01)

- **Citation.** Cisco Talos, *ClamAV Documentation* (the source of docs.clamav.net), GitHub `Cisco-Talos/clamav-documentation`, commit `26dceb239dff15088c5b04b469fd056d1933548b` (2026-08-07). D. Theunsub, *ClamTk*, GitHub `dave-theunsub/clamtk`, commit `694833d27c800e7c3ac4ff6dd44f0b2e65025260` (2024-03-30, ClamTk 6.18). Ubuntu package page `https://packages.ubuntu.com/noble/clamtk`. Read at stage 3 at 인지오's request, after item 19's first recommendation; the passages on unattended-upgrades are from S2-03's copy of `unattended-upgrades_2.9.1+nmu4ubuntu1_all.deb`, the popcon lines from S3-30's copy of `by_inst.gz`.
- **Copy read.** Both repositories shallow-cloned at the commits above, the package page fetched, accessed 2026-10-01; local `sources/S2-30/`. SHA-256: `repo/src/Introduction.md` e92196b92f020bec845924961aa2220d4fb34086de968bc2efa7c538efc14bd3; `repo/src/appendix/Terminology.md` e23f46b9994157eaddf1a204ef559958243733691479cb153ca3f32f6731b335; `repo/src/manual/Usage/Scanning.md` 25e51043fb9d5df174810cb0ddd56366e1c3c31ca67f2cd96fb6b69f0a42035b; `repo/src/manual/Installing/Community-projects.md` 2f1296890125316f6517b607b3da39249201332de6ae9f90f5b664a658a7c4e3; `clamtk/README.md` 7ee8f243a25c8778d93839306888871cd2f7e2b7513ac0fbfcc7b7eaf21a7614; `clamtk/lib/Schedule.pm` 7074b610baa84acf855076dcf4ffadb3a70ad46952142e79a3135582488cf301; `clamtk-noble.html` fcd09d9d22ef8819d2a535ab8157e5fab527879a57a948016c2303d648a66984; S2-03's `x-unattended-upgrades/usr/bin/unattended-upgrade` 3b4eadb2667d662380e24ee2561b33a6b0619701bd9ea1425b5f541d86d9c5b8 and `x-unattended-upgrades/usr/share/unattended-upgrades/50unattended-upgrades` ac8eb4fbfeb483815e5a7a224a86d4242f70bdb41ceb84333b05a9a39f5296be; S3-30's `by_inst.gz` 76cbabe2feb581d69ddc64a4e38895a0adffcef5e9fa94e898b5071ec9af5007 (the copy S3-30 records).
- **Passages — ClamAV documentation.**
  - `src/Introduction.md:10`: "ClamAV is an open source (GPLv2) anti-virus toolkit, designed especially for e-mail scanning on mail gateways. It provides a number of utilities including a flexible and scalable multi-threaded daemon, a command line scanner and advanced tool for automatic database updates."
  - `src/Introduction.md:12`: "> _Tip_: ClamAV is not a traditional anti-virus or endpoint security suite. For a fully featured modern endpoint security suite, check out *Cisco Secure Endpoint*."
  - `src/appendix/Terminology.md:12–13`: "| *endpoint* | An endpoint is a computer that a human interacts with, such as a laptop, desktop, or mobile device. |" / "| *endpoint security suite* | An endpoint security suite is software that bundles a variety of services to protect a computer system. In addition to scheduled malware scanning, this may include features like a firewall, on-access scanning, network traffic monitoring, process behavioral monitoring, and other real time protection features. |"
  - `src/manual/Usage/Scanning.md:152–156`: "## One-Time Scanning" / "### ClamScan" / "`clamscan` is a command line tool which uses *libclamav* to scan files and/or directories for viruses. Unlike `clamdscan`, `clamscan` does *not* require a running `clamd` instance to function. Instead, `clamscan` will create a new engine and load in the virus database each time it is run. It will then scan the files and/or directories specified at the command line, create a scan report, and exit."
  - `src/manual/Installing/Community-projects.md:380–382`: "### ClamTK | ClamAV" / "ClamTk is a GUI front-end for ClamAV using gtk2-perl. It is designed to be an easy-to-use, on-demand scanner for Linux systems."
  - A grep of `src/` for `cron`, `schedul` and `timer` finds no instruction to run a scan on a schedule; its hits are the terminology line above, on-access scanning (`clamonacc`, set up by the user through `clamd.conf`), and a `cron` job for a private signature mirror (`src/appendix/CvdPrivateMirror.md:43`).
- **Passages — ClamTk.**
  - `README.md:3`: "Note: This program is no longer maintained."
  - `lib/Schedule.pm:17`: "# scheduling, so we have call crontab as a system command."; `:424`: `print $T "$min $hour * * * $full_cmd # clamtk-scan\n";`, where `$full_cmd` starts from the `clamscan` path (`:356`).
  - `clamtk-noble.html:84`: "Package: clamtk (6.07-1.1)", in Ubuntu noble's universe component.
- **Passages — unattended-upgrades 2.9.1+nmu4ubuntu1** (S2-03's copy).
  - `50unattended-upgrades:6–8`: `Unattended-Upgrade::Allowed-Origins {` / `"${distro_id}:${distro_codename}";` / `"${distro_id}:${distro_codename}-security";` (each tab-indented), and the ESM pockets at `:13–14`.
  - `unattended-upgrade:2150–2155`: "# be nice when calculating the upgrade as its pretty CPU intensive" / "old_priority = os.nice(0)" / "try:" / "# Check that we will be able to restore the priority" / "os.nice(-1)" / "os.nice(20)"; `:2172–2173`: "# stop being nice" / "os.nice(old_priority - os.nice(0))", before the download and install (`:2175` "# download what looks good").
- **Passages — popcon** (S3-30's copy, `by_inst.gz`; columns inst, vote, old, recent, no-files): "2010  unattended-upgrades            52931 37751 13449  1716    15"; "5408  clamav-freshclam               11371 10152  1106   111     2"; "5435  clamav                         11197  2472  8142   581     2"; "6831  clamav-daemon                   6732  5883   803    45     1"; "11221 clamtk                          1992   314  1564   114     0". Reader's own, over 291,196 submissions: `clamav` (which ships `clamscan`) installed on 3.85 %, in regular use on 0.85 %; `clamtk` installed on 0.68 %, in regular use on 0.11 %; `unattended-upgrades` installed on 18.18 %, in regular use on 12.96 %.
- **Coverage.** T5 — covers how an anti-virus scan comes to run on a Linux desktop with ClamAV: its vendor describes a toolkit "designed especially for e-mail scanning on mail gateways", "not a traditional anti-virus or endpoint security suite", whose desktop scanner `clamscan` is a one-time scan run from the command line; scheduled malware scanning is named as a feature of endpoint security suites, which ClamAV says it is not. A scheduled `clamscan` on a desktop exists only as a user's choice: ClamTk's scheduler writes a daily user crontab line that runs `clamscan`; ClamTk is no longer maintained, is packaged in Ubuntu 24.04's universe component, and is in regular use on 0.11 % of Debian popcon submissions. For the stock unattended upgrade: what it installs by default (the release and security pockets, and ESM where present) and that it lowers its own priority while calculating the upgrade, not while downloading and installing. Supports existence only; prevalence from popcon (Debian, servers and desktops mixed).
- **One observation?** Documents and source, not an observation; the popcon lines are S3-30's one observation.

## 3. Not found

- **T3 — numbers of open tabs and windows, and visible windows, from vendor telemetry; observed renderer-process counts for a set of tabs.** Searches: rows 33 and 40 (Mozilla telemetry dashboards and Mozilla Metrics blog; no Chromium/Google publication). The only S2 user data is new-tab openings (S2-29). The Chromium soft limit and spare process are definitions (S2-16), not observations.
- **T4 — thread counts, thread names and busy threads of a running game (native or Proton); what runs beside a game; whether Steam downloads during gameplay by default; the Steam overlay's process.** Primary sources give only mechanisms (S2-18, S2-19, S2-21) and the existence of a per-game download setting (S2-20); rows 29–30 found no Valve statement of the default. The Steam client and overlay are closed source; `steamwebhelper` appears only as a name in `steam.sh` (S2-25); `gameoverlayui` was not found in the bootstrap listing. Observed frame cadence of nested gamescope: not found (S2-21 gives the rule only).
- **T5 — typical durations of the jobs; how often an indexer re-crawls on real desktops; DKMS build durations; which DKMS modules desktops actually carry.** No primary source states these (they need observations). Debian 13 was covered only through its desktop task (S2-10).
- **T7 — CpsMark+ scenarios.** The defining article (doi 10.1016/j.tbench.2023.100084) is literature, and every route to its text failed (row 24: 403, 400, captcha, 404). SYSmark 25 and SYSmark 2018 white papers: not obtained (rows 22–23: 403; Wayback 404; CDX offline). PCMark 10 Applications and Storage benchmarks: not in the 2018 guide read.
- **T8 — share of Linux desktop sessions on X11 against Wayland.** Row 33: the reachable Mozilla data has no window-protocol field; the press article that reports one was 403. No vendor or project publication with a share was found. Spotify, Slack, Discord, Element: actual binary names inside the unpacked trees were not listed (manifests only).
- **T10 — rates of heavy operations (e-mail sends with or without attachment, image filters, video previews, chat messages received) per hour or session.** No vendor or project publication found beyond S2-29's page loads. Thread structure of a Zoom, Teams, Meet or Jitsi call on Linux: only names in source (S2-16) and executables (S2-25); no primary-source observation.
