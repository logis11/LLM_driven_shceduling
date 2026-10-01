# S1 — peer-reviewed and preprint literature

Task 9.10 scenarios and timelines, stage 2 search. Reader class S1; topics T1, T2, T3, T4, T6, T7, T9, T10 as defined in `input.md`. All searches, downloads and readings on 2026-10-01.

**Conventions.**

- Copies are under `sources/S1-NN/` (gitignored), fetched with `curl -L`; each file's SHA-256 is from `shasum -a 256`. PDF text was extracted with pypdf 6.18.0 into a sibling `.txt` working file with page markers; that file is not a source.
- Verbatim passages are copied from the copy's text layer (HTML and XML with tags stripped). Line breaks are joined and whitespace is not significant. End-of-line hyphenation and stray or missing spaces of the text layer are either kept as extracted or joined; nothing else is changed. Ligatures (ﬁ, ﬂ, ﬃ) may be written fi, fl, ffi and curly quotation marks as straight ones. "…" marks an omission; " / " inside a quoted table or figure marks a line or row break; square brackets inside a quote are the reader's notes (page breaks, translations, figure transcriptions).
- "[transcribed from figure]" marks text read from an image inside a PDF rather than its text layer; the image file and its SHA-256 are listed in the entry.
- Locators: "p. N" or "PDF p. N" is the page of the copy as a file; printed page numbers are added where the copy shows them.
- A number the reader computed or read off a chart is labelled the reader's own; it locates a candidate and is not a value.
- Every quoted passage taken from a text layer was checked by script against the extraction of the local copy, compared on letters and digits only; transcriptions from figure images cannot be checked that way.
- Candidate ids are provisional; S1-23 to S1-29, S1-52 to S1-54 and S1-69 to S1-79 are unused.

## 1. Search log

