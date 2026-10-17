# S4 — own measurement on a CI runner (T11 CI observability): documentation research

> Reader class S4 · task 9.10 scenarios and timelines, stage 2 search · written 2026-10-01 · nothing was measured and no workflow was run; every runner-side statement below is a documented fact (quoted), a reader's reading or inference labelled as such, or a check a runner would have to make (Appendix B).

Topic T11 asks which of the questions T1–T10 a GitHub-hosted `ubuntu-24.04` runner (4 vCPUs, no GPU, no physical display, Xvfb, sudo; the load pinned to one CPU with `taskset`, instruments on the others: `perf sched record` on `CLOCK_MONOTONIC` read with `perf sched timehist` and its wakeup rows, taskstats with delay accounting, `/proc` snapshots) can observe, and what it cannot. All candidates below are documents of deployed software or of public package archives: under the brief's rules they establish **existence only** (what is installed, packaged, scheduled, configurable). None is an observation of program or user behaviour: for every candidate the answer to "one observation?" is *no — a document*, so no machine, run or observation window applies; the subject (program, package, image) and its version are named in each citation. Where the reader extracted or computed something from a downloaded file, it is labelled *reader's own* and the command is given.

Local copies are under `sources/S4-NN/` (gitignored). Passages in fenced blocks are copied verbatim from those files by a script, with the file's own line numbers; the few inline quotations (marked "verbatim substring" or "verbatim, tags stripped") were checked as exact substrings of the stated copy. Nothing in this record depends on the local copies surviving.

---

## 1. Search log

All rows dated 2026-10-01. "200/206/302/404/500" are HTTP statuses as returned to `curl` (or the tool named).

| # | engine / venue | query terms or URL | hits followed | dead ends (status) |
|---|---|---|---|---|
| 1 | git, github.com | `git ls-remote https://github.com/actions/runner-images.git` (HEAD = `14d8569222caf7662f18b6875bf518683db9ff58`; newest tag `ubuntu24/20260927.320`) | blobless sparse clone of `images/ubuntu` at `14d8569…` → S4-01 | — |
| 2 | curl, docs.github.com | `https://docs.github.com/en/actions/reference/runners/github-hosted-runners` (200) and its markdown body `https://docs.github.com/api/article/body?pathname=/en/actions/reference/runners/github-hosted-runners` (200) | → S4-02 | — |
| 3 | curl, docs.github.com | `https://docs.github.com/api/article/body?pathname=/en/actions/reference/limits` (200) | → S4-02 | — |
| 4 | WebSearch | `github.blog changelog hardware accelerated Android virtualization Linux larger runners /dev/kvm udev rule` | `https://github.blog/changelog/2024-04-02-github-actions-hardware-accelerated-android-virtualization-now-available/` (200) → S4-02 | — |
| 5 | curl, releases.ubuntu.com | `https://releases.ubuntu.com/24.04/` listing (200); `ubuntu-24.04.5.1-desktop-amd64.manifest` (200), `.list` (200), `SHA256SUMS` (200) | → S4-03 | — |
| 6 | curl byte ranges, releases.ubuntu.com | `https://releases.ubuntu.com/24.04/ubuntu-24.04.5.1-desktop-amd64.iso` with `Range:` (206 Partial Content; `Content-Range: bytes 32768-34815/6250332160`) — ISO 9660 directory of `/casper`, the layer manifests, `install-sources.yaml`, the metadata tail (inode table → end) of `minimal.squashfs` and `minimal.standard.squashfs`, and selected small files from fragment blocks | → S4-03 | — |
| 7 | curl, archive.ubuntu.com | `dists/noble/Contents-amd64.gz` (200), `dists/noble-updates/Contents-amd64.gz` (200) | → S4-04 | — |
| 8 | curl, launchpad.net librarian | `https://launchpad.net/ubuntu/+archive/primary/+files/<pkg>_<ver>_<arch>.deb` for 19 desktop packages at the manifest versions (200 each when the right architecture was used) | → S4-05 | wrong-architecture guesses for `Architecture: all` packages: `apport_2.28.3-0ubuntu0.1_amd64.deb` (404), `update-notifier-common_3.192.68.2_amd64.deb` (404), `python3-launchpadlib_1.11.0-6_amd64.deb` (404), `cron-daemon-common_3.0pl1-184ubuntu2_amd64.deb` (404), `unattended-upgrades_2.9.1+nmu4ubuntu1_amd64.deb` (404); the `_all.deb` names returned 200 |
| 9 | curl, archive.ubuntu.com | `dists/{noble,noble-updates}/{main,restricted,universe,multiverse}/binary-amd64/Packages.xz` (8 × 200) | → S4-06 | — |
| 10 | curl, archive.ubuntu.com pool | `dkms_3.0.11-1ubuntu13_all.deb`, `v4l2loopback-dkms_0.12.7-2ubuntu5.2_all.deb`, `linux-headers-6.17.0-1022-azure_6.17.0-1022.22_amd64.deb`, `linux-azure-6.17-headers-6.17.0-1022_6.17.0-1022.22_all.deb`, `deja-dup_45.2-1build2_amd64.deb` (200 each) | → S4-05, S4-07, S4-08 | — |
| 11 | curl, changelogs.ubuntu.com | `virtualbox_7.0.16-dfsg-2ubuntu1.3/changelog`, `zfs-linux_2.2.2-0ubuntu9.5/changelog`, `nvidia-graphics-drivers-580_580.178.04-0ubuntu0.24.04.1/changelog` (200 each) | → S4-07 | — |
| 12 | curl, gnu.org | `https://www.gnu.org/software/coreutils/manual/html_node/nproc-invocation.html` (200) | → S4-07 | — |
| 13 | WebSearch | `GitHub Actions hosted runner secure boot enabled mokutil sb-state dkms module load ubuntu runner` | no GitHub source on the runners' Secure Boot state; Ubuntu wiki page tried | `https://wiki.ubuntu.com/UEFI/SecureBoot/DKMS?action=raw` (404); `https://web.archive.org/web/2026id_/https://wiki.ubuntu.com/UEFI/SecureBoot/DKMS` (500); `https://web.archive.org/web/20260804171646id_/…` (500) — replaced by the kernel's own Kconfig and module-signing source (S4-08, S4-09) |
| 14 | curl, raw.githubusercontent.com | `torvalds/linux` at tag `v6.17`: `tools/perf/Documentation/perf-sched.txt`, `perf-record.txt`, `Documentation/accounting/delay-accounting.rst`, `Documentation/admin-guide/sysctl/kernel.rst`, `…/sysctl/vm.rst`, `include/linux/sched.h`, `kernel/module/signing.c` (200 each); `systemd/systemd` at `v255`: `man/systemd.resource-control.xml` (200) | → S4-09 | — |
| 15 | WebSearch | `Steam support offline mode must be logged in previously "Offline Mode"` | community threads and third-party pages only — not primary, not followed | — |
| 16 | WebSearch | `Steam "downloads during gameplay" setting help.steampowered.com` | `https://help.steampowered.com/en/faqs/view/71AB-698D-57EB-178C` (200; article body is in the page's embedded `data-faqstore` JSON) → S4-10 | WebFetch of the same URL returned navigation only (body rendered by script) |
| 17 | curl, developer.valvesoftware.com | `https://developer.valvesoftware.com/wiki/SteamCMD?action=raw` | Wayback availability API → snapshot `20260101130455`; `https://web.archive.org/web/20260101130455id_/https://developer.valvesoftware.com/wiki/SteamCMD` (200, article) → S4-10 | direct URL: 200 but an Anubis "Making sure you're not a bot!" page (dead end, deleted); `https://web.archive.org/web/2026id_/…` → 302 to `20260924234729id_`, which is the same bot-check page (dead end, deleted) |
| 18 | git + curl, github.com | `git ls-remote` of `ValveSoftware/Proton` (`5b89db94…`), `Open-Wine-Components/umu-launcher` (`e2b203a1…`), `ValveSoftware/gamescope` (`0e590c75…`), `ValveSoftware/steam-runtime` (`8cb6d88c…`), `jitsi/docker-jitsi-meet` (`5ba823f9…`), `webrtc/samples` (`6e2c5a11…`); raw READMEs and umu sources at those commits (200 each) | → S4-11, S4-14 | — |
| 19 | curl, api.github.com | `repos/{Open-Wine-Components/umu-launcher, Open-Wine-Components/umu-proton, GloriousEggroll/proton-ge-custom, ValveSoftware/Proton}/releases/latest` (200 each) | → S4-11 | — |
| 20 | curl, repo.steampowered.com | `steamrt-images-sniper/snapshots/latest-container-runtime-public-beta/BUILD_ID.txt` (200), `steamrt4/images/latest-public-beta/BUILD_ID.txt` (200), `steamrt3/images/latest-public-beta/BUILD_ID.txt` (200, body `3.0.20260914.260626`) — the host umu downloads the Steam Linux Runtime from, fetched without credentials | → S4-11 | — |
| 21 | curl / git, gitlab.freedesktop.org | `https://gitlab.freedesktop.org/mesa/mesa/-/raw/mesa-25.2.8/docs/envvars.rst` | `git clone --depth 1 --branch mesa-25.2.8` (tag object `5287731b…` → commit `f97d7dcca0e51d7e20ed4342bb5ea8afea7db7fa`), `docs/envvars.rst` → S4-12 | raw URL: 200 but an Anubis bot-check page (dead end, deleted); `https://raw.githubusercontent.com/Mesa3D/mesa/mesa-25.2.8/docs/envvars.rst` (404); `https://web.archive.org/web/2026id_/https://docs.mesa3d.org/envvars.html` (200, gzip; not used, git copy preferred) |
| 22 | curl, raw.githubusercontent.com | `chromium/chromium` at tag `153.0.8010.52` (→ `78e5e45d…`): `media/base/media_switches.cc`, `media/capture/capture_switches.cc`, `content/public/common/content_switches.cc` (200 each) | → S4-13 | — |
| 23 | curl, vendor repositories | `packages.microsoft.com/repos/code/…/Packages.gz` (200); `dl.google.com/linux/chrome/deb/…/Packages` (200); `repository.spotify.com/dists/testing/non-free/…/Packages` (200); `packages.microsoft.com/repos/ms-teams/…/Packages` (200, **0 bytes**); `packagecloud.io/slacktechnologies/slack/debian/…/Packages` (200); `packages.element.io/debian/…/Packages` (200); `repo.steampowered.com/steam/dists/stable/steam/binary-{amd64,i386}/Packages` (200, 200); `dl.winehq.org/wine-builds/ubuntu/dists/noble/main/binary-amd64/Packages` (200) | → S4-15 | — |
| 24 | curl -I, vendor download URLs | `https://zoom.us/client/latest/zoom_amd64.deb` → 302 `https://cdn.zoom.us/prod/7.2.1.5760/zoom_amd64.deb` → 200 (`content-length: 302788858`); `https://discord.com/api/download?platform=linux&format=deb` → 302 `https://stable.dl2.discordapp.net/apps/linux/1.0.160/discord-1.0.160.deb` → 200 | recorded in S4-15 | — |
| 25 | WebSearch | `Microsoft Teams Linux client retirement December 2022 progressive web app techcommunity` | `https://techcommunity.microsoft.com/blog/microsoftteamsblog/microsoft-teams-progressive-web-app-now-available-on-linux/3669846` (200) → S4-15 | the other hits are third-party summaries, not followed |
| 26 | curl, raw.githubusercontent.com | `GNOME/mutter` at tag `46.2`: `src/core/meta-context-main.c` (200) | → S4-16 | — |
| 27 | WebSearch | `sysstat enabled by default Ubuntu 24.04 desktop sysstat-collect.timer launchpad bug ENABLED=false` | no primary source on the state of sysstat on a stock 24.04 desktop | (see §3) |
| 28 | WebSearch | `GitHub-hosted runner ubuntu-24.04 Azure VM size CPU model processor documented` | GitHub docs only (vCPU / RAM / SSD) | (see §3) |

---

## 2. Candidates

### S4-01 — actions/runner-images: the `ubuntu-24.04` runner image definition at commit `14d8569`

- **Citation.** GitHub, actions/runner-images, `images/ubuntu/Ubuntu2404-Readme.md` (Image Version 20260920.314.1; the Readme was last changed by commit `c9dd57c6b6333892b46abcc439ba0676fd03867a`, 2026-09-25) and the build scripts `images/ubuntu/scripts/build/*.sh`, `images/ubuntu/templates/locals.ubuntu.pkr.hcl`, `images/ubuntu/toolsets/toolset-2404.json`, all at commit `14d8569222caf7662f18b6875bf518683db9ff58` (branch `main`, accessed 2026-10-01).
- **Copy read.** Blobless sparse `git clone` of `https://github.com/actions/runner-images.git`, checkout `14d8569…`; files copied to `sources/S4-01/`.

| file (under `sources/S4-01/`) | bytes | SHA-256 |
|---|---:|---|
| `Ubuntu2404-Readme.md` | 16328 | `a37278942f07a81dc00eac64cfb123130a36f52432a5e687d91a626488718735` |
| `configure-apt.sh` | 3865 | `0857e4ceed76b032bbf82588f52ea2f9acea086c9c2609f170d03a6705f48807` |
| `configure-environment.sh` | 5713 | `d891d1a107d55fca792efce0cebf1170df8097e47ec44c6fdf12404a17351201` |
| `configure-snap.sh` | 995 | `eb9318854aac758fc67ca89bd586de503a13b6764359b6b9bb5b55f1e9f8575f` |
| `configure-system.sh` | 1513 | `604976982f8515d86df578993b6c852bc636d53555fefeaa61fa984ecc7fef11` |
| `install-firefox.sh` | 1674 | `dfd2dad863f82472390759bc3e1b35dba6bf2faafdfdcb1912d6d5cecaacc3f3` |
| `install-google-chrome.sh` | 4303 | `73dfff23f2ae59d94c9f44cd5212fadc309fd15889df3b4d9bb5eeddef555386` |
| `locals.ubuntu.pkr.hcl` | 1176 | `9de904fe6c77708d0c22506ae61411f61bd97e036f405569f32c7616d15958cf` |
| `toolset-2404.json` | 7613 | `291c28ea606bdbf16ec8f11c1b60d54c97f1cf0496b23060771c05cbc1391414` |

- **Passages.**

`sources/S4-01/Ubuntu2404-Readme.md` lines 9–12:
```
    9  - OS Version: 24.04.5 LTS
   10  - Kernel Version: 6.17.0-1022-azure
   11  - Image Version: 20260920.314.1
   12  - Systemd version: 255.4-1ubuntu8.17
```
`sources/S4-01/Ubuntu2404-Readme.md` lines 148–154:
```
  148  - Google Chrome 153.0.8010.52
  149  - ChromeDriver 153.0.8010.52
  150  - Chromium 153.0.8010.0
  151  - Microsoft Edge 153.0.4234.48
  152  - Microsoft Edge WebDriver 153.0.4234.48
  153  - Selenium server 4.49.0
  154  - Mozilla Firefox 156.0
```
`sources/S4-01/Ubuntu2404-Readme.md` lines 329–329:
```
  329  | xvfb                   | 2:21.1.12-1ubuntu1.6          |
```
`sources/S4-01/locals.ubuntu.pkr.hcl` lines 11–14:
```
   11        "ubuntu24" = {
   12              source_image_marketplace_sku = "canonical:ubuntu-24_04-lts:server"
   13              os_disk_size_gb = 75
   14        },
```
`sources/S4-01/configure-apt.sh` lines 9–15:
```
    9  # Stop and disable apt-daily upgrade services;
   10  systemctl stop apt-daily.timer
   11  systemctl disable apt-daily.timer
   12  systemctl disable apt-daily.service
   13  systemctl stop apt-daily-upgrade.timer
   14  systemctl disable apt-daily-upgrade.timer
   15  systemctl disable apt-daily-upgrade.service
```
`sources/S4-01/configure-apt.sh` lines 70–71:
```
   70  # Uninstall unattended-upgrades
   71  apt-get purge unattended-upgrades
```
`sources/S4-01/configure-environment.sh` lines 94–103:
```
   94  # Disable motd updates metadata
   95  sed -i 's/ENABLED=1/ENABLED=0/g' /etc/default/motd-news
   96  
   97  # Remove fwupd if installed. We're running on VMs in Azure and the fwupd package is not needed.
   98  # Leaving it enable means periodic refreshes show in network traffic and firewall logs
   99  # Check if fwupd-refresh.timer exists in systemd
  100  if systemctl list-unit-files fwupd-refresh.timer &>/dev/null; then
  101      echo "Masking fwupd-refresh.timer..."
  102      systemctl mask fwupd-refresh.timer
  103  fi
```
`sources/S4-01/configure-environment.sh` lines 117–119:
```
  117  # Disable man-db auto update
  118  echo "set man-db/auto-update false" | debconf-communicate
  119  dpkg-reconfigure man-db
```
`sources/S4-01/configure-environment.sh` lines 75–87:
```
   75  # Relax root filesystem durability guarantees to speed up I/O heavy workloads. Runner VMs are
   76  # ephemeral, so losing recent writes on an unclean shutdown is acceptable.
   77  # data= and journal_async_commit can only be set on the initial mount performed by the initramfs,
   78  # so they have to be passed through rootflags on the kernel command line rather than through fstab.
   79  root_fs_type=$(findmnt --noheadings --first-only --output FSTYPE --target /)
   80  if [[ "$root_fs_type" != "ext4" ]]; then
   81      echo "Expected an ext4 root filesystem but found '${root_fs_type}', refusing to set ext4 rootflags"
   82      exit 1
   83  fi
   84  
   85  grub_dropin='/etc/default/grub.d/99-runner-performance.cfg'
   86  mkdir -p "$(dirname "$grub_dropin")"
   87  echo 'GRUB_CMDLINE_LINUX_DEFAULT="$GRUB_CMDLINE_LINUX_DEFAULT rootflags=nobarrier,data=writeback,journal_async_commit,commit=30"' | tee "$grub_dropin"
```
`sources/S4-01/configure-snap.sh` lines 15–26:
```
   15  # Put snapd auto refresh on hold
   16  # as it may generate too much traffic on Canonical's snap server
   17  # when they are rolling a new major update out.
   18  # Hold is calculated as today's date + 60 days
   19  
   20  # snapd is started automatically, but during image generation
   21  # a unix socket may die, restart snapd.service (and therefore snapd.socket)
   22  # to make sure the socket is alive.
   23  
   24  systemctl restart snapd.socket
   25  systemctl restart snapd
   26  snap set system refresh.hold="$(date --date='today+60 days' +%Y-%m-%dT%H:%M:%S%:z)"
```
`sources/S4-01/install-firefox.sh` lines 21–26:
```
   21  FIREFOX_REPO="ppa:mozillateam/ppa"
   22  
   23  # Install Firefox
   24  add-apt-repository $FIREFOX_REPO -y
   25  apt-get update
   26  apt-get install --target-release 'o=LP-PPA-mozillateam' -y firefox
```
`sources/S4-01/install-google-chrome.sh` lines 37–45:
```
   37  # Download and install Google Chrome
   38  CHROME_DEB_URL="https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
   39  chrome_deb_path=$(download_with_retry "$CHROME_DEB_URL")
   40  apt-get install "$chrome_deb_path" -f
   41  set_etc_environment_variable "CHROME_BIN" "/usr/bin/google-chrome"
   42  
   43  # Remove Google Chrome repo. The glob covers the legacy .list and the deb822 .sources layouts.
   44  # Keep /etc/default/google-chrome: its repo_add_once="false" is what stops the repo coming back.
   45  rm -f /etc/cron.daily/google-chrome /etc/apt/sources.list.d/google-chrome*
```
`sources/S4-01/install-google-chrome.sh` lines 74–87:
```
   74  # Download and unpack Chromium
   75  chrome_revision=$(echo "${chrome_versions_json}" | jq -r '.builds["'"$chrome_version"'"].revision')
   76  chromium_revision=$(get_chromium_revision $chrome_revision)
   77  chromium_url="https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F${chromium_revision}%2Fchrome-linux.zip?alt=media"
   78  CHROMIUM_DIR="/usr/local/share/chromium"
   79  chromium_bin="${CHROMIUM_DIR}/chrome-linux/chrome"
   80  
   81  echo "Installing chromium revision $chromium_revision"
   82  chromium_archive_path=$(download_with_retry "$chromium_url")
   83  mkdir $CHROMIUM_DIR
   84  unzip -qq "$chromium_archive_path" -d $CHROMIUM_DIR
   85  
   86  ln -s $chromium_bin /usr/bin/chromium
   87  ln -s $chromium_bin /usr/bin/chromium-browser
```

- **Coverage.** T11 — covers: the runner's operating system (Ubuntu 24.04.5 LTS), kernel (`6.17.0-1022-azure`), systemd version, preinstalled browsers (Google Chrome 153.0.8010.52 from Google's deb; Chromium 153.0.8010.0 as a snapshot zip under `/usr/local/share/chromium`, not the Ubuntu snap; Firefox 156.0 from the Mozilla Team PPA as a deb, not the snap), Xvfb, Docker; that the image is built from Canonical's Azure **server** image (`canonical:ubuntu-24_04-lts:server`), not a desktop install; and that the image build changes background jobs: `apt-daily.timer` and `apt-daily-upgrade.timer` stopped and disabled, `unattended-upgrades` purged, `fwupd-refresh.timer` masked, motd-news disabled, man-db auto-update set false, snap auto-refresh held for 60 days, and the root ext4 file system mounted with `nobarrier,data=writeback,journal_async_commit,commit=30`. T1–T10: does not cover. Not an observation (documents of deployed software; existence only). Machine: the GitHub-hosted `ubuntu-24.04` image, version 20260920.314.1; window: the image as described at the named commit (the repository's tags `ubuntu24/20260823.283` … `ubuntu24/20260927.320` show the image being replaced; a newer tag than the Readme's image version existed at access time).

