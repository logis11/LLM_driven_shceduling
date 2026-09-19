# S1 — peer-reviewed and preprint literature (T1, T2, T3, T6)

Reader: S1. Date of all searches and fetches: 2026-09-19 (UTC times in the copy identification). Read only `search/input.md` and this class's output folder.

Conventions. Every source was fetched with `curl -sS -L` through the session proxy (TLS verified against `/root/.ccr/ca-bundle.crt`) except where a row says WebFetch or WebSearch; WebSearch was used only to locate open copies, never as a source. PDF text was extracted with PyMuPDF 1.28.2 (`pymupdf`, pip-installed; `pypdf` failed to import: cryptography `_cffi_backend` missing). "PDF page" is the page index in the fetched file (cover pages counted); where a venue's own page number is known it is given too. Passages are verbatim from the extracted text; hyphenation at line ends is joined and PDF ligatures (ﬁ, ﬂ) written as plain letters; nothing else is changed. HTML pages (LWN, ACM Queue archive) are quoted from the article body and located by the article's section heading. SHA-256 is of the file as saved under `sources/S1-NN/` (gitignored). A "Linux observation" below is one measured on Linux with machine, program version, state and window named; everything else is context, marked.

## 1. Search log

| # | Engine / venue | Exact query or URL | Hits followed | Dead ends (HTTP status) |
|---|---|---|---|---|
| 1 | arXiv API `export.arxiv.org/api/query` | `search_query=all:"site isolation" AND all:browser` | 0 entries | — |
| 2 | arXiv API | `all:chromium AND all:renderer AND all:process` | — | 429 (rate-limited; not retried after batch) |
| 3 | arXiv API | `all:"background tabs"` | 0 entries | — |
| 4 | arXiv API | `all:electron AND all:"desktop application" AND all:energy` | 0 entries | — |
| 5 | arXiv API | `all:"web browser" AND all:"energy consumption" AND all:linux` | 2 entries: 1710.03559 (mobile, title only), 1906.03018 (off-topic) | — |
| 6 | arXiv API | `all:"video conferencing" AND all:zoom AND all:measurement` | 8 entries; followed 2105.13478 (S1-04), 2210.09651 (S1-05), 2107.00904 (S1-06) | — |
| 7 | arXiv API | `all:discord AND all:websocket` | 0 | — |
| 8 | arXiv API | `all:matrix AND all:synapse AND all:federation` | 0 | — |
| 9 | arXiv API | `all:sched_ext` | 4 entries; followed 2511.11628 (S1-13); 2511.08297, 2605.02377, 2602.09345 off-topic by title/abstract | — |
| 10 | arXiv API | `all:"linux scheduler" AND all:interactive AND all:latency` | 0 | — |
| 11 | arXiv API | `all:steam AND all:proton AND all:linux AND all:gaming` | 0 | — |
| 12 | USENIX direct | `https://www.usenix.org/system/files/sec19-reis.pdf` | S1-01 | — |
| 13 | Google Research archive | `https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/34924.pdf` | S1-02 | — |
| 14 | Stanford seclab | `https://seclab.stanford.edu/websec/chromium/chromium-security-architecture.pdf` | S1-03 | — |
| 15 | OpenAlex API `api.openalex.org/works?search=` | `chromium renderer process idle tab energy` | 55 results, top 12 unrelated (relevance ranking useless) | — |
| 16 | OpenAlex API | `background tab throttling browser`; `electron framework desktop application energy consumption`; `web browser energy consumption linux desktop`; `matrix protocol element client measurement`; `microsoft teams zoom client cpu measurement`; `steam client linux proton performance`; `sched_ext linux scheduler bpf`; `linux desktop scheduler interactivity browser workload`; `EEVDF scheduler linux latency`; `chromium site isolation process overhead`; `multi-process browser architecture memory cpu overhead`; `tab discarding browser memory pressure` | — | 429 on all twelve (2 s spacing; not retried — arXiv and WebSearch covered the same ground) |
| 17 | OpenAlex API | `discord client traffic characterization` | 329 results; top 12 generic traffic-classification papers, none on the Discord client | — |
| 18 | OpenAlex API | `slack client measurement websocket` | 77 results, none relevant | — |
| 19 | OpenAlex API | `websocket keep-alive heartbeat energy interval` | 13 results, none relevant (IoT, EV charging) | — |
| 20 | Semantic Scholar `api.semanticscholar.org/graph/v1/paper/search` | `Electron desktop application energy CPU`; `Chromium renderer process idle tab wakeup`; `Discord desktop client measurement`; `Matrix messaging protocol Synapse performance`; `Zoom client CPU measurement Linux`; `Steam client Linux Proton game performance overhead`; `sched_ext BPF scheduler Linux`; `Linux scheduler desktop interactivity web browser background workload` | — | 429 on every query, 4 attempts each with 8/16/24/32 s backoff |
| 21 | WebSearch | `paper measurement "background tabs" browser CPU energy throttling study` | Varvello TMA 2021 (S1-26), arXiv 2404.06827 (S1-15) | researchgate.net hit not attempted (403 per access notes); alibaba "lifetips" pages are not sources |
| 22 | WebSearch | `Electron desktop application energy consumption CPU empirical study paper` | Malavolta group QUATIC 2024 PDF (S1-07) | bit-Tech "Tauri vs Electron" (doi 10.32877/bt.v8i3.3733) not fetched: snippet names no OS and no chat client |
| 23 | WebSearch | `sched_ext LAVD scx_lavd gaming latency criticality scheduler talk slides Steam Deck` | LPC 2024 slides (S1-08), LPC 2025 slides (S1-09) | github.com hits not followed (403 per access notes; S2 class anyway) |
| 24 | WebSearch | `lwn.net sched_ext gaming scheduler Steam Deck LAVD` | LWN 1051430 (S1-10), 991205 (S1-11), 974387 (S1-24) | LWN 972075 (patch posting) not followed |
| 25 | WebSearch | `paper measurement Discord OR Slack OR "Microsoft Teams" desktop client CPU usage idle traffic characterization Linux` | none: only support forums, Medium posts, slack.engineering blog (out of class) | — |
| 26 | WebSearch | `Matrix protocol Synapse Element client performance measurement paper sync long polling` | none: matrix.org blog posts and a synapse issue (S2/S3 class) | — |
| 27 | WebSearch | `Linux scheduler evaluation interactive workload browser "many tabs" latency CFS EEVDF paper` | LWN 925371 (S1-12), arXiv 1012.3452 (S1-23), arXiv 2306.15076 (S1-14), arXiv 2511.11628 (S1-13) | Wong et al. 2008 (see row 66) |
| 28 | WebSearch | `arxiv "web browser" "wake-ups" OR "wakeups" idle power Linux Firefox Chrome measurement` | none in class: Mozilla bugzilla 1547526 / 407325 and Phoronix are S3/press | — |
| 29 | WebSearch | `browser energy consumption study "100 tabs" OR "100 concurrent tabs" 15 browsers measurement paper` | Varvello TMA 2021 (S1-26); Energy Wars (S1-17, via row 33) | DiBenedetto & Wedyan, FMEC 2025 (ieeexplore 11119363): IEEE serves a challenge body (access notes), no open copy found |
| 30 | WebSearch | `Zoom Linux client CPU utilization measurement paper Ubuntu "video conferencing" client-side resource usage` | arXiv 2109.13113 (S1-16) | Zoom community / Linux Mint forum threads are S3 class |
| 31 | WebSearch | `Chromium site isolation process count renderer memory overhead measurement study paper "process-per-site-instance"` | arXiv 1702.06764 Loophole (S1-18) | chromium.googlesource process-models doc is S2 class, not followed |
| 32 | WebSearch | `"tab discarding" OR "tab freezing" OR "intensive wake up throttling" Chrome research paper energy measurement` | none in class: developer.chrome.com blog, blink-dev intents (S2) | — |
| 33 | WebSearch | `"Energy wars" "Chrome vs. Firefox" Macedo Abreu Pereira Saraiva pdf repositorium` | open copy `states.github.io/files/p23.pdf` (S1-17) | researchgate 403 |
| 34 | WebSearch | `"An Empirical Evaluation of Energy Consumption Across Web Browsers" 2025 pdf` | none open | ieeexplore (challenge), researchgate (403) |
| 35 | WebSearch | `"Comparative Analysis of Energy Efficiency in Desktop Web Browsers" Towards Sustainable Software Applications pdf` | none open | academia.edu (login wall), researchgate (403) |
| 36 | WebSearch | `paper "Steam" client "steamwebhelper" OR "gameoverlayui" Linux measurement OR trace OR profile` | none in class: steamcommunity threads, Arch forums, ValveSoftware issues (S3) | — |
| 37 | ACM Queue direct | `https://queue.acm.org/detail.cfm?id=1556050` | — | 403 (Cloudflare "Attention Required") |
| 38 | Internet Archive | `https://web.archive.org/web/2023id_/https://queue.acm.org/detail.cfm?id=1556050` | S1-19 | — |
| 39 | arXiv API | `all:tauri AND all:electron` | 15 entries, all astrophysics (T Tauri) | — |
| 40 | arXiv API | `all:matrix AND all:homeserver` | 0 | — |
| 41 | arXiv API | `all:"microsoft teams" AND all:measurement` | 6; only the VC papers already held (S1-04, S1-05) | — |
| 42 | arXiv API | `all:slack AND all:"instant messaging"` | 5, social-science, none relevant | — |
| 43 | arXiv API | `abs:"web browser" AND abs:scheduler AND abs:linux` | 1 (1710.03559, mobile) | — |
| 44 | arXiv API | `abs:interactive AND abs:linux AND abs:scheduler AND abs:desktop` | 0 | — |
| 45 | arXiv API | `abs:"site isolation"` | 4; none relevant (2404.07042 is a CPU side channel) | — |
| 46 | arXiv API | `abs:browser AND abs:energy AND abs:tabs` | 0 | — |
| 47 | arXiv API | `abs:"latency nice" OR abs:EEVDF` | 1 (2511.11628, held) | — |
| 48 | arXiv API | `abs:"Steam Deck"` | 1, off-topic | — |
| 49 | arXiv API | `abs:discord` | 15, all quantum discord | — |
| 50 | arXiv API | `abs:"video conferencing" AND abs:CPU AND abs:client` | 0 | — |
| 51 | arXiv API | `id_list=2101.09359,1012.3452,2404.07042` (abstracts) | 1012.3452 fetched (S1-23); 2101.09359 is embedded/Android load balancing (context by abstract, not fetched); 2404.07042 off-topic | — |
| 52 | arXiv API | `abs:matrix AND abs:federated AND abs:messaging` | 11; followed 1910.06295 (S1-22) | — |
| 53 | arXiv API | `abs:proton AND abs:wine AND abs:games` | 0 | — |
| 54 | arXiv API | `abs:websocket AND abs:"keep-alive"` | 0 | — |
| 55 | arXiv API | `abs:"renderer process"` | 15, all graphics rendering | — |
| 56 | arXiv API | `abs:"background tab" OR abs:"background tabs"` | 0 | — |
| 57 | arXiv API | `abs:electron AND abs:chromium` | 15, all chemistry/physics | — |
| 58 | arXiv API | `abs:"idle power" AND abs:"wake-ups"` | 4, none relevant | — |
| 59 | WebSearch | `"Performance Comparison of Tauri and Electron Frameworks" bit-Tech operating system Linux OR Windows idle CPU` | not fetched: no snippet names the OS; no chat client | — |
| 60 | WebSearch | `Matrix homeserver Synapse Dendrite Conduit performance evaluation thesis OR paper pdf CPU load sync` | none in class (blogs, matrix.org) | — |
| 61 | WebSearch | `scheduler paper evaluation "Chrome" "tabs" background load interactive latency Linux "perf sched" OR "wakeup" desktop responsiveness` | LWN 725238 (S1-20) | Brendan Gregg blog and manpages are not literature |
| 62 | WebSearch | `Discord gateway heartbeat interval websocket paper malware C2 "heartbeat" "41250" OR "41.25"` | none in class (Discord docs, GitHub issues — S2/S3) | — |
| 63 | LWN direct | `https://lwn.net/Articles/418884/` (the 2010 group-scheduling discussion, known title) | S1-21 | — |
| 64 | LWN site search | `https://lwn.net/Search/DoSearch?words=chrome+scheduler+tabs&ctype3=yes&cat_2=yes` | — | 200 but only the search form returned (results need a subscriber login) |
| 65 | WebSearch | `"Steam" Linux Proton Wine game performance evaluation paper pdf overhead "Steam client"` | "Is Proton Good Enough?" (ICCCI 2023, Springer LNCS 978-3-031-41456-5_48) — paywalled | link.springer.com (paywall), dl.acm.org (403 per notes), researchgate (403) |
| 66 | WebSearch | `"Fairness and interactive performance of O(1) and CFS Linux kernel schedulers" pdf Wong Tan` | no open copy | academia.edu (login), researchgate (403), ieeexplore 4631872 (challenge) |
| 67 | WebSearch | `"Electron" apps idle CPU "wake" OR "wakeups" study Linux Slack Discord measurement paper energy "desktop"` | none in class; leads for S3: electron/electron#25021 ("Electron wakes up frequently even when running an app that is at rest"), pixijs/pixijs#11050 | — |
| 68 | LWN direct | `https://lwn.net/Articles/974387/`, `https://lwn.net/Articles/922405/` | S1-24; 922405 read (S1-25), no workload content | — |
| 69 | raw.githubusercontent.com (lead check, out of class) | `https://raw.githubusercontent.com/Igalia/vapormark/main/README.md` | 200; the tool's `scmon -n steam` "log the system call usage of 'steam' and all its decendents"; README names no Steam process. Lead for S2/S3, not a candidate | — |
| 70 | WebSearch | `scx_bpfland Andrea Righi talk slides responsiveness "web browser" OR "browser" OR "gaming" kernel build background interactive workload results` | no slides; only Phoronix, lib.rs, a blog (not literature) | — |
| 71 | WebSearch | `"Microsoft Teams" OR "Discord" client traffic characterization measurement paper keep-alive heartbeat interval idle "desktop client"` | none in class | — |
| 72 | WebSearch | `"Is Proton Good Enough" performance comparison gaming Windows Linux pdf open access` | no open copy | — |
| 73 | WebSearch | `lwn.net "scx_bpfland" OR "bpfland" interactive scheduler article` | 991205 (held), 974387, 922405 | — |
| 74 | IFIP DL direct | `https://dl.ifip.org/db/conf/tma/tma2021/tma2021-paper18.pdf` | S1-26 | — |
| 75 | WebSearch | `Linux scheduler evaluation paper "Firefox" OR "Chromium" foreground interactive workload background "kernel compile" latency measured 2020..2025 arXiv OR USENIX OR EuroSys` | nothing new: arXiv 2509.01245 (Agentic OS; snippet shows no browser workload, not fetched); EuroSys'16 Lozi et al. (dl.acm 403; no browser workload known) | — |
| 76 | WebSearch | `"Chromium" OR "Chrome" "renderer" "timer throttling" OR "throttled" background tab "wake" measurement paper energy Linux OR laptop "Intel" RAPL` | none in class: blink-dev intents, chromium blog M87 (S2 class) | — |

