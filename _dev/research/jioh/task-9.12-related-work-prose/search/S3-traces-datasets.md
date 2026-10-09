# S3 — public traces and datasets (reader record)

Reader class S3. Access date for every fetch and computation: 2026-10-07. Sandbox: Ubuntu 24.04.5 LTS container, outbound HTTPS through the session proxy (TLS verified against the proxy CA bundle). Copies were saved under `sources/S3-NN/` (gitignored). Everything a reader needs is quoted below. Counts I computed myself come with the exact command or script and its verbatim output. Scripts are reproduced in full in Appendix A, and long outputs are in Appendix B.

Topics in scope: T7 (counts over units, packages or a rules catalogue), T10 (traces or datasets with context-switch rates or latencies), T11 (benchmark datasets of local LLM latency), T12 (session-duration or application-usage datasets). For T1–T6, T8, T9 and T13–T15, see the end of section 2.

---

## 1. Search log

| # | Date | Engine / venue | Exact query or URL | Hits followed | Dead ends (HTTP status) |
|---|---|---|---|---|---|
| 1 | 2026-10-07 | Debian Code Search (codesearch.debian.net), no-JS HTML `/search` | `CPUSchedulingPolicy=idle` (literal) | 3 result pages, 13 packages | `GET /api/v1/search?query=…&match_mode=literal` → **403** (API needs key). The no-JS page returns results after polling (it first shows "Still searching", then refreshes) |
| 2 | 2026-10-07 | DCS | `CPUSchedulingPolicy=idle path:\.(service\|timer)` (literal) | 2 pages | — |
| 3 | 2026-10-07 | DCS | `CPUSchedulingPolicy=batch path:\.(service\|timer)` (literal) | 1 page | — |
| 4 | 2026-10-07 | DCS | `Nice=19 path:\.(service\|timer)` (literal) | 4 pages | — |
| 5 | 2026-10-07 | DCS | `IOSchedulingClass=idle path:\.(service\|timer)` (literal) | 4 pages | — |
| 6 | 2026-10-07 | DCS | `IOSchedulingClass=3 path:\.(service\|timer)` (literal) | 1 page | — |
| 7 | 2026-10-07 | DCS | `CPUSchedulingPolicy= path:\.(service\|timer)` (literal) | 5 pages | — |
| 8 | 2026-10-07 | DCS | `^\s*Nice= path:\.(service\|timer)` (regex) | 7 pages | — |
| 9 | 2026-10-07 | DCS | `IOSchedulingClass= path:\.(service\|timer)` (literal) | 8 pages | — |
| 10 | 2026-10-07 | DCS | `SCHED_IDLE path:\.(c\|cc\|cpp\|h)$` (literal) | 34 pages | The first run broke at page 15 (curl transfer error, file not written; the proxy status listed `ws_closed_mid_exchange … codesearch.debian.net:443`). I re-ran it with `--retry 5` and it completed |
| 11 | 2026-10-07 | DCS, grouped by package (`perpkg=1`) | `^\[Service\] path:\.service` (regex), pages 0, 1, 318 | denominator: 319 pages | — |
| 12 | 2026-10-07 | DCS, per package | `^\[Service\] path:\.service package:<p>` (regex) for p ∈ {clamav, localsearch, kf6-baloo, plocate, mlocate, findutils, deja-dup, borgbackup, restic, timeshift, backintime, tracker-miners, baloo-kf5, akonadi-search} | unit files of localsearch, kf6-baloo, plocate, findutils, restic-rest-server | Zero hits for clamav, mlocate, deja-dup, borgbackup, timeshift, backintime, tracker-miners, baloo-kf5 and akonadi-search. A check query `package:clamav freshclam` (literal) matched only `clamav-cvdupdate`, so the `clamav` source package is **absent from the DCS index** even though its units exist (row 13) |
| 13 | 2026-10-07 | sources.debian.org `/data/main/…` and `/api/src/…` | Raw files: plocate 1.1.25-1 `plocate-updatedb.service.in`; findutils 4.11.0-3 `debian/locate.service`; localsearch 3.12.0-1 `src/indexer/tracker-miner-fs.service.in` and `src/indexer/tracker-main.c`; kf6-baloo 6.30.0-1 `src/file/kde-baloo.service.in`, `src/file/priority.cpp`, `src/file/main.cpp`, `src/file/extractor/main.cpp`; tumbler 4.20.2-1 `tumblerd/tumbler-scheduler.c`; recoll 1.43.16-1 `index/recollindex.cpp`; akonadi-search 4:26.04.3-3 `agent/priority.cpp`; clamav 1.4.6+dfsg-1 `clamd/clamav-daemon.service.in`, `freshclam/clamav-freshclam.service.in`, `clamonacc/clamav-clamonacc.service.in` | all 200 | — |
| 14 | 2026-10-07 | Local filesystem of this sandbox | `/lib/systemd/system/*.{service,timer}`, `/usr/lib/systemd/user/*.{service,timer}` | 163 unit files | `dpkg -S` printed nothing (dpkg database not usable here) |
| 15 | 2026-10-07 | git clone | `https://github.com/CachyOS/ananicy-rules.git` (depth 1) | commit 03ef03fb… | — |
| 16 | 2026-10-07 | Hugging Face Hub API | `https://huggingface.co/api/datasets/optimum-benchmark/llm-perf-leaderboard`; `…/resolve/94a9713e…/data/perf-df-pytorch-cuda-awq-1xT4.csv` | 1 CSV (12.3 MB) | — |
| 17 | 2026-10-07 | localscore.ai | `/`, `/about`, `/latest`, `/download`, `/model/1`, `/model/2`, `/model/3`, `/accelerator/349`, `/accelerator/43`, `/result/4246`, `/result/4252`, `/result/4254`, `/result/4255` | all 200 | — |
| 18 | 2026-10-07 | mlcommons.org | `https://mlcommons.org/benchmarks/client/` | 1 page | No public results table was found on that page |
| 19 | 2026-10-07 | github.com (llama.cpp performance discussions) | `https://github.com/ggml-org/llama.cpp/discussions/4167`, `…/discussions/15013`, `https://api.github.com/repos/ggml-org/llama.cpp/discussions/4167` | — | **403** on all three |
| 20 | 2026-10-07 | artificialanalysis.ai (hosted-API latency) | `/models/llama-3-1-instruct-8b/providers` | 1 page | — |
| 21 | 2026-10-07 | storage.googleapis.com (Perfetto example trace) | `https://storage.googleapis.com/perfetto-misc/example_android_trace_15s` (57.2 MB); `https://get.perfetto.dev/trace_processor` → `https://commondatastorage.googleapis.com/perfetto-luci-artifacts/v58.2/linux-amd64/trace_processor_shell` | trace + tool (tool SHA-256 matches the launcher's pinned hash) | — |
| 22 | 2026-10-07 | raw.githubusercontent.com / drive.google.com | google/cluster-data `ClusterData2019.md`, `ClusterData2011_2.md`, `README.md`; 2019 schema PDF (drive id 10r6cnJ5…), 2011 schema PDF (drive id 0B5g07T_…); alibaba/clusterdata `README.md`, `cluster-trace-v2018/trace_2018.md`, `cluster-trace-v2018/schema.txt`, `cluster-trace-v2017/trace_201708.md` | all 200 | Grep for `context.switch\|context_switch\|ctx` in all of them returned no hits |
| 23 | 2026-10-07 | openbenchmarking.org / phoronix.com | `https://openbenchmarking.org/test/pts/ctx-clock`, `…/pts/ctx-clock-1.0.0`, `…/pts/stress-ng`, `https://www.phoronix.com/`, `https://www.phoronix.com/review/linux-611-features` | — | **403** on all of them (the body is a Cloudflare "Just a moment… Enable JavaScript and cookies to continue" challenge) |
| 24 | 2026-10-07 | git clone | `https://github.com/intel/lmbench.git` (depth 1) | `doc/ctx.tbl`, `doc/usenix96.ms`, `doc/lat_ctx.8` | `results/` holds only a Makefile. `https://www.lmbench.org/` → no connection (curl 000) |
| 25 | 2026-10-07 | raw.githubusercontent.com | torvalds/linux master `tools/perf/Documentation/perf-sched.txt` | 1 file | — |
| 26 | 2026-10-07 | WebSearch | `World of Warcraft Avatar History dataset WoWAH download session length` | web.cs.wpi.edu mirror (paper + index), homepage.iis.sinica.edu.tw | `https://homepage.iis.sinica.edu.tw/~swc/pub/world_of_warcraft_avatar_history.html` → **500**; `https://mmnet.iis.sinica.edu.tw/dl/wowah/` → no connection (curl 000) |
| 27 | 2026-10-07 | WebSearch | `dataset PC game play session durations telemetry public download` | researchdata.gla.ac.uk/2227 Readme.md; eprints.soton.ac.uk/377465 (IdleWars) | `https://eprints.soton.ac.uk/377465/` → **401** |
| 28 | 2026-10-07 | WebSearch | `SWELL-KW dataset computer interaction logging application switches DANS` | cs.ru.nl SWELL-KW pages, ICMI 2014 paper, DANS (ssh.datastations.nl) dataset API, arXiv 2404.10505 (RLKWiC) | — |
| 29 | 2026-10-07 | WebSearch | `BEHACOM dataset keyboard mouse application statistics resource consumption Mendeley Data` | PMC7270191, Mendeley Data cg4br62535 v2 | — |
| 30 | 2026-10-07 | Zenodo REST API `https://zenodo.org/api/records?q=…&size=8` | `"World of Warcraft" avatar history`; `game session length`; `gaming session duration dataset`; `application usage log desktop`; `SWELL knowledge work`; `computer interaction logging window switching`; `active window log dataset` | none relevant (top 8 of each were off-topic) | `steam playtime sessions` → curl (35) SSL_ERROR_SYSCALL (connection reset) |
| 31 | 2026-10-07 | cseweb.ucsd.edu | `https://cseweb.ucsd.edu/~jmcauley/datasets.html` (Steam Video Game and Bundle Data) | 1 page | — |
| 32 | 2026-10-07 | kaggle.com | `https://www.kaggle.com/datasets` (reachability probe only) | 200 | Not used: Kaggle downloads need a login |
| 33 | 2026-10-08 | git (stage 3) | `git clone https://github.com/CachyOS/ananicy-rules` (full history) | HEAD `03ef03fb`, 2 762 commits → S3-19 | — |
| 34 | 2026-10-08 | codesearch.debian.net (stage 3) | `^\[Service\] path:\.service` grouped, all 319 pages, first sequentially (13 min), then in one burst; the same with `-path:(^\|/)(tests?\|testsuite\|testdata\|examples?\|samples?\|demos?\|contrib\|docs?)/` (301 pages, the first burst inconsistent, the second consistent); `^\s*Nice=`, `^\s*IOSchedulingClass=`, `^\s*CPUSchedulingPolicy=` with `path:\.service`, with and without that filter | → S3-20 | the sequential read spanned a re-run of the query |
| 35 | 2026-10-08 | deb.debian.org (stage 3) | `dists/sid/Release`; `main/Contents-amd64.gz`, `main/Contents-all.gz`, `main/binary-amd64/Packages.xz`, `main/binary-all/Packages.xz` | 200; each SHA-256 equal to Release's → S3-20 | — |
| 36 | 2026-10-09 | local copies (stage 3) | the campaigns' downloaded artifacts under `~/.cache/meas-loop` (2 028 `report.json`, 2 259 `perf.*.timehist.txt.gz`): every gate-open EPYC 7763 repeat's timehist files, counted per CPU (A.17) | → S3-21 | — |
| 37 | 2026-10-09 | WebSearch (standard); usenix.org (stage 3) | `measured PC game play session length distribution study Steam telemetry hours per session`; the IMC '05 paper's HTML (`index`, `node2`, `node3`, `node5`) | 200 → S3-23; the other results — arXiv 1703.04696 ("On Quitting", platform not stated in the snippet), the AAU/Fraunhofer "Playtime Principle" (total playtime, not sessions), a developer's blog, a 2009 Nielsen report, Statista (a survey) — not read | — |
| 38 | 2026-10-09 | own run (stage 3) | the development Mac: llama.cpp at `bd4eeaa0` built with Metal; the two GGUF files of `meas-ci:costs` (D31); `sources/S3-22/m1_run.sh` (A.18), five repeats | → S3-22 | — |

---

## 2. Candidates

(Id S3-14 was assigned to the IdleWars record at eprints.soton.ac.uk/377465, which returned 401. It has no copy and is not a candidate, so the numbering skips it.)

### S3-01 — Debian Code Search: units and C sources in Debian that declare an idle/batch/nice/I-O class (T7)

- **Citation.** Debian Code Search, https://codesearch.debian.net/ (dcs-web commit `7c71293812877aa110d277a9b747b2d29485c65a`, as printed in the page footer). It indexes the current Debian unstable source packages. The package versions in the hits (e.g. `systemd_262-1`, `e2fsprogs_1.47.4-1`, `plocate_1.1.25-1`) identify the snapshot.
- **Copy read.** No-JS HTML result pages fetched on 2026-10-07 with `dcs.sh` (Appendix A.1). Queries q01–q09 used the first version of the script, without `--retry`; q10–q12 used the version shown. Saved under `sources/S3-01/qNN_*/page_N.html`. Per-query manifests are `sources/S3-01/qNN_*.sha256`; the SHA-256 of each manifest:

| Query dir | Query | Mode | Pages | SHA-256 of manifest |
|---|---|---|---|---|
| q01_cpuidle_unit | `CPUSchedulingPolicy=idle path:\.(service\|timer)` | literal | 2 | d2299d91e0c519c83e6b32617b1fac7057630622e3dbdb75c8687eeb628fcad0 |
| q02_cpuidle_all | `CPUSchedulingPolicy=idle` | literal | 3 | 2e9a7d8721ef8b809bf237b55fbdbcb069b294499d89308a43e11e523d690c8c |
| q03_cpubatch_unit | `CPUSchedulingPolicy=batch path:\.(service\|timer)` | literal | 1 | a8eda383005e2775d1591418cbe75a1281aee178dbfa8d06673a77a80a1b577b |
| q04_nice19_unit | `Nice=19 path:\.(service\|timer)` | literal | 4 | 3d7b36c5eb044fa042448e8a47942967debdf11206df61e7838abac080531b15 |
| q05_ioidle_unit | `IOSchedulingClass=idle path:\.(service\|timer)` | literal | 4 | 19730ca89ff3493aedeec2b80a93495a4eab9d90529700bbfaeb55ec756b2712 |
| q06_io3_unit | `IOSchedulingClass=3 path:\.(service\|timer)` | literal | 1 | cb7f43b0b160715c88ff9ee8752c41b10ea62dba1666596ebc9c0ccc70c879c0 |
| q07_cpupolicy_any_unit | `CPUSchedulingPolicy= path:\.(service\|timer)` | literal | 5 | 5e4b5b8fdb47aee21b5a21c08cb93a0026e2e09dac13fa6eaea599e876a00a5d |
| q08_nice_any_unit | `^\s*Nice= path:\.(service\|timer)` | regex | 7 | 0af6d44c1debb21b57d3e2f9fb718b4988f9c51eff51ddcf73cedded4bf17a42 |
| q09_ioclass_any_unit | `IOSchedulingClass= path:\.(service\|timer)` | literal | 8 | e1e98c79538e1e5f85722d78e2b1361450154241a34d3fa63e19479b2071483b |
| q10_sched_idle_c | `SCHED_IDLE path:\.(c\|cc\|cpp\|h)$` | literal | 34 | 1a37730d2ccdd7e26a5ace2d62fe807cae848407b799ddf681e9a39d5bec6220 |
| q11_denominator | `^\[Service\] path:\.service` (perpkg=1; pages 0, 1, 318) | regex | 3 fetched | dc8108d6de04fcbf33e01b26fe97279c6f612c404b183ab90dbbe8332a5b30bd |

  Note: the `path:` filter is a regex on the file path, so `\.service` also matches `.service.in` templates.
- **Computed counts** (`python3 -I parse.py <dir>`, Appendix A.2; the first three output lines are verbatim). Lines whose matched text starts with `#` or `;` count as "commented".

```
== q01_cpuidle_unit
hits 16 files 16 packages 10 | uncommented hits 16 packages(uncommented) 10
packages: apt-xapian-index btrfsd btrfsmaintenance bumblebee e2fsprogs radvd rtags rust-rebuilderd-worker snapper xfsprogs
== q02_cpuidle_all
hits 28 files 26 packages 13 | uncommented hits 28 packages(uncommented) 13
packages: apt-xapian-index btrfsd btrfsmaintenance bumblebee debian-reference e2fsprogs manpages-l10n radvd rtags rust-rebuilderd-worker snapper systemd-cron xfsprogs
== q03_cpubatch_unit
hits 3 files 3 packages 2 | uncommented hits 3 packages(uncommented) 2
packages: borgmatic grokmirror
== q04_nice19_unit
hits 35 files 35 packages 26 | uncommented hits 35 packages(uncommented) 26
packages: apt-show-versions apt-xapian-index borgmatic codelite debusine dnf dnf5 exim4 findutils hw-probe kanboard lighttpd logrotate lynis mailgraph man-db openqa openqa-server pk4 plocate privoxy rtags storebackup universal-ctags wtmpdb xfsprogs
== q05_ioidle_unit
hits 39 files 37 packages 20 | uncommented hits 39 packages(uncommented) 20
packages: apt-listchanges apt-xapian-index boinc btrfsd btrfsmaintenance clsync duply e2fsprogs etckeeper findutils flatpak hw-probe man-db ntpsec pk4 plocate snapper systemd systemd-udeb xfsprogs
== q06_io3_unit
hits 3 files 3 packages 3 | uncommented hits 3 packages(uncommented) 3
packages: codelite rust-rebuilderd-worker universal-ctags
== q07_cpupolicy_any_unit
hits 49 files 49 packages 22 | uncommented hits 45 packages(uncommented) 21
packages: apt-xapian-index borgmatic btrfsd btrfsmaintenance bumblebee coturn e2fsprogs grokmirror hipercontracer low-memory-monitor nohang osmo-bts osmo-mgw osmo-pcu osmo-trx radvd rtags rust-rebuilderd-worker snapper systemd systemd-udeb xfsprogs
== q08_nice_any_unit
hits 68 files 68 packages 48 | uncommented hits 68 packages(uncommented) 48
packages: apt-show-versions apt-xapian-index boinc borgmatic brltty chkrootkit codelite debusine deepin-boot-maker deepin-log-viewer dnf dnf5 drkonqi earlyoom espeakup exim4 findutils frr gdnsd hdapsd hw-probe jacktrip jamulus kanboard lighttpd logcheck logrotate lynis mailgraph man-db openqa openqa-server pk4 plocate privoxy railcontrol rauc-hawkbit-updater readsb rtags sitesummary storebackup svxlink systemd systemd-udeb universal-ctags vdradmin-am wtmpdb xfsprogs
== q09_ioclass_any_unit
hits 80 files 71 packages 40 | uncommented hits 79 packages(uncommented) 39
packages: apt-listchanges apt-show-versions apt-xapian-index boinc borgmatic btrfsd btrfsmaintenance clsync codelite dnf dnf5 duply e2fsprogs etckeeper exim4 findutils flatpak hipercontracer hw-probe jacktrip jamulus kanboard keepalived lighttpd logrotate lynis man-db ntpsec pk4 plocate privoxy railcontrol rust-rebuilderd-worker snapper storebackup systemd systemd-udeb universal-ctags wtmpdb xfsprogs
== q10_sched_idle_c
hits 337 files 170 packages 93 | uncommented hits 211 packages(uncommented) 84
```

  For q10 (C sources) the "uncommented" heuristic means nothing, because `#define` and `#ifdef` lines start with `#`. Hits there include libc headers, kernels and process viewers that only define or print `SCHED_IDLE`; they are not callers that set the policy.

- **Value tabulations** (verbatim output; commands in Appendix A.3):

```
q07  CPUSchedulingPolicy= values over hits (count, value):
     19  CPUSchedulingPolicy=rr
     16  CPUSchedulingPolicy=idle
      4  #CPUSchedulingPolicy=rr
      3  CPUSchedulingPolicy=batch
      2  CPUSchedulingPolicy=fifo
      2  CPUSchedulingPolicy=ext
      2  CPUSchedulingPolicy=
      1  CPUSchedulingPolicy=other
q08  Nice= values over hits (count, value):
     35  Nice=19
      8  Nice=-5
      7  Nice=10
      6  Nice=-10
      4  Nice=9
      4  Nice=-20
      2  Nice=
      1  Nice=-11
      1  Nice=-1
```

  The rr/fifo/ext hits come from systemd's own tests (`systemd_262-1/test/test-sched-prio/…`), osmo-bts/osmo-mgw/osmo-pcu/osmo-trx (`contrib/systemd/*.service`, `debian/*.service`), `hipercontracer_2.2.10-1/src/udp-echo-server.service:46` and `low-memory-monitor_2.1-3/data/low-memory-monitor.service.in:12` (fifo). Negative `Nice=` hits are listed in full in Appendix B.1. Examples: `earlyoom_1.9.0-1/earlyoom.service.in:12 | Nice=-20`, `jamulus_3.9.1+dfsg-2/linux/debian/jamulus-headless.service:13 | Nice=-20`, `brltty_6.9.1+repack-2/debian/brltty.service:30 | Nice=-10`, `systemd_262-1/debian/extra/units-ubuntu/systemd-journald.service.d/nice.conf:4 | Nice=-1`.

- **Denominator.** Grouped view of `^\[Service\] path:\.service` (regex, perpkg=1). Page 0 shows the pagination string `… <a …page=318">319</a>`. Each grouped page lists 5 packages, and page 318 (the last) lists 3 (`smartdns`, `kylin-ai-runtime`, `debiman`). Verbatim command output:
  ```
  h2 package headers on page 1:
  5
  ...
  h2 package headers on page 318:
  3
  <h2>All results <h2>Results by package <h2>Search Results by package for "^\[Service\] path:\.service" <h2>smartdns <h2>kylin-ai-runtime <h2>debiman
  5   (page 0)
  ```
  That gives 318×5+3 = **1,593 source packages** with at least one file whose path matches `\.service` and that has a line beginning `[Service]`. I assumed stable paging and did not fetch all 319 pages. On that denominator: CPUSchedulingPolicy=idle in a unit, 10 packages (0.6%); Nice=19, 26 (1.6%); IOSchedulingClass=idle, 20 (1.3%); any `Nice=`, 48 (3.0%); any `IOSchedulingClass=`, 40 (2.5%). These percentages are my arithmetic. The numerator also counts example, contrib and test units, and the denominator excludes packages missing from the index (e.g. `clamav`; see search log row 12).
- **Verbatim passages** (DCS hit lines, `file:line | matched line`, from q04/q05):
  - `plocate_1.1.25-1/plocate-updatedb.service.in:8 | IOSchedulingClass=idle` and `…:9 | Nice=19`
  - `findutils_4.11.0-3/debian/locate.service:9 | Nice=19`, `…:10 | IOSchedulingClass=idle`
  - `man-db_2.13.1-1/init/systemd/man-db.service.in:13 | Nice=19`, `…:14 | IOSchedulingClass=idle`
  - `systemd_262-1/units/systemd-tmpfiles-clean.service:23 | IOSchedulingClass=idle`
  - `xfsprogs_7.2.0-1/scrub/xfs_scrub@.service.in:30` context: `# Run scrub with minimal CPU and IO priority so that nothing else will starve.` / `IOSchedulingClass=idle` / `CPUSchedulingPolicy=idle` / `CPUAccounting=true` / `Nice=19`
  - `radvd_1:2.20-1/radvd.service.in:20` context: `# Set the CPU scheduling policy to idle which is for running very low priority background jobs` / `CPUSchedulingPolicy=idle`
  - `borgmatic_2.0.11-2/sample/systemd/borgmatic.service:64 | CPUSchedulingPolicy=batch`
  - q10 (C): `kf6-baloo_6.30.0-1/src/file/priority.cpp:65 | return !sched_setscheduler(0, SCHED_IDLE, &param);`; `localsearch_3.12.0-1/src/indexer/tracker-main.c:95 | if (pthread_setschedparam (pthread_self(), SCHED_IDLE, &sp) < 0)`; `tumbler_4.20.2-1/tumblerd/tumbler-scheduler.c:332 | sched_setscheduler (0, SCHED_IDLE, &sp);`; `recoll_1.43.16-1/index/recollindex.cpp:212 | sched_setscheduler(getpid(), SCHED_IDLE, &param);`; `akonadi-search_4:26.04.3-3/agent/priority.cpp:96 | return !sched_setscheduler(0, SCHED_IDLE, &param);`; `boinc_8.2.15+dfsg-10/client/app_start.cpp:1116 | if (sched_setscheduler(0, SCHED_IDLE, &sp)) {`; `pinot_1.24-1/Core/pinot-dbus-daemon.cpp:392 | else if (sched_setscheduler(0, SCHED_IDLE, &schedParam) == -1)`.
- **Coverage.**
  - T7 covered. Object: Debian unstable source packages. Unit: source package, file and line. Statistic: count of packages and files containing each directive in a `.service`/`.timer`(/.in) path, plus a denominator of 1,593 packages with a `[Service]` unit file. Scope: Debian main source as indexed by DCS on 2026-10-07. Population: all indexed source packages (packages missing from the index excluded). This is one observation (one index snapshot, window = access date), not a machine. It counts declarations in source, not what is installed or enabled on any system.
  - Other topics: does not cover.

### S3-02 — Debian source files of desktop background tools (T7, per-tool declarations)

- **Citation.** Debian sources archive, https://sources.debian.org/data/main/… (versions in the file names below), accessed 2026-10-07.
- **Copy read** (`sources/S3-02/`, SHA-256):
  - plocate 1.1.25-1 `plocate-updatedb.service.in`: d8867da6abc3e7062679c51c8b7e46d8f9484c337b127a0efe97410e0bede5a7
  - findutils 4.11.0-3 `debian/locate.service`: 48cb7fe113e740ac879f59cc5508c70a461b4c5885ffe240166855fab54e7b3f
  - localsearch 3.12.0-1 `src/indexer/tracker-miner-fs.service.in`: aef73d13f1229fd9a494385078e7595dfe55b542579da0b859ccac53da4d7eb4
  - localsearch 3.12.0-1 `src/indexer/tracker-main.c`: bf0bf720467204e003ad50ccfdd5530211664574714755a3d37e342041d0bf5a
  - kf6-baloo 6.30.0-1 `src/file/kde-baloo.service.in`: 68da2312f10da6986108515e28001bc9d4f753cee0441f9dd71036f098ca44d3
  - kf6-baloo `src/file/priority.cpp`: b6df2a1172131df3fec91fbf5fb254909dd6abe282b339b35f8b90739109d7d5
  - kf6-baloo `src/file/main.cpp`: 8eef78475cd3dad766137ef9efd2e73624b7f3de216463e459e9fed0dd788bab
  - kf6-baloo `src/file/extractor/main.cpp`: 69cf06518045f5c5b2d13c06f1678684faeb89542776c37c9955cdfa93e2acf9
  - tumbler 4.20.2-1 `tumblerd/tumbler-scheduler.c`: d7b47cce25b3f89b3eb364123a06f54612afe0acfdd17fa3f45451489246a75d
  - recoll 1.43.16-1 `index/recollindex.cpp`: 4aa4829007344ad10c8b1484e33348025c860d7c20a4a9b9eb228652826619a6
  - akonadi-search 4:26.04.3-3 `agent/priority.cpp`: 9fc0476e7a592570b23519ed96da1d7fdc3262c133fd27110aeff3b89ab935cf
  - clamav 1.4.6+dfsg-1 `clamd/clamav-daemon.service.in`: e0bd83bb1bb454bdb7a374c276a4a840476a2525b9926bd771d8fa1741d241ff
  - clamav `freshclam/clamav-freshclam.service.in`: eaefe47e09e594d77c12c5c3d0f936f989d4db5976bf4cbaebfb48f43f3efdb1
  - clamav `clamonacc/clamav-clamonacc.service.in`: 2bdb09552829872b358bab42b0102bb030c9ab9e10bbbaa9add5e22619cf72a5
- **Verbatim passages.**
  - `plocate-updatedb.service.in:4-9`: `[Service]` / `Type=oneshot` / `ExecStart=@sbindir@/@updatedb_progname@` / `LimitNOFILE=131072` / `IOSchedulingClass=idle` / `Nice=19`
  - `findutils debian/locate.service:6-11`: `[Service]` / `Type=oneshot` / `ExecStart=/etc/cron.daily/locate systemd-timer` / `Nice=19` / `IOSchedulingClass=idle` / `IOSchedulingPriority=7`
  - `localsearch tracker-miner-fs.service.in:7-12`: `[Service]` / `Type=notify` / `BusName=org.freedesktop.LocalSearch3` / `ExecStart=@libexecdir@/localsearch-3` / `Restart=on-failure` / `Slice=background.slice` (no Nice/CPUSchedulingPolicy/IOSchedulingClass in the unit)
  - `localsearch tracker-main.c:84`: `TRACKER_NOTE (CONFIG, g_message ("Setting scheduler policy to SCHED_IDLE"));`; `:95`: `if (pthread_setschedparam (pthread_self(), SCHED_IDLE, &sp) < 0)`; `:100-102`: `ioprio = 7; /* priority is ignored with idle class */` / `ioclass = IOPRIO_CLASS_IDLE << IOPRIO_CLASS_SHIFT;` / `if (syscall (SYS_ioprio_set, IOPRIO_WHO_PROCESS, 0, ioprio | ioclass) < 0)`; `:106-107`: `TRACKER_NOTE (CONFIG, g_message ("Setting priority nice level to 19"));` / `if (nice (19) < 0)`
  - `kf6-baloo kde-baloo.service.in:8-12`: `Slice=background.slice` / `ExecCondition=…` / `# We'll basically only want to consume resources if they aren't needed anywhere else, hence weights are way low.` / `CPUWeight=1` / `IOWeight=1`
  - `kf6-baloo priority.cpp:27`: `if (syscall(SYS_ioprio_set, IOPRIO_WHO_PROCESS, 0, ioprio_value(IOPRIO_CLASS_IDLE, 0, IOPRIO_HINT_NONE)) >= 0) {`; `:44`: `return !setpriority(PRIO_PROCESS, 0, 19);`; `:53`: `return !sched_setscheduler(0, SCHED_BATCH, &param);` (in `lowerSchedulingPriority()`); `:65`: `return !sched_setscheduler(0, SCHED_IDLE, &param);` (in `setIdleSchedulingPriority()`)
  - `kf6-baloo src/file/main.cpp:28-30`: `lowerIOPriority();` / `lowerSchedulingPriority();` / `lowerPriority();`. `src/file/extractor/main.cpp:21-23`: `lowerIOPriority();` / `setIdleSchedulingPriority();` / `lowerPriority();`. So the indexer daemon uses SCHED_BATCH and the extractor uses SCHED_IDLE, and both use nice 19 and the idle I/O class.
  - `tumbler-scheduler.c:325-332`: `ioprio = 7; /* priority is ignored with idle class */` / `ioclass = IOPRIO_CLASS_IDLE << IOPRIO_CLASS_SHIFT;` / … / `sched_setscheduler (0, SCHED_IDLE, &sp);`
  - `recollindex.cpp:208-212`: `// By default, or if the user has set idxniceprio > 19, use SCHED_IDLE if available.` / `if (prio > 19) {` / … / `sched_setscheduler(getpid(), SCHED_IDLE, &param);`
  - `akonadi-search agent/priority.cpp:96`: `return !sched_setscheduler(0, SCHED_IDLE, &param);`
  - `clamav-daemon.service.in:9-13`: `[Service]` / `ExecStart=@prefix@/sbin/clamd --foreground=true` / `# Reload the database` / `ExecReload=/bin/kill -USR2 $MAINPID` / `TimeoutStartSec=420`. `clamav-freshclam.service.in:9-10`: `[Service]` / `ExecStart=@prefix@/bin/freshclam -d --foreground=true`. `clamav-clamonacc.service.in:10-15`: `[Service]` / `Type=simple` / `User=root` / `ExecStartPre=…` / `ExecStart=@prefix@/sbin/clamonacc -F --log=/var/log/clamav/clamonacc.log --move=/root/quarantine` / `ExecStop=/bin/kill -SIGKILL $MAINPID`. None of the three ClamAV units sets Nice, CPUSchedulingPolicy or IOSchedulingClass.
- **Coverage.** T7 covered. Object: per-tool declarations. Unit: the directive or call in a named file:line at a named Debian version. Population: plocate, findutils locate, localsearch (Tracker 3), Baloo (KF6), tumbler, recoll, akonadi-search, ClamAV. Not searched: mlocate (no Debian unstable source per DCS query 12), deja-dup, borgbackup, timeshift, backintime (DCS found no `.service` unit for them). Each item is one observation per file version. Other topics: does not cover.

### S3-03 — CachyOS ananicy-rules catalogue (T7 counts over a rules catalogue; T8 by content)

- **Citation.** CachyOS, ananicy-rules, https://github.com/CachyOS/ananicy-rules, commit `03ef03fbf7e834385377432ccecaedd32e3414bb` (2026-09-08T19:11:25-03:00, "Merge pull request #605 from Tiagoquix/samp").
- **Copy read.** `git clone --depth 1` on 2026-10-07 into `sources/S3-03/ananicy-rules/`. SHA-256: `00-types.types` 667d89cb61a949ac9b6595f2f318dc452b65c735d8cd6d4fcd5f934dc940591d; `README.md` 0886ec1f23a1ef772e676ba65bc13961ce7942bec6e0dc9d0936a4f60b16b7ed; `00-default/System Utilities & Maintenance/clamav.rules` 14709997d06ba912f4367ee968496615aabf087eab4fe279a8d1941c5663e006; `00-default/DEs-and-WMs/plasma.rules` 090a8f88fb82a3be2699d762d431f80814e4bb466a8ea1ea467039001cc56800; `00-default/DEs-and-WMs/gnome.rules` 4cd43aab6cd3170348c0d36d53195cef6b9ef884b6cc101c1c2c324f879fce23; `…/borg.rules` 594126ae9ca6f6a607c8fbbad54f52cae42f65051ac5ed1e0191d71d744f07d5; `…/restic.rules` c1d472c5215562c37a991b7186445876d17e702e081dd5acc835029b34c22431; `…/recoll.rules` 50418dc6b0d8d0653cfe37492726868d56a10a0de79bc9f6bdc8cbfb03d535de; `00-default/Networking/syncthing.rules` d44cd25238421653d1d446407756a07182a9b375d0e159fffc018587710296e4; `00-default/Tools/rsync.rules` ecd9608546e9915a38700fea3ec8d590b417a501dcc017942659db21c48d038a; `…/thrash-protect.rules` fc797eb60f34e11b1d05c8c20a9d1d7aa75e9150540a384d4a16b8dec0f028d2.
- **Verbatim passages** (`file:line` at 03ef03fb).
  - `00-types.types:4`: `{ "type": "Game", "nice": -5, "ioclass": "best-effort", "sched": "normal" }`
  - `00-types.types:20-22`: `# Type: BackGround CPU/IO Load` / `# Background CPU/IO it's needed, but it must be as silent as possible` / `{ "type": "BG_CPUIO", "nice": 16, "ioclass": "idle", "sched": "idle" }`
  - `00-types.types:18`: `{ "type": "LowLatency_RT", "nice": -12, "ioclass": "best-effort" }`; `:39`: `{ "type": "Service", "nice": 10, "ioclass": "best-effort", "ionice": 6 }`; `:33`: `{ "type": "Heavy_CPU", "nice": 9, "ioclass": "best-effort", "ionice": 7 }`
  - `README.md:3`: `This is a ananicy-cpp-rules collection for ananicy-cpp maintained by the CachyOS team and the community.`; `README.md:22`: `You can add your favorite games, apps, and more. Any help would be greatly appreciated!`; `README.md:44-45`: `# Just Cause 2 https://store.steampowered.com/app/8190/Just_Cause_2/` / `{ "name": "JustCause2.exe", "type": "Game" }`
  - `00-default/System Utilities & Maintenance/clamav.rules:1-4`: `# ClamAV Daemon` / `{ "name": "clamd", "type": "BG_CPUIO" }` / `# ClamUI` / `{ "name": "clamui", "type": "Service" }`
  - `00-default/DEs-and-WMs/plasma.rules:10-14`: `# https://community.kde.org/Baloo` / `# Baloo is the file indexing and file search framework for KDE.` / `{ "name": "baloo_file", "type": "BG_CPUIO" }` / `{ "name": "baloorunner", "type": "BG_CPUIO" }` / `{ "name": "baloo_file_extractor", "type": "BG_CPUIO" }`
  - `…/borg.rules:2`: `{ "name": "borg", "type": "BG_CPUIO" }`; `…/restic.rules:2`: `{ "name": "restic", "type": "BG_CPUIO" }`; `…/recoll.rules:2`: `{ "name": "recollindex", "type": "BG_CPUIO" }`; `…/kopia.rules:2-3`: `{ "name": "kopia", "type": "BG_CPUIO" }` / `{ "name": "kopia-ui", "type": "BG_CPUIO" }`; `Networking/syncthing.rules:2`: `{ "name": "syncthing", "type": "BG_CPUIO" }`; `Tools/rsync.rules:1`: `{ "name": "rsync", "type": "BG_CPUIO" }`
  - `DEs-and-WMs/gnome.rules:1-2`: `# http://live.gnome.org/ThumbnailerSpec ` / `{ "name": "tumblerd", "type": "TODO" }`
  - `System Utilities & Maintenance/thrash-protect.rules:2`: `{ "name": "thrash-protect", "nice": -12, "ioclass": "realtime" }`; `DEs-and-WMs/plasma.rules:29`: `{ "name": "plasmashell", "nice": -6 }`
- **Computed counts** (`python3 -I ananicy_count.py sources/S3-03/ananicy-rules`, Appendix A.4; verbatim output in Appendix B.2, summary):
  ```
  rules files 361 entries 15813 unparseable 1
  entries per type: Game 13528, BG_CPUIO 1615, Service 194, Doc-View 160, LowLatency_RT 109, Chat 51, Heavy_CPU 33, Image-View 32, Player-Audio 28, Launcher 24, Player-Video 24, IN_DIFF 10, OOM_NO_KILL 2, (no type: explicit fields) 2, TODO 1
  ```
  The one unparseable line is `00-default/Games/linux-native/linux-native_d.rules:315`: `{ "name": "Dungeon Drafters.x86_64", "type": "Game" }+` (trailing `+`). Of the 15,813 entries, 15,093 sit under `00-default/Games` (13,528 of type Game). Name search for indexers, updatedb, backup and antivirus (regex in A.4) found baloo_file/baloorunner/baloo_file_extractor, clamd, borg, restic, recollindex, syncthing, rsync and kopia, all **BG_CPUIO**. `clamui` is **Service** and `tumblerd` is `"TODO"`. No entry matched `updatedb`, `locate`, `tracker`, `localsearch` or `freshclam`. Other regex hits were game executables (listed in B.2).
- **Coverage.**
  - T7 covered. Object: a rules catalogue. Unit: rule entry (one JSON line). Statistic: count per type. Scope: the whole repository at one commit. Population: every `.rules` file. One observation (one commit); no machine.
  - T8: covers by content what a rule matches on (`"name"`, the process name) and sets (type → nice/ioclass/sched). How entries are added is quoted from README. T8 is not my class topic.
  - Other topics: does not cover.

### S3-04 — Hugging Face optimum-benchmark LLM-Perf Leaderboard dataset (T11)

- **Citation.** optimum-benchmark, "llm-perf-leaderboard" dataset, https://huggingface.co/datasets/optimum-benchmark/llm-perf-leaderboard, revision `94a9713e1842c87029a1dcc829e0003533a6d275` (lastModified 2024-12-13T10:07:03.000Z per the API).
- **Copy read.** `api.json` (SHA-256 6e574427f695cb21fa7f9cb630d34c76562c783ae0b9c946833f57c2f58fcab0) and `data/perf-df-pytorch-cuda-awq-1xT4.csv` at that revision (12,278,222 bytes, SHA-256 268adc57b15d3b97e1778c152c1496d9c42f75464a5a03a90511818ab7f7270b), in `sources/S3-04/`. Other files in the dataset are named for hardware: `…-1xA10`, `…-1xA100`, `…-1xT4`, `…-32vCPU-C7i` (datacenter GPUs and AWS server CPU).
- **Verbatim passage.** The CSV record ending at physical line 4509, with column=value pairs printed by Appendix A.5:
  ```
  config.name = '4bit-awq-gemv-sdpa'
  config.backend.model = 'meta-llama/Llama-3.1-8B-Instruct'
  config.backend.version = '2.4.1+cu124'
  config.scenario.input_shapes.batch_size = '1'
  config.scenario.input_shapes.sequence_length = '256'
  config.scenario.generate_kwargs.max_new_tokens = '64'
  config.environment.cpu = ' Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz'
  config.environment.gpu = "['Tesla T4']"
  config.environment.platform = 'Linux-5.10.225-213.878.amzn2.x86_64-x86_64-with-glibc2.35'
  report.prefill.latency.unit = 's'
  report.prefill.latency.mean = '0.3676786682128906'
  report.prefill.latency.p50 = '0.3678643798828125'
  report.decode.latency.mean = '2.0179779541015628'
  report.decode.throughput.unit = 'tokens/s'
  report.decode.throughput.value = '31.219369801316113'
  report.per_token.latency.mean = '0.032026476781330415'
  ```
  The file holds 1,362 rows, 427 with a prefill latency (`rows 1362 with prefill latency 427`). For Llama-3/3.1-8B AWQ 4-bit on the T4, the 24 rows give prefill means of 0.21–3.25 s and decode throughput of 22.0–33.5 tokens/s across kernel variants (Appendix B.3; min/max computed with a regex over the B.3 output).
- **Coverage.**
  - T11 covered, partly. Object: latency of a 4-bit (AWQ) 8B model. Units: s (prefill), tokens/s (decode). Statistic: mean/p50 over iterations. Scope: batch 1, 256 input tokens, 64 new tokens. Each row is one benchmark config. Machine named: Tesla T4 with Xeon Platinum 8259CL, an AWS datacenter GPU. Not a consumer CPU/GPU and not llama.cpp/Ollama/vLLM; PyTorch backend, 2024 data.
  - Other topics: does not cover.

### S3-05 — LocalScore public results database (T11)

- **Citation.** LocalScore (a Mozilla Builders project), https://www.localscore.ai/, accessed 2026-10-07.
- **Copy read** (`sources/S3-05/`, SHA-256): `about.html` 3fffc1e033945eae9bf03ae17934704a36e837ba3db44c0ba86849a5ce9cacac; `index.html` 3107be67d3f4d6378c8b70986d2557b20b8dbd29aaf19d5c2f311266be0d0174; `latest.html` c9fd095810ef8382b1514e928f9cbdf5079a62eee4ccac4fa885f40a3e400661; `download.html` a7821688a963c26bf991f2220a5f53e50d1b387b48ce20b4583efffe978d2db2; `model_1.html` 54146204e5a0c4e5da5aafb3ca02ec59ffb20570737edb212ff84cdfe8589ee2; `model_2.html` 44fe13b105be3bc0059b5903280e68bc74fe4938b1e2d6b94615b932147519e5; `model_3.html` 4de495d8560b9e613c5d03eba9aac12bc05544d01f2f10174eeab433e735fdde; `accelerator_349.html` c3167525ba9c6a3bd0f23d040252eb68c5cf3d43012174d85cfaeb349d47b6fb; `accelerator_43.html` 09b35df8a91ef99af30ba3e0c4fc05abc97f554e33a92ab19f41827e4001582b; `result_4246.html` ce3e705680852173656f2a4e2aaa430dcd4a34ac54f5a74bce9d079be98654fd; `result_4252.html` 54aefbc5371a96c5ba78d6246254645f8224ea139865c7350ff5f28196545994; `result_4254.html` 197ddbd9af49c82448616defc9c3849d3c463c5b7f34207f4ef3d0261b9ff5a5; `result_4255.html` 4b4d25f8485c2fb8e0d10643d607e2f19beb3a6d24a488b9fef2cd1155e05c02. The data was read from each page's embedded `__NEXT_DATA__` JSON.
- **Verbatim passages.**
  - `/about`: "LocalScore is an open-source benchmarking tool designed to measure how fast Large Language Models (LLMs) run on your specific hardware. It is also a public database for the benchmark results." … "Time to First Token:The latency before the first response appears (milliseconds)" … "Under the hood, LocalScore leverages Llamafile to ensure portability across different systems". Test table (rendered text): "1024tokens 16tokens Classification, sentiment analysis, keyword extraction." (that is, 1024 prompt tokens, 16 generated). The site reports nine tests, from pp1024+tg16 to pp16+tg1536. "We collect the following non personally identifiable system information: Operating System Info: Name, Version, Release CPU Info: Name, Architecture RAM Info: Capacity GPU Info: Name, Manufacturer, Total Memory".
  - `/result/4252`, test pp1024+tg16 (JSON verbatim): `{"id":38260,"benchmark_run_id":4252,"name":"pp1024+tg16","n_prompt":1024,"n_gen":16,"avg_time_ms":1106.549945,"power_watts":0,"prompt_tps":1264.59026,"gen_tps":53.908791,"prompt_tps_watt":0,"gen_tps_watt":0,"ttft_ms":828.379409,"created_at":"2026-10-07 12:08:43"}`. Same run: accelerator `NVIDIA GeForce GTX 1070`; model `{'name': 'qwen2.5-3b-instruct', 'quant': 'Q4_K - Medium', … 'params': 3397103616}`; system `cpu_name: 'Intel Core i7-7700K CPU @ 4.20GHz (skylake)', ram_gb: 31.1, kernel_type: 'Linux', kernel_release: '6.17.13-21-pve'`; runtime `llamafile 0.9.3`.
  - `/result/4255`, test pp1024+tg16: `{"id":38287,"benchmark_run_id":4255,"name":"pp1024+tg16","n_prompt":1024,"n_gen":16,"avg_time_ms":3614.8654,"power_watts":0,"prompt_tps":322.521889,"gen_tps":36.373184,"prompt_tps_watt":0,"gen_tps_watt":0,"ttft_ms":3202.4788,"created_at":"2026-10-07 20:05:10"}`. Accelerator `AMD Ryzen AI 9 HX 470 w/ Radeon 890M`, type CPU; model `Llama 3.2 1B Instruct`, `Q4_K - Medium`; `kernel_type: 'Windows', kernel_release: '10.0'`; `llamafile 0.9.3`. The same run's pp64+tg1024 test: `ttft_ms 256.8712 gen_tps 36.613062` (printed by Appendix A.6).
  - `/result/4246` (CPU `Intel Core i7-14700HX (alderlake)`, Linux `6.1.0-53-amd64`, model name `'..'`, `Q4_0`, 1.10B params): pp1024+tg16 `ttft_ms 3593.630016 gen_tps 57.196733`.
  - `/model/1` aggregate for one accelerator: `{"avg_prompt_tps":93.41267666666666,"avg_gen_tps":10.939956444444444,"avg_ttft":14656.055673111114,"performance_score":41.15931147695306,"performance_rank":200,"number_ranked":417,"accelerator":{"name":"AMD Ryzen 7 7800X3D 8-Core Processor (znver4)","type":"CPU","id":349,"memory_gb":31,…}}` and `{"avg_prompt_tps":1482.5665064537036,"avg_gen_tps":51.28081109259259,"avg_ttft":881.7180316018517,…,"accelerator":{"name":"NVIDIA GeForce RTX 3060","type":"GPU","id":43,"memory_gb":12,…}}` (model: Meta Llama 3.1 8B Instruct, Q4_K - Medium).
- **Computed summary** (`python3 -I localscore.py model_N.html …`, Appendix A.6; verbatim):
  ```
  {'name': 'Meta Llama 3.1 8B Instruct', 'quant': 'Q4_K - Medium', 'id': 1, 'variantId': 1, 'params': 8030263296}
  accelerator entries 417 by type Counter({'CPU': 233, 'GPU': 184})
  CPU n 233 avg_ttft ms median 40757 min 5437 max 1737533 | avg_gen_tps median 7.76 min 0.66 max 26.59
  GPU n 184 avg_ttft ms median 1583 min 176 max 31480 | avg_gen_tps median 37.91 min 1.31 max 120.98
  {'name': 'Llama 3.2 1B Instruct', 'quant': 'Q4_K - Medium', 'id': 3, 'variantId': 3, 'params': 1498483200}
  accelerator entries 869 by type Counter({'CPU': 641, 'GPU': 228})
  CPU n 641 avg_ttft ms median 7534 min 849 max 2959599 | avg_gen_tps median 34.73 min 0.32 max 156.30
  GPU n 228 avg_ttft ms median 405 min 53 max 11448 | avg_gen_tps median 116.69 min 5.91 max 410.76
  ```
  The per-accelerator `avg_ttft` averages the nine tests (prompts of 16–4,096 tokens), so it is dominated by long prompts. It is not the latency of a short prompt.
- **Coverage.**
  - T11 covered. Object: TTFT (ms) and generation speed (tokens/s) of Q4 GGUF models (1B, 3B, 8B, 14B) run with llamafile (llama.cpp-based) on consumer CPUs and GPUs. Statistic: per-test value per run, and per-accelerator averages. Population: crowd-submitted runs. A per-run record (`/result/N`) is one observation with machine (CPU/GPU name, RAM, OS kernel), model and date named. Aggregates are not single observations.
  - There is no structured or JSON-output test, and the shortest-prompt test is pp16+tg1536.
  - Other topics: does not cover.

### S3-06 — MLCommons MLPerf Client benchmark page (T11, metric definitions only)

- **Citation.** MLCommons, "MLPerf Client" benchmark page, https://mlcommons.org/benchmarks/client/ (describes v2.0), accessed 2026-10-07.
- **Copy read.** `sources/S3-06/client.html`, SHA-256 5aac529d091203540de2525a96d7ebb643f5098447f6195cf67b3c213f54a2df.
- **Verbatim passages** (section "What do the performance metrics mean?"): "Time to first token (TTFT): This the wait time in seconds before the system produces the first token in response to each prompt. In LLM interactions, the wait for the first output token is typically the longest one in the ensuing response. Following widespread industry practice, we have chosen to report this result separately." From the FAQ: "the benchmark actually runs each test four times internally in the default configuration files. There's one warm-up run and three performance runs. The application then reports the averages of the results of the three performance runs." From "What's new in MLPerf Client v2.0": "Transitioned select summarization tasks to structured JSON output tasks." Models list: "Llama 3.1 8B Instruct / Phi 4 Mini Instruct / Phi 4 Reasoning 14B* / Qwen 3 8B*".
- **Coverage.**
  - T11 covers the metric definitions for TTFT and TPS on client PCs, plus a structured-JSON task. It holds **no published results table**, so it gives no numbers.
  - Other topics: does not cover.

### S3-07 — Perfetto example trace `example_android_trace_15s` (T10)

- **Citation.** Perfetto project, example trace `example_android_trace_15s`, https://storage.googleapis.com/perfetto-misc/example_android_trace_15s (object last-modified "Wed, 11 Mar 2026 13:47:18 GMT", etag `"c724b58b0b6d104f37381fbdc0291647"`, x-goog-hash md5=xyS1iwttEE83OB+9wCkWRw==).
- **Copy read.** `sources/S3-07/example_android_trace_15s`, 57,202,082 bytes, SHA-256 7f6d973d06e478e1266a83f7cb7e59bcb41df90449f6cc7f59211e385b8fad92. Analysed with `trace_processor_shell` v58.2 linux-amd64 (SHA-256 58042408e6cc861fb1a731c26bb082dc222285561eaa4e12a48a8b2b90dca7b9, equal to the hash pinned in https://get.perfetto.dev/trace_processor).
- **Trace metadata** (verbatim output of `select name, str_value, int_value from metadata where name not like 'trace_config%';`):
  ```
  "system_name","Linux","[NULL]"
  "system_version","#1 SMP PREEMPT Wed Jun 12 20:42:24 UTC 2019","[NULL]"
  "system_release","4.4.177-g17696cf513dd","[NULL]"
  "system_machine","aarch64","[NULL]"
  "trace_size_bytes","[NULL]",57202082
  ```
  The embedded trace config contains `duration_ms: 15000`. The metadata does not name the device model.
- **Computed counts** (SQL in Appendix A.7; output verbatim):
  ```
  "start_ts","end_ts","dur_s"
  261187012114381,261201738290119,14.726176

  "cpu","slices","first_ts","last_end","slices_per_s","idle_slices"
  0,60207,261187012454537,261201738290119,4088.500000,16248
  1,44061,261187012574745,261201730885743,2993.600000,12518
  2,29892,261187012170995,261201712336887,2033.400000,9244
  3,26894,261187012460318,261201737248764,1826.400000,7362
  4,42409,261187012421099,261201734271160,2880.700000,13011
  5,39974,261187012640474,261201736962723,2714.800000,11210
  6,39731,261187013945787,261201735013452,2698.900000,8508
  7,41137,261187021438288,261201738020171,2795.300000,8238

  "total_slices","per_s_all_cpus"
  324305,22022.400000

  "n"            (select count(*) from ftrace_event where name='sched_switch')
  324305

  "nonidle_slices","median_dur_ns","mean_dur_ns"
  237958,56250,200117.991574
  ```
  So: 324,305 `sched_switch` events in 14.73 s on 8 CPUs, which is 22,022 per second in total and 1,826–4,089 per second per CPU. The median non-idle run slice is 56.25 µs and the mean 200 µs. ("idle_slices" counts slices of the tid-0 swapper thread.)
- **Coverage.**
  - T10 covered. Object: context switches (sched_switch events) per second per CPU, and run-slice lengths. Scope: one 14.7 s trace on one Android device (Linux 4.4.177, aarch64, 8 CPUs; model unnamed; 2019 kernel build; workload not described in the trace metadata). It is one observation. Machine partly named (kernel and arch only). Not a desktop or server, and not x86.
  - Other topics: does not cover.

### S3-08 — Google and Alibaba cluster traces: schemas (T10, negative)

- **Citation.** J. Wilkes et al., "Google cluster-usage traces v3" (schema document, "Original version 2020-04-01, updated 2020-05-01, 2020-07-28, 2020-08-10, 2020-08-18"), linked from https://github.com/google/cluster-data/blob/master/ClusterData2019.md. Google "cluster-usage traces: format + schema" (2011 trace, linked from ClusterData2011_2.md). Alibaba cluster-trace-v2018 `schema.txt` (https://github.com/alibaba/clusterdata).
- **Copy read** (`sources/S3-08/`, SHA-256): `google_2019_schema.pdf` 17267c7c634a6ee01146b8032bacc26d9c7354e7b3bdb6a48fc0cbb69f02d6f9 (16 pp.); `google_2011_schema.pdf` a1bd9dffe09157873c321a942bbcd66e50c454c22db6bac4316af3f6bdcab1a5 (14 pp.); `alibaba_v2018_schema.txt` 731763f9570c555cce6e27bab66fc6cf2aa19ea98ee9607063845bd37bb5af2e; `google_ClusterData2019.md` 6209413ba5dc94e45b9dda811871b7eab406980aab5279466fa9eb48578ff6e3; `google_ClusterData2011_2.md` e189e6d6716603855707238eab489f54163620310f46683ff521a5c1922050a1; `alibaba_cluster-trace-v2018_trace_2018.md` daea8423c65cd24995500fcb6da103b1d4dec505f7b13ff2f6975caae0ede2fc.
- **Verbatim passages.**
  - Google 2019 schema, p. 13 (InstanceUsage table): "14. cycles_per_instruction – the mean CPI during the window (obtained by counting the CPU cycles used and dividing by the number of instructions executed)" … "16. sample_rate – the number of samples taken per second during the window. The nominal target is 1 Hz". Also "Cycles Per Instruction (CPI) and Memory Accesses Per Instruction (MAI) statistics are collected from processor performance counters; not all machines collect this data."
  - Google 2011 schema, pp. 10–11: "16. cycles per instruction (CPI)" / "17. memory accesses per instruction (MAI)".
  - Alibaba v2018 `schema.txt:22-34` (machine usage): `| cpu_util_percent | bigint | | [0, 100] |`, `| mkpi | bigint | | cache miss per thousand instruction |`, `| disk_io_percent | double | | [0, 100], abnormal values are of -1 or 101 |`.
- **Coverage.**
  - T10: **does not cover.** None of the schemas has a context-switch count or a scheduling-latency field. A grep for `context.switch|context_switch|ctx` across all of them matched nothing. The 2019 PDF's only "switch" hits refer to the top-of-rack network switch.
  - Other topics: does not cover.

### S3-09 — lmbench `ctx.tbl` (published context-switch table, 1996) (T10)

- **Citation.** L. McVoy and C. Staelin, "lmbench: Portable tools for performance analysis" (USENIX 1996), troff source `doc/usenix96.ms` and table `doc/ctx.tbl` in https://github.com/intel/lmbench, commit `27b43aeec9dc0bb45f420388c78e42dde4c23bf0` (2026-09-29).
- **Copy read.** `sources/S3-09/lmbench/doc/` (clone of 2026-10-07). SHA-256: `ctx.tbl` 3b94f25d8a33434ff8a941e3f8e445176addc56d76023002795acfdc33645e0c; `usenix96.ms` 39fd20389fe3c7cbdbc254d09bcca4b9b3ddcc428b97c13917ffeee2be2957e2; `lat_ctx.8` 04015eb32f5378d88dbcf7945d00bd484247e9a7fa6ec881943e9f5191c6c634.
- **Verbatim passages.**
  - `ctx.tbl:7-11`: `\t2 processes\t8 processes` / `System\t\fB0KB\fP\t32KB\t0KB\t32KB` / `=` / `Linux alpha\t10\t17\t13\t41\ ` / `Linux i486\t11\t394\t18\t594\ `
  - `ctx.tbl:35`: `Linux i686\t6\t22\t7\t107\ `
  - `usenix96.ms:1353-1355`: `.TSTART` / `.so ../Results/tmp/ctx.tbl` / `.TEND "Context switch time (microseconds)"`
  - `lat_ctx.8` DESCRIPTION: "lat_ctx measures context switching time for any reasonable number of processes of any reasonable size. The processes are connected in a ring of Unix pipes."
- **Coverage.**
  - T10 covered, but for historical hardware only. Object: context-switch time (µs) for 2 and 8 processes at 0 KB and 32 KB per-process footprint. Population: about 30 mid-1990s systems, named only by OS/architecture string (e.g. "Linux i686"). The table names no kernel versions. Each row is one machine. It does not cover current x86.
  - Other topics: does not cover.

### S3-10 — Linux `perf-sched` documentation example output (T10, illustrative)

- **Citation.** Linux kernel, `tools/perf/Documentation/perf-sched.txt`, fetched from raw.githubusercontent.com torvalds/linux `master`. `git ls-remote` gave master = `7b63ef2d55f24519e7e9e5f4d15dbea03f126e40` at access time.
- **Copy read.** `sources/S3-10/perf-sched.txt`, SHA-256 19f10af4a255882c0159317165fe87de78b2b6a97c6649434d2764a5936139be.
- **Verbatim passages.**
  - `:79`: `        79371.874569 [0011]  gcc[31949]                0.014      0.000      1.148` (columns: time, cpu, task, wait time, sch delay, run time; `:87` "Times are in msec.usec.")
  - `:102`: `        perf sched stats record -- sleep 1`
  - `:125`: `   Time elapsed (in jiffies)                                   :        2323`
  - `:131`: `   In the example below, schedule() left the CPU0 idle 36.58% of the time. 0.45% of total`
  - `:142-143`: `   sched_count                                                      :      402267` / `   sched_goidle                                                     :      147161  (    36.58% )`
  - `:166`: `   CPU 0, DOMAIN SMT CPUS 0,64`
- **Coverage.**
  - T10: illustrative only. The example's machine, kernel, HZ and workload are not named, so no rate can be derived: jiffies are given but HZ is not. It is not an observation with a named machine.
  - Other topics: does not cover.

### S3-11 — World of Warcraft Avatar History (WoWAH) dataset paper (T12)

- **Citation.** Y.-T. Lee, K.-T. Chen, Y.-M. Cheng, C.-L. Lei, "World of Warcraft Avatar History Dataset," Proc. ACM MMSys 2011, San Jose, pp. 123–128. Mirror: https://web.cs.wpi.edu/~claypool/mmsys-dataset/2011/wow/p123.pdf.
- **Copy read.** `sources/S3-11/p123.pdf` (974,596 bytes, 6 pp., SHA-256 5ef59d759f236cbe6f4dfc6a10bac2f7d0fff6db449dc84c3793c38a1a7ce9c5); mirror index `wpi_index.html` (SHA-256 233c67b212c948758c0ee58060b9418b3e9d24499bf81ce664a94142c657cc51). The data archive `wowah.rar` on the same mirror is 577,556,091 bytes (Last-Modified Sat, 19 Feb 2011). It is over the 300 MB limit and was **not downloaded**.
- **Verbatim passages.**
  - p. 124: "Observations were made at 10-minute intervals; hence, during the 3-year period, we made approximately 157, 680 observations (samples) on a WoW server."
  - p. 124: "To collect the trace, we created a character in a World of Warcraft realm (the Light's Hope realm in Taiwan) and kept it online throughout the 3-year study period." … "If an avatar logins and logouts within 10 minutes, we may not be able to observe his re-login activity in consecutive snapshots."
  - p. 125: "During the monitored period, 91, 065 avatars, and 667, 032 sessions associated with the avatars were observed."
  - p. 126, Table 4 "Summary of daily game play activities", (Mean, SD) and Quantiles (5%, 25%, 50%, 75%, 95%): "Session time (hr) (2.8, 1.8) (0.4, 1.0, 1.8, 3.0, 5.5)"; "Daily session count (1.7, 0.9) (1.0, 1.1, 1.4, 2.1, 3.3)"; "Daily play time (hr) (3.7, 2.8) (0.5, 1.6, 3.1, 5.1, 8.8)".
  - p. 126: "If we analyze the average session play time, we find significant "knee" around 1 hour and 5 hours, which indicate that after logging into the game, there is a high probability that players will stay for at least one hour, but usually no longer than 5 hours."
- **Coverage.**
  - T12 covered. Object: MMORPG play session length (hours) and sessions per day. Statistic: per-avatar averages, then mean/SD/quantiles across avatars. Scope: one realm (Light's Hope, Taiwan), Jan 2006–Jan 2009 (1,107 days). Population: 91,065 avatars (one faction, as observed by `who`). One observation (one server and window named). Resolution is 10 minutes. It is game-server-side login presence, not PC process activity.
  - Other topics: does not cover.

### S3-12 — SWELL-KW dataset (computer interaction features per minute) (T12)

- **Citation.** S. Koldijk, M. Sappelli, S. Verberne, M. Neerincx, W. Kraaij, "The SWELL Knowledge Work Dataset for Stress and User Modeling Research," ICMI 2014. Dataset: W. Kraaij, S. Koldijk, M. Sappelli, DANS Data Station SSH, doi:10.17026/dans-x55-69zp, version 4 (releaseTime 2025-06-04T08:57:35Z).
- **Copy read** (`sources/S3-12/`, SHA-256): `swell_dataset.html` (https://cs.ru.nl/~skoldijk/SWELL-KW/Dataset.html) 9f3df722d7d45e019f1815d700a042262d16096b102f4f3af7775f28b7cc2a75; `icmi2014.pdf` (https://cs.ru.nl/~skoldijk/Papers/ICMI%202014%20paper_final_cr.pdf) a10bffe9ea55cb66af6a8e7c2b61fbc5dfeffb3ebef57db8ef0f41cc6c1e5720; `dans_meta.json` fa6e6ee01d0246d4864df69744ca65453b72330acc74f2c272ed3538cbec7c3e; `swell_ulog_features_sheet1.csv` (DANS datafile id 189419, "A - Computer interaction features (Ulog - All Features per minute)-Sheet_1.csv", 256,466 bytes) b9799737fc6d86b40776079e0c755465ba8ce5b3d1796010954805fd7ba09f44. Not downloaded: `0_SWELL.zip`, 7,534,108,141 bytes (over the size limit).
- **Verbatim passages.**
  - Dataset page: "The SWELL-KW dataset contains data from 25 participants (~3 hours each), for working under 3 conditions: neutral, interruptions and time pressure (plus a relax phase)." Features table: "Computer interactions … Mouse (3) Keyboard (7) Applications (2)".
  - ICMI paper p. 4 (§3.4): "Participants performed their tasks on a computer (Dell Latitude E6400) with Windows 7 Professional with a 17 inch screen"; (§3.6) "Computer interactions were logged with the key-logging application uLog (version 3.2.5, by Noldus Information Technology)". Table 2: "AppChanges … Number of application changes" / "TabfocusChange … Number of tab focus changes". p. 5: "we computed several relevant mouse, keyboard and application characteristics per minute (listed in Table 2)".
  - CSV header (line 1): `PP,Blok,Condition,timestamp,SnMouseAct,…,SnAppChange,SnTabfocusChange,,`. Line 1360: `PP11,3,I,20121009T115500000,999,999,…,999,,uLog crashed…  12:18:00`, which shows that 999 marks missing minutes.
- **Computed** (`python3 -I swell.py swell_ulog_features_sheet1.csv`, Appendix A.8; verbatim):
  ```
  rows 3139 participants 25 conditions Counter({'N': 1028, 'I': 996, 'T': 664, 'R': 451})
  SnAppChange min 0.0 max 999.0 all integer True
  condition I minutes 996 mean per minute 35.324 -> per hour 2119.5 median per minute 4.0
  condition N minutes 1028 mean per minute 2.966 -> per hour 178.0 median per minute 2.0
  condition R minutes 451 mean per minute 0.095 -> per hour 5.7 median per minute 0.0
  condition T minutes 664 mean per minute 3.517 -> per hour 211.0 median per minute 3.0
  per-participant per-hour rate (work conditions N,I,T pooled): n 25 min 94.8 median 208.5 max 11665.9
  minutes with SnAppChange>60: 31 [('PP11', 'I', '20121009T115500000', '999'), …]
  condition I excluding minutes >60: minutes 965 mean per hour 262.0
  condition N excluding minutes >60: minutes 1028 mean per hour 178.0
  condition R excluding minutes >60: minutes 451 mean per hour 5.7
  condition T excluding minutes >60: minutes 664 mean per hour 211.0
  ```
  Valid only with the 999 (missing) minutes excluded: about 178 application changes per hour in the neutral condition, 262 under interruptions, 211 under time pressure and 5.7 during relaxation. The per-participant line above still includes the 999 minutes, so its max is invalid.
- **Coverage.**
  - T12 covered, partly. Object: **foreground application changes** per minute (focus switches between applications). This is not a change in the set of running applications. Population: 25 participants in a lab, Windows 7 laptop (named), ~3 h each, with assigned tasks, in Sept–Nov 2012 (CSV timestamps). One observation (one experiment).
  - Other topics: does not cover.

### S3-13 — RLKWiC dataset paper (T12, describes logging but reports no rate)

- **Citation.** M. Bakhshizadeh, C. Jilek, M. Schröder, H. Maus, A. Dengel, "Data Collection of Real-Life Knowledge Work in Context: The RLKWiC Dataset," arXiv:2404.10505v1, 16 Apr 2024.
- **Copy read.** `sources/S3-13/rlkwic.pdf` (1,486,529 bytes), SHA-256 e540f3fec18de419b5a68d86e0749cda8b6c5cc2e8fac7d8d538740329395b9b.
- **Verbatim passages.**
  - Abstract: "This paper presents RLKWiC, a novel dataset of Real-Life Knowledge Work in Context, derived from monitoring the computer interactions of eight participants over a span of two months."
  - Example context record (Table, §IV): "used apps / SearchApp, cSpaces, javaw, pycharm64, chrome".
  - Related-work table row: "BEHACOM [19] Modelling users' behavior 2020 Real-life tasks no task assignment 12 males with ages ranging from 20 to 45 years old 55 days keyboard, mouse, application statistics and resource consumption".
- **Coverage.**
  - T12: the dataset logs app names and window titles, but the paper (as read) reports **no** per-hour application-change statistic. It does not cover the quantity directly. I did not download the dataset.
  - Other topics: does not cover.

### S3-15 — UCSD Steam Video Game and Bundle Data (T12, negative)

- **Citation.** J. McAuley lab, "Steam Video Game and Bundle Data," https://cseweb.ucsd.edu/~jmcauley/datasets.html.
- **Copy read.** `sources/S3-15/ucsd_datasets.html`, SHA-256 dcfea83f969e6e2897a9ae2af1de550df18c1a23b1c5bd626cae7acb739cc6c3.
- **Verbatim passage.** "These datasets contain reviews from the Steam video game platform, and information about which games were bundled together." … "Metadata / reviews / purchases, plays, recommends ("likes") / product bundles / pricing information".
- **Coverage.** T12: does not cover session duration. The page lists reviews, purchases, plays, likes, bundles and prices, with no per-session timing. Other topics: does not cover.

### S3-16 — BEHACOM dataset (per-minute application statistics on personal computers) (T12)

- **Citation.** P. M. Sánchez Sánchez et al., "BEHACOM – a dataset modelling users' behaviour in computers," *Data in Brief* (2020), doi:10.1016/j.dib.2020.105767 (PMC7270191). Data: Mendeley Data doi:10.17632/cg4br62535.2 (version 2, files created 2020-05-06).
- **Copy read** (`sources/S3-16/`, SHA-256): `pmc7270191.html` aa16e6e67815afd8b2dd6d54a7ea9a9d0985fdfe30b3808985d1fc8c3a661f0c; `mendeley.json` 193d4c6c6acae0d0d649979efdec32ec3e7c05a780cc6ef383572021e6e513f4; `Behacom.zip` (37,414,157 bytes) 92e1b44b0d0853435f8e984e8dff76aa5ad7a90c5f04fdb7936045d3d0a15e44, which equals the `sha256_hash` Mendeley lists for the file; `Behacom_Readme.txt` (from the zip) c02056adaf0f013adb940fa4cd25ace9809bf7c9c12ef44dbfaf448b7863b1b5. The zip unpacks to 5.7 GB of CSV; I analysed it and then deleted the unpacked files, keeping the zip.
- **Verbatim passages.**
  - Article abstract: "The generated dataset, called BEHACOM, contains for each user a set of features that models, in one-minute time windows, the usage of computer resources such as CPU or memory, as well as the activities registered by applications, mouse and keyboard." Also: monitoring of "twelve users for fifty-five consecutive days without preestablished indications or restrictions" (fragment, abstract).
  - Article Table 5: "active_apps_average / Average number of applications active during the time window." … "changes_between_apps / Number of changes between different foreground applications during the time window."
  - `Readme.txt:67`: `    -  active_apps_average. This feature measures the average number of applications active during the time window.`; `:73`: `    -  changes_between_apps. This feature contains the number of changes between different foreground applications during the time window.`
  - Article: "Client application for Windows and Linux operating systems".
- **Computed** (`behacom.py`, Appendix A.9; verbatim):
  ```
  User0 vectors=6059 span=2019-11-20..2020-01-11 changes_between_apps mean/min=0.26 (=16/h) median/min=0.0 active_apps_average mean=2.0 consecutive-pairs=5324 with active_apps_average changed=12.2%
  User1 vectors=42281 span=2019-12-04..2020-01-14 changes_between_apps mean/min=0.01 (=0/h) median/min=0.0 active_apps_average mean=31.3 consecutive-pairs=2389 with active_apps_average changed=0.6%
  User2 vectors=179 span=2019-12-02..2019-12-02 changes_between_apps mean/min=0.34 (=20/h) median/min=0.0 active_apps_average mean=6.0 consecutive-pairs=11 with active_apps_average changed=72.7%
  User3 vectors=3221 span=2019-12-09..2020-01-13 changes_between_apps mean/min=0.15 (=9/h) median/min=0.0 active_apps_average mean=5.3 consecutive-pairs=2044 with active_apps_average changed=13.6%
  User4 vectors=10114 span=2019-11-26..2020-01-14 changes_between_apps mean/min=0.82 (=49/h) median/min=0.0 active_apps_average mean=5.6 consecutive-pairs=5894 with active_apps_average changed=39.0%
  User5 vectors=2128 span=2019-12-02..2019-12-06 changes_between_apps mean/min=0.27 (=16/h) median/min=0.0 active_apps_average mean=4.2 consecutive-pairs=1395 with active_apps_average changed=21.1%
  User6 vectors=1332 span=2019-12-18..2020-01-14 changes_between_apps mean/min=0.27 (=16/h) median/min=0.0 active_apps_average mean=1.5 consecutive-pairs=1301 with active_apps_average changed=9.9%
  User7 vectors=55778 span=2019-12-04..2020-01-14 changes_between_apps mean/min=0.02 (=1/h) median/min=0.0 active_apps_average mean=8.9 consecutive-pairs=17957 with active_apps_average changed=1.0%
  User8 vectors=5404 span=2019-11-20..2020-01-13 changes_between_apps mean/min=0.51 (=31/h) median/min=0.0 active_apps_average mean=5.8 consecutive-pairs=2496 with active_apps_average changed=31.5%
  User9 vectors=7920 span=2019-11-20..2019-12-15 changes_between_apps mean/min=0.83 (=50/h) median/min=0.0 active_apps_average mean=4.6 consecutive-pairs=4718 with active_apps_average changed=29.7%
  User10 vectors=15358 span=2019-11-20..2020-01-14 changes_between_apps mean/min=0.11 (=7/h) median/min=0.0 active_apps_average mean=5.0 consecutive-pairs=9527 with active_apps_average changed=8.3%
  User11 vectors=17284 span=2019-11-20..2020-01-14 changes_between_apps mean/min=0.24 (=14/h) median/min=0.0 active_apps_average mean=8.6 consecutive-pairs=6893 with active_apps_average changed=15.5%
  ALL users pooled: vectors=167058 changes_between_apps mean per vector 0.17 (=10 per hour of logged minutes)
  ```
  "consecutive-pairs" counts adjacent vectors 60 ± 5 s apart. The last column is the share of such adjacent minutes in which `active_apps_average` changed value; that is my derived proxy for a change in the active-application set. User1 has 42,281 vectors but only 2,389 adjacent pairs, so its timestamps are irregular or duplicated. I did not investigate why.
- **Coverage.**
  - T12 covered, partly. Objects: foreground-application changes per one-minute window, and the average number of "applications active" per window. Population: 12 users on their own personal computers (Windows/Linux; machines not named), 2019-11-20 to 2020-01-14 by timestamps, real-life use. It is one dataset. Per-user rows are observations with subject (anonymised user id) and window named, but no machine.
  - Rate of foreground changes: roughly 0–50 per logged hour per user, pooled about 10 per hour. The paper does not report a rate of change of the running set directly; my proxy is above.
  - Other topics: does not cover.

### S3-17 — University of Glasgow "Context-Guided Agents Dataset" (60 Seconds! telemetry) (T12, different notion of session)

- **Citation.** University of Glasgow Enlighten Research Data, record 2227, "Context-Guided Agents Dataset," https://researchdata.gla.ac.uk/2227/ (Readme.md).
- **Copy read.** `sources/S3-17/Readme.md` (18,052 bytes), SHA-256 0193fcb6d09ac0001a351eb0e2f85b1b1b7579c9151965a99c14ee72370fb38e.
- **Verbatim passages.** `Readme.md:6`: "Data was crowd-sourced from the players of the Steam desktop PC version of the game. The dataset contains 8,244,111 gameplay telemetry samples, each representing a single game session, for 808,659 unique players. It was crowdsourced from the real players of the game, playing the game in their natural play setups between January 2017 and May 2022." `:48`: "**total_time**: game session total time, including exploration and collection times (integer)". `:49`: "**elapsed_time**: actual game session total time, which includes startup and conclusion margins (float)".
- **Coverage.**
  - T12: here a "session" is one round of the game's scavenge mode (the per-second distribution fields are 60 characters long), not a sitting of PC play. It does not cover gaming-session length as asked. Data not downloaded.
  - Other topics: does not cover.

### S3-18 — Artificial Analysis provider benchmarks, Llama 3.1 8B (T11, hosted-API latency)

- **Citation.** Artificial Analysis, "Llama 3.1 8B: API Provider Benchmarking," https://artificialanalysis.ai/models/llama-3-1-instruct-8b/providers, accessed 2026-10-07. The page's schema.org block says: "citation":"Artificial Analysis (2025). LLM benchmarks dataset."
- **Copy read.** `sources/S3-18/aa_llama31_8b_providers.html`, SHA-256 99a25492dca28c779fdfb2ff057e9bda664599babb721412ae6b10586951bb98.
- **Verbatim passages** (embedded JSON, with backslash-escaped quotes removed):
  - `"slug":"groq_llama-3-1-instruct-8b","host":{"name":"Groq",…` then `"performance":{"outputSpeed":{"median":639.265170259853,"percentile05":448.039011391206,"percentile95":952.805624880943,…},"timeToFirstToken":{"median":0.839711704999957,"percentile05":0.713398121400014,"percentile95":1.1482771917,…},…"endToEndResponseTime":{"inputTime":0.839711704999957,"reasoningTime":0,"answerTime":0.78214804006412,"totalTime":1.6218597450640768},"byPromptType":{"long":{"medianOutputSpeed":639.265170259853,"medianTimeToFirstChunk":0.839711704999957,"medianEndToEndResponseTime":1.6218597450640768}}}`
  - UI strings: `"promptLengths":"Moderate prompts are ~1,000 input tokens, Long prompts ~10,000, and 100k prompts ~100,000."`; chart caption "Seconds to first token received · Lower is better · 10,000 input tokens"; `"measurementTechnique":"Independent test run by Artificial Analysis on dedicated hardware."`
  - Other providers' medians on the same page (my extraction, Appendix A.10): Novita TTFT 0.913 s / 150.8 tok/s; CoreWeave 0.661 s / 141.5 tok/s; DeepInfra (Turbo, FP8) 1.143 s / 30.9 tok/s; DeepInfra 1.074 s / 27.5 tok/s.
- **Coverage.**
  - T11 (hosted-API part) covered. Object: median TTFT (s), output speed (tokens/s) and end-to-end response time for Llama 3.1 8B per API provider. Scope: the "long" (~10,000-token) prompt. Population: providers listed on the page. The measurement window and the number of output tokens are not stated in the quoted data. It is not a short-prompt measurement.
  - Other topics: does not cover.

### Topics outside S3's assignment

- T1, T2, T3, T4, T5, T6, T9, T13, T14: not applicable to this class. They concern papers, documentation or news, not datasets, and I did not search for them.
- T8: not my topic. S3-03 incidentally quotes the catalogue's rule format and README.
- T15: not applicable; that is S4's own measurement.

---

### S3-19 — CachyOS ananicy-rules, history (T8; stage 3, 2026-10-08)

- **Copy read.** Full `git clone https://github.com/CachyOS/ananicy-rules` on 2026-10-08 into `sources/S3-19/ananicy-rules/`. HEAD `03ef03fbf7e834385377432ccecaedd32e3414bb`, unchanged since S3-03. 2,762 commits (2,239 non-merge, 523 merges); first commit `c3efeb28371e835151f928e321fbfeeadbb1125d`, 2022-03-16. Tag `1.1.49`, the version CachyOS packages (S2-45), resolves to `03ef03fb…`.
- **Computed: entries over time** (`count_at.py`, Appendix A.12; S3-03's method — each `.rules` file parsed separately, one JSON object per non-blank, non-`#` line; at the last first-parent commit on or before each date):

  | Date | Commit | `.rules` files | Entries | `Game` |
  |---|---|---|---|---|
  | 2022-12-31 | `8dda7561` (2022-12-13) | 348 | 880 | 524 |
  | 2023-12-31 | `f524ad42` (2023-12-27) | 245 | 1 066 | 675 |
  | 2024-12-31 | `32c77758` (2024-12-30) | 257 | 1 367 | 764 |
  | 2025-12-31 | `3f1f24c3` (2025-12-28) | 292 | 1 645 | 965 |
  | 2026-03-31 | `7460ed8d` (2026-03-30) | 331 | 6 329 | 5 533 |
  | 2026-06-30 | `fd4e898d` (2026-06-29) | 352 | 14 731 | 12 602 |
  | HEAD | `03ef03fb` (2026-09-08) | 361 | 15 813 (1 unparseable line) | 13 528 |

- **Computed: who last changed each current entry** (`blame_rules.py`, Appendix A.13; `git blame --line-porcelain -w -M -C` on every `.rules` file at HEAD): the 15 813 entries trace to 1 214 commits by 112 authors. Two authors account for 13 493 (85.3 %): Luka Ogadze 9 445, pollux78 4 048; then Shendisx 1 100, jilv220 204. 22 commits cover half the entries. 15 077 lines date from 2026 commits. Blame dates a line's last change, which includes re-sorts and retypings (e.g. `7a1d26ab`, "updated UE game rules", retypes `Game` entries to `BG_CPUIO`), so these figures say who last edited each entry, not who first added it; the dated counts above are the growth measure.
- **What the repository carries besides rules** (`git ls-files` at HEAD): `00-types.types`, `00-cgroups.cgroups`, `ananicy.conf`, the two JSON schemas, `Makefile`, `README.md`, an issue template, `lint.py` (added `75ab9bc5`, 2026-08-25: "add lint.py script and JSONSchema for rules and cgroups definitions") and `sort-games.sh` (added `9100589b`, 2026-04-09). No script that generates entries.
- **Passages: audio entries** (at `03ef03fb`; read for scope-card item 37, 2026-10-08):
  - `00-default/Creative/reaper.rules:1–2` (SHA-256 `0636d1efc0468853fc53cf112f070ec898393c5138a121227f2ae722be17c8e5`): `# https://reaper.fm` / `{ "name": "reaper", "type": "Player-Audio" }`
  - `00-default/Creative/bitwig-studio.rules:1–3` (`24867be61c329379f97110ab1eb01bfb2925f5b3f425251e3d55c5ecb2a1013e`): `# Digital Audio Workstation: https://www.bitwig.com/en/bitwig-studio.html` / `{ "name": "bitwig-studio", "type": "Player-Audio" }` / `{ "name": "BitwigStudioEngine", "type": "Player-Audio" }`
  - `00-default/Creative/ardour.rules:1–2` (`08807d572fde478f726bf823d635c6620e3e6be57d8e392e33efb3c99d2ced9c`): `# https://ardour.org/` / `{ "name": "ArdourGUI", "type": "Player-Audio" }`
  - `00-default/Creative/lmms.rules:1–2` (`bf29720ff2e17c642db518dd2592128e177b99b8118d65a9ca9e15fc90efe4d1`): `# https://lmms.io/` / `{ "name": "lmms", "type": "Player-Audio" }`
  - `00-default/Creative/audacity.rules:1–2` (`30c7ab58edd37c48e941ba13671b60f1e8bb3fa615fc2a1ae86f254af29bd2f1`): `# Sound editor: http://www.audacityteam.org/` / `{ "name": "audacity", "type": "Player-Audio" }`
  - `00-default/Audio-Video/audioserver.rules:1–4` (`3b8b4a9d6f52298e7f9ac738615909846932645ec9af2edf9ed4c8b1baa41bd5`): `pipewire`, `pipewire-pulse`, `wireplumber`, `pulseaudio`, each `"type": "LowLatency_RT"`; `00-default/Audio-Video/mixxx.rules:2`: `{ "name": "mixxx", "type": "LowLatency_RT" }`
  - `00-types.types:9`: `{ "type": "Player-Audio", "nice": -4 }`; `:18`: `{ "type": "LowLatency_RT", "nice": -12, "ioclass": "best-effort" }`
  - The 28 `Player-Audio` entries are the five workstations above with `helgobox`, `KholorsStation`, `BitwigStudioEngine` and `tenacity`, and nineteen music players (`clementine`, `spotify`, `rhythmbox`, `mpd`, `cmus`, `audacious`, …). No entry names `qtractor`, `rosegarden`, `zrythm`, `renoise`, `hydrogen`, `carla` or `jackd`.
- **Computed: the core set's process names in the catalogue** (`names_vs_catalogue.py`, Appendix A.14; the 50 compiled files of `dataset/build/coreset-single/` at repository commit `06895b81`, every `arrive` event's `name`, matched exactly against entry names at `03ef03fb`, and after truncating entry names to 15 characters): 35 distinct names; 14 match exactly — `Troy.exe` (`Game`), `steam` (`Launcher`), `wineserver`, `gnome-shell`, `pipewire` (`LowLatency_RT`), `chrome`, `code`, `soffice.bin` (`Doc-View`), `mpv` (`Player-Video`), `gimp` (`Image-View`), `element-desktop` (`Chat`), `dbus-daemon` (`Service`), `7z`, `baloo_file` (`BG_CPUIO`); none more after truncation. Unmatched: `kdenlive`, `kdenlive_render`, `make`, `python`, `HandBrakeCLI`, `deja-dup`, `tracker-miner-f`, `thunderbird-bin` (the catalogue carries `thunderbird`), `unattended-upgr`, `dkms`, `systemd`, the game chain's `dxvk-cs`, `dxvk-submit`, `FAudio_AudioCli`, `Task worker thr`, `winepulse_mainl`, `winepulse_timer`, and `audio-stream-he`, `video-playback-`, `qzvd`, `xkrr`. Files whose every arriving name matches: 7 of 50. Whether ananicy-cpp compares a rule's `name` with the 15-character `comm` or with the executable's basename was not read.
- **Coverage.**
  - T8 covered for how entries enter: by commit, from contributors — 112 authors for the current entries. Whether a contributor wrote an entry by hand or produced it with a tool outside the repository is not observable from the history.
  - T7 (counts): growth from 1 645 entries at the end of 2025 to 15 813 at `03ef03fb`, nearly all of it `Game` entries (965 → 13 528). One observation per date (one commit each); no machine.

### S3-20 — Debian unstable: declared scheduling classes over the systemd units Debian installs (T7; stage 3, 2026-10-08)

Redoes S3-01's percentages, by 인지오's decision on scope-card item 26. Two findings about S3-01's method come first.

- **The grouped Debian Code Search view is not a package list.** Fetched page by page (`perpkg=1`, `^\[Service\] path:\.service`), the 319 pages carry 1 595 package headers. Debian Code Search keeps a query's result set for a few minutes and then re-runs it in a different order: page 5 fetched at 20:58 and again after 21:05 listed different packages, page 200 the same (the sequential fetch's pages are kept under `sources/S3-20/denom_all/`). Read inside one result set — every page fetched in one parallel burst, page 0 identical before and after (`dcs_burst.sh`, Appendix A.15) — the 1 595 headers still hold only 1 248 distinct packages, and packages whose units carry a matched directive are absent from them (`e2fsprogs`' `scrub/e2scrub@.service.in`, `btrfsmaintenance`, `wtmpdb`, `espeakup` and nine more). S3-01's denominator, 318 × 5 + 3 = 1 593, counts headers, not packages.
- **The denominator is taken from Debian's own indexes instead.** `dists/sid/main/Contents-amd64.gz` and `Contents-all.gz` list every file every binary package installs; `binary-amd64/Packages.xz` and `binary-all/Packages.xz` map binary to source. All four were fetched from deb.debian.org on 2026-10-08 and verified against the `Release` file (`Date: Thu, 08 Oct 2026 08:27:44 UTC`; Release SHA-256 `0c7e059f95f9d77662acd6d8a850eb990ec40dcc990c7cb5d22999581600bb07`): `Contents-amd64.gz` `6891558de9344e90a3ac260051e13afa6a952c8660448a6490d8df9445cc3da0`, `Contents-all.gz` `22977015fb491c22b21c4f768a5499e8db685d7ec76b82bd9bdb67d864b10351`, `binary-amd64/Packages.xz` `d01b8095aa94531e63c3d44eedd229ab112c2d62b7abef9ca83beadb9b3f2a12`, `binary-all/Packages.xz` `aa59b51545989cb2ee34e44ce8c01ec5a5e997ee644635b1da635b81a13bc588` (`sources/S3-20/debian-index/`).

- **Method** (`installed_units_count.py`, Appendix A.16).
  - Denominator: source packages whose binaries in `main` install at least one systemd service unit, `(usr/)lib/systemd/{system,user}/*.service`.
  - Numerator: Debian Code Search hits of an uncommented `Nice=`, `IOSchedulingClass=` or `CPUSchedulingPolicy=` line in a `\.service` path (regex `^\s*Nice=` and the like; each query read in one burst, page 0 unchanged: `burst/nice_all.1`, `ioclass_all.1`, `cpupolicy_all.1`; page manifests SHA-256 `6af6c52869b023f73e0d39ce3e8decfda4be29b841b46b3a16ef97f9c36046eb`, `b1fefb118db3b250ed76fd08131768cff6063c74502682a28a714c7b5e1d7953`, `e2950f95f36f05e5181f7012c489771be90b85f176016793e903305fe2a5828f`; no hit duplicated), counted only where the file's installed name — its basename without `.in`, `.cmake` or `.tmpl`; a drop-in with its `<unit>.service.d/` parent; debhelper's `debian/<binary>.<unit>.service` as `<unit>.service`; one rename read in the source's build file, `snapper_0.10.6-1.3/data/Makefile.am:29`, `install -D -m 644 cleanup.service $(DESTDIR)/usr/lib/systemd/system/snapper-cleanup.service` — is among that source package's installed units.
  - Direction: `Nice=` above 0, `CPUSchedulingPolicy=` `idle` or `batch`, `IOSchedulingClass=` `idle` or `3` lower a unit's priority; `Nice=` below 0, `rr` or `fifo`, `realtime` or `1` raise it.
- **Computed** (verbatim, the first fourteen lines of `installed_units_count.out`, SHA-256 `db9cb9c3956c44fb950b5d80133286700366406ced03c7bf755f2eca139c186f`):

```
denominator: source packages installing >= 1 .service unit: 1438 (system units 1261, user units 218); binary names in Contents without a Packages stanza: 0
Nice=                  hits  68, in installed units  49; packages  38 (2.6 %), lowering 27 (1.9 %), raising 11 (0.8 %)
   values: 19 x25, -5 x8, 10 x6, -10 x5, 9 x2, -20 x2, -11 x1
   lowering: apt-show-versions apt-xapian-index boinc borgmatic chkrootkit debusine dnf5 drkonqi exim4 findutils kanboard lighttpd logcheck logrotate lynis mailgraph man-db openqa-server pk4 plocate privoxy rauc-hawkbit-updater rtags sitesummary storebackup systemd xfsprogs
   raising: brltty deepin-boot-maker deepin-log-viewer earlyoom espeakup frr gdnsd hdapsd railcontrol readsb svxlink
IOSchedulingClass=     hits  71, in installed units  41; packages  30 (2.1 %), lowering 18 (1.3 %), raising 2 (0.1 %)
   values: idle x26, best-effort x10, realtime x2, 2 x2, 3 x1
   lowering: apt-listchanges apt-xapian-index boinc btrfsd btrfsmaintenance clsync e2fsprogs etckeeper findutils flatpak man-db ntpsec pk4 plocate rust-rebuilderd-worker snapper systemd xfsprogs
   raising: hipercontracer railcontrol
CPUSchedulingPolicy=   hits  45, in installed units  25; packages  17 (1.2 %), lowering 12 (0.8 %), raising 5 (0.3 %)
   values: idle x16, rr x4, batch x3, fifo x2
   lowering: apt-xapian-index borgmatic btrfsd btrfsmaintenance bumblebee e2fsprogs grokmirror radvd rtags rust-rebuilderd-worker snapper xfsprogs
   raising: hipercontracer low-memory-monitor osmo-bts osmo-mgw osmo-pcu
ANY of the three: 56 packages (3.9 % of 1438); lowering 40 (2.8 %); raising 16 (1.1 %); lowering only 40, raising only 16, both 0
```

- **Not matched to an installed unit** (69 lines in 54 files, listed in full in the output): systemd's test units (`test/test-execute/`, `test/test-sched-prio/`, `test/fuzz/`) and its Ubuntu-only `debian/extra/units-ubuntu/systemd-journald.service.d/nice.conf`; the `systemd-udeb` source; example units (`duply_2.5.6-1/systemd-unit.examples/`); upstream `contrib/` units (`osmo-bts`, `osmo-trx`, `vdradmin-am`); an RPM-only file (`coturn_4.18.0-1/rpm/turnserver.service.fc`); `ctags` test inputs (`codelite`, `universal-ctags`); and units the binaries do not install (`dnf_4.24.0-1/etc/systemd/*`, `hw-probe`'s `periodic/`, `jacktrip`'s container unit, `jamulus`' upstream `linux/debian/`, `keepalived-non-root`, `openqa-gru`, `brltty@`, `wtmpdb-rotate`).
- **Coverage.**
  - T7 covered for units. Object: Debian unstable `main`, binaries for amd64 and all, on 2026-10-08. Unit: source package. Statistic: packages installing a service unit (1 438); packages whose installed units carry each directive, and its direction. Of the 1 438, 56 (3.9 %) carry any of the three directives in an installed unit: 40 (2.8 %) only lowering, 16 (1.1 %) only raising, none both. Of the 49 `Nice=` values in installed units, 33 lower priority (25 at 19) and 16 raise it.
  - Not counted: a class a program sets on itself in code (LocalSearch, Baloo, tumbler, recoll, akonadi-search; S3-02) or through a wrapper (Déjà Dup's `chrt --idle 0 ionice -c3`, 9.11 S2-27) — the desktop indexers are of this kind, so the unit count is a floor on declaration, not its total; packages Debian Code Search does not index (S3-01 names `clamav`; its units declare nothing, S3-02). One observation per index snapshot, not a machine.

### S3-21 — Context switches per second on the measured CPU, from the campaigns' own traces (T10; stage 3, 2026-10-09)

- **Copy read.** The artifacts of the measurement campaigns as downloaded by the loop tools (`~/.cache/meas-loop`, the development Mac; 2 028 `report.json`, 2 259 `perf.*.timehist.txt.gz`), each a `perf sched timehist --state` of a `perf sched record -a` over a whole phase (`dataset/tools/meas/campaign/run.sh:152`, `:162`; `build/run.sh:106`; `background/run.sh:212`, `:231`; `desktop/run.sh:127`). Script `sources/S3-21/switch_rates.py` (A.17, SHA-256 `07fd828ee78eb048f6b93a94b4300bed2443fdbcca7caf97f829b0fab1c6d252`), output `rates.tsv` (2 195 lines, `5c732b7c6e3658ee2bed091f4f410646b092710a689058fd0ef6978e3757f30b`); `summarize.py` (`334a8a8a…`), output `summary.txt` (`ed80b65c…`).
- **Method.** A timehist row is one switch-out on the CPU in its second column, `<idle>` included; every CPU is recorded. Per phase file: the rows on the repeat's load CPU (`pin.load_cpu`, CPU 3) over the file's span, first row to last. Kept: `gate` open and `machine.model` the EPYC 7763; one row per (run, family, application, repeat, phase). The summary keeps full-mode repeats: 1 806 phase files over 509 runs, 71 program-phase groups. The load CPU holds the measured program and whatever else the runner schedules there (the runner's agent shares it, each entry's scope; the session's idle phase, 17 a second, is the floor).
- **Output** (`summary.txt`, verbatim):
  ```
  rows 2195, full-mode 1806, groups 71
  family       app                      phase               n    median       min       max
  background   steamcmd                 steam-fresh-untraced   33   12446.7     297.0   14036.3
  background   steamcmd                 steam-fresh-shaped   33   11094.4    5579.8   12192.0
  background   steamcmd                 steam-fresh-unshaped   33    5634.5     299.1    9169.9
  None         webrtc                   play               50    3112.9    2985.6    3332.9
  desktop      launch-webrtc            launch              5    2907.4    2900.6    2922.4
  background   borg                     borg-first-cold    31    2206.0     239.5    2304.4
  None         thunderbird-send         op                 17    1585.9    1554.4    1629.5
  None         mpv-video                play               24    1577.7    1453.7    1729.0
  desktop      launch-mpv-video         launch              5    1521.2    1416.8    1599.0
  None         code                     driven-alt        127    1503.1    1034.1    1809.0
  build        None                     handbrake          14    1489.0    1473.7    1510.5
  build        None                     ffmpeg             14    1141.1    1118.8    1160.9
  None         code                     driven            127    1075.3     751.4    1752.1
  background   upgrade                  upgrade-install     9     981.5     911.2    1012.0
  background   borg                     borg-repeat-cold   31     978.1     224.5    1007.5
  build        None                     dkms               14     973.1     916.9    1048.0
  background   dkms                     dkms-install       26     963.2     907.9     996.5
  None         thunderbird              driven-alt          8     771.1     703.1     869.3
  build        None                     tracker            14     766.9     736.0     898.4
  None         thunderbird-send         driven-alt         16     744.8     686.0     867.1
  background   handbrake                handbrake-transcode    5     694.8     690.8     705.6
  background   kdenlive                 kdenlive-export    30     692.1     651.7     747.7
  desktop      launch-steam             launch              5     670.8     668.1     676.6
  background   dejadup                  dejadup-incremental   30     612.7     237.4     841.4
  desktop      steam                    shown              12     604.0     591.2     610.0
  None         kdenlive                 op                 20     597.5     586.1     607.9
  background   7z                       7z-mmt8-cold        6     590.8     571.9     598.6
  background   tracker                  tracker-index      30     568.8     464.4     598.2
  background   7z                       7z-mmt8-warm        6     558.0     549.3     564.9
  desktop      steam                    minimised          12     528.3     517.1     535.9
  None         thunderbird              driven              8     463.4     327.4     570.3
  desktop      launch-mpv-audio         launch              5     453.8     411.4     457.4
  None         chrome                   driven-alt         86     451.4     204.6     616.3
  build        None                     build-j8-cold      14     450.9     447.4     454.8
  None         thunderbird-send         driven             17     442.0      78.9     558.1
  build        None                     build-j8-warm      14     436.9     434.1     439.5
  None         mpv-audio                play               31     422.0     404.7     436.9
  None         kdenlive                 driven             20     379.2     344.2     414.8
  desktop      launch-element           launch              5     360.5     357.3     395.2
  desktop      chrome-visible           steady-timer       11     331.6     320.8     335.8
  None         chrome                   op                 86     274.6     261.8     287.4
  None         code                     idle              128     244.2     201.1     330.9
  build        None                     clamscan           14     224.1     213.8     233.2
  None         chrome                   driven             86     194.9     157.4     339.7
  None         soffice                  driven-alt         14     179.0     165.4     202.3
  desktop      launch-chrome            launch              5     168.4     154.3     175.8
  desktop      element                  traffic            18     163.3     152.8     175.2
  None         soffice                  driven             14     147.4     127.3     170.7
  desktop      launch-thunderbird-send  launch              5     140.4     132.7     147.6
  desktop      launch-kdenlive          launch             10     140.2      82.1     236.8
  None         chrome                   idle               86     139.9     123.2     247.9
  desktop      launch-chrome-hidden     launch             10     139.1     127.3     151.9
  build        None                     build-j1-warm      14     138.3     135.1     142.4
  background   borg                     borg-first-warm    31     128.9     105.2     281.0
  desktop      launch-soffice           launch              5     117.1     115.4     128.0
  desktop      chrome-hidden            steady             24     107.1      94.5     122.8
  None         thunderbird              idle                8     100.9      89.7     112.3
  None         gimp                     driven              5      98.6      97.2     112.9
  desktop      element                  idle               18      95.6      88.0     112.7
  desktop      chrome-visible           steady-notimer     11      94.7      77.8     105.7
  None         soffice                  idle               14      86.1      75.8     101.0
  None         thunderbird-send         idle               86      84.8      67.8      98.5
  None         kdenlive                 idle               20      84.6      69.5     102.4
  None         gimp                     idle                5      83.3      61.3      91.5
  None         gimp                     op                  5      45.9      43.5      52.4
  background   borg                     borg-repeat-warm   31      40.8      32.8     171.3
  build        None                     train              14      37.0      19.6     334.9
  session      session                  steady             24      16.9      14.8      19.1
  background   7z                       7z-mmt1-warm        6      13.0       9.9      14.0
  background   mnist                    mnist-train         6      12.9      12.0      13.9
  background   mnist-madvise            mnist-train         5      12.2      11.2      13.7
  group medians: min 12.2, median 436.9, max 12446.7
  full-mode phase files: n 1806, p10 90.1, p50 419.9, p90 2103.7, max 14036.3
  ```
  Of the 71 groups' medians, 57 are at least 100 a second, 13 at least 1 000, 2 at least 10 000 (both SteamCMD's download phases).
- **The measured CPU's busy share** (`sources/S3-21/busy_share.py`, A.17, SHA-256 `16e234bb600423f8629c6be0d5ef12731a879ffda819bfc0f8173d76bb59d398`; one minus the `<idle>` task's run time on the load CPU over the span), 9.6's build-family phases, 14 repeats each (output verbatim):
  ```
  build build-j8-warm: repeats 14, busy share 0.9974–0.9977, median 0.9976
  build build-j8-cold: repeats 14, busy share 0.9973–0.9974, median 0.9974
  build build-j1-warm: repeats 14, busy share 0.9970–0.9971, median 0.9971
  build handbrake: repeats 14, busy share 0.9345–0.9389, median 0.9371
  build ffmpeg: repeats 14, busy share 0.9179–0.9208, median 0.9196
  build tracker: repeats 14, busy share 0.2042–0.2541, median 0.2069
  build clamscan: repeats 14, busy share 0.9334–0.9440, median 0.9387
  build train: repeats 14, busy share 0.8190–0.8575, median 0.8506
  build dkms: repeats 14, busy share 0.4036–0.4166, median 0.4090
  ```
- **Coverage.** T10 covered for one quantity: context switches per second on one CPU running one desktop program at a time, for the dataset's programs, on the EPYC 7763 runner (kernel 6.17.0-1022-azure), from 12 a second (single-threaded MNIST training) to 12 447 (SteamCMD's download), the median group 437. A switch is a lower bound on schedule() calls (the runner's idle CPUs call schedule() more often than they switch, `meas-ci:costs` dry run). Not covered: a desktop CPU shared by several programs at once, which this measurement isolates by design (`pin.sh`).

### S3-23 — Chambers, Feng, Sahu & Saha, IMC 2005: session times on one Counter-Strike server (T12; stage 3, 2026-10-09)

- **Citation.** Chris Chambers, Wu-chang Feng, Sambit Sahu, Debanjan Saha. "Measurement-based Characterization of a Collection of On-line Games." Internet Measurement Conference (IMC '05), 2005. HTML edition at usenix.org/legacy/event/imc05/tech/full_papers/chambers/chambers_html/.
- **Copy read** (2026-10-09, `sources/S3-23/`): `index.html` SHA-256 `5322b990249ded0bb162aaefd248624f612d2f8ad81e4635a4290d616edf5636`; `node2.html` (Methodology) `00fa689944a676286847d4dc49da8239d5cacbf71989e6ddfdb5f98f3dcbc296`; `node3.html` `076db7e2…`; `node5.html` ("Gamers have short attention spans") `f3d1c2eb16cb1bd376a04f60850cfe22e6036ce2f3d0dfb6f3c84b475d0f6d8e`.
- **Passages.** Methodology: "we examined the activity of one of the busiest and longest running Counter-Strike servers in the country located at cs.mshmro.com"; the abstract's "a 13-month trace of an extremely busy game server containing over 2.8 million connections". §"Gamers have short attention spans": "a significant number of players play only for a short time before disconnecting and that the number of players that play for longer periods of time drops sharply as time increases" … "more than 99% of all sessions last less than 2 hours" … "the data can be closely matched to a Weibull distribution".
- **Coverage.** T12 covered for one game: session time on one Counter-Strike server, server-side connection time, 13 months; not PC process activity, and a player's session on one server, not a sitting. Other topics: does not cover.

### S3-22 — A recognizer-shaped request's latency on a consumer machine: Apple M1 Pro, llama.cpp with Metal (T11; stage 3, 2026-10-09)

- **Machine** (`sources/S3-22/machine.txt`): 인지오's development Mac, Apple M1 Pro (8 performance and 2 efficiency cores), 16 GB, macOS 27.0.1 (26A434), on AC power; the machine's own work running beside it (the VS Code tunnel, this session). Run 2026-10-08T23:54Z onward.
- **Software and inputs.** llama.cpp at `bd4eeaa047006cb1fe71999fbd11134b5836e167`, built with CMake, Release, Metal on (`GGML_METAL=ON`); the two GGUF files of the runner campaign (D31), SHA-256 equal to the pinned `626b4a66…` and `7b064f58…`; `dataset/tools/meas/llm/request.py` with `prompt.json` and the two schemas (the runner campaign's request, unchanged). Per repeat and model: `llama-server -c 4096 -np 1` at its default offload, the time to `/health`, a warm-up and five requests per schema, then `llama-bench -p 512 -n 64 -r 3`. Five repeats. Script `m1_run.sh` (A.18, SHA-256 `613a5cb62d086412f889147631dd070c61733d2a557e252ba43be95b48603d48`), summary `summarize_llm.py` (A.18, `2205fe69f019da7247ba37a7618d92aba5728272194d46473d772ca9b5135a85`), output `summary.txt` (`dbb990a2d40e4b54cedda805b0a3c3d76fd456e825365d19c08ea0204eb1f9f7`); the page cache is not dropped between repeats (`purge` needs `sudo`), so the load times after the first are warm (8.8 s and 3.4 s cold in repeat 1, 1.2–1.9 s after).
- **Output** (`summary.txt`, verbatim; ms, means over each repeat's five requests, then the mean and range over the five repeats):
  ```
  llama3.1-8b  full   repeats 5: wall_ms 5340.1 (5335.7–5345.3), prompt_n 454.0 (454.0–454.0), prompt_ms 1907.6 (1906.9–1907.9), predicted_n 82.0 (82.0–82.0), predicted_ms 3431.0 (3426.3–3435.8)
                      distinct answers over every request: 1
  llama3.1-8b  system repeats 5: wall_ms 2951.9 (2950.2–2953.5), prompt_n 454.0 (454.0–454.0), prompt_ms 1907.7 (1906.8–1908.9), predicted_n 26.0 (26.0–26.0), predicted_ms 1042.7 (1041.1–1044.5)
                      distinct answers over every request: 1
  qwen2.5-3b   full   repeats 5: wall_ms 2254.7 (2244.9–2281.4), prompt_n 437.0 (437.0–437.0), prompt_ms 731.7 (731.3–732.3), predicted_n 81.0 (81.0–81.0), predicted_ms 1521.3 (1511.6–1547.3)
                      distinct answers over every request: 1
  qwen2.5-3b   system repeats 5: wall_ms 1190.2 (1187.0–1195.8), prompt_n 437.0 (437.0–437.0), prompt_ms 731.8 (731.6–731.9), predicted_n 25.0 (25.0–25.0), predicted_ms 456.7 (453.1–462.1)
                      distinct answers over every request: 1
  llama3.1-8b  bench: pp512 255.57 t/s (255.42–255.74, n 5), tg64 25.58 t/s (25.48–25.65, n 5)
  qwen2.5-3b   bench: pp512 623.42 t/s (622.92–623.72, n 5), tg64 59.78 t/s (59.75–59.82, n 5)
  ```
- **Placement.** llama-bench reports `backends: MTL,BLAS`, `gpu_info: Apple M1 Pro`, `n_gpu_layers: -1` (every layer on the GPU); the server's prompt rate, 238 tokens a second for the 8B, matches the bench's Metal rate.
- **Answers.** Each model and schema returned one answer, byte-identical, across all 25 requests (5 repeats × 5) at temperature 0 and seed 1. To this one prompt (`c2-p2a` at 60 s: a game and a user-started download, ground truth `gaming`, `background_wanted: true`), the 3B answered `idle` with the `system` block alone and `gaming` with reasoning first, `background_wanted: false`; the 8B `gaming`, `true` alone and `gaming`, `false` with reasoning first. One prompt, not a measure of accuracy.
- **Coverage.** T11 covered on one consumer machine: end-to-end latency of a 437–454-token recognizer prompt and a 25–82-token JSON answer from a 3B and an 8B Q4_K_M model — 1.19 s and 2.95 s for the `system` block, 2.25 s and 5.34 s with `reasoning` and `situation` first — prompt processing 0.73 s and 1.91 s of it; determinism of the answer on one machine. One machine, one prompt.

## 3. Not found

- **T10 — context-switch rate per core on a desktop or server, with machine and kernel named, from a public dataset.** Not found. The only trace with a computable rate is S3-07, from an Android phone (Linux 4.4.177, aarch64). Searches that established this:
  - Google 2011/2019 and Alibaba 2017/2018 cluster traces (S3-08): no context-switch field.
  - OpenBenchmarking pts/ctx-clock and stress-ng, and Phoronix: **403** (Cloudflare challenge).
  - lmbench: only the 1996 table (S3-09); `results/` is empty; www.lmbench.org gave no connection.
  - perf-sched doc example (S3-10): machine unnamed.
- **T10 — cost of one pick-next-task decision, and current-x86 context-switch cost, as a published dataset.** Not found among datasets; OpenBenchmarking (403) was the only results database tried. lmbench `ctx.tbl` covers 1990s hardware only.
- **T10 — typical time-slice lengths as a dataset.** Not found. S3-07 gives run-slice durations (median 56.25 µs, mean 200 µs) for one Android trace. Those are observed run lengths, not configured slices.
- **T11 — dataset of local short structured-output (JSON) latency for 3–8B quantized models on consumer hardware.** Not found:
  - LocalScore (S3-05) has consumer CPU/GPU TTFT and tokens/s, but no structured-output test.
  - LLM-Perf (S3-04) is datacenter hardware.
  - MLPerf Client (S3-06) defines a JSON task but publishes no results table.
  - llama.cpp performance discussions (#4167, #15013) returned **403**.
- **T12 — PC (desktop) gaming session-length dataset.** Not found with PC-side process data:
  - WoWAH (S3-11) measures game-server login presence for one MMORPG realm.
  - The Glasgow dataset (S3-17) uses "session" for one game round.
  - The UCSD Steam data (S3-15) has no per-session timing.
  - IdleWars (Southampton eprint 377465) returned **401**.
  - The WoWAH home and download host gave **500** and no connection; the WPI mirror worked.
  - Zenodo searches (log row 30) found nothing relevant; one query failed with a connection reset.
- **T12 — how often the set of running applications changes per hour.** Not found as a reported statistic. Two datasets give foreground-application change rates per minute:
  - SWELL-KW (S3-12): lab, Windows 7.
  - BEHACOM (S3-16): 12 users, real use. BEHACOM also has an "applications active" count per minute, from which I derived only a proxy (share of adjacent minutes in which it changes).
  - RLKWiC (S3-13) logs apps but reports no rate.
- **T7 — any published survey or count of how many packages or units declare a scheduling policy, nice level or I/O class.** No published count was found; S3-01 is my own count from Debian Code Search. No query was made for a published survey. The documented case of an application raising its own priority beyond what its work warrants is outside a dataset search; S3-01's negative-`Nice=` and rr/fifo hits only list declarations and do not judge whether they are warranted.

---

## Appendix A — scripts and commands (verbatim)

### A.1 `dcs.sh` (Debian Code Search fetcher; q01–q09 ran an earlier copy whose curl line lacked `--retry 5 --retry-all-errors -m 120`)
```bash
#!/bin/bash
# usage: dcs.sh OUTDIR LITERAL QUERY  -> fetches all result pages (non-grouped) of Debian Code Search, no-JS HTML
out=$1; lit=$2; q=$3
mkdir -p "$out"
enc=$(python3 -I -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1],safe=""))' "$q")
p=0
while :; do
  f="$out/page_$p.html"
  for t in 1 2 3 4 5 6 7 8 9 10; do
    code=$(curl -sS --retry 5 --retry-all-errors -m 120 -o "$f" -w "%{http_code}" "https://codesearch.debian.net/search?q=$enc&literal=$lit&page=$p")
    if grep -q 'Still searching' "$f"; then sleep 5; else break; fi
  done
  echo "page $p http $code" >&2
  grep -q "page=$((p+1))\" rel=\"next\"" "$f" || break
  p=$((p+1)); [ $p -gt 400 ] && break
done
```
Invocations: `./dcs.sh sources/S3-01/q01_cpuidle_unit 1 'CPUSchedulingPolicy=idle path:\.(service|timer)'` and likewise for each row of the S3-01 table (literal flag 1, or 0 for regex). The q11 grouped pages were fetched with `curl -sS -m 120 "https://codesearch.debian.net/search?q=%5E%5C%5BService%5C%5D+path%3A%5C.service&literal=0&perpkg=1&page=$p"` (p = 0, 1, 318), re-polled while the page contained `Still searching`, and counted with `sed 's/<style.*<\/style>//' $f | grep -c '^<h2>[a-z0-9]'`.

### A.2 `parse.py`
```python
# usage: python3 -I parse.py DIR  -> for all page_*.html of a Debian Code Search no-JS result set:
# prints hit count, unique files, unique source packages, and each hit as file:line | matched line
import sys,glob,re,urllib.parse,html
d=sys.argv[1]
hits=[]
for f in sorted(glob.glob(d+'/page_*.html'),key=lambda x:int(re.findall(r'page_(\d+)',x)[0])):
    t=open(f,encoding='utf-8').read()
    for m in re.finditer(r'<li><a href="/show\?file=([^&"]+)&(?:amp;)?line=(\d+)[^>]*>.*?<pre>\n?(.*?)</pre>',t,re.S):
        segs=m.group(3).split('<br>')
        ml=[s for s in segs if '<strong>' in s]
        line=html.unescape(re.sub(r'<[^>]+>','',ml[0] if ml else '')).strip()
        hits.append((urllib.parse.unquote(m.group(1)),m.group(2),line))
files=sorted({h[0] for h in hits})
pk=sorted({re.match(r'([^_/]+)_',x).group(1) for x in files})
nc=[h for h in hits if not h[2].lstrip().startswith(('#',';'))]
pknc=sorted({re.match(r'([^_/]+)_',h[0]).group(1) for h in nc})
print('hits',len(hits),'files',len(files),'packages',len(pk),'| uncommented hits',len(nc),'packages(uncommented)',len(pknc))
print('packages:',' '.join(pk))
print('packages(uncommented):',' '.join(pknc))
for h in hits: print('  %s:%s | %s'%h)
```

### A.3 value tabulations
```bash
python3 -I parse.py sources/S3-01/q07_cpupolicy_any_unit | sed -n '4,100p' | awk -F'|' '{print $2}' | sort | uniq -c | sort -rn
python3 -I parse.py sources/S3-01/q08_nice_any_unit | sed -n '4,200p' | awk -F'|' '{print $2}' | sed 's/ *#.*//' | sort | uniq -c | sort -rn
python3 -I parse.py sources/S3-01/q08_nice_any_unit | grep 'Nice=-'
```

### A.4 `ananicy_count.py` (run as `python3 -I ananicy_count.py sources/S3-03/ananicy-rules`)
```python
# usage: python3 -I ananicy_count.py REPO_ROOT
# Parses every *.rules file separately: one JSON object per non-blank line not starting with '#'.
import sys,os,json,collections,re
root=sys.argv[1]
types=collections.Counter(); bytop=collections.defaultdict(collections.Counter)
n=0; bad=[]; nofile=0; notype=collections.Counter(); names=[]
for dp,dn,fn in os.walk(root):
    if '.git' in dp: continue
    for f in fn:
        if not f.endswith('.rules'): continue
        nofile+=1
        p=os.path.join(dp,f); rel=os.path.relpath(p,root)
        top=rel.split(os.sep)[1] if rel.startswith('00-default'+os.sep) and rel.count(os.sep)>=2 else rel.split(os.sep)[0]
        for i,l in enumerate(open(p,encoding='utf-8'),1):
            s=l.strip()
            if not s or s.startswith('#'): continue
            try: o=json.loads(s)
            except Exception as e: bad.append((rel,i,s[:80])); continue
            n+=1
            t=o.get('type')
            if t is None: notype[tuple(sorted(k for k in o if k!='name'))]+=1; t='(no type: explicit fields)'
            types[t]+=1; bytop[top][t]+=1
            names.append((o.get('name',''),t,rel,i))
print('rules files',nofile,'entries',n,'unparseable',len(bad))
for b in bad[:20]: print('  BAD',b)
print('entries per type:')
for t,c in types.most_common(): print('  %-30s %d'%(t,c))
print('entries without "type", by field set:')
for k,c in notype.most_common(): print('  ',k,c)
print('entries per 00-default subdirectory (top 3 types):')
for top in sorted(bytop): print('  %-40s %5d  %s'%(top,sum(bytop[top].values()),bytop[top].most_common(3)))
pat=re.compile(sys.argv[2] if len(sys.argv)>2 else r'updatedb|locate|baloo|tracker|localsearch|miner|clam|freshclam|backup|borg|restic|timeshift|deja|duplicity|rsync|syncthing|snapper|indexer|recoll|akonadi|antivir|virus',re.I)
print('name matches for',pat.pattern)
for nm,t,rel,i in names:
    if pat.search(nm): print('  %s:%d  %s -> %s'%(rel,i,nm,t))
```

### A.5 `llmperf.py` and row extraction
```python
# usage: python3 -I llmperf.py CSV REGEX  -> rows with a prefill latency, model matching REGEX
import csv,sys,re
csv.field_size_limit(10**9)
rows=list(csv.DictReader(open(sys.argv[1])))
ok=[r for r in rows if r['report.prefill.latency.mean']]
print('rows',len(rows),'with prefill latency',len(ok))
pat=re.compile(sys.argv[2])
for r in ok:
    if pat.search(r['config.backend.model']):
        print(' | '.join([r['config.name'],r['config.backend.model'],r['config.backend.quantization_scheme'],r.get('config.backend.quantization_config.bits',''),'bs='+r['config.scenario.input_shapes.batch_size'],'seq='+r['config.scenario.input_shapes.sequence_length'],'new='+r['config.scenario.generate_kwargs.max_new_tokens'],'prefill_mean='+r['report.prefill.latency.mean']+' '+r['report.prefill.latency.unit'],'decode_tput='+r['report.decode.throughput.value']+' '+r['report.decode.throughput.unit'],'decode_lat_mean='+r['report.decode.latency.mean'],'gpu='+r['config.environment.gpu'],'cpu='+r['config.environment.cpu'].strip()]))
```
Run: `python3 -I llmperf.py perf-df-pytorch-cuda-awq-1xT4.csv '(?i)llama-3.*8b|mistral-7b|qwen2.*7b|llama-2-7b'`. The single-row printout in S3-04 came from an inline script that opens the CSV with `csv.reader`, finds the row with `config.name==4bit-awq-gemv-sdpa` and `config.backend.model==meta-llama/Llama-3.1-8B-Instruct`, prints `rd.line_num` (4509) and the listed columns.

### A.6 `localscore.py`
```python
# usage: python3 -I localscore.py model_N.html  -> per-accelerator averages from the page's __NEXT_DATA__ JSON
import re,json,sys,collections,statistics
t=open(sys.argv[1]).read()
d=json.loads(re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',t,re.S).group(1)); r=d['props']['pageProps']['result']
print(r['model'])
res=r['results']; print('accelerator entries',len(res), 'by type',collections.Counter(x['accelerator']['type'] for x in res))
for ty in ['CPU','GPU']:
    s=[x for x in res if x['accelerator']['type']==ty]
    if not s: continue
    tt=[x['avg_ttft'] for x in s]; g=[x['avg_gen_tps'] for x in s]
    print(ty,'n',len(s),'avg_ttft ms median %.0f min %.0f max %.0f'%(statistics.median(tt),min(tt),max(tt)),'| avg_gen_tps median %.2f min %.2f max %.2f'%(statistics.median(g),min(g),max(g)))
want=sys.argv[2:] 
for x in res:
    if any(w.lower() in x['accelerator']['name'].lower() for w in want):
        print('  %-55s %-4s ttft_ms=%.1f gen_tps=%.2f prompt_tps=%.1f rank=%s/%s'%(x['accelerator']['name'],x['accelerator']['type'],x['avg_ttft'],x['avg_gen_tps'],x['avg_prompt_tps'],x['performance_rank'],x['number_ranked']))
```
Run: `python3 -I localscore.py model_1.html 'Ryzen 7 7800X3D' 'i7-12700' …` (also model_2, model_3). Per-run test values came from an inline script that loads `__NEXT_DATA__` from `result_N.html` and prints `name, ttft_ms, gen_tps, prompt_tps, avg_time_ms` for each entry of `props.pageProps.result.results`.

### A.7 Perfetto trace_processor SQL (run as `./trace_processor_shell -q qN.sql example_android_trace_15s`)
```sql
select name, str_value, int_value from metadata;
select start_ts, end_ts, (end_ts-start_ts)/1e9 as dur_s from trace_bounds;
select cpu, count(*) as slices, min(ts) as first_ts, max(ts+dur) as last_end, round(count(*)/((max(ts+dur)-min(ts))/1e9),1) as slices_per_s, sum(case when utid=0 then 1 else 0 end) as idle_slices from sched group by cpu order by cpu;
select count(*) as total_slices, round(count(*)/((select end_ts-start_ts from trace_bounds)/1e9),1) as per_s_all_cpus from sched;
select name, str_value, int_value from metadata where name not like 'trace_config%';
select cpu, count(*) as slices, sum(case when t.tid=0 then 1 else 0 end) as swapper_slices from sched s join thread t using(utid) group by cpu order by cpu;
select count(*) as n from ftrace_event where name='sched_switch';
select cpu, max(freq) from cpu_frequency_counters group by cpu;
select count(*) as nonidle_slices, (select dur from sched s2 join thread t2 using(utid) where t2.tid!=0 and s2.dur>0 order by s2.dur limit 1 offset (select count(*)/2 from sched s3 join thread t3 using(utid) where t3.tid!=0 and s3.dur>0)) as median_dur_ns, avg(dur) as mean_dur_ns from sched s join thread t using(utid) where t.tid!=0 and s.dur>0;
```
(The `cpu_frequency_counters` query in q2 failed with "no such table"; the others ran.)

### A.8 `swell.py` (run as `python3 -I swell.py swell_ulog_features_sheet1.csv`)
```python
# usage: python3 -I swell.py CSV -> SnAppChange per minute aggregated to per hour, by condition and overall
import csv,sys,collections,statistics
rows=list(csv.DictReader(open(sys.argv[1],encoding='utf-8-sig')))
print('rows',len(rows),'participants',len({r['PP'] for r in rows}),'conditions',collections.Counter(r['Condition'] for r in rows))
vals=[float(r['SnAppChange']) for r in rows]
print('SnAppChange min',min(vals),'max',max(vals),'all integer',all(v==int(v) for v in vals))
by=collections.defaultdict(list)
for r in rows: by[r['Condition']].append(float(r['SnAppChange']))
for c,v in sorted(by.items()): print('condition',c,'minutes',len(v),'mean per minute %.3f -> per hour %.1f'%(statistics.mean(v),60*statistics.mean(v)),'median per minute',statistics.median(v))
pp=collections.defaultdict(list)
for r in rows:
    if r['Condition']!='R': pp[r['PP']].append(float(r['SnAppChange']))
ph=sorted(60*statistics.mean(v) for v in pp.values())
print('per-participant per-hour rate (work conditions N,I,T pooled): n',len(ph),'min %.1f median %.1f max %.1f'%(ph[0],statistics.median(ph),ph[-1]))
big=[(r['PP'],r['Condition'],r['timestamp'],r['SnAppChange']) for r in rows if float(r['SnAppChange'])>60]
print('minutes with SnAppChange>60:',len(big),big[:8])
for c,v in sorted(by.items()):
    w=[x for x in v if x<=60]
    print('condition',c,'excluding minutes >60: minutes',len(w),'mean per hour %.1f'%(60*statistics.mean(w)))
```

### A.9 `behacom.py` (run as `ls User*/User*_BEHACOM.csv | sort -V | xargs python3 -I behacom.py` inside the unzipped `Behacom/` folder)
```python
# usage: python3 -I behacom.py User*/User*_BEHACOM.csv
# Per user: number of one-minute vectors, first/last timestamp (UTC), mean changes_between_apps per vector (x60 = per hour of logged minutes),
# mean active_apps_average, and fraction of consecutive vectors (gap == 60 s +-5 s) whose active_apps_average differs.
import csv,sys,statistics,datetime
csv.field_size_limit(10**9)
allc=[];
for fn in sys.argv[1:]:
    with open(fn,newline='',encoding='latin-1') as f:
        rd=csv.reader(f); h=next(rd); it=h.index('timestamp'); ia=h.index('active_apps_average'); ic=h.index('changes_between_apps')
        ts=[];aa=[];ch=[]
        for r in rd:
            try: ts.append(int(float(r[it]))); aa.append(float(r[ia])); ch.append(float(r[ic]))
            except Exception: pass
    o=sorted(range(len(ts)),key=lambda i:ts[i]); ts=[ts[i] for i in o]; aa=[aa[i] for i in o]; ch=[ch[i] for i in o]
    pairs=[(aa[i-1],aa[i]) for i in range(1,len(ts)) if abs(ts[i]-ts[i-1]-60000)<=5000]
    diff=sum(1 for a,b in pairs if a!=b)
    d=lambda x: datetime.datetime.fromtimestamp(x/1000,datetime.UTC).strftime('%Y-%m-%d')
    allc+=ch
    print('%s vectors=%d span=%s..%s changes_between_apps mean/min=%.2f (=%.0f/h) median/min=%.1f active_apps_average mean=%.1f consecutive-pairs=%d with active_apps_average changed=%.1f%%'%(fn.split('/')[0],len(ts),d(ts[0]),d(ts[-1]),statistics.mean(ch),60*statistics.mean(ch),statistics.median(ch),statistics.mean(aa),len(pairs),100*diff/max(1,len(pairs))))
print('ALL users pooled: vectors=%d changes_between_apps mean per vector %.2f (=%.0f per hour of logged minutes)'%(len(allc),statistics.mean(allc),60*statistics.mean(allc)))
```

### A.10 Artificial Analysis extraction (inline)
```python
import re
t=open('aa_llama31_8b_providers.html',encoding='utf-8').read().replace('\\"','"')
seen=set()
for m in re.finditer(r'"performance":\{"outputSpeed":\{"median":([0-9.]+)[^}]*\},"timeToFirstToken":\{"median":([0-9.]+)',t):
    back=t[max(0,m.start()-6000):m.start()]
    hs=re.findall(r'"host":\{[^{}]*?"name":"([^"]+)"',back) or re.findall(r'"hostName":"([^"]+)"',back) or re.findall(r'"name":"([^"]+)"',back)
    key=(hs[-1] if hs else '?',m.group(1)[:6])
    if key in seen: continue
    seen.add(key)
    print(key[0],'| outputSpeed median',round(float(m.group(1)),1),'tok/s | TTFT median',round(float(m.group(2)),3),'s')
```
Output:
```
Groq | outputSpeed median 639.3 tok/s | TTFT median 0.84 s
Novita | outputSpeed median 150.8 tok/s | TTFT median 0.913 s
CoreWeave | outputSpeed median 141.5 tok/s | TTFT median 0.661 s
DeepInfra (Turbo, FP8) | outputSpeed median 30.9 tok/s | TTFT median 1.143 s
DeepInfra | outputSpeed median 27.5 tok/s | TTFT median 1.074 s
```
The Groq attribution was checked directly: `"slug":"groq_llama-3-1-instruct-8b"` precedes that performance block by 582 characters. The other four attributions are by nearest preceding host name and were not checked one by one.

### A.11 Local illustration (sandbox image, Ubuntu 24.04.5 LTS "Noble Numbat")
```
$ ls /lib/systemd/system/*.service /lib/systemd/system/*.timer /usr/lib/systemd/user/*.service /usr/lib/systemd/user/*.timer 2>/dev/null | wc -l
163
$ grep -HnE '^(CPUSchedulingPolicy|Nice|IOSchedulingClass|IOSchedulingPriority|CPUWeight|IOWeight)=' <same globs>
/lib/systemd/system/e2scrub@.service:16:IOSchedulingClass=idle
/lib/systemd/system/e2scrub@.service:17:CPUSchedulingPolicy=idle
/lib/systemd/system/e2scrub_reap.service:17:IOSchedulingClass=idle
/lib/systemd/system/e2scrub_reap.service:18:CPUSchedulingPolicy=idle
/lib/systemd/system/systemd-tmpfiles-clean.service:23:IOSchedulingClass=idle
/usr/lib/systemd/user/systemd-tmpfiles-clean.service:21:IOSchedulingClass=idle
```
So 3 of the 163 unit files in this minimal container image declare an idle class: e2scrub@, e2scrub_reap, and systemd-tmpfiles-clean (system and user). This is a labelled illustration only; the image is a minimal sandbox, not a desktop install.

### A.12 `count_at.py` (stage 3, 2026-10-08)
```python
"""Count rule entries at a commit: each .rules file parsed separately, one JSON object per non-blank, non-# line."""
import json, subprocess, sys, collections
repo, rev = sys.argv[1], sys.argv[2]
names = subprocess.run(['git', '-C', repo, 'ls-tree', '-r', '--name-only', rev], capture_output=True, text=True, check=True).stdout.split('\n')
files = [n for n in names if n.endswith('.rules')]
entries, bad, types = 0, 0, collections.Counter()
for f in files:
    blob = subprocess.run(['git', '-C', repo, 'show', f'{rev}:{f}'], capture_output=True, check=True).stdout.decode('utf-8', 'replace')
    for line in blob.split('\n'):
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        try:
            o = json.loads(s)
        except Exception:
            bad += 1
            continue
        if isinstance(o, dict) and 'name' in o:
            entries += 1
            types[o.get('type')] += 1
print(rev[:8], 'files', len(files), 'entries', entries, 'unparseable', bad, 'Game', types.get('Game', 0))
```
Run: `for d in 2022-12-31 2023-12-31 2024-12-31 2025-12-31 2026-03-31 2026-06-30; do c=$(git rev-list -1 --first-parent --before="$d 23:59:59" HEAD); python3 -I count_at.py . $c; done` in `sources/S3-19/ananicy-rules`.

### A.13 `blame_rules.py` (stage 3, 2026-10-08)
```python
"""Attribute each rule entry at HEAD to the commit that introduced its line (git blame -w -M -C)."""
import json, subprocess, sys, collections, pathlib, concurrent.futures as cf
repo = pathlib.Path(sys.argv[1])
files = sorted(p for p in repo.rglob('*.rules') if '.git' not in p.parts)
def blame(p):
    out = subprocess.run(['git', '-C', str(repo), 'blame', '--line-porcelain', '-w', '-M', '-C', '--', str(p.relative_to(repo))],
                         capture_output=True, text=True, check=True).stdout
    rows, cur = [], {}
    for line in out.split('\n'):
        if line.startswith('\t'):
            text = line[1:].strip()
            if text and not text.startswith('#'):
                try:
                    obj = json.loads(text)
                except Exception:
                    obj = None
                if isinstance(obj, dict) and 'name' in obj:
                    rows.append((cur['sha'], cur['author'], cur['time'], cur['summary'], obj.get('type'), str(p.relative_to(repo))))
            cur = {}
        elif not cur:
            cur['sha'] = line.split(' ')[0]
        elif line.startswith('author '):
            cur['author'] = line[7:]
        elif line.startswith('author-time '):
            cur['time'] = int(line.split()[1])
        elif line.startswith('summary '):
            cur['summary'] = line[8:]
    return rows
rows = []
with cf.ThreadPoolExecutor(8) as ex:
    for r in ex.map(blame, files):
        rows.extend(r)
print('files', len(files), 'entries', len(rows))
by_commit = collections.Counter((r[0][:8], r[1], r[3]) for r in rows)
by_author = collections.Counter(r[1] for r in rows)
print('commits introducing current entries', len(by_commit), 'authors', len(by_author))
print('top commits:')
for (sha, a, s), n in by_commit.most_common(15):
    print(f'  {n:6d} {sha} {a} | {s}')
print('top authors:')
for a, n in by_author.most_common(10):
    print(f'  {n:6d} {a}')
import datetime
yr = collections.Counter(datetime.datetime.utcfromtimestamp(r[2]).year for r in rows)
print('entries by year of introducing commit:', sorted(yr.items()))
n = len(rows); top = by_commit.most_common()
cum = 0
for i, (_, c) in enumerate(top, 1):
    cum += c
    if cum >= n / 2:
        print(f'commits covering half the entries: {i}'); break
```
Run: `python3 -I blame_rules.py ananicy-rules` in `sources/S3-19`. Output (summary lines verbatim):
```
files 361 entries 15813
commits introducing current entries 1214 authors 112
top authors: 9445 Luka Ogadze; 4048 pollux78; 1100 Shendisx; 204 jilv220; 71 Mach565; 68 NIICKTCHUNS; 62 Masum Reza; 62 Peter Jung; 47 pinitik1906; 46 miwakasa
entries by year of introducing commit: [(2022, 295), (2023, 85), (2024, 210), (2025, 146), (2026, 15077)]
commits covering half the entries: 22
```

### A.14 `names_vs_catalogue.py` (stage 3, 2026-10-08)
```python
"""Process names arriving in the compiled core set, matched against catalogue entry names at a commit.
Exact match, and match after truncating the entry name to 15 characters (the kernel's comm length)."""
import json, subprocess, sys, pathlib, collections
build, repo, rev = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3]
files_by_name = collections.defaultdict(set)
for f in sorted(build.glob('*.workload.json')):
    for e in json.loads(f.read_text())['events']:
        if e.get('op') == 'arrive' and 'name' in e:
            files_by_name[e['name']].add(f.name.split('.')[0])
cat = {}
for fn in subprocess.run(['git', '-C', repo, 'ls-tree', '-r', '--name-only', rev], capture_output=True, text=True, check=True).stdout.split('\n'):
    if not fn.endswith('.rules'): continue
    for line in subprocess.run(['git', '-C', repo, 'show', f'{rev}:{fn}'], capture_output=True, check=True).stdout.decode('utf-8', 'replace').split('\n'):
        s = line.strip()
        if not s or s.startswith('#'): continue
        try: o = json.loads(s)
        except Exception: continue
        if isinstance(o, dict) and 'name' in o: cat.setdefault(o['name'], o.get('type'))
trunc = {}
for n, t in cat.items(): trunc.setdefault(n[:15], (n, t))
nfiles = len(list(build.glob('*.workload.json')))
exact = [n for n in files_by_name if n in cat]
viatrunc = [n for n in files_by_name if n not in cat and n in trunc]
print(f'workload files {nfiles}; distinct arriving names {len(files_by_name)}; exact matches {len(exact)}; matches only after 15-char truncation {len(viatrunc)}')
for n in sorted(files_by_name, key=str.lower):
    tag = f'EXACT {cat[n]}' if n in cat else (f'TRUNC {trunc[n][0]} {trunc[n][1]}' if n in trunc else '-')
    print(f'  {n:18s} {tag:40s} files {len(files_by_name[n])}')
files_all = collections.Counter()
for f in sorted(build.glob('*.workload.json')):
    names = {e['name'] for e in json.loads(f.read_text())['events'] if e.get('op') == 'arrive' and 'name' in e}
    files_all[sum(1 for n in names if n in cat or n in trunc) == len(names)] += 1
print('files whose every arriving name matches (exact or truncated):', files_all[True], 'of', nfiles)
```
Run: `python3 -I names_vs_catalogue.py dataset/build/coreset-single <S3-19 clone> 03ef03fbf7e834385377432ccecaedd32e3414bb` from the repository root.

### A.15 `dcs_burst.sh` and `dcs_run2.sh` (stage 3, 2026-10-08)
```bash
#!/bin/bash
# Fetch every result page of one Debian Code Search query inside one cache window: page 0 until the search finishes,
# then all pages in parallel (8 at a time), then page 0 again; valid only if page 0's packages/hits are unchanged.
# usage: dcs_burst.sh OUTDIR PERPKG QUERY   (OUTDIR must not exist yet)
set -u
out=$1; perpkg=$2; q=$3
[ -e "$out" ] && { echo "EXISTS $out"; exit 1; }
mkdir -p "$out"; printf '%s\n' "$q" > "$out/query.txt"
enc=$(python3 -I -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1],safe=""))' "$q")
export base="https://codesearch.debian.net/search?q=$enc&literal=0&perpkg=$perpkg&page=" out
get() { for t in $(seq 1 30); do curl -sS -m 120 --retry 5 --retry-all-errors -o "$2" "$base$1" && [ -s "$2" ] && ! grep -q 'Still searching' "$2" && return 0; sleep 3; done; return 1; }
export -f get
get 0 "$out/page_0.html" || { echo "FAIL $out page 0"; exit 1; }
last=$(grep -o 'page=[0-9]*">[0-9]*<' "$out/page_0.html" | sed 's/page=\([0-9]*\).*/\1/' | sort -n | tail -1); last=${last:-0}
seq 1 "$last" | xargs -P 8 -I{} bash -c 'get {} "$out/page_{}.html" || echo "FAIL page {}"'
get 0 "$out/page_0_after.html"
sig() { grep -o -E '<h2>[^<]*</h2>|href="/show\?file=[^"]*' "$1" | md5; }
if [ "$(sig "$out/page_0.html")" = "$(sig "$out/page_0_after.html")" ]; then echo "$out pages $((last+1)) consistent"; else echo "$out pages $((last+1)) INCONSISTENT"; fi
```
```bash
#!/bin/bash
set -u
mkdir -p "$1/burst"; cd "$1/burst"
B=/private/tmp/claude-501/-Users-jiohin-Desktop-future-of-sw-LLM-driven-shceduling/a0ea6242-8fee-4db5-99ef-2a68c44081db/scratchpad/dcs_burst.sh
F=' -path:(^|/)(tests?|testsuite|testdata|examples?|samples?|demos?|contrib|docs?)/'
try() { for a in 1 2 3; do $B "$1.$a" "$2" "$3" | tee -a run.log | grep -q ' consistent$' && return 0; done; return 1; }
try denom_all 1 '^\[Service\] path:\.service'
try denom_F 1 "^\[Service\] path:\.service$F"
for kind in all F; do
  if [ $kind = F ]; then x="$F"; else x=''; fi
  try nice_$kind 0 "^\s*Nice= path:\.service$x"
  try ioclass_$kind 0 "^\s*IOSchedulingClass= path:\.service$x"
  try cpupolicy_$kind 0 "^\s*CPUSchedulingPolicy= path:\.service$x"
done
echo DCS_DONE | tee -a run.log
```
`burst/run.log`: `denom_all.1 pages 319 consistent` / `denom_F.1 pages 301 INCONSISTENT` / `denom_F.2 pages 301 consistent` / `nice_all.1 pages 7 consistent` / `ioclass_all.1 pages 8 consistent` / `cpupolicy_all.1 pages 5 consistent` / `nice_F.1 pages 7 consistent` / `ioclass_F.1 pages 6 consistent` / `cpupolicy_F.1 pages 3 consistent`.

### A.16 `installed_units_count.py` (stage 3, 2026-10-08)
```python
"""S3-20: declared scheduling classes over the systemd units Debian unstable installs.
usage: python3 -I installed_units_count.py S3_20_DIR
Denominator: source packages whose binaries (amd64 + all, main) install >= 1 systemd unit (.service) under
(usr/)lib/systemd/{system,user}/ — from Contents-{amd64,all}.gz, binary->source from Packages.xz.
Numerator: Debian Code Search hits (consistent runs, unfiltered) of an uncommented Nice= / IOSchedulingClass= /
CPUSchedulingPolicy= line in a source file whose installed name (basename without .in; drop-ins keep their
'<unit>.service.d/' parent) is among that source package's installed unit paths."""
import sys, re, gzip, lzma, glob, html, urllib.parse, pathlib, collections
root = pathlib.Path(sys.argv[1]); idx = root / 'debian-index'; burst = root / 'burst'
src_of = {}
for f in ('main_binary-amd64_Packages.xz', 'main_binary-all_Packages.xz'):
    for stanza in lzma.open(idx / f, 'rt', encoding='utf-8').read().split('\n\n'):
        m = re.search(r'^Package: (\S+)', stanza, re.M)
        if not m: continue
        s = re.search(r'^Source: (\S+)', stanza, re.M)
        src_of.setdefault(m.group(1), s.group(1) if s else m.group(1))
unit_re = re.compile(r'^(?:usr/)?lib/systemd/(system|user)/([^/]+\.service|[^/]+\.service\.d/[^/]+\.conf)$')
units = collections.defaultdict(set); kinds = collections.defaultdict(set); nobin = set()
for f in ('main_Contents-amd64.gz', 'main_Contents-all.gz'):
    for line in gzip.open(idx / f, 'rt', encoding='utf-8', errors='replace'):
        path, _, locs = line.rstrip('\n').rpartition(' ')
        path = path.strip()
        m = unit_re.match(path)
        if not m: continue
        for loc in locs.split(','):
            b = loc.rsplit('/', 1)[-1]
            s = src_of.get(b)
            if s is None: nobin.add(b); continue
            units[s].add(m.group(2)); kinds[s].add(m.group(1))
denom = {s for s, u in units.items() if any(x.endswith('.service') for x in u)}
print(f'denominator: source packages installing >= 1 .service unit: {len(denom)} '
      f'(system units {sum(1 for s in denom if "system" in kinds[s])}, user units {sum(1 for s in denom if "user" in kinds[s])}); '
      f'binary names in Contents without a Packages stanza: {len(nobin)}')
def pages(d): return sorted([x for x in glob.glob(str(burst / d / 'page_*.html')) if not x.endswith('_after.html')], key=lambda x: int(re.findall(r'page_(\d+)', x)[0]))
def hits(d):
    for f in pages(d):
        t = open(f, encoding='utf-8').read()
        for m in re.finditer(r'<li><a href="/show\?file=([^&"]+)&(?:amp;)?line=(\d+)[^>]*>.*?<pre>\n?(.*?)</pre>', t, re.S):
            segs = m.group(3).split('<br>'); ml = [s for s in segs if '<strong>' in s]
            yield urllib.parse.unquote(m.group(1)), int(m.group(2)), html.unescape(re.sub(r'<[^>]+>', '', ml[0] if ml else '')).strip()
def direction(key, v):
    v = v.strip().strip('"').lower()
    if key == 'nice':
        try: n = int(v)
        except ValueError: return 'other'
        return 'lower' if n > 0 else 'raise' if n < 0 else 'zero'
    if key == 'cpupolicy': return 'lower' if v in ('idle', 'batch') else 'raise' if v in ('rr', 'fifo') else 'other'
    return 'lower' if v in ('idle', '3') else 'raise' if v in ('realtime', '1') else 'other'
# renames documented in the source's build files (read through Debian Code Search):
# snapper_0.10.6-1.3/data/Makefile.am:29 'install -D -m 644 cleanup.service $(DESTDIR)/usr/lib/systemd/system/snapper-cleanup.service'
RENAME = {('snapper', 'cleanup.service'): 'snapper-cleanup.service'}
DIRS = {'nice': ('nice_all.1', 'Nice='), 'ioclass': ('ioclass_all.1', 'IOSchedulingClass='), 'cpupolicy': ('cpupolicy_all.1', 'CPUSchedulingPolicy=')}
anyp = collections.defaultdict(set); unmatched = collections.Counter(); per = {}
for key, (d, directive) in DIRS.items():
    pk = collections.defaultdict(set); vals = collections.Counter(); n_inst = 0; n_hits = 0
    for path, ln, line in hits(d):
        n_hits += 1
        m = re.match(r'\s*' + re.escape(directive) + r'(.*)$', line)
        if not m: continue
        v = m.group(1).split('#')[0].strip()
        src = re.match(r'([^_/]+)_', path).group(1)
        parts = path.split('/'); base = re.sub(r'\.(in|cmake|tmpl)$', '', parts[-1])
        cands = {(parts[-2] + '/' + base) if parts[-2].endswith('.service.d') else base}
        if len(parts) >= 3 and parts[1] == 'debian':
            # debhelper: debian/<binary>.<unit>.service installs <unit>.service; debian/<binary>.service installs <binary>.service
            segs = base.split('.')
            if len(segs) >= 3: cands.add('.'.join(segs[1:]))
        cands |= {RENAME[(src, base)]} if (src, base) in RENAME else set()
        inst = units.get(src, set())
        if cands & inst:
            n_inst += 1; vals[v] += 1; dirn = direction(key, v); pk[src].add(dirn); anyp[src].add(dirn)
        else:
            unmatched[(src, path)] += 1
    low = {p for p, s in pk.items() if 'lower' in s}; rai = {p for p, s in pk.items() if 'raise' in s}
    per[key] = (pk, low, rai)
    print(f'{directive:22s} hits {n_hits:3d}, in installed units {n_inst:3d}; packages {len(pk):3d} ({100*len(pk)/len(denom):.1f} %), '
          f'lowering {len(low)} ({100*len(low)/len(denom):.1f} %), raising {len(rai)} ({100*len(rai)/len(denom):.1f} %)')
    print('   values:', ', '.join(f'{k or "(empty)"} x{c}' for k, c in vals.most_common()))
    print('   lowering:', ' '.join(sorted(low))); print('   raising:', ' '.join(sorted(rai)))
A = set(anyp); low = {p for p, s in anyp.items() if 'lower' in s}; rai = {p for p, s in anyp.items() if 'raise' in s}
print(f'ANY of the three: {len(A)} packages ({100*len(A)/len(denom):.1f} % of {len(denom)}); lowering {len(low)} ({100*len(low)/len(denom):.1f} %); '
      f'raising {len(rai)} ({100*len(rai)/len(denom):.1f} %); lowering only {len(low - rai)}, raising only {len(rai - low)}, both {len(low & rai)}')
print(f'hits not matched to an installed unit: {sum(unmatched.values())} lines in {len(unmatched)} files')
for (s, p), c in sorted(unmatched.items()): print('   ', p, f'x{c}')
```
Run: `python3 -I installed_units_count.py sources/S3-20`.

### A.17 `switch_rates.py`, `summarize.py` and `busy_share.py` (stage 3, 2026-10-09)

```python
#!/usr/bin/env python3
"""Context switches per second on the measured CPU, from the campaigns' `perf sched timehist --state` files
(9.12 stage 3, search record S3-21). A timehist row is one switch-out on the CPU in its second column, `<idle>`
included; every CPU is recorded (`perf sched record -a`). Per phase file: the rows on the repeat's load CPU
(`pin.load_cpu`) over the file's span, first row to last. Kept: gate `open`, `machine.model` containing EPYC 7763;
one row per (run id, family, app, repeat, phase), the first path found; rows sorted by path.

    switch_rates.py <root>   → TSV on stdout: run, family, app, mode, repeat, phase, load_cpu, span_s, rows, per_s,
                               and the other CPUs' rates
"""
import collections, glob, gzip, json, multiprocessing, os, re, sys

ROW = re.compile(rb"^\s*([0-9]+\.[0-9]+)\s+\[([0-9]+)\]\s")


def count(job):
    """One phase file: rows per CPU and the span, first row to last."""
    th, cpu, fields = job
    counts, t_first, t_last = collections.Counter(), None, None
    try:
        with gzip.open(th, "rb") as fh:
            for line in fh:
                m = ROW.match(line)
                if not m:
                    continue
                t = float(m.group(1)); counts[int(m.group(2))] += 1
                t_first = t if t_first is None else t_first
                t_last = t
    except (OSError, EOFError):
        return None
    if t_first is None or t_last <= t_first:
        return None
    span = t_last - t_first
    other = ",".join(f"{c}:{n / span:.1f}" for c, n in sorted(counts.items()) if c != cpu)
    return "\t".join(str(x) for x in fields + [cpu, f"{span:.3f}", counts[cpu], f"{counts[cpu] / span:.1f}", other,
                                               os.path.relpath(th, sys.argv[1])])


def build_jobs(root):
    jobs, seen = [], set()
    for rep in sorted(glob.glob(os.path.join(root, "**", "report.json"), recursive=True)):
        d = os.path.dirname(rep)
        try:
            r = json.load(open(rep))
        except ValueError:
            continue
        if r.get("gate") != "open" or "EPYC 7763" not in r.get("machine.model", ""):
            continue
        try:
            run = json.load(open(os.path.join(d, "spec.json")))["github_run"]["GITHUB_RUN_ID"]
        except (OSError, ValueError, KeyError, TypeError):
            run = "?"
        cpu = int(r.get("pin.load_cpu", "-1"))
        for th in sorted(glob.glob(os.path.join(d, "perf.*.timehist.txt.gz"))):
            phase = os.path.basename(th)[len("perf."):-len(".timehist.txt.gz")]
            key = (run, r.get("family"), r.get("app"), r.get("repeat"), phase)
            if key in seen:
                continue
            seen.add(key)
            jobs.append((th, cpu, [run, r.get("family"), r.get("app"), r.get("mode"), r.get("repeat"), phase]))

    return jobs


if __name__ == "__main__":
    print("\t".join(["run", "family", "app", "mode", "repeat", "phase", "load_cpu", "span_s", "rows", "per_s", "other_cpus_per_s", "path"]))
    jobs = build_jobs(sys.argv[1])
    with multiprocessing.Pool(8) as pool:
        rows = [x for x in pool.map(count, jobs, chunksize=4) if x]
    for row in sorted(rows, key=lambda x: x.rsplit("\t", 1)[1]):
        print(row)
```

```python
#!/usr/bin/env python3
"""Summarise rates.tsv (switch_rates.py): per (family, app, phase), over the full-mode repeats, the measured CPU's
context switches per second — repeats, median, min, max — and the same over every row.

    summarize.py rates.tsv   → table on stdout
"""
import collections, csv, statistics, sys
rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
full = [r for r in rows if r["mode"] == "full"]
g = collections.defaultdict(list)
for r in full:
    g[(r["family"], r["app"], r["phase"])].append(float(r["per_s"]))
print(f"rows {len(rows)}, full-mode {len(full)}, groups {len(g)}")
print(f"{'family':12} {'app':24} {'phase':16} {'n':>4} {'median':>9} {'min':>9} {'max':>9}")
for k in sorted(g, key=lambda k: -statistics.median(g[k])):
    v = g[k]
    print(f"{str(k[0]):12} {str(k[1]):24} {k[2]:16} {len(v):>4} {statistics.median(v):>9.1f} {min(v):>9.1f} {max(v):>9.1f}")
meds = [statistics.median(v) for v in g.values()]
print(f"group medians: min {min(meds):.1f}, median {statistics.median(meds):.1f}, max {max(meds):.1f}")
allv = [float(r["per_s"]) for r in full]
q = sorted(allv)
print(f"full-mode phase files: n {len(q)}, p10 {q[len(q)//10]:.1f}, p50 {statistics.median(q):.1f}, p90 {q[9*len(q)//10]:.1f}, max {q[-1]:.1f}")
```

```python
#!/usr/bin/env python3
"""The measured CPU's busy share per phase, from the campaigns' timehist files (search record S3-21): one minus the
`<idle>` task's run time on the load CPU over the file's span, first row to last. Same selection as switch_rates.py
(gate open, EPYC 7763, one row per run/family/app/repeat/phase), restricted to the families and phases named.

    busy_share.py <root> <family> <phase>...   → per phase: repeats, busy share min–max and median
"""
import glob, gzip, json, os, re, statistics, sys

ROW = re.compile(rb"^\s*([0-9]+\.[0-9]+)\s+\[([0-9]+)\]\s+(\S.*?)\s+([0-9]+\.[0-9]+)\s+([0-9]+\.[0-9]+)\s+([0-9]+\.[0-9]+)\s")
root, family, phases = sys.argv[1], sys.argv[2], sys.argv[3:]
res, seen = {p: [] for p in phases}, set()
for rep in sorted(glob.glob(os.path.join(root, "**", "report.json"), recursive=True)):
    d = os.path.dirname(rep)
    r = json.load(open(rep))
    if r.get("gate") != "open" or "EPYC 7763" not in r.get("machine.model", "") or r.get("family") != family or r.get("mode") != "full":
        continue
    run = json.load(open(os.path.join(d, "spec.json")))["github_run"]["GITHUB_RUN_ID"]
    cpu = int(r.get("pin.load_cpu", "-1"))
    for p in phases:
        th = os.path.join(d, f"perf.{p}.timehist.txt.gz")
        key = (run, r.get("repeat"), p)
        if not os.path.exists(th) or key in seen:
            continue
        seen.add(key)
        idle, t0, t1 = 0.0, None, None
        with gzip.open(th, "rb") as fh:
            for line in fh:
                m = ROW.match(line)
                if not m:
                    continue
                t = float(m.group(1)); t0 = t if t0 is None else t0; t1 = t
                if int(m.group(2)) == cpu and m.group(3).startswith(b"<idle>"):
                    idle += float(m.group(6)) / 1000.0
        if t0 is not None and t1 > t0:
            res[p].append(1 - idle / (t1 - t0))
for p, v in res.items():
    if v:
        print(f"{family} {p}: repeats {len(v)}, busy share {min(v):.4f}–{max(v):.4f}, median {statistics.median(v):.4f}")
```

### A.18 `m1_run.sh` and `summarize_llm.py` (stage 3, 2026-10-09)

```bash
#!/usr/bin/env bash
# m1_run.sh <scratch> <repo> <repeats> — the 9.12 latency request on the development Mac (Apple M1 Pro), search
# record S3-22: llama.cpp at bd4eeaa0 built with Metal; per repeat and model, llama-server with its default GPU
# offload, the time to /health, dataset/tools/meas/llm/request.py's five requests per schema, then llama-bench.
set -u
S="$1"; REPO="$2"; N="$3"; OUT="$(cd "$(dirname "$0")" && pwd)"
BIN="$S/llama.cpp/build/bin"
now_ms() { python3 -c 'import time; print(int(time.time()*1000))'; }
for k in $(seq 1 "$N"); do
  for m in "qwen2.5-3b:qwen2.5-3b-instruct-q4_k_m.gguf" "llama3.1-8b:Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"; do
    name="${m%%:*}"; file="${m#*:}"; R="$OUT/r$k"; mkdir -p "$R"
    t0=$(now_ms)
    "$BIN/llama-server" -m "$S/models/$file" -c 4096 -np 1 --host 127.0.0.1 --port 8091 > "$R/server.$name.log" 2>&1 &
    SPID=$!
    up=0
    for _ in $(seq 1 600); do
      if curl -sf http://127.0.0.1:8091/health > /dev/null 2>&1; then up=1; break; fi
      kill -0 "$SPID" 2>/dev/null || break
      sleep 0.2
    done
    echo "repeat=$k model=$name up=$up load_ms=$(( $(now_ms) - t0 ))" >> "$OUT/loads.txt"
    [ "$up" = 1 ] && python3 -I "$REPO/dataset/tools/meas/llm/request.py" http://127.0.0.1:8091 "$REPO/dataset/tools/meas/llm" 5 > "$R/requests.$name.jsonl" 2> "$R/requests.$name.err"
    kill "$SPID" 2>/dev/null; wait "$SPID" 2>/dev/null
    "$BIN/llama-bench" -m "$S/models/$file" -p 512 -n 64 -r 3 -o json > "$R/bench.$name.json" 2> "$R/bench.$name.err"
  done
done
echo done >> "$OUT/loads.txt"
```

```python
#!/usr/bin/env python3
"""Summarise llm/request.py outputs (search record S3-22, and the runner repeats of meas-ci:costs): per model and
schema, over the repeats (r<k>/ folders or artifact folders), the mean over each repeat's five requests of the wall
time, prompt and generation times and token counts, then min–max and mean across repeats; the llama-bench rates;
and whether the answers are identical across every request and repeat.

    summarize_llm.py <dir of repeat folders>
"""
import collections, glob, json, os, statistics, sys
root = sys.argv[1]
per = collections.defaultdict(lambda: collections.defaultdict(list))
answers = collections.defaultdict(set)
bench = collections.defaultdict(lambda: collections.defaultdict(list))
for path in sorted(glob.glob(os.path.join(root, "**", "requests.*.jsonl"), recursive=True)):
    model = os.path.basename(path)[len("requests."):-len(".jsonl")]
    rows = [json.loads(x) for x in open(path) if x.strip()]
    reqs = [r for r in rows if r.get("kind") == "request" and r.get("label") != "warmup" and r.get("timings")]
    for schema in ("system", "full"):
        rs = [r for r in reqs if r["schema"] == schema]
        if not rs:
            continue
        for key, f in (("wall_ms", lambda r: r["wall_ms"]), ("prompt_n", lambda r: r["timings"]["prompt_n"]),
                       ("prompt_ms", lambda r: r["timings"]["prompt_ms"]), ("predicted_n", lambda r: r["timings"]["predicted_n"]),
                       ("predicted_ms", lambda r: r["timings"]["predicted_ms"])):
            per[(model, schema)][key].append(statistics.fmean(f(r) for r in rs))
        for r in rs:
            answers[(model, schema)].add(r["content"])
    b = os.path.join(os.path.dirname(path), f"bench.{model}.json")
    try:
        for x in json.load(open(b)):
            tag = f"pp{x['n_prompt']}" if x.get("n_prompt") and not x.get("n_gen") else f"tg{x['n_gen']}"
            bench[model][tag].append(x["avg_ts"])
    except (OSError, ValueError, KeyError):
        pass
for (model, schema), d in sorted(per.items()):
    k = len(d["wall_ms"])
    line = f"{model:12} {schema:6} repeats {k}: " + ", ".join(
        f"{key} {statistics.fmean(v):.1f} ({min(v):.1f}–{max(v):.1f})" for key, v in d.items())
    print(line)
    print(f"{'':19} distinct answers over every request: {len(answers[(model, schema)])}")
for model, d in sorted(bench.items()):
    print(f"{model:12} bench: " + ", ".join(f"{t} {statistics.fmean(v):.2f} t/s ({min(v):.2f}–{max(v):.2f}, n {len(v)})" for t, v in sorted(d.items())))
```

## Appendix B — long outputs (verbatim)

### B.1 Negative `Nice=` hits (q08)
```
  systemd_262-1/debian/extra/units-ubuntu/systemd-journald.service.d/nice.conf:4 | Nice=-1
  brltty_6.9.1+repack-2/Autostart/Systemd/brltty@.service.in:62 | Nice=-10
  brltty_6.9.1+repack-2/debian/brltty.service:30 | Nice=-10
  svxlink_26.05.1-1/src/svxlink/systemd/svxlink.service.in:50 | Nice=-10
  svxlink_26.05.1-1/src/svxlink/systemd/svxreflector.service.in:48 | Nice=-10
  svxlink_26.05.1-1/src/svxlink/systemd/remotetrx.service.in:44 | Nice=-10
  frr_10.7.1-2/tools/frr@.service.in:10 | Nice=-5
  frr_10.7.1-2/tools/frr.service.in:10 | Nice=-5
  espeakup_1:0.90-18/services/systemd/espeakup.service.in:16 | Nice=-10
  jacktrip_3.0.1+ds-1/linux/container/jacktrip.service:13 | Nice=-20
  earlyoom_1.9.0-1/earlyoom.service.in:12 | Nice=-20
  deepin-boot-maker_6.0.19+dfsg-1/src/service/data/deepin-boot-maker.service:52 | Nice=-5
  jamulus_3.9.1+dfsg-2/linux/debian/jamulus-headless.service:13 | Nice=-20
  hdapsd_1:20250908-1/misc/hdapsd@.service.in:7 | Nice=-5
  hdapsd_1:20250908-1/misc/hdapsd.service.in:7 | Nice=-5
  readsb_3.16-2/debian/readsb.service:23 | Nice=-5
  deepin-log-viewer_6.5.33+ds1-1/application/configs/coredump-reporter.service:12 | Nice=-5
  deepin-log-viewer_6.5.33+ds1-1/logViewerService/assets/data/deepin-log-viewer-daemon.service:21 | Nice=-5
  gdnsd_3.8.3-2.1/init/gdnsd.service.tmpl:34 | Nice=-11
  railcontrol_026+dfsg1-3/debian/railcontrol.service:25 | Nice=-20
```

### B.1b q07 non-idle/batch hits
```
  systemd_262-1/test/test-sched-prio/sched_rr_change.service:10 | CPUSchedulingPolicy=rr
  systemd_262-1/test/test-sched-prio/sched_rr_ok.service:7 | CPUSchedulingPolicy=rr
  systemd_262-1/test/test-sched-prio/sched_rr_bad.service:9 | CPUSchedulingPolicy=rr
  systemd_262-1/test/test-sched-prio/sched_ext_ok.service:8 | CPUSchedulingPolicy=ext
  systemd_262-1/test/fuzz/fuzz-unit-file/directives-all.service:786 | CPUSchedulingPolicy=
  hipercontracer_2.2.10-1/src/udp-echo-server.service:46 | CPUSchedulingPolicy=fifo
  low-memory-monitor_2.1-3/data/low-memory-monitor.service.in:12 | CPUSchedulingPolicy=fifo
  osmo-mgw_1.15.0+dfsg1-1/contrib/systemd/osmo-mgw.service:18 | CPUSchedulingPolicy=rr
  coturn_4.18.0-1/rpm/turnserver.service.fc:21 | CPUSchedulingPolicy=other
  osmo-bts_1.9.0+dfsg1-2/contrib/systemd/osmo-bts-virtual.service:18 | CPUSchedulingPolicy=rr
  osmo-bts_1.9.0+dfsg1-2/contrib/systemd/osmo-bts-trx.service:18 | CPUSchedulingPolicy=rr
  osmo-bts_1.9.0+dfsg1-2/contrib/systemd/osmo-bts-oc2g.service:16 | CPUSchedulingPolicy=rr
  osmo-bts_1.9.0+dfsg1-2/contrib/systemd/osmo-bts-sysmo.service:18 | CPUSchedulingPolicy=rr
  osmo-bts_1.9.0+dfsg1-2/contrib/systemd/osmo-bts-lc15.service:16 | CPUSchedulingPolicy=rr
  osmo-bts_1.9.0+dfsg1-2/debian/osmo-bts.service:14 | CPUSchedulingPolicy=rr
  osmo-pcu_1.5.3-1/debian/osmo-pcu.service:14 | CPUSchedulingPolicy=rr
  osmo-pcu_1.5.3-1/contrib/systemd/osmo-pcu.service:17 | CPUSchedulingPolicy=rr
  osmo-trx_1.8.0-1/contrib/systemd/osmo-trx-usrp1.service:17 | CPUSchedulingPolicy=rr
  osmo-trx_1.8.0-1/contrib/systemd/osmo-trx-lms.service:17 | CPUSchedulingPolicy=rr
  osmo-trx_1.8.0-1/contrib/systemd/osmo-trx-uhd.service:18 | CPUSchedulingPolicy=rr
  osmo-trx_1.8.0-1/contrib/systemd/osmo-trx-ipc.service:17 | CPUSchedulingPolicy=rr
  systemd-udeb_262-1/test/test-sched-prio/sched_rr_change.service:10 | CPUSchedulingPolicy=rr
  systemd-udeb_262-1/test/test-sched-prio/sched_rr_bad.service:9 | CPUSchedulingPolicy=rr
  systemd-udeb_262-1/test/test-sched-prio/sched_ext_ok.service:8 | CPUSchedulingPolicy=ext
  systemd-udeb_262-1/test/test-sched-prio/sched_rr_ok.service:7 | CPUSchedulingPolicy=rr
  nohang_0.3.0-3/debian/nohang.service:57 | #CPUSchedulingPolicy=rr
  nohang_0.3.0-3/systemd/nohang-desktop.service.in:57 | #CPUSchedulingPolicy=rr
  nohang_0.3.0-3/debian/nohang-desktop.service:57 | #CPUSchedulingPolicy=rr
  nohang_0.3.0-3/systemd/nohang.service.in:57 | #CPUSchedulingPolicy=rr
  systemd-udeb_262-1/test/fuzz/fuzz-unit-file/directives-all.service:786 | CPUSchedulingPolicy=
```

### B.2 `ananicy_count.py` full output
```
rules files 361 entries 15813 unparseable 1
  BAD ('00-default/Games/linux-native/linux-native_d.rules', 315, '{ "name": "Dungeon Drafters.x86_64", "type": "Game" }+')
entries per type:
  Game                           13528
  BG_CPUIO                       1615
  Service                        194
  Doc-View                       160
  LowLatency_RT                  109
  Chat                           51
  Heavy_CPU                      33
  Image-View                     32
  Player-Audio                   28
  Launcher                       24
  Player-Video                   24
  IN_DIFF                        10
  OOM_NO_KILL                    2
  (no type: explicit fields)     2
  TODO                           1
entries without "type", by field set:
   ('nice',) 1
   ('ioclass', 'nice') 1
entries per 00-default subdirectory (top 3 types):
  Audio-Video                                 62  [('Player-Video', 20), ('Player-Audio', 19), ('BG_CPUIO', 7)]
  Browsers                                    44  [('Doc-View', 42), ('BG_CPUIO', 2)]
  Chats                                       50  [('Chat', 50)]
  Creative                                    27  [('Player-Audio', 9), ('Image-View', 9), ('Player-Video', 4)]
  DEs-and-WMs                                184  [('LowLatency_RT', 72), ('Service', 42), ('BG_CPUIO', 29)]
  Development & Programming                   35  [('BG_CPUIO', 22), ('Heavy_CPU', 9), ('Service', 2)]
  Document Viewers                             3  [('Doc-View', 3)]
  Games                                    15093  [('Game', 13528), ('BG_CPUIO', 1453), ('Service', 80)]
  Networking                                  57  [('BG_CPUIO', 40), ('LowLatency_RT', 13), ('Service', 2)]
  Productivity & Office                       23  [('Doc-View', 21), ('Heavy_CPU', 2)]
  Services                                    77  [('Service', 61), ('BG_CPUIO', 13), ('LowLatency_RT', 3)]
  System Utilities & Maintenance              26  [('BG_CPUIO', 23), ('Service', 1), ('(no type: explicit fields)', 1)]
  Terminals & Shells                          33  [('Doc-View', 33)]
  Text Editors                                39  [('Doc-View', 28), ('Heavy_CPU', 11)]
  Tools                                       48  [('BG_CPUIO', 24), ('Doc-View', 11), ('Heavy_CPU', 6)]
  VPN                                         12  [('LowLatency_RT', 6), ('IN_DIFF', 6)]
name matches for updatedb|locate|baloo|tracker|localsearch|miner|clam|freshclam|backup|borg|restic|timeshift|deja|duplicity|rsync|syncthing|snapper|indexer|recoll|akonadi|antivir|virus
  00-default/DEs-and-WMs/plasma.rules:12  baloo_file -> BG_CPUIO
  00-default/DEs-and-WMs/plasma.rules:13  baloorunner -> BG_CPUIO
  00-default/DEs-and-WMs/plasma.rules:14  baloo_file_extractor -> BG_CPUIO
  00-default/Audio-Video/gpu-screen-recorder.rules:4  gsr-game-tracker -> BG_CPUIO
  00-default/Networking/syncthing.rules:2  syncthing -> BG_CPUIO
  00-default/Networking/syncthing.rules:3  syncthing-gtk -> BG_CPUIO
  00-default/Tools/rsync.rules:1  rsync -> BG_CPUIO
  00-default/System Utilities & Maintenance/clamav.rules:2  clamd -> BG_CPUIO
  00-default/System Utilities & Maintenance/clamav.rules:4  clamui -> Service
  00-default/System Utilities & Maintenance/borg.rules:2  borg -> BG_CPUIO
  00-default/System Utilities & Maintenance/recoll.rules:2  recollindex -> BG_CPUIO
  00-default/System Utilities & Maintenance/restic.rules:2  restic -> BG_CPUIO
  00-default/Games/linux-native/linux-native_f.rules:15  FACEMINER -> Game
  00-default/Games/linux-native/linux-native_i.rules:16  Idle Cave Miner.x86_64 -> Game
  00-default/Games/linux-native/linux-native_the.rules:288  TheZachtronicsSolitaireCollection -> Game
  00-default/Games/linux-native/linux-native_a.rules:210  AntiVirus Girl.x86_64 -> Game
  00-default/Games/linux-native/linux-native_m.rules:292  MurderMiners -> Game
  00-default/Games/wine_proton/wine_proton_c.rules:448  CastleMinerZ.exe -> Game
  00-default/Games/wine_proton/wine_proton_m.rules:969  Mineral Mining Simulator.exe -> Game
  00-default/Games/wine_proton/wine_proton_m.rules:1412  MooseMiners.exe -> Game
  00-default/Games/wine_proton/wine_proton_m.rules:1701  Murder Miners.exe -> Game
  00-default/Games/wine_proton/wine_proton_f.rules:76  FACEMINER.exe -> Game
  00-default/Games/wine_proton/wine_proton_x.rules:80  Xvirus.exe -> Game
  00-default/Games/wine_proton/wine_proton_s.rules:2768  STORY OF SEASONS Friends of Mineral Town.exe -> Game
  00-default/Games/wine_proton/wine_proton_s.rules:2769  STORY OF SEASONS Friends of Mineral Town_Compatibility.exe -> Game
  00-default/Games/wine_proton/wine_proton_t.rules:728  TimeShift.Exe -> Game
  00-default/Games/wine_proton/wine_proton_a.rules:936  AntiVirus Girl.exe -> Game
  00-default/Games/wine_proton/wine_proton_k.rules:218  Kiborg-Win64-Shipping.exe -> Game
  00-default/Games/wine_proton/wine_proton_k.rules:219  Kiborg.exe -> BG_CPUIO
  00-default/Games/wine_proton/wine_proton_d.rules:1245  DO NOT FEED THE VIRUS.exe -> Game
  00-default/Games/wine_proton/wine_proton_n.rules:533  NOBACKUP.exe -> BG_CPUIO
  00-default/Games/wine_proton/wine_proton_n.rules:534  NOBACKUP-Win64-Shipping.exe -> Game
  00-default/Games/wine_proton/wine_proton_n.rules:821  NTR_DejaVu.exe -> BG_CPUIO
  00-default/Games/wine_proton/wine_proton_n.rules:822  NTR_DejaVu-Win64-Shipping.exe -> Game
  00-default/Games/wine_proton/wine_proton_i.rules:73  Idle Cave Miner.exe -> Game
  00-default/Games/wine_proton/wine_proton_q.rules:44  CookerSync.exe -> BG_CPUIO
  00-default/Games/wine_proton/common.rules:218  BeamEyeTracker.exe -> Game
  00-default/Games/wine_proton/wine_proton_z.rules:157  Zomborg.exe -> Game
```

### B.3 `llmperf.py` output (Llama-3/3.1-8B rows, AWQ, 1xT4)
```
rows 1362 with prefill latency 427
4bit-awq-gemm-eager | meta-llama/Meta-Llama-3-8B-Instruct | awq | 4 | bs=1 | seq=256 | new=64 | prefill_mean=0.40531998901367183 s | decode_tput=22.27493301865801 tokens/s | decode_lat_mean=2.8282913330078125 | gpu=['Tesla T4'] | cpu=Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
4bit-awq-exllama-v1-sdpa | meta-llama/Meta-Llama-3-8B | awq | 4 | bs=1 | seq=256 | new=64 | prefill_mean=3.235117993164063 s | decode_tput=33.28901257083097 tokens/s | decode_lat_mean=1.8925163330078125 | gpu=['Tesla T4'] | cpu=Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
4bit-awq-exllama-v2-sdpa | meta-llama/Meta-Llama-3-8B | awq | 4 | bs=1 | seq=256 | new=64 | prefill_mean=0.21179373321533204 s | decode_tput=32.918606701295445 tokens/s | decode_lat_mean=1.9138112548828126 | gpu=['Tesla T4'] | cpu=Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
4bit-awq-gemv-eager | meta-llama/Meta-Llama-3-8B-Instruct | awq | 4 | bs=1 | seq=256 | new=64 | prefill_mean=0.3746915832519532 s | decode_tput=27.371389720982876 tokens/s | decode_lat_mean=2.3016734130859375 | gpu=['Tesla T4'] | cpu=Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
4bit-awq-gemv-eager | meta-llama/Llama-3.1-8B-Instruct | awq | 4 | bs=1 | seq=256 | new=64 | prefill_mean=0.3761126342773437 s | decode_tput=27.090488865596804 tokens/s | decode_lat_mean=2.3255394287109374 | gpu=['Tesla T4'] | cpu=Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
4bit-awq-gemm-eager | meta-llama/Llama-3.1-8B-Instruct | awq | 4 | bs=1 | seq=256 | new=64 | prefill_mean=0.40519516296386715 s | decode_tput=22.024580134036633 tokens/s | decode_lat_mean=2.8604404541015627 | gpu=['Tesla T4'] | cpu=Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
4bit-awq-exllama-v2-eager | meta-llama/Meta-Llama-3-8B | awq | 4 | bs=1 | seq=256 | new=64 | prefill_mean=0.2200324401855469 s | decode_tput=28.465174571799047 tokens/s | decode_lat_mean=2.21323076171875 | gpu=['Tesla T4'] | cpu=Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
4bit-awq-gemm-eager | meta-llama/Meta-Llama-3-8B | awq | 4 | bs=1 | seq=256 | new=64 | prefill_mean=0.4094328796386718 s | decode_tput=22.44153612753104 tokens/s | decode_lat_mean=2.8072944580078127 | gpu=['Tesla T4'] | cpu=Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
4bit-awq-exllama-v1-sdpa | meta-llama/Llama-3.1-8B-Instruct | awq | 4 | bs=1 | seq=256 | new=64 | prefill_mean=3.2326163085937503 s | decode_tput=33.312253482330604 tokens/s | decode_lat_mean=1.8911959838867187 | gpu=['Tesla T4'] | cpu=Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
4bit-awq-gemv-sdpa | meta-llama/Meta-Llama-3-8B | awq | 4 | bs=1 | seq=256 | new=64 | prefill_mean=0.3682376434326172 s | decode_tput=31.411470420974908 tokens/s | decode_lat_mean=2.005636767578125 | gpu=['Tesla T4'] | cpu=Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
4bit-awq-gemm-sdpa | meta-llama/Meta-Llama-3-8B-Instruct | awq | 4 | bs=1 | seq=256 | new=64 | prefill_mean=0.41649641723632813 s | decode_tput=23.621633369379833 tokens/s | decode_lat_mean=2.6670467285156247 | gpu=['Tesla T4'] | cpu=Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
4bit-awq-gemv-eager | meta-llama/Meta-Llama-3-8B | awq | 4 | bs=1 | seq=256 | new=64 | prefill_mean=0.3750298034667968 s | decode_tput=28.14105919667357 tokens/s | decode_lat_mean=2.2387217041015623 | gpu=['Tesla T4'] | cpu=Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
4bit-awq-exllama-v1-eager | meta-llama/Meta-Llama-3-8B-Instruct | awq | 4 | bs=1 | seq=256 | new=64 | prefill_mean=3.250932910156249 s | decode_tput=28.633491453643803 tokens/s | decode_lat_mean=2.2002206787109375 | gpu=['Tesla T4'] | cpu=Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
4bit-awq-exllama-v2-eager | meta-llama/Llama-3.1-8B-Instruct | awq | 4 | bs=1 | seq=256 | new=64 | prefill_mean=0.22021053161621093 s | decode_tput=28.12034568165892 tokens/s | decode_lat_mean=2.2403707519531246 | gpu=['Tesla T4'] | cpu=Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
4bit-awq-exllama-v1-sdpa | meta-llama/Meta-Llama-3-8B-Instruct | awq | 4 | bs=1 | seq=256 | new=64 | prefill_mean=3.2356754638671874 s | decode_tput=33.247221010685216 tokens/s | decode_lat_mean=1.89489521484375 | gpu=['Tesla T4'] | cpu=Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
4bit-awq-exllama-v1-eager | meta-llama/Meta-Llama-3-8B | awq | 4 | bs=1 | seq=256 | new=64 | prefill_mean=3.2459571533203126 s | decode_tput=28.277173678694854 tokens/s | decode_lat_mean=2.2279454345703122 | gpu=['Tesla T4'] | cpu=Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
4bit-awq-gemv-sdpa | meta-llama/Llama-3.1-8B-Instruct | awq | 4 | bs=1 | seq=256 | new=64 | prefill_mean=0.3676786682128906 s | decode_tput=31.219369801316113 tokens/s | decode_lat_mean=2.0179779541015628 | gpu=['Tesla T4'] | cpu=Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
4bit-awq-exllama-v1-eager | meta-llama/Llama-3.1-8B-Instruct | awq | 4 | bs=1 | seq=256 | new=64 | prefill_mean=3.245940185546875 s | decode_tput=28.471721370364452 tokens/s | decode_lat_mean=2.212721850585937 | gpu=['Tesla T4'] | cpu=Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
4bit-awq-exllama-v2-sdpa | meta-llama/Llama-3.1-8B-Instruct | awq | 4 | bs=1 | seq=256 | new=64 | prefill_mean=0.21214552307128906 s | decode_tput=33.07810714951686 tokens/s | decode_lat_mean=1.9045829833984373 | gpu=['Tesla T4'] | cpu=Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
4bit-awq-exllama-v2-sdpa | meta-llama/Meta-Llama-3-8B-Instruct | awq | 4 | bs=1 | seq=256 | new=64 | prefill_mean=0.21281651611328126 s | decode_tput=33.460910879444036 tokens/s | decode_lat_mean=1.8827939331054686 | gpu=['Tesla T4'] | cpu=Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
4bit-awq-exllama-v2-eager | meta-llama/Meta-Llama-3-8B-Instruct | awq | 4 | bs=1 | seq=256 | new=64 | prefill_mean=0.21970255432128907 s | decode_tput=28.548940110862578 tokens/s | decode_lat_mean=2.2067369140624997 | gpu=['Tesla T4'] | cpu=Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
4bit-awq-gemm-sdpa | meta-llama/Llama-3.1-8B-Instruct | awq | 4 | bs=1 | seq=256 | new=64 | prefill_mean=0.41426298217773433 s | decode_tput=23.833781540589897 tokens/s | decode_lat_mean=2.64330693359375 | gpu=['Tesla T4'] | cpu=Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
4bit-awq-gemv-sdpa | meta-llama/Meta-Llama-3-8B-Instruct | awq | 4 | bs=1 | seq=256 | new=64 | prefill_mean=0.36864620361328126 s | decode_tput=31.6722433403514 tokens/s | decode_lat_mean=1.9891233886718749 | gpu=['Tesla T4'] | cpu=Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
4bit-awq-gemm-sdpa | meta-llama/Meta-Llama-3-8B | awq | 4 | bs=1 | seq=256 | new=64 | prefill_mean=0.4163207153320313 s | decode_tput=23.93802318448678 tokens/s | decode_lat_mean=2.6317962646484374 | gpu=['Tesla T4'] | cpu=Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
```

---

## Audit notes (9.12 audit, 2026-10-09)

The records above stay as read; the audit's re-reads and recounts are `search/A-audit.md`.

- **S3-02** — on Ubuntu 24.04, the distribution the dataset depicts, `updatedb` is not in the stock desktop image, and the installable plocate 1.1.19 declares only `IOSchedulingClass=idle`; `Nice=19` enters with plocate 1.1.23 (A2-05; D64).
- **S3-05** — the 0.88 s is the 12 GB RTX 3060 (accelerator 43), a mean over the runs submitted for it (A2-21; D107).
- **S3-11** — Table 4 is a distribution of each avatar's average session, over one realm's Horde faction (A2-13; D70).
- **S3-18** — the figures are 72-hour medians, one per provider; they move between reads (A2-21; D107).
- **S3-19** — the 14-of-35 count is on the dataset's bound names; ananicy-cpp keys a process by its `argv[0]` basename (A3-07; D105); recounted on that key, 19 of 35, every name in 7 of 50 files (A3-09; D109).
- **S3-20** — the count re-run, output byte-identical; the 16 that raise are named (A2-24; D64).
- **S3-21** — restricted to the repeat lists the owning slices pooled, the madvise check left out: 67 program phases over 1 223 phase files; group medians 12.9 to 12 497.2 a second, the median phase 422.0; 53 at 100 or more, 13 at 1 000 or more, 2 at 10 000 or more. 594 of the 1 806 full-mode files kept above lie outside those lists. The busy shares are over whole phase files, harness time included; restricted, `clamscan` 0.9334–0.9435 over 10 repeats and `train` 0.8475–0.8575 over 8 (A1-07, A1-08; D58).
- **S3-22** — every request's answer counted per model, schema, prompt and machine (A1-05; D60).
- **S3-23** — the session-time fit's median, about 9.6 minutes (arithmetic); the trace table spans 14 months against the abstract's "13-month" (A2-12; D70).
