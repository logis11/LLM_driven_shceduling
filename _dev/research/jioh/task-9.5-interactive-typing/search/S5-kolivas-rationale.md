# S5 — Kolivas / interbench: primary text behind the Audio, Video and X emulation constants

Reader: S5. Date of all searches, fetches and reads: 2026-09-14. Input read: `search/input.md`; layout matched to `search/S1-literature.md`.

Questions this record answers (from the task brief):

- **Q1** Which "popular linux audio player" was seen writing to the audio card at 50 ms; on what machine; how it was seen; when.
- **Q2** Any observation, benchmark or measurement behind the video thread's 60 Hz and 40 % CPU.
- **Q3** Any observation, benchmark or measurement behind the X thread's 0–100 % variable CPU.
- **Q4** Any later revision of these constants and its reason.
- **Q5** Whether interbench was used or cited in a peer-reviewed paper with those constants explained.

Method notes. Every web copy was fetched with `curl` (a browser-like `User-Agent` where a host required it) and read from the fetched file. HTML was reduced to text with a small Python `re`-based stripper; mailing-list text archives were read as-is; PDFs were extracted with `pypdf` 6.18.0 (page markers inserted per PDF page; page locators are PDF page numbers of the copy read). lore.kernel.org could not be read at all (see §1a), so LKML was read from the Indiana University hypermail mirror (`lkml.iu.edu`), `marc.info`, `narkive.com` and LWN copies; Message-IDs come from the ck-list pipermail copies of the same messages (the hypermail mirror does not expose them). All copies are under `sources/S5-*/` (gitignored); SHA-256 values are of the file named in each entry. The interbench git clone is `sources/S5-01-interbench-git/repo/` at HEAD `e612a65ce941028ddea804e6b45ccde2750720d2`. Nothing below is quoted from a search-engine snippet or a fetch-tool summary; where a tool returned only a summary it is marked "not citable".

## 1. Search log

### 1a. lore.kernel.org (LKML public-inbox) — all 2026-09-14

| # | Query / URL | Result |
|---|---|---|
| 1 | `https://lore.kernel.org/lkml/?q=interbench` (curl, default UA) | 403 (nginx "403 Forbidden", 146 B) |
| 2 | `…/?q=interbench+audio` | 403 |
| 3 | `…/?q=interbench+video` | 403 |
| 4 | `…/?q=interbench+xmms` | 403 |
| 5 | `…/?q=interbench` with a browser `User-Agent` | 200 but body is an Anubis proof-of-work page ("Making sure you're not a bot!"), 7 462 B; no search results |
| 6 | same URL via WebFetch | "Access Denied: error code 9e4edb5b6b850c41" (Anubis); no results — not citable |

Date-bounded lore queries (2005–2008) were therefore not possible; LKML was covered through the mirrors in §1b instead.

### 1b. LKML mirrors — lkml.iu.edu hypermail, marc.info, narkive, LWN (all 2026-09-14)

