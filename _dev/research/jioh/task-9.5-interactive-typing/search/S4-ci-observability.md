# S4 — own measurement on a CI runner (T7): search record

Reader S4. Date of all searches and fetches: 2026-09-13. Class: what a GitHub Actions hosted runner can and cannot observe of the topics, established from primary documentation and source only — nothing was installed or run. Every passage below is quoted verbatim from a copy saved under `sources/S4-<id>/` (gitignored); each copy is identified by URL or commit, version, access date and SHA-256, so the record stands without the local files. `file:line` locators refer to line numbers in the saved copy (identical to upstream at the commit named).

Coverage note that applies to every candidate: all candidates are documentation or source code; none is an observation (no population, trace, machine, subject or window is measured). Every candidate covers T7 only and does not cover T1–T6 unless a row says otherwise.

## 1. Search log

| # | Date | Engine / venue | Query or URL | Hits followed | Dead ends (HTTP status) |
|---|------|----------------|--------------|---------------|-------------------------|
| 1 | 2026-09-13 | raw.githubusercontent.com (curl) | actions/runner-images `main`: `images/ubuntu/Ubuntu2404-Readme.md`, `images/ubuntu/toolsets/toolset-2404.json` | both 200 → S4-01 | — |
| 2 | 2026-09-13 | api.github.com (curl) | `repos/actions/runner-images/commits?path=…` for a commit id | — | 200 body "GitHub access to this repository is not enabled for this session" (API gated). Commit ids taken instead from `git ls-remote` (see row 30). |
| 3 | 2026-09-13 | raw.githubusercontent.com | github/docs `main`: `content/actions/reference/runners/github-hosted-runners.md`; `data/reusables/actions/supported-github-runners.md` | both 200 → S4-02 | `content/actions/using-github-hosted-runners/using-github-hosted-runners/about-github-hosted-runners.md` 404 |
| 4 | 2026-09-13 | salsa.debian.org raw | xorg-team/xserver/xorg-server `debian-unstable`: `debian/local/xvfb-run.1`, `debian/local/xvfb-run` | both 200 → S4-04 | — |
| 5 | 2026-09-13 | gitlab.freedesktop.org raw | `xorg/xserver/xserver/-/raw/master/hw/vfb/man/Xvfb.man` | — | 200 but body was a GitLab sign-in HTML page (wrong project path); discarded |
| 6 | 2026-09-13 | gitlab.freedesktop.org raw | `xorg/xserver/-/raw/master/hw/vfb/man/Xvfb.man` | 200 → S4-03 | — |
| 7 | 2026-09-13 | raw.githubusercontent.com | jordansissel/xdotool `master` `xdotool.pod` | 200 → S4-05 | — |
| 8 | 2026-09-13 | raw.githubusercontent.com | ReimuNotMoe/ydotool `master`: `README.md`, `manpage/ydotool.1.scd`, `manpage/ydotoold.8.scd` | all 200 → S4-06 | — |
| 9 | 2026-09-13 | raw.githubusercontent.com | microsoft/playwright `main`: `docs/src/api/class-keyboard.md`, `docs/src/ci.md`, `docs/src/browsers.md` | 200 → S4-08 | `docs/src/api/class-electron.md` 404 (page lives at `docs/src/electron-api/class-electron.md`, found via sparse clone, row 31) |
| 10 | 2026-09-13 | raw.githubusercontent.com | mpv-player/mpv `master`: `DOCS/man/ao.rst`, `vo.rst`, `options.rst`; FFmpeg `doc/ffplay.texi` | 200 → S4-13 (ffplay read, not cited) | — |
| 11 | 2026-09-13 | raw.githubusercontent.com | torvalds/linux `master`: `tools/perf/Documentation/perf-sched.txt`, `Documentation/scheduler/sched-stats.rst`, `Documentation/admin-guide/perf-security.rst`, `Documentation/trace/ftrace.rst`, `Documentation/trace/events.rst` | all 200 → S4-16, S4-17, S4-18, S4-19 | — |
| 12 | 2026-09-13 | raw.githubusercontent.com | mkerrisk/man-pages `master` `man5/proc_pid_{stat,status,schedstat,task}.5` | — | all four 404 (repository moved) |
| 13 | 2026-09-13 | git.kernel.org cgit plain | man-pages `man/man5/proc_pid_stat.5`, `proc_pid_status.5`, `proc_pid_task.5`, `proc_pid_schedstat.5` | three 200 → S4-15 | `proc_pid_schedstat.5` 404 (no such page; schedstat is documented by the kernel, S4-16) |
| 14 | 2026-09-13 | gitlab.freedesktop.org raw + API | libevdev/evemu `master`: `tools/evemu-record.txt`, `tools/evemu-play.txt` | — | both 404; API tree of `tools/` listed `evemu-describe.txt`, `evemu-device.txt` only |
| 15 | 2026-09-13 | gitlab.freedesktop.org raw | libevdev/evemu: `tools/evemu-describe.txt`, `tools/evemu-device.txt`, `README.md`, `src/evemu.c`, `tools/evemu-play.c`, `tools/evemu-record.c` | all 200 → S4-07 | — |
| 16 | 2026-09-13 | raw.githubusercontent.com | strace/strace `doc/strace.1.in`; rostedt/trace-cmd `Documentation/trace-cmd/trace-cmd-record.1.txt` | 200 → S4-20, S4-19 | — |
| 17 | 2026-09-13 | gitlab.freedesktop.org raw | mesa/mesa `main` `docs/drivers/llvmpipe.rst` | 200 → S4-24 | — |
| 18 | 2026-09-13 | gitlab.freedesktop.org raw + API | pipewire/pipewire `master`: `spa/plugins/support/null-audio-sink.c`, `src/daemon/pipewire.conf.in`, `src/modules/module-protocol-pulse/modules/pulse-module-null-sink.c` | 200 → S4-22 | `…/modules/module-null-sink.c` 404 (file is named `pulse-module-null-sink.c`, found via API tree) |
| 19 | 2026-09-13 | gitlab.freedesktop.org raw | pulseaudio/pulseaudio `master`: `src/modules/module-null-sink.c`, `man/pulseaudio.1.xml.in` | 200 → S4-23 (man page read, not cited) | — |
| 20 | 2026-09-13 | gitlab.gnome.org raw | GNOME/gimp `master` `.gitlab-ci.yml` | 200 → S4-11 | — |
| 21 | 2026-09-13 | gimp.org | `https://www.gimp.org/tutorials/Basic_Batch/` | — | 200 but a 143-byte `<meta http-equiv="refresh">` stub to `/tutorials/legacy/Basic_Batch/`; not followed (GIMP's CI file, S4-11, answers the batch-mode question) |
| 22 | 2026-09-13 | invent.kde.org raw + API | multimedia/kdenlive `master` `.kde-ci.yml`; sysadmin/ci-utilities `master`: `components/TestHandler.py`, `run-ci-build.py`, `gitlab-templates/linux-qt6.yml`, `gitlab-templates/linux.yml`; sdk/selenium-webdriver-at-spi `README.md` | 200 → S4-12 | `run-tests.py` 404 (no such file; tree listed `run-ci-build.py`); `gitlab-templates/linux.yml` 200 but 0 bytes |
| 23 | 2026-09-13 | raw.githubusercontent.com | microsoft/vscode `main`: `.github/workflows/pr.yml`, `build/azure-pipelines/linux/product-build-linux.yml`, `test/automation/src/playwrightDriver.ts`, `test/automation/src/code.ts` | 200 (superseded by sparse clone, row 31) | `.github/workflows/ci.yml`, `basePr.yml`, `build/azure-pipelines/linux/product-build-linux-test.yml` 404 |
| 24 | 2026-09-13 | raw.githubusercontent.com | LibreOffice/core `master`: `uitest/uitest/uihelper/common.py`, `uitest/README.md`, `solenv/gbuild/UITest.mk`, `uitest/test_main.py`, `uitest/uitest/framework.py`, `uitest/libreoffice/connection.py`, `desktop/source/app/cmdlinehelp.cxx`, `sw/UITest_writer_tests.mk` | 200 (superseded by sparse clone, row 31) | `sw/UITest_sw_writer.mk` 404; `sw/qa/uitest/writer_tests/tdf53460.py` 404 |
| 25 | 2026-09-13 | chromium.googlesource.com gitiles | `chromium/src/+/main/headless/README.md?format=TEXT` | 200 (base64) → S4-14 | — |
| 26 | 2026-09-13 | raw.githubusercontent.com | bpftrace/bpftrace `master`: `tools/runqlat.bt`; iovisor/bcc `master`: `tools/offcputime_example.txt`, `INSTALL.md` | 200 → S4-21 | bpftrace `tools/runqlat_example.txt` 404, `INSTALL.md` 404, `docs/install.md` 404 |
| 27 | 2026-09-13 | git.launchpad.net cgit plain | `~ubuntu-kernel/ubuntu/+source/linux-azure/+git/noble/plain/debian.azure/config/annotations` (kernel config: CONFIG_SND*, CONFIG_INPUT_UINPUT) | — | 403 (twice, with and without -L); `git ls-remote` to the same repo failed with an authentication prompt |
| 28 | 2026-09-13 | packages.ubuntu.com | `/noble/linux-tools-azure`, `/noble/xdotool`, `/noble/ydotool`, `/noble/evemu-tools`, `/noble-updates/linux-image-6.17.0-1022-azure`, `/noble-updates/amd64/linux-modules-6.17.0-1022-azure/filelist`, `/noble-updates/amd64/linux-modules-extra-6.17.0-1022-azure/filelist` | all 200 → S4-25 | — |
| 29 | 2026-09-13 | github.com HTML (curl) | `actions/runner-images/issues/1114`, `/11789`, `/11689`, `/4974`; `orgs/community/discussions/45004` | — | all five 403 |
| 30 | 2026-09-13 | git ls-remote / GitLab API `commits?per_page=1` | HEAD commit ids for every repository fetched raw (recorded in each `SOURCE.txt` and in section 2) | — | `gitlab.freedesktop.org/xorg/xserver/xserver` ls-remote failed (auth prompt; wrong path) — replaced by API commit of `xorg/xserver` |
| 31 | 2026-09-13 | git clone --depth 1 --filter=blob:none --sparse | microsoft/vscode @ 3e8601c5f63f5b2358e0fbbfb825fbbfd72cbe2b (`.github/workflows`, `build/azure-pipelines/linux`, `test/automation/src`); LibreOffice/core @ 2410e6d5e8f08f537a76027be263849a52181b2c (`uitest`, `sw/qa/uitest`, `solenv/gbuild`, `desktop/source/app`); microsoft/playwright @ d1ead3ecca23182f2d06d761c28e3d4edafb6595 (`docs/src`) | grep for `xvfb`, `DISPLAY`, `_electron`, `type_text`, `SAL_USE_VCLPLUGIN`, `headless` → S4-08, S4-09, S4-10 | — |
| 32 | 2026-09-13 | WebSearch | `"actions/runner-images" issue audio device sound card pulseaudio "ubuntu-latest" no sound` | none relevant (generic Ubuntu audio troubleshooting pages) | — |
| 33 | 2026-09-13 | WebSearch | `"runner-images" perf "perf_event_paranoid" github actions ubuntu perf record not working` | leads: runner-images issues #11789, #11689, #4974; community discussion #45004 — all unreadable (row 29, 35, 36) | — |
| 34 | 2026-09-13 | WebSearch | `github actions ubuntu "snd-aloop" OR "snd-dummy" modprobe runner audio loopback` | lead: runner-images (then `actions/virtual-environments`) issue #1114 "Add soundcore and snd-aloop kernel modules" — unreadable (row 29, 35, 36) | — |
| 35 | 2026-09-13 | WebFetch (model summary of page) | issues #1114, #11789; discussion #45004 | Summaries obtained; they are paraphrases produced by a fetch model, not verbatim copies, and no file could be saved or hashed — **not cited**. Recorded here only as leads: #1114 (opened 2020-06-24, closed) asks for `snd-aloop`/`soundcore` on Ubuntu runners; #11789 (opened 2025-03-13, closed) concerns `perf stat` power events; #45004 concerns `perf` in Codespaces (`<not supported>` hardware counters). | — |
| 36 | 2026-09-13 | GitHub MCP `issue_read` | actions/runner-images #1114, #11789, #11689 | — | "Access denied: repository actions/runner-images is not configured for this session" (×3) |
| 37 | 2026-09-13 | WebSearch | `Azure virtual machine audio device sound card not supported Hyper-V generation 2 "audio"` | none primary (Hyper-V forum/Q&A posts only; none fetched) | — |
| 38 | 2026-09-13 | WebSearch | `site:github.com/actions/runner-images pulseaudio OR pipewire "null-sink" OR "no sound card" ubuntu runner` | none relevant (site: operator not honoured) | — |
| 39 | 2026-09-13 | WebSearch | `LibreOffice jenkins "uitest" OR "UITest" xvfb OR "SAL_USE_VCLPLUGIN" CI tinderbox headless gen` | none primary (two tinderbox failure mails, generic Jenkins/Xvfb pages) | — |

Totals: 6 WebSearch queries, 3 WebFetch summaries (not citable), 3 MCP reads (denied), 3 sparse clones, roughly 85 curl fetches of which 62 returned usable copies.

## 2. Candidates

### S4-01 — actions/runner-images, Ubuntu 24.04 image readme and toolset

- **Citation.** GitHub, `actions/runner-images`, `images/ubuntu/Ubuntu2404-Readme.md` and `images/ubuntu/toolsets/toolset-2404.json`, image version 20260907.300.1.
- **Copy read.** `https://raw.githubusercontent.com/actions/runner-images/main/images/ubuntu/Ubuntu2404-Readme.md` and `…/toolsets/toolset-2404.json`, branch `main` whose HEAD at access was `bac22751eb7d886e12c6063685275299469e9e5b`; accessed 2026-09-13; local `sources/S4-runner-images-2404/`; SHA-256 readme `4edbefde1df512f024363b1f66f78448f944f071c9e1775056b220d5bdc8dc81`, toolset `291c28ea606bdbf16ec8f11c1b60d54c97f1cf0496b23060771c05cbc1391414`.
- **Passages.**
  - `Ubuntu2404-Readme.md:9-11`: "- OS Version: 24.04.5 LTS" / "- Kernel Version: 6.17.0-1022-azure" / "- Image Version: 20260907.300.1"
  - `Ubuntu2404-Readme.md:147-154` (section "### Browsers and Drivers"): "- Google Chrome 152.0.7977.82" … "- Chromium 152.0.7977.0" … "- Mozilla Firefox 155.0"
  - `Ubuntu2404-Readme.md:329` (table "### Installed apt packages"): "| xvfb                   | 2:21.1.12-1ubuntu1.6         |"
  - `toolset-2404.json:150` (array `apt.common_packages`): `"xvfb",`
  - Absence (my grep over the whole readme, pattern `xdotool|libreoffice|pulseaudio|pipewire|ffmpeg|mpv|mesa|alsa|linux-tools|strace|evemu|ydotool|gimp`): no line of the apt table or any other section names any of these packages. Only `xvfb` (line 329), `dbus` (line 269) and `fonts-noto-color-emoji` (line 277) match display-related packages.
- **Coverage.** T7: covers the runner's kernel flavour (`azure`), the installed X virtual framebuffer (`xvfb` package present in the image) and installed browsers (Chrome, Chromium, Firefox); establishes by absence that xdotool, ydotool, LibreOffice, GIMP, mpv, PulseAudio/PipeWire, ffmpeg and perf/`linux-tools` are not preinstalled (they would have to be apt-installed in the job). T1–T6: does not cover.
- **Observation?** No — documentation.

### S4-02 — GitHub Docs, "GitHub-hosted runners reference"

- **Citation.** GitHub Docs, `content/actions/reference/runners/github-hosted-runners.md` with reusable `data/reusables/actions/supported-github-runners.md`, repository `github/docs`.
- **Copy read.** `https://raw.githubusercontent.com/github/docs/main/content/actions/reference/runners/github-hosted-runners.md` and `https://raw.githubusercontent.com/github/docs/main/data/reusables/actions/supported-github-runners.md`, branch `main` HEAD `078b5832caa5cde591c2babb389ef447a0ef66eb` at access; accessed 2026-09-13; local `sources/S4-github-docs-hosted-runners/`; SHA-256 `2ba4307f64e55251e63555e97a51381e4eb36334693a464c743522a09546a148` and `ffce1176fb7f6571c2beabacc95ba78600b275152ff92e2c051935583a56070c`.
- **Passages.**
  - `supported-github-runners.md:19-26` (table "Standard … hosted runners for public repositories"): "<td>Linux</td>" / "<td>4</td>" / "<td>16 GB</td>" / "<td>14 GB</td>" / "<td> x64 </td>" … "ubuntu-latest" … "ubuntu-24.04" (columns: Processor (CPU), Memory (RAM), Storage (SSD), Architecture, Workflow label).
  - `github-hosted-runners.md:77`: "The Linux and macOS virtual machines both run using passwordless `sudo`. When you need to execute commands or install tools that require more privileges than the current user, you can use `sudo` without needing to provide a password."
  - `github-hosted-runners.md:85`: "Windows and Ubuntu runners are hosted in Azure and subsequently have the same IP address ranges as the Azure datacenters."
- **Coverage.** T7: covers the runner's resources (4 vCPU, 16 GB RAM, x64 for `ubuntu-24.04` on public repositories), root access (passwordless sudo — relevant to `perf`, tracefs, `/dev/uinput`, `modprobe`), and hosting (Azure VM). Says nothing about GPU, audio hardware or perf availability. T1–T6: does not cover.
- **Observation?** No.

### S4-03 — Xvfb(1)

- **Citation.** X.Org Server, `hw/vfb/man/Xvfb.man`, "Xvfb - virtual framebuffer X server for X Version 11".
- **Copy read.** `https://gitlab.freedesktop.org/xorg/xserver/-/raw/master/hw/vfb/man/Xvfb.man`, `master` HEAD `bd3ca7da06ec5634e29a0242bf99f6a8e57a7389` at access; accessed 2026-09-13; local `sources/S4-xvfb/Xvfb.man`; SHA-256 `9cda6c2f13e084167c8a0e70a1e0cc454af9e9cacab2cab4fe10141fb3403e43`.
- **Passages.**
  - `Xvfb.man:36-40` (DESCRIPTION): "is an X server that can run on machines with no display hardware / and no physical input devices.  It emulates a dumb framebuffer using / virtual memory."
  - `Xvfb.man:41-49`: "The primary use of this server was intended to be server testing. … doing batch processing with \fIXvfb\fP as a background rendering engine, load testing, … and providing an unobtrusive way to run applications that don't really need an X server but insist on having one anyway."
  - `Xvfb.man:56-58` (`-screen`): "This option creates screen \fIscreennum\fP and sets its width, height, and depth to W, H, and D respectively.  By default, only screen 0 exists and has the dimensions 1280x1024x24."
  - Absence: the man page contains no occurrence of "refresh", "vblank", "vsync" or "rate" (my grep). It documents no display refresh cadence at all.
- **Coverage.** T7: covers what Xvfb is (a memory framebuffer with no display hardware and no physical input devices) — the basis for "a runner cannot observe real display refresh": the document states there is no display hardware and documents no refresh timing. T1–T6: does not cover.
- **Observation?** No.

### S4-04 — xvfb-run(1) (Debian)

- **Citation.** Debian xorg-server packaging, `debian/local/xvfb-run.1`, "xvfb-run - run specified X client or command in a virtual X server environment", dated 2004-11-12.
- **Copy read.** `https://salsa.debian.org/xorg-team/xserver/xorg-server/-/raw/debian-unstable/debian/local/xvfb-run.1` (and the script `xvfb-run`), branch `debian-unstable` HEAD `8744d4a95e277b4269d5ac3a873983ece2b7478a`; accessed 2026-09-13; local `sources/S4-xvfb-run/`; SHA-256 man `7e8e39c98ae006b8ba583b59c8be0419885eaead062c3ae87592854de33e5a00`, script `97e86a102eee7212bfa3bf87d452b27dd4f16ef6e68658eeae20bca63db2ceee`.
- **Passages.**
  - `xvfb-run.1:36-41`: "is a wrapper for the / .BR Xvfb (1x) / command which simplifies the task of running commands (typically an X client, or a script containing a list of clients to be run) within a virtual X server environment."
  - `xvfb-run.1:43-58`: "sets up an X authority file (or uses an existing user\-specified one), writes a cookie to it … and then starts the / .B Xvfb / X server as a background process. … The specified / .I command / is then run using the X display corresponding to the / .B Xvfb / server just started".
- **Coverage.** T7: covers the mechanism by which a job step runs a GUI program under Xvfb (`xvfb-run <command>`). T1–T6: does not cover.
- **Observation?** No.

### S4-05 — xdotool(1)

- **Citation.** Jordan Sissel, xdotool, `xdotool.pod` (source of the man page).
- **Copy read.** `https://raw.githubusercontent.com/jordansissel/xdotool/master/xdotool.pod`, `master` HEAD `5c27b117c91bdc4d0f56a71ac4e78c04e4e60dba`; accessed 2026-09-13; local `sources/S4-xdotool/xdotool.pod`; SHA-256 `658d90981117e78d83e043af0a0932b11b2dc9dea9fd830e247eaa94720a4338`.
- **Passages.**
  - `xdotool.pod:28` "=item B<key> I<[options]> I<keystroke> [I<keystroke> ...]"; `:42-48`: "=item B<--clearmodifiers> / Clear modifiers before sending keystrokes. See L<CLEARMODIFIERS> below. / =item B<--delay milliseconds> / Delay between keystrokes. Default is 12ms."
  - `xdotool.pod:87` "=item B<type> I<[options]> I<something to type>"; `:94-98`: "Send keystrokes to a specific window id. See L<SENDEVENT NOTES> below. The default, if no window is given, depends on the window stack. If the window stack is empty the current window is typed at using XTEST."; `:100-102`: "=item B<--delay milliseconds> / Delay between keystrokes. Default is 12ms."; `:110-111`: "Types as if you had typed it. Supports newlines and tabs (ASCII newline and tab). Each keystroke is separated by a delay given by the B<--delay> option."; `:113-114`: "this command consumes the remainder of the arguments and types them. That is, no commands can chain after 'type'."
  - `xdotool.pod:963-966`: "=item B<sleep> I<seconds> / Sleep for a specified period. Fractions of seconds (like 1.3, or 0.4) are valid, here."
  - `xdotool.pod:970-985` (SCRIPTS): "xdotool can read a list of commands via stdin or a file if you want. A script will fail when any command fails. / Truthfully, 'script' mode isn't fully fleshed out and may fall below your expectations. … Scripts are processed for parameter and environment variable expansion and then run as if you had invoked xdotool with the entire script on one line (using COMMAND CHAINING)."; `:993-995`: "=item * Read commands from stdin: / xdotool -"
- **Coverage.** T7: covers synthetic keyboard input into an X display (XTEST). The `--delay` of `type`/`key` is a single constant per invocation ("Each keystroke is separated by a delay given by the --delay option"); the man page gives no per-key delay list. Per-key intervals recorded from a human can be replayed only by chaining `key … sleep <fraction> key …` in a script (sleep accepts fractions of seconds; script mode is documented as "not fully fleshed out"). T1–T6: does not cover.
- **Observation?** No.

### S4-06 — ydotool(1), ydotoold(8), ydotool README

- **Citation.** ReimuNotMoe, ydotool, `manpage/ydotool.1.scd`, `manpage/ydotoold.8.scd`, `README.md`.
- **Copy read.** `https://raw.githubusercontent.com/ReimuNotMoe/ydotool/master/{manpage/ydotool.1.scd,manpage/ydotoold.8.scd,README.md}`, `master` HEAD `708e96ff27e381a8c549418a9d34cdde12305317`; accessed 2026-09-13; local `sources/S4-ydotool/`; SHA-256 `10d349af986eb2274c89dacaa3f1cc1f6947fed63d892e582398f8577e3fb608`, `af31607e18d6367493d21bbce1740d1da3c5f88204fcc64553ad73caf0f13dba`, `74f69347721dc159430e8ba3b0379b59cb29a580fd1dc8a5281e08d2e17791c3`.
- **Passages.**
  - `ydotool.1.scd:4`: "ydotool - command-line _/dev/uinput_ automation tool"; `:14-15`: "*ydotool* lets you programmatically (or manually) simulate keyboard input and mouse activity, etc. / The *ydotoold*(8) daemon must be running."
  - `ydotool.1.scd:32-34` (key): "*key* [*-d*,*--key-delay* _<ms>_] [_<KEYCODE:PRESSED>_ ...] / Type a given keycode."; `:41`: "Non-interpretable values, such as 0, aaa, l0l, will only cause a delay."; `:48-49`: "*-d*,*--key-delay* _<ms>_ / Delay time between keystrokes. Default 12ms."
  - `ydotool.1.scd:51-61` (type): "*type* [*-D*,*--next-delay* _<ms>_] [*-d*,*--key-delay* _<ms>_] [*-f*,*--file* _<filepath>_] "_text_" / Types text as if you had typed it on the keyboard. … *-d*,*--key-delay* _<ms>_ / Delay time between key events (up/down each). Default 12ms. / *-D*,*--next-delay* _<ms>_ / Delay between strings. Default 0ms."
  - `ydotoold.8.scd:12`: "*ydotoold* holds a persistent virtual device, and accepts input from *ydotool*(1)."
  - `README.md:77`: "`ydotoold` (daemon) program requires access to `/dev/uinput`. **This usually requires root permissions.**"; `:83`: "ydotool works differently from xdotool. xdotool sends X events directly to X server, while ydotool uses the uinput framework of Linux kernel to emulate an input device."; `:85-87`: "When ydotool runs and creates a virtual input device, it will take some time for your graphical environment (X11/Wayland) to recognize and enable the virtual input device. (Usually done by udev) / So, if the delay was too short, the virtual input device may not get recognized & enabled by your graphical environment in time."
- **Coverage.** T7: covers kernel-level synthetic input via `/dev/uinput` (root, available on a runner through passwordless sudo — S4-02 — provided the kernel offers uinput, which no document read establishes; see Not found). Delays are constant per invocation (`--key-delay`, `--next-delay`); no per-key list. Note that ydotool injects into the kernel input layer, so under Xvfb (which has "no physical input devices", S4-03) the X server would need an input driver reading evdev — no document read establishes that Xvfb does. T1–T6: does not cover.
- **Observation?** No.

### S4-07 — evemu: evemu-device(1)/evemu-play, evemu-describe(1)/evemu-record, `src/evemu.c`

- **Citation.** freedesktop.org libevdev/evemu, `tools/evemu-device.txt`, `tools/evemu-describe.txt` (asciidoc man sources), `src/evemu.c`.
- **Copy read.** `https://gitlab.freedesktop.org/libevdev/evemu/-/raw/master/{tools/evemu-device.txt,tools/evemu-describe.txt,src/evemu.c}`, `master` HEAD `ac0531bbf81c4a58918c7b7837ba87c76edef639`; accessed 2026-09-13; local `sources/S4-evemu/`; SHA-256 `c9a819af2fa9a73d301900aecfe255f4b469d91aae1ab0b99493f849798dcc59`, `ead72c1511b9c3580f14ead719fc15b08645eaa7f37e5b694eeaceb051902701`, `c7159fef84f43ebd5d75d4c65496bc700c42d9e26dee74571a149aeeab053311`.
- **Passages.**
  - `evemu-describe.txt:22-24`: "evemu-record captures events from the input device and prints them to stdout. The events can be parsed by evemu-play(1) to let a virtual input device created with evemu-device(1) emit the exact same event sequence."; `:26-27`: "evemu-describe and evemu-record need to be able to read from the device; in most cases this means they must be run as root."
  - `evemu-device.txt:21-25`: "evemu-device creates a virtual input device based on the description-file. This description is usually created by evemu-describe(1). evemu-device then creates a new input device with uinput"; `:27-30`: "evemu-play replays the event sequence given on stdin through the input device. The event sequence must be in the form created by evemu-record(1). If the argument is a file containing a recording, evemu-play creates the device and prompts the user for an interactive replay of the events."; `:37-39`: "evemu-device must be able to write to the uinput device node, and evemu-play must be able to write to the device node specified; in most cases this means it must be run as root."
  - `README.md` (same folder, SHA-256 `ffea37a5b0fd8927319ab36f66e625d6150335e27e497bc2be67fd6f28128aa6`), "Event Data Format": "E: <sec>.<usec> <evtype (hex)> <evcode (hex)> <ev value>"
  - `evemu.c:882-908` (`evemu_read_event_realtime`): "const unsigned long ERROR_MARGIN = 150; /* µs */" … "usec = time_to_long(&tv) - time_to_long(evtime); / if (usec > ERROR_MARGIN * 2) { / if (usec > s2us(10)) / error(INFO, "Sleeping for %lds.\n", us2s(usec)); / usleep(usec - ERROR_MARGIN); / *evtime = tv; }"; `evemu.c:938-960` (`evemu_play`): "while (evemu_read_event_realtime(fp, &ev, &evtime) > 0) { … SYSCALL(ret = write(fd, &ev, sizeof(ev))); }"
- **Coverage.** T7: covers replay of a recorded input stream at its recorded per-event timestamps (microsecond field; the replay sleeps the recorded delta minus a 150 µs margin before each event) through a uinput virtual device — the only tool read whose documentation and source establish per-key interval fidelity. Requires root and uinput (same caveat as S4-06). T1: does not cover (records format only, no data). T2–T6: does not cover.
- **Observation?** No.

### S4-08 — Playwright docs: Keyboard, Electron, CI

- **Citation.** Microsoft Playwright documentation sources `docs/src/api/class-keyboard.md`, `docs/src/electron-api/class-electron.md`, `docs/src/ci.md`.
- **Copy read.** Sparse clone of `https://github.com/microsoft/playwright` at commit `d1ead3ecca23182f2d06d761c28e3d4edafb6595` (identical bytes to the raw `main` fetch); accessed 2026-09-13; local `sources/S4-playwright/clone/docs/src/…`; SHA-256 keyboard `ea47d9b0db59479d41efd29aa4245b540fc698d444376db8b8743a5a3595d95a`, electron `37892992a5aa123d84d9febb71092a37928c7e001ef626ee7b1f908310975e87`, ci `10840b0eb1f075f32b38cf8848a33aec0b84c9400d7784518e8f1dc2f4d22253`.
- **Passages.**
  - `class-keyboard.md:296-300`: "### option: Keyboard.press.delay … Time to wait between `keydown` and `keyup` in milliseconds. Defaults to 0."
  - `class-keyboard.md:302-309`: "## async method: Keyboard.type … Sends a `keydown`, `keypress`/`input`, and `keyup` event for each character in the text."; `:316-317`: "await page.keyboard.type('Hello'); // Types instantly / await page.keyboard.type('World', { delay: 100 }); // Types slower, like a user"; `:356-360`: "### option: Keyboard.type.delay … Time to wait between key presses in milliseconds. Defaults to 0."
  - `class-electron.md:1-5`: "# class: Electron / * since: v1.9 / * langs: js / Playwright has **experimental** support for Electron automation."; `:82`: "## async method: Electron.launch"
  - `ci.md:1033-1035`: "By default, Playwright launches browsers in headless mode. … On Linux agents, headed execution requires [Xvfb](https://en.wikipedia.org/wiki/Xvfb) to be installed. Our [Docker image](./docker.md) and GitHub Action have Xvfb pre-installed. To run browsers in headed mode with Xvfb, add `xvfb-run` before the actual command."
- **Coverage.** T7: covers driving a browser (headless or headed under Xvfb) and, experimentally, an Electron app (a code editor such as VS Code) with synthetic keyboard events; `type` takes one constant `delay`, but `press` can be called per key from a script with arbitrary waits, so recorded intervals can be replayed at script granularity (the document does not state timing precision). T1–T6: does not cover.
- **Observation?** No.

### S4-09 — VS Code's own CI: Electron tests under Xvfb on `ubuntu-24.04`

- **Citation.** microsoft/vscode, `.github/workflows/pr-linux-test.yml`, `build/azure-pipelines/linux/xvfb.init`, `test/automation/src/playwrightElectron.ts`, `test/automation/src/playwrightDriver.ts`.
- **Copy read.** Sparse clone of `https://github.com/microsoft/vscode` at commit `3e8601c5f63f5b2358e0fbbfb825fbbfd72cbe2b`; accessed 2026-09-13; local `sources/S4-vscode-ci/clone/…`; SHA-256 `9ff4402c19a234da5264a41ecfebf45379ec04684fa51c8aff8a3f01a7dea5a0` (pr-linux-test.yml), `722e3b83fe84f597af3d2a8411b99631e9268d60ad450dcf7c82212c7241d124` (xvfb.init), `0107da3d695d26aafb977833f6c23d22f046310755414afe5c60289c36bb049f` (playwrightElectron.ts), `d653f963204ae6383e7ec5879d32d0ac29160318884ddd671ea17f0836333ecc` (playwrightDriver.ts).
- **Passages.**
  - `pr-linux-test.yml:29`: "    runs-on: ubuntu-24.04"
  - `pr-linux-test.yml:55-73` (step "Setup system services"): "# Allow unprivileged user namespaces for Chromium's namespace sandbox / # Ubuntu 24.04 restricts this by default via AppArmor / sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0 / # Start X server / … sudo apt-get install -y pkg-config \ / xvfb \ / libgtk-3-0 \ / libxkbfile-dev \ / libkrb5-dev \ / libgbm1 \ / rpm \ / bubblewrap \ / socat / sudo cp build/azure-pipelines/linux/xvfb.init /etc/init.d/xvfb / sudo chmod +x /etc/init.d/xvfb / sudo update-rc.d xvfb defaults / sudo service xvfb start"
  - `pr-linux-test.yml:358-363`: "- name: 🧪 Run unit tests (Electron) / if: ${{ inputs.electron_tests && inputs.unit_tests }} / timeout-minutes: 15 / run: ./scripts/test.sh --tfs "Unit Tests" / env: / DISPLAY: ":10""; same `DISPLAY: ":10"` at `:406` (integration tests) and `:420`; `:467-468`: "- name: 🧪 Run smoke tests (Electron) / if: ${{ inputs.electron_tests && inputs.smoke_tests }}"
  - `xvfb.init:21-22`: "PROG="/usr/bin/Xvfb" / PROG_OPTIONS=":10 -ac -screen 0 1024x768x24""
  - `playwrightElectron.ts:49-58`: "electron = await measureAndLog(() => playwrightImpl._electron.launch({ / executablePath: configuration.electronPath, / args: configuration.args, / recordVideo: … / env: configuration.env as { [key: string]: string }, / timeout: LAUNCH_TIMEOUT / }), 'playwright-electron#launch', logger);"
  - `playwrightDriver.ts:339-345`: "async typeText(selector: string, text: string, slowly: boolean = false): Promise<void> { / if (slowly) { / await this.page.type(selector, text, { delay: 50 }); / } else { / await this.page.fill(selector, text); / } }"; `:409`: "await this.page.keyboard.press(key);"
- **Coverage.** T7: covers, as a working primary example, that a GitHub-hosted `ubuntu-24.04` runner runs VS Code (Electron) unit, integration and smoke tests under Xvfb (`Xvfb :10 -ac -screen 0 1024x768x24`) with Playwright's `_electron.launch` and types with a constant 50 ms delay. Also documents a runner-specific prerequisite (AppArmor user-namespace sysctl for Chromium's sandbox). T1–T6: does not cover.
- **Observation?** No (CI configuration and driver code, no measurement).

