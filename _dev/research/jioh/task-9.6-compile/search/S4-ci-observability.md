# S4 — own measurement on a CI runner (T8): documentation research record

Reader class S4, topic T8 (CI observability under a single-core pin). Access date for every source: 2026-09-16. Nothing was measured or installed in this session (the container is not a GitHub runner). Source copies are under `sources/S4-NN/` (gitignored); every passage a reader needs is quoted here with its locator, and every copy is identified by URL/commit, version and SHA-256.

Network note: github.com HTML and api.github.com returned HTTP 403 through the session proxy (organisation egress policy); raw.githubusercontent.com, launchpad.net, launchpadlibrarian.net, packages.ubuntu.com, kernel.ubuntu.com, docs.github.com, man7.org, freedesktop.org, learn.microsoft.com, docs.python.org, runs-on.com, lore.altlinux.org, bugs.launchpad.net, lwn.net and git.savannah.gnu.org worked. git.launchpad.net returned 403; www.gnu.org returned no response (curl exit code 000; proxy status recorded `ws_closed_mid_exchange` for www.gnu.org:443). GitHub issues were reached through the GitHub MCP connector's `search_issues` tool only; its `list_commits`, `get_file_contents` and `issue_read` tools were denied for repositories other than this one, so commits of files fetched from `raw.githubusercontent.com/<owner>/<repo>/main|master/...` could not be resolved and those copies are identified by URL, access date, and SHA-256 (plus, where the file carries one, an internal version string).

Line locators: for `.rst`, `.txt`, `.c`, `.h`, `.py`, `.md`, `.texi` and config files the line numbers are those of the fetched file. For HTML pages (man7.org, docs.github.com, freedesktop.org, learn.microsoft.com, docs.python.org, runs-on.com, launchpad, lore.altlinux.org) the reader converted the fetched HTML to plain text with a fixed tag-stripping script (the `.txt` next to each `.html`) and cites `<file>.txt:<line>`; the SHA-256 recorded is that of the HTML as fetched, and the passages are verbatim from the page text.

## 1. Search log

| # | Date | Engine / venue | Query or URL | Hits followed | Dead ends (HTTP status) |
|---|------|----------------|--------------|---------------|-------------------------|
| 1 | 2026-09-16 | curl reachability probe (16 URLs) | docs.github.com runners reference; raw.githubusercontent.com runner-images readme; docs.kernel.org delay-accounting; man7 acct(5); gnu.org make manual; git.launchpad.net linux-azure annotations; kernel.ubuntu.com; github.com issues; api.github.com; changelogs.ubuntu.com linux-azure; launchpad.net linux-azure; freedesktop systemd.resource-control; learn.microsoft.com managed-disks; docs.python.org os; github.com bcc raw; raw.githubusercontent.com bcc | all 200 except listed | www.gnu.org (000, no response); git.launchpad.net (403); github.com HTML (403); api.github.com (403); github.com/<owner>/<repo>/raw/ (403) |
| 2 | 2026-09-16 | curl | https://raw.githubusercontent.com/actions/runner-images/main/images/ubuntu/Ubuntu2404-Readme.md | S4-02 | — |
| 3 | 2026-09-16 | curl | https://docs.github.com/en/actions/reference/runners/github-hosted-runners | S4-01 | — |
| 4 | 2026-09-16 | curl | https://raw.githubusercontent.com/actions/runner/main/README.md ; .../docs/start/envlinux.md | S4-03 | — |
| 5 | 2026-09-16 | curl | https://launchpad.net/ubuntu/+source/linux-azure ; https://kernel.ubuntu.com/ ; https://kernel.ubuntu.com/git/ | located linux-azure-6.17 source package for noble; kernel.ubuntu.com/git/ only links to git.launchpad.net (403) | git.launchpad.net (403) |
| 6 | 2026-09-16 | GitHub MCP `list_commits` | actions/runner-images path images/ubuntu/Ubuntu2404-Readme.md ; actions/runner | — | Access denied: repository not configured for this session (both) |
| 7 | 2026-09-16 | GitHub MCP `search_issues` (repo actions/runner-images) | "CPU model varies between runs hosted runner ubuntu-latest different processor lscpu" | #11789 (perf stat on Linux runners), #11934 (inconsistent execution times) | — |
| 8 | 2026-09-16 | GitHub MCP `search_issues` (repo actions/runner-images) | "perf_event_paranoid perf stat not permitted hosted runner" | #11789, #14091, #11689 bodies (saved in S4-22) | — |
| 9 | 2026-09-16 | GitHub MCP `search_issues` (repo actions/runner-images) | "ubuntu runner CPU model name AMD EPYC Xeon Platinum lscpu varies between jobs inconsistent performance benchmark noise" | #12545 (names "Hosted Compute Agent"), #13264 (ps listing with Runner.Listener/Runner.Worker), #11934 | — |
| 10 | 2026-09-16 | GitHub MCP `issue_read` | actions/runner-images #11789 | — | Access denied (repository not configured) |
| 11 | 2026-09-16 | WebFetch | https://github.com/actions/runner-images/issues/11789 | returned a summary only (not a verbatim copy; not cited) | — |
| 12 | 2026-09-16 | WebSearch | GitHub Actions hosted runner "hosted-compute" agent process Runner.Listener Runner.Worker | depot.dev blog, docs.github.com pages (secondary; not cited) | no primary hit for "hosted-compute agent" beyond the runner-images issue bodies (S4-22) |
| 13 | 2026-09-16 | WebSearch | GitHub Actions ubuntu-latest runner CPU model "AMD EPYC 7763" "Xeon Platinum 8370C" benchmark variance measurement | runs-on.com benchmark pages (S4-19); buildjet/avrea/carbonrunner blogs (not fetched) | — |
| 14 | 2026-09-16 | WebSearch | Ubuntu kernel kernel.perf_event_paranoid default 4 SAUCE patch "perf_event_paranoid" restrict unprivileged | lore.altlinux.org re-post of the Ubuntu SAUCE patch; bugs.launchpad.net #2131046; lwn.net/Articles/696216 (S4-21) | — |
| 15 | 2026-09-16 | curl, raw.githubusercontent.com torvalds/linux at tag v6.17 | Documentation/accounting/{taskstats,taskstats-struct,delay-accounting,psi}.rst; tools/accounting/getdelays.c; include/uapi/linux/{taskstats,acct}.h; kernel/acct.c; Documentation/scheduler/sched-stats.rst; Documentation/filesystems/proc.rst; tools/perf/Documentation/{perf-sched,perf-record,perf-trace,perf-stat}.txt; Documentation/admin-guide/{perf-security.rst,cgroup-v2.rst,kernel-parameters.txt,sysctl/kernel.rst,sysctl/vm.rst}; Documentation/ABI/stable/sysfs-block | S4-05, S4-06, S4-08, S4-09, S4-14, S4-17, S4-18 | — |
| 16 | 2026-09-16 | curl, man7.org | acct.2, acct.5, wait4.2, getrusage.2, time.1, proc_pid_stat.5, proc_pid_schedstat.5, strace.1, taskset.1, sched_setaffinity.2, nproc.1 | S4-06, S4-07, S4-08, S4-10, S4-16 | proc_pid_schedstat.5 (404 — no such page) |
| 17 | 2026-09-16 | curl, raw.githubusercontent.com | iovisor/bcc master tools/{execsnoop,exitsnoop}.py and *_example.txt; bpftrace/bpftrace master docs/stdlib.md, docs/language.md, docs/adoc/language.adoc | S4-11 | docs/adoc/language.adoc (404) |
| 18 | 2026-09-16 | curl, raw.githubusercontent.com | ColinIanKing/forkstat master forkstat.8, README.md, forkstat.c | S4-12 | — |
| 19 | 2026-09-16 | curl | https://git.savannah.gnu.org/cgit/make.git/plain/doc/make.texi (mirror used because www.gnu.org gave no response) | S4-13 | www.gnu.org/software/make/manual/make.html (000) |
| 20 | 2026-09-16 | curl, freedesktop.org | systemd.resource-control.html, systemd-run.html (latest) | S4-15 | — |
| 21 | 2026-09-16 | curl, raw.githubusercontent.com | coreutils/coreutils master src/nproc.c; coreutils/gnulib master lib/nproc.c; docs.python.org/3/library/os.html | S4-16 | — |
| 22 | 2026-09-16 | curl | https://learn.microsoft.com/en-us/azure/virtual-machines/managed-disks-overview | S4-18 | — |
| 23 | 2026-09-16 | curl, launchpad.net | /ubuntu/+source/linux-azure-6.17 ; /ubuntu/+source/linux-azure-6.17/6.17.0-1022.22 ; /ubuntu/noble/+package/linux-buildinfo-6.17.0-1022-azure ; /ubuntu/noble/amd64/linux-buildinfo-6.17.0-1022-azure/6.17.0-1022.22 ; http://launchpadlibrarian.net/871128553/linux-buildinfo-6.17.0-1022-azure_6.17.0-1022.22_amd64.deb (366 858 bytes) | S4-04 (kernel config extracted from the deb with dpkg-deb -x) | — |
| 24 | 2026-09-16 | curl | https://changelogs.ubuntu.com/changelogs/pool/main/l/linux-azure/ | index only; not needed once the buildinfo deb was found | — |
| 25 | 2026-09-16 | curl, packages.ubuntu.com/noble | forkstat, linux-tools-common, bpfcc-tools, bpftrace, acct, trace-cmd | S4-20 | — |
| 26 | 2026-09-16 | curl | https://runs-on.com/benchmarks/github-actions-cpu-performance/ ; https://runs-on.com/reference/benchmarks-gha-providers/ (identical content, same SHA-256) | S4-19 | — |
| 27 | 2026-09-16 | curl | https://lore.altlinux.org/devel-kernel/Yp4PuQTPUQt+7A9c@asheplyakov-rocket/T/ ; https://bugs.launchpad.net/ubuntu/+source/linux/+bug/2131046 ; https://lwn.net/Articles/696216/ | S4-21 | — |
| 28 | 2026-09-16 | grep over fetched files | proc.rst for `schedstat`, `/proc/<pid>/sched`, `SCHED_DEBUG`: no match; perf-record.txt for "lost": only line 823; perf-stat.txt for `task-clock`: example output line 583 only; execsnoop.py/exitsnoop.py for "lost"/"dropped": no match; Ubuntu2404-Readme.md for `containerd`, `walinuxagent`, `snapd`, `linux-tools`, `acct`, `strace`, `bpf`: no match | — | establishes several Not-found items (section 3) |

## 2. Candidates

Ordered by the sub-questions of T8: (a) the runner and what shares the pinned CPU — S4-01, S4-02, S4-03, S4-22, S4-19; (b) the kernel and its configuration — S4-04, S4-17, S4-21; (c) the instruments, one candidate per primary document — S4-05 taskstats/delay accounting, S4-06 BSD accounting, S4-07 wait4/rusage/time, S4-08 /proc stat and schedstat, S4-09 perf, S4-10 strace, S4-11 BCC/bpftrace, S4-12 forkstat, S4-13 GNU make, S4-14 PSI/cgroup, S4-15 systemd confinement, S4-20 package availability; (d) the pin's effects — S4-16; (e) page cache and disk — S4-17 (drop_caches), S4-18. A closing synthesis follows the candidates.

