# S4 — own measurement on a CI runner (T6)

Reader class S4. Topic T6 only: whether a GitHub Actions hosted runner can run a game at all (native Linux game under Xvfb with software rendering; Proton without a GPU) and what a `/proc` sidecar could observe of it. Documentation research only; nothing was executed or installed. Access date for every source: 2026-09-13. Source copies are under `../sources/S4-*/`; each folder carries a `SOURCE.txt` with URL, version/commit and SHA-256 per file. The `.txt` files next to `.html` copies are tag-stripped renderings made locally for grepping; passages below were read from those renderings and checked against the `.html`.

## 1. Search log

| # | Date | Engine / venue | Query or URL | Followed | Dead ends |
|---|------|----------------|--------------|----------|-----------|
| 1 | 2026-09-13 | raw.githubusercontent.com | `actions/runner-images/main/images/ubuntu/Ubuntu2204-Readme.md`, `Ubuntu2404-Readme.md` | saved; grep for `Xvfb`, `mesa`, `GPU`, `Kernel`, `Image Version` | no `mesa`/`libgl` string in either README |
| 2 | 2026-09-13 | api.github.com | `repos/actions/runner-images/commits?path=images/ubuntu/Ubuntu2204-Readme.md` (and 2404, README.md, toolsets) | commit ids recorded in SOURCE.txt | — |
| 3 | 2026-09-13 | docs.github.com | `/en/actions/using-github-hosted-runners/using-github-hosted-runners/about-github-hosted-runners` | saved; no hardware table on this page | hardware table is on the reference page (row 4) |
| 4 | 2026-09-13 | docs.github.com | `/en/actions/reference/runners/github-hosted-runners` | saved; extracted "Standard GitHub-hosted runners for public repositories" table | — |
| 5 | 2026-09-13 | raw.githubusercontent.com | `actions/runner-images/main/README.md`; `images/ubuntu/toolsets/toolset-2404.json`, `toolset-2204.json` | label table; `apt.common_packages` lists | — |
| 6 | 2026-09-13 | docs.mesa3d.org | `envvars.html`, `drivers/llvmpipe.html` | saved; grep `LIBGL_ALWAYS_SOFTWARE`, `MESA_LOADER_DRIVER_OVERRIDE`, `VK_ICD_FILENAMES`, `VK_DRIVER_FILES`, `LP_NUM_THREADS`, `GALLIUM_DRIVER` | `drivers/lavapipe.html` → 404 (no dedicated lavapipe page) |
| 7 | 2026-09-13 | packages.ubuntu.com | `/jammy/<pkg>`, `/noble/<pkg>` for `mesa-vulkan-drivers libgl1-mesa-dri xvfb supertuxkart xonotic 0ad openarena minetest sauerbraten warzone2100 armagetronad darkplaces nexuiz ioquake3 xonotic-data` | versions/components saved | `xonotic`, `xonotic-data`: "No such package"; `/noble/0ad`: "Package not available in this suite"; the site's long-description `div#pdesc` is empty for every page fetched |
| 8 | 2026-09-13 | packages.ubuntu.com | `search?keywords=xonotic&searchon=names&suite=all`, same for `0ad` | xonotic: "your search gave no results"; 0ad present in jammy and noble-updates | — |
| 9 | 2026-09-13 | packages.debian.org | `/bookworm/xonotic` | "No such package" | Xonotic is not packaged in Debian either |
| 10 | 2026-09-13 | packages.ubuntu.com | `/jammy-updates/amd64/{mesa-vulkan-drivers,libgl1-mesa-dri}/filelist`, `/noble-updates/amd64/…/filelist` | lavapipe ICD (`lvp_icd*.json`, `libvulkan_lvp.so`) and `swrast_dri.so` present | — |
| 11 | 2026-09-13 | api.launchpad.net | `getPublishedBinaries` for the same packages (jammy, noble) | versions/pockets confirmed | the publishing-history entry carries no `description` field; JSON discarded |
| 12 | 2026-09-13 | salsa.debian.org | `xorg-team/lib/mesa/-/raw/debian-unstable/debian/control` | `mesa-vulkan-drivers` and `libgl1-mesa-dri` descriptions | control does not name lavapipe/llvmpipe |
| 13 | 2026-09-13 | man7.org | `man5/proc_pid_stat.5`, `proc_pid_status.5`, `proc_pid_task.5`, `proc_pid_wchan.5`, `proc.5` | fields (2),(14),(15),(35),(39)-(42); `voluntary_ctxt_switches`; `task/` semantics | `man5/proc_pid_schedstat.5` → 404; `proc.5` (index page) contains no `schedstat` |
| 14 | 2026-09-13 | raw.githubusercontent.com | `torvalds/linux/master/Documentation/scheduler/sched-stats.rst` | `/proc/<pid>/schedstat` three fields | — |
| 15 | 2026-09-13 | man7.org | `man7/time.7` | `USER_HZ` / `sysconf(_SC_CLK_TCK)` | page does not state the numeric value |
| 16 | 2026-09-13 | raw.githubusercontent.com | `torvalds/linux/master/include/asm-generic/param.h`, `include/uapi/asm-generic/param.h` | `__USER_HZ 100` | — |
| 17 | 2026-09-13 | raw.githubusercontent.com | `torvalds/linux/master/Documentation/admin-guide/perf-security.rst`, `Documentation/trace/ftrace.rst` | paranoid levels; tracefs mount | ftrace.rst has no statement about VM/Azure availability |
| 18 | 2026-09-13 | manpages.ubuntu.com | `noble/man2/perf_event_open.2`, `jammy/man2/perf_event_open.2` | `/proc/sys/kernel/perf_event_paranoid` values 2/1/0/-1 | Ubuntu man page does not document levels 3/4 |
| 19 | 2026-09-13 | WebSearch | `Ubuntu kernel.perf_event_paranoid default value 4 Ubuntu patch "perf_event_paranoid"` | hits: lynis #1376, launchpad bug 2131046, medium post — none primary | not cited |
| 20 | 2026-09-13 | WebSearch | `Ubuntu kernel "perf_event_paranoid" default 4 SAUCE patch "Restrict" perf_event_open unprivileged launchpad` | lore.altlinux.org copy of the "UBUNTU: SAUCE" patch; LWN 696216 | — |
| 21 | 2026-09-13 | git.launchpad.net, kernel.ubuntu.com | `~ubuntu-kernel/ubuntu/+source/linux/+git/noble/plain/kernel/events/core.c`; gitea raw `…/noble/kernel/events/core.c`, `Documentation/admin-guide/sysctl/kernel.rst` | — | launchpad: "403 Forbidden … administrative rules"; gitea: sign-in page. Ubuntu's own `core.c` could not be fetched; the SAUCE patch copy (row 20) is used instead |
| 22 | 2026-09-13 | salsa.debian.org | `kernel-team/linux/-/raw/master/debian/patches/features/all/security-perf-allow-further-restriction-of-perf_event_open.patch` | — | 404 (path guessed) |
| 23 | 2026-09-13 | WebSearch | `github actions runner-images ubuntu ftrace tracefs perf_event_paranoid "perf" not permitted issue` | runner-images issues #4974, #11689, #11789; community discussion #45004 | discussion #45004 not fetched (secondary) |
| 24 | 2026-09-13 | api.github.com | `repos/actions/runner-images/issues/{4974,11689,11789}` + `/comments` | saved JSON | — |
| 25 | 2026-09-13 | raw.githubusercontent.com | `supertuxkart/stk-code/1.4/src/main.cpp`, `src/modes/profile_world.hpp`, `src/audio/sfx_manager.hpp`, `src/network/stk_host.hpp`, `src/main_loop.cpp` | help text; `--profile-laps/--profile-time/--no-graphics` handlers; thread members | no `--benchmark` option exists in 1.4 `main.cpp` |
| 26 | 2026-09-13 | raw.githubusercontent.com | `DarkPlacesEngine/darkplaces/master/host.c`, `cl_demo.c`, `thread.h` | `-benchmark`, `-demo`, `timedemo`; `CL_FinishTimeDemo` | thread.h shows a threading API only; no doc of which threads the engine spawns |
| 27 | 2026-09-13 | raw.githubusercontent.com | `0ad/0ad/master/binaries/system/readme.txt`, `source/ps/TaskManager.h`, `TaskManager.cpp` | `-autostart-nonvisual`, `-replay`; worker count | — |
| 28 | 2026-09-13 | raw.githubusercontent.com | `ioquake/ioq3/main/README.md`, `code/client/cl_main.c` | `timedemo` cvar, `demo` command, `CL_DemoCompleted` output | README has no thread statement |
| 29 | 2026-09-13 | raw.githubusercontent.com | `minetest/minetest/5.6.1/{src/main.cpp,doc/minetest.6,src/client/mesh_generator_thread.h,src/emerge.h,src/server.h,src/client/client.h}` (redirects to luanti-org/luanti) | `--go`, `--random-input`, `--speedtests`; thread classes | — |
| 30 | 2026-09-13 | raw.githubusercontent.com | `Warzone2100/warzone2100/4.4.2/src/clparse.cpp` | `--autogame`, `--headless`, `--skirmish`, `--autohost` | `doc/warzone2100.6.in` → 404 (no such path at 4.4.2) |
| 31 | 2026-09-13 | api.github.com | `repos/ArmagetronAd/armagetronad/git/trees/master?recursive=1` grep `.6` | — | no man page found in tree listing; used Ubuntu man page (row 32) |
| 32 | 2026-09-13 | manpages.ubuntu.com | `noble/man6/{armagetronad,warzone2100,sauerbraten,openarena,supertuxkart,darkplaces,pyrogenesis,0ad,nexuiz,minetest}.6` | armagetronad `--benchmark/--playback/--fastforward`; sauerbraten `-d`; others confirm sources above | warzone2100.6 (noble) lists no `--autogame`/`--headless` |
| 33 | 2026-09-13 | sources.debian.org | `api/src/sauerbraten/0.0.20201227-1/docs/`; `data/non-free/s/sauerbraten/0.0.20201227-1/docs/{game.html,config.html}` | "Demo Recording" section: demo mode `-1` | `raw.githubusercontent.com/cube2/sauerbraten/master/docs/README.html` → 404 |
| 34 | 2026-09-13 | gitlab.winehq.org | `wine/wine/-/wikis/FAQ` (HTML), `FAQ.md` (raw) | grep `Xvfb`, `headless`, `virtual desktop`, `OpenGL`, `3D` | FAQ has no Xvfb/headless entry; `FAQ?format=raw` → 404 |
| 35 | 2026-09-13 | gitlab.winehq.org | `wine/wine/-/raw/master/tools/gitlab/test.yml`, `test-linux`; API `repository/tree?path=tools/gitlab` | Wine's own CI: `LP_NUM_THREADS=4`, xorg `dummy` driver via `startx` | Wine CI does not use Xvfb; uses Xorg dummy |
| 36 | 2026-09-13 | raw.githubusercontent.com | `ValveSoftware/Proton/proton_9.0/README.md` | "tool for use with the Steam client"; install into `compatibilitytools.d`; `PROTON_USE_WINED3D` | README has no explicit "requires a GPU/Vulkan" sentence |
| 37 | 2026-09-13 | developer.valvesoftware.com; web.archive.org | `wiki/SteamCMD` direct (curl and WebFetch) → 403 "Making sure you're not a bot"; `web.archive.org/web/2026id_/…` | Wayback copy saved (gzip-decoded) | live page blocks non-browser fetches |
| 38 | 2026-09-13 | raw.githubusercontent.com | `doitsujin/dxvk/master/README.md` | "using Wine"; requirements | README has no `dxvk-native` section |
| 39 | 2026-09-13 | manpages.ubuntu.com | `noble/man1/Xvfb.1` | DESCRIPTION | — |
| 40 | 2026-09-13 | lwn.net | `Articles/696216/` | Debian/Android level 3 history | — |
| 41 | 2026-09-13 | api.github.com | tag/commit lookups: `stk-code` tag 1.4, `luanti-org/luanti` tag 5.6.1, `warzone2100` tag 4.4.2, `Proton` branch `proton_9.0`, `torvalds/linux` file commits | ids in SOURCE.txt | `repos/minetest/minetest/git/ref/tags/5.6.1` returns nothing (repo renamed); `repos/ValveSoftware/Proton/git/ref/tags/proton_9.0` → no such tag (it is a branch) |

