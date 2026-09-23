# S2 — primary project and vendor documentation and source code

Reader class S2. Topics owned: T4, T5, T6, T8, T10, T11 (plus what documentation says about others).
Search date for every row and every copy: **2026-09-23** (UTC). Source copies are under `../sources/S2-NN/` (gitignored); everything needed is quoted below.

Conventions in this record:

- `file:line` locators refer to the file inside the named package version or git commit.
- For a `.deb`, the SHA-256 is of the `.deb` as fetched; the quoted file is the path inside it (`dpkg-deb -x`). Maintainer scripts are `DEBIAN/postinst` from `dpkg-deb -e`.
- For a git clone, the commit id and committer date identify the copy; the SHA-256 is of the single file copied out of that commit.
- "Documentation" here means configuration and source that *define* behaviour. None of these candidates is an observation of real users; each is marked as such.

---

## 1. Search log

| # | Date | Engine / venue | Exact query or request | Hits followed | Dead ends (HTTP status) |
|---|---|---|---|---|---|
| 1 | 2026-09-23 | Ubuntu archive via `apt-get download` (noble / noble-updates / noble-security, amd64) | `plocate man-db dpkg apt fwupd logrotate e2fsprogs util-linux base-files update-notifier-common clamav-freshclam clamav-daemon dkms packagekit gnome-software ubuntu-release-upgrader-core` | 17 packages downloaded after `apt-get update` | first attempt with stale index: dpkg, fwupd, packagekit, ubuntu-release-upgrader-core, util-linux → **404 Not Found** (superseded versions); retried after `apt-get update` → OK |
| 2 | 2026-09-23 | Ubuntu archive `apt-get download` | `clamav-base ubuntu-desktop-minimal ubuntu-desktop ubuntu-standard tracker-miner-fs tracker-extract tracker kubuntu-desktop baloo-kf5 gdm3 dbus dbus-user-session dbus-broker pipewire pipewire-pulse wireplumber sddm update-notifier ubuntu-session gnome-session-common` | all downloaded (`libkf5baloo5` not needed) | — |
| 3 | 2026-09-23 | `apt-cache rdepends --no-suggests plocate` (noble index) | `plocate` | reverse deps: catfish, kubuntu-desktop, ubuntustudio-desktop, hollywood, cruft-ng (not ubuntu-desktop) | — |
| 4 | 2026-09-23 | src.fedoraproject.org raw file | `https://src.fedoraproject.org/rpms/fedora-release/raw/{f43,f44,rawhide}/f/{90-default.preset,80-workstation.preset,90-default-user.preset}` | none | **HTTP 200 but Anubis bot-check HTML** ("Making sure you're not a bot!") — dead end; copies deleted |
| 5 | 2026-09-23 | `git clone` src.fedoraproject.org | `rpms/fedora-release.git` | rawhide spec says presets moved to `redhat-systemd-presets`; f43 branch still has `90-default.preset` | — |
| 6 | 2026-09-23 | `git clone` src.fedoraproject.org | `rpms/redhat-systemd-presets.git`, `rpms/plocate.git`, `rpms/man-db.git` | all | — |
| 7 | 2026-09-23 | `git clone` GitHub | `rpm-software-management/dnf5` | `etc/systemd/dnf5-makecache.{timer,service}`, `dnf5.spec` | — |
| 8 | 2026-09-23 | curl | `https://plocate.sesse.net/download/plocate-1.1.25.tar.gz` | 200 | SHA-512 of fetched tarball (93d8abbe…) does **not** match Fedora `sources` (ad0bb2df…); recorded, content read as-is |
| 9 | 2026-09-23 | `git clone` gitlab.archlinux.org | `archlinux/packaging/packages/{plocate,dbus-broker,dbus,dkms}` | all | — |
| 10 | 2026-09-23 | WebSearch | `archlinux.org news dbus-broker default dbus-units` | archlinux.org/news/making-dbus-broker-our-default-d-bus-daemon/ (200) | — |
| 11 | 2026-09-23 | WebSearch | `GNOME tracker-miner-fs renamed localsearch 3.8 GNOME 47` | blogs.gnome.org/carlosg/2024/07/14/… (200) | — |
| 12 | 2026-09-23 | `git clone` gitlab.gnome.org | `GNOME/localsearch` | NEWS, `src/indexer/*`, `src/extractor/meson.build` | — |
| 13 | 2026-09-23 | `git clone` GitHub | `dell/dkms` | `dkms.service.in`, `redhat_kernel_install.d.in`, `dkms.in`, `dkms_framework.conf.in`, `Makefile` | — |
| 14 | 2026-09-23 | `git clone` GitHub (sparse / blob-less) | `umlaeute/v4l2loopback`, `NVIDIA/open-gpu-kernel-modules`, `openzfs/zfs`, `morrownr/88x2bu-20210702`, `VirtualBox/virtualbox` | Kbuild / Makefile object lists | — |
| 15 | 2026-09-23 | curl raw.githubusercontent.com | `torvalds/linux/v6.16/include/linux/sched.h`; man7.org `PR_SET_NAME.2const.html` | both 200 | — |
| 16 | 2026-09-23 | `git clone` gitlab.gnome.org (blob-less) | `GNOME/mutter` → `NEWS`, `src/core/meta-context-main.c`, `data/org.gnome.mutter.gschema.xml.in` | all | gschema has flag `autoclose-xwayland` but no description text for it — nothing quotable on auto-close |
| 17 | 2026-09-23 | `git clone` | `gitlab.freedesktop.org/pipewire/pipewire`, `…/pipewire/wireplumber`, `github.com/bus1/dbus-broker` | user units | — |
| 18 | 2026-09-23 | Ubuntu 26.04 (resolute) archive: `dists/resolute{,-updates}/{main,universe}/binary-amd64/Packages.xz`, then pool files | `ubuntu-desktop-minimal ubuntu-desktop kubuntu-desktop dbus dbus-user-session dbus-broker localsearch plocate gdm3 mutter gnome-session pipewire wireplumber sddm ubuntu-session` | 8 debs downloaded | — |
| 19 | 2026-09-23 | chromium.googlesource.com `?format=TEXT` at commit `86098b063d52985b42f3f0e2ff45ca039ff533f5` | `docs/process_model_and_site_isolation.md`, `content/browser/renderer_host/render_process_host_impl.cc`, `content/public/browser/render_process_host.h`, `content/public/common/content_features.cc`, `content/common/features.cc`, `base/threading/platform_thread_linux.cc`, `chrome/VERSION` | all 200 | api.github.com commits endpoint returned no `sha` (rate-limited JSON) — used `git ls-remote` |
| 20 | 2026-09-23 | raw.githubusercontent.com `mozilla-firefox/firefox@281872e7df7b7d31f0090788d747d44e5d124874` | `modules/libpref/init/all.js`, `browser/app/profile/firefox.js`, `modules/libpref/init/StaticPrefList.yaml`, `browser/components/metrics.yaml`, `toolkit/components/telemetry/Scalars.yaml`, `browser/config/version.txt` | all 200 | `browser/components/metrics.yaml`: no tab/window count metric (grep empty) |
| 21 | 2026-09-23 | WebSearch | `Firefox Public Data Report usage behavior tabs open "data.firefox.com"` | data.firefox.com (JS-rendered, not read); `mozilla/firefox-public-data-report-etl` cloned | data.firefox.com dashboards need JS; ETL README read instead |
| 22 | 2026-09-23 | curl help.steampowered.com | `/en/faqs/view/4F9E-6328-E9B8-47F9`, `/en/faqs/view/71AB-698D-57EB-178C` | both 200; body is in a JSON `data-` attribute of the page | Wayback not needed |
| 23 | 2026-09-23 | `git clone` | `gitlab.steamos.cloud/steamrt/steam-runtime-tools`, `github.com/ValveSoftware/steam-runtime` | `docs/steam-compat-tool-interface.md`, `docs/steam-runtime-emulator.json.5.md`, `pressure-vessel/adverb.1.md` | `steam-runtime/doc/*` had no process-tree text |
| 24 | 2026-09-23 | `git clone` GitHub | `ValveSoftware/Proton` (default branch `proton_11.0`) | `proton` script | — |
| 25 | 2026-09-23 | curl gitlab.winehq.org raw | `wine/wine/-/raw/df15af36…/dlls/ntdll/unix/thread.c`, `…/VERSION` | none | **HTTP 200 but Anubis bot-check HTML** — dead end; copies deleted |
| 26 | 2026-09-23 | curl raw.githubusercontent.com `wine-mirror/wine@df15af3652511150490934682202d45af892f887` | `dlls/ntdll/unix/thread.c`, `dlls/ntdll/unix/env.c`, `dlls/ntdll/unix/loader.c`, `programs/wineboot/wineboot.c`, `programs/services/services.c`, `VERSION`; also grep of `loader/preloader.c`, `dlls/ntdll/unix/process.c`, `server.c`, `virtual.c`, `dlls/kernelbase/process.c`, `dlls/ntdll/loader.c` | all 200 | — |
| 27 | 2026-09-23 | curl raw.githubusercontent.com | `ValveSoftware/gamescope@2cfb4803984e8e4144805b57ebb5d38ea42bec13/README.md` | 200 | — |
| 28 | 2026-09-23 | WebSearch | `Discord support game overlay supported platforms Linux` | support.discord.com article 217659737 | HTML page **HTTP 403**; Zendesk API `support.discord.com/api/v2/help_center/en-us/articles/217659737.json` → 200 |
| 29 | 2026-09-23 | WebSearch | `Microsoft Teams Linux client retirement December 2022 progressive web app announcement` | techcommunity.microsoft.com discussion 3630968 (200, MVP post, not Microsoft); learn.microsoft.com/en-us/microsoftteams/get-clients (200) | Microsoft 365 message center MC412007 itself not publicly reachable (not attempted beyond search results) |
| 30 | 2026-09-23 | WebSearch | `Zoom Workplace Linux client processes zoom ZoomWebviewHost documentation` | only community forums / third-party guides; no Zoom documentation of process structure | — (no vendor doc found) |
| 31 | 2026-09-23 | curl zoom.us | `https://zoom.us/client/latest/zoom_amd64.deb` → 302 → `https://cdn.zoom.us/prod/7.2.1.5760/zoom_amd64.deb` | 200, 302 788 858 bytes | — |
| 32 | 2026-09-23 | WebSearch | `GNOME application startup time measurement documentation sysprof "startup" app launch Linux` | tecnocode.co.uk/2020/07/14/startup-time-profiling-of-gnome-software/ (200) | developer.gnome.org sysprof page not followed (tool doc, no numbers) |
| 33 | 2026-09-23 | curl raw.githubusercontent.com | `systemd/systemd@f30c9ea09c1ca4ca0da330537cd00f421fd851f3/units/user@.service.in`, `meson.version` | 200 | — |

---

## 2. Candidates

### S2-01 — Ubuntu 24.04 LTS (noble) packaging: timers and services enabled on package install

- **Citation.** Ubuntu archive, noble / noble-updates / noble-security, amd64 binary packages (Canonical / Debian maintainers).
- **Copies read** (`../sources/S2-01/`, fetched 2026-09-23 with `apt-get download`, archive.ubuntu.com / security.ubuntu.com):

| package_version | SHA-256 of .deb |
|---|---|
| apt_2.8.3_amd64.deb | c9ace99efc7726fe0035f921a9acf262a9723bbf35b861aab4f9075a0be67442 |
| base-files_13ubuntu10.5_amd64.deb | 87e8c41e62f61625fb78a982d0bc0a70f40ef8375bc313b154914d1b3759c823 |
| dkms_3.0.11-1ubuntu13_all.deb | 18d098c65e3002040afc11f80656e84377551a5d1bdcd3933cdf6ae2e58dcd75 |
| dpkg_1.22.6ubuntu6.6_amd64.deb | ceb6aa4da59fbcb8a3b0549b4280c60b7d849b519859797c8668bdfbe378fb3b |
| e2fsprogs_1.47.0-2.4~exp1ubuntu4.1_amd64.deb | 1d0fb19dcf14316d04602260871dba3c1441c0ecf3c3bde54eacba35dcc5a40b |
| fwupd_2.0.20-1ubuntu2~24.04.2_amd64.deb | 0e04b5c0081114c080e4a3618e12e73a311f33bf061c8e53c151459a6149fcea |
| gnome-software_46.0-1ubuntu2_amd64.deb | 338dacc6f5e73786c032fc25cf095e2ab671a3d0998c4b44db6c499e9417d1a2 |
| logrotate_3.21.0-2build1_amd64.deb | e609ad80a9cec135b404a84f99d9d87bc304800eb212702444a985527edba70c |
| man-db_2.12.0-4build2_amd64.deb | d7ce31173a73bd3a93b7216a837a2e8641fff3fd7ae2dfc0ca705dbabe03e92b |
| packagekit_1.2.8-2ubuntu1.5_amd64.deb | 7731a59a7c9acbd0e32d957184ffd3bfc0034a68ba6309f22b7d177ca14067a7 |
| plocate_1.1.19-2ubuntu2_amd64.deb | 90375d69eda16ca5f73e6449447ef05c1a18b7b1de4092879eda9850898c04b0 |
| ubuntu-release-upgrader-core_1%3a24.04.29_all.deb | be3e4274cff3ecd4941b7cb6cd8b90865dcedded21dcf053298e2016629be3b5 |
| update-notifier-common_3.192.68.2_all.deb | 50c3303b52aaaaadcf11750e1a0afc905bdee0d6f75aa2f1febdd4416afe7fec |
| update-notifier_3.192.68.2_amd64.deb | 73a1125b22bee324fb9af0ff01bacf2cdba8a5f95c8ae1dcb7dc93333b4eddc7 |
| util-linux_2.39.3-9ubuntu6.6_amd64.deb | 08eb17ba3b83378ed1e73d8335d0ce03b429c0bbeb07e374f536234edab02465 |

