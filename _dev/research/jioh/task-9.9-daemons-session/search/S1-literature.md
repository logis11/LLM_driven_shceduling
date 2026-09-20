# S1 — peer-reviewed and preprint literature (T1, T2, T3, T6)

Reader S1, task 9.9 "Daemons and session processes", stage 2 search. Written 2026-09-20 from `search/input.md` only. Topics searched: T1 (system services at idle), T2 (session processes at idle and under drawing/playing), T3 (the idle desktop as a whole), T6 (system services and the session as a scheduler workload). T4, T5, T7 were not searched.

Conventions. Every passage below is verbatim from the copy read, with a locator in square brackets (`[p. N]` is the PDF page index counted from 1 in the fetched file; `[slide N]` for slide decks; `[§ …]` for HTML pages that have no pagination). Ligatures (fi, fl, ff) in the PDF text are written as plain letters and words hyphenated across a line break are joined; nothing else is changed. "One observation" means one population, trace, run or log with machine, subject and window named. Sources that are not peer-reviewed or preprint literature but were the only literature-class carriers of a Linux observation (a vendor white paper, conference slide decks, LWN conference reports) are kept as candidates and flagged `grey` in the citation. Copies are under `sources/S1-NN/` (gitignored); `sources/ctx/` holds context-only material. All copies accessed 2026-09-20. Tooling: `curl -sSL` through the session proxy, `pymupdf` for text extraction, `sha256sum`.

## 1. Search log

Engines: WS = the session's WebSearch tool (web index, US); direct = `curl` fetch of a known URL. Every row lists hits followed and dead ends with their HTTP status. Notes shared by the previous slice's readers held again today: dl.acm.org, ieeexplore, researchgate and academia.edu return 403 or a challenge page (202 with no content); Semantic Scholar's API answered once (200) for a DOI lookup; Zenodo answered 410 (record deleted); arxiv.org, landley.net, usenix.org (legacy), lwn.net, lpc.events, static.sched.com, retis/iris.sssup.it, lac.linuxaudio.org, lac2020.sciencesconf.org, embedded-recipes.org, htor.inf.ethz.ch, intel.com, cs.columbia.edu, cs.technion.ac.il, web.njit.edu, proceedings.jacow.org served files.

| # | date | engine / venue | exact query | hits followed | dead ends (HTTP status) |
|---|------|----------------|-------------|---------------|-------------------------|
| 1 | 2026-09-20 | WS | `idle wakeups per second Linux desktop daemons power measurement paper` | Intel "Linux Power Efficiency Analysis Methods" PDF → S1-01 | forum threads (bbs.archlinux.org, narkive) not followed: not literature |
| 2 | 2026-09-20 | WS | `arxiv Linux desktop idle CPU wakeups compositor GNOME Shell energy measurement` | none new (arXiv hits were energy-measurement tooling papers, not desktop-idle observations) | — |
| 3 | 2026-09-20 | WS | `PipeWire PulseAudio JACK audio server real-time scheduling latency CPU measurement paper Linux` | none (guides, wikis, forums only) | — |
| 4 | 2026-09-20 | WS | `Wayland compositor frame scheduling CPU cost measurement paper Weston Mutter KWin` | none (openlib.io essays without measurements; not followed) | — |
| 5 | 2026-09-20 | WS | `Linux scheduler interactivity evaluation background daemons noise CFS EEVDF paper` | arXiv 2511.11628 (Mixture-of-Schedulers) → S1-15; Wong et al. 2008 (researchgate) → see row 28 | — |
| 6 | 2026-09-20 | WS | `"Getting maximum mileage out of tickless" Siddha Pallipadi OLS 2007 wakeups` | landley.net OLS 2007 PDF → S1-02; Paratick (web.njit.edu) → ctx; OLS 2008 Srinivasan (cs.columbia.edu) → S1-03 | — |
| 7 | 2026-09-20 | WS | `Cucinotta "Low-latency audio on Linux by means of real-time scheduling" JACK SCHED_DEADLINE LAC 2011` | lac.linuxaudio.org 2011 index → paper 46.pdf → S1-05 | researchgate, slideshare not followed |
| 8 | 2026-09-20 | WS | `"OS noise" Linux daemons periodic wakeups quantitative analysis Morari Gioiosa IPDPS 2011` | iris.sssup.it IEEE-TC-2022.pdf (Bristot de Oliveira et al.) → S1-14 | dl.acm.org 10.1145/3095770.3095772 not attempted (ACM blocks) |
| 9 | 2026-09-20 | WS | `energy consumption comparison Linux desktop environments GNOME KDE Xfce idle study paper` | none: phoronix.com unreachable per prior notes (not attempted); blog posts not literature | — |
| 10 | 2026-09-20 | WS | `Redline "first class support for interactivity" OSDI 2008 X server Linux` | usenix.org legacy PDF → S1-04 | — |
| 11 | 2026-09-20 | WS | `"A Quantitative Analysis of OS Noise" pdf Morari Gioiosa Wisniewski Cazorla Valero` | Semantic Scholar page (see direct fetches) | ieeexplore.ieee.org/document/6012894 → 202 challenge page; researchgate → 403 |
| 12 | 2026-09-20 | WS | `Wayland input latency measurement compositor study arXiv GNOME KDE Sway "frame" latency` | none (blogs only: marco-nett.de, farnoy.dev, zamundaaa.github.io — not literature, not followed) | — |
| 13 | 2026-09-20 | WS | `"Evolution of thread-level parallelism in desktop applications" Blake Dreslinski Mudge Flautner ISCA 2010 idle` | dblp record read in results: study on Windows 7 and OS X → context, not fetched | dl.acm.org not attempted (blocks) |
| 14 | 2026-09-20 | WS | `Linux Audio Conference paper PipeWire latency measurement CPU load xruns evaluation` | none (guides only) | — |
| 15 | 2026-09-20 | WS | `LWN OSPM summit report audio compositor latency scheduler "latency nice" desktop` | lwn.net/Articles/820659 and 887842 → S1-11 | — |
| 16 | 2026-09-20 | WS | `timer slack timer coalescing Linux paper wakeups idle "deferrable timers" energy evaluation` | none new (LWN "Timer slack" 369549 is a mechanism article; not a Linux observation; not fetched) | — |
| 17 | 2026-09-20 | WS | `"A Quantitative Analysis of OS Noise" upcommons OR bsc.es pdf` | none | upcommons.upc.edu discover → 404 |
| 18 | 2026-09-20 | WS | `Wayland compositor power consumption energy measurement thesis "GNOME Shell" OR "KWin" OR "Weston" CPU usage per frame` | none (phoronix/dedoimedo blog measurements — not literature; phoronix unreachable) | — |
| 19 | 2026-09-20 | WS | `PipeWire thesis latency measurement "PulseAudio" "JACK" comparison Linux 2022 OR 2023 OR 2024 pdf` | embedded-recipes.org 2023 Gleonec slides → S1-08; lac2020.sciencesconf.org PipeWire.pdf → S1-07 | — |
| 20 | 2026-09-20 | WS | `sched_ext LAVD paper latency criticality gaming Steam Deck scheduler evaluation compositor audio` | lpc.events LPC 2024 slides and static.sched.com OSS NA 2024 slides → S1-09; lwn.net/Articles/1051430 → S1-10 | — |
| 21 | 2026-09-20 | WS | `arxiv "idle" Linux "background processes" desktop "context switches" characterization workload study processes threads population` | arXiv 1811.01412 (Becker & Chakraborty, TUM tech report) → ctx (benchmark stability, no idle-population figures) | — |
| 22 | 2026-09-20 | WS | `"Stepping towards noiseless Linux environment" Akkan pdf ROSS 2012` | htor.inf.ethz.ch ROSS 2012 slides → S1-13 | dl.acm.org not attempted |
| 23 | 2026-09-20 | WS | `Tizen Wayland compositor performance evaluation paper CPU frame Enlightenment OR Weston embedded measurement` | none (wiki/forum) | — |
| 24 | 2026-09-20 | WS | `LWN "wakeups" idle desktop "per second" tickless 2007 OR 2008 article Arjan van de Ven powertop results` | lwn.net/Articles/240365 (OLS 2007 report) → ctx | — |
| 25 | 2026-09-20 | WS | `"Understanding and isolating the noise in the Linux kernel" Akkan Lang Liebrock pdf` | none open (journal paywalled) | journals.sagepub.com, dl.acm.org not attempted; researchgate/academia block |
| 26 | 2026-09-20 | WS | `Linux desktop idle "wakeups" study "GNOME" OR "KDE" measurement "per second" powertop paper OR thesis` | Intel "PowerTOP Primer" article → ctx (vendor article, no machine named) | Launchpad bug 283100 is an S3-class item, not followed |
| 27 | 2026-09-20 | WS | `interbench Con Kolivas interactivity benchmark "background" loads X compile audio video documentation` | none fetched (interbench is a tool, S2/S3 class; man page and LKML announce are not literature) | github.com blocks HTML per prior notes; not attempted |
| 28 | 2026-09-20 | WS | `"Fairness and interactive performance of O(1) and CFS Linux kernel schedulers" Wong pdf` | see direct fetches | ieeexplore PDF → 418; academia.edu → 403 |
| 29 | 2026-09-20 | WS | `"Self-tuning schedulers for legacy real-time applications" Cucinotta Checconi Abeni Palopoli EuroSys 2010 pdf Xorg` | retis.santannapisa.it papers page → hdl.handle.net/11382/304382 → iris.sssup.it PDF → S1-06 | core.ac.uk search → 403 |
| 30 | 2026-09-20 | WS | `D-Bus performance evaluation paper systemd measurement "dbus-daemon" latency messages per second` | LPC 2011 session page (Collabora) → ctx (no slides linked); ICALEPCS 2017 TUPHA168 → ctx | — |
| 31 | 2026-09-20 | WS | `retis.santannapisa.it "Self-tuning schedulers for legacy real-time applications" pdf download` | retis.santannapisa.it/papers/ (see row 29) | — |
| 32 | 2026-09-20 | WS | `systemd academic paper analysis "systemd" boot OR service manager performance measurement journald udev study` | none (tutorials); arXiv 1211.4839 (boot debugger) not relevant | — |
| 33 | 2026-09-20 | WS | `Linux "idle power" laptop measurement study "Wayland" "X11" OR "Xorg" paper 2021 OR 2022 OR 2023 OR 2024 OR 2025 energy desktop session` | none (blogs/phoronix only) | — |
| 34 | 2026-09-20 | WS | `"green software" OR "energy efficiency" study Linux desktop environments comparison measurement paper Xfce GNOME KDE journal 2019 OR 2020 OR 2021 OR 2022 OR 2023` | none. A result page (lifetips.alibaba.com) claimed "a 2023 study in ACM Transactions on Management Information Systems, 210 participants, XFCE 1.42 joules per command"; no such paper could be located by title, author or venue and the claim is recorded as unverified, not followed | — |
| 35 | 2026-09-20 | WS | `"OS noise" OR "OS jitter" daemons Linux desktop "user-level" processes periodic wakeups measured Hz paper ntpd crond syslogd` | Tsafrir et al. ICS 2005 → ctx (two decades old); osti.gov Ferreira 2008 not followed (HPC, no per-daemon rates in abstract) | — |
| 36 | 2026-09-20 | WS | `scheduler benchmark Linux desktop responsiveness evaluation paper "audio" "video" background load latency BFS CFS MuQSS comparison measurement` | lwn.net/Articles/725238 "A survey of scheduler benchmarks" → S1-12 | phoronix unreachable |
| 37 | 2026-09-20 | WS | `"Thread-level parallelism and interactive performance of desktop applications" Flautner ASPLOS 2000 Linux idle pdf` | none open; 26 years old → context only, not fetched | dl.acm.org PDF not attempted (blocks) |
| 38 | 2026-09-20 | WS | `Wong Tan Kumari Lam Fun 2008 CFS O(1) interactivity interbench pdf site:academia.edu OR site:hw.ac.uk OR site:monash.edu` | none open | academia.edu → 403 (direct) |
| 39 | 2026-09-20 | WS | `arxiv 2025 sched_ext scheduler evaluation interactive desktop workloads "background" daemons frame time` | arXiv 2509.01245 (Agentic OS) seen; abstract names no daemon figures; not fetched. 2511.11628 already S1-15 | — |
| 40 | 2026-09-20 | WS | `Collabora "D-Bus performance" Linux Plumbers 2011 slides pdf context switches dbus-daemon scheduling` | LPC 2011 session page → ctx (abstract only, no slides on page) | — |
| 41 | 2026-09-20 | WS | `"GNOME Shell" OR "Mutter" OR "KWin" compositor CPU "frame" profiling measurement paper OR thesis Linux "per frame" milliseconds vsync` | none (developer blogs: fishsoup.net 2011, feaneron.com — not literature, not followed) | — |
| 42 | 2026-09-20 | WS | `comparative study Linux init systems paper systemd OpenRC runit sysvinit measurement resource usage arXiv OR IEEE` | arXiv 1808.10097 (IoT duty-cycling, systemd units) → ctx (boot/shutdown only) | — |
| 43 | 2026-09-20 | WS | `"Sleepless in Seattle" OR "LiteGreen" OR "SleepServer" idle desktop wakeups measurement paper Windows Linux context` | usenix.org ATC 2010 Reich et al. → ctx (Windows; context only) | — |
| 44 | 2026-09-20 | WS | `HotPower OR ISLPED OR IISWC paper "idle" desktop Linux "wakeups" "timer" energy characterization user-space processes` | none | — |
| 45 | 2026-09-20 | WS | `"X server" OR "Xorg" CPU usage compositing "composite" window manager performance study paper measurement Linux 2009 OR 2010 OR 2011 OR 2012 OR 2013` | none (forums; CHI 2011 importance-driven compositing is HCI, not a CPU measurement — not followed) | — |
| 46 | 2026-09-20 | WS | `PulseAudio "timer-based scheduling" OR "glitch-free" wakeups measurement paper OR thesis power consumption audio server Linux` | none in class (0pointer.de blog and Fedora wiki are S2-class) | — |
| 47 | 2026-09-20 | WS | `idle virtual machine "timer interrupts" OR wakeups Linux guest idle characterization paper "idle VM" wake rate` | Paratick ICPP 2021 (already fetched) → ctx | — |
| 48 | 2026-09-20 | WS | `"Linux" desktop "idle" "processes" count "threads" measured "wakeups" battery study Ubuntu laptop paper university 2015..2025 "powertop"` | none in class (Launchpad bugs, tutorials) | — |
| 49 | 2026-09-20 | WS | `Weston OR wlroots compositor evaluation paper embedded automotive Linux "CPU load" "frame" measurement IEEE OR Springer 2018..2025` | none | — |
| 50 | 2026-09-20 | WS | `thesis "window manager" OR "desktop environment" energy consumption Linux measurement diva-portal OR "bachelor thesis" OR "master thesis" i3 GNOME KDE Xfce idle power` | none in scope (kardan.edu.af kernel power comparison not followed: no desktop-session content in snippet) | — |
| 51 | 2026-09-20 | WS | `"Chrome OS" OR "ChromeOS" idle wakeups power measurement paper daemons "per second" Linux` | none in class (chromium.googlesource docs are S2-class) | github.com issue not followed (403 per notes) |
| 52 | 2026-09-20 | WS | `"system daemons" OR "background daemons" Linux "idle system" measurement "CPU time" characterization paper operating system overhead desktop workload trace` | none | — |
| 53 | 2026-09-20 | WS | `Linux "gaming" workload characterization paper "perf sched" tasks "audio" "compositor" OR "gamescope" share scheduling Steam Deck Wine` | confirms S1-09/S1-10; nothing new | — |
| 54 | 2026-09-20 | WS | `"Getting maximum mileage out of tickless" OR "cpuidle" OLS 2007 "Do nothing efficiently" Pallipadi pdf landley` | landley.net cpuidle OLS 2007 PDF → ctx (C-state mechanism; no per-daemon figures) | — |