## 2. Candidates

Coverage key: every candidate below covers T6 only unless stated; none covers T1–T5 (no frame-cadence, task-structure, non-dominant-task, lifetime, or LAVD-platform observation). "One observation" answers whether the source is a single measured population/run; documentation sources are marked "not an observation".

### S4-runner-2404 — Ubuntu 24.04 runner image README

- **Citation.** actions/runner-images, `images/ubuntu/Ubuntu2404-Readme.md`, branch `main`, file last commit `cf6f08e1bc2b902d44a33500d2c4c63b65882bce` (2026-09-11). Image Version 20260907.300.1.
- **Copy.** `sources/S4-runner-2404/Ubuntu2404-Readme.md`, SHA-256 `4edbefde1df512f024363b1f66f78448f944f071c9e1775056b220d5bdc8dc81`.
- **Passages.**
  - L8–12: `# Ubuntu 24.04` / `- OS Version: 24.04.5 LTS` / `- Kernel Version: 6.17.0-1022-azure` / `- Image Version: 20260907.300.1` / `- Systemd version: 255.4-1ubuntu8.17`
  - L256 (section `### Installed apt packages`), L329: `| xvfb                   | 2:21.1.12-1ubuntu1.6         |`
  - The apt table (L256–335) contains no row whose name contains `mesa`, `libgl`, `vulkan` or `libgbm` (grep, 0 hits). The README lists explicitly installed apt packages only; it does not enumerate dependency-pulled packages, so absence of a row is not evidence of absence on disk.
- **Coverage.** T6: covers runner software (kernel `6.17.0-1022-azure`, `xvfb` preinstalled); does not state CPU/RAM (see S4-gh-hosted-runners) nor GPU.
- **Observation?** Not an observation; a generated inventory of one image version. Machine named (image version), no game, no window.

### S4-runner-2204 — Ubuntu 22.04 runner image README

- **Citation.** actions/runner-images, `images/ubuntu/Ubuntu2204-Readme.md`, `main`, file last commit `447cb43f71185c500949f3d4a2354f6c5652313b` (2026-09-11). Image Version 20260907.292.1.
- **Copy.** `sources/S4-runner-2204/Ubuntu2204-Readme.md`, SHA-256 `f3bce22f10e370ff599363edc06c6ebb957a85dbd2b00afb7c3681deb3ad34e7`.
- **Passages.**
  - L5 (Announcements): `[[Ubuntu] The Ubuntu 22 based runner images will begin deprecation on September 17th and will be fully unsupported by April 17th for GitHub Actions and Azure DevOps](https://github.com/actions/runner-images/issues/14254)`
  - L8–12: `# Ubuntu 22.04` / `- OS Version: 22.04.5 LTS` / `- Kernel Version: 6.8.0-1064-azure` / `- Image Version: 20260907.292.1` / `- Systemd version: 249.11-0ubuntu3.22`
  - L319: `| libgbm-dev             | 23.2.1-1ubuntu3.1\~22.04.4          |` (a Mesa-sourced package; present on 22.04 apt list, absent from the 24.04 list)
  - L375: `| xvfb                   | 2:21.1.4-2ubuntu1.7\~22.04.16       |`
- **Difference 22.04 vs 24.04 (from the two READMEs).** Kernel `6.8.0-1064-azure` vs `6.17.0-1022-azure`; xvfb `21.1.4` vs `21.1.12`; 22.04 apt list additionally carries `libgbm-dev`, `libgtk-3-0`, `libxss1`, `lib32z1` etc. (L283–380 vs L256–335); 22.04 is announced as deprecating from 2026-09-17.
- **Coverage.** T6 as above. Not an observation.

### S4-runner-toolset — image toolset definitions

- **Citation.** actions/runner-images, `images/ubuntu/toolsets/toolset-2404.json` and `toolset-2204.json`, `main`, last commit `abac76dc78cf571e72be5c0296c061ee7ae594fb` (2026-08-31).
- **Copy.** `sources/S4-runner-toolset/`, SHA-256 `291c28ea…1414` (2404), `58df048e…cdf6f` (2204).
- **Passages.** toolset-2404.json L109 `"apt": {`, L150 `"xvfb",` inside `common_packages`; toolset-2204.json L113 `"apt": {`, L171 `"xvfb",`. Neither file contains the strings `mesa`, `libgl` or `vulkan` (grep, 0 hits).
- **Coverage.** T6: confirms `xvfb` is a deliberately installed package on both images; Mesa is not an explicitly listed package. Not an observation.

### S4-runner-images-readme — label mapping

- **Citation.** actions/runner-images `README.md`, `main`, last commit `148c0a4acb53bb2c7c853446a290aec86b61d3c3` (2026-08-20).
- **Copy.** `sources/S4-runner-images-readme/README.md`, SHA-256 `e2282f1ccf4a8c952433ada336e1eeda9eaffe97592c9b9c334fcaac6115f63d`.
- **Passages.** L25: `| Ubuntu 24.04 … | x64 | `ubuntu-latest` or `ubuntu-24.04` | [ubuntu-24.04] |`; L27: `| Ubuntu 22.04 … | x64 | `ubuntu-22.04` | [ubuntu-22.04] |`; L95: `GitHub Actions and Azure DevOps use the `-latest` YAML label (ex: `ubuntu-latest`, `windows-latest`, and `macos-latest`). These labels point towards the newest stable OS version available.`
- **Coverage.** T6: `ubuntu-latest` = Ubuntu 24.04 at access date. Not an observation.

### S4-gh-hosted-runners — GitHub Docs, hosted-runner hardware

