# S1 — peer-reviewed and preprint literature (T1, T2, T3, T4, T6)

Reader: S1 (literature). Date of work: 2026-09-17 (all accesses that day, UTC). Input read: `search/input.md` only.

Conventions of this record:

- Fetches were made with `curl` through the session proxy (TLS verified against `/root/.ccr/ca-bundle.crt`). PDFs were text-extracted with **PyMuPDF 1.28.2** (`fitz`; `page.get_text()`); pypdf 6.19.0 was installed but not used. HTML pages were reduced to text with a small tag-stripping script of my own for reading; passages below are quoted from the rendered text, and their locators name the article section/paragraph, not my extraction's line numbers.
- PDF locators are "p. N" = the N-th page of the fetched PDF file (not the printed page number) unless stated. Source-file locators are `file:line` at the named commit.
- Passages are verbatim except for two extraction normalisations, which I state here once: typographic ligatures (fi, fl, ff, ffl) that the extractor rendered as single glyphs or as the replacement character are written as plain letters; "∼" is written as "~".
- Where a number is my own computation it is labelled *reader's computation* with the command or arithmetic.
- Copies live under `sources/S1-NN/` (gitignored). Every citation carries URL, version, access date and SHA-256 so the record stands without the folder.
- Rule applied throughout: a response-side value (CPU per block/wake, wake cadence, run/wait, thread structure) is a candidate only from a Linux observation; other platforms and observations two decades old are recorded as *context* and marked so.

Candidate ids are provisional and not contiguous: S1-14 (GrAVity), S1-28 (Kolivas blog), S1-30 (Wong 2008) and S1-39 (SYSTOR 2009 compression) were assigned during the search and dropped because no copy could be fetched; they appear in the search log only. S1-09 (Lozi 2016) and S1-21 (Gouicem 2020) were fetched and read and found to cover no topic; they are listed in §3, not as candidates.

---

## 1. Search log