### S4-02 — GitHub Docs: GitHub-hosted runners reference, Actions limits; GitHub changelog of 2024-04-02

- **Citation.** GitHub Docs, "GitHub-hosted runners reference", `https://docs.github.com/en/actions/reference/runners/github-hosted-runners` (accessed 2026-10-01, as HTML and as the markdown body served by `docs.github.com/api/article/body`); GitHub Docs, "Actions limits", `https://docs.github.com/en/actions/reference/limits` (markdown body, accessed 2026-10-01); GitHub Changelog, "GitHub Actions: Hardware accelerated Android virtualization now available", 2024-04-02, `https://github.blog/changelog/2024-04-02-github-actions-hardware-accelerated-android-virtualization-now-available/` (accessed 2026-10-01).
- **Copy read.** `sources/S4-02/`.

| file (under `sources/S4-02/`) | bytes | SHA-256 |
|---|---:|---|
| `actions-limits.md` | 30767 | `6041828ec4a05a04ddc67b5507f5ef5ede480e66593923ba91b9cad1b69abd58` |
| `gh-changelog-2024-04-02-android-virtualization.html` | 95717 | `e8cbc65c5b22bffed6e8c8d8a3d5a5316ab7f8a289153643167d476994db8eb3` |
| `github-hosted-runners.html` | 432872 | `bc976212fda6dbb704b6389c3b9210d927dac30b326dd5b6173cf49e0092f97a` |
| `github-hosted-runners.md` | 20497 | `2537c22a86f6ee64431576ab49bb6d2043270dbea0f8737ab4bf2f242f09d198` |

- **Passages.**

`sources/S4-02/github-hosted-runners.md` lines 14–14:
```
   14  GitHub-hosted Linux runners support hardware acceleration for Android SDK tools, which makes running Android tests much faster and consumes fewer minutes. For more information on Android hardware acceleration, see [Configure hardware acceleration for the Android Emulator](https://developer.android.com/studio/run/emulator-acceleration) in the Android Developers documentation.
```
`sources/S4-02/github-hosted-runners.md` lines 24–24:
```
   24  For public repositories, jobs using the workflow labels shown in the table below will run with the associated specifications. With the exception of single-CPU runners, each GitHub-hosted runner is a new virtual machine (VM) hosted by GitHub. Single-CPU runners are hosted in a container on a shared VM—see [GitHub-hosted runners reference](/en/actions/reference/runners/github-hosted-runners#single-cpu-runners). Use of the standard GitHub-hosted runners is free and unlimited on public repositories.
```
`sources/S4-02/github-hosted-runners.md` lines 48–60:
```
   48      <tr>
   49        <td>Linux</td>
   50        <td>4</td>
   51        <td>16 GB</td>
   52        <td>14 GB</td>
   53        <td> x64 </td>
   54        <td>
   55          <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md">ubuntu-latest</a></code>,
   56          <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md">ubuntu-24.04</a></code>,
   57          <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2204-Readme.md">ubuntu-22.04</a></code>,
   58          <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2604-Readme.md">ubuntu-26.04</a></code>
   59        </td>
   60      </tr>
```
`sources/S4-02/github-hosted-runners.md` lines 128–128:
```
  128  For  private repositories, jobs using the workflow labels shown in the table below will run on virtual machines with the associated specifications. These runners use your GitHub account's allotment of free minutes, and are then charged at the per minute rates. See [Actions runner pricing](/en/billing/reference/actions-runner-pricing).
```
`sources/S4-02/github-hosted-runners.md` lines 152–163:
```
  152      <tr>
  153        <td>Linux</td>
  154        <td>2</td>
  155        <td>8 GB</td>
  156        <td>14 GB</td>
  157        <td> x64 </td>
  158        <td>
  159          <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md">ubuntu-latest</a></code>,
  160          <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md">ubuntu-24.04</a></code>,
  161          <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2204-Readme.md">ubuntu-22.04</a></code>,
  162          <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2604-Readme.md">ubuntu-26.04</a></code>
  163        </td>
```
`sources/S4-02/github-hosted-runners.md` lines 256–265:
```
  256  Larger runners are available for organizations and enterprises on GitHub Team and GitHub Enterprise Cloud plans.
  257  
  258  Larger runners are managed virtual machines with more resources than [standard GitHub-hosted runners](/en/actions/reference/runners/github-hosted-runners#supported-runners-and-hardware-resources). They offer the following advanced features:
  259  
  260  * More RAM, CPU, and disk space
  261  * Static IP addresses
  262  * Azure private networking
  263  * The ability to group runners
  264  * Autoscaling to support concurrent workflows
  265  * GPU-powered runners
```
`sources/S4-02/github-hosted-runners.md` lines 273–273:
```
  273  The Linux and macOS virtual machines both run using passwordless `sudo`. When you need to execute commands or install tools that require more privileges than the current user, you can use `sudo` without needing to provide a password. For more information, see the [Sudo Manual](https://www.sudo.ws/man/1.8.27/sudo.man.html).
```

`actions-limits.md` line 31, row "All GitHub-hosted runners | Job execution time | 6 hours", description cell (verbatim substring): "Each job in a workflow can run for up to 6 hours of execution time. If a job reaches this limit, the job is terminated and fails."

`gh-changelog-2024-04-02-android-virtualization.html`, article text (verbatim, tags stripped): "Available now, Actions users of our 2-vCPU GitHub-hosted Linux runners will be able to make use of hardware acceleration for Android testing. Previously this feature was only available on runners with 4 or more vCPUs. To make use of this on Linux, Actions users will need to add the runner user to the KVM user group" followed by the step `echo 'KERNEL=="kvm", GROUP="kvm", MODE="0666", OPTIONS+="static_node=kvm"' | sudo tee /etc/udev/rules.d/99-kvm4all.rules`, `sudo udevadm control --reload-rules`, `sudo udevadm trigger --name-match=kvm`.

- **Coverage.** T11 — covers: the standard `ubuntu-24.04` runner is a fresh VM per job with 4 CPUs / 16 GB RAM / 14 GB SSD **in public repositories** and 2 CPUs / 8 GB / 14 GB **in private repositories**; passwordless `sudo`; GPUs only on "larger runners" (Team / Enterprise Cloud plans); KVM usable after a udev rule (so a nested VM can be booted on the runner); a 6-hour cap per job. Does not name the Azure VM size, the CPU model, the network bandwidth, or the Secure Boot state (see §3). Not an observation. Machine: GitHub-hosted runners as documented on 2026-10-01.

### S4-03 — Ubuntu 24.04.5.1 desktop ISO: install layers, layer manifests, and the timer and cron state shipped in the image (reader's own extraction)

- **Citation.** Canonical, `ubuntu-24.04.5.1-desktop-amd64.iso` (6 250 332 160 bytes; SHA-256 `4da4a0c9035da8e68a59a838674f403f0a54472c78a83b4fb7f78d03588f85a7` per the release's `SHA256SUMS`; ISO `Last-Modified: Mon, 14 Sep 2026 23:20:53 GMT`), `https://releases.ubuntu.com/24.04/`, accessed 2026-10-01. The installer offers two layers: `minimal.squashfs` = "Ubuntu Desktop (minimized)", id `ubuntu-desktop-minimal`, the default; `minimal.standard.squashfs` = "Ubuntu Desktop", id `ubuntu-desktop`, the extended selection. `minimal.standard.live` is the live session only.
- **Copy read.** The release-directory files, and byte ranges of the ISO read with `curl -r` by the reader's scripts `isoread.py` (ISO 9660 + Rock Ridge directory walk of `/casper`), `sqfs.py` (SquashFS 4.0 superblock, inode table and directory table parse; xz metadata blocks) and `sqcat.py` (small-file read through the fragment table). The metadata tails fetched were bytes `inode_table_start … bytes_used` of each squashfs (2 408 400 bytes for `minimal.squashfs`, 901 560 bytes for `minimal.standard.squashfs`), saved as `*.meta-tail.bin`. Commands: `python3 isoread.py <outdir>`; `python3 sqfs.py 49794 minimal.meta <paths…>` (49794 = ISO extent of `minimal.squashfs`, 2048-byte sectors); `python3 sqfs.py 1208605 standard.meta <paths…>`; `python3 sqcat.py 49794 minimal.meta <outdir> <files…>`.

| file (under `sources/S4-03/`) | bytes | SHA-256 |
|---|---:|---|
| `SHA256SUMS` | 893 | `728064ecf411f4ab702d9c3ca0a938ce672771424c028a1b52b2449f7eb5a068` |
| `filesystem.manifest` | 64285 | `6c200933618b2e382e7732b69b247aa5f63ed6600d8ee730d57b02ec74e4f8ff` |
| `install-sources.yaml` | 679 | `3d3e0d097b51c21aeb8d3330de0220e33d29e694dd56c0de5797b8bbc6cb1ec9` |
| `isoread.py` | 1426 | `5efdb34a3129c493ccc54ca87e0bf4e8902cf42d32bc5350cd0021467f5b9444` |
| `minimal.manifest` | 53244 | `31544e9fb82e6c7e4d8f6062f46bc2ec5d7e7061b4df1040036c061d33206a49` |
| `minimal.squashfs.meta-tail.bin` | 2408400 | `81ca7f070864655613a2da18dac436eb1deaba0a7559a4e3ec719a1e72d0e5b9` |
| `minimal.standard.live.manifest` | 4668 | `d94776bd26ffd5223b271e4616fb272b0fba6a8734cfc2fa7d113f4e25694c07` |
| `minimal.standard.manifest` | 8732 | `99fce3823f2ce2f253ff92f5517f94f0779afa3ade60ff881fc8ef58adb5aa1d` |
| `minimal.standard.squashfs.meta-tail.bin` | 901560 | `53d27c5bc0e4fcf864d065201fc7388670f433b3afcdbaa7855efbab9fcfcc1b` |
| `sq_minimal_listing.txt` | 3162 | `0805c9b18c00c441e687bd4d96889700470a0718d5b63a13976f0c09fcd42be3` |
| `sq_standard_listing.txt` | 596 | `8dceca50d5825c79940323ace651b2f45f657d4d0f1a0c895ded8ab1dd287efc` |
| `sqcat.py` | 1859 | `a5a23b2940e9c6c03f1094c134a241ce8e96d7751afe220d6a17b043f9d50654` |
| `sqfs.py` | 3506 | `6065d5a4389fdb0090baa1cf1f9da740b432fe3fb164ec4550a7e0f7ee0a9ead` |
| `ubuntu-24.04.5.1-desktop-amd64.list` | 30479 | `9fb3e8041e7e95b028f5629069295fb079e93499f55ce2c88901afc087895ad2` |
| `ubuntu-24.04.5.1-desktop-amd64.manifest` | 64285 | `6c200933618b2e382e7732b69b247aa5f63ed6600d8ee730d57b02ec74e4f8ff` |
| `extracted/etc__apt__apt.conf.d__10periodic` | 129 | `82d9ce0d3f5d2c66945d8a1267445e9955409d1ef3cb9934107adccb46bf5f6a` |
| `extracted/etc__apt__apt.conf.d__20auto-upgrades` | 80 | `b81a3a01864d5ed7f8d023f3fa86d65087ad6b85706d399dc229a60b1c784807` |
| `extracted/etc__default__anacron` | 830 | `f8154cdaed40aa93224cb78fd84f351f0a75e0055b37042e0470eac3e227031e` |
| `extracted/etc__default__apport` | 149 | `810304fb0df6dbc8a651a8928ddd0bb2b521fa0ca6f32a328aa103be61977f91` |
| `extracted/etc__default__kerneloops` | 84 | `33daf1bdf1ce4018bf8c532280c8accb741c7c9077523a34d272c4a59451bba4` |
| `extracted/etc__default__sysstat` | 284 | `df83ca773bd3100f2402028ef23b2e64641a293805e0e88a4fb892f999bdd09a` |
| `extracted/etc__systemd__user__snap.firmware-updater.firmware-notifier.service` | 408 | `4948e32ad3636521f3b212771a4e9ee72a70309348f6273e5e8cf4e4065811fb` |
| `extracted/etc__systemd__user__snap.firmware-updater.firmware-notifier.timer` | 422 | `640be96a7a4cc06f86abb8a0b05e1c3b748fadc462ced2fcd4f22fe33d628db5` |
| `extracted/usr__share__glib-2.0__schemas__10_ubuntu-settings.gschema.override` | 7258 | `fa63fa302dd98cab86551705a60ac980dd88196b1460d164963e4d7cfb76c27a` |

- **Passages (published files).**

`sources/S4-03/install-sources.yaml` lines 1–8:
```
    1  - default: true
    2    description:
    3      en: A minimal but usable Ubuntu Desktop.
    4    id: ubuntu-desktop-minimal
    5    locale_support: langpack
    6    name:
    7      en: Ubuntu Desktop (minimized)
    8    path: minimal.squashfs
```
`sources/S4-03/install-sources.yaml` lines 22–29:
```
   22  - default: false
   23    description:
   24      en: A full featured Ubuntu Desktop.
   25    id: ubuntu-desktop
   26    locale_support: langpack
   27    name:
   28      en: Ubuntu Desktop
   29    path: minimal.standard.squashfs
```
`sources/S4-03/minimal.manifest` (matching lines):
```
   11  +anacron	2.3-39ubuntu2
   14  +apport	2.28.3-0ubuntu0.1
   19  +apt	2.8.3
   31  +base-files	13ubuntu10.5
   64  +cron	3.0pl1-184ubuntu2
   82  +dbus-daemon	1.14.10-4ubuntu4.1
  107  +dpkg	1.22.6ubuntu6.6
  109  +e2fsprogs	1.47.0-2.4~exp1ubuntu4.1
  119  +evince	46.3.1-0ubuntu1.1
  126  +firefox	1:1snap1-0ubuntu5
  147  +fwupd	2.0.20-1ubuntu2~24.04.2
  238  +gnome-shell	46.0-0ubuntu6~24.04.14
 1139  +logrotate	3.21.0-2build1
 1145  +man-db	2.12.0-4build2
 1204  +pipewire:amd64	1.0.5-1ubuntu3.3
 1241  +python3	3.12.3-0ubuntu2.1
 1279  +python3-launchpadlib	1.11.0-6
 1319  +rsync	3.2.7-1ubuntu1.5
 1335  +snapd	2.76.3+ubuntu24.04
 1358  +sysstat	12.6.1-2
 1361  +systemd	255.4-1ubuntu8.17
 1381  +tracker-miner-fs	3.7.1-1ubuntu0.1
 1384  +ubuntu-desktop-minimal	1.539.2
 1390  +ubuntu-pro-client	37.2ubuntu~24.04.1
 1404  +unattended-upgrades	2.9.1+nmu4ubuntu1
 1410  +update-notifier-common	3.192.68.2
 1417  +util-linux	2.39.3-9ubuntu6.6
 1477  +xwayland	2:23.2.6-1ubuntu0.8
```
`sources/S4-03/minimal.standard.manifest` (matching lines):
```
    4  +deja-dup	45.2-1build2
    5  +duplicity	2.1.4-3ubuntu2
  137  +libreoffice-writer	4:24.2.7-0ubuntu0.24.04.6
  188  +thunderbird	2:1snap1-0ubuntu3
  210  +ubuntu-desktop	1.539.2
```
`sources/S4-03/minimal.standard.live.manifest` (matching lines):
```
   85  +linux-generic-hwe-24.04	7.0.0-31.31~24.04.1
   90  +linux-image-7.0.0-31-generic	7.0.0-31.31~24.04.1
```

Reader's own check: `grep -c -E '^\+(dkms|gcc|make|plocate|mlocate|clamav)\b' minimal.manifest minimal.standard.manifest` → `0` and `0` — none of these packages is in either installable layer.

- **Reader's own extraction (directory listings from the image's squashfs metadata; not a passage, an extraction).** `minimal.squashfs`:

`sources/S4-03/sq_minimal_listing.txt` lines 1–63:
```
    1  comp 4 inodes 123729 bytes 2238519720 meta bytes 2408400
    2  == /etc/systemd/system/timers.target.wants 
    3     anacron.timer -> ('link', '/usr/lib/systemd/system/anacron.timer')
    4     apport-autoreport.timer -> ('link', '/usr/lib/systemd/system/apport-autoreport.timer')
    5     apt-daily-upgrade.timer -> ('link', '/usr/lib/systemd/system/apt-daily-upgrade.timer')
    6     apt-daily.timer -> ('link', '/usr/lib/systemd/system/apt-daily.timer')
    7     dpkg-db-backup.timer -> ('link', '/lib/systemd/system/dpkg-db-backup.timer')
    8     e2scrub_all.timer -> ('link', '/lib/systemd/system/e2scrub_all.timer')
    9     fstrim.timer -> ('link', '/lib/systemd/system/fstrim.timer')
   10     fwupd-refresh.timer -> ('link', '/usr/lib/systemd/system/fwupd-refresh.timer')
   11     logrotate.timer -> ('link', '/usr/lib/systemd/system/logrotate.timer')
   12     man-db.timer -> ('link', '/usr/lib/systemd/system/man-db.timer')
   13     motd-news.timer -> ('link', '/lib/systemd/system/motd-news.timer')
   14     snapd.snap-repair.timer -> ('link', '/usr/lib/systemd/system/snapd.snap-repair.timer')
   15     ua-timer.timer -> ('link', '/usr/lib/systemd/system/ua-timer.timer')
   16     update-notifier-download.timer -> ('link', '/usr/lib/systemd/system/update-notifier-download.timer')
   17     update-notifier-motd.timer -> ('link', '/usr/lib/systemd/system/update-notifier-motd.timer')
   18  == /etc/systemd/user/timers.target.wants 
   19     launchpadlib-cache-clean.timer -> ('link', '/usr/lib/systemd/user/launchpadlib-cache-clean.timer')
   20  == /etc/systemd/system/sysstat.service.wants 
   21     sysstat-collect.timer -> ('link', '/usr/lib/systemd/system/sysstat-collect.timer')
   22     sysstat-summary.timer -> ('link', '/usr/lib/systemd/system/sysstat-summary.timer')
   23  == /etc/cron.d 
   24     .placeholder -> ('file',)
   25     anacron -> ('file',)
   26     e2scrub_all -> ('file',)
   27     sysstat -> ('file',)
   28  == /etc/cron.daily 
   29     .placeholder -> ('file',)
   30     0anacron -> ('file',)
   31     apport -> ('file',)
   32     apt-compat -> ('file',)
   33     dpkg -> ('file',)
   34     logrotate -> ('file',)
   35     man-db -> ('file',)
   36     sysstat -> ('file',)
   37  == /etc/cron.weekly 
   38     .placeholder -> ('file',)
   39     0anacron -> ('file',)
   40     man-db -> ('file',)
   41  == /etc/cron.monthly 
   42     .placeholder -> ('file',)
   43     0anacron -> ('file',)
   44  == /etc/cron.hourly 
   45     .placeholder -> ('file',)
   46  == /etc/kernel/postinst.d 
   47     initramfs-tools -> ('file',)
   48     unattended-upgrades -> ('file',)
   49     update-notifier -> ('link', '/usr/share/update-notifier/notify-reboot-required')
   50     xx-update-initrd-links -> ('file',)
   51  == /etc/systemd/system/multi-user.target.wants 
   52     anacron.service -> ('link', '/usr/lib/systemd/system/anacron.service')
   53     cron.service -> ('link', '/usr/lib/systemd/system/cron.service')
   54     kerneloops.service -> ('link', '/usr/lib/systemd/system/kerneloops.service')
   55     sysstat.service -> ('link', '/usr/lib/systemd/system/sysstat.service')
   56     unattended-upgrades.service -> ('link', '/usr/lib/systemd/system/unattended-upgrades.service')
   57     whoopsie.path -> ('link', '/usr/lib/systemd/system/whoopsie.path')
   58  == /var/lib/apport 
   59     coredump -> ('dir', 1088306, 2850, 3)
   60  == /var/lib/apport/autoreport MISSING
   61  == /var/lib/ubuntu-advantage 
   62  == /var/lib/ubuntu-advantage/private MISSING
   63  == /etc/default/motd-news MISSING
```

