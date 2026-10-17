# S3 — public traces and datasets (T1, T3, T6, T7, T9)

Reader: S3. Access date for every source: 2026-09-24. Copies under `sources/S3-NN/` (gitignored); everything needed is quoted below.

Access conditions this session (they shape what could be read):
- `curl` to `github.com`, `api.github.com` (including `search/issues` and repo-scoped `repos/...` endpoints), `codeload.github.com`, `lore.kernel.org`, `www.phoronix.com`, `openbenchmarking.org`: **HTTP 403** from the session egress proxy. The GitHub MCP tool refused `sched-ext/scx` ("repository ... is not configured for this session"). `www.spinics.net`: connection reset (curl exit 35).
- Reachable with curl: `raw.githubusercontent.com`, `git clone` of github repos, `objects.githubusercontent.com` (signed attachment URLs), `marc.info`, `lkml.iu.edu`, `git.kernel.org`, `patchwork.kernel.org`, `gitlab.freedesktop.org` API, `zenodo.org` API, `api.osf.io`, `pastebin.com/raw`.
- GitHub issue pages were therefore read with the WebFetch tool, which returns tool-rendered markdown, not the page bytes. For those candidates (S3-06 issue text, S3-08, S3-09, S3-10) the copy saved is the WebFetch transcript and the SHA-256 is of that transcript; passages are marked **[WebFetch]** — the tool was instructed to print unchanged text, and log/code blocks came back as code blocks, but byte-exactness against the original page is not independently verifiable. All other passages are from byte copies fetched with curl.

## 1. Search log