Direct fetches (all 2026-09-20; status in parentheses): intel.com linux-power-efficiency-analysis-methods-2.pdf (200); landley.net ols2007v2-pages-201-208.pdf (200); usenix.org osdi08 yang.pdf (200); iris.sssup.it IEEE-TC-2022.pdf (200); lac.linuxaudio.org/2011/papers/ index (200), 24/26/32/46.pdf (200 each; only 46 is the target); lac.linuxaudio.org/2011/?page=program (200); landley.net ols2006v1-pages-441-450.pdf (200); core.ac.uk search (403); blog.linuxplumbersconf.org/2011/ocw/sessions/321 (200); intel.com powertop-primer (200); lpc.events scx_lavd-lpc-mc-24.pdf (200); static.sched.com scx-lavd-oss-na24.pdf (200); lwn.net/Articles/1051430, 820659, 887842, 240365, 725238 (200 each); embedded-recipes.org Gleonec PDF (200); lac2020.sciencesconf.org PipeWire.pdf (200); htor.inf.ethz.ch ross2012-akkan.pdf (200); arxiv.org/pdf/2511.11628 (200); arxiv.org/pdf/1811.01412 (200); cs.huji.ac.il Noise05ICS.pdf (HTML error page returned with 200 — "Something went wrong"); cs.technion.ac.il/~dan/papers/Noise05ICS.pdf (200); upcommons.upc.edu discover (404); semanticscholar.org paper page (202, empty body); api.semanticscholar.org DOI:10.1109/IPDPS.2011.84 (200; openAccessPdf → zenodo.org/record/3432539); zenodo.org/record/3432539 (410 "Record removed on request by third-party", also via API); ieeexplore.ieee.org/document/6012894 (202 challenge); ieeexplore iel5 …/04631872.pdf (418); academia.edu Wong 2008 (403); researchgate Morari (403); retis.santannapisa.it/papers/ (200); hdl.handle.net/11382/304382 → iris.sssup.it (200) → retrieve/…/EuroSys-2010.pdf (200); web.njit.edu paratick.pdf (200); arxiv.org/pdf/1808.10097 (200); usenix.org atc10 Reich.pdf (200); proceedings.jacow.org icalepcs2017 tupha168.pdf (200); cs.columbia.edu ols-2008-srinivasan-energy.pdf (200); landley.net ols2007v2-pages-119-126.pdf (200).

Not attempted because the previous readers' notes report them blocked and no alternative copy was needed: dl.acm.org (Flautner 2000, Blake 2010, Akkan 2013, Jitter-Trace 2017), phoronix.com, openbenchmarking.org, github.com HTML.

## 2. Candidates

### S1-01 — Intel, "Linux* Power Efficiency Analysis Methods" (2013) — grey (vendor white paper)