- **Citation.** GitHub Docs, "GitHub-hosted runners reference" (`/en/actions/reference/runners/github-hosted-runners`) and "About GitHub-hosted runners" (`/en/actions/using-github-hosted-runners/using-github-hosted-runners/about-github-hosted-runners`), live pages, no version string.
- **Copy.** `sources/S4-gh-hosted-runners/github-hosted-runners-reference.html` SHA-256 `100765e2943b67d5f7243c187c9d69093a76717e110ffad3d20be428243a1b7c`; `about-github-hosted-runners.html` SHA-256 `bc6b1bbbd57d38c908d9aa8341c8b83ef4cc448d2e4202e6eb7cfb60d1b0e3ea`.
- **Passages** (reference page, section "Standard GitHub-hosted runners for public repositories"; table rendered as text):
  - `For public repositories, jobs using the workflow labels shown in the table below will run with the associated specifications. With the exception of single-CPU runners, each GitHub-hosted runner is a new virtual machine (VM) hosted by GitHub.`
  - Table header and rows: `Virtual machine / container | Processor (CPU) | Memory (RAM) | Storage (SSD) | Architecture | Workflow label` → `Linux | 1 | 5 GB | 14 GB | x64 | ubuntu-slim` ; `Linux | 4 | 16 GB | 14 GB | x64 | ubuntu-latest, ubuntu-24.04, ubuntu-22.04, ubuntu-26.04 (Public preview)`
  - Section "Standard GitHub-hosted runners for private repositories": `Linux | 2 | 8 GB | 14 GB | x64 | ubuntu-latest, ubuntu-24.04, ubuntu-22.04, ubuntu-26.04 (Public preview)`
  - Section "Larger runners" bullet list includes `GPU-powered runners` under `They offer the following advanced features:` — i.e. GPU is a larger-runner feature, not a standard-runner one. No sentence on either page states that standard runners have no GPU; absence of GPU on standard runners is inferred from the table (no GPU column) and the larger-runner list only.
  - Section "Administrative privileges": `The Linux and macOS virtual machines both run using passwordless sudo.`
  - About page, section "Cloud hosts used by GitHub-hosted runners": `GitHub hosts Linux and Windows runners on virtual machines in Microsoft Azure with the GitHub Actions runner application installed. The GitHub-hosted runner application is a fork of the Azure Pipelines Agent.`
- **Coverage.** T6: CPU count (4 public / 2 private), RAM (16 GB / 8 GB), VM on Azure, passwordless sudo. Not an observation.

### S4-mesa-envvars — Mesa environment variables

- **Citation.** The Mesa 3D Graphics Library documentation, "Environment Variables", `https://docs.mesa3d.org/envvars.html`, "latest" build.
- **Copy.** `sources/S4-mesa-envvars/envvars.html` SHA-256 `68ad3fbbb905d02e8c162b8a8cd90a7aac8c5cee248b38682294216d00f3e922` (rendering `envvars.txt`, line numbers below refer to it).
- **Passages.**
  - L30–31: `LIBGL_ALWAYS_SOFTWARE` / `if set to true, always use software rendering`
  - L306–307: `MESA_LOADER_DRIVER_OVERRIDE` / `chooses a different driver binary such as etnaviv or zink.`
  - L736–738: `GALLIUM_DRIVER` / `useful in combination with LIBGL_ALWAYS_SOFTWARE = true for choosing one of the software renderers softpipe or llvmpipe.`
  - L867–870: `LP_NUM_THREADS` / `an integer indicating how many threads to use for rendering. Zero turns off threading completely. The default value is the number of CPU cores present.`
  - L1422–1426: `VK_DRIVER_FILES` / `Force the loader to use the specific driver JSON files. The value contains a list of delimited full path listings to driver JSON Manifest files and/or paths to folders containing driver JSON files. See Vulkan loader docs on environment variables.`
  - L1434–1435: `VK_ICD_FILENAMES` / `Deprecated, replaced by VK_DRIVER_FILES.`
- **Coverage.** T6: how to force llvmpipe (OpenGL) and select the lavapipe ICD (Vulkan); llvmpipe thread count defaults to core count (relevant to the sidecar: the renderer itself adds threads). Not an observation.

### S4-mesa-llvmpipe — Mesa LLVMpipe driver page

- **Citation.** Mesa documentation, "LLVMpipe", `https://docs.mesa3d.org/drivers/llvmpipe.html`, "latest".
- **Copy.** `sources/S4-mesa-llvmpipe/llvmpipe.html` SHA-256 `be53af6c4a6e2bc7e866cbac63b531745c2b0aef7bacd224b0c9984645accebf`.
- **Passages** (section "Introduction", rendering L17–22): `The Gallium LLVMpipe driver is a software rasterizer that uses LLVM to do runtime code generation. Shaders, point/line/triangle rasterization and vertex processing are implemented with LLVM IR which is translated to x86, x86-64, or ppc64le machine code. Also, the driver is multithreaded to take advantage of multiple CPU cores (up to 32 at this time). It's the fastest software rasterizer for Mesa.`
- **Coverage.** T6: llvmpipe is multithreaded (adds rasterizer threads to the observed process). Not an observation. No lavapipe page exists in the docs tree (404).

### S4-ubuntu-pkgs — packages.ubuntu.com pages and file lists

- **Citation.** Ubuntu Packages Search, live pages for suites jammy (22.04 LTS) and noble (24.04 LTS); amd64 file lists for the `-updates` pockets.
- **Copy.** `sources/S4-ubuntu-pkgs/*.html` (28 files; SHA-256 per file in `SOURCE.txt`).
- **Passages** (page header `Package:` line; component in brackets; file-list lines by line number of the saved html):
  - `mesa-vulkan-drivers`: jammy `Package: mesa-vulkan-drivers (23.2.1-1ubuntu3.1~22.04.4 and others) [security]` ; noble `Package: mesa-vulkan-drivers (25.2.8-0ubuntu0.24.04.2 and others) [security]`. Short description: `Mesa Vulkan graphics drivers`.
  - File list jammy-updates/amd64 `mesa-vulkan-drivers`: L51 `/usr/lib/x86_64-linux-gnu/libvulkan_lvp.so`, L64 `/usr/share/vulkan/icd.d/lvp_icd.x86_64.json`. Noble-updates: L53 `/usr/lib/x86_64-linux-gnu/libvulkan_lvp.so`, L69 `/usr/share/vulkan/icd.d/lvp_icd.json`. (lvp = lavapipe ICD; the ICD filename differs between suites, which matters for `VK_DRIVER_FILES`.)
  - `libgl1-mesa-dri`: jammy `(23.2.1-1ubuntu3.1~22.04.4 and others)`, noble `(25.2.8-0ubuntu0.24.04.2 and others)`; short description `free implementation of the OpenGL API -- DRI modules`. File list jammy-updates L49 `/usr/lib/x86_64-linux-gnu/dri/kms_swrast_dri.so`, L54 `/usr/lib/x86_64-linux-gnu/dri/swrast_dri.so`; noble-updates L65 `…/dri/kms_swrast_dri.so`, L90 `…/dri/swrast_dri.so`.
  - `xvfb`: jammy `(2:21.1.4-2ubuntu1.7~22.04.16 and others) [security] [universe]`; noble `(2:21.1.12-1ubuntu1.5 and others) [security] [universe]`; short description `Virtual Framebuffer 'fake' X server`.
  - `supertuxkart`: jammy `(1.3+dfsg1-3) [universe]`; noble `(1.4+dfsg-3ubuntu1) [universe]`.
  - `xonotic`: `No such package.` (jammy, noble); name search across all suites: `Sorry, your search gave no results`.
  - `0ad`: jammy `(0.0.25b-2) [universe]`; `/noble/0ad`: `Package not available in this suite.`; name search: `noble-updates (games): … 0.0.26-6ubuntu0.24.04.1: amd64 arm64 armhf` and `0ad-data … noble (24.04LTS) (games): … 0.0.26-1: all`.
  - `openarena`: jammy `(0.8.8+dfsg-5) [universe]`; noble `(0.8.8+dfsg-7) [universe]`.
  - `minetest`: jammy `(5.4.1+repack-2build1) [universe]`; noble `(5.6.1+dfsg+~1.9.0mt8+dfsg-4build3) [universe]`.
  - `sauerbraten` (Cube 2): jammy and noble `(0.0.20201227-1) [multiverse]`.
  - `warzone2100`: jammy `(4.2.3-3) [universe]`; noble `(4.4.2-1build3) [universe]`.
  - `armagetronad`: jammy `(0.2.9.1.0-2) [universe]`; noble `(0.2.9.1.1-1build2) [universe]`.
  - `darkplaces` (engine used by Xonotic/Nexuiz): noble `(0~20180908~beta1-5build3) [universe]`; `nexuiz`: noble `(2.5.2+dp-9) [universe]`; `ioquake3`: noble `(1.36+u20240217.7d711f8+dfsg-1build2) [universe]`.
- **Coverage.** T6: package availability and versions per suite; lavapipe and swrast modules shipped. Not an observation. Note: the site's long-description block (`div#pdesc`) is empty on every page fetched, so no long description could be quoted.

### S4-debian-mesa — Debian mesa `debian/control`

- **Citation.** Debian X Strike Force, `mesa` packaging, `debian/control`, branch `debian-unstable`, salsa.debian.org (raw endpoint gives no commit id).
- **Copy.** `sources/S4-debian-mesa/control` SHA-256 `79feff733a930b746be26f546ef466525f2dbd1dad680d9c823dbaf0c4f2948c`.
- **Passages.** L270–279: `Package: mesa-vulkan-drivers` … `Provides: vulkan-icd` … `Description: Mesa Vulkan graphics drivers` / ` Vulkan is a low-overhead 3D graphics and compute API. This package` / ` includes Vulkan drivers provided by the Mesa project.` L169–182: `Package: libgl1-mesa-dri` … `Description: free implementation of the OpenGL API -- DRI modules` / ` This version of Mesa provides GLX and DRI capabilities: it is capable of` / ` both direct and indirect rendering.  For direct rendering, it can use DRI` / ` modules from the libgl1-mesa-dri package to accelerate drawing.`
- **Coverage.** T6: package descriptions (Ubuntu inherits them). Neither names lavapipe/llvmpipe; the file lists above are the evidence. Not an observation.