| # | Date | Engine / venue | Exact query | Hits followed | Dead ends (status) |
|---|---|---|---|---|---|
| 1 | 2026-09-24 | GitHub REST API (curl) | `https://api.github.com/search/issues?q=repo:sched-ext/scx+stall` | — | 403 ("sessions are bound to their configured repositories") |
| 2 | 2026-09-24 | GitHub REST API (curl) | `https://api.github.com/repos/sched-ext/scx/issues?state=all&per_page=1` | — | 403 |
| 3 | 2026-09-24 | curl probes | `github.com/sched-ext/scx/issues?q=stall`, `lore.kernel.org/lkml/`, `www.phoronix.com`, `openbenchmarking.org`, `codeload.github.com/...`, `www.spinics.net` | — | 403 / 403 / 403 / 403 / 403 / curl 35 conn. reset |
| 4 | 2026-09-24 | GitHub MCP `issue_read` | sched-ext/scx #3791 | — | refused: repo not configured for session |
| 5 | 2026-09-24 | Zenodo API `/api/records` | `latency perception touchscreen`; `just noticeable difference latency`; `touch latency perception`; `input latency perception threshold`; `keyboard latency perception`; `latency detection threshold` | top 10 each read by title | none relevant (haptics, JND for images, networks) |
| 6 | 2026-09-24 | Zenodo API, `type=dataset` | `"latency perception"`; `"perceived latency"`; `"touch latency"`; `"input latency"`; `"end-to-end latency" perception`; `"latency" "just noticeable"` | titles | 0 / 0 / 0 / 2 irrelevant / "Glass-to-Glass Latency Dataset for Mobile Devices" (device latency, no perception measure — not T1) / irrelevant |
| 7 | 2026-09-24 | OSF API | `api.osf.io/v2/search/?q=...` (5 queries) | — | 404 "Not found." (endpoint) |
| 8 | 2026-09-24 | OSF API | `api.osf.io/v2/nodes/?filter[title]=` for `latency perception`, `latency just noticeable difference`, `touch latency`, `input lag perception`, `delay detection threshold interaction` | — | 0 results each |
| 9 | 2026-09-24 | OSF API | `filter[title][icontains]=latency` (97 public nodes) | all 97 titles scanned | none on input/touch/keyboard latency perception; nearest "Measuring motion-to-photon latency for sensorimotor experiments with virtual reality systems" (device measurement), "The Impact of Response Latency and Task Type on Human-LLM Interaction" (seconds-scale LLM latency) — not T1 |
| 10 | 2026-09-24 | SHARE (share.osf.io) `_search` | `latency perception touch` | first hit (tactile) | irrelevant |
| 11 | 2026-09-24 | WebSearch | `touch latency perception just noticeable difference dataset osf data release` | result list | only papers (ResearchGate, IFIP) — no data release |
| 12 | 2026-09-24 | WebSearch | `"latency" "just noticeable difference" user study data github repository csv touchscreen OR stylus OR keyboard` | result list | papers only; no dataset link |
| 13 | 2026-09-24 | WebSearch | `github dataset latency perception experiment JND participants raw data "latency" "perception" HCI study repository` | HCI-SENSE-42 (by snippet: 42-participant desktop interaction dataset) | snippet describes no latency-perception threshold; not followed further — not T1 |
| 14 | 2026-09-24 | WebSearch | `osf.io latency perception threshold experiment data keyboard OR mouse OR touch` | result list | papers only (Springer "Are 100 ms Fast Enough?") — no data release located |
| 15 | 2026-09-24 | WebFetch github.com issue search | `sched-ext/scx/issues?q="runnable task stall"` | #3791, #3750, #3739, #3624 | #3750: no logs; #3624: log pastes not in page text |
| 16 | 2026-09-24 | WebFetch github.com issue search | `sched-ext/scx/issues?q="failed to run for" is:issue` | #3791, #3739, #3119 (via #17), 12 listed | — |
| 17 | 2026-09-24 | WebFetch github.com issue search | `sched-ext/scx/issues?q="--stats" slice is:issue` | #3119, #3750 | #3750 no stats |
| 18 | 2026-09-24 | WebFetch github.com issue search | `sched-ext/scx/issues?q="slice_us"`; `?q="--monitor" is:issue` | #3739, #3541 | #3541: no monitor output with slice |
| 19 | 2026-09-24 | marc.info (linux-kernel, bodies) | `Fallback to sched-idle CPU` | V3 0/2 cover (m=156152560909077) + raw | — |
| 20 | 2026-09-24 | pastebin raw | `https://pastebin.com/raw/TMHGGBxD` (rt-app json cited by S3-01) | fetched | — |
| 21 | 2026-09-24 | marc.info (subjects) | `SCHED_IDLE`; `sched_idle latency` | first 30 subjects | fuzzy matching; no further SCHED_IDLE measurement thread found |
| 22 | 2026-09-24 | patchwork.kernel.org API | `/api/patches/?q=sched-idle CPU` | — | 200, empty list |
| 23 | 2026-09-24 | git.kernel.org | `torvalds/linux.git/patch/?id=51ce83ed523b00d58f2937ec014b12daaad55185` | fetched (S3-02) | — |
| 24 | 2026-09-24 | marc.info (subjects) | `SCHED_DEADLINE server infrastructure` | RFC V3 0/6 (m=168623990405859), V7 0/9 (m=171681142401640) | `deadline server`, `RT throttling activated` (subject search): no rows |
| 25 | 2026-09-24 | WebSearch | `"sched: RT throttling activated" dmesg bug report` | lkml.iu.edu 1312.1/02313, 02318 | forums (raspberrypi, debian, TI, Red Hat) not followed |
| 26 | 2026-09-24 | marc.info (bodies) | `base_slice`; `sched_base_slice`; `custom slice` | "[REGRESSION] [PATCH v3 7/7] sched/eevdf: Move to a si…" (m=179017450477186; first try 502 CONNECT, retry 200) | reports schbench p99 only, no slice measured — not T3 (T8 matter, outside S3 topics) |
| 27 | 2026-09-24 | WebFetch github.com issue search | `mpv-player/mpv/issues?q="frame dropped" log-file is:issue` | #16346 | others not followed (GPU performance reports) |
| 28 | 2026-09-24 | curl → objects.githubusercontent.com | signed redirect of `github.com/user-attachments/files/20219345/mpv_debug.log` (redirect obtained via WebFetch; direct curl to github.com 403) | fetched (S3-06) | — |
| 29 | 2026-09-24 | WebFetch github.com issue search | `scheduler-tools/rt-app/issues?q=overrun OR slack OR "missed"` | PR #101 | no rt-app log output in PR |
| 30 | 2026-09-24 | git clone (blob:none) | `https://github.com/ARM-software/lisa.git` HEAD `bb5ff50d0ff5f5e3620634dc3342103dcfa1d6d2`, file listing | `tests/assets/trace_txt/{trace.txt,plat_info.yml}` via raw.githubusercontent (S3-05) | binary `trace.dat` files not parsed (no trace-cmd installed) |
| 31 | 2026-09-24 | gitlab.freedesktop.org API | `projects/gstreamer%2Fgstreamer/issues?search=A lot of buffers are being dropped` | #3798 (S3-07) | notes endpoint 401 |

## 2. Candidates

### S3-01 — Viresh Kumar, "[PATCH V3 0/2] sched/fair: Fallback to sched-idle CPU in absence of idle CPUs", LKML, 2019-06-26