| date | engine or venue | query terms | hits followed | dead ends (HTTP status) |
|---|---|---|---|---|
| 2026-10-01 | WebSearch | Meyer Fritz Murphy Zimmermann "The Work Life of Developers: Activities, Switches and Perceived Productivity" pdf | thomas-zimmermann.com/publications/files/meyer-tse-2018.pdf (200) → S1-01 | — |
| 2026-10-01 | WebSearch | SWELL Knowledge Work dataset stress user modeling Koldijk computer interaction application logs | cs.ru.nl/~skoldijk/SWELL-KW/Dataset.html (200), uLogData.html (200), FeatureData.html (200), cs.ru.nl/~skoldijk/Papers/ICMI 2014 paper_final_cr.pdf (200) → S1-10 | persistent-identifier.nl resolver (308 → 200, JavaScript-only page, no record shown) |
| 2026-10-01 | DANS SSH Data Station API | search?q=SWELL knowledge work; datasets/:persistentId doi:10.17026/DANS-X55-69ZP | dataset JSON (200) → S1-10 | — |
| 2026-10-01 | WebSearch | BEHACOM dataset modelling users' behaviour in computers application usage keyboard mouse | ncbi PMC7270191/pdf/ (200 but an HTML proof-of-work page, no PDF); Europe PMC REST PMC7270191/fullTextXML (200) → S1-02; Mendeley public-api datasets/cg4br62535 (200) → S1-02 | europepmc.org/api/fulltextRepo?…main.pdf (403); Mendeley public-api …/versions/2 (404) |
| 2026-10-01 | WebSearch | Mark Iqbal Czerwinski Johns "Bored Mondays and focused afternoons" pdf | gwern.net/doc/psychology/writing/2014-mark.pdf (200) → S1-05 | — |
| 2026-10-01 | WebSearch | Mark Iqbal Czerwinski Johns Sano "Neurotics can't focus" … window duration | ics.uci.edu/~gmark/…/CHI 16 Multitasking and Focus.pdf (200) → S1-04; arxiv.org/pdf/2101.11865 (200) → S1-15 | — |
| 2026-10-01 | WebSearch | Iqbal Horvitz "Disruption and recovery of computing tasks" CHI 2007 pdf | erichorvitz.com/CHI_2007_Iqbal_Horvitz.pdf (200) → S1-03; interruptions.net Czerwinski-CHI04-p175 (200) → S1-14 | — |
| 2026-10-01 | WebSearch | Hutchings Smith Meyers Czerwinski Robertson "Display space usage and window management operation comparisons…" pdf | facstaff.elon.edu hutchings2004exploring.pdf (200; position paper summarising the study — discarded, primary paper preferred); uist.acm.org 2005 p2-hutchings.pdf (200; TaskZones poster — discarded); MSR publication page via WebFetch → microsoft.com/…/2016/02/avi2004-displayspace.pdf (200) → S1-06 | — |
| 2026-10-01 | WebSearch | Gonzalez Mark "Constant, constant, multi-tasking craziness" pdf | ics.uci.edu/~gmark/CHI2004.pdf (200) → S1-07 | — |
| 2026-10-01 | WebSearch | Tak Cockburn "Characterising switching behaviour" window switching logging study frequency | dl.ifip.org/IFIP-LNCS-6946/hal-01590560 | dl.ifip.org (connection failed after 75 s, HTTP 000); core.ac.uk/display/35463015 (403) |
| 2026-10-01 | WebSearch | Smith Baudisch Robertson Czerwinski "GroupBar: The TaskBar Evolved" number of windows open logging | microsoft.com/…/2003/01/ozchi2003-groupbar.pdf (200) → S1-08 | — |
| 2026-10-01 | WebSearch | DesktopBench FOCAL dataset desktop screen activity application focus logs | arxiv.org/pdf/2604.19541 (200) → S1-09 | export.arxiv.org API ("Rate exceeded." body) |
| 2026-10-01 | WebSearch | Yeykelis Cummings Reeves 2014 multitasking on a single device switching … 19 seconds; "Yeykelis" "Multitasking on a single device" filetype:pdf | no full text | OpenAlex oa_url none; Semantic Scholar openAccessPdf status CLOSED; Unpaywall is_oa false (Journal of Communication 64(1), doi 10.1111/jcom.12070) |
| 2026-10-01 | WebSearch + OpenAlex | Screenomics laptop switching median seconds Reeves Ram Robinson | Wayback 20250426205340 of pmc.ncbi.nlm.nih.gov/articles/PMC8045984/ (200) → S1-11 | Europe PMC REST PMC8045984/fullTextXML (500, twice); europepmc.org/articles/PMC8045984?pdf=render (403); europepmc.org/backend/ptpmcrender.fcgi (403) |
| 2026-10-01 | WebSearch | Mozilla Test Pilot study window tab usage Firefox users results paper | blog.mozilla.org metrics posts (not followed: Mozilla blog posts are not literature; Test Pilot tab results are S3 material) | — |
| 2026-10-01 | WebSearch + OpenAlex | Judd Kennedy "Measurement and evidence of computer-based task switching and multitasking by Net Generation students" | AJET 2015 Judd article download 1992/1264 (200) → S1-18 | Judd & Kennedy 2011 (Computers & Education 56(3), doi 10.1016/j.compedu.2010.10.004): OpenAlex no OA, Semantic Scholar CLOSED |
| 2026-10-01 | WebSearch | Mark Gonzalez Harris "No task left behind? Examining the nature of fragmented work" CHI 2005 pdf | interruptions.net/literature/Mark-CHI05-p321-mark.pdf (200) → S1-12 | — |
| 2026-10-01 | WebSearch + OpenAlex | Tak Cockburn "Improving window switching interfaces" INTERACT 2009 … | OpenAlex → publications.tno.nl/…/tak-2011-understanding.pdf (200) → S1-13 | — |
| 2026-10-01 | WebSearch (extended) | large-scale telemetry study desktop application usage Windows PCs foreground application switching number of applications running concurrently | arxiv.org/pdf/1809.03920 (200; PC data "out of scope" — discarded); arxiv.org/pdf/1803.09152 (200; PC usage hours per month only — discarded) | — |
| 2026-10-01 | WebSearch | field study background processes running on personal computers logging number of processes concurrent applications user study energy | Springer s12053-012-9167-5 PDF (200 but a JavaScript client-challenge page); Wayback 20220127105849 of the PDF (200) → S1-21 | WebFetch link.springer.com (303 to login) |
| 2026-10-01 | ics.uci.edu/~gmark Publications.html | (page listing) | CHI 16 Email Duration.pdf (200) → S1-04 (same observation); CHI 2012.pdf (200) → S1-17; CSCW 2015 Focused.pdf (200) → S1-05 (same observation); CHI 2018 Workplace Distractions.pdf (200; self-report on blocking, no logged switching — discarded) | — |
| 2026-10-01 | WebSearch | Etsion Tsafrir Feitelson desktop scheduling "how can we know what the user wants" Linux X server | bibliographic hits only (scheduler design; not followed) | — |
| 2026-10-01 | WebSearch | Meyer Bachelli Fritz "Detecting developers' task switches and types" TSE logged application switches per hour | pointer to FSE 2014 observation → thomas-zimmermann.com/publications/files/meyer-fse-2014.pdf (200) → S1-20 | — |
| 2026-10-01 | WebSearch | Linux desktop user activity logging study window focus switching field study GNOME X11 participants | pepite-depot.univ-lille.fr …/50376-2010-Xu.pdf (200) → S1-16; edge.launchpad.net/activityfinder (WebFetch 404) | — |
| 2026-10-01 | WebSearch | Dodier-Lazaro Linux users field study application usage multitasking Zeitgeist activity sandboxing thesis UCL; "Dodier-Lazaro" "sandbox" … | discovery.ucl.ac.uk/id/eprint/10046583/1/Dodier-Lazaro_Thesis.pdf (200) → S1-19; Wayback 20260214072721 of the eprint record (200, metadata); Wayback 20251121044828 of RN/17/03 (200; interview study, not a candidate) | discovery.ucl.ac.uk/id/eprint/10046583/ (403); discovery-pp.ucl.ac.uk/id/eprint/1540944 (403) |
| 2026-10-01 | WebSearch | Intel telemetry PC usage study foreground application "DCA" client analytics | Intel IT white papers (vendor documents; not followed) | — |
| 2026-10-01 | WebSearch | RescueTime data study knowledge workers time in applications switching per day large-scale analysis paper CHI | only vendor blog and aggregator pages (not literature; not followed) | — |
| 2026-10-01 | WebSearch | ActivityWatch dataset study window focus logs participants computer usage paper | sites.google.com/umd.edu/wta (WebFetch: participant instructions, no results); cdn.nafath.mada.org.qa …/293_Too-Many-Tabs-Open….pdf (200; data simulated by the research team on Macs — discarded) | — |
| 2026-10-01 | OpenAlex | Task selection, task switching … independent study; Judd making sense of multitasking; Benbunan-Fich measuring multitasking activity-based metrics | AJET 1992 (200) → S1-18 | Benbunan-Fich et al. TOCHI 2011: no OA location |
| 2026-10-01 | WebSearch + OpenAlex | Chetty Brush Meyers Johns "It's not easy being green: understanding home computer power management" CHI 2009 | no full text | microsoft.com …/chi09-chetty.pdf (404), …/CHI2009_GreenComputing.pdf (404); MSR wp-json search (no PDF); OpenAlex (not matched) |
| 2026-10-01 | WebSearch | public dataset desktop computer usage logs application name window title timestamps … | arxiv.org/pdf/2602.09310 (200; A11y-CUA, 60 instructed tasks in a controlled Windows environment — discarded); ResearchGate PIM desktop dataset PDF (403); service.tib.eu desktop-activity-log (anti-bot challenge page) | as listed |
| 2026-10-01 | arXiv | Jeuris Tell Houben Bardram "The Hidden Cost of Window Management" | arxiv.org/pdf/1810.04673 (200; controlled study with instructed switches — discarded) | — |
| 2026-10-01 | WebSearch | Siddha Pallipadi van de Ven "Getting maximum mileage out of tickless" OLS 2007 idle desktop wakeups | kernel.org/doc/ols/2007/ols2007v2-pages-201-208.pdf (200; idle timer counts only — discarded in favour of its reference [9]); kernel.org/doc/ols/2006/ index → ols2006v1-pages-441-450.pdf (200) → S1-22 | — |
| 2026-10-01 | WebSearch + Crossref | Proksch Amann Nadi "Enriched event streams" MSR 2018 KaVE pdf | no full text | proks.ch/papers/… (404); zora.uzh.ch/id/eprint/150563 (200, no PDF link); dl.acm.org/doi/pdf/10.1145/3196398.3196400 (403) |
| 2026-10-01 | WebSearch + HAL API | Chapuis "Gestion des fenêtres : enregistrement et visualisation de l'interaction" IHM 2005 | HAL API record (200; abstract: a logging/replay tool paper for X Window, "some examples", no population statistics) | hal.science/hal-00534168/document (200 but anti-bot challenge page) |
| 2026-10-01 | WebSearch | energy consumption Linux desktop environments GNOME KDE Xfce idle background processes empirical study paper | Phoronix articles only (not literature; not followed) | — |
| 2026-10-01 | WebSearch | "Linux" users logged "window switches" OR "application switches" field study per hour developers X11 logging tool | tool repositories (wmtrace, activity-logger, window-tracker-x11); no population study | — |
| 2026-10-01 | OpenAlex | Bi & Balakrishnan 2009 large high-resolution display daily work; Ringel 2003 virtual desktop usage strategies | no OA location for either | — |
| 2026-10-01 | WebSearch | Dubroy Balakrishnan "A study of tabbed browsing among Mozilla Firefox users" pdf | dgp.toronto.edu/public_user/ravin/papers/chi2010_tabbedbrowsing.pdf (200) → S1-30; jeffhuang.com/papers/ParallelBrowsing_HT10.pdf (200) → S1-32; arxiv.org/pdf/1307.1542 (200) → S1-34 | dubroy.com blog posts not followed (author blog on Test Pilot data — S3 material) |
| 2026-10-01 | WebSearch | Reis Moshchuk Oskov "Site Isolation: Process Separation for Web Sites within the Browser" USENIX Security 2019 pdf | usenix.org/system/files/sec19-reis.pdf (200) → S1-31 | — |
| 2026-10-01 | WebSearch | Weinreich Obendorf Herder Mayer "Not quite the average: An empirical study of Web use" pdf | vsis-www.informatik.uni-hamburg.de/publications/view.php/315 (200) → getDoc.php/publications/315/Weinreich-2008_-_Empirical_Study_of_Web_Use.pdf (200) → S1-33 | dl.acm.org/doi/pdf/10.1145/1326561.1326566 (403, Cloudflare "Just a moment"); OpenAlex works/doi:10.1145/1326561.1326566: oa_status closed |
| 2026-10-01 | WebSearch | Chang Hahn Kittur "When the Tab Comes Due: Challenges in the Cost Structure of Browser Tab Usage" CHI 2021 pdf | CMU news pages only (not sources) | dl.acm.org/doi/pdf/10.1145/3411764.3445585 (403); web.archive.org/web/2026id_/… (302 → 20251017134102 capture, 403); Semantic Scholar openAccessPdf points to the same ACM URL; josephcc.github.io (301 → joe.cat, connection failed, curl 000); kittur.org (200, no link to the paper); cs.cmu.edu/~jcchang/ (404); export.arxiv.org API (http: empty; https: 429) |
| 2026-10-01 | WebSearch | "When the Tab Comes Due" Chang Hahn Kim Coupland Breneman Kim Hearst Kittur pdf josephcc OR kittur.org | none relevant | — |
| 2026-10-01 | Wayback CDX API | url=dl.acm.org/doi/pdf/10.1145/3411764.3445585 | capture 20250526065900 (application/pdf, 200) → S1-36 | captures 20230309202413, 20251017134102 (403) |
| 2026-10-01 | WebSearch | arxiv browser tab usage logging study number of open tabs users | arxiv.org/pdf/1402.5255 (200) → merged into S1-34 (same DOBBS observation) | — |
| 2026-10-01 | WebSearch | Labaj Bieliková "Tabbed browsing behavior as a source for user modeling" UMAP 2013 pdf | none (UMAP 2013, LNCS, pp. 388–391, DOI 10.1007/978-3-642-38844-6_46) | no open copy located; not fetched |
| 2026-10-01 | WebSearch | Skeema "browser tabs" Chang Kittur CHI 2023 arxiv; Tabs.do task-centric browser tab management UIST 2021 field deployment number of tabs | par.nsf.gov/servlets/purl/10358962 (200, Tabs.do UIST 2021) read in full: field-deployment log counts Tabs.do interactions (sessions, saved tabs, reopened tabs), not open tabs; not a candidate, copy deleted | — |
| 2026-10-01 | OpenAlex search | "When the Tab Comes Due" | 10.1145/3544548.3580690 (Ma et al. CHI 2023): research.aalto.fi/files/107553048/SCI_Ma_etal_CHI_2023.pdf (403) → web.archive.org/web/2026id_/… (200) → S1-35; Fuse UIST 2022 (arXiv 2208.14861) not followed (title indicates a sensemaking tool, not a usage study) | research.aalto.fi file (403) |
| 2026-10-01 | NSF PAR, scholar.archive.org | "When the Tab Comes Due" | — | par.nsf.gov search (200, no match); scholar.archive.org (302 → /verify bot check) |
| 2026-10-01 | WebSearch | measurement study number of renderer processes Chrome tabs site isolation memory overhead paper Linux | arxiv.org/pdf/1702.06764 (200) → S1-38 | remaining hits blogs / Chromium source (S2/S3 material) |
| 2026-10-01 | WebSearch | Reis Gribble "Isolating Web Programs in Modern Browser Architectures" EuroSys 2009 pdf | research.google pub page (200, no PDF link); charlesreis.com/research/publications/eurosys-2009.pdf (200) → S1-37 | cs.washington.edu/research/projects/security/papers/eurosys09.pdf (404); homes.cs.washington.edu/~gribble/papers/eurosys09.pdf (404) |
| 2026-10-01 | WebSearch | "open tabs" distribution telemetry Firefox OR Chrome OR Edge study paper median tabs per user desktop large-scale | only DOBBS, Dubroy (already held) and forum/blog posts | — |
| 2026-10-01 | WebSearch (extended) | "tab" browsing logging study 2015..2025 participants "number of open tabs" log extension Chrome field study CHI OR CSCW OR WWW | arxiv.org/pdf/2608.09107 (200, ITO, UIST 2026): 12-participant comparative evaluation of a tab tool, no field counts of open tabs — not a candidate; github.com/mjuarezm/tablogger not followed | — |
| 2026-10-01 | WebSearch | Juarez Afroz Acar Diaz Greenstadt "A Critical Evaluation of Website Fingerprinting Attacks" tab usage study | nymity.ch/tor-dns/pdf/Juarez2014a.pdf (200) read: cites tab studies; its own browsing data come from the ALAD dataset (80 users in a simulated work environment); no tab counts — not a candidate | — |
| 2026-10-01 | WebSearch | "tabs" "windows" browser telemetry large scale analysis paper "Chrome" users "number of tabs" percentile 2019 OR 2020 OR 2022 OR 2023 OR 2024 | Ruth et al., "A World Wide View of Browsing the World Wide Web", IMC 2022: zakird.com/papers/browsing.pdf (200) read — monthly per-domain aggregates of page loads and time on page for Windows and Android Chrome; no per-user rates, no tab counts — not a candidate, copy deleted | ndownloader.figshare.com/files/43248699 (202, empty body); zakird.com/papers/ (404) |
| 2026-10-01 | WebSearch | arxiv Chromium "renderer processes" tabs memory measurement Linux experiment number of processes per tab "site-per-process" | arxiv.org/pdf/2111.02325 (200) → S1-48 | other hits Chromium docs / blogs |
| 2026-10-01 | WebSearch | Kooti Aiello Grbovic Lerman Mantrach "Evolution of Conversations in the Age of Email Overload" WWW 2015 arxiv | arxiv.org/pdf/1504.00704 (200) → S1-39 | — |
| 2026-10-01 | WebSearch | Fisher Brush Gleave Smith "Revisiting Whittaker & Sidner's email overload ten years later" CSCW 2006 pdf | microsoft.com/en-us/research/?p=152080 (200) → wp-content/uploads/2006/11/p309-fisher.pdf (200) → S1-40 | — |
| 2026-10-01 | arXiv (direct) | Yang et al., How Work From Home Affects Collaboration (arXiv 2007.15584) | arxiv.org/pdf/2007.15584 (200) read: reports e-mail/IM/meeting *hours*, not counts of messages — not a candidate, copy deleted | — |
| 2026-10-01 | WebSearch | Kumar Tomkins "A characterization of online browsing behavior" WWW 2010 pdf pageviews per day | archives.iw3c2.org/www2010/proceedings/www/p561.pdf (200) → S1-41; arxiv.org/pdf/2108.06745 (200) → S1-42 | 5harad.com whowhatweb.pdf (Goel et al. ICWSM 2012) not followed |
| 2026-10-01 | WebSearch | Cockburn McKenzie "What do web users do? An empirical analysis of web use" International Journal of Human-Computer Studies 2001 pdf | hdl.handle.net/10092/514 | ir.canterbury.ac.nz/handle/10092/514 (403); Wayback CDX API (returned "Internet Archive: Temporarily Offline" page); core.ac.uk/works/4855248 (403); api.core.ac.uk/v3/works/4855248 (429) — not obtained |
| 2026-10-01 | WebSearch | "What do web users do" Cockburn McKenzie pdf cosc.canterbury.ac.nz OR ir.canterbury.ac.nz Netscape history four months | same repository handle only | as above |
| 2026-10-01 | WebSearch | Terry Kay Van Vugt Slack Park "ingimp" instrumentation GIMP usage data CHI 2008 pdf | mjskay.com/papers/chi_2008_ingimp.pdf (200) read: design of the instrumentation, "installed by over 700 users in the first six months", no usage rates — not a candidate, copy deleted | OpenAlex doi:10.1145/1357054.1357152 closed |
| 2026-10-01 | WebSearch | log analysis image editing application command usage frequency filters per session users Photoshop OR GIMP study | microsoft.com/en-us/research/?p=184827 (200; 2010 talk abstract by M. Terry, no paper) | graphicsinterface.org/?p=5024 (403, Cloudflare) |
| 2026-10-01 | WebSearch | "Characterizing large-scale use of a direct manipulation application in the wild" Lafreniere Bunt … Terry GI 2010 pdf | cs.uwaterloo.ca/research/tr/2009/CS-2009-27.pdf (200) → S1-43 | — |
| 2026-10-01 | WebSearch | video editing software usage log analysis users render preview frequency per session study Premiere OR Kdenlive OR "video editor" telemetry HCI paper | none (ExpressEdit, CutVerse: lab/agent studies; Kdenlive docs) | — |
| 2026-10-01 | WebSearch | measurement study Zoom Webex Google Meet client CPU usage Linux "Can you see me now" IMC 2021 Chang Varvello | arxiv.org/pdf/2109.13113 (200) → S1-44 | — |
| 2026-10-01 | WebSearch | MacMillan Mangla Saxon Feamster "Measuring the Performance and Network Utilization of Popular Video Conferencing Applications" IMC 2021 arxiv | arxiv.org/pdf/2105.13478 (200) → S1-45 | — |
| 2026-10-01 | WebSearch | video conferencing client CPU usage threads processes measurement Jitsi Meet browser WebRTC Linux desktop paper energy consumption Zoom Teams laptop | blogs and mailing lists only (wirelessmoves, LWN, openstack-discuss) — not S1 | — |
| 2026-10-01 | WebSearch | arxiv energy consumption video conferencing applications laptop RAPL Zoom Teams Meet Jitsi measurement Ubuntu | Greenspector and CableLabs blog posts — not S1 | — |
| 2026-10-01 | WebSearch | Isaacs Walendowski Whittaker Schiano Kamm "The character, functions, and styles of instant messaging in the workplace" CSCW 2002 pdf | interruptions.net/literature/Isaacs-CSCW02-p11-isaacs.pdf (200) → S1-51 | interruptions.net/literature/Isaacs-CSCW02.pdf (404) |
| 2026-10-01 | WebSearch | Avrahami Hudson "Communication characteristics of instant messaging" CSCW 2006 pdf messages per day logged | arxiv.org/pdf/0803.0939 (200) → S1-46; arxiv.org/pdf/1906.01756 (200) → S1-47 | CSCW 2006 paper itself: no open copy located (OpenAlex search, no match) |
| 2026-10-01 | WebSearch | Avrahami Fussell Hudson "IM waiting: timing and responsiveness in semi-synchronous communication" pdf | interruptions.net/literature/Avrahami-CSCW08.pdf (200) and Avrahami-CHI06-p731-avrahami.pdf (200) → S1-50 (one observation) | — |
| 2026-10-01 | WebSearch | logged email client study emails sent per day per user attachments percentage enterprise Outlook log analysis paper | industry statistics only (Radicati, vendor blogs) — not S1 | — |
| 2026-10-01 | WebSearch | Jackson Dawson Wilson "The cost of email interruption" OR "Reducing the effect of email interruptions on employees" | interruptions.net/literature/Jackson-IJIM03.pdf (200) → S1-49 | — |
| 2026-10-01 | WebSearch | server log study email traffic per user "messages sent per day" university OR enterprise characterization of email workload paper | server-side SMTP workload studies (TUC, ODU) — not followed: server traffic, not per-user desktop behaviour | — |
| 2026-10-01 | OpenAlex / Wayback | Grevet, Choi, Kumar, Gilbert, "Overload is overloaded: email in the age of Gmail", CHI 2014 (10.1145/2556288.2557013) | — | OpenAlex: closed; web.archive.org/web/{2020..2024}id_/dl.acm.org/doi/pdf/… (302 → cookieSet capture, empty body) — not obtained |
| 2026-10-01 | WebSearch | Flautner Uhlig Reinhardt Mudge thread-level parallelism and interactive performance of desktop applications ASPLOS 2000 pdf | tnm.engin.umich.edu `krisf.pdf` (200; turned out to be Flautner's 2001 dissertation) → S1-55 | — |
| 2026-10-01 | WebSearch | Blake Dreslinski Mudge Flautner Evolution of thread-level parallelism in desktop applications ISCA 2010 pdf | tnm.engin.umich.edu PDF (200) → S1-56 | — |
| 2026-10-01 | WebSearch | thread-level parallelism modern video games characterization CPU cores study paper 2020..2025 | none relevant (blogs, a SciTePress overview) | — |
| 2026-10-01 | WebSearch | Proton Wine game threads Linux characterization paper "Steam Deck" scheduling arXiv | none (blogs, Wikipedia) | — |
| 2026-10-01 | arXiv API (export.arxiv.org) | all:sched_ext; all:LAVD; abs:"Steam Deck"; abs:Proton AND abs:Wine; abs:"video game" AND scheduler AND Linux; abs:game AND "thread-level parallelism"; abs:gamescope; abs:"frame pacing" | none | http: 301 for all; https: 429 (sched_ext, LAVD, Steam Deck, video game…), 503 (Proton AND Wine) — rate-limited, not retried |
| 2026-10-01 | OpenAlex API | sched_ext LAVD scheduler gaming | 1 hit, irrelevant (provenance scheduler) | — |
| 2026-10-01 | OpenAlex API | Steam Deck Linux game scheduling latency | Gegout et al. AsHES 2025 (→ S1-64); anti-cheat arXiv 2609.17525 (not followed, security) | — |
| 2026-10-01 | OpenAlex API | Proton Wine Windows games Linux performance | "Is Proton Good Enough?" (Springer 2023, DOI 10.1007/978-3-031-41456-5_48) — closed, no OA copy listed | not retrieved (closed access) |
| 2026-10-01 | Semantic Scholar API | latency criticality aware virtual deadline scheduler gaming; video game thread level parallelism Linux; gamescope compositor | — | 429 ×3 |
| 2026-10-01 | OpenAlex API | thread level parallelism video games; game workload characterization Linux threads; latency-criticality aware virtual deadline scheduling; video game CPU scheduling Linux frame time; Wine compatibility layer performance games; gamescope Valve compositor (0 hits); Steam client download while playing; multithreaded game engine thread analysis profiling | none relevant | — |
| 2026-10-01 | WebSearch | LAVD scheduler Changwoo Min latency-criticality gaming Steam Deck paper pdf | LWN 1051430 (journalism, not a candidate; WebFetch of it yielded the LPC 2025 slide URL) → S1-62; SNU seminar abstract | — |
| 2026-10-01 | WebSearch | "Is Proton Good Enough" performance comparison gaming Windows Linux pdf | none (forum posts) | — |
| 2026-10-01 | WebSearch | SYSmark PCMark benchmark representativeness real user workloads paper analysis | press and vendor pages only (bit-tech, PCWorld, BAPCo whitepaper) — out of class (S2) | — |
| 2026-10-01 | WebSearch | PCMark 10 workloads scenarios study paper Essentials Productivity Digital Content Creation ieee | vendor/press only (UL support, AnandTech) — out of class | — |
| 2026-10-01 | WebSearch | IISWC game workload characterization threads CPU games thread-level parallelism measurement PC | Roca et al. IISWC 2006 "Workload characterization of 3D games" (GPU/OpenGL trace simulation; not followed — no process/thread population) | — |
| 2026-10-01 | WebSearch | Lin Bezemer Hassan studying urgent updates of popular games Steam platform empirical software engineering pdf | ASGAARD publications page (200) → EMSE 2017 PDF (200) → S1-66 | — |
| 2026-10-01 | WebSearch | Steam content delivery download traffic measurement study game updates size paper | Chambers et al. IMC 2005 (→ S1-65); APRICOT 2024 slides "Inside the Engine room" (IIJ, CDN-side; not followed: describes cache infrastructure, not client behaviour during play) | — |
| 2026-10-01 | WebSearch | Endo Wang Chen Seltzer "Using latency to evaluate interactive system performance" OSDI 1996 pdf | USENIX legacy text (200) → S1-60 | — |
| 2026-10-01 | WebSearch | "Inside the Engine Room" Steam content delivery platform infrastructure 100GB games PAM 2024 paper | APRICOT slides only | — |
| 2026-10-01 | WebSearch | Chambers Feng Sahu Saha "Measurement-based characterization of a collection of on-line games" IMC 2005 Steam | USENIX PDF (200; text extraction garbled by font encoding) and HTML nodes 2, 17, 18 (200) → S1-65 | — |
| 2026-10-01 | WebSearch | "SYSmark 2004" VirusScan background scenario Communication Office Productivity paper workload | AnandTech pages only — out of class (press) | — |
| 2026-10-01 | WebSearch | Bircher John "SYSmark 2007" power management multi-core workload description paper | utexas `BircherICS2008.pdf` (200) → S1-57 | — |
| 2026-10-01 | WebSearch | CpsMark+ benchmark 中国 计算机 性能 测试 CPSMark 场景 | none | — |
| 2026-10-01 | WebSearch | arXiv on-device AI PC benchmark survey "UL Procyon" "MLPerf Client" Geekbench AI comparison | vendor/press only | — |
| 2026-10-01 | WebSearch | "SYSmark 2004" workload characterization paper processor "Office Productivity" "Internet Content Creation" concurrent applications academic | pcstats.com press only | — |
| 2026-10-01 | WebSearch | Bircher dissertation "Predictive power management for multi-core processors" University of Texas 2010 pdf SYSmark | utexas `bircher_dissertation_20109.pdf` (200) → S1-57 | — |
| 2026-10-01 | WebSearch | "SYSmark" multitasking scenario "virus scan" background benchmark hyper-threading paper Intel Technology Journal | Principled Technologies reports commissioned by Intel (vendor-commissioned, out of class); no ITJ article | — |
| 2026-10-01 | WebSearch | "PCMark 10" OR "SYSmark 25" evaluation hybrid processor Alder Lake Thread Director paper | Saez & Prieto-Matias APSys 2022 (not followed — evaluates Thread Director scheduling, not benchmark definitions) | — |
| 2026-10-01 | OpenAlex API | "PCMark 10" (14 hits); "SYSmark" (92, all pages listed); "UL Procyon" (2); "CPSMark" (1); "BAPCo benchmark" (6); "PCMark" (237) | CpsMark+ (→ S1-58); Sibai PCMark05 papers (closed); arXiv 2005.07613, 2112.11587, 2110.07822 (fetched 200, only use the benchmarks as workloads — no scenario definitions, not candidates); ASEE 2001 "Benchmarks – Are they Really Useful?" (fetched 200, names SYSmark only — not a candidate) | — |
| 2026-10-01 | Crossref / Elsevier / ScienceDirect / Wayback | CpsMark+ DOI 10.1016/j.tbench.2023.100084 | Wayback snapshot 20230114130231 of the article page (200, gzip; abstract, highlights, graphical abstract only); graphical abstract image ars.els-cdn.com (200) → S1-58 | sciencedirect `pdfft` 403; article page 403; Elsevier API text/plain 400; Elsevier API text/xml 200 (metadata only); Wayback 2026id_/2024id_ 403 snapshots; CORE API (Cloudflare redirect); Wayback CDX for pdf.sciencedirectassets.com: no captures; Wayback CDX once "Temporarily Offline" |
| 2026-10-01 | ACM DL | 10.1145/1364644.1364647 (Sibai, PCMark05, SIGMETRICS PER 2008); 10.1145/356989.357001 (Flautner ASPLOS 2000) | ASPLOS paper later found on the authors' page (200) → S1-55 | 403, 403 (Cloudflare); Sibai papers closed, no OA copy (OpenAlex) |
| 2026-10-01 | WebSearch | EEVDF CFS gaming frame time stutter Linux scheduler evaluation paper 2024 2025 arXiv games threads | FOSDEM 2025 slides (first URL 404; FOSDEM schedule XML 200 gave the live slides URL 200 and the subtitle file 200) → S1-61 | slides URL `/slides/237450/` 404 |
| 2026-10-01 | WebSearch | thesis DXVK Proton performance analysis Linux games CPU threads wineserver measurement | none (forums, blogs) | — |
| 2026-10-01 | WebSearch | Steam Deck energy consumption measurement study paper handheld gaming PC SteamOS | press/blogs only | — |
| 2026-10-01 | WebSearch + WebFetch | lpc.events Changwoo Min LAVD slides pdf "latency criticality" gaming Steam Deck tasks | LPC 2025 slides (200) → S1-62 | — |
| 2026-10-01 | WebSearch / sched.com / lpc.events | Changwoo Min LAVD 2024 slides OSS / LPC | ossna2024.sched.com event page (200; abstract only, no slides attached); osseu2024 search (200, no hit); lpc.events event 18 search (200, unrelated) | — |
| 2026-10-01 | WebSearch | "Optimizing Scheduler for Linux Gaming" Changwoo Min slides pdf igalia | liglab.fr 2026 slide deck (200) → S1-63; Everything Open 2024 talk page (200, no slides) | — |
| 2026-10-01 | HAL | hal-05094575 (Gegout et al.) | HAL API (200) → file URL; with a curl user agent 200 PDF → S1-64 | `/document` 500; `/file/main.pdf` and the AsHES file with a browser user agent: 200 HTML Anubis bot challenge, not the PDF |
| 2026-10-01 | WebSearch | survey gamers use voice chat Discord while playing percentage concurrent applications during PC gaming study | market statistics pages (Statista, YouGov, blogs) — not literature | — |
| 2026-10-01 | WebSearch | media multitasking while playing video games study second screen browser during gameplay PC players logged | press only | — |
| 2026-10-01 | OpenAlex API | Xonotic; SuperTuxKart CPU threads; game frame rate DVFS Linux desktop; interactive application Linux scheduler latency game benchmark; Steam Deck | "Give Me Steam" ARES 2024 (→ S1-67); "Well Played, Suspect!" DFRWS EU 2024 (→ S1-68); others irrelevant | — |
| 2026-10-01 | LSU repository / Wayback | "Give Me Steam" DOI 10.1145/3664476.3670903 | Wayback capture 20241108012224 of the ACM PDF (200) → S1-67 | repository.lsu.edu (200, metadata only, no file); Wayback CDX for the DOI page: "Temporarily Offline" |
| 2026-10-01 | WebSearch / figshare | "Well Played, Suspect" Steam Deck forensic examination dfrws pdf Eichhorn | CISPA figshare API (200) → ndownloader file 49358884 (200) → S1-68 | opus.bibliothek.uni-augsburg.de: connect timeout (HTTP 000); dfrws.org search 403 |
| 2026-10-01 | WebSearch | ProtonDB empirical study compatibility reports Windows games Linux Proton paper mining | blogs only (Boiling Steam) | — |
| 2026-10-01 | TNM lab pages | Gao et al. ISPASS 2014; Flautner ASPLOS 2000 | web.eecs.umich.edu/~tnm/trev_test/publications.html (200) → ASPLOS 2000 PDF (200) → S1-55; ISPASS 2014 PDF (200) → S1-59 | tnm.engin.umich.edu/publications/ 403; Swarthmore CS97 Team12 final report 404 |
| 2026-10-01 | WebSearch | thesis measurement input latency Wayland X11 compositor frame timing Linux desktop games gamescope study | Marco Nett blog post "Measuring input latency on Linux" (blog, out of class — pointer for S3) | — |
| 2026-10-01 | WebSearch | "View Planner" VMware desktop virtualization benchmark workload operations 7-Zip Word Excel paper Agrawal; "VMware View Planner: Measuring True Virtual Desktop Experience at Scale" | vendor whitepapers only; VMware Technical Journal paper not located | — |
| 2026-10-01 | WebSearch | arXiv "Procyon" AI PC NPU benchmark characterization LLM inference laptop 2024 2025 paper; thesis "PCMark 10" workloads description …; "SYSmark 2018" OR "SYSmark 2014" Productivity Creativity Responsiveness scenarios … | vendor and press pages only | — |
| 2026-10-01 | WebSearch | FAST: Quick Application Launch on Solid-State Drives Joo Ryu Park Shin USENIX FAST 2011 Linux | kabru.eecs.umich.edu author-group PDF (HTTP 200) → S1-80 | — |
| 2026-10-01 | WebSearch | preload adaptive prefetching daemon Linux Esfahbod thesis application launches logged | cs.uwaterloo.ca course copy of the thesis (HTTP 200) → S1-81 | — |
| 2026-10-01 | WebSearch | desktop application launch frequency field study logged launches per day users Windows | hits are press reports of a Soluto Windows 8 app-launch study (computerworld, betanews, techspot) and mobile studies; no peer-reviewed desktop source | press reports not literature; not followed |
| 2026-10-01 | WebSearch | snap flatpak application startup time measurement paper Linux desktop cold start evaluation | ph.pollub.pl JCSI 2023 PDF (HTTP 200) → S1-83; forum.snapcraft.io and ubuntu.com blog posts (vendor/project documents, S2 class, not followed) | — |
| 2026-10-01 | WebSearch | "application launch" desktop Linux prefetching paper evaluation applications launch time page cache 2015..2024 | rtcl.eecs.umich.edu FAST'23 PDF (HTTP 200) → S1-82 | — |
| 2026-10-01 | WebSearch | predicting application launches desktop computer logged usage study users applications started per day "desktop" launcher prediction | patents and a mobile thesis only | no desktop observation |
| 2026-10-01 | WebSearch | logging study Windows PC usage "applications" launched per hour field study users process creation telemetry | arxiv.org/pdf/2105.09900 (HTTP 200) → S1-84 | — |
| 2026-10-01 | WebSearch | Amann Proksch Nadi Mezini "A Study of Visual Studio Usage in Practice" SANER 2016 build events pdf | st.informatik.tu-darmstadt.de artifacts page (WebFetch 200; CSV tables, no paper PDF); OpenAlex API (200, no OA copy); Semantic Scholar API (200, "CLOSED") | dl.acm.org PDF for 10.1145/3196398.3196400 HTTP 403; sarahnadi.org/publications HTTP 404; proks.ch/publications HTTP 200 with DOI links only |
| 2026-10-01 | WebSearch | zora.uzh.ch Proksch "Enriched event streams" dataset in-IDE activities | tuprints.ulb.tu-darmstadt.de/id/eprint/6971 (Proksch PhD thesis) | TUprints HTTP 200 but an Anubis bot-challenge page; Wayback CDX 200 listed the landing page; Wayback copy of proksch-phd-thesis.pdf HTTP 200 truncated at 1,048,576 bytes twice (unreadable, discarded); Wayback CDX later "Temporarily Offline" |
| 2026-10-01 | WebSearch | Blackbox large scale repository novice programmers activity BlueJ compile events per session Brown Kölling Altadmri | kar.kent.ac.uk/38938 (HTTP 200) → PDF → S1-85 | — |
| 2026-10-01 | WebSearch | empirical study local developer builds frequency duration incremental versus clean builds IDE telemetry developers | LaForge (arXiv 2108.12469, build tool, no observation of users), ICSE 2022 incremental build of configurations (not user behaviour), getdx newsletter (secondary) | none followed to a candidate |
| 2026-10-01 | WebSearch | "Build Latency, Predictability, and Developer Productivity" Google research IEEE Software developer builds per week | research.google publication page (HTTP 200; only an ieeexplore link, document 10176199) | no open copy; Google's distributed builds, not desktop |
| 2026-10-01 | WebSearch | survey users running local LLM inference on personal computers how often model sizes empirical study 2024 2025 arXiv | arXiv 2511.07885 (local query coverage), 2601.09527 (SME deployment guide), 2505.15030 | followed separately below |
| 2026-10-01 | WebSearch | how users launch applications desktop field study start menu taskbar dock logged launches study HCI | academia.edu start-menu usability studies, KDE Kickoff (akademy 2006) slides | lab usability tests, no logged launch rates |
| 2026-10-01 | WebSearch | Beller Gousios Panichella Zaidman "Developer Testing in the IDE: Patterns, Beliefs, and Behavior" WatchDog test runs duration pdf | inventitech.com/publications (HTTP 200) → accepted-manuscript PDF (HTTP 200) → S1-86 | repository.tudelft.nl/file/File_431a1200… HTTP 404; cs.unibg.it FSE'15 proceedings PDF HTTP 401; resolver.tudelft.nl → repository.tudelft.nl record: curl empty reply, WebFetch timeout |
| 2026-10-01 | WebSearch | vbench benchmarking video transcoding in the cloud Lottarini ASPLOS 2018 pdf video duration resolution distribution uploads | arcade.cs.columbia.edu/vbench (HTTP 200) | arcade.cs.columbia.edu/vbench/data/vbench.pdf HTTP 404; Wayback 2020id_ copy HTTP 404; OpenAlex lists gold OA at dl.acm.org, but dl.acm.org/doi/pdf/10.1145/3173162.3173207 HTTP 403 (cloud transcoding, not a desktop observation in any case) |
| 2026-10-01 | WebSearch | real-world PC usage telemetry characterization applications CPU utilization client workloads IISWC Intel DCA consumer laptops study | arxiv.org/pdf/2602.22339 (HTTP 200) → S1-87; Intel IT white papers (vendor documents, not followed) | — |
| 2026-10-01 | WebSearch | Intel DCA telemetry "frgnd_backgrnd_apps" foreground background applications UCSD capstone analysis | patents, Intel PMT specifications, Nokia NSP pages | no further analysis of the DCA foreground/background table found |
| 2026-10-01 | WebSearch | why people run LLMs locally interview survey study r/LocalLLaMA users hardware usage frequency CHI 2025 | blog posts, a Hugging Face forum survey call, a University of Turku thesis record (usability evaluation, no job sizes) | no peer-reviewed observation of what local inference users run |
| 2026-10-01 | WebSearch | arXiv empirical study Ollama llama.cpp users consumer GPUs model sizes quantization deployed locally mining GitHub issues or Hugging Face downloads 2025 | vendor and blog pages only | — |
| 2026-10-01 | arXiv API | all:"local LLM" AND all:users AND all:survey | — | export.arxiv.org over HTTP: empty reply; over HTTPS: HTTP 429 "Rate exceeded" |
| 2026-10-01 | WebSearch | survey of video creators editing practices export render time video length study CHI CSCW amateur YouTubers editing software usage | AVscript (arXiv 2302.14117), ChunkyEdit (Adobe), formative studies of 8–9 creators | no study reports render/export job sizes or frequencies |
| 2026-10-01 | WebSearch | PARSEC benchmark suite characterization Bienia Kumar Singh Li PACT 2008 x264 native input frames resolution pdf | cs.princeton.edu TR-811-08 PDF (HTTP 200) → S1-88 | — |
| 2026-10-01 | WebSearch | measurement what desktop application does after startup network connections first minutes browser launch Leith "phone home" Chrome Firefox startup | scss.tcd.ie author PDF (HTTP 200) → S1-89; brave.com first-run blog (vendor document, S2 class, not followed) | — |
| 2026-10-01 | WebSearch | Electron desktop applications performance empirical study startup time memory comparison native apps measurement paper | betterstack, dev.to, electronjs.org documentation | blog benchmarks and project documentation only; no peer-reviewed Linux start-up observation |
| 2026-10-01 | WebSearch | personal backup practices home computer users survey how often back up manual backup study SOUPS CHI | pim.famnit.upr.si authors' draft (HTTP 200) → S1-90; strathprints.strath.ac.uk CHI '25 manuscript (HTTP 200) → S1-91; Acronis 2009 press release and storagenewsletter (vendor surveys, not followed) | — |
| 2026-10-01 | WebSearch | "local builds" developers empirical study build scans Gradle Develocity build duration distribution developer machines incremental compilation study 2022 2023 | gradle.com and dpe.org vendor pages, arXiv 2408.11544 (buildability across Java versions, not user behaviour), uwaterloo incremental-build forecasting (CI) | no peer-reviewed observation of local build sizes on developer desktops |
| 2026-10-01 | direct (known paper) | Seo et al. ICSE 2014 "Programmers' build errors" | research.google.com/pubs/archive/42184.pdf (HTTP 200) → S1-92 | — |
| 2026-10-01 | WebSearch | "applications per day" OR "distinct applications" desktop computer logging study knowledge workers number of applications used per day | publications.tno.nl Koldijk 2011 activity-logging paper (SWELL precursor, left to the T1/T2 share); Pegasystems "Demystifying the desktop" and Asana/Forrester pages (vendor reports, not literature) | no launch-rate statistic in peer-reviewed form found in this query |
| 2026-10-01 | WebSearch | Ottawa Linux Symposium 2007 "Getting maximum mileage out of tickless" Siddha Pallipadi van de Ven wakeups per second desktop idle processes | kernel.org/doc/ols/2007/ols2007v2-pages-201-208.pdf (HTTP 200; read, kernel-level idle interrupt counts only, no S1 topic covered, discarded); its reference to Dave Jones' OLS 2006 paper followed: kernel.org/doc/ols/2006/ index (HTTP 200) → ols2006v1-pages-441-450.pdf (HTTP 200) → S1-22 | ols2006v1-pages-431-440.pdf and -451-460.pdf HTTP 404 (wrong page-range guesses) |

## 2. Candidates

Index (topics as covered in each entry; "partial", "existence", "locates only", "context" as defined there):

| id | source | what was observed | topics covered |
|---|---|---|---|
| S1-01 | Meyer et al. 2017 (IEEE TSE), work life of developers | 20 developers, Windows, ≈11 workdays each, foreground sampled every 10 s | T1, T2; T10 partial |
| S1-02 | Sánchez Sánchez et al. 2020 (Data in Brief), BEHACOM | dataset: 12 users (8 Windows, 3 Linux, 1 both), 55 days, 2019–20 | T1, T2 (dataset fields, no statistic) |
| S1-03 | Iqbal & Horvitz 2007 (CHI), disruption and recovery of computing tasks | 27 Microsoft employees, 2 weeks of logging | T1, T2, T10 |
| S1-04 | Mark et al. 2016 (CHI, two papers on one observation) | 40 information workers, ≈12 days, Windows | T2, T10 |
| S1-05 | Mark et al. 2014 (CHI) and 2015 (CSCW), one observation | 32 information workers, 5 days, Windows 7 | T2, T10 |
| S1-06 | Hutchings et al. 2004 (AVI), VibeLog | 39 volunteers, 3 weeks, Windows XP | T1, T2 |
| S1-07 | González & Mark 2004 (CHI) | shadowing, 14 information workers, 3 days each | T2 |
| S1-08 | Smith et al. 2003 (OZCHI), GroupBar | informal study N = 16; 5-person deployment | T1 |
| S1-09 | Yin et al. 2026 (arXiv), FOCAL / DesktopBench | benchmark assembled from task templates, not a log of everyday use | none (named in the brief; does not cover) |
| S1-10 | Koldijk et al. 2014 (ICMI), SWELL-KW | laboratory, 25 participants × ≈3 h, Windows 7 | T2 (dataset) |
| S1-11 | Reeves et al. 2019/2021 (Human–Computer Interaction), Screenomics | example analysis of 30 student laptops | T2 |
| S1-12 | Mark, Gonzalez & Harris 2005 (CHI) | shadowing, 24 information workers (informants overlap S1-07) | T2 |
| S1-13 | Tak 2011 (PhD thesis), PyLogger window-switching study | 25 users, 3 weeks | T1, T2; T9 proxy |
| S1-14 | Czerwinski et al. 2004 (CHI), diary study | 11 Windows users, 1 week, self-report | T2 |
| S1-15 | Cao et al. 2021 (CHI), multitasking during remote meetings | Microsoft telemetry, Feb–May 2020 | T1, T10 |
| S1-16 | Xu 2010 (PhD thesis, Lille), WindowsOSLog | 26 participants, ≥5 weeks, Windows | T1 |
| S1-17 | Mark et al. 2012 (CHI), work without email | 13 information workers, 8 days | T2 |
| S1-18 | Judd 2015 (Australasian Journal of Educational Technology) | open-access lab, 1,230 students, Mac, 2009 | T2 |
| S1-19 | Dodier-Lazaro 2020 (PhD thesis, UCL), Xubuntu field study | 13 Xubuntu users' own computers, ≈3 weeks | T1; T9 proxy (Linux) |
| S1-20 | Meyer et al. 2014 (FSE), developers' perceptions of productivity | 11 developers observed 4 h each | T2 |
| S1-21 | Jones et al. 2012 (Energy Efficiency), laptop energy-saving opportunities | 13 student laptops (Windows), 1 month | T1; T3 marginal |
| S1-22 | Jones 2006 (Ottawa Linux Symposium), "Why userspace sucks" | one Fedora Core 5 system: boot, login, idle desktop | T1, T9 (Linux, program side) |
| S1-30 | Dubroy & Balakrishnan 2010 (CHI), tabbed browsing | 21 Firefox users, 13–21 days | T3; T2, T10 partial |
| S1-31 | Reis, Moshchuk & Oskov 2019 (USENIX Security), Site Isolation | Chrome 69 telemetry on Windows, Oct 2018; one Windows 10 microbenchmark | T3 (renderer counts are Windows: context) |
| S1-32 | Huang & White 2010 (Hypertext), parallel browsing | >50 M browser plug-in users, June 2009 | T3 partial; T2, T10 partial |
| S1-33 | Weinreich et al. 2008 (ACM TWeb), Web use | 25 users, winter 2004/05 | T3, T10 |
| S1-34 | von der Weth & Hauswirth 2013/2014 (arXiv), DOBBS | 30 Firefox add-on users, to Jan 2014 | T3; T2, T10 partial |
| S1-35 | Ma et al. 2023 (CHI), browsing clutter | survey N = 400, 2022 | T3 (self-report) |
| S1-36 | Chang et al. 2021 (CHI), cost structure of tab usage | MTurk N = 103, tab snapshot | T3 (self-report) |
| S1-37 | Reis & Gribble 2009 (EuroSys), browser process models | design; one Windows XP machine | T3 (existence; context) |
| S1-38 | Vila & Köpf 2017 (USENIX Security; arXiv), Loophole | two machines (4 GB and 8 GB RAM) | T3 (program side; Linux likely, not stated) |
| S1-39 | Kooti et al. 2015 (WWW), Yahoo Mail | 2 M users | T10 partial |
| S1-40 | Fisher et al. 2006 (CSCW), email overload revisited | 600 Outlook users, 2005–06 | T10 |
| S1-41 | Kumar & Tomkins 2010 (WWW), online browsing | Yahoo! toolbar sample, March 2009 | T10; T1 partial |
| S1-42 | Lut et al. 2021 (arXiv), how we browse | 31 students, 14 days, 2019 | T10 partial; T1, T3 partial |
| S1-43 | Lafreniere et al. 2009/2010 (TR CS-2009-27; GI 2010), ingimp | 211 GIMP users, 2007–09, 73 % Windows / 26 % Linux | T10, T1, T9 partial |
| S1-44 | Chang, Varvello et al. 2021 (IMC), Zoom/Webex/Meet | Linux cloud VMs, 2021 | T10 (existence) |
| S1-45 | MacMillan et al. 2021 (IMC), video-conferencing network use | two Ubuntu 20.04.1 laptops | T10 (existence) |
| S1-46 | Leskovec & Horvitz 2008 (arXiv; WWW), Messenger network | all Messenger users, June 2006 | T10 |
| S1-47 | Wang et al. 2022 (CSCW), Slack group chat | 4,300 channels, 2016–19 | T10 partial |
| S1-48 | Oliveira et al. 2021/2023 (arXiv), Chromebook field study | 114 Google employees, 3 months, ChromeOS | T3; T2 partial |
| S1-49 | Jackson et al. 2003 (Int. J. Information Management), email interruptions | 15 employees, 28 working days, Outlook on Windows | T10 partial; T2 partial |
| S1-50 | Avrahami et al. 2006 (CHI) and 2008 (CSCW), one IM corpus | 16–19 IM users, 2005, Windows | T10; T2 partial |
| S1-51 | Isaacs et al. 2002 (CSCW), workplace IM (Hubbub) | 437 users, 2000–01 | T10; T2 partial |
| S1-55 | Flautner 2001 (PhD thesis) / Flautner et al. 2000 (ASPLOS) | laboratory, Linux 2.2.3 and 2.3.99 kernels | T4 weak, T1, T6 (Linux); T7 existence |
| S1-56 | Blake et al. 2010 (ISCA), thread-level parallelism of desktop applications | laboratory, Windows 7 / OS X | context only (T1, T4, T6) |
| S1-57 | Bircher & John 2008 (ICS); Bircher 2010 (PhD thesis) | SYSmark 2007 composition | T7 |
| S1-58 | Zhang & Wu 2022 (BenchCouncil Transactions), CpsMark+ | abstract, highlights and graphical abstract only | T7 partial |
| S1-59 | Gao et al. 2014 (ISPASS), thread-level parallelism on mobile | Android laboratory | context only (T4, T1) |
| S1-60 | Endo et al. 1996 (OSDI), latency of interactive systems | critique of SYSmark NT/32 and Winstone | T7 |
| S1-61 | Righi 2025, FOSDEM talk (not peer-reviewed) | one Linux desktop trace of a game | T4 (Linux); T6 context |
| S1-62 | Min 2025, Linux Plumbers talk (not peer-reviewed) | one `perf sched` trace of a Proton game | T4 (Linux); T1 weak |
| S1-63 | Min 2026, seminar talk (not peer-reviewed) | one trace of a Proton game (Troy.exe) | T4 (Linux); T1 weak |
| S1-64 | Gegout et al. 2025 (AsHES / IPDPS workshops), containerised cloud gaming | server testbed | T4 (existence) |
| S1-65 | Chambers et al. 2005 (IMC), on-line games incl. Steam CDN | Steam CDN trace, 2004–05 | T4 partial |
| S1-66 | Lin, Bezemer & Hassan 2017 (Empirical Software Engineering), Steam game updates | update notes of 50 popular Steam games | T4 partial |
| S1-67 | Alsmadi et al. 2024 (ARES), Steam Deck memory forensics | one Steam Deck, before and during a game | T4 (Linux) |
| S1-68 | Eichhorn et al. 2024 (DFRWS EU), Steam Deck forensics | one Steam Deck | T4 (existence) |
| S1-80 | Joo et al. 2011 (FAST), quick application launch on SSDs | one Fedora 12 desktop, 22 applications | T9 (Linux) |
| S1-81 | Esfahbod 2006 (MSc thesis), preload | one Fedora Core 5 machine | T9 (Linux) |
| S1-82 | Ryu et al. 2023 (FAST), Paralfetch | one Ubuntu laptop, kernel 5.4.51, 16 applications | T9 (Linux) |
| S1-83 | Cichocki & Przyłucki 2023 (JCSI), Flatpak and Snap | toy application, Ubuntu 23.04 | T9 (Linux, weak) |
| S1-84 | Giovanini et al. 2021 (arXiv), computer-usage profiles | 31 Windows 10 users, 8 weeks | T1, T9 (locates only) |
| S1-85 | Brown et al. 2014 (SIGCSE), Blackbox | >150,000 BlueJ users | T6 (thin) |
| S1-86 | Beller et al. 2017/2019 (IEEE TSE), developer testing in the IDE | 2,443 developers, 2014–17 | T6 |
| S1-87 | Cheon et al. 2026 (arXiv), Intel client telemetry | 1 M devices | T1, T6, T9 (locates only) |
| S1-88 | Bienia et al. 2008 (Princeton TR-811-08), PARSEC | benchmark definition | T6 (definition) |
| S1-89 | Leith 2020 (TCD report), browsers phoning home | two MacBooks, Feb 2020 | T9 context (macOS) |
| S1-90 | Kljun et al. 2016 (JASIST), backup strategies | survey, 319 people / 542 computers, 2013 | T6 |
| S1-91 | Wunder et al. 2025 (CHI), data loss and recovery | survey, 1,423 people, Germany/UK/US | T6 |
| S1-92 | Seo et al. 2014 (ICSE), build errors at Google | 26.6 M builds, 18,000 developers, 2012–13 | T6 |

### S1-01 — Meyer 2017, The work life of developers

- **Citation.** André N. Meyer, Laura E. Barton, Gail C. Murphy, Thomas Zimmermann, Thomas Fritz. "The Work Life of Developers: Activities, Switches and Perceived Productivity." IEEE Transactions on Software Engineering 43(12), December 2017.
- **Copy read.** https://thomas-zimmermann.com/publications/files/meyer-tse-2018.pdf (authors' copy, 16 pp., journal layout), accessed 2026-10-01, `sources/S1-01/meyer-tse-2018.pdf`, SHA-256 `240f857ca475aab78de0b7a064d460f6d52d77ff86ec0bf3a99a9b6e3285812b`.
- **One observation.** Yes: one monitoring deployment, 20 professional developers at 4 companies, average 11 workdays each, 2,197 hours of computer use.
- **Machine/platform, subject, window named?** Platform named (Windows 7, 8, 10); subject named (professional developers, companies in the USA, Canada, Switzerland); calendar window of the deployment not stated in the passages read.
- **Verbatim passages.**
  > "we deployed a monitoring application at 20 computers of professional software developers from four companies for an average of 11 full workdaysin situ." (p. 1, abstract)

  > "The monitoring application was developed and tested to run on the Windows 7, 8 and 10 operating system." (p. 4, §3.2)

  > "The monitoring application logged the currently active process and window title every 10 seconds, or an 'idle' entry in case there was no user input for longer than 10 seconds." (p. 4, §3.2)

  > "During the study, the monitoring application collected data from 2197 hours of participants' computer use over a total of 220 work days." (p. 5, §4)

  > "Participants used a total of 331 different applications, with each participant using an average of 42.8 ( ±13.9) different applications over the study duration and 15.8 ( ±4.1) appli- cations per day." (p. 7, §5.1.3)

  > "TABLE 3: Top 10 Used Applications (Sorted by Usage). Application % of time used # of users Microsoft Outlook 14.2% 18 PuTTY 12.8% 8 Google Chrome 11.4% 16 Microsoft Internet Explorer 9.4% 20 Microsoft Visual Studio 8.3% 13 File Explorer 6.6% 20 Mozilla Firefox 5.9% 8 Eclipse 3.0% 10 Microsoft OneNote 2.3% 9 Command Line 2.2% 16" (p. 7, Table 3)

  > "With the exception of planned meetings, a developer only remains in an activity between 0.3 (±2.6) and 2.0 ( ±6.5) minutes before switching to another one." (p. 9, §5.2)

  > "For example, participant S4 was coding in the late afternoon for 135.7 minutes, without any break longer than 2 minutes." (p. 9, §5.2)

  > "The activity pattern, which occurred most often, was a quick switch to emails during coding tasks." … "After these quick switches, developers usually switch back to their main coding task." (p. 9, §5.2)

  > "Every hour, developers take an average of 2.5 ( ±0.8) short breaks that are about 4.2 ( ±0.6) minutes long each" (p. 7, §5.1.2)

  > "A developer's typical work day is mostly spent on coding (21.0%), emails (14.5%), and work-related web browsing (11.4%)." (p. 7, §5.1.4)

  > "Similarly, Amann et al. found that developers continue working while builds run in the background [13]." (p. 9, §5.2)
- **Coverage.**
  - T1 covers: applications used per day (mean 15.8, SD 4.1, per participant per day) and over the study (42.8); share of logged time per application (Table 3: Outlook, PuTTY, Chrome, IE, Visual Studio, File Explorer, Firefox, Eclipse, OneNote, Command Line) — foreground time, not simultaneous open count; 20 developers, Windows 7/8/10.
  - T2 covers: time in an activity before switching (means 0.3–2.0 min per activity category, Table 4; planned meetings 15.8 min), longest continuous coding span 135.7 min, return pattern coding → email → coding (n-gram analysis), short breaks 2.5 per hour of 4.2 min; granularity: activity category derived from foreground process + window title sampled every 10 s; statistic: mean ± SD across participants.
  - T3 does not cover. T4 does not cover. T6 does not cover (only the cited remark on builds running in the background, from another study). T7 does not cover. T9 does not cover.
  - T10 covers partially: email time share 14.5% of logged time, 74.3 min/day email for most participants (p. 8); no per-message rate.
- **Side.** User-side values (any platform; here Windows).

### S1-02 — Sánchez Sánchez 2020, BEHACOM dataset

- **Citation.** Pedro M. Sánchez Sánchez, José M. Jorquera Valero, Mattia Zago, Alberto Huertas Celdrán, Lorenzo Fernández Maimó, Eduardo López Bernal, Sergio López Bernal, Javier Martínez Valverde, Pantaleone Nespoli, Javier Pastor Galindo, Ángel L. Perales Gómez, Manuel Gil Pérez, Gregorio Martínez Pérez. "BEHACOM – a dataset modelling users' behaviour in computers." Data in Brief 31 (2020) 105767, doi 10.1016/j.dib.2020.105767 (PMC7270191). Dataset: BEHACOM, Mendeley Data, doi 10.17632/cg4br62535.2.
- **Copy read.** (1) Europe PMC full-text XML, https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7270191/fullTextXML (CC BY article), accessed 2026-10-01, `sources/S1-02/behacom-PMC7270191-fulltext.xml`, SHA-256 `c7880aa76a91786aa91fa5e76f331cb8db3370967b53f9007f5feb17d8f3ccfd`. (2) Mendeley Data public API record, https://data.mendeley.com/public-api/datasets/cg4br62535 (version 2), accessed 2026-10-01, `sources/S1-02/mendeley-public-api-cg4br62535.json`, SHA-256 `342375a3f391957b78fbbff98dd602dd2acb36cf4e14945d082b9f64b1f869dd`. The dataset itself (Behacom.zip, 37,414,157 bytes) was not downloaded by this reader.
- **One observation.** Yes: 12 users on their own computers, 55 consecutive days, 2019-11-20 to 2020-01-14.
- **Machine/platform, subject, window named?** Platform named (8 Windows, 3 Linux, 1 both; Linux collector for Debian-based distributions using xdotool and psutil); subject named (12 right-handed males aged 20–45, Spanish and Italian); window named (first and last timestamps).
- **Verbatim passages.**
  > "This paper details the methodology and approach conducted to monitor the behaviour of twelve users interacting with their computers for fifty-five consecutive days without preestablished indications or restrictions. The generated dataset, called BEHACOM, contains for each user a set of features that models, in one-minute time windows, the usage of computer resources such as CPU or memory, as well as the activities registered by applications, mouse and keyboard." (Abstract)

  > "The twelve individuals are right-handed male, with ages ranging from 20 to 45 years old. Eight of them use Windows as operating system, three Linux, and one both. … The first timestamp (UNIX ms) of the dataset is 1574245230186 (Wednesday, 20-Nov-19 10:20:30 UTC) and the last one is 1578995678310 (Tuesday, 14-Jan-20 09:54:38 UTC)." (§ Scenario description and selected features)

  > "active_apps_average Average number of applications active during the time window." … "current_app Application executable name in foreground when the vector was generated." … "penultimate_app Penultimate application executable name in foreground during the time window." … "changes_between_apps Number of changes between different foreground applications during the time window." … "current_app_foreground_time Number of seconds that the current application has been in foreground during the time window. If no application changes occur, the value of this feature will be 60." (Table 5, Application usage statistics features)

  > "Application and resource usage: Timestamp, number of applications active, name of the current application in foreground, percentage of CPU used by the process in foreground, … number of processes of the application in foreground." (§ Data collection)

  > "To obtain the process identifier (pid) of the application in foreground, xdotool [8] is used in the Linux implementation and pywin32 (win32process and win32gui) [9] in Windows." (§ Data collection)

  > "This file is read line by line, extracting the periodic measurements (every 5 seconds) about active applications and resources in use." (§ Feature extraction)

  > "Data repository: BEHACOM [1] Data identification number: 10.17632/cg4br62535.2Direct URL to data: https://data.mendeley.com/datasets/cg4br62535/2" (Specification table)

  > "In consequence, these periods will have their corresponding vectors with the keyboard, mouse and application features set to zero" (§ Limitations)

  Mendeley record (JSON excerpt, field `data_licence`): "short_name": "CC BY 4.0", "full_name": "Creative Commons Attribution 4.0 International"; files "Behacom.zip" size 37414157 and "scripts.zip"; "publish_date": "2020-05-06T15:26:50.362Z".
- **Coverage.**
  - T1 covers (as a dataset; no statistic computed in the paper): per-minute average number of active applications, foreground application executable name; 12 users, Windows and Linux, Nov 2019 – Jan 2020.
  - T2 covers (as a dataset): per-minute foreground application name, previous foreground application, number of foreground application changes, seconds in foreground; granularity application (executable), 1-minute aggregates from 5-second samples; no window titles; access: Mendeley Data, CC BY 4.0. The paper reports no switching statistic; one would have to be computed from the CSVs (S3's remit).
  - T3, T4, T6, T7, T9, T10 do not cover.
- **Side.** User-side (applications open, foreground changes) from any platform; Linux subset of 3–4 users.

### S1-03 — Iqbal 2007, Disruption and recovery of computing tasks

- **Citation.** Shamsi T. Iqbal, Eric Horvitz. "Disruption and Recovery of Computing Tasks: Field Study, Analysis, and Directions." CHI 2007, San Jose, 28 April – 3 May 2007.
- **Copy read.** https://www.erichorvitz.com/CHI_2007_Iqbal_Horvitz.pdf (authors' copy, 10 pp.), accessed 2026-10-01, `sources/S1-03/CHI_2007_Iqbal_Horvitz.pdf`, SHA-256 `8ac1b548e8558c3575a7547bca6ca19df867bff7b10664c46df781d72ea04876`.
- **One observation.** Yes: one DART logging deployment, 27 people at Microsoft, 2 weeks, 2,267 hours, 974 sessions.
- **Machine/platform, subject, window named?** Platform implied Windows (Outlook, Windows Messenger, MSN Messenger, Office Communicator; Eve monitoring infrastructure) but the OS is not named in the passages read; subject named (program managers, administrators, researchers, developers at "our organization"); calendar window not stated.
- **Verbatim passages.**
  > "DART runs as a background process, and continues to logs the name, size, and location of all windows on a computing system, noting the op ening and closing of windows. The system also logs user activities, including when users are actively engag ed with the software, keyboard and mouse activity, and swit ches among windows as well as actions of saving, cutting , and pasting." (p. 4)

  > "We deployed DART on the primary machines of 27 people at our organization, whose job descriptions ranged from program manager, administrator, and researcher to s oftware developer." (p. 4)

  > "We collected 2,267 hours of activity data over a pe riod of 2 weeks, resulting in 974 sessions (M(session length) =2h, 17m, S.D= 410.37 m)." (p. 4)

  > "Preliminary ana lysis showed that, on average, the maximum time spent on an application before switching to another is just abo ve 4 minutes, with an average of below a minute." (p. 5)

  > "Overall, we found that, on an hourly basis, a user' s primary tasks were interrupted by an average of 4.28 email (S.D.=5.56) alerts and 3.21 IM (S.D.=4.31) alerts, with an overall average rate of 3.74/hour (S.D.=4.94)." (p. 5)

  > "For 40.8% (2344/5747) of the email alerts, users re sponded immediately (<15s), leaving on average 3 (S.D.=1.92 ) task windows suspended." (p. 5)

  > "For email, the average time to retur n to any suspended application (time spent on the diversion) was 9 minutes and 33 seconds (S.D.=13m, 15s). For IM, th e return time was 8 minutes (S.D.=11m, 32s) on averag e." (p. 5)

  > "Phases Email Alerts Mean(S.D) IM Alerts Mean(S.D) Pre-interruption 0.84(0.6) 0.84(0.6) … Resumption: Immediate Response 2.34(2.71) 2.56(2.82) … Table 1. Task switches per minute across different phases fo r email and IM alerts." (p. 6, Table 1)

  > "Actions Pre-interruption Mean(S.D.) Diversion Mean(S.D.) p Mail open 0.53 (0.5) 3.66(6.7) 0.001 Mail write 0.44(0.31) 3.15(5.71) 0.002 Mail send 0.35(0.27) 1.69(2.89) 0.008 Table 2. Actions per minute of email operations during pre- interruption and diversion phases." (p. 6, Table 2)

  > "On average, 27 % of the alerts resulted in users being diverted from these prior active windows for more than 2 hours into the resum ption phase." (p. 7)
- **Coverage.**
  - T1 covers: suspended task windows at the moment of an alert (mean 3, SD 1.92–2.3); email client and IM clients running concurrently with the primary task; 27 information workers.
  - T2 covers: task switches per minute (pre-interruption baseline 0.84, SD 0.6; up to 2.56 in resumption), mean time on an application before switching below 1 min, mean maximum just above 4 min; return to the suspended application after an alert 9 min 33 s (email) and 8 min (IM); 27% of alerts lead to diversions over 2 hours (A → B → A return pattern); granularity window/application; statistic: means (SD) across users/events.
  - T3 does not cover. T4 does not cover. T6 does not cover. T7 does not cover. T9 does not cover.
  - T10 covers: incoming email alerts 4.28/hour and IM alerts 3.21/hour; mail opens 0.53/min, writes 0.44/min, sends 0.35/min in the 5-minute pre-interruption baseline (rates measured only in windows around alerts, not over the whole session).
- **Side.** User-side values.

### S1-04 — Mark 2016, Neurotics can't focus (with: Email duration, batching and self-interruption, same observation)

- **Citation.** (a) Gloria Mark, Shamsi T. Iqbal, Mary Czerwinski, Paul Johns, Akane Sano. "Neurotics Can't Focus: An in situ Study of Online Multitasking in the Workplace." CHI 2016. (b) Same authors. "Email Duration, Batching and Self-interruption: Patterns of Email Use on Productivity and Stress." CHI 2016. Both report the same 40-participant deployment, so they count as one observation.
- **Copy read.** (a) https://ics.uci.edu/~gmark/Home_page/Publications_files/CHI%2016%20Multitasking%20and%20Focus.pdf (author's copy, 6 pp.), accessed 2026-10-01, `sources/S1-04/mark-chi16-neurotics.pdf`, SHA-256 `75224a9aa38fee32ac36c70cfd0831f7291901a19a7a28223eb95311e8a28870`. (b) https://ics.uci.edu/~gmark/Home_page/Publications_files/CHI%2016%20Email%20Duration.pdf (author's copy), accessed 2026-10-01, `sources/S1-04/mark-chi16-email-duration.pdf`, SHA-256 `6897f2d9867042917c96ac46dc888ba714e6d294b59c7ac0ccf6459369de7637`.
- **One observation.** Yes: 40 information workers at a large US high-tech corporation, about 12 business days each, 1,981.5 hours of window logging.
- **Machine/platform, subject, window named?** Platform named ("custom-built Windows Activity Logging software"); subject named (40 volunteers, 20 female, 20 male; administrative support, engineering, management); calendar window not stated.
- **Verbatim passages.**
  > "Forty volunteers (20 females, 20 males) in a large high tech U.S. corporation, who responded to an ad, were observed in situ in their real work environment for about 12 business days." (a, p. 2, Method)

  > "Participants' computer activity at work was logged during all business hours automatically via custom-built Windows Activity Logging software. This logging software tracks every open application, which window is in the foreground, and whether the user is interacting with that window (with mouse, keyboard, touch, etc.)." (a, p. 3)

  > "Focus Duration (online) was measured by dividing total daily logged computer duration by the number of computer screen switches." (a, p. 3)

  > "Averaged over all workdays per person, and for all applications and online sites, the median duration of focus is about 4 0 seconds." (a, p. 3, Results)

  > "Mean sd Median %Total All computer usage 47.0 21.4 40.2 100% Email usage 61.8 35.1 51.8 33.95 Productivity SW usage 64.0 39.3 52.9 21.14 Communication SW usage 42.5 25.5 34.5 5.96 Daily switches within apps 131.9 103.7 112.0 -- Daily switches betw apps 272.7 117.9 261.0 -- Table 1. Avg. online screen focus duration (sec.) and switches." (a, p. 3, Table 1)

  > "The total hours of data collected for window logging was 1981.5, with an average of 49.5 hours of computer screen data logged per participant. The average number of weekdays with window activity logged per person (i.e. excluding Saturdays and Sundays) was 12.4 days." (b, p. 7, Results)

  > "Table 2 shows that the average daily time spent by our participants on the computer (averaged over work days) is about four and a half hours. Our 40 participants averaged almost one and a half hours per day of time on email and checked their email on average 77 times per day." (b, p. 7)

  > "Email Checks was measured as the number of separate times that the email client switched to the foreground." (b, p. 5)
- **Coverage.**
  - T1 does not cover (open-application counts are logged but not reported).
  - T2 covers: focus duration per screen (mean 47.0 s, SD 21.4, median 40.2 s, per person-day average over 40 participants); daily switches between applications (mean 272.7, median 261.0) and within applications (mean 131.9, median 112.0); by application class (email median 51.8 s, productivity software 52.9 s, communication software 34.5 s); granularity window/application; Windows; logging method named.
  - T3, T4, T6, T7, T9 do not cover.
  - T10 covers: email checks (email client brought to foreground) mean 77 per day; email time about 1.5 h/day of about 4.5 h daily computer time.
- **Side.** User-side values.

### S1-05 — Mark 2014, Bored Mondays and focused afternoons (with: Focused, aroused, but so distractible, CSCW 2015, same observation)

- **Citation.** (a) Gloria Mark, Shamsi T. Iqbal, Mary Czerwinski, Paul Johns. "Bored Mondays and Focused Afternoons: The Rhythm of Attention and Online Activity in the Workplace." CHI 2014. (b) Gloria Mark, Shamsi Iqbal, Mary Czerwinski, Paul Johns. "Focused, Aroused, but so Distractible: A Temporal Perspective on Multitasking and Communications." CSCW 2015. Both report the same 32-participant, 1,509-hour deployment (one observation).
- **Copy read.** (a) https://www.gwern.net/doc/psychology/writing/2014-mark.pdf (mirror of the published paper, 10 pp.), accessed 2026-10-01, `sources/S1-05/2014-mark-bored-mondays.pdf`, SHA-256 `9cba7136abbbacf75c8ef90673f7e8894924abd028ba1681b9feafb820d90d6c`. (b) https://ics.uci.edu/~gmark/Home_page/Publications_files/CSCW%202015%20Focused.pdf (author's copy), accessed 2026-10-01, `sources/S1-05/mark-cscw15-focused.pdf`, SHA-256 `8b4399b721ee025ed7f9c013b96cf5544ae00c5914a13c3a6629b73ccc6f104a`.
- **One observation.** Yes: 32 information workers, 5 workdays each, 160 person-days, 1,509 hours, 91,409 window switches.
- **Machine/platform, subject, window named?** Platform named (Windows 7); subject named (researchers, managers, administrators, an engineer, a director, a designer, a consultant); calendar window not stated.
- **Verbatim passages.**
  > "We logged online interactions with custom -built software that captured all activity in the Windows 7.0 Operating System. This included beginning and end times for th e lifespan of every window, and the beginning and end times for every instance of every for eground window." (a, p. 4)

  > "We collected data on each of the 32 participants for 5 days each, for a total of 160 person -days, or 1,509 hours of data collection. Our computer logging software collected 91,409 computer window switches." (a, p. 5)

  > "A Bonferroni test (.05) showed Win Switches were significantly higher o n Monday (M= 661.2 switches/day, SE=69.60) than Friday ( M=390.7 Win [page break; figure caption omitted] switches/day, SE=28.7), and also that Internet surfing is higher on Monday (M=280.8 switches/day , SE= 42.9) than Friday (M=151.3 switches/day, SE=16.2 )." (a, pp. 7–8)

  > "Logging is done only when a window is moved to the foreground, i.e., if an email client is open, its use will not be logged unless it becomes active. Changing tabs in a browser was counted as separate switches." (b, p. 5)

  > "The average duration per visit for FB is about 18 seconds and for email is about 32 seconds." (b, p. 6)

  > "Participants visited email much more daily: averaging 74 times per day, with a maximum of checking 373 times per day." (b, p. 6)
- **Reader's own computation (locates, is not a value).** 91,409 window switches / 1,509 hours of data collection = 60.6 switches per logged hour (`python3 -c "print(91409/1509)"`); the 1,509 hours are collection hours, not active hours.
- **Coverage.**
  - T1 does not cover.
  - T2 covers: window switches per day (Monday mean 661.2, Friday 390.7; counts include browser tab changes), duration per visit (email about 32 s, Facebook about 18 s); granularity foreground window (and browser tab); 32 information workers; Windows 7.
  - T3 does not cover (tab changes counted as switches but not reported separately). T4, T6, T7, T9 do not cover.
  - T10 covers: email visits 74 per day on average (max 373); Facebook visits 21 per day.
- **Side.** User-side values.

### S1-06 — Hutchings 2004, Display space usage and window management (VibeLog)

- **Citation.** Dugald Ralph Hutchings, Greg Smith, Brian Meyers, Mary Czerwinski, George Robertson. "Display Space Usage and Window Management Operation Comparisons between Single Monitor and Multiple Monitor Users." AVI 2004.
- **Copy read.** https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/avi2004-displayspace.pdf (MSR copy, 8 pp.), accessed 2026-10-01, `sources/S1-06/avi2004-displayspace.pdf`, SHA-256 `26c5ed8a5f42ed45ab5e79b7512e81a6b989de3b5edb1d2c6ae1626486aa0e4d`.
- **One observation.** Yes: VibeLog deployment, 39 volunteers in a research organisation, 3 weeks, 105,402 active minutes, 360,084 activate events.
- **Machine/platform, subject, window named?** Platform named (Windows XP window manager); subject named (39 researchers within computer science; 29 single-, 18 dual-, 2 triple-monitor configurations); calendar window not stated.
- **Verbatim passages.**
  > "Our field study involves users of the Windows XP window manager (hereafter referred to as Windows)" (p. 2, §3)

  > "Thirty-nine volunteers from within a research organization participated in a 3-week study of their computing event activity by [page break] using VibeLog on their work PCs." (pp. 2–3, §4)

  > "We captured 105,402 minutes (just over 73 person-days) of participants' active time." (p. 3, §4)

  > "the log of windows contains a series of entries enumerating the on-screen windows each minute that a user is active." (p. 3, §5)

  > "Analysis of our participants' data revealed that 78.1% of the time people had eight or more windows open, so users may often experience problems with using the taskbar." (p. 4, §6.1)

  > "Participants produced 360,084 activate events, accounting for both the opening of new windows and switching to already opened windows. The average amount of time that any window was active was 20.9 seconds. (This average excludes activation durations of less than 150 milliseconds …). Perhaps more revealing, however, is that the median amount of activation time is 3.77 seconds, i.e., half of all window activation lengths are quite short." (p. 4, §6.2)

  > "the gap between single monitor users, who averaged 3.5 visible windows, and small multimon users, who averaged 4.1 visible windows, is surprisingly small. On the other hand, large multimon users averaged 6.8 visible windows. The median for each group was 3, 4, and 6 visible windows, respectively." (p. 4, §6.3.1)
- **Coverage.**
  - T1 covers: share of active time with ≥ 8 windows open (78.1%); visible windows (mean 3.5 / 4.1 / 6.8, median 3 / 4 / 6 by monitor group); 39 CS researchers; Windows XP; window granularity (not applications).
  - T2 covers: window activation duration (mean 20.9 s, median 3.77 s, all activations incl. new windows, excluding < 150 ms); taskbar vs direct-click switching shares (Table 1).
  - T3, T4, T6, T7, T9, T10 do not cover.
- **Side.** User-side values.

### S1-07 — González 2004, Constant, constant, multi-tasking craziness

- **Citation.** Victor M. González, Gloria Mark. "'Constant, Constant, Multi-tasking Craziness': Managing Multiple Working Spheres." CHI 2004, Vienna.
- **Copy read.** https://www.ics.uci.edu/~gmark/CHI2004.pdf (author's copy, 8 pp.; proceedings pp. 113–120), accessed 2026-10-01, `sources/S1-07/gonzalez-mark-chi2004.pdf`, SHA-256 `988981bfff2408ba2158cf6bcc8bc24c4b1eed9e9cfd3490c69044ea88dcfac4`.
- **One observation.** Yes: shadowing observation of 14 information workers (analysts, developers, managers) at one firm, three days each, 477 hours.
- **Machine/platform, subject, window named?** Platform not named (PCs and financial terminals); subject named; window: "a seven-month period", calendar dates not stated.
- **Verbatim passages.**
  > "People average about three minutes on a task and somewhat more than two minutes using any electronic tool or paper document before switching tasks. … People worked in an average of ten different working spheres. Working spheres are also fragmented; people spend about 12 minutes in a working sphere before they switch to another." (p. 1, abstract)

  > "Fourteen people were observed over a seven-month period. Each person was observed for a period of three and a half days. … the average time of formal observation for each individual was 26 hours." (p. 3, proceedings p. 115)

  > "A total of 477 hours was spent in observation at the field site." (p. 2, proceedings p. 114)

  > "showed that developers spend significantly more time using a PC (mean=4 min. 0 sec., sd=29 sec.) compared with managers (mean=1 min. 58 sec., sd=46 sec.)." (p. 4)

  > "People spend an average of less than two and a half minutes reading email before they switch to another event, or are interrupted." (p. 4)

  > "People spent an average of 2 min. 11 sec. working with any device or paper before they switched to another device or event." (p. 4, proceedings p. 116)

  > "Table 4 shows that the actual average duration of a working sphere segment is quite short (11 min, 28 sec.)." (p. 5)
- **Coverage.**
  - T1 does not cover.
  - T2 covers: continuous time on an event (about 3 min), on the PC before switching (developers 4 min 0 s, managers 1 min 58 s), on any device (2 min 11 s), working-sphere segment 11 min 28 s; granularity event/task and working sphere (not window); method: human shadowing with time-stamped notes; 14 workers.
  - T3, T4, T6, T7, T9 do not cover.
  - T10 covers marginally: continuous email reading under 2.5 min per episode (duration, not rate).
- **Side.** User-side values.

### S1-08 — Smith 2003, GroupBar: the TaskBar evolved

- **Citation.** Greg Smith, Patrick Baudisch, George Robertson, Mary Czerwinski, Brian Meyers, Daniel Robbins, Donna Andrews. "GroupBar: The TaskBar Evolved." OZCHI 2003.
- **Copy read.** https://www.microsoft.com/en-us/research/wp-content/uploads/2003/01/ozchi2003-groupbar.pdf (MSR copy, 10 pp.), accessed 2026-10-01, `sources/S1-08/ozchi2003-groupbar.pdf`, SHA-256 `63c24c32e124a429842e980f39d2a4703bf7ca8283d87b85325ec9e016e87cd5`.
- **One observation.** Two small observations are reported: an informal study (N = 16) and a 5-participant field deployment with self-report baseline; each is one observation; neither is described in detail.
- **Machine/platform, subject, window named?** Platform implied Windows (TaskBar) but not named in the passage; subject "at our corporation" (Microsoft); window not stated.
- **Verbatim passages.**
  > "In an informal study at our corporation, we found that when users shift to larger display surfaces, they leave more applications running and associated windows open. For example, we observed that single display users tend to keep an average or 4 windows open at once, while dual monitor users keep 12 and triple monitor users keep 18 windows open on aver- age (N=16 users). Although a larger study is required for verification of these results" (p. 1)

  > "Before using GroupBar, the participants reported typi- cally running 5.6 applications or programs at once, on average, and that they kept an average of 6.4 windows open at once." (p. 6, §5.2.1)
- **Coverage.**
  - T1 covers: windows open at once (mean 4 / 12 / 18 by monitor count, N = 16, method not described); self-reported applications running at once (5.6) and windows open (6.4), 5 participants.
  - T2, T3, T4, T6, T7, T9, T10 do not cover.
- **Side.** User-side values.

### S1-09 — Yin 2026, FOCAL and DesktopBench

- **Citation.** Haoran Yin, Zhiyuan Wen, Jiannong Cao, Ruosong Yang, Bo Yuan. "FOCAL: Filtered On-device Continuous Activity Logging for Efficient Personal Desktop Summarization." arXiv:2604.19541 (preprint, "Under review").
- **Copy read.** https://arxiv.org/pdf/2604.19541 (version served on 2026-10-01), accessed 2026-10-01, `sources/S1-09/focal-arxiv-2604.19541.pdf`, SHA-256 `fb5742cf5e56f3b911cbaab8926db272314334a051886a1580df31bef2998734`.
- **One observation.** No: DesktopBench is a benchmark assembled by template from VideoGUI task recordings, not a log of anyone's everyday desktop use.
- **Machine/platform, subject, window named?** Not applicable (constructed sessions); no OS named in the passages read; no licence or download location stated in the passages read.
- **Verbatim passages.**
  > "We reconstructVideoGUI[ 14] into DesktopBench, a benchmark for multi-task desktop activity log- ging." (p. 4, §4)

  > "We therefore augment each action with the foreground application name (app) and window title (title), while retaining the original task descriptions as semantic reference (Figure 2). DesktopBench-Multitask (320 sessions).Sessions are assembled through template-based composition grounded in realistic creative workflows. We use 20 patterns spanning video-centric workflows such as video→ref→video and design-centric workflows such as generation→image→slide." (p. 4, §4.1)

  > "an𝐴→𝐵→𝐴 split in which a long-running creative task 𝐴 is interrupted by a short YouTube browsing task𝐵 before resuming." (p. 5, §4.1)

  > "DesktopBench is reconstructed from 2,572 screenshots and uses the sessionas the evaluation unit. It contains 420 sessions in total: 320 in DesktopBench-Multitask and 100 in DesktopBench-Interruption. … The average session length is 17.3 actions for DesktopBench-Multitask and 16.5 for DesktopBench- Interruption." (p. 5, §4.3)
- **Coverage.**
  - T1 does not cover (application combinations are author-chosen templates).
  - T2 does not cover as an observation: the fields exist (foreground application name, window title per action; A → B → A sessions) but sequences and switches are synthetic; no timestamps or dwell times reported.
  - T3, T4, T6, T7, T9, T10 do not cover.
- **Side.** Not applicable (no observation).

### S1-10 — Koldijk 2014, SWELL knowledge work dataset

- **Citation.** Saskia Koldijk, Maya Sappelli, Suzan Verberne, Mark Neerincx, Wessel Kraaij. "The SWELL Knowledge Work Dataset for Stress and User Modeling Research." ICMI 2014, Istanbul, 12–16 November 2014, doi 10.1145/2663204.2663257. Dataset: DANS Data Station Social Sciences and Humanities, doi 10.17026/DANS-X55-69ZP.
- **Copy read.** (1) https://cs.ru.nl/~skoldijk/Papers/ICMI%202014%20paper_final_cr.pdf (camera-ready, 8 pp.), accessed 2026-10-01, `sources/S1-10/koldijk-icmi2014-swell-kw.pdf`, SHA-256 `a10bffe9ea55cb66af6a8e7c2b61fbc5dfeffb3ebef57db8ef0f41cc6c1e5720`. (2) https://cs.ru.nl/~skoldijk/SWELL-KW/Dataset.html, `sources/S1-10/swell-kw-dataset-page.html`, SHA-256 `9f3df722d7d45e019f1815d700a042262d16096b102f4f3af7775f28b7cc2a75`; uLogData.html `a7a07ddd7dde16e522713fc558d47ee900ae81e0312c99bfa8652456941646fa`; FeatureData.html `4bcdf3fad300fec46e3371689de131188634bc3b3b6b15b9a4521d4b82aabbf7`. (3) DANS API record https://ssh.datastations.nl/api/datasets/:persistentId/?persistentId=doi:10.17026/DANS-X55-69ZP (latest version 4, released 2025-06-04T08:57:35Z), `sources/S1-10/dans-x55-69zp-dataset.json`, SHA-256 `fa6e6ee01d0246d4864df69744ca65453b72330acc74f2c272ed3538cbec7c3e`. All accessed 2026-10-01.
- **One observation.** Yes: one laboratory experiment, 25 participants, about 3 hours each, three conditions.
- **Machine/platform, subject, window named?** Machine and platform named (Dell Latitude E6400, Windows 7 Professional, Office 2010, Internet Explorer); subject named (25 students/interns, 8 female, average age 25); window: uLog file names in the DANS record carry dates 2012-09-18 to 2012-11-07 (e.g. `a_pp1_c1_uLog_20120918_131425.xml`, `a_pp25_c3_uLog_20121107_154241.xml`).
- **Verbatim passages.**
  > "The dataset was collected in an experiment, in which 25 people performed typical knowledge work (writing reports, making presentations, reading e-mail, searching for information). We manipulated their working conditions with the stressors: email interruptions and time pressure." (Dataset.html)

  > "The SWELL-KW dataset contains data from 25 participants (~3 hours each), for working under 3 conditions: neutral, interruptions and time pressure (plus a relax phase)." (Dataset.html, Available data)

  > "Stressor 'Interruptions': 8 emails were sent to the par- ticipant during the task." (ICMI paper p. 3, §3.1)

  > "The participants performed knowledge worker tasks on a desktop computer in a controlled lab setting." (p. 3, §3.2)

  > "Participants performed their tasks on a computer (Dell Latitude E6400) with Windows 7 Professional with a 17 inch screen and mouse and keyboard (see Figure 2). Office 2010 was installed, which the participants used for email (Outlook), report writing (Word) and making presentations (Powerpoint). As a browser, Internet Explorer was used" (p. 4, §3.4)

  > "Computer interactions were logged with the key-logging application uLog (version 3.2.5, by Noldus Information Technology), which ran as a background appli- cation on the users' computer." (p. 4, §3.6)

  > "The computer logging software recorded detailed timestamped information in XML format about each computer event. Examples of computer events are mouse clicks, mouse scrolls and application changes." (p. 5, §4.2)

  > "Appli- cations AppChanges TabfocusChange Number of application changes Number of tab focus changes" (p. 5, Table 2, computer interaction features aggregated per minute)

  DANS record (JSON excerpt of `data.latestVersion`, iconUri field omitted): `"license": {"name": "CC-BY-NC-SA-4.0", "uri": "http://creativecommons.org/licenses/by-nc-sa/4.0"}`; files include 75+ uLog XML files (one per participant × condition) and "A - Computer interaction features (Ulog - All Features per minute).xlsx", all `"restricted": false`.
- **Coverage.**
  - T1 does not cover (fixed lab application set).
  - T2 covers (as a dataset): timestamped application changes and tab-focus changes in uLog XML per participant and condition, plus per-minute AppChanges/TabfocusChange features; 25 students in a controlled lab, Windows 7, about 3 hours each, Sept–Nov 2012 (from file names); access DANS SSH Data Station, CC BY-NC-SA 4.0, unrestricted files. Not everyday desktop use. No switching statistic is reported in the paper (S3 computes from the files).
  - T3, T4, T6, T7, T9 do not cover.
  - T10 covers only by design (8 emails sent in the interruption condition; an experimental parameter, not an observed rate).
- **Side.** User-side values (lab).

### S1-11 — Reeves 2019/2021, Screenomics

- **Citation.** Byron Reeves, Nilam Ram, Thomas N. Robinson, James J. Cummings, C. Lee Giles, Jennifer Pan, Agnese Chiatti, MJ Cho, Katie Roehrick, Xiao Yang, Anupriya Gagneja, Miriam Brinberg, Daniel Muise, Yingdan Lu, Mufan Luo, Andrew Fitzgerald, Leo Yeykelis. "Screenomics: A Framework to Capture and Analyze Personal Life Experiences and the Ways that Technology Shapes Them." Human–Computer Interaction 36(2):150–201 (online 2019-03-13; issue 2021), doi 10.1080/07370024.2019.1578652; author manuscript PMC8045984.
- **Copy read.** Wayback snapshot 2025-04-26 20:53:40 GMT of https://pmc.ncbi.nlm.nih.gov/articles/PMC8045984/ (retrieved as https://web.archive.org/web/20250426205340id_/…), author manuscript, accessed 2026-10-01, `sources/S1-11/screenomics-PMC8045984-wayback.html`, SHA-256 `dc13ab3bf4db1806a9e338532444ec4b7fcd618fd652b9448fbceb668940457f`.
- **One observation.** The framework paper reports several example analyses; the switching example is one observation (30 student laptops, analysed in Yeykelis et al. 2018, which this reader could not obtain).
- **Machine/platform, subject, window named?** Platform: "Windows and Mac laptops" (capture software); subject: students; window of the 30-laptop sample not stated in the passage read.
- **Verbatim passages.**
  > "In-house applications take screenshots at periodic intervals (e.g., every five seconds that the device is in use), and store those images in a local folder." (§4.1)

  > "There is a separate application for Windows and Mac laptops, and an application for Android smartphones (iPhones are currently not supported)." (§4)

  > "we applied a proportional hazards model (Cox, 1972) to screenomes from 30 student laptop computers (see Yeykelis et al., 2018).i We identified median task switching time between segments at 20 seconds (e.g., switching from reading an email to conducting a Google search to texting a friend to liking a Facebook post)." (§5.1, Example 1)

  > "As shown in Figure 2 there were substantial differences in median switch-times (a) between individuals (χ2(29, N = 30) = 548, p <.01; top left panel)" (§5.1)

  > "with five-second intervals we are only able to model behaviors manifesting at a ten-second time-scale." (§7)
- **Coverage.**
  - T1 does not cover.
  - T2 covers: median time between content-segment switches 20 s on 30 student laptops (screenshot every 5 s; resolution about 10 s); granularity: content segment (application or site/content), not window focus; per-individual medians differ significantly; platform Windows/Mac.
  - T3, T4, T6, T7, T9, T10 do not cover.
- **Side.** User-side values.

### S1-12 — Mark 2005, No task left behind

- **Citation.** Gloria Mark, Victor M. Gonzalez, Justin Harris. "No Task Left Behind? Examining the Nature of Fragmented Work." CHI 2005, Portland, pp. 321–330.
- **Copy read.** https://www.interruptions.net/literature/Mark-CHI05-p321-mark.pdf (10 pp.), accessed 2026-10-01, `sources/S1-12/Mark-CHI05-p321-mark.pdf`, SHA-256 `61d92cb8ab86c693fce135c167a3da3dfd4417ad3a93d8cc5d1f17771fd911d2`.
- **One observation.** Yes: shadowing of 24 information workers, three days each, over 700 hours. It extends the observation of S1-07 ("We have expanded our observations to include almost double the number of informants", p. 1), so S1-07 and S1-12 likely share informants and are not independent.
- **Machine/platform, subject, window named?** Platform not named; subject named (24 informants at an IT services firm); calendar window not stated.
- **Verbatim passages.**
  > "We present data from detailed observation of 24 information workers that shows that they experience work fragmentation as common practice." (p. 1, abstract)

  > "Twenty-four people in total were observed in detail" … "observations and activity timing were done over the next three days for an average time of 25 hours, 42 minutes per person. Over 700 formal hours of observation were done." (p. 3)

  > "First, we found that 57.1% of all informants' working sphere segments were interrupted, on the average." (p. 4, proceedings p. 324)

  > "The average length of time that the informants spent in central and peripheral working spheres was 11 min. 4 sec., (sd=18 min. 9 sec.) before switching to another working sphere or being interrupted." (p. 4, proceedings p. 324)

  > "When people did resume work on the same day, it took an average length of time of 25 min. 26 sec (sd=54 min. 48 sec.). … our informants worked in an average of 2.26 (sd=2.79) working spheres." (p. 6, proceedings p. 326)
- **Coverage.**
  - T1 does not cover.
  - T2 covers: working-sphere segment length (mean 11 min 4 s), interruption share (57.1%), time to resumption same day (mean 25 min 26 s) with 2.26 intervening spheres (A → B → … → A); granularity: working sphere (project-level task), observed by shadowing; 24 workers.
  - T3, T4, T6, T7, T9, T10 do not cover.
- **Side.** User-side values.

### S1-13 — Tak 2011, Understanding and supporting window switching (PyLogger study)

- **Citation.** Susanne Tak. "Understanding and Supporting Window Switching." PhD thesis, University of Canterbury, 2011, doi 10.26021/2152. The PyLogger study is also reported in Tak, Cockburn, Humm, Ahlström, Gutwin, Scarr, "Improving Window Switching Interfaces," INTERACT 2009 (not read).
- **Copy read.** https://publications.tno.nl/publication/100746/rHFrfg/tak-2011-understanding.pdf (212 pp.), accessed 2026-10-01, `sources/S1-13/tak-2011-understanding-window-switching-thesis.pdf`, SHA-256 `d93a6938e51b9bb358a0f241147ae38c63bd88ccf55e6196d001d71a8a0b4ded`.
- **One observation.** Yes: PyLogger installed for three weeks on the computers of 25 university students or employees.
- **Machine/platform, subject, window named?** Platform named (Windows XP; 7 participants Windows Vista); subject named (25 participants aged 21–61, 9 single-, 9 dual-monitor, 7 mixed); calendar window not stated in the passages read.
- **Verbatim passages.**
  > "a three week log-based longitudi- nal study of window use by 25 participants was conducted using the custom-made tool PyLogger, which recorded actual window switching behaviour." (PDF p. 3, abstract)

  > "Twenty-five people participated, all university students or employees. Age ranged from 21 to 61 years old, with a mean of 31 years old. Reported computer use ranged from 25 to 90 hours per week, with a mean of 49 hours. … Seven participants used Windows Vista, the others used Windows XP." (PDF p. 77, printed p. 53, §5.3)

  > "On average, users had 8.5 windows open (SD=4.6)." (PDF p. 78, printed p. 54, §5.4.1)

  > "On average, single monitor users have 5.9 windows open ( SD=2.4), while dual monitors users have 11.1 windows open ( SD=4.9)." (PDF p. 79, printed p. 55)

  > "single monitor users have 4.2 non-minimised windows on average (SD=1.2), while dual monitors users have 7.2 non-minimised windows ( SD=2.1)." (PDF p. 80, printed p. 56, §5.4.2)

  > "single mon- itor users have 1.7 visible windows on average ( SD=0.2), while dual monitors users have 4.1 visible windows (SD=1.5)." (PDF p. 81, printed p. 57, §5.4.3)

  > "An analysis of how often there is more than one window associated with [page break] an application reveals that 71.1% of open applications have only one window as- sociated with it" (PDF pp. 81–82, printed pp. 57–58, §5.4.4)

  > "Across all users, a window switch takes place 515 times per day, on average. … The analysis reveals a median window activation time of 4.3 seconds" (PDF p. 83, printed p. 59, §5.5.1)

  > "Single monitor users switch between windows 150 times per day ( SD=96), on average, dual monitor users 270 times per day (SD=114) … single monitor user opening a window 134 times per day (SD=96), and dual monitor users 156 times per day ( SD=47). Similarly, single monitor users close a window 136 times per day (SD=95), and dual monitor users 157 times per day (SD=53)" (PDF p. 84, printed p. 60)

  > "In the majority of cases (81%) where the user opened a new window this was a new window for an application that was already active. In the remaining minority of cases a new application was launched." (PDF p. 90, printed p. 66)

  > "On average, 57% of switches ( SD=9%) is to the most recently used window. Across participants this percentage ranges from 41% to 76%" (PDF p. 103, printed p. 79, §5.8.1)

  > "the results show that 80% of switches is to 2 to 11 applica- tions, with a cross participant mean of 6 applications. Analysis of the most revisited application per participant reveals that these are a browser (12 participants), e-mail client (4), IDE (3), file explorer (2), doc- ument editor (2), file sharing application (1), and a graphics editor (1)." (PDF p. 104, printed p. 80, §5.8.2)
- **Reader's own computation (locates, is not a value).** Application launches per day ≈ 19% (= 100% − 81%) of windows opened per day: 0.19 × 134 = 25.5 (single monitor) and 0.19 × 156 = 29.6 (dual monitor) (`python3 -c "print(134*0.19,156*0.19)"`); assumes the 81/19 split applies uniformly to both groups.
- **Coverage.**
  - T1 covers: windows open at once (mean 8.5, SD 4.6; 5.9 single, 11.1 dual), non-minimised (4.2 / 7.2), visible (1.7 / 4.1), windows per application (71.1% of open applications have one window), 80% of switches go to 2–11 applications (mean 6); 25 participants; Windows XP/Vista.
  - T2 covers: window switches per day (515 all types; 150 / 270 between open windows), median activation 4.3 s, return to most recently used window 57% of switches (range 41–76%), 55% of windows never revisited; granularity window; logging method PyLogger (Windows API hooks).
  - T3 does not cover. T4, T6, T7 do not cover.
  - T9 covers partially: 19% of window openings are launches of a new application (share only; daily count only by the reader's own computation above).
  - T10 does not cover.
- **Side.** User-side values.

### S1-14 — Czerwinski 2004, A diary study of task switching and interruptions

- **Citation.** Mary Czerwinski, Eric Horvitz, Susan Wilhite. "A Diary Study of Task Switching and Interruptions." CHI 2004, pp. 175–182.
- **Copy read.** https://www.interruptions.net/literature/Czerwinski-CHI04-p175-czerwinski.pdf (8 pp.), accessed 2026-10-01, `sources/S1-14/Czerwinski-CHI04-p175-czerwinski.pdf`, SHA-256 `42aebba4b2371961baa48a0ae825d95b186f1ed982cf9162d8b2af198e00b5da`.
- **One observation.** Yes: one week-long self-report diary study, 11 experienced Windows users (10 analysed).
- **Machine/platform, subject, window named?** Platform: "Microsoft Windows users" (self-report, not logged); subject named (stock broker, professor, web designer, developer, boat salesman, network administrator); calendar window not stated.
- **Verbatim passages.**
  > "Eleven experienced Microsoft Windows™ users (3 female) participated in the study." (p. 2, proceedings p. 176)

  > "We found that 23% of the tasks reported could best be described as “email.”" (p. 4)

  > "Reported task lengths averaged 53 minutes, with a large standard deviation of 90.9 minutes. The distribution of task lengths was highly negatively skewed, with the majority of the tasks reported being shorter than the average length." (p. 4)

  > "We found that the largest category of task switches (40%) were self initiated" (p. 4)

  > "The returned-to tasks were over twice as long as those tasks described as more routine, shorter-term projects (average task length = 120 minutes v. 45 minutes, respectively)" (p. 5)
- **Coverage.**
  - T1 does not cover.
  - T2 covers: self-reported task length (mean 53 min, SD 90.9; returned-to tasks 120 min vs 45 min), task-switch causes (40% self-initiated); granularity task (self-defined); diary, not logged; 10 analysed users.
  - T3, T4, T6, T7, T9 do not cover.
  - T10 covers marginally: email is 23% of reported tasks (share, not a rate).
- **Side.** User-side values (self-report).

### S1-15 — Cao 2021, Large-scale analysis of multitasking behavior during remote meetings

- **Citation.** Hancheng Cao, Chia-Jung Lee, Shamsi Iqbal, Mary Czerwinski, Priscilla Wong, Sean Rintel, Brent Hecht, Jaime Teevan, Longqi Yang. "Large Scale Analysis of Multitasking Behavior During Remote Meetings." CHI 2021; preprint arXiv:2101.11865.
- **Copy read.** https://arxiv.org/pdf/2101.11865 (v1 as served 2026-10-01), accessed 2026-10-01, `sources/S1-15/cao-remote-meetings-arxiv-2101.11865.pdf`, SHA-256 `48b9694b1064bb8e12cea4526317515fb3f933568f80c92f6a11e90f410ad02f`.
- **One observation.** Yes for the telemetry part (one telemetry extraction: four one-week snapshots, Feb–May 2020, US Microsoft employees); the 715-person diary study is a second observation in the same paper.
- **Machine/platform, subject, window named?** Platform: Microsoft Teams, Outlook, OneDrive/SharePoint (client OS not named); subject named (US Microsoft employees); window named (24–28 Feb, 23–27 Mar, 20–24 Apr, 18–22 May 2020).
- **Verbatim passages.**
  > "through an analysis of a large-scale telemetry dataset collected from February to May 2020 of U.S. Microsoft employees and a 715-person diary study." (p. 1, abstract)

  > "We collected metadata (without any content information) on remote meetings (Microsoft Teams), email usage (Microsoft Outlook), and file edits (Onedrive/Sharepoint) of US em- ployees from Microsoft." … "1) February 24-28, which represents a period of pre-COVID, mostly co-located work, 2) March 23-27, … and 3) April 20-24 and 4) May 18-22, to represent fully re- mote work periods." (p. 3, §3.1)

  > "on Microsoft Outlook, we collected the time when people actively send, respond to, or forward an email." (p. 4)

  > "from February to May, we find that 31.1%, 30.9%, 29.2%, and 28.9% meetings involve email multitasking, and 23.7%, 23.1%, 24.8%, and 25.5% meetings involve file multitasking." (p. 5)
- **Coverage.**
  - T1 covers: co-occurrence of a video meeting (Teams) with email sending (about 29–31% of meetings) and with file editing (about 23–26%); population: US Microsoft employees; Feb–May 2020; meeting-level share, not simultaneous application counts.
  - T2 does not cover.
  - T3, T4, T6, T7, T9 do not cover.
  - T10 covers partially: share of meetings with at least one email send/respond/forward; the paper does not give emails per hour in the passages read.
- **Side.** User-side values.

### S1-16 — Xu 2010, Contribution à l'étude et au développement de techniques de gestion de fenêtres (WindowsOSLog study)

- **Citation.** Xu Quan. "Contribution à l'étude et au développement de techniques de gestion de fenêtres." Doctoral thesis, Université Lille 1, defended 15 December 2010 (written in English).
- **Copy read.** https://pepite-depot.univ-lille.fr/LIBRE/EDSPI/2010/50376-2010-Xu.pdf (192 pp.), accessed 2026-10-01, `sources/S1-16/50376-2010-Xu.pdf`, SHA-256 `d3030df48a02f6efb8f7708c9316cfd77658df17f00c4395d294f8ab55419260`.
- **One observation.** Yes: WindowsOSLog deployment, 26 participants, over 5 weeks (eight over 10 weeks).
- **Machine/platform, subject, window named?** Platform named (Windows XP 22, Vista 2, Windows 7 2; resolutions given); subject named (26 participants, mean age 27; 18 computer science, 8 other students); calendar window not stated.
- **Verbatim passages.**
  > "26 participants participated in this study with a mean age of 27 (SD = 2.4), 18 par- ticipants (Group1) are from within the computer science department … All participants are Windows [page break] Operating System users, including Windows XP (22), Vista (2), Window 7 (2)." (PDF pp. 63–64, printed pp. 42–43)

  > "The study duration is over 5-weeks (eight of them is over 10-weeks)." (PDF p. 64)

  > "the mean number of windows opened was 7 for single monitor user and 10 for dual monitors user." (PDF p. 70, printed p. 49)

  > "Table 3.5: Users opened more windows on dual monitor system than on the single monitor system (s.d. = standard deviation). Display Mean Median s.d. Min Max Single monitor 6.8 5.9 0.01 0 31 Dual monitors 10.3 11 0.02 0 24" (PDF p. 70, Table 3.5)

  > "Figure 3.3 shows that window activation activity happens more frequently than win- dow creation and destruction under both single monitor and dual monitors conditions" (PDF p. 71)
- **Coverage.**
  - T1 covers: windows open on the desktop (single monitor mean 6.8, median 5.9, max 31; dual mean 10.3, median 11, max 24); 26 participants; Windows XP/Vista/7. The reported "s.d." values (0.01–0.12) look inconsistent with the ranges; quoted as printed.
  - T2 covers only qualitatively (activation more frequent than creation/destruction; no rate in the passages read).
  - T3, T4, T6, T7, T9, T10 do not cover.
- **Side.** User-side values.

### S1-17 — Mark 2012, A pace not dictated by electrons (work without email)

- **Citation.** Gloria J. Mark, Stephen Voida, Armand V. Cardello. "'A Pace Not Dictated by Electrons': An Empirical Study of Work Without Email." CHI 2012.
- **Copy read.** https://ics.uci.edu/~gmark/Home_page/Publications_files/CHI%202012.pdf (author's copy, 10 pp.), accessed 2026-10-01, `sources/S1-17/mark-chi12-without-email.pdf`, SHA-256 `eae94e81c9115707f79c705712ea023a563e14ff79c2508c4d65591f6ed3a7ed`.
- **One observation.** Yes: 13 information workers at one US research organisation, 8-day within-subject study (baseline then email cut-off), over 25,000 window data points.
- **Machine/platform, subject, window named?** Platform not named in the passages read ("custom window activity logging application"); subject named (13 participants: chemical engineer, materials scientist, psychologist, biologist, food technologist, research administrator; mean age 46); calendar window not stated.
- **Verbatim passages.**
  > "A total of 13 participants volunteered for the study (6 females, 7 males, mean age = 46)." (p. 2)

  > "Table 2 shows, for each participant, the means and standard deviations of the durations (in seconds) that application and document windows were left open, as well as the frequency of window switches (in switches per hour) during each hour that our sensors collected data. We counted all window switches, including when auxiliary windows were invoked (e.g., reading a PDF attachmen t from a past email). Seven extreme outliers were removed from our set of over 25,000 data points." (p. 4)

  > "Baseline No Email Duration Frequency Duration Frequency P M SD M SD M SD M SD … M 75.5 394.3 37.1 31.4 131.9 568.1 18.2 23.5 Table 2. Mean and SD of window duration (in seconds) and frequency of window switches (switches/hour in which data were collected) for each participant." (p. 5, Table 2; per-participant rows 1–13 also given, baseline switches/hour from 17.5 to 53.9)
- **Coverage.**
  - T1 does not cover.
  - T2 covers: window dwell (baseline mean 75.5 s, SD 394.3) and switches per hour (baseline mean 37.1, SD 31.4; no-email condition 18.2), per participant (Table 2); granularity window; 13 information workers.
  - T3, T4, T6, T7, T9 do not cover.
  - T10 does not cover (email removed as treatment; no rate of sending reported in the passages read).
- **Side.** User-side values.

### S1-18 — Judd 2015, Task selection, task switching and multitasking during computer-based independent study

- **Citation.** Terry Judd. "Task selection, task switching and multitasking during computer-based independent study." Australasian Journal of Educational Technology 31(2), 2015, pp. 193–207, doi 10.14742/ajet.1992.
- **Copy read.** https://ajet.org.au/index.php/AJET/article/download/1992/1264 (published PDF, 15 pp.), accessed 2026-10-01, `sources/S1-18/judd-ajet-2015.pdf`, SHA-256 `e5d8f095eb0968df8c6a64655e5f478af987ba6201ab8947a2e014c009e41c35`.
- **One observation.** Yes: automated logging in one open-access computer laboratory, August–September 2009, 3,349 sessions by 1,230 users.
- **Machine/platform, subject, window named?** Machine/platform: about 50 lab workstations; the task names (Finder, Preview) indicate macOS but the OS is not named in the passages read; subject named (medical and biomedical students); window named (August–September 2009).
- **Verbatim passages.**
  > "Data collection for this study took place at a large Australian metropolitan university during August and September in 2009. Automated logs of students' computer-based activities were captured within an open - access computer laboratory containing approximately 50 computer workstations" (p. 2, printed p. 194)

  > "Task names were derived from the active application, in the case of non -browser tasks, or the Internet domain in the case of in -browser tasks. Task records were generated each time users opened a new application or website or switched to or reactivated an existing application or website. Data analysis was restricted to sessions of between 20 minutes and 2 hours in length." (p. 3, printed p. 195)

  > "A total of 3349 sessions contributed by 1230 unique users were analysed. The combined sessions contained 13350, 20 minute segments comprised of 87666 task instances. The mean and median task durations were 126.8 seconds and 31 seconds respectively (Table 2)." (p. 5, printed p. 197)

  > "Application tasks were the next most common (22.8% of all task instances ), with two helper applications – (Preview – 5.9% of all task instances; Word – 5.7% of all task instances), and the operating system 's file management application (Finder – 5.9% of all task instances)" (p. 5)
- **Coverage.**
  - T1 does not cover (sequence of foreground tasks, not concurrently open set).
  - T2 covers: task (foreground application or web domain) duration mean 126.8 s, median 31 s; 87,666 task instances; segment classification (focused / sequential / multitasking with returns); 1,230 students; lab; 2009.
  - T3 does not cover (domains, not tabs). T4, T6, T7, T9, T10 do not cover.
- **Side.** User-side values.

### S1-19 — Dodier-Lazaro 2020, Appropriate security and confinement technologies (Xubuntu field study)

- **Citation.** Steve Dodier-Lazaro. "Appropriate security and confinement technologies: methods for the design of appropriate security and a case study on confinement technologies for desktop computers." PhD thesis, University College London, 2020-02-28 (UCL Discovery eprint 10046583).
- **Copy read.** https://discovery.ucl.ac.uk/id/eprint/10046583/1/Dodier-Lazaro_Thesis.pdf, accessed 2026-10-01, `sources/S1-19/Dodier-Lazaro_Thesis.pdf`, SHA-256 `4db5b72207f8a9bba46d0d85d2e62e3b3e0da4e64b6417e2061577c4b37e1fc3`.
- **One observation.** Yes: one field deployment on 13 Xubuntu users' own computers (data collection average 23 days; chapter 8 says three weeks).
- **Machine/platform, subject, window named?** Platform named (Xubuntu 15.10 and 16.04, Xfce; Zeitgeist and an LD_PRELOAD system-call logger); subject named (13 Xubuntu users from 8 countries, aged 18–54, recruited via Reddit); calendar window not stated in the passages read.
- **Verbatim passages.**
  > "I recruited 13 Xubuntu users from a pool of 40-50. The participants come from 8 coun- tries, are aged between 18 and 54" (PDF p. 155, printed p. 141, §5.3.2)

  > "My participants include a Web developer, two adult high school students, two tech support representatives, a musician, a consumer retail employee, a student teacher, a sales engineer and four computer science students. … Eight of them write code regularly, seven perform information work, and seven produce media content (e.g. graphics, audio, video, scores, photos)." (PDF p. 156, printed p. 142)

  > "The study started with participants installing data collection software on their systems, which I had them run for an average of 23 days (min: 15; max: 38)." (PDF p. 156, printed p. 142, §5.4.1)

  > "The second tool was aLD_PRELOAD library5 injected into all apps of the participants' Desktop session, which logged all system calls related to files" (PDF p. 157, printed p. 143)

  > "All the study software on participants' computers was made compatible with Xubuntu 15.10 and Xubuntu 16.04 OSs, and were tested for those platforms." (PDF p. 164, printed p. 150)

  > "I monitored the activity of all applications run on my participants' personal computers for three weeks." (PDF p. 216, printed p. 202, §8.3)

  > "I excluded Chromium from this analysis, as Chromium's sandbox is not compatible with dynamic library loading" … "a median number of 37.24% of each participant's processess succeeded in saving log data." (PDF pp. 217–218, printed pp. 203–204)

  > "Combining both data sources, I collected a median 276171 events per participant con- cerning a median 12006 files, of which 1141 were user documents; and 9978 application instances (grouped in 85 applications), of which 772 were user application instances (grouped in 24 applications). Variability across participants was high. User documents collected varied between 22 and 25710; Applications from 8 to 51." (PDF p. 218, printed p. 204, §8.3.3)
- **Reader's own computation (locates, is not a value).** 772 user application instances per participant (median) over 21–23 days ≈ 34–37 per day (`python3 -c "print(772/21, 772/23)"`); the per-day denominator mixes active and inactive days and the instance count undercounts Chromium and processes that did not save logs.
- **Coverage.**
  - T1 covers: on Linux (Xubuntu, Xfce), per participant median 85 distinct applications and 9,978 application instances over about three weeks, of which 24 applications / 772 instances are user applications — the rest (about 92% of instances) are non-user programs (helpers, daemons, utilities); range 8–51 applications; 13 users; Xubuntu 15.10/16.04 era. No simultaneous-open count.
  - T2 does not cover.
  - T3 covers marginally: Chromium excluded because its sandbox blocks LD_PRELOAD (no tab or renderer counts).
  - T4, T6, T7 do not cover.
  - T9 covers partially: user application instances (launch count proxy, median 772 per participant over the study).
  - T10 does not cover.
- **Side.** Both: application instance counts are what the user (and the session) started — user-side; the non-user instance population is a program-side observation, and it is a Linux observation.

### S1-20 — Meyer 2014, Software developers' perceptions of productivity

- **Citation.** André N. Meyer, Thomas Fritz, Gail C. Murphy, Thomas Zimmermann. "Software Developers' Perceptions of Productivity." FSE 2014.
- **Copy read.** https://thomas-zimmermann.com/publications/files/meyer-fse-2014.pdf (authors' copy, 11 pp.), accessed 2026-10-01, `sources/S1-20/meyer-fse-2014.pdf`, SHA-256 `949c0f8986495585b1a4b72c423c9479897540dd1b07b8adfbb0b30ab6e5fce3`.
- **One observation.** Yes for the observational part: 11 professional developers at 3 companies, 4 hours each, 2,650 log entries (the survey of 379 is a separate observation, not used here).
- **Machine/platform, subject, window named?** Platform not named; subject named; calendar window not stated.
- **Verbatim passages.**
  > "The observational study we conducted involved observing 11 professional software developers from three companies at work for four hours each. As the developers worked, we col- lected detailed logs of the tasks worked on and the programs used to perform work, gathering a total of 2650 log entries." (p. 2)

  > "The number of task switches we observed, 13.3 (±8.5) per hour on average, is similar to other reports in the literature [20, 29]. The number of activity switches is larger than reported in previous studies at 47 ( ±19.8) times per hour on average." (p. 2)

  > "During the sessions, participants switched activities 47.0 (±19.8) times per hour, spending on average 1.6 (±0.8) min- utes on an activity before switching." (p. 7, Theme 2: Activities)
- **Coverage.**
  - T1 does not cover.
  - T2 covers: task switches 13.3 (SD 8.5) per hour, activity switches 47 (SD 19.8) per hour, about 1.6 min per activity; granularity task and activity (observer-coded, including the program used); 11 developers; human observation with logs.
  - T3, T4, T6, T7, T9, T10 do not cover.
- **Side.** User-side values.

### S1-21 — Jones 2012, Laptop energy-saving opportunities based on user behaviors

- **Citation.** Morris E. Jones Jr., Belle W. Y. Wei, Donald L. Hung. "Laptop energy-saving opportunities based on user behaviors." Energy Efficiency 6:425–431 (2013; published online 2012-08-14), doi 10.1007/s12053-012-9167-5 (open access).
- **Copy read.** Wayback snapshot 2022-01-27 10:58:49 of https://link.springer.com/content/pdf/10.1007/s12053-012-9167-5.pdf (published PDF), accessed 2026-10-01, `sources/S1-21/jones-2012-laptop-energy-user-behaviors.pdf`, SHA-256 `c0d9dd2a34a6d04e22e33f027f70d9d637ea7fce6ff0320666f812b0dc327c1b`.
- **One observation.** Yes: 13 college students' laptops, 1 month, about 2,260 hours of samples, about one million sample points.
- **Machine/platform, subject, window named?** Platform named (monitor for Windows 7, Vista, XP); subject named (13 college students, "ABC University"); calendar window not stated (received August 2011).
- **Verbatim passages.**
  > "a pilot study was undertaken to develop and test software tools and methods for monitoring the laptop computer usage of 13 college students for a period of 1 month." (p. 1, abstract)

  > "a software monitor tool written in C++ was developed for Windows 7, Windows Vista, and Windows XP . It runs in the background of the user's laptop without user interface. … The data collection period is thus between 7 and 10 s." (p. 2, printed p. 426)

  > "In addition, information on visible processes, pro- cesses that are visible by the monitor tool, and their related resource consumption was collected. This includes process creation time, execution time, disk read/write rates, system resources used, and the names of all .exe and .dll files loaded." (p. 2)

  > "Data were collected for each laptop for, on average, 170 h in total and about 6 h each day." (p. 3)

  > "During idle periods longer than 5 min, the top resource- consuming processes were mostly browsers, virus scanners, and the windows display manager." (p. 4)

  > "Figure5 shows the sample counts for the top nine user-visible processes (out of 832 different ap- plication processes), which account for nearly 80 % of the total process samples. Each sample had, on average, ten user-visible processes." … "only four out of nine top visible processes are user-controllable applica- tions, which are browser applications." (p. 5, printed p. 429)

  > "The maximum number of open browser applications was 11, the average 1.9, and the median 4. As for active browser applications, 50 % of all samples had a single active browser application; 23 % had two or more active brows ers applications; about 2 % had five or more active browser applications." (p. 6; average and median as printed)
- **Coverage.**
  - T1 covers: user-visible processes per sample (mean about 10), 832 distinct application processes, top processes (display manager, user shell, three browsers, a browser helper, touch-pad driver, dynamic-linking support), background consumers during idle (browsers, virus scanners, display manager), open browser applications (max 11); 13 students; Windows laptops; c. 2011.
  - T2 does not cover.
  - T3 covers marginally: open/active browser applications (processes) per sample; not tabs.
  - T4, T6, T7, T9, T10 do not cover.
- **Side.** User-side for which applications are open; the process population is program-side and on Windows, so context only for program-side use.

### S1-22 — Jones 2006, "Why userspace sucks" (Fedora Core 5 boot, login and idle-desktop profiling)

- **Citation:** Dave Jones. "Why Userspace Sucks—Or 101 Really Dumb Things Your App Shouldn't Do." *Proceedings of the Linux Symposium (OLS 2006)*, Volume One, pp. 441–450, Ottawa, 2006.
- **Copy read:** https://www.kernel.org/doc/ols/2006/ols2006v1-pages-441-450.pdf (kernel.org copy of the proceedings pages; HTTP 200), accessed 2026-10-01; `sources/S1-22/ols2006v1-pages-441-450.pdf`; SHA-256 `6f3f2cd7b7acba6e4b605f17ad6c6cee1dbbd1da7554999affaeacd902ac2e43`. Page numbers below are the PDF's pages 1–12 (printed pages 441–450 shown in brackets where read).
- **One observation:** several observations by one author on his development machines during Fedora Core 5 development (2006): a kernel patch logging every open/stat/exec during the first five minutes of uptime (boot and login), the same patch on an idle desktop, a font-stress rerun, and a timer listing on an idle Athlon XP laptop.
- **Machine/platform, subject, window named:** platform named (Fedora Core 5 development, GNOME desktop; one machine an Athlon XP laptop; kernel version not stated); subjects named by program (HAL daemon, CUPS, Xorg, xfs, gdm/gnome-session, irqbalance, gamin, nautilus, gnome-terminal, metacity, wnck-applet, mixer_applet2, hpssd.py …), versions not given; windows: first five minutes of uptime; timer-listing interval not stated.
- **Verbatim passages:**
  > "the file list was created using a kernel patch that simply printk'd the filename of every file open()'d during the first five minutes of uptime." (p. 2 [442], §2)

  > "During boot-up, 79576 files were stat()'d. 26769 were open()'d, 1382 commands were exec'd. • During shutdown, 23246 files were stat()'d, 8724 files were open()'d." (p. 2 [442], §2)

  > "HAL Daemon. … Accounted for a total of 1918 open()'s, and 7106 stat()'s. • CUPS … Responsible for around 2500 stat()'s, and around 500 open()'s." (pp. 2–3 [442–443], §2.1)

  > "Going further, removing the "first 5 minutes" check of the patch allowed me to profile what was going on at an otherwise idle desktop. • irqbalance. – Wakes up every 10 seconds to rebalance interrupts in a round-robin manner." (p. 3 [443], §2.2)

  > "gamin – Was stat()'ing a bunch of gnome menu files every few seconds for no apparent reason." (p. 3 [443], §2.2)

  > "nautilus – Was stat'ing $HOME/Templates, /usr/share/applications, and $HOME/.local/share/applications every few seconds even though they had not changed." (p. 4 [444], §2.2)

  > "gnome-terminal was another oddball. It open()'ed 764 fonts and stat()'d another 770 including re-stat()'ing many of them multiple times. … strace -c shows that gnome-terminal spends a not-insignificant amount of its startup time, stat()'ing a bunch of fonts that it never uses." (p. 4 [444], §2.3, after copying 6,000 TTF fonts to $HOME/.fonts)

  > "peer_check_expire 181 crond / dst_run_gc 194 syslogd / rt_check_expire 251 auditd / process_timeout 334 hald / it_real_fn 410 automount / process_timeout 437 kjournald … it_real_fn 1564 rpc.idmapd … process_timeout 1652 sendmail … process_timeout 2218 hald-addon-stor / process_timeout 3492 cpuspeed … it_real_fn 7965 Xorg / process_timeout 13269 gdmgreeter / process_timeout 15607 python" (p. 8 [448], Figure 3 "/proc/timertop"; counts per timer function and process, interval not stated)

  > "The python process that kept waking up belonged to hpssd.py, a part of hplip. As I do not have a printer, … this was completely unnecessary." (pp. 8–9 [448–449]; the sentence crosses the page break)
- **Coverage:**
  - T1: covers (program-side, Linux) — what runs unseen on an idle 2006 GNOME desktop and how often it wakes: named daemons and session programs (crond, syslogd, auditd, hald, automount, rpc.idmapd, sendmail, cpuspeed, Xorg, gdmgreeter, hpssd.py, irqbalance every 10 s, gamin and nautilus polling every few seconds), Figure 3 timer counts; one machine, Fedora Core 5 era. Not a user-population observation of which applications are open.
  - T9: covers (program-side, Linux) — start-up work: boot-to-login file I/O (79,576 stat, 26,769 open, 1,382 exec in the first five minutes), per-daemon start-up I/O (HAL, CUPS, Xorg), gnome-terminal start-up stat/open of fonts; no durations per application.
  - T2, T3, T4, T6, T7, T10: do not cover.
- **Side:** program-side observation on Linux (candidate); dated (2006, Fedora Core 5).

### S1-30 — Dubroy 2010, tabbed browsing among Firefox users

- **Citation.** Patrick Dubroy and Ravin Balakrishnan. 2010. A Study of Tabbed Browsing Among Mozilla Firefox Users. In *Proceedings of CHI 2010*, Atlanta, GA, USA, April 10–15, 2010, pp. 673–682. ACM.
- **Copy read.** https://www.dgp.toronto.edu/public_user/ravin/papers/chi2010_tabbedbrowsing.pdf (author-hosted camera-ready, footer "CHI 2010: Browsing … 673"), accessed 2026-10-01, `sources/S1-30/chi2010_tabbedbrowsing.pdf`, SHA-256 `8f1189484d86152d99ad64d67a96be9139bd33d510a86eb353148264040a33a3`.
- **One observation.** Yes — one client-side logging study (Firefox extension click-stream logs plus diaries and interviews) of 21 participants.
- **Machine/platform, subject, window named?** Platform: Firefox 1.5–3.0 extension; OS only described as "Most of our participants used Microsoft Windows". Subject: 21 participants recruited as people who "often use multiple tabs or windows" (selection toward tab users). Window: 13–21 days per participant; calendar period not stated.
- **Verbatim passages.**
  > "The detailed web browsing usage of 21 participants was logged over a period of 13 to 21 days each, and was supplemented by qualitative data from diary entries and interviews." (Abstract, PDF p.1, p.673)

  > "21 people (13 female, 8 male; 15 aged 18-29, 4 in their 30s, and 2 in their 50s) were recruited via email through the extended network of the researchers, and by posters on bulletin boards around campus. The study was advertised as “a research study exploring how people use web browsers”, looking for participants who “use Mozilla Firefox for several hours a day, and often use multiple tabs or windows.”" (Methodology › Participants, PDF p.3, p.675)

  > "Click-stream data was collected using a custom extension for Firefox that was compatible with Firefox versions 1.5 through 3.0 so that it could be installed without upgrading or significantly changing the user's browsing environment." (Instruments and Data Collection, PDF p.3, p.675)

  > "Number of concurrent tabs and windows. We measured the number of windows and tabs that were open when a navigation event occurred, as in Weinreich et al. [18]. For simplicity, we ignored all navigation events caused by Firefox's session restore feature in calculating this measure." (Analysis Methods, PDF p.4–5, pp.676–677)

  > "Figure 3 shows the number of tabs open when a navigation action occurred. The most common number of tabs to have open is one, with a steady descent down to 9. There is a second peak at 16 tabs, but this was almost entirely due to just two of the participants, P14 and P20." (Characterizing Tab Usage, PDF p.6, p.678)

  > "Participant 14 had by far the highest median number of tabs open with 17, while no other participant had a median higher than 6. Participant 20 had the highest number of tabs open at once, with 42." (PDF p.6, p.678)

  > "P19 is interesting—he had a median of only one tab open, but a max of 27. Participant 2 is similar, but not nearly as extreme: a median of 4 and a max of 20." (PDF p.6, p.678)

  > "Over half our participants (13/21) are clustered around the 0.04 mark. In other words, these people created about 4 tabs for every 100 navigation actions." (Characterizing Tab Usage, PDF p.5, p.677)

  > "Across all of our participants, we found that 45% of tabs were selected exactly once. As we saw in Figure 3, the largest portion of navigation events during the study happened with only one tab open, and Figure 6 showed that 7 participants had a median of only one or two tabs open." (Measuring Tab Revisitation, PDF p.8, p.680)
- **Coverage.**
  - T3 — covers: object = browser tabs (and windows) open at each navigation event; unit = count of open tabs; statistic = distribution over navigation events (Fig. 3, values only described in text) and per-participant median and maximum (Fig. 4; text gives medians ≤ 6 except one participant at 17, maxima 20, 27, 42 for named participants); also tab-creation rate per navigation action; scope = Firefox only; population = 21 self-selected active tab users, mostly on Windows; period not stated (Firefox 1.5–3.0 era). Visible-at-once windows: not covered.
  - T10 — partial: navigation actions are the denominator of rates but no per-hour or per-session page-load rate is reported in the text.
  - T2 — partial: tab-switch rate (switches per navigation action, Fig. 5, no numbers in text); browser-internal focus, not application focus.
  - T1, T4, T6, T7, T9 — does not cover.
- **Side.** User-side (any platform).

### S1-31 — Reis 2019, Site Isolation in Chrome (field telemetry and microbenchmarks)

- **Citation.** Charles Reis, Alexander Moshchuk, Nasko Oskov. 2019. Site Isolation: Process Separation for Web Sites within the Browser. In *28th USENIX Security Symposium*, Santa Clara, CA, August 14–16, 2019, pp. 1661–1678.
- **Copy read.** https://www.usenix.org/system/files/sec19-reis.pdf (USENIX open-access proceedings PDF with cover page; PDF p.2 = p.1661), accessed 2026-10-01, `sources/S1-31/sec19-reis.pdf`, SHA-256 `fc5e13705338c66f219b9aa1385a51a6d9f743fa7e66ef55b48794502e1be6a0`.
- **One observation.** Two observations in one paper: (a) field telemetry from Chrome 69 on Windows, two weeks from 2018-10-01, equal-sized test and control groups; (b) a microbenchmark on one Windows 10 desktop. Plus design description (existence-only).
- **Machine/platform, subject, window named?** (a) platform Windows, Chrome 69, desktop and laptop users with metrics reporting enabled, window 2 weeks from 2018-10-01, population size not given. (b) Windows 10, Intel Core i7-8700K, 16 GB RAM, Chrome 69.0.3497.100, clean profile, single tab. No Linux observation.
- **Verbatim passages.**
  > "For example, a web page with four cross-site iframes, all on different sites, will re- quire ﬁve renderer processes versus one in the old architec- ture." (§4.1, PDF p.8, p.1667)

  > "Instead, we use process consolidation for same-site main frames only after crossing a soft process limit that approximates memory pressure. When the number of processes is below this limit, main frames in independent tabs don’t share processes; when above the limit, all new frames start reusing same-site processes when possible. Our threshold is calculated based on performance characteristics of a given machine. Note that Site Isolation cannot support a hard process limit, because the number of sites present in the browser may always exceed it." (§4.1.1 Process Consolidation, PDF p.8, p.1667)

  > "To address this, we maintain a warmed-up spare renderer process, which may be used immediately by a new navigation to any site. When a spare process is locked to a site and used, a new one is created in the background, similar to process pre-creation optimizations in OP2 [23]. To control memory overhead, we avoid spare processes on low memory devices, when the system experiences memory pressure, or when the browser goes over the soft process limit." (§4.1.3, PDF p.8, p.1667)

  > "The data in this section was collected using pseudonymous met- ric reporting over a two-week period starting October 1, 2018, from desktop and laptop users of Chrome (version 69) on Windows who have this reporting enabled." (§5.3.1 Observed Workload, PDF p.11, p.1670)

  > "Using periodic samples, we found that users had 6.0 unique sites open across the entire browser at the 50th per- centile of the distribution, and 41.9 unique sites at the 99th percentile. This only provides a lower bound for the num- ber of renderer processes; each instance of a site might live in a separate process. If this were the case, our metrics give an upper bound estimate of 79.7 processes at the 99th per- centile." (§5.3.1 Process Count, PDF p.11, p.1670)

  > "At the 50th percentile, the number of processes increased 43.5% from 4.4 without Site Isolation to 6.2 with Site Isolation. At the 99th percentile, the process count increased 50.6% from 35.0 to 52.7 processes." (§5.3.1, PDF p.11, p.1670)

  > "We conﬁrmed that this is not due to a change in workload size: there were no statistically signiﬁcant differ- ences in page load count, and we saw at most a 1.5% de- crease in the number of open tabs (at the 99th percentile)." (§5.3.1 Memory Overhead, PDF p.12, p.1671)

  > "Site Isolation signiﬁcantly increased the percentage of navigations that cross a process boundary, from 5.73% to 56.0%." (§5.3.1 Latency, PDF p.12, p.1671)

  > "Our experiments were performed on a Windows 10 desktop with an Intel Core i7-8700K 3.7 GHz 6-core CPU and 16 GB RAM." (§5.3.2 Microbenchmarks, PDF p.13, p.1672)

  > "As expected, the relative memory overhead gen- erally increases with the number of processes, peaking at 89% for wowprogress.com with 10 processes. … For example, a heavier amazon.com site has a 5% overhead com- pared to seatguru.com’s 31%, even though both require ﬁve processes. google.com does not have any cross-site iframes and requires no extra processes" (§5.3.2, PDF p.13, p.1672)

  > "This underscores the limi- tations of microbenchmarks: users tend to have multiple tabs (four at 50th percentile) and a variety of open URLs." (§5.3.2, PDF p.13, p.1672)
- **Coverage.**
  - T3 — covers (user side): object = unique sites open across the browser and open tabs; unit = count per periodic sample; statistic = 50th percentile 6.0 sites, 99th percentile 41.9 sites; tabs "four at 50th percentile"; population = Chrome 69 desktop/laptop users on Windows with metrics reporting enabled; period = two weeks from 2018-10-01. Covers (program side, context only — Windows): renderer-process count per browser, 50th percentile 4.4 → 6.2 and 99th percentile 35.0 → 52.7 with Site Isolation; renderer processes for single-tab page loads (google.com: no extra process; amazon.com and seatguru.com: five; wowprogress.com: ten) on a Windows 10 desktop. Existence (design): soft process limit computed from machine characteristics, no hard limit, same-site main-frame consolidation above the limit, one warmed-up spare renderer, out-of-process iframes. Linux mapping: not covered.
  - T10 — does not cover a rate (page-load count only compared between groups, no value given).
  - T1, T2, T4, T6, T7, T9 — does not cover.
- **Side.** Mixed: open sites/tabs are user-side (any platform, Windows); renderer-process counts are program-side from Windows — context only.

### S1-32 — Huang 2010, parallel browsing behaviour (browser plug-in logs)

- **Citation.** Jeff Huang and Ryen W. White. 2010. Parallel Browsing Behavior on the Web. In *Proceedings of the 21st ACM Conference on Hypertext and Hypermedia (HT '10)*, Toronto, June 13–16, 2010. ACM.
- **Copy read.** https://jeffhuang.com/papers/ParallelBrowsing_HT10.pdf (author-hosted, 5 pages), accessed 2026-10-01, `sources/S1-32/ParallelBrowsing_HT10.pdf`, SHA-256 `0551037335a93bc99306dbf40b7bd57cd75e736c2985ce1506ee6e5bd3b675f9`.
- **One observation.** Yes — one month of logs from one browser plug-in.
- **Machine/platform, subject, window named?** Platform: "a widely-distributed browser plug-in … installed alongside a popular Web browser" — browser and OS not named. Subject: over 50 million consenting users, ~60 billion pageviews. Window: June 2009.
- **Verbatim passages.**
  > "We study the use of parallel browsing through a log-based study of millions of Web users and present findings on their behavior." (Abstract, PDF p.1)

  > "We used the entire set of logs from June 2009 containing approx-imately 60 billion pageviews from over 50 million users, giving us high coverage of Web browsing behavior." (§3 Method, PDF p.2; hyphen as extracted)

  > "However, our data did not contain reliable indicators of window creation events, precluding that analysis." (§3, PDF p.2)

  > "The figure shows that 5-10 page views per tab is common, mean-ing users often visit a handful of pages in each tab." (§4.1, PDF p.3)

  > "Our logs showed that 88.7% of pageviews and 42.6% of tab sessions did not involve tab switch es. That is, users would remain on the same tab for the next pageview in 88.7% of cases, and continuous pageviews comprised en tire tab sessions in 42.6% of cases. Conversely, 57.4% of tab sessions had a least one tab switch." (§4.1, PDF p.3)
- **Coverage.**
  - T3 — partial: object = tab sessions and tab switches; unit = pageviews per tab, share of tab sessions with a switch; statistic = log-normal fit of pageviews per tab, 57.4% of tab sessions with ≥1 switch, 88.7% of pageviews followed by a pageview in the same tab; population = >50 M plug-in users; period June 2009. Number of tabs or windows open at once: not covered (no window events).
  - T10 — partial: pageview counts exist but no per-hour or per-session page-load rate is reported in the text.
  - T2 — partial: tab switches per pageview (browser-internal).
  - T1, T4, T6, T7, T9 — does not cover.
- **Side.** User-side (any platform; browser/OS unnamed).

### S1-33 — Weinreich 2008, long-term client-side study of Web use

- **Citation.** Harald Weinreich, Hartmut Obendorf, Eelco Herder, Matthias Mayer. 2008. Not Quite the Average: An Empirical Study of Web Use. *ACM Transactions on the Web* 2(1), Article 5 (DOI 10.1145/1326561.1326566). The same observation is also reported in Obendorf et al., "Web page revisitation revisited", CHI 2007, and Weinreich et al., "Off the beaten tracks", WWW 2006 (not opened; same data).
- **Copy read.** https://vsis-www.informatik.uni-hamburg.de/getDoc.php/publications/315/Weinreich-2008_-_Empirical_Study_of_Web_Use.pdf (authors' manuscript in the University of Hamburg repository, pages numbered 1–26, no journal pagination), accessed 2026-10-01, `sources/S1-33/Weinreich-2008_Empirical_Study_of_Web_Use.pdf`, SHA-256 `c3f30b622303fdbbef32ab12706e7bd58d01b079a6f3ab9537ad62efe2179fc3`.
- **One observation.** Yes — one logging study of 25 participants (intermediary proxy for all, instrumented Firefox 1.0 for 15).
- **Machine/platform, subject, window named?** Platform: proxy intermediary plus instrumented Firefox 1.0 (15 participants); OS not named. Subject: 25 unpaid volunteers, mostly German and Dutch, eight Dutch computer-science university employees. Window: Winter 2004/2005, 52–195 days per participant.
- **Verbatim passages.**
  > "The Web-usage study presented here was conducted in Winter 2004/2005 with 25 unpaid volunteers." (§3, p.4)

  > "length of the study varied individually from 52 to 195 days (mean: 105 days). We were able to confirm 137,272 user-initiated page visits to 65,643 distinct URIs and 9,741 dif- ferent domains (see section 3.3)." (§3, p.4)

  > "every participant had an intermediary installed that filt ered all transferred pages, and 15 of the 25 participants additionally made use of an instrumented version of the Firefox browser." (§3.2, p.5)

  > "Our participants had on average 2.1 windows or tabs opened when they access ed a new page 12 , suggesting that the use of multiple windows is not an exception, bu t the rule. However, the individual average differed from 1.07 to 8.19 concurrently ope ned documents, which shows that this practice was not followed by all users. About one t hird used mainly one window while the remaining participants used windows and tabs to a different extent. The number of people in our study using multiple windows was high er than the number of those using tabs – only six of the fifteen Firefox users (40%) regularly opened browser tabs." (§4.3, p.13; footnote 12: "Framesets were considered as one window.")

  > "nearly half of our participants used to keep one or several windows opened in the backgroun d of their computer desktop for extended periods." (§4.3, p.14)

  > "25% of all documents were displayed for less than 4 sec onds, and 52% of all visits were shorter than 10 seconds (median: 9.4s). However, ne arly 10% of the page visits were longer than two minutes." (§4.4, p.15)
- **Coverage.**
  - T3 — covers: object = browser windows plus tabs open when a new page is accessed; unit = count; statistic = mean 2.1 across participants, per-participant averages 1.07–8.19; population = 25 experienced Web users (Germany/Netherlands, many in computer science); period Winter 2004/2005. Visible-at-once: not covered.
  - T10 — covers: object = user-initiated page visits; unit = count and stay time; statistic = 137,272 visits over 52–195 days per participant (no per-hour rate stated; mean study length 105 days); stay time median 9.4 s (12.4 s for first visits). Reader's own arithmetic, not a value: 137,272 / (25 × 105 days) ≈ 52 page visits per participant-day of enrolment (enrolment days, not browsing days).
  - T1, T2, T4, T6, T7, T9 — does not cover.
- **Side.** User-side (any platform; OS unnamed).

### S1-34 — von der Weth 2013/2014, DOBBS browsing dataset (Firefox add-on)

- **Citation.** (a) Christian von der Weth, Manfred Hauswirth. 2013. DOBBS: Towards a Comprehensive Dataset to Study the Browsing Behavior of Online Users. DERI Technical Report 2013-06-08, arXiv:1307.1542v1. (b) Christian von der Weth, Manfred Hauswirth. 2014. Analysing Parallel and Passive Web Browsing Behavior and its Effects on Website Metrics. DERI Technical Report 2014-02-20, arXiv:1402.5255v1. Both report the same DOBBS add-on observation at two snapshots → one source.
- **Copy read.** (a) https://arxiv.org/pdf/1307.1542 (v1, 5 Jul 2013), `sources/S1-34/DOBBS-arxiv-1307.1542.pdf`, SHA-256 `86cbea9b4a92d0f2211c62f90a5d0ab0740ea4a6ffb0a4dbaf38152b1b57650e`; (b) https://arxiv.org/pdf/1402.5255 (v1, 21 Feb 2014), `sources/S1-34/arxiv-1402.5255.pdf`, SHA-256 `91a406fb0c949575d0355c87b0320ad7d54d816cc3cbba08f54b79f838ead3be`; both accessed 2026-10-01.
- **One observation.** Yes — one unsupervised field logging effort (Firefox add-on), reported at the 2013 snapshot (five longest-participating users) and the January 2014 snapshot (30 most active users).
- **Machine/platform, subject, window named?** Platform: Firefox add-on ("Currently available for Firefox at http://dobbs.deri.ie", (a) footnote 2); OS not named. Subject: volunteers recruited via mailing lists; 30 most active users with 1.6k–88k page loads each. Window: dataset "as it was available in January 2014"; start given as "August 2014" in (b) (as printed, inconsistent with the January 2014 snapshot).
- **Verbatim passages.**
  > "Figure 1 shows that User 1 is browsing most of the time with one browser window. Only ∼5% of the time s/he is using at least two windows in parallel (a nd almost never three or more). Regarding User 1’s usage of mult ple tabs, ∼78% of the time s/he has has at least two parallel open tabs, ∼40% of the time at least four parallel open tabs, ∼18% of the time at least eight parallel open tabs, and ∼1% of the time at least 16 parallel open tabs." ((a) §4, PDF p.15)

  > "This section presents the results of our analysis of the DOBB S dataset as it was available in January 2014." ((b) §4, PDF p.9)

  > "For our evaluation, we identiﬁed the 30 most active users with an activity ranging from 1,6k up to 88k overall page loads for individual users." ((b) §4, PDF p.10)

  > "DOBBS has ﬁrst been announced and promoted in August 2014 ove r pop- ular mailing lists." ((b) §4 Evaluation methodology, PDF p.10)

  > "We calculated th e average number of parallel open windows based the time intervals a user had one, two, three, etc. wind ows were open at the same time." ((b) §4.1, PDF p.10)

  > "The results show that tabbe d browsing is way more common than open multiple browser windows. Except for two users, the averagenumbers of parallel open windows is less than 2." ((b) §4.1, PDF p.12)

  > "User 5 is typically browsing with on e browser window. ∼25% of the time s/he is using at least two windows in parallel, and three or more wi ndows ∼5% of the time. Regarding tabbed browsing, ∼70% of the time User 5 has at least two parallel open tabs,∼60% of the time at least four parallel open tabs, ∼30% of the time at least eight parallel open tabs, and ∼5% of the time at least 16 parallel open tabs." ((b) §4.1, PDF p.12)

  > "As some kind of extreme cases, some users have a very high average number of open tabs, up to more than 60 ; cf. Figure 1(a). Even more, Users 29 and 30 have more than 16 tabs open for most of their browsing time." ((b) §4.1, PDF p.12)

  > "Figure 4 shows the average session length and the average exp licit idle time for each user, as well as the average number of page loads as number over each bar. Al l three results are the median of the respective measures and are sorted according to the average session length." ((b) §4.2, PDF p.14)
- **Coverage.**
  - T3 — covers: object = browser windows and tabs open in parallel; unit = share of browsing time with ≥k windows / ≥k tabs, and per-user average (median over sessions) of open windows and tabs; statistic = per-user distributions in Fig. 1 of (b) (only Users 1, 5, 29, 30 and the extremes described in text; per-user averages up to "more than 60" tabs); population = 30 most active Firefox add-on volunteers; period up to January 2014. Visible-at-once: not covered (window focus events logged but not reported as counts).
  - T10 — partial: per-user median page loads per session (Fig. 4 of (b), figure labels only) and session lengths; no per-hour rate in text.
  - T2 — partial: browser window focus lost/regained and explicit idle time recorded; reported as idle ratios vs session length (figures), not as focus dwell statistics.
  - T1, T4, T6, T7, T9 — does not cover.
- **Side.** User-side (any platform; OS unnamed).

### S1-35 — Ma 2023, browsing clutter (interviews and survey; self-report)

- **Citation.** Rongjun Ma, Henrik Lassila, Leysan Nurgalieva, Janne Lindqvist. 2023. When Browsing Gets Cluttered: Exploring and Modeling Interactions of Browsing Clutter, Browsing Habits, and Coping. In *CHI '23*, Article 861. ACM. DOI 10.1145/3544548.3580690.
- **Copy read.** https://research.aalto.fi/files/107553048/SCI_Ma_etal_CHI_2023.pdf via https://web.archive.org/web/2026id_/https://research.aalto.fi/files/107553048/SCI_Ma_etal_CHI_2023.pdf (Aalto repository reprint of the publisher's version, CC BY, with a repository cover page as PDF p.1), accessed 2026-10-01, `sources/S1-35/SCI_Ma_etal_CHI_2023.pdf`, SHA-256 `541d9b4a6a341e986dfffbe505ab2090b6d0d9a04493915d18ddd33a5a572e56`.
- **One observation.** Two observations: an interview study (N = 16) and a Prolific online survey (N = 400, 24 June – 11 July 2022). Both are self-report, not logs.
- **Machine/platform, subject, window named?** Survey: Prolific participants who use laptops or desktops daily; browser and OS not tabulated in the passages used; window 24 June – 11 July 2022.
- **Verbatim passages.**
  > "On a typical day, a majority of partici-pants (13/16) had one or two open browser windows, and between 10 and 20 open browser tabs. Only two participants experienced extremes: P14 had a minimalist approach that keeps the amount of tabs below three, and P1 had around 400 open tabs at a time." (§4.1.1, PDF p.6; hyphen as extracted)

  > "We collected data through the Prolific platform. The survey was released with the Webropol survey software and was open between 24th of June to 11th of July 2022. … Participants were selected based on the Prolific pre-screening question asking whether they used laptops or desktops on a daily basis. … In total, we received 400 valid survey answers" (§5.1, PDF p.10)

  > "Figure 2: Number of open tabs during web browsing. The majority of participants have commonly 5–10 tabs open." (PDF p.11)

  > Table 13 rows (number of tabs, responses, percentage): "<5 85 21.2%", "5-10 211 52.8%", "10-20 65 16.2%", "20-30 23 5.7%", "30-50 9 2.3%", "50-100 7 1.8%", ">100 0 0%" — "Table 13: Data for Figure 2: Number of open tabs during web browsing." (Appendix, PDF p.29)

  > Table 14 rows (number of windows): "1-3 318 79.5%", "3-5 52 13.0%", "5-10 22 5.5%", ">10 8 2.0%" — "Table 14: Data for Figure 3: Number of open windows during web browsing." (Appendix, PDF p.29)
- **Coverage.**
  - T3 — covers only as self-report (not logged data, so outside T3's "from logged data"): object = usually open tabs and windows; unit = response bins; statistic = share of 400 respondents per bin (52.8% report 5–10 tabs; 79.5% report 1–3 windows); population = Prolific laptop/desktop users; period June–July 2022.
  - T1, T2, T4, T6, T7, T9, T10 — does not cover.
- **Side.** User-side (self-report; platform not specified).

### S1-36 — Chang 2021, cost structure of browser tab usage (interviews, survey with tab snapshot)

- **Citation.** Joseph Chee Chang, Nathan Hahn, Yongsung Kim, Julina Coupland, Bradley Breneisen, Hannah S Kim, John Hwong, Aniket Kittur. 2021. When the Tab Comes Due: Challenges in the Cost Structure of Browser Tab Usage. In *CHI '21*, Yokohama, May 8–13, 2021. ACM. DOI 10.1145/3411764.3445585.
- **Copy read.** https://web.archive.org/web/20250526065900id_/https://dl.acm.org/doi/pdf/10.1145/3411764.3445585 (ACM publisher PDF, CC BY 4.0, archived 2025-05-26), accessed 2026-10-01, `sources/S1-36/Chang-CHI2021-3411764.3445585.pdf`, SHA-256 `8244e76bae0b67e2a336692831bdfd6d81ae9b585a8f335b60b7059413fc2501`. (Author list taken from the copy's title block.)
- **One observation.** Three: a preliminary survey (N = 64), interviews with 10 researchers over two weeks, and an MTurk survey (N = 103) in which each respondent listed their currently open tabs (capped at 10). All self-reported; none is a log.
- **Machine/platform, subject, window named?** Browser/OS not named; MTurk respondents "mostly from the US"; calendar period not stated.
- **Verbatim passages.**
  > "we conducted a preliminary survey to collect more empirical evidence about tab clutter (N=64, Age: 19-67; M=33.7; SD=10.6; 57% male; 77% from the US). … 25% of the participants reported that they had experienced browsers or computers crashing from having too many browser tabs." (§1 Introduction, PDF p.2)

  > "2) people who self-reported often reaching 12 or more tabs open on their work computer . … In the end, a total of ten participants were recruited (Age: 19-32, M=23.0, SD=4.7, 40% male, mostly graduate and undergraduate students)." (§3 Methodology, Study 1 Participants, PDF p.3)

  > "For this, participants gave a short description for each of their open browser tabs at the time when the survey took place (excluding tabs related to Mechanical Turk tasks, such as our survey page). … To control for survey duration, participants reported up to 10 browser tabs if they had more than 10, which accounted for 7.8% of all participants (N=103). On average, each participant labeled 6.15 tabs (SD = 3.69), or a total of 633 tabs." (§3 Methodology, Study 2, PDF p.4)

  > "The responses followed an long-tailed distribution showing that people have different toler-ances (Figure 1), with the median number being eight tabs (N=103, first quartile: 5 tabs; third quartile: 12 tabs). We further asked them how frequently they reach this threshold. The majority (67%) of our participants responded at least once a week" (§5 Pressures to Close Tabs, PDF p.5)
- **Coverage.**
  - T3 — partial, self-reported snapshot: object = tabs open at survey time; unit = count, censored at 10; statistic = mean 6.15 labelled (SD 3.69), 7.8% had more than 10; population = 103 MTurk workers, mostly US; period not stated (published 2021). Also an overwhelm threshold (median 8 tabs). Not logged data.
  - T1, T2, T4, T6, T7, T9, T10 — does not cover.
- **Side.** User-side (self-report).

### S1-37 — Reis 2009, Chromium process models (process-per-site-instance, process limit)

- **Citation.** Charles Reis and Steven D. Gribble. 2009. Isolating Web Programs in Modern Browser Architectures. In *EuroSys '09*, Nuremberg, April 1–3, 2009, pp. 219–232. ACM.
- **Copy read.** https://www.charlesreis.com/research/publications/eurosys-2009.pdf (author-hosted camera-ready, 13 pages), accessed 2026-10-01, `sources/S1-37/eurosys-2009.pdf`, SHA-256 `5f88f5af85a065811eb15a088172bd95539240a01525d3e131c24de58608d060`.
- **One observation.** Design description (existence) plus an evaluation on one Windows XP machine; no observation of process counts for a set of tabs.
- **Machine/platform, subject, window named?** Chromium 0.3.154, dual-core 2.8 GHz Pentium D, Windows XP SP3 (evaluation). Not Linux.
- **Verbatim passages.**
  > "Process-per-Site-Instance: The above process model can be reﬁned to create a separate renderer process for each site instance, providing meaningful fate sharing and isolation for each web program instance. This model pro-vides the best isolation beneﬁts and is used in Chromium by default." (§3.2, PDF p.8)

  > "Chromium also places a limit on the number of renderer processes it will create (usually 20), to avoid imposing too much overhead on the user’s machine. This limit may be raised in future versions of the browser if RAM is plentiful. When the browser does reach this limit, existing rendering engine processes are re-used for new site instances." (§3.2 Caveats, PDF p.8)

  > "Our experiments are conducted using Chromium 0.3.154 on a dual core 2.8 GHz Pentium D computer running Win-dows XP SP3." (§4, PDF p.9)
- **Coverage.**
  - T3 — existence only (program side, historical, Windows): process-per-browsing-instance, process-per-site-instance (default in 2009), process-per-site models; renderer-process limit "usually 20" with reuse above it. No count observation; no Linux.
  - T1, T2, T4, T6, T7, T9, T10 — does not cover.
- **Side.** Program-side, non-Linux — context only.

### S1-38 — Vila 2017, Loophole (Chrome event loops; renderer-sharing threshold observed)

- **Citation.** Pepe Vila and Boris Köpf. 2017. Loophole: Timing Attacks on Shared Event Loops in Chrome. In *26th USENIX Security Symposium*. Preprint arXiv:1702.06764.
- **Copy read.** https://arxiv.org/pdf/1702.06764 (v2, 28 Jun 2017), accessed 2026-10-01, `sources/S1-38/Loophole-arxiv-1702.06764.pdf`, SHA-256 `11d7d5557b5fb20e17f89f63a3776c60f00566ce5dea660e8d3028f33856f501`.
- **One observation.** The renderer-sharing threshold is one small observation on two machines (4 GB and 8 GB RAM); the attack experiments are separate observations on three named machines.
- **Machine/platform, subject, window named?** Threshold observation: RAM named (4 GB, 8 GB), OS and Chrome version for that specific experiment not named (the threshold rule is stated for 64-bit OS X and Linux). Attack experiments: Debian 8.6 kernel 3.16.0-4-amd64, i5 3.30 GHz ×4, 4 GB, Chromium v53; Debian 8.7, i5-6500 ×4, 16 GB, Chromium v57; OS X MacBook Pro 5.5, 4 GB, Chrome v54; Chrome v52–v58 over about a year.
- **Verbatim passages.**
  > "Each renderer runs several threads; the most relevant ones are: • the MainThread where resource parsing, style cal-culation, layout, painting and non-worker Javascript runs, • the IOChildThread, which handles IPC communi-cation with the host process, and • the CompositorThread, which improves respon-siveness during the rendering phase" (§2.2, PDF p.3)

  > "When the number of renderer processes exceeds a certain threshold, Chrome starts to reuse existing [page break, PDF p.3 → p.4] renderers instead of creating new ones. On (64-bit) OSX and Linux, the threshold for reusing renderers is calculated by splitting half of the physical RAM among the renderers, under the assumption that each consumes 60MB. 1 In our experiments, on a ma-chine with 4 GB of RAM we could spawn 31 new tabs before any renderer was shared, whereas on a machine with 8 GB of RAM we observed a threshold of approx-imately 70 renderers. There is no apparent grouping policy for the pages that can share a process when this threshold is exceeded, except for tabs in Incognito mode not being mixed up with “normal” tabs." (§2.3, PDF p.3–4; footnote 1: "On Android there is no threshold since the OS suspends idle pr o-cesses.")

  > "1. Debian 8.6 with kernel 3.16.0-4-amd64, running on an Intel i5 @ 3.30GHz x 4 with 4 GB of RAM, and Chromium v53; 2. Debian 8.7 with kernel 3.16.0-4-amd64, running on an Intel i5-6500 @ 3.20GHz x 4 with 16 GB of RAM, and Chromium v57; and 3. OSX running on a Macbook Pro 5.5 with In-tel Core 2 Duo @ 2.53GHz with 4 GB of RAM, and Chrome v54." (§4.1.2, PDF p.7)
- **Coverage.**
  - T3 — covers (program side): object = renderer processes before process sharing begins; unit = number of new tabs / renderers; statistic = 31 tabs on a 4 GB machine, ≈70 renderers on an 8 GB machine (single observations); rule stated for 64-bit OS X and Linux (half of physical RAM / 60 MB per renderer); Chrome/Chromium v52–v58 era. Linux-ness of the threshold run is not stated explicitly. Also names renderer threads (MainThread, IOChildThread, CompositorThread) and host threads (CrBrowserMain, IOThread) — existence.
  - T1, T2, T4, T6, T7, T9, T10 — does not cover.
- **Side.** Program-side; Linux likely but not stated for the threshold run — candidate with that caveat.

### S1-39 — Kooti 2015, Yahoo Mail conversations and e-mail load

- **Citation.** Farshad Kooti, Luca Maria Aiello, Mihajlo Grbovic, Kristina Lerman, Amin Mantrach. 2015. Evolution of Conversations in the Age of Email Overload. In *WWW 2015*, Florence, pp. 603–613. Preprint arXiv:1504.00704.
- **Copy read.** https://arxiv.org/pdf/1504.00704 (v1, 2 Apr 2015), accessed 2026-10-01, `sources/S1-39/Kooti-arxiv-1504.00704.pdf`, SHA-256 `ac8f1a63419e2fa3127a57867f71ffd37c1204f1f310e25c5c08ee26726e7df7`.
- **One observation.** Yes — one Yahoo Mail log sample (opt-in users) over an undisclosed number of months.
- **Machine/platform, subject, window named?** Platform: Yahoo Mail (web and mobile clients; device type analysed separately). Subject: 2M opt-in users in 1.3M reciprocal dyads; 16B e-mails. Window: "undisclosed number of months".
- **Verbatim passages.**
  > "Accordingly, we selected a random subsample E of 1.3M dyads of Yahoo Mail users worldwide who have signiﬁcant interactions with each other, sending at least ﬁve replies in each direction in the time span of undisclosed number of months. … These pairs comprise a set N containing 2M unique users exchanging 187M emails overall. … Next, we gathered all incoming and outgoing emails of users in N over the same time period, a total of 16B emails." (§2, PDF p.2)

  > "Each email included the sender ID, receiver ID, time sent, sub-ject, body of the email, and number of attachments." (§2, PDF p.2)

  > "Replies to emails with attachments are much slower (median of 56 minutes) than replies to emails without any attachment (median of 32 minutes)." (§4.4, PDF p.6)

  > "We characterize a user’semail load by the number of messages the user receives in a day, and the useractivity by the number of sent emails." (§4.5, PDF p.6)

  > "Figure 13 shows that user activity increases, both in terms of the number of sent emails and replied emails, as the number of emails they receive in a day grows. Here, we eliminate the users who sent more than 1,000 emails in a day" (§4.5, PDF p.6)

  > "Figure 14(a) shows that as the email load increases, users reply to a smaller fraction of their emails, from about 25% of all emails received in a day at low load to less than 5% of emails at high load (about 100 emails a day)." (§4.5, PDF p.6)
- **Coverage.**
  - T10 — partial: object = e-mails received and sent per user-day; unit = count per day; statistic = mean sent vs received per day shown only as a curve (Fig. 13, x-axis 0–100 received per day); attachments recorded but only reply-time differences reported; population = 2M opt-in Yahoo Mail users; period undisclosed. No per-hour send rate, no attachment share.
  - T1, T2, T3, T4, T6, T7, T9 — does not cover.
- **Side.** User-side (webmail, any device).

### S1-40 — Fisher 2006, e-mail overload revisited (600 Outlook mailboxes)

- **Citation.** Danyel Fisher, A. J. Brush, Eric Gleave, Marc A. Smith. 2006. Revisiting Whittaker & Sidner's "Email Overload" Ten Years Later. In *CSCW '06*, Banff, November 4–8, 2006, pp. 309–312. ACM.
- **Copy read.** https://www.microsoft.com/en-us/research/wp-content/uploads/2006/11/p309-fisher.pdf (publisher-format PDF on Microsoft Research), accessed 2026-10-01, `sources/S1-40/p309-fisher.pdf`, SHA-256 `7245a09d920cb26d3e973cc72ed107b8b2824ca5258f8c172c8fa43e7b64b248`.
- **One observation.** Yes — one snapshot per user of 600 Outlook archives uploaded by the SNARF prototype.
- **Machine/platform, subject, window named?** Platform: Microsoft Outlook (2003, XP) at one technology company (Microsoft); OS not stated. Subject: 600 employees, diverse roles. Window: snapshots between 15 July 2005 and 30 January 2006; daily rate from the last seven days of each archive.
- **Verbatim passages.**
  > "We collected data snapshots of email archives from users of SNARF between July 15, 2005 and January 30, 2006. … Our final sample contained 600 participants." (§2, PDF p.1, p.309)

  > "we es timated the number of messages each participant receives daily by averaging the number of messages in a user’s archive received in the last seven days. This approximation is a lower bound for email received because we assume that people delete some fraction of incoming email. For our participants, the mean number of messages received daily was 87 (median = 58)." (§3.2, PDF p.2, p.310)

  > "Daily # msg. received 49 87 (58)" (Table 1, columns 1996 / 2006, PDF p.2, p.310)

  > "We found nearly a third (mean = 30%, median = 27%) of the messages in an archive were sent by the participant’s themselves." (§3.1, PDF p.2, p.310)
- **Coverage.**
  - T10 — covers (receive side): object = e-mail messages received; unit = messages per day (lower bound, deletion not observed); statistic = mean 87, median 58; population = 600 employees of one technology company using Outlook; period mid-2005 to early 2006. Sent rate not reported (only the share of archived messages sent by the user). Attachments not covered.
  - T1, T2, T3, T4, T6, T7, T9 — does not cover.
- **Side.** User-side.

### S1-41 — Kumar 2010, characterization of online browsing (Yahoo! toolbar logs)

- **Citation.** Ravi Kumar and Andrew Tomkins. 2010. A Characterization of Online Browsing Behavior. In *WWW 2010*, Raleigh, NC, April 26–30, 2010, pp. 561–570.
- **Copy read.** https://archives.iw3c2.org/www2010/proceedings/www/p561.pdf (IW3C2 proceedings PDF), accessed 2026-10-01, `sources/S1-41/Kumar-Tomkins-WWW2010-p561.pdf`, SHA-256 `30d4c43ce8efe0bd85bbbd570b12fbdc28ce78ae979aa1ce39cf5386c4307df9`.
- **One observation.** Yes — one random sample of Yahoo! toolbar users over 18–24 March 2009 (plus 25 March).
- **Machine/platform, subject, window named?** Platform: Yahoo! toolbar (browser/OS not named). Subject: random sample of toolbar users who consented to logging; >50 million pageviews. Window: 18–24 March 2009.
- **Verbatim passages.**
  > "We pro- pose a new CCS taxonomy of pageviews consisting of Con- tent (news, portals, games, verticals, multimedia), Commu- nication (email, social networking, forums, blogs, chat), and Search (Web search, item search, multimedia search). We show that roughly half of all pageviews online are content, one-third are communications, and the remaining one-sixth are search." (Abstract, PDF p.1, p.561)

  > "We consider a random sample of users drawn from Yahoo! toolbar logs over a one week period from March 18, 2009 to March 24, 2009." (§3, PDF p.2, p.562)

  > "A sequence of pageviews for a particular user is broken into subsequences called sessions between any two consecutive pageviews whose timestamps are more than thirty minutes apart." (§4.1, PDF p.3, p.563)

  > "For users, the median number of pageviews per day is 59, and the median time online is about an hour. … 1% of users spend more than 9 hours per day online, and view over 927 pageviews averaged over our sam-ple. Likewise, 10% of users spend only three minutes per day and view fewer than 5 pages. Individual sessions tend to be signiﬁcantly smaller. The median length is 17 pageviews taking 16 minutes of time." (§4.1, PDF p.3, p.563)

  > Table 1 (as extracted): "Per user Total pageviews Total time online per week per week Pageviews % users Total time % users ≤ 3 11 ≤ 30 sec 10 ≤ 113 50 ≤ 1.6 hrs 50 ≤ 1097 90 ≤ 15 hrs 90 ≤ 3614 99 ≤ 41 hrs 99 Per session … ≤ 2 13 ≤ 7 sec 10 ≤ 17 50 ≤ 17 min 50 ≤ 113 90 ≤ 1.5 hrs 90 ≤ 385 99 ≤ 4.0 hrs 99" (PDF p.3, p.563)

  > "The median pageview has a gap of only 12 seconds, and fewer than 10% of pageviews have a gap that stretches to more than 90 seconds." (§4.1, PDF p.3, p.563)

  > "Inter-arrival time % pageviews ≤ 1 sec 16 ≤ 11 sec 50 ≤ 1.5 min 90 ≤ 12.8 min 99" (Table 2, PDF p.4, p.564)
- **Coverage.**
  - T10 — covers: object = pageviews (page loads); unit = pageviews per user-day, per session, inter-arrival time; statistic = median 59 per day (text) — note Table 1 is headed "per week" with median ≤113, an inconsistency in the source; median session 17 pageviews / 16–17 min; median inter-arrival 12 s (Table 2: 50% ≤ 11 s); population = consenting Yahoo! toolbar users (biases listed by the authors); period 18–24 March 2009. Also one-third of pageviews are communication (e-mail, social networking, forums, blogs, chat), per the abstract.
  - T1 — partial: time online per user-day (median about an hour).
  - T2, T3, T4, T6, T7, T9 — does not cover.
- **Side.** User-side.

### S1-42 — Lut 2021, How we browse (Chrome extension, 31 participants, 14 days)

- **Citation.** Yuliia Lut, Michael Wang, Elissa M. Redmiles, Rachel Cummings. 2021. How we browse: Measurement and analysis of digital behavior. arXiv:2108.06745v1.
- **Copy read.** https://arxiv.org/pdf/2108.06745 (v1, 15 Aug 2021), accessed 2026-10-01, `sources/S1-42/HowWeBrowse-arxiv-2108.06745.pdf`, SHA-256 `13f5864348a143e14ca451740a962d0a48ca1763f38374d53a585f78fca7e81b`.
- **One observation.** Yes — one 14-day Chrome-extension logging study of 31 participants.
- **Machine/platform, subject, window named?** Platform: Chrome extension on desktop/laptop (OS not named). Subject: 31 participants, mostly Georgia Tech students. Window: 14 days in August–September 2019.
- **Verbatim passages.**
  > "we observed the browsing beha vior of 31 participants over a period of 14 days in August and September 2019" (§3, PDF p.3)

  > "We chose a set of user browsing actions to observe through this extension, which included: hitting the back button or forward button ( backButton), creating a new tab either manually or by opening a link in a new tab ( newTab), changing tabs ( tabChange), typing in the address bar ( omniBox), going to a new URL either by using the address bar or clicking a link in a page ( urlChange), clicking a button in a webpage that does not change the URL (e.g., ‘Like’ on social media) ( click), and typing in a textbox within a webpage ( type)." (§3.2.1, PDF p.4)

  > "Overall, we observe that our participants spent an average of 146 minutes (SD = 100.5) browsing daily during the course of the study. Participants averaged 968 brows ing actions per day (SD = 1529)." (§4, PDF p.8)

  > "we observe that our participants visit similar numbers of pages per session (5-151 per se ssion vs. 14-130 in [1]), but spend more time online (median of 2.9 hours per day vs. a median of an hour per day in [19])." (§4, PDF p.8)
- **Coverage.**
  - T10 — partial: object = browsing actions (including typed characters, clicks, URL changes) and pages per session; unit = actions per day, pages per session; statistic = mean 968 actions/day (SD 1529), pages per session range 5–151 across participants; population = 31 students; period Aug–Sep 2019. Page loads per hour not separated from other actions.
  - T1 — partial: browsing time per day (mean 146 min; median 2.9 h).
  - T3 — partial: newTab and tabChange events logged but no counts of open tabs reported.
  - T2, T4, T6, T7, T9 — does not cover.
- **Side.** User-side.

### S1-43 — Lafreniere 2009/2010, two years of instrumented GIMP use (ingimp)

- **Citation.** Ben Lafreniere, Andrea Bunt, John Whissell, Charlie Clarke, Michael Terry. Characterizing Large-Scale Use of a Direct Manipulation Application in the Wild. University of Waterloo technical report CS-2009-27 (2009); published in *Proceedings of Graphics Interface 2010*, pp. 11–18.
- **Copy read.** https://cs.uwaterloo.ca/research/tr/2009/CS-2009-27.pdf (technical-report version; the GI 2010 paper was not reachable, graphicsinterface.org 403), accessed 2026-10-01, `sources/S1-43/CS-2009-27.pdf`, SHA-256 `69be081b44f9276d12469bf2f64e997b8f5c73cda08cad697748cd49a8e3d79d`.
- **One observation.** Yes — one public deployment of instrumented GIMP (ingimp), logs 15 May 2007 – 15 May 2009.
- **Machine/platform, subject, window named?** Platform: Windows 73%, Linux 26% of users. Subject: 211 "significant users" (used and saved on ≥2 separate days), 4,198 logs. Window: 15 May 2007 – 15 May 2009.
- **Verbatim passages.**
  > "Our analysis considers all log files collected in the 2-year period between May 15, 2007 and May 15, 2009." (PDF p.3)

  > "Using these criteria, the ingimp community consists of 211 significant users who have con-tributed 4198 logs." (PDF p.3)

  > "The majority of ingimp users run Windows (73%) with the second-largest group running Linux (26%)." (PDF p.4)

  > "The median number of ses-sions for an individual user was 11 (mean 20, SD 26.0)." (PDF p.4)

  > "The average session length for the community was 59 minutes (median 9 min-utes, SD 3 hours 49 minutes). However, this measure sim-ply refers to the duration for which the application was open. … Given that the average length of time be-tween commands was 19 seconds, we chose 120 seconds as a conservative threshold for idle time. Once idle time is removed, Figure 1 shows that most sessions are made up of less than 10 minutes of active usage, with a median of 6 minutes and an average of 16 minutes (SD 26 minutes)." (PDF p.4)

  > "Conversely, applying a filter will only result in one logged command, regardless of how long the user spends adjusting settings before it is fi-nally applied." (PDF p.5)

  > "The number of command invocations per session ranged from 1 to 9236 with a median of 24 and mean of 167.3 (SD 479.8) (see Figure 2)." (PDF p.4)

  > "Notably absent from this list are commands for manipulating or touching-up photographic images, such as those that alter the brightness, contrast, hue, or saturation of an image." (PDF p.5)
- **Coverage.**
  - T10 — partial: object = undo-stack commands in GIMP (filters count as one command each); unit = commands per session, time between commands; statistic = median 24 commands per session (mean 167.3), mean 19 s between commands, active session median 6 min; filters are not among the 20 most used commands (Tables 1–2, top commands Undo, Paintbrush, selection, layers); population = 211 ingimp users, 73% Windows / 26% Linux; period May 2007 – May 2009. No filter-specific per-hour rate.
  - T1 — partial: object = GIMP open duration; statistic = session (open-to-close) mean 59 min, median 9 min.
  - T9 — partial: object = application sessions (one log per launch-to-close); statistic = median 11 sessions per user over the study (mean 20); no launches-per-hour.
  - T2, T3, T4, T6, T7 — does not cover.
- **Side.** User-side (mixed Windows/Linux population).

### S1-44 — Chang 2021, Zoom/Webex/Meet measurement with emulated Linux clients

- **Citation.** Hyunseok Chang, Matteo Varvello, Fang Hao, Sarit Mukherjee. 2021. Can You See Me Now? A Measurement Study of Zoom, Webex, and Meet. In *IMC '21*. Preprint arXiv:2109.13113.
- **Copy read.** https://arxiv.org/pdf/2109.13113 (v1, 27 Sep 2021), accessed 2026-10-01, `sources/S1-44/ChangVarvello-IMC2021-arxiv-2109.13113.pdf`, SHA-256 `639750300ce4c7f36b62180cdf4f3f5c5d9e102a3f68c3cc280be036fd7a6815`.
- **One observation.** One benchmark campaign (cloud VMs plus Android phones), April–May 2021; client resource use measured on Android only.
- **Machine/platform, subject, window named?** Cloud VM: 8 vCPUs Xeon Platinum 8272CL, 16 GB; native Linux Zoom client v5.4.9 (57862.0110); Webex and Meet via web client; period 4/2021–5/2021.
- **Verbatim passages.**
  > "In Linux,snd-aloop and v4l2loopback modules allow one to set up a virtual sound-card device and a virtual video device, respectively. … In our setup we useaplay and ffmpeg to replay audio/video files into these virtual devices." (§3.1 Design Approach, PDF p.3)

  > "The experiments were conducted from 4/2021 to 5/2021." (§4, PDF p.4)

  > "Each cloud VM we deploy has 8 vCPUs (Intel Xeon Platinum 8272CL with 2.60GHz), 16GB memory and 30GB SSD. … We use the native Linux client for Zoom (v5.4.9 (57862.0110)), and the web client for Webex and Meet since they do not provide a native Linux client." (§4.1, PDF p.4)
- **Coverage.**
  - T10 — existence only for the video-call question: a native Zoom Linux client and browser-based Webex/Meet ran on Linux VMs in 2021 with loopback camera/microphone; process and thread structure not reported; CPU usage reported only for Android phones (context, not Linux).
  - T1, T2, T3, T4, T6, T7, T9 — does not cover.
- **Side.** Program-side; existence only.

### S1-45 — MacMillan 2021, video-conferencing network utilization on Ubuntu laptops

- **Citation.** Kyle MacMillan, Tarun Mangla, James Saxon, Nick Feamster. 2021. Measuring the Performance and Network Utilization of Popular Video Conferencing Applications. In *IMC '21*, pp. 229–244. Preprint arXiv:2105.13478.
- **Copy read.** https://arxiv.org/pdf/2105.13478 (v1, 27 May 2021), accessed 2026-10-01, `sources/S1-45/MacMillan-IMC2021-arxiv-2105.13478.pdf`, SHA-256 `5c3ec6aa554fbce2d4df7678cdae70427ad5e53a1dfb37484b6aa6f93ad8adc7`.
- **One observation.** One lab campaign (two identical laptops); network metrics only.
- **Machine/platform, subject, window named?** Two Dell Latitude 3300, 1366×768, Ubuntu 20.04.1; Chrome 89.0.4389 (Meet), Zoom 5.6.1, Teams 1.4.00.7556; period not stated beyond 2021.
- **Verbatim passages.**
  > "Teams and Zoom provide desktop applica-tions as well as browser clients, whereas Meet is “native" in the Chrome. Most of our tests are conducted using the desk-top applications for Teams and Zoom, and using the Google Chrome browser for Meet. … We use Chrome (Meet) version 89.0.4389, Zoom client version 5.6.1, and Teams client version 1.4.00.7556." (§2.2, PDF p.2)

  > "We use two identical laptops, referred to as C1 and C2, representing the two VCA clients. Each laptop is a Dell Latitude 3300 with a screen resolution of 1366 × 768 pixels and running Ubuntu 20.04.1." (§2.2, PDF p.3)
- **Coverage.**
  - T10 — existence only: Zoom and Teams native clients and Meet/Teams/Zoom in Chrome ran on Ubuntu 20.04.1 in two-party calls in 2021; process and thread structure not reported.
  - T1, T2, T3, T4, T6, T7, T9 — does not cover.
- **Side.** Program-side; existence only.

### S1-46 — Leskovec 2008, planetary-scale view of an IM network (MSN Messenger, June 2006)

- **Citation.** Jure Leskovec and Eric Horvitz. 2008. Planetary-Scale Views on an Instant-Messaging Network. arXiv:0803.0939v1 (also WWW 2008, "Planetary-scale views on a large instant-messaging network").
- **Copy read.** https://arxiv.org/pdf/0803.0939 (v1, 6 Mar 2008), accessed 2026-10-01, `sources/S1-46/Leskovec-Horvitz-arxiv-0803.0939.pdf`, SHA-256 `df54096ddb704a9807a6c2fb2a9229a879b6f0ba5b5fe304194f95b592313f55`.
- **One observation.** Yes — one month (June 2006) of Microsoft Messenger presence and conversation logs.
- **Machine/platform, subject, window named?** Platform: Microsoft Messenger (client OS not named). Subject: 242.7 M users logged in, 179.8 M in conversations. Window: 30 days of June 2006.
- **Verbatim passages.**
  > "• Communication: For each user participating in the session, the log contains the following tuple: session id, user id, time joined the sessio n, time left the session, number of messages sent, number of messages received." (§2, PDF p.4)

  > "Over the observation period, 242,720,596 users logged into Messenger and 179,792,538 of these users were actively engaged in conversations by sendi ng or receiving at least one IM message. … As a representative day, on June 1 2006, there were almost 1 bill ion (982,005,323) diﬀerent sessions (conversations among any number of people), with m ore than 7 billion IM messages sent. Approximately 93 million users logged in with 64 milli on diﬀerent users becoming engaged in conversations on that day." (§3.1, PDF p.4)

  > "Table 1: Cross-gender communication. Data is based on all tw o-person conversations from June 2006. (a) Percentage of conversations among users of diﬀere nt self-reported gender; (b) average conversation length in seconds; (c) number of exchanged mes sages per conversation; (d) number of exchanged messages per minute of conversation." (PDF p.11; table values: (b) 252–304 s, (c) 5.7–7.6 messages, (d) 1.25–1.50 messages per minute)
- **Coverage.**
  - T10 — covers (population level): object = instant messages sent/exchanged; unit = messages per day (whole network), messages per conversation, messages per conversation-minute; statistic = >7 billion messages on 1 June 2006 among 64 M engaged users; 5.7–7.6 messages per two-person conversation; 1.25–1.50 messages per minute of conversation; average conversation 252–304 s; population = all Messenger users, June 2006. Reader's own arithmetic, not a value: 7×10⁹ / 64×10⁶ ≈ 110 messages sent per engaged user on that day. Per-user per-hour received rate not reported.
  - T1, T2, T3, T4, T6, T7, T9 — does not cover.
- **Side.** User-side.

### S1-47 — Wang 2022, Slack group-chat channels in an enterprise R&D division

- **Citation.** Dakuo Wang, Haoyu Wang, Mo Yu, Zahra Ashktorab, Ming Tan. 2022. Group Chat Ecology in Enterprise Instant Messaging: How Employees Collaborate Through Multi-User Chat Channels on Slack. *Proc. ACM Hum.-Comput. Interact.* 6(CSCW1), Article 94. Preprint arXiv:1906.01756v5.
- **Copy read.** https://arxiv.org/pdf/1906.01756 (v5, 27 Jan 2022), accessed 2026-10-01, `sources/S1-47/GroupChatEcology-arxiv-1906.01756.pdf`, SHA-256 `aa48330365f21491db79c40ab4a0fb7b051818b4903b65e454ff83792ea87275`.
- **One observation.** Yes — one corpus of 4,300 Slack channels of one company division, March 2016 – March 2019.
- **Machine/platform, subject, window named?** Platform: Slack (client devices not named). Subject: 8,000 employees of an R&D division of a large IT company. Window: March 2016 – March 2019.
- **Verbatim passages.**
  > "we collected a total number of 4,300 group chat channels being created and used by 8,000 employees in a R&D division in a b ig IT company. We collected both the meta data and the raw messages of these channels spanning from Mar 2016 (Slack was ﬁrst introduced) to Mar 2019 (this Paper was written)." (§1, PDF p.2)

  > Table rows (per channel category; columns as extracted, first three categories): "3 active_timespan #days between ﬁrst message and last mes-sage 281.3 478.6 506.5" and "6 #messages #messages in total in this Slack channel 355.9 3059.0 4537.4" (PDF p.7)
- **Coverage.**
  - T10 — partial: object = messages per channel; unit = total messages and active days per channel; statistic = category means (e.g. 355.9 messages over 281.3 active days in the first category); population = 4,300 channels of 8,000 employees; period 2016–2019. Per-user received-message rate not reported. Reader's own arithmetic, not a value: 355.9 / 281.3 ≈ 1.3 messages per active day for a channel of that category.
  - T1, T2, T3, T4, T6, T7, T9 — does not cover.
- **Side.** User-side.

### S1-48 — Oliveira 2021/2023, Chromebook field study of open Chrome tabs (114 Google users)

- **Citation.** Geraldo F. Oliveira, Saugata Ghose, Juan Gómez-Luna, Amirali Boroumand, Alexis Savery, Sonny Rao, Salman Qazi, Gwendal Grignou, Rahul Thakur, Eric Shiu, Onur Mutlu. Extending Memory Capacity in Consumer Devices with Emerging Non-Volatile Memory: An Experimental Study. arXiv:2111.02325v3 (19 Sep 2023).
- **Copy read.** https://arxiv.org/pdf/2111.02325 (v3, 19 Sep 2023), accessed 2026-10-01, `sources/S1-48/Oliveira-NVM-arxiv-2111.02325.pdf`, SHA-256 `b1a43f5ac34938b109c2ca63840d82d051508773767c9e6b46d8eda620748249`.
- **One observation.** Yes for the field study (114 users, three months, samples every 5 minutes); separate lab experiments follow.
- **Machine/platform, subject, window named?** Platform: off-the-shelf Chromebooks (ChromeOS, Linux kernel) with 8 GB DRAM of which 4 GB reserved for in-DRAM compressed swap. Subject: 114 randomly picked users from a major division at Google. Window: "a period of three months"; calendar dates not given.
- **Verbatim passages.**
  > "For this purpose, we distributed Chromebook devices1 to 114 different users at Google, whom we asked to perform their daily activities using the Chromebook devices. We picked the users randomly from a major division at the company that employs thousands of people. We monitored their activity by periodically collecting the following system information over a period of three months: • Number of Chrome tabs opened: We recorded the number of open tabs across all Chrome windows. Data samples were reported every 5 minutes. In total, we collected 19,487 data samples. • Tab switch latency: We collected the tab switch latencies for each tab switch the user performed during their activity. Data samples were reported at each individual tab switch. In total, we collected 62,243 data samples." (§2.2, PDF p.4)

  > "1The Chromebook devices we use for our experiment consist of off-the-shelf Chrome-book devices with 8 GB DRAM capacity, of which 4 GB are reserved to enable an in-DRAM compressed swap space." (§2.2 footnote, PDF p.4)

  > "We observe that users had up to 20 Chrome tabs open in 68% of the samples; 21 to 40 Chrome tabs open in 18% of the samples; 41 to 80 Chrome tabs open in 10% of the samples; and 81 to 160 Chrome tabs open in 4% of the samples (no user had more than 160 tabs open at any time). Even though 4% is a relatively low number of occurrences, it represents 710 sample points where the users kept a large number of Chrome tabs open." (§2.2, PDF p.4)

  > "In Chrome, each tab represents a single process associated with the web page displayed in the tab, which improves reliability and se-curity [154, 155]." (§2.1, PDF p.3)
- **Coverage.**
  - T3 — covers: object = open Chrome tabs across all windows; unit = count per 5-minute sample; statistic = binned distribution (Fig. 2a: 0–20: 67.66%, 21–40: 18.03%, then 8.37, 1.89, 0.71, 1.75, 1.20, 0.38% per 20-tab bin up to 160 — figure labels; text: ≤20 in 68%, 21–40 in 18%, 41–80 in 10%, 81–160 in 4%, max ≤160); population = 114 Google employees; platform = ChromeOS Chromebooks; period three months (dates not stated). Renderer processes: the paper asserts one process per tab (citing documentation) but does not measure process counts. Also 62,243 tab switches logged (no per-hour rate).
  - T2 — partial: tab-switch events counted (browser-internal), no rate.
  - T1, T4, T6, T7, T9, T10 — does not cover.
- **Side.** User-side (any platform: ChromeOS). Program-side process claim is not an observation.

### S1-49 — Jackson 2003, e-mail interruptions observed by screen recording (Outlook)

- **Citation.** Thomas Jackson, Ray Dawson, Darren Wilson. 2003. Reducing the effect of email interruptions on employees. *International Journal of Information Management* 23, 55–65.
- **Copy read.** https://www.interruptions.net/literature/Jackson-IJIM03.pdf (publisher-format PDF on interruptions.net; PDF p.n = printed p.54+n), accessed 2026-10-01, `sources/S1-49/Jackson-IJIM03.pdf`, SHA-256 `2a4ad009165d6ace4b5aed794733830de294555b671903643657219476a21d10`.
- **One observation.** Yes — 15 employees of one UK company, 28 working days of WinVNC screen recording.
- **Machine/platform, subject, window named?** Platform: Windows PCs (WinVNC), Microsoft Outlook 2000 (70%) and Outlook 97 (30%). Subject: 15 employees of the Danwood Group (~500 employees). Window: 28 working days; year not stated (published 2003).
- **Verbatim passages.**
  > "A total of 15 employees were monitored over 28 working days, which led to over 180 hours of videotape recordings." (§3, PDF p.5, p.59)

  > "Out of the employees monitored 70% used Microsoft Outlook2000 and 30% used Microsoft Outlook97. … The majority of the employees monitored had their email software checkfor incoming messages every 5min. This was set by default when the software was ﬁrst installed." (§4, PDF p.5, p.59)

  > "It tookthe employees an average of 1min 44s to react to a new email notiﬁcation by opening uptheemailapplication. Themajority of emails, 70%,were reactedto within 6s ofthem arriving and85%werereactedtowithin2minofarriving." (§4, PDF p.5, p.59; missing spaces as extracted)

  > "The time it takes the employees to recover from an email interrupt, and to return to their workat the same workrate at which they left it, was found to be on average 64s." (§4, PDF p.5, p.59)

  > "The ﬁndings of the email analysis show that, on [Fig. 1 and page break, PDF p.6 → p.7] average, about 60s is spent per email excluding recovery time" (§5, PDF p.6–7, pp.60–61)
- **Coverage.**
  - T10 — partial: object = reaction to incoming e-mail; unit = seconds from arrival to opening the mail application, recovery time; statistic = mean 1 min 44 s, 70% within 6 s, 85% within 2 min, mean recovery 64 s, about 60 s handling per e-mail; population = 15 employees of one UK company, Outlook on Windows; period 28 working days. Number of e-mails received or sent per hour not reported.
  - T2 — partial: interruption and resumption (recovery 64 s).
  - T1, T3, T4, T6, T7, T9 — does not cover.
- **Side.** User-side.

### S1-50 — Avrahami 2006/2008, logged instant messaging (Trillian Pro on Windows)

- **Citation.** (a) Daniel Avrahami and Scott E. Hudson. 2006. Responsiveness in Instant Messaging: Predictive Models Supporting Inter-Personal Communication. In *CHI 2006*, Montréal, pp. 731–740. (b) Daniel Avrahami, Susan R. Fussell, Scott E. Hudson. 2008. IM Waiting: Timing and Responsiveness in Semi-Synchronous Communication. In *CSCW '08*, San Diego. (b) extends the same logged corpus ("see [2] and [3] for other analyses of this data") → one source.
- **Copy read.** (a) https://www.interruptions.net/literature/Avrahami-CHI06-p731-avrahami.pdf, `sources/S1-50/Avrahami-CHI06-p731.pdf`, SHA-256 `3ae82153267a4a25de6dcdfdf1bd4955529c382a46886b40b5771e971e889dee`; (b) https://www.interruptions.net/literature/Avrahami-CSCW08.pdf, `sources/S1-50/Avrahami-CSCW08.pdf`, SHA-256 `6b5bd5c26656e4725bfcd6b0370f2728d4ed2d2df4e11c172ec4656e6e5cae15`; both publisher-format PDFs, accessed 2026-10-01.
- **One observation.** Yes — one logging corpus (Trillian Pro plug-in): 16 participants in (a), extended to 19 in (b).
- **Machine/platform, subject, window named?** Platform: Trillian Pro on Windows, on participants' laptops (and one shared lab desktop). Subject: 8 Master's students (phase 1, from May 2005), 6 researchers + 2 interns of an industrial research lab (phase 2, from July 2005); (b) adds 3 start-up employees. Window: at least four weeks per participant, two for about three months.
- **Verbatim passages.**
  > "Our data were collected us ing a background process implemented as a custom plug- in module for Trillian Pro, a commercial IM client developed by Cerulean Studios [ 6], and running on the Windows operating system." ((a) Data Collection, PDF p.3, p.733)

  > "Participants were required to use Trillian Pro for all their IM interactions for a period of at least four weeks." ((a) PDF p.4, p.734)

  > "We collected a total of approximately 5200 hours of recorded data, observing over 90,000 incoming and outgoing instant messages. 73,906 messages from participants of phase 1 spread over 3,839 recorded hours, and 17,633 messages in phase 2 from 1355 hours of recordings." ((a) Data Overview, PDF p.5, p.735)

  > "Participants in the Students and Interns groups exchanged an astonishing average of 19.25 and 19.54 messages per hour recorded respectively. In other words, when Trillian was running, they exchanged, on average, a single message almost every 3 minutes! By comparison, the Researchers exchanged an average of 7.42 messages per hour, or a single message every 8 minutes." ((a) PDF p.5, p.735)

  > "Overall 16 31.7 15138.0 5195.2 324.7 8.2 28.2 91539 17.6 3.4" ((a) Table 1 row; columns: N, avg age, total hours in study, total hours recorded, avg hours recorded per participant, avg Trillian hours per day, avg active buddies, total msgs, avg msg per recorded hour, minutes per message; PDF p.5, p.735)

  > "Of the 45,468 incoming messages in our data, 3,805 were identified as SIA-5 and 3,161 as SIA-10" ((a) PDF p.6, p.736)

  > "In our data set, 92% of messages are responded to within 5 minutes (in fact, 50% of the messages in our data are responded to within 15 seconds)." ((a) PDF p.5, p.735)

  > "we collected a total of approximately 6,600 hours of recorded data, observing over 125,000 incoming and outgoing instant messages from 19 participants who communicated with a total of nearly 500 buddies (see [2] and [3] for other analyses of this data)." ((b) Participants, PDF p.4)
- **Coverage.**
  - T10 — covers: object = instant messages exchanged (incoming + outgoing) while the IM client runs; unit = messages per recorded hour; statistic = overall 17.6 per recorded hour (Students 19.2, Researchers 7.4, Interns 27.7 in Table 1; text gives 19.25 / 7.42 / 19.54), 45,468 incoming messages of 91,539; Trillian running 8.2 h per day on average; population = 16 (later 19) students and researchers in Pittsburgh-area settings; platform Windows; period 2005. Incoming-only per-hour rate not stated (reader's own arithmetic, not a value: 45,468 / 5,195 recorded hours ≈ 8.8 incoming messages per recorded hour).
  - T2 — partial: desktop focus features are logged (82 features) but not reported as dwell/switch statistics in the passages read.
  - T1, T3, T4, T6, T7, T9 — does not cover.
- **Side.** User-side.

### S1-51 — Isaacs 2002, logged workplace IM (Hubbub, 437 users, 16 months)

- **Citation.** Ellen Isaacs, Alan Walendowski, Steve Whittaker, Diane J. Schiano, Candace Kamm. 2002. The Character, Functions, and Styles of Instant Messaging in the Workplace. In *CSCW '02*, New Orleans, November 16–20, 2002, pp. 11–20. ACM.
- **Copy read.** https://www.interruptions.net/literature/Isaacs-CSCW02-p11-isaacs.pdf (publisher-format PDF; PDF p.n = printed p.10+n; the text layer has many spurious intra-word spaces), accessed 2026-10-01, `sources/S1-51/Isaacs-CSCW02-p11-isaacs.pdf`, SHA-256 `7398bc3ce8916a4656ed0044ad6340613975f6fe6dac3e63a0e7f180440242af`.
- **One observation.** Yes — one logged deployment of the Hubbub prototype, August 2000 – November 2001.
- **Machine/platform, subject, window named?** Platform: Hubbub prototype IM (client OS/devices not named in the paper; reference [8] describes it as a mobile messenger). Subject: 437 users who ran Hubbub ≥5 days and had ≥5 conversations, about half AT&T employees. Window: 16 months, August 2000 – November 2001.
- **Verbatim passages.**
  > "During the 1 6 months peri od between A ugust 2 000 and November 2001, 1,031 p eople r an Hub bub at least once, but many just tried it out an d never became regular users. Since ou r g oal was to u nderstand stable I M behavior, we included only users who ran Hubbub for at least five days (a business week) and had at least 5 conversations, leaving 437 users." (Method › Users, PDF p.3, p.13)

  > "This left a co rpus of 303,648 messages com prising 21,213 conversations between 692 pairs of users over the 16 months of the study." (Measures, PDF p.3, p.13)

  > "Overall, th e full g roup had an average of 6.2 people on their buddy list, and averaged 1.7 conversations per day. The range was broad, from 15.5 cpd for th e m ost activ e u ser to 0 .1 for th e least" (Frequency and Duration, PDF p.4, p.14)

  > "Conversations lasted an ave rage of 4 m in 23 secs, with a n exchange of 17.2 tu rns (or m essages). Each turn consist ed of an average of 13.5 words, with a turn gap of 24 seconds." (PDF p.4, p.14)

  > "The full gr oup of use rs moved o ut of the wi ndow an average of 3.8 times per conversation, about once every 70 seconds, and in 85.7% of the conversations at least one person multitasked." (Multitasking, PDF p.4, p.14)
- **Coverage.**
  - T10 — covers: object = IM conversations and messages; unit = conversations per active day, messages (turns) per conversation, turn gap; statistic = mean 1.7 conversations per day (range 0.1–15.5), 17.2 turns per conversation, 24 s turn gap; population = 437 users, mostly workplace; period Aug 2000 – Nov 2001. Reader's own arithmetic, not a value: 1.7 × 17.2 ≈ 29 messages exchanged per active day.
  - T2 — partial: focus moved out of the IM window 3.8 times per conversation, about once every 70 s (focus switching during IM conversations).
  - T1, T3, T4, T6, T7, T9 — does not cover.
- **Side.** User-side.

### S1-55 — Flautner 2001 (dissertation) / Flautner et al. 2000 (ASPLOS), thread-level parallelism of desktop applications incl. Linux and Quake 2

- **Citation.** Krisztián Flautner, *Automatic Monitoring for Interactive Performance and Power Reduction*, PhD dissertation, University of Michigan, 2001. Chapter 5 published as: K. Flautner, R. Uhlig, S. Reinhardt, T. Mudge, "Thread-level parallelism and interactive performance of desktop applications", ASPLOS-IX, 2000, pp. 129–138, DOI 10.1145/356989.357001.
- **Copy read.** (a) https://tnm.engin.umich.edu/wp-content/uploads/sites/353/2017/12/krisf.pdf (dissertation, 97 PDF pages), `sources/S1-55/flautner-dissertation-2001.pdf`, SHA-256 `eefa8d3e270cf200a6fd7b87df826c888d22cea433e936fad4d9c508795452b8`. (b) https://web.eecs.umich.edu/~tnm/trev_test/papersPDF/2000.8.Thread-level_parallelism_ASPLOS-IX.pdf (authors' copy headed "ASPLOS 2000 August 21, 2000", 10 pages), `sources/S1-55/flautner-asplos2000.pdf`, SHA-256 `f34a7fcc43365d568e7c48d16b36d697fa91e026a2f90e1d0ef0a860d34df085`. Accessed 2026-10-01.
- **One observation.** No — two lab observations by one group: (i) dissertation ch. 3, a survey of >50 applications on Windows NT, BeOS and Linux (Linux part: Red Hat 6.0, modified kernel 2.2.3, 4-way 500 MHz Pentium III, 512 MB), each workload one run; (ii) dissertation ch. 5 = the ASPLOS paper, six interactive Linux applications driven by a live user, seven runs each, on Linux Mandrake 7, modified 2.3.99-pre3 kernel, dual 450 MHz Pentium II, XFree86 3.3.6, Helix GNOME 1.2. The two documents of (ii) count as one source.
- **Machine/platform, subject, window named?** Machine, OS, kernel, application versions named; window = per-benchmark run length (e.g. Quake2 demo 20.01 s). Program-side values from Linux (1999–2000 kernels).
- **Verbatim passages.**
  > "Linux (kernel 2.2.3) implementation differs from the one for Windows NT in that instead of writing a device driver, we inserted the required calls into the kernel directly and added two system calls to control the measurement process." (dissertation, PDF p. 26 / printed p. 18, §3.2.1)
  > "The BeOS applications were run on BeOS 4.5.2 and we used the RedHat 6.0 distribution with our modified 2.2.3 kernel for Linux benchmarks." (dissertation, PDF p. 30 / printed p. 22, §3.3)
  > Table 3.5 "Linux benchmark results", rows "Make / gcc kernel src 69.11 82.18% 4.5% 13.2% 3.3% 7.1% 71.9% 3.44 1.92" and "Quake2 Demo 20.01 25.06% 0.1% 99.7% 0.3% 0% 0% 1.00 1.00" (columns: total time (s), MU, c0–c4, TLP4, TLP2) (dissertation, PDF p. 36 / printed p. 28)
  > "Linux is not a threaded operating system in the same sense as the Windows NT and BeOS. … Even applications that are threaded do not always use Linux’ ker- [Table 3.5 intervenes in the copy] nel threads; usually because of unresolved issues regarding the thread safety of standard libraries." (dissertation, PDF pp. 36–37 / printed pp. 28–29, §3.4.3)
  > "The only workload in our suite that exhibits a significant amount of TLP is the compiler benchmark, which uses parallel make to compile files concurrently." (dissertation, PDF p. 37 / printed p. 29)
  > "The Sysmark 98 [46] and Winstone 99 [49] benchmark sets provided a large number of applications for our initial observations. The advantage of these benchmark suites is that they consist of commercial applications that are driven by a GUI automation tool to achieve life-like behaviour." (dissertation, PDF p. 30 / printed p. 22, §3.3)
  > "Most Linux applications are not threaded; concurrency emerges from simultaneously running multiple processes. The only applications from our benchmarks that actually used threads (through the LinuxThreads API) were Netscape and GIMP. … most of the TLP was achieved by running the application thread concurrently with the user interface threads: mostly with the X server but also with the other GUI tasks (such as the window manager, desktop applets, etc.)." (ASPLOS copy, p. 7, §4.1)
  > "Task pids in the figure correspond to the following: 757 - X server, 778 - sawmill (window manager), 895 - gnome-termina l, 889 - tasklist_applet, 2088 - Ghostview (gv), 2090 - Ghostscript (gs)." (ASPLOS copy, p. 4, Figure 4 caption)
  > "We used a very simple MP3 player called mpg123 (version 0.59r) along with the esd sound daemon. … We measured 1.02 TLP and 95% idle time when running music playback by itself." (ASPLOS copy, p. 9, §4.4)
  > Table 1: "Average 1.31 1.27 89% 88%" (TLPie, TLPrun dual processor; Idlerun dual, uniprocessor) over Acroread 4.0, FrameMaker 5.5.6beta, Ghostview 3.5.8, GIMP 1.1.22, Netscape 4.7, Xemacs 21.1 (ASPLOS copy, p. 5)
- **Coverage.**
  - T1: covers, Linux program side — the set of processes co-running with one interactive application (X server, window manager sawmill, gnome-terminal, tasklist_applet, gv + gs) in one trace fragment; idle fraction 84–93% per application run; an MP3 player as the one background job studied. Lab, one user driving scripted actions, not real-user co-occurrence; 2000.
  - T2: does not cover.
  - T3: does not cover (Netscape 4.x / Mozilla M10 TLP only).
  - T4: covers, Linux program side, weakly — Quake 2 demo on Linux 2.2.3: TLP 1.00, one CPU busy 99.7% of non-idle time, MU 25.06% on 4 CPUs (one run, 20.01 s). No thread count or names for the game on Linux (the Linux table carries no thread column values). Native Linux game of 1997; no Wine/Proton, no Steam.
  - T6: covers, Linux program side — `make`/`gcc` kernel-source build with parallel make: 69.11 s, TLP 3.44 on 4 CPUs (one run; -j level not stated for the Linux run; the Windows/cygwin gzip build used `make -j 8`).
  - T7: covers existence only — SYSmark 98 and Winstone 99 described as commercial applications driven by a GUI automation tool; used on Windows NT.
  - T9: does not cover.
  - T10: does not cover.
- **Side.** Program-side values on Linux (old kernels): candidates. Windows NT and BeOS rows: context only.

### S1-56 — Blake et al. 2010, Evolution of thread-level parallelism in desktop applications (Windows 7 / OS X; context)

- **Citation.** Geoffrey Blake, Ronald G. Dreslinski, Trevor Mudge, Krisztián Flautner, "Evolution of Thread-Level Parallelism in Desktop Applications", ISCA 2010, pp. 302–313, DOI 10.1145/1815961.1816000.
- **Copy read.** https://tnm.engin.umich.edu/wp-content/uploads/sites/353/2017/12/2010.06.Evolution-of-Thread-Level-Parallelism.pdf, published version, 12 pages, `sources/S1-56/blake-isca2010.pdf`, SHA-256 `fa80ba994b65818a4efd82561e12c1ca1c034c711f65a39ad160ada9af8480a7`, accessed 2026-10-01.
- **One observation.** One lab study, each benchmark run by hand ≥5 times; Windows 7 Enterprise and OS X 10.6.2 on a 2009 Mac Pro (2× Xeon E5520, 6 GB, GTX285 or GT120).
- **Machine/platform, subject, window named?** Machine, OS, applications named; per-benchmark windows not stated in the extracted text.
- **Verbatim passages.**
  > Table 1 "Summary of number of threads created and average that were being used by a benchmark from each category of applications tested": "Handbrake 0.9 22511 24 / Call of Duty 4 77 44 / Photoshop CS4 82 75 / Adobe Reader 9 239 24 / Quicktime-HD 53 52 / Firefox 3.5 522 38" (columns Created, Avg Live) (PDF p. 3 / printed p. 304)
  > "Hardware Software 2009 Mac Pro OS X 10.6.2 2x Intel Xeon E5520 Snow Leopard 6GB RAM Dual boot NVIDIA GTX285 -or- Windows 7 NVIDIA GT120 Enterprise" (Table 2, PDF p. 3)
  > "Games were primarily single threaded until around 2005 when chip multi-processors were released on both PC and the current generation gaming consoles." (§4.1, PDF p. 4 / printed p. 305)
  > Table 3 row "Call of Duty 4 Windows 0% 12% 35% 20% 14% 8% 7% 2% 1% … 2.1 0.21 86%" (C0…C16, TLP, σ, GPU utilization) (PDF p. 6 / printed p. 307)
- **Coverage.** T1: context only (threads per desktop application, Windows/OS X). T4: context only — a Windows game's thread population: Call of Duty 4 created 77 threads, 44 live on average, TLP 2.1 (Windows 7). T6: context only (HandBrake 0.9 created 22,511 threads, 24 live on average). T7: does not cover. T2, T3, T9, T10: do not cover.
- **Side.** Program-side values on Windows/OS X → context, not candidates.

### S1-57 — Bircher & John 2008 (ICS) and Bircher 2010 (dissertation), SYSmark 2007 composition

- **Citation.** W. Lloyd Bircher, Lizy K. John, "Analysis of Dynamic Power Management on Multi-Core Processors", ICS 2008, DOI 10.1145/1375527.1375575; W. Lloyd Bircher, *Predictive Power Management for Multi-Core Processors*, PhD dissertation, The University of Texas at Austin, December 2010.
- **Copy read.** https://utw10244.utweb.utexas.edu/pubs/BircherICS2008.pdf (12 pages), `sources/S1-57/bircher-ics2008.pdf`, SHA-256 `915c0583bc330485db1e9646291c01bbdbacf199246ca920af0d72ffe4fb5f2f`; https://utw10244.utweb.utexas.edu/pubs/bircher_dissertation_20109.pdf (190 PDF pages), `sources/S1-57/bircher-dissertation-2010.pdf`, SHA-256 `d519f9242e78a36815865b0062966c266d73fabbd358d97abf778ef9e4367e9e`. Accessed 2026-10-01.
- **One observation.** Description of one benchmark (SYSmark 2007 Preview) as used in one author's power study on Windows Vista; two documents, one source.
- **Machine/platform, subject, window named?** Benchmark and its applications named; durations and input sizes not given.
- **Verbatim passages.**
  > "Additionally, we present data from the SYSmark 2007 benchmark suite. This suite represents a wide range of desktop computing applications. The major categories are: e-learning, video creation, productivity, and 3D. … it provides realistic user scenarios which include user input and think time." (ICS 2008, PDF p. 5, §3.4)
  > Table 3 "SYSmark 2007": "E-Learning 3D / Adobe® Illustrator® Autodesk® 3Ds Max / Adobe Photoshop® Google™ SketchUp / Microsoft PowerPoint® / Adobe Flash® / Productivity Video Creation / Microsoft Excel® Adobe After Effects® / Microsoft Outlook® Adobe Illustrator / Microsoft Word® Adobe Photoshop / Microsoft PowerPoint Microsoft Media Encoder / Microsoft Project® Sony Vegas / Winzip®" (ICS 2008, PDF p. 5)
  > "SYSmark 2007 [Sm07] is implemented using simulated user input through the application GUI (graphical user interface). The numerous delays required for GUI interaction causes many idle phases across the subsystems." (dissertation, PDF p. 39)
  > Table 7.1 "SYSmark 2007 Components" lists under Productivity "Corel - WinZip" (dissertation, PDF p. 143 / printed p. 127)
- **Coverage.** T7: covers existence — SYSmark 2007's four scenarios and their applications; an archive workload (WinZip, in Productivity) and a video transcode (Media Encoder, Sony Vegas, in Video Creation) exist; no backup, malware-scan, software-compile, game-download or ML-training workload is listed; concurrency inside a scenario, ordering, input sizes and durations not described. T1, T2, T3, T4, T6, T9, T10: do not cover.
- **Side.** Benchmark definition (existence only).

### S1-58 — Zhang & Wu 2022, CpsMark+ (abstract, highlights and graphical abstract only)

- **Citation.** Yue Zhang, Tong Wu, "CpsMark+: A scenario-oriented benchmark system for office desktop performance evaluation in centralized procurement via simulating user experience", *BenchCouncil Transactions on Benchmarks, Standards and Evaluations* 2(4):100084, October 2022 (online 2023-01-05), DOI 10.1016/j.tbench.2023.100084, CC BY-NC-ND.
- **Copy read.** Full text NOT read (ScienceDirect 403; see log). Read: Wayback snapshot https://web.archive.org/web/20230114130231id_/https://www.sciencedirect.com/science/article/pii/S2772485923000017 (article page with abstract, highlights, keywords), `sources/S1-58/cpsmark-sciencedirect-wayback-20230114.html.gz` SHA-256 `cc79bf837b460399e5e3e879b286ab33abd3c728803f6f5aaf984ca714c71461`, decompressed `…html` SHA-256 `63c919c0526b21a95bad7394783af5f2b837cbae723a42be0fbac5fc7636f135`; graphical abstract https://ars.els-cdn.com/content/image/1-s2.0-S2772485923000017-ga1_lrg.jpg, `sources/S1-58/cpsmark-graphical-abstract-lrg.jpg` SHA-256 `2fedcc29b02033e7e0b4b52fa5ceadd3d24741973fe1fc2efc38d95ec826e088`; its small version https://ars.els-cdn.com/content/image/1-s2.0-S2772485923000017-ga1.jpg (301×186 px, not used for reading), `sources/S1-58/cpsmark-graphical-abstract.jpg` SHA-256 `2e63d18b0b2048f375561a02b2d7652fb12e796c18f5f26272051ef78673e7ab`. Accessed 2026-10-01.
- **One observation.** A benchmark-definition paper with a comparison against SYSmark 2018 and PCMark 10 and one procurement case study; what was read is the summary only.
- **Machine/platform, subject, window named?** Not an observation of use: a benchmark definition; the machines of its comparison runs are not in the material read.
- **Verbatim passages.**
  > "CpsMark+ has high sensitivity and optimal repeatability under various hardware characteristics, compared to SYSmark 2018 and PCMark 10, two state-of-the-art computer benchmarks for commercial use." (Highlights)
  > "Specifically, CpsMark+ includes scenario-oriented workloads portraying representative user behaviors modeled from the cooperative workflow in modern office routines, and flexibly adapted metrics properly reflecting end-user experience according to different task types." (Abstract)
  > [transcribed from figure] Graphical abstract labels: "User Profile Abstraction" over "Task Workers", "Knowledge Workers", "Power Users"; "Usage Scenario Modeling": "Document Manupilation", "Internet Service", "Graphic Design", "Multimedia Processing"; "Master Control Program": "Comprehensive Application" (Workload 1 … Workload m) and "Comprehensive Calculation" (Workload 1 … Workload n), each ending in "Scoring"; "Input Files": "Document Files", "Image Files", "Video Files", "Webpage Files", "Compressed Files", "Application Specific Files".
- **Coverage.** T7: covers existence only, partially — CpsMark+ has four usage scenarios and two suites of workloads run in sequence (arrows in the figure); compressed files are among its inputs. Applications, concurrency inside a scenario, input sizes, durations and whether backup/malware-scan/compile/game-download/ML-training workloads exist are not in the read material. All other topics: do not cover.
- **Side.** Benchmark definition (existence only).

### S1-59 — Gao et al. 2014, thread-level parallelism on mobile devices (Android; context)

- **Citation.** Cao Gao, Anthony Gutierrez, Ronald G. Dreslinski, Trevor Mudge, Krisztián Flautner, Geoffrey Blake, "A Study of Thread Level Parallelism on Mobile Devices", ISPASS 2014 (2-page poster), pp. 126–127.
- **Copy read.** https://web.eecs.umich.edu/~tnm/trev_test/papersPDF/2014.03.A%20Study%20of%20Thread%20Level%20Parallelism%20on%20Mobile%20Devices.pdf, published version, `sources/S1-59/gao-ispass2014-tlp-mobile.pdf`, SHA-256 `1030f3d05f48239fe8c8e7814cf192d0cdbda22fe8559756e2463210f4dc57ad`, accessed 2026-10-01.
- **One observation.** One lab study, 20 Android apps, 30 s actions, ≥5 repetitions, ftrace context switches; Samsung Origen (Exynos 4412, quad Cortex-A9) and Qualcomm Dragonboard.
- **Machine/platform, subject, window named?** Machines named (Samsung Origen, Exynos 4412 quad Cortex-A9; Qualcomm Dragonboard); subjects named (20 Android applications); window: 30-s actions, ≥5 repetitions; Android, not a desktop.
- **Verbatim passages.**
  > "To calculate TLP, we collect all the context switch events using ftrace, a Linux kernel internal tracer." (p. 1, §II.A)
  > "The applications with high TLP, namely Games, Browser and Navigation, have TLPs around 1.5 to 1.6." (p. 1, §III)
- **Coverage.** T4: context only — mobile games' TLP ≈1.5–1.6 on Android (Linux kernel, but not a desktop; no thread counts or names). T1: context (multi-tasking runs with background apps, no co-occurrence data). Others: do not cover.
- **Side.** Program-side, Android → context.

### S1-60 — Endo et al. 1996, Using latency to evaluate interactive system performance (critique of desktop benchmarks)

- **Citation.** Yasuhiro Endo, Zheng Wang, J. Bradley Chen, Margo Seltzer, "Using Latency to Evaluate Interactive System Performance", OSDI '96, Seattle, October 28–31, 1996.
- **Copy read.** https://static.usenix.org/publications/library/proceedings/osdi96/full_papers/endo/endo.txt (USENIX plain-text version, ISO-8859-1), `sources/S1-60/endo-osdi1996.txt`, SHA-256 `cfe8263de8adac0647ec24ac9726f705c2efce0a5e452e9e14137ad3bd3f6c35`, accessed 2026-10-01.
- **One observation.** Argument plus measurements on Windows NT 3.51/4.0 and Windows 95 (100 MHz Pentium); the benchmark critique is a design argument, not an observation.
- **Machine/platform, subject, window named?** Machine and systems named (100 MHz Pentium; Windows NT 3.51/4.0, Windows 95); the benchmark suites are named by version (SYSmark NT, SYSmark 32, Winstone 95); no user population.
- **Verbatim passages.**
  > "Benchmarks such as Winstone, BAPCo SYSmark NT and BAPCo SYSmark 32 sacrifice portability in order to use popular interactive applications. … Although these benchmark suites use interactive applications and simulated interactive input, they report performance in terms of throughput metrics and suffer from the problems presented in Section 1.1. Non-trivial batch computations are sometimes included in these workloads when they are consistent with realistic usage of the application. Examples are circuit board layout in MAXEDA (BAPCo SYSmark NT) and database queries in Microsoft Access (Winstone 95). Although these benchmarks use realistic applications, the input streams used to drive them model an infinitely fast user." (§1.2 Related Work)
  > "However, the results of these benchmarks do not correlate directly with user-perceived performance-a critical metric when evaluating interactive system performance." (§1.1 The Irrelevance of Throughput)
- **Coverage.** T7: covers — critique of representativeness of SYSmark NT / SYSmark 32 / Winstone (old versions): no think time ("infinitely fast user"), throughput scoring; batch computations embedded in scenarios (circuit layout, database queries). Not about current SYSmark/PCMark/Procyon. Others: do not cover.
- **Side.** Benchmark design (existence/critique).

### S1-61 — Righi 2025, FOSDEM talk "Level up your Linux gaming: how sched_ext can save your fps" (conference talk; not peer-reviewed)

- **Citation.** Andrea Righi (NVIDIA), "Level up your Linux gaming: How sched_ext can save your fps", FOSDEM 2025, Kernel devroom, event fosdem-2025-4618 (slides + recording subtitle file).
- **Copy read.** Slides https://fosdem.org/2025/events/attachments/fosdem-2025-4618-level-up-your-linux-gaming-how-schedext-can-save-your-fps/slides/238583/Level_up_nKtb5A3.pdf (23 pages), `sources/S1-61/righi-fosdem2025-schedext-gaming.pdf`, SHA-256 `578962a1954c667f5159f5fa932d8b720547d9cec117ece020e1daa7b3a048c4`; subtitles https://video.fosdem.org/2025/ud2208/fosdem-2025-4618-level-up-your-linux-gaming-how-schedext-can-save-your-fps.vtt (automatic transcript, contains recognition errors), `sources/S1-61/righi-fosdem2025-schedext-gaming.vtt`, SHA-256 `5f204a717e3619cac872c34a6aeedb9cb9bcc908ce9871ee20f44b71f077b76e`. Accessed 2026-10-01.
- **One observation.** One presenter's perfetto trace of one (unnamed) game on a Linux desktop, normal vs. with a kernel build in the background, plus a live demo (Counter-Strike, Baldur's Gate 3, Cyberpunk) — machine, kernel, distribution not named.
- **Machine/platform, subject, window named?** Machine, kernel, distribution and the traced game not named; window: one trace under normal load and one with a kernel build in the background; talk at FOSDEM 2025.
- **Verbatim passages.**
  > "Gaming workload (normal condition) https://perfetto.dev Xwayland 16.6ms = 60fps Xwayland runs consistently every 16.6ms" (slide 9)
  > "Gaming workload (overloaded system) … Xwayland execution is inconsistent, missing the 16.6ms intervals" (slide 10)
  > "If I try to overload the system, this is, like, the same game, but with a kernel build running in the background." (VTT 07:51–08:02)
  > "So I'm building the kernel, while playing counter strike." (VTT 21:39–21:51); "And I'm building the kernel in background with make dash j, 30." (VTT 22:16–22:21); "So this is Baldur's Gate 3, another triple A game, 6 FPS without doing anything, of course." (VTT 22:21–22:29)
  > "You may have a system that runs the game, but there are other things running in the background. Let's say an update is starting the background." (VTT 24:32–24:41)
- **Coverage.** T4: covers, Linux program side, weakly — Xwayland (in the game's frame path) wakes once per 16.6 ms at 60 fps on a desktop; under a background `make -j30` kernel build the cadence fragments. No thread counts or names of the game. Machine, OS, game in the trace not named. T6: context — a user-started kernel build alongside a game is used as the stress scenario (demonstration, not usage data). Others: do not cover.
- **Side.** Program-side, Linux → candidate (grey literature).

### S1-62 — Min 2025, LPC talk "Steps Towards a Gaming-Optimized Scheduler" (conference talk; not peer-reviewed)

- **Citation.** Changwoo Min (Igalia), "Steps Towards a Gaming-Optimized Scheduler", Linux Plumbers Conference 2025 (Tokyo), Gaming on Linux microconference, December 13, 2025, contribution 2150.
- **Copy read.** https://lpc.events/event/19/contributions/2150/attachments/1951/4162/Steps_Towards_a_Gaming_Optimized_Schedule-lpc2025.pdf (15 pages), `sources/S1-62/min-lpc2025-gaming-scheduler.pdf`, SHA-256 `e478aa851e39c1d01e94e3b7bcbecaaf51310107c801b6c1821015ff57267059`. Figure images extracted from the PDF by the reader: `p7-task-runtimes.jpg` `aa0661925e83bfce3b5189d253bdc6c3c8a0c6288ce44deb6dcc8d861c12afb4`, `p7-per-task-stats.jpg` `4898df69cc20bb4db1a3673c236475ef95261e68983a3b01e2bfcc30f6cfed67`, `p7-callstacks.jpg` `9f9283664dae0828110aafaaee3e016e510ea362159b39bc5bb07d0365cb0a3a`, `p7-waker-waiter-graph.jpg` `0b48da75f8126e5ffc9e5e6434e1b761c06c0de9a3e49f5bab11ea774eb928fa`, `p8-task-graph.png` `0d3d6468fd7bef4da5ba2b558a6f3933d90ed222c55e8fc57f11363440a26461`. Accessed 2026-10-01.
- **One observation.** One `perf sched record` trace of one game under Wine/Proton analysed with VaporMark; game, machine, kernel and trace length not named on the slides.
- **Machine/platform, subject, window named?** Game, machine, kernel and trace length not named on the slides; the game is identifiable only through its thread names; talk of December 2025.
- **Verbatim passages.**
  > "Primary target: Windows games running on Linux (SteamOS)" (slide 2)
  > "VaporMark collects all the scheduling activities during a period using “perf sched record”" (slide 6)
  > "To accomplish a single high-level job (e.g., moving a character upon a keypress event), many tasks should tightly collaborate." (slide 8)
  > [transcribed from figure, slide 7 "Task's wait_time, sched_delay, and runtimes"] column headers "redDispatcher5[6349/6340]", "redDispatcher1[6345/6340]", "redDispatcher2[6346/6340]"
  > [transcribed from figure, slide 7 "Callstacks tiggered scheduling"] "sched_preempt (28.78%)", "ioctl (13.25%)", "alloc (7.95%)", "unlock (7.28%)", "syscall (6.76%)", "futex_wait (5.94%)", "fs_write (4.11%)", "lock (3.96%)", "fs_read (3.83%)", "pipe_write (3.69%)", "pipe_read (2.96%)", "futex_wake (2.23%)", "page_fault (1.57%)", "recvmsg (1.36%)", "poll (1.26%)", "futex (1.05%)"
  > [transcribed from figure, slide 7, "30.00 percentile of waker-waiter"] nodes "wineserver[5789/0]", "wine_xinput_hid[6597/6340]", "redDispatcher1[6345/6340]" … "redDispatcher7[6351/6340]"; edge labels e.g. "pipe_read (183350)" (wineserver → wine_xinput_hid), "epoll (121662)" (wine_xinput_hid → wineserver)
  > [transcribed from figure, slide 7, "40.00 percentile of waker-waiter"] adds "GameThread[6340/0]", "wine_sechost_se[5821/5806]", and a separate pair "perf[6675/0]" → "baloo_file[4302/0]" labelled "poll (58147)"
  > [transcribed from figure, slide 8 task graph] adds "GameThread[6356/6340]", "wine_sechost_se[5820/5806]", "wine_sechost_se[5809/5806]"; edges "futex_wait (31804)" etc. among redDispatcher threads
- **Reader's notes (not values).** The per-task plots on slide 7 ("Task statistics using per-task average": num_sched, num_mig, num_wake, num_wait) have a sorted x-axis running to roughly 125 tasks (reader's reading of the figure). The `[a/b]` labels look like [thread id / thread-group id] with 0 for a group leader — reader's interpretation, not stated. The "redDispatcher" naming suggests a REDengine title — reader's inference, the slides do not name the game. KDE's file indexer `baloo_file` and `perf` appear in the trace beside the game.
- **Coverage.** T4: covers, Linux program side — thread names (`comm`) of a game under Wine: a main "GameThread", seven "redDispatcher" workers, "wine_xinput_hid", "wine_sechost_se" (×3, separate process 5806), the "wineserver" process; which waits drive scheduling (72% non-preemption, by the pie); companion processes in the trace (baloo_file, perf); about 125 tasks in the per-task statistics (reader's reading). No Steam client process visible in the graphs shown; frame cadence not given. T1: covers weakly (KDE Baloo indexer running beside a game on a real Linux desktop/handheld). Others: do not cover.
- **Side.** Program-side, Linux → candidate (grey literature: talk slides by the LAVD scheduler author).

### S1-63 — Min 2026, talk "Optimizing the Linux Scheduler for Gaming and Large Servers" (LIG/Inria seminar; not peer-reviewed)

- **Citation.** Changwoo Min (Igalia), "Optimizing the Linux Scheduler for Gaming and Large Servers", talk at LIG (Laboratoire d'Informatique de Grenoble), April 27, 2026.
- **Copy read.** https://www.liglab.fr/sites/default/files/Mediatheque/scx_lavd-inria2026.pdf (39 pages), `sources/S1-63/min-inria2026-scx-lavd.pdf`, SHA-256 `c37a050e4760bbaab71ee67e3e9260183c07c2bf8db9a524d8882aff501562cc`; extracted figure images `p12-runtime-avg.jpg` `e3bd3ba6fc4870fe94c71ba06c640f16d7cca00df996bf510263d7935cb2587c`, `p14-task-graph.png` `bdaa20d5ef286ad88880e569186773dda24d98bd5b9874572ed97a3e54d536b9`. Accessed 2026-10-01.
- **One observation.** One VaporMark trace of a game under Wine/Proton (slide 14: Troy.exe, i.e. a Windows executable); possibly overlapping with S1-62 for slides 12–13 (the slides do not say which trace). Machine and kernel not named on these slides (slide 28 says "Demo on SteamDeck"; slides 29–30 a Snapdragon board).
- **Machine/platform, subject, window named?** Game executable named (Troy.exe); machine and kernel of that trace not named; trace length not named; talk of April 2026.
- **Verbatim passages.**
  > "In general, tasks run for very short duration – roughly a few 100s usec on average to a few msec maximum." … "Some coordination tasks run very shortly (e.g., wineserver:260 usec) but some work tasks (e.g., a task worker: 1.65 msec) run longer than average." (slide 12, "Distribution of task's runtime average per schedule in a game")
  > "Preemption (e.g., timer interrupt) takes only 25-30% of scheduling." "70-75% of scheduling is initiated by waiting system calls – such as epoll, pipe_read, futex_wait , etc." (slide 13)
  > [transcribed from figure, slide 14 "Task graphs of top 50 percentile of waiter-wakers"] nodes "Troy.exe[7781/0]", "wineserver[7256/0]", "explorer.exe[7301/0]", "winedevice.exe[7284/7273]", "Task worker thr[7825/7781]", "Task worker thr[7826/7781]", "Task worker thr[7827/7781]", "Task worker thr[7828/7781]", "dxvk-cs[7922/7781]", "dxvk-submit[7920/7781]", "winepulse_mainl[7991/7781]", "winepulse_timer[7993/7781]", "FAudio_AudioCli[7992/7781]", "CSteamControlle[4908/4788]", "pipewire-pulse[1703/0]", "pipewire-pulse[1707/1703]", "pipewire[1214/1204]", "swapper[0/0]"; edges e.g. "epoll (134200)" (Troy.exe → wineserver), "futex_wait (30970)" (dxvk-cs → dxvk-submit)
- **Reader's notes.** The runtime_avg figure on slide 12 has a sorted x-axis to roughly 128 tasks (reader's reading). "CSteamControlle" is a 15-character `comm` (truncated) in thread group 4788, i.e. a Steam-client thread — reader's inference from the name.
- **Coverage.** T4: covers, Linux program side — a Proton game's thread names (`comm`): game main thread, 4 "Task worker thr", DXVK "dxvk-cs"/"dxvk-submit", Wine audio "winepulse_mainl"/"winepulse_timer", "FAudio_AudioCli"; Wine processes wineserver, explorer.exe, winedevice.exe; companions PipeWire, pipewire-pulse and a Steam-client thread; per-task mean runtime per scheduling (wineserver 260 µs, task worker 1.65 ms); 70–75% of scheduling from blocking syscalls. T1: weakly (PipeWire and Steam client beside a game). Others: do not cover.
- **Side.** Program-side, Linux → candidate (grey literature).

### S1-64 — Gegout et al. 2025, Towards an efficient containerized cloud gaming platform

- **Citation.** Adrien Gegout, Djob Mvondo, Davide Frey, Pascal Monchon, "Towards an Efficient Containerized Cloud Gaming Platform", AsHES – IPDPS 2025 Workshops, IEEE, June 2025, Milano, pp. 78–86, DOI 10.1109/IPDPSW66978.2025.00018, HAL hal-05094575v1 (CC BY 4.0).
- **Copy read.** https://hal.science/hal-05094575/file/AsHES_2025_Containerized_Cloud_Gaming.pdf (HAL deposit of 2025-06-03, 10 pages), `sources/S1-64/gegout-ashes2025-containerized-cloud-gaming.pdf`, SHA-256 `7858b66b5117c638c2f4bc8ca1ea9c26a7f820ad6e8ebf9f3a89484123561d80`, accessed 2026-10-01.
- **One observation.** One server testbed (AMD EPYC 7502P, Nvidia T4, Ubuntu 22.04 host and containers), four Windows games at fixed FPS presets.
- **Machine/platform, subject, window named?** Machine named (AMD EPYC 7502P, Nvidia T4, Ubuntu 22.04 host and containers, 8 vCPU and 10 GiB per instance); subjects named (four Windows games under wine-GE and DXVK); server side, not a desktop.
- **Verbatim passages.**
  > "In our game container, we install all libraries and software needed to adequately run a Windows game inside a Linux environment: (1) "wine-GE-custom" [42] of the open-source Wine project [43], [44] to simulate Windows system API calls inside a Linux system, (2) "DXVK" [50] and "DXVK NvAPI" [51], … (3) "VkD3D" [52], [53] … and (4) MangoHud [54] for debugging and for collecting game-layer telemetry." (PDF p. 5, §III)
  > "The streaming container embeds all the libraries and software needed to run the Cloud-gaming provider's streaming components (e.g. Gstreamer [55] dependencies) and to build a minimal graphical interface for games, including an X11 or Wayland graphical server bound to the GPU driver and a PulseAudio server." (PDF p. 5)
  > "The container and VM instances are configured with a limited cpuset of 8 vCPU (4 physical cores) each and limited to 10 GiB of RAM each. The server host runs Ubuntu 22.04 …" (PDF p. 5)
- **Coverage.** T4: covers existence only — what runs beside a Wine game in a server-side cloud-gaming instance (X11/Wayland server, PulseAudio, GStreamer streaming, MangoHud); no process/thread counts, names or busy threads; not a desktop. Others: do not cover.
- **Side.** Program-side, Linux, but existence-level only.

### S1-65 — Chambers et al. 2005, measurement-based characterization of on-line games (Steam CDN patch delivery)

- **Citation.** Chris Chambers, Wu-chang Feng, Sambit Sahu, Debanjan Saha, "Measurement-based Characterization of a Collection of On-line Games", Internet Measurement Conference (IMC) 2005, USENIX.
- **Copy read.** HTML version https://static.usenix.org/events/imc05/tech/full_papers/chambers/chambers_html/node2.html (`sources/S1-65/chambers-imc2005-node2.html`, SHA-256 `0675d26e1ac809acf01a85312340ce81affcecfafce12a9822a0fafaedd0a0c0`), node17.html (`…node17.html`, `4de51bb734339b552d56647dc2b11a576afccd3336e6558830194b9b26702c7b`), node18.html (`…node18.html`, `58a0787c5bb924f08739e4aeb1f72bdc8dabe137f28cb353b151bb924abbb2cd`); PDF https://www.usenix.org/legacy/event/imc05/tech/full_papers/chambers/chambers.pdf (`…chambers-imc2005.pdf`, `6d9dea3b145f9513917b82a636702d966286bb3a17734c53280067d7be0a0c3a`; text extraction garbled, quotes taken from the HTML). Accessed 2026-10-01.
- **One observation.** Yes for the Steam part — one CDN trace, Mon Sep 27 2004 – Mon Apr 8 2005, 6,193 TB transferred, Valve's Steam network (Half-Life and mods).
- **Machine/platform, subject, window named?** Platform: Valve's Steam content-delivery network (server side), client operating systems not distinguished; subject: Steam content (Half-Life and mods); window named (27 Sep 2004 – 8 Apr 2005).
- **Verbatim passages.**
  > "Steam CDN trace Start time Mon Sep 27 2004 End time Mon Apr 8 2005 Content transferred 6,193 TB Average transfer rate 3.14 Gbs" (Table 1, Methodology)
  > "Players are authenticated to Steam for each game session, via the download of an authentication module. Content is distributed to players (and servers) via Steam at irregular intervals and irregular sizes." (§ "Game updates significantly impact resource usage")
  > "By integrating these two signals and subtracting, we estimate the patch burden on Steam for this patch to be 129.7 terabytes, which is 30% of that week's total load including authentication." (same section)
  > "the cumulative distribution function (CDF) of the patch delivery data in Figure 18 shows that 80% of the load occurs in the first 72 hours for the three single-patch traces, whereas the various patches in trace p7 are delivered throughout a two-week period." (same section)
- **Coverage.** T4: covers partially — when Steam downloads game updates in aggregate: patch delivery concentrated after release (80% of patch bytes within 72 h, three single-patch traces); per-session authentication-module download (2004–2005 Steam). Does not cover whether downloads happen during play, the client's default settings, or per-client timing. Others: do not cover.
- **Side.** Platform-level observation of Steam's content delivery (neither a desktop program's own work nor a user choice); platform of clients not distinguished.

### S1-66 — Lin, Bezemer & Hassan 2017, Studying the urgent updates of popular games on the Steam platform

- **Citation.** Dayi Lin, Cor-Paul Bezemer, Ahmed E. Hassan, "Studying the Urgent Updates of Popular Games on the Steam Platform", *Empirical Software Engineering* 22(4):2095–2126, 2017.
- **Copy read.** http://asgaard.ece.ualberta.ca/papers/Journal/EMSE_2017_Lin_Studying_the_Urgent_Updates_of_Popular_Games_on_the_Steam_Platform.pdf (author manuscript, "Noname manuscript"), `sources/S1-66/lin-emse2017-urgent-updates-steam.pdf`, SHA-256 `756bf78dca8cfd126ffeeea4f3a46d0066e2f939dfda68f106b4d6269eba9d57`, accessed 2026-10-01.
- **One observation.** Yes — one crawl of 11,970 Steam news posts → 2,672 update notes of the 50 most popular Steam games (player counts as of Jan 12, 2016; timelines 2013–2016).
- **Machine/platform, subject, window named?** Platform: Steam (release notes, independent of operating system); subjects named (the 50 most popular games by player count on 12 Jan 2016); window: update notes 2013–2016.
- **Verbatim passages.**
  > "The Steam client will verify ownership of the game and automatically install any available updates. It is mandatory to install the latest update in order to play a game through Steam." (PDF p. 3, §2)
  > "An update to Team Fortress 2 has been released. The update will be applied automatically when you restart Team Fortress 2." (Table 3, PDF p. 10)
  > "We identify 2,672 update notes for the 50 studied games." (PDF p. 10)
  > "Table 5 shows that 20 out of 45 (44%) studied games have a median days-between-updates that is equal to or less than 7 days, i.e., at least 50% of the updates of these games are released within a week after the previous update. Moreover, in 81% of the studied games, at least one of the modes of the days-between-updates is smaller than 7" (PDF p. 15, §4.1)
- **Coverage.** T4: covers partially — how often popular Steam games ship updates the client must download (44% of 45 games: median gap ≤7 days; lower bound from published notes); the client installs updates automatically and an update is applied when the game restarts (statement by the authors and a Valve update note — existence, not an observation of client timing). Does not cover downloads during play. Others: do not cover.
- **Side.** Platform-level (release cadence); OS-independent.

### S1-67 — Alsmadi et al. 2024, "Give Me Steam": memory forensics of the Steam Deck (process list before and during a game)

- **Citation.** Ruba Alsmadi, Taha Gharaibeh, Andrew M. Webb, Ibrahim Baggili, "Give Me Steam: A Systematic Approach for Handling Stripped Symbols in Memory Forensics of the Steam Deck", ARES 2024, Vienna, July 30–August 2, 2024, DOI 10.1145/3664476.3670903, CC BY 4.0.
- **Copy read.** Wayback capture https://web.archive.org/web/20241108012224id_/https://dl.acm.org/doi/pdf/10.1145/3664476.3670903 (ACM published PDF, 10 pages), `sources/S1-67/alsmadi-ares2024-give-me-steam.pdf`, SHA-256 `7ecc02d59d4e97eefb82282b23c95202fffe1867da2a3738a88e112931f438b5`; page 6 rendered by the reader with macOS `sips` to read Figure 6: `sources/S1-67/page6-render.png`, SHA-256 `e57434f850cc9076f399795f076013494acddbcdbc08606a67b80a30404f6b43`. Accessed 2026-10-01.
- **One observation.** Yes — two LiME memory dumps of one Steam Deck (SteamOS 3.0, kernel 6.1.52-valve16), one before and one during a game (game not named), analysed with Volatility 3 `linux.pslist`.
- **Machine/platform, subject, window named?** Machine named (Steam Deck, SteamOS 3.0, kernel 6.1.52-valve16); subject: one game, not named; window: two memory snapshots, before and during play.
- **Verbatim passages.**
  > "Steam Deck𝑒 SteamOS 3.0 Gaming console" (Table 1, PDF p. 2)
  > "We took two memory dumps: one before and one after playing games." (PDF p. 4, §4.1)
  > "In our case, we captured two memory dumps, one before and one during the game. Figure 6 shows how the number of processes by category changed before and after playing a game. … User and Steam categories experienced a noticeable increase in processes." (PDF p. 6, §5)
  > "following are the unique processes (game-related) that can be found in Steam deck memory dumps: • steam-runtime-s: … • srt-bwrap: Another component of the Steam Runtime. • pressure-vessel: Compatibility tools to run games in individual game-specific containers • steamwebhelper: Handles web-related tasks for Steam, such as displaying browser overlays or handling web content. • gamescope-session: Part of the Gamescope Wayland compositor used for optimizing the gaming environment. • gamescope-wl: Another component of the Gamescope Wayland compositor. • powerbuttond: Handles power button events. • mangoapp: Displaying an overlay with real-time performance metrics in games, such as CPU and GPU usage." (PDF p. 6)
  > [transcribed from figure, Figure 4] pslist header "OFFSET (V) PID TID PPID COMM File output" (PDF p. 5)
- **Reader's reading of Figure 6 (locates, not a value).** Before → after: System ≈109 → ≈110, User ≈35 → ≈45, Steam ≈1 → ≈8, Network 5 → 5, Other 7 → 7 processes.
- **Coverage.** T4: covers, Linux program side — processes present beside a running game on a Steam Deck (Steam runtime/pressure-vessel container, steamwebhelper, gamescope session and Wayland compositor, mangoapp overlay, powerbuttond) and the change in process count by category (≈+17 total, reader's reading). Process level only (pslist lists thread-group leaders), no thread counts, no busy threads; Steam Deck, not a desktop; the list mixes `comm`-truncated names ("steam-runtime-s") with untruncated ones ("gamescope-session"). T9: does not cover (no timing). Others: do not cover.
- **Side.** Program-side, Linux → candidate.

### S1-68 — Eichhorn, Schneider & Pugliese 2024, "Well Played, Suspect!" forensic examination of the Steam Deck (existence of Steam logs)

- **Citation.** Maximilian Eichhorn, Janine Schneider, Gaston Pugliese, "Well Played, Suspect! – Forensic examination of the handheld gaming console "Steam Deck"", *Forensic Science International: Digital Investigation* 48 (2024) 301688 (DFRWS EU 2024), DOI 10.1016/j.fsidi.2023.301688, CC BY-NC-ND.
- **Copy read.** CISPA repository copy (publisher PDF "1-s2.0-S266628172300207X-main.pdf") https://ndownloader.figshare.com/files/49358884, `sources/S1-68/eichhorn-dfrws2024-steam-deck.pdf`, SHA-256 `113d67c14a935d4db7845a4ecd8ce09d0c566fb400ddb3a8a5995c4a54ef7a36`, accessed 2026-10-01.
- **One observation.** Differential disk-image analysis of one Steam Deck under scripted action sets (install and play CS:GO, chat, voice chat, …).
- **Machine/platform, subject, window named?** Machine named (one Steam Deck); subjects named (scripted action sets such as installing and playing CS:GO, chat, voice chat); window: per action set.
- **Verbatim passages.**
  > "logs/appinfo_log.txt Installs and updates of Steam apps … logs/content_log.txt Steam app names & IDs, uninstalls … logs/durationcontrol_log.txt Begin of playing games" (Table 3, PDF p. 5)
  > "timestamps of when games have been started (σ3) are logged in the durationcontrol_log.txt file … the appinfo_log.txt file logs which games have been installed or updated" (PDF p. 8, §5.2.10)
- **Coverage.** T4: existence only — the Steam client on SteamOS keeps logs that timestamp game starts and app installs/updates, a route to observing whether updates coincide with play; no such observation reported. Others: do not cover.
- **Side.** Existence (program artefacts on Linux).

### S1-80 — Joo 2011, FAST: quick application launch on SSDs

- **Citation:** Yongsoo Joo, Junhee Ryu, Sangsoo Park, Kang G. Shin. "FAST: Quick Application Launch on Solid-State Drives." *9th USENIX Conference on File and Storage Technologies (FAST '11)*, San Jose, CA, February 2011.
- **Copy read:** https://kabru.eecs.umich.edu/rtclweb/assets/publications/2011/fast11_final.pdf (authors' group copy of the camera-ready paper, 15 pages; HTTP 200), accessed 2026-10-01; `sources/S1-80/joo2011-fast.pdf`; SHA-256 `482413c772c4d0d6b6f022a3291ef796854efcdad3db677ba27aff2ce5fba38b`. Text extracted with pypdf to `joo2011-fast.pdf.txt` (figure labels in Figure 6 are glyph-encoded in the text layer and cannot be read).
- **One observation:** yes — one lab desktop, a fixed benchmark set of 22 applications, each launched repeatedly under cold start (page cache flushed), warm start and with prefetchers; block-level traces with blktrace.
- **Machine/platform, subject, window named:** machine named (Intel i7-860 2.8 GHz, 4 GB DDR3, Intel X25-M 80 GB SSD; Fedora 12, Linux 2.6.32, NOOP I/O scheduler); subjects named (application list below, versions not given); window: one launch per run, publication 2011.
- **Verbatim passages:**
  > "We used a desktop PC equipped with an Intel i7-860 2.8 GHz CPU, 4GB of PC12800 DDR3 SDRAM and an Intel 80GB SSD (X25-M G2 Mainstream). We installed a Fedora 12 with Linux kernel 2.6.32 on the desktop, in which we set NOOP as the default I/O scheduler." (p. 8, §5.1)

  > "Our benchmark set consists of the following Linux applications: Acrobat reader, Designer-qt4, Eclipse, F-Spot, Firefox, Gimp, Gnome, Houdini, Kdevdesigner, Kdevelop, Konqueror, Labview, Matlab, OpenOffice, Skype, Thunderbird, and XilinxISE. In addition to these, we used Wine [1], which is an implementation of the Windows API running on the Linux OS, to test Access, Excel, Powerpoint, Visio, and Word—typical Windows applications." (p. 8, §5.1)

  > "Cold start: The application is launched immediately after flushing the page cache" (p. 8, §5.1, test scenarios)

  > "Table 3: Collected launch sequences (Nrawseq = 2) … Eclipse 4163 155 216 787 … Firefox 1566 60 944 433 … Gimp 1939 66 928 799 … Gnome 4739 228 872 538 … OpenOffice 1425 104 600 308 … Skype 892 41 560 197 … Thunderbird 1533 64 784 429" (p. 9, Table 3; columns: number of block requests, number of fetched blocks, number of used files; the fetched-blocks column prints with a thousands space, so Firefox's row reads 1,566 requests, 60,944 blocks, 433 files)

  > "the first raw input request sequence includes a set of bursty I/O requests generated by OS and user daemons that are irrelevant to the application launch." (p. 9)

  > "we investigated the SSD's maximum idle time during the cold-start of applications, and found it to range from 24 ms (Thunderbird) to 826 ms (Xilinx ISE). … As the maximum cold-start launch time is observed to be less than 10 seconds" (p. 12)

  > "The average cold start time of the smartphone applications is 6.1 seconds, which is more than twice of the average cold start time of the PC applications (2.4 seconds) shown in Figure 6." (p. 12)

  > "1.6s 0.8s 1.9s 4.8s 2.1s 1.1s 0.9s 2.3s 2.6s 5.6s 1.8s 1.6s 1.2s 2.7s 5.1s 0.9s 1.9s 1.0s 1.0s 3.7s 2.6s 6.6s" (p. 10, Figure 6 "Measured application launch time (normalized to tcold)", text layer: the absolute cold-start times printed above the bars; the bar labels are glyph-encoded, so which application each time belongs to cannot be read)
- **Coverage:**
  - T9: covers — launch work of Linux desktop applications at a cold start: block requests, blocks fetched and files used per launch (Table 3, per application), cold-start launch time (mean 2.4 s over the set; maximum under 10 s), on one Fedora 12 desktop with SSD, 2010–2011. Launch defined as until the GUI is ready for interaction; does not cover what the application does in the minutes after launch (cache warm-up beyond launch, first sync) nor how often users launch.
  - T1, T2, T3, T4, T6, T7, T10: do not cover.
- **Side:** program-side value from a Linux observation (candidate). The five Office applications run under Wine on Linux; still a Linux observation.

### S1-81 — Esfahbod 2006, Preload: an adaptive prefetching daemon (MSc thesis)

- **Citation:** Behdad Esfahbod. *Preload — An Adaptive Prefetching Daemon.* Master of Science thesis, Graduate Department of Computer Science, University of Toronto, 2006.
- **Copy read:** https://cs.uwaterloo.ca/~brecht/courses/epfl/Possible-Readings/prefetching-to-memory/preload-thesis.pdf (course-reading copy of the thesis; HTTP 200), accessed 2026-10-01; `sources/S1-81/esfahbod2006-preload-thesis.pdf`; SHA-256 `6cf04282c0faa3d94e91fb551d4caac95c782c9d2af6ffd272c7bdadc5fffa15` (81 pages per pypdf).
- **One observation:** two observations in one document — (a) start-up-time runs of five GNOME applications on one laptop-class machine (≈5 trials each, cold/warm/preload); (b) a two-week normal-use run of a modified preload under two usage scenarios (single user; two users GNOME and KDE) reporting hit ratios only.
- **Machine/platform, subject, window named:** machine named (Pentium M 1.7 GHz, 512 MB RAM, 4500 RPM 60 GB HDD; Fedora Core 5, Linux 2.6.17-1.2139 FC5); subjects named (OpenOffice.org Writer, Firefox, Evolution, Gedit, GNOME Terminal; versions not given); window: two weeks for the hit-ratio run, 2006.
- **Verbatim passages:**
  > "the time from launching the application until the application window is fully exposed. The start-up time is measured by modifying the source code of the program to print out the time of day once as the first operation in main(), and another time in an idle callback called from the main loop of the application." (p. 54, §6.1.1)

  > "Application cold warm preload gain # Maps size / OpenOffice.org Writer 15s 2s 7s 53% 323 90 MB / Firefox Web Browser 11s 2s 5s 55% 288 38 MB / Evolution Mailer 9s 1s 4s 55% 308 85 MB / Gedit Text Editor 6s 0.1s 4s 33% 216 52 MB / Gnome Terminal 4s 0.4s 3s 25% 184 27 MB / Table 6.1: Application start-up time with cold and warm caches, and with preload" (p. 56, Table 6.1)

  > "Boot time 95s 103s / Login time 30s 23s / Total time 125s 126s / Table 6.2: Boot and login times with and without preload" (p. 57, Table 6.2)

  > "Under a warm cache there are only five system calls (out of about 4900) lasting more than a millisecond, for a total of 10 milliseconds." (p. 59, §6.3.1, Gnome Terminal start-up under strace -T)

  > "We have performed all of the experiments on a system with an Intel Pentium M 1.7 GHz processor with 2 MB of CPU cache, 512 MB of main memory, and a 4500RPM 60GB hard-disk drive. The operating system used is a stock Fedora Core 5 distribution, with Linux kernel version 2.6.17-1.2139 FC5" (p. 55, §6.1.2)

  > "our training data stream is fairly low-frequency too, in the rate of zero or a few application start-ups per minute, if not per hour." (p. 25, §3; an author's characterisation, no logged count behind it)

  > "a single-user scenario with a single user using the system for her day-to-day computer uses (email, web, document processing, instant messaging, and games)" (p. 55, §6.1.1)
- **Coverage:**
  - T9: covers — start-up time (cold, warm) of five Linux desktop applications, number of mapped files at start-up and their size, system-call time at start-up (Gnome Terminal ≈4,900 system calls), boot and login times; one machine, Fedora Core 5, 2006. Launch rate: only an unmeasured characterisation ("zero or a few application start-ups per minute, if not per hour"); the two-week usage run reports hit ratios, not launch counts.
  - T1: does not cover (the usage scenarios are described in words; no co-occurrence counts).
  - T2, T3, T4, T6, T7, T10: do not cover.
- **Side:** program-side values from a Linux observation (candidate); the launch-rate sentence is user-side but not an observation.

### S1-82 — Ryu 2023, Paralfetch: fast application launch on personal computing devices

- **Citation:** Junhee Ryu, Dongeun Lee, Kang G. Shin, Kyungtae Kang. "Fast Application Launch on Personal Computing/Communication Devices." *21st USENIX Conference on File and Storage Technologies (FAST '23)*, 2023.
- **Copy read:** https://rtcl.eecs.umich.edu/rtclweb/assets/publications/2023/fast23-ryu.pdf (authors' group copy, 15 pages; HTTP 200), accessed 2026-10-01; `sources/S1-82/ryu2023-paralfetch-fast23.pdf`; SHA-256 `1fc0e56c218b460b53ee98eb4e00d99efd4ff36f3b77ae9afc0c3f1723433ef6`.
- **One observation:** yes for the PC part — one laptop, 16 applications (10 desktop applications, 6 games) launched under cold, warm and prefetched conditions; the Raspberry Pi and Android parts are separate observations in the same paper.
- **Machine/platform, subject, window named:** machine named (laptop, Intel Core i5-8265, 16 GB RAM, 1 TB Samsung 860 QVO QLC SSD, Linux kernel 5.4.51; Table 1 labels the platform "Ubuntu Linux (Laptop PC)", release not given); subjects named, versions not given; window: one launch, launch defined from `load_elf_binary` to completion of the last launch block request.
- **Verbatim passages:**
  > "A cold start occurs when the disk cache does not hold any data required by the app, either because it is the first time the app has been launched, or because all of the app's data has been evicted since its last run. A system cold start is a special case of cold start, which occurs when no user-launched app is already running. A warm start occurs when the app being launched has been running recently" (p. 1, §1)

  > "Table 1: Metadata and data block requests required to launch applications … Ubuntu Linux (Laptop PC) / Android Studio 1,330 (6,844) 3,845 (197,932) 58 954 10 38 / Chromium Browser 612 (3,048) 1,135 (130,728) 37 629 108 34 / Eclipse 565 (3,348) 1,669 (67,256) 28 744 328 49 / GIMP 489 (2,620) 1,026 (38,512) 20 975 474 28 / LibreOffice Impress 590 (2,900) 706 (83,004) 37 438 232 32 / LibreOffice Writer 552 (2,800) 729 (83,824) 25 476 227 33 / Okular 1,093 (5,720) 426 (23,640) 41 349 238 36 / Scribus 840 (5,984) 1,560 (141,056) 35 1,230 682 21 / VLC Player 682 (5,420) 444 (20,192) 41 375 104 32" (p. 4, Table 1; columns: metadata accesses (KB), file-data accesses (KB), missing metadata blocks detected, regular files, mmaped files, missing I/Os)

  > "Since usually many user and system processes run in the background, this issue can significantly degrade tracing accuracy. For example, 225 files of this kind were accessed by both LibreOffice Impress and LibreOffice Writer (on a laptop) during a launch of either." (p. 4, §3.1)

  > "case of Linux, the launch is deemed to start when the load_elf_binary function is called, and to finish when the completion block request has itself completed." (p. 10, §5.1)

  > "We conducted experiments on a laptop PC equipped with an Intel Core i5-8265 CPU and 16 GB of RAM, running Linux kernel 5.4.51. This PC has a 1 TB Samsung 860 QVO QLC SSD … We tested Paralfetch, GSoC Prefetch and FAST on 16 applications, 6 of which were games. The 10 non-game applications were Android Studio, Chromium Browser, Eclipse, GIMP, LibreOffice Impress, LibreOffice Writer, Okular, Scribus, VLC player, and Xilinx ISE; and the 6 games were Ancestors Legacy, Atom RPG, Battle Tech, Pillars of Eternity 2, Tyranny, Witcher 3." (p. 10, §5.2)

  > "Android Studio / Chromium Browser / Eclipse GIMP Libreoffice Impress / Libreoffice Writer / Okular Scribus VLC player Xilinx ISE Ancestors Legacy / Atom RPG / Battle Tech / Pillars of Eternity 2 / Tyranny Witcher 3 Average … 11.7s 2.0s 5.4s 2.5s 2.3s 2.1s 1.6s 3.8s 1.4s 7.2s 8.2s 15.6s 23.0s 32.0s 17.7s 14.0s" (p. 10, Figure 10 "Launch times on a laptop equipped with a QLC SSD, normalized to cold start times", text layer: the application labels, then the absolute times printed above the cold-start bars; pairing each time with an application by position is the reader's own reading)
- **Coverage:**
  - T9: covers — launch I/O work per application on Linux (metadata and data read requests and KB, files and mmaped files touched per launch, Table 1) and cold launch time per application (≈1.4 s VLC to 11.7 s Android Studio for desktop applications; 8–32 s for games, Figure 10 by position), one laptop, kernel 5.4.51, ≈2022. Launch only; nothing on work in the minutes after the window appears, nor launch rates.
  - T4: does not cover (launch time of six games, but no process/thread population; whether Witcher 3 and Ancestors Legacy ran under Wine/Proton is not stated).
  - T1, T2, T3, T6, T7, T10: do not cover.
- **Side:** program-side values from a Linux observation (candidate).

### S1-83 — Cichocki 2023, Flatpak and Snap comparison (start-up time)

- **Citation:** Grzegorz Jan Cichocki, Sławomir Wojciech Przyłucki. "Analiza porównawcza menedżerów pakietów Flatpak i Snap wykorzystywanych do dystrybucji oprogramowania o otwartym kodzie" (Comparative analysis of package managers Flatpak and Snap used for open-source software distribution). *Journal of Computer Sciences Institute* 29 (2023) 405–412. CC BY-SA 4.0.
- **Copy read:** https://ph.pollub.pl/index.php/jcsi/article/download/4587/4278/21968 (publisher PDF, 8 pages; HTTP 200), accessed 2026-10-01; `sources/S1-83/jcsi-flatpak-snap.pdf`; SHA-256 `15b825daa887858fadc1d81e37be8dd3a242ee0a35c02c2682cf48e40ca321fa`. Text is Polish; passages below are verbatim Polish with the reader's translation in brackets.
- **One observation:** yes — one laptop, one purpose-built test application ("Tabela", Python + Qt 6/PySide6) installed as Flatpak and as Snap, launched repeatedly, first launch directly after boot.
- **Machine/platform, subject, window named:** machine named (Intel Core i7-1165G7, Intel Iris Xe, 16 GB LPDDR4X, Toshiba KXG60ZNV1T02 NVMe 1 TB, Ubuntu 23.04); subject named (the authors' own test application, not a real desktop application); number of launches not stated in the passages read.
- **Verbatim passages:**
  > "Procesor: Intel Core i7-1165G7. … Pamięć operacyjna RAM: 16 GB LPDDR4X. … System operacyjny: Ubuntu 23.04." (p. 409, §3.3) [Processor …; RAM …; operating system: Ubuntu 23.04]

  > "W badaniu porównano uruchamianie aplikacji Tabela zainstalowanej za pomocą Flatpak i Snap. Pierwsze uruchomienie odbyło się bezpośrednio po uruchomieniu systemu operacyjnego." (p. 410, §4.3) [The study compared the launch of the Tabela application installed with Flatpak and Snap. The first launch took place directly after the operating system started.]

  > "Tabela 2: Dane statystyczne dotyczące czasów uruchamiania aplikacji - Flatpak Snap Średni czas uruchamiania [s] 1,0231 1,0304 Najkrótszy uzyskany czas uruchamiania [s] 1,0169 1,0165 Najdłuższy uzyskany czas uruchamiania [s] 1,0300 2,0266 Odchylenie standardowe [s] 0,0050 0,1007 Mediana [s] 1,0189 1,0177" (p. 411, Table 2) [mean, shortest, longest launch time, standard deviation, median, seconds]

  > "Pierwsze uruchomienie aplikacji po starcie systemu operacyjnego zawsze zajmuje więcej czasu." (p. 411, §4.3, about Snap) [The first launch of the application after the operating system starts always takes more time.]
- **Coverage:**
  - T9: covers weakly — launch time of a toy Qt application under Flatpak and Snap on Ubuntu 23.04 (≈1.02 s median both; Snap's first launch after boot ≈2.03 s), one laptop, 2023. Not a real desktop application; nothing after launch.
  - T1, T2, T3, T4, T6, T7, T10: do not cover.
- **Side:** program-side value from a Linux observation (candidate, weak).

### S1-84 — Giovanini 2021, computer-usage profiles of 31 Windows 10 users (Sysmon process logging)

- **Citation:** Luiz Giovanini, Fabrício Ceschin, Mirela Silva, Aokun Chen, Ramchandra Kulkarni, Sanjay Banda, Madison Lysaght, Heng Qiao, Nikolaos Sapountzis, Ruimin Sun, Brandon Matthews, Dapeng Oliver Wu, André Grégio, Daniela Oliveira. "Online Binary Models are Promising for Distinguishing Temporally Consistent Computer Usage Profiles." arXiv:2105.09900v2 [cs.LG], 2 Sep 2021 (later in IEEE Transactions on Biometrics, Behavior, and Identity Science).
- **Copy read:** https://arxiv.org/pdf/2105.09900 (arXiv v2, 21 pages; HTTP 200), accessed 2026-10-01; `sources/S1-84/arxiv2105.09900.pdf`; SHA-256 `92fbe5f909ec23f68aef2ffe69f172eabc0d8561b3850abbc518087f60a234c9`.
- **One observation:** yes — 31 participants' own Windows 10 computers, 8 weeks, Sysmon-based process-creation/termination and network logging plus click/keystroke timestamps per application.
- **Machine/platform, subject, window named:** platform named (MS Windows 10, participants' own laptops/desktops); population named (31 of 63 enrolled, aged 18–53); window named (8 weeks; 56 study days); calendar period not stated in the passages read (COVID-19 is mentioned).
- **Verbatim passages:**
  > "We collected ecologically-valid computer usage profiles from 31 MS Windows 10 computer users over 8 weeks" (p. 1, abstract)

  > "On average, we recorded 272 hours of computer usage data from each participant (SD = 189.9 hours, range: 31− 859), which corresponds to approximately 4.9 hours per study day ( SD = 3 .4 hr/day, range: 0.6− 15.3)." (p. 3, §4)

  > "To collect system-level events (process creation and termination, network connection), we developed a logger based on Sysmon [26]" (p. 4, §5)

  > "each line represented one minute of computer activity on a given study day … The columns contained: (i) a timestamp, (ii) a list of all active processes, (iii) a list of all domains accessed, (iv) the number of clicks associated with the timestamp, (v) the number of keystrokes associated with the timestamp, and (vi) an indicator (binary) of background processes activity" (p. 4, §6.1)

  > "our dataset of ecologically-valid computer usage data itself, will be made publicly available for vetted research usage" (p. 2, §1; footnote: "We are discussing with our IRB and legal counsel about options of data release")

  > "A notable exception is the dataset by Murphy et al. [15], wherein the keystroke data, mouse movements and clicks, and background processes were collected from 103 users over 2.5 years on each participant's private computer" (p. 2, §2)
- **Coverage:**
  - T1: locates, does not report — the per-minute lists of active processes per user are exactly co-occurrence data, but the paper reports only hours of use (mean 272 h per participant, ≈4.9 h per study day) and classifier results, no counts of concurrently open applications; data release only to vetted researchers, status unresolved in the copy read. Points to a second dataset (Murphy et al., 103 users, 2.5 years, background processes).
  - T9: locates, does not report — process creation events logged, no launch rates reported.
  - T2, T3, T4, T6, T7, T10: do not cover.
- **Side:** user-side (hours of use) from Windows 10; any program-side use would be context only.

### S1-85 — Brown 2014, Blackbox: BlueJ novice programmers' activity repository

- **Citation:** Neil C. C. Brown, Michael Kölling, Davin McCall, Ian Utting. "Blackbox: A Large Scale Repository of Novice Programmers' Activity." *Proceedings of the 45th ACM Technical Symposium on Computer Science Education (SIGCSE '14)*, pp. 223–228, 2014.
- **Copy read:** https://kar.kent.ac.uk/38938/1/2014-03-SIGCSE-Blackbox.pdf (Kent Academic Repository author copy, 7 pages incl. cover; HTTP 200), accessed 2026-10-01; `sources/S1-85/brown2014-blackbox-sigcse.pdf`; SHA-256 `494d8cbb1ce5aa75cf831d4328fb134ad90d896549cb9e32b0c1b48f4307b891`.
- **One observation:** yes — one continuous collection from opted-in BlueJ users worldwide (first ≈6 months reported).
- **Machine/platform, subject, window named:** platform not named (BlueJ runs on Windows, macOS, Linux; no split given); subject BlueJ 3.1.0 users (novice Java programmers); window ≈ mid-2013 to early 2014.
- **Verbatim passages:**
  > "Start and end times of programming sessions. • Use of all IDE tools, such as editing, compiling, execution, instantiation of objects, interactive method invocations, runs of unit tests, use of the debugger … compilation events include compilation outcomes/errors" (p. 4, §4.4)

  > "Nearly six months after launch we have a total of over 150,000 users participating in the Blackbox project, with over 10,000,000 compilation events." (p. 4, §5.1)
- **Coverage:**
  - T6: covers thinly — compiles users start themselves: aggregate count (>10 million compilation events from >150,000 novice users in ≈6 months, i.e. ≈67 per user over the window — the reader's own division), no per-hour rate, no project size or compile duration. Locates a dataset (Blackbox, access by researcher agreement) with per-session timestamps of compile events.
  - T1, T2, T3, T4, T7, T9, T10: do not cover.
- **Side:** user-side (how often users compile), any platform.

### S1-86 — Beller 2017/2019, Developer testing in the IDE (WatchDog and KaVE FeedBaG++)

- **Citation:** Moritz Beller, Georgios Gousios, Annibale Panichella, Sebastian Proksch, Sven Amann, Andy Zaidman. "Developer Testing in the IDE: Patterns, Beliefs, and Behavior." *IEEE Transactions on Software Engineering* 45(3):261–284, 2019 (accepted version 2017, DOI 10.1109/TSE.2017.2776152).
- **Copy read:** https://inventitech.com/assets/publications/2017_beller_gousios_panichella_amann_proksch_zaidman_developer_testing_in_the_ide_patterns_beliefs_and_behavior.pdf (first author's copy of the accepted manuscript, 24 pages; HTTP 200), accessed 2026-10-01; `sources/S1-86/beller2017-developer-testing-ide-tse.pdf`; SHA-256 `05e53018c6125100d230eb2937f35cc02867ca19993c82be34e507107957143c`.
- **One observation:** yes — one field study (WatchDog for Eclipse, IntelliJ, Android Studio; FeedBaG++ for Visual Studio), 2,443 developers, 15 Sep 2014 – 1 Mar 2017.
- **Machine/platform, subject, window named:** platform named in shares (Windows 81 % of users, macOS 11 %, Linux 8 %); subject named (IDE test runs, Java/C#); window named.
- **Verbatim passages:**
  > "In total, we observed 14,266,683 user interactions (so-called intervals, see Section 2.1) in 77,110 distinct IDE sessions." (p. 8, §4.2)

  > "Our developers predominately use some variant of Windows (81% of users), MacOS (11%), or Linux (8%)." (p. 8, §4.2)

  > "In these 431 projects, developers performed 70,951 test runs (EC: 63,912, IJ: 3,614, AS: 472, VS: 2,942). From 59,198 sessions in which tests could have been run … we observed that in only 8% or 4,726 sessions … developers made use of them and executed at least one test. … When we consider only sessions in which at least one test was run, the average number of test runs per session is 15 (EC: 15.3, IJ: 11.1, AS: 7.6, VS: 17.9)." (p. 9, §5.1, RQ1.2)

  > "In all IDEs except for Visual Studio, 50% of all test executions finish within half a second (EC: 0.42, AS: 1.8s, IJ: 0.47s, VS: 10.9s), and over 75% within five seconds (EC: 2.37s, IJ: 2.17s, AS: 3.95s, VS: 163s) … Test durations longer than one minute represent only 8.4% (EC: 4.2%, IJ: 6.9%, AS: 6.1%, VS: 32.0%) of the JUnitExecutions." (p. 10, §5.2, RQ2.1)

  > "JUnitExecution duration Sec 0 0 0.5 107.2 3.1 652,600" (p. 11, Table 3; columns Min, 25 %, Median, Mean, 75 %, Max)
- **Coverage:**
  - T6: covers — test runs developers start in the IDE: share of sessions with any test run (8 %), runs per session when testing (mean 15), run duration distribution (median 0.5 s, 75th percentile 3.1 s, mean 107.2 s; Visual Studio median 10.9 s), 2,443 developers, mostly Windows, 2014–2017. Does not cover compile/build runs or their size.
  - T1, T2, T3, T4, T7, T9, T10: do not cover.
- **Side:** user-side (how often and how long the jobs users start), any platform.

### S1-87 — Cheon 2026, power-consumption patterns from Intel's client telemetry (DCA)

- **Citation:** Harry Cheon, Yuyang Pang, Zhiting Hu, Benjamin Smarr, Julien Sebot, Bijan Arbab, Ahmed Shams. "Power Consumption Patterns Using Telemetry Data." arXiv:2602.22339, February 2026 (page header: "2023 Intel-HDSI DCA Collaboration: Carbon Footprint Project").
- **Copy read:** https://arxiv.org/pdf/2602.22339 (arXiv v1, 10 pages; HTTP 200), accessed 2026-10-01; `sources/S1-87/arxiv2602.22339.pdf`; SHA-256 `1806bfe35948519fd59cc89c59750cdd2d23175e124b75a48f6ce99af8017431`.
- **One observation:** yes — a 1-million-device (GUID) sample of Intel's opt-in client telemetry, mostly daily aggregates; collection dates not given in the copy read.
- **Machine/platform, subject, window named:** platform implied Windows PCs with Intel CPUs (the persona list includes "Win Store App User"; the OS is not stated outright); population named (1 million GUIDs, worldwide, US and China compared); window not named.
- **Verbatim passages:**
  > "Approximately 40% of people Opt-In, while 60% of people Opt-Out of sending telemetry data back to Intel. The data from these millions of worldwide devices is the primary source of data used in this study. Over 1,400 device specific parameters are collected from each device (CPU power used, temperature, network traffic, Hard Drive Disk (HDD) read/write traffic, applications launch times and duration used, frame per second experiences for each window, hard and soft page faults, etc." (p. 2, §2.1)

  > "The dataset used for this study was a 1 million GUID sample of Intel's telemetry data." (p. 2, §2.1)

  > "5. frgnd_backgrnd_apps_v4_hist: Software usage information, contains software names, duration, AC/DC status, display ON/OFF, and more" (p. 9, Appendix A)

  > "Persona China (%) US (%) / Web User 8.35 27.48 / Unknown 34.62 17.24 / Gamer 10.54 11.44 / Casual User 22.61 10.96 / Communication 2.13 8.27 / Casual Gamer 3.92 6.68 / Office/Productivity 6.49 5.14 / Content Creator/IT 4.17 5.07 / Win Store App User 1.71 3.97 / Entertainment 4.38 1.95 / File & Network Sharer 1.08 1.79 / Table 3: Persona breakdowns for the US and China. Persona was determined by Intel's Data Science team through k-means clustering." (p. 9, Appendix B, Table 3)
- **Coverage:**
  - T1: locates, reports little — Intel's client telemetry carries a per-device table of foreground and background software with names and durations, and launch times; this paper reports only k-means usage personas (share of devices per persona, US and China, e.g. "Gamer" 11.44 % US, "Content Creator/IT" 5.07 % US), not co-occurrence. The data is Intel-internal (a "sample toy dataset" in the project repository).
  - T6: locates, does not report — "Content Creator/IT" persona share only; no job sizes.
  - T9: locates, does not report — "applications launch times" collected, none reported.
  - T2, T3, T4, T7, T10: do not cover.
- **Side:** user-side (personas), presumably Windows; any program-side use would be context only.

### S1-88 — Bienia 2008, the PARSEC benchmark suite (input-set definitions)

- **Citation:** Christian Bienia, Sanjeev Kumar, Jaswinder Pal Singh, Kai Li. "The PARSEC Benchmark Suite: Characterization and Architectural Implications." Princeton University Technical Report TR-811-08, January 2008 (conference version: PACT 2008, DOI 10.1145/1454115.1454128).
- **Copy read:** https://www.cs.princeton.edu/techreports/2008/811.pdf (technical report, 22 pages; HTTP 200), accessed 2026-10-01; `sources/S1-88/bienia2008-parsec-tr811.pdf`; SHA-256 `4c08caea66098781d11a1222822a38ad7a0ac032c363cbbad4dcaf88a6fa3f4b`.
- **One observation:** not an observation — a benchmark definition (fixed inputs per workload); one document.
- **Machine/platform, subject, window named:** subject named (x264 H.264 encoder, VIPS image pipeline, dedup compression kernel) with fixed inputs; no users, no window.
- **Verbatim passages:**
  > "native A large input set intended for native execution. … the native input set is intended for performance measurements on real machines" (p. 3, §3.1)

  > "The videos used for the input sets have been derived from the uncompressed version of the short film "Elephants Dream"[3]. The number of frames determines the amount of parallelism." (p. 13, §3.2.12)

  > "• simlarge: 640 × 360 pixels ( 1/3 HDTV resolution), 128 frames • native: 1 , 920 × 1, 080 pixels (HDTV resolution), 512 frames" (p. 14, §3.2.12; "1/3" is typeset as a stacked fraction)

  > "The sizes of the images used for the input sets for vips are: … • simlarge: 2 , 662 × 5, 500 pixels • native: 18 , 000 × 18, 000 pixels" (p. 13, §3.2.11)

  > "Each input for dedup is an archive which contains a selection of files. The archives have the following sizes: … • simlarge: 184 MB • native: 672 MB" (p. 7, §3.2.4)
- **Coverage:**
  - T6: covers as a benchmark definition, not as user behaviour — a video-transcode job (x264, 512 frames at 1920×1080 from "Elephants Dream", ≈21 s at 24 fps — the frame-rate conversion is the reader's own), an image-processing job (VIPS, 18,000×18,000 pixels), a compression/deduplication job over a 672 MB archive; no statement of what desktop users actually run.
  - T7: does not cover (not a desktop scenario benchmark; no concurrency between applications).
  - T1, T2, T3, T4, T9, T10: do not cover.
- **Side:** neither — a definition of job sizes, no observation.

### S1-89 — Leith 2020, what browsers send when they phone home (first start, restart, idle)

- **Citation:** Douglas J. Leith. "Web Browser Privacy: What Do Browsers Say When They Phone Home?" Technical report, School of Computer Science & Statistics, Trinity College Dublin, 24 Feb 2020 (updated 11 and 19 March 2020); later in IEEE Access 9 (2021).
- **Copy read:** https://www.scss.tcd.ie/Doug.Leith/pubs/browser_privacy.pdf (author's copy, 15 pages; HTTP 200), accessed 2026-10-01; `sources/S1-89/leith2020-browser-privacy.pdf`; SHA-256 `b1d7d893c016629c72492335f1ced79034b103b89d54644d05a919c67b389d69`.
- **One observation:** yes — one set of scripted tests (fresh-profile first start, restart, URL paste/type, ≈24 h idle) per browser on two MacBooks, February 2020.
- **Machine/platform, subject, window named:** platform named (macOS Mojave 10.14.6 and Catalina 10.15; a Windows 10 check mentioned); subjects named with versions (Chrome 80.0.3987.87, Firefox 73.0, Brave 1.3.115, Safari 13.0.3, Edge 80.0.361.48, Yandex 20.2.0.1145); window named (first start; ≈24 h idle).
- **Verbatim passages:**
  > "We study six browsers: Chrome (v80.0.3987.87), Firefox (v73.0), Brave (v1.3.115), Safari (v13.0.3), Edge (v80.0.361.48) and Yandex (v20.2.0.1145). Measurements are taken using two Apple Macbooks, one running MacOS Mojave 10.14.6 and one running MacOS Catalina 10.15." (p. 3, §III)

  > "we evaluate the data shared: (i) on first startup of a fresh browser install, (ii) on browser close and restart, (iii) on pasting a URL into the top bar, (iv) on typing a URL into the top bar and (v) when a browser is sitting idle." (p. 1, §I)

  > "Start the browser from a fresh install/new user profile, click past any initial window if necessary, and then leave the browser untouched for around 24 hours (with power save disabled on the user device) and record network activity." (p. 4, §III-E)

  > "Our measurements indicate that browsers typically contact the Safe Browsing API roughly every 30 mins to request updates." (p. 5, §IV-A)

  > "Our measurements indicate that browsers typically check for updates to extensions no more than about every 5 hours." (p. 6, §IV-B)
- **Coverage:**
  - T9: context only (macOS) — what six desktop browsers do on the network at first start, restart and while idle (Safe Browsing list updates ≈ every 30 min, extension update checks ≤ every ≈5 h, per-browser connection lists in §V); network work only, no CPU or disk work, no Linux run.
  - T3, T1, T2, T4, T6, T7, T10: do not cover.
- **Side:** program-side observation on macOS — context, not a candidate value.

### S1-90 — Kljun 2016, backup strategies of end users (survey of 319)

- **Citation:** Matjaž Kljun, John Mariani, Alan Dix. "Toward understanding short-term personal information preservation: A study of backup strategies of end users." *Journal of the Association for Information Science and Technology* 67(12), 2016 (online 15 June 2015), DOI 10.1002/asi.23526.
- **Copy read:** https://pim.famnit.upr.si/wp/wp-content/uploads/serenditipy-old-blog/Papers/backup2015kljun.pdf (authors' draft dated 30 Oct 2014, header "The paper first appeared in the Journal of the Association for Information Science and Technology on June 15, 2015"; 21 pages; HTTP 200), accessed 2026-10-01; `sources/S1-90/kljun2016-backup-strategies-jasist.pdf`; SHA-256 `c63fa0e8e69b37a970295eec292988266dace921415bcaa1ab66b67a78d503a9`.
- **One observation:** yes — one online questionnaire, 319 respondents describing 542 computers, February–April 2013.
- **Machine/platform, subject, window named:** platform split named (Windows versions, OS X, Linux; per-OS figures are in Figures 2–3, not in the text layer); population named (convenience/snowball sample, several European countries plus Japan, Australia, US, Mexico, Canada); window named (Feb–Apr 2013); self-report, not logged.
- **Verbatim passages:**
  > "The results show that the majority of users do manual, selective and non-continuous backups, rely on a set of planned and unplanned backups (as a consequence of other activities)" (p. 1, abstract)

  > "The questionnaire circulated in several European countries besides Japan, Australia, United states, Mexico, and Canada from February to April 2013. It was answered by 319 individuals" (p. 4, §4.2)

  > "Participants described backup strategies for 542 computers (319 main and 223 secondary computers). … 30 (9.4%) main computers and 81 (36.3%) secondary computers are not backed up (111 or 20.5% of computers). By far most popular strategy is backing up to an external hard drive followed by a cloud storage and network drive." (p. 5, §5.1)

  > "The frequency values available for each selected strategy were: all the time, several times a day, once a day, every few days, once a week, every few weeks, every few months, other and don't know." (p. 7, §5.2)

  > "Out of 542 computers only 155 (28.6%) are backed up all the time (31 on a hard drive, 100 in the cloud, 28 on the network drive and 16 other)." (p. 7, §5.2)

  > "Company desktops and laptops are backed up more frequently (daily backed up 54% and 50% respectively) than personal desktops and laptops (daily 31.7% and 34.4% respectively) as seen in Table 5." (p. 7, §5.2)

  > "Only 160 (37.1%) off 431 backed up computers have a fully automated backup procedures in use, 62 (14.4%) a semi-automated (where backup is mostly automatic but some user intervention is needed to initialise it) and 209 (48.5%) use manual procedures (everything done by the user)." (p. 8, §5.3)

  > "when a scheduled backup is running it uses a significant chunk of your computers resources (slowing down everything, and make YouTube videos jumpy for example)." (p. 8, §5.3, a respondent's quote)
- **Coverage:**
  - T6: covers — backups started by hand: share of backed-up computers using manual procedures (48.5 % of 431), semi-automatic (14.4 %), automatic (37.1 %); frequency categories per strategy (personal desktops backed up daily 31.7 %); main destination (external hard drive most common); 319 respondents / 542 computers, mixed OS, 2013, self-report. Does not cover backup size or duration.
  - T1: does not cover (one respondent reports a scheduled backup running beside video playback — an anecdote, not a co-occurrence count).
  - T2, T3, T4, T7, T9, T10: do not cover.
- **Side:** user-side (which jobs users start, how often), any platform.

### S1-91 — Wunder 2025, data loss and recovery on personal devices in three countries (CHI '25)

- **Citation:** Julia Wunder, Rick Wash, Karen Renaud, Daniela A. Oliveira, Zinaida Benenson. "Achieving Resilience: Data Loss and Recovery on Devices for Personal Use in Three Countries." *CHI Conference on Human Factors in Computing Systems (CHI '25)*, Yokohama, 2025, 36 pages, DOI 10.1145/3706598.3714202.
- **Copy read:** https://strathprints.strath.ac.uk/92011/1/Wunder-etal-ACM-CHI-2025-Achieving-resilience-data-loss-and-recovery.pdf (Strathclyde repository, author manuscript, 36 pages; HTTP 200), accessed 2026-10-01; `sources/S1-91/wunder2025-data-loss-recovery-chi.pdf`; SHA-256 `7e11334f22ed5c43c497f4c76c717fc85b4e3f1953bc002f7a21557624949ec8`.
- **One observation:** yes — one online survey, 1,423 participants (494 USA, 498 UK, 431 Germany), recruited via Prolific and Clickworker; survey date not stated in the passages read (platform statistics cited as "accessed in Feb 2023").
- **Machine/platform, subject, window named:** device types named (desktop, laptop, smartphone, tablet), OS not split in the passages read; population named (near-representative in age and gender); self-report.
- **Verbatim passages:**
  > "we surveyed almost representative (in age and gender) samples of German, UK and USA populations, 1423 in total. … In the full sample, 86% of participants created full or partial backups of at least one of their devices, the most important trigger being prior data loss experiences." (p. 1, abstract)

  > "Table 6. Of the people who use backups on each device type, the percentage of those who use each backup method … Desktop Laptop Smartphone Tablet / Cloud 58.6% 69.8% 83.9% 80.6% / External Drive 73.5% 62.6% 17.6% 17.7% / Builtin Backups 32.1% 23.8% NA NA … Third Party Tool 9.3% 4.1% NA% NA% / Network Storage 7.8% 5.5% 2.1% 2.1% / 𝑁 396 652 917 237" (p. 17, Table 6)

  > "Usage of cloud backups usually means backing up quite frequently, every few … days to every time a file is changed. In contrast, backups to external hard drives, other devices or using builtin features7 take place every few weeks to months." (pp. 16–17, §5.1; the sentence is interrupted by the page break and Table 6)

  > "Built-in features are backup functions offered by the device itself. They can run passively in the background or be actively started by a user." (p. 17, footnote 7)
- **Coverage:**
  - T6: covers — which backup methods users of desktop computers use (external drive 73.5 %, cloud 58.6 %, built-in 32.1 %, third-party tool 9.3 % of 396 desktop backers) and their cadence in words (external-drive backups every few weeks to months); USA, UK, Germany, ≈2023, self-report. Does not give backup sizes or durations, and does not split manual from automatic starts.
  - T1, T2, T3, T4, T7, T9, T10: do not cover.
- **Side:** user-side, any platform.

### S1-92 — Seo 2014, programmers' build errors at Google

- **Citation:** Hyunmin Seo, Caitlin Sadowski, Sebastian Elbaum, Edward Aftandilian, Robert Bowdidge. "Programmers' Build Errors: A Case Study (at Google)." *Proceedings of the 36th International Conference on Software Engineering (ICSE 2014)*, pp. 724–734.
- **Copy read:** https://research.google.com/pubs/archive/42184.pdf (Google Research copy, 11 pages; HTTP 200), accessed 2026-10-01; `sources/S1-92/seo2014-programmers-build-errors-google.pdf`; SHA-256 `036d3315dbfbc0cb7f10ba89832b10986ea83313e8465e103abef89c16f7df90`.
- **One observation:** yes — the logs of Google's centralised cloud build system, November 2012 – July 2013, 26.6 million build invocations by 18,000 developers.
- **Machine/platform, subject, window named:** platform named (Google's cloud-based build system, builds of C++ and Java server binaries; not desktop-local compiles); population named; window named.
- **Verbatim passages:**
  > "Throughout this paper, a build represents a single request from a programmer which executes one or more compiles; a build only succeeds if all compiles succeed." (p. 2, §2)

  > "This dataset contains over 26.6 millions build attempts performed by over 18,000 developers during a period of nine months, and logged by the centralized build system. … we already observe quite a variance in a long tail distribution, with a mean of 1446 and a median of 759 builds per developer over nine months." (p. 2, §2)

  > "For this study, we examined log data from the build system for a period of nine months from November 2012 through July 2013. This data represented the compilation work necessary to build C++ and Java binaries that would run on Google's own servers. The data did not include projects built by other build systems within Google (generally client software for Mac, Windows, or mobile, or outside software such as javac, gcc, or the Linux kernel)." (p. 3, §3.2)

  > "We recognized janitors, robots and infrastructure developers either by the specific build commands they used, or by detecting users performing more than 50 builds per day over the entire nine months. We also classified non-active developers as any user performing less than one build per day. Across standard developers, each month Java programmers performed an average of 140 builds (median: 101 builds) and C++ programmers performed an average of 202 builds (median: 147 builds)." (p. 3, §3.2)
- **Coverage:**
  - T6: covers — how often developers start builds of their own code: per developer per month, Java mean 140 / median 101, C++ mean 202 / median 147 (standard developers); per developer over nine months mean 1,446 / median 759; 18,000 Google developers, Nov 2012 – Jul 2013. The builds run on a remote build service, so the frequency is a user-side value but the build's size on a desktop CPU is not covered; objects per build and incremental against full are not reported.
  - T1, T2, T3, T4, T7, T9, T10: do not cover.
- **Side:** user-side (how often users start builds), any platform; the build's execution is remote, not desktop.

## 3. Not found

### T1 — Application co-occurrence on real desktops

- **T1 — co-occurrence on Linux desktops at population scale.** No peer-reviewed or preprint study found that logs which applications are open simultaneously on Linux desktops across a population; the closest are S1-19 (13 Xubuntu users, application-instance counts, no simultaneity) and S1-02 (BEHACOM, 3–4 Linux users, per-minute active-application average available only as raw data). Searches: "Linux desktop user activity logging study window focus switching field study GNOME X11 participants"; "\"Linux\" users logged \"window switches\" … field study per hour developers X11"; "energy consumption Linux desktop environments GNOME KDE Xfce idle background processes empirical study paper" (only Phoronix benchmarks); Chapuis IHM 2005 wmtrace paper (X Window logging tool, abstract shows no population statistics; full text behind HAL anti-bot page).
- **T1 — home use, gaming, music, video playback, video calls, transcoding, backups, indexing combinations.** No logging study found that reports co-occurrence of these activity classes on desktops; the closest are S1-15 (Teams meetings with concurrent email/file editing, workplace) and S1-21 (student laptops: browsers, virus scanners). Chetty et al. CHI 2009 (home computer power management) could not be read (no open copy; guessed MSR URLs 404). Searches: "field study background processes running on personal computers logging number of processes …"; "large-scale telemetry study desktop application usage Windows PCs …" (Verto Analytics panel papers exclude or only total PC time).
- **T1 — how long each application stays open (lifetime).** Not reported as a distribution in any source read; S1-13 gives windows opened/closed per day and that 55% of windows are never revisited; S1-05 logs window lifespans but does not report them.

### T2 — Foreground focus and switching

- **T2 — Linux foreground-focus statistics.** None found in the literature (all logged switching statistics read are Windows, macOS lab, or OS-unspecified observation). BEHACOM (S1-02) and SWELL-KW (S1-10, Windows lab) are the datasets with foreground fields; SWELL is not everyday use.
- **T2 — Mozilla Test Pilot studies and OS/browser telemetry releases.** Test Pilot results were published as Mozilla metrics blog posts and the author's blog (dubroy.com), not as literature (S3 material); the peer-reviewed Firefox tab-logging study is S1-30, which used its own extension. No OS telemetry release with application/window names and timestamps found in the literature. RescueTime aggregate "switches" figures exist only as vendor blogs (search "RescueTime data study knowledge workers time in applications switching per day…"), not literature.
- **T2 — Yeykelis, Cummings & Reeves 2014 ("switches every 19 seconds") and Yeykelis et al. 2018 (Media Psychology), Judd & Kennedy 2011 (Computers & Education).** Closed access; not read (OpenAlex no OA, Semantic Scholar status CLOSED, Unpaywall is_oa false). The 30-laptop result is quoted second-hand in S1-11.
- **T2 — KaVE / Enriched Event Streams IDE dataset (Proksch, Amann, Nadi, MSR 2018).** Not read (proks.ch 404, ACM DL 403); in-IDE events only.

### T3 — Browser windows, tabs and renderer processes

- **T3, visible-at-once windows and tabs.** No logged count of how many browser windows or tabs are *visible* at once was found. DOBBS (S1-34) logs window focus and visibility events but reports only open counts; Weinreich (S1-33) reports keeping windows "opened in the background" qualitatively. Searches: the T3 rows of the search log (tabbed browsing, telemetry, logging-study queries).
- **T3, Chromium process model on desktop Linux observed for a set of tabs.** No peer-reviewed or preprint observation of renderer-process counts for a given set of tabs on desktop Linux under site-per-process. Closest: S1-38 (renderer-sharing threshold of 31 tabs on a 4 GB machine and ≈70 on an 8 GB machine, Chrome v52–v58, OS of that run not stated, rule stated for 64-bit OS X and Linux); S1-31 (renderer counts from Windows telemetry and a Windows 10 microbenchmark — context); S1-48 (asserts one process per tab on ChromeOS, not measured). Spare renderer and soft process limit appear only as design statements (S1-31). Searches: "measurement study number of renderer processes …", "arxiv Chromium renderer processes tabs memory measurement Linux …".
- **T3 sources not obtained.** Labaj & Bieliková UMAP 2013 (no open copy). Firefox/Chrome/Edge tab-count telemetry appears only in blogs, forums and source code (S3/S2 material), not in literature located here.

### T4 — Games and their companions on Linux

- **T4, thread population of a running game on desktop Linux (counts, names, busy threads) in peer-reviewed literature.** No peer-reviewed or arXiv paper found that lists a game's threads on Linux, native or under Proton/Wine. The only Linux observations with thread names are conference-talk slides by the LAVD author (S1-62, S1-63) and process-level lists from Steam Deck forensics (S1-67); the only peer-reviewed Linux game TLP figure is Quake 2 on kernel 2.2.3 (S1-55). Searches: arXiv API (rate-limited, 429/503), OpenAlex (8 queries), Semantic Scholar (429), WebSearch (thesis DXVK/Proton; EEVDF gaming; Proton/Wine threads). "Is Proton Good Enough?" (2023, Springer) exists but is closed access and not read.
- **T4, Steam client downloading while a game runs by default, and the download settings.** No literature observation found. S1-65 and S1-66 cover update cadence and aggregate delivery; S1-66 and S1-68 establish auto-install and logging (existence). The setting "allow downloads during gameplay" is vendor documentation (S2's class). Pointer for S3: SteamOS `appinfo_log.txt` / `content_log.txt` timestamps (S1-68).
- **T4, nested-compositor (gamescope) frame cadence on a desktop vs the Steam Deck.** Not found in literature. Only S1-61 (Xwayland at 16.6 ms in a 60 fps game, desktop, talk slides). A blog measurement of X11/Wayland/Xwayland input latency (Marco Nett) exists — out of class, pointer for S3.
- **T4, what users run beside a game (voice chat, browser).** Only market surveys (Statista, YouGov) and press found — not literature; no logged observation.

### T6 — Batch jobs the user starts

- **T6 — video transcodes and renders started by users (source length, settings, duration on a desktop CPU):** no observation of user-started render or transcode jobs found. Searches: "survey of video creators editing practices export render time …" (formative studies of 8–9 creators only), "vbench … video duration resolution distribution uploads" (cloud transcoding; paper behind HTTP 403/404). Only a benchmark definition (S1-88, PARSEC x264 512 frames at 1080p).
- **T6 — local ML training or fine-tuning, local AI inference on desktops:** no peer-reviewed observation of what users run or how large. Searches: "why people run LLMs locally interview survey study r/LocalLLaMA …", "arXiv empirical study Ollama llama.cpp users consumer GPUs …", arXiv API query (HTTP 429).
- **T6 — compiles of users' own projects, objects per build, incremental against full, on a desktop:** build frequencies found only for remote builds (S1-92, Google) and novice compile counts (S1-85, BlueJ); no observation of object counts per local build or incremental/full ratio. Searches: "empirical study local developer builds frequency duration incremental versus clean builds …", "\"local builds\" developers empirical study build scans Gradle Develocity …", "\"Build Latency, Predictability, and Developer Productivity\" …" (the Google Research page links only an IEEE Xplore copy; not read). The Visual Studio interaction dataset papers (Amann et al. SANER 2016; Proksch et al. MSR 2018) that log build events could not be read: ACM HTTP 403, Semantic Scholar "CLOSED", Proksch's thesis behind an Anubis bot challenge and a truncated Wayback copy.
- **T6 — archive creation and hand-started backups' size and duration:** backup frequency and manual/automatic split found (S1-90, S1-91); no source gives backup or archive sizes or durations.

### T7 — Desktop scenario benchmarks

- **T7, PCMark 10, SYSmark 30, SYSmark 25, SYSmark 2018, UL Procyon scenario definitions in peer-reviewed literature.** Not found. Peer-reviewed/academic descriptions exist only for SYSmark 98 / Winstone 99 (S1-55), SYSmark NT / SYSmark 32 / Winstone 95 (S1-60) and SYSmark 2007 (S1-57); CpsMark+ (S1-58) read at abstract level only (full text blocked, 403). Papers that run PCMark 10 or SYSmark (arXiv 2110.07822, 2005.07613, 2112.11587) do not describe scenarios. Fadi Sibai's PCMark05 papers (2006, 2008) are closed (ACM 403, no OA copy). Concurrency inside a scenario (e.g. SYSmark 2004's VirusScan during Communication) appears only in press and vendor-commissioned reports — S2's class.
- **T7, backup / malware-scan / compile / game-download / ML-training workloads in these benchmarks.** In the literature read: archive (WinZip) and video transcode exist in SYSmark 2007 (S1-57); none of the others found. VDI benchmarks (VMware View Planner, Login VSI) reportedly include virus scan and 7-Zip but no peer-reviewed description was located.

### T9 — Launch and first minutes

- **T9 — launches per hour / applications started mid-session from logged desktop data:** no logged rate found. Proxies only: S1-13 (share of window openings that start a new application), S1-19 (user-application instances per participant, Xubuntu), S1-43 (GIMP sessions per user). Searches: "desktop application launch frequency field study logged launches per day …" (press reports of a Soluto Windows 8 study only), "predicting application launches desktop computer logged usage …" (patents, mobile), "how users launch applications desktop field study start menu …" (lab usability tests). The only statement is an unmeasured characterisation in S1-81. Telemetry that records launches exists (S1-84, S1-87) but reports no rates.
- **T9 — what an application does in the minutes after start on Linux (cache warm-up, first sync):** no Linux observation found; launch-phase work only (S1-80, S1-81, S1-82, S1-83). The one observation of post-start behaviour (network work of browsers at first start and idle) is on macOS (S1-89, context). Searches: "measurement what desktop application does after startup network connections first minutes …", "Electron desktop applications performance empirical study startup time …".

### T10 — Rates of operations in real use, and a video call's processes

- **T10, e-mails *sent* per hour, with or without attachments.** No logged per-user sending rate split by attachment was found in the literature opened. Received per day: S1-40 (mean 87, median 58). Sent vs received per day only as a curve: S1-39. Reaction to arrival: S1-49. E-mail alert, checking and visit rates from window-logging studies are in S1-03 (Iqbal & Horvitz, CHI 2007), S1-04 (Mark et al., CHI 2016) and S1-05 (Mark et al., CHI 2014 / CSCW 2015). Grevet et al. CHI 2014 and Cockburn & McKenzie IJHCS 2001 could not be obtained (dead ends logged).
- **T10, image-filter operations per hour.** Not found as a filter-specific rate. Closest: GIMP command logs (S1-43: median 24 commands per session, 19 s between commands, filters outside the top-20 commands). ingimp CHI 2008 (design paper) has no rates.
- **T10, video-preview renders per hour/session.** Not found (search "video editing software usage log analysis … render preview frequency …" returned no logging study).
- **T10, chat messages received per hour on a current platform.** No per-user received-message rate for Slack, Teams or Discord was found. The rates found are for IM clients of 2000–2006 (S1-50: 17.6 messages exchanged per recorded hour, Windows, 2005; S1-51: 1.7 conversations per day × 17.2 turns, 2000–2001; S1-46: population level, June 2006) and per-channel totals for Slack (S1-47, 2016–2019).
- **T10, process and thread structure of a video call on Linux (Zoom, Teams, Meet, Jitsi in a browser).** Not found in the literature. Measurement papers that ran calls on Linux report network and QoE metrics only (S1-44: native Zoom Linux client v5.4.9 plus Webex/Meet web clients on Linux VMs, 2021; S1-45: Zoom 5.6.1 and Teams 1.4.00.7556 native and Chrome clients on Ubuntu 20.04.1, 2021). Client CPU usage was measured only on Android (S1-44, context). Searches on Jitsi/WebRTC CPU, threads and energy returned only blogs (wirelessmoves, LWN, Greenspector, CableLabs).
