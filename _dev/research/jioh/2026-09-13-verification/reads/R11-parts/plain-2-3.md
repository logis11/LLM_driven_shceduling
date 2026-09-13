## C-plain-2 and C-plain-3 — copies used

All retrieved 2026-09-13. `S` = `_dev/research/jioh/2026-09-13-verification/sources`. Every `.deb` was checked with SHA-256 against the `SHA256:` field of the archive's `Packages` index; they all matched.

| Copy | URL | Version / commit | Local path |
|---|---|---|---|
| Debian 13 archive index | https://deb.debian.org/debian/dists/trixie/Release , .../trixie/main/binary-amd64/Packages.xz | Release file: "Version: 13.7", "Date: Sat, 12 Sep 2026 07:55:41 UTC" | S/C-plain-3/debian-trixie-* |
| Debian 12 archive index | https://deb.debian.org/debian/dists/bookworm/Release , .../bookworm/main/binary-amd64/Packages.xz | "Version: 12.15" | S/C-plain-3/debian-bookworm-* |
| Ubuntu 24.04 archive index | http://archive.ubuntu.com/ubuntu/dists/noble{,-updates}/{main,universe}/binary-amd64/Packages.xz | noble, noble-updates as of retrieval | S/C-plain-3/ubuntu-noble-* |
| clamav, clamav-base, clamav-daemon, clamav-freshclam (Debian 13) | https://deb.debian.org/debian/pool/main/c/clamav/ | 1.4.3+dfsg-1 | S/C-plain-2/debs/, extracted to S/C-plain-2/x/ |
| clamav Debian source packaging | https://deb.debian.org/debian/pool/main/c/clamav/clamav_1.4.3+dfsg-1.debian.tar.xz | 1.4.3+dfsg-1 (sha256 03ba75f8…18ff, matching the .dsc) | S/C-plain-2/debian-source/debian/ |
| clamav, clamav-daemon, clamav-freshclam (Ubuntu 24.04 updates) | http://archive.ubuntu.com/ubuntu/pool/main/c/clamav/ | 1.5.3+dfsg-0ubuntu0.24.04.1 | S/C-plain-2/debs/, S/C-plain-2/x/ |
| init-system-helpers (the `update-rc.d` script) | https://deb.debian.org/debian/pool/main/i/init-system-helpers/init-system-helpers_1.69~deb13u1_all.deb | 1.69~deb13u1 | S/C-plain-2/x/init-system-helpers_1.69~deb13u1_all/ |
| ClamAV official documentation source | https://github.com/Cisco-Talos/clamav-documentation.git | commit 26dceb239dff15088c5b04b469fd056d1933548b (2026-08-07) | S/C-plain-2/clamav-documentation/ |
| Fedora clamav packaging | https://src.fedoraproject.org/rpms/clamav.git | commit 110ace5be45f538ef3689b548a220bffa1ad5e6f (2026-09-10), spec Version 1.4.6 Release 2 | S/C-plain-2/fedora/clamav-rpm/ |
| tracker-extract, which ships localsearch (Debian 13) | https://deb.debian.org/debian/pool/main/t/tracker-miners/tracker-extract_3.8.2-4+b1_amd64.deb | 3.8.2-4+b1 | S/C-plain-3/debs/, S/C-plain-3/x/ |
| tracker-miner-fs (Debian 13, transitional) | .../tracker-miner-fs_3.8.2-4_all.deb | 3.8.2-4 | same |
| tracker-miner-fs (Debian 12) | https://deb.debian.org/debian/pool/main/t/tracker-miners/tracker-miner-fs_3.4.3-1_amd64.deb | 3.4.3-1 | same |
| tracker-miner-fs (Ubuntu 24.04 updates) | http://archive.ubuntu.com/ubuntu/pool/main/t/tracker-miners/tracker-miner-fs_3.7.1-1ubuntu0.1_amd64.deb | 3.7.1-1ubuntu0.1 | same |
| GNOME LocalSearch upstream | https://gitlab.gnome.org/GNOME/localsearch.git | tag 3.8.2 → commit ec1fb9abf8223c37cddc141567b2c6650d4ee6e3 | S/C-plain-3/localsearch-3.8.2/ |
| baloo6 (Debian 13) | https://deb.debian.org/debian/pool/main/k/kf6-baloo/baloo6_6.13.0-1_amd64.deb | 6.13.0-1 | S/C-plain-3/debs/, S/C-plain-3/x/ |
| baloo-kf5 (Debian 12) | https://deb.debian.org/debian/pool/main/b/baloo-kf5/baloo-kf5_5.103.0-2_amd64.deb | 5.103.0-2 | same |
| KDE Baloo upstream | https://invent.kde.org/frameworks/baloo.git (git clone; the `-/raw/` web URLs returned HTTP 403) | tag v6.13.0 → commit 652de972bf24d4ab9d6ddb1f1e9e88d300375b0e | S/C-plain-3/kde-src/baloo/ |
| plocate (Debian 13) | https://deb.debian.org/debian/pool/main/p/plocate/plocate_1.1.23-1_amd64.deb | 1.1.23-1 | S/C-plain-3/debs/, S/C-plain-3/x/ |
| plocate (Ubuntu 24.04, universe) | http://archive.ubuntu.com/ubuntu/pool/universe/p/plocate/plocate_1.1.19-2ubuntu2_amd64.deb | 1.1.19-2ubuntu2 | same |
| Linux man-pages | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_stat.5?id=adb436b2… (also proc_pid_comm.5, man2const/PR_SET_NAME.2const) | tag man-pages-6.19 → commit adb436b2e4471218021d86f188fb58dec3946eb8 | S/C-plain-3/man-pages/ |

