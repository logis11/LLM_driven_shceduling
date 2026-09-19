# T9 — S1 peer-reviewed and preprint literature (T9 parts b, c)

Reader: S1 (literature), addendum run for topic T9 (input file sets for backup and archive runs). Date of work: 2026-09-19 (all accesses that day). Input read: `search/input.md` (the "Addendum — T9" section, the class rule and the record format); `search/S1-literature.md` opened only for the record format.

Scope of this record: T9 part (b), studies of what personal or desktop file systems contain (file counts, size distributions, type or extension mix, total bytes per user or machine, compressibility, duplication), and T9 part (c), characterisations of real backup data (what backup sources contain, size and type mix, compressibility and deduplication, and how much changes between consecutive backups). Parts (a) and (d) belong to S2 and S3 and were not searched. Topics T1–T8 were not assessed in this run.

Conventions of this record:

- Fetches were made with `curl -sS -L` (browser User-Agent string, no proxy), directly from the machine. Web search was used only to locate copies; no search result is cited.
- PDFs were text-extracted with **PyMuPDF 1.28.2** (`pymupdf`, `page.get_text()`), installed into a venv under the session scratchpad. The one PostScript copy (T9-S1-15) was converted to PDF with **Ghostscript 10.05.0 `ps2pdf`** (already present at `/opt/homebrew/bin`) and the PDF then extracted with PyMuPDF. Where a table's rows came out of the extractor one cell per line, the rows were rebuilt with PyMuPDF `page.get_text("words")` grouped by line position; such tables are marked *reader's layout reconstruction* — the cell values are verbatim, only the row grouping is mine.
- Locators "p. N" are the N-th page of the fetched file as PyMuPDF counts it (not the printed page number) unless stated.
- Passages are verbatim except for extraction normalisations, stated once here: typographic ligatures (fi, fl, ff) rendered as single glyphs, as "￿" (T9-S1-21) or as "$" (the "ti" ligature in T9-S1-27) are written as plain letters; "∼" is written "~"; "⇥" (T9-S1-21) and "×" are written "×"; footnote markers are omitted; superscripts lost by the extractor are shown as "10^n" where the exponent is unambiguous from context, and the raw extraction is given in brackets.
- For USENIX papers whose copy carries no venue footer (T9-S1-02, -03, -19, -24, -29), the venue is taken from the USENIX proceedings path of the URL fetched (e.g. `/fast12/`, `/atc12/`); the S1 record of 2026-09-17 identifies T9-S1-02 and T9-S1-03 the same way.
- Copies live under `sources/T9-S1-NN/` (gitignored). Every citation carries URL, access date, byte count, page count and SHA-256 so the record stands without the folder.
- T9 is an input, not a response-side value: every platform is admissible; platform, population and date are named for each candidate; age is recorded, not a ground for exclusion.

Candidate ids are provisional and not contiguous. T9-S1-32 (Gonçalves & Jorge 2003) was assigned and dropped because no copy could be fetched. T9-S1-09, T9-S1-23, T9-S1-25, T9-S1-34 and T9-S1-35 were fetched and read and found not to be candidates; they are listed in §3.

---

## 1. Search log