### S4-xvfb-man — Xvfb(1)

- **Citation.** Ubuntu manpages, noble, `Xvfb.1` (xorg-server 21.1.12).
- **Copy.** `sources/S4-xvfb-man/Xvfb.1.noble.html` SHA-256 `cbb6705b867d15a1f1755b1373c81916a3d9d0262fe0a075e65691dbfe36c5f6`.
- **Passage** (DESCRIPTION): `Xvfb is an X server that can run on machines with no display hardware and no physical input devices. It emulates a dumb framebuffer using virtual memory.` … `doing batch processing with Xvfb as a background rendering engine, load testing, …`
- **Coverage.** T6. Not an observation. The man page says nothing about GLX or refresh; no display-refresh notion exists for a memory framebuffer per this text.

### S4-stk — SuperTuxKart 1.4 source

- **Citation.** supertuxkart/stk-code, tag `1.4` (commit `bea5b530a56296e6110e7755a56d79742bd94176`); `src/main.cpp` (last commit at tag `f777e01a217778fe206f74d130fc6514bef11906`, 2022-08-13), `src/modes/profile_world.hpp`, `src/audio/sfx_manager.hpp`, `src/network/stk_host.hpp`, `src/main_loop.cpp`. Same upstream version as Ubuntu noble `supertuxkart 1.4+dfsg-3ubuntu1`.
- **Copy.** `sources/S4-stk/` (SHA-256 in SOURCE.txt; `main.cpp` `d19df64658c46db9862c55115b2e31851707ee05165ae191d1f7f3dd363ea0aa`).
- **Passages.**
  - `main.cpp` L589–592 (help text): `"       --profile-laps=n   Enable automatic driven profile mode for n "` `"laps.\n"` / `"       --profile-time=n   Enable automatic driven profile mode for n "` `"seconds.\n"`
  - L599: `"       --no-graphics      Do not display the actual race.\n"`
  - L1690–1703: `if(CommandLine::has("--profile-laps",  &n))` … `UserConfigParams::m_no_start_screen = true;` / `ProfileWorld::setProfileModeLaps(n);` / `RaceManager::get()->setNumLaps(n);`
  - L1716–1722: `if(CommandLine::has("--profile-time",  &n))` … `UserConfigParams::m_no_start_screen = true;` / `ProfileWorld::setProfileModeTime((float)n);` / `RaceManager::get()->setNumLaps(999999); // profile end depends on time`
  - L2185–2188: `#ifndef SERVER_ONLY` / `        if(CommandLine::has("--no-graphics") || CommandLine::has("-l"))` / `#endif` / `            GUIEngine::disableGraphics();`
  - `profile_world.hpp` L34: `enum        ProfileType {PROFILE_NONE, PROFILE_TIME, PROFILE_LAPS};`; L39–40: `/** In time based profiling only: time to run. */` `static float m_time;`
  - Threads: `sfx_manager.hpp` L219–220: `/** Thread id of the thread running in this object. */` / `std::thread               m_thread;`; `stk_host.hpp` L81 `std::thread m_client_loop_thread;`, L87 `std::thread m_network_console;`, L114 `std::thread m_listening_thread;`
  - Frame pacing: `main_loop.cpp` L316–318: `const int max_fps =` / `UserConfigParams::m_swap_interval == 2 ? UserConfigParams::m_max_fps :` …; L327–334: `if (!m_throttle_fps || current_fps <= max_fps ||` … `int wait_time = 1000 / max_fps - 1000 / current_fps;` … `StkTime::sleep(wait_time);`
- **Coverage.** T6: a fixed AI-driven workload (`--profile-laps=n` / `--profile-time=n`) exists; `--no-graphics` disables rendering; the game has at least an audio thread and network threads besides the main loop; the main loop self-throttles to `m_max_fps` by sleeping. There is no `--benchmark` option in 1.4. Not an observation.

### S4-ubuntu-manpages — game man pages (noble)

- **Citation.** Ubuntu manpages, noble, section 6: `armagetronad.6`, `sauerbraten.6`, `openarena.6`, `supertuxkart.6`, `darkplaces.6`, `pyrogenesis.6`/`0ad.6`, `nexuiz.6`, `minetest.6`, `warzone2100.6`.
- **Copy.** `sources/S4-ubuntu-manpages/` (SHA-256 per file in SOURCE.txt).
- **Passages.**
  - `armagetronad.6` SYNOPSIS: `armagetronad [ -h, --help ] [ -v, --version ] [ --doc ] [ -f, --fullscreen ] [ -w, --window, --windowed ] [ --fastforward ] [ --benchmark ] [ --record ] [ --playback ]`; OPTIONS: `--fastforward TIME Lets time run very fast until the given time is reached.` / `--benchmark Renders frames as they were recorded.` / `--record FILENAME Creates a DEBUG recording while running.` / `--playback FILENAME Plays back a DEBUG recording.`
  - `sauerbraten.6` OPTIONS: `-d Run as a dedicated server and don't start the client.` (no demo/benchmark option on the command line).
  - `openarena.6`: `Options that can be set with +set (note that this is not a full list!) include: r_fullscreen <bool> 1: Play in fullscreen mode; 0: Play in window mode r_mode <num> …` (no timedemo mention; see S4-ioq3).
  - `darkplaces.6`: `-dedicated Run as a dedicated server, without the GUI.` (no `-benchmark` in the man page; see S4-xonotic).
  - `supertuxkart.6`: same text as `main.cpp` help (`--no-graphics Do not display the actual race.`, `--profile-laps=n`, `--profile-time=n`).
  - `0ad.6`/`pyrogenesis.6`: `-autostart Load a map instead of showing main menu (see below).` (older option list than the readme; `-autostart-nonvisual` absent from this man page).
  - `minetest.6`: `--go Disable main menu` / `--random-input Enable random user input, for testing (client only)` / `--speedtests Run speed tests`.
  - `warzone2100.6`: `--fullscreen Play in fullscreen mode.` … (the noble man page lists no `--autogame`/`--headless`; see S4-wz2100).
- **Coverage.** T6: Armagetron Advanced has a documented deterministic playback (`--playback`) and render-as-recorded (`--benchmark`) mode. Not an observation.

### S4-xonotic — DarkPlaces engine (Xonotic/Nexuiz) timedemo

- **Citation.** DarkPlacesEngine/darkplaces, `master`; `host.c` last commit `0435530735836f65cb6c9c2ddb271e35813a17df` (2025-04-06); `cl_demo.c` last commit `ca9d3d8cbc29233c21894c46cd1ad9e49313d395` (2024-08-28). Xonotic is not in Ubuntu; the same engine ships as Ubuntu `darkplaces` and drives `nexuiz`.
- **Copy.** `sources/S4-xonotic/` (`darkplaces-host.c` SHA-256 `a9f962fc05c0febdcb332e4502ab90aa23ae685ecdfa3c0c6588200744546b71`; `darkplaces-cl_demo.c` `59e274cb900ebd01e120ecc20235abab1e3c224e053ae1d93468d3ddda941cdc`).
- **Passages.**
  - `host.c` L513–518: `// COMMANDLINEOPTION: Client: -benchmark <demoname> runs a timedemo and quits, results of any timedemo can be found in gamedir/benchmark.log (for example id1/benchmark.log)` / `i = Sys_CheckParm("-benchmark");` … `Cbuf_AddText(cmd_local, va(vabuf, sizeof(vabuf), "timedemo %s\n", sys.argv[i + 1]));`
  - L523–528: `// COMMANDLINEOPTION: Client: -demo <demoname> runs a playdemo and quits` … `"playdemo %s\n"`
  - L401–402: `if (Sys_CheckParm("-benchmark"))` / `srand(0); // predictable random sequence for -benchmark`
  - `cl_demo.c` L607–616: `CL_TimeDemo_f` / `timedemo [demoname]` … `Con_Print("timedemo <demoname> : gets demo speeds\n");`
  - L521–522: `// LadyHavoc: timedemo now prints out 7 digits of fraction, and min/avg/max` / `Con_Printf("%i frames %5.7f seconds %5.7f fps, one-second fps min/avg/max: %.0f %.0f %.0f (%i seconds)\n", frames, time, totalfpsavg, fpsmin, fpsavg, fpsmax, cls.td_onesecondavgcount);`
  - L524: `Log_Printf("benchmark.log", "date %s | enginedate %s | demo %s | commandline %s | run %d | result %i frames …`
- **Coverage.** T6: `-benchmark <demo>` is a fixed, input-free workload that exits and logs aggregate fps (frame count, total time, one-second min/avg/max) — not per-frame times. Thread population is not documented in these files (`thread.h` is only a wrapper API). Not an observation.

### S4-ioq3 — ioquake3 (OpenArena engine) timedemo