- **Verbatim passages.**

  Enabling mechanism (identical debhelper block in every package below; plocate shown), `plocate_1.1.19-2ubuntu2 DEBIAN/postinst:38-42`:
  ```
  	# was-enabled defaults to true, so new installations run enable.
  	if deb-systemd-helper --quiet was-enabled 'plocate-updatedb.timer'; then
  		# Enables the unit on first installation, creates new
  		# symlinks on upgrades if the unit file has changed.
  		deb-systemd-helper enable 'plocate-updatedb.timer' >/dev/null || true
  ```
  The same `deb-systemd-helper enable '<unit>'` line is present at: `apt DEBIAN/postinst:29` (`apt-daily-upgrade.timer`), `:46` (`apt-daily.timer`); `base-files :155` (`motd-news.timer`); `dpkg :97` (`dpkg-db-backup.timer`); `e2fsprogs :20` (`e2scrub_all.timer`), `:37` (`e2scrub_reap.service`); `fwupd :36` (`fwupd-refresh.timer`); `logrotate :12` (`logrotate.timer`); `man-db :134` (`man-db.timer`); `update-notifier-common :45` (`update-notifier-download.timer`), `:62` (`update-notifier-motd.timer`); `util-linux :17` (`fstrim.timer`).

  Timer schedules (file inside the package):
  - `apt: usr/lib/systemd/system/apt-daily.timer:5-7` — `OnCalendar=*-*-* 6,18:00` / `RandomizedDelaySec=12h` / `Persistent=true`
  - `apt: …/apt-daily-upgrade.timer:6-8` — `OnCalendar=*-*-* 6:00` / `RandomizedDelaySec=60m` / `Persistent=true`
  - `apt: …/apt-daily.service:4,10` — `ConditionACPower=true` … `ExecStart=/usr/lib/apt/apt.systemd.daily update`; `apt-daily-upgrade.service:10` — `ExecStart=/usr/lib/apt/apt.systemd.daily install`
  - `base-files: …/motd-news.timer:5-8` — `OnCalendar=00,12:00:00` / `RandomizedDelaySec=12h` / `Persistent=true` / `OnStartupSec=1min`; `motd-news.service:8` — `ExecStart=/etc/update-motd.d/50-motd-news --force`; `etc/update-motd.d/50-motd-news:37` — `[ "$ENABLED" = "1" ] || exit 0`
  - `dpkg: …/dpkg-db-backup.timer:2,6-7` — `Description=Daily dpkg database backup timer` / `OnCalendar=daily` / `Persistent=true`; `dpkg-db-backup.service:7` — `ExecStart=/usr/libexec/dpkg/dpkg-db-backup`
  - `e2fsprogs: …/e2scrub_all.timer:6-8` — `OnCalendar=Sun *-*-* 03:10:00` / `RandomizedDelaySec=60` / `Persistent=true`; `e2scrub_all.service:3,11` — `ConditionACPower=true` … `ExecStart=/sbin/e2scrub_all`
  - `fwupd: …/fwupd-refresh.timer:3,6-8` — `ConditionVirtualization=!container` / `OnCalendar=*-*-* *:00:00` / `RandomizedDelaySec=1h` / `Persistent=true`; `fwupd-refresh.service:25` — `ExecStart=/usr/bin/fwupdmgr refresh`
  - `logrotate: …/logrotate.timer:6-8` — `OnCalendar=daily` / `AccuracySec=1h` / `Persistent=true`; `logrotate.service:9,11-14` — `ExecStart=/usr/sbin/logrotate /etc/logrotate.conf` / `# performance options` / `Nice=19` / `IOSchedulingClass=best-effort` / `IOSchedulingPriority=7`
  - `man-db: …/man-db.timer:6-8` — `OnCalendar=daily` / `RandomizedDelaySec=12h` / `Persistent=true`; `man-db.service:4,11-15` — `ConditionACPower=true` … `ExecStart=/usr/bin/mandb --quiet` / `User=man` / `Nice=19` / `IOSchedulingClass=idle` / `IOSchedulingPriority=7`
  - `plocate: …/plocate-updatedb.timer:5-8` — `OnCalendar=daily` / `RandomizedDelaySec=12h` / `AccuracySec=20min` / `Persistent=true`; `plocate-updatedb.service:3,7-9` — `ConditionACPower=true` … `ExecStart=/usr/sbin/updatedb.plocate` / `LimitNOFILE=131072` / `IOSchedulingClass=idle` (no `Nice=` line in this Ubuntu unit)
  - `update-notifier-common: lib/systemd/system/update-notifier-download.timer:6-7` — `OnStartupSec=5m` / `OnUnitActiveSec=24h`; `update-notifier-motd.timer:2,6-8` — `Description=Check to see whether there is a new version of Ubuntu available` / `OnCalendar=Sun *-*-* 06:00:00` / `RandomizedDelaySec=1w` / `Persistent=true`
  - `util-linux: …/fstrim.timer:2,4,8-11` — `Description=Discard unused filesystem blocks once a week` / `ConditionVirtualization=!container` / `OnCalendar=weekly` / `AccuracySec=1h` / `Persistent=true` / `RandomizedDelaySec=100min`
  - `packagekit: …/packagekit.service:10-13` — `Type=dbus` / `BusName=org.freedesktop.PackageKit` / `User=root` / `ExecStart=/usr/libexec/packagekitd` (no `[Install]`; D-Bus activated)
  - `gnome-software: etc/xdg/autostart/org.gnome.Software.desktop:4-5` — `Exec=/usr/bin/gnome-software --gapplication-service` / `OnlyShowIn=GNOME;Unity;`
  - `update-notifier: etc/xdg/autostart/update-notifier.desktop:192,198` — `Exec=update-notifier` / `X-GNOME-Autostart-Delay=60`; `usr/share/glib-2.0/schemas/com.ubuntu.update-notifier.gschema.xml:14-16` — `<key type="i" name="regular-auto-launch-interval">` / `<default>7</default>` / `<summary>Interval (in days) when to auto launch for normal updates</summary>`

  DKMS on Ubuntu (package `dkms_3.0.11-1ubuntu13`): `etc/kernel/postinst.d/dkms:37-38`
  ```
  if [ -x /usr/lib/dkms/dkms_autoinstaller ]; then
      exec /usr/lib/dkms/dkms_autoinstaller start "$inst_kern"
  ```
  `usr/lib/dkms/dkms_autoinstaller:74-75`
  ```
  			log_action_msg "$prog: running auto installation service for kernel $kernel"
  			dkms autoinstall --kernelver $kernel
  ```
  `usr/sbin/dkms:1113` — `local the_make_command="${make_command/#make/make -j$parallel_jobs KERNELRELEASE=$kernelver}"`; `:2594` — `parallel_jobs=${parallel_jobs:-$(get_num_cpus)}`.

- **Coverage.**
  - T6: covers — object: systemd timers/services shipped *and enabled on install* by each package; unit: calendar spec, randomized delay, scheduling class/nice; statistic: configured schedule (not observed runs); scope: Ubuntu 24.04 amd64 package versions listed; population: any system with these packages installed. Process names follow from `ExecStart` (`apt.systemd.daily`, `dpkg-db-backup`, `e2scrub_all`, `fwupdmgr`, `logrotate`, `mandb`, `updatedb.plocate`, `fstrim`, `packagekitd`, `gnome-software`, `update-notifier`). Does **not** give how long each job runs. DKMS: kernel postinst hook runs `dkms autoinstall` with `make -j<nproc>`; no duration.
  - Which of these packages a *stock* desktop has is S2-02.
  - T8: partly (update-notifier, gnome-software autostart processes in a GNOME session).
  - Other topics: does not cover.
- **One observation?** No — configuration, not an observation. Platform named (Ubuntu 24.04 amd64, package versions); no subjects, no window.

### S2-02 — Ubuntu 24.04 desktop metapackages (what a stock install contains)

- **Citation.** Ubuntu archive, `ubuntu-meta` 1.539.2 and `kubuntu-meta` 1.451.2 (noble-updates).
- **Copies read** (`../sources/S2-02/`, 2026-09-23, `apt-get download`):
  ubuntu-desktop-minimal_1.539.2_amd64.deb `fef7780320e50c1453e6d1346862c283e70616631204ecf73e29f41d038cbe48`;
  ubuntu-desktop_1.539.2_amd64.deb `cb36ea605b1225c091d2d6ece2bf6aa17fbb7771e9d18811374494784626d785`;
  ubuntu-standard_1.539.2_amd64.deb `86eee4aa5f149b94984df2f8b79fe0cdcf81cc38ca5b441f9df4516b38ade7f7`;
  kubuntu-desktop_1.451.2_amd64.deb `ed56cfa0810de5b5e2c23a94b1bc113058f7a1bf41849f8f95f631ae82c9112a`.
- **Verbatim passages** (control fields, `dpkg-deb -f`):
  - `ubuntu-desktop-minimal 1.539.2` `Depends:` includes `… gdm3, … gnome-shell, … nautilus, … pipewire-pulse, … ubuntu-session, … update-manager, update-notifier, … wireplumber, … xorg, …`; `Recommends:` includes `… fwupd, fwupd-signed, … packagekit, … snapd, … systemd-oomd, …`. Neither field lists `plocate`, `clamav*` or `gnome-software`.
  - `ubuntu-standard 1.539.2` `Depends: bind9-dnsutils, busybox-static, cpio, cron, … logrotate, lshw, lsof, man-db, …`
  - `kubuntu-desktop 1.451.2` Depends/Recommends include (one per line after splitting on commas): `pipewire`, `pipewire-pulse`, `xorg`, `baloo-kf5`, `dbus-x11`, `kwin-wayland`, `plocate`.
  - Priorities (`DEBIAN/control`): `apt … Priority: required`, `base-files … required`, `dpkg … required`, `e2fsprogs … required`; `clamav-daemon`, `clamav-freshclam`, `dkms`, `fwupd`, `gnome-software`: `Priority: optional`.
- **Coverage.** T6: which package sets a stock Ubuntu 24.04 GNOME vs Kubuntu desktop pulls in → with S2-01, stock Ubuntu GNOME gets apt-daily*, dpkg-db-backup, e2scrub_all, fstrim, logrotate, man-db, motd-news, update-notifier-*, fwupd-refresh (via Recommends) but not plocate (plocate comes with Kubuntu); ClamAV is not in any seed. T8: xorg installed alongside Wayland session packages on 24.04. Other topics: no.
- **One observation?** No (configuration). Platform Ubuntu 24.04; no subjects/window.

### S2-03 — Ubuntu 24.04 ClamAV packaging (freshclam defaults; no scan timer)

- **Citation.** `clamav` source 1.5.4+dfsg-0ubuntu0.24.04.1 (noble-updates).
- **Copies** (`../sources/S2-03/`, 2026-09-23): clamav-freshclam_1.5.4+dfsg-0ubuntu0.24.04.1_amd64.deb `684b8c6fb5c50a7efb744a2e1f2998cff1e847980cc1eccd6a39cba28a8981c2`; clamav-daemon_… `e9943d5e9dc7a5b37162ad19331a960aa6713b9f74bf64074cb1ac4f210abf4d`; clamav-base_… `bb45463d7db3513f97711beda93271128cb00b2e53d26d3fabd1dcda67662986`.
- **Verbatim passages.**
  - `clamav-freshclam DEBIAN/templates:1-3,22` — `Template: clamav-freshclam/autoupdate_freshclam` / `Type: select` / `Choices: daemon, ifup.d, cron, manual` … `Default: daemon`
  - `DEBIAN/templates:504-507` — `Template: clamav-freshclam/update_interval` / `Type: string` / `Default: 24` / `Description: Number of freshclam updates per day:`
  - `DEBIAN/postinst` (lines 591-593 of 609): `  if [ "$runas" = 'daemon' ]; then` / `    update-rc.d clamav-freshclam defaults >/dev/null` / `    invoke-rc.d clamav-freshclam start`
  - `usr/lib/systemd/system/clamav-freshclam.service:10` — `ExecStart=/usr/bin/freshclam -d --foreground=true`
  - `usr/lib/systemd/system/clamav-freshclam-once.timer:2,5-7` — `Description=Daily ClamAV virus database update` / `OnCalendar=daily` / `AccuracySec=1h` / `RandomizedDelaySec=1h` (this timer has **no** `deb-systemd-helper enable` line in postinst)
  - `clamav-daemon: usr/lib/systemd/system/clamav-daemon.service:10` — `ExecStart=/usr/sbin/clamd --foreground=true`; enabled by `DEBIAN/postinst:779` `deb-systemd-helper enable 'clamav-daemon.service'`
  - `clamav-daemon: usr/lib/systemd/system/clamav-clamonacc.service:14` — `ExecStart=/usr/sbin/clamonacc -F --log=/var/log/clamav/clamonacc.log --move=/root/quarantine` (no enable line in postinst)
  - No unit in these three packages runs `clamscan`; `find` over the extracted trees found no `*clamscan*` timer or service.