Citation. Intel Corporation, *Linux\* Power Efficiency Analysis Methods — A look at power efficiency analysis methods under Linux environments*, white paper dated 7/25/2013, 44 pp. Not peer-reviewed; kept because it is the only literature-class document found that prints a per-process wakeup table for an idle Linux desktop session. (Also within S2's remit as vendor documentation.)

Copy read.
- `S1-01/linux-power-efficiency-analysis-methods-2.pdf` — URL https://www.intel.com/content/dam/develop/external/us/en/documents/linux-power-efficiency-analysis-methods-2.pdf, version: document date "7/25/2013" [p. 1], 44 pages, accessed 2026-09-20, SHA-256 `c9690d620d4353be6592fbeeee910a3a265c3d397d6609abe3c60ef035411a42`

Passages.
> If the goal is to investigate both system and user application efficiency problems, it is best to start the analysis with a fresh-boot system where no extra services or user applications are started. Having a solid baseline helps greatly when trying to pinpoint potential problems without having to weed through many potential problems that can be due to user applications. [p. 7]

> In the above example all three tools were instructed to gather statistics for 10 measurements with a duration of 10 seconds each. Assuming this is an idle analysis scenario, the first metric to check should be the measurement averages to ensure there is no excessive activity. [p. 10]

> Total Wakeups/s 107.2 Total GFX Wakes/s 29.91 Total CPU % 1.93 Table 1: Initial Summary Statistics [p. 10]

> While 107 wakeups per second isn't an excessive number, it is still elevated for a machine that is supposed to be idle. Note also the high graphics activity. This could be due to either the compositor (compiz in this case), or some application triggering the X server frequently. [p. 10]

> /usr/bin/gtk-window-decorator Wakeups 3.86 /usr/lib/gnome-settings-daemon/gnome-settings-daemon Wakeups 0.37 /usr/lib/unity/unity-panel-service Wakeups 0.29 [4] block(softirq) Wakeups 0.28 [7] sched(softirq) Wakeups 0.4 [rcu_sched] Wakeups 0.57 [usb-storage] Wakeups 3.88 blk_delay_work Wakeups 0.81 Clipit Wakeups 64.57 Compiz Wakeups 8.32 hrtimer_wakeup Wakeups 2.17 menu_hrtimer_notify Wakeups 2.94 od_dbs_timer Wakeups 13.07 tick_sched_timer Wakeups 3.22 Table 6: Initial Process Activity [p. 13]

> Judging from the list above, the most apparent offender is clipit. Similarly, the PIDStat output in Table 7 leads to the same conclusion, with the addition of the X server as a potential problem too. However, in most cases, the X server should be assumed to be as efficient as possible at idle (the same assumption goes for the kernel). [p. 13]

> It is a clipboard manager that is waking up 64.57 times per second [p. 13]

> The X server is waking up (or being woken up) 30.9 times every second [p. 13]

> The two major contributors to context switches are again clipit and the X server [p. 13]

Table 7 (Initial PIDStat Output, `pidstat -w -l 10 10`, columns UID PID cswch/s nvcswch/s Command), the rows for the display server, the compositor and the session daemons, read from the table cells [p. 14]:
> 0 1392 30.90 0.83 /usr/bin/X :0 –core –auth /var/run/lightdm/root/:0 tcp vt7 -novtswitch [p. 14]

> 1000 1874 0.37 0.02 /usr/lib/gnome-settings-daemon/gnome-settings-daemon [p. 14]

> 1000 1910 25.10 1.33 compiz [p. 14]

> 1000 2006 3.98 0.11 /usr/bin/gtk-window-decorator [p. 14]

> 1000 2215 36.09 0.91 clipit [p. 14]

> A quick glance over the PIDStat output (Table 8) reveals that the X server is no longer causing 30.9 context switches per second. It is down to a more manageable 1.65. [p. 15]

> Total Wakeups/s 30.19 Total GFX Wakes/s 0.08 Total CPU % 1.17 Table 9: Final Summary Statistics [p. 15]

> The total number of wakeups per second was cut down to 30, which is a good number for a machine running a full desktop environment. CPU utilization has also gone down from 1.93% to 1.17%. Similarly, the number of graphics-related wakeups was slashed to nearly 0, which is likely due to the fact that the X server is no longer being frequently polled. [p. 15]

> Package 0 C-State - C7s-HSW 99.64 % Table 11: Final Processor C-State Statistics [p. 16]

> /usr/bin/python /usr/lib/ubuntu-sso-client/ubuntu-sso-login Wakeups 0.25 /usr/bin/python3.3 /usr/share/oneconf/oneconf-service Wakeups 0.26 /usr/lib/gnome-settings-daemon/gnome-settings-daemon Wakeups 0.37 /usr/lib/udisks2/udisksd --no-debug Wakeups 0.1 /usr/lib/unity/unity-panel-service Wakeups 0.14 /usr/lib/x86_64-linux-gnu/unity-lens-applications/unity-applications-daemon Wakeups 0.26 [3] net_rx(softirq) Wakeups 0.44 [4] block(softirq) Wakeups 0.18 [7] sched(softirq) Wakeups 0.81 [rcu_sched] Wakeups 0.92 [usb-storage] Wakeups 4.01 blk_delay_work Wakeups 0.79 compiz Wakeups 3.37 hrtimer_wakeup Wakeups 1.01 menu_hrtimer_notify Wakeups 1.16 od_dbs_timer Wakeups 10.75 tick_sched_timer Wakeups 2.82 Table 12: Final Process Activity [p. 16]

Table 8 (Final PIDStat Output) rows [p. 15]:
> 0 1392 1.65 0.15 /usr/bin/X :0 -core -auth /var/run/lightdm/root/:0 tcp vt7 -novtswitch [p. 15]

> 1000 1910 21.05 1.34 compiz [p. 15]

Coverage.
- T1: covers, weakly. Object: system daemons at idle (`udisksd --no-debug`, `accounts-daemon`, kernel threads `rcu_sched`, `ksoftirqd/N`, `kworker/N`, `usb-storage`, `jbd2/sda1-8`); unit: wakeups per second (PowerTOP) and voluntary/involuntary context switches per second (pidstat, 10 × 10 s); statistic: per-process averages; scope: one Ubuntu desktop (LightDM, Unity, Compiz; Haswell C-states) at idle, two runs (with and without the clipit clipboard manager); population: one machine. No systemd services appear in the printed rows other than the kernel threads and udisksd (0.1 wakeups/s).
- T2: covers. Object: Xorg (`/usr/bin/X :0`, launched by lightdm) and Compiz (compositor) and `gtk-window-decorator` at an idle desktop; unit: wakeups/s and cswch/s; statistic: per-process average over 100 s; scope: idle desktop, screen state not stated; population: one machine. Values: X 30.90 cswch/s while polled by clipit, 1.65 cswch/s after clipit removed; Compiz 8.32 wakeups/s and 25.10 cswch/s before, 3.37 wakeups/s and 21.05 cswch/s after; "Total GFX Wakes/s" 29.91 before, 0.08 after. No per-frame cost, no drawing state, no audio server.
- T3: covers. Object: the whole idle desktop; unit: total wakeups/s, total CPU %, C7s residency; statistic: averages over 10 × 10 s; values: 107.2 wakeups/s, 1.93 % CPU with clipit; 30.19 wakeups/s, 1.17 % CPU, 99.64 % C7s-HSW without; the per-process split is in Tables 6/7/8/12 (session processes dominate; kernel timers `od_dbs_timer` 13.07 → 10.75 wakeups/s the largest non-session item). No comparison across desktops (GNOME/KDE/Wayland) and no VM/headless contrast.
- T6: does not cover.
- One observation? Yes, one machine, but the machine is named only by its C-state family ("C7s-HSW", i.e. a Haswell client platform), the distribution only by its components (Ubuntu with LightDM/Unity/Compiz/python3.3), the kernel not stated; window 10 × 10 s per tool. Subject state: idle desktop, user logged in. Not a full machine name.

### S1-02 — Siddha, Pallipadi, Van De Ven, "Getting maximum mileage out of tickless" (OLS 2007)

Citation. Suresh Siddha, Venkatesh Pallipadi, Arjan Van De Ven (Intel Open Source Technology Center), "Getting maximum mileage out of tickless", *Proceedings of the Linux Symposium 2007*, Ottawa, vol. 2, pp. 201–208. Reviewed conference proceedings (OLS). 19 years old: within the two-decade limit.

Copy read.
- `S1-02/ols2007v2-pages-201-208.pdf` — URL https://landley.net/kdocs/ols/2007/ols2007v2-pages-201-208.pdf, version: proceedings reprint, 10 pages, accessed 2026-09-20, SHA-256 `cfcb4ca8b5bb465be310ce9897e29e62e1cf34bedaa5c80f9e72a8e49fe126c8`

Passages.
> These measurements reported were taken on a totally idle system, few minutes after reboot. The number of interrupts in the system, per second, is computed by taking the average from output of vmstat. The value reported is the number of interrupts per second on the whole system (all CPUs). The number of events reported is from /proc/timer_stats and the value reported is events per second. [p. 2]

> The system used for the measurement is a Mobile reference system with Intel […] 2 Duo CPUs (2 CPU cores), running i386 kernel with a HZ rate of 1000. [p. 2]

(The elided words are the trademarked "Core" name with its ® and ™ marks, which the PDF text layer renders as separate glyphs.)

> # interrupts #events Avg CPU idle residency (uS) With ticks 2002 59.59 651 Tickless 118 60.60 10161 Table 1: System activity during idle with and without periodic ticks [p. 3]

> ondemand governor monitors each processor utilization at periodic intervals (many times per second) and tries to manage the processor frequency, keeping it close to the processor utilization. When a processor is totally idle, there is no pressing need for ondemand to periodically wakeup the processor just to look at its utilization. To resolve this issue, a new API of deferrable timers was introduced [1] in the recent kernel. [p. 3]

> # interrupts #events Avg CPU idle residency (uS) Ondemand 118 60.60 10161 Ondemand + 89 17.17 20312 deferrable timer Table 2: System activity during idle with and without deferrable timer usage in ondemand [p. 4]

> Tickless idle kernel alone is not sufficient to enable the idle processor to go into long and deep sleeps. In addition to the kernel space, applications in the user space also need to quite down during idle periods, which will ensure that the whole system goes to long sleeps, ultimately saving power (and thus enhancing battery life in case of laptops). [p. 6]

> Number of applications and daemons wakeup at frequent intervals (even on a completely idle system) for performing a periodic activity like polling a device, cursor blinking, querying for a status change to modify the graphical icon accordingly and so on (for more information about the mischeivous application behaviors look into references [9, 10, 2]). [p. 6]

> For example, the hal daemon used to poll very frequently to check for media changes and thus making the idle processor wakeup often. Newer SATA hardware supports a feature called Asynchronous Notification, which will notify the host at a media change event. With the recent changes in the community, hal daemon will avoid the polling on platforms which has the support of this asynchronous notification. [p. 6]

> For example all gnome applications use the glib timer g_timeout_add() API for their timers, which expire at scattered instances. A second API, g_timeout_add_seconds() has now been added which causes all recurring timers to happen at the start of the second, enabling the system wide grouping of timers. The start of the second is offset by a value which is system wide but system-specific to prevent all Linux machines on the internet doing network traffic at the same time. [p. 6]

Coverage.
- T1: covers, as mechanism and as an aggregate observation. Mechanism: deferrable timers for the ondemand governor, `__round_jiffies()` coalescing, glib `g_timeout_add_seconds()` grouping, hald polling replaced by SATA asynchronous notification (no interval stated). Observation: whole-system interrupts/s and timer events/s at idle (2002 → 118 interrupts/s, 59.59 → 60.60 events/s with dynticks; 118 → 89 and 60.60 → 17.17 with deferrable ondemand timers), average idle residency 651 → 10161 → 20312 µs. No per-daemon rows.
- T2: does not cover (no display or audio server).
- T3: covers, aggregate only: an idle Linux system's timer-event and interrupt rate; whether a desktop session was running is not stated ("totally idle system, few minutes after reboot").
- T6: does not cover.
- One observation? Yes: "Mobile reference system with Intel Core 2 Duo CPUs (2 CPU cores), running i386 kernel with a HZ rate of 1000", state idle a few minutes after reboot, window not stated (vmstat average). Distribution and session not named.

### S1-03 — Srinivasan, Shenoy, Vaddagiri, Sarma, Pallipadi, "Energy-aware task and interrupt management in Linux" (OLS 2008)

Citation. Vaidyanathan Srinivasan, Gautham R Shenoy, Srivatsa Vaddagiri, Dipankar Sarma (IBM Linux Technology Center), Venkatesh Pallipadi (Intel OTC), "Energy-aware task and interrupt management in Linux", *Proceedings of the Linux Symposium 2008*, Ottawa, vol. 2, pp. 187–200 (page headers "2008 Linux Symposium, Volume Two • 187–"). Reviewed conference proceedings.

Copy read.
- `S1-03/ols-2008-srinivasan-energy.pdf` — URL http://www.cs.columbia.edu/~nahum/w6998/papers/ols-2008-srinivasan-energy.pdf (course mirror of the OLS reprint), 14 pages, accessed 2026-09-20, SHA-256 `3a46261c74e7a4c839ecd5800104aab983f1f217c938ff85876ed707a168f6de`

Passages.
> Since cpu load is sampled periodically, it is possible that short lived tasks (ex: daemon that run periodically for short intervals of time) don't show up as cpu load, which can result in failure to consolidate on fewer cpus/chips. This is discussed in detail in the Section 3.5. Typically the total CPU time utilised by the daemons in an idle system will be less than 1% but the distribution of this jobs across all CPUs influence the CPU's low power sleep time thereby affecting the power consumption at idle. [p. 2]

> The daemon process that are running in an idle system can be easily identified using ps or top commands. [p. 3]

> Other than the processes that use CPU time, there could be interrupts from IO devices like ethernet and harddisk that wakeup CPUs and consume power. Timers programmed by applications and device drivers are actually interrupts that wakeup CPUs when the timer expires. [p. 4]

> In a typical distro installation,1 CPU utilisation from top and process wakeup rate from powertop at idle are shown in Table 3.1. The number of interrupts observed during the 15-second duration is listed in Table 1. [p. 4]

> 1Fedora 9 beta was used in this experiment. [p. 4]

> Actually this experiment was done on a two socket dual core system and such histograms are available for each of the four CPUs. [p. 4]

> As observed in the histogram, the maximum idle time was 2 seconds while most of the samples are concentrated at less than 10ms. There is a pattern of 1s idle time as well. [p. 4]

> Utilisation from top: Cpu(s): 0.0%us, 0.1%sy, 0.0%ni, 99.9%id, 0.0%wa, 0.0%hi, 0.0%si, 0.0%st Output of powertop -d: PowerTOP 1.8 (C) 2007 Intel Corporation Collecting data for 15 seconds [p. 5]

> Wakeups-from-idle per second : 10.8 interval: 15.0s Top causes for wakeups: 28.7% ( 4.0) <kernel module> : usb_hcd_poll_rh_status (rh_timer_func) 27.3% ( 3.8) <interrupt> : eth0 10.0% ( 1.4) <interrupt> : ata_piix 7.2% ( 1.0) ip : bnx2_open (bnx2_timer) [p. 5]

> The maximum sleep time was 400ms while the typical sleep time was less than 10ms. [p. 5]

Coverage.
- T1: covers, aggregate and as a claim. Object: the daemons of an idle Fedora 9 beta server install; unit: CPU share ("less than 1%", a stated typical value, not a measured row) and wakeups-from-idle per second (PowerTOP 1.8, 15 s); statistic: total 10.8 wakeups/s with the top four causes all kernel or device timers (USB root-hub poll 4.0/s, eth0 3.8/s, ata_piix 1.4/s, bnx2 timer 1.0/s) — no user-space daemon in the printed top list. Also the idle-period histogram: average idle 565 ms, average sleep 137 ms on CPU0 (figure captions "CPU0 Average = 565ms" and "CPU0 Average = 137ms" [p. 4–5]).
- T2: does not cover (server, no display server).
- T3: covers, for a headless/server idle population: 10.8 wakeups/s total at 99.9 % idle on a two-socket dual-core server. This is the headless counterpart to the desktop figures in S1-01 (107 / 30 wakeups/s), different machines and years.
- T6: does not cover (the paper is about consolidating daemons and interrupts onto one package for power).
- One observation? Yes: Fedora 9 beta, two-socket dual-core (4 CPU) system with bnx2 and eth0 NICs, state idle, window 15 s (PowerTOP) and 120 s (idle histogram). Exact CPU model not named.

### S1-04 — Yang, Liu, Berger, Kaplan, Moss, "Redline: First Class Support for Interactivity in Commodity Operating Systems" (OSDI 2008)

Citation. Ting Yang, Tongping Liu, Emery D. Berger, Scott F. Kaplan, J. Eliot B. Moss, "Redline: First Class Support for Interactivity in Commodity Operating Systems", *8th USENIX Symposium on Operating Systems Design and Implementation (OSDI '08)*, pp. 73–86. Peer-reviewed.

Copy read.
- `S1-04/yang.pdf` — URL https://www.usenix.org/legacy/event/osdi08/tech/full_papers/yang/yang.pdf, 14 pages, accessed 2026-09-20, SHA-256 `f1abb8705461d50ba2db2833d9a4fff61fa4a122c16b45ac00e4c8c077b47f0a`

Passages.
> These specifications are concise, consisting of just a few parameters (Section 3), and are straightforward to generate: a graduate student was able to write specifications for a suite of about 100 applications—including Linux's latency-sensitive daemons—in just one day. [p. 1]

> 1. Interactive (Iact): response-time sensitive tasks that provide services in response to external requests or events. These include not only tasks that interact with users, but also tasks that serve requests from other tasks, such as kernel daemons; [p. 2]

> Specifically, the graphical user interface (e.g., the X Windows server, the window/desktop manager) comprise a set of tasks that must be given specifications to ensure that the user interface remains responsive. Similarly, specifications for a range of kernel threads and daemons allow Redline to ensure that the system remains stable. [p. 3]

> While most kernel threads and daemons are not CPU intensive, they are response-time sensitive, so their reservation period should be in the tens of milliseconds. Finally, for interactive applications like a movie player, the reservation period should be around 30 ms to ensure 30 frames per second, which implies that the X server and window/desktop manager should also use the same reservation period. [p. 3]

> We use a Linux kernel (version 2.6.22.5) patched with the CFS scheduler (version 20.3) as our control. Redline is implemented as a patch to this same Linux version. For all experiments, the screen resolution was set to 1600 x 1200 pixels. [p. 9]

> It includes the init process, kjournald, the X11 server Xorg, KDE's desktop/window manager, the bash shell, and several typical interactive applications. [p. 9]

Table 1 (task specifications C:T in ms) rows [p. 9]:
> init 2:50 kjournald 10:100 Xorg 15:30 kdeinit 2:30 kwin 3:30 kdesktop 3:30 bash 5:100 vim 5:100 mplayer 5:30 [p. 9]

> Xorg requires a good deal of CPU bandwidth to update the screen. However, the CFS scheduler gives the same CPU share to all runnable tasks, allowing the window manager to submit screen update requests faster than Xorg can process them. [p. 10]

> In Redline, mplayer plays the movie smoothly no matter how quickly we move the window, even though Xorg and all of the tasks comprising the GUI are themselves interactive tasks. We believe that because Xorg effectively gets more bandwidth (50% reserved plus proportional sharing with other tasks), and the EDF scheduler causes mplayer add its requests into Xorg's service queue earlier. [p. 11]

Coverage.
- T1: does not cover as observation. The reservation values it assigns to `init` (2 ms per 50 ms) and `kjournald` (10 ms per 100 ms) are the paper's treatment choices (its "specifications"), recorded as a treatment fact of a research prototype, not a shipped treatment and not a behaviour value.
- T2: covers as argument, weakly as observation. Argument: the X server and window manager need the same reservation period as a 30 fps player; Xorg "requires a good deal of CPU bandwidth to update the screen"; under CFS the window manager can flood Xorg. Observation: mplayer frame rate under Linux CFS vs Redline while a window is dragged (Figure 6, curve only, no per-frame CPU of Xorg/kwin printed). Treatment fact: Xorg 15 ms per 30 ms (50 %), kwin and kdesktop 3 ms per 30 ms in the prototype. No wake cadence, no idle behaviour.
- T3: does not cover.
- T6: covers. How an interactivity scheduler treats daemons and the GUI: kernel daemons and system daemons classed as "interactive" (response-time sensitive, not CPU intensive) with tens-of-millisecond periods; the GUI stack (Xorg, window/desktop manager) given reservations; interference workloads are memory bombs, fork bombs and I/O-heavy background tasks, not the daemons themselves. No CPU/run/wait figures for daemons.
- One observation? Yes: Linux 2.6.22.5 + CFS v20.3, KDE (Xorg, kwin, kdesktop), 1600 × 1200, machine partially named (Intel 82865G integrated graphics, Fujitsu 5400 rpm ATA disk, HyperThreaded processor [p. 9]), states: video playing while a window is dragged and under memory/fork/I/O bombs; window ≈ 160 s per figure; each experiment run 30 times.

### S1-05 — Cucinotta, Faggioli, Bagnoli, "Low-Latency Audio on Linux by Means of Real-Time Scheduling" (LAC 2011)

Citation. Tommaso Cucinotta, Dario Faggioli, Giacomo Bagnoli (Scuola Superiore Sant'Anna), "Low-Latency Audio on Linux by Means of Real-Time Scheduling", *Proceedings of the Linux Audio Conference 2011 (LAC 2011)*, Maynooth, paper 46, 8 pp. Reviewed conference paper.

Copy read.
- `S1-05/46.pdf` — URL https://lac.linuxaudio.org/2011/papers/46.pdf, 8 pages, accessed 2026-09-20, SHA-256 `1ad5f386f8ba18dc7a1af0325f09532efbd79bbaa68d011cb8e10bad9bfe1dea`
- `S1-05/lac2011-index.html` — URL https://lac.linuxaudio.org/2011/?page=program (used to identify paper 46 as this title), accessed 2026-09-20, SHA-256 `7b0445f3f8b02aea4828d86f0db3b664336df236ac69b0de41a0e9c8aeb89f04`
- `S1-05/lac2011.html` — URL https://lac.linuxaudio.org/2011/papers/ (directory index), accessed 2026-09-20, SHA-256 `ddc43fdafde799226bb9abfb846d60f260eaa624aa052fb2c8051b7cfa693fe9`

Passages.
> Though, on a nowadays GNU/Linux system, we may easily find a variety of applications with tight timing constraints that might benefit from precise scheduling guarantees, in order to provide near-professional quality of the user experience, e.g., audio acquisition and playback, multimedia (video, gaming, etc.) display, video acquisition (v4l2), just to cite a few of them. In such a challenging scenario in which we can easily find a few tens of threads of execution with potentially tight real-time requirements, an accurate set-up of real-time priorities may easily become cumbersome, especially for the user of the system, who is usually left alone with such critical decisions as setting the real-time priority of a multimedia task. [p. 1]

> All experiments have been performed on a common consumer PC (Intel(R) E8400@3.00 GHz) with CPU dynamic voltage-scaling disabled, and with a Terratec EWX24/96 PCI sound card. [p. 3]

> First of all the audio driver timing in a configuration where no clients were attached to JACK has been measured, and results are shown in Table 1. JACK was using a buffer-size of 128 samples and a sample-rate of 96 kHz, resulting in a period of 1333µs. Since, in this case, no other activities were running concurrently (and since the system load was being kept as low as possible), the statistics reveal a correct behaviour of all the tested scheduling strategies, with CFS exhibiting the highest variability, as it could have been expected. [p. 4]

> Table 1: Audio driver timing of JACK with no clients using the 4 different schedulers (values are in µs). Min Max Average Std. Dev CFS 1268 1555 1342.769 3.028 FIFO 1243 1423 1333.268 2.421 AQuoSA 1279 1389 1333.268 2.704 SHRUB 1275 1344 1333.268 2.692 [p. 4]

> In all of the following experiments, we used a "fake" JACK client, dnl, constituted by a simple loop taking about 7% of the CPU for its computations. The audio processing pipeline of JACK is made up of 10 dnl clients, added one after the other. This leads to a total of 75% CPU utilisation. [p. 4]

> In this experiment, JACK is configured with a sample-rate of 96 kHz and a buffer-size of 128 samples, resulting in an activation period of 1333µs, while rt-app has period of 40ms and execution time of 5ms. This configuration for rt-app makes it resemble the typical workload produced by a video (e.g., MPEG format) decoder/player, displaying a video at 25 frames per second. [p. 4]

> The best effort Linux scheduler manages to keep the JACK performance good, but rt-app undergoes increased response-times and exhibits deadline misses in correspondence of the start and termination of JACK clients. [p. 4]

Coverage.
- T1: does not cover.
- T2: covers, for the audio server JACK (not PipeWire/PulseAudio). Object: JACK2 server real-time thread and its clients; unit: driver activation interval (µs) per cycle, CPU time per cycle (Figure 1c, curve only); statistic: min/max/mean/sd over a 1-minute run; scope: one PC, period 1333 µs (128 frames at 96 kHz) and 2666 µs (128 at 48 kHz), states "no clients" and "10 synthetic clients at 75 % CPU" with a 25 fps-like or VoIP-like competing task; population: one machine. Wake cadence of the audio server is the configured period: measured mean 1342.8 µs under CFS (sd 3.0), 1333.3 µs under FIFO (sd 2.4). No idle/suspended-node behaviour, no PipeWire.
- T3: does not cover.
- T6: covers, as argument and observation: an audio server under CFS holds its period but a co-scheduled periodic task misses deadlines when JACK clients start and stop; SCHED_FIFO and reservation schedulers (AQuoSA/SHRUB) restore isolation; the paper argues "a few tens of threads" with tight timing exist on a desktop and that priority assignment by the user is cumbersome, motivating reservations.
- One observation? Yes: Intel E8400 @ 3.00 GHz, DVFS disabled, Terratec EWX24/96, Linux with AQuoSA patch (kernel version not stated in the text read), JACK2, states named, window 1 minute per experiment.

### S1-06 — Cucinotta, Checconi, Abeni, Palopoli, "Self-tuning Schedulers for Legacy Real-Time Applications" (EuroSys 2010)

Citation. Tommaso Cucinotta, Fabio Checconi, Luca Abeni, Luigi Palopoli, "Self-tuning Schedulers for Legacy Real-Time Applications", *Proceedings of the 5th European Conference on Computer Systems (EuroSys 2010)*, Paris, pp. 55–68. Peer-reviewed.

Copy read.
- `S1-06/EuroSys-2010.pdf` — URL https://www.iris.sssup.it/retrieve/dd9e0b32-0a70-709e-e053-3705fe0a83fd/EuroSys-2010.pdf (author copy via http://hdl.handle.net/11382/304382), 13 pages, accessed 2026-09-20, SHA-256 `a343a69f11db6333c0b1a3746335ab4147f45a62f4bab802ef64511b4c3c0dab`
- `S1-06/iris-304382.html` — URL https://www.iris.sssup.it/handle/11382/304382 (record page), accessed 2026-09-20, SHA-256 `3e0267c58fa60064619c02da0eb2005d1085e98304d3a7cd97e3442663caeb05`

Passages.
> We present an approach for adaptive scheduling of soft real-time legacy applications (for which no timing information is exposed to the system). Our strategy is based on the combination of two techniques: 1) a real-time monitor that observes the sequence of events generated by the application to infer its activation period, 2) a feedback mechanism that adapts the scheduling parameters to ensure a timely execution of the application. [p. 1]

> The machine used for the tests is based on an Intel(R) Core(TM) 2 Duo CPU at 2.6 GHz, with an operating frequency fixed at 800 MHz, running an Ubuntu 9.04 Linux Operating System. [p. 8]

> Many of the experiments have been performed by using mplayer2, a popular media player for Linux. [p. 8]

Coverage.
- T1, T2, T3: does not cover (the subject is a media player application, mplayer, not a session service; no audio server or display server is measured).
- T6: covers marginally, as argument: a latency-sensitive legacy multimedia application on a Linux desktop (Ubuntu 9.04, kernel 2.6.29 with AQuoSA) is argued to need a reservation inferred from its observed activation period rather than a user-set priority. No daemon or session-process figures.
- One observation? Yes (Core 2 Duo 2.6 GHz fixed at 800 MHz, Ubuntu 9.04, Linux 2.6.29 + AQuoSA, mplayer playing video/MP3, windows of a few minutes), but of an application, not of a daemon or session process. Kept as a weak T6 pointer only.

### S1-07 — Taymans, "PipeWire: A Low-Level Multimedia Subsystem" (LAC 2020)

Citation. Wim Taymans (Red Hat), "PipeWire: A Low-Level Multimedia Subsystem", *Proceedings of the 18th Linux Audio Conference (LAC-20)*, SCRIME, Université de Bordeaux, 25–27 November 2020, 6 pp. Reviewed conference paper; authored by the project's maintainer, so it doubles as primary documentation (S2's remit).

