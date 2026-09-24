# S4 — own measurement on a CI runner (T11 CI observability)

Reader: S4 class reader, access date 2026-09-24 (all fetches). No GitHub workflow was created or run: nothing below is an observation made **on** a GitHub Actions runner. The record covers (a) what documentation and the runner's own kernel build say a hosted runner exposes, and (b) the method a later runner measurement would use. One section (end of Candidates) records what **this cloud sandbox** shows, labelled as such; it is not a runner observation.

Source copies are under `_dev/research/jioh/task-9.11-scheduler-constants/sources/S4-NN/` (gitignored, will not survive). Every passage below is quoted verbatim; HTML pages were reduced to text by stripping tags (the SHA-256 is of the fetched HTML, not the text reduction).

## 1. Search log

| # | Date | Engine / venue | Exact query or request | Hits followed | Dead ends (status) |
|---|---|---|---|---|---|
| 1 | 2026-09-24 | git (github.com via git proxy) | `git ls-remote https://github.com/actions/runner-images HEAD` | HEAD = `ebade26c60adcb867918b31c8f8caa37343a3d39` (commit date 2026-09-23T17:21:51Z, "Updating readme file for ubuntu-slim version 20260922.6.5 (#14771)") | — |
| 2 | 2026-09-24 | raw.githubusercontent.com | `actions/runner-images/<commit>/images/ubuntu/Ubuntu2404-Readme.md`, `.../Ubuntu2204-Readme.md` | both 200 → S4-01 | — |
| 3 | 2026-09-24 | api.github.com | `repos/actions/runner-images/commits/<commit>`; `search/issues?q=repo:actions/runner-images+steal` | — | refused by session proxy ("GitHub access to this repository is not enabled for this session" / "This GitHub API path is not available") |
| 4 | 2026-09-24 | git clone `--depth 1` actions/runner-images at `ebade26c…` | `grep -rn -iE "sysctl|perf_event|debugfs|sched_|kernel\.|steal" images/ubuntu/scripts images/ubuntu/templates` | `images/ubuntu/scripts/build/configure-environment.sh` (sysctl lines) → S4-01; no hit for perf_event, debugfs, sched_, steal | `grep -iE "linux-azure|hwe|linux-image|linux-tools"` over `images/ubuntu/` (excluding Readmes): 0 hits |
| 5 | 2026-09-24 | docs.github.com (curl) | `/en/actions/reference/runners/github-hosted-runners`; `/en/actions/concepts/runners/github-hosted-runners` | both 200 → S4-02 | — |
| 6 | 2026-09-24 | archive.ubuntu.com pool | `pool/main/l/linux-azure-6.17/` index; `pool/main/l/linux-azure/` | linux-azure-6.17 index lists 6.17.0-1022.22 packages (headers, tools, diff.gz) → S4-03 | `pool/main/l/linux-azure/` listed no 6.17.0-1022 file (dir has other series) |
| 7 | 2026-09-24 | archive.ubuntu.com | `linux-headers-6.17.0-1022-azure_6.17.0-1022.22_amd64.deb` (extract `usr/src/linux-headers-6.17.0-1022-azure/.config`) | 200 → S4-03 | — |
| 8 | 2026-09-24 | archive.ubuntu.com | `linux-azure-6.17_6.17.0-1022.22.diff.gz`; grep changed lines in kernel/sched/{fair,debug,rt,deadline}.c | 200 → S4-03 | — |
| 9 | 2026-09-24 | archive.ubuntu.com | `pool/main/l/linux-azure-6.8/linux-headers-6.8.0-1064-azure_6.8.0-1064.72~22.04.1_amd64.deb` | 200 → S4-04 | — |
| 10 | 2026-09-24 | raw.githubusercontent.com torvalds/linux | tags `v6.17` (commit `e5f0a698b34ed76002dc5cff3804a61c80233a7a`) and `v6.8` (commit `e8f897f4afef0031fe618a8e94127a0934896aba`): `kernel/sched/{debug,fair,rt,core,ext,deadline}.c`, `kernel/sched/sched.h`, `Documentation/scheduler/{sched-rt-group,sched-ext,sched-eevdf,sched-design-CFS}.rst` | 200 → S4-05 | `v6.17/Documentation/scheduler/sched-eevdf.rst` first try 429 (local concurrency cap), 200 on retry; at `v6.8`: `kernel/sched/ext.c` 404, `sched-ext.rst` 404, `sched-eevdf.rst` 404 (files do not exist at that tag) |
| 11 | 2026-09-24 | man7.org | `man1/chrt.1.html`, `man1/taskset.1.html`, `man7/sched.7.html` | 200 → S4-06 | — |
| 12 | 2026-09-24 | packages.ubuntu.com | `noble/util-linux`, `noble/amd64/util-linux/filelist` | 200 → S4-06 | — |
| 13 | 2026-09-24 | man7.org | `man8/cyclictest.8.html` | — | 404 |
| 14 | 2026-09-24 | manpages.ubuntu.com | `manpages/noble/man8/cyclictest.8.html` | — | 503 |
| 15 | 2026-09-24 | git.kernel.org rt-tests | `plain/src/cyclictest/cyclictest.8?h=v2.5` (tag v2.5 → commit `4579b9a6d85ae528f76e92421eb5e7b33cd26b17`); `packages.ubuntu.com/noble/rt-tests` | 200, 200 → S4-07 (a `main` copy, commit `62da2bef…`, was fetched then discarded in favour of the v2.5 tag that noble ships) | — |
| 16 | 2026-09-24 | man7.org | `man1/perf-sched.1.html` | 200 → S4-08 | — |
| 17 | 2026-09-24 | packages.ubuntu.com | `noble/rt-app`, `noble/schbench`, `noble/stress-ng` | 200 ×3 → S4-09 | `noble/schbench`: page says "No such package." |
| 18 | 2026-09-24 | man7.org | `man5/proc_stat.5.html` | 200 → S4-10 | — |
| 19 | 2026-09-24 | WebSearch | `actions/runner-images issue steal time CPU performance variance ubuntu runner` | issues #7107, #12512, #13770, #2607, #14545, #11790 (titles only) | github.com issue pages: curl 403 (egress proxy); not read |
| 20 | 2026-09-24 | WebSearch | `github actions runner perf_event_paranoid perf sched ftrace ubuntu-latest` | runner-images issue #11789 (WebFetch rendering only, see note) | github.com: curl 403; WebFetch returned a model summary, not a file, so no SHA-256 and no verbatim guarantee → not used as a candidate |
| 21 | 2026-09-24 | WebSearch | `"steal" time github actions hosted runner /proc/stat noisy neighbor benchmark variance` | arXiv 2411.05491 → S4-11; vendor blogs (codspeed.io, runs-on.com, blacksmith.sh, avrea.com, markaicode.com) not followed (commercial, not primary for runner internals) | — |
| 22 | 2026-09-24 | arxiv.org | `pdf/2411.05491v1` | 200 → S4-11 | — |
| 23 | 2026-09-24 | this sandbox shell | `uname -a; nproc; ls /sys/kernel/debug/sched; cat /proc/sys/kernel/sched_rt_*; ls /sys/kernel/sched_ext; mount -t debugfs …` | see §2 "Sandbox illustration" | — |