### S4-10 — LibreOffice: `--headless` help text and the Python UI-test framework

- **Citation.** LibreOffice core, `desktop/source/app/cmdlinehelp.cxx`; `uitest/README.md`; `uitest/uitest/uihelper/common.py`; `uitest/uitest/uihelper/keyboard.py`; `uitest/libreoffice/connection.py`; `solenv/gbuild/UITest.mk`; `sw/qa/uitest/writer_tests/tdf78068.py`.
- **Copy read.** Sparse clone of `https://github.com/LibreOffice/core` (mirror of git.libreoffice.org) at commit `2410e6d5e8f08f537a76027be263849a52181b2c`; accessed 2026-09-13; local `sources/S4-libreoffice-uitest/clone/…` (cmdlinehelp also raw at `sources/S4-libreoffice-cmdline/`); SHA-256 cmdlinehelp `775e11920c10003c2ad32bc492a1377660c8bcf5aca2e75ca7a879dc30381e7a`, README `2c57a88927514078750dc81f1e083bab6799cdbbcb4070cf6e3e4445365f8447`, common.py `b5119a74e55cde6821f9d9f7332fbeaba791a3956db68854a45d9aba10cc1ad2`, keyboard.py `474f339e6fe48c0a1b8a183e6a229b14359e6b003c23840f9f51fe82975d56b6`, connection.py `4cd071aa8302695998ffbde1bdd2071dc87cb320228c051db66e60c81afd9104`, UITest.mk `5672f65744fcfc3fedfd262f0cf9c875e7c1de2c5b2988abe23bb3caa34ee49a`, tdf78068.py `6b98fbb03b2aecd99ed909a14ef32b0be611a90437c52e5b8a76330fc51a216a`.
- **Passages.**
  - `cmdlinehelp.cxx:92-95`: `"   --headless          Starts in \"headless mode\" which allows using the      \n" "                       application without GUI. This special mode can be used  \n" "                       when the application is controlled by external clients  \n" "                       via the API.                                            \n"`; `:85-88`: `"   --invisible         Starts in invisible mode. Neither the start-up logo nor \n" "                       the initial program window will be visible. Application \n" "                       can be controlled, and documents and dialogs can be     \n" "                       controlled and opened via the API. …"`
  - `uitest/README.md:1-6`: "# UI Testing Framework / The code for the UI testing framework and the UI tests. / The UI tests run on a dedicated desktop on Windows, to not interfere with the interactive session. To make them run on the current (active) desktop, define the following environment variable: LIBO_TEST_DEFAULT_DESKTOP"
  - `common.py:16-17`: "def type_text(ui_object, text): / ui_object.executeAction("TYPE", mkPropertyValues({"TEXT": text}))"
  - `keyboard.py:10-11`: "def select_all(ui_object): / ui_object.executeAction("TYPE", mkPropertyValues({"KEYCODE":"CTRL+A"}))"
  - `connection.py:81-84` (`bootstrap`): "argv = [soffice, "--accept=" + socket + ";urp", / "-env:UserInstallation=" + userdir, / "--quickstart=no", "--nofirststartwizard", / "--norestore", "--nologo"]"
  - `UITest.mk:37`: "gb_UITest_SOFFICEARG:=path:$(INSTROOT)/$(LIBO_BIN_FOLDER)/soffice"; `:40`: "gb_UITest_COMMAND = $(ICECREAM_RUN) $(gb_CppunitTest_coredumpctl_run) $(gb_CppunitTest_RR) $(gb_UITest_EXECUTABLE) $(SRCDIR)/uitest/test_main.py"
  - `tdf78068.py:19-22`: "xWriterDoc = self.xUITest.getTopFocusWindow() / xWriterEdit = xWriterDoc.getChild("writer_edit") / #- add some text / type_text(xWriterEdit, "Test")"
  - Absence: `grep -rn -i 'xvfb|SAL_USE_VCLPLUGIN|headless' uitest solenv/gbuild` finds no Xvfb reference; the UI-test launcher does not pass `--headless` (argv above), i.e. the UI tests need a display (the README speaks of a desktop; the repository holds no CI configuration).