- **Citation.** ioquake/ioq3, `main`, `code/client/cl_main.c` last commit `b75bee106481f955898072010d30912facfbb36a` (2026-07-08); `README.md`. Ubuntu `openarena 0.8.8` is built on this engine (Ubuntu also ships `ioquake3`).
- **Copy.** `sources/S4-ioq3/cl_main.c` SHA-256 `b9a8e49c5b105d7a5be8ed0df4ec67cc5b256fc47d04b816b173689a91d9e792`.
- **Passages.**
  - L3575–3576: `cl_timedemo = Cvar_Get ("timedemo", "0", 0);` / `cl_timedemoLog = Cvar_Get ("cl_timedemoLog", "", CVAR_ARCHIVE);`
  - L3722: `Cmd_AddCommand ("demo", CL_PlayDemo_f);`
  - L870–891 (`CL_DemoCompleted`): `if( cl_timedemo && cl_timedemo->integer )` … `// Millisecond times are frame durations:` / `// minimum/average/maximum/std deviation` / `Com_sprintf( buffer, sizeof( buffer ), "%i frames %3.1f seconds %3.1f fps %d.0/%.1f/%d.0/%.1f ms\n", clc.timeDemoFrames, time/1000.0, clc.timeDemoFrames*1000.0 / time, clc.timeDemoMinDuration, time / (float)clc.timeDemoFrames, clc.timeDemoMaxDuration, CL_DemoFrameDurationSDev( ) );`
  - L893–895: `// Write a log of all the frame durations` / `if( cl_timedemoLog && strlen( cl_timedemoLog->string ) > 0 )`
- **Coverage.** T6: `+set timedemo 1 +demo <name>` gives a fixed workload; with `cl_timedemoLog` set the engine writes per-frame durations (the only game here documented to log per-frame times). No thread statement in README. Not an observation.

### S4-0ad — 0 A.D. command line and task manager

- **Citation.** 0ad/0ad GitHub mirror, `master`; `binaries/system/readme.txt` last commit `c8ef1f02b0c3bf231d8ebd22953e034f3e7b17d3` (2023-06-14); `source/ps/TaskManager.h` last commit `657fb096fb3b21b65cf731037a37dc48f8135e0d` (2023-12-03); `source/ps/TaskManager.cpp`.
- **Copy.** `sources/S4-0ad/` (`readme.txt` SHA-256 `342933f9e3cd1677f3febbf200118097c9d8cd2eb0c412a3e7906330161369ca`).
- **Passages.**
  - `readme.txt` L4: `-autostart=...      load a map instead of showing main menu (see below)`; L13: `-autostart-ai=PLAYER:AI         sets the AI for PLAYER (e.g. 2:petra)`; L16: `-autostart-player=NUMBER        sets the playerID in non-networked games (default 1, use -1 for observer)`; L20: `-autostart-nonvisual            disable any graphics and sounds`; L51: `-nosound            disable audio`; L53: `-vsync              enable VSync, i.e. lock FPS to monitor refresh rate`; L67: `-replay=PATH        non-visual replay of a previous game, used for analysis purposes`
  - `TaskManager.h` L35–36: ` * The task manager creates all worker threads on initialisation,` / ` * and manages the task queues.`
  - `TaskManager.cpp` L50: `constexpr size_t MAX_WORKERS = 32;`; L52–56: `size_t GetDefaultNumberOfWorkers()` / `{` / `const size_t hardware_concurrency = std::thread::hardware_concurrency();` / `return hardware_concurrency ? Clamp(hardware_concurrency - 1, MIN_WORKERS, MAX_WORKERS) : MIN_WORKERS;` / `}`
- **Coverage.** T6: fixed AI-vs-AI workload (`-autostart … -autostart-ai=1:petra -autostart-ai=2:petra -autostart-player=-1`, readme example 3), either rendered or `-autostart-nonvisual`; worker-thread pool sized `hardware_concurrency - 1` (= 3 on a 4-vCPU runner). Ubuntu ships 0.0.25b (jammy) and 0.0.26 (noble-updates), older than this readme's revision. Not an observation.

### S4-minetest — Minetest 5.6.1

- **Citation.** minetest/minetest (now luanti-org/luanti), tag `5.6.1` (tag object `5dcbdac45984b2db648d0e61b4bc067e58d75c8c`); `src/main.cpp`, `doc/minetest.6`, `src/client/mesh_generator_thread.h`, `src/emerge.h`, `src/server.h`, `src/client/client.h`. Same upstream version as Ubuntu noble `minetest 5.6.1+…`.
- **Copy.** `sources/S4-minetest/` (`main.cpp` SHA-256 `5a6e5e3b8113eb7f5b96468a977f6b3016b7d52394abdbcc6f86b3671d3ce199`).
- **Passages.**
  - `main.cpp` L332–333: `allowed_options->insert(std::make_pair("speedtests", ValueSpec(VALUETYPE_FLAG,` / `_("Run speed tests"))));`; L336–337: `…("random-input", ValueSpec(VALUETYPE_FLAG,` / `_("Enable random user input, for testing"))));`; L346–347: `…("go", ValueSpec(VALUETYPE_FLAG,` / `_("Disable main menu"))));`
  - `minetest.6` CLIENT OPTIONS: `--go Disable main menu` / `--random-input Enable random user input, for testing (client only)` / `--speedtests Run speed tests`
  - Threads: `mesh_generator_thread.h` L114 `class MeshUpdateThread : public UpdateThread`; `client.h` L489 `MeshUpdateThread m_mesh_update_thread;`; `emerge.h` L198 `std::vector<EmergeThread *> m_threads;`; `server.h` L73 `class ServerThread;`, L627 `ServerThread *m_thread = nullptr;`
- **Coverage.** T6: `--go --random-input` runs without a menu with synthetic input (random, not a fixed replay); the client process hosts a server thread, emerge (map-generation) threads and a mesh-update thread. Not an observation.

### S4-wz2100 — Warzone 2100 4.4.2 command line

- **Citation.** Warzone2100/warzone2100, tag `4.4.2` → commit `bb5d641f107285bb814d907ca019e086e9f65001`; `src/clparse.cpp` last commit `1d9fd6f97850689e2eb7ae99684dcc67e0db9e65` (2023-11-18). Same upstream version as Ubuntu noble `warzone2100 4.4.2-1build3`.
- **Copy.** `sources/S4-wz2100/clparse.cpp` SHA-256 `0c4b5dddf40f6cd8d8ac4a24dc2b0a37846b42f0b7368ecdacb1bb41d2f076fd`.
- **Passages.** L425: `{ "autogame", POPT_ARG_NONE, CLI_AUTOGAME,   N_("Run games automatically for testing"), nullptr },`; L426: `{ "headless", POPT_ARG_NONE, CLI_AUTOHEADLESS,   N_("Headless mode (only supported when also specifying --autogame, --autohost, --skirmish)"), nullptr },`; L428: `{ "skirmish", POPT_ARG_STRING, CLI_SKIRMISH,   N_("Start skirmish game with given settings file"), N_("test") },`; L403: `{ "nosound", POPT_ARG_NONE, CLI_NOSOUND,    N_("Disable sound"),                     nullptr },`; L409: `{ "gfxbackend", POPT_ARG_STRING, CLI_GFXBACKEND, N_("Set gfx backend"),`
- **Coverage.** T6: `--autogame` (AI-driven) with or without `--headless`; `--skirmish <file>` fixes the setup. Thread structure not documented in this file. Not an observation.

### S4-sauerbraten — Cube 2: Sauerbraten docs

- **Citation.** Sauerbraten 2020-12-27 release, `docs/game.html`, `docs/config.html`, from Debian source `sauerbraten 0.0.20201227-1` (sources.debian.org; identical upstream version to the Ubuntu package).
- **Copy.** `sources/S4-sauerbraten/game.html` SHA-256 `45321389e39d6a12910cf59b111bbc6ee844498a876906fae0bd03993c23f140`.
- **Passage** (game.html, section "Demo Recording"): `You may record server-side demos during multiplayer games. You must have gained "admin" privileges by using the "setmaster" command to enable demo recording for a match.` … `Demos may be played back via the special local "demo" mode (mode -1), where the map name is the name of the demo to be played.` … `stopdemo … If used during local demo playback, this will stop demo playback.`
- **Coverage.** T6: demo playback exists but only as an in-game console mode, no command-line benchmark/timedemo switch (man page offers `-d` dedicated only); no thread documentation. Not an observation.

### S4-wine-faq — Wine FAQ and Wine's own CI environment