| # | Venue / query | Hits followed | Dead ends (status) |
|---|---|---|---|
| 7 | WebSearch `"interbench" Kolivas "[ANNOUNCE]" lkml 2005 audio 50ms xmms` | lkml.iu.edu/hypermail/linux/kernel/0507.1/1210.html (v0.20 announcement, 200); ck.vds.kolivas.narkive.com/DwLthTog (v0.21 ck-list thread, 200); linux.kernel.narkive.com/7XeJMS2n (v0.21 LKML thread, 200) | — |
| 8 | lkml.iu.edu 0507.1 thread walk from 1210 following every "Next in thread"/"Reply" link | 20 messages fetched (1210, 1230, 1232, 1237, 1240, 1306, 1359, 1372, 1439, 1449, 1604, 1687, 1817, 1847, 1855, 1859, 1862, 1868, 2301, 2302), all 200; every message converted to text and searched for `audio|xmms|50 ?ms|60 ?fps|40 ?%|5 ?%|window|drag`; the messages with hits (1210, 1230, 1232, 1237, 1604, 1687, 1817, 1847, 1855, 1859, 1862, 1868, 2301, 2302) were read in full | — |
| 9 | lkml.iu.edu 0507.2 thread walk from 0020 ("Re: [ANNOUNCE] Interbench v0.21", Lee Revell) | 0020, 0181 (200) | — |
| 10 | lkml.iu.edu/hypermail/linux/kernel/0603.3/0374.html "[benchmark] Interbench 2.6.16-ck/mm" (from WebSearch #23) | 200; result tables only, no constants discussion | — |
| 11 | marc.info `?l=linux-kernel&w=2&r=1&s=interbench&q=b` | 200; 30 hits listed (2007-04-08 … 2026-05-26). Raw copies fetched (`&q=raw`, all 200) for m=118647160513548 (2007-08-07 Michal Piotrowski "O(1) vs. CFS interbench comparison"), 117679543417180, 117679501023393, 117679498805547, 117679463026751, 117679388606632 (2007-04-17 "Modular Scheduler Core" replies), 117614421726766, 117614163823533, 117603183711614 (2007-04-08/09 "Ten percent test"), 118106977518946 (2007-06-05), 117862237205591 (2007-05-08). Each grepped for interbench context: only pointers to result files, autotest logs, or "Just reuse SDET, AIM7/AIM9, OAST, contest, interbench, et al."; none discusses the constants | — |
| 12 | LWN copies: lwn.net/Articles/144328 (v0.22 announcement), /174369 (v0.30 announcement), /144327 ("Interbench real time benchmark results", 2005-07-20) | all 200 | — |

### 1c. ck mailing list archive (bhhdoa.org.au pipermail) — all 2026-09-14

| # | Query / URL | Result |
|---|---|---|
| 13 | `http://bhhdoa.org.au/pipermail/ck/` and `https://…` (live) | connection failed (curl status 000) |
| 14 | `web.archive.org/web/2008id_/http://bhhdoa.org.au/pipermail/ck/` | 200 from Wayback but the archived body is the origin's "403 Forbidden … Apache/2.2.3 (Debian) Server at bhhdoa.org.au" page (293 B) |
| 15 | Wayback CDX `url=bhhdoa.org.au/pipermail/ck/*&filter=statuscode:200&from=2005&to=2009` | 200; 3 000 rows (cap hit) |
| 16 | CDX per month: `pipermail/ck/2005-July*`, `2005-August*`, `2005-September*`, `2005-October*`, `2006-March*`, `2005-June*` | 143 / (in #15) / 369 / 112 / 333 / 14 rows; monthly `.txt.gz` captures exist for 2005-July (ts 20060129195948), 2005-August (20060129200256), 2005-September, 2005-October; none for 2006-March |
| 17 | CDX `pipermail/ck.mbox/ck.mbox` | 7 captures; latest 20070806053117 (10 110 835 B compressed listing; 41 836 723 B fetched) |
| 18 | Fetched: `2005-July.txt.gz` (200, 76 236 B), `2005-August.txt.gz` (200, 137 993 B), `ck.mbox` @20070806053117 (200, 41 836 723 B, 8 420 messages, 2004-06-30 → 2007-08) | read as described in S5-04 / S5-06 |
| 19 | Full-mbox grep for `audio player|write to (the )?(audio|sound) card|50 ?ms interval|xmms.*(50|interval|period)|(50|interval|period).*xmms` | hits are only the readme text itself (lines 465204–466474), Lee Revell's XMMS patch (468633), and unrelated threads (2004 "xmms alsa uses ~50% cpu"; 2007 swap-prefetch and wine/directsound threads). No message from Kolivas names the player behind the 50 ms figure |
| 20 | Full-mbox subject survey for `interbench` | 46 distinct subjects; the only thread asking what the workloads represent is "[ck] interbench: workload characterization." (2007-03-11, hugo vanwoerkom; one reply pointing to the homepage) — read, no rationale |

### 1d. Kolivas's own pages — all 2026-09-14

| # | URL | Result |
|---|---|---|
| 21 | `http://ck.kolivas.org/apps/interbench/` (live) | 200; directory lists `interbench-0.31.tar.bz2`, `.lrz`, `readme` (18-Aug-2012). `https://` variant: connection failed |
| 22 | `web.archive.org/web/2006id_/http://ck.kolivas.org/apps/interbench/` | 200; directory lists 0.20 (12-Jul-2005) … 0.29 (10-Aug-2005), 0.30 (04-Mar-2006), `debian_readme.txt`, `pending/` (empty), `readme`, two `.log` files |
| 23 | CDX `interbench.kolivas.org*` | 22 captures, all 301 → `members.optusnet.com.au/ckolivas/interbench/` |
| 24 | CDX `members.optusnet.com.au/ckolivas/interbench/*` | 1 capture, 20051119115545, fetched (200) |
| 25 | CDX `users.on.net/~ckolivas/interbench/*` | 1 capture, 20090802111522, fetched (200) |
| 26 | WebSearch `ck-hack.blogspot.com interbench`; then fetched `ck-hack.blogspot.com/2016/10/interbench-benchmarks-for-muqss-116.html`, `/2016/10/linux-48-ck4-muqss-cpu-scheduler-v0116.html`, `/search?q=interbench` | all 200; the search page lists three posts (the two above and 2011-03 "2.6.38-ck2, BFS 0.370"); none discusses the constants |

### 1e. Source history — all 2026-09-14

| # | Action | Result |
|---|---|---|
| 27 | `git clone https://github.com/ckolivas/interbench.git` | 11 commits, 2016-10-21 → 2016-10-24; first commit "Initial commit of version 0.31" |
| 28 | `git log -L 490,512:interbench.c`, `git log -S AUDIO_INTERVAL` | only commit 2b42050 touches the constant lines |
| 29 | Wayback `…/2006id_/http://ck.kolivas.org/apps/interbench/interbench-<v>.tar.bz2` for v = 0.20 … 0.30; live `interbench-0.31.tar.bz2` | all 200; all valid bzip2; extracted and diffed pairwise (S5-02) |

### 1f. Scholarly indexes — all 2026-09-14

| # | Query | Hits followed | Dead ends (status) |
|---|---|---|---|
| 30 | Semantic Scholar `paper/search?query=interbench` | first call 429; retry 200, 7 records: only "Comparison of Interactivity Performance of Linux CFS and Windows 10 CPU Schedulers" (ICGHIT 2020, DOI 10.1109/ICGHIT49656.2020.00014) and "Interactivity performance benchmark for Windows and Mac OS" (2020) concern interbench | — |
| 31 | OpenAlex `works?search=interbench` | 200, 27 records; relevant: ICGHIT 2020 (above); "Interactivity performance benchmark for Windows and Mac OS" (2020); "LOTTERY SCHEDULING IN THE LINUX KERNEL: A CLOSER LOOK" (Cal Poly 2012); "Multidimensional Load Balancing and Finer Grained Resource Allocation Employing Online Performance Monitoring Capabilities" (Ohio 2015); "Addressing Hybrid OS Environment Issues in the Embedded Virtualization Multicore Platform" (Waseda doctoral thesis, year not given); "Collaborative Scheduling and Synchronization of Distributable Real-Time Threads" (VT 2010); "Agile Development of Linux Schedulers with Ekiben" (arXiv 2306.15076) | — |
| 32 | Fetch of the open copies above | ohiolink (200, PDF); waseda.repo.nii.ac.jp Honbun-6572.pdf (200, PDF); arxiv 2306.15076 (200, PDF — zero occurrences of "interbench" in its text; OpenAlex false positive) | digitalcommons.calpoly.edu viewcontent.cgi?article=1816 (403, HTML challenge page); vtechworks.lib.vt.edu/bitstreams/handle/10919/27578 (404) |
| 33 | WebSearch `"Comparison of Interactivity Performance of Linux CFS and Windows 10 CPU Schedulers" ICGHIT 2020 interbench pdf` | eprints.utar.edu.my/3865/1/16ACB02681_FYP.pdf (200, PDF; the first author's bachelor report on the same work) | ieeexplore.ieee.org/document/9058348 (paywalled venue, not fetched); researchgate/typeset copies (not fetched) |
| 34 | WebSearch `Wong Tan Kumari Wey "Fairness and interactive performance of O(1) and CFS Linux kernel schedulers" pdf interbench audio 50ms` | none open | researchportal.hw.ac.uk (metadata only); academia.edu and researchgate (login-walled, not fetched); S1 reader already recorded the IEEE copy as paywalled |
| 35 | WebSearch `"interbench" scheduler paper pdf "50ms" audio "5%" cpu Kolivas benchmark evaluation` | only man-page mirrors, GitHub, OpenBenchmarking, LWN 144328, the 2016 blog post, and the ResearchGate page of Wong 2008 | — |

### 1g. Other web searches — all 2026-09-14

| # | Query | Hits followed | Dead ends |
|---|---|---|---|
| 36 | WebSearch `"interbench" "xmms" Kolivas audio "50ms" OR "50 ms" interval write audio card` | linux.die.net man page (same text as S5-09); lwn 144327; narkive v0.21 thread; lkml.iu.edu 0603.3/0374 — no new primary text | — |
| 37 | WebSearch `Debian ITP interbench bug Julien Valroff 2005` | nothing on an ITP; linux.die.net man page notes it was "written for the Debian system by Julien Valroff" (search-result summary only — not citable) | — |

### 1h. Packaging — all 2026-09-14

| # | URL | Result |
|---|---|---|
| 38 | `bugs.debian.org/cgi-bin/pkgreport.cgi?src=interbench;archive=both` | 200 but body is a JavaScript proof-of-work challenge page ("I Challenge Thee"); no bug list readable |
| 39 | `tracker.debian.org/pkg/interbench` | 404 |
| 40 | `debian_readme.txt` from the 2006 ck.kolivas.org listing (Wayback, 200, 192 B) | only two `deb`/`deb-src` lines for `julien.valroff.free.fr`; no rationale |

Gentoo/Arch packaging pages were not queried (time-box reached; the brief limits packaging to pages quoting a rationale, and none was indicated by any hit above).

## 2. Candidates

### S5-01 — interbench git repository (GitHub, 2016)

**Citation.** Con Kolivas, *interbench — Interactivity benchmark*, git repository `https://github.com/ckolivas/interbench.git`, 11 commits 2016-10-21 → 2016-10-24, HEAD `e612a65ce941028ddea804e6b45ccde2750720d2`.

**Copy read.** Clone at `sources/S5-01-interbench-git/repo/` (cloned 2026-09-14). SHA-256 at HEAD: `interbench.c` `a381b94085427cda4169466d3833c272fe4e9672cfbad74a64897621db7f2191`; `readme` `a67f2b8b3d92896e63f2f03e25dc3f59077eb49192fa353d56cbe0da1f7c0b29`; `interbench.8` `31bc88e508bb7f81cc01a4ef632fbee4f4acb908082140427acba11ca2ee92ee`.

**Commit list (all by Con Kolivas / ckolivas).**

```
e612a65 2016-10-24 Hackbench still frequently fails to return so disable it for the time being.
f23ee1b 2016-10-22 Get more accurate CPU calibration by running for at least one second to guarantee CPU gets to max frequency with frequency scaling.
de958be 2016-10-22 Use monotonic_raw clock where possible to not worry about time changes.
70d2068 2016-10-21 Fix uninitialised affinity variable.
f96e2ef 2016-10-21 Reinstate ring load, setting number of rings to CPUs
6adccf8 2016-10-21 Add back in hackbench as a load, setting groups and receivers in hackbench to cpu load.
86e4624 2016-10-21 Set affinity of timekeeping thread back to normal in case it has been set on the parent process.
718667c 2016-10-21 Fix numerous compile issues. Fix cpu calibration being unstable without affinity. Fix affinity. Determine processors automatically.
58ea031 2016-10-21 Merge branch 'master' of github.com:ckolivas/interbench
2b42050 2016-10-21 Initial commit of version 0.31
28b6640 2016-10-21 Initial commit
```

`git log -L 490,512:interbench.c` and `git log -S AUDIO_INTERVAL -- interbench.c` both return only `2b42050` ("Initial commit of version 0.31"): no commit in the repository changes the constants.

**Verbatim, `interbench.c` at `e612a65`.**

Lines 490–493:
```
#define AUDIO_INTERVAL	(50000)
#define AUDIO_RUN	(AUDIO_INTERVAL / 20)
/* We emulate audio by using 5% cpu and waking every 50ms */
void emulate_audio(struct thread *th)
```
Lines 510–513:
```
/* We emulate video by using 40% cpu and waking for 60fps */
#define VIDEO_INTERVAL	(1000000 / 60)
#define VIDEO_RUN	(VIDEO_INTERVAL * 40 / 100)
void emulate_video(struct thread *th)
```
Lines 530–556:
```
/*
 * We emulate X by running for a variable percentage of cpu from 0-100% 
 * in 1ms chunks.
 */
void emulate_x(struct thread *th)
{
	unsigned long long deadline;
	sem_t *s = &th->sem.stop;
	struct timespec myts;

	th->decasecond_deadlines = 100;
	deadline = get_usecs(&myts);

	while (1) {
		int i, j;
		for (i = 0 ; i <= 100 ; i++) {
			j = 100 - i;
			deadline = periodic_schedule(th, i * 1000, j * 1000,
				deadline);
			deadline += i * 1000;
			if (!trywait_sem(s))
				return;
		}
	}
}
```

`readme` at `e612a65` (dated at its foot "Sat Oct 31 15:17:12 2009"), section "What interactive tasks are simulated and how?":
```
X:
X is simulated as a thread that uses a variable amount of cpu ranging from 0 to
100%. This simulates an idle gui where a window is grabbed and then dragged
across the screen.

Audio:
Audio is simulated as a thread that tries to run at 50ms intervals that then
requires 5% cpu. This behaviour ignores any caching that would normally be done
by well designed audio applications, but has been seen as the interval used to
write to audio cards by a popular linux audio player. It also ignores any of the
effects of different audio drivers and audio cards. Audio is also benchmarked
running SCHED_FIFO if the real time benchmarking option is used.

Video:
Video is simulated as a thread that tries to receive cpu 60 times per second
and uses 40% cpu. This would be quite a demanding video playback at 60fps. Like
the audio simulator it ignores caching, drivers and video cards. As per audio,
video is benchmarked with the real time option.
```
`readme`, section "What is relevant in the data?":
```
The results pessimise quite a lot what happens in real world terms because they
ignore the reality of buffering, but this allows us to pick up subtle 
differences more readily. In terms of what would be noticed by the end user,
dropping deadlines would make noticable clicks in audio, subtle visible frame
time delays in video, and loss of "smooth" movement in X. Dropping desired cpu
would be much more noticeable with audio skips, missed video frames or jerks
in window movement under X. The magnitude of these would be best represented by
the maximum latency. When the deadlines are actually met, the average latency
represents how "smooth" it would look. Average humans' limit of perception for
jitter is in the order of 7ms. Trained audio observers might notice much less.
```

**Coverage.** Q1: states only "a popular linux audio player"; no player, machine, method or date. Q2: only "This would be quite a demanding video playback at 60fps" — a characterisation, not a measurement. Q3: only "simulates an idle gui where a window is grabbed and then dragged across the screen"; no measurement. Q4: no revision in the git history. Q5: not applicable. **One observation?** No observation is reported; nothing is named.

### S5-02 — interbench release tarballs 0.20 … 0.31 (2005-07-12 … 2012)

**Citation.** Con Kolivas, `interbench-<v>.tar.bz2`, v = 0.20, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.30 from `http://ck.kolivas.org/apps/interbench/` as archived by the Wayback Machine (`web.archive.org/web/2006id_/…`); v0.31 from the live host. Directory listing dates (Wayback 2006 capture, `sources/S5-ck-list/656049608d0c82ebfe992991464b147a.html`): 0.20 12-Jul-2005, 0.21 15-Jul-2005, 0.22 20-Jul-2005, 0.23 27-Jul-2005, 0.24 29-Jul-2005, 0.25 30-Jul-2005, 0.26 03-Aug-2005, 0.27 04-Aug-2005, 0.28 06-Aug-2005, 0.29 10-Aug-2005, 0.30 04-Mar-2006; live listing (`…/7e032220724baea5779465a2e119252d.html`): 0.31 18-Aug-2012.

**Copies read.** `sources/S5-02-tarballs/interbench-<v>.tar.bz2`, extracted under `sources/S5-02-tarballs/x/<v>/`. SHA-256: 0.20 `0f66024c63ef481957175a3f21bd2199c8623abe0db492b0d9bf24ee78aab6ef`; 0.24 `a92428d49afe7557131dd52d91f8afe8b51fe24f293fbf716642b1d7360990da`; 0.30 `a77d4a82573b07a9f6c6d256b399accea1f6cd433f3f1e6d038272cf0d320365`; 0.31 `89d438b28aef22d26e79812762a57a9f9344a8dd8826edebfe60dad48ee1c784` (the remaining eight are in the same folder; their content differences are fully described below).

**Verbatim, `interbench-0.20/interbench.c` (readme foot date "Mon Jul 11 23:50:39 2005").** Lines 369–371:
```
#define audio_interval	(50000)
#define audio_run	(audio_interval / 20)
/* We emulate audio by using 5% cpu and waking every 50ms */
```
Lines 390–392:
```
/* We emulate video by using 40% cpu and waking for 60fps */
#define video_interval	(1000000 / 60)
#define video_run	(video_interval * 40 / 100)
```
Lines 411–414:
```
/*
 * We emulate X by running for a variable percentage of cpu from 0-100% 
 * in 1ms chunks.
 */
```

**Pairwise diff of the three emulation functions (`emulate_audio`, `emulate_video`, `emulate_x` with their `#define`s) across all twelve versions.** Identical for 0.20→0.21→0.22→0.23. 0.23→0.24: identifiers renamed `audio_interval`→`AUDIO_INTERVAL`, `audio_run`→`AUDIO_RUN`, `video_interval`→`VIDEO_INTERVAL`, `video_run`→`VIDEO_RUN`; `sem_trywait(s)`→`trywait_sem(s)`; values unchanged. Identical 0.24→0.25→0.26→0.27. 0.27→0.28: `unsigned long deadline`→`unsigned long long deadline` in all three functions and removal of `th->dt->nr_samples++`; values unchanged. Identical 0.28→0.29→0.30→0.31, and 0.31 equals the git HEAD text quoted in S5-01. **No version changes 50 ms, 5 %, 60 Hz, 40 % or the 0–100 % X sweep.**

**Pairwise diff of the readme "X:/Audio:/Video:" paragraphs.** 0.20→0.21 changes only the real-time sentences: 0.20 reads "Audio is run twice, the / second / time it is run as a real time SCHED_FIFO task." and "video is run SCHED_FIFO on a repeat run."; 0.21 reads "Audio is also benchmarked / running SCHED_FIFO if the real time benchmarking option is used." and "video is benchmarked with the real time option." The sentence "has been seen as the interval used to / write to audio cards by a popular linux audio player" is present, unchanged, in every version 0.20 … 0.31. No version names the player.

**Changelogs carried by the tarballs.** None: no `ChangeLog` file exists in any version (0.20 ships `COPYING interbench.c Makefile readme readme.interactivity sample.log`; 0.24 adds `hackbench.c interbench.h`; 0.30 adds `interbench.8`). Release notes exist only in the mailing-list announcements (S5-06).

**Coverage.** Q4: establishes there was no later revision of the constants (values identical across 0.20 … 0.31 and git HEAD; only identifier and integer-type changes). Q1–Q3: no rationale beyond the readme text quoted in S5-01. **One observation?** None reported.

### S5-03 — LKML thread "[ANNOUNCE] Interbench v0.20 - Interactivity benchmark" (July 2005)

**Citation.** Con Kolivas, "[ANNOUNCE] Interbench v0.20 - Interactivity benchmark", linux-kernel, Message-ID `<200507122110.43967.kernel@kolivas.org>` (hypermail date "Tue Jul 12 2005 - 06:15:59 EST"), and replies.

**Copies read.** `sources/S5-03-lkml-announce/0507.1-<n>.html` (lkml.iu.edu hypermail, fetched 2026-09-14) with `.txt` conversions alongside; Message-IDs and In-Reply-To from the ck-list pipermail copies in `sources/S5-ck-list/ck-2005-July.txt` (S5-04). SHA-256: 1210 `10000dde50d2a16b8dc2bf4ea3ee8ba00d1874cb5307654b2505616b29d79df9`; 1230 `d166e3e9647b9fc9316c48a0e2ed56353e7699b3b228a5e8d02450f35f381e4e`; 1237 `732d6cc97a30147f7ca48f4e517615d922269461810f4c386862ce0fc1dc1f0a`; 1604 `d28390c552e2a01760819c5a0ed775d3fa284df67ea465a371319b4aceab5b47`; 1687 `ef1892ee53d06e60e58a3e280765c049960808212593b145591c138241e8ade6`; 1862 `129310c71ed0bcdd9040356246a4f95ec74efa59557cd3bcb0741bfd60873c6f`; 1868 `a681c8c462d275f0fcf2e0fda74a1fd50688900adb8c87611879e068f9910b27`.

**Verbatim.**

(a) Announcement, Con Kolivas, `<200507122110.43967.kernel@kolivas.org>`, hypermail 0507.1/1210 — the "What interactive tasks are simulated and how?" section reads exactly as the 0.20 readme:
```
X:
X is simulated as a thread that uses a variable amount of cpu ranging from 0 
to 100%. This simulates an idle gui where a window is grabbed and then 
dragged across the screen.

Audio:
Audio is simulated as a thread that tries to run at 50ms intervals that then
requires 5% cpu. This behaviour ignores any caching that would normally be 
done by well designed audio applications, but has been seen as the interval 
used to write to audio cards by a popular linux audio player. It also ignores 
any of the effects of different audio drivers and audio cards. Audio can also 
be run as a real time SCHED_FIFO task.

Video:
Video is simulated as a thread that tries to receive cpu 60 times per second
and uses 40% cpu. This would be quite a demanding video playback at 60fps. 
Like the audio simulator it ignores caching, drivers and video cards. As per 
audio, video can be run SCHED_FIFO.
```

(b) David Lang, hypermail 0507.1/1230 ("Tue Jul 12 2005 - 07:06:21 EST"), `<Pine.LNX.4.62.0507120446450.9200@qynat.qvtvafvgr.pbz>`:
```
for some of the loads you really are going to be independant of the speed 
of the hardware (burn, compile, etc will use whatever you have) however 
for others (X, audio, video) saying that they take a specific percentage 
of the cpu doesn't seem right.

if I have a 400MHz cpu each of these will take a much larger percentage of 
the cpu to get the job done then if I have a 4GHz cpu for example.

for audio and video this would seem to be a fairly simple scaleing factor 
(or just doing a fixed amount of work rather then a fixed percentage of 
the CPU worth of work), however for X it is probably much more complicated 
(is the X load really linearly random in how much work it does, or is it 
weighted towards small amounts with occasional large amounts hitting? I 
would guess that at least beyond a certin point the liklyhood of that much 
work being needed would be lower)
```

(c) Con Kolivas, reply, `<200507122202.39988.kernel@kolivas.org>` (quoted inside 0507.1/1237 and in the ck copy):
```
Actually I don't disagree. What I mean by hardware changes is more along the 
lines of changing the hard disk type in the same setup. That's what I mean by 
careful with the benchmarking. Taking the results from an athlon XP and 
comparing it to an altix is silly for example.
```

(d) Con Kolivas, `<200507141021.55020.kernel@kolivas.org>` (reply to Bill Davidsen `<42D55562.3060908@tmr.com>`), quoted inside 0507.1/1859–1868:
```
That is rather hard to do because each architecture's interpretation of fixed 
number of cycles is different and this doesn't represent their speed in the 
real world. The calculation when interbench is first run to see how many 
"loops per ms" took quite a bit of effort to find just how many loops each 
different cpu would do per ms and then find a way to make that not change 
through compiler optimised code. The "loops per ms" parameter did not end up 
being proportional to cpu Mhz except on the same cpu type.
```

(e) Con Kolivas, hypermail 0507.1/1862 ("Wed Jul 13 2005 - 19:51:28 EST"), `<200507141046.27788.kernel@kolivas.org>`:
```
Once again I don't disagree, and the current system of loops_per_ms does 
exactly that and can be simply used as a fixed number of loops already. My 
point was there'd be argument about what sort of "loop" or load should be 
used as each cpu type would do different "loops" faster and they won't 
necessarily represent video, audio or X in the real world. Currently the loop 
in interbench is simply:
	for (i = 0 ; i < loops ; i++)
	     asm volatile("" : : : "memory");

and if noone argues i can use that for fixed workload.
```

(f) szonyi calin, hypermail 0507.1/1604 ("Wed Jul 13 2005 - 06:28:53 EST"), `<20050713112710.60204.qmail@web52902.mail.yahoo.com>`, after quoting the Audio paragraph:
```
I have the following problem with audio:
Xmms is running with threads for audio and spectrum
analyzer(OpenGL).
The audio eats 5% cpu, the spectrum analyzer about 80 %. The
problem is that sometimes the spectrum analyzer is eating all of
the cpu while the audio is skipping. Xmms is version 1.2.10
kernel is vanilla, latest "stable" version 2.6.12, suid root.

Does your benchmark simultes this kind of behaviour ? 
```

(g) Lee Revell, hypermail 0507.1/1687 ("Wed Jul 13 2005 - 12:41:50 EST"), `<1121276077.4435.50.camel@mindpipe>`:
```
That's just a broken app, the kernel can't do anything about it.  XMMS
should not be running the spectrum analyzer thread at such a high
priority as to interfere with the audio thread.
```

(h) Con Kolivas, `<200507140958.00510.kernel@kolivas.org>` (reply to (g); ck copy, S5-04), entire own text:
```
I agree; optimising for this is just silly.
```

**Coverage.** Q1: the only player named anywhere in the thread is XMMS, and it is named by a *user* (szonyi calin) reporting a skipping problem — not by Kolivas, and not as the source of the 50 ms figure; Kolivas's replies never identify the player. Q2/Q3: the thread debates fixed-work vs fixed-percentage emulation (b–e); no measurement behind 60 Hz/40 % or the X sweep is offered. Q4: no. **One observation?** (f) is one user's observation (XMMS 1.2.10 audio thread "eats 5% cpu", kernel 2.6.12, machine not named), but it concerns CPU share under a spectrum analyser, not the 50 ms interval, and post-dates the constant.

### S5-04 — ck mailing list, July 2005 monthly archive (pipermail text)

**Citation.** ck mailing list (`ck@vds.kolivas.org`, archive `bhhdoa.org.au/pipermail/ck/2005-July.txt.gz`), Wayback capture 20060129195948.

**Copy read.** `sources/S5-ck-list/ck-2005-July.txt.gz` (SHA-256 `3b8bce0d271962182e328d6dd982f10e850a521121b594ff333369ce00a0d2e3`), decompressed to `ck-2005-July.txt` (9 314 lines). Interbench subjects in the month: "[ANNOUNCE] Interbench v0.20" (+21 "Re:" / 3 "RE:"), "v0.21" (+3/+4), "v0.22", "v0.24" (+5), "[Interbench Patch] Calculating the value where n% of the", "amd64 Interbench Results" (+5), "Interbench real time benchmark results" (+8), "Interbench: does it measure disk stuff?" (+2). Grep for `xmms|audio player|amarok|mplayer|xine|50 ?ms|60 ?fps|40 ?%` hits only the readme text, the szonyi calin / Lee Revell exchange (S5-03 f–h), and the two Lee Revell messages below.

**Verbatim.**

(a) Lee Revell, "[ck] Re: [ANNOUNCE] Interbench v0.20 - Interactivity benchmark", `<1121545716.10774.16.camel@mindpipe>`, In-Reply-To `<200507140958.00510.kernel@kolivas.org>`, list date "Sun Jul 17 04:16:24 2005":
```
I took a closer look and it's indeed quite broken.  If XMMS is run in
realtime mode, and multithreading is enabled, it runs everything
SCHED_RR - GUI, audio, spectrum analyzer.  (And since it relies on new
threads inheriting RT scheduling when pthread_create()'d, the threads
will fail to get SCHED_RR on buggy NPTL versions like the one in Debian
Sarge).

This untested patch should enable RT scheduling for only the (ALSA)
audio thread.  Make sure NOT to run in realtime mode.

Lee

--- ../xmms-1.2.10+cvs20050209.orig/Output/alsa/audio.c	2005-01-31 17:45:08.000000000 -0500
+++ Output/alsa/audio.c	2005-07-16 16:06:06.000000000 -0400
```
(the patch adds `pthread_setschedparam(audio_thread, SCHED_FIFO, …)` after `pthread_create(&audio_thread, NULL, alsa_loop, NULL);` in `alsa_open()`; no timing or interval figure appears in it).

(b) Con Kolivas, "[ck] Re: [ANNOUNCE] Interbench v0.21", `<200507180618.27121.kernel@kolivas.org>`, In-Reply-To `<1121503267.5070.21.camel@mindpipe>`, replying to Lee Revell's suggestion (S5-05):
```
While I agree with you in principal on getting the rlimit feature working and 
supported, this benchmark is meant to be run in single user mode for most 
reproducible and valid results. However, clearly there will be people using 
it cautiously as a normal user first. I originally did not include the 
information that you need to be root in v.20 and said in the documentation 
"need rt privileges" but within about 5 minutes of posting it I had someone 
not understanding what "unable to get SCHED_FIFO" meant. I guess a more 
verbose message will be required explaining non-root RT as well.
```

**Coverage.** Q1: XMMS is discussed (its thread scheduling), never as the source of the 50 ms figure; Kolivas does not name the player. Q2–Q4: nothing. **One observation?** (a) is a code reading of `xmms-1.2.10+cvs20050209` by Lee Revell, not a timing measurement.

### S5-05 — "[ANNOUNCE] Interbench v0.21" thread (15–18 July 2005)

**Citation.** Con Kolivas, "[ANNOUNCE] Interbench v0.21", `<200507151401.49854.kernel@kolivas.org>` (LKML copy 2005-07-15 04:10:06 UTC per narkive; ck copy 04:01:47 UTC), and Lee Revell's reply `<1121503267.5070.21.camel@mindpipe>` (LKML hypermail 0507.2/0020, "Sat Jul 16 2005 - 05:10:28 EST").

**Copies read.** `sources/S5-05-narkive/linux.kernel.narkive.com_7XeJMS2n_announce-interbench-v0-21.html` (SHA-256 `4734d1eef109b264f3f8898b4d5c8956fe099bb212731ef46357ca93b53d047c`); `sources/S5-05-narkive/ck.vds.kolivas.narkive.com_DwLthTog_announce-interbench-v0-21.html` (`c1b667ab4cd0bc0f7fd4911f2ec421289f8d87c8c22b9766a954fea338f1c5ea`); `sources/S5-03-lkml-announce/0507.2-0020.html` (`6c70c9d316477055f90b9c6ea3bb0065dc27c39c643c60eb2cf8005ef2d77b85`).

**Verbatim.** Announcement changelog:
```
Changes:
Changed the design to run the benchmarked and background loads as separate
processes that spawn their own threads instead of everything running as a
thread of the same process. This was suggested to me originally by Ingo
Molnar who noticed significant slowdown due to conflict over ->mm->mmap_sem,
invalidating the benchmark results when run in real time mode. This makes a
large difference to the latencies measured under mem_load particularly when
running real time benchmarks on a RT-PREEMPT kernel.
Accounting changes to max_latency to only measure the largest latency of a
single scheduling frame - this makes max_latency much smaller (and probably
more realistic). Often you may see max latency exactly one frame wide now
(consistent with one dropped frame) such as 16.7ms on video.
Minor cleanups.
```
Lee Revell, 0507.2/0020:
```
We should encourage more applications to take advantage of, and distros
to support, the non-root RT scheduling available in 2.6.12+.  I really
think the kernel is good enough at this point that we could achieve
OSX-like multimedia performance on the desktop if more apps like xmms,
xine, and mplayer were to adopt a multithreaded model with the
time-critical rendering threads running RT.  XMMS recently adopted such
a model, but I don't think the audio thread runs SCHED_FIFO yet.  These
benchmarks imply that it would be a massive improvement.
```
Lee Revell's results in the same thread are on "my 600MHz C3" running "2.6.12-RT-V0.7.51-28" (benchmark output tables only).

**Coverage.** Q1–Q4: nothing on the constants' origin; XMMS again named by Revell for its threading, not for a 50 ms write interval. **One observation?** No.

### S5-06 — Later release announcements 0.22, 0.24, 0.26, 0.27, 0.28, 0.29, 0.30 (changelogs)

**Citations and copies.**
- v0.22, Con Kolivas → linux-kernel, cc ck, "Wed, 20 Jul 2005 16:20:59 +1000", LWN copy `https://lwn.net/Articles/144328/` — `sources/S5-07-lwn/lwn-144328.html`, SHA-256 `a140084ff39f14d38758e68791bfe61b22c584061bcf07364a7787e7ea4ab8c7`.
- v0.24, "[ck] [ANNOUNCE] Interbench v0.24", ck list, list date "Fri Jul 29 11:00:59 2005" — in `sources/S5-ck-list/ck-2005-July.txt`.
- v0.26 ("Wed Aug 3 15:53:53 2005"), 0.27 ("Thu Aug 4 08:00:08 2005"), 0.28 ("Sat Aug 6 13:17:50 2005"), 0.29 ("Wed Aug 10 08:44:47 2005") — in `sources/S5-ck-list/ck-2005-August.txt.gz` (SHA-256 `616f7454c5193a67bd7709c78ac0d431c9ab1af5557a93eceeafcf390f1724a5`), decompressed alongside.
- v0.30, Con Kolivas → linux list, cc ck list, "Sat, 4 Mar 2006 14:11:05 +1100", LWN copy `https://lwn.net/Articles/174369/` — `sources/S5-07-lwn/lwn-174369.html`, SHA-256 `e0a40821276358780aa7e29d4dbaffd7c9cdff32c514edda21ad7e7b19b3094e`.
- Full list mbox to 2007-08 (`sources/S5-ck-list/ck.mbox-20070806.mbox`, SHA-256 `dd6f7d201ec0d0d5d26fe1f35be86ce65e0926afb37a384c1d76d608482b6cd5`) used to confirm no further interbench announcement exists on the ck list between 0.30 and August 2007 (subject survey, §1c #20). A v0.23 or v0.25 announcement was not found on the ck list (0.25's notes are folded into the 0.26 announcement); v0.23 is dated only by the tarball readme foot ("Wed Jul 27 11:26:24 2005").

**Verbatim changelogs.**

v0.22: "Changes since v0.21: / Real time processes were converted to also do mlockall(). / 2.4 kernel support was added thanks to Miguel Freitas. / Some overflow accounting bugs were fixed."

v0.24 (the only announcement that touches the periodic emulations):
```
Changes:
3 new loads were added:

Gaming benchmark:
This simulates an unlocked frame rate cpu intensive 3d gaming environment. It 
measures the latencies mean/sd/max and desired cpu percentage only. These 
should give a marker of frame rate stability (latencies), and maximum frame 
rates under different loads (desired cpu percentage). As this simulates an 
unlocked frame rate the deadlines met is meaningless. This does not 
accurately emulate a 3d game which is gpu bound, only a cpu bound one.

Hackbench:
Taken from Rusty's hackbench code as suggested by Ingo Molnar, this will run 
'hackbench 50' repeatedly in the background when benchmarking real time 
performance.

Custom:
Based on the periodic scheduling used for audio/video, custom will allow you 
to specify a cpu percentage and frame rate of a custom workload, and this can 
be used to benchmark this workload's performance under normal scheduling, 
real time scheduling or it can be used as a background load.
```

v0.26: "v0.25: / The timekeeping thread of background load no longer runs SCHED_FIFO. The / benchmark is allowed to proceed if it does not detect swap and instead / disables mem_load. The documentation was updated. // v0.26: / Fixed the standard deviation measurements at last (thanks Peter Williams). / There should be no practical limit to how long you can run a benchmark for / now."

v0.27: "Standard deviation and average latency calculation was corrected. Gaming / standard deviation was implemented."

v0.28: "Yet more floating point fixes mostly coutesy of Peter Williams - Thanks!"

v0.29: "Changes (PW: thanks to Peter Williams): / Altered the calibration loop. / Added the option to select loads to perform or not perform - PW / Added optional comment to logfile - PW / Numerous bugfixes - PW"

v0.30: "Hackbench as a load was made optional during realtime testing instead of / defaulting on as this load caused out of memory kills very easily. Some form / of userspace starvation is occurring (and this may be something useful to / instrument but I haven't the time). // Selecting or unselecting loads to benchmark was added (thanks Peter Williams) // Manpage was added (thanks Julien Valroff)."

**Coverage.** Q4: no announcement reports a change to the audio/video/X constants, consistent with the tarball diffs (S5-02). Q1–Q3: nothing. **One observation?** No.

### S5-07 — interbench homepages (2005 and 2009 captures)

**Citation.** Con Kolivas, "The homepage of Interbench, the Linux Interactivity benchmark": `http://members.optusnet.com.au/ckolivas/interbench/` (Wayback 20051119115545; "Download: Interbench v0.29") and `http://users.on.net/~ckolivas/interbench/` (Wayback 20090802111522; "Download: … Interbench v0.30"; the target `interbench.kolivas.org` redirected to the optusnet page in every 2005–2006 capture).

**Copies read.** `sources/S5-06-homepage/optusnet-20051119115545.html` (SHA-256 `b028ae5f58deeb13104c63da32e2ad8583b1ebb2b7a0bf4a4618d636eb9c44da`); `sources/S5-06-homepage/usersonnet-20090802111522.html` (`40dc8240cf311e23fdd459bc2f45d92efffea3bf382af56a72409a5e51039ff9`).

**Verbatim.** Both pages reproduce the readme; the 2009 page's Audio paragraph reads: "Audio is simulated as a thread that tries to run at 50ms intervals that then / requires 5% cpu. This behaviour ignores any caching that would normally be done / by well designed audio applications, but has been seen as the interval used to / write to audio cards by a popular linux audio player. It also ignores any of the / effects of different audio drivers and audio cards. Audio is also benchmarked / running SCHED_FIFO if the real time benchmarking option is used." The 2005 page carries the same sentence ("write to audio cards by a popular linux audio player. It also ignores any of the").

**Coverage.** Nothing beyond the readme. **One observation?** No.

### S5-08 — ck-hack blog, October 2016

**Citation.** Con Kolivas, "-ck hacking: Interbench benchmarks for MuQSS 116" (`http://ck-hack.blogspot.com/2016/10/interbench-benchmarks-for-muqss-116.html`) and "linux-4.8-ck4, MuQSS CPU scheduler v0.116" (`…/2016/10/linux-48-ck4-muqss-cpu-scheduler-v0116.html`).

**Copies read.** `sources/S5-04-blog/muqss116.html` (SHA-256 `b53f2933cd7f32ea070c1dce79522ff1cbe1351453cab574ca99282f88d336a7`); `sources/S5-04-blog/ck-hack.blogspot.com_2016_10_linux-48-ck4-muqss-cpu-scheduler-v0116.html.html` (`ae959635e40b856cf5880d4961662aeaf9d38600859deb306fa1dc903800611b`); the blog's own search page `…_search_q_interbench.html`.

**Verbatim.** "As mentioned in my previous post, I recently upgraded interbench which is a benchmark application I invented/wrote to assess perceptible latency in the setting of various loads. The updates were to make the results meaningful on today's larger ram/multicore machines where the load scales accordingly." … "This is a 3.6GHz hexcore with 64GB ram and fast Intel SSDs". From the ck4 post: "The results come up quite well now with interbench (my latency under load benchmark) which I have recently updated and should now give sensible values: / https://github.com/ckolivas/interbench / If you're baffled by interbench results, the most important number is %deadlines met which should be as close to 100% as possible followed by max latency which should be as low as possible for each section. In the near future I'll announce an official new release version."

**Coverage.** Q4: the 2016 "upgrade" is described as scaling *loads* to RAM/cores, matching the git commits (S5-01), which leave the audio/video/X constants untouched. Q1–Q3: nothing. **One observation?** The 2016 result tables are one run on the named hexcore; they do not bear on the constants' origin.

### S5-09 — Man page `interbench.8` (Julien Valroff, March 2006)

**Citation.** `interbench.8`, header `.TH interbench "8" "March 2006" "Interbench 0.30" "System Commands"` in `interbench-0.30.tar.bz2` (first version to ship it; 0.29 has none); `"Interbench 0.31"` in 0.31 and at git HEAD (the 0.30→0.31 diff is the version string and one added line "Recommend to run as root and set -L to number of CPUs on the system"). The 0.30 announcement credits "Manpage was added (thanks Julien Valroff)."; `debian_readme.txt` (SHA-256 `c15a3cede9976333d741a3d7f5c8b28b11b5bb7cead17e8304ff5ddda1933542`) reads in full: "interbench packages available here / (add to sources.lst): // deb http://julien.valroff.free.fr unstable main contrib non-free / deb-src http://julien.valroff.free.fr unstable main contrib non-free".

**Verbatim, `interbench.8` lines 76–93 at git HEAD.**
```
.B X:
X is simulated as a thread that uses a variable amount of cpu ranging from 0 to
100%. This simulates an idle gui where a window is grabbed and then dragged
across the screen.

.B Audio:
Audio is simulated as a thread that tries to run at 50ms intervals that then
requires 5% cpu. This behaviour ignores any caching that would normally be done
by well designed audio applications, but has been seen as the interval used to
write to audio cards by a popular linux audio player. It also ignores any of the
effects of different audio drivers and audio cards. Audio is also benchmarked
running SCHED_FIFO if the real time benchmarking option is used.

.B Video:
Video is simulated as a thread that tries to receive cpu 60 times per second
and uses 40% cpu. This would be quite a demanding video playback at 60fps. Like
the audio simulator it ignores caching, drivers and video cards. As per audio,
video is benchmarked with the real time option.
```

**Coverage.** The man page is a transcription of the readme; the "popular linux audio player" sentence originates in the 0.20 readme (S5-02/S5-03), not in the man page. **One observation?** No.

### S5-10 — Works citing interbench (Q5)

**S5-10a. Fan Wei Cong & Wong (ICGHIT 2020) and Fan's bachelor report (2020).**
- Peer-reviewed: "Comparison of Interactivity Performance of Linux CFS and Windows 10 CPU Schedulers", 2020 International Conference on Green and Human Information Technology (ICGHIT), DOI 10.1109/ICGHIT49656.2020.00014 (Semantic Scholar and OpenAlex records; IEEE Xplore paywalled — **not fetched, not read**).
- Open report by the same first author: Fan Wei Cong, *Interactivity Performance Benchmark for Windows and Mac OS*, bachelor's report, Universiti Tunku Abdul Rahman, `http://eprints.utar.edu.my/3865/1/16ACB02681_FYP.pdf` — copy `sources/S5-scholar/utar-2020-fan-fyp.pdf`, 160 pages, SHA-256 `e2377157d944dbf16b8efda96d8969acaa7009a503c3c34984d722a48d58c48c`. 147 occurrences of "interbench".
- Verbatim, p. 84 (PDF page): "X: A thread that utilizes amount of CPU that change from time to time ranging from 0% / to 100%. An idle Graphical User Interface (GUI) with a window being grabbed and / dragged across the screen is simulated / Audio: A thread which to execute at an interval of 50ms and requires 5% of CPU / utilization is used to simulate the Audio task. / Video: A thread which requires to utilize the 40% of CPU and attempts to receive from / the CPU 60 times per second is used to simulate the Video task. / Gaming: Emulates a CPU-bound game by using as much CPU as possible."
- Verbatim, p. 33 (literature review of the ICGHIT paper): "For interactive tasks with low CPU consumption, / such as Audio task that consumed only 5% of CPU resources and Video task that / consumed 40% of CPU resources, both operating systems showed a very similar results".
- Verbatim, p. 135: "At / the end of the verification, Audio interactive task's was proven to be able to generate / 5% CPU utilization which is similar to the original Linux Interbench."
- Coverage: restates the constants; gives no origin for 50 ms, 60 Hz, 40 % or the X sweep.

**S5-10b. Wong, Tan, Kumari, Lam, Fun 2008**, "Fairness and interactive performance of O(1) and CFS Linux kernel schedulers", 2008 International Symposium on Information Technology (ITSim), DOI 10.1109/ITSIM.2008.4631872 — paywalled (IEEE); ResearchGate/Academia copies login-walled; **not fetched, not read**. Whether it explains the constants is not established by this record.

**S5-10c. Jacob A. Cooper 2015**, *Multidimensional Load Balancing and Finer Grained Resource Allocation Employing Online Performance Monitoring Capabilities*, M.S. thesis, Ohio University (August 2015), OhioLINK ETD accession ohiou1438269844 — copy `sources/S5-scholar/ohio-2015-loadbalancing.pdf`, SHA-256 `052a56d35f33708a63705109d7e6ffa1aef1828072af8114300a22c33b2cd628`. Verbatim, p. 60: "The simulated audio load performs uncached reads from RAM at 50 millisecond / intervals and simulates decoding with a 5% cpu load. The video decoding simulation is / similar to the audio load simulation, though requires an additional resources. … The X / simulation requests between zero and complete utilization of the CPU, to simulate a user / performing operations within a GUI environment." Reference [17] (p. of bibliography): "C. Kolivas. (2006, March) The homepage of interbench the linux interactivity / benchmark. [Online]. Available: http://users.on.net/∼ckolivas/interbench/". Coverage: restates (and re-describes) the constants; no origin given. Not peer-reviewed (thesis).

**S5-10d. Waseda University doctoral thesis**, title per OpenAlex "Addressing Hybrid OS Environment Issues in the Embedded Virtualization Multicore Platform" (author and year not extracted from the copy's title page, which is partly glyph-encoded), `https://waseda.repo.nii.ac.jp/record/16836/files/Honbun-6572.pdf` — copy `sources/S5-scholar/waseda-hybrid-os.pdf`, SHA-256 `c053f788e20f815cebdaf690598e6dab4495c55d7ff210c5d48127d5da712dce`. Verbatim, PDF p. 85: "For generating some soft real-time workload in a GPOS and measuring the im- / pact of our migration approach, Interbench1 is used. Interbench emulates the / scheduling behavior of some interactive tasks and measures the latency and dead- / line miss, where the deadline of each task is given randomly. … Here, three interactive tasks, / Audio, Video and X system, are being used as measurement targets." Footnote 1: "http://users.on.net/~ckolivas/interbench/". Coverage: uses interbench; does not state or explain the constants. Not peer-reviewed (thesis).

**S5-10e. Not read.** "LOTTERY SCHEDULING IN THE LINUX KERNEL: A CLOSER LOOK" (Cal Poly M.S. thesis 2012; digitalcommons 403); "Collaborative Scheduling and Synchronization of Distributable Real-Time Threads" (Virginia Tech 2010; VTechWorks 404). "Agile Development of Linux Schedulers with Ekiben" (arXiv 2306.15076, fetched, SHA-256 `efa0068ec5c3a6ec63293beda99698918f05afe6c8318ccd36d67c77d278c131`) contains no occurrence of "interbench" — an OpenAlex false positive.

## 3. Not found

**Q1 — the "popular linux audio player": name, machine, method, date.** Not found in any primary text. Established by: the readme in every release 0.20 … 0.31 and at git HEAD (S5-01, S5-02) carries only "a popular linux audio player"; the v0.20 LKML announcement and all 20 messages of its thread (S5-03, §1b #8); the v0.21, v0.22, v0.24–v0.30 announcements (S5-05, S5-06); the ck-list July and August 2005 archives and the full ck mbox to August 2007 grepped for player names and "audio card"/"50 ms" phrases (§1c #18–20); the 2005 and 2009 homepages (S5-07); the 2016 blog posts (S5-08); the man page (S5-09); marc.info's 30 LKML hits 2007–2026 (§1b #11). XMMS is the only player named near interbench in 2005 (S5-03 f, S5-04 a, S5-05), each time by a user or by Lee Revell about thread scheduling — never by Kolivas and never as the source of the 50 ms figure. lore.kernel.org was unreadable (§1a), so a date-bounded lore search could not be run; the hypermail mirror's thread walk covered the announcement threads instead.

**Q2 — observation behind 60 Hz / 40 % CPU.** Not found. The only statements are the code comment "We emulate video by using 40% cpu and waking for 60fps" (0.20 `interbench.c:390`; HEAD `:510`) and the readme's "This would be quite a demanding video playback at 60fps." Searches as for Q1.

**Q3 — observation behind the X 0–100 % sweep.** Not found. The only statements are the code comment "We emulate X by running for a variable percentage of cpu from 0-100% in 1ms chunks." (0.20 `:411–414`; HEAD `:530–533`) and the readme's "This simulates an idle gui where a window is grabbed and then dragged across the screen." David Lang's question whether "the X load really linearly random in how much work it does" (S5-03 b) received no answer about the sweep's origin.

**Q4 — later revision of the constants.** None exists. Established by the pairwise diffs of all twelve tarballs (S5-02: values unchanged; 0.24 renamed identifiers; 0.28 widened `deadline` to `unsigned long long`), by `git log -L`/`-S` on the GitHub history (S5-01: only the initial import touches the lines), and by every release announcement 0.21–0.30 (S5-05, S5-06) plus the 2016 blog description of the last update (S5-08).

**Q5 — peer-reviewed use with the constants explained.** No peer-reviewed text explaining the constants was found. Semantic Scholar and OpenAlex (§1f #30–31) surface two peer-reviewed venues: Fan & Wong, ICGHIT 2020 (paywalled; its open sibling report restates the constants without origin, S5-10a) and Wong et al., ITSim 2008 (paywalled, not read, S5-10b). The three theses read (S5-10a, c, d) restate or merely use the constants.