Engines/venues used: arXiv API (`export.arxiv.org/api/query`), WebSearch (the session's web-search tool; used to locate open copies, never as a source), LWN site search, lore.kernel.org, GitHub (raw/API/clone), Semantic Scholar API, OpenAlex API, publisher/author sites by direct URL. HTTP status in brackets.

| # | Date | Engine / venue | Query or URL | Hits followed / dead ends |
|---|------|----------------|--------------|---------------------------|
| 1 | 2026-09-17 | GitHub raw | `raw.githubusercontent.com/ckolivas/interbench/master/README` | [404] (file is `readme`, lowercase) |
| 2 | 2026-09-17 | Cornell author page | `cs.cornell.edu/~ragarwal/pubs/network-stack.pdf` | [200] → S1-02 |
| 3 | 2026-09-17 | MIT PDOS | `pdos.csail.mit.edu/papers/linux:osdi10.pdf` | [200] → S1-03 |
| 4 | 2026-09-17 | FSL Stony Brook | `fsl.cs.sunysb.edu/docs/fsbench/fsbench.pdf` | [200] → S1-04 |
| 5 | 2026-09-17 | USENIX legacy | `usenix.org/legacy/event/nsdi10/tech/full_papers/cha.pdf` | [200] → S1-05 |
| 6 | 2026-09-17 | samba.org | `samba.org/~tridge/phd_thesis.pdf` | [200] → S1-06 |
| 7 | 2026-09-17 | LWN | `lwn.net/Articles/682582/` | [200] → S1-07 |
| 8 | 2026-09-17 | USENIX legacy | `usenix.org/legacy/event/fast11/tech/full_papers/Meyer.pdf` | [200] → S1-08 |
| 9 | 2026-09-17 | UBC author page | `ece.ubc.ca/~sasha/papers/eurosys16-final29.pdf` | [200] but body is a "Browser Verification / UBC Cybersecurity" HTML page, not the PDF — dead end |
| 10 | 2026-09-17 | LWN | `lwn.net/Articles/925371/`, `lwn.net/Articles/969062/` | [200],[200] → S1-10, S1-11 |
| 11 | 2026-09-17 | arXiv API | `all:interbench` | 1 irrelevant hit (Hunyuan-GameCraft-2) |
| 12 | 2026-09-17 | arXiv API | `all:"background I/O" AND all:interactivity AND all:scheduler` | 0 hits |
| 13 | 2026-09-17 | arXiv API | `all:ClamAV` | 3 hits, none a ClamAV characterisation (Wu-Manber hardware 2003.00405; SafePickle; zero-day malware) — not followed |
| 14 | 2026-09-17 | arXiv API | `all:rsync AND all:CPU` | 0 hits |
| 15 | 2026-09-17 | arXiv API | `all:zstd AND all:compression AND all:benchmark` | 1 hit (LLM compression 2608.11249) — irrelevant |
| 16 | 2026-09-17 | arXiv API | `all:"desktop search" AND all:indexer` | 2 hits (Spotlight forensics 1903.07053; attacks on local search 1108.2704) — not overhead studies, not followed |
| 17 | 2026-09-17 | arXiv API | `all:Steam AND all:game AND all:download AND all:traffic` | 0 hits |
| 18 | 2026-09-17 | arXiv API | `all:"network stack" AND all:overhead AND all:"per-byte"` | 0 hits |
| 19 | 2026-09-17 | arXiv API | `all:SchedCP` | 2509.01245v4 → S1-12 |
| 20 | 2026-09-17 | arXiv API | `all:"sched_ext"` | 4 hits (2511.08297, 2605.02377, 2602.09345, 2511.11628) — DAG/database/agent scheduling, no desktop background-I/O load; not followed |
| 21 | 2026-09-17 | arXiv API | `all:"page cache" AND all:writeback AND all:latency AND all:desktop` | 0 hits |
| 22 | 2026-09-17 | arXiv API | `all:antivirus AND all:scan AND all:performance AND all:Linux` | 0 hits |
| 23 | 2026-09-17 | LWN site search | `lwn.net/Search/DoSearch?words=interbench` | [200] but the returned page carries no result list (search form only) — dead end |
| 24 | 2026-09-17 | lore.kernel.org | `lore.kernel.org/lkml/?q=interbench` | [403]; retry with browser UA [200] but body is an Anubis "Making sure you're not a bot!" challenge — dead end |
| 25 | 2026-09-17 | GitHub API | `api.github.com/repos/ckolivas/interbench/contents/`; `…/ckolivas/linux/branches` | proxy refusal ("Request path could not be canonicalized"; "GitHub access to this repository is not enabled for this session") — dead end |
| 26 | 2026-09-17 | ck.kolivas.org | `http://ck.kolivas.org/apps/interbench/` | [200] listing: `interbench-0.31.tar.bz2`, `interbench-0.31.tar.lrz`, `readme`; `https://` variant: connection reset [000]; `users.on.net/~ckolivas/interbench/` [503] |
| 27 | 2026-09-17 | git clone | `https://github.com/ckolivas/interbench` (depth 1) | OK, HEAD e612a65ce941028ddea804e6b45ccde2750720d2 (2016-10-24) → S1-01 |
| 28 | 2026-09-17 | WebSearch | Torrey Coleman Miller "A comparison of interactivity in the Linux 2.6 scheduler and an MLFQ scheduler" pdf | `ftp.cs.wisc.edu/pub/paradyn/papers/LinuxSched-SPE2007.pdf` [200] → S1-13 |
| 29 | 2026-09-17 | WebSearch | Uluski Moffie Kaeli "Characterizing antivirus workload execution" pdf | ResearchGate PDF link [403]; kipdf.com transcription (not the paper) — no open copy; Windows XP per abstract — not fetched |
| 30 | 2026-09-17 | WebSearch | Vasiliadis Ioannidis "GrAVity: A Massively Parallel Antivirus Engine" pdf | `publications.ics.forth.gr/…/gravity_raid10.pdf` [000, TLS/connect failure], `projects.ics.forth.gr/…` [000], `link.springer.com/content/pdf/10.1007/978-3-642-15512-3_5.pdf` [200] but HTML paywall page — dead end (S1-14 dropped) |
| 31 | 2026-09-17 | WebSearch | Endo Seltzer "Improving Interactive Performance Using TIPME" pdf | only ResearchGate/ACM; `eecs.harvard.edu/~margo/papers/sigmetrics00-tipme/paper.pdf` [200] but HTML, not PDF; OSDI'96 Endo et al. `.ps` at usenix.org [200] but no PostScript converter on the box — not read (Windows NT study; context at best) |
| 32 | 2026-09-17 | WebSearch | Wallace Douglis "Characteristics of Backup Workloads in Production Systems" FAST 2012 | `usenix.org/system/files/conference/fast12/wallace2-9-12.pdf` [200] → S1-15 |
| 33 | 2026-09-17 | WebSearch | Humphries "ghOSt: Fast & Flexible User-Space Delegation of Linux Scheduling" pdf | `cs.stanford.edu/~jhumphri/documents/ghost.pdf` [200] → S1-16 |
| 34 | 2026-09-17 | WebSearch | Lozi Lepers Quema "The Linux Scheduler: a Decade of Wasted Cores" pdf | `cs.utexas.edu/~venkatar/sys_perf_analysis/linux-wasted-cores.pdf` [200] (HAL hal-01295194 copy) → read, no coverage (§3) |
| 35 | 2026-09-17 | WebSearch | LWN large file copy desktop stalls dirty pages writeback interactivity | `lwn.net/Articles/532455/` [200] → S1-17; `lkml.iu.edu/hypermail/linux/kernel/1008.0/00361.html` [200] → S1-18; Red Hat bug 552634 and `lwn.net/Articles/396561/` not followed (bug tracker is S3's class; reclaim article off-topic) |
| 36 | 2026-09-17 | WebSearch | paper measurement rsync CPU utilization I/O wait backup tool performance evaluation borg restic | only blogs and GitHub benchmark repos (borgbase/benchmarks etc.) — no peer-reviewed hit |
| 37 | 2026-09-17 | WebSearch | study desktop search indexer overhead energy inotify Tracker Baloo laptop paper | wikis/forums only — no paper |
| 38 | 2026-09-17 | WebSearch | Steam game download depot characterization measurement study paper throughput | Visser & Fontugne PAM 2024 (Springer, paywalled) → see #45 |
| 39 | 2026-09-17 | WebSearch | ClamAV multithreaded scanning throughput performance evaluation paper Linux clamd | ResearchGate "Applying Parallelization Techniques to Speedup ClamAV" (no open copy); ClamAV docs (S2's class) |
| 40 | 2026-09-17 | Semantic Scholar API | `paper/search?query=interbench+scheduler+interactivity` | [429] Too Many Requests — dead end |
| 41 | 2026-09-17 | OpenAlex API | `works?search=interbench scheduler interactivity` | [429] "Insufficient budget" — dead end |
| 42 | 2026-09-17 | ResearchGate | Uluski 2005 PDF direct link | [403] |
| 43 | 2026-09-17 | Wiley | `onlinelibrary.wiley.com/doi/pdfdirect/10.1049/iet-ifs.2012.0192` (Al-Saleh, IET IFS) | [403]; open preprint found at `cs.unm.edu/~csgsa/archive/2010-2011/papers/MohammedAl-saleh.pdf` [200] → S1-19 |
| 44 | 2026-09-17 | USENIX | `usenix.org/system/files/atc20-gouicem.pdf` | [200] → read, no coverage (§3) |
| 45 | 2026-09-17 | WebSearch | Visser Fontugne "Inside the Engine Room" Steam content delivery PAM 2024 pdf | `pam2024.cs.northwestern.edu/pdfs/paper-08.pdf` [000, TLS handshake failed through proxy, twice]; IIJ member page → `iijlab.net/en/members/romain/pdf/chris_pam2024.pdf` [200] → S1-22 |
| 46 | 2026-09-17 | WebSearch | "Applying Parallelization Techniques to Speedup ClamAV" pdf | only ResearchGate/SpeakerDeck; MDPI Symmetry 2017 OpenMP-ClamAV paper found: `mdpi.com/2073-8994/9/9/172/pdf` [403]; `pdfs.semanticscholar.org/acd5/fb8955767547927ef6a01edce82cd0f33468.pdf` [200] → S1-24 |
| 47 | 2026-09-17 | WebSearch | "interbench" scheduler evaluation paper results "Write" "Read" load latency | Wong et al. 2008 (ITSim) found; `ieeexplore.ieee.org/iel5/4625945/4631845/04631872.pdf` [202 → HTML document page, paywalled]; academia.edu/ResearchGate login-walled — S1-30 dropped |
| 48 | 2026-09-17 | WebSearch | paper benchmark lossless compression tools zstd xz brotli CPU time energy Linux measurement | arXiv 2510.07015 (time-series libraries, not CLI tools) and 2312.10301 (FCBench) — not the programs in scope; not followed |
| 49 | 2026-09-17 | WebSearch | paper inotify file system change notification overhead CPU wakeups measurement study | Linux Journal "Intro to inotify" (Love 2005) → S1-40 (context); no measurement paper |
| 50 | 2026-09-17 | WebSearch | Steam download measurement client "six parallel TCP" chunks paper | ThousandEyes/SamKnows blog (not literature) — not fetched |
| 51 | 2026-09-17 | WebSearch | "Characterizing antivirus workload execution" Uluski citeseerx OR kipdf OR pdf | no open copy of the paper itself |
| 52 | 2026-09-17 | WebSearch | HTTP download client wget curl aria2 parallel connections performance measurement study paper CPU | arXiv 2310.09423 "QUIC is not Quick Enough over Fast Internet" (cURL CPU on Linux) → `arxiv.org/pdf/2310.09423` [200] → S1-23 |
| 53 | 2026-09-17 | arXiv | `arxiv.org/pdf/2509.01245v4` | [200] → S1-12 |
| 54 | 2026-09-17 | WebSearch | Wong Tan Kumari Wei "Fairness and interactive performance of O(1) and CFS Linux kernel schedulers" pdf | see #47 — paywalled |
| 55 | 2026-09-17 | WebSearch | desktop search engines Linux Beagle Tracker Strigi indexing performance evaluation paper CPU memory | 2007 Sun-employee comparison (Pryc & Hou) reported second-hand on blogs/OSnews; original not located — not literature |
| 56 | 2026-09-17 | WebSearch | rsync performance analysis paper CPU bound I/O bound measurement Linux "rsync" sender receiver generator profiling | `lwn.net/Articles/400489/` [200] → S1-25 |
| 57 | 2026-09-17 | WebSearch | Erdogan Cao "Hash-AV" fast virus signature scanning ClamAV pdf | `crypto.stanford.edu/~cao/hash-av.pdf` [200] → S1-29 |
| 58 | 2026-09-17 | ck.kolivas.org | `patches/muqss/sched-MuQSS.txt`, `patches/bfs/bfs-faq.txt`, `patches/bfs/bfs-configuration-faq.txt` | [200]×3 → S1-26, S1-27 |
| 59 | 2026-09-17 | ck-hack.blogspot.com | `2016/10/muqss-multiple-queue-skiplist-scheduler.html` (https, http, browser UA) | [503]×3 — dead end (S1-28 dropped) |
| 60 | 2026-09-17 | WebSearch | Pryc Hou Sun "desktop indexers" comparison Beagle JIndex Tracker Strigi pdf 2007 | only blog reports — dead end |
| 61 | 2026-09-17 | WebSearch | Linux TCP receive "cycles per byte" data copy overhead measurement study kernel network stack paper | Menon & Zwaenepoel USENIX ATC 2008 → `usenix.org/legacy/event/usenix08/tech/full_papers/menon/menon.pdf` [200] → S1-34; Wu & Crawford CHEP 2006 slides → `indico.cern.ch/…/CHEP06.pdf` [200] → S1-33 |
| 62 | 2026-09-17 | WebSearch | deduplication backup tools evaluation "BorgBackup" OR "restic" OR "duplicity" performance study journal OR conference paper | blogs only — no paper |
| 63 | 2026-09-17 | WebSearch | LWN EEVDF wakeup preemption I/O-bound tasks lag "sleeper" latency article 2024 2025 | `lists.ozlabs.org/pipermail/linuxppc-dev/2024-February/268909.html` [200] → S1-31; LWN 969062 already S1-11 |
| 64 | 2026-09-17 | arXiv API | `all:"file indexing" AND all:daemon`; `all:Baloo`; `all:Tracker AND all:GNOME AND all:index`; `all:borg AND all:backup AND all:deduplication`; `all:wget AND all:download AND all:CPU`; `all:SMTP AND all:client AND all:CPU`; `all:"page cache" AND all:copy AND all:interactive`; `all:interactivity AND all:Linux AND all:scheduler AND all:desktop`; `all:antivirus AND all:overhead AND all:characterization` | 0 relevant hits each (Baloo returns a robotics torso and unrelated physics; 7-Zip query returns grammar-compression theory) |
| 65 | 2026-09-17 | WebSearch | Nepomuk Strigi semantic desktop indexing CPU overhead evaluation paper KDE | wikis/blogs only |
| 66 | 2026-09-17 | WebSearch | scx_lavd sched_ext gaming background load LWN article latency criticality | `lpc.events/event/18/contributions/1713/attachments/1425/3058/scx_lavd-lpc-mc-24.pdf` [200] → S1-36; `lwn.net/Articles/991205/` [200] → S1-37 |
| 67 | 2026-09-17 | WebSearch | energy consumption measurement file compression utilities gzip xz zstd 7z Linux paper | `ece.uah.edu/~milenka/docs/aadam_mascots13.pdf` [200] → S1-38; SYSTOR 2009 compression paper `fsl.cs.sunysb.edu/docs/systor09-compression/systor09-compression.pdf` [404], not listed on `fsl.cs.sunysb.edu/docs/` — dead end (S1-39 dropped) |
| 68 | 2026-09-17 | WebSearch | Linux desktop responsiveness under heavy I/O empirical study paper "iowait" latency interactive applications | `people.cs.umass.edu/~emery/pubs/redline.pdf` [200] → S1-35; Ubuntu bug 131094 (bug tracker, S3's class) not followed |
| 69 | 2026-09-17 | Linux Journal | `linuxjournal.com/article/8478` | [200] → S1-40 |

---

## 2. Candidates

### S1-01 — Kolivas, *interbench* readme, readme.interactivity and source

**Citation.** Con Kolivas, "Interbench - The Linux Interactivity Benchmark" (readme dated "Sat Oct 31 15:17:12 2009"; readme.interactivity dated "Mon Jul 11 17:29:21 2005"); interbench.c. Distributed as interbench 0.31 (`http://ck.kolivas.org/apps/interbench/`) and as git repository `https://github.com/ckolivas/interbench`.

**Copies read.**
- `http://ck.kolivas.org/apps/interbench/readme`, accessed 2026-09-17, `sources/S1-01/interbench-0.31-readme`, SHA-256 `a67f2b8b3d92896e63f2f03e25dc3f59077eb49192fa353d56cbe0da1f7c0b29` (10 769 bytes). Byte-identical (`diff`) to the git `readme`.
- git clone of `https://github.com/ckolivas/interbench`, commit `e612a65ce941028ddea804e6b45ccde2750720d2` (2016-10-24), accessed 2026-09-17: `readme` SHA-256 as above; `readme.interactivity` SHA-256 `d18bc9cacbbf05a81c88637d2668b657df76442bb21f022f70ef3ee1ef502ff1`; `interbench.c` SHA-256 `a381b94085427cda4169466d3833c272fe4e9672cfbad74a64897621db7f2191`. Saved as `sources/S1-01/git-readme`, `git-readme.interactivity`, `git-interbench.c`.

**Passages.**

readme, "What does it do?" (lines 16–19):
> It is designed to emulate the cpu scheduling behaviour of interactive tasks and measure their scheduling latency and jitter. It does this with the tasks on their own and then in the presence of various background loads, both with configurable nice levels and the benchmarked tasks can be real time.

readme, "How does it work?" (lines 28–35):
> It runs a real time high priority timing thread that wakes up the thread or threads of the simulated interactive tasks and then measures the latency in the time taken to schedule. As there is no accurate timer driven scheduling in linux the timing thread sleeps as accurately as linux kernel supports, and latency is considered as the time from this sleep till the simulated task gets scheduled.
>
> Each benchmarked simulation runs as a separate process with its own threads, and the background load (if any) also runs as a separate process.

readme, "What loads are simulated?" (lines 84–96):
> Burn: A configurable number of threads fully cpu bound (4 by default).
> Write: A streaming write to disk repeatedly of a file the size of physical ram.
> Read: Repeatedly reading a file from disk the size of physical ram (to avoid any caching effects).
> Compile: Simulating a heavy 'make -j4' compilation by running Burn, Write and Read concurrently.

readme, "What is measured and what does it mean?" (lines 116–122):
> 1. The average scheduling latency (time to requesting cpu till actually getting it) of deadlines met during the test period. 2. The scheduling jitter is represented by calculating the standard deviation of the latency 3. The maximum latency seen during the test period 4. Percentage of desired cpu 5. Percentage of deadlines met.

readme, "Sample:" (lines 128–136; columns: Load, Latency +/- SD (ms), Max Latency, % Desired CPU, % Deadlines Met):
> --- Benchmarking simulated cpu of X in the presence of simulated ---
> None 0.495 +/- 0.495 45 100 96
> Video 11.7 +/- 11.7 1815 89.6 62.7
> Burn 27.9 +/- 28.1 3335 78.5 44
> Write 4.02 +/- 4.03 372 97 78.7
> Read 1.09 +/- 1.09 158 99.7 88
> Compile 28.8 +/- 28.8 3351 78.2 43.7
> Memload 2.81 +/- 2.81 187 98.7 85

readme, "What is relevant in the data?" (lines 154–163):
> The results pessimise quite a lot what happens in real world terms because they ignore the reality of buffering, but this allows us to pick up subtle differences more readily. […] Average humans' limit of perception for jitter is in the order of 7ms. Trained audio observers might notice much less.

readme, "Longer version:" (lines 187–191):
> You need free disk space in the directory it is being run in the order of 2* your physical ram for the disk loads. A default run in v0.21 takes about 15 minutes to complete, longer if your disk is slow.

readme, options (lines 210–211, 215):
> -t Seconds to run each benchmark (default: 30)
> -B Nice the benchmarked thread to <int> (default: 0)
> -N Nice the load thread to <int> (default: 0)

readme.interactivity (lines 9–13):
> Responsiveness: The rate at which your workloads can proceed under different load conditions.
> Interactivity: The scheduling latency and jitter present in tasks where the user would notice a palpable deterioration under different load conditions.

interbench.c at e612a65, the Write load (`interbench.c:632–663`):
```c
/* Write a file the size of ram continuously */
void emulate_write(struct thread *th)
{
	…
	if (statbuf.st_blksize < MIN_BLK_SIZE)
		statbuf.st_blksize = MIN_BLK_SIZE;
	mem = ud.filesize / (statbuf.st_blksize / 1024);	/* kilobytes to blocks */
	…
	while (1) {
		unsigned int i;

		if (!(fp = fopen(name, "w")))
			terminal_error("fopen");
		if (stat(name, &statbuf) == -1)
			terminal_fileopen_error(fp, "stat");
		for (i = 0 ; i < mem; i++) {
			if (fwrite(buf, statbuf.st_blksize, 1, fp) != 1)
				terminal_fileopen_error(fp, "fwrite");
			if (!trywait_sem(s))
				goto out;
		}
		if (fclose(fp) == -1)
			terminal_error("fclose");
	}
```
(`interbench.c:53`: `#define MIN_BLK_SIZE		1024`.)

interbench.c, the Read load (`interbench.c:679–712`):
```c
/* Read a file the size of ram continuously */
void emulate_read(struct thread *th)
{
	…
	bsize = statbuf.st_blksize;
	…
	while (1) {
		int rd;

		/*
		 * We have to read the whole file before quitting the load
		 * to prevent the data being cached for the next read. This
		 * is also the reason the file is the size of physical ram.
		 */
		while ((rd = Read(tmp , buf, bsize)) > 0);
		if(!trywait_sem(s))
			return;
		if (lseek(tmp, (off_t)0, SEEK_SET) == -1)
			terminal_error("lseek");
	}
}
```

interbench.c, file-size cap (`interbench.c:1189–1193`):
```c
	/* Limit filesize to 1GB */
	if (ud.ram > 1000)
		ud.filesize = 1000000;
	else
		ud.filesize = ud.ram;
```
and the flush used after creating the read file and after the write load (`interbench.c:243–250`): `sync_flush()` calls `fflush(NULL)` then `sync(); sync(); sync();`.

**Coverage.**
- **T6 — covers.** Object: interbench's "Write" and "Read" background loads; unit: the load is a single process doing buffered `fwrite` of `st_blksize` blocks (≥1024 B) to a file of `MemTotal` capped at 1 000 000 kB, re-opened and rewritten continuously, no `fsync`/`O_DIRECT`, `sync()` only at the end; the Read load `read()`s the same-sized file in `st_blksize` chunks and `lseek`s back. Statistic reported for interactive simulations under each load: mean scheduling latency ± SD (ms), max latency (ms), % desired CPU, % deadlines met, over `-t` seconds (default 30). Scope: the readme's "Sample" is one table for the X simulation (Write: 4.02 ± 4.03 ms, max 372 ms, 97 % desired CPU, 78.7 % deadlines; Read: 1.09 ± 1.09 ms, max 158 ms, 99.7 %, 88 %). Population: one unnamed machine, unnamed kernel, unnamed date. "What the literature says such a load does": the readme's own interpretation of dropped deadlines and the 7 ms jitter threshold.
- **T1 — does not cover** (the loads are the benchmark's own, not `rsync`/`cp`/`tar`; no CPU share reported for the load itself).
- T2, T3, T4 — does not cover.

**Observation status.** The sample table is one run; machine, kernel and date are *not* named; the subject (interbench version) is named indirectly ("v0.21" in the run-time note; readme shipped with 0.31); window: 30 s per benchmark by default. Linux: yes.

---

### S1-25 — van Winkel, "A look at rsync performance" (LWN, 2010)

**Citation.** JC van Winkel, "A look at rsync performance", LWN.net, 2010-08-18, `https://lwn.net/Articles/400489/`.

**Copy read.** `https://lwn.net/Articles/400489/`, accessed 2026-09-17, `sources/S1-25/lwn-400489-rsync-performance.html`, SHA-256 `5c7e40bf87302c31a1131092b3971a2be6cdc1e4f10359609aa915a0358c120a` (74 571 bytes).

**Passages.**

Section "The problem", paragraph 1:
> Recently I bought a shiny new disk for my Fedora-10 based Mythtv system. I had to copy some 700GiB of video files from the old disk to the new one. […] the files were copied at about 37MiB/s. Both disks can handle about three times that speed — at least on the outer cylinders. […] Note that both SATA disks were local to the system and no network was involved.

Section "Measuring", paragraphs 1–3:
> Wanting to know what happened, I created a small test to see what was going on: copying a 10GiB file from one disk to the other. I made sure that the ext4 file systems involved were completely fresh so fragmentation could not play a part (a new mkfs after each test.) […] Simply reading the source file could be done at 106MiB/s and writing a 10GiB file to the destination file system could be done at 134MiB/s.
>
> The copy programs under test were rsync, cpio, cp, and cat. Of course I took care that the cache could not interfere by flushing the cache before each test, and waiting for the dirty buffers to be flushed to the destination disk after the test command completes. […]
> sync # flush dirty buffers to disk
> echo 3 > /proc/sys/vm/drop_caches # discard caches
> time sh -c "cp $SRC $DEST; sync" # measure cp and sync time

Section "Measuring", results table (the HTML table renders in my extraction with columns run together; header "user sys elapsed hog MiB/s test"; quoted as rendered):
> usersyselapsedhogMiB/stest
> 5.2477.92101.8681%100.53cpio
> 0.8553.77101.1254%101.27cp
> 1.7359.47100.8460%101.55cat
> 139.6993.50280.4083%36.52rsync

*Reader's parsing of that table (column split by the two-decimal pattern):* cpio user 5.24 s, sys 77.92 s, elapsed 101.86 s, hog 81 %, 100.53 MiB/s; cp 0.85 / 53.77 / 101.12 / 54 % / 101.27; cat 1.73 / 59.47 / 100.84 / 60 % / 101.55; rsync 139.69 / 93.50 / 280.40 / 83 % / 36.52.

Section "Measuring", paragraph after the table:
> The observation that rsync was slow was indeed substantiated. Looking at the hog factor (the amount of cpu-time used relative to the elapsed time), we can conclude that rsync is not so much disk-bound (as is to be expected), but cpu-bound. That required some more scrutiny. The atop program showed rsync appears to need three processes: one process that does only disk reads, one that does only disk writes and one (I assume) control process that uses little CPU time and does no disk I/O.
>
> Using strace, it can be shown that cp only uses read() and write() system calls in a tight loop, while rsync uses two processes that talk to each other using reads and writes through a socket, sprinkled with loads of select() system calls.

Section "The kernel plays a role too":
> On my 4-core AMD Athlon II X4 620 system, all three processes seem to run on the same CPU most of the time. […] By using taskset right after rsync was started, the throughput of rsync went up from 36.5MiB to 40MiB. Though a 10% improvement, it was still nowhere near cat's performance. When forcing the three rsync processes to run on the same CPU, performance went down to 32MiB/s
>
> rsync needs quite a lot of CPU power (both user and system time). Despite that, the on-demand frequency governor does not scale up the CPU frequency. […] If the CPU-frequency is forced on the highest frequency (2.6GHz), the results for three rsyncs on a single core goes up: 62MiB/s. Combining this with the "spread the load" tactic using taskset, we even get up to 85MiB/s.

Section "The future":
> In the time the processor is waiting for the I/O to finish, the clock frequency is scaled down almost immediately. But when the disk request finishes, and the process continues using the CPU, the ondemand governor waits too long in scaling the frequency back up again.
> […] I compiled kernel version 2.6.35-rc3 that has the patches incorporated and used that instead of the 2.6.27.41-170.2.117 kernel Fedora 10 was running when the original problem popped up. For comparison, I also ran the tests with a more recent kernel that does not incorporate Arjan's patches: 2.6.34

**Coverage.**
- **T1 — covers.** Object: `rsync` (local disk-to-disk copy of one 10 GiB file), against `cp`, `cpio`, `cat`; unit: user and sys CPU seconds, elapsed seconds, "hog" = CPU time / elapsed (%), MiB/s; statistic: one value per command (single run as reported); scope: cold page cache (`sync; echo 3 > drop_caches`), fresh ext4, Fedora 10 kernel 2.6.27.41, later 2.6.34 and 2.6.35-rc3, 4-core AMD Athlon II X4 620 with ondemand governor; process structure: three rsync processes (reader, writer, control) observed with `atop`, socket + `select()` observed with `strace`; the effect of the ondemand governor on an I/O-waiting process. Not covered: on-CPU run lengths between waits, per-block CPU, rsync version, `-a` multi-file trees.
- T2, T3, T4, T6 — does not cover.

**Observation status.** One observation set on one named machine; subject rsync (version not named), input one 10 GiB file, cache state cold; window = one full copy per command (~100–280 s). Linux, 2010 — a Linux observation (16 years old; hardware and kernel dated but the structure is an rsync property).

---

### S1-02 — Cai et al., "Understanding Host Network Stack Overheads" (SIGCOMM 2021)

**Citation.** Qizhe Cai, Shubham Chaudhary, Midhul Vuppalapati, Jaehyun Hwang, Rachit Agarwal, "Understanding Host Network Stack Overheads", ACM SIGCOMM 2021 (SIGCOMM '21, August 23–27, 2021, Virtual Event, USA).

**Copy read.** `https://www.cs.cornell.edu/~ragarwal/pubs/network-stack.pdf`, accessed 2026-09-17, `sources/S1-02/cai2021-network-stack.pdf`, SHA-256 `1ea9fdde87ddc709d002b7b16287eed65d7426a3a85bb5768943b78c592ed6bd` (2 643 423 bytes, 13 pages).

**Passages.**

p. 1, §1 key findings:
> High-bandwidth links result in performance bottlenecks shifting from protocol processing to data copy. Modern Linux network stack can achieve ~42Gbps throughput-per-core by exploiting all commonly available features in commodity NICs, e.g., segmentation and receive offload, jumbo frames, and packet steering. While this throughput is for the best-case scenario of a single long flow, the dominant overhead is consistent across a variety of scenarios—data copy from kernel buffers to application buffers (e.g., > 50% of total CPU cycles for a single long flow). This is in sharp contrast to previous studies on short flows and/or low-bandwidth links, where protocol processing was shown to be the main bottleneck. We also observe receiver-side packet processing to become a bottleneck much earlier than the sender-side.

p. 3, §2.2 "Testbed setup":
> Both of our servers have a 4-socket NUMA-enabled Intel Xeon Gold 6128 3.4GHz CPU with 6 cores per socket, 32KB/1MB/20MB L1/L2/L3 caches, 256GB RAM, and a 100Gbps Mellanox ConnectX-5 Ex NIC connected to one of the sockets. Both servers run Ubuntu 16.04 with Linux kernel 5.4.43.

p. 4, §2.2 metrics:
> […] utilization across all cores (using sysstat [19], which includes kernel and application processing), and throughput-per-core—ratio of total throughput and total CPU utilization at the bottleneck (sender or receiver). To perform CPU profiling, we use the standard sampling-based technique to obtain a per-function breakdown of CPU cycles [20].

p. 4, §3.1:
> A single core is no longer sufficient. For 10−40Gbps access link bandwidths, a single thread was able to saturate the network bandwidth. However, such is no longer the case for high-bandwidth networks: as shown in Fig. 3(a), even with all optimization enabled, Linux network stack achieves throughput-per-core of ~42Gbps. Both Jumbo frames and TSO/GRO reduce the per-byte processing overhead as they allow each skb to bring larger payloads (up to 9000B and 64KB respectively).

p. 5, §3.1:
> Receiver-side CPU is the bottleneck. Fig. 3(b) shows the overall CPU utilization at sender and receiver sides. Independent of the optimizations enabled, receiver-side CPU is the bottleneck. There are two dominant overheads that create the gap between sender and receiver CPU utilization: (1) data copy and (2) skb allocation. […] Second, when TSO is enabled, the sender is able to allocate large-sized skbs. The receiver, however, allocates MTU-sized skbs at device driver and then the skbs are merged at GRO layer. Therefore, the receiver incurs higher overheads for skb allocation.

**Coverage.**
- **T3 — covers (server-class, not consumer).** Object: Linux 5.4.43 TCP receive and send path; unit: throughput-per-core (Gbps per 100 % of one core) and per-function share of CPU cycles; statistic: ~42 Gbps per core best case, data copy > 50 % of cycles for a single long flow, receiver more expensive than sender; scope: two directly connected 100 Gbps servers, Xeon Gold 6128, Ubuntu 16.04; population: one testbed. Not covered: a consumer link, a user-space downloader's own CPU, bytes per wake or wakes per second, disk-write work per chunk. Mark: *server hardware and 100 Gbps link; Linux; usable as an upper-bound ratio, not as a desktop value*.
- T1, T2, T4, T6 — does not cover.

**Observation status.** One testbed, machine named, kernel named, workloads described (single long flow etc.); window per experiment not given in the quoted passages.

---

### S1-34 — Menon & Zwaenepoel, "Optimizing TCP Receive Performance" (USENIX ATC 2008) — *context: 18 years old*

**Citation.** Aravind Menon, Willy Zwaenepoel, "Optimizing TCP Receive Performance", 2008 USENIX Annual Technical Conference.

**Copy read.** `https://www.usenix.org/legacy/event/usenix08/tech/full_papers/menon/menon.pdf`, accessed 2026-09-17, `sources/S1-34/menon2008-tcp-receive.pdf`, SHA-256 `4b01d572f3f6a62acd362b3acc872d05c8a800c71b2c231490c7aeeb7aa01059` (226 489 bytes, 14 pages).

**Passages.**

p. 2, §2:
> We use a simple netperf [1] like microbenchmark, which receives data continuously over a single TCP connection at Gigabit rate. […] The experiments are run on a 3.80 GHz Intel Xeon dual-core machine, with an Intel e1000 Gigabit NIC. The native Linux kernel version used is Linux 2.6.16.34 […] Profile statistics are collected and reported using the OProfile [2] tool.

p. 2–3, §2.1:
> The total processing overhead is divided into three categories: the per-byte data copying routines, per-byte, the per-packet routines, per-packet, and other miscellaneous routines, misc. […]
> As the CPU is configured to prefetch more aggressively, the contribution of the per-byte operations to the overall overhead declines from 52% to 14%. The proportion of the per-packet operations in the overall overhead increases correspondingly from 37% to nearly 70%, and becomes more important than the per-byte overheads.

**Coverage.**
- **T3 — context.** Object: Linux 2.6.16 TCP receive of MTU-sized packets at 1 Gbps; unit: share of receive-processing CPU cycles by class (per-byte copy vs per-packet); statistic: per-byte 52 % → 14 % as prefetching is enabled; scope: one 3.8 GHz Xeon, e1000 NIC, single connection. Linux, but 2008 and a 2.6.16 kernel; recorded as context for the per-byte/per-packet split.
- Other topics — does not cover.

**Observation status.** One machine, named; kernel named; window not stated in the quoted passage.

---

### S1-33 — Wu & Crawford, "The Performance Analysis of Linux Networking – Packet Receiving" (CHEP 2006 slides) — *context: 20 years old*

**Citation.** Wenji Wu, Matt Crawford (Fermilab), "The Performance Analysis of Linux Networking – Packet Receiving", CHEP 2006 presentation slides.

**Copy read.** `https://indico.cern.ch/event/408139/session/6/contribution/132/attachments/815628/1117588/CHEP06.pdf` (served from `…/contributions/979737/…`), accessed 2026-09-17, `sources/S1-33/wu2006-chep-linux-packet-receiving.pdf`, SHA-256 `2920379af6dd7c1fff8cabaf531e1543c9c5e7154c83a00d95ba423c4d3742fa` (762 288 bytes, 27 slides).

**Passage.** Slide 21, "Experiment Settings", table "Sender & Receiver Features":
> CPU — Two Intel Xeon CPUs (3.0 GHz) — One Intel Pentium II CPU (350 MHz)
> System Memory — 3829 MB — 256MB
> NIC — Tigon, 64bit-PCI bus slot at 66MHz, 1Gbps/sec, twisted pair — Syskonnect, 32bit-PCI bus slot at 33MHz, 1Gbps/sec, twisted pair

**Coverage.** T3 — *context only* (2006, Linux 2.4/2.6-era packet-receive path on a Pentium II receiver; no per-process downloader figure). Other topics — does not cover. Recorded because the search direction named "kin" of Cai; it adds nothing usable beyond the hardware of the era.

---

### S1-23 — Zhang et al., "QUIC is not Quick Enough over Fast Internet" (WWW 2024; arXiv 2310.09423v2)

**Citation.** Xumiao Zhang, Shuowei Jin, Yi He, Ahmad Hassan, et al., "QUIC is not Quick Enough over Fast Internet", in Proceedings of the ACM Web Conference 2024 (WWW '24), May 13–17, 2024; arXiv:2310.09423v2 [cs.NI], 30 Sep 2024.

**Copy read.** `https://arxiv.org/pdf/2310.09423` (resolved to v2), accessed 2026-09-17, `sources/S1-23/quic-not-quick-2310.09423.pdf`, SHA-256 `c000afca3e29275cd5a091e8867461b54559a20b273487bf6ec70ac22dd9cd32` (839 783 bytes, 10 pages).

**Passages.**

p. 1, §1:
> We begin with comparing QUIC and HTTP/2 in a simple environment: file download using a command-line data transfer tool, cURL [1], and a Chromium-based client, quic_client [26]. […] The results show that QUIC and HTTP/2 exhibit similar performance when the network bandwidth is relatively low (below ~600 Mbps), whereas under a higher network bandwidth, QUIC consistently lags behind HTTP/2 by up to 15.7% in terms of throughput. […] Notably, during packet reception, QUIC incurs considerably higher CPU usage than HTTP/2 on state-of-the-art client hosts.

p. 3, §3.1 testbed:
> We deploy a server machine equipped with an Intel Xeon E5-2640 CPU and a client desktop featuring an Intel Core i7-6700 CPU. They are connected through a 1-Gbps Ethernet, only two hops away from each other. […] Both machines run Ubuntu 18.04. We host an HTTP server using OpenLiteSpeed (v1.7.15) [25] built based on a mainstream QUIC library, LSQUIC [21]. […] We employ Linux tc [2] to control available network bandwidth when evaluating QUIC and HTTP/2 under low or changing bandwidth conditions.

p. 3, §3.2:
> On average, the throughput of cURL running QUIC and that of quic_client is 7-16% and 8-12% lower, respectively, compared to cURL with HTTP/2. […]
> We present in Figure 2 the distribution of the client's CPU usage during the download of a 1 GB file. The CPU usage for cURL when running QUIC is higher than that of cURL on HTTP/2. quic_client's CPU usage is further elevated, nearly maxing out at 100%, while its throughput remains similar to cURL on QUIC. […]
> We next limit the available network bandwidth from 50 Mbps to 1000 Mbps. As shown in Figure 3, when the available bandwidth is low, QUIC and HTTP/2 exhibit similar performance. […] The CPU usage for quic_client is always high and that of cURL QUIC hovers around 70%, reemphasizing the computational challenges associated with the protocol.

p. 3, Figure 3 caption:
> Figure 3: Throughput and CPU usage of cURL and quic_client during file download under limited bandwidth.

**Coverage.**
- **T3 — covers (partially).** Object: `cURL` downloading a 1 GB file over HTTP/2 (TCP+TLS) and HTTP/3 (QUIC) on a Linux desktop; unit: client CPU usage in % of one core (distribution in Fig. 2; text values: QUIC ~70 %, HTTP/2 "lower", exact HTTP/2 value only in the figure, which I do not quote) and throughput; scope: Core i7-6700 client, Ubuntu 18.04, 1 Gbps LAN with `tc`-shaped bandwidth 50–1000 Mbps; population: one testbed. This is the only Linux observation found of a stock command-line downloader's CPU share; note it is on a 1 Gbps LAN and the reported number is for QUIC, with HTTP/2 lower and not stated numerically in the text. Not covered: bytes per wake, receive-buffer sizes, disk-write work per chunk, wget/aria2c.
- T1, T2, T4, T6 — does not cover.

**Observation status.** One testbed, machine and OS named, cURL version not named in the passages read, window = one 1 GB download per condition.

---

### S1-22 — Visser & Fontugne, "Inside the Engine Room: Investigating Steam's Content Delivery Platform Infrastructure in the Era of 100GB Games" (PAM 2024)

**Citation.** Christoff Visser, Romain Fontugne (IIJ Research Lab), "Inside the Engine Room: Investigating Steam's Content Delivery Platform Infrastructure in the Era of 100GB Games", Passive and Active Measurement (PAM) 2024, Springer LNCS, DOI 10.1007/978-3-031-56249-5_2 (DOI per search-result metadata; the copy read is the authors' preprint).

**Copy read.** `https://www.iijlab.net/en/members/romain/pdf/chris_pam2024.pdf`, accessed 2026-09-17, `sources/S1-22/visser2024-steam-pam.pdf`, SHA-256 `31d4dc7b2bb8eec4fddc5ee9c16a76fee609dc574a245509b08cf0aa3149e10e` (810 242 bytes, 29 pages).

**Passages.**

p. 1, abstract:
> Players downloaded a monumental 44.7 exabytes from Steam in 2022 alone. With no signs of slowing down in 2023, Steam served an average of 15 Tbps of traffic between February and October, with peaks of up to 146 Tbps.

p. 7, §3.1 "Validation with Steam CLI":
> To confirm our findings, we set up five virtual machines (VMs) in the following cities, each of which had a cell_id: Chicago, São Paolo, Frankfurt, Tokyo, and Sydney. Using Steam's command line interface [67] we downloaded an instance of Counter Strike: Global Offensive (CS:GO) on each VM. During the download, Steam provided verbose logging for the CMs it connects to, as well as the cache servers it uses.

p. 8:
> Although we were only able to retrieve a maximum of 20 download sources via the web API, we found that the Steam client can reach up to 30 download sources. […]
> Figure 1 shows the Tokyo VM logs during a CS: GO download, highlighting increased traffic and load. […] The download speed correlates with the intended number of connections, which increased to five, although only four Steam caches were used without initiating the fifth. Once done, a summary provided detailed statistics for each connection, including bytes downloaded, time taken, speeds, and cache hits.
> Just 30 minutes after the initial download, Tokyo's Steam cache load had intensified. This time, the client connected to only two sources, a CDN endpoint from Akamai and a Steam Cache server in Hong Kong, compared to the previous five.

p. 7, Figure 1 (condensed download log; per-connection speeds as rendered in the extraction):
> (206.63 Mbps ). 19295 Hits / 538 […] (229.86 Mbps ). 12637 Hits / 4 Misses […] (750.42 Mbps ). 72373 Hits / 2129 […] (39.55 Mbps ). 2377 Hits / 9 Misses […] (718.19 Mbps ). 0 Hits / 0 Misses (0 %, 0 % bytes)
> Fig. 1: Condensed download logs for Steam Client in Tokyo as traffic and load increases.

Reference [67] in the copy's bibliography (p. 27): `…tware.com/wiki/SteamCMD#Linux, accessed: 2023-09-20` (the SteamCMD wiki, Linux section).

**Coverage.**
- **T3 — covers (partially).** Object: the Steam client (SteamCMD) downloading a depot (CS:GO) on cloud VMs; unit: number of download sources/connections (up to 30 sources listed; "intended number of connections" five in the log) and per-connection Mbps from the client's own summary (39.55–750.42 Mbps on a datacentre VM); scope: five VMs in five cities, 2023; population: one download per VM plus repeats under load. Not covered: CPU per chunk, wake structure, chunk sizes, the client's process names, consumer-link throughput (VM links are datacentre-class). VM OS is not stated in the passages; the SteamCMD reference points at its Linux section.
- T1, T2, T4, T6 — does not cover.

**Observation status.** One measurement campaign; machines are unnamed cloud VMs (locations named); subject SteamCMD, game named; window one download.

---

### S1-05 — Cha et al., "SplitScreen: Enabling Efficient, Distributed Malware Detection" (NSDI 2010)

**Citation.** Sang Kil Cha, Iulian Moraru, Jiyong Jang, John Truelove, David Brumley, David G. Andersen, "SplitScreen: Enabling Efficient, Distributed Malware Detection", USENIX NSDI 2010.

**Copy read.** `https://www.usenix.org/legacy/event/nsdi10/tech/full_papers/cha.pdf`, accessed 2026-09-17, `sources/S1-05/cha2010-splitscreen.pdf`, SHA-256 `99fb21d1688d4ddc2ba06746f98ed2056202a487aeed7c0f90f9c4aa7bf6cd59` (533 017 bytes, 14 pages).

**Passages.**

p. 8, §5.1 "Evaluation Setup":
> Unless otherwise specified, our experiments were conducted on an Intel 2.4 GHz Core 2 Quad with 4 GB of RAM and a 8 MB split L2 cache using a 12-byte window size (see §3). When comparing SplitScreen against ClamAV, we exclude data structure initialization time in ClamAV, but count the time for FFBF INIT in SplitScreen. […] Unless otherwise specified, we report the average over 10 runs.
> Scanned files. Unless otherwise specified, all measurements reflect scanning 344 MB of 100% clean files.

p. 9, §5.3 "Understanding throughput: Cache misses":
> We hypothesized that a primary bottleneck in ClamAV was L2 cache misses in regular expression matching. Figure 8 shows ClamAV's throughput and memory use as the number of regular expression signatures grows from zero to roughly 125,000, with no MD5 signatures. In contrast, increasing the number of MD5 signatures linearly increases the total memory required by ClamAV, but has almost no effect on its throughput. With no regexp signatures, ClamAV scanned nearly 50 MB/sec, regardless of the number of MD5 signatures.
> […] the number of regex signatures increases the number of cache misses, decreases throughput, and thus is the primary throughput bottleneck in ClamAV.

p. 10, §5.5:
> At 3 million signatures, ClamAV consumed over 500 MB of memory […] We compare SplitScreen and ClamAV using the current signature set on: a 2009 desktop computer (Intel 2.4 GHz Core 2 Quad, 4 GB RAM, 8 MB L2 cache); a 2008 Apple laptop (Intel 2.4 GHz Core 2 Duo, 2 GB RAM, 3 MB L2 cache); a 2005 desktop (Intel Pentium D 2.8 GHz, 4 GB RAM, 2 MB L2 Cache); and a Alix3c2 (AMD Geode 500 Mhz, 256 MB RAM, 128 KB L2 Cache) […] On the desktop systems and laptop, SplitScreen performs roughly 2x better than ClamAV. On the embedded system, SplitScreen performs 30% better than the baseline ClamAV.

p. 11, Figure 12 caption (y-axis "Throughput (MB/s)", ticks 0, 5, 10; bars per machine for ClamAV and SplitScreen):
> Figure 12: Performance for four different systems (differing CPU, cache, and memory size).

**Coverage.**
- **T4 — covers (partially).** Object: ClamAV signature scanning (modified `libclamav`; ClamAV version not named in the passages read); unit: MB/s of scanned clean files and MB of memory; statistic: ~50 MB/s with no regexp signatures; with the 2010 signature set the ClamAV bars in Fig. 12 lie on a 0–10 MB/s axis (value only in the figure; not quoted as a number); average of 10 runs; scope: 344 MB of clean files on a 2.4 GHz Core 2 Quad and three other machines; population: one lab. Operating system is not named in the passages I read. Not covered: whether `clamscan` throttles itself, threading, I/O pattern, CPU share over a scan (the scan is CPU-bound by construction: the bottleneck named is L2 cache misses).
- Other topics — does not cover.

**Observation status.** One lab, machines named, OS not named, subject "ClamAV" with the 2010 signature set, input 344 MB clean files, cache state not stated; window one scan, 10-run average.

---

### S1-29 — Erdogan & Cao, "Hash-AV: Fast Virus Signature Scanning by Cache-Resident Filters" — *context: ~20 years old*

**Citation.** Ozgun Erdogan, Pei Cao (Stanford), "Hash-AV: Fast Virus Signature Scanning by Cache-Resident Filters"; the copy is the Stanford preprint (its bibliography cites "http://crypto.stanford.edu/~cao/hash-av/, 2005" and the text says "As of July 2005"); published in Int. J. Security and Networks 2(1/2), 2007 per search-result metadata (not verified in the copy).

**Copy read.** `http://crypto.stanford.edu/~cao/hash-av.pdf`, accessed 2026-09-17, `sources/S1-29/erdogan-cao-hash-av.pdf`, SHA-256 `597b83818698d296e08f667104ec04432f2f8cdedb32db16ee47de1b09957147` (145 099 bytes, 9 pages).

**Passages.**

p. 1–2, §I:
> We have applied Hash-AV to Clam-AV [12], the most popular open source anti-virus software. Hash-AV improves Clam-AV's scanning throughput to 29.4 MB/s for executables, 16.6 MB/s for web pages, and 29.5 MB/s for random data, on an Athlon XP 2000+. This represents a speed-up factor of 1.7 to 4.4. […] Clam-AV with Hash-AV can scan executables at 85 MB/s, web pages at 91 MB/s, and random data at 120MB/s. Given that the memory copy speed is 260 MB/s on the Athlon XP 2000+, the results confirmed our intuition that virus scanning can potentially reach memory copy speeds.

p. 4, §III-C:
> Our experiments are run on an Athlon 64 3200+ PC, with 2.0 Ghz CPU, 128KB L1, and 512KB L2 cache. We have also repeated the experiments on an Athlon XP 2000+ and a Pentium-4 2.6Ghz PC, and found matching results.

p. 6, §V:
> In the experiments, three different types of inputs are used: the 120MB sample executable file as described in Section III-C, a file of 99 MB containing HTML data crawled from the web, and a 100 MB random file.

p. 7, §VI:
> We have implemented two approaches for on-access scanning of Hash-AV on Linux. The first approach uses Dazuko [8] to pass open/close/exec system calls to Hash-AV. The second approach implements a wrapper around the glibc read(), write(), send() and recv() code […]

*Reader's computation:* baseline ClamAV throughput implied by "29.4 MB/s … speed-up factor of 1.7 to 4.4" lies between 29.4/4.4 ≈ 6.7 MB/s and 29.4/1.7 ≈ 17 MB/s (executables, Athlon XP 2000+, 2005 signature set).

**Coverage.**
- **T4 — context.** Object: ClamAV plain-text/AC signature scanning of 100–120 MB single files; unit: MB/s; scope: Athlon 64 3200+ / Athlon XP 2000+ / P4 2.6 GHz, 2005 signature databases (30 K and 120 K signatures); the on-access mode is stated to be implemented on Linux. Twenty years old → context only. Not covered: throttling, threads, CPU share.
- Other topics — does not cover.

---

### S1-24 — Forain et al., "Endpoint Security in Networks: An OpenMP Approach for Increasing Malware Detection Speed" (Symmetry 2017) — *experiments on Windows: context*

**Citation.** Igor Forain, Robson de Oliveira Albuquerque, Ana Lucila Sandoval Orozco, Luis Javier García Villalba, Tai-Hoon Kim, "Endpoint Security in Networks: An OpenMP Approach for Increasing Malware Detection Speed", Symmetry 2017, 9(9), 172; doi:10.3390/sym9090172.

**Copy read.** `https://pdfs.semanticscholar.org/acd5/fb8955767547927ef6a01edce82cd0f33468.pdf` (MDPI's own PDF URL returned 403), accessed 2026-09-17, `sources/S1-24/mdpi-symmetry-2017-openmp-clamav.pdf`, SHA-256 `f6ae57e9794f6f4d36edbd47c4b7204ddd53cc856cf3f258f92c2fb139e77a2d` (362 413 bytes, 19 pages).

**Passages.**

p. 3, §2.2:
> The paper of Huang and Tsai [22] analyzed the 0.95.2 version performance of ClamAV during the inspection of a 600 MB file. They observed that, despite 80% of the malware signatures being hash codes, ClamAV uses 1% of the entire execution time during the match of this type of signature. Nevertheless, the search for signatures based on strings consumes at least 90% of that AV's processing time.

p. 3, §2.2:
> Through source code analysis of the 0.98.1 version of ClamAV, this work identified 14 modules inside the project of the engine. The two most important among these 14 modules are clamscan and libclamav. The first one (clamscan) is the entry point of the application, responsible for command […]

p. 6, §4:
> After profiling ClamAV, it is possible to describe the use of the program against n distinct files as the sequential execution of the same function scan( ) n times. […] Figure 2 also shows the existence of a single thread, named master thread, which is responsible for executing the entire program.
> Even if there is more than one file to be inspected by the AV engine, they are analyzed sequentially by the system.

p. 8, §5.1:
> For the evaluation of the proposed parallel version of ClamAV, this work uses two PCs. The first one with an Intel Core I5-3210m CPU with two hyper-threading (HT) processor cores, 2.5 GHz clock speed and 4 GB of DDR3 RAM. The second one with an Intel Core2 Duo T6660 CPU with two processor cores, 2.2 GHz clock speed and 4GB of DDR3 RAM. Both computers use Microsoft Windows version 2007 for the x84 64 bit architecture. All programs were implemented in C using OpenMP library 2.0 and compiled using Microsoft Visual Studio 2010.

p. 1, abstract:
> […] our work achieved an execution time around 62% lower than the original software version, reaching a speedup of 2.6 times faster.

**Coverage.**
- **T4 — covers the documentation/source question; measurements are context.** Threading: `clamscan` 0.98.1 scans files sequentially in a single master thread (their source analysis); string-signature matching ≥ 90 % of processing time (citing Huang & Tsai on 0.95.2). The speed-up measurements are on Windows → context. Not covered: I/O pattern, throttling, CPU share on Linux.
- Other topics — does not cover.

---

### S1-19 — Al-Saleh, "Antivirus Performance Characterization: System-Wide View" (UNM preprint; IET Information Security 2013) — *Windows 7: context*

**Citation.** Mohammed I. Al-Saleh, "Antivirus Performance Characterization: System-Wide View", University of New Mexico CS graduate student paper archive 2010–2011 (preprint); published version IET Information Security, DOI 10.1049/iet-ifs.2012.0192 (Wiley copy 403; not verified).

**Copy read.** `https://www.cs.unm.edu/~csgsa/archive/2010-2011/papers/MohammedAl-saleh.pdf`, accessed 2026-09-17, `sources/S1-19/alsaleh-av-systemwide.pdf`, SHA-256 `d0c3fd37cd9dca57c44444d18f932357f027a2998012eef64cb4053210215bee` (1 115 326 bytes, 9 pages).

**Passages (line fragments as extracted; contiguous lines joined).**

p. 2:
> the whole system; a Windows built-in technology, called Event Tracing for Windows (ETW). This technology is integrated with Microsoft Windows kernel to log events

p. 4 (fragment):
> iments on a machine that has Windows 7 OS, Intel Dual

**Coverage.** T4 — *context only*: an AV characterisation on Windows 7 using ETW/xperf; not Linux, no ClamAV. Other topics — does not cover. Recorded so the search direction "on-access/on-demand AV overhead studies" is accounted for.

---

### S1-03 — Boyd-Wickizer et al., "An Analysis of Linux Scalability to Many Cores" (OSDI 2010) — Psearchy/pedsort

**Citation.** Silas Boyd-Wickizer, Austin T. Clements, Yandong Mao, Aleksey Pesterev, M. Frans Kaashoek, Robert Morris, Nickolai Zeldovich, "An Analysis of Linux Scalability to Many Cores", USENIX OSDI 2010 (the MOSBENCH paper).

**Copy read.** `https://pdos.csail.mit.edu/papers/linux:osdi10.pdf`, accessed 2026-09-17, `sources/S1-03/boyd-wickizer2010-mosbench.pdf`, SHA-256 `f5a618044994b7dc0824064b918fc5a6502bbd44509520eb4a87744fbd69f4cc` (222 262 bytes, 16 pages).

**Passages.**

p. 4, §3.6 "File indexer":
> Psearchy is a parallel version of searchy [35, 48], a program to index and query Web pages. We focus on the indexing component of searchy because it is more system intensive. Our parallel version, pedsort, runs the searchy indexer on each core, sharing a work queue of input files. Each core operates in two phases. In phase 1, it pulls input files off the work queue, reading each file and recording the positions of each word in a per-core hash table. When the hash table reaches a fixed size limit, it sorts it alphabetically, flushes it to an intermediate index on disk, and continues processing input files. Phase 1 is both compute intensive (looking up words in the hash table and sorting it) and file-system intensive (reading input files and flushing the hash table). […] Unlike phase 1, phase 2 is mostly file-system intensive. While pedsort spends only 1.9% of its time in the kernel at one core, this grows to 23% at 48 cores, indicating scalability limitations.

p. 12, §5.7 "Psearchy/pedsort":
> Figure 10 shows the runtime for different versions of pedsort indexing the Linux 2.6.35-rc5 source tree, which consists of 368 Mbyte of text across 33,312 source files. The input files are in the buffer cache and the output files are written to tmpfs. Each core uses a 48 Mbyte word hash table and limits the size of each output index to 200,000 entries […]
> The initial version of pedsort used a single process with one thread per core. […] for 1 core the system time is 2.3 seconds, while at 48 cores the total system time is 41 seconds.
> […] pedsort reads input files using libc file streams, which access file contents via mmap […] We avoided this problem by modifying pedsort to use one process per core for concurrency […]

p. 3, §3:
> Because many applications are bottlenecked by disk writes, we used an in-memory tmpfs file system to explore non-disk limitations.

**Coverage.**
- **T2 — covers only the "first full index" case, which the topic excludes; recorded as the only indexer observation in the literature found.** Object: pedsort (Psearchy) batch-indexing 368 MB / 33 312 files from a warm buffer cache to tmpfs on Linux 2.6.35-rc5, 48-core machine; unit: kernel-time share (1.9 % at one core), system seconds (2.3 s at one core), CPU time per job (Fig. 10); structure: one process per core (after modification), two phases. Not covered: a daemon's steady-state wake cadence, inotify, scheduling class, Tracker/Baloo/plocate.
- T1, T3, T4, T6 — does not cover.

**Observation status.** One machine (48-core; model on p. 9 not quoted), kernel named, input named, cache warm, window one indexing run.

---

### S1-40 — Love, "Kernel Korner - Intro to inotify" (Linux Journal, 2005) — *context: 21 years old*

**Citation.** Robert Love, "Kernel Korner - Intro to inotify", Linux Journal, 2005-09-28, `https://www.linuxjournal.com/article/8478`.

**Copy read.** accessed 2026-09-17, `sources/S1-40/lj-8478-intro-to-inotify.html`, SHA-256 `6328a05c431330d6c7e6e70537bd2640115b8091c871cc65921d66f339e06213` (56 311 bytes).

**Passages.**

Section "What Is inotify?":
> inotify is a file change notification system—a kernel feature that allows applications to request the monitoring of a set of files against a list of events. When the event occurs, the application is notified. To be useful, such a feature must be simple to use, lightweight with little overhead and flexible.

Section "Conclusion":
> inotify is currently in use in various projects, including Beagle, an advanced desktop indexing system, and Gamin, a FAM replacement.

**Coverage.** T2 — *context*: names Beagle as an inotify-driven indexer in 2005; no measurement. Other topics — does not cover.

---

### S1-04 — Traeger, Zadok, Joukov, Wright, "A Nine Year Study of File System and Storage Benchmarking" (ACM TOS 2008)

**Citation.** Avishay Traeger, Erez Zadok, Nikolai Joukov, Charles P. Wright, "A Nine Year Study of File System and Storage Benchmarking", ACM Transactions on Storage 4(2), May 2008.

**Copy read.** `https://www.fsl.cs.sunysb.edu/docs/fsbench/fsbench.pdf`, accessed 2026-09-17, `sources/S1-04/traeger2008-fsbench.pdf`, SHA-256 `79ec01a29579d5c9413b3a1865d71180721d4dd7c338e32807fc8ccb91de3fe8` (559 001 bytes, 56 pages).

**Passages.**

p. 1, abstract:
> As a specific example, slowing down read operations on ext2 by a factor of 32 resulted in only a 2–5% wall-clock slowdown in a popular compile benchmark.

p. 6, §4 (cache state):
> It is not always clear whether benchmarks should be run with "warm" or "cold" caches. On one hand, real systems do not generally run with completely cold caches. On the other hand, a benchmark that accesses too much cached data may be unrealistic as well. […] If cold-cache results are desired, caches should be cleared before each run. This can be done by allocating and freeing large amounts of memory, remounting the file system, reloading the storage driver, or rebooting. We have found that rebooting is more effective than the other methods [Wright et al. 2005]. […] If, however, warm-cache results are desired, this can be achieved by running the experiment N+1 times, and discarding the first run's result.

p. 18, §7.2:
> The main problem with compile benchmarks is that because they are CPU intensive, they can hide the overheads in many file systems.

p. 40, §10 (utilities used as benchmarks):
> —cp [Zadok et al. 2001; Padioleau and Ridoux 2003; Schindler et al. 2002; Santry et al. 1999; Muniswamy-Reddy et al. 2004] sequentially reads from one file while copying to another.
> —diff [Schindler et al. 2002] sequentially reads two files and compares them.
> —tar [Lee et al. 1999; Anderson et al. 2000] and gzip [DeBergalis et al. 2003] sequentially read from a file and append to a set of files while consuming CPU.
> Using these utilities is slightly better than creating ad hoc benchmarks because the former are widely available and there is no misunderstanding about what the benchmark does. However, none of the papers specified what version the authors were using […]

**Coverage.**
- **T1 — covers method only.** How the file-system-benchmarking literature characterises `cp`/`tar`/`gzip` (sequential read + append, "consuming CPU" for tar/gzip), the warm/cold cache procedure (drop by reboot/remount; warm = N+1 runs, discard first), and that CPU-intensive workloads hide I/O overheads (32× slower reads → 2–5 % wall). No CPU-share, run/wait or thread figures for any copy/archive program.
- T2, T3, T4, T6 — does not cover.

**Observation status.** Survey plus the authors' own Slowfs experiment (Linux, ext2; machine on p. 14 not quoted); not a background-job observation.

---

### S1-06 — Tridgell, "Efficient Algorithms for Sorting and Synchronization" (PhD thesis, ANU, 1999) — *context: 27 years old*

**Citation.** Andrew Tridgell, "Efficient Algorithms for Sorting and Synchronization", PhD thesis, The Australian National University, February 1999.

**Copy read.** `https://www.samba.org/~tridge/phd_thesis.pdf`, accessed 2026-09-17, `sources/S1-06/tridgell1999-thesis.pdf`, SHA-256 `d2032e6d13f4d79bf6e845dacfd16fb91056b1908073fe4fac9ed7785a22ef0c` (415 309 bytes, 115 PDF pages).

**Passage.** PDF p. 89 (printed p. 80), §4.5 "Multiple files and pipelining":
> The pipelining method used by rsync is shown in Figure 4.1. The process is broken into three pieces – the generator, the sender and the receiver. The generator runs on B and generates the signatures for all files that are to be transferred, sending the signatures to the sender. The sender (running on A) matches the signatures from B against the new files and sends a stream of block tokens and literal bytes to the receiver. The receiver (running on B) reconstructs the files.
> The link from the receiver to the generator (shown as a dashed line in the diagram) is for a small message to indicate if a file has not been successfully received (which is detected when the strong signature of the reconstructed file is not correct). In that case the generator starts again, but with a larger per-block strong signature.

**Coverage.** T1 — *context* (the three-piece generator/sender/receiver structure as designed in 1999; no CPU or run/wait figures; no statement that the pieces are separate processes in the thesis text quoted — the process realisation is S1-25's `atop` observation). Other topics — does not cover.

---

### S1-38 — Milenkovic, Dzhagaryan, Burtscher, "Performance and Energy Consumption of Lossless Compression/Decompression Utilities on Mobile Computing Platforms" (MASCOTS 2013)

**Citation.** Aleksandar Milenkovic, Armen Dzhagaryan (Univ. of Alabama in Huntsville), Martin Burtscher (Texas State), "Performance and Energy Consumption of Lossless Compression/Decompression Utilities on Mobile Computing Platforms", 2013 IEEE 21st Int. Symp. on Modelling, Analysis & Simulation of Computer and Telecommunication Systems (MASCOTS), DOI 10.1109/MASCOTS.2013.33.

**Copy read.** `http://www.ece.uah.edu/~milenka/docs/aadam_mascots13.pdf`, accessed 2026-09-17, `sources/S1-38/aadam2013-mascots-compression.pdf`, SHA-256 `98b3894211baaac8c14d997bdab0d5c012ff20082bb21764ccf9390be6683d81` (529 013 bytes, 10 pages).

**Passages.**

p. 3, §III.A "Platforms":
> The OMAP4430 SoC includes a dual-core ARM Cortex-A9 MPCore processor […] In our experiments, we use an Ubuntu distribution provided by Linaro […] [Raspberry Pi] features a Broadcom BCM2835 SoC, which contains an ARM1176JZFS running at 700 MHz, a Videocore 4 GPU, and 512 MB of RAM. […] We use Raspbian, a Debian Linux distribution optimized for Raspberry Pi.

p. 3, §III.B "Datasets":
> The files are merged into a single archive file (tar) that is used as an input for the compression utilities.

p. 6, §V:
> For all compression utilities, the higher compression levels result in lower throughput because of the increased computational complexity. The throughput drop may exceed an order of magnitude, e.g., for lzop. By far the highest compression throughput is achieved by lzop -1 to -6, ~26 MB/s on Pandaboard and 9.5 MB/s on Raspberry Pi. The second highest compression throughput is achieved by pigz -1, 13.2 MB/s on Pandaboard and 2.7 MB/s on Raspberry Pi. pigz fully utilizes two processor cores on Pandaboard to almost double the compression throughput relative to gzip (~7.4 MB/s with -1). […] xz and bzip2 achieve significantly lower compression throughputs (e.g., from 1.6 to 1.1 MB/s for bzip2, and from 2.2 to 0.3 MB/s for xz on Pandaboard).
> […] The highest decompression throughput is achieved by lzop (of 71.9 MB/s on Pandaboard, 26.5 MB/s on Raspberry Pi), followed by pigz and gzip. xz, bzip2, and pbzip2 achieve significantly lower decompression throughputs (below ~10.8 MB/s on Pandaboard and below 4.7 MB/s on Raspberry Pi). […] Although decompression itself in pigz is not parallelized (it is single threaded), three other threads are created for reading, writing, and checking calculations that speed up decompression [13].

**Coverage.**
- **T1 — covers (partially).** Object: `xz`, `gzip`, `bzip2`, `lzop`, `pigz`, `pbzip2` compressing one tar archive on Linux (Ubuntu/Linaro on a dual-core Cortex-A9 at 1 GHz; Raspbian on a 700 MHz ARM11); unit: MB/s of input per compression level; statistic: xz 2.2 → 0.3 MB/s (levels -1…-6 on Pandaboard), gzip -1 ~7.4 MB/s, pigz uses both cores; thread structure of pigz decompression (one decompressor thread plus three helper threads, citing pigz docs). Not covered: CPU share of wall time (the loads are CPU-bound by construction on tmp/SD storage), run/wait, `zstd`, `7z`, `tar` itself, page-cache state.
- Other topics — does not cover.

**Observation status.** One lab, two named boards, named distributions, one tar input of named file mix (Table 2, not quoted), window one run per level. Linux, 2013, mobile-class hardware: recorded as a Linux observation with the hardware caveat.

---

### S1-08 — Meyer & Bolosky, "A Study of Practical Deduplication" (FAST 2011) — *Windows: context*

**Citation.** Dutch T. Meyer, William J. Bolosky, "A Study of Practical Deduplication", USENIX FAST 2011.

**Copy read.** `https://www.usenix.org/legacy/event/fast11/tech/full_papers/Meyer.pdf`, accessed 2026-09-17, `sources/S1-08/meyer2011-dedup.pdf`, SHA-256 `9c91ba8b42d7a42d39fb78eb4a79cc7b51bfc8e9249558b5db09476609a371c5` (709 718 bytes, 13 pages).

**Passage.** p. 1, §1:
> In order to evaluate the tradeoff in space savings between whole-file and block-based deduplication, we conducted a large-scale study of file system contents on desktop Windows machines at Microsoft. Our study consists of 857 file systems spanning 162 terabytes of disk over 4 weeks.

**Coverage.** T1 — *context only*: a Windows file-content study of deduplication ratios; no backup-process CPU or I/O behaviour. Other topics — does not cover.

---

### S1-15 — Wallace et al., "Characteristics of Backup Workloads in Production Systems" (FAST 2012) — *appliance-side: context*

**Citation.** Grant Wallace, Fred Douglis, Hangwei Qian, Philip Shilane, Stephen Smaldone, Mark Chamness, Windsor Hsu (EMC Backup Recovery Systems Division), "Characteristics of Backup Workloads in Production Systems", USENIX FAST 2012.

**Copy read.** `https://www.usenix.org/system/files/conference/fast12/wallace2-9-12.pdf`, accessed 2026-09-17, `sources/S1-15/wallace2012-backup-workloads.pdf`, SHA-256 `436619c8df7504a782b47a06787877e08e76baa35e5c1c57d0c5771ce0e1e797` (228 990 bytes, 16 pages).

**Passages.** p. 1, abstract:
> In this paper, we present a comprehensive characterization of backup workloads by analyzing statistics and content metadata collected from a large set of EMC Data Domain backup systems in production use. This analysis is both broad (encompassing statistics from over 10,000 systems) and deep (using detailed metadata traces from several production systems storing almost 700TB of backup data).

p. 3, §3.1:
> The Data Domain systems that are the subject of this study send system data back to EMC periodically, usually on a daily basis.

**Coverage.** T1 — *context only*: characterises the storage-appliance side of enterprise backup (dedup ratios, churn), not a desktop backup client's CPU/I/O. Other topics — does not cover.

---

### S1-07 — Corbet, "Toward less-annoying background writeback" (LWN, 2016)

**Citation.** Jonathan Corbet, "Toward less-annoying background writeback", LWN.net, 2016-04-13, `https://lwn.net/Articles/682582/`.

**Copy read.** accessed 2026-09-17, `sources/S1-07/lwn-682582.html`, SHA-256 `d84f38553f1f44a1515ff09dfdca2b73a4687d973af3816c096614670c853aa5` (67 283 bytes; article plus reader comments).

**Passages.**

Article, paragraph 1:
> It's an experience many of us have had: write a bunch of data to a relatively slow block device, then try to get some other work done. In many cases, the system will slow to a crawl or even appear to freeze for a while; things do not recover until the bulk of the data has been written to the device. On a system with a lot of memory and a slow I/O device, getting things back to a workable state can take a long time, sometimes measured in minutes.

Article, paragraphs 3–5:
> Jens's diagnosis is that it has to do with the queuing of I/O requests in the block layer. […] The problem is that, if there is a lot of dirty data to write, there may end up being vast numbers (as in thousands) of requests queued for the device. Even a reasonably fast drive can take some time to work through that many requests. If some other activity (clicking a link in a web browser, say, or launching an application) generates I/O requests on the same block device, those requests go to the back of that long queue and may not be serviced for some time. If multiple, synchronous requests are generated — page faults from a newly launched application, for example — each of those requests may, in turn, have to pass through this long queue. That is the point where things appear to just stop.
> In other words, the block layer has a bufferbloat problem that mirrors the issues that have been seen in the networking stack.

Article, "Taming the queues", paragraph 2:
> Jens's patch set aims to reduce the amount of data "in flight" through all of those queues by throttling requests when they are first submitted. To put it simply, each device has a maximum number of buffered-write requests that can be outstanding at any given time. If an incoming request would cause that limit to be exceeded, the process submitting the request will block until the length of the queue drops below the limit.

Reader comment (in the same copy; comment thread, poster "axboe"):
> Network scheduling has the luxury of being able to drop packets, that's not something I can do. At least not without corrupting data. So backing off is the best solution we have.

Reader comment (same copy; poster "ksandstr", 2016-04-17, quoted for the observation it reports):
> […] when copying data from a fast device to a slow one, the kernel accumulates a fantastic amount of writeback before ever starting to write to the target device. This results in device bandwidth that's going unused, leading to (say) a write-limited 5GB copy to a 50MB/s device taking not just the requisite 100s but also what's possibly tens of seconds until the kernel finally deigns to chooch along […] And so the impatient console user's terminals fail to refresh and eventually the entire X session jams up -- all because of a copy to an USB2 storage device, or SD card.

**Coverage.**
- **T6 — covers ("what such a load does to interactivity and why").** Object: a large buffered write to a slow block device on Linux; mechanism: thousands of queued writeback requests ahead of the interactive task's synchronous reads/page faults (block-layer "bufferbloat"); remedy: writeback throttling (`wbt`, 2016). No measured CPU/run/wait figures; the comment's "5GB copy to a 50MB/s device … 100s" is a user's arithmetic, not a measurement.
- T1 — does not cover the copy program itself.
- T2, T3, T4 — does not cover.

**Observation status.** Not a measurement; editorial explanation of an LKML patch set plus user reports. Linux.

---

### S1-17 — LWN reader comment thread "stalls caused by USB drive copy" (2013) — *user reports: context*

**Citation.** Comment thread under the LWN article "Per-entity load tracking", comments dated 2013-01-12 to 2017-03-17, `https://lwn.net/Articles/532455/`.

**Copy read.** accessed 2026-09-17, `sources/S1-17/lwn-532455.html`, SHA-256 `109717a60ebc7e951734fe8c2cc30523fc865cdf0ea8cdbf53965271ec0c7753` (11 854 bytes).

**Passages.**

Comment by "nix", 2013-01-12:
> It's got nothing to do with the CPU. This is a longstanding problem whereby with a sufficiently large copy, cp fills memory up with dirty pages awaiting writeout and then everything freezes solid because until the writeout to the slow block device has finished, there's hardly any memory left to do anything.

Comment by "nybble41", 2013-01-13:
> vm.dirty_bytes = 201326592
> This limits total dirty memory to 192MB before the kernel forces processes to work on writing data to disk rather than dirtying new pages. The default is something like 10% of total RAM. It seems to help.

Comment by "hummassa", 2013-01-13:
> For information, I can trigger this bug by copying anything (it does not seem to be necessary to be a single file, but a single file happens to trigger it more aggressively apparently) above 1/2 GiB via USB. Trying to backup my VMs (20G each file) to a USB drive is a nightmare. Usually I do "nice -20 cp" or, more commonly, "kde-cp".

Comment by "serzan", 2013-04-11:
> have you tried ionice -c 3? though not sure it'd have much of an impact, if thrashing memory is the cause

**Coverage.** T6 — *context*: Linux users' descriptions of `cp`-to-USB stalls (dirty-page accumulation, `vm.dirty_bytes`, `nice`/`ionice` as user remedies); no measurement. Other topics — does not cover.

---

### S1-18 — Wu Fengguang, "Re: Bug 12309 - Large I/O operations result in poor interactive performance and high iowait times" (LKML, 2010)

**Citation.** Wu Fengguang, LKML message "Re: Bug 12309 - Large I/O operations result in poor interactive performance and high iowait times", Mon Aug 02 2010 04:13:13 EST, via the lkml.iu.edu hypermail archive.

**Copy read.** `https://lkml.iu.edu/hypermail/linux/kernel/1008.0/00361.html`, accessed 2026-09-17, `sources/S1-18/lkml-bug12309-1008.0-00361.html`, SHA-256 `4d16a1ce35338960a2398b3c3c5b9050b78e545c046c70162655d8e7cacac8da` (30 429 bytes).

**Passages.**

Quoted bug-tracker comments carried in the mail (comments #460, #461 of kernel bug 12309, as quoted by Wu):
> I've tried stress also. I have 2 Gb og memory and 1.5 Gb swap. With swap activated stress -d 1 hangs my machine. Same does stress -d while swapiness set to 0. Widh swap deactivated things runs pretty fine.
> I can also confirm this. Disabling swap with swapoff -a solves the problem. I have 8gb of ram and 8gb of swap with a fake raid mirror. Before this I couldn't do backups without the whole system grinding to a halt. Right now I am doing a backup from the drives, watching a movie from the same drives and more. No more iowait times and programs freezing as they are starved from being able to access the drives.

Wu's own text:
> So swapping is another major cause of responsiveness lags.
> I just tested the heavy swapping case with the patches to remove the congestion_wait() and wait_on_page_writeback() stalls on high order allocations. The patches work as expected. […]
> The test case is basically
> usemem -n $nr_cpu --random $((2 * mem / nr_cpu)) --repeat 1000&
> cp /dev/zero /mnt/tmp/
> which creates 8 usemem processes randomly doing page faults on a dataset that is 2 times the physical memory size and one cp writing to a local file. The usemem processes are mostly waiting in lock_page() for the completion of swap-in IO, which is expected.

**Coverage.** T6 — covers how a kernel developer set up a "large I/O + memory pressure" load in 2010 (`cp /dev/zero` to a file next to 8 page-faulting `usemem` processes) and the user-reported mechanism (swap + writeback congestion stalls); no CPU or throughput figures. Other topics — does not cover. Linux, 2010; developer's test, machine not named in the quoted part.

---

### S1-13 — Torrey, Coleman, Miller, "A comparison of interactivity in the Linux 2.6 scheduler and an MLFQ scheduler" (SPE 2007) — *2006 observation on Linux 2.6.3: at the two-decade boundary, marked context*

**Citation.** Lisa A. Torrey, Joyce Coleman, Barton P. Miller, "A comparison of interactivity in the Linux 2.6 scheduler and an MLFQ scheduler", Software: Practice and Experience 37:347–364 (2007), published online 24 October 2006, DOI 10.1002/spe.772.

**Copy read.** `https://ftp.cs.wisc.edu/pub/paradyn/papers/LinuxSched-SPE2007.pdf`, accessed 2026-09-17, `sources/S1-13/torrey2007-spe.pdf`, SHA-256 `9f1a26a433dcd36dd9f4fd1605ef9b733a1e17e495aa0ef026fbca56a844c49b` (194 230 bytes, 18 pages).

**Passages.**

p. 4:
> Another case involves tasks that block for disk I/O, which would gain large dynamic bonuses under the general policy, but are not usually interactive with the user. The sleep average of such a task is set at a threshold: high enough to classify as interactive, but low enough to lose interactive status quickly if the task starts to use up its time slices.

p. 7 (experiments):
> The second test […] We used compilations of the Linux 2.6 kernel, which perform some CPU-intensive work and also some disk I/O. Again, we were interested in the response times of the bash shell. In fact, we suspected that the Linux 2.6 scheduler might give the user-interactive task better response times than MLFQ because it lowers the priority of tasks that perform disk I/O.
> […] The hardware that we used to perform the tests contained a 425 MHz Pentium III processor with 128 MB of memory. We used a Gentoo Linux distribution with the 2.6.3 kernel.

p. 9, Table III "Shell response times with a compilation workload without daemon activity" (columns: 1 compile task, 2 compile tasks):
> Average response time (Linux 2.6) 5695 µs 6462 µs
> Average response time (MLFQ) 1670 µs 1268 µs
> Minimum response time (Linux 2.6) 3.9 µs 3.9 µs
> Maximum response time (Linux 2.6) 20 610 µs 28 890 µs
> Maximum response time (MLFQ) 9414 µs 10 000 µs
> Compile task interference frequency (Linux 2.6) 0.5% 0.7%
> Compile task interference frequency (MLFQ) 1.5% 2.4%
> Data points collected (Linux 2.6) 6502 7478

p. 9–10:
> Sometimes compile tasks shared the priority level of the interactive task, running while the interactive task waited on the run queue, and then the response time of the interactive task increased by several orders of magnitude. However, these times are all still too small to be noticeable to the user.
> So the Linux 2.6 scheduler appears to keep compile tasks from competing with the maximally interactive shell more often, because it directly limits the interactivity of tasks that perform disk I/O, but when it fails to do so these tasks run for relatively long periods.

**Coverage.** T6 — covers how a scheduler paper used a disk-I/O-bearing background (kernel compile) next to an interactive shell and what it measured (run-queue-to-run latency in µs from `rdtsc` in `try_to_wake_up`/`schedule`, thousands of samples; Linux 2.6.3 O(1) scheduler's disk-I/O sleep-average special case). Twenty years old and pre-CFS: marked *context*. Other topics — does not cover. Machine, kernel and window (minutes of key-repeat) named.

---

### S1-35 — Yang, Liu, Berger, Kaplan, Moss, "Redline: First Class Support for Interactivity in Commodity Operating Systems" (2008)

**Citation.** Ting Yang, Tongping Liu, Emery D. Berger, Scott F. Kaplan, J. Eliot B. Moss (UMass Amherst / Amherst College), "Redline: First Class Support for Interactivity in Commodity Operating Systems"; USENIX OSDI 2008 per search-result metadata (the copy's front matter does not name the venue).

**Copy read.** `https://people.cs.umass.edu/~emery/pubs/redline.pdf`, accessed 2026-09-17, `sources/S1-35/yang2008-redline.pdf`, SHA-256 `4da807ae005daf48034138e547b225279910b7018c3f7d4b9c3b831f9d1bd390` (292 187 bytes, 14 pages).

**Passages.**

p. 2, §1:
> As an example, Figure 1 shows the frame rate of mplayer, a movie player, while a Linux kernel compilation, invoked using make -j32, is performed using both a standard Linux 2.6.x kernel and our Redline kernel. For the standard kernel, the compilation substantially degrades the interactivity of the movie player, rendering the video unwatchable. Worse, the entire GUI becomes unresponsive. Similar behavior occurs on Windows when watching a video using the Windows Media Player while running a virus scan in the background.

p. 9, §8 "Platform":
> We perform all measurements on a system with a 3 GHz Pentium 4 CPU, 1 GB of RAM, a 40GB FUJITSU 5400RPM ATA disk, and an Intel 82865G integrated graphics card. […] We use a Linux kernel (version 2.6.22.5) patched with the CFS scheduler (version 20.3) as our control.

p. 10, §8 (disk I/O experiments):
> Writing: To test disk writing operations, we launch two background tasks meant to interfere with responsiveness. Specifically, each task repeatedly writes to an existing, 200 MB file using buffered writes. We then use vim, modified to report the time required to execute its write command, to perform sporadic write requests of a 30 KB file. It is set to the highest priority (-20) under Linux […]
> For Linux, each transaction in the journaling file system is heavily loaded with dirty pages from the background tasks. Thus, the calls to fsync() performed by vim causes it to block for a mean of 28 seconds. Under Redline, the reduced dirty threshold for best-effort tasks forces the system to flush the dirtied pages of the background task more frequently. When vim calls fsync(), the transaction committed by the journaling file system takes much less time because it is much smaller, requiring a mean of only 2.5 seconds.
> Reading: We play a movie using mplayer in the foreground while nine background tasks consume all of the disk bandwidth. Each background task reads 100 MB from disk in 20 MB chunks using direct I/O (bypassing the file system cache to achieve steady I/O streams). Figure 10 shows the number frame rate of mplayer over time for both Linux and Redline. Under Linux, mplayer blocks frequently because of the pending I/O requests of the background tasks, thus making the frame rate severely degraded and erratic.

p. 10, Figure 10 title and caption:
> Impact of large disk reads on mplayer
> Figure 10: The impact of massive reads on mplayer.

(Reader's note, not a quote: the figure's two series are labelled "Linux CFQ" and "Redline"; y-axis "Frames per Second (fps)", x-axis "Elapsed Time (Seconds)" running to 160.)

**Coverage.**
- **T6 — covers.** Object: background disk loads as set up in a scheduler/OS-interactivity paper on Linux 2.6.22.5 + CFS 20.3: (a) two writers repeatedly rewriting a 200 MB file with buffered writes, (b) nine readers each reading 100 MB in 20 MB direct-I/O chunks; effect on interactive work: `vim` `fsync()` of a 30 KB file blocks a mean 28 s (journal transaction loaded with the background's dirty pages) vs 2.5 s with Redline's reduced dirty threshold; `mplayer` frame rate "severely degraded and erratic" under Linux CFQ (values only in Fig. 10). Mechanism named: dirty pages in the journaling transaction; pending I/O requests of background tasks. No CPU-share figures for the background loads.
- T1 — does not cover (synthetic loads, not `cp`/`rsync`).
- T2, T3, T4 — does not cover.

**Observation status.** One machine (named), kernel named, loads named, window: per-experiment tens to 160 s (Fig. 10 axis). Linux, 2008 (18 years): a Linux observation on dated hardware and the CFQ I/O scheduler.

---

### S1-26 — Kolivas, "MuQSS - The Multiple Queue Skiplist Scheduler" (sched-MuQSS.txt)

**Citation.** Con Kolivas, `sched-MuQSS.txt`, kernel documentation shipped with the MuQSS patch set, `http://ck.kolivas.org/patches/muqss/sched-MuQSS.txt` (undated file; MuQSS era 2016–2020).

**Copy read.** accessed 2026-09-17, `sources/S1-26/sched-MuQSS.txt`, SHA-256 `e2419d95b46055094918f193ee0edc978dba2d730e3474204905ffb7250c7517` (18 637 bytes).

**Passages.**

lines 13–17:
> The main focus of MuQSS is to achieve excellent desktop interactivity and responsiveness without heuristics and tuning knobs that are difficult to understand, impossible to model and predict the effect of, and when tuned to one workload cause massive detriment to another, while still being scalable to many CPUs and processes.

lines 161–171, "Latency.":
> Through the use of virtual deadlines to govern the scheduling order of normal tasks, queue-to-activation latency per runqueue is guaranteed to be bound by the rr_interval tunable which is set to 6ms by default. This means that the longest a CPU bound task will wait for more CPU is proportional to the number of running tasks and in the common case of 0-2 running tasks per CPU, will be under the 7ms threshold for human perception of jitter. Additionally, as newly woken tasks will have an early deadline from their previous runtime, the very tasks that are usually latency sensitive will have the shortest interval for activation, usually preempting any existing CPU bound tasks.

lines 291–299, "Idleprio scheduling:":
> Idleprio scheduling is a scheduling policy designed to give out CPU to a task _only_ when the CPU would be otherwise idle. The idea behind this is to allow ultra low priority tasks to be run in the background that have virtually no effect on the foreground tasks. This is ideally suited to distributed computing clients (like setiathome, folding, mprime etc) but can also be used to start a video encode or so on without any slowdown of other tasks. To avoid this policy from grabbing shared resources and holding them indefinitely, if it detects a state where the task is waiting on I/O, the machine is about to suspend to ram and so on, it will transiently schedule them as SCHED_NORMAL.

**Coverage.** T6 — covers the Kolivas-era design statements: 6 ms `rr_interval` bound, the 7 ms jitter threshold, newly woken tasks get early deadlines, and that an I/O-waiting SCHED_IDLEPRIO background task is transiently promoted to SCHED_NORMAL so it does not hold shared resources. No measured figures. Other topics — does not cover.

---

### S1-27 — Kolivas, "FAQS about BFS. v0.330" (bfs-faq.txt) — *design statement, no data*

**Citation.** Con Kolivas, `bfs-faq.txt` v0.330 and `bfs-configuration-faq.txt`, `http://ck.kolivas.org/patches/bfs/`.

**Copies read.** accessed 2026-09-17: `sources/S1-27/bfs-faq.txt` SHA-256 `ecfc47b086dd3e420fa042aa64c903c9a1dda2d2cf6f6449a27a6e1dff5f5869` (13 895 bytes); `sources/S1-27/bfs-configuration-faq.txt` SHA-256 `2528e97bc64d4b0eda842a85355c7539a304c314d72d7d98567252a0ddbdacf2` (577 bytes).

**Passage.** bfs-faq.txt lines 9–27:
> Random stalls in mouse movements, keypresses, strange cpu distribution in various workloads and unpredictable behaviour all around were exactly what I was hoping had gone away. […] It varies timeslice length to try and preserve some deadline list and it determines cpu distribution based on a run/sleep relationship. […] The whole sleep calculation thing is exactly what I found was responsible for making varied behaviour under different loads and relative starvation and unfairness.

**Coverage.** T6 — context only (motivation against sleep-based interactivity heuristics; no background-I/O data). Other topics — does not cover.

---

### S1-10 — Corbet, "An EEVDF CPU scheduler for Linux" (LWN, 2023)

**Citation.** Jonathan Corbet, "An EEVDF CPU scheduler for Linux", LWN.net, 2023-03-09, `https://lwn.net/Articles/925371/`.

**Copy read.** accessed 2026-09-17, `sources/S1-10/lwn-925371.html`, SHA-256 `f24849da9c03a1fe76e6ee6f88b3ddad0dcdec08ec1085dd4c866ed924c0768e` (47 436 bytes).

**Passages.**

Section "Addressing the latency problem":
> When the scheduler is calculating the time slice for each process, it factors in that process's assigned latency-nice value; a process with a lower latency-nice setting (and, thus, tighter latency requirements) will get a shorter time slice. […] Latency-sensitive processes, which normally don't need large amounts of CPU time, will be able to respond quickly to events, while processes without latency requirements will be given longer time slices, which can help to improve throughput. No tricky scheduler heuristics are needed to get this result.

Same section, Zijlstra quoted:
> Some of the results, he said, "seem to indicate EEVDF schedules a lot more consistently than CFS and has a bunch of latency wins".

**Coverage.** T6 — covers the EEVDF design position on latency-sensitive vs throughput tasks (time-slice length, no sleep heuristics); no I/O-bound-task figure. Other topics — does not cover.

---

### S1-11 — Corbet, "Completing the EEVDF scheduler" (LWN, 2024)

**Citation.** Jonathan Corbet, "Completing the EEVDF scheduler", LWN.net, 2024-04-11, `https://lwn.net/Articles/969062/`.

**Copy read.** accessed 2026-09-17, `sources/S1-11/lwn-969062.html`, SHA-256 `246ee9fb66ffa55c62cf90cba9768ea1bfb575e93f11f026a4e7278ecc6b777a` (35 571 bytes).

**Passages.**

Section "A quick EEVDF review":
> A task is deemed "eligible" if its lag value is zero or greater; whenever the CPU scheduler must pick a task to run, it chooses from the set of eligible tasks. For each of those tasks, a virtual deadline is computed by adding the time remaining in its time slice to the time it became eligible. The task with the earliest virtual deadline will be the one that is chosen to run. Since a longer time slice will lead to a later virtual deadline, tasks with shorter time slices (which are often latency sensitive) will tend to run first.

Section "Lag and sleeping":
> The scheduler does, however, retain a task's current lag value when it goes to sleep, and starts from that value when the task wakes. So, if a task had run beyond its allocation before it sleeps, it will pay the penalty for that later, when it wakes.
> […] With the new patch, instead, an ineligible process that goes to sleep will be left on the queue, but marked for "deferred dequeue". Since it is ineligible, it will not be chosen to execute, but its lag will increase according to the virtual run time that passes. Once the lag goes positive, the scheduler will notice the task and remove it from the run queue.
> The result of this implementation is that a task that sleeps briefly will not be able to escape a negative lag value, but long-sleeping tasks will eventually have their lag debt forgiven.

Section "Time-slice control":
> If a latency-sensitive task with a short time slice wakes up, it may still have to wait for the current task to exhaust its time slice (which might be long) before being able to run. Zijlstra's patch series changes that, though, by allowing one task to preempt another if its virtual deadline is earlier.

**Coverage.** T6 — covers the EEVDF/CFS discussion of how a task that sleeps (an I/O-bound task blocks between bursts) is placed on wakeup: lag retained across sleep, deferred dequeue, wakeup preemption by earlier virtual deadline, `sched_runtime` slice request. No measured figures. Other topics — does not cover.

---

### S1-31 — Nayak replying to Huschle, "[RFC] sched/eevdf: sched feature to dismiss lag on wakeup" (linuxppc-dev mirror, 2024)

**Citation.** K Prateek Nayak (AMD), reply of Thu Feb 29 2024 14:36:16 AEDT quoting Tobias Huschle (IBM), "[RFC] sched/eevdf: sched feature to dismiss lag on wakeup" (2024-02-28), as archived at lists.ozlabs.org (linuxppc-dev). lore.kernel.org was unreachable (search log #24).

**Copy read.** `https://lists.ozlabs.org/pipermail/linuxppc-dev/2024-February/268909.html`, accessed 2026-09-17, `sources/S1-31/huschle-2024-eevdf-lag-wakeup.html`, SHA-256 `1a77a46714381fa22b4647533b9792f717303beb3879de0e5bc3b3d8eff57385` (8 028 bytes).

**Passages (Huschle's text as quoted in the reply).**
> The previously used CFS scheduler gave tasks that were woken up an enhanced chance to see runtime immediately by deducting a certain value from its vruntime on runqueue placement during wakeup.
> This property was used by some, at least vhost, to ensure, that certain kworkers are scheduled immediately after being woken up. The EEVDF scheduler, does not support this so far. Instead, if such a woken up entitiy carries a negative lag from its previous execution, it will have to wait for the current time slice to finish, which affects the performance of the process expecting the immediate execution negatively.
> […] 1. The kworker getting its negative lag occurs in the following scenario
> - kworker and a cgroup are supposed to execute on the same CPU
> - one task within the cgroup is executing and wakes up the kworker
> - kworker with 0 lag, gets picked immediately and finishes its execution within ~5000ns
> - on dequeue, kworker gets assigned a negative lag

**Coverage.** T6 — covers an LKML discussion of EEVDF wakeup placement for a short-running I/O helper (a vhost kworker, ~5000 ns per run) — server/virtualisation context, not desktop; one quantitative fact (≈5 µs run per wake) from a developer's description, machine not named. Other topics — does not cover.

---

### S1-36 — Min, "Using sched_ext to improve frame rates on the SteamDeck — Ideas behind the LAVD scheduler" (LPC 2024 slides)

**Citation.** Changwoo Min (Igalia), "Using sched_ext to improve frame rates on the SteamDeck: Ideas behind the LAVD scheduler", Linux Plumbers Conference 2024 sched_ext microconference, September 18, 2024, slides.

**Copy read.** `https://lpc.events/event/18/contributions/1713/attachments/1425/3058/scx_lavd-lpc-mc-24.pdf`, accessed 2026-09-17, `sources/S1-36/scx_lavd-lpc-mc-24.pdf`, SHA-256 `77c9cefec98e0346d5b89a219ca30eff7cb4f448016b24fa0871b286ba421eb4` (854 241 bytes, 20 slides).

**Passages.**

Slide 15 "Usages can be captured by CPU utilization":
> Light load (around 10%) — Usage: code editing + reading a PDF + music/video streaming
> Medium load (<70%) — Usage: running a casual game, a kernel module compilation
> Heavy load (>70%) — Usage: running a AAA game, full kernel compilation

Slide 17 "Performance Comparison with EEVDF":
> FH5 in-game benchmark with background recording on SteamDeck OLED
> LAVD 1419.49 J (15.4 W) — EEVDF 1423.75 J (15.5 W)

Slide 18:
> Tomb Raider in-game benchmark without background task on SteamDeck OLED
> LAVD 752.83 J (10.7 W) — EEVDF 896.07 J (12.7 W)

**Coverage.** T6 — covers how a shipped sched_ext scheduler's author frames background load: as system CPU-utilisation bands (10 % / <70 % / >70 %) and, in the benchmark, "background recording" (video capture — CPU/encode work, not disk/network bulk I/O); figures given are energy/power, FPS only in slide charts (not quoted). Other topics — does not cover. One device (Steam Deck OLED), Linux; window one in-game benchmark.

---

### S1-37 — Corbet, "Sched_ext at LPC 2024" (LWN, 2024)

**Citation.** Jonathan Corbet, "Sched_ext at LPC 2024", LWN.net, 2024-09-26, `https://lwn.net/Articles/991205/`.

**Copy read.** accessed 2026-09-17, `sources/S1-37/lwn-991205.html`, SHA-256 `aacfa63fecfba21761debbdfea89a91e0dc95d319ceaff1128952a7c5f890c25` (20 807 bytes).

**Passages.** Section "Higher frame rates":
> A key aspect of gaming workloads is that tasks tend to run quickly, typically no more than 100µs at a time. There are a lot of tightly linked tasks, though, and performance depends on the most critical of those tasks running in the necessary sequence; that is the critical path. Every task has a latency criticality that is determined by its place in this path […]
> Each task has a virtual deadline calculated for it, which is a function of both its waking and waiting frequencies — its latency criticality, in other words. […]
> In the scx_lavd "autopilot" mode, the scheduler looks at the current CPU utilization. For light loads, a power-saving mode is chosen; for heavy loads, the fast cores are used in a race-to-idle strategy.
> Min concluded by saying that, for gaming applications, scx_lavd consistently enables higher frame rates than the EEVDF scheduler while using (slightly) less power and with fewer stutters.

**Coverage.** T6 — covers the sched_ext/scx framing (latency criticality from wake/wait frequencies; game tasks ≤100 µs per run); says nothing about disk or network background loads specifically. Other topics — does not cover.

---

### S1-16 — Humphries et al., "ghOSt: Fast & Flexible User-Space Delegation of Linux Scheduling" (SOSP 2021)

**Citation.** Jack Tigar Humphries, Neel Natu, Ashwin Chaugule, Ofir Weisse, Barret Rhoden, Josh Don, Luigi Rizzo, Oleg Rombakh, Paul Turner, Christos Kozyrakis, "ghOSt: Fast & Flexible User-Space Delegation of Linux Scheduling", SOSP 2021.

**Copy read.** `https://cs.stanford.edu/~jhumphri/documents/ghost.pdf`, accessed 2026-09-17, `sources/S1-16/humphries2021-ghost.pdf`, SHA-256 `c37d636045a45e2216e7047ba1fb9ffa4ed88fe54b09ee0ccc33435cacd35c91` (858 413 bytes, 17 pages).

**Passage.** p. 11, §5.3:
> We run tests in two modes. In the quiet mode, the client/server threads are the only explicit workload on their machines. In the loaded mode, the machines are also running 40 additional antagonist threads of a batch workload that attempt to use idling CPU resources, unused by server or Snap threads, when network traffic is low. […] Antagonist threads only run when there are spare resources from both CFS threads and Snap. We did not use any dedicated cores.

**Coverage.** T6 — covers how this scheduler paper set up its background load: 40 CPU-consuming "antagonist" batch threads, not a disk or network I/O load; no I/O-bound background figure. Other topics — does not cover.

---

### S1-12 — Zheng, Hu, Zhang, Quinn, "Towards Agentic OS: An LLM Agent Framework for Linux Schedulers" (SchedCP; arXiv 2509.01245v4)

**Citation.** Yusheng Zheng, Yanpeng Hu, Wei Zhang, Andi Quinn, "Towards Agentic OS: An LLM Agent Framework for Linux Schedulers", arXiv:2509.01245v4 (2025).

**Copy read.** `https://arxiv.org/pdf/2509.01245v4`, accessed 2026-09-17, `sources/S1-12/schedcp-2509.01245v4.pdf`, SHA-256 `cce49d3c0ff5466cafc3b921373f6d43df2adcb97e38b40c9d45e3b21206e97c` (430 348 bytes, 6 pages).

**Passages.** p. 4, §Evaluation:
> Evaluation uses two machines: 86-core Intel Xeon 6787P with 758GB RAM running Linux 6.14, and 8-core Intel Core Ultra 7 258V with 30GB RAM running Linux 6.13.
> Scheduler Configuration: For kernel compilation (tinyconfig, "make -j 172" on 6.14 source), SchedCP achieves 1.63× speedup with scx_rusty initially, then iterative refinement selects scx_layered […] On schbench [12], initial AI configuration (scx_bpfland) underperformed, but three refinement iterations identified scx_rusty as superior: 2.11× better P99 latency and 1.60× higher […]

**Coverage.** T6 — the workloads are kernel compilation and schbench; no disk or network background load next to interactive work: **does not cover** the topic's I/O question; recorded because the search direction named it. Other topics — does not cover.

---

## 3. Read and found not to cover any topic

- **Lozi, Lepers, Funston, Gaud, Quéma, Fedorova, "The Linux Scheduler: a Decade of Wasted Cores" (EuroSys 2016)** — copy `https://www.cs.utexas.edu/~venkatar/sys_perf_analysis/linux-wasted-cores.pdf` (HAL hal-01295194 version), accessed 2026-09-17, `sources/S1-09/lozi2016-wasted-cores.pdf`, SHA-256 `7a72378254598541a7271d181c223e2b9281d1813c221785e1aef262c6c5ccca` (514 001 bytes, 17 pages). Grep for `I/O`, `disk`, `background` finds only load-balancing prose ("core intermittently sleeps due to a synchronization or I/O", p. 9); no background I/O load is set up or characterised. Not a candidate.
- **Gouicem et al., "Fewer Cores, More Hertz: Leveraging High-Frequency Cores in the OS Scheduler for Improved Application Performance" (USENIX ATC 2020)** — copy `https://www.usenix.org/system/files/atc20-gouicem.pdf`, accessed 2026-09-17, `sources/S1-21/gouicem2020-atc.pdf`, SHA-256 `4e9e4a0f9a04717b4efefaaba10a5a4d58482e1d012722f97f7b6a05789ce447` (3 722 345 bytes, 15 pages). Grep for `I/O-bound`, `disk`, `background`, `interactive` finds one incidental phrase ("nothing running in the background", p. 10). Not a candidate.

## 4. Not found

- **T1, response-side values on Linux for the named programs.** No peer-reviewed or preprint study reports CPU share, run lengths between I/O waits, blocked-on-I/O time, or warm/cold comparison for `rsync -a` trees, `cp`, `borg`, `restic`, `tar`+`xz`/`zstd`, or `7z`. Established by search-log rows 14, 15, 36, 48, 62, 64 (arXiv `rsync AND CPU`, `zstd … benchmark`, `borg AND backup`, `7-Zip`; WebSearch for backup-tool and compression-tool papers). What exists: one LWN measurement of `rsync` on a single 10 GiB file (S1-25: hog 83 %, three processes, ondemand-governor interaction), one MASCOTS 2013 throughput study of `xz`/`gzip`/`bzip2` on ARM Linux boards (S1-38), and method-level guidance on cp/tar/gzip and cache state (S1-04). The borg/restic literature is blog benchmarks only (S3's class).
- **T2, steady-state indexer behaviour.** No paper observes Tracker Miners/LocalSearch, Baloo or plocate `updatedb` in steady-state monitoring (wake cadence, CPU per wake, I/O wait, scheduling class). Established by rows 16, 37, 55, 60, 64, 65 (arXiv `"desktop search" AND indexer`, `"file indexing" AND daemon`, `Baloo`, `Tracker AND GNOME AND index`; WebSearch for indexer overhead/energy papers, Beagle/Tracker/Strigi comparisons, Nepomuk/Strigi). The only literature indexer observation is a batch first-index run of Psearchy (S1-03), which the topic excludes; the 2007 Sun comparison of Beagle/JIndex/Tracker/Strigi is reported second-hand on blogs and its original was not located.
- **T3, downloader wake structure and consumer links.** No study reports bytes per wake, wakes per second or receive-buffer behaviour for `wget`/`curl`/`aria2c`, nor any CPU figure for a Steam client's download or for an SMTP client (Thunderbird) send. Established by rows 17, 18, 50, 52, 64 (arXiv `Steam … download`, `wget AND download AND CPU`, `SMTP AND client AND CPU`, `"network stack" … "per-byte"`; WebSearch for downloader studies). What exists: cURL client CPU on a 1 Gbps LAN Linux desktop (S1-23: ~70 % under QUIC, lower under HTTP/2, value only in a figure), Steam client connection counts and per-connection Mbps from SteamCMD logs on cloud VMs (S1-22), and kernel-stack per-byte costs on server hardware (S1-02; S1-34 and S1-33 as dated context).
- **T4, `clamscan`/`clamdscan` on Linux: throttling, I/O pattern, CPU share over a scan.** No Linux-side characterisation found. Established by rows 13, 22, 39, 46, 51, 64 (arXiv `ClamAV`, `antivirus … Linux`, `antivirus AND overhead AND characterization`; WebSearch for ClamAV multithreaded/clamd evaluations and AV overhead studies). What exists: ClamAV throughput in MB/s on 2005–2010 x86 desktops with OS unnamed (S1-05, S1-29), the statement from source analysis that `clamscan` 0.98.1 scans files sequentially in one thread (S1-24, measurements on Windows), and Windows-only AV characterisations (S1-19; Uluski 2005 unreachable, Windows XP by abstract).
- **T6, measured CPU/run/wait/throughput of an interbench Write/Read load or of a copy next to interactive work under CFS/EEVDF.** No paper reports interbench Write/Read results (Wong et al. 2008 uses interbench but is paywalled — row 47/54 — and by the search summary excluded the disk loads); no CFS/EEVDF-era paper sets up a disk or network background load (S1-09, S1-12, S1-16, S1-21 use CPU antagonists, kernel builds or schbench). Established by rows 11, 12, 20, 21, 23, 24, 40, 41, 47, 64, 68. What exists: interbench's own load definitions and one unnamed-machine sample (S1-01), Redline's two synthetic disk loads with a 28 s `fsync` stall and an erratic mplayer frame rate on Linux 2.6.22 (S1-35), Torrey's kernel-compile background on Linux 2.6.3 (S1-13, context), the writeback-queue mechanism (S1-07, S1-17, S1-18), and the EEVDF/MuQSS design statements on wakeup placement (S1-10, S1-11, S1-26, S1-31).

**Unreachable or paywalled (not read):** Uluski et al. 2005 (ResearchGate 403; kipdf transcription not used); Wong et al. 2008 ITSim (IEEE Xplore paywall); Vasiliadis & Ioannidis 2010 GrAVity (ics.forth.gr TLS failure; Springer paywall); Endo & Seltzer 2000 TIPME (no open PDF; the 1996 OSDI `.ps` fetched but no converter); Kothiyal et al. SYSTOR 2009 compression study (FSL URL 404); Kolivas's MuQSS blog post (blogspot 503 via proxy); Lozi's UBC copy (browser-verification wall; replaced by the HAL copy); lore.kernel.org (Anubis challenge); Semantic Scholar and OpenAlex APIs (429).