Coverage is stated against T8 only; none of these documents covers T1–T7 and that is not restated per candidate. None is an observation of a build: each is a specification or reference text, except S4-19 (a benchmark aggregator's table) and S4-22 (issue reports), which are marked as such.

---

### S4-01 — GitHub Docs, "GitHub-hosted runners reference"

**Citation.** GitHub, Inc. *GitHub-hosted runners reference*, GitHub Docs, page https://docs.github.com/en/actions/reference/runners/github-hosted-runners (rendered page; no version number on the page).

**Copy read.** URL above, fetched 2026-09-16 with curl; `sources/S4-01/github-hosted-runners.html`, 431 359 bytes, SHA-256 `b52229eb329d2dfd291953359699d0a296387ccd65c506962dc771fd49033762`; plain-text conversion `sources/S4-01/github-hosted-runners.txt` (SHA-256 `04cd9aa2a0a8b31cf5acc05a0c55132c84859392167e7337e92335f5b33991bd`), lines cited from the `.txt`.

**Passages.**

- `github-hosted-runners.txt:277` (section "Standard GitHub-hosted runners for public repositories"): "For public repositories, jobs using the workflow labels shown in the table below will run with the associated specifications. With the exception of single-CPU runners, each GitHub-hosted runner is a new virtual machine (VM) hosted by GitHub. Single-CPU runners are hosted in a container on a shared VM—see GitHub-hosted runners reference. Use of the standard GitHub-hosted runners is free and unlimited on public repositories."
- `github-hosted-runners.txt:278–289` (the table; cells rendered with `|`): "Virtual machine / container | Processor (CPU) | Memory (RAM) | Storage (SSD) | Architecture | Workflow label |" / "Linux | 1 | 5 GB | 14 GB | x64 |" "ubuntu-slim" / "Linux | 4 | 16 GB | 14 GB | x64 |" "ubuntu-latest," "ubuntu-24.04," "ubuntu-22.04," "ubuntu-26.04 (Public preview)".
- `github-hosted-runners.txt:378` (section "Administrative privileges"): "The Linux and macOS virtual machines both run using passwordless sudo. When you need to execute commands or install tools that require more privileges than the current user, you can use sudo without needing to provide a password. For more information, see the Sudo Manual."
- `github-hosted-runners.txt:382` (section "IP addresses"): "Windows and Ubuntu runners are hosted in Azure and subsequently have the same IP address ranges as the Azure datacenters. macOS runners are hosted in GitHub's own macOS cloud."
- `github-hosted-runners.txt:441` (section "File systems"): "GitHub executes actions and shell commands in specific directories on the virtual machine. The file paths on virtual machines are not static."

**Coverage (T8).** Covers the runner's nominal hardware for `ubuntu-latest` on a public repository: object = one hosted-runner VM; units = vCPU count (4), RAM (16 GB), storage (14 GB, labelled SSD); scope = the standard-runner label table; population = all jobs on those labels. Covers root: passwordless sudo on Linux VMs. Covers provider: Azure. Does not cover whether vCPUs are dedicated or shared, the VM size/series, the CPU model, the disk device type behind "SSD", or any daemon on the image. Not an observation.

---

### S4-02 — actions/runner-images, `images/ubuntu/Ubuntu2404-Readme.md` (image 20260907.300.1)

**Citation.** GitHub Actions team. *Ubuntu 24.04* runner image software list, file `images/ubuntu/Ubuntu2404-Readme.md` in repository actions/runner-images, branch `main`; the file states "Image Version: 20260907.300.1".

**Copy read.** https://raw.githubusercontent.com/actions/runner-images/main/images/ubuntu/Ubuntu2404-Readme.md, fetched 2026-09-16; commit not resolvable (api.github.com 403, MCP list_commits denied — search-log rows 1, 6); identified by the internal image version and by SHA-256 `4edbefde1df512f024363b1f66f78448f944f071c9e1775056b220d5bdc8dc81` (16 250 bytes, 301 non-empty lines); `sources/S4-02/Ubuntu2404-Readme.md`.

**Passages.**

- `Ubuntu2404-Readme.md:8–12`: "# Ubuntu 24.04" / "- OS Version: 24.04.5 LTS" / "- Kernel Version: 6.17.0-1022-azure" / "- Image Version: 20260907.300.1" / "- Systemd version: 255.4-1ubuntu8.17".
- `Ubuntu2404-Readme.md:18`: "- Clang: 16.0.6, 17.0.6, 18.1.3"; `:23`: "- GNU C++: 12.4.0, 13.3.0, 14.2.0"; `:28`: "- Python 3.12.3"; `:72`: "- CMake 3.31.6"; `:77–78`: "- Docker Client 28.0.4" / "- Docker Server 28.0.4"; `:104`: "- Ninja 1.13.2".
- Installed apt packages table (`### Installed apt packages`, `:256` ff.): `:262` "| automake               | 1:1.16.5-1.3ubuntu1          |"; `:280` "| gcc                    | 4:13.2.0-7ubuntu1            |"; `:295` "| make                   | 4.3-4.1build2                |"; `:316` "| sudo                   | 1.9.15p5-3ubuntu5.24.04.2    |"; `:318` "| systemd-coredump       | 255.4-1ubuntu8.17            |".
- Reader's own grep (search-log row 28): the strings `containerd`, `walinuxagent`, `snapd`, `linux-tools`, `perf`, `bpf`, `acct`, `strace`, `trace-cmd`, `forkstat` do not occur in the file.

**Coverage (T8).** Covers the image's kernel version string (object = `ubuntu-latest`/`ubuntu-24.04` image; value = the `uname -r` string "6.17.0-1022-azure"; scope = image version 20260907.300.1), the toolchain versions available for a build (gcc 13.2.0 apt package, GNU C++ 12.4.0/13.3.0/14.2.0, clang 16–18, make 4.3, ninja 1.13.2), and that a Docker server is present. Does not list any of the measurement tools (perf via linux-tools, bpfcc-tools, bpftrace, acct, forkstat, trace-cmd, strace): they are absent from the software list, so a job must install them (see S4-20). Does not name the daemons running on the image. Not an observation.

---

### S4-03 — actions/runner, README and `docs/start/envlinux.md`

**Citation.** GitHub. *GitHub Actions Runner*, repository actions/runner, `README.md` and `docs/start/envlinux.md`, branch `main`.

**Copy read.** https://raw.githubusercontent.com/actions/runner/main/README.md (2 621 bytes, SHA-256 `9e0e2e14907032403e4d4a715522569340cdb6dc3eb155fd4068872284f46302`) and https://raw.githubusercontent.com/actions/runner/main/docs/start/envlinux.md (1 793 bytes, SHA-256 `3720f8f315882afe81262d7f9c43eb2e587c673ceca8356cd301ab7be22d4cbe`), fetched 2026-09-16; commit not resolvable (see S4-02); `sources/S4-03/`.

**Passages.**

- `README.md:9`: "The runner is the application that runs a job from a GitHub Actions workflow. It is used by GitHub Actions in the [hosted virtual environments](https://github.com/actions/virtual-environments), or you can [self-host the runner](...) in your own environment."
- `envlinux.md:8–9` (section "Install .Net Core 3.x Linux Dependencies"): "The [config.sh](../../src/Misc/layoutroot/config.sh) will check .Net Core 3.x dependencies during runner configuration." and `:16–17`: "Dependencies is missing for Dotnet Core 6.0" / "Execute ./bin/installdependencies.sh to install any missing Dotnet Core 6.0 dependencies."

**Coverage (T8).** Covers only that the job-running application on hosted VMs is the actions/runner application and that it is a .NET application (its dependency check names Dotnet Core). Neither file names the `Runner.Listener` / `Runner.Worker` processes; those names appear as process paths in a hosted-runner `ps` listing quoted in S4-22 (`.../bin/Runner.Listener run`, `.../bin/Runner.Worker spawnclient ...`). Does not cover CPU cost or affinity of the agent. Not an observation.

---

### S4-04 — Ubuntu `linux-azure-6.17` 6.17.0-1022.22 (noble): the kernel configuration of the runner's kernel

**Citation.** Canonical Ltd. Source package `linux-azure-6.17`, version `6.17.0-1022.22`, Ubuntu 24.04 LTS (noble), binary `linux-buildinfo-6.17.0-1022-azure_6.17.0-1022.22_amd64.deb`, file `/usr/lib/linux/6.17.0-1022-azure/config`. The kernel version string it builds, `6.17.0-1022-azure`, is the one the runner image reports (S4-02 `Ubuntu2404-Readme.md:10`).

**Copy read.** Launchpad pages https://launchpad.net/ubuntu/+source/linux-azure-6.17 (SHA-256 `72959a0f5894015f87b9edd39a1847e85c32cf5fa2264e4668ad4cfe5e2260da`), https://launchpad.net/ubuntu/+source/linux-azure-6.17/6.17.0-1022.22 (SHA-256 `e8abc57816d6f1dcc7a45b357fd08f9305904182f3400a1874ae870e024f0d57`), https://launchpad.net/ubuntu/noble/amd64/linux-buildinfo-6.17.0-1022-azure/6.17.0-1022.22 (SHA-256 `03c416e7c3c03df6e5e40d7fc7404d5c444c7bddeb0be50dddb800375ea4bd57`); the deb from http://launchpadlibrarian.net/871128553/linux-buildinfo-6.17.0-1022-azure_6.17.0-1022.22_amd64.deb, 366 858 bytes, SHA-256 `e6f5c92a8cafa00ea93b573b77591c76c8ec1603c308b301d3d03e89cc57c5b3`; extracted config `sources/S4-04/config-6.17.0-1022-azure`, 206 837 bytes, SHA-256 `b684cdecf90ab6fb67f49c2b63ee95738810ee5c92476fa6f801815f75051ab5`. All fetched 2026-09-16. The launchpad text (converted) shows "6.17.0-1022.22" published for "The Noble Numbat" in "updates, security" (`launchpad-linux-azure-6.17.html`, converted text lines containing "Noble (6.17.0-1022.22)"). The deb's changelog head (`changelog.Debian.gz`): "linux-azure-6.17 (6.17.0-1022.22) noble; urgency=medium".

**Passages** (`config-6.17.0-1022-azure`, line numbers of the file):

- `:3` "# Linux/x86 6.17.13 Kernel Configuration"; `:5` `CONFIG_CC_VERSION_TEXT="x86_64-linux-gnu-gcc-13 (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0"`.
- `:107` `CONFIG_NO_HZ_FULL=y`; `:108` `CONFIG_CONTEXT_TRACKING_USER=y`; `:123` `CONFIG_BPF_SYSCALL=y`; `:146` `CONFIG_VIRT_CPU_ACCOUNTING=y`; `:148` `# CONFIG_IRQ_TIME_ACCOUNTING is not set`.
- `:149` `CONFIG_BSD_PROCESS_ACCT=y`; `:150` `CONFIG_BSD_PROCESS_ACCT_V3=y`; `:151` `CONFIG_TASKSTATS=y`; `:152` `CONFIG_TASK_DELAY_ACCT=y`; `:153` `CONFIG_TASK_XACCT=y`; `:154` `CONFIG_TASK_IO_ACCOUNTING=y`; `:155` `CONFIG_PSI=y`; `:156` `# CONFIG_PSI_DEFAULT_DISABLED is not set`; `:159` `CONFIG_CPU_ISOLATION=y`.
- `:204` `CONFIG_CGROUPS=y`; `:225` `CONFIG_CPUSETS=y`; `:228` `CONFIG_CGROUP_CPUACCT=y`; `:242` `CONFIG_SCHED_AUTOGROUP=y`; `:306` `CONFIG_PERF_EVENTS=y`; `:313` `CONFIG_TRACEPOINTS=y`; `:395` `# CONFIG_PARAVIRT_TIME_ACCOUNTING is not set`.
- `:503–506` `# CONFIG_HZ_250 is not set` / `# CONFIG_HZ_300 is not set` / `CONFIG_HZ_1000=y` / `CONFIG_HZ=1000`.
- `:855` `CONFIG_KPROBES=y`; `:861` `CONFIG_UPROBES=y`; `:2414` `CONFIG_CONNECTOR=y`; `:2415` `CONFIG_PROC_EVENTS=y`; `:6482` `CONFIG_HYPERV=y`; `:7512` `CONFIG_SECURITY_PERF_EVENTS_RESTRICT=y`; `:8189` `CONFIG_DEBUG_FS=y`; `:8312` `CONFIG_SCHEDSTATS=y`; `:8399` `CONFIG_FTRACE=y`; `:8402` `CONFIG_FUNCTION_TRACER=y`; `:8407` `CONFIG_DYNAMIC_FTRACE=y`; `:8431` `CONFIG_BPF_EVENTS=y`.
- Reader's own check: `grep -c '^CONFIG_SCHED_DEBUG' config-6.17.0-1022-azure` → 0 matches (the symbol does not appear in this 6.17 config either set or unset).

**Coverage (T8).** Covers the kernel-config requirements of every instrument in T8 for the runner's exact kernel: taskstats + delay accounting built in (`CONFIG_TASKSTATS`, `CONFIG_TASK_DELAY_ACCT`), I/O accounting (`CONFIG_TASK_IO_ACCOUNTING`), BSD accounting v3, PSI enabled by default, schedstats, ftrace, BPF syscall and BPF tracepoint events, kprobes/uprobes, proc connector (`CONFIG_PROC_EVENTS`, forkstat's event source), cpusets and cpuacct, `CONFIG_HZ=1000` (the tick behind clock-tick-granular fields), `CONFIG_NO_HZ_FULL` compiled in (but `nohz_full=` is a boot parameter, S4-17), and the Ubuntu perf restriction symbol `CONFIG_SECURITY_PERF_EVENTS_RESTRICT=y` (its meaning in S4-21). Object = kernel build options; scope = one package version; population = every VM booted with this kernel. Does not cover the runtime state of `kernel.task_delayacct`, `kernel.perf_event_paranoid` or `kernel.sched_schedstats` on the running VM (sysctl defaults documented in S4-17/S4-21). Not an observation.

---

### S4-05 — Linux kernel v6.17: taskstats and per-task delay accounting (`taskstats.rst`, `taskstats-struct.rst`, `delay-accounting.rst`, `getdelays.c`, `taskstats.h`)

**Citation.** Linux kernel documentation, tag v6.17: `Documentation/accounting/taskstats.rst`, `Documentation/accounting/taskstats-struct.rst`, `Documentation/accounting/delay-accounting.rst`, `tools/accounting/getdelays.c`, `include/uapi/linux/taskstats.h`.

**Copy read.** https://raw.githubusercontent.com/torvalds/linux/v6.17/<path>, fetched 2026-09-16; `sources/S4-05/`. SHA-256: taskstats.rst `cea5d7f579a9babe07e29a55579841324018ab7fff81b5e1fe8b6662277f1fda` (8 141 B); taskstats-struct.rst `a01e53bd8369510f0cb4c938fc6fadd2af898007056b9fe4b6732ef67332990a` (6 104 B); delay-accounting.rst `f7733c138f9b096ba1c79551502a4fd65fcd1e392089784424a8a69221f7f6de` (8 472 B); getdelays.c `3608a22369656d9383d83fbb42ba822fc242d554e208e5fc8e09ff422d7d9afb` (15 840 B); taskstats.h `0193e07cc8a2dd867438360b569cfb70813b004041e3593d2661c24a72330bc2` (8 836 B).

**Passages.**