## 2. Candidates

### S4-01 — actions/runner-images: Ubuntu 24.04 and 22.04 image READMEs, and the image build script

- **Citation.** GitHub, *actions/runner-images*, `images/ubuntu/Ubuntu2404-Readme.md`, `images/ubuntu/Ubuntu2204-Readme.md`, `images/ubuntu/scripts/build/configure-environment.sh`.
- **Copy read.** Commit `ebade26c60adcb867918b31c8f8caa37343a3d39` (2026-09-23), fetched 2026-09-24 from `https://raw.githubusercontent.com/actions/runner-images/ebade26c60adcb867918b31c8f8caa37343a3d39/images/ubuntu/…`; script from a `git clone --depth 1` at the same commit. Local: `sources/S4-01/`.
  - `Ubuntu2404-Readme.md` SHA-256 `4edbefde1df512f024363b1f66f78448f944f071c9e1775056b220d5bdc8dc81`
  - `Ubuntu2204-Readme.md` SHA-256 `f3bce22f10e370ff599363edc06c6ebb957a85dbd2b00afb7c3681deb3ad34e7`
  - `configure-environment.sh` SHA-256 `d891d1a107d55fca792efce0cebf1170df8097e47ec44c6fdf12404a17351201`
- **Passages.**
  - `Ubuntu2404-Readme.md:8-12`: "# Ubuntu 24.04 / - OS Version: 24.04.5 LTS / - Kernel Version: 6.17.0-1022-azure / - Image Version: 20260907.300.1 / - Systemd version: 255.4-1ubuntu8.17"
  - `Ubuntu2204-Readme.md:9-12`: "- OS Version: 22.04.5 LTS / - Kernel Version: 6.8.0-1064-azure / - Image Version: 20260907.292.1 / - Systemd version: 249.11-0ubuntu3.22"
  - `Ubuntu2404-Readme.md:256` heading "### Installed apt packages"; `:267` "| coreutils              | 9.4-3ubuntu6.3               |"; `:316` "| sudo                   | 1.9.15p5-3ubuntu5.24.04.2    |". The table (lines 259-332) contains no `rt-tests`, `linux-tools-*`, `stress-ng`, `rt-app` or `schbench` row.
  - `Ubuntu2404-Readme.md:5` (announcement table): "[[Ubuntu] The Ubuntu 22 based runner images will begin deprecation on September 17th and will be fully unsupported by April 17th for GitHub Actions and Azure DevOps](https://github.com/actions/runner-images/issues/14254)"
  - `configure-environment.sh:48`: "echo 'vm.max_map_count=262144' | tee -a /etc/sysctl.conf"; `:51-52`: "echo 'fs.inotify.max_user_watches=655360' | tee -a /etc/sysctl.conf" / "echo 'fs.inotify.max_user_instances=1280' | tee -a /etc/sysctl.conf"; `:55`: "echo 'vm.mmap_rnd_bits=28' | tee -a /etc/sysctl.conf". (Grep over `images/ubuntu/scripts` and `templates` found no `kernel.sched_*`, `perf_event`, `debugfs` or `steal` setting.)
- **Coverage.** T11: covers the **running kernel version string** of the image (`6.17.0-1022-azure` for `ubuntu-24.04`/`ubuntu-latest`, `6.8.0-1064-azure` for `ubuntu-22.04`), image version, and that the image build changes no scheduler sysctl — as of image 20260907 at the stated commit. Does not cover CPU count, slice values, sched_ext state, RT/fair-server values, or any measured latency. T1–T10: does not cover.
- **Observation?** Not an observation of a running runner; it is the image's self-description, generated per image build. Machine: the image (not a specific VM); window: image version 20260907.300.1 / .292.1.

### S4-02 — GitHub Docs: GitHub-hosted runners reference, and the concepts page

- **Citation.** GitHub Docs, "GitHub-hosted runners reference" (`https://docs.github.com/en/actions/reference/runners/github-hosted-runners`) and "GitHub-hosted runners" (`https://docs.github.com/en/actions/concepts/runners/github-hosted-runners`).
- **Copy read.** Fetched 2026-09-24 by curl (HTTP 200, no version stamp on the page). Local: `sources/S4-02/`.
  - `github-hosted-runners-reference.html` SHA-256 `f6f66543c9ab0a6053570ff79d8293e189d0838bfaa0c6f99666abfa40fa4aa1`
  - `about-github-hosted-runners.html` SHA-256 `7b61084129c284a033e6288e15452fac48ebef42393838800a07b52b9882f2b0`
- **Passages (reference page).**
  - Section "Standard GitHub-hosted runners for public repositories": "For public repositories, jobs using the workflow labels shown in the table below will run with the associated specifications. With the exception of single-CPU runners, each GitHub-hosted runner is a new virtual machine (VM) hosted by GitHub. Single-CPU runners are hosted in a container on a shared VM—see GitHub-hosted runners reference."
  - Same table, row: "Linux | 4 | 16 GB | 14 GB | x64 | ubuntu-latest, ubuntu-24.04, ubuntu-22.04, ubuntu-26.04" (columns "Virtual machine / container | Processor (CPU) | Memory (RAM) | Storage (SSD) | Architecture | Workflow label"); row: "Linux | 1 | 5 GB | 14 GB | x64 | ubuntu-slim"; row: "Linux | 4 | 16 GB | 14 GB | arm64 | ubuntu-24.04-arm, ubuntu-22.04-arm, ubuntu-26.04-arm".
  - Section "Standard GitHub-hosted runners for private repositories", row: "Linux | 2 | 8 GB | 14 GB | x64 | ubuntu-latest, ubuntu-24.04, ubuntu-22.04, ubuntu-26.04".
  - Section "Single-CPU runners": "ubuntu-slim runners execute Actions workflows in Ubuntu Linux, inside a container rather than a full VM instance. … Each container provides hypervisor level 2 isolation." and Note: "The container for ubuntu-slim runners runs in unprivileged mode. This means that some operations requiring elevated privileges—such as mounting file systems, using Docker-in-Docker, or accessing low-level kernel features—are not supported."
  - Section "Administrative privileges": "The Linux and macOS virtual machines both run using passwordless sudo. When you need to execute commands or install tools that require more privileges than the current user, you can use sudo without needing to provide a password."
  - Section "IP addresses": "Windows and Ubuntu runners are hosted in Azure and subsequently have the same IP address ranges as the Azure datacenters."
