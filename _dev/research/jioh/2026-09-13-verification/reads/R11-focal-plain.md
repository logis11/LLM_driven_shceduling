# R11 read — focal-arxiv26, videogui-arxiv24, plain

> Independent primary-source read. Input: `inputs/R11-focal-plain.md`. All copies retrieved 2026-09-13. `S` = `_dev/research/jioh/2026-09-13-verification/sources`.

## Copies used

"Part row" = the row number the per-topic section below uses when it says "row N" (numbering restarts per part: C-plain-1/6, C-plain-4/5 and C-plain-7/8/9 each have their own; F/V rows belong to the FOCAL/VideoGUI sections).

| Topic(s) | Part row | Copy | URL | Version / commit / date | Local path |
|---|---|---|---|---|---|
| C-focal-1…5 | F1 | FOCAL arXiv abstract page (v2 current) and v1 abstract page | https://arxiv.org/abs/2604.19541 ; https://arxiv.org/abs/2604.19541v1 | submission history v1 2026-04-21, v2 2026-07-18 | `S/focal-arxiv26/abs.html`, `abs-v1.html` |
| C-focal-1…5 | F2 | FOCAL PDF v2 (+ extracted text) | https://arxiv.org/pdf/2604.19541v2 | v2; PDF CreationDate 2026-07-21 (arXiv GenPDF) | `S/focal-arxiv26/v2.pdf`, `v2.txt` |
| C-focal-1…5 | F3 | FOCAL PDF v1 (+ extracted text) | https://arxiv.org/pdf/2604.19541v1 | v1; PDF CreationDate 2026-04-22 | `S/focal-arxiv26/v1.pdf`, `v1.txt` |
| C-focal-1…5 | F4 | FOCAL v2 author TeX source | https://arxiv.org/src/2604.19541v2 | v2 source tarball | `S/focal-arxiv26/src-v2/` (main file `sample-sigconf-authordraft.tex`) |
| C-focal-1…4 | F5 | DesktopBench dataset repo (HF), git clone | https://huggingface.co/datasets/HaoranYin/desktopbench | commit `49c3683061073ecf8cfadf962ce5d563a2e1dd43` (2026-07-19) = annotated tag `v0.1.0` | `S/focal-arxiv26/hf-desktopbench/`, `hf-dataset-api.json` |
| C-focal-4 | F6 | Companion code repo metadata (GitHub API) | https://api.github.com/repos/Haoran2099/focal | created 2026-07-19; latest commit `0ce2eae723efc144249aa84e447e6e16351752c2` | `S/focal-arxiv26/gh-focal-repo.json` |
| C-focal-4 | F7 | Discovery searches (not evidence): GitHub repo search "DesktopBench", HF dataset search "DesktopBench" | https://api.github.com/search/repositories?q=DesktopBench ; https://huggingface.co/api/datasets?search=DesktopBench | responses 2026-09-13 | `S/focal-arxiv26/gh-search-desktopbench.json`, `hf-search.json` |
| C-videogui-1 | V1 | VideoGUI arXiv abstract page | https://arxiv.org/abs/2406.10227 | v1 only, 2024-06-14 | `S/videogui-arxiv24/abs.html` |
| C-videogui-1 | V2 | VideoGUI PDF v1 (+ text) | https://arxiv.org/pdf/2406.10227v1 | v1 | `S/videogui-arxiv24/v1.pdf`, `v1.txt` |
| C-videogui-1 | V3 | VideoGUI NeurIPS 2024 D&B proceedings page | https://proceedings.neurips.cc/paper_files/paper/2024/hash/804e757b7d7043c26701c3a313032101-Abstract-Datasets_and_Benchmarks_Track.html | as served | `S/videogui-arxiv24/neurips-abstract-804e.html` |
| C-videogui-1, C-focal-4 | V4 | VideoGUI HF dataset cards at pinned revisions | https://huggingface.co/api/datasets/VideoGUI/VideoGUI-Action/revision/0a8110739acf4c766d4d55c9672cb38d1d9bfcbd ; …/VideoGUI-Mid-Plan/revision/6852d8c9f2b9c586d7ff7cce2611080140f1a30c (+ raw README.md at those revisions) | Action @0a81107 (2025-06-13); Mid-Plan @6852d8c (2025-06-13) | `S/videogui-arxiv24/hf-VideoGUI-*.json`, `hf-VideoGUI-*-README.md` |
| C-plain-1, C-plain-6 | 1 | Chromium `docs/process_model_and_site_isolation.md` | https://chromium.googlesource.com/chromium/src/+/2060fcb7f9606a3364966768115a9848d8a69880/docs/process_model_and_site_isolation.md?format=TEXT | chromium/src main @ `2060fcb7f9606a3364966768115a9848d8a69880` (committed 2026-09-13 05:18:08) | `S/C-plain-1/docs_process_model_and_site_isolation.md` |
| C-plain-1, C-plain-6 | 2 | Chromium `docs/linux/zygote.md` | same host, same commit | `2060fcb7…` | `S/C-plain-1/docs_linux_zygote.md` |
| C-plain-1, C-plain-6 | 3 | Chromium `content/public/common/content_switches.cc` | same host, same commit | `2060fcb7…` | `S/C-plain-1/content_public_common_content_switches.cc` |
| C-plain-1, C-plain-6 | 4 | Chromium `base/process/set_process_title.cc`, `base/process/set_process_title_linux.cc` | same host, same commit | `2060fcb7…` | `S/C-plain-1/base_process_set_process_title*.cc` |
| C-plain-1, C-plain-6 | 5 | Chromium `base/threading/platform_thread_linux.cc` | same host, same commit | `2060fcb7…` | `S/C-plain-1/base_threading_platform_thread_linux.cc` |
| C-plain-1, C-plain-6 | 6 | Chromium `content/app/content_main.cc`, `content/zygote/zygote_linux.cc` | same host, same commit | `2060fcb7…` | `S/C-plain-1/content_app_content_main.cc`, `S/C-plain-1/content_zygote_zygote_linux.cc` |
| C-plain-1, C-plain-6 | 7 | Chromium `sandbox/policy/mojom/sandbox.mojom` | same host, same commit | `2060fcb7…` | `S/C-plain-1/sandbox_policy_mojom_sandbox.mojom` |
| C-plain-1, C-plain-6 | 8 | chromium.org design doc "Multi-process Architecture" (source markdown) | https://chromium.googlesource.com/website/+/a88b32e46218523463a769f0ecfcb4da46649ce5/site/developers/design-documents/multi-process-architecture/index.md?format=TEXT (rendered page https://www.chromium.org/developers/design-documents/multi-process-architecture/ also saved) | chromium/website main @ `a88b32e46218523463a769f0ecfcb4da46649ce5` | `S/C-plain-1/website_multi-process-architecture_index.md`, `S/C-plain-1/chromiumorg-multi-process-architecture.{html,txt}` |
| C-plain-1, C-plain-6 | 9 | Debian binary package `chromium` 150.0.7871.181-1~deb13u1 (trixie, amd64) — file list and `/usr/bin/chromium` | https://deb.debian.org/debian/pool/main/c/chromium/chromium_150.0.7871.181-1~deb13u1_amd64.deb (index: https://deb.debian.org/debian/dists/trixie/main/binary-amd64/Packages.xz) | .deb SHA256 `581780e30ef1c04cefcb3eef2c754b80fad8654c38255feb2f957d0cb1a199fa` (matches Packages index); .deb deleted after listing | `S/C-plain-1/chromium_150.0.7871.181-1~deb13u1_amd64.filelist.txt`, `S/C-plain-1/chromium_150.0.7871.181-1~deb13u1_usr_bin_chromium.sh`, `S/C-plain-1/trixie-main-amd64-Packages.xz` |
| C-plain-1, C-plain-6 | 10 | Wine source, tag `wine-11.17` | https://gitlab.winehq.org/wine/wine.git (shallow clone of tag; raw files via https://gitlab.winehq.org/wine/wine/-/raw/36b6a2cf679fb395f668a917b76537190e212d9c/<path>) | tag `wine-11.17` = commit `36b6a2cf679fb395f668a917b76537190e212d9c` (2026-09-04) | `S/C-plain-6/wine-11.17-excerpts/` (whole files: `dlls_ntdll_unix_env.c`, `dlls_ntdll_unix_process.c`, `dlls_ntdll_unix_loader.c`, `dlls_ntdll_unix_thread.c`, `dlls_ntdll_thread.c`, `dlls_ntdll_exception.c`, `include_winternl.h`, `dlls_kernelbase_thread.c`, `loader_preloader.c`, `programs_wineboot_wineboot.c`, `programs_services_services.c`, `dlls_win32u_winstation.c`, `loader_wine.inf.in`, `dlls_rpcrt4_rpc_server.c`) |
| C-plain-1, C-plain-6 | 11 | Proton, tag `proton-11.0-2` (`proton`, `toolmanifest_x86_64.vdf`, `steam_helper/steam.c`) | https://raw.githubusercontent.com/ValveSoftware/Proton/proton-11.0-2/<path> | tag → commit `db9e6ffbf24a95b104fb699dd62532c70a2f9a51` (release published 2026-08-21); `wine` submodule pinned at `dc26e61847081a1b5cb0733dc30feba6ee575482` | `S/C-plain-6/proton-11.0-2/` |
| C-plain-1, C-plain-6 | 12 | Valve's Wine fork at the Proton 11.0-2 submodule commit (`dlls/ntdll/unix/env.c`, `dlls/ntdll/unix/thread.c`, `loader/preloader.c`) | https://raw.githubusercontent.com/ValveSoftware/wine/dc26e61847081a1b5cb0733dc30feba6ee575482/<path> | `dc26e61847081a1b5cb0733dc30feba6ee575482` (2026-08-03) | `S/C-plain-6/valve-wine-dc26e61847081a1b5cb0733dc30feba6ee575482/` |
| C-plain-1, C-plain-6 | 13 | Linux man-pages `PR_SET_NAME(2const)` | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man2const/PR_SET_NAME.2const?id=73ec1f03be502afc79db4c8f5eb18a045b0e8f48 | last commit touching file `73ec1f03be502afc79db4c8f5eb18a045b0e8f48` (byte-identical to master at retrieval) | `S/C-plain-6/PR_SET_NAME.2const` |
| C-plain-6 | 14 (added) | steam-runtime-tools (`docs/steam-compat-tool-interface.md`, `pressure-vessel/wrap.1.md`, `pressure-vessel/adverb.1.md`, `pressure-vessel/meson.build`, `bin/meson.build`) | https://gitlab.steamos.cloud/steamrt/steam-runtime-tools.git | tag `v0.20260903.0` = `06a2477429fe271c5b254399caffdab8b7737e99` (2026-09-03) | `S/C-plain-6/steam-runtime-tools/` |
| C-plain-2, C-plain-3 |  | Debian 13 archive index | https://deb.debian.org/debian/dists/trixie/Release , .../trixie/main/binary-amd64/Packages.xz | Release file: "Version: 13.7", "Date: Sat, 12 Sep 2026 07:55:41 UTC" | S/C-plain-3/debian-trixie-* |
| C-plain-2, C-plain-3 |  | Debian 12 archive index | https://deb.debian.org/debian/dists/bookworm/Release , .../bookworm/main/binary-amd64/Packages.xz | "Version: 12.15" | S/C-plain-3/debian-bookworm-* |
| C-plain-2, C-plain-3 |  | Ubuntu 24.04 archive index | http://archive.ubuntu.com/ubuntu/dists/noble{,-updates}/{main,universe}/binary-amd64/Packages.xz | noble, noble-updates as of retrieval | S/C-plain-3/ubuntu-noble-* |
| C-plain-2, C-plain-3 |  | clamav, clamav-base, clamav-daemon, clamav-freshclam (Debian 13) | https://deb.debian.org/debian/pool/main/c/clamav/ | 1.4.3+dfsg-1 | S/C-plain-2/debs/, extracted to S/C-plain-2/x/ |
| C-plain-2, C-plain-3 |  | clamav Debian source packaging | https://deb.debian.org/debian/pool/main/c/clamav/clamav_1.4.3+dfsg-1.debian.tar.xz | 1.4.3+dfsg-1 (sha256 03ba75f8…18ff, matching the .dsc) | S/C-plain-2/debian-source/debian/ |
| C-plain-2, C-plain-3 |  | clamav, clamav-daemon, clamav-freshclam (Ubuntu 24.04 updates) | http://archive.ubuntu.com/ubuntu/pool/main/c/clamav/ | 1.5.3+dfsg-0ubuntu0.24.04.1 | S/C-plain-2/debs/, S/C-plain-2/x/ |
| C-plain-2, C-plain-3 |  | init-system-helpers (the `update-rc.d` script) | https://deb.debian.org/debian/pool/main/i/init-system-helpers/init-system-helpers_1.69~deb13u1_all.deb | 1.69~deb13u1 | S/C-plain-2/x/init-system-helpers_1.69~deb13u1_all/ |
| C-plain-2, C-plain-3 |  | ClamAV official documentation source | https://github.com/Cisco-Talos/clamav-documentation.git | commit 26dceb239dff15088c5b04b469fd056d1933548b (2026-08-07) | S/C-plain-2/clamav-documentation/ |
| C-plain-2, C-plain-3 |  | Fedora clamav packaging | https://src.fedoraproject.org/rpms/clamav.git | commit 110ace5be45f538ef3689b548a220bffa1ad5e6f (2026-09-10), spec Version 1.4.6 Release 2 | S/C-plain-2/fedora/clamav-rpm/ |
| C-plain-2, C-plain-3 |  | tracker-extract, which ships localsearch (Debian 13) | https://deb.debian.org/debian/pool/main/t/tracker-miners/tracker-extract_3.8.2-4+b1_amd64.deb | 3.8.2-4+b1 | S/C-plain-3/debs/, S/C-plain-3/x/ |
| C-plain-2, C-plain-3 |  | tracker-miner-fs (Debian 13, transitional) | .../tracker-miner-fs_3.8.2-4_all.deb | 3.8.2-4 | same |
| C-plain-2, C-plain-3 |  | tracker-miner-fs (Debian 12) | https://deb.debian.org/debian/pool/main/t/tracker-miners/tracker-miner-fs_3.4.3-1_amd64.deb | 3.4.3-1 | same |
| C-plain-2, C-plain-3 |  | tracker-miner-fs (Ubuntu 24.04 updates) | http://archive.ubuntu.com/ubuntu/pool/main/t/tracker-miners/tracker-miner-fs_3.7.1-1ubuntu0.1_amd64.deb | 3.7.1-1ubuntu0.1 | same |
| C-plain-2, C-plain-3 |  | GNOME LocalSearch upstream | https://gitlab.gnome.org/GNOME/localsearch.git | tag 3.8.2 → commit ec1fb9abf8223c37cddc141567b2c6650d4ee6e3 | S/C-plain-3/localsearch-3.8.2/ |
| C-plain-2, C-plain-3 |  | baloo6 (Debian 13) | https://deb.debian.org/debian/pool/main/k/kf6-baloo/baloo6_6.13.0-1_amd64.deb | 6.13.0-1 | S/C-plain-3/debs/, S/C-plain-3/x/ |
| C-plain-2, C-plain-3 |  | baloo-kf5 (Debian 12) | https://deb.debian.org/debian/pool/main/b/baloo-kf5/baloo-kf5_5.103.0-2_amd64.deb | 5.103.0-2 | same |
| C-plain-2, C-plain-3 |  | KDE Baloo upstream | https://invent.kde.org/frameworks/baloo.git (git clone; the `-/raw/` web URLs returned HTTP 403) | tag v6.13.0 → commit 652de972bf24d4ab9d6ddb1f1e9e88d300375b0e | S/C-plain-3/kde-src/baloo/ |
| C-plain-2, C-plain-3 |  | plocate (Debian 13) | https://deb.debian.org/debian/pool/main/p/plocate/plocate_1.1.23-1_amd64.deb | 1.1.23-1 | S/C-plain-3/debs/, S/C-plain-3/x/ |
| C-plain-2, C-plain-3 |  | plocate (Ubuntu 24.04, universe) | http://archive.ubuntu.com/ubuntu/pool/universe/p/plocate/plocate_1.1.19-2ubuntu2_amd64.deb | 1.1.19-2ubuntu2 | same |
| C-plain-2, C-plain-3 |  | Linux man-pages | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_stat.5?id=adb436b2… (also proc_pid_comm.5, man2const/PR_SET_NAME.2const) | tag man-pages-6.19 → commit adb436b2e4471218021d86f188fb58dec3946eb8 | S/C-plain-3/man-pages/ |
| C-plain-4, C-plain-5 | 1 | jellyfin-ffmpeg8 Debian package (trixie, amd64): control + file list | https://github.com/jellyfin/jellyfin-ffmpeg/releases/download/v8.1.2-4/jellyfin-ffmpeg8_8.1.2-4-trixie_amd64.deb | release v8.1.2-4 (published 2026-09-06); .deb sha256 783568b3…b2a8a5 (deb removed after listing) | S/C-plain-4/deb/control/, S/C-plain-4/deb-filelist.txt, S/C-plain-4/jellyfin-ffmpeg8_8.1.2-4-trixie_amd64.deb.sha256 |
| C-plain-4, C-plain-5 | 2 | jellyfin-ffmpeg source repo | https://github.com/jellyfin/jellyfin-ffmpeg | tag v8.1.2-4 = 6c051dec38eb0e88d2d4d3c54b13014bf69f9799 | S/C-plain-4/jellyfin-ffmpeg-v8.1.2-4/ |
| C-plain-4, C-plain-5 | 3 | Jellyfin server source | https://github.com/jellyfin/jellyfin | tag v12.0 (release 2026-09-08) = 6c073e19ddf604b2369c638716164fdab4c952dc | S/C-plain-4/jellyfin-v12.0/ |
| C-plain-4, C-plain-5 | 4 | Jellyfin official packaging (deb defaults, systemd unit, Dockerfile) | https://github.com/jellyfin/jellyfin-packaging | tag v12.0-202609072105 = b19fe6435f9a972106364f3cc6f7df21348b7493 | S/C-plain-4/jellyfin-packaging-v12.0/ |
| C-plain-4, C-plain-5 | 5 | Jellyfin web client (library-options form defaults) | https://github.com/jellyfin/jellyfin-web | tag v12.0 = 0e83c6a724b31f3e9b5a499244331a288c060a4a | S/C-plain-4/jellyfin-web-v12.0/ |
| C-plain-4, C-plain-5 | 6 | Jellyfin official docs | https://github.com/jellyfin/jellyfin.org | main @ 1edeb876d1a197de6ead0148ca32e4ae241a6f2d (2026-09-10) | S/C-plain-4/jellyfin.org-docs/ |
| C-plain-4, C-plain-5 | 7 | Linux kernel fs/exec.c, fs/binfmt_script.c | https://raw.githubusercontent.com/torvalds/linux/v6.16/fs/exec.c (and …/binfmt_script.c) | tag v6.16 | S/C-plain-4/linux-v6.16-fs-exec.c, S/C-plain-4/linux-v6.16-fs-binfmt_script.c |
| C-plain-4, C-plain-5 | 8 | man-pages proc_pid_comm(5) | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_comm.5?h=man-pages-6.9 | requested ref man-pages-6.9; file header reads `"Linux man-pages (unreleased)"` (source placeholder) | S/C-plain-4/man-pages-proc_pid_comm.5 |
| C-plain-4, C-plain-5 | 9 | Debian 13 "trixie" Release + main/binary-amd64 Packages index | https://deb.debian.org/debian/dists/trixie/Release, …/main/binary-amd64/Packages.xz | Release "Version: 13.7", "Date: Sat, 12 Sep 2026 07:55:41 UTC" | S/C-plain-5/debian-trixie-Release, S/C-plain-5/debian-trixie-main-amd64-Packages |
| C-plain-4, C-plain-5 | 10 | Debian trixie main Contents-amd64.gz (filtered extracts) | https://deb.debian.org/debian/dists/trixie/main/Contents-amd64.gz | md5 28de400dfa7efef5fa35072adedede3d (matches Release); full file deleted after filtering | S/C-plain-5/debian-trixie-main-amd64-Contents-{timers,cron,xdg-autostart,systemd-user}.txt |
| C-plain-4, C-plain-5 | 11 | Debian packages deja-dup 45.2-3+b1, timeshift 24.06.6-2, dpkg 1.22.22, kup-backup 0.10.0-1+b1, ffmpegthumbnailer 2.2.3-2, totem 43.2-3 (amd64) | https://deb.debian.org/debian/pool/main/… (Filename fields of the Packages index) | sha256 in S/C-plain-5/debs.sha256 | S/C-plain-5/<pkg>_<ver>_amd64/ and *.filelist.txt |
| C-plain-4, C-plain-5 | 12 | Déjà Dup upstream source (monitor, libdeja) | https://gitlab.gnome.org/World/deja-dup/-/raw/45.2/… | tag 45.2 = 585b723da27fdc6ad5c2a3b27858fdc9056f0038 | S/C-plain-5/deja-dup-45.2-*.vala, S/C-plain-5/deja-dup-45.2-monitor-README.md |
| C-plain-4, C-plain-5 | 13 | Timeshift upstream source | https://github.com/linuxmint/timeshift | tag 24.06.6 → commit 36429afa9aa37f3e9c4a621fd71b674eb3fc2d7a | S/C-plain-5/timeshift-24.06.6/ |
| C-plain-4, C-plain-5 | 14 | Plex Media Server .deb (control, file list, systemd unit) | https://downloads.plex.tv/plex-media-server-new/1.43.4.10903-e5521bd8c/debian/plexmediaserver_1.43.4.10903-e5521bd8c_amd64.deb (from https://plex.tv/api/downloads/5.json) | 1.43.4.10903-e5521bd8c; sha1 15b047e6eae77bbbc61573ae8bf728fdcc0e40f5 (matches vendor JSON); deb removed after listing | S/C-plain-5/plex-deb/, S/C-plain-5/plexmediaserver_1.43.4.10903-e5521bd8c_amd64.filelist.txt, S/C-plain-5/plex-downloads-5.json |
| C-plain-4, C-plain-5 | 15 | Plex Support "Scheduled Tasks" | https://support.plex.tv/articles/201553286-scheduled-tasks/ | page "Last modified on: July 31, 2025" | S/C-plain-5/plex-support-201553286-scheduled-tasks.{html,txt} |
| C-plain-4, C-plain-5 | 16 | Immich (vendor ML service) compose, ML Dockerfile, ML README, ML main.py | https://raw.githubusercontent.com/immich-app/immich/v3.2.0/… | tag v3.2.0 = 1b6098c9dbfffe978bec2d414606ed7a4c8e019a | S/C-plain-5/immich-v3.2.0/ |
| C-plain-7, C-plain-8, C-plain-9 | 1 | Google cluster-data repo | https://github.com/google/cluster-data | commit `48b12446464b0422abcc18e0ec5b0b13e2f3a90c` (2026-08-07) | `S/C-plain-7/cluster-data/` |
| C-plain-7, C-plain-8, C-plain-9 | 2 | Google cluster-usage traces v3 (2019) doc | https://drive.usercontent.google.com/download?id=10r6cnJ5cJ89fPWCgj7j4LtLBqYN9RiI9 (linked from ClusterData2019.md) | "Original version 2020-04-01, updated … 2020-08-18" | `S/C-plain-7/google-2019-v3-doc.pdf` / `.txt` |
| C-plain-7, C-plain-8, C-plain-9 | 3 | Google cluster-usage traces format + schema (2011, v2.1) | https://drive.usercontent.google.com/download?id=0B5g07T_gRDg9Z0lsSTEtTWtpOW8 (linked from ClusterData2011_2.md) | "Version of 2013-05-06 … Revised 2014-11-17 for trace version 2.1" | `S/C-plain-7/google-2011-v2.1-schema.pdf` / `.txt` |
| C-plain-7, C-plain-8, C-plain-9 | 4 | Google clusterdata-2011-2 schema.csv | https://storage.googleapis.com/clusterdata-2011-2/schema.csv | bucket object as served | `S/C-plain-7/google-2011-2-schema.csv` |
| C-plain-7, C-plain-8, C-plain-9 | 5 | Azure/AzurePublicDataset repo | https://github.com/Azure/AzurePublicDataset | commit `207bed67dd10090b28ad4f745b2cfd41a11aace4` (2026-06-03) | `S/C-plain-7/AzurePublicDataset/` |
| C-plain-7, C-plain-8, C-plain-9 | 6 | LANL "Comprehensive, Multi-Source Cyber-Security Events" page | https://csr.lanl.gov/data/cyber1/ | page as served | `S/C-plain-7/lanl-cyber1.html` / `.txt` |
| C-plain-7, C-plain-8, C-plain-9 | 7 | LANL "Unified Host and Network Data Set" page | https://csr.lanl.gov/data/2017/ | page as served | `S/C-plain-7/lanl-2017.html` / `.txt` |
| C-plain-7, C-plain-8, C-plain-9 | 8 | Turcotte, Kent, Hash, "Unified Host and Network Data Set" | https://arxiv.org/abs/1708.07518 (PDF /pdf/1708.07518) | arXiv v1, 2017-08-24 | `S/C-plain-7/turcotte-1708.07518.pdf` / `.txt` |
| C-plain-7, C-plain-8, C-plain-9 | 9 | DARPA OpTC data release docs (FiveDirections/OpTC-data) | https://github.com/FiveDirections/OpTC-data | commit `5b108604f11f767aa11ea79ff827595f3fad15fd` (2020-06-17) | `S/C-plain-7/OpTC-data/` |
| C-plain-7, C-plain-8, C-plain-9 | 10 | BEHACOM (Data in Brief 31, 105767, doi:10.1016/j.dib.2020.105767) | https://pmc.ncbi.nlm.nih.gov/articles/PMC7270191/ | PMC HTML as served | `S/C-plain-7/behacom-pmc7270191.html` / `.txt` |
| C-plain-7, C-plain-8, C-plain-9 | 11 | Phoronix Test Suite README + documentation | https://raw.githubusercontent.com/phoronix-test-suite/phoronix-test-suite/v10.8.4/README.md and …/documentation/phoronix-test-suite.md | tag `v10.8.4` = commit `f0365737ae42c2a4ae80c28491a8c0ac22a10f3c` (2022-07-03; highest version tag in `git ls-remote`) | `S/C-plain-8/pts-v10.8.4/` |
| C-plain-7, C-plain-8, C-plain-9 | 12 | byte-unixbench | https://github.com/kdlucas/byte-unixbench | commit `e949d4402f76b4bc9b7b114418faace882f0ef12` (2026-05-19) | `S/C-plain-8/byte-unixbench/` |
| C-plain-7, C-plain-8, C-plain-9 | 13 | LSApp | https://github.com/aliannejadi/LSApp | commit `c001713b5c9f56069d48ecb3128da53f0fdd9534` (2021-07-16) | `S/C-plain-8/LSApp/` |
| C-plain-7, C-plain-8, C-plain-9 | 14 | Tsinghua App Usage dataset page | https://fi.ee.tsinghua.edu.cn/appusage/ | page as served | `S/C-plain-8/tsinghua-appusage.html` / `.txt` |
| C-plain-7, C-plain-8, C-plain-9 | 15 | LiveLab traces page | http://livelab.recg.rice.edu/traces.html → redirected to https://yecl.org/livelab/ ; traces page fetched at https://yecl.org/livelab/traces.html | "last updated on 7/15/2012" | `S/C-plain-8/livelab-traces.html` / `.txt` |
| C-plain-7, C-plain-8, C-plain-9 | 16 | Carat Top 1000 Users dataset page | https://www.cs.helsinki.fi/group/carat/data-sharing/ | page as served | `S/C-plain-8/carat-data-sharing.html` |
| C-plain-7, C-plain-8, C-plain-9 | 17 | Li, Dolan-Gavitt, Weber, Cappos, "Lock-in-Pop", USENIX ATC '17 | https://www.usenix.org/system/files/conference/atc17/atc17-li_yiwen.pdf | USENIX open-access proceedings PDF | `S/C-plain-9/atc17-li_yiwen.pdf` / `.txt` |
| C-plain-7, C-plain-8, C-plain-9 | 18 | Lamprou et al., "The Koala Benchmarks for the Shell", USENIX ATC '25 | https://www.usenix.org/system/files/atc25-lamprou.pdf | USENIX open-access proceedings PDF | `S/C-plain-9/atc25-lamprou.pdf` / `.txt` |
| C-plain-7, C-plain-8, C-plain-9 | 19 | Popescu & Lopes, "Exploiting Undefined Behavior in C/C++ Programs for Optimization", PACMPL 9 (PLDI), Article 161 | https://web.ist.utl.pt/nuno.lopes/pubs/ub-pldi25.pdf (publisher PDF https://dl.acm.org/doi/pdf/10.1145/3729260 returned HTTP 403) | author-hosted copy carrying PACMPL running heads "161:n" and CC-BY 4.0 notice | `S/C-plain-9/ub-pldi25-lopes.pdf` / `.txt` |
| C-plain-7, C-plain-8, C-plain-9 | 20 | Gamess & Hernandez, IJACSA 13(2), 2022 | http://thesai.org/Downloads/Volume13No2/Paper_95-Performance_Evaluation_of_Different_Raspberry_Pi_Models.pdf | journal PDF | `S/C-plain-9/ijacsa-2022-130295.pdf` / `.txt` |
| C-plain-7, C-plain-8, C-plain-9 | 21 | OpenAlex full-text search result (discovery aid only, not evidence) | https://api.openalex.org/works?filter=fulltext.search:"github.com/phoronix-test-suite" | response 2026-09-13 | `S/C-plain-9/openalex-github_com_phoronix-test-suite.json` |
| C-plain-7, C-plain-8, C-plain-9 | 22 | arXiv 2305.04641 and 2401.10582 (preprints; not counted as peer-reviewed) | https://arxiv.org/pdf/2305.04641 , https://arxiv.org/pdf/2401.10582 | as served | `S/C-plain-9/arxiv-2305.04641.*`, `S/C-plain-9/arxiv-2401.10582.*` |