- **Coverage.** T7: covers two ways to drive Writer on a runner: `--headless` (no GUI, API-controlled — no input path is exercised) and the UI-test framework, which launches a normal `soffice` with a UNO `--accept` socket and injects text through the UI-object `TYPE` action (a whole string per call; no per-key timing parameter) — so under Xvfb it exercises the GUI edit path but not X input events or recorded inter-key intervals. T1–T6: does not cover.
- **Observation?** No.

### S4-11 — GIMP `.gitlab-ci.yml`

- **Citation.** GNOME/gimp, `.gitlab-ci.yml`.
- **Copy read.** `https://gitlab.gnome.org/GNOME/gimp/-/raw/master/.gitlab-ci.yml`, `master` HEAD `d586c1c51cc7b3d3ba2758d9e23eb54c74ce0827`; accessed 2026-09-13; local `sources/S4-gimp/gitlab-ci.yml`; SHA-256 `cb5f7634bbfc37426ce26210ebc5d1fc72e92d9b2f06804c818fc363b300ea49`.
- **Passages.**
  - `gitlab-ci.yml:825`: "- export GIMP_TESTS_CONFIG_FILE="${PLUG_IN_DIR}test-file-plug-ins/tests/batch-config.ini""; `:830`: "- cat "${PLUG_IN_DIR}test-file-plug-ins/batch-import-tests.py" | gimp-console-${APP_VER} -id --batch-interpreter python-fu-eval -b - --quit"
  - Absence: the file contains no occurrence of `xvfb`, `Xvfb` or `DISPLAY` (my grep, case-insensitive).