Copy read.
- `S1-07/PipeWire-LAC2020.pdf` — URL https://lac2020.sciencesconf.org/307881/PipeWire.pdf, 6 pages, accessed 2026-09-20, SHA-256 `8c65e0d4a91fc25b4f8a71fae3f7abe19dfeb1513f29c0dd63e5aa34968cdc21`

Passages.
> JACK maintains a graph of applications (clients) that are connected using ports. In contrast to the previous audio servers, JACK will use the device interrupt to wake up each client in the graph in turn to process data. This makes it possible to keep the delay between processing and recording/playback very low. [p. 1]

> PulseAudio is optimized for power saving and does not handle low-latency audio very well, the code paths to wake up a client are in general too CPU hungry. [p. 2]

> eventfd is used to wakeup nodes when they need to process input buffers and produce output buffers. timerfd is used to measure when a devices will be empty/filled. The timeout is adjusted based on the fill level of the device and a DLL. By using a timer, we can also dynamically adjust the period size based on client requirements. It is also possible to write the device wakeup using the traditional IRQ based approach but that does not provide flexible period adjustments. [p. 2]

> When a device needs more data (or has more data, in case of a source), the graph is woken up. PipeWire uses the same concepts as JACK2 to schedule the processing graph. It keeps track of dependencies between nodes and nodes are informed about the peer nodes they are linked to. When processing starts, all nodes without dependencies are scheduled (sources). When they complete, dependencies are satisfied on their peer nodes, which are then scheduled, and so on until the whole graph is completed. Nodes that complete can directly wake up their peers by signaling the eventfd without having to wake up the PipeWire daemon. [p. 2]