- **Passages (concepts page).** Section "Cloud hosts used by GitHub-hosted runners": "GitHub hosts Linux and Windows runners on virtual machines in Microsoft Azure with the GitHub Actions runner application installed."
- **Coverage.** T11: covers **CPU count** (stated "Processor (CPU)" column: 4 for public-repo x64 Linux, 2 for private-repo x64 Linux, 1 for `ubuntu-slim`; the unit is not defined further — vCPU vs core is not stated), that standard Linux runners are **Azure VMs** (hence a guest kernel with a hypervisor underneath), that **passwordless sudo** is available (so debugfs mount/read, `chrt`, `apt-get install` are permitted in principle), and that `ubuntu-slim` is an unprivileged container where "accessing low-level kernel features" is not supported. Does not cover kernel scheduler values or latency. T1–T10: does not cover.
- **Observation?** No; vendor specification, undated page, read 2026-09-24.

### S4-03 — Ubuntu kernel build 6.17.0-1022.22 (linux-azure-6.17, noble): shipped `.config` and packaging

- **Citation.** Canonical, Ubuntu archive, source package `linux-azure-6.17`, version `6.17.0-1022.22`; binary `linux-headers-6.17.0-1022-azure_6.17.0-1022.22_amd64.deb` (file `usr/src/linux-headers-6.17.0-1022-azure/.config`), `linux-azure-6.17_6.17.0-1022.22.diff.gz`, and the pool directory index.
- **Copy read.** `http://archive.ubuntu.com/ubuntu/pool/main/l/linux-azure-6.17/…`, fetched 2026-09-24. Local: `sources/S4-03/`.
  - `hdr.deb` (3,515,486 bytes) SHA-256 `7e800c3af8998d33df25cad0b26c789f5e0b583fb1f84090f83e1fd5099e4d5a`
  - extracted `config-6.17.0-1022-azure` SHA-256 `b684cdecf90ab6fb67f49c2b63ee95738810ee5c92476fa6f801815f75051ab5`
  - `diff.gz` SHA-256 `cb0154101fc7e337228a00c1caae7760b88afcb033f75c01756b3669dd376c54`
  - `pool-linux-azure-6.17-index.html` SHA-256 `c91cbec2b503fc61a977fc49fdf5034b98e15ce2451b7e0083d0b1905d2026be`
- **Passages (`config-6.17.0-1022-azure`, `file:line`).**
  - `:3` "# Linux/x86 6.17.13 Kernel Configuration"
  - `:116` "CONFIG_BPF=y"; `:123-126` "CONFIG_BPF_SYSCALL=y" / "CONFIG_BPF_JIT=y" / "CONFIG_BPF_JIT_ALWAYS_ON=y" / "CONFIG_BPF_JIT_DEFAULT_ON=y"
  - `:132-141` "CONFIG_PREEMPT_VOLUNTARY_BUILD=y / CONFIG_ARCH_HAS_PREEMPT_LAZY=y / # CONFIG_PREEMPT_NONE is not set / CONFIG_PREEMPT_VOLUNTARY=y / # CONFIG_PREEMPT is not set / # CONFIG_PREEMPT_LAZY is not set / # CONFIG_PREEMPT_RT is not set / # CONFIG_PREEMPT_DYNAMIC is not set / CONFIG_SCHED_CORE=y / CONFIG_SCHED_CLASS_EXT=y"
  - `:214-217` "CONFIG_FAIR_GROUP_SCHED=y / CONFIG_CFS_BANDWIDTH=y / # CONFIG_RT_GROUP_SCHED is not set / CONFIG_EXT_GROUP_SCHED=y"
  - `:242` "CONFIG_SCHED_AUTOGROUP=y"
  - `:505-506` "CONFIG_HZ_1000=y / CONFIG_HZ=1000"
  - `:8159` "CONFIG_DEBUG_INFO_BTF=y"
  - `:8189-8192` "CONFIG_DEBUG_FS=y / CONFIG_DEBUG_FS_ALLOW_ALL=y / # CONFIG_DEBUG_FS_DISALLOW_MOUNT is not set / # CONFIG_DEBUG_FS_ALLOW_NONE is not set"
  - also `:306` "CONFIG_PERF_EVENTS=y", `:8399` "CONFIG_FTRACE=y", `:8415` "CONFIG_SCHED_TRACER=y", `:8312` "CONFIG_SCHEDSTATS=y", `:6482` "CONFIG_HYPERV=y".