---

## Source: focal-arxiv26

Copies used for this source (all retrieved 2026-09-13; local root `_dev/research/jioh/2026-09-13-verification/sources/focal-arxiv26/`):

- arXiv abstract page https://arxiv.org/abs/2604.19541 → `abs.html`; https://arxiv.org/abs/2604.19541v1 → `abs-v1.html`
- v2 PDF https://arxiv.org/pdf/2604.19541v2 (arXiv GenPDF, PDF CreationDate 2026-07-21) → `v2.pdf`, text `v2.txt`
- v1 PDF https://arxiv.org/pdf/2604.19541v1 (PDF CreationDate 2026-04-22) → `v1.pdf`, text `v1.txt`
- v2 author TeX source https://arxiv.org/src/2604.19541v2 → `src-v2/sample-sigconf-authordraft.tex` (+ `src-v2/figures/Data_contruction_2.png`)
- DesktopBench dataset repo https://huggingface.co/datasets/HaoranYin/desktopbench, git clone at commit `49c3683061073ecf8cfadf962ce5d563a2e1dd43` ("Initial public release", 2026-07-19), which is the target of annotated tag `v0.1.0` → `hf-desktopbench/`; HF API JSON → `hf-dataset-api.json`
- Companion code repo metadata https://api.github.com/repos/Haoran2099/focal → `gh-focal-repo.json` (not cloned; metadata only)