- **Citation.** WineHQ GitLab wiki "FAQ" (`wine/wine/-/wikis/FAQ.md`, live); Wine `tools/gitlab/test.yml` and `tools/gitlab/test-linux`, branch `master` (raw endpoint, no commit id).
- **Copy.** `sources/S4-wine-faq/FAQ.raw.md` SHA-256 `6814558f015f2ebd3980ab319faa828647a60badebb04fed407c90a93f56e78c`; `gitlab-test.yml` SHA-256 `fe7582dbbff9727d5a171f35064c102d0bde5c65f61902ea4ecf083040a64f29`.
- **Passages.**
  - FAQ L841: `#### How do I get Wine to launch an application in a virtual desktop?` (a Wine-internal desktop window; not headless).
  - FAQ L1261–1265: `### My 3D application/game is very slow (FPS)` / `Usually a 3D performance issue, indicates that something is wrong with your OpenGL 3D drivers. See [3D Driver Issues](3D-Driver-Issues) for more information.`
  - The FAQ contains no occurrence of `Xvfb`, `headless` or `software render` (grep, 0 hits).
  - `test.yml` L25: `- export DISPLAY=:0`; L27: `- export LP_NUM_THREADS=4`; L30–36: `cat >$HOME/xorg.conf << EOF` / `Section "Device"` / `Identifier "dummy"` / `Driver "dummy"` / `VideoRam 32768` / `EndSection`; L38: `- startx -- -config $HOME/xorg.conf $DISPLAY & while ! pgrep fvwm >/dev/null 2>&1; do sleep 1; done`
- **Coverage.** T6: Wine's own test CI runs under an Xorg `dummy` device (no GPU) with `LP_NUM_THREADS` set, i.e. Mesa llvmpipe — evidence that Wine runs and renders on a GPU-less X server; the Wine FAQ itself documents nothing about Xvfb or headless use. Not an observation of a game.

### S4-proton-readme — Proton README

- **Citation.** ValveSoftware/Proton, branch `proton_9.0` (head `2c620c0fd7c2c424f6bd91898602bdc4d4260468`, 2025-06-05), `README.md` last commit `3ffb520d58f1dc876bb6fded7645d14dbd5128af` (2024-08-15).
- **Copy.** `sources/S4-proton-readme/README.md` SHA-256 `67d272bfa00c86bc620f10461f91c68041a34aca30d450e576eac3626a532d5b`.
- **Passages.** L4–6: `**Proton** is a tool for use with the Steam client which allows games which are exclusive to Windows to run on the Linux operating system. It uses Wine to facilitate this.`; L8: `**Most users should use Proton provided by the Steam Client itself.**`; L170–173: `Steam ships with several versions of Proton, which games will use by default or that you can select in Steam Settings' Steam Play page. Steam also supports running games with local builds of Proton, which you can install on your system.`; L175–177: `To install a local build of Proton into Steam, make a new directory in `~/.steam/root/compatibilitytools.d/` with a tool name of your choosing …`; L181: `restart the Steam client for it to pick up on a new tool.`; L263–264: `The Steam client sets some options for known games using the `STEAM_COMPAT_CONFIG` variable.`; L291: `| `wined3d` | `PROTON_USE_WINED3D` | Use OpenGL-based wined3d instead of Vulkan-based DXVK for d3d11, d3d10, and d3d9. |`
- **Coverage.** T6: Proton is defined and installed as a Steam-client tool; the README documents no standalone run path and no GPU/Vulkan requirement sentence. Not an observation.

### S4-steamcmd — SteamCMD (Valve Developer Community)

- **Citation.** Valve Developer Community wiki, "SteamCMD", Wayback Machine capture (`web.archive.org/web/2026id_/…`); the live page returns a bot-check to non-browser fetches.
- **Copy.** `sources/S4-steamcmd/SteamCMD.archive.html` SHA-256 `980b2d15827364d70b91579ed9ba1e006c9e20a732b462a8b3dff51859b90571`.
- **Passages.** Lead: `The Steam Console Client or SteamCMD is a command-line version of the Steam Client. Its primary use is to install and update various dedicated servers available on Steam using a command-line interface. It works with games that use the SteamPipe content system.`; section "SteamCMD Login": `To download most game servers, you can login anonymously using login anonymous`; `Some servers require you to login with a Steam Account.`; `Note: A user can only be logged in once at any time (counting both graphical client as well as SteamCMD logins).`; `If Steam Guard is activated on the user account, check your e-mail for a Steam Guard access code and enter it.`; section "Known Issues": `If you get the "No subscription" error, the game/server you are trying to download either requires a login or that you have purchased the game.`
- **Coverage.** T6: SteamCMD is a content-install tool for dedicated servers, not a runtime for Proton; game downloads need an owning, Steam-Guard-capable account. No source found that documents driving the graphical `steam` client headlessly on a runner (see Not found). Not an observation.

### S4-dxvk — DXVK README

- **Citation.** doitsujin/dxvk, `master`, `README.md` last commit `eeb5d83a922a529fff332212a946737d5dce71a0` (2026-07-12).
- **Copy.** `sources/S4-dxvk/README.md` SHA-256 `cddb299b327467c04f9d6f70e12be5b0db87c605a1d6a6cc705ffa7a1d871c6e`.
- **Passages.** L3: `A Vulkan-based translation layer for Direct3D 8/9/10/11 which allows running 3D applications on Linux using Wine.`; L44: `Before reporting an issue, please check the [Wiki](https://github.com/doitsujin/dxvk/wiki/Driver-support) page on the current driver status and make sure you run a recent enough driver version for your hardware.`; L97–98: `By default, this will use `%LOCALAPPDATA%/dxvk` in a Windows` / `or Wine environment, and `$HOME/.cache` or `$XDG_CACHE_HOME` in a native Linux environment.`; L114–115: `### Requirements:` / `- [wine 10.0](https://www.winehq.org/) or newer`
- **Coverage.** T6: the README mentions a "native Linux environment" only for cache paths; it has no `dxvk-native` section and no statement on lavapipe. Not an observation.

### S4-proc5 — proc(5) split pages, Linux man-pages 6.19

- **Citation.** Linux man-pages 6.19 (2026-02-08): `proc_pid_stat(5)`, `proc_pid_status(5)`, `proc_pid_task(5)`, `proc_pid_wchan(5)`.
- **Copy.** `sources/S4-proc5/` (SHA-256 per file in SOURCE.txt; `proc_pid_stat.5.html` `0f04d78946538fd84db1536845abeb236da51a04844989f34ea7ee7cb0b6700f`).
- **Passages** (`proc_pid_stat(5)`, field list):
  - `(2) comm %s The filename of the executable, in parentheses. Strings longer than TASK_COMM_LEN (16) characters (including the terminating null byte) are silently truncated.`
  - `(14) utime %lu Amount of time that this process has been scheduled in user mode, measured in clock ticks (divide by sysconf(_SC_CLK_TCK)).`
  - `(15) stime %lu Amount of time that this process has been scheduled in kernel mode, measured in clock ticks (divide by sysconf(_SC_CLK_TCK)).`
  - `(20) num_threads %ld Number of threads in this process (since Linux 2.6).`
  - `(35) wchan %lu [PT] This is the "channel" in which the process is waiting. It is the address of a location in the kernel where the process is sleeping. The corresponding symbolic name can be found in /proc/pid/wchan.`
  - `(39) processor %d (since Linux 2.2.8) CPU number last executed on.`
  - `(40) rt_priority %u … (41) policy %u (since Linux 2.5.19) Scheduling policy (see sched_setscheduler(2)).`
  - `(42) delayacct_blkio_ticks %llu (since Linux 2.6.18) Aggregated block I/O delays, measured in clock ticks (centiseconds).`
  - `proc_pid_status(5)`: example lines `Threads:        1`, `voluntary_ctxt_switches:        150`, `nonvoluntary_ctxt_switches:     545`; field text: `voluntary_ctxt_switches` / `nonvoluntary_ctxt_switches` / `Number of voluntary and involuntary context switches (since Linux 2.6.23).`; `Name Command run by this process. Strings longer than TASK_COMM_LEN (16) characters (including the terminating null byte) are silently truncated.`
  - `proc_pid_task(5)`: `/proc/pid/task/ (since Linux 2.6.0) This is a directory that contains one subdirectory for each thread in the process. The name of each subdirectory is the numerical thread ID (tid) of the thread (see gettid(2)). Within each of these subdirectories, there is a set of files with the same names and contents as under the /proc/pid directories.` … `In a multithreaded process, the contents of the /proc/pid/task directory are not available if the main thread has already terminated (typically by calling pthread_exit(3)).`
  - `proc_pid_wchan(5)`: `/proc/pid/wchan (since Linux 2.6.0) The symbolic name corresponding to the location in the kernel where the process is sleeping. Permission to access this file is governed by a ptrace access mode PTRACE_MODE_READ_FSCREDS check; see ptrace(2).`
- **Coverage.** T6: what a sidecar can read per thread (comm 15 chars + NUL, utime/stime in ticks, ctxt-switch counters, wchan, last CPU, policy); man7.org has no `schedstat` page (404) — see S4-sched-stats. Not an observation.

### S4-sched-stats — kernel scheduler statistics doc

- **Citation.** Linux kernel `Documentation/scheduler/sched-stats.rst`, torvalds/linux `master`, file last commit `d3f825032091fc14c7d5e34bcd54317ae4246903` (2025-04-30).
- **Copy.** `sources/S4-sched-stats/sched-stats.rst` SHA-256 `6c80bd9a62d50aa37161d6d909dfeff8c460c3b949454bf4c093c211f6252335`.
- **Passage** L190–198: `/proc/<pid>/schedstat` / `---------------------` / `schedstats also adds a new /proc/<pid>/schedstat file to include some of` / `the same information on a per-process level.  There are three fields in` / `this file correlating for that process to:` / `1) time spent on the cpu (in nanoseconds)` / `2) time spent waiting on a runqueue (in nanoseconds)` / `3) # of timeslices run on this cpu`
- **Coverage.** T6: per-task (via `task/<tid>/schedstat`, per S4-proc5 `task/` semantics) cumulative run time and runqueue wait in nanoseconds plus a schedule count; per-schedule CPU is obtainable only as differences of these cumulative counters between samples, not as individual schedule lengths. Not an observation.