Unreachable or paywalled overall: Semantic Scholar (429 throughout), OpenAlex (429 for 12 of 16 queries), dl.acm.org / ieeexplore / researchgate / academia.edu (403 or challenge or login), queue.acm.org (403; archive copy used), LWN site search (login).

## 2. Candidates

### S1-01 — Reis, Moshchuk, Oskov, "Site Isolation: Process Separation for Web Sites within the Browser", USENIX Security 2019

- Citation: Charles Reis, Alexander Moshchuk, Nasko Oskov (Google). Proceedings of the 28th USENIX Security Symposium, Santa Clara, August 14–16 2019, pp. 1661–1678. ISBN 978-1-939133-06-9.
- Copy read: `https://www.usenix.org/system/files/sec19-reis.pdf`, published version, accessed 2026-09-19T01:47Z, `sources/S1-01/sec19-reis.pdf`, SHA-256 `fc5e13705338c66f219b9aa1385a51a6d9f743fa7e66ef55b48794502e1be6a0`. PDF page 1 is the USENIX cover; PDF page n = paper page 1659+n.
- Passages:
  - §4.1.1 Process Consolidation (PDF p. 8 = paper p. 1667): "Our security model dictates that a renderer process may never contain documents hosted at different sites, but a process may still be shared across separate instances of documents from the same site. Fortunately, many users keep several tabs open, which presents an opportunity for process sharing across those tabs. To reduce the process count, we have implemented a process consolidation policy that looks for an existing same-site process when creating an out-of-process iframe."
  - same section (PDF p. 8): "Instead, we use process consolidation for same-site main frames only after crossing a soft process limit that approximates memory pressure. When the number of processes is below this limit, main frames in independent tabs don't share processes; when above the limit, all new frames start reusing same-site processes when possible. Our threshold is calculated based on performance characteristics of a given machine. Note that Site Isolation cannot support a hard process limit, because the number of sites present in the browser may always exceed it."
  - §4.1.3 (PDF p. 8): "To address this, we maintain a warmed-up spare renderer process, which may be used immediately by a new navigation to any site. When a spare process is locked to a site and used, a new one is created in the background, similar to process pre-creation optimizations in OP2 [23]. To control memory overhead, we avoid spare processes on low memory devices, when the system experiences memory pressure, or when the browser goes over the soft process limit."
  - §5.3.1 Observed Workload (PDF p. 11 = paper p. 1670): "The data in this section was collected using pseudonymous metric reporting over a two-week period starting October 1, 2018, from desktop and laptop users of Chrome (version 69) on Windows who have this reporting enabled."
  - same (PDF p. 11): "Using periodic samples, we found that users had 6.0 unique sites open across the entire browser at the 50th percentile of the distribution, and 41.9 unique sites at the 99th percentile. [...] At the 50th percentile, the number of processes increased 43.5% from 4.4 without Site Isolation to 6.2 with Site Isolation. At the 99th percentile, the process count increased 50.6% from 35.0 to 52.7 processes."
  - same (PDF p. 11): "In reported metrics, we found that private memory use per renderer process decreased 51.5% (87.2 MB to 42.3 MB) at"
  - CPU Usage (PDF pp. 12–13 = paper pp. 1671–1672): "Average CPU usage in the browser process increased 8.2% (32.0% to 34.6%) at the 99th percentile, [...] due to additional IPC messages and coordination across processes. While there were more renderer processes, each renderer's average CPU usage dropped 33.5% (47.7% to 31.8%) at the 99th percentile, since the workload was distributed across more processes."
  - §5.3.2 Microbenchmarks (PDF p. 13): "Our experiments were performed on a Windows 10 desktop with an Intel Core i7-8700K 3.7 GHz 6-core CPU and 16 GB RAM."
