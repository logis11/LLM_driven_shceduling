# S4 — own measurement on a CI runner (observability)

Reader: S4. Topic: T13, plus what a runner can contribute to T5, T6, T8, T10.
Date of all access: 2026-09-23. Source copies under `../sources/S4-NN/` (gitignored; every passage needed is quoted here).

No GitHub Actions workflow was created or triggered. Everything below is either (a) documentation / source code / public workflow files read at a named commit, or (b) a **local check in this container (not a runner)**.

## Environment of the local checks (local check in this container, not a runner)

```
$ uname -a
Linux vm 6.18.44-fc-v37 #1 SMP PREEMPT_DYNAMIC @0 x86_64 x86_64 x86_64 GNU/Linux
$ cat /etc/os-release   (excerpt)
PRETTY_NAME="Ubuntu 24.04.4 LTS"
VERSION_ID="24.04"
VERSION_CODENAME=noble
$ nproc
4
$ ps -p 1 -o comm=
process_api
$ grep -m1 'model name' /proc/cpuinfo
model name	: Intel(R) Xeon(R) Processor @ 2.80GHz
$ free -g   (Mem total) 15
```

PID 1 in this container is `process_api`, not systemd, so no unit can be *started* here; checks were limited to reading packages, resolving dependencies and compiling kernel modules against installed headers. The container's apt sources are Ubuntu noble / noble-updates / noble-backports (archive.ubuntu.com) plus third-party PPAs, which do not affect the packages used below.

---

## 1. Search log

| # | Date | Engine / venue | Exact query or request | Hits followed | Dead ends (HTTP status) |
|---|---|---|---|---|---|
| 1 | 2026-09-23 | git (github.com) | `git clone --depth 1 https://github.com/actions/runner-images.git` | `images/ubuntu/Ubuntu2404-Readme.md`, `scripts/build/configure-apt.sh`, `configure-environment.sh`, `post-build-validation.sh`, `toolsets/toolset-2404.json` → S4-01 | — |
| 2 | 2026-09-23 | grep over runner-images | `grep -rn -i -E 'systemctl\|timer\|disable\|mask'` and `'kvm\|linux-headers\|dkms\|headless\|xvfb\|gpu'` in `images/ubuntu/` | configure-apt.sh, configure-environment.sh, toolsets | no mention of kvm, dkms, linux-headers, headless, gpu in `images/ubuntu/scripts`/`toolsets`/`templates` |
| 3 | 2026-09-23 | GitHub REST API | `GET https://api.github.com/repos/github/docs/commits/main` | — | 403-equivalent from session proxy: "GitHub access to this repository is not enabled for this session" |
| 4 | 2026-09-23 | git (github.com) | `git clone --depth 1 --filter=blob:none --sparse https://github.com/github/docs.git`; sparse `content/actions data/reusables` | `data/reusables/actions/supported-github-runners.md`, `content/actions/concepts/runners/github-hosted-runners.md`, `content/actions/reference/runners/github-hosted-runners.md`, `content/actions/reference/runners/larger-runners.md` → S4-02 | — |
| 5 | 2026-09-23 | WebSearch | `GitHub changelog hardware accelerated Android virtualization Linux runners KVM` | github.blog changelog 2024-04-02 → S4-03 | community discussion #8305, runner-images discussion #7191 not followed (changelog is primary) |
| 6 | 2026-09-23 | WebSearch | `"gnome-shell --headless" github actions workflow CI` | happytomatoe/fedora-speech-to-text PR #157 → S4-04; schneegans.github.io GNOME Shell Extensions & CI Part III → S4-05 | GitHub web pages for PR #157 (`/pull/157`, `/pull/157.patch`): proxy refusal (403, "GitHub access to this repository is not enabled"); obtained via `git fetch origin pull/157/head` instead |
| 7 | 2026-09-23 | curl | schneegans.github.io Part I/II guessed URLs `/tutorials/2022/02/13/…-01`, `/2022/02/24/…-02` | Part III (200) | 404 on both guessed URLs (true URLs are 2022/02/28 and 2022/03/01; not needed) |
| 8 | 2026-09-23 | git (github.com) | `git clone --depth 1 https://github.com/Schneegans/gnome-shell-pod.git` | Dockerfile, systemd units, README → S4-05 | — |
| 9 | 2026-09-23 | gitlab.gnome.org API + raw | `GET /api/v4/projects/GNOME%2Fmutter/repository/commits/main`; raw `src/core/meta-context-main.c` at main and at tag 46.2 | → S4-06 | — |
| 10 | 2026-09-23 | invent.kde.org API + raw | `GET /api/v4/projects/plasma%2Fkwin/repository/commits/master`; raw `src/main_wayland.cpp` | → S4-07 | — |
| 11 | 2026-09-23 | apt / archive.ubuntu.com (local check) | `apt-get -s -o Dir::State::status=/dev/null install ubuntu-desktop ubuntu-minimal ubuntu-standard <73 Priority:required pkgs>`; `Contents-amd64.gz` for noble and noble-updates; `apt-get download` of 20 packages | → S4-08 | — |
| 12 | 2026-09-23 | src.fedoraproject.org API + raw | `GET /api/0/rpms/fedora-release/git/branches?with_commits=true`; `tree/rawhide`; raw `fedora-release.spec` and 6 preset files at f44 commit | → S4-09 | `rpms/systemd` f44 tree has no preset files (presets are in fedora-release) |
| 13 | 2026-09-23 | geo.mirror.pkgbuild.com (local check) | directory listings `core/os/x86_64/`, `extra/os/x86_64/`; packages systemd, man-db, shadow, util-linux, logrotate, pacman, plocate | → S4-10 | — |
| 14 | 2026-09-23 | developer.valvesoftware.com | `/wiki/SteamCMD`, `/w/index.php?title=SteamCMD&action=raw`, `/w/api.php?action=parse&page=SteamCMD…` | — | HTTP 200 but body is a bot-challenge page ("Making sure you're not a bot!"); WebFetch: HTTP 403 |
| 15 | 2026-09-23 | web.archive.org | CDX `url=developer.valvesoftware.com/wiki/SteamCMD&filter=statuscode:200&limit=-8`; `web/20260909202315id_/…` | → S4-11 | `web/2026id_/…` redirected to the bot-challenge URL (not usable) |
| 16 | 2026-09-23 | archive.ubuntu.com (local check) | `pool/multiverse/s/steamcmd/steamcmd_0~20180105-5build1_i386.deb` | man page and `steamcmdcommands.txt` read; no "anonymous" text in either | `apt-get download steamcmd:i386` → "Unable to locate package" (i386 not enabled) |
| 17 | 2026-09-23 | WebSearch | `firefox-source-docs talos ts_paint startup test Linux measures time` | firefox-source-docs talos.html → S4-12 | wiki.mozilla.org, searchfox not followed |
| 18 | 2026-09-23 | WebSearch | `github actions ubuntu runner "systemctl --user" "Failed to connect to bus" loginctl enable-linger runner` | none about hosted runners | generic Arch/Launchpad threads only — dead end for runner-specific documentation |
| 19 | 2026-09-23 | GitHub code search (MCP) | `"kwin_wayland" "--virtual" path:.github/workflows` | 5 hits; Tapuuk/Lumanin `de-smoke.yml` → S4-15 | sidorares/react-x11, spyoungtech/pyclip, biglinux/biglinux-webapps, marunine/marupop not opened |
| 20 | 2026-09-23 | GitHub code search (MCP) | `"enable-linger" "gnome" path:.github/workflows` | 12 hits; canonical/ubuntu-desktop-provision `ci.yml` → S4-14 | others not opened |
| 21 | 2026-09-23 | GitHub code search (MCP) | `"dkms build" "make.log" path:.github/workflows` | 16 hits; redhat-cne/netdevsim-dkms `ci.yml` → S4-13 | others not opened |
| 22 | 2026-09-23 | apt (local check) | `apt-get install dkms linux-headers-6.17.0-1022-azure`, then `v4l2loopback-dkms`, `zfs-dkms`, `nvidia-dkms-580-open` | → S4-16 | zfs-dkms 2.2.2 configure fails on 6.17 (see S4-16) |

---

## 2. Candidates

### S4-01 — actions/runner-images, Ubuntu 24.04 image definition and README

- Citation: GitHub, *actions/runner-images*, `images/ubuntu/Ubuntu2404-Readme.md` (Image Version 20260907.300.1) and build scripts.
- Copy read: `https://github.com/actions/runner-images.git`, commit `5257d1b466f9b19d009114c096e17e963f8f1b6c` (2026-09-21T21:57:36Z), accessed 2026-09-23. Local: `../sources/S4-01/`.
  - `Ubuntu2404-Readme.md` sha256 `4edbefde1df512f024363b1f66f78448f944f071c9e1775056b220d5bdc8dc81`
  - `configure-apt.sh` sha256 `217808ff019a6421d6f52775bbbba4f9b687d2c34819fbb9d858404c9ba7f3fa`
  - `configure-environment.sh` sha256 `7bb66dc8781fb8344ca8f85aa11b267365c1a93536c73a9f1de1d81e91335383`
  - `toolset-2404.json` sha256 `291c28ea606bdbf16ec8f11c1b60d54c97f1cf0496b23060771c05cbc1391414`
  - `post-build-validation.sh` sha256 `74c5480f012895892fcbb478fca8f882960b8f3b3bfbf5307ea4e761ce9b7ec5`