> The clock slaving and resampling algorithm is inspired by zita-ajbridge [12]. It however runs in a single thread and uses a DLL to drive the resampler by matching its device fill level to the graph period size. [p. 2]

Coverage.
- T1: does not cover.
- T2: covers as mechanism only. What PipeWire does per audio period: a timerfd programmed from the device fill level and a DLL wakes the graph once per period; nodes wake their peers through eventfd without the daemon; period size is adjustable per client requirement; resampling runs in a single thread. What PulseAudio does: wake paths described as "too CPU hungry" for low latency (a claim, no figure). No idle/suspend behaviour, no thread count, no scheduling policy (rtkit is not mentioned in the text read), no measurement.
- T3, T6: does not cover.
- One observation? No — a design description; no machine, subject state or window.

### S1-08 — Gleonec, "Pipewire as the heart of Linux-based audio systems" (Embedded Recipes 2023) — grey (conference slides)

Citation. Philip-Dylan Gleonec (Savoir-faire Linux), "Pipewire as the heart of Linux-based audio systems", slide deck, Embedded Recipes, Paris, 28 September 2023, 26 slides. Not peer-reviewed; kept because it is the only literature-class source found that prints measured CPU load of PipeWire, JACK and PulseAudio servers while streams play, on Linux.

Copy read.
- `S1-08/Pipewire-embedded-recipes-2023.pdf` — URL https://embedded-recipes.org/2023/wp-content/uploads/2023/10/Pipewire-as-the-heart-of-Linux-based-audio-systems-Philip-Dylan-Gleonec-compressed.pdf, 26 slides, accessed 2026-09-20, SHA-256 `87a0a8992e2008633ec706f062688c4ca4f89b3330ca1c5b647b28aeb3693d17`

Passages.
> Evaluated on i.MX8M Nano EVK + CS42448 - One codec, no asynchronous interfaces ● Distribution based on Yocto Kirkstone ● Kernel linux-imx v5.4 ● Use-case : karaoke using CamillaDSP framework [slide 11]

> Measurements done : - CPU consumption - Latency [slide 11]

> Backend CamillaDSP load Server load JACK 28% 18% Pipewire 16% 14% We observe both latency and CPU load reduction! [slide 13]

> 60ms latency measured with Pulseaudio [slide 14]

> To make measurements « fair », we configured Pipewire and JACK to increase their latency to 60ms [slide 14]

> Pipewire needs an external Pipewire-pulse process, which is CPU consuming [slide 14]

> Backend CamillaDSP load Server load JACK 26.1% 14.1% Pulseaudio 26.7% 35.1% Pipewire (JACK API) 14.3% 10.5% Pipewire (Pulseaudio API) 35.6% 41.7% (17.4% PW + 24.3% PW-pulse) [slide 14]

> CPU load measurements have been measured with htop and perf - Htop measures global CPU usage - Perf measures CPU usage by functions [slide 16]

Coverage.
- T1: does not cover.
- T2: covers, for the audio server while a stream plays, on embedded Linux (not a desktop). Object: the audio server process (JACK, PulseAudio, PipeWire; PipeWire split into `pipewire` and `pipewire-pulse`); unit: CPU load in % (htop, whole-process share of one core, core count of the i.MX8M Nano not stated on the slide); statistic: single reported values; scope: karaoke DSP pipeline (CamillaDSP) playing through a CS42448 codec, at the servers' default latency (slide 13) and at 60 ms latency for all (slide 14); population: one board. Values: server load JACK 18 % / PipeWire 14 % (default latency); at 60 ms: JACK 14.1 %, PulseAudio 35.1 %, PipeWire-JACK-API 10.5 %, PipeWire-Pulse-API 41.7 % (17.4 % PW + 24.3 % PW-pulse). No idle state, no per-wake cost, no thread structure.
- T3, T6: does not cover.
- One observation? Yes: NXP i.MX8M Nano EVK with CS42448 codec, Yocto Kirkstone, kernel linux-imx v5.4, state "playing a karaoke DSP graph", window not stated. Embedded board, not a desktop, so an ARM Linux observation of an audio server under load.