- Coverage:
  - T1: covers the process model as mechanism — renderer-per-site, same-site consolidation for iframes, a machine-dependent *soft* process limit above which same-site main frames share a process, a warmed-up spare renderer. Covers renderer-process counts as a statistic (renderer process count per browser, count, 50th/99th percentile, population = Chrome 69 desktop/laptop users on Windows who report metrics, October 2018, two weeks) and per-process CPU (average CPU usage of a renderer process and of the browser process, per cent, 99th percentile, same population). **Windows field data → context, not a Linux observation.** Does not cover an idle renderer's wake cadence or CPU per wake; does not cover Electron/CEF.
  - T2, T3: does not cover. T6: does not cover.
- One observation? Two: a field population (Windows, Chrome 69, Oct 2018) and a microbenchmark (one Windows 10 machine named, Chrome 69.0.3497.100, single tab). Subject and window named; machine named only for the microbenchmark.

### S1-02 — Reis & Gribble, "Isolating Web Programs in Modern Browser Architectures", EuroSys 2009

- Citation: Charles Reis, Steven D. Gribble (University of Washington / Google). Proceedings of EuroSys 2009, Nuremberg, April 1–3 2009, pp. 219–230.
- Copy read: `https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/34924.pdf`, author copy, accessed 2026-09-19T01:47Z, `sources/S1-02/reis-gribble-eurosys09.pdf`, SHA-256 `5f88f5af85a065811eb15a088172bd95539240a01525d3e131c24de58608d060`. PDF page n = paper page 218+n.
- Passages:
  - §3.2, Process-per-Browsing-Instance (PDF p. 7 = paper p. 225): "Chromium's simplest multi-process model creates a separate rendering engine process for each browsing instance. Implementing this model requires mapping each group of connected browser tabs to a rendering engine process. The browser kernel must display the process's output and forward user interactions to it, communicating via IPC."
  - Process-per-Site-Instance (PDF p. 8): "The above process model can be refined to create a separate renderer process for each site instance, providing meaningful fate sharing and isolation for each web program instance. This model provides the best isolation benefits and is used in Chromium by default."
  - Caveats (PDF p. 8): "Chromium also places a limit on the number of renderer processes it will create (usually 20), to avoid imposing too much overhead on the user's machine. This limit may be raised in future versions of the browser if RAM is plentiful. When the browser does reach this limit, existing rendering engine processes are re-used for new site instances."
  - §4.3 (PDF pp. 11–12): "For blank pages, the average site instance footprint rises from 0.38 MB to 1.7 MB between architectures. For popular pages, it rises from 3.9 MB to 10.6 MB." and "Also note that Chromium currently creates at most 20 rendering engine processes and then reuses existing processes, as discussed in Section 3.2."
- Coverage: T1 — covers the 2009 process model (browser kernel + rendering-engine processes; process-per-site-instance default; renderer cap "usually 20" with reuse) and per-site-instance memory (MB, mean, Chromium 2008, 10 Alexa pages; platform not stated in the quoted passages). **Dated (2009) and not a Linux observation → context** for the process model's origins; the 20-process cap is superseded by S1-01's soft limit and S1-18's RAM-derived threshold. Does not cover idle behaviour, wake cadence, CPU. T2/T3/T6: does not cover.
- One observation: one Chromium build, memory footprint per tab count; machine not stated in the passages read.

### S1-03 — Barth, Jackson, Reis, "The Security Architecture of the Chromium Browser", technical report 2008

- Citation: Adam Barth (UC Berkeley), Collin Jackson (Stanford), Charles Reis (University of Washington), and the Google Chrome Team. Stanford technical report, 2008.
- Copy read: `https://seclab.stanford.edu/websec/chromium/chromium-security-architecture.pdf`, accessed 2026-09-19T01:47Z, `sources/S1-03/chromium-security-architecture.pdf`, SHA-256 `8a19fed4ab876f29d07734a6a71893da6b730d742aceea38204b44c2bf61de5a`.
- Passages:
  - §3 (PDF p. 3): "Chromium's architecture has two modules: a rendering engine and a browser kernel. At a high level, the rendering engine is responsible for converting HTTP responses and user input events into rendered bitmaps, whereas the browser kernel is responsible for interacting with the operating system."
  - Process Granularity (PDF p. 4): "Roughly speaking, Chromium uses a separate instance of the rendering engine for each tab that displays content from the web, providing fault tolerance in the case of a rendering engine crash."
- Coverage: T1 — the two-module model and "a separate instance of the rendering engine for each tab" as of 2008. Dated → context only. No observation.

### S1-19 — Reis, Barth, Pizano, "Browser Security: Lessons from Google Chrome", ACM Queue 7(5), 2009

- Citation: Charles Reis, Adam Barth, Carlos Pizano. ACM Queue vol. 7 no. 5, June 2009 (also CACM 52(8), August 2009).
- Copy read: Internet Archive raw capture `https://web.archive.org/web/2023id_/https://queue.acm.org/detail.cfm?id=1556050` (queue.acm.org itself returned 403), accessed 2026-09-19T01:56Z, `sources/S1-19/browser-security-lessons-chrome-archive.html`, SHA-256 `7d8f055edead2d9da3399f5c25740df770898636085d5a4ffde99339bdec6298`.
- Passages (section "Reducing the Severity of Vulnerabilities"):
  - "Google Chrome has two major components that run in different operating-system processes: a high-privilege browser kernel and a low-privilege rendering engine. The browser kernel acts with the user's authority and is responsible for drawing the user interface, storing the cookie and history databases, and providing network access."
  - "Google Chrome generally places pages from different Web sites into different rendering-engine processes,11 but it can be difficult to do this in all cases, as is necessary for security. [...] For now, Google Chrome sometimes places pages from different origins in the same process."
  - "As we port Google Chrome to other platforms such as Mac and Linux, we expect to use a number of different sandboxing techniques but keep the same security architecture."
- Coverage: T1 context (2009, Windows-first description of the two-process split). No observation.

### S1-18 — Vila & Köpf, "Loophole: Timing Attacks on Shared Event Loops in Chrome", USENIX Security 2017 (arXiv 1702.06764)