- **Coverage.** T7: covers that GIMP's own CI exercises the application only in console batch mode (`gimp-console … -i -d --batch-interpreter python-fu-eval -b -`), not the GUI under Xvfb; batch mode is not interactive input. T1–T6: does not cover.
- **Observation?** No.

### S4-12 — Kdenlive `.kde-ci.yml`, KDE ci-utilities `TestHandler.py`, selenium-webdriver-at-spi README

- **Citation.** KDE Invent: multimedia/kdenlive `.kde-ci.yml`; sysadmin/ci-utilities `components/TestHandler.py`; sdk/selenium-webdriver-at-spi `README.md`.
- **Copy read.** `https://invent.kde.org/multimedia/kdenlive/-/raw/master/.kde-ci.yml` (HEAD `e5ec4f78ded01db92d43f557e8eab5940c965bb3`); `https://invent.kde.org/sysadmin/ci-utilities/-/raw/master/components/TestHandler.py` (HEAD `9441adc110876c180b9f9d00253b450134a617e4`); `https://invent.kde.org/sdk/selenium-webdriver-at-spi/-/raw/master/README.md` (HEAD `d45a21e8f1b3591dc921f0be85f1ecd834cbe413`); accessed 2026-09-13; local `sources/S4-kdenlive/`, `sources/S4-kde-ci/`, `sources/S4-kde-selenium/`; SHA-256 `dad914f2c1d4623e53e30df91da766a65b1fb534c65272b18fb4e16b64e2e857`, `40be3724b0d9b56a6ee93bc23a99c71627e873007f070aa0110f154c60a3945c`, `ea20f483069bc500718b092fa8e42709df4dd81965c85fd06100c861c90bff09`.
- **Passages.**
  - `kde-ci.yml:35-38`: "RuntimeDependencies: / - 'on': ['Linux'] / 'require': / 'sdk/selenium-webdriver-at-spi': '@latest-kf6'"; `:41`: "require-passing-tests-on: [ 'Linux/Qt6', 'FreeBSD/Qt6', 'Windows/Qt6' ]"
  - `TestHandler.py:73-76`: "# Setup Xvfb / buildEnvironment['DISPLAY'] = ':90' / commandToRun = "Xvfb :90 -ac -screen 0 1600x1200x24+32" / xvfbProcess = subprocess.Popen( commandToRun, stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT, shell=True, env=buildEnvironment )"; `:170`: "commandToRun = "ctest -T Test --output-junit {junitFilename} --output-on-failure --no-compress-output --test-output-size-passed 1048576 --test-output-size-failed 1048576 -j {cpuCount} --timeout {timeLimit} {additionalCTestArguments}""
  - `selenium README.md:7-10`: "selenium-webdriver-at-spi is a [WebDriver](https://www.w3.org/TR/webdriver/) for [Appium](https://appium.io) (based on [Selenium](https://www.selenium.dev/)) using the Linux accessibility API [AT-SPI2](https://www.freedesktop.org/wiki/Accessibility/AT-SPI2/). / It effectively enables us to write selenium-style UI tests that behind the scenes manipulate the UI through the accessibility API."