- Passages:
  - `images/ubuntu/Ubuntu2404-Readme.md:9-12` @5257d1b:
    > `- OS Version: 24.04.5 LTS`
    > `- Kernel Version: 6.17.0-1022-azure`
    > `- Image Version: 20260907.300.1`
    > `- Systemd version: 255.4-1ubuntu8.17`
  - `Ubuntu2404-Readme.md:269` > `| dbus                   | 1.14.10-4ubuntu4.1           |`
  - `Ubuntu2404-Readme.md:329` > `| xvfb                   | 2:21.1.12-1ubuntu1.6         |`
  - `Ubuntu2404-Readme.md:147-154` > `### Browsers and Drivers` / `- Google Chrome 152.0.7977.82` / … / `- Microsoft Edge 152.0.4191.66` / … / `- Mozilla Firefox 155.0`
  - `images/ubuntu/scripts/build/configure-apt.sh:9-15`:
    > `# Stop and disable apt-daily upgrade services;`
    > `systemctl stop apt-daily.timer`
    > `systemctl disable apt-daily.timer`
    > `systemctl disable apt-daily.service`
    > `systemctl stop apt-daily-upgrade.timer`
    > `systemctl disable apt-daily-upgrade.timer`
    > `systemctl disable apt-daily-upgrade.service`
  - `images/ubuntu/scripts/build/configure-environment.sh:85-94`:
    > `# Disable motd updates metadata`
    > `sed -i 's/ENABLED=1/ENABLED=0/g' /etc/default/motd-news`
    > `# Remove fwupd if installed. We're running on VMs in Azure and the fwupd package is not needed.`
    > `# Leaving it enable means periodic refreshes show in network traffic and firewall logs`
    > `# Check if fwupd-refresh.timer exists in systemd`
    > `if systemctl list-unit-files fwupd-refresh.timer &>/dev/null; then`
    > `    echo "Masking fwupd-refresh.timer..."`
    > `    systemctl mask fwupd-refresh.timer`
  - `configure-environment.sh:108-110`:
    > `# Disable man-db auto update`
    > `echo "set man-db/auto-update false" | debconf-communicate`
    > `dpkg-reconfigure man-db`
  - `images/ubuntu/toolsets/toolset-2404.json:150` > `"xvfb",`
- Coverage:
  - T13: covers — object: the ubuntu-24.04 hosted-runner image; states kernel (6.17.0-1022-azure), systemd 255.4 present, Xvfb and dbus packages installed, browsers installed; and that the image builders **disable** `apt-daily.timer`, `apt-daily-upgrade.timer`, mask `fwupd-refresh.timer`, disable motd-news and man-db auto-update. Consequence (inference, not a quotation): `systemctl list-timers` on the runner itself would show a modified, non-stock timer set; stock defaults must be read from packages (S4-08) or from a clean container/VM. No mention of GPU, display, desktop session or `/dev/kvm`.
  - T6: covers indirectly — names the stock Ubuntu timers that the image removes (apt-daily, apt-daily-upgrade, fwupd-refresh, motd-news, man-db auto-update); no schedule/duration.
  - T8: covers only package presence (`dbus` 1.14.10, `xvfb`); no desktop session packages listed in the apt table; does not cover session processes.
  - T1–T5, T7, T9–T12: does not cover.
- One observation? It is one image version (20260907.300.1) description, not a run. Machine: ubuntu-24.04 hosted runner image; no subjects; window: image built 2026-09-07.

### S4-02 — GitHub Docs, GitHub-hosted runners (specs, VM, nested virtualization, GPU)

- Citation: GitHub Docs, *GitHub-hosted runners* (concepts and reference) and reusable *supported-github-runners*, *larger-runners*.
- Copy read: `https://github.com/github/docs.git`, commit `61469655a1950d52a4346dc7f16cf231a29866af` (2026-09-22T16:28:48-07:00), accessed 2026-09-23. Local `../sources/S4-02/`.
  - `supported-github-runners.md` (= `data/reusables/actions/supported-github-runners.md`) sha256 `02da2db69d6b00be660ec0434aef5da48260d367e6c3f0e61dd59e9605eaa188`
  - `concepts-github-hosted-runners.md` (= `content/actions/concepts/runners/github-hosted-runners.md`) sha256 `af0e3264fb446a32985e90902cc8ab524c812cdbbbe8b21d2a24f5ea3c2f866a`
  - `reference-github-hosted-runners.md` (= `content/actions/reference/runners/github-hosted-runners.md`) sha256 `2ba4307f64e55251e63555e97a51381e4eb36334693a464c743522a09546a148`
  - `larger-runners.md` (= `content/actions/reference/runners/larger-runners.md`) sha256 `890ca099ff6313f39a4b5564371432721540c15e5e81721d5f0b7f599dd103e3`
- Passages:
  - `supported-github-runners.md:1-3` > `### Standard {% data variables.product.prodname_dotcom %}-hosted runners for public repositories` … `For public repositories, jobs using the workflow labels shown in the table below will run with the associated specifications.`
  - `supported-github-runners.md:19-26` (table row) > `<td>Linux</td>` `<td>4</td>` `<td>16 GB</td>` `<td>14 GB</td>` `<td> x64 </td>` … `ubuntu-24.04`
  - `supported-github-runners.md:96` > `### Standard {% data variables.product.prodname_dotcom %}-hosted runners for {% ifversion ghec %}internal and{% endif %} private repositories`
  - `supported-github-runners.md:114-118` > `<td>Linux</td>` `<td>2</td>` `<td>8 GB</td>` `<td>14 GB</td>` `<td> x64 </td>`
  - `concepts-github-hosted-runners.md:83` > `> * While nested virtualization is technically possible while using runners, it is not officially supported. Any use of nested VMs is experimental and done at your own risk, we offer no guarantees regarding stability, performance, or compatibility.`
  - `concepts-github-hosted-runners.md:100` > `{% data variables.product.prodname_dotcom %} hosts Linux and Windows runners on virtual machines in Microsoft Azure with the {% data variables.product.prodname_actions %} runner application installed.`
  - `reference-github-hosted-runners.md:77` > `The Linux and macOS virtual machines both run using passwordless `sudo`.`
  - `larger-runners.md:45-49` > `### Specifications for GPU {% data variables.actions.hosted_runners %}` … `| 4   | 1   | Tesla T4 | 28 GB        | 16 GB             | 176 GB        | Ubuntu, Windows       |`
