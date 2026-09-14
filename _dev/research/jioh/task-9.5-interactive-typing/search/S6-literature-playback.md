# S6 — second literature pass on T4 (audio playback cadence) and T5 (video playback and conferencing cadence), Linux, 2010 onward

Reader: S6. Date of all searches, fetches and reads: 2026-09-14. Inputs read: `search/input.md` (topics T4 and T5 as written there; record format) and `search/S1-literature.md` in full (its queries were not repeated; its sources were not re-read).

Method notes. Every source below was fetched by `curl` and read from the fetched copy; text was extracted with pypdf 6.18.0 (page markers inserted per PDF page); page locators are PDF page numbers of the copy read unless noted, and section numbers are given where the extraction had no page markers. Copies are under `sources/S6-<id>/` (gitignored). SHA-256 values are of the file named in each entry. Search-engine result snippets, WebSearch summaries and WebFetch summaries were used only to locate copies; nothing is quoted from them. Extraction caveat: pypdf drops underscores inside code identifiers in the LAC PDFs, so quoted identifiers such as "tsched buffer size", "module udev detect", "PA STREAM EARLY REQUESTS" and "snd pcm rewind()" appear in the PDF as `tsched_buffer_size`, `module-udev-detect`, `PA_STREAM_EARLY_REQUESTS`, `snd_pcm_rewind()`; the quotations reproduce the extracted text and this note records the difference. Typographical errors inside quotations ("requiree", "stablizes", "represent the lowest") are the sources' own. Scope filter applied at read time: observations before 2010 and observations on non-desktop (embedded, phone, board) platforms are logged in one line and not read further.

## 1. Search log

### 1a. Bibliographic databases and APIs (2026-09-14)

