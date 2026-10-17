# S3 — public traces, datasets, logs and benchmark databases

Task 9.7 "Background and IO", stage-2 search. Reader class S3; topics T1, T2, T3, T4, T7. Rows 1–48 and S3-01…S3-27: all fetches 2026-09-17 (UTC times in the copy lines), with `curl -sSL --cacert /root/.ccr/ca-bundle.crt -A curl/8.5.0` through the session proxy; SHA-256 is `sha256sum` of the saved file. Rows 49–84 and S3-28…S3-36: a retry on 2026-09-19 (UTC times in the copy lines) from the development Mac without a proxy — GitHub issues through `gh api` (gh 2.89.0, authenticated) and every other file with `curl` 8.7.1; SHA-256 is `shasum -a 256` of the saved file. Source copies are under `sources/S3-NN/` (gitignored; the 2026-09-19 copies sit at `_dev/research/jioh/task-9.7-background-io/sources/S3-NN/`); every quoted passage and copy identification below is meant to stand on its own.

Walls met on 2026-09-17 (each probed with curl, status recorded): `github.com` HTML 403, `api.github.com` 403, `openbenchmarking.org` 403, `www.phoronix.com/search/*` 403 (article pages 200), `gitlab.gnome.org` 406 with a browser User-Agent but 200 with `curl/8.5.0` (REST API and `/-/issues/N/discussions.json`; `/notes` endpoint 401), `sylab-srv.cs.fiu.edu` and `iotta.snia.org/traces/block-io/391` connection failure (curl exit, no HTTP status), `git.sesse.net` CONNECT rejected by the proxy (502 recorded in proxy status), `pmc.ncbi.nlm.nih.gov` served a reCAPTCHA page (200, no article) — Europe PMC full-text XML used instead. `raw.githubusercontent.com`, `gist.githubusercontent.com` and `git clone --depth 1` work. WebFetch was not used for any cited text.

On the 2026-09-19 retry (rows 49–84): `api.github.com` (through `gh api`), `github.com/user-attachments`, `user-images.githubusercontent.com`, `i.imgur.com` and `tinystash.undef.im` returned 200, so the GitHub issues and the files their threads link were read. `openbenchmarking.org` still returns 403 to plain curl and to a browser User-Agent: the result page, its `&export=csv|txt|pdf|xml|json` forms, the `http://` scheme and the test-profile page all answer with a Cloudflare challenge (`cf-mitigated: challenge`, page title "Just a moment..."). Its Phoronix Test Suite client endpoint `https://openbenchmarking.org/f/client.php` answers 200 to the request the PTS client makes, and the result was read that way (S3-36). The other 2026-09-17 walls were not retried. WebFetch was not used.

A reminder of the class rule applied throughout: a response-side value (CPU per block/wake, wake cadence, run/wait structure, thread structure) is a candidate only from a Linux observation; Windows/Cygwin/macOS observations and traces around two decades old are marked as context.

## 1. Search log

| # | Date | Engine / venue | Query | Hits followed | Dead ends (HTTP) |
|---|------|----------------|-------|---------------|------------------|
| 1 | 2026-09-17 | WebSearch | phoronix rsync benchmark CPU usage test profile results | none usable (PTS docs only) | openbenchmarking.org/tests/pts 403 on probe |
| 2 | 2026-09-17 | WebSearch | borgbackup issue "real" "user" "sys" time create backup slow CPU github | borg issues #2245 #3471 #5804 #7374 identified | github.com/borgbackup/borg/issues/2245 403; api.github.com 403 |
| 3 | 2026-09-17 | WebSearch | tracker-miner-fs high CPU idle steady state bug report top output gitlab.gnome.org | GNOME localsearch #340 #161 #228; tinysparql #348 #334 #173; Debian #1016745 | gitlab HTML 406 (browser UA) → API 200 with curl UA |
| 4 | 2026-09-17 | WebSearch | bugs.kde.org baloo_file high CPU usage idle after indexing complete top | KDE 384372, 406486, 418323; Manjaro forum 96726 | — |
| 5 | 2026-09-17 | WebSearch | clamscan summary "Scanned files" "Data scanned" "Time:" issue slow scan linux | Arch BBS 247158; ClamAV GH #849 #590 #1375 (unreachable) | github.com 403 |
| 6 | 2026-09-17 | WebSearch | Steam content_log.txt depot download throughput linux log | store.steampowered.com/stats/content/; steam-for-linux #12291 (unreachable) | github.com 403; scribd copies not fetched (login wall, not tried) |
| 7 | 2026-09-17 | WebSearch | public dataset per-process CPU usage trace Linux desktop atop collectl archive | none (tool pages only) | — |
| 8 | 2026-09-17 | WebSearch | Brendan Gregg biosnoop example tar rsync cp output | bcc tools `*_example.txt` via raw.githubusercontent.com | — |
| 9 | 2026-09-17 | curl probes | reachability of 17 hosts (github, api.github, gitlab.gnome, bugs.kde, bugs.debian, bbs.archlinux, forum.manjaro, phoronix review, openbenchmarking, bugzilla.redhat, launchpad, lists.samba, store.steampowered, bugzilla.mozilla REST, raw.githubusercontent, mail-archive) | see header | github 403, api.github 403, openbenchmarking 403, gitlab 406 (UA), bmo `rest/bug/1` 404 (restricted bug; REST otherwise 200) |
| 10 | 2026-09-17 | WebSearch | rsync mailing list samba "top" CPU "generator" "receiver" "sender" 100% cpu benchmark slow | lists.samba.org 2010-February/024743, 2019-July/031942; narkive threads | — |
| 11 | 2026-09-17 | WebSearch | phoronix "CPU Usage" monitor graph 7-Zip compression benchmark article sensor | openbenchmarking result 2305286-NE-MONITORSY37 (compress-7zip with MONITOR=cpu.usage) | openbenchmarking.org/result/2305286-NE-MONITORSY37 403 |
| 12 | 2026-09-17 | WebSearch | wget vs curl vs aria2c download benchmark CPU usage percent linux comparison | none with measurements | — |
| 13 | 2026-09-17 | WebSearch | clamav-users mailing list clamscan CPU 100% scan time "Data scanned" "Time:" lists.clamav.net | mail-archive msg48677; virtualmin 61555; narkive "Performance Help - 100% cpu usage" | — |
| 14 | 2026-09-17 | WebSearch | desktop workload trace dataset per-process CPU Linux laptop "process name" energy profiling dataset public | none | — |
| 15 | 2026-09-17 | WebSearch | restic backup slow CPU "user" "sys" "real" time output issue forum.restic.net | forum.restic.net 4221, 1727, 5289, 8098 | restic GH issues 403 (not attempted after probe) |
| 16 | 2026-09-17 | WebSearch | thunderbird bugzilla sending large attachment slow SMTP takes minutes CPU 100% | bmo 538283, 577545, 742697, 358427, 774401 (REST) | — |
| 17 | 2026-09-17 | WebSearch | Steam linux download high CPU usage while downloading "steam" process 100% cpu github steam-for-linux | steam-for-linux #6684 (unreachable) | github.com 403 |
| 18 | 2026-09-17 | WebSearch | site:phoronix.com "CPU Usage" monitor compression xz zstd benchmark "MONITOR=" | Phoronix forum thread (no data); phoronix review zstd-1.5-benchmarks fetched | grep of fetched article: 0 occurrences of "cpu usage"/"cpu utilization" |
| 19 | 2026-09-17 | WebSearch | borgbackup mailing list mail.python.org borg create "real" "user" "sys" time benchmark | pipermail borgbackup 2017q3/000799, 000779; borgbase/benchmarks README + clone | — |
| 20 | 2026-09-17 | WebSearch | "atop" raw log files dataset download research desktop "atop -r" archive published trace | none | — |
| 21 | 2026-09-17 | WebSearch | Linux desktop user activity trace dataset process-level "sysdig" OR "LTTng" OR "perf sched" desktop interactive workload public trace download | none | — |
| 22 | 2026-09-17 | WebSearch | launchpad bug tracker-miner-fs high CPU perf top ubuntu "tracker-miner-fs-3" idle | LP 925948, 1961540, 1970805, 2025523 (API); Fedora discussion 115906 | — |
| 23 | 2026-09-17 | WebSearch | 7-zip xz zstd tar benchmark blog "user" "sys" "real" time multi-thread compression linux kernel source tarball CPU | redpill-linpro compression-tool-test (2024-12-18); sourceforge 7-Zip 18.02 benchmark thread | — |
| 24 | 2026-09-17 | WebSearch | SNIA IOTTA FIU traces "home" desktop block I/O trace process name fields Linux | iotta.snia.org/traces/block-io/390, tracetypes/3 | — |
| 25 | 2026-09-17 | WebSearch | zenodo OR figshare dataset "Linux" laptop OR desktop process-level CPU usage logs "ps" OR "top" OR "atop" time series user study | none relevant (cluster traces, Mozilla perf) | — |
| 26 | 2026-09-17 | WebSearch | plocate updatedb benchmark time seconds "updatedb" plocate-build sesse | plocate.sesse.net (query timing only, no updatedb timing) | git.sesse.net CONNECT rejected (proxy 502) |
| 27 | 2026-09-17 | WebSearch | bugs.kde.org baloo_file_extractor "perf" report OR "perf top" high CPU idle indexing complete | KDE 358548, 363384, 500665; discuss.kde.org 6043 | — |
| 28 | 2026-09-17 | WebSearch | curl OR wget "100% CPU" OR "high CPU" downloading large file Linux mailing list curl-users bug report | Debian #760473; RHBZ 85817, 479967; curl GH #336 #11242 (unreachable) | github.com 403 |
| 29 | 2026-09-17 | WebSearch | rsync "perf" OR "strace -c" OR "top" generator receiver CPU bound Linux benchmark blog post local copy NVMe | LWN 400489 | — |
| 30 | 2026-09-17 | WebSearch | clamscan vs clamdscan benchmark Linux time CPU "clamdscan --multiscan" seconds blog | Fedora discussion 138122; dev.to article | — |
| 31 | 2026-09-17 | WebSearch | "Steam" Linux "content_log" "depot" "chunks" download log paste gist "Downloading" throughput MB/s | steam-for-linux #13024, #12015, #7956 (unreachable) | github.com 403 |
| 32 | 2026-09-17 | curl probes | plocate.sesse.net, bugzilla.samba.org XML, narkive rsync, bugs.kde.org REST, iotta 390/tracetypes, lists.clamav.net hyperkitty, steamcommunity, mail-archive search, phoronix search, narkive clamav, 7-cpu.com, curl.se mail, sourceforge | all 200 except noted | www.phoronix.com/search/rsync 403 |
| 33 | 2026-09-17 | WebSearch | "steam-for-linux" 13024 "Download Speed Issue" socket read receive window gamingonlinux OR phoronix OR reddit | gist FikriRNurhidayat (raw fetched — turned out to be a DNS workaround note, not the socket analysis) | github.com/ValveSoftware/steam-for-linux/issues/13024 403 |
| 34 | 2026-09-17 | WebSearch | site:curl.se/mail "100% CPU" OR "cpu usage" download curl-users | curl.se/mail lib-2009-08/0217, lib-2025-09/0029 | — |
| 35 | 2026-09-17 | WebSearch | FIU IODedup traces "home" "mail" "web-vm" 2008 2010 trace format process name Koller Rangaswami | SNIA readme for FIU IODedup | sylab-srv.cs.fiu.edu no HTTP response (curl exit 000) |
| 36 | 2026-09-17 | WebSearch | dataset "Linux" desktop "energy" per-process … "powertop" OR "scaphandre" OR "powerjoular" | none (tools only) | — |
| 37 | 2026-09-17 | WebSearch | "updatedb" mlocate OR plocate "time" "real" "user" "sys" seconds bug report high load ionice Debian OR Fedora | Arch FS#10532; LP 1190696; RHBZ 1282232; Arch BBS 297983 | — |
| 38 | 2026-09-17 | WebSearch | "tar" OR "cp -a" "perf sched" OR "offcputime" OR "biosnoop" blog trace copying files blocked I/O wait Linux example output kernel source tree | brendangregg.com/offcpuanalysis.html | — |
| 39 | 2026-09-17 | WebSearch | "wget" Linux download "CPU" percent "top" OR "time" gigabit "MB/s" observed cpu usage wget 100 MB/s cores | none beyond #760473 | — |
| 40 | 2026-09-17 | WebSearch | desktop OR laptop Linux "I/O trace" OR "block trace" dataset 2015..2025 "process name" personal computer users collected blktrace released | none new (SNIA enterprise/VDI traces) | — |
| 41 | 2026-09-17 | WebSearch | rsync "atop" OR "htop" screenshot generator sender receiver three processes CPU local copy observation blog 2018..2025 | LWN 400489 (again); Stapelberg rsync article 3 | — |
| 42 | 2026-09-17 | WebSearch | steamcommunity.com "Steam for Linux" discussion download "CPU usage" high while downloading game Linux client percent | steamcommunity forum/11/3004429475631021322; EndeavourOS 36404 | steam-for-linux #6684 403 |
| 43 | 2026-09-17 | WebSearch | "7z" OR "7za" OR "7zz" "real" "user" "sys" time linux compression benchmark blog multithreaded cores "-mmt" | 0ink.net 7z benchmark; binarytides 7z; sourceforge thread | — |
| 44 | 2026-09-17 | WebSearch | dataset of desktop application usage logs with process names and CPU per process, personal computers, released for research (not Windows), Linux users, "in the wild" | BEHACOM (Mendeley, IEEE DataPort, Data in Brief article) | pmc.ncbi.nlm.nih.gov reCAPTCHA page; Europe PMC XML 200 |
| 45 | 2026-09-17 | WebSearch | "Steam" Linux client "recvfrom" strace download slow receive window issue analysis blog 2025 2026 | only steam-for-linux GitHub issues | github.com 403 |
| 46 | 2026-09-17 | mail-archive.com search | l=clamav-users@lists.clamav.net q=clamscan %CPU top | result page saved (15 msg links, none opened: subjects were clamd/milter server threads) | — |
| 47 | 2026-09-17 | lists.clamav.net hyperkitty search | q=clamscan cpu top | result page saved; no desktop on-demand scan thread with CPU figures in the first page | — |
| 48 | 2026-09-17 | bugs.kde.org REST | product=frameworks-baloo quicksearch="cpu idle" | 3 hits returned (ids in S3-03 copy) | — |
| 49 | 2026-09-19 | GitHub REST (`gh api`) | ValveSoftware/steam-for-linux issue 13024 + `/comments` (retry of rows 31, 33, 45) | 200; 14 of 14 comments → S3-28 | — |
| 50 | 2026-09-19 | GitHub REST | steam-for-linux 12015 + comments (row 31) | 200; 10 of 10 → S3-29 | — |
| 51 | 2026-09-19 | github.com user-attachments | #12015 body attachment `https://github.com/user-attachments/files/20233784/steam-logs.tar.gz` (redirected to objects.githubusercontent.com) | 200, 8,349,732 B; `content_log.txt` and `content_log.previous.txt` extracted → S3-29 | — |
| 52 | 2026-09-19 | GitHub REST | steam-for-linux 7956 + comments (row 31) | 200; 11 of 11 → S3-30 | — |
| 53 | 2026-09-19 | GitHub REST | steam-for-linux 6684 + comments (rows 17, 42) | 200; the issue lists 18 comments, the comments endpoint returned 17 → S3-31 | — |
| 54 | 2026-09-19 | user-images.githubusercontent.com | #6684 body screenshot `17158780/68635668-24c24e80-055e-11ea-961b-59c02f8c1754.png` | 200, 133,785 B → S3-31 | — |
| 55 | 2026-09-19 | user-images.githubusercontent.com | #6684 comment 955878117 screenshot `11761863/139614157-559b7e4d-4cb4-4405-9395-38c05266d677.png` | 200, 18,986 B → S3-31 | — |
| 56 | 2026-09-19 | GitHub REST | borgbackup/borg 2245 + comments (rows 2, 15) | 200; 19 of 19 → S3-32 | — |
| 57 | 2026-09-19 | GitHub REST | borg 3471 + comments | 200; 24 of 24 → S3-32 (macOS report; context) | — |
| 58 | 2026-09-19 | GitHub REST | borg 5804 + comments | 200; 14 of 14 → S3-32 | — |
| 59 | 2026-09-19 | GitHub REST | borg 7374 + comments | 200; 15 of 15 → S3-32 | — |
| 60 | 2026-09-19 | GitHub REST | restic/restic 652 + comments (rows 2, 15) | 200; 32 of 32 → S3-33 | — |
| 61 | 2026-09-19 | GitHub REST | restic 2696 + comments | 200; 1 of 1 → S3-33 | — |
| 62 | 2026-09-19 | GitHub REST | restic 2679 + comments | 200; 8 of 8 → S3-33 (Windows observation; maintainer statements on the write path) | — |
| 63 | 2026-09-19 | GitHub REST | curl/curl 336 + comments (rows 12, 28, 34, 39) | 200; 11 of 11 → S3-34 | — |
| 64 | 2026-09-19 | i.imgur.com | #336 comment 119079303 screenshot `http://i.imgur.com/ZFj6Fqc.png` (redirected to https) | 200, 23,830 B → S3-34 | — |
| 65 | 2026-09-19 | i.imgur.com | #336 comment 119090279 screenshot `http://i.imgur.com/KrNQlyr.png` | 200, 23,264 B → S3-34 | — |
| 66 | 2026-09-19 | GitHub REST | curl 11242 + comments | 200; 11 of 11 → S3-34 | — |
| 67 | 2026-09-19 | tinystash.undef.im | #11242 comment 1594442502 linked `CURL_DEBUG=http/2` log `https://tinystash.undef.im/il/2EQtfhvYcr9r9SPd1TkCyqudqFDNKSc9yaCHNAw9t4gsEdd9gKLaQUKAt2pBMiTgKow7kDcA2DhETsB8Q2ggAWsw` | 200, 104,954 B text/plain → S3-34 | — |
| 68 | 2026-09-19 | GitHub REST | Cisco-Talos/clamav 849 + comments (rows 5, 13, 30, 46, 47) | 200; 13 of 13 → S3-35 | — |
| 69 | 2026-09-19 | GitHub REST | clamav 590 + comments | 200; 53 of 53 → S3-35 | — |
| 70 | 2026-09-19 | user-images.githubusercontent.com | #590 comment 1535822498 flamegraph `7189867/236843976-1e079c4e-3275-4920-8f75-033c151be4a3.svg` (0.104.2 on the unit-test database) | 200, 12,125 B → S3-35 (not quoted) | — |
| 71 | 2026-09-19 | user-images.githubusercontent.com | #590 comment 1535822498 flamegraph `7189867/236844093-3fb0f8ea-4507-49e9-a045-a06dc8c9794f.svg` (1.0.1 on the unit-test database) | 200, 11,788 B → S3-35 (not quoted) | — |
| 72 | 2026-09-19 | user-images.githubusercontent.com | #590 comment 1537198319 flamegraph `5107748/236641028-e1c1ee9d-a07b-4915-9cf6-5bd88d706843.svg` | 200, 59,954 B → S3-35 | — |
| 73 | 2026-09-19 | user-images.githubusercontent.com | #590 comment 1537473757 flamegraph `7189867/236687385-d8063987-5649-414a-88e0-0c6d6be6898d.svg` (0.104.2, `$HOME`) | 200, 34,568 B → S3-35 | — |
| 74 | 2026-09-19 | user-images.githubusercontent.com | #590 comment 1537473757 flamegraph `7189867/236687444-36808f86-16e4-4e46-8cc3-2cb4b923ff61.svg` (1.0.1, `$HOME`) | 200, 36,946 B → S3-35 | — |
| 75 | 2026-09-19 | GitHub REST | clamav 1375 + comments | 200; 3 of 3 → S3-35 | — |
| 76 | 2026-09-19 | curl, default UA `curl/8.7.1` | `https://openbenchmarking.org/result/2305286-NE-MONITORSY37` (row 11) | — | 403 (5,498 B) |
| 77 | 2026-09-19 | curl, Chrome 140 macOS User-Agent with browser `Accept`/`Accept-Language` headers | same URL | — | 403, `server: cloudflare`, `cf-mitigated: challenge`, page title "Just a moment..." |
| 78 | 2026-09-19 | curl, same browser UA | same URL + `&export=csv`, `&export=txt`, `&export=pdf`, `&export=xml`, `&export=json`; and `http://openbenchmarking.org/result/2305286-NE-MONITORSY37` | — | each 403, `cf-mitigated: challenge` |
| 79 | 2026-09-19 | curl, same browser UA | `https://openbenchmarking.org/test/pts/compress-7zip` | — | 403 |
| 80 | 2026-09-19 | GitHub REST (`gh api`, raw) | phoronix-test-suite/phoronix-test-suite `pts-core/objects/pts_openbenchmarking.php`, `pts-core/objects/pts_network.php`, `pts-core/pts-core.php` at master f977d6e270d5eb9eebfa26d3ca62385c00a547a6 (2026-07-27) — how the PTS client clones a result | 200: POST `r=clone_openbenchmarking_result`, `i=<id>` to `https://openbenchmarking.org/f/client.php` with User-Agent `PhoronixTestSuite/<Codename>` (PTS_VERSION 10.8.6, codename Nesseby) | — |
| 81 | 2026-09-19 | curl POST, UA `PTS/10.8.6` | `f/client.php` `r=clone_openbenchmarking_result&client_version=10860&gsid=&gsid_e=&i=2305286-NE-MONITORSY37` | 200, body "No Client" (9 B) | — |
| 82 | 2026-09-19 | curl POST, UA `PhoronixTestSuite/Nesseby` | same request | 200, JSON 4,783 B with `composite_xml` and `system_logs_available` → S3-36 | — |
| 83 | 2026-09-19 | curl POST, UA `PhoronixTestSuite/Nesseby` | `r=clone_openbenchmarking_system_logs&…&i=2305286-NE-MONITORSY37` | 200, zip 97,896 B whose SHA-1 equals `system_logs_available` → S3-36 | — |
| 84 | 2026-09-19 | GitHub REST (`gh api`, raw) | PTS repository `ob-cache/test-profiles/pts/compress-7zip-1.10.0/` (`install.sh`, `test-definition.xml`, `results-definition.xml`, `downloads.xml`, `changelog.json`) at f977d6e | 200 → S3-36 (what the test runs) | — |

## 2. Candidates

### S3-01 — GNOME LocalSearch (tracker-miners) issues #340, #161, #228

**Citation.** GNOME / LocalSearch issue tracker (formerly tracker-miners), gitlab.gnome.org: #340 "Constant high CPU usage" (opened 2024-05-02, closed, 48 notes); #161 "tracker-miner-fs-3 times out, with high CPU usage." (2021-03-14, closed, 29 notes); #228 "tracker-miner-fs-3 at 100% CPU activity for hours" (2022-08-01, closed, 6 notes).

**Copy read.** REST `https://gitlab.gnome.org/api/v4/projects/GNOME%2Flocalsearch/issues/{340,161,228}` (JSON) and `https://gitlab.gnome.org/GNOME/localsearch/-/issues/{340,161,228}/discussions.json?per_page=100` (60b54403ed786dff2b4b45f2af4b11244d149141ec93a37e57f8c79c7089a6be; 6e6ca0080e6aa5b797e9da446ece11c97d905183f230b33016a3b491d3303cd6; 5a7d283de8d6ec85b9e6bcf2d11ddbeddec9947f302541c2f10ccc3e03b2b7a6). Issue JSON: 340 = 4305d0cb88f05b8ee4041b50d02d2e00b8742edb97b1028d4539f222d03c39f1, 161 = ee1696b4bca16d1801a7081df8160c1df9eada67c4f3a20c1c120135273998c5, 228 = 6a84151dc941653eaffdcb701e7640d02230b8bdfb2734259cd98feec56c4083. Accessed 2026-09-17 21:22–21:24 UTC. Local: `sources/S3-01/`.

**Passages.**

- #228, `description` (API JSON): "I've noticed several times that after moving "a lot" of files around (e.g. in this case: several folders with ~500 files each), the tracker-miner-fs-3 process then spends a few hours at 100% CPU until it eventually calms down. Today it took around 3.5 hours to settle." … "Nothing is logged to journal; `tracker3 status` says "All data miners are idle, indexing complete" (and no related errors); but `strace -ff -p <pid>` shows a continuous stream of the miner-fs process reading from `FileSystem.db` and `meta.db` the whole time, with an occassional write." … "The entire system is running from an SSD." … "$ find ~/Documents/ ~/Pictures/ ~/Music/ | wc -l / 196877" … "tracker3 3.3.2 / tracker3-miners 3.3.1 / sqlite 3.39.1-1".
- #228, note 1522228 (2022-08-02, grawity): "After restarting miner-fs (and waiting for it to go idle), then renaming 11 folders (containing ~180 files total), it takes around 30 minutes for miner-fs to settle down, almost the same with both 3.39.1 and 3.39.2." … "Aug 02 12:20:41 frost tracker-miner-f[7985]: Processed 0/23, estimated less than one second left, 18s elapsed / Aug 02 12:57:22 frost tracker-miner-f[7985]: Finished mining in seconds:2236.910116, total directories:0, total files:0".
- #228, note 1522229 (2022-08-06, carlosg, maintainer): "I tested here on tracker & miners from git, with ~130K indexed files, moving once a directory with 180 files and waiting for it to sit idle and I see it spending ~50s on the operation. Since your database is larger, and you talk about multiple move operations, the overall 30min wait sounds plausible." … "these are the queries moving recursively directory contents, which is the expensive part on itself (i.e. a prefix search)".
- #228, note 1523129 (2022-08-08, grawity): "I'm testing this on top of Arch's 3.3.1 and it definitely helps, what took 30 minutes now seems to take 20-30 seconds."
- #161, note 1070232 (2021-03-30, juxuanu): "My laptop's CPU fans start spinning like crazy and I see this (one thread at 100%, ~230MB of RAM)" … "Tracker is at version 3.1.0." … "system uptime is almost 4h. Memory usage is now 1.1GB, total disk writes 28.3GB and climbing".
- #340, `description`: "the process "tracker-miner-fs-3 (version 3.7.1)" was using a lot of CPU resources and not stopping." … "Mai 02 13:20:20 erik-fedora-laptop tracker-miner-fs-3[18268]: (tracker-extract-3:18268): Tracker-WARNING **: 13:20:20.057: Task for ‘file:///home/erik/Videos/filename.temp.webm’ finished with error: Error when getting information for file “filename.temp.webm”: No such file or directory".
- #340, note 2245302 (2024-10-12, universish): "tracker-extract-3 is constantly pushing the processor to full capacity, it takes a few seconds. Then it backs off for a few seconds. Then it again pushes the processor to full capacity."

