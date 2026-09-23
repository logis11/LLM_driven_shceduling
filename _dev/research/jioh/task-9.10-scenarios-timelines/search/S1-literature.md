# S1 — Peer-reviewed and preprint literature (task 9.10, stage 2 search)

Reader class S1. Topics in scope: T1, T2, T3, T4, T6, T7, T9, T10, T11, T12. Reader worked from `search/input.md` only; no other repository file was opened. All accesses on 2026-09-23 (UTC). Every source was read directly from the copy identified in its entry. The local copies under `../sources/<id>/` are gitignored and will not survive this clone. Each entry therefore quotes the passages and identifies the copy by URL, date and SHA-256. Text was extracted with pypdf, or with pdfminer.six where noted. Page locators are PDF page numbers unless an entry says printed pages are used. A text layer sometimes splits words ("participa nts") or garbles a symbol ("/C6" for ±). In quotations only those artifacts are repaired, and the entry says so. Nothing else is changed. `[…]` marks reader insertions.

Summary of what the literature holds for this subject:
- **Logged observations with a named population:** S1-01, S1-03, S1-04/S1-33, S1-05, S1-07, S1-08, S1-09, S1-12, S1-13, S1-14, S1-21 (same population as S1-13), S1-24, S1-25 and S1-31. All are on Windows or have no OS stated.
- **Human-observer logs:** S1-02 and S1-06.
- **Lab benchmarks on Linux with a named machine:** S1-11 and S1-15.
- **Public traces:** S1-16 (lab), S1-17 (12 users, including 4 on Linux), S1-18 (a testbed with 1,000 Windows 10 hosts) and S1-19 (LANL; process names de-identified).
- **Grey literature, kept for T3 and T10 only:** S1-27 (the PCMark 10 guide).
- **Weak or off-population:** S1-10, S1-20, S1-22, S1-23, S1-26, S1-28, S1-29, S1-30 and S1-32.

## 1. Search log

All rows dated 2026-09-23. "WS" = WebSearch tool (web search engine, US results). "curl" = `curl -sSL` through the session proxy with the system CA bundle (TLS verification never disabled). Hits followed are the URLs actually fetched; dead ends carry the HTTP status (000 = no HTTP response).

| # | Engine / venue | Exact query or request | Hits followed | Dead ends (status) |
|---|---|---|---|---|
| 1 | Semantic Scholar API `/graph/v1/paper/search` | `display space usage and window management operation comparisons` | — | 429 Too Many Requests (rate limit, no key) |
| 2 | WS | `Hutchings Smith Meyers Czerwinski Robertson "Display space usage and window management operation comparisons" pdf` | microsoft.com …/avi2004-displayspace.pdf → S1-01 | — |
| 3 | WS | `Meyer Fritz Murphy Zimmermann "Software developers' perceptions of productivity" FSE 2014 pdf activity switching` | thomas-zimmermann.com …/meyer-fse-2014.pdf → S1-02 | — |
| 4 | WS | `Mark Iqbal Czerwinski Johns "Bored Mondays and focused afternoons" CHI 2014 pdf computer logging window switches` | wpmucdn (UCI) CHI-14-Focus-camera-ready.pdf → S1-03 | — |
| 5 | WS | `Dubroy Balakrishnan "A study of tabbed browsing among Mozilla Firefox users" CHI 2010 pdf` | dgp.toronto.edu …/chi2010_tabbedbrowsing.pdf → S1-04 | — |
| 6 | WS | `Meyer Barton Murphy Zimmermann Fritz "The work life of developers: activities, switches and perceived productivity" TSE 2017 pdf` | gwern.net …/2017-meyer.pdf → S1-05 | — |
| 7 | WS | `González Mark "Constant, constant, multi-tasking craziness" CHI 2004 pdf working spheres` | ics.uci.edu/~gmark/CHI2004.pdf → S1-06 | — |
| 8 | WS | `Weinreich Obendorf Herder Mayer "Not quite the average: An empirical study of Web use" pdf` | eelcoherder.com …/not_quite_the_average.pdf → S1-07 | — |
| 9 | WS | `Huang White "Parallel browsing behavior on the web" Hypertext 2010 pdf tabs` | jeffhuang.com …/ParallelBrowsing_HT10.pdf → S1-08; arxiv.org/pdf/2103.04694 (Ou et al., "Modeling Web Browsing Behavior across Tabs and Websites") fetched 200 (SHA-256 1b2e21c83a07ec6f4645f28a02792d19c2128908915dfe432d24dbb67a8e5326) and excluded: lab study of 21 participants on prescribed tasks, no in-the-wild counts | — |
| 10 | WS | `Chang Hahn Kim Kittur "When the tab comes due" CHI 2021 pdf arxiv` | — | dl.acm.org/doi/pdf/10.1145/3411764.3445585 → 403; dl.acm.org/doi/fullHtml/10.1145/3411764.3445585 → 403 |
| 11 | WS | `"When the Tab Comes Due" Chang Kittur pdf tab usage survey 103 participants tabs open` | — | joe.cat/CHI-browser-tabs/ → proxy CONNECT 502 (000) |
| 12 | Semantic Scholar API `/paper/DOI:…` | DOIs 10.1145/3411764.3445585, 10.1145/1816038.1816000, 10.1145/378993.379233, 10.1145/3487552.3487842, 10.1145/3473343, 10.1145/1111449.1111492 | open-PDF pointers: 3411764.3445585 → ACM (403 above); 3487552.3487842 → arXiv 2105.13478 (not fetched: network-performance study, no process data); 3473343 → ACM | 1816038.1816000 and 378993.379233 "not found"; 1111449.1111492 "CLOSED" |
| 13 | WS | `Reis Moshchuk Oskov "Site Isolation: Process Separation for Web Sites within the Browser" USENIX Security 2019 pdf` | usenix.org/system/files/sec19-reis.pdf → S1-09 | — |
| 14 | WS | `Terry Kay Van Vugt Slack Park "ingimp" instrumentation GIMP usage data CHI 2008 pdf` | mjskay.com …/chi_2008_ingimp.pdf → S1-10 | — |
| 15 | WS | `Joo Ryu Hahn Shin "FAST: quick application launch on solid-state drives" FAST 2011 pdf Linux launch time` | usenix.org legacy …/Joo.pdf → S1-11; usenix.org …/fast23-ryu.pdf → S1-15 | — |
| 16 | WS | `Amann Proksch Nadi Mezini "A study of Visual Studio usage in practice" SANER 2016 build duration pdf` | sarahnadi.org …/AmannSANER16.pdf → S1-12 | — |
| 17 | WS | `Blake Dreslinski Mudge Flautner "Evolution of thread-level parallelism in desktop applications" ISCA 2010 pdf` | — | dl.acm.org/doi/pdf/10.1145/1816038.1816000 → 403; researchgate.net/publication/220772094 → 403 |
| 18 | WS | `Mark Iqbal Czerwinski Johns Sano "Neurotics can't focus" in situ study online multitasking workplace CHI 2016 pdf` | ics.uci.edu …/CHI 16 Multitasking and Focus.pdf → S1-13 | — |
| 19 | WS | `Tak Cockburn "window switching" logging study Alt-Tab frequency revisitation desktop windows pdf` | opendl.ifip-tc6.org …/TakCHAGS09.pdf → S1-14 | — |
| 20 | WS | `Koldijk Sappelli Verberne Neerincx Kraaij "The SWELL knowledge work dataset for stress and user modeling research" ICMI 2014 pdf` | cs.ru.nl/~skoldijk/SWELL-KW/Dataset.html (link) → cs.ru.nl/~skoldijk/Papers/ICMI 2014 paper_final_cr.pdf → S1-16 | repository.tno.nl/SingleDoc?docId=42707 → 200 but HTML landing page, no PDF |
| 21 | WS | `BEHACOM dataset behaviour of computer users keyboard mouse application usage Data in Brief 2020` | ebi.ac.uk Europe PMC fullTextXML PMC7270191 → S1-17 | pmc.ncbi.nlm.nih.gov/articles/PMC7270191/ → 200 but reCAPTCHA challenge page |
| 22 | WS | `DARPA OpTC operationally transparent cyber dataset process creation events endpoints paper` | nrc-publications.canada.ca author version → S1-18 | dl.acm.org/doi/pdf/10.1145/3450569.3463573 → 403 |
| 23 | WS | `Kent "Comprehensive, multi-source cyber-security events" LANL dataset process start stop events Windows computers` | csr.lanl.gov/data/cyber1/ → S1-19 | book chapter (Imperial College Press) not openly available — not fetched |
| 24 | WS | `Flautner Uhlig Reinhardt Mudge "Thread-level parallelism and interactive performance of desktop applications" ASPLOS 2000 pdf` | — | dl.acm.org/doi/pdf/10.1145/378993.379233 → 403 |
| 25 | WS | `large-scale study desktop application usage telemetry concurrent applications running simultaneously Windows users log analysis paper` | microsoft.com …/Windows Reliability ICSE … 2010.pdf → S1-20 | — |
| 26 | WS | `Blake Dreslinski Mudge Flautner evolution thread-level parallelism desktop applications pdf umich TLP Windows 7 Snow Leopard` | — | — (no open copy listed) |
| 27 | WS | `"Evolution of thread-level parallelism in desktop applications" filetype:pdf` | — | cse.wustl.edu/~roger/566S.s21/Evolution of Thread-Level Parallelism in Desktop Applications.pdf → 000 (curl exit 60, TLS "unable to get local issuer certificate"; also with explicit `--cacert`); web.eecs.umich.edu/~manowar/…/threads-on-desktop-MTEAC2000.pdf (Flautner et al. 1999 tech. report) → 000 (same TLS error, https and http) |
| 28 | curl (guess) | tnm.engin.umich.edu/wp-content/uploads/sites/353/2017/12/2010.06.Evolution-of-thread-level-parallelism-in-desktop-applications.pdf | — | 403 |
| 29 | WS | `tnm.engin.umich.edu Blake "thread-level parallelism" desktop applications ISCA 2010 pdf` | — | no new copy |
| 30 | DBLP publ API | `q=Evolution of thread-level parallelism in desktop applications&format=json` | — | response not JSON (not parsed) |
| 31 | WS | `RescueTime data large-scale analysis computer usage application switching study paper` | — | no peer-reviewed RescueTime-based desktop study with published switch statistics among hits |
| 32 | WS | `ActivityWatch dataset study computer usage applications window focus logged participants paper` | — | no study found (arXiv 2304.04711 diary study noted, not followed: diary, not logging) |
| 33 | WS | `empirical study of build times developer machines incremental clean build duration C++ projects measurement paper` | seal-queensu.github.io …/EMSE-Taher-2019.pdf → S1-23 | no desktop build-time study among hits |
| 34 | WS | `measurement study Zoom Webex Meet client CPU usage video conferencing Linux laptop IMC 2021` | arxiv.org/pdf/2109.13113v1 → S1-22 | — |
| 35 | WS | `email usage logging study messages sent per day received per day field study workers attachments frequency` | microsoft.com …/Email Duration Camera Ready submission3-1.pdf → S1-21 | CSCW 2016 "Cost of email use" PDF listed, not followed (same population as S1-13/S1-21) |
| 36 | WS | `study background processes idle Linux desktop wakeups services measurement paper power PowerTOP Ottawa Linux Symposium` | — | no peer-reviewed study; vendor docs and forum pages only |
| 37 | WS | `DKMS kernel module rebuild time study OR measurement out-of-tree module compile objects academic` | — | no academic source; documentation/wiki only |
| 38 | WS | `backup behavior study users first full backup incremental size duration field study personal computers paper` | — | academia.edu survey paper ("Towards understanding short-term personal information preservation…", 319-respondent survey) → 403; researchgate → not tried (403 pattern) |
| 39 | WS | `music listening while working computer logging study concurrent media playback multitasking desktop` | — | only lab/psychology studies of effects; no logged concurrency study |
| 40 | WS | `application launch frequency desktop users per day log study Linux preload Esfahbod thesis application prediction` | — | Esfahbod 2006 MSc thesis ("Preload — An Adaptive Prefetching Daemon", U. Toronto) listed only on Google Books; no open copy found |
| 41 | WS | `Iqbal Horvitz "Disruption and recovery of computing tasks: field study, analysis, and directions" CHI 2007 pdf` | microsoft.com …/CHI_2007_Iqbal_Horvitz-1.pdf → S1-24; arXiv 2101.11865 (listed in same results) → S1-25 | — |
| 42 | WS | `Firefox telemetry tab count distribution study users open tabs windows large-scale paper browser` | — | only Firefox telemetry docs/bugzilla (S2 material) and the 2010 study |
| 43 | WS | `Linux desktop users application usage logging study processes running study participants Ubuntu empirical` | — | nothing relevant |
| 44 | WS | `Oliver Smith Thakkar Surendran "SWISH: semantic analysis of window titles and switching history" IUI 2006 pdf` | — | nuriaoliver.com/swish/iui2006-oliver.pdf → 404; dl.acm.org/doi/pdf/10.1145/1111449.1111492 → 403 |
| 45 | WS | `Security Behavior Observatory home computers Windows processes collected participants paper Forget Christin Cranor infrastructure` | usenix.org SOUPS 2016 forget.pdf → S1-26 | dl.acm.org/doi/pdf/10.1145/3473343 (Crichton et al., "How Do Home Computer Users Browse the Web?", TWEB 2021) → 403 |
| 46 | arXiv API | `ti:"home computer users browse"`; `all:"Security Behavior Observatory"` | — | 0 entries each |
| 47 | WS | `VMware View Planner "desktop workload" benchmark operations Word Excel PowerPoint Internet Explorer video think time VMware Technical Journal pdf` | — | vendor pages/blogs only; no paper with a workload order located |
| 48 | WS | `PCMark 10 technical guide pdf workloads app start-up video conferencing web browsing spreadsheets writing photo editing rendering order` | s3.amazonaws.com download-aws.futuremark.com/pcmark10-technical-guide.pdf → S1-27 | — |
| 49 | WS | `Wallace Douglis Qian Shilane Smaldone Chamness Hsu "Characteristics of backup workloads in production systems" FAST 2012 pdf` | usenix.org …/fast12/wallace.pdf → S1-28 | — |
| 50 | WS | `Lottarini vbench benchmarking video transcoding in the cloud ASPLOS 2018 pdf video durations` | arcade.cs.columbia.edu/vbench-asplos18.pdf → S1-29 | — |
| 51 | WS | `developer build latency study local builds duration distribution productivity Google OR Microsoft empirical "build time" developers wait paper 2020` | — | newsletters/blogs only; no primary paper with desktop build-duration distribution located |
| 52 | WS | `desktop search indexer CPU overhead measurement study OR antivirus scan performance overhead desktop empirical study paper` | — | JUCS 2019 antivirus file-operation overhead paper listed (Windows, per-operation latency; not followed — measures overhead, not schedule or duration of scans) |
| 53 | WS | `Oliner Iyer Stoica Lagerspetz Tarkoma "Carat: collaborative energy diagnosis for mobile devices" SenSys 2013 pdf` | amplab.cs.berkeley.edu …/oliner-Carat-SenSys13.pdf → S1-30 | — |
| 54 | WS | `Kumar Tomkins "A characterization of online browsing behavior" WWW 2010 pdf pageviews toolbar` | ra.ethz.ch cdstore www2010 p561.pdf → S1-31 | — |
| 55 | WS | `Falaki Mahajan Kandula Lymberopoulos Govindan Estrin "Diversity in smartphone usage" MobiSys 2010 pdf application sessions per day` | ratul.org …/mobisys2010-diversity.pdf → S1-32 | — |
| 56 | WS | `Linux X11 active window logging field study participants application usage GNOME KDE study paper window focus` | — | no study found |
| 57 | WS | `browser tab usage in the wild logged tab counts Chrome extension study 2019 2020 2022 participants open tabs median maximum` | dubroy.com blog (Test Pilot/tab study write-up) → S1-33 | only blogs/extension pages otherwise; no post-2010 logged tab-count paper found |