Shared primary source for process names (used by both topics). Linux man-pages 6.19, `man/man5/proc_pid_stat.5`, lines 35–40:

> .RI (2)\~ comm \~%s
> The filename of the executable, in parentheses.
> Strings longer than
> .B TASK_COMM_LEN
> (16) characters (including the terminating null byte) are silently truncated.

`man/man5/proc_pid_comm.5`: "Different threads in the same process may have different
.I comm
values, accessible via
.IR /proc/ pid /task/ tid /comm ."

What this means: the kernel's process name (comm) is the executable's filename, cut to 15 visible characters. Any executable name of 16 characters or more therefore appears truncated. The truncated forms below are derived from this rule. I did not observe them on a running system.

---

## C-plain-2 — ClamAV: is a scheduled scan shipped by default, and which process runs it?

### (a) Verbatim passages / file content

**1. ClamAV official docs** (Cisco-Talos/clamav-documentation @26dceb2)

`src/manual/Usage/Scanning.md` line 30:
> `clamd` is a multi-threaded daemon that uses *libclamav* to scan files for viruses. Scanning behavior can be fully configured to fit most needs by modifying `clamd.conf`.

Line 114:
> The ClamOnAcc application provides On-Access Scanning for Linux systems. On-Access Scanning is a form of real-time protection that uses ClamD to scan files when they're accessed.

Line 156 (under "## One-Time Scanning"):
> `clamscan` is a command line tool which uses *libclamav* to scan files and/or directories for viruses. Unlike `clamdscan`, `clamscan` does *not* require a running `clamd` instance to function. Instead, `clamscan` will create a new engine and load in the virus database each time it is run. It will then scan the files and/or directories specified at the command line, create a scan report, and exit.

`src/manual/Usage/Configuration.md` lines 128–134:
> The other way is to use the *cron* daemon. You have to add the following line to the *crontab* of **root** or **clamav** user:
>
> ```
> N * * * *   /usr/local/bin/freshclam --quiet
> ```
>
> to check for a new database every hour.

`src/faq/faq-cvd.md` line 11:
> ClamAV comes with _FreshClam_, a tool which periodically checks for new database releases and keeps your database up to date.

**2. Debian 13 package file lists** (1.4.3+dfsg-1). The listing shows every systemd, cron and binary path. Man pages, docs and locale files are omitted.

- `clamav`: `./usr/bin/clambc`, `./usr/bin/clamscan`, `./usr/bin/clamsubmit`, `./usr/bin/sigtool`. No systemd unit, no cron file.
- `clamav-daemon`: `./usr/lib/systemd/system/clamav-clamonacc.service`, `./usr/lib/systemd/system/clamav-daemon.service`, `./usr/lib/systemd/system/clamav-daemon.socket`, `./usr/sbin/clamd`, `./usr/sbin/clamonacc`, `./etc/init.d/clamav-daemon`, and others.
- `clamav-freshclam`: `./usr/bin/freshclam`, `./usr/lib/systemd/system/clamav-freshclam-once.service`, `./usr/lib/systemd/system/clamav-freshclam-once.timer`, `./usr/lib/systemd/system/clamav-freshclam.service`, `./etc/init.d/clamav-freshclam`, the if-up.d/ppp hooks, and others.
- None of the four packages contains a `cron.*` file.

