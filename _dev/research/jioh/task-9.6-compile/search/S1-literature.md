# S1 — peer-reviewed and preprint literature (T1, T2, T3, T6, T7)

Reader: S1. Date of all searches and accesses: 2026-09-14. Source copies under `sources/S1-<id>/` (PDF or HTML plus a `pypdf` / own tag-stripping text extraction, `.txt` next to the copy). Only `input.md` and my own `S1-` folders were read; other readers' folders under `sources/` were not opened. T4, T5 and T8 are outside my class; I note them only where a paper happens to touch them.

Extraction notes. Page numbers are PDF page numbers from `pypdf`; where the copy carries printed proceedings page numbers I give both ("PDF p. 8 / printed 383"). Ligatures (ﬁ, ﬂ) in the extracted text are written as plain letters; a minus sign that the extraction rendered as "2" (Harchol-Balter, S1-07) is written as "−" and flagged. HTML copies (S1-08, S1-10, S1-25) have no pages; the locator is the section heading. Anything I computed myself is labelled "my computation".

Working conditions worth recording: a shared `sources/_probe/` staging folder I used at first was deleted by another process mid-session (the `sources/` tree is shared with the other class readers) and the disk filled up once; every copy cited below was re-fetched into its own `S1-<id>/` folder afterwards and the SHA-256 given is of that re-fetched file (`sources/_S1-tools/SHA256SUMS.txt` holds the list).

## 1. Search log

| # | Date | Engine / venue | Exact query or URL | Hits followed | Dead ends (HTTP status) |
|---|------|----------------|--------------------|---------------|-------------------------|
| 1 | 2026-09-14 | curl (direct URL probe, 12 URLs) | arxiv.org/pdf/1705.05937; usenix …/atc17/atc17-ocallahan.pdf; arxiv.org/pdf/1203.2704; arxiv.org/pdf/2509.01245; cs.cmu.edu/~harchol/Papers/tocs.pdf; usenix …/osdi10/…/Boyd-Wickizer.pdf; microsoft.com …/build-systems.pdf; microsoft.com …/fork-hotos19.pdf; usenix …/fast17-vangoor.pdf; usenix …/hotcloud19-paper-young.pdf; parsec.cs.princeton.edu/doc/parsec-report.pdf; cs.cmu.edu/~harchol/Papers/sigmetrics96.pdf | 200: rr arXiv (S1-01), Coetzee (S1-03), SchedCP (S1-04), Boyd-Wickizer (S1-02), Mokhov build-systems (read, discarded — no timing or process data), fork-hotos19 (S1-11), FUSE FAST'17 (read, discarded — no compile workload), gVisor HotCloud'19 (read, discarded — no compile workload) | atc17-ocallahan.pdf 404 (correct name has an underscore, row 7); harchol tocs.pdf 404; sigmetrics96.pdf 404 (case-sensitive, row 2); parsec-report.pdf: proxy CONNECT 502 |
| 2 | 2026-09-14 | WebSearch | `"Exploiting process lifetime distributions for dynamic load balancing" Harchol-Balter Downey pdf` | users.soe.ucsc.edu …/harcholbalter-tocs97.pdf and cs.cmu.edu/~harchol/Papers/Sigmetrics96.pdf (S1-07) | — |
| 3 | 2026-09-14 | WebSearch | `paper measurement "kernel compile" OR "kernel build" "fork" "exec" process count benchmark "make -j" processes created` | es.tldp.org …/blanchard/talk_2.html (S1-08) | kcbench man pages, forum posts (not literature) |
| 4 | 2026-09-14 | WebSearch | `GNU make jobserver overhead parallel build scalability measurement paper thesis "make -j"` | none academic | GNU make manual, mad-scientist.net jobserver page, blogs (S2 territory) |
| 5 | 2026-09-14 | WebSearch | `empirical study C++ compile time per translation unit distribution "-ftime-trace" OR "-ftime-report" paper arXiv` | none | unrelated arXiv hits (code translation, CQ metric) |
| 6 | 2026-09-14 | curl (direct URL probe, 11 URLs) | ucsc harcholbalter-tocs97.pdf; cmu Sigmetrics96.pdf; usenix atc17-o_callahan.pdf; microsoft …/q_icse16.pdf; people.ece.ubc.ca/sasha/papers/eurosys16-final29.pdf; cs.princeton.edu/~cbienia/papers/parsec-pact08.pdf; fsl.cs.stonybrook.edu/docs/fuse/fuse-tos19.pdf; fsl.cs.sunysb.edu …; es.tldp.org …/talk_2.html; usenix nsdi10-cha.pdf; usenix legacy …/cha.pdf | 200: TOCS'97 + SIGMETRICS'96 (S1-07), rr ATC'17 (S1-01), Lozi EuroSys'16 (S1-06), Blanchard (S1-08), SplitScreen NSDI'10 (read, discarded — ClamAV signature-matching throughput, no scan-job CPU/thread characterisation) | q_icse16.pdf 404; parsec-pact08.pdf 404; fuse-tos19.pdf 404 (both hosts); nsdi10-cha.pdf 404 |
| 7 | 2026-09-14 | WebSearch | `"Engineering Record and Replay for Deployability" USENIX ATC 2017 pdf O'Callahan` | usenix.org/conference/atc17/…/ocallahan; arXiv 1705.05937 | dl.acm.org (403 for this container) |
| 8 | 2026-09-14 | WebSearch | `Esfahani "CloudBuild: Microsoft's distributed and caching build service" ICSE 2016 pdf` | microsoft.com …/2016/06/q_signed-2.pdf — fetched and read; discarded: distributed CI service, no per-process/per-action timing (only "critical path" scatter figures) | — |
| 9 | 2026-09-14 | WebSearch | `x264 encoder thread scaling CPU utilization multicore characterization paper parallel speedup frames threads` | none open (ResearchGate H.264 papers) | forum posts; x265 docs (S2 territory) |
| 10 | 2026-09-14 | WebSearch | `antivirus scan CPU overhead measurement paper ClamAV performance scanning throughput characterization` | Al-Saleh & Hamdan JUCS 2019 (fetched, read, discarded — file-system-operation latencies under on-access AV, no full-scan job); Hash-AV (crypto.stanford.edu, fetched, read, discarded — signature-matching throughput MB/s, no thread/utilisation data) | ResearchGate copies 403 |
| 11 | 2026-09-14 | WebSearch | `Linux scheduler evaluation paper "kernel compile" OR "kernel build" workload "-j" EEVDF OR CFS OR sched_ext arXiv 2024 2025` | arXiv 2509.01245 (S1-04); liu.diva-portal.org …/diva2:1972665 (Linköping thesis) | diva-portal: curl "Connection reset by peer" ×2, WebFetch 503 — not read |
| 12 | 2026-09-14 | WebSearch | `Unix process lifetime distribution measurement study Leland Ott 1986 "Load-balancing heuristics and process behavior" pdf` | no open copy of Leland & Ott | dl.acm.org only (403) |
| 13 | 2026-09-14 | WebSearch | `"The PARSEC benchmark suite: characterization and architectural implications" pdf Bienia x264 threads` | parsec.cs.princeton.edu/doc/parsec-report.pdf (proxy 502 ×3); cs.princeton.edu/techreports/2008/811.pdf 200 (S1-14, the TR version) | ResearchGate/academia copies not tried (login walls) |
| 14 | 2026-09-14 | WebSearch | `"Precise Performance Characterization of Antivirus on the File System Operations" pdf` | jucs.org PDF (read, discarded, see row 10); cs.unm.edu/~csgsa/…/MohammedAl-saleh.pdf (S1-13) | — |
| 15 | 2026-09-14 | WebSearch | `predicting compilation time C C++ source files machine learning paper "compile time" per file prediction empirical` | none on per-file compile time | compiler-optimisation ML papers (off-topic) |
| 16 | 2026-09-14 | WebSearch | `"Recursive Make Considered Harmful" Miller 1998 pdf AUUG` | aegis.sourceforge.net/auug97.pdf (S1-09) | — |
| 17 | 2026-09-14 | WebSearch | `cost of fork exec Linux measurement paper process creation latency microbenchmark "posix_spawn" OR "vfork" evaluation` | arXiv 2509.09439 (μFork, SOSP'25) fetched and read — discarded: single-address-space OS, no build workload | LWN articles (S2 territory) |
| 18 | 2026-09-14 | WebSearch | `"Performance and Resource Utilization of FUSE User-Space File Systems" pdf Vangoor Zadok ACM TOS 2019` | fsl.cs.stonybrook.edu/docs/fuse/fuse-tos19-a15-vangoor.pdf fetched (49 pp.) and grepped — discarded: no compile workload | — |
| 19 | 2026-09-14 | WebSearch | `process lifetime distribution Linux measurement study heavy-tailed "process lifetimes" desktop workstation trace 2000s paper` | nothing beyond Harchol-Balter & Downey | unrelated statistics papers |
| 20 | 2026-09-14 | WebSearch | `deep learning training on desktop CPU utilization characterization paper threads "CPU utilization" PyTorch OR TensorFlow CPU-only training benchmark cores` | arXiv 2309.02521 (S1-17) | IEEE Xplore cluster-DNN paper (paywalled) |
| 21 | 2026-09-14 | WebSearch | `"Characterizing antivirus workload execution" Uluski Moffie Kaeli pdf` | ResearchGate PDF link → 403; kipdf mirror → 403 | dblp record only |
| 22 | 2026-09-14 | WebSearch | `scheduler paper "Linux kernel" compile "build" benchmark "make -j" sched_ext OR "scx" arXiv evaluation "kernel compilation" cores time` | arXiv 2511.11628 (S1-12) | eunomia blog, openbenchmarking (403), kernel docs (S2) |
| 23 | 2026-09-14 | WebSearch | `paper "compile time" distribution "translation units" OR "source files" LLVM OR Chromium OR "Linux kernel" build profiling per-file "seconds" study 2019..2025 arXiv OR ICSE OR MSR` | none academic | blogs (randomascii Chromium build times), CompileScore, ctbench JOSS (tool paper, no measurement) |
| 24 | 2026-09-14 | WebSearch | `"kernel compile" OR "kernel build" workload measured "number of processes" OR "processes" "fork" "exec" "syscall" characterization paper "make" build I/O system call trace study` | arXiv 2606.25189 ActPlane (S1-24); arXiv 2304.08569 DIO (fetched, read, discarded — no build workload) | tutorials, patents |
| 25 | 2026-09-14 | WebSearch | `Google Scholar "parallel make" OR "make -j" speedup scalability study build dependency graph critical path paper "build systems" ICSE MSR empirical build duration` | arXiv 2405.00796 (Bazel CI study; fetched, read, discarded — CI-level durations, no process data) | patents |
| 26 | 2026-09-14 | WebSearch | `"autogroup" OR "child runs first" OR "sched_child_runs_first" Linux scheduler paper evaluation "kernel build" desktop interactivity study` | none academic (man pages, LKML, kernel source — S2 territory) | — |
| 27 | 2026-09-14 | WebSearch | `paper "distcc" OR "ccache" OR "icecream" distributed compilation evaluation "Linux kernel" compile time per file measurements gcc "cc1" preprocessing assembler` | none academic | tool docs, blogs |
| 28 | 2026-09-14 | WebSearch | `"page cache" cold warm build time compilation I/O bound CPU bound study "kernel compile" OR "compile" filesystem benchmark paper "compile phase" OR "compilation phase" iozone OR filebench OR "postmark" OR "compilebench"` | fsl.cs.stonybrook.edu/docs/fsbench/ (Traeger et al., S1-26, via row 50) | — |
| 29 | 2026-09-14 | WebSearch | `arXiv paper x264 OR ffmpeg video transcoding CPU cores utilization desktop benchmark "thread" scaling characterization 2020..2026` | arXiv 2110.11462 (S1-15); arXiv 2005.02947 (S1-16) | vendor briefs (Ampere, Intel) |
| 30 | 2026-09-14 | WebFetch | liu.diva-portal.org/smash/get/diva2:1972665/FULLTEXT01.pdf | — | 503 |
| 31 | 2026-09-14 | Google Scholar (WebFetch) | `"make -j" jobserver parallel build overhead` | Belinassi, Biener, Hubička et al., "Compiling Files in Parallel: A Study with GCC", SBAC-PADW 2022 — identified, not read (row 41, 51) | — |
| 32 | 2026-09-14 | WebSearch | `"Characterizing antivirus workload execution" Uluski 2005 pdf site:ece.neu.edu OR site:coe.neu.edu OR site:semanticscholar.org` | none | patents |
| 33 | 2026-09-14 | WebSearch | `file system paper evaluation "kernel compile" OR "Linux build" macrobenchmark "processes" spawned "fork" count "exec" count BetrFS OR Strata OR SplitFS OR "Nine Year Study"` | pointer to Traeger et al. (S1-26) | SplitFS/Strata (no compile process counts) |
| 34 | 2026-09-14 | WebSearch | `"desktop search" OR "file indexer" full index rescan CPU cost measurement paper Recoll OR Tracker OR "Windows Search" OR Spotlight indexing performance study` | none academic | MS Learn troubleshooting page, patents |
| 35 | 2026-09-14 | WebSearch | `ninja build system "make" startup time comparison paper OR thesis evaluation "job scheduling" build tool "critical path" scheduling "compile jobs" duration distribution measurement` | aosabook.org/en/posa/ninja.html (S1-10, book chapter) | blogs, build2 post |
| 36 | 2026-09-14 | arXiv API (curl) | `export.arxiv.org/api/query?search_query=all:%22kernel%20compilation%22%20AND%20all:scheduler&max_results=25` | — | 429 rate-limited on four attempts spread over ~30 minutes (first probe of the endpoint returned 200) |
| 37 | 2026-09-14 | Google Scholar (WebFetch) | `"process lifetime" distribution Linux measurement trace desktop` | Flautner, Uhlig, Reinhardt 2000 "Thread-level parallelism of desktop applications" (umich PDF: curl TLS "unable to get local issuer certificate" — not read) | availability-modelling papers (off-topic) |
| 38 | 2026-09-14 | Google Scholar (WebFetch) | `"kernel compile" OR "kernel build" benchmark "processes" fork exec "short-lived" measurement` | usenix atc20-gouicem.pdf (S1-05); static.russross.com/papers/cs261.pdf (S1-23) | — |
| 39 | 2026-09-14 | Google Scholar (WebFetch) | `antivirus "full scan" OR "on-demand scan" CPU utilization duration measurement` | Dogonyaro et al. 2020 (irepo.futminna.edu.ng:8080 — curl timeout 120 s, then 000) — not read; Vashishtha 2023 NCIRL thesis (server AV, not pursued) | — |
| 40 | 2026-09-14 | Google Scholar (WebFetch) | `"compile time" per "translation unit" distribution empirical C++ headers study` | usenix Krishnaswamy 2000 (S1-22); Kubota, Suzuki, Kono CC 2019 (row 45) | — |
| 41 | 2026-09-14 | WebSearch | `Belinassi Biener Hubička "Compiling files in parallel: A study with gcc" 2022 pdf arXiv OR ime.usp.br` | none open | IEEE Xplore (paywalled), computer.org, ResearchGate |
| 42 | 2026-09-14 | Google Scholar (WebFetch) | `x264 encoder threads "CPU utilization" multicore scaling measurement PARSEC` | none usable | Caladan, SmartBoost etc. (off-topic) |
| 43 | 2026-09-14 | Google Scholar (WebFetch) | `"Linux kernel" build "make -j" "number of processes" OR "processes created" measurement scheduler evaluation` | Zheng & Nieh (S1-19); Antfarm USENIX'06 (S1-18); Groves et al. (S1-20); Nikseresht arXiv 1012.3452 (S1-21); Chandra OSDI'00 (S1-25) | Kozak MIT thesis 2020, Saubhasik 2008, Shao 2009, Gonzalez-Ferez 2007 (not pursued: `make -j` used only as background load, no process data in snippets) |
| 44 | 2026-09-14 | Google Scholar (WebFetch) | `"Characterizing antivirus workload execution"` | dl.acm.org/doi/pdf/10.1145/1055626.1055639 | 403 (row 51) |
| 45 | 2026-09-14 | WebSearch | `Kubota Suzuki Kono "To unify or not to unify" unified builds WebKit 2019 pdf` | tk1012.github.io (WebFetch: no PDF link, ACM only) | dl.acm.org/doi/pdf/10.1145/3302516.3307347 → 403 (row 51) |
| 46 | 2026-09-14 | WebSearch | `Giuliano Belinassi thesis "GCC" parallel compilation USP teses.usp.br pdf "make -j" jobserver` | gcc.gnu.org mailing-list posts only (S2/primary territory) | no thesis PDF located |
| 47 | 2026-09-14 | WebFetch | https://tk1012.github.io/ | — | no PDF; ACM/IEEE/J-Stage links only |
| 48 | 2026-09-14 | Google Scholar (WebFetch) | `"compilation time" "long tail" OR "distribution of compile times" source files build profiling C C++` | none on-topic (FPGA/ML compilers) | — |
| 49 | 2026-09-14 | Google Scholar (WebFetch) | `"GNU make" "jobserver" OR "-j" parallel build overhead measurement dissertation build parallelism` | Van Veen 2013 gold thesis, Grosskurth 2007, Ammons 2006 (not pursued: linker/rebuild-correctness topics) | — |
| 50 | 2026-09-14 | Google Scholar (WebFetch) | `"kernel build" OR "kernel compile" "cold cache" "warm cache" I/O bound CPU bound build time file system evaluation` | Traeger et al. TOS 2008 → fsl.cs.stonybrook.edu/docs/fsbench/fsbench.pdf 200 (S1-26) | fsbench-tos.pdf 404 |
| 51 | 2026-09-14 | curl (paywall probes) | irepo.futminna.edu.ng:8080 …/7.1.pdf; kipdf.com …uluski; dl.acm.org/doi/pdf/10.1145/1055626.1055639; ieeexplore.ieee.org/document/9978516/; dl.acm.org/doi/pdf/10.1145/3302516.3307347; researchgate.net …Characterizing-antivirus-workload-execution.pdf | — | timeout/000; 403; 403; 202 (bot page, no PDF); 403; 403 |
| 52 | 2026-09-14 | Google Scholar (WebFetch) | `"ninja" OR "cargo" build system jobserver "-j" parallelism measurement paper 2020..2026` | — | "did not match any articles" |
| 53 | 2026-09-14 | Google Scholar (WebFetch) | `compiler process "I/O wait" OR "blocked on I/O" OR "iowait" build "page cache" compilation CPU-bound measurement` | none on-topic | — |
| 54 | 2026-09-14 | dblp API (curl) | `dblp.org/search/publ/api?q=parallel%20make%20build%20jobserver&format=json` | — | 200 but body is an Anubis "Making sure you're not a bot" page, no JSON |
| 55 | 2026-09-14 | curl (Scholar-derived direct downloads) | academiccommons.columbia.edu/doi/10.7916/D8891DPX/download; usenix legacy …/usenix06/…/jones.pdf; cs.unm.edu/~eschulte/…/bfs-v-cfs_groves-knockel-schulte.pdf; arxiv.org/pdf/1012.3452; usenix legacy …/wiess2000/…/krishnaswamy.pdf; usenix …/osdi2000/full_papers/chandra/chandra_html/index.html; static.russross.com/papers/cs261.pdf; usenix …/atc20-gouicem.pdf; cs.princeton.edu/techreports/2008/811.pdf | all 200 (S1-19, S1-18, S1-20, S1-21, S1-22, S1-25, S1-23, S1-05, S1-14) | — |

## 2. Candidates

### S1-01 — O'Callahan, Jones, Froyd, Huey, Noll, Partush, "Engineering Record and Replay for Deployability", USENIX ATC '17 (+ arXiv extended report)

- **Citation.** Robert O'Callahan, Chris Jones, Nathan Froyd, Kyle Huey, Albert Noll, Nimrod Partush. *Engineering Record And Replay For Deployability.* 2017 USENIX Annual Technical Conference (USENIX ATC '17), Santa Clara, July 12–14, 2017, pp. 377–393. Extended technical report: arXiv:1705.05937v1 [cs.PL], 16 May 2017.
- **Copy read.** (a) `https://www.usenix.org/system/files/conference/atc17/atc17-o_callahan.pdf`, as served 2026-09-14, 15 pages; local `sources/S1-01/rr-atc17.pdf`; SHA-256 `589ec37978260f968312288061e710e64b58e2e652c8479649694403ac037772`. (b) `https://arxiv.org/pdf/1705.05937` (stamp "arXiv:1705.05937v1 [cs.PL] 16 May 2017"), 20 pages; local `sources/S1-01/rr-arxiv-1705.05937v2.pdf` (file name is mine; the content is v1); SHA-256 `f348cc0a1fea3665edab4310208b57b896cf7fbac763e502a51fa7e688794e21`. The §4 text is identical in both; locators below are for the ATC copy, with the arXiv page in brackets.
- **Passages.**
  - §4.1 Workloads, PDF p. 8 / printed 383 [arXiv p. 11]: "Benchmarks were chosen to illuminate RR's strengths and weaknesses, while also containing representatives of real-world usage. They were tuned to fit in system memory (to minimize the impact of I/O on test results), to run for about 30 seconds each (except for cp where a 30s run time would require it to not fit in memory)."
  - §4.1, p. 8 / 383 [arXiv p. 11]: "make builds DynamoRio [8] (version 6.1.0) with make -j8 (-j8 omitted when restricting to a single core). This tests potentially-parallel execution of many short-lived processes."
  - §4.1, p. 8 / 383 [arXiv p. 12]: "All tests run on a Dell XPS15 laptop with a quad-core Intel Skylake CPU (8 SMT threads), 16GB RAM and a 512GB SSD using Btrfs in Fedora Core 23 Linux."
  - §4.2, p. 8 / 383 [arXiv p. 12]: "Each test was run six times, discarding the first result and reporting the geometric mean of the other five results. Thus the results represent warm-cache performance."
  - §4.3 Observations, p. 8 / 383 [arXiv p. 12]: "Overhead on make is significantly higher than for the other workloads. Forcing make onto a single core imposes major slowdown. Also, make forks and execs 2430 processes, mostly short-lived. (The next most prolific workload is sambatest with 89.) In-process system-call interception only starts working in a process once the interception library has been loaded, but at least 80 system calls are performed before that completes, so its effectiveness is limited for short-lived processes."
  - Table 1 "Run-time overhead", p. 9 / 384 [arXiv p. 12], row for make (columns: Baseline duration, Record, Replay, Single core, Record no-intercept, Replay no-intercept, Record no-cloning, DynamoRio-null): "make 20.99s 7.85× 11.93× 3.36× 11.32× 14.36× 7.84× 10.97×"
  - §4.3, p. 9 / 384: "octane is the only workload here other than make making significant use of multiple cores, and this accounts for the majority of RR's overhead on octane."