- **Coverage.** T6: covers antivirus signature updates *when ClamAV is installed* (not in the Ubuntu seeds, S2-02): daemon `freshclam`, 24 checks/day default; resident `clamd`; no scheduled full scan shipped. Duration/size of an update: not covered. Other topics: no.
- **One observation?** No. Platform Ubuntu 24.04.

### S2-04 — Ubuntu 24.04 file indexers: tracker-miner-fs 3.7 (GNOME) and baloo (KDE)

- **Copies** (`../sources/S2-04/`, 2026-09-23): tracker-miner-fs_3.7.1-1ubuntu0.1_amd64.deb `573bdac5dbd64761fe88f48bf54204f6ceb9f9c2e785e96a2e02ea0866f5ae41`; tracker-extract_3.7.1-1ubuntu0.1_amd64.deb `808d8a0eb1cd5704db56d8e7b0e9a08a51f256004d3b42356904ad1650460ccc`; tracker_3.7.1-1build1_amd64.deb `cf0a8a341eed41e6e03f193c71c92d906e95be6c325f03982988259f85f356c5`; baloo-kf5_5.115.0-0ubuntu5_amd64.deb `008698bdb4096baabf1f1ee6e02f907cc0bd28ddfd48e961608f720009ac33e5`.
- **Verbatim passages.**
  - Noble `nautilus 1:46.4-0ubuntu0.2` `Depends:` (from `apt-cache show`, same archive index) includes `tracker (>= 3), tracker-miner-fs (>= 3), tracker-extract (>= 3)`.
  - `tracker-miner-fs: usr/lib/systemd/user/tracker-miner-fs-3.service:2,5,8-10,14,17` — `Description=Tracker file system data miner` / `After=gnome-session.target` / `Type=dbus` / `BusName=org.freedesktop.Tracker3.Miner.Files` / `ExecStart=/usr/libexec/tracker-miner-fs-3` / `Slice=background.slice` / `WantedBy=gnome-session.target`
  - `tracker-miner-fs: etc/xdg/autostart/tracker-miner-fs-3.desktop:4,8-9,14` — `Exec=/usr/libexec/tracker-miner-fs-3` / `X-GNOME-Autostart-enabled=true` / `X-GNOME-HiddenUnderSystemd=true` / `OnlyShowIn=GNOME;KDE;XFCE;X-IVI;Unity;`
  - Executables shipped: `usr/libexec/tracker-miner-fs-3`, `usr/libexec/tracker-miner-fs-control-3` (tracker-miner-fs); `usr/libexec/tracker-extract-3`, `usr/libexec/tracker-writeback-3` (tracker-extract).
  - `baloo-kf5: usr/lib/systemd/user/kde-baloo.service:2,3,6,8-12,15,18` — `Description=Baloo File Indexer Daemon` / `PartOf=graphical-session.target` / `ExecStart=/usr/lib/x86_64-linux-gnu/libexec/baloo_file` / `Slice=background.slice` / `ExecCondition=/usr/bin/kde-systemd-start-condition --condition "baloofilerc:Basic Settings:Indexing-Enabled:true"` / `# We'll basically only want to consume resources if they aren't needed anywhere else, hence weights are way low.` / `CPUWeight=1` / `IOWeight=1` / `MemoryHigh=512M` / `WantedBy=graphical-session.target`
  - `baloo-kf5: etc/xdg/autostart/baloo_file.desktop:3,5` — `Exec=/usr/lib/x86_64-linux-gnu/libexec/baloo_file` / `X-KDE-autostart-condition=baloofilerc:Basic Settings:Indexing-Enabled:true`
- **Coverage.** T6/T8: file-indexer processes started per user session without the user: GNOME `tracker-miner-fs-3` (+ `tracker-extract-3` on D-Bus activation), KDE `baloo_file`; cgroup weights for baloo. Executable basenames longer than 15 characters (`tracker-miner-fs-3`, 18 chars) are truncated in `/proc/<pid>/comm` per S2-11. No duration or indexing volume. Other topics: no.
- **One observation?** No. Platform Ubuntu 24.04.

### S2-05 — Fedora systemd presets (`redhat-systemd-presets` 102 on rawhide; `fedora-release` 43)

- **Citation.** Fedora dist-git `rpms/redhat-systemd-presets`, commit `7b91090183bfa0bf4820b30df397dd6dcfb065fc` (2026-07-16, spec `Version: 102`); `rpms/fedora-release` branch `f43`, commit `ce9c951bf62beea766f405774b4948687f153881` (2026-04-06, spec `Version: 43`).
- **Copies** (`../sources/S2-05/`, git clone 2026-09-23): 90-default.preset `8ea36fbbb750b42b648a5f7853c62fe2d9acda612bf22f75eae4fd0fe0e38bbb`; 90-default-user.preset `9260b5d161312f09ec24e13551be5a390e3bdf512a64d9afe9c7c874e52719c9`; 81-desktop.preset `091f9670c2c18a5d6a2030c55d05c2cc904a4763d1099a7e64eddc09efb01486`; 85-display-manager.preset `f9bd1a91e3b11b92b6a33604789dd7b6ed3fd883b7ae7371ecdad81b07f336db`; 99-default-disable.preset `3127b197b9eae62eb84eeed69b0413419612238332006183e36a3fba89578378`; 81-atomic-desktop.preset `2a3640c4ff967e916997b975272d4a5292df4e49f7900906d780aa8dab15d366`; f43/90-default.preset `85613d778de7a7b597620ed0010f16c9d05cff125eb6fef914134092d5490e40`; f43/90-default-user.preset `73c60a7416bc6aa2b2ab360b25c8320163b409f08117aefad3899e26adf70d30`.
- **Verbatim passages** (rawhide `90-default.preset`):
  - `:23-24` — `enable dbus.socket` / `enable dbus-broker.service`
  - `:181-182` — `# https://bugzilla.redhat.com/show_bug.cgi?id=928726` / `enable dnf-makecache.timer`
  - `:193-194` — `# https://bugzilla.redhat.com/show_bug.cgi?id=976315` / `enable dkms.service`
  - `:271-275` — `# https://bugzilla.redhat.com/show_bug.cgi?id=1231745` / `enable mlocate-updatedb.timer` / (blank) / `# https://src.fedoraproject.org/rpms/fedora-release/pull-request/204` / `enable plocate-updatedb.timer`
  - `:351` — `enable akmods.service`
  - `:385-386` — `# Run fstrim weekly on filesystems listed in fstab` / `enable fstrim.timer`
  - `:392-394` — `# Enable rotation of system log files` / `# https://bugzilla.redhat.com/show_bug.cgi?id=1655153#c4` / `enable logrotate.timer`
  - `:173` — `enable raid-check.timer`
  - `99-default-disable.preset:1` — `disable *`
  - `90-default-user.preset:5-6,10,16,21` — `enable dbus.socket` / `enable dbus-broker.service` / `enable pipewire.socket` / `enable pipewire-pulse.socket` / `enable wireplumber.service`
  - `f43/90-default.preset` has the same lines at `:24` (`dbus-broker.service`), `:176` (`dnf-makecache.timer`), `:188` (`dkms.service`), `:263` (`mlocate-updatedb.timer`), `:266` (`plocate-updatedb.timer`), `:342` (`akmods.service`), `:376-377` (fstrim), `:385` (logrotate).
  - `fedora-release.spec` (rawhide) `:113-114` — `# Handle the split between fedora-release-common and redhat-systemd-presets` / `Obsoletes: fedora-release-common < 45-0.3`
- **Coverage.** T6: Fedora's default-enable list (applies when the package is installed): dnf-makecache.timer, plocate-updatedb.timer, fstrim.timer, logrotate.timer, raid-check.timer, dkms.service, akmods.service; everything not listed is disabled. Whether plocate/dkms are in a default Fedora Workstation install is **not** covered by these files (comps not read). T8: Fedora uses dbus-broker for system and user bus; PipeWire + pipewire-pulse + WirePlumber enabled per user. Schedules are S2-06.
- **One observation?** No. Platform Fedora 43 and rawhide (45).

### S2-06 — Fedora/upstream unit definitions: plocate 1.1.25, dnf5 makecache, man-db

- **Copies** (`../sources/S2-06/`, 2026-09-23):
  - `plocate-1.1.25.tar.gz` from `https://plocate.sesse.net/download/plocate-1.1.25.tar.gz`, SHA-256 `68c1d5fbb11864403ae39c1a5937f13afd80b03e68041368831ef58cb613578e` (note: its SHA-512 `93d8abbe…` differs from the `ad0bb2df…` in Fedora `rpms/plocate` `sources`; the upstream tarball may have been regenerated — content quoted as fetched).
  - `fedora-rpms/plocate.spec` (rpms/plocate commit `c6bfe250093dbe6a8f240073430cd32ebd990e70`, 2026-09-07, `Version: 1.1.25`) `3333f310bf819e6b4e768ebed1f16291ce5b429268ed8ca8a0e67c40686d4e11`
  - `fedora-rpms/man-db-cache-update.service` (rpms/man-db `514425d19188d8bce926e8e071261c4f1533c562`, 2026-07-16, `Version: 2.13.1`) `909ac47ac04f63aa97b285e6ced6d66c5476b806b19da36f4174e5a01a8d86f5`; `man-db.spec` `735d951934012290ea9dfa18a86c4258e9a905e846488d2c97261173094e2817`
  - `fedora-rpms/dnf5-makecache.timer` `2d6d41a2f2429fb0b9690e015ca645fa3b70543582a35b820a02612593333bcd`, `dnf5-makecache.service` `d082e745a0555da1bdc4a1a985e47122a5bfda5a7f0a7e0f8319b7bb94f722ac`, `dnf5.spec` `a18ec0b297a240fb609edf92028a97adb9e036cf7522dc95347f51b381791c77` (dnf5 commit `bed397efabfe5f1040597c34b2335a00ef14e778`, 2026-09-22)
- **Verbatim passages.**
  - upstream `plocate-updatedb.timer:5-8` — `OnCalendar=daily` / `RandomizedDelaySec=1h` / `AccuracySec=6h` / `Persistent=true`
  - upstream `plocate-updatedb.service.in:6-9` — `ExecStart=@sbindir@/@updatedb_progname@` / `LimitNOFILE=131072` / `IOSchedulingClass=idle` / `Nice=19`
  - `plocate.spec:88-95` — `# The timer runs once per day. On new installs, let's start both the` / `# timer and the service immediately in the background, so that the db` / `# becomes populated. …` … `      systemctl start --no-block plocate-updatedb.timer plocate-updatedb.service || :`
  - `dnf5-makecache.timer:9-11` — `OnBootSec=10min` / `OnUnitInactiveSec=3h` / `RandomizedDelaySec=60m`
  - `dnf5-makecache.service:22,28-31` — `ConditionACPower=true` … `Nice=19` / `IOSchedulingClass=2` / `IOSchedulingPriority=7` / `ExecStart=/usr/bin/dnf5 makecache`
  - `dnf5.spec:1134-1136` — `# Make "dnf-makecache" the "real" unit name, but keep compatibility for playbooks that refer to dnf5-makecache` / `mv %{buildroot}%{_unitdir}/dnf5-makecache.service %{buildroot}%{_unitdir}/dnf-makecache.service` / `mv … dnf5-makecache.timer … dnf-makecache.timer`
  - Fedora `man-db-cache-update.service:8,10-11` — `ExecStart=/bin/sh -c '[ "$SERVICE" != "no" ] && /usr/bin/mandb $OPTS || true'` / `Nice=19` / `IOWeight=20` (Fedora ships no man-db timer; `man-db.spec:102-103` installs `/etc/cron.daily/man-db.cron` in the `man-db-cron` subpackage)
- **Coverage.** T6: Fedora schedules — dnf5 metadata refresh every 3 h after 10 min from boot (process `dnf5`), plocate daily (process `updatedb`, nice 19, idle I/O), and started immediately on first install; man-db cache update after package transactions. No durations. Other: no.
- **One observation?** No.

### S2-07 — Arch Linux packaging: plocate timer statically enabled; dbus-broker default; DKMS pacman hooks