`clamav-freshclam` → `/usr/lib/systemd/system/clamav-freshclam-once.timer` (entire file):
```
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
`clamav-freshclam-once.service` contains `ExecStart=/usr/bin/freshclam`.

`clamav-freshclam.service` contains:
```
# If user wants it run from cron, don't start the daemon.
ConditionPathExists=!/etc/cron.d/clamav-freshclam
...
ExecStart=/usr/bin/freshclam -d --foreground=true
```

`clamav-daemon.service` contains:
```
ConditionPathExistsGlob=/var/lib/clamav/main.{c[vl]d,inc}
ConditionPathExistsGlob=/var/lib/clamav/daily.{c[vl]d,inc}

[Service]
ExecStart=/usr/sbin/clamd --foreground=true
```

`clamav-clamonacc.service` contains:
```
Requires=clamav-daemon.service
...
ExecStart=/usr/sbin/clamonacc -F --log=/var/log/clamav/clamonacc.log --move=/root/quarantine
```

**3. Which units the Debian maintainer scripts enable**

Debian source `debian/rules` lines 156–170:
```
override_dh_installinit:
	dh_installinit -pclamav-daemon
	# Don't change the postinst/postrm scripts for clamav-freshclam, as they need non-standard code.
	dh_installinit -pclamav-freshclam --noscripts
	dh_installinit -pclamav-milter
...
override_dh_installsystemd:
ifneq (linux, $(DEB_HOST_ARCH_OS))
	dh_installsystemd --name clamav-clamonacc --no-enable --no-start
endif
	dh_installsystemd --name clamav-daemon
```

`clamav-daemon` postinst lines 758–761, repeated for `clamav-daemon.socket` at 775–778:
```
	if deb-systemd-helper --quiet was-enabled 'clamav-daemon.service'; then
		# Enables the unit on first installation, creates new
		# symlinks on upgrades if the unit file has changed.
		deb-systemd-helper enable 'clamav-daemon.service' >/dev/null || true
```
A grep of all `clamav-daemon` and `clamav-freshclam` control scripts found no `deb-systemd-helper` line for `clamav-clamonacc`, `clamav-freshclam-once.timer` or `clamav-freshclam.service`. The only `clamonacc` hits in `control/` were in `md5sums`.

`clamav-freshclam` templates, lines 2–4 and 22:
```
Template: clamav-freshclam/autoupdate_freshclam
Type: select
Choices: daemon, ifup.d, cron, manual
...
Default: daemon
```

`clamav-freshclam` postinst lines 585–589:
```
if [ $DO_RUN_AS_EVALUATION -eq 1 ]
then
  if [ "$runas" = 'daemon' ]; then
    update-rc.d clamav-freshclam defaults >/dev/null
    invoke-rc.d clamav-freshclam start
```

The cron file is written only when the admin picks the cron method. Postinst lines 396–402:
```
  # Set up cron method
  if [ "$runas" = cron ]; then
...
    echo "$min */$cronhour * * *    $dbowner [ -x /usr/bin/freshclam ] && /usr/bin/freshclam --quiet >/dev/null" > "$FRESHCLAMTEMP"
```

`init-system-helpers` 1.69~deb13u1, `/usr/sbin/update-rc.d`, systemd handler (lines 269–275):
```
    my $systemd = {};
    $systemd->{remove} = sub {
        systemd_reload;
    };
    $systemd->{defaults} = sub {
        systemd_reload;
    };
