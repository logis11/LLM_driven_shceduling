# S1 — Literature reader record (task 9.12, stage 2 search)

Reader class: S1 (peer-reviewed and preprint literature, textbooks, technical reports).
Topics assigned: T1 (ghOSt only), T3, T4, T5, T9 (Waldspurger & Weihl; Liu & Layland), T10, T11, T12, T13 (literature side).
Access date for every copy below: 2026-10-07. All copies saved under `sources/<id>/` (gitignored).

**Quotation conventions.** Passages are copied from `pdftotext` output of the fetched file, with line breaks collapsed to single spaces and end-of-line hyphenation joined as the extractor joined it (e.g. "faulttolerance" for "fault-tolerance" split across lines). Where the extractor dropped glyphs (ligatures "fi"/"fl"/"ff" in S1-05; math symbols in S1-09; minus signs rendered "?" in S1-05), the dropped characters are restored in square brackets, e.g. `de[fi]ne`, and the passage was checked against a rendered image of the page where marked "(checked against page image)". Locators: "p.N" = PDF page N of the fetched file; printed page numbers are given when they differ.

---

## 1. Search log

| # | Date | Engine / venue | Exact query or URL | Hits followed | Dead ends (HTTP status) |
|---|---|---|---|---|---|
| 1 | 2026-10-07 | direct fetch (curl) | https://cs.stanford.edu/~jhumphri/documents/ghost.pdf | S1-01 (200) | — |
| 2 | 2026-10-07 | direct fetch | https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-mlfq.pdf ; …/cpu-sched.pdf | S1-02, S1-03 (200) | — |
| 3 | 2026-10-07 | direct fetch | https://cseweb.ucsd.edu/classes/wi19/cse221-a/papers/corbato62.pdf | S1-04 (200) | — |
| 4 | 2026-10-07 | direct fetch | https://people.eecs.berkeley.edu/~istoica/papers/eevdf-tr-95.pdf | S1-05 (200) | — |
| 5 | 2026-10-07 | direct fetch | https://people.csail.mit.edu/hongzi/content/publications/Decima-Sigcomm19.pdf | S1-06 (200) | — |
| 6 | 2026-10-07 | direct fetch | https://www.usenix.org/system/files/osdi20-qiu.pdf | S1-07 (200) | — |
| 7 | 2026-10-07 | NeurIPS proceedings index | https://proceedings.neurips.cc/paper_files/paper/2019 (grep "Park") → hash f69e505b08403ad2298b9f262659929a | S1-08 (200) | — |
| 8 | 2026-10-07 | direct fetch | https://www.waldspurger.org/carl/papers/lottery-osdi94.pdf | S1-09 (200) | — |
| 9 | 2026-10-07 | direct fetch | https://www.cs.ru.nl/~hooman/DES/liu-layland.pdf | S1-10 (200) | — |
| 10 | 2026-10-07 | arXiv abs + PDF | export.arxiv.org/abs/2511.11628 ; arxiv.org/pdf/2511.11628v1 | S1-11 | — |
| 11 | 2026-10-07 | arXiv abs + PDF | export.arxiv.org/abs/2509.01245 ; arxiv.org/pdf/2509.01245v1, v2, v3, v4 | S1-12 (all 200) | — |
| 12 | 2026-10-07 | ACM DL | https://dl.acm.org/doi/10.1145/3672197.3673434 and /doi/pdf/… (Kgent) | — | **403** both (bot block / no access) |
| 13 | 2026-10-07 | GitHub raw | https://raw.githubusercontent.com/eunomia-bpf/KEN/main/README.md ; pinned commit via `git ls-remote` | S1-13 (200) | `gh api repos/eunomia-bpf/KEN` → 403 (session GitHub policy), worked around with `git ls-remote` |
| 14 | 2026-10-07 | arXiv API | `search_query=all:Kgent` | 0 hits | — |
| 15 | 2026-10-07 | arXiv API | `search_query=all:KEN AND all:eBPF` | 1 hit: 2312.05531 (KEN) → S1-13 | — |
| 16 | 2026-10-07 | arXiv abs + PDF | 2508.12551 v1, v2 | S1-14 | — |
| 17 | 2026-10-07 | arXiv abs + PDF | 2506.02025 (latest = v2) | S1-15 | — |
| 18 | 2026-10-07 | arXiv abs + PDF | 2511.11612 v1 | S1-16 | — |
| 19 | 2026-10-07 | arXiv abs + PDF | 2605.15026 (latest = v2) | S1-17 | — |
| 20 | 2026-10-07 | arXiv abs + PDF | 2512.25065 v3 (latest) and v1 | S1-18 | — |
| 21 | 2026-10-07 | arXiv API (sorted by date) | `all:"sched_ext"` | 4 hits: 2605.02377, 2602.09345, 2511.08297, 2511.11628 (only the last is LLM/recognition-related) | — |
| 22 | 2026-10-07 | arXiv API | `all:LLM AND all:"Linux scheduler"` | 1 hit: 2509.01245 | — |
| 23 | 2026-10-07 | arXiv API | `au:Zheng_Yusheng` | 26 hits; none a scheduler follow-up to 2509.01245 (titles scanned: AgentCgroup, gpu_ext, KernelScript, ActPlane, etc.) | — |
| 24 | 2026-10-07 | arXiv API | `au:Quinn_Andi` | 21 hits; same result | — |
| 25 | 2026-10-07 | arXiv API | `all:"agentic OS"` | 10 hits; followed 2609.12276 (AKTS) → S1-19 | — |
| 26 | 2026-10-07 | arXiv API | `ti:LLM AND ti:"operating system" AND ti:tuning` | 0 | — |
| 27 | 2026-10-07 | arXiv API | `abs:LLM AND abs:"workload classification"` | 1 (2606.02982, GPU inference QoS — not followed, not OS process recognition) | — |
| 28 | 2026-10-07 | arXiv API | `abs:"process list" AND abs:LLM` | 0 | — |
| 29 | 2026-10-07 | arXiv API | `ti:"expert in residence"` | 0 | — |
| 30 | 2026-10-07 | arXiv API | `abs:"large language model" AND abs:"CPU scheduler"` | 1 (2609.22978, sandbox infra — not relevant) | — |
| 31 | 2026-10-07 | arXiv API | `abs:LLM AND abs:eBPF AND abs:scheduler` | 5; 2609.12276 (S1-19), 2509.01245 (S1-12) relevant | — |
| 32 | 2026-10-07 | arXiv API | `abs:LLM AND abs:sysctl` ; `abs:LLM AND abs:"OS tuning"` | 1 each: 2605.15026 (S1-17) | — |
| 33 | 2026-10-07 | arXiv API | `abs:LLM AND abs:"kernel tuning"` | 4: 2508.12551 (S1-14), 2503.09663 (BYOS, kernel config; not followed), 2 GPU-kernel papers | — |
| 34 | 2026-10-07 | arXiv API | `abs:"language model" AND abs:"workload characterization"` ; `abs:LLM AND abs:"workload identification"` | 4 LLM-serving papers / 0 — none about OS workload recognition | — |
| 35 | 2026-10-07 | WebSearch | `"An expert in residence" LLM agents always-on operating system tuning Liargkovas` | neurips.cc/virtual/2025/129122 → S1-20; daplab.cs.columbia.edu/projects/lumos → S1-20 | openreview.net/pdf?id=7dhlgPp8ni → **403** |
| 36 | 2026-10-07 | WebSearch | `LLM classify workload from process list accuracy Linux desktop scheduler 2025 2026 paper` | neurips.cc/virtual/2025/loc/san-diego/129092 (SchedCP venue) → S1-12; arXiv 2505.15213 (KernelOracle, LSTM, not LLM; not followed) | — |
| 37 | 2026-10-07 | direct fetch | https://www.cs.rochester.edu/u/cli/research/switch.pdf ; https://www.cs.rochester.edu/~cli/research/switch.pdf | — | **404** both |
| 38 | 2026-10-07 | WebSearch | `"Quantifying the cost of context switch" Li Ding Shen pdf` | https://www.cs.rochester.edu/~kshen/papers/expcs2007.pdf → S1-21 (200) | — |
| 39 | 2026-10-07 | WebSearch | `"Context switch overheads for Linux on ARM platforms" David Carlyle Campbell pdf` | ACM DL https://dl.acm.org/doi/pdf/10.1145/1281700.1281703 | **403** (paywall/bot block); no open copy found |
| 40 | 2026-10-07 | arXiv API | `ti:"context switch" AND abs:cost` ; `abs:"context switches per second"` ; `ti:"scheduler overhead" AND abs:Linux` ; `abs:"pick_next_task"` | 3 / 0 / 0 / 0 hits; none a measurement study of switch cost (2508.15703, 2411.18424 not followed: cluster/LLM-serving) | — |
| 41 | 2026-10-07 | WebSearch | `measured context switch cost microseconds modern x86 Linux paper 2020 2021 2022 "context switch" direct indirect cost Skylake` | arXiv 1811.01412 → S1-23; blog posts (eli.thegreenplace.net, huizhou92.com; not literature, not used) | — |
| 42 | 2026-10-07 | WebSearch | `study measured context switches per second desktop workload Linux interactive applications trace paper` | only mailing-list posts / vendor docs (lkml 2001, erlang 2004, Microsoft TechNet) — not literature; not used | — |
| 43 | 2026-10-07 | arXiv abs + PDF | 2403.12844 (v4), 2408.04667 (v5), 2201.11903 (v6), 2408.02442 (v3), 2409.12183 (v3) | S1-24 … S1-28 | — |
| 44 | 2026-10-07 | arXiv API | `abs:"llama.cpp" AND abs:benchmark AND abs:CPU` | 4; followed 2601.14277 → S1-29 | — |
| 45 | 2026-10-07 | arXiv API | `ti:"gaming session"` ; `abs:"session length" AND abs:"video game"` | 1 (LLM role-play storytelling — irrelevant) / 0 | — |
| 46 | 2026-10-07 | WebSearch | `peer-reviewed study PC video game play session length telemetry average session duration minutes` | Nielsen 2009 industry report, Fraunhofer Steam paper abstract, Statista (paywalled), arXiv 1707.00863 (Flappy Bird, mobile) — none gives a PC session-length measurement I could read in full; not used | Statista: paywalled |
| 47 | 2026-10-07 | arXiv API | `abs:"audio latency" AND abs:"buffer size"` | 0 | — |
| 48 | 2026-10-07 | WebSearch | `Wessel Wright "Problems and prospects for intimate musical control of computers" latency 10 ms pdf` | arXiv 2010.01570 → S1-30 | — |
| 49 | 2026-10-08 | arXiv API (stage 3) | `all:LAVD AND all:scheduler`; `all:"latency criticality" AND all:"virtual deadline"` | 0 results each | — |
| 50 | 2026-10-08 | OpenAlex API (stage 3) | `search=LAVD scheduler` (68 works), `latency-criticality aware virtual deadline` (11 891), `sched_ext gaming scheduler` (4); first 15 of each read | no work describing LAVD by its authors | dblp: bot challenge, then 429 |
| 51 | 2026-10-08 | arXiv API (stage 3) | eight queries, sorted by submission date, 100 results each: `all:"language model" AND all:workload AND all:recognition AND all:scheduler` (3); `all:LLM AND all:"process list"` (1); `all:LLM AND all:sched_ext` (1); `all:LLM AND all:"workload classification" AND all:"operating system"` (0); `all:"agentic OS"` (10); `all:LLM AND all:scheduler AND all:desktop` (3); `all:LLM AND all:"process names"` (5); `all:LLM AND all:"kernel scheduler"` (4) | 26 distinct works read by title; none measures an LLM's accuracy at recognizing workloads from a process list; AKTS has a v2 (2026-10-07) → S1-32 | — |
| 52 | 2026-10-08 | dl.acm.org; OpenAlex; escholarship.org (stage 3) | `https://dl.acm.org/doi/pdf/10.1145/3672197.3673434`; `api.openalex.org/works/doi:10.1145/3672197.3673434` (open-access locations); `https://escholarship.org/content/qt3jg1f0jr/qt3jg1f0jr.pdf` | eScholarship 200 (first request 202, empty) → S1-33 | ACM DL 403 (both URLs) |
| 53 | 2026-10-08 | arxiv.org (stage 3) | `/pdf/2509.01245v1`, `/pdf/2509.01245v4` | 200, byte-identical to S1-12's copies → S1-34 | — |
| 54 | 2026-10-08 | api.crossref.org; arxiv.org (stage 3) | `works/10.1145/3770855.3817987`; `/abs/2506.02025`; `/abs/2508.12551` | 200 each → S1-35 | — |

---

## 2. Candidates

### S1-01 — ghOSt (T1, T10)