- `taskstats.rst:11` (design goals): "- efficiently provide statistics during lifetime of a task and on its exit".
- `taskstats.rst:35–40`: "To obtain statistics for tasks which are exiting, the userspace listener sends a register command and specifies a cpumask. Whenever a task exits on one of the cpus in the cpumask, its per-pid statistics are sent to the registered listener. Using cpumasks allows the data received by one listener to be limited and assists in flow control over the netlink interface and is explained in more detail below."
- `taskstats.rst:42–45`: "If the exiting task is the last thread exiting its thread group, an additional record containing the per-tgid stats is also sent to userspace. The latter contains the sum of per-pid stats for all threads in the thread group, both past and present."
- `taskstats.rst:83–88`: "Commands to register/deregister interest in exit data from a set of cpus consist of one attribute, of type TASKSTATS_CMD_ATTR_REGISTER/DEREGISTER_CPUMASK and contain a cpumask in the attribute payload. The cpumask is specified as an ascii string of comma-separated cpu ranges e.g. to listen to exit data from cpus 1,2,3,5,7,8 the cpumask would be "1-3,5,7-8"."
- `taskstats.rst:160–181` ("Flow control for taskstats"): "When the rate of task exits becomes large, a listener may not be able to keep up with the kernel's rate of sending per-tid/tgid exit data leading to data loss. This possibility gets compounded when the taskstats structure gets extended and the number of cpus grows large." / "To avoid losing statistics, userspace should do one or more of the following:" / "- increase the receive buffer sizes for the netlink sockets opened by listeners to receive exit data." / "- create more listeners and reduce the number of cpus being listened to by each listener. In the extreme case, there could be one listener for each cpu. Users may also consider setting the cpu affinity of the listener to the subset of cpus to which it listens, especially if they are listening to just one cpu." / "Despite these measures, if the userspace receives ENOBUFS error messages indicated overflow of receive buffers, it should take measures to handle the loss of data."
- `delay-accounting.rst:5–7, 9–13`: "Tasks encounter delays in execution when they wait for some kernel resource to become available e.g. a runnable task may wait for a free CPU to run on." / "The per-task delay accounting functionality measures the delays experienced by a task while" / "a) waiting for a CPU (while being runnable)" / "b) completion of synchronous block I/O initiated by the task".
- `delay-accounting.rst:33–36`: "Userspace utilities, particularly resource management applications, can also aggregate delay statistics into arbitrary groups. To enable this, delay statistics of a task are available both during its lifetime as well as on its exit, ensuring continuous and complete monitoring can be done."
- `delay-accounting.rst:72–85`: "Compile the kernel with::" / "CONFIG_TASK_DELAY_ACCT=y" / "CONFIG_TASKSTATS=y" / "Delay accounting is disabled by default at boot up. To enable, add::" / "delayacct" / "to the kernel boot options. The rest of the instructions below assume this has been done. Alternatively, use sysctl kernel.task_delayacct to switch the state at runtime. Note however that only tasks started after enabling it will have delayacct information."
- `delay-accounting.rst:105` ("bash-4.4# ./getdelays -d -t 242") and `:110–112` (its output): "CPU         count     real total  virtual total    delay total  delay average      delay max      delay min" / "39      156000000      156576579        2111069          0.054ms     0.212296ms     0.031307ms" and "IO          count    delay total  delay average      delay max      delay min".
- `taskstats-struct.rst:82` "__u64	ac_etime;		/* Elapsed time [usec] */"; `:85` "__u64	ac_utime;		/* User CPU time [usec] */"; `:88` "__u64	ac_stime;		/* System CPU time [usec] */"; `:79` "__u32	ac_btime;		/* Begin time [sec since 1970] */".
- `taskstats-struct.rst:101–103`: "All values, until the comment "Delay accounting fields end" are available only if delay accounting is enabled, even though the last few fields are not delays"; `:105–106`: "xxx_count is the number of delay values recorded" / "xxx_delay_total is the corresponding cumulative delay in nanoseconds".
- `taskstats-struct.rst:112–116`: "/* Delay waiting for cpu, while runnable" / "* count, delay_total NOT updated atomically" / "*/" / "__u64	cpu_count;" / "__u64	cpu_delay_total;"; `:120–124`: "/* Delay waiting for synchronous block I/O to complete" / "* does not account for delays in I/O submission" / "*/" / "__u64	blkio_count;" / "__u64	blkio_delay_total;".
- `taskstats-struct.rst:130–136`: "/* cpu "wall-clock" running time" / "* On some architectures, value will adjust for cpu time stolen" / "* from the kernel in involuntary waits due to virtualization." / "* Value is cumulative, in nanoseconds, without a corresponding count" / "* and wraps around to zero silently on overflow" / "*/" / "__u64	cpu_run_real_total;".
- `getdelays.c:76–80` (usage): "getdelays [-dilv] [-w logfile] [-r bufsize] [-m cpumask] [-t tgid] [-p pid]" / "-d: print delayacct stats" / "-i: print IO accounting (works only with -p)" / "-l: listen forever".
- `getdelays.c:64` "#define MAX_CPUS	32"; `getdelays.c:12` (build note) "gcc -I/usr/src/linux/include getdelays.c -o getdelays".
- `taskstats.h:37` "#define TASKSTATS_VERSION	16".

**Coverage (T8).** Covers per-process CPU time at exit (object = exiting task/thread-group; `ac_utime`, `ac_stime` in microseconds; `cpu_run_real_total` in nanoseconds), lifetime (`ac_etime` in microseconds, `ac_btime` in seconds), and time blocked on synchronous block I/O (`blkio_delay_total`, nanoseconds, with `blkio_count`), delivered by the kernel at every exit to a listener registered on a cpumask — i.e. the listener can be registered for the one pinned CPU while running on other CPUs (`taskstats.rst:35–40, 83–88`). Covers the kernel-config requirement (S4-04 satisfies it) and the runtime requirement (`delayacct` boot option or `kernel.task_delayacct` sysctl; "only tasks started after enabling it"). Covers the documented loss mode (ENOBUFS overflow at high exit rates, `taskstats.rst:160–181`). Does not state a privilege requirement in these files (the `CAP_NET_ADMIN` requirement named in the brief was not found in this documentation set — see Not found). Not an observation.

---

### S4-06 — BSD process accounting: `acct(2)`, `acct(5)`, `include/uapi/linux/acct.h`, `kernel/acct.c`

**Citation.** Linux man-pages 6.19 (2026-02-08): acct(2), acct(5); Linux kernel v6.17: `include/uapi/linux/acct.h`, `kernel/acct.c`.

**Copy read.** https://man7.org/linux/man-pages/man2/acct.2.html (SHA-256 `85927245400377d070a06c07abbb1f59cd3818f648176581e55dcb8952e15a83`), https://man7.org/linux/man-pages/man5/acct.5.html (SHA-256 `423eb92035bf9760299457ac30e5586b6190a2f8a99613cf924321e5b2432fb3`; footer `acct.5.txt:208` "Linux man-pages 6.19            2026-02-08                        acct(5)"), https://raw.githubusercontent.com/torvalds/linux/v6.17/include/uapi/linux/acct.h (SHA-256 `eb58bebd5f0193df0ae1371b2cb118f0bad39982b5ede509e94f870332303b15`), https://raw.githubusercontent.com/torvalds/linux/v6.17/kernel/acct.c (SHA-256 `f1752f223ba5ff87114db4ff1a4eca07c4ebe53954962c735de651e78a5510ee`); fetched 2026-09-16; `sources/S4-06/`.

**Passages.**

- `acct.2.txt:91–95`: "The acct() system call enables or disables process accounting. If called with the pathname of an existing file as its argument, accounting is turned on, and records for each terminating process are appended to the file as it terminates."
- `acct.2.txt:125–128`: "ENOSYS BSD process accounting has not been enabled when the operating system kernel was compiled. The kernel configuration parameter controlling this feature is CONFIG_BSD_PROCESS_ACCT."; `:134–136`: "EPERM  The calling process has insufficient privilege to enable process accounting. On Linux, the CAP_SYS_PACCT capability is required."
- `acct.5.txt:121–125`: "The comp_t data type is a floating-point value consisting of a 3-bit, base-8 exponent, and a 13-bit mantissa. A value, c, of this type can be converted to a (long) integer as follows:" / "v = (c & 0x1fff) << (((c >> 13) & 0x7) * 3);"
- `acct.5.txt:127–129`: "The ac_utime, ac_stime, and ac_etime fields measure time in "clock ticks"; divide these values by sysconf(_SC_CLK_TCK) to convert them to seconds."
- `acct.5.txt:132–138` and the v3 struct `:140–160`: "Since Linux 2.6.8, an optional alternative version of the accounting file can be produced if the CONFIG_BSD_PROCESS_ACCT_V3 option is set when building the kernel." / "float     ac_etime;     /* Elapsed time */" / "comp_t    ac_utime;     /* User CPU time */" / "comp_t    ac_stime;     /* System time */" / "comp_t    ac_io;        /* Characters transferred (unused) */" / "comp_t    ac_rw;        /* Blocks read or written" / "(unused) */".
- `acct.h:25–26`: "comp_t is a 16-bit "floating" point number with a 3-bit base 8" / "exponent and a 13-bit fraction."; `acct.h:95–96` (struct acct_v3): "comp_t		ac_io;			/* Chars Transferred */" / "comp_t		ac_rw;			/* Blocks Read or Written */".
- `acct.c:481` "memset(ac, 0, sizeof(acct_t));"; `acct.c:486–490`: "/* calculate run_time in nsec*/" / "run_time = ktime_get_ns();" / "run_time -= current->group_leader->start_time;" / "/* convert nsec -> AHZ */" / "elapsed = nsec_to_AHZ(run_time);"; `acct.c:516–517`: "ac->ac_utime = encode_comp_t(nsec_to_AHZ(pacct->ac_utime));" / "ac->ac_stime = encode_comp_t(nsec_to_AHZ(pacct->ac_stime));". Reader's own check: `grep -n 'ac_io\|ac_rw' kernel/acct.c` → no match, i.e. `fill_ac()` never assigns `ac_io`/`ac_rw` after the `memset` (consistent with acct(5)'s "(unused)").