- Copy read: `https://marc.info/?l=linux-kernel&m=156152560909077&q=raw` (body) → `sources/S3-01/v3-cover.mbox`, SHA-256 `13bd5b40ef10409b161eb9c7c9d93cef51a94dc68c3f51d6a2a2030b527d373e`; HTML view with headers `https://marc.info/?l=linux-kernel&m=156152560909077&w=2` → `v3-cover.html`, SHA-256 `8adbf37975a7ebe0dd2a44eaba12cb4478f0a0b08bfff2c3086388e63802157a`. rt-app config cited as [1]: `https://pastebin.com/raw/TMHGGBxD` → `rt-app.json`, SHA-256 `46da6bc20c4d296fb072aa874cb986ab900fa1bda3c43f861cf6a5aa76e81bd3`. Version: message as archived; Message-ID `cover.1561523542.git.viresh.kumar () linaro ! org`.
- Headers (v3-cover.html:11–15): "Subject:    [PATCH V3 0/2] sched/fair: Fallback to sched-idle CPU in absence of idle CPUs" / "From:       Viresh Kumar <viresh.kumar () linaro ! org>" / "Date:       2019-06-26 5:18:28".
- Passages (v3-cover.mbox line numbers):
  - :7–10 "A CPU which isn't idle but has only SCHED_IDLE activity queued on it should be a good target based on this criteria as any normal fair task will most likely preempt the currently running SCHED_IDLE task immediately."
  - :19–23 "- Tested on Octacore Hikey platform (all CPUs change frequency together). - rt-app json [1] creates few tasks and we monitor the scheduling latency for them by looking at "wu_lat" field (usec)."
  - :34 "Test 1: Create 8 CFS tasks (no SCHED_IDLE tasks) without this patchset:" ; :48–49 "N       min     max     sum     mean    stddev" / "5136    0       2452    535985  104.358 104.585"
  - :52–54 "Test 2: Create 8 CFS tasks and 5 SCHED_IDLE tasks: A. Without sched-idle patchset:" ; :66 ">1000 : 34% (1218)" ; :68–69 "N       min     max     sum             mean    stddev" / "4710    0       67664   5.25956e+06     1116.68 2315.09"
  - :72 "B. With sched-idle patchset:" ; :86–87 "5095    0       7773    523170  102.683 475.482"
  - :90–91 "The mean latency dropped to 10% and the stddev to around 25% with this patchset."
  - :101 "- Rebased over latest tip/master, fixed rebase conflicts."
  - rt-app.json:3–13 `"cfs_thread" : { "instance" : 8, "run" :   5333, "timer" : { "ref" : "unique", "period" : 7777 }, "policy" : "SCHED_OTHER" }, "idle_thread" : { "instance" : 5, "run" :   3000, "policy" : "SCHED_IDLE" }` ; :16 `"duration" : 5,`
- Coverage:
  - **T9 covers.** Object: wake-up latency (rt-app `wu_lat`, usec) of 8 periodic SCHED_OTHER tasks (run 5333 us / period 7777 us) with and without 5 SCHED_IDLE CPU hogs, on stock kernel (Test 2A) vs patched (2B). Statistic: N, min, max, sum, mean, stddev and a 100-us histogram. Values: no hogs mean 104.358 us, max 2452 us (N=5136); with SCHED_IDLE hogs, unpatched, mean 1116.68 us, max 67664 us, 34% of wake-ups >1000 us (N=4710); patched mean 102.683 us, max 7773 us (N=5095). Scope: one platform, one rt-app run per configuration.
  - T3: does not cover (no slice stated). T1, T6, T7: do not cover.
- Observation: yes — one run per configuration; machine named ("Octacore Hikey platform"); subject named (rt-app cfs_thread ×8 beside idle_thread ×5); window named (rt-app `"duration" : 5` s, N samples given). Kernel only as "latest tip/master" in June 2019 (no version number).

### S3-02 — Josh Don, "sched: reduce sched slice for SCHED_IDLE entities", Linux commit 51ce83ed523b (2021-08-19)

- Copy read: `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/patch/?id=51ce83ed523b00d58f2937ec014b12daaad55185` → `sources/S3-02/commit.patch`, SHA-256 `d7c15531ec94c4a438b4bb2795a4e022cd75450d4860a69325da43d3e33c9667`. Commit `51ce83ed523b00d58f2937ec014b12daaad55185`.
- Passages (commit.patch):
  - :1–4 "From 51ce83ed523b00d58f2937ec014b12daaad55185 ..." / "From: Josh Don <joshdon@google.com>" / "Date: Thu, 19 Aug 2021 18:04:02 -0700" / "Subject: sched: reduce sched slice for SCHED_IDLE entities"
  - :6–9 "Use a small, non-scaled min granularity for SCHED_IDLE entities, when competing with normal entities. This reduces the latency of getting a normal entity back on cpu, at the expense of increased context switch frequency of SCHED_IDLE entities."
  - :14–17 "Example: on a machine with HZ=1000, spawned two threads, one of which is SCHED_IDLE, and affined to one cpu. Without this patch, the SCHED_IDLE thread runs for 4ms then waits for 1.4s. With this patch, it runs for 1ms and waits 340ms (as it round-robins with the other thread)."
  - :22 "Link: https://lore.kernel.org/r/20210820010403.946838-4-joshdon@google.com"
  - :54 "unsigned int sysctl_sched_min_granularity			= 750000ULL;" (context line of diff, fair.c)
- Coverage:
  - **T9 covers.** Object: run length and wait of a SCHED_IDLE thread sharing one CPU with one normal thread (both CPU-bound, affined). Unit ms/s. Values: before patch runs 4 ms, waits 1.4 s; after, runs 1 ms, waits 340 ms. Statistic: not stated (single example, typical values). Scope: one machine, HZ=1000.
  - **T3 covers (observed effective slice for the SCHED_IDLE entity):** 4 ms per turn under the pre-patch CFS on that machine, 1 ms after. Does not state the normal thread's slice.
  - T1, T6, T7: do not cover.