`minimal.standard.squashfs` (the extended layer adds no timer, cron file or enabled timer; it adds the Thunderbird snap mount and the Déjà Dup monitor autostart):

`sources/S4-03/sq_standard_listing.txt` lines 1–13:
```
    1  comp 4 inodes 53606 bytes 561095334 meta bytes 901560
    2  == /etc/systemd/system/timers.target.wants MISSING
    3  == /etc/cron.daily MISSING
    4  == /etc/cron.d MISSING
    5  == /etc/systemd/system 
    6     multi-user.target.wants -> ('dir', 0, 2003, 50)
    7     snap-thunderbird-1255.mount -> ('file',)
    8     snapd.mounts.target.wants -> ('dir', 0, 2050, 50)
    9  comp 4 inodes 53606 bytes 561095334 meta bytes 901560
   10  == /etc/systemd/system/multi-user.target.wants 
   11     snap-thunderbird-1255.mount -> ('link', '/etc/systemd/system/snap-thunderbird-1255.mount')
   12  == /etc/xdg/autostart 
   13     org.gnome.DejaDup.Monitor.desktop -> ('file',)
```

Files read out of `minimal.squashfs` (reader's own extraction; verbatim file contents):

`sources/S4-03/extracted/etc__default__sysstat` (matching lines):
```
    9  ENABLED="false"
```
`sources/S4-03/extracted/etc__apt__apt.conf.d__20auto-upgrades` lines 1–2:
```
    1  APT::Periodic::Update-Package-Lists "1";
    2  APT::Periodic::Unattended-Upgrade "1";
```
`sources/S4-03/extracted/etc__apt__apt.conf.d__10periodic` lines 1–3:
```
    1  APT::Periodic::Update-Package-Lists "1";
    2  APT::Periodic::Download-Upgradeable-Packages "0";
    3  APT::Periodic::AutocleanInterval "0";
```
`sources/S4-03/extracted/etc__default__anacron` (matching lines):
```
   16  ANACRON_RUN_ON_BATTERY_POWER=no
   25  ANACRON_ARGS=-s
```
`sources/S4-03/extracted/etc__systemd__user__snap.firmware-updater.firmware-notifier.timer` lines 5–16:
```
    5  
    6  [Timer]
    7  Unit=snap.firmware-updater.firmware-notifier.service
    8  OnCalendar=*-*-* 00:00
    9  OnCalendar=*-*-* 03:00
   10  OnCalendar=*-*-* 06:00
   11  OnCalendar=*-*-* 09:00
   12  OnCalendar=*-*-* 12:00
   13  OnCalendar=*-*-* 15:00
   14  OnCalendar=*-*-* 18:00
   15  OnCalendar=*-*-* 21:00
   16  
```
`sources/S4-03/extracted/etc__systemd__user__snap.firmware-updater.firmware-notifier.service` (matching lines):
```
    8  ExecStart=/usr/bin/snap run --timer="00:00-24:00/8" firmware-updater.firmware-notifier
```

`/etc/default/motd-news`, `/var/lib/apport/autoreport` and `/var/lib/ubuntu-advantage/private` are absent from `minimal.squashfs` (reader's lookups at the end of the listing above returned MISSING).

- **Coverage.** T11 — covers the existence and enablement of systemd timers and cron jobs in the shipped image of the stock Ubuntu 24.04 desktop (both selections): 15 system timers enabled through `timers.target.wants` (`anacron`, `apport-autoreport`, `apt-daily`, `apt-daily-upgrade`, `dpkg-db-backup`, `e2scrub_all`, `fstrim`, `fwupd-refresh`, `logrotate`, `man-db`, `motd-news`, `snapd.snap-repair`, `ua-timer`, `update-notifier-download`, `update-notifier-motd`), two sysstat timers wired into the enabled `sysstat.service`, one user timer enabled globally (`launchpadlib-cache-clean`), one snap user timer present but not in the global `timers.target.wants` (`snap.firmware-updater.firmware-notifier`), cron files in `/etc/cron.d`, `cron.daily`, `cron.weekly`, `cron.monthly`. Also bears on T5 (same facts, existence only). Does not show whether each timer's conditions are met at run time, how long each job runs, or how often it actually fires — that needs a booted system (Appendix B). Not an observation: a shipped image read without booting it. Subject named: Ubuntu 24.04.5.1 desktop amd64 image, both install selections; window: image built 2026-09-14.

### S4-04 — Ubuntu noble Contents indexes and the reader's intersection with the desktop layers

- **Citation.** Ubuntu archive, `http://archive.ubuntu.com/ubuntu/dists/noble/Contents-amd64.gz` (`Last-Modified: Wed, 24 Apr 2024 02:07:41 GMT`) and `dists/noble-updates/Contents-amd64.gz` (`Last-Modified: Fri, 25 Sep 2026 22:09:01 GMT`), accessed 2026-10-01.
- **Copy read.** `sources/S4-04/`.

| file (under `sources/S4-04/`) | bytes | SHA-256 |
|---|---:|---|
| `noble-Contents-amd64.gz` | 51301092 | `c8718dbbacd1ab72675513cf0674ff9921fcf781d9f49c4c0eaf68a49c18adc1` |
| `noble-updates-Contents-amd64.gz` | 75084451 | `5cc306984bc08ad02dc15d7dc7f8a8fcb83958eb900aa33f9b6d7810924bce9e` |
| `reader-intersection-desktop-units.txt` | 7584 | `f8fe3bef48c4466cf9066b682a9c22a2918d9a4349470402dfc59fd351713d3a` |

- **Reader's own computation.** Every Contents line whose path matches `^(usr/lib|lib)/systemd/(system|user)/[^/ ]+\.timer\s`, `^etc/cron\.(d|daily|weekly|monthly|hourly)/` or `^etc/xdg/autostart/` (765 lines), joined with the package names added by `minimal.manifest` and `minimal.standard.manifest` (S4-03). Command: `gzcat <Contents> | grep -E '<the three patterns>' > units_raw.txt`, then a Python join on package name (result saved as `reader-intersection-desktop-units.txt`). Result (timer and cron rows only; the 38 autostart rows are in the saved file):

`sources/S4-04/reader-intersection-desktop-units.txt` (matching lines):
```
    1  etc/cron.d/.placeholder [('cron-daemon-common', 'minimal', '3.0pl1-184ubuntu2')]
    2  etc/cron.d/anacron [('anacron', 'minimal', '2.3-39ubuntu2')]
    3  etc/cron.d/e2scrub_all [('e2fsprogs', 'minimal', '1.47.0-2.4~exp1ubuntu4.1')]
    4  etc/cron.d/sysstat [('sysstat', 'minimal', '12.6.1-2')]
    5  etc/cron.daily/.placeholder [('cron-daemon-common', 'minimal', '3.0pl1-184ubuntu2')]
    6  etc/cron.daily/0anacron [('anacron', 'minimal', '2.3-39ubuntu2')]
    7  etc/cron.daily/apport [('apport', 'minimal', '2.28.3-0ubuntu0.1')]
    8  etc/cron.daily/apt-compat [('apt', 'minimal', '2.8.3')]
    9  etc/cron.daily/dpkg [('dpkg', 'minimal', '1.22.6ubuntu6.6')]
   10  etc/cron.daily/logrotate [('logrotate', 'minimal', '3.21.0-2build1')]
   11  etc/cron.daily/man-db [('man-db', 'minimal', '2.12.0-4build2')]
   12  etc/cron.daily/sysstat [('sysstat', 'minimal', '12.6.1-2')]
   13  etc/cron.hourly/.placeholder [('cron-daemon-common', 'minimal', '3.0pl1-184ubuntu2')]
   14  etc/cron.monthly/.placeholder [('cron-daemon-common', 'minimal', '3.0pl1-184ubuntu2')]
   15  etc/cron.monthly/0anacron [('anacron', 'minimal', '2.3-39ubuntu2')]
   16  etc/cron.weekly/.placeholder [('cron-daemon-common', 'minimal', '3.0pl1-184ubuntu2')]
   17  etc/cron.weekly/0anacron [('anacron', 'minimal', '2.3-39ubuntu2')]
   18  etc/cron.weekly/man-db [('man-db', 'minimal', '2.12.0-4build2')]
   57  lib/systemd/system/apport-autoreport.timer [('apport', 'minimal', '2.28.3-0ubuntu0.1')]
   58  lib/systemd/system/snapd.snap-repair.timer [('snapd', 'minimal', '2.76.3+ubuntu24.04')]
   59  lib/systemd/system/ua-timer.timer [('ubuntu-pro-client', 'minimal', '37.2ubuntu~24.04.1')]
   60  lib/systemd/system/update-notifier-download.timer [('update-notifier-common', 'minimal', '3.192.68.2')]
   61  lib/systemd/system/update-notifier-motd.timer [('update-notifier-common', 'minimal', '3.192.68.2')]
   62  usr/lib/systemd/system/anacron.timer [('anacron', 'minimal', '2.3-39ubuntu2')]
   63  usr/lib/systemd/system/apport-autoreport.timer [('apport', 'minimal', '2.28.3-0ubuntu0.1')]
   64  usr/lib/systemd/system/apt-daily-upgrade.timer [('apt', 'minimal', '2.8.3')]
   65  usr/lib/systemd/system/apt-daily.timer [('apt', 'minimal', '2.8.3')]
   66  usr/lib/systemd/system/dpkg-db-backup.timer [('dpkg', 'minimal', '1.22.6ubuntu6.6')]
   67  usr/lib/systemd/system/e2scrub_all.timer [('e2fsprogs', 'minimal', '1.47.0-2.4~exp1ubuntu4.1')]
   68  usr/lib/systemd/system/fstrim.timer [('util-linux', 'minimal', '2.39.3-9ubuntu6.6')]
   69  usr/lib/systemd/system/fwupd-refresh.timer [('fwupd', 'minimal', '2.0.20-1ubuntu2~24.04.2')]
   70  usr/lib/systemd/system/logrotate.timer [('logrotate', 'minimal', '3.21.0-2build1')]
   71  usr/lib/systemd/system/man-db.timer [('man-db', 'minimal', '2.12.0-4build2')]
   72  usr/lib/systemd/system/motd-news.timer [('base-files', 'minimal', '13ubuntu10.5')]
   73  usr/lib/systemd/system/snapd.snap-repair.timer [('snapd', 'minimal', '2.76.3+ubuntu24.04')]
   74  usr/lib/systemd/system/sysstat-collect.timer [('sysstat', 'minimal', '12.6.1-2')]
   75  usr/lib/systemd/system/sysstat-summary.timer [('sysstat', 'minimal', '12.6.1-2')]
   76  usr/lib/systemd/system/systemd-sysupdate-reboot.timer [('systemd', 'minimal', '255.4-1ubuntu8.17')]
   77  usr/lib/systemd/system/systemd-sysupdate.timer [('systemd', 'minimal', '255.4-1ubuntu8.17')]
   78  usr/lib/systemd/system/systemd-tmpfiles-clean.timer [('systemd', 'minimal', '255.4-1ubuntu8.17')]
   79  usr/lib/systemd/user/launchpadlib-cache-clean.timer [('python3-launchpadlib', 'minimal', '1.11.0-6')]
   80  usr/lib/systemd/user/systemd-tmpfiles-clean.timer [('systemd', 'minimal', '255.4-1ubuntu8.17')]
```

- **Passages (index lines).**

`sources/S4-04/noble-updates-Contents-amd64.gz` (matching lines):
```
  372  boot/config-6.17.0-1022-azure				    kernel/linux-modules-6.17.0-1022-azure
482300  lib/modules/6.17.0-1022-azure/kernel/drivers/gpu/drm/vkms/vkms.ko.zst kernel/linux-modules-extra-6.17.0-1022-azure
482995  lib/modules/6.17.0-1022-azure/kernel/drivers/media/v4l2-core/videodev.ko.zst kernel/linux-modules-extra-6.17.0-1022-azure
485927  lib/modules/6.17.0-1022-azure/kernel/v4l2loopback/v4l2loopback.ko.zst kernel/linux-modules-6.17.0-1022-azure
485930  lib/modules/6.17.0-1022-azure/kernel/zfs/zfs.ko.zst	    kernel/linux-modules-6.17.0-1022-azure
2682232  usr/lib/x86_64-linux-gnu/dri/swrast_dri.so		    libs/libgl1-mesa-dri
2688528  usr/lib/x86_64-linux-gnu/libvulkan_lvp.so		    libs/mesa-vulkan-drivers
```

- **Coverage.** T11 — covers which desktop packages ship timer, cron and autostart files (a superset of what the image enables; S4-03 gives the enabled set), and that the runner's own kernel package set (`6.17.0-1022-azure`) already ships prebuilt `v4l2loopback.ko` and `zfs.ko` and a `vkms.ko` virtual KMS driver; and that Mesa's software OpenGL (`swrast_dri.so`, package `libgl1-mesa-dri`) and software Vulkan (`libvulkan_lvp.so`, package `mesa-vulkan-drivers`) are packaged. Not an observation.

### S4-05 — The desktop packages at the manifest versions: timer and service units, cron scripts, maintainer scripts

- **Citation.** Ubuntu binary packages, fetched from the Launchpad librarian (`https://launchpad.net/ubuntu/+archive/primary/+files/…`) or the archive pool at exactly the versions in `minimal.manifest` / `minimal.standard.manifest` (S4-03), accessed 2026-10-01. Unpacked with `ar x` + `zstd -dc | tar -x`.
- **Copy read.** `sources/S4-05/` (the `.deb` files; quotations below are from files inside them, shown as `<deb>!/<path>`; maintainer scripts as `!/DEBIAN/<script>`).

| file (under `sources/S4-05/`) | bytes | SHA-256 |
|---|---:|---|
| `anacron_2.3-39ubuntu2_amd64.deb` | 28310 | `2b4142e8a0a451f4d3922dfcc8f5d04f9bc4d301bc5ef86c0321a151fd06d2c2` |
| `apport_2.28.3-0ubuntu0.1_all.deb` | 85276 | `3fb6842df77c2a60373981d2a00e25c11b3793f4301e115bcb9dd3e3b69e8847` |
| `apt_2.8.3_amd64.deb` | 1375526 | `c9ace99efc7726fe0035f921a9acf262a9723bbf35b861aab4f9075a0be67442` |
| `base-files_13ubuntu10.5_amd64.deb` | 73220 | `87e8c41e62f61625fb78a982d0bc0a70f40ef8375bc313b154914d1b3759c823` |
| `cron-daemon-common_3.0pl1-184ubuntu2_all.deb` | 13578 | `289604310fb1e92b9dae924161f94194533af1fccef3b156f970e5365848ff34` |
| `cron_3.0pl1-184ubuntu2_amd64.deb` | 85350 | `5a257b6b3b05d290964f68868db8127cca7eeef64c30dc9586f46cd4f68f1b90` |
| `deja-dup_45.2-1build2_amd64.deb` | 337862 | `092007f597967e564b326550845ed814a06aa254cd31cc9e198a91da2e14b4e8` |
| `dpkg_1.22.6ubuntu6.6_amd64.deb` | 1282284 | `ceb6aa4da59fbcb8a3b0549b4280c60b7d849b519859797c8668bdfbe378fb3b` |
| `e2fsprogs_1.47.0-2.4~exp1ubuntu4.1_amd64.deb` | 600736 | `1d0fb19dcf14316d04602260871dba3c1441c0ecf3c3bde54eacba35dcc5a40b` |
| `fwupd_2.0.20-1ubuntu2~24.04.2_amd64.deb` | 6135970 | `0e04b5c0081114c080e4a3618e12e73a311f33bf061c8e53c151459a6149fcea` |
| `logrotate_3.21.0-2build1_amd64.deb` | 52212 | `e609ad80a9cec135b404a84f99d9d87bc304800eb212702444a985527edba70c` |
| `man-db_2.12.0-4build2_amd64.deb` | 1236636 | `d7ce31173a73bd3a93b7216a837a2e8641fff3fd7ae2dfc0ca705dbabe03e92b` |
| `python3-launchpadlib_1.11.0-6_all.deb` | 126540 | `5c6eacd5deae0da0839a614e7c80ec371a0b5d1482af96ca952ff71a33804979` |
| `snapd_2.76.3+ubuntu24.04_amd64.deb` | 36576380 | `9ffe7430c7769234e58c9b83a5fe6e33c7ca963976133e4a0ede4c29dcd0fa82` |
| `sysstat_12.6.1-2_amd64.deb` | 489308 | `40f8a528434e2816f78869b7aa71a9ff4057678e76ae3a4109b5a7a72caa1285` |
| `systemd_255.4-1ubuntu8.17_amd64.deb` | 3475000 | `250345b73e42a97ee71cae7c1e470897dfad3c639eb0a7aafe4f9a3a29871cb2` |
| `ubuntu-pro-client_37.2ubuntu~24.04.1_amd64.deb` | 259672 | `c148f08254e2a961d473fb742660afd4041fc5a6e8907509640e0aaa20f11f75` |
| `unattended-upgrades_2.9.1+nmu4ubuntu1_all.deb` | 51198 | `13c576c7d8184f509d5ddc4d75bec6e62ef3f745319cce60f8131f401091113b` |
| `update-notifier-common_3.192.68.2_all.deb` | 206730 | `50c3303b52aaaaadcf11750e1a0afc905bdee0d6f75aa2f1febdd4416afe7fec` |
| `util-linux_2.39.3-9ubuntu6.6_amd64.deb` | 1128326 | `08eb17ba3b83378ed1e73d8335d0ce03b429c0bbeb07e374f536234edab02465` |

- **Passages — system timers and what they run.**

`anacron_2.3-39ubuntu2_amd64.deb!/usr/lib/systemd/system/anacron.timer` (matching lines):
```
    5  OnCalendar=*-*-* 07..23:30
    6  RandomizedDelaySec=5m
    7  Persistent=true
   10  WantedBy=timers.target
```
`anacron_2.3-39ubuntu2_amd64.deb!/usr/lib/systemd/system/anacron.service` (matching lines):
```
   12  ConditionACPower=true
   16  EnvironmentFile=/etc/default/anacron
   17  ExecStart=/usr/sbin/anacron -d -q $ANACRON_ARGS
```
`anacron_2.3-39ubuntu2_amd64.deb!/etc/anacrontab` (matching lines):
```
   10  1	5	cron.daily	run-parts --report /etc/cron.daily
   11  7	10	cron.weekly	run-parts --report /etc/cron.weekly
   12  @monthly	15	cron.monthly	run-parts --report /etc/cron.monthly
```
`apt_2.8.3_amd64.deb!/usr/lib/systemd/system/apt-daily.timer` (matching lines):
```
    5  OnCalendar=*-*-* 6,18:00
    6  RandomizedDelaySec=12h
    7  Persistent=true
   10  WantedBy=timers.target
```
`apt_2.8.3_amd64.deb!/usr/lib/systemd/system/apt-daily.service` (matching lines):
```
    4  ConditionACPower=true
    9  ExecStartPre=-/usr/lib/apt/apt-helper wait-online
   10  ExecStart=/usr/lib/apt/apt.systemd.daily update
```
`apt_2.8.3_amd64.deb!/usr/lib/systemd/system/apt-daily-upgrade.timer` (matching lines):
```
    6  OnCalendar=*-*-* 6:00
    7  RandomizedDelaySec=60m
    8  Persistent=true
   11  WantedBy=timers.target
```
`apt_2.8.3_amd64.deb!/usr/lib/systemd/system/apt-daily-upgrade.service` (matching lines):
```
    4  ConditionACPower=true
   10  ExecStart=/usr/lib/apt/apt.systemd.daily install
```
`apport_2.28.3-0ubuntu0.1_all.deb!/usr/lib/systemd/system/apport-autoreport.timer` (matching lines):
```
    3  ConditionPathExists=/var/lib/apport/autoreport
    6  OnStartupSec=1h
    7  OnUnitActiveSec=3h
   10  WantedBy=timers.target
```
`apport_2.28.3-0ubuntu0.1_all.deb!/usr/lib/systemd/system/apport-autoreport.service` (matching lines):
```
    3  ConditionPathExists=/var/lib/apport/autoreport
    9  ExecStart=/usr/share/apport/whoopsie-upload-all --timeout 20
```
`base-files_13ubuntu10.5_amd64.deb!/usr/lib/systemd/system/motd-news.timer` (matching lines):
```
    5  OnCalendar=00,12:00:00
    6  RandomizedDelaySec=12h
    7  Persistent=true
    8  OnStartupSec=1min
   11  WantedBy=timers.target
```
`base-files_13ubuntu10.5_amd64.deb!/usr/lib/systemd/system/motd-news.service` (matching lines):
```
    8  ExecStart=/etc/update-motd.d/50-motd-news --force
```
`base-files_13ubuntu10.5_amd64.deb!/etc/update-motd.d/50-motd-news` lines 33–37:
```
   33  [ -r /etc/default/motd-news ] && . /etc/default/motd-news
   34  
   35  # Exit immediately, unless we're enabled
   36  # This makes this script very easy to disable in /etc/default/motd-news configuration
   37  [ "$ENABLED" = "1" ] || exit 0
```
`dpkg_1.22.6ubuntu6.6_amd64.deb!/usr/lib/systemd/system/dpkg-db-backup.timer` (matching lines):
```
    6  OnCalendar=daily
    7  Persistent=true
   10  WantedBy=timers.target
```
`dpkg_1.22.6ubuntu6.6_amd64.deb!/usr/lib/systemd/system/dpkg-db-backup.service` (matching lines):
```
    7  ExecStart=/usr/libexec/dpkg/dpkg-db-backup
```
`e2fsprogs_1.47.0-2.4~exp1ubuntu4.1_amd64.deb!/usr/lib/systemd/system/e2scrub_all.timer` (matching lines):
```
    6  OnCalendar=Sun *-*-* 03:10:00
    7  RandomizedDelaySec=60
    8  Persistent=true
   11  WantedBy=timers.target
```
`e2fsprogs_1.47.0-2.4~exp1ubuntu4.1_amd64.deb!/usr/lib/systemd/system/e2scrub_all.service` (matching lines):
```
    3  ConditionACPower=true
    4  ConditionCapability=CAP_SYS_ADMIN
    5  ConditionCapability=CAP_SYS_RAWIO
   11  ExecStart=/sbin/e2scrub_all
```
`util-linux_2.39.3-9ubuntu6.6_amd64.deb!/usr/lib/systemd/system/fstrim.timer` (matching lines):
```
    4  ConditionVirtualization=!container
    5  ConditionPathExists=!/etc/initrd-release
    8  OnCalendar=weekly
   10  Persistent=true
   11  RandomizedDelaySec=100min
   14  WantedBy=timers.target
```
`util-linux_2.39.3-9ubuntu6.6_amd64.deb!/usr/lib/systemd/system/fstrim.service` (matching lines):
```
    8  ExecStart=/sbin/fstrim --listed-in /etc/fstab:/proc/self/mountinfo --verbose --quiet-unsupported
```
`fwupd_2.0.20-1ubuntu2~24.04.2_amd64.deb!/usr/lib/systemd/system/fwupd-refresh.timer` (matching lines):
```
    3  ConditionVirtualization=!container
    6  OnCalendar=*-*-* *:00:00
    7  RandomizedDelaySec=1h
    8  Persistent=true
   11  WantedBy=timers.target
```
`fwupd_2.0.20-1ubuntu2~24.04.2_amd64.deb!/usr/lib/systemd/system/fwupd-refresh.service` (matching lines):
```
   13  User=fwupd-refresh
   25  ExecStart=/usr/bin/fwupdmgr refresh
```
`logrotate_3.21.0-2build1_amd64.deb!/usr/lib/systemd/system/logrotate.timer` (matching lines):
```
    6  OnCalendar=daily
    7  AccuracySec=1h
    8  Persistent=true
   11  WantedBy=timers.target
```
`logrotate_3.21.0-2build1_amd64.deb!/usr/lib/systemd/system/logrotate.service` (matching lines):
```
    5  ConditionACPower=true
    9  ExecStart=/usr/sbin/logrotate /etc/logrotate.conf
   12  Nice=19
   13  IOSchedulingClass=best-effort
```
`man-db_2.12.0-4build2_amd64.deb!/usr/lib/systemd/system/man-db.timer` (matching lines):
```
    6  OnCalendar=daily
    7  RandomizedDelaySec=12h
    8  Persistent=true
   11  WantedBy=timers.target
```
`man-db_2.12.0-4build2_amd64.deb!/usr/lib/systemd/system/man-db.service` (matching lines):
```
    4  ConditionACPower=true
    9  ExecStart=+/usr/bin/install -d -o man -g man -m 0755 /var/cache/man
   11  ExecStart=/usr/bin/mandb --quiet
   12  User=man
   13  Nice=19
   14  IOSchedulingClass=idle
```
`snapd_2.76.3+ubuntu24.04_amd64.deb!/usr/lib/systemd/system/snapd.snap-repair.timer` (matching lines):
```
    4  ConditionKernelCommandLine=|snap_core
    5  ConditionKernelCommandLine=|snapd_recovery_mode
    8  OnCalendar=*-*-* 5,11,17,23:00
    9  RandomizedDelaySec=2h
   12  OnStartupSec=15m
   15  WantedBy=timers.target
```
`snapd_2.76.3+ubuntu24.04_amd64.deb!/usr/lib/systemd/system/snapd.snap-repair.service` (matching lines):
```
   10  ExecStart=/usr/lib/snapd/snap-repair run
```
`ubuntu-pro-client_37.2ubuntu~24.04.1_amd64.deb!/lib/systemd/system/ua-timer.timer` (matching lines):
```
    6  ConditionPathExists=/var/lib/ubuntu-advantage/private/machine-token.json
    9  OnUnitActiveSec=6h
   10  RandomizedDelaySec=1h
   11  OnStartupSec=1min
   14  WantedBy=timers.target
```
`ubuntu-pro-client_37.2ubuntu~24.04.1_amd64.deb!/lib/systemd/system/ua-timer.service` (matching lines):
```
   14  ExecStart=/usr/bin/python3 /usr/lib/ubuntu-advantage/timer.py
```
`update-notifier-common_3.192.68.2_all.deb!/lib/systemd/system/update-notifier-download.timer` (matching lines):
```
    6  OnStartupSec=5m
    7  OnUnitActiveSec=24h
   10  WantedBy=timers.target
```
`update-notifier-common_3.192.68.2_all.deb!/lib/systemd/system/update-notifier-download.service` (matching lines):
```
    3  ConditionFileIsExecutable=/usr/lib/update-notifier/package-data-downloader
    6  ExecStart=/usr/lib/update-notifier/package-data-downloader
```
`update-notifier-common_3.192.68.2_all.deb!/lib/systemd/system/update-notifier-motd.timer` (matching lines):
```
    6  OnCalendar=Sun *-*-* 06:00:00
    7  RandomizedDelaySec=1w
    8  Persistent=true
   11  WantedBy=timers.target
```
`update-notifier-common_3.192.68.2_all.deb!/lib/systemd/system/update-notifier-motd.service` (matching lines):
```
    3  ConditionFileIsExecutable=/usr/lib/ubuntu-release-upgrader/release-upgrade-motd
    6  ExecStart=/usr/lib/ubuntu-release-upgrader/release-upgrade-motd
```
`systemd_255.4-1ubuntu8.17_amd64.deb!/usr/lib/systemd/system/systemd-tmpfiles-clean.timer` (matching lines):
```
   16  OnBootSec=15min
   17  OnUnitActiveSec=1d
```
`systemd_255.4-1ubuntu8.17_amd64.deb!/usr/lib/systemd/system/systemd-tmpfiles-clean.service` (matching lines):
```
   21  ExecStart=systemd-tmpfiles --clean
   23  IOSchedulingClass=idle
```
`systemd_255.4-1ubuntu8.17_amd64.deb!/usr/lib/systemd/system/systemd-sysupdate.timer` (matching lines):
```
   16  ConditionVirtualization=!container
   23  OnBootSec=15min
   24  OnUnitActiveSec=2h
   25  OnCalendar=Sat
   30  WantedBy=timers.target
```
`sysstat_12.6.1-2_amd64.deb!/usr/lib/systemd/system/sysstat-collect.timer` (matching lines):
```
   11  OnCalendar=*:00/10
   14  WantedBy=sysstat.service
```
`sysstat_12.6.1-2_amd64.deb!/usr/lib/systemd/system/sysstat-collect.service` (matching lines):
```
   16  ExecStart=/usr/lib/sysstat/sa1 1 1
```
`sysstat_12.6.1-2_amd64.deb!/usr/lib/systemd/system/sysstat-summary.timer` (matching lines):
```
   12  OnCalendar=00:07:00
   15  WantedBy=sysstat.service
```
`sysstat_12.6.1-2_amd64.deb!/usr/lib/systemd/system/sysstat-summary.service` (matching lines):
```
   15  ExecStart=/usr/lib/sysstat/sa2 -A
```
`sysstat_12.6.1-2_amd64.deb!/usr/lib/systemd/system/sysstat.service` (matching lines):
```
   16  ExecStart=/usr/lib/sysstat/sa1 --boot
   19  WantedBy=multi-user.target
   20  Also=sysstat-collect.timer
   21  Also=sysstat-summary.timer
```

- **Passages — user timers.**

`python3-launchpadlib_1.11.0-6_all.deb!/usr/lib/systemd/user/launchpadlib-cache-clean.timer` (matching lines):
```
    5  OnStartupSec=5min
    6  OnUnitActiveSec=1d
    9  WantedBy=timers.target
```
`python3-launchpadlib_1.11.0-6_all.deb!/usr/lib/systemd/user/launchpadlib-cache-clean.service` (matching lines):
```
    3  ConditionPathExists=%h/.launchpadlib/api.launchpad.net/cache
    7  ExecStart=find %h/.launchpadlib/api.launchpad.net/cache -type f -mtime +30 -delete
```
`systemd_255.4-1ubuntu8.17_amd64.deb!/usr/lib/systemd/user/systemd-tmpfiles-clean.timer` (matching lines):
```
   15  OnStartupSec=5min
   16  OnUnitActiveSec=1d
   19  WantedBy=timers.target
```

- **Passages — cron.**

`cron-daemon-common_3.0pl1-184ubuntu2_all.deb!/etc/crontab` lines 19–22:
```
   19  17 *	* * *	root	cd / && run-parts --report /etc/cron.hourly
   20  25 6	* * *	root	test -x /usr/sbin/anacron || { cd / && run-parts --report /etc/cron.daily; }
   21  47 6	* * 7	root	test -x /usr/sbin/anacron || { cd / && run-parts --report /etc/cron.weekly; }
   22  52 6	1 * *	root	test -x /usr/sbin/anacron || { cd / && run-parts --report /etc/cron.monthly; }
```
`anacron_2.3-39ubuntu2_amd64.deb!/etc/cron.d/anacron` (matching lines):
```
    5  30 7-23 * * *   root	[ -x /etc/init.d/anacron ] && if [ ! -d /run/systemd/system ]; then /usr/sbin/invoke-rc.d anacron start >/dev/null; fi
```
`e2fsprogs_1.47.0-2.4~exp1ubuntu4.1_amd64.deb!/etc/cron.d/e2scrub_all` lines 1–2:
```
    1  30 3 * * 0 root test -e /run/systemd/system || SERVICE_MODE=1 /usr/lib/x86_64-linux-gnu/e2fsprogs/e2scrub_all_cron
    2  10 3 * * * root test -e /run/systemd/system || SERVICE_MODE=1 /sbin/e2scrub_all -A -r
```
`sysstat_12.6.1-2_amd64.deb!/etc/cron.d/sysstat` (matching lines):
```
    1  # The first element of the path is a directory where the debian-sa1
    6  5-55/10 * * * * root command -v debian-sa1 > /dev/null && debian-sa1 1 1
    9  59 23 * * * root command -v debian-sa1 > /dev/null && debian-sa1 60 2
```
`apport_2.28.3-0ubuntu0.1_all.deb!/etc/cron.daily/apport` lines 3–5:
```
    3  [ -d /var/crash ] || exit 0
    4  find /var/crash/. ! -name . -prune -type f \( \( -size 0 -a \! -name '*.upload*' -a \! -name '*.drkonqi*' \) -o -mtime +7 \) -exec rm -f -- '{}' \;
    5  find /var/crash/. ! -name . -prune -type d -regextype posix-extended -regex '.*/[0-9]{12}$' \( -mtime +7 \) -exec rm -Rf -- '{}' \;
```
`apt_2.8.3_amd64.deb!/etc/cron.daily/apt-compat` lines 10–12:
```
   10  if [ -d /run/systemd/system ]; then
   11      exit 0
   12  fi
```
`dpkg_1.22.6ubuntu6.6_amd64.deb!/etc/cron.daily/dpkg` lines 4–8:
```
    4  if [ -d /run/systemd/system ]; then
    5    exit 0
    6  fi
    7  
    8  /usr/libexec/dpkg/dpkg-db-backup
```
`logrotate_3.21.0-2build1_amd64.deb!/etc/cron.daily/logrotate` lines 4–6:
```
    4  if [ -d /run/systemd/system ]; then
    5      exit 0
    6  fi
```
`man-db_2.12.0-4build2_amd64.deb!/etc/cron.daily/man-db` lines 7–10:
```
    7  if [ -d /run/systemd/system ]; then
    8      # Skip in favour of systemd timer.
    9      exit 0
   10  fi
```
`man-db_2.12.0-4build2_amd64.deb!/etc/cron.weekly/man-db` lines 7–10:
```
    7  if [ -d /run/systemd/system ]; then
    8      # Skip in favour of systemd timer.
    9      exit 0
   10  fi
```
`sysstat_12.6.1-2_amd64.deb!/etc/cron.daily/sysstat` (matching lines):
```
   10  ENABLED=false
   13  [ ! -d /run/systemd/system ] || exit 0
   20  [ "$ENABLED" = "true" ]  || exit 0
```

- **Passages — enablement logic and the sysstat switch.**

`logrotate_3.21.0-2build1_amd64.deb!/DEBIAN/postinst` lines 3–18:
```
    3  # Automatically added by dh_installsystemd/13.14.1ubuntu5
    4  if [ "$1" = "configure" ] || [ "$1" = "abort-upgrade" ] || [ "$1" = "abort-deconfigure" ] || [ "$1" = "abort-remove" ] ; then
    5  	# The following line should be removed in trixie or trixie+1
    6  	deb-systemd-helper unmask 'logrotate.timer' >/dev/null || true
    7  
    8  	# was-enabled defaults to true, so new installations run enable.
    9  	if deb-systemd-helper --quiet was-enabled 'logrotate.timer'; then
   10  		# Enables the unit on first installation, creates new
   11  		# symlinks on upgrades if the unit file has changed.
   12  		deb-systemd-helper enable 'logrotate.timer' >/dev/null || true
   13  	else
   14  		# Update the statefile to add new symlinks (if any), which need to be
   15  		# cleaned up on purge. Also remove old symlinks.
   16  		deb-systemd-helper update-state 'logrotate.timer' >/dev/null || true
   17  	fi
   18  fi
```
`sysstat_12.6.1-2_amd64.deb!/DEBIAN/postinst` lines 47–57:
```
   47  manage_systemd_services()
   48  {
   49      ENABLED="$1"
   50      all_services='sysstat-collect.timer sysstat-summary.timer sysstat.service'
   51      num_all_services=3
   52  
   53      # deb-systemd-helper does not have the --now option
   54      sysctl='/bin/systemctl'
   55      num_disabled=0
   56  
   57      [ -x "$sysctl" ] && [ -d /run/systemd/system ] || return 0
```
`sysstat_12.6.1-2_amd64.deb!/DEBIAN/postinst` lines 101–106:
```
  101      db_reset sysstat/remove_files || true
  102  
  103      db_get sysstat/enable || true
  104      ENABLED="$RET"
  105  
  106      manage_default_file "$ENABLED"
```
`sysstat_12.6.1-2_amd64.deb!/usr/lib/sysstat/sa1` lines 14–19:
```
   14  SYSCONFIG_DIR=/etc/sysstat
   15  SYSCONFIG_FILE=sysstat
   16  UMASK=0022
   17  LONG_NAME=n
   18  
   19  [ -r ${SYSCONFIG_DIR}/${SYSCONFIG_FILE} ] && . ${SYSCONFIG_DIR}/${SYSCONFIG_FILE}
```

Reader's own check: `grep -c -E 'ENABLED|default/sysstat' sysstat_12.6.1-2_amd64.deb!/usr/lib/sysstat/sa1` → `0`: the collector that `sysstat-collect.service` runs does not read the `ENABLED` switch of `/etc/default/sysstat`; it reads `/etc/sysstat/sysstat`.

- **Passages — Déjà Dup (extended selection only).**

`deja-dup_45.2-1build2_amd64.deb!/usr/share/glib-2.0/schemas/org.gnome.DejaDup.gschema.xml` lines 48–57:
```
   48      <key name="periodic" type="b">
   49        <default>false</default>
   50        <summary>Whether to periodically back up</summary>
   51        <description>Whether to automatically back up on a regular schedule.</description>
   52      </key>
   53      <key name="periodic-period" type="i">
   54        <default>7</default>
   55        <summary>How often to periodically back up</summary>
   56        <description>The number of days between backups.</description>
   57      </key>
```
`deja-dup_45.2-1build2_amd64.deb!/usr/share/glib-2.0/schemas/org.gnome.DejaDup.gschema.xml` lines 98–99:
```
   98      <key name="tool" type="s">
   99        <default>'duplicity'</default>
```
`deja-dup_45.2-1build2_amd64.deb!/etc/xdg/autostart/org.gnome.DejaDup.Monitor.desktop` (matching lines):
```
   11  Exec=/usr/libexec/deja-dup/deja-dup-monitor
   13  X-GNOME-Autostart-Delay=120
```

- **Coverage.** T11 — covers what each scheduled job on the stock desktop runs and when it is scheduled to fire (schedules as written in the units; existence only). Reader's reading of the passages together with S4-03, labelled as such: on a running systemd the cron.daily scripts of `apt`, `dpkg`, `logrotate`, `man-db` and `sysstat` exit at once (`/run/systemd/system` test), so the effective cron work is anacron's run of `cron.daily/apport` (crash-file cleanup) plus the empty hourly/weekly/monthly parts; `apport-autoreport` and `ua-timer` are gated by `ConditionPathExists=` on paths the image does not contain (`/var/lib/apport/autoreport`; `/var/lib/ubuntu-advantage/private/…`, S4-03) and `snapd.snap-repair` by `snap_core` / `snapd_recovery_mode` on the kernel command line — whether any of them fires on a running desktop is a runtime check; `motd-news.service` exits immediately because `/etc/default/motd-news` is absent; `sysstat.service` is enabled and pulls in the two sysstat timers even though `/etc/default/sysstat` says `ENABLED="false"` (the postinst's own systemd handling returns early when `/run/systemd/system` does not exist, as in an image build chroot), and `sa1` does not read that switch — so the image is wired to run `sadc` every 10 minutes; this is an inference from files, to be settled on a booted system (Appendix B, check 4). `systemd-sysupdate.timer` is shipped but not enabled (not in `timers.target.wants`). Déjà Dup's periodic backup defaults to off (`periodic` = `false`). Also bears on T5 (existence only). Not an observation.

### S4-06 — Ubuntu noble Packages indexes: what is packaged, in which component, at which version (reader's extraction)

- **Citation.** Ubuntu archive `dists/{noble,noble-updates}/{main,restricted,universe,multiverse}/binary-amd64/Packages.xz`, accessed 2026-10-01 (noble-updates indexes dated 2026-09-25 by the Contents index of the same pocket).
- **Copy read.** `sources/S4-06/`.

| file (under `sources/S4-06/`) | bytes | SHA-256 |
|---|---:|---|
| `noble-main-Packages.xz` | 1401160 | `2a6a199e1031a5c279cb346646d594993f35b1c03dd4a82aaa0323980dd92451` |
| `noble-multiverse-Packages.xz` | 269224 | `8080460fe0864ab72bfc2a6d52e76d8c82d55f2cc2188a12f83d6fbe3e1750ea` |
| `noble-restricted-Packages.xz` | 93924 | `aa3f9520f4e46cdcd610c7f0ce9450cda430f20085b028845e95122e9d61680c` |
| `noble-universe-Packages.xz` | 15037908 | `ba9057fa1b91438cc8a1d26808d00c85389fe101d0c1496254df97236405599a` |
| `noble-updates-main-Packages.xz` | 1341696 | `1f8e5657e0d7ea2b701acfcef0b6ea270b0f6a205a841bb719b3d321300878c5` |
| `noble-updates-multiverse-Packages.xz` | 45692 | `57d8a516d9904dbd57931601d952837841cadb8805811cb1174029637ac129e7` |
| `noble-updates-restricted-Packages.xz` | 1697020 | `9722122311a84b3d1ec0f79a5bda1ea0130ca69f16884f02f115082ced3c25b4` |
| `noble-updates-universe-Packages.xz` | 1699404 | `05fbd38a074570b65a932043204bc43baec6e08cd96ef611d015afbcc0ecaac1` |
| `pkgq.py` | 956 | `f36be7d13a528548da3a69d3f61066113c2c57258eb9c27ca663f46805a9bbba` |
| `selected-packages.txt` | 7396 | `6bed71560e7b2448b6632389b417c6a0c901693c5999b4b087c82f14b568650d` |

- **Reader's own extraction.** `python3 pkgq.py Version,Section <names…>` prints, for each package name, every (pocket/component) stanza in the eight indexes with its `Version` and `Section` fields, or `NOT IN noble/noble-updates`. Output (verbatim field values):

`sources/S4-06/selected-packages.txt` lines 1–101:
```
    1  libreoffice-writer | noble/main | Version=4:24.2.2-0ubuntu1 | Section=editors
    2  libreoffice-writer | noble-updates/main | Version=4:24.2.7-0ubuntu0.24.04.6 | Section=editors
    3  evince | noble/main | Version=46.0-1build1 | Section=gnome
    4  evince | noble-updates/main | Version=46.3.1-0ubuntu1.1 | Section=gnome
    5  chromium-browser | noble/universe | Version=2:1snap1-0ubuntu2 | Section=universe/web
    6  firefox | noble/main | Version=1:1snap1-0ubuntu5 | Section=web
    7  thunderbird | noble/main | Version=2:1snap1-0ubuntu3 | Section=mail
    8  gimp | noble/universe | Version=2.10.36-3build3 | Section=universe/graphics
    9  gimp | noble-updates/universe | Version=2.10.36-3ubuntu0.24.04.1 | Section=universe/graphics
   10  darktable | noble/universe | Version=4.6.1-2ubuntu1 | Section=universe/graphics
   11  kdenlive | noble/universe | Version=4:23.08.5-0ubuntu4 | Section=universe/graphics
   12  melt | noble/universe | Version=7.22.0-1build6 | Section=universe/utils
   13  blender | noble/universe | Version=4.0.2+dfsg-1ubuntu8 | Section=universe/graphics
   14  mpv | noble/universe | Version=0.37.0-1ubuntu4 | Section=universe/video
   15  vlc | noble/universe | Version=3.0.20-3build6 | Section=universe/graphics
   16  steam-installer | noble/multiverse | Version=1:1.0.0.79~ds-2 | Section=multiverse/games
   17  steam-devices | noble/multiverse | Version=1:1.0.0.79~ds-2 | Section=multiverse/games
   18  wine | noble/universe | Version=9.0~repack-4build3 | Section=universe/otherosfs
   19  wine64 | noble/universe | Version=9.0~repack-4build3 | Section=universe/otherosfs
   20  tracker-miner-fs | noble/main | Version=3.7.1-1build1 | Section=utils
   21  tracker-miner-fs | noble-updates/main | Version=3.7.1-1ubuntu0.1 | Section=utils
   22  baloo-kf5 | noble/universe | Version=5.115.0-0ubuntu5 | Section=universe/utils
   23  plocate | noble/universe | Version=1.1.19-2ubuntu2 | Section=universe/utils
   24  clamav | noble/main | Version=1.0.5+dfsg-1.1ubuntu3 | Section=utils
   25  clamav | noble-updates/main | Version=1.5.4+dfsg-0ubuntu0.24.04.1 | Section=utils
   26  clamav-daemon | noble/main | Version=1.0.5+dfsg-1.1ubuntu3 | Section=utils
   27  clamav-daemon | noble-updates/main | Version=1.5.4+dfsg-0ubuntu0.24.04.1 | Section=utils
   28  clamav-freshclam | noble/main | Version=1.0.5+dfsg-1.1ubuntu3 | Section=utils
   29  clamav-freshclam | noble-updates/main | Version=1.5.4+dfsg-0ubuntu0.24.04.1 | Section=utils
   30  borgbackup | noble/universe | Version=1.2.8-1 | Section=universe/admin
   31  restic | noble/universe | Version=0.16.4-2 | Section=universe/misc
   32  restic | noble-updates/universe | Version=0.16.4-2ubuntu0.24.04.3 | Section=universe/misc
   33  duplicity | noble/main | Version=2.1.4-3ubuntu2 | Section=utils
   34  deja-dup | noble/main | Version=45.2-1build2 | Section=utils
   35  rsync | noble/main | Version=3.2.7-1ubuntu1 | Section=net
   36  rsync | noble-updates/main | Version=3.2.7-1ubuntu1.5 | Section=net
   37  rclone | noble/universe | Version=1.60.1+dfsg-3 | Section=universe/net
   38  rclone | noble-updates/universe | Version=1.60.1+dfsg-3ubuntu0.24.04.6 | Section=universe/net
   39  7zip | noble/universe | Version=23.01+dfsg-11 | Section=universe/utils
   40  p7zip-full | noble/universe | Version=16.02+transitional.1 | Section=universe/utils
   41  tar | noble/main | Version=1.35+dfsg-3build1 | Section=utils
   42  tar | noble-updates/main | Version=1.35+dfsg-3ubuntu0.4 | Section=utils
   43  xz-utils | noble/main | Version=5.6.1+really5.4.5-1 | Section=utils
   44  xz-utils | noble-updates/main | Version=5.6.1+really5.4.5-1ubuntu0.3 | Section=utils
   45  handbrake-cli | noble/universe | Version=1.7.2+ds1-1build2 | Section=universe/graphics
   46  ffmpeg | noble/universe | Version=7:6.1.1-3ubuntu5 | Section=universe/video
   47  python3 | noble/main | Version=3.12.3-0ubuntu1 | Section=python
   48  python3 | noble-updates/main | Version=3.12.3-0ubuntu2.1 | Section=python
   49  make | noble/main | Version=4.3-4.1build2 | Section=devel
   50  gcc | noble/main | Version=4:13.2.0-7ubuntu1 | Section=devel
   51  dkms | noble/main | Version=3.0.11-1ubuntu13 | Section=admin
   52  v4l2loopback-dkms | noble/universe | Version=0.12.7-2ubuntu5 | Section=universe/graphics
   53  v4l2loopback-dkms | noble-updates/universe | Version=0.12.7-2ubuntu5.2 | Section=universe/graphics
   54  virtualbox-dkms | noble/multiverse | Version=7.0.16-dfsg-2 | Section=multiverse/kernel
   55  virtualbox-dkms | noble-updates/multiverse | Version=7.0.16-dfsg-2ubuntu1.3 | Section=multiverse/kernel
   56  zfs-dkms | noble/universe | Version=2.2.2-0ubuntu9 | Section=universe/kernel
   57  zfs-dkms | noble-updates/universe | Version=2.2.2-0ubuntu9.5 | Section=universe/kernel
   58  nvidia-dkms-580 | noble-updates/restricted | Version=580.178.04-0ubuntu0.24.04.1 | Section=restricted/libs
   59  gnome-shell | noble/main | Version=46.0-0ubuntu5 | Section=gnome
   60  gnome-shell | noble-updates/main | Version=46.0-0ubuntu6~24.04.15 | Section=gnome
   61  xserver-xorg-core | noble/main | Version=2:21.1.12-1ubuntu1 | Section=x11
   62  xserver-xorg-core | noble-updates/main | Version=2:21.1.12-1ubuntu1.8 | Section=x11
   63  xwayland | noble/main | Version=2:23.2.6-1 | Section=x11
   64  xwayland | noble-updates/main | Version=2:23.2.6-1ubuntu0.8 | Section=x11
   65  xvfb | noble/universe | Version=2:21.1.12-1ubuntu1 | Section=universe/x11
   66  xvfb | noble-updates/universe | Version=2:21.1.12-1ubuntu1.8 | Section=universe/x11
   67  pipewire | noble/main | Version=1.0.5-1 | Section=libs
   68  pipewire | noble-updates/main | Version=1.0.5-1ubuntu3.3 | Section=libs
   69  pipewire-bin | noble/main | Version=1.0.5-1 | Section=video
   70  pipewire-bin | noble-updates/main | Version=1.0.5-1ubuntu3.3 | Section=video
   71  systemd | noble/main | Version=255.4-1ubuntu8 | Section=admin
   72  systemd | noble-updates/main | Version=255.4-1ubuntu8.17 | Section=admin
   73  dbus-daemon | noble/main | Version=1.14.10-4ubuntu4 | Section=admin
   74  dbus-daemon | noble-updates/main | Version=1.14.10-4ubuntu4.1 | Section=admin
   75  dbus-broker | noble/universe | Version=35-2 | Section=universe/admin
   76  dbus-broker | noble-updates/universe | Version=35-2ubuntu0.1 | Section=universe/admin
   77  mesa-vulkan-drivers | noble/main | Version=24.0.5-1ubuntu1 | Section=libs
   78  mesa-vulkan-drivers | noble-updates/main | Version=25.2.8-0ubuntu0.24.04.3 | Section=libs
   79  libgl1-mesa-dri | noble/main | Version=24.0.5-1ubuntu1 | Section=libs
   80  libgl1-mesa-dri | noble-updates/main | Version=25.2.8-0ubuntu0.24.04.3 | Section=libs
   81  linux-headers-6.17.0-1022-azure | noble-updates/main | Version=6.17.0-1022.22 | Section=devel
   82  linux-tools-6.17.0-1022-azure | noble-updates/main | Version=6.17.0-1022.22 | Section=devel
   83  linux-modules-extra-6.17.0-1022-azure | noble-updates/main | Version=6.17.0-1022.22 | Section=kernel
   84  linux-headers-6.8.0-146-generic | noble-updates/main | Version=6.8.0-146.146 | Section=devel
   85  linux-azure | noble/main | Version=6.8.0-1007.7 | Section=metapackages
   86  linux-azure | noble-updates/main | Version=7.0.0-1014.14~24.04.1 | Section=metapackages
   87  systemd-container | noble/main | Version=255.4-1ubuntu8 | Section=admin
   88  systemd-container | noble-updates/main | Version=255.4-1ubuntu8.17 | Section=admin
   89  qemu-system-x86 | noble/main | Version=1:8.2.2+ds-0ubuntu1 | Section=misc
   90  qemu-system-x86 | noble-updates/main | Version=1:8.2.2+ds-0ubuntu1.18 | Section=misc
   91  code: NOT IN noble/noble-updates
   92  google-chrome-stable: NOT IN noble/noble-updates
   93  spotify-client: NOT IN noble/noble-updates
   94  zoom: NOT IN noble/noble-updates
   95  teams: NOT IN noble/noble-updates
   96  slack-desktop: NOT IN noble/noble-updates
   97  discord: NOT IN noble/noble-updates
   98  element-desktop: NOT IN noble/noble-updates
   99  gamescope: NOT IN noble/noble-updates
  100  localsearch: NOT IN noble/noble-updates
  101  matrix-synapse: NOT IN noble/noble-updates
```

- **Coverage.** T11 — covers the Ubuntu-archive install route for the T8 programs and the instruments: in `main` or `universe`/`multiverse`, or absent (VS Code, Google Chrome, Spotify, Zoom, Teams, Slack, Discord, Element, gamescope, LocalSearch, matrix-synapse are not in the noble archive; Firefox, Thunderbird and Chromium are transitional debs to snaps; `steam-installer` is in multiverse); the runner kernel's headers and tools (`linux-headers-6.17.0-1022-azure`, `linux-tools-6.17.0-1022-azure`) are installable from `noble-updates/main`; DKMS module packages exist for v4l2loopback, VirtualBox, ZFS and NVIDIA 580. Also bears on T8 (packaging existence). Not an observation. Window: archive state of 2026-09-25/10-01.

### S4-07 — DKMS 3.0.11-1ubuntu13, v4l2loopback-dkms 0.12.7-2ubuntu5.2, the VirtualBox / ZFS / NVIDIA changelogs, coreutils `nproc`

- **Citation.** Ubuntu packages `dkms_3.0.11-1ubuntu13_all.deb` (noble/main) and `v4l2loopback-dkms_0.12.7-2ubuntu5.2_all.deb` (noble-updates/universe); Ubuntu changelogs for `virtualbox 7.0.16-dfsg-2ubuntu1.3`, `zfs-linux 2.2.2-0ubuntu9.5`, `nvidia-graphics-drivers-580 580.178.04-0ubuntu0.24.04.1` from `changelogs.ubuntu.com`; GNU coreutils manual, "nproc invocation", `https://www.gnu.org/software/coreutils/manual/html_node/nproc-invocation.html`; all accessed 2026-10-01.
- **Copy read.** `sources/S4-07/`.

| file (under `sources/S4-07/`) | bytes | SHA-256 |
|---|---:|---|
| `coreutils-nproc-invocation.html` | 4764 | `178da32dcd8e2278e8d30aa25ac10f90498748fe6008f9f5533d7ca671ffbda4` |
| `dkms_3.0.11-1ubuntu13_all.deb` | 51542 | `18d098c65e3002040afc11f80656e84377551a5d1bdcd3933cdf6ae2e58dcd75` |
| `nvidia-580_580.178.04-0ubuntu0.24.04.1.changelog` | 4287 | `7728aefc3fa35834e2782c68de864529f784eb9748ec52d545ebf372762cff40` |
| `v4l2loopback-dkms_0.12.7-2ubuntu5.2_all.deb` | 31044 | `236d2d8fbe8e2eac6b7ef76a5470e1b5a98205a925083575b6c4ab7d285a25e6` |
| `virtualbox_7.0.16-dfsg-2ubuntu1.3.changelog` | 140151 | `26fde3a3851be143487c5d13baba8b96d924a1b4fb7c57be45a867da26eb6787` |
| `zfs-linux_2.2.2-0ubuntu9.5.changelog` | 55636 | `47964c4b58626d1c25e908e044aa6c214fcefebaffa39951d60c18bc404d78e0` |

- **Passages.**

`dkms_3.0.11-1ubuntu13_all.deb!/etc/kernel/postinst.d/dkms` lines 37–39:
```
   37  if [ -x /usr/lib/dkms/dkms_autoinstaller ]; then
   38      exec /usr/lib/dkms/dkms_autoinstaller start "$inst_kern"
   39  fi
```
`dkms_3.0.11-1ubuntu13_all.deb!/etc/kernel/header_postinst.d/dkms` lines 37–39:
```
   37  if [ -x /usr/lib/dkms/dkms_autoinstaller ]; then
   38      exec /usr/lib/dkms/dkms_autoinstaller start "$inst_kern"
   39  fi
```
`dkms_3.0.11-1ubuntu13_all.deb!/usr/lib/dkms/dkms_autoinstaller` lines 69–75:
```
   69  		if [ -f /etc/dkms/no-autoinstall ]; then
   70  			log_action_msg "$prog: autoinstall for dkms modules has been disabled"
   71  		elif ! _check_kernel_dir $kernel; then
   72  			log_action_msg "$prog: autoinstall for kernel $kernel was skipped since the kernel headers for this kernel do not seem to be installed"
   73  		else
   74  			log_action_msg "$prog: running auto installation service for kernel $kernel"
   75  			dkms autoinstall --kernelver $kernel
```
`dkms_3.0.11-1ubuntu13_all.deb!/usr/sbin/dkms` lines 178–188:
```
  178  # Find out how many CPUs there are so that we may pass an appropriate -j
  179  # option to make. Ignore hyperthreading for now.
  180  get_num_cpus()
  181  {
  182      # use nproc(1) from coreutils 8.1-1+ if available, otherwise single job
  183      if [ -x /usr/bin/nproc ]; then
  184          nproc
  185      else
  186          echo "1"
  187      fi
  188  }
```
`dkms_3.0.11-1ubuntu13_all.deb!/usr/sbin/dkms` lines 1113–1113:
```
 1113      local the_make_command="${make_command/#make/make -j$parallel_jobs KERNELRELEASE=$kernelver}"
```
`dkms_3.0.11-1ubuntu13_all.deb!/usr/sbin/dkms` lines 2593–2594:
```
 2593  # Default to -j<number of CPUs>
 2594  parallel_jobs=${parallel_jobs:-$(get_num_cpus)}
```
`sources/S4-07/coreutils-nproc-invocation.html` (matching lines):
```
   57  <p>Print the number of processing units available to the current process,
```
`v4l2loopback-dkms_0.12.7-2ubuntu5.2_all.deb!/usr/src/v4l2loopback-0.12.7/dkms.conf` lines 1–25:
```
    1  PACKAGE_NAME="v4l2loopback"
    2  PACKAGE_VERSION="0.12.7"
    3  
    4  if [ -f $kernel_source_dir/.config ]; then
    5      . $kernel_source_dir/.config
    6      if ! { echo "$kernelver"; echo 5.18; } | sort -V -C; then
    7          # for linux>=5.18, CONFIG_VIDEO_V4L2 has been renamed to CONFIG_VIDEO_DEV
    8          if [ "${CONFIG_VIDEO_DEV:-n}" = "n" ]; then
    9              BUILD_EXCLUSIVE_KERNEL="REQUIRES CONFIG_VIDEO_DEV"
   10          fi
   11      else
   12          if [ "${CONFIG_VIDEO_V4L2:-n}" = "n" ]; then
   13              BUILD_EXCLUSIVE_KERNEL="REQUIRES CONFIG_VIDEO_V4L2"
   14          fi
   15      fi
   16  fi
   17  
   18  # Items below here should not have to change with each driver version
   19  MAKE[0]="make KERNEL_DIR=${kernel_source_dir} all"
   20  CLEAN="make clean"
   21  
   22  BUILT_MODULE_NAME[0]="$PACKAGE_NAME"
   23  DEST_MODULE_LOCATION[0]="/extra"
   24  
   25  AUTOINSTALL="yes"
```
`v4l2loopback-dkms_0.12.7-2ubuntu5.2_all.deb!/usr/share/doc/v4l2loopback-dkms/changelog.Debian.gz` lines 1–21:
```
    1  v4l2loopback (0.12.7-2ubuntu5.2) noble; urgency=medium
    2  
    3    * Fix FTBFS and oops against linux-6.18 (LP: #2161037)
    4      - d/p/lp2161037-0-fix-ftbfs-linux-6.18.patch: add filp argument to
    5        v4l2_fh_add(), with compat macro for linux<6.18
    6      - d/p/lp2161037-1-fix-v4l2-fh-del-linux-6.18.patch: do the same for
    7        v4l2_fh_del()
    8      - d/p/lp2161037-2-use-file-accessor.patch: find the opener via
    9        file_to_v4l2_fh() on linux>=6.18, which no longer allows
   10        container_of() on the fh argument
   11    * Fix outbufs_list corruption under concurrent output DQBUF (LP: #2161239).
   12      - d/p/lp2161239-lock-outbufs-list-in-dqbuf.patch: serialize output
   13        DQBUF list rotation.
   14  
   15   -- Seyeong Kim <seyeong.kim@canonical.com>  Wed, 29 Jul 2026 07:08:29 +0000
   16  
   17  v4l2loopback (0.12.7-2ubuntu5.1) noble; urgency=medium
   18  
   19    * Failed to build against linux-6.16 (LP: #2114259)
   20      - added functionality for linux 6.15+ (#626)
   21      - only use `timer_delete_sync` compat macro for linux<6.2.0
```
`sources/S4-07/virtualbox_7.0.16-dfsg-2ubuntu1.3.changelog` lines 1–3:
```
    1  virtualbox (7.0.16-dfsg-2ubuntu1.3) noble; urgency=medium
    2  
    3    * Further patches for Linux 6.17 kernel support (LP: #2136499) 
```
`sources/S4-07/virtualbox_7.0.16-dfsg-2ubuntu1.3.changelog` lines 20–22:
```
   20  virtualbox (7.0.16-dfsg-2ubuntu1.2) noble; urgency=medium
   21  
   22    * Linux 6.17 kernel support (LP: #2136499)
```
`sources/S4-07/zfs-linux_2.2.2-0ubuntu9.5.changelog` (matching lines):
```
   53      - Linux 6.7 support (LP: #2077487)
   60      - Linux 6.8 support(LP: #2058179)
  132      - Linux 6.6 support(LP: #2042565)
```
`sources/S4-07/nvidia-580_580.178.04-0ubuntu0.24.04.1.changelog` lines 1–3:
```
    1  nvidia-graphics-drivers-580 (580.178.04-0ubuntu0.24.04.1) noble; urgency=medium
    2  
    3    * New upstream version 580.178.04 (LP: #2163128)
```

- **Coverage.** T11 — covers how a DKMS autoinstall is triggered (installing a `linux-headers-<ver>` package runs `/etc/kernel/header_postinst.d`; installing a kernel image runs `/etc/kernel/postinst.d`; both exec `dkms_autoinstaller start <ver>`, which runs `dkms autoinstall --kernelver <ver>` if that kernel's headers are present), the build command (`make -j$parallel_jobs`, `parallel_jobs` defaulting to `nproc`, which counts the CPUs available to the calling process — so an autoinstall started under a one-CPU `taskset` would build with `-j1`), that v4l2loopback refuses to build without `CONFIG_VIDEO_DEV` and carries fixes for Linux 6.16 and 6.18, that VirtualBox's DKMS package carries Linux 6.17 support patches, and that the ZFS DKMS package's changelog lists support up to Linux 6.8. Also bears on T5 (DKMS mechanics; existence only). Does not give object counts or durations. Not an observation.

### S4-08 — The runner's kernel: linux-azure 6.17.0-1022 headers (`.config`, `postinst`, Kconfig)

- **Citation.** Ubuntu packages `linux-headers-6.17.0-1022-azure_6.17.0-1022.22_amd64.deb` and `linux-azure-6.17-headers-6.17.0-1022_6.17.0-1022.22_all.deb` (noble-updates/main), accessed 2026-10-01. `config-6.17.0-1022-azure` is the package's `/usr/src/linux-headers-6.17.0-1022-azure/.config`; `kconfig/` holds `security/Kconfig`, `security/lockdown/Kconfig` and `security/apparmor/Kconfig` from the second package.
- **Copy read.** `sources/S4-08/`.

| file (under `sources/S4-08/`) | bytes | SHA-256 |
|---|---:|---|
| `config-6.17.0-1022-azure` | 206837 | `b684cdecf90ab6fb67f49c2b63ee95738810ee5c92476fa6f801815f75051ab5` |
| `linux-azure-6.17-headers-6.17.0-1022_6.17.0-1022.22_all.deb` | 14442750 | `76af6797e536169fde8782545bb043cbbb011708c7fc6fec51799c6aff22c3a7` |
| `linux-headers-6.17.0-1022-azure_6.17.0-1022.22_amd64.deb` | 3515486 | `7e800c3af8998d33df25cad0b26c789f5e0b583fb1f84090f83e1fd5099e4d5a` |
| `kconfig/security_Kconfig` | 10773 | `4cd534b23db4d5967697a1e67e08a647a0e81a8da3109da256a80f4411903c20` |
| `kconfig/security_apparmor_Kconfig` | 4923 | `cd3554630edb031cf12ca3a54c0fe647c29a9cbfeaaf291bfa2e9da52d4f780e` |
| `kconfig/security_lockdown_Kconfig` | 2027 | `4ba1823fd661243a0f90cacf9ce08a65f230d6b9c804cbb0fb369a8c34764dda` |

- **Passages.**

`sources/S4-08/config-6.17.0-1022-azure` (matching lines):
```
  107  CONFIG_NO_HZ_FULL=y
  135  CONFIG_PREEMPT_VOLUNTARY=y
  151  CONFIG_TASKSTATS=y
  152  CONFIG_TASK_DELAY_ACCT=y
  153  CONFIG_TASK_XACCT=y
  154  CONFIG_TASK_IO_ACCOUNTING=y
  238  CONFIG_USER_NS=y
  306  CONFIG_PERF_EVENTS=y
  313  CONFIG_TRACEPOINTS=y
  505  CONFIG_HZ_1000=y
  506  CONFIG_HZ=1000
 1034  CONFIG_MODULE_SIG=y
 1035  # CONFIG_MODULE_SIG_FORCE is not set
 3708  CONFIG_INPUT_UINPUT=y
 5052  CONFIG_MEDIA_SUPPORT=m
 5068  CONFIG_VIDEO_DEV=m
 5399  CONFIG_DRM=y
 5570  # CONFIG_DRM_VGEM is not set
 5571  CONFIG_DRM_VKMS=m
 5771  # CONFIG_SOUND is not set
 7195  CONFIG_FUSE_FS=y
 7512  CONFIG_SECURITY_PERF_EVENTS_RESTRICT=y
 7550  # CONFIG_SECURITY_APPARMOR_RESTRICT_USERNS is not set
 7556  CONFIG_LOCK_DOWN_IN_SECURE_BOOT=y
 7557  CONFIG_LOCK_DOWN_KERNEL_FORCE_NONE=y
 8311  CONFIG_SCHED_INFO=y
 8312  CONFIG_SCHEDSTATS=y
 8394  CONFIG_EVENT_TRACING=y
 8399  CONFIG_FTRACE=y
```
`linux-headers-6.17.0-1022-azure.deb!/DEBIAN/postinst` lines 10–13:
```
   10  if [ -d /etc/kernel/header_postinst.d ]; then
   11      DEB_MAINT_PARAMS="$*" run-parts --report --exit-on-error --arg=$version \
   12  		/etc/kernel/header_postinst.d
   13  fi
```
`sources/S4-08/kconfig/security_lockdown_Kconfig` lines 19–30:
```
   19  config LOCK_DOWN_IN_SECURE_BOOT
   20  	bool "Lock down the kernel in Secure Boot mode"
   21  	default n
   22  	depends on (EFI || S390 || PPC) && SECURITY_LOCKDOWN_LSM_EARLY
   23  	help
   24  	  Secure Boot provides a mechanism for ensuring that the firmware will
   25  	  only load signed bootloaders and kernels.  Secure boot mode
   26  	  determination is platform-specific; examples include EFI secure boot
   27  	  and SIPL on s390.
   28  
   29  	  Enabling this option results in kernel lockdown being triggered if
   30  	  booted under secure boot.
```
`sources/S4-08/kconfig/security_apparmor_Kconfig` lines 107–117:
```
  107  config SECURITY_APPARMOR_RESTRICT_USERNS
  108  	bool "Restrict user namespace creation to confined domains"
  109  	depends on SECURITY_APPARMOR && USER_NS
  110  	default y
  111  	help
  112  	  This options allows controlling whether apparmor restricts
  113  	  the creation of new user namespaces to confined tasks by
  114  	  default. If set unconfined tasks without CAP_SYS_ADMIN
  115  	  will not be allowed to create new user namespaces. Confined
  116  	  tasks ability to create new user namespaces will be controlled
  117  	  by their profile.
```
`sources/S4-08/kconfig/security_Kconfig` lines 75–82:
```
   75  config SECURITY_PERF_EVENTS_RESTRICT
   76  	bool "Restrict unprivileged use of performance events"
   77  	depends on PERF_EVENTS
   78  	help
   79  	  If you say Y here, the kernel.perf_event_paranoid sysctl
   80  	  will be set to 3 by default, and no unprivileged use of the
   81  	  perf_event_open syscall will be permitted unless it is
   82  	  changed.
```

- **Coverage.** T11 — covers the instruments' kernel prerequisites on the runner kernel (taskstats, delay accounting, schedstats, perf events and tracepoints compiled in; perf events closed to unprivileged users by default (`kernel.perf_event_paranoid` set to 3); HZ 1000; voluntary preemption), that the runner kernel has **no sound support** (`CONFIG_SOUND` not set — no ALSA devices, so no `snd-aloop` loopback), has V4L2 as a module (so v4l2loopback can build), has `vkms` but not `vgem`, that module signatures are checked but not forced unless the kernel is locked down, and that lockdown is triggered when booted under Secure Boot. The AppArmor user-namespace restriction is **not** a compile-time default in this kernel. Not an observation.

### S4-09 — Linux v6.17 documentation and source; systemd v255 resource-control

- **Citation.** torvalds/linux at tag `v6.17`: `tools/perf/Documentation/perf-sched.txt`, `tools/perf/Documentation/perf-record.txt`, `Documentation/accounting/delay-accounting.rst`, `Documentation/admin-guide/sysctl/kernel.rst`, `Documentation/admin-guide/sysctl/vm.rst`, `include/linux/sched.h`, `kernel/module/signing.c`; systemd/systemd at tag `v255`: `man/systemd.resource-control.xml`; via `raw.githubusercontent.com`, accessed 2026-10-01.
- **Copy read.** `sources/S4-09/`.

| file (under `sources/S4-09/`) | bytes | SHA-256 |
|---|---:|---|
| `systemd-v255-systemd.resource-control.xml` | 96926 | `5666a4f337073cc42482775831f44e07a6a0ca31f7f4db5ba98925e943ecde80` |
| `v6.17__Documentation_accounting_delay-accounting.rst` | 8472 | `f7733c138f9b096ba1c79551502a4fd65fcd1e392089784424a8a69221f7f6de` |
| `v6.17__Documentation_admin-guide_sysctl_kernel.rst` | 57679 | `c18e37e1b32344d7600bca19b72f5d40af855cf7889c09890568da6a3d24f337` |
| `v6.17__Documentation_admin-guide_sysctl_vm.rst` | 41001 | `5cf010b57064fcb15c5d154be6f01e0522006a12d09007c0adcc99590689de64` |
| `v6.17__include_linux_sched.h` | 68014 | `d7a2b1e7876e8893308c7d737ba6b2cfa6bf6f77820dc44884caa6cd0855d7ab` |
| `v6.17__kernel_module_signing.c` | 3125 | `b6dac3fb2527b3a2b897bf1279f056479d888be82cbdb612225c49568962e938` |
| `v6.17__tools_perf_Documentation_perf-record.txt` | 34046 | `91ffcc9dc0e5a570f1ed2f4689acb92a2a548da9f8e71248c56145d5878b9081` |
| `v6.17__tools_perf_Documentation_perf-sched.txt` | 7660 | `d2a924734550d42ab8e19bd3a820dfb637795118f810f396a59263aba2ea6b7e` |

- **Passages.**

`sources/S4-09/v6.17__tools_perf_Documentation_perf-sched.txt` lines 17–18:
```
   17    'perf sched record <command>' to record the scheduling events
   18    of an arbitrary workload.
```
`sources/S4-09/v6.17__tools_perf_Documentation_perf-sched.txt` lines 59–63:
```
   59    'perf sched timehist' provides an analysis of scheduling events.
   60      
   61      Example usage:
   62          perf sched record -- sleep 1
   63          perf sched timehist
```
`sources/S4-09/v6.17__tools_perf_Documentation_perf-sched.txt` lines 190–191:
```
  190  --wakeups::
  191  	Show wakeup events.
```
`sources/S4-09/v6.17__tools_perf_Documentation_perf-record.txt` lines 521–526:
```
  521  -k::
  522  --clockid::
  523  Sets the clock id to use for the various time fields in the perf_event_type
  524  records. See clock_gettime(). In particular CLOCK_MONOTONIC and
  525  CLOCK_MONOTONIC_RAW are supported, some events might also allow
  526  CLOCK_BOOTTIME, CLOCK_REALTIME and CLOCK_TAI.
```
`sources/S4-09/v6.17__Documentation_accounting_delay-accounting.rst` lines 77–85:
```
   77  Delay accounting is disabled by default at boot up.
   78  To enable, add::
   79  
   80     delayacct
   81  
   82  to the kernel boot options. The rest of the instructions below assume this has
   83  been done. Alternatively, use sysctl kernel.task_delayacct to switch the state
   84  at runtime. Note however that only tasks started after enabling it will have
   85  delayacct information.
```
`sources/S4-09/v6.17__Documentation_admin-guide_sysctl_kernel.rst` lines 1243–1249:
```
 1243  task_delayacct
 1244  ===============
 1245  
 1246  Enables/disables task delay accounting (see
 1247  Documentation/accounting/delay-accounting.rst. Enabling this feature incurs
 1248  a small amount of overhead in the scheduler but is useful for debugging
 1249  and performance tuning. It is required by some tools such as iotop.
```
`sources/S4-09/v6.17__Documentation_admin-guide_sysctl_vm.rst` lines 245–255:
```
  245  drop_caches
  246  ===========
  247  
  248  Writing to this will cause the kernel to drop clean caches, as well as
  249  reclaimable slab objects like dentries and inodes.  Once dropped, their
  250  memory becomes free.
  251  
  252  To free pagecache::
  253  
  254  	echo 1 > /proc/sys/vm/drop_caches
  255  
```
`sources/S4-09/v6.17__include_linux_sched.h` lines 320–320:
```
  320  	TASK_COMM_LEN = 16,
```
`sources/S4-09/v6.17__kernel_module_signing.c` lines 99–124:
```
   99  	switch (err) {
  100  	case -ENODATA:
  101  		reason = "unsigned module";
  102  		break;
  103  	case -ENOPKG:
  104  		reason = "module with unsupported crypto";
  105  		break;
  106  	case -ENOKEY:
  107  		reason = "module with unavailable key";
  108  		break;
  109  
  110  	default:
  111  		/*
  112  		 * All other errors are fatal, including lack of memory,
  113  		 * unparseable signatures, and signature check failures --
  114  		 * even if signatures aren't required.
  115  		 */
  116  		return err;
  117  	}
  118  
  119  	if (is_module_sig_enforced()) {
  120  		pr_notice("Loading of %s is rejected\n", reason);
  121  		return -EKEYREJECTED;
  122  	}
  123  
  124  	return security_locked_down(LOCKDOWN_MODULE_SIGNATURE);
```
`sources/S4-09/systemd-v255-systemd.resource-control.xml` lines 295–306:
```
  295          <term><varname>AllowedCPUs=</varname></term>
  296          <term><varname>StartupAllowedCPUs=</varname></term>
  297  
  298          <listitem>
  299            <para>This setting controls the <option>cpuset</option> controller in the unified hierarchy.</para>
  300  
  301            <para>Restrict processes to be executed on specific CPUs. Takes a list of CPU indices or ranges separated by either
  302            whitespace or commas. CPU ranges are specified by the lower and upper CPU indices separated by a dash.</para>
  303  
  304            <para>Setting <varname>AllowedCPUs=</varname> or <varname>StartupAllowedCPUs=</varname> doesn't guarantee that all
  305            of the CPUs will be used by the processes as it may be limited by parent units. The effective configuration is
  306            reported as <varname>EffectiveCPUs=</varname>.</para>
```

- **Coverage.** T11 — covers the instruments named in T11 as documented: `perf sched record` / `timehist` with `--wakeups`; `perf record -k CLOCK_MONOTONIC`; delay accounting off at boot, switchable at run time with `kernel.task_delayacct`, and only for tasks started after it is switched on; `drop_caches` for cold-cache launches; the 16-byte `comm` (15 characters + NUL); an unsigned module is refused when the kernel is locked down; systemd's `AllowedCPUs=` to fence other services off the load CPU. Not an observation.

### S4-10 — Steam: support FAQ "Managing Steam Downloads & Updates"; Valve Developer Community "SteamCMD"

- **Citation.** Valve, Steam Support FAQ `71AB-698D-57EB-178C`, "Managing Steam Downloads & Updates" (FAQ JSON fields: version 4, timestamp 1727216103 = 2024-09-24 UTC), `https://help.steampowered.com/en/faqs/view/71AB-698D-57EB-178C`, accessed 2026-10-01; Valve Developer Community, "SteamCMD", Wayback Machine snapshot `20260101130455` of `https://developer.valvesoftware.com/wiki/SteamCMD`, accessed 2026-10-01.
- **Copy read.** `sources/S4-10/` (`steam-faq-71AB-content.txt` is the FAQ's `content` field decoded from the page's `data-faqstore` JSON; `vdc-SteamCMD-20260101.text.txt` is the text of the gzip HTML with tags stripped).

| file (under `sources/S4-10/`) | bytes | SHA-256 |
|---|---:|---|
| `steam-faq-71AB-698D-57EB-178C.html` | 33254 | `a67c57e42d31186e4551b46aea4312516150e0c2de7d312f966b3f5c44a622fe` |
| `steam-faq-71AB-content.txt` | 4873 | `243f0ee32b08b9d3f903e131446ce6dd9330af452ad0bff9effd41a50a960f44` |
| `vdc-SteamCMD-20260101.html.gz` | 20639 | `0fabb58101320f786b1af6dd40eee8c13257538a5af5391c740a9473aa39dcbc` |
| `vdc-SteamCMD-20260101.text.txt` | 23192 | `8a3f719904cc3a70d15e65a8cbf019bff89b8b72e6a4b34dda59f7eb16e36ab4` |

- **Passages.**

`sources/S4-10/steam-faq-71AB-content.txt` lines 1–1:
```
    1  Steam will automatically download updates for your games based on the Steam client's download settings. Downloads can also be manually controlled from the Download Manager within your Steam client.
```
`sources/S4-10/steam-faq-71AB-content.txt` (matching lines):
```
   11  There's also a per-game setting to allow/prevent the downloading of other updates while you're playing.[/section]    [section id=disable]  [h4]Disabling automatic updates[/h4]If you'd like to stop Steam from automatically updating a game, select "Only update this game when I launch it" from the game's Library page > Properties > Updates.[/section]    [section id=scheduling]  [h4]Scheduling automatic updates[/h4]Your queued downloads can be manually re-ordered from your Download Manager.
   13  You can also limit the times during the day when Steam updates your games. From your downloads settings ([i]Steam > Settings > Downloads[/i]) check the [i]Only auto-update games[/i] box and specify the time when Steam should perform auto-updates. For example, selecting '12AM' And '8AM' would mean that Steam will only download auto-updated games between midnight and 8 AM your local time.
```
`sources/S4-10/vdc-SteamCMD-20260101.text.txt` lines 150–153:
```
  150  Anonymous
  151  To download most game servers, you can login anonymously using login anonymous
  152  With a Steam Account
  153  Some servers require you to login with a Steam Account.
```
`sources/S4-10/vdc-SteamCMD-20260101.text.txt` lines 158–158:
```
  158  If Steam Guard is activated on the user account, check your e-mail for a Steam Guard access code and enter it. This is only required the first time you log in (as well as when you delete the files where SteamCMD stores the login information).
```
`sources/S4-10/vdc-SteamCMD-20260101.text.txt` (matching lines):
```
   54  9.1 ERROR! Failed to install app "xxxxxx" (No subscription)
  313  ERROR! Failed to install app "xxxxxx" (No subscription)
  314  If you get the "No subscription" error, the game/server you are trying to download either requires a login or that you have purchased the game. You will therefore have to log in with a Steam username and password. If that doesn't help, you may need to purchase a copy of the game on Steam first. See Dedicated Servers List.
```

- **Coverage.** T11 — covers that the Steam client downloads updates per the client's download settings, that a per-game setting allows or prevents downloads while playing, that SteamCMD can log in anonymously for most game servers, that other content needs a Steam account, and that an account with Steam Guard needs an e-mailed code on first login and whenever SteamCMD's stored login files are deleted (an ephemeral runner starts without them). Does **not** state the default of the during-gameplay setting, nor what the Steam client can do without logging in. Also bears on T4 (existence of the setting). Not an observation.

### S4-11 — Proton, umu-launcher, Proton builds, gamescope

- **Citation.** ValveSoftware/Proton `README.md` at `5b89db940e0ebe3a137a6009a3589232fe084c09`; Open-Wine-Components/umu-launcher `README.md`, `umu/umu_runtime.py`, `umu/umu_consts.py`, `umu/umu_proton.py` at `e2b203a1fdd2af9f35166f5713cb3f85d72587e2`; GitHub REST `releases/latest` of umu-launcher (1.4.4, 2026-07-25), umu-proton (UMU-Proton-10.0-4, 2026-03-30), GloriousEggroll/proton-ge-custom (GE-Proton11-7, 2026-09-16) and ValveSoftware/Proton (proton-11.0-2, 2026-08-21); ValveSoftware/gamescope `README.md` at `0e590c755e79c23607378495d10ceb4308b01a59`; accessed 2026-10-01.
- **Copy read.** `sources/S4-11/`.

| file (under `sources/S4-11/`) | bytes | SHA-256 |
|---|---:|---|
| `GloriousEggroll_proton-ge-custom-releases-latest.json` | 42787 | `9136bb3c97299ce5ca9f72f17b8847bc6484d5557781807aa3cfb4b2e1743576` |
| `Open-Wine-Components_umu-launcher-releases-latest.json` | 31520 | `7f5a42d5c92e4abec8934b22d0e323efffc09bce26af3aa304f5c1a31dde9b52` |
| `Open-Wine-Components_umu-proton-releases-latest.json` | 5401 | `0544dc9d54838845850908f027d215aa52703bc095c17b568d50291dd34cac2d` |
| `Proton-README.md` | 16877 | `658deba79398c78d292d7095457ffa290881186c30967f9f6b771c24a581a041` |
| `ValveSoftware_Proton-releases-latest.json` | 7714 | `20393b1cbbcd68de793a1ef56e847c3395a88e3d4c3af7961966c720349e506e` |
| `gamescope-README.md` | 5685 | `5a9130ced7900e30f62fc7a0b033d2e5d9f849e1069704483c3e396652aeff87` |
| `umu-launcher-README.md` | 19270 | `0a6fb30322d1c27ec54f56f86fcaf729d4bbdebd26e3e079b053b79baa27ca14` |
| `umu-umu_consts.py` | 6295 | `2cef55bf907a3a8c25460f941fbde29465fe20a8e69b2900d386d0707b642b23` |
| `umu-umu_proton.py` | 29046 | `acd951e3e558ec96f1f003b4073be6c81790c99bfef79340ba995ba896150b92` |
| `umu-umu_runtime.py` | 24284 | `ade533c91402f8952113e1cf0893c67547b4e7c4cecf3c94b05b54adb1891669` |

- **Passages.**

`sources/S4-11/Proton-README.md` lines 4–9:
```
    4  **Proton** is a tool for use with the Steam client which allows games which are
    5  exclusive to Windows to run on the Linux operating system. It uses Wine to
    6  facilitate this.
    7  
    8  **Most users should use Proton provided by the Steam Client itself.** See
    9  [this Steam Community post][steam-play-introduction] for more details.
```
`sources/S4-11/Proton-README.md` lines 302–306:
```
  302  If you want to change the runtime configuration for a specific game, you can
  303  use the `Set Launch Options` setting in the game's `Properties` dialog in the
  304  Steam client. Set the variable, followed by `%command%`. For example, input
  305  "`PROTON_USE_WINED3D=1 %command%`" to use the OpenGL-based wined3d renderer
  306  instead of the Vulkan-based DXVK renderer.
```
`sources/S4-11/Proton-README.md` (matching lines):
```
  321  | `wined3d`             | `PROTON_USE_WINED3D`               | Use OpenGL-based wined3d instead of Vulkan-based DXVK for d3d11, d3d10, and d3d9. |
```
`sources/S4-11/umu-launcher-README.md` lines 12–12:
```
   12  This is a unified launcher for Windows games on Linux. It is essentially a copy of the [Steam Runtime Tools](https://gitlab.steamos.cloud/steamrt/steam-runtime-tools) and [Steam Linux Runtime](https://gitlab.steamos.cloud/steamrt/steam-runtime-tools/-/blob/main/docs/container-runtime.md) that Valve uses for [Proton](https://github.com/ValveSoftware/Proton), with some modifications made so that it can be used outside of Steam.
```
`sources/S4-11/umu-launcher-README.md` lines 38–38:
```
   38  When you use `umu-run` to run a game, it uses the specified `WINEPREFIX`, Proton version, executable, and arguments passed to it to run the game in Proton, inside Steam's runtime container JUST like if you were running the game through Steam, except now you're no longer limited to Steam's game library or forced to add the game to Steam's library. In fact, you don't even have to have Steam installed.
```
`sources/S4-11/umu-launcher-README.md` lines 56–56:
```
   56  - `PROTONPATH` designates the full path to a specific proton version. Alternatively you can use value "GE-Proton" to auto-download and use the latest GE-Proton build. Defaults to UMU-Proton. (UMU-Proton is the latest stable version of Valve's proton tool with UMU compatibility added)
```
`sources/S4-11/umu-launcher-README.md` lines 61–61:
```
   61  **Note**: umu-launcher will automatically use and download the latest Steam Runtime that is required by Proton, and move its files to `$HOME/.local/share/umu`.
```
`sources/S4-11/umu-launcher-README.md` lines 67–67:
```
   67  - No Steam or Steam binaries required
```
`sources/S4-11/umu-umu_runtime.py` lines 80–81:
```
   80      host: str = "repo.steampowered.com"
   81      base_url: str = f"https://{host}/{variant.removesuffix('-arm64')}/images/{version}/"
```
`sources/S4-11/umu-umu_runtime.py` lines 276–278:
```
  276      host: str = "repo.steampowered.com"
  277      endpoint: str = f"/{variant.removesuffix('-arm64')}/images"
  278      url: str = f"https://{host}{endpoint}/latest-public-beta.txt"
```
`sources/S4-11/gamescope-README.md` lines 9–9:
```
    9  It also runs on top of a regular desktop, the 'nested' usecase steamcompmgr didn't support.
```
`sources/S4-11/gamescope-README.md` lines 14–14:
```
   14  It runs on Mesa + AMD or Intel, and could be made to run on other Mesa/DRM drivers with minimal work. AMD requires Mesa 20.3+, Intel requires Mesa 21.2+. For NVIDIA's proprietary driver, version 515.43.04+ is required (make sure the `nvidia-drm.modeset=1` kernel parameter is set).
```

Release assets (reader's own extraction from the release JSON: `name` and `size` of each asset): umu-launcher 1.4.4 includes `python3-umu-launcher_1.4.4-1_amd64_ubuntu-noble.deb` (661 336 bytes) and `umu-launcher_1.4.4-1_all_ubuntu-noble.deb` (12 954 bytes); UMU-Proton-10.0-4: `UMU-Proton-10.0-4.tar.gz` (491 237 448 bytes); GE-Proton11-7: `GE-Proton11-7-x86_64.tar.gz` (563 784 602 bytes); ValveSoftware/Proton proton-11.0-2: no assets (empty `assets` list).

- **Coverage.** T11 — covers that Proton is built for use through the Steam client; that umu-launcher runs Proton inside the Steam Linux Runtime container without the Steam client ("No Steam or Steam binaries required"), packaged for Ubuntu noble, downloading the runtime from `repo.steampowered.com` (reachable without credentials, search log row 20) and Proton builds from GitHub; that Valve's Proton GitHub release ships no binaries; that Proton can be switched from DXVK (Vulkan) to wined3d (OpenGL); that gamescope's documented targets are Mesa AMD/Intel and NVIDIA's driver (no software renderer named). Also bears on T4 (existence). Not an observation.

### S4-12 — Mesa 25.2.8 environment variables (llvmpipe threads)

- **Citation.** Mesa, `docs/envvars.rst` at tag `mesa-25.2.8` (commit `f97d7dcca0e51d7e20ed4342bb5ea8afea7db7fa`; the version of `libgl1-mesa-dri` / `mesa-vulkan-drivers` in noble-updates is 25.2.8-0ubuntu0.24.04.x, S4-06), cloned from `https://gitlab.freedesktop.org/mesa/mesa.git`, accessed 2026-10-01.

| file (under `sources/S4-12/`) | bytes | SHA-256 |
|---|---:|---|
| `mesa-25.2.8-envvars.rst` | 71115 | `cea2d9f6cb6f10831207b4a2446a8199e20e74af23c675efb9831a15640a6804` |

- **Passage.**

`sources/S4-12/mesa-25.2.8-envvars.rst` lines 1294–1298:
```
 1294  .. envvar:: LP_NUM_THREADS
 1295  
 1296     an integer indicating how many threads to use for rendering. Zero
 1297     turns off threading completely. The default value is the number of
 1298     CPU cores present.
```

- **Coverage.** T11 — covers that the software rasteriser used on a GPU-less runner sizes its rendering thread pool by default from the number of CPU cores present (so the thread population of any software-rendered program depends on the runner's CPU count, and pinning or `LP_NUM_THREADS` changes it). Not an observation.

### S4-13 — Chromium 153.0.8010.52 command-line switches

- **Citation.** chromium/chromium at tag `153.0.8010.52` (`78e5e45d4bb41035e17ea4da2cc257f496416ac9`): `media/base/media_switches.cc`, `media/capture/capture_switches.cc`, `content/public/common/content_switches.cc`, accessed 2026-10-01. The runner's Google Chrome is 153.0.8010.52 (S4-01).

| file (under `sources/S4-13/`) | bytes | SHA-256 |
|---|---:|---|
| `chromium-153.0.8010.52-capture_switches.cc` | 2294 | `d613d4562f76a222ead29fdf2248bf20b194af74c3da93608814181d71e20315` |
| `chromium-153.0.8010.52-content_switches.cc` | 45238 | `c5790d35e18cfd1151a9e5af651eb2b39e4d725090b1ee23ad8163e4ad0f290b` |
| `chromium-153.0.8010.52-media_switches.cc` | 87017 | `fa4c15a682e8900429e6d24c297176cc1ced247e90538ee4168e618509e8a7d7` |

- **Passages.**

`sources/S4-13/chromium-153.0.8010.52-media_switches.cc` lines 142–145:
```
  142  // Forces input and output stream creation to use fake audio streams.
  143  const char kDisableAudioInput[] = "disable-audio-input";
  144  
  145  const char kDisableAudioOutput[] = "disable-audio-output";
```
`sources/S4-13/chromium-153.0.8010.52-media_switches.cc` lines 229–232:
```
  229  // Use fake device for Media Stream to replace actual camera and microphone.
  230  // For the list of allowed parameters, see
  231  // FakeVideoCaptureDeviceFactory::ParseFakeDevicesConfigFromOptionsString().
  232  const char kUseFakeDeviceForMediaStream[] = "use-fake-device-for-media-stream";
```
`sources/S4-13/chromium-153.0.8010.52-media_switches.cc` lines 240–252:
```
  240  // Play a .wav file as the microphone. Note that for WebRTC calls we'll treat
  241  // the bits as if they came from the microphone, which means you should disable
  242  // audio processing (lest your audio file will play back distorted). The input
  243  // file is converted to suit Chrome's audio buses if necessary, so most sane
  244  // .wav files should work. You can pass either <path> to play the file looping
  245  // or <path>%noloop to stop after playing the file to completion.
  246  //
  247  // Must also be used with kDisableAudioInput or kUseFakeDeviceForMediaStream.
  248  const char kUseFileForFakeAudioCapture[] = "use-file-for-fake-audio-capture";
  249  
  250  // Use an .y4m file to play as the webcam. See the comments in
  251  // media/capture/video/file_video_capture_device.h for more details.
  252  const char kUseFileForFakeVideoCapture[] = "use-file-for-fake-video-capture";
```
`sources/S4-13/chromium-153.0.8010.52-content_switches.cc` lines 129–131:
```
  129  // Disables GPU hardware acceleration.  If software renderer is not in place,
  130  // then the GPU process won't launch.
  131  const char kDisableGpu[]                    = "disable-gpu";
```
`sources/S4-13/chromium-153.0.8010.52-content_switches.cc` lines 623–626:
```
  623  // Overrides the default/calculated limit to the number of renderer processes.
  624  // Very high values for this setting can lead to high memory/resource usage
  625  // or instability.
  626  const char kRendererProcessLimit[]          = "renderer-process-limit";
```
`sources/S4-13/chromium-153.0.8010.52-content_switches.cc` lines 751–755:
```
  751  // Bypass the media stream infobar by selecting the default device for media
  752  // streams (e.g. WebRTC). Works with --use-fake-device-for-media-stream.
  753  // Prefer --auto-accept-camera-and-microphone-capture which does not interact
  754  // with screen/tab capture.
  755  const char kUseFakeUIForMediaStream[]     = "use-fake-ui-for-media-stream";
```
`sources/S4-13/chromium-153.0.8010.52-content_switches.cc` lines 674–678:
```
  674  // - The class comment in site_instance.h, listing the supported process models.
  675  //
  676  // IMPORTANT: this isn't to be confused with --process-per-site (which is about
  677  // process consolidation, not isolation). You probably want this one.
  678  const char kSitePerProcess[]                = "site-per-process";
```

- **Coverage.** T11 — covers that the runner's Chrome can replace camera and microphone with fake or file-backed devices and auto-accept the permission prompt, can force fake audio input/output streams, and has switches for the renderer-process limit and site-per-process. Also bears on T3 and T10 (existence of the switches). Not an observation.

### S4-14 — Two-peer WebRTC on one machine: docker-jitsi-meet; WebRTC samples "Peer connection"

- **Citation.** jitsi/docker-jitsi-meet `README.md` at `5ba823f9b4cf2cf7b67aa23c9102416bc28fc35c`; webrtc/samples `src/content/peerconnection/pc1/index.html` at `6e2c5a117aa860d66d874f7c0df0ef9a3e2cd74e`; accessed 2026-10-01.

| file (under `sources/S4-14/`) | bytes | SHA-256 |
|---|---:|---|
| `docker-jitsi-meet-README.md` | 1281 | `c7c4c9be561c28e4a22f095cfac094a44d5231698aebf86704ec7ced690f2d92` |
| `webrtc-samples-pc1-index.html` | 2761 | `d9aaea53d7874c469a2d02baa64d9ce20246f8f28805ecaacb6b83ad50897741` |

- **Passages.**

`sources/S4-14/docker-jitsi-meet-README.md` lines 7–9:
```
    7  [Jitsi Meet](https://jitsi.org/jitsi-meet/) is a fully encrypted, 100% Open Source video conferencing solution that you can use all day, every day, for free — with no account needed.
    8  
    9  This repository contains the necessary tools to run a Jitsi Meet stack on [Docker](https://www.docker.com) using [Docker Compose](https://docs.docker.com/compose/).
```
`sources/S4-14/webrtc-samples-pc1-index.html` lines 38–40:
```
   38      <p>This sample shows how to setup a connection between two peers using
   39          <a href="https://developer.mozilla.org/en-US/docs/Web/API/RTCPeerConnection">RTCPeerConnection</a>.
   40      </p>
```

- **Coverage.** T11 — covers that a complete Jitsi Meet server can run from Docker images without an account (the runner has Docker, S4-01), and that a single-page two-peer `RTCPeerConnection` sample exists (both peers inside one page, hence one renderer). Not an observation.

### S4-15 — Vendor repositories and download endpoints for the T8 programs not in the Ubuntu archive; Microsoft's Teams-on-Linux announcement

- **Citation.** The apt indexes listed in search-log row 23 and the redirects in row 24, accessed 2026-10-01; Microsoft Tech Community, Anupam Pattnaik, "Microsoft Teams progressive web app now available on Linux", Nov 07, 2022, `https://techcommunity.microsoft.com/blog/microsoftteamsblog/microsoft-teams-progressive-web-app-now-available-on-linux/3669846`, accessed 2026-10-01.

| file (under `sources/S4-15/`) | bytes | SHA-256 |
|---|---:|---|
| `element-Packages` | 2628 | `41b1136164fd9414f3b343927080580a66bf18e2705d1f6f810dfa68880ea9a5` |
| `google-chrome-Packages` | 6205 | `d475fc8f06bedf47ea1aa0296b7c470c23742fe917e1c8899b9bb91b66bd5697` |
| `ms-code-Packages.gz` | 30622 | `c647adab349cd477a9092f9e3efbddbce5263b391b68a55059f3b6a4caee1ab0` |
| `ms-teams-Packages` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `ms-teams-pwa-linux-blog.html` | 370826 | `1991276a2772dcbc78c36a4ef60b16a70452e18758a220b2a1e74c5519e4a9c4` |
| `slack-Packages` | 30364 | `e30625021217b5e1ad0910f5205bd40699509cb57671f20f4e7191bb8cf2c8cb` |
| `spotify-Packages` | 987 | `dc1fb9d8fa17df0396914a7b0a2b9461691a1ef684c3b59647c0fda25bc37704` |
| `steam-amd64-Packages` | 2657 | `ed846bba87d7b831aa648dc6a92c759bba60551d940b1397c7d4cf60c261da57` |
| `steam-i386-Packages` | 1834 | `156d3795f4e388a97c44d515b3384b014fe48ecf33ffbc37ca5f6f37bdd01b1e` |
| `winehq-noble-amd64-Packages` | 1226503 | `bffbe75274ad7678d51eb8b1c404e2cd986221208f846a5f63988d9daedf2cfd` |

- **Passages (index fields).**

`sources/S4-15/ms-code-Packages.gz` lines 1591–1593:
```
 1591  Package: code
 1592  Version: 1.140.0-1790759618
 1593  Architecture: amd64
```
`sources/S4-15/google-chrome-Packages` (matching lines):
```
    1  Package: google-chrome-beta
    2  Version: 156.0.8078.4-1
   19  Package: google-chrome-canary
   20  Version: 157.0.8080.0-1
   37  Package: google-chrome-repo
   38  Version: 3
   54  Package: google-chrome-stable
   55  Version: 154.0.8037.92-1
   72  Package: google-chrome-unstable
   73  Version: 156.0.8072.0-1
```
`sources/S4-15/spotify-Packages` (matching lines):
```
    1  Package: spotify-client
    3  Version: 1:1.2.96.518.g366879e1
```
`sources/S4-15/slack-Packages` lines 595–601:
```
  595  Package: slack-desktop
  596  Priority: optional
  597  Section: misc
  598  Installed-Size: 144964
  599  Maintainer: Slack Technologies <feedback@slack.com>
  600  Architecture: amd64
  601  Version: 4.52.162
```
`sources/S4-15/element-Packages` (matching lines):
```
    1  Package: element-desktop
    2  Version: 1.12.30
   22  Package: element-io-archive-keyring
   25  Version: 1.2
   35  Package: element-nightly
   36  Version: 2026093001
   56  Package: element-web
   57  Version: 1.12.30
```
`sources/S4-15/steam-amd64-Packages` (matching lines):
```
    1  Package: steam-launcher
    3  Version: 1:1.0.0.87
    8  Depends: apt (>= 1.1), apt (>= 1.6) | apt-transport-https, ca-certificates, coreutils (>= 8.23-1~), curl, default-dbus-session-bus | dbus-session-bus | dbus-x11, file, libc6 (>= 2.15), libnss3 (>= 2:3.26), lsof, pkexec | policykit-1, python3 (>= 3.4), python3-apt, xdg-user-dirs, xterm | gnome-terminal | konsole, xz-utils, zenity
    9  Recommends: steam-libs-amd64, steam-libs-i386, sudo, xdg-desktop-portal, xdg-desktop-portal-gtk | xdg-desktop-portal-backend, xdg-utils | steamos-base-files
   28  Package: steam-libs-amd64
   30  Version: 1:1.0.0.87
   34  Depends: default-dbus-session-bus | dbus-session-bus | dbus-x11, libc6 (>= 2.15), libcrypt1 | libc6 (<< 2.29-4), libegl1 | libegl1-mesa, libgbm1, libnss3 (>= 2:3.26), libgl1, libgl1-mesa-dri, libgcc-s1 | libgcc1, libgpg-error0 (>= 1.10), libstdc++6, libudev1 | libudev0, libxcb-dri3-0, libxcb1, libxinerama1 (>= 2:1.1.1), libx11-6
   35  Recommends: libasound2-plugins, libxkbcommon-x11-0, libva2, libva-drm2, libva-glx2, libva-x11-2, libxss1, mesa-vulkan-drivers, va-driver-all | va-driver, xdg-desktop-portal, xdg-desktop-portal-gtk | xdg-desktop-portal-backend
```
`sources/S4-15/steam-i386-Packages` (matching lines):
```
    1  Package: steam
    2  Version: 1:1.0.0.87
   18  Package: steam-libs-i386
   20  Version: 1:1.0.0.87
```
`sources/S4-15/winehq-noble-amd64-Packages` lines 15811–15811:
```
15811  Package: winehq-stable
```
`sources/S4-15/winehq-noble-amd64-Packages` lines 15819–15819:
```
15819  Version: 11.0.0.0~noble-1
```

`ms-teams-Packages`: HTTP 200, 0 bytes (SHA-256 of the empty string) — the Microsoft Teams Linux repository index lists no package.

Teams blog, article text (verbatim, tags stripped): "We’re excited to announce the general availability of support for the Microsoft Teams progressive web app (PWA) as a feature of our current web client for Linux customers." … "The PWA experience is available for both Edge and Chrome browsers running on Linux."

Download redirects (`curl -sI -L`, search-log row 24): Zoom `zoom_amd64.deb` 7.2.1.5760 (302 → 200); Discord `discord-1.0.160.deb` (302 → 200).

- **Coverage.** T11 — covers the install route on the runner for VS Code (Microsoft repo, 1.140.0), Google Chrome (154.0.8037.92-1 in the repo; the runner has 153), Spotify (1:1.2.96.518.g366879e1), Slack (4.52.162), Element (1.12.30), Steam (`steam-launcher` 1:1.0.0.87, recommending `steam-libs-i386`), WineHQ (stable 11.0.0.0, devel/staging 11.18), Zoom and Discord (vendor debs), and the absence of a Teams Linux desktop package (Teams on Linux is a PWA in Edge or Chrome). Also bears on T8 (packaging). Not an observation.

### S4-16 — mutter 46.2 command-line options (GNOME Shell's compositor library)

- **Citation.** GNOME/mutter at tag `46.2`, `src/core/meta-context-main.c`, via the GitHub mirror, accessed 2026-10-01. The desktop image ships `mutter-common 46.2-1ubuntu0.24.04.16` and `gnome-shell 46.0-0ubuntu6~24.04.14` (S4-03).

| file (under `sources/S4-16/`) | bytes | SHA-256 |
|---|---:|---|
| `mutter-46.2-meta-context-main.c` | 21656 | `a559e0b970c23f9f04fce303d1077f2ec9d20196d685b61c2aae0830a6b4d2d7` |

- **Passages.**

`sources/S4-16/mutter-46.2-meta-context-main.c` lines 637–647:
```
  637        "wayland", 0, 0, G_OPTION_ARG_NONE,
  638        &context_main->options.wayland,
  639        N_("Run as a wayland compositor"),
  640        NULL
  641      },
  642      {
  643        "nested", 0, 0, G_OPTION_ARG_NONE,
  644        &context_main->options.nested,
  645        N_("Run as a nested compositor"),
  646        NULL
  647      },
```
`sources/S4-16/mutter-46.2-meta-context-main.c` lines 667–676:
```
  667      {
  668        "headless", 0, 0, G_OPTION_ARG_NONE,
  669        &context_main->options.headless,
  670        N_("Run as a headless display server")
  671      },
  672      {
  673        "virtual-monitor", 0, 0, G_OPTION_ARG_CALLBACK,
  674        add_virtual_monitor_cb,
  675        N_("Add persistent virtual monitor (WxH or WxH@R)")
  676      },
```

- **Coverage.** T11 — covers that mutter (and so GNOME Shell built on it) has nested, headless and virtual-monitor modes — the route by which a runner without a display could host a GNOME Shell Wayland session and its on-demand Xwayland. Whether it starts on the runner without a GPU is not documented here. Also bears on T8 (existence). Not an observation.

---

## 3. Not found

| question | searches that established it |
|---|---|
| The Azure VM size, CPU model and network bandwidth of standard `ubuntu-24.04` runners | GitHub hosted-runner reference read in full (S4-02); WebSearch row 28 — the docs give CPU count, RAM and SSD only. |
| Whether standard runner VMs boot with UEFI Secure Boot (decides whether a DKMS-built module can be loaded) | WebSearch row 13; runner-images build scripts grepped for `secure`/`mok`/`kvm` at `14d8569` (no hits for Secure Boot); Ubuntu wiki page unreachable (404, 500, 500). |
| Whether a runner job has a logind session / a running `systemd --user` and session D-Bus (needed by Tracker, PipeWire, portals, Déjà Dup) | Hosted-runner reference and runner-images scripts read; nothing found. |
| What the Steam client does without logging in (whether it can download Proton, the runtime or any app) and the default of "allow downloads during gameplay" | Steam FAQ `71AB-698D-57EB-178C` read in full (states the setting exists, not its default); WebSearch rows 15–16 gave only community threads. |
| gamescope running on a software Vulkan driver (lavapipe) or headless on a GPU-less machine | gamescope README at `0e590c75` read in full; gamescope is not in the noble archive (S4-06). |
| Any primary statement on whether sysstat collects on a stock Ubuntu 24.04 desktop | WebSearch row 27 (only third-party pages on enabling sysstat); settled here only as an inference from the image (S4-03, S4-05). |
| Object counts, build durations or process populations of any DKMS build, and any duration of any timer job | Out of reach for documents (existence only); every T11 duration needs a runner observation (Appendix B). |

---

## Appendix A — T11 observability per item (reader's assessment, resting on the candidates above)

Verdicts: **observable**, **observable with conditions**, **not observable**. "Deciding fact" names the candidate and says what it states.

**A1. A game under Proton / Wine with software rendering beside the Steam client; its process and thread population and names; without a Steam account where that is required — observable with conditions.**
- Wine path: `wine`/`wine64` 9.0 are in noble universe and WineHQ ships 11.x for noble (S4-06, S4-15); Mesa's software OpenGL (`swrast_dri.so`) and software Vulkan (`libvulkan_lvp.so`, lavapipe) are packaged (S4-04 Contents lines; S4-06); Xvfb is on the runner (S4-01). No account is needed for a freely redistributable Windows game. The runner can see the full process tree, thread counts, `comm` names (15 characters, S4-09) and per-thread scheduling.
- Proton path without Steam: umu-launcher (Ubuntu noble debs) runs Proton in the Steam Linux Runtime container — "you don't even have to have Steam installed" — fetching the runtime from `repo.steampowered.com` and UMU-Proton/GE-Proton from GitHub — no account (S4-11). Proton's README says Proton is meant for use with the Steam client and Valve's GitHub release ships no binary (S4-11), so *Valve's* Proton build through Steam needs whatever the Steam client needs (not documented, §3). Proton's `PROTON_USE_WINED3D` selects OpenGL instead of Vulkan (S4-11).
- Steam client beside it: installable (`steam-installer` in multiverse depends on `steam-libs-i386`; Valve's `steam-launcher` recommends it — so `dpkg --add-architecture i386` is needed; S4-06, S4-15). What the client runs and downloads without an account is not documented (§3; Appendix B check 9); a logged-in client needs credentials and, for a Steam Guard account, an e-mailed code on every fresh runner unless the login files are carried over (S4-10).
- Cannot observe: GPU-driven rendering and its threads (no GPU, S4-02); the thread population of a GPU desktop — llvmpipe adds a rendering pool sized from the CPU count (S4-12), so the software-rendered population is not the hardware one; a logged-in Steam client without an account.

**A2. The Steam client downloading while a game runs — not observable without a Steam account; observable with conditions with one.**
- Deciding fact: Steam "will automatically download updates for your games based on the Steam client's download settings", and there is "a per-game setting to allow/prevent the downloading of other updates while you're playing" (S4-10) — the games are an account's games; the default of that setting is not documented (§3). Anonymous SteamCMD can download most dedicated-server apps (S4-10) — that is a different program (`steamcmd`), a proxy only, not the client's download path.
- Conditions with an account: credential and Steam Guard handling on an ephemeral VM (S4-10); download bandwidth of the runner is undocumented (§3).

**A3. A DKMS autoinstall of a real module after a kernel package is installed; its process population and duration — observable with conditions.**
- Deciding facts: `dkms` 3.0.11 is in noble main; installing `linux-headers-<ver>` runs `/etc/kernel/header_postinst.d/dkms` and installing a kernel image runs `/etc/kernel/postinst.d/dkms`, both of which run `dkms autoinstall --kernelver <ver>` when that kernel's headers exist (S4-07, S4-08). Headers and tools for the runner's own kernel are in noble-updates (S4-06). The build runs `make -j$(nproc)` and `nproc` counts only the CPUs the caller may use (S4-07).
- Real modules that should build against the runner's 6.17 kernel per their packages: `v4l2loopback-dkms` (6.16/6.18 fixes; needs `CONFIG_VIDEO_DEV`, which the azure kernel has as a module — S4-07, S4-08), `virtualbox-dkms` (6.17 patches, S4-07), `nvidia-dkms-580` (whether it builds without a GPU is not documented in the sources read). `zfs-dkms`'s changelog stops at Linux 6.8 (S4-07), so for ZFS the "kernel package installed" should be a 6.8 kernel (`linux-headers-6.8.0-146-generic` is in noble-updates, S4-06).
- Conditions: the build process tree and duration are runner-specific (CPU model undocumented, §3); if the autoinstall is launched inside the pinned CPU set, `-j` becomes 1 — the pinning decides the parallelism; the azure kernel already ships `v4l2loopback.ko` and `zfs.ko` (S4-04), which may change what `dkms install` does after the build (to check); *loading* a DKMS-built module is refused if the VM booted under Secure Boot (lockdown, S4-08, S4-09) — the build itself is unaffected.
- Not on a stock desktop: `dkms`, `gcc` and `make` are in neither desktop selection (S4-03), so on a stock 24.04 desktop a DKMS autoinstall exists only after the user installs a DKMS package.

**A4. Which systemd timers and cron jobs a stock Ubuntu 24.04 desktop schedules and what each runs — existence answered without a runner (S4-03, S4-05); execution observable with conditions.**
- Answered from the shipped image: the enabled timer list, the cron files, each unit's schedule and command, the gating conditions, the sysstat wiring, Déjà Dup's default (S4-03, S4-05; listed in their coverage).
- The runner image is not a stock desktop: it is the Azure server image with apt timers disabled, `unattended-upgrades` purged, `fwupd-refresh` masked, motd-news and man-db auto-update off, snap refresh held (S4-01). Installing `ubuntu-desktop-minimal` on top would not reproduce the stock state (reader's reading, to be checked): packages already present (`apt`, `fwupd`, `man-db`, `base-files`) are not reconfigured by installing other packages, and the generated postinst enables a unit on reconfiguration only when it "was-enabled" (S4-05, logrotate postinst) — the runner disabled or masked those units.
- Route to the stock state on a runner: boot the image itself — the ISO's layered squashfs or an installed disk — as a KVM guest (KVM usable after a udev rule, S4-02); `qemu-system-x86` and `ovmf` are in noble (S4-06). A `systemd-nspawn` container would skip `fstrim`, `fwupd-refresh` and `systemd-sysupdate`, which carry `ConditionVirtualization=!container` (S4-05). The instruments then run inside the guest (or see only the QEMU process from the host).
- Cannot observe in one job: timers that fire daily or weekly at their real times (6-hour job cap, S4-02) — each job must be started by hand or the guest clock moved; what a job does on a real user's disk (man-db, logrotate, e2scrub, fstrim work on the guest's own content).

**A5. The `comm` strings of the T8 programs once installed and run — observable with conditions, per program.**
- Installable and runnable on the runner without an account (under Xvfb where graphical): LibreOffice Writer, Evince, VS Code, Google Chrome, Chromium, Firefox, Thunderbird (the noble deb is a transitional package to the snap), GIMP, darktable, Kdenlive and `melt`, Blender, mpv, VLC, Wine, Tracker 3.7, Baloo (KF5), plocate, ClamAV, borg, rsync, rclone, 7-Zip (`7zz`), tar, xz, HandBrakeCLI, ffmpeg, python3, make, gcc, dkms, PipeWire, systemd, `dbus-daemon`, `dbus-broker`, Xvfb (S4-01, S4-06, S4-15). The kernel stores 15 characters of `comm` (S4-09).
- Need an account for their main function: Spotify, Slack, Discord, Element, Zoom, Steam (reader's expectation, not documented in the sources read except for Steam, S4-10); what each runs before login is a runner check. Install routes: S4-15.
- Not installable as a native client: Microsoft Teams (repository index empty; Teams on Linux is a PWA in Edge or Chrome, S4-15).
- Need extra work: gamescope (not in the noble archive; build from source, documented for GPU drivers only — S4-06, S4-11); GNOME Shell and Xwayland, which needs a Wayland compositor to attach to (mutter's `--headless` / `--nested` modes exist, S4-16; starting without a GPU is a runner check); Xorg proper (the runner provides Xvfb; a real Xorg needs a DRM device — `vkms` exists as a module, S4-04, S4-08, untested); LocalSearch (not in noble; noble ships Tracker 3.7, S4-06).
- Cannot observe: names that differ with packaging the runner does not use by default (the runner's Firefox and Chromium are a PPA deb and a snapshot zip, not the stock desktop's snaps — S4-01, S4-06); audio threads that depend on sound hardware (no `CONFIG_SOUND`, S4-08).

**A6. An incremental backup — observable with conditions.**
- `rsync` is preinstalled; `borgbackup`, `restic`, `duplicity`, `deja-dup` are in noble (S4-01, S4-06). Déjà Dup's scheduled backups are off by default and its default tool is duplicity (S4-05).
- Conditions: the data set must be made or copied in (a fresh VM has no user data); 14 GB SSD per the docs (S4-02) — the free space at run time is a check; the runner's root ext4 is mounted `nobarrier,data=writeback,journal_async_commit,commit=30` (S4-01), so write and fsync costs differ from a desktop's default ext4; Déjà Dup needs a session bus and display (§3 for the session question).

**A7. An application's launch work — observable with conditions.**
- Any of A5's programs can be launched under the instruments; page cache can be dropped for cold launches (S4-09).
- Conditions: no GPU (software rendering threads, S4-12); every job is a first run on a fresh VM (S4-02), so first-run work (profile creation, caches) is the default and warm-start runs must be repeated inside the job; the runner forces `read_ahead_kb` to 128 by udev rule (S4-01); desktop-session services the app talks to at start-up (portals, keyring, Tracker, D-Bus session) exist only if the job starts them (§3).

**A8. A browser with several windows — observable with conditions.**
- Chrome 153, Chromium 153 and Firefox 156 are preinstalled (S4-01); several windows can be opened on Xvfb; the renderer-process limit and site isolation are switchable (S4-13).
- Conditions: no GPU (`--disable-gpu` doc: without a software renderer the GPU process does not launch, S4-13); the browser builds are not the stock desktop's snaps (S4-01); how many windows count as "visible" under Xvfb without a window manager is a runner check.

**A9. A video call in a browser between two local peers — observable with conditions; commercial services not observable.**
- Chrome's fake capture devices, file-backed camera (`.y4m`) and microphone (`.wav`), and auto-accepted permission are documented switches (S4-13). Two local peers: a self-hosted Jitsi Meet from docker-jitsi-meet ("no account needed"; Docker is on the runner — S4-14, S4-01) with two browser instances, or the single-page WebRTC sample (both peers in one renderer, S4-14).
- Conditions: no sound hardware (no `CONFIG_SOUND`, S4-08) — audio must be a fake stream or a PipeWire null sink; video encode/decode is software (no GPU).
- Not established, treated as not observable: calls through Zoom, Teams, Google Meet or other hosted services — the sources read document only the clients' packaging (S4-15), not joining without an account; a hosted call also involves peers and servers outside the runner.

**A10. Instruments themselves — observable with conditions.**
- `perf` for the runner kernel is `linux-tools-6.17.0-1022-azure` (S4-06); tracepoints, schedstats, taskstats and delay accounting are compiled in, perf events are restricted for unprivileged users so `sudo` is needed (S4-08); `perf record -k CLOCK_MONOTONIC` and `timehist --wakeups` are documented (S4-09); delay accounting must be switched on (`sysctl kernel.task_delayacct=1`) **before** the measured tasks start (S4-09).
- Conditions: 4 vCPUs only in a public repository (2 in a private one, S4-02); the runner's own services (runner agent, Docker, snapd, …) are not pinned unless fenced with `AllowedCPUs=` on the slices (S4-09); the runner image is replaced over time (tags `ubuntu24/20260823.283` … `ubuntu24/20260927.320`, search-log row 1), so the kernel ABI and package versions must be recorded per run.

**What the runner cannot observe at all (from the above):** GPU-rendered paths and display timing (no GPU, no display, S4-02); sound hardware (S4-08); real users' data, open-application mixes, focus, tabs or operation rates (all user-side questions T1, T2, T3-usage, T6, T9-rates, T10-rates — a runner only executes what the probe scripts); logged-in third-party services without accounts (A2, A5, A9); multi-day timer behaviour (A4).

## Appendix B — checks a runner would have to make (described, not run)

1. **Runner identity per run.** `nproc`, `lscpu`, `uname -r`, `grep -E 'ImageVersion|ImageOS' /etc/environment`, `df -h / /mnt`, `cat /proc/cmdline`; record the image version and kernel ABI (the image is replaced over time, S4-01).
2. **Instrument readiness.** `sudo apt-get install linux-tools-$(uname -r)`; `sudo perf sched record -k CLOCK_MONOTONIC -- sleep 1 && sudo perf sched timehist --wakeups | head`; `sysctl kernel.perf_event_paranoid kernel.task_delayacct`; `sudo sysctl kernel.task_delayacct=1` before starting the load; check that a taskstats client (the kernel tree's `getdelays`, named in the delay-accounting document) returns non-zero delays for a task started afterwards.
3. **CPU fencing.** `sudo systemctl set-property --runtime system.slice AllowedCPUs=1-3` (and `user.slice`, `init.scope`), load under `taskset -c 0`; verify with `ps -eo pid,psr,comm` and `perf sched timehist` that nothing else ran on CPU 0.
4. **Stock desktop timers in a KVM guest.** Add the KVM udev rule (S4-02), install `qemu-system-x86 ovmf`, install the 24.04.5.1 desktop (default selection) into a disk image unattended or boot its layered squashfs, then inside the guest: `systemctl list-timers --all`, `systemctl --global list-unit-files --type=timer`, `systemctl status sysstat-collect.timer` and `ls /var/log/sysstat` after 20 minutes (settles the sysstat inference of S4-05), `journalctl -u apport-autoreport -u ua-timer -u snapd.snap-repair -u motd-news` (settles which gated jobs run), then `systemctl start <each>.service` under `perf sched record` for each job's process tree and duration.
5. **Secure Boot and module loading.** `mokutil --sb-state`, `cat /sys/kernel/security/lockdown`; after a DKMS build, `sudo modprobe v4l2loopback` and read the error if refused.
6. **DKMS autoinstall.** `sudo apt-get install dkms v4l2loopback-dkms` (records the build for the running kernel), then `sudo apt-get install linux-headers-6.8.0-146-generic` or another kernel's headers/image under `perf sched record` and `/proc` snapshots; once launched outside and once inside the pinned CPU set (to see the `-j` change); read `/var/lib/dkms/*/*/build/make.log` for the make command; repeat with `virtualbox-dkms`, `nvidia-dkms-580`, and `zfs-dkms` against a 6.8 kernel.
7. **Session plumbing.** `loginctl list-sessions`, `systemctl --user status`, `echo $DBUS_SESSION_BUS_ADDRESS $XDG_RUNTIME_DIR`; if absent, `sudo loginctl enable-linger runner` or `dbus-run-session`, and check that `pipewire`, `wireplumber`, `tracker-miner-fs-3` start.
8. **User namespaces (Proton container, Chrome sandbox).** `sysctl kernel.apparmor_restrict_unprivileged_userns`, `ls /etc/apparmor.d/ | grep -E 'steam|chrome|unprivileged_userns'`; run `umu-run` on a small freely redistributable Windows program with `PROTON_USE_WINED3D=1` under Xvfb and record `ps -eLo pid,tid,comm`.
9. **Steam client.** `sudo dpkg --add-architecture i386`, install `steam-launcher` (Valve repo) or `steam-installer`, start it under Xvfb without credentials and record which processes appear and what it downloads (bytes, hosts) before the login screen.
10. **GNOME Shell headless.** Install `gnome-shell` and run `gnome-shell --headless --wayland --virtual-monitor 1920x1080` inside `dbus-run-session`; check whether it starts on llvmpipe and whether an X11 client makes Xwayland start and later exit.
11. **Video call.** `docker compose` up docker-jitsi-meet locally; two Chrome instances with `--use-fake-device-for-media-stream --use-fake-ui-for-media-stream --use-file-for-fake-video-capture=<y4m>`; record per-process thread names and wakeups; separately, check what Chrome does for audio output with no sound devices.
12. **Browser windows.** Open N windows × M tabs under Xvfb with and without a window manager (`openbox`, if used); count renderer processes and whether background windows are throttled.