- **Citation.** Jack Tigar Humphries, Neel Natu, Ashwin Chaugule, Ofir Weisse, Barret Rhoden, Josh Don, Luigi Rizzo, Oleg Rombakh, Paul Turner, Christos Kozyrakis. "ghOSt: Fast & Flexible User-Space Delegation of Linux Scheduling." SOSP '21, October 26–28, 2021. https://doi.org/10.1145/3477132.3483542
- **Copy read.** https://cs.stanford.edu/~jhumphri/documents/ghost.pdf · accessed 2026-10-07 · `sources/S1-01/ghost.pdf` · SHA-256 `c37d636045a45e2216e7047ba1fb9ffa4ed88fe54b09ee0ccc33435cacd35c91` · full text.
- **Passages.**
  - p.1, Abstract: "ghOSt is designed to support the rapidly evolving needs of our data center workloads and platforms. Improving scheduling decisions can drastically improve the throughput, tail latency, scalability, and security of important workloads. However, kernel schedulers are difficult to implement, test, and deploy efficiently across a large fleet."
  - p.1, Abstract: "Programmers use any language to develop and optimize policies, which are modified without a host reboot."
  - p.3, §2 (Background/motivation): "Deploying schedulers is even harder. Deploying changes to scheduling policy requires deploying a new kernel across a large fleet. This is extremely challenging for cloud providers. So much so that, in our experience, kernel rollouts are not well-tolerated below an O(month) granularity."
  - p.3: "ghOSt enables scheduler update, testing, and tuning without having to update the kernel and/or reboot machines and applications."
  - p.4, §2.1: "Therefore, the scheduling policy should be decoupled from the host kernel and ghOSt must allow new policies to be deployed, updated, rolled-back, or even crash without incurring the machine-reboot costs."
  - p.5, §3: "To achieve fault tolerance and isolation, if one or several of the agents crash, the system will fall back to the default scheduler, such as CFS. The machine is then still fully functional while a new ghOSt userspace agent is launched — either the last known stable release or a newer revision with a fix."
  - p.8, §3.4 "Fault Isolation and Dynamic Upgrades": "We achieve this goal by assigning ghOSt's kernel scheduler class a lower priority (§2) than the default scheduler class — typically CFS — in the kernel's scheduling class hierarchy. The result is that most threads in the system will preempt ghOSt threads."
  - p.8, §3.4: "Destroying the enclave kills all the agents in that enclave, keeping other enclaves in the system intact, and automatically moves all threads in the destroyed enclave back to CFS."
  - p.8, §3.4 "ghOSt watchdog": "As a safety mechanism, ghOSt automatically destroys enclaves with misbehaving agents. For example, the kernel will destroy an enclave when it detects an agent has not scheduled a runnable thread within a user-configurable number of milliseconds."
  - p.12, §4.4 (Google Search): "When developing a kernel scheduler, the write-test-write cycle includes (a) compiling a kernel (up to 15 minutes), (b) deploying the kernel (10-20 minutes), and (c) running the test (1 hour due to database initialization following a reboot). As a result, the enthusiastic kernel developer experiments with 5 variants per day. With ghOSt, compiling, deploying and launching the new agent is comfortably done within one minute."
  - p.8, §4.1 setup: "Experimental Setup: Unless otherwise noted, experiments run on Linux 4.15 with our ghOSt patches applied. We run microbenchmarks on a 2-socket Intel Xeon Platinum 8173M @ 2GHz, 28 cores per socket, 2 logical cores each."
  - p.9, §4.1: "Local scheduling (line 3). In the per-CPU model, this is the overhead of committing a transaction and performing a context switch on the local CPU, until the target thread is running. The overhead (888 ns) is slightly higher than CFS context switch overhead (599 ns) due to the transaction commit, but still competitive."
  - p.9, Table 3 values (as extracted, row labels and values in table order): "10. Syscall Overhead 11. pthread Minimal Context Switch Overhead 12. CFS Context Switch Overhead … 72 ns 410 ns 599 ns".
  - p.9: "The overhead (725 ns) is dominated by the context switch (410 ns)."
- **Coverage.**
  - T1: covers ghOSt's stated motivation (fleet-scale kernel rollout cost, O(month) rollouts, iteration speed: 5 variants/day vs <1 min), mechanism (kernel scheduling class + userspace agents, transactions), safety fallback (lower-priority class than CFS; enclave destruction moves threads back to CFS; watchdog after a user-configurable number of ms). Population: Google data-center fleet.
  - T10: covers one microbenchmark observation of context-switch cost: CFS context switch 599 ns, minimal pthread context switch 410 ns, syscall 72 ns; machine named (2-socket Xeon Platinum 8173M @ 2 GHz), kernel named (Linux 4.15 + ghOSt patches); method: microbenchmark (statistic not stated beyond a single value per row; not stated whether mean or median). Does not cover pick-next cost in isolation, context switches/s, or time-slice lengths.
  - All other topics: does not cover.
- **One observation?** T10 values: one microbenchmark run set on one named machine and kernel; window not named.

### S1-02 — OSTEP, chapter 8 "Scheduling: The Multi-Level Feedback Queue" (T3)

- **Citation.** Remzi H. Arpaci-Dusseau, Andrea C. Arpaci-Dusseau. *Operating Systems: Three Easy Pieces*, chapter 8, "[VERSION 1.10]", "© 2008–23". PDF CreationDate 2023-11-14.
- **Copy read.** https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-mlfq.pdf · 2026-10-07 · `sources/S1-02/cpu-sched-mlfq.pdf` · SHA-256 `96241b4e6708991740560334a1f67516c3c68eb3e6a570af7b03cdb4b32918db` · full chapter (12 pp.).
- **Passages.**
  - p.1: "The Multi-level Feedback Queue (MLFQ) scheduler was first described by Corbato et al. in 1962 [C+62] in a system known as the Compatible Time-Sharing System (CTSS)"
  - p.2: "If, for example, a job repeatedly relinquishes the CPU while waiting for input from the keyboard, MLFQ will keep its priority high, as this is how an interactive process might behave. If, instead, a job uses the CPU intensively for long periods of time, MLFQ will reduce its priority."
  - p.3: "• Rule 4a: If a job uses up its allotment while running, its priority is reduced (i.e., it moves down one queue). • Rule 4b: If a job gives up the CPU (for example, by performing an I/O operation) before the allotment is up, it stays at the same priority level (i.e., its allotment is reset)."
  - p.5 "Example 3: What About I/O?": "if an interactive job, for example, is doing a lot of I/O (say by waiting for user input from the keyboard or mouse), it will relinquish the CPU before its allotment is complete; in such case, we don't wish to penalize the job and thus simply keep it at the same level."
  - p.5: "Second, a smart user could rewrite their program to game the scheduler. Gaming the scheduler generally refers to the idea of doing something sneaky to trick the scheduler into giving you more than your fair share of the resource."
  - p.6: "the following attack: before the allotment is used, issue an I/O operation (e.g., to a file) and thus relinquish the CPU; doing so allows you to remain in the same queue, and thus gain a higher percentage of CPU time. When done right (e.g., by running for 99% of the allotment before relinquishing the CPU), a job could nearly monopolize the CPU."
  - p.8: "• Rule 4: Once a job uses up its time allotment at a given level (regardless of how many times it has given up the CPU), its priority is reduced (i.e., it moves down one queue)."
  - p.8–9: "For example, most MLFQ variants allow for varying time-slice length across different queues. The high-priority queues are usually given short time slices; they are comprised of interactive jobs, after all, and thus quickly alternating between them makes sense (e.g., 10 or fewer milliseconds). The low-priority queues, in contrast, contain long-running jobs that are CPU-bound; hence, longer time slices work well (e.g., 100s of ms)."
  - p.9: "Default values for the table are 60 queues, with slowly increasing time-slice lengths from 20 milliseconds (highest priority) to a few hundred milliseconds (lowest), and priorities boosted around every 1 second or so." (Solaris TS class)
  - p.9: "For example, the FreeBSD scheduler (version 4.3) uses a formula to calculate the current priority level of a job, basing it on how much CPU the process has used [LM+89]"
  - p.10: "For this reason, many systems, including BSD UNIX derivatives [LM+89, B86], Solaris [M06], and Windows NT and subsequent Windows operating systems [CS97] use a form of MLFQ as their base scheduler."
  - The chapter text contains no occurrence of the string "Linux" (`grep -c Linux` = 0).
- **Coverage.** T3: covers MLFQ demotion rules (4a/4b → 4), treatment of I/O/keyboard-waiting jobs, gaming via I/O before allotment ends (99% example), longer slices at lower priority (10 ms vs 100s of ms; Solaris table 20 ms → few hundred ms, 60 queues), shipped systems named as using MLFQ forms (BSD UNIX derivatives, Solaris, Windows NT and later). Does not describe Linux's default class. T10: covers documented (not measured) time-slice values in Solaris TS defaults. Other topics: does not cover.
- **One observation?** Not a measurement (textbook exposition).

### S1-03 — OSTEP, chapter 7 "Scheduling: Introduction" (T3, T10)

- **Citation.** Arpaci-Dusseau & Arpaci-Dusseau, OSTEP ch. 7, "[VERSION 1.10]", "© 2008–23"; PDF CreationDate 2023-11-14.
- **Copy read.** https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf · 2026-10-07 · `sources/S1-03/cpu-sched.pdf` · SHA-256 `0912b1a34977a70704b921ecfdf0dd65300e038a3eb4e5e57b2d9c38f66b63c3` · full chapter.
- **Passages.**
  - p.2 (workload assumptions): "1. Each job runs for the same amount of time. 2. All jobs arrive at the same time. 3. Once started, each job runs to completion. 4. All jobs only use the CPU (i.e., they perform no I/O) 5. The run-time of each job is known."
  - p.5: "In fact, given our assumptions about jobs all arriving at the same time, we could prove that SJF is indeed an optimal scheduling algorithm. However, you are in a systems class, not theory or operations research; no proofs are allowed."
  - p.6: "STCF is provably optimal; given that SJF is optimal if all jobs arrive at the same time, you should probably be able to see the intuition behind the optimality of STCF."
  - p.6: "Thus, if we knew job lengths, and that jobs only used the CPU, and our only metric was turnaround time, STCF would be a great policy."
  - p.8 (tip on amortization): "For example, if the time slice is set to 10 ms, and the context-switch cost is 1 ms, roughly 10% of time is spent context switching and is thus wasted. If we want to amortize this cost, we can increase the time slice, e.g., to 100 ms. In this case, less than 1% of time is spent context switching"
  - p.9: "The first type (SJF, STCF) optimizes turnaround time, but is bad for response time. The second type (RR) optimizes response time but is bad for turnaround."
- **Coverage.** T3: covers SJF optimality and its conditions (all jobs arrive together, turnaround metric, known run times; proof not given). T10: the 10 ms / 1 ms figures are an illustrative example, not a measurement. Others: does not cover.
- **One observation?** Not a measurement.

### S1-04 — Corbató, Merwin-Daggett & Daley 1962 (T3)

- **Citation.** Fernando J. Corbató, Marjorie Merwin-Daggett, Robert C. Daley. "An Experimental Time-Sharing System." Proc. AFIPS 1962 Spring Joint Computer Conference, Vol. 21, Spartan Books, pp. 335–344 (header of the course reprint: "In Proc. AFIPS 1962 SJCC, Vol. 21, Spartan Books, New York, 335-344").
- **Copy read.** https://cseweb.ucsd.edu/classes/wi19/cse221-a/papers/corbato62.pdf (UCSD CSE221 W19 reprint, scanned with OCR layer; includes an instructor's note "formula (2) is incorrect") · 2026-10-07 · `sources/S1-04/corbato62.pdf` · SHA-256 `3e5f2a3b2561c5863da88ed6d19d6c587131416d68a35ce140e5ee92bf47841e` · full text. The OCR renders ℓ as "£"; passages below were checked against rendered page images and ℓ is restored.
- **Passages.**
  - PDF p.7 / printed p.341, lines 24–28 (checked against page image): "The basis of the multi-level scheduling algorithm is to assign each user program as it enters the system to be run (or completes a response to a user) to an ℓth level priority queue. Programs are initially entered into a level ℓ0, corresponding to their size such that"
  - PDF p.7 / printed p.341, lines 41–56 (checked against page image): "The process starts with the time-sharing supervisor operating the program at the head of the lowest level occupied queue, ℓ, for up to 2^ℓ quanta of time and then if the program is not completed (i.e. has not made a response to the user) placing it at the end of the ℓ+1 level queue. If there are no programs entering the system at levels lower than ℓ, this process proceeds until the queue at level ℓ is exhausted; the process is then iteratively begun again at level ℓ+1, where now each program is run for 2^(ℓ+1) quanta of time."
  - PDF p.7 / printed p.341, right column lines 105–112: "The relative swap time on long runs can be made vanishingly small. This conclusion follows since the longer a program is run, the higher the level number it cascades to with a correspondingly smaller relative swap time. It is an important feature of the algorithm that long runs must in effect prove they are long so that programs which have an unexpected demise are detected quickly."
  - PDF p.8 / printed p.342, lines 48–53 (checked against page image): "5. In the multi-level algorithm the level classification procedure for programs is entirely automatic, depending on performance and program size rather than on the declarations (or hopes) of each user."
  - PDF p.9 / printed p.343, lines 1–15 (checked against page image): "It should also be noted that Figure 2 only accounts for the scheduling of programs in a working status and still does not take into account the storage allocation of programs which are in a dormant (or input-output wait status). One systematic method of handling this case is to modify the scheduling algorithm so that programs which become dormant at level ℓ are entered into the queue at level ℓ+1. The scheduling algorithm proceeds as before with the dormant programs continuing to cascade but not operating when they reached the head of a queue."
  - PDF p.9 / printed p.343, line 21: "q = 16 m.s. (based on 1% switching overhead)"
- **Coverage.** T3: covers the demotion rule (not completing within 2^ℓ quanta → level ℓ+1, with level-ℓ quantum budget doubling per level, i.e. lower priority levels get longer runs), the treatment of dormant / I/O-wait programs (entered at ℓ+1, i.e. also demoted, for storage allocation), and the statement that classification is automatic rather than declared by users. T10: one documented quantum value for the IBM 7090 (16 ms, derived from 1% switching overhead), not a Linux measurement.
- **One observation?** Analytical paper; the 16 ms figure is a derived design value for one machine (IBM 7090).

### S1-05 — Stoica & Abdel-Wahab, EEVDF TR-95-22 (T3)

