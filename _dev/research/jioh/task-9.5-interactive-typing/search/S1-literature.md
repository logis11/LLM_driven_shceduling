# S1 — peer-reviewed and preprint literature (T1–T6)

Reader: S1. Date of all searches, fetches and reads: 2026-09-13. Input read: `search/input.md` only.

Method notes. Every source below was fetched by `curl` through the session proxy and read from the fetched copy; text was extracted with PyMuPDF 1.28.2 (page markers inserted per PDF page), except Tsafrir 2003, whose Type-3 fonts drop every "c" in extraction — its pages 4 and 7–9 were rendered to PNG (110 dpi) and read visually; every quote from that paper is transcribed from a rendered page. Page locators are PDF page numbers of the copy read unless noted. Copies are under `sources/S1-<id>/` (gitignored). SHA-256 values are of the file named in each entry. Semantic Scholar metadata lookups were used only to locate open copies; nothing is quoted from a metadata record or an abstract page.

## 1. Search log

### 1a. Web searches (engine: WebSearch, 2026-09-13)

| # | Query | Hits followed | Dead ends (status) |
|---|---|---|---|
| 1 | `Feit Weir Oulasvirta "How We Type" CHI 2016 pdf` | zenodo.org/records/4034268 (dataset record, API JSON 200 — lists Typing.zip, Motion Capture.zip; no paper PDF); userinterfaces.aalto.fi/how-we-type/ (200) → resources/HowWeType_CHI16.pdf (200) | userinterfaces.aalto.fi/how-we-type/resources/chi16-typing.pdf (404) |
| 2 | `Endo Wang Chen Seltzer "Using latency to evaluate interactive system performance" OSDI 1996 pdf` | usenix.org conference page (200, no PDF link); Wayback CDX for usenix.org/…/osdi96/full_papers/endo* → endo.txt and endo.ps (200) | usenix.org/legacy/…/full_papers/endo/endo.pdf (404); usenix.org/legacy/…/osdi96/full_papers/endo.pdf (404, S3 NoSuchKey); dl.acm.org/doi/pdf/10.1145/238721.238775 (403 Cloudflare challenge); syrah.eecs.harvard.edu (403); eecs.harvard.edu/margo/papers/osdi96/paper.pdf (200 but an HTML redirect to the home page); web.archive.org/web/2010id_/http://www.usenix.org/…/endo.pdf (404) |
| 3 | `Lee Crowley Baer Anderson Bershad "Execution characteristics of desktop applications on Windows NT" pdf` | dblp; ieeexplore.ieee.org/document/694760 (not fetched — paywalled venue) | homes.cs.washington.edu/~bershad/Papers/p27-lee.pdf (404); dl.acm.org/doi/pdf/10.1145/279358.279366 (403 Cloudflare) |
| 4 | `"Execution Characteristics of Desktop Applications on Windows NT" ISCA 1998 pdf citeseerx OR wustl OR washington.edu` | homes.cs.washington.edu/~baer/isca98.pdf (200) | — |
| 5 | `Etsion Tsafrir Feitelson "Desktop scheduling: how can we know what the user wants" pdf` | yoav.net.technion.ac.il/files/2016/05/Desktop04NOSSDAV.pdf (200); dants.github.io/papers/HuCsched06TOMCCAP.pdf (200) | cs.huji.ac.il/~feit/papers/DesktopSched04NOSSDAV.pdf, OutputSched06TOMCCAP.pdf, ClockRes03SIGMETRICS.pdf (all 200 but body is a HUJI WAF error page "Something went wrong… Support ID", not the PDF); cs.technion.ac.il/~dan/papers/DesktopSched04NOSSDAV.pdf (404), OutputSched06TOMCCAP.pdf (404) |
| 6 | `Lorch Smith "Using user interface event information in dynamic voltage scaling algorithms" pdf` | www2.eecs.berkeley.edu/Pubs/TechRpts/2002/5261.html → CSD-02-1190.pdf (200) | cs.berkeley.edu/~lorch/papers/mswim03.pdf (404); people.eecs.berkeley.edu/~lorch/papers/mswim03.pdf (404); ieeexplore.ieee.org/document/1240641 (paywalled venue, not fetched) |
| 7 | `Flautner Reinhardt Mudge "Automatic performance setting for dynamic voltage scaling" pdf` | Wayback 2015 copy of web.eecs.umich.edu/~tnm/papers/mobicom01.pdf (200) | web.eecs.umich.edu/~tnm/papers/mobicom01.pdf (curl exit 60 "unable to get local issuer certificate", also with the proxy CA bundle; proxy status shows no relay failure — host's TLS chain not verifiable); link.springer.com/content/pdf/10.1023/A:1016546330128.pdf (200, HTML paywall page, not a PDF); deepblue.lib.umich.edu/bitstream/2027.42/41391/… (403 Cloudflare) |
| 8 | `Blake Dreslinski Mudge Flautner "Evolution of thread-level parallelism in desktop applications" pdf` | dblp, ACM (not fetched) | web.eecs.umich.edu/~tnm/papers/isca10.pdf (TLS failure as above); Wayback copy of the same URL (404, never archived); Wayback CDX of tnm.engin.umich.edu/wp-content/uploads/* has no 2010 ISCA file; tnm.engin.umich.edu/publications/ (403) |
| 9 | `Roeser De Maeyer Leijten Van Waes "Modelling typing disfluencies as finite mixture process" Reading and Writing` | link.springer.com/content/pdf/10.1007/s11145-021-10203-z.pdf (200, open access) | — |
| 10 | `PipeWire PulseAudio latency measurement Linux Audio Conference paper pdf quantum period` | none (forum/blog hits only) | — |
| 11 | `MacMillan Mangla Saxon Feamster "Measuring the performance and network utilization of popular video conferencing applications" arXiv` | arxiv.org/pdf/2105.13478 (200) | people.cs.uchicago.edu/~macmillan/papers/macmillan2021videoconferencing.pdf (curl exit, connection failed) |
| 12 | `Endo Seltzer "Improving interactive performance using TIPME" SIGMETRICS 2000 pdf` | Wayback 2005 copy of eecs.harvard.edu/~margo/papers/sigmetrics00/paper.pdf (200) | dl.acm.org/doi/pdf/10.1145/339331.339420 (403 Cloudflare, although Semantic Scholar marks it GOLD); eecs.harvard.edu/margo/papers/sigmetrics00/paper.pdf (200, HTML home page) |
| 13 | `Chang Varvello Hao Mukherjee "Can you see me now? A measurement study of Zoom, Webex, and Meet" IMC 2021 pdf` | arxiv.org/pdf/2109.13113 (200) | — |
| 14 | `Wong Tan Kumari Wey "Fairness and interactive performance of O(1) and CFS Linux kernel schedulers" pdf` | researchportal.hw.ac.uk publication page (200, no PDF) | ieeexplore (DOI 10.1109/ITSIM.2008.4631872, paywalled venue); ResearchGate/Academia copies (login-walled, not fetched) |
| 15 | `paper measurement software video decoding CPU time per frame desktop player VLC mpv ffmpeg energy characterization Linux` | arxiv.org/pdf/2209.10283 (200); arxiv.org/pdf/2204.10151 (200) | remaining hits were vendor/blog pages |
| 16 | `Linux Audio Conference proceedings paper round-trip latency measurement JACK ALSA PulseAudio period size pdf` | lac.linuxaudio.org/2011/?page=program (200) → papers/46.pdf (200, Cucinotta et al.) and papers/45.pdf (200, Henningsson "FluidSynth real-time and thread safety challenges" — fetched, set aside: no measurements of playback cadence or CPU read in it, not a candidate) | lac.linuxaudio.org/2019/doc/kuhr.pdf not fetched (IEEE 1722 AVTP sync, off-topic by title) |
| 17 | `keystroke inter-key interval distribution log-normal ex-Gaussian free text typing large dataset paper desktop keyboard` | Heliyon 2021 via Europe PMC XML (PMC8606350, 200); arxiv.org/pdf/1912.02736 (200) | pmc.ncbi.nlm.nih.gov/articles/PMC8606350/pdf/main.pdf (200 but a "Preparing to download" bot-check page) |
| 18 | `Cucinotta "Low-latency audio on Linux by means of real-time scheduling" LAC 2011 pdf` | see #16 | — |
| 19 | `Chukharev-Hudilainen "Pauses in spontaneous written communication: a keystroke logging study" Journal of Writing Research pdf` | Wayback 2020 copy of lib.dr.iastate.edu/cgi/viewcontent.cgi?article=1119&context=engl_pubs (200) | lib.dr.iastate.edu/cgi/viewcontent.cgi?… (200, HTML redirect page); jowr.org/index.php/jowr/article/view/682 (200, JS single-page app, no PDF link) |
| 20 | `keystroke data programming students inter-keystroke interval distribution dataset paper code editing (Leinonen OR Blackbox OR "keystroke-level")` | juholeinonen.com/assets/pdf/leinonen2019keystroke.pdf (200); files.eric.ed.gov/fulltext/EJ1383373.pdf (200) | — |
| 21 | `web browser input event handling CPU time per keystroke measurement paper desktop Chromium Firefox event latency characterization` | none academic (online latency-test tools, Mozilla Hacks blog) | — |
| 22 | `Linux scheduler trace desktop GUI application wakeup interval CPU burst distribution interactive workload characterization paper` | none academic (perfetto/schedviz docs, blog) | — |
| 23 | `text editor keystroke latency measurement study paper end-to-end latency typing Casiez OR "keyboard to display"` | dl.acm.org/doi/fullHtml/10.1145/3544549.3585779 (Wimmer et al. CHI EA 2023; see #24) | — |
| 24 | `"Measuring the Latency of Graphics Frameworks on X11-Based Systems" CHI 2023 pdf Regensburg` | hci.ur.de publication page (200) → epub.uni-regensburg.de/54287/1/framework-latency-authorversion.pdf | epub.uni-regensburg.de PDF (401 Unauthorized, direct and via Wayback); dl.acm.org fullHtml not fetched (Cloudflare on dl.acm.org PDFs above) |
| 25 | `academic paper PulseAudio OR PipeWire measurement wakeups CPU usage energy audio playback Linux desktop "timer-based scheduling"` | none academic | — |
| 26 | `paper measurement video player mpv OR VLC OR GStreamer frame timing CPU utilization per frame Linux desktop playback decode thread trace` | none academic (github issues, vendor pages) | — |
| 27 | `Zoom OR Teams OR "Google Meet" desktop client CPU utilization measurement study encode decode threads paper` | arxiv.org/pdf/2210.09651 (200) | — |
| 28 | `Salthouse 1986 "Perceptual, cognitive, and motoric aspects of transcription typing" Psychological Bulletin pdf interkey interval` | — | researchgate.net profile PDF (403 "Access restricted"); psycnet.apa.org (paywalled) |
| 29 | `PipeWire academic paper arXiv OR ieeexplore OR acm "PipeWire" audio latency evaluation Linux measurement 2022 OR 2023 OR 2024 OR 2025` | none academic | — |
| 30 | `mouse movement event timestamps dataset inter-event interval distribution desktop users paper (Balabit OR "mouse dynamics" OR "pointer events") raw timestamps` | BEHACOM (Data in Brief 2020) via Europe PMC XML (PMC7270191, 200) | ReMouse / "mouse movement information" datasets on IEEE DataPort not fetched (dataset pages, S3's class) |
| 31 | `paper measurement Wayland OR X11 compositor frame scheduling GTK OR Qt application repaint cadence vsync input latency Linux desktop trace` | none academic (blogs) | — |

### 1b. Direct fetches not covered above (venue = host; all 2026-09-13)

| Host / URL | Result |
|---|---|
| userinterfaces.aalto.fi/136Mkeystrokes/resources/chi-18-analysis.pdf | 200 (Dhakal 2018) |
| userinterfaces.aalto.fi/typing37k/resources/Mobile_typing_study.pdf | 200 (Palin 2019) |
| usenix.org/legacy/events/osdi02/tech/full_papers/flautner/flautner.pdf | 200 (Vertigo) |
| cs.cmu.edu/~maxion/pubs/KillourhyMaxion09.pdf | 200 |
| cs.technion.ac.il/~dan/papers/ClockRes03SIGMETRICS.pdf | 200 |
| web.archive.org/web/2015id_/http://web.eecs.umich.edu/~tnm/papers/asplos00.pdf | 200 (Flautner 2000) |
| web.archive.org/web/20170830230307id_/https://www.usenix.org/legacy/publications/library/proceedings/osdi96/full_papers/endo/endo.txt and …230310id_/…/endo.ps | 200, 200 (no PostScript-to-PDF tool in this environment; text copy read) |
| ebi.ac.uk/europepmc/webservices/rest/PMC8606350/fullTextXML and …/PMC7270191/fullTextXML | 200, 200 |
| api.semanticscholar.org/graph/v1/paper/DOI:… (6 DOI lookups) | 200 each; /paper/search (4 title queries) 429 Too Many Requests |
| web.archive.org/cdx/search/cdx?url=eecs.umich.edu/~blakeg/* | connection reset by peer |

## 2. Candidates

Coverage key: for each topic, "covers" names object, unit, statistic, scope and population; otherwise "does not cover". "One observation?" states whether the source is a single population/trace/run and whether machine, application/subject and window are named.

---

### S1-flautner2000

**Citation.** Krisztián Flautner, Rich Uhlig, Steve Reinhardt, Trevor Mudge. "Thread-level parallelism and interactive performance of desktop applications." ASPLOS-IX (Nov 2000), pp. 129–138.

**Copy read.** Author preprint headed "Thread level parallelism and Interactive performance of desktop applications - ASPLOS 2000 / August 21, 2000", 10 pages. URL: https://web.archive.org/web/2015id_/http://web.eecs.umich.edu/~tnm/papers/asplos00.pdf (Wayback snapshot of the umich author copy). Accessed 2026-09-13. Local: `sources/S1-flautner2000/paper.pdf`. SHA-256 `f1b33e4bec0c6b81e35ff9081a4bcde34c13788c0fa3aab697375cc44802bf18`.

**Passages.**

- p. 3, Fig. 3 "Benchmarking environment configuration": "Dell Precision WorkStation 410 / Two 450Mhz Pentium II / 512K L2 Cache / 512M RAM / Matrox Millennium II AGP 4M / Linux Mandrake 7 / Modified 2.3.99-pre3 kernel / XFree86 3.3.6 / Helix GNOME 1.2 / glibc 2.1.3 C library"
- p. 3, §3: "Response time (TR) is the length of time between the initiation and completion of an interactive event, which we also refer to as the length of an interactive episode."
- p. 4, §3.1: "The start of an interactive episode is signified by the GUI controller (X server in our case) sending a message through a socket to another task. … The end of the episode is reached when all the following conditions are met for tasks in the task set: • No tasks are executing. • Data written by the tasks have been consumed. • No task was preempted the last time it ran (i.e., all gave up time on their own by blocking in a system call). • No tasks are blocked on I/O."
- p. 5, §3.2: "The data presented in this paper are averages of seven benchmark runs in each configuration. All benchmarks were run by a live user."
- p. 5, Table 1 "Linux benchmark descriptions and characteristics" (Benchmark / Version / Description / Dual TLPie / Dual TLPrun / Dual Idlerun / Uni Idlerun): "Acroread 4.0 Acrobat PDF file viewer 1.20 1.19 88% 87% / FrameMaker 5.5.6beta Document editor 1.35 1.33 93% 93% / Ghostview 3.5.8 PostScript and PDF file viewer 1.42 1.39 84% 84% / GIMP 1.1.22 The GNU Image Manipulation Program 1.26 1.24 88% 84% / Netscape 4.7 Web browser 1.34 1.28 90% 89% / Xemacs 21.1 patch 8 Text editor 1.26 1.21 93% 92% / Average 1.31 1.27 89% 88%"
- p. 7, §4.2: "While the majority of the episodes are very short and are in the few tenths of a millisecond range, only a small portion of the time is spent in episodes corresponding to them."
- p. 7, Table 3 "Episode distribution (dual processor)", columns [0ms,1ms) % of episodes / % of time; [1ms,10ms); [10ms,100ms); [100ms,inf): "Acroread 92.69% 5.75% 4.11% 3.52% 1.13% 11.89% 2.08% 78.85% / FrameMaker 72.10% 2.87% 17.60% 6.98% 8.58% 42.11% 1.72% 48.04% / Ghostview 89.87% 2.24% 6.73% 2.22% 0.76% 6.7% 2.64% 88.85% / GIMP 87.93% 2.7% 10.19% 5.89% 0.32% 0.64% 1.57% 90.77% / Netscape 89.98% 3.56% 8.62% 13.88% 0.98% 31.43% 0.42% 51.13% / Xemacs 65.01% 4.78% 34.36% 86.01% 0.63% 9.21% 0% 0%"
- p. 7, Table 4 "TLP and episode length distribution (dual processor)", per bucket TLPie / avg. length (ms): "Acroread 1.38 0.25 1.19 3.47 1.20 42.76 1.18 153.66 / FrameMaker 1.38 0.30 1.20 2.94 1.36 36.42 1.37 207.72 / Ghostview 1.30 0.23 1.18 3.10 1.33 83.39 1.43 315.85 / GIMP 1.43 0.17 1.22 3.28 1.35 11.49 1.26 328.83 / Netscape 1.70 0.07 1.16 2.73 1.41 55.59 1.33 210.60 / Xemacs 1.87 0.07 1.24 2.52 1.14 14.68 N?A N/A"
- p. 8: "Examples of the short episodes include: • Moving the mouse and updating its position. • Updating the appearance of the cursor. • Handling window focus changes. • Handling keyboard events."
- p. 8: "Moreover, in all cases the interactive episodes appear to be very CPU bound, with zero or close zero idle time."
- p. 8, §4.3: "Our measurements show that the delay between the hardware event and event dispatch can vary from a few tenths to hundreds of milliseconds."
- p. 9, §4.4: "We used a very simple MP3 player called mpg123 (version 0.59r) along with the esd sound daemon. … We measured 1.02 TLP and 95% idle time when running music playback by itself." and "MP3 playback is periodic and has no inherent concurrency (it is not threaded, just a single task)".
- p. 7, §4.1: "Most Linux applications are not threaded; concurrency emerges from simultaneously running multiple processes. The only applications from our benchmarks that actually used threads (through the LinuxThreads API) were Netscape and GIMP. … most of the TLP was achieved by running the application thread concurrently with the user interface threads: mostly with the X server but also with the other GUI tasks (such as the window manager, desktop applets, etc.)."

**Coverage.**
- T1: does not cover (no inter-arrival statistics; only states that "the amount of time between events varies from one run to the other", p. 5).
- T2: covers — object: interactive episode (all CPU work of the task set triggered by one X event, from event dispatch to quiescence); unit: wall-clock ms on a dual 450 MHz Pentium II; statistic: fraction of episodes and fraction of episode time in four log buckets (<1, 1–10, 10–100, ≥100 ms) plus mean length per bucket (Tables 3–4) — this directly gives how often one event's work exceeds 1, 10, 100 ms; scope: six Linux GUI applications listed in Table 1, X11/GNOME 1.2, kernel 2.3.99-pre3; population: one user, seven runs per configuration, averaged.
- T3: covers partially — wake structure is characterised as GUI-event-triggered episodes detected via X-server socket communication (p. 4); thread structure: "Most Linux applications are not threaded" and only Netscape and GIMP used LinuxThreads (p. 7); background periodic task (mpg123+esd) is "periodic … a single task" (p. 9). No wake-gap distribution; no timer-driven wakeups of the GUI apps themselves quantified.
- T4: covers marginally — mpg123 + esd playback alone: "1.02 TLP and 95% idle time" (p. 9), i.e. ~5% CPU share, no period stated.
- T5: does not cover.
- T6: covers — per-class episode-length distributions differ (Table 3: Xemacs has 0% of episodes ≥100 ms and 86% of time in 1–10 ms episodes; GIMP/Ghostview/Acroread have >78% of time in ≥100 ms episodes; Netscape/FrameMaker intermediate). Classes present: PDF viewer, document editor (FrameMaker), PS viewer, image editor (GIMP), browser (Netscape), text editor (Xemacs). No mail client, no video editor, no office writer other than FrameMaker.
- T7: not this reader's topic.

**One observation?** Yes: one machine (named), one OS build (named), six applications (named with versions), one user, seven runs; the window is a scripted-by-hand session per benchmark, length not stated.

---

### S1-flautner2001

**Citation.** Krisztián Flautner, Steve Reinhardt, Trevor Mudge. "Automatic performance setting for dynamic voltage scaling." MobiCom 2001 (July 2001); journal version Wireless Networks 8, 507–520 (2002).

**Copy read.** Author preprint headed "Automatic Performance Setting for Dynamic Voltage Scaling / May 30, 2001", 12 pages. URL: https://web.archive.org/web/2015id_/http://web.eecs.umich.edu/~tnm/papers/mobicom01.pdf. Accessed 2026-09-13. Local: `sources/S1-flautner2001/paper.pdf`. SHA-256 `99304253d71324ee056a49203e21ea8c295b465f582c244c18b44871166ff52e`.

**Passages.**

- p. 4, Fig. 4 caption: "Cumulative interactive episode length distributions. Left line shows the cumulative number, right line the cumulative percentage of time spent in interactive episodes whose lengths are less than or equal to the time specified on the x axis. The x axis is drawn using a logarithmic scale. Vertical lines from right to left: a) 50ms, b) 12.5ms and c) 5ms." (panels: Acrobat Reader, FrameMaker, Ghostview, Xemacs; x axis 1e-05 to 1 s)
- p. 5: "These graphs show that while most episodes are very short, the vast majority of time is actually spent in a small fraction that correspond to the long episodes. For example, in Ghostview, 92% of the time is spent in 4% of the episodes. This distribution holds true on the Xemacs benchmark as well, however in this case even the relatively long episodes fall under the perception threshold. Xemacs is an example of an application where one could run almost all of its interactive episodes in the lowest performance level without ever exceeding the perception threshold."
- p. 4, §3.2.1: "A case in point is the Linux esd sound daemon, which wakes up periodically to check for sound playback requests and to send data to the sound card. If esd's playback buffer is not empty, it sends some of the data to the sound card. If the buffer is close to being empty, it wakes up and unblocks the music decoders (e.g. MP3 players), which causes them to generate the next few frames of data."
- p. 3, §3.2: "If a task exhibits only a small amount of variation in period length over the last n runs (< 5%), then we treat it as a periodic task."
- p. 7, §4.3: "Our studies in [3] have shown that even lightweight background activity, such as MP3 playback, extends the duration of perceptible interactive episodes by an average of 14%."
- p. 7, §5: "Our simulator is driven by traces collected using a modified Linux kernel (2.3.99-pre3) running on a Dell Precision workstation 410, with only one of the two Pentium II 450Mhz processors enabled (512M RAM). The software environment was Mandrake Linux 7 with Helix Gnome 1.2. The traces used in this study are the same as the uniprocessor traces used in [3]. All benchmarks were run by a live user. … in this paper we only use a single run for each simulation."
- p. 10, §6.2: "We have pointed out that the majority of interactive episodes are very short (less than 1ms) and that very little time is spent in those episodes (<5%)."
- p. 8, Table 1 (XSB, 50 ms threshold), "Performance transitions" column without MP3: "Acrobat Reader 543 / FrameMaker 155 / Ghostview 510 / GIMP 919 / Netscape 1026 / Xemacs 381".

**Coverage.**
- T1: does not cover.
- T2: covers — object: interactive episode length (uniprocessor traces of the same six applications as S1-flautner2000); unit: seconds on log axis, 10 µs to 1 s; statistic: cumulative count and cumulative time distributions (Fig. 4, four applications) with the summary "majority … less than 1ms" and "<5%" of time (p. 10) and "92% of the time is spent in 4% of the episodes" for Ghostview (p. 5); scope: Linux 2.3.99-pre3, X11; population: one user, one run per benchmark.
- T3: covers partially — classifies wakeups into interactive vs periodic (producer/consumer) episodes; the periodic-task detector (<5% period variation) and the esd wake-and-unblock behaviour are described qualitatively (p. 3–4). No numeric wake-gap distributions.
- T4: covers qualitatively only — esd periodic wakeups and decoder unblocking (p. 4); no period or CPU-per-wake value.
- T5: does not cover.
- T6: covers — the CDF panels (Fig. 4) and the Xemacs-vs-Ghostview contrast (p. 5) distinguish a text editor from viewers/editors in episode-length distribution.

**One observation?** Yes — same machine and applications as S1-flautner2000, single run per benchmark, one user; window not stated.

---

### S1-flautner2002

**Citation.** Krisztián Flautner, Trevor Mudge. "Vertigo: automatic performance-setting for Linux." OSDI 2002 (Boston, Dec 9–11, 2002).

**Copy read.** USENIX proceedings PDF, 13 pages (page 1 = USENIX cover; body pages 2–13). URL: https://www.usenix.org/legacy/events/osdi02/tech/full_papers/flautner/flautner.pdf. Accessed 2026-09-13. Local: `sources/S1-flautner2002/paper.pdf`. SHA-256 `9bdf8c1c901b15ac04d831c51448e743e36bca3f002161e906bdc8bb1da3c61d`.

**Passages.**

- p. 6, §2.3: "We observed that the vast majority of interactive episodes are so short (sub millisecond) as to not warrant any special consideration. These short episodes are the results of echoing key presses to the window or moving the mouse across the screen and redrawing small rectangles. We found that a skip threshold of 5ms is good value for filtering short episodes without adversely impacting the worst case."
- p. 5, §2.2: "As a result of our strategy, work estimates for each task are recomputed on a varying interval with a mean of around 50-150ms (depending on workload), however, as a result of multiple tasks running in the system, there is actually a refinement of the work estimate every 5ms to 10ms."
- p. 8, §4: "Our measurements were performed on a Sony Vaio PCG-C1VN notebook computer using the Transmeta Crusoe 5600 processor running at 300Mhz to 600Mhz with 100Mhz steps. The operating system used is Mandrake 7.2 with a modified version of the Linux 2.4.4-ac18 kernel. The workloads used in the evaluation are the following: Plaympeg SDL MPEG player library [18], Acrobat Reader for rendering PDF files, Emacs for text editing, Netscape Mail and News 4.7 for news reading, Konqueror 1.9.8 for web browsing, and Xwelltris 1.0.0 as a 3D tetris-like game. The interactive shell commands benchmark is a record of a user doing miscellaneous shell operations during a span of about 30 minutes."
- p. 8, §4.1: "MPEG video playback poses a difficult challenge for performance-setting algorithms. While the algorithm puts a periodic load on the system, the performance requirements can vary depending on the frame's type."
- p. 9, Table 3 "Application-level statistics about the plaympeg benchmark playing various movies" (Length (s) / Idle / Sleep for LongRun then Vertigo): "Danse De Cable LongRun 247.1 54% 23% … 320x160 +audio Vertigo 27% 4% … / Legendary LongRun 19.4 33% 13% … 352x240 +audio Vertigo 24% 7% … / Red's Nightmare LongRun 49.1 48% 36% … 320x240 Vertigo 32% 13% … / Red's Nightmare LongRun 49.3 22% 15% … 480x360 Vertigo 18% 11% … / Roadkill Turtle LongRun 121.3 46% 19% … 304x240 +audio Vertigo 25% 4% … / Sentinel LongRun 35.6 28% 10% … 320x240 +audio Vertigo 19% 5% … / SpecialOps LongRun 60.8 30% 11% … 320x240 +audio Vertigo 20% 5%"
- p. 9: "The difference between the Idle and Sleep fields are that the first corresponds to the fraction of time spent in the kernel's idle loop—possibly doing housekeeping chores or just spinning—while the latter shows the fraction of time the processor actually spends in a low-power sleep mode."
- p. 12: "On some benchmarks such as Emacs, there is hardly ever a need to go fast and the interactive deadlines are met while the machine stays at its lowest possible performance level. On the other end of the spectrum is Acrobat Reader, which exhibits bimodal behaviour: the processor either runs at its peak level or at its minimum."
- p. 12, Fig. 8 "Fraction of time at different performance levels" (LongRun vs Vertigo, fraction of interactive-episode time at 300/400/500/600 MHz): Emacs Vertigo "95.57%" at the lowest level; Acrobat Reader Vertigo "40.37%" / "55.90%"; Konqueror Vertigo "38.49% 25.56% 14.75% 26.65%"; Netscape News Vertigo "60.70% 14.15% 22.22%".

**Coverage.**
- T1: does not cover.
- T2: covers qualitatively — keystroke echo and mouse-move episodes are "sub millisecond" (p. 6); no distribution given here (refers to [4]). Per-application performance-level demand of interactive episodes (Fig. 8) is a proxy, not CPU time.
- T3: covers partially — per-task work estimates refined every 5–10 ms because multiple tasks run (p. 5), i.e., an indirect statement that task switches occur at that granularity; no wake-gap distribution.
- T4: does not cover (audio present in the MPEG clips but not measured separately).
- T5: covers — object: MPEG video playback CPU demand under plaympeg (SDL smpeg) on a Crusoe 5600 300–600 MHz laptop; unit: fraction of run time idle/sleep and fraction of non-idle time at each MHz level; statistic: per-movie totals (Table 3, Table 4); scope: Linux 2.4.4-ac18, seven clips 304×240–480×360; population: one machine, one run per clip (after warm-up). No per-frame CPU distribution; cadence described as "periodic load" with per-frame variation by frame type.
- T6: covers — Emacs vs Acrobat Reader vs Konqueror vs Netscape News differ in the performance level their interactive episodes need (p. 12, Fig. 8); includes a mail/news client (Netscape Mail and News 4.7) and a browser (Konqueror).

**One observation?** Yes — one named laptop, named OS/kernel, named applications, one user; the shell benchmark window is "about 30 minutes", others unstated.

---

### S1-lorch2003

**Citation.** Jacob R. Lorch, Alan Jay Smith. "Using user interface event information in dynamic voltage scaling algorithms." Report No. UCB/CSD-02-1190, Computer Science Division, UC Berkeley, August 2002 (published at MASCOTS 2003).

**Copy read.** Berkeley technical report PDF, 14 pages. URL: https://www2.eecs.berkeley.edu/Pubs/TechRpts/2002/CSD-02-1190.pdf. Accessed 2026-09-13. Local: `sources/S1-lorch2003/paper.pdf`. SHA-256 `da217ae9dcc585c2fbcf13bc88a5fa2460ccb5f3d32e110c6a73d5db358ee744`.

**Passages.**

- p. 3, §1: "In this paper, we use several months' worth of trace data from each of eight users running Windows NT/2000."
- p. 4, §3.1: "We used VTrace, a Windows NT/2000 tracer that runs in the background on users' machines [LS00]. It collects time-stamped records describing events related to processes, threads, messages, disk operations, network operations, the keyboard, and the mouse. To limit trace volume, VTrace only collects the full set of events it can for sessions lasting 90 minutes at a time, after which it pauses for 2 hours. Also, it stops collecting the full set of events when the user is idle for 10 minutes, or when the user chooses to temporarily turn off tracing."
- p. 5, Table 1 "Trace information for all users": "Trace duration 8 months 7 months 4 months 15 months 3 months 19 months 2 months 9 months / Time full tracing on 435.8 hours 504.3 hours 83.0 hours 212.2 hours 134.9 hours 202.6 hours 106.9 hours 215.1 hours / … / CPU speed 450 MHz 300 MHz 500 MHz 200 MHz 500 MHz 400 MHz 433 MHz 350 MHz / CPU type Pentium III Pentium II Pentium III Pentium Pro Pentium III Pentium II Celeron Pentium II / … / Windows version NT 4.0 SP 6 NT 4.0 SP 4 NT 4.0 NT 4.0 SP 3 2000 SP 1 NT 4.0 SP 4 2000 SP 1 NT 4.0 SP 4"
- p. 5, §3.3: "We consider a user interface event to occur when a thread receives a message representing either a keystroke (i.e., a key press or release), a mouse movement, or a mouse click. A user interface task is a task triggered by a user interface event. Note that such a task includes all work the system does in response to the event, not simply the time to handle the user interface device interrupt."
- p. 5, footnote 2: "The system samples the mouse position at some fixed rate, and will generate a message only if the position changes between two consecutive samples. It sends at most one message per sample period, no matter how much the mouse moved during the sampling period."
- p. 5, §4.1: "We find that the CPU time due to user interface events ranges from 5.6%–43.7%, with an average of 20.3%." and "A substantial fraction of total CPU time, especially for users with little time spent on user interface events, is due to timer messages. An application typically uses timer messages to establish a periodic operation; for example, if it must take some action every 50 ms, it arranges for the delivery of a timer message every 50 ms. Some of this activity has important implied deadlines, such as media playback, and some does not, such as blinking the cursor. The average percentage of CPU time spent working on such timer messages is 35.1%."
- p. 6, Table 2 (percent of CPU time triggered by each event type; columns: User interface message / Timer message / Other message / Timer object / Other waitable object / Packet / Thread start / Session start / Timeout / APC): "1 29.5% 29.2% 3.6% 0.0% 23.4% 0.0% 2.9% 2.1% 2.7% 6.7% / 2 43.7% 27.2% 3.9% 0.0% 16.4% 0.1% 2.6% 0.9% 4.1% 1.2% / 3 7.3% 68.1% 2.5% 0.0% 6.4% 0.0% 0.2% 1.3% 11.6% 2.6% / 4 22.9% 28.0% 3.9% 0.0% 21.6% 0.0% 0.4% 2.2% 20.4% 0.7% / 5 10.9% 23.4% 4.9% 0.1% 29.8% 0.0% 6.1% 16.8% 7.9% 0.0% / 6 17.7% 46.9% 2.3% 0.0% 22.7% 0.1% 1.0% 5.3% 3.8% 0.3% / 7 5.6% 6.8% 1.5% 0.0% 39.0% 0.0% 0.2% 43.0% 3.9% 0.0% / 8 24.5% 51.1% 1.4% 0.0% 16.0% 0.1% 0.6% 1.7% 4.0% 0.6% / Avg 20.3% 35.1% 3.0% 0.0% 21.9% 0.0% 1.8% 9.2% 7.3% 1.5%"; caption: "100% corresponds to the total time the CPU spends running threads other than the idle thread; we assume that the CPU halts while the idle thread is running."
- p. 7, §4.3: "We find that 0.3–3.5% of user interface tasks wait for I/O, with an average of 1.3%. … In contrast, 5.1–18.1% of all mouse clicks, with an average of 12.3%, wait for I/O. … The rate of I/O among keystroke tasks is a modest 0.3–5.9% with an average of 3.1%, or only 0.1–2.6% with an average of 0.7% if we ignore network I/O."
- p. 8, §4.4: "For mouse movements, we assume a soft deadline of 50 ms, following [ES00]. … At this minimum speed, we complete 10 Mc (10 million CPU cycles) within 50 ms. For all users, this is above the 99th percentile, meaning this strategy would complete over 99% of tasks within the deadline. If we want to make 99.5% of all deadlines instead of 99%, we need 3.5–13.3 Mc".
- p. 8, §4.4: "Next, we consider keystrokes. … Users #1, 3, 4, 5, and 6 show relatively low CDF slopes beyond about 10.5 Mc. On the other hand, users #2, 7, and 8 show much steeper CDF slopes above 10.5 Mc. In other words, five of our users would probably not much mind if their processors ran at only 210 MHz before the deadline for all keystroke tasks, but three of our users would suffer significant changes in deadlines made".
- p. 8, §4.4: "With mouse clicks, we find general agreement among all users: the CDF slope is relatively high at and well beyond 10 Mc."
- p. 9, Fig. 1 caption: "The cumulative distribution function of CPU time required by various user interface event types for each user, but only above the 90th percentile" (axes: Megacycles 1–100 and Milliseconds 1–1000, log; series: Key presses/releases, Mouse moves, Mouse clicks, All user-interface events; eight panels, User #1–#8).
- p. 10, §4.6.1: "we find that by far the most common case, across all keys and users, is for key press processing time to be significantly different than key release processing time. Furthermore, key presses usually take longer to process than key releases."
- p. 11, Table 6 caption: "Average per-task energy consumption for various DVS algorithms operating on various users' keystroke events. Parenthetical information shows percent of deadlines made. All algorithms shown here other than 'No DVS' use an average pre-deadline speed of 400 MHz"; "No DVS" column: "4.577 mJ (99.86%) … 11.621 mJ (98.52%) … 5.973 mJ (99.88%) … 4.978 mJ (99.93%) … 8.380 mJ (99.58%) … 5.550 mJ (99.94%) … 13.515 mJ (98.56%) … 6.685 mJ (99.80%) … Avg 7.660 mJ (99.51%)".
- p. 11, §4.6.2: "For example, for iexplore for user #2, the standard deviation of left down event times is five times the mean, and for left up events it is almost 40 times the mean!"
- p. 11–12, §4.7: "The conclusion we draw from these results is that different applications have very different CPU requirements, even when handling the same type of user interface event. This holds for mouse movements, keystrokes, and mouse clicks, despite the fact that the operating system provides default handlers for many of these events."
- p. 13, §6: "Differences in the user, the application, the user interface event type, and even the category of event can have substantial effect on the CPU usage of a task."

**Coverage.**
- T1: does not cover directly (event counts and rates are not reported; mouse-move messages are noted to be rate-limited to the sampling period, p. 5 fn. 2).
- T2: covers — object: CPU time of the task triggered by one UI event (keystroke press/release, mouse move, mouse click), all dependent work included, I/O-waiting tasks excluded; unit: megacycles and ms (200–600 MHz assumed CPU); statistic: per-user CDFs above the 90th percentile (Fig. 1), tail thresholds (mouse moves: >99% under 10 Mc; keystrokes: knee ≈10.5 Mc for five users), share of CPU time attributable to UI events (avg 20.3%) vs timer messages (35.1%), per-event mean energy at 400/500 MHz (Tables 6–7); scope: Windows NT 4.0/2000, real desktop use; population: eight users, 83–504 h of full tracing each, over 2–19 months. This is the only long-window real-use per-event CPU distribution found. Not Linux.
- T3: covers — wakeup sources of all non-idle CPU time broken down by trigger type (Table 2): UI messages, timer messages, timer objects, other waitable objects, packets, thread starts, timeouts, APCs — per user; states timer messages establish periodic operations such as media playback and "blinking the cursor" (p. 5). No per-schedule runtime or wake-gap distributions.
- T4, T5: does not cover (media playback only as an example of timer-driven work).
- T6: covers — applications differ significantly in per-event CPU for all three event types (§4.7); PACE-Classify gain of 1.5% (keystrokes) / 0.5% (clicks) when separating by application and category (§4.8). Per-application tables are in the thesis [Lor01], not in this report.

**One observation?** No — eight users on eight named machines (Table 1), months-long windows; applications are named where discussed (iexplore, exceed, java, ssh, starcraft) but per-application distributions are deferred to [Lor01].

---

### S1-endo1996

**Citation.** Yasuhiro Endo, Zheng Wang, J. Bradley Chen, Margo Seltzer. "Using latency to evaluate interactive system performance." Proc. 2nd USENIX Symposium on Operating Systems Design and Implementation (OSDI '96), Seattle, Oct 28–31 1996, pp. 185–199.

**Copy read.** USENIX plain-text rendition of the paper (`endo.txt`, 62,329 bytes; figures described by captions only) and the PostScript original (`endo.ps`, not renderable here — no ghostscript in the environment). URLs: https://web.archive.org/web/20170830230307id_/https://www.usenix.org/legacy/publications/library/proceedings/osdi96/full_papers/endo/endo.txt and https://web.archive.org/web/20170830230310id_/https://www.usenix.org/legacy/publications/library/proceedings/osdi96/full_papers/endo/endo.ps. Accessed 2026-09-13. Local: `sources/S1-endo1996/paper.txt` SHA-256 `cfe8263de8adac0647ec24ac9726f705c2efce0a5e452e9e14137ad3bd3f6c35`; `sources/S1-endo1996/paper.ps` SHA-256 `3ab740ba802ec8058cb66e5dacf750e07a4451301721c754f06a186f78ca0b98`. Locators are section numbers (text copy has no page numbers).

**Passages.**

- §2: "A good example of unnoticeable wait time is the time required to service a keystroke when a user is entering text. Although the system may require a few tens of milliseconds to respond to each keystroke, such small 'waits' will be unnoticeable, as even the best typists require approximately 120 ms per keystroke [12]."
- §2.1: "We ran our experiments on a personal computer based on an Intel Premiere II motherboard, with the Intel Neptune chip set and a 100 MHz Pentium processor. Our machine was equipped with a 256KB asynchronous SRAM Level 2 cache, 32 MB of RAM, and a Diamond Stealth 64 DRAM display card."
- §2.3: "We select the value of N such that the inner loop takes one ms to complete when the processor is idle. In this way we generate one trace record per millisecond of idle time." and "The figure shows that the system spent approximately one ms generating samples A, B, D, and E, indicating that the system was idle during the periods in which these samples were generated, but spent 10.76 ms generating sample C. The difference, (10.76 - 1) or 9.76 ms, represents the time required to handle the event. Next, we used the traditional approach, recording one timestamp when the program received the character (i.e., after a call to getchar()) and a second timestamp after the character was echoed back to the screen. This measurement reported an event-handling latency of only 7.42 ms."
- §2.5: "Both versions of Windows NT show bursts of CPU activity at 10 ms intervals due to hardware clock interrupts."
- §2.6: "From Figure 4a, we can observe that the bursts of CPU activity for performing animation are aligned on 10 ms boundaries, suggesting that they are scheduled by clock interrupts."
- §5.1: "Our Notepad benchmark models an editing session on a 56KB text file, which includes text entry of 1300 characters at approximately 100 words per minute, as well as cursor and page movement." and "The cumulative latency graph shows that for all three systems, over 80% of the latency of Notepad is due to low-latency (less than 10 ms) events. These short-latency events are the keystrokes that generate printable ASCII characters. The remaining 20% of the total latency are due to the longer latency (at least 28 ms) keystrokes that cause 'page down' or newline operations."
- §5.2: "As with Notepad, we used a Microsoft Test script to drive the application and deliver keystrokes at a realistic rate, with each keystroke separated by at least 150 ms."
- §5.4: "Our task-oriented workload for Microsoft Word consists of text entry of a paragraph of approximately 1000 characters. It includes cursor movement with arrow keys and backspace characters to correct typing errors. The timing between keystrokes was varied to simulate realistic pauses when composing a document, and line justification and interactive spell checking were enabled." … "Compared to Notepad, Word requires substantially more processing time per keystroke, due to additional functionality such as text formatting, variable-width fonts and interactive spell checking." … "Our analysis indicates that Word uses a single system thread, but responds to input events and handles background computations asynchronously using an internal system of coroutines or user level threads." … "While the Test results showed that most events had latency between 80 and 100 ms, we measured a 32 ms typical latency for the hand-generated input. This difference in event latency was accompanied by a compensating difference in background activity. The hand-generated input showed a higher level of background activity than the Test-generated results. We also observed that carriage returns under the hand-generated input took longer than 200 ms to handle while the longest latency events we saw in the Test-generated runs were 140 ms."
- §6, Table 2 "Summary of interarrival distributions for Microsoft Word benchmark on Windows NT 3.51": "Threshold (in msec) / Number of events above threshold / Interarrival times Average (in sec) / Std. Dev. (in sec): 100 101 3.1 3.1 / 110 26 12.4 10.6 / 120 8 41.1 48.8".
- §1.1: "In addition, user interfaces tend to use features such as blinking cursors and interactive spelling checkers that have (or are intended to have) negligible impact on perceived interactive performance, yet may be responsible for a significant amount of the computation in the overall activity of an application."

**Coverage.**
- T1: covers only as scripted input rates ("approximately 100 words per minute"; keystrokes "separated by at least 150 ms"); no measured human inter-arrival distribution.
- T2: covers — object: CPU busy time per keystroke/event measured by idle-loop displacement (1 ms resolution), Windows NT 3.51/4.0/95 on a 100 MHz Pentium; statistic: Notepad — >80% of cumulative latency from <10 ms keystrokes, page-down/newline ≥28 ms; Word — typical 32 ms per keystroke under hand typing vs 80–100 ms under MS Test, carriage returns >200 ms; count of events above 100/110/120 ms in a 1000-event Word trace (Table 2); scope: Notepad, PowerPoint, Word; population: one machine, five scripted runs (SD 1–2%), seven hand-typed Word trials.
- T3: covers partially — clock-interrupt-aligned 10 ms bursts in the idle system and in window-maximize animation (§2.5, §2.6); Word single-threaded with internal coroutines and background activity (§5.4); blinking cursor and spell checker named as background computation (§1.1). Windows, not Linux; no wake-gap distribution.
- T4, T5: does not cover.
- T6: covers — Notepad vs Word per-keystroke cost differ by an order of magnitude on the same machine (§5.1 vs §5.4).

**One observation?** Yes — one named machine, named OS versions and applications; windows: 1300-character Notepad session, ~1000-character Word paragraph, 46-page PowerPoint task.

---

### S1-endo2000

**Citation.** Yasuhiro Endo, Margo Seltzer. "Improving interactive performance using TIPME." Proc. ACM SIGMETRICS 2000, pp. 240–251.

**Copy read.** Author PDF, 12 pages. URL: https://web.archive.org/web/2005id_/http://www.eecs.harvard.edu/~margo/papers/sigmetrics00/paper.pdf. Accessed 2026-09-13. Local: `sources/S1-endo2000/paper.pdf`. SHA-256 `8b57643ee1c31ddd4cda73b68623f289772d0de3f24d26bd6c2c628a5e94f257`.

**Passages.**

- p. 3, §3.2: "We implemented TIPME on BSD/OS 3.0 and X Free86 R6.3 running on Intel Pentium- or Pentium Pro-based personal computers."
- p. 4, §3.4: "At every other timer interrupt (every 20 ms under BSD/OS), we collect the status of all the processes in the system." p. 5: "We also record every context switch, sleep, and wake-up."
- p. 6, Table 2 "Latency and TIPME overheads. These latencies were measured using the Pentium cycle counter": "Event / Event Latency (incl. overhead) / TIPME overhead / %-age TIPME overhead: Moving a mouse pointer 0.3 ms 80 us 27% / Typing a character in a Xterm Window 2.0 ms 340 us 17% / Displaying the file menu in Netscape 3.0 470.0 ms 5100 us 1.1%"; text p. 6: "Table 2 shows some typical latencies and TIPME overhead for common events measured using a 100 MHz Pentium PC with 64 MB of memory."
- p. 7–8, §4.1.1: "The timing process sleeps for 100 ms, reads a word from a 4MB buffer, and records a timestamp … (The 100-ms delay was selected to model the inter-arrival time of fairly rapid keyboard input.)"
- p. 9, §4.2: "During the problem interval, the system spent up to a second updating the mouse pointer in response to the user's movement." and "MacKenzie and Ware showed that the speed and accuracy of mouse pointer movement does not change in a significant manner when the latency of mouse pointer update changes from 8.3 ms to 25 ms but that both speed and accuracy worsen in a measurable way when latency is increased to 75 ms [11]."
- p. 10, §4.2.1: "The measurement thread executes a loop that performs a computation that takes approximately 10 ms of CPU time followed by 50 ms of sleep time. We selected the duration of the computation and sleep intervals such that the priority of the measurement process would stay around 58 to approximate the priority level of the X Server when the system experienced the performance problem."
- p. 10: "It takes several hundred milliseconds for the scheduler to build up enough CPU usage history to adjust the compile job's priority to be lower than that of the X Server."

**Coverage.**
- T1: covers only as a modelling assumption ("100-ms delay … to model the inter-arrival time of fairly rapid keyboard input", p. 8).
- T2: covers — object: end-to-end event latency (kernel interrupt to X server display update) for three named events on BSD/OS + XFree86 on a 100 MHz Pentium; unit: ms; statistic: single "typical" values (mouse move 0.3 ms, xterm character 2.0 ms, Netscape 3.0 file menu 470 ms); population: one machine, typical values, no distribution. Unix/X11 but not Linux.
- T3: covers partially — describes the X11 input path (kernel → X server → client → X server → display, Fig. 2) and the X server being charged for client work; synthetic model of an X-server-like process as "10 ms of CPU … followed by 50 ms of sleep" (p. 10). No traces of real GUI wake structure.
- T4, T5: does not cover.
- T6: covers marginally — xterm keystroke (2.0 ms) vs Netscape menu (470 ms) on the same machine (Table 2).

**One observation?** Yes — one named test machine (100 MHz Pentium, 64 MB), deployed on two other named machines; applications named (xterm, Netscape 3.0); windows: 30–40 s ring buffers around user-reported problems.

---

### S1-lee1998

**Citation.** Dennis C. Lee, Patrick J. Crowley, Jean-Loup Baer, Thomas E. Anderson, Brian N. Bershad. "Execution characteristics of desktop applications on Windows NT." Proc. 25th ISCA (June 1998), pp. 27–38.

**Copy read.** Author PDF, 12 pages. URL: https://homes.cs.washington.edu/~baer/isca98.pdf. Accessed 2026-09-13. Local: `sources/S1-lee1998/paper.pdf`. SHA-256 `ced2e1653721401b683fb278937d321a706e2e434b325d14289b6b10ccdb10d5`.

**Passages.**

- p. 3, Table 1 (benchmarks, instructions executed in millions): "acrord32 Adobe Acrobat Reader 3.0 … 408 / netscape Netscape Navigator 3.1 web browser … 92 / photoshp Adobe Photoshop 4.0 … 1,511 / powerpnt Microsoft PowerPoint 7.0b … 209 / winword Microsoft Word 7.0 word processor. The benchmark simulates a user typing in seven paragraphs in an eight page document (document size is 29K). The benchmark then performs four search and replace commands on the document before saving a text version of the file. The interactive spell checker was turned on. 351"; caption: "The traces of these applications were produced on a dual Pentium Pro 200 system running Windows NT Workstation 4.0 service pack 3."
- p. 3: "For a small application, the traced application runs about 85-100 times slower than the original." and "However, 4 of the 5 desktop applications spent greater than 97% of their time in a single thread, suggesting that preemptions were rare."
- p. 4, Table 3 "Thread instruction distribution. Nearly all instructions are executed in the primary thread." (Application / # of Trds / Prim Trd(%) / Thread 2 (%) / Thread 3 (%) / Others (%)): "acrord32 3 98.63 1.37 0.00 - / netscape 4 99.58 0.26 0.16 0.00 / photoshp 5 97.16 2.84 0.00 0.00 / powerpnt 8 78.93 18.38 2.56 0.14 / winword 3 99.92 0.08 0.00 -"
- p. 2, §2.2: "Using VTune, we determined that the kernel driver responsible for graphics and windowing functionality (win32k.sys) constitutes from 15 to 30% of the application total instruction count for a given application run."
- p. 9, §4.3: "For example, a single mouse click in winword takes a few thousand instructions (and hence a few hundred conditionals) to process."

**Coverage.**
- T1: does not cover (scripted input via Visual Test; no timing).
- T2: covers marginally — one order-of-magnitude statement: "a single mouse click in winword takes a few thousand instructions" (p. 9); per-application total instruction counts of scripted sessions (Table 1) are not per-event.
- T3: covers thread structure — number of threads and instruction share of the primary thread per application (Table 3); win32k.sys 15–30% of instructions (p. 2). Windows NT 4.0, user-level instruction traces; no wake timing.
- T4, T5: does not cover.
- T6: covers — five applications (PDF viewer, browser, image editor, presentation, word processor) differ in thread count/primary-thread share (Table 3) and in module distribution (Table 4); no editor, mail client or video editor.

**One observation?** Yes — one named machine, named OS, five named applications, scripted runs; windows defined by the scripts in Table 1.

---

### S1-etsion2004

**Citation.** Yoav Etsion, Dan Tsafrir, Dror G. Feitelson. "Desktop scheduling: how can we know what the user wants?" NOSSDAV '04, Cork, June 16–18 2004 (ACM 1-58113-801-6/04/0006).

**Copy read.** Author PDF, 6 pages. URL: https://yoav.net.technion.ac.il/files/2016/05/Desktop04NOSSDAV.pdf. Accessed 2026-09-13. Local: `sources/S1-etsion2004/paper.pdf`. SHA-256 `2439f9106ec369dcafd167fc563aa1f9ebd27865480adb12cf86b39ef77b7ad6`.

**Passages.**

- p. 2, §2: "Our measurements were conducted on a 664 MHz Pentium 3 machine equipped with 256 MB RAM and a 3DFX Voodoo3 graphics accelerator with 16 MB RAM that supports OpenGL in hardware. The operating system is a 2.4.8 Linux kernel (RedHat 7.0), with the XFree86 4.1 X server. The clock interrupt rate was increased from the default 100Hz to 1,000Hz."
- p. 2: "• Classic interactive applications: The (traditional) Emacs and the (newer) OpenOffice text editors. During the test, editors were used for standard typing at a rate of about 8 characters per second." … "• Movie players: MPlayer and the Xine MPEG viewer, which were used to show a short video clip in a loop. While MPlayer is a single threaded application, Xine's implementation is multithreaded, making it a suitable representative of this growing class of applications [8]. In our experiments, audio output was disabled rather than sent to the sound card, to allow focus on interactions with the X server."
- p. 2, Fig. 2 "CPU consumption of different applications (when run alone) expressed as a percentage of the wallclock time." Bars (Application + X Server + Other stacked) labelled: "Emacs 0.2 / OpenOffice 2.6 / MPlayer 11.0 / Xine 1:1 11.6 / Xine 2:1 41.2 / Quake player 97.0 / Quake demo 99.4 / Kernel make 94.7 / Stressor 99.8".
- p. 3, §3.1: "Movie players such as Xine provide an especially interesting example: their CPU usage is proportional to the viewing scale. Showing a relatively small movie, taking about 13% of the screen space, required about 15% of the CPU resources for the player and X combined. Using a zoom factor of 2:1, the viewing size quadrupled to about half the screen, and the resource usage also quadrupled to about 60%."
- p. 3, §3.2: "An effective quantum is defined to be the period from when a process is allocated a processor until the processor is relinquished, either because the process has exhausted its allocated quantum, or because it blocks waiting for some event, or because a newly awakened process has a higher priority."
- p. 4, Fig. 3 caption: "Cumulative distribution function of the effective quanta when applications are run alone. (a) Editors have very short effective quanta. (b) Movie players also have short effective quanta, but this is similar to the profile of the kernel-make batch job. (c) Quake can consume all available CPU cycles, so when running in demo mode it behaves like a stressor. Both are occasionally interrupted by various system daemons, causing around 50% of the effective quanta to end prematurely." (x axis "Effective Quantum Duration [milliseconds]" 0–50; series (a) Emacs, OpenOffice; (b) Kernel Make, X (with Xine), MPlayer, Xine.)
- p. 3, Table 1 "Percent of context switches that are voluntary for the various applications.": "Emacs 99.6 / OpenOffice 99.1 / MPlayer 98.5 / Xine 83.1 / Quake user 14.3 / Quake demo 1.2 / Kernel make 81.6 / Stressor 0.5"
- p. 2: "When no such processes are present, Xine gets all the resources it needs (which is about 40% of the CPU)."
- p. 5: "Emacs only requires maybe 1% of the CPU resources, and gets it even under the default scheduler".
- p. 5: "The dispatch latencies of HuC-processes remains very low (≤1ms), regardless of the background load." (Fig. 7 series: Quake, OpenOffice, Xine, X (with Xine), MPlayer, Emacs.)

**Coverage.**
- T1: covers only as the driving rate: "standard typing at a rate of about 8 characters per second" (p. 2).
- T2: covers — object: total CPU share of an editor under 8 char/s typing (Emacs 0.2%, OpenOffice 2.6% of wall-clock, application + X server + other, Fig. 2), i.e. mean CPU per keystroke derivable as share/rate (not stated by the paper); statistic: mean over the test; scope: Linux 2.4.8 at 1000 Hz, XFree86 4.1, 664 MHz P3; population: one machine, one run per application. No per-event distribution.
- T3: covers — per-schedule runtime ("effective quantum") CDFs of Emacs, OpenOffice, MPlayer, Xine, X-with-Xine, kernel make, Quake (Fig. 3, 0–50 ms axis; editors "very short"); voluntary-context-switch fraction per application (Table 1). No wake-gap distribution; the paper argues CPU patterns cannot separate GUI from batch work.
- T4: does not cover (audio disabled).
- T5: covers — Xine and MPlayer CPU share on this machine: MPlayer 11.0%, Xine 1:1 11.6%, Xine 2:1 41.2% including X (Fig. 2); Xine multithreaded vs MPlayer single-threaded; frame-loss vs stressors (Fig. 1). No per-frame CPU or frame-rate value stated in this paper.
- T6: covers — editors (Emacs, OpenOffice) vs movie players vs game vs batch differ in CPU share and effective-quantum CDF; no browser, mail client, image or video editor.

**One observation?** Yes — one named machine, named kernel/X versions, named applications, one run each; window not stated.

---

### S1-etsion2006

**Citation.** Yoav Etsion, Dan Tsafrir, Dror G. Feitelson. "Process prioritization using output production: scheduling for multimedia." ACM Transactions on Multimedia Computing, Communications and Applications (TOMCCAP) 2(4), 2006.

**Copy read.** Author manuscript ("huc-trans.dvi", running head "ACM Journal Name, Vol. V, No. N, Month 20YY"), 28 pages; page locators are pages of this copy. URL: https://dants.github.io/papers/HuCsched06TOMCCAP.pdf. Accessed 2026-09-13. Local: `sources/S1-etsion2006/paper.pdf`. SHA-256 `a90f67fa4bb1cd7794ff792403caa90544614fc677d3e9f5267f5c05b6f19efe`.

**Passages.**

- p. 6, §3.3: "—Classic interactive applications: The (traditional) Emacs and the (newer) OpenOffice text editors. During the test, editors were used for standard typing at a rate of about 8 characters per second." … "—Movie players: MPlayer and the Xine MPEG viewer, which were used to show various video segments encoded with different standard frame rates. While MPlayer is a single threaded application, Xine's implementation is multithreaded … In our experiments audio output was disabled, to allow focus on interactions with the X server."
- p. 7, §4.2: "The intuition is that although HuC processes may exhibit large CPU consumption, their effective quanta probably remain very small due to their close interaction with I/O devices, and because they often need to use timer alarms to pace themselves (e.g. to generate the correct frame rate regardless of processor speed)."
- p. 8, Table I "Percent of context switches that are voluntary for the various applications.": "Emacs 99.6 / OpenOffice 99.1 / MPlayer 98.5 / Xine 83.1 / Quake user 14.3 / Quake demo 1.2 / Kernel make 81.6 / Stressor 0.5"
- p. 8, §4.3: "HuC processes (such as movie players) often relinquish the processor voluntarily, due to their dependency on I/O and timing devices, through which they communicate with the user in a paced manner."
- p. 22, §9.1: "Xine and the X server require about 60% of the CPU in this case." and "Emacs only requires about 1% of the CPU resources, and gets it even under the default scheduler".
- p. 5 (§3.2 by line 247 of the extraction): "export is performed by a daemon that wakes up every five seconds."

**Coverage.** Same measurements and machine as S1-etsion2004 (the journal version restates them; Fig. 1 is credited "from [Etsion et al. 2004]"). T1 (8 char/s driving rate), T2 (Emacs ≈1% CPU, editors' short effective quanta), T3 (effective-quantum CDFs, voluntary switch fractions, explicit statement that players pace themselves with timer alarms), T5 (Xine+X ≈60% at 2:1; frame-rate equalisation experiments with four Xine players, Figs. 8–10), T6 (editors vs players vs game vs batch) — as for S1-etsion2004. T4: does not cover (audio disabled).

**One observation?** Yes — same single machine/run population as S1-etsion2004; the multi-Xine experiments (Figs. 9–10) name the window: "Four Xine players of different sizes are started 5 minutes apart and run for 22 minutes each" (p. 24, Fig. 10 caption).

---

### S1-tsafrir2003

**Citation.** Yoav Etsion, Dan Tsafrir, Dror G. Feitelson. "Effects of clock resolution on the scheduling of interactive and soft real-time processes." Proc. ACM SIGMETRICS 2003, San Diego, June 10–14 2003, pp. 172–183 (ACM 1-58113-664-1/03/0006).

**Copy read.** Author PDF ("clock4.dvi"), 12 pages. URL: https://www.cs.technion.ac.il/~dan/papers/ClockRes03SIGMETRICS.pdf. Accessed 2026-09-13. Local: `sources/S1-tsafrir2003/paper.pdf`. SHA-256 `7443c88004c98f4098989a4505a3e9cb30cf12c2a8abd4a79d8f2e69e2f69911`. Text extraction drops every letter "c" (Type-3 fonts); pages 4 and 7–9 were rendered to `page4.png`, `page7.png`, `page8.png`, `page9.png` and read visually; every quotation below is transcribed from a rendered page.

**Passages.**

- p. 4 (rendered), §2.1: "a 2.4.8 Linux kernel (RedHat 7.0), with the XFree86 4.1 X server. … The default clock interrupt rate is 100 Hz. We modified the kernel to run at up to 20,000 Hz." and "The measurements were conducted using klogger, a kernel logger we developed that supports fine-grain events. … In our use, we log all scheduling-related events: context switching, recalculation of priorities, forks, execs, and changing the state of processes."
- p. 4 (rendered), §2.2: "• A classic interactive application — the Emacs text editor. During the test the editor was used for standard typing at a rate of about 8 characters per seconds. • The Xine MPEG viewer, which was used to show a short video clip in a loop. Xine's implementation is multithreaded, making it a suitable representative of this growing class of applications [11]. Specifically, Xine uses 6 distinct processes. The two most important ones are the decoder, which reads the data stream from the disk and generates frames for display, and the displayer, which displays the frames at the appropriate rate. The displayer keeps track of time using alarms with a resolution of 4 ms. On each alarm it checks whether the next frame should be displayed, and if so, sends the frame to the X server. If it is too late, the frame is discarded. If it is very late, the displayer can also notify the decoder to skip certain frames. In the experiments, audio output was sent to /dev/null rather than to the sound card, to allow focus on interactions with the X server."
- p. 8 (rendered), §6: "One of the Xine processes sets a 4 ms alarm, that is used to synchronize the video stream. In a 100 Hz system, the alarm signal is only delivered every 10 ms, because this is the size of a tick."
- p. 7 (rendered): "A notable exception is the X server when running with Xine (we used Xine because it intensively uses the X server, as opposed to Quake which uses DRI). As shown below in Section 6, when running at 100 Hz this application has quanta that are either extremely short (around 68% of the quanta), or 0.8–0.9 of a tick (the remaining 32%). Given the distribution of quanta, we should expect over 30% of them to include a tick and be counted. But the scheduler misses over 99% of them, and only bills about 2% of the consumed time! This turns out to be the result of synchronization with the operating system ticks. Specifically, the long quanta always occur after a very short quantum of a Xine process that was activated by a timer alarm. This is the displayer, which checks whether to display the next frame. When it decides that the time is right, it passes the frame to X. The X server then awakes and takes a relatively long time to actually display the frame, but just less than a full tick."
- p. 7, Fig. 4 (rendered): "The relationship between effective quanta durations and how much the process is billed, for different applications, using a kernel running at 100 Hz and at 1000 Hz." Panel labels: "53700 quanta xine / 21810 quanta quake / 2634 quanta emacs / 8205 quanta X (w/xine)" at 100 Hz and "73200 quanta xine / 30390 quanta quake / 4050 quanta emacs / 16005 quanta X (w/xine)" at 1000 Hz.
- p. 8 (rendered), Table 4 "Average quanta per second achieved by each application when running in isolation." (Application / @100Hz / @1000Hz): "Emacs 22.36 34.60 / Xine (all processes) 470.67 695.94 / Quake 187.88 273.85 / X Server (w/Xine) 71.35 148.21 / CPU-bound 28.81 38.97"
- p. 8 (rendered), Table 5 "CPU usage distribution when running Xine." (Application / @100Hz / @1000Hz): "Xine 39.42% 40.42% / X Server 20.10% 20.79% / idle loop 31.46% 31.58% / other 9.02% 7.21%"
- p. 8 (rendered), §5: "Xine operates according to two rules: it does not display a frame ahead of its time, and it skips frames that are late by more than half a frame duration." and "For Xine to display a movie at 60 Hz, the timing service needs a resolution of 4 ms."
- p. 8 (rendered), §6: "On our Linux system, the allocation for a quantum is 50 ms plus one tick. However, as we can see from Figures 4 and 6 (introduced below), our interactive applications never even approach this limit. They are always preempted or blocked much sooner, often quite soon in their first tick. In other words, the effective quantum length is very short. This enables the system to support more than 100 quanta per second, even if the clock interrupt rate is only 100 Hz, as shown in Table 4."
- p. 9 (rendered), Fig. 6: "Cumulative distribution plots of the effective quantum durations of the different applications." Panels: Xine, Emacs, CPU bound (alone), X (with Xine), Quake, CPU bound (with quake); x axis Milliseconds 0–30 (0–60 for CPU bound); series 100HZ (dashed) and 1000HZ (solid). Text p. 9: "As a result the maximal effective quanta of X and the other Xine processes are reduced to 4 ms, because they get interrupted by the Xine process with the 4 ms timer."

**Coverage.**
- T1: covers only as driving rate (8 char/s Emacs).
- T2: covers — object: per-schedule runtime (effective quantum) of Emacs under 8 char/s typing; unit: ms; statistic: CDF (Fig. 6, Emacs panel, essentially all quanta well under 10 ms at both clock rates) and quanta per second (Emacs 22.36/s at 100 Hz, 34.60/s at 1000 Hz, Table 4); scope: Linux 2.4.8 on a 664 MHz P3; population: one machine, single runs (Fig. 4 gives quantum counts: Emacs 2634 quanta at 100 Hz, 4050 at 1000 Hz).
- T3: covers — wakeups per second and per-schedule runtime CDFs for an editor (Emacs), a video player (Xine, all processes), the X server with Xine, a game and a CPU-bound process (Tables 4, Fig. 6); timer-driven wake structure of Xine (4 ms alarm displayer → X server) described (p. 7–8). No wake-gap distribution beyond the per-second counts.
- T4: does not cover (audio to /dev/null).
- T5: covers — Xine (6 processes; decoder + displayer) paced by a 4 ms alarm (content cadence, not display refresh); CPU share when playing a clip already in memory: Xine 39.42% + X 20.10% at 100 Hz (Table 5); Xine wakeups ≈470/s at 100 Hz, ≈696/s at 1000 Hz (Table 4); frame-skip rule; achieved vs desired frame rate at 100 vs 1000 Hz (Fig. 1). No per-frame CPU distribution.
- T6: covers — Emacs vs Xine vs X server vs Quake vs CPU-bound differ by an order of magnitude in quanta/s and in quantum CDF shape (Table 4, Fig. 6).

**One observation?** Yes — one named machine, named kernel/X, named applications (Xine, Emacs, Quake 3), single runs; window not stated (quantum counts imply tens of seconds to minutes).

---

### S1-dhakal2018

**Citation.** Vivek Dhakal, Anna Maria Feit, Per Ola Kristensson, Antti Oulasvirta. "Observations on typing from 136 million keystrokes." CHI 2018, Montreal, April 21–26 2018. doi 10.1145/3173574.3174220.

**Copy read.** Author PDF, 12 pages. URL: https://userinterfaces.aalto.fi/136Mkeystrokes/resources/chi-18-analysis.pdf. Accessed 2026-09-13. Local: `sources/S1-dhakal2018/paper.pdf`. SHA-256 `e5e72facf874deed7b18fcf87f827dce565a8c56f6f7a99de4564303301496a2`.

**Passages.**

- p. 3, "Task and Procedure": "The task was to transcribe 15 English sentences. Participants were shown instructions stating to first read through and memorise a sentence, then type it as quickly and accurately as possible."
- p. 3, Table 1 excerpts: "Age: mean 24.5 … Countries 218 68.05% from US, 85% native language English / Took a typing course 72% / … / Qwerty layout 98.1% / Physical keyboard 43.8% Rest on-screen (touch) / Laptop keyboard 54.15% or small physical keyboard"
- p. 3–4, "Key-event Instrumentation": "The timestamps were recorded via JavaScript's date.now() function. Expected precision on a regular computer is 10–15 ms. Local logging of timestamps is accurate to 1 ms with date.now(), and modern browsers pass key-events to listeners with an overhead of 1–3 milliseconds at worst. However, OS-level threading may delay timestamping by a few milliseconds. The largest source of variability stems from the USB polling rate, which under the standard is set to 10 ms".
- p. 4: "INTER-KEY INTERVAL (IKI) is the difference in timestamps between two keypress events. For IKI-based analysis, we removed keystrokes that were typed more than 5000 ms after the previous keystroke."
- p. 5: "The final dataset includes 136,857,600 keystrokes from 168,960 participants with, on average, about 810 keypresses per participant."
- p. 5: "INTER-KEY INTERVALS Average inter-key interval is 238.656 ms (SD = 111.6). A lower bound of about 60 ms can be observed. The IKI distribution shown in Figure 2 has a skewness of 1.98 and kurtosis measure of 7.1. The differences between typists are remarkable. For fast typists, the average IKI is ∼120 ms, with a standard deviation of only 11 ms, while slow typists have an IKI of over 480 ms, sometimes as high as 900 ms, with a large standard deviation: over 120 ms."
- p. 5: "KEYPRESS DURATIONS In contrast, the average keypress duration is only 116.24 ms (SD = 23.88) and is not shown to vary greatly even for slow typists (80–150 ms)."
- p. 5, Table 3 (All: mean, SD): "WPM 51.56 20.20 … IKI (ms) 238.66 111.60 … Keypr. duration 116.25 23.88 … Rollover ratio (%) 25.00 17.00"
- p. 8: "When rollover is used, keystrokes overlap by 30 ms, on average, and up to 100 ms."
- p. 10: "The dataset (N > 168,000) and the code for the test are released at http://userinterfaces.aalto.fi/136Mkeystrokes."

**Coverage.**
- T1: covers — object: inter-key interval between successive keydown events during sentence transcription in a web page; unit: ms (browser timestamps, ±10–15 ms precision, USB 10 ms polling); statistic: mean 238.66 ms, SD 111.6, skewness 1.98, kurtosis 7.1, lower bound ≈60 ms, histogram (Fig. 2), group means (fast ≈120 ms SD 11; slow >480 ms), keypress duration mean 116 ms; IKIs >5000 ms removed; scope: transcription only (no free composition, code, forms; pauses between bursts not analysed); population: 168,960 self-selected online volunteers, 43.8% physical keyboard, 54% laptop keyboard, remainder on-screen; dataset released (licence not stated in the paper).
- T2–T6: does not cover.

**One observation?** No — one large online population, one task; no machine named (participants' own devices; browser/OS not recorded in the paper); window = 15 sentences per participant.

---

### S1-feit2016

**Citation.** Anna Maria Feit, Daryl Weir, Antti Oulasvirta. "How we type: movement strategies and performance in everyday typing." CHI 2016, San Jose, May 7–12 2016, pp. 4262–4273. doi 10.1145/2858036.2858233.

**Copy read.** Author PDF, 12 pages. URL: https://userinterfaces.aalto.fi/how-we-type/resources/HowWeType_CHI16.pdf. Accessed 2026-09-13. Local: `sources/S1-feit2016/paper.pdf`. SHA-256 `fd305c7626abc9a232f358d03515ee0d7be158720c8505eba5e09fe37cb14b16`.

**Passages.**

- p. 3, Table 1 (prior touch-typist literature): "IKI easy prose (ms) 140 – [29] / IKI random strings (ms) 326 – [29]"; "Hand alternation … IKI (ms) 155 43 [23] / Finger alternation … IKI (ms) 194 45 [23] / Same finger … IKI (ms) 223 41 [23] / Letter repetition … IKI (ms) 176 26 [23]".
- p. 3: "We recruited 30 participants (17 female) ranging in age from 20–55, with a mean of 31." "Their performance, measured based on the collected data, ranged from 34–79 wpm."
- p. 4: "Keyboard logging: The typing software (implemented in Python) showed one stimulus at a time on the display. … The physical keyboard had a Finnish layout, similar to QWERTY (see Figure 7, 8). All keypresses were logged."
- p. 4: "From the typing log, we excluded outliers more than 2 SD from the mean inter-key interval. On average this was 4.4 % of the data (maximum 5.9 %)."
- p. 5: "We collected 93,294 keypresses over the three conditions, and 36,955 in the sentences condition."
- p. 6: "Average entry rate and IKI were found to be 57.8 WPM and 176.39 ms for touch typists, and 58.93 WPM and 168.91 ms for non-touch typists."
- p. 6, Table 2: "Avg. IKI (ms) 176.39 44.31 168.91 33.22 … - Random (ms) 382.31 122.56 399.36 133.70"
- p. 10, "THE HOW-WE-TYPE DATASET": "We are publicly releasing over 150GB of data, which includes: 1. Motion capture data … 2. Keypress data: key symbol, press and release time, and inter-key interval for every keypress".

**Coverage.**
- T1: covers — object: IKI on a physical keyboard during sentence transcription (and random-string transcription) in a lab; unit: ms; statistic: per-group means and SDs (touch 176.39 ± 44.31 ms; non-touch 168.91 ± 33.22 ms; random strings ≈382–399 ms), outliers >2 SD removed; scope: transcription, lab, Finnish/English; population: 30 participants; raw press/release timestamps released (150 GB, Zenodo record 4034268; licence not stated in the paper).
- T2–T6: does not cover.

**One observation?** No — 30 participants; one lab setup (Python logger, one physical keyboard, motion-capture lab); window = 50 sentences + 50 random strings + 50 mixed per participant.

---

### S1-roeser2021

**Citation.** Jens Roeser, Sven De Maeyer, Mariëlle Leijten, Luuk Van Waes. "Modelling typing disfluencies as finite mixture process." Reading and Writing 37, 359–384 (2024); published online 2021. doi 10.1007/s11145-021-10203-z.

**Copy read.** Springer open-access PDF, 26 pages (journal pages 359–384; page locators below are PDF pages with journal pages in parentheses). URL: https://link.springer.com/content/pdf/10.1007/s11145-021-10203-z.pdf. Accessed 2026-09-13. Local: `sources/S1-roeser2021/paper.pdf`. SHA-256 `7eb2298808ec062506910e19e40bcd205baf2ba7a4563a5107387a4156c03839`.

**Passages.**

- p. 1 (359), abstract: "tested these models on a random sample of 250 copy-task recordings. Our results illustrate that we can model copy typing as a mixture process of fluent and disfluent key transitions."
- p. 4 (362), Fig. 1 caption: "Example for mean as biased estimator for the inter-keystroke intervals (IKIs) for two participants … mean = 256 (SD = 98). The untransformed IKIs are shown in plot A and the log-scaled IKIs are shown …" and text p. 4: "positive skew in the keystroke data but is related to a bimodal tendency that can … density function shows two peaks in both participants. This mixture of short and …"
- p. 11 (369): "2 log-Gaussian (log-normal) distributions, of which one represents fluent typing—shorter IKIs—and the other represents disfluencies—longer IKIs."
- p. 12–13 (370–371): "The copy-task corpus consists of keystroke data collected via a Javascript-based web application as part of Inputlog 8 (available on www.inputlog.net) with the source code released on github.com/lvanwaes/Inputlog-Copy-Task and zenodo.org/record/2908966. … We used a random sample of 250 participants (175 females, 71 males, 4 unknown) from the age range of 18 to 25 years (median age = 22 years). In this analysis we focus on the difference between key-down presses rather than key lifts or combinations of key presses and lifts. Before analysis we excluded spaces and editing operations from the data."
- p. 13 (371): "In the consonants task, participants saw and copy-typed a single time four blocks of six consonants; i.e. 'tjxgfl pgkfkq dtdrgt npwdvf.' … In the LF-bigram task, participants typed three-word combinations seven times (een chaotische cowboy 'a chaotic cowboy' in the Dutch version)".
- p. 16 (374): "After accounting for process disfluencies, keystroke intervals were longer for the consonants task (429 msecs, PI: 356–515) compared to the LF-bigrams task (158 msecs, PI: 139–180). The slowdown for disfluencies was about four times longer for the consonants task. For the LF-bigrams task, the model determined a slowdown of 95 msecs (PI: 76–116) with a probability of 0.34 (PI: 0.31–0.38); for the consonants task we found a slowdown of 414 msecs (PI: 333–509) with a probability of 0.73 (PI: 0.66–0.80)."
- p. 15 (373): "Data, R scripts and Stan code are available on OSF (osf.io/y3p4d)."

**Coverage.**
- T1: covers — object: keydown-to-keydown IKI in a web-based copy task (Inputlog copy task, Dutch); unit: ms; statistic: two-component log-normal mixture — fluent component 158 ms (words) / 429 ms (consonant strings), disfluency slowdown 95 ms with probability 0.34 (words) / 414 ms with probability 0.73 (consonants); scope: transcription (copy) task, spaces and edits excluded; population: 250 participants aged 18–25; data and code on OSF (licence not stated in the paper).
- T2–T6: does not cover.

**One observation?** No — 250 participants; no machine named (participants' browsers); window = one copy of each string.

---

### S1-chukharev2014

**Citation.** Evgeny Chukharev-Hudilainen. "Pauses in spontaneous written communication: A keystroke logging study." Journal of Writing Research 6(1), 61–84 (2014). doi 10.17239/jowr-2014.06.01.3.

**Copy read.** Iowa State University repository PDF (26 PDF pages; journal page numbers printed on the pages, cited below as journal pages with PDF page in brackets). URL: https://web.archive.org/web/2020id_/https://lib.dr.iastate.edu/cgi/viewcontent.cgi?article=1119&context=engl_pubs. Accessed 2026-09-13. Local: `sources/S1-chukharev2014/paper.pdf`. SHA-256 `5fe288f7595acfa81881ed694467cd8103a2c1cf27e0eeda51bd1f75a3405bdf`.

**Passages.**

- Abstract [PDF p. 2]: "keystrokes made by chat users in a game were recorded. The distributions of the inter-key intervals were analyzed and fitted with ex-Gaussian distribution equation, and an argument for psycholinguistic interpretation of the distribution parameters is presented. This analysis leads to establishing a threshold of 500 ms for the identification of pauses in spontaneous writing."
- p. 70 [PDF 12]: "While JavaScript provides timestamps with a resolution of 1 ms, it is important to note that the temporal accuracy of keystroke logging depends on the programmatic approach used in the key-logging software (Frid, Wengelin, Johansson, & Johansson, …"
- p. 72 [PDF 14]: "Twenty-five team chatroom sessions and 18 common chatroom sessions were retained in the corpus, containing a total of 11,518 messages and over 68,000 tokens produced by 36 participants." … "Based on the questionnaire, only 8 out of 36 participants (22%) touch typed, others were keyboard gazers. … The typing rate averaged 110 keystrokes per minute (SD = 52) across participants."
- p. 73 [PDF 15]: "Specifically, we excluded keystrokes made to insert characters into the middle of the string (rather than append them to the end of the string), 'Backspace' and 'Delete' keys used to remove portions of the string, and keys pressed immediately after 'Backspace' or 'Delete.' Also discarded from the data were utterance-initial IKIs and those occurring after the input textbox had lost and regained keyboard focus (participant switching to another window)."
- p. 74 [PDF 16], Fig. 2: "a) Solid line -- empirical distribution of IKIs produced by Participant #7 (N = 37,002); dashed line -- ex-Gaussian distribution (μ = 92; σ = 45; τ = 249) b) Solid line -- empirical distribution of IKIs produced by Participant #14 (N = 1,824); dashed line -- ex-Gaussian distribution (μ = 72; σ = 41; τ = 192)"
- p. 76 [PDF 18], Table 2 "Ex-Gaussian Distribution Parameters for IKIs (in ms)." (Parameter / min / max / mean / SD across participants): "Mean of the Gaussian component (μ) 46.09 189.30 99.35 36.22 / SD of the Gaussian component (σ) 23.62 103.96 41.58 15.59 / Scale of the exponential component (τ) 156.12 549.17 267.71 81.50 / Estimated pause threshold (tpause) 357.51 810.28 491.79 119.36"
- p. 77 [PDF 19]: "Therefore, we propose to use the value of tpause = μ + τ + 3σ (4) as the threshold for observable pause. For practical purposes, it seems convenient to assume tpause = 500 ms. … We notice that this threshold is lower than the cutoff of 1--2 s used in composition studies (cf. Alves et al., 2007)."

**Coverage.**
- T1: covers — object: IKI during free composition (real-time multi-party chat in a quiz game), keydown timestamps from a web chat application; unit: ms; statistic: per-participant ex-Gaussian fits (μ mean 99 ms, σ 42 ms, τ 268 ms across 36 participants; example N = 37,002 IKIs for one participant), derived pause threshold ≈492 ms (range 358–810); edits and utterance-initial IKIs excluded; scope: free composition in chat, Russian; population: 36 participants, 22% touch typists, 110 keystrokes/min mean. No raw dataset release stated.
- T2–T6: does not cover.

**One observation?** No — 36 participants over 34 games; no machine named (participants' own computers); windows = chat sessions.

---

### S1-gonzalez2021

**Citation.** Nahuel González, Enrique P. Calot, Jorge S. Ierache, Waldo Hasperué. "On the shape of timings distributions in free-text keystroke dynamics profiles." Heliyon 7(11): e08413, Nov 2021. doi 10.1016/j.heliyon.2021.e08413. CC BY-NC-ND 4.0.

**Copy read.** Europe PMC full-text JATS XML of PMC8606350 (flattened to `fulltext.txt` for reading; locators are section numbers). URL: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8606350/fullTextXML. Accessed 2026-09-13. Local: `sources/S1-gonzalez2021/fulltext.xml`. SHA-256 `dc5be5e2cdbbde08735e08050ae6902c564fc5997166a7c6b2d6e0ad895922b6`.

**Passages.**

- Highlights: "Most keystroke timings in free text do not follow a gaussian law. • The three-parameter log-logistic distribution provides the best fit for hold times and flight times, over three datasets. • Other previously considered distributions, like the log-normal, provide a good fit but not as good as the log-logistic."
- §1: "But free text involves pauses and hesitations of many different kinds. Thinking, looking at the keyboard, resting, external interruptions, etc., occur invariably however short the sample might be, skewing the distribution, changing its shape, and adding heavy tails."
- §3.3: "The dataset LSIA is the same as previously used in [37] … It consists of typing sessions recorded during daily work in a healthcare environment for more than a year where the users, mostly doctors, worked rotating shifts and on duty. The dataset KM was used in [39] to evaluate if a free writing or a transcription task would produce similar enough profiles … The dataset PROSODY was used in [40] to study cues of deceptive intent reflected in typing pattern variations."
- §3.4: "A dataset containing CSV files with the timing features (hold times and flight times) of every keypress in the three source datasets — grouped by dataset, user, task, virtual key code, and feature — is made available both at the laboratory website, at IEEE DataPort [42], and as a Mendeley Data repository [43]. … Each file contains a single timing value per line, in miliseconds".
- §3.6: "All candidate distributions were evaluated against each alphanumeric profile with enough keystrokes (20 for two parameters and 40 for three), truncating them to 100 samples at most for performance considerations."
- §4.2: "Fitting flight times with two parameters, its lowest best match count for all datasets is around 50% in LSIA and above 65% in the rest, whereas the following candidate, the (two-parameter) log-normal distribution, achieves 28% in LSIA and less than 20% in the rest." and "The exgaussian distribution is not a very good choice for modeling flight time histograms."
- §4.4: "Two languages were considered in this study, English and Spanish, and no significant differences were found between them".

**Coverage.**
- T1: covers — object: per-user, per-key flight time (keydown-to-keydown) and hold time histograms in free composition and transcription on desktop keyboards (three public datasets: LSIA real operational healthcare work >1 year; KM free vs transcribed; PROSODY deceptive/truthful essays); unit: ms; statistic: distribution-family ranking (log-logistic best; log-normal second; ex-Gaussian poor), AICc per profile ≈4.5 nats hold / ≈6 nats flight; no parameter values (means) reported in the text; scope: free text and transcription, per-key profiles truncated to 100 samples; population: users per dataset in Table 2 (table body not present in the XML text). Companion timing dataset released (IEEE DataPort, Mendeley), per-key CSVs.
- T2–T6: does not cover.

**One observation?** No — three datasets by different authors; machines not named; windows not stated in the text read.

---

### S1-killourhy2009

**Citation.** Kevin S. Killourhy, Roy A. Maxion. "Comparing anomaly-detection algorithms for keystroke dynamics." DSN 2009, pp. 125–134.

**Copy read.** Author PDF, 10 pages. URL: https://www.cs.cmu.edu/~maxion/pubs/KillourhyMaxion09.pdf. Accessed 2026-09-13. Local: `sources/S1-killourhy2009/paper.pdf`. SHA-256 `40e0f9ae6416062c546f55d2b5c8e6439bab940b8b8f87fafc5b114a3818080e`.

**Passages.**

- p. 4, §4.2: "We set up a laptop with an external keyboard to collect data, and developed a Windows application that prompts a subject to type the password. … Whenever the subject presses or releases a key, the application records the event (i.e., keydown or keyup), the name of the key involved, and what time the event occurred. An external reference clock was used to generate highly accurate timestamps. The reference clock was demonstrated to have an accuracy of ±200 microseconds (by using a function generator to simulate key presses at fixed intervals)."
- p. 4, §4.3: "We recruited 51 subjects from within the university. Subjects completed 8 data-collection sessions (of 50 passwords each), for a total of 400 password-typing samples. They waited at least one day between sessions".
- p. 4, §4.4: "we extracted keydown-keydown times, keyup-keydown times, and hold times for all keys in the password. For each password, 31 timing features were extracted and organized into a vector. The times are stored in seconds (as floating-point numbers)."

**Coverage.**
- T1: covers — object: keydown-keydown, keyup-keydown and hold times for the 11 keystrokes of one fixed password (".tie5Roanl" + Enter); unit: seconds, ±200 µs reference clock; statistic: raw per-repetition vectors (no distribution summarised in the paper); scope: fixed-text password typing only (not composition, transcription of prose, code or forms; no pauses between bursts); population: 51 subjects × 400 repetitions. Dataset published with the paper (licence not stated in the paper).
- T2–T6: does not cover.

**One observation?** No — 51 subjects on one named apparatus (laptop + external keyboard, Windows application); windows: sessions of 1.25–11 minutes.

---

### S1-behacom2020

**Citation.** Pedro M. Sánchez Sánchez, José M. Jorquera Valero, Mattia Zago, Alberto Huertas Celdrán, Lorenzo Fernández Maimó, Eduardo López Bernal, Sergio López Bernal, Javier Martínez Valverde, Pantaleone Nespoli, Javier Pastor Galindo, Ángel L. Perales Gómez, Manuel Gil Pérez, Gregorio Martínez Pérez. "BEHACOM - a dataset modelling users' behaviour in computers." Data in Brief 31: 105767 (2020). doi 10.1016/j.dib.2020.105767. CC BY 4.0.

**Copy read.** Europe PMC full-text JATS XML of PMC7270191 (flattened; locators are section numbers). URL: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7270191/fullTextXML. Accessed 2026-09-13. Local: `sources/S1-behacom2020/fulltext.xml`. SHA-256 `c7880aa76a91786aa91fa5e76f331cb8db3370967b53f9007f5feb17d8f3ccfd`.

**Passages.**

- Abstract: "This paper details the methodology and approach conducted to monitor the behaviour of twelve users interacting with their computers for fifty-five consecutive days without preestablished indications or restrictions. The generated dataset, called BEHACOM, contains for each user a set of features that models, in one-minute time windows, the usage of computer resources such as CPU or memory, as well as the activities registered by applications, mouse and keyboard."
- §2.1: "The twelve individuals are right-handed male, with ages ranging from 20 to 45 years old. Eight of them use Windows as operating system, three Linux, and one both."
- §2.1: "it is important to highlight that features have been calculated from raw data grouped in time windows of one-minute to guarantee the privacy of sensitive data and avoid data leakages, especially in the case of keyboard data."
- Table 3 (keyboard features): "press_press_average_interval Average time elapsed between two consecutive keystrokes, measured in milliseconds. R press_press_stddev_interval Standard deviation on the time elapsed between two consecutive keystrokes, measured in milliseconds."
- Table 4 (mouse features): "mouse_action_counter_N Set of features that counters the number of events related to the mouse activity. N represents each possible action: 0, is a left button single click, 1 is a right button click, 2 is a left button double click, 3 is a scroll action, 4 is a mouse pointer movement, 5 is a drag or selection action (left press-movement-release), 6 is a middle button click." and "mouse_average_movement_duration Average duration of the mouse movements, measured in milliseconds."
- §2.2.1: "•Keyboard: Timestamp, key press, key release, key and application in foreground. •Mouse: –Mouse movement events: Timestamp, pointer x coordinate, pointer y coordinate, application in foreground." and "Furthermore, raw data is destroyed once features are collected and sent to the server."
- Table 6: "current_app_average_cpu Average percentage of CPU used by the current application during the time window." §2.2.2: "extracting the periodic measurements (every 5 seconds) about active applications and resources in use."

**Coverage.**
- T1: covers partially — object: keyboard and mouse activity during unrestricted real desktop use (Windows and Linux); unit: per-minute aggregates — mean and SD of press-press interval (ms), keystroke counts, mouse-event counts by type (moves, clicks, scroll, drag), mean movement duration; no raw per-event timestamps in the released data ("raw data is destroyed"); scope: real use, 55 days; population: 12 male users. Licence CC BY 4.0 (Mendeley Data 10.17632/cg4br62535.2).
- T2: covers marginally — per-minute average CPU % of the foreground application sampled every 5 s alongside keystroke counts; no per-event CPU.
- T3–T6: does not cover.

**One observation?** No — 12 users on their own (unnamed) machines; window 55 days (first/last timestamps given in §2.1).

---

### S1-belman2019

**Citation.** Amith K. Belman, Li Wang, S. S. Iyengar, Paweł Śniatała, Robert Wright, Robert Dora, Jacob Baldwin, Zhanpeng Jin, Vir V. Phoha. "Insights from BB-MAS – A Large Dataset for Typing, Gait and Swipes of the Same Person on Desktop, Tablet and Phone." arXiv:1912.02736 (2019).

**Copy read.** arXiv PDF v1, 14 pages. URL: https://arxiv.org/pdf/1912.02736. Accessed 2026-09-13. Local: `sources/S1-belman2019/paper.pdf`. SHA-256 `71f55270eb8c0b5108f2ee175f199d101c92d9ad3b2435b0913fb165ac4f3099`.

**Passages.**

- p. 1: "A total of 117 participants have provided data volun-" … "desktop, phone and tablet."
- p. 2: "• Desktops: Two identical desktop stations were setup. Each desktop station consisted of a standard QWERTY … and a Dell 21 inch monitor. The keystrokes, mouse …"; p. 2–3: "They had to use a popular web-browser (Mozilla Firefox) to browse for the best prices for the six items"; p. 3: "loggers were deployed on the desktop to log all the actions".
- p. 8, §3.1: "On an average each participant performed around 11,750, 8,950 and 9,400 keystrokes on desktop, tablet and phone respectively." and "We use a simple filter to remove any instances of keys that were held down for two seconds or more. We also remove instances of the inter-key pauses that are greater than two seconds."
- p. 8, Table 12 "Summary of keyhold feature statistics. All values are in milliseconds." Desktop µ(avg)/µ(std): "bspace 168 211 / space 114 57 / a 137 68 / e 123 58 / h 116 53 / i 119 61 / l 102 50 / n 122 63 / o 118 61 / r 129 63 / s 130 60 / t 116 54".
- p. 8: "Especially in case of flight1, which is also called the inter-key latency, we can see the values are almost doubled for many digraphs (d6, d10, d11 etc.)" [on hand-held devices relative to desktop].
- p. 10: "from the same 117 participants performing; a) typing activity, both fixed and free text, on desktop, tablet and phone".

**Coverage.**
- T1: covers — object: keystroke press/release events with timestamps on a desktop station (fixed and free text, plus a Firefox shopping task with mouse logging); unit: ms; statistic: per-key hold-time means and SDs (Table 12) and digraph flight-time means (Tables 13–16, not transcribed here); scope: lab tasks, IKIs >2 s removed; population: 117 participants (age 19–35), ~11,750 desktop keystrokes each; dataset described as released (terms not read in this copy).
- T2–T6: does not cover.

**One observation?** No — 117 participants on two identical named desktop stations; windows = the task list in Table 1.

---

### S1-csedm2023

**Citation.** John Edwards, Kaden Hart, Raj Shrestha. "Review of CSEDM Data and Introduction of Two Public CS1 Keystroke Datasets." Journal of Educational Data Mining 15(1), 2023.

**Copy read.** ERIC PDF, 31 pages. URL: https://files.eric.ed.gov/fulltext/EJ1383373.pdf. Accessed 2026-09-13. Local: `sources/S1-csedm2023/paper.pdf`. SHA-256 `fc4f15d8864656c2b2ce363ef4918de8705adee9059793d65a752e55ead316f4`.

**Passages.**

- p. 2: "The datasets are CSV log files of keystrokes and other events of CS1 students while working on their programming projects. … The first of these datasets, collected in a CS1 course in 2019, has 5 million unique events across 505 subjects and 5 assignments." footnotes: "2019 dataset: https://doi.org/10.7910/DVN/6BPCXN … 2021 dataset: https://doi.org/10.7910/DVN/BVOF7S"
- p. 3: "The second dataset, collected in a CS1 course in 2021, is smaller, with 1 million events".
- p. 17: "Our data, however, often contains multiple events per second, and so storing a snapshot at each event would result in prohibitively large files."
- p. 23: "original keystroke latencies (though pauses are clamped to be no longer than five seconds)."

**Coverage.**
- T1: covers as a dataset pointer — object: timestamped keystroke/edit events while writing Python in a browser IDE (Phanon) and PyCharm; statistic: none for inter-arrival in the paper; scope: code editing; population: 505 students (2019), 44 (2021); Harvard Dataverse DOIs. Distribution shapes not reported here.
- T2–T6: does not cover.

**One observation?** No — course cohorts, unnamed student machines.

---

### S1-leinonen2019

**Citation.** Juho Leinonen. "Keystroke Data in Programming Courses." Doctoral dissertation, University of Helsinki, Department of Computer Science, Series of Publications A, Report A-2019-8 (2019).

**Copy read.** Author PDF, 122 pages. URL: https://juholeinonen.com/assets/pdf/leinonen2019keystroke.pdf. Accessed 2026-09-13. Local: `sources/S1-leinonen2019/paper.pdf`. SHA-256 `8efd3d9bd0d7d61b9e2c268f06d05f7014403971ceafa54d828edb446a25a5b9`. Only pp. 3–4, 21–35 read.

**Passages.**

- p. 30–31 [PDF 30–31]: "The most relevant data for this thesis are edit events, which are collected when students edit … single character addition or deletion, which is the case when students are writing source code." and "A digraph latency is the time between two sequential keypresses, which form the digraph." (Fig. 3.1 caption)
- p. 31, Table 3.1 (illustrative example only): "L->O 137 ms / O->L 232 ms".

**Coverage.**
- T1: covers only as methodology — digraph latencies from IDE (NetBeans TMC plugin) edit events of programming students; no distribution of IKIs reported in the sections read (numbers on pp. 31–32 are worked examples, not data).
- T2–T6: does not cover.

**One observation?** No; population and windows are per included article, not read here.

---

### S1-palin2019 (off-platform: mobile)

**Citation.** Kseniia Palin, Anna Maria Feit, Sunjun Kim, Per Ola Kristensson, Antti Oulasvirta. "How do people type on mobile devices? Observations from a study with 37,000 volunteers." MobileHCI 2019.

**Copy read.** Author PDF, 12 pages. URL: https://userinterfaces.aalto.fi/typing37k/resources/Mobile_typing_study.pdf. Accessed 2026-09-13. Local: `sources/S1-palin2019/paper.pdf`. SHA-256 `dbb32524303409c1eb05f2eee285d69f15f95d7a3ab863ab5735089cb6f0ddbd`.

**Passages.** p. 5: "sentence (inter-key interval >5s). This yielded a dataset of 37,370 participants typing 15 sentences each." p. 6: "Words per minute. On average, participants typed at 36.17 WPM (SD = 13.22)".

**Coverage.** T1: mobile touch-screen typing only — does not cover desktop input; listed to record that it was read and excluded. T2–T6: does not cover.

---

### S1-cucinotta2011

**Citation.** Tommaso Cucinotta, Dario Faggioli, Giacomo Bagnoli. "Low-Latency Audio on Linux by Means of Real-Time Scheduling." Proc. Linux Audio Conference 2011 (LAC-11), paper 46.

**Copy read.** LAC proceedings PDF, 8 pages. URL: http://lac.linuxaudio.org/2011/papers/46.pdf. Accessed 2026-09-13. Local: `sources/S1-cucinotta2011/paper.pdf`. SHA-256 `1ad5f386f8ba18dc7a1af0325f09532efbd79bbaa68d011cb8e10bad9bfe1dea`.

**Passages.**

- p. 2, §4: "In JACK, an entire graph of end-to-end computations is activated with a periodicity equal to buffersize/samplerate and it must complete within the same period."
- p. 3, §5: "All experiments have been performed on a common consumer PC (Intel(R) E8400@3.00 GHz) with CPU dynamic voltage-scaling disabled, and with a Terratec EWX24/96 PCI sound card."
- p. 4: "JACK was using a buffer-size of 128 samples and a sample-rate of 96 kHz, resulting in a period of 1333µs."; Table 1 "Audio driver timing of JACK with no clients using the 4 different schedulers (values are in µs)." (Min / Max / Average / Std. Dev): "CFS 1268 1555 1342.769 3.028 / FIFO 1243 1423 1333.268 2.421 / AQuoSA 1279 1389 1333.268 2.704 / SHRUB 1275 1344 1333.268 2.692"
- p. 4: "In all of the following experiments, we used a 'fake' JACK client, dnl, constituted by a simple loop taking about 7% of the CPU for its computations. The audio processing pipeline of JACK is made up of 10 dnl clients, added one after the other. This leads to a total of 75% CPU utilisation."
- p. 4, §5.1.1: "rt-app has period of 40ms and execution time of 5ms. This configuration for rt-app makes it resemble the typical workload produced by a video (e.g. MPEG format) decoder/player, displaying a video at 25 frames per second."
- p. 5, §5.1.2: "This time JACK has a sample-rate of 48kHz and a buffer-size of 128 samples, resulting in a period of 2666µs, while rt-app has a period of 10ms and an execution time of 1.7ms. This could be representative of a VoIP application, or of a 100 Hz video player."
- p. 6, §5.1.3 and Table 3: "JACK configured to have only 64 samples as buffer-size and a sample-rate of 96kHz, resulting in 667µs of period." Table 3 "period and driver end time in the 3 cases (values are in µs)." (SHRUB / FIFO / CFS): "Min. 650.0 629.0 621.0 / Max. 683.0 711.0 1369.0 / Average 666.645 666.263 666.652 / Std. Dev 0.626 1.747 2.696 / Drv. End Min. 6.0 6.0 5.0 / Drv. End Max. 552.0 602.0 663.0"

**Coverage.**
- T4: covers — object: JACK (v2) server wake period on Linux with ALSA backend, driver activation interval; unit: µs; statistic: min/max/mean/SD of the period at 128/96 kHz (1333 µs) and 64/96 kHz (667 µs) under CFS, SCHED_FIFO, AQuoSA, SHRUB (Tables 1, 3); per-cycle CPU time of JACK+clients plotted (Fig. 1c, 5c) with synthetic clients of ≈7% CPU each; scope: JACK only (no PulseAudio/PipeWire, no media player), one named machine and sound card; population: single runs of 1 minute. Gives a fixed wake interval (buffer/rate) with a load-dependent CPU share — synthetic, not a playback path of a desktop player.
- T5: covers only as an assumed model — a video player modelled as period 40 ms / execution 5 ms (25 fps) and VoIP as 10 ms / 1.7 ms (p. 4–5); no measurement of a real player.
- T1, T2, T3, T6: does not cover.

**One observation?** Yes — one named PC and sound card, JACK 2, synthetic clients; 1-minute runs.

---

### S1-chang2021

**Citation.** Hyunseok Chang, Matteo Varvello, Fang Hao, Sarit Mukherjee. "Can You See Me Now? A Measurement Study of Zoom, Webex, and Meet." IMC '21 (Nov 2021); arXiv:2109.13113.

**Copy read.** arXiv PDF, 13 pages. URL: https://arxiv.org/pdf/2109.13113. Accessed 2026-09-13. Local: `sources/S1-chang2021/paper.pdf`. SHA-256 `639750300ce4c7f36b62180cdf4f3f5c5d9e102a3f68c3cc280be036fd7a6815`.

**Passages.**

- p. 4, §4.1: "Each cloud VM we deploy has 8 vCPUs (Intel Xeon Platinum 8272CL with 2.60GHz), 16GB memory and 30GB SSD. … The screen resolution of the VM's remote desktop is set to 1900×1200. We use the native Linux client for Zoom (v5.4.9 (57862.0110)), and the web client for Webex and Meet since they do not provide a native Linux client."
- p. 11, §7: "CPU usage. Fig. 19a shows boxplots of CPU usage sampled every three seconds for the experiment duration across all devices and scenarios. … We report CPU usage in absolute numbers, e.g., 200% implies full utilization of two cores. If we focus on the LM and HM scenarios for S10 (high-end), the figure shows that Zoom and Webex have comparable CPU usage (median of 150–175%), while Meet adds an extra 50%. When we focus on J3 (low-end device), CPU usage among the three clients is instead comparable (median around 200%)." and "Irrespective of the videoconferencing client, activating the device's camera (LM-Video-View) adds an extra 100% and 50% of CPU usage on S10 and J3, respectively."

**Coverage.**
- T5: covers partially — Linux (cloud VM) clients are used for QoE, but the CPU measurements are on two Android phones (S10, J3): whole-client CPU % sampled every 3 s, medians 150–200%, camera adds 50–100%; no per-frame CPU, no thread breakdown, no Linux-desktop CPU numbers.
- T1–T4, T6: does not cover.

**One observation?** CPU: two named phones, five repetitions per scenario; Linux side: named VM type and client versions, 4–5/2021.

---

### S1-macmillan2021

**Citation.** Kyle MacMillan, Tarun Mangla, James Saxon, Nick Feamster. "Measuring the Performance and Network Utilization of Popular Video Conferencing Applications." IMC '21; arXiv:2105.13478.

**Copy read.** arXiv PDF (latest version served on 2026-09-13; same bytes as v1), 14 pages. URL: https://arxiv.org/pdf/2105.13478. Accessed 2026-09-13. Local: `sources/S1-macmillan2021/paper.pdf`. SHA-256 `5c3ec6aa554fbce2d4df7678cdae70427ad5e53a1dfb37484b6aa6f93ad8adc7`.

**Passages.**

- p. 3: "We use two identical laptops, referred to as C1 and C2, representing the two VCA clients. Each laptop is a Dell Latitude 3300 with a screen resolution of 1366 × 768 pixels and running Ubuntu 20.04.1." and "We use Chrome (Meet) version 89.0.4389, Zoom client version 5.6.1, and Teams client version 1.4.00.7556." and "A pre-recorded talking-head video with a resolution of 1280 × 720 is used as the video source for the call, using ffmpeg."
- p. 5: "VCAs adapt the video quality by adjusting the encoding parameters to achieve a target bitrate estimate provided by the transport. Ideally, VCAs can adjust one or more of the following three parameters: • frames per second (FPS), • quantization parameter used in video compression, and • video resolution". "Within the 0.7–1 Mbps range, Meet adapts the bitrate primarily by adapting frames per second".

**Coverage.**
- T5: covers cadence only — object: encoded/received frames per second of Zoom, Meet and Teams native/browser clients on Ubuntu 20.04 laptops as a function of link capacity (WebRTC stats); no CPU measurement at all in the paper (search of the text for "CPU" found no match).
- T1–T4, T6: does not cover.

**One observation?** Yes — two named laptops, Ubuntu 20.04.1, named client versions; window per experiment not transcribed.

---

### S1-kumar2022

**Citation.** Rohan Kumar, Dhruv Nagpal, Vinayak Naik, Dipanjan Chakraborty. "Comparison of Popular Video Conferencing Apps Using Client-side Measurements on Different Backhaul Networks." arXiv:2210.09651 (2022).

**Copy read.** arXiv PDF, 14 pages. URL: https://arxiv.org/pdf/2210.09651. Accessed 2026-09-13. Local: `sources/S1-kumar2022/paper.pdf`. SHA-256 `b6cd5b9b87fcac4ceb0ef199562ce9bbb1d0064966a783ad6c809ef527b38c71`.

**Passages.**

- p. 3, Table 2 "Configuration of network and end-hosts": "CPU Intel i5-8265U Intel i5-8250U / RAM 16 GB 16 GB / OS Windows 10 Windows 10".
- p. 6, Fig. 8 caption: "Sender-side CPU load for WiFi with mic ON and camera ON. Microsoft Teams uses the highest amount of CPU resources on the sender-side. Google Meet and Zoom have a similar average CPU utilization, however, CPU load has lesser variation for Zoom." (y axis "CPU load in %" 15–35 over 800 s); Fig. 9 caption: "Receiver-side CPU load for WiFi with mic ON and cam ON. Microsoft Teams uses the least amount of CPU resources on the receiver-side." (y axis 6–18%).
- p. 6, §3.1.1: "On the sender-side, in addition to sending high payload, Microsoft Teams has the highest CPU load among all the apps for all test types."
- p. 13: "We conducted our measurements on laptop-class machines."

**Coverage.**
- T5: covers partially — whole-system CPU load (%) time series over ~800 s calls for Zoom, Teams, Meet as sender and receiver on two Windows 10 laptops (sender 15–35%, receiver 6–18%); not Linux, no per-frame or per-thread figures.
- T1–T4, T6: does not cover.

**One observation?** Yes — two named laptops, Windows 10; ~800 s per call.

---

### S1-kraenzler2020

**Citation.** Matthias Kränzler, Christian Herglotz, André Kaup. "A Comparative Analysis of the Time and Energy Demand of Versatile Video Coding and High Efficiency Video Coding Reference Decoders." (©2020 IEEE; arXiv:2209.10283, Sept 2022.)

**Copy read.** arXiv PDF v1, 6 pages. URL: https://arxiv.org/pdf/2209.10283. Accessed 2026-09-13. Local: `sources/S1-kraenzler2020/paper.pdf`. SHA-256 `7d9982e5554b57fbe39a9e15e1a5b13317157da557dcc1af8296b223226b23b8`.

**Passages.**

- p. 2, §II: "For our measurements, we use a desktop PC with an Intel i7-8700 CPU, which is a hexa-core CPU with a base frequency of 3.20 GHz. The measurements of RAPL can be accessed through the file system of an Unix-PC."
- p. 3, §III: "On average, the decoding time is increased by 62.03% and the decoding energy demand by 67.03% for AI. For LB, the bit rate is decreased by 31.01%, the decoding time is increased by 67.66%, and the decoding energy demand by 77.76%."

**Coverage.**
- T5: covers marginally — offline decoding time/energy of reference decoders (VTM-7.0 vs HM-16.20) on a Linux/Unix desktop; relative figures only; not a player, no cadence, no per-frame CPU values in the text read.
- T1–T4, T6: does not cover.

**One observation?** Yes — one named desktop, reference software, common test conditions.

---

### S1-herglotz2016 (off-platform: ARM Pandaboard)

**Citation.** Christian Herglotz, Yongjun Wen, Bowen Dai, Matthias Kränzler, André Kaup. "A Bitstream Feature Based Model for Video Decoding Energy Estimation." (©2016 IEEE; arXiv:2204.10151, Apr 2022.)

**Copy read.** arXiv PDF v1, 5 pages. URL: https://arxiv.org/pdf/2204.10151. Accessed 2026-09-13. Local: `sources/S1-herglotz2016/paper.pdf`. SHA-256 `b9c6b7ddac55f8cf0d17df38e60cfa193cc6c80115aca974707f1176d32029af`.

**Passages.** p. 3, §A: "We measure the energy consumption of the FFmpeg software decoder [18] which is readily capable of decoding all considered codecs. … The decoding device (DEC) is a Pandaboard [19] which features a smartphone like architecture using an ARM processor."

**Coverage.** T5: FFmpeg decoding energy per bitstream on an ARM development board — not a desktop player; recorded as read and excluded. T1–T4, T6: does not cover.

---

### Identified but not read (paywalled or blocked; no passages quoted)

- Geoffrey Blake, Ronald G. Dreslinski, Trevor Mudge, Krisztián Flautner. "Evolution of thread-level parallelism in desktop applications." ISCA 2010 (ACM 10.1145/1816038.1816000). Found by search #8; no open copy (umich host TLS failure; Wayback never archived; Cloudflare on ACM). Relevant to T3/T6 (thread structure of Windows 7 / OS X desktop applications).
- C. S. Wong, I. K. T. Tan, R. D. Kumari, J. W. Lam, W. Fun. "Fairness and interactive performance of O(1) and CFS Linux kernel schedulers." ITSim 2008, IEEE 10.1109/ITSIM.2008.4631872. Found by search #14; IEEE paywalled, Semantic Scholar "CLOSED". Relevance to T3 unverified.
- Raphael Wimmer et al. "Measuring the Latency of Graphics Frameworks on X11-Based Systems." CHI EA 2023, 10.1145/3544549.3585779. Found by searches #23–24; author version at epub.uni-regensburg.de returns 401. Relevance to T3 (toolkit latency under X11) unverified.
- Timothy A. Salthouse. "Perceptual, cognitive, and motoric aspects of transcription typing." Psychological Bulletin 99(3), 303–319 (1986). Search #28; APA paywall, ResearchGate 403. Its IKI figures are cited second-hand in S1-feit2016 Table 1 (140 ms easy prose, 326 ms random strings) — those are S1-feit2016's citations of [29] Shaffer & Hardwick and [23] Salthouse 1984, not a reading of Salthouse 1986.
- Dennis C. Lee et al., "Tracing and Characterization of Windows NT-based System Workloads" (Digital Technical Journal 1998) — surfaced by search #3, not fetched (studylib mirror only).

## 3. Not found

- **T1 — pointer-event inter-arrival distributions on a desktop.** No paper read reports a distribution of the time between successive mouse-move or click events reaching an application. S1-lorch2003 explains why the OS caps mouse-move message rate to its sampling period (p. 5 fn. 2) but gives no interval statistics; S1-behacom2020 releases only per-minute counts and mean movement durations. Searches #30 and #31 (mouse datasets; compositor scheduling) returned dataset pages (ReMouse, IEEE DataPort) that belong to S3's class and blogs. **T1 — free composition / code editing / form filling with distribution shapes:** free composition is covered by S1-chukharev2014 (chat, ex-Gaussian, 36 participants) and S1-gonzalez2021 (distribution family only, no parameters); code editing is covered only as dataset pointers (S1-csedm2023, S1-leinonen2019) with no IKI distribution in the pages read; form filling: no candidate (search #17 and #20 terms did not surface any).
- **T2 — per-wake CPU of GUI applications on Linux with a distribution.** The Linux evidence is S1-flautner2000/2001 (episode-length buckets on a 2000-era dual PII, six X11 apps) and S1-tsafrir2003/S1-etsion2004 (effective-quantum CDFs, Emacs at 8 char/s). No Linux measurement of a browser, mail client, office suite (other than OpenOffice's 2.6% CPU share and FrameMaker episodes), or video editor per input event was found; the only long-window real-use distribution is Windows NT/2000 (S1-lorch2003). Searches #21, #22 returned no academic hits for browser per-keystroke CPU or scheduler-trace characterisation of desktop GUI apps.
- **T3 — wake-gap distributions and toolkit scheduling.** No paper read gives inter-wake gap distributions for a GUI application, nor a measured account of how GTK, Qt, Electron/Chromium or LibreOffice VCL schedule work after an input event. Closest: S1-tsafrir2003 (quanta per second, effective-quantum CDF), S1-lorch2003 (CPU share by trigger type incl. timers, Windows), S1-endo1996 (10 ms clock-aligned bursts, Windows NT). Search #31 (compositor/frame scheduling) found only blogs.
- **T4 — PulseAudio / PipeWire / ALSA period defaults and per-wake CPU of an audio playback path.** No peer-reviewed or preprint measurement found (searches #10, #16, #25, #29). Only S1-cucinotta2011 (JACK, synthetic clients, wake period = buffer/rate at 667–2666 µs) and the qualitative esd description in S1-flautner2001; S1-flautner2000 gives mpg123+esd ≈5% CPU without a period.
- **T5 — per-frame CPU of a software-decoding desktop player (mpv, VLC, GStreamer) and per-thread CPU of a Linux conferencing client.** Not found (searches #15, #26, #27). Closest: S1-tsafrir2003/S1-etsion2004 (Xine on Linux 2.4: 4 ms pacing alarm, ≈40% player + ≈20% X CPU share, ≈470–696 wakeups/s), S1-flautner2002 (plaympeg idle/sleep fractions on a Crusoe laptop), S1-kumar2022 (whole-system CPU of Zoom/Teams/Meet on Windows 10 laptops), S1-chang2021 (Android CPU), S1-macmillan2021 (FPS only, Ubuntu).
- **T6 — a single study spanning text editor, office writer, mail client, browser, image editor and video editor.** No paper covers all six. Union of what was read: editor+office+browser+image editor (S1-flautner2000: Xemacs, FrameMaker, Netscape, GIMP; Windows NT: S1-lee1998 winword/powerpnt/netscape/photoshp); editor+mail/news+browser (S1-flautner2002: Emacs, Netscape News, Konqueror); no video editor in any source read. Per-application differences in per-event CPU are asserted statistically for Windows by S1-lorch2003 (§4.7) without per-application tables in the report read.