### S4-kernel-param / S4-time7 — clock-tick resolution

- **Citation.** torvalds/linux `master`, `include/uapi/asm-generic/param.h` and `include/asm-generic/param.h` (last commit `f65bbf05392b44714ccdcc4b5b1bebfd471d2665`, 2025-06-25); Linux man-pages 6.19 `time(7)`.
- **Copy.** `sources/S4-kernel-param/uapi-param.h` SHA-256 `aebe74d8dfe3078a039a3a5faad35d9840c67e6472239e78bd8340bb6deaebfe`; `sources/S4-time7/time.7.html` SHA-256 `c56893ad9937adcc0e23841e9904b1555d39717d3914dc6741ca9b662264a035`.
- **Passages.** `uapi-param.h` L5–7: `#ifndef __USER_HZ` / `#define __USER_HZ	100` / `#endif`; `param.h` L9–10: `# define USER_HZ	__USER_HZ	/* some user interfaces are */` / `# define CLOCKS_PER_SEC	(USER_HZ)       /* in "ticks" like times() */`; `time(7)`: `The times(2) system call is a special case. It reports times with a granularity defined by the kernel constant USER_HZ. User-space applications can determine the value of this constant using sysconf(_SC_CLK_TCK).`
- **Coverage.** T6: `utime`/`stime` in `/proc/*/stat` are 10 ms ticks (USER_HZ = 100 on asm-generic); `schedstat` is nanoseconds. Not an observation.

### S4-perf-security — kernel perf security and ftrace docs

- **Citation.** torvalds/linux `master`, `Documentation/admin-guide/perf-security.rst` (last commit `a15cb2c1658417f9e8c7e84fe5d6ee0b63cbb9b0`, 2021-02-11) and `Documentation/trace/ftrace.rst` (last commit `b0c857049153680e1b6ccb59abf359a4ca523561`, 2026-08-11).
- **Copy.** `sources/S4-perf-security/` (perf-security.rst SHA-256 `080dc302bb2ed254192522e1b78d65d71a965d4d893634b052e595d65c6c9383`; ftrace.rst `17dc4ebc317ca03d261146421c6d9235b0e5d25d929706eecdf2f0bb18420cc8`).
- **Passages.** perf-security.rst L226–227: `perf_events *scope* and *access* control for unprivileged processes` / `is governed by perf_event_paranoid [2]_ setting:`; L237–239: `>=0:` / `*scope* includes per-process and system wide performance monitoring` / `but excludes raw tracepoints and ftrace function tracepoints`; L246–247: `>=1:` / `*scope* includes per-process performance monitoring only and` / `excludes system wide performance monitoring.`; L254–256: `>=2:` / `*scope* includes per-process performance monitoring only. CPU and` / `system events happened when executing in user space only can be` / `monitored`. ftrace.rst L49–50: `Ftrace uses the tracefs file system to hold the control files as` / `well as the files to display output.`; L52–53: `When tracefs is configured into the kernel (which selecting any ftrace` / `option will do) the directory /sys/kernel/tracing will be created.`; L60: ` mount -t tracefs nodev /sys/kernel/tracing`.
- **Coverage.** T6: upstream semantics only; ftrace.rst says nothing about VMs, Azure, or permissions beyond the mount. Not an observation.

### S4-ubuntu-perf-paranoid — Ubuntu perf_event_open(2)

- **Citation.** Ubuntu manpages, noble and jammy, `perf_event_open(2)`.
- **Copy.** `sources/S4-ubuntu-perf-paranoid/perf_event_open.2.noble.html` SHA-256 `45e8221b6e0727e74e96e59177d17fe75df5604643cfb532b95d895b034e1068`.
- **Passage** (section "Files in /proc/sys/kernel/"): `/proc/sys/kernel/perf_event_paranoid The perf_event_paranoid file can be set to restrict access to the performance counters.` / `2 allow only user-space measurements (default since Linux 4.6).` / `1 allow both kernel and user measurements (default before Linux 4.6).` / `0 allow access to CPU-specific data but not raw tracepoint samples.` / `-1 no restrictions.`
- **Coverage.** T6: the Ubuntu-shipped man page does not document levels 3 or 4. Not an observation.

### S4-ubuntu-kernel-paranoid — the "UBUNTU: SAUCE" perf restriction patch (copy)

- **Citation.** Patch "UBUNTU: SAUCE: security,perf: Allow further restriction of perf_event_open", From: Ben Hutchings; Signed-off-by Ben Hutchings, Tim Gardner (Canonical), Seth Forshee (Canonical), Vitaly Chikunov (ALT Linux, "[ vt: Make it default y. ]"); as posted to the ALT Linux devel-kernel list 2022-06-02 (`lore.altlinux.org/devel-kernel/20220602003100.524482-1-vt@altlinux.org`). This is a third-party repost of the Ubuntu kernel patch; Ubuntu's own git could not be fetched (search log rows 21–22), so the Ubuntu default is not verified against Ubuntu's primary tree.
- **Copy.** `sources/S4-ubuntu-kernel-paranoid/altlinux-lore-ubuntu-sauce.txt` SHA-256 `37abdb932c0bfc935f9c59e48cf1e039b36b3b3f32489fc4ff5703100f5b4974`.
- **Passages.** L40–43: `When kernel.perf_event_open is set to 3 (or greater), disallow all` / `access to performance events by users without CAP_SYS_ADMIN.` / `Add a Kconfig symbol CONFIG_SECURITY_PERF_EVENTS_RESTRICT that` / `makes this value the default.`; L70–75: `+#define PERF_SECURITY_MAX		4` / `+` / `+static inline bool perf_paranoid_any(void)` / `+{` / `+	return sysctl_perf_event_paranoid >= PERF_SECURITY_MAX;` / `+}`; L86–93: ` *   2 - disallow kernel profiling for unpriv` / `+ *   4 - disallow all unpriv perf event use` / ` */` / `+#ifdef CONFIG_SECURITY_PERF_EVENTS_RESTRICT` / `+int sysctl_perf_event_paranoid __read_mostly = PERF_SECURITY_MAX;` / `+#else` / ` int sysctl_perf_event_paranoid __read_mostly = 2;` / `+#endif`; L101–102: `+	if (perf_paranoid_any() && !capable(CAP_SYS_ADMIN))` / `+		return -EACCES;`
- **Coverage.** T6: explains the value 4 seen on Ubuntu kernels (level 4 = no unprivileged perf at all; root/CAP_SYS_ADMIN unaffected). Not an observation.

### S4-lwn-696216 — LWN, "Disallowing perf_event_open()"

- **Citation.** Jake Edge, LWN.net, 2016-08-03, `https://lwn.net/Articles/696216/`.
- **Copy.** `sources/S4-lwn-696216/lwn-696216.html` SHA-256 `c676ebf480da3254d5c8e37046a81d6fad7a8062a43577d03327c5f487f38a36`.
- **Passages.** `The patch simply provides another setting for the kernel.perf_event_paranoid sysctl parameter to disallow unprivileged processes from accessing the perf_event_open() system call at all. It is currently used in both Android and Debian kernels…`; `It adds a another value that can be set for the sysctl parameter (i.e. kernel.perf_event_paranoid=3) that restricts perf_event_open() to processes with the CAP_SYS_ADMIN capability.`; `he said it had been running in the Debian kernel since August 2015 with no complaints.`
- **Coverage.** T6: history of the >2 level (Debian/Android). Not an observation.

### S4-runner-perf-issues — actions/runner-images issues on perf

- **Citation.** GitHub issues actions/runner-images #4974 (AlexTMjugador, 2022-01-30, closed), #11689 (visheshruparelia, 2025-02-28, closed), #11789 (Luni-4, 2025-03-13, closed), with maintainer comments.
- **Copy.** `sources/S4-runner-perf-issues/*.json` (SHA-256 in SOURCE.txt).
- **Passages.**
  - #4974 title: `[Ubuntu] The `perf_event_open` syscall may not work, returning EPERM (permission denied)`; body: `Interestingly enough, the default value of that sysctl reads 4, which is not documented in the upstream kernel docs … as a value that has any different meaning than 2.` … `Image version: 20220123.1` (Ubuntu 20.04); `The perf subsystem does not work. `perf stat ls` shows that some performance counters are not available, but they work on my Linux box for privileged processes`.
  - #4974 comment (mikhailkoliada, 2022-02-01): `Github-hosted runner images (Ubuntu and Windows specifically) are generated on the top of Ubuntu/Windows images from Azure marketplace, perf is a part of the linux kernel which we do not modify at all, in practice this means that if you try the same perf commands on a clean Ubuntu VM in Azure the result is going to be literally the same. Please file a support request against Azure directly.`
  - #11689 body: `I have set the `kernel.perf_event_paranoid=1` and `kernel.kptr_restrict=0`. Upon running the command: `sudo perf record -g -e cycles -a -o perf.data sleep 5` it collects no samples in case of Linux ARM runners. The same command works just fine in Linux x64 runners.`; repro steps: `run: sudo apt-get install linux-tools-generic` / `run: sudo sysctl kernel.perf_event_paranoid=1` / `run: sudo perf record -g -e cycles -a -o perf.data sleep 5`.
  - #11689 comment (apangin, 2025-03-05): `The same happens with all PERF_TYPE_HARDWARE events, such as `instructions`, `cache-misses` etc.  `cpu-clock` works well, but it is a software event (`PERF_TYPE_SOFTWARE`).` (about ARM runners).
  - #11789 body: `Run sudo perf stat --timeout 10000 -ae power/energy-cores/,power/energy-pkg/,power/energy-psys/` → `Unable to find PMU or event on a PMU of 'power'` (Ubuntu 24.04 image 20250309.1.0); comment (RaviAkshintala, 2025-03-19): `Currently, our runner images are using kernel version `6.8.0-1021-azure`.`