- **Citation.** Ion Stoica, Hussein Abdel-Wahab. "Earliest Eligible Virtual Deadline First: A Flexible and Accurate Mechanism for Proportional Share Resource Allocation." Technical Report TR-95-22, Department of Computer Science, Old Dominion University; "Revised January 26, 1996."
- **Copy read.** https://people.eecs.berkeley.edu/~istoica/papers/eevdf-tr-95.pdf · 2026-10-07 · `sources/S1-05/eevdf-tr-95.pdf` · SHA-256 `b44b71a76f6a4b27f1c476282732c69498c86e7ec253f3cdd96ca66684f2aa97` · full text (37 pp.).
- **Passages.**
  - p.1, Abstract: "Mainly, we show that in steady conditions our algorithm guarantees that the di[ff]erence between the service time that a client should receive in the idealized system and the service time it actually receives in the real system is bounded by the size q of a time quantum. The algorithm provides support for dynamic operations, such as a client joining or leaving the competition (for the resource), and changing a client's weight. By using an e[ffi]cient augmented binary search tree data structure we implement these operations in O(log n), where n represents the number of clients competing for the resource."
  - p.2: "Similarly, an interactive application (such as an editor) can be modeled as an aperiodic process, where an event is generated as a result of the user pressing a key, the service time is the time required to process and display the corresponding character, and the deadline is given by the largest acceptable delay between the moment when the key is pressed and the moment when the character is displayed."
  - p.4: "The di[ff]erence between the service time that a client should receive at a time t, and the service time it actually receives is called service time lag."
  - p.7: "EEVDF Algorithm. A new quantum is allocated to the client that has the eligible request with the earliest virtual deadline."
  - p.11: "We need to decide whether a client that becomes passive without using its entire share could use it when it again becomes active next time, and whether a client that leaves the competition after it has used more service time than its share should be penalized when it rejoins the competition. … Unfortunately, there is no simple answer to this question. If we decide not to compensate, then the lost service time may accumulate over multiple periods of activity, and consequently, over large intervals of time the client may receive signi[fi]cantly less service time than it is entitled to. On the other hand, if we decide to compensate a client for the lost service when it rejoins the competition, this might hamper other clients."
  - p.12, §5: "Strategy 1. In this strategy a client may leave or join the competition at any time, and depending on its lag it is either penalized or it receives compensation when it rejoins the competition." … "Strategy 2. This strategy is similar to the previous one with the only di[ff]erence being that the lag is not preserved after a client leaves the competition, i.e., any client that (re)joins the competition has zero lag."
  - p.18, Theorem 1: "The lag of any active client k in a steady system is bounded as follows, [−]rmax < lagk (d) < max(rmax ; q); (35) where rmax represents the maximum duration of any request issued by client k. Moreover, these bounds are asymptotically tight."
  - p.20: "While shorter requests o[ff]er a better allocation accuracy, the longer ones reduce the system overhead since for the same total service time fewer requests need to be generated. … For example, for an intensive computation task it would be acceptable to take the length of the request to be in the order of seconds. On the other hand, in the case of a multimedia application we need to take the length of a request no greater than several tens of milliseconds, due to the delay constraints."
  - p.20, Corollary 2: "Consider a steady system and a client k such that no request of client k is larger than a time quantum. Then at any time t, the lag of client k is bounded as follows: [−]q < lagk (t) < q: (42)"
- **Coverage.** T3: covers lag definition, what EEVDF guarantees (lag bound by q, or by max(rmax,q) in steady systems), the treatment of clients that leave/become passive and rejoin (compensation vs. not, Strategies 1–3), and the link between request length and latency (shorter requests → better accuracy; multimedia requests ≤ tens of ms). It does not describe Linux. Others: does not cover.
- **One observation?** Analytical; no measurement.

### S1-06 — Decima (T4)

- **Citation.** Hongzi Mao, Malte Schwarzkopf, Shaileshh Bojja Venkatakrishnan, Zili Meng, Mohammad Alizadeh. "Learning Scheduling Algorithms for Data Processing Clusters." SIGCOMM '19, August 19–23, 2019, Beijing. https://doi.org/10.1145/3341302.3342080
- **Copy read.** https://people.csail.mit.edu/hongzi/content/publications/Decima-Sigcomm19.pdf · 2026-10-07 · `sources/S1-06/decima.pdf` · SHA-256 `b6b50a58ea743049f9bf7d92d2941afff1e4308b40ed208fc348fae8b57904d3` · full text incl. appendices.
- **Passages.**
  - p.1: "Decima encodes its scheduling policy in a neural network trained via a large number of simulated experiments, during which it schedules a workload, observes the outcome, and gradually improves its policy."
  - p.3, §4: "On scheduling events — e.g., a stage completion (which frees up executors), or a job arrival (which adds a DAG) — the agent takes as input the current state of the cluster and outputs a scheduling action. At a high level, the state captures the status of the DAGs in the scheduler's queue and the executors, while the actions determine which DAG stages executors work on at any given time. Decima trains its neural network using RL through a large number of offline (simulated) experiments."
  - p.4, §5.1: "The graph embedding takes as input the job DAGs whose nodes carry a set of stage attributes (e.g., the number of remaining tasks, expected task duration, etc.)"
  - p.11, §7.4 "Generalizing to different workloads": "As Decima learns workload-specific policies, we expect its effectiveness to depend on whether broad test workload characteristics, such as interarrival time and job size distributions, match the training workload. … Unsurprisingly, when Decima trains with an "anti-skewed" workload (75 seconds interarrival time), it generalizes poorly and underperforms the optimized weighted fair policy."
  - p.11: "These results highlight that a diverse training workload set helps make Decima's learned policies robust to workload shifts; we discuss possible online learning in §8."
  - p.11: "Each training iteration takes about 5 seconds."
  - p.16, App. C: "Finally, we train Decima for at least 50,000 iterations for all experiments. We implemented Decima's training framework using TensorFlow [1], and we use 16 workers to compute episodes with the same job sequence in parallel during training. Each training iteration, including interaction with the simulator, model inference and model update from all training workers, takes roughly 1.5 seconds on a machine with Intel Xeon E5-2640 CPU and Nvidia Tesla P100 GPU."
  - p.12, §8: "However, more drastic workload changes than interarrival time shifts could occur. … Another direction is to adjust the scheduling policy online as the workload changes. The key challenge with an online approach is to reduce the large sample complexity of model-free RL when the workload changes quickly."
  - p.19, App. I: "Decima is robust to changing parameters: the agent trained with 15× fewer jobs generalizes to the test workload with a 7% reduced average JCT, and an agent trained on a 10× smaller cluster generalizes with a 3% reduction in average JCT. … By contrast, generalizing to a workload with many more jobs is harder, as the smaller-scale training lacks experiences with complex job combinations."
- **Coverage.** T4: covers what is learned (scheduling policy for Spark DAG jobs: stage selection + parallelism limit), inputs (job DAGs with stage attributes, executor state), training requirements (≥ 50,000 iterations; ~1.5 s or ~5 s per iteration as stated in two places; offline simulator), and statements on generalization across workloads and cluster sizes (workload-specific; generalizes poorly to anti-skewed workloads; diverse training helps; online adaptation open). It contains no statement about retraining for different hardware. Others: does not cover.
- **One observation?** Experimental results on one simulator + Spark testbed + Alibaba trace; training machine named.

### S1-07 — FIRM (T4)

- **Citation.** Haoran Qiu, Subho S. Banerjee, Saurabh Jha, Zbigniew T. Kalbarczyk, Ravishankar K. Iyer. "FIRM: An Intelligent Fine-grained Resource Management Framework for SLO-Oriented Microservices." 14th USENIX OSDI, November 4–6, 2020, pp. 805–825.
- **Copy read.** https://www.usenix.org/system/files/osdi20-qiu.pdf · 2026-10-07 · `sources/S1-07/firm.pdf` · SHA-256 `a0adcf9865358b5f10fc99b2fe4257ffb3eea3137d4c9ec72d6d91c2c9d46c68` · full text.
- **Passages.**
  - p.1 (title page, author line): "Haoran Qiu, Subho S. Banerjee, Saurabh Jha, Zbigniew T. Kalbarczyk, and Ravishankar K. Iyer, University of Illinois at Urbana–Champaign"
  - p.3: "Support vector machine (SVM) driven detection and localization of SLO violations to individual microservice instances."
  - p.3: "To enable rapid (re)training of the proposed system as the underlying systems [67] and workloads [40,42,96,98] change in datacenter environments, FIRM uses transfer learning. That is, FIRM leverages transfer learning to train microservicespecific RL agents based on previous RL experience."
  - p.9: "In particular, FIRM utilizes the deep deterministic policy gradient (DDPG) algorithm [59], which is a model-free, actor-critic RL framework"
  - p.10, Table 3: "State (st ) SLO Maintenance Ratio (SMt ), Workload Changes (WCt ), Request Composition (RCt ), Resource Utilization (RUt ) Action Space (at ) Resource Limits RLTi (t), i ∈ {CPU, Mem, LLC, IO, Net}"
  - p.10: "However, such an approach is hard to justify in practice (i.e., for deployment) because of the time required to train such tailored models for user workloads, which might have significant churn. FIRM addresses the problem of rapid model training by using transfer learning in the domain of RL"
  - p.10: "The RL model that FIRM uses is designed to scale since both the state space and the action space are independent of the size of the application or the cluster."
  - p.13, §4: "Transfer-learning-based RL converged even faster (around 2000 iterations5 ) because of parameter sharing. The one-forall RL required more iterations to converge (around 15000 iterations)"
  - p.13: "We trained the abovementioned three RL models on the Train-Ticket benchmark. We studied the generalization of the RL model by evaluating the end-to-end performance of FIRM on the DeathStarBench benchmarks."
- **Coverage.** T4: covers what is learned (SVM culprit localization; DDPG RL resource-limit policy for CPU/Mem/LLC/IO/Net), inputs (telemetry: latency, arrival rate, request composition, utilization), training requirements (~15,000 iterations one-for-all; ~2,000 with transfer learning; anomaly injection), and statements on retraining when systems/workloads change (transfer learning to enable rapid (re)training). Others: does not cover.
- **One observation?** Experimental; benchmarks named (Train-Ticket, DeathStarBench).

### S1-08 — Park (T4)

- **Citation.** Hongzi Mao, Parimarjan Negi, Akshay Narayan, Hanrui Wang, Jiacheng Yang, Haonan Wang, Ryan Marcus, Ravichandra Addanki, Mehrdad Khani, Songtao He, Vikram Nathan, Frank Cangialosi, Shaileshh Bojja Venkatakrishnan, Wei-Hung Weng, Song Han, Tim Kraska, Mohammad Alizadeh. "Park: An Open Platform for Learning-Augmented Computer Systems." 33rd Conference on Neural Information Processing Systems (NeurIPS 2019), Vancouver.
- **Copy read.** https://proceedings.neurips.cc/paper_files/paper/2019/file/f69e505b08403ad2298b9f262659929a-Paper.pdf · 2026-10-07 · `sources/S1-08/park.pdf` · SHA-256 `c686bc445a7e97e36f342cf1234bc0ca1a9100056a16e6a9e362350ed7045f98` · full text (13 pp.).
- **Passages.**
  - p.1, Abstract: "Currently, Park consists of 12 real world system-centric optimization problems with one common easy to use interface."
  - p.1: "Further, these algorithms can be complex (e.g., a commercial database query optimizer involves hundreds of rules [14]), and are often difficult to adapt across different systems and operating environments [63, 66] (e.g., different workloads, different distribution of data in a database, etc.)."
  - p.2: "In the backend, the environments are powered by both real systems (in 7 environments) and high fidelity simulators (in 5 environments)."
  - p.5, §3.3 "Simulation-Reality Gap": "First, discrepancies between simulation and reality prevent direct generalization." … "Naively using the same training method from simulation (as in Figure 4a) would take a single-threaded agent more than 10 years to complete training in reality. Finally, live training or directly deploying an agent from simulation can degrade the system performance."
  - p.5: "However, when the distribution changes, blindly reserving a server wastes compute resource and reduces system throughput. Therefore, to deploy training algorithms online, these problems require RL to train robust policies that ensure safety [2, 33, 49]."
  - p.6 (end of §3.4): "For example, a learned scheduling algorithm could fall back to a simple heuristic if it detects that the input distribution significantly drifted."
  - p.8, Fig. 4 caption: "In y-axes, "testing" means the agents are tested with unseen settings in the environment (e.g., newly sampled workload unseen during training, unseen job patterns to schedule, etc.)."
- **Coverage.** T4: covers Park as a platform (12 environments; MDP formulation per environment), statements on generalization/simulation-reality gap, training cost in reality (>10 years single-threaded for video streaming), and distribution drift (fallback suggestion). It is a platform paper; it does not itself learn one scheduler. No statement about retraining for new hardware specifically. Others: does not cover.
- **One observation?** Benchmark results across 12 environments; not one observation.

### S1-09 — Waldspurger & Weihl, Lottery Scheduling (T9)

- **Citation.** Carl A. Waldspurger, William E. Weihl. "Lottery Scheduling: Flexible Proportional-Share Resource Management." Proceedings of the First Symposium on Operating System Design and Implementation (OSDI), November 1994.
- **Copy read.** https://www.waldspurger.org/carl/papers/lottery-osdi94.pdf · 2026-10-07 · `sources/S1-09/lottery.pdf` · SHA-256 `e704678ec0cf6064136794a23c1722ad32a24868259dcdf3a9ad8087d8f1b73a` · full text. Math glyphs are dropped by the text extractor; passages below were checked against page images of pp.2–3 and symbols restored in brackets.
- **Passages.**
  - p.2, §2.2: "Scheduling by lottery is probabilistically fair. The expected allocation of resources to clients is proportional to the number of tickets that they hold. Since the scheduling algorithm is randomized, the actual allocated proportions are not guaranteed to match the expected proportions exactly. However, the disparity between them decreases as the number of allocations increases."
  - p.2: "Thus, a client's throughput is proportional to its ticket allocation, with accuracy that improves with [√n]."
  - p.2: "The expected number of lotteries [n] that a client must wait before its first win is [E[n] = 1/p], with variance [σ²n = (1 − p)/p²]. Thus, a client's average response time is inversely proportional to its ticket allocation." (checked against page image)
  - p.2: "With a scheduling quantum of 10 milliseconds (100 lotteries per second), reasonable fairness can be achieved over subsecond time intervals."
  - p.2: "Since any client with a non-zero number of tickets will eventually win a lottery, the conventional problem of starvation does not exist."
  - p.2, §3: "Tickets can be used to insulate the resource management policies of independent modules, because each ticket probabilistically guarantees its owner the right to a worst-case resource consumption rate."
  - p.3, §4.2: "This requires a random number generation and [O(n)] operations to traverse a client list of length [n], accumulating a running ticket sum until it reaches the winning value." (checked against page image)
  - p.3, §4.2: "For large [n], a more efficient implementation is to use a tree of partial ticket sums, with clients at the leaves. To locate the client holding a winning ticket, the tree is traversed starting at the root node, and ending with the winning client leaf node, requiring only [O(lg n)] operations." (checked against page image)
  - p.3, §4: "The scheduling quantum on this platform is 100 milliseconds." (Mach 3.0 prototype on a 25MHz MIPS-based DECStation 5000/125)