### S1-09 — Min, "Optimizing Scheduler for Linux Gaming" (OSS NA 2024) and "Using sched_ext to improve frame rates on the SteamDeck" (LPC 2024) — grey (conference slides)

Citation. Changwoo Min (Igalia), "Optimizing Scheduler for Linux Gaming", slide deck, Open Source Summit North America, 17 April 2024, 30 slides; and "Using sched_ext to improve frame rates on the SteamDeck — Ideas behind the LAVD scheduler", slide deck, Linux Plumbers Conference 2024 (sched_ext microconference), 18 September 2024, 20 slides. Not peer-reviewed; kept because the decks print a `perf sched`-derived characterisation of a Linux game session in which system tasks (Wine, graphics and audio servers) are counted with their share of scheduling.

Copy read.
- `S1-09/scx-lavd-oss-na24.pdf` — URL https://static.sched.com/hosted_files/ossna2024/9b/scx-lavd-oss-na24.pdf, 30 slides, accessed 2026-09-20, SHA-256 `e62d69cd401021f8bfedadde2c4de62b01383facaa83acce7d218af3b6402475`
- `S1-09/scx_lavd-lpc-mc-24.pdf` — URL https://lpc.events/event/18/contributions/1713/attachments/1425/3058/scx_lavd-lpc-mc-24.pdf, 20 slides, accessed 2026-09-20, SHA-256 `77c9cefec98e0346d5b89a219ca30eff7cb4f448016b24fa0871b286ba421eb4`

Passages (OSS NA 2024 deck).
> SteamDeck runs x86 Windows games! ● AMD APU ○ AMD Van Gogh: x86 8-core CPU + AMD GPU ● SteamOS ○ Arch-Linux based Linux distribution [slide 4]

> We collect and analyze all scheduling activities while playing games. [slide 10]

> Around 300 tasks are scheduled while running a game. ○ Around 90% are long-living tasks; only 10% of tasks are terminated. ● Top 30-40 most frequently scheduled tasks take 95% of scheduling. ○ Around half of them are system tasks -- especially, wine, graphics, and audio servers, taking 30--40% of scheduling. ○ There are 15-20 game-specific tasks, which takes 60-70% scheduling. ● CPU utilization is moderately high -- around 65-95%, but not overloaded (i.e., no 100%). [slide 12]

> In general, tasks run for very short duration – roughly a few 100s usec on average to a few msec maximum. ● Task execution time is very stable and is predictable using its average. [slide 13]

> Some coordination tasks run very shortly (e.g., wineserver:260 usec) but some work tasks (e.g., a task worker: 1.65 msec) run longer than average. [slide 13]

> Preemption (e.g., timer interrupt) takes only 25-30% of scheduling. ● 70-75% of scheduling is initiated by waiting system calls – such as epoll, pipe_read, futex_wait, etc. [slide 14]

> Wait time from one schedule to another schedule is a task's behavioral property. Each task's wait time is pretty constant. [slide 15]

Passages (LPC 2024 deck).
> Implications of wake-up/wait frequency ○ High wake up frequency ⇒ important producer in a task graph ○ High wait frequency ⇒ important consumer in a task graph ○ Both are high ⇒ important task in the middle [slide 9]

> We want to make each and every task run in a fixed time interval. ○ a fixed time interval == targeted latency (e.g., 15 msec) [slide 10]

Coverage.
- T1: does not cover (system services are not separated from "system tasks").
- T2: covers, weakly, for the session under load: "graphics, and audio servers" are named among the system tasks that, with Wine, take 30–40 % of scheduling events while a game runs; per-task run time per schedule is "a few 100s usec on average to a few msec maximum"; no per-process rows for the compositor (gamescope) or the audio server (PipeWire) are printed, no idle state.
- T3: does not cover (not idle; the population figure of ~300 scheduled tasks, 90 % long-lived, is under a game).
- T6: covers. How a scheduler evaluation treats system services and the session: as part of a wake-up task graph in which system tasks (Wine, graphics and audio servers) are ~half of the 30–40 most-scheduled tasks and take 30–40 % of scheduling; 70–75 % of schedules are initiated by blocking system calls, 25–30 % by preemption; wake-up and wait frequency define latency criticality and a task's virtual deadline. Figures are shares of scheduling events, not CPU time.
- One observation? Partly: machine Steam Deck (AMD Van Gogh, 8-core x86 APU) and SteamOS (Arch-based) are named on slide 4; the game(s) traced, kernel version, and trace window are not named on the slides; the figures are summarised over "a lot of scheduling traces" [slide 11]. Not a single named observation.

### S1-10 — Edge (LWN), "Lessons from creating a gaming-oriented scheduler" (LPC 2025 report, 2026)

Citation. Jake Edge, "Lessons from creating a gaming-oriented scheduler", LWN.net, 7 January 2026, report on Changwoo Min's session in the Gaming on Linux microconference, Linux Plumbers Conference 2025 (Tokyo, December 2025), https://lwn.net/Articles/1051430/. Journalism (conference report), grey; complements S1-09 with the method (VaporMark on `perf sched record`) and per-task run-time ranges.

Copy read.
- `S1-10/lwn-1051430.html` — URL https://lwn.net/Articles/1051430/, HTML as served on 2026-09-20 (article plus reader comments), SHA-256 `c448c34f9d84243a776f6683627b6a15806dfee59d46583986606c426e3badc6`

Passages (from the article body; the page has no pagination, locators are section headings).
> Most of the tasks are fairly short running, around 1ms, though there are a few that run for 2-3ms or more. There are also tasks that run for less than 100µs, which means there is more flexibility in terms of their task placement, he said. [§ Gaming workloads]

> So he developed VaporMark—the name refers to Steam—which analyzes data collected using "perf sched record". [§ Gaming workloads]

> The key finding that came out of his analysis is perhaps somewhat obvious: a single high-level action, such as moving a character on-screen and emitting a sound based on a key-press event, requires that many tasks work together. Some of the tasks are threads in the game process, but others are not because they are in the game engine, kernel, and device drivers; there are often 20 or 30 tasks in a chain that all need to collaborate. Finding tasks with a high waker or wakee frequency and prioritizing them is the basis of the LAVD scheduling policy. [§ Gaming workloads]

> So, microbenchmarks are of interest as well, but most of the ones he has found for schedulers (e.g. stress-ng and hackbench) are focused on stressing schedulers and measuring the scheduling overhead. That is useful, but improving those numbers does not always lead to better game performance. [§ Benchmarking]

> There are some microbenchmarks that mimic specific workloads; one example is schbench, which is meant to reproduce the scheduling characteristics of production web-server workloads. There is a need for something like that to mimic gaming workloads, he said. [§ Benchmarking]

Coverage.
- T1, T3: does not cover.
- T2: covers marginally: the chain from key press to display and sound spans 20–30 tasks including kernel and driver tasks; no compositor/audio-server rows.
- T6: covers, as an account of how a scheduler developer treats the session's task chain (game, engine, kernel, drivers, and — per S1-09 — graphics and audio servers) as a wake-up graph, and of what existing scheduler benchmarks (hackbench, stress-ng, schbench) do not represent. Figures: per-task run times ~1 ms typical, 2–3 ms for a few, < 100 µs for others.
- One observation? No machine, game or window named in the article text (the underlying traces are the ones of S1-09).

### S1-11 — Corbet (LWN), "The many faces of 'latency nice'" (OSPM 2020 report) and "Improved response times with latency nice" (2022)

Citation. Jonathan Corbet, "The many faces of 'latency nice'", LWN.net, 18 May 2020, report from the 2020 Power Management and Scheduling in the Linux Kernel summit (OSPM), https://lwn.net/Articles/820659/; Jonathan Corbet, "Improved response times with latency nice", LWN.net, 17 March 2022, https://lwn.net/Articles/887842/. Conference report and kernel-development journalism, grey.

Copy read.
- `S1-11/lwn-820659.html` — URL https://lwn.net/Articles/820659/, HTML as served 2026-09-20, SHA-256 `fa83d2a75a34bad9f8917efc51b16172ca237c30951d7b422ac8e7164fd52ccf`
- `S1-11/lwn-887842.html` — URL https://lwn.net/Articles/887842/, HTML as served 2026-09-20, SHA-256 `52634d036f0a1a8c4373f45fd055db402b3f7863e574dfb9f467f11057436d39`

Passages (820659).
> The initial effect of this feature is to control how hard the scheduler will look for an idle core to place a task on when it wakes up. This search takes time (thus increasing latency); an idle core may also have to be roused out of a sleep state, increasing latency further. Dhaval Giani pointed out a use case that Oracle cares about, where some latency-sensitive tasks will typically run for very short periods — less than the time spent searching for an idle core sometimes. [§ A different kind of nice]

> Eggemann took over the presentation at this point to talk about what the Android developers would like to see. Android currently uses a control-group interface that includes a "prefer idle" attribute; setting that will bias CPU selection toward an idle CPU. [§ Control groups]

Passages (887842).
> Even then, users can become grumpy if specific processes do not get their CPU share quickly; from that comes years of debates over desktop responsiveness, for example. The latency-nice priority proposal recently resurrected by Vincent Guittot aims to provide a new tool to help latency-sensitive applications get their CPU time more quickly. [§ opening]

> The traditional Unix "nice" value can be used to raise a process's priority, for example. That can work, but a process's niceness does not directly translate into latency; it controls how much of the available CPU time the process can consume, but not when the process can actually run. Using the realtime priorities will cause the scheduler to run a process quickly, especially if realtime preemption is enabled, but a process running at that priority can also take over the system. [§ opening]

> Whenever a blocked process wakes, the scheduler must decide whether to run it immediately or to put it into a run queue and make it wait for a CPU. A number of factors go into that decision now; the latency-nice mechanism adds another. If the new process has a higher latency-nice priority than the process that is running in a CPU, and that new process has available CPU time in its current slice, then the new process can preempt the running process. [§ opening]

Coverage.
- T1, T2, T3: does not cover.
- T6: covers as argument only: why latency-sensitive tasks are argued to need a scheduler hint distinct from nice (nice controls share, not when a task runs; real-time priority can take over the system); the use cases quoted are Oracle/Facebook/IBM/Android workloads, not audio servers or compositors (an audio use case appears only in reader comments, which are not quoted). No figures.
- One observation? No.

### S1-12 — Fleming (LWN), "A survey of scheduler benchmarks" (2017)

Citation. Matt Fleming, "A survey of scheduler benchmarks", LWN.net, 14 June 2017, https://lwn.net/Articles/725238/. Kernel-development journalism, grey.

