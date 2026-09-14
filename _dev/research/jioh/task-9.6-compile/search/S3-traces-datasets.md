# S3 — public traces and datasets (T1, T2, T4, T5, T6, T7)

Reader class S3. Access date for everything below: 2026-09-14. Source copies under `sources/S3-*/`, each folder carrying a `SHA256SUMS.txt` (the SHA-256 values quoted here are copied from those files). T3 and T8 are recorded as "does not cover" for every candidate; no dataset happened to cover them.

Every number in this record that is not a verbatim quote is a computation and says which file and what computation. Where a page was fetched as HTML, line locators refer to the tag-stripped text of the saved copy (produced by the `h2t.py` helper quoted under §1.0), unless a `file:line` of a plain-text file is given. Partial, sampled or single-excerpt data is labelled as such.

## 1. Search log

### 1.0 Tooling note

All fetches were `curl -sS -L` through the preconfigured HTTPS proxy (TLS verification on). HTML pages were converted to text for locators with this script (`h2t.py`):

```python
import sys,re,html
s=open(sys.argv[1],encoding='utf-8',errors='replace').read()
s=re.sub(r'(?is)<(script|style).*?</\1>','',s)
s=re.sub(r'(?i)<br\s*/?>','\n',s); s=re.sub(r'(?i)</(p|div|li|tr|h\d|pre)>','\n',s)
s=re.sub(r'<[^>]+>','',s); s=html.unescape(s)
s=re.sub(r'\n\s*\n+','\n',s)
print(s)
```