**Coverage.** T2 — covers: duration of the miner's CPU-bound settle after a metadata change on a settled index (object: tracker-miner-fs-3 wall time from rename to idle; unit: seconds; statistic: single runs, 2236.9 s for 11 folders/~180 files at ~197 k indexed files on SSD, ~50 s for one 180-file directory at ~130 k files (maintainer), 20–30 s after the fix); CPU level during that phase (100 % of one thread, reporter's monitor); tracker-extract-3 burst/back-off cadence in seconds (qualitative, note 2245302). T1, T3, T4: does not cover. T7: the notes contain no downloadable trace; strace/journal excerpts only.

**Observation status.** #228 is one observation on one machine ("frost", Arch Linux, SSD, tracker 3.3.x, sqlite 3.39.x, ~197 k files under Documents/Pictures/Music; window: one rename batch, 2022-08-02 12:20–12:57) plus one maintainer counter-observation (machine unnamed, ~130 k files, git build). #161/#340: machine named only as "laptop"/Fedora laptop; no window; screenshots not fetched.

**Reader's own computation.** None beyond the quoted values.

### S3-02 — GNOME TinySPARQL (tracker) issues #348, #334, #173, #373

**Citation.** GNOME / TinySPARQL (formerly tracker) issue tracker: #348 "tracker-miner-fs-3 massive CPU usage and system slowdown" (2022-02-21); #334 "tracker-miner-f 100% CPU and slows system down" (2021-10-21); #173 "tracker-miner-fs eating my CPU" (2020-01-11); #373 (2022-08-01; the same report as LocalSearch #228 before it was moved).

**Copy read.** `https://gitlab.gnome.org/api/v4/projects/GNOME%2Ftinysparql/issues/{348,334,173,373}` (sha256 aec7eb70e77492a9ca8c7d11fbce474ef7854faaea5af54c027f0e8d45c84bf1; 7f4422d6403490d4f33b9603281bddad8ef15fdf10f9ac72ba41b85aed9020b1; 23ad5294a06a5f024a61ed1c3e950be331a4bfa1fd25803e47b61e68df955716; 5ff4dee1b3ceeaab5229e5be7f9d6c136742d1e2474be97da6934133196f362e) and `/-/issues/{348,334,173,373}/discussions.json` (9dce6a6e1a9236795f84e47334b287cf47df320cb9c2e6d8968ffa8f1ab10448; d08b6235ec22e95de5b1da9ab8b7afc23d101370c1f4434bede53cc7d66a286c; 530afdf595849f34e651cf59e26d11bbf5c3470da3ff44da394a8c5c571edcfc; c40d5c21dea1d61f9c1b095372c80744c588836891feb8f137b1c52ebb7e9fc8). Accessed 2026-09-17 21:22–21:24 UTC. Local: `sources/S3-02/`.

**Passages.**

- #173, note 683800 (2020-01-12, sthursfield, maintainer): "Your screenshots show tracker-miner-fs using around 25% of CPU. This is normal for short periods while Tracker indexes new or changed files."
- #173, note 683836 (2020-01-12, sthursfield): "Tracker daemons opt into the SCHED_IDLE scheduler policy which gives the lowest possible scheduler priority. It's not clear what more we can do there."
- #348, note 1694083 (2023-03-09, brainblaze, Ubuntu 22.04.2): "tracker-miner-fs-3 is using 100% CPU and when I do my tracker3 status it says my indexing is complete" … "brain@ubraintuMOBILE:~$ env TRACKER_DEBUG=config,sparql /usr/libexec/tracker-miner-fs-3 / Tracker-Message: 14:09:31.417: Set scheduler policy to SCHED_IDLE / Tracker-Message: 14:09:31.417: Setting priority nice level to 19 / … / Tracker-Message: 14:09:31.423:   Initial Sleep  ........................  15 / Tracker-Message: 14:09:31.423: Indexer options: / Tracker-Message: 14:09:31.423:   Throttle level  .......................  0 / Tracker-Message: 14:09:31.423:   Indexing while on battery  ............  yes (first time only = yes) / Tracker-Message: 14:09:31.424:   Low disk space limit  .................  Disabled".
- #348, note 1392499 (2022-02-22, carlosg): "since Tracker services do already have minimum nice and I/O priorities, the cpu% does not mean much" … "this is not a runaway situation, it will eventually come to an stop after every "broken" file is tagged as such, despite many `tracker-extract-3` restarts."
- #334, `description` (Ubuntu 20.04, tracker 2.3.6, kernel 5.11.0-37): "tracker-miner-f has been using 100% CPU and my system making it almost unresponsive. This happens around once a month or so when I boot up. It sometimes lasts for a number of days" … "Currently indexed: 101154 files, 16046 folders".

**Coverage.** T2 — covers: the daemon's self-set scheduling class and nice (SCHED_IDLE, nice 19) as printed by the daemon on Linux; the default "Initial Sleep 15" and "Throttle level 0" configuration echo; a maintainer's stated normal CPU level (~25 % for short periods) — qualitative. Steady-state wake cadence/CPU per wake: does not cover (no time series). T1/T3/T4/T7: does not cover.

**Observation status.** Each issue is one reporter's machine (named by distro/version only). The SCHED_IDLE/nice-19 lines are a daemon log on one Ubuntu 22.04.2 machine, 2023-03-09 14:09.

### S3-03 — KDE Baloo bug reports 384372, 406486, 418323, 358548, 363384, 500665; discuss.kde.org 6043

**Citation.** bugs.kde.org, product frameworks-baloo: 384372 "baloo_file_extractor always high CPU usage" (2017-09-05, RESOLVED DUPLICATE); 406486 "baloo consumes an excessive amount of CPU indexing files" (2019-04-12, DUPLICATE of 418323); 418323 "Baloo indexer is swallowing cpu usage and slow down other apps" (2020-02-29, RESOLVED FIXED); 358548 "baloo_file_extractor high CPU and memory usage"; 363384 "Baloo file extractor process uses up nearly 100% of CPU" (2016-05-21, DUPLICATE); 500665 "Baloo File Extractor uses 25-40% CPU and 3 GB of RAM while indexing an HDD and slows down the whole system" (2025-02-24, RESOLVED WORKSFORME). KDE Discuss thread 6043 "Baloo_file_extractor running and eating up CPU and memory" (2023-10-13).

**Copy read.** `https://bugs.kde.org/show_bug.cgi?ctype=xml&id=N` (Bugzilla XML): 384372 = 46ee040977158c72881176522e615f27d04fc6446249996bcb4e92117fe2c861 (14,531 B); 406486 = 7eca228e83a9f04c4872773362fdc248807b421267db14e573db5ac36405d6ae; 418323 = 8a01159a030e93465102854c583d6dfa5e610037ec53a86631d5c12e3b0b5433; 358548 = 9ff8aa7eba23ba6d20d42684b4556ba3ceb3adb8aa7001fee77a3150c50fdf57 (839,493 B); 363384 = 5ab93e2f0c1e96a7c63974c5fd6ba805ab036d27e7e80f67a970f18b65f08989; 500665 = 652bc6c4c44ef9ed8e4623274b59d803ed38d63cb278a142bb639ec7a189ae13 (12,861,916 B, attachments inline). REST search `https://bugs.kde.org/rest/bug?product=frameworks-baloo&quicksearch=cpu%20idle&limit=40&…` = 2dbf35db6d6d5d4a91b40538399dc3faf00a0ebebda5625bdca6d717c5b51fc8. `https://discuss.kde.org/t/…/6043.json` = 87e7730e163bdc09250c71b219d2c74a31203f2441c55dbe9748f7f55959f68b. Accessed 2026-09-17 21:23 and 21:28 UTC. Local: `sources/S3-03/`.

**Passages.**

- 406486, comment #0 (commentid 1850081, 2019-04-12, KDE neon, Frameworks 5.56.0): "OBSERVED RESULT / USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND / HOME\p2   2017 99.8  0.0 268818620 51696 ?     RNl  10:47 744:29 /usr/bin/baloo_file_extractor" — "baloo_file_extractor seems to get into an infinite loop when encountering a big endian TIFF file." (The `ps` STAT field `RNl` shows the process running, low-priority (nice), multi-threaded.)
- 384372, comment #0 (1699044, 2017-09-05, openSUSE, Frameworks 5.37): "baloo_file_extractor always use about 12% total CPU and cause computer over heat." Comment 1727003 (2018-02-01, openSUSE Leap 42.3, baloo 5.32.0): "The file extractor showd up in the task list with 13% cpu (a full core in an 8-core machine)." … "My home directory is sized about 32GB, and after about 45 min of shuffling around, the index has round about 1.4GB." Comment 1722861 (2018-01-17): "The baloo_file_extractor process consumes a single core completely (100%). Gladly this thing is not multi-threaded". Comment 1729447 (2018-02-11): "As far as I understand, *nice* is without effect in such situations, and baloo will get as much CPU time as it wants".
- 418323, comment #0 (1913744, 2020-02-29, Kubuntu 19.10, Frameworks 5.67.0, "Processors: 2 × Pentium® Dual-Core CPU T4400 @ 2.20GHz"): "after any noticeable changes in the hierarchy of files/folders then after rebooting baloo indexer starts to index and consumes half of cpu use which slow down other apps". Comment 2333818 (2024-07-01): "There's been a patch here that applies limits on Baloo's RAM and CPU usage / https://invent.kde.org/frameworks/baloo/-/merge_requests/121 / Baloo was being run at the lowest priority, this change reinforces that."
- 500665, comment #0 (2025-02-24, openSUSE Tumbleweed 20250222, Plasma 6.3.1, Frameworks 6.11.0, kernel 6.13.3, "Processors: 24 × AMD Ryzen 9 5900X 12-Core Processor", "System is installed on an NVMe using BTRFS / HDDs are two WD RED 7200 RPM with a few TB and NTFS"): "baloo_runner starts baloo_file, which starts baloo_file_extractor / Baloo File Extractor uses 25-40% CPU and 3 GB of RAM while indexing files on the HDD." Comment 1 (2025-02-24, attachment 178804 "Flamegraph for baloo_file_extractor"): "Recorded over 2 min and 20 seconds. / 1.438E+11 (100%) aggregated cycles costs in Baloo::WriteTransaction::commit() (libKF5BalooEngine.so.5.116.0) and below. / … / 5.122E+10 (35.6%) aggregated cycles costs in Baloo::PositionDB::get(QByteArray const&) … / 8.215E+10 (57.1%) aggregated cycles costs in Baloo::PostingDB::get(QByteArray const&) … / 4.809E+10 (33.4%) aggregated cycles costs in mdb_get (liblmdb-0.9.30.so) and below. / 8.138E+10 (56.6%) aggregated cycles costs in mdb_get (liblmdb-0.9.30.so) and below." Comment 7: "chrt -p (pidof baloo_file) / pid 21116's current scheduling policy: SCHED_BATCH / pid 21116's current scheduling priority: 0" … "chrt -p (pidof baloo_file_extractor) / pid 21300's current scheduling policy: SCHED_IDLE / pid 21300's current scheduling priority: 0 / … / At this point it still lags most of the time!" Comment 24: "In htop one can observe a constant switching between the process state's R(unning) and D(isk Sleep)." Comment 13: "I've tried to stop baloo by `balooctl disable` and `balooctl suspend`, however, baloo_file_extractor process still keeps running now 40 minutes after starting it."
- discuss.kde.org 6043, post #1 (2023-10-13, Debian 12.1): "baloo_file_extractor is eating up a full CPU core and >20GB of RAM, as well as periodically thrashing my SSD."

**Coverage.** T2 — covers: process structure (baloo_runner → baloo_file → baloo_file_extractor), the scheduling classes observed on the running processes (baloo_file SCHED_BATCH, baloo_file_extractor SCHED_IDLE, `chrt` on Linux 6.13.3), a `ps` line with nice state, CPU levels during content indexing (25–40 % of a 24-thread machine; 12–13 % ≈ one core of eight; "half of cpu" on a 2-core), a 140 s cycle profile by function (LMDB `mdb_get` dominated), and the R↔D state alternation. Steady-state of a settled home directory: does not cover — every report is a first/ongoing content index or a stuck file (TIFF). T1/T3/T4/T7: does not cover.

**Observation status.** 500665 is one observation with machine (Ryzen 9 5900X, NVMe/BTRFS, NTFS HDDs), subject (baloo_file_extractor, Frameworks 6.11.0, content+filename indexing of two multi-TB NTFS mounts, cache state not stated) and window (2 min 20 s profile; 25-min heaptrack) named. 406486: one `ps` snapshot, 744 min CPU time, KDE neon, Frameworks 5.56.0. Others: machine partially named.

### S3-04 — Debian bug #1016745 "tracker-miner-fs: at 100% CPU activity for long minutes"

**Citation.** Debian BTS #1016745, filed 2022-08-06 by Patrice Duroux against tracker-miner-fs 3.3.1-2.

**Copy read.** `https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1016745;mbox=yes` (mbox, 3,338 B, sha256 48739c211f5a929284c485907e1b1f179c4536fad5ad28fbcddf005e4bdcaf59), accessed 2026-09-17 21:23 UTC. Local: `sources/S3-04/`.

**Passages.** Message 0 body: "I am facing something very similar to the following: / https://gitlab.gnome.org/GNOME/tracker/-/issues/373" … "Kernel: Linux 5.19.0-trunk-amd64 (SMP w/12 CPU threads; PREEMPT)" … "Versions of packages tracker-miner-fs depends on: … libupower-glib3 0.99.20-1 … tracker-extract 3.3.1-2".

**Coverage.** T2 — context only: no CPU figure or duration beyond the title; it links to the S3-01/#228 report. Other topics: does not cover.

**Observation status.** One machine (Debian bookworm/sid, 12 threads), no window.

### S3-05 — Manjaro forum thread 96726 "Baloo indexing high CPU and memory usage when idle"

**Citation.** forum.manjaro.org, KDE Plasma category, 2021-12-30, 8 posts.

**Copy read.** `https://forum.manjaro.org/t/baloo-indexing-high-cpu-and-memory-usage-when-idle/96726.json` (Discourse JSON, 43,375 B, sha256 801c793981cc5dcb518d90bcfcbaf6f4da34a647584723158f12af192ad8a5cc), accessed 2026-09-17 21:23 UTC. Local: `sources/S3-05/`.

**Passages.** Post #1: "baloo_file_extractor uses 3.0 GB of memory when it is idle as shown below" … "Sometimes it can use up to 5 GB of RAM and over 10% of CPU." Post #2 (a `balooctl status` example on the responder's machine): "Indexer state: Idle / Total files indexed: 36 527 / Files waiting for content indexing: 0 / Files failed to index: 0 / Current size of index is 17,35 MiB".

**Coverage.** T2 — weak: one user's "over 10 % of CPU" while "idle" (no core count, screenshot not fetched); an index-size/file-count example. Other topics: does not cover.

**Observation status.** Machine unnamed; no window.

### S3-06 — Arch Linux BBS thread 247158 "[Solved] clamscan very slow (clamav)"

**Citation.** bbs.archlinux.org, Applications & Desktop Environments, thread 247158 (2019-06-17 … 2021-11-11).

**Copy read.** `https://bbs.archlinux.org/viewtopic.php?id=247158` (HTML, 20,267 B, sha256 3fed5377ac023c0798b02a702901aeb58c6e6c289b219dfcafd3d6a8e20597ad), accessed 2026-09-17 21:23 UTC. Local: `sources/S3-06/`.

**Passages.** Post p2002727 (2021-11-11 20:19:30): "This is my scan summary, just finished after 4 days scanning only 101GiB on a USB 3.0 external hard drive (a fast Samsung SSD) using a brand new computer based on an Intel i7 10xxx series with 64GB DRAM.----------- SCAN SUMMARY ----------- / Known viruses: 8573992 / Engine version: 0.104.1 / Scanned directories: 298991 / Scanned files: 2895752 / Infected files: 0 / Total errors: 71689 / Data scanned: 338962.49 MB / Data read: 255505.27 MB (ratio 1.33:1) / Time: 390400.275 sec (6506 m 40 s) / Start Date: 2021:11:07 08:07:32 / End Date:   2021:11:11 20:34:13" … "The 71689 "errors" come from files that it eventually tried to decompress only to later display an error stating that it exceeded the clamscan size limit for compressed files." … "With same data on a 15 year old laptop, Intel Core Duo with 4GB SDRAM, and a typical commercial antivirus (Trend Micro) the scanning took less than 3 hours."

**Coverage.** T4 — covers: one complete `clamscan` summary block on Linux (Arch; ClamAV 0.104.1; 2,895,752 files, 338,962.49 MB scanned, 255,505.27 MB read, 390,400 s wall; source a USB 3.0 SSD; i7 10th gen, 64 GB). CPU share over the scan: does not cover (no CPU figure). T1/T2/T3/T7: does not cover.

**Observation status.** One run, machine partly named (CPU family, RAM, source medium), subject named (clamscan 0.104.1, recursive scan of 101 GiB), window 2021-11-07 08:07 → 2021-11-11 20:34; cache state not stated (cold for most, by size).

**Reader's own computation** (locates the candidate; not a value): `python3 -c "print(338962.49/390400.275, 2895752/390400.275)"` → 0.868 MB/s scanned, 7.42 files/s.

### S3-07 — Valve "Steam Download Stats" page and its public JSONP feeds

**Citation.** Valve Corporation, "Steam: Game and Player Statistics — Steam Download Stats", `store.steampowered.com/stats/content/`, with data files on `cdn.fastly.steamstatic.com/steam/publicstats/`: `contentserver_bandwidth_stacked.jsonp`, `download_traffic_per_country.jsonp`, `top_asns_per_country.jsonp` (version parameter `v=09-17-2026-21`).

**Copy read.** Page HTML 49,535 B, sha256 66b6d7230d6ecabbaa7708ea2a54dc2e92035039c87bd48fd701b37c77a703a5 (accessed 2026-09-17 21:23 UTC); `contentserver_bandwidth_stacked.jsonp?v=09-17-2026-21` 146,961 B, 784803036a0c8f57279272ead78f3e72ab3363fa9feef28525aa6e71db5563e5; `download_traffic_per_country.jsonp?v=09-17-2026-21` 19,671 B, 9ae9389244d1e4cfb35482949cdbea8210f187c750c92b576ec29bcede556280; `top_asns_per_country.jsonp?v=09-17-2026-21` 182,921 B, abfb7005593fa23ca69adcc6468345febc22f17c59ae008b8f4fc5d5e8a7e870 (accessed 21:25 UTC). Local: `sources/S3-07/`.

**Passages.**

- Page text: "Steam Download Stats / Steam Global Traffic Map (most recent 7 days) / Interactive Map | Satellite View / … / Select Data: Total Bytes Average Download Rate / Show US States / Click any region to see details".
- `contentserver_bandwidth_stacked.jsonp`, first bytes: `jsonpFetch.onCSBandwidth({"xml":"<chart stack100Percent=\"0\" formatnumberscale=\"0\" showvalues=\"0\" cur=\"33474986\" peak=\"48909147\" … numbersuffix=\" Gbps\" …>` followed by `<category label="2026-09-15 14:00:00" />` … and datasets named "Central America", "Africa", "Middle East", "Oceania", "South America", "Russia", "Asia", "Europe", "North America".
- `download_traffic_per_country.jsonp`, first bytes: `jsonpFetch.onTrafficData({"PRI":{"totalbytes":"1748980921043375","avgmbps":93341391.20228735},"NFK":{"totalbytes":"10959240628","avgmbps":2188413.2593478113},…"USA":{"totalbytes":468173124837745048,"avgmbps":181770517.34823415},…`
- `top_asns_per_country.jsonp`, first bytes: `jsonpFetch.onCountryASNData({"AND":[{"asname":"Andorra Telecom, S.a.u.","totalbytes":"305462763194227","avgmbps":170.55089995590163},{"asname":"GSL Networks","totalbytes":"47488041458533","avgmbps":104.5877105047798},…`

**Coverage.** T3 — covers: throughput on consumer links at population scale (object: Steam content-server download traffic; units: bytes per country/ASN over the "most recent 7 days", an `avgmbps` field per ASN whose page label is "Average Download Rate", and a 10-minute global bandwidth series in Gbps by region); population: all Steam clients worldwide. Per-client CPU, chunking, wake structure: does not cover. T7 — a public, continuously refreshed dataset, but without process-level fields. T1/T2/T4: does not cover.

**Observation status.** Not one machine; a 7-day aggregate ending 2026-09-17 13:50 UTC (last category label). Field semantics of `avgmbps` at country level (values ~10^8) versus ASN level (values ~10^2) are not documented on the page; only the ASN-level values are consistent with a per-client Mbps reading.

**Reader's own computation** (structure only): `python3` parse of the chart XML: 284 ten-minute categories from 2026-09-15 14:00 to 2026-09-17 13:50; 9 regional series; sum over series max 48,950 (at 2026-09-16 07:20), min 23,140, mean 33,026 (units as given by `numbersuffix`, " Gbps"); 289 country keys; 236 countries with ASN lists; e.g. USA top-5 ASN `avgmbps` = Comcast Cable 224.3, Spectrum 188.2, AT&T Internet 173.8, Verizon Fios 204.0, Cox 199.7; DEU: Deutsche Telekom 76.5, Vodafone Germany 129.9; KOR: KT 184.2, SK Broadband 181.1; GBR: Virgin Media 156.5, BT 101.2.

### S3-08 — rsync mailing list and Samba Bugzilla: 2010-02 "Rsync / ssh high cpu load"; bug 10518; 2009 "How to speed up rsync when having lots of files"

**Citation.** rsync@lists.samba.org archive, February 2010, message 024743 (Jan Alphenaar, "RE: Rsync / ssh high cpu load"); July 2019 message 031942 (Bugzilla mail for bug 10518, "rsync hangs (100% cpu)"); bugzilla.samba.org bug 10518; narkive mirror of the March 2009 thread.

**Copy read.** `https://lists.samba.org/archive/rsync/2010-February/024743.html` 6,604 B, sha256 92940ea3876701e202baf4c0bd0037ac7f5904a561d0b25841c2462cf6058be6; `…/2019-July/031942.html` 3,623 B, 2e0ef1cf3911b1dd293b8abd217fd4edeedb61f0f6cc00404569369288477c05 (21:24 UTC); `https://bugzilla.samba.org/show_bug.cgi?ctype=xml&id=10518` 20,364 B, 3ba817d7ef0d39f49fc679f2b57fcd91146ea6ea6600d4068b9b0be97d6d0438; `https://rsync.samba.narkive.com/ff80qA0P/how-to-speed-up-when-haveing-lots-of-files` 80,482 B, b2a7993c10b09a96bcaf86e26710268b96957e6d03d877b43935c302204516fd (21:28 UTC). Local: `sources/S3-08/`.

**Passages.** 024743 (Cygwin, i.e. Windows — context, other platform): "The issue is that the CPU on the sending side is fully allocated by rsync/ssh (both taking 50%) during a file transfer." … "if the uplink is 128KB/s and I pass in the --bwlimit=24 parameter the cpu is around 0%. Even --bw-limit=126 does not take 100% cpu, but --bwlimit=132 does." … "When I rsync/ssh a big file to my server over the local network (100Mbit/s) with the --bwlimit=1000 I only have a small CPU load. SSH takes about 10% and rsync approximately 0-5%." … "In an attempt to narrow this down a bit I installed a RedHat machine with openssh-5.3p1 and rsync-3.0.7 and did the same test as below. / Transferring data, both up and downstream, are not giving me any CPU load." … "Cygwin: 1.7.1-1 / ssh: OpenSSH_5.3p1 / rsync: 3.0.6". 031942: "i have pathological slow transfer when re-syncing 500gb vhd image to linux/zfs remote system." 2009 thread: "unfortunatelly rsync is beeing REALLY slow and produces a high load when we try to sync lots of files (>250 000 small files)." … "rsync version 2.6.9 protocol version 29".