- Citation: Pepe Vila, Boris Köpf (IMDEA Software Institute). 26th USENIX Security Symposium, 2017. arXiv:1702.06764.
- Copy read: `https://arxiv.org/pdf/1702.06764` (arXiv version), accessed 2026-09-19T01:54Z, `sources/S1-18/loophole.pdf`, SHA-256 `11d7d5557b5fb20e17f89f63a3776c60f00566ce5dea660e8d3028f33856f501`.
- Passages:
  - §2.2 (PDF p. 3): "The renderer processes are sandboxed processes responsible for parsing, rendering and Javascript execution. Communication with the host process is done via an inter-process communication (IPC) system based on message passing. Each renderer runs several threads; the most relevant ones are: • the MainThread where resource parsing, style calculation, layout, painting and non-worker Javascript runs, • the IOChildThread, which handles IPC communication with the host process, and • the CompositorThread, which improves responsiveness during the rendering phase by allowing the user to scroll and see animations while the main thread is busy, thanks to a snapshot of the page's state."
  - §2.3 (PDF p. 3): "The default policy is called process-per-site-instance. It requires using a dedicated renderer process for each instance of a site. [...] The other supported policies are more permissive. For example, the process-per-site policy groups all instances of a site in the same renderer process, trading robustness for a lower memory overhead. The process-per-tab policy dedicates one renderer process to each group of script-connected tabs."
  - §2.3 (PDF pp. 3–4): "Even in the restrictive default process-per-site-instance policy, there are some situations that force Chrome to host documents from different sites in the same renderer process, causing them to share the event loop: • Iframes are currently hosted in the same process as their parent. • Renderer-initiated navigations such as link clicks, form submissions, and scripted redirections will reuse the same renderer as the origin page. • When the number of renderer processes exceeds a certain threshold, Chrome starts to reuse existing renderers instead of creating new ones. On (64-bit) OSX and Linux, the threshold for reusing renderers is calculated by splitting half of the physical RAM among the renderers, under the assumption that each consumes 60MB.1 In our experiments, on a machine with 4 GB of RAM we could spawn 31 new tabs before any renderer was shared, whereas on a machine with 8 GB of RAM we observed a threshold of approximately 70 renderers. There is no apparent grouping policy for the pages that can share a process when this threshold is exceeded, except for tabs in Incognito mode not being mixed up with "normal" tabs. [...] In fact, even filesystem pages (loaded with file://) can co-reside with an arbitrary HTTP site."
  - §4.1.2 (PDF p. 7): "We conducted measurements on the following three machines: 1. Debian 8.6 with kernel 3.16.0-4-amd64, running on an Intel i5 @ 3.30GHz x 4 with 4 GB of RAM, and Chromium v53; 2. Debian 8.7 with kernel 3.16.0-4-amd64, running on an Intel i5-6500 @ 3.20GHz x 4 with 16 GB of RAM, and Chromium v57; and 3. OSX running on a Macbook Pro 5.5 with Intel Core 2 Duo @ 2.53GHz with 4 GB of RAM, and Chrome v54."
- Coverage:
  - T1: covers (a) the renderer's thread structure (MainThread, IOChildThread, CompositorThread) and the host process's CrBrowserMain/IOThread as mechanism; (b) the renderer-reuse threshold on Linux/OSX as mechanism (half of RAM ÷ 60 MB per renderer) and as a **Linux observation** of the process cap (object: number of tabs opened before a renderer is shared; unit: count; statistic: single observed threshold; scope: Chromium v53/v57 on Debian 8 kernel 3.16 in 2016–17; 31 tabs at 4 GB, ≈70 at 8 GB — note the 8 GB machine is not among the three listed, so its identity is not named); (c) file:// pages share renderers like any other. Pre-site-isolation (2017) — the iframe and link-click statements are superseded by S1-01. Does not cover idle-renderer wake cadence, CPU share or CPU per wake.
  - T2, T3, T6: does not cover.
- One observation? Yes for the threshold: machine (Debian 8.6, i5, 4 GB), subject (Chromium v53, N fresh tabs), window not stated (a count, not a time series).

### S1-07 — Thangadurai et al., "Electron vs. Web: A Comparative Analysis of Energy and Performance in Communication Apps", QUATIC 2024

- Citation: Jonathan Thangadurai, Priyeta Saha, Korawit Rupanya, Rosheen Naeem, Alejandro Enriquez, Ivano Malavolta (Vrije Universiteit Amsterdam), Gian Luca Scoccia, Matias Martinez. 17th International Conference on the Quality of Information and Communications Technology (QUATIC 2024), Springer CCIS, DOI 10.1007/978-3-031-70245-7_13.
- Copy read: author copy `http://www.ivanomalavolta.com/files/papers/QUATIC_2024_2.pdf`, accessed 2026-09-19T01:49Z, `sources/S1-07/electron-vs-web-quatic2024.pdf`, SHA-256 `be6daa9d830d44e51aff4405b815fb9fd36d11a7c07134ed1f02ccd8fa7ce120`. 16 PDF pages.
- Passages:
  - §5 Experiment Setup (PDF p. 7): "to conduct the experiment, we utilize a laptop with an Intel i7-11370H @ 3.30GHz CPU (CPU scaling enabled), an NVIDIA GeForce RTX 3050ti GPU, 4GB GDDR6 RAM, a 512GB PCIe NVMe M.2 SSD disk, and a virtual Web Camera (30FPS, 1280x720 resolution), running Ubuntu 22.04.2."
  - (PDF p. 7): "For the desktop version, we selected the most recent releases at the time this experiment has been executed (October 2023), i.e., Skype (version 8.104.0.207), Slack (4.34.120), and Discord (6.2.0-33-Generic). For the Web version, the latest version is automatically provided from the servers, accessed through the Google Chrome browser (117.0.5938.92)."
  - (PDF p. 8): "PowerJoular (version 0.6.2) [13]: a command-line tool for real-time monitoring of power consumption in CPU, GPU, and processes on GNU/Linux systems with low overhead. We choose this tool to capture, one sample per second, both energy consumption and CPU utilization."
  - (PDF p. 8): "In our measurements, observed CPU utilization refers to the combined usage of all 4 physical cores, given that hyper-threading is enabled. Similarly, memory utilization is calculated as the process' Resident Set Size (RSS) divided by the total device RAM."
  - (PDF p. 8): "Each run represents a unique combination of treatments, specifically a platform type (Electron-based apps or Web apps), an interaction mode (A, V, AS, or VS), and the interaction duration (2 or 8 minutes). Each distinct combination is executed eight times on each of our selected subjects"
  - §6 Results (PDF p. 9): "meetings we observed median values of 10.223J (10.216J), 14.33% (15.94%) CPU utilization, 2.899% (2.019%) memory utilization, and 14,204 (19,561) exchanged network packets. Regarding 8 minutes meetings, for Web (Electron) apps we observed median values of 41.17J (40.98J), 14.03% (15.91%) CPU utilization, 2.897% (2.02%) memory utilization, and 45,563 (71,413) exchanged network packets."
  - (PDF p. 9): "CPU usage: Web applications at both durations have means of 14.33% and 14.03% respectively, while Electron apps demonstrated means of 15.94% for the 2-minute duration and 15.91% for the 8-minute duration. Thus, Web apps use, as mean, less CPU than Electron ones. [...] Electron applications exhibited greater variability."
  - §7.2 (PDF p. 13): "Despite higher CPU utilization, Electron apps exhibited comparable or even lower energy consumption than Web apps. Although they engage the CPU more actively, especially in complex modes such as video and screen sharing, Electron apps perform these tasks more efficiently."
- Coverage:
  - T2: **Linux observation** — object: CPU utilization of the application process (as PowerJoular reports it, "combined usage of all 4 physical cores"), unit: per cent of the machine, statistic: median and mean over 1-Hz samples, scope: 2-minute and 8-minute two-party calls in audio / video / audio+screen-share / video+screen-share modes, population: Slack 4.34.120, Discord 6.2.0-33-Generic and Skype 8.104.0.207 Electron desktop clients pooled (the paper reports the Electron-vs-Web pooled figures; per-app figures are in an appendix not in this PDF), Ubuntu 22.04.2, i7-11370H, October 2023, 8 repetitions per treatment. The state is **in a call**, not idle; the figure is the app's CPU share under call traffic, pooled across three apps. Does not cover process/thread structure, heartbeat intervals, wake cadence, CPU per wake, message cost, or idle. Notes that the same apps run in Chrome 117 as a Web baseline.
  - T1: covers Electron only as "leveraging the capabilities of Chromium and Node.js" (PDF p. 2); no process-model detail. T3, T6: does not cover.
- One observation? One machine and one population of runs; machine, program versions, state (call, mode, duration) and window (2 / 8 min) named. The pooled statistic mixes three programs.

### S1-16 — Chang, Varvello, Hao, Mukherjee, "Can You See Me Now? A Measurement Study of Zoom, Webex, and Meet", IMC 2021 (arXiv 2109.13113)