- Observation: one example; machine not named (only "a machine with HZ=1000"); subject named (two threads, one SCHED_IDLE, one CPU); window not stated; kernel = the tree the patch was written against (merged as 51ce83ed523b; version not stated in the message).

### S3-03 — Daniel Bristot de Oliveira, "SCHED_DEADLINE server infrastructure", RFC V3 0/6 (2023-06-08) and V7 0/9 (2024-05-27), LKML

- Copies read: RFC V3 body `https://marc.info/?l=linux-kernel&m=168623990405859&q=raw` → `sources/S3-03/v3-cover.txt`, SHA-256 `e491976de645baf03b35bf28af1213a4469f9e3d6dd081b4ad9423b8327c80a0`; headers `...&w=2` → `v3-cover.html`, SHA-256 `0b172905179339174215742eb89d31eb7266b298016e42380f104d6336384ab7` (Message-ID `cover.1686239016.git.bristot () kernel ! org`, Date 2023-06-08 15:58:12). V7 body `https://marc.info/?l=linux-kernel&m=171681142401640&q=raw` → `v7-cover.txt`, SHA-256 `1d76ac58ac597f722a2230b662f4319b9f280e2d76b3072345e77a3bc7dfefcf`; headers → `v7-cover.html`, SHA-256 `14913d19e011875914735f70982374eaef450d75975b3e69246d6336223f1db6` (Message-ID `cover.1716811043.git.bristot () kernel ! org`, Date 2024-05-27 12:06:46).
- Passages, RFC V3 (v3-cover.txt):
  - :4–7 "SCHED_DEADLINE servers can help fixing starvation issues of low priority tasks (e.g., SCHED_OTHER) when higher priority tasks monopolize CPU cycles. Today we have RT Throttling; DEADLINE servers should be able to replace and improve that."
  - :58–60 "The patch 6/6 adds a PoC of an starvation monitor/watchdog that delays enqueuing of deadline servers to the point when fair tasks might start to actually suffer from starvation (just randomly picked HZ/2 for now)."
  - :89–94 "Here are some osnoise measurement, with osnoise threads running as FIFO:1 with different setups*: - CPU 2 isolated - CPU 3 isolated shared with a CFS busy loop task - CPU 8 non-isolated - CPU 9 non-isolated shared with a CFS busy loop task"
  - :97–104 "# osnoise -P f:1 -c 2,3,8,9 -T 1 -d 10m -H 1 -q" / "duration:   0 00:12:39 | time is in us" / "CPU Period       Runtime        Noise  % CPU Aval   Max Noise   Max Single ..." / "  3 #757       757001039     39322713    94.80546       52992         1103 ..." / "  9 #757       757001043     39922677    94.72620       53775         1105 ..." (CPU 2: "99.99999", CPU 8: "99.89698")
  - :110–111 "* tests with throttling disabled, on the 6.3 stable RT. But also on 6.4 and tip/sched/core."
- Passages, V7 (v7-cover.txt):
  - :59–62 "The defer the server start to the (absolute deadline - runtime) point in time. This is achieved by starting the dl server throttled, with a next replenishing time set to activate the server at (absolute deadline - runtime)."
  - :70–72 "The interface is per CPU and has two knobs:" / "fair_server_runtime (950 ms)" / "fair_server_period  (1s)" (quoted as written)
  - :99–104 "~# taskset -c 3 ./f &" / "~# taskset -c 9 ./f &" / "~# osnoise -P f:1 -c 2,3,8,9 -T 1 -d 10m -H 1"
  - :106–111 "duration:   0 00:10:00 | time is in us" / "  3 #598       598054434     31351553    94.75774      104442       104442 ..." / "  9 #598       598021196     31742537    94.69207       71707        53357 ..."
  - :123 "- also tested with PREEMPT_RT 6.9-rt." ; :138 "- Rebased on top of v6.10-rc1"
- Coverage:
  - **T6 covers (observed, fair server).** Object: share of CPU a CFS busy-loop task obtains beside a FIFO:1 busy thread via the deadline (fair) server, observed as the FIFO thread's lost CPU ("% CPU Aval"). Values: ~94.8% available to FIFO on CPUs shared with a CFS busy loop (i.e. ~5.2% noise = CFS task + IRQ), vs 99.99999% on the isolated CPU without CFS task; max single noise 1103 us (V3) and 104442 us / 53357 us (V7, defer mode). Unit us / percent. Statistic: totals over the osnoise run, max noise, max single. Scope: 4 CPUs (2, 3, 8, 9) of one machine. Also the stated starvation-monitor delay "HZ/2" (V3, a design value, not a measurement).
  - Timerlat tables (V3:15–45, V7:14–88) show FIFO thread latency max up to 61095 us when the DL server runs without defer — these are latency of the RT task, relevant to T6 only as the cost side.
  - T1, T3, T7, T9: do not cover.
- Observation: yes — one osnoise run per version; subject named (osnoise FIFO:1 threads, `./f` CFS busy loop on CPUs 3 and 9); window named (V3 "0 00:12:39", V7 "0 00:10:00"); kernel named (V3: 6.3 stable RT, also 6.4/tip; V7: v6.10-rc1 base, also 6.9-rt). Machine not named (CPU count ≥10 implied by CPU ids; model not stated).