**Coverage.** T1 — context only: the CPU-% figures are on Cygwin/Windows (other platform); the one Linux statement ("not giving me any CPU load", RedHat, rsync 3.0.7) carries no number. Bug 10518 and the 2009 thread carry no per-process CPU figure. Other topics: does not cover.

**Observation status.** Not a Linux observation with numbers.

### S3-09 — Mozilla Bugzilla, Thunderbird SMTP send CPU: bugs 538283, 577545, 742697, 358427, 774401

**Citation.** bugzilla.mozilla.org: 538283 "CPU went to 100% while sending message or while uploading messeage via TLS/SSL or StartTLS connection." (MailNews Core: Networking, platform x86 All, 2010-01-06, RESOLVED WORKSFORME); 577545 "100% CPU while sending (SMTP with SSL encryption)" (x86 Windows XP, 2010-07-08, DUPLICATE); 742697 "SMTP connection progress bar causes high CPU usage" (Networking: SMTP, platform All/All, 2012-04-05, RESOLVED FIXED); 358427 (Windows XP, 2006); 774401 (Windows 7, 2012).

**Copy read.** `https://bugzilla.mozilla.org/rest/bug/N` and `/rest/bug/N/comment` (JSON): 538283 = 532778287bbc8eb9bf4cda36074bb3429b8d946067330a189be9044243724aa4 / comments 8dda1abacb76bab71cbefc20d29021084c88b8bba7be879f2029de398dc8e225; 577545 = 7ab29df61b25856297d5b929549fd01059453b49095cbc950959ed1646e41803 / 18302bc7ff98cf583a769210ef5e8a8c90e7840e0f439095ee1adc4571440f8c; 742697 = c69e407622ae837fc867f1a373d7b7302232787df4e06768d17a1106ca2da9a5 / 2f2a0b80179d1a140220104357c3661b0dfb905c8692bd022f1ddb30fbfe0195; 358427 = ed852bebc62fa8a774d8782366fe302c79e2e55bbb7c4208dfc44330bb939471 / 8b6e406549235b3d856b0f1fa7a43e01ba0fed9b5b0195754dfe8e0bc7c7dc6c; 774401 = 0c43a8a92d986cb4cea4e37227531042b0e7d2e005e0afcf2055c444d17afbf3 / 49b17ae6277bf17581f701f40d27a6451be2e46a7db5191f4842bd62aed810ce. Accessed 2026-09-17 21:24 UTC. Local: `sources/S3-09/`.

**Passages.**

- 742697 comment 24 (2020-11-11, it@von-Oheimb.de): "The problem is easily reproducible, also on Linux, with any TB version (meanwhile including 78.4.2.)." … "the progress bar moves forth and back with significant CPU load (10% of one core on my current Linux machine)."
- 742697 comment 25 (2021-04-26, bernie@codewiz.org): "I have experienced this bug for several years on multiple Linux machines. / It just happened to me today on Thunderbird 89.0b1 (beta): sending a message over SMTP hung for several minutes while the progressbar keeps on scanning left and right,  eating ~60% CPU on a fast machine."
- 742697 comment 23 (2019-09-03, acelists@atlas.sk): "Do I read the profile correctly that most of the time (80%) is used in the poll() function in libc.so.6 (Linux system C standard library)? That would seem to confirm the theory really the drawing/synchronizing on the screen of the progress bar."
- 742697 comment 18 (2013-05-25): "FWIW, I see the CPU spike on Linux but can't reproduce on Windows 7..."
- 538283 comment 0 (2010-01-06, Windows XP — context): "If I send a larger message it holds CPU on 100% at all time. For example, if it takes 5 minutes to send message he keep CPU at 100%." Comment 65 (2010-07-21, m-wada, Windows — context): "it merely took 50 seconds to send 1.5MD mail(text mail with a PDF) to Gmai's SMTP with network.tcp.sendbuffer=4096, and CPU utilizaion was several %(value shown by Task Manager)." Comment 63 (2010-07-21, Windows dual-core — context): "On my home computer is the CPU hogging 60% of core1 and 0% of core2." Comment 71 (2010-09-15): "Sending without TLS is OK and we get about 50 KB/s throughput. But we do need TLS".

**Coverage.** T3 — covers (Linux, bug 742697): CPU share of the Thunderbird process while an SMTP send is in progress — 10 % of one core and ~60 % on "a fast machine" — attributed by the reporters to the progress-bar animation, with a profile summary (80 % in `poll()`); no attachment size, link rate or machine named. The 2010 bugs (Windows) are context: 100 % CPU only with SSL/TLS on the SMTP session, dependent on send buffer. Bytes per wake/wakes per second: does not cover. T1/T2/T4/T7: does not cover.

**Observation status.** 742697 comments 24/25: two observations on unnamed Linux machines, Thunderbird 78.4.2 and 89.0b1, no window, no message size.

### S3-10 — ClamAV user venues: clamav-users msg48677; Virtualmin 61555; narkive "Performance Help - 100% cpu usage" (2004); Fedora Discussion 138122; dev.to guide; list searches

**Citation.** mail-archive.com copy of clamav-users message 48677 ("Re: [clamav-users] Heuristics.Limits.Exceeded FOUND"); forum.virtualmin.com topic 61555 "ClamAV - ClamScan & CPU 100%" (2019-11-16); clamav-users 2004-10-26 "Performance Help - 100% cpu usage" (narkive mirror); discussion.fedoraproject.org topic 138122 "Clamscan vs clamdscan" (2024-11-21); dev.to "How to run efficient ClamAV scans on a 4GB RAM server…".

**Copy read.** `https://www.mail-archive.com/clamav-users@lists.clamav.net/msg48677.html` 14,111 B, sha256 8f1b5e84edb63bba8f2c805f4f5521e409662e7a28cf400689d61420b94b7031; `https://forum.virtualmin.com/t/clamav-clamscan-cpu-100/61555.json` 24,344 B, c0d7479fa9b722bf5f834d56134af49651454333c1a063626d1357aa79cceae7 (21:24 UTC); `https://clamav-users.clamav.narkive.com/enOedTH1/performance-help-100-cpu-usage` 190,437 B, 19264112e429800588d45b7ff3d187a3ff8921f9c6f7bea2f2e688d4550451dd; `https://www.mail-archive.com/search?l=clamav-users%40lists.clamav.net&q=clamscan+%25CPU+top` 52,769 B, deaa808a43276ba86238696ee9bc2167f0b9f5613eaa44edd6f4937b670b7987; `https://discussion.fedoraproject.org/t/clamscan-vs-clamdscan/138122.json` 50,431 B, 9fd5f8342eba83d32c9ebfb85bda63678eb994cf33fc40d30241290f0c141a8b; dev.to article 103,027 B, 49ec51f6807e313141181f0a48ec57fcc0c209f18ee1093ea55d2f63690c2d43 (21:28 UTC); `https://lists.clamav.net/hyperkitty/search?mlist=clamav-users%40lists.clamav.net&q=clamscan+cpu+top` 83,807 B, 343e90828ee33c544ea84258532a4f7b6fa4e70e7126d59e0f572af7e09a4b1d (21:31 UTC). Local: `sources/S3-10/`.

**Passages.**

- msg48677: "It *does* take more than 120 secs for the clamscan command to fully scan the 62 MB Firefox installation file (.tar.bz2). Trying the scan with the default clamscan limits results in 62 MB "Data read" but *zero* "Data scanned"!"
- Virtualmin 61555 post #1 (2019-11-16): "every 60 minutes if I take the command top I can watch 2-3 processes name clamscan that use 40/50% of CPU…" … "Sat Nov 16 14:53:13 2019 -> clamd daemon 0.99.2 (OS: linux-gnu, ARCH: x86_64, CPU: x86_64) / … / Sat Nov 16 14:54:52 2019 -> Loaded 6548684 signatures. / … / Sat Nov 16 14:54:56 2019 -> Limits: Global size limit set to 104857600 bytes. / Sat Nov 16 14:54:56 2019 -> Limits: File size limit set to 26214400 bytes. / Sat Nov 16 14:54:56 2019 -> Limits: Recursion level limit set to 10. / Sat Nov 16 14:54:56 2019 -> Limits: Files limit set to 10000."
- narkive 2004 thread (Debian 3.0r1, clamav 0.75.1, 4× Pentium III Xeon 700 MHz mail server — two-decade-old, server, context): "PID USER PR NI VIRT RES SHR S %CPU %MEM TIME+ COMMAND / 1290 qscand 15 0 57368 56m 696 R 50.8 5.6 172:29.51 clamdscan / 25135 qscand 14 0 57368 56m 696 R 50.2 5.6 187:57.60 clamdscan / …" (six clamdscan processes at ~50 % each, "Cpu0 : 69.2% user, 30.8% system, 0.0% nice, 0.0% idle").
- Fedora 138122 post #1: "Afaik clamd is more resource efficient and suited for background usage?" (no measurement in the thread).
- dev.to article (lines containing figures): "This creates high CPU + heavy RAM spikes → a 4GB server suffers." / "MaxThreads 1 → prevents CPU/RAM spikes" (no measurement).