- Citation: Hyunseok Chang, Matteo Varvello, Fang Hao, Sarit Mukherjee (Nokia Bell Labs). ACM IMC 2021. arXiv:2109.13113.
- Copy read: `https://arxiv.org/pdf/2109.13113`, accessed 2026-09-19T01:50Z, `sources/S1-16/can-you-see-me-now.pdf`, SHA-256 `639750300ce4c7f36b62180cdf4f3f5c5d9e102a3f68c3cc280be036fd7a6815`. 13 PDF pages.
- Passages:
  - §4.1 Cloud VM Setup (PDF p. 4): "Each cloud VM we deploy has 8 vCPUs (Intel Xeon Platinum 8272CL with 2.60GHz), 16GB memory and 30GB SSD. [...] We use the native Linux client for Zoom (v5.4.9 (57862.0110)), and the web client for Webex and Meet since they do not provide a native Linux client."
  - §6 (PDF p. 11), the mobile part: "CPU usage. Fig. 19a shows boxplots of CPU usage sampled every three seconds for the experiment duration across all devices and scenarios. [...] We report CPU usage in absolute numbers, e.g., 200% implies full utilization of two cores. If we focus on the LM and HM scenarios for S10 (high-end), the figure shows that Zoom and Webex have comparable CPU usage (median of 150–175%), while Meet adds an extra 50%. [...] Finally, CPU usage is minimized when the device screen is off. However, while Zoom and Meet's CPU usage is reduced to 25–50% (S10), Webex still requires about 125%." — preceded (PDF p. 11) by "two Android devices: S10 (high-end) and J3 (low-end)".
  - §7 (PDF p. 13): "Videoconferencing client. Our emulated client runs on Linux only (via in-kernel virtual devices). We consider that the modern Linux environment is representative enough for videoconferencing due to the good Linux support [13] or the use of cross-platform web clients by the existing systems."
- Coverage: T2 — covers that the native Zoom Linux client (v5.4.9) can be driven headlessly on a Linux VM with in-kernel virtual devices (the paper names snd-aloop and v4l2loopback, PDF p. 3, and xdotool for input, PDF p. 3); the **CPU figures are Android (S10/J3) → context, marked**; no CPU figure for the Linux client, no process structure, no idle state. T1/T3/T6: does not cover.
- One observation? Mobile CPU: two devices named, Zoom/Webex/Meet, five-minute calls × 5 repetitions. Linux VM: named (8 vCPU Xeon 8272CL), but no CPU statistic reported for it.

### S1-04 — MacMillan, Mangla, Saxon, Feamster, "Measuring the Performance and Network Utilization of Popular Video Conferencing Applications", IMC 2021 (arXiv 2105.13478)

- Citation: Kyle MacMillan, Tarun Mangla, James Saxon, Nick Feamster (University of Chicago). ACM IMC 2021. arXiv:2105.13478v1.
- Copy read: `https://arxiv.org/pdf/2105.13478v1`, accessed 2026-09-19T01:47Z, `sources/S1-04/macmillan-imc21.pdf`, SHA-256 `5c3ec6aa554fbce2d4df7678cdae70427ad5e53a1dfb37484b6aa6f93ad8adc7`.
- Passages (§3 Experiment Setup, PDF p. 3): "Most of our tests are conducted using the desktop applications for Teams and Zoom, and using the Google Chrome browser for Meet. [...] We use Chrome (Meet) version 89.0.4389, Zoom client version 5.6.1, and Teams client version 1.4.00.7556." and "Each laptop is a Dell Latitude 3300 with a screen resolution of 1366 × 768 pixels and running Ubuntu 20.04.1."
- Coverage: T2 — context only: names the Zoom (5.6.1) and Microsoft Teams (1.4.00.7556) native desktop clients running on Ubuntu 20.04.1 in 2021, with tc-shaped links and an ffmpeg-fed video source; the paper measures network utilisation and video quality, **no CPU, process or wake data** (the word "CPU" does not occur in the text). T1/T3/T6: does not cover.

### S1-06 — Sander, Kunze, Wehrle, Rüth, "Video Conferencing and Flow-Rate Fairness: A First Look at Zoom and the Impact of Flow-Queuing AQM", PAM 2021 (arXiv 2107.00904)

- Citation: Constantin Sander, Ike Kunze, Klaus Wehrle, Jan Rüth (RWTH Aachen). Passive and Active Measurement (PAM) 2021, author's version. arXiv:2107.00904v1.
- Copy read: `https://arxiv.org/pdf/2107.00904v1`, accessed 2026-09-19T01:47Z, `sources/S1-06/zoom-flowrate.pdf`, SHA-256 `7bef6968e68868ffbcb3553b13b8203f939e25c28d5d682ecd87466ecc99009a`.
- Passage (§3, PDF p. 6): "As their video feeds, both clients simulate a webcam via v4l2loopback [3]. [...] The measurements were made from July 2020 to October 2020 on Linux 5.4.0-31 with Zoom version 5.0.408598.0517."
- Coverage: T2 — context: Zoom's Linux client run under Linux 5.4 with v4l2loopback for a network-side (congestion-control) study; no CPU, process or idle data. T1/T3/T6: does not cover.

### S1-05 — Kumar, Nagpal, Naik, Chakraborty, "Comparison of Popular Video Conferencing Apps Using Client-side Measurements on Different Backhaul Networks", arXiv 2210.09651 (2022)

- Citation: Rohan Kumar, Dhruv Nagpal, Vinayak Naik (BITS Pilani Goa), Dipanjan Chakraborty (BITS Pilani Hyderabad). arXiv:2210.09651v1, October 2022.
- Copy read: `https://arxiv.org/pdf/2210.09651v1`, accessed 2026-09-19T01:47Z, `sources/S1-05/vc-apps-clientside.pdf`, SHA-256 `b6cd5b9b87fcac4ceb0ef199562ce9bbb1d0064966a783ad6c809ef527b38c71`.
- Passages: Table 2 (PDF p. 4): "CPU Intel i5-8265U / Intel i5-8250U — RAM 16 GB / 16 GB — OS Windows 10 / Windows 10". Figure 8 caption (PDF p. 8): "Sender-side CPU load for WiFi with mic ON [...] Meet and Zoom have a similar average CPU utilization, however, CPU load has lesser variation for Zoom." (PDF p. 8): "Microsoft Teams [...] the highest CPU load among all the apps for all test types."
- Coverage: T2 — **Windows 10 → context, marked**: client CPU load (per cent, psutil sampling) for Zoom, Meet, Teams during calls. No Linux data. T1/T3/T6: does not cover.

### S1-22 — Jacob, Grashöfer, Hartenstein, "A Glimpse of the Matrix (Extended Version): Scalability Issues of a New Message-Oriented Data Synchronization Middleware", Middleware 2019 demos & posters (arXiv 1910.06295)

- Citation: Florian Jacob, Jan Grashöfer, Hannes Hartenstein (Karlsruhe Institute of Technology, Institute of Telematics). ACM Middleware 2019 Demos and Posters, DOI 10.1145/3366627.3368106; extended version arXiv:1910.06295v2.
- Copy read: `https://arxiv.org/pdf/1910.06295v2`, accessed 2026-09-19T01:58Z, `sources/S1-22/glimpse-of-the-matrix.pdf`, SHA-256 `279b9bd502d1a693f521ca93e22f27dd7defa24506edf9d165613950269605a2`.
- Passage (§1, PDF p. 1): "It is based on a client-server architecture where independent servers with limited mutual trust cooperate. It provides topic-based publish-subscribe access on an eventually-consistent database of messages and state changes. Topics are called rooms in Matrix. A user's devices only connect to the user's Matrix homeserver, which acts as representative for the user in the Matrix federation. [...] In contrast to other message-oriented middlewares, Matrix does not provide message passing but message history synchronization [16]."
- Coverage: T2 — mechanism context for Element/Matrix: a client talks only to its homeserver and synchronises history (the paper is about server-to-server federation load; it states no client sync interval, no keep-alive, no CPU). T1/T3/T6: does not cover.

### S1-08 — Changwoo Min, "Using sched_ext to improve frame rates on the SteamDeck — Ideas behind the LAVD scheduler", Linux Plumbers Conference 2024 (slides)