Copy read.
- `S1-12/lwn-725238.html` — URL https://lwn.net/Articles/725238/, HTML as served 2026-09-20, SHA-256 `d4a87c9da6b57fa55837c3fccb3e179397030fff34ff661ac18e022d76a03a57`

Passages.
> Hackbench is a message-passing scheduler benchmark that allows developers to [§ Hackbench]

> The output of the benchmark is the average scheduler wakeup latency — the duration between telling a task it needs to wake up to perform work and that task running on a CPU. [§ Hackbench]

> One benchmark that does provide detailed latency distribution statistics for scheduler wakeups is schbench. It allows users to configure the usual parameters — such as number of tasks and test duration — but also the time between wakeups (--sleeptime), time spinning once woken (--cputime); it also has the ability to automatically increase the task count until the 99th percentile wakeup latencies become extreme. [§ Schbench]

> It was originally created by Giacomo Bagnoli as part of his master's thesis so that he could create background tasks to induce scheduler latency and test his Linux kernel changes for low-latency audio. [§ Rt-app]

Coverage.
- T1, T2, T3: does not cover.
- T6: covers, as an account of how the kernel's scheduler benchmarks treat the rest of the system: hackbench, `perf bench sched pipe`, schbench and rt-app are synthetic wake-up/latency loads that do not model daemons; rt-app's origin is explicitly a synthetic "background task" generator built to test low-latency audio scheduling (the JACK work of S1-05). No figures on daemons.
- One observation? No.

### S1-13 — Akkan, Lang, Liebrock, "Stepping towards a noiseless Linux environment" (ROSS 2012, slides)

Citation. Hakan Akkan, Michael Lang, Lorie Liebrock (New Mexico Tech / Los Alamos), "Stepping Towards a Noiseless Linux Environment", slides presented (by Abhishek Kulkarni) at the 2nd International Workshop on Runtime and Operating Systems for Supercomputers (ROSS 2012), Venice, 29 June 2012, 31 slides. The paper is peer-reviewed (ACM, doi 10.1145/2318916.2318925) but only the slides were reachable; the slides are cited.

Copy read.
- `S1-13/ross2012-akkan.pdf` — URL https://htor.inf.ethz.ch/ross2012/slides/ross2012-akkan.pdf, 31 slides, accessed 2026-09-20, SHA-256 `a5f93704622e8ab9e958419ec4e720fbb86e108761a85cc314f2c1d6294bced0`

Passages.
> Low frequency, Long duration noise • System services, daemons • Can be moved to separate cores • High frequency, Short duration noise • OS clock ticks • Not as easy to synchronize - usually much more frequent and shorter than the computation granularity of the application [slide 5]

> 8904772 Local timer interrupts 4780062 Rescheduling interrupts 1922138 TLB shootdowns 851563 PCI-MSI-edge eth1 100687 PCI-MSI-edge eth0 57104 Function call interrupts 41456 IO-APIC-fasteoi ioc0 11112 Machine check polls 7564 PCI-MSI-edge ib_mthca-comp@pci:0000:47:00.0 (on a 24 core Linux 2.6.x machine with hz=100) [slide 9]

> A kernel thread was woken up periodically (every second) to refresh VM statistics! [slide 11]

> Tests run on a 4 socket, 6 core AMD machine with 16 MPI processes • Pinned to cores 3,4,5,6 on each NUMA domain (first 2 cores were reserved for the OS) [slide 14]

> Difficult to disable certain kernel threads (such as kworker) without source-level changes [slide 13]

Coverage.
- T1: covers, weakly and for a server: a kernel thread refreshing VM statistics every second (vmstat work, an in-kernel periodic; mechanism, observed), and an `/proc/interrupts` census on a 24-core 2.6.x HZ=100 machine (counts, window not stated). No user-space daemon rows.
- T2, T3: does not cover.
- T6: covers, as the HPC treatment of daemons: "system services, daemons" are the low-frequency long-duration noise class that can be moved to separate cores; clock ticks are the high-frequency short class; the remedy is pinning, isolcpus/cgroups and tickless cores. No CPU/run/wait figures for daemons.
- One observation? Partly: a 4-socket 6-core AMD machine with 16 MPI ranks, cores 3–6 per NUMA node, first two cores reserved for the OS; and a 24-core Linux 2.6.x machine (interrupt counts). Windows and distribution not named.

### S1-14 — Bristot de Oliveira, Casini, Cucinotta, "Operating System Noise in the Linux Kernel" (IEEE Trans. Computers, 2022)