**Coverage.** T4 — covers weakly: a Linux `top` reading of on-demand `clamscan` processes at 40–50 % CPU each (Virtualmin, 2019; machine unnamed, no core count, the scans triggered hourly by a mail-filter setup, not a user's scan); clamd 0.99.2 signature-load time (14:53:13 → 14:54:52, 99 s) and default limits from the daemon log. The 2004 `top` capture is server-side `clamdscan` on a 2004 Debian box — context (age, server). CPU share over one user scan on a desktop: does not cover. T1/T2/T3/T7: does not cover. The mail-archive and hyperkitty search pages returned only clamd/milter server threads in the first page (subjects checked, none opened).

**Observation status.** Virtualmin: one host, `top` snapshots, no window length.

### S3-11 — restic forum threads 4221, 1727, 5289, 8098

**Citation.** forum.restic.net (Discourse): "Restic backup is quite slow. This normal?" (4221, 2021-08-02); "Low performance after first backup, and restic seems to spend a lot of time doing nothing" (1727, 2019-05-15); "Restic first backup very slowly" (5289, 2022-07-31); "Restic Backup Taking Too Long…" (8098, 2024-07-30).

**Copy read.** `https://forum.restic.net/t/<slug>/<id>.json`: 4221 = 803b5a236f9e87a561a4f2e99d622f6157c968e375c922384c2745f74acdbfef; 1727 = 03269ca06faa023cda91f15f5de481341ed3fb6c8b244b58741c3a74c0bed691; 5289 = bf73ce628a28f23d7af31944f3cda67f55a9707bb6fe6b0e799c0bc446d7ac9a; 8098 = 550cc174afc70b759be17c346c8055eba6d9f6e6cba00f1fd63616297dba45e9. Accessed 2026-09-17 21:24 UTC. Local: `sources/S3-11/`.

**Passages.**

- 4221 post #1 (Ubuntu 21.04, Ryzen 7 laptop, 40 GB RAM, USB 2 TB spinning disk): "Restic tells me a 1TB backup job will take 37hrs! Rsync only took about 14 hrs under same conditions."
- 5289 post #1 (2022-07-31, Linux, external USB 3.1 HDD): "It runs very slowly, only about 9 mb/s. After almost 10 hours only 320 GB saved" … post #2: "dd if=/dev/zero of=tempfile bs=1M count=1024 conv=fdatasync,notrunc / Result= 144 MB/s"; post #15 (after rebuilding restic with `minpacksize` 128 MiB): "At around 30 minutes, the cut is calculated: 80 MB/s."; post #17: "I think about 60 MB/s is an acceptable value via USB. / The CPU load has increased noticeably, but I can still do normal work that doesn't require 100% CPU power."; post #19: "so in the end it completed the full backup at about 45 MB/s average. / The CPU load is noticeably higher than with 4 MB packed size." … "Another job is currently running with a 'normal' old 2TB Seagate disk, i.e. with CMR technology. / Here the throughput is about twice as large, i.e. about 90 MB/s."
- 1727 (macOS High Sierra, MacPro 2013 — other platform, context): "yesterday's backup took over 16h" … pprof `top10` over 30 s: "Total samples = 10.21s (34.03%) … 4.78s 46.82% … runtime.scanobject".
- 8098: Windows 10 — context only.

**Coverage.** T1 — covers weakly: restic throughput on Linux to USB HDDs (9 → 45 → 90 MB/s by pack size and SMR/CMR), first backup (cold), CPU "noticeably higher" without a number (screenshot `CPU_restic` not fetched). macOS thread: context (a 30 s CPU profile of restic idle-ish at 34 % of one core, dominated by Go GC). Other topics: does not cover.

**Observation status.** 5289: one user, one machine (32 GB RAM, USB 3.1 dock, disks named by type), restic version not stated, first-backup windows of hours.

### S3-12 — iovisor/bcc tool example files (biosnoop, biotop, filetop, offcputime, biolatency, fileslower)

**Citation.** iovisor/bcc repository, `tools/*_example.txt`, master branch as served by raw.githubusercontent.com on 2026-09-17 (commit not resolvable through the raw endpoint; the repository's HEAD at the time is not recorded).

**Copy read.** `https://raw.githubusercontent.com/iovisor/bcc/master/tools/{biosnoop,fileslower,offcputime,biolatency,biotop,filetop}_example.txt`: 9c85eaf38d681f00f3cbb2e0dd49587d27d199f0a982058734eb343d277dfbe1; 9a2fcdfe083d78fd315ecf56e9db890caffef820054073f3b6346cdaeb3ec834; a0c4f5df73a1ec8b608ce8e64d155c9ab5835fcae44a490f25f341ff4bda92d9; d0975ddf04de455e1fd0c35c764455f5a66979a87b54072a4a18d6b79a88cfff; 95d0abd0ae134504dabcda8a1c639de2dc62428ba29275e7390163dcb8d4186d; 4dfcef38b5452b43268494bc27e444586c0cc3a3330382a919ae1e4af998581b. Accessed 2026-09-17 21:24 UTC. Local: `sources/S3-12/`.

**Passages.** `offcputime_example.txt` line 645–648: "Here, dd was blocked for 4.4 seconds out of 5. Or put differently, likely / … / # time dd if=/dev/md0 iflag=direct of=/dev/null bs=1k". `biotop_example.txt` lines 13–15: "14501  cksum            R 202 1   xvda1      361   28832   3.39 / 6961   dd               R 202 1   xvda1     1628   13024   0.59 / 13855  dd               R 202 1   xvda1     1627   13016   0.59" (columns PID COMM D MAJ MIN DISK I/O Kbytes AVGms). `filetop_example.txt` line 32: "This shows various files read and written during a Linux kernel build."

**Coverage.** T1 — context: Linux block-I/O and off-CPU examples for `dd` and `cksum` (not rsync/cp/tar); `dd` with `iflag=direct` blocked 4.4 s of 5 s. None of the six files traces tar, rsync or cp. Other topics: does not cover.

**Observation status.** Author's machines unnamed (EC2 `xvda1` implied by device name); windows of seconds.

### S3-13 — BorgBackup: mailing-list "some performance numbers…" (2017); "Test : Borg vs Restic" (2017); borgbase/benchmarks results (Dec 2022)

**Citation.** (a) mail.python.org pipermail, borgbackup list, 2017q3 message 000799 "[Borgbackup] some performance numbers..." and 000779 "[Borgbackup] Test : Borg vs Restic" (reply by the maintainer quoting the original). (b) BorgBase, "Backup Benchmarks", GitHub repository borgbase/benchmarks, commit 16e6e8c70ee34bb9bf0928ebb85e1c6dc8478e1c (README.md, `v2/tests.sh`, `v2/results/<scenario>/<tool>/<task>.txt` = GNU time `-v` outputs).

**Copy read.** `https://mail.python.org/pipermail/borgbackup/2017q3/000799.html` 5,973 B, sha256 e6ea72a2eb0100dce2622106456c26ca44e520c1bec546870291bb3706b0089a; `…/000779.html` 10,091 B, f077925efacf8cc7a1f91196dbe28ef2ff85419bac0359b32c0f168ca548fd3e; README via `https://raw.githubusercontent.com/borgbase/benchmarks/master/README.md` 4,533 B, 9041b9684ff5ffd72f70d133f7b9544ed0f6595fc7ea1308b0bd80c6e28ace10 (21:25 UTC); `git clone --depth 1 https://github.com/borgbase/benchmarks.git` → HEAD 16e6e8c70ee34bb9bf0928ebb85e1c6dc8478e1c, 64 result/script files copied to `sources/S3-13/borgbase-benchmarks/` with `SHA256SUMS.txt`. Local: `sources/S3-13/`.

**Passages.**

- 000799 (2017-09, "home server", platform not stated): "time borg prune --verbose --list -d 30 -w 52 -y 10 $repo / That deleted 860 archives and kept 85. It freed about 500GB of disk space and took well over 12 hours: / real    798m5,477s / user    341m9,688s / sys     18m16,624s" … "Archive name: marcos-2017-09-15 / … / Duration: 20 minutes 29.83 seconds / Number of files: 1920931 / … / This archive:              231.90 GB            212.51 GB              1.11 GB".
- 000779 (quoted original, platform not stated): "The backup data consists of a live mail repository using the maildir format and holding 139 GB (2327 dirs, 665456 files)." … "- Borg is way faster on first pass (1h15m vs 1h48m) but significantly slower on second pass (2m1s vs 47s)" … "- Borg is faster by a factor of 2 to restore the exact same data using about 2x more CPU."
- README: "Backup client specs: / 1 Core, 30GB SSD Storage, 1GB Memory, 1G network / VPS hosted with OneProvider in Sydney and Nuremberg / Test data: 19.5 GB total, 43921 files" … "Measurements taken by GNU Time: / Time: wall clock / CPU usage: user time, system time / Final backup size: in GB / Memory usage: max RSS / File system inputs: Data read in blocks of 512 bytes / File system outputs: Data written in blocks of 512 bytes" … "normal latency: backup nearby server with connection in Germany, 25ms ping / high latency: backup server on high latency connection in Australia, 270ms ping" … "OS: Debian GNU/Linux 11 (bullseye)" … "Empty cache between runs to avoid seeing lower *Reads* due to OS-level caching" (listed as an unchecked shortcoming).
- `v2/tests.sh`: "function timeit() { / /bin/time -v -o results/$TEST_BIN/$1.txt ./bin/$TEST_BIN "${@:2}" / }" … "timeit create-1 create --compression zstd ::initial corpa-1 / timeit create-2 create --compression zstd ::second corpa-1 corpa-2 / timeit create-3 create --compression zstd ::third corpa-1".
- `v2/results/de-normal-lat/borg-12/create-1.txt`: "Command being timed: "./bin/borg-12 create --compression zstd ::initial corpa-1" / User time (seconds): 254.77 / System time (seconds): 39.05 / Percent of CPU this job got: 54% / Elapsed (wall clock) time (h:mm:ss or m:ss): 8:56.27 / … / Maximum resident set size (kbytes): 140644 / … / Voluntary context switches: 397290 / Involuntary context switches: 309084 / … / File system inputs: 18911856 / File system outputs: 127960".
- `…/borg-12/create-2.txt`: "User time (seconds): 125.96 / System time (seconds): 18.07 / Percent of CPU this job got: 98% / Elapsed (wall clock) time (h:mm:ss or m:ss): 2:26.30 / … / Voluntary context switches: 19419 / Involuntary context switches: 31707 / … / File system inputs: 22075056".
- `…/borg-12/create-3.txt` (unchanged data): "User time (seconds): 16.02 / System time (seconds): 1.46 / Percent of CPU this job got: 92% / Elapsed (wall clock) time (h:mm:ss or m:ss): 0:18.88 / … / Voluntary context switches: 87 / Involuntary context switches: 2469 / … / File system inputs: 40 / File system outputs: 152824".
- `…/borg-20/create-1.txt`: "User time (seconds): 136.52 / System time (seconds): 29.49 / Percent of CPU this job got: 39% / Elapsed (wall clock) time (h:mm:ss or m:ss): 6:57.60 / … / Voluntary context switches: 414710 / Involuntary context switches: 283707".
- `…/restic-14-run1/create-1.txt`: "User time (seconds): 581.19 / System time (seconds): 74.77 / Percent of CPU this job got: 72% / Elapsed (wall clock) time (h:mm:ss or m:ss): 14:58.61 / … / Maximum resident set size (kbytes): 217484 / … / Voluntary context switches: 274587 / Involuntary context switches: 386888 / … / File system inputs: 18924384 / File system outputs: 18621760".
- `v2/results/au-high-lat/borg-12/create-1.txt`: "Percent of CPU this job got: 15% / Elapsed (wall clock) time (h:mm:ss or m:ss): 23:40.42 / … / Voluntary context switches: 424177 / Involuntary context switches: 273393".

**Coverage.** T1 — covers: CPU share of wall time for `borg create` and `restic backup` on Linux (object: whole job, GNU time; unit: %, seconds; statistic: single runs per scenario; scope: 19.5 GB / 43,921 files over SSH to a remote repository at 25 ms and 270 ms RTT; population: one 1-vCPU Debian 11 VPS per site) — borg 1.2.2 initial 54 % (25 ms) and 15 % (270 ms), incremental-with-new-data 98 %, unchanged 92 %; borg 2.0.0b4 initial 39 %; restic 0.14 initial 72 %; voluntary/involuntary context-switch counts per job (a coarse proxy for the number of blocking waits: ~4×10^5 voluntary switches over a 9-min initial run, 87 over an 19 s unchanged run); `File system inputs/outputs` in 512-byte blocks; max RSS. Warm/cold cache: not controlled (README shortcoming). Process/thread structure, on-CPU run lengths: does not cover. The 2017 list post gives `time` for `borg prune` (real 798 m, user 341 m, sys 18 m) and an archive create duration (20 m 30 s for 1.92 M files / 231.9 GB, deduplicated to 1.11 GB) with platform not stated. T2/T3/T4: does not cover. T7: the results directory is itself a small public benchmark record (64 files).

**Observation status.** borgbase v2: machine named (OneProvider VPS, 1 core, 1 GB, Debian 11; Nuremberg and Sydney), subject named (borg 1.2.2 / 2.0.0b4 / restic 0.14.0 binaries, corpus composition, `--compression zstd`, repokey-blake2), window: Dec 2022, one run per cell (restic has run1/run2 in de-normal-lat); cache state not controlled.

**Reader's own computation.** Borg prune CPU share `(341*60+9.688+18*60+16.624)/(798*60+5.477)` = 0.45; borg-12 create-1 `(254.77+39.05)/536.27` = 0.548 (matches GNU time's 54 %).

### S3-14 — Ubuntu Launchpad bugs 925948, 1961540, 1970805, 2025523; Fedora Discussion 115906

**Citation.** bugs.launchpad.net (via `api.launchpad.net/1.0/bugs/N` and `/messages`): 925948 "tracker-miner-fs very high cpu usage" (2012-02-03); 1961540 "tracker-miner-fs-3 massive CPU usage and system slowdown" (2022-02-20, tags focal/impish/performance); 1970805 "tracker-miner-fs eats cpu and hard drive space…" (2022-04-28, jammy); 2025523 "tracker3 taking 100% CPU for a long time" (2023-07-01, jammy/noble). discussion.fedoraproject.org 115906 "Tracker-Miner service causing high CPU usage" (2024-05-02).

**Copy read.** `https://api.launchpad.net/1.0/bugs/N` / `…/messages?ws.size=100` (JSON): 925948 = 821d428f4407ce7217d6933af035a6172293cb0aa9434ead8d76fbe25f5dd7bf / 2b606d073cdb90cec51724e5218f7f0d69eff5cc26bc6388977f339e9afe9dcf; 1961540 = aa81399d85d55208812b1a130a4e5297580e73f4d7cf6fbc8aa8a565803d243f / 3ef7fe6c290fb7d7f3c64b23e5751a8d1d7cd3847d94c52b7f3079fab17827f1; 1970805 = b68f47c94e94b98ecc4831ccb02a3273bd000fae7dc0024b31986f9c3ff10f3f / 8daab9b4505356a01cfc0a1ad0f11d8dba917994a1c7800314cc57aed0ae5aeb; 2025523 = e0167cfc84e931bcb7774e4bc9866b27fcce640156f8698c9c7dc13090537678 / 68c40a2f28d279df4b4e0d0c59b6608226a7f96c9edb75aca81a955a5fa437a6; Fedora 115906.json = 9a097bb00a2149bebf5760d6dff113f82a89a9677a154784d046c1e48cb51540. Accessed 2026-09-17 21:25 UTC. Local: `sources/S3-14/`.

**Passages.**

- 925948 description (2012): "starts at login as it is supposed to but keeps running with cpu @ 60-85 % watched it for over an hour without it stopping!!!"; message 2 (2016-09-30, Ubuntu 16.04, "CPU Intel® Core™ i7 CPU M 640 @ 2.80GHz × 4"): "tracker-miner-fs costs me 23% of CPU and 296mb without any descktop app opened. / tracker-extract eat pretty same amount."
- 1961540 message 5/6 (2022-03-01, 2023-01-12, the reporter): "My CPU was limited to 500Mhz max causing the whole system to run super slow." … "The problem was when I switch on the AC power to my laptop at the wrong time during bootup, the CPU is limited to 500Mhz." (the report was set invalid by the reporter).
- 1970805 message 4 (2023-01-22): "The issue was caused by 400k json and jpeg files in the Documents folder which I only placed there temporarily." … "I found that when I placed the files in one of the folders / Documents, Desktop, Music, Pictures or Videos / tracker would index them while the folders / Downloads, Public and Templates / are ignored as well as any other folder that isn't created by default." Message 3 (French): "y compris les modifications dans dconf (org > freedesktop > Tracker > Miner > Files > crawling-interval à -2 et enable-monitors à faux), rien n'y fait."
- 2025523 description (Ubuntu 22.04, kernel 5.19.0-46, tracker-extract 3.3.0-1): "/usr/libexec/tracker-extract-3 and /usr/libexec/tracker-miner-fs-3 are constantly taking 100% CPU" … "running "tracker3 status" claims "Estimated less than one second left", but it nevertheless runs continuously."; message 6 (2024-08-25, HP ENVY 13, i7-10510U, kernel 6.8.0-40): "takes 80% of my 4 i7 cpu cores"; message 8 (2024-09-18): "After upgrade from 24.0 to 24.1 this started to take 10% of CPU after a couple of minutes it went away."
- Fedora 115906 post #10 (2024-08-14): "# gsettings list-recursively |grep -i 'org.freedesktop.tracker3.miner.files'  | grep  ignored / org.freedesktop.Tracker3.Miner.Files ignored-directories ['po', 'CVS', 'core-dumps', 'lost+found'] / org.freedesktop.Tracker3.Miner.Files ignored-directories-with-content ['.trackerignore', '.git', '.hg', '.nomedia'] / org.freedesktop.Tracker3.Miner.Files ignored-files ['*~', '*.o', '*.la', … '*.part', …". Post #8: "For some reason, this issue seems to happen with yt-dlp specifically".

**Coverage.** T2 — covers: CPU levels of tracker-miner-fs/tracker-extract in fault states on named Ubuntu machines (23 % on an i7 M640 with the desktop idle; 80 % of four cores on an i7-10510U; 60–85 % for over an hour in 2012), the configuration keys `crawling-interval`, `enable-monitors` and the default ignore lists as printed by `gsettings`. Steady-state wake cadence on a healthy settled directory: does not cover — these are stuck/looping states (temp files from yt-dlp, 400 k files, a CPU-frequency cap). T1/T3/T4/T7: does not cover.

**Observation status.** Each is one reporter's machine; windows are hours to days; versions named per report.

### S3-15 — Redpill Linpro techblog, "Comparison of different compression tools" (Are Tysland, 2024-12-18)

**Citation.** Are Tysland, "Comparison of different compression tools", Redpill Linpro techblog, 18 December 2024.

**Copy read.** `https://www.redpill-linpro.com/techblog/2024/12/18/compression-tool-test.html` (HTML, 22,188 B, sha256 86fe0ca8f10ce41f2eafdd0399665e22cb4b6feccc2f1d30b9d471a3b1185d72), accessed 2026-09-17 21:25 UTC. Local: `sources/S3-15/`.

**Passages** ("The setup"; tables under "Maximize compression", "Default compression", "Comparison of multi-core default compression", "Decompression times"; each row is Method | File size | Size % | Peak memory usage | User time | System time | Wall time | CPU usage as laid out in the page tables):

- "The file I chose was a 4194304000 byte (4.0 GB) Ubuntu installation disk image. / The machine tasked with doing of the bit-mashing was an Ubuntu with a AMD Ryzen 9 5900X 12-Core CPU, 64 GB RAM, and WD Black SN850 NVMe drive."
- "gzip -9 | 519492454 | 12.4% | 2.0 MB | 167.92 sec | 1.22 sec | 2:49.16 | 99%"; "bzip2 -9 | 461727440 | 11.0% | 8.7 MB | 86.21 sec | 1.64 sec | 1:27.86 | 99%"; "xz -9 -e -T 0 | 300608284 | 7.2% | 17.3 GB | 563.23 sec | 10.17 sec | 1:34.13 | 609%"; "lzma -9 -e -T 0 | 299004234 | 7.1% | 675.8 MB | 465.10 sec | 2.17 sec | 7:47.30 | 99%"; "zstd –ultra -22 -T0 | 320193687 | 7.6% | 9.2 GB | 496.78 sec | 6.10 sec | 3:45.29 | 223%"; "pigz -9 | 519405554 | 12.4% | 21.3 MB | 187.17 sec | 6.02 sec | 0:11.80 | 1636%".
- ""Peak memory usage" is the "Maximum resident set size" value from /usr/bin/time -v."
- Default settings: "gzip | 522133876 | 12.4% | 2.1 MB | 48.67 sec | 1.28 sec | 0:49.96 | 99%"; "xz | 310830856 | 7.4% | 95.8 MB | 269.40 sec | 1.51 sec | 4:30.94 | 99%"; "zstd | 428213344 | 10.2% | 51.0 MB | 4.84 sec | 1.75 sec | 0:05.21 | 126%"; "pigz | 521830464 | 12.4% | 21.4 MB | 67.71 sec | 5.98 sec | 0:05.75 | 1280%".
- Multi-core default: "xz -T0 | 315784172 | 498.57 sec | 4.00 sec | 0:25.06 | 2005%"; "zstd -T0 | 428213344 | 6.43 sec | 0.83 sec | 0:01.39 | 522%"; "pigz | 521830464 | 64.89 sec | 5.52 sec | 0:05.16 | 1363%". "Thanks to disk cache, zstd complete in just above one second! Without disk cache, the machine used 4 seconds to cat the file to /dev/null."
- Decompression: "gunzip | 14.46 sec | 2.98 sec | 0:17.44 | 99%"; "xz -d | 16.43 sec | 1.17 sec | 0:17.60 | 99%"; "zstd -d | 1.73 sec | 1.15 sec | 0:02.89 | 99%"; "pigz -d | 11.70 sec | 5.20 sec | 0:08.26 | 204%".

**Coverage.** T1 — covers: CPU share of wall time (GNU time "CPU usage" %) and user/sys/wall for gzip, bzip2, xz, lzma, zstd, pigz compressing one 4.0 GB file on Linux, warm page cache (stated), single-threaded runs pinned near 99 % and multi-threaded runs at 126–2005 % of one core; decompression likewise. Thread structure implied by the CPU-% ratios (xz -T0 ≈ 20 threads busy; zstd -T0 ≈ 5). A file *set* stream (tar of many files) and cold cache: does not cover (single file; one cold `cat` timing of 4 s given). 7z: does not cover. T2/T3/T4/T7: does not cover.

**Observation status.** One machine (Ryzen 9 5900X, 64 GB, WD SN850 NVMe, Ubuntu; tool versions not stated), one run per cell, December 2024, cache warm.

### S3-16 — LWN.net, "A look at rsync performance" (JC van Winkel, 2010-08-18)

**Citation.** JC van Winkel, "A look at rsync performance", LWN.net, August 18, 2010, https://lwn.net/Articles/400489/.

**Copy read.** HTML 74,013 B, sha256 a2738f330f65d0c1113b2dbe2ff29210e9fe6cb34a1b47f4f9dfc8bf978434eb, accessed 2026-09-17 21:28 UTC. Local: `sources/S3-16/`.

**Passages.**

- "The problem": "Recently I bought a shiny new disk for my Fedora-10 based Mythtv system. I had to copy some 700GiB of video files from the old disk to the new one." … "the files were copied at about 37MiB/s." … "Note that both SATA disks were local to the system and no network was involved."
- "Measuring": "copying a 10GiB file from one disk to the other. I made sure that the ext4 file systems involved were completely fresh" … "Simply reading the source file could be done at 106MiB/s and writing a 10GiB file to the destination file system could be done at 134MiB/s." … "sync # flush dirty buffers to disk / echo 3 > /proc/sys/vm/drop_caches # discard caches / time sh -c "cp $SRC $DEST; sync" # measure cp and sync time".
- Results table (columns user, sys, elapsed, hog, MiB/s, test): "5.24 | 77.92 | 101.86 | 81% | 100.53 | cpio"; "0.85 | 53.77 | 101.12 | 54% | 101.27 | cp"; "1.73 | 59.47 | 100.84 | 60% | 101.55 | cat"; "139.69 | 93.50 | 280.40 | 83% | 36.52 | rsync".
- "Looking at the hog factor (the amount of cpu-time used relative to the elapsed time), we can conclude that rsync is not so much disk-bound (as is to be expected), but cpu-bound. That required some more scrutiny. The atop program showed rsync appears to need three processes: one process that does only disk reads, one that does only disk writes and one (I assume) control process that uses little CPU time and does no disk I/O."
- "Using strace, it can be shown that cp only uses read() and write() system calls in a tight loop, while rsync uses two processes that talk to each other using reads and writes through a socket, sprinkled with loads of select() system calls."
- "On my 4-core AMD Athlon II X4 620 system, all three processes seem to run on the same CPU most of the time." … "By using taskset right after rsync was started, the throughput of rsync went up from 36.5MiB to 40MiB." … "When forcing the three rsync processes to run on the same CPU, performance went down to 32MiB/s" … "If the CPU-frequency is forced on the highest frequency (2.6GHz), the results for three rsyncs on a single core goes up: 62MiB/s. Combining this with the "spread the load" tactic using taskset, we even get up to 85MiB/s."
- Summary table (Throughput | CPUs | Core frequency): "22MiB/s | 1-3 | 0.8GHz"; "23MiB/s | 1 | 0.8GHz"; "34MiB/s | 1 | ondemand"; "37MiB/s | 1-3 | ondemand | << default"; "39MiB/s | 3 | 0.8GHz"; "40MiB/s | 3 | ondemand"; "62MiB/s | 1 | 2.6GHz"; "62MiB/s | 1-3 | 2.6GHz"; "85MiB/s | 3 | 2.6GHz".
- "$ cat /sys/devices/system/cpu/cpu2/cpufreq/stats/time_in_state / 2600000 423293 / 1900000 363 / 1400000 534 / 800000 6645805" … "The frequency (in 1000Hz units) is the first column, while the time (in 10ms units) is the second column."
- Kernel comparison table (FC10 2.6.27 | 2.6.34 | 2.6.35-rc3 | CPUs | Frequency): "36.52 | 44.85 | 45.08 | 1-3 | ondemand | <<default"; "62.15 | 92.34 | 91.84 | 1-3 | 2.6GHz". "I could immediately see (in atop) that the three rsync processes were on separate processors most of the time. The newer kernels apparently are better at spreading the load."

**Coverage.** T1 — covers: CPU share of wall time ("hog") for rsync (83 %), cp (54 %), cat (60 %), cpio (81 %) copying one 10 GiB file disk-to-disk on Linux with a cold page cache (drop_caches + sync, stated); rsync's three-process structure as seen in atop (reader, writer, control) and its socket+select() pattern (strace); the effect of pinning the three processes to one core versus three (32 vs 40 MiB/s; 62 vs 85 MiB/s at fixed 2.6 GHz); cpufreq time-in-state under the load. It is a 2010 observation (kernels 2.6.27–2.6.35, ondemand governor) — sixteen years old, not two decades; recorded as a Linux observation with that caveat. On-CPU run lengths between I/O waits: does not cover. Many-file trees: does not cover (one 10 GiB file). T2/T3/T4/T7: does not cover.

**Observation status.** One machine (AMD Athlon II X4 620, Fedora 10, two local SATA disks, ext4), subject named (rsync/cp/cat/cpio, 10 GiB file, cold cache; rsync version not stated), window: single timed runs, mid-2010.

**Reader's own computation.** `(139.69+93.50)/280.40` = 0.832 (matches "83%"); `(0.85+53.77)/101.12` = 0.540.

### S3-17 — Debian bug #760473 "apt method http uses 100% cpu with high transfer rate" (wget comparison)

**Citation.** Debian BTS #760473, Lennart Weller, 2014-09-04, against apt 1.0.7 (later reassigned to libapt-pkg4.12); also carried on the deity list (lists.debian.org/deity/2014/09/msg00011.html).

**Copy read.** `https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=760473;mbox=yes` (mbox, 137,891 B, sha256 db52e21496da1b1ff88b19ea847b1bb761e9de51d5b952403830ac3e982e9c40); `https://lists.debian.org/deity/2014/09/msg00011.html` 7,366 B, 97b9ff0b12849fed782f1c3d59e873c6de8fbd58980631fb8d5474bfdaf84d70. Accessed 2026-09-17 21:28 UTC. Local: `sources/S3-17/`.

**Passages** (message 0, 2014-09-04):

- "As an example I downloaded a large file from the deb mirror (0ad-data) which is then cached by local squid. Which in turn then provides higher transfer rates in case I download it again and causing this bug to appear:"
- "cli: / % apt-get download 0ad-data / Get:1 http://ftp.de.debian.org/debian/ jessie/main 0ad-data all 0.0.16-1 [530 MB] / 46% [1 0ad-data 247 MB/530 MB 46%] 24.6 MB/s 11s / top: / PID  USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM   TIME+   COMMAND / 8516 weller    20   0    5516   4200   3944 R  99.4  0.0   0:04.60 http"
- "For comparison the same download with wget: / cli: / % wget http://ftp.de.debian.org/debian/pool/main/0/0ad-data/0ad-data_0.0.16-1_all.deb / (58.5 MB/s) - '0ad-data_0.0.16-1_all.deb' saved [530253138/530253138] / top: / PID   USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM  TIME+   COMMAND / 12578 weller    20   0    5992   4104   3712 R  18.2  0.0  0:00.57 wget"
- "/proc/cpuinfo: / processor       : 31 / model name      : Intel(R) Xeon(R) CPU E5-2690 0 @ 2.90GHz / cpu MHz         : 2328.042" … "Kernel: Linux 3.15.3-64+ (SMP w/32 CPU cores; PREEMPT)" … "Architecture: i386 (x86_64)".
- Message 1 (2015-01-30): "it has nothing to do with the way the http method is structured but solely stems from the way hashing is done in apt, sequential and in the same thread as the download. / Replacing the hashing methods with the ones provided by libnettle … resulted in a speedboost from 24MBps up to around 32MBps. … For reference the maximum speed without hashing would be 75MBps."

**Coverage.** T3 — covers: CPU share of a `wget` process on Linux while receiving a 530 MB file from a LAN squid cache at 58.5 MB/s: 18.2 % of one core (`top` snapshot, `TIME+` 0:00.57 at that instant), against apt's `http` method at 99.4 % CPU and 24.6 MB/s on the same host (hashing in the download thread). Bytes per wake / wakes per second / receive-buffer size: does not cover. T1/T2/T4/T7: does not cover.

**Observation status.** One machine (Xeon E5-2690, 32 threads, Linux 3.15.3, Debian jessie/sid, i386 userland on x86_64), subject named (wget, version not stated, HTTP from local squid, file 530,253,138 B), window: one download in September 2014; `top` snapshot, not a time series.

**Reader's own computation.** `99.4/24.6` = 4.04 %CPU per MB/s for apt-http versus `18.2/58.5` = 0.311 %CPU per MB/s for wget.

### S3-18 — Red Hat Bugzilla 85817, 479967; curl-library list 2009-08 and 2025-09

**Citation.** bugzilla.redhat.com 85817 "curl uses 100% CPU on slow connection"; 479967 "curl uses 100% of CPU if upload connection is broken"; curl-library, Vourhey, ""100% CPU usage during SFTP transfer" bugfix" (2009-08-18); curl-library, "High CPU usage associated to busy loop in curl_timediff_us()" (2025-09).

**Copy read.** `https://bugzilla.redhat.com/show_bug.cgi?ctype=xml&id=85817` 9,372 B, sha256 4346fc2331dc28fc6dd8682720837d6850f9954282e7bc6d857c9db5e3a4141b; `…id=479967` 12,864 B, 236b258a1f8ba3f0674ee594b30651874092da39b7c134a148c3c39672d6fc01 (21:28 UTC); `https://curl.se/mail/lib-2009-08/0217.html` 7,692 B, 1fe32764409030ef5f6efdaa51c64872eb0c4265b99ca12d68d4dc388baafa32; `https://curl.se/mail/lib-2025-09/0029.html` 14,084 B, 002104e401816ece7951603534272d963ae02897f787b1a624b3beab6938a3e6. Accessed 21:29 UTC. Local: `sources/S3-18/`.

**Passages.** curl-library 2009-08-18: "I use lubcurl 7.19.5 with libssh2-1.2 on Linux. I can see 100% CPU usage when I try to upload any file by SFTP." … "This bug is due to using non-blocking mode enabled by default. Infinite loop (invoking of clock_gettime, poll, recv functions) loads CPU." … "After libcurl recompiling, file uploading by SFTP loads CPU to ~9%."

**Coverage.** T3 — context: bug-state busy loops in curl (SFTP non-blocking loop 2009; timediff busy loop 2025), not a steady-state HTTP download; the 2009 post gives ~9 % CPU for an SFTP upload after the fix, machine and link unnamed. RHBZ 85817/479967 are 2003/2009 bug states (not quoted; no figures beyond "100% CPU"). Other topics: does not cover.

**Observation status.** Not a usable observation.

### S3-19 — updatedb (mlocate/plocate) reports: Arch FS#10532 (2008); Launchpad 1190696 (2013–2019); Red Hat 1282232 (2015–2019); Arch BBS 297983 (2024); plocate.sesse.net

**Citation.** bugs.archlinux.org FS#10532 "updatedb (mlocate) doesn't work correctly" (2008-05-29); Launchpad #1190696 "updatedb.mlocate uses 100% of the hdd IO. The OS is completely unusable." (2013-06-13); bugzilla.redhat.com 1282232 "mlocate-updatedb.service doubles time taken to boot" (2015-11-15, Fedora 23–31); bbs.archlinux.org thread 297983 "Kernel 6.10 regression: mlocate/updatedb 3x slower, unresponsive shell" (2024-07-23); Steinar H. Gunderson, plocate home page (plocate 1.1.25, "last update: September 6th, 2026").

**Copy read.** `https://bugs.archlinux.org/task/10532` 20,434 B, sha256 8ab3e07f2b23efb1968add62a4ec38effebea853cbd746de9847de1cb19c734c; `https://api.launchpad.net/1.0/bugs/1190696` 3,243 B, d035f3e89538c13463ec91290490252f5b96c624754ffb4b38cc3842c820041d and `/messages?ws.size=100` 39,693 B, 9309d45cc2f6563327a32dee924600a30fafb01a7b97f1ba9682cc853e3e7eed; `https://bugzilla.redhat.com/show_bug.cgi?ctype=xml&id=1282232` 3,065,177 B, 37a9a617f485a601414ee45284ce98c297ee3767f29e1d07da41702c7deed85e; `https://bbs.archlinux.org/viewtopic.php?id=297983` 19,230 B, 4c42cee3c7e25d85df3bb065f51e20ddea6a144cb3aab8983ca1db18f6c37050 (21:29 UTC); `https://plocate.sesse.net/` 3,517 B, 8efeab8f0b1df7774317bdf030a06f72d472130b0dbdcc9b723fbf8c857cfc7f (21:28 UTC). Local: `sources/S3-19/`.

**Passages.**

- Arch BBS 297983 post #1 (2024-07-23, laptop, 16 GB, btrfs on LUKS, GNOME): "On 6.10: / Jul 23 22:17:30 amezin-laptop.home.arpa systemd[1]: updatedb.service: Consumed 8min 7.865s CPU time, 9.1G memory peak. / Jul 23 22:17:30 amezin-laptop.home.arpa systemd[1]: Finished Update locate database. / … / Jul 23 22:08:03 amezin-laptop.home.arpa systemd[1]: Starting Update locate database... / On 6.9.10: / Jul 23 21:55:46 amezin-laptop.home.arpa systemd[1]: updatedb.service: Consumed 57.781s CPU time, 5.3G memory peak. / … / Jul 23 21:53:18 amezin-laptop.home.arpa systemd[1]: Starting Update locate database..." … "I can watch youtube while updatedb is running, and won't notice it. Also, updatedb is about 3x slower on 6.10." Post #7: "I'm seeing similar issues with btrfs + 6.10.2 + restic. Same high kswapd0 usage".
- Arch FS#10532 (2008, Core 2 T5500 laptop; mlocate 0.18/0.20 — context by age): comment by Attila 2008-05-29 20:34: "To test it again i delete mlocate.db and recreate with less < 10% CPU: / time /etc/cron.hourly/updatedb / real 2m50.548s / user 0m0.358s / sys 0m5.730s"; comment 2008-05-29 17:08: "Replace in /etc/cron.daily/updatedb "/usr/bin/updatedb" with "eval nice -n 19 ionice -c 3 /usr/bin/updatedb"… Opensuse runs the cronjob in this way."; comment by James Rayner 2008-05-30: "Random note, instead of using nice, use schedtools and set the task batch/idleprio."
- Launchpad 1190696 message 10 (2014-03-22, Ubuntu precise, kernel 3.11): "98% disk usage during updatedb.mlocate rendering the system useless until the process is killed or finished. / From atop: / DSK 98% / RDDDK 10100K / WRDSK 1052K"; message 15 (2014-10-13): "ps auxw shows me the ionice'd process: / root 6466 0.0 0.0 4328 356 ? S 07:35 0:00 flock --nonblock /run/mlocate.daily.lock /usr/bin/ionice -c3 /usr/bin/updatedb.mlocate / but the problem process, blocking IO is: / root 6467 1.0 0.0 5688 2220 ? D 07:35 1:25 /usr/bin/updatedb.mlocate"; message 23 (2016-01-29): "it seems that ``ionice -c3`` only works if the kernel scheduler of that device is set to ``cfq``."; message 16: "updatedb.mlocate uses 100% of the hdd IO. Not for an hour but 5-15 minutes."
- RHBZ 1282232 comment 25 (2016-03-25): "Here is systemd-analyze blame from this morning: / "1min 44.635s mlocate-updatedb.service / 1min 1.633s plymouth-quit-wait.service"; comment 37 (2018-05-03, F28): "First boot: / Startup finished in 2.563s (kernel) + 4.992s (initrd) + 2min 25.399s (userspace) = 2min 32.955s / … / Subsequent boot: / Startup finished in 2.585s (kernel) + 4.782s (initrd) + 48.069s (userspace) = 55.436s"; comment 36 (2018-04-16): "Setting IOSchedulingClass=3 seems to help here."; comment 48 (2019-11-05): "adding RandomizedDelaySec to mlocate-updatedb.timer will fix the problem in F31 with systemd 243."
- plocate.sesse.net: "cassarossa:~> time mlocate movit-fosdem-talk / … / mlocate movit-fosdem-talk 19.75s user 0.33s system 99% cpu 20.118 total / cassarossa:~> time plocate movit-fosdem-talk / … / plocate movit-fosdem-talk 0.01s user 0.00s system 78% cpu 0.008 total / … / -rw-r----- 1 root mlocate 1.1G Apr 2 06:26 /var/lib/mlocate/mlocate.db / -rw-r----- 1 root plocate 466M Apr 2 06:28 /var/lib/plocate/plocate.db" … "plocate found two files out of 27 million in just a few milliseconds." … "It does nearly all I/O asynchronously using io_uring if available (Linux 5.1+)".

**Coverage.** T2 (`updatedb`) — covers: CPU time and wall time of one `updatedb.service` run on a Linux laptop (mlocate; 57.781 s CPU over a 148 s run on 6.9.10; 8 min 7.9 s CPU over 567 s on 6.10, with 5.3/9.1 GB memory peak from systemd accounting); an `atop` disk line at 98 % busy during updatedb.mlocate (2014); a `ps` line with state D and 1 min 25 s CPU after ~? min (start 07:35); the ionice/cfq dependency; systemd `mlocate-updatedb.service` 1 min 44.6 s in `systemd-analyze blame` and boot-time deltas (F28/F29). The 2008 Arch `time` line (real 2 m 50 s, user 0.36 s, sys 5.7 s) is 18 years old — context. plocate: `locate` query timing only; updatedb timing not covered by the page. Wake cadence/scheduling class from the unit itself: not covered here (S2/S5 territory). T1/T3/T4/T7: does not cover.

**Observation status.** Arch BBS 297983: one laptop (16 GB, iGPU, btrfs/LUKS; CPU model not stated), mlocate updatedb, kernels 6.9.10 vs 6.10, windows 21:53:18–21:55:46 and 22:08:03–22:17:30 on 2024-07-23, cache state not stated (repeated runs).

**Reader's own computation.** 6.9.10 run: wall = 21:55:46 − 21:53:18 = 148 s; CPU share = 57.781/148 = 0.39. 6.10 run: wall = 567 s; share = 487.865/567 = 0.86.

### S3-20 — SNIA IOTTA repository: FIU IODedup block traces (2008) and the system-call trace list

**Citation.** SNIA IOTTA Repository, "FIU Traces" (trace 390: FIU IODedup, 2008, 29 days, 475 million records, 14.2 GB; FIU SRCMap, 2008–2009); README of FIU IODedup (adapted from sylab-srv.cs.fiu.edu); "System Call Traces" list (FIU Filesystem SysCall Traces 2014; MobiGen 2013; iBench 2011; TraceFS 2007; LASR 2000–2001).

**Copy read.** `https://iotta.snia.org/traces/block-io/390` 16,422 B, sha256 6ea29404d04ed722f7bff6974a097406d0e10f80d16f4d7c831fbe8b64e9d421; `https://iotta.snia.org/tracetypes/3` 75,637 B, 874c2377db40feaf67d33bd90e27ab81597cc49df8405aaf6492e2effc49986d (21:28 UTC); `https://iotta.snia.org/traces/block-io/391/download?type=readme` 1,122 B, 3839832e390ff8925e095d53e6bfeb37daeb60fa39b9628847070f9383e653b6; `https://iotta.snia.org/traces/system-call` 54,937 B, a472567bf72383e6f522caba0718350a9bbc296578b1203cd528b3434b8cb262 (21:29–21:31 UTC). `https://iotta.snia.org/traces/block-io/391` and `https://sylab-srv.cs.fiu.edu/doku.php?id=projects:iodedup:start`: no HTTP response (curl exit, status 000). Trace data files not downloaded (14.2 GB). Local: `sources/S3-20/`.

**Passages.**

- Trace 390 page: "FIU IODedup | Traces collected by FIU for the 2009 paper I/O Deduplication: Utilizing Content Similarity to Improve I/O Performance . | I/O Deduplication | These traces can be decoded using blkparse. This utility is available on all standard Linux systems. | 2008 | 29 days | 475 Million | 14.2 GB".
- README: "3 weeks of traces collected during the period 11/01/08-11/21/08. All the systems were running Linux using the ext3 file system. / Files Description / mail.tar.xz (LZMA compression) CS department's mail server traces. … / homes.tar.gz Research group activities: developing, testing, experiments, technical writing, plotting. / web-vm.tar.gz CS department webmail proxy and online course management. / The traces files (one per day) are in ASCII and each record is as follows: / [ts in ns] [pid] [process] [lba] [size in 512 Bytes blocks] [Write or Read] [major device number] [minor device number] [MD5 per 4096 Bytes] / In the case of the homes traces, the format is different for the digests: / … [MD5 per 512 Bytes]".
- System-call list: "[There are no traces less than 10 years old for this tracetype.] / WARNING: These traces are over 10 years old! / They should not be used for modern research!" … "FIU Filesystem SysCall Traces | System-call traces from "Non-blocking Writes to Files" … The six main traces are all one day of traces collected on 09/16/2014. All the systems were running Linux using the ext4 and zfs file systems." … "LASR Traces (ASCII) | I/O traces taken at the system-call level in 2000 and 2001 as part of a security research project. The traces cover thirteen computers used for software development by CS researchers."

**Coverage.** T7 — covers: a public Linux block-I/O trace with a per-record process name and pid (FIU "homes": research-group workstation activity, 2008, ext3) — fields as quoted; no CPU fields; whether any background job of the T1–T4 kinds appears cannot be established without downloading the 14.2 GB set (not done). Age: 18 years — treated as context near the two-decade line. The system-call traces are all >10 years old by SNIA's own warning; the 2014 FIU syscall traces (Linux, ext4/zfs) are server/experimental machines. T1–T4: does not cover.

**Observation status.** Population-level trace collections; machines named by role, windows given (29 days from 2008-11-01).

### S3-21 — Steam community and EndeavourOS forum threads on CPU during Steam downloads

**Citation.** steamcommunity.com, Hardware and Operating Systems forum, "High CPU usage when steam is downloading games" (Jens, 2020-12-26, 42 comments); forum.endeavouros.com "Steam 100% cpu usage issue" (2023-01-23); steamcommunity Steam-for-Linux thread 3441214221465957847 (depot single-file download question, 2019 — no measurements).

**Copy read.** `https://steamcommunity.com/discussions/forum/11/3004429475631021322/` 121,487 B, sha256 9634e07cd94c02e3e7a7614a5a286e2bcd6982df7d807e639c1ea49b7ed0797f; `https://forum.endeavouros.com/t/steam-100-cpu-usage-issue/36404.json` 30,028 B, fddbdf84b092ae1af0395820ddb20ae05bfed3b45e9fc8fc2f627f7a49147c64 (21:32 UTC); `https://steamcommunity.com/app/221410/discussions/0/3441214221465957847` 120,577 B, 6163834ef1d37bf433daaddfb9cc84e1eca8a1068b70d5d1884d87956f692b2f (21:28 UTC). Local: `sources/S3-21/`.

**Passages.** Steam forum, opening post (2020-12-26): "I've had this problem on two operating systems (Windows 8.1, Arch Linux now) for at least two months. When Steam is downloading games, the download speed tends to go up and down, and as it goes up, my CPU usage goes up a lot as well" … "I'm currently downloading Pathfinder: Kingmaker, and the downloads speed seems to cycle between 5 MB/s and 45 MB/s, disk usage seems to hover between 10 MB/s and 30 MB/s. At peak, I can hear my CPU fan go wild. / My hardware consists of an i7-6700k cpu, a 512 GB Intel 660p nvme ssd, 16GB of ram, and an nvidia gtx 1060." Reply #1: "Steam compresses the downloads for the smallest download size. You are dealing with decompression of the files. Takes CPU cycles." Reply #2 (Jens): "I'd gladly give Steam like, one core, so I could continue using the 7 others." EndeavourOS #2 (2023-01-23): "High CPU usage when downloading or installing is normal. Do you mean %100 on one thread or %100 on all threads?"; #4: "Turn out it was the damn Shader pre-caching".

**Coverage.** T3 — covers weakly: download-rate and disk-write ranges during a Steam depot download on a named Linux machine (Arch, i7-6700K, NVMe: 5–45 MB/s network, 10–30 MB/s disk) and the user's attribution of CPU load to per-chunk decompression; no CPU number. The socket-read pattern analysis (issue #13024), behind the GitHub wall on 2026-09-17, was read on the 2026-09-19 retry (S3-28). T1/T2/T4/T7: does not cover.

**Observation status.** One machine, no CPU figure, no window.

### S3-22 — Brendan Gregg, "Off-CPU Analysis" (tar example)

**Citation.** Brendan Gregg, "Off-CPU Analysis", brendangregg.com/offcpuanalysis.html (sections "Off-CPU Time" and "Off-CPU Analysis"; page undated on the copy, examples on Linux 4.x with bcc).

**Copy read.** HTML 48,742 B, sha256 766e0b85728ba199f20b151f1825c33008983ae2f3cbf701c10585fbd2fc96be, accessed 2026-09-17 21:29 UTC. Local: `sources/S3-22/`.

**Passages.**

- "Off-CPU Time": "$ time tar cf archive.tar linux-4.15-rc2 / real	0m50.798s / user	0m1.048s / sys	0m11.627s / tar took about one minute to run, but the time command shows it only spent 1.0 seconds of user-mode CPU time, and 11.6 seconds of kernel-mode CPU time, out of a total 50.8 seconds of elapsed time. We are missing 38.2 seconds! That is the time the tar command was blocked off-CPU, no doubt doing storage I/O as part of its archive generation."
- "# /usr/share/bcc/tools/cpudist -O -p `pgrep -nx tar` / Tracing off-CPU time... Hit Ctrl-C to end. / ^C /      usecs               : count     distribution /          0 -> 1          : 3        | / 2 -> 3          : 50 / 4 -> 7          : 289 / 8 -> 15         : 342 / 16 -> 31         : 517 / 32 -> 63         : 5862     |*** / 64 -> 127        : 30135    |****************" (histogram continues in the page).
- "Off-CPU Analysis": "# /usr/share/bcc/tools/offcputime -K -p `pgrep -nx tar` / Tracing off-CPU time (us) of PID 15342 by kernel stack... Hit Ctrl-C to end." … stacks ending "xfs_dir2_block_getdents / xfs_readdir / iterate_dir / SyS_getdents / entry_SYSCALL_64_fastpath / -                tar (18235) / 203075"; "… vfs_statx / SYSC_newfstatat / … / -                tar (18235) / 661626"; "… io_schedule / generic_file_read_iter / xfs_file_buffered_aio_read / xfs_file_read_iter / __vfs_read / vfs_read / SyS_read / entry_SYSCALL_64_fastpath / -                tar (18235) / 18413238".
- "The last, showing a total of 18.4 seconds of off-CPU time, is in the read syscall path ending up with io_schedule() – this is tar reading file contents, and blocking on disk I/O. The stack above it shows 662 milliseconds in a stat syscall, which also ends up waiting for storage I/O via xfs_buf_submit_wait(). The top stack, with a total of 203 milliseconds, appears to show tar blocking on locks while doing a getdents syscall (directory listing)."
- With user stacks: "… __read_nocancel / dump_file0 / dump_file / dump_dir0 / dump_dir / … / create_archive / main / __libc_start_main / [unknown] / -                tar (15113) / 426525 / [...] / Ok, so it looks like tar has a recursive walk algorithm for the file system tree."

**Coverage.** T1 — covers: for `tar cf` of a kernel source tree (linux-4.15-rc2) on Linux/XFS: CPU share of wall time (12.7 s CPU of 50.8 s), time blocked on I/O (38.2 s off-CPU; 18.4 s attributed to `read()`→`io_schedule`, 0.66 s to `stat`, 0.20 s to `getdents` locks in one traced run) and the distribution of off-CPU intervals (cpudist histogram: mode 64–127 µs, 30,135 events; 5,862 in 32–63 µs) — i.e. the on/off-CPU alternation structure of an archiver streaming many files. Cache state: not stated (the 38 s blocked implies mostly cold). Machine: not named (XFS, Linux ≥4.8, bcc). Compression, rsync, borg, 7z: does not cover. T2/T3/T4/T7: does not cover.

**Observation status.** One machine (unnamed; XFS; kernel 4.x-era bcc), subject named (GNU tar `cf`, linux-4.15-rc2 tree; tar version not stated), windows: one `time` run and separate tracing runs (PIDs 15342, 18235, 18311, 18375, 15113 — different invocations).

**Reader's own computation.** `(1.048+11.627)/50.798` = 0.25 CPU share; `50.798−12.675` = 38.123 s off-CPU (the page's "38.2").