Reachability established on 2026-09-14 by the fetches below: bugs.launchpad.net 200, bugzilla.redhat.com 200, bugs.debian.org 200, buildd.debian.org 200, kojipkgs.fedoraproject.org 200, git.yoctoproject.org 200 (cgit HTML and `git clone`; the `/poky/plain/...` raw paths 404), tests.reproducible-builds.org 200, opendata.blender.org 200, llvm-compile-time-tracker.com 200, forums.developer.nvidia.com 200 (Discourse `.json`), phoronix.com 200 for page 1 of articles and 403 for `/review/<slug>/2` and `scan.php` URLs, dashboard.kernelci.org 403, chromium-build-stats.appspot.com 200 but a Google sign-in page, forums.gentoo.org 200 but a login page. github.com HTML and api.github.com were not attempted (known 403); GitHub content was reached by `git clone --depth 1`, raw.githubusercontent.com, and the GitHub MCP code-search tool (search works; `get_file_contents` refused every repository outside the session's own: "Access denied: repository ... is not configured for this session").

### 1.1 Queries

| # | date | engine / venue | query (exact) | followed | dead ends |
|---|------|----------------|---------------|----------|-----------|
| 1 | 2026-09-14 | WebSearch | `yocto buildstats sample output "utime" "stime" per-task rusage buildstats.log example` | wiki.yoctoproject.org TipsAndTricks/InvestigatingBuildTime (200) → S3-05; `git clone` openembedded/openembedded-core for `buildstats.bbclass` → S3-05 | git.yoctoproject.org/poky/plain/scripts/contrib/bb-perf/buildstats.sh, /meta/classes/buildstats.bbclass, /scripts/buildstats-diff: HTTP 404 |
| 2 | 2026-09-14 | WebSearch | `llvm-compile-time-tracker per-file instructions "kimwitu++" "sqlite3" data csv` | `git clone` nikic/llvm-compile-time-tracker; llvm-compile-time-tracker.com/ (200), /about.php (200) → S3-09 | green.lab.llvm.org not followed (Jenkins UI) |
| 3 | 2026-09-14 | WebSearch | `".ninja_log" file published chromium OR llvm "# ninja log v5" example start end ms` | chromium.googlesource.com depot_tools `post_build_ninja_summary.py?format=TEXT` (200) → S3-13 | depot_tools `ninjalog.README.md?format=TEXT` 404; chromium-build-stats.appspot.com/ and /ninja_log/ 200 but body is a Google sign-in page (copy `S3-x-dead-ends/chromium-build-stats-signin.html`) |
| 4 | 2026-09-14 | WebSearch | `"execsnoop" OR "exitsnoop" output during "make -j" kernel build cc1 collect2 processes trace` | none usable; `git clone` iovisor/bcc and brendangregg/perf-tools and grepped `tools/execsnoop_example.txt`, `tools/exitsnoop_example.txt`, `examples/execsnoop_example.txt` for `cc1|gcc|collect2|make` → no build example (exitsnoop's example is `sleep`/`bash` loops) | — |
| 5 | 2026-09-14 | WebSearch | `phoronix "build-linux-kernel" defconfig "time to compile" Ryzen threads scaling results 2025` | phoronix.com/news/Linux-16-Seconds-AMD-EPYC-2P (200) → S3-10 | openbenchmarking.org not attempted (known 403) |
| 6 | 2026-09-14 | WebSearch | `"perf sched timehist" output "cc1" OR "make" kernel compile example wait time sch delay` | lkml.iu.edu/hypermail/linux/kernel/1611.2/05655.html (200) → S3-02; brendangregg.com/blog/2017-03-16/perf-sched.html (200) → S3-01 | man7.org not followed (S2 domain) |
| 7 | 2026-09-14 | WebSearch | `DKMS "make -j" autoinstall duration nvidia module build time log "dkms.log" bug report` | forums.developer.nvidia.com/t/…/206793 (HTML 200 but JS shell; `/t/206793.json` 200) → S3-07 | Linux Mint forum hits not followed |
| 8 | 2026-09-14 | WebSearch | `Debian buildd build log "Build needed" time "parallel=" sbuild build duration dataset` | buildd.debian.org/status/logs.php?pkg=linux&arch=amd64 (200) and fetch.php raw logs → S3-03 | — |
| 9 | 2026-09-14 | WebSearch | `Gentoo emerge.log dataset published qlop "genlop" build times package compile durations github raw emerge.log` | tools only (emlop, genlop, qlop); no dataset | — |
| 10 | 2026-09-14 | WebSearch | `Harchol-Balter Downey process lifetime data trace Unix "process lifetimes" dataset archive download` | www.cs.cmu.edu/~harchol/ (200): text grep for `trace|dataset|lifetime` hits only the biography line "Known for the discovery of Pareto heavy-tailed distribution of UNIX process CPU lifetimes." — no data link (copy `S3-x-dead-ends/harchol-balter-homepage.html`) | papers only (class S1) |
| 11 | 2026-09-14 | WebSearch | `"-ftime-trace" OR ClangBuildAnalyzer results published real project "Total frontend" "Total backend" full report github` | `git clone` aras-p/ClangBuildAnalyzer → S3-14 | — |
| 12 | 2026-09-14 | WebSearch | `Mozilla "build_resources.json" OR "mach resource-usage" firefox build CPU utilization per-tier data` | bugzilla.mozilla.org 1242017 and firefox-source-docs pages seen in results; no published data file exists in the results; not followed | — |
| 13 | 2026-09-14 | WebSearch | `Phoronix x264 OR ffmpeg OR HandBrake thread scaling CPU cores utilization encode benchmark 2025 2026` | forum threads only; nothing with measured utilisation | openbenchmarking.org/test/pts/x264 not attempted (known 403) |
| 14 | 2026-09-14 | WebSearch | `yocto autobuilder published buildstats tarball "buildstats" performance tests results download` | git.yoctoproject.org/yocto-buildstats/ (200) → cloned one branch → S3-05; wiki TipsAndTricks/MiningPerformanceData (200); docs.yoctoproject.org/dev/test-manual/test-process.html (200) | autobuilder.yocto.io/pub/non-release/ 404 (curl); git.yoctoproject.org/yp-qa-build-perf-data/ 404 |
| 15 | 2026-09-14 | curl probes | (URL list) | bugs.launchpad.net/ubuntu/+source/dkms 200; bugzilla.redhat.com/show_bug.cgi?id=2000000 200; bugs.debian.org/cgi-bin/bugreport.cgi?bug=1000000 200; kernelci.org 200; lwn.net/Articles/706404 200; tests.reproducible-builds.org/debian/index_bugs.html 200 | dashboard.kernelci.org 403 (copy `S3-x-dead-ends/kernelci-dashboard-403.html`); tests.reproducible-builds.org/debian/stats.html 404 |
| 16 | 2026-09-14 | WebSearch | `Stack Overflow developer survey OR poll "make -j" how many jobs do you use nproc+1 "2*nproc" reddit poll results` | nothing: `nproc` how-to pages, a python/devguide PR, a cki kernel-ark MR | no survey or poll exists in the results |
| 17 | 2026-09-14 | WebSearch | `Phoronix ClamAV OR "clamscan" benchmark threads CPU Linux "pts/clamav" results` | nothing quantitative (how-to pages) | — |
| 18 | 2026-09-14 | WebSearch | `sched-ext scx "kernel compile" OR "make -j" benchmark results scx_bpfland scx_lavd "kernel build" time comparison` | `git clone` sched-ext/scx and grepped `*.md` for `make -j|kernel build|kernel compile` → `DEVELOPER_GUIDE.md:242`, `scheds/rust/scx_rustland/README.md:47` → S3-12 | scx issue #998 (github HTML, not fetched) |
| 19 | 2026-09-14 | WebSearch | `launchpad bug dkms "make -j" "nproc" autoinstall took minutes "dkms autoinstall" boot slow nvidia log attachment` | bugs.launchpad.net/bugs/2141316 (200) and its attachments (200) → S3-06 | bugs.launchpad.net/bugs/2115002 (200): only an `nvidia-bug-report.log.gz` attachment, no `make.log` |
| 20 | 2026-09-14 | curl | `https://bugs.launchpad.net/ubuntu/+source/dkms/+bugs?field.searchtext=make.log` | 200; 4 old bugs (#1428568, #1578455, #1689390, #1871162), none with timing; not followed | — |
| 21 | 2026-09-14 | curl | `https://buildd.debian.org/status/fetch.php?pkg=linux&arch=amd64&ver=7.1.13-1&stamp=…&raw=1` and the same for `hello` 2.12.3-1 | 200 (214,411,815 B) and 200 (210,273 B) → S3-03 | — |
| 22 | 2026-09-14 | curl | `https://kojipkgs.fedoraproject.org/packages/kernel/6.17.0/0.rc1.17.fc43/data/logs/x86_64/{root,build,hw_info,state,mock_output}.log` | all 200 → S3-04 | koji.fedoraproject.org web search page not needed |
| 23 | 2026-09-14 | WebSearch (allowed_domains phoronix.com) | `site:phoronix.com kernel compile "-j" cores scaling "Timed Linux Kernel Compilation" thread count comparison` | /review/intel-scalability-optimizations page 1 (200) → S3-10 | pages /2 and /3: HTTP 403 (copy `S3-x-dead-ends/phoronix-intel-scalability-p2-403.html`); WebFetch of /2 also 403; `scan.php?page=news_item&px=MTAyNjU` 403 |
| 24 | 2026-09-14 | WebSearch (allowed_domains phoronix.com) | `Phoronix "Linux 7.4" kernel builds faster incremental builds 36% article` | /news/Faster-Kernel-Builds-AI-v2 (200), /news/AI-To-Faster-Linux-Kernel-Comp (200) → S3-10 | — |
| 25 | 2026-09-14 | GitHub code search (MCP) | `"# ninja log v5" filename:.ninja_log` | 54,656 hits; fetched via raw.githubusercontent.com: hoholee12/rpcs3-custom `llvm_build/.ninja_log`, XeroMz69/Bebas `.ninja_log`, thead-yocto-mirror/gpu_bxm_4_64-kernel `tools/llvm/llvm.riscv64/.ninja_log` → S3-08 | hlavacs/ViennaGameJobSystem (3 lines) and OneRaynyDay/autodiff (11 lines) fetched and discarded as trivial |
| 26 | 2026-09-14 | GitHub code search (MCP) | `filename:.ninja_log "lib/Transforms"` | 6 hits, all LLVM builds; the three above | — |
| 27 | 2026-09-14 | GitHub code search (MCP) | `"Compiling" ">>>" filename:emerge.log` | 1 hit: cklaucke/genloppy `tests/parser/good_emerge.log` (raw 200, 2,109 B) — a 2017 two-package parser test fixture, not a dataset (copy in `S3-x-dead-ends/`) | — |
| 28 | 2026-09-14 | GitHub code search (MCP) | `"perf sched timehist" cc1 "sch delay" extension:txt` | 4 hits, all copies of Gregg's article or of the BPF book; not followed | — |
| 29 | 2026-09-14 | GitHub code search (MCP) | `execsnoop cc1 collect2 "as -" extension:txt` | 1 irrelevant hit | — |
| 30 | 2026-09-14 | GitHub MCP `get_file_contents` | nikic/llvm-compile-time-data `/`; cklaucke/genloppy `tests/parser/good_emerge.log` | — | "Access denied: repository … is not configured for this session" for both; replaced by git/raw fetches |
| 31 | 2026-09-14 | git | `git clone --depth 1 https://github.com/nikic/llvm-compile-time-data` | aborted: the clone reached 29 GB and filled the disk; re-done as `git clone --depth 1 --filter=blob:none --no-checkout` (21 MB) and one experiment's two blobs fetched with `git show` → S3-09 | — |
| 32 | 2026-09-14 | WebSearch | `Gentoo forums poll MAKEOPTS "-j" what value do you use nproc cores "MAKEOPTS" poll results users` | forums.gentoo.org/viewtopic-t-1147777-start-0.html: HTTP 200 but the body is the login page (WebFetch: "displays only the Gentoo Forums login screen"); copy `S3-x-dead-ends/gentoo-forum-1147777-login.html` | Gentoo wiki MAKEOPTS not fetched (S2 domain) |
| 33 | 2026-09-14 | WebSearch | `"tracker-miner-fs" OR "tracker3" full reindex time minutes CPU usage benchmark OR "updatedb" plocate "took" seconds files indexed measurement` | only bug reports (gitlab.gnome.org tracker-miners #228, LP #2025523) with unmeasured "100% CPU for hours" complaints; not followed (no machine, no duration measured) | — |
| 34 | 2026-09-14 | WebSearch | `clamscan benchmark "--multiscan" OR clamdscan threads scan time CPU cores measured seconds GB files` | man pages and how-tos only | — |
| 35 | 2026-09-14 | WebSearch | `PyTorch CPU training utilization "torch.get_num_threads" all cores 100% utilization measured benchmark desktop laptop ResNet CPU epoch time` | tutorials only | — |
| 36 | 2026-09-14 | WebSearch | `cachyos-benchmarker OR mini-benchmarker results "kernel" build time scx scheduler comparison seconds table` | `git clone` CachyOS/cachyos-benchmarker → S3-12; gist.githubusercontent.com/galpt/…/raw (200) → `git clone --branch benchmark-archives` galpt/testing-scx_flow (59 MB): no compile workload (`grep -rlE 'make -j|kernel compile'` over its logs/md = 0; README.md:70 mentions hackbench/spike metrics only) | phoronix.com/review/cachyos-bore page 1 200 (System76 Thelio Major named; no numbers on page 1), page 2 403 |
| 37 | 2026-09-14 | curl | `https://opendata.blender.org/`, `/snapshots/`, `/snapshots/opendata-2020-01-08-063356+0000.zip` | 200 / 200 / 200 (2,018,885 B) → S3-16 | `/benchmarks/query/?compute_type=CPU…` 200 but a JS shell |
| 38 | 2026-09-14 | curl | `https://tests.reproducible-builds.org/debian/history/linux.html`, `/debian/index_performance.html`, `/debian/index_nodes_health.html` | 200 / 200 / 200 → S3-15 | `/reproducible.json` 200 (104,678,435 B) downloaded but deleted unexamined when the disk filled; `/debian/nodes_health_check.html`, `/debian/index_nodes_info.html` 404 |
| 39 | 2026-09-14 | git | `git fetch --depth 1 --filter=blob:none origin refs/notes/buildstats/perf-debian12-vk/master/qemux86` on the yocto-buildstats clone | the notes ref arrived after ≈3.6 GB of objects; the note for the results commit `a4a792be` (8,614,927 B JSON) extracted → S3-05 | a second, duplicate fetch was killed at 7.1 GB |
| 40 | 2026-09-14 | curl | `https://kojipkgs.fedoraproject.org/packages/kernel/` and `/6.17.0/` listings | 200; picked `0.rc1.17.fc43` | — |

Not queried: Zenodo and HuggingFace dataset APIs (the topics are build traces, for which the searches above found the primary hosts directly); Google Dataset Search (no non-JS interface).

## 2. Candidates

### S3-01 — Brendan Gregg, "perf sched for Linux CPU scheduler analysis": one second of `perf sched record` on an 8-CPU VM running a kernel build

**Citation.** Brendan Gregg, *perf sched for Linux CPU scheduler analysis*, blog post dated 16 Mar 2017, https://www.brendangregg.com/blog/2017-03-16/perf-sched.html. Licence/terms: personal blog, no licence stated; quoted here under citation.

**Copy.** `sources/S3-01-gregg-perf-sched/perf-sched.html` (SHA-256 `37a80dd6662f1a669b36f0d3f45ea5af744aca012b646fd238e0670991e43bbe`), tag-stripped text `perf-sched.txt` (`ceeb435a43dff74a71ee0cefdbda723706b50c11ab62ede70253b5d5e08fd6c2`); accessed 2026-09-14. Line locators below are lines of `perf-sched.txt`.

**Passages.**

Lines 91–94:
> `# perf sched record -- sleep 1`
> `[ perf record: Woken up 1 times to write data ]`
> `[ perf record: Captured and wrote 1.886 MB perf.data (13502 samples) ]`
> That's 1.9 Mbytes for one second, including 13,502 samples. The size and rate will be relative to your workload and number of CPUs (this example is an 8 CPU server running a software build).

Lines 97–107 (`perf script --header`):
> `# captured on: Sun Feb 26 19:40:00 2017`
> `# hostname : bgregg-xenial`
> `# os release : 4.10-virtual`
> `# perf version : 4.10`
> `# arch : x86_64`
> `# nrcpus online : 8`
> `# nrcpus avail : 8`
> `# cpudesc : Intel(R) Xeon(R) CPU E5-2680 v2 @ 2.80GHz`
> `# cpuid : GenuineIntel,6,62,4`
> `# total memory : 15401700 kB`
> `# cmdline : /usr/bin/perf sched record -- sleep 1 `

Lines 134–151 (`perf sched latency`, the rows that name build processes; the table header is at lines 136):
> `  Task                  |   Runtime ms  | Switches | Average delay ms | Maximum delay ms | Maximum delay at       |`
> `  cat:(6)               |     12.002 ms |        6 | avg:   17.541 ms | max:   29.702 ms | max at: 991962.948070 s`
> `  ar:17043              |      3.191 ms |        1 | avg:   13.638 ms | max:   13.638 ms | max at: 991963.048070 s`
> `  rm:(10)               |     20.955 ms |       10 | avg:   11.212 ms | max:   19.598 ms | max at: 991963.404069 s`
> `  objdump:(6)           |     35.870 ms |        8 | avg:   10.969 ms | max:   16.509 ms | max at: 991963.424443 s`
> `  :17008:17008          |    462.213 ms |       50 | avg:   10.464 ms | max:   35.999 ms | max at: 991963.120069 s`
> `  grep:(7)              |     21.655 ms |       11 | avg:    9.465 ms | max:   24.502 ms | max at: 991963.464082 s`
> `  fixdep:(6)            |     81.066 ms |        8 | avg:    9.023 ms | max:   19.521 ms | max at: 991963.120068 s`
> `  mv:(10)               |     30.249 ms |       14 | avg:    8.380 ms | max:   21.688 ms | max at: 991963.200073 s`
> `  ld:(3)                |     14.353 ms |        6 | avg:    7.376 ms | max:   15.498 ms | max at: 991963.452070 s`
> `  recordmcount:(7)      |     14.629 ms |        9 | avg:    7.155 ms | max:   18.964 ms | max at: 991963.292100 s`
> `  svstat:17067          |      1.862 ms |        1 | avg:    6.142 ms | max:    6.142 ms | max at: 991963.280069 s`
> `  cc1:(21)              |   6013.457 ms |     1138 | avg:    5.305 ms | max:   44.001 ms | max at: 991963.436070 s`
> `  gcc:(18)              |     43.596 ms |       40 | avg:    3.905 ms | max:   26.994 ms | max at: 991963.380069 s`
> `  ps:17073              |     27.158 ms |        4 | avg:    3.751 ms | max:    8.000 ms | max at: 991963.332070 s`
> `...]`

Lines 153–159:
> To shed some light as to how this is instrumented and calculated, I'll show the events that led to the top event's "Maximum delay at" of 29.702 ms. Here are the raw events from perf sched script:
> `      sh 17028 [001] 991962.918368:   sched:sched_wakeup_new: comm=sh pid=17030 prio=120 target_cpu=002`
> `     cc1 16819 [002] 991962.948070:       sched:sched_switch: prev_comm=cc1 prev_pid=16819 prev_prio=120`
> `                                                            prev_state=R ==> next_comm=sh next_pid=17030 next_prio=120`
> The time from the wakeup (991962.918368, which is in seconds) to the context switch (991962.948070) is 29.702 ms. This process is listed as "sh" (shell) in the raw events, but execs "cat" soon after, so is shown as "cat" in the perf sched latency output.

Lines 174–176, 185–186 (`perf sched map`):
> `   G0      C0  K0      J0 *M0  B0   991962.882289 secs M0 => make:16637`
> `   G0      C0  K0      J0 *N0  B0   991962.883102 secs N0 => make:16545`
> `   G0     *O0  K0      J0  N0  B0   991962.883880 secs O0 => cc1:16819`
> This is an 8 CPU system, and you can see the 8 columns for each CPU starting from the left. …
> For example, the very last line shows that at 991962.886917 (seconds) CPU 4 context-switched to K0 (a "cc1" process, PID 16945).

Lines 209–231 (`perf sched timehist`, header and the cc1 rows):
> perf sched timehist was added in Linux 4.10, and shows the scheduler latency by event, including the time the task was waiting to be woken up (wait time) and the scheduler latency after wakeup to running (sch delay).
> `           time    cpu  task name                       wait time  sch delay   run time`
> `                        [tid/pid]                          (msec)     (msec)     (msec)`
> `  991962.880070 [0002]  cc1[16880]                          0.000      0.000      0.000`
> `  991962.880078 [0000]  cc1[16881]                          0.000      0.000      0.000`
> `  991962.880081 [0003]  cc1[16945]                          0.000      0.000      0.000`
> `  991962.881841 [0006]  cc1[16825]                          0.000      0.000      0.000`
> `  991963.885740 [0001]  :17008[17008]                      25.613      0.000      0.057`
> `  991963.886009 [0001]  sleep[16999]                     1000.104      0.006      0.269`
> `  991963.886018 [0005]  cc1[17083]                         19.998      0.000      9.948`

Lines 263–264 and 272:
> `  :17008 17008 [001] 991963.885740:       sched:sched_switch: prev_comm=cc1 prev_pid=17008 prev_prio=120`
> `                                                             prev_state=R ==> next_comm=sleep next_pid=16999 next_prio=120`
> When sleep finished, a waiting "cc1" process then executed.

**Computed (from the quoted `perf sched latency` rows, arithmetic only).** The `(N)` suffix is perf's count of distinct PIDs merged under one comm; within the one-second window 21 `cc1`, 18 `gcc`, 6 `fixdep`, 7 `recordmcount`, 3 `ld`, 6 `objdump`, 6 `cat`, 10 `rm`, 10 `mv`, 7 `grep` processes were seen. `cc1` runtime 6013.457 ms over 8 CPUs in a 1.0 s window = 75.2 % of CPU capacity; `cc1` mean run per switch = 6013.457 / 1138 = 5.28 ms; `gcc` driver runtime 43.596 ms = 0.7 % of the `cc1` runtime. `fixdep` and `recordmcount` are kbuild helpers, so the "software build" is a Linux kernel build (inference from process names, not stated by the author).

**Coverage.**
- T1 — covers, partially: object = processes visible to the scheduler in a 1 s window; unit = per-comm runtime, switch count, mean/max wakeup delay; scope = whole system; population = one kernel build on one VM. Distinct PIDs per comm are quoted (`cc1:(21)`, `gcc:(18)`, `fixdep:(6)`, `recordmcount:(7)`, `ld:(3)`, `sh`→`cat`, `make:16637`/`make:16545`). No per-process lifetimes (window is 1 s).
- T2 — covers, partially: per-comm CPU runtime, context-switch counts and per-switch run time (cc1 5.305 ms average delay, 44.001 ms max delay; individual timehist rows give wait time 19.998 ms / run time 9.948 ms for `cc1[17083]`). No I/O-blocking split, no cold-cache case.
- T4 — does not cover (the `-j` is not stated).
- T6 — covers weakly: it is a kernel build used as the example workload for a scheduler analysis tool; machine named.
- T3, T5, T7, T8 — does not cover.

**One observation?** Yes: one 1-second `perf sched record` on `bgregg-xenial` (8 vCPU Xeon E5-2680 v2 VM, kernel 4.10-virtual, 15.4 GB RAM), 2017-02-26 19:40:00, during a build whose `-j` and tree are not stated. Machine and window named; project inferred.

---

### S3-02 — `perf sched timehist` introduction patch: the documented example output shows `gcc` processes

**Citation.** David Ahern (author), Arnaldo Carvalho de Melo (sender), "[PATCH 14/18] perf sched timehist: Introduce timehist command", LKML, Wed Nov 23 2016, archived at https://lkml.iu.edu/hypermail/linux/kernel/1611.2/05655.html (Link header in the patch: `http://lkml.kernel.org/r/20161116060634.28477-4-namhyung@xxxxxxxxxx`).

**Copy.** `sources/S3-02-perf-timehist-patch/lkml-1611.2-05655.html` (SHA-256 `1d1739ad3ac6e8fbdf400c7a8d4cf51a2497fbec3e92a132dbc7cce15d808051`), accessed 2026-09-14.

**Passages** (commit message, section "Example usage"):
> By default it shows the individual schedule events, including the wait time (time between sched-out and next sched-in events for the task), the task scheduling delay (time between wakeup and actually running) and run time for the task:
> `            time    cpu  task name             wait time  sch delay   run time`
> `                         [tid/pid]                (msec)     (msec)     (msec)`
> `    79371.874569 [0011]  gcc[31949]                0.014      0.000      1.148`
> `    79371.874591 [0010]  gcc[31951]                0.000      0.000      0.024`
> `    79371.874603 [0010]  migration/10[59]          3.350      0.004      0.011`
> `    79371.874604 [0011]  <idle>                    1.148      0.000      0.035`
> `    79371.874723 [0005]  <idle>                    0.016      0.000      1.383`
> `    79371.874746 [0005]  gcc[31949]                0.153      0.078      0.022`
> Times are in msec.usec.

**Coverage.** T2 — covers weakly: six real scheduler events of `gcc` processes (run times 1.148 ms, 0.024 ms, 0.022 ms; wait 0.153 ms; scheduling delay 0.078 ms) on a ≥12-CPU machine (CPU column `[0011]`); no machine, build or `-j` stated. T1, T4–T8 — does not cover. Not usable as a distribution; recorded because it is the canonical documented sample of the tool the S4 reader would use.

**One observation?** A six-line excerpt of one unnamed run; machine and window not named.

---

### S3-03 — Debian buildd logs: `linux` 7.1.13-1 amd64 (full kernel build under `parallel=6`) and `hello` 2.12.3-1 amd64

**Citation.** Debian Package Auto-Building, build logs for `linux` on amd64 and `hello` on amd64, https://buildd.debian.org/status/logs.php?pkg=linux&arch=amd64 and `…pkg=hello&arch=amd64`; raw logs `https://buildd.debian.org/status/fetch.php?pkg=linux&arch=amd64&ver=7.1.13-1&stamp=1788481014&raw=1` (stamp taken from the index page) and `…pkg=hello&arch=amd64&ver=2.12.3-1&stamp=1778749005&raw=1`. Terms: public build logs of the Debian project; the index page says "Pages written by Mehdi Dogguy".

**Copy.** `sources/S3-03-debian-buildd-logs/`: `linux_7.1.13-1_amd64.log` (214,411,815 B, 644,934 lines, SHA-256 `25b9841439e0b8525ce6ef7ff37fcc7ec7eba355823e23944cf0ec839ec0aa58`), `hello_2.12.3-1_amd64.log` (`6555bddf588faddc02bca59b3a64bb883b699162388a1f2f020799703a877d53`), index pages `logs.php_pkg=linux_arch=amd64.html` (`a372aed1f086b37fb52cb83b9e0057e6ed9d521c2a2dcf315e1182e7ad0d8d73`), `logs.php_pkg=hello_arch=amd64.html` (`1f9232b43346a418b064c03fd014084653c88a1c93694c2325caf162f7f77d7a`); accessed 2026-09-14.

**Passages.**

`linux_7.1.13-1_amd64.log:2`, `:5`, `:8-15`:
> `sbuild (Debian sbuild) 0.91.9~bpo13+1 (23 May 2026) on x86-conova-01.debian.org`
> `| linux 7.1.13-1 (amd64)                       Thu, 03 Sep 2026 21:35:10 +0000 |`
> `Package: linux` / `Version: 7.1.13-1` / `Source Version: 7.1.13-1` / `Distribution: sid` / `Machine Architecture: amd64` / `Host Architecture: amd64` / `Build Architecture: amd64` / `Build Type: any`

`:1623-1624`:
> `Kernel: Linux 6.12.107+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.107-1 (2026-08-29) amd64 (x86_64)`
> `Toolchain package versions: binutils_2.47-2 dpkg-dev_1.23.7 g++-16_16.2.0-2 gcc-16_16.2.0-2 libc6-dev_2.43-4 libstdc++-15-dev_15.3.0-3 libstdc++-16-dev_16.2.0-2 libstdc++6_16.2.0-2 linux-libc-dev_7.1.12-1`

`:1628`, `:2668`:
> `| Build                                        Thu, 03 Sep 2026 21:36:59 +0000 |`
> `DEB_BUILD_OPTIONS=parallel=6`

`:4918` (one of three flavour builds; the others are at `:262512` and `:333634`):
> `/usr/bin/make -f debian/rules.real build_binary ABINAME='7.1.13+deb14' ARCH='amd64' C_COMPILER='gcc-15' DESTDIR='/build/reproducible-path/linux-7.1.13/debian/linux-binary-unsigned-7.1.13+deb14-amd64' DH_OPTIONS='-plinux-binary-unsigned-7.1.13+deb14-amd64' FEATURESET='none' FLAVOUR='amd64' IMAGE_FILE='arch/x86/boot/bzImage' IMAGE_INSTALL_STEM='vmlinuz' INSTALLDOCS_LINK_DOC='linux-base-7.1.13+deb14-amd64' KCONFIG='debian/config/config debian/config/amd64/config' KCONFIG_OPTIONS=' -o "BUILD_SALT=\"7.1.13+deb14-amd64\""' KERNEL_ARCH='x86' LOCALVERSION='-amd64' LOCALVERSION_HEADERS='' LOCALVERSION_IMAGE='-amd64' PACKAGE_NAME='linux-binary-unsigned-7.1.13+deb14-amd64' SOURCEVERSION='7.1.13-1' SOURCE_BASENAME='linux' SOURCE_SUFFIX='' UPSTREAMVERSION='7.1'`

`:35354-35355` (one compile as logged with `KBUILD_VERBOSE=1`; the command line is truncated here after the `-Wp` option, the full line is 3.1 kB):
> `# CC [M]  net/sctp/sm_make_chunk.o`
> `   x86_64-linux-gnu-gcc-15 -Wp,-MMD,net/sctp/.sm_make_chunk.o.d -nostdinc …`

`:644902`, `:644914-644934`:
> `| Post Build                                   Fri, 04 Sep 2026 00:16:40 +0000 |`
> `| Summary                                      Fri, 04 Sep 2026 00:16:53 +0000 |`
> `Build Architecture: amd64` / `Build Type: any` / `Build-Space: 100835680` / `Build-Time: 9443` / `Distribution: sid` / `Host Architecture: amd64` / `Install-Time: 92` / `Job: linux_7.1.13-1` / `Machine Architecture: amd64` / `Package: linux` / `Package-Time: 9567` / `Source-Version: 7.1.13-1` / `Space: 100835680` / `Status: successful` / `Version: 7.1.13-1`
> `Finished at 2026-09-04T00:14:37Z`
> `Build needed 02:39:27, 100835680k disk space`

Index page `logs.php_pkg=linux_arch=amd64.html` (first rows of the table, text lines 12–37): columns `Version / Architecture / Result / Build date / Builder / Build time / Disk space`; rows `7.2.3-1~exp1 (experimental) amd64 Maybe-Successful 2026-09-05 07:24:01 x86-grnet-01 2h 52m 97.76 GB`, `7.2.2-1~exp1 … x86-ubc-01 2h 54m`, `7.2~rc7-1~exp1 … x86-conova-01 2h 42m`, `7.2~rc5-1~exp1 … x86-ubc-01 2h 55m`, `7.2~rc3-1~exp1 … x86-csail-01 2h 28m`, `7.1.13-1 (sid) … x86-conova-01 2h 39m 96.16 GB`, `7.1.12-1 … x86-ubc-01 2h 54m`, `7.1.10-1 … x86-csail-01 2h 42m`, `7.1.9-1 … x86-csail-01 2h 39m`, `7.1.8-2 … x86-conova-01 2h 37m`.

`hello_2.12.3-1_amd64.log:385`, `:463`, `:772`, `:2710`:
> `Kernel: Linux 6.12.86+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.86-1 (2026-05-08) amd64 (x86_64)`
> `DEB_BUILD_OPTIONS=parallel=6`
> `	make -j6`
> ` DEB_BUILD_OPTIONS="parallel=6"`

Index page for `hello`: `2.12.3-1 (sid) amd64 Maybe-Successful 2026-05-14 08:56:45 x86-ubc-01 28s 12.16 MB`.

**Computed (file `linux_7.1.13-1_amd64.log`, `grep -a` pipelines).**
- Flavours built in the one log: `grep -aoE "FLAVOUR='[^']*'" | sort | uniq -c` → `amd64` 16 lines, `cloud-amd64` 10, `rt-amd64` 10; `build_binary` invoked 3 times (lines 4918, 262512, 333634) — three full kernel configurations are compiled in the 2 h 39 m.
- Compiler invocations: lines matching `x86_64-linux-gnu-gcc-15 .* -c -o ` = 45,608; distinct `-c -o <object>` targets = 19,819 (`grep -aoE 'gcc-15 .* -c -o [^ ]+' | grep -aoE ' -c -o [^ ]+' | sort -u | wc -l`); of the compile lines, 342 compile a `.S` file (assembler input). `x86_64-linux-gnu-ld` lines = 12,488, of which 3,073 contain ` -r ` (partial links); lines containing `objtool` = 18,972; `scripts/mod/modpost` = 26; `scripts/genksyms/genksyms` = 6; `scripts/basic/fixdep` = 12 (fixdep is invoked from the `cmd` files and mostly not echoed); module files listed as `.ko.xz` in the package contents = 24,390 lines.
- Wall time: `Build-Time: 9443` s = 2 h 37 m 23 s of the "Build" phase; `Package-Time: 9567` s; the "Build needed 02:39:27" line agrees to within the install time.
- The three-flavour repetition explains 45,608 ≈ 2.3 × 19,819 (the `cloud-amd64` and `rt-amd64` configs compile subsets/supersets of the same objects).

**Coverage.**
- T1 — covers the *counts* only: number of compiler, `ld -r`, `objtool`, `modpost`, `genksyms` invocations of a full Debian kernel build (three flavours), from the verbose command log; no lifetimes or CPU per process.
- T2 — does not cover (no timing per compile).
- T4 — covers: a distribution build farm's parallelism as actually used: `DEB_BUILD_OPTIONS=parallel=6` on `x86-conova-01.debian.org` (linux) and on `x86-ubc-01` (hello, `make -j6`); the builder hosts' core counts are not in the logs.
- T6 — covers: kernel 7.1.13 (Debian config, three flavours) built with `gcc-15` at `parallel=6` in 9,443 s of build phase; ten more wall times per builder host from the index page (2 h 28 m – 2 h 55 m).
- T3, T5, T7, T8 — does not cover.

**One observation?** Yes: one build of one package version on one named buildd host (hardware not described), 2026-09-03/04; the index page adds a series of comparable builds on four named hosts. Not a desktop.

---

### S3-04 — Fedora koji: kernel 6.17.0-0.rc1.17.fc43 x86_64 build logs (`make -j64` on a 2-socket EPYC 9174F)

**Citation.** Fedora Koji build artifacts, `https://kojipkgs.fedoraproject.org/packages/kernel/6.17.0/0.rc1.17.fc43/data/logs/x86_64/` — `root.log`, `build.log`, `hw_info.log`, `state.log`, `mock_output.log`. Terms: Fedora Project public build logs.

**Copy.** `sources/S3-04-fedora-koji-kernel/`: `root.log` (`70eab3898157cd0c7bc1b0af0c9eb3de861ddef54dc617814deb96b0e9df7f24`), `build.log` (8,407,359 B, `b1714e97dd4101d47b41eb0f2c15a323f474017ad7e0b93284cae4ee09bc1eb5`), `hw_info.log` (`9eddf249d90267932d1f879567afebab712403ea5379553c522d8c384b18bdd7`), `state.log` (`d3971486d0fa3693b353eff5417baffb5d948bea5b651336f6adf3e4333b052f`), `mock_output.log` (`2d1b60500b287d26b0cd476afa1bf1eafae0884abfcb32396ec07b5f9e799393`); accessed 2026-09-14.

**Passages.**

`hw_info.log:1-13`:
> `CPU info:` / `Architecture:                            x86_64` / … / `CPU(s):                                  64` / `On-line CPU(s) list:                     0-63` / `Vendor ID:                               AuthenticAMD` / `Model name:                              AMD EPYC 9174F 16-Core Processor` / `CPU family:                              25` / `Model:                                   17` / `Thread(s) per core:                      2` / `Core(s) per socket:                      16` / `Socket(s):                               2`

`root.log:58`:
> `DEBUG util.py:461:  Mem:           125Gi       3.4Gi       117Gi       8.5Mi       5.8Gi       122Gi`

`build.log:1209` (the whole line is 1.1 kB; quoted with the HOSTCFLAGS/HOSTLDFLAGS values elided):
> `+ /usr/bin/make -s 'HOSTCFLAGS=-O2  -fexceptions -g -grecord-gcc-switches -pipe -Wall …' 'HOSTLDFLAGS=-Wl,-z,relro …' ARCH=x86_64 KCFLAGS= WITH_GCOV=0 -j64 bzImage`

`build.log:1218`:
> `+ /usr/bin/make -s … ARCH=x86_64 KCFLAGS= WITH_GCOV=0 -j64 modules`

(the same two lines recur at `:3533` and `:3542` for the second variant; `grep -aoE 'KERNELRELEASE=[^ ]+' build.log | sort | uniq -c` → `KERNELRELEASE=6.17.0-0.rc1.17.fc43.x86_64` ×2 and `KERNELRELEASE=6.17.0-0.rc1.17.fc43.x86_64+debug` ×2.)

`state.log:19-21`:
> `2025-08-11 16:33:06,238 - Start: rpmbuild kernel-6.17.0-0.rc1.17.fc43.src.rpm`
> `2025-08-11 17:36:53,638 - Finish: rpmbuild kernel-6.17.0-0.rc1.17.fc43.src.rpm`
> `2025-08-11 17:36:55,820 - Finish: build phase for kernel-6.17.0-0.rc1.17.fc43.src.rpm`

**Computed.** `rpmbuild` wall time = 17:36:53.638 − 16:33:06.238 = 3,827.4 s (63 min 47 s) for the whole package build, which compiles two kernel variants (`x86_64` and `x86_64+debug`, each `bzImage` + `modules`) at `-j64` = the host's 64 logical CPUs (`hw_info.log`). `build.log` is `make -s` (silent), so per-object lines are not present (`grep -acE '^  CC ' build.log` = 29, all from non-kernel sub-builds).

**Coverage.**
- T4 — covers: Fedora's koji builder uses `-j64` on a 64-thread host (i.e. `-j` = logical CPU count; `%_smp_mflags` expansion visible as the literal `-j64`), with machine named.
- T6 — covers: two Fedora kernel configs (rc kernel 6.17.0-rc1) built in 63 min 47 s total on a 2× EPYC 9174F (32 c / 64 t, 125 GiB RAM) build host.
- T1 — does not cover (silent make). T2, T3, T5, T7, T8 — does not cover.

**One observation?** Yes: one koji task on one named builder (mock chroot, Fedora 43), 2025-08-11. Not a desktop.

---

### S3-05 — Yocto Project build-performance results (`yocto-buildstats` repo): per-task rusage/IO of a full `core-image-sato` build and a `virtual/kernel` build on `perf-debian12-vk`

**Citation.** Yocto Project, *yocto-buildstats — Build performance test results from the Yocto project*, https://git.yoctoproject.org/yocto-buildstats/, branch `perf-debian12-vk/master/qemux86`, commit `a4a792be0e0d6994898e9fa43d8a8716460ee37e` (2026-09-14T17:29:29+00:00, "Results of master:f94ae3d6ba49aef86f497998c0e0232a5039510a on perf-debian12-vk"), tag `perf-debian12-vk/master/qemux86/68785-gf94ae3d6ba49aef86f497998c0e0232a5039510a/5`; git note `refs/notes/buildstats/perf-debian12-vk/master/qemux86` (notes commit `b1f28e63c198c63aa2eb215af052ed3af71c6360`, 2026-09-14T17:29:29+00:00, note object `bcd38b2416b7ae007cb5ee36987124ae4b577fb4` for commit `a4a792be`). Format definitions: openembedded-core commit `225db9c0df20fdf07479c6d0b992dd52fe2a8464` (2026-09-14), `meta/classes-global/buildstats.bbclass`, `meta/lib/oeqa/buildperf/base.py`, `scripts/lib/buildstats.py`. Documentation: docs.yoctoproject.org/dev/test-manual/test-process.html; wiki TipsAndTricks/MiningPerformanceData (last edit per page) and TipsAndTricks/InvestigatingBuildTime (page footer: "last edited on 28 February 2017"). Licence: OE-core files are MIT (header of `buildstats.bbclass`); the results repository states no licence.

**Copy.** `sources/S3-05-yocto-buildperf/`: `results.json` (`6d2e6a1403d796fe5aca091ae41a9e4a402420b67f9714206c5a8f86c734bd42`), `metadata.json` (`7dd0568e2a3aec8ddd312a1cbc4cb41b7d322426ece49d2d87543cc17b12a22f`), `oe-build-perf-test.log` (`2485ec884c884d6bcf7e31ddecaf5fd3a6a0ef3e36048418803a4700c976f008`), `build-conf-auto.conf` (`a57118e69bce286162415527acfbf53b2526b55b75ff7a8cdb6df9333f302e54`), `buildstats-note-a4a792be.json` (8,614,927 B, `6e4903a9f4c5480b487aa3ca07dc7e303124bdb5198e32ed7176dcd1e4070962`), `buildstats.bbclass` (`f626a542e370eabe56e374b267d1f67bc6b3f019aa36396f77e46e8be057bc0f`), `oe-core-oeqa-buildperf-base.py` (`b47ad82fe8b606bef8eeb5b7db82b3e36e8372a4eeb59c78e89fc9fce510efca`), `oe-core-scripts-lib-buildstats.py` (`cc9d105b1cf6bb85a603c8cc672f40cbacbad8f3825e135e70fc5a5b3e3157ee`), `yocto-buildstats-cgit-index.html`, `wiki-MiningPerformanceData.html` (`15319649cade3541b2322622b5b27e01a3a312ab31bf73b2ef3bc62b9508f417`), `wiki-InvestigatingBuildTime.html`, `docs-test-process.html`; accessed 2026-09-14.

**Passages.**

`buildstats.bbclass:17-21` (what is recorded per task):
> `def get_buildprocess_cputime(pid):`
> `    with open("/proc/%d/stat" % pid, "r") as f:`
> `        fields = f.readline().rstrip().split()`
> `    # 13: utime, 14: stime, 15: cutime, 16: cstime`
> `    return sum(int(field) for field in fields[13:16])`

`buildstats.bbclass:88-111`:
> `def write_task_data(status, logfile, e, d):` … `f.write(d.expand("${PF}: %s\n" % e.task))` / `f.write(d.expand("Elapsed time: %0.2f seconds\n" % elapsedtime))` / `cpu, iostats, resources, childres = get_process_cputime(os.getpid())` / `f.write("utime: %s\n" % cpu['utime'])` / `f.write("stime: %s\n" % cpu['stime'])` / `f.write("cutime: %s\n" % cpu['cutime'])` / `f.write("cstime: %s\n" % cpu['cstime'])` / `for i in iostats: f.write("IO %s: %s\n" % (i, iostats[i]))` / `rusages = ["ru_utime", "ru_stime", "ru_maxrss", "ru_minflt", "ru_majflt", "ru_inblock", "ru_oublock", "ru_nvcsw", "ru_nivcsw"]` / `for i in rusages: f.write("rusage %s: %s\n" % (i, getattr(resources, i)))` / `for i in rusages: f.write("Child rusage %s: %s\n" % (i, getattr(childres, i)))` … `f.write("Ended: %0.2f \n" % e.time)`

`buildstats.bbclass:47-48`:
> `    resources = resource.getrusage(resource.RUSAGE_SELF)`
> `    childres = resource.getrusage(resource.RUSAGE_CHILDREN)`

`oe-core-oeqa-buildperf-base.py:405-435` (how the perf test folds these into the JSON note; note that self and child rusage are *summed* into one `rusage` dict):
> `        def bs_to_json(filename):`
> `            """Convert (task) buildstats file into json format"""`
> …
> `                    elif key.find('rusage') >= 0:`
> `                        split = key.split()`
> `                        ru_key = split[-1]`
> `                        if ru_key in ('ru_stime', 'ru_utime'):`
> `                            val = float(val)`
> `                        else:`
> `                            val = int(val)`
> `                        rusage[ru_key] = rusage.get(ru_key, 0) + val`
> …
> `            bs_json['elapsed_time'] = end_time - start_time`
> `            bs_json['rusage'] = rusage`
> `            bs_json['iostat'] = iostat`

`oe-core-scripts-lib-buildstats.py:38-46`:
> `    @property` / `    def cputime(self):` / `        """Sum of user and system time taken by the task"""` / `        rusage = self['rusage']['ru_stime'] + self['rusage']['ru_utime']` / `        if self['child_rusage']:` / `            # Child rusage may have been optimized out` / `            return rusage + self['child_rusage']['ru_stime'] + self['child_rusage']['ru_utime']`

`metadata.json` (whole file is 40 lines; the config block):
> `"hostname": "perf-debian12-vk"` … `"host_distro": {"id": "debian", "version_id": "12", "pretty_name": "Debian GNU/Linux 12 (bookworm)"}` … `"meta": {"commit": "f94ae3d6ba49aef86f497998c0e0232a5039510a", "commit_count": 68785, …, "branch": "master"}` … `"config": {"BB_NUMBER_THREADS": "16", "MACHINE": "qemux86", "PARALLEL_MAKE": "-j 16 -l 75"}`

`build-conf-auto.conf:5,7` (the autobuilder-written conf in the same results directory states a different value; both are quoted, the discrepancy is not resolved by the files):
> `BB_NUMBER_THREADS = '24'`
> `PARALLEL_MAKE = '-j 24'`

`results.json` (`tests.test12`):
> `"name": "test12", "description": "Build virtual/kernel", "status": "SUCCESS", "start_time": 1789401675.889464, "elapsed_time": 331.765599, "measurements": {"build": {"type": "sysres", "name": "build", "legend": "bitbake virtual/kernel", "values": {"start_time": 1789401720.95261, "elapsed_time": 286.698475, "rusage": {"ru_utime": 0.576741, "ru_stime": 0.13089599999999998, "ru_maxrss": 77752, …, "ru_nvcsw": 14594, "ru_nivcsw": 12}, "iostat": {"rchar": 10976329, "wchar": 26721, "syscr": 7752, "syscw": 232, "read_bytes": 19005440, "write_bytes": 32768, "cancelled_write_bytes": 0}}}}`

(the `rusage` in `results.json` is that of the timed `bitbake` client process only — 0.58 s user for a 286.7 s build — not of the build.)

`results.json` (`tests.test1`): `"description": "Build core-image-sato"`, `"legend": "bitbake core-image-sato"`, `"elapsed_time": 3566.749511`.

`oe-build-perf-test.log:1-8`:
> `[2026-09-14 15:00:42,246] INFO: Testing Git revision branch:commit master:f94ae3d6ba49aef86f497998c0e0232a5039510a (68785)` / `[2026-09-14 15:00:42,247] INFO: Executing test test1: Build core-image-sato` / … / `[2026-09-14 16:00:35,972] INFO: Saving buildstats in JSON format` / `[2026-09-14 16:01:15,889] INFO: Executing test test12: Build virtual/kernel` / … / `[2026-09-14 16:02:00,949] INFO: Timing command: bitbake virtual/kernel`

`buildstats-note-a4a792be.json`, key `test1.build`, recipe `linux-yocto` (`"version": "7.2.4+git", "revision": "r0"`), task `do_compile` (one JSON object, quoted whole):
> `{"start_time": 1789400550.46, "status": "PASSED", "elapsed_time": 229.01, "rusage": {"ru_utime": 1989.325205, "ru_stime": 313.590933, "ru_maxrss": 1227632, "ru_minflt": 84049951, "ru_majflt": 689, "ru_inblock": 568, "ru_oublock": 13946728, "ru_nvcsw": 115827, "ru_nivcsw": 140666}, "iostat": {"rchar": 48569522015, "wchar": 7168702479, "syscr": 6422164, "syscw": 1435747, "read_bytes": 290816, "write_bytes": 7140724736, "cancelled_write_bytes": 1174847488}}`

same recipe, `do_compile_kernelmodules`:
> `{"start_time": 1789400949.27, "status": "PASSED", "elapsed_time": 116.05, "rusage": {"ru_utime": 1293.80425, "ru_stime": 223.783508, "ru_maxrss": 688564, "ru_minflt": 61787559, "ru_majflt": 544, "ru_inblock": 264, "ru_oublock": 8356816, "ru_nvcsw": 68928, "ru_nivcsw": 124805}, "iostat": {"rchar": 35423784276, "wchar": 4248387580, "syscr": 4266862, "syscw": 884412, "read_bytes": 135168, "write_bytes": 4278689792, "cancelled_write_bytes": 186396672}}`

docs test-process (text lines 79–81):
> Performance builds (buildperf-\* targets in the console) are triggered separately every six hours and automatically push their results to the buildstats repository.

wiki MiningPerformanceData:
> We can dive into the buildstats by telling oe-build-perf-report to extract the buildstats using --dump-buildstats.  These are also in the git repository but due to their size they are not fetched by default.
> `ERROR: No buildstats found, please try running 'git fetch origin refs/notes/buildstats/ypperf-fedora25/master/qemux86:refs/notes/buildstats/ypperf-fedora25/master/qemux86' to fetch them from the remote`
> Note that these JSON files are not the same format as the buildstats files written by bitbake, but the data is the same and the tools work with both.

**Computed (file `buildstats-note-a4a792be.json`, key `test1.build`; python: load JSON, iterate `recipes[*].tasks`).** The note holds `test1.build` and `test13.build` (572 recipes each); `test12` (the kernel-only build) has no note, so the kernel figures come from the `core-image-sato` build. 9,649 task records; Σ `rusage.ru_utime` = 90,646 s, Σ `ru_stime` = 12,621 s, Σ `elapsed_time` = 21,234 s; build window (max end − min start) = 3,548 s; peak number of simultaneously running tasks = 16 (= `BB_NUMBER_THREADS` 16 in `metadata.json`). 556 `do_compile` tasks: elapsed p10 0.1 s, p50 2.2 s, mean 16.9 s, p90 30.2 s, max 1,180.3 s (`clang-native`), sum 9,369 s; the eight longest: `clang-native` 1,180.3 s, `llvm` 977.5, `llvm-native` 878.9, `gcc` 377.1, `linux-yocto` 229.0, `mesa` 189.8, `librsvg` 173.3, `cargo-c-native` 172.1. For `linux-yocto do_compile`: (1989.33 + 313.59) / 229.01 = 10.05 CPUs busy on average against `PARALLEL_MAKE -j 16 -l 75`; system time is 13.6 % of CPU time; `ru_inblock` 568 vs `ru_oublock` 13,946,728 (512-byte blocks) → reads came from the page cache, 7.14 GB written (`iostat.write_bytes` 7,140,724,736); involuntary context switches 140,666 vs voluntary 115,827 over the task. For `do_compile_kernelmodules`: (1293.80 + 223.78) / 116.05 = 13.08 CPUs busy.

**Coverage.**
- T1 — covers, partially: object = a bitbake task (`do_compile` of a recipe = one `make -j16` tree) with all its children folded in; unit = seconds of user/system CPU, block I/O counts, context switches per task; scope = one full distribution build (572 recipes) and, within it, the kernel's compile tasks; population = one build on one perf host. No per-process data (children are summed by `RUSAGE_CHILDREN`).
- T2 — covers weakly: the kernel compile task's aggregate CPU/wall ratio and I/O counts (warm cache, since `ru_inblock` is 568); no per-TU distribution, no blocking split.
- T4 — covers: the perf host's `PARALLEL_MAKE = -j 16 -l 75` and `BB_NUMBER_THREADS = 16` (metadata) — `auto.conf` says `-j 24`; the note's peak concurrency of 16 tasks matches the metadata value.
- T6 — covers: `linux-yocto` 7.2.4 (qemux86 config) `do_compile` 229.0 s + `do_compile_kernelmodules` 116.1 s inside the image build, and `bitbake virtual/kernel` 286.7 s standalone, on `perf-debian12-vk` (CPU model not recorded anywhere in the fetched files).
- T3, T5, T7, T8 — does not cover.

**One observation?** One results commit of one host (`perf-debian12-vk`, Debian 12) on 2026-09-14; the repository holds the same tests for ≈70 host/branch combinations back to 2016 (cgit index page), each with a git note. Machine hardware unnamed; project (poky master `f94ae3d6`) and window named. This is a 16-thread build server, not a desktop.

---

### S3-06 — Launchpad bug #2141316: a DKMS `make.log` for `nvidia/580.126.09` (`make -j8` on an i7-4790, 208 module objects, 58 s to failure)

**Citation.** Gray (bugreport-6), "nvidia-dkms-580 580.126.09-0ubuntu3: nvidia kernel module failed to build", Ubuntu bug #2141316, filed 2026-02-09, https://bugs.launchpad.net/ubuntu/+source/nvidia-graphics-drivers-580/+bug/2141316; attachments `make.log` (`…/+attachment/5944364/+files/make.log`, 5,421,440 B), `ProcCpuinfoMinimal.txt` (`…/5944366/+files/ProcCpuinfoMinimal.txt`), `Dependencies.txt`. Terms: public Launchpad bug data.

**Copy.** `sources/S3-06-launchpad-2141316-dkms/`: `make.log` (`082128b39b14a42fd8d68bd16fa218b80c16bc5a2e43206ac45d50762c03b8df`), `ProcCpuinfoMinimal.txt` (`cd08ecc262466ef434b5eb3683a1707855360576061e8aa0dc5ccdbd3f058e72`), `Dependencies.txt`, `bug-2141316.html` (`d7552699529b691766181ecf7de35af45e0d924248effcd234378195d7f4868e`); accessed 2026-09-14.

**Passages.**

`make.log:1-5`:
> `DKMS (dkms-3.2.0) make.log for nvidia/580.126.09 for kernel 6.19.0-3-generic (x86_64)`
> `Mon Feb  9 13:38:53 GMT 2026`
> ``
> `Building module(s)`
> `# command: unset ARCH; [ ! -h /usr/bin/cc ] && export CC=/usr/bin/gcc; env NV_VERBOSE=1 'make' -j8 NV_EXCLUDE_BUILD_MODULES='' KERNEL_UNAME=6.19.0-3-generic IGNORE_XEN_PRESENCE=1 IGNORE_CC_MISMATCH=1 SYSSRC=/lib/modules/6.19.0-3-generic/build LD=/usr/bin/ld.bfd CONFIG_X86_KERNEL_IBT= modules`

`make.log:50269`, `:50284-50285` (end of file):
> `nvidia.o: error: objtool: _nv027633rm+0xf: call without frame pointer save/setup`
> `# exit code: 2`
> `# elapsed time: 00:00:58`

`ProcCpuinfoMinimal.txt:5,11,13`:
> `model name	: Intel(R) Core(TM) i7-4790 CPU @ 3.60GHz`
> `siblings	: 8`
> `cpu cores	: 4`

Bug description (text lines 35, 38, 55–56, 68, 77 of the tag-stripped page):
> Kubuntu 26.04 dev
> ` DKMS (dkms-3.2.0) make.log for nvidia/580.126.09 for kernel 6.19.0-3-generic (x86_64)`
> ` # exit code: 2`
> ` # elapsed time: 00:00:57`
> `ProcVersionSignature: Ubuntu 6.18.0-9.9-generic 6.18.5`
> `InstallationMedia: Kubuntu 26.04 LTS "Resolute Raccoon" - Daily amd64 (20260128)`

**Computed (file `make.log`).** `grep -c '^# CC \[M\]'` = 208 module objects compiled; `grep -c '^# LD \[M\]'` = 5 (`nvidia`, `nvidia-uvm`, `nvidia-modeset`, `nvidia-drm`, `nvidia-peermem`, from the `cmd_mod` lines 13–29); `grep -c 'cmd_gen_symversions'` = 208; lines containing `objtool` = 49,160 (the verbose objtool error dump); `grep -oE ' -c -o [^ ]+' | sort -u | wc -l` = 208. `-j8` equals the host's 8 logical CPUs (`siblings 8`, `cpu cores 4`), consistent with NVIDIA's `dkms.conf` using `nproc` (S2's domain to verify). The 58 s elapsed is for a run that compiled all 208 objects and failed at the objtool stage of `nvidia.o`, so it is a lower bound on a successful autoinstall on this machine.

**Coverage.**
- T5 — covers: the exact `make` invocation DKMS ran (`'make' -j8 … modules` with `NV_VERBOSE=1`), the number of compiler invocations (208 `CC [M]`), the elapsed time footer DKMS writes (`# elapsed time: 00:00:58`), the machine (i7-4790, 4c/8t) and the kernel (6.19.0-3-generic). No CPU time and no process trace. What triggered the run: an apt upgrade of the kernel (the bug text's dpkg output), i.e. the kernel-install hook; the DKMS mechanism itself is S2's domain.
- T4 — covers weakly: the observed DKMS parallelism equals the logical CPU count.
- T1, T2, T3, T6, T7, T8 — does not cover.

**One observation?** Yes: one DKMS build on one desktop (Kubuntu 26.04 dev, i7-4790), 2026-02-09 13:38:53 GMT; a second run (bug description, 00:00:57) on the same machine. Machine and window named.

---

### S3-07 — NVIDIA developer forum thread 206793: an unmeasured user claim that a DKMS module build takes "approx. 15mins" vs "2-3 mins" without DKMS

**Citation.** "Could you please help us to reduce the DKMS kernel module build time?", NVIDIA Developer Forums (Mellanox OFED category), topic 206793, opened 2019-07-05T07:10:58Z, 3 posts (users `system`, `march`), https://forums.developer.nvidia.com/t/could-you-please-help-us-to-reduce-the-dkms-kernel-module-build-time/206793 — read via the Discourse JSON endpoint `/t/206793.json`.

**Copy.** `sources/S3-07-nvidia-forum-206793/t-206793.json` (`a08701b84aa287dfe809021c384d26b55683e420eed10d141e1efcf2addc6cef`), accessed 2026-09-14.

**Passages** (`post_stream.posts[0].cooked`, tags stripped; post 1, 2019-07-05T07:10:58Z):
> We have ConnectX5 adapters and would like to use it with Ubuntu 16.04, however when DKMS package is going to be installed it takes approx. 15mins on Dell 620 blade to be built which is quite a huge time, taking account that only some kernel modules are expected to be built.
> When trying to build only the modules instead of DKMS the build time significantly less, it takes only approx. 2-3 mins. This time would be acceptable for DKMS build as well.

Post 3 (2019-07-08T11:17:36Z):
> However the installation time of the DKMS way is unacceptable (15-20 mins).

**Coverage.** T5 — covers only as an *unmeasured user claim*: MLNX_OFED (not a desktop driver) DKMS build ≈15–20 min vs 2–3 min direct, on a "Dell 620 blade", Ubuntu 16.04, 2019; no `-j`, no CPU, no log. T1–T4, T6–T8 — does not cover. Labelled: unmeasured user claim, server hardware.

---

### S3-08 — Three `.ninja_log` files of LLVM builds published in GitHub repositories (per-edge wall-clock start/end in ms)

**Citation.** (a) XeroMz69/Bebas, `.ninja_log` at branch `master` (raw.githubusercontent.com, 81,230 B, 739 lines); (b) hoholee12/rpcs3-custom, `llvm_build/.ninja_log` at `master` (195,712 B, 1,713 lines; Windows paths `C:/Users/hoholee12/Documents/GitHub/rpcs3-custom/llvm_build/…`, `.obj` outputs); (c) thead-yocto-mirror/gpu_bxm_4_64-kernel, `tools/llvm/llvm.riscv64/.ninja_log` at `master` (149,289 B, 1,465 lines). Found by GitHub code search (log rows 25–26); the commits are those of `master` on 2026-09-14 (raw fetch does not expose the hash; no clone was made). Format definition: Chromium depot_tools `post_build_ninja_summary.py` (S3-13). Licences: the repositories' licences were not read (the logs are build by-products, not source); quoted numbers only.

**Copy.** `sources/S3-08-ninja-logs/`: `XeroMz69_Bebas_.ninja_log` (`d68875d33c927462d68090c468c3d9ae3737942029f991af7ad38deb1d33dc79`), `hoholee12_rpcs3-custom_.ninja_log` (`5d245b331b088b523b871d6b8240352f14949c13047d0393982174b3bfadb4cf`), `thead-yocto-mirror_gpu_bxm_4_64-kernel_.ninja_log` (`6126a4d62bfec5ad8385713a1c0b37a990977c508bff8fee06237d04c4053b88`); accessed 2026-09-14.

**Passages.**

`XeroMz69_Bebas_.ninja_log:1-2`:
> `# ninja log v5`
> `41	143	1734706561521247081	lib/Support/CMakeFiles/LLVMSupport.dir/AutoConvert.cpp.o	db30eaae3c150570`

`hoholee12_rpcs3-custom_.ninja_log:1-2`:
> `# ninja log v5`
> `39	144	6799304867112142	lib/Support/CMakeFiles/LLVMSupport.dir/ABIBreak.cpp.obj	aa0cf3a30bdda31c`

`thead-yocto-mirror_gpu_bxm_4_64-kernel_.ninja_log:1-2`:
> `# ninja log v5`
> `9	54	1626094296	lib/Demangle/CMakeFiles/LLVMDemangle.dir/Demangle.cpp.o	6bbd0332cc30c225`

Column meaning, from `post_build_ninja_summary.py:127-148` (S3-13):
> `    assert header in ("# ninja log v5\n", "# ninja log v6\n"), (`
> `        start, end, _, name, cmdhash = parts  # Ignore restat.`
> `        start = int(start) / 1000.0`
> `        end = int(end) / 1000.0`
> `            # This has to be done by comparing end times because records are`
> `            # written to the .ninja_log file when commands complete, so end`
> `            # times are guaranteed to be in order, but start times are not.`

**Computed (python over each file; a new ninja run is assumed to start wherever `end` decreases relative to the previous line, as the Chromium script does; statistics are for the largest run; "compile edges" = outputs ending in `.cpp.o`, `.c.o`, `.cc.o`, `.cpp.obj`, `.c.obj`; durations = `end − start` in ms).**
- (a) Bebas: 1 run, 738 edges, span 35–420,707 ms (≈7.0 min); all edges p10 1,431 / p50 6,237 / mean 9,789 / p90 22,268 / p99 43,512 / max 78,885 ms, Σ 7,223,955 ms; 646 compile edges p10 2,267 / p50 7,779 / mean 10,978 / p90 25,211 / max 78,885 ms; peak concurrent edges 30; Σ duration ÷ span = 17.2 (mean concurrency). Longest non-compile edges: `RISCVTargetParserDef.inc` 9,979 ms, `AArch64TargetParserDef.inc` 4,783 ms. Mtime column 1734706561521247081 ns → 2024-12-20. Linux paths (`/workspace/Bebas/`).
- (b) rpcs3-custom (Windows, MSVC `.obj`): 2 runs, largest 1,711 edges, span 32–2,555,842 ms (≈42.6 min); all edges p10 1,270 / p50 5,241 / mean 17,547 / p90 11,882 / p99 28,021 / max 1,528,911 ms; 1,538 compile edges p50 5,775 / p90 12,040 ms, Σ 20,593,286 ms; peak concurrency 19; the max is `X86GenAsmMatcher.inc` 1,521,848 ms (TableGen, 25 min). The mean exceeds p90 because of the TableGen outliers.
- (c) gpu_bxm_4_64-kernel `llvm.riscv64`: 5 runs, largest 1,437 edges, span 9–15,732 ms; compile edges p10 39 / p50 52 / mean 243 / p90 104 / max 15,557 ms; peak concurrency 66 — a ≈16 s "build" of 1,333 objects at 52 ms median is a cache-hit or no-op rebuild, not real compilation; labelled as such and not used further. Mtime column is in seconds (1626094296 → 2021-07-12), an older ninja.

**Coverage.**
- T2 — covers, partially, for LLVM (a C++ project, not the kernel): the per-translation-unit *wall* time distribution under ninja's default parallelism (object = one ninja edge, unit = ms wall, statistic = quantiles above, population = one full LLVM build each). Wall time, not CPU time; machine, compiler and `-j` are not recorded in the file; (b) is Windows.
- T1 — covers weakly: the number of edges (≈740 / 1,711 for an LLVM subset build) and the peak concurrency (30 / 19), which bounds the number of simultaneously live compiler processes.
- T4 — covers weakly: the observed peak concurrency (30 and 19) is a lower bound on the `-j` in force.
- T3, T5, T6, T7, T8 — does not cover.

**One observation?** Each file is one build on an unnamed machine at an unnamed `-j`; project named (LLVM sub-trees), window given by the log span, dates from the mtime column. Partial builds are possible (a `.ninja_log` records only edges that ran).

---

### S3-09 — LLVM Compile-Time Tracker and its raw data repository: per-file `perf stat` (instructions, task-clock, wall-time, max-rss) for every CTMark file at every LLVM commit

**Citation.** Nikita Popov, *LLVM Compile-Time Tracker*, https://llvm-compile-time-tracker.com/ (index and `about.php`); infrastructure repo nikic/llvm-compile-time-tracker, commit `c9d76a9e51a6a118473f17dadbc7c3c64dc8ee87` (2026-04-11); data repo nikic/llvm-compile-time-data, `master` = `545e324386d2d220be29712356ee2b63e8cf17e9` (2023-09-30, "Remove non-main data"; branches `master`, `historical`; 253,073 tree entries under `experiments/`), example experiment `experiments/00/00030b18c1e60e5e4f7444e30694bac9ffc14e/` = LLVM commit `0000030b18c1e60e5e4f7444e30694bac9ffc14e` ("Revert "[Flang][OpenMP] Add semantic check…"", Kiran Chandramohan, 2022-04-03T15:54:02+00:00, per `commits.json`). Licence: `LICENSE` files exist in both repos (not quoted); the tracker README says "Everything in here is something of a hack and not designed for general usage."

**Copy.** `sources/S3-09-llvm-compile-time-tracker/`: `README.md` (`61719fe4c7ffe5b65f9e0c072da07a81e6c256be447c4480a80762de99ee6ed4`), `timeit.sh` (`94306dd1b068fb7450a2696c9f16d0c898d24bf8679f24fcea7b4110bb78c18e`), `build_llvm_test_suite.sh` (`6f5a5919e496778971fe787dc8f667972725ff2187e2a10f03397c9076552d36`), `runner.php`, `llvm-compile-time-data-README.md`, `commits.json` (147,029 commits, `3b5972e50327984f224cd097a71c4022d69f9bba90b139a6b2b59053c70e29c6`), `summary.json` (`9a281760bb168d36f18ccda2442d4d6a1c5295917b5087525b2ae80fd8e2f0cf`), `stats.msgpack.gz` (289,667 B, `af3e5c7991e348805a896e3d07b5820f5adc8d8b7ddb3e50f3f7e4bc936aca4e`), its decoding `stats.json` and the decoder `mp.py` (a minimal msgpack reader written for this record), `index.php.html`; accessed 2026-09-14.

**Passages.**

`timeit.sh:1-20` (the measurement wrapper; each compiler invocation is run under `perf stat`):
> `TIME_OUT=$OUT` / `PERF_OUT="$OUT.perfstats"` / `LC_ALL=C \` / `    time -f "%M;%e" -o $TIME_OUT \` / `    perf stat -x \; -o $PERF_OUT \` / `        -e instructions \` / `        -e instructions:u \` / `        -e cycles \` / `        -e task-clock \` / `        -e branches \` / `        -e branch-misses \` / `        $@`

`build_llvm_test_suite.sh:3-5`:
> `# By default ninja will use nproc + 2 threads.`
> `# Limit to nproc - 1 to reduce noise.`
> `ninja -j7 -C/tmp/llvm-test-suite-build`

about.php (text):
> The compile time tracker tests the CTMark portion of the LLVM test-suite against specific cached CMake configurations.
> The $CONFIGs used by the tracker are O3, ReleaseThinLTO, ReleaseLTO-g and O0-g.
> Compilers: host: gcc 11.4 / stage1: clang compiled using host compiler (release build) / stage2: clang compiled using stage1 compiler (release build with ThinLTO)
> Displayed statistics for clang generally refer to the stage2 build. The stage1 build uses ccache and as such does not produce stable timing results.

`llvm-compile-time-data-README.md`:
> This repository contains raw compile-time statistics for LLVM. The data can be viewed at http://llvm-compile-time-tracker.com.

`stats.json` (decoded from `stats.msgpack.gz`), key path `NewPM-O3 → lencod → CMakeFiles/lencod.dir/nalucommon.c.o` (one per-file record, whole):
> `{"instructions": 106569050.0, "instructions:u": 86240948.0, "cycles": 100525065.0, "task-clock": 27.95, "branches": 20926781.0, "branch-misses": 562585.0, "max-rss": 66880.0, "wall-time": 0.03, "size-file": 5048, "size-text": 256, "size-data": 0, "size-bss": 0, "size-total": 256}`

`summary.json`, `data.NewPM-O3.lencod` (per-benchmark totals):
> `"instructions": 84668498037, "instructions:u": 83273822698, "cycles": 56537800529, "task-clock": 15718.130000000005, "branches": 16589215376, "branch-misses": 425518099, "max-rss": 4019808, "wall-time": 15.759999999999998, "size-file": 966464, …`

**Computed (file `stats.json`, per config, files = keys not ending in `.link`; wall-time in s, task-clock in ms; quantile = sorted value at index ⌊p·n⌋).**
- `NewPM-O3`: lencod 55 files, wall p10 0.03 / p50 0.15 / mean 0.29 / p90 0.74 / max 1.36 s, Σ 15.7 s, task-clock p50 147 ms, Σtask-clock/Σwall = 0.997; Bullet 121 files p50 0.14 / p90 0.37 / max 2.53 s (0.988); mafft 27 files p50 0.25 / max 1.40 s; ClamAV 98 files p50 0.09 / p90 0.38 / max 1.14 s (0.993); kimwitu++ 14 files p50 0.44 / max 3.62 s; sqlite3 2 files, `sqlite3.c` 9.87 s; SPASS 51 files p50 0.16 / max 1.05 s; 7zip 212 files p50 0.11 / p90 0.42 / max 0.85 s (0.990); consumer-typeset 51 files p50 0.15 / max 1.06 s; tramp3d-v4 1 file 23.71 s (1.11 × 10¹¹ user instructions).
- `NewPM-ReleaseThinLTO`: Σtask-clock/Σwall drops to 0.59–0.82 for most benchmarks (e.g. SPASS 0.590, Bullet 0.612, ClamAV 0.651) — the only configuration in this record where a compiler process is visibly *not* CPU-bound for its whole wall time; at `-O3` and `-O0-g` the ratio is 0.97–1.00.
- Across the ten CTMark benchmarks at `-O3`: 632 files; per-file wall time is right-skewed with medians of 0.09–0.44 s and maxima 0.85–3.6 s, plus two single-file outliers (`sqlite3.c` 9.9 s, `tramp3d-v4.cpp` 23.7 s).

**Coverage.**
- T2 — covers: the per-translation-unit CPU-time distribution (task-clock, cycles, user instructions) and wall time of one clang compilation per file, for 632 C/C++ files of CTMark at one LLVM commit, in four optimisation configurations, on the tracker's machine; the task-clock/wall ratio ≈1 (except ThinLTO) is evidence that a compiler process is CPU-bound throughout under a warm cache (the tracker rebuilds the same tree repeatedly). No cold-cache case, no blocking breakdown, not the kernel, not gcc. The data repository holds the same for ~147k commits (partial: only one experiment was fetched).
- T4 — covers, as a documented practitioner rationale: "By default ninja will use nproc + 2 threads. Limit to nproc - 1 to reduce noise." with `-j7` (so an 8-CPU machine).
- T1 — covers weakly: CTMark file counts per benchmark (the number of compiler processes a `ninja` build of each spawns).
- T3, T5, T6, T7, T8 — does not cover.

**One observation?** The fetched sample is one experiment (one LLVM commit, 2022-04-03) on the tracker's dedicated machine (CPU model not stated on the fetched pages; `-j7` implies 8 CPUs); the population is the whole CTMark tree; window = one full build per config. Machine unnamed, project and window named.

---

### S3-10 — Phoronix articles: kernel `defconfig` build times (EPYC 7742 2P 16 s; OpenBenchmarking average 125 s over 2,687 results) and the 2026 "faster kernel builds" series

**Citation.** Michael Larabel, "Building The Default x86_64 Linux Kernel In Just 16 Seconds", Phoronix, 14 August 2019, https://www.phoronix.com/news/Linux-16-Seconds-AMD-EPYC-2P; "Linux 7.4 Could End Up Seeing Kernel Builds ~36% Faster, Incremental Builds ~70% Faster", https://www.phoronix.com/news/Faster-Kernel-Builds-AI-v2; "AI Made A Lot Of "Hideous" Code But Found Major Bottlenecks For Faster Linux Compilation", https://www.phoronix.com/news/AI-To-Faster-Linux-Kernel-Comp; "Intel Linux Kernel Optimizations Show Huge Benefit For High Core Count Servers", https://www.phoronix.com/review/intel-scalability-optimizations (page 1 only); "Benchmarking The BORE Scheduler Performance With CachyOS Linux", https://www.phoronix.com/review/cachyos-bore (page 1 only). Terms: Phoronix editorial content, quoted under citation.

**Copy.** `sources/S3-10-phoronix/`: `Linux-16-Seconds-AMD-EPYC-2P.html` (`4913d660478a3d7175c4a5d1da3f5a9cf615dc8ab82adeeacff812d77e1112ff`), `Faster-Kernel-Builds-AI-v2.html` (`8381c619e89520fe66903727a519593fdb05b3d8f1ebb92a89c6e79c113b09d9`), `AI-To-Faster-Linux-Kernel-Comp.html` (`bd4409f9793d0e834ec66e353d26cb1978b8d2d572cf18f1d84502b7089ace18`), `intel-scalability-optimizations-p1.html` (`ead8798bbb2c90cbc5d6571b2595027c3741e9f5ec0f8e52fb32711fbe911603`), `cachyos-bore-p1.html` (`622cf8f01397839d32df926897ba0263cba69f9844006f585b0b90f97bc38a3a`); accessed 2026-09-14.

**Passages.**

16-seconds article (text lines 18–22):
> Written by Michael Larabel in Linux Kernel on 14 August 2019 at 03:02 AM EDT.
> It used to be that building out the Linux kernel could easily take the time needed to enjoy a beverage or have a meal while now with the EPYC 7742 2P it's easy to build the Linux kernel in just 15~16 seconds! … That is with a Linux x86_64 default "defconfig" build.
> That's with each server tested using an Intel Optane 900p 280GB NVMe SSD and maximum channels/frequency supported RAM and running Ubuntu 19.04 with the stock compiler. For fun on the weekend I intend to see how much lower I can get the kernel build time using a RAID setup as I/O appears to be the bottleneck at this point.
> If pulling up statistics from OpenBenchmarking.org with that same exact test profile version for building the kernel in the same manner and the same Linux 4.18 LTS sources, of 2,687 public sample results the average kernel build time is 125 seconds. That's over two minutes as the average kernel build time from mostly higher-end systems/servers. The EPYC 7742 2P accomplishes the same amount of work in just 16 seconds (or 15 seconds, sometimes) and is the fastest result I've found on OpenBenchmarking.org.
> Or the very common LLVM stack can be built in just 82 seconds while the dual Xeon Platinum 8280 came in at 106 seconds.

Faster-Kernel-Builds-AI-v2 (text lines 19–21):
> A number of single-threaded bottlenecks were tracked down and fixed within the Linux kernel thanks to the assistance of AI. A second revision of those patches hit the mailing list this morning and there is hope they could be upstreamed for Linux 7.4.
> A Linux kernel build with all modules included "allmodconfig" came in at 36% faster while incremental kernel builds came in at around 70% faster.
> Lorenzo Stoakes of ARM spearheaded this work …

AI-To-Faster-Linux-Kernel-Comp (text lines 20, 29):
> In the end he found a kernel build with all modules enabled was around 36% faster, incremental kernel builds up to 70% faster, and noop builds up to ~90% faster.
> Areas such as Kbuild, kallsyms, modpost, objtool, mksysmap, and the Rust build system were all affected by this work.

intel-scalability-optimizations page 1 (text line 24):
> This round of testing was carried out on both operating systems using Intel's Eagle Stream server with two flagship Intel Xeon Platinum 8490H "Sapphire Rapids" processors. From there both operating systems / kernels were tested at 240 threads (the default capacity; 120 cores + SMT for the two 8490H processors), 120 threads (disabling SMT/HT), 60 threads, 30 threads, 15 threads, 8 threads, and 4 threads for looking at the scaling performance across a wide variety of workloads.

cachyos-bore page 1 (text line 25): "… still having the System76 Thelio Major system in the same setup on CachyOS as the prior round of tests, here are the benchmarks with the CachyOS BORE kernel compared to the other kernel flavors …" — the result pages (2–4) returned HTTP 403.

**Coverage.**
- T6 — covers: kernel 4.18 `defconfig` wall time 15–16 s on 2× EPYC 7742 (Ubuntu 19.04, stock gcc), and an OpenBenchmarking population statistic: mean 125 s over 2,687 public results of the same profile version (population "mostly higher-end systems/servers"); the author's remark "I/O appears to be the bottleneck at this point" is an observation about the defconfig build at 256 threads. The 2026 articles give relative speed-ups (allmodconfig −36 %, incremental −70 %) with the bottleneck areas named (`kallsyms`, `modpost`, `objtool`, `mksysmap`), no absolute times on the fetched pages. The Intel scalability article documents a thread-count sweep (240/120/60/30/15/8/4) on a named machine, but the kernel-compile results are on the 403 pages.
- T4 — does not cover (PTS uses `-j $NUM_CPU_CORES`, see S3-11).
- T1, T2, T3, T5, T7, T8 — does not cover.

**One observation?** The EPYC figure is one machine/one profile (window not stated beyond the article date); the 125 s figure is an aggregate over 2,687 anonymous submissions (population statistic, machines not enumerable here because openbenchmarking.org is blocked).

---

### S3-11 — Phoronix Test Suite profiles that generate the OpenBenchmarking compile and batch data: `pts/build-linux-kernel`, `pts/build-llvm`, `pts/x264`, `pts/ffmpeg`, `pts/svt-av1`, `pts/pytorch`

**Citation.** phoronix-test-suite/test-profiles, `master` = `d2f1a150d388bd062737b445891edda0780f7e25` (2024-11-23): `pts/build-linux-kernel-1.16.0/`, `pts/build-llvm-1.5.0/`, `pts/x264-2.7.0/`, `pts/ffmpeg-7.0.1/`, `pts/svt-av1-2.15.0/`, `pts/pytorch-1.1.0/`. Licence: GPL-3.0 per the repository (not quoted).

**Copy.** `sources/S3-11-pts-test-profiles/<profile>/…` (per-file SHA-256 in the folder's `SHA256SUMS.txt`, e.g. `build-linux-kernel-1.16.0/install.sh` `735dcb5ea399ccc18b65981ca6e60165e1f1bc79caabf29802051054874485dd`, `build-linux-kernel-1.16.0/test-definition.xml` `791b68cc7162446c00d10c63e7846847b2b2debab3db1b18b994159e03290ae9`); accessed 2026-09-14.

**Passages.**

`build-linux-kernel-1.16.0/test-definition.xml:5-11`, `:33-42`:
> `    <Title>Timed Linux Kernel Compilation</Title>` / `    <AppVersion>6.8</AppVersion>` / `    <Description>This test times how long it takes to build the Linux kernel in a default configuration (defconfig) for the architecture being tested or alternatively an allmodconfig for building all possible kernel modules for the build.</Description>` / `    <ResultScale>Seconds</ResultScale>` / `    <Proportion>LIB</Proportion>` / `    <SubTitle>Time To Compile</SubTitle>` / `    <TimesToRun>3</TimesToRun>`
> `          <Name>defconfig</Name>` / `          <Value>defconfig</Value>` / `          <Message>Default Kernel Build</Message>` / … / `          <Name>allmodconfig</Name>` / `          <Value>allmodconfig</Value>` / `          <Message>This option is *much* more time consuming...</Message>`

`build-linux-kernel-1.16.0/install.sh:1-6`:
> `#!/bin/sh` / `echo "#!/bin/sh` / `cd linux-6.8` / `make -s -j \$NUM_CPU_CORES 2>&1` / `echo \$? > ~/test-exit-status" > build-linux-kernel` / `chmod +x build-linux-kernel`

`build-llvm-1.5.0/install.sh:4`:
> `cmake --build . -- -j \$NUM_CPU_CORES 2>&1`

`x264-2.7.0/test-definition.xml:7`, `:28`; `install.sh:23-25`:
> `    <Description>This is a multi-threaded test of the x264 video encoder run on the CPU with a choice of 1080p or 4K video input.</Description>`
> `      <Arguments>--slow-firstpass </Arguments>`
> `./x264_/bin/x264 -o /dev/null \$@ > \$LOG_FILE 2>&1`

`ffmpeg-7.0.1/install.sh:91-92` (the profile patches vbench to a single encoder thread):
> `-    cmd =  [ffmpeg,"-i",video,"-c:v","libx264","-threads",str(1)]+settings+["-y",output]`
> `+    cmd =  [ffmpeg,"-i",video,"-c:v",encoder,"-threads",str(1)]+settings+["-y",output]`

`svt-av1-2.15.0/test-definition.xml:7`:
> `    <Description>… SVT-AV1 is a CPU-based multi-threaded video encoder for the AV1 video format with a sample YUV video file.</Description>`

`pytorch-1.1.0/install.sh:10-11`:
> `num_threads = torch.get_num_threads()`
> `print(f'Benchmarking on {num_threads} threads')`

**Coverage.**
- T6 — covers the *definition* of the most widely used public kernel-compile benchmark: kernel 6.8, `defconfig` or `allmodconfig`, `make -s -j $NUM_CPU_CORES`, three runs, result in seconds; and `build-llvm` at `-j $NUM_CPU_CORES`. No data here (openbenchmarking.org blocked); the population statistic for an earlier version is quoted in S3-10.
- T7 — covers the definitions only: x264 with its default thread count (no `--threads` argument is passed), ffmpeg/vbench pinned to `-threads 1`, SVT-AV1 multi-threaded, PyTorch at `torch.get_num_threads()`; results are frames/s or batches/s, never utilisation.
- T4 — covers weakly: PTS's convention `-j $NUM_CPU_CORES` for builds.
- T1, T2, T3, T5, T8 — does not cover. Not an observation.

---

### S3-12 — `cachyos-benchmarker` (the sched-ext / CachyOS community's compile workload) and the scx repository's own references to kernel builds as a scheduler workload

**Citation.** CachyOS/cachyos-benchmarker, `master` = `02c56089da9c5056b0fd44216f7897d1f1d057fd` (2026-07-08), files `cachyos-benchmarker` (bash) and `README.md`; sched-ext/scx, `main` = `6c54f4f664bb8e9cc445c8333128b4ba17b93608` (2026-09-14), `DEVELOPER_GUIDE.md` and `scheds/rust/scx_rustland/README.md`. Licences: not read (tool descriptions quoted only).

**Copy.** `sources/S3-12-cachyos-benchmarker/`: `cachyos-benchmarker` (`64b3a5b8e2ac01ac8748b743c15dbbabcf4dfdfbeecec0e45579746be5ac8c4c`), `README.md` (`7207c299c4ea7cf4fb6804ca6e011f3e5f56e9f308c1f780c382aeda3f154679`), `scx-DEVELOPER_GUIDE.md` (`22cf67bb069ca7fa0aab116ea69180c6d2b286b71f912690bff2dc21720b0b78`), `scx_rustland-README.md` (`9ad422e4abe89f179b2ccdf0fd94c675cf1e8a0f1cae20bf561ca48e8b3792a5`); accessed 2026-09-14.

**Passages.**

`cachyos-benchmarker:20`, `:383`, `:386`, `:596`, `:97` (the kernel and ffmpeg compile workloads; line 97 is the ffmpeg build timer, the kernel build uses the same `make -s -j${CPUCORES}` pattern):
> `	'kernel defconfig'		#10`
> `CPUCORES=$(nproc)`
> `KERNVER="6.14.7"`
> `	make -s distclean && make -s defconfig`
> `	/usr/bin/time -f %e -o "$RESFILE" make -s -j${CPUCORES} &>/dev/null &`

`README.md:9,14,16,54`:
> `* ffmpeg compilation` / `* kernel defconfig` / `* x265 encoding`
> `*   **cachyos-benchmarker**: The core script. It prepares the environment, downloads necessary assets, and runs a suite of 14 synthetic and real-world benchmarks (such as `stress-ng`, Blender CPU render, FFmpeg/Kernel compilation, x265 encoding, schbench, and cyclictest). Results, along with detailed system and `sched-ext` information, are logged to a `.log` file.`

`scx-DEVELOPER_GUIDE.md:238-243`:
> `### `cachyos-benchmarker``
> `[`cachyos-benchmarker`](https://github.com/CachyOS/cachyos-benchmarker) is a lightweight benchmarking and stress testing tool, based on [mini-benchmarker](https://gitlab.com/torvic9/mini-benchmarker) by Tor Vic. It runs a variety of real-world and synthetic workloads, such as kernel build, ffmpeg, x265, y-cruncher, and more. It's particularly useful for exposing scheduler issues under stress, and works across most Linux distributions.`

`scx_rustland-README.md:44-47`:
> `… we can still obtain interesting results and, in this particular case, even outperform the default Linux scheduler (EEVDF) in terms of application responsiveness (FPS), while a CPU intensive workload (parallel kernel build) is running in the background.`

**Coverage.**
- T6 — covers the *definition* of the compile workload the sched-ext community uses: kernel 6.14.7 `defconfig`, `make -s -j$(nproc)`, timed with `/usr/bin/time -f %e` (wall only); an ffmpeg 7.0.1 build the same way; and the scx maintainers' statement that a parallel kernel build is their background load for responsiveness demos. No published numbers were found (the galpt archives, log row 36, contain no compile results).
- T7 — covers the definition only: x265 encoding and Blender CPU render are in the same suite (results are wall times, not utilisation).
- T4 — covers weakly: `-j$(nproc)` as the community tool's choice.
- T1, T2, T3, T5, T8 — does not cover. Not an observation.

---

### S3-13 — Chromium `post_build_ninja_summary.py`: the `.ninja_log` format and one documented example summary of a Chromium build (770 `.obj`, 37.7× parallelism)

**Citation.** The Chromium Authors, `post_build_ninja_summary.py`, depot_tools at `refs/heads/main`, https://chromium.googlesource.com/chromium/tools/depot_tools.git/+/refs/heads/main/post_build_ninja_summary.py (fetched with `?format=TEXT`, base64-decoded). Licence: BSD-style (file header lines 2–4).

**Copy.** `sources/S3-13-chromium-ninja-summary/post_build_ninja_summary.py` (`97f40f5028f4b8f9ebfd89618fe8a5a7be81139b9426aff026e637acd6dfd3db`), accessed 2026-09-14.

**Passages** (`post_build_ninja_summary.py:22-49`, the docstring's "Typical output"):
> `>ninja -C out\debug_component base`
> `ninja.exe -C out\debug_component base -j 960 -l 48  -d keeprsp`
> `Longest build steps:`
> `       0.1 weighted s to build obj/base/base/trace_log.obj (6.7 s elapsed time)`
> `       0.3 weighted s to build obj/base/base/win_util.obj (12.4 s elapsed time)`
> `       1.2 weighted s to build base.dll, base.dll.lib (1.2 s elapsed time)`
> `Time by build-step type:`
> `       0.2 s weighted time to generate 20 .o files (2.8 s elapsed time sum)`
> `       1.7 s weighted time to generate 4 PEFile (linking) files (2.0 s elapsed`
> `      23.9 s weighted time to generate 770 .obj files (974.8 s elapsed time sum)`
> `26.1 s weighted time (982.9 s elapsed time sum, 37.7x parallelism)`
> `839 build steps completed, average of 32.17/s`
> The "weighted" time is the elapsed time of each build step divided by the number of tasks that were running in parallel.

**Coverage.** T1/T2 — covers weakly: one example of per-step-type elapsed sums for a Chromium `base` target on Windows with a distributed backend (`-j 960`): 770 object compiles averaging 974.8/770 = 1.27 s wall each, 37.7× mean parallelism; machine unnamed; not Linux, not a local `-j`. T4 — the `-j 960 -l 48` shows a distributed-build setting, not a desktop choice. T3, T5–T8 — does not cover. Also the format authority for S3-08.

---

### S3-14 — ClangBuildAnalyzer README: an example `-ftime-trace` aggregate over 7,664 compilations of Blender (frontend 2,118.9 s vs backend 1,204.1 s; slowest files named)

**Citation.** Aras Pranckevičius, ClangBuildAnalyzer, `readme.md` at `55447756ff8af2f87e4a315f2ba637b9380363ea` (2025-03-21), https://github.com/aras-p/ClangBuildAnalyzer. Licence: Unlicense (`license.md`, not quoted).

**Copy.** `sources/S3-14-clangbuildanalyzer/readme.md` (`41396123362fce3e39156efda4d6b6c76cbfa03856cc7c66739f0e768ec0c474`), accessed 2026-09-14.

**Passages** (`readme.md:37-57`):
> The analysis output will look something like this:
> `Analyzing build trace from 'artifacts/FullCapture.bin'...`
> `**** Time summary:`
> `Compilation (7664 times):`
> `  Parsing (frontend):         2118.9 s`
> `  Codegen & opts (backend):   1204.1 s`
> `**** Files that took longest to parse (compiler frontend):`
> `  5084 ms: cycles_scene.build/RelWithDebInfo/volume.o`
> `  4471 ms: extern_ceres.build/RelWithDebInfo/covariance_impl.o`
> `**** Files that took longest to codegen (compiler backend):`
> ` 47123 ms: bf_blenkernel.build/RelWithDebInfo/volume.o`
> ` 39617 ms: bf_blenkernel.build/RelWithDebInfo/volume_to_mesh.o`

`readme.md:21-25`:
> As long as it invokes Clang and passes `-ftime-trace` flag to the compiler (**Clang 9.0 or later is required** for this).
> … (Clang `-ftime-trace` produces one JSON file next to each object file) …

**Computed (arithmetic on the quoted summary).** 7,664 compilations, (2118.9 + 1204.1) / 7664 = 0.434 s mean in-compiler time per TU; frontend share 63.8 %.

**Coverage.** T2 — covers weakly: a per-project aggregate of clang's own in-process timing (frontend vs backend) with the slowest TUs (up to 47 s codegen) for Blender (`RelWithDebInfo`, macOS paths — `kernel.mm`), machine and date unnamed, a single excerpt. T1, T3–T8 — does not cover.

---

### S3-15 — tests.reproducible-builds.org: build history of the Debian `linux` package on named build nodes (durations per rebuild), and the network's performance page

**Citation.** Reproducible Builds (Debian), *build history of linux*, https://tests.reproducible-builds.org/debian/history/linux.html; *Build network performance stats*, https://tests.reproducible-builds.org/debian/index_performance.html; node list https://tests.reproducible-builds.org/debian/index_nodes_health.html. Terms: project CI pages, public.

**Copy.** `sources/S3-15-reproducible-builds/`: `history-linux.html` (`16034642dbf9b9b81b12815f7231c713eed82c2cddf4513dbe6b7a865a8145e0`), `index_performance.html` (`431f51cb29bad6d0306a7265b8b4f5fea2ba4d535f335b00f9204ed865e140c1`), `index_nodes_health.html` (`d0bfede7aeedda01c047237ae802fa73dad7de438b1ca3e6a7d90db60d292a4e`); accessed 2026-09-14.

**Passages.**

history-linux (table header, text lines 4–12, then rows 13–…):
> `build date` / `version` / `suite` / `architecture` / `result` / `build duration` / `node1` / `node2` / `job`
> `2026-09-13 19:08:00` / `6.12.107-1` / `trixie` / `arm64` / `FTBFS` / `2h 46m 34s` / `codethink04-arm64` / `codethink03-arm64` / `arm64_8/150753`
> `2026-09-12 17:01:00` / `6.12.107-1` / `trixie` / `amd64` / `reproducible` / `7h 58m 46s` / `ionos5-amd64` / `ionos11-amd64` / `amd64_32/102508`

index_performance (text):
> `average test duration (on 2026-09-13)` / `13 min., 9 sec.` / `12 min., 52 sec.` (amd64 / arm64 columns) … `packages tested yesterday (2026-09-13)` / `4121` / `947`

index_nodes_health lists the amd64 nodes by name only (`ionos1`, `ionos5 (r-b Debian builds)`, `ionos11 (r-b Debian builds)`, `ionos15`, `infom01`, `infom02`, …); no hardware description on the page.

**Computed (file `history-linux.html`; regex over `<tr>…<td>` cells; duration parsed as `(\d+)h (\d+)m (\d+)s`).** 3,497 rows. amd64 builds with result `reproducible`: n 282, duration min 10,153 s, median 26,571 s (7 h 23 m), max 104,350 s; `unreproducible`: n 734, median 29,908 s; `build timeout`: n 27 at ≈64,860 s (the 18 h limit). The six most recent amd64 `reproducible` rows: `6.12.107-1 7h 58m 46s ionos5/ionos11`, `7.2.3-1~exp1 8h 9m 31s infom01/infom02`, `7.1.12-1 7h 9m 48s infom02/infom01`, `7.1.13-1 7h 20m 16s infom01/infom02`, `7.1.12-1 9h 18m 28s ionos5/ionos11`, `7.2.2-1~exp1 6h 49m 51s ionos11/ionos5`. A reproducibility test builds the package twice (node1, node2), so a "build duration" spans two full kernel package builds under the varied environment; it is not one `make` run.

**Coverage.** T6 — covers, weakly: kernel-package wall times on named CI nodes (hardware not described on the fetched pages; the same `linux` 7.1.13-1 that took 2 h 39 m on the Debian buildd at `parallel=6` (S3-03) takes 7 h 20 m for a double build here). T4 — does not cover (the `parallel=` used by the r-b builders is not on these pages). T1, T2, T3, T5, T7, T8 — does not cover.

**One observation?** A series of builds on a handful of named nodes; machine hardware unnamed; project and windows named. Not a desktop.

---

### S3-16 — Blender Open Data snapshot 2020-01-08: 6,246 Linux CPU render-benchmark results (threads used, CPU model, per-scene render time)

**Citation.** Blender Foundation, *Blender Open Data*, snapshot `opendata-2020-01-08-063356+0000.zip` from https://opendata.blender.org/snapshots/ (listed there as `27-Jun-2022 11:27 2018885`), containing `README.txt`, `LICENSE.txt`, `opendata-2020-01-08-063356+0000.jsonl.bz2`. Licence (README): "The data in this archive is licensed under the *Creative Commons 0* license." Newer data is only served through a JS front end (`/benchmarks/query/…` returns a JS shell); the 2018 and 2020 zips are the only raw dumps listed.

**Copy.** `sources/S3-16-blender-opendata/`: `opendata-2020-01-08-063356+0000.zip` (`5d4b46dda93d2d8ebadb70126ffde4b5b19bfc2aa13b9e2efa8a95ae3fdb938e`), `README.txt` (`9eb32de45e7c967d49f87cd373107600cc9d5b72e1c1160bb36ab00d6da33fbd`), `LICENSE.txt` (`a2010f343487d3f7618affe54f789f5487602331c0a8d03f49e9a7c547cf0499`), `snapshots-index.html`; the decompressed `.jsonl` (35,793 lines) has SHA-256 `9cb841d1673e5ac9b565ddeb6a7874037db02f2d077e4831f6e206a004f00327` and is not stored (reproducible from the zip); accessed 2026-09-14.

**Passages.**

`README.txt`:
> This archive contains a direct dump of [Blender Open Data](https://opendata.blender.org/). The data itself is contained in the `xxxx.jsonl.bz2` file. This is a BZip2-compressed text file, and contains a JSON-formatted document on each line.

First record of the `.jsonl` (fields relevant here; this record is a CUDA one and is shown for the schema):
> `"scene": {"name": "bmw27", "stats": {"result": "OK", "total_render_time": 164.723, "device_peak_memory": 142.45, "device_memory_usage": 142.45, "render_time_no_sync": 155.22, "pipeline_render_time": 167.42000000000002}}` … `"device_info": {"device_type": "CUDA", "compute_devices": [{"name": "GeForce GTX 1060 3GB", "type": "CUDA", "is_display": false}], "num_cpu_threads": 4}` … `"system_info": {"system": "Linux", "bitness": "64bit", …, "cpu_brand": "AMD Phenom(tm) 9650 Quad-Core Processor", "dist_name": "debian", "dist_version": "9.0", "num_cpu_cores": 4, "num_cpu_sockets": 1, "num_cpu_threads": 4}` … `"blender_version": {"version": "2.79 (sub 1)", …}`

**Computed (python over the `.jsonl`; `device_info.device_type == "CPU"` and `system_info.system == "Linux"`; quantile = sorted value at ⌊p·n⌋).** 35,793 records: CPU 19,622, CUDA 10,633, OPENCL 5,538. Linux CPU records 6,246 (Windows 12,908, Darwin 468), timestamps 2017-08-26 … 2020-01-08, Blender 2.79 (sub 0/1/2) for all but 5. `device_info.num_cpu_threads` equals `system_info.num_cpu_threads` in 6,246 of 6,246 records, i.e. the benchmark used every logical CPU. Thread-count distribution of the Linux CPU records: 2:24, 4:264, 6:56, 8:1,201, 12:669, 16:1,216, 20:841, 24:208, 28:6, 32:636, 40:34, 44:848, 48:44, 56:6, 64:150, 72:6, 80:12, 96:13, 112:4, 128:2, 160:6. `total_render_time` (s) per scene, `result == "OK"`: `bmw27` n 1,354 p10 116 / p50 224 / mean 384 / p90 720 / max 17,797; `classroom` n 1,346 p50 707 / p90 2,312; `fishy_cat` n 799 p50 285; `koro` n 800 p50 417; `pavillon_barcelona` n 801 p50 567; `barbershop_interior` n 603 p50 835 / p90 2,449; `victor` n 526 p50 1,427. Restricted to 8-thread Linux machines, `bmw27`: n 281, p10 444 / p50 551 / p90 784 s. Most frequent CPUs: `Intel(R) Xeon(R) CPU E5-2699 v4 @ 2.20GHz` 848, `Intel(R) Core(TM) i7-6950X CPU @ 3.00GHz` 811, `Intel(R) Core(TM) i7-2600K CPU @ 3.40GHz` 603, `AMD Ryzen 7 1800X Eight-Core Processor` 602, `AMD Ryzen Threadripper 1950X 16-Core Processor` 514 (the population is skewed by a few heavy submitters).

**Coverage.**
- T7 — covers: a CPU-saturating desktop batch job (Cycles render) characterised by thread count (= all logical CPUs, per record), duration per scene (seconds, distributions above) and machine (CPU model, cores, sockets, OS/distribution) for 6,246 Linux runs; no utilisation time series (the benchmark records only total times). Population: self-submitted 2017–2020 Blender 2.79 results, dominated by a few users' machines; sampled/partial in that sense.
- T1–T6, T8 — does not cover.

**One observation?** No — 6,246 runs on ≈ hundreds of distinct machines (CPU brand strings counted above), each run's machine and window (timestamp, scene) named in its record.

## 3. Not found

- **T1, a per-process trace of a full parallel build (every `cc1`/`as`/`ld`/`sh`/`fixdep` with lifetime and CPU at exit).** Not found. The closest is the 1-second `perf sched` excerpt in S3-01 (21 `cc1`, 18 `gcc`, 6 `fixdep`, 7 `recordmcount` processes visible; no lifetimes). Searches: rows 4 (execsnoop/exitsnoop examples — none show a build), 6, 28, 29; GitHub code search returns only copies of Gregg's article. The Yocto buildstats (S3-05) fold all children of a task into one rusage; the Debian log (S3-03) gives invocation counts only.
- **T2, CPU-time distribution across a kernel build and blocked-time under cold vs warm cache.** Not found for gcc/kernel. Found instead: per-TU clang CPU/wall for CTMark at `-O3` etc. (S3-09; task-clock/wall ≈ 0.99 at `-O3`, 0.59–0.82 under ThinLTO), per-edge ninja wall times for LLVM (S3-08, wall only, machine unnamed), a Blender `-ftime-trace` aggregate (S3-14). No dataset records a cold-cache case; no dataset splits a compiler's lifetime into run/wait. Rows 2, 3, 11, 25–26.
- **T4, an observation of what `-j` users actually pick.** Not found: no survey or poll exists in the results (row 16); the Gentoo forum thread is behind a login (row 32, copy of the login page saved). Found instead: build-farm settings — Debian buildd `parallel=6` (S3-03), Fedora koji `-j64` on 64 CPUs (S3-04), Yocto perf host `-j 16 -l 75` (S3-05), DKMS `-j8` on an 8-thread desktop (S3-06), and the LLVM tracker's "nproc + 2 … Limit to nproc - 1 to reduce noise" (S3-09).
- **T5, a measured DKMS autoinstall with CPU and process counts.** Only S3-06 (one `make.log` with `-j8`, 208 objects, 58 s to failure, i7-4790) and the unmeasured S3-07 claim. Launchpad's `dkms` package bug list search for `make.log` gives four old bugs without timing (row 20); bug #2115002 carries no `make.log` (row 19). bugzilla.redhat.com and bugs.debian.org are reachable (row 15) but were not searched for DKMS timing after the Launchpad log satisfied the invocation question; recorded as a limit of this pass.
- **T6, process-lifetime distributions on Unix/Linux desktops.** Not found as a dataset: the Harchol-Balter/Downey traces are not published on the author's page (row 10). Google/LANL cluster traces were not pursued (not desktops). Kernel-build-as-scheduler-workload: definitions found (S3-11, S3-12) and wall times (S3-03, S3-04, S3-05, S3-10, S3-15); no published sched-ext benchmark table with kernel build times (row 36: the only public archive contains hackbench/cyclictest/stress-ng only). Phoronix's thread-count sweep exists but its result pages are 403 (row 23).
- **T7, sustained utilisation and thread counts of an antivirus scan, a video encode, a training loop, an indexer rescan.** Only Blender CPU renders (S3-16) give thread counts and durations; encoders/ClamAV/PyTorch/tracker: only tool definitions (S3-11) and unmeasured complaints (rows 13, 17, 33, 34, 35). openbenchmarking.org result pages (which would give x264/SVT-AV1 per-machine FPS) are blocked (403), and they would not give utilisation either.
- **Chromium build statistics** (ninja logs of real Chromium builds): chromium-build-stats.appspot.com requires a Google sign-in (row 3); only the docstring example (S3-13) was obtainable.
- **T3 and T8** — no dataset covers them; nothing was searched for them by this reader (out of class).