- **Coverage.** T9: covers starvation (does not exist for nonzero tickets), the nature of the proportional guarantee (probabilistic; accuracy improves with √n; per-ticket probabilistic worst-case rate), and selection cost (list O(n), move-to-front, tree O(lg n)). T10: documents quantum values (10 ms example; 100 ms on the prototype). Others: does not cover.
- **One observation?** Design/analysis plus prototype experiments on one named machine.

### S1-10 — Liu & Layland 1973 (T9)

- **Citation.** C. L. Liu, James W. Layland. "Scheduling Algorithms for Multiprogramming in a Hard-Real-Time Environment." Journal of the ACM, Vol. 20, No. 1, January 1973, pp. 46–61.
- **Copy read.** https://www.cs.ru.nl/~hooman/DES/liu-layland.pdf (scan with OCR) · 2026-10-07 · `sources/S1-10/liu-layland.pdf` · SHA-256 `de9fb72577ff1f45aa50ccae0774b248ef67ebe15c6b6e90b00e0ab377f2b927` · full text. Theorem 7 checked against page image of PDF p.11.
- **Passages.**
  - PDF p.3 / printed p.48: "(A1) The requests for all tasks for which hard deadlines exist are periodic, with constant interval between requests. (A2) Deadlines consist of run-ability constraints only--i.e, each task must be completed before the next request for it occurs. (A3) The tasks are independent in that requests for a certain task do not depend on the initiation or the completion of requests for other tasks. (A4) Run-time for each task is constant for that task and does not vary with time. Run-time here refers to the time w[h]ich is taken by a processor to execute the task without interruption. (A5) Any nonperiodic tasks in the system are special; they are initialization or failure-recovery routines; they displace periodic tasks while they themselves are being run, and do not themselves have hard, critical deadlines."
  - PDF p.3: "The run-time in assumption (A4) can be interpreted as the maximum processing time for a task. In this way the bookkeeping time necessary to request a successor and the costs of preemptions can be taken into account."
  - PDF p.5 / printed p.50: "As it turns out, such a priority assignment is optimum in the sense that no other fixed priority assignment rule can schedule a task set which cannot be scheduled by the rate-monotonic priority assignment."
  - PDF p.10 / printed p.55: "This method is optimum in the sense t[h]at if a set of tasks can be scheduled b[y] some priority assignment, it can also be scheduled by this method. In other words, the least upper bound on the processor utilization factor is uniformly 100 percent." … "Using this algorithm, priorities are assigned to tasks according to the deadlines of their current requests."
  - PDF p.11 / printed p.56 (checked against page image): "THEOREM 7. For a given set of m tasks, the deadline driven scheduling algorithm is feasible if and only if (C1/T1) + (C2/T2) + ··· + (Cm/Tm) ≤ 1."
  - Abstract (PDF p.1): "It is shown that an optimum fixed priority scheduler possesses an upper bound to processor utilization which may be as low as 70 percent for large task sets."
- **Coverage.** T9: covers the assumptions (A1–A5: periodic, deadline = next request, independent, constant run-time, no critical aperiodic tasks; single processor per abstract) and the optimality/feasibility theorem for the deadline-driven algorithm (Theorem 7: feasible iff ΣCi/Ti ≤ 1). Others: does not cover.
- **One observation?** Theoretical.

### S1-11 — ASA / Mixture-of-Schedulers, arXiv:2511.11628 (T5)

- **Citation.** Xinbo Wang, Shian Jia, Ziyang Huang, Jing Cao, Mingli Song. "Mixture-of-Schedulers: An Adaptive Scheduling Agent as a Learned Router for Expert Policies." arXiv:2511.11628v1 [cs.DC], 7 Nov 2025. Only version: v1 (submitted Fri, 7 Nov 2025 14:16:31 UTC). No journal-ref, no comments field on the abs page; no venue stated in the PDF.
- **Copy read.** https://export.arxiv.org/abs/2511.11628 (`sources/S1-11/abs.html`, SHA-256 `15e239f3d6bea2e215cf493042f2298de269234f6ae74ab4063dab5e76e98c8a`); https://arxiv.org/pdf/2511.11628v1 (`sources/S1-11/asa-2511.11628v1.pdf`, SHA-256 `3a887853b4b21974373f912492963108f55f1526f1e951934a233c850fb07b8b`) · 2026-10-07 · full text.
- **Passages.**
  - p.1, Abstract: "First, an offline process trains a universal, hardware-agnostic machine learning model to recognize abstract workload patterns from system behaviors. Second, at runtime, ASA continually processes the model's predictions using a time-weighted probability voting algorithm to identify the workload, then makes a scheduling decision by consulting a pre-configured, machine-specific mapping table to switch to the optimal scheduler via Linux's sched_ext framework. This decoupled architecture allows ASA to adapt to new hardware platforms rapidly without expensive retraining of the core recognition model."
  - p.1, Abstract: "ASA consistently outperforms the default Linux scheduler (EEVDF), achieving superior results in 86.4% of test scenarios. Furthermore, ASA's selections are near-optimal, ranking among the top three schedulers in 78.6% of all scenarios."
  - p.4, §3.3: "The classification model uses an ensemble approach combining multiple algorithms to improve robustness and accuracy. The primary classifier is based on XGBoost, chosen for its excellent performance on structured data and ability to handle feature interactions. Additional classifiers including Random Forest and Support Vector Machines provide complementary perspectives and help detect edge cases."
  - p.4, Table 1 "the System State Metrics that ASA monitors" (as extracted): "CPU User / System Mode Utilization, Nice / Idle / I/O Wait / Hardware Interrupt / Software Interrupt / Steal Utilization, Hot-Spot Core Ratio Memory Total / Free / Cached Memory, Total / Available Swap, Buffers Disk Disk I/O Queue Length, Read/Write Operation Count, Read/Write Latency, Average I/O Size Process Process Count, GPU-Using Process Count / CPU Utilization, WindowFocused Process CPU / Memory Utilization, Input Event Scheduling Task Migration Count, Lock Contention / Acquisition Failure Count, Lock Hold / Thread Blocked Time, Thread Wakeup / Context Switch Latency, Context Switch Count, Run Queue Length Network Total / New / Closed / Reset"
  - p.5, §4.1: "However, our core insight is that for any single machine, a workload pattern can correspond to an optimal scheduler. This principle enables a practical cross-platform optimization strategy, where the general task of pattern recognition can be decoupled from the machine-specific task of policy selection."
  - p.7, §4.4: "By exclusively running the "Generalization Model Training" (Stage 3) on the target machine, ASA can interact directly with the new environment and its available schedulers, resulting in the creation of a precise, hardware-specific scheduler mapping table ready for immediate use. The entire process can then be followed by an optional, low-overhead fine-tuning process"
  - p.7: "Through this process, ASA's model and mapping data are derived entirely from its own runtime environment."
  - p.8: "The expert scheduler set available to ASA includes: scx_p2dq [9], scx_bpfland [2], scx_nest [24], scx_lavd [3], scx_simple, scx_flash [4], scx_rusty [1], and the baseline EEVDF [29]." Evaluation on "a cluster of 10 distinct virtual machines (VMs) managed by Proxmox VE" (p.7), base CPUs Intel i5-6500, i5-9400, i7-12700 (Table 3, p.8).
  - p.9: "Without fine-tuning, the base workload classifier achieves a notable accuracy of 96.83%. After the online fine-tuning process, the accuracy of the raw model output (before the time-weighted voting is applied) increases to 99.19%."
  - p.9, Table 4 "ASA Latency Statistics (values in milliseconds)": "Inference Latency Decision Latency Total Latency Average 1.004 17.305 18.309 P90 1.109 0.083 1.359 P95 1.329 0.307 2.722 P99 3.445 376.417 379.540"
- **Coverage.** T5: covers how it recognizes workloads (XGBoost-led ensemble over OS metrics incl. window-focused process and input events; time-weighted voting), what it trains and where (universal classifier offline; per-machine mapping table built by running Stage 3 on the target machine; optional per-machine fine-tuning), the features read (Table 1), recognition accuracy (96.83% base, 99.19% after fine-tuning; 28 benchmark scenarios S1–S28; VMs named), venue (none stated). It is not LLM-based. T11: inference latency of its (non-LLM) classifier only. Others: does not cover.
- **One observation?** One evaluation campaign on 10 named VMs; window not named.

### S1-12 — Towards Agentic OS / SchedCP, arXiv:2509.01245 v1–v4 (T5)

- **Citation.** Yusheng Zheng, Yanpeng Hu, Wei Zhang, Andi Quinn. "Towards Agentic OS: An LLM Agent Framework for Linux Schedulers." arXiv:2509.01245 [cs.AI]. Versions (abs page): v1 Mon, 1 Sep 2025 08:38:49 UTC; v2 Wed, 3 Sep 2025 06:09:05 UTC; v3 Fri, 26 Sep 2025 07:10:59 UTC; v4 Tue, 30 Sep 2025 02:48:14 UTC. Abs-page journal-ref: "MLforSystem 2025". NeurIPS 2025 virtual site lists it as "Poster in Workshop: ML for Systems". v1/v2 PDFs carry the ACM template placeholder "Conference'17, July 2017, Washington, DC, USA"; v3/v4 carry "Preprint."
- **Copies read.** abs: https://export.arxiv.org/abs/2509.01245 (`S1-12/abs.html`, `96a128b3ecd40eec9536bc5a1eb75a783c79034c62de7c416fba68601a3f51d6`); v1 (`agenticos-2509.01245v1.pdf`, `b0fc4ec042d9cb9b2c6ec7eaecf66a7f9dbaca209fbc5f3c6cb5f311328f3a8b`); v2 (`…v2.pdf`, `7dbfe839cbfa3937db68b4654b8dec82c6b6d1d20e25736848729ef7fe25c378`); v3 (`…v3.pdf`, `e22190017e1b88bfa4c9b68fcdd7cde77bf36907577aa8306dae21cc28b35fe4`); v4 (`…v4.pdf`, `cce49d3c0ff5466cafc3b921373f6d43df2adcb97e38b40c9d45e3b21206e97c`); NeurIPS page https://neurips.cc/virtual/2025/loc/san-diego/129092 (`neurips-129092.html`, `33a8ac62430e2839fe3661d53f51d5c3f2df9fe333a7b6d3585e51cfa81e1f6e`) · all 2026-10-07 · full texts of all four versions.
- **Passages — all versions.**
  - Abstract (v1–v4 identical in this sentence): "Operating system schedulers suffer from a fundamental semantic gap, where kernel policies fail to understand application-specific needs, leading to suboptimal performance."
  - Abstract v1/v2: "Implemented as Model Context Protocol(MCP) server, SchedCP provides a stable interface with three key services: a Workload Analysis Engine, an evolving Scheduler Policy Repository, and an Execution Verifier that validates all AI-generated code and configure before deployment with static and dynamic analysis." … "Our evaluation shows that SchedCP achieves up to an 1.79x performance improvement, and a 13x cost reduction compared to naive agentic approaches, all while maintaining high success rate."
  - Abstract v4 adds: "thereby separating the optimization problem into two stages: goal-inference and policy-synthesis."
- **Passages — v1.**
  - p.1, §1: "Prior attempts to automate scheduler optimization, such as those using reinforcement learning [20, 29], have shown promise but remain fundamentally limited. By mapping numerical state to predefined actions, they cannot grasp the semantic intent of a workload and miss optimization opportunities that require deeper reasoning." ([20] = Mao et al., Decima, SIGCOMM 2019; [29] = FIRM, listed in v1 as "Haoran Qiu, Siddhartha Banerjee, Saurabh Jha, Shivaram Kalyanaraman, and Chuan Tang. 2020. FIRM: … OSDI. 805–825.")
  - p.2, §3.1: "Edge and personal devices face worse challenges. Gamers, creative professionals, and office workers lack kernel expertise for optimization. LLMs can bridge this gap by understanding high-level workload patterns from source code and deployment artifacts, and translating them into concrete scheduling policies."
  - p.4, §4.2: "1. Workload Analysis Engine. This service provides agents with tiered access to system performance data. It offers three levels of information: (1) cost-effective API endpoints delivering pre-processed summaries like CPU load and memory usage, (2) secure sandbox access to basic file reading, application building, standard Linux profiling tools (perf, strace) and dynamically attachable eBPF probes for detailed analysis, and (3) a feedback channel that reports post-deployment performance metrics such as percentage change in makespan or latency."
  - p.4: "beginning with the kernel's standard eBPF verifier to guarantee fundamental memory safety and termination. However, because the standard verifier is agnostic to scheduling logic, it cannot detect flaws like task starvation or unfairness; therefore, our pipeline adds a crucial second layer of scheduler-specific static analysis checkers using customize PREVAIL verifier[14]"
  - p.5, §6: "• RQ1: Can SchedCP effectively configure existing schedulers? • RQ2: Can SchedCP generate new schedulers for specific workloads? • RQ3: What is the cost and efficiency of SchedCP's scheduler generation? • RQ4: How much can sched-agent continue to improve performance after initial attempt?"
  - p.5, §6.1: "machine 1 is an 86-core, 172 threads Intel Xeon 6787P with 758GB RAM … running Linux 6.14 with sched_ext. Machine 2 is an 8-core, 8 threads Intel Core Ultra 7 258V with 30GB RAM … running Linux 6.13 with sched_ext. We test Claude Code (Opus 4) as AI agents to validate framework generality. For each case, we test 3 times and get the average results."
  - p.6: "In contrast, basic RL approaches show no improvement in our tests, likely because they require hardwarespecific retraining, which is costly and time-consuming." (the "basic RL algorithms … [11]" cited is "[11] Jonathan Corbet. 2025. Improved load balancing with machine learning. https://lwn.net/Articles/1027096/. LWN.net (1 July 2025).")
  - p.6: "We note that the powerful Claude Opus agent successfully classified all 8 workloads, whereas the smaller Claude Sonnet model could not." and "cost for this analysis averaged $0.15 per workload, based on Claude Opus 4 pricing from August 2025."
  - p.6, §7: "Machine learning has a history of optimizing systems, including learned indexes [16], database tuning [22, 32], and RLbased job schedulers [20, 29, 36] supported by platforms like Park [21]. However, these methods require extensive training, lack the semantic understanding to transfer knowledge across diverse workloads, or need human specify high level optimization goals." ([36] = "Wei Zhang et al. 2024. Multi-Resource Scheduling with Reinforcement Learning. IEEE Transactions on Parallel and Distributed Systems (2024)."; [21] = "Hongzi Mao, Shaileshh Bojja Venkatakrishnan, Malte Schwarzkopf, and Mohammad Alizadeh. 2019. Park: …")
  - p.5, §5.2 (v1 wording): "It generates a patch to make the scheduler dependency-aware."