```
`make_systemd_links` (the function that runs `systemctl ... enable`) is called only from `$systemd->{toggle}`, i.e. `update-rc.d enable|disable`.

**4. Ubuntu 24.04** (1.5.3+dfsg-0ubuntu0.24.04.1)
- The same unit set ships: `clamav-freshclam-once.{service,timer}`, `clamav-freshclam.service`, `clamav-clamonacc.service`, `clamav-daemon.{service,socket}`.
- `diff` against Debian 13 shows the `clamav-freshclam-once.timer`, `clamav-freshclam.service` and `clamav-clamonacc.service` files are identical.
- The postinst files have the same structure: `Default: daemon` (templates line 22), `update-rc.d clamav-freshclam defaults` (postinst line 592), and `deb-systemd-helper enable` only for `clamav-daemon.service` and `clamav-daemon.socket` (lines 779, 796).

**5. Fedora** (rpms/clamav @110ace5, `clamav.spec`)
- Line 52: `Source202:  clamav-update.crond`. That file's content is `0  */3 * * * root /usr/share/clamav/freshclam-sleep > /dev/null`, which is a freshclam update, not a scan.
- A grep for `crond|SOURCE202|cron.d` found no install or `%files` line for it. The only other hit is changelog line 868.
- Scriptlets: `%systemd_post clamav-clamonacc.service`, `%systemd_post clamd@scan.service`, `%systemd_post clamav-freshclam.service`. `%files` lists `%{_unitdir}/clamav-freshclam-once.timer`.

### (b) Locators
- Docs: repo and commit as above, file paths and line numbers as given.
- Debian: files inside the named `.deb` files (paths shown); control scripts at `S/C-plain-2/x/<pkg>/control/{postinst,templates}`; `debian/rules` from `clamav_1.4.3+dfsg-1.debian.tar.xz`.
- Ubuntu and Fedora: as in the copies table.

### (c) Plain-words reading
- **Scheduled scan: none is shipped.** The Debian 13, Ubuntu 24.04 and Fedora (spec 1.4.6-2) packaging has no timer, cron job or unit that runs `clamscan` or `clamdscan` on a schedule. ClamAV's own docs describe `clamscan` as "One-Time Scanning" run from the command line. They mention cron only for `freshclam`, i.e. database updates.
- **What is scheduled is the database update, `freshclam`.**
  - Debian and Ubuntu default to running `freshclam` as a daemon (`freshclam -d`; debconf `Default: daemon`). The postinst starts it via `invoke-rc.d`.
  - The shipped `clamav-freshclam-once.timer` (daily) is not enabled by any maintainer script found.
  - Whether `clamav-freshclam.service` is also enabled for boot on a systemd system is not settled by these files. `update-rc.d ... defaults` only runs a systemd daemon-reload and does not enable the native unit, and no `deb-systemd-helper enable` exists for it. I did not read systemd's sysv-generator behaviour.
- **clamd** (`/usr/sbin/clamd`): `clamav-daemon.service` and `.socket` are enabled on install by the dh_installsystemd snippet. The service has a condition requiring downloaded signature databases. It is a scanning server, not a scheduled scan.
- **clamonacc** (`/usr/sbin/clamonacc`): the on-access scanner. Its unit is shipped but not enabled by any Debian maintainer script.
- **Process names:** `freshclam`, `clamd`, `clamonacc`, and `clamscan` if a user runs it. All are under 16 characters, so they are not truncated.
- **Caveats:**
  - The packages are not installed by default. No Debian 13 or Ubuntu 24.04 `task-*`, `ubuntu-*`, `gnome*` or `kde*` package in the indexes read Depends on or Recommends clamav, clamav-daemon or clamav-freshclam.
  - Fedora's `%systemd_post` enables a unit only if the distribution preset allows it. I did not read Fedora's preset files, so Fedora's enable state is unverified.

### (d) Verdict
- **FOUND** (the answer is no). No ClamAV package examined ships a scheduled scan. The scheduled or background job shipped is the `freshclam` database update: a daemon by default on Debian and Ubuntu, plus a daily `clamav-freshclam-once.timer` that is not enabled.
- "Which process performs the scheduled scan": **PREMISE NOT IN SOURCE**. There is no scheduled scan. What exists instead is `freshclam` (update), `clamd` (daemon, enabled on Debian and Ubuntu) and `clamonacc` (on-access, not enabled).
- Fedora enable state: **PARTIAL** (presets not read).

---

## C-plain-3 — tracker-miner-fs(-3), baloo_file, plocate updatedb timer: shipped and enabled by default? Process names?

### C-plain-3 item 1: GNOME file indexer, tracker-miner-fs-3 (renamed localsearch-3)

**(a) Verbatim**

Debian 12 `tracker-miner-fs` 3.4.3-1 and Ubuntu 24.04 `tracker-miner-fs` 3.7.1-1ubuntu0.1 ship the same file set: `./etc/xdg/autostart/tracker-miner-fs-3.desktop`, `./usr/lib/systemd/user/tracker-miner-fs-3.service`, `./usr/lib/systemd/user/tracker-miner-fs-control-3.service`, `./usr/libexec/tracker-miner-fs-3`, `./usr/libexec/tracker-miner-fs-control-3`.

`tracker-miner-fs-3.service` (Ubuntu 3.7.1-1ubuntu0.1):
```
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
The Debian 12 unit is identical except that it lacks the `ConditionUser=!gnome-initial-setup` line.

