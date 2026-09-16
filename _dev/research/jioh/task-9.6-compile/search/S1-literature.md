# S1 — peer-reviewed and preprint literature (T1–T7), task 9.6 compile, stage 2 search

Reader: S1. Access date for every source: 2026-09-16. Copies saved under `sources/S1-NN/` (gitignored; the record is self-sufficient — every value a reader needs is in the quoted passages and copy identification below).

Tooling used for text extraction: `pdfminer.six 20260107` (`extract_text`, default LAParams) in a venv; `curl -sSL` through the session proxy; SHA-256 via `sha256sum`. Where a PDF's text layer is unreadable the record says so.

Network probe (2026-09-16, before searching): usenix.org 200; arxiv.org 200; api.openalex.org 200; dblp.org 200; api.semanticscholar.org **429** (rate-limited on first request); dl.acm.org **403**; ieeexplore.ieee.org **202** with 0-byte body (challenge page); scholar.google.com **403**.

## 1. Search log

| # | Date | Engine / venue | Exact query or URL | Hits followed | Dead ends (HTTP status) |
|---|------|----------------|--------------------|---------------|-------------------------|
| 1 | 2026-09-16 | usenix.org direct URL | `https://www.usenix.org/system/files/conference/atc17/atc17-ocallahan.pdf` | — | 404 (HTML "page not found") |
| 2 | 2026-09-16 | arxiv.org direct | `https://arxiv.org/abs/1705.05937`, `https://arxiv.org/pdf/1705.05937` | S1-01 (rr, extended arXiv version) | — |
| 3 | 2026-09-16 | arxiv.org direct | `https://arxiv.org/abs/1203.2704`, `https://arxiv.org/pdf/1203.2704` | S1-02 (Coetzee et al.) | — |
| 4 | 2026-09-16 | arxiv.org direct | `https://arxiv.org/abs/2509.01245`, `https://arxiv.org/pdf/2509.01245` | S1-03 (SchedCP) | — |
| 5 | 2026-09-16 | usenix.org direct | `https://www.usenix.org/legacy/event/usenix06/tech/full_papers/jones/jones.pdf` | S1-04 (Antfarm) | — |
| 6 | 2026-09-16 | usenix.org direct | `https://www.usenix.org/system/files/atc20-gouicem.pdf` | S1-05 (Gouicem et al.) | — |
| 7 | 2026-09-16 | author site direct | `https://www.ece.ubc.ca/~sasha/papers/eurosys16-final29.pdf` | — | 200 but body is an HTML page (31 093 B), not the PDF |
| 8 | 2026-09-16 | usenix.org direct | `https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Boyd-Wickizer.pdf` | S1-07 (Boyd-Wickizer et al.) | — |
| 9 | 2026-09-16 | author lab site direct | `https://www.fsl.cs.sunysb.edu/docs/fsbench/fsbench.pdf` | S1-08 (Traeger et al.) | — |
| 10 | 2026-09-16 | author site direct | `https://www.cs.cmu.edu/~harchol/Papers/tocs.pdf` | — | 404 |
| 11 | 2026-09-16 | usenix.org presentation page | `https://www.usenix.org/conference/atc17/technical-sessions/presentation/ocallahan` → PDF link `…/atc17-o_callahan.pdf` | S1-01 (rr, ATC '17 proceedings PDF) | — |
| 12 | 2026-09-16 | HAL API | `https://api.archives-ouvertes.fr/search/?q=title_t:"Decade of Wasted Cores"` → `https://hal.science/hal-01295194/document` | S1-06 (Lozi et al.) | — |
| 13 | 2026-09-16 | author site index | `https://www.cs.cmu.edu/~harchol/Papers/` → `TOCS.pdf` | S1-09 (Harchol-Balter & Downey) | — |
| 14 | 2026-09-16 | OpenAlex API | `https://api.openalex.org/works?search=Exploiting process lifetime distributions…` (and five other titles) | — | JSON error `"Rate limit exceeded" … "Insufficient budget … $0 remaining"` on every query; OpenAlex unusable this session |
| 15 | 2026-09-16 | Semantic Scholar API | `https://api.semanticscholar.org/graph/v1/paper/search?query=test` | — | 429 on the first request; not retried |
| 16 | 2026-09-16 | Crossref API | `query.bibliographic=Load-balancing heuristics and process behavior` | DOI 10.1145/317499.317539 (Leland & Ott, SIGMETRICS '86) → row 22 | — |
| 17 | 2026-09-16 | Crossref API | `query.bibliographic=Characterizing antivirus workload execution` | DOI 10.1145/1055626.1055639 (Uluski, Moffie, Kaeli, SIGARCH CAN 33(1), 2005) → rows 22, 25 | — |
| 18 | 2026-09-16 | Crossref API | `query.bibliographic=Belinassi parallel GCC` | DOI 10.1109/sbac-padw56527.2022.00011 "Compiling Files in Parallel: A Study with GCC" (SBAC-PADW 2022) → rows 22, 24 | — |
| 19 | 2026-09-16 | Crossref API | `query.bibliographic=unity builds compile time Kubota` | DOI 10.1587/transinf.2020edp7105 "Native Build System for Unity Builds with Sophisticated Bundle Strategies" (IEICE Trans. Inf. & Syst., 2021) → row 22 | — |
| 20 | 2026-09-16 | Crossref API | `query.bibliographic=SCHED_AUTOGROUP`; `…=kernel compilation scheduler workload processes short-lived` | — | first returned only dictionary entries (no hit); second 429 |
| 21 | 2026-09-16 | dblp search API | `https://dblp.org/search/publ/api?q=Uluski antivirus&format=json` (and four other queries) | — | 200 but body is an Anubis "Making sure you're not a bot!" challenge page; one query 429. dblp unusable |
| 22 | 2026-09-16 | arXiv API | `https://export.arxiv.org/api/query?search_query=all:"kernel compilation" AND all:scheduler` (and five other queries) | — | http:// gave 301; https:// gave 429 on all six queries (rate-limited) |
| 23 | 2026-09-16 | publisher DOI probes | `https://dl.acm.org/doi/10.1145/317499.317539`; `https://dl.acm.org/doi/10.1145/1055626.1055639`; `https://doi.org/10.1109/sbac-padw56527.2022.00011`; `https://doi.org/10.1587/transinf.2020edp7105`; jstage `_pdf` | S1-10 (Kubota, jstage PDF 200) | ACM DL 403 (both); IEEE Xplore 202 with 0-byte body (challenge) for 9978516 and 9980836 |
| 24 | 2026-09-16 | WebSearch | `"Compiling Files in Parallel: A Study with GCC" Belinassi pdf` | ResearchGate (request-only), IEEE 9978516, computer.org CSDL — no open PDF | — |
| 25 | 2026-09-16 | WebSearch | `Uluski "Characterizing antivirus workload execution" pdf` | ResearchGate author-profile PDF link → S1-11 | — |
| 26 | 2026-09-16 | WebSearch | `Leland Ott 1986 "Load-balancing heuristics and process behavior" pdf` | — | no open copy surfaced; ACM DL 403 (row 23). Its findings are quoted second-hand from S1-09 |
| 27 | 2026-09-16 | WebSearch | `paper measurement "make -j" kernel build "process lifetimes" OR "short-lived processes" fork exec trace distribution` | — | only blog posts / tool pages (execsnoop, forkstat, eBPF); no paper |
| 28 | 2026-09-16 | WebSearch | `Linux "autogroup" OR "sched_autogroup" scheduler "kernel build" OR "make -j" paper evaluation interactivity` | — | only kernel source, LKML RFC docs, man-page text (documentation — S2's class); no peer-reviewed or preprint evaluation |
| 29 | 2026-09-16 | direct fetch | `https://www.jstage.jst.go.jp/article/transinf/E104.D/1/E104.D_2020EDP7105/_pdf` | S1-10 (Kubota & Kono) | — |
| 30 | 2026-09-16 | direct fetch (browser UA) | ResearchGate author-profile PDF link for Uluski et al. (from row 25) | — | 403 (HTML), also 403 via WebFetch |
| 31 | 2026-09-16 | direct fetch | `https://aegis.sourceforge.net/auug97.pdf` (Miller, "Recursive Make Considered Harmful") | S1-12 | — |
| 32 | 2026-09-16 | direct fetch | `https://www.microsoft.com/en-us/research/uploads/prod/2018/03/build-systems.pdf` (Mokhov, Mitchell, Peyton Jones, ICFP 2018) | S1-13 | — |
| 33 | 2026-09-16 | WebSearch | `Belinassi "Parallelizing GCC" OR "paralelização do GCC" dissertação USP pdf jobserver` | USP Lattes pages, GSoC final report on gcc.gnu.org (mailing list — S2's class) | no open PDF of the SBAC-PADW 2022 paper or a thesis |
| 34 | 2026-09-16 | WebSearch | `empirical study C++ "compile time" per "translation unit" distribution LLVM OR Clang OR GCC percentiles paper` | — | no paper on per-TU compile-time distributions surfaced (only compiler-comparison blogs, a bug study) |
| 35 | 2026-09-16 | WebSearch | `"make -j" optimal number of jobs study "kernel" compile cores speedup measurement paper 2 x nproc` | — | forums, kcbench man page, LKML threads only (S2/S3 classes); no paper |
| 36 | 2026-09-16 | WebSearch | `x264 encoder "frame-level" threading parallel efficiency "cores" characterization paper CPU utilization` | ResearchGate (request-only) H.264-on-hyper-threading paper; QUB task-based H.264 encoder PDF (not x264) | no open x264 characterisation with thread count / sustained utilisation followed |
| 37 | 2026-09-16 | WebSearch | `energy DVFS study "kernel compilation" OR "linux kernel build" workload "number of cores" "make -j" processes measurement paper` | — | DVFS-governor papers without a kernel-build workload; nothing followed |
| 38 | 2026-09-16 | WebSearch | `DKMS "dkms autoinstall" kernel module rebuild study OR paper OR measurement duration` | — | only wikis, man pages, bug reports (S2/S3 classes); no literature |
| 39 | 2026-09-16 | WebSearch | `nucar northeastern Kaeli Uluski Moffie antivirus workload characterization Simics Pentium 4 Windows XP pdf` | NUCAR research/antivirus page and publications page (probed in row 41) | — |
| 40 | 2026-09-16 | WebSearch | `paper measurement compiler "cold cache" OR "page cache" "compile time" headers I/O wait "CPU-bound" gcc OR clang build study` | — | blogs and compiler manuals only; no measurement paper |
| 41 | 2026-09-16 | WebSearch | `"taskset" OR "cgroup" OR "cpu quota" "kernel build" OR "make -j" "single core" OR "one core" slowdown processes measurement paper OR thesis` | arXiv 1705.05937 (already S1-01) | nothing else in the literature class |
| 42 | 2026-09-16 | lab page probe | `https://ece.northeastern.edu/groups/nucar/research/antivirus/` → link `http://www.ece.neu.edu/groups/nucar/publications/uluski.pdf` | S1-11 (Uluski et al., if the PDF resolves — see S1-11) | — |
| 43 | 2026-09-16 | Crossref API | `query.bibliographic=Exploiting process lifetime distributions dynamic load balancing` + `query.container-title=Transactions on Computer Systems` | DOI 10.1145/263326.263344 (TOCS 15(3):253–285, 1997) — citation for S1-09 | — |

## 2. Candidates

### S1-01 — O'Callahan et al., "Engineering Record and Replay for Deployability" (USENIX ATC '17; extended arXiv:1705.05937)

**Citation.** Robert O'Callahan, Chris Jones, Nathan Froyd, Kyle Huey, Albert Noll, Nimrod Partush. "Engineering Record And Replay For Deployability." Proceedings of the 2017 USENIX Annual Technical Conference (USENIX ATC '17), Santa Clara, CA, July 2017, pp. 377–389. Extended version: arXiv:1705.05937v1 (submitted 16 May 2017).

**Copies read.**
- `https://www.usenix.org/system/files/conference/atc17/atc17-o_callahan.pdf` (proceedings PDF, 525 825 bytes), accessed 2026-09-16, saved as `sources/S1-01/atc17-o_callahan.pdf`, SHA-256 `589ec37978260f968312288061e710e64b58e2e652c8479649694403ac037772`.
- `https://arxiv.org/pdf/1705.05937` (v1, 425 129 bytes), accessed 2026-09-16, saved as `sources/S1-01/arxiv-1705.05937.pdf`, SHA-256 `f348cc0a1fea3665edab4310208b57b896cf7fbac763e502a51fa7e688794e21`; abstract page `https://arxiv.org/abs/1705.05937` saved as `arxiv-1705.05937-abs.html`, SHA-256 `229417e8dd8df699c631c21fc3b0d95e5897afd138059e02f0166611df2820f1` (shows "[v1] Submitted on 16 May 2017"; only one version).
- The predecessor arXiv:1610.02144 was not fetched (the ATC paper and 1705.05937 carry the same §4 text and Table 1; verified by grep on both extractions).

**Verbatim passages** (ATC '17 PDF; the arXiv v1 text is identical for these passages except the citation number "[11]" instead of "[8]").

§4.1 Workloads, p. 382–383:
> "Benchmarks were chosen to illuminate RR's strengths and weaknesses, while also containing representatives of real-world usage. They were tuned to fit in system memory (to minimize the impact of I/O on test results), to run for about 30 seconds each (except for cp where a 30s run time would require it to not fit in memory)."

> "make builds DynamoRio [8] (version 6.1.0) with make -j8 (-j8 omitted when restricting to a single core). This tests potentially-parallel execution of many short-lived processes."

> "All tests run on a Dell XPS15 laptop with a quad-core Intel Skylake CPU (8 SMT threads), 16GB RAM and a 512GB SSD using Btrfs in Fedora Core 23 Linux."

§4.2 Overhead, p. 383:
> "Each test was run six times, discarding the first result and reporting the geometric mean of the other five results. Thus the results represent warm-cache performance."

> "“Single core” reports the overhead of just restricting all threads to a single core using Linux taskset."

§4.3 Observations, p. 383:
> "Overhead on make is significantly higher than for the other workloads. Forcing make onto a single core imposes major slowdown. Also, make forks and execs 2430 processes, mostly short-lived. (The next most prolific workload is sambatest with 89.) In-process system-call interception only starts working in a process once the interception library has been loaded, but at least 80 system calls are performed before that completes, so its effectiveness is limited for short-lived processes."

> "octane is the only workload here other than make making significant use of multiple cores, and this accounts for the majority of RR's overhead on octane."

Table 1 "Run-time overhead", p. 384 (row for make; columns as printed: Workload, Baseline duration, Record, Replay, Single core, Record no-intercept, Replay no-intercept, Record no-cloning, DynamoRio-null; read from the PDF page in pypdf layout mode):
> "make 20.99s 7.85× 11.93× 3.36× 11.32× 14.36× 7.84× 10.97×"

§4.5 Memory usage, p. 385:
> "In make, just running on a single core reduces peak PSS significantly because not as many processes run simultaneously."

**Coverage.**
- T1 — covers, coarsely: object = processes forked-and-exec'd by one `make -j8` build of DynamoRio 6.1.0; unit = count per build; statistic = total (2430) with the qualitative "mostly short-lived"; scope = one build on one laptop; population = that build's processes. No per-process lifetime or CPU-time distribution, no breakdown by program (cc1, as, ld…).
- T2 — does not cover.
- T3 — does not cover.
- T4 — does not cover (the paper's own choice, `-j8` on 8 SMT threads, is a choice, not an observation of users).
- T5 — does not cover.
- T6 — covers: the same build run confined to one core with `taskset` (with `-j8` omitted, i.e. a serial make) takes 3.36× the wall-clock of the unconfined `-j8` baseline of 20.99 s (warm cache, geometric mean of five runs), with peak PSS reduced "because not as many processes run simultaneously". No process-lifetime or CPU-total comparison between the two runs is reported. Also a scheduler-adjacent evaluation using a build as workload.
- T7 — does not cover.
- **One observation**: yes — one machine (Dell XPS15, quad-core Skylake, 8 SMT threads, 16 GB, 512 GB SSD, Btrfs, Fedora 23), one subject (DynamoRio 6.1.0, `make -j8`; serial make when pinned), window ≈ 21 s baseline (six runs, first discarded).

### S1-02 — Coetzee, Bhaskar, Necula, "A model and framework for reliable build systems" (arXiv:1203.2704, 2012)

**Citation.** Derrick Coetzee, Anand Bhaskar, George Necula. "A model and framework for reliable build systems." arXiv:1203.2704v1 [cs.SE], submitted 13 March 2012 (also UC Berkeley EECS technical report EECS-2012-27; the TR copy was not fetched).

**Copy read.** `https://arxiv.org/pdf/1203.2704` (v1, 137 292 bytes), accessed 2026-09-16, saved as `sources/S1-02/arxiv-1203.2704.pdf`, SHA-256 `637cbce65f2ceceed18434f59efadbfd54dc3bdcfdc85ee5f6cb75fd4ae882b9`; abstract page saved as `arxiv-1203.2704-abs.html`, SHA-256 `607f1014e1e46c2fc4e5e4ebc9748faa626ed2dc0f5ce4b64dbeabcc8400aec4` ("[v1] Submitted on 13 Mar 2012", single version).

**Verbatim passages.**

§8 Task and resource granularity:
> "Generally the most fine-grained task possible is an execution of a build process, since such tasks cannot be easily subdivided. However, the intuitive association of a single process with a task may be counterproductive: a large number of processes leads to a large number of tasks and a large dependency graph which takes more time to construct and analyze."

§9 Preliminary experimental results:
> "In the first, a ptrace-based prototype that could only perform full builds, a pessimistic locking scheme was used where build processes took locks on any files they accessed. […] Given enough concurrent processes, this build scaled to 85% the time of a parallel make build of the Linux kernel. However, it was not a complete system, as it was unable to handle unexpected new dependencies, could not perform incremental builds, and inferred its list of processes to execute from a prior make run, making it necessary to rerun the make build whenever this process sequence was changed."

> "In practice, even with caching, the system added too much overhead to be practical due to the Linux kernel build's enormous number of short-lived processes like cp and mkdir. This is less likely to be an issue in a more monolithic build system."

> "The second prototype was based on multiversion timestamping and was able to handle process hierarchies. Instead of replacing make, make is run sequentially and children of make are run speculatively, pretending to succeed so that make will continue and begin the next process."

**Coverage.**
- T1 — covers only qualitatively: names the Linux kernel build's "enormous number of short-lived processes like cp and mkdir"; no count, no lifetime, no CPU figure, no kernel version, no `-j`, no machine.
- T2, T3, T4, T5, T6, T7 — does not cover (the §9 "85% the time of a parallel make build" is the prototype's time relative to make, with neither absolute times nor `-j` given).
- **One observation**: no quantified observation; machine, kernel version, configuration and `-j` are all unnamed.

### S1-03 — Zheng, Hu, Zhang, Quinn, "Towards Agentic OS: An LLM Agent Framework for Linux Schedulers" (SchedCP, arXiv:2509.01245, v1–v4)

**Citation.** Yusheng Zheng, Yanpeng Hu, Wei Zhang, Andi Quinn. "Towards Agentic OS: An LLM Agent Framework for Linux Schedulers." arXiv:2509.01245; v1 submitted 1 Sep 2025, last revised 30 Sep 2025 (v4). (Author list as printed in the v1 running header; the abstract page title matches.)

**Copies read** (all accessed 2026-09-16, all under `sources/S1-03/`):
- `https://arxiv.org/abs/2509.01245` → `arxiv-2509.01245-abs.html`, SHA-256 `96a128b3ecd40eec9536bc5a1eb75a783c79034c62de7c416fba68601a3f51d6` (version list v1–v4; "Submitted on 1 Sep 2025 (v1), last revised 30 Sep 2025 (this version, v4)").
- `https://arxiv.org/pdf/2509.01245` (current = v4, 430 348 bytes) → `arxiv-2509.01245.pdf`, SHA-256 `cce49d3c0ff5466cafc3b921373f6d43df2adcb97e38b40c9d45e3b21206e97c`.
- `https://arxiv.org/pdf/2509.01245v1` (737 092 bytes) → `arxiv-2509.01245v1.pdf`, SHA-256 `b0fc4ec042d9cb9b2c6ec7eaecf66a7f9dbaca209fbc5f3c6cb5f311328f3a8b`.
- `https://arxiv.org/pdf/2509.01245v2` (737 845 bytes) → `arxiv-2509.01245v2.pdf`, SHA-256 `7dbfe839cbfa3937db68b4654b8dec82c6b6d1d20e25736848729ef7fe25c378`.
- `https://arxiv.org/pdf/2509.01245v3` (429 352 bytes) → `arxiv-2509.01245v3.pdf`, SHA-256 `e22190017e1b88bfa4c9b68fcdd7cde77bf36907577aa8306dae21cc28b35fe4`.

**Verbatim passages.**

v1, §5.2 "Example: Kernel Compilation" (p. 7 of the v1 PDF):
> "To illustrate how these four agents work together, consider a kernel compilation workload. The Observation Agent begins by analyzing the Linux kernel source tree, executing make -j to understand the build process, and running perf stat to profile resource usage. This observation produces a Workload Profile: “CPU-intensive parallel compilation task with short-lived processes, inter-process dependencies, and a goal to minimize makespan.”"

v1, §6.1 "Experimental Setup":
> "We evaluate SchedCP on two machines, machine 1 is an 86-core, 172 threads Intel Xeon 6787P with 758GB RAM, NVMe SSDs, 10Gbps network, with 2x 256 GB CXL (Compute Express Link) memory device, 3 numa node, running Linux 6.14 with sched_ext. Machine 2 is an 8-core, 8 threads Intel Core Ultra 7 258V with 30GB RAM, NVMe SSDs, 1 NUMA node, running Linux 6.13 with sched_ext. We test Claude Code (Opus 4) as AI agents to validate framework generality. For each case, we test 3 times and get the average results."

v1, §6.2:
> "The Linux kernel build benchmark compile the kernel 6.14 with tinyconfig and “make -j 172” on machine 1. Figure 2 shows performance improvements across three stages: baseline EEVDF, LLM-configured schedulers, and Iteration-improved configurations. […] The workload shows 1.63x speedup from 13.57s to 8.31s using scx_rusty as the first attemp. After 3 iteration of observe-optimization process, the sched-agent selects the scx_layered scheduler and adds 16% additional gain beyond LLM configuration, with total improvements of 1.79x over baseline EEVDF."

v4 (current), §5 "Preliminary Evaluation" (p. 4):
> "Evaluation uses two machines: 86-core Intel Xeon 6787P with 758GB RAM running Linux 6.14, and 8-core Intel Core Ultra 7 258V with 30GB RAM running Linux 6.13. Agents use Claude Code (Opus 4), testing each case three times and averaging results."

> "Scheduler Configuration: For kernel compilation (tinyconfig, “make -j 172” on 6.14 source), SchedCP achieves 1.63× speedup with scx_rusty initially, then iterative refinement selects scx_layered for 16% additional gain, reaching 1.79× total improvement over EEVDF (Figure 2a)."

v4, Figure 2a data labels as extracted from the embedded chart text (same string in v1–v3): "Average Build Time (seconds) … default Linux EEVDF … 13.57s 8.31s 7.60s 13.79s 1.63× 1.79× 0.98×".

Version differences (reader's own comparison by grep over the four extractions): v1 and v2 are the long form (§5.2 example, §6.1 setup with NVMe/CXL/NUMA detail); v3 and v4 are a condensed 4-page form. The workload description (kernel 6.14, tinyconfig, `make -j 172`, machine 1), the machines and the numbers 13.57 s / 8.31 s / 7.60 s / 1.63× / 1.79× are the same in all four versions. No version reports process counts, process lifetimes or CPU-time distributions for the build.

**Coverage.**
- T1 — does not cover (only the agent's own profile string "short-lived processes"; no data).
- T2, T3, T4, T5 — does not cover.
- T6 — covers: a scheduler evaluation using a kernel build; subject = Linux 6.14 source, `tinyconfig`, `make -j 172`; machine = 86-core/172-thread Intel Xeon 6787P, 758 GB RAM, Linux 6.14 with sched_ext; statistic = average build wall time over 3 runs (13.57 s EEVDF, 8.31 s scx_rusty, 7.60 s scx_layered, 13.79 s "basic RL scheduler"). Also an ML-for-systems paper using a kernel build as workload. No process data.
- T7 — marginal: the "8 diverse batch workloads (file compression, video transcoding, software testing, data analytics) with long-tail distributions (40 parallel tasks: 39 short, one long)" (v4 §5) are synthetic batch tasks with wall-clock times only; no thread count or utilisation is characterised. Recorded as does-not-cover for T7's characterisation question.
- **One observation**: yes — one machine, one subject (6.14 tinyconfig, `-j 172`), window = a 13.57 s build averaged over three runs.

### S1-04 — Jones, Arpaci-Dusseau, Arpaci-Dusseau, "Antfarm: Tracking Processes in a Virtual Machine Environment" (USENIX ATC '06)

**Citation.** Stephen T. Jones, Andrea C. Arpaci-Dusseau, Remzi H. Arpaci-Dusseau. "Antfarm: Tracking Processes in a Virtual Machine Environment." Proceedings of the 2006 USENIX Annual Technical Conference (Annual Tech '06), Boston, MA, 2006.

**Copy read.** `https://www.usenix.org/legacy/event/usenix06/tech/full_papers/jones/jones.pdf` (622 886 bytes), accessed 2026-09-16, saved as `sources/S1-04/usenix06-jones-antfarm.pdf`, SHA-256 `e9a16b94a26612fb31e5f78f608d3d349fe177a21cd344f8ee82da0175b0e533`.

**Verbatim passages.**

§6.1 x86 Evaluation (PDF p. 6):
> "Our evaluation on x86 uses Xen version 2.0.6. Version 2.6.11 of the Linux kernel was used in Xen's privileged control VM. Linux kernel version 2.4.30 and 2.6.11 are used in unprivileged VMs as noted. Our evaluation hardware consists of a 2.4 GHz Pentium IV PC with 512 MB of RAM. Virtual machines are each allocated 128 MB of RAM in this environment."

§6.1.1 Completeness (PDF p. 6):
> "The first workload is synthetic. It creates 1000 processes, each of which runs for 10 seconds then exits. The process creation rate is 10 processes/second."

> "The second workload is a parallel compile of the bash shell sources using the command “make -j 20” in a clean object directory. A compilation workload was chosen because it creates a large number of short-lived processes, stressing Antfarm's ability to track many concurrent processes that have varying runtimes."

Table 2 "Completeness" (PDF p. 7; columns: Process Create, Addr Spc Create, Inferred Create, Process Exit, Addr Spc Exit, Inferred Exit, Context Switch, CS Inferred; rows reconstructed from word positions with PyMuPDF and checked against a rendering of the page — the flow extraction emits this table column-major):
> "Linux 2.4 x86 … Compile 815 815 815 815 815 815 4447 4447"
> "Linux 2.6 x86 … Compile 748 1191 1191 748 1191 1191 2550 2550"
> "Windows … Compile 2602 2602 2602 2602 2602 2602 835248 835248"

Table 2 caption:
> "The table shows the total number of creations and exits for processes and address spaces reported by the operating system. The total number of process creations and exits inferred by Antfarm are shown in comparison."

§6.1.1, on fork/exec lifetimes in the compile (PDF p. 7):
> "In Linux 2.4, when exec is invoked the existing process address space is cleared and reused for the newly loaded program. In contrast, Linux 2.6 destroys and releases the address space of a process invoking exec. […] One segment corresponds to the period between fork and exec and the other corresponds to the period between exec and process exit."

> "The duration of the first pseudo-process will nearly always be small. For example, in the case of our compilation workload, the average time between fork and exec is less than 1 ms, compared to the average lifetime of the second pseudo-process, which is more than 2 seconds, a difference of three orders of magnitude."

> "During the compilation workload this interval averaged less than 0.1 ms and was never larger than 2.3 ms."

**Coverage.**
- T1 — covers: object = processes created by one clean `make -j 20` build of the bash shell sources; unit = count per build and mean lifetime; statistics = total process creations (815 on Linux 2.4.30, 748 on Linux 2.6.11, 2602 on Windows NT4 under Simics), OS-reported context switches during the build (4447 / 2550), mean fork→exec interval (< 1 ms) and mean exec→exit lifetime (> 2 s) on Linux 2.6; scope = one build per OS in a 128 MB Xen VM; population = all processes of that build. No breakdown by program, no distribution beyond the mean, no CPU time.
- T2, T3, T4, T5 — does not cover.
- T6 — covers the process-lifetime question only via the mean lifetime above (a build workload, not a general process population).
- T7 — does not cover.
- **One observation**: yes — machine named (2.4 GHz Pentium IV, 512 MB, Xen 2.0.6, 128 MB guests), subject named (bash shell sources, version unstated; `make -j 20`; clean object directory), window = one full build per guest OS (wall time not stated).

### S1-05 — Gouicem et al., "Fewer Cores, More Hertz: Leveraging High-Frequency Cores in the OS Scheduler for Improved Application Performance" (USENIX ATC '20)

**Citation.** Redha Gouicem, Damien Carver, Jean-Pierre Lozi, Julien Sopena, Baptiste Lepers, Willy Zwaenepoel, Nicolas Palix, Julia Lawall, Gilles Muller. "Fewer Cores, More Hertz: Leveraging High-Frequency Cores in the OS Scheduler for Improved Application Performance." Proceedings of the 2020 USENIX Annual Technical Conference (USENIX ATC '20), July 2020, pp. 435–448.

**Copy read.** `https://www.usenix.org/system/files/atc20-gouicem.pdf` (3 722 345 bytes), accessed 2026-09-16, saved as `sources/S1-05/atc20-gouicem.pdf`, SHA-256 `4e9e4a0f9a04717b4efefaaba10a5a4d58482e1d012722f97f7b6a05789ce447`.

**Verbatim passages.**

§1 Introduction (p. 435):
> "One source of challenges in managing core frequencies is the Frequency Transition Latency (FTL). Indeed, transitioning a core from a low to a high frequency, or conversely, has an FTL of dozens to hundreds of milliseconds. FTL leads to a problem of frequency inversion in scenarios that are typical of the use of the standard POSIX fork() and wait() system calls on process creation, or of synchronization between lightweight threads in a producer-consumer application."

§2 A Case Study: Building the Linux Kernel (p. 436):
> "We present a case study of the workload that led us to discover the frequency inversion phenomenon: building the Linux kernel version 5.4 with 320 jobs (-j) on a 4-socket Intel Xeon E7-8870 v4 machine with 80 cores (160 hardware threads), with a nominal frequency of 2.1 GHz. Thanks to the Intel SpeedStep and Turbo Boost technologies, our CPUs can individually vary the frequency of each core between 1.2 and 3.0 GHz."

> "In Figure 1, we notice different phases in the execution. For a short period around 2 seconds, for a longer period between 4.5 and 18 seconds, and for a short period around 28 seconds, the kernel build has highly parallel phases that use all of the cores at a high frequency. The second of these three phases corresponds to the bulk of the compilation. In these three phases, the CPUs seem to be exploited to their maximum. Furthermore, between 22 and 31 seconds, there is a long phase of mostly sequential code with very few active cores, of which there is always one running at a high frequency. In this phase, the bottleneck is the CPU's single-core performance. Between 0 and 4.5 seconds, and between 18 and 22 seconds however, there are phases during which all cores are used but they run at the CPU's lowest frequency (1.2 GHz). Upon closer inspection, these phases are actually mainly sequential: zooming in reveals that while all cores are used across the duration of the phase, only one or two cores are used at any given time."

§2 (p. 437):
> "It appears that in the considered phase of the execution, the FTL is much higher than the duration of the tasks. Since tasks that follow each other tend to be scheduled on different cores, they are likely to always run at a low frequency as most cores are idle most of the time in this phase of the execution."

> "It takes an FTL of 29 ms for the core to go from its minimum frequency of 1.25 GHz to its maximum frequency of 3.00 GHz in order to accommodate the task."

§3 (p. 438):
> "Computations in the (near) sequential phases of the build of Linux are launched sequentially as processes through the fork() and wait() system calls, and the execution of these computations is shorter than the FTL."

§5 Evaluation (p. 443):
> "As a result, for example, the phase before the long parallel phase is executed in 4.4 seconds on CFS and in only 2.9 seconds with Smove."

> "To understand the impact of Smove better, Figure 8 shows the kbuild-sched-320 benchmark, which builds only the scheduler subsystem of the Linux kernel. Here, the parallel phase is much shorter than with a complete build, as there are fewer files to compile, making the sequential phases of the execution more visible."

**Coverage.**
- T1 — covers only the structure: the kernel build's near-sequential phases consist of processes launched through `fork()`/`wait()` whose execution is shorter than the FTL (tens of ms); no process counts, no lifetime distribution.
- T2, T3, T4, T5 — does not cover.
- T6 — covers: a scheduler paper with a kernel build as the motivating workload; subject = Linux 5.4 source (configuration not named), `-j 320`; machine = 4-socket Intel Xeon E7-8870 v4, 80 cores / 160 hardware threads, 2.1 GHz nominal, 1.2–3.0 GHz; statistic = per-core frequency/activity trace over a ≈31 s build split into phases (parallel bulk 4.5–18 s; mostly-sequential 22–31 s; low-frequency near-sequential 0–4.5 s and 18–22 s). No process-count or CPU-time distribution.
- T7 — does not cover.
- **One observation**: yes — one machine, one subject (5.4, `-j 320`, config unnamed), window ≈ 31 s (the Figure 1 trace).

### S1-06 — Lozi et al., "The Linux Scheduler: a Decade of Wasted Cores" (EuroSys '16)

**Citation.** Jean-Pierre Lozi, Baptiste Lepers, Justin Funston, Fabien Gaud, Vivien Quéma, Alexandra Fedorova. "The Linux Scheduler: a Decade of Wasted Cores." Proceedings of the Eleventh European Conference on Computer Systems (EuroSys '16), London, April 2016. HAL id hal-01295194.

**Copy read.** `https://hal.science/hal-01295194/document` (517 942 bytes), accessed 2026-09-16, saved as `sources/S1-06/hal-01295194-lozi-eurosys16.pdf`, SHA-256 `a65a0d22c18fceaafca73d0b8ac390a7d695834bcf62ff959adc4d35774f0623`. (The author copy at `https://www.ece.ubc.ca/~sasha/papers/eurosys16-final29.pdf` returned a "Browser Verification | UBC Cybersecurity" challenge page, HTTP 200, not the PDF.)

**Verbatim passages.**

§3.1 The Group Imbalance bug:
> "We encountered this bug on a multi-user machine which we used to perform kernel compilation and data analysis using the R machine learning package. We suspected that this system, a 64-core, eight-node NUMA server, did not use all available cores for highly-threaded computations, instead crowding all threads on a few nodes."

> "In the time period shown in the figure, the machine was executing a compilation of the kernel (make with 64 threads), and running two R processes (each with one thread). The make and the two R processes were launched from 3 different ssh connections (i.e., 3 different ttys)."

> "Remember that a threads' load is a combination of its weight and how much CPU it needs. With autogroups, the thread's load is also divided by the number of threads in the parent autogroup. In our case, a thread in the 64-thread make process has a load roughly 64 times smaller than a thread in a single-threaded R process."

> "After we fixed the bug, the completion time of the make job, in the make/R workload described earlier in this section, decreased by 13%. The completion time of the two R processes did not change."

Table 5 "Hardware of our AMD Bulldozer machine":
> "8 × 8-core Opteron 6272 CPUs (64 threads in total) 2.1 GHz 768 KB L1 cache, 16 MB L2 cache, 12 MB L3 cache 512 GB of 1.6 Ghz DDR-3 HyperTransport 3.0 (see Figure 4)"

**Coverage.**
- T1, T2, T3, T4, T5 — does not cover.
- T6 — covers: a scheduler bug study whose motivating workload is a kernel compilation ("make with 64 threads", kernel version and configuration not named) alongside two single-threaded R processes on a 64-core, 8-node AMD Opteron 6272 machine (2.1 GHz, 512 GB); statistic = make completion time −13% after the fix. Also the only literature passage found on autogroup's effect on a parallel build: the per-thread load of the 64-thread make is divided by the autogroup's thread count. No process counts or lifetimes.
- T7 — does not cover.
- **One observation**: yes — machine named; subject only partly named (kernel version/config absent; `-j64` implied by "make with 64 threads"); window not stated.

### S1-07 — Boyd-Wickizer et al., "An Analysis of Linux Scalability to Many Cores" (OSDI '10)

**Citation.** Silas Boyd-Wickizer, Austin T. Clements, Yandong Mao, Aleksey Pesterev, M. Frans Kaashoek, Robert Morris, Nickolai Zeldovich. "An Analysis of Linux Scalability to Many Cores." Proceedings of the 9th USENIX Symposium on Operating Systems Design and Implementation (OSDI '10), Vancouver, October 2010.

**Copy read.** `https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Boyd-Wickizer.pdf` (222 262 bytes), accessed 2026-09-16, saved as `sources/S1-07/osdi10-boyd-wickizer.pdf`, SHA-256 `f5a618044994b7dc0824064b918fc5a6502bbd44509520eb4a87744fbd69f4cc`.

**Verbatim passages.**

§1 Introduction:
> "First we measure scalability of the MOSBENCH applications on a recent Linux kernel (2.6.35-rc5, released July 12, 2010) with 48 cores, using the in-memory tmpfs file system to avoid disk bottlenecks. gmake scales well, but the other applications scale poorly, performing much less work per core with 48 cores than with one core."

§3.5 Parallel build:
> "gmake is the unofficial default benchmark in the Linux community since all developers use it to build the Linux kernel. Indeed, many Linux patches include comments like “This speeds up compiling the kernel.” We benchmarked gmake by building the stock Linux 2.6.35-rc5 kernel with the default configuration for x86 64. gmake creates more processes than there are cores, and reads and writes many files. The execution time of gmake is dominated by the compiler it runs, but system time is not negligible: with one core, 7.6% of the execution time is system time."

§3.6 File indexer:
> "Phase 1 is both compute intensive (looking up words in the hash table and sorting it) and file-system intensive (reading input files and flushing the hash table)." […] "Unlike phase 1, phase 2 is mostly file-system intensive. While pedsort spends only 1.9% of its time in the kernel at one core, this grows to 23% at 48 cores, indicating scalability limitations."

§5 (hardware):
> "We run experiments on a 48-core machine, with a Tyan Thunder S4985 board and an M4985 quad CPU daughterboard. The machine has a total of eight 2.4 GHz 6-core AMD Opteron 8431 chips."

§5.6 gmake:
> "We measure the performance of parallel gmake by building the object files of Linux 2.6.35-rc5 for x86 64. All input source files reside in the buffer cache, and the output files are written to tmpfs. We set the maximum number of concurrent jobs of gmake to twice the number of cores. Figure 9 shows that gmake on 48 cores achieves excellent scalability, running 35 times faster on 48 cores than on one core for both the stock and PK kernels."

**Coverage.**
- T1 — covers only qualitatively ("gmake creates more processes than there are cores"); no counts.
- T2 — covers coarsely: the build's execution time "is dominated by the compiler it runs", with 7.6% system time at one core (warm buffer cache, tmpfs output); no per-process figures.
- T3 — does not cover.
- T4 — covers as a documented choice with rationale absent: `-j` = 2 × cores (96 on 48 cores; 2 on one core) in a research benchmark, not a desktop-user observation.
- T5 — does not cover.
- T6 — covers: kernel-scalability evaluation using a kernel build (Linux 2.6.35-rc5, x86_64 defconfig, object files only) on 48 × 2.4 GHz AMD Opteron 8431 cores, sources in buffer cache, tmpfs output, `-j` = 2 × cores; statistic = speedup 35× at 48 cores vs one core; plus a one-core run of the same build (the one-core point of Figure 9, absolute time not printed in the text). No process-level data.
- T7 — covers the file-indexer class: Psearchy/pedsort, a parallel indexer with one worker per core, phase 1 compute- and FS-intensive, phase 2 FS-intensive; kernel-time share 1.9% (one core) → 23% (48 cores). No sustained-utilisation or duration figures for a desktop indexer.
- **One observation**: yes for the gmake result — machine, subject (2.6.35-rc5 defconfig x86_64, `-j` 2 × cores) named; window not stated in the text.

### S1-08 — Traeger, Zadok, Joukov, Wright, "A Nine Year Study of File System and Storage Benchmarking" (ACM TOS 2008)

**Citation.** Avishay Traeger, Erez Zadok, Nikolai Joukov, Charles P. Wright. "A Nine Year Study of File System and Storage Benchmarking." ACM Transactions on Storage, Vol. 4, No. 2, Article 5, May 2008.

**Copy read.** `https://www.fsl.cs.sunysb.edu/docs/fsbench/fsbench.pdf` (559 001 bytes; the authors' lab copy of the TOS article, with the TOS running footer "ACM Transactions on Storage, Vol. 4, No. 2, Article 5, Publication date: May 2008"), accessed 2026-09-16, saved as `sources/S1-08/tos08-traeger-fsbench.pdf`, SHA-256 `79ec01a29579d5c9413b3a1865d71180721d4dd7c338e32807fc8ccb91de3fe8`.

**Verbatim passages.**

Abstract (p. 5:1):
> "As a specific example, slowing down read operations on ext2 by a factor of 32 resulted in only a 2–5% wall-clock slowdown in a popular compile benchmark."

§7.2 Compile Benchmarks (p. 5:17–5:18):
> "Of the papers we surveyed, 36 timed the compiling of some code to benchmark their projects." […] "Eight compiled an OS kernel [Zhang and Ghose 2003; Mazières et al. 1999; Tolia et al. 2004; Gulati et al. 2007; Radkov et al. 2004; Sivathanu et al. 2006; Papathanasiou and Scott 2004; Muniswamy-Reddy et al. 2006]."

> "The main problem with compile benchmarks is that because they are CPU intensive, they can hide the overheads in many file systems. This issue is discussed further in Section 12.2."

§7.2 (p. 5:19–5:20):
> "Using OSprof [Joukov et al. 2006], we profiled the build process of three packages commonly used as compile benchmarks: (1) SSH 2.1.0; (2) Am-utils 6.1b3; and (3) the Linux 2.4.20 kernel with the default configuration." […] "Not surprisingly, the kernel-build process profile differs from both SSH and Am-utils. As can be seen in Figure 4(c), both of the kernel-build phases are strongly read biased. In addition, the kernel-build process is more intensive in file-open and file-release operations."

§6 Benchmarking procedure (p. 5:14):
> "We configured Auto-pilot to run all tests at least ten times, and compute 95% confidence intervals for the mean elapsed, system, and user times using the student-t distribution." […] "In addition, we define “wait time” to be the time that the process was not using the CPU (mostly due to I/O)."

§12.2 Hiding Overheads (p. 5:44–5:45):
> "Because a compile benchmark is CPU intensive, such extraordinary overheads as a factor of 32 on read can go unnoticed (the factor of 32 comes from setting N to 5, as described in Section 12.1). For all of these graphs, the half-widths were less than 1.5% of the mean, and the CPU% was always more than 99.2%, where CPU% = timeuser + timesystem / timeelapsed × 100."

> "For the configure phase, the highest overhead was 2.7% for elapsed time, and 10.1% for system time (both for version 3.7). For the compile phase, the highest overhead was 4.5% for elapsed time and 59.2% for system time (both for version 3.5)."

> "These results clearly show that even with extraordinary delays in critical file system operations, compile benchmarks show only marginal overheads because they are bound by CPU time spent in user space."

**Coverage.**
- T1 — does not cover.
- T2 — covers, at whole-build granularity: object = configure+compile of OpenSSH 3.5/3.7/3.9 on ext2 and on a deliberately slowed ext2 (Slowfs); unit = elapsed / user / system time of the whole build; statistic = CPU% (user+system over elapsed) always > 99.2%, i.e. wait time < 0.8% of elapsed after a remount, with reads slowed 32× costing at most 4.5% elapsed; population = one machine, ≥ 10 runs, first discarded. Not per compiler process; not cold-cache (file systems were remounted before runs, compilers on the system disk). Also VFS-operation mixes of a Linux 2.4.20 defconfig build ("strongly read biased").
- T3, T4, T5 — does not cover.
- T6 — covers the "which builds are used as benchmarks" question for file-system papers 1999–2007: 36 of 106 surveyed papers timed a compile; 8 compiled an OS kernel.
- T7 — does not cover.
- **One observation**: the §12.2 experiment is one observation (one machine — its description is in §6 of the article, not quoted here; subject OpenSSH 3.5/3.7 configure+compile; ≥ 10 runs). The survey counts are a literature census, not a measurement.

### S1-09 — Harchol-Balter & Downey, "Exploiting Process Lifetime Distributions for Dynamic Load Balancing" (ACM TOCS 1997; earlier SIGMETRICS '96)

**Citation.** Mor Harchol-Balter, Allen B. Downey. "Exploiting Process Lifetime Distributions for Dynamic Load Balancing." ACM Transactions on Computer Systems 15(3):253–285, August 1997, DOI 10.1145/263326.263344 (Crossref record, log row 43). Earlier versions: Proc. ACM SIGMETRICS '96, Performance Evaluation Review 24(1):13–24, DOI 10.1145/233008.233019; SOSP '95 WIP abstract, DOI 10.1145/224056.225838. The copy read is the author's copy, whose text was not compared line-by-line with the ACM version (ACM DL is 403 to this session).

**Copy read.** `https://www.cs.cmu.edu/~harchol/Papers/TOCS.pdf` (499 150 bytes; author's copy, running head "Exploiting Process Lifetime Distributions for Dynamic Load Balancing"), accessed 2026-09-16, saved as `sources/S1-09/TOCS-harchol-balter-downey.pdf`, SHA-256 `e98e288bc0740896d7ecc78a7735723c3027e9b6e7a1630ef50caeffc58fbf9f`.

**Verbatim passages** (page numbers are the copy's own running numbers).

Abstract (p. 1):
> "Our measurements indicate that the distribution of lifetimes for UNIX process is Pareto (heavy-tailed), with a consistent functional form over a variety of workloads."

§1 (p. 3):
> "we use “age” to mean CPU age (the CPU time used by a process thus far) and “lifetime” to mean CPU lifetime (the total CPU time from start to"[…]

§2 Distribution of Lifetimes (p. 6):
> "That same year, Leland and Ott proposed a functional form for the process lifetime distribution, based on measurements of the lifetimes of 9.5 million UNIX processes between 1984 and 1985 [Leland and Ott 1986]. They conclude that process lifetimes have a UBNE (used-better-than-new-in-expectation) type of distribution. That is, the greater the current CPU age of a process, the greater its expected remaining CPU lifetime. Specifically, they find that for T > 3 seconds, the probability of a process's lifetime exceeding T seconds is rT^k, where −1.25 < k < −1.05 and r normalizes the distribution."

> "we performed an independent study of this distribution, and found that the functional form proposed by Leland and Ott fits the observed distributions well, for processes with lifetimes greater than 1 second. This functional form is consistent across a variety of machines and workloads, and although the parameter, k, varies from -1.3 to -.8, it is generally near -1. Thus, as a rule of thumb, —The probability that a process with age 1 second uses at least T seconds of total CPU time is about 1/T. —The probability that a process with age T seconds uses at least an additional T seconds of CPU time is about 1/2. Thus, the median remaining lifetime of a process is equal to its current age."

§2.1 (p. 6–7):
> "To determine the distribution of lifetimes for UNIX processes, we measured the lifetimes of over one million processes, generated from a variety of academic workloads, including instructional machines, research machines, and machines used for system administration. We obtained our data using the UNIX command lastcomm, which outputs the CPU time used by each completed process."

§2.1 (p. 8–9):
> "For all the machines we studied, the distribution of process lifetimes fits a curve of the form T^k, with k varying from −1.3 to −0.8 for different machines."

> "The functional form we are proposing (the fitted distribution) has the property that its moments (mean, variance, etc.) are infinite. Of course, since the observed distributions have finite sample size, they have finite mean (0.4 seconds) and coefficient of variation (5–7)."

§2.1.1 (p. 9):
> "For processes with lifetimes less than 1 second, we did not find a consistent functional form; however, for the machines we studied these processes had an even lower hazard rate than those of age > 1"[…]

(Typography note: the extraction renders "T^k" as "T" followed by "k" on the next line and the minus sign as "(cid:0)"; the passages above restore the printed superscript and minus, as read on the rendered page.)

**Coverage.**
- T1, T2, T3, T4, T5 — does not cover.
- T6 — covers the general process-lifetime-distribution question: object = CPU lifetime (total CPU time at exit, from `lastcomm` / BSD process accounting) of UNIX processes; unit = seconds of CPU; statistic = survival function P{Lifetime > T} ∝ T^k with k ∈ [−1.3, −0.8] for lifetimes > 1 s, sample mean 0.4 s, CV 5–7; scope = over one million processes on academic instructional/research/sysadmin UNIX workstations (mid-1990s; machine names in Table 1 of the copy, e.g. "po"); population = all completed processes, not build processes. Also relays Leland & Ott 1986 (9.5 million processes, 1984–85, k ∈ (−1.25, −1.05) for T > 3 s), whose primary copy this reader could not obtain (ACM DL 403).
- T7 — does not cover.
- **One observation**: no — several machines and workloads pooled; each machine's fit is one observation (Table 1). No build subject; the window is a semester-scale collection period ("mid-semester" in Fig. 1's caption).

### S1-10 — Kubota & Kono, "Native Build System for Unity Builds with Sophisticated Bundle Strategies" (IEICE Trans. Inf. & Syst. 2021)

**Citation.** Takafumi Kubota, Kenji Kono. "Native Build System for Unity Builds with Sophisticated Bundle Strategies." IEICE Transactions on Information and Systems, Vol. E104-D, No. 1, January 2021, pp. 126–137 (first page 126 as printed). DOI 10.1587/transinf.2020EDP7105.

**Copy read.** `https://www.jstage.jst.go.jp/article/transinf/E104.D/1/E104.D_2020EDP7105/_pdf` (1 428 955 bytes), accessed 2026-09-16, saved as `sources/S1-10/kubota-ieice-2021-unity-builds.pdf`, SHA-256 `adca255f01dce372fa846bbfbdf0772f16c92558ebcf730cb0adf771b8e887f3`.

**Verbatim passages.**

§2.3 (p. 128):
> "To confirm that the problem is not limited to WebKit, we analyzed the logs of build bots of LLVM [25], [39], which is an open-source compiler framework written in C++, from March 9 to August 1 in 2018. The number of build tasks submitted during the period was 1,146. Build tasks consuming more than 15 minutes happened 227 times on 74 out of 81 days when the build bot was active."

§2.4 (p. 128), Fig. 3 caption:
> "Fig. 3 How much time does the compiler spend parsing? Here, the x-axis shows source-file indexes for each project. The y-axis shows parse ratios for each source file. The parse ratio indicates the occupancy of parsing time during the compile time. The times are measured by using the timer report functionality of GCC (-ftime-report). The x-axis is sorted in ascending order of the parse ratio."

§2.4 (p. 128):
> "In large C++ projects, much of the compilation time is spent parsing. For example, Fig. 3 a and Fig. 3 b show the distribution of times in which the compiler performs parsing. According to these figures, parsing occupies a majority of the compilation time (60%>) in many source files (56% in LLVM and 80% in WebKit). This high ratio stems from shared header files that are included in multiple source files. The compiler repeatedly reads the shared headers, parses them, and instantiates the same template bodies across different source files."

§4 (p. 131):
> "For example, when we bundle source A whose compile time is one second with source B whose compile time is 10 seconds, the build time of unity builds cannot be under 10 seconds because the compile time of source B becomes a bottleneck."

> "Thus, we decided to use the word count of ‘;’ to estimate compile times. Figure 4 shows the relationship between the number of ‘;’s and the compile times in LLVM and WebKit. We performed polynomial regression on these data and calculated an approximate expression that our build system uses to estimate the compile times."

§5 Evaluation setup (p. 133):
> "We perform the evaluation on our DELL Power Edge R430 server that has a Fedora 29 server installed. The server consists of 8-core 2.1 GHz Xeon E5-2620V4 processor, 128 GB of RAM, and a 1TB SATA HDD disk. All source files are resident in the disk."

> "We choose three real C/C++ projects for evaluating our build system, including LLVM (git-commit-id: ca1e713fdd4), WebKit (git-commit-id: ec4eb02a9e2), and Mesa 3D library (v18.3.6) [26]. In the evaluations, we use GCC v8.3.1 and LLVM/Clang v9.0.0 as compilers but only show the results of the GCC, because the results of the Clang are similar to those of the GCC. The linker is GNU ld v2.31.1."

**Coverage.**
- T1 — does not cover.
- T2 — covers, partially: object = per-source-file compile time of every translation unit of LLVM and WebKit (GCC 8.3.1, `-ftime-report`); statistics reported = the parse-time share per file (Fig. 3; "56% in LLVM and 80% in WebKit" of files have parsing above 60% of compile time) and the per-file compile time against the file's ‘;’ count (Fig. 4, scatter); the paper gives no histogram, percentiles, mean or median of compile time itself in its text — the per-file distribution is visible only as the Fig. 4 scatter. Reader's own reading of the rendered Fig. 4 (p. 131, "Compile time estimation", y-axis "Compile times (sec)", x-axis "Num of semicolon"): y-axis ticks run 0–200 s with the great majority of LLVM and WebKit points below 50 s and a handful of outliers between 100 and about 230 s; Fig. 3's x-axes ("Source file index") run to about 1 500 files for LLVM and about 7 500 for WebKit. These are readings of a plot, not values. No blocking/I-O split, no cold-cache case.
- T3 — does not cover (the build system is the paper's own; no make/ninja dispatch mechanics).
- T4, T5, T6, T7 — does not cover.
- **One observation**: yes — machine named (Dell PowerEdge R430, 8-core 2.1 GHz Xeon E5-2620 v4, 128 GB, SATA HDD, Fedora 29), subjects named (LLVM ca1e713fdd4, WebKit ec4eb02a9e2, Mesa 18.3.6; GCC 8.3.1), `-j` not stated in the text read; window = one full build per project for the Fig. 3/4 data (not stated explicitly).

### S1-12 — Miller, "Recursive Make Considered Harmful" (AUUGN 1998)

**Citation.** Peter Miller. "Recursive Make Considered Harmful." AUUGN, Journal of AUUG Inc., 19(1):14–25, 1998 (self-citation printed in the copy; copyright line "Copyright © 1997 Peter Miller"; presented at AUUGN '97).

**Copy read.** `https://aegis.sourceforge.net/auug97.pdf` (77 877 bytes), accessed 2026-09-16, saved as `sources/S1-12/miller-1998-recursive-make.pdf`, SHA-256 `bbffbbbd5763b7cf08cc30ebfd61805f0fe1784e8bc4335fb79027b20d5019b4`.

**Verbatim passages.**

§3.3.1 (Reshuffle):
> "Note that “make -j” (parallel build) invalidates many of the ordering assumptions implicit in the reshuffle solution, making it useless. And then there are all of the sub-makes all doing their builds in parallel, too."

§3.3.2 (Overkill):
> "Note that “make -j” (parallel build) invalidates many of the ordering assumptions implicit in the overkill solution, making it useless, because all of the sub-makes are all doing their builds ("clean" then "all") in parallel, constantly interfering with each other in non-deterministic ways."

§7.1 Side Effects:
> "The GNU Make -j option, for parallel builds, works even better than before. It can find even more unrelated things to do at once, and no longer has some subtle problems."

**Coverage.**
- T3 — covers only the recursive-make aspect qualitatively: with recursive make each sub-make parallelises independently under `-j`; a single whole-project Makefile exposes more concurrent work to `make -j`. Nothing on the jobserver (which post-dates the article), make's own CPU cost, or the live-process count under `-jN`.
- T1, T2, T4, T5, T6, T7 — does not cover.
- **One observation**: no measurement; an argument paper.

### S1-13 — Mokhov, Mitchell, Peyton Jones, "Build Systems à la Carte" (ICFP 2018)

**Citation.** Andrey Mokhov, Neil Mitchell, Simon Peyton Jones. "Build Systems à la Carte." Proc. ACM Program. Lang. 2, ICFP, Article 79 (September 2018), 29 pages. DOI 10.1145/3236774.

**Copy read.** `https://www.microsoft.com/en-us/research/uploads/prod/2018/03/build-systems.pdf` (redirects to `…/wp-content/uploads/2018/03/build-systems.pdf`; 728 559 bytes), accessed 2026-09-16, saved as `sources/S1-13/mokhov-2018-build-systems-a-la-carte.pdf`, SHA-256 `d6c175a48cc908ca3f185e1fb4620e3278c5655218ac687d83dfa7f405624ede`.

**Verbatim passages.**

§6.2 Parallelism:
> "We have given simple implementations assuming a single thread of execution, but all the build systems we address can actually build independent keys in parallel. While it complicates the model, the complications can be restricted exclusively to the scheduler: (1) The topological scheduler can build the full dependency graph, and whenever all dependencies of a task are complete, the task itself can be started."

> "The actual implementation of the parallel schedulers is not overly onerous, but neither is it beautiful or informative."

**Coverage.**
- T3 — covers only the abstract dispatch rule of a Make-style ("topological") scheduler: a task starts when all its dependencies are complete. Nothing on the jobserver, the shell between make and the compiler, make's CPU cost, the number of live processes under `-jN`, or behaviour at the cap; ninja and cargo are not analysed for parallelism.
- T1, T2, T4, T5, T6, T7 — does not cover.
- **One observation**: no measurement; a model paper.

### S1-11 — Uluski, Moffie, Kaeli, "Characterizing Antivirus Workload Execution" (ACM SIGARCH CAN 2005)

**Citation.** Derek Uluski, Micha Moffie, David Kaeli. "Characterizing Antivirus Workload Execution." ACM SIGARCH Computer Architecture News 33(1):90–98, March 2005, DOI 10.1145/1055626.1055639 (Crossref record, log row 17; the copy read carries no venue header, so the journal data are Crossref's, not the copy's).

**Copy read.** `http://www.ece.neu.edu/groups/nucar/publications/uluski.pdf` (redirects to `https://ece.northeastern.edu/groups/nucar/publications/uluski.pdf`; 96 512 bytes; authors' lab copy), accessed 2026-09-16, saved as `sources/S1-11/uluski-2005-antivirus.pdf`, SHA-256 `d8af814d621474a40892d962535f45b0d13dbf166154528166f1fb5951eea827`. (ResearchGate copy: 403.)

**Verbatim passages.**

Abstract:
> "Using the Virtutech Simics toolset, we profile the behavior of four popular anti-virus packages as run on an Intel PentiumIV platform running Microsoft Windows-XP. In our study, we focus on the overhead introduced by the anti-virus software during on-access execution. The overhead associated with anti-virus execution can dominate overall performance. The AV-Test group has already reported that this overhead can range from 23-129% on live systems running on-access experiments [3]."

§2:
> "Figure 1 plots the increase in execution time due to anti-virus overhead. We study three different test scenarios: 1) copying a small executable from the CDROM to the hard disk, 2) executing calc.exe, and 3) executing wordpad.exe. All of this execution is running under Windows XP professional. The value shown in each bar is the percent increase in execution time relative to a base case (the base case is the same scenario run without any anti-virus software present)."

§4:
> "The Simics model we are using is known as the Dredd model, a 2GHz Intel PentiumIV with 256MB of memory."

Table 2 (configurations), as extracted:
> "Norton Anti-Virus Professional 2004 … Trend Micro Internet Security … McAfee Virus Scan Professional … F-Prot Anti-virus for Windows"

§5.1:
> "We see a consistent increase in the cache activity for each of the anti-virus workloads. This overhead is smallest for F-Prot, which performs the least amount of scanning. Norton introduces the most overhead."

**Coverage.**
- T7 — covers only the on-access (real-time) antivirus case, not a full on-demand scan: object = execution-time increase and instruction/cache-access counts of three short Windows XP scenarios (a file copy, launching calc.exe, launching wordpad.exe) with four AV packages, in a cycle-accurate Simics model of a 2 GHz Pentium 4 with 256 MB; no thread count, no sustained CPU utilisation, no scan duration; the 23–129% range is relayed from AV-Test, not measured. Not Linux, not a desktop batch rescan.
- T1, T2, T3, T4, T5, T6 — does not cover.
- **One observation**: yes — simulated machine named, subjects named (four AV products, versions in Table 2), windows = three short scenarios (durations not stated in the text read).

## 3. Not found

Topics or sub-questions with no literature candidate, and the searches that established it (row numbers refer to the search log):

- **T1, per-process lifetime or CPU-time distributions of a parallel build, and per-program counts (cc1 / as / ld / collect2 / sh / fixdep / genksyms / modpost).** Nothing in the literature class gives a distribution or a per-program breakdown. The closest are totals: 2430 processes for a DynamoRio `make -j8` (S1-01), 815/748 processes for a bash `make -j 20` with mean fork→exec < 1 ms and mean exec→exit > 2 s (S1-04), and the qualitative "enormous number of short-lived processes like cp and mkdir" for the kernel build (S1-02). Established by rows 27 (WebSearch, process-lifetime trace papers), 22 (arXiv API — rate-limited, so arXiv full-text was searched only through WebSearch), 14/15/21 (OpenAlex, Semantic Scholar and dblp unusable this session).
- **T2, per-compiler-process I/O blocking (warm vs cold cache) and run/wait/run structure.** No paper measures blocking time inside a compiler process. Whole-build CPU% > 99.2% on a warm ext2 (S1-08) and the per-file compile-time scatter and parse share (S1-10) are the nearest. Established by rows 34 and 40.
- **T3, GNU make's jobserver, make's own CPU cost per job, the live-process count under `-jN`, behaviour at the cap; ninja and cargo.** Only argument/model papers (S1-12, S1-13) and no measurement; Belinassi et al. 2022 (SBAC-PADW, which discusses GCC-internal parallelism against `make -j`) could not be read: IEEE Xplore 202/challenge, ResearchGate request-only, no author copy (rows 18, 23, 24, 33). This is documentation and source-code territory (S2).
- **T4, `-j` levels developers and distributions use, with rationale, and observations of user choices.** No literature; the only `-j` choices found are the papers' own (S1-01 `-j8` on 8 threads; S1-03 `-j 172` on 172 threads; S1-05 `-j 320` on 160 threads; S1-07 2 × cores; S1-06 64 on 64). Established by row 35 (forums, kcbench man page, LKML only — S2/S3 classes).
- **T5, DKMS autoinstall process behaviour, triggers, duration.** No literature at all. Established by row 38.
- **T6, autogroup / `sched_child_runs_first` documentation or evaluation in the literature.** Only S1-06's one sentence on autogroup's load division; the feature's own documentation (man `sched(7)`, LKML RFC, `kernel/sched/autogroup.c`) is S2's class (row 28). No paper evaluating a build confined by cgroup `cpu.max` or container `--cpus`; the single-core `taskset` run in S1-01 is the only confined-build observation (row 41). No energy/DVFS paper running `make -jN` across core counts was found (row 37).
- **T7, desktop batch-job characterisation: full antivirus rescan, video encoder threading with sustained utilisation, CPU-side model training on desktop CPUs, file-indexer full rescan duration; ananicy / distribution scheduling-class catalogues.** Only partial: on-access AV overhead in a simulator (S1-11), and a parallel indexer's kernel-time share (S1-07 Psearchy). x264 characterisations surfaced only as request-only ResearchGate entries or non-x264 encoders (row 36); no search was spent on model-training utilisation or ananicy rule sets, which are source-code catalogues (S2's class), so those remain unsearched in this class.
- **Primary copy of Leland & Ott 1986** (SIGMETRICS '86, DOI 10.1145/317499.317539): ACM DL 403, no open copy found (rows 16, 23, 26). Its lifetime-distribution finding is quoted second-hand from S1-09.

Searches logged: 43 rows (several rows group one engine's batch of queries; counted as rows). Candidates recorded: 13 (S1-01 … S1-13), of which S1-02, S1-12 and S1-13 carry no measurement.