Directions from the brief that were searched with no usable primary copy: Dragunov et al. TaskTracer and Oliver et al. SWISH (SWISH: 404/403, row 44; TaskTracer: not separately located; it appears only as a citation in S1-14). "Zhang et al. CHB 2015" could not be identified from the information given; no search located a matching logging study. Blake et al. ISCA 2010 and Flautner et al. ASPLOS 2000: rows 17, 24, 27, 28. Chang et al. CHI 2021: rows 10–12.

## 2. Candidates

### S1-01 — Hutchings, Smith, Meyers, Czerwinski & Robertson 2004 (VibeLog)

- **Citation.** D. R. Hutchings, G. Smith, B. Meyers, M. Czerwinski, G. Robertson. "Display Space Usage and Window Management Operation Comparisons between Single Monitor and Multiple Monitor Users." Proc. AVI '04 (Working Conference on Advanced Visual Interfaces), Gallipoli, Italy, May 25–28 2004, pp. 32–39. ACM. DOI 10.1145/989863.989867.
- **Copy read.** https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/avi2004-displayspace.pdf — author/publisher-hosted camera-ready (8 pp., printed page numbers 32–39); accessed 2026-09-23; HTTP 200; local `../sources/S1-01/paper.pdf`; SHA-256 `26c5ed8a5f42ed45ab5e79b7512e81a6b989de3b5edb1d2c6ae1626486aa0e4d`.
- **Platform / population / year / method.** Windows XP; 39 volunteers in a research organization (Microsoft Research implied by affiliation; occupations listed); 3-week study; published 2004; logged with the VibeLog window-event hook tool (event log + per-minute window log). Logged, not self-reported.
- **Passages.**
  - p. 33 (§4): "Thirty-nine volunteers from within a research organization participated in a 3-week study of their computing event activity by" / p. 34: "using VibeLog on their work PCs." … "Occupations of our participants included Administrative Assistant (1), UI designer (1), Program Manager (3), Software Developer (9), Research Intern (8), and Researcher (17). We captured 105,402 minutes (just over 73 person-days) of participants' active time. A particular point in time is active if, within the previous 5 minutes, there was a mouse movement or key press."
  - p. 33 (§3): "Our field study involves users of the Windows XP window manager (hereafter referred to as Windows)".
  - p. 34 (§5.1): "These activities include opening and closing a window, showing and hiding a window, activating a window, and moving, sizing, minimizing, maximizing, and restoring a window. There is also an entry when users press <alt>+<tab> to switch to a different window." … "Each log entry has a timestamp and contains window and input information." §5.1.1: "Window information includes the window's ID, title, host application, coordinates, size state, style, and monitor information."
  - p. 34 (§5.2): "The window log writes a series of entries, one per each open window, every minute."
  - p. 35 (§6.1): "Analysis of our participants' data revealed that 78.1% of the time people had eight or more windows open, so users may often experience problems with using the taskbar."
  - p. 35 (§6.2): "Participants produced 360,084 activate events, accounting for both the opening of new windows and switching to already opened windows. The average amount of time that any window was active was 20.9 seconds. (This average excludes activation durations of less than 150 milliseconds, which are likely to be artifacts of multiple windows and sub-windows popping up near-simultaneously in response to a single user action, rather than representing multiple user actions). Perhaps more revealing, however, is that the median amount of activation time is 3.77 seconds, i.e., half of all window activation lengths are quite short."
  - p. 35 (§6.3.1): "single monitor users, who averaged 3.5 visible windows, and small multimon users, who averaged 4.1 visible windows, is surprisingly small. On the other hand, large multimon users averaged 6.8 visible windows. The median for each group was 3, 4, and 6 visible windows, respectively."
  - p. 35 Table 1 (Total Switches / Window Switches / Taskbar Switches): "single monitor 186,708 64.7 % 26.3 %"; "small multimon 63,083 78.9 % 13.3 %"; "large multimon 90,284 87.4 % 5.2 %".
  - p. 35 Table 2 / p. 36 (§6.3.2): "For single monitor users, the inbox was invisible 67.1% of the time and completely visible 6.7% of the time. When completely visible, the inbox was active 90.0% of the time".
- **Coverage.**
  - T1 covers (partly): object = open windows (not processes); statistic = share of active time with ≥ 8 windows open (78.1%); mean/median visible windows per per-minute snapshot (3.5/3, 4.1/4, 6.8/6 by monitor group); population 39 researchers-org staff, Windows XP. No per-activity co-occurrence and no process or application names listed in the text (host application name is logged but not tabulated).
  - T2 covers: object = window activations (foreground); unit = seconds; statistic = mean 20.9 s, median 3.77 s activation duration (activations < 150 ms excluded); count = 360,084 activations; switch counts by method (Table 1). No distribution beyond mean/median; no per-application dwell.
  - T9 covers (marginally): email inbox visibility/active share (Table 2), not operation frequency.
  - T3, T4, T6, T7, T10, T11, T12: does not cover (log not published).
- **One observation?** Yes — one population (39 volunteers, one research organization, Windows XP work PCs), one 3-week window (calendar dates not stated). Machine hardware not named beyond monitor counts.

### S1-02 — Meyer, Fritz, Murphy & Zimmermann 2014 (FSE)

- **Citation.** A. N. Meyer, T. Fritz, G. C. Murphy, T. Zimmermann. "Software Developers' Perceptions of Productivity." Proc. 22nd ACM SIGSOFT International Symposium on Foundations of Software Engineering (FSE 2014), pp. 19–29. DOI 10.1145/2635868.2635892.
- **Copy read.** https://thomas-zimmermann.com/publications/files/meyer-fse-2014.pdf — author-hosted copy (11 PDF pages; locators below are PDF page numbers); accessed 2026-09-23; HTTP 200; local `../sources/S1-02/paper.pdf`; SHA-256 `949c0f8986495585b1a4b72c423c9479897540dd1b07b8adfbb0b30ab6e5fce3`.
- **Platform / population / year / method.** OS not stated. 11 professional software developers, 3 companies (US/Canada), 4 h each on one workday; human observer log (not software logging); plus a 379-respondent survey (self-report). Published 2014.
- **Passages.**
  - PDF p. 2: "The observational study we conducted involved observing 11 professional software developers from three companies at work for four hours each. As the developers worked, we collected detailed logs of the tasks worked on and the programs used to perform work, gathering a total of 2650 log entries."
  - PDF p. 6 (§4.1): "The observer noted in an observation log each time the participant switched a program on his computer, was interrupted by others or interrupted him or herself, or switched a task while being in the same program. Each entry in the observation log consists of a time stamp, a reason for the switch, the program that the participant switched to and the task that the participant was working on." … "Due to confidentiality reasons, we are not able to share the observation logs."
  - PDF p. 6 (Table 6, "% of time over all Observ."): "Code reading/editing/navigating code 32.3%"; "Debug debugging 3.9%"; "TestApp testing application outside IDE 11.7%"; "Email reading/writing emails 4.9%"; "MeetInformal … 13.1%"; "BrowsingRel Internet browsing related to code/work/task 4.0%"; "BrowsingUnrel Internet browsing work unrelated 0.4%".
  - PDF p. 6 (Theme 1): "Each participant switched frequently between tasks with a mean task switch rate of 13.3 (±8.5) times per hour. The average time spent on each task was 6.2 (±3.3) minutes."
  - PDF p. 7: "The participants also mentioned that task switches occurred when they were blocked themselves or waiting, such as waiting for a build to finish. In these cases, the participants mentioned that switching to email, code reviews, or other small tasks can help increase their productivity."
  - PDF p. 7 (Theme 2): "During the sessions, participants switched activities 47.0 (±19.8) times per hour, spending on average 1.6 (±0.8) minutes on an activity before switching." … "Following coding the next activity was testing in 28.5% of the cases; a similar result holds for switches from testing to coding. Coding was also often superseded by an informal meeting (14.9%) … After an informal meeting, developers either went to coding (26.1%), testing (14.8%) or right into planning (18.3%). Finally, emails were mostly checked while coding (18.8%) or testing (19.4%) and developers generally returned to testing (20.7%), coding (17.2%) or planning (19.5%) after the email check."
- **Coverage.**
  - T2 covers: object = activity (program-based category) and task switches; unit = switches/hour, minutes/activity; statistic = mean ± SD (47.0 ± 19.8 activity switches/h; 1.6 ± 0.8 min per activity; 13.3 ± 8.5 task switches/h; 6.2 ± 3.3 min per task); population = 11 developers, software development situation.
  - T3 covers: activity-to-activity transition percentages (coding→testing 28.5%, email preceded by coding 18.8%/testing 19.4%, etc.) — an observed order for development work (bigram shares, not a full sequence).
  - T1: does not cover (programs switched to are logged but co-running sets are not reported).
  - T7 (marginal): build waiting mentioned qualitatively only; no build durations.
  - T9: email share of time (4.9%) — not a per-operation frequency. Does not cover operation rates.
  - T4, T6, T10, T11, T12: does not cover (logs not shareable).
- **One observation?** Yes — one population (11 developers, 3 companies), 4 h each; machines/OS and calendar window not named.

### S1-03 — Mark, Iqbal, Czerwinski & Johns 2014 (CHI, "Bored Mondays")

- **Citation.** G. Mark, S. T. Iqbal, M. Czerwinski, P. Johns. "Bored Mondays and Focused Afternoons: The Rhythm of Attention and Online Activity in the Workplace." Proc. CHI 2014, pp. 3025–3034. DOI 10.1145/2556288.2557204.
- **Copy read.** https://bpb-us-e2.wpmucdn.com/sites.uci.edu/dist/5/1068/files/2014/04/CHI-14-Focus-camera-ready.pdf — author-hosted camera-ready (10 PDF pages); accessed 2026-09-23; HTTP 200; local `../sources/S1-03/paper.pdf`; SHA-256 `4143c67f5f878da4b2c3e9a851057c06a2aa699c05d63ad6650b5a9adca3370f`.
- **Platform / population / year / method.** Windows 7; 32 information workers (15 researchers plus managers, administrators, etc.) at one organization (Microsoft Research co-authors; organization not named in the quoted text); 5 days each; custom foreground-window logger + experience sampling. Published 2014; collection year not stated in the passages read.
- **Passages.**
  - PDF p. 4 (Methodology): "Thirty-two people (17 females, 15 males) participated. Participants included researchers (15), managers, administrators, an engineer, a department director, a designer, and a consultant." … "Each participant was observed for a period of five days, Monday through Friday, for most people."
  - PDF p. 4: "We logged online interactions with custom-built software that captured all activity in the Windows 7.0 Operating System. This included beginning and end times for the lifespan of every window, and the beginning and end times for every instance of every foreground window. Mouse and keyboard activity were captured, as was computer sleep mode, so that we could ignore periods of time when a window was open but was not being used in the foreground. Capturing what email was being read or any other application interaction was not collected due to privacy and technical limitations."
  - PDF p. 5 (Results): "We collected data on each of the 32 participants for 5 days each, for a total of 160 person-days, or 1,509 hours of data collection. Our computer logging software collected 91,409 computer window switches."
  - PDF p. 7–8: "Win Switches were significantly higher on Monday (M=661.2 switches/day, SE=69.60) than Friday (M=390.7 Win switches/day, SE=28.7), and also that Internet surfing is higher on Monday (M=280.8 switches/day, SE=42.9) than Friday (M=151.3 switches/day, SE=16.2)."
- **Coverage.**
  - T2 covers: object = foreground-window switches; unit = switches per person-day; statistic = means (SE) by weekday (Monday 661.2, Friday 390.7); aggregate 91,409 switches over 1,509 h (≈ 60.6/h derived by division — not a published figure); population 32 information workers, Windows 7.
  - T4 (partial): "Internet surfing" switch counts per day (Monday 280.8, Friday 151.3) — not tab/window counts.
  - T9 (partial): email/Facebook seconds in the 10 min before probes (Figure 3/Tables 3–4; values are in figures/tables not transcribed here) — not operation rates.
  - T1, T3, T6, T7, T10, T11, T12: does not cover.
- **One observation?** Yes — one population (32 workers, one organization, Windows 7), 5 days each; calendar dates and machines not named.

### S1-04 — Dubroy & Balakrishnan 2010 (CHI, Firefox tabs)

- **Citation.** P. Dubroy, R. Balakrishnan. "A Study of Tabbed Browsing Among Mozilla Firefox Users." Proc. CHI 2010, Atlanta, pp. 673–682. DOI 10.1145/1753326.1753426.
- **Copy read.** https://www.dgp.toronto.edu/~ravin/papers/chi2010_tabbedbrowsing.pdf — author-hosted, publisher pagination 673–682 (10 PDF pages); accessed 2026-09-23; HTTP 200; local `../sources/S1-04/paper.pdf`; SHA-256 `8f1189484d86152d99ad64d67a96be9139bd33d510a86eb353148264040a33a3`.
- **Platform / population / year / method.** Firefox 1.5–3.0, "Most of our participants used Microsoft Windows"; 21 participants (Toronto campus network; 6 students, 15 office workers); 13–21 days each; custom Firefox click-stream extension + diary + interviews. Published 2010 (collection period not dated in passages read).
- **Passages.**
  - p. 675 (PDF p. 3, Participants): "21 people (13 female, 8 male; 15 aged 18-29, 4 in their 30s, and 2 in their 50s) were recruited via email through the extended network of the researchers, and by posters on bulletin boards around campus." … "6 of the participants were full-time students, and 15 were working in office environments where they spent most of their time on the computer."
  - p. 675: "Click-stream data was collected using a custom extension for Firefox that was compatible with Firefox versions 1.5 through 3.0 so that it could be installed without upgrading or significantly changing the user's browsing environment."
  - p. 676 (PDF p. 4): "Number of concurrent tabs and windows. We measured the number of windows and tabs that were open when a navigation event occurred, as in Weinreich et al. [18]."
  - p. 677 (PDF p. 5): "Most of our participants used Microsoft Windows".
  - p. 677: "Over half our participants (13/21) are clustered around the 0.04 mark. In other words, these people created about 4 tabs for every 100 navigation actions. The rest of the participants are loosely centered around 0.14 … Two participants are even higher, creating (respectively) 17 and 22 tabs per 100 navigation actions."
  - p. 678 (PDF p. 6): "Figure 3 shows the number of tabs open when a navigation action occurred. The most common number of tabs to have open is one, with a steady descent down to 9. There is a second peak at 16 tabs, but this was almost entirely due to just two of the participants, P14 and P20." … "Participant 14 had by far the highest median number of tabs open with 17, while no other participant had a median higher than 6. Participant 20 had the highest number of tabs open at once, with 42."