**v1 vs v2.** A word-level diff of the extracted text of v1 and v2 shows only three differences: v1 marks "Cao∗" with a "∗Corresponding author." footnote, and the arXiv side-stamp reads `arXiv:2604.19541v1 [cs.MA] 21 Apr 2026` (v1) vs `arXiv:2604.19541v2 [cs.MA] 18 Jul 2026` (v2). Every passage quoted below is therefore present in both versions. Quotes are copied from the v2 TeX source (the PDF text extraction drops inter-word spaces); PDF page locators are given for the v2 PDF.

### C-focal-1 — Interruption split: session count, session structure, primary and interrupting activities

(a) Verbatim.

TeX line 457 (PDF p. 4, §4 intro):
> DesktopBench has two splits: \textbf{DesktopBench-Multitask} for interleaved cross-application workflows and \textbf{DesktopBench-Interruption} for controlled $A\!\rightarrow\!B\!\rightarrow\!A$ timelines that test whether a method can preserve and resume task state after interruption.

TeX lines 507–508 (PDF pp. 4–5, §4.1):
> \textit{DesktopBench-Interruption (100 sessions).}
> To evaluate robustness to context switching, we construct an $A\!\rightarrow\!B\!\rightarrow\!A$ split in which a long-running creative task~$A$ is interrupted by a short YouTube browsing task~$B$ before resuming. This tests whether a model can preserve and recover the latent state of task~$A$ without cross-task drift.

TeX lines 517–518 (PDF p. 5, §4.3):
> It contains 420 sessions in total: 320 in DesktopBench-Multitask and 100 in DesktopBench-Interruption. Multitask sessions contain 2--4 tasks, while Interruption sessions contain exactly two tasks under the $A\!\rightarrow\!B\!\rightarrow\!A$ structure.
> Table~\ref{tab:dataset} summarizes the key statistics. The average session length is 17.3 actions for DesktopBench-Multitask and 16.5 for DesktopBench-Interruption.

Figure 3 caption (TeX line 540, PDF p. 6): `(d)~Interrupted task distribution. (e)~Actions per segment (Interruption).` Panel (e) x-axis labels in the PDF text layer: `A-pre YouTube A-post`.

Released generator `hf-desktopbench/scripts/provenance/generate_videogui_youtube_aba_sessions.py` (commit 49c3683), lines 51–56 and 59–64:
```python
def choose_split_point(action_count: int) -> int:
    if action_count < 4:
        raise ValueError("A-B-A sessions require at least 4 actions in the interrupted task.")
    if action_count == 4:
        return 2
    return action_count // 2
```
```python
    youtube_tasks = [task for task in tasks if task["prefix"] == "YT"]
    interruptable_tasks = [task for task in tasks if task["prefix"] != "YT" and task["action_count"] >= 4]

    if not youtube_tasks:
        raise RuntimeError("No YouTube subtasks found in the source data.")
    if len(interruptable_tasks) < target_sessions:
        raise RuntimeError("Not enough interruptable tasks to build the requested number of A-B-A sessions.")
```
Same file, lines 69–70:
```python
    interruptable_tasks.sort(key=lambda item: (-item["action_count"], item["task_uid"]))
    selected_a_tasks = interruptable_tasks[:target_sessions]
```

Released data `hf-desktopbench/data/interruption_sessions/train.jsonl`, first row, verbatim:
```json
{"scenario": "a_to_youtube_to_a", "segments": [{"action_indices": [18, 19, 20, 21, 22, 23, 24, 25, 26], "subtask_id": 3, "task_id": "PS_03"}, {"action_indices": [0, 1], "subtask_id": 0, "task_id": "YT_10"}, {"action_indices": [27, 28, 29, 30, 31, 32, 33, 34, 35, 36], "subtask_id": 3, "task_id": "PS_03"}], "session_id": "aba_session001"}
```
`hf-desktopbench/README.md`:
> The 100 interruption sessions materialize to 1,691 actions (16.91 per session).
> The paper text reports 16.5 for the latter average; `16.91` is the value computed
> from the released catalog and is recorded as a known discrepancy.

(b) Locators: arXiv:2604.19541v2 §4 intro, §4.1, §4.3, Table 3, Fig. 3(d)(e) (PDF pp. 4–6); TeX source lines as given; DesktopBench v0.1.0 files as given.

(c) Reading. The Interruption split has **100 sessions**. Each is an A→B→A timeline: one task A, interrupted by a short YouTube browsing task B, then A resumes; the paper counts this as exactly two tasks (three segments: A-pre, YouTube, A-post). The paper calls A "a long-running creative task". In the released generator, A is any non-YouTube VideoGUI subtask with ≥4 actions, taking the 100 longest; A is split at ⌊n/2⌋ actions (2 if n = 4); B is one YouTube (`YT`) VideoGUI subtask, chosen to balance reuse. My own count over the released `interruption_sessions` file (python): all 100 rows have 3 segments, segment 2 is always a `YT_*` subtask, segments 1 and 3 are always the same task/subtask; A-pre 4–18 actions (mean 6.15), YouTube 2–10 (mean 4.17), A-post 4–18 (mean 6.59); A prefixes: PPT 23, PS 16, AE 16, RW 12, WEB 10, VLC 7, CC 4, DV 4, PR 3, SD 3, AI 2. Caveats: (1) 17 of the 100 A tasks are `WEB`/`VLC`, which the paper's own Table 2 files under the "Reference" family ("Tutorials, asset browsing"), not a creative/editing family — so "creative task" does not hold for every session in the release. (2) Average length: paper 16.5, released catalog 16.91 (the release itself flags this). (3) The generator's internal record says `"task_count": 3` for each A-B-A session (it counts segments), while the paper says exactly two tasks.

(d) Verdict: **FOUND**.

### C-focal-2 — Multitask split: session count, template count, fields each recorded action carries

(a) Verbatim.

TeX line 501 (PDF p. 4, §4.1):
> Because VideoGUI was built for single-task automation, it lacks the session organization and metadata required for activity logging. We therefore augment each action with the foreground application name (\texttt{app}) and window title (\texttt{title}), while retaining the original task descriptions as semantic reference (Figure~\ref{fig:dataset_construction}).

TeX lines 505–506 (PDF p. 4, §4.1):
> \textit{DesktopBench-Multitask (320 sessions).}
> Sessions are assembled through template-based composition grounded in realistic creative workflows. We use 20 patterns spanning video-centric workflows such as \texttt{video$\to$ref$\to$video} and design-centric workflows such as \texttt{generation$\to$image$\to$slide}. Each session contains at least two distinct application prefixes, and compatible subtasks may be reused to compose richer workflows.

TeX lines 324–332, §3.2 problem formulation (PDF p. 3, eqs. 1–2):
```latex
We model a \textit{session} as an ordered desktop interaction sequence generated within one continuous working context, consisting of $N$ actions:
\begin{equation}
    \mathcal{S} = \{(m_i, v_i)\}_{i=1}^{N}
\end{equation}
where each action contains structured metadata
\begin{equation}
    m_i = (\text{app}_i,\ \text{title}_i)
\end{equation}
and a screenshot $v_i \in \mathbb{R}^{H \times W \times 3}$. A session contains $K$ latent \textit{tasks}; each action is associated with a task id $y_i \in [1, K]$. Define the action-index set of task $k$ as
```

Table 3 (PDF p. 5), text layer:
> Number of sessions 320 100
> Average session length (actions) 17.3 16.5
> Task count per session 2–4 2

Figure 2 (`src-v2/figures/Data_contruction_2.png`, image text, transcribed from the image — not a text layer): middle panel "Metadata Annotation": "1. Collect one screenshot at a time from the raw screen recording dataset", "2. Identify the active application and its window title from the screenshot", "3. Output structured Result"; example table with columns "Task | app | title" and rows "PPT_12_0 | PowerPoint | project - Saved to this PC", "SD_7_2 | Chrome | Stable Diffusion"; right panel "Human Verification & Session Assembly".

Released generator `hf-desktopbench/scripts/provenance/generate_videogui_multitask_sessions.py` lines 20–44 define `VIDEO_PATTERNS` with 9 entries (`video_ref`, `ref_video`, `video_ref_video`, `ref_video_video`, `generation_video`, `video_generation`, `ref_video_generation`, `generation_ref_video`, `ref_video_video_generation`) and `DESIGN_PATTERNS` with 11 entries (`image_slide`, `slide_image`, `reference_image`, `reference_slide`, `reference_image_slide`, `image_reference_slide`, `slide_reference_image`, `generation_image`, `generation_image_slide`, `reference_generation_slide`, `reference_image_slide_generation`); e.g. line 21:
```python
    ("video_ref", ["editing_video", "reference"], 0.7),
```
Same file lines 360–361:
```python
    parser.add_argument("--target-sessions", type=int, default=320)
    parser.add_argument("--seed", type=int, default=20260324)
```

Released annotation file `hf-desktopbench/data/active_window_annotations/train.jsonl`, first row verbatim:
```json
{"app": "Adobe After Effects 2023", "image_id": "AE_0_action000", "label_source": "ollama_vlm", "title": "project (converted).aep"}
```
`hf-desktopbench/scripts/provenance/annotate_active_window_with_ollama.py` lines 2–9:
```
"""Annotate active window app/title for screenshots using an Ollama VLM.

Output fields per image:
- image_id: e.g. PPT_14_action004
- app: normalized app name from allowed list
- title: active window title (browser tab title or project/file name)
- screenshot_path
- file_name
```
`hf-desktopbench/README.md` table row and limitation:
> | `active_window_annotations` | 2,572 | Stable image IDs and project-generated app/title labels |

> - App/title and summary labels are model-generated and can contain errors.

`hf-desktopbench/scripts/prepare_videogui_raw_from_hf.py` (runtime reconstruction) lines 11–20:
```
Each output record corresponds to one atomic action with fields required by
FOCAL experiments:
- timestamp (ISO 8601)
- app
- title
- duration
- kpm
- cpm
- screenshot_path
- gt_task_id / gt_subtask_id / gt_subtask_query
```
and `scripts/rebuild_desktopbench.py` line 13:
```python
DROP_FIELDS = {"timestamp", "duration", "kpm", "cpm", "screenshot_paths"}
```

(b) Locators: arXiv:2604.19541v2 §3.2 eq. (1)–(2) (p. 3), §4.1 (p. 4), Table 3 (p. 5), Figure 2 (p. 5); TeX lines as given; DesktopBench v0.1.0 files at commit 49c3683.

(c) Reading. **320 sessions**; each has 2–4 tasks and at least two distinct application prefixes; mean 17.3 actions (the release computes 5,540 actions / 320 = 17.3125). The paper says "template-based composition" and **20 patterns**; the released generator indeed holds 20 (9 video-band + 11 design-band), each a weighted sequence of application families, and it also forbids repeating a prefix within a session. Per action, the paper's model input is **(app, title) metadata plus one screenshot**, with the original VideoGUI task description retained as a semantic reference; the ground-truth task id is the label. Caveats on the word "recorded": (1) `app`/`title` were not captured from the OS — the release says they are VLM-generated from each screenshot (`label_source: "ollama_vlm"`, script default model `qwen3-vl:8b`), and Figure 2 says "Identify the active application and its window title from the screenshot"; the paper's wording "augment each action with the foreground application name … and window title" does not say this. (2) In the full runtime reconstruction each record also carries the upstream VideoGUI action payload (`action_id`, `action_type`, `start_position`, `action_narration`), `subtask_query`, `action_sequence`, and ground-truth task ids, while `timestamp`, `duration`, `kpm`, `cpm` are dropped (see C-focal-4). (3) No per-action process/PID/CPU field exists anywhere in the paper or release.

(d) Verdict: **FOUND** (template count is stated as "20 patterns").

### C-focal-3 — How sessions were produced (recorded natural use vs constructed) and from which dataset

(a) Verbatim.

TeX line 265 (PDF p. 2, §1):
> To validate FOCAL, we conduct experiments on DesktopBench, reconstructed from VideoGUI, with both multi-task sessions and interruption scenarios.

TeX line 456 (PDF p. 4, §4):
> We reconstruct \textbf{VideoGUI}~\citep{lin2024videogui} into \textbf{DesktopBench}, a benchmark for multi-task desktop activity logging. Following Table~\ref{tab:task_family}, we regroup its source tasks into five application families spanning editing, generation, slides, and reference activities.

TeX line 518 (PDF p. 5, §4.3):
> Because compatible source subtasks may be reused when composing workflows, these counts measure instantiated actions with multiplicity rather than unique screenshots.

Figure 2 `\Description` (TeX line 495):
> Diagram showing the dataset construction pipeline from original VideoGUI subtasks to Multi-task and Interruption session splits.

`hf-desktopbench/README.md`:
> Reconstruction is pinned to:
>
> - `VideoGUI/VideoGUI-Mid-Plan@6852d8c9f2b9c586d7ff7cce2611080140f1a30c`
> - `VideoGUI/VideoGUI-Action@0a8110739acf4c766d4d55c9672cb38d1d9bfcbd`

`hf-desktopbench/scripts/prepare_videogui_raw_from_hf.py` lines 210–212 and 258:
```python
            for action_row in ordered_actions:
                app = str(mid_info.get("app") or action_row.get("app") or "Unknown")
                duration = 6.0
```
```python
                current_ts = current_ts + timedelta(seconds=duration)
```

(b) Locators: arXiv:2604.19541v2 §1 (p. 2), §4 and §4.1 (p. 4), §4.3 (p. 5); Fig. 2; DesktopBench v0.1.0 README and scripts at commit 49c3683.

(c) Reading. Sessions are **constructed, not recorded natural use**. The authors took single-task VideoGUI subtasks (screenshots of human re-enactments of YouTube tutorials — see C-videogui-1) and concatenated them: Multitask by sampling one of 20 family patterns, Interruption by splitting one subtask around a YouTube subtask. Source subtasks are reused across sessions (the paper says counts are "with multiplicity"). The source dataset is **VideoGUI** (Lin et al., NeurIPS 2024 D&B), specifically the Hugging Face `VideoGUI-Action` (2,572 rows at the pinned revision) and `VideoGUI-Mid-Plan` (462 rows) datasets. No inter-session or cross-subtask timing comes from real use; the runtime timeline is synthetic (fixed 6.0 s per action from a base timestamp), and even that is dropped.