**Coverage (T8).** Covers per-process CPU time at exit (`ac_utime`, `ac_stime`; unit = clock ticks, encoded as 13-bit-mantissa `comp_t`, i.e. tick-granular and losing precision above 8191 ticks) and lifetime (`ac_etime`, float seconds-in-ticks in v3, computed from the thread-group leader's start time), written for every terminating process by the kernel; root requirement `CAP_SYS_PACCT`; kernel requirement `CONFIG_BSD_PROCESS_ACCT(_V3)` (both `=y` in S4-04). Does not cover I/O blocking (the I/O fields are unused/zero) and does not record on which CPU the process ran. Not an observation.

---

### S4-07 — `wait4(2)` / `getrusage(2)` rusage and GNU `time(1)`

**Citation.** Linux man-pages 6.19 (2026-02-08): wait4(2), getrusage(2), time(1).

**Copy read.** https://man7.org/linux/man-pages/man2/wait4.2.html (SHA-256 `3227e5a279c2c00b682498bdc276f8dc04918d70968bd615c36f8780a9855450`; footer `wait4.2.txt:179` "Linux man-pages 6.19            2026-02-08                       wait4(2)"), https://man7.org/linux/man-pages/man2/getrusage.2.html (SHA-256 `ade816073a4c25f6d272fbf628d7bdf6d9a5b4ae76b29f1889cc01420220d523`; footer `:260`), https://man7.org/linux/man-pages/man1/time.1.html (SHA-256 `1b95f934b1716a98d62add1851ed360da4c1f433054a136c0133ec674f2c9f21`; footer `:285`); fetched 2026-09-16; `sources/S4-07/`.

**Passages.**

- `wait4.2.txt:106–108`: "but additionally return resource usage information about the child in the structure pointed to by rusage."
- `getrusage.2.txt:88–94`: "RUSAGE_CHILDREN" / "Return resource usage statistics for all children of the calling process that have terminated and been waited for. These statistics will include the resources used by grandchildren, and further removed descendants, if all of the intervening descendants waited on their terminated children."
- `getrusage.2.txt:129–137`: "ru_utime" / "This is the total amount of time spent executing in user mode, expressed in a timeval structure (seconds plus microseconds)." / "ru_stime" / "This is the total amount of time spent executing in kernel mode, expressed in a timeval structure (seconds plus microseconds)."
- `getrusage.2.txt:166–169`: "ru_inblock (since Linux 2.6.22)" / "The number of times the filesystem had to perform input." / "ru_oublock (since Linux 2.6.22)" / "The number of times the filesystem had to perform output."; `:181–190`: "ru_nvcsw (since Linux 2.6)" / "The number of times a context switch resulted due to a process voluntarily giving up the processor before its time slice was completed (usually to await availability of a resource)." / "ru_nivcsw (since Linux 2.6)" / "The number of times a context switch resulted due to a higher priority process becoming runnable or because the current process exceeded its time slice."
- `time.1.txt:76–82`: "When command finishes, time writes a message to standard error giving timing statistics about this program run. These statistics consist of (i) the elapsed real time between invocation and termination, (ii) the user CPU time (the sum of the tms_utime and tms_cutime values in a struct tms as returned by times(2)), and (iii) the system CPU time (the sum of the tms_stime and tms_cstime values in a struct tms as returned by times(2))."
- `time.1.txt:95–97` (`-p`): "(with numbers in seconds) where the number of decimals in the output for %f is unspecified but is sufficient to express the clock tick accuracy, and at least one."
- `time.1.txt:143–150`: "%S     Total number of CPU-seconds that the process spent in kernel mode." / "%U     Total number of CPU-seconds that the process spent in user mode." / "%P     Percentage of the CPU that this job got, computed as (%U + %S) / %E."; `:224–225`: "-v, --verbose" / "Give very verbose output about all the program knows about."

**Coverage (T8).** Covers CPU time at exit for the wrapped child and, through `RUSAGE_CHILDREN` semantics, its waited-for descendants aggregated (object = one child plus descendants; unit = seconds+microseconds `timeval`; statistic = totals); covers I/O only as block-operation counts (`ru_inblock`/`ru_oublock`), not time blocked; covers context-switch counts. `time(1)` reports user and system CPU as tms sums including children (`tms_cutime`, `tms_cstime`), so it cannot separate the compiler from the shell that wraps it. Does not cover per-process values for processes not directly waited on by the wrapper (a wrapper around `make` sees one aggregate). Not an observation.

---

### S4-08 — `/proc/<pid>/stat` fields (`proc_pid_stat(5)`) and `/proc/<pid>/schedstat` (`sched-stats.rst`)

**Citation.** Linux man-pages 6.19 (2026-02-08): proc_pid_stat(5); Linux kernel v6.17 `Documentation/scheduler/sched-stats.rst`; `Documentation/filesystems/proc.rst` (checked, no schedstat text).

**Copy read.** https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html (SHA-256 `0f04d78946538fd84db1536845abeb236da51a04844989f34ea7ee7cb0b6700f`; footer `proc_pid_stat.5.txt:391` "Linux man-pages 6.19            2026-02-08               proc_pid_stat(5)"); https://raw.githubusercontent.com/torvalds/linux/v6.17/Documentation/scheduler/sched-stats.rst (SHA-256 `6c80bd9a62d50aa37161d6d909dfeff8c460c3b949454bf4c093c211f6252335`); https://raw.githubusercontent.com/torvalds/linux/v6.17/Documentation/filesystems/proc.rst (SHA-256 `265d46cc5507b19d371a35ed6bd37b0833dbd64a30a67fddef5c9bc316124e9f`); man7 `proc_pid_schedstat.5` does not exist (404). Fetched 2026-09-16; `sources/S4-08/`.

**Passages.**

- `proc_pid_stat.5.txt:171–174`: "(14) utime %lu" / "Amount of time that this process has been scheduled in user mode, measured in clock ticks (divide by sysconf(_SC_CLK_TCK))."; `:180–183`: "(15) stime %lu" / "Amount of time that this process has been scheduled in kernel mode, measured in clock ticks (divide by sysconf(_SC_CLK_TCK))."
- `proc_pid_stat.5.txt:230–234`: "(22) starttime %llu" / "The time the process started after system boot. Before Linux 2.6, this value was expressed in jiffies. Since Linux 2.6, the value is expressed in clock ticks (divide by sysconf(_SC_CLK_TCK))."
- `proc_pid_stat.5.txt:328–330`: "(42) delayacct_blkio_ticks %llu (since Linux 2.6.18)" / "Aggregated block I/O delays, measured in clock ticks (centiseconds)."
- `sched-stats.rst:190–198`: "/proc/<pid>/schedstat" / "schedstats also adds a new /proc/<pid>/schedstat file to include some of the same information on a per-process level. There are three fields in this file correlating for that process to:" / "1) time spent on the cpu (in nanoseconds)" / "2) time spent waiting on a runqueue (in nanoseconds)" / "3) # of timeslices run on this cpu".
- Reader's own grep: `proc.rst` contains no occurrence of `schedstat`, `/proc/<pid>/sched` or `SCHED_DEBUG`.

**Coverage (T8).** Covers what a `/proc` sampler (the given `proc_sampler.py`) can read per pid while the process is alive: CPU in clock ticks (`utime`, `stime`; with `CONFIG_HZ=1000` in S4-04 the userspace `_SC_CLK_TCK` is still the value `sysconf` reports, not documented here), start time in ticks, and aggregated block-I/O delay in clock ticks (`delayacct_blkio_ticks`, the tick-granular twin of taskstats' nanosecond `blkio_delay_total`); `/proc/<pid>/schedstat` gives on-CPU time and runqueue-wait time in nanoseconds plus a timeslice count, under `CONFIG_SCHEDSTATS` (=y in S4-04) and the `kernel.sched_schedstats` sysctl (S4-17). Does not cover values at exit (a sampler reads them only while the pid exists) — this is the mechanism behind censoring of short-lived processes, which no document here quantifies. Not an observation.

---

### S4-09 — perf: `perf-sched.txt`, `perf-record.txt`, `perf-trace.txt`, `perf-stat.txt`, `perf-security.rst` (kernel v6.17)

**Citation.** Linux kernel v6.17, `tools/perf/Documentation/perf-sched.txt`, `perf-record.txt`, `perf-trace.txt`, `perf-stat.txt`; `Documentation/admin-guide/perf-security.rst`.

**Copy read.** https://raw.githubusercontent.com/torvalds/linux/v6.17/tools/perf/Documentation/perf-sched.txt (SHA-256 `d2a924734550d42ab8e19bd3a820dfb637795118f810f396a59263aba2ea6b7e`), perf-record.txt (`91ffcc9dc0e5a570f1ed2f4689acb92a2a548da9f8e71248c56145d5878b9081`), perf-trace.txt (`e593ae5dd3c6f078139ed859297dc690ff823716880fd17c03a24bc1425fc077`), perf-stat.txt (`a1ec9986d93d3f1e1597db72558e8ebe731715f3e93f41e0c7df0d707470e2d0`), https://raw.githubusercontent.com/torvalds/linux/v6.17/Documentation/admin-guide/perf-security.rst (`080dc302bb2ed254192522e1b78d65d71a965d4d893634b052e595d65c6c9383`); fetched 2026-09-16; `sources/S4-09/`.

**Passages.**

- `perf-sched.txt:17–21`: "'perf sched record <command>' to record the scheduling events of an arbitrary workload." / "'perf sched latency' to report the per task scheduling latencies and other scheduling properties of the workload."
- `perf-sched.txt:59, 65–68`: "'perf sched timehist' provides an analysis of scheduling events." / "By default it shows the individual schedule events, including the wait time (time between sched-out and next sched-in events for the task), the task scheduling delay (time between runnable and actually running) and run time for the task:"; example rows `:70–79`: "time    cpu  task name             wait time  sch delay   run time" / "[tid/pid]                (msec)     (msec)     (msec)" / "79371.874569 [0011]  gcc[31949]                0.014      0.000      1.148" / "79371.874591 [0010]  gcc[31951]                0.000      0.000      0.024" / "79371.874746 [0005]  gcc[31949]                0.153      0.078      0.022"; `:81` "Times are in msec.usec."
- `perf-sched.txt:159–161` (timehist options): "-C=::" / "--cpu=::" / "Only show events for the given CPU(s) (comma separated list)."; `:189–191`: "-w::" / "--wakeups::" / "Show wakeup events."; `:212–213`: "--state::" / "Show task state when it switched out."; `:171–174`: "-s::" / "--summary::" / "Show only a summary of scheduling by thread with min, max, and average run times (in sec) and relative stddev."; `:225–230`: "--pre-migrations::" / "Show pre-migration wait time. pre-migration wait time is the time spent by a task waiting on a runqueue but not getting the chance to run there and is migrated to a different runqueue where it is finally run."
- `perf-record.txt:281–285`: "-m::" / "--mmap-pages=::" / "Number of mmap data pages (must be a power of two) or size specification in bytes with appended unit character - B/K/M/G. The size is rounded up to the nearest power-of-two page value."; `:385–392`: "--cpu::" / "Collect samples only on the list of CPUs provided. Multiple CPUs can be provided as a comma-separated list with no space: 0,1. Ranges of CPUs are specified with -: 0-2. In per-thread mode with inheritance mode on (default), samples are captured only when the thread executes on the designated CPUs. Default is to monitor all CPUs." / "User space tasks can migrate between CPUs, so when tracing selected CPUs, a dummy event is created to track sideband for all CPUs."; `:700–704`: "--overwrite::" / "Makes all events use an overwritable ring buffer. An overwritable ring buffer works like a flight recorder: when it gets full, the kernel will overwrite the oldest records, that thus will never make it to the perf.data file."; `:822–824` (`--threads` layouts): "Predefined layouts can be used on systems with large number of CPUs in order not to spawn multiple per-cpu streaming threads but still avoid LOST events in data directory files."
- `perf-trace.txt:16–18`: "This command will show the events associated with the target, initially syscalls, but other system events like pagefaults, task lifetime events, scheduling events, etc."; `:139–142`: "-s::" / "--summary::" / "Show only a summary of syscalls by thread with min, max, and average times (in msec) and relative stddev."; `:32–34`: "-a::" / "--all-cpus::" / "System-wide collection from all CPUs."
- `perf-stat.txt:583` (example output): "83723.452481      task-clock:u (msec)       #    1.004 CPUs utilized"; `:488–489`: "and -a (global monitoring) is needed, requiring root rights or perf.perf_event_paranoid=-1."
- `perf-security.rst:226–227`: "perf_events *scope* and *access* control for unprivileged processes is governed by perf_event_paranoid [2]_ setting:"; `:246–251`: ">=1:" / "*scope* includes per-process performance monitoring only and excludes system wide performance monitoring."; `:254–256`: ">=2:" / "*scope* includes per-process performance monitoring only. CPU and system events happened when executing in user space only can be monitored and captured for later analysis."; `:69–72`: "Unprivileged processes with enabled CAP_PERFMON capability are treated as privileged processes with respect to perf_events performance monitoring and observability operations, thus, bypass *scope* permissions checks in the kernel."

**Coverage (T8).** Covers what `perf sched record` + `timehist` yield per schedule event (object = each sched-in of a thread; wait time, scheduling delay, run time in msec.usec; `-w` adds wakeup rows; `-C` restricts the report to the pinned CPU; `--state` adds the sched-out state) and thus per-schedule run/wait for every thread that ran on the pinned CPU including short-lived ones; covers `perf trace -s` (per-thread syscall time summary) and `perf stat` `task-clock`. Covers the ring-buffer loss mode (LOST events; `-m` sizing; `--overwrite` flight-recorder) but gives no figure for data volume or overhead per CPU-second. Covers the privilege gate (`perf_event_paranoid`, `CAP_PERFMON`; the runner's Ubuntu default is in S4-21; `sudo` is available per S4-01). Not an observation.

---

### S4-10 — `strace(1)`: `-f`, `-c`, `-w`, `-O`

**Citation.** strace manual page as published at man7.org (strace project; page footer not captured in the text conversion — see copy).

**Copy read.** https://man7.org/linux/man-pages/man1/strace.1.html, fetched 2026-09-16; 85 238 bytes; SHA-256 `eedefecf7c55cf36976fce6fbfff8b1340c62b696bb7268a83df643ee8ea02f6`; `sources/S4-10/strace.1.html`, text `strace.1.txt`.

**Passages.**

- `strace.1.txt:327–333`: "-f" / "--follow-forks" / "Traces child processes as they are created by currently traced processes as a result of the fork(2), vfork(2) and clone(2) system calls."
- `strace.1.txt:976–983`: "-c" / "--summary-only" / "Counts time, calls, and errors for each system call and report a summary on program exit, suppressing the regular output. This shows system time (CPU time spent in the kernel), which is independent of wall clock time. If -c is used with -f, only aggregate totals for all traced processes are kept."
- `strace.1.txt:990–1000`: "-O overhead" / "--summary-syscall-overhead=overhead" / "Sets the overhead for tracing system calls to overhead. This is useful for overriding the default heuristic, which estimates the time spent in the measurement process itself when timing system calls with the -c option. The same overhead is subtracted from polymorphic time columns and from wall-total, wall-min, wall-max, and wall-avg. The accuracy of the heuristic can be gauged by timing a given program run without tracing (using time(1)) and comparing the accumulated system call time to the total produced"
- `strace.1.txt:1062–1066`: "-w" / "--summary-wall-clock" / "Summarizes the wall clock time for each system call, measured from its beginning to its end. The default is to summarize the system time."
- `strace.1.txt:341–345` (the `-ff` note): "This is incompatible with -c, since no per-process counts are kept."

**Coverage (T8).** Covers `strace -f -c -w`: per-syscall wall-clock totals over the whole traced tree, aggregated ("only aggregate totals for all traced processes are kept"), so it cannot give per-process blocked time; documents that tracing adds measurement overhead the tool tries to subtract (`-O`), without quantifying it. Not an observation.

---

### S4-11 — BCC `exitsnoop` / `execsnoop` and bpftrace `tracepoint` probes

**Citation.** iovisor/bcc, `tools/exitsnoop.py`, `tools/exitsnoop_example.txt`, `tools/execsnoop.py`, `tools/execsnoop_example.txt` (branch master); bpftrace/bpftrace `docs/language.md` (branch master).

**Copy read.** https://raw.githubusercontent.com/iovisor/bcc/master/tools/exitsnoop.py (SHA-256 `ec9373486fbee101f7f57e49f597896ad2e9a6d9c43fbc2d0248a3762c946280`), exitsnoop_example.txt (`d0201cde5db059ccde7271138b696d843a246d56218e72585cd4918d63d5aa05`), execsnoop.py (`ffde91812e5bc04d8bc56ade7d44a4a501b65c2bd5114c36a143e7485146f3bd`), execsnoop_example.txt (`ea1c06774c61270abb205c00fc3c8ecdcf96f8a807384a108027f2a021f695c9`); https://raw.githubusercontent.com/bpftrace/bpftrace/master/docs/language.md (`53e6870cb79ec6def8142d925185f0616d06babfda7d355b298131c4e60861ca`) and docs/stdlib.md (`61f27ecad1b518314e06290183209a11309e7f1c87d2c4130eecf507720ebda5`); commits not resolvable (see S4-02); fetched 2026-09-16; `sources/S4-11/`.

**Passages.**

- `exitsnoop_example.txt:3–9`: "This Linux tool traces all process terminations and reason, it" / "- is implemented using BPF, which requires CAP_SYS_ADMIN and" / "should therefore be invoked with sudo" / "- traces sched_process_exit tracepoint in kernel/exit.c" / "- includes processes by root and all users" / "- includes processes in containers" / "- includes processes that become zombie".
- `exitsnoop_example.txt:22–24`: "PCOMM            PID    PPID   TID    AGE(s)  EXIT_CODE" / "sleep            19004  19003  19004  1.65    0" / "bash             19003  17656  19003  1.65    code 65"; `:34–37`: "The output shows the process/command name (PCOMM), the PID, the process that will be notified (PPID), the thread (TID), the AGE of the process with hundredth of a second resolution, and the reason for the process exit (EXIT_CODE)."
- `exitsnoop.py:99–113` (the BPF program): "TRACEPOINT_PROBE(sched, sched_process_exit)" / "struct task_struct *task = (typeof(task))bpf_get_current_task();" / ... / "data.start_time = PROCESS_START_TIME_NS," / "data.exit_time = bpf_ktime_get_ns()," / "data.pid = task->tgid," / "data.tid = task->pid," / "data.ppid = task->real_parent->tgid," / "data.exit_code = task->exit_code >> 8," / "data.sig_info = task->exit_code & 0xFF," / "bpf_get_current_comm(&data.task, sizeof(data.task));"; the data struct `:86–94` has fields "u64 start_time; u64 exit_time; u32 pid; u32 tid; u32 ppid; int exit_code; u32 sig_info; char task[TASK_COMM_LEN];" and no CPU-time field.
- `exitsnoop.py:38`: "77 EX_NOPERM    Need sudo (CAP_SYS_ADMIN) for BPF() system call".
- `execsnoop.py:4, 11–14`: "# execsnoop Trace new processes via exec() syscalls." / "# This currently will print up to a maximum of 19 arguments, plus the process" / "# name, so 20 fields in total (MAXARG)." / "# This won't catch all new processes: an application may fork() but not exec()."
- `bpftrace language.md:1531–1535, 1541–1542, 1553`: "### tracepoint" / "* `tracepoint:subsys:event`" / "Tracepoints are hooks into events in the kernel. Tracepoints are defined in the kernel source and compiled into the kernel binary which makes them a form of static tracing." / "Tracepoint arguments are available in the `args` struct which can be inspected with verbose listing"; `:1566`: "Alternatively members for each tracepoint can be listed from their /format file in /sys."
- Reader's own grep: neither `exitsnoop.py`, `execsnoop.py` nor their example files contain "lost", "dropped" or "missed".

**Coverage (T8).** Covers per-process lifetime at exit from the `sched:sched_process_exit` tracepoint (object = every exiting task; AGE = exit_time − task start_time, nanoseconds internally, printed at 0.01 s resolution) and exec events with argv (execsnoop), both under `CAP_SYS_ADMIN`/sudo; the exitsnoop program reads `task_struct` fields directly, so the same probe could read the task's CPU counters, but the shipped tool does not emit CPU time or blocked time. Does not document event loss under load. Kernel requirement `CONFIG_BPF_SYSCALL`, `CONFIG_BPF_EVENTS`, `CONFIG_TRACEPOINTS` (all `=y` in S4-04). Not an observation.

---

### S4-12 — forkstat(8): proc-connector fork/exec/exit logging and its documented loss

**Citation.** Colin Ian King, *forkstat* — `forkstat.8` (dated "16 April 2025" in its `.TH`), `README.md`, `forkstat.c`, repository ColinIanKing/forkstat, branch master.

**Copy read.** https://raw.githubusercontent.com/ColinIanKing/forkstat/master/forkstat.8 (SHA-256 `7776450b37f5e42d77b1826e5d4d01f7f65ec3ed703269b2a87d2e982aababa2`), README.md (`b3efd99ffda6b3adc3732ac87494f794fe2607b4ee1bd6e458f21ca3eb4e7d68`), forkstat.c (`470ffb5c1df1112e92eb81473f71aaac219ec79fcd3dcea89ef767980cce6971`); commit not resolvable; fetched 2026-09-16; `sources/S4-12/`. The Ubuntu noble package is forkstat 0.03.02-1 (S4-20).

**Passages.**

- `forkstat.8:27–28`: "Forkstat is a program that logs process fork(), exec(), exit(), coredump and process name change activity."
- `forkstat.8:32–34`: "Note that forkstat uses the Linux netlink connector to gather process activity and this may miss events if the system is overly busy. Netlink connector also requires root privilege." (identically `README.md:9`.)
- `forkstat.8:42–47` (columns): "Time	When the fork/exec/exit event occurred." / "PID	Process or thread ID." / "Info	Parent or child if a fork, or process exit(2) value." / "Duration	T{" / "On exit, the duration the command ran for in seconds."
- `forkstat.c:1463`: "if ((sock = socket(PF_NETLINK, SOCK_DGRAM, NETLINK_CONNECTOR)) < 0) {"; `:1511`: "op = PROC_CN_MCAST_LISTEN;"; `:1542–1556` (the receive loop's ENOBUFS branch): "case ENOBUFS: {" / ... / "(void)printf("%2.2d:%2.2d:%2.2d recv ----- " / ""nobufs %8.8s (%s)\n"," / ...; `:1690–1700` (exit event): "if (info1->start.tv_sec) {" / ... / "d1 = timeval_to_double(&info1->start);" / "d2 = timeval_to_double(&tv);" / "(void)snprintf(duration, sizeof(duration), "%8s", secs_to_str(d2 - d1));" / "} else {" / "(void)snprintf(duration, sizeof(duration), "unknown");".

**Coverage (T8).** Covers lifetime (exit-event "Duration", computed in user space from the fork/exec event's arrival time to the exit event's arrival time, using `gettimeofday`, and "unknown" if the start was not seen) and exit code per process, from the proc connector (`CONFIG_CONNECTOR`, `CONFIG_PROC_EVENTS` = y in S4-04); root required. Documents the loss mode in its own words ("may miss events if the system is overly busy"; ENOBUFS lines written into the log) without quantifying it. Does not cover CPU time or I/O blocking (the exit event carries only `exit_code`). Not an observation.

---

### S4-13 — GNU make manual (`doc/make.texi`, edition 0.77): `--trace`, `--debug=j`, `-j`, `-l`

**Citation.** Free Software Foundation, *GNU make* manual, source `doc/make.texi` ("@set EDITION 0.77", `make.texi:6`), git.savannah.gnu.org make.git, master.

**Copy read.** https://git.savannah.gnu.org/cgit/make.git/plain/doc/make.texi (mirror used because www.gnu.org gave no response — search-log rows 1, 19), fetched 2026-09-16; 554 484 bytes; SHA-256 `c58aed707907b3477e7817c4cd5319ec33bee6142beed9de575faa9a4a616428`; commit not pinned by the plain URL; `sources/S4-13/make.texi`.

**Passages.**

- `make.texi:9998–10001`: "@item --trace" / "@cindex @code{--trace}" / "Show tracing information for @code{make} execution. Using @code{--trace} is" / "shorthand for @code{--debug=print,why}."
- `make.texi:9685–9686`: "@item j (@i{jobs})" / "Prints messages giving details on the invocation of specific sub-commands."; `:9694–9696`: "@item p (@i{print})" / "Prints the recipe to be executed, even when the recipe is normally" / "silent (due to @code{.SILENT} or @samp{@@})."; `:9698–9700`: "@item w (@i{why})" / "Explains why each target must be remade by showing which prerequisites" / "are more up to date than the target."
- `make.texi:9763–9769`: "@item -j [@var{jobs}]" / ... / "Specifies the number of recipes (jobs) to run simultaneously. With no" / "argument, @code{make} runs as many recipes simultaneously as are allowed by" / "the dependency graph."
- `make.texi:9791–9800`: "@item -l [@var{load}]" / ... / "Specifies that no new recipes should be started if there are other" / "recipes running and the load average is at least @var{load} (a" / "floating-point number). With no argument, removes a previous load" / "limit."; `:4434–4437`: "More precisely, when @code{make} goes to start up a job, and it already has" / "at least one job running, it checks the current load average; if it is not" / "lower than the limit given with @samp{-l}, @code{make} waits until the load" / "average goes below that limit, or until all the other jobs finish."; `:4439` "By default, there is no load limit."

**Coverage (T8).** Covers what `make --trace` and `--debug=j` print (recipe text and why-remade; job sub-command invocation details), i.e. the dispatch record available without root or kernel support; covers that `-l` consults the system load average (the manual does not name `/proc/loadavg`) and that no load limit applies by default — relevant because the given workflow runs `make -j8` on one pinned CPU with no `-l`. Does not cover how make behaves when the process is confined to one CPU. Not an observation.

---

### S4-14 — PSI (`psi.rst`) and cgroup v2 (`cgroup-v2.rst`): `cpu.pressure`, `io.pressure`, `cpu.stat`, `cpuset.cpus`

**Citation.** Linux kernel v6.17, `Documentation/accounting/psi.rst`, `Documentation/admin-guide/cgroup-v2.rst`.

**Copy read.** https://raw.githubusercontent.com/torvalds/linux/v6.17/Documentation/accounting/psi.rst (SHA-256 `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692`), .../Documentation/admin-guide/cgroup-v2.rst (SHA-256 `4c6248886425e22566f5b3b905939eef59d824007e11eaf6dd73933f08695559`); fetched 2026-09-16; `sources/S4-14/`.

**Passages.**

- `psi.rst:37–38`: "Pressure information for each resource is exported through the respective file in /proc/pressure/ -- cpu, memory, and io."; `:42–43`: "some avg10=0.00 avg60=0.00 avg300=0.00 total=0" / "full avg10=0.00 avg60=0.00 avg300=0.00 total=0"; `:45–46`: "The "some" line indicates the share of time in which at least some tasks are stalled on a given resource."; `:48–49`: "The "full" line indicates the share of time in which all non-idle tasks are stalled on a given resource simultaneously."; `:57–58`: "CPU full is undefined at the system level, but has been reported since 5.13, so it is set to zero for backward compatibility."; `:60–63`: "The ratios (in %) are tracked as recent trends over ten, sixty, and three hundred second windows, which gives insight into short term events as well as medium and long term trends. The total absolute stall time (in us) is tracked and exported as well".
- `cgroup-v2.rst:1122–1131`: "cpu.stat" / "A read-only flat-keyed file." / "This file exists whether the controller is enabled or not." / "It always reports the following three stats, which account for all the processes in the cgroup:" / "- usage_usec" / "- user_usec" / "- system_usec"; `:1194–1200`: "cpu.pressure" / "A read-write nested-keyed file." / "Shows pressure stall information for CPU." / "This file accounts for all the processes in the cgroup."; `:2123–2126`: "io.pressure" / "A read-only nested-keyed file." / "Shows pressure stall information for IO."; `:2409–2416`: "cpuset.cpus" / "A read-write multiple values file which exists on non-root cpuset-enabled cgroups." / "It lists the requested CPUs to be used by tasks within this cgroup. The actual list of CPUs to be granted, however, is subjected to constraints imposed by its parent and can differ from the requested CPUs."; `:2431–2437`: "cpuset.cpus.effective" / "A read-only multiple values file which exists on all cpuset-enabled cgroups." / "It lists the onlined CPUs that are actually granted to this cgroup by its parent."

**Coverage (T8).** Covers group-level (not per-process) accounting available if the build is run in its own cgroup: `cpu.stat` CPU totals in microseconds for all processes of the group; `cpu.pressure`/`io.pressure` share-of-time stalled ("some"/"full") with a cumulative `total` in microseconds; `cpuset.cpus` as an alternative to `taskset` for confining the group to one CPU. `CONFIG_PSI=y` and `PSI_DEFAULT_DISABLED` unset in S4-04, so PSI is on by default on the runner kernel. Does not cover per-process values. Not an observation.

---

### S4-15 — systemd: `AllowedCPUs=`, `CPUQuota=`, `systemd-run --scope -p`

**Citation.** systemd manual pages `systemd.resource-control(5)` and `systemd-run(1)`, "latest" on freedesktop.org (the page header reads "systemd 261.2", `systemd.resource-control.txt:2`); the runner image ships systemd 255.4 (S4-02 `:12`).

**Copy read.** https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html (SHA-256 `d20f68b72a7ef8340c16cd081b9732cc58b8a4db15a8c857f39fc1853b3b8a2e`), https://www.freedesktop.org/software/systemd/man/latest/systemd-run.html (SHA-256 `53caa09ae4d1a8768278038d03d75b792690f29d109ed969cf1447d69c9088a1`); fetched 2026-09-16; `sources/S4-15/`.

**Passages.**

- `systemd.resource-control.txt:170–172`: "AllowedCPUs=, StartupAllowedCPUs=" / "This setting controls the cpuset controller in the unified hierarchy." / "Restrict processes to be executed on specific CPUs. Takes a list of CPU indices or ranges separated by either whitespace or commas."; `:174–176`: "Setting AllowedCPUs= or StartupAllowedCPUs= does not guarantee that all of the CPUs will be used by the processes as it may be limited by parent units. The effective configuration is reported as EffectiveCPUs=."; `:182` "Added in version 244."
- `systemd.resource-control.txt:146–152`: "CPUQuota=" / "This setting controls the cpu controller in the unified hierarchy." / "Assign the specified CPU time quota to the processes executed. Takes a percentage value, suffixed with "%". The percentage specifies how much CPU time the unit shall get at maximum, relative to the total CPU time available on one CPU. Use values > 100% for allotting CPU time on more than one CPU. This controls the "cpu.max" attribute on the unified control group hierarchy"; `:154–155`: "Example: CPUQuota=20% ensures that the executed processes will never get more than 20% CPU time on one CPU."
- `systemd-run.txt:57–59`: "--scope" / "Create a transient .scope unit instead of the default transient .service unit (see above)."; `:65–68`: "--property=, -p" / "Sets a property on the scope or service unit that is created. This option takes an assignment in the same format as systemctl(1)'s set-property command."; `:28–32`: "If a command is run as transient scope unit, it will be executed by systemd-run" ... "will return only when the command finishes. This mode is enabled via the --scope switch".

**Coverage (T8).** Covers the mechanism by which a root-capable job could confine either the build or a root-owned service to a CPU set (`systemd-run --scope -p AllowedCPUs=...`; `systemctl set-property <unit> AllowedCPUs=` on an existing unit) and cap it (`CPUQuota=`), with per-unit `cpu.stat`/pressure accounting following from S4-14. Does not say which units exist on the runner image (S4-02 does not list its running services) or whether the hosted-compute agent runs as a systemd unit. Not an observation.

---

### S4-16 — The pin's effects: `taskset(1)`, `sched_setaffinity(2)`, `nproc(1)` + coreutils/gnulib `nproc.c`, Python `os.cpu_count` / `os.process_cpu_count` / `os.sched_getaffinity`

**Citation.** util-linux taskset(1) (page footer `taskset.1.txt:246`: "util-linux 2.43.devel-739-eee2e 2026-05-24"); Linux man-pages 6.19 sched_setaffinity(2) (footer `:364`, 2026-02-08); GNU coreutils 9.11 nproc(1) (footer `nproc.1.txt:127`: "GNU coreutils 9.11              April 2026"); coreutils `src/nproc.c` and gnulib `lib/nproc.c` (master); Python 3 documentation, `os` module.

**Copy read.** https://man7.org/linux/man-pages/man1/taskset.1.html (SHA-256 `2a2bf31d0942b0a16b863703c9d81f0db9e9ce72252f45a05c2e9c38ad3e58a1`), https://man7.org/linux/man-pages/man2/sched_setaffinity.2.html (`a55f0f1590ae5fb208ac66794b901995b767d9f9ea6e82b11383af85b3cc87d6`), https://man7.org/linux/man-pages/man1/nproc.1.html (`4018eea68e67a925231b8d5d81b18af917f63d2950ec8c0fe914d3d48b90f5e2`), https://raw.githubusercontent.com/coreutils/coreutils/master/src/nproc.c (`68fed48321bcfc5c64f12601a6fc7c1689b1dd6c7f0737f69a61a5c0a45f86d8`), https://raw.githubusercontent.com/coreutils/gnulib/master/lib/nproc.c (`bb85782659919a439a09574f699b18206ef38082e9ce7231f3d2b307fa4e896d`), https://docs.python.org/3/library/os.html (`445393fa10ee7fb88e4ac04ccdd7e30b3c3c1e9d5c645d1057b20ab342ddd932`); commits of the raw files not resolvable; fetched 2026-09-16; `sources/S4-16/`. The runner image's coreutils apt package is 9.4-3ubuntu6.3 (S4-02 apt table, line "| coreutils              | 9.4-3ubuntu6.3               |") and its Python is 3.12.3 (S4-02 `:28`).

**Passages.**

- `sched_setaffinity.2.txt:193–194`: "A child created via fork(2) inherits its parent's CPU affinity mask. The affinity mask is preserved across an execve(2)."
- `sched_setaffinity.2.txt:136–141`: "EPERM  (sched_setaffinity()) The calling thread does not have appropriate privileges. The caller needs an effective user ID equal to the real user ID or effective user ID of the thread identified by pid, or it must possess the CAP_SYS_NICE capability in the user namespace of the thread pid."
- `sched_setaffinity.2.txt:183–187`: "The isolcpus boot option can be used to isolate one or more CPUs at boot time, so that no processes are scheduled onto those CPUs. Following the use of this boot option, the only way to schedule processes onto the isolated CPUs is via sched_setaffinity() or the cpuset(7) mechanism."
- `taskset.1.txt:162–165` (PERMISSIONS): "A user can change the CPU affinity of a process belonging to the same user. A user must possess CAP_SYS_NICE to change the CPU affinity of a process belonging to another user. A user can retrieve the affinity mask of any process."; `:86–87`: "The affinity of some processes like kernel per-CPU threads cannot be set."
- `nproc.1.txt:75–79`: "Print the number of processing units available to the current process, which may be less than the number of online processors. If the 'OMP_NUM_THREADS' or 'OMP_THREAD_LIMIT' environment variables are set, then they will determine the minimum and maximum returned value respectively."; `:81–82`: "--all  print the number of installed processors, disregarding any OpenMP environment variables, or CPU quotas."
- `gnulib lib/nproc.c:239–245`: "/* On systems with a modern affinity mask system call, we have" / "sysconf (_SC_NPROCESSORS_CONF)" / ">= sysconf (_SC_NPROCESSORS_ONLN)" / ">= num_processors_via_affinity_mask ()" / "The first number is the number of CPUs configured in the system." / "The second number is the number of CPUs available to the scheduler." / "The third number is the number of CPUs available to the current process."; `:254–261`: "if (query == NPROC_CURRENT)" / "{" / "/* Try the modern affinity mask system call.  */" / "{" / "unsigned long nprocs = num_processors_via_affinity_mask ();" / "if (nprocs > 0)" / "return nprocs;"; `:144` "if (sched_getaffinity (0, size, set) == 0)". coreutils `src/nproc.c:94`: "enum nproc_query mode = NPROC_CURRENT_OVERRIDABLE;"; `:108`: "mode = NPROC_ALL;" (under `--all`); `:127`: "unsigned long nproc = num_processors (mode);".
- `python-os.txt:3537–3539`: "os.cpu_count()" / "Return the number of logical CPUs in the system. Returns None if undetermined."; `:3550–3553`: "os.process_cpu_count()" / "Get the number of logical CPUs usable by the calling thread of the current process. Returns None if undetermined. It can be less than cpu_count() depending on the CPU affinity."; `:3511–3514`: "os.sched_getaffinity(pid, /)" / "Return the set of CPUs the process with PID pid is restricted to. If pid is zero, return the set of CPUs the calling thread of the current process is restricted to."; `:3559` "Added in version 3.13." (for `process_cpu_count`).

**Coverage (T8).** Covers that a `taskset -c N` pin is inherited by every fork and preserved across exec, so all of a build's processes stay on the pinned CPU; that moving another user's (root's) process needs `CAP_SYS_NICE` (available through passwordless sudo, S4-01) while kernel per-CPU threads cannot be moved; that `nproc` returns the affinity-mask count (so `make -j$(nproc)` under a one-CPU pin gives `-j1`, whereas the given workflow's explicit `-j8` is unaffected); that Python 3.12's `os.cpu_count()` returns the system count while `os.sched_getaffinity(0)` returns the pinned set (`os.process_cpu_count()` only from 3.13). Not an observation.

---

### S4-17 — sysctls and boot parameters: `kernel.task_delayacct`, `kernel.perf_event_paranoid`, `kernel.sched_schedstats`, `kernel.acct`, `vm.drop_caches`, `delayacct`, `isolcpus=`, `nohz_full=`, `psi=`, `schedstats=`

**Citation.** Linux kernel v6.17, `Documentation/admin-guide/sysctl/kernel.rst`, `Documentation/admin-guide/sysctl/vm.rst`, `Documentation/admin-guide/kernel-parameters.txt`.

**Copy read.** https://raw.githubusercontent.com/torvalds/linux/v6.17/Documentation/admin-guide/sysctl/kernel.rst (SHA-256 `c18e37e1b32344d7600bca19b72f5d40af855cf7889c09890568da6a3d24f337`), .../sysctl/vm.rst (`5cf010b57064fcb15c5d154be6f01e0522006a12d09007c0adcc99590689de64`), .../kernel-parameters.txt (`7b2ea6c48029e18f6178db866ded6315d40abf09aeb4e0d624e2ec7039083adb`); fetched 2026-09-16; `sources/S4-17/`.

**Passages.**

- `sysctl-kernel.rst:1243–1249`: "task_delayacct" / "Enables/disables task delay accounting (see Documentation/accounting/delay-accounting.rst. Enabling this feature incurs a small amount of overhead in the scheduler but is useful for debugging and performance tuning. It is required by some tools such as iotop."
- `sysctl-kernel.rst:1251–1256`: "sched_schedstats" / "Enables/disables scheduler statistics. Enabling this feature incurs a small amount of overhead in the scheduler but is useful for debugging and performance tuning."
- `sysctl-kernel.rst:968–972`: "perf_event_paranoid" / "Controls use of the performance events system by unprivileged users (without CAP_PERFMON). The default value is 2."; `:981` " -1  Allow use of (almost) all events by all users."; `:986–987` ">=0  Disallow ftrace function tracepoint by users without ``CAP_PERFMON``."; `:991` ">=1  Disallow CPU event access by users without ``CAP_PERFMON``."; `:993` ">=2  Disallow kernel profiling by users without ``CAP_PERFMON``." (the mainline table ends at >=2; Ubuntu's level 4 is in S4-21).
- `sysctl-kernel.rst:32–42`: "acct" / "highwater lowwater frequency" / "If BSD-style process accounting is enabled these values control its behaviour. If free space on filesystem where the log lives goes below ``lowwater``\ % accounting suspends. If free space gets above ``highwater``\ % accounting resumes."
- `sysctl-vm.rst:245–256`: "drop_caches" / "Writing to this will cause the kernel to drop clean caches, as well as reclaimable slab objects like dentries and inodes. Once dropped, their memory becomes free." / "To free pagecache::" / "echo 1 > /proc/sys/vm/drop_caches" / "To free reclaimable slab objects (includes dentries and inodes)::".
- `kernel-parameters.txt:1135`: "delayacct	[KNL] Enable per-task delay accounting"; `:2618–2619`: "isolcpus=	[KNL,SMP,ISOL] Isolate a given set of CPUs from disturbance." / "[Deprecated - use cpusets instead]"; `:2641–2646` (domain flag): "Isolate from the general SMP balancing and scheduling algorithms. Note that performing domain isolation this way is irreversible: it's not possible to bring back a CPU to the domains once isolated through isolcpus. It's strongly advised to use cpusets instead to disable scheduler load balancing through the "cpuset.sched_load_balance" file."; `:4264–4268`: "nohz_full=	[KNL,BOOT,SMP,ISOL]" / "The argument is a cpu list, as described above." / "In kernels built with CONFIG_NO_HZ_FULL=y, set the specified list of CPUs whose tick will be stopped whenever possible. The boot CPU will be forced outside the range to maintain the timekeeping."; `:5244–5246`: "psi=		[KNL] Enable or disable pressure stall information" / "tracking." / "Format: <bool>"; `:6486–6489`: "schedstats=	[KNL,X86] Enable or disable scheduled statistics." / "Allowed values are enable and disable. This feature incurs a small amount of overhead in the scheduler but is useful for debugging and performance tuning."

**Coverage (T8).** Covers the runtime switches a job with sudo can flip without a reboot (`kernel.task_delayacct=1`, `kernel.sched_schedstats=1`, `kernel.perf_event_paranoid`, `vm.drop_caches=3` — the last being the page-cache control the given workflow already uses) and those that are boot parameters and therefore unavailable on a hosted runner that cannot be rebooted into a chosen cmdline (`delayacct`, `isolcpus=`, `nohz_full=`, `psi=`, `schedstats=`); the mainline default for `perf_event_paranoid` (2) and the mainline meaning of its levels. Does not state the runner's actual sysctl values. Not an observation.

---

### S4-18 — Disk type: Azure temporary disk and `/sys/block/<disk>/queue/rotational`

**Citation.** Microsoft Learn, *Azure managed disks overview* (page metadata `ms.date` 2026-08-20, `managed-disks-overview.html:79`); Linux kernel v6.17 `Documentation/ABI/stable/sysfs-block`.

**Copy read.** https://learn.microsoft.com/en-us/azure/virtual-machines/managed-disks-overview (SHA-256 `bf7e29a06ea1dfcc64614abbb95bb73ede3052f0250e7583bafb40452f4ddef6`), https://raw.githubusercontent.com/torvalds/linux/v6.17/Documentation/ABI/stable/sysfs-block (SHA-256 `feaacfc02790f638f5e120e4976da8b68e50f64ea352108f547b7dffd0e0998b`); fetched 2026-09-16; `sources/S4-18/`.

**Passages.**

- `managed-disks-overview.txt:103–106`: "Temporary disk" / "Most VMs contain a temporary disk, which isn't a managed disk. The temporary disk provides short-term storage for applications and processes. It's intended for storing only data such as page files, swap files, or SQL Server tempdb files." / "Data on the temporary disk might be lost during a maintenance event, when you redeploy a VM, or when you stop the VM." / "On Azure Linux VMs, the temporary disk is typically /dev/disk/azure/resource."
- `managed-disks-overview.txt:30`: "There are five types of managed disks: Ultra Disks, Premium solid-state drives (SSD) v2, Premium SSD, Standard SSD, and Standard hard disk drives (HDD)."
- `sysfs-block:664–669`: "What:		/sys/block/<disk>/queue/rotational" / "Date:		January 2009" / ... / "[RW] This file is used to stat if the device is of rotational type or non-rotational type."

**Coverage (T8).** Covers how a job can read the disk type it got (`/sys/block/<disk>/queue/rotational`) and that an Azure Linux VM's temporary disk appears at `/dev/disk/azure/resource` and is non-persistent. Does not say which disk the runner's workspace lives on, its managed-disk tier, or its throughput; GitHub's table only says "Storage (SSD) 14 GB" (S4-01). Not an observation.

---

### S4-19 — RunsOn, "Fastest GitHub Actions Runners: CPU Speed" (benchmark aggregator; CPU models seen on GitHub official runners)

**Citation.** RunsOn (a commercial self-hosted-runner vendor), *Fastest GitHub Actions Runners: CPU Speed*, https://runs-on.com/benchmarks/github-actions-cpu-performance/, "Last updated: Sep 2, 2026". Secondary and vendor-authored; cited only for the CPU model strings and sample counts it reports for GitHub's official runners.

**Copy read.** URL above (the same bytes are served at https://runs-on.com/reference/benchmarks-gha-providers/), fetched 2026-09-16; 323 702 bytes; SHA-256 `c9ec0880237a6201facc8fbcc63d477dae4574dc4bae4a40f5f8279e7ea784fd`; `sources/S4-19/runs-on-cpu-performance.html`, text `.txt`.

**Passages.**

- `runs-on-cpu-performance.txt:41–43`: "Last updated: Sep 2, 2026" / "Benchmarks use Linux runners only, the Passmark single-thread metric, and the last 30 days of data."
- `runs-on-cpu-performance.txt:165–172` (leaderboard row): "8 GitHub Official" / "ubuntu-24.04, github24-2cpu-x64" / "$0.006/min ≈ GitHub" / "p50: 3382p90: 3479" / "p50: 7.0sp90: 11.0s" / "Intel(R) Xeon(R) 6973P-C (x86_64)" / "Azure" / "2 samples".
- `runs-on-cpu-performance.txt:222–229`: "15 GitHub Official" / "ubuntu-24.04, github24-2cpu-x64" / "$0.006/min ≈ GitHub" / "p50: 2674p90: 2735" / "p50: 7.0sp90: 8.0s" / "INTEL(R) XEON(R) PLATINUM 8573C (x86_64)" / "Azure" / "4 samples".
- `runs-on-cpu-performance.txt:74, 76–78` (a second table, same page): "14GitHububuntu-24.04, github24-2cpu-x64Official2×8GB347911s$0.0060≈ GitHub40" / "16GitHububuntu-24.04, github24-2cpu-x64Official2×8GB26787s$0.0060≈ GitHub17" / "17GitHububuntu-24.04, github24-2cpu-x64Official2×8GB22697s$0.0060≈ GitHub4" / "18GitHububuntu-24.04, github24-2cpu-x64Official2×8GB21956s$0.0060≈ GitHub2".

**Coverage (T8).** Covers hardware variance across GitHub-hosted `ubuntu-24.04` jobs as one vendor's 30-day sample: at least two distinct Intel Xeon models ("Xeon(R) 6973P-C", "XEON(R) PLATINUM 8573C") with Passmark single-thread p50 of 3382 vs 2674 (a 26 % spread between models on the same label), and four distinct GitHub-official rows in the second table with scores 3479/2678/2269/2195. Object = GitHub official `ubuntu-24.04` runner (the vendor labels it "github24-2cpu-x64", "2×8GB" — the private-repository shape, not the 4-vCPU public one of S4-01); statistic = Passmark single-thread p50/p90; population = 2–40 samples per row in the 30 days before 2026-09-02. It is one observation window by one party with an undisclosed harness, so it locates the phenomenon (CPU model differs run to run) but is not a value. Machine named (CPU model), subject named (a synthetic benchmark, not a build), window named (30 days to 2026-09-02).

---

### S4-20 — Ubuntu 24.04 (noble) package availability of the instruments (packages.ubuntu.com)

**Citation.** Canonical, packages.ubuntu.com, noble pages for `forkstat`, `linux-tools-common`, `bpfcc-tools`, `bpftrace`, `acct`, `trace-cmd`.

**Copy read.** https://packages.ubuntu.com/noble/<package>, fetched 2026-09-16; `sources/S4-20/pkg-<package>.html`; SHA-256: forkstat `98f649192db9f4e2e5e38a84651b6435c116d142129f591f5100428e649aedc4`; linux-tools-common `e27ba108c985983b28cbe218d345ac7e632c4d5fafcb0afd68df18fb2c9e9e64`; bpfcc-tools `8abfc8a66d321422ac4e3948af38b7bdad18aad4d52cbfa6d93e307e37be3a5d`; bpftrace `e8643a16ae4fcb880c0a1266f609d5d3fbfdc3ca79294d1b40e1d869df629e4e`; acct `4a8a2723f672c5304a7f719c47063b3cef79a42ccc23c6732dfaeabe2989ac37`; trace-cmd `3eaa166d323032d5a60131c7624671556bddfb2285a3059883f856ec10a03216`.

**Passages** (each page's "Package:" heading line, from the converted text): "Package: forkstat (0.03.02-1)" with "[universe]"; "Package: linux-tools-common (6.8.0-139.139)" (source package "linux"); "Package: bpfcc-tools (0.29.1+ds-1ubuntu7)"; "Package: bpftrace (0.20.2-1ubuntu4)"; "Package: acct (6.6.4-5build1)"; "Package: trace-cmd (3.2-1ubuntu2)".

Also from S4-04's Launchpad version page (`launchpad-linux-azure-6.17_6.17.0-1022.22.html`, link hrefs): the source package builds binaries named "linux-tools-6.17.0-1022-azure", "linux-cloud-tools-6.17.0-1022-azure", "linux-headers-6.17.0-1022-azure", "linux-modules-6.17.0-1022-azure", "linux-buildinfo-6.17.0-1022-azure" for noble.

**Coverage (T8).** Covers that every user-space instrument in T8 is installable from the noble archive with the runner's passwordless sudo: `forkstat` (already installed by the given workflow), `acct` (BSD accounting tools `accton`, `sa`, `lastcomm`), `bpfcc-tools` (execsnoop/exitsnoop), `bpftrace`, `trace-cmd`, and `perf` through `linux-tools-common` plus the kernel-matching `linux-tools-6.17.0-1022-azure` (the `linux-tools-common` page's version 6.8.0-139.139 is the generic-kernel source; the azure kernel's own tools package exists per Launchpad). Not an observation; versions are as of the access date.

---

### S4-21 — Ubuntu's `perf_event_paranoid` level 4 (`CONFIG_SECURITY_PERF_EVENTS_RESTRICT`)

**Citation.** (a) Ben Hutchings / Canonical, patch "UBUNTU: SAUCE: security, perf: Allow further restriction of perf_event_open", as re-posted verbatim to the ALT Linux `devel-kernel` list by Vitaly Chikunov on 2022-06-02 (with Canonical sign-offs preserved: "Signed-off-by: Tim Gardner <tim.gardner@canonical.com>", "Signed-off-by: Seth Forshee <seth.forshee@canonical.com>"); (b) Launchpad bug #2131046 "CAP_PERFMON insufficient to get perf data" (linux package, Ubuntu). The Ubuntu tree itself (git.launchpad.net) returned 403, so (a) is a mirror copy of the patch text, marked as such, and (b) is Canonical's own bug tracker describing the same level 4.

**Copy read.** https://lore.altlinux.org/devel-kernel/Yp4PuQTPUQt+7A9c@asheplyakov-rocket/T/ (SHA-256 `2b08af92c7776fe008efd86069001fa660d220a644e40352b2e8b12975aab983`); https://bugs.launchpad.net/ubuntu/+source/linux/+bug/2131046 (SHA-256 `fb554af8f20bc964ca015f40d68ec8edc432f447ee839b5c4e541c8bd5890c22`); https://lwn.net/Articles/696216/ (SHA-256 `0b771cf893371976b0d881d9ae266d2d197a2e94995c28fe7050b17c20d974ae`, background only, not quoted); fetched 2026-09-16; `sources/S4-21/`.

**Passages.**

- `altlinux-ubuntu-sauce-perf-restrict.txt:15–18`: "When kernel.perf_event_open is set to 3 (or greater), disallow all access to performance events by users without CAP_SYS_ADMIN." / "Add a Kconfig symbol CONFIG_SECURITY_PERF_EVENTS_RESTRICT that makes this value the default."
- `altlinux-ubuntu-sauce-perf-restrict.txt:42–46` (include/linux/perf_event.h hunk): "+#define PERF_SECURITY_MAX 4" / "+static inline bool perf_paranoid_any(void)" / "+{" / "+ return sysctl_perf_event_paranoid >= PERF_SECURITY_MAX;"
- `altlinux-ubuntu-sauce-perf-restrict.txt:57–64` (kernel/events/core.c hunk): " * 2 - disallow kernel profiling for unpriv" / "+ * 4 - disallow all unpriv perf event use" / " */" / "+#ifdef CONFIG_SECURITY_PERF_EVENTS_RESTRICT" / "+int sysctl_perf_event_paranoid __read_mostly = PERF_SECURITY_MAX;" / "+#else" / " int sysctl_perf_event_paranoid __read_mostly = 2;" / "+#endif"; `:70–71`: "+ if (perf_paranoid_any() && !capable(CAP_SYS_ADMIN))" / "+ return -EACCES;"
- `altlinux-ubuntu-sauce-perf-restrict.txt:82–91` (security/Kconfig hunk): "+config SECURITY_PERF_EVENTS_RESTRICT" / "+ bool "Restrict unprivileged use of performance events"" / "+ depends on PERF_EVENTS" / "+ default y" / "+ help" / "+ If you say Y here, the kernel.perf_event_paranoid sysctl" / "+ will be set to 3 by default, and no unprivileged use of the" / "+ perf_event_open syscall will be permitted unless it is" / "+ changed."
- `lp-bug-2131046.txt:48–49`: "The Ubuntu-specific perf_event_paranoid level 4 introduces an additional capability check that requires CAP_SYS_ADMIN to access perf events."; `:149–150` (test output): "[*] Current perf_event_paranoid level: 4." / "[*] This is a custom Ubuntu paranoid level."; `:178–179`: "Ubuntu carries a patch that introduces a new security level for perf events: perf_event_paranoid=4" / "This patch limits calling the perf open syscall to processes with CAP_SYS_ADMIN. This patch is from ~2016."

**Coverage (T8).** Covers the root requirement for perf on the runner: with `CONFIG_SECURITY_PERF_EVENTS_RESTRICT=y` in the runner's kernel config (S4-04 `:7512`), the default `kernel.perf_event_paranoid` is `PERF_SECURITY_MAX` = 4, at which `perf_event_open` returns `EACCES` without `CAP_SYS_ADMIN`; so every `perf` invocation in the given tooling needs `sudo` (as the GUI campaign already does with `sudo perf sched record`) or a `sysctl` lowering the level (as in the issue bodies of S4-22). Not an observation of the runner; the patch text is a mirror copy and the Kconfig help text says "3" where the code says `PERF_SECURITY_MAX` (4) — the inconsistency is in the source, reproduced verbatim.

---

### S4-22 — actions/runner-images issues reached through the GitHub MCP search API: perf on hosted runners; "Hosted Compute Agent"; `Runner.Listener` / `Runner.Worker` process names

**Citation.** Issue reports in github.com/actions/runner-images: #11789 (2025-03-13, "`perf stat` does not work on Linux runners (even ARM ones)"), #14091 (2025-03-13, "Linux Perf tool does not work as expected in Linux ARM runners"), #12545 (2025-07-08, "[macOS] macos-15 (x86) runner is excruciatingly slow"), #13264 (2025-11-05, "Xcode 26.0.1 / 26.1 RC hanging on both `macos-15-arm64` and `macos-26-xlarge`"), #11934 (2025-04-03, inconsistent execution times). User-authored reports, not GitHub statements.

**Copy read.** github.com HTML and api.github.com returned 403 (search-log rows 1, 10); the issue bodies were obtained through the GitHub MCP connector's `search_issues` tool (rows 8–9) and the quoted portions saved verbatim in `sources/S4-22/github-mcp-search_issues-runner-images.txt` (SHA-256 `8300aee06961cc259b80e304c0a6aea0c37b48a82a2766ba5de9e6508377b594`); the file states which fields were saved. Comments were not retrievable.

**Passages** (from the saved file; each is the issue body text as returned by the API).

- #11789 body, section "Image version and build link": "Current runner version: '2.322.0'" / "Operating System" / "Ubuntu" / "24.04.2" / "LTS" / "Runner Image" / "Image: ubuntu-24.04" / "Version: 20250309.1.0"; section "Repro steps": "- name: Install perf" / "run: |" / "sudo apt-get update && sudo apt-get install linux-tools-common \" / "- name: Enable perf event paranoid flag" / "run: sudo sysctl kernel.perf_event_paranoid=1" / "- name: Set Kernel KPTR  Restriction" / "run: sudo sysctl kernel.kptr_restrict=0" / "- name: Run perf" / "run: sudo perf stat --timeout 10000 -ae power/energy-cores/,power/energy-pkg/,power/energy-psys/"; the failure: "Cannot find PMU `power'. Missing kernel support?".
- #14091 body: "In Linux ARM based runners, the [perf record](...) command does not collect any samples. I have set the `kernel.perf_event_paranoid=1` and `kernel.kptr_restrict=0`. Upon running the command: `sudo perf record -g -e cycles -a -o perf.data sleep 5` it collects no samples in case of Linux ARM runners. The same command works just fine in Linux x64 runners."
- #12545 body, section "Image version and build link": "Current runner version: '2.325.0'" / "Runner Image Provisioner" / "Hosted Compute Agent" / "Version: 20250703.357" / "Commit: 07daf62238a21140d93e045a38f3784d75c509e1" / "Build Date: 2025-07-03T14:39:09Z".
- #13264 body, a `ps` listing captured on a macOS hosted runner: "runner            7015  19.0  0.5 436984176  67840   ??  S<    9:48PM   0:17.66 /Users/runner/actions-runner/cached/bin/Runner.Worker spawnclient 143 146" / "runner            7012   1.2  0.5 436714080  69520   ??  S<    9:48PM   0:03.00 /Users/runner/actions-runner/cached/bin/Runner.Listener run".

**Coverage (T8).** Covers, as user reports: that on `ubuntu-24.04` x64 hosted runners `sudo sysctl kernel.perf_event_paranoid=1` is accepted and `sudo perf record -a` and `perf stat` run (software/CPU events; the `power/` RAPL PMU is absent in the VM); that the job log's provisioner block names a "Hosted Compute Agent" as a component distinct from the runner application ("Current runner version"); and that the runner application runs as two processes, `Runner.Listener run` and `Runner.Worker spawnclient`, both under the `runner` user (a macOS listing; the Linux layout is the same application per S4-03). Each is one observation by one user on one run; machine, subject and window are only partly named (image version and runner version, no CPU model, no build). Not a measurement of a build.

---

### What a pinned single-core runner can observe of a build under the given tooling (synthesis)

Written by the reader; every claim points at a quoted passage above.

1. **The platform.** `ubuntu-latest` on a public repository is a fresh 4-vCPU / 16 GB / 14 GB-SSD Azure VM with passwordless sudo (S4-01 `:277–289, :378, :382`), running image 20260907.300.1 with kernel `6.17.0-1022-azure` (S4-02 `:8–12`), whose exact configuration is in hand (S4-04): `CONFIG_TASKSTATS`, `TASK_DELAY_ACCT`, `TASK_IO_ACCOUNTING`, `BSD_PROCESS_ACCT(_V3)`, `PSI` (on by default), `SCHEDSTATS`, `FTRACE`, `BPF_SYSCALL`/`BPF_EVENTS`, `PROC_EVENTS`, `CPUSETS`, `CGROUP_CPUACCT`, `HZ=1000` are all `=y`. Every instrument's kernel-config requirement is therefore met; none needs a different kernel.

2. **Root and runtime switches.** All instruments except `make --trace` and a `/proc` sampler need root: taskstats/delay accounting needs `kernel.task_delayacct=1` (or the `delayacct` boot option) and "only tasks started after enabling it will have delayacct information" (S4-05 `delay-accounting.rst:77–85`; S4-17 `:1243–1249`); BSD accounting needs `CAP_SYS_PACCT` (S4-06 `acct.2.txt:134–136`); BPF tools need `CAP_SYS_ADMIN` (S4-11 `exitsnoop_example.txt:3–5`); forkstat needs root (S4-12 `forkstat.8:32–34`); perf needs sudo because the Ubuntu kernel is built with `CONFIG_SECURITY_PERF_EVENTS_RESTRICT=y` (S4-04 `:7512`) which sets the default `perf_event_paranoid` to 4 and makes `perf_event_open` fail without `CAP_SYS_ADMIN` (S4-21), and a job may lower it with `sudo sysctl` (S4-22 #11789). Boot-time isolation (`isolcpus=`, `nohz_full=`) is a cmdline change and so unavailable (S4-17 `:2618–2646, :4264–4268`).

3. **CPU time at exit, for every process.** Two kernel-side exit records exist that need no polling: taskstats (`ac_utime`, `ac_stime` in µs, `ac_etime` in µs, `cpu_run_real_total` in ns, `cpu_delay_total` in ns, delivered for every exiting task on a registered cpumask — which can be exactly the pinned CPU — and summed per thread group at the last thread's exit; S4-05 `taskstats.rst:35–45, :83–88`; `taskstats-struct.rst:82–88, :112–116, :130–136`) and BSD accounting (`ac_utime`/`ac_stime`/`ac_etime` in clock ticks, `comp_t`-encoded; S4-06 `acct.5.txt:121–129`). The `wait4` rusage through a wrapper shell only gives totals for the wrapped child plus its waited-for descendants in seconds+µs (S4-07 `getrusage.2.txt:88–94, :129–137`), i.e. one aggregate for `make`, not per compiler.

4. **Lifetime.** Available from taskstats (`ac_etime`, µs) and BSD accounting (`ac_etime`), from BPF exit tracing (`exitsnoop` AGE from `task->start_time` to `bpf_ktime_get_ns()`, printed at 0.01 s; S4-11 `exitsnoop.py:106–107`, `exitsnoop_example.txt:34–37`), and from forkstat's exit "Duration", which is user-space arrival-time arithmetic and "unknown" when the start event was missed (S4-12 `forkstat.c:1690–1700`).

5. **Time blocked on I/O.** Only delay accounting gives it per process: `blkio_delay_total` (ns, synchronous block I/O, "does not account for delays in I/O submission"; S4-05 `taskstats-struct.rst:120–124`), and its tick-granular twin `delayacct_blkio_ticks` in `/proc/<pid>/stat` field 42 (S4-08 `proc_pid_stat.5.txt:328–330`). BSD accounting's I/O fields are unused (S4-06 `acct.5.txt:150–160`; `acct.c` never sets them); rusage gives block-operation counts, not time (S4-07 `getrusage.2.txt:166–169`); `strace -f -c -w` gives syscall wall time but "only aggregate totals for all traced processes" (S4-10 `:976–983, :1062–1066`); PSI gives a cgroup-wide share of time stalled, not per process (S4-14 `psi.rst:45–49`).

6. **Per-schedule run/wait.** `perf sched record` + `timehist` gives wait time, scheduling delay and run time per sched-in at µs resolution, with `-w` wakeups, `-C` for the pinned CPU and `--state` (S4-09 `perf-sched.txt:65–82, :159–161, :189–191, :212–213`); it captures processes of any lifetime that ran on that CPU. The ring buffer can drop ("LOST") events and `-m` sizes it (S4-09 `perf-record.txt:281–285, :822–824`); no document quantifies volume or overhead for one CPU, so that remains to be measured.

7. **What the pin does to each instrument.** `taskset` affinity is inherited across fork and exec (S4-16 `sched_setaffinity.2.txt:193–194`), so the whole build stays on the measured CPU and `nproc` inside it returns 1 (S4-16 `gnulib nproc.c:239–261`; `nproc.1.txt:75–79`) — the given workflow's explicit `-j8` is unaffected, and make applies no load limit unless `-l` is given (S4-13 `:4439`). A `/proc` sampler on another CPU still misses any process that starts and exits between two polls; the primary texts motivate exit-time delivery precisely because lifetime polling is incomplete (S4-05 `taskstats.rst:11`, `delay-accounting.rst:33–36`), but no document quantifies how time-sharing on one CPU changes that censoring. forkstat and taskstats both document loss under a high exit rate (ENOBUFS; S4-12 `forkstat.8:32–34`; S4-05 `taskstats.rst:160–181`), and taskstats' remedy is a larger receive buffer and one listener per CPU pinned to that CPU.

8. **What shares the pinned CPU.** GitHub's runner application runs as `Runner.Listener` and `Runner.Worker` under the `runner` user, and the provisioner is a separate "Hosted Compute Agent" (S4-22 #13264, #12545); the image also runs a Docker server (S4-02 `:78`). The job's own user may `taskset -p` its own processes, and with sudo (`CAP_SYS_NICE`) any other user's, but not kernel per-CPU threads (S4-16 `taskset.1.txt:86–87, :162–165`); a root-owned service can be confined with `systemd-run --scope -p AllowedCPUs=` or `systemctl set-property` (S4-15). Whether the hosted-compute agent is a movable process or a VM-level component is not documented anywhere found.

9. **Hardware, page cache, disk.** GitHub documents only the shape (4 vCPU, 16 GB, 14 GB "SSD") and not the CPU model; one vendor's 30-day sample shows at least two Xeon models on the same label with a 26 % spread in single-thread score (S4-19 `:165–172, :222–229`), so the CPU model must be recorded per run (the given `runner_spec.py` does). `vm.drop_caches` is the documented page-cache control (S4-17 `sysctl-vm.rst:245–256`); the disk's rotational flag is readable from sysfs (S4-18 `sysfs-block:664–669`) and Azure's temporary disk is `/dev/disk/azure/resource` (S4-18 `:106`).

10. **What it cannot observe.** Nothing in these sources gives desktop-class hardware, a user's own `-j` choice, an interactive session around the build, or parallel execution itself — the pin serialises the build on one CPU by construction (`pin.sh`, quoted in input.md), and the platform is a hypervisor VM with a virtualisation-aware kernel (`CONFIG_HYPERV=y`, S4-04 `:6482`) whose `cpu_run_real_total` "will adjust for cpu time stolen from the kernel in involuntary waits due to virtualization" on some architectures (S4-05 `taskstats-struct.rst:130–136`).

## 3. Not found

T8 sub-questions for which no candidate was found, with the searches that established it:

- **Quantified overhead or data volume of `perf sched record` on one CPU, and of `strace -f -c`.** perf-sched.txt, perf-record.txt and strace(1) (search-log rows 15–16) document the mechanisms and the loss mode but give no figures; no web search was spent on third-party overhead measurements because they would not be primary for this runner.
- **Whether a `/proc` sampler's censoring of short-lived processes changes when the observed processes are time-shared on one CPU.** taskstats.rst, delay-accounting.rst, acct(2) (row 15–16) give the rationale for exit-time records but no quantification; grep of proc.rst for `schedstat`/`sched` found nothing relevant (row 28). This remains something only the measurement itself can answer.
- **forkstat's event-loss rate under load.** forkstat.8/README/forkstat.c (row 18) say only "may miss events if the system is overly busy" and print ENOBUFS lines; no figure.
- **The `CAP_NET_ADMIN` requirement for a taskstats listener.** Not stated in taskstats.rst, delay-accounting.rst or getdelays.c at v6.17 (row 15; grep for `CAP_NET_ADMIN` in `sources/S4-05/` found no match); the requirement, if any, lives in `kernel/taskstats.c`, which was not fetched.
- **Which daemons run on the `ubuntu-latest` image (containerd, snapd, walinuxagent) and whether the "Hosted Compute Agent" is a movable process.** Ubuntu2404-Readme.md lists Docker Server but none of those names (row 28); actions/runner docs (row 4) do not describe hosted-runner agents; WebSearch (row 12) returned only secondary blog posts; the only primary mention of "Hosted Compute Agent" is a job-log excerpt in an issue body (S4-22).
- **The runner VM's Azure size/series and the disk tier behind "SSD".** GitHub docs (row 3) give only the shape; learn.microsoft.com (row 22) describes disk roles generically.
- **The running kernel's actual `kernel.perf_event_paranoid`, `kernel.task_delayacct` and `kernel.sched_schedstats` values.** Defaults are established (S4-17, S4-21) but no source reports the values on a live runner; the issue bodies (S4-22) show users setting `perf_event_paranoid=1` with sudo, not the pre-existing value.
- **The `_SC_CLK_TCK` (USER_HZ) value on the runner.** proc_pid_stat(5) and acct(5) say "divide by sysconf(_SC_CLK_TCK)"; `CONFIG_HZ=1000` (S4-04) is the scheduler tick, and no fetched document states the user-visible tick.
- **GitHub's own statement of CPU model variance or of dedicated vs shared vCPUs.** docs.github.com (row 3) and runner-images issues via MCP search (rows 7–9) contain no such statement; S4-19 is a vendor sample only.
- **A commit id for any file fetched from a `main`/`master` raw URL** (runner-images readme, actions/runner docs, bcc, bpftrace, forkstat, coreutils, gnulib, make.texi): api.github.com and MCP `list_commits` were denied (rows 1, 6); copies are pinned by SHA-256 and internal version strings instead.
