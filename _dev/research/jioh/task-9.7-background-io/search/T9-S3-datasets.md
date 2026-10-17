# T9-S3 — published data on input file sets for backup and archive runs

Task 9.7 "Background and IO", stage-2 search, addendum topic T9 (input file sets for backup and archive runs). Reader class S3 (public traces, datasets and published data). Parts of T9 read here: (b) published data on what personal or desktop file systems contain; (c) published data on real backup sources and their change between backups; (d) standard corpora for compressors, archivers or backup tools as downloadable data. Part (a) (benchmark-owner definitions of a compression or backup workload's input) belongs to S2 and is touched here only where a published data set is itself the input.

All fetches on 2026-09-19 (UTC times in the copy tables) from the development Mac without a proxy: GitHub metadata through `gh api` (gh 2.89.0, authenticated), every other file with `curl` 8.7.1 (`curl -sSL -A curl/8.7.1`). SHA-256 is `shasum -a 256` of the saved file. Copies are under `_dev/research/jioh/task-9.7-background-io/sources/T9-S3-NN/` (gitignored); every passage and copy identification below is meant to stand on its own. WebFetch was not used; web search only located copies.

Quoting convention: passages from HTML pages are the page's text content with tags removed and runs of whitespace collapsed; table cells are separated by " | ". Passages from text, Markdown, CSV, JSON and source files are quoted as saved. "…" marks an omission.

Where a data set is large, the README, manifest and listings were saved rather than the whole, and the candidate says so. Downloads in this session total about 0.28 GB.

A reminder of the T9 rule applied throughout: T9 is an input, not a response-side value. An observation from any platform is a candidate, with its platform, population and date named. Age is recorded, not a ground for exclusion.

## 1. Search log

| # | Date | Engine / venue | Query or request | Hits followed | Dead ends (HTTP) |
|---|------|----------------|------------------|---------------|------------------|
| 1 | 2026-09-19 | WebSearch | FSL traces and snapshots public archive fslhomes daily snapshots home directories dedup tracer.filesystems.org | tracer.filesystems.org → T9-S3-01 | — |
| 2 | 2026-09-19 | curl | tracer.filesystems.org index, `traces/fslhomes/` and `traces/macos/` listings with every per-year listing, both timemaps, `fs-hasher-0.9.5.tar.gz`, `traces/fslhomes/2013/SHA256SUM` | all 200 → T9-S3-01 | — |
| 3 | 2026-09-19 | curl | eight FSL Homes snapshot tarballs (user008 2013-02-12/13; user004 2013-03-19/20; user005 2012-04-17/18 and 2012-05-04/05), `traces/fslhomes/2012/SHA256SUM`, and HEAD of user005's 127 snapshots of 2012 | 200 → T9-S3-01 | the user004 downloads hit the 600 s `--max-time` (curl exit 28) and were resumed with `curl -C -`; every tarball matches the publisher's SHA256SUM |
| 4 | 2026-09-19 | WebSearch | SNIA IOTTA static snapshot trace Microsoft file system metadata five-year study download | iotta.snia.org/traces/static → T9-S3-02…05, T9-S3-10 | — |
| 5 | 2026-09-19 | WebSearch | Meyer Bolosky "A Study of Practical Deduplication" data released SNIA 857 desktop file systems | the SNIA listing (UBC-Dedup) → T9-S3-02 | — |
| 6 | 2026-09-19 | curl | iotta.snia.org `traces/static`, `/traces/static/{3382,3382?page=2,3387,183,4,415,5228}`, readmes `/traces/static/{4197,184,123}/download?type=readme`, sample `/traces/static/415/download?type=sample_trace` | all 200 → T9-S3-01…05 | `/traces/static/415/download?type=file` answers 307 to a licence-acceptance form that requires first name, last name, e-mail and company (saved; not submitted, so no full SNIA trace file was downloaded) |
| 7 | 2026-09-19 | curl | microsoft.com/en-us/research/publication/a-five-year-study-of-file-system-metadata/ | 200 → T9-S3-03 | — |
| 8 | 2026-09-19 | WebSearch | Kuenning "file size survey" results page submitted file size distributions | Dinneen & Nguyen 2021 (arXiv 2107.03272); no Kuenning survey page. The Evans & Kuenning data turned up in row 6 (SNIA 415) | — |
| 9 | 2026-09-19 | WebSearch | Dinneen Julien "personal file collections" dataset OSF OR figshare OR zenodo file metadata Cardinal tool | arXiv 2402.06421; no deposited raw data | — |
| 10 | 2026-09-19 | WebSearch | "What's in People's Digital File Collections" Dinneen data availability extensions file counts participants | arXiv 2107.03272, 2402.06421 (PDFs saved for the population and date) → T9-S3-06 | — |
| 11 | 2026-09-19 | WebSearch | crowdsourced file size distribution survey users submit results home directory histogram github dataset | github.com/jddinneen/fm-results-tables → T9-S3-06 | — |
| 12 | 2026-09-19 | GitHub REST | `repos/jddinneen/fm-results-tables` (tree at 1a5a243), `users/jddinneen/repos` | 200 → T9-S3-06 | — |
| 13 | 2026-09-19 | WebSearch | public dataset file system metadata snapshots Linux home directories file sizes extensions released researchers download | nothing new (the Microsoft five-year study again) | — |
| 14 | 2026-09-19 | WebSearch | zenodo dataset personal computer file system metadata file extensions sizes users anonymized collection 2020…2023 | arXiv 2503.22089 (Saric et al. 2025, 9 Windows participants' 25 largest files): a paper, and grep of its PDF found no data release; left to S1 | — |
| 15 | 2026-09-19 | WebSearch | Steam hardware survey "Total Hard Drive Space" "Free Hard Drive Space" distribution | store.steampowered.com/hwsurvey → T9-S3-07 | — |
| 16 | 2026-09-19 | WebSearch | UbuntuOne trace dataset Gracia-Tinedo "Dissecting UbuntuOne" download file metadata extension size | cloudspaces.eu/results/datasets → T9-S3-08 | — |
| 17 | 2026-09-19 | curl | NEC Personal Cloud trace `http://ast-deim.urv.cat/NEC_sharing_traces`; U1 trace `ftp://ast2-deim.urv.cat/ubuntuone_trace.gz` | — | NEC: 301 → https with a certificate for another host (curl exit 60); with `-k`: 302 → cloudlab.urv.cat → 404 "Site not found · GitHub Pages" (saved). U1: FTP connection failed (curl exit 7, no HTTP status) |
| 18 | 2026-09-19 | WebSearch | "ubuntuone_trace" OR "U1 trace" mirror download SNIA OR zenodo OR github UbuntuOne personal cloud trace 84GB | no mirror found | — |
| 19 | 2026-09-19 | WebSearch | Backblaze blog average backup size per customer number of files file types backed up statistics | Backblaze posts on restores and total stored data only; no per-customer size or type data | — |
| 20 | 2026-09-19 | WebSearch | backup workload dataset released "backup" deduplication traces public download enterprise backup job metadata Symantec OR Veritas OR "Data Domain" trace | none | — |
| 21 | 2026-09-19 | WebSearch | Amvrosiadis Bhadkamkar "Identifying trends in enterprise data protection systems" dataset released backup jobs Symantec | the ATC'15 paper only; no released data found | — |
| 22 | 2026-09-19 | WebSearch | Duplicati usage reporter statistics public backup size file count distribution usage-reporter.duplicati.com | usage-reporter.duplicati.com → T9-S3-09 | — |
| 23 | 2026-09-19 | curl + GitHub code search | usage-reporter.duplicati.com page and `/api/v1/view?page_size=7&page_offset=0&rangetype={month,year}`; `search/code q=BACKUP_FILESIZE repo:duplicati/duplicati` → `Duplicati/Library/Main/Controller.cs` at 015c809 | 200 → T9-S3-09 | `rangetype=Month` and `=Year` (capitalised) → 400 `{"error":"No valid rangetype found"}` (discarded) |
| 24 | 2026-09-19 | WebSearch | daily data change rate between consecutive backups measured dataset home directories percent changed per day incremental backup published statistics | vendor blog and forum rules of thumb (Keepit on SaaS backups, Commvault community) — not followed: not data about personal or desktop file sets | — |
| 25 | 2026-09-19 | curl | pdos.csail.mit.edu/archive/p9trace/ (index, Readme, format.txt, bootes/ and emelie/ listings) | 200 → T9-S3-10 | — |
| 26 | 2026-09-19 | WebSearch | Matt Mahoney 10 GB benchmark compression archivers file set 79,431 files mattmahoney.net/dc/10gb.html | mattmahoney.net/dc/10gb.html and /dc/mingw.html → T9-S3-11 | — |
| 27 | 2026-09-19 | WebSearch | Silesia compression corpus files list sizes download sun.aei.polsl.pl sdeor silesia.zip | sun.aei.polsl.pl/~sdeor → T9-S3-12 (page + `corpus/silesia.zip`, 68 MB, downloaded whole) | — |
| 28 | 2026-09-19 | curl | corpus.canterbury.ac.nz/descriptions/ and `resources/{cantrbry,large,calgary,artificl,misc}.tar.gz` | 200 → T9-S3-13 | `resources/` directory index 403 |
| 29 | 2026-09-19 | curl | mattmahoney.net/dc/text.html, /dc/textdata.html; HEAD of /dc/enwik8.zip and /dc/enwik9.zip | 200 → T9-S3-14 (data files not downloaded) | — |
| 30 | 2026-09-19 | WebSearch | Squash compression benchmark corpus files list alice29 fireworks.jpeg geo.protodata kppkn.gtb urls.10K download | quixdb/squash-benchmark → T9-S3-15 | — |
| 31 | 2026-09-19 | GitHub REST + curl | `repos/quixdb/squash-benchmark` contents at 37ee145; quixdb.github.io/squash-benchmark/ and its `squash-benchmark.js` | 200 → T9-S3-15 | — |
| 32 | 2026-09-19 | WebSearch | Maximum Compression benchmark Werner Bergmans multiple file compression test file set 510 files description archived | maximumcompression.com → T9-S3-16 | www.maximumcompression.com/data/summary_mf.php 404; the live domain now serves unrelated blog posts (home page saved). archive.org availability API 429 ("Too Many Requests"); a single Wayback fetch then returned 200 |
| 33 | 2026-09-19 | curl | www.squeezechart.com/ and SqueezeChart2018web.xlsx; HEAD of the test-set archives named in it | 200 → T9-S3-17 | compressionratings.com/files/squeezechart_*.7z: 200 with a 114-byte redirect to "/lander" (parked domain); squeezechart.com/TEST_Audio.arc 404; imagecompression.info/test_images/squeezechart_camera_raw.zip 301 → 404 |
| 34 | 2026-09-19 | WebSearch | deajan backup-bench borg restic kopia duplicacy bupstash benchmark dataset initial backup git versions | deajan/backup-bench → T9-S3-18 | — |
| 35 | 2026-09-19 | GitHub REST + raw | `repos/deajan/backup-bench` at 4a0ff4f (README, HOWTO, RESULTS-20220819, RESULTS-20220906, CHANGELOG, script/backup-bench.sh, script/backup-bench.conf) | 200 → T9-S3-18 | — |
| 36 | 2026-09-19 | WebSearch | gilbertchen benchmarking duplicacy restic attic duplicity linux code base backup benchmark VirtualBox image | gilbertchen/benchmarking → T9-S3-19 | — |
| 37 | 2026-09-19 | GitHub REST + raw | `repos/gilbertchen/benchmarking` at b56d7e7 (README, linux-backup-test.sh, vbox-backup-test.sh, common.sh); `repos/borgbase/benchmarks` at 16e6e8c (README, v2/tests.sh, one final-size result) | 200 → T9-S3-19, T9-S3-20 | — |
| 38 | 2026-09-19 | WebSearch | deduplication research datasets download "Linux kernel" "VM images" "RDB" "Web" snapshots dataset FastCDC evaluation public datasets list | Kaggle sreeharshau/vm-deb-fast25 → T9-S3-21; arXiv 2409.06066 (dataset construction in a paper; left to S1) | — |
| 39 | 2026-09-19 | Kaggle REST + GitHub | `kaggle.com/api/v1/datasets/view/sreeharshau/vm-deb-fast25`, `…/datasets/list/…` (4 pages); UWASL/dedup-bench README at 8e2697c | 200 → T9-S3-21 | — |

## 2. Candidates

Ordered by T9 part: (b) and (c) data sets first (T9-S3-01…10), then (d) corpora and backup-benchmark inputs (T9-S3-11…21).

### T9-S3-01 — FSL Traces and Snapshots Public Archive: "Homes" and "MacOS" daily snapshots (Stony Brook University File systems and Storage Lab)

**Citation.** File systems and Storage Lab (FSL), Stony Brook University, "FSL Traces and Snapshots Public Archive", https://tracer.filesystems.org/ (page "Last updated: 2026-01-08"); releases 1 (July 2014), 2 (December 2016) and "1+2 Updated" (December 2017). Collected with fs-hasher 0.9.5. The site names V. Tarasov et al., "Generating Realistic Datasets for Deduplication Analysis", USENIX ATC 2012, and Z. Sun et al., "A Long Term User-Centric Analysis of Deduplication Patterns", MSST 2016, as the studies that used and characterised it. Also mirrored on SNIA IOTTA as "FSL-Dedup Traces" (`iotta.snia.org/traces/static/5228`).

**Copy read.** The data set itself is large: the reader's sum over the listings is 5,807 Homes snapshots (about 2,973 GB compressed) and 1,321 MacOS snapshots (about 2,325 GB compressed). So the index, READMEs, all listings, the checksum files for 2012 and 2013, the collection tool and eight whole Homes snapshots (three users, two-day pairs) were saved, not the archive.

| File | Size (B) | SHA-256 | Accessed (UTC) |
|---|---|---|---|
| `index.html` (https://tracer.filesystems.org/) | 9,215 | 563649aacb877831d320b5c4571cf0e4d58458a16d3abab2b547568ec1261283 | 03:48:41 |
| `fslhomes2-timemap.html` | 2,047,585 | 14f5c4de704da0e09b09970b760910bb2d526164041ef4270f597b271281402f | 03:48:43 |
| `macos2-timemap.html` | 372,663 | 1592f56afc2cb2e60f92f0f9323f62887fef67c4ba6020d2792af542e6767361 | 03:48:45 |
| `listing-fslhomes.html` (`traces/fslhomes/`) | 1,953 | 4a5f82b3d1d692d7d895efbfca051840ef2b2bb7a677dd72cc999640f00b49d7 | 03:49:08 |
| `listing-fslhomes-{2011-8kb-only,2012-8kb-only,2012,2013,2014,2015}.html` | 580,674 / 155,297 / 855,684 / 411,924 / 990,876 / 8,928 | 108a7262…d5add56a9 / 796805772f…929a13 / 73054ad5…4f761 / 6c498945…4b853 / ddb3c9a3…f2b300d43 / 2e9582f3…c44870 (full: see the note below the table) | 03:49:21–03:49:54 |
| `listing-macos.html` (`traces/macos/`) | 2,327 | 60edd471e425f4942fe32ffe7b09c5583677a5caf13c1de7aa0ddc06c871036e | 03:49:09 |
| `listing-macos-{2011-8kb-only,2011,2012-8kb-only,2012,2013,2014,2015,2016}.html` | 51,004 / 4,679 / 28,004 / 126,679 / 126,179 / 172,679 / 126,179 / 34,179 | see note | 03:49:54–03:50:05 |
| `fs-hasher-0.9.5.tar.gz` | 228,105 | 7fae29993ce4d4c316a1fd656f41b0a21d9fb7be0d0169b44eac9cddd7217082 | 03:49:09 |
| `SHA256SUM-fslhomes-2013` (`traces/fslhomes/2013/SHA256SUM`) | 81,192 | b38fdf57f4d596fa7fb2eb6896e5d4f3678e4a66fe86bc4efe8c351f818ef102 | 03:51:35 |
| `fslhomes-user008-2013-02-12.tar.bz2` | 22,926,889 | 6b142406306faf60e77ee1bedc3bc724b6ed3575306a5a181f2b13a7faef955f (= publisher SHA256SUM) | 03:51:37 |
| `fslhomes-user008-2013-02-13.tar.bz2` | 22,925,964 | ce0b89cf2dcf713d76c35997f7d36c4d36684f7898e9803ac79fcbac97c381f8 (= publisher SHA256SUM) | 03:55:23 |
| `fslhomes-user004-2013-03-19.tar.bz2` | 66,700,183 | b11564e168ae0eeb5324035ab7274fdd2d649fc822b146a7f51d40aa2128a1a8 (= publisher SHA256SUM; the first attempt stopped at 61,071,112 B and was resumed) | 04:00:29, resumed to 04:12:29 |
| `fslhomes-user004-2013-03-20.tar.bz2` | 66,699,000 | f3c8539a8d5840b6ec5a17bbc22aa7604f30c0b780e2384210f0ac5696f96b38 (= publisher SHA256SUM; the first attempt stopped at 61,091,592 B and was resumed) | 04:10:29, resumed to 04:22:52 |
| `SHA256SUM-fslhomes-2012` (`traces/fslhomes/2012/SHA256SUM`) | 168,912 | d9954a1b286da2abf07d8f115c02d5ecd0caa94de40cd4ccf915739f949b0f13 | 04:24:11 |
| `fslhomes-user005-2012-04-17.tar.bz2` | 4,440,100 | b4c12f4942799106218954854f2ff6ba4353107890a56fd22cdc7f68cef76de4 (= publisher SHA256SUM) | 04:24:14 |
| `fslhomes-user005-2012-04-18.tar.bz2` | 4,459,425 | b8cbd2625065dfe58cd370f34df275a90d992580594276daec25e56a49de3114 (= publisher SHA256SUM) | 04:24:58 |
| `fslhomes-user005-2012-05-04.tar.bz2` | 4,791,395 | 04830af3627c5a9c74e6fcc6309f8c0f63ab45e9c2dea5f5540fe967f341c81b (= publisher SHA256SUM) | 04:25:42 |
| `fslhomes-user005-2012-05-05.tar.bz2` | 6,711,081 | 534a962e248be2d97c8de44d6fdef9897d471fabed34605a4dd65420a768b3da (= publisher SHA256SUM) | 04:26:30 |
| `README-fslhomes-snapshot.txt` (the `README` member of the user008 2013-02-12 tarball; `cmp` finds it identical in the user004 2013 and user005 2012 tarballs) | 3,717 | e02ffb55b30d1ffa9b081ad7a47b82772981d2edbb4f12d38fecf1e003ecaed5 | extracted |
| `iotta-static-5228.html` (SNIA mirror page) | 16,346 | 26b2bde9b3de92b23301447082175c01ef77a124894072e56063769e147f35d4 | 03:54:00 |

Full SHA-256 of the listings: fslhomes 2011-8kb-only 108a7262739c8073320378a6bece776c806b407494470ab4cbb9818d5add56a9; 2012-8kb-only 796805772f4eb2dcad8da9962836318c215df9b7554258eb6ad71b4090929a13; 2012 73054ad5c70303ee7706f0833f27f92e22c60a3db0bea8e7cd84bc4990b4f761; 2013 6c498945c15747882b7e05de14d15b2903c2f49881ed2c38cbf861b7dc74e853; 2014 ddb3c9a3214cb9df7aa01992b5928a80ff2b7dfdd08b7ab3f10e798f2b300d43; 2015 2e9582f3157c8b50b4021c4c14c09b28aca6c05818bf93abfbe8f53d52c44870. macos 2011-8kb-only 084c97e6b4afb20527b487be2f668ebf6d9aa7ee8bfc58e8633430f9f227f293; 2011 3edb9a7184e18f9e82666877418466280774c0a837e280313d3d17de6662145f; 2012-8kb-only 6f0a40db0d5749482be78d3df4d9e13549893f69ba0393c21fa3fc1d7e9c941c; 2012 c0b97de817ab2279c00af53040cd2f7eb3f66fe20c939608d2bdddc12b80e740; 2013 dd6da73b685adb14712a3b9f77c44e1eefaaf7f96665e9f0abfab46a14488799; 2014 1da55b3447c543026b64599596c34526a45b6cd07acb63888f0ece52e80ef3a1; 2015 d8134bcbc67e3dab45cbcf2b690eb32600ac955a20f48e7468c494da0b218aac; 2016 a394bfbaaa47dbc0917db404cd9187b0dbfed25d99bd811adb06e854d7b14643.

**Passages.**

- `index.html`, Homes section: "The Homes dataset contains snapshots of students' home directories from a shared network file system. The snapshots were collected in the File system and Storage Lab (FSL) at Stony Brook University. A typical activity in the lab involves code development and debugging, paper writing, and other office activities. The files consist of source code, binaries, office documents, virtual machine images, and other miscellaneous files."
- `index.html`, Homes section: "The snapshots were collected between the end of year 2011 and the beginning of year 2014. Upon joining the lab the students were added to the list of active users and the snapshots of their home directories were preserved daily. After graduating, the students were removed from the active users list. If a student was out of the lab for a summer internship, we removed him or her from the active users list for the duration of their internship. In total, over the course of three years, 38 users were active during some time period. At any given time, between 4 and 11 users were active."
- `README-fslhomes-snapshot.txt` (inside each tarball read, 2012 and 2013), the same paragraph in a later wording: "The snapshots were collected between the end of year 2011 and the beginning of year 2015. … In total, over the course of four years, 39 users were active during some time period. At any given time, anywhere from half a dozen to a dozen users were active."
- `index.html`, Homes section: "Until Jan 25, 2012, the snapshots were collected with an average chunk size of 8KiB. Afterwards, the snapshots were collected with multiple average chunk sizes of 2KiB, 4KiB, 8KiB, 16KiB, 32KiB, 64KiB, and 128KiB." … "For privacy reasons, file paths and chunk hashes were anonymized. The anonymization process ensured the preservation of parent-child relationship between files and directories. The process also guaranteed that the files that had the same names in the original snapshots have the same anonymized names. To preserve valuable information about file types we did not anonymize file extensions."
- `index.html`, MacOS section: "These snapshots were collected on a Mac OS X Snow Leopard server running in an academic computer lab. The server runs the following services: LDAP: OpenDirectory (user/group management) SMTP: Postfix Mailman for mailing lists MySQL for Bugzilla HTTP: Apache2 FTP Calendar server (CalDAV) Wiki server Contacts server (CardDAV) There are over 250 users in the system, many are current and ex-students, some guests, and collaborators. At any given time, between 20-30 users are actually active. On Nov 1, 2013, the server was upgraded to Mountain Lion."
- `index.html`, releases table: "1 | July 2014 | From June 2011 to May 2014 | From September 2011 to May 2014 | 2 | December 2016 | From May 2014 to May 2016 | From August 2014 to November 2014 | 1+2 Updated * | December 2017 | From June 2011 to May 2016 | From September 2011 to April 2015".
- `index.html`, software section: "Fs-hasher collects both file system metadata (file names, inode numbers, permissions, etc.) and content hashes. Here is a snippet of hf-stat output for a single file: File path: /home/test/info.dat File size: 47KB 512B file system blocks allocated: 96 Chunks: 4 UID: 0 GID: 80 Permission bits: 100664 Access time: Tue Dec 31 01:14:51 2013 Modification time: Sat Feb 11 23:18:45 2012 Change time: Tue Aug 6 15:31:23 2013 Hardlinks: 1 Device ID: 16777222 Inode Num: 12438164 Chunk Hash Chunk Size (bytes) Compression Ratio (tenth) 88:c0:bb:85:cc:98 16384 120 …"
- `fs-hasher-0.9.5/fs-hasher.c:858` (zlib method): "cratio = (buffersz * 10) / compressedsz;"; `fs-hasher.c:815–818` (method "none"): "uint8_t none_compute_cratio(unsigned char *buffer, int buffersz) / { / return 10; / }". The man page `manpages/fs-hasher.1` words it the other way round: "computes the compression ratio of every chunk by first compressing the chunk and then dividing the size of the compressed chunk by its original size."
- `iotta-static-5228.html` (SNIA mirror): "FSL Homes | Snapshots of students' home directories from a shared network file system at Stony Brook University. … 2011 - 2015 | over 3 years | 469 Billion | 2.88 TB | Mac OS | Snapshots of Stony Brook server running Mac OS X in a computer lab. On Nov 1, 2013, Mac OS X was upgraded from Snow Leopard to Mountain Lion. … 2011 - 2016 | almost 5 years | 240 Billion | 2.26 TB".

**Coverage.**
- T9 (b): covers. Per-file records of real home directories: anonymised path with the extension kept, size in bytes, 512-B blocks, uid, gid, permission bits, atime, mtime, ctime, hard links, device and inode, and per-chunk hash, size and compression ratio. Population: 38 or 39 lab members' home directories on a shared network file system (Stony Brook FSL). Platform: a shared network file system for Homes, whose server OS is not stated; the anonymising host in the 2012 and 2013 hash files reads "Darwin 16.7.0 x86_64 vir.fsl.cs.sunysb.edu". Dates: 2011-09-10 to 2015-04-10 per the listings. The MacOS set is a lab *server* with 250 accounts, not a desktop: context.
- T9 (c): covers. Daily snapshots per user make the change between consecutive backups directly computable: files added, removed or modified, and new chunk bytes. Within-snapshot and cross-snapshot deduplication is computable from the chunk hashes.
- Compressibility: covers only where the snapshot was collected with the zlib method; the 2012 and 2013 files read here all carry the "none" constant (see the reader's computation below).
- Licence: none stated on the site; the README in each tarball carries "Copyright (c) 2012-2016 … The Research Foundation expressly disclaims any warranty … and provides the snapshots "as is."".

**Observation status.** A set of per-user time series, each user one observation. For a named snapshot, the machine (shared file server; per-user home), the subject (that user's home directory on that date) and the window (one daily scan) are named. The collection host is anonymised.

**Reader's own computation** (locates the candidate; not a value). fs-hasher's `hf-stat` and a small dumper over `libhashfile` were built from the saved tarball (`cc -O2 -w -o hf-stat hf-stat.c libhashfile.c liblog.c`, and the same for `hfdump.c`, which prints one line per file and per chunk). Each snapshot's `*.8kb.hash.anon` file was dumped and summarised with a Python script. Paths below are relative to the scratchpad.

- Listing sums (`python3` regex over the saved `listing-*.html`): 39 users (user000–user038), 5,807 Homes snapshots from 2011-09-10 to 2015-04-10, compressed tarballs from 2.2 KB to 9.0 GB. MacOS: 1,321 snapshots from 2011-06-23 to 2016-05-08, 35 MB to 2.4 GB each.
- user008, 2013-02-12 (`hf-stat -t`): "Files hashed: 3586 / Chunks hashed: 331391 / Bytes hashed: 2936236231 / Chunking method: Variable-rabin bits=13, pattern=ffff, Window size=48[2048:16384] / Hashing method: MD5-48".
  - File-size percentiles over the 3,586 files: p10 65 B, p50 1,576 B, p90 107,255 B, p99 1,781,760 B, max 729,067,520 B; 49 zero-byte files.
  - Bytes by extension: `.iso` 2,175,467,520 B in 4 files (74 % of bytes); no extension 424,333,721 B in 2,683 files; `.jar` 222,251,517 B; `.so` 98,504,373 B.
  - Chunk-level deduplication within the snapshot: 2,936,236,231 chunk bytes, 2,792,468,205 unique (ratio 1.051).
  - Every chunk's compression-ratio byte is 10, the value fs-hasher writes for the "none" method, so this snapshot carries no compressibility.
- user008, 2013-02-12 → 2013-02-13: 0 files added, 0 removed, 0 content-modified, 0 mtime changes, 0 new chunk bytes. This user's home did not change between those two days.
- user004, 2013-03-19 (`hfdump` header): 11,206 files, 10,130,780,090 bytes; all 1,072,212 chunks carry compression ratio 10.
  - File-size percentiles: p10 131 B, p50 2,247 B, p90 11,484 B, p99 332,713 B, max 2,122,448,896 B.
  - Bytes by extension: `.vmdk` 7,687,374,548 B in 24 files (76 % of bytes); `.vmem` 1,073,741,824 B; `.iso` 723,517,440 B.
  - Files by count: `.c` 4,148; no extension 3,578; `.sh` 876.
  - Chunk deduplication within the snapshot: ratio 1.458.
- user004, 2013-03-19 → 2013-03-20: no difference. `diff` of the two dumps without the header line gives 0 lines. The newest mtime in the 2013-03-19 snapshot is 6 March 2013, and all 11,206 files share one atime per snapshot, "Tue Mar 19 13:02:59 2013" and "Wed Mar 20 13:03:10 2013" (`hf-stat -f … | grep 'Access time' | sort | uniq -c`), so atime carries no information in these snapshots.
- These quiet pairs led to a search for an active pair. HEAD requests (`curl -sI`, Content-Length) over user005's 127 snapshots of 2012 gave exact tarball sizes. They grow from 4,090,921 B (2012-03-09) to 27,776,458 B (2012-11-19), with day-to-day steps from a few hundred bytes to 13,150,717 B (2012-09-12 → 09-13). The reader's output was saved as `reader-HEAD-sizes-user005-2012.txt` (sha256 96e900afe17a900713b35b354de8a2dfb3f06655253716410eb8a307fcef9171; the reader's own file, not a publisher copy). Two pairs were read: an ordinary weekday step and the largest step before September.
- user005, 2012-04-17 (Tue) → 2012-04-18 (Wed):
  - Day 1: 4,304 files, 553,716,024 B; p50 3,705 B, p90 36,842 B, max 67,108,864 B.
  - Largest types by bytes: no extension 144.9 MB in 998 files, `.log` 87.0 MB in 565, `.pdf` 55.7 MB, `.raw` 47.9 MB in 551.
  - Chunk deduplication within the snapshot: ratio 1.317.
  - Change: 16 files added (1,443,518 B), 1 removed (5,422 B), 16 content-modified (60,094,046 B at their day-2 size), 16 with a changed mtime. Day-2 chunk bytes absent from day 1: 37,120,717 B, 6.7 % of day 2's 555,168,989 chunk bytes.
- user005, 2012-05-04 (Fri) → 2012-05-05 (Sat):
  - Day 1: 5,125 files, 579,960,692 B.
  - Change: 675 files added (245,210,176 B), 4 removed (43,298 B), 78 content-modified (65,201,067 B), 91 with a changed mtime. Day-2 chunk bytes absent from day 1: 271,939,147 B, 33 % of day 2's 825,197,554.
  - The growth is mostly extensionless files: 150.4 MB in 1,190 files on day 1, 336.8 MB in 1,582 on day 2.
- All user005 chunks also carry compression ratio 10.
- Script: `scratchpad/t9s3/fsl_analyze.py <day1.tsv> <day2.tsv>`. Change is keyed by anonymised path, since anonymised names are stable across snapshots per the README. "Content-modified" means the chunk-hash list or the size differs. "New chunk bytes" are day-2 chunks whose hash is absent from day 1.

### T9-S3-02 — SNIA IOTTA "UBC-Dedup": file-system scans of 857 file systems at Microsoft (Meyer & Bolosky, 2009)

**Citation.** SNIA IOTTA Repository, Static Snapshots, "UBC-Dedup", trace id 3382 (16 subtraces), "Traces collected for the paper "A Study of Practical Deduplication" by Dutch T. Meyer and William J. Bolosky of The University of British Columbia and Microsoft Research" (USENIX FAST 2011). README by Dutch T. Meyer dated 1/1/2013.

**Copy read.** The traces total 3.4 TB (SNIA listing), so the listing pages and one subtrace README were saved.

| File | Size (B) | SHA-256 | Accessed (UTC) |
|---|---|---|---|
| `iotta-traces-static.html` (http://iotta.snia.org/traces/static) | 36,136 | d71314392875ef0ef958d4499700df0df1e20d0e7f70835eda156772d9da7a11 | 03:53:42 |
| `iotta-static-3382.html` | 45,497 | cc986ef8976c87427e41c9ac775d08434c07f43b1945aa2827e81ae04a54d0bf | 03:53:57 |
| `iotta-static-3382-p2.html` (`?n=10&page=2`) | 31,136 | 02f60628238fe0782f70a02f21424396759b49a87629c7707559a31fdedd1d09 | 03:54:27 |
| `iotta-static-3387.html` (subtrace group 16f) | 52,206 | 4f9904a98dbc43060080b72e23f68f62032970b8eb22a79a68cf4e91680526b0 | 03:54:36 |
| `ubc-dedup-16f-000-readme` (`/traces/static/4197/download?type=readme`; server `Last-Modified: Fri, 18 Sep 2015 21:45:25 GMT`) | 3,350 | c25a0edbe44022073cb00717d5d41d9ecf946210fccabdd742e335d82817f9f2 | 03:54:50 |

**Passages.**

- `iotta-traces-static.html`: "UBC-Dedup | Traces collected for the paper "A Study of Practical Deduplication" by Dutch T. Meyer and William J. Bolosky of The University of British Columbia and Microsoft Research | Several scans of 857 file systems at Microsoft Scans vary with respect to hash type, block size and contents of metadata. | 2009 | 4 months | 3.4 TB".
- `iotta-static-3382.html` / `-p2.html`, the 16 subtrace groups and sizes: 16f 171 GB, 16fb 186 GB, 16r 253 GB, 16rb 258 GB, 32f 122 GB, 32fb 123 GB, 32r 189 GB, 32rb 190 GB, 64f 89.3 GB, 64fb 90.4 GB, 64r 154 GB, 64rb 155 GB, 8f 330 GB, 8fb 335 GB, 8r 415 GB, 8rb 419 GB. For example: "16f | … | Scan of 857 file systems at Microsoft hashed using fixed blocks of size 16 kilobytes. | 2009 | 2 months | 171 GB"; "8r | Scan of 857 file systems at Microsoft hashed according to the Rabin fingerprinting algorithm with 8 kilobytes selected as the statistical mean chunk size. | 2009 | 2 months | 415 GB".
- `iotta-static-3387.html`: "16f-000 | … | 2009 | about 3 hours | 2.78 GB"; "16f-001 | … | about 2 hours | 2.78 GB"; "16f-002 | … | about 5 hours | 2.79 GB".
- README: "The full data set gathered in this study contains 16 distinct scans each across around 850 file systems. The scans differ only in the content hashing scheme used, and in that different scans happened to be collected across somewhat different collections of machines, though there is extensive overlap."
- README, per-file format: "Directory name:length (hashed) / File name:length (hashed) / extension:0 hashed (hashed) / namespace depth / file size / file attributes flag (in hex) / file id / number of hard links to file / the reparse flag status (in hex) / Creation time / last access time / last modification time" … "Hash of data:chunk size".
- README, system metadata: "OS from GetVersionEx()" … "Free clusters from GetDiskFreeSpace() / Total clusters from GetDiskFreeSpace()".

**Coverage.**
- T9 (b): covers. Per-file records of Windows file systems at Microsoft, 2009: hashed names, a hashed extension, size, attributes, timestamps and chunk hashes with chunk sizes, plus volume capacity and free space. File counts, size distributions, capacity used and duplication are computable. The extension is hashed ("extension:0 hashed (hashed)"), so the type mix is recoverable only by equality between hashed values, not by name.
- T9 (c): covers partially. The 16 scans are separate passes over largely overlapping machines within about 2 to 4 months. Whether any machine was scanned on consecutive schedule points is not stated in the saved copies. No compressibility field.
- Platform: Windows (NTFS fields). Population: about 850 to 857 file systems at Microsoft. Date: 2009.
- Licence: SNIA Trace Data Files Download License (quoted under T9-S3-05).

**Observation status.** Many observations (one per file system per scan); machine identifiers hashed.

**Reader's own computation.** None (no trace file downloaded).

### T9-S3-03 — SNIA IOTTA "Microsoft Longitudinal Study": annual file-system metadata snapshots 2000–2004 (Agrawal, Bolosky, Douceur, Lorch)

**Citation.** SNIA IOTTA Repository, Static Snapshots, "Microsoft Longitudinal Study", trace id 183 (22 repackaged parts). The raw data of N. Agrawal, W. J. Bolosky, J. R. Douceur, J. R. Lorch, "A Five-Year Study of File-System Metadata", USENIX FAST 2007 (journal version ACM TOS). Microsoft Research publication page saved for the population statement.

**Copy read.**

| File | Size (B) | SHA-256 | Accessed (UTC) |
|---|---|---|---|
| `iotta-traces-static.html` | 36,136 | d71314392875ef0ef958d4499700df0df1e20d0e7f70835eda156772d9da7a11 | 03:53:42 |
| `iotta-static-183.html` | 53,371 | adce14df44510c9af9f8441329f3a79102aa4e7312ed02bf11823976b96fe4aa | 03:53:58 |
| `ms-longitudinal-part01-readme` (`/traces/static/184/download?type=readme`) | 11,049 | d484a45d08d3f0e755787ee35c68b75b79ee730247b9452c815dc9c8b4fee443 | 03:55:04 |
| `msr-publication-page.html` (microsoft.com/en-us/research/publication/a-five-year-study-of-file-system-metadata/) | 176,948 | 79f6b4cf30e170f18f4cdbd28f41cd3508b2df512c622ca44e905666f1584f8d | 04:14:13 |

The data (91.1 GB in 22 parts) was not downloaded.

**Passages.**

- `iotta-traces-static.html`: "Microsoft Longitudinal Study | Because of the size of the traces, they have been repackaged by IOTTA into 22 zip files. … | The raw data used for the FAST 2007 paper "A Five Year Study Of File System Metadata" by Nitin Agarwal, William J. Bolosky, John R. Douceur, and Jacob R. Lorch. There are five years worth of snapshot data, for years from 2000 to 2004. | 2000 - 2004 | over 4 years | 5 Billion | 91.1 GB".
- `iotta-static-183.html`: "MS Longitudinal Part 01 | This zipped tar file contains data for a subset of the users in the original study. Downloading any of these parts will give you snapshot, directory, and file data for a randomly selected subset of users, and downloading all 22 parts will give you all the data originally included in the study. … | 2000 - 2005 | over 4 years | 200 Million | 4.24 GB".
- `msr-publication-page.html`: "For five years, we collected annual snapshots of file-system metadata from over 60,000 Windows PC file systems in a large corporation. In this article, we use these snapshots to study temporal changes in file size, file age, file-type frequency, directory size, namespace structure, file-system population, storage capacity and consumption, and degree of file modification."
- README: "In our terminology, a snapshot is a single file system that we scanned. We eliminated duplicates within a dataset, and usually kept the newest snapshot for a particular file system."
- README, snapshot line: "SnapshotID UserName ComputerName VolumeName VolumeID DriveLetter FileSystemType FreeSpace TotalSpace SnapshotTime ClusterSize FilesystemFlags ScanOptions".
- README, file line: "SnapshotID FileID ParentDirectoryID FileName FileExtension CompressionType FileSize 0 AccessAge WriteAge CreationAge Attributes"; "FileExtension is the portion of the file name following the last "." character in the file name, if it is five or fewer characters in length. … FileExtension is not anonymized."; "FileSize is the size of the file expressed as a 64-bit decimal integer."
- README: "FileSystemType is the type of the file system. It's an ascii string. Nearly all of the file systems are NTFS, FAT32, or FAT."

**Coverage.**
- T9 (b): covers. Per-file size and plain-text extension (up to five characters), directory tree, timestamps and per-volume capacity and free space, for annual scans of Windows PC file systems in one corporation. Population: "over 60,000 Windows PC file systems" (Microsoft Research page). Platform: Windows (NTFS, FAT32, FAT). Dates: 2000–2004.
- T9 (c): the annual cadence gives year-to-year change only, not between consecutive backups; content hashes are absent.
- Licence: SNIA Trace Data Files Download License.
- The repository labels this group: "WARNING: These traces are over 10 years old! They should not be used for modern research!" (`iotta-traces-static.html`). Recorded; not a ground for exclusion under T9.

**Observation status.** One observation per file system per year; users and machines anonymised.

**Reader's own computation.** None.

### T9-S3-04 — SNIA IOTTA "Microsoft 1998 Static Study": 10,568 file systems on 4,801 PCs (Douceur & Bolosky)

**Citation.** SNIA IOTTA Repository, Static Snapshots, "Microsoft 1998 Static Study", trace id 4 (7 subtraces by job category). Data of J. R. Douceur and W. J. Bolosky, "A Large-Scale Study of File-System Contents", ACM SIGMETRICS 1999.

**Copy read.**

| File | Size (B) | SHA-256 | Accessed (UTC) |
|---|---|---|---|
| `iotta-traces-static.html` | 36,136 | d71314392875ef0ef958d4499700df0df1e20d0e7f70835eda156772d9da7a11 | 03:53:42 |
| `iotta-static-4.html` | 38,166 | d8ffa2f6bdf2eb8453a6e1c2a9eab1dbd332a77fbf66222bb100bb92acb928de | 03:53:59 |
| `ms-1998-jobtype0-readme` (`/traces/static/123/download?type=readme`) | 24,920 | b0e803d92d3acae9db1c32ba63ddc5120ce94b393a17cf8e8938eb77a98178d3 | 03:55:20 |

The data (3.73 GB) was not downloaded.

**Passages.**

- `iotta-traces-static.html`: "Microsoft 1998 Static Study | Static analysis of 10,568 file systems on 4801 workstations at Microsoft. This data formed the basis for the paper "A Large-Scale Study of File-System Contents" by John R. Douceur and William J. Bolosky, published in ACM SIGMETRICS 1999. | Static snapshot of 4800 PCs at Microsoft. | 1998 | 8 days | 153 Million | 3.73 GB".
- `iotta-static-4.html`, subtrace sizes: "Job Type 0 … misc. job types … 187 MB"; "Job Type 1 … administration … 70.6 MB"; "Job Type 2 … business … 202 MB"; "Job Type 3 … management … 292 MB"; "Job Type 4 … non-technical development … 136 MB"; "Job Type 5 … technical development … 2.55 GB"; "Job Type 6 … technical support … 320 MB".
- README §1: "Between the dates of 1 September and 25 September, 1998, we collected snapshots of data from 10,568 file systems of 4801 personal computers at Microsoft Corporation. The file systems contain 140 million files totaling 10.5 TB of data. We recorded the name, size, timestamps, and containing directory of each file and subdirectory on every file system."
- README §2.1.2: "Field 9 is a 64-bit decimal value indicating the size of the file, expressed in bytes." / "Field 10 is a decimal value indicating the extension of the file name. If the extension is one of the 1000 most popular extensions, then this field will have a value between 0 and 999, indicating the corresponding extension in section 2.2.3. Otherwise, this field will have a value of -1."
- README §2.1.1: "Field 4 is a 64-bit decimal value indicating the available space on the file system, expressed in bytes. … Field 5 is a 64-bit decimal value indicating the total (available plus occupied) space on the file system, expressed in bytes. … Field 6 is a decimal value indicating the job category of the user of the file system."

**Coverage.**
- T9 (b): covers. Per-file size and extension (top-1000 extensions decoded by a table in the README), directory structure and timestamps, per-volume total and free space, and the user's job category. Population: 4,801 PCs, 10,568 file systems, 140 million files, 10.5 TB, at Microsoft. Platform: Windows (FAT, FAT32, NTFS, WCEFS). Date: 1–25 September 1998.
- T9 (c): no content hashes and a single scan, so no change between backups.
- Licence: SNIA Trace Data Files Download License. Age: 1998; SNIA's "over 10 years old" warning applies.

**Observation status.** One snapshot per file system.

**Reader's own computation.** None.

### T9-S3-05 — SNIA IOTTA "Multimedia file sizes" (Evans & Kuenning, 2001)

**Citation.** SNIA IOTTA Repository, Static Snapshots, "Multimedia file sizes", trace id 415: "File-size data collected for the paper "A Study of Irregularities in File-Size Distributions"" (K. M. Evans and G. H. Kuenning, SPECTS 2002).

**Copy read.**

| File | Size (B) | SHA-256 | Accessed (UTC) |
|---|---|---|---|
| `iotta-traces-static.html` | 36,136 | d71314392875ef0ef958d4499700df0df1e20d0e7f70835eda156772d9da7a11 | 03:53:42 |
| `iotta-static-415.html` | 8,145 | 922cf381472e849b7209781dc0949a7b9f1b5204205ef6cf201593c871529efe | 03:53:59 |
| `multimedia_sizes-sample.gz` (`/traces/static/415/download?type=sample_trace`; `Content-Disposition: … filename="multimedia_sizes-sample.gz"`; gzip header: original name "01Ext", modified Wed Jun 13 19:08:44 2001) | 381,294 | 9f06f213930543c6b705cdb9c9d8b8a2c01dcc13b76e6b061905015835fc0e64 | 03:55:21 |
| `snia-license-form-415.html` (what `/traces/static/415/download?type=file` returns after its 307) | 14,479 | 216924d8f8a4b6c3293ac9e955af8e0529ed7f61a93124ec8f02280fcf683a91 | 03:55:30 |

The full file (17.1 MB) sits behind the licence form and was not downloaded. No README is offered for this trace.

**Passages.**

- `iotta-traces-static.html`: "Multimedia file sizes | File-size data collected for the paper "A Study of Irregularities in File-Size Distributions". | File-size data collected on various OSes, including measurements of multimedia files. | This trace has no related tools yet. | 2001 | 21 days | 17.1 MB".
- `snia-license-form-415.html`: "SNIA Trace Data Files Download License Acceptance … For downloaded materials that are licensed under any license not approved by the Open Source Initiative, permission is hereby granted, free of charge, to any person obtaining a copy of these I/O trace tool(s) and/or trace data file(s) and associated documentation ("Trace Tools and Data Files") to deal in the Trace Tools and Data Files without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Trace Tools and Data Files". The form's inputs are `downloaderinfo[firstname]`, `[lastname]`, `[emailaddress]` and `[company]` (all `required`).
- `multimedia_sizes-sample.gz`, first lines: "1 - 67047424 2 Jun 3 12:17 --- 0" / "1 - 58720256 4 May 20 13:43 .swp 57344" / "1 - 31451648 7 Dec 8 1997 .cag 30716" / "1 - 22931776 3 Feb 21 2000 .a 22424" / "1 - 12978688 5 Jan 26 2000 .TAR 12726" / "1 - 9024029 4 Sep 17 1998 .mp3 8816".

**Coverage.**
- T9 (b): covers weakly. Per-file lines with a size, a date and an extension, "collected on various OSes", 2001. The field layout is not documented in any saved copy; the reading of column 3 as a size in bytes and column 8 as the extension is the reader's, from the sample lines.
- Population and machines are not stated on the SNIA pages; only the sample (one listing, "01Ext") was read.
- T9 (c): not covered (one scan).
- Licence: SNIA Trace Data Files Download License.

**Observation status.** The sample is one file listing from one unnamed system.

**Reader's own computation** (on the sample only):
- `gzip -dc multimedia_sizes-sample.gz | wc -l` → 74,098 lines.
- Column 3 (`awk '{print $3}' | sort -n`): sum 3,052,396,271, p50 3,068, p90 35,248, max 67,047,424.
- Column 8 (`awk '{print $8}' | sort | uniq -c | sort -rn`): "---" 19,282, `.gif` 8,651, `.html` 3,916, `.h` 3,187, `.htm` 2,083, `.jpe` 1,427, `.o` 1,198, `.dll` 1,110.
- Column 2 takes the values "-", "b", "c", "d", "l", "p", "s", which resemble `ls` file-type letters (reader's reading).

### T9-S3-06 — Dinneen & Nguyen (2021) file-size-distribution result tables for 348 users' personal file collections (Mac OS, Windows, GNU/Linux), `jddinneen/fm-results-tables`

**Citation.** J. D. Dinneen, B. X. Nguyen, "How Big Are Peoples' Computer Files? File Size Distributions Among User-managed Collections", Proc. ASIS&T 2021 (arXiv 2107.03272). Published results: GitHub `jddinneen/fm-results-tables`, folder `ASIST21-FSD`, commit 1a5a2436c5ff76295bfda729f5076c5068e6239b (2021-07-08), no licence file (`license: null`). Population and dates from J. D. Dinneen, C.-A. Julien, "What's in People's Digital File Collections?", Proc. ASIS&T 2019 (arXiv 2402.06421).

**Copy read.**

| File | Size (B) | SHA-256 | Accessed (UTC) |
|---|---|---|---|
| `README.md` (ASIST21-FSD) | 1,055 | 4ba66179f2f9b40c15bab22ac8b862ebb6cba3a04e254309e6d0928ba812ffa4 | 04:04:06 |
| `1-sample-breakdown.csv` | 582 | 66b5ed4f73fbf1bb686b9def6127b805e8203ad45cbd1eef594fad2e5ff5d14f | 04:04:06 |
| `2-normal-stats.csv` | 759 | 37568550d1fb99903c3a2644cb0b2651648dbe6153913b599ed97f66281ef7b6 | 04:04:07 |
| `3-lognormal-stats.csv` | 670 | 68d582d4bd803ef68160cdb486b5afc90be428b1f574897430f4cce2295d912a | 04:04:07 |
| `CountingFileSizes.R` | 10,104 | 19c899149a52509dd6c3ea02eb07fb3b1ad9667dd9bc3f7692bae59a93656cad | 04:04:07 |
| `ReadingJSON.R` | 8,408 | d5abc7b6b2608414a838e916cf8abf4ec6356feb57387e0ea81c2339de85d5cc | 04:04:08 |
| `three-operating-systems-FSD-CDFs.png` | 16,816 | c0538fa5b9c29ef3225b886758c5a656d73cbfefac7b33993d664d0ff0134408 | 04:05:00 |
| `arxiv-2107.03272v1.pdf` | 198,242 | bc87ee9bfaf17892ff4d6f49cde91222c5e50707e4b4a41bd3de4d6545392762 | 04:04:23 |
| `arxiv-2402.06421v1.pdf` | 269,645 | d4988a0a806b0ad51ad666f8d3bb23912352d45b45a4bcdb7f1d88bd9f0ba86a | 04:04:42 |

PDF text was extracted with pypdf 6.19.0 in a scratchpad venv.

**Passages.**

- `README.md`: "This folder contains the tabular results, CDF plots, and R scripts produced during a study of file-size distributions among users' desktop and laptop computers running Mac OS, Windows, and GNU/Linux (Dinneen & Nguyen, 2021)."
- `1-sample-breakdown.csv`: "operating system,all,45638253,346,minus two outliers," / "operating system,darwin (macOS),29251483,169,," / "operating system,win32 (windows),11921985,135,," / "operating system,linux,4464785,42,," / "collection use,knowledge work,11387302,93,," / "collection use,IT work,5978892,24,minus one outlier," / "collection use,study,15361348,142,minus one outlier," / "collection use,personal use,5537206,39,,". Header: "grouped by,category,files / file sizes analysed,participants (n=),note,…".
- `2-normal-stats.csv` (KB): "all,5.271484375,1528.647626,83812.23874,265931072," / "darwin,4.657226563,1361.452531,80916.20861,134423104," / "win32,7.6875,1673.725732,50732.05874,61898304," / "linux,4.596679688,2236.45735,148417.2171,265931072,". Header: "category …,Median file size (in KB),Mean file size (in KB),Standard deviation of file sizes (in KB),Maximum file size (in KB),…".
- `3-lognormal-stats.csv` (KB): "all,9.025024028,730.3251907,19.38081453," / "darwin,7.954528757,532.8117247,18.17055278," / "win32,11.52145405,1085.970547,20.39521851," / "linux,10.82777225,1739.766342,24.22256562,".
- arXiv 2107.03272 p. 3 (Methodology; PDF page 3 of 7): "348 remote and anonymous participants downloaded and ran on their desktops and laptops open-source software (Dinneen et al. 2016) that collected data about files they indicated they manage. File sizes were measured in bytes using python's os.stat().st_size … Care was taken to exclude files not managed by the participant: hidden files and common folders containing operating system files were explicitly ignored." Table 1: "Mac OS (10.7 – 11): 169 (48%) / Windows (XP – 10): 135 (39%) / GNU/Linux: 44 (13%)".
- arXiv 2107.03272 p. 3: "Comprehensive CDF plots, full data tables with discrete values for each distribution, and all analysis scripts can be accessed at github.com/jddinneen/fm-results-tables."
- arXiv 2402.06421 p. 4 (Recruitment and data collection; PDF page 4 of 10): "We recruited participants[1] from February of 2016 to August of 2018 by posting calls on study recruitment Websites, online communities (e.g., Facebook, Reddit), and mailing lists (e.g., industrial, governmental, and academic)." … "specifying where on the computer they manage files (both active, working areas and backup locations like external drives were encouraged)". p. 4: "Though no file or folder names were recorded, instances of non-unique names were noted to provide a measure of duplication."

**Coverage.**
- T9 (b): covers, as published summary statistics only. Per-OS and per-use file counts, median, mean, SD and maximum file size (arithmetic and log-normal), and CDF plots by count, of user-managed files.
- Population: 348 participants (346 after two outliers), 45.6 million files. The GNU/Linux group is 42 participants and 4,464,785 files (44 in the paper's Table 1, 42 in the table after exclusions). Platform: Mac OS, Windows, GNU/Linux desktops and laptops. Date: Feb 2016 – Aug 2018.
- The repository holds three summary CSVs, the R scripts and PNG CDFs. The "full data tables with discrete values for each distribution" that the paper announces are not in the tree at 1a5a243: the reader's `gh api` tree listing shows only the files above plus two more PNGs. No raw per-file data is published.
- Extension mix and duplication appear only in the 2019 paper (S1 territory), not as data here.
- T9 (c): not covered.

**Observation status.** Aggregates over many observations; per-participant data not published.

**Reader's own computation.** None beyond the tree listing.

### T9-S3-07 — Steam Hardware & Software Survey, August 2026: total and free drive space (all platforms and Linux)

**Citation.** Valve, "Steam Hardware & Software Survey: August 2026", https://store.steampowered.com/hwsurvey/Steam-Hardware-Software-Survey-Welcome-to-Steam (`?l=english`, and `&platform=linux`).

**Copy read.**

| File | Size (B) | SHA-256 | Accessed (UTC) |
|---|---|---|---|
| `hwsurvey-combined.html` | 231,927 | f7004033a35336a9933ce8c8785e9143317b9bab7179364cb214c7e32fb84180 | 04:08:00 |
| `hwsurvey-linux.html` | 218,098 | af78e7b96330cf1212a1c22393bc280f40af1c63dbfb003e50da214b7273dd59 | 04:08:00 |

**Passages.**

- Both pages: "Steam Hardware & Software Survey: August 2026 | Steam conducts a monthly survey to collect data about what kinds of computer hardware and software our customers are using. Participation in the survey is optional, and anonymous."
- Combined: "Free Hard Drive Space | … Less than 10 GB | 0.88% | -0.08% | 10 GB to 99 GB | 15.92% | -0.24% | 100 GB to 249 GB | 23.98% | +0.44% | 250 GB to 499 GB | 23.01% | +0.19% | 500 GB to 749 GB | 11.07% | -0.07% | 750 GB to 999 GB | 8.72% | -0.23% | 1 TB to 2 TB | 9.25% | -0.06% | 2 TB to 3 TB | 2.31% | -0.02% | 3 TB to 4 TB | 1.64% | +0.01% | Above 4 TB | 3.22% | +0.07%".
- Combined: "Total Hard Drive Space | … Unspecified | 0.08% | +0.06% | Less than 10 GB | 0.00% | 0.00% | 10 GB to 99 GB | 0.18% | -0.02% | 100 GB to 249 GB | 5.44% | -0.29% | 250 GB to 499 GB | 17.69% | -0.37% | 500 GB to 749 GB | 2.42% | -0.02% | 750 GB to 999 GB | 24.67% | +0.45% | Above 1 TB | 49.51% | +0.18%".
- Linux: "Free Hard Drive Space (Linux) | … Less than 10 GB | 2.85% | … 10 GB to 99 GB | 22.42% | … 100 GB to 249 GB | 23.79% | … 250 GB to 499 GB | 22.45% | … 500 GB to 749 GB | 8.76% | … 750 GB to 999 GB | 10.24% | … 1 TB to 2 TB | 7.73% | … 2 TB to 3 TB | 0.83% | … 3 TB to 4 TB | 0.76% | … Above 4 TB | 0.16%"; "Total Hard Drive Space (Linux) | … Less than 10 GB | 0.04% | … 10 GB to 99 GB | 3.00% | … 100 GB to 249 GB | 17.99% | … 250 GB to 499 GB | 30.12% | … 500 GB to 749 GB | 2.23% | … 750 GB to 999 GB | 30.09% | … Above 1 TB | 16.53%".
- Linux: "Linux Version | SteamOS Holo 64 bit | 21.07% | -1.17%".

**Coverage.**
- T9 (b): context only. Machine-level total and free drive space, as bucketed shares, for the Steam-client population in August 2026, all platforms and Linux separately. It says nothing about file counts, sizes, types or which files a backup would read.
- Used space is not published and cannot be derived per machine, because total and free are separate marginal distributions.
- The Linux population includes SteamOS (Steam Deck) at 21.07 %.
- Whether "Hard Drive Space" means all drives or the system drive is not stated in the saved pages.
- Licence: none stated.

**Observation status.** A monthly aggregate over survey participants.

**Reader's own computation.** None.

### T9-S3-08 — CloudSpaces personal-cloud datasets: UbuntuOne (U1) back-end trace and the NEC Personal Cloud storage snapshot (data unreachable)

**Citation.** FP7 CloudSpaces project, "Datasets", https://cloudspaces.eu/results/datasets. U1 trace: R. Gracia-Tinedo et al., "Dissecting UbuntuOne: Autopsy of a Global-scale Personal Cloud Back-end", ACM IMC 2015. NEC trace: R. Gracia-Tinedo, P. García-López, A. Gómez, A. Illana, "Understanding Data Sharing in Private Personal Clouds", IEEE CLOUD 2016.

**Copy read.**

| File | Size (B) | SHA-256 | Accessed (UTC) |
|---|---|---|---|
| `cloudspaces-datasets.html` | 42,571 | f8c0f15cbd3bb2fd27f2f434d5895da57d6561359eb5ac3645f41c744edffc22 | 04:05:13 |
| `NEC_sharing_traces-404.html` (what the NEC link returns after 301 → https, then with `-k` 302 → cloudlab.urv.cat → 404) | 9,115 | 70d613e3acfba24fd2876fcbacaf639e1e111ef4d54baf70761c47673f37d6a3 | 04:05:41 |

The U1 file `ftp://ast2-deim.urv.cat/ubuntuone_trace.gz` refused the connection (curl exit 7).

**Passages.**

- "NEC Personal Cloud Trace … Regarding storage (CS_FileTraces), the trace is a snapshot of the data store contents (OpenStack Swift). To wit, the trace contains log lines that identify and describe files (size, extension), as well as the file owner and the container/folder where it is stored." … "This trace contains all sharing interactions in the NEC Personal Cloud (Madrid datacenter) from March 7th 2013 to September 9th 2015." … "Download the NEC trace (.zip) - 7.7MB (md5: 27f9f5478d7cbffcedc1b317e8765321)".
- U1: "Explanation of the columns in the trace file (.csv): … ext: file extension. … hash: sha1sum of the file … mime: file type. … size: file size. … tstamp: trace timestamp. … user_id: user identifier." … "Download the U1 dataset (.gz) - 84GB (md5: 62cf355792e59e85a95886e8e23b4ae3)."
- U1: "Consider a line in the trace like this "production-whitecurrant-23-20140128"."
- `NEC_sharing_traces-404.html`: "<title>Site not found &middot; GitHub Pages".

**Coverage.**
- T9 (b) and (c), as described: the U1 trace would give per-upload file size, extension, MIME type and SHA-1 for a personal cloud service's users (Ubuntu desktop sync), over the month the logs cover. The page shows a January 2014 log name; it does not state the window. The NEC storage snapshot would give size and extension per file for a private personal cloud.
- Neither data file could be retrieved on 2026-09-19. The fields are recorded; no values.
- Licence: a citation policy only.

**Observation status.** Not read (data unreachable).

**Reader's own computation.** None.

### T9-S3-09 — Duplicati public usage statistics: per-run source file count and source size, aggregated by OS and month or year

**Citation.** Duplicati, "Usage statistics for Duplicati", https://usage-reporter.duplicati.com/ and its JSON endpoint `/api/v1/view?page_size=7&page_offset=0&rangetype={month|year}`. The reported fields are defined in `duplicati/duplicati`, `Duplicati/Library/Main/Controller.cs` at commit 015c80912780f812a7186054a683d427724c7aef (master on 2026-09-19).

**Copy read.**

| File | Size (B) | SHA-256 | Accessed (UTC) |
|---|---|---|---|
| `usage-reporter-index.html` | 7,913 | 68cecbb3c9413f5929e470b52332cc509a015c81487e9b0456e239e7abee97f9 | 04:06:44 |
| `api-view-month.json` | 88,362 | 71da056b08a8dbc85c47bd13357093cb8afaa75a6f00f744d331b36150ac1f1b | 04:07:15 |
| `api-view-year.json` | 91,933 | cc02ba06bb6216e196f8efa1e169cda7e96ccb623b84244a8d55a7903c9df550 | 04:07:16 |
| `Controller.cs` | 88,081 | 5e5246fe708a203cbc314045dd39ad8d40fd5a677495487b1f3546d5f7cd8483 | 04:07:37 |

**Passages.**

- `Controller.cs:150–152`: "UsageReporter.Reporter.Report("BACKUP_FILECOUNT", config.Result.ExaminedFiles);" / "UsageReporter.Reporter.Report("BACKUP_FILESIZE", config.Result.SizeOfExaminedFiles);" / "UsageReporter.Reporter.Report("BACKUP_DURATION", (long)config.Result.Duration.TotalSeconds);". These calls follow the backup handler's run (`Controller.cs:146–148`).
- `usage-reporter-index.html`: "Usage statistics for Duplicati | Range | Day | Week | Month | Year | Feature | Backend | Encryption | Compression | Duration | Size | Operating system"; its script averages: "if (filter == "BACKUP_DURATION" || filter == "BACKUP_FILESIZE") … entrycounts[i][j] = entrysums[i][j] / Math.max(1, entrycounts[i][j]);".
- `api-view-month.json` opens: `{"kind":"aggregate-month","page_size":7,"offset":0,"next_offset":716,"count":716,"fromtime":1790812799,"rangetype":"month","items":[…`; one item: `{"name":"BACKUP_FILESIZE","value":"","ostype":"Linux","sum":318305765315996293,"count":1546139,"lastupdated":1789786863,"timestamp":1785542400}` (timestamp 1785542400 = 2026-08-01 00:00 UTC).
- `api-view-year.json`, items whose sums sit at the int64 limits: `{"name":"BACKUP_FILESIZE","value":"","ostype":"Windows","sum":9223372036854775807,"count":36321057,"lastupdated":1789370597,"timestamp":1735689600}`; `{"name":"BACKUP_FILESIZE","value":"","ostype":"Windows","sum":-9223372036854775808,"count":38068623,"lastupdated":1783731787,"timestamp":1672531200}` (timestamps = 2025-01-01 and 2023-01-01 UTC).

**Coverage.**
- T9 (c): covers weakly. For every Duplicati backup run that reports usage, the number of files examined and their total size, i.e. the backup source, aggregated as sum and count per OS (Windows, Linux, OSX, Other) per month (Mar–Sep 2026) and per year (2020–2026). Population: Duplicati installations with usage reporting on, desktops and servers alike, not separable.
- Only means are derivable; there is no distribution, no type mix, no compressibility and no change between runs. SizeOfExaminedFiles counts every examined file, not the changed bytes.
- The sums overflow: some sit at ±2^63, and others give negative means. So any sum may have wrapped undetected, and the means below are unreliable.
- Licence: none stated.

**Observation status.** Aggregates over millions of runs; no machine named.

**Reader's own computation** (Python over the saved JSON: for each (timestamp, ostype), sum/count of BACKUP_FILESIZE and BACKUP_FILECOUNT):
- August 2026, examined size per run (mean): Linux 2.059e11 B (n 1,546,139), Windows 1.43e11 B (n 2,962,131), OSX 1.684e11 B (n 1,734).
- August 2026, examined files per run (mean): Linux 9.393e4, Windows 1.093e5, OSX 1.354e5.
- Year 2024, examined files per run (mean): Linux 8.231e4, Windows 8.08e4.
- Visibly wrapped or saturated: the BACKUP_FILESIZE sums for Windows 2021 (negative), Windows 2023 and 2025, Linux 2025 and Other 2026; the BACKUP_DURATION sums with negative means: Windows April, July, August and September 2026 and Linux September 2026 (month view), and Windows 2020 and Linux 2021 (year view).

### T9-S3-10 — Plan 9 file-server daily snapshots, Bell Labs (bootes, emelie), 1990–2001

**Citation.** S. Quinlan (Bell Labs), "Plan 9 File System Traces", mirror at https://pdos.csail.mit.edu/archive/p9trace/ (original ftp://www.cs.bell-labs.com/p9trace); listed by SNIA IOTTA as "Plan 9 Traces" (Static Snapshots). Paper: S. Quinlan, S. Dorward, "Venti: a new approach to archival storage", USENIX FAST 2002.

**Copy read.**

| File | Size (B) | SHA-256 | Accessed (UTC) |
|---|---|---|---|
| `p9trace-index.html` | 940 | 65debf07ce4cb722a375b694e5ddcbbf7ecd7e241247fa2b3c27fc0d0bb71d51 | 03:55:53 |
| `Readme` | 618 | a12bbf70eb149bd909073c275fbebdf76e1e4d7010a0f34d49f20b01daf6ca5c | 04:10:05 |
| `format.txt` ("Last modified: 10/02/2001") | 7,769 | 8ac24471af1f9a72f310b7f0f8ba9ff5feef70055b3eec7ec59b0ee4f239b512 | 04:09:55 |
| `bootes-listing.html` | 11,300 | 6cac3b568c1a7500c63ec4cf0fe4782ea15f168df122dbc317fef08ce92a3402 | 04:09:56 |
| `emelie-listing.html` | 6,854 | eee7017095fe3e90aed1f6d4d5c9df60500b41569b452e15ed18594c714db8da | 04:09:58 |

**Passages.**

- SNIA listing (`T9-S3-02/iotta-traces-static.html`): "Plan 9 Traces | This is a time series set of "snapshots" of the contents of the Plan 9 file servers at Bell Labs. One snapshot per day for over ten years. The snapshots were taken on two different machines: bootes and emelie. See the Venti paper for more information. … | 1990 - 2001 | about 11 years | 0 Bytes".
- `format.txt`: "The trace files contain a condensed version of the data blocks of a plan 9 file system. For each block in the file system, there is a corresponding record in the trace files." … "Each record contains a number of fields that are common to all blocks including the address of the block, its type, various sizes, the file it is associated with and a hash of the block's original contents."
- `bootes-listing.html`: "bootes00 2001-11-15 00:00 41M … bootes01 … 46M … bootes02 … 55M".

**Coverage.**
- T9 (c): context. Daily block-level snapshots of two shared research file servers, not personal desktops, with a per-block content hash, so day-to-day change is computable at block granularity.
- Platform: Plan 9 file servers. Date: 1990–2001.
- T9 (b): does not cover desktops.
- Licence: none stated.

**Observation status.** Two server time series.

**Reader's own computation.** None.

### T9-S3-11 — Matt Mahoney's "10 GB Compression Benchmark" data set (10gb.zpaq) and "Incremental Compression Benchmark" (MinGW 4.4.0 → 4.5.0)

**Citation.** M. Mahoney, "10 GB Compression Benchmark", https://mattmahoney.net/dc/10gb.html ("Benchmark created July 28, 2013. Last update July 25, 2019."); M. Mahoney, "Incremental Compression Benchmark", https://mattmahoney.net/dc/mingw.html ("Last updated Jan. 13, 2014").

**Copy read.**

| File | Size (B) | SHA-256 | Accessed (UTC) |
|---|---|---|---|
| `10gb.html` | 49,849 | 72df209338f2a30b41cec8708a64ab6f85f448bcaf473c68efa45610be308a02 | 03:56:06 |
| `mingw.html` | 20,869 | adcc477d08c6790b0fc00979980b67149ab2f887591f87b9bb273822aaf39496 | 03:56:07 |

The data (`10gb.zpaq`, 3,701,584,921 B per the page) was not downloaded; the page's own manifest tables are quoted.

**Passages.**

- `10gb.html`, "Test Data Description": "The test data is designed to test archivers in realistic backup scenarios with lots of already-compressed or hard to compress files and lots of duplicate or nearly identical files. It consists of exactly 10 GB (1010) bytes in 79,431 files in 4006 directories from my Windows laptop collected from 2009 to 2013. The archive preserves file dates but not attributes." (The "1010" is 10^10 with the superscript lost in text extraction.)
- `10gb.html`: "Size Name Description ---- --- ----------- 3240 hg19/ Human genome in FASTA format 1998 benchmarks/ Collection of data compression benchmarks 1584 mingw/ Several versions of MinGW g++ compiler 1212 www.mattmahoney.net/ Backup copy of my website in 2013 730 2011/ dc subdirectory of my website in 2011 678 progs/ Several open source applications 502 cygwin/ Cygwin version from 2009 52 zeropad File of all zero bytes".
- `10gb.html`: "Overall, the most common file types (sorted by total size in MB) and their compression ratios with zpaq -m2 after deduplication from 10 GB to 8.45 GB are as follows: Type Files Size Ratio … All 83437 10000 .4655 .fa 93 3199 .3489 . 27128 1665 .3433 .zip 461 1035 .9759 .exe 1219 763 .3605 .dll 1672 529 .3559 .a 4665 504 .1190 .pmd 4 410 .9504 .jpg 1491 236 .9455 .zpaq 13 193 1.0001 .h 9377 148 .1455 .tar 5 85 .2052 .mo 1253 82 .2774 .lzma 123 73 .9365 .bmp 135 71 .5980 .pdf 157 57 .9010".
- `10gb.html`: "Comparison of data sets. 10GB 1GB 100MB … 3,701,584,921 424,346,384 44,304,455 Download size (zpaq) 10,000,000,000 1,000,000,000 100,000,000 Uncompressed size 79,431 1,524 788 Number of files 4,006 825 630 Number of directories 125,895 656,168 126,904 Average file size".
- `10gb.html`: "Compression ratios and + or - differences from 10GB. … .8446 +.0640 .9086 +.1308 .9754 Deduplication (zpaq) … .4797 +.0597 .5324 -.0030 .4767 tar|gzip … .3892 +.0248 .4140 -.0045 .3847 7zip 9.20".
- `10gb.html`, licence: "10gb.zpaq is copyright (C) 2013, Matt Mahoney. … You are granted permission to download these files for your own use. … Please do not use this data set for any purpose other than benchmarking data compression and archiving programs and related research."
- `mingw.html`: "The following test shows what happens when the 32 bit MinGW g++ compiler version 4.4.0 is backed up, followed by version 4.5.0, which has many files (40% of total size) in common, and then both directories are extracted." … "The test data (88 MB, compressed with zpaq -method 2) consists of two directories: mingw44 - 116 MB in 1409 files in 215 directories. mingw45 - 159 MB in 1522 files in 362 directories. There is a mix of text (headers, documentation) and binary (programs and libraries)." Table header row: "uncompressed 116,655,760 276,348,369".

**Coverage.**
- T9 (d): covers. An archiver and backup benchmark input taken from one real Windows laptop (2009–2013): 10^10 bytes, 79,431 files, 4,006 directories, with a published type-by-bytes table, a per-type compressibility table (zpaq -m2), a deduplication ratio (0.8446 on 10 GB) and 1 GB and 100 MB random subsets.
- T9 (c): the Incremental benchmark is a two-step backup input, MinGW 4.4.0 (116,655,760 B, 1,409 files) then 4.5.0 added (276,348,369 B cumulative, 1,522 files), with about 40 % of bytes in common.
- Platform of origin: Windows laptop. Licence: stated above.

**Observation status.** One file set from one machine, with named contents.

**Reader's own computation.** None.

### T9-S3-12 — Silesia compression corpus (Deorowicz, 2003)

**Citation.** S. Deorowicz, "Silesia compression corpus", https://sun.aei.polsl.pl/~sdeor/index.php?page=silesia; archive `corpus/silesia.zip`.

**Copy read.**

| File | Size (B) | SHA-256 | Accessed (UTC) |
|---|---|---|---|
| `silesia-page.html` | 19,080 | cb157f8284ae7546809ff9dc3100244a7bd08d0623ab6f923da075b0c44168ce | 03:56:41 |
| `silesia.zip` (https://sun.aei.polsl.pl/~sdeor/corpus/silesia.zip) | 68,182,744 | 0626e25f45c0ffb5dc801f13b7c82a3b75743ba07e3a71835a41e3d9f63c77af | 03:57:08 |

**Passages.**

- Page: "The intention of the Silesia corpus is to provide a data set of files that covers the typical data types used nowadays. The sizes of the files are between 6 MB and 51 MB." … "In our opinion, nowadays the two fastest growing types of data are multimedia and databases. The former are typically compressed with lossy methods so we do not include them in the corpus."
- Page, contents table ("Filename | Description | Type | Source | Raw size [B] | Bzipped size [B]"): "dickens | Collected works of Charles Dickens | English text | … | 10,192,446 | 2,799,528"; "mozilla | Tarred executables of Mozilla 1.0 (Tru64 UNIX edition) | exe | … | 51,220,480 | 17,914,392"; "mr | Medical magnetic resonanse image | picture | … | 9,970,564 | 2,441,280"; "nci | Chemical database of structures | database | … | 33,553,445 | 1,812,734"; "ooffice | A dll from Open Office.org 1.01 | exe | … | 6,152,192 | 2,862,526"; "osdb | Sample database in MySQL format from Open Source Database Benchmark | database | … | 10,085,684 | 2,802,792"; "reymont | … | Polish pdf | … | 6,627,202 | 1,246,230"; "samba | Tarred source code of Samba 2-2.3 | src | … | 21,606,400 | 4,549,790"; "sao | The SAO star catalog | bin data | … | 7,251,944 | 4,940,524"; "webster | The 1913 Webster Unabridged Dictionary | html | … | 41,458,703 | 8,644,714"; "xml | Collected XML files | html | … | 5,345,280 | 441,186"; "x-ray | X-ray medical picture | Hospital image | … | 8,474,240 | 4,051,112"; "Total | 211,938,580 | 54,506,808".

**Coverage.**
- T9 (d): covers. A compressor corpus of 12 files totalling 211,938,580 B, 6–51 MB each, of types text, executable, database, medical image, source tar and XML; it excludes lossy multimedia by design.
- It is a set of concatenated single files, not a directory tree of user files.
- Licence: none stated on the page.

**Observation status.** A fixed corpus.

**Reader's own computation.** `unzip -l silesia.zip` → 12 members, 211,938,580 bytes, member dates 2000-11-30 to 2003-03-20; the member sizes equal the page's table.

### T9-S3-13 — Canterbury Corpus family: Canterbury, Large, Artificial, Miscellaneous and Calgary corpora (University of Canterbury)

**Citation.** "The Canterbury Corpus", https://corpus.canterbury.ac.nz/descriptions/ ("This page last updated Monday, January 08, 2001 by Matt Powell"); archives under `resources/`. The page links the DCC '97 paper (R. Arnold, T. Bell).

**Copy read.**

| File | Size (B) | SHA-256 | Accessed (UTC) |
|---|---|---|---|
| `descriptions.html` | 16,928 | 6bfe5c032e6f5518773df407e96de0543a09f3c89afc94a35dfa3bcffdd2090c | 03:57:25 |
| `resources.html` (the `resources/` index, 403) | 326 | c52981893ddeec73ef09c2280f2e7d2791393e6dc8e8c34ad7ebb94b41d43e62 | 03:57:26 |
| `cantrbry.tar.gz` | 739,071 | f140e8a5b73d3f53198555a63bfb827889394a42f20825df33c810c3d5e3f8fb | 03:57:42 |
| `large.tar.gz` | 3,258,648 | 7df00ff4cb8c9ce4187d9fa4100aa88208a72d9a227e3cd8bab23b71971eaf41 | 03:57:48 |
| `calgary.tar.gz` | 1,070,276 | e109eebdc19c5cee533c58bd6a49a4be3a77cc52f84ba234a089148a4f2093b7 | 03:58:00 |
| `artificl.tar.gz` | 76,723 | cc1818a084d61fe693fe2a9db7312da25fdb4b54313502a6920abf692b7a47ab | 03:58:04 |
| `misc.tar.gz` | 470,592 | 7ffa1217087e9508d24f869cbea6c404ca0910729e0b9cdae6ef2c2df3e72ea5 | 03:58:05 |

**Passages.**

- "This collection is the main benchmark for comparing compression methods. … This collection was developed in 1997 as an improved version of the Calgary corpus. The files were chosen because their results on existing compression algorithms are "typical", and so it is hoped this will also be true for new methods."
- Canterbury, 11 files: "alice29.txt | text | English text | 152089 | asyoulik.txt | play | Shakespeare | 125179 | cp.html | html | HTML source | 24603 | fields.c | Csrc | C source | 11150 | grammar.lsp | list | LISP source | 3721 | kennedy.xls | Excl | Excel Spreadsheet | 1029744 | lcet10.txt | tech | Technical writing | 426754 | plrabn12.txt | poem | Poetry | 481861 | ptt5 | fax | CCITT test set | 513216 | sum | SPRC | SPARC Executable | 38240 | xargs.1 | man | GNU manual page | 4227".
- Large, 3 files: "E.coli | E.coli | Complete genome of the E. Coli bacterium | 4638690 | bible.txt | bible | The King James version of the bible | 4047392 | world192.txt | world | The CIA world fact book | 2473400".
- Calgary: "This was developed in the late 1980s, and during the 1990s became something of a de facto standard for lossless compression evaluation. … There are 14 files in this corpus". Artificial: "files containing little or no repetition (e.g. random.txt), files containing large amounts of repetition (e.g. alphabet.txt), or very small files (e.g. a.txt)". Miscellaneous: "pi.txt | pi | The first million digits of pi | 1000000".

**Coverage.**
- T9 (d): covers. Small single-file compressor corpora of 1-byte to 4.6 MB files, typed as text, source, spreadsheet, fax image, executable, genome, synthetic and digits, from 1989 to 2000.
- Not a user file tree. Licence: none stated.

**Observation status.** Fixed corpora.

**Reader's own computation.** `tar -tvzf <set>.tar.gz | awk '{n++; s+=$5} END{print n, s}'`:
- cantrbry: 11 files, 2,810,784 B.
- large: 3 files, 11,159,482 B.
- calgary: 18 files, 3,251,493 B. The tarball also carries paper3–paper6, which the page says are "no longer in the corpus".
- artificl: 4 files, 300,001 B.
- misc: 1 file, 1,000,000 B.

### T9-S3-14 — Large Text Compression Benchmark data: enwik8 and enwik9 (Mahoney)

**Citation.** M. Mahoney, "Large Text Compression Benchmark", https://mattmahoney.net/dc/text.html ("Last update: Sept 15, 2026"), and "About the Test Data", https://mattmahoney.net/dc/textdata.html ("Last update: Sept. 1, 2011").

**Copy read.**

| File | Size (B) | SHA-256 | Accessed (UTC) |
|---|---|---|---|
| `text.html` | 693,875 | 7ea13d26b7c8e67427361a333dfe0eae82981f4e24cf1b7fddeb6affaaf76866 | 04:02:34 |
| `textdata.html` | 35,391 | b91ee875eb9d9b17ba825dc59ad8789b65f6d12661df0e5dffcb578668ac6822 | 04:02:33 |

HEAD only for the data: `enwik8.zip` "content-length: 36445475", `enwik9.zip` "content-length: 322592222" (both "last-modified: Fri, 24 Feb 2023"). Not downloaded.

**Passages.**

- `textdata.html`: "The test data for the Large Text Compression Benchmark is the first 10^9 bytes of the English Wikipedia dump on Mar. 3, 2006." (superscript rendered here as ^). … "enwik8 100,000,000 a1fa5ffddb56f4953e226637dabbb36a … enwik9 1,000,000,000 e206c3450ac99950df65bf70ef61a12d …" … "The data is UTF-8 encoded XML consisting primarily of English text. enwik9 contains 243,426 article titles, of which 85,560 are #REDIRECT to fix broken links, and the rest are regular articles."
- `text.html` (raw HTML): "first 10<sup>9</sup> bytes of enwiki-20060303-pages-articles."

**Coverage.** T9 (d): covers, for compressors only. One text file of 10^8 or 10^9 bytes of Wikipedia XML (2006). Not a file tree; not representative of a user's file mix. Licence: not stated in the saved pages.

**Observation status.** A fixed corpus.

**Reader's own computation.** None.

### T9-S3-15 — Squash Compression Benchmark data sets (quixdb/squash-benchmark)

**Citation.** E. Nemerson et al., "Squash Compression Benchmark", https://quixdb.github.io/squash-benchmark/ and GitHub `quixdb/squash-benchmark` (MIT), commit 37ee14532dea32ffd6145eec5ab5a4ed85896f4f (2017-04-19).

**Copy read.**

| File | Size (B) | SHA-256 | Accessed (UTC) |
|---|---|---|---|
| `squash-benchmark-index.html` | 46,349 | ae98e08c958c4fcbd1814cfd4cd3bcb59ee93e100a39dcd669e871a20520f87b | 04:03:03 |
| `squash-benchmark.js` | 49,359 | 101a3b9edb8c7420c092207acd35a2a43a374a8ef7c777a621588782bce83da2 | 04:03:15 |
| `repo-contents-37ee145.json` (`gh api repos/quixdb/squash-benchmark/contents?ref=37ee145…`) | 32,662 | 85697c2f74401abd987e22f8c13d1e293a3d618e1f4d62c607490d1628f8bfde | 04:03 |

**Passages.**

- `squash-benchmark.js:71–76`: "var datasets = [" / "{ id: 'alice29.txt'," / "source: 'Canterbury Corpus'," / "sourceUrl: 'http://corpus.canterbury.ac.nz/descriptions/#cantrbry'," / "description: 'English text'," / "size: 152089 },".
- `squash-benchmark.js`, the non-corpus entries: "{ id: 'fireworks.jpeg', source: 'Snappy', … description: 'A JPEG image', size: 123093 }"; "{ id: 'geo.protodata', source: 'Snappy', … description: 'A set of Protocol Buffer data', size: 118588 }"; "{ id: 'paper-100k.pdf', source: 'Snappy', … description: 'A PDF', size: 102400 }"; "{ id: 'urls.10K', source: 'Snappy', … description: 'List of 10000 URLs', size: 702087 }"; "{ id: 'enwik8', source: 'Large Text Compression Benchmark', … size: 100000000 }".

**Coverage.** T9 (d): covers, for compressors. A union of the 11 Canterbury files, the 12 Silesia files, enwik8 and four files from Snappy's testdata (JPEG, protobuf, PDF, URL list). The repository ships each as `.xz`. Not a user file tree.

**Observation status.** A fixed corpus.

**Reader's own computation.** From `squash-benchmark.js` lines 71–212: 28 data sets totalling 315,795,532 B; by source 11 Canterbury, 12 Silesia, 1 Large Text Compression Benchmark, 4 Snappy.

### T9-S3-16 — MaximumCompression "Multiple file compression" (MFC) test set (Bergmans; archived page)

**Citation.** W. Bergmans, maximumcompression.com, "Summary of the multiple file compression benchmark tests", `data/summary_mf.php`, read from the Internet Archive capture of 2013-03-28 06:04:04.

**Copy read.**

| File | Size (B) | SHA-256 | Accessed (UTC) |
|---|---|---|---|
| `wayback-20130328060404-summary_mf.php` (https://web.archive.org/web/20130328060404/http://www.maximumcompression.com/data/summary_mf.php) | 159,198 | 647100126fab151219fea50df389b17964939cea7447eb2cc21430748f82b259 | 04:02:18 |
| `index.html` (the live www.maximumcompression.com/, now unrelated content) | 68,750 | 61a7050598d28af81da2ba6e161da60f95a0736f7c7bc9f1a49f8af5c9eaeaef | 04:01:27 |

The live `data/summary_mf.php` returned 404.

**Passages.**

- "File type : Multiple file types (46 in total) | # of files to compress in this test : 510 | Total File Size (bytes) : 316.355.757 | Average File Size (bytes) : 620,305 | Largest File (bytes) : 18,403,071 | Smallest File (bytes) : 3,554".
- "This test is designed to model 'real-world' performance of lossless data compressors. The test set contains a mix of different file types which are chosen with 'What do people use archivers for the most' in mind. The testset should contain data, weighted (in both type and proportion of files in the set) by how often these files are used for compression by normal users using compression software."
- "Filetype(s) | Description | % of total | # of files | TOC, MBX | Eudora mailboxes | 12.31 | 16 | EXE, DLL, OCX, DRV | Executables | 10.99 | 35 | TXT, RTF, DIC, LNG | Text files in several languages | 10.21 | 41 | BMP, TIFF | Bitmaps/TIF images | 7.88 | 15 | LOG | Log files | 6.34 | 6 | HTM, PHP | HTML files | 6.13 | 19 | DOC | MS Word files | 6.08 | 30 | C, CPP, PAS, DCU | Source Code | 6.00 | 235 | MDB, CSV | Databases | 4.26 | 7 | HLP | Windows Help files | 4.23 | 7 | CBF, CBG | Precompressed chess-databases | 3.55 | 2 | WAV | Wave soundfiles | 3.45 | 9 | XLS | XLS Spreadsheets | 2.41 | 16 | PDF | Adobe Acrobat document | 1.59 | 6 | TTF | True Type Fonts | 1.15 | 15 | DEF | Virus definition files | 1.10 | 3 | JPG, GIF | Image files | 0.53 | 9 | CHM | Precompressed help files | 0.49 | 2 | INI, INF | INI files | 0.42 | 10 | Others | DAT,JAR,M3D,SYS,PPT,MAP,WP,RLL,RIB.. | 10.88 | 27".

**Coverage.**
- T9 (d): covers, as a description only. An archiver test set of 510 files, 316,355,757 B, 46 types, with the share of bytes and file count per type group, chosen by the author to mimic what users archive. Platform of origin: Windows file types.
- The files themselves were not published for download on the saved page.
- Date: the capture is of 2013; when the set was built is not stated.
- Licence: n/a.

**Observation status.** One author-chosen file set.

**Reader's own computation.** None.

### T9-S3-17 — SqueezeChart archiver benchmark test sets (Busch, 2018 revision)

**Citation.** S. Busch, "Squeeze Chart – Lossless Data Compression Benchmarks", https://www.squeezechart.com/, spreadsheet `SqueezeChart2018web.xlsx` ("Revision 8.2 (Web Version)", 2018-10-31).

**Copy read.**

| File | Size (B) | SHA-256 | Accessed (UTC) |
|---|---|---|---|
| `index.html` | 5,325 | 91d9975a88db2f33c2414d7359382a04006883ba9a583988b6cdc01a764b0af9 | 04:10:20 |
| `SqueezeChart2018web.xlsx` (server `Last-Modified: Wed, 31 Oct 2018 19:54:12 GMT`) | 1,115,856 | c44af9c5cae6254a6e277ecd9bc17284de1c434ead96d604ab79c9196bcc9b79 | 04:10:35 |

Read with openpyxl in a scratchpad venv.

**Passages.**

- `index.html`: "All archivers have to run over the the same test data and are rated by the size of the resulting archives. In the main test we have 9 testsets."
- Sheet "FAQ", rows 19–48: "APP | http://www.compressionratings.com/files/squeezechart_app.7z | an open testset that consisrs of the portable free open-sourced office suite called "Libre Office"" … "AUDIO | … an open testset that includes 12 .WAV files (16-bit stereo) licensed under creative commons license." … "Camera RAW | … an open testset that includes 25 camera raw images from 25 different cameras." … "GUTENBERG | … all contents from the Project Gutenberg ISO | ‣ 34,9% of this testset are .JPEG images" … "INSTALLER | … a selection of about 25% InnoSetup/Nullsoft, 25% InstallShield, 25% Windows Installer/MSI and 25% WISE Installer/GZIP/ZIP SFX setups" … "MOBILE | … a collection of public domain .JPEG, .MP3, .MP4, .MTS including some .JAR from sourceforge.net and .EPUB from http://gutenberg.org | This test set indicates an archiver's skill to serve as lossless backup solution for data from mobile devices." … "SOURCES | … a collection of free sourcecodes such as those from 7-Zip 4.42, GIMP 2.3.1, Lazarus 0.9.20, Stellarium 0.8.2 and more." … "XML | … the first 100 MB of wikipedia dumps in 10 languages".
- Sheet "PRACTICAL CHART", row 8 header "APP | AUDIO | CAMERA RAW | GUTENBERG | INSTALLER | MOBILE | PGM / PPM | SOURCES | XML" and row 12 "UNCOMPRESSED SIZE | 321.69350998072196 | 327811342 | 606681890 | 577835051 | 709240453 | 609139052 | 492103406 | 633482445 | 200001544 | 1000000000"; rows 3–5: "Test Machine Specifications: … * Intel Core i7 (Sandy Bridge) … * 16 GB RAM (DDR-3 @ 1600 MHz), SSD (SATA-3)".

**Coverage.**
- T9 (d): covers, as descriptions and sizes only. Nine archiver test sets with uncompressed sizes (APP 327,811,342 B … XML 1,000,000,000 B) and type notes, including a "MOBILE" set framed as backup of mobile-device data.
- File counts are not given.
- The download links are dead (row 33), so no contents or listing could be read.
- Licence: per set, as quoted ("open testset", "licensed under creative commons", "public domain").

**Observation status.** Author-chosen sets.

**Reader's own computation.** None.

### T9-S3-18 — deajan/backup-bench: Linux-kernel checkouts as a four-step backup series, plus a private qcow2 set

**Citation.** O. (deajan), "backup-bench — Quick and dirty backup tool benchmark with reproducible results", GitHub `deajan/backup-bench` (BSD-3-Clause), commit 4a0ff4f114dafb8e59ebe50bf14333d75ca74ac1 (2026-08-13). Result rounds dated 2022-08-19, 2022-09-06 and 2022-10-02.

**Copy read.**

| File | Size (B) | SHA-256 | Accessed (UTC) |
|---|---|---|---|
| `README.md` | 23,842 | 12d2b530e03bee8f051e02b4eae55f37cb6df33b050a4a1de3f89662de316123 | 03:58:26 |
| `HOWTO.md` | 3,663 | c670e4336d541e915c99473e88b4a9b6dc47d4f00c1a9f8c92f7249aedc3ddce | 03:58:26 |
| `RESULTS-20220819.md` | 7,056 | 5f799f11056420deab3d975e211034036f78d292d91501ed5baaeec74ba336da | 03:58:27 |
| `RESULTS-20220906.md` | 6,396 | dc859ed2b6ad5ba03deeec6ad19175cbc073a1dcc197440db38d707b333c279a | 03:58:27 |
| `CHANGELOG.md` | 1,516 | e6ca0c470dcdd5899d8cd079dd70ed6c56862fdb2d1abdfe0ba10522dcdee20b | 03:58:27 |
| `backup-bench.sh` (script/) | 65,552 | 32eefd5c64d5260071bf0ea9a622e08aa223c4bdc00f7275eca74ea2b2bedddb | 03:58:48 |
| `backup-bench.conf` (script/) | 3,661 | 3f69e58b9d966259e8f39e13b2aa7fe58492df53b68f7b62a5ac3da9b5bfa7c4 | 03:58:49 |

**Passages.**

- `README.md:19–20`: "We'll use a quite big (and popular) git repo as first dataset so results can be reproduced by checking out branches (and ignoring .git directory). I'll also use another (not public) dataset which will be some qcow2 files which are in use."
- `README.md:125–126`: "Linux kernel sources, initial git checkout v5.19, then changed to v5.18, 4.18 and finally v3.10 for the last run. Initial git directory totals 4.1GB, for 5039 directories and 76951 files. Using `env GZIP=-9 tar cvzf kernel.tar.gz /opt/backup_test/linux` produced a 2.8GB file. Again, using "best" compression with `tar cf - /opt/backup_test/linux | xz -9e -T4 -c - > kernel.tar.bz` produces a 2.6GB file".
- `README.md:112`: "Source system: Xeon E3-1275, 64GB RAM, 2x SSD 480GB (for git dataset and local target), 2x4TB disks 7.2krpm (for bigger dataset), using XFS, running AlmaLinux 8.6".
- `README.md:135–143` (2022-10-02, local): "| backup 1st run | 9 | 41 | 55 | 10 | 23 | 32 |" … "| size 1st run | 213268 | 257300 | 265748 | 259780 | 260520 | 360200 |" … "| size 4th run | 655836 | 660812 | 680092 | 666408 | 668404 | 894984 |" (columns bupstash 0.11.1, borg 1.2.2, borg_beta 2.0.0b2, kopia 0.12.0, restic 0.14.0, duplicacy 2.7.2).
- `README.md:186`: "Source data are 8 qemu qcow2 files, and 7 virtual machines description JSON files for a total of 366GB."
- `backup-bench.conf:27–28`: "GIT_DATASET_REPOSITORY="https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git"" / "GIT_TAGS=(v5.19 v5.18 v4.18 v3.10)  # List of tags to backup".
- `backup-bench.sh:963–965`: "size=$(${REMOTE_SSH_RUNNER} du -cs "${TARGET_ROOT}/${backup_software}" | tail -n 1 | awk '{print $1}')" / "size=$(du -cs "${TARGET_ROOT}/${backup_software}" | tail -n 1 | awk '{print $1}')"; `:1110`: "echo 3 > /proc/sys/vm/drop_caches       # Make sure we drop caches (including zfs arc cache before every backup)"; `:697`: "… create --compression zstd,3 --exclude 're:\.git/.*$' …".

**Coverage.**
- T9 (d) and (c): covers. A reproducible backup-tool input: a Linux kernel working tree checked out at four tags in sequence, v5.19 → v5.18 → v4.18 → v3.10, with `.git` excluded by every tool. The first backup is the full tree and the later ones are the change between tags.
- The README gives the directory and file count of the "initial git directory" (4.1 GB, 5,039 directories, 76,951 files, which include `.git`). Compressibility of the whole: gzip -9 to 2.8 GB, xz -9e to 2.6 GB.
- Repository size after each run is `du -cs`; the unit is not stated in the README.
- The second set (366 GB of qcow2 images) is private.
- Platform: AlmaLinux 8.6 on a Xeon server with SATA SSDs.

**Observation status.** One machine named; subject named (tool versions, tags); window by date of each result round.

**Reader's own computation.** None.

### T9-S3-19 — gilbertchen/benchmarking: Linux code base at 12 monthly commits (Jul 2016 – Jun 2017) and a CentOS 7 VirtualBox image, as backup inputs

**Citation.** G. Chen, "benchmarking — A performance comparison of Duplicacy, restic, Attic, and duplicity", GitHub `gilbertchen/benchmarking` (MIT), commit b56d7e7f9771c9259f5c4afc0d7af92b2470dbc8 (2017-09-28).

**Copy read.**

| File | Size (B) | SHA-256 | Accessed (UTC) |
|---|---|---|---|
| `README.md` | 12,996 | 53a6c772340174731a84b530d2d5c105ff78238adec87ecebe56319b3b2caef0 | 03:59:08 |
| `linux-backup-test.sh` | 4,729 | 6eec4ba145e28b81698ca09fc28c1481797ce8524f4e51e9c40aa69d92a85e5f | 03:59:08 |
| `vbox-backup-test.sh` | 3,944 | 729bd871389497e173abdda0b60d6509ecb7c076c02343f840bdfca8db6eff9d | 03:59:08 |
| `common.sh` | 1,434 | 75d9ba92b37c1ae77c3ddfcce98f179ebf0368e29944af568256455ca9b8ee74 | 03:59:09 |

**Passages.**

- README: "All tests were performed on a Mac mini 2012 model running macOS Sierra (10.12.3), with a 2.3 GHZ Intel i7 4-core processor and 16 GB memory."
- README: "The first dataset is the [Linux code base](https://github.com/torvalds/linux) mostly because it is the largest github repository that we could find and it has frequent commits (good for testing incremental backups). Its size is 1.76 GB with about 58K files, so it is a relatively small repository consisting of small files … To test incremental backup, a random commit on July 2016 was selected, and the entire code base is rolled back to that commit. After the initial backup was finished, other commits were chosen such that they were about one month apart."
- `linux-backup-test.sh:120–153`: "git checkout -f 4f302921c1458d790ae21147f7043f4e6b6a1085 # commit on 07/02/2016" … "git checkout -f 57caf4ec2b8bfbcb4f738ab5a12eedf3a8786045 # commit on 06/05/2017" (12 checkouts).
- README: "Initial backup | 224MB | 631MB | 259MB | 183MB |" … "12th backup | 834MB | 2.2GB | 869MB | 294MB |" (storage after each backup; columns Duplicacy, restic, Attic, duplicity).
- README: "The second test was targeted at the other end of the spectrum - a dataset with fewer but much larger files. … The base disk image is 64 bit CentOS 7, downloaded from http://www.osboxes.org/centos/. Its size is about 4 GB … The first backup was performed right after the virtual machine had been set up without installing any software. The second backup was performed after installing common developer tools using the command `yum groupinstall 'Development Tools'`. The third backup was performed after a power on immediately followed by a power off."

**Coverage.**
- T9 (d) and (c): covers. Two public backup-tool inputs with defined change steps. (1) The Linux tree at 1.76 GB and about 58K files (`.git` excluded), then 11 monthly commit steps; the growth of each tool's storage per step is published. (2) A roughly 4 GB CentOS 7 VM disk image with two change steps (a package-group install, then a boot and shutdown).
- Platform of the run: macOS Sierra, Mac mini 2012.

**Observation status.** One machine; subject and steps named; 2017.

**Reader's own computation.** None.

### T9-S3-20 — borgbase/benchmarks "Test v2" (Dec 2022): Ubuntu ISO, Visual Genome images and a Wikidata XML dump as backup input

**Citation.** BorgBase, "Backup Benchmarks", GitHub `borgbase/benchmarks`, commit 16e6e8c70ee34bb9bf0928ebb85e1c6dc8478e1c (2022-12-10); no licence file.

**Copy read.**

| File | Size (B) | SHA-256 | Accessed (UTC) |
|---|---|---|---|
| `README.md` | 4,533 | 9041b9684ff5ffd72f70d133f7b9544ed0f6595fc7ea1308b0bd80c6e28ace10 | 04:00:47 |
| `tests.sh` (v2/) | 1,569 | 5cbac827ca5cbe00df9bcfa8076a2a078622933dd412cb9fa837ed5a529fd287 | 04:00:57 |
| `de-normal-lat-borg-20-final-size.txt` (v2/results/de-normal-lat/borg-20/final-size.txt) | 1,253 | 7007d09e261c7b93617194b5e521c9e3575bc08ced2da4e5be9adbde9739c304 | 04:00:57 |

**Passages.**

- README: "Test data: 19.5 GB total, 43921 files / Corpus part 1: / [ubuntu-22.10-desktop-amd64.iso](…), 3.8 GB / [Visual Genome](…), images part 2, 5.5 GB / Corpus part 2: / [wikidatawiki-20221201-pages-articles-multistream10.xml-p13998368p15498367.bz2](…), uncompressed, 11 G".
- README: "initial backup of corpus part 1 (create-1) / subsequent backup with corpus part 2 added (create-2) / subsequent backup without new data (create-3) / pruning 50% (prune-1)".
- README: "Backup client specs: 1 Core, 30GB SSD Storage, 1GB Memory, 1G network / VPS hosted with OneProvider in Sydney and Nuremberg"; "OS: Debian GNU/Linux 11 (bullseye)".
- `final-size.txt`: "Command line: ./bin/borg-20 create --compression zstd initial corpa-1 / Number of files: 43904 / Original size: 9.59 GB / Deduplicated size: 1.12 kB" … "Command line: ./bin/borg-20 create --compression zstd second corpa-1 corpa-2 / Number of files: 43905 / Original size: 20.90 GB / Deduplicated size: 11.30 GB".

**Coverage.** T9 (d) and (c): covers. A public backup-tool input of 43,904 files and 9.59 GB (one ISO plus the Visual Genome JPEG images), then one step adding one 11 GB XML file, then an unchanged step. Its type mix is dominated by already-compressed images and an ISO. Platform of the run: Debian 11 VPS, 1 vCPU.

**Observation status.** One machine class; subject named; December 2022.

**Reader's own computation.** None.

### T9-S3-21 — DedupBench "DEB" data set: 62 Bitnami VM images (Kaggle `sreeharshau/vm-deb-fast25`)

**Citation.** S. Udayashankar, A. Baba, S. Al-Kiswany, "VM Images for Deduplication" (DEB), Kaggle `sreeharshau/vm-deb-fast25`, version 1, updated 2025-01-23, CC0; used in "VectorCDC", USENIX FAST 2025, and in DedupBench (GitHub `UWASL/dedup-bench`, Apache-2.0, commit 8e2697cbf6332ac5da6dc615bfab82a720e820e4).

**Copy read.**

| File | Size (B) | SHA-256 | Accessed (UTC) |
|---|---|---|---|
| `kaggle-api-view.json` | 5,109 | 6c5e8d5fc2c8411b352003c092cc7abaeaf882e4d3f3b692686c7cd19ad59bc6 | 04:09:16 |
| `kaggle-api-list-files.json` (page 1) | 8,365 | 6ffe1c1a439c4789ee36b427b883273522982581dd69b073b886fac45084f80b | 04:09:16 |
| `kaggle-api-list-files-p2.json` | 8,343 | 4e21f89cbfdb4ff87907b49f93531f56ced7f010c402a9b1df3fe72b986b48d0 | 04:09:28 |
| `kaggle-api-list-files-p3.json` | 7,722 | fc04ad0af38a24771e7095b790d45215c41e995e7ea347fe162c499a74cc3826 | 04:09:29 |
| `kaggle-api-list-files-p4.json` | 793 | 6f506b6af06fb68efdf4a12f449066db5f77b900adae906fbf9f672a8951dd64 | 04:09:29 |
| `dedup-bench-README.md` | 12,622 | 9ede1075fad94250060c4a5f21ca3621c78b65a216f89f23f312897bd06385d3 | 04:09:39 |

The data (42.2 GB) was not downloaded; the manifest was.

**Passages.**

- `kaggle-api-view.json`: ""descriptionNullable":"This is a dataset of VM images from the VMWare marketplace, mainly intended for use within data deduplication projects. This dataset is compatible with the [DedupBench framework](https://github.com/UWASL/dedup-bench) on GitHub."", ""totalBytes":42198924800", ""licenseName":"CC0: Public Domain"", ""lastUpdated":"2025-01-23T18:07:21.363Z"".
- `kaggle-api-list-files.json`: "{"name":"bitnami-activemq-5.18.1-r3-debian-11-amd64.ova", … "totalBytes":555176448, …}".
- `dedup-bench-README.md:13`: "DedupBench is a benchmarking tool for data chunking techniques used in data deduplication."

**Coverage.** T9 (d): covers, as context. A published corpus for evaluating deduplication (backup-side chunking) made of server appliance VM images (Debian 11 guests), not user files.

**Observation status.** A fixed corpus.

**Reader's own computation.** Over the four saved list pages: 62 files, all `.ova`, 42,198,924,800 B in total (equal to `totalBytes`), 290,242,048 B (bitnami-memcached) to 1,795,583,488 B (bitnami-gitlab-ce).

## 3. Not found

- **T9 (b), a public per-file data set of Linux desktop or laptop home directories.** None found. The published per-file data sets of personal machines are Windows corporate PCs (T9-S3-02, -03, -04; 1998–2009) and one shared lab file system of students' homes (T9-S3-01, 2011–2015). For Linux desktops, only aggregate statistics exist (T9-S3-06: 42 GNU/Linux participants, median and mean only). Searches 8–14, 19. The Cardinal raw data behind T9-S3-06 is not deposited (searches 9–12). arXiv 2503.22089 (9 Windows users' 25 largest files) publishes no data (search 14).
- **T9 (b), a published extension or type mix of personal file collections as data.** Only the plain-text extension fields of the Microsoft Longitudinal data (T9-S3-03, not downloaded), the top-1000 extension table in the 1998 data (T9-S3-04) and the FSL Homes extensions (T9-S3-01, computed here for two users) were found. The Dinneen type-mix results exist only in the 2019 paper, not as data (search 10).
- **T9 (b), compressibility of personal file sets as data.** Only the FSL fs-hasher per-chunk ratio (T9-S3-01), and all eight 2012–2013 Homes snapshots read here carry the "none" constant 10. Mahoney's per-type zpaq ratios apply to one laptop's 10 GB set (T9-S3-11). No study data set found.
- **T9 (c), real backup-source data with change between consecutive backups for personal machines, other than FSL Homes.**
  - The UbuntuOne and NEC personal-cloud traces are unreachable (T9-S3-08; searches 16–18).
  - Duplicati's statistics carry only per-OS mean source size and file count, with overflowing sums (T9-S3-09).
  - Backblaze publishes no per-customer backup size or type data (search 19).
  - No released enterprise backup data (Symantec NetBackup, Data Domain) was found (searches 20–21).
  - Vendor change-rate figures found in search 24 are rules of thumb about SaaS or server backups, not data.
  - The public backup-tool inputs with defined change steps are synthetic series: kernel tags (T9-S3-18), monthly kernel commits and a VM image (T9-S3-19), and an added corpus part (T9-S3-20).
- **T9 (d), a standard corpus that is a realistic directory tree of user files with a public manifest.** Mahoney's 10 GB set (T9-S3-11) is the only downloadable one found: a single Windows laptop, 79,431 files. Its per-file manifest was not read because the archive is 3.7 GB, but its type table is quoted. The MaximumCompression MFC set (T9-S3-16) and the SqueezeChart sets (T9-S3-17) are described but not downloadable (search 33; the MFC files were never on the saved page). The other corpora are single-file compressor corpora (T9-S3-12…15).
- Walls on 2026-09-19:
  - SNIA IOTTA full trace files sit behind a licence form that asks for name, e-mail and company; it was not submitted.
  - The archive.org availability API answered 429.
  - The cloudspaces NEC and U1 links are dead: a 404 behind a TLS name mismatch, and an FTP connection failure.
  - compressionratings.com is parked.
  - maximumcompression.com now serves unrelated content.