- Citation: Changwoo Min (Igalia), LPC 2024 sched_ext microconference, Vienna, 18 September 2024. Slide deck, 20 slides. Grey literature (conference talk), not peer-reviewed.
- Copy read: `https://lpc.events/event/18/contributions/1713/attachments/1425/3058/scx_lavd-lpc-mc-24.pdf`, accessed 2026-09-19T01:49Z, `sources/S1-08/scx_lavd-lpc-mc-24.pdf`, SHA-256 `77c9cefec98e0346d5b89a219ca30eff7cb4f448016b24fa0871b286ba421eb4`.
- Passages:
  - Slide 5 "Understanding game workloads": "Tasks run for very short duration — roughly a few 100s usec on average. Multiple tasks are tightly linked to in a task graph to finish a single job (e.g., updating a frame)." Chart labels: "Distribution of task's runtime average per schedule in a game", "< 1 msec", "Top 50% of waiters and wakers".
  - Slide 9: "High wake up frequency ⇒ important producer in a task graph. High wait frequency ⇒ important consumer in a task graph. Both are high ⇒ important task in the middle."
  - Slide 10: "a fixed time interval == targeted latency (e.g., 15 msec) [...] Time slice = f(number of runnable tasks)".
  - Slide 15 "Usages can be captured by CPU utilization": "Light load (around 10%) — Usage: code editing + reading a PDF + music/video streaming [...] Medium load (<70%) — Usage: running a casual game, a kernel module compilation [...] Heavy load (>70%) — Usage: running a AAA game, full kernel compilation".
  - Slide 17: "FH5 in-game benchmark with background recording on SteamDeck OLED — LAVD 1419.49 J (15.4 W) — EEVDF 1423.75 J (15.5 W)". Slide 18: "Tomb Raider in-game benchmark without background task on SteamDeck OLED — LAVD 752.83 J (10.7 W) — EEVDF 896.07 J (12.7 W)".
- Coverage:
  - T6: covers how a gaming-scheduler author characterises the interactive workload — a task graph of short-running (hundreds of µs) tasks where waker/wakee frequency defines latency criticality; the only "background" load beside a game is "background recording" (slide 17; the recorder is not named), with whole-device energy (J, W) as the figure; no browser, Electron or chat client, no per-process CPU or wake count.
  - T3: does not name any Steam client process; the SteamDeck is the machine, the games are the subject. Does not cover T3's process structure or CPU share.
  - T1, T2: does not cover.
- One observation? The energy figures: machine (SteamDeck OLED) and subject (FH5 / Tomb Raider in-game benchmark, LAVD vs EEVDF) named; window = the in-game benchmark run; trace details not on the slides.

### S1-09 — Changwoo Min, "Steps Towards a Gaming-Optimized Scheduler", Linux Plumbers Conference 2025 (slides)

- Citation: Changwoo Min (Igalia), LPC 2025, 13 December 2025. 15 slides. Grey literature.
- Copy read: `https://lpc.events/event/19/contributions/2150/attachments/1951/4162/Steps_Towards_a_Gaming_Optimized_Schedule-lpc2025.pdf`, accessed 2026-09-19T01:49Z, `sources/S1-09/gaming-optimized-scheduler-lpc2025.pdf`, SHA-256 `e478aa851e39c1d01e94e3b7bcbecaaf51310107c801b6c1821015ff57267059`.
- Passages:
  - Slide 2: "Primary target: Windows games running on Linux (SteamOS) — Implemented based on the sched_ext framework (BPF + Rust)".
  - Slide 6: "We developed an analysis tool, VaporMark — https://github.com/Igalia/vapormark — VaporMark collects all the scheduling activities during a period using "perf sched record" — Then, it analyzes the collected trace to understand high-level properties."
  - Slide 8: "To accomplish a single high-level job (e.g., moving a character upon a keypress event), many tasks should tightly collaborate. Task graphs of top 50 percentile of waker-wakees. Let's prioritize a task with high waker-wakee frequency! Those tasks are in the middle of the task chain."
  - Slide 12: "most scheduler benchmarks focus on stressing schedulers. E.g., stress-ng, perf bench, hackbench. Improving the score of those benchmark may not improve the actual game performance." Slide 13: "schbench: reproduce the scheduler characteristics of a production web workload. We need something similar to schbench for gaming, say gamebench?"
- Coverage: T6 — the method (perf sched record → waker/wakee graphs) and the statement that standard scheduler benchmarks are stress tests unrelated to interactive performance. T3 — VaporMark targets Steam-launched games but the slides name no Steam client process. T1/T2: does not cover. No numbers.

### S1-10 — LWN, "Lessons from creating a gaming-oriented scheduler" (report of the LPC 2025 talk), LWN.net, 2025