- **Coverage.**
  - T4 covers: object = open tabs per navigation event (histogram, Fig. 3; per-participant median and max, Fig. 4), tab creation rate (tabs per 100 navigation actions), tab switch rate (Fig. 5, values only in figure). Population 21 Firefox users (mostly Windows). Per-minute rates are not published in the text.
  - T2 (partial): tab switches — only as a normalized rate in a figure.
  - T1, T3, T6, T7, T9, T10, T11, T12: does not cover.
- **One observation?** Yes — 21 participants, 13–21 days each, Firefox 1.5–3.0; machines not named; calendar window not stated in passages read.

### S1-05 — Meyer, Barton, Murphy, Zimmermann & Fritz 2017 (TSE, "The Work Life of Developers")

- **Citation.** A. N. Meyer, L. E. Barton, G. C. Murphy, T. Zimmermann, T. Fritz. "The Work Life of Developers: Activities, Switches and Perceived Productivity." IEEE Transactions on Software Engineering 43(12):1178–1193, Dec. 2017. DOI 10.1109/TSE.2017.2656886.
- **Copy read.** https://gwern.net/doc/psychology/writing/2017-meyer.pdf — third-party mirror of the published IEEE version (16 PDF pages, printed pp. 1178–1193; IEEE footer "0098-5589 © 2017 IEEE"); accessed 2026-09-23; HTTP 200; local `../sources/S1-05/paper.pdf`; SHA-256 `fa95356daf3fd87db09cc0a0e1d149593e995296e7e798be12b36d0b8d2d6c0d`. (Text layer renders "±" as "/C6"; quoted below with ±.)
- **Platform / population / year / method.** Windows 7/8/10; 20 professional developers (19 m, 1 f), 4 companies; 7–20 work days each (mean 11.0), 2,197 h over 220 work days; monitoring app sampling active process name + window title every 10 s, input events, hourly experience sampling. Manuscript received May 2016, so collection ≤ 2016 (exact dates not stated).
- **Passages.**
  - p. 1181 (§3.2): "The monitoring application was developed and tested to run on the Windows 7, 8 and 10 operating system." … "The monitoring application logged the currently active process and window title every 10 seconds, or an 'idle' entry in case there was no user input for longer than 10 seconds. In addition an event for each mouse click, movement, scrolling, and keystroke was logged."
  - p. 1182: "During the study, the monitoring application collected data from 2,197 hours of participants' computer use over a total of 220 work days. Table 1 shows that each participant was part of the study for between 7 and 20 work days (mean: 11.0 days, ±3.6)."
  - p. 1184 (§5.1.1): "Overall, developers averaged spans of 8.4 (±1.2) hours per day, with active time of 4.3 (±0.5) hours." §5.1.2: "Every hour, developers take an average of 2.5 (±0.8) short breaks that are about 4.2 (±0.6) minutes long each and in which the developers are not interacting with their computer."
  - p. 1185 (§5.1.3): "Participants used a total of 331 different applications, with each participant using an average of 42.8 (±13.9) different applications over the study duration and 15.8 (±4.1) applications per day." … "Table 3 shows the ten most popular applications across all participants (all were using Windows operating systems)."
  - p. 1185 Table 3 ("Application % of time used # of users"): "Microsoft Outlook 14.2% 18"; "PuTTY 12.8% 8"; "Google Chrome 11.4% 16"; "Microsoft Internet Explorer 9.4% 20"; "Microsoft Visual Studio 8.3% 13"; "File Explorer 6.6% 20"; "Mozilla Firefox 5.9% 8"; "Eclipse 3.0% 10"; "Microsoft OneNote 2.3% 9"; "Command Line 2.2% 16".
  - p. 1185 Table 4 (% of time; duration per day h avg ± sd, max; time before switching min avg ± sd, max): "Coding … 21.0% 1.5 ±1.6 7.3 0.6 ±2.6 135.7"; "Email reading/writing emails 14.5% 1.1 ±1.3 8.1 0.9 ±4.8 89.6"; "Work related browsing … 11.4% 0.8 ±1.3 12.8 0.5 ±5.5 102.6"; "Work unrelated browsing … 5.9% 0.5 ±0.7 3.4 1.1 ±4.3 91.8"; "Planned meeting scheduled meeting/call 6.5% 1.0 ±1.3 7.1 15.8 ±35.3 203.1".
  - p. 1186 (§5.2): "With the exception of planned meetings, a developer only remains in an activity between 0.3 (±2.6) and 2.0 (±6.5) minutes before switching to another one." … "The activity pattern, which occurred most often, was a quick switch to emails during coding tasks." … "Similarly, Amann et al. found that developers continue working while builds run in the background [13]. Developers also regularly switch away from coding to work related web browsing (22.1 percent), reading or writing documents (14.3 percent) or planning (14.2 percent)."
- **Coverage.**
  - T1 (partial): object = distinct applications used per participant-day (15.8 ± 4.1) and over the study (42.8 ± 13.9); named top-10 applications with share of foreground time and number of users (Table 3). Foreground only — not concurrently running processes.
  - T2 covers: object = activity categories derived from foreground process + title sampled every 10 s; unit = minutes before switching; statistic = mean ± SD, max per category (Table 4); breaks per hour; active hours per day; population 20 developers, Windows 7/8/10.
  - T3 covers (partial): most frequent n-gram (coding → email → coding); coding → work browsing 22.1%, → documents 14.3%, → planning 14.2%; activity before informal meeting (email 40.1%, coding 18.1%, browsing 13.5%).
  - T7 (qualitative only): builds run in background (citing Amann et al.). No sizes.
  - T4, T6, T9, T10, T11, T12: does not cover (data not published).
- **One observation?** Yes — one population (20 developers, 4 companies, Windows 7/8/10), 220 work days; calendar window not stated; machines not named.

### S1-06 — González & Mark 2004 (CHI, "working spheres")

- **Citation.** V. M. González, G. Mark. "'Constant, Constant, Multi-tasking Craziness': Managing Multiple Working Spheres." Proc. CHI 2004, Vienna, pp. 113–120. DOI 10.1145/985692.985707.
- **Copy read.** https://ics.uci.edu/~gmark/CHI2004.pdf — author-hosted (8 PDF pages; printed pp. 113–120, PDF p. n = printed 112+n); accessed 2026-09-23; HTTP 200; local `../sources/S1-06/paper.pdf`; SHA-256 `988981bfff2408ba2158cf6bcc8bc24c4b1eed9e9cfd3490c69044ea88dcfac4`.
- **Platform / population / year / method.** 14 information workers (analysts, developers, managers) at one US west-coast investment-management IT outsourcer; shadowing (human observation), ~26 h formal observation each over a seven-month period; OS not stated. Published 2004.
- **Passages.**
  - p. 114: "we conducted an observational study at ITS[footnote marker "1"], an investment management company located on the west coast of the U.S." … "A total of 477 hours was spent in observation at the field site."
  - p. 115: "Fourteen people were observed over a seven-month period. Each person was observed for a period of three and a half days." … "the average time of formal observation for each individual was 26 hours."
  - p. 116 Table 2 ("Average continuous time spent on events before switching (hour:min:sec)"; % entire day, avg time/day (sd), avg time/event (sd)): "Using email 9.17 0:47:46 (0:21:18) 0:02:22 (0:00:27)"; "Using PCs 29.48 2:33:36" (footnote: "Includes both PCs and financial terminals – does not include email").
  - p. 116: "What was most surprising to us was that people spend on the average slightly over three minutes on an event (leaving out formal meetings, unknown, and personal events) before another event is initiated." … "developers spend significantly more time using a PC (mean=4 min. 0 sec., sd=29 sec.) compared with managers (mean=1 min. 58 sec., sd=46 sec.)." … "People spend an average of less than two and a half minutes reading email before they switch to another event, or are interrupted."
  - p. 116 Table 3: "PC 37.01 72.37 3:12:52 (1:13:48) 0:02:52 (0:00:51)" (PC: % entire day, % of device usage, avg time/day, avg time/event); "People spent an average of 2 min. 11 sec. working with any device or paper before they switched to another device or event."
  - p. 117 Table 4: "All All 12.81 (3.39) 0:40:41 (0:50:58) 0:13:49 (0:16:14)" (avg no. of working spheres per person; avg time per WS per day; per segment).
- **Coverage.**
  - T2 covers (at event granularity, observer-coded, not application-level): mean continuous time per event (≈3 min), PC use per event (2:52 mean), email per event (2:22), per-role PC dwell (developers 4:00, managers 1:58); working-sphere segments (mean 13:49 per segment); population 14 workers, one firm.
  - T9 (partial): email use 47:46 per day, 2:22 per continuous stretch — duration, not send frequency.
  - T1, T3, T4, T6, T7, T10, T11, T12: does not cover.
- **One observation?** Yes — one firm, 14 people, seven months (calendar dates not stated); machines/OS not named.

### S1-07 — Weinreich, Obendorf, Herder & Mayer 2008 (TWEB)

- **Citation.** H. Weinreich, H. Obendorf, E. Herder, M. Mayer. "Not Quite the Average: An Empirical Study of Web Use." ACM Transactions on the Web 2(1), Article 5, February 2008. DOI 10.1145/1326561.1326566.
- **Copy read.** https://www.eelcoherder.com/images/publications/2008/not_quite_the_average.pdf — author-hosted, journal pagination 5:1–5:31 (31 PDF pages; PDF page n = article page 5:n); accessed 2026-09-23; HTTP 200; local `../sources/S1-07/paper.pdf`; SHA-256 `c2a2a597698bd686478432a2de2d36b954fe02afc9fa84d7a7fd3c45ba2853f4`.
- **Platform / population / year / method.** Winter 2004/2005; 25 volunteers (Germany/Netherlands; 8 CS university employees); 52–195 days (mean 105); logging intermediary proxy injecting JavaScript for all 25 plus instrumented Firefox for 15. OS not stated in passages read.
- **Passages.**
  - p. 5:5 (§3): "The Web-usage study presented here was conducted in Winter 2004/2005 with 25 unpaid volunteers." … "Most of them came from Germany and the Netherlands".
  - p. 5:7 (§3.2): "every participant had an intermediary installed that filtered all transferred pages, and 15 of the 25 participants additionally made use of an instrumented version of the Firefox browser."
  - p. 5:10 Table I ("This Study" column): "Time of study … 2004–2005"; "No. of users … 25"; "Length (days) … 52–195, ø=105"; "No. of visits … 137,272"; "New window … 10.5%"; "Back … 14.3%".
  - p. 5:15–5:16 (§4.3): "Our participants had on average 2.1 windows or tabs opened when they accessed a new page, suggesting that the use of multiple windows is not an exception, but the rule. However, the individual average differed from 1.07 to 8.19 concurrently opened documents, which shows that this practice was not followed by all users." … "only six of the fifteen Firefox users (40%) regularly opened browser tabs."
  - p. 5:18 (§4.4): "25% of all documents were displayed for less than 4 seconds, and 52% of all visits were shorter than 10 seconds (median: 9.4s). However, nearly 10% of the page visits were longer than two minutes." … "The peak value of the average stay times is located between 2 and 3 seconds; these stay times contribute 8.6% of all visits."
  - p. 5:19: "more than 17% of all new pages were still visited for less than 4 seconds, nearly 50% were shown for less than 12 seconds and 11.6% were displayed for more than 2 minutes (median: 12.4s). However, a fifth of the 11.6% were visits of over 30 minutes to up to 5 days—most of these events are most likely created by unattended browser windows that were left open in the background of the desktop."
- **Coverage.**
  - T4 covers: object = concurrently open browser windows+tabs at each page access; statistic = mean 2.1, per-user means 1.07–8.19; population 25 users, 2004–05.
  - T9 covers: object = page visit (stay time between page display and next navigation); unit = seconds; statistic = median 9.4 s (all), 12.4 s (first visits), quantiles (25% < 4 s; 52% < 10 s; ~10% > 2 min). Total 137,272 visits over mean 105 days per user. Inverse gives a page-load rate while browsing (not published as per-minute).
  - T2 (partial): page stay time is a within-browser dwell time.
  - T1, T3, T6, T7, T10, T11, T12: does not cover.
- **One observation?** Yes — one population (25 users), winter 2004/2005, 52–195 days; OS/machines not named in passages read.

### S1-08 — Huang & White 2010 (Hypertext, parallel browsing)