Engines and venues used: WebSearch (the session's web-search tool, used only to locate copies), USENIX proceedings by direct URL and via presentation pages, Microsoft Research publication PDFs, arXiv (PDF and `export.arxiv.org/api/query`), author and lab sites (cs.hmc.edu, fsl.cs.stonybrook.edu, minix3.org, cs.cornell.edu), conference sites (conferences.sigcomm.org, systor.org), university repositories (conservancy.umn.edu, openscience.ub.uni-mainz.de). HTTP status in brackets; [000] = no connection.

| # | Date | Engine / venue | Query or URL | Hits followed / dead ends |
|---|------|----------------|--------------|---------------------------|
| 1 | 2026-09-19 | USENIX (direct) | `usenix.org/legacy/event/fast07/tech/full_papers/agrawal/agrawal.pdf` | [200] → T9-S1-01 |
| 2 | 2026-09-19 | USENIX (direct) | `usenix.org/legacy/event/fast11/tech/full_papers/Meyer.pdf` | [200] → T9-S1-02 (byte-identical, by SHA-256, to the S1-08 copy of 2026-09-17) |
| 3 | 2026-09-19 | USENIX (direct) | `usenix.org/system/files/conference/fast12/wallace2-9-12.pdf` | [200] → T9-S1-03 (byte-identical, by SHA-256, to the S1-15 copy of 2026-09-17) |
| 4 | 2026-09-19 | USENIX (direct) | `usenix.org/system/files/conference/atc15/atc15-paper-amvrosiadis.pdf` | [404] (guessed file name); see row 20 |
| 5 | 2026-09-19 | USENIX (direct) | `usenix.org/legacy/event/fast09/tech/full_papers/vrable/vrable.pdf` | [200] → T9-S1-05 |
| 6 | 2026-09-19 | USENIX (direct) | `…/fast09/tech/full_papers/lillibridge/lillibridge.pdf`; `…/osdi02/tech/full_papers/cox/cox.pdf`; `…/usenix04/tech/general/full_papers/policroniades/policroniades.pdf`; `…/usenix-win2000/full_papers/bolosky/bolosky.pdf`; `usenix.org/system/files/conference/fast13/fast13-final124.pdf` | [200] ×5 → T9-S1-06, T9-S1-07, T9-S1-08, T9-S1-09 (§3), T9-S1-10 |
| 7 | 2026-09-19 | WebSearch | Douceur Bolosky "A large-scale study of file-system contents" SIGMETRICS 1999 pdf | `microsoft.com/en-us/research/wp-content/uploads/1999/01/Sigmetrics1999.pdf` [200] → T9-S1-11; ACM DL copies not followed |
| 8 | 2026-09-19 | WebSearch | Bolosky Douceur Ely Theimer "Feasibility of a serverless distributed file system deployed on an existing set of desktop PCs" pdf | `…/uploads/2000/01/Sigmetrics2000.pdf` [200] → T9-S1-12; `…/uploads/2016/02/tr-2002-30.pdf` [200] → T9-S1-13 |
| 9 | 2026-09-19 | WebSearch | Tanenbaum Herder Bos "File size distribution on UNIX systems: then and now" pdf | only Semantic Scholar, ResearchGate, DeepDyve, ACM DL listed; not followed |
| 10 | 2026-09-19 | direct probes | `cs.vu.nl/~ast/Publications/Papers/osr-2006.pdf`, `cs.vu.nl/~herbertb/papers/osr06.pdf`, `cs.vu.nl/~herbertb/papers/filesize_osr06.pdf` | [404] ×3 |
| 11 | 2026-09-19 | direct probe | `minix3.org/docs/jorrit-herder/osr-jan06.pdf` | [200] → T9-S1-14 (co-author's document folder) |
| 12 | 2026-09-19 | WebSearch | Evans Kuenning "A Study of Irregularities in File-Size Distributions" SPECTS 2002 pdf | no copy listed; `cs.hmc.edu/~geoff/papers/spects02.pdf` [404] (guess); `cs.hmc.edu/~geoff/pubs.html` [200] links `cs.hmc.edu/~geoff/papers/filesize02.ps` [200] → T9-S1-15 |
| 13 | 2026-09-19 | WebSearch | Dinneen Julien Frissen "The scale and structure of personal file collections" CHI 2019 pdf | `library.usc.edu.ph/ACM/CHI2019/1proc/paper327.pdf` [200] → T9-S1-16; ACM DL, ResearchGate not followed; the result list also surfaced arXiv 2107.03272 → `arxiv.org/pdf/2107.03272v1` [200] → T9-S1-17 |
| 14 | 2026-09-19 | WebSearch | Sun Kuenning Mandal Shilane Tarasov Zadok "A long-term user-centric analysis of deduplication patterns" MSST 2016 pdf | IEEE Xplore only; probes `fsl.cs.stonybrook.edu/docs/msst16dedup/msst16dedup.pdf` and the `fsl.cs.sunysb.edu` variant [404] ×2 |
| 15 | 2026-09-19 | WebSearch | "long-term user-centric analysis of deduplication patterns" fsl.cs.stonybrook.edu OR fsl.cs.sunysb.edu pdf; "Cluster and Single-Node Analysis of Long-Term Deduplication Patterns" … pdf | `fsl.cs.stonybrook.edu/docs/msst16dedup-study/data-set-analysis.pdf` [200] → T9-S1-20; `fsl.cs.sunysb.edu/docs/msst16dedup-study/tos17dedup-study-a13-sun.pdf` [200] → T9-S1-21 |
| 16 | 2026-09-19 | WebSearch | Dinneen Julien "What's in people's digital file collections?" pdf | `arxiv.org/pdf/2402.06421v1` [200] → T9-S1-18 |
| 17 | 2026-09-19 | WebSearch | Tarasov Mudrankit Buik Shilane Kuenning Zadok "Generating Realistic Datasets for Deduplication Analysis" USENIX ATC 2012 pdf | `usenix.org/system/files/conference/atc12/atc12-final129.pdf` [200] → T9-S1-19; FSL copy and `tracer.filesystems.org` (trace archive, S3's class) not followed |
| 18 | 2026-09-19 | WebSearch | Amvrosiadis Bhadkamkar "Identifying Trends in Enterprise Data Protection Systems" USENIX ATC 2015 pdf | USENIX presentation page → row 20 |
| 19 | 2026-09-19 | WebSearch | Park Lilja "Characterizing datasets for data deduplication in backup applications" IISWC 2010 pdf | IEEE Xplore only (paywalled, not fetched — dropped); a UMN thesis surfaced: `conservancy.umn.edu/server/api/core/bitstreams/15d8ca76-…/content` [200] → T9-S1-23 (§3) |
| 20 | 2026-09-19 | USENIX presentation pages | `…/conference/atc15/technical-session/presentation/amvrosiadis`, `…/atc12/technical-sessions/presentation/el-shimi`, `…/atc18/presentation/allu`, `…/fast13/technical-sessions/presentation/harnik`, `…/fast14/technical-sessions/presentation/lin`, `…/hotstorage15/workshop-program/presentation/lin` | PDF links read from the pages: `atc15-paper-amvrosladis.pdf` [200] → T9-S1-04; `atc12-final293.pdf` [200] → T9-S1-24; `atc18-allu.pdf` [200] → T9-S1-25 (§3); `fast13-final38.pdf` [200] → T9-S1-26; `fast14-paper_lin.pdf` [200] → T9-S1-30; `hotstorage15-lin.pdf` located, not fetched (metadata-and-dedup design paper) |
| 21 | 2026-09-19 | WebSearch | Meister Brinkmann "Multi-level comparison of data deduplication in a backup scenario" SYSTOR 2009 pdf (two phrasings) | paper itself only at ACM DL (paywalled); `systor.org/2009/papers/2_1_3.pdf` [200] (authors' conference slides) → T9-S1-27; `openscience.ub.uni-mainz.de/server/api/core/bitstreams/95550a44-…/content` [200] (Meister's 2013 dissertation) → T9-S1-28 |
| 22 | 2026-09-19 | WebSearch | Gracia-Tinedo "Dissecting UbuntuOne: Autopsy of a Global-scale Personal Cloud Back-end" IMC 2015 pdf | `conferences.sigcomm.org/imc/2015/papers/p155.pdf` [200] → T9-S1-22 |
| 23 | 2026-09-19 | WebSearch | Tan Jiang Feng "SAM: A Semantic-Aware Multi-tiered Source De-duplication Framework for Cloud Backup" personal computer datasets … pdf | IEEE Xplore, ResearchGate, Semantic Scholar only — no open copy; dropped |
| 24 | 2026-09-19 | WebSearch | Fu Jiang Xiao "AA-Dedupe" application-aware source deduplication cloud backup personal computing environment dataset … pdf | IEEE Xplore, ResearchGate, Springer only — no open copy; dropped |
| 25 | 2026-09-19 | WebSearch | study file system contents personal computers file size distribution extension total bytes per machine 2020 OR 2021 OR 2022 OR 2023 measurement paper | only Dinneen & Nguyen 2021 (row 13) and an arXiv comparison of billion-file file systems (not personal data; not followed) |
| 26 | 2026-09-19 | USENIX (direct probes) | `…/legacy/event/fast11/tech/full_papers/Dong.pdf`; `…/legacy/event/fast08/tech/full_papers/zhu/zhu.pdf`; `…/system/files/conference/fast14/fast14-paper_lin.pdf` | [200] ×3; Dong → T9-S1-29; Lin → T9-S1-30; Zhu (Data Domain file-system design, FAST 2008) not fetched — its data sets are appliance-side Exchange/engineering streams already represented by T9-S1-03 |
| 27 | 2026-09-19 | WebSearch | Vogels "File system usage in Windows NT 4.0" SOSP 1999 pdf | `cs.cornell.edu/projects/Quicksilver/public_pdfs/File%20System%20Usage.pdf` [200] → T9-S1-31 |
| 28 | 2026-09-19 | WebSearch | Henderson Srinivasan "An empirical analysis of personal digital document structures" file types duplication pdf | Springer chapter only (paywalled) — dropped |
| 29 | 2026-09-19 | WebSearch | Gonçalves Jorge "An empirical study of personal document spaces" 2003 pdf file types | `virtual.inesc.pt/dsvis03/papers/05.pdf` [000, connection failed] — dropped (T9-S1-32) |
| 30 | 2026-09-19 | WebSearch | measurement study personal computer backup daily incremental size change rate desktop users dataset deduplication paper | Meyer & Bolosky (have), arXiv 1607.08388 and 1904.05736 (encrypted-deduplication systems that re-describe the FSL and Microsoft data sets — secondary, not followed), vendor community pages (not literature) |
| 31 | 2026-09-19 | WebSearch | Kaczmarczyk Barczynski Kilian Dubnicki "Reducing impact of data fragmentation caused by in-line deduplication" SYSTOR 2012 pdf backup datasets | ACM DL, ResearchGate only — dropped; result list surfaced arXiv 1405.5661 → `arxiv.org/pdf/1405.5661v1` [200] → T9-S1-33 |
| 32 | 2026-09-19 | arXiv API | `all:"file system" AND all:contents AND all:desktop`; `all:"home directories" AND all:backup AND all:deduplication`; `abs:"backup" AND abs:"workload" AND abs:"characterization"`; `all:"data deduplication" AND all:"snapshots" AND all:users` | 0 hits each |
| 33 | 2026-09-19 | arXiv API | `all:"personal files" AND all:"file size"`; `all:"file size distribution"` | 1 relevant hit (2107.03272, have); others (Pareto file sizes in distributed storage, ORAM, caching, D2D) not about file-system contents |
| 34 | 2026-09-19 | arXiv API | `all:deduplication AND all:backup AND all:dataset`; `all:compressibility AND all:"real-world" AND all:storage` | 1405.5661 (have) and 1904.05736 (secondary); compressibility query: 20 hits on model, image, columnar and scientific-data compression — none about personal file systems |
| 35 | 2026-09-19 | WebSearch | study compressibility of user files desktop personal data gzip compression ratio file types measurement paper | arXiv 2308.12275 → `arxiv.org/pdf/2308.12275v1` [200] → T9-S1-34 (§3); a ScienceDirect source-code compressibility study (not personal data; not followed) |
| 36 | 2026-09-19 | WebSearch | large-scale study Windows 10 file system metadata enterprise desktops 2015..2020 file count size distribution paper FAST OR SYSTOR OR TOS | only Agrawal 2007 and Douceur 1999 (have) |
| 37 | 2026-09-19 | USENIX (direct) | `usenix.org/legacy/event/usenix08/tech/full_papers/rhea/rhea.pdf` | [200] → T9-S1-35 (§3) |

---

## 2. Candidates

### 2.1 Part (b) — what personal or desktop file systems contain

### T9-S1-11 — Douceur & Bolosky, "A Large-Scale Study of File-System Contents" (SIGMETRICS 1999)

**Citation.** John R. Douceur, William J. Bolosky, "A Large-Scale Study of File-System Contents", Proceedings of SIGMETRICS '99, Atlanta, May 1999, pp. 59–70 (pages as given in the reference lists of T9-S1-01, ref. [9], and T9-S1-12).

**Copy read.** `https://www.microsoft.com/en-us/research/wp-content/uploads/1999/01/Sigmetrics1999.pdf`, accessed 2026-09-19, `sources/T9-S1-11/douceur1999-sigmetrics.pdf`, 244 486 bytes, 12 pages (PyMuPDF count), SHA-256 `ad3e4caa155abbb331ee7ad85e88f22ad4f2709f0d30eb7d2cf28bd154bc2421`.

**Passages.**

p. 1, abstract:
> We collect and analyze a snapshot of data from 10,568 file systems of 4801 Windows personal computers in a commercial environment. The file systems contain 140 million files totaling 10.5 TB of data.

p. 2, §3:
> We distributed the scanning program via email to nearly all of the employees at the Microsoft Corporation main campus, requesting the recipients to execute the program on their personal computers. To reduce the peak load on the network and on the receiving server, we spread the requests over 13 business days between September 1 and September 23, 1998.

p. 2, §3:
> By this measure, the total size of all scanned files was 10.5 TB. All computer systems were Intel x86 machines, except for one Digital Alpha machine that contained three file systems. The file systems were primarily 16- or 32-bit FAT [21] and NTFS [34], as indicated in Table 1.

p. 3, §4:
> The mean file size ranges from 64 kB to 128 kB across the middle two quartiles of all file systems, which is approximately four times the mean file size found in a recent study [30] of Unix systems.

p. 3, §4:
> Figure 1 shows a histogram of files by size. 1.7% of all files have a size of zero, and the median size is 4 kB. We can approximate this histogram with a mixture of a constant distribution for zero-size files and a log-normal distribution [11] (µ(2) = 12.2, σ(2) = 3.43, binary log; or µ(e) = 8.46, σ(e) = 2.38, natural log)

p. 8, §7:
> We generated a list of all file-name extensions (the characters following the last period) of five characters or less, excluding those that were purely numeric, resulting in a list of 19,140 entries including the null extension. This list accounts for over 99% of all files in our data set. Table 4 lists the 30 most popular extensions, representing 70% of all files.

p. 9, §8:
> The total space allotted to each file system is fairly consistent across our sample set: 62% of file systems have 1 to 2 GB of total space, and this mode is consistent across job categories. […] The mean number of files per user is 31,835, which is 20 to 26 times that found on Unix systems in 1991 [2] and 1994 [30], largely because each user's machine has a separate installation of the operating system and application programs.

**Coverage.** T9(b) — **covers.** Object: whole fixed-disk file systems (system and user files) of desktop PCs. Units and statistics: file count per user (mean 31,835), file-size distribution (median 4 kB, 1.7 % zero-size, mean per file system 64–128 kB across the middle quartiles, log-normal fit parameters), extension popularity (30 extensions = 70 % of files), file-system capacity (62 % of file systems 1–2 GB), total bytes of the population (10.5 TB over 140 million files). Population: 4 418 self-selected Microsoft employees, 4 801 machines, 10 568 file systems. Platform: Windows (FAT16/FAT32/NTFS), x86. Date: September 1998. Does not cover: content (no hashes, so no duplication or compressibility in this paper — see T9-S1-12), change between snapshots (single snapshot), Linux.

**Observation status.** One snapshot of one population; machine class and window named; per-file contents not observed. 28 years old: recorded, not excluded.

---

### T9-S1-12 — Bolosky, Douceur, Ely, Theimer, "Feasibility of a Serverless Distributed File System Deployed on an Existing Set of Desktop PCs" (SIGMETRICS 2000)

**Citation.** William J. Bolosky, John R. Douceur, David Ely, Marvin Theimer (Microsoft Research), SIGMETRICS 2000, June 2000, Santa Clara (per the copy's p. 1 footer "SIGMETRICS 2000 6/00 Santa Clara, California, USA").

**Copy read.** `https://www.microsoft.com/en-us/research/wp-content/uploads/2000/01/Sigmetrics2000.pdf`, accessed 2026-09-19, `sources/T9-S1-12/bolosky2000-sigmetrics.pdf`, 354 223 bytes, 10 pages, SHA-256 `6d8fa04a83b292d70e44ae56c77c64e45cc22866fb48c303166e39ed72088d0d`.

**Passages.**

p. 3, §3.1.1–3.1.2:
> In September 1998, we asked Microsoft employees to run a scanning program on their Windows and Windows NT computers that collected directory information (file names, sizes, and timestamps) from their file systems [7]. By this means, we obtained measurements of 10,568 file systems [8]. In August 1999, we remotely read the performance counters (free disk space, total disk space, and logon name of the primary user) of every Windows NT computer we could access. By this means, we obtained measurements of 8669 file systems.
>
> In February 1999, we asked a random subset of the participants in the 1998 study to run a scanning program that computed and recorded hashes of all the files on their file systems. By this means, we obtained data from 550 file systems, which we used to determine the amount of duplicate file content.

p. 4, §4.1.1–4.1.2:
> The self-selected September 1998 data show 53% of overall disk space in use. The remotely read August 1999 data show 50% of overall disk space in use.
>
> The open circle on the graph shows that removing duplicates from the whole population of 550 file systems reclaims 47% of used file space.

p. 5, §4.1.2:
> Only about 5% of file space is reclaimed by eliminating duplicates of files with at least 100 duplicates, less than 30% with a minimum of 10, and 47% when considering files with at least one duplicate.

**Coverage.** T9(b) — **covers duplication.** Object: whole-file content duplication across desktop file systems. Unit: share of used file space reclaimable by whole-file deduplication. Statistic: 47 % over the 550-file-system population; reclaimable share as a function of population size is in Figure 1 (values not quoted). Fullness: 53 % (Sept 1998), 50 % (Aug 1999, 8 669 file systems). Population: random subset of the 1998 Microsoft participants. Platform: Windows / Windows NT. Date: February 1999 (hashes). Does not cover: duplication within one machine alone (the 1-file-system point is only in the figure), sub-file duplication, compressibility, change between backups.

**Observation status.** One hash scan of one population; window named.

---

### T9-S1-13 — Douceur, Adya, Bolosky, Simon, Theimer, "Reclaiming Space from Duplicate Files in a Serverless Distributed File System" (MSR-TR-2002-30; ICDCS 2002)

**Citation.** John R. Douceur, Atul Adya, William J. Bolosky, Dan Simon, Marvin Theimer, Microsoft Research Technical Report MSR-TR-2002-30, July 2002. The copy states (p. 2, footnote): "This paper is an extended version of a paper that appeared in the 22nd IEEE International Conference on Distributed Computing Systems".

**Copy read.** `https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-2002-30.pdf`, accessed 2026-09-19, `sources/T9-S1-13/douceur2002-tr-2002-30.pdf`, 572 963 bytes, 14 pages, SHA-256 `13ee89db024ba79e0fdb51e51b26d8ad25a288fb4460ae59f08143a7ab680f27`.

**Passage.** p. 10, §5:
> we evaluated the DFC subsystem via large-scale simulation using file content data collected from 585 desktop file systems. We distributed a scanning program to a randomly selected set of Microsoft employees and asked them to scan their desktop machines. The program computed a 36-byte cryptographically strong hash of each 64-Kbyte block of all files on their systems, and it recorded these hashes along with file sizes and other attributes. The scanned systems contain 10,514,105 files in 730,871 directories, totaling 685 GB of file data. There were 4,060,748 distinct file contents totaling 368 GB of file data, implying that coalescing duplicates could ideally reclaim up to 46% of all consumed space.

**Coverage.** T9(b) — **covers.** Object: whole desktop file systems. Units: files, directories, bytes; whole-file duplicate share. Statistics: 585 file systems, 10 514 105 files, 685 GB, 368 GB distinct content, 46 % reclaimable across the pooled population. Population: randomly selected Microsoft employees. Platform: Windows desktops (OS version not named in the passage). Date: scan date not stated in this copy (report dated July 2002). Does not cover: per-machine size distribution, types, compressibility, change over time.

**Observation status.** One scan of one population; window not named.

---

### T9-S1-31 — Vogels, "File system usage in Windows NT 4.0" (SOSP 1999)

**Citation.** Werner Vogels (Cornell University), "File system usage in Windows NT 4.0", 17th ACM Symposium on Operating Systems Principles (SOSP'99), Kiawah Island, SC, December 1999 (per the copy's p. 1 footer "SOSP-17 12/1999 Kiawah Island, SC"); ACM SIGOPS Operating Systems Review 33(5):93–109 (volume and pages as given in the reference list of T9-S1-17, p. 7).

**Copy read.** `https://www.cs.cornell.edu/projects/Quicksilver/public_pdfs/File%20System%20Usage.pdf`, accessed 2026-09-19, `sources/T9-S1-31/vogels1999-file-system-usage.pdf`, 2 257 216 bytes, 17 pages, SHA-256 `ab0a39fca0cd6efc47135d158e654a634e1dfaec8b100fa6acbf1a6c5244a2a0`.

**Passages.**

p. 2, §2:
> All systems ran Windows NT 4.0 with the latest service packs applied. At the time of the traces the age of file systems ranged from 2 months to 3 years, with an average of 1.2 years.

p. 3, §3:
> The analysis reported in this paper is based on a final data collection that ran for 4 weeks in November and December of 1998. The 45 systems generated close to 19 GB of trace data over this period.

p. 5, §5:
> We see that the local file systems have between 24,000 and 45,000 files, that the file size distribution is similar for all systems, and that the directory depth and sizes are almost identical. File systems are between 54% and 87% full.
>
> The network server file systems are organized into shares, which is a remote mountable sub-tree of a file system. In our setting each share represents a user's home directory. There was no uniformity in size or content of the user shares; sizes ranged from 500 Kbytes to 700 Mbytes and number of files from 150 to 27,000.

p. 5, §5:
> For local file systems the size distribution is dominated by executables, dynamic loadable libraries and fonts, while for the network file system the set of large files is augmented with development databases, archives and installation packages.

p. 6, §5:
> A commonly observed daily pattern is one where 300-500 files change or are added to the system, with peaks of up to 2,500 and 3,000 files, up to 93% of which are in the WWW cache.
>
> Changes to user shares at the network file server occur at much slower pace. A common daily pattern is where 5-40 files change or are added to the share, with peaks occurring when the user installs an application package or retrieves a large set of files from an archive.

**Coverage.** T9(b) — **covers**: file count per local file system (24 000–45 000), fullness (54–87 %), per-user home-share size (500 KB–700 MB, 150–27 000 files), which types dominate bytes. T9(c) — **covers, as file-count change per day**: 300–500 files changed or added per day on a local file system (peaks 2 500–3 000, up to 93 % in the web cache); 5–40 files per day on a home share. Population: 45 Windows NT 4.0 machines in five usage categories (walk-up, pool, personal, administrative, scientific) at Cornell, plus the users' network home shares. Date: November–December 1998. Does not cover: bytes changed per day, compressibility, duplication, extension shares as numbers.

**Observation status.** One 4-week collection on named machine classes; window named. 28 years old: recorded.

---

### T9-S1-01 — Agrawal, Bolosky, Douceur, Lorch, "A Five-Year Study of File-System Metadata" (FAST 2007)

**Citation.** Nitin Agrawal, William J. Bolosky, John R. Douceur, Jacob R. Lorch, "A Five-Year Study of File-System Metadata", 5th USENIX Conference on File and Storage Technologies (FAST '07); first printed page 31.

**Copy read.** `https://www.usenix.org/legacy/event/fast07/tech/full_papers/agrawal/agrawal.pdf`, accessed 2026-09-19, `sources/T9-S1-01/agrawal2007-five-year-metadata.pdf`, 207 918 bytes, 15 pages, SHA-256 `7adf18fb25ad68a3bf6851bfb8c3b85352cf522ecc38489cf0136f9120ca27bc`.

**Passages.**

p. 1, §1:
> Every year from 2000 to 2004, we collected snapshots of metadata from over ten thousand file systems on the Windows desktop computers at Microsoft Corporation. We gathered this data by mass-emailing a scanning program to Microsoft's employees, and we had a 22% participation rate every year. Our resulting datasets contain metadata from 63,398 distinct file systems, 6457 of which provided snapshots in multiple years.

p. 1, §1:
> • The space used in file systems has increased over the course of our study, not only because mean file size has increased (from 108 KB to 189 KB), but also because the number of files has increased (from 30K to 90K).
> • Eight file-name extensions account for over 35% of files, and nine file-name extensions account for over 35% of the bytes in files. The same sets of extensions have remained popular for many years.

p. 3, §2.5 (Limitations):
> All our data comes from a relatively homogenous sample of machines: Microsoft desktops running Windows. […] our conclusions are likely not applicable to file system server workloads, and it is unclear to what extent they can be generalized to non-Windows operating systems.

p. 3, §3.1:
> The count of files per file system has increased steadily over our five-year sample period: The arithmetic mean has grown from 30K to 90K files and the median has grown from 18K to 52K files.

p. 5, Figure 6 caption:
> Contribution of file types to Figure 4 (2004). Video means files with extension avi, dps, mpeg, mpg, vob, or wmv; DB means files with extension ldf, mad, mdf, ndf, ost, or pst; and Blob means files named hiberfil.sys and files with extension bak, bkf, bkp, dmp, gho, iso, pqi, rbf, or vhd.

p. 5, §3.2:
> We observe that the distribution of file size has shifted to the right over time, with the median weighted file size increasing from 3 MB to 9 MB.

p. 9, §4.3:
> Backup software generally does not have to back up system files, since they are static and easily restored. Since system files are accounting for a larger and larger fraction of used space, it is becoming more and more useful for backup software to exclude these files.

p. 11, §5.1:
> Space consumption increased steadily over our five-year sample period: The geometric mean has grown from 1 GB to 9 GB, the arithmetic mean has grown from 3 GB to 18 GB, and the median has grown from 2 GB to 13 GB.

p. 12, §5.2:
> Analyzing the factors that contribute to the 14-point mean year-to-year increase in fullness revealed the following breakdown: Fullness increases by 28 percentage points due to files that are present in the later snapshot but not in the earlier one, meaning that they were created during the intervening year. Fullness decreases by 15 percentage points due to files that are present in the earlier snapshot but not in the later one, meaning that they were deleted during the intervening year. Fullness also increases by 1 percentage point due to growth in the size of files that are present in both snapshots.

**Coverage.** T9(b) — **covers.** Object: whole fixed-disk file systems of desktops. Units and statistics: files per file system (mean 30K→90K, median 18K→52K), mean file size (108 KB→189 KB), byte-weighted median file size (3 MB→9 MB), consumed space per file system (median 2 GB→13 GB; mean 3→18 GB), extension shares by count and bytes (Figures 9–10; values in figures), share of bytes in `Documents and Settings`, `Windows`, `Program Files` (Figure 17; the text gives 7 %→15 % for user documents and settings). Population: ~5 400–7 500 users per year, 63 398 distinct file systems. Platform: Windows (80 % NTFS). Date: autumn 2000–2004. T9(c) — **partly**: year-over-year change for the same file system (+28 points created, −15 deleted, +1 growth of fullness) — an annual interval, not a backup interval. Does not cover: content (no hashes, no compressibility, no duplication), Linux.

**Observation status.** Five annual snapshots of one population; windows named (Table 1: 13 Sep–29 Sep 2000 … 5 Oct–12 Nov 2004).

---

### T9-S1-02 — Meyer & Bolosky, "A Study of Practical Deduplication" (FAST 2011)

**Citation.** Dutch T. Meyer, William J. Bolosky, "A Study of Practical Deduplication", 9th USENIX Conference on File and Storage Technologies (FAST '11).

**Copy read.** `https://www.usenix.org/legacy/event/fast11/tech/full_papers/Meyer.pdf`, accessed 2026-09-19, `sources/T9-S1-02/meyer2011-practical-dedup.pdf`, 709 718 bytes, 13 pages, SHA-256 `9c91ba8b42d7a42d39fb78eb4a79cc7b51bfc8e9249558b5db09476609a371c5` (identical to the copy recorded as S1-08 in `S1-literature.md`).

**Passages.**

p. 1, abstract and §1:
> We collected file system content data from 857 desktop computers at Microsoft over a span of 4 weeks.
>
> We find that the previously observed trend toward storage being consumed by files of increasing size continues unabated; half of all bytes are in files larger than 30MB (this figure was 2MB in 2000).

p. 2, §2:
> The scanner ran autonomously during off hours once per week from September 18 – October 16, 2009. We contacted 10,500 people in this manner to reach the target study size of about 1000 users.

p. 5, §3.3:
> The most aggressive chunking algorithm (8K Rabin) reclaimed between 18% and 20% more of the total file size than did whole file deduplication.
>
> This table shows that the savings due to whole file duplicates are concentrated in files containing program binaries: dll, lib, pdb, exe, cab, msp, and msi together make up 58% of the saved space.

p. 6, §3.4:
> We considered the 483 file systems for which four continuous weeks of complete scans were available, starting with September 18, 2009 […]
>
> Using the Rabin chunking algorithm with an 8K expected chunk size, block-level deduplication reclaimed 83% of the total space. Whole file deduplication, on the other hand, yielded 72%. These numbers, of course, are highly sensitive to the number of weeks of scans used in the study; it's no accident that the results were around ¾ of the space being claimed when there were four weeks of backups. However, one should not assume that because 72% of the space was reclaimed by whole file deduplication that only 3% of the bytes were in files that changed. The amount of change was larger than that, but the deduplicator found redundancy within a week as well and the two effects offset.

p. 8, §4:
> Our data set contains scans of 857 file systems hosted on 597 computers. 59% were running Windows 7, 20% Windows Vista, 18% Windows Server 2008 and 3% Windows Server 2003.
>
> The mean file system capacity is 194GB.
>
> Mean utilization is 43%, only somewhat less than the 53% found in 2000.
>
> Both file and directory counts show a significant increase from previous years in Figures 6 and 7 respectively, with a mean of 225K files and 36K directories per file system.
>
> The mean file size is now 318K, about three times what it was in 2000.

p. 9, §4.4:
> The median file size remains 4K (a result that has been remarkably consistent since at least 1981 [27])

**Coverage.** T9(b) — **covers.** Object: whole fixed-disk file systems of desktop workstations. Statistics: 225K files and 36K directories per file system (means), mean file size 318K, median 4K, half of bytes in files > 30 MB, capacity mean 194 GB, utilisation mean 43 %, extension shares by count and bytes (Figures 18–19), whole-file vs block deduplication (8K Rabin reclaims 18–20 % more than whole-file on the pooled set; duplicates by extension in Tables 1–2). T9(c) — **covers, weekly**: four weekly full-backup images of 483 file systems deduplicate by 83 % (block, 8K Rabin) and 72 % (whole-file); the authors state the changed-byte share is larger than 3 % but do not give it. Population: randomly contacted Microsoft employees (≈10 % participation), 597 computers. Platform: Windows 7/Vista/Server 2008/Server 2003. Date: 18 September–16 October 2009. Does not cover: compressibility; bytes changed between consecutive weeks as a number; Linux.

**Observation status.** One population, four weekly scans; window named.

---

### T9-S1-15 — Evans & Kuenning, "A Study of Irregularities in File-Size Distributions" (SPECTS 2002)

**Citation.** Kylie M. Evans, Geoffrey H. Kuenning, "A Study of Irregularities in File-Size Distributions", 2002 International Symposium on Performance Evaluation of Computer and Telecommunication Systems (SPECTS '02), San Diego, July 2002 (citation as listed on the author's publication page, `cs.hmc.edu/~geoff/pubs.html`, lines 437–442 of the page as fetched).

**Copy read.** `https://www.cs.hmc.edu/~geoff/papers/filesize02.ps`, accessed 2026-09-19, `sources/T9-S1-15/evans2002-filesize02.ps`, 1 499 465 bytes (PostScript, dvips 5.86, "TeX output 2002.05.29"), SHA-256 `057d142092eb459149ec70cbfe0ef6bd09cd712a61ac4d952346a3cf144dfece`. Converted with Ghostscript 10.05.0 `ps2pdf` to a scratch PDF (12 pages) and extracted with PyMuPDF; the scratch PDF is not kept.

**Passages.**

p. 2, §4.1:
> We gathered the data in the summer of 2001, from both personal computers and large servers. There were six systems running various editions of Windows, eight running Linux distributions (including the three machines from MBL), five that dual-booted both Windows and Linux, and three large Unix-based campus servers.

p. 2, §4.1:
> The data for the Linux and Unix machines was collected by a shell script that used find (as root) to locate all files. To maintain privacy, we discarded directory and file names, keeping only the size in bytes, type, modification date, directory depth, extension, and the number of blocks used by the file.

p. 3, Table 1 (*reader's layout reconstruction*; columns: Fig., OS, Type, # of Machines, # of Files, # of Zero-Size Files, # of Media Files):
> 1 Linux all 8 901,055 17,242 2373
> 2 Multi all 3 2,632,014 104,132 567
> 3 Windows all 6 204,037 2118 20,740
> – Dual all 5 752,192 9683 11,806
> 5 Linux HMC non-media 5 362,847 6039 0
> – Linux MBL non-media 3 535,835 11,199 0
> 6 all MP3 18 18,303 25 18,303
> – All OSes all files 22 4,489,298 133,175 35,486

**Coverage.** T9(b) — **covers.** Object: whole file systems of named machine classes (personal computers and campus servers). Units: file counts per OS group, zero-size files, media files; size distributions and fitted models in figures (values not quoted). Population: volunteers at Harvey Mudd College (680 students) plus three machines at the Marine Biological Laboratories. Platform: Linux (8), Windows (6), dual-boot (5), Unix servers (3) — one of the few (b) sources with Linux personal machines. Date: summer 2001. Does not cover: bytes per machine as a quoted number, compressibility, duplication, change over time; the authors state selection toward large MP3 collections (bias noted in §4.2).

**Observation status.** One collection across 22 machines; window named. 25 years old: recorded.

---

### T9-S1-14 — Tanenbaum, Herder, Bos, "File Size Distribution on UNIX Systems—Then and Now" (ACM SIGOPS OSR 2006)

**Citation.** Andrew S. Tanenbaum, Jorrit N. Herder, Herbert Bos, "File Size Distribution on UNIX Systems—Then and Now", ACM SIGOPS Operating Systems Review 40(1):100–104, 2006 (volume, pages and year as given in the reference list of T9-S1-17, p. 7; the fetched copy carries no journal footer).

**Copy read.** `https://www.minix3.org/docs/jorrit-herder/osr-jan06.pdf` (co-author's document folder), accessed 2026-09-19, `sources/T9-S1-14/tanenbaum2006-osr-jan06.pdf`, 334 777 bytes, 5 pages, SHA-256 `394800dfe2c09c75ccb34759b581ea423543fe0a30d165b45432d05f30db4551`.

**Passages.**

p. 1, abstract and §1:
> In 1984, we published the file size distribution for a university computer science department. We have now made the same measurements 20 years later to see how file sizes have changed. In short, the median file size has more than doubled (from 1080 bytes to 2475 bytes), but large files still dominate the storage requirements.
>
> These files represented the totality of files owned by students and faculty members on the Dept.'s UNIX machines.

p. 2, §2:
> The third column gives the data for 2005. Files are definitely larger now, with the median file size in 2005 being 2475 bytes and the percentage of files that are 'small' (10 1-KB disk blocks or fewer) being 73%. Furthermore, the largest file recorded was now 2 GB, more than 4000 times larger than in 1984.
>
> This system, which was at a commercial hosting service in upstate New York, had only 53,000 files (vs. 1.7 million at the VU).
>
> Put in other words, 10% of all files are 164 bytes or smaller, 20% of all files are 485 bytes are smaller, half of all files are 2475 bytes or smaller and 90% of all files are 56,788 bytes or smaller.

**Coverage.** T9(b) — **covers file sizes only.** Object: all user-owned files on a university department's UNIX file systems (≈1.7 million files, 2005) and, separately, a Linux web server (53 000 files). Statistic: file-size CDF by power of two and deciles (median 2 475 B; 90th percentile 56 788 B; max 2 GB). Population: students and faculty of the VU Amsterdam Computer Science Department. Platform: UNIX (department servers); the second data point is Linux but a web server. Date: 2005 (compared with 1984). Does not cover: per-user totals, types, compressibility, duplication, change.

**Observation status.** One snapshot per system; date named by year only.

---

### T9-S1-08 — Policroniades & Pratt, "Alternatives for Detecting Redundancy in Storage Systems Data" (USENIX ATC 2004)

**Citation.** Calicrates Policroniades, Ian Pratt (Computer Laboratory, Cambridge University), "Alternatives for Detecting Redundancy in Storage Systems Data", 2004 USENIX Annual Technical Conference, General Track.

**Copy read.** `https://www.usenix.org/legacy/event/usenix04/tech/general/full_papers/policroniades/policroniades.pdf`, accessed 2026-09-19, `sources/T9-S1-08/policroniades2004-redundancy.pdf`, 303 066 bytes, 15 pages, SHA-256 `5bc9c787deb94027eb8b3adc4c517f27a06ae6d80396c97458ce272a924f6284`.

**Passages.**

p. 8, §4.2:
> The data analysed in this section was held in 44 home directories of different users of the Computer Laboratory. Although the total amount of data processed was only 2.9 GB, this data set presented high diversity in the kind of files stored; we collected 1,756 different file-name extensions in 98,678 files with an average file size of 31 KB. […] Apart from the files without extension, home directories are mainly used to store files related to word processing and source code development. The 15 file-name extensions showed in Table 4 under the column related to storage space account for over 69% of the whole data set.
>
> In this case the percentage of identical data in whole files was 12.80%.
>
> Our results indicate that using the content-defined chunking method and an expected chunk size of 2 KB, which is the best case, a storage utility would maintain only 2.3 GB of the original 2.9 GB. This represents a storage space reduction of 20.6%. However, the compressed tar version of the data set used only 1.4 GB of disk space; considerably outperforming our best duplicate suppression scenario.

p. 9, Table 4 (storage-space column, rank: extension, % storage; extraction order as printed):
> 1 .ps 17.24 · 2 – 11.73 · 3 .gz 10.66 · 4 .pdf 6.16 · 5 .eps 4.58 · 6 .zip 4.13 · 7 .doc 3.13 · 8 .ppt 2.60 · 9 .obj 1.75 · 10 .xls 1.53 · 11 .tgz 1.29 · 12 .tex 1.25 · 13 .c 1.24 · 14 .so 1.19 · 15 .txt 1.04 · Total 69.52

p. 9, Table 5 (% of data in identical blocks, content-defined / fixed-size):
> 8 KB 24.16 17.22 · 4 KB 26.76 18.05 · 2 KB 29.30 19.25

**Coverage.** T9(b) — **covers**, including compressibility and duplication. Object: 44 users' home directories on a department file system. Statistics: 98 678 files, 2.9 GB, mean 31 KB, 1 756 extensions, extension shares by count and bytes (Table 4), whole-file duplicate share 12.80 %, sub-file duplicate share 17–29 % (Table 5), compressed tar 1.4 GB of 2.9 GB. Population: Cambridge University Computer Laboratory users. Platform: not named in the passages (a university Unix-style environment is implied by `.ps`, `.tex`, `.so`, not stated). Date: not stated (paper 2004). Does not cover: per-user totals, change between snapshots.

**Observation status.** One snapshot of one population; compression tool behind "compressed tar" not named in the passage.

---

### T9-S1-07 — Cox, Murray, Noble, "Pastiche: Making Backup Cheap and Easy" (OSDI 2002)

**Citation.** Landon P. Cox, Christopher D. Murray, Brian D. Noble (University of Michigan), "Pastiche: Making Backup Cheap and Easy", 5th Symposium on Operating Systems Design and Implementation (OSDI '02), December 2002.

**Copy read.** `https://www.usenix.org/legacy/event/osdi02/tech/full_papers/cox/cox.pdf`, accessed 2026-09-19, `sources/T9-S1-07/cox2002-pastiche.pdf`, 157 290 bytes, 15 pages (page 1 is the USENIX cover sheet), SHA-256 `e758b92589476e918dc9984712d0353d8b2ed79bdc3c6b47e8538ea170b8d03f`.

**Passages.**

p. 2, §1:
> Luckily, much of the data on a given machine is not unique, and is generated at install time. Furthermore, for most machines, common data will be shared widely. The default installation of Office 2000 Professional requires 217 MB; it is nearly ubiquitous and different installations are largely the same.

p. 10, §5.3:
> To answer the first question, we took the signatures of seventeen machines at Michigan. These machines run Windows, Linux, Solaris, and various flavors of BSD. We also took the signatures of two freshly installed machines. The first ran Windows 98 with an Office 2000 Professional installation, but without any service packs applied. This machine held roughly 90 thousand chunks. The second was a Linux machine running a Debian unstable release, configured as a conventional workstation with development and document processing tools. This machine held approximately 270 thousand chunks.

p. 11, §5.3:
> Interestingly, bnoble, a Windows 2000 machine, has a coverage rate for this Debian machine of almost 15%. This is because bnoble also has a stable release of Debian, installed in a VMware virtual machine

**Coverage.** T9(b) — **covers weakly (cross-machine duplication).** Object: content-defined chunk overlap between one fresh machine and each of 17 others. Statistic: coverage rate per host pair — values only in Figure 7 except the one quoted (≈15 %). Population: 17 machines at the University of Michigan. Platform: Windows, Linux (Debian), Solaris, BSD. Date: not stated (paper 2002). Does not cover: file counts, sizes, types, per-machine totals, compressibility, change over time.

**Observation status.** One signature collection; machines named by host name; window not named.

---

### T9-S1-16 — Dinneen, Julien, Frissen, "The Scale and Structure of Personal File Collections" (CHI 2019)

**Citation.** Jesse David Dinneen, Charles-Antoine Julien, Ilja Frissen, "The Scale and Structure of Personal File Collections", Proceedings of CHI 2019, paper 327, Glasgow, May 2019. DOI 10.1145/3290605.3300557.

**Copy read.** `http://library.usc.edu.ph/ACM/CHI2019/1proc/paper327.pdf`, accessed 2026-09-19 — a third-party library mirror (University of San Carlos) of the ACM CHI 2019 proceedings file; the page footer reads "CHI 2019 Paper · CHI 2019, May 4–9, 2019, Glasgow, Scotland, UK · Paper 327". `sources/T9-S1-16/dinneen2019-chi-paper327.pdf`, 1 169 044 bytes, 12 pages, SHA-256 `8dad2a4397413bdc485df7cb64642abb2e696f2e1fc1fa54e6b4c19840195161`.

**Passages.**

p. 3, §3:
> We recruited participants from February 2016 to August 2018 by posting calls for participation on study recruitment Websites and in online communities on Facebook and Reddit, sending emails to mailing lists (e.g., industrial, governmental, and academic), and contacting colleagues, friends, and family.

p. 3, §3:
> Any visible and accessible folders and files within such spaces were included in data collection, but locations outside of those specified (i.e., system folders) were not examined, nor were hidden folders (e.g., /Users/jesse/Library in MacOS and /home/jesse/.cache/ in Linux), nor folders that an unprivileged user could not access

p. 4, §4:
> We received 348 data files, all of which were usable, describing 49.2 million files across 7.9 million folders. […] Data came from a variety of machines (laptops, desktops, and tablets) with varied uses (personal matters, work and/or school, or a combination thereof) and operating systems (Windows XP to 10, MacOS 10.8 to 10.13, and eight Linux distributions).

p. 4, Table 2 (OS row): "MacOS 169 (48%) · Windows 135 (39%) · GNU/Linux 44 (13%)".

p. 5, Table 3 (*reader's layout reconstruction*; columns: measure, median*, mean*, SD*, (mean; SD); starred values are the authors' log-normal statistics):
> # files 29,123 193,001 6.99 (73,821; 72,996)
> # folders 3,818 26,363 7.14 (10,673; 12,011)
> total size (items) 33,900 221,826 6.95 (85,614; 83,756)
> total size (GB) 32.92 232.42 7.22 (92.46; 108.99)

**Coverage.** T9(b) — **covers.** Object: the user-managed part of a machine (home folder and user-chosen locations; system and hidden folders excluded — which is close to what a desktop user's backup reads). Units: files, folders, GB per collection. Statistics: typical range 29–193 thousand files and 32.9–232 GB per collection (log-normal median*/mean*); arithmetic mean 73 821 files and 92.46 GB after outlier removal. Population: 348 remote, self-selected participants (ages 14–64). Platform: macOS 48 %, Windows 39 %, GNU/Linux 13 %. Date: February 2016–August 2018. Does not cover: per-OS totals (not split in this paper), types (see T9-S1-18), sizes (see T9-S1-17), compressibility, content duplication, change over time.

**Observation status.** One snapshot per participant; participants anonymous; window named.

---

### T9-S1-18 — Dinneen & Julien, "What's in People's Digital File Collections?" (ASIS&T 2019; arXiv 2402.06421)

**Citation.** Jesse David Dinneen, Charles-Antoine Julien, "What's in People's Digital File Collections?", Proceedings of the 82nd Annual Meeting of the Association for Information Science & Technology 56(1):68–77, 2019 (journal reference as given on arXiv).

**Copy read.** Author preprint, `https://arxiv.org/pdf/2402.06421v1` (arXiv v1, posted 2024-02-09), accessed 2026-09-19, `sources/T9-S1-18/dinneen2019-asist-arxiv-2402.06421v1.pdf`, 269 645 bytes, 11 pages, SHA-256 `d4988a0a806b0ad51ad666f8d3bb23912352d45b45a4bcdb7f1d88bd9f0ba86a`.

**Passages.**

p. 5, Methodology:
> Following Henderson (2011), proportions of file and folder duplication within each collection was inferred by the presence of duplicate file and folder names.

p. 5, Results:
> We received data describing 348 collections, totalling 50 million files and nearly 8 million folders.
>
> The collected data contain 85,000 unique extensions, distributed in a highly skewed and long-tailed manner as observed in prior works (Douceur & Bolosky, 1999). Thus, despite our categorisation efforts accounting for less than 1% of the variety of extensions, and despite extensionless files comprising on average 10%, 83% of all files were categorised and on average only 7% of each collection was left uncategorised.
>
> Personal collections were, in typical cases, comprised of 45 thousand to 85 thousand files across 7 thousand to 21 thousand folders.

pp. 5–6, Results (the sentence runs across a footnote and the page break):
> Images and development files were the most common types at 22-29% and 4-35%, respectively (e.g., 20,000 image files and 12,000 development files, depending on collection size). Next most common were system, audio, and extensionless files at roughly 5-25% each (e.g., ~7,000 of each kind). The typical proportion of audio files varied greatly, however, from 1% to 20%. Unidentified files comprised 6-9% of collections, and text files 3-5% (e.g., ~2,000 text files). PIM and video files were relatively scarce (0-1%)

p. 6, Duplication results:
> Across all groups we observed that 23-34% of files in a collection were typically duplicated (excludes two outliers), while on average 44% (traditional mean) of folders were duplicated. IT collections exhibited the most duplication of files (40-48%), and personal collections the least (20-26%; p=0.002 when comparing to IT)

**Coverage.** T9(b) — **covers type mix and name-level duplication.** Object: same 348 user-managed collections as T9-S1-16. Unit: share of files by category (15 categories from 453 extensions). Statistics: typical ranges per collection type (personal, knowledge work, IT, other work, study); file-name duplication 23–34 % of files. Population, platform and date as T9-S1-16 (2016–2018; macOS/Windows/GNU/Linux). Does not cover: shares by bytes (counts only), content duplication (name-based, not hash-based), compressibility, per-OS split of types.

**Observation status.** One snapshot per participant; same data as T9-S1-16 and T9-S1-17 — not an independent observation.

---

### T9-S1-17 — Dinneen & Nguyen, "How Big Are Peoples' Computer Files? File Size Distributions Among User-managed Collections" (ASIS&T 2021; arXiv 2107.03272)

**Citation.** Jesse David Dinneen, Ba Xuan Nguyen, ASIS&T '21: Proceedings of the 84th Annual Meeting of the Association for Information Science & Technology, 58 (2021).

**Copy read.** Author preprint, `https://arxiv.org/pdf/2107.03272v1` (arXiv v1, 2021-07-07), accessed 2026-09-19, `sources/T9-S1-17/dinneen2021-arxiv-2107.03272v1.pdf`, 198 242 bytes, 7 pages, SHA-256 `bc87ee9bfaf17892ff4d6f49cde91222c5e50707e4b4a41bd3de4d6545392762`.

**Passages.**

p. 3, Methodology:
> Data Collection and Sample - 348 remote and anonymous participants downloaded and ran on their desktops and laptops open-source software (Dinneen et al. 2016) that collected data about files they indicated they manage. File sizes were measured in bytes using python's os.stat().st_size […] Care was taken to exclude files not managed by the participant: hidden files and common folders containing operating system files were explicitly ignored.

p. 3, Table 1: "348 participants · 49 million files · […] Mac OS (10.7 – 11): 169 (48%) · Windows (XP – 10): 135 (39%) · GNU/Linux: 44 (13%)".

p. 3, Results:
> Relatively small files are very common in each OS: files below ~5 KB account for 50% of Mac and Linux collections, and files below 8.5 KB account for 50% of files in Windows. However, the CDFs of each OS differ significantly (p<0.001) across all measures. Notably, the Mac distribution has more small files than Windows's, while Linux is so skewed (e.g., SD 145 MB, three times that of Windows) that its CDF resembles Mac's below 5 KB (i.e., such files are 50% of both CDFs) despite having more files above 64 KB than Windows.

p. 4, Table 2 (*reader's layout reconstruction*; columns: Data set / OS, Log-normal median & mean, Arithmetic mean, 50% occupied by (< mean)):
> whole data set 9.0 KB, 730 KB 1.5 MB < 5.4 KB
> Mac OS 8.0 KB, 533 KB 1.4 MB < 4.9 KB
> Windows 11.5 KB, 1.0 MB 1.7 MB < 8.3 KB
> GNU/Linux 10.8 KB, 1.7 MB 2.2 MB < 4.8 KB

p. 5, Discussion:
> RQ3. File sizes have grown more than ten-fold since the mid-2000s, but most files are still under 8 MB in size.

p. 3, Results (data availability, not fetched — published data is S3's class):
> Comprehensive CDF plots, full data tables with discrete values for each distribution, and all analysis scripts can be accessed at github.com/jddinneen/fm-results-tables.

**Coverage.** T9(b) — **covers file-size distribution per OS, with a GNU/Linux split.** Object: user-managed files (hidden and OS folders excluded). Unit: bytes per file. Statistics: per-OS log-normal median and mean, arithmetic mean, median-by-count (GNU/Linux: 10.8 KB / 1.7 MB log-normal, 2.2 MB arithmetic mean, 50 % of files < 4.8 KB). Population and date as T9-S1-16 (collected 2016–2018; paper 2021); GNU/Linux n = 44. Does not cover: bytes per collection per OS, types by bytes, compressibility, duplication, change.

**Observation status.** Same data as T9-S1-16/-18.

---

### T9-S1-22 — Gracia-Tinedo et al., "Dissecting UbuntuOne: Autopsy of a Global-scale Personal Cloud Back-end" (IMC 2015)

**Citation.** Raúl Gracia-Tinedo, Yongchao Tian, Josep Sampé, Hamza Harkous, John Lenton, Pedro García-López, Marc Sánchez-Artigas, Marko Vukolić, "Dissecting UbuntuOne: Autopsy of a Global-scale Personal Cloud Back-end", ACM Internet Measurement Conference (IMC '15), Tokyo, October 2015.

**Copy read.** `https://conferences.sigcomm.org/imc/2015/papers/p155.pdf`, accessed 2026-09-19, `sources/T9-S1-22/gracia-tinedo2015-imc-p155.pdf`, 7 591 561 bytes, 14 pages, SHA-256 `059434251b78fdaa7c1b9d0410d71212aaeb16d4d63684488ddedd87a65dd720`.

**Passages.**

p. 1, §1:
> In this paper, we present results of our study of U1: the Personal Cloud of Canonical, integrated by default in Linux Ubuntu OS. […] U1 provided service to 1.29 million users at the time of the study on January-February 2014

p. 5, Table 3: "Trace duration 30 days (01/11 - 02/10) · Trace size 758GB · Back-end servers traced 6 servers (all) · Unique user IDs 1, 294, 794 · Unique files 137.63M · User sessions 42.5M · Transfer operations 194.3M · Total upload traffic 105TB · Total download traffic 120TB".

p. 5, §4.1:
> Dataset limitations. The dataset only includes events originating from desktop clients. Other sources of user requests (e.g., the web front-end, mobile clients) are handled by different software stacks that were not logged.

p. 6, §5.1:
> For uploads, we found that 10.05% of total upload operations are updates, that is, an upload of an existing file that has distinct hash/size. However, in terms of traffic, file updates represent 18.47% of the U1 upload traffic.

p. 7, §5.3:
> We detected a dr of 0.171, meaning that 17% of files' data in the trace can be deduplicated
>
> To wit, 90% of files are smaller than 1MByte.
>
> It is worth noting that in general, incompressible files like zipped files or compressed media are larger than compressible files (docs, code).

p. 8, §5.3:
> Further, the Code category contains the highest fraction of files, indicating that many U1 users are code developers who frequently update such files, despite the storage space required for this category is minimal. Docs are also popular (10.1%), subject to updates and hold 6.9% of the storage

**Coverage.** T9(b) — **covers, for the synced subset of users' files.** Object: files uploaded/downloaded by Ubuntu desktop sync clients (not whole file systems). Statistics: 90 % of transferred files < 1 MB; cross-user whole-file duplicate share 17 %; category shares by count and storage (Figure 4c; Docs 10.1 % of files, 6.9 % of storage quoted). T9(c) — **partly**: 10.05 % of upload operations (18.47 % of upload bytes) are updates of existing files — sync-interval change, not backup-interval. Population: 1.29 million UbuntuOne users. Platform: Ubuntu Linux desktop clients. Date: 30 days, January–February 2014. Does not cover: per-user totals, full home-directory contents, compressibility as a number.

**Observation status.** One 30-day provider-side trace; window named.

---

### T9-S1-24 — El-Shimi et al., "Primary Data Deduplication – Large Scale Study and System Design" (USENIX ATC 2012)

**Citation.** Ahmed El-Shimi, Ran Kalach, Ankit Kumar, Adi Oltean, Jin Li, Sudipta Sengupta (Microsoft), 2012 USENIX Annual Technical Conference.

**Copy read.** `https://www.usenix.org/system/files/conference/atc12/atc12-final293.pdf`, accessed 2026-09-19, `sources/T9-S1-24/elshimi2012-atc12-final293.pdf`, 432 602 bytes, 12 pages, SHA-256 `92c719a0d802f162a6a94485afa22bb162bad642ebdf52ba14b48bcac81c50ba`.

**Passages.**

p. 1, abstract:
> File data was analyzed from 15 globally distributed file servers hosting data for over 2000 users in a large multinational corporation.

p. 2, §3.1 and Table 1 (row "Home Folders (HF)": Srvrs 8, Users 1867, Total Data 2.4TB, Locations US, Dublin, Amsterdam, Japan):
> Home Folder servers host the file contents of user home folders (Documents, Photos, Music, etc.) of multiple individual users. Each file in this workload is typically created, modified, and accessed by a single user.

p. 3, Table 2 (Dedup space savings: File Level, Chunk Level, Gap; average chunk size 64KB):
> HF-Amsterdam 1.9% 15.2% 8x · HF-Dublin 6.7% 16.8% 2.5x · HF-Japan 4.0% 19.6% 4.9x

p. 4, §3.2 (for the GFS-US group-file-share data set, not home folders):
> On the other hand, we find that roughly 31% of the chunks (42% of the bytes) do not compress at all

**Coverage.** T9(b) — **covers duplication of users' home-folder data**, server-hosted. Object: home-folder shares (Documents, Photos, Music) on corporate file servers. Statistic: whole-file dedup savings 1.9–6.7 %, chunk-level 15.2–19.6 % per site. Population: 1 867 users on 8 servers. Platform: Windows file servers. Date: not stated (paper 2012). Does not cover: per-user sizes, types, compressibility of home folders (the compressibility figure is for group shares), change over time.

**Observation status.** One scan per server; window not named.

---

### T9-S1-26 — Harnik, Kat, Margalit, Sotnikov, Traeger, "To Zip or not to Zip: Effective Resource Usage for Real-Time Compression" (FAST 2013)

**Citation.** Danny Harnik, Ronen Kat, Oded Margalit, Dmitry Sotnikov, Avishay Traeger (IBM Research–Haifa), 11th USENIX Conference on File and Storage Technologies (FAST '13); first printed page 229.

**Copy read.** `https://www.usenix.org/system/files/conference/fast13/fast13-final38.pdf`, accessed 2026-09-19, `sources/T9-S1-26/harnik2013-fast13-final38.pdf`, 1 181 315 bytes, 13 pages, SHA-256 `a3e90f62ad1eb8a5f90ff1f1f50962aa3b1cbe58a5da302c5d31d59868087a16`.

**Passages.** p. 7, §4:
> The file server data set contains home or project directories owned by different users, stored in 42 different back-end volumes. […] The file server and VM images data sets were sampled from active primary storage using the sampling techniques described in Section 3.

p. 8, Table 3 (columns: Data Set, Total Size, Compressed Size, Compression Saving, Zero Chunks, Comments):
> File server 37TB 15.2TB 17.5TB 4.6TB 42 volumes, 144K samples

**Coverage.** T9(b) — **covers compressibility, weakly.** Object: home or project directories on an enterprise file server, sampled. Statistic: 37 TB total, 15.2 TB compressed, 4.6 TB zero chunks (compressor for the estimate is the paper's own estimator; the passage does not name the algorithm). Population, organisation and date: not named. Platform: not named. Does not cover: per-user values, types, duplication, change.

**Observation status.** One sampled estimate; organisation and window not named.

---

### 2.2 Part (c) — real backup data

### T9-S1-05 — Vrable, Savage, Voelker, "Cumulus: Filesystem Backup to the Cloud" (FAST 2009)

**Citation.** Michael Vrable, Stefan Savage, Geoffrey M. Voelker (UC San Diego), 7th USENIX Conference on File and Storage Technologies (FAST '09); first printed page 225.

**Copy read.** `https://www.usenix.org/legacy/event/fast09/tech/full_papers/vrable/vrable.pdf`, accessed 2026-09-19, `sources/T9-S1-05/vrable2009-cumulus.pdf`, 227 303 bytes, 14 pages, SHA-256 `7ce5a31c975e09a97e311745544af8f92a026d4c1cb1c8a3710c522410dcfe83`.

**Passages.**

pp. 7–8, §5.1 (the last sentence runs across the page break):
> A fileserver trace tracks all files stored on our research group fileserver, and models the use of a cloud service for remote backup in an enterprise setting. A user trace is taken from the Cumulus backups of the home directory of one of the author's personal computers, and models the use of remote backup in a home setting. The traces contain a daily record of the metadata of all files in each setting, including a hash of the file contents. The user trace further includes complete backups of all file data, and enables evaluation of the effects of compression and sub-file incrementals.

p. 8, Table 2 (columns: Fileserver, User; "File counts and sizes are for the last day in the trace"):
> Duration (days) 157 223 · Entries 26673083 122007 · Files 24344167 116426 · File Sizes Median 0.996 KB 4.4 KB · Average 153 KB 21.4 KB · Maximum 54.1 GB 169 MB · Total 3.47 TB 2.37 GB · Update Rates New data/day 9.50 GB 10.3 MB · Changed data/day 805 MB 29.9 MB · Total data/day 10.3 GB 40.2 MB

p. 9, §5.2:
> The user workload has higher overheads relative to optimal due to smaller average files and more churn in the file data

p. 12, §5.4.2:
> We used as a sample the full data contained in the first day of the user trace: the uncompressed size is 1916 MB, the compressed tar size is 1152 MB (factor of 1.66), and files individually compressed total 1219 MB (1.57×), 5.8% larger than whole-snapshot compression.

p. 13, §5.4.4:
> File A is a frequently-updated Bayesian spam filtering database, about 90% of which changes daily. File B records the state for a file-synchronization tool (unison), of which an average of 5% changes each day

**Coverage.** T9(c) — **covers, for one personal machine.** Object: the home directory of one personal computer, backed up daily. Statistics: 116 426 files, 2.37 GB, median file 4.4 KB, mean 21.4 KB, max 169 MB; new data 10.3 MB/day and changed data 29.9 MB/day (total 40.2 MB/day) over 223 days; compressibility of the first full backup 1.66 (tar + compressor; §5.4.2 names gzip and bzip2 for segment compression, the passage does not say which gave 1.66). Also the research-group file server (3.47 TB, 9.50 GB new/day). T9(b) — the same trace gives one machine's size distribution. Population: one author's personal computer. Platform: not named. Date: not named (paper 2009). Does not cover: a population of users, types.

**Observation status.** One machine, one 223-day daily trace; machine and window not named.

---

### T9-S1-20 — Sun, Kuenning, Mandal, Shilane, Tarasov, Xiao, Zadok, "A Long-Term User-Centric Analysis of Deduplication Patterns" (MSST 2016)

**Citation.** Zhen Sun, Geoff Kuenning, Sonam Mandal, Philip Shilane, Vasily Tarasov, Nong Xiao, Erez Zadok, 32nd IEEE Conference on Mass Storage Systems and Technologies (MSST 2016) (venue as worded on the copy's banner).

**Copy read.** `https://www.fsl.cs.stonybrook.edu/docs/msst16dedup-study/data-set-analysis.pdf` (lab copy; first-page banner "Appears in the proceedings of the 32nd IEEE Conference on Mass Storage Systems and Technologies (MSST 2016)"), accessed 2026-09-19, `sources/T9-S1-20/sun2016-msst-data-set-analysis.pdf`, 405 845 bytes, 7 pages, SHA-256 `3b2e71f99d41fa7dac422c5324fcd3275701192eaed1e3610eab201c22d2e1c6`.

**Passages.**

p. 1, abstract:
> For this paper, we collected 21 months of data from a shared user file system; 33 users and over 4,000 snapshots are covered.

p. 2, §III:
> The Homes data set contains almost-daily snapshots of our users' home directories on a shared file system; we collected one daily snapshot per user for a total of over 4,000 snapshots. The users are all Linux systems software developers who work on several joint projects.

p. 2, Table I: "03/09/2012–11/23/2014 · 4,181 dailies (about 21 months) · […] Number of logical chunks 1.9×10^10 (2KB chunk size) [extracted "1.9×1010"] · 4.0×10^8 (128KB chunking) · Number of unique chunks 9.8×10^7 (2KB chunk size) · 3.3×10^6 (128KB chunking)".

p. 3, §IV-A:
> For this paper we chose three typical backup strategies: Full, Incremental, and Weekly-Full (a full backup each Saturday and incrementals for the rest of the week). Since full snapshots were collected daily, they inherently represent full backups. For incremental and weekly-full backups we needed to detect newly added and modified files. By comparing two consecutive snapshots we identified whether a file was newly added. By checking the mtime we determined the files that were modified since the previous snapshot.

p. 3, Table II, raw deduplication ratios (columns: Full backup, Incremental backup, Weekly-full backup):
> 2KB 218.5 13.6 42.8 · 4KB 197.0 12.6 39.4 · 8KB 181.9 11.7 36.5 · 16KB 167.4 10.7 33.6 · 32KB 153.3 9.8 30.8 · 64KB 139.1 8.9 27.9 · 128KB 128.0 8.2 25.7 · WFC 16.4 1.1 2.3

p. 3, §IV-B:
> The upper line of Figure 1 shows that more than 99% of the files are smaller than 1MB, but the lower line demonstrates that in aggregate, these small files consume less than 4% of total space.

p. 4, §IV-B:
> Figure 3 shows the percentage of total space occupied by various common file types; we can see that virtual machine images (vmdk) consume nearly 60% of the entire data size.
>
> However, the average file size in our data set is 366KB due to large vmdk files.

p. 4, §IV-C:
> user 15 has both the longest duration (20 months) and the largest data-set size (8.3TB).

**Coverage.** T9(c) and T9(b) — **covers.** Object: daily snapshots (chunk hashes and metadata) of users' home directories on a shared server. Statistics: dedup ratios for full / incremental / weekly-full backup strategies by chunk size; file-size distribution (> 99 % of files < 1 MB holding < 4 % of bytes; mean 366 KB); byte share by type (vmdk ≈ 60 %). Population: 33 Linux systems-software developers ("our users" — the authors' group; the copy is hosted by the Stony Brook File Systems and Storage Lab). Platform: Linux users; data on a shared file server, not on personal machines. Date: 9 March 2012–23 November 2014. Does not cover: compressibility (stated in §III-C: content not recorded), bytes changed per day as a number (derivable from the published data set, which is S3's class), per-user home size except the largest.

**Observation status.** One long-term trace of one group; window named. The same Homes data set underlies T9-S1-21. Tarasov et al.'s "Home" (T9-S1-19), from the same research group, is described as weekly snapshots of students' home directories; the passages do not say whether it is the same collection.

---

### T9-S1-21 — Sun et al., "Cluster and Single-Node Analysis of Long-Term Deduplication Patterns" (ACM TOS 2018)

**Citation.** Zhen "Jason" Sun, Geoff Kuenning, Sonam Mandal, Philip Shilane, Vasily Tarasov, Nong Xiao, Erez Zadok, ACM Transactions on Storage 14(2), Article 13, 2018. DOI 10.1145/3183890.

**Copy read.** `https://www.fsl.cs.sunysb.edu/docs/msst16dedup-study/tos17dedup-study-a13-sun.pdf`, accessed 2026-09-19, `sources/T9-S1-21/sun2018-tos-a13.pdf`, 2 183 287 bytes, 28 pages, SHA-256 `3fc4e33fa6dc4b06af5dd05f2e1b518cb979ab576d8c44b08be98e9ef6685947`.

**Passages.**

p. 6, Table 1 ("Features of the Homes data set"):
> Total size 456TB · Start and end time 03/09/2012–11/23/2014 · Number of users 33 · Number of snapshots 4,181 dailies (about 21 months) · […] Number of files 1.3×10^9 [extracted "1.3⇥109"] · Number of logical chunks 1.9×10^11 (2KB chunk size) [extracted "1.9⇥1011"]

p. 11, §4.2:
> The main reason for this phenomenon is that most of these file types store compressed data. In a software-development environment, these files are rarely changed.

p. 12, §4.3:
> the largest user's data (62TB) is about three orders of magnitude larger

**Coverage.** T9(c) — extended version of T9-S1-20; adds the logical total over all daily snapshots (456 TB, 1.3×10^9 file instances) and retention-policy simulations (Figures 2–3, values not quoted). Note for the downstream reader: the two versions differ on figures that should be the same — logical chunks at 2 KB (1.9×10^10 in MSST, 1.9×10^11 in TOS) and the largest user's data (8.3 TB in MSST, 62 TB in TOS); neither text explains the change. Population, platform, date as T9-S1-20.

**Observation status.** Same data as T9-S1-20.

---

### T9-S1-19 — Tarasov, Mudrankit, Buik, Shilane, Kuenning, Zadok, "Generating Realistic Datasets for Deduplication Analysis" (USENIX ATC 2012)

**Citation.** Vasily Tarasov, Amar Mudrankit, Will Buik, Philip Shilane, Geoff Kuenning, Erez Zadok (Stony Brook University, Harvey Mudd College, EMC), 2012 USENIX Annual Technical Conference.

**Copy read.** `https://www.usenix.org/system/files/conference/atc12/atc12-final129.pdf`, accessed 2026-09-19, `sources/T9-S1-19/tarasov2012-atc12-final129.pdf`, 380 378 bytes, 12 pages, SHA-256 `5399826b46dc3367a1e971d7fdd4f93fe38a1f4096666206aaa9449a61307733`.

**Passages.**

p. 4, §4:
> Home: Weekly snapshots of students' home directories from a shared file system. The files consisted of source code, binaries, office documents, virtual machine images, and miscellaneous files.

p. 4, Table 1 (row Home; columns: Total size (GB), Total files (thousands), Snapshots & period, Avg. snapshot size (GB), Avg. number of files in a snapshot (thousands)):
> Home 3,482 15,352 15 weekly 227 1,023

p. 6, §5.2:
> Analysis of our datasets showed that the file sets defined above remain relatively stable. Files that were unmodified between snapshots F0 →F1 tended to remain unmodified between snapshots F1 →F2.
>
> The Markov model allows us to accurately capture the rates of file appearance, deletion, and modification in the trace. Table 2 presents the average transition probabilities observed for our datasets. As mentioned earlier, in all datasets files often remain Unchanged, and thus the probabilities of UU transitions are high.

p. 7, Table 2 (*reader's layout reconstruction*; "Probabilities (in percents) of file state transitions for different datasets. N: new file appearance. D: file deletion."; columns N NM NU ND MU MD MM UM UD UU DN D):
> Home 4 2 78 20 54 10 36 0.14 0.35 99.51 6 0.50

**Coverage.** T9(c) — **covers change between consecutive weekly snapshots, in file-state terms.** Object: weekly snapshots of students' home directories (average snapshot 227 GB, 1.02 million files). Statistics: per-transition probabilities (an unmodified file stays unmodified with 99.51 %, is modified with 0.14 %, deleted with 0.35 %; new-file and deletion rates 4 % and 0.50 %). Population: students; the institution is not named — p. 4 says the six data sets are "two commonly used public datasets, two collected locally, and two originally presented by Dong et al. [6]", and by elimination against the list (Kernels and CentOS public; System Logs and Sources also appear in T9-S1-29) Home is one of the locally collected ones (reader's inference). Platform: not named. Date: not named. Does not cover: bytes changed per snapshot, compressibility, types by bytes.

**Observation status.** One 15-week trace; window not named.

---

### T9-S1-27 — Meister & Brinkmann, "Multi-level Comparison of Data Deduplication in a Backup Scenario" (SYSTOR 2009) — authors' slides

**Citation.** Dirk Meister, André Brinkmann (Paderborn Center for Parallel Computing, University of Paderborn), "Multi-level Comparison of Data Deduplication in a Backup Scenario", Proceedings of the 2nd Israeli Experimental Systems Conference (SYSTOR), pages 8:1–8:12, ACM, 2009 (as listed in T9-S1-28's publication list, p. 9, entry [MB09]; the paper is on the ACM DL and was not open). What was read is the authors' conference slide deck.

**Copy read.** `https://www.systor.org/2009/papers/2_1_3.pdf`, accessed 2026-09-19, `sources/T9-S1-27/meister2009-systor-2_1_3.pdf`, 744 232 bytes, 35 pages (PyMuPDF count), SHA-256 `06241376f3c6dcbddce8096ea079a2caca1553e93cf62141aa5af01c8fbb39fe`.

**Passages.**

slide 11 ("Real Life System"):
> User directories of the University of Paderborn · Weekly measurements · Key Facts – 450 GB data – 3.6M files – 8.000 active users

slide 21 ("Conclusion"):
> Large-Scale: – ≈ 35% internal redundancy (CDC-8) – Advantage for Content-defined Chunking – > 98,5% temporal redundancy (all) – High variation between weeks

**Coverage.** T9(c) — **covers.** Object: weekly full backups of a university home-directory file server. Statistics: 450 GB, 3.6 million files; ≈ 35 % redundancy within one backup (content-defined chunking, 8 KB); > 98.5 % redundancy against the previous week; per-type and per-size redundancy in figures (slides 13–15, values not quoted). Population: 8 000 active users. Platform: not named. Date: not named on the slides (T9-S1-28 dates the collection to 2008). Does not cover: compressibility, type mix by bytes.

**Observation status.** One weekly series; slide-level detail only.

---

### T9-S1-28 — Meister, "Advanced Data Deduplication Techniques and their Application" (dissertation, Johannes Gutenberg-Universität Mainz, 2013)

**Citation.** Dirk Meister, Dissertation, Fachbereich Physik, Mathematik und Informatik, Johannes Gutenberg-Universität Mainz, März 2013 (D77).

**Copy read.** `https://openscience.ub.uni-mainz.de/server/api/core/bitstreams/95550a44-1af1-4b52-bde8-e83374ee915f/content`, accessed 2026-09-19, `sources/T9-S1-28/meister-mainz-openscience.pdf`, 12 547 119 bytes, 254 pages, SHA-256 `8c64fc86a037933a067bff3428cd74fdf541b8442fa4a176d220a23d2e3589f9`.

**Passages.**

p. 36, §2.4:
> upb: The first data set is based on the home directory file server of the University of Paderborn, which has been collected in 2008 [MB09]. It is a time series containing 15 weekly full backup traces of the same file system of around 440 GB (6.6 TB total). With data deduplication, the data set size can be reduced by a factor of 1:20 to 369 GB.
>
> jgu: The second data set contains trace data from a home directory file server at the Johannes Gutenberg University Mainz. This data set, which has been collected in 2012, consists of 13 weekly backups forming a total data set of 16.1 TB. Data deduplication compresses the backup data set to 1.4 TB (factor 1:11.5).

p. 37, Table 1 ("Statistics about the backup data sets"; columns UPB, JGU, ENG; "All values are the total over all backup runs"):
> Total File Count 53,605,162 30,744,985 256,207 · Total Capacity 6.6 TB 16.1 TB 318.7 GB · Capacity After Deduplication 369.0 GB 1.4 TB 8.0 GB · Mean File Size 132.4 KB 700.3 KB 1.3 MB · Median File Size 1.0 KB 13.50 KB 31.6 KB · Cumulated Median File Size 7.7 GB 42.9 GB 1.5 GB

p. 37, §2.4:
> eng: The third data set contains fingerprints of files from a file server of an engineering department of a private company backed up over 21 weeks in 2011/2012 (319 GB total).

p. 80, §8:
> The data sets introduced in Section 2.4 have a weekly deduplication ratio of 98% or higher in most weeks.

p. 96, §10.4:
> On the other hand, the UPB data set contains only 0.6% zero-chunks and the JGU data set contains only 0.3%.

**Coverage.** T9(c) — **covers.** Object: weekly full backups of two university home-directory file servers (and one company engineering file server). Statistics: per-backup size (UPB ≈ 440 GB; JGU 16.1 TB over 13 backups), file counts, mean and median file size, dedup factors (1:20, 1:11.5), week-by-week inter-backup deduplication ≥ 98 % in most weeks (Figure 7 plots 93–100 %). Population: University of Paderborn (2008) and Johannes Gutenberg University Mainz (2012) home directories; users not counted in these passages. Platform: not named. Does not cover: compressibility, type mix.

**Observation status.** Three named weekly series; years named.

---

### T9-S1-06 — Lillibridge et al., "Sparse Indexing: Large Scale, Inline Deduplication Using Sampling and Locality" (FAST 2009)

**Citation.** Mark Lillibridge, Kave Eshghi, Deepavali Bhagwat, Vinay Deolalikar, Greg Trezise, Peter Camble (HP Labs), 7th USENIX Conference on File and Storage Technologies (FAST '09); first printed page 111.

**Copy read.** `https://www.usenix.org/legacy/event/fast09/tech/full_papers/lillibridge/lillibridge.pdf`, accessed 2026-09-19, `sources/T9-S1-06/lillibridge2009-sparse-indexing.pdf`, 583 492 bytes, 13 pages, SHA-256 `dc009964befe62d0a7267607da4d0da2315b36acbd4d41584ad7cb38b837ed22`.

**Passage.** p. 6, §4.2:
> The first data set, which we call Workgroup, is composed of a semi-regular series of backups of the desktop PCs of a group of 20 engineers taken over a period of three months. Although the original collection included only an initial full and later weekday incrementals for each machine, we have generated synthetic fulls at the end of each week for which incrementals are available by applying that week's incrementals to the last full. […] Altogether, there are 154 fulls and 392 incrementals in this 3.8 TB data set, which consists of each of these backup snapshots tar'ed up without compression in the order they were taken. We believe this data set is representative of a small corporate workgroup being backed up via tar directly to a NAS interface.

**Coverage.** T9(c) — **covers the size of desktop backups, coarsely.** Object: tar backups (full and weekday incremental) of 20 desktop PCs. Statistic: 154 fulls + 392 incrementals = 3.8 TB. Population: a corporate engineering workgroup (HP). Platform: not named. Date: not named. Does not cover: per-backup size split (see T9-S1-10), change per incremental, types, compressibility.

**Observation status.** One collection; duration stated as three months here and four months in T9-S1-10.

---

### T9-S1-10 — Lillibridge, Eshghi, Bhagwat, "Improving Restore Speed for Backup Systems that Use Inline Chunk-Based Deduplication" (FAST 2013)

**Citation.** Mark Lillibridge, Kave Eshghi, Deepavali Bhagwat, 11th USENIX Conference on File and Storage Technologies (FAST '13); first printed page 183.

**Copy read.** `https://www.usenix.org/system/files/conference/fast13/fast13-final124.pdf`, accessed 2026-09-19, `sources/T9-S1-10/lillibridge2013-restore.pdf`, 636 610 bytes, 15 pages, SHA-256 `c956bc8469b28c7de60c5faebffadd2f767a308cdeb2b85756ea1c8aa1151825`.

**Passage.** p. 5, §4.2:
> The first data set, which we call Workgroup, is created from a semi-regular series of backups of the desktop PCs of a group of 20 engineers taken over a period of four months. The backups were taken using uncompressed tar. […] There are 154 fulls and 392 incrementals in this 3.8 TB collection, with the fulls ranging from 3 GB to 56 GB, with a mean size of 21 GB.

**Coverage.** T9(c) — **covers full-backup size per desktop**: 3–56 GB, mean 21 GB, for the same Workgroup collection as T9-S1-06. Population, platform, date as T9-S1-06 (not named). Does not cover: incremental sizes, types, compressibility. Note: the two HP papers give the collection period as three months (2009) and four months (2013).

**Observation status.** Same data as T9-S1-06.

---

### T9-S1-03 — Wallace et al., "Characteristics of Backup Workloads in Production Systems" (FAST 2012)

**Citation.** Grant Wallace, Fred Douglis, Hangwei Qian, Philip Shilane, Stephen Smaldone, Mark Chamness, Windsor Hsu (EMC Backup Recovery Systems Division), 10th USENIX Conference on File and Storage Technologies (FAST '12).

**Copy read.** `https://www.usenix.org/system/files/conference/fast12/wallace2-9-12.pdf`, accessed 2026-09-19, `sources/T9-S1-03/wallace2012-backup-workloads.pdf`, 228 990 bytes, 16 pages, SHA-256 `436619c8df7504a782b47a06787877e08e76baa35e5c1c57d0c5771ce0e1e797` (identical to the copy recorded as S1-15 in `S1-literature.md`, where it was marked context for T1).

**Passages.**

p. 1, abstract:
> we present a comprehensive characterization of backup workloads by analyzing statistics and content metadata collected from a large set of EMC Data Domain backup systems in production use. This analysis is both broad (encompassing statistics from over 10,000 systems) and deep (using detailed metadata traces from several production systems storing almost 700TB of backup data).

p. 5, §4:
> We have analyzed the autosupport information from more than 10,000 production deduplicated filesystems, taken from an arbitrary week, July 24, 2011.

p. 6, §4.4:
> Filesystem churn is a measure of the percentage of storage that is freed and then written per time period, for instance in a week. […] On average about 21% of the total stored data is freed and written per week. This high churn rate is driven by backup retention periods.

p. 8, Figure 9 legend: "O Mean = 10.9x · X Median = 8.7x" (deduplication ratio, backup 2011).

p. 9, §4.8.1 and Figure 10 legend ("O Mean = 1.9x · X Median = 1.7x", local compression ratio):
> Figure 10 shows the local compression we see across production backup workloads, with a mean value of almost 2X as the expected rule of thumb [19].

p. 9, Table 1 (*reader's layout reconstruction*; columns: #, Snapshot, Class, Data Type, Size (TB), Dedup. Ratio, 1-Wk Dedup., MedAge (Weeks), Retention Time, Update Freq.):
> 1 homedirs LT-B Home Directories 201 14.0 3.0 3.49 1–3 years / 5 weeks MF / DF
> 6 mixed2 B Workstations, Servers 43 11.0 3.0 9.44 4–6 months WF/DI
> 7 workstations B Workstations 4.5 7.5 2.3 13.56 4 months WF/DI

p. 9, §5:
> The former estimates the average deduplication seen within a single week, which typically includes a full backup plus incrementals.

**Coverage.** T9(c) — **covers, appliance-side.** Object: backup streams as stored on deduplicating appliances (tar-like aggregates), including data sets labelled "Home Directories" and "Workstations". Statistics: dedup ratio across >10 000 systems (mean 10.9×, median 8.7×), local compression after dedup (mean 1.9×, median 1.7×), weekly churn (mean ≈ 21 %, retention-driven: bytes freed and written per week on the appliance, not bytes changed at the source), per-data-set 1-week dedup (workstations 2.3, home directories 3.0). Population: EMC Data Domain customers (enterprise) and eight named traces. Platform: not named. Date: week of 24 July 2011. Does not cover: what a single desktop's backup contains (types, file sizes at the source), source-side change between consecutive backups.

**Observation status.** One week of autosupports plus eight traces; window named for the autosupports.

---

### T9-S1-04 — Amvrosiadis & Bhadkamkar, "Identifying Trends in Enterprise Data Protection Systems" (USENIX ATC 2015)

**Citation.** George Amvrosiadis (University of Toronto), Medha Bhadkamkar (Symantec Research Labs), 2015 USENIX Annual Technical Conference; first printed page 151.

**Copy read.** `https://www.usenix.org/system/files/conference/atc15/atc15-paper-amvrosladis.pdf` (file name as linked from the USENIX presentation page), accessed 2026-09-19, `sources/T9-S1-04/amvrosiadis2015-atc15-paper-amvrosladis.pdf`, 581 139 bytes, 15 pages, SHA-256 `af88ff1a5bdc3d7309ee8b24caddedceb7eb4f864f038f0657bb094e0230f3bb`.

**Passages.**

p. 2, abstract:
> In this paper, we present a study of 40,000 enterprise data protection systems deploying Symantec NetBackup, a commercial backup product. In total, we analyze over a million weekly reports which have been collected over a period of three years.

p. 4, §2.2:
> Clients can be desktops, servers, or virtual machines generating data that is protected by the backup system against failures.

p. 5, §3:
> The reports contain no personal identifiable information, or details about the data being backed up.
>
> The telemetry reports in our dataset were collected over the span of 3 years (January 2012 to December 2014), across two major versions of the NetBackup software. We collected 1 million reports from over 40,000 server installations deployed in 124 countries, on most modern operating systems.

p. 10, Figure 13 legend (average gigabytes transferred per job, after client-side deduplication): "Management operations (Mean: 32.9GB) · Incremental backups (Mean: 34.9GB) · Full backups (Mean: 47.1GB) · Recovery operations (Mean: 51.8GB)"; Figure 14 legend (average number of files transferred per job): "Incremental backups (Mean: 52033 files) · (Mean: 75916 files) [full backups] · Recovery operations (Mean: 73223 files)".

p. 10, §6.1:
> Surprisingly, incremental backups resemble full backups in size. Although the distribution of full backups is skewed toward larger job sizes, 29% of full backups on domains that also perform incremental backups tend to be equal or smaller in size than the latter, 21% range from 1 −1.5 times the size of incremental backups, and the remainder range from 1.5 −10^6 [extracted "106"] times. […] Third, maintenance applications, such as anti-virus scanners, can update file metadata making unchanged files appear modified.

p. 11, §6.2:
> Across all domains in our dataset, however, the average daily deduplication ratio is 88-89%, for both full and incremental backups.

**Coverage.** T9(c) — **covers job sizes and file counts, enterprise.** Object: NetBackup jobs (bytes and files transferred per full and incremental backup, per domain average). Statistics: mean incremental 34.9 GB / 52 033 files; mean full 47.1 GB / 75 916 files; dedup 88–89 %. Population: 40 000 enterprise backup domains in 124 countries; clients may be desktops, servers or VMs, not separated. Platform: "most modern operating systems" (not split). Date: January 2012–December 2014. Does not cover: content types, compressibility, anything specific to desktops.

**Observation status.** Telemetry over three years; one product; the data backed up is not visible to the authors (stated).

---

### T9-S1-29 — Dong, Douglis, Li, Patterson, Reddy, Shilane, "Tradeoffs in Scalable Data Routing for Deduplication Clusters" (FAST 2011)

**Citation.** Wei Dong (Princeton University), Fred Douglis (EMC), Kai Li (Princeton University and EMC), Hugo Patterson (EMC), Sazzala Reddy (EMC), Philip Shilane (EMC), 9th USENIX Conference on File and Storage Technologies (FAST '11).

**Copy read.** `https://www.usenix.org/legacy/event/fast11/tech/full_papers/Dong.pdf`, accessed 2026-09-19, `sources/T9-S1-29/dong2011-fast11-Dong.pdf`, 226 238 bytes, 15 pages, SHA-256 `a1c4fa73d032c672d52477837b2050a8a54ed31475444022c974293786d807e8`.

**Passages.** p. 6, §4.1:
> Collection 2: Backups from approximately 50 engineering workstations with 4 months of retention and servers with 6 months of retention.
>
> Workstations: Backups from 16 workstations used for build and test.
>
> Home Directory: Backups from engineers' home directories, containing source code, office documents, etc. Full backups were created weekly.

p. 6, Table 1 (*reader's layout reconstruction*; columns: Name, Total (GB), Peak (GB), Dedup., Months; "Deduplication ratios are obtained from a single-node system"):
> Collection 2 44,536 1,536 11.5 4–6 · Workstations 4,926 200 5.6 6 · Home Dirs. 12,907 855 19.3 3

**Coverage.** T9(c) — **covers, enterprise, coarse.** Object: backup streams of EMC-internal workstations and engineers' home directories. Statistics: total logical size, daily peak, single-node dedup (workstations 5.6×, home directories 19.3×). Population: EMC production backup servers. Platform, date: not named. Does not cover: per-machine sizes, types, compressibility, change per backup.

**Observation status.** Named data sets; window not named.

---

### T9-S1-30 — Lin, Lu, Douglis, Shilane, Wallace, "Migratory Compression: Coarse-grained Data Reordering to Improve Compressibility" (FAST 2014)

**Citation.** Xing Lin (University of Utah), Guanlin Lu, Fred Douglis, Philip Shilane, Grant Wallace (EMC Corporation — Data Protection and Availability Division), 12th USENIX Conference on File and Storage Technologies (FAST '14), Santa Clara, February 2014; first printed page 257.

**Copy read.** `https://www.usenix.org/system/files/conference/fast14/fast14-paper_lin.pdf`, accessed 2026-09-19, `sources/T9-S1-30/lin2014-fast14-paper_lin.pdf`, 502 251 bytes, 16 pages, SHA-256 `ce31e5ae9dd831f48eefa5c5593d6e2e73f22ca6be7501b6cfee115c74373e27`.

**Passages.** p. 8, §4.3:
> We use four single backup image files taken from production deduplication backup appliances. Two are backups of workstations while the other two are backups of Exchange email servers.

p. 8, Table 1 (*reader's layout reconstruction*; "Dataset summary: size, deduplication factor of 8 KB variable chunking and compression ratios of standalone compressors"; columns: Type, Name, Size (GB), Dedupe (X), gzip, bzip2, 7z, rzip):
> Workstation Backup WS1 17.36 1.69 2.70 3.22 4.44 4.46
> Workstation Backup WS2 15.73 1.77 2.32 2.61 3.16 3.12

**Coverage.** T9(c) — **covers compressibility of a workstation backup image.** Object: two single workstation backup images (tar-like, 17.36 and 15.73 GB). Statistics: within-image dedup 1.69–1.77×; compression factor gzip 2.32–2.70, bzip2 2.61–3.22, 7z 3.16–4.44, rzip 3.12–4.46. Population: EMC production appliances; workstation owners, OS and date not named. Does not cover: types, change between backups.

**Observation status.** Two images; source machines not named.

---

### T9-S1-33 — Li, Xu, Ng, Lee, "Efficient Hybrid Inline and Out-of-line Deduplication for Backup Storage" (arXiv 1405.5661)

**Citation.** Yan-Kit Li, Min Xu, Chun-Ho Ng, Patrick P. C. Lee (The Chinese University of Hong Kong), arXiv:1405.5661v1 [cs.DC], 22 May 2014.

**Copy read.** `https://arxiv.org/pdf/1405.5661v1`, accessed 2026-09-19, `sources/T9-S1-33/li2014-arxiv-1405.5661v1.pdf`, 331 087 bytes, 21 pages, SHA-256 `1ad53d6ee21651be9f6f37f498b7c4bead0c02e6b556cbf2f37e07f7df2df7e1`.

**Passages.** p. 10–11, §4.1:
> We also consider a real-world dataset taken from the snapshots of VM images used by university students in a programming course. We prepared a master image of 7.6GB installed with Ubuntu 10.04 and assigned it to each student to work on three programming assignments over a 12-week span. We took weekly snapshots for the VMs. […] Our evaluation selects a subset of 80 VMs covering a total of 960 weekly full backups. The total size is 7.2TB with 3.3TB of non-zero blocks.

p. 12, §4.3:
> For the real-world dataset VM, RevDedup achieves a saving of 96.3~97.1%, which is close to 98.3% achieved by Conv. In particular, segment-level inline deduplication saves at least 90% of space, since most system files remain unchanged in the VM images.

**Coverage.** T9(c) — **covers weekly full backups of Linux desktop VMs.** Object: whole-disk images of student Ubuntu 10.04 VMs (7.6 GB master image), weekly. Statistics: 960 weekly fulls, 7.2 TB (3.3 TB non-zero), dedup saving 96.3–98.3 % across the series. Population: 80 students' VMs at CUHK. Platform: Ubuntu 10.04. Date: not named (12-week course; paper 2014). Does not cover: home-directory contents apart from the VM image, types, compressibility; the authors state it is not representative of general virtual desktops.

**Observation status.** One course's VMs; window length named, dates not.

---

## 3. Read and found not to be candidates

- **T9-S1-09 — Bolosky, Corbin, Goebel, Douceur, "Single Instance Storage in Windows 2000" (4th USENIX Windows Systems Symposium, 2000).** Copy `https://www.usenix.org/legacy/events/usenix-win2000/full_papers/bolosky/bolosky.pdf`, accessed 2026-09-19, `sources/T9-S1-09/bolosky2000-sis.pdf`, 120 601 bytes, 12 pages, SHA-256 `1ba0b52e837f6d67ae58b2c0849ac65bb84eed9ce2949a46261e2f837ecb9a79`. Its only desktop-content statement (p. 10: "In [Bolosky 00] we measured the contents of a number of desktop personal computer file systems at Microsoft … Grouping 100 randomly selected file systems gave a little better than 30% space savings. At 1000 file systems the savings was just under 50%.") restates T9-S1-12, which was fetched as the primary. Its own measurement is of a remote-install server. Not a candidate.
- **T9-S1-23 — Pradeep Ganesan, "Read Performance Enhancement in Data Deduplication for Secondary Storage" (MS thesis, University of Minnesota, May 2013).** Copy `https://conservancy.umn.edu/server/api/core/bitstreams/15d8ca76-0f90-454e-bea6-a0feb846569f/content`, accessed 2026-09-19, `sources/T9-S1-23/park-thesis-umn-conservancy.pdf` (file name from the search that located it; the thesis is Ganesan's), 1 301 453 bytes, 50 pages, SHA-256 `94fc113323af443e08591672d68cec349a47842778bd8f301bc0729e9c4f65bf`. Its data sets are "trimmed versions" of traces, 8–20 GB each; the one home-directory set is described only as "DS#5 is home directory data of several users" (p. 28). A restore-performance study, not a characterisation. Not a candidate.
- **T9-S1-25 — Allu, Douglis, Kamat, Prabhakar, Shilane, Ugale, "Can't We All Get Along? Redesigning Protection Storage for Modern Workloads" (USENIX ATC 2018).** Copy `https://www.usenix.org/system/files/conference/atc18/atc18-allu.pdf`, accessed 2026-09-19, `sources/T9-S1-25/allu2018-atc18-allu.pdf`, 779 228 bytes, 14 pages, SHA-256 `97c276ffc592809f315f61eafb7c38a5107eda5e8893858a47d23d898cd83d99`. A storage-appliance caching design for non-sequential workloads; grep for churn, incremental, compression finds no characterisation of backup contents. Not a candidate.
- **T9-S1-34 — Han Yang, Guangjun Qin, Yongqing Hu, "Compression Performance Analysis of Different File Formats" (arXiv 2308.12275v1, 2023).** Copy `https://arxiv.org/pdf/2308.12275v1`, accessed 2026-09-19, `sources/T9-S1-34/arxiv-2308.12275v1.pdf`, 882 773 bytes, 18 pages, SHA-256 `c4f5cce72c7aeb0333504dd4b2f6d3362e39bbd3a75172b1c7e7a6039f5e7b9e`. Abstract (p. 1): "22 file formats with approximately 178GB of data were collected and the Zlib algorithm was used for compression experiments". A collected per-format corpus, not a study of what personal file systems contain — it belongs to part (d) (S2/S3), not to (b) or (c). Not a candidate here.
- **T9-S1-35 — Sean Rhea (Meraki), Russ Cox, Alex Pesterev (MIT CSAIL), "Fast, Inexpensive Content-Addressed Storage in Foundation" (USENIX '08: 2008 USENIX Annual Technical Conference, per the copy's page footer).** Copy `https://www.usenix.org/legacy/event/usenix08/tech/full_papers/rhea/rhea.pdf`, accessed 2026-09-19, `sources/T9-S1-35/rhea2008-foundation.pdf`, 221 793 bytes, 14 pages, SHA-256 `a93d4cc7efb07c5f4114bb9d37ed4fc98d2eec93994f8dfb9378158fe572e78f`. Its archival evaluation uses "sixteen months of nightly snapshots using traces derived from our research group's" file server (p. 9), not a personal machine, and reports throughput, not contents. Not a candidate.

## 4. Not found

- **(b) A population study of Linux desktop or laptop file systems.** No paper surveys whole Linux personal machines across a population. What exists with Linux: 44 GNU/Linux user-managed collections within Dinneen et al.'s 348 (T9-S1-16/-17/-18; 2016–2018; size distribution split by OS, totals and types not split), 8 Linux and 5 dual-boot machines at Harvey Mudd in 2001 (T9-S1-15), one Debian workstation's chunk overlap (T9-S1-07), 33 Linux developers' home directories on a shared server (T9-S1-20/-21), a university UNIX department (T9-S1-14) and Cambridge home directories with the platform not named (T9-S1-08). Established by search-log rows 12–16, 25, 32–33, 36. The large populations (T9-S1-01/-02/-11/-12/-13/-31) are all Windows at Microsoft or Cornell, 1998–2009.
- **(b) Anything after 2018 on whole-machine contents.** The newest collection is Dinneen et al. (collected 2016–2018, published 2019 and 2021). Rows 25, 32–33, 36.
- **(b) Compressibility of a personal file system across a population.** Only single points: one user's home directory (T9-S1-05, factor 1.66), 44 Cambridge home directories as one tar (T9-S1-08, 2.9 GB → 1.4 GB), enterprise home/project volumes (T9-S1-26), UbuntuOne's qualitative statement (T9-S1-22). Rows 30, 34, 35.
- **(c) Bytes changed between consecutive backups of a personal machine, across a population.** Only: one personal machine's daily new/changed bytes (T9-S1-05), file-count change per day on 45 Windows NT machines (T9-S1-31), weekly file-state transition probabilities for students' home directories (T9-S1-19), week-to-week dedup ≥ 98 % (≈ 98.5 %) on university home-directory servers (T9-S1-27/-28), four weekly Windows desktop fulls deduplicating to 72–83 % (T9-S1-02), and dedup ratios of simulated incremental and weekly-full backups for 33 Linux developers (T9-S1-20). Enterprise telemetry (T9-S1-03/-04) sees appliance churn and job sizes, not source change. Rows 19, 21, 23, 24, 30, 31.
- **(c) Consumer backup tools' data (Time Machine, Windows File History, Déjà Dup, borg/restic users).** No literature characterisation found; not specifically searched beyond rows 30 and 36 — the literature found is enterprise appliance and research-trace work.

**Unreachable or paywalled (not read):** Park & Lilja, "Characterizing datasets for data deduplication in backup applications", IISWC 2010 (IEEE Xplore only; row 19); Meister & Brinkmann SYSTOR 2009 paper text (ACM DL only; slides and the author's dissertation read instead, row 21); Tan et al., SAM, ICPP 2010 and Fu et al., AA-Dedupe, IEEE Cluster 2011 — both characterise personal-computer backup data sets per their abstracts (IEEE/ResearchGate only; rows 23–24); Kaczmarczyk et al., SYSTOR 2012 (ACM/ResearchGate only; row 31); Henderson & Srinivasan 2009 (Springer; row 28); Gonçalves & Jorge 2003 (host unreachable; row 29; id T9-S1-32 dropped). Earlier studies cited by T9-S1-01 and T9-S1-11 — Satyanarayanan 1981, Mullender & Tanenbaum 1984, Bennett et al. 1991, Sienknecht et al. 1994, Hicks et al. 2008 (ACM TOIS) — were not searched for open copies; Irlam's 1993 Unix file-size survey is a Usenet/web posting, not literature, and belongs to S3. Published data behind candidates (FSL Homes traces at `tracer.filesystems.org`, `github.com/jddinneen/fm-results-tables`) is S3's class and was not fetched.