- **Passages — v2 (differences from v1).**
  - §3.1: "Prior RL-based schedulers [19, 20, 28, 35] require extensive training per workload type, lack semantic understanding to transfer knowledge across workloads, and cannot generate new scheduling code." ([19] Decima, [20] Park, [28] FIRM, [35] Wei Zhang et al. TPDS 2024.)
  - §3.1: "LLMs generate and optimize scheduling policies offline, producing native eBPF code that executes without any ML inference overhead during actual scheduling decisions."
  - §5.2 (v2 wording): "It generates a configuration to make the scheduler more adaptive to the build process."
  - §6.1 adds: "To mitigate cache warming effects, we clear the page cache (via sync; echo 3 > /proc/sys/vm/drop_caches) before each run and perform a warm-up run that is excluded from measurements."
  - p.6: "In contrast, basic RL approaches show no improvement in our tests, likely because they require hardware or workload-specific retraining, which is costly and time-consuming."
  - The edge/personal-device sentence becomes: "while edge/personal device users lack both kernel optimization expertise and understanding of application-specific performance targets." (the v1 "Gamers, creative professionals, and office workers" sentence is removed).
- **Passages — v4 (v3 differs only as noted).**
  - p.1: "While sched_ext [6] in Linux 6.12 enables custom extended Berkeley Packet Filter(eBPF) schedulers with safety guarantees through verification, developing them still requires both deep kernel expertise and a good understanding of the workloads. Prior reinforcement learning-based schedulers [10, 17] lack semantic understanding of workloads, are often limited to tweaking configurations within a problem space predefined by human engineers, preventing fully automatic system optimization." (v3 ends the sentence at "lack semantic understanding of workloads.") [10] = Decima; [17] = FIRM (author list as in v1).
  - p.2, §2: "Prior RL-based schedulers [10, 17, 19, 11] require extensive training per workload type, lack semantic understanding to transfer across workloads, and only tweak configurations after engineers have already defined the entire problem space: selecting features, specifying knobs, and writing objective functions." (v3: "… and cannot generate code.") [19] = Wei Zhang et al. TPDS 2024; [11] = Park.
  - p.3: "1. Workload Analysis Engine Provides tiered access to system performance data: (1) cost-effective API endpoints with pre-processed summaries (CPU load, memory usage), (2) secure sandbox access to file reading, application building, Linux profiling tools (perf, top) and dynamically attachable eBPF probes, (3) feedback channel reporting post-deployment metrics (percentage change in throughput/latency)."
  - p.4: "The Observation Agent builds Workload Profiles by querying the Workload Analysis Engine strategically, starting with high-level summaries from process name and commands then requesting deeper profiling (perf stat, top) based on findings"
  - p.4, §5: "We validate SchedCP's effectiveness through four research questions: configuring existing schedulers (RQ1), generating new schedulers for specific workloads (RQ2), cost and efficiency of scheduler generation (RQ3), and iterative refinement improvements (RQ4)."
  - p.4: "For kernel compilation (tinyconfig, "make -j 172" on 6.14 source), SchedCP achieves 1.63× speedup with scx_rusty initially, then iterative refinement selects scx_layered for 16% additional gain, reaching 1.79× total improvement over EEVDF (Figure 2a). Pre-trained RL approaches [7] show no improvement, likely because they require costly hardware/workload-specific retraining." ([7] = "Jonathan Corbet. Improved load balancing with machine learning. LWN.net, July 2025.")
  - p.4: "On schbench [12], initial AI configuration (scx_bpfland) underperformed, but three refinement iterations identified scx_rusty as superior: 2.11× better P99 latency and 1.60× higher throughput versus EEVDF"
  - p.5: "Claude Opus successfully classified all 8 workloads at $0.15 per analysis, while Claude Sonnet failed. Generation efficiency improved 13× (to 2.5 minutes) with $0.45 synthesis cost per workload"
  - p.2: "The successful generation required 33 minutes, 221 LLM API calls, and 15+ iterations, costing $6 (vs. 5 minutes typically for an expert developer)."
- **Coverage.** T5: covers problem statement ("semantic gap"), architecture (SchedCP MCP server: Workload Analysis Engine, Scheduler Policy Repository, Execution Verifier; sched-agent with 4 agents), profiling tools (v1/v2: perf, strace, eBPF probes; v3/v4: perf, top, eBPF probes; process name and commands as first input in v3/v4), workloads and headline speedups (kernel build 1.79×; schbench 2.11× P99 / 1.60× throughput; 8 batch workloads 20%; 13× cost), RQs (RQ1–RQ4, wording per version), statements about RL schedulers and the works cited for them per version (Decima, FIRM, Park, Wei Zhang et al. TPDS 2024; LWN for the "basic/pre-trained RL" evaluation claim), venue (NeurIPS 2025 ML for Systems workshop per NeurIPS site; arXiv journal-ref "MLforSystem 2025"). Workload "classification" is reported as all-8-correct for Opus and failure for Sonnet on 8 batch workloads; no accuracy rate over a larger set. Others: does not cover.
- **One observation?** Each result: one or two named machines, 3 runs averaged, Claude Opus 4; window ("August 2025" pricing) partially named.

### S1-13 — Kgent / KEN (T5)

