# R11 part: C-plain-4, C-plain-5

S = `_dev/research/jioh/2026-09-13-verification/sources`. All retrievals 2026-09-13.

---

## C-plain-4 — the executable/process name Jellyfin uses for transcoding on Linux, and whether it ships a renamed build

### (a) Verbatim passages

**A1. Jellyfin docs, hardware acceleration index** — `docs/general/post-install/transcoding/hardware-acceleration/index.md` line 12 (jellyfin.org @ 1edeb876):

> The Jellyfin server uses a modified version of [FFmpeg](http://ffmpeg.org/) as its transcoder, namely [jellyfin-ffmpeg](https://github.com/jellyfin/jellyfin-ffmpeg).

Same file, lines 62–66 and 76:

> Using [jellyfin-ffmpeg](https://github.com/jellyfin/jellyfin-ffmpeg/releases) with Jellyfin is highly recommended, which has a `-Jellyfin` suffix in the version string.
>
> ```shell
> $ /usr/lib/jellyfin-ffmpeg/ffmpeg
> ```

> Jellyfin-ffmpeg usually ships with our deb package, official Docker images and Windows installers.

**A2. Jellyfin docs, NVIDIA page** — `docs/general/post-install/transcoding/hardware-acceleration/nvidia.md` line 547 (example `nvidia-smi` output):

> `|    0   N/A  N/A      5837      C   /usr/lib/jellyfin-ffmpeg/ffmpeg   195MiB |`

**A3. jellyfin-ffmpeg8 package control** — `control` inside jellyfin-ffmpeg8_8.1.2-4-trixie_amd64.deb:

> Package: jellyfin-ffmpeg8
> Source: jellyfin-ffmpeg (8.1.2-4)
> Version: 8.1.2-4-trixie
> …
> This package contains a static build compatible with all Debian/Ubuntu
> releases, designed to facilitate Jellyfin on systems with an unpatched version
> of ffmpeg in their repository. Included files are:
>  * ffmpeg: a command line tool to convert multimedia files between formats
>  * ffprobe: a simple multimedia stream analyzer
>  * vainfo: a command line tool to get information about local VA-API devices

**A4. jellyfin-ffmpeg8 file list** (top-level executables; `tar -tvf data.tar.xz`):

> -rwxr-xr-x  0 root   root   431768 Sep  3 13:38 ./usr/lib/jellyfin-ffmpeg/ffmpeg
> -rwxr-xr-x  0 root   root   200640 Sep  3 13:38 ./usr/lib/jellyfin-ffmpeg/ffprobe
> -rwxr-xr-x  0 root   root    32512 Sep  3 13:38 ./usr/lib/jellyfin-ffmpeg/vainfo

(No file under `usr/bin/`; the remaining 137 entries are `usr/lib/jellyfin-ffmpeg/lib/…` shared libraries and `usr/share/doc/jellyfin-ffmpeg8/…`.)

**A5. Official packaging defaults** — `debian/conf/jellyfin` lines 30–31 (jellyfin-packaging @ v12.0-202609072105):

> \# ffmpeg binary paths, overriding the system values
> JELLYFIN_FFMPEG_OPT="--ffmpeg=/usr/lib/jellyfin-ffmpeg/ffmpeg"

`debian/conf/jellyfin.service`:

> ExecStart = /usr/bin/jellyfin $JELLYFIN_WEB_OPT $JELLYFIN_FFMPEG_OPT $JELLYFIN_SERVICE_OPT $JELLYFIN_NOWEBAPP_OPT $JELLYFIN_ADDITIONAL_OPTS

`debian/control`:

> Package: jellyfin
> Architecture: all
> Depends: jellyfin-server, jellyfin-web, jellyfin-ffmpeg8

> Package: jellyfin-server
> …
> Recommends: jellyfin-web, sudo, jellyfin-ffmpeg8 | ffmpeg

`docker/Dockerfile` line 135:

> JELLYFIN_FFMPEG="/usr/lib/jellyfin-ffmpeg/ffmpeg"

**A6. Server path resolution** — `MediaBrowser.MediaEncoding/Encoder/MediaEncoder.cs` (jellyfin @ v12.0), lines 177, 189–202, 220–221:

> /// Precedence is: CLI/Env var > Config > $PATH.

> // 1) Check if the --ffmpeg CLI switch has been given
> var ffmpegPath = _startupOptionFFmpegPath;
> …
> // 2) Custom path stored in config/encoding xml file under tag <EncoderAppPath> should be used as a fallback
> …
> // 3) Check "ffmpeg"
> ffmpegPath = "ffmpeg";

> // Determine a probe path from the mpeg path
> _ffprobePath = FfprobePathRegex().Replace(_ffmpegPath, "ffprobe$1");

Lines 785–789 (and identically 1036–1040), process launch:

> StartInfo = new ProcessStartInfo
> {
>     CreateNoWindow = true,
>     UseShellExecute = false,
>     FileName = _ffmpegPath,

`Jellyfin.Server/StartupOptions.cs` line 56:

> [Option("ffmpeg", Required = false, HelpText = "Path to external FFmpeg executable to use in place of default found in PATH.")]

**A7. How Linux derives the process name** — kernel `fs/exec.c` (v6.16) lines 1245–1247:

> } else {
> 	__set_task_comm(me, kbasename(bprm->filename), true);
> }

man-pages `proc_pid_comm.5`:

> Strings longer than
> .B TASK_COMM_LEN
> (16) characters (including the terminating null byte) are silently truncated.

### (b) Locators
As given per passage above (file path + line numbers at the named tag/commit; deb member names).

### (c) Plain-words reading
- Jellyfin's transcoder is **jellyfin-ffmpeg**, a modified FFmpeg (A1). The *package* is renamed (`jellyfin-ffmpeg8`; source `jellyfin-ffmpeg`) and installs into its own directory `/usr/lib/jellyfin-ffmpeg/`, but the *executable* is still named `ffmpeg` (with `ffprobe` next to it) (A3, A4). The only distinguishing mark the docs name is the `-Jellyfin` suffix in the version string (A1), not a different binary name.
- The official deb and Docker packaging point the server at `/usr/lib/jellyfin-ffmpeg/ffmpeg` (A5); without that option the server falls back to the config value and then to `ffmpeg` on `$PATH` (A6). `jellyfin-server` alone only *Recommends* `jellyfin-ffmpeg8 | ffmpeg`, so a distro `ffmpeg` is also acceptable — its binary is likewise `ffmpeg`.
- The server launches the transcoder directly (`UseShellExecute = false`, `FileName = _ffmpegPath`) (A6). By the kernel rule (A7) the process name (`comm`) is the basename of the executed file, so it is `ffmpeg`; the full path `/usr/lib/jellyfin-ffmpeg/ffmpeg` appears in tools that show the executable path (A2 shows it in `nvidia-smi`). The step "comm = ffmpeg" is an inference from the kernel source plus the Jellyfin launch code; no Jellyfin document states `comm` directly.
- Scope: official Jellyfin deb (Debian trixie build), official Docker image, Jellyfin server v12.0. Third-party distribution packages of Jellyfin (Arch, Nix, Fedora, etc.) and the portable tarballs were not checked. Windows/macOS out of scope.

### (d) Verdict
**FOUND** — transcoder executable `ffmpeg` (path `/usr/lib/jellyfin-ffmpeg/ffmpeg` in official packaging), a patched FFmpeg build shipped under a renamed package/directory but not a renamed executable.

---

## C-plain-5 — process names of scheduled/automatic ML training, media rendering, transcoding and backup jobs that distributions or vendors start without the user

Answered per job kind. "Distribution" evidence is Debian 13 (trixie, point release 13.7) main, amd64; "vendor" evidence is Jellyfin 12.0, Plex Media Server 1.43.4, Immich v3.2.0. Other distributions (Ubuntu, Fedora, openSUSE, Arch) were not checked.

### C-plain-5.1 — ML training

#### (a)/(b) Verbatim passages
**Immich v3.2.0 (vendor ML service).** `machine-learning/Dockerfile` lines 166–167:

> ENTRYPOINT ["tini", "--"]
> CMD ["python", "-m", "immich_ml"]

`machine-learning/README.md` lines 1–4 and 17:

> \# Immich Machine Learning
>
> - CLIP embeddings
> - Facial recognition

> To measure inference throughput and latency, you can use [Locust](https://locust.io/) using the provided `locustfile.py`.

`machine-learning/immich_ml/main.py` lines 156, 161, 166 (the HTTP routes):

> @app.get("/")
> @app.get("/ping")
> @app.post("/predict", dependencies=[Depends(update_state)])

`docker/docker-compose.yml` line 35: `container_name: immich_machine_learning`

#### How searched
1. Debian trixie main amd64 Contents index (md5-verified against Release), filtered to every systemd timer unit (82 entries), every `etc/cron.{d,daily,hourly,weekly,monthly}/` file (101), every `etc/xdg/autostart/` entry (176) and every `usr/lib/systemd/user/` unit (291); all names grepped (case-insensitive) for `train|learn|model|neural|ml[-_.]`. Result: zero hits. Full timer-name list is in S/C-plain-5/debian-trixie-main-amd64-Contents-timers.txt (e.g. apt-daily, man-db, plocate-updatedb, fstrim, logrotate, dpkg-db-backup, snapper-timeline, sysstat-collect — none ML).
2. WebSearch "Linux desktop distribution default background machine learning model training systemd timer on-device training" — only patents and generic systemd-timer pages; no distribution artifact.
3. Immich as a vendor that auto-runs ML: its ML service exposes only `/`, `/ping`, `/predict`; `grep -c train main.py` = 0.

#### (c) Reading
No distribution-default ML **training** job was found within the scope searched (file names of timers/cron/autostart/user units in Debian trixie main; this does not see scheduling implemented inside an application's own code). The one vendor ML service checked (Immich) does inference (CLIP embeddings, facial recognition via `/predict`), not training; its process runs as `python -m immich_ml` in the `immich_machine_learning` container (so `comm` would be the Python interpreter name, e.g. `python`/`python3.x` — inference from A7 in C-plain-4, not stated by Immich). When Immich triggers these jobs was not read.

#### (d) Verdict
**NOT FOUND** (searches above). The premise that distributions/vendors start ML *training* without the user is not supported by any source read.

### C-plain-5.2 — media rendering (thumbnails / preview images)

#### (a)/(b) Verbatim passages
**Jellyfin v12.0 scheduled tasks** — `MediaBrowser.Providers/Trickplay/TrickplayImagesTask.cs` lines 54, 60–69:

> public string Key => "RefreshTrickplayImages";

> public IEnumerable<TaskTriggerInfo> GetDefaultTriggers()
> {
>     return
>     [
>         new TaskTriggerInfo
>         {
>             Type = TaskTriggerInfoType.DailyTrigger,
>             TimeOfDayTicks = TimeSpan.FromHours(3).Ticks
>         }
>     ];

`Emby.Server.Implementations/ScheduledTasks/Tasks/ChapterImagesTask.cs` lines 69, 74–79:

> public string Key => "RefreshChapterImages";

> yield return new TaskTriggerInfo
> {
>     Type = TaskTriggerInfoType.DailyTrigger,
>     TimeOfDayTicks = TimeSpan.FromHours(2).Ticks,
>     MaxRuntimeTicks = TimeSpan.FromHours(4).Ticks
> };

Image extraction in `MediaEncoder.cs` (methods `ExtractImageInternal` line 674, `ExtractVideoImagesOnIntervalInternal` line 974) launches `FileName = _ffmpegPath` (lines 789, 1040; quoted in C-plain-4 A6).

Gating library options — jellyfin-web v12.0 `src/components/libraryoptionseditor/libraryoptionseditor.template.html` lines 125 and 152 (checkboxes rendered **without** `checked`):

> <input type="checkbox" is="emby-checkbox" class="chkExtractTrickplayImages" />

> <input type="checkbox" is="emby-checkbox" class="chkExtractChapterImages" />

Server `MediaBrowser.Model/Configuration/LibraryOptions.cs` lines 51, 55 (not assigned in the constructor, lines 13–41):

> public bool EnableChapterImageExtraction { get; set; }
> public bool EnableTrickplayImageExtraction { get; set; }

**Debian thumbnailer** — `usr/share/thumbnailers/ffmpegthumbnailer.thumbnailer` in ffmpegthumbnailer 2.2.3-2:

> [Thumbnailer Entry]
> TryExec=ffmpegthumbnailer
> Exec=ffmpegthumbnailer -i %i -o %o -s %s -f

Debian trixie Contents also lists `usr/lib/systemd/user/ethumb.service  libs/libethumb-client-bin` (file not read).

#### (c) Reading
- Jellyfin (vendor) defines daily trickplay-image (03:00) and chapter-image (02:00) tasks that run the `ffmpeg` binary (comm `ffmpeg`) without a user action — but only for libraries where those options are on, and both options default to off in the v12.0 web form and server model. So out of the box they do nothing until an admin enables the option.
- Debian's video thumbnailer entry runs `ffmpegthumbnailer` (17 characters → `comm` truncated to `ffmpegthumbnail` by the TASK_COMM_LEN rule; inference). Which component invokes thumbnailers, and whether it does so without a user browsing files, was not read in this pass (GNOME/KDE thumbnail factory source not opened).
- No distribution artifact that renders media (e.g. Blender/video render) on a schedule was found in the timer/cron/autostart name scan (keywords `thumb|render` matched nothing except `ethumb.service`).

#### (d) Verdict
**PARTIAL** — process names found for vendor scheduled image extraction (`ffmpeg`, off by default) and for the Debian thumbnailer binary (`ffmpegthumbnailer`); no distribution-started scheduled rendering job found.

### C-plain-5.3 — transcoding

#### (a)/(b) Verbatim passages
**Jellyfin v12.0** — `src/Jellyfin.MediaEncoding.Hls/ScheduledTasks/KeyframeExtractionScheduledTask.cs` lines 44, 109:

> public string Key => "KeyframeExtraction";

> public IEnumerable<TaskTriggerInfo> GetDefaultTriggers() => [];

`Emby.Server.Implementations/ScheduledTasks/Tasks/AudioNormalizationTask.cs` lines 74, 221–225, 230, 236:

> public string Key => "AudioNormalization";

> yield return new TaskTriggerInfo
> {
>     Type = TaskTriggerInfoType.IntervalTrigger,
>     IntervalTicks = TimeSpan.FromHours(24).Ticks
> };

> var args = $"-hide_banner {inputArgs} -af ebur128=framelog=verbose -f null -";

> FileName = _mediaEncoder.EncoderPath,

jellyfin-web v12.0 `libraryoptionseditor.template.html` line 68 and `libraryoptionseditor.js` line 550:

> <input type="checkbox" is="emby-checkbox" class="chkEnableLUFSScan" checked />

> parent.querySelector('.chkEnableLUFSScanContainer').classList.toggle('hide', contentType !== 'music');

**Plex Media Server 1.43.4** — file list of plexmediaserver_1.43.4.10903-e5521bd8c_amd64.deb:

> -rwxr-xr-x  0 root   root   361360 Aug 17 05:55 ./usr/lib/plexmediaserver/Plex Transcoder
> -rwxr-xr-x  0 root   root 23433320 Aug 17 06:16 ./usr/lib/plexmediaserver/Plex Media Server
> -rwxr-xr-x  0 root   root  5899248 Aug 17 06:16 ./usr/lib/plexmediaserver/Plex Media Scanner

`usr/lib/plexmediaserver/lib/plexmediaserver.service` line 30: `exec "/usr/lib/plexmediaserver/Plex Media Server"'`; `control/postinst` line 458: `    systemctl enable plexmediaserver`

Plex Support "Scheduled Tasks" (Last modified July 31, 2025):

> You can choose the (local to the server) hour at which the background maintenance tasks should start and end. This defaults to starting at 3am and ending at 6am.

> Upgrade media analysis during maintenance
> We do extensive media analysis on every file to ensure correct playback across the huge range of devices and apps.

> Perform extensive media analysis during maintenance
> This does an extensive bitrate analysis on each file in your library to help with bandwidth controls.

#### (c) Reading
- Jellyfin's only scheduled tasks that invoke the transcoder binary without a user are analysis/extraction tasks, not format conversion: audio normalization runs `ffmpeg … -af ebur128 … -f null -` every 24 h (LUFS scan checkbox is pre-checked for music libraries in the v12.0 form), keyframe extraction has no default trigger, and image extraction is covered in 5.2. Process name `ffmpeg`.
- Plex ships a separate `Plex Transcoder` binary (15 characters, fits `comm` unchanged — inference) and its maintenance window (default 03:00–06:00) runs media-analysis tasks inside the enabled `plexmediaserver` service; the Plex article does not say which binary performs those tasks, so linking them to `Plex Transcoder` is not supported by the source.
- No source read shows a distribution or vendor starting an actual transcode (format conversion) job on a schedule without a user request. On-demand playback transcoding in Jellyfin/Plex is user-triggered and was not traced in source here.
- Debian timer/cron/autostart name scan: no `transcod` hits.

#### (d) Verdict
**PARTIAL** — transcoder process names found (`ffmpeg` for Jellyfin, `Plex Transcoder` for Plex) and vendor scheduled media *analysis* jobs found; no scheduled, user-less *transcoding* job found in any source read.

### C-plain-5.4 — backup

#### (a)/(b) Verbatim passages
**dpkg 1.22.22 (Debian essential package)** — `usr/lib/systemd/system/dpkg-db-backup.timer`:

> [Unit]
> Description=Daily dpkg database backup timer
> Documentation=man:dpkg(1)
>
> [Timer]
> OnCalendar=daily
> Persistent=true
>
> [Install]
> WantedBy=timers.target

`usr/lib/systemd/system/dpkg-db-backup.service`:

> [Service]
> Type=oneshot
> ExecStart=/usr/libexec/dpkg/dpkg-db-backup

`control/postinst` lines 54–58:

> 	# was-enabled defaults to true, so new installations run enable.
> 	if deb-systemd-helper --quiet was-enabled 'dpkg-db-backup.timer'; then
> 		# Enables the unit on first installation, creates new
> 		# symlinks on upgrades if the unit file has changed.
> 		deb-systemd-helper enable 'dpkg-db-backup.timer' >/dev/null || true

`usr/libexec/dpkg/dpkg-db-backup` line 1 and lines 18–19: `#!/bin/sh` / `ADMINDIR='/var/lib/dpkg'` / `BACKUPSDIR='/var/backups'`

Kernel (script case): `fs/binfmt_script.c` line 125 `retval = bprm_change_interp(i_name, bprm);` and `fs/exec.c` `bprm_change_interp` lines 1475–1480 change only `bprm->interp` (`bprm->interp = kstrdup(interp, GFP_KERNEL);`), leaving `bprm->filename` for `__set_task_comm(me, kbasename(bprm->filename), true);`.

**Déjà Dup 45.2-3+b1** — `etc/xdg/autostart/org.gnome.DejaDup.Monitor.desktop`:

> Name=Backup Monitor
> Comment=Schedules backups at regular intervals
> …
> Exec=/usr/libexec/deja-dup/deja-dup-monitor
>
> X-GNOME-Autostart-Delay=120

`usr/share/glib-2.0/schemas/org.gnome.DejaDup.gschema.xml` lines 48–52, 98–99:

> <key name="periodic" type="b">
>   <default>false</default>
>   <summary>Whether to periodically back up</summary>

> <key name="tool" type="s">
>   <default>'duplicity'</default>

Upstream 45.2 `monitor/BackupInterface.vala` line 39: `DejaDup.run_deja_dup({"--backup", "--auto"});`
`libdeja/CommonUtils.vala` lines 134, 118, 127, 129: `public void run_deja_dup(string[] args = {}, string exec = "deja-dup")` / `cmd = "ionice -c3 " + cmd; // idle class` / `cmd = "chrt --idle 0 " + cmd;` / `cmd = "nice -n19 " + cmd;`
Debian `Depends: duplicity (>= 0.7.14), …`

**Timeshift 24.06.6-2** — package file list has no cron or systemd file (only `./etc/timeshift/default.json`, `./usr/bin/timeshift`, `./usr/bin/timeshift-gtk`, `./usr/bin/timeshift-launcher`, docs, images, polkit policy). `etc/timeshift/default.json` lines 8–12:

> "schedule_monthly" : "false",
> "schedule_weekly" : "false",
> "schedule_daily" : "false",
> "schedule_hourly" : "false",
> "schedule_boot" : "false",

Upstream 24.06.6 `src/Core/Main.vala` lines 4244–4251:

> if (scheduled){
> 	
> 	//hourly
> 	CronTab.add_script_file("timeshift-hourly", "d", "0 * * * * root timeshift --check --scripted", stop_cron_emails);
> 	
> 	//boot
> 	if (schedule_boot){
> 		CronTab.add_script_file("timeshift-boot", "d", "@reboot root sleep 10m && timeshift --create --scripted --tags B", stop_cron_emails);

**Kup 0.10.0-1+b1 (KDE)** — `etc/xdg/autostart/kup-daemon.desktop` lines 36, 69, 76:

> GenericName=Backup Monitor
> Exec=kup-daemon
> X-KDE-autostart-condition=kuprc:Kup settings:Backups enabled:true

**Plex Media Server (vendor)** — Plex Support "Scheduled Tasks":

> Backup database every three days
> Every three days, a backup of your core SQL database file will be created (if it is not already corrupted).

#### (c) Reading
- **Found, on by default:** Debian's `dpkg` ships `dpkg-db-backup.timer`, enabled at install, running daily `/usr/libexec/dpkg/dpkg-db-backup`, a `/bin/sh` script that tars the dpkg database into `/var/backups`. Process name `dpkg-db-backup` (script basename per the kernel code above; inference), with `tar`/`savelog` child processes. This is a small system-metadata backup, not a user-data backup.
- **Monitor on by default, backup off:** Déjà Dup's monitor autostarts in every GNOME session (`deja-dup-monitor`, 16 characters → `comm` `deja-dup-monito`; inference), but `periodic` defaults to `false`. When a user turns it on, the monitor runs `deja-dup --backup --auto` behind `ionice`/`chrt`/`nice` (those exec the command, so the final process is `deja-dup`), with the default tool `duplicity`. Déjà Dup is not installed by default in Debian; which desktops pull it in was not checked.
- **Off by default:** Timeshift ships no scheduler and all schedules default to false; enabling one writes `/etc/cron.d/timeshift-hourly` running `timeshift --check --scripted` as root. Kup's daemon autostarts only if `Backups enabled:true`.
- **Vendor:** Plex backs up its own database every three days inside the always-enabled `plexmediaserver` service. The article names no separate process, so it presumably runs inside `Plex Media Server` (17 characters → `Plex Media Serv`) — not confirmed by the source.
- Also in the Debian timer scan but not read: `boxbackup-client.timer`, `burp.timer`, `snapper-timeline.timer` (snapshots), `etc/cron.*/rsbackup`. These are admin tools that need configuration.

#### (d) Verdict
**FOUND** for one distribution job started without the user (`dpkg-db-backup`, Debian trixie). Desktop and user-data backup tools checked (Déjà Dup, Timeshift, Kup) ship with scheduling off by default, and their process names are recorded above.

### C-plain-5 overall verdict
Per job kind: ML training **NOT FOUND**; media rendering **PARTIAL**; transcoding **PARTIAL**; backup **FOUND** (dpkg-db-backup), with the desktop backup tools off by default.