- Citation: Jake Edge, LWN.net, Article 1051430, 7 January 2026 (report of Changwoo Min's LPC 2025 session). Grey literature.
- Copy read: `https://lwn.net/Articles/1051430/`, accessed 2026-09-19T01:49Z, `sources/S1-10/lwn-1051430.html`, SHA-256 `5013b01ed434bb0d6bc93820569c056c22cc032babfdff0e8cbfde92f1570651`.
- Passages (article body):
  - "So he developed VaporMark—the name refers to Steam—which analyzes data collected using "perf sched record". "After collecting huge amounts of data, post-processing it for an hour or two, it shows some reports.""
  - "The key finding that came out of his analysis is perhaps somewhat obvious: a single high-level action, such as moving a character on-screen and emitting a sound based on a key-press event, requires that many tasks work together. Some of the tasks are threads in the game process, but others are not because they are in the game engine, kernel, and device drivers; there are often 20 or 30 tasks in a chain that all need to collaborate."
  - "For example, a game may run smoothly most of the time, but have a latency spike every five minutes or so that results in a drop in the FPS rate. "How should I catch this?" He was not able to find a way to trigger on the problem so that his trace showed what led to it; instead he used brute-force methods of sampling every ten seconds, hoping to catch the problem occurring."
  - Section "Locks": "Most of the tasks in a Windows game are short-running and computation-intensive, so it is important to avoid situations where locking prevents a task from quickly completing."
- Coverage: T6 — chain length ("20 or 30 tasks") for one keypress in a game, as an author's characterisation, and the perf-sched-based method. T3 — Steam is named only as the source of VaporMark's name; no client process named. T1/T2: does not cover. No CPU or wake figures.

### S1-11 — LWN, "Sched_ext at LPC 2024", LWN.net, 2024

- Citation: Jonathan Corbet, LWN.net, Article 991205, 26 September 2024. Grey literature.
- Copy read: `https://lwn.net/Articles/991205/`, accessed 2026-09-19T01:49Z, `sources/S1-11/lwn-991205.html`, SHA-256 `aacfa63fecfba21761debbdfea89a91e0dc95d319ceaff1128952a7c5f890c25`.
- Passages:
  - (opening section) "The scx_lavd scheduler, for example, is focused on interactivity and, specifically, consistently getting higher frame rates out of games. The scx_bpfland scheduler, instead, is aimed at minimizing response times."
  - "One of those appears to be scx_lavd (about which more was heard later), which is headed for shipment in Steam Deck gaming systems. scx_bpfland is showing promising results for personal machines, while scx_layered has been deployed in over one million machines and is delivering significant performance gains."
  - Section "Higher frame rates": "A key aspect of gaming workloads is that tasks tend to run quickly, typically no more than 100µs at a time. There are a lot of tightly linked tasks, though, and performance depends on the most critical of those tasks running in the necessary sequence; that is the critical path. Every task has a latency criticality that is determined by its place in this path; tasks that wait on others, and are waited on in turn, have a large impact on overall performance and are thus "latency critical"."
  - "Min concluded by saying that, for gaming applications, scx_lavd consistently enables higher frame rates than the EEVDF scheduler while using (slightly) less power and with fewer stutters."
- Coverage: T6 — the "≤100 µs per run" characterisation (reported speech; S1-08 slide 5 says "a few 100s usec") and the stated mechanism (latency criticality from wait/wake frequencies); no browser/chat workload; no figures. T3: "Steam Deck" as deployment target only. T1/T2: does not cover.

### S1-24 — LWN, "What's scheduled for sched_ext", LWN.net, 2024

- Citation: Daroc Alden, LWN.net, Article 974387, 23 May 2024 (report from LSFMM+BPF 2024). Grey literature.
- Copy read: `https://lwn.net/Articles/974387/`, accessed 2026-09-19T01:59Z, `sources/S1-24/lwn-974387.html`, SHA-256 `54600c22d5524ea55f63bc86b074f8489c6a67313d26498d1ead1dcbebdab0ab`.
- Passages:
  - "scx_rusty uses the length of time for which a task actually ran, instead of its static slice length, which lets it schedule tasks that only run for a short time before blocking more frequently than tasks that use their whole time quantum. The scheduler also considers whether the task often blocks waiting for other tasks (indicating a consumer), wakes other tasks (indicating a producer), or both (indicating the middle of a pipeline). It factors this information in to the virtual deadline calculated for the task, slightly prioritizing tasks that block frequently, and greatly prioritizing tasks that wake other threads."
  - "Vernet showed another demo of a game experiencing lag under EEVDF, which immediately disappears upon enabling scx_rusty. Normally, interactivity is a tradeoff against throughput. Vernet claimed that scx_rusty actually also has slightly better throughput than EEVDF, but didn't cite specific numbers."
  - "Vernet clarified that for gaming, people mostly care about tail latency."
- Coverage: T6 — mechanism only (short-runtime and waker tasks prioritised; a lag demo without numbers). Does not cover T1/T2/T3.

### S1-12 — LWN, "An EEVDF CPU scheduler for Linux", LWN.net, 2023

- Citation: Jonathan Corbet, LWN.net, Article 925371, 9 March 2023. Grey literature.
- Copy read: `https://lwn.net/Articles/925371/`, accessed 2026-09-19T01:49Z, `sources/S1-12/lwn-925371.html`, SHA-256 `25ef08e5f3f4b0b8ea441aa1407ddcadc907c790c1c799453e472a29903aaf7c`.
- Passages:
  - "One place where there is a desire for improvement is in the handling of latency requirements. Some processes may not need a lot of CPU time but, when they do need that time, they need it quickly. Others might need more CPU time but can wait for it if need be. CFS does not give processes a way to express their latency requirements; nice values (priorities) can be used to give a process more CPU time, but that is not the same thing."
  - Section "Addressing the latency problem": "When the scheduler is calculating the time slice for each process, it factors in that process's assigned latency-nice value; a process with a lower latency-nice setting (and, thus, tighter latency requirements) will get a shorter time slice. [...] Latency-sensitive processes, which normally don't need large amounts of CPU time, will be able to respond quickly to events, while processes without latency requirements will be given longer time slices, which can help to improve throughput."
  - "Some of the results, he said, "seem to indicate EEVDF schedules a lot more consistently than CFS and has a bunch of latency wins"."
- Coverage: T6 — the stated mechanism by which an interactive process that "may not need a lot of CPU time" is served under EEVDF; no workload named, no browser/chat client, no figures. Does not cover T1/T2/T3.

### S1-13 — Wang, Jia, Huang et al., "Mixture-of-Schedulers: An Adaptive Scheduling Agent as a Learned Router for Expert Policies", arXiv 2511.11628 (2025)

- Citation: Xinbo Wang, Shian Jia, Ziyang Huang et al. (Zhejiang University). arXiv:2511.11628v1, 7 November 2025. Preprint.
- Copy read: `https://arxiv.org/pdf/2511.11628v1`, accessed 2026-09-19T01:49Z, `sources/S1-13/mixture-of-schedulers.pdf`, SHA-256 `3a887853b4b21974373f912492963108f55f1526f1e951934a233c850fb07b8b`. 15 PDF pages.
- Passages:
  - §5.1.1 (PDF p. 7): "we constructed a benchmark suite of 28 scenarios. These are generated by pairing 4 interactive, latency-sensitive applications (Web Browsing, Audio Remix, Office File, Game Play) with 7 resource-intensive, background workloads (e.g., kernel compilation, blender render, LLM local generation)."
  - Appendix A (PDF p. 13): "Web Browsing Scenario: Users are particularly sensitive to issues such as page load latency, scrolling stutter, and unresponsive input. [...] To objectively quantify the user experience in the web browsing scenario, this study designed the following test method: multiple local HTML files containing common interface components found in web browsing were written as test content. The Selenium framework [40], widely used for browser automation testing, was utilized to perform automated operations in the Chrome browser [42]. By injecting JavaScript timers, the response time of interactions such as clicks, scrolls, and tab switches, as well as the stability of the frame rate, were accurately recorded to evaluate the scheduler's performance in this scenario."
  - Appendix A (PDF p. 13), Game Play: "This study selected the best-selling game of all time, "Minecraft" [32], for testing. [...] collecting frame rate, frame generation time, number of loaded chunks, and MSPT (milliseconds per game tick)".
  - §5 results (PDF p. 11): "achieves an overall win rate of 86.4% against EEVDF, with a global average improvement of +8.83% (95% CI [7.08%, 10.59%])."
  - Appendix (PDF p. 14): "this study chose the complete compilation of the Linux 6.14" [kernel as the compile load].
- Coverage: T6 — the only scheduler evaluation found that uses a **browser (Chrome, driven by Selenium over local HTML files) as the foreground interactive workload** beside background loads, on Linux with sched_ext expert schedulers (LAVD among them, PDF p. 2) against EEVDF; the browser is the *interactive* subject, not a background load of idle renderers; figures are composite scores (response time of clicks/scrolls/tab switches, frame-rate stability) and the aggregate +8.83 % — **no per-process CPU, run/wait or wake figures, and the number of tabs is not stated**. The hardware is not named in the passages located (the text extraction has no CPU model). T1/T2/T3: does not cover.
- One observation? A benchmark campaign; machine not named in the text located; subject (Chrome + local HTML + Selenium; Minecraft; PulseAudio mixing; LibreOffice) named; windows not quoted.

### S1-23 — Nikseresht, Somayaji, Maheshwari, "Customer Appeasement Scheduling", arXiv 1012.3452 (2010)

- Citation: Mohammad R. Nikseresht, Anil Somayaji, Anil Maheshwari. arXiv:1012.3452v1, 15 December 2010. Preprint, 23 pages.
- Copy read: `https://arxiv.org/pdf/1012.3452v1`, accessed 2026-09-19T01:58Z, `sources/S1-23/customer-appeasement.pdf`, SHA-256 `508ed1576f8ca1b083a344332af8cf056f4f1c0f372322facf9b5eff54f7c95b`.
- Passages: (PDF p. 4) "For example, we observed almost constant average Mysql response times, and almost constant frame rate for mplayer under different (simulated) background loads." (§7.1, PDF p. 17) "All tests are performed on an IBM (R) IntelliStation M Pro with Intel P4 2.8GHz CPU and 1GB of RAM running Fedora 12 with Kernel 2.6.32. In order to simulate different background system loads we compile Linux kernel and use different -j values with the make command to initiate different parallel compilations."
- Coverage: T6 — **dated (2010, kernel 2.6.32) → context**: interactive subject is mplayer (frame rate) beside kernel-compile background load; a web browser is mentioned only as an example of an interactive program (PDF p. 3), not measured. Does not cover T1/T2/T3.

### S1-21 — LWN, "Group scheduling and alternatives", LWN.net, 2010

- Citation: Jonathan Corbet, LWN.net, Article 418884, 6 December 2010. Grey literature.
- Copy read: `https://lwn.net/Articles/418884/`, accessed 2026-09-19T01:56Z, `sources/S1-21/lwn-418884.html`, SHA-256 `b700655c9bd8316ff85afea7c48df0c156822ece1982274bf5b49d5218961ca4`.
- Passages: "Group scheduling, instead, is about isolation - keeping groups of processes from interfering with each other. [...] Group scheduling will not cause one set of processes to run in favor of another; it just ensures that the division of CPU time between the groups is fair." and (Con Kolivas's alternative) "He would attach a parameter to every process describing its latency needs. Applications could then be coded to communicate their needs to the kernel; an audio processing application would request the lowest latency, while make would inform the kernel that latency matters little."
- Coverage: T6 — **dated (2010) → context** on why background load hurts interactivity under fair scheduling (per-session groups as the remedy). No browser, no figures. Does not cover T1/T2/T3.

### S1-20 — LWN, "A survey of scheduler benchmarks", LWN.net, 2017

- Citation: Matt Fleming (guest article), LWN.net, Article 725238, 14 June 2017. Grey literature.
- Copy read: `https://lwn.net/Articles/725238/`, accessed 2026-09-19T01:56Z, `sources/S1-20/lwn-725238.html`, SHA-256 `ef29afa716efa8909a14324b755a10571e60152c2319067018749b95d7f03dcb`.
- Passage: "One benchmark that does provide detailed latency distribution statistics for scheduler wakeups is schbench. It allows users to configure the usual parameters — such as number of tasks and test duration — but also the time between wakeups (--sleeptime), time spinning once woken (--cputime); it also has the ability to automatically increase the task count until the 99th percentile wakeup latencies become extreme." and "scheduler wakeup delays can quickly lead to major performance issues."
- Coverage: T6 — context: the benchmark literature models a workload as wake-ups with sleep/spin times (schbench, hackbench, perf bench sched); no desktop application, browser or chat client appears. Does not cover T1/T2/T3.

### S1-15 — Jin, Li, Zou, "Impact of Extensions on Browser Performance: An Empirical Study on Google Chrome", Empirical Software Engineering (manuscript), arXiv 2404.06827 (2024)

- Citation: Bihui Jin, Heng Li, Ying Zou. Empirical Software Engineering manuscript; arXiv:2404.06827.
- Copy read: `https://arxiv.org/pdf/2404.06827`, accessed 2026-09-19T01:49Z, `sources/S1-15/chrome-extensions.pdf`, SHA-256 `796a49ce4d905da5fce28fbc129cb61760d79431911222c9e19ac15a15d6aa74`.
- Passages: (PDF p. 9) "To conduct our experiment, we use a desktop equipped with an Intel i7-4770 @3.4GHz processor, 32 GB of RAM, running Ubuntu (kernel version: 5.15.0-48-generic) with both WiFi and Bluetooth disabled. [...] The Google Chrome browser of version 104.0.5112.79 (Official Build 64-bit) is utilized in our experiment." (PDF p. 9) "The stabilized energy consumption measures the energy consumption of the CPU and RAM by the entire system in joules during a fixed period of time after a webpage has been fully loaded." (PDF p. 10) "Once the page finishes loading, the stabilized energy consumption of CPU and memory usage is measured for one minute for non-video testing scenarios and two minutes for the video testing scenario." (PDF p. 14) "63% (i.e., 45) of the extensions consume an extra 2.0% of the stabilized energy on average, while 8.3% (i.e., 6) of the extensions reduce the stabilized energy consumption by"
- Coverage: T1 — **Linux, but system-level**: the "stabilized" one-minute window after page load is the nearest thing found to a loaded-but-idle Chrome tab on Linux; the object is whole-system RAPL energy (J), not renderer CPU, wake cadence or per-process anything; one tab per run. Context. T2/T3/T6: does not cover.

### S1-17 — de Macedo, Aloísio, Gonçalves, Pereira, Saraiva, "Energy Wars – Chrome vs. Firefox: Which browser is more energy efficient?", ASEW 2020

- Citation: João de Macedo, João Aloísio, Nelson Gonçalves (Univ. of Minho), Rui Pereira (HASLab/INESC Tec), João Saraiva (Univ. of Minho). 35th IEEE/ACM ASE Workshops (ASEW 2020), DOI 10.1145/3417113.3423000.
- Copy read: `https://states.github.io/files/p23.pdf` (open copy located by WebSearch; repositorium.uminho.pt also lists it), accessed 2026-09-19T01:52Z, `sources/S1-17/energy-wars-chrome-firefox.pdf`, SHA-256 `10d094e6c44f2dc8f02a11ca35754de224e6129dea99890b94274c4bff301a7e`.
- Passage (PDF p. 3): "All measurements were performed in the same machine17: Linux Ubuntu Desktop 18.04 operating system, with 16GB of RAM, Intel® Core™i7 8750H 2.2 GHz Maximum Boost Speed 4.1 GHz." and (PDF p. 2) "as the script actions were monitored, CPU and DRAM energy measurements were collected: 10 per second, according to the RAPL".
- Coverage: T1 — context only: Linux RAPL energy of scripted browsing (Selenium) per site for Chrome and Firefox; no process model, no idle/background state, no per-process CPU. T2/T3/T6: does not cover.

### S1-26 — Varvello & Livshits, "Shedding (Some) Light on Mobile Browsers Energy Consumption", TMA 2021

- Citation: Matteo Varvello (Nokia Bell Labs), Benjamin Livshits (Brave Software). IFIP TMA 2021, paper 18.
- Copy read: `https://dl.ifip.org/db/conf/tma/tma2021/tma2021-paper18.pdf`, accessed 2026-09-19T01:59Z, `sources/S1-26/varvello-tma2021.pdf`, SHA-256 `e6f55b1a97f818185b8c82d571e82550f8d2d81b989a778c437f924e14d530fa`.
- Passages (PDF p. 3): "In these workloads, we stress test the browsers by loading 100 websites sequentially, each in a new tab. We choose 100 tabs given Chrome stops counting tabs at this point, suggesting that it should be an upper bound for most users." and "Opera Mini (along with Vivaldi) shows very high CPU consumption, with median of 65%, 2.5x times the CPU consumption of the lightest browsers".
- Coverage: T1 — **Android → context, marked**: the only many-tabs CPU study found (up to 100 tabs, CPU % per browser, Android Debug Bridge sampling); nothing on desktop Linux renderer processes. Does not cover T2/T3/T6.

### 2b. Read, not candidates (copies kept for the record)

- S1-14 — Miller et al., "Agile Development of Linux Schedulers with Ekiben", arXiv 2306.15076; `https://arxiv.org/pdf/2306.15076`, accessed 2026-09-19T01:49Z, `sources/S1-14/ekiben.pdf`, SHA-256 `efa0068ec5c3a6ec63293beda99698918f05afe6c8318ccd36d67c77d278c131`. Evaluated with schbench-style latency and server workloads; no browser, desktop or chat workload (grep for browser/chrome/firefox/interactive/desktop/game hit only references). Does not cover T1/T2/T3/T6.
- S1-25 — LWN, "The extensible scheduler class", Article 922405; `https://lwn.net/Articles/922405/`, accessed 2026-09-19T01:59Z, `sources/S1-25/lwn-922405.html`, SHA-256 `fb281438f6a52d62a31f702dc2d3a8824c1c8a017ca4a15d67c803e95f96f1f2`. Describes the sched_ext framework; no workload characterisation. Does not cover.

## 3. Not found

- **T1, Linux observation of an idle renderer's wake cadence, CPU per wake or CPU share per tab state** — no peer-reviewed or preprint source found. Established by rows 1–5, 15–16, 21, 28, 31–32, 43, 45–46, 55–58, 76 (arXiv abstract searches for "background tab(s)", "renderer process", "site isolation", "idle power"+"wake-ups", browser+energy+tabs all returned 0 or off-topic; WebSearch surfaced only vendor docs (S2) and bug reports (S3)). What exists in class: the process model as mechanism (S1-01, S1-18), Windows field statistics of renderer counts and CPU (S1-01, context), a Linux renderer-reuse threshold (S1-18), whole-system Linux energy after page load (S1-15, context), Android many-tabs CPU (S1-26, context). Electron/CEF: S1-07 says only that Electron embeds Chromium and Node.js; no source describes what Electron/CEF hosts share of Chromium's process model.
- **T2, process/thread structure, heartbeat or keep-alive intervals, message cost, idle CPU or wake cadence of Discord, Slack, Element, Zoom, Teams on Linux** — no source in class states any of these. Established by rows 7–8, 17–20, 25–26, 40–42, 49–50, 52–54, 59–62, 71. Found instead: an in-call Linux CPU share pooled over Slack/Discord/Skype (S1-07); Zoom's and Teams' Linux clients run under automation on Ubuntu (S1-04, S1-06, S1-16) with no CPU figures for Linux; Windows in-call CPU (S1-05, context); Matrix's client–homeserver architecture at the level of one sentence (S1-22). Nothing on running any client without an account or against a self-hosted server beyond the automation setups quoted.
- **T3, the Steam client's processes (steamwebhelper, gameoverlayui) or any measurement of the client beside a game on Linux** — nothing in class. Established by rows 9, 11, 23–24, 36, 48, 53, 65, 69, 72. The gaming-scheduler talks and LWN reports (S1-08 to S1-11, S1-24) name the Steam Deck and Steam-launched games but never a client-side process; the VaporMark README (out of class, row 69) monitors "steam and all its decendents" without naming them; the only Proton paper found (ICCCI 2023) is paywalled and, by its abstract, compares FPS across OSes.
- **T6, a scheduler evaluation using a many-tab browser, an Electron app or a chat client as *background* load with reported CPU, run/wait or wake figures** — not found. Established by rows 9–10, 27, 44, 47, 61, 70, 73, 75. Nearest: S1-13 uses Chrome as the *foreground* interactive subject against compile/render/LLM background loads with composite scores and no per-process figures; the gaming literature (S1-08, S1-10, S1-11, S1-24) characterises the interactive load as chains of short (≤ hundreds of µs) tasks ranked by wake/wait frequency, and treats "background recording" as the only co-load; the benchmark literature (S1-20) models load as synthetic wake-ups (schbench). No source states what an idle multi-process browser or chat client does to interactivity, with figures.