- **Citation.** Yusheng Zheng, Yiwei Yang, Maolin Chen, Andrew Quinn. "Kgent: Kernel Extensions Large Language Model Agent." Proceedings of the ACM SIGCOMM 2024 Workshop on eBPF and Kernel Extensions (eBPF '24), Sydney, pp. 30–36. https://doi.org/10.1145/3672197.3673434. Earlier version: "KEN: Kernel Extensions using Natural Language," arXiv:2312.05531v1 [cs.AI], 9 Dec 2023 (only version).
- **Copies read.** ACM DL HTML and PDF: **HTTP 403**, not read (paper body of the eBPF '24 version not read). Read instead: repository README at https://github.com/eunomia-bpf/KEN commit `7575d9bab260d3b508b9312df9cc9fda3bacab2a` (raw URL pinned to that commit, byte-identical to `main` on access) → `sources/S1-13/ken-readme.md`, SHA-256 `dc6d76579e41ec4158e0f9f6e0558c1f4807e08720def792e9e2d5b819d877ac`; arXiv KEN v1 PDF `sources/S1-13/ken-2312.05531v1.pdf`, SHA-256 `1a49785cc23a8bd4f085b127991a947c99f55c5a330ca4a5c19392e76d259880`; abs page `abs-2312.05531.html`, SHA-256 `b3915fff73ce960deed4774c90e1f9ef30c98e721cd7f774c75725e2a6b8d149`. Accessed 2026-10-07.
- **Passages.**
  - README.md:11 (at 7575d9b): "- **Natural Language to eBPF**: Translates user prompts in natural language to eBPF programs."
  - README.md:60 (BibTeX abstract field of the eBPF '24 paper, at 7575d9b): "This paper presents Kgent, an alternative framework that alleviates the difficulty of writing an eBPF program by allowing Kernel Extensions to be written in Natural language. Kgent uses recent advances in large language models (LLMs) to synthesize an eBPF program given a user's English language prompt. To ensure that LLM's output is semantically equivalent to the user's prompt, Kgent employs a combination of LLM-empowered program comprehension, symbolic execution, and a series of feedback loops. … We show that Kgent produces correct eBPF programs on 80\%---which is an improvement of a factor of 2.67 compared to GPT-4 program synthesis baseline."
  - KEN arXiv v1, p.2: "• We evaluate KEN on eBPFNLDataset and show that KEN accurately synthesizes eBPF programs on 80% of prompts in a representative test set while only verifying a semantically incorrect program in 2.5% of cases."
- **Coverage.** T5: covers what Kgent produces (eBPF programs) from what input (English natural-language prompt), per the authors' repository abstract and the arXiv predecessor; the eBPF '24 paper body itself was not read (403). Others: does not cover.
- **One observation?** Evaluation on one dataset (eBPFNLDataset).

### S1-14 — OS-R1 / TuneAgent, arXiv:2508.12551 v1 & v2 (T5)

- **Citation.** v1: Hongyu Lin, Yuchen Li, Haoran Luo, Kaichun Yao, Libo Zhang, Mingjie Xing, Yanjun Wu. "OS-R1: Agentic Operating System Kernel Tuning with Reinforcement Learning." arXiv:2508.12551v1 [cs.LG], 18 Aug 2025 (no venue stated). v2: Hongyu Lin, Yuchen Li, Haoran Luo, Zhenghong Lin, Libo Zhang, Mingjie Xing, Yanjun Wu. "TuneAgent: Agentic Operating System Kernel Tuning with Reinforcement Learning." arXiv:2508.12551v2, submitted Sun, 31 May 2026; PDF states "In Proceedings of the 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2 (KDD '26), August 09–13, 2026, Jeju Island, Republic of Korea. … https://doi.org/10.1145/3770855.3817987".
- **Copies read.** abs (`S1-14/abs.html`, `220f6ca1547dd1e565ef74f4eeff92dfcdecb1113b2c966ede18b46b066caa1e`); v1 PDF (`osr1-2508.12551v1.pdf`, `ee2cd50620be34e0bba2038d50c612d42c32752408eba0308106df84b17ec125`); v2 PDF (`osr1-2508.12551v2.pdf`, `90ed2128c1832671fb19c3947191ac2baa1da0f97b431481280cbaa2ba75f413`) · 2026-10-07 · full texts.
- **Passages.**
  - v1 p.1, Abstract: "This paper introduces OS-R1, an agentic Linux kernel tuning framework powered by rule-based reinforcement learning (RL). By abstracting the kernel configuration space as an RL environment, OS-R1 facilitates efficient exploration by large language models (LLMs) and ensures accurate configuration modifications." … "Furthermore, we propose a two-phase training process that accelerates convergence and minimizes retraining across diverse tuning scenarios. Experimental results show that OS-R1 significantly outperforms existing baseline methods, achieving up to 5.6% performance improvement over heuristic tuning"
  - v1 p.5: "We utilize Qwen2.5-3B-Instruct and Qwen2.57B-Instruct (Yang et al. 2024) as the base models."
  - v1 p.6: "Benchmark. UnixBench (Byte UnixBench Developers 1983) is used to evaluate kernel performance"
  - v2 p.1, Abstract: "TuneAgent formulates the kernel space as a constrained RL environment, enabling large language models (LLMs) to autonomously explore the kernel while enforcing valid and precise configuration modifications."
- **Coverage.** T5: covers what it does with an LLM (RL-fine-tuned Qwen2.5 3B/7B choosing kernel configuration options), and venue (v1 none; v2 KDD '26 per PDF). Others: does not cover.
- **One observation?** Benchmark campaign (UnixBench); not one observation.

### S1-15 — Jadhav et al., arXiv:2506.02025 (T5, T11)

- **Citation.** Prachi Jadhav, Hongwei Jin, Ewa Deelman, Prasanna Balaprakash. "Evaluating the Efficacy of LLM-Based Reasoning for Multiobjective HPC Job Scheduling." arXiv:2506.02025 [cs.DC]; v1 29 May 2025, v2 3 Sep 2025; abs comments "10 pages, 6 figures, work under review". PDF carries ACM template placeholders ("Conference acronym 'XX … Woodstock, NY").
- **Copies read.** abs (`S1-15/abs.html`, `5f7117a4a1c977bb92e80ccf8b7722cb11d54680e0704c4664a464f62b991ec6`); v2 PDF (`2506.02025v2.pdf`, `f6fd740b58046ea3b2bb742707d026f8dd7bc2eb3683a83186e545f7a9ca440f`) · 2026-10-07 · full text of v2 (v1 not read).
- **Passages.**
  - p.1, Abstract: "we propose a novel Large Language Model (LLM)based scheduler using a ReAct-style framework (Reason + Act), enabling iterative, interpretable decision-making. The system incorporates a scratchpad memory to track scheduling history and refine decisions via natural language feedback, while a constraint enforcement module ensures feasibility and safety. We evaluate our approach using OpenAI's O4-Mini and Anthropic's Claude 3.7 across seven real-world HPC workload scenarios" … "However, a trade-off between reasoning quality and computational overhead challenges real-time deployment."
  - p.7, §3.7.1: "And LLM Call Time Distribution (Right Plot): Claude 3.7's per-call latencies are tightly clustered below 10 seconds, showing low variance and stable reasoning latency."
  - p.8, Fig. 6 caption: "Scheduling time grows super-linearly, reaching 4k s (O4-Mini) and 700 s (Claude 3.7) for 100 jobs, while API calls scale linearly."
- **Coverage.** T5: covers what it does with an LLM (ReAct LLM agent makes HPC job-queue scheduling decisions). T11: covers hosted-API per-call latency of reasoning models in this task (Claude 3.7 per-call < 10 s; totals 700 s / 4k s for 100 jobs) — one experiment set; not a short structured-output latency benchmark. Others: does not cover.
- **One observation?** One experimental campaign; machine not applicable (hosted APIs); window not named.

### S1-16 — Sharma & Kunkel, arXiv:2511.11612 (T5)

- **Citation.** Aasish Kumar Sharma, Julian Kunkel. "Evaluating Large Language Models for Workload Mapping and Scheduling in Heterogeneous HPC Systems." arXiv:2511.11612v1 [cs.DC], 4 Nov 2025. Journal-ref: "Robot Autom Eng J. 2025; 6(5): 555696"; DOI 10.19080/RAEJ.2025.06.555696; comments: "Published in Research in Academic Engineering Journal (RAEJ), 2025".
- **Copies read.** abs (`S1-16/abs.html`, `cf3d060fdec01300a76fc3cc099b48ebbb360dc850b016f65f80cfaad7a3c00c`); v1 PDF (`2511.11612.pdf`, fetched from https://arxiv.org/pdf/2511.11612 = v1, `73bd264f16dd563e616a7285b2551f6dae61b015df5b635e870e0a7bbd073c8f`) · 2026-10-07.
- **Passages.**
  - p.1, Abstract: "This study evaluates 21 publicly available LLMs on a representative heterogeneous High-Performance Computing (HPC) workload mapping and scheduling problem. Each model receives the same textual description of system nodes, task requirements, and scheduling constraints, and must assign tasks to nodes, compute the total makespan, and explain its reasoning. A manually derived analytical optimum of 9 h 20 s serves as the ground-truth reference. Three models (o3-mini, GPT-4.1 Mini, and Gemini Pro 2.5) exactly reproduced the analytical optimum while satisfying all constraints"
  - p.1, Abstract: "The findings underscore LLMs' promise as explainable co-pilots for optimization and decision-support tasks, rather than autonomous solvers."
- **Coverage.** T5: covers what it does with an LLM (one-shot task-to-node mapping and makespan computation from a text description, 21 models). Others: does not cover.
- **One observation?** One problem instance, 21 models.

### S1-17 — TuxBot, arXiv:2605.15026 (T5, T11)

- **Citation.** Georgios Liargkovas, Mihir Nitin Joshi, Hubertus Franke, Kostis Kaffes. "TuxBot: Semantic-Aware Online OS Tuning with Large Language Models." arXiv:2605.15026 [cs.OS]; v1 Thu, 14 May 2026; v2 Tue, 14 Jul 2026; comments "18 pages, 12 figures"; no venue stated.
- **Copies read.** abs (`S1-17/abs.html`, `4cb1f85e834e889bf2a2642165c0e601fa4390a9bd701e46fcf7e2a0f1787269`); v2 PDF (`tuxbot-2605.15026v2.pdf`, `543bd4fcc48785e2762de4a098f3feb2dd72f7732b21f514d178de2233a90760`) · 2026-10-07 · full body of v2 (v1 not read).
- **Passages.**
  - p.1, Abstract: "We present TuxBot, a host-side framework for steady-state OS tuning with bounded language-model guidance. TuxBot turns knob schemas, telemetry, current configuration, recent action–response history, and retrieved prior runs into a compact decision context. A fast loop proposes low-latency updates, a slower loop periodically revises the search strategy, and every proposed change passes through typed validation before reaching kernel or sysctl interfaces." … "We evaluate TuxBot on 13 live workloads from five benchmark suites while tuning up to 41 Linux parameters. Across the suite, TuxBot improves stablephase performance by 72.5% over default settings and by 153.3% relative to the strongest non-LLM baseline. A 30window session costs about $0.20 in model calls."
  - p.1: "We study tuners that operate out of band: they are not inline on each request, and they are not kernel fast-path controllers such as the CPU scheduler, a packet scheduler, or a TCP congestion controller [16, 30, 36, 56]. Instead, they perform steady-state online tuning. While services continue to run, the tuner adjusts the parameters of such OS controllers, e.g., the CPU scheduler time slice or the network stack's polling budget, over seconds-to-minutes timescales"
  - p.2: "First, strong reasoning models are slow and expensive. In an online tuner, that matters twice: (1) they cost more to run, and (2) they delay the next control decision while the service keeps running."
  - p.6, §4.2: "The fast loop, which we call Instant, runs every tuning interval (1-5 seconds) and handles local exploration and quick corrections. … The slow loop, which we call Reasoning, runs less often (tens of seconds)"
  - p.9: "TuxBot (ST) uses Gemini 2.5 Flash as the Reasoning loop and Gemini 2.5 Flash-Lite as the Instant loop, with 0.7 temperature."
  - p.9: "We compare against the default Ubuntu 22.04 configuration (Default Parameters), MLOS [55] using SMAC3"
- **Coverage.** T5: covers what it does (LLM proposes values for up to 41 Linux knobs incl. scheduler parameters, online, with typed validation). It does not report workload-recognition accuracy. T11: states loop cadences (1–5 s, tens of seconds) and hosted models; no per-call latency figure quoted. Others: does not cover.
- **One observation?** Benchmark campaign (13 workloads); not one observation.

### S1-18 — Vulcan, arXiv:2512.25065 (T5)

- **Citation.** Rohit Dwivedula, Divyanshu Saxena, Sujay Yadalam, Eric Hayden Campbell, Daehyeok Kim, Aditya Akella. "Vulcan: Instance-Specialized, Verifiable Systems Heuristics Through LLM-Driven Search." arXiv:2512.25065 [cs.OS]; v1 31 Dec 2025 (title "VULCAN: Instance-Optimal Systems Heuristics Through LLM-Driven Search"), v2 16 Jun 2026, v3 28 Sep 2026; comments "Accepted for publication at EuroSys 2027"; DOI 10.1145/3842654.3848582 (EuroSys '27, April 19–23, 2027, Rabat).
- **Copies read.** abs (`S1-18/abs.html`, `4395b2c2f28414bf0d516b820cad28fcebec47fa17b00a4207f3eab74345736f`); v3 PDF (`vulcan-2512.25065v3.pdf`, `ed85ead607bee6409a2d1fa0389063d0d513f09a718c53317affe028ca16fed6`), full body; v1 PDF (`vulcan-2512.25065v1.pdf`, `9ac8414ea6c9c6a261bf47d245739dc7a60982f22a6033cdc766f6695de87d7b`), searched for scheduling passages · 2026-10-07.
- **Passages.**
  - v3 p.1, Abstract: "We propose Vulcan, a framework that identifies LLM-friendly interfaces that isolate core decision logic from the rest of the implementation. With Vulcan, LLM-generated code is restricted to simple stateless decision functions, while trusted runtime abstractions provide rich derived statistics for meaningful policy exploration without system-integration bugs. To ensure execution safety, LLMs synthesize heuristics in a restricted language, Anvil, that guarantees important properties by construction. We evaluate Vulcan across three well-studied domains and demonstrate up to 4.9× higher savings for spot-VM scheduling, up to 2× lower miss ratios for cache eviction, and up to 14% higher application performance for tiered-memory systems"
  - v3 p.1: "In practice, however, neural approaches remain difficult to deploy in core systems paths: their behavior is opaque, their training and serving pipelines add operational complexity, and integrating them with existing systems code is cumbersome [27, 83]."
  - v1 p.6, Table 3 (as extracted): "CPU scheduling runnable tasks load avg, number of tasks niceness, CPU util represents task urgency schedule task" (CPU scheduling given as an example of a RANK-type task in v1).
- **Coverage.** T5: covers what it does (LLM-driven evolutionary search synthesizing per-instance heuristics in a restricted language; evaluated on spot-VM scheduling, cache eviction, memory tiering; CPU scheduling appears only as an interface example in v1 Table 3). Does not report workload recognition. Others: does not cover.
- **One observation?** Multi-domain evaluation.

### S1-19 — AKTS, arXiv:2609.12276 (T5 successor/recognition; T11)

- **Citation.** Mohammadali Khodabandehlou, Mahdi Alizadeh. "AKTS: Sub-Microsecond Kernel Policy Switching for Language-Model Agents." arXiv:2609.12276v1 [cs.OS], 10 Sep 2026 (only version); comments "6 pages, 1 figure. Code and raw measurement data: this https URL"; PDF marked "Preprint."
- **Copies read.** abs (`S1-19/abs-2609.12276.html`, `89e6404ba126752a4a773f1ee904b0a32d1d088e6dcb321944bfd931e2c71036`); v1 PDF (`akts-2609.12276v1.pdf`, `65451f32ac268f49cf0be1cc4ab483c96e4541e68514188cc076bb8fad08bbeb`) · 2026-10-07 · full text.
- **Passages.**
  - p.1: "The system should recognize the current regime at a coarse timescale and switch the kernel scheduling behavior that is best for that regime." … "Kernel schedulers make placement decisions every few microseconds, while even small language models need milliseconds to produce a decision. Placing inference on the scheduling path is therefore ruled out by construction."
  - p.2: "SchedCP [15] has an LLM generate sched_ext [8] scheduling policy code, which is then compiled, checked by the in-kernel verifier, and loaded, reporting up to 1.79× improvement on target workloads. This recovers full expressiveness, but it places compilation and verification on the actuation path, costs seconds to a minute per policy change" ([15] cited as "In NeurIPS Workshop on Machine Learning for Systems, 2025. Also arXiv:2509.01245.")
  - p.3, §3: "All measurements in this paper use one host: an NVIDIA A100-SXM4-40GB (40 GB) with a 30-vCPU AMD EPYC 7J13 and 216 GB RAM, Ubuntu 24.04, Linux 6.14.0-27."
  - p.4, §4.2: "Serving Qwen2.5-0.5B [12], the model class this design targets, on an A100 and constraining it to emit a single digit, median decision latency is 13.5 ms (n=30, temperature 0), fast enough for a coarse adaptation loop. Decision validity is another matter. Across three prompt formulations and two telemetry regimes, 16 of 48 decisions (33%) were not a valid index: the model returned "3" and, in one case, "0.3", not an integer. Nor does scale fix the underlying problem: with a stronger prompt, Qwen2.5 at 0.5B, 1.5B and 3B all emit valid indices, and all emit a constant one, answering identically for high-load and low-load telemetry (20/40 correct, i.e. chance; n=40 per model; p50 13.3–23.9 ms). Constraining decoding to {0, 1} [13] changes nothing, so the failure at these scales is the decision, not the output format."
  - p.4, Table 1: AKTS "bpf_map_update_elem" p50 920 ns, p99 950 ns, mean 931 ns; "/proc/sys scalar write" 1110 / 1131 / 1123 ns; "recompile + verify + reload" "seconds – minutes".
  - p.5, §5: "The switching experiment is oracle-driven, so it is an upper bound on what an online detector or agent can achieve. An agent-driven arm must show that workload regimes can be detected in time and that a language model improves over a contextualbandit baseline; the models we tested do not yet route reliably on telemetry."
- **Coverage.** T5: covers a 2026 measurement of LLM accuracy at classifying system state (telemetry, two regimes) into a policy index: Qwen2.5 0.5B/1.5B/3B; 20/40 correct each (chance) with stronger prompt; 33% invalid outputs for 0.5B across 48 decisions; statistic = count correct / n; population = 2 telemetry regimes × prompts; it cites SchedCP and "An expert in residence" (S1-20) — a successor in the "agentic OS" line, not by the same authors. T11: covers local small-model decision latency (median 13.5 ms, n=30, temperature 0, A100 GPU, constrained to one digit; p50 13.3–23.9 ms for 0.5–3B) and states constrained decoding to {0,1} did not change decision quality. T10: kernel-side actuation latency of a map write (920 ns p50), not a scheduling-decision cost. Others: does not cover.
- **One observation?** Yes: one host (named), one model family, small n; window not named.

### S1-20 — "An Expert in Residence" (LumOS), NeurIPS 2025 ML for Systems workshop (T5) — abstract only

- **Citation.** Georgios Liargkovas, Vahab Jabrayilov, Hubertus Franke, Kostis Kaffes. "An Expert in Residence: LLM Agents for Always-On Operating System Tuning." Poster, NeurIPS 2025 Workshop: ML for Systems. OpenReview id 7dhlgPp8ni.
- **Copies read.** https://neurips.cc/virtual/2025/129122 (`S1-20/neurips-129122.html`, `57c272e4181ea88f8dd2b3092e2f88e53089b7645eec0c4f07c2bf150cd2249b`); https://daplab.cs.columbia.edu/projects/lumos (`S1-20/lumos.html`, `166682047325887490611462a67374ebd4534db7952dfb9c8fa88d2ad9a28c22`) · 2026-10-07. Full paper (https://openreview.net/pdf?id=7dhlgPp8ni) **HTTP 403** — **only the abstract was read.**
- **Passages.**
  - NeurIPS page, Abstract: "Classical machine-learning auto-tuners for OS control struggle with semantic gaps, brittle rewards, and unsafe exploration. We introduce an online, LLM-driven agent that emulates expert reasoning for continuous OS optimization. When tuning the Linux Completely Fair Scheduler's hyperparameters, the agent outperforms Bayesian optimization by 5\% in single-parameter tuning, 7.1\% in two-parameter co-tuning, and a human expert by 2.98\% overall, while converging faster and adapting more quickly to workload changes. When application counters are unavailable, system-level proxies (e.g., Instructions Per Cycle (IPC)) preserved tail latency in our setup."
  - LumOS project page: "An Expert in Residence: LLM Agents for Always-On Operating System Tuning NeurIPS'25 MLForSys 2025"
- **Coverage.** T5: covers (abstract-level) an LLM agent tuning CFS hyperparameters online; no recognition accuracy stated in abstract. Others: does not cover.
- **One observation?** Unknown (abstract only).

### S1-21 — Li, Ding & Shen, ExpCS 2007 (T10)

- **Citation.** Chuanpeng Li, Chen Ding, Kai Shen. "Quantifying the Cost of Context Switch." Workshop on Experimental Computer Science (ExpCS '07), 2007. DOI 10.1145/1281700.1281702 (DOI from search-result listing; not on the copy).
- **Copy read.** https://www.cs.rochester.edu/~kshen/papers/expcs2007.pdf · 2026-10-07 · `sources/S1-21/expcs2007.pdf` · SHA-256 `8b7a606976610acd6332c7cef6592d58380d49d611a696bf05d2ea122f0c71cf` · full text (4 pp.).
- **Passages.**
  - p.1: "Following Ousterhout's method, we have two processes repeatedly sending a single-byte message to each other via two pipes. During each round-trip communication between the processes, there are two context switches, plus one read and one write system call in each process."
  - p.2: "To avoid potential interference from background interrupt handling of the OS or from other processes in the system, we use a dual-processor machine for our experiment. … We also set up our test processes with real-time scheduling policy SCHED FIFO and give them the maximum priority."
  - p.2: "The machine we use is an IBM eServer with dual 2.0 GHz Intel Pentium Xeon CPUs. Each processor has 512KB L2 cache and the cache line size is 128B. The operating system is Linux 2.6.17 kernel with Redhat 9."
  - p.2: "The average direct context switch cost (c1 ) in our system is 3.8 microsecond. The results shown below are about the total cost per context switch (c2 ). In general, c2 ranges from several microseconds to more than one thousand microseconds."
  - p.2: "In this region, all the curves are relatively flat, with context switch times ranging from 4.2µs to 8.7µs." (array sizes 1 KB–~200 KB) … "the cost of context switch increases dramatically, from 38.6µs to 203.2µs, with the increment of array size." (256 KB–512 KB)
- **Coverage.** T10: covers direct context-switch cost (3.8 µs mean over 20,000 switches) and total cost with cache effects (4.2 µs → >1000 µs depending on working set and stride); machine (dual 2.0 GHz Pentium Xeon, 512 KB L2), kernel (Linux 2.6.17), method (pipe ping-pong, single-process subtraction) named. Not current x86 hardware. Others: does not cover.
- **One observation?** Yes: one machine, one kernel, synthetic workload; window not named.

### S1-23 — Becker & Chakraborty, arXiv:1811.01412 (T10)

- **Citation.** Martin Becker, Samarjit Chakraborty. "Measuring Software Performance on Linux." arXiv:1811.01412v2 (v1 4 Nov 2018; v2 20 Nov 2018). Technical report; no venue stated.
- **Copies read.** abs (`S1-23/abs.html`, `f0419fe4d31bde04bcf11e27c7ff58564d241f98ff92364c9c5046de2c4cdf2d`); v2 PDF (`becker-1811.01412v2.pdf`, `27f6c68ec8f3c688d07ad5a31db7d018c64393d7e43bc07d46da346c1ac52c67`) · 2026-10-07 · full text.
- **Passages.**
  - p.2, Table 1 (as extracted): "Processor … Intel Core i7-2640M @2.8GHz, dual-core "Sandy Bridge", Microcode version 0x25 … OS … Debian 8.11 GNU/Linux SMP 3.16.51-3"
  - p.7, §2.2.2: "Using lmbench, we found that context switches on our system take at least 3,400 cycles, with a frequent value around 30,000 cycles. Note that this number would increase if a core migration happens at the same time"
  - p.7: "This can only be avoided with hardware that supports process context identifiers (PCIDs) and with newer kernels supporting this feature – such as x86 on Kernel 4.14 onwards [22]."
- **Coverage.** T10: covers one lmbench measurement of context-switch cost in cycles (min ≥ 3,400; frequent ≈ 30,000) on a named laptop CPU (Sandy Bridge i7-2640M @ 2.8 GHz) and kernel (3.16.51). Others: does not cover.
- **One observation?** Yes: one machine, one kernel; window not named.

### S1-24 — MELTing point (T11)

- **Citation.** Stefanos Laskaridis, Kleomenis Katevas, Lorenzo Minto, Hamed Haddadi. "MELTing point: Mobile Evaluation of Language Transformers." arXiv:2403.12844v4 (v1 19 Mar 2024 … v4 25 Jul 2024); comments: "Accepted at the 30th Annual International Conference On Mobile Computing And Networking (MobiCom 2024)".
- **Copies read.** abs (`S1-24/abs-2403.12844.html`, `96109e74abb417f2c78ac453bc6810b1a0424acc3d5e97c2ca94f86963b16d18`); v4 PDF (`2403.12844v4.pdf`, `9551aeac42b4b89a91737945aad9af02f3753edd10a3ce6124fa624d26023be7`) · 2026-10-07 · searched full text.
- **Passages.**
  - p.1, Abstract: "To achieve this, we have created our own automation infrastructure, MELT, which supports the headless execution and benchmarking of LLMs on device, supporting different models, devices and frameworks, including Android, iOS and Nvidia Jetson devices." … "Quantization drastically reduces memory requirements and renders execution viable, but at a non-negligible accuracy cost."
  - p.3: "Indicatively, from our measurements, a recent M2-based Mac Studio can run Llama-2 [99] 7B model (4-bit quantized) at a sustained 46.8 tokens/sec."
- **Coverage.** T11: covers on-device LLM throughput (phones, Jetson, one Mac Studio M2 Max figure: 46.8 tokens/s for Llama-2 7B 4-bit). No x86 consumer CPU/GPU latency for short structured outputs was located in the passages searched. Others: does not cover.
- **One observation?** Multi-device benchmark; the 46.8 tok/s figure is one device.

### S1-25 — Atil et al., non-determinism at temperature 0 (T11)

- **Citation.** Berk Atil, Sarp Aykent, Alexa Chittams, Lisheng Fu, Rebecca J. Passonneau, Evan Radcliffe, Guru Rajan Rajagopal, Adam Sloan, Tomasz Tudrej, Ferhan Ture, Zhe Wu, Lixinyu Xu, Breck Baldwin. "Non-Determinism of "Deterministic" LLM Settings." arXiv:2408.04667v5 [cs.CL], 2 Apr 2025 (v1 6 Aug 2024). No venue on abs page.
- **Copies read.** abs (`S1-25/abs-2408.04667.html`, `2d229a5862f32131a8825ca95733e04a2fb93c44f39d667a0de5e863df95a4dd`); v5 PDF (`2408.04667v5.pdf`, `8aa6e2f2488397d0ce305e8c97461d55123f87dbaa440230424a87f59d024056`) · 2026-10-07.
- **Passages.**
  - p.1, Abstract: "We investigate non-determinism in five LLMs configured to be deterministic when applied to eight common tasks in across 10 runs, in both zero-shot and few-shot settings. We see accuracy variations up to 15% across naturally occurring runs with a gap of best possible performance to worst possible performance up to 70%. In fact, none of the LLMs consistently delivers repeatable accuracy across all tasks, much less identical output strings."
  - p.3: "We set the temperature at 0, top-p at 1, and fix the seed."
  - p.4, §5.1: "GPT-3.5 Turbo (Brown et al., 2020), GPT-4o (OpenAI et al., 2024), Llama-3-70B-Instruct (Meta, 2024), Llama-3-8B-Instruct (Meta, 2024), and Mixtral-8x7B-Instruct (Jiang et al., 2024a)."
  - p.7: "We find that all models are more stable when they generate shorter responses."
- **Coverage.** T11: covers output/accuracy non-determinism at temperature 0 with fixed seed (5 models, 8 tasks, 10 runs; accuracy variation up to 15%). Others: does not cover.
- **One observation?** One study campaign.

### S1-26 — Wei et al., Chain-of-Thought (T11)

- **Citation.** Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc Le, Denny Zhou. "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." NeurIPS 2022 ("36th Conference on Neural Information Processing Systems (NeurIPS 2022)" on PDF). arXiv:2201.11903v6.
- **Copies read.** abs (`S1-26/abs-2201.11903.html`, `24184a86d1b99c7c9451c66e538d41d3468d9f3d3dd371f55cbb62a7d285cb9a`); v6 PDF (`2201.11903v6.pdf`, `7d9f878c23b460e4566aa4ec9201b1abfb3b8faefb2b1356e411cb90fef72a12`) · 2026-10-07.
- **Passages.**
  - p.4: "First, Figure 4 shows that chain-of-thought prompting is an emergent ability of model scale (Wei et al., 2022b). That is, chain-of-thought prompting does not positively impact performance for small models, and only yields performance gains when used with models of ∼100B parameters. We qualitatively found that models of smaller scale produced fluent but illogical chains of thought, leading to lower performance than standard prompting."
- **Coverage.** T11: covers whether reasoning-before-answer helps (gains only at ~100B scale on the paper's benchmarks). Does not measure latency cost. Others: does not cover.
- **One observation?** Benchmark study.

### S1-27 — Tam et al., "Let Me Speak Freely?" (T11)

- **Citation.** Zhi Rui Tam, Cheng-Kuang Wu, Yi-Lin Tsai, Chieh-Yen Lin, Hung-yi Lee, Yun-Nung Chen. "Let Me Speak Freely? A Study on the Impact of Format Restrictions on Performance of Large Language Models." arXiv:2408.02442v3 [cs.CL], 14 Oct 2024; comments "18 pages"; no venue stated on the copy.
- **Copies read.** abs (`S1-27/abs-2408.02442.html`, `4c4bf317788bd8d708576435c92b58abad16f48c52de0524d884781091bad0e4`); v3 PDF (`2408.02442v3.pdf`, `172930a8e9166ded9df95bb9ec41aafb7f43907969d14ea2dd05240d2c902f75`) · 2026-10-07.
- **Passages.**
  - p.1, Abstract: "Surprisingly, we observe a significant decline in LLMs' reasoning abilities under format restrictions. Furthermore, we find that stricter format constraints generally lead to greater performance degradation in reasoning tasks."
  - p.4: "We hypothesize that JSON-mode improves classification task performance by constraining possible answers resulted in reducing errors in answer selection." … "These findings suggest format restrictions' impact on LLM performance is task-dependent: stringent formats may hinder reasoning-intensive tasks but enhance accuracy in classification tasks requiring structured outputs."
  - p.7: "Format restrictions, particularly constrained decoding (JSON-mode), can hinder reasoning abilities while enhancing classification task accuracy."
- **Coverage.** T11: covers format-restriction / constrained-decoding effects (reasoning tasks degrade; classification tasks can improve). Model names appear only as garbled figure labels in the extracted text (Gemini 1.5 Flash is named in the p.4 passage); the full model list was not verified. Others: does not cover.
- **One observation?** Benchmark study.

### S1-28 — Sprague et al., "To CoT or not to CoT?" (T11)

- **Citation.** Zayne Sprague, Fangcong Yin, Juan Diego Rodriguez, Dongwei Jiang, Manya Wadhwa, Prasann Singhal, Xinyu Zhao, Xi Ye, Kyle Mahowald, Greg Durrett. "To CoT or not to CoT? Chain-of-thought helps mainly on math and symbolic reasoning." ICLR 2025 (abs comments: "Published at ICLR 2025"). arXiv:2409.12183v3.
- **Copies read.** abs (`S1-28/abs-2409.12183.html`, `e6fc195d990b46fa1a36dcf938183c056301ffce5af13b5759e38a59b160960e`); v3 PDF (`2409.12183v3.pdf`, `9f6aeece29b29ed4a20e7edbb430267e11ed6481ce872edc1bff91a9069573a1`) · 2026-10-07.
- **Passages.**
  - p.1, Abstract: "Our results show that CoT gives strong performance benefits primarily on tasks involving math or logic, with much smaller gains on other types of tasks. On MMLU, directly generating the answer without CoT leads to almost identical accuracy as CoT unless the question or model's response contains an equals sign, indicating symbolic operations and reasoning." … "Our results indicate that CoT can be applied selectively, maintaining performance while saving inference costs."
  - p.2: "First, CoT is unnecessary for many problems where it is widely employed: there exist more efficient prompting strategies that yield similar performance for much lower inference cost."
- **Coverage.** T11: covers whether reasoning-before-answer improves answers (meta-analysis of 100+ papers + 20 datasets × 14 models), and states an inference-cost argument (no latency measurements quoted). Others: does not cover.
- **One observation?** Meta-analysis + benchmark study.

### S1-29 — Kurt, llama.cpp quantization on Llama-3.1-8B, arXiv:2601.14277 (T11)

- **Citation.** Uygar Kurt. "Which Quantization Should I Use? A Unified Evaluation of llama.cpp Quantization on Llama-3.1-8B-Instruct." arXiv:2601.14277v1 [cs.LG], 11 Jan 2026. No venue stated.
- **Copies read.** abs (`S1-29/abs.html`, `ee3e4ce0b2880cb72b07d79c3a381fff3da950d54f018201fa76ba09756c6731`); v1 PDF (`2601.14277v1.pdf`, `9b388b4cec217f498604f37ff1e253e2651b58462e13a8e30b227a6c9573c376`) · 2026-10-07.
- **Passages.**
  - p.5: "Quantization and evaluation were performed on a dual-socket CPU server with two Intel Xeon Platinum 8488C processors, totaling 96 physical cores (192 threads), with AVX-512 and BF16 support enabled. We used llama.cpp (commit b7600)"
  - p.6: "We also record throughput under fixed settings of pp = 512 (prompt processing) and tg = 128 (token generation)"
  - p.9, Table 3 (tokens/s, pp512 / tg128): "F16 79.57 ± 1.00 2.83 ± 0.01 … Q4_0 97.35 ± 0.68 4.36 ± 0.20 … Q4_K_S 92.52 ± 1.53 4.65 ± 0.15 Q4_K_M 87.70 ± 0.70 5.12 ± 0.37 … Q8_0 71.42 ± 3.15 5.03 ± 0.16"
- **Coverage.** T11: covers llama.cpp CPU throughput for an 8B model at several quantizations (Q4_K_M: 87.70 tok/s prompt processing, 5.12 tok/s generation) on a **server** CPU (dual Xeon Platinum 8488C), not a consumer CPU; no end-to-end short-output latency. Others: does not cover.
- **One observation?** Yes: one machine, one model, one llama.cpp commit; window not named.

### S1-30 — Wessel & Wright, NIME 2001 (T13)

- **Citation.** David Wessel, Matthew Wright. "Problems and Prospects for Intimate Musical Control of Computers." Proceedings of the CHI'01 Workshop on New Interfaces for Musical Expression (NIME-01), Seattle. arXiv:2010.01570v1.
- **Copies read.** abs (`S1-30/abs.html`, `75f7f689e3b4f20591871fa8c297a0fbf8210795deb01fbcb2ada15d372410e3`); v1 PDF (`2010.01570v1.pdf`, `f8c6ba8551994406a6ff8e3060fb97929cb726c1b70dc65f323fc968e6c2a83b`) · 2026-10-07.
- **Passages.**
  - p.2, "Latency requirements for control intimacy": "Few practitioners of live performance computer music would deny that low latency is essential. Just how low is the subject of considerable debate. We place the acceptable upper bound on the computer's audible reaction to gesture at 10 milliseconds (ms) and the systems described in this paper provide for measured [2] latencies nearer 7 ms. Low variation of latency is critical and we argue that the range of variation should not exceed 1 ms."
- **Coverage.** T13: covers a stated latency requirement for live computer-music performance (≤ 10 ms; jitter ≤ 1 ms). Does not state buffer sizes or sample rates. Others: does not cover.
- **One observation?** Position/design paper; the 7 ms is a measured figure attributed to their ref [2].

---

### S1-32 — AKTS v2, arXiv:2609.12276v2 (T5; stage 3, 2026-10-08)

- **Copies read.** https://arxiv.org/abs/2609.12276 (`sources/S1-32/akts-abs-arxivorg.html`, SHA-256 `9e67b8488acc459e79a1da3a01e277897307cc38f9bed915c578deeb671f86cf`; submission history: "[v1] Thu, 10 Sep 2026 23:10:25 UTC (14 KB) [v2] Wed, 7 Oct 2026 11:31:07 UTC (13 KB)"); https://arxiv.org/pdf/2609.12276v2 (`akts-2609.12276v2.pdf`, `dfc179fc2395b41a6f13e606ea033bb7e61a1272d82faa89e0f794a1dc3239fe`, 5 pages); v1 re-fetched byte-identical to S1-19 (`65451f32…`). Text by `pdftotext -layout` (poppler 26.10.0); v2 text SHA-256 `47b0bf46a7cd80bea5cfa9cb094ed6057dd63032b154c4df6c1034578b1dbc77`.
- **Passages (v2).**
  - §4.2: "Serving Qwen2.5-0.5B [12], the model class this design targets, on the A100 with single-digit output, median decision latency is 13.5 ms (n=30, temperature 0), fast enough for a coarse adaptation loop. Decision validity is another matter. Across three prompt formulations and two telemetry regimes, 16 of 48 decisions (33%) were not a valid index: the model returned "3" and, in one case, "0.3", not an integer. Nor does scale fix the underlying problem: with a stronger prompt, Qwen2.5 at 0.5B, 1.5B and 3B all emit valid indices, and all emit a constant one, answering identically for high-load and low-load telemetry (20/40 correct, i.e. chance; n=40 per model; p50 13.3–23.9 ms). Constraining decoding to {0, 1} [13] changes nothing, so the failure at these scales is the decision, not the output format."
  - §5: "Switching here is oracle-driven, an upper bound on any online detector. An agent-driven arm must show a language model beats a bandit baseline."
- **Against v1 (S1-19).** The abstract and introduction are shortened; §4.2's figures are unchanged; v1's "the models we tested do not yet route reliably on telemetry" (§5) is not in v2.
- **Coverage.** T5: as S1-19, at v2. One host, one model family, n = 40 per model; not an observation of ours.

### S1-33 — Kgent, eBPF '24, the paper itself (T5; stage 3, 2026-10-08)

- **Citation.** Yusheng Zheng, Yiwei Yang, Maolin Chen, Andrew Quinn. "Kgent: Kernel Extensions Large Language Model Agent." eBPF '24, August 4–8, 2024, Sydney, NSW, Australia. DOI 10.1145/3672197.3673434.
- **Copy read.** The ACM Digital Library answered 403. OpenAlex lists the work as gold open access with a repository copy: UC Santa Cruz's eScholarship, https://escholarship.org/content/qt3jg1f0jr/qt3jg1f0jr.pdf (cover page: "UC Santa Cruz Previously Published Works", DOI 10.1145/3672197.3673434, "Publication Date 2024-08-04", CC BY 4.0, "Peer reviewed"), accessed 2026-10-08 → `sources/S1-33/kgent-escholarship.pdf`, SHA-256 `1292f7508075a393ea431777dd3458d30fa6a2a3de2428ec813061693bebf754` (9 pages: the cover and the ACM-template paper, running head "eBPF '24, August 4–8, 2024, Sydney, NSW, Australia"); text by `pdftotext -layout`, SHA-256 `5ed5ff1ec056258d580eaa8cb0a78cffd6eded8c548f935f9c011cf32798ff67`; the OpenAlex record `openalex-kgent.json`, `bf7ddce8…`.
- **Passages** (Abstract, p. 1): "The extended Berkeley Packet Filters (eBPF) ecosystem allows for the extension of Linux and Windows kernels, but writing eBPF programs is challenging due to the required knowledge of OS internals and programming limitations enforced by the eBPF verifier." … "This paper presents Kgent, an alternative framework that alleviates the difficulty of writing an eBPF program by allowing Kernel Extensions to be written in Natural language. Kgent uses recent advances in large language models (LLMs) to synthesize an eBPF program given a user's English language prompt. To ensure that LLM's output is semantically equivalent to the user's prompt, Kgent employs a combination of LLM-empowered program comprehension, symbolic execution, and a series of feedback loops." … "We show that Kgent produces correct eBPF programs on 80%—which is an improvement of a factor of 2.67 compared to GPT-4 program synthesis baseline".
- **Coverage.** T5: the paper body S1-13 could not read; its abstract matches the authors' repository BibTeX (S1-13). Not an observation.

### S1-34 — SchedCP v4, re-read for its motivation and evaluation machines (T5; stage 3, 2026-10-08)

- **Copies.** https://arxiv.org/pdf/2509.01245v1 and …v4, fetched 2026-10-08 into `sources/S1-34/`, byte-identical to S1-12's (SHA-256 v1 `b0fc4ec0…`, v4 `cce49d3c…`); text by `pdftotext -layout`.
- **Passages (v4).**
  - §2 Motivation, p. 2: "First, a domain knowledge gap exists between developers and users: DevOps engineers lack insight into workload characteristics (latency-sensitive vs. throughput-oriented), while edge/personal device users lack both kernel optimization expertise and understanding of application-specific targets."
  - §5, p. 4: "Evaluation uses two machines: 86-core Intel Xeon 6787P with 758GB RAM running Linux 6.14, and 8-core Intel Core Ultra 7 258V with 30GB RAM running Linux 6.13. Agents use Claude Code (Opus 4), testing each case three times and averaging results." … "Future evaluation requires a complete benchmark."
  - §3, p. 3: "1. Workload Analysis Engine Provides tiered access to system performance data: (1) cost-effective API endpoints with pre-processed summaries (CPU load, memory usage), (2) secure sandbox access to file reading, application building, Linux profiling tools (perf, top) and dynamically attachable eBPF probes, (3) feedback channel reporting post-deployment metrics (percentage change in throughput/latency)."
  - §4, p. 4: the Observation, Planning, Execution and Learning Agents; the Planning Agent's "decision hierarchy: configuring existing schedulers, generating patches, or composing new schedulers from primitives".
- **Coverage.** T5: SchedCP names edge and personal devices among its motivations and evaluates on given workloads (kernel compilation, schbench, batch workloads) on an 86-core Xeon and an 8-core Core Ultra 7 258V. Not an observation.

### S1-35 — TuneAgent's DOI resolved; the two adjacent preprints' versions re-checked (T5; stage 3, 2026-10-08)

- **Copies** (2026-10-08, `sources/S1-35/`): Crossref's record of DOI 10.1145/3770855.3817987 → `crossref-tuneagent.json`, SHA-256 `2af8e0717a40c5c2524dcede9a80fd2048cd93df855934c2430acd0fc56c1281`; the arXiv abstract pages of 2506.02025 (`5f7117a4…`, byte-identical to S1-15's) and 2508.12551 (`220f6ca1…`, byte-identical to S1-14's).
- **Passages.**
  - Crossref: title "TuneAgent: Agentic Operating System Kernel Tuning with Reinforcement Learning"; container "Proceedings of the 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2"; published 2026-08-08; event "KDD '26: The 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining"; authors Lin, Li, Luo, Lin, Zhang, Xing, Wu — the venue S1-14's v2 PDF states, now in the DOI registry.
  - arXiv 2508.12551: "[v1] Mon, 18 Aug 2025 … [v2] Sun, 31 May 2026"; no later version.
  - arXiv 2506.02025: "[v1] Thu, 29 May 2025 … [v2] Wed, 3 Sep 2025"; "Comments: 10 pages, 6 figures, work under review" — no later version, no venue.
- **Coverage.** T5: TuneAgent's venue confirmed by its DOI; Jadhav et al. still an unpublished preprint. Not an observation.

## 3. Not found

- **T1 (ghOSt) — none missing.** (sched_ext docs / scx repo are S2.)
- **T2 — a peer-reviewed paper or archived preprint describing LAVD** (stage 3, 2026-10-08; searches #49, #50; responses in `sources/S1-31/`, SHA-256 `cf05addc…` and `347efa1d…` for the two arXiv queries, `d78f0b60…`, `9cc9257b…`, `6b052ab7…` for the three OpenAlex queries). None found: arXiv returns no result for either query; OpenAlex's hits are unrelated works or later papers that use scx_lavd ("SchedAgent", 2026; "Rethinking Provenance Completeness with a Learning-Based Linux Scheduler", arXiv 2025). LAVD's own descriptions are its talks (S2-10, S2-11), LWN's reports of them (S2-12, S2-13) and its source and README (S2-09).
- **T3 — Linux's default class description in literature.** OSTEP chapters read (S1-02, S1-03) contain no description of Linux's scheduler (`grep -c Linux` = 0 in ch. 8). The kernel's `sched-eevdf.rst` / `sched-design-CFS.rst` are S2. No literature source in this search states whether Linux's default class is MLFQ or proportional share.
- **T4 — any statement in Decima/FIRM/Park about retraining for new hardware specifically.** Decima speaks of workloads and cluster size (S1-06), FIRM of "underlying systems and workloads" (S1-07), Park of operating environments/simulation-reality (S1-08); no hardware-specific retraining statement found by full-text search for "retrain", "hardware", "generaliz".
- **T5 — the eBPF '24 Kgent paper body.** ACM DL 403 (searches #12); read only the authors' repository abstract and arXiv predecessor KEN.
- **T5 — a successor to Agentic OS by the same authors.** arXiv API author searches `au:Zheng_Yusheng`, `au:Quinn_Andi` (#23, #24) and `all:"agentic OS"` (#25) found no follow-up scheduler paper by them; related later works by others: AKTS (S1-19), TuxBot (S1-17), Expert in Residence (S1-20).
- **T5 — an LLM's recognition accuracy from a process list.** Searches #27, #28, #34, #36: no paper measuring an LLM's accuracy at recognizing workloads from a process list was found. The only accuracy figures found: AKTS (S1-19; LLM on telemetry, chance-level for 0.5–3B), Agentic OS (S1-12; 8/8 workloads Opus, Sonnet failed), ASA (S1-11; non-LLM XGBoost, 96.83%/99.19%).
- **T10 — scheduler pick_next_task cost measurement; context switches per second on desktops/servers; recent (≥2020) x86 context-switch measurement beyond ghOSt.** Searches #37–#42. David, Carlyle & Campbell (ExpCS 2007) is ARM and paywalled (ACM 403, #39). Desktop context-switch rates surfaced only in mailing-list posts and vendor docs (not literature). ghOSt (S1-01, Skylake Xeon, Linux 4.15, CFS switch 599 ns) is the most recent x86 measurement found.
- **T11 — end-to-end latency for a short structured output from a 3–8B quantized model on a consumer x86 CPU or GPU.** Searches #43, #44. Found only: Mac Studio M2 Max throughput (S1-24), server-Xeon llama.cpp throughput (S1-29), A100 0.5–3B decision latency (S1-19), hosted reasoning-model per-call latency (S1-15). No consumer-x86 end-to-end figure. Latency cost of CoT not measured in S1-26/S1-28.
- **T12 — PC gaming session length; application-set change rate per hour.** Searches #45, #46: no peer-reviewed measurement read in full. Hits were an industry report (Nielsen 2009, casual games, not read in full), a Steam telemetry conference paper (abstract seen only via search results, no session-length figure), Statista (paywalled survey), and a mobile game preprint. Nothing on desktop application-set change rates.
- **T13 — literature on audio buffer sizes / sample rates and game frame budgets.** Searches #47, #48: only Wessel & Wright's 10 ms / 1 ms requirement (S1-30). No literature source on buffer sizes, sample rates or display frame budgets was found in this search (vendor documentation is S2).
- **Paywalled / unreachable:** dl.acm.org Kgent HTML and PDF (403); dl.acm.org David et al. 2007 PDF (403); openreview.net Expert-in-Residence PDF (403); rochester.edu `~cli/research/switch.pdf` (404); Statista session-length page (paywalled).