- **Coverage.**
  - T1: covers, one number. Object: processes forked-and-exec'd by a `make -j8` build of DynamoRio 6.1.0 (C/C++, CMake-generated Makefiles — the paper does not say which generator); unit: process count per build; statistic: total (2430) and the qualitative "mostly short-lived"; scope: one build on one laptop; no breakdown by process type (compiler driver / cc1 / as / ld / shell) and no lifetime distribution. My computation: 2430 processes / 20.99 s baseline ≈ 116 process creations per second on average.
  - T2: partial. The "single core" column shows the same build on one core takes 3.36× the wall time of the 8-thread build (my reading of Table 1: 20.99 s × 3.36 ≈ 70.5 s); no per-compile CPU time, no I/O blocking measurement; tests were "tuned to fit in system memory" and are "warm-cache".
  - T3: does not cover (make's own cost not separated).
  - T4: mentions `-j8` on a 4-core/8-thread laptop (`-j` = SMT-thread count); no rationale given.
  - T5, T8: do not cover.
  - T6: covers as a workload description: a parallel build used as a "potentially-parallel execution of many short-lived processes" test; machine, project, version and `-j` named.
  - T7: does not cover.
- **One observation?** Yes: one build (DynamoRio 6.1.0, `make -j8`), one machine (Dell XPS15, quad-core Skylake, 8 SMT threads, 16 GB, SSD/Btrfs, Fedora 23), window = the ~21 s build, repeated six times.

### S1-02 — Boyd-Wickizer, Clements, Mao, Pesterev, Kaashoek, Morris, Zeldovich, "An Analysis of Linux Scalability to Many Cores", OSDI 2010

- **Citation.** Silas Boyd-Wickizer, Austin T. Clements, Yandong Mao, Aleksey Pesterev, M. Frans Kaashoek, Robert Morris, Nickolai Zeldovich. *An Analysis of Linux Scalability to Many Cores.* 9th USENIX Symposium on Operating Systems Design and Implementation (OSDI '10), Vancouver, October 2010. 16 pages.
- **Copy read.** `https://www.usenix.org/legacy/events/osdi10/tech/full_papers/Boyd-Wickizer.pdf`, as served 2026-09-14; local `sources/S1-02/boyd-wickizer-osdi10.pdf`; SHA-256 `f5a618044994b7dc0824064b918fc5a6502bbd44509520eb4a87744fbd69f4cc`. PDF page = printed page.
- **Passages.**
  - §1, p. 1: "First we measure scalability of the MOSBENCH applications on a recent Linux kernel (2.6.35-rc5, released July 12, 2010) with 48 cores, using the in-memory tmpfs file system to avoid disk bottlenecks. gmake scales well, but the other applications scale poorly, performing much less work per core with 48 cores than with one core."
  - §3.5 Parallel build, p. 4: "gmake [23] is an implementation of the standard make utility that supports executing independent build rules concurrently. gmake is the unofficial default benchmark in the Linux community since all developers use it to build the Linux kernel. Indeed, many Linux patches include comments like “This speeds up compiling the kernel.” We benchmarked gmake by building the stock Linux 2.6.35-rc5 kernel with the default configuration for x86_64. gmake creates more processes than there are cores, and reads and writes many files. The execution time of gmake is dominated by the compiler it runs, but system time is not negligible: with one core, 7.6% of the execution time is system time."
  - §5, p. 9: "We run experiments on a 48-core machine, with a Tyan Thunder S4985 board and an M4985 quad CPU daughterboard. The machine has a total of eight 2.4 GHz 6-core AMD Opteron 8431 chips."
  - §5.6 gmake, p. 12: "We measure the performance of parallel gmake by building the object files of Linux 2.6.35-rc5 for x86_64. All input source files reside in the buffer cache, and the output files are written to tmpfs. We set the maximum number of concurrent jobs of gmake to twice the number of cores."
  - §5.6, p. 12: "Figure 9 shows that gmake on 48 cores achieves excellent scalability, running 35 times faster on 48 cores than on one core for both the stock and PK kernels. The PK kernel shows slightly lower system time owing to the changes to the dentry cache. gmake scales imperfectly because of serial stages at the beginning of the build and straggling processes at the end."
  - §5.6, p. 12: "gmake scales so well in part because much of the CPU time is in the compiler, which runs independently on each core. In addition, Linux kernel developers have thoroughly optimized kernel compilation, since it is of particular importance to them."
  - Figure 9 caption, p. 12: "gmake throughput and runtime breakdown." (axes: "Throughput (builds / hour / core)" and "CPU time (sec / build)", legend "Stock / PK / PK user time / PK system time"; the numeric values are in the plot only and did not extract.)
- **Coverage.**
  - T1: partial. Object: the kernel build's process population; statement only that "gmake creates more processes than there are cores"; no counts, no per-process lifetimes.
  - T2: partial. Object: CPU time of the whole build; statistic: system-time share 7.6% on one core (user/system split per build in Figure 9, not extractable as numbers); sources in the buffer cache, outputs on tmpfs (a deliberately warm, no-disk configuration); no per-compile distribution and no I/O-blocking measurement.
  - T3: does not cover beyond "-j = 2 × cores".
  - T4: mentions "twice the number of cores" as the paper's own choice, no rationale beyond scalability testing.
  - T6: covers. Workload: Linux 2.6.35-rc5 `defconfig` x86_64, object files only ("building the object files"), `-j` = 2 × cores, 1–48 cores; machine: 8 × 6-core AMD Opteron 8431, 2.4 GHz; observation: 35× speedup at 48 cores, imperfect because of "serial stages at the beginning of the build and straggling processes at the end".
  - T5, T7, T8: do not cover.
- **One observation?** One machine, one kernel tree and config, a sweep over core counts; window = one build per point.

### S1-03 — Coetzee, Bhaskar, Necula, "A Model and Framework for Reliable Build Systems", arXiv 1203.2704

- **Citation.** Derrick Coetzee, Anand Bhaskar, George Necula (UC Berkeley). *A Model and Framework for Reliable Build Systems.* arXiv:1203.2704v1 [cs.SE], 13 Mar 2012. 11 pages.
- **Copy read.** `https://arxiv.org/pdf/1203.2704` (v1), as served 2026-09-14; local `sources/S1-03/coetzee-1203.2704.pdf`; SHA-256 `637cbce65f2ceceed18434f59efadbfd54dc3bdcfdc85ee5f6cb75fd4ae882b9`.
- **Passages.**
  - §4 (resources), p. 3: "For example, the Linux kernel build has a single header containing all configuration options which is included by all source files. In order to make incremental builds useful in the event of configuration option changes, the Linux build tracks each option as a separate resource."
  - §9 (prototypes), p. 9: "Given enough concurrent processes, this build scaled to 85% the time of a parallel make build of the Linux kernel. However, it was not a complete system, as it was unable to handle unexpected new dependencies, could not perform incremental builds, and inferred its list of processes to execute from a prior make run, making it necessary to rerun the make build whenever this process sequence was changed."
  - §9, p. 9: "The major performance bottleneck in this prototype was the necessity for the central build monitor process to sequentially handle all ptrace messages. A variant of this prototype used binary rewriting based on Jockey [12] to track system calls without the use of ptrace. Jockey rewrites binaries at load time by searching for system calls, and also keeps a cache of patches to apply for binaries it's seen before. In practice, even with caching, the system added too much overhead to be practical due to the Linux kernel build's enormous number of short-lived processes like cp and mkdir. This is less likely to be an issue in a more monolithic build system."
  - §9, p. 9: "Instead of replacing make, make is run sequentially and children of make are run speculatively, pretending to succeed so that make will continue and begin the next process."
- **Coverage.**
  - T1: partial, qualitative only. Names the Linux kernel build's "enormous number of short-lived processes like cp and mkdir" as the reason a per-process instrumentation approach failed; no counts, no lifetimes, no machine.
  - T2, T3 (beyond the sequential-make-with-speculative-children design), T6, T7: do not cover. T4, T5, T8: do not cover.
- **One observation?** No: prototype experience reported without machine, kernel version, `-j` or window.

### S1-04 — Zheng et al., "Towards Agentic OS: An LLM Agent Framework for Linux Schedulers", arXiv 2509.01245

- **Citation.** Yusheng Zheng et al. *Towards Agentic OS: An LLM Agent Framework for Linux Schedulers.* arXiv:2509.01245v4 [cs.AI], 30 Sep 2025. 6 pages (short paper; "Preliminary Evaluation").
- **Copy read.** `https://arxiv.org/pdf/2509.01245` (stamp "arXiv:2509.01245v4 [cs.AI] 30 Sep 2025"), as served 2026-09-14; local `sources/S1-04/schedcp-2509.01245.pdf`; SHA-256 `cce49d3c0ff5466cafc3b921373f6d43df2adcb97e38b40c9d45e3b21206e97c`.
- **Passages.**
  - §4, p. 4: "For kernel compilation, it produces profiles like “CPU-intensive parallel compilation with short-lived processes, inter-process dependencies, targeting makespan minimization.”"
  - §5 Preliminary Evaluation, p. 4: "Evaluation uses two machines: 86-core Intel Xeon 6787P with 758GB RAM running Linux 6.14, and 8-core Intel Core Ultra 7 258V with 30GB RAM running Linux 6.13. Agents use Claude Code (Opus 4), testing each case three times and averaging results."
  - §5, p. 4: "Scheduler Configuration: For kernel compilation (tinyconfig, “make -j 172” on 6.14 source), SchedCP achieves 1.63× speedup with scx_rusty initially, then iterative refinement selects scx_layered for 16% additional gain, reaching 1.79× total improvement over EEVDF (Figure 2a)."
  - Figure 2(a) "AI configured scheduler for Linux build time", p. 4, bar labels as extracted: "default Linux EEVDF / first attempt / Iter 3 times / basic RL scheduler … 13.57s 8.31s 7.60s 13.79s 1.63× 1.79× 0.98×" (axis "Average Build Time (seconds)").
- **Coverage.**
  - T1: partial, qualitative — the workload profile string "short-lived processes, inter-process dependencies" is the agent's generated description, not a measurement.
  - T2, T3: do not cover.
  - T4: `-j 172` on the 86-core machine (my inference: 172 = 2 × 86 cores; the paper does not state which of the two machines ran the build, nor whether 86 counts hardware threads).
  - T6: covers. Workload: Linux 6.14 `tinyconfig`, `make -j 172`; schedulers EEVDF vs scx_rusty vs scx_layered; build time 13.57 s (EEVDF) → 8.31 s → 7.60 s; no process counts or lifetimes.
  - T5, T7, T8: do not cover.
- **One observation?** One workload, averaged over three runs; machine not unambiguously tied to the build (see above); window = one tinyconfig build (~8–14 s).

### S1-05 — Gouicem, Carver, Lozi, Sopena, Bouron, Lepers, Zwaenepoel, Muller, Lawall, "Fewer Cores, More Hertz: Leveraging High-Frequency Cores in the OS Scheduler for Improved Application Performance", USENIX ATC '20

- **Citation.** Redha Gouicem, Damien Carver, Jean-Pierre Lozi, Julien Sopena, Baptiste Lepers, Willy Zwaenepoel, Nicolas Palix, Julia Lawall, Gilles Muller. *Fewer Cores, More Hertz: Leveraging High-Frequency Cores in the OS Scheduler for Improved Application Performance.* 2020 USENIX Annual Technical Conference (ATC '20), July 15–17, 2020, pp. 435–448.
- **Copy read.** `https://www.usenix.org/system/files/atc20-gouicem.pdf`, as served 2026-09-14, 15 pages; local `sources/S1-05/gouicem-atc20.pdf`; SHA-256 `4e9e4a0f9a04717b4efefaaba10a5a4d58482e1d012722f97f7b6a05789ce447`. PDF p. 2 = printed 435, p. 3 = 436, p. 4 = 437, p. 6 = 439, p. 7 = 440.
- **Passages.**
  - §1, PDF p. 2 / printed 435: "Our case study finds repeated frequency inversions when processes are created through the fork() and wait() system calls, and our profiling traces make it clear that frequency inversion leads to tasks running on low frequency cores for a significant part of their execution."
  - §2 "A Case Study: Building the Linux Kernel", p. 3 / 436: "We present a case study of the workload that led us to discover the frequency inversion phenomenon: building the Linux kernel version 5.4 with 320 jobs (-j) on a 4-socket Intel Xeon E7-8870 v4 machine with 80 cores (160 hardware threads), with a nominal frequency of 2.1 GHz. Thanks to the Intel SpeedStep and Turbo Boost technologies, our CPUs can individually vary the frequency of each core between 1.2 and 3.0 GHz."
  - Figure 1 caption, p. 3 / 436: "Execution trace when building the Linux kernel version 5.4 using 320 jobs."
  - §2, p. 4 / 437: "In Figure 1, we notice different phases in the execution. For a short period around 2 seconds, for a longer period between 4.5 and 18 seconds, and for a short period around 28 seconds, the kernel build has highly parallel phases that use all of the cores at a high frequency. The second of these three phases corresponds to the bulk of the compilation. In these three phases, the CPUs seem to be exploited to their maximum. Furthermore, between 22 and 31 seconds, there is a long phase of mostly sequential code with very few active cores, of which there is always one running at a high frequency. In this phase, the bottleneck is the CPU's single-core performance. Between 0 and 4.5 seconds, and between 18 and 22 seconds however, there are phases during which all cores are used but they run at the CPU's lowest frequency (1.2 GHz). Upon closer inspection, these phases are actually mainly sequential: zooming in reveals that while all cores are used across the duration of the phase, only one or two cores are used at any given time."
  - §2, p. 4 / 437: "We are in the presence of a pattern that is typical of mostly-sequential shell scripts: processes are created through the fork() and exec() system calls, and generally execute one after the other. These processes can easily be recognized on Figure 2a as they start with WAKEUP_NEW and EXEC scheduler events. After the process that runs on Core 56 blocks around the 0.96 s mark, three such short-lived processes execute one after the other on Cores 132, 140, and 65. After that, two longer-running ones run on Core 69 around the 0.98 s mark, and on Core 152 between the 0.98 s and 1.00 s mark."
  - §2, p. 4 / 437: "a FTL of several dozens of milliseconds is significantly longer than the execution of the tasks that are visible in the figure, as the longest task runs for around 20 ms between the 1.00 s and 1.02 s marks."
  - §2, p. 5 / 438: "Computations in the (near) sequential phases of the build of Linux are launched sequentially as processes through the fork() and wait() system calls, and the execution of these computations is shorter than the FTL."
  - §3, p. 6 / 439: "We have chosen a default value of 50 µs, which is close to the delay between a fork and a wait system call during our Linux kernel build experiments."
  - §4 (Figure 4 benchmark labels), p. 7 / 440: "kbuild-all-80", "kbuild-all-160", "kbuild-all-320", "build-linux-kernel-0", "kbuild-sched-320", "kbuild-sched-160", "kbuild-sched-80", "build-llvm-0", "llvmcmake" (Phoronix-suite and own kernel-build variants; the numeric suffixes are the job counts as I read them — the paper's own label legend did not extract).
- **Coverage.**
  - T1: covers the shape, not the counts. Object: processes of a `make -j320` Linux 5.4 build, from a scheduler trace (SchedLog, per-tick 4 ms); observations: sequential phases of fork/exec'd "short-lived processes" one after another; "the longest task runs for around 20 ms" in the zoomed 1.00–1.02 s window; "delay between a fork and a wait system call" ≈ 50 µs (paper's characterisation of the sequential phases). No population counts, no per-process-type breakdown, no lifetime histogram.
  - T2: partial — phase structure of the whole build (parallel phases at 2 s, 4.5–18 s, 28 s; sequential phases 0–4.5 s, 18–22 s, 22–31 s) for one ~31 s build; nothing per compiler process, nothing on I/O blocking.
  - T3: does not cover make itself (the sequential phases are attributed to "mostly-sequential shell scripts").
  - T4: `-j` = 320 = 2 × 160 hardware threads (my reading; no rationale given).
  - T6: covers. Workload: Linux 5.4 build, `-j320`, plus `kbuild-all-{80,160,320}`, `kbuild-sched-{80,160,320}`, `build-linux-kernel`, `build-llvm` in the evaluation; machine: 4 × Intel Xeon E7-8870 v4, 80 cores/160 threads, 1.2–3.0 GHz; scheduler CFS (kernel version of the test host not quoted here); also "an AMD desktop machine" is mentioned as a second evaluation host (§4, p. 6).
  - T5, T7, T8: do not cover.
- **One observation?** Figure 1/2: one build on one named machine, window 0–31 s; Figure 4: benchmark sweeps on the same machine.

### S1-06 — Lozi, Lepers, Funston, Gaud, Quéma, Fedorova, "The Linux Scheduler: a Decade of Wasted Cores", EuroSys 2016

- **Citation.** Jean-Pierre Lozi, Baptiste Lepers, Justin Funston, Fabien Gaud, Vivien Quéma, Alexandra Fedorova. *The Linux Scheduler: a Decade of Wasted Cores.* EuroSys '16, London, April 18–21, 2016. 16 pages.
- **Copy read.** Author copy `https://people.ece.ubc.ca/sasha/papers/eurosys16-final29.pdf`, as served 2026-09-14; local `sources/S1-06/lozi-eurosys16.pdf`; SHA-256 `c0d99ee07a3ec791e0e75b60a2834a6f46afb41c0959230aae4110d5321f9515`.
- **Passages.**
  - §3.1 The Group Imbalance bug, p. 5: "We encountered this bug on a multi-user machine which we used to perform kernel compilation and data analysis using the R machine learning package. We suspected that this system, a 64-core, eight-node NUMA server, did not use all available cores for highly-threaded computations, instead crowding all threads on a few nodes."
  - §3.1, p. 5: "In the time period shown in the figure, the machine was executing a compilation of the kernel (make with 64 threads), and running two R processes (each with one thread). The make and the two R processes were launched from 3 different ssh connections (i.e., 3 different ttys)."
  - §3.1, p. 5: "With autogroups, the thread's load is also divided by the number of threads in the parent autogroup. In our case, a thread in the 64-thread make process has a load roughly 64 times smaller than a thread in a single-threaded R process."
  - §3.3 (Overload-on-Wakeup), p. 8: "Since we already described the Group Imbalance bug in Section 3.1, we disabled autogroups in this experiment in order to better illustrate the Overload-on-Wakeup bug."
  - Figure 4 caption, p. 6: "Topology of our 8-node AMD Bulldozer machine"
- **Coverage.**
  - T1, T2, T3: do not cover (the build is treated as a 64-thread load source; "the 64-thread make process" is the authors' phrasing for `make -j64`'s process tree).
  - T4: `-j64` on 64 cores (my reading of "make with 64 threads").
  - T6: covers. (a) Kernel compilation with 64 parallel jobs on a 64-core, 8-node AMD Bulldozer NUMA server as the workload that exposed the Group Imbalance bug; (b) the autogroup feature's effect stated concretely: per-thread load divided by the autogroup's thread count, so a make thread weighs ~1/64 of a single-threaded R process — the paper's explanation of why the build's threads were crowded onto a few nodes; (c) autogroups disabled for the wake-up experiment. Kernel versions studied: "from Linux 3.17 through 4.3" (p. 2).
  - T5, T7, T8: do not cover.
- **One observation?** Figure 2: one time window on one named machine with one build (kernel version built not stated) and two R processes.

### S1-07 — Harchol-Balter, Downey, "Exploiting Process Lifetime Distributions for Dynamic Load Balancing", ACM TOCS 15(3) 1997 (and SIGMETRICS '96)

- **Citation.** Mor Harchol-Balter, Allen B. Downey. *Exploiting Process Lifetime Distributions for Dynamic Load Balancing.* ACM Transactions on Computer Systems 15(3), August 1997, pp. 253–285. Earlier version: Proc. ACM SIGMETRICS '96, Philadelphia, May 1996, pp. 13–24.
- **Copy read.** (a) TOCS: `https://users.soe.ucsc.edu/~scott/courses/Fall11/221/Papers/Sync/harcholbalter-tocs97.pdf` (course mirror of the ACM PDF), 33 pages; local `sources/S1-07/harchol-tocs97.pdf`; SHA-256 `df2363134ea9c72d62a8e3e382dd5ba7f5d4a73f2472f181f969fea2435e6336`. PDF p. 7 = printed 259, p. 8 = 260, p. 10 = 262. (b) SIGMETRICS: `https://www.cs.cmu.edu/~harchol/Papers/Sigmetrics96.pdf` (author copy, scanned), 12 pages; local `sources/S1-07/harchol-sigmetrics96.pdf`; SHA-256 `1cbf485d65404ca5c94b66e5b2583b6623bfb1cfd81a8151b58bcb2ad18bcff9`. Both accessed 2026-09-14.
- **Passages.**
  - TOCS §2, PDF p. 7 / printed 259: "In 1986, Cabrera measured UNIX processes and found that over 40% doubled their current age [Cabrera 1986]. That same year, Leland and Ott [1986] proposed a functional form for the process lifetime distribution, based on measurements of the lifetimes of 9.5 million UNIX processes between 1984 and 1985. They conclude that process lifetimes have a UBNE (used-better-than-new-in-expectation) type of distribution. That is, the greater the current CPU age of a process, the greater its expected remaining CPU lifetime."
  - TOCS §2, p. 7 / 259: "we performed an independent study of this distribution and found that the functional form proposed by Leland and Ott fits the observed distributions well, for processes with lifetimes greater than 1 second. This functional form is consistent across a variety of machines and workloads, and although the parameter k varies from −1.3 to −0.8, it is generally near −1." (the minus signs did not extract; the SIGMETRICS copy reads "varies from -1.3 to -.8, it is generally near -1.0")
  - TOCS §2, p. 8 / 260: "—the probability that a process with age 1 second uses at least T seconds of total CPU time is about 1/T; —the probability that a process with age T seconds uses at least an additional T seconds of CPU time is about 1/2—thus, the median remaining lifetime of a process is equal to its current age."
  - TOCS §2.1, p. 8 / 260: "To determine the distribution of lifetimes for UNIX processes, we measured the lifetimes of over one million processes, generated from a variety of academic workloads, including instructional machines, research machines, and machines used for system administration. We obtained our data using the UNIX command lastcomm, which outputs the CPU time used by each completed process."
  - TOCS §2.1, p. 8 / 260: "The functional form we are proposing (the fitted distribution) has the property that its moments (mean, variance, etc.) are infinite. Of course, since the observed distributions have finite sample size, they have finite mean (0.4 seconds) and coefficient of variation (5–7)."
  - TOCS §2.1.1, p. 10 / 262: "For processes with lifetimes less than 1 second, we did not find a consistent functional form; however, for the machines we studied these processes had an even lower hazard rate than those of age > 1 second. That is, the probability that a process of age T < 1 seconds lives another T seconds is always greater than 1/2. Thus for jobs with lifetimes less than 1 second, the median remaining lifetime is greater than the current age."
  - SIGMETRICS Table 1, PDF p. 4 (columns "Total Number Procs. Studied" and "Num. Procs. with Age > 1", row labels as OCR'd "pol po2 po3 cow pors bugs faith", i.e. po1, po2, po3, cory, porsche, bugs, faith): "77440 154368 111997 182523 141950 83600 76507" and "4107 11468 7524 14253 10402 4940 3328"; caption: "The estimated lifetime distribution curve for each machine measured, and the associated goodness of fit statistics. Description of machines: Po is a heavily-used DECserver5000/240, used primarily for undergraduate coursework. Po1, po2, and po3 refer to measurements made on po mid-semester, late-semester, and end-semester. Cory is a heavily-used machine, used for coursework and research. Porsche is a less frequently-used machine, used primarily for research on scientific computing. Bugs is a heavily-used machine, used primarily for multimedia research. Faith is an infrequently-used machine, used both for video applications and system administration."
- **Coverage.**
  - T1, T2, T3: do not cover builds specifically (compilers are not singled out).
  - T6: covers the "study of process lifetime distributions on Unix in general" clause. Object: CPU lifetime (total CPU time at exit, from `lastcomm` accounting) of >1,000,000 UNIX processes on seven traces from six machines (1990s academic UNIX, DECserver 5000/240 named); statistic: Pr{L > T} ≈ T^k with k ≈ −1 for L > 1 s (Pareto/heavy-tailed), sample mean 0.4 s, CV 5–7, median remaining lifetime = age; below 1 s no consistent form but hazard rate even lower. My computation from Table 1: the share of processes with CPU age > 1 s is 3328/76507 ≈ 4.3% (faith) to 14253/182523 ≈ 7.8% (cory), i.e. roughly 92–96% of processes used ≤ 1 s of CPU. Also cites Leland & Ott's 9.5-million-process 1984–85 measurement (not read: no open copy, row 12).
  - T4, T5, T7, T8: do not cover.
- **One observation?** Several: seven traces on six named machines; windows are semesters (not quantified in seconds); no Linux, no builds.

### S1-08 — Blanchard, "The seven second kernel compile", Hispalinux Congress 2002 (talk paper, not peer-reviewed)

- **Citation.** Anton Blanchard (IBM OzLabs Linux Technology Center). *The seven second kernel compile.* Paper for the Hispalinux Congress, November 2002 ("preliminary version"). HTML.
- **Copy read.** `http://es.tldp.org/Presentaciones/200211hispalinux/blanchard/talk_2.html`, as served 2026-09-14; local `sources/S1-08/blanchard-talk_2.html` (+ `.txt`); SHA-256 `61c448a13bbcf23abf948df7c8fca891f72b22b924066c097db2ce384b84429f`.
- **Passages.**
  - §1 Introduction: "The kernel compile benchmark is a benchmark often used by Linux kernel developers to assess the performance of changes they make. It has the the advantages of being both easy to run as well as having reasonably repeatable results. Although heavily CPU bound, it stresses a number of areas in the kernel, like the process, filesystem and virtual memory subsystems."
  - §2 (quoted e-mail, Martin J. Bligh, 8 Mar 2002): "“time make -j32 bzImage” is now down to 23 seconds. (16 way NUMA-Q, 700MHz P3's, 4Gb RAM)."
  - §4 (quoted e-mail, Anton Blanchard, 13 Mar 2002): "hardware: 24 way logical partition, 1.1GHz POWER4, 60G RAM / kernel: 2.5.6 + ppc64 pagetable rework / kernel compiled: 2.4.18 x86 with Martin's config / compiler: gcc 2.95.3 x86 cross compiler / # MAKE="make -j14" /usr/bin/time make -j14 bzImage / ... / 130.63user 71.31system 0:10.31elapsed 1957%CPU"
  - §4: "Averaged over the entire run, less than 20 CPUs (19.57) were used The benchmark was significantly system bound (130.64 user vs 71.31 system) While most of the benchmark could be split across all CPUs, the final link stage was single threaded. This explained why we saw only 20 CPUs utilised."
- **Coverage.**
  - T1: does not cover (no process counts).
  - T2: partial, build-level only: user 130.63 s vs system 71.31 s CPU for a 10.31 s wall `make -j14 bzImage` (2.4.18 x86 cross-compiled with gcc 2.95.3); the single-threaded final link named as the reason for < 20 CPUs average.
  - T3: does not cover.
  - T4: `-j14` on a 24-way partition, `-j32` on a 16-way NUMA-Q; no rationale.
  - T6: covers historically: the kernel-compile benchmark as the kernel developers' yardstick, with machine (24-way 1.1 GHz POWER4 LPAR, 60 GB), kernel (2.5.6 + patches), tree built (2.4.18 x86, "Martin's config") and `-j`.
  - T5, T7, T8: do not cover.
- **One observation?** Yes for the quoted run: one machine, one tree/config, one `-j`, window 10.31 s. Not peer-reviewed (kernel-developer talk paper reproducing mailing-list posts).

### S1-09 — Miller, "Recursive Make Considered Harmful", AUUGN 1998

- **Citation.** Peter Miller. *Recursive Make Considered Harmful.* AUUGN (Journal of AUUG Inc.) 19(1), 1998, pp. 14–25 (PDF dated "10 March 2008" in the footer, from the Aegis project site; content labelled "AUUGN´97"). 16 pages in this copy.
- **Copy read.** `https://aegis.sourceforge.net/auug97.pdf`, as served 2026-09-14; local `sources/S1-09/miller-auug97.pdf`; SHA-256 `bbffbbbd5763b7cf08cc30ebfd61805f0fe1784e8bc4335fb79027b20d5019b4`.
- **Passages.** (the extraction inserts spurious spaces inside words; I have joined them)
  - §3.3.1, p. 5: "Note that “make -j” (parallel build) invalidates many of the ordering assumptions implicit in the reshuffle solution, making it useless. And then there are all of the sub-makes all doing their builds in parallel, too."
  - §4.5.1 Project Builds, p. 6: "In order to build the DAG, make must “stat” 3000 files, plus an additional 2000 files or so, depending on which implicit rules your make knows about and your Makefile has left enabled. On the author's humble 66MHz i486 this takes about 10 seconds; on native disk on faster platforms it goes even faster. With NFS over 10MB Ethernet it takes about 10 seconds, no matter what the platform."
  - §4.5.1, p. 7: "Breaking the set of files up into 100 modules, and running it as a recursive make takes about 25 seconds. The repeated process creation for the subordinate make invocations take quite a long time."
  - §4.5.1, p. 7: "The above result tells us that it is not the number of files which is slowing us down (that only takes 10 seconds), and it is not the repeated process creation for the subordinate make invocations (that only takes another 15 seconds). So just what is taking so long? … Complexity of the Makefile is what is taking so long."
- **Coverage.**
  - T3: covers make's own overhead, 1990s scale: a 1000-source-file no-op build costs ~10 s of `stat` work on a 66 MHz i486 and ~15 s more for 100 recursive sub-make invocations; qualitative statement that `-j` and recursive sub-makes interact ("all of the sub-makes all doing their builds in parallel"). No jobserver (the paper predates it), no per-job CPU cost, no live-process count.
  - T1, T2, T6, T7: do not cover. T4, T5, T8: do not cover.
- **One observation?** A "hypothetical project with 1000 source (.c) files" timed on the author's machine; no window, no `-j`.

### S1-10 — Martin, "Ninja", chapter in *The Performance of Open Source Applications* (2013; book chapter, not peer-reviewed)

- **Citation.** Evan Martin. *Ninja.* In: Tavish Armstrong (ed.), *The Performance of Open Source Applications*, Lulu, 2013 (aosabook.org). HTML.
- **Copy read.** `https://aosabook.org/en/posa/ninja.html`, as served 2026-09-14; local `sources/S1-10/posa-ninja.html` (+ `.txt`); SHA-256 `edc95e34b0c571c3be69234fa45aa5883ed1369afa030717dc33ec58c3e7f7fc`.
- **Passages.**
  - Section "Executing a Build": "Performance-wise the process of executing the commands judged necessary according to the dependencies discussed above is relatively uninteresting because the bulk of the work that needs to be done is performed in those commands (i.e., in the compilers, linkers, etc.), not in Ninja itself."
  - Same section: "Ninja runs build commands in parallel by default, based on the number of available CPUs on the system. Since commands running simultaneously could have their outputs interleave, Ninja buffers all output from a command until that command completes before printing its output. The resulting output appears as if the commands were run serially."
  - Footnote to that section: "One minor benefit of this is that users on systems with few CPU cores have noticed their end-to-end builds are faster due to Ninja consuming relatively little processing power while driving the build, which frees up a core for use by build commands."
  - Section "The Build Log", footnote 9: "It also stores when each command started and finished, which is useful for profiling builds of many files."
  - Section "A Small History of Chrome": "The initial attempt used the Scons build system, but I was dismayed to discover that a GYP-generated Scons build could take 30 seconds to start while Scons computed which files had changed. I figured that Chrome was roughly the size of the Linux kernel so the approach taken there ought to work. I rolled up my sleeves and wrote the code to make GYP generate plain Makefiles using tricks from the kernel's Makefiles."
- **Coverage.**
  - T3: covers ninja's dispatch policy qualitatively (parallel by default, job count from CPU count; the driver's own CPU cost described as "relatively little", with the anecdotal claim that it frees a core versus make on few-core machines); no measurement of the driver's per-job cost, no jobserver discussion, no live-process count relation.
  - T4: ninja's default parallelism "based on the number of available CPUs" (outside my class; noted).
  - T1, T2, T6, T7: do not cover. T5, T8: do not cover.
- **One observation?** No measurements; author's design account.

### S1-11 — Baumann, Appavoo, Krieger, Roscoe, "A fork() in the road", HotOS 2019

- **Citation.** Andrew Baumann, Jonathan Appavoo, Orran Krieger, Timothy Roscoe. *A fork() in the road.* Workshop on Hot Topics in Operating Systems (HotOS '19), Bertinoro, May 13–15, 2019. 9 pages.
- **Copy read.** `https://www.microsoft.com/en-us/research/uploads/prod/2019/04/fork-hotos19.pdf`, as served 2026-09-14; local `sources/S1-11/fork-hotos19.pdf`; SHA-256 `176a40a6ba80d6e6a25b2f2584f0d46d8ed781e283ad105fa92146168d68263c`.
- **Passages.**
  - §4 "Fork is slow", p. 3: "Today, even the time to establish copy-on-write mappings is a problem: Chrome experiences delays of up to 100 ms in fork [28], and Node.js applications can be blocked for seconds while forking prior to exec [56]."
  - §4, p. 3: "Figure 1 plots the time to fork and exec from a process of varying size under Ubuntu 16.04.3 on an Intel i7-6850K CPU at 3.6 GHz. The dirty line shows the cost of forking a process with dirty pages, which must be downgraded to read-only for copy-on-write mappings. In the fragmented case, the parent dirties only its stack, but simulates memory layout in a complex application using shared libraries, address space randomisation, and just-in-time compilation, by allocating alternating read-only and read-write pages. By contrast, posix_spawn() takes the same time (around 0.5 ms) regardless of the parent's size or memory layout."
  - §1, p. 1: "50 years later, fork remains the default process creation API on POSIX: Atlidakis et al. [8] found 1304 Ubuntu packages (7.2% of the total) calling fork, compared to only 41 uses of the more modern posix_spawn(). Fork is used by almost every Unix shell, major web and database servers (e.g., Apache, PostgreSQL, and Oracle), Google Chrome, the Redis key-value store, and even Node.js."
- **Coverage.**
  - T1: marginal — gives the order of magnitude of one fork+exec (posix_spawn ≈ 0.5 ms; fork+exec rising with parent size, plotted up to 25 ms in Figure 1) on a named desktop CPU, which bounds the per-process creation cost a make-driven build pays; no build workload.
  - T2, T3, T6, T7: do not cover. T4, T5, T8: do not cover.
- **One observation?** One microbenchmark on one named machine (i7-6850K, Ubuntu 16.04.3); no window.

### S1-12 — Wang, Jia, Huang, Cao, Song, "Mixture-of-Schedulers: An Adaptive Scheduling Agent as a Learned Router for Expert Policies", arXiv 2511.11628

- **Citation.** Xinbo Wang, Shian Jia, Ziyang Huang, Jing Cao, Mingli Song (Zhejiang University; HangZhou City University). *Mixture-of-Schedulers: An Adaptive Scheduling Agent as a Learned Router for Expert Policies.* arXiv:2511.11628v1 [cs.DC], 7 Nov 2025. 15 pages.
- **Copy read.** `https://arxiv.org/pdf/2511.11628` (v1), as served 2026-09-14; local `sources/S1-12/mos-2511.11628.pdf`; SHA-256 `3a887853b4b21974373f912492963108f55f1526f1e951934a233c850fb07b8b`.
- **Passages.**
  - §5.1.1, p. 7: "we constructed a benchmark suite of 28 scenarios. These are generated by pairing 4 interactive, latency-sensitive applications (Web Browsing, Audio Remix, Office File, Game Play) with 7 resource-intensive, background workloads (e.g., kernel compilation, blender render, LLM local generation)."
  - Table 2, p. 7 (rows): "S3 Game Play & Kernel Compile", "S10 Office File Editing & Kernel Compile", "S17 Web Browsing & Kernel Compile", "S24 Audio Remix & Kernel Compile"; other background workloads listed: "Archive Extraction", "Blender Render", "LLM Generate", "Disk IO", "Network Transfer", "Video Render".
  - §5.1.1, p. 7: "Our evaluation is conducted on a cluster of 10 distinct virtual machines (VMs) managed by Proxmox VE, which allows us to adjust parameters such as the number of CPU cores allocated to a VM on the base hardware, thereby creating a richer set of test hardware platforms. As shown in Table 3, these VMs feature heterogeneous CPU architectures with core counts ranging from 2 to 20, including both symmetric core designs and asymmetric Intel Hybrid Architecture configurations."
  - Appendix "Kernel Compile Scenario", p. 15: "The Kernel Compile scenario simulates the compilation process of an operating system kernel. It is a typical batch processing workload with extremely complex dependencies, and a dense mix of I/O read/write and computing tasks. The compilation process generates a large number of processes and threads and frequently switches between file reading/writing and computation."
  - Appendix, p. 15: "this study chose the complete compilation of the Linux 6.14 kernel [47] under the default configuration as the test load. The total compilation completion time was recorded to measure whether the scheduler can efficiently complete the background compute-intensive task while ensuring the smooth operation of foreground applications."
- **Coverage.**
  - T1: qualitative only ("generates a large number of processes and threads and frequently switches between file reading/writing and computation") — a description, not a measurement.
  - T2, T3: do not cover.
  - T6: covers. Workload: "complete compilation of the Linux 6.14 kernel under the default configuration" as a background load paired with four interactive apps, on 10 Proxmox VMs of 2–20 vCPUs (Table 3 details did not extract as text); metric: total compile time; `-j` not stated; schedulers: sched_ext expert policies vs EEVDF (Figure 5 heat-map percentages extracted but not attributable per scenario without the table).
  - T7: partial — names "Blender Render", "Video Render", "LLM Generate", "Archive Extraction" as the CPU-saturating background jobs of a desktop scenario suite; no thread counts, utilisation or durations quoted.
  - T4, T5, T8: do not cover.
- **One observation?** 28 scenarios × 10 VMs; base hardware not named; window = one full kernel build per run.

### S1-13 — Al-Saleh, Crandall, "Antivirus Performance Characterization: System-Wide View" (UNM copy; published as IET Information Security 7(2), 2013 — publication details not verified from the copy)

- **Citation.** Mohammed I. Al-Saleh, Jedidiah R. Crandall (University of New Mexico). *Antivirus Performance Characterization: System-Wide View.* Copy from the UNM CS graduate-student archive 2010–2011, 9 pages, undated. (Search results identify the journal version as IET Information Security 2013, DOI 10.1049/iet-ifs.2012.0192; that version was not read.)
- **Copy read.** `https://www.cs.unm.edu/~csgsa/archive/2010-2011/papers/MohammedAl-saleh.pdf`, as served 2026-09-14; local `sources/S1-13/alsaleh-unm.pdf`; SHA-256 `d0c3fd37cd9dca57c44444d18f932357f027a2998012eef64cb4053210215bee`.
- **Passages.**
  - Abstract, p. 1: "Our results show that the main reason of performance degradation the tasks have with the existence of the AV software is that they mainly spend the extra time waiting on events. Also, the AV in most of our experiments enforces the tasks to spend more time using the CPU. Although there is an overhead from the competition between the tasks and the AV on the CPU, this competition is not a main factor of the overall overhead. Because of the AV intrusiveness, the tasks in our experiments are caused to create more file IO operations, page faults, system calls, and threads."
  - §3, p. 3: "We ran the experiments on a machine that has Windows 7 OS, Intel Dual Core Atom processor at 1.66 GHz, 4 GB RAM, and 250 GB of hard disk. … All partitions have the same exact software except that the second partition has Sophos AV installed, and the third partition has Symantec AV installed."
  - §4, p. 4: "in Sophos case, the total wait time is about 17 seconds while the whole execution is about 4.1 seconds. We found that 7za.exe process has three threads; the wait time is accumulated for the all three, see figure 11. However, that total time for all 7za.exe threads is about 2.8 seconds out of the 17 seconds. We found that python.exe process creates five threads in case of Sophos, while it is only one thread in case of Vanilla and Symantec."
  - §4, p. 5: "More threads are created for the iexplore.exe processes in case of Sophos (74 threads) and Symantec (64 threads) than in Vanilla (60 threads)."
  - §4, p. 5: "Although there is an overhead from the competition between the tasks and the AV on the CPU, this competition is not a main factor of the overall overhead because those tasks spend negligible time in the scheduler's ready queue."
- **Coverage.**
  - T7: partial and off-target. Object: on-access antivirus (Sophos, Symantec) overhead on four scripted end-user tasks under Windows 7 on a dual-core Atom netbook, measured with ETW/xperf; units: per-process lifetime split into execute / ready / wait states, thread counts, file-I/O and syscall counts. It is not a full-disk scan job; there is no sustained-utilisation or thread-count figure for the scanner itself. Nothing on process-treatment catalogues.
  - T1, T2, T3, T6: do not cover. T4, T5, T8: do not cover.
- **One observation?** One machine (named), four tasks, three OS partitions; windows are the 4–17 s task runs.

### S1-14 — Bienia, Kumar, Singh, Li, "The PARSEC Benchmark Suite: Characterization and Architectural Implications", Princeton TR-811-08 (2008; PACT 2008 version not obtained)

- **Citation.** Christian Bienia, Sanjeev Kumar, Jaswinder Pal Singh, Kai Li. *The PARSEC Benchmark Suite: Characterization and Architectural Implications.* Princeton University Technical Report TR-811-08, January 2008. 22 pages. (The PACT 2008 paper of the same title was not obtained — parsec.cs.princeton.edu returned proxy 502 three times.)
- **Copy read.** `https://www.cs.princeton.edu/techreports/2008/811.pdf`, as served 2026-09-14; local `sources/S1-14/parsec-tr811.pdf`; SHA-256 `4c08caea66098781d11a1222822a38ad7a0ac032c363cbbad4dcaf88a6fa3f4b`.
- **Passages.**
  - Table 1, p. 3 (columns Program, Application Domain, Parallelization Model, Granularity, Working Set, Data Usage Sharing, Exchange): "x264 Media Processing pipeline coarse medium high high"
  - Table 2, p. 4 (columns Program, Problem Size, Instructions (Billions) Total / FLOPS / Reads / Writes, Synchronization Primitives Locks / Barriers / Conditions): "x264 128 frames, 640 × 360 pixels 32.43 8.76 9.01 3.11 16,767 0 1,056"; caption: "Breakdown of instructions and synchronization primitives for input set simlarge on a system with 8 cores. All numbers are totals across all threads."
  - §3.2.12 x264, p. 13: "The parallel algorithm of x264 uses the pipeline model with one stage per input video frame. This results in a virtual pipeline with as many stages as there are input frames. x264 processes a number of pipeline stages equal to the number of encoder threads in parallel, resulting in a sliding window which moves from the beginning of the pipeline to its end. For P- and B-Frames the encoder requires the image data and motion vectors from the relevant region of the reference frames in order to encode the current frame, and so each stage makes this information available as it is calculated during the encoding process. Fast upward movements can thus cause delays which can limit the achievable speedup of x264 in practice. In order to compensate for this effect, the parallelization model requires that x264 is executed with a number of threads greater than the number of cores to achieve maximum performance."
  - §3.2.12, p. 13: "The number of frames determines the amount of parallelism."
- **Coverage.**
  - T7: partial. Object: the x264 H.264 encoder's threading model (frame-level pipeline; one encoder thread per in-flight frame; recommended thread count > core count); scope: PARSEC `simlarge` input (128 frames, 640×360) on an 8-core system, instruction and synchronisation totals; no sustained CPU-utilisation percentage and no wall-clock duration quoted in text (the TR's later figures on parallel speedup did not extract as text). No antivirus, indexer or training jobs; no process-treatment catalogues.
  - T1, T2, T3, T6: do not cover. T4, T5, T8: do not cover.
- **One observation?** Characterisation on a simulated/real 8-core system (machine not named in the quoted text); one input set.

### S1-15 — van Rijn, Rellermeyer, "A Fresh Look at the Architecture and Performance of Contemporary Isolation Platforms", Middleware '21 (arXiv 2110.11462)

- **Citation.** Vincent van Rijn, Jan S. Rellermeyer (TU Delft). *A Fresh Look at the Architecture and Performance of Contemporary Isolation Platforms.* Middleware '21, December 6–10, 2021 (virtual). arXiv:2110.11462. 13 pages.
- **Copy read.** `https://arxiv.org/pdf/2110.11462` (no arXiv version stamp in the extracted text; camera-ready layout), as served 2026-09-14; local `sources/S1-15/isolation-2110.11462.pdf`; SHA-256 `4c94f14f025784e24eb39f63423e5f7d45601aca3d2aa943c766157aa13a2db6`.
- **Passages.**
  - §3, p. 5: "All experiments were conducted on a dual-socket AMD EPYC2 7542 CPU setup with 64 threads each, 256 GiB of RAM, a dedicated fast NVMe SSD as storage, and running Ubuntu Linux Server 20.04 LTS."
  - §3.1 Compute, p. 5: "The video encoding task entails loading a 30MB video file into memory, and then encoding that video file from H.264 to the H.265 video codec. For this benchmark we make use of the ffmpeg [16] program. The task is executed on guests that have access to 16 CPU cores, and the job itself is executed using 16 threads."
  - §3.1, p. 5: "In this experiment, we have used the ‘slower’ preset which trades CPU cycles for a higher compression ratio. The difference in performance between platforms in this benchmark can thus be attested to actual differences in CPU performance, not I/O"
  - §3.1, p. 5: "As Figure 5 shows, most of the runs end up at around 65000 milliseconds, while some differences between platforms can be observed."
  - Figure 5 caption, p. 5: "ffmpeg video re-encoding CPU bound benchmark, re-encoding a 1080p 30Mb video from H.264 to H.265. Time in ms, per platform."
- **Coverage.**
  - T7: covers one video-transcode job: ffmpeg H.264→H.265 (x265 "slower" preset implied by the preset name; the encoder library is not named), 16 threads on 16 vCPUs, ~65 s duration, characterised as "CPU bound"; no utilisation percentage; server (EPYC) hardware, in VMs/containers — not a desktop.
  - T1, T2, T3, T6: do not cover. T4, T5, T8: do not cover.
- **One observation?** One job, one named host, ≥10 repetitions; window ≈ 65 s.

### S1-16 — Coutinho, De Sensi, Lorenzon, Georgiou, Nunez-Yanez, Eder, Xavier-de-Souza, "Performance and Energy Trade-Offs for Parallel Applications on Heterogeneous Multi-Processing Systems", arXiv 2005.02947

- **Citation.** Demetrios A. M. Coutinho, Daniele De Sensi, Arthur Francisco Lorenzon, Kyriakos Georgiou, Jose Nunez-Yanez, Kerstin Eder, Samuel Xavier-de-Souza. *Performance and Energy Trade-Offs for Parallel Applications on Heterogeneous Multi-Processing Systems.* arXiv:2005.02947v1 [eess.SY], 6 May 2020 (journal article layout, "Received: 17 March 2020; Accepted: 21 April 2020"). 26 pages.
- **Copy read.** `https://arxiv.org/pdf/2005.02947` (v1), as served 2026-09-14; local `sources/S1-16/hmp-2005.02947.pdf`; SHA-256 `d7ae2b5a39ca4aa1b08c77b37dd5037cb7da545b79fdb17803ee242cb43e9628`.
- **Passages.**
  - §4.1, p. 11: "The proposed methodology was validated using an ODROID-XU3 [45] board developed by Hardkernel co. with two core types of the same single-ISA … It uses a Samsung Exynos5422 System on a Chip (SoC), which utilizes ARM big.LITTLE technology and constitutes an ARM Cortex-A15 (big) quad-core cluster and a Cortex-A7 (LITTLE) quad-core cluster."
  - §4.3, p. 14: "The notable exception for the chosen criteria is the x264 encoder provided by the Phoronix test suite since it has only POSIX threads for parallelism."
  - Table 2, p. 15: "x264 Media Processing CPU and memory intensive 1920 × 1080 pixels (HDTV resolution), 600 frames H.264 video encoder"
  - Table 3 "The fitted parallel fraction values of each application", p. 15: "Application Black-scholes Bodytrack Freqmine Smallpt x264 Kmeans Particle Filter LavaMD / f 0.7743 0.9384 0.9343 0.9898 0.888 0.6381 0.9251 0.9961"
  - §4.4, p. 20: "In particular, the x264 application (see Figure 5e) requires more refined modelling since video processing is much more complex, and the application phases tends to vary according to the frames from the input video."
- **Coverage.**
  - T7: partial. Object: x264 (Phoronix Test Suite version) encoding 600 1080p frames; statistic: fitted Amdahl parallel fraction f = 0.888 and the qualitative "phases … vary according to the frames"; no thread count (x264's own, "POSIX threads"), no utilisation, no wall time quoted; embedded ARM board, not a desktop.
  - T1, T2, T3, T6: do not cover. T4, T5, T8: do not cover.
- **One observation?** One board (ODROID-XU3), 50 Halton configurations per application.

### S1-17 — Gyawali, "Comparative Analysis of CPU and GPU Profiling for Deep Learning Models", arXiv 2309.02521

- **Citation.** Dipesh Gyawali (Louisiana State University). *Comparative Analysis of CPU and GPU Profiling for Deep Learning Models.* arXiv:2309.02521v3 [cs.DC], 9 Dec 2023. 6 pages.
- **Copy read.** `https://arxiv.org/pdf/2309.02521` (v3), as served 2026-09-14; local `sources/S1-17/cpugpu-2309.02521.pdf`; SHA-256 `c7307dd5f0ea1eca702240a70da63dc436c03fa3ce33f53b3de40ae665e65062`.
- **Passages.**
  - §VII (setup), p. 4: "• Total epochs: 20 • Optimizer: Adam • Loss Function: Cross-entropy • Batch size: 64 and 128 • Learning Rate: 0.003 and 0.03"
  - §VIII.A Utilization, p. 4: "The task was first processed through CPU which uses 62% resource consumption."
  - §VIII.A, p. 4: "Regarding CPU, the total resource utilization is (60-63)%. A total of 307 processes and 5410 threads were running with a clock speed of 4.10 GHz as shown in Figure 9. However, using only CPU, the model training time is comparatively higher as compared to GPU."
- **Coverage.**
  - T7: partial. Object: PyTorch CNN training (MNIST-class model, 20 epochs) on an unnamed workstation CPU at 4.10 GHz with two GPUs present; statistic: system-wide CPU utilisation 60–63% while training on CPU; 307 processes / 5410 threads system-wide (not the trainer's own thread count); no duration in the quoted text. Machine model not named.
  - T1, T2, T3, T6: do not cover. T4, T5, T8: do not cover.
- **One observation?** One run per configuration on one unnamed machine; window = the training run (length not quoted).

### S1-18 — Jones, Arpaci-Dusseau, Arpaci-Dusseau, "Antfarm: Tracking Processes in a Virtual Machine Environment", USENIX ATC 2006

- **Citation.** Stephen T. Jones, Andrea C. Arpaci-Dusseau, Remzi H. Arpaci-Dusseau (University of Wisconsin, Madison). *Antfarm: Tracking Processes in a Virtual Machine Environment.* 2006 USENIX Annual Technical Conference, Boston, May 30–June 3, 2006. 14 pages.
- **Copy read.** `https://www.usenix.org/legacy/event/usenix06/tech/full_papers/jones/jones.pdf`, as served 2026-09-14; local `sources/S1-18/antfarm-usenix06.pdf`; SHA-256 `e9a16b94a26612fb31e5f78f608d3d349fe177a21cd344f8ee82da0175b0e533`.
- **Passages.**
  - §6.1, p. 6: "Our evaluation on x86 uses Xen version 2.0.6. Version 2.6.11 of the Linux kernel was used in Xen's privileged control VM. Linux kernel version 2.4.30 and 2.6.11 are used in unprivileged VMs as noted. Our evaluation hardware consists of a 2.4 GHz Pentium IV PC with 512 MB of RAM. Virtual machines are each allocated 128 MB of RAM in this environment."
  - §6.1.1, p. 6: "The second workload is a parallel compile of the bash shell sources using the command “make -j 20” in a clean object directory. A compilation workload was chosen because it creates a large number of short-lived processes, stressing Antfarm's ability to track many concurrent processes that have varying runtimes."
  - Table 2 "Completeness", p. 7, rows as extracted (columns: Process Create / Addr Spc Create / Inferred Create; Process Exit / Addr Spc Exit / Inferred Exit; Context Switch / CS Inferred): under "Linux 2.4 x86": "Compile 815 815 815 / 815 815 815 / 4447 4447"; under "Linux 2.6 x86": "Compile 748 1191 1191 / 748 1191 1191 / 2550 2550"; under "Windows": "Compile 2602 2602 2602 / 2602 2602 2602 / 835248 835248". Caption: "The table shows the total number of creations and exits for processes and address spaces reported by the operating system. The total number of process creations and exits inferred by Antfarm are shown in comparison."
  - §6.1.1, p. 7: "Due to the idiomatic use of fork and exec, however, a process is partitioned in a distinctive way. … The duration of the first pseudo-process will nearly always be small. For example, in the case of our compilation workload, the average time between fork and exec is less than 1 ms, compared to the average lifetime of the second pseudo-process, which is more than 2 seconds, a difference of three orders of magnitude."
  - §6.1.1, p. 7: "The two pseudo-processes are separated by a short time period where neither is active. This interval corresponds to the time after the original address space is destroyed and before the new address space is created. During the compilation workload this interval averaged less than 0.1 ms and was never larger than 2.3 ms."
- **Coverage.**
  - T1: covers, with numbers. Object: all processes created by `make -j 20` building bash (version not stated; C, autoconf Makefiles); unit: process count per build; statistics: 815 processes (Linux 2.4.30 guest), 748 (Linux 2.6.11 guest), 2602 (Windows NT4 guest under Simics — a different toolchain, not comparable); mean fork→exec interval < 1 ms; mean exec→exit lifetime "more than 2 seconds" (Linux 2.6 guest, from the OS-reported trace); no per-process-type breakdown, no distribution beyond the mean. The 2.6 vs 2.4 count difference (748 vs 815) is unexplained in the paper. My computation: none needed.
  - T2: partial — the mean post-exec lifetime > 2 s covers all exec'd processes (compilers, shells, `make` children) on a 2.4 GHz Pentium 4 in a 128 MB VM; CPU vs blocked time not separated.
  - T3: does not cover.
  - T4: `-j 20` on a single-CPU VM (chosen to stress concurrency, no rationale about cores).
  - T6: covers as a named workload: bash `make -j 20`, Xen 2.0.6, guests Linux 2.4.30 / 2.6.11 / Windows NT4, host 2.4 GHz Pentium IV, 512 MB.
  - T5, T7, T8: do not cover.
- **One observation?** Yes: one build per guest OS, machine named, window = the build (duration not stated).

### S1-19 — Zheng, Nieh, "Automatic User Interaction Detection and Scheduling with RSIO" (Columbia University / VMware; technical report copy, 2008)

- **Citation.** Haoqiang Zheng (Columbia University, VMware), Jason Nieh (Columbia University). *Automatic User Interaction Detection and Scheduling with RSIO.* Columbia University Academic Commons, DOI 10.7916/D8891DPX (technical report; year per Google Scholar 2008). 16 pages.
- **Copy read.** `https://academiccommons.columbia.edu/doi/10.7916/D8891DPX/download`, as served 2026-09-14; local `sources/S1-19/zheng-nieh-rsio.pdf`; SHA-256 `9006fa71a8c66f136b2cd3e9e05646a53ec512cd9c7cd6404fe369c266c26147`.
- **Passages.**
  - §6, p. 10: "The machine used for all our measurements is an HP xw9300 PC with a 2.6 GHZ AMD Opteron processor and 2 GB RAM. The server was running Ubuntu 6.06, and the kernel used was Linux 2.6.19."
  - §6.1, p. 11: "In one terminal, a Linux kernel compilation is executed, which is a long running batch job. In the other terminal, a user types at the command prompt “time ls” … We also varied the load on the system due to the Linux kernel compilation by allow the compilation to be done in parallel with different numbers of processes. This was done using the -j option to specify the number of kernel compile processes to be generated. For example, we use the command make -j 4 to start the Linux kernel compile with 4 concurrent processes."
  - §6.1, p. 11: "We varied the system load imposed by the kernel compilation from no load when no kernel compilation processes were run, to allowing 64 concurrent processes to run to perform the kernel compilation. When running without any background kernel compilation workload, Linux and RSIO provide the same response time of 10 ms for the interactive directory listing command. However, as the load on the system increases, the response time of vanilla Linux increases dramatically. When 64 kernel compilation processes were running, the worst response time for Linux was 2.5 s"
  - §6.1, p. 11: "As a result, the worst case response time of RSIO is 28 ms even with 64 kernel compilation processes running. … The small performance degradation is mostly caused by I/O contention since both the background load and the interactive commands exercise the file system."
- **Coverage.**
  - T6: covers. Workload: Linux kernel compilation (version built not stated) with `-j` from 1 to 64 on a single-CPU 2.6 GHz Opteron workstation, Linux 2.6.19 (CFS predecessor), as background load for interactive response-time tests; no process counts or lifetimes.
  - T7: partial — a kernel compile characterised only as "a long running batch job" whose I/O also contends with interactive commands.
  - T1, T2, T3: do not cover. T4, T5, T8: do not cover.
- **One observation?** One machine (named), one build tree (unnamed), fifty repetitions per `-j` level.

### S1-20 — Groves, Knockel, Schulte, "BFS vs. CFS — Scheduler Comparison", University of New Mexico course report, 11 December 2009 (not peer-reviewed)

- **Citation.** Taylor Groves, Jeff Knockel, Eric Schulte (University of New Mexico). *BFS vs. CFS — Scheduler Comparison.* Course report (CS 587), 11 December 2009. 12 pages.
- **Copy read.** `https://www.cs.unm.edu/~eschulte/classes/cs587/data/bfs-v-cfs_groves-knockel-schulte.pdf`, as served 2026-09-14; local `sources/S1-20/groves-bfs-cfs.pdf`; SHA-256 `c3c7b38b6b3525da09edca8b762d83bb88ba558ac4c772638780ae6e6ca9b555`. (Extraction inserts spaces inside words; joined below.)
- **Passages.**
  - "Kernel Patching", p. 8: "we downloaded the 2.6.31.6 source code from http://www.kernel.org and made two copies. For one, we left the source code unmodified, and for the other we patched it with version 311 of Kolivas's BFS patch."
  - "Test Execution — Make", p. 8–9: "Our tests compiling VLC from source is designed to test the turnaround time of a scheduler. The VLC source is composed of 691 files of C source code, containing more than 416 thousand lines of code. … For our tests we use the command: make -j<number_of_jobs> The -j option launches the specified number of processes, for independent rules in the makefile, so that the compiling can occur in parallel. For our tests we used a j ranging from one to four."
  - Results, p. 11: "To further demonstrate the superiority of CFS on batch processes we compared make results run on a desktop using various numbers of jobs. These results contradict the claims of Con Kolvias, the creator of BFS. Kolivas claims that the BFS scheduler performs best when the -j level of make is equal to the number of CPUs. His claim goes against common wisdom – that make best utilizes CPU when -j is greater than the number of CPUs available – in effect that it is worth while to oversubscribe the number of CPUs. Our results reinforce the common wisdom and show that BFS does run faster when oversubscribed, albeit to a lesser degree than CFS."
  - Results, p. 10: "The CFS scheduler had better performance in terms of turnaround time on all three machines and under all load conditions. The difference in performance was more dramatic on more powerful machines like the multi-core desktop for which results are shown."
- **Coverage.**
  - T6: covers. Workload: VLC (691 C files) `make -j1..4` on three machines including a "multi-core desktop" (models not quoted in the extracted text), kernel 2.6.31.6 CFS vs BFS 311; metric: turnaround time; no process data.
  - T4 (outside my class, noted): records the 2009 folk rule "make best utilizes CPU when -j is greater than the number of CPUs" and Kolivas's counter-claim for BFS.
  - T1, T2, T3, T7: do not cover. T5, T8: do not cover.
- **One observation?** Several machines, one project; windows = one VLC build per point. Course report, not peer-reviewed.

### S1-21 — Nikseresht, Somayaji, Maheshwari, "Customer Appeasement Scheduling", arXiv 1012.3452

- **Citation.** Mohammad R. Nikseresht, Anil Somayaji, Anil Maheshwari (Carleton University). *Customer Appeasement Scheduling.* arXiv:1012.3452v1 [cs.OS], 15 Dec 2010. 23 pages.
- **Copy read.** `https://arxiv.org/pdf/1012.3452` (v1), as served 2026-09-14; local `sources/S1-21/nikseresht-1012.3452.pdf`; SHA-256 `508ed1576f8ca1b083a344332af8cf056f4f1c0f372322facf9b5eff54f7c95b`.
- **Passages.**
  - §7.1, p. 17: "All tests are performed on an IBM IntelliStation M Pro with Intel P4 2.8GHz CPU and 1GB of RAM running Fedora 12 with Kernel 2.6.32. In order to simulate different background system loads we compile Linux kernel and use different -j values with the make command to initiate different parallel compilations."
  - §7.4, p. 20: "Again we simulate the system load with parallel compilation of Linux kernel and use make -j with different values for -j to control the number of parallel makes. For each -j value the experiment is repeated three times and the average value of dropped frames is depicted in Figure 7.4. As we see in this graph under CFS/RBPE the frame drop is almost zero for all load values up to -j 12. Under CFS the number of frame drops significantly increases after -j 4."
  - §7.4, p. 20: "mplayer frame rate drops to almost 8 frame per second under CFS when 12 parallel compilation is running, while at the same load level CFS with RBPE shows almost no frame rate reduction."
- **Coverage.**
  - T6: covers. Workload: Linux kernel compilation (tree version not stated) with `-j` 1–14 on a single-CPU Pentium 4 workstation, Fedora 12, kernel 2.6.32 CFS; used as load for Apache, MySQL and mplayer response tests; no process data.
  - T7: partial — a kernel compile at `-j` ≥ 5 makes a 25 fps video "not viewable" under stock CFS on that single core (their observation), which is a desktop-batch-job-vs-interactive characterisation without thread/utilisation numbers.
  - T1, T2, T3: do not cover. T4, T5, T8: do not cover.
- **One observation?** One named machine, one unnamed tree, three repetitions per `-j`.

### S1-22 — Krishnaswamy, "Automatic Precompiled Headers: Speeding up C++ Application Build Times", USENIX WIESS 2000

- **Citation.** Tara Krishnaswamy (HP, Internet & IA-64 Foundations Lab). *Automatic Precompiled Headers: Speeding up C++ Application Build Times.* First Workshop on Industrial Experiences with Systems Software (WIESS 2000), San Diego, October 22, 2000. 10 pages.
- **Copy read.** `https://www.usenix.org/legacy/publications/library/proceedings/osdi2000/wiess2000/full_papers/krishnaswamy/krishnaswamy.pdf`, as served 2026-09-14; local `sources/S1-22/krishnaswamy-2000.pdf`; SHA-256 `42c9f7fceb778b1c4d5d28ea591ffcc96361c39602afd9aff9f32a8d0d40321c`.
- **Passages.**
  - §2, p. 2: "The table shows that on average about 87% of the application's code resides in header files."
  - §2, p. 2: "Table 3 reports the compile-time division between actual source line processing and header processing. Note that the processing times for the header files serve only as a lower bound although they represent actual compile-times due to the fact that these numbers were gathered only for headers continuously #include-ed at the head of the source files."
  - Table 3, p. 2 (columns: Application, Compile time of preprocessed lines (secs), Compile time of header lines (secs), % time spent compiling headers): "Perl 7.3 3.9 53 / Class Library 17.2 17.1 72 / Ray Tracer 44.7 38.1 85 / CAD 38.7 31.3 80 / Web Browser 14.6 14 95 / Linker 85.8 77.6 90 / Optimizer 194.2 146.5 75 / Business Planner 70.5 34.6 49" (the "Class Library" and "Web Browser" header-time cells exceed the percentage shown; I quote the table as printed and do not resolve the inconsistency.)
  - §2, p. 2: "Table 3 clearly demonstrates that a large part of the compile times of these applications is spent in processing the #include header files."
- **Coverage.**
  - T2: partial. Object: total compile time of eight C++ applications (the table is per application, not per translation unit) with HP aCC, split into header processing vs source processing; unit seconds; machine and aCC version not named in the quoted text. It is the only literature I found with measured compile-time composition, but it is per application, ca. 2000, C++ on HP-UX, and says nothing about CPU-vs-blocked time or per-TU distributions.
  - T1, T3, T6, T7: do not cover. T4, T5, T8: do not cover.
- **One observation?** Eight applications, one compiler; machine and window not stated.

### S1-23 — Ross, Abel, "An Evaluation of the Linux Scheduler for Single User Workstations", Harvard CS261 course paper, 15 January 2000 (not peer-reviewed)

- **Citation.** Russ Ross, Deborah Abel (Harvard). *An Evaluation of the Linux Scheduler for Single User Workstations.* Course paper, January 15, 2000. 11 pages.
- **Copy read.** `http://static.russross.com/papers/cs261.pdf`, as served 2026-09-14; local `sources/S1-23/ross-abel-2000.pdf`; SHA-256 `206df1b30366fb3b7ac828f8035c8552604ae94aa35e570dce9d83ae3ca6e69e`.
- **Passages.**
  - §4.1, p. 4: "We instrumented the Linux 2.2.13 kernel to trace scheduling events and record when processes become blocked, ready, or running."
  - §4.1, p. 4: "The second piece of the software involves simply recording important process data such as PID, creation time, and parent information. This gives us a connection between PIDs and executables and also parent/children information for determining which processes are related to each other (e.g. descendants of make are all part of the same compile job)."
  - §4.1, p. 4: "We work from two traces, the first of which lasted 31 minutes and produced 11,127 process accounting records, 2,763,197 scheduling events, and 104 focus events."
  - §4.2, p. 5: "We began with a 31-minute trace on a machine with an AMD K6-2 300 MHz processor with 128 MB RAM running our trace-enabled Linux 2.2.13 kernel based on RedHat Linux 6.1. This trace contained an intentionally heavy workload to find and amplify latency issues. The three most important process families were a kernel compile, an mp3 encoding, and a session with LyX"
  - §5.2.1, p. 6: "However, Metafont was in great contention with the compile going on, and the compile won. Metafont didn't really get to run until after the compile had completed"
- **Coverage.**
  - T1: partial — 11,127 process accounting records in a 31-minute desktop trace whose largest process family was a kernel compile (`-j` not stated); no split by family is quoted.
  - T6: covers as a 2000-era desktop trace with a kernel compile plus mp3 encoding as the batch jobs, on a named machine (K6-2 300 MHz, Linux 2.2.13); scheduling and BSD process accounting collected (T8-adjacent: shows the accounting data was obtainable on 2.2).
  - T7: partial — "an mp3 encoding" as a CPU-saturating desktop batch job, no numbers.
  - T2, T3: do not cover. T4, T5, T8: do not cover.
- **One observation?** Two traces (31 min and 17 min) on one named machine. Course paper, not peer-reviewed.

### S1-24 — Zheng, Wu, Fu, Yu, Mao, Ma, Williams, Wang, Quinn, "ActPlane: Programmable OS-Level Policy Enforcement for Agent Harnesses", arXiv 2606.25189

- **Citation.** Yusheng Zheng, Tianyuan Wu, Quanzhi Fu, Tong Yu, Wenan Mao, Tao Ma, Dan Williams, Wei Wang, Andi Quinn. *ActPlane: Programmable OS-Level Policy Enforcement for Agent Harnesses.* arXiv:2606.25189v2 [cs.OS], 30 Jun 2026. 16 pages.
- **Copy read.** `https://arxiv.org/pdf/2606.25189` (v2), as served 2026-09-14; local `sources/S1-24/actplane-2606.25189.pdf`; SHA-256 `59c2b86a375aa637abe0e4e4630b0b56affc540fa34dfbf2234493f63573220a`.
- **Passages.**
  - §5.1, p. 8: "All experiments run on a machine with an Intel Core Ultra 9 285K CPU with 24 hardware cores, 125 GiB RAM, and Linux 6.15.11."
  - §5.4.1, p. 10: "The second is a Linux kernel build using defconfig plus vmlinux with make -j24 on a clean output directory. Each workload runs three trials per configuration"
  - §5.4.1, p. 10: "At 32 active rules, ActPlane adds 1.9% overhead on the agent-trace replay and 6.5% on the Linux kernel build, and at 100 rules, overhead remains below 8.4%. The agent-trace workload exhibits lower overhead because tool actions are interspersed with model inference pauses that dwarf syscall cost, whereas the kernel build stresses sustained I/O and process creation, exposing more of ActPlane's per-event cost."
  - Table 3 "Per-operation latency in microseconds for no-hit configurations. Values are medians across seven trials.", p. 10 (columns Native p50, AP-1 p50, AP-32 p50, AP-100 p50): "fork 48.94 52.06 74.05 69.33 / exec 248.30 263.95 314.86 317.03"
- **Coverage.**
  - T1: partial — native fork (48.94 µs) and exec (248.30 µs) median latencies on a named desktop CPU (Core Ultra 9 285K, Linux 6.15.11), pinned to one core; the kernel build is described as stressing "sustained I/O and process creation"; no process counts.
  - T6: covers as a workload description: Linux `defconfig` + `vmlinux`, `make -j24` (= hardware-core count), clean output directory, three trials; the kernel tree version is not stated; used to measure a BPF policy engine's overhead.
  - T4: `-j24` on 24 hardware cores (noted).
  - T2, T3, T7: do not cover. T5, T8: do not cover.
- **One observation?** One machine (named), one build configuration; window = one build (duration not stated).

### S1-25 — Chandra, Adler, Goyal, Shenoy, "Surplus Fair Scheduling: A Proportional-Share CPU Scheduling Algorithm for Symmetric Multiprocessors", OSDI 2000 (HTML)

- **Citation.** Abhishek Chandra, Micah Adler, Pawan Goyal, Prashant Shenoy. *Surplus Fair Scheduling: A Proportional-Share CPU Scheduling Algorithm for Symmetric Multiprocessors.* 4th USENIX OSDI, San Diego, October 2000. HTML version.
- **Copy read.** `https://www.usenix.org/events/osdi2000/full_papers/chandra/chandra_html/index.html`, as served 2026-09-14; local `sources/S1-25/chandra-osdi2000.html` (+ `.txt`); SHA-256 `1b056f014b99202871396cf8d0e4fa8b62b3e7ede8f572a5d08e6af4bbecc579`.
- **Passages.**
  - §4.1 Experimental Setup: "The test-bed for our experiments consisted of a 500 MHz Pentium III-based dual-processor PC with 128 MB RAM, 13GB SCSI disk, and a 100 Mb/s 3-Com ethernet card (model 3c595). The PC ran the default installation of Red Hat Linux 6.0. We used version 2.2.14 of the Linux kernel for our experiments"
  - §4.4: "Simultaneously, we ran a varying number of gcc compile jobs, each with a weight of 1. The scenario represents video playback in the presence of background compilations; running multiple compilations simultaneously corresponds to a parallel make job (i.e., make -j) that spawns multiple independent compilations in parallel."
  - §4.4: "We hypothesize that the slight decrease in the frame rate in SFS is caused due to the increasing number of intermediate files created and written by the gcc compiler, which interferes with the reading of the MPEG-1 file by the decoder."
- **Coverage.**
  - T6: partial — independent gcc compile jobs standing in for `make -j` as background load on a dual-Pentium III, Linux 2.2.14; no process or lifetime data.
  - T2: one qualitative remark that gcc's intermediate-file writes interfere with a reader's I/O.
  - T1, T3, T7: do not cover. T4, T5, T8: do not cover.
- **One observation?** One machine (named); the compiled sources are not named.

### S1-26 — Traeger, Zadok, Joukov, Wright, "A Nine Year Study of File System and Storage Benchmarking", ACM Transactions on Storage 4(2), 2008

- **Citation.** Avishay Traeger, Erez Zadok (Stony Brook University), Nikolai Joukov, Charles P. Wright (IBM T. J. Watson). *A Nine Year Study of File System and Storage Benchmarking.* ACM Transactions on Storage 4(2), Article 5, May 2008. 56 pages.
- **Copy read.** Author copy `https://www.fsl.cs.stonybrook.edu/docs/fsbench/fsbench.pdf` (ACM TOS layout), as served 2026-09-14; local `sources/S1-26/traeger-fsbench.pdf`; SHA-256 `79ec01a29579d5c9413b3a1865d71180721d4dd7c338e32807fc8ccb91de3fe8`. PDF page n = printed "5:n".
- **Passages.**
  - Abstract, p. 1: "As a specific example, slowing down read operations on ext2 by a factor of 32 resulted in only a 2–5% wall-clock slowdown in a popular compile benchmark."
  - §7.2 Compile Benchmarks, p. 18: "The main problem with compile benchmarks is that because they are CPU intensive, they can hide the overheads in many file systems."
  - Table III, p. 19 ("SSH 2.1.0, Am-Utils 6.1b3, and Linux Kernel 2.4.20 Characteristics", column Linux Kernel): "Directories 608 / Files 11,352 / Lines of Code 4,490,349 / Code Size (Bytes) 126,735,431 / Total Size (Bytes) 174,755,840"
  - §7.2, p. 19: "Using OSprof [Joukov et al. 2006], we profiled the build process of three packages commonly used as compile benchmarks: (1) SSH 2.1.0; (2) Am-utils 6.1b3; and (3) the Linux 2.4.20 kernel with the default configuration. … Before the configuration- and compilation phases, we remounted the ext2 file system on which the benchmark was run, to reduce caching effects."
  - §7.2, p. 20: "the read-write ratio for the Am-utils build was 0.75:1, whereas it was 1.28:1 for the SSH build. … Not surprisingly, the kernel-build process profile differs from both SSH and Am-utils. As can be seen in Figure 4(c), both of the kernel-build phases are strongly read biased. In addition, the kernel-build process is more intensive in file-open and file-release operations."
  - §12.2 Hiding Overheads, p. 44: "Compile benchmarks. In our first experiment, we compared Slowfs and ext2 for configuring and compiling OpenSSH versions 3.5, 3.7, and 3.9. We used Slowfs with the read operation slowed down by several factors. … Because a compile benchmark is CPU intensive, such extraordinary overheads as a factor of 32 on read can go unnoticed (the factor of 32 comes from setting N to 5, as described in Section 12.1). For all of these graphs, the half-widths were less than 1.5% of the mean, and the CPU % was always more than 99.2%, where CPU % = (time user + time system) / time elapsed × 100."
  - §12.2, p. 45: "For the configure phase, the highest overhead was 2.7% for elapsed time, and 10.1% for system time (both for version 3.7). For the compile phase, the highest overhead was 4.5% for elapsed time and 59.2% for system time (both for version 3.5)."
  - §12.2, p. 45: "These results clearly show that even with extraordinary delays in critical file system operations, compile benchmarks show only marginal overheads because they are bound by CPU time spent in user space."
- **Coverage.**
  - T2: covers the "blocked on file I/O" question at build level (not per compiler process): with the ext2 file system remounted before each phase ("to reduce caching effects", i.e. a cold-ish cache), an OpenSSH 3.5/3.7 build ran at CPU% > 99.2% of elapsed time, and a 32× slowdown of every read cost ≤ 4.5% elapsed (≤ 59.2% system time). The build is therefore CPU-bound throughout at whole-build granularity; the machine for this experiment is described in §12.1 (not quoted — I did not extract it) and the build was single-job (no `-j` mentioned). Also: VFS-operation mix of a Linux 2.4.20 `defconfig` build — "strongly read biased", open/release-intensive (counts in Figure 4(c) only).
  - T6: partial — surveys that 33 of 106 file-system papers used compile benchmarks (8 an OS kernel), and gives the kernel-2.4.20 tree size (11,352 files).
  - T1, T3, T7: do not cover. T4, T5, T8: do not cover.
- **One observation?** §12.2: OpenSSH 3.5/3.7/3.9 builds on ext2 vs Slowfs, several read-slowdown factors, half-widths reported; machine named only in §12.1 (unread). Figure 4: one build each of three packages.

### Identified but not read (no passage; listed so the gap is explicit)

- **Belinassi, Biener, Hubička et al. "Compiling Files in Parallel: A Study with GCC."** SBAC-PADW 2022, IEEE Xplore 9978516. Per the Scholar/ResearchGate snippets it measures GCC self-compilation with `make -j` parallelism vs intra-file LTO parallelism and integrates with the make jobserver — directly T3. IEEE page returns a 202 bot page; no arXiv, author or USP copy found (rows 31, 41, 46, 51). Cannot be quoted.
- **Kubota, Suzuki, Kono. "To unify or not to unify: a case study on unified builds (in WebKit)."** CC 2019, DOI 10.1145/3302516.3307347. Per its abstract snippet it measures per-compiler-task build and incremental-build times for WebKit (T2). ACM PDF 403; author page links only to ACM (rows 40, 45, 47, 51).
- **Uluski, Moffie, Kaeli. "Characterizing antivirus workload execution."** SIGARCH CAN 33(1), 2005. Per snippets: four AV packages on a Pentium 4 / Windows XP under Simics, on-access overhead 23–129% (T7). ACM 403, ResearchGate 403, kipdf 403 (rows 21, 32, 44, 51).
- **Dogonyaro, Victor, Shafii et al. "Comparative performance analysis of anti-virus software."** ICTA 2020 (FUTMINNA repository). Institutional server timed out (rows 39, 51). Would be the only found source on full-scan durations; unverified.
- **Leland, Ott. "Load-balancing heuristics and process behavior."** SIGMETRICS/Performance 1986. Known only through S1-07's summary (9.5 million UNIX processes, Pr{L > T} = rT^k, −1.25 < k < −1.05 for T > 3 s). No open copy (row 12).
- **Linköping thesis "Linux Kernel Scheduler Evaluation for Performance-…" (diva2:1972665).** Snippet mentions EEVDF and sched_ext evaluation; diva-portal unreachable (rows 11, 30).
- **Flautner, Uhlig, Reinhardt. "Thread-level parallelism of desktop applications."** MTEAC 2000. umich.edu TLS failure in this container (row 37). Desktop-application TLP, marginal for T7.

## 3. Not found

- **T1 — per-process lifetime or CPU-time distributions inside a parallel build, and per-type process counts (cc1/as/ld/collect2/sh/fixdep/genksyms/modpost).** No peer-reviewed or preprint document found that breaks a build's process population down by role or gives a lifetime histogram. The nearest data: S1-01 (2430 processes, "mostly short-lived", `make -j8` DynamoRio, one laptop), S1-18 (815 / 748 processes for bash `make -j20`, mean exec-to-exit lifetime "more than 2 seconds", mean fork-to-exec "< 1 ms"), S1-05 (traced fork/exec sequences with the longest visible task ≈ 20 ms in a sequential phase of a kernel build), S1-02/S1-03/S1-12 (qualitative: "more processes than cores", "enormous number of short-lived processes like cp and mkdir", "a large number of processes and threads"). Searches 3, 24, 33, 38, 43 established this.
- **T2 — CPU time per compilation across a project (histogram/percentiles) and the blocked-on-I/O share of a compiler process under warm vs cold cache.** Nothing per translation unit. The only measured composition is S1-22 (per-application header vs source compile time, HP aCC, 2000). The only I/O-blocking evidence is at whole-build granularity: S1-26 (OpenSSH build > 99.2% CPU-bound on a remounted ext2; 32× read slowdown → ≤ 4.5% elapsed) and S1-08 (user 130.6 s vs system 71.3 s for a `-j14` kernel build; single-threaded final link). No run/wait/run structure inside a compiler process appears anywhere. Searches 5, 15, 23, 27, 28, 40, 48, 50, 53.
- **T3 — make's own CPU cost per dispatched job, the jobserver's behaviour under load, and the live-process-count-vs-N relation.** No measurement in the literature reached. S1-09 gives 1990s no-op-build costs (10 s stat work for 1000 files on a 66 MHz i486; +15 s for 100 recursive sub-makes) and S1-10 an unmeasured claim that ninja's driver cost is "relatively little"; the one paper that measures jobserver-integrated parallel compilation (Belinassi 2022) is paywalled. Nothing on ninja or cargo dispatch in literature (Scholar row 52: zero results). Searches 4, 25, 31, 35, 46, 49, 52, 54.
- **T6 — kernel scheduler feature documentation (autogroup, child-runs-first) as literature; sched_ext/EEVDF/BORE evaluations with process-level data.** Autogroup appears only as S1-06's explanation of the Group Imbalance bug (per-thread load ÷ 64 for a 64-job make) and its being disabled for another experiment; no paper evaluates child-runs-first. Kernel-compile-as-workload papers found (S1-02, S1-04, S1-05, S1-06, S1-08, S1-12, S1-18, S1-19, S1-20, S1-21, S1-24, S1-25) report machine and `-j` but never process counts or lifetime distributions beyond S1-18. General process-lifetime studies: only S1-07 (1990s academic UNIX, `lastcomm`), plus the unread Leland & Ott 1986; no Linux-era desktop study. Searches 11, 19, 22, 26, 36 (arXiv API 429), 37, 43.
- **T7 — antivirus full-scan, file-indexer rescan and desktop CPU training jobs characterised by thread count, sustained utilisation and duration; process-treatment catalogues assigning classes to compilers/batch jobs.** No open paper characterises a full antivirus scan (S1-13 is on-access overhead on a netbook; Uluski 2005 and Dogonyaro 2020 unreachable). No academic source on desktop indexers at all (search 34). Video encode: S1-15 (ffmpeg 16 threads on 16 vCPUs, ~65 s, server), S1-14 and S1-16 (x264 threading model and f = 0.888, no utilisation). ML training: S1-17 (60–63% system-wide CPU utilisation, unnamed machine). No literature on ananicy or distribution nice/ionice catalogues (search 26 and the general searches returned only S2-class primary sources). Searches 9, 10, 14, 20, 21, 29, 32, 34, 39, 42, 44.
- **T4, T5, T8** — not my class; no paper read covers DKMS (T5) or runner observability (T8). T4 surfaced incidentally only as each paper's own `-j` choice (S1-02: 2 × cores; S1-04: 172 on 86 cores; S1-05: 320 on 160 threads; S1-06: 64 on 64 cores; S1-24: 24 on 24 cores; S1-20: the 2009 "oversubscribe" folk rule).