(d) Verdict: **FOUND**.

### C-focal-4 — Release location, version, data licence, script licence; per-action timestamps

(a) Verbatim.

Paper: searched `v1.txt`, `v2.txt` and the v2 TeX source for `github`, `hugging`, `licen`, `release`, `zenodo`, `http`, `available`; and listed every link annotation in both PDFs. The only URLs are reference-list DOIs/URLs (NeurIPS, OpenAI docs, PMLR). The acknowledgments block in the TeX source (line 1220) reads `Omitted for anonymous review.` inside a disabled `\iffalse` (line 864) … `\fi` (line 1224) region, so it does not print. The arXiv licence field for the paper itself is `http://arxiv.org/licenses/nonexclusive-distrib/1.0/` (PDF metadata `/License`).

`hf-desktopbench/README.md` (commit 49c3683):
> DesktopBench is the benchmark used by
> [FOCAL: Filtered On-device Continuous Activity Logging for Efficient Personal
> Desktop Summarization](https://arxiv.org/abs/2604.19541). This public `v0.1.0`
> release contains only project-generated annotations, session constructions,
> ground-truth summaries, provenance, and deterministic reconstruction tools.
>
> It does **not** redistribute VideoGUI screenshots, image bytes, screenshot
> paths, or copied `raw_records` containing upstream action text. Complete runtime
> inputs are reconstructed locally from pinned upstream revisions.

> As of this release, the upstream Hugging Face dataset cards do not declare a
> data license. Access to this public repository does not grant any right to
> VideoGUI artifacts. Users must review and comply with upstream terms before
> downloading or using them.

> The companion [`Haoran2099/focal`](https://github.com/Haoran2099/focal)
> repository provides the supported wrapper:

> Scripts are MIT licensed under [LICENSE_CODE](LICENSE_CODE). The dataset itself
> is marked `license: other`; repository visibility does not grant a redistribution
> license for the annotations or GT. Cite the paper using
> [CITATION.cff](CITATION.cff).

`hf-desktopbench/DATA_TERMS.md`:
> The project-generated annotations, session mappings, and ground-truth summaries
> in this public `v0.1.0` release are available for research inspection. Public
> repository visibility is not a license grant: the dataset remains marked
> `license: other`, and no redistribution, sublicensing, or republication license
> is granted for annotations or ground-truth summaries unless separately
> authorized by the applicable rights holder.

`hf-desktopbench/LICENSE_CODE` lines 1–3:
> MIT License
>
> Copyright (c) 2026 HAORAN YIN

`hf-desktopbench/CITATION.cff`:
> version: 0.1.0
> date-released: 2026-07-19
> repository: "https://huggingface.co/datasets/HaoranYin/desktopbench"

`hf-desktopbench/manifests/upstream.json` (excerpt):
```json
      "license_declared_in_dataset_card": null,
      "repo_id": "VideoGUI/VideoGUI-Action",
      "revision": "0a8110739acf4c766d4d55c9672cb38d1d9bfcbd"
```

Timestamps: `scripts/prepare_videogui_raw_from_hf.py` line 212 `duration = 6.0`, line 237 `"timestamp": current_ts.isoformat(),`, line 258 `current_ts = current_ts + timedelta(seconds=duration)`, lines 283–286:
```python
        "--base-timestamp",
        type=str,
        default="2026-01-01T08:00:00+00:00",
        help="ISO 8601 base timestamp for sequential assignment",
```
`scripts/rebuild_desktopbench.py` line 13 and line 76:
```python
DROP_FIELDS = {"timestamp", "duration", "kpm", "cpm", "screenshot_paths"}
```
```python
        updated = {key: value for key, value in row.items() if key not in DROP_FIELDS}
```
Upstream `VideoGUI/VideoGUI-Action` dataset card at revision 0a81107 (`sources/videogui-arxiv24/hf-VideoGUI-Action-README.md`) lists features `split, app, screenshot_start, action_type, action_narration, start_position, end_position, scroll_value, task_id, subtask_id, action_id` — no time field.

GitHub API for `Haoran2099/focal` (`gh-focal-repo.json`): `created_at` 2026-07-19T11:33:21Z, `license.spdx_id` `MIT`.

(b) Locators: as given; DesktopBench HF repo commit `49c3683061073ecf8cfadf962ce5d563a2e1dd43`, tag `v0.1.0` (annotated tag object pointing at that commit).

(c) Reading. The **paper does not state any release location, version or licence** for DesktopBench. The release exists separately: **Hugging Face dataset `HaoranYin/desktopbench`, v0.1.0, released 2026-07-19** (one day after arXiv v2), with a companion GitHub repo `Haoran2099/focal` (MIT). **Data terms:** the data is marked `license: other`; it is available "for research inspection" but no redistribution/sublicensing/republication licence is granted for annotations or GT; no VideoGUI screenshots are redistributed; upstream VideoGUI HF cards declare no licence, and users must check upstream terms themselves. **Scripts:** MIT. **Per-action timestamps: not included.** The released files carry no time field; the reconstruction script assigns synthetic timestamps (base 2026-01-01T08:00Z, +6.0 s per action, ordered by task id) and then drops `timestamp`, `duration`, `kpm`, `cpm` when building the runtime records; the upstream VideoGUI-Action rows have no time field either. Caveat: the VideoGUI card points to a Google Drive "full metadata, recording" archive that I did not download; whether it holds real timings is unchecked.

(d) Verdict: **PARTIAL** — release location, version, data terms, script licence and timestamp absence are FOUND in the release artifacts, but **NOT in the paper itself** (searched as described).

### C-focal-5 — Authors, title, arXiv number, version and date, venue status

(a) Verbatim.

`abs.html` meta tags: `citation_title` = `FOCAL: Filtered On-device Continuous Activity Logging for Efficient Personal Desktop Summarization`; `citation_author` in order `Yin, Haoran`, `Wen, Zhiyuan`, `Cao, Jiannong`, `Yuan, Bo`, `Yang, Ruosong`; `citation_arxiv_id` `2604.19541`.

`abs.html` submission history (tags stripped):
> [v1] Tue, 21 Apr 2026 15:00:41 UTC (4,239 KB)
> [v2] Sat, 18 Jul 2026 13:19:51 UTC (3,848 KB)

Subjects: `Multiagent Systems (cs.MA); Human-Computer Interaction (cs.HC)`. No Comments and no Journal-ref field on the abstract page.

v2 PDF p. 1 author block order (text layer): `Haoran Yin … Zhiyuan Wen … Jiannong Cao … Ruosong Yang … Bo Yuan` (affiliations: The Hong Kong Polytechnic University ×4; China Mobile Communications Company Limited Research Institute for Bo Yuan). Side stamp: `arXiv:2604.19541v2  [cs.MA]  18 Jul 2026`. Running header pp. 2–9: `Preprint. Under review.`

(b) Locators: https://arxiv.org/abs/2604.19541 (retrieved 2026-09-13); v2 PDF p. 1–2.

(c) Reading. Yin, H., Wen, Z., Cao, J., Yuan, B., Yang, R. (arXiv metadata order); title as above; arXiv:2604.19541; latest version v2 submitted 2026-07-18 (v1 2026-04-21). **Preprint, no venue**: arXiv has no journal reference, and the PDF says "Preprint. Under review." (ACM `acmart` template, acknowledgments "Omitted for anonymous review"). Caveat: the author order **differs** between the arXiv metadata / PDF metadata (`…Cao; Bo Yuan; Ruosong Yang`) and the printed author block in both PDFs (`…Cao, Ruosong Yang, Bo Yuan`). The DesktopBench `CITATION.cff` follows the arXiv metadata order.

(d) Verdict: **FOUND** (with the author-order discrepancy noted).

## Source: videogui-arxiv24

Copies used (retrieved 2026-09-13; local root `_dev/research/jioh/2026-09-13-verification/sources/videogui-arxiv24/`):

- arXiv abstract page https://arxiv.org/abs/2406.10227 → `abs.html` (only v1 exists: `[v1] Fri, 14 Jun 2024 17:59:08 UTC (46,368 KB)`)
- v1 PDF https://arxiv.org/pdf/2406.10227v1 → `v1.pdf` (24 pp.), text `v1.txt`
- NeurIPS proceedings page https://proceedings.neurips.cc/paper_files/paper/2024/hash/804e757b7d7043c26701c3a313032101-Abstract-Datasets_and_Benchmarks_Track.html → `neurips-abstract-804e.html` (found via web search; the page itself is the evidence)
- The URL printed in FOCAL's reference [14], https://proceedings.neurips.cc/paper_files/paper/2024/hash/0fa4e4715c2d876d5ba7bb04f6f7f75f-Abstract-Datasets_and_Benchmarks_Track.html → HTTP 404 (`neurips-abstract.html`); same hash on papers.nips.cc → 404
- HF API + dataset cards at pinned revisions: `VideoGUI/VideoGUI-Action@0a8110739acf4c766d4d55c9672cb38d1d9bfcbd` → `hf-VideoGUI-Action.json`, `hf-VideoGUI-Action-README.md`; `VideoGUI/VideoGUI-Mid-Plan@6852d8c9f2b9c586d7ff7cce2611080140f1a30c` → `hf-VideoGUI-Mid-Plan.json`, `hf-VideoGUI-Mid-Plan-README.md`

### C-videogui-1 — Identity of the VideoGUI paper; whether DesktopBench derives from it

(a) Verbatim.

arXiv `abs.html` meta: title `VideoGUI: A Benchmark for GUI Automation from Instructional Videos`; authors `Lin, Kevin Qinghong`, `Li, Linjie`, `Gao, Difei`, `WU, Qinchen`, `Yan, Mingyi`, `Yang, Zhengyuan`, `Wang, Lijuan`, `Shou, Mike Zheng`; date `2024/06/14`; Comments `24 pages, 16 tables, 17 figures`.

NeurIPS proceedings page text:
> VideoGUI: A Benchmark for GUI Automation from Instructional Videos
> Kevin Qinghong Lin, Linjie Li, Difei Gao, Qinchen Wu, Mingyi Yan, Zhengyuan Yang, Lijuan Wang, Mike Zheng Shou
> Advances in Neural Information Processing Systems 37  (NeurIPS 2024)
> Datasets and Benchmarks Track

VideoGUI v1 PDF p. 3 §3.1 (text layer):
> Pipeline. The VideoGUI creation pipeline is illustrated in Fig.2. For each software, (i) we manually
> select instructional videos paired with high-quality transcripts from YouTube, focusing on those
> teaching practical and novel usages. To collect the human manipulation trajectory , we build a
> simulated environment to monitor user behaviors including Click, Drag, Type/Press, and Scroll.
> (ii) We invite five participants who first watch the selected video and then try to reproduce the effects
> shown using our simulator, which records all cursor and keyboard activities (e.g., [x, y] coordinates of

p. 4:
> Data statistic. Overall, VideoGUI includes 178 tasks across 11 software applications (Fig. 3a) on
> Windows and Web browsers (Chrome, Edge, Firefox). It comprises 86 complex tasks (i.e., full task)
> and 92 simple tasks (i.e., subtask) that do not require high-level planning, where those 86 full tasks
> can be further divided into 371 subtasks, resulting in a total of 463 subtasks. Fig. 3b shows the
> distribution of number of actions per task. In total, we collect 2,712 atomic manual actions.

VideoGUI-Action card YAML at revision 0a81107: `num_examples: 2572`. VideoGUI-Mid-Plan card at 6852d8c: `num_examples: 462`.

FOCAL side (from focal-arxiv26): TeX line 456 `We reconstruct \textbf{VideoGUI}~\citep{lin2024videogui} into \textbf{DesktopBench}`; FOCAL reference [14] (v2 PDF p. 9): `Kevin Qinghong Lin, Linjie Li, Difei Gao, Qinchen Wu, Mingyi Yan, Zhengyuan Yang, Lijuan Wang, and Mike Zheng Shou. 2024. VideoGUI: A Benchmark for GUI Automation from Instructional Videos. InAdvances in Neural Information Processing Systems, Vol. 37.` (followed by the 0fa4e47… URL). DesktopBench `manifests/upstream.json` pins `VideoGUI/VideoGUI-Action` (expected_rows 2572) and `VideoGUI/VideoGUI-Mid-Plan` (expected_rows 462).

(b) Locators: arXiv:2406.10227v1 abstract page, PDF pp. 3–4 §3.1; NeurIPS 2024 proceedings page (hash 804e757b…); HF cards at the named revisions; FOCAL v2 §4 and ref. [14]; DesktopBench v0.1.0 manifest.

(c) Reading. VideoGUI = Lin, Li, Gao, Wu, Yan, Yang, Wang, Shou, "VideoGUI: A Benchmark for GUI Automation from Instructional Videos", arXiv:2406.10227 (v1 only, 2024-06-14), published in NeurIPS 2024 Datasets and Benchmarks Track (Advances in NeurIPS 37). Its data are five participants re-enacting YouTube tutorials in 11 applications on Windows/web inside the authors' recording simulator — scripted reproductions, not natural desktop use; 178 tasks, 463 subtasks, 2,712 atomic actions (the public HF Action split has 2,572 rows). **Yes, DesktopBench derives from it**: FOCAL states it, and the DesktopBench release rebuilds from the two pinned VideoGUI HF datasets. The VideoGUI paper itself of course says nothing about DesktopBench. Caveat: the NeurIPS URL printed in FOCAL's reference [14] returns HTTP 404; the working proceedings URL has hash `804e757b7d7043c26701c3a313032101`.

(d) Verdict: **FOUND**.


---

# Plain topics


Retrieval date for every copy: 2026-09-13. `S` = `_dev/research/jioh/2026-09-13-verification/sources`.

---

## C-plain-1 — Chromium's documented process model: which processes a browser session runs, how renderer processes map to tabs or sites, process name on Linux

### Sub-item 1a — which processes a browser session runs

(a) Verbatim.

Row 8, `website_multi-process-architecture_index.md` (chromium/website @ a88b32e4):

> We refer to the main process that runs the UI and manages renderer and other
> processes as the "browser process" or "browser." Likewise, the processes
> that handle web content are called "renderer processes" or "renderers."

> ## Additional Process Types
>
> Chromium has split out a number of other components into separate processes as
> well, sometimes in platform-specific ways. For example, it now has a separate
> GPU process, network service, and storage service. Sandboxed utility processes
> can also be used for small or risky tasks, as one way to satisfy the [Rule of
> Two](https://chromium.googlesource.com/chromium/src/+/master/docs/security/rule-of-2.md)
> for security.

Row 3, `content/public/common/content_switches.cc` (@ 2060fcb7), lines 452–453, 568–570, 615–616, 778–779, 783–787, 827–828:

> // Makes this process a GPU sub-process.
> const char kGpuProcess[]                    = "gpu-process";

> // The value of this switch determines whether the process is started as a
> // renderer or plugin host.  If it's empty, it's the browser.
> const char kProcessType[]                   = "type";

> // Causes the process to run as renderer instead of as browser.
> const char kRendererProcess[]               = "renderer";

> // Causes the process to run as a utility subprocess.
> const char kUtilityProcess[]                = "utility";

> // This switch indicates the type of a utility process. It does not affect the
> // services offered by the process, but is added to the command line to make
> // it easier to identify the purpose of the utility process.
> const char kUtilitySubType[] = "utility-sub-type";

> // Causes the process to run as a zygote.
> const char kZygoteProcess[] = "zygote";

Row 2, `docs/linux/zygote.md` lines 31–39:

> Instead, we exec the prototypical renderer at the beginning of the browser
> execution. When we need more renderers, we signal this prototypical process (the
> zygote) to fork itself. The zygote is always the correct version and, by
> exec'ing one, we make sure the renderers have a different address space
> randomisation than the browser.
>
> The zygote process is triggered by the `--type=zygote` command line flag, which
> causes `ZygoteMain` (in `chrome/browser/zygote_main_linux.cc`) to be run.

Row 1, `docs/process_model_and_site_isolation.md` lines 476–479:

> * **Spare Process**: Chromium often creates a spare RenderProcessHost with a
>     live but unlocked renderer process, which is used the next time a renderer
>     process is needed. This avoids the need to wait for a new process to
>     start.

Row 7, `sandbox/policy/mojom/sandbox.mojom` (enum `Sandbox`, excerpt):

> // The audio service process. May be disabled by policy.
> kAudio,

> // The network service. May be disabled by policy.
> kNetwork,

> // Hosts the GPU service and can talk to GPU drivers and other OS APIs which
> // may not be expecting untrusted input.
> kGpu,

> // Hosts untrustworthy web content. Blocks as much OS access as possible.

(b) Locators: as given above per file and commit.

(c) Reading. The design doc names one browser process (UI, manages the others), renderer processes (web content), and "additional process types": a GPU process, a network service, a storage service, and sandboxed utility processes. The command-line switch file shows the kinds are distinguished by `--type=` (`renderer`, `gpu-process`, `utility`, `zygote`; empty = browser), with `--utility-sub-type=` added to label which service a utility process hosts. On Linux a zygote process (`--type=zygote`) is started at browser start and forks renderers. A spare, not-yet-used renderer is often kept. The sandbox enum lists more service-process kinds (audio, network, GPU, print compositor, CDM, etc.), some platform-gated. Caveats: the docs do not give a fixed count of processes per session; the exact set depends on platform, flags and policy ("sometimes in platform-specific ways", "May be disabled by policy"). The zygote.md path `chrome/browser/zygote_main_linux.cc` is stale — at this commit the zygote code lives under `content/zygote/` (row 6); the doc's description is still what it states.

(d) Verdict: FOUND.

### Sub-item 1b — how renderer processes map to tabs or sites

(a) Verbatim, row 1 (`docs/process_model_and_site_isolation.md` @ 2060fcb7).

Lines 141–150:

> ### Full Site Isolation (site-per-process)
>
> _Used on: Desktop platforms (Windows, Mac, Linux, ChromeOS)._
>
> In (one-)site-per-process mode, each process is locked to documents from a
> single site. Sites are defined as scheme plus eTLD+1, since different origins
> within a given site may have synchronous access to each other if they each
> modify their document.domain. This mode provides all sites protection against
> compromised renderers and Spectre-like attacks, without breaking backwards
> compatibility.

Lines 115–118:

> Note that the user may visit multiple instances of a given principal in the
> browser, sometimes in unrelated tabs (i.e., separate browsing context
> groups). These separate instances do not need synchronous access to each
> other and can safely run in separate processes.

Lines 322–331:

> * **Soft Process Limit**: On desktop platforms, Chromium sets a "soft" process
>     limit based on the memory available on a given client. While this can be
>     exceeded (e.g., if Site Isolation is enabled and the user has more open
>     sites than the limit), Chromium makes an attempt to start randomly reusing
>     same-site processes when over this limit. For example, if the limit is 100
>     processes and the user has 50 open tabs to `example.com` and 50 open tabs to
>     `example.org`, then a new `example.com` tab will share a process with a
>     random existing `example.com` tab, while a `chromium.org` tab will create a
>     101st process. Note that Chromium on Android does not set this soft process
>     limit, and instead relies on the OS to discard processes.

Lines 332–342:

> * **Aggressive Reuse**: For some cases (including on Android), Chromium will
>     aggressively look for existing same-site processes to reuse even before
>     reaching the process limit. Out-of-process iframes (OOPIFs) and [fenced
>     frames](https://developer.chrome.com/en/docs/privacy-sandbox/fenced-frame/)
>     use this approach, such that an `example.com` iframe in a cross-site page
>     will be placed in an existing `example.com` process (in any browsing context
>     group), even if the process limit has not been reached.

Lines 269–273 (under "Historical Modes"):

> * **Process-per-tab**: This model used a separate process for each browsing
>     context group (i.e., possibly multiple related tabs), but did not attempt
>     to switch processes on cross-site navigations. In practice, though, this
>     model still needed to swap processes for privileged pages like `chrome://`
>     URLs.

Row 8 (`website_multi-process-architecture_index.md`), lines 100–111:

> ## Sharing the renderer process
>
> In general, each new window or tab opens in a new process. The browser will
> spawn a new process and instruct it to create a single `RenderFrame`, which
> may create more iframes in the page (possibly in different processes).
>
> Sometimes it is necessary or desirable to share the renderer process between
> tabs or windows. For example, a web application can use `window.open` to
> create another window, and the new document must share the same process if
> it belongs to the same origin. Chromium also has strategies to assign new
> tabs to existing processes if the total number of processes is too large.

(b) Locators: as above.

(c) Reading. On desktop Linux the current documented mode is full Site Isolation: a renderer process is locked to one site (scheme + eTLD+1). The mapping is therefore to sites/browsing-context-groups, not strictly one-per-tab: one tab can use several renderer processes (cross-site iframes go out of process), and several tabs can share one (same-site pages over the soft process limit, `window.open` relatives, process-per-site cases like the New Tab Page and extensions, and aggressive reuse for same-site iframes). "Process-per-tab" is listed only as a historical mode. The older design doc says "In general, each new window or tab opens in a new process", qualified by the sharing rules. Caveats: the soft limit depends on client memory and no number is fixed except the illustrative "100"; Android and WebView differ.

(d) Verdict: FOUND. (If a topic premise says "one renderer per tab", that is PARTIAL against the source: the source maps renderers to sites with sharing and splitting across tabs; per-tab is historical.)

### Sub-item 1c — process name on Linux

(a) Verbatim.

Row 4, `base/process/set_process_title.cc` (@ 2060fcb7), lines 64–105 (excerpt, contiguous pieces):

> // In Linux we sometimes exec ourselves from /proc/self/exe, but this makes us
> // show up as "exe" in process listings. Read the symlink /proc/self/exe and
> // use the path it points at for our process title. Note that this is only for
> // display purposes and has no TOCTTOU security implications.

>     base::FilePath::StringType base_name =
>         base::FilePath(title).BaseName().value();
>     // PR_SET_NAME is available in Linux 2.6.9 and newer.
>     // When available at run time, this sets the short process name that shows
>     // when the full command line is not being displayed in most process
>     // listings.
>     prctl(PR_SET_NAME, base_name.c_str());

>   const base::CommandLine* command_line =
>       base::CommandLine::ForCurrentProcess();
>   for (size_t i = 1; i < command_line->argv().size(); ++i) {
>     if (!title.empty()) {
>       title += " ";
>     }
>     title += command_line->argv()[i];
>   }
>   // Disable prepending argv[0] with '-' if we prepended it ourselves above.
>   setproctitle(have_argv0 ? "-%s" : "%s", title.c_str());

Row 6, `content/app/content_main.cc` line 252:

> base::SetProcessTitleFromCommandLine(argv);

Row 6, `content/zygote/zygote_linux.cc` lines 601–609:

>     // Reset the process-wide command line to our new command line.
>     base::CommandLine::Reset();
>     base::CommandLine::Init(0, nullptr);
>     base::CommandLine::ForCurrentProcess()->InitFromArgv(args);
>
>     // Update the process title. The argv was already cached by the call to
>     // SetProcessTitleFromCommandLine in ChromeMain, so we can pass NULL here
>     // (we don't have the original argv at this point).
>     base::SetProcessTitleFromCommandLine(nullptr);

Row 5, `base/threading/platform_thread_linux.cc` lines 210–226:

> void PlatformThreadBase::SetName(const std::string& name) {
>   SetNameCommon(name);
>
>   // On linux we can get the thread names to show up in the debugger by setting
>   // the process name for the LWP.  We don't want to do this for the main
>   // thread because that would rename the process, causing tools like killall
>   // to stop working.
>   if (PlatformThread::CurrentId().raw() == getpid()) {
>     return;
>   }
>
>   // http://0pointer.de/blog/projects/name-your-threads.html
>   // Set the name for the LWP (which gets truncated to 15 characters).

>   int err = prctl(PR_SET_NAME, name.c_str());

Row 9, Debian `chromium` 150.0.7871.181-1~deb13u1 file list (from `tar -tvf data.tar.xz`), lines:

> -rwxr-xr-x  0 root   root     5064 Jul 22 12:21 ./usr/bin/chromium

> -rwxr-xr-x  0 root   root 314612488 Jul 22 12:21 ./usr/lib/chromium/chromium

Row 9, `/usr/bin/chromium` from that package, lines 9, 12, 153:

> APPNAME=chromium

> LIBDIR=/usr/lib/$APPNAME

>     exec $LIBDIR/$APPNAME $CHROMIUM_FLAGS "$@"

(b) Locators: as above.

(c) Reading. Chromium does not give its child processes distinct short names. Every content process (browser, and each zygote-forked child after it rewrites its command line) sets the kernel short name (`comm`, via `PR_SET_NAME`) to the basename of its own executable, and rewrites the long command-line title to the executable path plus arguments. Process kinds are therefore told apart only by the `--type=…` argument in `/proc/<pid>/cmdline`, not by `comm`. For the Debian trixie package the executable is `/usr/lib/chromium/chromium` (started by the shell wrapper `/usr/bin/chromium` via `exec`), so the short name is `chromium` for browser, zygote, renderer, GPU and utility processes alike. Non-main threads get their own per-thread names (truncated to 15 characters); the main thread is deliberately not renamed. Caveats: (1) the executable basename depends on the build/package — for the Debian package it is `chromium`; Google's own Chrome build was not package-verified here (zygote.md's appendix only shows example paths `/opt/google/chrome-beta/chrome`, which is not packaging evidence). (2) Whether `/proc/self/exe` is readable inside the sandboxed zygote child was not verified; if it is not, the child keeps the `comm` inherited by fork, which is the same executable basename. (3) No documentation page states the Linux process name directly; this is read from code.

(d) Verdict: FOUND (from source code and the Debian package; no prose doc states it).

---

## C-plain-6 — process names under which Windows games run through Proton/Wine on Linux; whether all game threads/processes share one name

### Sub-item 6a — name of the game process itself (Wine, upstream)

(a) Verbatim, row 10 (Wine `wine-11.17`, commit 36b6a2cf).

`dlls/ntdll/unix/env.c` lines 481–505:

> /***********************************************************************
>  *           set_process_name
>  *
>  * Change the process name in the ps output.
>  */
> static void set_process_name( const char *name )
> {
>     const char *p;
>
> #ifdef HAVE_SETPROCTITLE
>     setproctitle("-%s", name );
> #endif
>     if ((p = strrchr( name, '\\' ))) name = p + 1;
>     if ((p = strrchr( name, '/' ))) name = p + 1;
> #ifdef HAVE_SETPROGNAME
>     setprogname( name );
> #endif
> #ifdef HAVE_PRCTL
> #ifndef PR_SET_NAME
> # define PR_SET_NAME 15
> #endif
>     prctl( PR_SET_NAME, name );
> #endif
> }

`dlls/ntdll/unix/env.c` lines 508–535 (`rebuild_argv`, head comment and last lines):

>  * Build the main argv by removing argv[0].

>     main_argv[--main_argc] = NULL;
>     set_process_name( main_argv[0] );
> }

`dlls/ntdll/unix/env.c` lines 2120–2126 (in `init_startup_info`, the path for a process created by another Wine process):

>     status = load_main_exe( &nt_name, machine, &module );
>     if (!NT_SUCCESS(status))
>     {
>         MESSAGE( "wine: failed to start %s: %x\n", debugstr_us(&params->ImagePathName), status );
>         NtTerminateProcess( GetCurrentProcess(), status );
>     }
>     rebuild_argv();

`dlls/ntdll/unix/env.c` lines 1951–1962 (first process started from a Unix command line):

>     if (status)  /* try launching it through start.exe */
>     {
>         static const char *args[] = { "start.exe", "/exec" };
>         free( nt_name.Buffer );
>         if (*module) NtUnmapViewOfSection( GetCurrentProcess(), *module );
>         load_start_exe( &nt_name, module );
>         prepend_argv( args, 2 );
>     }
>     else
>     {
>         rebuild_argv();

`dlls/ntdll/unix/process.c` (`spawn_process`, grandchild) lines 441–443:

>             argv = build_argv( &params->CommandLine, 2 );
>
>             exec_wineloader( argv, socketfd, pe_info );

`loader/preloader.c` lines 1372–1382:

> /* set the process name if supported */
> static void set_process_name( int argc, char *argv[] )
> {
>     int i;
>     unsigned int off;
>     char *p, *name, *end;
>
>     /* set the process short name */
>     for (p = name = argv[1]; *p; p++) if (p[0] == '/' && p[1]) name = p + 1;
>     if (wld_prctl( 15 /* PR_SET_NAME */, (long)name ) == -1) return;

Row 13, `PR_SET_NAME(2const)`:

> Set the name of the calling thread,
> using the value in the location pointed to by
> .IR name .
> .IP
> The name can be up to 16 bytes long,
> .\" TASK_COMM_LEN in include/linux/sched.h
> including the terminating null byte.
> If the length of the string, including the terminating null byte,
> exceeds 16 bytes, the string is silently truncated.

(b) Locators: as above.

(c) Reading. A Windows program run under Wine is a Unix process started from the Wine loader (`wine`, possibly via `wine-preloader`), but once ntdll has loaded the Windows executable it drops the loader from argv and sets the kernel short name to the last path component of the new argv[0] — which is the first token of the Windows command line (e.g. `C:\Games\Game.exe` → `Game.exe`), stripping both `\` and `/` separators. The kernel keeps at most 15 bytes, so long names are cut (e.g. a hypothetical `SomeLongGameName.exe` would show as its first 15 bytes). Caveats: the name comes from the command-line's first token, not necessarily from the image file name; a launch that falls back to `start.exe /exec` gets `start.exe` as argv[0] in that process; the long `/proc/<pid>/cmdline` is also rewritten (setproctitle where available, otherwise in-place argv rewriting). The concrete name of any particular game is not in the source — only the rule.

(d) Verdict: FOUND.

### Sub-item 6b — the Wine helper processes and their names

(a) Verbatim, row 10.

`dlls/ntdll/unix/loader.c` lines 506–524 (`exec_wineserver`, excerpt):

>     if (!build_path_and_exec( pid, bin_dir, "wineserver", argv )) return 0;
>     if ((path = getenv( "WINESERVER" )) && !build_path_and_exec( pid, "", path, argv )) return 0;

>     return build_path_and_exec( pid, BINDIR, "wineserver", argv );

`programs/wineboot/wineboot.c` lines 1465–1472:

> static BOOL start_services_process(void)
> {
>     static const WCHAR svcctl_started_event[] = SVCCTL_STARTED_EVENT;
>     PROCESS_INFORMATION pi;
>     HANDLE wait_handles[2];
>
>     if (!create_native_process( L"C:\\windows\\system32\\services.exe", NULL,
>                                 TRUE, DETACHED_PROCESS, L"C:\\windows\\system32", &pi))

`programs/services/services.c` lines 837–841:

>     if (!(*path = malloc(wcslen(system_dir) * sizeof(WCHAR) + sizeof(L"\\winedevice.exe"))))
>        return ERROR_NOT_ENOUGH_SERVER_MEMORY;
>
>     lstrcpyW(*path, system_dir);
>     lstrcatW(*path, L"\\winedevice.exe");

`dlls/win32u/winstation.c` lines 828–832:

>         static const WCHAR appnameW[] = {'\\','?','?','\\','C',':','\\','w','i','n','d','o','w','s',
>             '\\','s','y','s','t','e','m','3','2','\\','e','x','p','l','o','r','e','r','.','e','x','e',0};
>         static const WCHAR cmdlineW[] = {'"','C',':','\\','w','i','n','d','o','w','s','\\',
>             's','y','s','t','e','m','3','2','\\','e','x','p','l','o','r','e','r','.','e','x','e','"',
>             ' ','/','d','e','s','k','t','o','p',0};

`loader/wine.inf.in` lines 976–979 and 1064–1069:

> [RpcSsService]
> Description="RPC service"
> DisplayName="Remote Procedure Call (RPC)"
> ServiceBinary="%11%\rpcss.exe"

> [PlugPlayService]
> Description="Enables automatic configuration of devices"
> DisplayName="Plug and Play Service"
> ServiceBinary="%11%\plugplay.exe"
> ServiceType=32
> StartType=2

(b) Locators: as above.

(c) Reading. Besides the game, a Wine prefix runs `wineserver` (a native Unix binary exec'd by that name) and Windows-side helper programs that go through the same process-creation path and hence the same naming rule: `services.exe` (started by wineboot), `winedevice.exe` (driver host started by services), `explorer.exe` (started with `/desktop` for the desktop window), and service binaries such as `rpcss.exe`, `plugplay.exe` (auto-start, StartType=2) and `svchost.exe` entries in wine.inf. By the rule in 6a their short names are those `.exe` names. Caveat: which helpers are alive at a given moment depends on prefix state and what the game uses; no single source lists "the processes of a running game".

(d) Verdict: FOUND (per named helper: wineserver FOUND, services.exe FOUND, winedevice.exe FOUND, explorer.exe FOUND, rpcss.exe/plugplay.exe FOUND as service binaries; their runtime short name is an inference from the 6a rule, not a separate statement).

### Sub-item 6c — Proton's launch chain and the names it adds

(a) Verbatim, row 11 (Proton `proton-11.0-2`).

`toolmanifest_x86_64.vdf`:

> "manifest"
> {
>   "version" "2"
>   "commandline" "/proton %verb%"
>   "require_tool_appid" "4183110"
>   "use_sessions" "1"
>   "compatmanager_layer_name" "proton"
> }

`proton` lines 543–544:

>         self.wine_bin = self.bin_dir + "wine"
>         self.wineserver_bin = self.bin_dir + "wineserver"

`proton` lines 2055–2085 (excerpt):

>     def run(self):
>         if shutil.which('steam-runtime-launcher-interface-0') is not None:
>             adverb = ['steam-runtime-launcher-interface-0', 'proton']
>         else:
>             adverb = []

>             if g_proton.host_pe_arch == "x86_64-windows":
>                 #run with winepreloader directly to avoid restart through start.exe
>                 self.env["WINELOADERNOEXEC"] = "1"
>                 argv = [g_proton.lib_dir + "/wine/x86_64-unix/wine-preloader", g_proton.lib_dir + "/wine/x86_64-unix/wine", "c:\\windows\\system32\\steam.exe"]
>             else:
>                 argv = [g_proton.wine_bin, "c:\\windows\\system32\\steam.exe"]
>
>         rc = self.run_proc(adverb + argv + sys.argv[2:] + self.cmdlineappend)

`proton` lines 2126–2130:

>     elif sys.argv[1] == "waitforexitandrun":
>         #wait for wineserver to shut down
>         g_session.run_proc([g_proton.wineserver_bin, "-w"])
>         #then run
>         rc = g_session.run()

`steam_helper/steam.c` lines 417–419 and 637:

> static HANDLE run_process(BOOL *should_await, BOOL game_process)
> {
>     WCHAR *cmdline = GetCommandLineW();

>         if (!CreateProcessW(NULL, new_cmdline, NULL, NULL, FALSE, flags, NULL, NULL, &si, &pi))

Row 12, Valve Wine fork @ dc26e618, `dlls/ntdll/unix/env.c` lines 488–507 (same logic as upstream):

> static void set_process_name( const char *name )
> {
>     char *p;
>
> #ifdef HAVE_SETPROCTITLE
>     setproctitle("-%s", name );
> #endif
>     if ((p = strrchr( name, '\\' ))) name = p + 1;
>     if ((p = strrchr( name, '/' ))) name = p + 1;
> #ifdef HAVE_SETPROGNAME
>     setprogname( name );
> #endif
> #ifdef HAVE_PRCTL
> #ifndef PR_SET_NAME
> # define PR_SET_NAME 15
> #endif
>     prctl( PR_SET_NAME, name );
> #endif
> }

(b) Locators: as above.

(c) Reading. Steam starts Proton through the `proton` Python script (short name of that process would be the interpreter's, not verified here), optionally through `steam-runtime-launcher-interface-0`, inside a tool with app id 4183110 (a Steam Linux Runtime container; its identity is only the number in this source). The script runs Wine on Proton's built-in `c:\windows\system32\steam.exe` helper, which then `CreateProcessW`s the game's command line. So under Proton the process tree has at least a `steam.exe` process (Proton's helper, not the real Steam client) and the game process, plus `wineserver` and the Wine helpers from 6b. Valve's Wine fork at the pinned commit uses the same `set_process_name` code, so the game's short name follows the 6a rule (`<first command-line token basename>`, ≤15 bytes). Caveat: `reaper` and pressure-vessel wrapper names are covered in 6c-bis; the Steam client's own process name was not verified (closed source).

(d) Verdict: FOUND for `proton` → `steam.exe` → game chain and naming rule. (`reaper` / pressure-vessel names: see 6c-bis.)

### Sub-item 6c-bis — `reaper`, pressure-vessel and Steam Linux Runtime wrapper process names (added in the resumed pass)

Copy: steam-runtime-tools, https://gitlab.steamos.cloud/steamrt/steam-runtime-tools.git, tag `v0.20260903.0` = commit `06a2477429fe271c5b254399caffdab8b7737e99` (2026-09-03; highest tag in `git ls-remote` on 2026-09-13), shallow clone at `S/C-plain-6/steam-runtime-tools/`.

(a) Verbatim.

`docs/steam-compat-tool-interface.md` lines 528–530:

> In recent versions of Steam, the game process is wrapped in a `reaper`
> process which sets itself as a subreaper using `PR_SET_CHILD_SUBREAPER`
> (see [**prctl**(2)][prctl] for details).

Same file lines 567–570:

> Some Windows games, such as Soldat (638490), do not have an
> "install script" in their metadata. Running these games behaves much the
> same as a native Linux game: it is wrapped in a subreaper, version 1
> compat tools are not invoked specially, and version 2 compat tools

Same file lines 517–522:

> For example, when using Proton with "Steam Linux Runtime 2.0 (soldier)", the
> "outer" compatibility tool "Steam Linux Runtime 2.0 (soldier)" is run with
> `LD_LIBRARY_PATH` set by the Steam Runtime to point to mixed host and
> scout libraries. After setting up the container, it runs the "inner"
> compatibility tool (Proton) with an entirely new `LD_LIBRARY_PATH`
> pointing to mixed host and soldier libraries.

`pressure-vessel/wrap.1.md` line 28 and lines 1757–1760:

> **pressure-vessel-wrap** runs *COMMAND* in a container, using **bwrap**(1).

> The **pressure-vessel-wrap** process replaces itself with a **bwrap**(1)
> process. Fatal signals to the resulting **bwrap**(1) process will result
> in `SIGTERM` being received by the **pressure-vessel-wrap** process
> that runs *COMMAND* inside the container.

`pressure-vessel/adverb.1.md` lines 46–58:

> **pv-adverb** acts as the top-level process inside a Steam Linux Runtime
> container
> (the direct child of **bwrap**(1))
> with any other processes that will run inside the container,
> for example a game or an interactive shell,
> as its children.
> This means that it can supervise those processes and alter their execution
> environment.
>
> **pv-adverb** acts as a subreaper.
> This means that if the *COMMAND* starts background processes,
> they will be reparented to **pv-adverb** instead of to **init**
> when their parent process exits.

`pressure-vessel/meson.build` lines 141–142 and 232–233 (executable names):

```
pv_bin += executable(
  'pv-adverb',
```
```
pv_bin += executable(
  'pressure-vessel-wrap',
```

`bin/meson.build` line 37, line 122, and lines 252–261 (excerpt):

```
  { 'name': 'launcher-interface-0', 'glib': false },
```
```
  name_prefix = bin_details.get('prefix', 'steam-runtime-')
```
```
bubblewrap_subproject = subproject(
  'bubblewrap',
...
    'program_prefix=srt-',
```

(b) Locators: steam-runtime-tools v0.20260903.0, files and lines as given.

(c) Reading. Under Steam, the game (native or Proton) is wrapped by a Steam-client process named `reaper` that acts as a subreaper; the `reaper` binary is part of the closed-source Steam client, so its name here rests on this Valve-maintained interface document, not on its code. When Proton runs inside a Steam Linux Runtime container, the outer tool starts `pressure-vessel-wrap`, which replaces itself with `bwrap` (the bundled build is named `srt-bwrap` by `program_prefix=srt-`; whether the bundled or a host `bwrap` is used in a given run was not checked), and inside the container `pv-adverb` is the top-level process and subreaper, with Proton's `proton` script, Wine and the game below it. Proton's `proton` script calls `steam-runtime-launcher-interface-0` when present (6c); that executable name comes from the `steam-runtime-` default prefix plus `launcher-interface-0`. Short names (`comm`) by the 15-byte truncation rule (row 13), derived, not observed: `reaper`, `pv-adverb`, `bwrap`/`srt-bwrap` unchanged; `pressure-vessel-wrap` → `pressure-vessel`; `steam-runtime-launcher-interface-0` → `steam-runtime-l`. Caveat: whether `pressure-vessel-wrap` itself or `steam-runtime-launcher-interface-0` stays alive as a separate process during play (vs `exec`) was only read for `pressure-vessel-wrap` (it replaces itself).

(d) Verdict: FOUND for `reaper` (documented wrapper, closed-source binary), `pressure-vessel-wrap` → `bwrap`, `pv-adverb`; PARTIAL for which `bwrap` build runs and for whether `steam-runtime-launcher-interface-0` persists.

### Sub-item 6d — whether all game threads/processes share one name

(a) Verbatim, row 10.

`dlls/kernelbase/thread.c` lines 463–478:

> HRESULT WINAPI DECLSPEC_HOTPATCH SetThreadDescription( HANDLE thread, PCWSTR description )
> {

>     return HRESULT_FROM_NT(NtSetInformationThread( thread, ThreadNameInformation, &info, sizeof(info) ));
> }

`dlls/ntdll/unix/thread.c` lines 2640 and 2666 (in `NtSetInformationThread`):

>     case ThreadNameInformation:

>         set_native_thread_name( handle, &info->ThreadName );

`dlls/ntdll/unix/thread.c` lines 2076–2111 (Linux branch of `set_native_thread_name`, excerpt):

> static void set_native_thread_name( HANDLE handle, const UNICODE_STRING *name )
> {
> #ifdef linux

>     if (unix_pid != getpid())
>     {
>         static int once;
>         if (!once++) FIXME("cross-process native thread naming not supported\n");
>         return;
>     }
>
>     len = ntdll_wcstoumbs( name->Buffer, name->Length / sizeof(WCHAR), nameA, sizeof(nameA), FALSE );
>     snprintf(path, sizeof(path), "/proc/%u/task/%u/comm", unix_pid, unix_tid);
>     if ((fd = open( path, O_WRONLY )) != -1)
>     {
>         write( fd, nameA, len );
>         close( fd );
>     }

`include/winternl.h` lines 4096–4098:

>    undocumented exception understood by MS VC debugger, allowing the program
>    to name a particular thread. */
> #define EXCEPTION_WINE_NAME_THREAD     0x406D1388

`dlls/ntdll/exception.c` lines 257–268:

>     case EXCEPTION_WINE_NAME_THREAD:
>         if (rec->ExceptionInformation[0] == 0x1000)
>         {
>             const char *name = (char *)rec->ExceptionInformation[1];
>             DWORD tid = (DWORD)rec->ExceptionInformation[2];
>
>             if (tid == -1 || tid == GetCurrentThreadId())
>                 WARN_(threadname)( "Thread renamed to %s\n", debugstr_a(name) );
>             else
>                 WARN_(threadname)( "Thread ID %04lx renamed to %s\n", tid, debugstr_a(name) );
>             set_native_thread_name( tid, name );
>         }

`dlls/rpcrt4/rpc_server.c` line 554 (one example of Wine naming its own threads):

>   SetThreadDescription(GetCurrentThread(), L"wine_rpcrt4_io");

Row 12, Valve Wine fork @ dc26e618, `dlls/ntdll/unix/thread.c` line 2043:

>     snprintf(path, sizeof(path), "/proc/%u/task/%u/comm", unix_pid, unix_tid);

(b) Locators: as above.

(c) Reading. No. Threads do not all share the process name. On Linux, Wine (upstream 11.17 and Valve's fork used by Proton 11.0-2) writes a thread's Windows name into that thread's `/proc/<pid>/task/<tid>/comm` whenever the program names it — via `SetThreadDescription` or via the MSVC debugger exception `0x406D1388` — and Wine names its own internal worker threads (e.g. `wine_rpcrt4_io`). Threads that are never named keep the name inherited at creation, which for threads created after `set_process_name` is the game's short name. Processes also do not share one name: each process (game, `steam.exe`, `wineserver`, `services.exe`, `winedevice.exe`, `explorer.exe`, …) gets its own short name per 6a/6b. Caveats: names are truncated to 15 bytes by the kernel (man page row 13); cross-process thread renaming is not supported (FIXME branch); whether a given game names its threads is game-specific and not in the source. Chromium, by contrast, deliberately never renames its main thread (C-plain-1c).

(d) Verdict: FOUND.

---

## Verdict summary for this part

- C-plain-1a (processes in a session): FOUND
- C-plain-1b (renderer ↔ tab/site mapping): FOUND
- C-plain-1c (process name on Linux): FOUND (code + Debian package; no prose doc)
- C-plain-6a (game process name rule, Wine): FOUND
- C-plain-6b (Wine helper process names): FOUND
- C-plain-6c (Proton chain): FOUND for proton → steam.exe → game
- C-plain-6c-bis (reaper / pressure-vessel / pv-adverb names): FOUND; PARTIAL on which bwrap build runs and whether steam-runtime-launcher-interface-0 persists
- C-plain-6d (shared name for threads/processes): FOUND — they do not all share one name

Unreachable: packages.debian.org file-list and package pages (PoW challenge page, HTTP 200) — replaced by the .deb from deb.debian.org.


---

## C-plain-2 and C-plain-3

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


---


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


---


Local root: `_dev/research/jioh/2026-09-13-verification/sources/` (abbreviated `S/`). All retrievals 2026-09-13.

---

## C-plain-7 — public traces of desktop process activity with process names; process-identity fields in Azure and Google cluster traces

The topic covers three things: (A) Google cluster traces, (B) Azure traces, (C) desktop process-activity traces. Each gets its own answer below.

### C-plain-7A — Google cluster traces (2009 v1, 2011 v2.1, 2019 v3)

**(a) Verbatim**

`cluster-data/TraceVersion1.md` (commit 48b1244):
> The data have been anonymized in several ways: there are no task or job names, just numeric identifiers; timestamps are relative to the start of data collection; the consumption of CPU and memory is obscured using a linear transformation.

`cluster-data/ClusterData2019.md`:
> The 2019 traces focus on resource requests and usage, and contain no information about end users, their data, or access patterns to storage systems and other services.

`cluster-data/clusterdata_trace_format_v3.proto`, lines 199–204 (CollectionEvent):
```
  // The user who runs the collection
  optional string user = 9;
  // Obfuscated name of the collection.
  optional string collection_name = 10;
  // Obfuscated logical name of the collection.
  optional string collection_logical_name = 11;
```

Google cluster-usage traces v3 doc (PDF p. 3–4, "User and collection names"):
> User and collection names are hashed and provided as opaque base64-encoded strings that can be tested for equality.

> Usernames in this trace represent Google engineers and services. Production jobs run by the same username are likely to be part of the same external or internal service.

Same doc, PDF p. 9 (collection events field list):
> user – the obfuscated name of the “user” (person or system) that submitted the collection

> collection_name – a hash of the original complete collection name

> collection_logical_name – a hash of the parts of the collection name that reflect its purpose, and excluding things like sequence numbers or UIDs

2011 v2.1 schema doc, PDF p. 3 ("User and job names"):
> User and job names are hashed and provided as opaque base64-encoded strings that can be tested for equality.

2011 v2.1 schema doc, PDF p. 5:
> Usually all tasks within a job execute exactly the same binary with the same options and resource request.

`clusterdata-2011-2/schema.csv`, rows 6, 8, 9, 16:
```
job_events/part-?????-of-?????.csv.gz,5,user,STRING_HASH,NO
job_events/part-?????-of-?????.csv.gz,7,job name,STRING_HASH,NO
job_events/part-?????-of-?????.csv.gz,8,logical job name,STRING_HASH,NO
task_events/part-?????-of-?????.csv.gz,7,user,STRING_HASH,NO
```

**(b) Locators:** files and lines as given above, at google/cluster-data commit 48b12446; the v3 doc PDF (Drive id 10r6cnJ5…) pp. 3–4 and 9; the v2.1 doc PDF (Drive id 0B5g07T…) pp. 3 and 5; the GCS schema.csv.

**(c) Reading:** In Google's traces, workload identity is recorded per job (2011) or per collection (2019): a hashed user, a hashed job or collection name, and a hashed "logical" name. Tasks and instances are identified by numeric IDs. No trace has a process-name or binary-name field. The 2009 v1 trace has only numeric job and task IDs. The 2011 doc says tasks in a job usually run the same binary, but it does not name that binary. The 2019 v3 schema was checked in the proto and the v3 doc. The 2019 power traces and ETA exploration traces in the repo were not checked.

**(d) Verdict: FOUND.** The identity fields are hashed user, hashed job or collection name and hashed logical name, plus numeric IDs. There is no process-name field.

### C-plain-7B — Azure public traces

**(a) Verbatim**

`AzurePublicDatasetV2.md`, "### Schema" (lines 22–42). V1 has the same fields 1–12 at lines 21–35:
```
1.	Encrypted subscription id
2.	Encrypted deployment id 
...
6.	Encrypted VM id
...
12.	VM category
```

`AzureFunctionsDataset2019.md`, lines 38–47:
> | HashOwner | unique id of the application owner <sup>1</sup> |
> | HashApp | unique id for application name <sup>1</sup> |
> | HashFunction | unique id for the function name within the app <sup>1</sup>|

> 1. All ids are hashed using HMAC-SHA256 with secret salts. Each column uses a different salt.

`AzureFunctionsInvocationTrace2021.md`, lines 27–34:
> - app: application id (encrypted)
> - func: function id (encrypted), and unique only within an application

> In Azure Functions, the unit of deployment is called an application, and an application has one or more functions. For example, an application could be a binary file with one or more entry points.

`AzureTracesForPacking2020.md`, lines 36–43:
> | vmId | unique id of the vm request<sup>1</sup> |
> | tenantId | unique id for the owner of a group of requests<sup>1</sup> |
> | vmTypeId | requested VM type<sup>1</sup>|

> 1. All ids are anonymized. These are consistent only within a single sqlite file.

`AzureFunctionsBlobDataset2020.md`, lines 38–48:
> | AnonAppName | Unique id for the application<sup>1</sup> |

> 1. Ids are hashed using HMAC-SHA512 with secret salts and cropped.

`AzureLLMInferenceDataset2023.md`, lines 25–30:
> | TIMESTAMP | Invocation time |
> | ContextTokens | Number of context tokens |
> | GeneratedTokens | Number of generated  tokens |

**(b) Locators:** Azure/AzurePublicDataset commit 207bed67. Files and line ranges are given above.

**(c) Reading:** The Azure VM traces (2017 V1, 2019 V2) identify workloads by encrypted subscription, deployment and VM IDs, plus a "VM category". The Functions traces use hashed or encrypted owner, application and function IDs. The packing trace uses anonymized VM, tenant and VM-type IDs. The LLM inference trace has no identity field. None of these has a process name or executable name. The Functions doc says only that an app "could be a binary file"; the binary's name is hashed. The VM category values are not defined in the V1 or V2 md files; the docs point to the SOSP'17 paper, which was not checked. The Azure LMM 2025, LLM 2024, GreenSKU and VM-noise docs were grepped for "process" and "name" and have no process-identity field.

**(d) Verdict: FOUND.** The identity fields are encrypted or hashed IDs only. There is no process-name field.

### C-plain-7C — public traces of desktop process activity with process names

**(a) Verbatim**

LANL "Comprehensive, Multi-Source Cyber-Security Events" page (https://csr.lanl.gov/data/cyber1/), "proc.txt.gz":
> This data represents process start and stop events collected from individual Windows-based desktop computers and servers. Each event is on a separate line in the form of “time,user@domain,computer,process name,start/end” and represents a process event at the given time.

Same page:
> All other users, computers, process, ports, times, and other details were de-identified as a unified set across all the data elements (e.g. U1 is the same U1 in all of the data).

Example rows on the page:
```
1,C553$@DOM1,C553,P16,Start
1,C553$@DOM1,C553,P25,End
```

LANL "Unified Host and Network Data Set" page (https://csr.lanl.gov/data/2017/), field table:
> ProcessName
> The process executable name, for authentication events this is the process that processed the authentication event. ProcessNames may include the file type extensions (i.e exe).

Turcotte, Kent & Hash, arXiv:1708.07518v1, PDF p. 10:
> When de-identifying the process events, only the base process name was de-identified and the extension was left as is.

Same, PDF p. 11:
> For the process names, dates, version numbers, operating systems and hexadecimal strings were removed where possible so that processes run on different operating systems or with different versions would map to the same process name.

DARPA OpTC `README.md` (FiveDirections/OpTC-data commit 5b10860):
> Each Windows 10 endpoint is equipped with an endpoint sensor that monitors host events, packs them into JSON records, and sends them to Kafka.

> The evaluation started with a period of benign record generation, followed by the injection of malware by a red team. Benign traffic ran continuously during red team activity.

OpTC `ecar.md`:
> * When process details are present, an "image_path" entry in Event.properties will also typically be present

Example eCAR object in `ecar.md`:
```
  "object": "PROCESS",
  "action": "CREATE",
...
    "image_path": "\\Device\\HarddiskVolume1\\cygwin64\\bin\\bash.exe",
```

BEHACOM, Data in Brief 31 (2020) 105767, PMC7270191, Table 5 "Application usage statistics features description":
> current_app
> Application executable name in foreground when the vector was generated.

> penultimate_app
> Penultimate application executable name in foreground during the time window.

> active_apps_average
> Average number of applications active during the time window.

Same article, §2 (scenario):
> The proposed scenario comprises twelve different individuals interacting for fifty-five consecutive days with their personal computers in their own way and without restrictions.

**(b) Locators:** as given above. The LANL pages are HTML with no version. The Turcotte paper is arXiv 1708.07518v1, PDF pp. 10–11. OpTC is at commit 5b10860, files README.md and ecar.md. BEHACOM is PMC7270191, Table 5 and §2.

**(c) Reading:**
- **LANL 2015 (cyber1):** public per-computer process start and stop events from Windows desktops and servers. The "process name" field is de-identified to tokens such as `P16`, so no real names are published.
- **LANL 2017 (Unified Host and Network):** public Windows host events (4688/4689) with `ProcessName` and `ParentProcessName`. The base name is de-identified and only the file extension is kept, so again no real names. The raw data sits behind an email form: the HEAD request for `wls_day-01.bz2` returned 401, and I did not submit the form, so the data rows were not inspected.
- **DARPA OpTC:** publishes real executable paths (`image_path`) for PROCESS CREATE events on about 500 Windows 10 hosts. These are hosts in an instrumented enterprise exercise with red-team activity. The README does not say that the benign activity came from real human users. The data itself is on Google Drive and was not downloaded.
- **BEHACOM:** from real personal use by 12 users on Windows and Linux. It publishes the foreground application's executable name (current and penultimate) per one-minute window, plus only a *count* of active applications. Background process names are not released. The CSV files on Mendeley Data were not downloaded.

Search method: WebSearch queries "public dataset desktop computer process names application usage logs Windows users trace released researchers", "OpTC dataset FiveDirections process create image_path schema github", and "dataset "process names" "window titles" desktop users logged released open data computer usage study". I then read primary docs for LANL (2015, 2017), OpTC and BEHACOM. This is not an exhaustive survey. Loghub, GroundCUA and a UIC HCI log set appeared in search results but were not checked.

**(d) Verdict: PARTIAL.** Public traces with a process-name *field* exist. In LANL the names are de-identified. OpTC has real executable paths, but from an instrumented exercise that is not described as natural desktop use. BEHACOM from natural use gives only the foreground executable name per minute. No dataset checked publishes the real names of all processes from natural desktop use.

---

## C-plain-8 — what Phoronix Test Suite and UnixBench measure; whether mobile app-usage datasets record concurrent foreground apps

### C-plain-8A — Phoronix Test Suite

**(a) Verbatim** (`documentation/phoronix-test-suite.md` at tag v10.8.4, "Overview"):
> The Phoronix Test Suite client itself is an automated test framework for providing seamless execution of test profiles and test suites. There are more than 650 tests available by default, which are transparently available via OpenBenchmarking.org integration. Of these default test profiles there is a range of sub-systems that can be tested and a range of hardware from mobile devices to desktops and workstations/servers.

> Test profiles can produce a quantitative result or other qualitative/abstract results like image quality comparisons and pass/fail. Using Phoronix Test Suite modules, other data can also be automatically collected at run-time such as the system power consumption, disk usage, and other software/hardware sensors.

Same file, line 100 (`stress-run`):
> This option will run the passed tests/suites in the multi-process stress-testing mode. The stress-run mode will not produce a result file but is rather intended for running multiple test profiles concurrently to stress / burn-in the system. The number of tests to run concurrently can be toggled via the PTS_CONCURRENT_TEST_RUNS environment variable and by default is set to a value of 2.

`README.md` at v10.8.4:
> This framework is designed to be an extensible architecture so that new test profiles and suites can be easily added to represent performance benchmarks, unit tests, and other quantitative and qualitative (e.g. image quality comparison and pass/fail) measurements.

**(b) Locator:** phoronix-test-suite tag v10.8.4 (commit f0365737): `documentation/phoronix-test-suite.md` "Getting Started > Overview" and line 100; `README.md` paragraph 3.

**(c) Reading:** PTS is a framework, not a single benchmark. What it measures depends on the test profile chosen from more than 650 profiles, covering many subsystems. Profiles report a quantitative result, or an image-quality or pass/fail result, and modules can also collect sensor data. By default the `run` and `benchmark` commands run tests one after another. `stress-run` runs several profiles at the same time (default 2) but writes no result file. Caveat: the doc is v10.8.4 from 2022, the latest version tag in `git ls-remote`.

**(d) Verdict: FOUND.**

### C-plain-8B — UnixBench (byte-unixbench)

**(a) Verbatim** (`README.md`, commit e949d44):
> The purpose of UnixBench is to provide a basic indicator of the performance of a Unix-like system; hence, multiple tests are used to test various aspects of the system's performance. These test results are then compared to the scores from a baseline system to produce an index value, which is generally easier to handle than the raw scores. The entire set of index values is then combined to make an overall index for the system.

> Multi-CPU systems are handled. If your system has multiple CPUs, the default behaviour is to run the selected tests twice -- once with one copy of each test program running at a time, and once with N copies, where N is the number of CPUs.

> Do be aware that this is a system benchmark, not a CPU, RAM or disk benchmark.

`UnixBench/USAGE`, "Tests" (system category, excerpt):
```
    dhry2reg         Dhrystone 2 using register variables
    whetstone-double Double-Precision Whetstone
    syscall          System Call Overhead
    pipe             Pipe Throughput
    context1         Pipe-based Context Switching
    spawn            Process Creation
    execl            Execl Throughput
    fstime-w         File Write 1024 bufsize 2000 maxblocks
...
    shell1           Shell Scripts (1 concurrent) (runs "looper 60 multi.sh 1")
    shell8           Shell Scripts (8 concurrent) (runs "looper 60 multi.sh 8")
```

`UnixBench/USAGE`, "Running the Tests":
> However, if using a windowing system, you may want to switch to a minimal window setup (for example, log in to a "twm" session), so that randomly-churning background processes don't randomise the results too much.

**(b) Locator:** kdlucas/byte-unixbench commit e949d44: `README.md` (intro and "Included Tests"); `UnixBench/USAGE` ("Running the Tests", "Tests").

**(c) Reading:** UnixBench measures raw throughput of synthetic tests: integer and floating-point compute (Dhrystone, Whetstone), syscall overhead, pipe throughput, context switching, process creation, execl, file I/O, shell-script loops, and 2D/3D graphics. It normalises the scores against a baseline machine (SPARCstation 20-61 per the README) into index values. It runs 1 copy and N copies of each test. It is not an interactive-latency benchmark, and the USAGE file advises reducing background processes.

**(d) Verdict: FOUND.**

### C-plain-8C — do mobile app-usage datasets record concurrent foreground apps? (per dataset)

**LSApp** — `README.md` (commit c001713), "Format":
> * app_name: name of the app.
> * event_type: type of the event recorded. Possible values: Opened, Closed, User Interaction, Broken

Reading: the data is an event log (Opened, Closed, User Interaction, Broken) per user and session. The README does not say whether two apps can be open at once, and there is no foreground or background field. **NOT FOUND** (searched the README for foreground, concurrent, background and multi-window; none present).

**Tsinghua App Usage** — dataset page, "Dataset information":
> In this App usage dataset, each entry contains an anonymized User identification, timestamps of HTTP request or response, the length of the packet, the domain visited and the user-agent field. We identify Apps from the networking metadata by adopting SAMPLES

File description:
> App_Usage_Trace.txt
> User ID||Timestamp(Second) ||Location (base station ID)||Used App

Reading: apps are inferred from network traffic, so there is no notion of a foreground app. **PREMISE NOT IN SOURCE**: the dataset records network-derived "Used App" per timestamp, not foreground state.

**LiveLab** (Rice, iPhone 3GS, 2010–2011) — traces page, `appusage.sql`:
> appusage.sql: applications run by users (event / built-in logfile driven)

> duration: duration for which the application was running in seconds. Note that turning the screen off effectively exits the application

Reading: each row is an app run with a start time and duration. The page does not say whether runs can overlap or whether a row means foreground. **NOT FOUND**.

**Carat Top 1000 Users Long-Term App Usage Dataset** — data-sharing page:
> apps (app usage data, see below)
> Where app usage is a list of JSON objects with the following attributes:
> processName (App Android package name)
> priority (background, foreground, etc, see Android documentation)

> The app collected application usage and battery level information every time the battery level changed by 1%, as allowed by the mobile operating system.

Reading: each sample (taken at each 1% battery change) lists several running apps, each with an Android importance label that includes "foreground". The page does not say whether more than one app can carry "foreground" in the same sample, or what "foreground" means beyond the Android documentation. **PARTIAL**: a per-sample list of apps with foreground/background priority exists, but concurrent foreground apps are not documented. The zip (password given on the page) was not downloaded.

**Device Analyzer** (Cambridge) — **COPY UNREACHABLE**. https://deviceanalyzer.cl.cam.ac.uk/ and http://deviceanalyzer.cl.cam.ac.uk/ timed out (curl error 28, 30 s and 60 s). https://www.cl.cam.ac.uk/research/dtg/deviceanalyzer/ returned 404.

Not checked: Nokia Mobile Data Challenge (MDC), which is access-controlled.

**Overall C-plain-8C verdict: NOT FOUND.** None of the four reachable datasets documents concurrent foreground apps. Carat is the closest (PARTIAL).

---

## C-plain-9 — peer-reviewed papers citing Phoronix Test Suite / UnixBench by repository URL

### UnixBench (github.com/kdlucas/byte-unixbench)

**Example 1 — Lock-in-Pop, USENIX ATC '17** (Yiwen Li, Brendan Dolan-Gavitt, Sam Weber, Justin Cappos; *Proceedings of the 2017 USENIX Annual Technical Conference*, ISBN 978-1-931971-38-6). The USENIX PDF is byte-identical to the NYU-hosted copy (checked with `cmp`).

PDF p. 12 (body):
> Graphene [43] also shows an overhead ranging from 1.4x to 2x when running applications such as the Apache web server and the Unixbench suite [44].

PDF p. 13 (references):
> [44] Unixbench. https://github.com/kdlucas/byte-unixbench. Accessed September 2016.

**Example 2 — The Koala Benchmarks for the Shell, USENIX ATC '25** (Lamprou et al.; *Proceedings of the 2025 USENIX Annual Technical Conference*, ISBN 978-1-939133-48-9).

PDF p. 13 (body):
> Similarly, zsh-bench [68], the Oils benchmarks [8], and UnixBench [47] focus on isolated performance characteristics—e.g., interactive shell behavior or command invocation times.

PDF p. 15 (references):
> [47] Kirk D. Lucas and Contributors. UnixBench: The BYTE UNIX Benchmark Suite. https://github.com/kdlucas/byte-unixbench, 2012. Accessed: 2025-04-28.

Verdict (UnixBench): **FOUND**, two peer-reviewed USENIX ATC papers.

### Phoronix Test Suite (github.com/phoronix-test-suite/phoronix-test-suite)

**Example 3 — Popescu & Lopes, "Exploiting Undefined Behavior in C/C++ Programs for Optimization: A Study on the Performance Impact"**, *Proc. ACM Program. Lang.* 9 (PLDI), Article 161, 2025. Copy: author-hosted PDF with the PACMPL running heads "161:n" and a CC-BY 4.0 notice. The ACM DL PDF returned HTTP 403, so I could not compare it with the publisher copy.

PDF p. 6 (printed 161:6), body and footnote 4:
> All the benchmarks we used were from the Phoronix Test Suite,4 with the exception of Z3 for which we created new performance tests using files from the SMT library.5

> 4https://github.com/phoronix-test-suite/phoronix-test-suite/

**Example 4 — Gamess & Hernandez, "Performance Evaluation of Different Raspberry Pi Models for a Broad Spectrum of Interests"**, *IJACSA* 13(2), 2022. The repository URL appears in the body (Fig. 21 listing), but the reference list cites the website instead.

PDF p. 8 (printed p. 826):
> In Line 02, PTS was cloned from GitHub.

> 02: git clone https://github.com/phoronix-test-suite/\
> phoronix-test-suite.git

PDF p. 11 (printed p. 829, references):
> [38] “Phoronix Test Suite: Open-Source, Automated Benchmarking.” https://www.phoronix-test-suite.com.

Not counted as peer-reviewed (arXiv copies carry no venue statement):
- arXiv 2305.04641, "The Cure is in the Cause: A Filesystem for Container Debloating", PDF p. 14 ref: "[38] Phoronix. Phoronix test suite 10.8.4. https://github.com/phoronix-test-suite/ phoronix-test-suite, 2023. [Online; accessed 2023-04-30]."
- arXiv 2401.10582, "Exploiting Kubernetes' Image Pull Implementation to Deny Node Availability", PDF p. 14 ref: "[18] Phoronix Media, “Phoronix Test Suite,” Sep. 2023, original-date: 2014-01-12T04:56:38Z. [Online]. Available: https://github.com/ phoronix-test-suite/phoronix-test-suite".

Search method: WebSearch for the quoted repo URLs (with usenix and proceedings terms), and an OpenAlex full-text search for `"github.com/phoronix-test-suite"` (13 hits, used only for discovery). The OpenAlex search for `"github.com/kdlucas/byte-unixbench"` was rate-limited (HTTP 429, twice). Each paper listed was verified in its downloaded PDF. The PACMPL OOPSLA 2023 paper "Building Dynamic System Call Sandbox with Partial Order Analysis" (doi 10.1145/3622842) was also an OpenAlex hit, but the ACM PDF returned 403 and it was not verified. The TUNA EuroSys'25 paper (NSF PAR and arXiv copies) was checked and contains no "Phoronix" string.

Verdict (Phoronix Test Suite): **FOUND** for the PACMPL 2025 paper (footnote URL; caveat: author-hosted copy). **PARTIAL** for IJACSA 2022 (URL in body text only).

**Overall C-plain-9 verdict: FOUND.**

---

## Verdict summary (this part)

- C-plain-7A Google traces: FOUND (hashed user, job/collection name and logical name; numeric IDs; no process names)
- C-plain-7B Azure traces: FOUND (encrypted or hashed subscription, deployment, VM, owner, app and function IDs; no process names)
- C-plain-7C desktop process traces with names: PARTIAL (LANL de-identified; OpTC real image paths but from an exercise; BEHACOM foreground executable only)
- C-plain-8A PTS: FOUND
- C-plain-8B UnixBench: FOUND
- C-plain-8C mobile concurrent foreground: NOT FOUND overall. LSApp NOT FOUND; Tsinghua PREMISE NOT IN SOURCE; LiveLab NOT FOUND; Carat PARTIAL; Device Analyzer COPY UNREACHABLE.
- C-plain-9 papers citing by repo URL: FOUND (UnixBench: ATC'17, ATC'25; PTS: PACMPL/PLDI'25; IJACSA'22 partial)

Unreachable or blocked URLs:
- https://deviceanalyzer.cl.cam.ac.uk/ (timeout), http://deviceanalyzer.cl.cam.ac.uk/ (timeout), https://www.cl.cam.ac.uk/research/dtg/deviceanalyzer/ (404)
- https://csr.lanl.gov/data-fence//unified-host-network-dataset-2017/wls/wls_day-01.bz2 (401; form not submitted)
- https://dl.acm.org/doi/pdf/10.1145/3729260 and https://dl.acm.org/doi/pdf/10.1145/3622842 (403)
- https://www.mdpi.com/2079-9292/13/23/4838/pdf (403)
- https://dl.acm.org/doi/pdf/10.1145/3689031.3717480 and the MSR TUNA PDF (403)
- OpenAlex full-text search for byte-unixbench (429)


---

# Verdicts per topic / item

| Topic | Item | Verdict |
|---|---|---|
| C-focal-1 | Interruption split (100 sessions, A→YouTube→A) | FOUND |
| C-focal-2 | Multitask split (320 sessions, 20 patterns, per-action app/title + screenshot) | FOUND |
| C-focal-3 | Constructed from VideoGUI, not recorded natural use | FOUND |
| C-focal-4 | Release (HF `HaoranYin/desktopbench` v0.1.0; data `license: other`, no redistribution grant; scripts MIT; no per-action timestamps) — in release artifacts, not in the paper | PARTIAL |
| C-focal-5 | Bibliographic identity; preprint, no venue (author order differs between arXiv metadata and PDF author block) | FOUND |
| C-videogui-1 | VideoGUI identity (NeurIPS 2024 D&B); DesktopBench derives from it | FOUND |
| C-plain-1a | Chromium process kinds in a session | FOUND |
| C-plain-1b | Renderer ↔ site mapping (Site Isolation on desktop Linux; per-tab only historical) | FOUND |
| C-plain-1c | Linux process name = executable basename for all kinds (`chromium` in Debian 150.0.7871.181-1~deb13u1) | FOUND |
| C-plain-2 | Scheduled scan shipped by default (answer: no, Debian 13 / Ubuntu 24.04 / Fedora spec) | FOUND |
| C-plain-2 | Which process performs the scheduled scan | PREMISE NOT IN SOURCE |
| C-plain-2 | Fedora unit enable state (presets not read) | PARTIAL |
| C-plain-3 | tracker-miner-fs-3 (renamed localsearch-3 in Debian 13) | FOUND |
| C-plain-3 | baloo_file | FOUND |
| C-plain-3 | plocate-updatedb.timer → `updatedb.plocate` (enabled on install; package not default-installed) | FOUND |
| C-plain-4 | Jellyfin transcoder executable `ffmpeg` (renamed package/dir, not binary) | FOUND |
| C-plain-5 | ML training jobs started without the user | NOT FOUND |
| C-plain-5 | Media rendering jobs | PARTIAL |
| C-plain-5 | Transcoding jobs | PARTIAL |
| C-plain-5 | Backup jobs (`dpkg-db-backup`, Debian) | FOUND |
| C-plain-6a | Game process name rule under Wine | FOUND |
| C-plain-6b | Wine helper process names | FOUND |
| C-plain-6c | Proton chain `proton` → `steam.exe` → game | FOUND |
| C-plain-6c-bis | `reaper`, `pressure-vessel-wrap`→`bwrap`, `pv-adverb` | FOUND |
| C-plain-6c-bis | Which `bwrap` build runs; whether `steam-runtime-launcher-interface-0` persists | PARTIAL |
| C-plain-6d | Threads/processes do not all share one name | FOUND |
| C-plain-7A | Google cluster trace identity fields (hashed; no process name) | FOUND |
| C-plain-7B | Azure trace identity fields (encrypted/hashed IDs; no process name) | FOUND |
| C-plain-7C | Public desktop process traces with real process names | PARTIAL |
| C-plain-8A | Phoronix Test Suite | FOUND |
| C-plain-8B | UnixBench | FOUND |
| C-plain-8C | LSApp concurrent foreground apps | NOT FOUND |
| C-plain-8C | Tsinghua App Usage foreground apps | PREMISE NOT IN SOURCE |
| C-plain-8C | LiveLab concurrent foreground apps | NOT FOUND |
| C-plain-8C | Carat foreground priority per sample | PARTIAL |
| C-plain-8C | Device Analyzer | COPY UNREACHABLE |
| C-plain-9 | UnixBench cited by repo URL (USENIX ATC '17, ATC '25) | FOUND |
| C-plain-9 | Phoronix Test Suite cited by repo URL (PACMPL 9 PLDI 2025, footnote) | FOUND |
| C-plain-9 | IJACSA 13(2) 2022 (URL in body listing only) | PARTIAL |

**Counts (39 verdict items):** FOUND 25 · PARTIAL 8 · NOT FOUND 3 · PREMISE NOT IN SOURCE 2 · COPY UNREACHABLE 1.

# Unreachable / blocked URLs

- https://proceedings.neurips.cc/paper_files/paper/2024/hash/0fa4e4715c2d876d5ba7bb04f6f7f75f-Abstract-Datasets_and_Benchmarks_Track.html and the same path on papers.nips.cc → HTTP 404 (the URL printed in FOCAL ref. [14]); working page uses hash `804e757b7d7043c26701c3a313032101`.
- https://api.semanticscholar.org/graph/v1/paper/arXiv:2406.10227 → HTTP 429 (discovery only; not needed).
- https://packages.debian.org/trixie/amd64/chromium/filelist, https://packages.debian.org/trixie/chromium → HTTP 200 proof-of-work challenge page, no content; replaced by the .deb from deb.debian.org.
- invent.kde.org `-/raw/` URLs (baloo) → HTTP 403; replaced by `git clone` at tag v6.13.0.
- https://support.plex.tv/articles/200289526-scheduled-tasks/ → HTTP 404; correct article 201553286 used.
- https://deviceanalyzer.cl.cam.ac.uk/ and http://deviceanalyzer.cl.cam.ac.uk/ → timeout (curl 28); https://www.cl.cam.ac.uk/research/dtg/deviceanalyzer/ → HTTP 404. (Device Analyzer verdict COPY UNREACHABLE.)
- https://csr.lanl.gov/data-fence//unified-host-network-dataset-2017/wls/wls_day-01.bz2 → HTTP 401 (email form not submitted).
- https://dl.acm.org/doi/pdf/10.1145/3729260, https://dl.acm.org/doi/pdf/10.1145/3622842, https://dl.acm.org/doi/pdf/10.1145/3689031.3717480 → HTTP 403; https://www.mdpi.com/2079-9292/13/23/4838/pdf → HTTP 403; Microsoft Research TUNA PDF → HTTP 403.
- OpenAlex full-text search for `github.com/kdlucas/byte-unixbench` → HTTP 429.
- Not fetched by choice (noted as caveats in the sections): VideoGUI Google Drive "full metadata, recording" archive; DARPA OpTC data files; BEHACOM CSVs; Carat data zip.