- **Copies** (`../sources/S2-07/`, git clone of gitlab.archlinux.org 2026-09-23):
  - plocate (commit `eeaf360bddd443ea5799cbc5b80a2465d6729e87`, 2026-09-06, `pkgver=1.1.25 pkgrel=1`): PKGBUILD `c4eddece1b249f4526688e461034d1f8bdd415a1e83fd4ed0cfb322ed09cd748`; plocate-fix-updatedb.timer.patch `f519c901e2fb4195e25025a745db41c4167156be698738b198cbd5651cd9d9e6`
  - dbus-broker (commit `007302346bc4e1bc878b208047f27d86d620f39b`, 2026-02-14, `pkgver=37 pkgrel=3`): PKGBUILD `095df191116444cb7377c05d3d5d5168e50237729c647dfcf99deca9bc842fed`; 0001-units-Enable-statically.patch `20dcaf03d837d0715f71ccce3d393cba06a4b96f89f4fec3b6e35c1de0592d7d`
  - dkms (commit `1dc192d2318b11c7ded9aa6829f5bf29fe35ff4d`, 2026-08-17, `pkgver=3.4.3 pkgrel=2`): PKGBUILD `83658d2e8b6f058eecc9fe0c824af7233f1af4f8a01d50becdbe7393b8e3819a`; hook.install `da2dd53bdb427c3ffbe793fd05f898d8a0545e6dbd346c85fad1717b0f838c62`; hook.upgrade `cc04280e8eb095f4950f5e3c6b2997fbc8d5862d79c5ae29d5943b8ac204d0d4`; hook.sh `4fb4dded9f0b74f40e6543b6d05e7dc03712bd3ff1a2bd1f82f559a808060d10`
  - Arch news page `https://archlinux.org/news/making-dbus-broker-our-default-d-bus-daemon/` (HTTP 200) `arch-news-dbus-broker.html` `3bd27e3912a3e12944e3b622bdca64a8b0aabf48549567c92a1db57cd7588f17`
- **Verbatim passages.**
  - plocate `PKGBUILD:59-60` — `install -d "${pkgdir}/usr/lib/systemd/system/timers.target.wants"` / `ln -s ../plocate-updatedb.timer "${pkgdir}/usr/lib/systemd/system/timers.target.wants/plocate-updatedb.timer"`
  - plocate `plocate-fix-updatedb.timer.patch:5-11` removes `[Install]` / `WantedBy=timers.target` from the upstream timer (schedule lines kept: `RandomizedDelaySec=1h`, `AccuracySec=6h`, `Persistent=true`).
  - Arch news (2024-01-09, Jan Alexander Steffens): "We are making dbus-broker our default implementation of D-Bus, for improved performance, reliability and integration with systemd. For the foreseeable future we will still support the use of dbus-daemon , the previous implementation. Pacman will ask you whether to install dbus-broker-units or dbus-daemon-units . We recommend picking the default."
  - dbus-broker `PKGBUILD:108-112` — `package_dbus-units() {` / `  pkgdesc="D-Bus service units (default provider)"` / `  license=(CC0-1.0)` / `  depends=(dbus-broker-units)` / `}`
  - dbus-broker `0001-units-Enable-statically.patch:20-23` — `+install_symlink('dbus.service',` / `+        pointing_to: 'dbus-broker.service',` (same for user units at `:33-36`)
  - dkms `hook.install:1-13` — `[Trigger]` / `Operation = Install` / `Operation = Upgrade` / `Type = Path` / `Target = usr/src/*/dkms.conf` / `Target = usr/lib/modules/*/build/include/` / `Target = usr/lib/modules/*/modules.order` / (blank) / `[Action]` / `Description = Install DKMS modules` / `Depends = dkms` / `When = PostTransaction` / `Exec = /usr/share/libalpm/scripts/dkms install`
- **Coverage.** T6: on Arch, installing `plocate` enables its daily timer without `systemctl enable`; DKMS rebuilds run inside the pacman transaction when a kernel or its headers are installed/upgraded. T8: Arch default D-Bus implementation is dbus-broker (system and user bus, `dbus.service` alias). No durations.
- **One observation?** No. Platform Arch Linux (rolling, package versions named).

### S2-08 — GNOME LocalSearch (renamed tracker-miners): unit and process names, version of rename

- **Copies** (`../sources/S2-08/`, 2026-09-23): GNOME/localsearch commit `e406d768404b6cb3362ca086f7ee376e0f4478d9` (2026-09-19, `version: '3.12.0'`): NEWS `aa51076fe6fe076e53070f947d7a5ac2dad57bdee6efe91e4b481964d7d83a59`; `src/indexer/tracker-miner-fs.service.in` `aef73d13f1229fd9a494385078e7595dfe55b542579da0b859ccac53da4d7eb4`; `src/indexer/tracker-miner-fs.desktop.in` `4a673cb1981db9068222f3a1312f74308e67aec8898677c2ac93931378763dc1`; `src/indexer/meson.build` `ffb0bf81de53434d1de71440b02abe1b75ae2723f9d339a435577078ffc9677b`; `src/extractor/meson.build` (saved as extractor-meson.build) `94cc5d3581fa214dd7e059d283bcccd83bd5335564fce147a9ca0b7c299ff9ea`. Blog `https://blogs.gnome.org/carlosg/2024/07/14/goodbye-tracker-hello-tinysparql-and-localsearch/` (200) `96ac373c8fdc0ebb0edcf8180c9c95cc13d7a3dd9455e49c24c0d5e59abe4b62`.
- **Verbatim passages.**
  - Blog (Carlos Garnacho, 2024-07-14): "The Tracker Miners indexer will now be known as LocalSearch , or GNOME LocalSearch if you prefer."
  - `NEWS` "NEW in 3.8.alpha - 2024-07-04": "* Rename project to LocalSearch"; "NEW in 3.8.beta - 2024-08-09": "* Renamed command line tool"; "NEW in 3.8.0 - 2024-09-16" (translation updates only).
  - `src/indexer/tracker-miner-fs.service.in:2,5,8-12` — `Description=LocalSearch indexer` / `After=gnome-session.target` / `Type=notify` / `BusName=org.freedesktop.LocalSearch3` / `ExecStart=@libexecdir@/localsearch-3` / `Restart=on-failure` / `Slice=background.slice` (no `[Install]` section)
  - `src/indexer/meson.build:170-174` — `configure_file(` / `input: 'tracker-miner-fs.service.in',` / `output: 'localsearch-@0@.service'.format(tracker_api_major),` …; `:160-163` — `desktop_file = configure_file(` / `input: 'tracker-miner-fs.desktop.in',` / `output: 'localsearch-@0@.desktop'.format(tracker_api_major),`
  - `src/extractor/meson.build:178` — `executable('localsearch-extractor-@0@'.format(tracker_api_major),`
  - Ubuntu 26.04 package (S2-25) ships `usr/lib/systemd/user/localsearch-3.service` (same text, `ExecStart=/usr/libexec/localsearch-3`) and executables `localsearch-3`, `localsearch-control-3`, `localsearch-endpoint-3`, `localsearch-extractor-3`, `localsearch-writeback-3`.
- **Coverage.** T6/T8: GNOME indexer process names by version: `tracker-miner-fs-3` / `tracker-extract-3` up to 3.7 (Ubuntu 24.04, S2-04); `localsearch-3` / `localsearch-extractor-3` from 3.8 (2024-09, GNOME 47 cycle). `localsearch-extractor-3` is 23 characters → comm truncated to 15 (S2-11). No run durations.
- **One observation?** No.

### S2-09 — DKMS upstream (dell/dkms 3.4.3): kernel-install hook, dkms.service, parallelism

- **Copies** (`../sources/S2-09/`, git clone 2026-09-23, commit `00cd07431055fc7a1573235fcb93fbe185e726b2`, 2026-08-31; `Makefile:1-4` `RELEASE_DATE := "16 Aug 2026"`, 3.4.3): Makefile `4cb7e6a16251b375bf7a8ddc0469bfc156d0b6401c80815ebea92e61c7360003`; dkms.service.in `4d9b18547ce9dfffdf72cd3c91ae27a84528cf9c93e1d70abd7d052582a3d8e1`; redhat_kernel_install.d.in `bcc66a3934fbe1b98f94f1fe3380b5e4a088561a0b0115e804d8518863ecafd4`; dkms.in `7226bfe92b0e45826968ab419dcae67abc01557c5f72c9f1e32ece0de7038dfd`; dkms_framework.conf.in `6582c13c7b05046d1e7daa9ee7fced3def359904f680891e80125b44762d99f4`; debian_kernel_postinst.d.in `4b1852c3178c29d92b597a753186be13800c58d6628ddabbfcf27c2b12c0270e`; README.md `532642ad676af1703dfb794ff2b57c000b11cd1ccd8bca49bc46295632f9ab2c`.
- **Verbatim passages.**
  - `dkms.service.in:2,4,7-9,12` — `Description=Builds and install new kernel modules through DKMS` / `Before=network-pre.target graphical.target` / `Type=oneshot` / `RemainAfterExit=true` / `ExecStart=@SBINDIR@/dkms autoinstall --verbose --kernelver %v` / `WantedBy=multi-user.target`
  - `redhat_kernel_install.d.in:6-9` — `case "$COMMAND" in` / `    add)` / `        dkms kernel_postinst --kernelver "$KERNEL_VERSION"`
  - `dkms.in:3200-3209` — `kernel_postinst()` … `    have_one_kernel kernel_postinst` / (blank) / `    autoinstall`
  - `dkms.in:303-313` — `# Find out how many CPUs there are so that we may pass an appropriate -j` / `# option to make. Ignore hyperthreading for now.` / `get_num_cpus()` … `        nproc`
  - `dkms.in:1603` — `the_make_command="${make_command/#make/make -j$parallel_jobs KERNELRELEASE=$kernelver}"`; `:3628` — `parallel_jobs=${parallel_jobs:-$(get_num_cpus)}`
  - `dkms_framework.conf.in:54` — `# parallel_jobs=2`
- **Coverage.** T6: DKMS rebuild triggers — kernel-install `add` → `dkms kernel_postinst` → `autoinstall`; `dkms.service` (enabled in Fedora preset, S2-05) runs `autoinstall` at boot before `graphical.target`; builds use `make -j$(nproc)` by default. Object counts per module are S2-10. Duration of an autoinstall: **not** documented.
- **One observation?** No.

### S2-10 — Kbuild object lists of common DKMS modules (object counts)

- **Copies** (`../sources/S2-10/`, clones 2026-09-23):
  - v4l2loopback commit `e27cd86c924112ab1fb5e792a7ea43a37ab2903f` (2026-08-18; `dkms.conf:2` `PACKAGE_VERSION="0.15.4"`): Kbuild `fe95fd678781c0b3ebef6e2ea1b2bc5cd8c2e3a070e677ece54f8149cf9bf039`; dkms.conf `5c0f2bc0862a467b1d01659734a5c5f704db0695cad24197343dfa48f6febcc8`
  - NVIDIA/open-gpu-kernel-modules commit `61dcc93722ecb418bb5f2e00923f05b4b8051dd1` (2026-09-09; `version.mk` `NVIDIA_VERSION = 615.71.09`): kernel-open/Kbuild `95153be3…`, dkms.conf `edcec996c0ede26d902667860c39468d7928262bcad4a5a9aec1ee9a82b13c2b`, nvidia/nvidia-sources.Kbuild `4b4e6555a0865fc89dab5e49c91d8d1876a31a54565197d7c1402712f8eb389d`, nvidia/nvidia.Kbuild `6b2803664c904934bf92a24d55e5668aa82049b082972bce97d13b0ef390735b`, nvidia-uvm/nvidia-uvm-sources.Kbuild `17fbe3c6eded2dbfb28dd0f3866c796284f5bbc220f433973f52ab46eb0fe1e4`, nvidia-drm/nvidia-drm-sources.mk `3fa8c2cf04a7c4add6d18f6f4b0ccc8db6119585aad64fef3ccb8ab9a2aca439`, nvidia-drm/nvidia-drm.Kbuild `4b8af310c026fb1d6c91ced1c12e1bd317060b98e68a1788aa0b6f30826d4cb0`, nvidia-modeset/nvidia-modeset.Kbuild `4a401a144164a4394674f016bbb45075dc26f790c692f1af802866ce82d83cb2`, nvidia-peermem/nvidia-peermem.Kbuild `80cbee31baff0220c343d9752fb30692daec36c46a5a2764bee53d7265143bcb`, top-level Makefile `20f8635058c06cde6499b93d80d2b3556a316db010793a91e64110125cb31275`, src/nvidia/srcs.mk `df6843741ac1aa57fdd360a7151ae5e53960504b5f42619830326645a5ef7be9`, src/nvidia-modeset/srcs.mk `fd16c3010f7391789d1f896bd467afc94cdc74f9da074d774a22d23fc5be6b96`, README.md `c2ce63aedef8c6779e59fdc46596eaa4c4b97767dce888d85d99ce2790bfbb77`
  - openzfs/zfs commit `0d5bb1d010ae0cf85abcd88d7e8d9a330df615fd` (2026-09-22; META `Version: 2.4.99`): module/Kbuild.in `4c9316ffda868c1f288b50e09f5b133310753a5057c4cc88bc5769167dc3ae88`; META `f09aab5dfbea5116ce7a74264bb3f640cb833fe8eae2d54e81b3d2571319101c`
  - morrownr/88x2bu-20210702 commit `d31ffa827bb95b8a436c2a469b5163b634ac4333` (2026-09-11; `dkms.conf:2` `PACKAGE_VERSION="5.13.1"`): Makefile `6bb0c40902f5f73be4cb4cef435c20cd7105aa8efa64f89f27e054e34788e252`; dkms.conf `dfa232b8463437d180f2a1344eaffec7b83b6e850aaf54e86054f008339f3620`; dkms-make.sh `9b1b3036970b3f8e901b6d22d8d591d16812119c61f69335fe002053274bc79f`
  - VirtualBox/virtualbox commit `51b09acfb1905a9142e5ff1e1a64757b9250dcb1` (2026-09-22; `Version.kmk` 7.2.97): `src/VBox/HostDrivers/Support/linux/Makefile` `bc05124c6497869728321245ad7973f0e70259fb525584cd536d1763652a5b04`