`tracker-miner-fs-3.desktop` (both versions):
```
Exec=/usr/libexec/tracker-miner-fs-3
...
X-GNOME-Autostart-enabled=true
X-GNOME-HiddenUnderSystemd=true
...
OnlyShowIn=GNOME;KDE;XFCE;X-IVI;Unity;
X-systemd-skip=true
```

Postinst line 51 (both versions): `			deb-systemd-helper --user enable 'tracker-miner-fs-3.service' >/dev/null || true`

Ubuntu 24.04 `nautilus` 1:46.4-0ubuntu0.2 control field: `Depends: ... tracker (>= 3), tracker-miner-fs (>= 3), tracker-extract (>= 3), ...`

Debian 13:
- `tracker-miner-fs` 3.8.2-4 is `Architecture: all`, `Depends: localsearch`, `Description: metadata database, indexer and search tool - transitional package`.
- `tracker-extract` 3.8.2-4+b1 has `Provides: localsearch (= 3.8.2-4+b1)` and ships `./etc/xdg/autostart/localsearch-3.desktop`, `./usr/lib/systemd/user/localsearch-3.service`, `./usr/libexec/localsearch-3`, and others.
- `localsearch-3.service`: `ExecStart=/usr/libexec/localsearch-3`, `[Install]` `WantedBy=gnome-session.target`.
- `localsearch-3.desktop`: `Exec=/usr/libexec/localsearch-3`, `X-GNOME-Autostart-enabled=true`.
- Postinst line 47: `			deb-systemd-helper --user enable 'localsearch-3.service' >/dev/null || true`.
- Postinst also: `dpkg-maintscript-helper rm_conffile /etc/xdg/autostart/tracker-miner-fs-3.desktop 3.8.2-1\~ -- "$@"`.
- Dependency chain: `nautilus` 48.3-2 `Depends: ... localsearch, ...`, and `gnome-core` 1:48+2 `Depends: ... nautilus (>= 48), ...`.

GNOME upstream `localsearch` tag 3.8.2, `NEWS`, line 64 (under "NEW in 3.8.alpha - 2024-07-04"): `  * Rename project to LocalSearch`. Line 58 (3.8.beta): `  * Renamed command line tool`.

Upstream `src/miners/fs/meson.build` lines 135–151:
```
# This file allows starting the service automatically using XDG autostart.
# systemd user service activation is preferred if available.
desktop_file = configure_file(
    input: 'tracker-miner-fs.desktop.in',
    output: 'localsearch-@0@.desktop'.format(tracker_api_major),
...
if get_option('systemd_user_services')
  # This file allows starting the service as a systemd user service.
  configure_file(
      input: 'tracker-miner-fs.service.in',
      output: 'localsearch-@0@.service'.format(tracker_api_major),
```
`meson_options.txt` line 91: `option('systemd_user_services', type: 'boolean', value: true,`

**(c) Reading**
- **Upstream:** GNOME's file-system miner ships with an XDG autostart entry and, by default, a systemd user unit. From 3.8 (GNOME LocalSearch, released 2024) the project and binary are named `localsearch-3`; up to 3.7 the binary is `tracker-miner-fs-3`.
- **Debian 12 and Ubuntu 24.04:** the binary is `/usr/libexec/tracker-miner-fs-3`. The user unit is enabled on package install (`deb-systemd-helper --user enable`), and the autostart entry has `X-GNOME-Autostart-enabled=true`. In Ubuntu 24.04 the package is a hard dependency of the file manager, nautilus.
- **Debian 13:** the binary is `/usr/libexec/localsearch-3`. `tracker-miner-fs` is now only a transitional package. The chain gnome-core → nautilus → localsearch is a hard dependency, and the unit is enabled on install.
- **Process name:**
  - `tracker-miner-fs-3` is 18 characters, so per proc_pid_stat(5) the comm is the first 15: `tracker-miner-f`. This is derived from the man page, not observed.
  - `localsearch-3` (13 characters) is not truncated.