- **Coverage.** T7: covers that KDE's CI runs project tests (ctest) under an Xvfb display (`Xvfb :90 -ac -screen 0 1600x1200x24+32`), and that Kdenlive declares the AT-SPI WebDriver as a Linux runtime dependency for its tests — a Qt GUI driven through the accessibility API rather than through X input events. No KDE document read states per-key timing control. T1–T6: does not cover.
- **Observation?** No.

### S4-13 — mpv manual: `--ao=null`, `--vo=null`, `--vo=x11`, `--untimed`

- **Citation.** mpv, `DOCS/man/ao.rst`, `DOCS/man/vo.rst`, `DOCS/man/options.rst`.
- **Copy read.** `https://raw.githubusercontent.com/mpv-player/mpv/master/DOCS/man/{ao.rst,vo.rst,options.rst}`, `master` HEAD `13a4bfbc1a184c0576ca69c2de486a972aeb2407`; accessed 2026-09-13; local `sources/S4-mpv/`; SHA-256 `c3416e6d5e12f592762810ee802269ea9af784618c9f8a171a0c5e41ea67318f`, `58eb17fd3f8d77257d77a197b37012aa78b734a9adea084dd18053663914709b`, `e78aabb4a03f4cc3dfcf3221cd499a792a5914fedc3f272b088d1023418084fd`.
- **Passages.**
  - `ao.rst:245-257`: "``null`` / Produces no audio output but maintains video playback speed. You can use ``--ao=null --ao-null-untimed`` for benchmarking. … ``--ao-null-untimed`` / Do not simulate timing of a perfect audio device. This means audio decoding will go as fast as possible, instead of timing it to the system clock. / ``--ao-null-buffer`` / Simulated buffer length in seconds."
  - `ao.rst:180-181`: "``pulse`` / PulseAudio audio output driver"; `:207-208`: "``pipewire`` / PipeWire audio output driver"
  - `vo.rst:340-343`: "``null`` / Produces no video output. Useful for benchmarking. / Usually, it's better to disable video with ``--video=no`` instead."; `vo.rst:117-123`: "``x11`` (X11 only) / Shared memory video output driver without hardware acceleration that works whenever X11 is present. / You may need to use ``--profile=sw-fast`` to get decent performance. / .. note:: This is a fallback only, and should not be normally used."
  - `options.rst:1244-1246`: "``--untimed`` / Do not sleep when outputting video frames. Useful for benchmarks when used with ``--audio=no``."
- **Coverage.** T7: covers running mpv on a runner without audio hardware: `--ao=null` "simulate[s] timing of a perfect audio device" against the system clock (so a null-AO wake cadence is a simulated, not a device, timing); `--vo=x11` renders in software to an X display (usable under Xvfb); `--vo=null`/`--untimed` remove display pacing entirely. T4, T5: does not cover (no values or observations). T1–T3, T6: does not cover.
- **Observation?** No.

### S4-14 — Chromium `headless/README.md`