- **Verbatim passages and counts** (counts are my tally of the quoted lists; method stated):
  - v4l2loopback `Kbuild:1` — `obj-m		:= v4l2loopback.o` → **1 object**.
  - NVIDIA `README.md:141-148` — "When packaged in the NVIDIA .run installation package, the OS-agnostic component is provided as a binary: it is large and time-consuming to compile, so pre-built versions are provided so that the user does not have to compile it during every driver installation.  For the nvidia.ko kernel module, this component is named "nv-kernel.o_binary". For the nvidia-modeset.ko kernel module, this component is named "nv-modeset-kernel.o_binary".  Neither nvidia-drm.ko nor nvidia-uvm.ko have OS-agnostic components." `README.md:150-151` — "The kernel interface layer component for each kernel module must be built for the target kernel."
  - NVIDIA `kernel-open/dkms.conf:9` — `MAKE[0]="'make' -j__JOBS NV_EXCLUDE_BUILD_MODULES='__EXCLUDE_MODULES' KERNEL_UNAME=${kernelver} modules"`
  - NVIDIA `nvidia/nvidia.Kbuild:40,48` — `NVIDIA_BINARY_OBJECT := $(src)/nvidia/nv-kernel.o_binary` … `nvidia-y += $(NVIDIA_BINARY_OBJECT_O)`
  - NVIDIA counts (lines matching `…_SOURCES += <file>.c`): `nvidia/nvidia-sources.Kbuild` **58**; `nvidia-uvm/nvidia-uvm-sources.Kbuild` **117**; `nvidia-drm/nvidia-drm-sources.mk` **19** + `nvidia-drm.Kbuild:9` `NVIDIA_DRM_SOURCES += nvidia-drm/nvidia-drm-linux.c` = **20**; `nvidia-modeset.Kbuild:9-10` (`nvidia-modeset-linux.c`, `nv-kthread-q.c`) **2**; `nvidia-peermem.Kbuild:10` **1** → **198 C files** in the kernel interface layer (plus the 2 prebuilt OS-agnostic objects). OS-agnostic trees, built only when building from this repository (`Makefile:34,46,58-59` — `$(MAKE) -C src/nvidia`, `$(MAKE) -C src/nvidia-modeset`, `modules: $(nv_kernel_o_binary) $(nv_modeset_kernel_o_binary)` / `$(MAKE) -C kernel-open modules`): `src/nvidia/srcs.mk` **1099** `SRCS += *.c|*.cpp` lines; `src/nvidia-modeset/srcs.mk` **184**.
  - ZFS `module/Kbuild.in:85` — `obj-$(CONFIG_ZFS) := spl.o zfs.o`; `:108` — `spl-objs += $(addprefix os/linux/spl/,$(SPL_OBJS))`; `:110` — `zfs-objs += avl/avl.o`; `:181,182,184` icp (`ICP_OBJS`, `_X86`, `_X86_64`); `:223` `@ZCP_ENABLED_TRUE@zfs-objs += $(addprefix lua/,$(LUA_OBJS))`; `:232` nvpair; `:258-259` zcommon (+`_X86`); `:314` `zfs-objs += $(addprefix zstd/,$(ZSTD_OBJS) $(ZSTD_UPSTREAM_OBJS))`; `:459` `	$(ZCP_OBJS)` (inside `ZFS_OBJS`); `:510-511` `zfs-objs += $(addprefix zfs/,$(ZFS_OBJS)) $(addprefix os/linux/zfs/,$(ZFS_OBJS_OS))` / `zfs-$(CONFIG_X86) += …ZFS_OBJS_X86`. Per-list `.o` counts: SPL 19; ICP 29, ICP_X86 3, ICP_X86_64 13; LUA 25; NVPAIR 4; ZCOMMON 13, ZCOMMON_X86 3; ZSTD 2 + ZSTD_UPSTREAM 22; ZCP 6; ZFS_OBJS 128 (list text; includes the `$(ZCP_OBJS)` reference, not counted as a `.o`); ZFS_OBJS_OS 33; ZFS_OBJS_X86 5; avl 1. **x86_64 total ≈ 19 (spl.ko) + 1+29+3+13+25+4+13+3+24+6+128+33+5 = 287 (zfs.ko) → ≈ 306 objects** when ZCP is enabled (arithmetic mine; the `ZCP_OBJS` inclusion via `:459` assumed as written).
  - Realtek 88x2bu `Makefile:2507,2512-2516,2524` — `$(MODULE_NAME)-y += $(rtk_core)` … `$(MODULE_NAME)-y += $(_OS_INTFS_FILES)` / `$(_HAL_INTFS_FILES)` / `$(_PHYDM_FILES)` / `$(_BTC_FILES)` / `$(_PLATFORM_FILES)` … `obj-$(CONFIG_RTL8822BU) := $(MODULE_NAME).o`. Evaluated with `make -pn KERNELRELEASE=6.8.0-generic ARCH=x86_64 CONFIG_RTL8822BU=m` (make's variable database only; nothing compiled): rtk_core 56, _OS_INTFS_FILES 15, _HAL_INTFS_FILES 47, _PHYDM_FILES 53, _BTC_FILES 3, _PLATFORM_FILES 1 → **175 objects** (all unique). `dkms-make.sh:10,13-16,23` — `sproc=$(nproc)` … `if [ "$SMEM" -lt 1400000 ]; then` / `sproc=2` … `make "-j$sproc" "KVER=$kernelver" "KSRC=/lib/modules/$kernelver/build"`.
  - VirtualBox vboxdrv `Makefile:42-50` — `VBOXMOD_NAME = vboxdrv` / `VBOXMOD_OBJS = \` / `linux/SUPDrv-linux.o` / `SUPDrv.o` / `SUPDrvGip.o` / `SUPDrvSem.o` / `SUPDrvTracer.o` / `SUPLibAll.o` / `common/string/strformatrt.o`; `:52-56` — `ifndef VBOX_WITHOUT_COMBINED_SOURCES` / `VBOXMOD_OBJS += \` / `combined-agnostic1.o` / `combined-agnostic2.o` / `combined-os-specific.o` → **10 objects** (default, combined sources); `:57-147` the uncombined alternative lists 89 more objects (+2 for amd64) → 98.
- **Coverage.** T6: objects compiled per DKMS rebuild of one module (static, from build definitions): v4l2loopback 1; vboxdrv 10 (default); Realtek 88x2bu 175; NVIDIA open kernel interface layer 198 C files (OS-agnostic part prebuilt in the .run package; ~1283 more files if built from source); ZFS ≈306 objects. T7: gives sizes to compare against a kernel build (kernel counts not read). No durations anywhere in these sources (the 88x2bu `install-driver.sh:415` only prints `"Compile time: %U seconds"` at run time).
- **One observation?** No (static source analysis at named commits; no machine).

### S2-11 — Linux `comm` length (15 characters + NUL)

- **Copies** (`../sources/S2-11/`): `https://raw.githubusercontent.com/torvalds/linux/v6.16/include/linux/sched.h` (200) `babe43bb5272615c75504736d7a56b7e1bea4d663cf9ec0f34888836dead03ef`; `https://man7.org/linux/man-pages/man2/PR_SET_NAME.2const.html` (200; colophon: "This page was obtained from the tarball man-pages-6.19.tar.gz") `4a0ec1dfc70b621c9b609c713042cb244a20c0ccd03e7617c6b52156d2d7630b`.
- **Verbatim passages.** `sched.h:314-319` — `/*` / ` * Define the task command name length as enum, then it can be visible to` / ` * BPF programs.` / ` */` / `enum {` / `	TASK_COMM_LEN = 16,`; `sched.h:1167` — `char				comm[TASK_COMM_LEN];`. PR_SET_NAME(2const), DESCRIPTION: "Set the name of the calling thread, using the value in the location pointed to by name. The name can be up to 16 bytes long, including the terminating null byte.  If the length of the string, including the terminating null byte, exceeds 16 bytes, the string is silently truncated."
- **Coverage.** T8/T5/T6: rule for the process/thread names appearing in `/proc/<pid>/comm`. Consequences (my derivation): `tracker-miner-fs-3` → `tracker-miner-f`; `dbus-broker-launch` → `dbus-broker-lau`; `localsearch-extractor-3` → `localsearch-ext`.
- **One observation?** No.

### S2-12 — Mutter (GNOME compositor): Xwayland on demand; X11 backend removal

- **Copies** (`../sources/S2-12/`, blob-less clone of gitlab.gnome.org/GNOME/mutter 2026-09-23, commit `888a7b7dac0c58612007c46bbad75de9f9437f48`, 2026-09-17, `version: '51.0'`): NEWS `ced8911278483c281ea026cc6fd84f5c93e3119aa0f0381e0a9e6d461e80036a`; src/core/meta-context-main.c `21c0bd4c87b73ff5ed142abebd64d80af2982f09ee474d441fadfc8fb1bde7d6`; data/org.gnome.mutter.gschema.xml.in `a55eb5719bf02df81d44e63c2d3ff06f8579185120b77f3c14ba8bdc954ec253`.
- **Verbatim passages.**
  - `NEWS:2058` (section "40.beta", line 2053) — `* Default to starting Xwayland on demand [Olivier; !1673]`
  - `NEWS:2030` (section "40.rc", line 2014) — `* Only start XWayland on demand when running under systemd [Benjamin; !1771]`
  - `NEWS:573` (section "49.alpha.0", line 528) — `* Disable X11 backend by default [Jordan; !4454]`; `NEWS:557` — `* Drop x11 session restore [Bilal; !4438]`
  - `NEWS:308` (section "50.alpha", line 303) — `* Drop the X11 backend [Bilal; !4505]`
  - `meta-context-main.c:128-141` — `meta_context_main_get_x11_display_policy (MetaContext *context)` … `  if (context_main->options.no_x11)` / `    return META_X11_DISPLAY_POLICY_DISABLED;` / (blank) / `  if (sd_pid_get_user_unit (0, &unit) < 0)` / `    return META_X11_DISPLAY_POLICY_MANDATORY;` / `  else` / `    return META_X11_DISPLAY_POLICY_ON_DEMAND;`
- **Coverage.** T8: GNOME Shell (mutter) sessions since GNOME 40 start Xwayland only when an X11 client needs it (when gnome-shell runs as a systemd user unit); GNOME 49 disabled and GNOME 50 removed mutter's X11 backend, i.e. no GNOME-on-Xorg session from GNOME 50. Process names (`gnome-shell`, `Xwayland`) not stated in these files. No observation.
- **One observation?** No.

### S2-13 — PipeWire, WirePlumber and dbus-broker upstream user units

- **Copies** (`../sources/S2-13/`, clones 2026-09-23): pipewire commit `3528a90d5484ea0d1d032697b4d0d22d2ce620e5` (2026-09-22, `version : '1.7.0'`): pipewire.service.in `758ffe661c516331e2e8106dbfe3dac8d51e729e76e854934c9b8832e65cc7c1`, pipewire.socket `0314a8abf591bc159e8af842a627917bb99f78f8bd8fee6f5e0f9157ca9da208`, pipewire-pulse.service.in `2ffb6b2661064aafacc2c967de6e7ecd859ec2043242aa81c2bd21d863566b83`, pipewire-pulse.socket `c3abbf9ac1fdd17c252dafbf40293cde60fdf11b545b79cef48129e632bcf414`; wireplumber commit `1647f93bea1053d085df8cd60d3e2d7b0f46e7eb` (2026-09-22, `version : '0.5.17'`): wireplumber.service.in `8f12d8e81dd8db9e375817721cdbad4384bc722497f95e8de65da2666123b427`; dbus-broker commit `2956b5d381deeea709c53d02f10e799e50e44f4b` (2026-07-02, `version: '37'`): src/units/user/dbus-broker.service.in (saved dbus-broker-user.service.in) `4e4679992971405d267781d445280c7340b2bbbdfbc23ef402694dbd707b5feb`, system unit `847f1b0f0405e42111cd7cde483c0527aacdb7b19f9afd0afc30986207865371`. systemd `units/user@.service.in` at commit `f30c9ea09c1ca4ca0da330537cd00f421fd851f3` (`meson.version` `263~devel`) in `../sources/S2-26/` `72c2f40dcfced1d85bcc17583715966fc8a552b68af44404c213de2ea320504c`.
- **Verbatim passages.**
  - `pipewire.service.in:2,26,28,32` — `Description=PipeWire Multimedia Service` … `ExecStart=@PW_BINARY@` … `Slice=session.slice` … `WantedBy=default.target`
  - `pipewire.socket:7-8` — `ListenStream=%t/pipewire-0` / `ListenStream=%t/pipewire-0-manager`
  - `pipewire-pulse.service.in:2,18,31` — `Description=PipeWire PulseAudio` … `Wants=pipewire.service pipewire-session-manager.service` … `ExecStart=@PW_PULSE_BINARY@`
  - `wireplumber.service.in:2,4,14,20-21` — `Description=Multimedia Service Session Manager` / `BindsTo=pipewire.service` … `ExecStart=@WP_BINARY@` … `WantedBy=pipewire.service` / `Alias=pipewire-session-manager.service`
  - `dbus-broker user unit :5,17-18,21` — `Description=D-Bus User Message Bus` … `ExecStart=@bindir@/dbus-broker-launch --scope user` / `Slice=session.slice` … `Alias=dbus.service`
  - `user@.service.in:11,23` — `Description=User Manager for UID %i` … `ExecStart={{LIBEXECDIR}}/systemd --user`
- **Coverage.** T8: per-user always-on processes of a modern session: `systemd --user`, `pipewire`, `pipewire-pulse`, `wireplumber`, bus launcher `dbus-broker-launch` (+ its child `dbus-broker`, `launcher.c:294` names `"dbus-broker"`), all socket/dependency activated at login. No resource numbers.
- **One observation?** No.

### S2-14 — Ubuntu 24.04 session stack packaging (GDM Wayland default, dbus-daemon, X11 session still shipped)

- **Copies** (`../sources/S2-14/`, `apt-get download` 2026-09-23): gdm3_46.2-1ubuntu1~24.04.9_amd64.deb `d23b6242076fc4cd7e753db0f535d2500371109ab4e2c1ef002db1221fa3f27e`; dbus_1.14.10-4ubuntu4.1_amd64.deb `0d59be1393d5b01552edbf16c7b9357c473bf625aa47365ce2e8eef6da1dd2e1`; dbus-user-session_1.14.10-4ubuntu4.1_amd64.deb `e585b1694b854c3b75bfb39cc4022cafe7b14e44fd435433b613b8fb9919cb41`; dbus-broker_35-2ubuntu0.1_amd64.deb `1ff0c0a99b3f98dcdd9d88264740bdab4f3a1362ffe2e5ce42cfeb480fb80994`; pipewire_1.0.5-1ubuntu3.3_amd64.deb `cfcbfe39dfbba3e6e906f930ee7f59294dedb418a8fc758e73bb2728084e6e13`; pipewire-pulse_1.0.5-1ubuntu3.3_amd64.deb `b7ccd7f1c5608523a74293ca037e3f84a1149e740e483a23d820632bceb2998c`; wireplumber_0.4.17-1ubuntu4.1_amd64.deb `14d3aacef9850d5c3b82d1f225743b776a4619deb34f1089bcd21996cb131832`; sddm_0.20.0-2ubuntu4.2_amd64.deb `a161eb751cb1ab1cfbb21f8682f6591251651e155b8c97e8743a9423f359d0a1`; ubuntu-session_46.0-1ubuntu4_all.deb `21aa657e0660bd3f15f6017508cffc141351cd9009e8cf9515b01c488e23f509`.
- **Verbatim passages.**
  - `gdm3: etc/gdm3/custom.conf:6-7` — `# Uncomment the line below to force the login screen to use Xorg` / `#WaylandEnable=false`
  - `ubuntu-session 46.0-1ubuntu4` ships both `./usr/share/wayland-sessions/ubuntu.desktop` and `./usr/share/xsessions/ubuntu.desktop` (+ `ubuntu-xorg.desktop`, `ubuntu-wayland.desktop`); both `ubuntu.desktop` files `:4` — `Exec=env GNOME_SHELL_SESSION_MODE=ubuntu /usr/bin/gnome-session --session=ubuntu`
  - `dbus 1.14.10-4ubuntu4.1` `Priority: standard`; `Depends: dbus-bin (= 1.14.10-4ubuntu4.1), dbus-daemon (= 1.14.10-4ubuntu4.1), …`; `dbus-user-session` `Depends: dbus-daemon (= 1.14.10-4ubuntu4.1) | dbus-broker, …`; `dbus-broker 35-2ubuntu0.1` `Priority: optional`.
  - `pipewire DEBIAN/postinst:37-40` — `if deb-systemd-helper --quiet --user was-enabled 'pipewire.service' ; then` … `deb-systemd-helper --user enable 'pipewire.service' >/dev/null || true`
- **Coverage.** T8: Ubuntu 24.04 GNOME: login screen Wayland unless disabled; Xorg session still installed and selectable; message bus is dbus-daemon (dbus-broker only as an alternative); PipeWire user service enabled globally. Kubuntu 24.04's *default* session type (X11 vs Wayland) is **not** established by these files (sddm package does not state it).
- **One observation?** No.

### S2-25 — Ubuntu 26.04 LTS (resolute) packaging: GNOME Wayland-only, LocalSearch, dbus

- **Copies** (`../sources/S2-25/`, archive.ubuntu.com pool, 2026-09-23; index `dists/resolute/Release` `Version: 26.04`, `Date: Thu, 23 Apr 2026 17:07:15 UTC`): ubuntu-desktop-minimal_1.570.3_amd64.deb `fba2c0b58d1a82f7137368166c61c8b77ffdf14c6d4a94184f76c84860bece46`; ubuntu-desktop_1.570.3_amd64.deb `57979833ba7f2dd694bcf1219e5599008833ded082081ed9fb1647e775826d1c`; kubuntu-desktop_1.496_amd64.deb `e610d50fd4a87c936d120e57af308b32873f2619d90e48dddb89dc124998b23e`; localsearch_3.11.0-1ubuntu1.1_amd64.deb `0d1e647e655f9fa749515fa0aad656b2f700e3914c9e70eee6adb44be7b93da2`; plocate_1.1.23-1ubuntu3_amd64.deb `474c2cd99b3fe93eecd68e45974bcf39677bf8ac752344173a096974981e5051`; gdm3_50.1-0ubuntu0.1_amd64.deb `6d979c79ce3492236e9a2467c5a11e4f5355f087f08ca0dfc0e0e3320b5d2aae`; gnome-session_50.1-0ubuntu0.1_all.deb `3425c8e260ca89df3a136b3b55ff372effe306fa5d0ac6981371d0932944ca44`; ubuntu-session_50.1-0ubuntu0.1_all.deb `3ff88b755bb2dd2d9944c6a5613adc840444db166057a0880b803a0d76203c96`.
- **Verbatim passages / facts from the files.**
  - `ubuntu-session 50.1-0ubuntu0.1` file list: `./usr/share/wayland-sessions/ubuntu.desktop`, `./usr/share/gnome-session/sessions/ubuntu.session`, `./usr/lib/systemd/user/gnome-session@ubuntu.target.d/ubuntu.session.conf` — **no** `usr/share/xsessions/` entry (24.04 had two, S2-14). `gnome-session 50.1` likewise only `usr/share/wayland-sessions/gnome.desktop` (`:4` `Exec=/usr/bin/gnome-session --session=gnome`).
  - `ubuntu-desktop-minimal 1.570.3` Depends/Recommends contain `pipewire-pulse`, `wireplumber`, `fwupd`, `fwupd-signed` and **no** `xorg` (24.04 `1.539.2` had `xorg` in Depends).
  - `kubuntu-desktop 1.496` Depends/Recommends contain `kwin-wayland`, `pipewire`, `pipewire-audio`, `baloo6`, `dbus-x11`, `plocate`, `wireplumber`.
  - resolute `nautilus` `Depends:` contains `localsearch` and `libtinysparql-3.0-0 (>= 3.8.1)`.
  - `localsearch: usr/lib/systemd/user/localsearch-3.service:2,10,12` — `Description=LocalSearch indexer` / `ExecStart=/usr/libexec/localsearch-3` / `Slice=background.slice`.
  - `plocate 1.1.23-1ubuntu3: usr/lib/systemd/system/plocate-updatedb.timer:5-8` — `OnCalendar=daily` / `RandomizedDelaySec=1h` / `AccuracySec=6h` / `Persistent=true`; `DEBIAN/postinst:42` — `deb-systemd-helper enable 'plocate-updatedb.timer' >/dev/null || true`.
  - Index entries: `dbus 1.16.2-2ubuntu4 Priority: important`, `dbus-user-session … Priority: important`, `dbus-broker 37-5` in universe `Priority: optional`.
- **Coverage.** T8: Ubuntu 26.04 GNOME ships no Xorg session (Wayland + on-demand Xwayland per S2-12); message bus still dbus-daemon by default. T6: GNOME indexer is `localsearch-3`; Kubuntu 26.04 still pulls plocate (daily timer, now 1 h randomized delay vs 12 h in 24.04). 26.04 timers other than plocate were not re-read (assumed unchanged — not verified).
- **One observation?** No.

### S2-15 — Chromium process model and renderer-process limit (Chromium 156.0.8070.0, main @ 86098b06)

- **Citation.** Chromium `src` at commit `86098b063d52985b42f3f0e2ff45ca039ff533f5` (committer time 2026-09-23 04:14:54; `chrome/VERSION` `MAJOR=156 MINOR=0 BUILD=8070 PATCH=0`).
- **Copies** (`../sources/S2-15/`, chromium.googlesource.com `?format=TEXT`, base64-decoded, 2026-09-23): process_model_and_site_isolation.md `5a371fa56628822f38946d32ef5ce291e07ff74c1fb5a53b1eaac0249fe41bab`; render_process_host_impl.cc `1b97e4a23e849ac9f118781345d2df80de662b6edeb2558db277f74008157bcd`; render_process_host.h `5a836e13c677ad5bfa3c0e41d91ba460ac496d51be3627f0ae03b9f50deb0f42`; content_features.cc (content/public/common) `443f06e92afae6b013a3b233f019e41fd1adf0aa50377c83a198acc4ad922ad0`; common_features.cc (content/common/features.cc) `c005bb473c3b8f8049e0383713e3988f8ecce7977adf89f7ee0b4066ecb5b78f`; platform_thread_linux.cc `f1cbba5b3d7edbe2e3561d558bcf18e7af5c0ebe1cc38335e20381f5d2dd918d`.
- **Verbatim passages.**
  - `docs/process_model_and_site_isolation.md:141-150` — "### Full Site Isolation (site-per-process)" / "_Used on: Desktop platforms (Windows, Mac, Linux, ChromeOS)._" / "In (one-)site-per-process mode, each process is locked to documents from a single site. Sites are defined as scheme plus eTLD+1, since different origins within a given site may have synchronous access to each other if they each modify their document.domain."
  - `:322-331` — "* **Soft Process Limit**: On desktop platforms, Chromium sets a "soft" process limit based on the memory available on a given client. While this can be exceeded (e.g., if Site Isolation is enabled and the user has more open sites than the limit), Chromium makes an attempt to start randomly reusing same-site processes when over this limit. For example, if the limit is 100 processes and the user has 50 open tabs to `example.com` and 50 open tabs to `example.org`, then a new `example.com` tab will share a process with a random existing `example.com` tab, while a `chromium.org` tab will create a 101st process. Note that Chromium on Android does not set this soft process limit, and instead relies on the OS to discard processes."
  - `:332-342` — "* **Aggressive Reuse**: For some cases (including on Android), Chromium will aggressively look for existing same-site processes to reuse even before reaching the process limit. Out-of-process iframes (OOPIFs) and [fenced frames](…) use this approach, such that an `example.com` iframe in a cross-site page will be placed in an existing `example.com` process (in any browsing context group), even if the process limit has not been reached."
  - `:343-349` — "* **Extensions**: Chromium ensures that extensions do not share a process with each other or with web pages, but also that a large number of extensions will not consume the entire soft process limit, … Chromium only allows extensions to consume [one third](…) of the process limit before disregarding further extension processes from the process limit computation."
  - `:476-479` — "* **Spare Process**: Chromium often creates a spare RenderProcessHost with a live but unlocked renderer process, which is used the next time a renderer process is needed. This avoids the need to wait for a new process to start."
  - `render_process_host_impl.cc:1535-1552` — "  // On other platforms, calculate the maximum number of renderer process hosts / // according to the amount of installed memory as reported by the OS, along / // with some hard-coded limits. The calculation assumes that the renderers / // will use up to half of the installed RAM and assumes that each WebContents / // uses |kEstimatedWebContentsMemoryUsage| MB. … //   128 MB -> 0 / //   512 MB -> 3 / //  1024 MB -> 6 / //  4096 MB -> 24 / // 16384 MB -> 96"
  - `:1558-1574` — `static constexpr size_t kEstimatedWebContentsMemoryUsage =` / `#if defined(ARCH_CPU_64_BITS)` / `        85;  // In MB` … `max_count = base::SysInfo::AmountOfTotalPhysicalMemory().InMiB() / 2;` / `max_count /= kEstimatedWebContentsMemoryUsage;` … `static constexpr size_t kMinRendererProcessCount = 3;` … `max_count = std::clamp(max_count, kMinRendererProcessCount,` / `                           kMaxRendererProcessCount);`
  - `:1486-1494` — `// Set the limit to half of the system limit to leave room for other programs.` / `size_t limit = GetPlatformProcessLimit() / 2;` … `static constexpr size_t kMaxRendererProcessCount = 82;`; `:1205-1209` (Linux) — `if (getrlimit(RLIMIT_NPROC, &limit) != 0)` … `if (limit.rlim_cur == RLIM_INFINITY)` / `    return std::numeric_limits<size_t>::max();`
  - `:5286-5307` — `size_t process_count = RenderProcessHostImpl::GetProcessCountForLimit();` / `if (process_count >= GetMaxRendererProcessCount()) {` … `    if (base::FeatureList::IsEnabled(features::kRemoveRendererProcessLimit)) {` … `      size_t sys_limit = GetPlatformProcessLimit();` / `      if (sys_limit == kUnknownPlatformProcessLimit) {` / `        return false;` / `      }` / `      return process_count >= sys_limit;`
  - `content/common/features.cc:365-367` — `// A feature to experiment with removing the soft process limit. See` / `// https://crbug.com/369342694.` / `BASE_FEATURE(kRemoveRendererProcessLimit, base::FEATURE_ENABLED_BY_DEFAULT);`
  - `content/public/common/content_features.cc:1189-1191` — `// spare renderer process around for the most recently requested BrowserContext.` / `// This feature is only consulted in site-per-process mode.` / `BASE_FEATURE(kSpareRendererForSitePerProcess, base::FEATURE_ENABLED_BY_DEFAULT);`
  - `base/threading/platform_thread_linux.cc:212-226` — `// On linux we can get the thread names to show up in the debugger by setting` / `// the process name for the LWP.  We don't want to do this for the main` / `// thread because that would rename the process, causing tools like killall` / `// to stop working.` … `// Set the name for the LWP (which gets truncated to 15 characters).` … `int err = prctl(PR_SET_NAME, name.c_str());`
- **Coverage.** T4: renderer processes on Linux desktop ≈ one per distinct site (scheme+eTLD+1) across top-level tabs, plus cross-site iframes placed in (reused) same-site processes, plus extension processes, plus one spare renderer; soft limit = clamp(RAM_MiB/2/85, 3, RLIMIT_NPROC/2) (e.g. 96 at 16 GiB) — but at this commit `kRemoveRendererProcessLimit` is enabled by default, so on Linux reuse beyond the soft limit is only forced at `RLIMIT_NPROC`. Whether that default is in a *stable* release is not established here (main branch). Tab counts / page-load rates of real users: not covered. T8/T5: Chromium keeps the main-thread comm (process name) and names other threads via `PR_SET_NAME`.
- **One observation?** No (source at one commit).

### S2-16 — Firefox content-process prefs and tab/window telemetry probe definitions (Firefox 158.0a1)

- **Copies** (`../sources/S2-16/`, raw.githubusercontent.com `mozilla-firefox/firefox@281872e7df7b7d31f0090788d747d44e5d124874`, 2026-09-23; `browser/config/version.txt` = `158.0a1`, SHA-256 `798da2fb…`): modules_libpref_init_all.js `aabdef32220886689acaa3cdf65c90e4f15a2b0eb91299ff2ff68a0a9f1f7dca`; modules_libpref_init_StaticPrefList.yaml `356a429e4b476df594f4bbe5a7060e6b6d6aad00dc4c4770935898648b5242db`; toolkit_components_telemetry_Scalars.yaml `37a62accf01c330489b74b4601382cfdc53e8c15bd915b6dc3def9a36243578d`; browser_components_metrics.yaml `3a3d40f217827f2062c94b147b0c039812fdfb1ea378c8dd1708dc22720a79f5`; browser_app_profile_firefox.js `cf274eba36257087c81f4cf4d93be99f9e1b9fcf9eb23ac649e28350e9b97b12`. Also `mozilla/firefox-public-data-report-etl` README (commit `61b337ec7b72c956ced0f9bdc2bf3e54ec22d336`, 2026-05-19) `fx-public-data-report-etl-README.md` `bcf928833b3f90ecbb86e18824c673a54f5ae3d6a79a4beccb1ec1d444ec1c0c`.
- **Verbatim passages.**
  - `all.js:1860-1867` — `// Enable multi by default.` / `#if !defined(MOZ_ASAN) && !defined(MOZ_TSAN)` / `  pref("dom.ipc.processCount", 8);` …
  - `all.js:1882-1887` — `// Maximum number of isolated content processes per-origin.` / `#ifdef ANDROID` / `pref("dom.ipc.processCount.webIsolated", 1);` / `#else` / `pref("dom.ipc.processCount.webIsolated", 4);` / `#endif`
  - `all.js:1869-1880` — `pref("dom.ipc.processCount.file", 1);` … `pref("dom.ipc.processCount.extension", 1);` … `pref("dom.ipc.processCount.privilegedabout", 1);` … `pref("dom.ipc.processCount.privilegedmozilla", 1);`
  - `StaticPrefList.yaml:6784-6786` — `- name: fission.autostart` / `  type: bool` / `  value: true`
  - `Scalars.yaml:361-372` — `  max_concurrent_tab_count:` … `      The count of maximum number of tabs open during a subsession,` / `      across all windows, including tabs in private windows and restored` / `      at startup.` / `    expires: never` / `    kind: uint` … `    release_channel_collection: opt-out`
  - `Scalars.yaml:394-400` — `  tab_open_event_count:` … `      The count of tab open events per subsession, across all windows, after the` / `      session has been restored. …`
  - `Scalars.yaml:427-432` — `  max_concurrent_window_count:` … `      The count of maximum number of browser windows open during a subsession. This` / `      includes private windows and the ones opened when starting the browser.`
  - `Scalars.yaml:530-538` — `  total_uri_count:` … `      The count of the total non-unique http(s) URIs visited in a subsession, including` / `      page reloads, after the session has been restored. URIs on minimized or background` / `      tabs may also be counted towards this. Private browsing is not included in this` / `      count.`
  - `Scalars.yaml:595-603` — `  unique_domains_count:` … `      The count of the unique domains visited in a subsession, … The count is limited to 100 unique domains.`
  - ETL `README.md:19-29` — "User Activity (`fxhealth.json`): * Monthly Active users (MAU) … * Average daily usage hours … * Average intensity … * New profile rate … * Latest version ratio …" / "Usage Behavior (`webusage.json`): * Top languages … * Has Add-on … * Top Add-ons …" (no tab, window or URI metric listed).
- **Coverage.** T4: Firefox Fission defaults — per-site-origin isolated content processes up to 4 per origin (`webIsolated`), 8 shared web processes (`processCount`), 1 extension/file/privileged process each. Telemetry *definitions* exist for per-subsession max tabs, max windows, tab opens, total URIs, unique domains (opt-out on release), but the public data report publishes none of them — no aggregate available from this source. T12: points to non-public telemetry.
- **One observation?** No.

### S2-17 — Valve Steam Support: downloads during gameplay

- **Copies** (`../sources/S2-17/`, 2026-09-23): `https://help.steampowered.com/en/faqs/view/4F9E-6328-E9B8-47F9` (200) `faq-4F9E.html` `e2994a50694a87c7e1fa20d44f46a8c6b7e18fa09290f0a5ec40fad518d618e5`; `https://help.steampowered.com/en/faqs/view/71AB-698D-57EB-178C` (200) `faq-71AB.html` `021c1d9e3fc56ff2919953fc2a08f0d804f724faaa346781efd95b69c18b1742`. Article body is in the page's JSON `data-` attribute (`"timestamp":1625946595` = 2021-07-10 for 4F9E; `"timestamp":1727216103` = 2024-09-24 for 71AB).
- **Verbatim passages.**
  - 4F9E, title "Downloads automatically pause when launching a game": "Steam automatically pauses your downloads when a game is launched in order to prioritize the network activity for the game itself. You can turn this feature off by navigating to your download settings: [i]Steam > Settings > Downloads[/i]. From here, check the [i]Allow Downloads During Gameplay[/i] box."
  - 71AB, "Managing Steam Downloads & Updates": "Steam will automatically download updates for your games based on the Steam client's download settings." … "Games are automatically put into your download queue when a game releases an update." … "There's also a per-game setting to allow/prevent the downloading of other updates while you're playing." … "You can also limit the times during the day when Steam updates your games. From your downloads settings ([i]Steam > Settings > Downloads[/i]) check the [i]Only auto-update games[/i] box and specify the time when Steam should perform auto-updates."
- **Coverage.** T5: default — Steam pauses downloads while a game runs (setting "Allow Downloads During Gameplay" off by default is implied by "check … to turn this feature off"); per-game override. Not Linux-specific (applies to the client generally); no statement of how often updates arrive or their size.
- **One observation?** No.

### S2-18 — Steam Linux Runtime docs: process wrapping of a game (reaper, steam-launch-wrapper, pressure-vessel)

- **Copies** (`../sources/S2-18/`, git clone gitlab.steamos.cloud/steamrt/steam-runtime-tools, commit `9e55eb6240c3a238ebde0ccb90cd6f5e37d17fd2`, 2026-09-22): docs/steam-compat-tool-interface.md `3d1fbf262e39705ab8460ff7b352625c8764d9d1b4b5356152f5f406c54af8ea`; docs/steam-runtime-emulator.json.5.md `8428e0f3bd5f43ee65fd0eb81ea9c565fb3c8233ff909c6673495ffaaa384b50`; pressure-vessel/adverb.1.md `abc7899ff264aa3e9810ceceb3db8a9c817fa9f127a75e95c13d77f7699a26ad`.
- **Verbatim passages.**
  - `steam-compat-tool-interface.md:528-530` — "In recent versions of Steam, the game process is wrapped in a `reaper` process which sets itself as a subreaper using `PR_SET_CHILD_SUBREAPER`"
  - `:189-198` — "If a compatibility tool has `require_tool_appid` set, then the command-line is built up by taking the required tool, then appending the tool that requires it, and finally appending the actual game: … `/path/to/Outer/run waitforexitandrun -- \` / `/path/to/Inner/run waitforexitandrun -- \` / `/path/to/game.exe`"
  - `:517-522` — "For example, when using Proton with "Steam Linux Runtime 2.0 (soldier)", the "outer" compatibility tool "Steam Linux Runtime 2.0 (soldier)" is run with `LD_LIBRARY_PATH` set by the Steam Runtime … After setting up the container, it runs the "inner" compatibility tool (Proton) …"
  - `:675-678` — "The compat tool is expected to terminate any background processes (for example pressure-vessel terminates the container and Proton terminates the `wineserver`) and wait for them to exit, then launch the actual game."
  - `steam-runtime-emulator.json.5.md:315-321` — "and then using an exec chain that is similar to what it would do for an x86 game on x86 or an aarch64 game on aarch64:" / `"…/steam-launch-wrapper" … -- \` / `"…/reaper" SteamLaunch … -- \` / `"…/SteamLinuxRuntime_sniper/_v2-entry-point" --verb=waitforexitandrun -- \` / `"/path/to/game/executable"`
  - `adverb.1.md:46-58` — "**pv-adverb** acts as the top-level process inside a Steam Linux Runtime container (the direct child of **bwrap**(1)) with any other processes that will run inside the container, for example a game or an interactive shell, as its children. … **pv-adverb** acts as a subreaper."
- **Coverage.** T5: documented process chain for a Steam game on Linux: `steam-launch-wrapper` → `reaper SteamLaunch` → `_v2-entry-point` (SteamLinuxRuntime_sniper) → pressure-vessel → `bwrap` → `pv-adverb` → (Proton) → game; `wineserver` for Proton games. Comm names of these (e.g. `steam-launch-wr` after truncation) are derivations, not in the docs. Number of threads: not covered.
- **One observation?** No.

### S2-19 — Proton 11.0 launch script and Wine 11.18 process/thread naming

- **Copies** (`../sources/S2-19/`, 2026-09-23): `proton-proton.py` = `proton` from ValveSoftware/Proton branch `proton_11.0`, commit `5b89db940e0ebe3a137a6009a3589232fe084c09` (2026-09-04) `787504a79bacf6b303984a9a846cf47463f36599248e8306b26d5faf78267aad`; Wine from `wine-mirror/wine@df15af3652511150490934682202d45af892f887` (2026-09-22; `VERSION` = "Wine version 11.18", `77fff8d6…`): wine-thread.c `0db3d5d025a7571d7370b3268bb52e52214e6a2c9c02dee5ef9d7c2c5c20af0d`; wine-env.c `eac82bd2769b1622dd2d308169f9e1750c41169640656e832eb1f8992248396f`; wine-wineboot.c `f60dc3396d6d314aabee35712726c8a4db97c94723929719c62137bd46c0abd2`; wine-services.c `81396ab7263fc2d301ee0b1ca9db526223976579e207b5c49cfb4eccce51a2fa`; wine-loader.c `b4adcaab240ecca26305f212894597b6250a253f181f0861ba67e7a3376d24fa` (not quoted). Caveat: this is upstream Wine, not Proton's Wine fork (`ValveSoftware/wine`), which was not read.
- **Verbatim passages.**
  - `proton:2076-2083` — `argv = [g_proton.wine_bin, "c:\\Program Files (x86)\\Steam\\steam.exe"]` … `argv = [g_proton.lib_dir + "/wine/x86_64-unix/wine-preloader", g_proton.lib_dir + "/wine/x86_64-unix/wine", "c:\\windows\\system32\\steam.exe"]`
  - `proton:2126-2130` — `    elif sys.argv[1] == "waitforexitandrun":` / `        #wait for wineserver to shut down` / `        g_session.run_proc([g_proton.wineserver_bin, "-w"])` / `        #then run` / `        rc = g_session.run()`
  - `proton:1477` — `"steam.exe": "b", #always use our special built-in steam.exe`
  - `wine env.c:487-504` — `static void set_process_name( const char *name )` … `    if ((p = strrchr( name, '\\' ))) name = p + 1;` / `    if ((p = strrchr( name, '/' ))) name = p + 1;` … `    prctl( PR_SET_NAME, name );`
  - `wine thread.c:2057,2087-2091` — `static void set_native_thread_name( HANDLE handle, const UNICODE_STRING *name )` … `    snprintf(path, sizeof(path), "/proc/%u/task/%u/comm", unix_pid, unix_tid);` / `    if ((fd = open( path, O_WRONLY )) != -1)` / `    {` / `        write( fd, nameA, len );`
  - `wine thread.c:2647` — `        set_native_thread_name( handle, &info->ThreadName );` (in the `ThreadNameInformation` case of `NtSetInformationThread`, i.e. the path of Win32 `SetThreadDescription`)
  - `wineboot.c:1471-1472` — `    if (!create_native_process( L"C:\\windows\\system32\\services.exe", NULL,` / `                                TRUE, DETACHED_PROCESS, L"C:\\windows\\system32", &pi))`
  - `services.c:841` — `    lstrcatW(*path, L"\\winedevice.exe");`
- **Coverage.** T5: a Proton game runs as Linux processes whose comm is the Windows executable basename (15-char truncated), launched via Proton's `steam.exe` shim; `wineserver`, `services.exe` and `winedevice.exe` (driver host) run alongside; Windows thread descriptions become Linux thread comm names on Linux. Counts of processes/threads of a real game: not covered.
- **One observation?** No.

### S2-20 — gamescope README

- **Copy** (`../sources/S2-20/gamescope-README.md`, raw.githubusercontent.com `ValveSoftware/gamescope@2cfb4803984e8e4144805b57ebb5d38ea42bec13`, commit date 2026-09-22, fetched 2026-09-23) `5a9130ced7900e30f62fc7a0b033d2e5d9f849e1069704483c3e396652aeff87`.
- **Verbatim passages.** `README.md:1` — "## gamescope: the micro-compositor formerly known as steamcompmgr"; `:3` — "In an embedded session usecase, gamescope does the same thing as steamcompmgr, but with less extra copies and latency:"; `:9-11` — "It also runs on top of a regular desktop, the 'nested' usecase steamcompmgr didn't support. - Because the game is running in its own personal Xwayland sandbox desktop, it can't interfere with your desktop and your desktop can't interfere with it."; `:53-56` — "On any X11 or Wayland desktop, you can set the Steam launch arguments of your game as follows:" … `gamescope -h 720 -H 1440 -S integer -- %command%`.
- **Coverage.** T5: on a desktop, gamescope is opt-in per game (launch option) and then adds its own Xwayland nested inside the desktop compositor; embedded-session use (Steam Deck) replaces the desktop compositor. The README does not name the Steam Deck or state defaults. No observation.
- **One observation?** No.

### S2-21 — Discord: Game Overlay platform support

- **Copy** (`../sources/S2-21/discord-overlay-101.json`, Zendesk API `https://support.discord.com/api/v2/help_center/en-us/articles/217659737.json`, 200, 2026-09-23) `32515c156e7a868bb7e1cb5d8719fc58498574280fe77bd0abe4d97c5839c9e6`. Article "Game Overlay 101", `edited_at` 2025-04-02T17:39:44Z, `updated_at` 2026-09-23T02:11:53Z. (HTML page → HTTP 403.)
- **Verbatim passage.** "NOTE: The overlay is compatible with Windows OS only; it does not function on Mac OS or Linux."
- **Coverage.** T5: no Discord in-game overlay process on Linux; Discord voice client itself exists (not documented here). T11: no.
- **One observation?** No.

### S2-22 — Microsoft Teams on Linux

- **Copies** (`../sources/S2-22/`, 2026-09-23): `https://learn.microsoft.com/en-us/microsoftteams/get-clients` (200; page meta `ms.date` 2026-07-16) `ms-learn-get-clients.html` `b1039ed9866d7f059fb382a331bdb121db3a4be88ea4ecb96bd3ead6d0691932`; `https://techcommunity.microsoft.com/discussions/microsoftteams/end-of-the-road-for-teams-linux-desktop-client/3630968` (200) `ms-teams-linux-eol.html` `7c7a7b543394b46ceb919f0008b0d343ad42fb9e7e64133f46ed32166423bd7b`.
- **Verbatim passages.** Microsoft Learn availability table: "Linux ❌ Teams is no longer supported on Linux. Web ✅ Supported in Microsoft Edge, Chrome, Firefox, Safari." Tech Community post by Tony Redmond (MVP, not Microsoft staff), Sep 19, 2022: "According to notifications sent by Microsoft to customers that have users of the Teams Linux client, Microsoft plans to retire the client in early December and replace it with a progressive web app (PWA)."
- **Coverage.** T11: a Teams call on Linux runs inside a browser (Chromium-based or Firefox) — process structure then follows S2-15/S2-16. No call-time process data.
- **One observation?** No.

### S2-23 — Zoom Workplace for Linux 7.2.1.5760 package contents

- **Copy** (`../sources/S2-23/zoom_7.2.1.5760_amd64.deb`, `https://zoom.us/client/latest/zoom_amd64.deb` → 302 → `https://cdn.zoom.us/prod/7.2.1.5760/zoom_amd64.deb`, 200, 302 788 858 bytes, 2026-09-23) `e9a522c794622633b24908ac0589a8e4df8a542846b97818e76f6c27e117cbdb`.
- **Facts read from the package** (`dpkg-deb -f` / `-c`; a file list, not prose): `Package: zoom` / `Version: 7.2.1.5760`; `Depends:` includes `libpulse0`, `ibus`, `libgbm1`, `libxcb-*`. Executable files: `./opt/zoom/ZoomLauncher` (target of symlink `./usr/bin/zoom -> /opt/zoom/ZoomLauncher`), `./opt/zoom/zoom`, `./opt/zoom/ZoomWebviewHost`, `./opt/zoom/aomhost`, `./opt/zoom/cpthost`, `./opt/zoom/crashpad_handler`, `./opt/zoom/zopen`, `./opt/zoom/ZoomClips`, `./opt/zoom/cef/chrome_sandbox`, `./opt/zoom/minidump_processor`, `./opt/zoom/getbssid.sh`; `opt/zoom/version.txt` = `7.2.1.5760`.
- **Coverage.** T11: candidate process names of the Zoom Linux client (a CEF-based web view host is shipped). Which of them run during a call, and how many threads, is **not** documented by Zoom (see Not found).
- **One observation?** No.

### S2-24 — Philip Withnall, "Startup time profiling of gnome-software" (2020)

- **Copy** (`../sources/S2-24/withnall-gs-startup.html`, `https://tecnocode.co.uk/2020/07/14/startup-time-profiling-of-gnome-software/`, 200, 2026-09-23) `c35cd8407177356291632d1ba1806fa58e2f2f62e6439f227d55e52e9d068702`. Author is a GLib/GNOME maintainer; post dated 2020-07-14.
- **Verbatim passages.** "Adding items to a GtkFlowBox takes some time, and if there are a couple of hundred of apps to be added in a single idle callback, that can take several hundred milliseconds — a long enough time to block the main UI from being redrawn that the user will notice." "In it, you can see the 'get-updates' plugin job on gnome-software's flatpak plugin is taking 1.5 seconds (in a thread), and then 175ms to process the results in the main thread. The selected row above that is showing it's taking 110ms to process the results from a call to gs_plugin_loader_job_get_categories_async() in the main thread." Method: "This capture file was generated using sysprof-cli --gtk --use-trace-fd -- gnome-software".
- **Coverage.** T10: per-task CPU/wall components of one application's startup (gnome-software 3.36/3.37 era, Endless OS context) — not a total launch time, not per-session launch frequency. One developer measurement; machine not named.
- **One observation?** Yes, one run on an unnamed machine by one developer; window: July 2020.

### S2-26 — systemd user manager unit

See S2-13 (copy identification there). `user@.service.in:23` — `ExecStart={{LIBEXECDIR}}/systemd --user`. Coverage T8: per-user service manager process `systemd` (comm `systemd`) started per logged-in user.

---

## 3. Coverage summary by topic

| Topic | Candidates | What documentation establishes |
|---|---|---|
| T4 | S2-15, S2-16 | Chromium: site-per-process on Linux, soft limit formula, reuse rules, spare renderer, soft limit removed by default on main; Firefox: Fission on, webIsolated=4, processCount=8; tab/window/URI probes defined but not published |
| T5 | S2-17, S2-18, S2-19, S2-20, S2-21 | Downloads pause during gameplay by default; process chain steam-launch-wrapper → reaper → SLR entry point → pressure-vessel/bwrap → pv-adverb → Proton (steam.exe shim, wineserver, services.exe, winedevice.exe); Wine maps process and thread names to comm; gamescope opt-in; no Discord overlay on Linux |
| T6 | S2-01…S2-10, S2-25 | Timer/service sets and schedules for Ubuntu 24.04/26.04, Fedora 43/rawhide, Arch; ClamAV defaults; indexers; DKMS triggers and -j; object counts per module |
| T7 | S2-10 (partial) | DKMS module object counts only |
| T8 | S2-04, S2-05, S2-07, S2-08, S2-11, S2-12, S2-13, S2-14, S2-25, S2-26 | Xwayland on demand (GNOME ≥40), X11 backend removed (mutter 50), Ubuntu 26.04 GNOME Wayland-only, bus implementation per distro (Fedora/Arch dbus-broker, Ubuntu dbus-daemon), PipeWire/WirePlumber user units, comm 15-char rule |
| T10 | S2-24 (weak) | One developer's per-task startup timings of gnome-software |
| T11 | S2-22, S2-23 | Teams on Linux = browser only; Zoom ships ZoomLauncher/zoom/ZoomWebviewHost/aomhost/cpthost |
| T12 | S2-16 (negative) | Firefox telemetry exists but aggregates for tabs are not public |

## 4. Not found

- **T1, T2, T3, T9, T12, T13** — outside S2's scope; no project/vendor documentation searched specifically. Incidental: S2-16 shows Firefox tab/window telemetry is collected but not published (searches #20-21).
- **T4 — logged tab/window counts or page-load/tab-switch rates of real users**: no public vendor aggregate. Searches: #20 (probe definitions only), #21 (Public Data Report ETL lists no tab metric; dashboards JS-only, not read). Chromium UMA (`Tabs.*` histograms) not searched — histogram definitions would again be definitions, not published aggregates.
- **T4 — measured renderer counts for a given tab set on Linux**: not in documentation (only rules). Searches #19.
- **T5 — Steam client helper processes and their state during a game (steamwebhelper, gameoverlayui), Linux-specific statement about downloads during gameplay, and thread counts of a Proton game**: not documented. Searches #22-27 (Valve FAQs are platform-neutral; steam-runtime docs cover the wrapper chain only). `gameoverlayui` not found in any document read.
- **T6 — how long each timer job runs (updatedb, mandb, fwupd refresh, freshclam update, dpkg-db-backup) and how long a DKMS autoinstall takes**: no documentation gives durations. Searches #1-9, #13-14 (unit files and hooks carry schedules and priorities only; 88x2bu script only prints compile time at run time).
- **T6 — whether plocate / dkms are in a default Fedora Workstation install**: Fedora comps not read (presets only). Searches #4-6.
- **T8 — default session type of Kubuntu 24.04 (X11 or Wayland)**: not established by package files (#2, sddm package). KDE Plasma defaults per distribution not searched further.
- **T8 — which KDE/GNOME versions per distribution still run Xorg by default beyond Ubuntu**: Fedora comps/Arch not read.
- **T10 — application launch frequency within a session; total launch CPU/wall time of common apps on Linux**: only S2-24 (per-task timings). Search #32.
- **T11 — Zoom Linux client process structure during a call**: no Zoom documentation (search #30 returned only community forums/third-party guides); package file list only (S2-23). **Whether users play media alongside other work**: not a documentation question; nothing found.
- **Unreachable / blocked**: src.fedoraproject.org raw files — HTTP 200 Anubis bot-check page (#4; git clone worked); gitlab.winehq.org raw — HTTP 200 Anubis bot-check page (#25; GitHub mirror used); support.discord.com HTML — **HTTP 403** (#28; Zendesk JSON API worked); Ubuntu archive stale-index fetches — **HTTP 404** (#1; fixed by `apt-get update`); data.firefox.com — JS-rendered, not readable (#21).