- **Scope:** this is a continuously running user-session indexer started with the GNOME session, not a timer.

**(d) Verdict:** **FOUND** for Debian 12, Ubuntu 24.04 and Debian 13 at the named versions. The topic premise "tracker-miner-fs-3" holds for releases ≤3.7. Debian 13 / GNOME 47+ ship it as `localsearch-3`.

### C-plain-3 item 2: KDE Baloo, baloo_file

**(a) Verbatim**

Debian 13 `baloo6` 6.13.0-1 files: `./etc/xdg/autostart/baloo_file.desktop`, `./usr/lib/systemd/user/kde-baloo.service`, `./usr/lib/x86_64-linux-gnu/libexec/kf6/baloo_file`, `./usr/lib/x86_64-linux-gnu/libexec/kf6/baloo_file_extractor`, and others.

`kde-baloo.service`:
```
[Unit]
Description=Baloo File Indexer Daemon
PartOf=graphical-session.target

[Service]
ExecStart=/usr/lib/x86_64-linux-gnu/libexec/kf6/baloo_file
BusName=org.kde.baloo
Slice=background.slice
ExecCondition=/usr/bin/kde-systemd-start-condition --condition "baloofilerc:Basic Settings:Indexing-Enabled:true"
# We'll basically only want to consume resources if they aren't needed anywhere else, hence weights are way low.
CPUWeight=1
IOWeight=1
...
[Install]
WantedBy=graphical-session.target
```

`baloo_file.desktop`:
```
Exec=/usr/lib/x86_64-linux-gnu/libexec/kf6/baloo_file
X-KDE-StartupNotify=false
X-KDE-autostart-condition=baloofilerc:Basic Settings:Indexing-Enabled:true
X-KDE-autostart-phase=0
X-GNOME-Autostart-enabled=true
X-systemd-skip=true
OnlyShowIn=KDE;GNOME;Unity;XFCE
```

`baloo6` postinst line 13: `			deb-systemd-helper --user enable 'kde-baloo.service' >/dev/null || true`

Debian 13 `dolphin` 4:25.04.3-1+deb13u1: `Depends: baloo6, ...`

Debian 12 `baloo-kf5` 5.103.0-2:
- The autostart file has `Exec=/usr/lib/x86_64-linux-gnu/libexec/baloo_file` and the same `X-KDE-autostart-condition` line.
- `kde-baloo.service` has `ExecStart=/usr/lib/x86_64-linux-gnu/libexec/baloo_file`.
- Postinst line 13 is the same `deb-systemd-helper --user enable 'kde-baloo.service'` line.

Upstream Baloo v6.13.0 (commit 652de97), `src/lib/baloosettings.kcfg` lines 8–13:
```
  <kcfgfile name="baloofilerc" />
  <group name="Basic Settings">
    <entry name="indexingEnabled" key="Indexing-Enabled" type="Bool">
      <label>Indexing-Enabled</label>
      <default>true</default>
    </entry>
```
The same condition string appears upstream in `src/file/kde-baloo.service.in` line 9 and `src/file/baloo_file.desktop.in` line 5.

**(c) Reading**
- **Shipped and enabled:** KDE's Baloo ships the file indexer daemon `baloo_file` with both an XDG autostart entry and a systemd user unit. Debian enables the user unit on install.
- **Start condition:** start is gated on the `Indexing-Enabled` setting in `baloofilerc`. Upstream's settings schema gives that key `<default>true</default>`, so indexing is on unless the user turns it off.
- **Installation:** in Debian 13 the file manager `dolphin` hard-depends on `baloo6`.
- **Process name:** `baloo_file` (10 characters, not truncated). A separate `baloo_file_extractor` binary is also shipped.
- **Caveats:**
  - I did not read the parser for the trailing `:true` in the autostart condition string.
  - The claim "on by default" rests on the kcfg `<default>true</default>` entry.
- **Scope:** a session daemon, not a timer.