- **Citation.** Chromium, `headless/README.md`, "Headless Chromium".
- **Copy read.** `https://chromium.googlesource.com/chromium/src/+/main/headless/README.md?format=TEXT` (gitiles base64), decoded to `sources/S4-chromium-headless/README.decoded.md`; accessed 2026-09-13; SHA-256 base64 file `1b48200f154c1c603eb5b2d7d558875f1a690dc37a40cdd86c378e328ce50f71`, decoded `0c3e8a314f5c51e0127cf749cc16956891365b5befb13865b94babc691c8e0ed`. (Gitiles exposes no commit id for `main` in this form; not recorded.)
- **Passages.**
  - `README.decoded.md:1-6`: "# Headless Chromium / Headless Chromium allows running Chromium in a headless/server environment. Expected use cases include loading web pages, extracting metadata (e.g., the DOM) and generating bitmaps from page contents -- using all the modern web platform features provided by Chromium and Blink."
  - `:12-16`: "As of M132, headless shell functionality is no longer part of the Chrome binary, so --headless=old has no effect. If you are using old Headless functionality you should now migrate to `chrome-headless-shell`."
  - `:21-25`: "1. Start Chrome in headless mode using the `--headless` command line flag: … $ chrome --headless --remote-debugging-port=9222 https://chromium.org/"
- **Coverage.** T7: covers that a browser needs no X display at all on a runner (`--headless`); together with S4-08 it distinguishes headless from headed-under-Xvfb. T1–T6: does not cover.
- **Observation?** No.

### S4-15 — Linux man-pages: proc_pid_stat(5), proc_pid_status(5), proc_pid_task(5)

- **Citation.** Linux man-pages project (unreleased tree), `man/man5/proc_pid_stat.5`, `proc_pid_status.5`, `proc_pid_task.5`.
- **Copy read.** `https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/{proc_pid_stat.5,proc_pid_status.5,proc_pid_task.5}`, HEAD `59ba1c34fb6538206e96597739f053183d1e6428`; accessed 2026-09-13; local `sources/S4-man-pages-proc/`; SHA-256 `cba82e47c8c7917ec4f7c24d9c8779c53ecf478fdefe5c7835690989bb060bcd`, `b34589df733a25eab62388e39764477a0a525a0932fe70df3c94bb1e7e2c9f1a`, `c2db3e8d2d9e56e466d9144d946c22406947fd7390001ccf16167c7c4b278aeb`.
- **Passages.**
  - `proc_pid_stat.5:146-149`: ".RI (14)\~ utime \~%lu / Amount of time that this process has been scheduled in user mode, measured in clock ticks (divide by / .IR sysconf(_SC_CLK_TCK) )."; `:156-159`: ".RI (15)\~ stime \~%lu / Amount of time that this process has been scheduled in kernel mode, measured in clock ticks (divide by / .IR sysconf(_SC_CLK_TCK) )."; `:215-216`: ".RI (20)\~ num_threads \~%ld / Number of threads in this process (since Linux 2.6)."
  - `proc_pid_status.5:391-394`: ".I voluntary_ctxt_switches / .TQ / .I nonvoluntary_ctxt_switches / Number of voluntary and involuntary context switches (since Linux 2.6.23)."
  - `proc_pid_task.5:12-19` (a troff comment line 13 omitted): ".IR /proc/ pid /task/ " (since Linux 2.6.0)" / This is a directory that contains one subdirectory for each thread in the process. The name of each subdirectory is the numerical thread ID"; `:38-44`: "For attributes that are distinct for each thread, the corresponding files under / .IR task/ tid / may have different values (e.g., various fields in each of the / .IR task/ tid /status / files may be different for each thread),"
- **Coverage.** T7: covers what a `/proc` sidecar can read per thread: cumulative user/kernel CPU time in clock ticks (`stat` fields 14–15), thread count (`stat` field 20 / `task/` directory), and cumulative voluntary/involuntary switch counts (`status`). All are counters; the documents define no per-wake duration, so a poller obtains only differences between samples (CPU consumed and number of switches per polling interval), not the CPU cost of an individual wake. T1–T6: does not cover.
- **Observation?** No.

### S4-16 — Kernel `Documentation/scheduler/sched-stats.rst`, `/proc/<pid>/schedstat`

- **Citation.** Linux kernel documentation, "Scheduler Statistics", section "/proc/<pid>/schedstat".
- **Copy read.** `https://raw.githubusercontent.com/torvalds/linux/master/Documentation/scheduler/sched-stats.rst`, `master` HEAD `22098763a10d9c1340827fcf6edab66f153b27f0`; accessed 2026-09-13; local `sources/S4-kernel-sched-stats/sched-stats.rst`; SHA-256 `6c80bd9a62d50aa37161d6d909dfeff8c460c3b949454bf4c093c211f6252335`.
- **Passages.**
  - `sched-stats.rst:190-198`: "/proc/<pid>/schedstat / --------------------- / schedstats also adds a new /proc/<pid>/schedstat file to include some of the same information on a per-process level.  There are three fields in this file correlating for that process to: / 1) time spent on the cpu (in nanoseconds) / 2) time spent waiting on a runqueue (in nanoseconds) / 3) # of timeslices run on this cpu"
  - `sched-stats.rst:46-48`: "These fields are counters, and only increment.  Programs which make use of these will need to start with a baseline observation and then calculate the change in the counters at each subsequent observation."