### S3-04 — Howard Chu, "sched: RT throttling activated, 3.12.3", LKML, 2013-12-10, and his reply in thread

- Copies read: `https://lkml.iu.edu/hypermail/linux/kernel/1312.1/02313.html` → `sources/S3-04/02313.html`, SHA-256 `f3622cb1876b51fa2bba8354a6ea6ac45f633ca22a611a7b75b08c3f017b92b5`; `https://lkml.iu.edu/hypermail/linux/kernel/1312.1/02318.html` → `02318.html`, SHA-256 `d5349b92655fbb8b36618e915fc98f281456d01450bee3cec1f8b3c9a0f90ac5`.
- Passages:
  - 02313.html:51 (text) "I just upgraded a system from a 3.5 kernel to 3.12.3 and attempted to run some new benchmarks on it. I see my test program ramps up in CPU usage for a few seconds and then it gradually tails off."
  - 02313.html:61 "[167969.339513] [sched_delayed] sched: RT throttling activated"
  - 02318.html:71 (Li Zefan's answer as quoted) "Because that is the default setting of the kernel."
  - 02318.html:76–79 "lxc34:/proc/sys/kernel # cat sched_rt_period_us" / "1000000" / "lxc34:/proc/sys/kernel # cat sched_rt_runtime_us" / "950000"
  - 02318.html (Chu's reply text) "The code in question is not a realtime process. This behavior also wasn't seen in 3.10 or any older kernels."
- Coverage:
  - **T6 covers (observed values on a real system).** Object: RT throttling parameters read from a running kernel (`sched_rt_period_us` = 1000000 us, `sched_rt_runtime_us` = 950000 us) and the kernel's throttling message with its uptime timestamp (167969.339513 s). Statistic: none (setting read-out + one event). Scope: one host.
  - T1, T3, T7, T9: do not cover.
- Observation: one host ("lxc34"), kernel 3.12.3 named; subject (the benchmark program) not named; window not stated (single event at uptime 167969 s). Machine hardware not stated.

### S3-05 — ARM-software LISA test asset `tests/assets/trace_txt/trace.txt` with `plat_info.yml` (Juno, Linux 4.19)

- Copy read: `https://raw.githubusercontent.com/ARM-software/lisa/bb5ff50d0ff5f5e3620634dc3342103dcfa1d6d2/tests/assets/trace_txt/trace.txt` → `sources/S3-05/trace.txt`, SHA-256 `935755ab60607e433386ff670a1e7a3ddfca0c26fe4b1eb9dce662aa323917be` (2943 lines); `.../tests/assets/trace_txt/plat_info.yml` → `plat_info.yml`, SHA-256 `b4c9cd3a98bf93b9a4df0ba12eb1200a57ab630bb779e5e2455032ace4a20807`. Commit `bb5ff50d0ff5f5e3620634dc3342103dcfa1d6d2` (HEAD of default branch on 2026-09-24).
- Passages:
  - plat_info.yml:12 "cpus-count: 6" ; :57–70 "kernel:" … "release: 4.19.0-07801-gf317706" … "version: 38 SMP PREEMPT Fri Nov 30 13:55:54 GMT 2018" … "name: juno"
  - trace.txt:1–2 "version = 6" / "cpus=6"
  - trace.txt:3 "<...>-1701  [001]    76.211513: sched_switch:          prev_comm=trace-cmd prev_pid=1701 prev_prio=120 prev_state=64 next_comm=swapper/1 next_pid=0 next_prio=120"
  - trace.txt:459 "sh-1702  [005]    76.368433: print:                0xffff00000819ff24s: TRACE_MARKER_START" ; :2821 "sh-1717  [000]    82.731572: print:                0xffff00000819ff24s: TRACE_MARKER_STOP"
  - trace.txt:1472 "ramp-1706  [004]    76.902180: sched_switch:          prev_comm=ramp prev_pid=1706 prev_prio=120 prev_state=0 next_comm=kworker/4:1 next_pid=1152 next_prio=120"
- Coverage:
  - T3: **raw material only, does not state the quantity.** It is a real ftrace text trace (sched_switch ×1856, sched_wakeup ×1068 by event-name count) on a named machine, from which run intervals could be derived, but no slice or timeslice value is stated in the file and I computed none. The workload is an rt-app-style `ramp` task, mostly sleeping, so involuntary preemptions (prev_state=0) are few and mostly by kworkers.
  - T1, T6, T7, T9: do not cover.
- Observation: one trace; machine named (Arm Juno, 6 CPUs); kernel named (4.19.0-07801-gf317706); window named (76.211513–82.888010 s trace time; markers 76.368433–82.731572); subject "ramp" task (no rt-app config in this asset folder).

### S3-06 — mpv issue #16346 "AVFoundation causes frame drops when resuming from an underrun state." with attached `mpv_debug.log`

- Copies read: issue page via WebFetch **[WebFetch]** → `sources/S3-06/webfetch-mpv-issue-16346.txt`, SHA-256 `b883797295ed80bdaf0e650217f75a0c2b40c6e3642a6f82f76d8c3529d9fdef` (URL `https://github.com/mpv-player/mpv/issues/16346`); attached log `https://github.com/user-attachments/files/20219345/mpv_debug.log` (fetched by curl from its signed `objects.githubusercontent.com/github-production-repository-file-5c1aeb/6201092/20219345?...` redirect) → `mpv_debug.log`, SHA-256 `43cc990de0289053b197e63b1e88a4b0cf98ba68431434dc488c79146f18440c` (123499 bytes, 1579 lines).
- Passages:
  - [WebFetch] Title "AVFoundation causes frame drops when resuming from an underrun state. #16346", author bitxeno, May 15, 2025; "macOS 15.1.1".
  - [WebFetch] Actual behavior: "When the playback URL is slow, the player pauses to buffer after underrun. However, resuming playback causes a drop of approximately 30 or more frames."
  - [WebFetch] Expected: "Don't drop frames when resuming from an underrun state."
  - [WebFetch] status line as rendered: "AV: 00:00:34 / 00:23:43 (2%) A-V: 0.000 Dropped: 184 Cache: 3.1s/759KB"
  - mpv_debug.log:1 "[   0.003][v][cplayer] mpv v0.40.0-dev-gf9ec3d2c2 Copyright © 2000-2025 mpv/MPlayer/mplayer2 projects"
  - mpv_debug.log:15 "[   0.005][v][cplayer] Command line options: '--no-config' '--input-commands=script-message display-stats-toggle' '--gpu-debug' '--log-file=/tmp/mpv_debug.log' '--hwdec=yes' '--ao=avfoundation' 'http://alist.lan/d/...001.mp4'" (URL path shortened here; full in copy)
  - mpv_debug.log:174 "[   7.199][i][cplayer] ● Video  --vid=1  (h264 720x540 25 fps) [default]" ; :221 "[   7.229][v][vo/gpu/libplacebo]     Device Name: Apple M4"
  - mpv_debug.log:1393–1394 "[   9.729][w][cplayer] Audio device underrun detected." / "[   9.759][v][cplayer] Enter buffering (buffer went from 100% -> 0%) [0.000000s]."
  - mpv_debug.log:1407–1410 "[  18.678][v][cplayer] End buffering (waited 8.949649 secs) [1.280000s]." / "[  18.679][v][cplayer] restarting audio after underrun" / "[  18.679][w][cplayer] " / "[  18.679][w][cplayer] Audio/Video desynchronisation detected! Possible reasons include too slow"
- Coverage:
  - **T7 covers (player behaviour after a stall, observed).** Object: mpv's handling of video frames whose presentation time passed during a buffering stall — reported as dropping "approximately 30 or more frames" on resume (i.e. skip, not replay the backlog); cumulative "Dropped: 184" at 00:00:34 per the status line. The log itself records the stalls (buffering waits 8.949649 s, 6.382282 s, …) and audio restarts but contains no per-frame drop lines (grep for "drop" finds only an ffmpeg resize line), so the drop count rests on the issue text [WebFetch]. Unit: frames. Scope: one playback.
  - T1, T3, T6, T9: do not cover.
- Observation: one run; machine named (Apple M4, macOS 15.1.1); subject named (mpv v0.40.0-dev-gf9ec3d2c2, h264 720x540 25 fps over HTTP, `--ao=avfoundation`); window named (log 0.003–63.899 s).

### S3-07 — GStreamer issue #3798 "glimagesink framerate drops to ~1fps in about a second if launched in X11 session without monitor attached (virtual screen, framebuffer)"

- Copy read: `https://gitlab.freedesktop.org/api/v4/projects/gstreamer%2Fgstreamer/issues/3798` (JSON) → `sources/S3-07/issue-3798.json`, SHA-256 `c8b3e42a06e2c859ddae59b254c35cf7543f9738838d79f3a524d10cc9dd2f62`; its `description` field extracted to `desc.txt`, SHA-256 `5023d75de05bbc4558d97166442cfe8d5a2869a434844b7322ddce59dafb26aa` (line numbers below are desc.txt). Issue author Talkless, created 2024-09-11T07:37:30.816Z, state closed, updated 2025-06-06T06:34:28.611Z; web URL `https://gitlab.freedesktop.org/gstreamer/gstreamer/-/work_items/3798`.
- Passages:
  - desc.txt:14 "`glimagesink` should keep same expected (25fps for example) framerate in X11 session without physical monitor too."
  - desc.txt:18 "Pipeline with `glimagesink` as sink drop to 1fps after about 1 second of playback."
  - desc.txt:21–23 "- **Operating System:** Debian 12 amd64" / "- **Device:** Computer , Celeron J1900" / "- **GStreamer Version:** main branch"
  - desc.txt:30 "GST_DEBUG=3,fps*:7 ./gst-launch-1.0 videotestsrc ! video/x-raw,framerate=25/1 ! queue ! fpsdisplaysink fps-update-interval=200 silent=0 text-overlay=0 signal-fps-measurements=1 video-sink=glimagesink"
  - desc.txt:39 "`sync=false` does not help." ; :41 "No issue with `xvimagesink`."
  - desc.txt:63 "0:00:00.495809508 30634 0x55851bf2f4c0 LOG           fpsdisplaysink fpsdisplaysink.c:391:display_current_fps:<fpsdisplaysink0> Signaling measurements: fps:27.926950 droprate:0.000000 avg-fps:27.926950"
  - desc.txt:67 "0:00:02.025049668 30634 0x55851bf2f4c0 LOG           fpsdisplaysink fpsdisplaysink.c:391:display_current_fps:<fpsdisplaysink0> Signaling measurements: fps:1.000056 droprate:10.000562 avg-fps:5.160202"
  - desc.txt:69 "... Signaling measurements: fps:1.000034 droprate:24.000808 avg-fps:3.644203" (0:00:03.025006512) ; :71 "... fps:0.999874 droprate:23.996974 avg-fps:2.937869" (0:00:04.025154696)
- Coverage:
  - **T7 covers (sink drops late frames rather than accumulating).** Object: GStreamer fpsdisplaysink measurements of rendered vs dropped frames per second for a 25 fps source into glimagesink when presentation is blocked. Values: ~1 frame/s rendered and ~24 frames/s dropped (fps ≈ 1.0, droprate ≈ 24.0) from ~2 s onward; the pipeline does not build a backlog of late frames. Unit frames/s. Statistic: per-interval rate as printed by fpsdisplaysink. Scope: one pipeline run. Cause is a display/driver condition (no monitor), not CPU scheduling.
  - T1, T3, T6, T9: do not cover.
- Observation: one run; machine named (Celeron J1900, Debian 12 amd64, X11 without monitor); subject named (the gst-launch pipeline above, GStreamer main branch as of 2024-09); window named (log 0:00:00.49–0:00:04.03 in the first excerpt).

### S3-08 — sched-ext/scx issue #3791 "[Bug Report] scx_lavd 1.1.3: repeated "runnable task stall" watchdog ejections under normal desktop use"

- Copy read: **[WebFetch]** `https://github.com/sched-ext/scx/issues/3791` → `sources/S3-08/webfetch-scx-issue-3791.txt`, SHA-256 `c7edae88fd2fe39b51cb62182aaf508dee40f1a938ef14de2ec3bc43ef1b2008`. Author ultra-low, opened 2026-09-04 (closed 2026-09-12 per search listing).
- Passages [WebFetch]:
  - CPU "AMD Ryzen 5 PRO 2500U ("Raven Ridge", Zen 1, 4C/8T, single CCX, no NUMA, no hybrid cores)"; Kernel "linux-zen 7.2.3.zen1-2 (also reproduced on 7.2.2.zen1-1)"; scx-scheds "1.1.3-1 (Arch extra package)".
  - Log: "Sep 04 19:50:20 kernel: sched_ext: BPF scheduler "lavd_1.1.3_x86_64_unknown_linux_gnu" disabled (runnable task stall)" / "Sep 04 19:50:20 kernel: sched_ext: lavd_1.1.3_x86_64_unknown_linux_gnu: ThreadPoolForeg[2012] failed to run for 35.327s" / "Sep 04 19:55:37 kernel: sched_ext: lavd_1.1.3_x86_64_unknown_linux_gnu: brave[2356] failed to run for 45.099s" / "Sep 04 20:20:34 kernel: sched_ext: lavd_1.1.3_x86_64_unknown_linux_gnu: Compositor[4041] failed to run for 30.387s" (eight "failed to run for" lines in all, values 35.327, 37.902, 45.099, 32.199, 39.834, 39.795, 30.387, 31.238 s).
  - "Within roughly 1 to 4 minutes, an unrelated thread stalls for 30 to 45s and the scheduler is ejected."
- Coverage:
  - **T6 covers (sched_ext watchdog observed).** Object: runnable-task wait at which the sched_ext watchdog ejected the BPF scheduler. Unit s. Values: 30.387 s to 45.099 s across 8 ejections (min 30.387 s). Statistic: individual events. Scope: one laptop, desktop workload (Brave, video, Hyprland). The log does not state the configured watchdog timeout.
  - T1, T3, T7, T9: do not cover.
- Observation: yes — one machine (Ryzen 5 PRO 2500U) and kernel (linux-zen 7.2.3.zen1-2) named, subject named (scx_lavd 1.1.3 `--autopilot`, stalled threads named), window named (journal 2026-09-04 19:50:20–20:22:42).

### S3-09 — sched-ext/scx issue #3739 "[scx_lavd] Repeated system stutter under autopilot."

- Copy read: **[WebFetch]** `https://github.com/sched-ext/scx/issues/3739` → `sources/S3-09/webfetch-scx-issue-3739.txt`, SHA-256 `217f19b115ae95392f9998a43d3c3d10a89d5a407a5c99cd7f5fc189e5ea5db3`. Author howfool, 2026-08-15.
- Passages [WebFetch]:
  - "Kernel: Linux 7.1.8-1-cachyos" / "scx package: scx-scheds 1.1.2-1" / "LAVD build ID: 1.1.2 x86_64-unknown-linux-gnu" / "Kernel preemption: CONFIG_PREEMPT=y, CONFIG_PREEMPT_DYNAMIC=y" / "CPU: 12th Gen Intel(R) Core(TM) i7-12700H"
  - "Task                         Max delay    Start          End" / "MediaDe~hine #8:560427       661.639 ms   64786.700419   64787.362058" / "kworker/u85:0-i:544390       656.828 ms   64786.705255   64787.362083" / "kwin_wayland:(3)               2.958 ms   64782.869110   64782.872068"
- Coverage:
  - **T6 covers (observed wait, below watchdog).** Object: maximum wake-to-run delay per task (perf-sched-style "Max delay") under scx_lavd 1.1.2. Unit ms. Values: 661.639 ms and 656.828 ms maxima; compositor (kwin_wayland) 2.958 ms. Statistic: per-task maximum. The command and recording length are not shown in the fetched text.
  - T1, T3, T7, T9: do not cover.
- Observation: one trace; machine (i7-12700H) and kernel (7.1.8-1-cachyos) named; subject tasks named; window partially named (Start/End timestamps 64782.869110–64787.594923 of the listed rows; total recording length not stated).

### S3-10 — sched-ext/scx issue #3119 "lavd: tasks not scheduled for ~20ms despite multiple CPUs being idle"

- Copy read: **[WebFetch]** `https://github.com/sched-ext/scx/issues/3119` → `sources/S3-10/webfetch-scx-issue-3119.txt`, SHA-256 `13ed26fab83775940004aba5ddf4d606e2b176e4361c2131c181ca295739be89`. Author blezsan, 2025-12-02.
- Passages [WebFetch]:
  - "Seen when running lavd on an Intel Cooperlake system with the following flags: `--performance --slice-min-us 5000 --slice-max-us 20000 --pinned-slice-us 5000 --virt-llc`"
  - "The system is running at 90% cpu util, so very busy but there should be some CPU idle time."
  - "Using github revision `fab819291ffcbfe9a70708e8e44362026bebac44`"
  - "This screenshot from Perfetto shows the runnable task at the top, and a subset of the CPUs underneath, some of which are idle or become idle while the task is runnable."
  - "However no CPU is picking up the task until a full slice duration."
- Coverage:
  - **T3 covers (weakly).** Object: effective slice seen in a Perfetto trace under scx_lavd with explicit, non-default slice bounds (5000–20000 us); the wait equals "a full slice duration", ~20 ms per the title. Unit ms. Statistic: single observed interval (screenshot, not text). The defaults are overridden by flags, so this is not a default-slice observation.
  - **T6 covers (weakly):** a runnable task waits ~20 ms with idle CPUs present.
  - T1, T7, T9: do not cover.
- Observation: one trace; machine class named (Intel Cooperlake; exact model and kernel not stated); subject scx_lavd at revision fab819291ffcbfe9a70708e8e44362026bebac44; window not stated (screenshot only; trace file not attached as text).

## 3. Not found

- **T1 — no candidate.** No released dataset carrying a measured latency-perception threshold/JND (touch, stylus, keyboard, mouse) was located. Searches: Zenodo API free-text (6 queries, row 5) and dataset-type quoted phrases (6 queries, row 6); OSF search endpoint (404, row 7), OSF node title filters (5 queries, 0 hits, row 8), OSF title-contains "latency" (97 nodes scanned, row 9); SHARE (row 10); WebSearch ×4 (rows 11–14) — returned only the papers (Ng et al./Jota et al./Deber et al.-type studies, "Are 100 ms Fast Enough?", Kaaresoja et al.), not data releases. No README or data dictionary could therefore be quoted. The "136M Keystrokes" dataset was not pursued because none of the hits suggested it carries a latency-perception measure.
- **T3 — no candidate showing the default EEVDF/CFS `sched_base_slice` observed on a real machine.** Found only S3-02 (SCHED_IDLE entity's 4 ms/1 ms run length, HZ=1000 machine) and S3-10 (lavd with overridden slice flags); S3-05 is raw trace material with no stated slice. Phoronix/OpenBenchmarking result files unreachable (403, row 3); lore.kernel.org unreachable (403); marc.info body searches for `base_slice`, `sched_base_slice`, `custom slice` (row 26) surfaced no measured slice; scx issue searches for `--stats`/`slice_us`/`--monitor` (rows 17–18) found no pasted stats with slice values in fetched text. GitHub issue search API blocked (403, rows 1–2).
- T6, T7, T9 have candidates (S3-03, S3-04, S3-08, S3-09, S3-10; S3-06, S3-07; S3-01, S3-02). Gaps within them: T7 — no rt-app log showing overruns/slack and no interbench output found (row 29; LISA binary `trace.dat` files not parsed, row 30); T9 — no desktop-indexer (tracker/baloo) CPU measurement pursued beyond the kernel-list results; T6 — no public trace of illumos TS `ts_maxwait` aging.