- **Coverage.** T6: on x64 runners `sudo sysctl kernel.perf_event_paranoid=1` followed by `sudo perf record -e cycles -a` is reported to work (#11689, as the contrast case); hardware PMU events are absent/unavailable on the Azure VM (#4974, #11789); the sysctl default reads 4 (#4974, 2022, Ubuntu 20.04). Nothing found on ftrace/`/sys/kernel/tracing` specifically. These are user reports = observations on named runner images, with no game and no window; #11689 is the only one with a reproducible workflow.

## 3. Not found

- **T6 — Xonotic in Ubuntu.** `packages.ubuntu.com` search (all suites) and `packages.debian.org/bookworm/xonotic`: no package. Only the DarkPlaces engine (`darkplaces`) and Nexuiz (`nexuiz`) are packaged; Xonotic would have to be fetched from upstream (not investigated further; out of the packaged-game scope).
- **T6 — 0 A.D. in noble release pocket.** `/noble/0ad` "Package not available in this suite"; present only in `noble-updates` (0.0.26-6ubuntu0.24.04.1).
- **T6 — an explicit "no GPU on standard runners" sentence.** Neither GitHub Docs page says it; the hardware table has no GPU column and GPU is listed only under larger runners (S4-gh-hosted-runners). Whether Mesa (`libgl1-mesa-dri`, `mesa-vulkan-drivers`) is present on the image is not documented (S4-runner-2204/2404, S4-runner-toolset); installing it via apt is possible per passwordless sudo but was not tested.
- **T6 — Wine + Xvfb documentation.** Wine FAQ has no entry (search log row 34). The closest primary evidence is Wine's own CI running on an Xorg `dummy` device with `LP_NUM_THREADS` (row 35), which is not Xvfb.
- **T6 — Proton standalone / without Steam.** Proton README documents only Steam-client installation and `STEAM_COMPAT_CONFIG` set by the Steam client; no "run requirements" paragraph exists to quote. No source found documenting the graphical `steam` client being driven headlessly on a hosted runner; SteamCMD documents itself as a dedicated-server installer requiring an owning account for paid titles.
- **T6 — dxvk-native / winetricks route.** DXVK README has no `dxvk-native` section; winetricks not searched beyond the DXVK README (no documentation route found that mentions lavapipe).
- **T6 — thread documentation for DarkPlaces, ioquake3/OpenArena, Warzone 2100, Armagetron, Sauerbraten.** Only a threading wrapper header (`darkplaces/thread.h`) or nothing found; not quoted as evidence of thread population.
- **T6 — ftrace / `/sys/kernel/tracing` availability on Azure-hosted runners.** No runner-images issue or GitHub doc found that mentions tracefs; the only maintainer statement is the generic "perf is a part of the linux kernel which we do not modify at all … same as a clean Ubuntu VM in Azure" (#4974). Web search row 23 surfaced no ftrace-specific report.
- **T6 — Ubuntu's own `kernel/events/core.c` default.** Launchpad git and kernel.ubuntu.com gitea refuse anonymous raw fetches (rows 21–22); the value 4 rests on the reposted SAUCE patch (S4-ubuntu-kernel-paranoid) and the runner observation (#4974).
- **T1–T5.** Out of class; no candidate above covers them.

## 4. Coverage statement (T6) — what such a measurement could and could not observe

Presented from the sources above; no decision taken.

**Environment that the sources establish.** `ubuntu-latest` = Ubuntu 24.04 image, kernel `6.17.0-1022-azure`, 4 vCPU / 16 GB (public repo) or 2 vCPU / 8 GB (private), an Azure VM with passwordless sudo, `xvfb` preinstalled (S4-runner-2404, S4-gh-hosted-runners, S4-runner-toolset). Ubuntu 22.04 is the same shape on kernel `6.8.0-1064-azure` and enters deprecation on 2026-09-17 (S4-runner-2204). Mesa's llvmpipe (`swrast_dri.so`) and lavapipe (`libvulkan_lvp.so` + `lvp_icd*.json`) are shipped in `libgl1-mesa-dri` / `mesa-vulkan-drivers` for both suites; forcing them is documented via `LIBGL_ALWAYS_SOFTWARE=true` (+ `GALLIUM_DRIVER=llvmpipe`) and `VK_DRIVER_FILES` (`VK_ICD_FILENAMES` is deprecated) (S4-ubuntu-pkgs, S4-mesa-envvars). llvmpipe is itself multithreaded, defaulting to one thread per core (`LP_NUM_THREADS`).

**Native games with an input-free fixed workload (packaged in Ubuntu).** SuperTuxKart `--profile-laps=n`/`--profile-time=n` (AI-driven; `--no-graphics` optional) (S4-stk); DarkPlaces/Nexuiz `-benchmark <demo>` (timedemo, exits, logs aggregate fps) (S4-xonotic); OpenArena/ioquake3 `+set timedemo 1 +demo <name>` with `cl_timedemoLog` writing per-frame durations (S4-ioq3); 0 A.D. `-autostart … -autostart-ai=…` (rendered) or `-autostart-nonvisual`/`-replay` (no graphics) (S4-0ad); Warzone 2100 `--autogame [--headless] --skirmish <file>` (S4-wz2100); Armagetron Advanced `--playback FILE` / `--benchmark` (S4-ubuntu-manpages); Minetest `--go --random-input` (random, not fixed) (S4-minetest); Sauerbraten demo playback exists only as an in-game mode (S4-sauerbraten).

**What a `/proc` sidecar could observe** (S4-proc5, S4-sched-stats, S4-kernel-param):
- Thread population over time: the set of `/proc/<pid>/task/<tid>/` directories, each with `comm` (15 characters), `status` (`State`, `Threads`, `voluntary_ctxt_switches`, `nonvoluntary_ctxt_switches`), `stat` (`utime`/`stime` in 10 ms ticks, `processor`, `policy`, `rt_priority`), `wchan`. Includes llvmpipe's rasterizer threads, SDL/audio threads, and (for STK, Minetest, 0 A.D.) the game's own documented worker threads.
- Per-thread CPU consumption and scheduling counts: `schedstat` gives cumulative on-CPU nanoseconds, runqueue-wait nanoseconds and the number of timeslices; differencing between samples yields mean run length per schedule and mean wait, at the sidecar's sampling period — not individual schedule lengths or individual wake gaps.
- Wake gaps only as an aggregate: `voluntary_ctxt_switches` increments and `schedstat` timeslice counts per interval give a wake rate; the distribution of gaps is not exposed by `/proc`.
- Frame cadence only from the game's own log: ioquake3 per-frame durations (`cl_timedemoLog`), DarkPlaces aggregate fps, STK's `m_max_fps` throttle; nothing in `/proc` marks frames. Under Xvfb there is no display refresh to pace against (Xvfb "emulates a dumb framebuffer using virtual memory"); STK caps by its own sleep, 0 A.D. `-vsync` refers to a monitor that does not exist.
- Finer resolution would need `perf sched`/ftrace `sched_switch`: the sysctl default is 4 (no unprivileged perf) but the runner has passwordless sudo; user reports show `sudo sysctl kernel.perf_event_paranoid=1` + `sudo perf record -e cycles -a` working on x64 runners, hardware PMU events unavailable in the VM, and nothing documented for tracefs (S4-runner-perf-issues, S4-ubuntu-kernel-paranoid).

**What it cannot observe.**
- The Proton/Wine/DXVK structure (`wineserver`, `dxvk-cs`, `dxvk-submit`, `winepulse_*`): Proton is documented only as a Steam-client tool; SteamCMD is a dedicated-server installer; no documented headless route to a Proton game on a runner was found. Wine itself is documented (via its own CI) to run on a GPU-less Xorg dummy with llvmpipe, so a plain Wine + DXVK-on-lavapipe experiment is not excluded by the sources, but it is not documented either (S4-proton-readme, S4-steamcmd, S4-wine-faq, S4-dxvk).
- Real display refresh and vsync-paced frame cadence: no display exists; any period is set by the game's limiter or by CPU rendering time on a 4-vCPU (or 2-vCPU) shared VM.
- GPU-side threads and GPU-driven wakeups: absent by construction; llvmpipe's CPU threads replace them and inflate the CPU-side thread count relative to a GPU system.
- Per-schedule runtime distributions and wake-to-wake gaps at sub-sampling resolution from `/proc` alone (cumulative counters only; `utime`/`stime` at 10 ms).