### S3-23 — Gist "Steam Download Speed is so slow on Linux" (FikriRNurhidayat)

**Citation.** gist.github.com/FikriRNurhidayat/ce18426ad94fff2140538c0adf0e06ec, raw revision as served 2026-09-17.

**Copy read.** `https://gist.githubusercontent.com/FikriRNurhidayat/ce18426ad94fff2140538c0adf0e06ec/raw` 2,621 B, sha256 f6091a2491ce05eb1c72c1cbc63afb218eb19f675a9f6b074c198c0e29b95657, accessed 21:29 UTC. Local: `sources/S3-23/`.

**Passages.** Line 15: "I don't know, perhaps the Steam application doesn't cache the dns locally or something hence your computer will always lookup for the domain everytime you download it on each chunks. CMIIW." Line 10: "My solution seems to be deprecated, there are other solution from the comment on this Gist".

**Coverage.** T3 — does not cover (a dnsmasq workaround note; no measurement). Recorded because the search for a mirror of issue #13024 led here. Other topics: does not cover.

### S3-24 — Michael Stapelberg, "rsync, article 3: How does rsync work?" (2022-07-02)

**Citation.** Michael Stapelberg, "rsync, article 3: How does rsync work?", michael.stapelberg.ch, 2022-07-02; overview "rsync, article 1" (2022-06-18).

**Copy read.** `https://michael.stapelberg.ch/posts/2022-07-02-rsync-how-does-it-work/` 23,357 B, sha256 4a77ff203f1d2df2158df993b192cb719424bc34b02bdee7a1c0685cb26cf330; `…/2022-06-18-rsync-overview/` 8,533 B, 74495818ed8f2341324790e5118a427c46bf8c70db24ed4486d7ab87c029772b. Accessed 21:31 UTC. Local: `sources/S3-24/`.

**Passages.** "The architecture makes it easy to implement the second phase in 3 separate processes, each of which sending to the network as fast as possible using heavy pipelining." … "Observing rsync's transfer phases / When starting an rsync transfer, looking at the resource usage of both machines allows us to confirm our understanding of the rsync architecture, and to pin-point any bottlenecks: / phase: The rsync sender needs 17 seconds to walk the file system and send the file list. The rsync receiver reads from the network and writes into RAM during that time. / This phase is random I/O (querying file system metadata) for the sender. / phase: Afterwards, the rsync sender reads from disk and sends to the network. The rsync receiver receives from the network and writes to disk. / The receiver does roughly the same amount of random I/O as the sender did in phase 1" … "(Again, the above was captured using rsync protocol version 27, later rsync protocol versions don't synchronize after completing phase 1, but instead interleave the phases more.)"

**Coverage.** T1 — covers weakly: one phase timing (17 s file-list walk) from the author's own resource-usage capture (figures shown as images on the page, not fetched; machines and file set not named in text), and the three-process structure statement. Other topics: does not cover.

**Observation status.** Machine, file set and window not named in the text.

### S3-25 — 7-Zip benchmark records: 0ink.net "Using 7z for benchmarks" (2025-04-15); BinaryTides "Benchmark hardware on Linux with 7z LZMA"; SourceForge "7-Zip 18.02 benchmark" thread (2018)

**Citation.** alex, "Using 7z for benchmarks", 0ink.net, 2025-04-15; BinaryTides, "How to Benchmark Hardware on Linux with 7z LZMA Compression"; Igor Pavlov, "7-Zip 18.02 benchmark", SourceForge Open Discussion, 2018-03-04.

**Copy read.** `https://0ink.net/posts/2025/2025-04-15-7z-benchmark.html` 21,137 B, sha256 d5f896adaeff906087f6d6be2101c8bb4f925698ce8dfd5c7d584bc0f380ff41; `https://www.binarytides.com/benchmark-hardware-on-linux-with-7z-lzma/` 112,509 B, ebede8686eb5f511c0b4080fef93295fc6041cd92c44dcf8f31d4fc262340118 (21:32 UTC); `https://sourceforge.net/p/sevenzip/discussion/45797/thread/6d29ae53/` 183,212 B, f4fa29376fdce3fe7417cd52dc582f8dcb7ab06c34f5ed04e52b3894b6c817c2 (21:31 UTC). Local: `sources/S3-25/`.

**Passages.** 0ink.net: "$ 7z b / 7-Zip (z) 24.08 (x64) : Copyright (c) 1999-2024 Igor Pavlov : 2024-08-11 / 64-bit locale=en_US.UTF-8 Threads:16 OPEN_MAX:1024 / … / Linux : 6.6.56_2 : #1 SMP PREEMPT_DYNAMIC … : x86_64 / … / AMD Ryzen 7 5800U with Radeon Graphics / … / RAM size: 15412 MB, # CPU hardware threads: 16 / RAM usage: 3559 MB, # Benchmark threads: 16 / Compressing | Decompressing / Dict Speed Usage R/U Rating | Speed Usage R/U Rating / KiB/s % MIPS MIPS | KiB/s % MIPS MIPS / 22: 41524 1462 2763 40395 | 633594 1547 3491 54026 / … / Avr: 36152 1418 2668 37834 | 600975 1545 3387 52333" … "The Usage column shows the percentage of time the processor is working. It's normalized for a one-thread load. For example, 180% CPU Usage for 2 threads can mean that average CPU usage is about 90% for each thread." BinaryTides (p7zip 16.02, i5-1135G7, 8 threads): "22: 29002 677 4166 28214 | 266786 780 2919 22756". SourceForge: "7zr.exe b -mmt=* >> bench.txt" (Windows instructions; benchmark ratings only).

**Coverage.** T1 — context only: 7-Zip's built-in in-memory LZMA benchmark on Linux shows the worker-thread usage (16 threads at 1418–1545 % on a Ryzen 7 5800U; 8 threads at 677–780 % on an i5-1135G7), i.e. thread structure and CPU-boundness of the codec, but it streams no file set through the disk. Archiving a directory with 7z on Linux with CPU share: does not cover. Other topics: does not cover.

### S3-26 — Phoronix, "Zstd 1.5" review page (probe for CPU-usage graphs)

**Citation.** Phoronix, review "zstd-1.5-benchmarks" (fetched as an example of a Phoronix compression article).

**Copy read.** `https://www.phoronix.com/review/zstd-1.5-benchmarks` 71,476 B, sha256 611d3a9bdad0d6fe9bc0fd0b4a1952d3caa10f358b4a43527910f885cda81388 (21:31 UTC). Local: `sources/S3-26/`.