- **Coverage.** T7: covers the highest-resolution `/proc` counters a sidecar can poll per thread (`task/<tid>/schedstat`, per S4-15's rule that thread-distinct files live under `task/`): nanosecond on-CPU time, nanosecond runqueue wait, and a count of timeslices — cumulative only; the average CPU per timeslice between two samples is derivable, a per-wake distribution is not. T1–T6: does not cover.
- **Observation?** No.

### S4-17 — perf-sched(1)

- **Citation.** Linux perf, `tools/perf/Documentation/perf-sched.txt`, "perf-sched - Tool to trace/measure scheduler properties (latencies)".
- **Copy read.** `https://raw.githubusercontent.com/torvalds/linux/master/tools/perf/Documentation/perf-sched.txt`, HEAD `22098763a10d9c1340827fcf6edab66f153b27f0`; accessed 2026-09-13; local `sources/S4-perf-sched/perf-sched.txt`; SHA-256 `19f10af4a255882c0159317165fe87de78b2b6a97c6649434d2764a5936139be`.
- **Passages.**
  - `perf-sched.txt:11`: "'perf sched' {record|latency|map|replay|script|timehist|stats}"; `:17-18`: "'perf sched record <command>' to record the scheduling events of an arbitrary workload."
  - `perf-sched.txt:65-87`: "'perf sched timehist' provides an analysis of scheduling events. … By default it shows the individual schedule events, including the wait time (time between sched-out and next sched-in events for the task), the task scheduling delay (time between runnable and actually running) and run time for the task: / time    cpu  task name             wait time  sch delay   run time / [tid/pid]                (msec)     (msec)     (msec) … Times are in msec.usec."
  - `perf-sched.txt:428-434` (timehist options): "-p=:: / --pid=:: / Only show events for given process ID (comma separated list). / -t=:: / --tid=:: / Only show events for given thread ID (comma separated list)."; `:436-439`: "-s:: / --summary:: / Show only a summary of scheduling by thread with min, max, and average run times (in sec) and relative stddev."; `:457-459`: "-w:: / --wakeups:: / Show wakeup events."
- **Coverage.** T7: covers exactly the per-schedule quantities the topic asks about — per event, per thread: run time (CPU per schedule), wait time (gap between sched-out and next sched-in, i.e. the wake gap) and scheduling delay, in microsecond resolution, plus per-thread summaries and wakeup events. Whether `perf sched record` works on a hosted runner is governed by perf access rules (S4-18) and tool availability (S4-25); no document read states the runner's `perf_event_paranoid` value. T3: does not cover (method only, no application trace). T1–T2, T4–T6: does not cover.
- **Observation?** No.

### S4-18 — Kernel `Documentation/admin-guide/perf-security.rst`

- **Citation.** Linux kernel documentation, "Perf events and tool security", section on `perf_event_paranoid`.
- **Copy read.** `https://raw.githubusercontent.com/torvalds/linux/master/Documentation/admin-guide/perf-security.rst`, HEAD `22098763a10d9c1340827fcf6edab66f153b27f0`; accessed 2026-09-13; local `sources/S4-kernel-perf-security/perf-security.rst`; SHA-256 `080dc302bb2ed254192522e1b78d65d71a965d4d893634b052e595d65c6c9383`.
- **Passages.**
  - `perf-security.rst:226-227`: "perf_events *scope* and *access* control for unprivileged processes is governed by perf_event_paranoid [2]_ setting:"; `:237-244`: ">=0: / *scope* includes per-process and system wide performance monitoring but excludes raw tracepoints and ftrace function tracepoints monitoring."; `:246-248`: ">=1: / *scope* includes per-process performance monitoring only and excludes system wide performance monitoring."; `:254-256`: ">=2: / *scope* includes per-process performance monitoring only. CPU and system events happened when executing in user space only can be monitored"
- **Coverage.** T7: covers the rule that the `sched_*` tracepoints `perf sched` needs are excluded for unprivileged users at any paranoid level >= 0 — hence on a runner `perf sched record` must run as root (available via passwordless sudo, S4-02). T1–T6: does not cover.
- **Observation?** No.

### S4-19 — ftrace.rst and trace-cmd-record(1)

- **Citation.** Linux kernel `Documentation/trace/ftrace.rst` ("The File System"); trace-cmd `Documentation/trace-cmd/trace-cmd-record.1.txt`.
- **Copy read.** `https://raw.githubusercontent.com/torvalds/linux/master/Documentation/trace/ftrace.rst` (HEAD `22098763a10d9c1340827fcf6edab66f153b27f0`), `https://raw.githubusercontent.com/rostedt/trace-cmd/master/Documentation/trace-cmd/trace-cmd-record.1.txt` (HEAD `f35c3b04f30c6368413ceede2a27a5dc90f3ea7c`); accessed 2026-09-13; local `sources/S4-kernel-ftrace/`, `sources/S4-trace-cmd/`; SHA-256 `17dc4ebc317ca03d261146421c6d9235b0e5d25d929706eecdf2f0bb18420cc8`, `89b0f3c9b0f07f6e17e2108c4f23d8f82d89e8e6e4ffdb3b9222b0ae397121c5`.
- **Passages.**
  - `ftrace.rst:49-60`: "Ftrace uses the tracefs file system to hold the control files as well as the files to display output. / When tracefs is configured into the kernel (which selecting any ftrace option will do) the directory /sys/kernel/tracing will be created. … Or you can mount it at run time with:: / mount -t tracefs nodev /sys/kernel/tracing"
  - `trace-cmd-record.1.txt:39-41`: "Using "-e sched_switch" will enable the "sched_switch" event where as, "-e sched" will enable all events under the "sched" subsystem."; `:364-365`: "any events (like sched_switch), unless they are specifically specified on the command line (i.e. -p function -e sched_switch -e sched_wakeup)"; `:469` (example output): "ls-13587 [002] 106467.860313: sched_switch: prev_comm=trace-cmd prev_pid=13587 prev_prio=120 prev_state=R ==> next_comm=trace-cmd next_pid=13583 next_prio=120"
- **Coverage.** T7: covers the ftrace path to the same `sched_switch`/`sched_wakeup` events (root; tracefs mount) as an alternative to `perf sched` for per-schedule runtime and wake gaps; whether tracefs is mounted on the azure kernel is not stated by any document read. T1–T6: does not cover.
- **Observation?** No.

### S4-20 — strace(1)

- **Citation.** strace, `doc/strace.1.in`.
- **Copy read.** `https://raw.githubusercontent.com/strace/strace/master/doc/strace.1.in`, HEAD `f3c8d2fe783f6fa00add08a84aa4225a296b9ddc`; accessed 2026-09-13; local `sources/S4-strace/strace.1.in`; SHA-256 `c16859e07dacc5cda882c7ab5f2e353803645a6ca449a0ac41eda1034e67ae9a`.
- **Passages.**
  - `strace.1.in:437-445`: ".B \-f / .TQ / .BR \-\-follow\-forks / Traces child processes as they are created by currently traced processes as a result of the / .BR fork (2), / .BR vfork (2) / and / .BR clone (2)"; `:449-454`: "is multi-threaded, using / .B \-f / .B \-p / .I PID / attaches to all of its threads, not just the one with / .IR thread_id " = " PID ."
  - `strace.1.in:1255-1259`: ".B \-ttt / .TQ / .BR \-\-absolute\-timestamps = format:unix , precision:us / Prints the wall clock time as seconds since the epoch, with microsecond precision."; `:1261-1266`: ".B \-T / .TQ / .BR \-\-syscall\-times [= \fIprecision\fR ] / Shows the time spent in system calls. This records the time difference between the beginning and the end of each system call."
- **Coverage.** T7: covers the unprivileged fallback: per-thread timestamps of blocking calls (`poll`/`epoll_wait`/`read` on the X socket) give wake gaps at microsecond resolution, but syscall duration is not CPU time and ptrace stops perturb the traced program (the man page does not quantify this). T1–T6: does not cover.
- **Observation?** No.

### S4-21 — BPF tools: bcc `offcputime`, bcc INSTALL, bpftrace `runqlat.bt`

- **Citation.** iovisor/bcc `tools/offcputime_example.txt`, `INSTALL.md`; bpftrace `tools/runqlat.bt`.
- **Copy read.** `https://raw.githubusercontent.com/iovisor/bcc/master/{tools/offcputime_example.txt,INSTALL.md}` (HEAD `8a46070fe08d646e2781fba69586d755da766aa2`); `https://raw.githubusercontent.com/bpftrace/bpftrace/master/tools/runqlat.bt` (HEAD `ecca8a082b91e05f99e0b71ee9beec47f2527096`); accessed 2026-09-13; local `sources/S4-bcc/`, `sources/S4-bpftrace/`; SHA-256 `a0c4f5df73a1ec8b608ce8e64d155c9ab5835fcae44a490f25f341ff4bda92d9`, `2780afb139b08850ef2ce4925bc6cf03e39c5c69858723a1ab0bd5094e1828f1`, `6a7f67e1a83ffe30c01145a0a33ea6d2f7fd35c02181c7eadcee90aa8b0bade1`.
- **Passages.**
  - `offcputime_example.txt:4-8`: "This program shows stack traces that were blocked, and the total duration they were blocked. It works by tracing when threads block and when they return to CPU, measuring both the time they were blocked (aka the "off-CPU time") and the blocked stack trace and the task name. This data is summarized in kernel by summing the blocked time by unique stack trace and task name."
  - `INSTALL.md:96`: "sudo apt-get install bpfcc-tools linux-headers-$(uname -r)"; `:49`: "# Need kernel headers through /sys/kernel/kheaders.tar.xz"
  - `runqlat.bt:2-3`: "// runqlat.bt	CPU scheduler run queue latency as a histogram. / // 		For Linux, uses bpftrace, eBPF."; `:8-9`: "// Attaching 5 probes... / // Tracing CPU scheduler... Hit Ctrl-C to end."
- **Coverage.** T7: covers in-kernel aggregation (off-CPU time, run-queue latency histograms) as a lower-overhead complement to `perf sched`; requires root and, for bcc, matching kernel headers (Ubuntu package `linux-headers-$(uname -r)`; for the azure flavour the header package's availability was not checked). T1–T6: does not cover.
- **Observation?** No (example outputs in these files are from the tool authors' machines, unnamed; not used as data).

### S4-22 — PipeWire: `spa/plugins/support/null-audio-sink.c`, `pipewire.conf.in`, `pulse-module-null-sink.c`

- **Citation.** PipeWire source: SPA null audio sink plugin; daemon default configuration; PulseAudio-compatibility `module-null-sink`.
- **Copy read.** `https://gitlab.freedesktop.org/pipewire/pipewire/-/raw/master/{spa/plugins/support/null-audio-sink.c,src/daemon/pipewire.conf.in,src/modules/module-protocol-pulse/modules/pulse-module-null-sink.c}`, HEAD `1cd56b0615bb8bd112d9a2865a41cfdf638692f6`; accessed 2026-09-13; local `sources/S4-pipewire/`; SHA-256 `2d73bb551317075fabf88e708a728806c4822d9783bfb057597fd165b644b77e`, `8bb0dda1eecefd05f7fb234811e560a5c0edd467db16c9cefdd780c63fab0369`, `b1950121f97d5d970ca197fa4837f611441be40965edc9c43960971217be724c`.
- **Passages.**
  - `null-audio-sink.c:37`: "#define DEFAULT_CLOCK_NAME	"clock.system.monotonic""; `:179-190` (`set_timeout`): "ts.it_value.tv_sec = next_time / SPA_NSEC_PER_SEC; … spa_system_timerfd_settime(this->data_system, this->timer_source.fd, SPA_FD_TIMER_ABSTIME, &ts, NULL);"; `:270-311` (`on_timeout`): "nsec = this->next_time; / if (SPA_LIKELY(this->position)) { / duration = this->position->clock.target_duration; / rate = this->position->clock.target_rate.denom; / } else { / duration = 1024; / rate = 48000; / } / this->next_time = nsec + duration * SPA_NSEC_PER_SEC / rate; / if (SPA_LIKELY(this->clock)) { / this->clock->nsec = nsec; … this->clock->delay = 0; / this->clock->rate_diff = 1.0; / this->clock->next_nsec = this->next_time; } / spa_node_call_ready(&this->callbacks, SPA_STATUS_NEED_DATA); / set_timeout(this, this->next_time);"
  - `pipewire.conf.in:293-297`: "# A default dummy driver. This handles nodes marked with the "node.always-process" / # property when no other driver is currently active. JACK clients need this. / { factory = spa-node-factory / args = { / factory.name    = support.node.driver"; `:320-326`: "# This creates a new Source node. It will have input ports / # that you can link, to provide audio for this source. / #{ factory = adapter / #    args = { / #        factory.name     = support.null-audio-sink"
  - `pulse-module-null-sink.c:7-11`: "/** \page page_pulse_module_null_sink Null Sink / * / * ## Module Name / * / * `module-null-sink`"; `:17-18`: "{ "sink_name", "name of sink", 0, MODULE_TYPE_STRING, "null-sink" },"
- **Coverage.** T7 and T4 (documentation, not observation): covers how a PipeWire null sink is clocked on a machine without an audio device — an absolute CLOCK_MONOTONIC timerfd re-armed each cycle by `duration/rate` (the graph quantum; 1024/48000 s if no position is set), reporting zero delay and rate_diff 1.0 — i.e. an idealised timer, not a device clock. This is what a runner's audio path would show. T1–T3, T5–T6: does not cover.
- **Observation?** No.

### S4-23 — PulseAudio `src/modules/module-null-sink.c`

- **Citation.** PulseAudio source, `module-null-sink.c`, "Clocked NULL sink".
- **Copy read.** `https://gitlab.freedesktop.org/pulseaudio/pulseaudio/-/raw/master/src/modules/module-null-sink.c`, HEAD `77d25a1e613095bdf87a1d13b65e7c330565077a`; accessed 2026-09-13; local `sources/S4-pulseaudio/module-null-sink.c`; SHA-256 `60f9acbd5926419b0237b4e274513c5312c8f34b3f3ba62bb32853501749d918`.
- **Passages.**
  - `module-null-sink.c:46`: "PA_MODULE_DESCRIPTION(_("Clocked NULL sink"));"; `:60-61`: "#define BLOCK_USEC (2 * PA_USEC_PER_SEC) / #define BLOCK_USEC_NOREWINDS (50 * PA_USEC_PER_MSEC)"
  - `:236-242` (`process_render`): "/* This is the configured latency. Sink inputs connected to us might not have a single frame more than the maxrequest value queued. Hence: at maximum read this many bytes from the sink inputs. */ / /* Fill the buffer up the latency size */ / while (u->timestamp < now + u->block_usec) {"
  - `:276-295` (`thread_func`): "u->timestamp = pa_rtclock_now(); / for (;;) { … /* Render some data and drop it immediately */ / if (PA_SINK_IS_OPENED(u->sink->thread_info.state)) { / if (u->timestamp <= now) / process_render(u, now); / pa_rtpoll_set_timer_absolute(u->rtpoll, u->timestamp); / } else / pa_rtpoll_set_timer_disabled(u->rtpoll);"
- **Coverage.** T7 and T4 (documentation): the PulseAudio null sink renders and discards audio on an rtclock timer, with a 2 s default block (50 ms with `norewinds`) — again a timer-driven idealisation with no device. T1–T3, T5–T6: does not cover.
- **Observation?** No.

### S4-24 — Mesa `docs/drivers/llvmpipe.rst`

- **Citation.** Mesa 3D documentation, "LLVMpipe".
- **Copy read.** `https://gitlab.freedesktop.org/mesa/mesa/-/raw/main/docs/drivers/llvmpipe.rst`, HEAD `f6f4f66c975c4ced2547e78e20c3b71850765ab5`; accessed 2026-09-13; local `sources/S4-mesa/llvmpipe.rst`; SHA-256 `f392a78a830963078a3c7e529205f12685212e0d219ddce78ebcc00d8941eed8`.
- **Passages.**
  - `llvmpipe.rst:7-12`: "The Gallium LLVMpipe driver is a software rasterizer that uses LLVM to do runtime code generation. Shaders, point/line/triangle rasterization and vertex processing are implemented with LLVM IR which is translated to x86, x86-64, or ppc64le machine code. Also, the driver is multithreaded to take advantage of multiple CPU cores (up to 32 at this time). It's the fastest software rasterizer for Mesa."
- **Coverage.** T7: covers what GPU-less rendering means for CPU accounting — llvmpipe rasterises on CPU threads (so an application's "GPU" work appears as CPU time in its own or Mesa's threads). No document read states that the hosted runner uses llvmpipe; S4-01 and S4-02 name no GPU. T1–T6: does not cover.
- **Observation?** No.

### S4-25 — packages.ubuntu.com: azure kernel module file lists; `linux-tools-azure`, `xdotool`, `ydotool`, `evemu-tools`

- **Citation.** Ubuntu package pages (noble / noble-updates): "File list of package linux-modules-6.17.0-1022-azure in noble-updates of architecture amd64"; "File list of package linux-modules-extra-6.17.0-1022-azure in noble-updates of architecture amd64"; "Package: linux-tools-azure (6.17.0-1022.22 and others) [security]"; "Package: xdotool (1:3.20160805.1-5build1) [universe]"; "Package: ydotool (0.1.8-3build1) [universe]"; "Package: evemu-tools (2.7.0-4build1) [universe]".
- **Copy read.** `https://packages.ubuntu.com/noble-updates/amd64/linux-modules-6.17.0-1022-azure/filelist`, `…/linux-modules-extra-6.17.0-1022-azure/filelist`, `https://packages.ubuntu.com/noble/linux-tools-azure`, `/noble/xdotool`, `/noble/ydotool`, `/noble/evemu-tools`; accessed 2026-09-13; local `sources/S4-ubuntu-packages/`; SHA-256 `552552df7e0f3ab6a85b1b3576f336cef8f722a970b289eff918b2179b751003`, `8aa82d30dd48ed182d4cf0cdd25e83dc003f8788d66431b00bcace8741ca5245`, `038aad1914eb4f193a986ca3a1c5b149f6406a00fb55cf061699c9ac64bc6acb`, `288540d6906d36247eac48469e7b2f17546e8024d89f212ac463655cf29c1512`, `a0bb83edaee711fff66c997fc7d228ddef588f087785efcf99c40bd9614ff6a1`, `4efcafc4b59161ee6c3c08b0b2f87bffd8c28544ff41368d06cb760a8fcfcc55`.
- **Passages.**
  - `linux-tools-azure.html` `<meta name="Description">`: "Linux kernel versioned tools for Azure systems."; page `<h1>`: "Package: linux-tools-azure (6.17.0-1022.22 and others)" — the same 6.17.0-1022 ABI as the runner kernel in S4-01.
  - `xdotool.html` meta description: "simulate (generate) X11 keyboard/mouse input events"; `ydotool.html`: "Command-line automation tool - cli"; `evemu-tools.html`: "Linux Input Event Device Emulation Library - test tools".
  - Module file lists (my count over every `/lib/modules/6.17.0-1022-azure/…/*.ko.zst` path in the two saved pages): `linux-modules` 848 modules, `linux-modules-extra` 2150 modules; paths containing `/kernel/sound/` or `/snd`: 0 in both; paths containing `uinput`: 0 in both; `evdev`: 0 in both; example paths present: `kernel/drivers/input/serio/hyperv-keyboard.ko.zst` (linux-modules), `kernel/drivers/input/misc/gpio-vibra.ko.zst` (linux-modules-extra).
- **Coverage.** T7: covers (a) that `perf` for the runner's kernel ABI is packaged (`linux-tools-azure` 6.17.0-1022) and that xdotool, ydotool and evemu-tools are apt-installable on noble; (b) that neither azure kernel module package ships any ALSA module — so `modprobe snd-dummy`/`snd-aloop` cannot succeed from these packages; a user-space null sink (S4-22/S4-23) is the only documented audio path. The lists cannot settle whether uinput or evdev are built in or absent (neither appears as a module; the kernel config fetch failed, search-log row 27). T1–T6: does not cover.
- **Observation?** No (package metadata; the module counts are my tallies over the saved pages, method stated above).

## 3. Not found

Topics T1–T6 are outside this class; no candidate is offered for them (every candidate above is marked "does not cover" for T1–T6, with S4-13, S4-22, S4-23 touching T4/T5 as documentation only).

Within T7, the following were sought and not established by any document read:

1. **Whether a hosted runner has, or lacks, an audio device.** No GitHub or Azure document read says so. Searches: rows 32, 34, 37, 38; the one primary lead (runner-images issue #1114 asking for `snd-aloop`/`soundcore`) could not be read verbatim (rows 29, 35, 36: HTTP 403, API access denied). The only evidence is indirect: the azure kernel module packages contain no sound modules (S4-25), and a null sink needs none (S4-22, S4-23).
2. **Whether `/dev/uinput` exists on the azure kernel** (needed by ydotool, S4-06, and evemu, S4-07). The kernel config (`CONFIG_INPUT_UINPUT`) was unreachable (row 27, HTTP 403); the module lists show no `uinput.ko` and no `evdev.ko`, which is consistent with built-in or with absent (S4-25).
3. **Whether Xvfb accepts kernel (evdev/uinput) input at all.** Xvfb(1) states the server runs with "no physical input devices" (S4-03) and documents no input driver; no document read says whether uinput-injected keys reach clients of an Xvfb display. xdotool's XTEST path (S4-05) is the only documented input route into Xvfb.
4. **The runner's `perf_event_paranoid` value and whether `perf sched record` works there.** Issues #11789, #11689, #4974 and community discussion #45004 are leads only (rows 29, 33, 35, 36 — not readable). The kernel rule (S4-18) plus passwordless sudo (S4-02) and the packaged `linux-tools-azure` (S4-25) are the documented basis; no runner document confirms it.
5. **Whether tracefs is mounted, or kernel headers for `-azure` are installable, on the runner** (S4-19, S4-21): not stated by any document read.
6. **A GUI-input tool documenting per-keystroke variable delays.** xdotool `type`/`key --delay` (S4-05), ydotool `--key-delay` (S4-06) and Playwright `type({delay})` (S4-08) each document one constant delay. Replay of recorded intervals is documented only via xdotool script `sleep` chaining (S4-05, "not fully fleshed out") or evemu-play (S4-07, uinput, root).
7. **LibreOffice's own CI running UI tests under Xvfb.** The core repository holds no CI configuration; its UI-test launcher passes no `--headless` and mentions no Xvfb (S4-10). WebSearch row 39 returned only tinderbox failure mails and generic pages.
8. **GIMP's GUI under Xvfb in its CI.** Not found: its CI uses `gimp-console` batch mode only (S4-11).
9. **Kdenlive typing through the AT-SPI WebDriver with timing control.** The KDE documents read (S4-12) establish Xvfb use and the AT-SPI driver dependency, not per-key timing.
10. **A statement that Xvfb has no refresh cadence, or that hosted runners render with llvmpipe.** Xvfb(1) documents no refresh at all (absence, S4-03); Mesa documents llvmpipe as a CPU rasteriser (S4-24) but no runner document names the GL stack.
11. **Playwright Electron under Xvfb as a documented configuration.** Playwright's Electron page (S4-08) does not mention Xvfb or Linux; the practice is established only by VS Code's own workflow (S4-09).
12. **GitHub-hosted runner hardware beyond CPU/RAM/disk** (GPU, sound, hypervisor generation): S4-02 gives 4 vCPU / 16 GB / 14 GB SSD / x64 and "hosted in Azure" only.