**(d) Verdict:** **FOUND** (Debian 13 baloo6 6.13.0-1, Debian 12 baloo-kf5 5.103.0-2, upstream v6.13.0).

### C-plain-3 item 3: plocate updatedb timer

**(a) Verbatim**

Debian 13 `plocate` 1.1.23-1 files: `./etc/cron.daily/plocate`, `./etc/updatedb.conf`, `./usr/bin/plocate`, `./usr/lib/systemd/system/plocate-updatedb.service`, `./usr/lib/systemd/system/plocate-updatedb.timer`, `./usr/sbin/plocate-build`, `./usr/sbin/updatedb.plocate`, and others.

`plocate-updatedb.timer`:
```
[Unit]
Description=Update the plocate database daily

[Timer]
OnCalendar=daily
RandomizedDelaySec=1h
AccuracySec=6h
Persistent=true

[Install]
WantedBy=timers.target
```

`plocate-updatedb.service` (excerpt):
```
[Unit]
Description=Update the plocate database
ConditionACPower=true

[Service]
Type=oneshot
ExecStart=/usr/sbin/updatedb.plocate
LimitNOFILE=131072
IOSchedulingClass=idle
Nice=19
```

`/etc/cron.daily/plocate` (excerpt):
```
UPDATEDB=/usr/sbin/updatedb.plocate

# Skip if systemd timer is available.
if [ -d /run/systemd/system ]; then
    exit 0
fi
```

Postinst lines 23–32:
```
# Automatically added by dh_installsystemd/13.20
if [ "$1" = "configure" ] || [ "$1" = "abort-upgrade" ] || [ "$1" = "abort-deconfigure" ] || [ "$1" = "abort-remove" ] ; then
	# The following line should be removed in trixie or trixie+1
	deb-systemd-helper unmask 'plocate-updatedb.timer' >/dev/null || true

	# was-enabled defaults to true, so new installations run enable.
	if deb-systemd-helper --quiet was-enabled 'plocate-updatedb.timer'; then
		# Enables the unit on first installation, creates new
		# symlinks on upgrades if the unit file has changed.
		deb-systemd-helper enable 'plocate-updatedb.timer' >/dev/null || true
```

Postinst also: `	--slave /usr/bin/updatedb updatedb /usr/sbin/updatedb.plocate \`

Ubuntu 24.04 `plocate` 1.1.19-2ubuntu2 (universe):
- Same file set and same `ExecStart=/usr/sbin/updatedb.plocate`.
- The timer differs only in `RandomizedDelaySec=12h` and `AccuracySec=20min`.
- Postinst line 42: `		deb-systemd-helper enable 'plocate-updatedb.timer' >/dev/null || true`.

**(c) Reading**
- **Timer enabled on install:** when plocate is installed on Debian 13 or Ubuntu 24.04, the package enables a daily systemd timer. The timer runs `/usr/sbin/updatedb.plocate` at `Nice=19` with idle I/O priority, and only on AC power. On non-systemd systems a `cron.daily` script runs the same job.
- **Process name:** the binary `updatedb.plocate` is 16 characters, so per proc_pid_stat(5) the comm is `updatedb.plocat`. This is derived, not observed. `updatedb` is only an alternatives symlink to that binary.
- **Caveat:** the package itself is optional. In Debian 13 plocate has `Priority: optional`, and Ubuntu 24.04 has it in universe. No `task-*`, `ubuntu-*`, `gnome*` or `kde*` meta package in the indexes read Depends on or Recommends plocate. "Enabled by default" therefore means enabled once the package is installed, not present on a default install.

**(d) Verdict:** **FOUND** (Debian 13 plocate 1.1.23-1; Ubuntu 24.04 plocate 1.1.19-2ubuntu2). The timer is enabled on install. Default installation is not established; the indexes read show no default-install path.

### C-plain-3 overall verdict
**FOUND**:
- tracker-miner-fs-3 on Debian 12 and Ubuntu 24.04, renamed localsearch-3 on Debian 13.
- baloo_file on Debian 12 and 13.
- The plocate-updatedb.timer running updatedb.plocate, enabled on install but in a package that is not installed by default.

Unreachable: none needed. The invent.kde.org `-/raw/` web URLs returned HTTP 403, and the same files were obtained with `git clone` from invent.kde.org.