- Coverage:
  - T13: covers — object: the standard hosted Linux runner; unit: vCPU / RAM / SSD; scope: **4 CPU, 16 GB RAM, 14 GB SSD only for public repositories; 2 CPU, 8 GB for private repositories** (the brief's "4 vCPU" holds only if the measuring repository is public); Azure VM; passwordless sudo; nested VMs "not officially supported"; GPUs exist only on paid larger runners (Tesla T4), not standard runners.
  - T1–T12: does not cover.
- One observation? No — documentation of a product class. No subjects, no window.

### S4-03 — GitHub Changelog 2024-04-02: KVM on 2-vCPU Linux hosted runners

- Citation: GitHub Changelog, "GitHub Actions: Hardware accelerated Android virtualization now available", April 2, 2024.
- Copy read: `https://github.blog/changelog/2024-04-02-github-actions-hardware-accelerated-android-virtualization-now-available/`, HTTP 200, accessed 2026-09-23, `../sources/S4-03/changelog-2024-04-02.html`, sha256 `1f577f588ddc74521a4bb1b25286a4d3a9bc753f655693ae9dce99c3a75d8738`.
- Passages (article body):
  > "Available now, Actions users of our 2-vCPU GitHub-hosted Linux runners will be able to make use of hardware acceleration for Android testing. Previously this feature was only available on runners with 4 or more vCPUs."
  > "To make use of this on Linux, Actions users will need to add the runner user to the KVM user group"
  > `echo 'KERNEL=="kvm", GROUP="kvm", MODE="0666", OPTIONS+="static_node=kvm"' | sudo tee /etc/udev/rules.d/99-kvm4all.rules`
  > `sudo udevadm control --reload-rules`
  > `sudo udevadm trigger --name-match=kvm`
- Coverage:
  - T13: covers — `/dev/kvm` is usable on hosted Linux runners (2 vCPU and ≥4 vCPU), so a KVM guest (a booted Ubuntu/Fedora/Arch VM image with real systemd, a real login session, default timers) is feasible on a runner, subject to S4-02's "nested virtualization … not officially supported". Does not state guest performance or limits.
  - T1–T12: does not cover.
- One observation? No — an announcement.

### S4-04 — happytomatoe/fedora-speech-to-text: headless GNOME Shell on a bare hosted runner

- Citation: happytomatoe, *fedora-speech-to-text*, PR #157 "ci: headless E2E test — GNOME Shell + extension + service + Parakeet on bare runner"; workflow `.github/workflows/ubuntu-ci-e2e.yml` and scripts.
- Copy read: `git fetch origin pull/157/head` from `https://github.com/happytomatoe/fedora-speech-to-text.git`, PR head commit `8d34c0b44c13d240127dfd9a0a263bd437948cb2` (2026-09-05T14:00:26+02:00); the same `ubuntu-ci-e2e.yml` and scripts are present on `main` at `2a6dcf8977004926e16ace9de43884951ca4ffa5` (2026-09-20). Accessed 2026-09-23. Local `../sources/S4-04/`:
  - `ubuntu-ci-e2e.yml` sha256 `f80d5236db56679228d4053096ec0b7f3f4618f1bee1a2f614ba920a26e457b6`
  - `ci-e2e-boot.sh` sha256 `3e4f0dd6eca71c209dc1f9f909327a5353c87e7448c1aefde147b5c2cf41f396`
  - `ci-e2e-stage.sh` sha256 `2208febfa5869312ffa38e3ab5de71b0565b984c36f44c9f5fe9d2fd272db549`
- Passages:
  - `.github/workflows/ubuntu-ci-e2e.yml:1-4` @8d34c0b:
    > `# E2E on Ubuntu 26.04 — bare-runner headless path (no VM, no image download).`
    > `# Boots a real GNOME Shell (Wayland, headless virtual monitor) directly on the`
    > `# runner, deploys the extension + Python service, drives a record → transcribe`
    > `# → typed-text assertion via D-Bus, and captures screenshots + screencast.`
  - `ubuntu-ci-e2e.yml:35` > `    runs-on: ubuntu-26.04`
  - `ubuntu-ci-e2e.yml` step "Install GNOME Shell + harness dependencies (no VM, no container)" > `gnome-shell gnome-shell-common gnome-session glib2.0-bin dbus \` … `pipewire pipewire-bin wireplumber \` `pulseaudio pulseaudio-utils \`
  - `.github/workflows/scripts/ci-e2e-stage.sh:69` > `dbus-daemon --session --fork --address="$DBUS_SESSION_BUS_ADDRESS" --print-pid > "$ISOLATED/.runtime/dbus.pid"`
  - `.github/workflows/scripts/ci-e2e-boot.sh:144-148` > `pipewire &` … `wireplumber &`
  - `ci-e2e-boot.sh:157-158` > `gnome-shell --headless --wayland --no-x11 \` / `  --virtual-monitor "${CI_E2E_WIDTH:-960}x${CI_E2E_HEIGHT:-540}" > "$HOME/shell.log" 2>&1 &`
- Coverage:
  - T13: covers — method, not result: a GNOME Shell compositor (Wayland, headless, virtual monitor, Xwayland off) started directly on a hosted runner, with a hand-started `dbus-daemon --session`, `pipewire`, `wireplumber`, `pulseaudio`. It is **not a full GNOME session**: no gdm, no `gnome-session` leader started, no systemd user manager, no logind session; it runs on `ubuntu-26.04`, not 24.04. No process list, timer list or timing is published in the files read (run logs were not reachable: the proxy refuses GitHub web/API for this repository).
  - T8: partial — shows which session components had to be started by hand for gnome-shell to work on a runner (session bus, PipeWire, WirePlumber, PulseAudio); not a stock baseline.
  - Others: does not cover.
- One observation? The workflow is one configuration; no run output was read. Machine: ubuntu-26.04 hosted runner; no subjects; window not named.

### S4-05 — Schneegans/gnome-shell-pod: full GNOME session in a systemd container on hosted runners

- Citation: Simon Schneegans, *gnome-shell-pod* (GitHub), and blog post "GNOME Shell Extensions & CI: Part III" (2022-03-02).
- Copy read:
  - repo `https://github.com/Schneegans/gnome-shell-pod.git` commit `a484ef2ce4623dd6e009eda5caa84eb4117bc304` (2024-11-06T09:29:14+01:00), accessed 2026-09-23. Files: `Dockerfile` sha256 `2d30d3a56f0fca8255d36af7b5500256b00b4c03c471c2a8c813c40cd2bd3a4a`; `README.md` sha256 `691ce281ad8f3c61862d49cdabd4817bef5419bc7a83f028981549e61851b66f`; `etc/systemd/user/gnome-xsession@.service` sha256 `c45cded3a41c8c4695c32ef100a5f8e2c2dd0ca1ed90a7531222e6f3375c5133`; `etc/systemd/user/gnome-wayland-nested@.service` sha256 `8967d16ec53c7cc3d09389bd27ced6e20aa254950098bf0c3083d4e9464ba336`; `etc/systemd/system/xvfb@.service` sha256 `cfddc7072238e0bf11a8a6469123f886e6004ef59ea29891db590440de62b030`; `.github/workflows/build.yml` sha256 `9116cd334773f8908b871a5d032d83bf398c66b1360d473a1f034b699faec8b2`.
  - blog `http://schneegans.github.io/tutorials/2022/03/02/gnome-shell-extensions-ci-03`, HTTP 200, sha256 `f68f085008520826bb824c2a9062f9910e1cb57cb10a86d8a29565babc60fa99`.
  - Local `../sources/S4-05/`.
- Passages:
  - `README.md:9` > `So I thought: Why not try getting GNOME Shell running on the runners of GitHub Actions?`
  - `README.md:25-27` > `- [x] Choose display manager:` / `  - [x] Wayland` / `  - [x] X11`
  - `README.md:32` > `- [x] All of this works locally and on the GitHub hosted runners!`
  - `README.md:36` > ``A user called "gnomeshell" will auto-login via `systemd-logind.service.d` and run `gnome-shell` on `xvfb`.``
  - `README.md:23` > `  - [x] [**gnome-shell-pod-41**](…): GNOME Shell 47.1 (based on Fedora 41)`
  - `Dockerfile:3` > `FROM registry.fedoraproject.org/fedora:${fedora_version}`
  - `Dockerfile:6-9` > `RUN dnf update -y && \` / `    dnf --nodocs install -y \` / `        gnome-session-xsession gnome-extensions-app xorg-x11-xinit \` / `        xorg-x11-server-Xvfb gnome-terminal xdotool xautomation sudo && \`
  - `Dockerfile:18-20` > `RUN systemctl unmask systemd-logind.service console-getty.service getty.target && \` / `    systemctl enable xvfb@:99.service && \` / `    systemctl set-default multi-user.target && \`
  - `Dockerfile:27` > `CMD [ "/usr/sbin/init", "systemd.unified_cgroup_hierarchy=0" ]`
  - `etc/systemd/user/gnome-xsession@.service:7` > `ExecStart=/etc/X11/xinit/Xsession "gnome-session --disable-acceleration-check"`
  - `etc/systemd/user/gnome-wayland-nested@.service:7-8` > `Environment="MUTTER_DEBUG_DUMMY_MODE_SPECS=1920x1080@30.0"` / `ExecStart=gnome-shell --nested --wayland --no-x11`
  - `etc/systemd/system/xvfb@.service:10` > `ExecStart=Xvfb %I $XVFB_SCREENS -fbdir ${XVFB_FBDIR}`
  - `.github/workflows/build.yml:9` > `    runs-on: ubuntu-latest`
  - Blog Part III, section "GNOME Shell in a Container": > "So the idea is to run GNOME Shell in a container, install the extension, and perform various tests on it. For this purpose, I created several Fedora-based containers, one for each GNOME Shell version I want to run tests on." and > `podman run --rm --cap-add=SYS_NICE --cap-add=IPC_LOCK \` / `-ti ghcr.io/schneegans/gnome-shell-pod-33` … `systemctl --user start "gnome-xsession@:99"`
- Coverage:
  - T13: covers — method: a Fedora container with **systemd as PID 1** (`/usr/sbin/init`), logind, an auto-logged-in user with a systemd user manager, Xvfb on :99, and `gnome-session` (X11) or `gnome-shell --nested --wayland`, run under podman on hosted runners. This is the documented route by which a runner can list a GNOME session's processes *and* the enabled systemd timers/services of a Fedora userspace (`systemctl list-timers` inside the container). Scope limits: the image installs `gnome-session-xsession` with `--nodocs`, not the Fedora Workstation package set, and it uses `multi-user.target`, so its timer set is not stock Workstation. No process list is published in the files read. Last GNOME listed is 47.1 / Fedora 41 (repo last commit 2024-11-06).
  - T8: method only (no names observed).
  - T6: method only.
  - Others: does not cover.
- One observation? No run output read. Machine class: GitHub hosted runner `ubuntu-latest` running podman; no subjects; no window.

### S4-06 — GNOME mutter command-line options (`--headless`, `--virtual-monitor`, `--nested`/`--devkit`)

- Citation: GNOME, *mutter*, `src/core/meta-context-main.c`.
- Copy read (gitlab.gnome.org raw), accessed 2026-09-23, `../sources/S4-06/`:
  - main at commit `888a7b7dac0c58612007c46bbad75de9f9437f48` (2026-09-17T21:51:45Z), `meta-context-main.c` sha256 `21c0bd4c87b73ff5ed142abebd64d80af2982f09ee474d441fadfc8fb1bde7d6`. (Newest tags at access: 51.0 2026-09-14, 50.5, 49.8.)
  - tag `46.2` = commit `02050414855b370dbf2b08a971c8b332f7b3c9f4` (2024-05-25), `meta-context-main-46.2.c` sha256 `a559e0b970c23f9f04fce303d1077f2ec9d20196d685b61c2aae0830a6b4d2d7`.
- Passages:
  - 46.2, `src/core/meta-context-main.c:643-646` > `"nested", 0, 0, G_OPTION_ARG_NONE,` / `&context_main->options.nested,` / `N_("Run as a nested compositor"),`
  - 46.2, `:668-670` > `"headless", 0, 0, G_OPTION_ARG_NONE,` / `&context_main->options.headless,` / `N_("Run as a headless display server")`
  - 46.2, `:673-675` > `"virtual-monitor", 0, 0, G_OPTION_ARG_CALLBACK,` / `add_virtual_monitor_cb,` / `N_("Add persistent virtual monitor (WxH or WxH@R)")`
  - 46.2, `:685-687` > `"x11", 0, 0, G_OPTION_ARG_NONE,` / `&context_main->options.x11.force,` / `N_("Run with X11 backend")`
  - main, `:349-351` > `"no-x11", 0, 0, G_OPTION_ARG_NONE,` / … / `N_("Run wayland compositor without starting Xwayland"),`
  - main, `:367-374` > `"headless", 0, 0, G_OPTION_ARG_NONE,` … `N_("Run as a headless display server")` … `"virtual-monitor", 0, 0, G_OPTION_ARG_CALLBACK,` … `N_("Add persistent virtual monitor (WxH or WxH@R)")`
  - main, `:378-380` > `"devkit", 0, 0, G_OPTION_ARG_NONE,` / `&context_main->options.devkit,` / `N_("Run development kit")`
- Coverage:
  - T13: covers — the headless/virtual-monitor modes exist in mutter 46.2 (the major version Ubuntu 24.04 ships; the exact noble version was not checked) and in current main; `--nested` exists in 46.2 but is absent from main's option table (main has `--devkit` instead; inference from the option tables above). gnome-shell inherits mutter's options (used as `gnome-shell --headless … --virtual-monitor` in S4-04 and `gnome-shell --nested` in S4-05).
  - Others: does not cover.
- One observation? No — source code.

### S4-07 — KDE KWin `--virtual` framebuffer backend

- Citation: KDE, *KWin*, `src/main_wayland.cpp`.
- Copy read: `https://invent.kde.org/plasma/kwin/-/raw/a5a83437d09024c802eb6db738cfd9cbfd97e41c/src/main_wayland.cpp` (master, 2026-09-23T02:46:21Z), accessed 2026-09-23, `../sources/S4-07/main_wayland.cpp` sha256 `17ad8fad7686195065b80a77d7ab50bc7aedf3a242b6a292edb2057b6d5c6881`.
- Passages:
  - `src/main_wayland.cpp:353` > `QCommandLineOption virtualFbOption(QStringLiteral("virtual"), i18n("Render to a virtual framebuffer."));`
  - `:354-356` > `QCommandLineOption widthOption(QStringLiteral("width"),` / `i18n("The width for windowed mode. Default width is 1024."),`
  - `:510-511` > `} else if (parser.isSet(virtualFbOption)) {` / `backendType = BackendType::Virtual;`
- Coverage: T13 — `kwin_wayland --virtual` renders to a virtual framebuffer (no GPU/display needed by design); a Plasma session on a runner would start from this. Does not state what else a Plasma session needs. Others: does not cover.
- One observation? No — source code.

### S4-08 — Local check: Ubuntu 24.04 desktop default-enabled timers from distribution packages (local check in this container, not a runner)

- What: dependency closure of a desktop install computed offline with apt, then the timer units and maintainer scripts of every package in the closure that ships a `.timer`.
- Copies read (all from `http://archive.ubuntu.com/ubuntu`, accessed 2026-09-23, local `../sources/S4-08/`):
  - `dists/noble/Contents-amd64.gz` sha256 `c8718dbbacd1ab72675513cf0674ff9921fcf781d9f49c4c0eaf68a49c18adc1`; `dists/noble-updates/Contents-amd64.gz` sha256 `e4252b8fc215c9ce63071ee3b7ced61f7a7e1bda4b1ac0672a547cb7286d2d67` (not kept; hashes in `contents.sha256`).
  - Packages (`apt-get download`, candidate versions on 2026-09-23), sha256:
    - anacron_2.3-39ubuntu2 `2b4142e8a0a451f4d3922dfcc8f5d04f9bc4d301bc5ef86c0321a151fd06d2c2`
    - apport_2.28.3-0ubuntu0.1 `3fb6842df77c2a60373981d2a00e25c11b3793f4301e115bcb9dd3e3b69e8847`
    - apt_2.8.3 `c9ace99efc7726fe0035f921a9acf262a9723bbf35b861aab4f9075a0be67442`
    - base-files_13ubuntu10.5 `87e8c41e62f61625fb78a982d0bc0a70f40ef8375bc313b154914d1b3759c823`
    - clamav-freshclam_1.5.4+dfsg-0ubuntu0.24.04.1 `684b8c6fb5c50a7efb744a2e1f2998cff1e847980cc1eccd6a39cba28a8981c2`
    - dkms_3.0.11-1ubuntu13 `18d098c65e3002040afc11f80656e84377551a5d1bdcd3933cdf6ae2e58dcd75`
    - dpkg_1.22.6ubuntu6.6 `ceb6aa4da59fbcb8a3b0549b4280c60b7d849b519859797c8668bdfbe378fb3b`
    - e2fsprogs_1.47.0-2.4~exp1ubuntu4.1 `1d0fb19dcf14316d04602260871dba3c1441c0ecf3c3bde54eacba35dcc5a40b`
    - fwupd_2.0.20-1ubuntu2~24.04.2 `0e04b5c0081114c080e4a3618e12e73a311f33bf061c8e53c151459a6149fcea`
    - logrotate_3.21.0-2build1 `e609ad80a9cec135b404a84f99d9d87bc304800eb212702444a985527edba70c`
    - man-db_2.12.0-4build2 `d7ce31173a73bd3a93b7216a837a2e8641fff3fd7ae2dfc0ca705dbabe03e92b`
    - plocate_1.1.19-2ubuntu2 `90375d69eda16ca5f73e6449447ef05c1a18b7b1de4092879eda9850898c04b0`
    - python3-launchpadlib_1.11.0-6 `5c6eacd5deae0da0839a614e7c80ec371a0b5d1482af96ca952ff71a33804979`
    - snapd_2.76.3+ubuntu24.04 `9ffe7430c7769234e58c9b83a5fe6e33c7ca963976133e4a0ede4c29dcd0fa82`
    - sysstat_12.6.1-2 `40f8a528434e2816f78869b7aa71a9ff4057678e76ae3a4109b5a7a72caa1285`
    - systemd_255.4-1ubuntu8.17 `250345b73e42a97ee71cae7c1e470897dfad3c639eb0a7aafe4f9a3a29871cb2`
    - tracker-miner-fs_3.7.1-1ubuntu0.1 `573bdac5dbd64761fe88f48bf54204f6ceb9f9c2e785e96a2e02ea0866f5ae41`
    - ubuntu-pro-client_37.2ubuntu~24.04.1 `c148f08254e2a961d473fb742660afd4041fc5a6e8907509640e0aaa20f11f75`
    - update-notifier-common_3.192.68.2 `50c3303b52aaaaadcf11750e1a0afc905bdee0d6f75aa2f1febdd4416afe7fec`
    - util-linux_2.39.3-9ubuntu6.6 `08eb17ba3b83378ed1e73d8335d0ce03b429c0bbeb07e374f536234edab02465`
  - Derived files: `closure2.txt` sha256 `52dabd3cf8f8db279ede1a403f786b6e16f68d075f171265194d852b7c5227ff`; `timers-in-closure.txt` sha256 `3d3a9799e3268c7529134b5b0bee4b0f76a5cde2fbcdf0c2b3432ebabf98ae21`; extracted `.timer` files in `timers/`, maintainer scripts in `postinst/` (e.g. `apt.postinst` sha256 `1c80cdeccd4358d3aeec6bb20d73397c85980a40cd7df524f8214d3ca80fca6f`, `sysstat.postinst` `3c0ea724533332c5bfa5f5376f12699bff418b4793ca3de432af48d56a0e5466`, `tracker-miner-fs.postinst` `eaacc7075a7755c4f680f113f5000bebf00beea61ebfc0cfb7ed37cafe5d6757`, `python3-launchpadlib.postinst` `d6849065388bc7b10a20403cac6df742a96f0f4612f84f404ff3c344def14a0d`), `sysstat.templates` `f75f4c5d833d948baaadfe3c53586654ab6acf0219b9d33f264596414d3a18ed`.
- Commands and output (local check in this container, not a runner):
  ```
  $ apt-cache policy ubuntu-desktop            → Candidate: 1.539.2 (noble-updates/main)
  $ REQ=$(apt-cache dumpavail | awk '/^Package:/{p=$2} /^Priority: required/{print p}' | sort -u)   → 73 packages
  $ apt-get -s -o Dir::State::status=/dev/null install ubuntu-desktop ubuntu-minimal ubuntu-standard $REQ | grep '^Inst' | wc -l
  1572
  $ zcat Contents-{noble,noble-updates}.gz | grep -E '^(usr/)?lib/systemd/(system|user)/[^[:space:]/]+\.timer[[:space:]]' → 154 (package,timer) pairs archive-wide
  $ (intersect with closure) → timers-in-closure.txt:
  anacron usr/lib/systemd/system/anacron.timer
  apport usr/lib/systemd/system/apport-autoreport.timer
  apt usr/lib/systemd/system/apt-daily-upgrade.timer
  apt usr/lib/systemd/system/apt-daily.timer
  base-files usr/lib/systemd/system/motd-news.timer
  dpkg usr/lib/systemd/system/dpkg-db-backup.timer
  e2fsprogs usr/lib/systemd/system/e2scrub_all.timer
  fwupd usr/lib/systemd/system/fwupd-refresh.timer
  logrotate usr/lib/systemd/system/logrotate.timer
  man-db usr/lib/systemd/system/man-db.timer
  python3-launchpadlib usr/lib/systemd/user/launchpadlib-cache-clean.timer
  snapd usr/lib/systemd/system/snapd.snap-repair.timer
  sysstat usr/lib/systemd/system/sysstat-collect.timer
  sysstat usr/lib/systemd/system/sysstat-summary.timer
  systemd usr/lib/systemd/system/systemd-sysupdate-reboot.timer
  systemd usr/lib/systemd/system/systemd-sysupdate.timer
  systemd usr/lib/systemd/system/systemd-tmpfiles-clean.timer
  systemd usr/lib/systemd/user/systemd-tmpfiles-clean.timer
  ubuntu-pro-client lib/systemd/system/ua-timer.timer
  update-notifier-common lib/systemd/system/update-notifier-download.timer
  update-notifier-common lib/systemd/system/update-notifier-motd.timer
  util-linux usr/lib/systemd/system/fstrim.timer
  ```
  (apport and snapd timers appear under both `lib/` and `usr/lib/` in the two Contents pockets; de-duplicated here.) Closure membership checks: `plocate`, `mlocate`, `popularity-contest`, `clamav`, `dkms`, `dbus-broker`, `pulseaudio`, `gnome-software`, `localsearch` **not** in the closure; `tracker-miner-fs`, `tracker`, `gdm3`, `gnome-shell`, `pipewire`, `wireplumber`, `dbus-daemon`, `xwayland`, `packagekit`, `unattended-upgrades`, `whoopsie`, `kerneloops`, `ubuntu-report`, `evolution-data-server`, `sysstat` in it.
- Timer schedules, verbatim `file:line` inside each package at the version above:
  - `anacron.timer:5-6` > `OnCalendar=*-*-* 07..23:30` / `RandomizedDelaySec=5m`
  - `apport-autoreport.timer` > `ConditionPathExists=/var/lib/apport/autoreport` … `:7` `OnUnitActiveSec=3h`
  - `apt-daily-upgrade.timer:6-7` > `OnCalendar=*-*-* 6:00` / `RandomizedDelaySec=60m`
  - `apt-daily.timer:5-6` > `OnCalendar=*-*-* 6,18:00` / `RandomizedDelaySec=12h`
  - `motd-news.timer:5-6` > `OnCalendar=00,12:00:00` / `RandomizedDelaySec=12h`
  - `dpkg-db-backup.timer:6` > `OnCalendar=daily`
  - `e2scrub_all.timer:6-7` > `OnCalendar=Sun *-*-* 03:10:00` / `RandomizedDelaySec=60`
  - `fwupd-refresh.timer:6-7` > `OnCalendar=*-*-* *:00:00` / `RandomizedDelaySec=1h`
  - `logrotate.timer:6` > `OnCalendar=daily`
  - `man-db.timer:6-7` > `OnCalendar=daily` / `RandomizedDelaySec=12h`
  - `plocate-updatedb.timer:5-6` > `OnCalendar=daily` / `RandomizedDelaySec=12h` (package not in the computed closure)
  - `launchpadlib-cache-clean.timer:6` (user unit) > `OnUnitActiveSec=1d`
  - `snapd.snap-repair.timer:8-9` > `OnCalendar=*-*-* 5,11,17,23:00` / `RandomizedDelaySec=2h`
  - `sysstat-collect.timer:11` > `OnCalendar=*:00/10`; `sysstat-summary.timer:12` > `OnCalendar=00:07:00`
  - `systemd-sysupdate.timer:23-26` > `OnBootSec=15min` / `OnUnitActiveSec=2h` / `OnCalendar=Sat` / `RandomizedDelaySec=4h`
  - `systemd-tmpfiles-clean.timer:16-17` > `OnBootSec=15min` / `OnUnitActiveSec=1d` (shipped pre-linked: `usr/lib/systemd/system/timers.target.wants/systemd-tmpfiles-clean.timer` is in the systemd package)
  - `ua-timer.timer` > `ConditionPathExists=/var/lib/ubuntu-advantage/private/machine-token.json` … `:9-10` `OnUnitActiveSec=6h` / `RandomizedDelaySec=1h`
  - `update-notifier-download.timer:7` > `OnUnitActiveSec=24h`; `update-notifier-motd.timer:6-7` > `OnCalendar=Sun *-*-* 06:00:00` / `RandomizedDelaySec=1w`
  - `fstrim.timer:8,11` > `OnCalendar=weekly` / `RandomizedDelaySec=100min`
  - `clamav-freshclam-once.timer:5,7` > `OnCalendar=daily` / `RandomizedDelaySec=1h` (not in closure)
- How they are enabled on install (Debian helper code in `postinst`): `apt.postinst:40-51` @apt 2.8.3:
  > `deb-systemd-helper unmask 'apt-daily.timer' >/dev/null || true`
  > `# was-enabled defaults to true, so new installations run enable.`
  > `if deb-systemd-helper --quiet was-enabled 'apt-daily.timer'; then`
  > `# Enables the unit on first installation, creates new`
  > `# symlinks on upgrades if the unit file has changed.`
  > `deb-systemd-helper enable 'apt-daily.timer' >/dev/null || true`
  The same `deb-systemd-helper enable '<timer>'` block is present (grep output, `file:line`) in: `anacron.postinst:79` (anacron.timer), `apport.postinst:52`, `apt.postinst:29` (apt-daily-upgrade.timer), `base-files.postinst:155` (motd-news.timer), `dpkg.postinst:97` (dpkg-db-backup.timer), `e2fsprogs.postinst:20`, `fwupd.postinst:36`, `logrotate.postinst:12`, `man-db.postinst:134`, `plocate.postinst:42`, `snapd.postinst:213` (snapd.snap-repair.timer), `sysstat.postinst:138,155`, `ubuntu-pro-client.postinst:165` (ua-timer.timer), `update-notifier-common.postinst:45,62`, `util-linux.postinst:17` (fstrim.timer); user-level: `python3-launchpadlib.postinst:23` > `deb-systemd-helper --user enable 'launchpadlib-cache-clean.timer'`; `tracker-miner-fs.postinst:51` > `deb-systemd-helper --user enable 'tracker-miner-fs-3.service'`. The systemd package postinst contains no `deb-systemd-helper` enable for `systemd-sysupdate*.timer` (grep found none).
  - Exception — sysstat: `sysstat.templates:135-138` > `Template: sysstat/enable` / `Type: boolean` / `Default: false` / `Description: Activate sysstat's cron job?`, and `sysstat.postinst:71` > `[ "$ENABLED" = "true" ] && enable_arg="enable" || enable_arg="disable"`, i.e. the enable block is overridden by a debconf default of false.
  - clamav-freshclam (not in closure): `postinst:592` > `update-rc.d clamav-freshclam defaults >/dev/null` (daemon `freshclam -d`, `WantedBy=multi-user.target`).
  - tracker-miner-fs also ships `etc/xdg/autostart/tracker-miner-fs-3.desktop` and D-Bus service files (file list, no content quoted).
- DKMS rebuild trigger on kernel install: `dkms` package `etc/kernel/postinst.d/dkms:37-39` @3.0.11-1ubuntu13 (sha256 of extracted file `6676f59b21b9678f05bc2d74afe613120aa1fbf08971ab7d1f319f962ac82a7f`):
  > `if [ -x /usr/lib/dkms/dkms_autoinstaller ]; then`
  > `    exec /usr/lib/dkms/dkms_autoinstaller start "$inst_kern"`
  > `fi`
  and `usr/sbin/dkms:1113` > `local the_make_command="${make_command/#make/make -j$parallel_jobs KERNELRELEASE=$kernelver}"`, `:2594` > `parallel_jobs=${parallel_jobs:-$(get_num_cpus)}`, `:1099` > `local -r build_log="$build_dir/make.log"`, `:1133` > `mv -f "$build_log" "$base_dir/log/make.log" 2>/dev/null`.
- Coverage:
  - T6: covers — object: timers shipped **and enabled by the package on install** in Ubuntu 24.04 (noble + noble-updates, 2026-09-23 candidates) for the apt-resolved closure of `ubuntu-desktop ubuntu-minimal ubuntu-standard` + Priority:required packages; unit: schedule expressions (OnCalendar / OnUnitActiveSec / RandomizedDelaySec); statistic: none (definitions, not runs); scope: system and user units; process names are **not** established (they are the `ExecStart` binaries of the matching `.service` files, not read here). It does not give durations. Caveats: (1) the closure is an apt approximation — the real Ubuntu desktop ISO is built from seeds, so membership (e.g. of `plocate`) is not verified; (2) enablement on install does not mean the unit fires: several have `ConditionPathExists` guards (apport autoreport, ua-timer) and sysstat defaults off.
  - T13: covers — shows a runner (or any Linux box, no boot needed) can list stock default timers and their enablement from packages without Docker or a VM.
  - T8: partial — package membership only (gdm3, gnome-shell, xwayland, pipewire, wireplumber, dbus-daemon in; dbus-broker, pulseaudio not in). Process names not observed.
- One observation? One offline resolution on 2026-09-23 in this container; not a running system.

### S4-09 — Fedora 44 systemd preset files (fedora-release)

- Citation: Fedora Project, dist-git `rpms/fedora-release`, branch f44, `fedora-release.spec` (Version: 44) and preset sources.
- Copy read: `https://src.fedoraproject.org/rpms/fedora-release/raw/818360081645fb80f235036073a01f080cd7eb9d/f/<file>` (f44 head at access), all HTTP 200, accessed 2026-09-23, `../sources/S4-09/`. sha256: `fedora-release.spec` `e0637699b7b8f965dbfa3b62fcdc44119840f3b2862368f845dfb79dffe4dccd`; `90-default.preset` `1d41ebae4a396e3c0579aba9db5516e1e412172bacae31ec9ed43b4ddb1ae25f`; `90-default-user.preset` `73c60a7416bc6aa2b2ab360b25c8320163b409f08117aefad3899e26adf70d30`; `80-workstation.preset` `4c2cc14fb93e2c3a2f202133a4b5be298296dac52a05ee9503472b3988088974`; `80-kde-desktop.preset` `a9ad58b04ea3356bacd036cc7980860deef396b18869a0ff7d2fe601aea20240`; `81-desktop.preset` `8f3fb70ebf5395787073ff7a02e85c7f3f25b8ca92c429329e63da73b1ccdfe1`; `99-default-disable.preset` `3127b197b9eae62eb84eeed69b0413419612238332006183e36a3fba89578378`.
- Passages:
  - `fedora-release.spec:74` > `Version:        44`; `:85-89` > `Source11:       90-default.preset` / `Source12:       90-default-user.preset` / `Source13:       99-default-disable.preset` / `Source14:       80-server.preset` / `Source15:       80-workstation.preset`; `:132` > `and systemd preset files that determine which services are enabled by default.`
  - `90-default.preset:1-2` > `# See https://docs.fedoraproject.org/en-US/packaging-guidelines/DefaultServices/` / `# for the Fedora policy.`
  - `90-default.preset:166` > `enable raid-check.timer`
  - `90-default.preset:175` > `enable dnf-makecache.timer`
  - `90-default.preset:187` > `enable dkms.service`
  - `90-default.preset:265` > `enable mlocate-updatedb.timer`; `:268` > `enable plocate-updatedb.timer`
  - `90-default.preset:343-344` > `# https://bugzilla.redhat.com/show_bug.cgi?id=1518258` / `enable akmods.service` (preceded by `# Ensure that any installed kmods are built for the currently-running` / `# kernel at boot`)
  - `90-default.preset:378-379` > `# Run fstrim weekly on filesystems listed in fstab` / `enable fstrim.timer`
  - `90-default.preset:387` > `enable logrotate.timer`
  - `90-default.preset:243-244` > `enable sysstat-collect.timer` / `enable sysstat-summary.timer`
  - `99-default-disable.preset:1` > `disable *`
  - `80-workstation.preset:4` > `enable low-memory-monitor.service`
  - `90-default-user.preset:5-6` > `enable dbus.socket` / `enable dbus-broker.service`; `:10` `enable pipewire.socket`; `:16` `enable pipewire-pulse.socket`; `:21` `enable wireplumber.service`; `:29` `enable grub-boot-success.timer`; `:42` `enable xdg-user-dirs.service`
  - `grep -c '^enable' 90-default.preset` → `188`
- Coverage:
  - T6: covers — object: Fedora 44 default-enabled units by preset (a unit is enabled only if its package is installed and a preset line names it; everything else is disabled by `99-default-disable.preset`); timers named: raid-check, dnf-makecache, mlocate/plocate-updatedb, sysstat-collect/summary, fstrim, logrotate, plus services dkms.service and akmods.service (kmod rebuild at boot). No schedules (those are in the owning packages, not read), no durations.
  - T8: partial — user presets name `dbus-broker.service` (message-bus implementation), `pipewire`, `pipewire-pulse`, `wireplumber` for Fedora 44 user sessions. Not an observation of running processes.
  - T13: covers — the preset files are what a runner (or a Fedora container) applies via `systemctl preset-all`; readable without booting.
- One observation? No — distribution configuration, Fedora 44, f44 branch head on 2026-09-23.

### S4-10 — Local check: Arch Linux presets and shipped timer symlinks (local check in this container, not a runner)

- Copies read: `https://geo.mirror.pkgbuild.com/{core,extra}/os/x86_64/<pkg>`, accessed 2026-09-23, `../sources/S4-10/`, sha256:
  - `systemd-261.3-1-x86_64.pkg.tar.zst` `8bb07794de615af02d07c672ac38bbb4833793a3c5a9c9af5b4e7667da4b2a4d` (`.PKGINFO`: `pkgver = 261.3-1`, `builddate = 1789072852`)
  - `man-db-2.13.1-2-x86_64.pkg.tar.zst` `499a8dc7e6b080514528352e7dff198717b85427c4722b878c5a7f56c9c14881`
  - `shadow-4.20.0.arch1-1-x86_64.pkg.tar.zst` `615c819eb2d3e22158289f3cc2447f81ae981a6d11b3418da30b6085306b3e77`
  - `util-linux-2.42.3-1-x86_64.pkg.tar.zst` `0b0486c01a71393319f2bad1908c59fc2dce3a98969d4a054449efa71214b3c3`
  - `logrotate-3.22.0-1-x86_64.pkg.tar.zst` `5a5619364c6655c15d35ef26359e0fd3fb570ec0dfa85e8ab0175eb630a9566f`
  - `pacman-7.1.0.r9.g54d9411-2-x86_64.pkg.tar.zst` `2092ec7a0391416e4a1757c455bc071d7b58a124cedc83f582cb7d37d52f211b`
  - `plocate-1.1.25-1-x86_64.pkg.tar.zst` `d0082c96e3e9632651d0c7deb1dab6496715223bfe9fbdded2cf94f3feae03bf`
  - extracted `99-default.preset` `3127b197b9eae62eb84eeed69b0413419612238332006183e36a3fba89578378`, `90-systemd.preset` `ad4f37d36408ed061a1631c47414fa428bc82ede4f878924c7e0bbad7cee4fbf`
- Commands (zstd from Ubuntu's `zstd` .deb, extracted without installing) and output:
  ```
  $ zstd -dc systemd-261.3-1-x86_64.pkg.tar.zst | tar -x
  $ ls usr/lib/systemd/system-preset usr/lib/systemd/user-preset
  usr/lib/systemd/system-preset: 90-systemd.preset  99-default.preset
  usr/lib/systemd/user-preset:   90-systemd.preset
  $ grep -n -v '^#' usr/lib/systemd/system-preset/99-default.preset
  1:disable *
  $ find usr/lib/systemd -path '*wants*' -name '*.timer'
  usr/lib/systemd/system/timers.target.wants/systemd-tmpfiles-clean.timer
  $ grep -n -i preset .INSTALL        → (no output)
  (per package) find … -name '*.timer' -o -path '*wants*' -type l
  man-db:    usr/lib/systemd/system/man-db.timer, usr/lib/systemd/system/timers.target.wants/man-db.timer
  shadow:    usr/lib/systemd/system/shadow.timer, usr/lib/systemd/system/timers.target.wants/shadow.timer
  util-linux: usr/lib/systemd/system/fstrim.timer            (no wants symlink)
  logrotate: usr/lib/systemd/system/logrotate.timer, usr/lib/systemd/system/timers.target.wants/logrotate.timer
  pacman:    (no timer; six sockets.target.wants gpg-agent/dirmngr/keyboxd @etc-pacman.d-gnupg sockets)
  plocate:   usr/lib/systemd/system/plocate-updatedb.timer, usr/lib/systemd/system/timers.target.wants/plocate-updatedb.timer
  ```
  Timer definitions (`file:line`): `man-db.timer:6-7` > `OnCalendar=daily` / `RandomizedDelaySec=12h`; `shadow.timer:5-6` > `OnCalendar=daily` / `AccuracySec=12h`; `logrotate.timer:6-7` > `OnCalendar=daily` / `RandomizedDelaySec=1h`; `plocate-updatedb.timer:5-7` > `OnCalendar=daily` / `RandomizedDelaySec=1h` / `AccuracySec=6h`; `systemd-tmpfiles-clean.timer:16-17` > `OnBootSec=15min` / `OnUnitActiveSec=1d`.
- Coverage:
  - T6: covers — on Arch (2026-09 packages), the preset default is `disable *` and the systemd package's install script has no preset call, **but** some packages ship static `timers.target.wants` symlinks, so these timers are active whenever the package is installed: systemd-tmpfiles-clean, man-db, shadow, logrotate, plocate-updatedb (plocate is optional). `fstrim.timer` is shipped but not linked. So "Arch enables nothing by default" is not true for timers. Package set of a given Arch desktop not determined; no durations.
  - T13: covers — readable from packages without a booted system.
- One observation? One check of mirror packages on 2026-09-23.

### S4-11 — Valve Developer Community, "SteamCMD" (via Wayback Machine)

- Citation: Valve Developer Community, *SteamCMD*, page "last edited on 25 July 2026, at 08:54".
- Copy read: `https://web.archive.org/web/20260909202315id_/https://developer.valvesoftware.com/wiki/SteamCMD` (Wayback capture 2026-09-09 20:23:15 UTC), HTTP 200, accessed 2026-09-23. Local `../sources/S4-11/SteamCMD-wb-20260909202315.html` (gzip as served) sha256 `48b797a74850ed26d35837d7255062c5526b082de0b9e8f4186c893db5593d4c`; decompressed `.decompressed.html` sha256 `980b2d15827364d70b91579ed9ba1e006c9e20a732b462a8b3dff51859b90571`. The live page could not be read (bot challenge / 403; search log #14).
- Also read: Ubuntu `steamcmd_0~20180105-5build1_i386.deb` (sha256 `62604a5dcda78be789b6907e789520fa5827148fe32b4139ac5097c9b7efd2ce`), man page `steamcmd.6.gz` line 53 > `"steamcmd +@sSteamCmdForcePlatformType windows +login "$USER" "$PASS" +app_update 2310 +quit"` (no mention of anonymous login in the man page or `steamcmdcommands.txt`).
- Passages (wiki text):
  - Intro > "The Steam Console Client or SteamCMD is a command-line version of the Steam Client. Its primary use is to install and update various dedicated servers available on Steam using a command-line interface."
  - § SteamCMD Login › Anonymous > "To download most game servers, you can login anonymously using login anonymous"
  - § SteamCMD Login › With a Steam Account > "Some servers require you to login with a Steam Account." and > "Note: A user can only be logged in once at any time (counting both graphical client as well as SteamCMD logins)."
  - § Automating SteamCMD › Command Line > `steamcmd +force_install_dir ../cs1_ds +login anonymous +app_update 730 +quit`
- Coverage:
  - T5: covers only the negative for a runner — anonymous SteamCMD installs dedicated-server depots, not a logged-in desktop client; a logged-in Steam account on a runner would log the same account out elsewhere (per the note). A runner therefore cannot observe the desktop Steam client's helper processes, overlay, or download-during-gameplay behaviour for a real account. A logged-out Steam desktop client could be started under Xvfb, but that shows only the bootstrap/login state (inference; not documented here).
  - T13: covers the Steam part of "what it cannot observe".
  - Others: does not cover.
- One observation? No — documentation.

### S4-12 — Mozilla Firefox Source Docs, Talos `ts_paint` (launch-to-paint measurement)

- Citation: Mozilla, *Firefox Source Docs — Talos* (`testing/perfdocs/talos.html`).
- Copy read: `https://firefox-source-docs.mozilla.org/testing/perfdocs/talos.html`, HTTP 200, accessed 2026-09-23, `../sources/S4-12/talos.html` sha256 `4d5401bd88114b32306f649e752c09d0bcc7ac7aa747652f7f3b73731cc5f15f`. Page carries no version number; content is as served on the access date.
- Passages:
  - § Test types › Startup > "Startup tests launch Firefox and measure the time to the onload or paint events. We run this in a series of cycles (default is 20) to generate a full set of data."
  - § ts_paint > "data: 20 times we start the browser and time how long it takes to paint the startup test page, resulting in 1 set of 20 data points."
  - § ts_paint > "summarization: … suite: ignore first data point, then take the median of the remaining 19 data points"
  - § ts_paint > "Starts the browser to display tspaint_test.html with the start time in the url, waits for MozAfterPaint and onLoad to fire, then records the end time and calculates the time to startup."
  - § ts_paint "Example Data" > `[1666.0, 1195.0, 1139.0, 1198.0, 1248.0, 1224.0, 1213.0, 1194.0, 1229.0, 1196.0, 1191.0, 1230.0, 1247.0, 1169.0, 1217.0, 1184.0, 1196.0, 1192.0, 1224.0, 1192.0]`
- Coverage:
  - T10: partial — a documented method for launch wall time (start → first paint/onload, 20 cycles, first discarded, median). Example data has no machine, OS or unit stated (values look like milliseconds; the unit is not given in the passage), so it is **not** a usable observation. No CPU time. Firefox only.
  - T13: method a runner could copy under Xvfb.
- One observation? The example data is one unlabelled series; machine, OS and window not named.

### S4-13 — redhat-cne/netdevsim-dkms CI: DKMS build + module load on hosted runners

- Citation: redhat-cne, *netdevsim-dkms*, `.github/workflows/ci.yml`.
- Copy read: `https://github.com/redhat-cne/netdevsim-dkms.git` commit `ba6fb6cdfce67c4d62429ddee253a59ee4b5c663` (2026-09-01T09:19:04-05:00), accessed 2026-09-23, `../sources/S4-13/netdevsim-dkms-ci.yml` sha256 `f40b0d9d8a96e16155241eec4ea03a640512d3f9ceca7bb3c07ef4609bb33697`.
- Passages:
  - `ci.yml:24-30` > `  dkms-test:` / `    runs-on: ${{ matrix.os }}` / `    timeout-minutes: 20` / … / `        os: [ubuntu-22.04, ubuntu-24.04]`
  - `ci.yml:45-46` > `dkms gcc make ethtool linuxptp \` / `linux-headers-$(uname -r)`
  - `ci.yml:64-70` > `sudo dkms add ${DKMS_PKG}/${DKMS_VER}` / `if sudo dkms build ${DKMS_PKG}/${DKMS_VER} 2>&1; then` … `sudo cat /var/lib/dkms/${DKMS_PKG}/${DKMS_VER}/build/make.log || true`
  - `ci.yml:82` > `sudo modprobe nsim_ptp`
- Coverage:
  - T13: covers (method) — a public workflow builds a DKMS module against the runner's own running kernel headers (`linux-headers-$(uname -r)`) on ubuntu-24.04 and loads it with `modprobe`, i.e. DKMS build **and** module loading work on hosted runners (as designed by this workflow; run results not read).
  - T6: does not give object counts or durations.
- One observation? No run output read.

### S4-14 — canonical/ubuntu-desktop-provision CI: systemd user manager on a runner via linger

- Citation: Canonical, *ubuntu-desktop-provision*, `.github/workflows/ci.yml`.
- Copy read: `https://github.com/canonical/ubuntu-desktop-provision.git` commit `8fc59c5219fc6a9693aab25a9739cd580aa813e3` (2026-09-18T15:51:40+02:00), accessed 2026-09-23, `../sources/S4-14/ubuntu-desktop-provision-ci.yml` sha256 `4a386ca58a23f98ec2dccd181964988e39932eaebfdb7c51fae7ce801bd0a447`.
- Passages:
  - `ci.yml:32` > `    runs-on: ubuntu-24.04`
  - `ci.yml:52-57` > `sudo loginctl enable-linger $USER` / `sudo systemctl start user@$UID.service` / `echo "XDG_RUNTIME_DIR=/run/user/$UID" >> $GITHUB_ENV` / `# write any setting to force-start dconf.service (via xvfb because dbus-launch needs a display)` / `xvfb-run -a gsettings set org.gnome.desktop.interface color-scheme "'default'"` / `- run: xvfb-run -a -s '-screen 0 1024x768x24 +extension GLX' flutter test integration_test/${{matrix.target}}`
- Coverage:
  - T13: covers (method) — on ubuntu-24.04 hosted runners, a systemd **user manager** for the runner user is started by `loginctl enable-linger` + `systemctl start user@$UID.service`; this implies systemd is the service manager on the runner VM (inference). Combined with Xvfb this gives the per-user service manager and user D-Bus needed for GNOME components. No process list.
  - T8: method only.
- One observation? No run output read.

### S4-15 — Tapuuk/Lumanin `de-smoke.yml`: author's statement that GNOME "does not fit a runner"

- Citation: Tapuuk, *Lumanin*, `.github/workflows/de-smoke.yml`.
- Copy read: `https://github.com/Tapuuk/Lumanin.git` commit `3ee3481d1db7301cbeab622f36e5823a38072d62` (2026-09-11T10:00:34+02:00), accessed 2026-09-23, `../sources/S4-15/de-smoke.yml` sha256 `3e66be55501ff4f99ed57b5a3fa318ca099544a9d12cf79c7bb3ed885c5afa8b`.
- Passages:
  - `de-smoke.yml:1-8` > `# The desktop-environment smoke test: the same Playwright real-window flows CI` / `# runs under Xvfb, but on a real Wayland compositor (sway, headless backend), so` / … / `# is exercised by a machine and not only by the dev desktop. sway is the one` / `# compositor that runs headless on a stock runner with no session, no GPU and no` / `# seat; KDE (kwin_wayland --virtual) is a possible later addition, GNOME does` / `# not fit a runner. This does not replace the human VM round —` / `# a headless compositor proves the code path, not the desktop.`
  - `de-smoke.yml:17` > `    runs-on: ubuntu-latest`
- Coverage: T13 — an opinion by a project author (not verified; contradicted in practice by S4-04's headless gnome-shell and S4-05's container session), and the useful caution that "a headless compositor proves the code path, not the desktop". Others: does not cover.
- One observation? No.

### S4-16 — Local check: DKMS builds against the runner's exact kernel headers (local check in this container, not a runner)

- What: installed `dkms` and `linux-headers-6.17.0-1022-azure` (the kernel named in S4-01's runner README) in this container, then built three out-of-tree modules with DKMS for that kernel release (not the container's running kernel). Compiler matches the kernel's: `CONFIG_CC_VERSION_TEXT="x86_64-linux-gnu-gcc-13 (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0"` from `/usr/src/linux-headers-6.17.0-1022-azure/.config`; local `gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0`. 4 CPUs (Intel Xeon @ 2.80GHz), 15 GiB RAM — similar to, but **not**, a public-repo hosted runner.
- Copies (`../sources/S4-16/`), sha256: `dkms-step1.log` `097f0b7c35c3f49dfd94d8d623ea16492f23c5550f726eecdcb1bec1441ea463`; `dkms-step2.log` `50bbfb1518b15000875d89fa1a4d407a571703ba04eeed34ed51f5b743d5553c`; `v4l2loopback-make.log` `9feb2b225b65be6f6cf8d9f049f14820c1021c54f4ed433336ea8d1d2a3daef9`; `dkms-rebuild.log` `4953bee832f9ff965a260a392e99bb45192d4c3295de32716ad6aa90683aba43`; `nvidia-install.log` `cba5bac213f9e76d2533ce3f153a4d922307e20a7f8cb4bf29ec587416956d07`; `nvidia-580-open-make.log` (initial build) `f56e9af669d7380301c1d57d6cf929fc1dc8b0c59414091f2b69ec39c31c13b1`; `nvidia-580-open-make.rebuild.log` `f6b42e0e60370aadb73c4467297c75cbd50077c29b18c83b50b42678ea80ea3d`; `nvidia-rebuild.log` `79a136be305f1f8b9366769aa99d5f9edff973cad182c9e45ad738dbae31a112`. Packages: `v4l2loopback-dkms 0.12.7-2ubuntu5.1`, `nvidia-dkms-580-open 580.178.04-0ubuntu0.24.04.1` (source deb `nvidia-kernel-source-580-open` sha256 `7ddde45d5325e7fffaffe5d78106ab28668069233a70a18d5c8f1bc29a364215`), `zfs-dkms 2.2.2-0ubuntu9.5` (sha256 `1d095eeb3d47ee9f3e420636b6c44afff50c19127bf2a54dd23eeb68ebc8eaae`), `virtualbox-dkms 7.0.16-dfsg-2ubuntu1.3` (downloaded only, sha256 `ee8193da2905ebfadbb068696437b93c0775be650555d7dc719bdb16e856031a`).
- Commands and output:
  ```
  $ apt-get install -y --no-install-recommends dkms linux-headers-6.17.0-1022-azure     (04:16:43Z → 04:16:51Z)
  $ apt-get install -y --no-install-recommends v4l2loopback-dkms                         (04:17:00Z → 04:17:09Z)
  Loading new v4l2loopback-0.12.7 DKMS files...
  It is likely that 6.18.44-fc-v37 belongs to a chroot's host
  Building for 6.17.0-1022-azure
  Building initial module for 6.17.0-1022-azure
  Done.
  $ cat /var/lib/dkms/v4l2loopback/0.12.7/6.17.0-1022-azure/x86_64/log/make.log  (excerpt)
  DKMS make.log for v4l2loopback-0.12.7 for kernel 6.17.0-1022-azure (x86_64)
  Wed Sep 23 04:17:05 UTC 2026
    CC [M]  v4l2loopback.o
    MODPOST Module.symvers
    CC [M]  v4l2loopback.mod.o
    CC [M]  .module-common.o
    LD [M]  v4l2loopback.ko
    BTF [M] v4l2loopback.ko
  Skipping BTF generation for v4l2loopback.ko due to unavailability of vmlinux
  $ for i in 1 2 3; do time dkms build v4l2loopback/0.12.7 -k 6.17.0-1022-azure --force; done
  real 2.558 s  user 2.525 s  sys 0.420 s
  real 2.706 s  user 2.586 s  sys 0.671 s
  real 2.769 s  user 2.597 s  sys 0.558 s

  $ apt-get install -y --no-install-recommends nvidia-dkms-580-open    (2026-09-23T04:20:33.12Z → 04:21:55.86Z, includes unpacking 4 packages)
  Building for 6.17.0-1022-azure
  Building initial module for 6.17.0-1022-azure
  Done.
  $ L=/var/lib/dkms/nvidia/580.178.04/6.17.0-1022-azure/x86_64/log/make.log
  $ head -2 $L → "DKMS make.log for nvidia-580.178.04 for kernel 6.17.0-1022-azure (x86_64)" / "Wed Sep 23 04:20:41 UTC 2026"
  $ grep -o -E '^# [A-Z]+ ?(\[M\])? ' $L | sort | uniq -c
        5 # BTF [M]
      214 # CC [M]
       10 # LD [M]
        1 # MODPOST
        2 # SYMLINK
  $ grep -E '^# LD \[M\].*\.ko' $L
  # LD [M]  nvidia.ko
  # LD [M]  nvidia-modeset.ko
  # LD [M]  nvidia-uvm.ko
  # LD [M]  nvidia-drm.ko
  # LD [M]  nvidia-peermem.ko
  $ grep -E '^# CC \[M\]' $L | awk '{print $4}' | awk -F/ '{print $1}' | sort | uniq -c
      1 .module-common.o   59 nvidia   19 nvidia-drm   1 nvidia-drm.mod.o   2 nvidia-modeset   1 nvidia-modeset.mod.o
      1 nvidia-peermem     1 nvidia-peermem.mod.o   127 nvidia-uvm   1 nvidia-uvm.mod.o   1 nvidia.mod.o
  $ grep 'SYMLINK nvidia/nv-kernel.o' -A1 $L
  # SYMLINK nvidia/nv-kernel.o
    ln -sf /var/lib/dkms/nvidia/580.178.04/build/nvidia/nv-kernel.o_binary nvidia/nv-kernel.o
  $ time dkms build nvidia/580.178.04 -k 6.17.0-1022-azure --force
  real 72.823 s  user 216.634 s  sys 35.520 s

  $ apt-get install -y --no-install-recommends zfs-dkms
  Building for 6.17.0-1022-azure
  Building initial module for 6.17.0-1022-azure
  Error! Bad return status for module build on kernel: 6.17.0-1022-azure (x86_64)
  $ grep -n -E 'Linux-Maximum|Linux-Minimum' /usr/src/zfs-2.2.2/META
  9:Linux-Maximum: 6.6
  10:Linux-Minimum: 3.10
  $ sed -n 1026,1045p /var/lib/dkms/zfs/2.2.2/build/config.log  (excerpt)
  configure:62346: error:
  	*** None of the expected "blkdev_get_by_path()" interfaces were detected.
  	*** This may be because your kernel version is newer than what is
  	*** supported, or you are using a patched custom kernel with
  	*** incompatible modifications.
  	*** ZFS Version: zfs-2.2.2-0ubuntu9.5
  	*** Compatible Kernels: 3.10 - 6.6
  (zfs removed afterwards with `dkms remove zfs/2.2.2 --all`; config.log was deleted with it and is not preserved — the excerpt above is the only copy.)

  Source-file counts (not objects): find usr/src -name '*.c' | wc -l
  zfs-dkms 290   virtualbox-dkms 112   nvidia-kernel-source-580-open 208
  ```
- Coverage:
  - T6: covers — object: DKMS builds of out-of-tree modules for Ubuntu's 6.17.0-1022-azure kernel; unit: compiled objects (Kbuild `CC [M]` lines in `make.log`) and seconds; statistic: counts and single/three-run wall/CPU times; population: this container only. Results: v4l2loopback 0.12.7 = 1 source object (+ `.mod.o`, `.module-common.o`), ~2.6–2.8 s wall per `dkms build`; NVIDIA 580.178.04 open = 214 `CC [M]` (208 source objects + 5 `.mod.o` + 1 `.module-common.o`) plus 2 linked prebuilt binaries, 5 `.ko`, 72.8 s wall / 216.6 s user / 35.5 s sys for one forced `dkms build` at `-j4`; the full `apt-get install` including unpack and initial build took 82.7 s. zfs-dkms 2.2.2 (noble) cannot build for 6.17 at all (max 6.6). virtualbox-dkms 7.0.16 was not built. A DKMS autoinstall on a real kernel update runs the same `dkms_autoinstaller` (S4-08) and therefore the same build, but that path was not timed here.
  - T13: covers — a runner-equivalent local check that a real DKMS module compiles against the runner kernel's headers and that objects and time can be counted from `make.log` and `time`.
  - T7: marginal — a module build size, not a user project build; does not cover.
- One observation? Yes: one machine (this container: 4 vCPU Xeon @ 2.80 GHz, 15 GiB, Linux 6.18.44-fc-v37 host kernel, Ubuntu 24.04.4 userspace), subject none, window 2026-09-23 04:16–04:24 UTC. Timings would differ on a hosted runner.

---

## 3. What a runner can and cannot observe, and proposed runner steps (not results)

Established from documentation (S4-01, S4-02, S4-03, S4-14): ubuntu-24.04 hosted runner = Azure VM, kernel 6.17.0-1022-azure, systemd 255.4 installed, passwordless sudo, Xvfb installed, `/dev/kvm` usable after a udev rule, nested virtualization "not officially supported", 4 vCPU/16 GB only for public repositories (2 vCPU/8 GB private), no GPU on standard runners, image builders disable apt-daily/apt-daily-upgrade and mask fwupd-refresh.

Proposed runner steps (commands only; **not run**):

1. Runner baseline (T13, T8 negative control): `cat /proc/1/comm; systemd-detect-virt; ls -l /dev/kvm /dev/dri 2>&1; systemctl list-timers --all --no-pager; systemctl list-unit-files --state=enabled --no-pager; ps -eo pid,ppid,comm,etimes,time --sort=pid`.
2. Headless GNOME Shell on the runner (T8, T13; after S4-04): `sudo apt-get install -y gnome-shell gnome-session pipewire wireplumber dbus-user-session xwayland`; `sudo loginctl enable-linger $USER; sudo systemctl start user@$UID.service` (S4-14); `export XDG_RUNTIME_DIR=/run/user/$UID`; `dbus-run-session -- gnome-shell --headless --wayland --virtual-monitor 1920x1080 & sleep 30; ps -eo pid,ppid,comm --forest > gnome-ps.txt; systemctl --user list-units --no-pager > user-units.txt`. A full `gnome-session` under the user manager: `dbus-run-session -- gnome-session --session=ubuntu` with `XDG_SESSION_TYPE=wayland` (untested; may need a logind seat).
3. Full stock desktop in a KVM guest (T6, T8, T13): enable `/dev/kvm` (S4-03 udev rule), boot an Ubuntu 24.04 desktop cloud/ISO image or Fedora 44 Workstation Live with `qemu-system-x86_64 -enable-kvm -m 8G -smp 3 -display none -vnc :0`, autologin, then over SSH/serial `systemctl list-timers --all`, `ps -eo comm`, `busctl --user list`. Only this route yields stock timers *and* a stock session (gdm, logind seat) on a runner; stability "not officially supported" (S4-02).
4. Fedora container (T6, T13; after S4-05): `podman run --rm fedora:44 sh -c 'dnf -y group install workstation-product-environment --setopt=install_weak_deps=True && systemctl preset-all && systemctl list-unit-files --state=enabled --type=timer,service'` (offline `systemctl` in the container; no boot).
5. Arch container: `podman run --rm archlinux:latest sh -c 'pacman -Syu --noconfirm gnome && ls /usr/lib/systemd/system/timers.target.wants /etc/systemd/system/timers.target.wants'`.
6. DKMS on the real runner (T6): the S4-16 commands verbatim, with `linux-headers-$(uname -r)`; plus a real kernel-update path: `sudo apt-get install linux-headers-<next> linux-image-<next>` and `time` the `dkms_autoinstaller` output in the apt log.
7. Application launch under Xvfb (T10): `xvfb-run -a sh -c 'start=$(date +%s.%N); gnome-text-editor & pid=$!; xdotool search --sync --onlyvisible --pid $pid >/dev/null; echo map $(echo "$(date +%s.%N)-$start"|bc); for i in $(seq 60); do awk "{print \$14+\$15}" /proc/$pid/stat; sleep 0.5; done'` — map time plus CPU ticks until they stop increasing ("settled"). Software rendering only (llvmpipe); cold vs warm cache must be separated. Method pattern after S4-12 (repeat 20, drop first, median).
8. Steam (T5, negative): `steamcmd +login anonymous +app_update <dedicated-server appid> +quit` observes SteamCMD only; `xvfb-run steam` observes the logged-out bootstrapper/login window only.

What a runner cannot observe (documentation-based, S4-02, S4-11, S4-15, and inference): real users, their co-occurring applications, focus sequences, dwell times, browsing and tab behaviour, in-application operations, video-call use (T1–T4, T7, T9, T11 — no subjects exist on a runner); a real GPU, a real display/seat, gamescope on real hardware, a Proton game using a GPU, a logged-in Steam client and its download-while-playing behaviour (T5); launch times on real desktop hardware with GPU acceleration (T10 only under software rendering); the stock timer set *of the runner itself* (modified by the image builders, S4-01).

---

## 4. Not found

- **T1 Application co-occurrence, T2 Focus and switching, T3 Activity order, T4 Browser tabs (user side), T7 Size of user-started jobs, T9 Operations within applications, T11 Video calls and media, T12 Public traces** — no S4 candidate. A runner has no users; nothing a runner runs is an observation of real desktop use. Established by searches #1–#2, #4 (runner documentation lists only installed software and VM specs) and #19–#21 (public workflows use desktops only as test harnesses). T4's process-count side (Chromium renderer processes for a given tab set) could be measured on a runner (Chrome 152 is installed, S4-01), but no document or workflow doing so was searched for or found; this belongs to S2/S1.
- **T5 Gaming composition** — no positive candidate: no document or workflow found that runs a Steam desktop client or a Proton game on a hosted runner. Searches #14–#16 (SteamCMD wiki, Ubuntu steamcmd package) establish only that anonymous SteamCMD serves dedicated servers and that one account can be logged in once. A runner has no GPU (S4-02).
- **T10 Launch timings on Linux as observations** — no observation with machine and window named; only a method (S4-12, example data without machine). Search #17.
- **Process lists of a headless/nested GNOME or KDE session on a runner** — no published process list found; S4-04/S4-05 give methods only, and run logs were unreachable (GitHub web/API refused by the session proxy for repositories not attached; search log #3, #6). Search #18 found no runner documentation on systemd user sessions.
- **DKMS object counts / autoinstall durations documented by others on runners** — not found; search #21 found workflows that build DKMS modules (S4-13) but none publishing counts or times in the files read. Only the local check S4-16 gives numbers.

Unreachable sources: developer.valvesoftware.com (bot challenge, HTTP 200 challenge page / 403 via WebFetch) — read via Wayback capture 20260909202315; github.com web and REST API for `github/docs` and `happytomatoe/fedora-speech-to-text` (session proxy refusal) — read via git clone/fetch instead; Actions run logs for any workflow (not attempted beyond the proxy refusal).