Citation. Daniel Bristot de Oliveira, Daniel Casini, Tommaso Cucinotta, "Operating System Noise in the Linux Kernel", *IEEE Transactions on Computers*, 2022 (accepted-manuscript author copy from the Sant'Anna IRIS repository; no DOI is printed in the copy read). Peer-reviewed.

Copy read.
- `S1-14/IEEE-TC-2022.pdf` — URL https://www.iris.sssup.it/bitstream/11382/548111/1/IEEE-TC-2022.pdf, 12 pages (LaTeX manuscript), accessed 2026-09-20, SHA-256 `e084d6639ea8690a82c8f6f2380db0891a71e0a6081aeaf4ed526b881eae2917`

Passages.
> The housekeeping CPUs are those where the tasks necessary for the regular system usage will run. This includes kernel threads responsible for in-kernel mechanisms, such as RCU (read-copy-update) callback threads [11], kernel threads that perform deferred work such as kworkers and threads dispatched by daemons and users. General system's IRQs (Interrupt ReQuests) are also routed to housekeeping CPUs. [p. 1]

> These systems' setup involve selecting a small set of CPUs to be in charge of all tasks necessary for the system execution and operation, such as running system daemons, periodic maintenance tasks, managing user access to the system for monitoring activities, etc., leaving a large set of CPUs isolated from most of the operating noise that users or the OS could cause. [p. 3]

> The system is a Dell workstation with an AMD Ryzen 9 5900 processor, with 12 cores and 24 threads. The system is configured with Fedora Linux 35 server and runs the kernel 5.15 patched with the PREEMPT RT patchset. [p. 9]

> The osnoise workload detected 230 out-of-scale noise samples, with the maximum value as long as 13045 µs. [p. 9]

> The Tuned experiment includes the nohz_full option that reduces the occurrence of the scheduler tick, reducing the execution of the ksoftirqd kernel thread that checks for expired timers and activities that follow. [p. 9]

> That is because background OS activities that run as threads are deferred by the real-time scheduler, without creating a fault in the system. For example, jobs dispatched on all CPUs via kworkers threads that execute deferrable work [45]. [p. 9]

> It is important to highlight that the results presented in this section are only valid for this specific scenario. Different hardware, CPU count, auxiliary operating system services, and conditions will likely provide different results. [p. 9]

Coverage.
- T1: covers, weakly and for a server: the OS-noise view names which threads run on housekeeping CPUs (RCU callback threads, kworkers, daemon threads) and shows that on an untuned ("As-is") Fedora 35 server the noise seen by a busy thread over 6 h reaches 13045 µs in a single occurrence with 230 out-of-scale samples; the sources are traced to IRQs, softirqs and threads but no per-daemon table is printed in the text read (the figures are histograms).
- T2, T3: does not cover (server install, no session).
- T6: covers, as the treatment of daemons in low-latency evaluation: daemons and kernel threads are "OS noise" to be confined to housekeeping CPUs; a SCHED_FIFO workload defers "background OS activities that run as threads"; the paper's caveat that results depend on "auxiliary operating system services" is a stated limitation.
- One observation? Yes: Dell workstation, AMD Ryzen 9 5900 (12c/24t), Fedora Linux 35 server, kernel 5.15 PREEMPT_RT, states As-is/Tuned × SCHED_OTHER/FIFO:1, window 6 hours per histogram.

### S1-15 — Wang, Jia, Huang et al., "Mixture-of-Schedulers: An Adaptive Scheduling Agent as a Learned Router for Expert Policies" (arXiv 2025)

Citation. Xinbo Wang, Shian Jia, Ziyang Huang et al. (Zhejiang University), "Mixture-of-Schedulers: An Adaptive Scheduling Agent as a Learned Router for Expert Policies", arXiv:2511.11628v1 [cs.DC], 7 Nov 2025, 15 pp. Preprint.

Copy read.
- `S1-15/arxiv-2511.11628.pdf` — URL https://arxiv.org/pdf/2511.11628 (served v1), 15 pages, accessed 2026-09-20, SHA-256 `3a887853b4b21974373f912492963108f55f1526f1e951934a233c850fb07b8b`

Passages.
> Perception module collects data from multiple sources, including kernel-level eBPF programs, the procfs file system, and GNOME Shell for desktop environment information. [p. 4]

> To simulate realistic and challenging conditions, we constructed a benchmark suite of 28 scenarios. These are generated by pairing 4 interactive, latency-sensitive applications (Web Browsing, Audio Remix, Office File, Game Play) with 7 resource-intensive, background workloads (e.g., kernel compilation, blender render, LLM local generation). [p. 7]

> Our evaluation is conducted on a cluster of 10 distinct virtual machines (VMs) managed by Proxmox VE, which allows us to adjust parameters such as the number of CPU cores allocated to a VM on the base hardware, thereby creating a richer set of test hardware platforms. [p. 7]

> To quantify the performance in the Audio Remix scenario, this study used the PulseAudio suite [46] to perform multi-track audio mixing and effects application, and recorded data such as the number of buffer underruns and computation latency during the audio preview process to evaluate the scheduler's ability to meet strict audio timing requirements. [p. 14]

Coverage.
- T1, T2, T3: does not cover (no daemon, compositor or audio-server figures; GNOME Shell is a data source for the agent).
- T6: covers, as an example of how a 2025 sched_ext scheduler evaluation treats the rest of the system: the "background" is seven heavy batch workloads, not the always-on services; interactive scenarios run in a GNOME session inside Proxmox VMs with PulseAudio for the audio scenario; underruns and latency are the audio metric. No CPU/run/wait figures for services.
- One observation? Machines are VMs (Proxmox, 2–20 cores, 8–16 GB); games and apps named; windows not stated in the passages read; not a daemon observation.

## Context (not candidates)

Recorded because they were read; none is a Linux observation within the two-decade limit that a topic can cite, or none is Linux.

### ctx — Jones, "Why Userspace Sucks — Or 101 Really Dumb Things Your App Shouldn't Do" (OLS 2006)

Dave Jones (Red Hat), *Proceedings of the Linux Symposium 2006*, vol. 1, pp. 441–450. Exactly twenty years old (2006) and measured on Fedora Core 5: context. `ctx/ols2006-jones.pdf` — URL https://landley.net/kdocs/ols/2006/ols2006v1-pages-441-450.pdf, 12 pages, accessed 2026-09-20, SHA-256 `6f3f2cd7b7acba6e4b605f17ad6c6cee1dbbd1da7554999affaeacd902ac2e43`. It prints a `/proc/timertop` census of an idle FC5 desktop (Figure 3, p. 8) with timer-expiry counts per process (e.g. `crond 194`, `syslogd 251`, `hald 410`, `automount 437`, `kjournald 1260`, `init 1652`, `Xorg 13269`, `gdmgreeter 15607`, `cursor_timer_handler 34096`, `i8042_timer_func 35437`, `rh_timer_func 52912`, window not stated) and per-daemon notes:
> Wakes up every 10 seconds to re-balance interrupts in a round-robin manner. [p. 3]

> Cursor blinking. Hilariously, at HZ/5 we wake up to blink the cursor. (Even if we are running X, and not sat at a VT) [p. 8]

The intervals (irqbalance 10 s, USB timer 256 ms, i8042 poll HZ/20, cursor HZ/5, X SIGALRM smart scheduler) are 2006-era mechanisms, several since removed.

### ctx — Tsafrir, Etsion, Feitelson, Kirkpatrick, "System Noise, OS Clock Ticks, and Fine-Grained Parallel Applications" (ICS 2005)

`ctx/tsafrir-technion.pdf` — URL https://www.cs.technion.ac.il/~dan/papers/Noise05ICS.pdf, 10 pages, accessed 2026-09-20, SHA-256 `20992e90f61289d0c51624abb40405d2bfcd52e4c5a190f25650723ba2465043` (the huji.ac.il copy returned an error page). 21 years old: context. Linux 2.6.9, 1000 Hz, default-installation daemons.
> First, there are various system daemons that wake up once in a while. In Linux, these may include kswapd and bdflush (deal with swapping), ntpd (synchronizes clock), inetd (serves requests for rsh, telnet etc.), nfsd (file system) and so on. [p. 2]

> We can therefore conclude that noise generated by system daemons is only responsible for the difference in variability exhibited by the two policies, that is, the horizontal "right turn" taken by the OTHER curve at p = 10−5 [p. 5]

### ctx — other files read and set aside

- Schildermans, Aerts, Shan, Ding, "Paratick: Reducing Timer Overhead in Virtual Machines", ICPP 2021 — `ctx/paratick/paratick.pdf`, URL https://web.njit.edu/~dingxn/papers/paratick.pdf, 10 pages, SHA-256 `6f67efff9fca42fb2ca372785df5c5b87bd10b039eb6ffcbb919987fbd05dd11`. Its idle-VM figures (Table 1, p. 4: 40 000 VM exits per 10 s for an idle 16-vCPU VM at 250 Hz with periodic ticks, 0 tickless) are computed from formulas, not measured, so they are not an observation for T3's VM-versus-desktop contrast.
- Amirtharaj, Groot, Dezfouli, "Profiling and Improving the Duty-Cycling Performance of Linux-based IoT Devices", arXiv:1808.10097 — `ctx/iot-dutycycling/arxiv-1808.10097.pdf`, 23 pages, SHA-256 `dae3690f82563325415e5b7a3a71de726a2829445fa8691242839e3e22264b9f`. Boot/shutdown durations of systemd units on Raspberry Pi; nothing on idle behaviour.
- Becker, Chakraborty, "Measuring Software Performance on Linux", TUM technical report, arXiv:1811.01412 — `ctx/arxiv-1811.01412.pdf`, SHA-256 `27f6c68ec8f3c688d07ad5a31db7d018c64393d7e43bc07d46da346c1ac52c67`. Benchmark-stability advice; no idle-population figures.
- Reich, Goraczko, Kansal, Padhye, "Sleepless in Seattle No Longer", USENIX ATC 2010 — `ctx/Reich-atc10.pdf`, SHA-256 `d005fc4960d1e7ac4d6db4208a618a81f2c3b512ab6759565881b964a759a3f9`. Windows enterprise desktops, sleep proxying: not Linux, context only, not quoted.
- Pallipadi, Li, Belay, "cpuidle — Do nothing, efficiently…", OLS 2007 — `ctx/ols2007-cpuidle.pdf`, SHA-256 `9e1a963b378a47f6c8657eaee9a7aa81a3df7b4214ab6200b7ac5b47ec76e971`. C-state governor mechanism; no per-daemon figures.
- ICALEPCS 2017 TUPHA168, "Improving Throughput and Latency of D-Bus to Meet the Requirements of the FAIR Accelerator" — `ctx/icalepcs2017-tupha168.pdf`, SHA-256 `f95f5d85065b532f9e8d29a734c82d8b184d56980759b5d539eec29d104bfa4c`. D-Bus latency under a control-system load (an application's bus traffic), not an idle-bus observation.
- LWN, "OLS: Three talks on power management" (2007) — `ctx/lwn-240365.html`, SHA-256 `7b6f7bd4226bd3bb0430319461cef94e485c837be23745fbaa380555b6c07c77`. Report; the per-process wakeup claims on the page are in reader comments, not quoted.
- Intel, "PowerTOP Primer" (developer article) — `ctx/powertop-primer.html`, SHA-256 `dbdef3762050b493590e3fa59c4516b9c4f54ed285d839a2e751525eaa789167`. Vendor article; states target wakeup rates for a GNOME desktop without naming a machine; S2-class, not quoted.
- LPC 2011 session page "D-Bus Performance: Observations and Solutions" (Collabora) — `ctx/lpc2011-dbus.html`, SHA-256 `51d1bac2f2659c968ce3df6ae21fb47186c291543ca6c7e773c604b37f72a561`. Abstract only; no slides linked from the page.
- Dead-end pages kept for the record: `ctx/core-search.html` (403), `ctx/academia-wong.html` (403), `ctx/upcommons.html` (404), `ctx/s2-morari.html` (empty, 202), `ctx/morari-attempt/zenodo-3432539.html` (410), `ctx/retis-papers.html` (200, used for row 29), `ctx/tsafrir-ics05.pdf` (huji error page, SHA-256 `1562d8f1f97aa56f7cbfdb0a7d77523fb9065c1e12d1855ef761b10f388e4a64`), `ctx/lac2011-other/{24,26,32}.pdf` (other LAC 2011 papers fetched while locating paper 46).

Not fetched, noted from search results only: Flautner, Uhlig, Reinhardt, Mudge, ASPLOS 2000 (Linux desktop TLP, 26 years old; ACM blocks); Blake, Dreslinski, Mudge, Flautner, ISCA 2010 (Windows 7 and OS X per its abstract: not Linux); Morari et al., IPDPS 2011 (all copies blocked or removed: IEEE 202 challenge, researchgate 403, Zenodo 410); Akkan, Lang, Liebrock, IJHPCA 2013 (paywalled; the ROSS 2012 slides S1-13 stand in); Wong et al., ITSim 2008 (IEEE 418, academia.edu 403).

## 3. Not found

**T1 — per-service wake cadence, CPU per wake or CPU share of systemd-era services at idle, in literature.** No peer-reviewed or preprint paper was found that prints per-service rows (systemd, journald, udevd, logind, resolved, NetworkManager, timesyncd/chrony, dbus, cron, polkitd, udisksd, packagekitd, rsyslogd, multipathd) for an idle Linux system. What exists in class is aggregate: S1-02 (interrupts/s and timer events/s of an idle 2007 laptop), S1-03 (10.8 wakeups/s on an idle Fedora 9 server, top causes all kernel/device timers, daemons "typically less than 1%" CPU as a claim), S1-13/S1-14 (daemons as OS noise on servers). The only per-process idle table in a literature-class document is the Intel white paper S1-01 (pre-systemd Ubuntu with Unity; udisksd 0.1 wakeups/s is the one systemd-era service row). Searches establishing this: rows 1, 2, 16, 24, 26, 32, 35, 42, 44, 48, 52; plus the D-Bus searches 30 and 40 (bus performance under load only). The mechanism side (intervals stated by documentation) belongs to S2 and was not searched here.

**T2 — compositor per-frame CPU cost, compositor/audio-server wake cadence per state, on a Linux GPU desktop, in literature.** No paper or preprint measuring Mutter/GNOME Shell, KWin, Sway/wlroots, Weston, Xorg or Xwayland per frame (CPU per frame, wake cadence idle vs animating vs blanked) was found; the only compositor figures in class are 2013 Compiz/Xorg wakeups and context switches at idle (S1-01) and the 2008 Redline argument with reservation values (S1-04). For audio servers: JACK period timing under CFS/FIFO on a 2011 PC (S1-05), PipeWire/PulseAudio/JACK CPU load while playing on an ARM board (S1-08, grey), PipeWire's wake mechanism (S1-07). Nothing on PipeWire node suspension or rtkit policy in literature (S2 territory). Searches: rows 3, 4, 12, 14, 18, 19, 23, 33, 41, 45, 46, 49.

**T3 — an idle desktop session's process population (counts, aggregate wake rate, dominance, services-vs-session split) and its variation across GNOME-Wayland / GNOME-X11 / Plasma / lighter sessions, in literature.** Not found as a peer-reviewed or preprint study. The nearest are S1-01 (one Ubuntu/Unity/Compiz desktop: 107 → 30 wakeups/s with per-process rows) and, for the headless contrast, S1-03 (one Fedora 9 server: 10.8 wakeups/s); no source compares desktops or a VM with a session against one without. Blog and Phoronix comparisons exist but are out of class and phoronix.com was unreachable. Searches: rows 2, 9, 18, 21, 26, 33, 34, 47, 48, 50, 51, 52.

**T6 — reported CPU / run / wait / wake figures for system services beside interactive work in scheduler evaluations.** Partly found: the only figures are shares of scheduling events on a Steam Deck under a game (S1-09: system tasks incl. graphics and audio servers 30–40 % of schedules; per-task runtimes 100s of µs to a few ms) and JACK period statistics under CFS vs FIFO (S1-05). The treatment as such is found: daemons as latency-sensitive tasks needing reservations (S1-04), as OS noise to be confined (S1-13, S1-14), as absent from hackbench/schbench/rt-app (S1-12, S1-10), as heavy batch "background" rather than services (S1-15), and the latency-nice argument (S1-11). Not found: any evaluation that reports the always-on services' own CPU or wake figures next to an interactive metric on a desktop. Searches: rows 5, 15, 20, 27, 28, 36, 39, 53.

Unreachable or paywalled sources that might bear on these topics: Morari et al. IPDPS 2011 (T6 noise-source frequency/duration per OS event; IEEE/RG/Zenodo all closed); Akkan et al. IJHPCA 2013 (SAGE/ACM); Wong et al. 2008 (IEEE 418, academia 403); ACM DL generally (Flautner 2000, Blake 2010 — both out of scope anyway); phoronix.com and openbenchmarking.org (desktop-environment power comparisons, out of class).