- **Pool index.** Lists (verbatim file names) "linux-tools-6.17.0-1022-azure_6.17.0-1022.22_amd64.deb", "linux-headers-6.17.0-1022-azure_6.17.0-1022.22_amd64.deb", "linux-azure-6.17_6.17.0-1022.22.diff.gz" — i.e. a `perf` build matching the runner kernel exists in the archive.
- **Diff check (reader's grep, not a passage).** `diff.gz` has hunks for `kernel/sched/deadline.c`, `debug.c`, `fair.c`, `rt.c` (lines 260808, 261192, 263966, 264623 of the decompressed diff), but no added or removed line matching `sched_base_slice|NSEC_PER_MSEC|base_slice|fair_server|debugfs_create|sched_rt_|min_t(unsigned int, num_online`. So the upstream defaults quoted in S4-05 are not changed by Ubuntu's patches in this build, as far as that pattern reaches.
- **Coverage.** T11: covers, for the `ubuntu-24.04` runner kernel as built: **sched_ext is compiled in** (`CONFIG_SCHED_CLASS_EXT=y` plus every prerequisite the kernel doc lists, see S4-05) → `/sys/kernel/sched_ext/` would exist; **debugfs is compiled and mountable** (`DEBUG_FS_ALLOW_ALL`) → `/sys/kernel/debug/sched/base_slice_ns` and `fair_server/` would exist (6.17 ≥ 6.12); `RT_GROUP_SCHED` off → RT throttling acts globally only (per S4-05 doc); preemption model **voluntary**, not dynamic (so `/sys/kernel/debug/sched/preempt` is absent, per the `#ifdef CONFIG_PREEMPT_DYNAMIC` in S4-05); **HZ=1000**; autogroup compiled in. Build configuration, not runtime values (a boot parameter could still override). T1–T10: does not cover (T3/T5/T6 values themselves are S2's).
- **Observation?** No; one kernel build's configuration. Machine: none (build artefact); version named.

### S4-04 — Ubuntu kernel build 6.8.0-1064.72~22.04.1 (linux-azure-6.8, jammy): shipped `.config`

- **Citation.** Canonical, Ubuntu archive, `linux-headers-6.8.0-1064-azure_6.8.0-1064.72~22.04.1_amd64.deb`, file `usr/src/linux-headers-6.8.0-1064-azure/.config`.
- **Copy read.** `http://archive.ubuntu.com/ubuntu/pool/main/l/linux-azure-6.8/…`, fetched 2026-09-24. Local `sources/S4-04/`. `hdr.deb` SHA-256 `6b709b09393e2cb3a12c7cde6987981842cf4fcb0a9b60d3805ab7861efc8ec2`; extracted config SHA-256 `3c7767bd878ae8f8683ddf303526da63ce9d8b09ca408c7e6bd18f7704b62968`.
- **Passages.** `:3` "# Linux/x86 6.8.12 Kernel Configuration"; `:133` "CONFIG_PREEMPT_VOLUNTARY=y"; `:206-207` "CONFIG_CFS_BANDWIDTH=y / # CONFIG_RT_GROUP_SCHED is not set"; `:232` "CONFIG_SCHED_AUTOGROUP=y"; `:505` "CONFIG_HZ=1000"; `:11126` "CONFIG_DEBUG_FS=y"; `:11244` "CONFIG_SCHED_DEBUG=y". The string `SCHED_CLASS_EXT` occurs 0 times in the file.
- **Coverage.** T11: for the `ubuntu-22.04` runner kernel: EEVDF kernel (6.8 ≥ 6.6) with debugfs → `base_slice_ns` would exist; **no sched_ext** option at all (not in 6.8); **no fair server** (added after 6.8; S4-05 shows `fair_server` absent from v6.8 `debug.c`). The Ubuntu 6.8 diff was not checked for backports (not fetched). T1–T10: does not cover.
- **Observation?** No; build configuration.

### S4-05 — Linux kernel source and scheduler documentation at v6.17 and v6.8 (upstream)

- **Citation.** Linus Torvalds et al., Linux kernel, tags `v6.17` (tag object `6063257da111c7639d020c5f15bfb37fb839d8b6`, commit `e5f0a698b34ed76002dc5cff3804a61c80233a7a`) and `v6.8` (commit `e8f897f4afef0031fe618a8e94127a0934896aba`), GitHub mirror `torvalds/linux`.
- **Copy read.** `https://raw.githubusercontent.com/torvalds/linux/<tag>/<path>`, fetched 2026-09-24. Local `sources/S4-05/v6.17/`, `sources/S4-05/v6.8/`. SHA-256:
  - v6.17 `kernel/sched/debug.c` `efae5ea664713656aa8918ff97639b6b5f336d9eb41b2f43886d31d8c140020f`; `fair.c` `e00d16ce68d3880bbfc10351a78abf5795f975d48566bdb5b5b03ec0884acbfe`; `rt.c` `6840fe4a929667e8b7b26e9d92db2faf8200875dd412b8347da2294e151abdd8`; `deadline.c` `a8a6f23e2f1515e0bc8a11df808966851a56dfe85fc318cf2ac7d460639f9089`; `core.c` `685d051d8b271f5fc7e51af5f3a488cb7ccc844c6673cf457ff67652281fedf9`; `ext.c` `ba9c0de9400b857d0fea48ce7572ca97228feb43858b7f7cc751da0be48d3b78`; `sched.h` `7ba1810941ee8016a5bf9a009058cbef6a5e8e6f51f4c147ca811f9f7676a9ad`; `Documentation/scheduler/sched-rt-group.rst` `c822e506021e8ee06ebc9be4e59b9d0dc52f12b6c2dd1ba3306f294b34ccadf6`; `sched-ext.rst` `ba2b0e7fd81808d566772d91e97b6a27bd5f55a48a71dd0c730cf378ba4053b5`; `sched-eevdf.rst` `75b99048d738b7683d06c5844e150253e91d75ec46e774f7a96cf0e9d39056a0`; `sched-design-CFS.rst` `8ed5eb40385db615f19d3ba7975285d3d08086fedd40f7f4b1f9c86f27b34d5a`.
  - v6.8 `debug.c` `e8a186a533dfa9c305ace3819b6ba9dcf22a6f2db0611ecb864ae6282e80c676`; `fair.c` `c7f0cda55beabbe56f5fdedded8701df79c5bee0111b8f2a210a68541f213f10`; `rt.c` `e859e950f8e5bf91af84ce982f64f59d8ebc7ea4059fc432a6de98e668c61e74`; `core.c` `3e73572fcaaa2fa05d2622d39ed8eec795f249bdce8330ff5ed864e82959c518`; `sched-rt-group.rst` `853bdf8677747cb3ff208810ffb112b209a0479cb86ba6a934167b7e628bbd63`; `sched-design-CFS.rst` `e5ef20efac91454d049588516d3a104f2110789d31c920e3565f7c09af3f47e7`.
- **Passages — base slice (where it lives, default, scaling).**
  - v6.17 `kernel/sched/debug.c:503`: "debugfs_create_u32("base_slice_ns", 0644, debugfs_sched, &sysctl_sched_base_slice);" inside `sched_init_debug()`, after `:495` "debugfs_sched = debugfs_create_dir("sched", NULL);". Same at v6.8 `debug.c:342,350`.
  - v6.17 `debug.c:499-501`: "#ifdef CONFIG_PREEMPT_DYNAMIC / debugfs_create_file("preempt", 0644, debugfs_sched, NULL, &sched_dynamic_fops); / #endif"
  - v6.17 `kernel/sched/fair.c:74-80`: "/* * Minimal preemption granularity for CPU-bound tasks: * * (default: 0.70 msec * (1 + ilog(ncpus)), units: nanoseconds) */ unsigned int sysctl_sched_base_slice = 700000ULL; static unsigned int normalized_sysctl_sched_base_slice = 700000ULL;"
  - v6.8 `fair.c:71-77`: "(default: 0.75 msec * (1 + ilog(ncpus)), units: nanoseconds) */ unsigned int sysctl_sched_base_slice = 750000ULL;"
  - v6.17 `fair.c:192-196, 204-206`: "static unsigned int get_update_sysctl_factor(void) { unsigned int cpus = min_t(unsigned int, num_online_cpus(), 8); … case SCHED_TUNABLESCALING_LOG: default: factor = 1 + ilog2(cpus);"; `:72` "unsigned int sysctl_sched_tunable_scaling = SCHED_TUNABLESCALING_LOG;"
  - Reader's arithmetic from these lines (a prediction, not an observation): 4 online CPUs → factor 3 → 2,100,000 ns on v6.17 (2,250,000 ns on v6.8); 2 CPUs → factor 2 → 1,400,000 ns (1,500,000 ns). The runner read of `base_slice_ns` is what would confirm it.
  - Sysctls that remain: at v6.17 the `.procname = "sched…"` entries in the files read are `sched_schedstats`, `sched_util_clamp_min`, `sched_util_clamp_max`, `sched_util_clamp_min_rt_default` (`core.c:4655-4680`), `sched_deadline_period_max_us`, `sched_deadline_period_min_us` (`deadline.c:35,43`), `sched_cfs_bandwidth_slice_us` (`fair.c:137`), `sched_rt_period_us`, `sched_rt_runtime_us`, `sched_rr_timeslice_ms` (`rt.c:34,43,52`). No `sched_base_slice`/`sched_min_granularity`/`sched_latency` sysctl.
- **Passages — EEVDF doc.** v6.17 `Documentation/scheduler/sched-eevdf.rst:5-9`: "The "Earliest Eligible Virtual Deadline First" (EEVDF) was first introduced in a scientific publication in 1995 [1]. The Linux kernel began transitioning to EEVDF in version 6.6 (as a new option in 2024), moving away from the earlier Completely Fair Scheduler (CFS)…"; `:30-32`: "…tasks can request specific time slices using the new sched_setattr() system call, which further facilitates the job of latency-sensitive applications." (The doc names no `base_slice_ns` file.)
- **Passages — RT throttling.** v6.17 `kernel/sched/rt.c:14-24`: "/* * period over which we measure -rt task CPU usage in us. * default: 1s */ int sysctl_sched_rt_period = 1000000; /* * part of the period that we allow rt tasks to run in us. * default: 0.95s */ int sysctl_sched_rt_runtime = 950000;" (identical values at v6.8 `rt.c:19,25`).
  - v6.17 `Documentation/scheduler/sched-rt-group.rst:91-97`: "/proc/sys/kernel/sched_rt_runtime_us: A global limit on how much time real-time scheduling may use. This is always less or equal to the period_us, as it denotes the time allocated from the period_us for the real-time tasks. Without CONFIG_RT_GROUP_SCHED enabled, this only serves for admission control of deadline tasks. With CONFIG_RT_GROUP_SCHED=y it also signifies the total bandwidth available to all real-time groups."
  - v6.17 same file `:105-107`: "* sched_rt_runtime_us/sched_rt_period_us > 0.05 inorder to preserve bandwidth for fair dl_server. For accurate value check average of runtime/period in /sys/kernel/debug/sched/fair_server/cpuX/"
  - v6.17 same file `:113-117`: "The default values for sched_rt_period_us (1000000 or 1s) and sched_rt_runtime_us (950000 or 0.95s). This gives 0.05s to be used by SCHED_OTHER (non-RT tasks). These defaults were chosen so that a run-away real-time tasks will not lock up the machine but leave a little time to recover it."
  - v6.8 same file `:92-98` (older wording, applies to the 22.04 kernel): "…Even without CONFIG_RT_GROUP_SCHED enabled, this will limit time reserved to real-time processes. With CONFIG_RT_GROUP_SCHED=y it signifies the total bandwidth available to all real-time groups."
- **Passages — fair server.** v6.17 `debug.c:470-490` (`debugfs_fair_server_init`): "d_fair = debugfs_create_dir("fair_server", debugfs_sched); … for_each_possible_cpu(cpu) { … snprintf(buf, sizeof(buf), "cpu%lu", cpu); d_cpu = debugfs_create_dir(buf, d_fair); debugfs_create_file("runtime", 0644, d_cpu, (void *) cpu, &fair_server_runtime_fops); debugfs_create_file("period", 0644, d_cpu, (void *) cpu, &fair_server_period_fops);", called at `:528` "debugfs_fair_server_init();". v6.17 `kernel/sched/deadline.c:1616-1618,1628`: "for_each_online_cpu(cpu) { u64 runtime =  50 * NSEC_PER_MSEC; u64 period = 1000 * NSEC_PER_MSEC; … dl_server_apply_params(dl_se, runtime, period, 1);". v6.8 `debug.c`: the string `fair_server` occurs 0 times.
- **Passages — sched_ext.** v6.17 `Documentation/scheduler/sched-ext.rst:33-45`: "``CONFIG_SCHED_CLASS_EXT`` is the config option to enable sched_ext and ``tools/sched_ext`` contains the example schedulers. The following config options should be enabled to use sched_ext: CONFIG_BPF=y CONFIG_SCHED_CLASS_EXT=y CONFIG_BPF_SYSCALL=y CONFIG_BPF_JIT=y CONFIG_DEBUG_INFO_BTF=y CONFIG_BPF_JIT_ALWAYS_ON=y CONFIG_BPF_JIT_DEFAULT_ON=y"; `:79-95`: "The current status of the BPF scheduler can be determined as follows: # cat /sys/kernel/sched_ext/state enabled # cat /sys/kernel/sched_ext/root/ops simple … You can check if any BPF scheduler has ever been loaded since boot by examining this monotonically incrementing counter (a value of zero indicates that no BPF scheduler has been loaded): # cat /sys/kernel/sched_ext/enable_seq 1". v6.17 `kernel/sched/ext.c:7658`: "scx_kset = kset_create_and_add("sched_ext", &scx_uevent_ops, kernel_kobj);"; `:17` "SCX_WATCHDOG_MAX_TIMEOUT = 30 * HZ,".
- **Passages — SCHED_IDLE / nice 19 weights (for the method's expected outcome).** v6.17 `Documentation/scheduler/sched-design-CFS.rst:139-141`: "- SCHED_IDLE: This is even weaker than nice 19, but its not a true idle timer scheduler in order to avoid to get into priority inversion problems which would deadlock the machine." v6.17 `kernel/sched/core.c:10374-10383`: "const int sched_prio_to_weight[40] = { … /*   0 */      1024, … /*  15 */        36,        29,        23,        18,        15, };" v6.17 `kernel/sched/sched.h:2333`: "#define WEIGHT_IDLEPRIO		3".
- **Coverage.** T11: covers **where** each quantity is exposed and its **default and scaling rule** on the runner kernels' upstream bases: `base_slice_ns` (debugfs, ns, 0.70 ms × (1+ilog2(min(ncpus,8))) at v6.17; 0.75 ms × … at v6.8); RT throttling `/proc/sys/kernel/sched_rt_period_us` = 1,000,000 µs, `sched_rt_runtime_us` = 950,000 µs, and that without `RT_GROUP_SCHED` (the runner's case, S4-03/S4-04) the 6.17 doc says runtime "only serves for admission control of deadline tasks" (the fair server then provides the fair-task reserve); fair server `/sys/kernel/debug/sched/fair_server/cpu<N>/{runtime,period}`, default 50 ms / 1000 ms per online CPU at v6.17, absent at v6.8; sched_ext state files under `/sys/kernel/sched_ext/`. Scope: upstream tags, not Ubuntu's patched tree (see S4-03 diff check for 6.17). Also T3/T5/T6/T9 values, but those are S2's topics; recorded here only as the expected values a runner read would be compared with.
- **Observation?** No; source code and docs at named tags.

### S4-06 — util-linux `chrt(1)`, `taskset(1)`; man-pages `sched(7)`; Ubuntu noble util-linux package

- **Citation.** util-linux project, `chrt(1)` and `taskset(1)` as rendered on man7.org; Linux man-pages project, `sched(7)`; packages.ubuntu.com, `noble/util-linux`, `noble/amd64/util-linux/filelist`.
- **Copy read.** Fetched 2026-09-24. Local `sources/S4-06/`.
  - `https://man7.org/linux/man-pages/man1/chrt.1.html` — footer "util-linux 2.43.devel-1062-f... 2026-08-03"; SHA-256 `a6c1e9ff5a75f7d73bd0934fbc5520568f8b878ae4b0512bec806d63a8fb78f4`
  - `https://man7.org/linux/man-pages/man1/taskset.1.html` — footer "util-linux 2.43.devel-739-eee2e 2026-05-24"; SHA-256 `2a2bf31d0942b0a16b863703c9d81f0db9e9ce72252f45a05c2e9c38ad3e58a1`
  - `https://man7.org/linux/man-pages/man7/sched.7.html` — footer "Linux man-pages 6.19 2026-02-08"; SHA-256 `3b52e0157557b7854f013eb13cee0ecdeacddc7f5f27c9e155dbbddc85786814`
  - `https://packages.ubuntu.com/noble/util-linux` SHA-256 `63e068c10fe30928933f930fbf153f8b833d0bffa437dfa919c2f1a0a7ddd6a6`; `…/noble/amd64/util-linux/filelist` SHA-256 `780cbda56d228822ceea1799494f101ed86b28a9d01632590402cd6cb376687e`
- **Passages.**
  - chrt(1), SYNOPSIS: "chrt [options] [priority] command [argument...]"
  - chrt(1), POLICY OPTIONS: "-o, --other Set scheduling policy to SCHED_OTHER (time-sharing scheduling). This is the default Linux scheduling policy. Since util-linux v2.42, the priority argument is optional; if specified, it must be set to zero." and "-i, --idle Set scheduling policy to SCHED_IDLE (scheduling very low priority jobs). Linux-specific, supported since 2.6.23. Since util-linux v2.42, the priority argument is optional; if specified, it must be set to zero."
  - chrt(1), PERMISSIONS: "A user must possess CAP_SYS_NICE to change the scheduling attributes of a process. Any user can retrieve the scheduling information."
  - taskset(1), DESCRIPTION: "The taskset command is used to set or retrieve the CPU affinity of a running process given its pid, or to launch a new command with a given CPU affinity. CPU affinity is a scheduler property that "bonds" a process to a given set of CPUs on the system. The Linux scheduler will honor the given CPU affinity and the process will not run on any other CPUs." OPTIONS: "-c, --cpu-list Interpret mask as numerical list of processors instead of a bit mask."
  - sched(7), "SCHED_IDLE: Scheduling very low priority jobs": "(Since Linux 2.6.23.) SCHED_IDLE can be used only at static priority 0; the process nice value has no influence for this policy. This policy is intended for running jobs at extremely low priority (lower even than a +19 nice value with the SCHED_OTHER or SCHED_BATCH policies)."
  - sched(7), "The nice value and group scheduling": "Under group scheduling, a thread's nice value has an effect for scheduling decisions only relative to other threads in the same task group. … if autogrouping is enabled (which is the default in various distributions), then employing setpriority(2) or nice(1) on a process has an effect only for scheduling relative to other processes executed in the same session (typically: the same terminal window)." and "All of the threads in a CPU cgroup form a task group."
  - packages.ubuntu.com noble: "Package: util-linux (2.39.3-9ubuntu6.6 and others) [ security ] [ essential ]"; filelist contains "/usr/bin/chrt" and "/usr/bin/taskset".
- **Coverage.** T11 (method): covers the tools to place the hog and the probe: `chrt -i 0 <cmd>` / `nice -n 19 <cmd>` / `taskset -c <cpu>`; noble ships util-linux 2.39.3 (< 2.42), so on the runner the explicit priority `0` is required for `-i`/`-o`. Covers the **group-scheduling caveat**: nice 19 only acts against tasks in the same task group, so the hog and the periodic task must run in the same cgroup/session for nice-19 results to mean anything (SCHED_IDLE is also a per-task-group weight; the doc passage covers nice only). T9 (definition side, S2's topic): sched(7) statement recorded. Other topics: does not cover.
- **Observation?** No; documentation.

### S4-07 — rt-tests `cyclictest(8)` at tag v2.5 (the version Ubuntu noble ships)

- **Citation.** rt-tests project, `src/cyclictest/cyclictest.8`, tag `v2.5` (commit `4579b9a6d85ae528f76e92421eb5e7b33cd26b17`), git.kernel.org; packages.ubuntu.com `noble/rt-tests`.
- **Copy read.** `https://git.kernel.org/pub/scm/utils/rt-tests/rt-tests.git/plain/src/cyclictest/cyclictest.8?h=v2.5`, 200, SHA-256 `f23b1b0c15a59be37f745a157cda887131c955f5aa6506079773d0a965cfebba`; `https://packages.ubuntu.com/noble/rt-tests`, SHA-256 `db2d21941608b919e42b000826d426eaf5a7b6fd0f2b979ef345636bb346d433`. Fetched 2026-09-24. Local `sources/S4-07/`.
- **Passages (`cyclictest.8` at v2.5, `file:line`).**
  - `:15-16` ".SH NAME / cyclictest \- High resolution test program"
  - `:36-39` "-a, --affinity[=PROC-SET] Run threads on the set of processors given by PROC-SET. If PROC-SET is not specified, all processors will be used. Threads will be assigned to processors in the set in numeric order, in a round-robin fashion."
  - `:68-71` "-D, --duration=TIME Specify a length for the test run. Append 'm', 'h', or 'd' to specify minutes, hours or days."
  - `:76-77` "-h, --histogram=US Dump latency histogram to stdout after the run. US is the max latency time to be be tracked in microseconds. This option runs all threads at the same priority."
  - `:85-86` "-i, --interval=INTV Set the base interval of the thread(s) in microseconds (default is 1000us). This sets the interval of the first thread. See also -d."
  - `:103-104` "-m, --mlockall Lock current and future memory allocations to prevent being paged out"
  - `:116-118` "-p, --prio=PRIO Set the priority of the first thread. The given priority is set to the first test thread. Each further thread gets a lower priority: Priority(Thread N) = max(Priority(Thread N-1) - 1, 0)"
  - `:120-122` "--policy=NAME set the scheduler policy of the measurement threads where NAME is one of: other, normal, batch, idle, fifo, rr"
  - `:127-128` "-q, --quiet Print a summary only on exit. Useful for automated tests, where only the summary output needs to be captured."
  - `:130-131` "-r, --relative Use relative timers instead of absolute. The default behaviour of the tests is to use absolute timers."
  - `:168-173` "-v, --verbose Output values on stdout for statistics. This option is used to gather statistical information about the latency distribution. The output is sent to stdout. The output format is: n:c:v where n=task number c=count v=latency value in us."
  - `:88-89` "--json=FILENAME Write final results into FILENAME, JSON formatted."
  - packages.ubuntu.com: "Package: rt-tests (2.5-1) [ universe ]" … "Test programs for rt kernels".
- **Coverage.** T11 (method): covers the probe: a periodic thread (`-i` µs, absolute timers by default) pinned (`-a`), with policy selectable (`--policy=other` makes it a default-policy task, which is what T11 asks for — cyclictest's usual use is SCHED_FIFO), for a fixed window (`-D`), reporting a latency histogram in µs (`-h`, `--histfile`, `--json`) or per-sample values (`-v`). The statistic it reports is **wake-up latency = actual wake time − programmed absolute expiry**, in µs, per thread. Installable on a runner with `sudo apt-get install rt-tests` (universe; the runner README does not list it as preinstalled). Other topics: does not cover (T8's hackbench is S2's).
- **Observation?** No; documentation.

### S4-08 — `perf-sched(1)` (Linux perf)

- **Citation.** Linux kernel `tools/perf/Documentation/perf-sched.txt`, as rendered on man7.org ("This page was obtained from the project's upstream Git repository … on 2026-08-04. (At that time, the date of the most recent commit that was found in the repository was 2026-08-03.)").
- **Copy read.** `https://man7.org/linux/man-pages/man1/perf-sched.1.html`, 200, fetched 2026-09-24, SHA-256 `545b3f01a34d3f00e27421f9f5d9ef17c656a68724fd57f87f7f9c40ad095268`. Local `sources/S4-08/`.
- **Passages (section DESCRIPTION).**
  - "'perf sched record <command>' to record the scheduling events of an arbitrary workload."
  - "'perf sched latency' to report the per task scheduling latencies and other scheduling properties of the workload." Example header: "Task | Runtime ms | Count | Avg delay ms | Max delay ms | Max delay start | Max delay end |"
  - "'perf sched timehist' provides an analysis of scheduling events. … By default it shows the individual schedule events, including the wait time (time between sched-out and next sched-in events for the task), the task scheduling delay (time between runnable and actually running) and run time for the task: … Times are in msec.usec."
- **Coverage.** T11 (method): covers a second, kernel-side measure — **scheduling delay per wake-up** (runnable → running, ms.µs) for the periodic task and the hog, from sched tracepoints, which separates scheduler delay from timer/hypervisor delay in cyclictest's number. On the runner needs `linux-tools-6.17.0-1022-azure` (present in the archive, S4-03), sudo, and tracepoint access (not verified on a runner; see Not found).
- **Observation?** No; documentation (example output in the page is from an unnamed machine).

### S4-09 — Ubuntu noble package availability for rt-app, schbench, stress-ng

- **Copy read.** `https://packages.ubuntu.com/noble/rt-app` SHA-256 `eb74fbc9ea297d2630ef228642a8177fdfddf9f2cf4a7c31bbdf17409d3181c6`; `…/noble/schbench` SHA-256 `ff945d5476659fd581ac1af9b947f0c2fef5239a3042a7c07af2d7ef72b6ab9d`; `…/noble/stress-ng` SHA-256 `cf039c8fc4b9ff3e7520491373fb3ad0c68fcc4a30c869796d3949bfb770cfe2`. Fetched 2026-09-24. Local `sources/S4-09/`.
- **Passages.** rt-app: "Package: rt-app (1.0-1) [ universe ]". schbench: "Error … No such package." stress-ng: "Package: stress-ng (0.17.06-1build1) [ universe ]".
- **Coverage.** T11 (method): rt-app and stress-ng (as a CPU hog) are apt-installable on the 24.04 runner; schbench is not packaged for noble and would have to be built from source. Does not cover any value.
- **Observation?** No.

### S4-10 — `proc_stat(5)`: the steal-time field

- **Copy read.** `https://man7.org/linux/man-pages/man5/proc_stat.5.html`, footer "Linux man-pages 6.19 2026-02-08", 200, fetched 2026-09-24, SHA-256 `3f0b831fc0708a4e11e9dd2ec729f45677afeb353cba76261aa03004c1c4818d`. Local `sources/S4-10/`.
- **Passage.** Under `/proc/stat` "cpu" line fields: "steal (since Linux 2.6.11) (8) Stolen time, which is the time spent in other operating systems when running in a virtualized environment"
- **Coverage.** T11 (method): covers how a runner job can **record** hypervisor interference during the window (read `/proc/stat` before/after each run and report the steal delta per CPU); it does not remove it. Does not cover any runner value.
- **Observation?** No.

### S4-11 — Reichelt, Jung & van Hoorn, "Overhead Measurement Noise in Different Runtime Environments" (arXiv:2411.05491v1)

- **Citation.** David Georg Reichelt, Reiner Jung, André van Hoorn, "Overhead Measurement Noise in Different Runtime Environments", arXiv:2411.05491v1 (2024).
- **Copy read.** `https://arxiv.org/pdf/2411.05491v1`, 200 `application/pdf`, fetched 2026-09-24, SHA-256 `5a6570cbe64e3f94f9a109bdf4dbfef2f787efb95e7ccc11c31c2c6e2fe4af0c`. Local `sources/S4-11/`.
- **Passages.**
  - p. 1, Abstract: "Nevertheless, we see that performance changes up to 4.41 % are detectable by GitHub actions, as long as only sequential workloads are examined."
  - p. 2, §2.3 "GitHub Actions Workflow": "We used the GitHub Actions Linux runners (4 processes), which are executed by default on a 16 GB memory runner with Ubuntu 22.04. These runners are in the Azure cloud."
  - p. 2, Table 1 "Measurement Results (in ns)", rows for "GH Actions": "Baseline 90.68 0.11% 0.24%" and "Binary Writer 3079.49 1.97% 4.41%" (columns "Environment | Mean | Rel. Std. Deviation σ | Min. Rel. Change ∆").
  - p. 2: "Since we do not have control over GitHubs measurement environment, we cannot generalize this for other benchmarks. Furthermore, since GitHubs investment in hosting might change, we do not know whether this low noise and good performance will be stable."
  - p. 3, §4.1: "Since our measured deviations are comparably low, we assume that this is due to efficient isolation capabilities used by GitHub."
- **Coverage.** T11: partially — covers **run-to-run noise of a Java microbenchmark (MooBench) execution time** on GitHub-hosted Linux runners (object: mean method-call time in ns; statistic: relative standard deviation across n = 10 loop starts; population: standard 4-CPU Ubuntu 22.04 runners, 2024). It does **not** cover scheduler wake-up latency, steal time, or any scheduler constant; it is evidence only that CPU-bound sequential timing on the runner has low run-to-run spread. T1–T10: does not cover.
- **Observation?** Yes — one measurement campaign on GitHub-hosted runners; machine named by class only ("GitHub Actions Linux runners … Ubuntu 22.04 … Azure"), subject MooBench, window not stated in the passages read (data at Zenodo DOI 10.5281/zenodo.11355256, not fetched).

### Sandbox illustration (this cloud sandbox, **not a GitHub Actions runner**)

Recorded 2026-09-24T09:10Z in the reader's own container, only to show what the commands of the method return; none of this is a runner value.

- `uname -a` → "Linux vm 6.18.44-fc-v37 #1 SMP PREEMPT_DYNAMIC @0 x86_64 x86_64 x86_64 GNU/Linux"; `nproc` → "4"; `/proc/cpuinfo` → "model name	: Intel(R) Xeon(R) Processor @ 2.10GHz", flag "hypervisor" present.
- `ls /sys/kernel/debug/sched` → "ls: cannot access '/sys/kernel/debug/sched': No such file or directory" (debugfs not mounted). After `mount -t debugfs none /sys/kernel/debug` (as uid 0): directory lists `base_slice_ns debug fair_server features latency_warn_ms latency_warn_once migration_cost_ns nr_migrate numa_balancing preempt tunable_scaling verbose`; `fair_server/` lists `cpu0 cpu1 cpu2 …`; but `cat /sys/kernel/debug/sched/base_slice_ns` → "Operation not permitted", and the same for `fair_server/cpu0/runtime` and `period`. (debugfs was unmounted afterwards.)
- `cat /proc/sys/kernel/sched_rt_period_us /proc/sys/kernel/sched_rt_runtime_us` → "1000000" / "950000".
- `ls /sys/kernel/sched_ext` → "No such file or directory"; `/proc/config.gz` → "# CONFIG_SCHED_CLASS_EXT is not set", "CONFIG_HZ=250".
- `ls /proc/sys/kernel | grep sched` → `sched_autogroup_enabled sched_cfs_bandwidth_slice_us sched_deadline_period_max_us sched_deadline_period_min_us sched_rr_timeslice_ms sched_rt_period_us sched_rt_runtime_us`.
- `/proc/stat` first line → "cpu  8859 0 2490 311586 172 0 1134 505 0 0" (8th field, steal, = 505 ticks since boot).
- `chrt`, `taskset`, `nice` present; `perf`, `cyclictest` absent.
- Lesson for the method: the existence of a debugfs file does not imply it is readable; a runner job must record the read's exit status and error text, not only the value.

## 3. What a runner can and cannot observe for T11 (synthesis of the candidates; no runner was run)

Predicted from S4-01…S4-05 for `ubuntu-24.04`/`ubuntu-latest` (kernel 6.17.0-1022-azure, 4 CPUs on public repos, Azure VM, passwordless sudo):

| Quantity | Where a job would read it | Expected from the sources | Status |
|---|---|---|---|
| Kernel version | `uname -r` | `6.17.0-1022-azure` (README at image 20260907.300.1) | documented; image changes weekly |
| CPU count | `nproc`, `/proc/cpuinfo` | 4 (public), 2 (private), 1 (`ubuntu-slim`) | documented |
| Effective base slice | `sudo mount -t debugfs none /sys/kernel/debug` (if not mounted); `sudo cat /sys/kernel/debug/sched/base_slice_ns` | 2,100,000 ns if 4 CPUs online (0.70 ms × 3); 1,400,000 on 2 CPUs | readable not verified (sandbox shows reads can be refused) |
| Tunable scaling | `…/sched/tunable_scaling` | LOG (1) | as above |
| sched_ext available | `ls /sys/kernel/sched_ext`; `cat …/state`, `…/enable_seq` | present (config `=y`), `state` expected `disabled`, `enable_seq` 0 | not verified |
| RT throttling | `cat /proc/sys/kernel/sched_rt_{period,runtime}_us` | 1000000 / 950000; with `RT_GROUP_SCHED` off it is admission control only (6.17 doc) | sysctl readable without sudo |
| Fair server | `sudo cat /sys/kernel/debug/sched/fair_server/cpu*/{runtime,period}` | 50,000,000 / 1,000,000,000 ns | absent on 22.04 (6.8) |
| Preemption model | `…/sched/preempt` | absent (`PREEMPT_DYNAMIC` not set); voluntary preemption, HZ=1000 | config-level |
| Steal time | `/proc/stat` field 8 | unknown | observable, not controllable |

Method (T11 last clause): pin a default-policy periodic probe and a hog to one CPU and compare the probe's wake-up latency with the hog absent, at nice 19, and under SCHED_IDLE:

1. `sudo apt-get install -y rt-tests linux-tools-$(uname -r)`; record `uname -r`, `nproc`, the table above, and `/proc/stat` before and after each run.
2. Baseline: `sudo cyclictest --policy=other -a 1 -t 1 -i 1000 -D 5m -m -q -h 20000 --histfile=base.hist --json=base.json` (default-policy probe, 1 ms period, CPU 1).
3. Hog at nice 19, same cgroup: `taskset -c 1 nice -n 19 sh -c 'while :; do :; done' &` then step 2 → `nice19.*`.
4. Hog under SCHED_IDLE: `taskset -c 1 chrt -i 0 sh -c 'while :; do :; done' &` (util-linux 2.39 on noble needs the `0`) then step 2 → `idle.*`.
5. Control with a default-policy hog (nice 0) to show the mechanism is visible at all.
6. Optionally `sudo perf sched record -C 1 -- sleep 60` during each run, then `perf sched timehist` / `perf sched latency` to split scheduling delay from timer/hypervisor delay.
7. Repeat across several jobs (different VMs) and report per-run histograms, not a pooled number.

Could be observed: the probe's wake-up latency distribution (µs, per wake-up, per run) on one vCPU of one Azure VM, with and without a nice-19 or SCHED_IDLE hog, plus the kernel's scheduling-delay per wake-up from `perf sched`, and the steal delta during the window.
Could not be observed: the effect of a desktop session (the runner has no desktop compositor or input stack; the README lists `xvfb` only); host-level interference, which appears only indirectly as steal time and latency outliers and differs between VMs; bare-metal behaviour (the guest kernel runs under Hyper-V, `CONFIG_HYPERV=y`); anything on `ubuntu-slim` needing low-level kernel access (docs, S4-02).

## 4. Not found

- **An actual observation on a GitHub Actions runner of `base_slice_ns`, `/sys/kernel/sched_ext`, fair-server values or wake-up latency under a SCHED_IDLE/nice-19 hog.** None found, and none made (no workflow was to be created). Searches: log rows 4 (image scripts), 19, 20, 21 (WebSearch), 22. The only runner measurement found (S4-11) is benchmark execution-time noise, not scheduler latency.
- **Whether debugfs is already mounted on the runner, and whether its `sched/` files are readable** (kernel lockdown or other restriction). Not stated in S4-01 (README, build scripts: no `debugfs` hit, row 4) or S4-02 (docs). Settled only by a runner run.
- **`perf_event_paranoid` value and tracepoint/ftrace availability on the runner.** runner-images issue #11789 ("`perf stat` does not work on Linux runners (even ARM ones)") was found by WebSearch (row 20), but github.com returned HTTP 403 to curl through the egress proxy and the GitHub API is not enabled for this repository in this session (row 3); a WebFetch rendering exists but is a model summary with no fetched file, so it is not quoted. No perf/ftrace setting in the image build scripts (row 4).
- **Steal time on runners (quoted runner-images issue).** Issues #12512 ("Performance has degraded"), #11790, #7107, #2607 found by WebSearch (row 19); all unreadable (github.com 403, row 19; API refused, row 3). No passage.
- **The Ubuntu 6.8.0-1064 (jammy) patch set** — not fetched; whether it backports anything to the 6.8 scheduler defaults is not checked (only the 6.17 diff was grepped, S4-03).
- **cyclictest man page on man7.org** (404) and **manpages.ubuntu.com noble** (503); replaced by the rt-tests v2.5 source man page (S4-07).
- **schbench packaged for Ubuntu noble**: "No such package." (row 17).
- **Topics T1–T10**: outside class S4; not searched by this reader beyond the incidental S2-type passages recorded in S4-05/S4-06.