- **Citation.** J. Huang, R. W. White. "Parallel Browsing Behavior on the Web." Proc. 21st ACM Conference on Hypertext and Hypermedia (HT '10), Toronto, June 13–16 2010. DOI 10.1145/1810617.1810622.
- **Copy read.** https://jeffhuang.com/papers/ParallelBrowsing_HT10.pdf — author-hosted (5 PDF pages); accessed 2026-09-23; HTTP 200; local `../sources/S1-08/paper.pdf`; SHA-256 `0551037335a93bc99306dbf40b7bd57cd75e736c2985ce1506ee6e5bd3b675f9`.
- **Platform / population / year / method.** Logs from an unnamed "widely-distributed browser plug-in" installed alongside "a popular Web browser"; June 2009; >50 million consenting users, ≈ 60 billion pageviews; server-side logging of pageview records. OS not stated.
- **Passages.**
  - p. 2 (§3): "Each pageview by a user triggered the recording of the following fields in logs on our servers, {UserId, Timestamp, TabId, ReferrerUrl, Url, IsQuery}".
  - p. 2 (§3): "We used the entire set of logs from June 2009 containing approximately 60 billion pageviews from over 50 million users, giving us high coverage of Web browsing behavior." … "However, our data did not contain reliable indicators of window creation events, precluding that analysis."
  - p. 3 (§4.1): "The figure shows that 5-10 page views per tab is common, meaning users often visit a handful of pages in each tab. The plot for pageviews per tab resembles a log-normal distribution with parameters [μ] = 0.76, [σ] = 2.16 found using maximum likelihood estimation." (Greek symbols are garbled in the PDF text layer; bracketed symbols are the reader's reconstruction.)
  - p. 3: "Both outclicks and tab switches have good linear fits ([R²] > 0.99) in the log-log plot; they follow a power law distribution … with exponents [k] = 3.2 and [k] = 3.5 respectively."
  - p. 3: "Our logs showed that 88.7% of pageviews and 42.6% of tab sessions did not involve tab switches. That is, users would remain on the same tab for the next pageview in 88.7% of cases, and continuous pageviews comprised entire tab sessions in 42.6% of cases. Conversely, 57.4% of tab sessions had a least one tab switch."
- **Coverage.**
  - T4 covers: object = pageviews per tab (log-normal fit), tab switches per pageview (power law, exponent 3.5), share of pageviews followed by a tab switch (11.3% = 100 − 88.7); population > 50 M users of one browser + plug-in, June 2009. No tab/window counts per session; no per-minute rates.
  - T9 (partial): pageviews per tab; no per-minute page-load rate.
  - T1, T2 (desktop-level), T3, T6, T7, T10, T11, T12: does not cover.
- **One observation?** Yes — one log (June 2009), one browser/plug-in (unnamed); OS and machines not named.

### S1-09 — Reis, Moshchuk & Oskov 2019 (USENIX Security, Site Isolation)

- **Citation.** C. Reis, A. Moshchuk, N. Oskov. "Site Isolation: Process Separation for Web Sites within the Browser." Proc. 28th USENIX Security Symposium, 2019, pp. 1661–1678.
- **Copy read.** https://www.usenix.org/system/files/sec19-reis.pdf — publisher open-access PDF (19 PDF pages; PDF p. 11 carries printed page 1670); accessed 2026-09-23; HTTP 200; local `../sources/S1-09/paper.pdf`; SHA-256 `fc5e13705338c66f219b9aa1385a51a6d9f743fa7e66ef55b48794502e1be6a0`.
- **Platform / population / year / method.** Field telemetry: Chrome 69 on Windows desktops/laptops, two weeks from 1 Oct 2018, equal test/control groups of opted-in users (count not given). Microbenchmark: Chrome 69.0.3497.100 on one Windows 10 desktop (i7-8700K, 16 GB). No Linux data.
- **Passages.**
  - PDF p. 8 (§4.1.1): "we use process consolidation for same-site main frames only after crossing a soft process limit that approximates memory pressure. When the number of processes is below this limit, main frames in independent tabs don't share processes; when above the limit, all new frames start reusing same-site processes when possible. Our threshold is calculated based on performance characteristics of a given machine. Note that Site Isolation cannot support a hard process limit, because the number of sites present in the browser may always exceed it."
  - PDF p. 8 (§4.1.3): "we maintain a warmed-up spare renderer process, which may be used immediately by a new navigation to any site." … "we avoid spare processes on low memory devices, when the system experiences memory pressure, or when the browser goes over the soft process limit."
  - p. 1670 (PDF p. 11, §5.3.1): "The data in this section was collected using pseudonymous metric reporting over a two-week period starting October 1, 2018, from desktop and laptop users of Chrome (version 69) on Windows who have this reporting enabled."
  - p. 1670: "Using periodic samples, we found that users had 6.0 unique sites open across the entire browser at the 50th percentile of the distribution, and 41.9 unique sites at the 99th percentile. This only provides a lower bound for the number of renderer processes; each instance of a site might live in a separate process. If this were the case, our metrics give an upper bound estimate of 79.7 processes at the 99th percentile." … "At the 50th percentile, the number of processes increased 43.5% from 4.4 without Site Isolation to 6.2 with Site Isolation. At the 99th percentile, the process count increased 50.6% from 35.0 to 52.7 processes."
  - p. 1670: "we found that private memory use per renderer process decreased 51.5% (87.2 MB to 42.3 MB) at" [the 50th percentile, continued on next page].
  - PDF p. 13 (§5.3.2): "Our experiments were performed on a Windows 10 desktop with an Intel Core i7-8700K 3.7 GHz 6-core CPU and 16 GB RAM." … "the relative memory overhead generally increases with the number of processes, peaking at 89% for wowprogress.com with 10 processes." … "a heavier amazon.com site has a 5% overhead compared to seatguru.com's 31%, even though both require five" [processes].
- **Coverage.**
  - T4 covers: object = unique sites open and renderer process count across the whole browser; statistic = percentiles (p50: 6.0 sites, 6.2 renderers with Site Isolation, 4.4 without; p99: 41.9 sites, 52.7 renderers, upper bound 79.7); population = Chrome 69 Windows desktop/laptop users with metrics enabled, Oct 2018. Mechanism: per-site processes, same-site consolidation above a machine-dependent soft limit, spare renderer. Per-page renderer counts for specific sites (Fig. 4; e.g. 10 for wowprogress.com, 5 for amazon.com and seatguru.com) on one Windows 10 desktop. Not Linux; tab counts not given.
  - T1, T2, T3, T6, T7, T9–T12: does not cover.
- **One observation?** Two: (a) field telemetry — one population/window named (Chrome 69, Windows, 2 weeks from 2018-10-01), machines not named; (b) microbenchmark — one machine named.

### S1-10 — Terry, Kay, Van Vugt, Slack & Park 2008 (CHI, ingimp)

- **Citation.** M. Terry, M. Kay, B. Van Vugt, B. Slack, T. Park. "ingimp: Introducing Instrumentation to an End-User Open Source Application." Proc. CHI 2008, Florence, pp. 607–616. DOI 10.1145/1357054.1357152.
- **Copy read.** https://www.mjskay.com/papers/chi_2008_ingimp.pdf — co-author-hosted (10 PDF pages); accessed 2026-09-23; HTTP 200; local `../sources/S1-10/paper.pdf`; SHA-256 `1b2bee1e327a7afcdcce01d44bb7aa4c552128b6ce9449ae8c0c925191da694d`.
- **Platform / population / year / method.** Instrumented GIMP ("ingimp"), open-source, distributed incl. Linux; first deployed May 2007; >700 installs in six months; logs command names from the undo stack plus UI events; collected data made public on the ingimp website (availability today not verified). The paper describes method; it reports no usage frequencies.
- **Passages.**
  - PDF p. 7: "ingimp automatically logs all commands that appear on the undo stack. Command names, but not command parameters, are directly recorded in the log file."
  - PDF p. 7: "ingimp logs fundamental user interface-level events: Window events (focus, move, resize), keyboard and mouse usage (but not the actual keys or mouse locations), the state of modifier keys, menu usage, and tool selections."
  - PDF p. 8: "ingimp records basic characteristics of the user's computing environment: Their operating system, the number of monitors, and the resolution of each monitor."
  - PDF p. 1 (abstract): "the augmentation of an open source application to openly collect and publicly disseminate rich application usage data" [quoted as rendered in the abstract, first page].
  - PDF p. 10: "ingimp was first deployed in May 2007 and has been installed by over 700 users in the first six months of its release. We are now just beginning to analyze the data being collected".
- **Coverage.**
  - T9: does not cover with numbers (describes a log of image-editor commands — which would record filter applications — but publishes no rates).
  - T12 (partial): describes a publicly disseminated per-command usage log of an image editor with OS field; population > 700 installs from May 2007; licence/access of the data not stated in the paper; no process-level data.
  - T1–T4, T6, T7, T10, T11: does not cover.
- **One observation?** Describes one deployment (ingimp, from May 2007) but reports no measured values.

### S1-11 — Joo, Ryu, Park & Shin 2011 (FAST '11, application launch on SSD, Linux)

- **Citation.** Y. Joo, J. Ryu, S. Park, K. G. Shin. "FAST: Quick Application Launch on Solid-State Drives." Proc. 9th USENIX Conference on File and Storage Technologies (FAST '11), San Jose, Feb. 2011.
- **Copy read.** https://www.usenix.org/legacy/event/fast11/tech/full_papers/Joo.pdf — publisher open access (14 PDF pages, page numbers printed 1–14); accessed 2026-09-23; HTTP 200; local `../sources/S1-11/paper.pdf`; SHA-256 `a713c64b63644b991601764186f15510ff7e02ee82e00f157905e2095bc586de`.
- **Platform / population / year / method.** One lab desktop: Intel i7-860 2.8 GHz, 4 GB DDR3, Intel X25-M G2 80 GB SSD, Fedora 12, Linux 2.6.32; 22 applications (17 Linux-native + 5 MS Office apps under Wine); cold/warm launches measured with blktrace from execve() to completion of last launch block request. Benchmark, not user observation.
- **Passages.**
  - p. 8 (§5.1): "We used a desktop PC equipped with an Intel i7-860 2.8 GHz CPU, 4GB of PC12800 DDR3 SDRAM and an Intel 80GB SSD (X25-M G2 Mainstream). We installed a Fedora 12 with Linux kernel 2.6.32 on the desktop, in which we set NOOP as the default I/O scheduler."
  - p. 8: "Our benchmark set consists of the following Linux applications: Acrobat reader, Designer-qt4, Eclipse, F-Spot, Firefox, Gimp, Gnome, Houdini, Kdevdesigner, Kdevelop, Konqueror, Labview, Matlab, OpenOffice, Skype, Thunderbird, and XilinxISE. In addition to these, we used Wine [1] … to test Access, Excel, Powerpoint, Visio, and Word".
  - p. 8: "We start an application launch by clicking an icon or inputting a command, and can accurately measure the launch start time by monitoring when execve() is called. Although it is difficult to clearly define the completion of a launch, a reasonable definition is the first moment the application becomes responsive to the user [2]. … we measured the completion time of the last block request in an application launch sequence using Blktrace".
  - p. 9 Table 3 ("# of block requests / # of fetched blocks / # of used files"): "Eclipse 4163 155 216 787"; "Firefox 1566 60 944 433"; "Gimp 1939 66 928 799"; "Gnome 4739 228 872 538"; "OpenOffice 1425 104 600 308"; "Thunderbird 1533 64 784 429"; "Skype 892 41 560 197".
  - p. 9: "Figure 6 shows that the average launch time reduction of FAST is 28% over the cold start scenario. The performance of FAST varies considerably among applications, ranging from 16% to 46% reduction of launch time."
  - p. 12: "we investigated the SSD's maximum idle time during the cold-start of applications, and found it to range from 24 ms (Thunderbird) to 826 ms (Xilinx ISE). … As the maximum cold-start launch time is observed to be less than 10 seconds, 30 seconds may be reasonable for Ttimeout."
  - p. 12: "The average cold start time of the smartphone applications is 6.1 seconds, which is more than twice of the average cold start time of the PC applications (2.4 seconds) shown in Figure 6. Figure 9 also shows that the average warm start time is 63% of the cold start time (almost the same ratio as in Figure 6)".
- **Coverage.**
  - T10 covers: object = application launch (wall time from execve() to last launch I/O); unit = s; statistic = mean cold start 2.4 s across the 22 apps, max < 10 s, warm ≈ 63% of cold; per-application block requests and files touched (Table 3); one Linux desktop with SSD, Fedora 12. Per-app absolute times only in Fig. 6 (normalized); CPU time not reported separately in quotable text. Launch frequency: not covered.
  - T1–T4, T6, T7, T9, T11, T12: does not cover.
- **One observation?** Yes — one machine (named), one OS (Fedora 12 / 2.6.32), benchmark runs; no users.

### S1-12 — Amann, Proksch, Nadi & Mezini 2016 (SANER, Visual Studio usage)

- **Citation.** S. Amann, S. Proksch, S. Nadi, M. Mezini. "A Study of Visual Studio Usage in Practice." Proc. IEEE 23rd International Conference on Software Analysis, Evolution, and Reengineering (SANER 2016), pp. 124–134. DOI 10.1109/SANER.2016.39.
- **Copy read.** https://sarahnadi.org/assets/pdf/pubs/AmannSANER16.pdf — co-author-hosted preprint/camera-ready (11 PDF pages); accessed 2026-09-23; HTTP 200; local `../sources/S1-12/paper.pdf`; SHA-256 `e43c5963aa945e5c31c4008a9c23076c51cccd739a80ab3930264945f50e4c39`.
- **Platform / population / year / method.** Visual Studio (Windows) with the FeedBaG interaction tracker; 27–84 professional C# developers at one company ("CompanyX", tax/accounting software); mid-January to mid-July 2015; 3,505,858 events, > 6,355 work hours, > 800 developer days.
- **Passages.**
  - PDF p. 2 (§III-B): "Timing: Each event contains the timestamp of its occurrence and, if an event takes some time to finish (e.g., when a build of a project is started), its duration." … "Build: When the user runs a build, we capture the target projects, the build duration, and whether it succeeds."
  - PDF p. 5 (§IV-C): "We tracked IDE interactions of developers for about six months, from mid January to mid July 2015. … their numbers to between 27 and 84 (see Section IV-A). The resulting dataset encompasses 3,505,858 events, amounting to over 6,355 hours of work time. From this time, participants spent about 2,103 hours inside Visual Studio."
  - PDF p. 7: "Building: A developer spends 0.9% of her time waiting for builds. Note that this includes only the time from the start of the build to the developer's next interaction. We find that the total build times are about four times larger. This supports our intuition that developers continue working during builds."
  - PDF p. 8 Table III ("Dev. Days with Usage / Usages per Dev. Day / Usages per Usage Day"): "2 Build System 546 (93%) 13.4 14.4". Table II: "10 Build.BuildSolution 5,586 1,7%". "O10: Developers continue working while builds run in the background."
- **Coverage.**
  - T7 covers (partial): object = IDE builds; statistic = 13.4 build-system usages per developer day (14.4 per day with use), share of time waiting for builds 0.9% of in-IDE time, total build time ≈ 4× waiting time; population 27–84 C# developers, one company, Jan–Jul 2015, Visual Studio/Windows. No per-build size or duration distribution in text.
  - T9 covers (analogue): frequency of a heavy in-app operation (build) per developer day.
  - T3 (partial): builds overlap with continued work (O10).
  - T1, T2, T4, T6, T10, T11, T12: does not cover (the dataset itself is not in this paper).
- **One observation?** Yes — one company, 2015-01 to 2015-07, Visual Studio on Windows; machines not named.

### S1-13 — Mark, Iqbal, Czerwinski, Johns & Sano 2016 (CHI, "Neurotics Can't Focus")

- **Citation.** G. Mark, S. T. Iqbal, M. Czerwinski, P. Johns, A. Sano. "Neurotics Can't Focus: An in situ Study of Online Multitasking in the Workplace." Proc. CHI 2016, pp. 1739–1744. DOI 10.1145/2858036.2858202.
- **Copy read.** https://ics.uci.edu/~gmark/Home_page/Publications_files/CHI%2016%20Multitasking%20and%20Focus.pdf — author-hosted (6 PDF pages); accessed 2026-09-23; HTTP 200; local `../sources/S1-13/paper.pdf`; SHA-256 `75224a9aa38fee32ac36c70cfd0831f7291901a19a7a28223eb95311e8a28870`.
- **Platform / population / year / method.** Windows; 40 information workers (20 f, 20 m) at "a large high tech U.S. corporation"; ~12 business days each; custom Windows activity logger (open applications, foreground window, interaction). Published 2016; collection dates not stated.
- **Passages.**
  - PDF p. 2 (Method): "Forty volunteers (20 females, 20 males) in a large high tech U.S. corporation, who responded to an ad, were observed in situ in their real work environment for about 12 business days. Their job roles involved information work and were varied: administrative support, engineering, and management."
  - PDF p. 3: "Participants' computer activity at work was logged during all business hours automatically via custom-built Windows Activity Logging software. This logging software tracks every open application, which window is in the foreground, and whether the user is interacting with that window (with mouse, keyboard, touch, etc.)." … "Focus Duration (online) was measured by dividing total daily logged computer duration by the number of computer screen switches."
  - PDF p. 3 Table 1 ("Avg. online screen focus duration (sec.) and switches"; Mean, sd, Median, %Total): "All computer usage 47.0 21.4 40.2 100%"; "Email usage 61.8 35.1 51.8 33.95"; "Productivity SW usage 64.0 39.3 52.9 21.14"; "Communication SW usage 42.5 25.5 34.5 5.96"; "Daily switches within apps 131.9 103.7 112.0 --"; "Daily switches betw apps 272.7 117.9 261.0 --".
  - PDF p. 3: "Participants had slightly longer focus on email clients, and productivity software (Word, Powerpoint, Excel, Visual Studio, etc.) but had a shorter focus when using communication software (e.g., Skype, IM, Lync)."
- **Coverage.**
  - T2 covers: object = foreground screen focus (daily duration ÷ switches); unit = s; statistic = mean/sd/median across participants (all 47.0/21.4/40.2 s; email 51.8 s median; productivity SW 52.9 s; communication SW 34.5 s); daily switches between apps (median 261.0) and within apps (median 112.0); share of foreground time: email 33.95%, productivity 21.14%, communication 5.96%. Population 40 workers, Windows.
  - T1: the logger records "every open application" but the paper publishes no co-occurrence data — does not cover.
  - T11 (marginal): communication-software foreground share (5.96%) — not process structure.
  - T3, T4, T6, T7, T9, T10, T12: does not cover.
- **One observation?** Yes — one population (40 workers, one corporation), ~12 business days; calendar window and machines not named.

### S1-14 — Tak, Cockburn, Humm, Ahlström, Gutwin & Scarr 2009 (INTERACT, window switching)

- **Citation.** S. Tak, A. Cockburn, K. Humm, D. Ahlström, C. Gutwin, J. Scarr. "Improving Window Switching Interfaces." Proc. INTERACT 2009, Part II, LNCS 5727, Springer, pp. 187–200. DOI 10.1007/978-3-642-03658-3_25.
- **Copy read.** https://opendl.ifip-tc6.org/db/conf/interact/interact2009-2/TakCHAGS09.pdf — IFIP Open Digital Library copy (14 PDF pages); accessed 2026-09-23; HTTP 200; local `../sources/S1-14/paper.pdf`; SHA-256 `4d700b18c50d5700715d7048357be2d322360daed20c949c8955a306cf563535`. (The PDF text layer inserts spurious spaces inside words, e.g. "participa nts"; these are removed in the quotations below and nothing else is changed.)
- **Platform / population / year / method.** Windows XP; 9 frequent computer users (18–55 years), 4 dual-monitor; 8–117 days each, 241 person-days; custom window-event logger; published 2009.
- **Passages.**
  - PDF p. 4 (§3): "We developed logging software for Windows XP that unobtrusively monitors window switches, window creation/destruction events, changes in window geometry, and the method used to switch windows (e.g., Alt+Tab, Taskbar, and direct mouse click). Nine frequent computer users (18 to 55 years old) took part in a study during which we recorded between 8 and 117 days of data per participant." … "Overall, we obtained 241 person-days of data. Only manual window switches were included in the analysis: automatic switches (such as window/dialog pop-ups) were removed from the data. This left a total of 45,377 switch events."
  - PDF p. 4 (§3.1): "The number of window switches per day for participants ranged from 5 to 807, with a cross participant mean of 219 per day (s.d. 91). The number of distinct windows switched to per day ranged from 3 to 177, with a cross participant mean of 39 (s.d. 19)."
  - PDF p. 5: "Adapting this formula for window revisitation gives a mean recurrence rate of 82%; much higher than the 58-61% rate reported for the Web." … "80% of window switches were triggered by between 24 and 40% of windows for the different participants (see Table 1), with a mean of 35.1%."
  - PDF p. 5: "The number of distinct applications used by the participants ranged from 23 to 54, with a mean of 38 (s.d. 10.6)."
  - PDF p. 5 Table 1 (columns: P., single/dual, # days, # switch, # apps, Pareto % Windows, Pareto % Apps, Interface % Click, Taskbar, Alt+Tab), e.g.: "2 dual 117 17088 45 34 7 78.4 21.4 0.2"; "9 single 15 2548 23 37 17 7.6 7.7 84.7".
- **Coverage.**
  - T2 covers: object = manual window switches (foreground changes); unit = switches/day; statistic = cross-participant mean 219 (sd 91), range 5–807; distinct windows switched to per day mean 39; recurrence rate 82%; per-participant switch counts, application counts and switching-method shares (Table 1). Population 9 users, Windows XP. No dwell-time distribution.
  - T1 (partial): distinct applications used over the study (23–54, mean 38) — not concurrent sets; application names not listed in text (Firefox/Outlook given as examples only).
  - T3, T4, T6, T7, T9, T10, T11, T12: does not cover.
- **One observation?** Yes — 9 participants, 241 person-days, Windows XP; calendar window and machines not named.

### S1-15 — Ryu, Lee, Shin & Kang 2023 (FAST '23, Paralfetch)

- **Citation.** J. Ryu, D. Lee, K. G. Shin, K. Kang. "Fast Application Launch on Personal Computing/Communication Devices." Proc. 21st USENIX Conference on File and Storage Technologies (FAST '23), Santa Clara, Feb. 21–23 2023, pp. 425–440 (printed p. 433 on PDF p. 10).
- **Copy read.** https://www.usenix.org/system/files/fast23-ryu.pdf — publisher open access (16 PDF pages incl. cover); accessed 2026-09-23; HTTP 200; local `../sources/S1-15/paper.pdf`; SHA-256 `b88e846aed6569c5bf5050e135f3564c3e74a8ad7c2661be5d7331a6dd310a89`.
- **Platform / population / year / method.** Lab benchmark: laptop Intel Core i5-8265, 16 GB, Samsung 860 QVO 1 TB QLC SSD, Linux 5.4.51; 16 apps (10 desktop incl. Chromium, GIMP, LibreOffice, VLC; 6 games incl. Witcher 3); also Raspberry Pi 3 and Pixel XL. Launch measured from load_elf_binary to completion of a "completion block request".
- **Passages.**
  - PDF p. 11 (§5.1): "In case of Linux, the launch is deemed to start when the load_elf_binary function is called, and to finish when the completion block request has itself completed."
  - PDF p. 11 (§5.2): "We conducted experiments on a laptop PC equipped with an Intel Core i5-8265 CPU and 16 GB of RAM, running Linux kernel 5.4.51. This PC has a 1TB Samsung 860 QVO QLC SSD, which uses native command queuing. We tested Paralfetch, GSoC Prefetch and FAST on 16 applications, 6 of which were games. The 10 non-game applications were Android Studio, Chromium Browser, Eclipse, GIMP, LibreOffice Impress, LibreOffice Writer, Okular, Scribus, VLC player, and Xilinx ISE; and the 6 games were Ancestors Legacy, Atom RPG, Battle Tech, Pillars of Eternity 2, Tyranny, Witcher 3."
  - PDF p. 11: "Paralfetch [reduces] the average launch time of these 16 applications by 44.2% with pre-scheduling alone." (text layer: "Figure 10 shows Paralfetch to reduce the average launch time of these 16 applications by 44.2% with pre-scheduling alone" — a line break separates "Figure 10 shows" from the rest.)
  - PDF p. 12: "application launches are CPU-bound (86% on average in our benchmarks) rather than disk-bound" (Android, Pixel XL, Android 8.0, Linux 3.18.52).
- **Coverage.**
  - T10 (partial): launch-time definition on Linux and relative reductions; absolute per-app launch times are only in Fig. 10 (not recoverable from text layer). CPU-bound share (86%) is for Android games, not the Linux desktop.
  - Others: does not cover.
- **One observation?** Yes — one named laptop, Linux 5.4.51, benchmark runs; no users.

### S1-16 — Koldijk, Sappelli, Verberne, Neerincx & Kraaij 2014 (ICMI, SWELL-KW dataset)

- **Citation.** S. Koldijk, M. Sappelli, S. Verberne, M. A. Neerincx, W. Kraaij. "The SWELL Knowledge Work Dataset for Stress and User Modeling Research." Proc. 16th ACM International Conference on Multimodal Interaction (ICMI 2014), Istanbul, Nov. 12–16 2014. DOI 10.1145/2663204.2663257.
- **Copy read.** https://cs.ru.nl/~skoldijk/Papers/ICMI%202014%20paper_final_cr.pdf — first author's camera-ready, linked from the dataset page http://cs.ru.nl/~skoldijk/SWELL-KW/Dataset.html (8 PDF pages); accessed 2026-09-23; HTTP 200; local `../sources/S1-16/paper.pdf`; SHA-256 `a10bffe9ea55cb66af6a8e7c2b61fbc5dfeffb3ebef57db8ef0f41cc6c1e5720`. (The TNO repository record https://repository.tno.nl/SingleDoc?docId=42707 returned an HTML landing page without the PDF.)
- **Platform / population / year / method.** Lab experiment (not in-the-wild): 25 participants, ~3 h each, a desktop computer with Outlook running, three conditions (neutral ≤ 45 min, time pressure, email interruptions); computer interaction logged with Noldus uLog 3.2.5. OS not stated (Outlook and uLog imply Windows). 2014.
- **Passages.**
  - PDF p. 3 (§3.1): "Neutral: the participant was allowed to work on the tasks as long as he/she needed. After a maximum of 45 minutes the participant was asked to stop" … "Stressor 'Interruptions': 8 emails were sent to the participant during the task."
  - PDF p. 3 (§3.2): "The participants performed knowledge worker tasks on a desktop computer in a controlled lab setting. We asked them to write reports and make presentations on predefined topics (in English)." … "During the task the email program Outlook was running and participants were told to make use of information from incoming emails and reply when necessary."
  - PDF p. 4 (§3.6): "Computer interactions were logged with the key-logging application uLog (version 3.2.5, by Noldus Information Technology), which ran as a background application on the users' computer."
  - PDF p. 5: "The computer logging software recorded detailed timestamped information in XML format about each computer event. Examples of computer events are mouse clicks, mouse scrolls and application changes." Table 2 (per-minute features): "AppChanges … Number of application changes"; "TabfocusChange … Number of tab focus changes".
  - PDF p. 6 Table 1 caption: "Our dataset contains data from 25 participants (3 hours each)."
  - PDF p. 8: "More information on the dataset and its access can be found at http://persistent-identifier.nl/?identifier=urn:nbn:nl:ui:13-kwrv-3e".
- **Coverage.**
  - T12 covers (partial): public dataset with timestamped application-change events (uLog XML) and per-minute AppChanges/TabfocusChange for 25 participants × ~3 h, lab office work (report writing, presentations, browsing, Outlook email). No process creation data; application names in raw logs not described in the paper. Licence not stated in the paper (access via DANS persistent identifier).
  - T2 (dataset only): per-minute application-change counts — values not published in the text read.
  - T3 (partial): tasks are prescribed (write report/presentation, answer emails) — a lab workflow definition, not observed order.
  - T1, T4, T6, T7, T9, T10, T11: does not cover.
- **One observation?** Yes — one lab study, 25 participants, 3 h each; machine not named; year of collection not stated (published 2014).

### S1-17 — Sánchez Sánchez et al. 2020 (Data in Brief, BEHACOM dataset)

- **Citation.** P. M. Sánchez Sánchez, J. M. Jorquera Valero, M. Zago, A. Huertas Celdrán, L. Fernández Maimó, E. López Bernal, S. López Bernal, J. Martínez Valverde, P. Nespoli, J. Pastor Galindo, Á. L. Perales Gómez, M. Gil Pérez, G. Martínez Pérez. "BEHACOM – a dataset modelling users' behaviour in computers." Data in Brief 31 (2020) 105767. DOI 10.1016/j.dib.2020.105767. CC BY 4.0.
- **Copy read.** https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7270191/fullTextXML — Europe PMC full-text XML of the published article (PMC7270191); accessed 2026-09-23; HTTP 200; local `../sources/S1-17/paper.xml`; SHA-256 `c7880aa76a91786aa91fa5e76f331cb8db3370967b53f9007f5feb17d8f3ccfd`. (https://pmc.ncbi.nlm.nih.gov/articles/PMC7270191/ returned a reCAPTCHA challenge page, HTTP 200 but no article.) Locators are article sections.
- **Platform / population / year / method.** 12 users, 55 consecutive days, own personal computers, unrestricted use; 8 Windows, 3 Linux (Debian-based), 1 both; Python collector (psutil; xdotool on Linux, pywin32 on Windows); features per one-minute window; data on Mendeley Data (DOI 10.17632/cg4br62535). Collection dates not stated in passages read.
- **Passages.**
  - Abstract: "This paper details the methodology and approach conducted to monitor the behaviour of twelve users interacting with their computers for fifty-five consecutive days without preestablished indications or restrictions. The generated dataset, called BEHACOM, contains for each user a set of features that models, in one-minute time windows, the usage of computer resources such as CPU or memory, as well as the activities registered by applications, mouse and keyboard."
  - Specifications table: "How data were acquired Client application for Windows and Linux operating systems"; "Data identification number: 10.17632/cg4br62535".
  - §2 (Scenario description): "The proposed scenario comprises twelve different individuals interacting for fifty-five consecutive days with their personal computers in their own way and without restrictions. Eight of them use Windows as operating system, three Linux, and one both."
  - Table 5: "active_apps_average Average number of applications active during the time window." … "current_app Application executable name in foreground when the vector was generated." … "changes_between_apps Number of changes between different foreground applications during the time window." … "current_app_average_processes Average number of processes that the current application in foreground had active during the time window."
  - Table 6: "system_average_cpu Average of the percentage of system CPU capacity used in total during the time window."
  - §3: "To obtain the process identifier (pid) of the application in foreground, xdotool [8] is used in the Linux implementation and pywin32 (win32process and win32gui) [9] in Windows. Process names, CPU, memory and network usage are obtained by the psutil [10] library, in both operating systems."
  - §1.1: "The data repository of BEHACOM is publicly available in Mendeley Data [1]."
- **Coverage.**
  - T12 covers: public per-minute dataset with foreground executable name, number of active applications, foreground-app process count, app switches per minute, CPU/memory; 12 users (4 with Linux), 55 days; licence of the article CC BY (dataset licence not stated in the article text read).
  - T1 (dataset only): active applications per minute and foreground app names exist in the data; the article publishes no statistics.
  - T2 (dataset only): changes between foreground apps per minute and foreground seconds; no statistics in article.
  - T3, T4, T6, T7, T9, T10, T11: does not cover.
- **One observation?** Yes — one population (12 users, University of Murcia context), 55 days; machines not named; calendar dates not given in passages read.

### S1-18 — Anjum, Iqbal & Hamelin 2021 (SACMAT, DARPA OpTC)

- **Citation.** Md. M. Anjum, S. Iqbal, B. Hamelin. "Analyzing the Usefulness of the DARPA OpTC Dataset in Cyber Threat Detection Research." Proc. 26th ACM Symposium on Access Control Models and Technologies (SACMAT '21), pp. 27–32, 2021. DOI 10.1145/3450569.3463573.
- **Copy read.** https://nrc-publications.canada.ca/fra/voir/auteur/version/?id=258e6cfb-8da9-4251-aaad-002142ccdb4a — NRC Publications Archive author version with cover sheet (7 PDF pages; PDF p. 1 is the archive cover); accessed 2026-09-23; HTTP 200; local `../sources/S1-18/paper.pdf`; SHA-256 `a69868074dc9088dd607312527b8246206d8a882517d5a0afd12090006d0a876`. (ACM DL PDF https://dl.acm.org/doi/pdf/10.1145/3450569.3463573 → HTTP 403.)
- **Platform / population / year / method.** 1,000 Windows 10 hosts in a DARPA testbed; endpoint sensor → eCAR JSON; benign period 19–23 September, red-team 23–25 September (year 2019 per the paper's reference "[6] DARPA. 2019. Operationally Transparent Cyber Dataset"); benign activity is testbed activity, not described as real users.
- **Passages.**
  - PDF p. 3 (§2.2): "The experiment testbed consisted of 1000 hosts with Windows 10 operating system. Each host of the experimental setup was equipped with a sensor. This sensor monitored the events and packed them into JSON records, which were dispatched to a central Kafka queue."
  - PDF p. 3 (§2.3): "an event with the object "process" and action "create" has fields like command line, name, and process id."
  - PDF p. 3 (§3.1): "The OpTC dataset contains around 1,100 gigabytes of data in the compressed JSON format." … "The benign folder stores the normal activity captured between 19th and 23rd September. The evaluation folder stores events captured during the red team activity period, between September 23 and September 25."
  - PDF p. 3 (§3.2): "The OpTC dataset has 17,433,324,390 events. These events split across 11 different object types, with 32 different (object/action) pairs." … "Regardless of the host, the process name (.exe) remains the same. Therefore, we categorize the process name as permanent."
  - PDF p. 4: "most of the dataset events consist of the FLOW, FILE and PROCESS objects. In total, these three events constitute more than 90% of the entire dataset".
- **Coverage.**
  - T12 covers: public process-creation/termination trace with process names, command lines and timestamps; 1,000 Windows 10 hosts; ~5 benign days (Sept 2019) + 2 red-team days; ~17.4 billion events. Nature of benign user activity (human vs scripted) not stated in the paper. Licence not stated in the paper.
  - T1 (dataset only): co-running processes per host derivable; no statistics published.
  - Others: does not cover.
- **One observation?** Yes — one testbed, 1,000 hosts, Sept 2019; hosts' hardware not named.

### S1-19 — Kent 2015 (LANL "Comprehensive, Multi-Source Cyber-Security Events")

- **Citation.** A. D. Kent. "Comprehensive, Multi-Source Cyber-Security Events." Los Alamos National Laboratory, 2015 (dataset), DOI via OSTI 10.17021/1179829; described in A. D. Kent, "Cybersecurity Data Sources for Dynamic Network Research," in Dynamic Networks in Cybersecurity, Imperial College Press, June 2015 (chapter not obtained — publisher copy not openly available; the dataset page below is the primary description read).
- **Copy read.** https://csr.lanl.gov/data/cyber1/ — LANL dataset page (HTML); accessed 2026-09-23; HTTP 200; local `../sources/S1-19/page.html`; SHA-256 `d8aa79edfbe50e139971687e92b591c5ceaed7686d8a7b21e4669df419f0881e`.
- **Platform / population / year / method.** LANL corporate network; Windows desktops and servers; 58 consecutive days (timeframe undisclosed); de-identified; 12,425 users, 17,684 computers, 62,974 processes; process start/stop events at 1 s resolution.
- **Passages.**
  - "This data set represents 58 consecutive days of de-identified event data collected from five sources within Los Alamos National Laboratory's corporate, internal computer network."
  - "In total, the data set is approximately 12 gigabytes compressed across the five data elements and presents 1,648,275,307 events in total for 12,425 users, 17,684 computers, and 62,974 processes."
  - "All other users, computers, process, ports, times, and other details were de-identified as a unified set across all the data elements (e.g. U1 is the same U1 in all of the data). The specific timeframe used is not disclosed for security purposes." … "All data starts with a time epoch of 1 using a time resolution of 1 second."
  - "proc.txt.gz — This data represents process start and stop events collected from individual Windows-based desktop computers and servers. Each event is on a separate line in the form of "time,user@domain,computer,process name,start/end"". Example line: "1,C553$@DOM1,C553,P16,Start".
  - "To download the data set, please help us understand how it will be used." Files listed: "proc.txt.gz (2.2G)".
- **Coverage.**
  - T12 covers: public process start/stop trace, Windows desktops+servers, 58 days, 17,684 computers; process names de-identified (e.g. "P16") — so real process names are NOT given; desktop vs server not distinguished in the record format. Access by web form; licence not stated on the page.
  - T1 (dataset only): concurrency of (pseudonymous) processes per computer derivable; no names.
  - Others: does not cover.
- **One observation?** Yes — one network (LANL), 58 days, timeframe undisclosed.

### S1-20 — Xue, Li, Mullally, Ni, Nichols, Heddaya & Murphy (Microsoft, Windows RAC telemetry)

- **Citation.** S. Xue, P. L. Li, J. P. Mullally, M. Ni, G. Nichols, S. Heddaya, B. Murphy. "Predicting the Reliability of Mass-Market Software in the Marketplace Based on Beta Usage: a Study of Windows Vista and Windows 7." Microsoft Research-hosted manuscript (filename indicates an ICSE 2010 research submission; venue of final publication not verified).
- **Copy read.** https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/Windows20Reliability20ICSE20Research20Submission202010.pdf (10 PDF pages); accessed 2026-09-23; HTTP 200; local `../sources/S1-20/paper.pdf`; SHA-256 `c902dabe7f76bb7faae3f4cd808bc1d60c71dfeb25ec37cca8da128263e58f7c`.
- **Platform / population / year / method.** Windows Vista/7 opt-in telemetry (Reliability Analysis Component, RAC) from "a few million machines"; vendor-internal, not public.
- **Passages.**
  - PDF p. 1: "Nearly half a million unique devices and over 6 million applications have been run on Windows Vista®."
  - PDF p. 3 (§3.2): "Metric data consists of counts of occurrences (e.g. system boot, application launch) and time durations in certain states (e.g. OS uptime, application uptime). Metrics are computed on pre-defined intervals (e.g. every 3 days)." … "State transitions: launches, terminations, and sleep transitions for the OS, services, and applications. Each state change is recorded with an associated timestamp and the appropriate parameters."
  - PDF p. 3: "RAC randomly selects a few million machines from the CEIP population."
- **Coverage.**
  - T10 / T12: describes vendor telemetry that records application launches and uptimes with timestamps, but publishes no launch counts or rates and the data are not public — does not cover with values.
  - Others: does not cover.
- **One observation?** Not an observation with published values.

### S1-21 — Mark, Iqbal, Czerwinski, Johns & Sano 2016 (CHI, email duration and checks)

- **Citation.** G. Mark, S. T. Iqbal, M. Czerwinski, P. Johns, A. Sano. "Email Duration, Batching and Self-interruption: Patterns of Email Use on Productivity and Stress." Proc. CHI 2016, pp. 1717–1728. DOI 10.1145/2858036.2858262.
- **Copy read.** https://www.microsoft.com/en-us/research/wp-content/uploads/2016/06/Email20Duration20Camera20Ready20submission3-1.pdf — Microsoft Research-hosted camera-ready (12 PDF pages); accessed 2026-09-23; HTTP 200; local `../sources/S1-21/paper.pdf`; SHA-256 `40f72b03495c32fe1ba6bf567e669be7192f6d7398080705e1b76d074759a192`.
- **Platform / population / year / method.** Same study population as S1-13: 40 volunteers in a research division of a large corporation; ~12 business days; custom Windows Activity Logging software (foreground window, open applications); heart-rate monitors. Published 2016.
- **Passages.**
  - PDF p. 4: "We conducted an in situ study with 40 participants (20 females, 20 males). Participants were volunteers working in a research division of a large corporation, and worked in different job roles: administrative support, engineering, and management." … "participants averaged 12 study days."
  - PDF p. 4: "Time spent on email was logged automatically via custom-built Windows Activity Logging software. This logging software tracks every open application, which window is in the foreground, and whether the user is interacting with that window".
  - PDF p. 5 (measures): "Email Checks was measured as the number of separate times that the email client switched to the foreground."
  - PDF p. 7: "The total hours of data collected for window logging was 1981.5, with an average of 49.5 hours of computer screen data logged per participant." … "the average daily time spent by our participants on the computer (averaged over work days) is about four and a half hours. Our 40 participants averaged almost one and a half hours per day of time on email and checked their email on average 77 times per day."
  - PDF p. 2 (related work, secondary): "Mark et al. [26] found that users in a logging study spent an average of 34.5 minutes per day on email."
- **Coverage.**
  - T9 covers (partial): object = email-client foreground activations ("checks"); unit = per day; statistic = mean 77 checks/day; email time ≈ 1.5 h/day of ≈ 4.5 h computer time; population 40 workers, Windows. Send frequency and attachments: not covered.
  - T2 covers (partial): email client foreground activations per day.
  - T1, T3, T4, T6, T7, T10, T11, T12: does not cover.
- **One observation?** Yes — same 40-person population as S1-13 (not independent of S1-13); ~12 days; calendar dates and machines not named.

### S1-22 — Chang, Varvello, Hao & Mukherjee 2021 (IMC, Zoom/Webex/Meet)

- **Citation.** H. Chang, M. Varvello, F. Hao, S. Mukherjee. "Can You See Me Now? A Measurement Study of Zoom, Webex, and Meet." Proc. ACM Internet Measurement Conference (IMC '21). DOI 10.1145/3487552.3487847. arXiv:2109.13113v1.
- **Copy read.** https://arxiv.org/pdf/2109.13113v1 — arXiv v1 (13 PDF pages); accessed 2026-09-23; HTTP 200; local `../sources/S1-22/paper.pdf`; SHA-256 `639750300ce4c7f36b62180cdf4f3f5c5d9e102a3f68c3cc280be036fd7a6815`.
- **Platform / population / year / method.** Emulated clients on Linux cloud VMs (8 vCPU Xeon Platinum 8272CL, 16 GB) plus Android phones; April–May 2021; CPU usage reported for Android devices only.
- **Passages.**
  - PDF p. 4: "The experiments were conducted from 4/2021 to 5/2021."
  - PDF p. 4 (§4.1): "Each cloud VM we deploy has 8 vCPUs (Intel Xeon Platinum 8272CL with 2.60GHz), 16GB memory and 30GB SSD." … "We use the native Linux client for Zoom (v5.4.9 (57862.0110)), and the web client for Webex and Meet since they do not provide a native Linux client."
  - PDF p. 3 (§3): "In Linux, snd-aloop and" [v4l2loopback are used to emulate devices — continuation not quoted] … "(e.g., xdotool for Linux, …)" for UI automation.
- **Coverage.**
  - T11 (marginal): establishes that in 2021 Zoom had a native Linux client (v5.4.9) while Webex and Meet were used via the web client on Linux; no process structure, process names or Linux CPU figures (CPU usage reported only for Android devices S10/J3).
  - Others: does not cover.
- **One observation?** Lab measurement; VMs named; no users.

### S1-23 — Ghaleb, da Costa & Zou 2019 (EMSE, CI build durations)

- **Citation.** T. A. Ghaleb, D. A. da Costa, Y. Zou. "An Empirical Study of the Long Duration of Continuous Integration Builds." Empirical Software Engineering 24 (2019). DOI 10.1007/s10664-019-09695-9.
- **Copy read.** https://seal-queensu.github.io/publications/pdf/EMSE-Taher-2019.pdf — author pre-print (33 PDF pages); accessed 2026-09-23; HTTP 200; local `../sources/S1-23/paper.pdf`; SHA-256 `57c0d1c8d015d8d4c18ec983ded1ace67085d5935101b77a52680547ba0ab834`.
- **Platform / population / year / method.** Travis CI (cloud CI, not desktops); 104,442 builds of 67 GitHub projects (Ruby/Java) drawn from TravisTorrent (11.1.2017 release), selected for high build-duration variability (MAD > 10 min).
- **Passages.**
  - PDF p. 3: "our exploration of 104,442 CI builds of 67 projects reveals that 84% of CI builds last more than the acceptable 10 minutes duration [11,28]."
  - PDF p. 3: "our study selects projects with high variations of build durations where the problem of long build durations may occur. To this end, we select 67 projects that have a build durations Median Absolute Deviation (MAD) above 10 minutes".
  - PDF p. 3: "We observe that 40% of builds in the studied projects have durations of more than 30 minutes."
- **Coverage.**
  - T7 (weak, off-population): CI build (incl. tests) wall durations on hosted CI for a sample deliberately biased to long builds; not desktop builds, no object counts, no relation to a kernel build.
  - Others: does not cover.
- **One observation?** Yes — one dataset (TravisTorrent 2017 release, 67 projects); CI machines not named.

### S1-24 — Iqbal & Horvitz 2007 (CHI, disruption and recovery; DART logger)

- **Citation.** S. T. Iqbal, E. Horvitz. "Disruption and Recovery of Computing Tasks: Field Study, Analysis, and Directions." Proc. CHI 2007, pp. 677–686. DOI 10.1145/1240624.1240730.
- **Copy read.** https://www.microsoft.com/en-us/research/wp-content/uploads/2016/11/CHI_2007_Iqbal_Horvitz-1.pdf — Microsoft Research-hosted (10 PDF pages); accessed 2026-09-23; HTTP 200; local `../sources/S1-24/paper.pdf`; SHA-256 `1be444bb4947ed868306b328422c176f665cdc44c316d754eaa9893bfbafa761`. (Text layer inserts spurious spaces inside words; removed in quotations, nothing else changed.)
- **Platform / population / year / method.** Windows (Outlook, Windows Messenger, MSN Messenger, Office Communicator named); 27 people at Microsoft Research ("our organization"); 2 weeks; DART logger on the Eve monitoring infrastructure (window names/sizes, open/close, switches, input). Published 2007.
- **Passages.**
  - PDF p. 4: "DART runs as a background process, and continues to logs the name, size, and location of all windows on a computing system, noting the opening and closing of windows. The system also logs user activities, including when users are actively engaged with the software, keyboard and mouse activity, and switches among windows as well as actions of saving, cutting, and pasting."
  - PDF p. 4: "We deployed DART on the primary machines of 27 people at our organization, whose job descriptions ranged from program manager, administrator, and researcher to software developer."
  - PDF p. 4: "We collected 2,267 hours of activity data over a period of 2 weeks, resulting in 974 sessions (M(session length)=2h, 17m, S.D=410.37 m). A session was defined as delimited by either the logging on and off or by the unlocking and locking of a machine."
  - PDF p. 4: "We focused on characterizing the behaviors of users in response to alerts generated by Outlook, a widely used email client, and IM clients, including Windows Messenger, MSN Messenger, and Office Communicator."
  - PDF p. 5: "Preliminary analysis showed that, on average, the maximum time spent on an application before switching to another is just above 4 minutes, with an average of below a minute."
  - PDF p. 5: "on an hourly basis, a user's primary tasks were interrupted by an average of 4.28 email (S.D.=5.56) alerts and 3.21 IM (S.D.=4.31) alerts, with an overall average rate of 3.74/hour (S.D.=4.94)."
  - PDF p. 5: "For 40.8% (2344/5747) of the email alerts, users responded immediately (<15s), leaving on average 3 (S.D.=1.92) task windows suspended."
- **Coverage.**
  - T2 covers: session length (logon/unlock to logoff/lock) mean 2 h 17 min (SD 410.37 min), 974 sessions; average time on an application before switching "below a minute", average maximum "just above 4 minutes"; population 27 Microsoft employees, Windows, 2 weeks.
  - T1 (partial): background communication clients named (Outlook, Windows Messenger, MSN Messenger, Office Communicator) running alongside primary tasks; suspended task windows at email-alert response: mean 3 (SD 1.92).
  - T9 (partial): incoming email alerts 4.28/h, IM alerts 3.21/h — incoming, not sends.
  - T3, T4, T6, T7, T10, T11, T12: does not cover.
- **One observation?** Yes — 27 people, one organization, 2 weeks; calendar dates and machines not named.

### S1-25 — Cao, Lee, Iqbal, Czerwinski, Wong, Rintel, Hecht, Teevan & Yang 2021 (CHI, multitasking in remote meetings)

- **Citation.** H. Cao, C.-J. Lee, S. Iqbal, M. Czerwinski, P. Wong, S. Rintel, B. Hecht, J. Teevan, L. Yang. "Large Scale Analysis of Multitasking Behavior During Remote Meetings." Proc. CHI 2021. DOI 10.1145/3411764.3445243. arXiv:2101.11865. (Author list after "Brent Hecht" taken from the arXiv record, not verified on the PDF page read.)
- **Copy read.** https://arxiv.org/pdf/2101.11865 — arXiv preprint (13 PDF pages; header still carries the "Conference'17" template); accessed 2026-09-23; HTTP 200; local `../sources/S1-25/paper.pdf`; SHA-256 `48b9694b1064bb8e12cea4526317515fb3f933568f80c92f6a11e90f410ad02f`.
- **Platform / population / year / method.** Vendor telemetry (Microsoft Teams meetings, Outlook send/reply/forward events, OneDrive/SharePoint file edits) of US Microsoft employees; four week-long snapshots Feb 24–28, Mar 23–27, Apr 20–24, May 18–22 2020; 34,524 (meeting, user) records in the May regression; plus a diary study. OS not stated. Not public.
- **Passages.**
  - PDF p. 3 (§3.1): "We collected metadata (without any content information) on remote meetings (Microsoft Teams), email usage (Microsoft Outlook), and file edits (Onedrive/Sharepoint) of US employees from Microsoft." … "We collected four separate week-long snapshots of data from February to May, 2020".
  - PDF p. 4: "on Microsoft Outlook, we collected the time when people actively send, respond to, or forward an email. On file platforms, we recorded events related to editing productivity-related files, including Excel, Powerpoint, Word, and PDFs."
  - PDF p. 4: "We joined three data sources by unique user identifiers (anonymized), which resulted in 34,524 (meeting, user) records. For each (meeting, user) pair, we labeled it as email multitasking (Y = 1) if the user was found to have at least one active email action during the meeting".
  - PDF p. 5: "from February to May, we find that 31.1%, 30.9%, 29.2%, and 28.9% meetings involve email multitasking, and 23.7%, 23.1%, 24.8%, and 25.5% meetings involve file multitasking."
  - PDF p. 3 footnote: "We only included meetings that are longer than two minutes to filter out data noise. We also filtered out meetings lasting longer than 3 hours".
- **Coverage.**
  - T11 covers (partial): object = video meetings (Teams); statistic = share of (meeting, user) pairs with ≥ 1 email send/reply/forward during the meeting (28.9–31.1%) and with a file edit (23.1–25.5%), by week in 2020; population = US Microsoft employees. No process structure; not Linux.
  - T1 (partial): co-occurrence of video call with email client activity and Office file editing (share of meetings).
  - T9 (partial): email send events as an operation during calls; no per-minute rate in text.
  - Others: does not cover.
- **One observation?** Yes — one population (Microsoft US employees), four named weeks in 2020; machines/OS not named.

### S1-26 — Forget et al. 2016 (SOUPS, Security Behavior Observatory)

- **Citation.** A. Forget, S. Pearman, J. Thomas, A. Acquisti, N. Christin, L. F. Cranor, S. Egelman, M. Harbach, R. Telang. "Do or Do Not, There Is No Try: User Engagement May Not Improve Security Outcomes." Proc. SOUPS 2016, Denver, June 22–24 2016, pp. 97–111. (Author list beyond first author from the USENIX program; not verified on the pages quoted.)
- **Copy read.** https://www.usenix.org/system/files/conference/soups2016/soups2016-paper-forget.pdf — USENIX open-access proceedings (16 PDF pages incl. cover; printed pp. 97ff.); accessed 2026-09-23; HTTP 200; local `../sources/S1-26/paper.pdf`; SHA-256 `2804d275e6eb2e5798beed3140a52e06c21f2e8f4c576634010a9ebb77ab7ea2`. (pypdf text layer is garbled for this file; text extracted with pdfminer.six.)
- **Platform / population / year / method.** Home Windows Vista/7/8/10 computers of Pittsburgh-area participants; SBO client sensors; initial study observed 73 users over 9 months. Data not public.
- **Passages.**
  - PDF p. 2: "After observing 73 users over the course of 9 months, we conducted interviews with 15 users whose computers were in a variety of security states".
  - PDF p. 4 (§3): "Potential participants are contacted to complete a brief pre-enrollment survey to ensure they are over 18 and own a Windows Vista, 7, 8, or 10 personal computer."
  - PDF p. 4: "Examples of collected data include processes, installed software, web browsing behavior, network packet headers, wireless network connections, Windows event logs, Windows registry data, and Windows update data."
- **Coverage.**
  - T12 (partial): a longitudinal home-computer panel that records processes, but the data are not public; no process statistics in this paper.
  - T6 (Windows, qualitative): examines Windows update state of home machines (not quoted; not Linux).
  - Others: does not cover.
- **One observation?** One panel (73 users, 9 months); no process-level values published.

### S1-27 — UL Benchmarks, PCMark 10 Technical Guide (updated 11 Feb 2021) — grey literature (benchmark vendor)

- **Citation.** UL Benchmarks. "PCMark 10 Technical Guide." Updated February 11, 2021. 141 pp. (Benchmark vendor documentation, not peer-reviewed; included for T3/T10 because the input names "benchmark suites' own workload orders".)
- **Copy read.** https://s3.amazonaws.com/download-aws.futuremark.com/pcmark10-technical-guide.pdf (141 PDF pages, each page printed "Page n of 141"); accessed 2026-09-23; HTTP 200; local `../sources/S1-27/paper.pdf`; SHA-256 `d7603a6cb96c78bd22b2721418361ecb92168d785846f241423bd943bb956067`.
- **Platform / population / year / method.** Windows 10 benchmark; scripted workloads; no users.
- **Passages.**
  - p. 4: "PCMark 10 is the latest in our series of industry standard PC benchmarks. Updated for Windows 10 with new and improved workloads".
  - p. 41 (benchmark structure table, "Benchmark / Test Groups / Workloads"): "PCMark 10 benchmark — Essentials: App Start-up, Web Browsing, Video Conferencing — Productivity: Writing, Spreadsheets — Digital Content Creation (DCC): Photo Editing, Video Editing, Rendering and Visualization" (table cells flattened in extraction; wording as in the cells).
  - p. 49: "The Essentials test group contains workloads that are relevant to the majority of desktop and laptop Windows PC users. It includes the following workloads: 1. App Start-up 2. Web Browsing 3. Video Conferencing".
  - p. 50: "The test has three parts: initialization, warm start, and cold start. For the initialization part, all the applications are started once then closed. For each application in the warm start part of the test: 1. Start the application. 2. Measure the time taken until the application is responsive. 3. Close the application. 4. Repeat from step 1 five times." (cold start adds "1. Flush the system cache.")
  - p. 50: "• Chromium web browser • Firefox web browser • LibreOffice Writer word processing program • GIMP image manipulation program".
  - p. 51 ("RESULT DEFINITION UNIT TYPICAL RANGE"): "R1 Writer warm start s 0.9-1.8"; "R2 Writer cold start s 3.0-8.0"; "R3 GIMP warm start s 1.8-3.2"; "R4 GIMP cold start s 4.5-9.1"; "R5 Chromium warm start s 0.17-0.35"; "R6 Chromium cold start s 1.3-3.0"; "R7 Firefox warm start s 0.86-1.8"; "R8 Firefox cold start s 2.0-5.4".
  - p. 52: "The Web Browsing test utilizes two browsers: Firefox and Google Chromium." … "The web pages are shown using both browsers, except the video page that is only run on Chromium. All the pages are run 2 times in both browsers."
  - p. 57: "Part 1: one-to-one video conferencing with basic quality video • Encode: 720p, 30 FPS, H.264 video, bitrate 14380 kb/s • Playback: 720p, 30 FPS, H.264 video, bitrate 11773 kb/s • Two video streams (a local and a remote one)" … "Runtime: 10s".
  - p. 70: "Digital Content Creation test group tests performance in video, photo and 3D content creation. It includes the following tests: 1. Photo Editing 2. Video Editing 3. Rendering and Visualization".
  - p. 72: "2. Apply brightness, contrast, saturation, unsharp mask, Gaussian noise, Gaussian blur, a further unsharp mask, local contrast and wavelet denoise to the source image via sliders in the user interface and display the resulting image in the adjustment view. Each slider is moved 2-5 times, depending on the operation. After each filtering pass constituting a secondary result, each image is saved on disk in JPEG and PNG formats."
- **Coverage.**
  - T3 covers (definition, not observation): benchmark's own workload order — Essentials (App Start-up → Web Browsing → Video Conferencing) → Productivity (Writing, Spreadsheets) → DCC (Photo Editing → Video Editing → Rendering and Visualization); within Photo Editing a fixed filter sequence. No real-user support for the order is claimed in passages read.
  - T10 covers (Windows, benchmark): "typical range" of warm/cold launch time until responsive for LibreOffice Writer, GIMP, Chromium, Firefox (cold 1.3–9.1 s; warm 0.17–3.2 s).
  - T9 (definition): photo-editing filter chain (each slider moved 2–5 times) — scripted, not observed frequency.
  - T11 (definition): video-conferencing workload = 720p/1080p H.264 encode + 1–3 remote 720p decodes, 10 s runtime — synthetic, not a real client's process structure.
  - T1, T2, T4, T6, T7, T12: does not cover.
- **One observation?** No — a benchmark definition; "typical ranges" have no stated machine population.

### S1-28 — Wallace, Douglis, Qian, Shilane, Smaldone, Chamness & Hsu 2012 (FAST, backup workloads)

- **Citation.** G. Wallace, F. Douglis, H. Qian, P. Shilane, S. Smaldone, M. Chamness, W. Hsu. "Characteristics of Backup Workloads in Production Systems." Proc. 10th USENIX Conference on File and Storage Technologies (FAST '12), 2012.
- **Copy read.** https://www.usenix.org/system/files/conference/fast12/wallace.pdf — publisher open access (16 PDF pages); accessed 2026-09-23; HTTP 200; local `../sources/S1-28/paper.pdf`; SHA-256 `c1ce67d8262d36f0f51500db2cbcfb182f46c110994d677ce5903c1c530430ff`.
- **Platform / population / year / method.** Enterprise backup appliances (EMC Data Domain), autosupport statistics from 10,000+ systems plus content metadata (~700 TB); not desktops.
- **Passages.**
  - PDF p. 1: "[a backup] might typically consist of a full copy of the primary data once per week (i.e., a weekly full), plus a daily backup of the files modified since the previous backup (i.e., a daily incremental)." (the text layer interleaves a footnote line "∗Current affiliation: Case Western Reserve University." inside this sentence).
  - PDF p. 2: "Backups usually run regularly, with the most common paradigm being weekly "full" backups and daily "incremental" backups."
  - PDF p. 1 (abstract): "several production systems storing almost 700TB of backup data".
- **Coverage.**
  - T7 (weak, off-population): enterprise backup schedule paradigm (weekly full + daily incremental); no desktop backup sizes or durations quoted.
  - Others: does not cover.
- **One observation?** Enterprise fleet (10,000+ systems); not a desktop observation.

### S1-29 — Lottarini et al. 2018 (ASPLOS, vbench)

- **Citation.** A. Lottarini, A. Ramirez, J. Coburn, M. A. Kim, P. Ranganathan, D. Stodolsky, M. Wachsler. "vbench: Benchmarking Video Transcoding in the Cloud." Proc. ASPLOS 2018. DOI 10.1145/3173162.3173207.
- **Copy read.** https://arcade.cs.columbia.edu/vbench-asplos18.pdf (13 PDF pages); accessed 2026-09-23; HTTP 200; local `../sources/S1-29/paper.pdf`; SHA-256 `3fe35adf60a7fcfc6e5ed130f9e077fdcd878d8753410f4c3c557a83fdc0e437`.
- **Platform / population / year / method.** Cloud transcoding benchmark derived from a YouTube upload corpus; not desktop.
- **Passages.**
  - PDF p. 2: "this paper presents a video transcoding benchmark, vbench, that reflects the transcode demands of a video sharing service such as YouTube. … vbench uses clustering techniques to select 15 videos of 5 seconds each."
- **Coverage.**
  - T7 (weak, off-population): benchmark clip length (5 s), not typical desktop render/transcode job lengths.
  - Others: does not cover.
- **One observation?** No — benchmark definition.

### S1-30 — Oliner, Iyer, Stoica, Lagerspetz & Tarkoma 2013 (SenSys, Carat)

- **Citation.** A. J. Oliner, A. P. Iyer, I. Stoica, E. Lagerspetz, S. Tarkoma. "Carat: Collaborative Energy Diagnosis for Mobile Devices." Proc. ACM SenSys 2013. DOI 10.1145/2517351.2517354.
- **Copy read.** https://amplab.cs.berkeley.edu/wp-content/uploads/2013/10/oliner-Carat-SenSys13.pdf (14 PDF pages); accessed 2026-09-23; HTTP 200; local `../sources/S1-30/paper.pdf`; SHA-256 `de0db995e00cd696bb45f8c11cbeff944197b8f518198e38155644b68c697439`.
- **Platform / population / year / method.** iOS and Android phones; > 500,000 devices; client app samples battery level with the names of running processes. Mobile, not desktop.
- **Passages.**
  - PDF p. 1 (abstract): "during a deployment to a community of more than 500,000 devices" [abstract wording around this phrase not quoted in full].
  - PDF p. 3 (§2.3): "A sample is a measurement taken at a particular point in time that consists of the battery level (%) and a list of features: device model, OS version, names of running processes, battery state (e.g., unplugged), etc."
  - PDF p. 4: "We conservatively say that an app was running during the period [t1, t2] if it was seen in either sample."
- **Coverage.**
  - T12 (partial, mobile): describes a very large sampled record of running-process names per device; this paper publishes no co-occurrence statistics, and availability/licence of the data is not stated in the passages read.
  - T1 (mobile analogue, dataset only). Others: does not cover.
- **One observation?** One deployment (> 500,000 devices, 2012–13); no desktop.

### S1-31 — Kumar & Tomkins 2010 (WWW, Yahoo! toolbar browsing)

- **Citation.** R. Kumar, A. Tomkins. "A Characterization of Online Browsing Behavior." Proc. WWW 2010, Raleigh, pp. 561–570. DOI 10.1145/1772690.1772748.
- **Copy read.** https://www.ra.ethz.ch/cdstore/www2010/www/p561.pdf — conference CD-store copy (10 PDF pages); accessed 2026-09-23; HTTP 200; local `../sources/S1-31/paper.pdf`; SHA-256 `30d4c43ce8efe0bd85bbbd570b12fbdc28ce78ae979aa1ce39cf5386c4307df9`.
- **Platform / population / year / method.** Random sample of consenting Yahoo! toolbar users; pageview logs 18–24 March 2009 (+25 March); OS/browser not stated; sessions split at 30-min gaps.
- **Passages.**
  - PDF p. 2 (§3): "We consider a random sample of users drawn from Yahoo! toolbar logs over a one week period from March 18, 2009 to March 24, 2009."
  - PDF p. 3 (§4.1): "A sequence of pageviews for a particular user is broken into subsequences called sessions between any two consecutive pageviews whose timestamps are more than thirty minutes apart."
  - PDF p. 3: "For users, the median number of pageviews per day is 59, and the median time online is about an hour. … 1% of users spend more than 9 hours per day online, and view over 927 pageviews averaged over our sample. Likewise, 10% of users spend only three minutes per day and view fewer than 5 pages. Individual sessions tend to be significantly smaller. The median length is 17 pageviews taking 16 minutes of time."
  - PDF p. 3: "The median pageview has a gap of only 12 seconds, and fewer than 10% of pageviews have a gap that stretches to more than 90 seconds. On the lower end of the distribution, around one in six pageviews have less than a second inter-arrival time. Some key factors contributing to short inter-arrival times are rapid use of the back button, but more importantly, multi-window and" [tabbed browsing — continuation not quoted].
- **Coverage.**
  - T9 covers: object = page loads (pageviews); statistic = median 59 pageviews/day/user, median session 17 pageviews in 16 min, median inter-pageview gap 12 s (< 10% > 90 s); population = Yahoo! toolbar sample, March 2009.
  - T4 (partial): session lengths of browsing; multi-window/tab effects noted qualitatively.
  - T2 (partial): browsing session length (median 16 min).
  - Others: does not cover.
- **One observation?** Yes — one sample, one week in March 2009; machines/OS not named.

### S1-32 — Falaki, Mahajan, Kandula, Lymberopoulos, Govindan & Estrin 2010 (MobiSys, smartphone usage)

- **Citation.** H. Falaki, R. Mahajan, S. Kandula, D. Lymberopoulos, R. Govindan, D. Estrin. "Diversity in Smartphone Usage." Proc. MobiSys 2010, San Francisco. DOI 10.1145/1814433.1814453.
- **Copy read.** https://ratul.org/papers/mobisys2010-diversity.pdf — co-author-hosted (16 PDF pages); accessed 2026-09-23; HTTP 200; local `../sources/S1-32/paper.pdf`; SHA-256 `06c332e6d1113d6de66aea22a48db758e8d42660b04aed4198f280ad50e83023`.
- **Platform / population / year / method.** 33 Android + 222 Windows Mobile users, 7–28 weeks each; custom loggers of screen state and applications used. Mobile.
- **Passages.**
  - PDF p. 1 (abstract): "Using detailed traces from 255 users, we conduct a comprehensive study of smartphone use." … "the average number of interactions per day varies from 10 to 200, and the average amount of data received per day varies from 1 to 1000 MB."
  - PDF p. 2 Table 1: "Dataset1 33 7-21 weeks/user Android 16 high school students, 17 knowledge workers Screen state, applications used, network traffic, battery state"; "Dataset2 222 8-28 weeks/user Windows Mobile … Screen state, applications used" (cells flattened in extraction).
- **Coverage.**
  - T2/T10 (mobile analogue only): interaction sessions per day 10–200 per user (average); not desktop application launches.
  - Others: does not cover.
- **One observation?** Two datasets (Android 33 users; Windows Mobile 222 users); not desktop.

### S1-33 — Dubroy 2009, blog post on the same tabbed-browsing study as S1-04 (grey literature, author's own write-up)

- **Citation.** P. Dubroy. "How many tabs do people use? (Now with real data!)" Blog post, dubroy.com, April 13, 2009. (Not peer-reviewed; the author's preliminary write-up of the study published as S1-04. Used here only for what S1-04 does not state: the collection period.)
- **Copy read.** https://dubroy.com/blog/how-many-tabs-do-people-use-now-with-real-data/ (HTML); accessed 2026-09-23; HTTP 200; local `../sources/S1-33/page.html`; SHA-256 `492afbdcd779a148fe04cf1c03fa72ef4b4e6d33e6b8433abe8f47b43617b185`.
- **Passages.**
  - Header: "April 13, 2009".
  - "For the past few months, I've been knee-deep in data from the tabbed browsing study that I conducted late last year."
  - "We also put posters up with similar wording across the University of Toronto campus. 21 people completed the study, and 1 person started it but dropped out early."
  - "At a typical screen size on a laptop or desktop, the tab bar can fit about 9-13 tabs without scrolling."
- **Coverage.**
  - T4: same values as S1-04; adds that data were collected in late 2008 (a post dated 2009-04-13 refers to a study "conducted late last year").
  - Others: does not cover.
- **One observation?** Same observation as S1-04 (not independent).


## 3. Coverage matrix (S1 topics only)

"obs" means a logged or observed value with a named population. "def" means a definition, benchmark or lab setting. "data" means a dataset that holds the object but no published statistic. "—" means the candidate does not cover the topic.

| id | T1 | T2 | T3 | T4 | T6 | T7 | T9 | T10 | T11 | T12 |
|---|---|---|---|---|---|---|---|---|---|---|
| S1-01 | obs (windows open/visible) | obs | — | — | — | — | (email visibility) | — | — | — |
| S1-02 | — | obs (observer) | obs (bigrams) | — | — | (qual.) | — | — | — | — |
| S1-03 | — | obs | — | (surf switches) | — | — | — | — | — | — |
| S1-04 / S1-33 | — | (fig. only) | — | obs | — | — | — | — | — | — |
| S1-05 | obs (apps/day, top-10) | obs | obs (n-grams) | — | — | (qual.) | — | — | — | — |
| S1-06 | — | obs (observer) | — | — | — | — | (email time) | — | — | — |
| S1-07 | — | (page stay) | — | obs | — | — | obs (page stay) | — | — | — |
| S1-08 | — | — | — | obs | — | — | (pv/tab) | — | — | — |
| S1-09 | — | — | — | obs (Windows) + def | — | — | — | — | — | — |
| S1-10 | — | — | — | — | — | — | def | — | — | data (described) |
| S1-11 | — | — | — | — | — | — | — | obs (bench, Linux) | — | — |
| S1-12 | — | — | (qual.) | — | — | obs (builds/day) | obs (builds/day) | — | — | — |
| S1-13 | — | obs | — | — | — | — | — | — | (comm. SW share) | — |
| S1-14 | (apps used) | obs | — | — | — | — | — | — | — | — |
| S1-15 | — | — | — | — | — | — | — | def (Linux) | — | — |
| S1-16 | — | data | def | — | — | — | — | — | — | data (lab) |
| S1-17 | data | data | — | — | — | — | — | — | — | data (incl. Linux) |
| S1-18 | data | — | — | — | — | — | — | — | — | data |
| S1-19 | data (pseudonymous) | — | — | — | — | — | — | — | — | data |
| S1-20 | — | — | — | — | — | — | — | (telemetry described) | — | (not public) |
| S1-21 | — | (email checks) | — | — | — | — | obs (checks/day) | — | — | — |
| S1-22 | — | — | — | — | — | — | — | — | (Linux client type) | — |
| S1-23 | — | — | — | — | — | (CI, off-pop.) | — | — | — | — |
| S1-24 | (suspended windows) | obs (session length) | — | — | — | — | (alerts/h) | — | — | — |
| S1-25 | (call + email/files) | — | — | — | — | — | (sends in calls) | — | obs | — |
| S1-26 | — | — | — | — | (Windows, qual.) | — | — | — | — | (not public) |
| S1-27 | — | — | def | — | — | — | def | def (Windows) | def | — |
| S1-28 | — | — | — | — | — | (enterprise) | — | — | — | — |
| S1-29 | — | — | — | — | — | (cloud bench) | — | — | — | — |
| S1-30 | (mobile) | — | — | — | — | — | — | — | — | data (mobile) |
| S1-31 | — | (session) | — | (session) | — | — | obs | — | — | — |
| S1-32 | — | (mobile) | — | — | — | — | — | (mobile) | — | — |

Populations that are not independent of each other: S1-13 and S1-21 are the same 40 participants. S1-04 and S1-33 describe the same 21 participants. S1-01 and S1-03 share Microsoft Research co-authors but describe different studies.

## 4. Not found

The Not-found sections below are grouped by topic. Each one says what the literature does not provide, and the search-log rows give the searches that established it.

- **T1: which applications and processes run at the same time.** No peer-reviewed or preprint study was found that publishes the sets of concurrently running processes or applications per activity on a real desktop. In particular, no such study was found for Linux, or for gaming, media playback or video calls. The literature gives only these:
  - numbers of open or visible windows (S1-01, Windows XP);
  - distinct applications per day and over the study (S1-05, S1-14, Windows);
  - suspended task windows (S1-24);
  - datasets from which co-occurrence could be derived but was not published: S1-17 (includes 4 Linux users), S1-18 and S1-19 (process names de-identified).

  Blake et al. (ISCA 2010) was unreachable. It measures thread-level parallelism of desktop applications on Windows 7 and OS X and may list concurrent threads and processes (rows 17, 26–29). Flautner et al. (ASPLOS 2000) was also unreachable (rows 24, 27). Searches: rows 25, 31, 32, 43, 56.
- **T2: focus and switching on Linux.** Coverage exists for Windows (S1-01, S1-03, S1-05, S1-13, S1-14, S1-24) and from human observers (S1-02, S1-06). No study with Linux window-focus logs was found, apart from the BEHACOM dataset (S1-17), which publishes no statistics. No published dwell-time distribution beyond means, medians and quantiles was found. Searches: rows 31, 32, 43, 56.
- **T3: activity order.** No observation of real users was found for the order of photo editing → video editing → export, or search → write → build → send mail across a session. The only observed orders are:
  - activity bigrams for developers (S1-02, observer-coded; S1-05, logged);
  - a benchmark-defined order (S1-27, PCMark 10), for which no real-user support is claimed;
  - SWELL-KW prescribed lab tasks (S1-16).

  Searches: rows 47, 48, plus the developer-study rows 3 and 6.
- **T4: browser tabs and processes.**
  - No logged tab or window counts published after 2010 were located. Chang et al. (CHI 2021) is interviews plus a survey and was unreachable (rows 10–12). Crichton et al. (TWEB 2021) was unreachable (row 45).
  - No literature measurement of Chromium renderer-process counts on Linux was found. S1-09 is Windows only.
  - No per-minute tab-switch rate was found. Page-view pacing exists (S1-07, S1-31).

  Searches: rows 9–13, 42, 57.
- **T6: unrequested background jobs on stock Linux desktops.** No peer-reviewed or preprint source was found on any of the following, for any distribution:
  - default-enabled timers or services;
  - antivirus, indexer, `updatedb`, package-backup or update-check schedules, durations or process names;
  - DKMS object counts or autoinstall durations.

  S1-26 covers only Windows update state, qualitatively. Searches: rows 36, 37, 52.
- **T7: size of user-started jobs.** None of the following was found:
  - build sizes (objects per build) or build times of software projects on developer desktops;
  - the relation of a typical project build to a Linux kernel build;
  - desktop video render or transcode lengths;
  - desktop backup first-versus-incremental sizes or durations;
  - archive-creation sizes;
  - ML training jobs on desktop CPUs.

  What exists: IDE builds per developer day and build-wait share (S1-12, Visual Studio/Windows, 2015); CI build durations for a sample biased toward long builds (S1-23); the enterprise weekly-full/daily-incremental paradigm (S1-28); cloud benchmark clip length (S1-29). The end-user backup survey was unreachable (row 38). Searches: rows 16, 33, 38, 49–51.
- **T9: operations within applications.** Not found:
  - frequency of image-filter application by real users (ingimp, S1-10, describes the log but publishes no rates);
  - video-editor preview renders per minute;
  - email send frequency with or without attachment for desktop users (S1-21 has email checks per day; S1-25 has the share of meetings with an email send);
  - whether heavy operations happen while the user interacts or is idle.

  Page loads per day and per session exist (S1-07, S1-31). Searches: rows 14, 35.
- **T10: application launches.** Not found:
  - application launch counts per desktop session or day. S1-20 describes Windows telemetry that counts launches but publishes no values. S1-32 is mobile only. Esfahbod's 2006 preload thesis, which may contain Linux launch logs, has no open copy (row 40).
  - CPU time of launch on Linux, separately from wall time.

  Launch wall time on Linux exists from a single benchmark machine (S1-11: mean cold start 2.4 s on Fedora 12, 2011; S1-15 defines launch timing on Linux 5.4 but its absolute values are only in figures), and there are Windows benchmark "typical ranges" (S1-27). Searches: rows 15, 25, 40.
- **T11: video calls and media.** Not found:
  - process structure (process names or counts) of Zoom, Teams or browser-based calls on Linux (S1-22 only establishes that Zoom had a native Linux client in 2021 and that Webex/Meet ran as web clients);
  - any logged observation of music or video playback concurrent with other work.

  S1-25 gives email and file multitasking during Teams meetings (Microsoft employees, 2020). Searches: rows 34, 39.
- **T12: public traces.** Found: S1-16, S1-17, S1-18 and S1-19, plus the described but not-public S1-10, S1-20, S1-26 and S1-30. Not found: a public trace of Linux desktop process creation with real process names from real users. BEHACOM (S1-17) records the foreground executable name and the count of active applications per minute for 4 Linux users, but not process creation events. Licences of the S1-17, S1-18 and S1-19 datasets are not stated in the passages read. Searches: rows 20–23, 45, 53.

## 5. Unreachable or paywalled sources

| Source | Attempts (status) |
|---|---|
| Blake, Dreslinski, Mudge, Flautner, "Evolution of Thread-Level Parallelism in Desktop Applications," ISCA 2010, DOI 10.1145/1816038.1816000 | ACM PDF 403; ResearchGate 403; cse.wustl.edu course mirror 000 (TLS: unable to get local issuer certificate); guessed tnm.engin.umich.edu URL 403 |
| Flautner, Uhlig, Reinhardt, Mudge, "Thread-level Parallelism and Interactive Performance of Desktop Applications," ASPLOS 2000, DOI 10.1145/378993.379233 (and 1999 tech-report version) | ACM PDF 403; web.eecs.umich.edu/~manowar mirror 000 (same TLS error) |
| Chang et al., "When the Tab Comes Due," CHI 2021, DOI 10.1145/3411764.3445585 (CC-BY per Semantic Scholar) | ACM PDF 403; ACM fullHtml 403; joe.cat project page proxy 502 |
| Crichton, Christin, Cranor, "How Do Home Computer Users Browse the Web?," TWEB 2021, DOI 10.1145/3473343 | ACM PDF 403 |
| Smith, Oliver, Surendran, Thakkar, "SWISH," IUI 2006, DOI 10.1145/1111449.1111492 | author PDF 404; ACM PDF 403 |
| "Towards understanding short-term personal information preservation: a study of backup strategies of end users" (319-respondent survey) | academia.edu 403 |
| Kent, "Cybersecurity Data Sources for Dynamic Network Research," Imperial College Press 2015 (chapter describing S1-19) | not openly available; dataset page used instead |
| Esfahbod, "Preload — An Adaptive Prefetching Daemon," MSc thesis, U. Toronto 2006 | only a Google Books record found; no open copy |