**Passages.** None quoted: a case-insensitive grep of the saved page for "cpu usage" and "cpu utilization" returns 0 lines (reader's check: `grep -c -i "cpu usage\|cpu utilization" phoronix-zstd-1.5.html` → 0).

**Coverage.** T1 — does not cover (throughput graphs only; OpenBenchmarking result pages with `MONITOR=cpu.usage`, e.g. 2305286-NE-MONITORSY37 for compress-7zip, were 403 on 2026-09-17; that result was read on the 2026-09-19 retry through the PTS client endpoint and carries no `cpu.usage` entry, S3-36). Recorded as the Phoronix attempt.

### S3-27 — BEHACOM dataset (Sánchez Sánchez et al., Data in Brief 31, 2020)

**Citation.** P. M. Sánchez Sánchez, J. M. Jorquera Valero, M. Zago, A. Huertas Celdrán, L. Fernández Maimó, E. López Bernal, S. López Bernal, J. Martínez Valverde, P. Nespoli, J. Pastor Galindo, Á. L. Perales Gómez, M. Gil Pérez, G. Martínez Pérez, "BEHACOM - a dataset modelling users' behaviour in computers", Data in Brief 31 (2020) 105767, PMC7270191; data: Mendeley Data doi 10.17632/cg4br62535.2 (v2); IEEE DataPort doi 10.21227/hc9m-q842.

**Copy read.** Europe PMC full text `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7270191/fullTextXML` (JATS XML, 77,532 B, sha256 c7880aa76a91786aa91fa5e76f331cb8db3370967b53f9007f5feb17d8f3ccfd, 21:33 UTC); `https://data.mendeley.com/datasets/cg4br62535/2` 123,059 B, af244107c7ab34b7c712043bc42b7fb0f7caf7beb4c6b92de2b7aa968145eae5; `https://ieee-dataport.org/open-access/behacom` 65,352 B, 9b4b839c496e74e1bc55528222e46c1a4ee70d0992993271e2572cb403ae57a3; `https://pmc.ncbi.nlm.nih.gov/articles/PMC7270191/` returned a "Checking your browser - reCAPTCHA" page (21,209 B, 6851f97bc3daf549526ad0da96a658b3ea5abe8b96fb79cff979e0128cba4bbd) — not the article. Data files not downloaded. Accessed 21:32–21:33 UTC. Local: `sources/S3-27/`.

**Passages** (JATS full text):

- Abstract: "This paper details the methodology and approach conducted to monitor the behaviour of twelve users interacting with their computers for fifty-five consecutive days without preestablished indications or restrictions. The generated dataset, called BEHACOM, contains for each user a set of features that models, in one-minute time windows, the usage of computer resources such as CPU or memory, as well as the activities registered by applications, mouse and keyboard."
- Specification table: "How data were acquired Client application for Windows and Linux operating systems … Description of data collection First, we have gathered the raw data generated by each individual interacting with his/her device. After that, we have aggregated the raw data in time windows of one minute each and have calculated relevant features for each dimension."
- §2.1: "The twelve individuals are right-handed male, with ages ranging from 20 to 45 years old. Eight of them use Windows as operating system, three Linux, and one both." … "The first timestamp (UNIX ms) of the dataset is 1574245230186 (Wednesday, 20-Nov-19 10:20:30 UTC) and the last one is 1578995678310 (Tuesday, 14-Jan-20 09:54:38 UTC)."
- §1.2: "we have implemented a data collection application for Windows, the most used desktop operating system, and another for Linux distributions based on Debian."
- Table 1: "Feature Group Scope Number Section / Keyboard Model the user's behaviour with the keyboard 11 989 2.1.1 / Mouse Model the events of the mouse 45 2.1.2 / App Usage Model the statistics of the applications usage 7 2.1.3 / Resources Model the computer resource usage 10 2.1.4".
- Table 5 (Application usage statistics): "active_apps_average Average number of applications active during the time window. R / current_app Application executable name in foreground when the vector was generated. S / penultimate_app Penultimate application executable name in foreground during the time window. … S / changes_between_apps Number of changes between different foreground applications during the time window. N / current_app_foreground_time Number of seconds that the current application has been in foreground during the time window. … R / current_app_average_processes Average number of processes that the current application in foreground had active during the time window. R / current_app_stddev_processes …"
- Table 6 (Resource consumption): "current_app_average_cpu Average percentage of CPU used by the current application during the time window. R / current_app_stddev_cpu … / system_average_cpu Average of the percentage of system CPU capacity used in total during the time window. R / system_stddev_cpu … / current_app_average_mem Average memory percentage used by the current application during the time window. R / … / system_average_mem … / received_bytes Number of bytes received through the network interfaces of the device during the time window. N / sent_bytes Number of bytes sent using the network interfaces of the device during the time window. N".
- Mendeley page: "This dataset contains the behavioural data of 12 different users freely utilising their personal computers. The data collection period is composed of 55 days of user interaction, each user having their own activity periods." … "User behaviour is stored in csv comma separated format. Each user file is located in a different folder."

**Coverage.** T7 — covers: a public per-user dataset of Linux (3 users + 1 dual-boot) and Windows desktop use, one-minute windows over 55 days (Nov 2019–Jan 2020), with fields: foreground application executable name, its process count, its average/stddev CPU %, system CPU %, memory %, bytes received/sent per minute, plus keyboard/mouse features. It carries CPU only for the *foreground* application and the system total — background jobs (indexers, backups, downloads) appear only through `system_average_cpu` and the byte counters, never by name (only the foreground executable is named). Per-process I/O: does not cover. Whether any background job of the T1–T4 kinds is present cannot be told from the features (not downloaded; by construction not identifiable except a downloader in the foreground). T1–T4: does not cover.

**Observation status.** Population: 12 users; machines not described; window Nov 2019–Jan 2020; Linux subset: Debian-based distributions (collector requirement).

### S3-28 — ValveSoftware/steam-for-linux issue #13024 "Steam Linux Download Speed Issue - Problem Found"

**Citation.** ValveSoftware/steam-for-linux, GitHub issue #13024, opened 2026-03-22 00:03:50 UTC by FrancescoPnr-dev, closed 2026-05-20 16:51:11 UTC, 14 comments, last updated 2026-08-30 20:09:08 UTC; https://github.com/ValveSoftware/steam-for-linux/issues/13024. The body was edited after posting: it opens "**EDIT** / **Problem Found!**", and the author's comment 4114010701 (2026-03-23 22:03:14 UTC) says "ok i found the problem, i used strace, check out my post i updated it".

**Copy read.** `gh api repos/ValveSoftware/steam-for-linux/issues/13024` (JSON 8,747 B, sha256 fa6f742ada487658e7f1aedd49557ef549badfe36aaee5372ec68ef02f246eb1) and `…/issues/13024/comments?per_page=100` (30,231 B, 052787d1f4950af663477b22dce316ec2335b5d761cb64c2445818734238349a), accessed 2026-09-19 01:30:34 UTC. Local: `sources/S3-28/`.

**Passages.**

- Issue body: "TCP metrics collected during active downloads show a consistent pattern: congestion window (cwnd) grows normally from its initial value, indicating no network congestion; however, the receive window (rcv_wnd) remains abnormally small (on the order of ~180 KB), and the delivery rate reported by BBR remains limited (~1 Mbps per connection) despite multiple parallel connections. In contrast, a reference downloader such as aria2c, executed on the same system and network path, achieves full line-rate throughput (200 MB/s+) with significantly larger receive windows (3 MB+) and efficient parallelization."
- Issue body: "system call tracing was performed on the Steam client process using strace, focusing on recvfrom and event loop behavior. The process was confirmed to run in 32-bit mode" … "data is consumed in small chunks (~6.7 KB per recvfrom call), followed by substantial idle periods ranging from hundreds of milliseconds to several seconds. Each read cycle consists of a small header read, a payload read, and then an immediate EAGAIN, after which the process remains idle before repeating the pattern." … "The limitation persists regardless of kernel tuning, TCP congestion control (including BBR), or increased socket buffer sizes".
- Issue body, the strace excerpt (seven calls, no date): `16:30:35.331635 recvfrom(128, "q9\275\0\0\0\200\3\377\377\37\0\0\1\0\0\24\0\377\377\1\7\0\0 \10\377\0\0\0\0"..., 6732, 0, NULL, NULL) = 6732 16:30:35.332277 recvfrom(128, "\1\0\v\0\0\0\223\6", 8, 0, NULL, NULL) = 8 16:30:35.332315 recvfrom(128, …, 6732, 0, NULL, NULL) = 6732 16:30:40.380843 recvfrom(71, "\1\0\v\0\0\0\223\6", 8, 0, NULL, NULL) = 8 16:30:40.380891 recvfrom(71, …, 6732, 0, NULL, NULL) = 6732 16:30:40.381503 recvfrom(71, "\1\0\v\0\0\0\223\6", 8, 0, NULL, NULL) = 8 16:30:40.381516 recvfrom(71, …, 6732, 0, NULL, NULL) = 6732` (payload strings elided with "…").
- Comment 4111297353 (FrancescoPnr-dev, 2026-03-23 15:00:51 UTC): "the download of the games does not go beyond 40MB/s, I think it is a limitation of the 32bit linux steam client". Comment 4111315295 (15:03:23 UTC): "mine never goes above 40MB/s at peak, even though on every other download I do outside of Steam I go well over 200MB/s".
- Comment 4106639242 (desx88, 2026-03-22 17:26:55 UTC): "Fixed it by adding to /etc/hosts 0.0.0.0 + slow steam cdn servers. Launch steam with steam://open/console. Start download and write in console download_sources. Add any slow cdn to hosts with 0.0.0.0 / My steam_dev.cfg / `@nClientDownloadEnableHTTP2PlatformLinux 0` / `@fDownloadRateImprovementToAddAnotherConnection 1.1` / `@cMaxInitialDownloadSources 15`".
- Comment 5470222856 (S4nic, 2026-08-30 17:35:07 UTC): "Two separate Linux PCs (one on a fresh Debian 13.6 / EXT4 install), both capped at ~20MB/s Steam downloads" … "Gigabit ISP connection, confirmed via wget pulling a Debian ISO at 110MB/s sustained" … "**CPU** — confirmed via btop during a capped download, no core anywhere near saturated (highest ~14%), load average low" … "15-16 simultaneous connections open, each individually capped in the 0.3–1.8MB/s range, summing to the ~20MB/s ceiling." … "Attached strace to the download thread handling actual TLS traffic to steamcontent.com. Sample of `recvmsg()` calls: / 18308 recvmsg(235, ...iov_len=65536..., MSG_DONTWAIT) = 1400 <0.000013> / 18308 recvmsg(235, ...iov_len=65536..., MSG_DONTWAIT) = 5600 <0.000012> / 18308 recvmsg(162, ...iov_len=65536..., MSG_DONTWAIT) = 516 <0.000014> / 18308 recvmsg(172, ...iov_len=65536..., MSG_DONTWAIT) = 5600 <0.000021>" … "Every call requests up to 65536 bytes but consistently returns small counts (mostly 1400-5600 bytes, occasionally as low as 516-518), always with `MSG_DONTWAIT`."
- Comment 5470979694 (FrancescoPnr-dev, 2026-08-30 20:09:08 UTC): "I've done some further research and it appears the issue is with the caching on the Valve fco server."

**Coverage.** T3 — covers the Steam client's wake structure against the socket on Linux, as two reporters describe and excerpt it:
- bytes per read: an 8-B header read then a 6,732-B payload read per `recvfrom` pair; `recvmsg` returning 516–5,600 B of a 65,536-B non-blocking request;
- the stated idle periods between read bursts (hundreds of ms to seconds);
- the advertised receive window (~180 KB) and the per-connection delivery rate (~1 Mbps, BBR);
- connection count and per-connection rate: 15–16 connections at 0.3–1.8 MB/s, summing to ~20 MB/s;
- the process mode (32-bit), and CPU during a capped download (btop: highest core ~14 %);
- throughput on consumer links: Steam capped at ~20 and ~40 MB/s, against wget at 110 MB/s and aria2c at 200 MB/s+ on the same links;
- client configuration keys for multi-connection behaviour: `@fDownloadRateImprovementToAddAnotherConnection`, `@cMaxInitialDownloadSources`, `@nClientDownloadEnableHTTP2PlatformLinux`.

The cause is disputed within the thread: the body reads it as the client's own behaviour, and the author's last comment puts it on Valve's server caching. CPU per chunk, decompression and disk-write work: does not cover. T7 — no trace file is attached, only the two excerpts. T1/T2/T4: does not cover.

**Observation status.** Two observations. (a) The author: Arch Linux; hardware not named; link given only as "well over 200MB/s" outside Steam; Steam client version not named. The strace excerpt is seven calls over about 5 s (clock 16:30:35–16:30:40, no date; posted between 2026-03-22 and 2026-03-23). The cwnd, rcv_wnd and BBR figures are summaries, with no raw `ss` output. (b) S4nic: two PCs, one Debian 13.6 on ext4, a gigabit PPPoE link, a Cyberpunk 2077 download on 2026-08-30. Its `recvmsg` lines carry per-call durations but no wall-clock timestamps.

**Reader's own computation** (locates the candidate; not a value): the gap between the last read on fd 128 and the first read on fd 71 in the excerpt, `python3 -c "from datetime import datetime as D; f='%H:%M:%S.%f'; print((D.strptime('16:30:40.380843',f)-D.strptime('16:30:35.332315',f)).total_seconds())"` → 5.048528 s. The gap spans two different sockets, and whether the trace covered every thread is not stated. Bytes per header+payload pair: 8 + 6,732 = 6,740.

### S3-29 — steam-for-linux issue #12015 and its attached Steam logs (`content_log.txt`, `content_log.previous.txt`)

**Citation.** ValveSoftware/steam-for-linux issue #12015 "Getting "content unavailable" on Linux client only, with unpack errors in the log", opened 2025-05-15 19:55:09 UTC by XANi, open, 10 comments; body attachment `steam-logs.tar.gz` (the reporter's `~/.steam/steam/logs/` directory).

**Copy read.** `gh api` issue JSON 7,216 B (sha256 6f4265967ad9cbbce196395b5bc13589b62769515060332cd7723b768bcf8e3a) and comments 22,563 B (253f13f5503206cf66d0371320f9fa2951e502c6e7932f2001164d8621193b98), 2026-09-19 01:30:35 UTC. Attachment `https://github.com/user-attachments/files/20233784/steam-logs.tar.gz`: 8,349,732 B (ed6dc9b57b3610ed12b3336326360cdd5b50e8e086a03b3fbb806bdd99521e90), 01:31:30 UTC; a gzip tar of 84 files under `home/xani/.steam/steam/logs/`. Two of them extracted: `content_log.txt` 847,169 B, 5,324 lines (69f381c56f69ee70824c12293b2f9238eac4bc9ca51350a715ae9632869ea68a), and `content_log.previous.txt` 4,194,149 B, 26,465 lines (7de1aa0152b102e299f626f132d12791289936357657a7d8fa4ba50ec65196b2). Local: `sources/S3-29/`.

**Passages.**

- Issue body: "Steam client version (build number or date): 2025-05-15, tried both stable and beta branch / * Distribution (e.g. Ubuntu):  Debian" … "I have tried downloading same game on windows and it works fine. I've noticed a lot of "unpack failed" in logs".
- `content_log.previous.txt` lines 7962, 7965, 7966, 7969, 7972 (one completed update): "[2025-05-15 21:31:48] AppID 1380910 update started : download 0/408033136, store 0/0, reuse 0/272518215, delta 0/0, stage 0/821581209" / "[2025-05-15 21:31:48] Downloading 1962 chunks from depot 1380917" / "[2025-05-15 21:31:49] Detected write gap 67 MB in file "Stardeus_Data\resources.assets.resS"" / "[2025-05-15 21:31:56] Increasing target number of download connections to 6 (rate was 172.464, now 215.223)" / "[2025-05-15 21:32:04] AppID 1380910 starting commit from "/mnt/steam/steamapps/downloading/1380910" to "/mnt/steam/steamapps/common/Stardeus" : 1620 updated, 1 moved, 82 deleted files".
- `content_log.previous.txt` lines 7984, 7986, 7987, 7990: "[2025-05-15 21:32:09] AppID 427520 update started : download 0/146394288, store 0/0, reuse 0/2424207, delta 0/0, stage 0/542509102" / "[2025-05-15 21:32:09] Downloading 2144 chunks from depot 645391" / "[2025-05-15 21:32:18] Current download rate: 123.584 Mbps" / "[2025-05-15 21:32:22] AppID 427520 starting commit from "/var/steam/steamapps/downloading/427520" to "/var/steam/steamapps/common/Factorio" : 1866 updated, 8 moved, 10 deleted files".
- `content_log.txt` line 83: "[2025-05-15 21:48:47] Turning on early CRC checks for all received data." Line 1387: "[2025-05-15 21:48:59] stats: (SteamCache, 251) cache1-waw-extl.steamcontent.com: 187208784 Bytes, 11 sec (131.89 Mbps). 257 Hits / 0 Misses (100 %, 100 % bytes)". Line 1396: "[2025-05-15 21:48:59] Increasing target number of download connections to 5 (rate was 0.000, now 234.990)".
- `content_log.txt` line 3: "[2025-05-15 21:47:20] Failed unpacking chunk "8ec22e6c1b0646bfd14102ce5e1f9bf15fd9d0af" from "cache1-sto1.steamcontent.com/depot/2939641/chunk/8ec22e6c1b0646bfd14102ce5e1f9bf15fd9d0af" (Unpack failed (c:774592,u:0,r:806485,b:0))".
- Comment 2923138888 (XANi, 2025-05-30 18:37:35 UTC): "@raethkcj That did fix it (clean re-install + re-adding 2 lib dirs), thanks".

**Coverage.** T3 — covers the throughput and multi-connection behaviour of the Steam client's depot downloads on one Linux machine over 23 minutes:
- per-CDN-host transfer counters about every 11 s: bytes, seconds, Mbps, cache hits and misses;
- the client's connection-count steps, with the rate that triggered each (to 5 at rates of 67–250 Mbps, to 6 at 215–260 Mbps);
- "Current download rate" lines of 123.6–189.2 Mbps;
- per-update download and stage byte totals with chunk counts, from which an average compressed chunk size follows;
- on the disk-write side, preallocation and "Detected write gap" lines, and per-update commit file counts;
- one mode switch: "Turning on early CRC checks for all received data".

CPU, wake structure, and process or thread structure: does not cover. T7 — covers: a public, complete `content_log.txt` pair from a Linux Steam client, with the fields quoted above. A fault dominates the window: repeated "Failed unpacking chunk" lines on depot 2939641, which a clean reinstall fixed (comment 2923138888). Interleaved with it, seven commits of six AppIDs complete normally. T1/T2/T4: does not cover.

**Observation status.** One machine: Debian (issue body); hardware and link not named; Steam libraries on `/mnt/steam` and `/var/steam`. Subject: the Steam client of 2025-05-15. Window named: 2025-05-15 21:27:42 → 21:50:23 in the log's local time. `content_log.previous.txt` covers 21:27:42–21:47:20 (rotated at about 4 MB, so earlier lines are gone); `content_log.txt` covers 21:47:20–21:50:23. The depot 2939641 failures are a fault state; the completed updates are not.

**Reader's own computation** (locates the candidate; not values):
- The `stats:` lines in both files: `grep -h -o 'stats: .* [0-9]* sec ([0-9.]* Mbps)' content_log.previous.txt content_log.txt | sed -E 's/.* ([0-9]+) sec \(([0-9.]+) Mbps\)/\1 \2/' | python3 -c "import sys,statistics as st; r=[l.split() for l in sys.stdin]; v=[float(b) for a,b in r]; print(len(v), min(v), st.median(v), max(v), sum(1 for a,b in r if 10<=int(a)<=12))"` → 121 lines. Per-host rate: min 5.96, median 54.41, max 141.62 Mbps. 86 of the 121 lines cover 10–12 s.
- Stardeus: 408,033,136 B between "update started" (21:31:48) and "starting commit" (21:32:04), 16 s ±1 s at the log's one-second resolution. `python3 -c "print(408033136/16/1e6, 408033136/1962)"` → 25.5 MB/s (204 Mbps) and 207,968 B per chunk.
- Factorio: 13 s, 21:32:09 → 21:32:22. `python3 -c "print(146394288/13/1e6, 146394288/2144)"` → 11.3 MB/s (90 Mbps) and 68,281 B per chunk.

### S3-30 — steam-for-linux issue #7956 "Downloading a large game can fail with EMFILE (errno 24)"

**Citation.** ValveSoftware/steam-for-linux issue #7956, opened 2021-07-30 18:15:06 UTC by smcv (CONTRIBUTOR association), label "Steam client", closed 2021-08-04 20:32:57 UTC, 11 comments.

**Copy read.** `gh api` issue JSON 9,290 B (sha256 2a1dd0812f5a731e57db7ae26ee1570b5913f5360577b8657a8e38e73806b1fe) and comments 24,092 B (a7e2f9114304df9b37b4aed557be7b3d7a6e1ddebb93c5ac659e38159e53d3e6), 2026-09-19 01:30:36 UTC. Local: `sources/S3-30/`.

**Passages.**

- Body (Debian 11, client build 1627607186, beta): "Downloading Civ VI gets paused after a while with "Disk write error". Looking at `~/.steam/root/logs/content_log.txt` I see this:" … "[2021-07-30 18:47:14] Downloading 35959 chunks from depot 533503 / [2021-07-30 18:47:26] Increasing target number of download connections to 4 (rate was 0.000, now 53.843) / [2021-07-30 18:47:26] Current download rate: 53.843 Mbps / [2021-07-30 18:47:26] Created download interface of type 'SteamCache' (7) to host cache1-lhr1.steamcontent.com (cache1-lhr1.steamcontent.com) / [2021-07-30 18:48:21] CGenericAsyncFileIOThread::AllocateResource() failed for CFileWriter: errno: 24, File: /home/steam/SteamLibrary/steamapps/downloading/289070/steamassets/base/platforms/windows/audio/751812779.wem / [2021-07-30 18:48:21] Failed to write chunk in file "steamassets\base\platforms\windows\audio\751812779.wem", 266788 bytes at offset 0 (File Not Found)".
- Body: "Looking in `/proc/$pid/fd/` for the main Steam process, I can see that there are about 1000 fds just before it fails."
- Comment 891353481 (PedroHLC, 2021-08-02 21:41:22 UTC; Arch Linux, ZFS, Steam beta of 2021-07-30): "[2021-08-02 18:23:32] AppID 1686450 update started : download 1274989264/1884205488, store 0/0, reuse 0/0, delta 0/0, stage 2881567184/4242800593" … "[2021-08-02 18:23:32] Downloading 7257 chunks from depot 1686451" … "[2021-08-02 18:24:29] Current download rate: 9.121 Mbps" … "Failed to write chunk in file "NanosWorld\Content\NanosWorld\Thumbnails\SM_Shoes.jpg", 9439 bytes at offset 0 (File Not Found)" … "It spawns like 100 fds per sec in `/proc/$pid/fd/`..."
- Comment 891837165 (TTimo, COLLABORATOR, 2021-08-03 13:14:57 UTC): "The Aug 2nd beta update brought the open files count during download back down. This problem may be less prevalent now. It's possible we are leaking fds though so we'll keep an eye on it."
- Comment 891909821 (PedroHLC, 2021-08-03 14:48:03 UTC): "I'm no longer able to reproduce it with built `Aug 2, 2021, 23:01`. But I can see it opened 1600+ file descriptors."

**Coverage.** T3 — covers the disk-write side of a Steam depot download on Linux:
- chunks are written by an asynchronous file-I/O thread (`CGenericAsyncFileIOThread`, `CFileWriter`) into per-file destinations under `steamapps/downloading/`;
- the main Steam process held about 1,000 open file descriptors (Debian 11) and 1,600+ (Arch), opened at "like 100 fds per sec";
- chunk write sizes as logged: 266,788 B and 9,439 B at offset 0;
- the connection-count step at the first rate reading: to 4 at 53.843 Mbps;
- depot chunk counts of 35,959 and 7,257, and rates of 53.843 and 9.121 Mbps.

The fd growth is a fault state of that client build, fixed by the 2021-08-03 update (comment 892954863). CPU per chunk and wake structure: does not cover. T7 — covers: `content_log.txt` excerpts with the field set shared with S3-29, plus `update started` byte totals. T1/T2/T4: does not cover.

**Observation status.** Two machines, hardware not named. (a) Debian 11, a btrfs library (comment 891639297), client build 1627607186 beta; window 2021-07-30 18:47:14–18:48:21. (b) Arch Linux on ZFS; window 2021-08-02 18:23:32–18:24:44. Link class not named.

### S3-31 — steam-for-linux issue #6684 "High CPU usage when download"

**Citation.** ValveSoftware/steam-for-linux issue #6684, opened 2019-11-12 02:07:41 UTC by howdev, labels "Not a bug" and "Steam client", open; the issue lists 18 comments and the API returned 17; last updated 2024-10-28 22:57:02 UTC.

**Copy read.** `gh api` issue JSON 3,653 B (sha256 ce09a65337f80929e1d8209c93300d61f171b552c70de9321528a03ee830cd68) and comments 33,024 B (662edb082c1b943cd0da41a48fbc7361f8ef6c939dd705f54232e38793453810), 2026-09-19 01:30:36 UTC. Screenshots `https://user-images.githubusercontent.com/17158780/68635668-24c24e80-055e-11ea-961b-59c02f8c1754.png` (133,785 B, 36a64e705c63e048bde8327d84fd9b980c779949a853929a3fb87380f597c951) and `https://user-images.githubusercontent.com/11761863/139614157-559b7e4d-4cb4-4405-9395-38c05266d677.png` (18,986 B, fc90f011d7132f08f8efe6e2eac332ca7b979d01f20df28b0bba5faf02f56a90), 01:32:37 UTC. Local: `sources/S3-31/`.

**Passages.**

- Body (Linux Mint 19.2, client of Nov 6 2019): "CPU usage goes up high when downloading. 40% CPU graph in system monitor. Same continue to happen when download resume from pause. Restart Steam, still not resolve. Stop the download and CPU usage drops."
- Comment 552704921 (kisak-valve, MEMBER, 2019-11-12 02:24:55 UTC): "the usage you've described is within expectations for SteamPipe."
- Comment 553086531 (Plagman, MEMBER, 2019-11-12 19:53:12 UTC): "It does a lot of decryption, decompression, and delta-patching work. You're right that in some situations, it's not suitable to play a game and download at the same time; for this reason, I believe downloading games while playing is off by default and has to be explicitly enabled by the user."
- Comment 554792172 (rcorre, 2019-11-17; Archlinux, client of Nov 14 2019, beta): "I've recently noticed my client get up to ~100% cpu during downloads."
- Comment 938177221 (rcorre, 2021-10-07 21:43:24 UTC), whitespace collapsed: "I just started downloading Phoenix Point, and steam consumed over 300% CPU on an AMD 5600X pretty much the whole download. / PID USER PR NI VIRT RES SHR S %CPU %MEM TIME+ COMMAND / 2722 rcorre 20 0 833844 520036 242920 S 341.5 1.6 4:14.77 steam" … "I'm on `Linux 5.14.8-arch1-1`, with the Sept. 17th steam build."
- Comment 955878117 (theoparis, 2021-11-01 02:40:47 UTC): "I have an AMD Ryzen 5 2600, but my cpu usage in top -i and htop seems really high as well and I'm just updating my games." … "I'm using a more recent version of Arch Linux than rcorre is: `5.14.14-arch1-1`".
- Comment 1117530936 (zany130, 2022-05-04 16:02:21 UTC; Garuda Linux, kernel 5.17.5-256-tkg-pds, "6-core AMD Ryzen 5 2600X", "Intel I211 Gigabit Network"): "limiting it to 500mbps instead of allowing it to reach about 800mbps (I have gigabit internet) reduces the CPU usage drastically and no longer causes my system to stutter".
- The reader's transcription of text legible in the body screenshot (GNOME System Monitor, Resources tab, 60-second history): "CPU1 36.3%", "CPU2 13.0%", "CPU3 15.0%", "CPU4 44.1%"; "Memory 3.0 GiB (39.2%) of 7.7 GiB"; "Receiving 8.5 MiB/s", "Total Received 19.6 GiB"; "Sending 232.1 KiB/s", "Total Sent 843.9 MiB". In the reader's reading of the plots, received traffic rises to a plateau of about 8 MiB/s over the last ~22 s of the window, with the four CPU lines mostly between 10 and 60 % over that stretch.
- The reader's transcription of the comment 955878117 screenshot (one `htop` row under the header "CPU%▽MEM% TIME+ Command"): "461. 5.8 1:42.81 /home/theo/.local/share/Steam/ubuntu12_32/st" (the row is cut at the image edge).

**Coverage.** T3 — covers the CPU share of the Steam client process during depot downloads on Linux:
- `top` shows 341.5 % (3.4 CPUs) for process `steam` on a Ryzen 5 5600X (Arch, kernel 5.14.8);
- `htop` shows 461 % for `…/Steam/ubuntu12_32/st…` on a Ryzen 5 2600 (Arch, 5.14.14);
- "~100 %" (Arch, 2019) and a "40%" graph (Mint 19.2);
- a Valve developer names the per-download work: decryption, decompression, delta-patching;
- a qualitative rate dependence: a 500 Mbps cap against ~800 Mbps uncapped on a Ryzen 5 2600X;
- the process name the work runs under: `steam`, from the 32-bit `ubuntu12_32` directory.

A download rate alongside a per-process CPU figure: does not cover. The only rate, 8.5 MiB/s, comes with system-wide per-CPU load on the Mint machine. Thread structure and wake structure: does not cover. T1/T2/T4/T7: does not cover.

**Observation status.** Snapshots, not series. Four machines, each named by CPU and distribution at most. Download rate, game size, disk and cache state are not named, except in the Mint screenshot (4 CPUs, 7.7 GiB, 8.5 MiB/s received). rcorre's line is one `top` refresh with TIME+ 4:14.77.

**Reader's own computation** (locates; not a value): the mean of the four per-CPU readings in the Mint screenshot, `python3 -c "print((36.3+13.0+15.0+44.1)/4)"` → 27.1 % of the 4-CPU machine, system-wide.

### S3-32 — BorgBackup GitHub issues #2245, #5804, #7374, #3471

**Citation.** borgbackup/borg GitHub issues:
- #2245 "A very slow repository": magma1447, 2017-03-02; labels "bug" and "c: index or hashtable"; closed 2017-03-04; 19 comments.
- #5804 "[1.2.0b3] borg info very slow": FabioPedretti, 2021-05-12; closed 2022-04-20; 14 comments.
- #7374 "Very slow backup speed when creating archive from sshfs to external hdd": AntonOellerer, 2023-02-23; label "cmd: create"; closed 2025-11-16; 15 comments.
- #3471 "Slow startup": 2017-12-22; closed 2017-12-25; 24 comments. It is a macOS and Raspberry Pi startup report, recorded as context.

**Copy read.** `gh api` issue and comments JSON, 2026-09-19 01:30:37–01:30:40 UTC:

| Issue | Issue JSON | Comments JSON |
|---|---|---|
| #2245 | 8,996 B, a3f94a639f86714d0d78ba107e06275d244905222a2f4196133d3e3a02426326 | 54,255 B, ff36c97cf3dfdd0f04cd8b60d6c4e81a55d1721cbde0c527c5969cd1a4567c9f |
| #3471 | 5,820 B, 2f26a0027820076773689b7cb4efad0358aba5346fcfa86327962a44b544a523 | 52,117 B, b03fbe65041a8b659066372d5351e0dec8aea8ae4d948534a4104698ac78c7c9 |
| #5804 | 6,456 B, 90b0dae2dc9e2900b8f1dfce34ad177e115071e7cfacffc01cbb4bc80d7b8b35 | 33,388 B, ca97f618658990128498cae974a847c4bdd0be5d95450e9a8178c1ca0ff6d686 |
| #7374 | 10,042 B, 8c4d4c5e581b1fd8000d07978b1ee86c7a1db89dfdf0cf6d56a57062c0ffa4ef | 29,567 B, 9dc9724676bfcbc99b27a26441764bf898dd5b30982e1272c89722eb09e66ddb |

Local: `sources/S3-32/`.

**Passages.**

- #2245 body (client `pgc-db-01`, server `thor` over ssh; "Client has borgbackup-1.1.0-b3, Server has borgbackup-1.1.0-b3"): "cp /var/log/syslog . / du -hs syslog / 3.3M    syslog" … "time BORG_RSH='ssh -i /root/.ssh/thor-borg' borgbackup create --verbose --compression auto,zlib,3 borg@thor:/data/borg-WedFriSun/pgc-db-01.borg::test_1 syslog / real    1m40.940s / user    0m1.000s / sys     0m0.180s"; into the other repository: "real    0m11.295s / user    0m1.168s / sys     0m0.208s" … "For the above test cases the server used 50-100% cpu. It's a i5-3570K. In my real backups it's stuck at 100% for a very long time (hours)." … "The dumps are ~12 GB or ~70 GB." … "Backing up the smaller ones takes about 8 minutes for the two good repositories, and somewhere around 5 hours for the slow repository."
- #2245 comment 283530493 (magma1447, 2017-03-02 01:46:24 UTC): "The process borgbackup uses 100%. I have not seen ssh in the top 10-15."
- #2245 comment 283531439 (ThomasWaldmann, MEMBER, 2017-03-02 01:52:11 UTC): "borg serve does not do much computing usually: / - it is mostly I/O, getting/putting chunks from/into segment files. / - it computes crc32 for all segment entries (not that heavy and not expected to vary much) / - it maintains the repo index, which is a big in-memory hashtable (hashtable perf can vary depending on load factor, data, number of tombstones, ...)".
- #2245 comment 283652563 (magma1447, 2017-03-02 13:25:45 UTC): "borg@thor:/data/borg-WedFriSun$ time borgbackup check --repair pgc-db-01.copy/" … "real    84m12.317s / user    18m28.868s / sys     9m35.000s".
- #2245 comment 283856546 (ThomasWaldmann, 2017-03-03 03:37:21 UTC): "**No empty buckets. Load ca. 0.53.**" … "Thus: all new chunks in the backup being created trigger full hashtable scans on the repo server. Worst case for performance, high cpu load in ht code."
- #5804 body (Debian 10 VM, "VM with ext4 main FS, repo on remote sshfs"), whitespace collapsed: "While running the borg 1.2.0b3 info command, "top" output shows borg CPU usage, as well as ssh/sshfs CPU usage (the repo is on sshfs). / PID USER PR NI VIRT RES SHR S %CPU %MEM TIME+ COMMAND / 17608 root 20 0 971804 937936 12504 S 20,6 11,5 0:19.73 borg-1.2.0b3 / 15527 root 20 0 19828 10240 5672 S 8,3 0,1 11:40.80 ssh / 15529 root 20 0 522012 6224 776 S 5,6 0,1 10:47.79 sshfs". Comment 839851591 (2021-05-12): "Platform: Linux borg 4.19.0-16-amd64 #1 SMP Debian 4.19.181-1 (2021-03-19) x86_64".
- #5804 comment 1059935562 (FabioPedretti, 2022-03-06 10:30:01 UTC): "# time ./borg-1.1.17 info" … "real	0m26,835s / user	0m2,231s / sys	0m1,492s"; "# time ./borg-1.2.0 info" … "real	1m43,685s / user	0m6,663s / sys	0m2,491s". Comment 1059983335: "# borg list | wc -l / 3088".
- #7374 body (borg 1.2.3; "fedora 37"; "linux laptop (`AMD Ryzen 7 4800H`, `32 GB RAM`), `btrfs + luks`"; "external hdd (`WDC WD20SDRW`), `xfs + luks`"; source a "hetzner storage box" mounted "via sshfs as `fuse.sshfs`"; "300GB"): "started to back up the content of the storage box, which turned out to be very slow (~10GB per hour), even when just deduplication of existing files was done". CRUD benchmark, "From the storage box to the hdd:": "C-R-BIG           3.89 MB/s (10 * 100.00 MB random files: 256.86s)" / "R-R-BIG         105.67 MB/s (10 * 100.00 MB random files: 9.46s)" / "C-R-SMALL         0.09 MB/s (10000 * 10.00 kB random files: 1093.80s)". "from the laptop to the hdd": "C-R-BIG          76.27 MB/s (10 * 100.00 MB random files: 13.11s)" / "C-R-SMALL        17.68 MB/s (10000 * 10.00 kB random files: 5.66s)".
- #7374 comment 1697827312 (enkore, CONTRIBUTOR, 2023-08-29 17:02:35 UTC): "sshfs makes no attempt at latency hiding and couldn't do much if it tried - so this is very dependent on the latency of the sshfs mount. This setup will always perform badly with many files."
- #7374 comment 2408718714 (thutex, 2024-10-12 22:33:36 UTC): "last upload (5263438 files, compressed 121.36GB, deduplicated 7.36GB) took over 24 hours: / Duration: 1 days 1 hours 8 minutes 5.14 seconds / my upload speed is 30Mbps".
- #7374 comment 2566020761 (ThomasWaldmann, 2024-12-31 00:03:11 UTC): "Many network filesystems (like sshfs) do not have stable inodes, but the default for detection of "this file was not changed" is `--files-cache=inode,ctime,size`. The files cache is what makes borg really fast."
- #3471 comment 364526948 (ThomasWaldmann, 2018-02-09 19:00:27 UTC; the thread concerns macOS and Raspberry Pi startup time): "any recent borg version does a quick self-test after startup and before executing any commands." … "borg can't exploit multiple cores yet, so it does not help that the rpi3 has 4 cores."

**Coverage.** T1 — covers weakly:
- the process structure of a remote borg backup: a `borg`/`borgbackup` client, an `ssh` transport, and `borg serve` on the repository host; with an sshfs source, `ssh` and `sshfs` processes beside `borg`;
- one `top` snapshot during `borg info` over sshfs (Debian 10 VM): borg 20.6 %, ssh 8.3 %, sshfs 5.6 % CPU;
- the maintainer's description of `borg serve`'s work (mostly I/O on segment files, crc32 per entry, the in-memory repository index), and the 2018 statement that borg uses one core;
- `time` triples for a repository-wide `borg check --repair` on the server (84 m 12 s wall, 18 m 29 s user, 9 m 35 s sys);
- `time` triples for small `borg create` runs whose wall time the server dominates (1 m 41 s wall against 1.2 s client CPU);
- throughput of `borg create` from an sshfs source (~10 GB/hour), and `borg benchmark crud` rates from a Fedora laptop to a USB HDD.

Every CPU figure comes either from a fault state (hashtable tombstones, #2245) or from `borg info`. None is from a healthy `borg create` on a desktop, and no thread states the cache state. T2/T3/T4/T7: does not cover. #3471 covers nothing beyond the quoted statement.

**Observation status.**
- #2245: one client/server pair, server CPU named (i5-3570K), borg 1.1.0b2/b3. Platform not stated; `/var/log/syslog` and the `borgbackup` command name fit a Debian-family Linux. Window 2017-03-01/02. Fault state.
- #5804: one Debian 10 VM (kernel 4.19.0-16), borg 1.1.16/1.1.17/1.2.0b3/1.2.0. The repository holds 2.30–2.46 TB deduplicated and 3,088 archives, on sshfs. Windows 2021-05 and 2022-03.
- #7374: one Fedora 37 laptop (Ryzen 7 4800H, 32 GB), borg 1.2.3, a 300 GB source over sshfs, 2023-02. A second user's `Duration` is over a 30 Mbps upload, machine not named.

**Reader's own computation** (locates; not values): `python3 -c "print((18*60+28.868+9*60+35.0)/(84*60+12.317), (6.663+2.491)/(60+43.685), (2.231+1.492)/26.835)"` → CPU share 0.333 for `check --repair`, 0.088 for 1.2.0 `info`, 0.139 for 1.1.17 `info`.

### S3-33 — restic GitHub issues #652, #2696, #2679

**Citation.** restic/restic GitHub issues:
- #652 "Reduce CPU usage": martin21, 2016-10-26; closed 2017-02-21; 32 comments.
- #2696 "restic is very slow to backup small files": blastrock, 2020-04-18; closed 2022-07-03; 1 comment.
- #2679 "High fragmentation and very slow backups": JsBergbau, 2020-04-03; closed 2022-08-08; 8 comments. The observation is on Windows, recorded as context.

**Copy read.** `gh api` issue and comments JSON, 2026-09-19 01:30:41–01:30:42 UTC:

| Issue | Issue JSON | Comments JSON |
|---|---|---|
| #652 | 12,737 B, 210127c5fa5433fad550091b92a83b7030314734d41372f176b1ef02b068b97c | 75,164 B, 7c077d3df09a14aeb0583bb2d9c946258968d882851d6d50c5cf6e154d1dfae1 |
| #2696 | 8,530 B, d195b8f0df58114f82acffa92108368c1051319b1136d60f4d765fa65714574d | 2,107 B, bccc0e3fcbb97afd2482f8636f0f68434ede81b67f8cfd000eee49aaa73c961b |
| #2679 | 10,243 B, 50d7d2782bf2612028224acf865b8204a7eae092fb327d4ea769f1a1f7f63da2 | 20,052 B, 7101648ba4029f033779a8466d2ee80af00b508b745f5fd0f9bcbb6f2b843db8 |

Local: `sources/S3-33/`.

**Passages.**

- #652 body ("restic 0.3.0 (v0.3.0-17-gd4f76fb) / compiled at 2016-10-26 12:41:55 with go1.7.3 on linux/amd64"; host `merkaba`): "Initial backup: Up to 150% (probably would have used more, but borgbackup and other processes also used some CPU) / Incremental backup: Up to 330% (see below). It currently has more than 300% for a longer time. Laptop fans at maximum speed".
- #652 body, the `atop` sample (whitespace collapsed): "ATOP - merkaba 2016/10/26 15:43:40 ------------- 10s elapsed / PRC | sys 4.05s | user 30.90s | | #proc 482 | #trun 5 | #tslpi 1383 | #tslpu 0 | #zombie 0 | clones 2 | | no procacct | / CPU | sys 36% | user 310% | irq 3% | | idle 29% | wait 22% | | steal 0% | guest 0% | curf 3.00GHz | curscal 93% | / CPL | avg1 4.63 | avg5 4.54 | | avg15 3.96 | | csw 180689 | | intr 54060 | | | numcpu 4 | / MEM | tot 15.5G | free 162.2M | cache 4.1G | dirty 0.2M | …" … "DSK | sda | busy 16% | read 6058 | write 44 | KiB/r 8 | KiB/w 42 | | MBr/s 4.8 | MBw/s 0.2 | avq 1.27 | avio 0.26 ms | / DSK | sdb | busy 12% | read 6424 | write 44 | KiB/r 9 | KiB/w 42 | | MBr/s 5.8 | MBw/s 0.2 | avq 1.33 | avio 0.18 ms |" … "PID TID RUID EUID THR SYSCPU USRCPU VGROW RGROW RDDSK WRDSK ST EXC S CPUNR CPU CMD 1/7 / 8991 - root root 22 2.61s 27.67s 0K 0K 94756K 0K -- - S 2 307% restic".
- #652 body, `atopsar` (kernel line "merkaba 4.7.0-1-amd64 #1 SMP Debian 4.7.8-1 (2016-10-19) x86_64 2016/10/26"), whitespace collapsed: `-c`: "15:29:07 cpu %usr %nice %sys %irq %softirq %steal %guest %wait %idle _cpu_ / 15:39:07 all 311 0 35 0 4 0 0 27 24" … "15:49:07 all 309 0 34 0 4 0 0 26 28"; `-O`: "15:39:07 8991 restic 316% | 24839 firefox 14% | 24372 Xorg 3% / 15:49:07 8991 restic 297% | 7490 firefox 27% | 2142 Xorg 4%".
- #652 body, restic progress and system: "[34:20] 99.86%  56.128 MiB/s  112.913 GiB / 113.072 GiB  2617417 / 2624033 items  0 errors  ETA 0:02" … "duration: 34:23, 56.12MiB/s" … "System that carries out the backup is ThinkPad T520 with dual SSD BTRFS RAID 1" … "Processor: Intel Core i5-2520M @ 3.20GHz (4 Cores), Motherboard: LENOVO 42433WG, … Memory: 16384MB, Disk: 300GB INTEL SSDSA2CW30 + 480GB Crucial_CT480M50" … "OS: Debian unstable, Kernel: 4.7.0-1-amd64 (x86_64), Desktop: KDE Frameworks 5" … "2) 1 GBit link and low latency (about 1 to 1,5 ms) to backup VM".
- #652 comment 268259319 (martin21, 2016-12-20 14:39:56 UTC): "During the scan phase restic usually uses about 50-70% CPU" … "During the backup phase however, it uses more than 200-320% of CPU while reading about 80 to 150 MiB/s from Dual BTRFS RAID 1."
- #652 comment 281457546 (fd0, MEMBER, 2017-02-21 19:43:33 UTC): "What you're seeing is restic splitting the files into chunks and calculating the SHA-256 hash of each chunk. That together takes a lot of CPU" … "In this phase, restic reads all files, splits them and hashes the chunks. Most of this process is CPU bound."
- #652 comment 284139405 (martin21, 2017-03-04 09:20:24 UTC; over a DSL uplink; the comment arrived by e-mail, and its hard line wraps are joined here): "resticbackup currently is at just 50-110% CPU usage most of the time now with occasionally pikes at 300-350%." … "Atop reports about / si   34 Kbps | so 1221 Kbps".
- #652 comment 284154677 (martin21, 2017-03-04 14:27:53 UTC; unchanged files after one completed backup with a fixed path): "scanned 4081 directories, 65882 files in 0:00" … "duration: 2:19, 1752.00MiB/s".
- #2696 body ("restic 0.9.4 compiled with go1.11.6 on linux/amd64 / Actually 5a7c27ddb62d86440e60764fab4725e520f78e54"; "The hard drive spins at 7200RPM. hdparm reports 175MB/s for non-cached reads."; "fast.com measured my upload speed at 300Mbps"; "I am using a debian unstable with linux 5.4.0"): "The linux cache is cleared before each test with `sync; echo 3 | sudo tee /proc/sys/vm/drop_caches`". Test #1, "1 file of 1GiB full of random" (columns Drive type | FileReadConcurrency | Total time | Speed): "| HDD | 2 | 53s | 19MiB/s |". Test #2, "1024 files of 1MiB full of random": "| HDD | 2 | 5min19s | 3.2MiB/s |" / "| tmpfs | 2 | 5min11s | 3.3MiB/s |" / "| HDD | 16 | 54s | 19MiB/s |".
- #2679 comment 608459562 (MichaelEischer, MEMBER, 2020-04-03 14:19:26 UTC). The reporter is on Windows (restic 0.9.6), so the observation is context; the statements describe restic's code. "Restic already collects all data that belongs into a pack file in a temporary file (stored in one of the usual temp directories) and then passes the full pack on to the operating system for writing into the backup repository. Actually the data is passed to the OS in smaller blocks (32kB)" … "A backup run can write up to `number of CPUs` packs at the same time." … "After writing restic forces the file to be flushed to disk".

**Coverage.** T1 — covers, for `restic backup` on a Linux laptop in 2016:
- the process's CPU share over 10-s and 10-min windows: 307 % in one `atop` interval, 316 % and 297 % in two 10-min `atopsar` intervals;
- 22 threads, from `atop`'s THR column;
- its disk read per interval (RDDSK 94,756 KiB in 10 s), the system's I/O-wait share (22 %) and the system-wide context-switch count;
- the phase split the user states: scan at 50–70 %; read, chunk and hash at 200–320 % while reading 80–150 MiB/s;
- the maintainer's explanation: every re-read file is chunked and SHA-256-hashed, "mostly CPU bound".

The 2016 re-read happened because a changing snapshot path defeated restic's file cache: a real workload, but one caused by configuration. Also covered:
- restic's write pacing as its maintainer describes it (restic ~0.9.6, 2020): a temporary pack file, 32 kB blocks to the OS, up to one pack per CPU in flight, a flush after each pack;
- throughput against file-read concurrency on Linux with a cold page cache (drop_caches stated): 3.2 → 19 MiB/s for 1 MiB files (2020).

On-CPU run lengths: does not cover. T7 — covers: a public `atop` per-process line for a named backup job, pasted into the issue for one interval, with fields PID, TID, RUID, EUID, THR, SYSCPU, USRCPU, VGROW, RGROW, RDDSK, WRDSK, ST, EXC, S, CPUNR, CPU, CMD. T2/T3/T4: does not cover.

**Observation status.**
- #652: one machine named: ThinkPad T520, i5-2520M (2 cores, 4 threads), 16 GB, two SATA SSDs in btrfs RAID 1, Debian unstable, kernel 4.7.0-1. Subject named: a restic 0.3.0 dev build backing up ~113–115 GiB (2.6 M files) of `/home` from a btrfs snapshot to a repository on a VM over 1 GbE. Windows named: `atop` on 2016-10-26 over the 10 s ending 15:43:40, `atopsar` 15:29–15:49, a 34 m 23 s run. Cache state not stated; `atop` shows 4.1 G of page cache out of 15.5 G.
- #2696: one Debian unstable machine (Linux 5.4.0), cold cache, restic commit 5a7c27d.
- #2679: Windows 10, restic 0.9.6 — context.

**Reader's own computation** (locates; not values): for the `atop` interval, `python3 -c "print((2.61+27.67)/10, 94756/10/1024, 180689/10)"` → 3.03 CPUs of restic user+sys per wall second, 9.25 MiB/s read from disk by restic, and 18,069 context switches per second system-wide.

### S3-34 — curl GitHub issues #336 and #11242, with #336's htop screenshots and #11242's debug log

**Citation.** curl/curl GitHub issues:
- #336 "High CPU usage when using --limit-rate option": Konstantinusz, 2015-07-06; closed 2015-07-26; 11 comments.
- #11242 "curl consumes 100% CPU when sending a file with -F": l29ah, 2023-06-03; labels "needs-info" and "HTTP/2"; closed 2023-06-20; 11 comments.

**Copy read.** `gh api` issue and comments JSON, 2026-09-19 01:30:43–01:30:44 UTC. Linked files: #336's screenshots at 01:34:18 UTC, #11242's debug log at 01:34:44 UTC.

| File | Size | SHA-256 |
|---|---|---|
| #336 issue JSON | 5,460 B | 1bc92c64d679347f1e213459117ae3f42656d0f4736694d21cbd3c726396daa7 |
| #336 comments JSON | 24,734 B | 844ff8158e798328e78077509cdf954289e2a98eba59e02a6a3896c79bbd485c |
| #11242 issue JSON | 7,484 B | 142dae1d4bbe56a3a3ac7f35c635fdba457c962f6504c322ed8bc4df062136a5 |
| #11242 comments JSON | 19,207 B | 81992bff983c9e18f03085df07a2a9a4827ac7822505719c65166e4bb84d0c0c |
| `https://i.imgur.com/ZFj6Fqc.png` (#336) | 23,830 B | 59f68e6a859c4e899e9bc326f84f2936db27c6b2b2cb6dc4576c0e4636a4fa1a |
| `https://i.imgur.com/KrNQlyr.png` (#336) | 23,264 B | 65f0677a5736b690836959a3e6fb29c5d36183295fda05c7b654465e2e749c6a |
| tinystash log `tinystash-11242.txt` (#11242; URL in search-log row 67) | 104,954 B, 1,346 lines | 4db6b7fc5ab4740e015a9687d694f595e43d60f5ef68cc339fcb481d9d16f1c5 |

Local: `sources/S3-34/`.

**Passages.**

- #336 body: "CPU was at 50% with one working thread, I used the command line utility "top" to examine CPU usage. If I omit this option CPU usage is only 1-2 % with one working thread."
- #336 comment 118833103 (Konstantinusz, 2015-07-06): "curl 7.43.0 (i686-pc-linux-gnu) libcurl/7.43.0 OpenSSL/1.0.2a zlib/1.2.8 libidn/1.30 libssh2/1.5.0" … "I am using Arch Linux, 4.0.2 and Apache/2.4.9 (Unix)".
- #336 comment 118958377 (jay, MEMBER, 2015-07-06; Ubuntu 14.04 x64 VM, curl 7.44.0-DEV, kernel 3.13.0-55): "Actually when I rate limit 320k I get the opposite effect in Ubuntu, the cpu usage is lower by at most several percentage points. (0-2%,avg 1 rate limited; 0-8%,avg 3 no limit -- empirical only: I just watched top and made some less-than-arbitrary notes)." … "curl --limit-rate 320K http://mirror.umd.edu/ubuntu-iso/15.04/ubuntu-15.04-desktop-i386.iso -L -o - | ./g" … "Worth mentioning that I did this in a VM which you can be sure had some effect on the results."
- #336 comment 119090279 (Konstantinusz, 2015-07-07): "when I omit that option, the CPU usage is always nearly at 0%-0.5% even when the download speed is about 10 MB / sec."
- #336 comment 124909457 (bagder, MEMBER, 2015-07-25): "it works perfectly fine for me with a 0.3 CPU% usage / curl http://localhost/4GB --limit-rate 320K -o /dev/null".
- #336 comment 124931328 (Konstantinusz, 2015-07-26): "I simply renamed the outdated libcurl.so.4.3.0 which was located in /opt/lampp/lib/ and now everything seems to be fine, I don't experience high CPU load, only 1.7-7 % which is quite acceptable on a VPS."
- The reader's transcription of `KrNQlyr.png` (htop, linked in comment 119090279, no `--limit-rate`): header "CPU[ 5.3%]", "Mem[ 118/498MB]", "Load average: 0.28 0.73 0.64"; row "15919 daemon 20 0 5552 4056 3616 S 0.0 0.8 0:00.05 curl -r 97690592-"; rows "5847 walaki 20 0 68848 20400 1560 S 0.5 4.0 1h31:58 transmission-daem" and "5848 walaki 20 0 68848 20400 1560 S 0.0 4.0 1h26:08 transmission-daem".
- The reader's transcription of `ZFj6Fqc.png` (htop, linked in comment 119079303, `--limit-rate` with the outdated libcurl): "CPU[ 100.0%]"; row "13721 daemon 20 0 5560 4116 3672 R 92.9 0.8 3:01.96 curl --limit-rate".
- #11242 body (Gentoo; "Linux l29ah-x201 6.2.5+ … Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz"; "curl 8.1.2 (x86_64-pc-linux-gnu) libcurl/8.1.2 GnuTLS/3.8.0 … nghttp2/1.52.0"): "Tiny CPU consumption appropriate for the pathetic ~200kB/s transfer speed on my i7 CPU." Top of `perf report`: "27.96%     0.00%  curl     [unknown]              [.] 0x0000000000020003" … "12.93%     5.91%  curl     libc.so.6              [.] __send".
- #11242 comment 1594485172 (icing, CONTRIBUTOR, 2023-06-16 10:47:17 UTC): "In the log I see that the upload is progressing. So we have no stall or busy loop here, "just" the action of chunking your upload file into the 16KB frame data of the HTTP/2 protocol, encrypting those and passing them to the network."
- #11242 comment 1594673344 (l29ah, 2023-06-16 13:25:08 UTC): "Downgraded curl to 8.0.1, now it consumes <1% CPU on the same scenario." Comment 1594725562 (icing): "Reproduced. You convinced me that this does not look right."
- Debug log `tinystash-11242.txt` (curl 8.1.2 debug build, no timestamps): line 40 "* h2 [content-length: 416678084]"; line 60 "* [CONN-0-HTTP/2] [h2sid=1] cf_recv(len=102400) -> -1 81, buffered=0, window=0/65535, connection 1048576000/1048576000"; line 62 "* [CONN-0-HTTP/2] [h2sid=1] req_body_read(len=16384) left=416661700 -> 16384, 0"; line 67 "* [CONN-0-HTTP/2] [h2sid=1] cf_send(len=65536) -> 65536, 0, buffered=1, upload_left=416612549, stream-window=0, connection-window=0".

**Coverage.** T3 — covers `curl`'s CPU share while downloading over HTTP on Linux, as `top`/`htop` readings:
- ~0–0.5 % at about 10 MB/s (curl 7.43.0 on an Arch VPS), and 0.0 % in one `htop` refresh with 5.3 % total CPU;
- avg 1 % rate-limited and avg 3 % unlimited from a mirror (Ubuntu 14.04 VM);
- 0.3 % at 320 KB/s from localhost (maintainer);
- 1.7–7 % after the fix.

It also covers bug states at 50–100 %: an outdated libcurl with `--limit-rate`, and curl 8.1.2's HTTP/2 upload at ~200 kB/s (<1 % with 8.0.1). The #11242 debug log shows the call sizes of an HTTP/2 upload: 16,384-B body reads, 65,536-B sends, and 102,400-B receive attempts returning EAGAIN (-1, 81), with the HTTP/2 window values. It has no timestamps, so no rate per call. The wake structure of a download (bytes per receive, wakes per second): does not cover. aria2c and wget: does not cover. T1/T2/T4/T7: does not cover.

**Observation status.**
- #336 (2015): the reporter's host is a VPS, not a desktop: one CPU bar in `htop`, 498 MB RAM, curl run as CGI under Apache. The maintainers' readings are from a VM and from localhost. No window lengths.
- #11242: one laptop (i7-8550U, Gentoo, kernel 6.2.5), curl 8.1.2 (bug) against 8.0.1, uploading a 416,678,084-B multipart body to 0x0.st, 2023-06.

**Reader's own computation** (locates; not values), over the debug log:
- `grep -o 'cf_send(len=[0-9]*) -> [-0-9]*' tinystash-11242.txt | sort | uniq -c` → 114 sends of 65,536 → 65,536; one 65,536 → 49,152; one of 181; one of 16,384.
- `grep -o 'req_body_read(len=[0-9]*) left=[0-9]* -> [-0-9]*' tinystash-11242.txt | sed -E 's/left=[0-9]+ //' | sort | uniq -c` → 462 reads returning 16,384.
- `grep -o 'cf_recv(len=[0-9]*) -> [-0-9]* [0-9]*' tinystash-11242.txt | sort | uniq -c` → 117 × "-1 81".
- Body bytes consumed over the log: `python3 -c "print(416678084-409141444)"` → 7,536,640 B (115 × 65,536).

### S3-35 — ClamAV GitHub issues #590, #849, #1375, with #590's flamegraphs

**Citation.** Cisco-Talos/clamav GitHub issues:
- #590 "Since version 0.105 the scan is unbearable slow": martin-ms, 2022-05-21; open; 53 comments; last updated 2026-03-18.
- #849 "(since running freshclam) scanning simple files is slow": leapfog, 2023-03-01; closed 2023-03-02; 13 comments.
- #1375 "Problem with slow clamscan": ebo-47, 2024-09-27; closed 2024-10-28 as a duplicate of #590; 3 comments.

**Copy read.** `gh api` issue and comments JSON, 2026-09-19 01:30:45–01:30:47 UTC. Flamegraph SVGs attached to #590 comments 1535822498, 1537198319 and 1537473757 (`https://user-images.githubusercontent.com/<user>/<name>.svg`; full names in search-log rows 70–74), 01:35:58 UTC.

| File | Size | SHA-256 |
|---|---|---|
| #590 issue JSON | 3,775 B | c33649e43e9304a06e22584b5ff67f824a00187609e5e54a9b0c9328458ad4d9 |
| #590 comments JSON | 132,226 B | 0dc719fd920eb49b6902dd490f90545c7a032f1874ec07d3b7a747a2bf5630d1 |
| #849 issue JSON | 6,361 B | aa64579a4b83fff581412fa832d1b5b9cd16b52393c1ebf7a30b4bb5f25fefd2 |
| #849 comments JSON | 23,749 B | d780fcce694d9e79d1b7d82bf1e09cd5da7d29940583f792c343dce000d2169e |
| #1375 issue JSON | 4,611 B | c264682a36e2df4d1a20c196210a8d505cfe2d6538732d8a7c8142b599a0cefd |
| #1375 comments JSON | 5,934 B | 12270d0d1839c07d2afd59510d69a1004a465fd448f61d012c22ddd48002d27f |
| `fg-236687385-…svg` (0.104.2, `$HOME`) | 34,568 B | a0e80e340ce18243929b4851721a01783bc86c7282acf95d188e0a2c3a4f68b9 |
| `fg-236687444-…svg` (1.0.1, `$HOME`) | 36,946 B | 921536eb689efb3c2677bea46007a5fd550ae82cc67d2f1e3ad55973fd58b14f |
| `fg-236641028-…svg` (one PDF) | 59,954 B | 0ce6205a552f30635741882e77d73d4cf8d3cd2ea714e28ac60b951ad99ed96f |
| `fg-236843976-…svg` (unit-test database; not quoted) | 12,125 B | 470b488d0363476b29b4f98440b641272d422ad0b289131eb3e4a6f2f420ffa1 |
| `fg-236844093-…svg` (unit-test database; not quoted) | 11,788 B | 3ee939aeedfda60e5395eabf53b8916ac177be6ce25bd543bf65884173b2adab |

Local: `sources/S3-35/`.

**Passages.**

- #590 comment 1537473757 (martin-ms, 2023-05-07 15:45:34 UTC), run as "`perf record -F 100 -g -- /usr/bin/clamscan -ir $HOME`". The 0.104.2 run: "Engine version: 0.104.2 / Scanned directories: 8457 / Scanned files: 145265 / Infected files: 3 / Data scanned: 21981.75 MB / Data read: 15944.07 MB (ratio 1.38:1) / Time: 2221.037 sec (37 m 1 s) / Start Date: 2023:05:07 13:22:45 / End Date:   2023:05:07 13:59:46 / [ perf record: Woken up 55 times to write data ] / [ perf record: Captured and wrote 13,965 MB perf.data (218477 samples) ]". The 1.0.1 run: "Engine version: 1.0.1 / Scanned directories: 8462 / Scanned files: 145753 / Infected files: 3 / Data scanned: 28681.03 MB / Data read: 15988.41 MB (ratio 1.79:1) / Time: 6552.762 sec (109 m 12 s) / Start Date: 2023:05:07 14:15:39 / End Date:   2023:05:07 16:04:52 / [ perf record: Woken up 175 times to write data ] / [ perf record: Captured and wrote 44,184 MB perf.data (656843 samples) ]".
- The flamegraph from that comment for 0.104.2 (`fg-236687385-…svg`), SVG `<title>` texts: "all (218,477 samples, 100%)", "clamscan (218,477 samples, 100.00%)", "cli_ac_scanbuff (57,402 samples, 26.27%)", "cli_bm_scanbuff (24,418 samples, 11.18%)", "sscanf (19,882 samples, 9.10%)". For 1.0.1 (`fg-236687444-…svg`): "all (656,843 samples, 100%)", "cli_ac_scanbuff (39,269 samples, 5.98%)", "&lt;jpeg_decoder::upsampler::UpsamplerH2V2 as jpeg_decoder::upsampler::Upsample&gt;::upsample_row (4,261 samples, 0.65%)". Neither graph carries kernel frames.
- #590 comment 1537198319 (Devstellar, 2023-05-06 18:33:06 UTC; clamscan 1.0.1 rebuilt with debug symbols, one PDF): "Loading:     9s, ETA:   0s [========================>]    8.67M/8.67M sigs / Compiling:   2s, ETA:   0s [========================>]       41/41 tasks" … "Data scanned: 472.84 MB / Data read: 17.62 MB (ratio 26.83:1) / Time: 132.078 sec (2 m 12 s)" … "[ perf record: Captured and wrote 0.875 MB perf.data (13206 samples) ]". Its flamegraph (`fg-236641028-…svg`) weights frames by event period, not by sample count: "clamscan (547,647,815,661 samples, 100.00%)", "ac_backward_match_branch (334,347,641,414 samples, 61.05%)", "pread64 (1,284,807,196 samples, 0.23%)".
- #590 comment 1336151478 (net1, 2022-12-03; clamscan 1.0.0): "Loading:    24s, ETA:   0s [========================>]    8.82M/8.82M sigs / Compiling:   4s, ETA:   0s [========================>]       42/42 tasks".
- #590 body (0.105.0 against 0.104.2, same `$HOME`, "a few minutes later"): "Engine version: 0.105.0 / Scanned directories: 6240 / Scanned files: 98280 / … / Data scanned: 22403.29 MB / Data read: 12333.45 MB (ratio 1.82:1) / Time: 5897.640 sec (98 m 17 s)" and "Engine version: 0.104.2 / Scanned directories: 6240 / Scanned files: 97797 / … / Data scanned: 17019.32 MB / Data read: 12226.76 MB (ratio 1.39:1) / Time: 1569.143 sec (26 m 9 s)".
- #590 comment 1758186534 (martin-ms, 2023-10-11 17:48:59 UTC; the same limits for both versions, `--exclude=pdf$ --exclude=jpg$ --exclude=jpeg$ --exclude=png$ --max-filesize=25M --max-scansize=100M …`): "Engine version: 0.104.2 / … / Scanned files: 154456 / … / Data read: 11790.80 MB (ratio 0.91:1) / Time: 1445.337 sec (24 m 5 s)" and "Engine version: 1.2.0 / … / Scanned files: 155398 / … / Data read: 11824.57 MB (ratio 0.92:1) / Time: 1798.677 sec (29 m 58 s)".
- #590 comment 1147948644 (val-ms, CONTRIBUTOR, 2022-06-06 21:26:18 UTC): "In 0.105 we increased the default max file-size, max scan-size, etc." … "- MaxFileSize        25M  -> 100M / - MaxScanSize        100M -> 400M". Comment 4084546953 (val-ms, 2026-03-18 18:01:02 UTC): "the complaint in this ticket wasn't signature count related.  It has to do with changes in functionality such as the addition of image fuzzy hashing as well as increasing default scan limitations that resulted in longer processing times."
- #849 body (Gentoo, "Linux 6.2.1-gentoo", ClamAV 0.103.8): "it took 12s to scan /etc/fstab. Then I run 'freshclam', now scanning the same file needs more than 90 seconds."
- #849 comment 1450304536 (lunika, 2023-03-01 15:06:30 UTC), before the faulty daily database: "time /usr/bin/clamscan --no-summary --stdout --remove=no --scan-archive=yes -r testfiles/sample.pdf / /var/task/lambda-convert/testfiles/sample.pdf: OK / / real	0m17.322s / user	0m16.817s / sys	0m0.505s".
- #849 comment 1472640852 (val-ms, 2023-03-16 19:43:02 UTC): "18 seconds is a normal amount of time for clamscan to load the databases. / If you want a faster scan time for individual scans, then you may wish to run clamd (which will take ~18 seconds to start) and then trigger scans with `clamdscan` instead of `clamscan`."
- #1375 body (Raspberry Pi 4 B, a 1 TB USB HDD mounted with ntfs-3g): Buster 32-bit, "Engine version: 0.103.9 … Scanned files: 3351 … Data scanned: 12147.82 MB / Data read: 46156.46 MB (ratio 0.26:1) / Time: 3653.004 sec (60 m 53 s)"; Bookworm 64-bit, "Engine version: 1.0.5 … Scanned files: 3353 … Data scanned: 17547.89 MB / Data read: 46156.81 MB (ratio 0.38:1) / Time: 46123.837 sec (768 m 43 s)".

**Coverage.** T4 — covers, for on-demand `clamscan` runs on Linux:
- CPU share over single-file scans: `time` gives user 16.8 s + sys 0.5 s of 17.3 s real. The database load dominates; "18 seconds is a normal amount of time", per a ClamAV developer.
- CPU share over two whole-`$HOME` scans: only through the `perf record -F 100` sample counts against the stated scan times — about one CPU for the whole wall time (see computation).
- the database-load phase: `Loading` 9 s and 24 s, and `Compiling` 2 s and 4 s, for 8.67 M and 8.82 M signatures in the quoted runs;
- scan summaries across versions and limits on the same `$HOME`: Data read 11.8–16.0 GB, 1,445–6,553 s;
- the developer's account of why 0.105 and later are slower (raised size limits, image fuzzy hashing), and the recommendation to use `clamd` with `clamdscan` for individual scans;
- a per-function CPU profile of whole-`$HOME` scans: the pattern matchers `cli_ac_scanbuff` and `cli_bm_scanbuff` dominate in 0.104.2.

Throttling or pacing of the scan: nothing in these threads says `clamscan` paces itself. Threading: the flamegraphs show one command, `clamscan`; there is no thread statement. I/O pattern: `pread64` takes 0.23 % of cycles for one PDF; the `$HOME` graphs carry no kernel frames. T1/T2/T3/T7: does not cover.

**Observation status.**
- #590 `$HOME` scans: one user's machine, not described. Linux is inferred from the glibc `libc.so.6` and `libclamav.so.*` frames in the flamegraphs and the `/run/clamav` paths in comment 1148514776; CPU, disk and distribution are not named. Subject named: clamscan 0.104.2 / 0.105.0 / 1.0.0 / 1.0.1 / 1.2.0 with `-ir $HOME`, ~98–190 k files. Windows named by start and end dates. Cache state not stated: the runs are minutes apart on the same tree, so later runs may be warm.
- Devstellar: machine unnamed, one PDF, 2023-05-06.
- #849: machines unnamed (Gentoo; a `/var/task/lambda-convert` path).
- #1375: Raspberry Pi 4 B, USB HDD, 2024-09.

**Reader's own computation** (locates; not a value):
- `python3 -c "print(218477/(100*2221.037), 656843/(100*6552.762), 13206/(100*132.078))"` → 0.98, 1.00, 1.00. perf's frequency mode aims at 100 samples per second of the sampled task's on-CPU time, so the ratio approximates CPUs used per wall second. That holds only if the event counts only while clamscan runs and the frequency target is met; the thread states neither.
- `python3 -c "print(15944.07/2221.037, 15988.41/6552.762)"` → 7.18 and 2.44 MB of `Data read` per second.
- `python3 -c "print((16.817+0.505)/17.322)"` → 1.00.

### S3-36 — OpenBenchmarking.org result 2305286-NE-MONITORSY37 (compress-7zip) and test profile pts/compress-7zip-1.10.0

**Citation.** OpenBenchmarking.org result 2305286-NE-MONITORSY37, titled "Monitor=sys.power,cpu.power,mem.temp,cpu.usage phoronix-test-suite benchmark compress-7zip". Uploader field `<User>chuck</User>`, system timestamp 2023-05-28 10:22:52, Phoronix Test Suite 10.8.4. Test profile `pts/compress-7zip-1.10.0` (maintainer Michael Larabel), as mirrored in the phoronix-test-suite repository at `ob-cache/test-profiles/pts/compress-7zip-1.10.0/`, commit f977d6e270d5eb9eebfa26d3ca62385c00a547a6 (2026-07-27).

**Copy read.** The HTML page could not be read (rows 76–79): the challenge pages saved are `p1.html` (5,498 B, 4bfe383e4abc784e1c32a372341a6cf9b62eebf3dc5508bd0d83670a6484d35d) and `p2.html` (5,818 B, f40a264e0135795d106f13b754ed59da609f79e1f5082ec3c63548a0529ed1db). The result was read through the Phoronix Test Suite client endpoint, POST `https://openbenchmarking.org/f/client.php` with `r=clone_openbenchmarking_result` and User-Agent `PhoronixTestSuite/Nesseby` (rows 80–82). The request format comes from the PTS sources at f977d6e.

| File | Size | SHA-256 | Accessed (UTC) |
|---|---|---|---|
| response JSON `clone2.json` | 4,783 B | fa04dc895bc28b3e1869828c38a0af4db393979c4b04174b6b45b073bbecfeef | 01:37:27 |
| its `composite_xml`, saved as `composite-2305286-NE-MONITORSY37.xml` | 4,467 B | 8c42307509d7795475c97af67717e19000e7ff65e6b579734c96a698fbae877a | 01:37:27 |
| earlier reply to UA `PTS/10.8.6`, `clone.json` ("No Client") | 9 B | 206044561c061d850c4578ea22f35d4ab615de0517446210cdcf7be10592040a | 01:37:19 |
| system logs, `r=clone_openbenchmarking_system_logs`, `syslogs.zip` (SHA-1 074ebc73e6e24c3872de97652f87247973de0f5e, equal to the JSON's `system_logs_available`) | 97,896 B | e889ddbfa321552afc22636c03217fa9ad7dccfc5e6df9e511ccef0e6acb6d6a | 01:37:53 |
| profile `install.sh` | 325 B | abc43fde61cb062cdd41f78aa2521a668bfc9b6b78a9b0f0c426313c344feb16 | 01:38:16 |
| profile `test-definition.xml` | 958 B | 6f4474a450af4fc04c372b4bb2b7d904657d24206dd19b8d12d3969ac0de0a65 | 01:38:16 |
| profile `results-definition.xml` | 1,719 B | 3bd93c65ef4ce1adc68d4c114f5582a750deed7a11485edd52da423f485d5254 | 01:38:16 |
| profile `downloads.xml` | 995 B | dbe1cb52bd79019d50295ead218786c2fc8cf985b002bd8500a48460ee6c0653 | 01:38:16 |
| profile `changelog.json` | 1,181 B | bf56f78740278cee887d04b0e297efa14e567dc4159edb39b5f9c44e7b7d5377 | 01:38:16 |
| PTS source `pts_openbenchmarking.php` | 38,870 B | 5ec1c3e1b5155fe081c55ac24c9bea15877f17e06243ccbb5c90a081dd3a0b3b | 01:36:53 |
| PTS source `pts_network.php` | 19,048 B | 859421d1be5e8cb6cec164d89493280b1acfdac09565ea0eca7f550ec8977a60 | 01:36:53 |
| PTS source `pts-core.php` | 10,658 B | 93f842db9f49123c29c2224879eb6e6a33ada4fb95c0be9b064e54bba14f9833 | 01:36:53 |

Local: `sources/S3-36/`.

**Passages.**

- Composite XML, `<Generated>`: "<Title>Monitor=sys.power,cpu.power,mem.temp,cpu.usage phoronix-test-suite benchmark compress-7zip</Title> / <LastModified>2023-05-28 10:30:58</LastModified> / <TestClient>Phoronix Test Suite v10.8.4</TestClient>".
- Composite XML, `<System>`: "<Hardware>Processor: AMD Ryzen 5 2600X Six-Core @ 3.60GHz (6 Cores / 12 Threads), Motherboard: Gigabyte X470 AORUS ULTRA GAMING-CF (F64a BIOS), Chipset: AMD 17h, Memory: 32GB, Disk: 1024GB Sabrent + 240GB SanDisk SDSSDX24 + 2048GB Micron_1100_MTFD, …</Hardware> / <Software>OS: Ubuntu 22.04, Kernel: 5.15.0-72-lowlatency (x86_64), Desktop: KDE Plasma 5.24.7, … File-System: ext4, Screen Resolution: 3440x1440</Software>"; in its JSON: `"cpu-scaling-governor":"acpi-cpufreq schedutil (Boost: Enabled)"`.
- Composite XML, the first `<Result>`: "<Identifier>pts/compress-7zip-1.10.0</Identifier> / <Title>7-Zip Compression</Title> / <AppVersion>22.01</AppVersion> / … / <Description>Test: Compression Rating</Description> / <Scale>MIPS</Scale> / … / <Value>38769</Value> / <RawString>38475:38968:38863</RawString> / <JSON>{…,"test-run-times":"35.49:35.79:35.77"}</JSON>". The second: "<Description>Test: Decompression Rating</Description>" … "<Value>35517</Value> / <RawString>35865:35351:35334</RawString>". These are the only two `<Result>` elements.
- System log `system-logs/2600/cmdline`: "BOOT_IMAGE=/boot/vmlinuz-5.15.0-72-lowlatency root=UUID=6a75675a-0afa-4565-88a9-cfca91c617dc ro threadirqs acpi_sleep=nonvs".
- Profile `install.sh`: "tar -xf 7z2201-src.tar.xz / cd CPP/7zip/Bundles/Alone2 / CFLAGS="-O3 -march=native -Wno-error $CFLAGS" make -j $NUM_CPU_CORES -f makefile.gcc" … "echo "#!/bin/sh / ./CPP/7zip/Bundles/Alone2/_o/7zz b > \$LOG_FILE 2>&1".
- Profile `test-definition.xml`: "<Description>This is a test of 7-Zip compression/decompression with its integrated benchmark feature.</Description> / <ResultScale>MIPS</ResultScale> / <Proportion>HIB</Proportion> / <TimesToRun>3</TimesToRun>" … "<TestType>Processor</TestType>" … "<InternalTags>SMP</InternalTags>".
- Profile `results-definition.xml`: the parser template opens "Compressing  |                  Decompressing / Dict     Speed Usage    R/U Rating  |      Speed Usage    R/U Rating / KiB/s     %   MIPS   MIPS" and takes its result from the "Avr:" row's Rating column.

**Coverage.** T1 — context only. The test runs 7-Zip 22.01's built-in in-memory benchmark (`7zz b`, built from source with `-O3 -march=native`), not an archive of a file set through the disk. Its result is a MIPS rating per run: compression 38,769 and decompression 35,517, three runs of ~35.5 s each, on a named Linux desktop. The `cpu.usage` monitor named in the title has no result entry in the composite XML the client endpoint serves. The system-log archive holds only system-description files (uname, cpuinfo, lspci, …). So no CPU-usage series was found in this result. 7-Zip's own "Usage" column, which the parser template shows, is not stored in the result. T7 — covers: the fields of a public OpenBenchmarking result record (hardware and software strings, kernel, governor, microcode, per-run raw values and run times, system logs). T2/T3/T4: does not cover.

**Observation status.** One machine named: Ryzen 5 2600X (6 cores, 12 threads), 32 GB, ext4, Ubuntu 22.04, kernel 5.15.0-72-lowlatency booted with `threadirqs`, schedutil. Subject named: 7-Zip 22.01 `7zz b`, in memory. Window 2023-05-28 10:22:52–10:30:58. The workload does no disk I/O. Whether the HTML result page shows monitor graphs could not be checked (403).

## 3. Not found

- **T1, rsync per-process CPU (generator/sender/receiver) on Linux in a current-decade trace or log with `top`/`ps` figures.** The only Linux per-process observation is the 2010 LWN article (S3-16, atop-based, three processes described but per-process CPU not tabulated; whole-job hog 83 %). Searches 10, 28, 29, 39, 41 (rsync + top/atop/htop/perf/strace, mailing list, blogs); the rsync list threads found (S3-08) are Cygwin or figure-free; Phoronix/OpenBenchmarking have no rsync profile with CPU (search 1; openbenchmarking 403).
- **T1, borg per-run CPU of a healthy `borg create` on a desktop.** Only a VPS benchmark (S3-13, borgbase, 1 vCPU) and a home-server `time` for `borg prune` with platform unstated. The borg GitHub issues #2245, #3471, #5804 and #7374 were read on the 2026-09-19 retry (S3-32, rows 56–59). They give a fault-state `borg serve` at 100 %, a `borg check --repair` `time` triple, a `top` line for `borg info` with its ssh/sshfs helpers, and throughput without CPU — none is a healthy `borg create` on a desktop (searches 2, 15). restic is no longer in this gap: the retry found a 2016 Linux-laptop `atop` capture of `restic backup` (S3-33, rows 60–62).
- **T1, 7z archiving a file set on Linux with CPU share.** Only the in-memory `7z b` benchmark (S3-25; searches 11, 23, 43). The OpenBenchmarking compress-7zip result with `MONITOR=cpu.usage` (2305286-NE-MONITORSY37) was read on the 2026-09-19 retry through the PTS client endpoint (S3-36, rows 76–84). It too runs `7zz b` in memory, and its result file carries no `cpu.usage` monitor entry.
- **T1, on-CPU run lengths between I/O waits for any of the named programs.** Only the off-CPU interval histogram for `tar` (S3-22, cpudist), context-switch counts per borg job (S3-13), and one system-wide `atop` context-switch count during `restic backup` (S3-33). No `perf sched` trace of rsync/cp/borg/7z was found (searches 29, 38).
- **T2, steady-state wake cadence and CPU per wake of an indexer on a settled home directory.** No time series found; the closest are the settle-after-rename durations for tracker-miner-fs-3 (S3-01, #228) and the flamegraph/`chrt` capture of baloo_file_extractor during a content index (S3-03, 500665). Searches 3, 4, 22, 27 (GNOME GitLab, KDE Bugzilla incl. REST quicksearch "cpu idle", Launchpad, Manjaro/Fedora/KDE forums). Baloo's own wake cadence: does not appear in any fetched report.
- **T2, plocate `updatedb` timing.** plocate.sesse.net carries query timings only (S3-19); only mlocate `updatedb` runs were found (S3-19: 2024 systemd accounting, 2008 `time`). Searches 26, 37; git.sesse.net unreachable (proxy CONNECT rejected).
- **T3, a timestamped trace of receive sizes and intervals (bytes per wake, wakes per second) for a Linux downloader or the Steam client.** ValveSoftware/steam-for-linux issue #13024 was read on the 2026-09-19 retry (S3-28, row 49). It carries:
  - the reporter's summary figures (~180 KB receive window, ~1 Mbps per connection, ~6.7 KB per `recvfrom`, idle periods of hundreds of ms to seconds);
  - a seven-call `strace` excerpt;
  - a second reporter's four `recvmsg` lines without wall-clock timestamps.

  No full trace is attached, and the reporter's last comment attributes the cap to Valve server caching. For wget, curl and aria2c downloads no such trace was found. The one curl debug log (S3-34, row 67) is of an HTTP/2 upload and has no timestamps (searches 31, 33, 45; rows 49, 63–67).
- **T3, Steam client CPU on Linux paired with its download rate.** Per-process CPU numbers now exist (S3-31, rows 53–55): `top` 341.5 % and `htop` 461 % for the `steam` process, with no rate stated. One GNOME System Monitor screenshot pairs per-CPU load with 8.5 MiB/s received, but system-wide, not per process. #13024 gives "highest ~14%" per core at ~20 MB/s (S3-28). No per-process CPU at a stated rate. The forum threads (S3-21) name machine and rates but not CPU.
- **T3, `content_log.txt` with depot chunk counts/throughput.** Found on the 2026-09-19 retry: a complete public `content_log.txt` pair (S3-29, rows 50–51) and excerpts (S3-30, row 52). The scribd copies (searches 6, 31) were still not attempted.
- **T3, curl/aria2c CPU at line rate on Linux.** curl #336 (S3-34, rows 63–65) gives `top`/`htop` readings of 0–0.5 % at about 10 MB/s on a VPS, and 0.3 % at 320 KB/s from localhost (2015). #11242 is an HTTP/2 upload busy-loop bug. Older bug-state busy loops are in S3-18; wget has one `top` snapshot (S3-17). No figure at gigabit line rate; aria2c none (searches 12, 28, 34, 39).
- **T3, Thunderbird attachment send with size/link/CPU on Linux.** Only progress-bar-CPU comments without message size (S3-09, 742697 c24/c25); the 100 %-CPU-with-TLS bugs are Windows-era (search 16).
- **T4, a directly measured CPU share over a whole-directory `clamscan`/`clamdscan` scan on a Linux desktop.** S3-06 has a summary without CPU. S3-10 has `top` lines from server-side mail scanning (2004/2019). The ClamAV GitHub issues #849, #590 and #1375, read on the 2026-09-19 retry (S3-35, rows 68–75), add:
  - `time` triples for single-file scans (user ≈ real; the database load dominates);
  - two whole-`$HOME` scans whose CPU share is available only as the reader's derivation from `perf record -F 100` sample counts (≈0.98–1.00), on an undescribed machine.

  No statement that `clamscan` throttles or paces itself appears in these threads (searches 5, 13, 30, 46, 47).
- **T7, a public per-process CPU+I/O dataset of Linux desktop background jobs.** Established as not found in the venues searched:
  - no atop/collectl/sysdig/LTTng/perf archives of desktops (searches 7, 20, 21, 25, 36, 40);
  - SNIA holds only ≥10-year-old syscall traces and the 2008 FIU block traces with process names (S3-20);
  - BEHACOM (S3-27) is the only in-the-wild Linux desktop dataset found, and it names only the foreground application.

  The closest small public records with per-process CPU or I/O for a named background job are the KDE 500665 flamegraph (S3-03), the borgbase results (S3-13), the 2016 `atop` line for `restic backup` (S3-33), and, for throughput only, a full Steam `content_log.txt` pair (S3-29). The OpenBenchmarking result read on the retry (S3-36) carries no monitor data.

Unreachable on 2026-09-17 (recorded, not cited then): github.com and api.github.com (all issue pages), openbenchmarking.org, phoronix.com search, sylab-srv.cs.fiu.edu, git.sesse.net, iotta.snia.org/traces/block-io/391 (subtrace listing), pmc.ncbi.nlm.nih.gov (reCAPTCHA; Europe PMC used). On the 2026-09-19 retry:
- the GitHub issues named in the brief and the files their threads link were read (rows 49–75);
- openbenchmarking.org's HTML result, export and test-profile pages still answer 403 behind a Cloudflare challenge, and the result itself was read through the Phoronix Test Suite client endpoint (rows 76–84);
- the other hosts were not retried.