| # | Engine | Query / request | Hits followed | Dead ends (status) |
|---|---|---|---|---|
| 1 | dblp publ API (`dblp.org/search/publ/api?q=…&format=json`) | `PulseAudio` | — | first request HTTP 000 (connection dropped); retry HTTP 200 but body is an Anubis (v1.27.0) proof-of-work bot challenge page, not JSON |
| 2–8 | dblp publ API | `PipeWire`; `JACK audio latency Linux`; `audio latency Linux scheduling`; `video playback energy Linux DVFS`; `mpv player`; `VLC CPU decode frame`; `video conferencing CPU Linux client` | — | each HTTP 000 (connection dropped); no JSON obtained |
| 9–10 | dblp web (`dblp.org/search?q=…`, via WebFetch) | `PulseAudio`; `video playback energy Linux` | — | both return an Anubis "Access Denied" challenge page; dblp not usable from this environment |
| 11 | OpenAlex works, `search=PulseAudio`, `publication_year:2010-2026` | 120 results; titles scanned; none is a measurement of a Linux desktop playback path (Apress book chapters "PulseAudio"/"Jack" 2017, BadBluetooth NDSS 2019, "Streaming Characteristics of Spotify Sessions" QoMEX 2018 [network], "Pulsemeeter" SBCM 2025 [mixer tool], udocker 2018, others unrelated) | — |
| 12 | OpenAlex, `search=PipeWire audio` | 22 results; "Pipewire audio backend in QEMU" (TIB video record, not a paper); Univ. Ljubljana 2026 thesis "Spatial Management of Concurrent Audio Sources in a GNU/Linux Desktop Environment" (not opened — title is a spatial-audio design, not a cadence measurement; time-box); rest unrelated | — |
| 13 | OpenAlex, `search=video playback DVFS Linux laptop energy per-frame decode` | 17 results; followed: Chi, Alvarez-Mesa, Juurlink TACO 2015 (see S6-chi15); Ejembi & Bhatti "Help Save The Planet" ACM MM 2014 (no open copy found — its experiment is reproduced as Chapter 4 of S6-ejembi16); Ejembi 2016 thesis (S6-ejembi16); "Client-Side Energy Costs of Video Streaming" DSDIS 2015 (S6-ejembi15). Not followed: Khernache 2021 HAL thesis (title states low-power multicore ARM) | dl.acm.org/doi/pdf/10.1145/2685551 (403, Cloudflare HTML); dl.acm.org/doi/pdf/10.1145/2647868.2654897 (403) |
| 14 | OpenAlex, `search=video decoding energy consumption software decoder Linux desktop frame` | 585 results; first 25 scanned; only S6-ejembi15 relevant (already followed) | — |
| 15 | OpenAlex, `search=video conferencing client CPU usage measurement Linux Zoom` | 355 results; first 25 scanned; followed arXiv 2408.16995 (Wang, Lyu, Sivaraman, "Characterizing User Platforms for Video Streaming in Broadband Networks", 200) — read and excluded: ISP-side traffic classifier, the only CPU named is the measurement server's ("8-core Intel Xeon E5-2620"), no client CPU; copy kept at `sources/S6-wang24/paper.pdf` SHA-256 `876667e0f26a0b070e502df14b124d24c27d6bd1a1ed41dd66e29a4c05de6bd0`. Not followed: "An In-depth Study of Bandwidth Allocation across Media Sources in Video Conferencing" ACM MM 2024 (bandwidth topic; dl.acm.org PDF) | — |
| 16 | OpenAlex, `search=audio playback wakeups power Linux timer` | 14 results; none relevant (Apress chapter "Power Consumption by Video Applications" 2014 not opened — book chapter) | — |
| 17 | OpenAlex with venue filter `primary_location.source.display_name.search:multimedia` (4 queries: video player CPU decoding frame Linux; video decoding energy DVFS laptop Linux; audio latency Linux PulseAudio JACK; video conferencing measurement client CPU) | — | API error "primary_location.source.display_name.search is not a valid field" ×4; venue restriction to MMSys/NOSSDAV/MM/ICME/TMM/PV could not be expressed in OpenAlex; unfiltered searches above used instead |
| 18 | OpenAlex, `search=NOSSDAV video playback CPU energy laptop`, `type:article` | 7 results; none relevant | — |
| 19 | OpenAlex, `search=Linux audio server latency measurement scheduling` | 1547 results; first 25 scanned; QMUL 2018 thesis "Low Latency Audio Processing" not opened (time-box; qmro handle page only) | — |
| 20 | OpenAlex, `search=MPlayer workload characterization Linux video player CPU` | 2 results (Southampton 2016 thesis, Toronto 2011 thesis); none relevant by title | — |
| 21 | OpenAlex, `search=media player wakeups PowerTOP Linux energy idle timer` | 1 result (Apress chapter); none | — |
| 22 | OpenAlex, `search=WebRTC Jitsi Linux client CPU profiling encode decode threads` | 1 result (ICN thesis); none | — |
| 23 | OpenAlex, `search=video decoding laptop Linux energy measurement H.264 playback ffmpeg DVFS ondemand governor` | 1 result (Khernache 2021, ARM); none | — |
| 24 | OpenAlex, `search=PulseAudio CPU usage measurement audio server Linux desktop` | 9 results; Aalto 2014 thesis "Audio Programming Interfaces in Real-time Context" not opened (time-box); none relevant by title | — |
| 25 | OpenAlex, `search=Zoom desktop client Linux CPU threads measurement` | 186 results; first 20 scanned; none relevant | — |
| 26–34 | arXiv API (`export.arxiv.org/api/query?search_query=…`) | `all:PulseAudio`; `all:PipeWire`; `all:"video playback" AND all:Linux AND all:energy`; `all:"video decoding" AND all:Linux AND all:"per-frame"`; `all:mpv AND all:"video player"`; `all:"video conferencing" AND all:CPU AND all:Linux`; `all:JACK AND all:audio AND all:Linux AND all:latency`; `all:VLC AND all:"CPU utilization"`; `all:"Google Meet" AND all:CPU AND all:Zoom` | — | HTTP 429 "Rate exceeded" on the first pass (percent-encoded), on the second pass (plus-encoded, 3 s spacing) and on a third pass after a 20 s wait with 6 s spacing; two requests HTTP 000; no arXiv API results were obtained in this session |
| 35–38 | Semantic Scholar `/graph/v1/paper/search` | `PulseAudio latency measurement Linux`; `video playback energy Linux laptop DVFS decode per frame`; `video conferencing client CPU per thread Linux measurement`; `mpv VLC MPlayer CPU utilization frame Linux measurement` | — | HTTP 429 on every attempt with back-off 8 s, 16 s, 24 s; one more retry after 45 s: 429 ("apply for a key") |
| 39 | Wayback availability API, `lac.linuxaudio.org/{2021,2022,2023,2024}/` | — | HTTP 429 ×4 |
| 40 | Wayback CDX, `research-repository.st-andrews.ac.uk/bitstream/*` filtered on `Ejembi` | — | empty response body |
| 41 | Zenodo API record 4463845/4452480 (Bieringa et al. technical report and dataset) | — | HTTP 403 "Access to this resource has been restricted due to unusual traffic from your network" |
| 42 | GitHub `kyle-macmillan/vca-imc-21` (MacMillan et al. IMC 2021 code) README and file tree | README 200; tree 200: files are `README.md`, `shaper.sh`, `static.sh`, `static.trace`, `test.py` and guibot screenshots; README's "Data Collected" section names network captures and WebRTC stats JSON only; grep for `cpu|top|pidstat|psutil|proc` in README: no match → no CPU-per-process data released with that paper | — |
| 43 | GitHub `svarvel/videoconf-tools` README (Chang et al. IMC 2021 tools) | 200; README is one line ("Suite of tools for performing testing of popular videoconferencing applications."); no dataset page found for the paper (web search #56) | — |
| 44 | CORE search `Ejembi Bhatti video energy` | 200; page contained no `/works/` links to parse | — |

### 1b. Linux Audio Conference proceedings by year (venue = `lac.linuxaudio.org/<year>/`, 2026-09-14)

| Year | Pages fetched (status) | Papers scanned for latency / scheduling / PulseAudio / PipeWire / JACK / measurement; action |
|---|---|---|
| 2010 | index (200), `?page=program` (200) | John Kacur, "Real-Time Kernel For Audio and Visual Applications" (`papers/15.pdf`, 200) — read by grep: an overview of PREEMPT_RT configuration (rtprio limits, SMI detection, `hwlatdetect`), no playback wake or CPU measurement; excluded. Copy `sources/S6-kacur10/paper.pdf` SHA-256 `dc78846d68ee6248efb7fdaa8d5b45223ffc8b75dddc12914e60d36610555f41`. Poettering keynote: slides only (not fetched). |
| 2011 | index (200), `?page=program` (200) | Covered by S1 (Cucinotta et al. `46.pdf`, Henningsson `45.pdf`); remaining titles ("PulseAudio on Mac OS X" slides, "Configuring your system for low-latency real-time audio processing" workshop, Airtime) not measurements; none fetched. |
| 2012 | index (200), `/2012/program` (200) | "From Jack to UDP packets to sound, and back", "Minivosc - a minimal virtual oscillator driver for ALSA", "An Open Source C++ Framework for Multithreaded Realtime Multichannel Audio Applications" — none a playback-cadence measurement by title/abstract; none fetched. |
| 2013 | index (200), `/2013/program` (200) | Freiberger, Huber, Meerwald, "Multi-Channel Noise/Echo Reduction in PulseAudio on Embedded Linux" (`papers/37.pdf`, 200) — read: platform is "a TI OMAP3 processor (DM3730)" speakerphone under "a custom embedded Linux system created with OpenBricks" (§2); the one CPU figure is "The overall runtime requirements of PulseAudio on the target platform depend on the signal-processing implementation, but to a large part also on the audio latency requirements (set to 50 ms). We observe approximately 25 % CPU load due to PulseAudio providing 4-channel AENR at 16 KHz. Profiling has been performed using the Linux perf tool." (§5) — embedded, not desktop; excluded from candidates. Copy `sources/S6-freiberger13/paper.pdf` SHA-256 `91d5bd32ccd761e2cf7453ad2c6773a4893f517a004d0c3a3e4096cb2e7d7db7`. |
| 2014 | index (200), `/2014/program` (200) | "Latency Performance for Real-Time Audio on BeagleBone Black" (Topliss, Zappi, McPherson; `papers/32.pdf`) — not fetched: abstract states the platform is a BeagleBone Black board (embedded). "Linux as a Low-Latency, Rock-Stable Live Performance System" (poster) — not fetched: stage experience report by abstract. "Audio Signal Visualization and Measurement" workshop — hardware measurement, not fetched. |
| 2015 | index (200), `/2015/program` (200), `files?page=program&mode=list` (200) | Alexander Patrakov, "Timing issues in desktop audio playback infrastructure" (`papers/10.pdf`, 200) — read in full → S6-patrakov15. Note: the program page's link order first led to `papers/20.pdf` (200), which is Malczewska, Żernicki, Szczechowiak (Zylia), "Low Delay Audio Streaming for a 3D Audio Recording System" — BeagleBone Black + Opus, embedded; excluded (copy `sources/S6-malczewska15/paper.pdf` SHA-256 `2b0e4578ce20cf5ee39901f35ad3780a4c858889d6f1cddf964416ea987d6adf`). The list page confirmed `10.pdf` is Patrakov. |
| 2016 | `/2016/` → 301 to `http://minilac.linuxaudio.org//` | `minilac.linuxaudio.org` HTTP 000 (connection failed, http and https); miniLAC 2016 not scanned. |
| 2017 | index (200), `lac2017/lacproceedings.html` (200), `lac2017/lacProgramGB.html` (200) | Program titles scanned (Ctlra, INScore, Faust libraries, openMHA, i-score, Moony, PlayGuru, C++ instruments…); no paper on audio-server timing or playback CPU; none fetched. |
| 2018 | index (200), `pages/schedule` (200) | Titles scanned (Rtosc, Jacktools, CLAPI, Ableton Link, AVB architecture, Cape4all, MRuby-Zest, Camomile…); none a measurement of a playback path; none fetched. |
| 2019 | index with program (200) | "A JACK Sound Server Backend to Synchronize to an IEEE1722 AVTP Mediaclock Stream" (`doc/kuhr.pdf`) — not fetched (AVB clock sync by title); "CPU Consumption for AM/FM Audio Effects" (`doc/goulart.pdf`) — not fetched (effect DSP cost, not a playback path by title). "Realtime Kernel and Linux Distributions" on the page is a call-for-papers topic heading, not a paper. |
| 2020 | `lac2020.sciencesconf.org` index (200), `program.html` (200) | Wim Taymans, "PipeWire: A Low-Level Multimedia Subsystem" (`307881/PipeWire.pdf`, 200) — read in full → S6-taymans20. "Express Data Path Kernel Objects for Real-Time Audio Streaming Optimization" — not fetched (network streaming by title). |
| 2021–2024 | `/2021/`, `/2022/`, `/2023/`, `/2024/` → HTTP 403 each (324-byte body) | `linuxaudio.org/lac.html` (200; reached via the 301 from `lac.linuxaudio.org/`) lists edition websites for 2010, 2011, 2012, 2013, 2014, 2015, 2017, 2018, 2019, 2020 and 2025 only; no 2021–2024 entries exist in that index. |
| 2025 | `/2025/` → 200 at `jimlac25.inria.fr` | Outside the 2010–2024 range requested; page states "In 2025, the Journées de l'Informatique Musicale and Linux Audio Conference joined forces"; program not scanned. |

### 1c. Web searches (engine: WebSearch, 2026-09-14)

| # | Query | Hits followed | Dead ends (status) |
|---|---|---|---|
| 45 | `Ejembi Bhatti "Help save the planet" video energy playback measurement Linux VLC OR mplayer pdf` | Semantic Scholar/Academia listing pages only (login-walled; not fetched); led to the St Andrews repository handles (503) and then Wayback (200) | research-repository.st-andrews.ac.uk (503 ×4) |
| 46 | `Chi Alvarez-Mesa Juurlink "Low-Power High-Efficiency Video Decoding using General-Purpose Processors" pdf` | static.tu.berlin/…/Chi2015a.pdf (200) | — |
| 47 | `paper measurement "PulseAudio" "timer-based scheduling" OR "wakeups" power consumption Linux laptop audio playback` | none academic (Fedora wiki, ArchWiki, forum threads, a 2011 blog "0.4 Watt Less During Audio Playback") | — |
| 48 | `video conferencing Linux client per-process OR per-thread CPU measurement study 2022 OR 2023 OR 2024 OR 2025 Zoom Meet Teams Ubuntu` | research.spec.org/icpe_proceedings/2021/companion/p65.pdf (200) and p171.pdf (200); atlarge-research.com/pdfs/vidconfperf-bieringa-hotcloudperf2021.pdf (200) | — |
| 49 | `paper "mpv" OR "MPlayer" OR "VLC" video playback Linux laptop "per-frame" decode time CPU DVFS governor measurement 2012 OR 2014 OR 2016 OR 2018` | none academic on a desktop player (GitHub issues, forums; embedded-DVFS papers on PXA270/handhelds not followed — off-platform) | — |
| 50 | `"timer slack" OR "timerslack" "audio playback" Linux measurement wakeups paper` | none academic (man pages, LWN); "Audio latency measurement for desktop operating systems with onboard soundcards" (ResearchGate/Academia, login-walled) not fetched — round-trip latency, not wake period or CPU | — |
| 51 | `GStreamer OR "gst-launch" video playback CPU time per frame Linux desktop measurement paper thread decode sink` | none academic (RidgeRun GstShark/gst-perf tool wikis) | — |
| 52 | `Bieringa Iosup "empirical evaluation of the performance of video conferencing systems" Zoom Teams Jitsi client operating system CPU` | atlarge-research PDF (200); ivanomalavolta.com/files/papers/QUATIC_2024_2.pdf (200) → S6-thangadurai24 | — |
| 53 | `"Timing issues in desktop audio playback infrastructure" Linux Audio Conference 2015` | lac.linuxaudio.org/2015/video.php?id=8 (not fetched; paper already obtained) | — |
| 54 | `Herglotz OR Kränzler video decoding energy x86 desktop ffmpeg OR dav1d OR libvpx "decoding time" per frame Linux measurement paper` | arxiv.org/pdf/2402.09001 (200) → S6-kraenzler24; arXiv 2510.12380 (AV1 decoder complexity via encoder tuning, 2025) not fetched — time-box, same group's method | — |
| 55 | `measurement paper web browser video playback power consumption Linux laptop Firefox Chrome YouTube CPU "frame" 2015 OR 2017 OR 2019 OR 2021` | states.github.io/files/p23.pdf (200) → S6-macedo20 | — |
| 56 | `Chang Varvello Hao Mukherjee "Can you see me now" Zoom Webex Meet IMC 2021 dataset release github OR zenodo` | github.com/svarvel/videoconf-tools (README fetched, row 43); no dataset page found | — |
| 57 | `MacMillan Mangla Saxon Feamster video conferencing dataset github release CPU usage per process Zoom Meet Teams Ubuntu` | github.com/kyle-macmillan/vca-imc-21 (row 42) | — |
| 58 | `"MPlayer" OR "mpv" OR "VLC" "wakeups" OR "timer" Linux "power" measurement paper laptop 2010..2016 media playback idle "PowerTOP"` | none academic (PowerTOP docs; Intel "Linux Power Efficiency Analysis Methods" white paper not fetched — vendor doc, S2's class) | — |
| 59 | `Chromium OR Chrome video playback threads "compositor" "media thread" CPU measurement Linux paper decode per frame` | none academic (Chromium design docs — S2's class) | — |
| 60 | `"perf sched" OR "ftrace" OR "LTTng" trace "video player" OR "mplayer" OR "VLC" Linux scheduler latency wakeup study paper` | none academic (tool docs) | — |
| 61 | `energy consumption video conferencing applications Linux Ubuntu measurement study 2022 OR 2023 OR 2024 OR 2025 Zoom Teams Jitsi CPU "per process" OR "threads" paper` | none academic beyond S6-thangadurai24 (Greenspector blog, forum posts; an IEEE Access 2025 "Foundations of Measuring Power and Energy Consumption in Video Communication" not fetched — methodology paper by title, time-box) | — |

### 1d. Direct fetches not covered above (2026-09-14)

| URL | Result |
|---|---|
| web.archive.org/web/2020id_/https://research-repository.st-andrews.ac.uk/bitstream/10023/9353/1/Ejembi_2015_Client_side_DSDIS_AAM.pdf | 200 (snapshot 20200314032734) |
| web.archive.org/web/2019id_/https://research-repository.st-andrews.ac.uk/handle/10023/9768 | 200 (snapshot 20200205221631; handle page linking `OcheEjembiPhDThesis.pdf?sequence=3`) |
| web.archive.org/web/2020id_/https://research-repository.st-andrews.ac.uk/bitstream/handle/10023/9768/OcheEjembiPhDThesis.pdf?sequence=3&isAllowed=y | 200 (snapshot 20200308213920, 15,123,065 bytes) |
| raw.githubusercontent.com/kyle-macmillan/vca-imc-21/main/README.md; api.github.com/repos/kyle-macmillan/vca-imc-21/git/trees/main | 200, 200 |
| lac.linuxaudio.org/2015/download/lac2015_arch_slides.pdf | 200 but 0 bytes |

## 2. Candidates

Coverage key: for T4 and T5, "covers" names object, unit, statistic, scope and population; otherwise "does not cover". "One observation?" states whether the source is a single population/trace/run and whether machine, application, subject and window are named. T1–T3, T6, T7 are not this reader's topics and are not assessed.

---

### S6-patrakov15

**Citation.** Alexander Patrakov. "Timing issues in desktop audio playback infrastructure." Proceedings of the Linux Audio Conference 2015 (LAC-15), Johannes Gutenberg University Mainz, April 9–12 2015, paper 10.

**Copy read.** LAC proceedings PDF, 7 pages. URL: http://lac.linuxaudio.org/2015/papers/10.pdf. Accessed 2026-09-14. Local: `sources/S6-patrakov15/paper.pdf`. SHA-256 `846c9c766722dae0b73e7b798ec40ad24f938aa5347ea5c283c15a78a3fc377e`. Locators are section numbers (extraction without page markers).

**Passages.**

- Abstract: "In year 2008, a feature with the name "timer-based scheduling" (also known as "glitch-free") has been introduced into PulseAudio in order to solve the conflicting requirements of low latency for VoIP applications and low amount of CPU time wasted for handling interrupts while playing music. The novel (at that time) idea was to use timer interrupts instead of sound card interrupts in order to overcome the limitation that the ALSA period size cannot be reconfigured dynamically."
- §1: "The hardware notifies the kernel when the hardware pointer crosses some predefined positions (period boundaries) in the circular buffer." … "E.g., an assumption is common that wakeups due to the audio device happen regularly (exactly once per period) and can be used as a clock. Another common assumption is that the default buffer and period sizes are suitable for the application's purpose. In fact, there was no way to change them programmatically in the default "plug:dmix" setup."
- §1: "On the other hand, low latencies are not optimal for music players. First, low latencies make applications sensitive to process scheduler decisions, increasing the chance of audio dropouts. Second, low latency means high rate of interrupts from the sound card and application wakeups, which is bad for power saving."
- §2: "PulseAudio has a client-server architecture. The server interacts with ALSA devices and performs mixing and routing of sound data received from client applications. Each time the timer fires, the sound card is asked about its current playback position, and, based on this information a decision is made how much data to request from applications in order to maintain their desired latency and to avoid underruns. Note that, if there are low-latency applications playing, the buffer will never be full."
- §3: "PulseAudio uses a large buffer (up to 2 seconds, if the hardware allows) by default. This is good for the purpose of providing high latencies for music players and thus for reducing the rate of CPU wakeups. The default can be overridden with the tsched buffer size parameter that is accepted by module udev detect, module alsa card, module alsa sink and module alsa source. The unit of the tsched buffer size parameter is microseconds."
- §3: "The problem is related to the fact that PulseAudio only has a finite budget of time it can run with real-time priority without making blocking system calls. rtkit contains a hard-coded limit that doesn't allow expanding this budget past 200 ms." … "Thus, in the worst case (which always happens at the start of a high-latency stream) PulseAudio has to finish its processing of two seconds of audio in 200 ms, or it gets killed." … "The situation is further aggravated by the fact that the cpufreq subsystem considers "low" (i.e. less than 80%) load as an excuse to keep the CPU frequency at the lowest possible value."
- §4 "Wakeup timings": "In the traditional timing model, the application usually is woken up once per period. The period size comes from application settings or from the defaults." … "With timer-based scheduling, better reaction to underruns is possible, and PulseAudio implements that. It looks at the sink's latency (which is just the amount of time until it underruns unless supplied with new data), subtracts the scheduling watermark, and sleeps for that time. The default watermark is 20 ms. It is increased if an underrun or a near-underrun happens, and decreased if sufficient time has passed without such bad events".
- §4: "Therefore, the smoother in PulseAudio uses a 10-second window and builds a least-squares linear approximation between the sample count and the wall-clock timestamp based on data within that window." … "A special rule (that cuts the sleeping time in half) is applied until one buffer worth of sound data is played."
- §4: "Typically, such batch cards provide position reports that are accurate to only one period, and timer-based scheduling makes a period as large as possible to avoid useless CPU wakeups from the interrupts originating from the sound card." … "Currently, PulseAudio disables timer-based scheduling on batch cards, because it cannot save the CPU from unneeded wakeups."
- §5.3: "The default safeguard is the largest of 256 bytes or 1.33 ms." … "For example, ymfpci updates its hardware pointer using a timer that fires every 5 ms." … "on common Intel HD Audio controllers, the granularity of the reported pointer position (as measured by calling snd pcm avail() and snd pcm rewindable() repeatedly) is 32 or 64 bytes."
- §5.5: "Indeed, this low-latency worker thread creates frequent wakeups and thus nullifies the primary motivation behind timer-based scheduling anyway."
- §6 "Client-side timing": "Some legacy applications (e.g. many ALSA-based media players) rely on the audio subsystem as a source of timing. In particular, they expect the wakeups to come in a regular fashion, in strict accordance to the period size. To satisfy such legacy clients, PulseAudio has a special PA STREAM EARLY REQUESTS flag that can be specified when creating a stream. Without this flag, requests will be made as late as possible. The pulse ALSA plugin always sets this flag." … "Problems begin when PulseAudio decides not to use timer-based scheduling (e.g., due to a batch card). In this case, PulseAudio uses the period size that is supported by the sound card and is close to the one specified in the daemon.conf file." … "As PulseAudio only wakes up and requests data from the client only on interrupts from the sound card, it no longer can wake up the client precisely when needed."
- §7: "Timer-based scheduling does solve the real problem that it is intended to solve: it achieves dynamic latency, which should be good for power saving."

**Coverage.**
- T4: covers as primary documentation, not as a measurement — object: PulseAudio server wake schedule under timer-based scheduling (sleep = sink latency − watermark; default watermark 20 ms; default buffer up to 2 s; batch cards fall back to interrupt-per-period with the daemon.conf period size; clients woken "as late as possible" unless PA_STREAM_EARLY_REQUESTS, which the ALSA pulse plugin always sets); unit: ms and µs as parameters; statistic: none (no measured wake-interval or per-wake CPU distribution; the only CPU statements are qualitative: rtkit's 200 ms real-time budget, cpufreq's <80 % load rule, "high rate of interrupts … bad for power saving"); scope: PulseAudio on ALSA, 2015 state of the code; population: none (no machine, no trace). It does not state a fixed wake interval with a fixed CPU share; it states the interval is dynamic and load-dependent.
- T5: does not cover.

**One observation?** No — a design/analysis paper; no machine, no application run, no window; only version pointers (alsa-lib 1.0.28/1.0.29, PulseAudio source functions) are named.

---

### S6-taymans20

**Citation.** Wim Taymans. "PipeWire: A Low-Level Multimedia Subsystem." Proceedings of the 18th Linux Audio Conference (LAC-20), SCRIME, Université de Bordeaux, November 25–27 2020.

**Copy read.** LAC-20 proceedings PDF, 6 pages. URL: https://lac2020.sciencesconf.org/307881/PipeWire.pdf. Accessed 2026-09-14. Local: `sources/S6-taymans20/paper.pdf`. SHA-256 `8c65e0d4a91fc25b4f8a71fae3f7abe19dfeb1513f29c0dd63e5aa34968cdc21`. Locators are section numbers.

**Passages.**

- §2.2: "JACK maintains a graph of applications (clients) that are connected using ports. In contrast to the previous audio servers, JACK will use the device interrupt to wake up each client in the graph in turn to process data. This makes it possible to keep the delay between processing and recording/playback very low."
- §2.3: "PulseAudio is optimized for power saving and does not handle low-latency audio very well, the code paths to wake up a client are in general too CPU hungry." … "PulseAudio can automatically become a JACK client when needed although this will cause high CPU load with low-latency JACK setups."
- §3.4: "The PipeWire audio processing graph uses a common single format between all the processing nodes. The format is not hard-coded into PipeWire but configured by the session manager and is currently the same format as used by JACK: Float 32 bits mono samples."
- §3.5 "Dataflow": "eventfd is used to wakeup nodes when they need to process input buffers and produce output buffers. timerfd is used to measure when a devices will be empty/filled. The timeout is adjusted based on the fill level of the device and a DLL. By using a timer, we can also dynamically adjust the period size based on client requirements. It is also possible to write the device wakeup using the traditional IRQ based approach but that does not provide flexible period adjustments." … "When a device needs more data (or has more data, in case of a source), the graph is woken up. PipeWire uses the same concepts as JACK2 to schedule the processing graph. It keeps track of dependencies between nodes and nodes are informed about the peer nodes they are linked to. When processing starts, all nodes without dependencies are scheduled (sources). When they complete, dependencies are satisfied on their peer nodes, which are then scheduled, and so on until the whole graph is completed. Nodes that complete can directly wake up their peers by signaling the eventfd without having to wake up the PipeWire daemon. This allows for the same latency and complexity as JACK and significantly better performance than PulseAudio."
- §3.6: "The clock slaving and resampling algorithm is inspired by zita-ajbridge [12]. It however runs in a single thread and uses a DLL to drive the resampler by matching its device fill level to the graph period size."
- §6.4: "Since Fedora 32 (early 2020), the redesigned version 3 with audio support has been shipped but not enabled by default." … "Currently, a plan is developing to try to enable PipeWire as the default Audio service in Fedora 34 (april 2021)".

**Coverage.**
- T4: covers as primary documentation only — object: PipeWire graph wake mechanism (timerfd-driven device wakeup with DLL-adjusted timeout; per-node eventfd wakeups; period size dynamically adjusted "based on client requirements"); unit: none stated; statistic: none — no default quantum value, no wake period, no CPU per wake, no trace; the comparative statements ("significantly better performance than PulseAudio", PulseAudio wake paths "too CPU hungry") are unquantified. Scope: PipeWire as of late 2020. Population: none.
- T5: does not cover (video paths are described only as camera/screen-share use cases, without cadence or CPU).

**One observation?** No — design paper; no machine, run or window.

---

### S6-chi15

**Citation.** Chi Ching Chi, Mauricio Alvarez-Mesa, Ben Juurlink. "Low Power High Efficiency Video Decoding using General Purpose Processors." ACM Transactions on Architecture and Code Optimization 11(4), Article 56 (January 2015). doi 10.1145/2685551.

**Copy read.** Author preprint from TU Berlin (running head "ACM Trans. Architec. Code Optim. V, N, Article A (YYYY), 25 pages"; article page numbers A:1–A:25 equal PDF pages 1–25). URL: https://www.static.tu.berlin/fileadmin/www/10002217/publications-pdf/Chi2015a.pdf. Accessed 2026-09-14. Local: `sources/S6-chi15/paper.pdf`. SHA-256 `9812d725716be2364de06fde29f48b08d6692f99d6510abdc035b00b7752b94b`.

**Passages.**

- p. A:2, §1: "video decoding is mostly utilized as a real-time application in video playback. In video playback a steady frame decoding rate, measured in frames per second, is required as compared to decoding the full sequence as fast as possible in offline decoding scenarios."
- p. A:7, §4: "In Figure 1 the frame times are plotted of decoding the 1080p 50Hz sequence BasketballDrive on an Intel Haswell@2.3GHz processor with a single core. The average frame time is 12.76 ms (78.4 fps). Periodic spikes can be observed for complex frames with a maximum of decoding time of 46.47 ms. To achieve a real-time performance of 50 fps, a new frame must be ready every 20 ms, which would not be possible in this case even on a high performance processor. Addressing this issue with more computing resources would be wasteful as the average frame rate is more than sufficient. Instead in video players a display buffer is used to account for this variability. Figure 1 shows that applying a display buffer of 4 (Tbuf 4) and 8 (Tbuf 8) pictures reduces the spikes considerably, providing more opportunity to exploit lower power active states of the processor."
- p. A:7, Fig. 1 caption: "Frame times of a 7Mbps 1080p50 sequence. Without playback buffers even high performance processors cannot guarantee real-time playback." (axes: Frame 0–500, Frametime (ms) 0–40; series Tbuf 1, Tbuf 4, Tbuf 8.)
- p. A:7, §4: "Because frames have to be decoded periodically, finishing early might not allow the processor to enter a deep idle state, because the next wakeup is predicted to occur soon. To increase the deeper C-state residency, a burst buffer could be used to allow the processor to pre-decode a longer part of the sequence (e.g. 1-second) at full speed and then go to near idle until the buffer is almost empty. In the (mostly) idle time only periodically a frame is released from the buffer."
- p. A:8, Table II "Architecture parameters of the platforms used in the evaluation.": "Haswell i5-4670T 4 - 32kB/32kB/256kB 6MB DDR3L-1600 2x64b 8GB / Haswell ULT i5-4200U 2 2w 32kB/32kB/256kB 3MB DDR3L-1600 2x64b 8GB / Baytrail-T Z3740 4 - 24kB/32kB/- 2MB LPDDR3-1066 2x64b 2GB / Exynos 5410-A7 4 … / 5410-A15 4 …"
- p. A:9, §5.2: "The HEVC decoder was compiled using GCC 4.8.1 with -O3, but without auto vectorization. Instead, all the vectorizable kernels are hand-optimized using SIMD: AVX2 is used for Haswell, SSE4.1 for Baytrail, and NEON for ARM. More information can be found in [Chi et al. 2014]. All platforms use a derivative of the (K)Ubuntu 13.10 Linux distributions. The x86 platforms run the 64-bit version and the ARM platform runs a 32-bit version of the operating system." … "The x86 platforms use Linux 3.12, 3.13rc2, and a modified version of Linux 3.13rc2, for Haswell ULT, Haswell, and Baytrail, respectively."
- p. A:10, Table IV "Kernel and power state drivers.": "Haswell 4670T 3.13rc2 intel pstate intel idle C7 C3 / Haswell ULT 4200U 3.12 intel pstate intel idle C7 C7 / Baytrail-T Z3740 3.13rc2(m) acpi cpufreq intel idle C6 C1 / Exynos 5410 3.4.67 exynos cpufreq exynos idle C2 n/a"
- p. A:10, §5.3: "The 1080p sequences are encoded using the HEVC reference encoder HM-12.1 with the random access main configuration (8-bit), and the 2160p sequences are encoded using the random access main10 configuration (10-bit)".
- p. A:18, §7.3: "In Figures 7 to 9 the power consumption of all platforms is plotted for real-time decoding of 1080p24 2.1 Mbps sequences (ParkScene@qp30, Kimono@qp27), and 1080p50 4.5 Mbps sequences (BasketballDrive@qp29, Cactus@qp29)." … "Each experiment is performed with a frame buffer of 8 frames to smooth the frame-to-frame decoding time variations. Additionally, the same experiments have been performed with an additional burst buffer able to hold 1-second of decoded video frames."
- p. A:18: "The figures show that for all platforms, decoding faster at higher frequencies and/or by using more cores ("race to idle") never yields the lowest power consumption for real-time decoding. Instead lower power consumption is achieved by spreading out the computation over more active time running at a lower frequency ("exploiting slack")."
- p. A:20: "For instance, the C-state residency of encoding a 1080p24 2.1 Mbps sequence on Haswell 4670T changes from CO(22%) - C1(18%) - C7(370%) when running 1 thread, to CO(33%) - C1(205%) - C7(162%) when running 4 threads. Also the package C-state residency is affected, and changes from PC0(32%) - PC7(68%) to PC0(90%) - PC7(10%), respectively, for 1 thread and 4 threads." … "We observed that the idle periods are predicted more conservatively when multiple threads were running."
- p. A:21: "on the Haswell 4670T, the 1080p50 sequences requiree roughly twice as much processing compared to the 1080p24 sequences, but the lowest achievable power consumption is 5.6 W and 4.5 W, respectively."
- p. A:22, §7.4: "For the ondemand DVFS experiments the number of decoding threads is set equal to the core count (no SMT), and for all experiments a frame buffer of size 8 is used." … "For the other sequences, corresponding to mid-activity levels, more than 50% higher power consumption is required by ondemand DVFS."
- p. A:23, Fig. 10 caption: "Power consumption of real-time decoding with best manual configuration and ondemand DVFS." (x axis "Activity (MCycles/s)" 0–10000 for Haswell 4670T; y axis Watt 0–30.)

**Coverage.**
- T4: does not cover.
- T5: covers partially — object: per-frame software decode time of an HEVC decoder (the authors' own optimized decoder, not mpv/VLC/GStreamer) on Linux (Ubuntu 13.10 derivative, kernels 3.12/3.13rc2) for a 1080p50 7 Mbps clip on a single Haswell core: mean 12.76 ms, maximum 46.47 ms, time series in Fig. 1 (unit ms; statistic mean, max, plotted per-frame series with 1/4/8-frame display buffering); real-time-decoding CPU demand expressed as "Activity (MCycles/s)" per sequence (Fig. 10) rather than as a per-frame CPU share; C-state residencies for one 1080p24 case; cadence is the content frame rate (20 ms at 50 fps, "frames have to be decoded periodically"), not display refresh. Scope: decoder library driven by the authors' harness, HM-encoded test sequences, offline and paced real-time modes; population: three Intel platforms + one ARM board, one run per configuration. No player thread structure, no audio, no scheduler trace.

**One observation?** Yes for the per-frame figure: one named machine (Haswell i5-4670T at 2.3 GHz, single core), one named sequence (BasketballDrive, 1080p50, 7 Mbps), window = 500 frames (Fig. 1 axis); the application is the authors' decoder (version not stated beyond "[Chi et al. 2014]").

---

### S6-ejembi15

**Citation.** Oche Ejembi, Saleem N. Bhatti. "Client-side Energy Costs of Video Streaming." Proc. IEEE International Conference on Data Science and Data Intensive Systems (DSDIS 2015), Sydney, December 2015. doi 10.1109/DSDIS.2015.49.

**Copy read.** Author accepted manuscript from the St Andrews Research Repository (handle 10023/9353), 8 pages, via Wayback snapshot 20200314032734. URL: https://web.archive.org/web/2020id_/https://research-repository.st-andrews.ac.uk/bitstream/10023/9353/1/Ejembi_2015_Client_side_DSDIS_AAM.pdf. Accessed 2026-09-14. Local: `sources/S6-ejembi15/paper.pdf`. SHA-256 `510908cde922b53d058a054ce38e174cb081c722cfca35ffd59d22d4e3f25bbb`. Locators are section numbers.

**Passages.**

- §III.A "Testbed": "Each system is a Shuttle XPC Glamor SG31G2 with an Intel® Core™ 2 Quad Q6600, 2.40GHz CPU, Intel 82G33/G31 chipset using an Express Integrated Graphics Controller core, with 4GB DRAM (128MB used for graphics, configured in the BIOS)." … "The client hosts ran a minimal installation of Ubuntu Linux (v13.10 64-bit x86-64 server), and with a minimal set of background processes running." … "We used the lightweight Openbox window manager, and the Mozilla Firefox (v29.0) web browser with the Pipelight plugin (v0.2.6, a Linux port of Silverlight, version 0.2.6) for playback of video content from the Netflix UK website. We measured energy usage through a Kill-a-Watt power meter, modified to send power readings via a short-range radio link to a USB receiver on the experiment controller at 1-second intervals."
- §III.B: "For each of the 202 titles and at each of the 3 quality levels, we streamed 2 minutes of video and repeated this 5 times." … "For each run, we sampled the power usage (with the Kill-A-Watt meter), CPU and memory utilization (with top), and network usage (with tshark) every 1 second. For 202 titles and at 3 quality levels, repeated 5 times, giving a total of over 3030 minutes of measurements."
- §IV.B: "We obtain average values of 10.8 J/sv, 12.7 J/sv and 14.5 J/sv for the respective quality levels. This corresponds to a difference of 34% between LOW and HIGH quality levels."
- §IV, Table II: "Low 'The Hobbit (Part 1)' AAA 7.9 (Best) / 'Parade's End' BRF 12.8 (Worst) / Medium 'Would You Rather' HRF 9.8 (Best) / 'Fresh Meat (S1E1)' BRT 15.9 (Worst) / High 'Peter Pan' CFF 9.7 (Best) / 'Toy Story' CFF 17.3 (Worst)"; "The values are the mean of 5 runs, with a 95% confidence interval that is less than 1 J/sv".
- §IV.C: "We measured the usage of system resources including CPU and memory utilisation, with the Unix process monitoring tool top, and the network bandwidth utilisation, with the opensource network monitoring tool tshark. In Figure 3b and 3c, we show boxplots summarising the CPU utilisation and network bitrate for the entire corpus, grouped by Netflix quality level. Each data point is the mean value for the resource used from 5 repetitions of playback of a video title." … "while CPU usage shows the strongest correlation with the overall system power, with a correlation coefficient of 0.89".
- Fig. 3 caption: "Summary of the resource usage (energy, CPU and network) for playback of the entire corpus of Netflix videos at the available quality levels. (202 videos. Each data point is the mean of 5 runs, each run is 120 seconds.)" (panel (b) axis "CPU Utilisation (%)" 0–100, LOW / MEDIUM / HIGH.)
- §IV.D: "The insertion of our graphics card added 22W to the idle power of our desktop system (up from 78W, to 100W with the card installed)." … "We did not observe any improvements in energy usage for video playback due to the GPU. This might be due to the Linux environment in which we ran our experiments, in which Silverlight is not natively supported by the GPU drivers."

**Coverage.**
- T4: does not cover (audio is inside the Netflix stream; not measured separately).
- T5: covers partially — object: whole-system CPU utilisation (`top`, 1 s samples) and system power during browser video playback (Firefox 29 + Pipelight/Silverlight, Netflix, software decoding) on a named Linux desktop; unit: CPU % (whole system), J per second of video; statistic: per-title means over 5 × 120 s runs, boxplots by quality level (Fig. 3b; the numeric CPU medians are only in the plot, not in the text); energy means 10.8/12.7/14.5 J/sv; scope: Ubuntu 13.10, one machine model; population: 202 titles × 3 qualities × 5 runs. No per-frame CPU, no frame cadence, no thread structure.

**One observation?** Yes — one named machine model (two identical units), named OS, browser and plugin versions, named content corpus, window = 120 s per run, 5 runs per title.

---

### S6-ejembi16

**Citation.** Oche Ejembi. "Enabling energy-awareness for internet video." PhD thesis, University of St Andrews, 2016 (handle 10023/9768). Chapter 4 reports the experiment published as O. Ejembi, S. N. Bhatti, "Help Save The Planet: Please Do Adjust Your Picture," Proc. 22nd ACM International Conference on Multimedia (MM 2014), doi 10.1145/2647868.2654897 (no open copy of the MM 2014 paper was found; ACM PDF 403).

**Copy read.** Thesis PDF, 223 pages, via Wayback snapshot 20200308213920 of the St Andrews repository bitstream. URL: https://web.archive.org/web/2020id_/https://research-repository.st-andrews.ac.uk/bitstream/handle/10023/9768/OcheEjembiPhDThesis.pdf?sequence=3&isAllowed=y. Accessed 2026-09-14. Local: `sources/S6-ejembi16/thesis.pdf`. SHA-256 `8a2097e1bb384aad6c453eed49f40acda5b5ae744f4804064458f241b7ea6447`. Locators are PDF pages (printed page numbers in parentheses). Only Chapters 4 and 5 were read (PDF pp. 74–113).

**Passages.**

- PDF p. 75 (46), §4.3: "is a Shuttle XPC Glamor SG31G2, with Intel® Core™ 2 Quad Q6600, 2.40GHz CPU with an Intel 82G33/G31 chipset and an Express Integrated Graphics Controller core, 4GB RAM (128MB used for graphics, set in BIOS)." … "This is considered a mid-range desktop configuration. The machine ran a minimal installation of Ubuntu Linux 13.10 64-bit (x86-64) Server installation, with no desktop environment, and with a minimal set of background processes running." … "However, to enable video playback on the client machine, I used the lightweight Openbox window manager. I played-back the video files using the opensource VLC media player application, version 2.2.git Weatherwax (revision 2.1.0-git-2995-dgf36375)."
- PDF p. 75 (46), Table 4.3 excerpt: "FLV from fmpeg-libavcodec v55.52 / H264 libx264 v0.125 / H265 libx265 v0.8 / MPEG4 from fmpeg-libavcodec v55.52 / MSMPEG4 from fmpeg-libavcodec v55.52 / VP8 libvpx VP8 v1.3.0-1780-g1f08824 / VP9 libvpx VP9 v1.3.0-1780-g1f08824".
- PDF p. 77 (48): "so a separate set of measurements were conducted for H.264 with hardware assist – 6 picture sizes, 20 runs, 2 minutes per run for each film, for an additional 480 minutes of tests." Table 4.4 "Summary of observables for experiments": "Power Watts MoteWatt power meter / {De,En}coding Time Seconds (s) time(1) / Energy K Joules (KJ) Power × time for {de,en}coding / CPU usage Percentage time(1) / RAM usage MiB time(1) / PSNR dB tiny_ssim / SSIM – tiny_ssim"; footnote "Note that this is /usr/bin/time and not the time command that is built into the default bash shell on linux."
- PDF p. 83 (54), §4.5.2: "Figure 4.3 shows the results from the decoding experiments entirely by software using the CPU without the video graphics card installed. The H265 codec, overall, consumes the greatest amount of energy, followed by VP9. H264 and VP8 consume an equal amount of energy and system resources during playback, while FLV consumes the least amount of resources during playback. It is important to note that these differences in energy and resource usage are at roughly the same target bit-rates."
- PDF p. 85 (56), Fig. 4.3 caption: "Resource usage for decoding of video files. 20 runs were used to plot each point, with 95% confidence (error bars not always visible as they are very small in some cases)." (panels per film 'Big Buck Bunny' and 'Tears of Steel': "Mean CPU Utilisation" Percentage(%) 0–200 (a) / 0–250 (b) over picture sizes QCIF, CIF, 360p, 480p, 720p, 1080p for FLV, H264, H265, MPEG4, MSMPG4, VP8, VP9; "Mean Memory Usage" RSS MB; "Raw Energy Usage" KJ 12–19.)
- PDF p. 98 (69), §5.2: "the tool interfaced with the popular libvlc (version 2.2.1) library, using its Python bindings." … "Process Monitoring: For playback to commence, vEQ-benchmark spawns a system process within which the chosen playback application (or browser or library) will exist. The processMonitor module highlighted in Figure 5.1 then begins to monitor the process, and records its computing resource utilisations and performance of that process. This is achieved using the psutil system monitoring Python library. These resources monitored are CPU utilisation (percentage), GPU Utilisation (percentage), memory usage (megabytes), network bitrate (bits per second) and file I/O (bytes). Data is collected every second by default".
- PDF p. 102 (73), §5.3.1: "I benchmarked the first 120s of each of these videos, and repeated each measurement 5 times."
- PDF p. 104 (75), Table 5.2 "Summary of the hardware and software benchmarked for evaluation." rows: "Intel X99 chipset, Intel i7-4920 CPU @ 4GHz, 16GB DDR4 DRAM | Ubuntu Linux 14.04 | Nvidia GTX 960, 2GB | H.264(libx264 version r2538), VP8/VP9 (libvpx version 1.4.0.8) | Voltcraft VC870 (with USB interface) | libVLC version 2.2.2"; "Intel X99 chipset, Intel i7-4920 CPU @ 4GHz, 16GB DDR4 DRAM | Windows 8.1 | … | libVLC version 2.2.2"; "Intel i5-4440 CPU @ 3.1 GHz, 8GB DDR4 DRAM | Ubuntu Linux 14.04 | None | … | libVLC version 2.2.2"; "Raspberry Pi 2 ARMv7 BCM2709 Quad-core CPU @ 900MHz, 1GB RAM | Ubuntu Linux MATE 14.04 | Videocore 4 GPU | H.264 (omx-h264 version 1.1) | … | omxplayer".
- PDF p. 112 (83), Fig. 5.7 caption: "Summary values from the benchmarking exercise for the Windows i7 (a) and Linux i7 (b) workstation configurations as described in Table 5.2. The power usage is grouped by itag value of the video (see Table 5.3 for itag keys)." (panel (b) "vEQ-benchmark - Summary results (Linux workstation, Youtube videos)", axes Power (W) 40–120 and CPU(%) 0–200 over itags 243, 43, 136, 244, 135, 247, 137, 248, 264, 272, 313.)

**Coverage.**
- T4: does not cover.
- T5: covers partially — object: (Chapter 4) per-process CPU utilisation of VLC 2.2.git decoding local files with seven software codecs at six picture sizes on a named Ubuntu 13.10 desktop, measured with `/usr/bin/time` over each 2-minute run (unit: % of one core, values above 100 % on the plot indicating multi-core use; statistic: mean of 20 runs per point with 95 % CI; plotted only — no numeric table in the text); (Chapter 5) per-process CPU % via psutil at 1 s for libVLC 2.2.2 playing YouTube files on Ubuntu 14.04 i7-4920 and i5-4440 (plotted per itag, Fig. 5.7b, axis 0–200 %). Scope: VLC on Linux desktops, software decoding; population: two films × 7 codecs × 6 sizes (Ch. 4); 10 YouTube titles × 16 itags × 5 runs (Ch. 5). No per-frame CPU, no frame cadence, no thread structure.

**One observation?** Yes — named machines (Table 5.2; Shuttle XPC in Ch. 4), named OS and player versions, named content ('Big Buck Bunny', 'Tears of Steel'; YouTube titles by itag), window = 120 s per run.

---

### S6-bieringa21

**Citation.** Richard Bieringa, Abijith Radhakrishnan, Tavneet Singh, Sophie Vos, Jesse Donkervliet, Alexandru Iosup. "An Empirical Evaluation of the Performance of Video Conferencing Systems." Companion of the 2021 ACM/SPEC International Conference on Performance Engineering (ICPE '21 Companion), April 19–23 2021, pp. 65–71. doi 10.1145/3447545.3451184.

**Copy read.** Published companion-proceedings PDF from SPEC Research, 7 pages. URL: https://research.spec.org/icpe_proceedings/2021/companion/p65.pdf. Accessed 2026-09-14. Local: `sources/S6-bieringa21/paper.pdf`. SHA-256 `b0886df5df8ed705eb5e49948f530c3a26dc41b6b47b29560c9b17c824148ee3`. A second copy (author version, https://atlarge-research.com/pdfs/vidconfperf-bieringa-hotcloudperf2021.pdf, `sources/S6-bieringa21/paper-atlarge.pdf`, SHA-256 `0c8a1639bb510a3d88b1ab42b9f17aef15228181820db0b957dd4fa93c221b2e`) has the same text. Locators are section numbers.

**Passages.**

- §3.2: "Our experiments collect the system-level metrics network bandwidth, CPU usage, and memory usage." … "To limit the duration of each experiment, the method further limits the extent of each experiment (to 5 minutes) and the number of repetitions (here, 4 times)."
- Table 2 "Experiment Workload.": "Video Audio Bitrate 570 KB Bitrate 1.41 MB Resolution 1280x720 Sample Rate 44100 Hz Format MJPEG Format WAV".
- §4.2: "it measures performance using a set of Measurement Tools (7): tcpdump [11], dpkt [7], and scapy [10] to capture network traffic and calculate network bandwidth usage, and Linux' ps (process status) command to measure CPU and memory usage."
- §5.1 "Experiment Setup": "In our experiments, all automated clients run on separate physical machines. All measurements are obtained from a client running on a machine equipped with an 8th generation 4.2 GHz 8-core Intel i7 processor and 16 GiB RAM memory. The machine connects to the orchestration server and video conferencing sessions over the Internet, using a Wi-Fi 5 (IEEE 802.11ac) connection limited to 100 Mbps upload and download bandwidth. Our experiments evaluate the Web-based applications of Zoom, Microsoft Teams, and Jitsi, and the Zoom desktop application".
- §5.2.1: "Zoom's average memory usage ranges from 3,182 MB for 6 clients to 3,794 MB for 2 clients, which is more than 3× the average memory usage of Teams and Jitsi, which do not exceed an average memory usage of 921 MB in all cases."
- Fig. 4 caption: "Effect of the number of clients on VCS client resource usage: memory (left), CPU (middle), and bandwidth (right). White dots show the arithmetic mean." (middle panel axis "Number of CPU Cores" 0.0–3.0; rows 2, 4, 6 clients; series ZOOMWEB, TEAMS, JITSI.)
- §5.2.2: "The left-most plot in Figure 5 shows that CPU usage is high, but stablizes over time for all VCSs. Microsoft Teams uses almost two full CPU-cores; this represent the lowest CPU usage among the systems we evaluate. Zoom's CPU usage is lower initially, but increases over time and takes almost 5 minutes (the full experiment duration) to stabilize."
- §5.3: "First, using only audio results in higher CPU usage than using only video." … "Second, while Zoom's Web client uses an average of 2.5 CPU cores for a 2-client conference, Zoom's desktop client does not use more than 0.5 cores. A decrease of 80%."
- §6: "Lastly, we have conducted our experiments on a Linux based operating system, and did not consider other popular operating systems such as Windows and OSX."
- Reference [15]: "Richard Bieringa, Abijith Radhakrishnan, Tavneet Singh, Sophie Vos, Jesse Donkervliet, and Alexandru Iosup. 2021. An Empirical Evaluation of the Performance of Video Conferencing Systems. https://doi.org/10.5281/zenodo.4463845" (Zenodo 403 in this session — see log row 41).

**Coverage.**
- T4: does not cover.
- T5: covers partially — object: whole-client CPU usage in "Number of CPU Cores" (from `ps`) of Zoom Web, Teams Web, Jitsi Web and the Zoom desktop client on "a Linux based operating system" (distribution and kernel not named); unit: cores; statistic: box plots with means over 5-minute runs × 4 repetitions per configuration (Fig. 4), time series (Fig. 5), and the stated values Teams ≈ 2 cores, Zoom Web 2.5 cores vs Zoom desktop ≤ 0.5 cores at 2 clients; scope: 2/4/6-client conferences with a fixed 1280×720 MJPEG + WAV feed; population: one client machine. No per-thread breakdown, no frame cadence, no capture/encode/decode split.

**One observation?** Yes — one named client machine ("8th generation 4.2 GHz 8-core Intel i7 … 16 GiB"), named applications (versions not stated), window = 5 minutes × 4 repetitions; OS named only as Linux.

---

### S6-cuijpers21

**Citation.** Jim Cuijpers, Kelvin Elsendoorn, Ean-Dan Tjon-Joek-Tjien, et al. "An Empirical Evaluation of Video Conferencing Systems Used in Industry, Academia, and Entertainment [Work-in-Progress]." ICPE '21 Companion, April 19–23 2021, pp. 171–174. doi 10.1145/3447545.3451174.

**Copy read.** SPEC Research PDF, 4 pages. URL: https://research.spec.org/icpe_proceedings/2021/companion/p171.pdf. Accessed 2026-09-14. Local: `sources/S6-cuijpers21/paper.pdf`. SHA-256 `037b320c015abdff042d666564493cbb250f707780ab7b405fbf61604dd95eaf`. Locators are section numbers.

**Passages.**

- §3.3: "Over the course of the experiment, the tool collects all the metrics (3 and 4), using Psutils [10]."
- §3.2: "We repeat the experiments for every system 50 times. This is done by taking 1-minute samples from a benchmark that we run for 50 minutes."
- §4.1 "Experimental Setup": "Each experiment is conducted using a PC equipped with a Ryzen 7 2700X CPU (8 logical cores) and 16GB DDR4 memory. The wired connection is Ethernet-based, with the machine connected to the Internet via the Dutch ISP KPN NetwerkNL".
- §4.2: "The CPU utilization is expressed as the number of utilized CPU cores, where a value of 1 is equivalent to 100% CPU utilization on a single core. The maximum value is equal to the number of logical CPU cores (8, in our experiments). When using audio+video and video, Discord has a significantly higher CPU utilization than both Microsoft Teams and Zoom."
- Fig. 4 caption: "Average number of CPU cores used for Zoom, Teams, and Discord. Setting: one-on-one, audio±video call." (axis 0.0–1.2 cores; groups audio, video, audio+video.)

**Coverage.**
- T4: does not cover.
- T5: covers marginally — whole-client CPU in cores for Zoom, Teams, Discord in one-on-one calls (means ≤ 1.2 cores, Fig. 4); the operating system is not named anywhere in the paper (grep for Windows/Ubuntu/Linux/macOS/"operating system": no match), so it cannot be placed on Linux; no per-thread or per-frame data.

**One observation?** Yes — one named PC (Ryzen 7 2700X), named applications; OS not named; window = 50 × 1-minute samples.

---

### S6-thangadurai24

**Citation.** Jonathan Thangadurai, Priyeta Saha, Korawit Rupanya, Rosheen Naeem, Alejandro Enriquez, Gian Luca Scoccia, Matias Martinez, Ivano Malavolta. "Electron vs. Web: A Comparative Analysis of Energy and Performance in Communication Apps." Proc. QUATIC 2024, LNCS (Springer), doi 10.1007/978-3-031-70245-7_13.

**Copy read.** Author PDF, 16 pages. URL: http://www.ivanomalavolta.com/files/papers/QUATIC_2024_2.pdf. Accessed 2026-09-14. Local: `sources/S6-thangadurai24/paper.pdf`. SHA-256 `be6daa9d830d44e51aff4405b815fb9fd36d11a7c07134ed1f02ccd8fa7ce120`. Locators are section numbers.

**Passages.**

- §4: "The selected subjects for this empirical examination are online communication platforms, particularly Skype, Discord, and Slack."
- §5 "Experiment Setup": "to conduct the experiment, we utilize a laptop with an Intel i7-11370H @ 3.30GHz CPU (CPU scaling enabled), an NVIDIA GeForce RTX 3050ti GPU, 4GB GDDR6 RAM, a 512GB PCIe NVMe M.2 SSD disk, and a virtual Web Camera (30FPS, 1280x720 resolution), running Ubuntu 22.04.2." … "For the desktop version, we selected the most recent releases at the time this experiment has been executed (October 2023), i.e., Skype (version 8.104.0.207), Slack (4.34.120), and Discord (6.2.0-33-Generic). For the Web version, the latest version is automatically provided from the servers, accessed through the Google Chrome browser (117.0.5938.92)."
- §5: "PowerJoular (version 0.6.2) [13]: a command-line tool for real-time monitoring of power consumption in CPU, GPU, and processes on GNU/Linux systems with low overhead. We choose this tool to capture, one sample per second, both energy consumption and CPU utilization."
- §5: "In our measurements, observed CPU utilization refers to the combined usage of all 4 physical cores, given that hyper-threading is enabled" (sentence continues in the copy).
- §5: "Each distinct combination is executed eight times on each of our selected subjects".
- §6: "CPU usage: Web applications at both durations have means of 14.33% and 14.03% respectively, while Electron apps demonstrated means of 15.94% for the 2-minute duration and 15.91% for the 8-minute duration. Thus, Web apps use, as mean, less CPU than Electron ones."
- §6, Table 1 rows: "CPU 2m 1.05x10−2 1.21x10−02 Significant 0.2137 Medium Electron ≠ Web / CPU 8m 4.017x10−04 1.07x10−03 Significant 0.29583 Medium Electron ≠ Web".

**Coverage.**
- T4: does not cover.
- T5: covers partially — object: process-level CPU utilisation (PowerJoular, 1 s samples) of Skype, Slack and Discord desktop (Electron) and web (Chrome 117) clients during two-party calls in audio, video, audio+screen-share and video+screen-share modes on a named Ubuntu 22.04 laptop; unit: % of the 4 physical cores combined; statistic: means (Web 14.33 %/14.03 %, Electron 15.94 %/15.91 % for 2- and 8-minute calls), distributions in Figs. 3a–3b, Mann–Whitney tests; population: one laptop, 8 repetitions per treatment. No per-thread split, no frame cadence.

**One observation?** Yes — one named laptop, named OS, named application versions, named virtual-camera feed (30 fps 1280×720), windows 2 and 8 minutes.

---

### S6-kraenzler24 (marginal)

**Citation.** Matthias Kränzler, Christian Herglotz. "A Comprehensive Review of Software and Hardware Energy Efficiency of Video Decoders." 2024 Picture Coding Symposium (©2024 IEEE); arXiv:2402.09001v1 (14 Feb 2024).

**Copy read.** arXiv PDF v1, 5 pages. URL: https://arxiv.org/pdf/2402.09001. Accessed 2026-09-14. Local: `sources/S6-kraenzler24/paper.pdf`. SHA-256 `6c18e30863fd0009c8c3bf6b6f9f7c775b86d31ebdc7024b5eaf17ea21a250a9`.

**Passages.**

- §II.A, Table I excerpt: "AVC x264 (r3065) JM (19.1) FFmpeg (4.4) / HEVC x265 (3.5.1) HM (16.23) openHEVC (2.0) / VVC VVenC (1.7) VTM (19.0) VVdeC (1.6)".
- §II.B: "For a fair comparison of each decoder, we limit the decoders to single-thread execution. For SW decoding measurements, we use a desktop PC with an Intel i7-8700 CPU and CentOS as an operating system (OS). The CPU incorporates an internal power meter with Running Average Power Limit (RAPL) [30] that can be directly accessed for energy measurements by the OS."
- §II.B: "As OS, we use Ubuntu, and the HW decoder is accessed over FFmpeg." (single-board computer with hardware decoder.)

**Coverage.**
- T4: does not cover.
- T5: covers marginally — offline, single-threaded decoding energy per bitstream (Bjøntegaard-delta energy relative to VP9/libvpx) of reference and optimized decoders (FFmpeg 4.4, openHEVC, VVdeC, dav1d, libvpx…) on a CentOS desktop; no per-frame time, no playback cadence, no player.

**One observation?** Yes — one named desktop (i7-8700, CentOS), named decoder versions, AOM CTC sequences.

---

### S6-macedo20 (read; excluded from coverage)

**Citation.** João de Macedo, João Aloísio, Nelson Gonçalves, Rui Pereira, João Saraiva. "Energy Wars - Chrome vs. Firefox: Which browser is more energy efficient?" ASEW 2020 (workshops of ASE 2020).

**Copy read.** Author PDF, 7 pages. URL: https://states.github.io/files/p23.pdf. Accessed 2026-09-14. Local: `sources/S6-macedo20/paper.pdf`. SHA-256 `10d094e6c44f2dc8f02a11ca35754de224e6129dea99890b94274c4bff301a7e`.

**Passage.** §3: "All measurements were performed in the same machine: Linux Ubuntu Desktop 18.04 operating system, with 16GB of RAM, Intel® Core™ i7 8750H 2.2 GHz" … "CPU and DRAM energy measurements were collected: 10 per second, according to the RAPL frequency of 100ms sampling rate".

**Why excluded.** Reports RAPL energy of Chrome vs Firefox across scripted sessions on YouTube, Instagram, Facebook, Twitch (Figs. 3–5); no CPU-time, per-frame or cadence observation of the video path; T4/T5 not covered.

---

### Identified but not read (blocked or off-scope; no passages quoted)

- Oche Ejembi, Saleem N. Bhatti. "Help Save The Planet: Please Do Adjust Your Picture." ACM MM 2014, doi 10.1145/2647868.2654897 — ACM PDF 403; St Andrews repository 503; Wayback CDX empty. Its experiment is presented in S6-ejembi16 Chapter 4 (VLC on Ubuntu 13.10).
- Bieringa et al. technical report and dataset, Zenodo 10.5281/zenodo.4463845 — Zenodo API 403 ("unusual traffic"); may hold per-run CPU series behind Fig. 4–5 of S6-bieringa21.
- Off-platform LAC papers logged in §1b (Topliss/Zappi/McPherson 2014 BeagleBone; Malczewska et al. 2015 BeagleBone/Opus; Freiberger et al. 2013 OMAP3 PulseAudio) — embedded boards, outside "Linux desktop".

## 3. Not found

- **T4 — measured wake period or per-wake CPU of a real audio playback path on a Linux desktop (PulseAudio, PipeWire, JACK with real clients, ALSA direct), 2010 onward.** Not found. What exists in this pass is primary documentation only: S6-patrakov15 states PulseAudio's timer-based schedule as an algorithm (sleep = sink latency − watermark, default watermark 20 ms, default buffer up to 2 s, interrupt-per-period fallback on batch cards, "as late as possible" client requests unless PA_STREAM_EARLY_REQUESTS) with no measured interval or CPU; S6-taymans20 states PipeWire's timerfd/DLL-driven wakeup with dynamically adjusted period size, again with no numbers. Neither documents a fixed wake interval with a fixed CPU share. The 2010–2020 LAC programs (§1b) contain no other paper on desktop audio-server timing or CPU; LAC 2016 (miniLAC) was unreachable and no LAC editions exist for 2021–2024 per the linuxaudio.org index. dblp was blocked (Anubis), arXiv API and Semantic Scholar were rate-limited (rows 1–10, 26–38); OpenAlex searches for PulseAudio, PipeWire, audio-server latency and wakeups (rows 11, 12, 19, 21, 24) and web searches 47, 50, 58 returned no measurement paper. Real-client JACK measurement: none beyond S1-cucinotta2011 (synthetic clients).
- **T5 — per-frame decode time and CPU share of mpv, VLC, MPlayer, GStreamer or browser video on a Linux desktop, with thread structure or scheduler trace.** Not found for any named player. Closest: S6-chi15 gives a per-frame decode-time series (mean 12.76 ms, max 46.47 ms, 1080p50, single Haswell core, Ubuntu 13.10) for the authors' own HEVC decoder, with cadence stated as the content frame rate and buffering of 4/8 frames; S6-ejembi16 (VLC 2.2 on Ubuntu 13.10/14.04) and S6-ejembi15 (Firefox+Silverlight on Ubuntu 13.10) give only per-run mean CPU % (plots) at 1 s sampling. Searches 13–15, 20, 23, 49, 51, 54, 55, 59, 60 found no player-level per-frame or thread-level study; Kränzler/Herglotz work (S6-kraenzler24 and the arXiv items in row 54) is offline decoder energy.
- **T5 — video-conference client threads (capture, encode, decode) with per-thread CPU on Linux; released datasets with CPU per process.** Not found. Whole-client CPU on Linux exists in S6-bieringa21 (cores via `ps`, Zoom/Teams/Jitsi web + Zoom desktop, OS named only as Linux, 2021) and S6-thangadurai24 (Skype/Slack/Discord, Ubuntu 22.04, PowerJoular, 2024); S6-cuijpers21 does not name its OS. MacMillan et al. 2021 released code (row 42) captures only pcaps and WebRTC stats — no CPU; Chang et al. 2021 released a tools repository with a one-line README and no dataset page (rows 43, 56); the Bieringa dataset on Zenodo was 403 (row 41). Searches 48 and 61 found no 2022–2025 Linux per-thread study.
- **Venues not effectively searched.** dblp (all queries blocked), arXiv API (rate-limited throughout), Semantic Scholar (rate-limited throughout), and OpenAlex venue filtering for MMSys/NOSSDAV/ACM MM/ICME/TMM/Packet Video (filter field invalid; only unfiltered OpenAlex full-text searches were possible). Google Scholar is not directly reachable; WebSearch (rows 45–61) stood in for it.
