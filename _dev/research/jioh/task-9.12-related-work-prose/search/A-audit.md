# 9.12 audit — reads and recounts (2026-10-09)

The audit of 9.12's decisions before the slice is ticked: every decision re-read against primary copies, the runner campaign re-pooled from its release, the dataset's numbers recounted from the raw records, vol-02's verdicts re-checked, the record checked for coverage and consistency. Decisions D55 onward cite these ids. Copies fetched in the audit are under `sources/<id>/audit-2026-10-09/` (gitignored); scripts and outputs not kept there are named with their hashes.

## A1 — measurement: the campaign re-pooled, S3-21 restricted, the dataset's numbers recounted

Paths: `SCR` = `sources/audit-2026-10-09/` (the audit's scripts and outputs, copied from its session scratchpad; gitignored; the release archives and their extraction left out, the release being the record); `S` = `_dev/research/jioh/task-9.12-related-work-prose/`. Each output's SHA-256 is stated.

### A1-01 — `meas-ci:costs:2026-10-08` re-downloaded from its release
- `gh release download meas-ci-costs-2026-10-08 -R logis11/LLM_driven_shceduling -D SCR/C1-campaign/release` (2026-10-09): 34 archives; their SHA-256 (`release.sha256`) equal GitHub's asset digests (`release.digest`) line for line. Extracted to `SCR/C1-campaign/x`; each of the 30 pooled job folders (19 `kernel`, 11 `llm`) `diff -rq`-identical to `~/.cache/meas-loop/costs/<run>/<job>`.

### A1-02 — the re-pool
- `python3 -I dataset/tools/meas/costs/pool.py SCR/C1-campaign/x --cpu-model "EPYC 7763" --out SCR/C1-campaign/pool-out` → `pool-out.txt` (`1e7a3816…`), `pool-out/pooled.json` (`3645bed8…`). `pool-out.txt` lines 1–68 `cmp`-identical to `S/campaign/results/pool.txt` lines 1–68; `pooled.json`'s `jobs` equal in every value; the 66 gated entries the same, in glob order.

### A1-03 — the traced calls classified by the next switch
- Script `SCR/C1-campaign/scripts/classify.py` (`d0e4f06f…`): each traced call in a function-graph trace classified by the next context-switch marker — `to_idle` (the next marker switches to `<idle>`), `from_idle`, `other`, `none`. Run on `trace.pick_task_fair.sleep.txt.gz` of the 19 pooled kernel repeats; output (medians over repeats, verbatim):
  ```
  medians over repeats to_idle min 340 max 351 mean 349.3
  medians over repeats from_idle min 421 max 471 mean 448.8
  medians over repeats other min 501 max 771 mean 582.1
  medians over repeats none min 461 max 651 mean 493.6
  ```

### A1-04 — the 8B's values split by prompt
- Script `SCR/C1-campaign/scripts/subset.py` (`3fc2ff06…`) over `pool-out/pooled.json`, `dataset/tools/meas/stability.py` for the rule. Output (verbatim, selected lines):
  ```
  llama3.1-8b.full.predicted_ms        all11 mean 10746.479 ±3.64% | 09-Oct k=9 mean 10501.808 ±1.67% pass=True | 08-Oct [11751.1, 11943.9]
  llama3.1-8b.full.predicted_n         all11 mean 72.454 ±3.00% | 09-Oct k=9 mean 71.000 ±0.00% pass=True | 08-Oct [79.0, 79.0]
  llama3.1-8b.full.wall_ms             all11 mean 43429.953 ±0.92% | 09-Oct k=9 mean 43183.248 ±0.43% pass=True | 08-Oct [44335.0, 44745.2]
  llama3.1-8b.system.wall_ms           all11 mean 36387.333 ±0.31% | 09-Oct k=9 mean 36368.868 ±0.35% pass=True | 08-Oct [36321.0, 36619.9]
  ```
  Every 8B value passes the rule over the nine.

### A1-05 — every request's answer, per prompt and machine
- Scripts `SCR/C1-campaign/scripts/llm_answers.py` (`555c90ea…`) over the release's `llm` jobs, dry run included; `m1_vs_runner.py` (`c8b3521f…`) over `S/sources/S3-22` and the release. Prompts: 8B `ac36d799f9` ("08 Oct 2026", 1 835 characters), `b765936ca9` ("09 Oct 2026", 1 835); 3B `d095db7d92`. M1 Pro prompt hashes: 8B `b765936ca9`, 3B `d095db7d92`. Distinct answers: one per (model, schema, prompt) on the EPYC 7763 and one on the M1 Pro; the 3B reasoning-first answer differs between the EPYC 9V45 (2 requests) and the EPYC 7763 (55), and the M1 Pro's equals neither; the 8B reasoning-first answer on `ac36d799f9` is one text on the EPYC 9V45 and the EPYC 7763 (12 requests); on `b765936ca9` the M1 Pro's differs from the EPYC 7763's; both `system` answers equal across every machine and prompt. Per prompt (verbatim): `('llama3.1-8b', 'full', 'ac36d799f9') repeats 2 wall mean 44540.1 … pred_n [79.0]`; `('llama3.1-8b', 'full', 'b765936ca9') repeats 9 wall mean 43183.2 … pred_n [71.0]`.

### A1-06 — kernel source at v6.17 (git.kernel.org, 2026-10-09)
- `kernel/sched/fair.c` (`e00d16ce…`): `pick_task_fair` `:8740`, its first test `:8747–8748`; `pick_next_task_fair` `:8771`, `put_prev_set_next_task` `:8828`, `sched_balance_newidle` `:8833`. `kernel/sched/core.c` (`685d051d…`): `__pick_next_task`'s fair-class fast path `:6001`. `kernel/trace/trace_functions_graph.c` (`43d33b60…`): `calltime` `:255`, `rettime` `:356`. Copies `SCR/C1-campaign/kernel/`.

### A1-07 — S3-21 restricted to the pooled repeats
- S3-21's scripts verified first (`switch_rates.py` `07fd828e…`, `summarize.py` `334a8a8a…`, `busy_share.py` `16e234bb…`) and re-run: `rates.tsv` and `summary.txt` byte-identical to the record. Restriction `SCR/C2-switchrates/scripts/restricted.py` (`6cdd3879…`) with the pooled lists of each slice's `pooled.json` (9.5 `results-re-measured/`, `results-same-machine/`; 9.6 `results/pooled.json`; 9.7 `{borg,7z,steamcmd}-pooled.json`; 9.8, 9.9 `pooled.json`; 9.10 per campaign). Output `restricted-summary.txt` (`0cb08b95…`), verbatim:
  ```
  [restricted, without the mnist-madvise check] groups 67; group medians min 12.9, median 422.0, max 12497.2
    >=100: 53, >=1000: 13, >=10000: 2
    >=1000 groups: steamcmd/steam-fresh-untraced 12497.2; steamcmd/steam-fresh-shaped 11094.5; steamcmd/steam-fresh-unshaped 5716.1; webrtc/play 3119.3; launch-webrtc/launch 2907.4; borg/borg-first-cold 2206.4; thunderbird-send/op 1583.6; mpv-video/play 1577.7; launch-mpv-video/launch 1521.2; code/driven-alt 1498.2; None/handbrake 1489.0; None/ffmpeg 1141.1; code/driven 1098.8
    phase files n 1223, p10 83.2, p50 439.5, p90 3085.0, max 14036.3
    min group: mnist/mnist-train 12.9, 7z/7z-mmt1-warm 13.0, session/steady 16.9
    median-adjacent: thunderbird-send/driven 388.3, mpv-audio/play 422.0, None/build-j8-warm 436.9
  ```
  Per-phase lists and every kept and dropped file: `restricted-pergroup.tsv` (`4e615cb2…`), `restricted-detail.json`. Row check `verify_rows.py` (`d91de534…`): 2 688 297 487 matched lines over 2 195 files, every one a switch row, no "lost events" line. perf and kernel source at v6.17: `tools/perf/builtin-sched.c` (`993b39a7…`), `kernel/sched/core.c` (`685d051d…`).

### A1-08 — S3-21's busy shares restricted
- `SCR/C2-switchrates/scripts/busy_share_restricted.py` (`aba5f30c…`), output `busy-restricted.txt` (`6ddba8b7…`), verbatim:
  ```
  build build-j8-warm: repeats 14 (pooled 14), busy share 0.9974–0.9977, median 0.9976
  build tracker: repeats 14 (pooled 14), busy share 0.2042–0.2541, median 0.2069
  build clamscan: repeats 10 (pooled 10), busy share 0.9334–0.9435, median 0.9387
  build train: repeats 8 (pooled 8), busy share 0.8475–0.8575, median 0.8548
  ```
  (the other five lines as recorded).

### A1-09 — the indexer over its job, and 9.6's rescan over its job
- `SCR/B4-dataset/job_sat.py` (`77e1d7df…`) and `rbb.py` (`db8b151a…`) over the 18 pooled repeats of `meas-ci:background:2026-10-02b` (runs 37077892756, 37077613408, 37077654870, 37079168920, 37079295954, 37079532509, 37079763885, 37080205717, 37080669302; load CPU 3). `tracker_sat.txt` (`fcfa0df4…`), verbatim summary:
  ```
  sat: n 18 min 0.65495 max 0.67554 median 0.66613
  sat_from_init: n 18 min 0.88357 max 0.91070 median 0.90206
  init_s: n 18 min 15.36600 max 16.23500 median 15.71400
  ```
  `tracker_rbb.txt` (`f5ab056f…`): "repeats 18; per-repeat mean 1.7917-1.9317 ms, mean of means 1.8566, pooled mean 1.8559 ms over 383088 runs, pooled median 0.0580 ms; share past 10 ms 0.8432-0.8479".
- `rescan96.py` (`937184a1…`) over 9.6's 14 pooled repeats; `rescan96.txt` (`f8624aff…`): "busy_phase: n 14 0.2042-0.2541", "prog_sat_job: n 14 0.9261-0.9639", "phase_span_s: n 14 20.7830-25.8510".

### A1-10 — the encode and the backup over their jobs
- `job_sat.py` over the HandBrakeCLI pool (runs 37109133562 r1–r3, 37109333265 r4–r5): `handbrake_sat.txt` (`177fc150…`) "sat: n 5 min 0.99938 max 0.99947"; over Déjà Dup's 28 (repeats 1–30 less 12 and 25): `dejadup_sat.txt` (`8440588…`) "sat: n 28 min 0.99352 max 0.99517".

### A1-11 — `cc1`'s wakes per object job
- `SCR/B4-dataset/cc1_wakes.py` (`e70fe192…`, importing 9.6's analyzer read-only) over 9.6's 14 pooled repeats; `cc1_wakes.txt` (`c1a38d23…`): per repeat 2 857 object jobs, `cc1` waking once in 0.9919–0.9961 of them (repeat 4: 0.9930); pooled 39 749 / 39 998.

### A1-12 — the switch-cost papers re-read
- S1-21, Li, Ding & Shen, ExpCS 2007: `https://www.cs.rochester.edu/~kshen/papers/expcs2007.pdf` → `S/sources/S1-21/audit-2026-10-09/expcs2007.pdf`, SHA-256 `8b7a606976610acd6332c7cef6592d58380d49d611a696bf05d2ea122f0c71cf` (the record's). Passages: p. 2 "is 3.8 microsecond"; §3.1 "context switch times ranging from 4.2µs to 8.7µs. This is because the entire dataset of our benchmark … can fit into the L2 cache"; "increases dramatically, from 38.6µs to 203.2µs, with the increment of array size"; "The third region starts from the array size 512KB"; §3.2 "When the access stride is 128B, the cost ranges between 133.8µs and 1496.1µs with the mean 825.3µs".
- S1-23, Becker & Chakraborty, arXiv 1811.01412v2: `https://arxiv.org/pdf/1811.01412v2` → `S/sources/S1-23/audit-2026-10-09/becker-1811.01412v2.pdf`, `27f6c68ec8f3c688d07ad5a31db7d018c64393d7e43bc07d46da346c1ac52c67` (the record's). §2.2.2, p. 7: "Using lmbench, we found that context switches on our system take at least 3,400 cycles, with a frequent value around 30,000 cycles."
- S1-01, ghOSt, SOSP '21: `S/sources/S1-01/audit-2026-10-09/ghost.pdf`, `c37d636045a45e2216e7047ba1fb9ffa4ed88fe54b09ee0ccc33435cacd35c91`. Printed p. 595: "Unless otherwise noted, experiments run on Linux 4.15 with our ghOSt patches applied"; Table 3 "599 ns" (CFS context switch overhead).

## A2 — sources re-read

Copies under `sources/<id>/audit-2026-10-09/` (gitignored), fetched 2026-10-09 unless stated.

### A2-01 — Miller 1968 (`miller-fjcc68`), re-read
- Copy: `https://yusufarslan.net/sites/yusufarslan.net/files/upload/content/Miller1968.pdf` → `sources/miller-fjcc68/audit-2026-10-09/Miller1968.pdf`, SHA-256 `470bc40b3200c6e289d5e4fc276d6d3c416d5574079ef752da27aa366d6da990` (byte-identical to 9.11's S1-01).
- Passages, p. 271: "This response should be immediate and perceived as a part of the mechanical action induced by the operator. Time delay: No more than 0.1 second."; "the delay between depressing the key and the visual feedback should be no more than 0.1 to 0.2 seconds"; "(Note that this delay in feedback may be far too slow for skilled keyboard users …)"; "the best calculated guesses by the author, a behavioral scientist".

### A2-02 — Deber et al., CHI 2015 (`deber-chi15`), re-read
- Copy: `https://www.tactuallabs.com/papers/howMuchFasterIsFastEnoughCHI15.pdf` → `sources/deber-chi15/audit-2026-10-09/howMuchFasterIsFastEnoughCHI15.pdf`, `e8b7cd6e81b39db59b257eb1fb08388cd573be6284aa7e6b7ef3efe4e05a2eaa` (byte-identical to 9.11's S1-11).
- Passages: p. 1829, "an indirect setup akin to a laptop touchpad and screen"; "Indirect systems separate input and output regions and require a pointing tool such as a mouse, touchpad, or stylus"; p. 1831, "mean JND values of 69 ms and 96 ms for Direct and Indirect input" (tapping); "the textbook threshold of 100 ms (a value based on Miller's work [16] …)".

### A2-03 — Linux `Documentation/scheduler/sched-eevdf.rst` at `7b63ef2d`, re-read
- Copy: `sources/S2-03/audit-2026-10-09/sched-eevdf-7b63ef2d.rst`, `75b99048d738b7683d06c5844e150253e91d75ec46e774f7a96cf0e9d39056a0` (byte-identical to S2-03's).
- Passages: `:18–22` "EEVDF picks tasks with lag greater or equal to zero and calculates a virtual deadline (VD) for each, selecting the task with the earliest VD to execute next. It's important to note that this allows latency-sensitive tasks with shorter time slices to be prioritized, which helps with their responsiveness."; `:30–32` "tasks can request specific time slices using the new sched_setattr() system call".

### A2-04 — OSTEP chapters 7 and 8, re-read
- Copies: `sources/S1-03/audit-2026-10-09/cpu-sched.pdf` `0912b1a34977a70704b921ecfdf0dd65300e038a3eb4e5e57b2d9c38f66b63c3`; `sources/S1-02/audit-2026-10-09/cpu-sched-mlfq.pdf` `96241b4e6708991740560334a1f67516c3c68eb3e6a570af7b03cdb4b32918db` (byte-identical to S1-03, S1-02).
- Passages: ch. 7 p. 2, §7.1's assumptions 1–5 ("4. All jobs only use the CPU (i.e., they perform no I/O)"); p. 3, "let's relax assumption 1, and thus no longer assume that each job runs for the same amount of time"; p. 5, "given our assumptions about jobs all arriving at the same time, we could prove that SJF is indeed an optimal scheduling algorithm"; p. 6, "if we knew job lengths, and that jobs only used the CPU, and our only metric was turnaround time, STCF would be a great policy"; ch. 8 p. 9, "from 20 milliseconds (highest priority) to a few hundred milliseconds (lowest)".

### A2-05 — `updatedb` on Ubuntu 24.04 and Debian unstable
- Copies (`sources/S3-02/audit-2026-10-09/`): `ubuntu-noble/ubuntu-24.04.5.1-desktop-amd64.manifest` (releases.ubuntu.com) `6c200933618b2e382e7732b69b247aa5f63ed6600d8ee730d57b02ec74e4f8ff`; `noble-Release` (Date: Thu, 25 Apr 2024 15:10:33 UTC) `26758a13cecfaff9ff274d31ea9a4633674a999bd130c09f6ecd66a4b8071184`; `noble-main-binary-amd64-Packages.xz` `2a6a199e1031a5c279cb346646d594993f35b1c03dd4a82aaa0323980dd92451`; `noble-universe-binary-amd64-Packages.xz` `ba9057fa1b91438cc8a1d26808d00c85389fe101d0c1496254df97236405599a`; `plocate_1.1.19-2ubuntu2_amd64.deb` `90375d69eda16ca5f73e6449447ef05c1a18b7b1de4092879eda9850898c04b0`, its `usr/lib/systemd/system/plocate-updatedb.service` `201399ab568b2b32aba0a1def593fe6c9f858d54d912e3c857ad17ecba9b74ed`, its `etc/cron.daily/plocate` `bca4957664bb8eea3b9c25f6dc60d2e74b7884d72dc4e67874add777e4ba56db`; `locate_4.9.0-5build1_amd64.deb` `9e1827bb36373d64607b8580fdb1dccc87cb33473ccf1353404224e112996abe`, its `etc/cron.daily/locate` `35939ea423f9d5828853adab6828043e5a516d47551a3053902f7dd333fc5f1d`; `launchpad-plocate-noble.json` (Launchpad `getPublishedSources`, plocate, noble) `f4d4561102bb57e4b2c4a0d2ce1a13a5c5e744b44d21359ba0eab637f277b58e`; `debian-sid/plocate-1.1.18-1_plocate-updatedb.service.in` `6301b1ec…`, `plocate-1.1.23-1_plocate-updatedb.service.in` `f56f4ee223c9e95863ac3368113af79f22637a7f9a91654db11e4eb16c281315`, `plocate-1.1.25-1_plocate-updatedb.service.in` `d8867da6abc3e7062679c51c8b7e46d8f9484c337b127a0efe97410e0bede5a7`, `plocate-1.1.25-1_NEWS` `4a6787be7564998827c9cdf43d5e108fbec7d23625b6daf07131dfaa6def6e20`, `findutils-4.11.0-3_debian_locate.service` `48cb7fe113e740ac879f59cc5508c70a461b4c5885ffe240166855fab54e7b3f`.
- Passages: the noble unit — "[Unit] Description=Update the plocate database ConditionACPower=true [Service] Type=oneshot ExecStart=/usr/sbin/updatedb.plocate LimitNOFILE=131072 IOSchedulingClass=idle PrivateTmp=true …" (no `Nice=`, no `CPUSchedulingPolicy=`); its cron job, `:7–10` "# Skip if systemd timer is available. if [ -d /run/systemd/system ]; then exit 0"; plocate 1.1.23-1's unit `:9–10` `IOSchedulingClass=idle`, `Nice=19`; NEWS "plocate 1.1.23, November 24th, 2024 — Various improvements, in particular to the systemd unit file."; findutils' noble cron job `:31` `NICE=10`, `:35` `IONICE_CLASS=3`, `:68` `nice -n ${NICE:-10} updatedb.findutils`; universe `Packages`: plocate Version 1.1.19-2ubuntu2, Section universe/utils, Priority optional; Launchpad: 1.1.19-2ubuntu2 Release Published 2024-04-19 (1.1.19-2ubuntu3 Proposed, Deleted); the manifest has no plocate, mlocate or locate line and has `tracker-miner-fs 3.7.1-1ubuntu0.1`; `ubuntu-desktop`, `ubuntu-desktop-minimal`, `ubuntu-standard` 1.539 Depends/Recommends name no locate package.

### A2-06 — OBS knowledge base page, the banner
- Copies: S2-55's `sources/S2-55/obsproject.com_kb_encoding-performance-troubleshooting.html` `06a57e86615323aab8d9151c87e657344b6a919712aafb053ddeb92d1cf53ebf`; today's `sources/S2-55/audit-2026-10-09/obsproject.com_kb_encoding-performance-troubleshooting.html` `6a9c9b8ed29ec647a8c63acaf4cb66ee604ef42c1656da4650f8c88650999525`.
- Passage, line 150 of both: `<!--<div id="noticeBar" style="margin-bottom: 32px;">Hey there! The OBS knowledge base is still currently a work in progress. While it is publicly accessible, we ask that you avoid linking users to any knowledge base pages at this time. Thank you!</div>-->` — inside an HTML comment, not displayed.

### A2-07 — The Cargo Book, "Why Cargo Exists"
- Copy: `https://doc.rust-lang.org/cargo/guide/why-cargo-exists.html` → `sources/S2-56/audit-2026-10-09/why-cargo-exists.html`, `10fabdb2e75bd1ae8177ef03cca9aab5e9420acd505422320f93cb9ee07d55a4`; `index.html` and `cargo-build.html` byte-identical to S2-56's.
- Passage: "To accomplish this goal, Cargo does four things: … Invokes `rustc` or another build tool with the correct parameters to build your package."

### A2-08 — Ardour manual, jackd(1), PipeWire, Steam Deck, re-read
- Copies: `sources/S2-38/audit-2026-10-09/` — `latency-considerations.html` `2f7429aa5dca1f1f2cecfe42d86d704084e41c3dbe81e7902fb483567fa58b17`, `latency-and-latency-compensation.html` `d3af5c17f37fcd70ccf9b7811d1201e43ffcde52575d3a74b570bb7038518346`, `preferences.html` `02fa43bca439d2dda3dde77d822988062215ac8861541b4e36c1932088d0c704` (byte-identical to S2-38/S2-57, the manual at `9628c8ba`); `sources/S2-37/audit-2026-10-09/jackd.0` `2c4eb5886fc7bd153622f200225070690c4f487e794c2ef4359d5d380941a47b`; `sources/S2-36/audit-2026-10-09/pipewire.conf.5.md` `8e08d8e6ff3d2ccb8277066e937210e39928372dc92fe0cffd2dcef917d3a0d9`; `sources/S2-39/audit-2026-10-09/steamdeck.html` `3d0cc70603370e7f0667d1590b646c9a2948f164b048642e07d3da2eb7901259` (the page is dynamic).
- Passages: Ardour `latency-considerations.html:12–23` (A/D/A "about 1.5–2 ms"; "Latency below 5 ms should be suitable for a professional recording setup"; "extremely low buffer sizes"; "Not all computer audio systems are able to work reliably at such low buffer sizes"), `:26–28` ("route the monitor signal through an external mixing console while recording, an approach taken by most if not all professional recording studios"); `latency-and-latency-compensation.html` — capture latency "(usually one audio period)", "the combination of both matters. It is called round-trip latency"; jackd(1), ALSA BACKEND OPTIONS (`:174`): `:244–246` playback latency "corresponds to --nperiods times --period divided by --rate. The default is 2", `:283–287` "If you need low latency, set -p as low as you can go without seeing xruns … The JACK capture latency in seconds is --period divided by --rate. (default: 1024)", `:291–292` rate "(default: 48000)"; COREAUDIO BACKEND PARAMETERS (`:319`): `:357–359` rate "(default: 44100)", `:362–364` period "(default: 128)"; PipeWire `:214` `default.clock.rate = 48000`, `:227–228` `default.clock.min-quantum = 32`, `:233–234` `default.clock.quantum = 1024` "Default quantum used when no client specifies one"; Steam Deck: "up to 60Hz refresh rate" (LCD list), "up to 90Hz refresh rate" (OLED list), and, in an embedded update post, "The in-game screen refresh rate can now be adjusted on the fly anywhere between 40-60Hz."

### A2-09 — Lottery scheduling (`waldspurger-osdi94`), re-read
- Copy: `sources/S1-09/audit-2026-10-09/lottery.pdf`, `e704678ec0cf6064136794a23c1722ad32a24868259dcdf3a9ad8087d8f1b73a` (byte-identical to S1-09); the formula read on the rendered page image (the text layer garbles it).
- Passages, §2.2, p. 2: "The number of lotteries required for a client's first win has a geometric distribution. The expected number of lotteries n that a client must wait before its first win is E[n] = 1/p, with variance σ²ₙ = (1 − p)/p². Thus, a client's average response time is inversely proportional to its ticket allocation."; "With a scheduling quantum of 10 milliseconds (100 lotteries per second)"; "Since any client with a non-zero number of tickets will eventually win a lottery, the conventional problem of starvation does not exist."

### A2-10 — Liu & Layland (`liu-jacm73`), re-read
- Copy: `sources/S1-10/audit-2026-10-09/liu-layland.pdf`, `de9fb72577ff1f45aa50ccae0774b248ef67ebe15c6b6e90b00e0ab377f2b927` (byte-identical to S1-10; OCR text layer).
- Passages: printed p. 55 (PDF p. 10), "This method is optimum in the sense that if a set of tasks can be scheduled by some priority assignment, it can also be scheduled by this method"; "priorities are assigned to tasks according to the deadlines of their current requests"; printed p. 56 (PDF p. 11), "THEOREM 7. For a given set of m tasks, the deadline driven scheduling algorithm is feasible if and only if (C1/T1) + (C2/T2) + … + (Cm/Tm) ≤ 1. PROOF. … (C1/T1) + (C2/T2) + … + (Cm/Tm) > 1, there is clearly no feasible scheduling algorithm."; printed p. 58 (PDF p. 13), "the deadline driven scheduling algorithm is optimum in the sense that if a set of tasks can be scheduled by any algorithm, it can be scheduled by the deadline driven scheduling algorithm."

### A2-11 — The provenance guard: contracts and code at `a7ad2f29`
- `docs/data-contracts.md:344` (§7): "`held` (proposal rejected; previous config carried forward), or `fallback` (the default, from boot or after repeated failures)"; "`config` is the post-validation configuration actually in force after the entry — clamped values for `clamped`, the carried-forward config for `held`". `harness/tools/harness/aggregates.py:185–187`: `fb = ci[ci["provenance"].isin(["fallback", "held"])]` → `fallback_share`. `harness/guards/guard-spec.yaml:114–123`: `provenance_share`, threshold 0.5, `direction: below`, `applies_to: [oracle, random, whitelist, llm_vocab, llm_algo, llm_full]`. `harness/boot-defaults/`: ten JSON files, each `"algorithm": "MLFQ"`.

### A2-12 — Chambers et al., IMC 2005 (S3-23), PDF
- Copy: `https://www.usenix.org/legacy/event/imc05/tech/full_papers/chambers/chambers.pdf` → `sources/S3-23/audit-2026-10-09/chambers.pdf`, `6d9dea3b145f9513917b82a636702d966286bb3a17734c53280067d7be0a0c3a`.
- Passages: p. 1, "a 13-month trace of an extremely busy game server containing over 2.8 million connections"; p. 2, the trace table, "cs.mshmro.com trace Start time Tue Apr 1 2003 End time Mon May 31 2004 Total connections 2,886,992"; p. 4, §3.2 "Gamers have short attention spans": "a significant number of players play only for a short time before disconnecting and that the number of players that play for longer periods of time drops sharply as time increases"; "more than 99% of all sessions last less than 2 hours"; "a Weibull distribution with β = 0.5, η = 20, and γ = 0 closely fits the PDF of measured session times for the trace" (Figure 2, minutes).

### A2-13 — WoWAH, MMSys 2011 (S3-11), PDF
- Copy: `https://web.cs.wpi.edu/~claypool/mmsys-dataset/2011/wow/p123.pdf` → `sources/S3-11/audit-2026-10-09/p123.pdf`, `5ef59d759f236cbe6f4dfc6a10bac2f7d0fff6db449dc84c3793c38a1a7ce9c5`.
- Passages: p. 124, "the Light's Hope realm in Taiwan"; "the status of 91, 065 avatars over a 3-year period (Jan. 2006 …"; p. 125, Table 1 "Realm TW-Light's Hope; Faction Horde; # of avatars 91,065; # of sessions 667,032"; p. 126, "We summarize the quantiles and averages of the average daily play time, average session play time, and average daily session count in Table 4"; Table 4, "(Mean, SD)", "Quantiles (5%, 25%, 50%, 75%, 95%)", "Session time (hr) (2.8, 1.8) (0.4, 1.0, 1.8, 3.0, 5.5)"; "If we analyze the average session play time, we find significant "knee" around 1 hour and 5 hours".

### A2-14 — Wei et al., Sprague et al., Tam et al., re-read; Tam et al.'s published version
- Copies: `sources/S1-26/audit-2026-10-09/2201.11903v6.pdf` `7d9f878c23b460e4566aa4ec9201b1abfb3b8faefb2b1356e411cb90fef72a12`; `sources/S1-28/audit-2026-10-09/2409.12183v3.pdf` `9f6aeece29b29ed4a20e7edbb430267e11ed6481ce872edc1bff91a9069573a1`; `sources/S1-27/audit-2026-10-09/2408.02442v3.pdf` `172930a8e9166ded9df95bb9ec41aafb7f43907969d14ea2dd05240d2c902f75`; `sources/S1-27/audit-2026-10-09/2024.emnlp-industry.91.pdf` `c8145f4d94b4112833a3f6f90535a60671864408dce0d0479d2fb6e6bdf80d6e` (equal to `https://aclanthology.org/2024.emnlp-industry.91.pdf`, fetched 2026-10-09; "Let Me Speak Freely? A Study on the Impact of Format Restrictions on Performance of Large Language Models", printed pp. 1218–1236).
- Passages: Wei p. 4, "does not positively impact performance for small models, and only yields performance gains when used with models of ∼100B parameters"; §3.1 (p. 4), "We evaluate five large language models. The first is GPT-3 … 350M, 1.3B, 6.7B, and 175B parameters … LaMDA … 422M, 2B, 8B, 68B, and 137B parameters. The third is PaLM, which has models of 8B, 62B, and 540B parameters. The fourth is UL2 20B …, and the fifth is Codex". Sprague, Table 6 (p. 25), "Direct answer and CoT accuracies for each reasoning category across models" (Commonsense, Knowledge, Mathematical, Symbolic, Soft; DA % / CoT %): Gemma 2 9b 75.0/76.1, 74.9/76.9, 18.5/50.5, 46.7/55.8, 58.2/60.5; Meta-Llama 3.1 8b 72.9/73.4, 70.1/74.1, 16.0/47.8, 34.8/51.6, 55.0/56.2; Qwen 2 7b 64.0/66.1, 65.2/71.3, 15.9/53.5, 43.8/52.3, 54.4/49.4; §4.2 (p. 6), "there is little to no separation between the performance of zero-shot CoT and zero-shot direct answer"; p. 2, "For non-math questions, we find no features to indicate when CoT will help". Tam (published version): §3.2 (p. 1220), "we limit the number of key-value pairs for each dataset to 2: reasoning and answer fields"; §3.3 (p. 1220), "For open weights model we use LLaMA3-8B-Instruct … and Gemma-2-9BInstruct"; p. 1221, "we found that 100% of GPT 3.5 Turbo JSON-mode responses placed the "answer" key before the "reason" key, resulting in zero-shot direct answering instead of zero-shot chain-of-thought reasoning"; "The order of keys in structured outputs and the decoupling of reasoning from format adherence emerge as important factors in maintaining LLM capabilities while providing structured responses"; p. 1222, "In Table 11 we found in classification task JSON-mode performs much better than text due to the restriction on answer space. However in reasoning related task, JSON-mode failed to adhere to the order of reasoning first followed by answer"; Conclusion (p. 1224), "Format restrictions, particularly constrained decoding (JSON-mode), can hinder reasoning abilities while enhancing classification task accuracy." Each passage is worded the same in arXiv v3 (pp. 3, 3, 4, 4, 5, 7).

### A2-15 — Vulcan (S1-18): tables and DOI
- Copies: `sources/S1-18/audit-2026-10-09/vulcan-2512.25065v3.pdf` `ed85ead607bee6409a2d1fa0389063d0d513f09a718c53317affe028ca16fed6`; `vulcan-2512.25065v1.pdf` `9ac8414ea6c9c6a261bf47d245739dc7a60982f22a6033cdc766f6695de87d7b` (both byte-identical to S1-18's record); `doi-handle-api.json` (`{"responseCode":100,"handle":"10.1145/3842654.3848582"}`), `crossref-vulcan.json` ("Resource not found."), `datacite.json`, `acmdl-doi.html`, `acmdl-doi-chrome.html` (challenge pages).
- Passages: v3 p. 6, Table 1, "Examples of systems resource management tasks and the type of task (Value or Rank) they fall into" — "CPU scheduling [70] | Select which thread to schedule next. | Rank: all runnable threads."; v1 p. 4, Table 1 (the same row, "[76]"); v1 p. 6, "Table 3: Examples of RANK tasks", columns "Memory Tiering | CPU scheduling"; v3 §3.2, "for our case studies (§7), we use two approaches (ShinkaEvolve [51], OpenEvolve [87])"; "we executed 17 caching algorithms using libCacheSim [43]"; v3 p. 1, "EuroSys '27, Rabat, Morocco … https://doi.org/10.1145/3842654.3848582".

### A2-16 — TuxBot v2 (S1-17), re-read
- Copy: `sources/S1-17/audit-2026-10-09/tuxbot-2605.15026v2.pdf`, `543bd4fcc48785e2762de4a098f3feb2dd72f7732b21f514d178de2233a90760` (byte-identical to S1-17's record).
- Passages: p. 1, "A fast loop proposes low-latency updates, a slower loop periodically revises the search strategy, and every proposed change passes [through typed validation …]"; "they are not inline on each request, and they are not kernel fast-path controllers such as the CPU scheduler"; p. 9, "TuxBot (ST) uses Gemini 2.5 Flash as the Reasoning loop and Gemini 2.5 Flash-Lite as the Inst[…]".

### A2-17 — LumOS, "An Expert in Residence" (S1-20), read in full
- Copy: `https://liargkovas.com/assets/pdf/Liargkovas_ML4Sys_NeurIPS25.pdf` (linked as the paper from `https://daplab.cs.columbia.edu/projects/lumos`, whose page is byte-identical to S1-20's `lumos.html`, `166682047325887490611462a67374ebd4534db7952dfb9c8fa88d2ad9a28c22`) → `sources/S1-20/audit-2026-10-09/Liargkovas_ML4Sys_NeurIPS25.pdf`, `e69e0deb647c596a0c2ad3f2d1ac045e1f37b8d203fb90b60b196c4a06b29078`, 12 pages, PDF created 2025-09-30, a diagonal draft watermark. OpenReview's PDF (`openreview.net/pdf?id=7dhlgPp8ni`) returned HTTP 403 again and its forum page a browser-verification page (`openreview-7dhlgPp8ni.pdf` and `openreview-forum-7dhlgPp8ni.rendered.html` in the folder are those error pages, not copies). No arXiv version (arXiv API, author Liargkovas, 2026-10-09).
- Passages: p. 1, authors "Georgios Liargkovas, Vahab Jabrayilov, Hubertus Franke, Kostis Kaffes", "39th Conference on Neural Information Processing Systems (NeurIPS 2025) Workshop: Machine Learning for Systems"; p. 2, "The goal is to minimize application-level p99 tail latency under load by adjusting two related knobs: latency_ns … and min_granularity_ns"; "a prompt-driven LLM loop (Gemini 2.5 Flash). All tuners run for the same number of cycles (200 by default). Each cycle consists of a 10-second workload run, metric collection, and a new configuration proposal."; p. 3, "the LLM (Gemini 2.5 Flash) reduces p99 by 5.0% in 1-parameter tuning (47.16 ms vs 49.62 ms) and by 7.1% in 2-parameter tuning (53.95 ms vs 58.09 ms)"; "tool inputs are described via JSON Schema and validated server-side (types/ranges), and we add semantic/unit checks beyond schema"; p. 4, "Results reflect one hardware class, Linux 5.15, and a TPC-C/PostgreSQL workload"; p. 6, "2× Intel Xeon Gold 6248R @ 3.00 GHz". No recognition or classification measure.

### A2-18 — `scx` at `v1.1.3` (`c8728c6b`), re-cloned
- Copy: `sources/S2-09/audit-2026-10-09/scx` (HEAD `c8728c6b6a3fde451f0f10b95f99aad7a32a750a`); `README.md` `b285939f618abb76625912cfa7f6a3f7017675852d6aa2b9de51ea2db419ae6b`, `OVERVIEW.md` `0a97538a0407981a5f48ccb1e69e1196eeb7ef32e154d35f8258b12d89a4b706`.
- Passages: `README.md:33–35`, "`sched_ext` is supported by the upstream kernel starting from version 6.12. Both Meta and Google are fully committed to `sched_ext` and Meta is in the process of mass production deployment."; `OVERVIEW.md:283–284`, "Distros are able to package and release these schedulers".

### A2-19 — Windows Game Mode: the Xbox Support article's dated copies and Xbox Wire
- Copies (`sources/S2-58/audit-2026-10-09/`): `xbox-gamemode.rendered.html` (headless Chrome, fresh profile) `06d24dada830871eae8a09262c0545ba34b1a8e1572bcd223e5bfefb7b46feae`, its article text identical to S2-58's rendering; `wayback/wb-20181230054712-en-US-games-game-setup.html` `b757875a2800940739f7f4980af3cc03a9c0c79361fe9f4c3a206fdffc38abf8` and `wayback/wb-20180706084246-en-US-games-game-setup.html` `0ce4937a57ac991f4e97438aec43a7bfbbabe508008d496ee4418ed5829cb904` (Internet Archive captures of `https://support.xbox.com/en-US/games/game-setup/use-game-mode-gaming-on-pc`, confirmed in the CDX index; 12 further captures 2017–2019 in the folder); `wayback/wb-20220808125358-xbox-wire-2018-10-02.html` `1223ccfccedf1e795b0b6a797b3f54051bcdd4530a4fea3d7b280619d038e312` (capture of `https://news.xbox.com/en-us/2018/10/02/latest-october-2018-windows-update-gaming-features/`; the live site returned 403, its saved 403 page `xbox-wire-2018-10-02-latest-october-2018-windows-update-gaming-features.html` is not a copy).
- Passages: 2018-12-30, "When you use Game Mode, Windows prioritizes your gaming experience. When you're running a game, Game Mode: Prevents Windows Update from performing driver installations and sending restart notifications."; "Game Mode is on by default."; 2018-07-06, no "Windows Update"; Xbox Wire, `datePublished` "2018-10-02T21:44:22Z", "Now auto-enabled for all games with a master On/Off toggle in Windows Settings, Game Mode suppresses Windows Update driver installs and blocks Windows Update interruptions such as restart notifications while you're gaming."

### A2-20 — SYSmark 2012 departures: Dessau's post and X-bit Labs
- Copies: `sources/S2-40/audit-2026-10-09/wayback-20110623165026id-dessau-1006.html` (`https://web.archive.org/web/20110623165026id_/http://blogs.amd.com:80/nigel-dessau/2011/06/21/1006/`, the earliest capture in the CDX index) `99434f4ffe367d9d78f746875a9a48ea76bf80919846e91b7ea0f898338a35ad`; `wayback-dessau-2011.html` `ff29c4487eec2d40642fbff037f50ed0abf41a87e77fe0800a30ff7658bda71a` (a later capture of the same post, the same passages); `amd-pr-368.html` `e7b265c2594d87f2d15494b77e2747333782cffb6d5939ccf7e56ab372eff8e0` (byte-identical to S2-40; links `blogs.amd.com/nigel-dessau/2011/06/21/1006/` as "Executive Blog"); `sources/S2-43/audit-2026-10-09/wayback-xbitlabs-20110623214036.raw` `91ea7ea73316270d8d41c7e3a3147075a3c61cb21bf25027e463089087eda98c` (X-bit Labs, `news/other/display/20110623214036_Nvidia_Via_Technologies_Confirm_Quitting_BAPCo.html`; captures from 20110625114727 in the CDX index); `sources/S2-41/audit-2026-10-09/wayback-20120106144430id-anandtech-4464.html` `65be098e5412c24698ad0334404957cd6c050bbd4fd968e22e34402c6d812352` (byte-identical to S2-41).
- Passages: Dessau — title "Voting for Openness", "June 21, 2011"; "We got workloads included that represent the things you and I actually do in a day (instead of 35,000 line spreadsheets!). But the question remained: what weighting would BAPCo ultimately give to the real-world workloads − since it is this weighting that defines the actual benchmark scores."; "only 7 applications and less than 10 percent of the total measurements dominate the overall score"; "a relatively large proportion of the SM2012 score is based on system performance rated during optical character recognition (OCR) and file compression activities − things an average user will rarely if ever do"; "SM2012 scores do not take into account GPU-accelerated applications"; "The heart of our complaint is this: the SYSmark benchmark is not only comprised of unrepresentative workloads (workloads that ignore the importance of heterogeneous computing and, frankly, favor our competitor's designs), but it actually generates misleading results"; "Nigel Dessau is Senior Vice President & Chief Marketing Officer for AMD. His postings are his own opinions and may not represent AMD's positions". X-bit Labs — "due to disagreements over the scoring system of SYSmark2012 which does not take graphics card's role into account"; ""We have resigned [from BAPCo]," said Irina Shekhovt[sova]". AnandTech — VIA's tests "do not accurately reflect real world PC usage scenarios and workloads"; Nvidia "No reason was given"; "a long standing dispute over the weighting of scores within the SYSmark suite".

### A2-21 — Artificial Analysis (S3-18) and LocalScore (S3-05), re-read

- **Copies.** Artificial Analysis, https://artificialanalysis.ai/models/llama-3-1-instruct-8b/providers — live 2026-10-09, `sources/S3-18/audit-2026-10-09/live-aa_llama31_8b_providers.html` (`7b83e81c4366c66cde7557b12eb97c9b7be364355e03c99165b6dfb9faf6fdd7`); the Internet Archive's capture 20260926065420, `wayback-20260926065420-aa_llama31_8b_providers.dec.html` (`73d6327b74314247ca4b1567f850168e8db0467adbbfda826a8d902f2e84355e`). S3-18's own copy (2026-10-07, `99a25492…`) is not on this machine; no capture lies between 2026-09-26 and 2026-10-09. LocalScore's model 1 page — live 2026-10-09, `sources/S3-05/audit-2026-10-09/live-model_1.html` (`b834a9d502afbb2d5042cafc9f5526142edf667f411003a4e6f0ac01ecbf42e6`); capture 20260926104509, `wayback-20260926104509-model_1.dec.html` (`e89a465add560721b5bd837ff39406cdaf66e4bcd498a40cbd682d081d6d74b9`).
- **Passages.** Artificial Analysis: "Figures represent median (P50) measurement over the past 72 hours to reflect sustained changes in performance."; per-provider `timeToFirstToken.median` — live 2026-10-09: CoreWeave 0.658, Groq 0.870, Novita 0.967, DeepInfra 1.126 and 1.128 s; 2026-09-26: Amazon Bedrock 0.688, CoreWeave 0.711, Novita 0.867, Groq 0.922, Cloudflare 1.030, DeepInfra 1.072 s. LocalScore, both copies: `"avg_ttft":881.7180316018517, … "accelerator":{"name":"NVIDIA GeForce RTX 3060","type":"GPU","id":43,"memory_gb":12,…}`; a separate `"NVIDIA GeForce RTX 3060", … "id":4053,"memory_gb":8`. The site's aggregation: `cjpais/LocalScore` at `bd6ffe9d`, `src/db/queries.ts:816` (per-accelerator average over submitted runs); a run's value: llamafile `localscore/localscore.cpp:293–328` at `a3ccf098` (the mean of the run's nine tests).
- **Coverage.** D51's two published figures; the read date and window of each.

### A2-22 — llama.cpp at `bd4eeaa0`: the converter, the grammar sampler, the server
- Copies (`sources/S2-33/audit-2026-10-09/`): `grammars_README.md` `e1874c0f08abbcfe45eff0b7b0290faa58f630981bf94274e2d99751ef3b0208` (byte-identical to S2-33's); `common_json-schema.cpp` `68ba2adbb6e0578c0d89e99cc9a9a7aa9c0b554b555bcd3908da71789045509d`; `common_json-schema-to-grammar.cpp` `d5a82fff5d611abd1198ff27c328b20376ffe9f110b4771d579c8bd20c70541f`; `src_llama-grammar.cpp` `97d76071a2ed1b0c4ce827f002f554b12a25593776adb525dde33ac4cb1eb1e9`; `tools_server_README.md` `14824a98d0b67f910c083c1aa2f5585b786c2d56276c11aadecb7ee247673cab`; `tools_server_server-schema.cpp` `cb42015b6d45748573f2b32528980b7c41caf99bb7a1c776b98a27581bd93273`; `CMakeLists.txt.bd4eeaa0` `94d646f48594469909522d2a539aad943705309686646fd8a69cc15c43029e69` (raw.githubusercontent.com at `bd4eeaa047006cb1fe71999fbd11134b5836e167`). `examples_json_schema_to_grammar.py` is a 404 body (the Python converter the README names is absent at this commit).
- Passages: README `:143` "`llama.cpp` supports converting a subset of https://json-schema.org/ to GBNF grammars"; `:207` "Unsupported features are skipped silently. It is currently advised to use the command-line Python converter (see above) to see any warnings"; `json-schema.cpp` — the 22 keywords listed in D77; `:104–105` "unsupported $ref " + ref + ", only references into the same document are supported"; `json-schema-to-grammar.cpp:394–397` "pattern … is not supported (…), accepting any string"; `:952–961` integer bounds built (`build_min_max_int`); `:963–964` `KIND_NUMBER: return _visit_primitive(rule_name, "number");`; `:976–980` "JSON schema conversion failed" thrown on errors, "WARNING: JSON schema conversion was incomplete" to stderr on warnings; `llama-grammar.cpp:1366–1387` `allow_eog` only when a stack is empty, otherwise `cur_p->data[i].logit = -INFINITY` for end-of-generation tokens; server README `:666–669` `stop_type` `none`/`eos`/`limit`/`word`, `:674` `truncated`; `server-schema.cpp:265–269` the conversion inside `try`, rethrown as `"json_schema": …`; `CMakeLists.txt:146` `option(LLAMA_LLGUIDANCE "…" OFF)`. Project: `dataset/tools/meas/llm/run.sh:14` `LLAMA_SHA=bd4eeaa047006cb1fe71999fbd11134b5836e167`, `:45` default `cmake -B build -DCMAKE_BUILD_TYPE=Release`; `request.py:40–42` `"n_predict": 384`, `"json_schema"`, `POST /completion`.

### A2-23 — Apple XNU, `sched_clutch_edge.md`, re-read
- Copies (`sources/S2-54/audit-2026-10-09/`): `sched_clutch_edge.md` (tag `xnu-12377.121.6`) `5f4201d269593c0a7d39e347ccf7241fc43f88073db3be54339e19d7bd51532c` (byte-identical to S2-54's); `xnu-6153.11.26_osfmk_kern_sched_clutch.md` `aaf8b21907e237c69b40438a1fef913685ce6fc3cc75f3ebca11450a8f145584`; `xnu-7195.50.7.100.1_osfmk_kern_sched_clutch.md` `70c45ce1e39dbf73db5d717ba7a765d841f16de3e27677c76d9d7b1bc16d0a82`.
- Passage: `:7` in full as quoted in D78; the word "macOS" does not occur in the file; the same paragraph is in `osfmk/kern/sched_clutch.md:5` at `xnu-6153.11.26`.

### A2-24 — S3-20's unit count, re-run
- `python3 -I installed_units_count.py sources/S3-20` (the script copied to the scratch folder, run on S3-20's inputs): output SHA-256 `db9cb9c3956c44fb950b5d80133286700366406ced03c7bf755f2eca139c186f`, byte-identical to `sources/S3-20/installed_units_count.out`. Raising packages, from its lines: `Nice=` brltty, deepin-boot-maker, deepin-log-viewer, earlyoom, espeakup, frr, gdnsd, hdapsd, railcontrol, readsb, svxlink; `IOSchedulingClass=` hipercontracer, railcontrol; `CPUSchedulingPolicy=` hipercontracer, low-memory-monitor, osmo-bts, osmo-mgw, osmo-pcu — 16 packages; "lowering only 40, raising only 16, both 0".

### A2-25 — The cap and the executor: code and contracts at `a7ad2f29`
- `docs/research-proposal.md:439` ("the cap and the constants remain the table's"), `:441` (`llm_full` "fills the whole `cpu_scheduler` block"), `:131`, `:174`, `:517`, `:621`, `:908` as quoted in D79; `docs/data-contracts.md:415` "reason ∈ block | preempt | exit | depart"; `:467` "`random`, `whitelist`, `llm_vocab`, and `oracle` read `system` only and receive the row's **default** entry"; `docs/recognition-vocabulary.md:66` `"batch_bandwidth_cap": null | 0.05–0.95`, `:70` "the ceiling on the fraction of the lane the **batch class** may consume while non-batch work is runnable; `null` means no ceiling … The executor has no starvation window and no config field for one"; `daemon/driver-table/prior.yaml:17` "batch_bandwidth_cap is never null" (values: 0.05 ×16, 0.5 ×11, 0.333 ×4, 0.2 ×1); `simulator/src/sim.cpp:165` FIFO `horizon` → `kNoHorizon`, `:291–293` EDF deadline tasks → `kNoHorizon`, `:892–925` the loader (algorithm and params only), no occurrence of "bandwidth"; `docs/simulator/simulator-guide.md:210` (§5) "**Needed eventually** … per-class bandwidth caps, enforced by the executor regardless of what any config says"; `simulator/memo/memo_261001.md:93` "`batch_bandwidth_cap` — not even read from the config"; 9.11 D5 "a task whose declared class is idle runs only when no task of another class is runnable"; 9.11 D7 "With D5 an idle task waits behind every run of its editor by design".

(A2-21 unused.)

## A3 — the decision record and vol-02

### A3-01 — vol-02's quotation count by rule (audit, 2026-10-09)

- **Copy.** `docs/guidebook/vol-02-related-work.md` at `a7ad2f29`, blob `48a88bc2`, the same blob at `1a7c98e0`, `2f7c7b58`, `60149db`, `6db09240`.
- **Counted.** `grep -c -P '^>\s*["“]'`: 277 lines — chapter 2 47, 3 45, 4 4, 5 79, 6 50, 7 23, 8 29 (chapter headings `:268`, `:829`, `:1291`, `:1459`, `:2185`, `:2693`, `:3187`, `:3506`). Less `:3360` ("이 회사가 데스크톱 사용을 이 네 묶음으로 나눈다"는 것은 …, the guidebook's commentary); plus `:2715` (`> > "The Game Mode APIs are deprecated in Windows 10, version 1809 and later."`, a source quotation nested in the "확인한 방식" callout at `:2711`). `:2609` ("**첫째, 제목이 바뀌었습니다.** 첫 판본의 제목은 "OS-R1: Agentic Operating System Kernel Tuning with Reinforcement Learning"이었습니다.") is a title quoted inline inside the "인용 정보 정정" callout (`:2607`). Total 277 = 92 + 133 + 52. The code blocks of chapter 7 (`:2864`, `:2878`, `:2925`, `:2944–2990`, `:3071–3074`, `:3082–3086`) and the inline output line in chapter 8 (`:3229`) are outside the count, as V60 lists them.
- **Coverage.** Item 60's count; V60's reports name `vol02-quotes.json` (a scratch file of the previous session) as their list; its 277 entries are the lines the pattern matches.

### A3-02 — vol-02 lines `:1032`, `:949`, `:582`, `:1967`/`:865` against their copies (audit, 2026-10-09)

- **Copies.** ghOSt: `sources/S1-01/ghost.pdf`, SHA-256 `c37d636045a45e2216e7047ba1fb9ffa4ed88fe54b09ee0ccc33435cacd35c91`. EEVDF TR: `sources/S1-05/eevdf-tr-95.pdf`. ASA: `sources/V60/asa-arxiv25/2511.11628v1.pdf`.
- **Passages.**
  - ghOSt p. 589, §1: "…With amortization, these overheads allow just a single ghOSt agent to schedule over 2 million threads per second (Fig. 5)." — vol-02 `:1032` ends "…per second."
  - ghOSt p. 591, §3: "…such as per-NUMA-socket or per-AMD-CCX [40]. Enclaves also help in isolating faults, limiting the damage of an agent-crash to the enclave it belongs to (see §3.4)." — vol-02 `:949` ends "…per-AMD-CCX. Enclaves also help in isolating faults, limiting the damage of an agent-crash to the enclave it belongs to."
  - EEVDF TR p. 3, §1: "…a virtual eligible time and a virtual deadline which are the corresponding starting and finishing times…" — vol-02 `:582` "virtual dead line".
  - ASA p. 1, Abstract: "Modern operating system schedulers employ a single, static policy, which struggles to deliver optimal performance across the diverse and dynamic workloads of contemporary systems. This "one-policy-fits-all" approach leads to significant compromises in fairness, throughput, and latency, particularly with the rise of heterogeneous hardware…" — vol-02 `:1967` ends at "latency"; `:1965` "초록의 첫 문장입니다." ghOSt `:867` quotes the abstract's first two sentences under `:865` "논문의 초록 첫 문장입니다."
- **Coverage.** The four rows re-graded or re-described in D97.

### A3-03 — provenance of vol-02's copies (audit, 2026-10-09)

- **Checked.** `_dev/research/jioh/task-9.11-scheduler-constants/sources/S1-05/nngroup.html`: 121 941 bytes, `cd24ce28…43a8`, mtime 2026-10-07 18:26; the 9.11 record S1-05 (`search/S1-literature.md:143`) gives 120 613 bytes, `ee93bba7…ee83`, accessed 2026-09-24. `sources/S2-16/`: absent on this machine (S2-16, `search/S2-project-docs.md:272`). Fixed captures saved by the audit's vol-02 reader: `sources/nielsen-ue93/audit-2026-10-09/nngroup-wayback-20260924002157.html` (`e6a7eb4f…24f`), `sources/gamemode-docs/audit-2026-10-09/game-mode-portal-wayback-20260907131311.html` (`32938205…62c3`); text-extracted and searched: Nielsen's sentence and "Excerpt from Chapter 5" present; the Game Mode portal's "The Game Mode APIs are deprecated in Windows 10, version 1809 and later", "This capability is granted on a per-title basis" and "they may opt-out of CPU exclusivity by calling ReleaseExclusiveCpuSets" present. The 2026-09-13 verification's portal copy: `ea08757d…cc74`.
- **Re-hashed** (equal to V60's records): `sources/V60/ghost-sosp21/ghost-userspace/README.md` `ebac49bb…e14a` (clone HEAD `9ca0a1fb6ed88f0c4b0b40a5a35502938efa567f`); `sources/V60/gamemode-docs/releaseexclusivecpusets.html` `77de8a94…5618`; `_dev/research/jioh/2026-09-13-verification/sources/rt-app/README.in` `a35dec35…ad93` (clone HEAD `d6f8be41107642fd6ab41bc1ab3bb01a486fd00e`); `sources/V60/schedcp-mlsys25/eprint-v1.bin` `df54a986…f791`, `-v2` `3421050c…d327`, `-v3` `3a1a1aaf…5939`, `-v4` `289b0d4a…ca46`; `sources/V60/nielsen-ue93/nngroup.html` `075f609c…7fe3`; `sources/V60/gamemode-docs/game-mode-portal.html` `d18e2969…3fbd`. `sections/evaluation.tex:13` in the v1 and v2 extractions: `% \item \textbf{RQ5}: How effectively can \sys understand workloads?`.
- **Coverage.** D53's provenance sentence; the registry's `ghost-sosp21` (paper only), `rt-app` (cites `doc/tutorial.txt`, `src/rt-app.c`).

### A3-04 — 9.10's hand-offs to 9.12 (audit, 2026-10-09)

- **Read.** `_dev/research/jioh/task-9.10-scenarios-timelines/changelog.md` — D12 `:245` ("Hands to 9.12 and 9.15: the wording rule of 9.6 D32 restated on the new run; the scenario catalog's S12 row."); D34 `:739–741`; D90 `:1584`; D100 `:1815–1818`; D111 `:2033–2036`; D125 `:2310–2313`; D169 `:2990`; D170 `:3003`. `_dev/research/jioh/task-9.7-background-io/changelog.md:93` (9.7 D17 (a) `interbench`, (b) `ananicy-rules`).
- **Grep** (`git show 60149db:<file> | grep -c -i`, and the working tree at `a7ad2f29`) over `docs/related-work.md`, `docs/research-proposal.md`, `docs/research-claims.md`, `docs/background-guide.md`: `cpu-batch`, `handbrake`, `ffmpeg`, `kdenlive`, `deja\|déjà`, `borg`, `file-backup`, `S7\b\|S8\b\|S12\b\|S15\b`, `huge.page\|hugepage\|THP`, `H\.264` — 0 in each. `grep -rn -i "H\.265\|hevc\|x265" docs dataset/README.md` — no line.
- **Coverage.** Each 9.10 hand-off's subject in the owned prose: none named.

### A3-05 — leaving and references-only entries, where cited (audit, 2026-10-09)

- **Grep** (each id, and the author or product name: `procyon`, `dkms`, `dubroy`, `chang et`, `test pilot\|testpilot`, `czerwinski`, `gloria mark\|mark et al`, `gallup`, `videogui`) over the four owned files at `60149db` and `a7ad2f29`: 0 everywhere. Across `docs/` (excluding `docs/references.md` and `docs/memos/`): `procyon` — vol-02 `:3449`, `:3897` (and the ch. 8.4 prose at `:3421`, "모음에 들어 있는 것이 아홉 개"), `docs/workload/scenario-catalog.md:23`, `:33`, `source-vetting.md:42`, `:93`, `:114`, `grounding-sources.md:16`; `dkms-man`, `dkms-debian` — `scenario-catalog.md:22`; `dubroy-chi10`, `chang-chi21` — vol-06 `:1162`, `:2519`, `:3954`, `:3956`, `building-plan.md:82`, `:189`, `archetype-plan.md:40`; `mozilla-testpilot10` — vol-06 `:1180`, `:2519`, `:3955`, `measurement-overview.md:162`, `building-plan.md:82`, `:189`, `archetype-plan.md:40`; `mark-gallup06` — `source-vetting.md:76`, `building-plan.md:136`; `czerwinski-chi04`, `mark-chi08`, `mark-chi14`, `videogui-arxiv24` — none.
- **Coverage.** 9.10 D34's and D169's question to 9.12.

### A3-06 — citation coordinates: Li, Ding & Shen; Tam et al.; Atil et al.; SchedCP's journal-ref (audit, 2026-10-09)

- **Copies.** Crossref `works/10.1145/1281700.1281702` → `sources/S1-21/audit-2026-10-09/crossref-1281700.1281702.json` (`83081c17…fdc8`; saved by the audit's scholarly reader). Crossref bibliographic queries and `works/<doi>` for 10.18653/v1/2024.emnlp-industry.91 (`6b87fa0c…bc32`) and 10.18653/v1/2025.eval4nlp-1.12 (`0a6d98a0…ca31`), saved in `sources/audit-2026-10-09/F4/`. ACL Anthology PDFs: https://aclanthology.org/2024.emnlp-industry.91.pdf → `sources/S1-27/audit-2026-10-09/2024.emnlp-industry.91.pdf` (19 pp., `c8145f4d…6e`); https://aclanthology.org/2025.eval4nlp-1.12.pdf → `sources/S1-25/audit-2026-10-09/2025.eval4nlp-1.12.pdf` (14 pp., `d94638d0…c5`). `sources/V60/schedcp-mlsys25/abs.html` (`jref">MLforSystem 2025`).
- **Passages.** Crossref: Li — title "Quantifying the cost of context switch", container "Proceedings of the 2007 workshop on Experimental computer science", event "ExpCS07: Workshop on Experimental Computer Science", page "2", issued 2007-06-13. Tam — title "Let Me Speak Freely? A Study On The Impact Of Format Restrictions On Large Language Model Performance.", container "Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing: Industry Track", pages 1218–1236. Atil — title "Non-Determinism of "Deterministic" LLM System Settings in Hosted Environments", container "Proceedings of the 5th Workshop on Evaluation and Comparison of NLP Systems", pages 135–148. Tam PDF p. 7 (printed 1224): "Format restrictions, particularly constrained decoding (JSON-mode), can hinder reasoning abilities while enhancing classification task accuracy."; p. 4 (1221): "…placed the "answer" key before the "reason" key, resulting in zero-shot direct answering instead of zero-shot chain-of-thought reasoning."; p. 1 (1218): "Surprisingly, we observe a significant decline in LLMs' reasoning abilities under format restrictions." Atil PDF p. 1 (135): "We apply five API-based LLMs configured to be deterministic to eight diverse tasks across 10 runs. Experiments reveal accuracy variations of up to 15% across runs, with a gap of up to 70% between best possible performance and worst possible performance."; p. 4 (138): "We set temperature at 0, top-p at 1, and we fix the seed."; p. 6 (140): "We find that all models are more stable when they generate shorter responses."
- **Coverage.** The citation forms of D32/D50 (Li), D40 (Tam), D52 (Atil), `schedcp-mlsys25`'s cite line. Not checked here: Wei et al.'s and Sprague et al.'s venues (on their copies, S1-26, S1-28), Cooper et al.

### A3-07 — ananicy-cpp's process name and rule lookup at `v1.2.0` (audit, 2026-10-09)

- **Copies.** `_dev/research/jioh/2026-09-13-verification/sources/ananicy-cpp` (clone, HEAD `3554447c`, tags `v1.0.1`–`v1.2.0`; `v1.2.0` → `cf5ac2eb7b9660794f26f274975066f33359c63e`, 2026-03-26), read with `git show v1.2.0:<path>`; `git diff v1.2.0 HEAD` on `process.cpp` adds one `#include <unistd.h>`, on `rules.cpp`, `worker.cpp`, `process_info.cpp` nothing. Arch's PKGBUILD, https://gitlab.archlinux.org/archlinux/packaging/packages/ananicy-cpp/-/raw/main/PKGBUILD → `sources/S2-31/audit-2026-10-09/arch-ananicy-cpp-PKGBUILD` (`1240eabb99c04971d7333d0c7cedbd81c205d73231610d1c5510178d3825425a`). The CachyOS ISO's pacman record `sources/S2-46/airootfs/var/lib/pacman/local/ananicy-cpp-1.2.0-1/desc` (S2-46's extract).
- **Passages** (at `v1.2.0`). `src/platform/linux/process.cpp:193` `std::string get_command_from_pid(pid_t pid) {`; `:197` `// Cmdline method`; `:201` `auto exe_name_begin = cmdline[0].find_last_of('/');`; `:217` `// Exe method` (`read_symlink` of `/proc/{}/exe`, `filename()`); `:250` `// Comm method` (`/proc/{}/comm`); `:61–64` `if (command.ends_with(".exe")) { … command = cmd_path.filename().string();`. `src/platform/linux/process_helpers.hpp:10–24` (`/proc/{}/cmdline` split on NUL). `src/rules.cpp:184` `if (m_program_rules.contains(name)) {`; `:186` `#ifdef ENABLE_REGEX_SUPPORT` … `is_str_matching_regex(name, regex_rule.second)`; `:74–77` `name_regex`. `src/worker.cpp:80` `const auto &rule = rules->get_rule(p.name);`. `src/platform/linux/priority.cpp:41` `bool set_priority(pid_t pid, std::int32_t nice_value) {`, `:43` `/proc/{}/task`, `:50` `setpriority(PRIO_PROCESS, static_cast<id_t>(tid), nice_value);`. `cmake/StandardProjectSettings.cmake:40` `option(ENABLE_REGEX_SUPPORT "Build regex support" OFF)`. PKGBUILD: `pkgver=1.2.0`, `pkgrel=1`, `source=("git+https://gitlab.com/ananicy-cpp/ananicy-cpp.git#tag=v${pkgver}")`, `-DUSE_BPF_PROC_IMPL=ON`, `-DENABLE_REGEX_SUPPORT=ON`. Pacman record: `%VERSION%` `1.2.0-1`, `%PACKAGER%` `Peter Jung <ptr1337@archlinux.org>`, `%BUILDDATE%` 1774596461 (2026-03-27), `%DEPENDS%` includes `libbpf`, `pcre2`. `grep -rh --include='*.rules' name_regex` over `sources/S3-19/ananicy-rules` at `03ef03fb`: 0.
- **Coverage.** D6's open "how ananicy-cpp compares a rule's `name`". Whether CachyOS rebuilds the package itself rather than taking Arch's is not read; the installed package's packager and dependencies match Arch's build.

### A3-08 — four pointers (audit, 2026-10-09)

- **Checked** (`git show 60149db:<file> | sed -n <n>p`). `docs/research-proposal.md:312–313` "The Steam process is downloading, which / the user started deliberately, so it should be throttled"; `:315` blank. `:178` blank; `:179` "Discord appears in five of these and means something different each time. Chrome the same. Rows 3 and 4 are the sharpest pair in the table: same process count, same behavioural signature, opposite cor[rect policy]…". `docs/related-work.md:16` sentence 1 "Where situational awareness exists in deployed schedulers today, it is inferred from runtime behavior.", sentence 2 "Classic interactivity heuristics — …"; `:24` sentence 1 "A second lineage replaces hand-written heuristics with learned policies.", sentence 2 "Decima learns cluster scheduling policies via RL over job DAGs [decima]; …". Changelog D15 `:266` (`:178`), D18 `:307`, D19 `:319`; `scope-card.md:15`, `:71` (item 34), `:104`, `:124` (item 67).
- **Coverage.** The locators of D101.

### A3-09 — S3-19 recounted on ananicy-cpp's key (audit, 2026-10-09)

- **Read.** ananicy-cpp at `v1.2.0` (`cf5ac2eb`; clone `SCR/G-argv0/dl/ananicy-cpp-v1.2.0`): `src/platform/linux/process_helpers.hpp:10–25`, `src/platform/linux/process.cpp:61–65`, `:199–207`, `ananicy_cpp.bpf.c:76–102`, `cmake/StandardProjectSettings.cmake:36`; Arch's PKGBUILD line 50 (`sources/S2-31/audit-2026-10-09/arch-ananicy-cpp-PKGBUILD`). The catalogue `sources/S3-19/ananicy-rules` at `03ef03fb`.
- **Evidence per name** (the process's `argv[0]`): snapshots, session census files and exec captures under `~/.cache/meas-loop` — e.g. Chrome's browser `"cmd": "/usr/bin/google-chrome --no-sandbox …"` (`batch-9.8/r1/chrome-hidden/snap.steady.after.json`), the census's `@dbus-daemon --system` and `/usr/bin/dbus-daemon --session`; Ubuntu noble's package files for wrappers and interpreters (`7z`, `baloo_file`, `dkms`, `unattended-upgrade`; `sources/S3-19/audit-2026-10-09/debs/`, `extract/`; SHA-256 7zip `0f79450d…`, baloo-kf5 `008698bd…`, dkms `18d098c6…`, unattended-upgrades `13c576c7…`); Proton's and upstream Wine's loader for the game chain (`sources/S3-19/audit-2026-10-09/wine/`, commits in `HEAD-sha.txt`); Chromium's `set_process_title_linux.cc:105–137` for its children's titles. The per-name table: `SCR/G-argv0/table.md`.
- **Count.** `python3 -I SCR/G-argv0/perfile.py dataset/build/coreset-single` (re-run 2026-10-09): `distinct 35 strict 19 lenient 20 old 14`; files whole — old 7 `['c1-browsing', 'c1-dev', 'c1-media', 'c1-meeting', 'c1-photo', 'c6-fold', 'c6-spoof']`, strict 7 `['c1-dev', 'c1-gaming', 'c1-media', 'c1-photo', 'c2-p2a', 'c4-gaming', 'c7-compile']` ("lenient" counts the session bus).
- **Coverage.** D6's count; D105's name mapping.

## A4 — `docs/related-work.md` sentences no item carried

### A4-01 — SchedCP v4 and v2: the hot-path statement and the semantic gap (T5; 9.12 audit, 2026-10-09)

- **Citation.** As S1-12: Zheng, Hu, Zhang, Quinn, "Towards Agentic OS: An LLM Agent Framework for Linux Schedulers", arXiv:2509.01245, v4 (30 Sep 2025) and v2 (3 Sep 2025).
- **Copies read.** v4: `sources/S1-34/schedcp-v4.pdf`, SHA-256 `cce49d3c0ff5466cafc3b921373f6d43df2adcb97e38b40c9d45e3b21206e97c` (equal to S1-12's v4). v2: https://arxiv.org/pdf/2509.01245v2 → `sources/S1-12/audit-2026-10-09/agenticos-2509.01245v2.pdf`, SHA-256 `7dbfe839cbfa3937db68b4654b8dec82c6b6d1d20e25736848729ef7fe25c378` (equal to S1-12's v2). 2026-10-09. Text by `pdftotext -layout`.
- **Passages.**
  - v4 Abstract, p. 1: "Operating system schedulers suffer from a fundamental semantic gap, where kernel policies fail to understand application-specific needs, leading to suboptimal performance."
  - v4 Abstract, p. 1: "architect a decoupled control plane that separates the AI's role of semantic reasoning ("what to optimize") from the system's role of execution ("how to observe and act")".
  - v4 §2, PDF p. 2: "LLMs uniquely bridge these gaps by: … (4) operating in the control plane to generate optimized code that runs natively with negligible runtime overhead, unlike traditional ML models that would cause unacceptable inference latency in the scheduler hot path."
  - v2 §3.1: "LLMs generate and optimize scheduling policies offline, producing native eBPF code that executes without any ML inference overhead during actual scheduling decisions."
- **Coverage.** The semantic-gap framing (v4 Abstract) and the hot-path statement at v4's locator (§2, p. 2), which S1-12 recorded only at v2.

### A4-02 — TuxBot v2: out of band, and "lack of semantic understanding" (T5; 9.12 audit, 2026-10-09)

- **Copy read.** `sources/S1-17/audit-2026-10-09/tuxbot-2605.15026v2.pdf`, SHA-256 `543bd4fcc48785e2762de4a098f3feb2dd72f7732b21f514d178de2233a90760` (equal to S1-17; re-downloaded 2026-10-09 by the audit's source-fidelity strand).
- **Passages.**
  - Abstract, p. 1: "TuxBot turns knob schemas, telemetry, current configuration, recent action–response history, and retrieved prior runs into a compact decision context."
  - §1, p. 1: "We study tuners that operate out of band: they are not inline on each request, and they are not kernel fast-path controllers such as the CPU scheduler, a packet scheduler, or a TCP congestion controller [16, 30, 36, 56]."
  - §1, p. 1: "Lack of semantic understanding: We show that these approaches are not sufficient for the online tuning of a live application's OS environment because of three recurring failures. First, a tuner can make semantically unsound changes …"
- **Coverage.** What TuxBot reads; its out-of-band stance; its semantic framing of prior tuners.

### A4-03 — Vulcan v3: neural inference kept out of the hot path (T5; 9.12 audit, 2026-10-09)

- **Copy read.** `sources/S1-18/audit-2026-10-09/vulcan-2512.25065v3.pdf`, SHA-256 `ed85ead607bee6409a2d1fa0389063d0d513f09a718c53317affe028ca16fed6` (equal to S1-18).
- **Passages.**
  - §9 "Related Work", "Traditional learning-based policies", PDF p. 14: "neural approaches introduce significant practical challenges: opaque behavior that complicates debugging [62], complex training and deployment pipelines [3, 27], inference overheads in the control path [27, 110], and safety concerns that limit adoption [83]. Vulcan takes a different stance: it avoids neural inference in the hot path entirely, confining learning to an offline search over small, interpretable LLM-generated code snippets."
- **Coverage.** Vulcan's hot-path stance. A search for "semantic gap" finds none.

### A4-04 — AKTS v2: inference off the scheduling path; recognize a regime and switch policies (T5; 9.12 audit, 2026-10-09)

- **Copy read.** `sources/S1-32/akts-2609.12276v2.pdf`, SHA-256 `dfc179fc2395b41a6f13e606ea033bb7e61a1272d82faa89e0f794a1dc3239fe` (equal to S1-32).
- **Passages.**
  - §1, p. 1: "On a GPU-backed LLM serving node the CPUs still handle request intake, tokenization, prefill orchestration and background jobs."
  - §1, p. 1: "AKTS targets this problem: recognize the regime at a coarse timescale and switch kernel scheduling behavior to match."
  - §1, p. 1: "Schedulers place tasks every few microseconds while even small models need milliseconds per decision, so inference on the scheduling path is ruled out by construction."
  - §1, p. 1: "the missing piece is the actuator, a safe, sub-microsecond mechanism letting a slow agent switch among verified kernel policies."
  - §1, p. 1, beside them: "LumOS [6] has an LLM agent tune Completely Fair Scheduler hyperparameters, outperforming Bayesian optimization by 5–7% and a human expert by 2.98%."
- **Coverage.** AKTS's setting (a serving node), its output (a switch among verified policies), its hot-path stance.

### A4-05 — Jadhav et al. v2: the LLM is the scheduler (T5; 9.12 audit, 2026-10-09)

- **Copy read.** https://arxiv.org/pdf/2506.02025v2 → `sources/S1-15/audit-2026-10-09/2506.02025v2.pdf`, SHA-256 `f6fd740b58046ea3b2bb742707d026f8dd7bc2eb3683a83186e545f7a9ca440f` (equal to S1-15). 2026-10-09.
- **Passages.**
  - Abstract, p. 1: "we propose a novel Large Language Model (LLM)-based scheduler using a ReAct-style framework (Reason + Act), enabling iterative, interpretable decision-making."
  - Abstract, p. 1: "However, a trade-off between reasoning quality and computational overhead challenges real-time deployment."
  - §3.7.3, PDF p. 9: "The wall-clock times required (up to an hour for 100 jobs) indicate that, at the moment, LLM-based scheduling is not suitable for real-time job submission scenarios. However, it may be practical for batch scheduling systems, periodic resource optimization, or strategic scheduling decisions where quality is prioritized over immediate response."
- **Coverage.** The LLM making the scheduling decisions; no semantic-gap framing (no "semantic" in the text).

### A4-06 — TuneAgent v2: the configuration is rebuilt and deployed before it runs (T5; 9.12 audit, 2026-10-09)

- **Copy read.** https://arxiv.org/pdf/2508.12551v2 → `sources/S1-14/audit-2026-10-09/osr1-2508.12551v2.pdf`, SHA-256 `90ed2128c1832671fb19c3947191ac2baa1da0f97b431481280cbaa2ba75f413` (equal to S1-14). 2026-10-09.
- **Passages.**
  - §1, PDF p. 2: "Unlike lightweight parameter tuning, kernel tuning requires rebuilding, deploying, and benchmarking the system to observe performance changes."
  - Evaluation, metrics: Nginx, Redis Benchmark, Sysbench for PostgreSQL.
- **Coverage.** Where TuneAgent's LLM output takes effect; its evaluation applications. No hot-path statement; no semantic-gap framing.

### A4-07 — Kgent: the problem it addresses (T5; 9.12 audit, 2026-10-09)

- **Copy read.** `sources/S1-33/kgent-escholarship.pdf`, SHA-256 `1292f7508075a393ea431777dd3458d30fa6a2a3de2428ec813061693bebf754` (equal to S1-33).
- **Passages.** Abstract, p. 1: "This paper presents Kgent, an alternative framework that alleviates the difficulty of writing an eBPF program by allowing Kernel Extensions to be written in Natural language."
- **Coverage.** Kgent's problem. A search for "semantic gap", "hot path", "fast path", "inference latency" finds none.

### A4-08 — Decima, FIRM, Park: state, action and the platform (T4; 9.12 audit, 2026-10-09)

- **Copies read.** The audit's re-downloads, each equal to its record:
  - `sources/S1-06/audit-2026-10-09/decima.pdf`, `b6b50a58ea743049f9bf7d92d2941afff1e4308b40ed208fc348fae8b57904d3`
  - `sources/S1-07/audit-2026-10-09/firm.pdf`, `a0adcf9865358b5f10fc99b2fe4257ffb3eea3137d4c9ec72d6d91c2c9d46c68`
  - `sources/S1-08/audit-2026-10-09/park.pdf`, `c686bc445a7e97e36f342cf1234bc0ca1a9100056a16e6a9e362350ed7045f98`
- **Passages.**
  - Decima, Fig. 4 caption, PDF p. 4: "In Decima's RL framework, a scheduling agent observes the cluster state to decide a scheduling action on the cluster environment, and receives a reward based on a high-level objective. The agent uses a graph neural network to turn job DAGs into vectors for the policy network, which outputs actions."
  - Decima §6.1, PDF p. 8: "Mapping the cluster state to a scheduling decision takes less than 15ms (Figure 15b)."
  - FIRM, RL primer, PDF p. 8: "the agent observes a state of the environment st ∈ S, and performs an action at ∈ A based on its policy πθ (s) (parameterized by θ), which maps state space S to action space A."
  - FIRM, Table 3, PDF p. 10: "State (st) SLO Maintenance Ratio (SMt), Workload Changes (WCt), Request Composition (RCt), Resource Utilization (RUt); Action Space (at) Resource Limits RLTi (t), i ∈ {CPU, Mem, LLC, IO, Net}".
  - Park §1, PDF p. 2: "We present Park, an open, extensible platform that presents a common RL interface to connect to a suite of 12 computer system environments (§4)." … "For each environment, Park defines the MDP formulation, e.g., events that triggers an MDP step, the state and action spaces and the reward function."
- **Coverage.** What each learns or provides, as a state-to-action mapping.

### A4-09 — Microsoft Learn, "Priority Boosts": foreground and input boosts (T7; 9.12 audit, 2026-10-09)

- **Copy read.** `sources/S2-54/win-priority-boosts.html`, SHA-256 `8cc60b3684eee8f1ad7cd7a88de825bc4e879cebe0784062f1c103e81ef68da4` (equal to S2-54; `ms.date` 2025-07-14).
- **Passages.**
  - "When a process that uses NORMAL_PRIORITY_CLASS is brought to the foreground, the scheduler boosts the priority class of the process associated with the foreground window, so that it is greater than or equal to the priority class of any background processes."
  - "The priority class returns to its original setting when the process is no longer in the foreground."
  - "When a window receives input, such as timer messages, mouse messages, or keyboard input, the scheduler boosts the priority of the thread that owns the window."
  - "For example, when a wait operation associated with disk or keyboard I/O finishes, the thread receives a priority boost."
- **Coverage.** The Windows scheduler acting on window state and on I/O completion.

### A4-10 — Microsoft Learn, Game Mode portal: the foreground condition (T6; 9.12 audit, 2026-10-09)

- **Copies read.** The Internet Archive capture of 2026-09-07 → `sources/gamemode-docs/audit-2026-10-09/game-mode-portal-wayback-20260907131311.html`, SHA-256 `329382052bc020258a9d3a616134c0137167cacec00ceb61df1d0d9638df62c3` (saved by the audit's guidebook-quotation strand); the 2026-09-13 verification copy, `_dev/research/jioh/2026-09-13-verification/sources/gamemode-docs/game-mode-portal.html`, SHA-256 `ea08757d68e15e1ea6ed66f3706646b3a06c366c2673c9213ac2548e9cf1cc74`. S2-16's own copy (`20bb5394…`) is not on disk.
- **Passages.** "The app must be in the foreground and have focus before exclusive resources are granted."
- **Coverage.** Windows Game Mode's foreground condition.

### A4-11 — Apple Support, "Use Game Mode", re-downloaded (T6; 9.12 audit, 2026-10-09)

- **Copy read.** https://support.apple.com/en-us/105118 → `sources/S2-18/audit-2026-10-09/apple-gamemode.html`, SHA-256 `10857702fd6e6ebdf41c7ee87c0e429f5ae4424eb9d9ab60df0a61fb36c95336` (equal to S2-18). 2026-10-09.
- **Passages.** "When your game enters full screen, Game Mode automatically turns on for that game."; "Game Mode optimizes your gaming experience by giving your game the highest priority access to your CPU and GPU, lowering usage for background tasks."
- **Coverage.** macOS Game Mode's full-screen trigger.

### A4-12 — sched(7), Apple's `QualityOfService`, XNU's buckets: declared classes (T7; 9.12 audit, 2026-10-09)

- **Copies read.** Each equal to its record:
  - `sources/S2-51/sched.7.html`, SHA-256 `3b52e0157557b7854f013eb13cee0ecdeacddc7f5f27c9e155dbbddc85786814` (S2-51; man-pages 6.19)
  - `sources/S2-53/qualityofservice.json`, `fcc979e02d151be8bd6427e1955c1911ade2be6a3fcc0a4547dbbc0039c148f2` (S2-53)
  - `sources/S2-54/sched_clutch_edge.md`, `5f4201d269593c0a7d39e347ccf7241fc43f88073db3be54339e19d7bd51532c` (S2-54, `xnu-12377.121.6`)
- **Passages.**
  - sched(7): "The nice value is an attribute that can be used to influence the CPU scheduler to favor or disfavor a process in scheduling decisions."; "The nice value can be modified using nice(2), setpriority(2), or sched_setattr(2)."
  - `QualityOfService`, abstract: "Constants that indicate the nature and importance of work to the system."
  - `sched_clutch_edge.md:24`: "These scheduling buckets roughly map to the QoS classes used by the OS runtime to define performance expectations for various pieces of work."
- **Coverage.** Linux and macOS scheduling acting on declared attributes.

### A4-13 — the simulator's one lane (project document; 9.12 audit, 2026-10-09)

- **Copy read.** `docs/simulator/simulator-guide.md` at `a7ad2f29` (unchanged since `60149db`).
- **Passages.** `:44`: "**One lane.** Exactly one simulated CPU. The scheduler answers one question: *who holds the lane until the next event*."
- **Coverage.** What the simulated executor is.

## A5 — the proposal's and the other owned docs' sentences no item carried

### A5-01 — `ananicy-rules` at `03ef03fb`: the Family 3 rows' programs

- Copy read: the S3-19 clone, `sources/S3-19/ananicy-rules`, HEAD `03ef03fbf7e834385377432ccecaedd32e3414bb` (2026-09-08), working tree clean; read 2026-10-09.
- SHA-256: `00-default/Creative/blender.rules` `dc6492c3…`; `00-default/Creative/davinci.rules` `a4e7c611…`; `00-default/Chats/chats.rules` `437a5422…`; `00-default/Development & Programming/node.rules` `02183cfd…`; `00-default/Games/linux-native/linux-native_g.rules` `b857d104…`; `00-default/Tools/podman.rules` `1ed0297f…`; `00-types.types` `667d89cb…`.
- Method: `grep -rn --include='*.rules' '"name": *"<name>'` over `00-default` for each name below, and a case-insensitive grep for `godot`, `kube`, `docker`, `podman`, `containerd`, `postgres`, `mysql`, `maria`, `redis`, `mongo`, `k3s`, `minikube`, `etcd`.
- Passages:
  - `Chats/chats.rules:17–18`: `{ "name": "Discord", "type": "Chat" }`, `{ "name": "discord", "type": "Chat" }`.
  - `Games/linux-native/linux-native_g.rules:90–91`: `{ "name": "godot.x11.opt.tools.64", "type": "Game" }`, `{ "name": "godot.x11.opt.tools.32", "type": "Game" }`; `Games/linux-native/common.rules:524`: `{ "name": "GodotWorkshopUtility.x86_64", "type": "BG_CPUIO" }`.
  - `Creative/blender.rules:2`: `{ "name": "blender", "type": "Heavy_CPU" }`; `Creative/davinci.rules:2`: `{ "name": "resolve", "type": "Heavy_CPU" }`.
  - `Development & Programming/node.rules:2`: `{ "name": "node", "type": "BG_CPUIO" }`; `Tools/podman.rules:2`: `{ "name": "podman", "type": "Service" }`; `Development & Programming/mysql-workbench.rules:2–3` and `mongodb_compass.rules:2` (client tools, `BG_CPUIO`).
  - No entry: `kubelet`, `kube-apiserver`, `k3s`, `k3d`, `kind`, `minikube`, `containerd`, `dockerd`, `docker`, `etcd`, `postgres`, `mysqld`, `mariadbd`, `redis-server`, `mongod`, `npm`, `vite`, `webpack`, `python`, `uvicorn`, `gunicorn`, `davinci`.
  - `00-types.types`: `:4` `Game` nice −5, best-effort, normal; `:22` `BG_CPUIO` nice 16, idle I/O, `sched` idle; `:33` `Heavy_CPU` nice 9, best-effort, ionice 7; `:36` `Chat` nice −3, best-effort, ionice 7; `:39` `Service` nice 10, best-effort, ionice 6.
- Coverage: the proposal's Family 3 rows `:636–638` and `docs/research-claims.md:75`.

### A5-02 — Linux kernel, `Documentation/scheduler/sched-design-CFS.rst` (mainline `7b63ef2d`), re-read

- Copy: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/scheduler/sched-design-CFS.rst?id=7b63ef2d55f24519e7e9e5f4d15dbea03f126e40 · 2026-10-09 · `sources/S2-04/audit-2026-10-09/sched-design-CFS-7b63ef2d.rst` · SHA-256 `25a5fa2bf66e2a076aaac1492f306bd6c92d1c5b399976831e637c30072e76b7`, equal to S2-04's.
- Passages: `:11–14` "CFS stands for "Completely Fair Scheduler," and is the "desktop" process scheduler implemented by Ingo Molnar and merged in Linux 2.6.23. When originally merged, it was the replacement for the previous vanilla scheduler's SCHED_OTHER interactivity code."; `:18–19` "80% of CFS's design can be summed up in a single sentence: CFS basically models an "ideal, precise multi-tasking CPU" on real hardware."; `:26–27` "On real hardware, we can run only a single task at once, so we have to introduce the concept of "virtual runtime.""; `:45–47` "CFS's task picking logic is based on this p->se.vruntime value and it is thus very simple: it always tries to run the task with the smallest p->se.vruntime value (i.e., the task which executed least so far)."; `:51–53` "Most of the rest of CFS's design just falls out of this really simple concept, with a few add-on embellishments like nice levels, multiprocessing and various algorithm variants to recognize sleepers."; `:96–98` "Thus the CFS scheduler has no notion of "timeslices" in the way the previous scheduler had, and has no heuristics whatsoever."
- Coverage: `docs/research-proposal.md:79`, `:89`.

### A5-03 — Linux kernel, `Documentation/scheduler/sched-eevdf.rst` (mainline `7b63ef2d`), re-read

- Copy: the audit's re-download, `sources/S2-03/audit-2026-10-09/sched-eevdf-7b63ef2d.rst` · SHA-256 `75b99048d738b7683d06c5844e150253e91d75ec46e774f7a96cf0e9d39056a0`, equal to S2-03's.
- Passages: `:13–14` "Similarly to CFS, EEVDF aims to distribute CPU time equally among all runnable tasks with the same priority."; `:18–20` "EEVDF picks tasks with lag greater or equal to zero and calculates a virtual deadline (VD) for each, selecting the task with the earliest VD to execute next."; `:30–32` "tasks can request specific time slices using the new sched_setattr() system call, which further facilitates the job of latency-sensitive applications."
- Coverage: `docs/research-proposal.md:89`.

### A5-04 — OSTEP ch. 8, "Scheduling: The Multi-Level Feedback Queue" (Version 1.10), re-read

- Copy: `sources/S1-02/audit-2026-10-09/cpu-sched-mlfq.pdf` · SHA-256 `96241b4e6708991740560334a1f67516c3c68eb3e6a570af7b03cdb4b32918db`, equal to S1-02's; read with `pdftotext -layout`, pages by the running head.
- Passages: p. 3 "Rule 4a: If a job uses up its allotment while running, its priority is reduced (i.e., it moves down one queue)." / "Rule 4b: If a job gives up the CPU (for example, by performing an I/O operation) before the allotment is up, it stays at the same priority level (i.e., its allotment is reset)."; p. 6 (§8.3) "Rule 5: After some time period S, move all the jobs in the system to the topmost queue." / "First, processes are guaranteed not to starve"; p. 8 (§8.4) "Without any protection from gaming, a process can issue an I/O before its allotment ends, thus staying at the same priority level, and dominating CPU time." / "We thus rewrite Rules 4a and 4b to the following single rule: • Rule 4: Once a job uses up its time allotment at a given level (regardless of how many times it has given up the CPU), its priority is reduced (i.e., it moves down one queue)."
- Coverage: `docs/research-proposal.md:119–121`; `docs/background-guide.md:111–113`, `:203`.

### A5-05 — the project's simulator, MLFQ policy (`simulator/src/sim.cpp` at `a7ad2f29`)

- Copy: `git show a7ad2f29:simulator/src/sim.cpp` · SHA-256 `7d34002baad830b407497589793cbe4b72665377528677de2bd68e6a581ea1f7`; read 2026-10-09.
- Passages: `:173` "// The five textbook rules (simulator-guide §5), parameterised by Params."; `:199` "// rule 5: everyone back to the top queue" (`:203` clears every level and allotment); `:214` "if (why == Yield::SliceEnd) { // rule 3: burned the allotment → demote"; `:221` "} else { // rule 4: blocking keeps both level and allotment"; `:230` "i64 horizon(int id) override { return slice_of(slot(id).level) - slot(id).allot; }"; `:231` "void charge(int id, i64 ran) override { slot(id).allot += ran; }". `docs/recognition-vocabulary.md:113`: `boost_interval_us` 100000 (OSTEP Fig. 8.4).
- Coverage: `docs/research-proposal.md:119–121` (what the baseline implements).

### A5-06 — Apple, "Use Game Mode" and the `LSSupportsGameMode` / `LSApplicationCategoryType` keys, re-read

- Copies (2026-10-09): https://support.apple.com/en-us/105118 → `sources/S2-18/audit-2026-10-09/apple-gamemode.html` · SHA-256 `10857702fd6e6ebdf41c7ee87c0e429f5ae4424eb9d9ab60df0a61fb36c95336`, equal to S2-18's; https://developer.apple.com/tutorials/data/documentation/bundleresources/information-property-list/lssupportsgamemode.json → `sources/S2-20/audit-2026-10-09/lssupportsgamemode.json` · `a712464b1dd11aada283ec3991b77e6e39fe78cd486669a66b40a304653db04b`, equal to S2-20's; …/lsapplicationcategorytype.json → `sources/S2-20/audit-2026-10-09/lsapplicationcategorytype.json` (9 552 bytes, new).
- Passages: Support page — "Mac with Apple silicon and macOS Sonoma 14 or later and a game that supports macOS full-screen mode."; "When your game enters full screen, Game Mode automatically turns on for that game. Quitting the game automatically turns Game Mode off. You can also turn Game Mode off or on manually while your game is still in full screen." `LSSupportsGameMode` JSON — `metadata.platforms`: iOS `introducedAt` 18.6, iPadOS 18.6, macOS 26.0; abstract "A Boolean value indicating whether the app supports Game Mode."; "If you don't include this key in your Info.plist, Game Mode might not turn on for your game." `LSApplicationCategoryType` JSON — macOS `introducedAt` 10.0; lists `public.app-category.games` and nineteen game subcategories; no mention of Game Mode.
- Searched, not found: `developer.apple.com/tutorials/data/documentation/{games/game-mode, games/improving-performance-with-game-mode, metal/game-mode, gamekit/game-mode, games, xcode/game-mode}.json` → 404.
- Coverage: `docs/research-proposal.md:148` (the row's versions). How macOS 14 and 15 recognise a game: not found.

### A5-07 — Vulkan `VkPresentModeKHR` and GStreamer's base sink, re-read

- Copies (2026-10-09): https://raw.githubusercontent.com/KhronosGroup/Vulkan-Docs/e4e53e4b31e13eeaee1ad99fb940aa72b2ec1b14/chapters/VK_KHR_surface/wsi.adoc → `sources/vulkan/audit-2026-10-09/wsi.adoc` · SHA-256 `8883facb7d9f7c61ccb606a129835ef26e640ac043d97c4c5541a0ab439a8fbd` (431 017 bytes; the registry entry records no hash); https://gitlab.freedesktop.org/gstreamer/gstreamer/-/raw/83e7df9168dd73f5dcd1caa60195a9d9dce558b4/subprojects/gstreamer/libs/gst/base/gstbasesink.c → `sources/gstreamer/audit-2026-10-09/gstbasesink.c` · `43a7223ce9ab63dc0bae4868f0660d6bf3e4e3201cf883eaee21cac2addd14c7`, equal to the registry's.
- Passages: `wsi.adoc:4418–4426` "ename:VK_PRESENT_MODE_FIFO_KHR specifies that the presentation engine waits for the next vertical blanking period to update the current image. Tearing cannot: be observed. An internal queue is used to hold pending presentation requests. New requests are appended to the end of the queue, and one request is removed from the beginning of the queue and processed during each vertical blanking period in which the queue is non-empty. This is the only value of pname:presentMode that is required: to be supported."; `gstbasesink.c:118–124` "A buffer arrives too late in the sink when the presentation time (as a combination of the last segment, buffer timestamp and element base_time) plus the duration is before the current time of the clock. If the frame is later than max-lateness, the sink will drop the buffer without calling the render method."
- Coverage: `docs/research-proposal.md:414`, `:820`; `docs/background-guide.md:207`.

### A5-08 — Li, Ding & Shen, ExpCS '07, re-read

- Copy: the audit's re-download, `sources/S1-21/audit-2026-10-09/expcs2007.pdf` · SHA-256 `8b7a606976610acd6332c7cef6592d58380d49d611a696bf05d2ea122f0c71cf`, equal to S1-21's.
- Passages: p. 2 "context switch times ranging from 4.2µs to 8.7µs. This is because the entire dataset of our benchmark (including the two communicating processes and the simulation process) can fit into the L2 cache, and the context switch does not cause any visible cache interference."; p. 2 "Because the dataset of the simulation process fits in L2 cache but the combined dataset of the two communicating processes does not, the cost of context switch increases dramatically, from 38.6µs to 203.2µs, with the increment of array size."; p. 3 "When the access stride is 128B, the cost ranges between 133.8µs and 1496.1µs with the mean 825.3µs."
- Coverage: `docs/research-proposal.md:416`; `docs/background-guide.md:119`.

### A5-09 — the 9.9 session census: processes and threads on the dataset's machine

- Input: `~/.cache/meas-loop/pool/session-session-from16/` and `…-from25/`, `meas-session-session-r<N>-full/census.steady.start.json` for the 24 repeats `meas-ci:session:2026-09-24` adopted (`measurement-campaign-record.md:215`: 47–49, 51, 58, 60–63, 68, 69, 71–77, 79, 83, 85–88); written by `dataset/tools/meas/session/census.py` at `a7ad2f29` (SHA-256 `3370be40…`), `procs` read from `/proc`, kernel threads flagged by `PF_KTHREAD`. Repeat 47's file SHA-256 `3fd9a213ba33ad69dc3177857c15375f659a73516cd367b77c560a4490406233`.
- Script: `sources/A5-09/census_count.py` (SHA-256 `ce6c06c7ddd65a0a06908734b6f9724841555f72fff47a773a2d5f7c6c79531b`); output `sources/A5-09/census_count.out` (`224262ce3ee85b359cc50d14d9a30e47a161c27ab4eda1ae6908d0ef0df9a5e7`), verbatim:
  ```
  repeats 24 [47, 48, 49, 51, 58, 60, 61, 62, 63, 68, 69, 71, 72, 73, 74, 75, 76, 77, 79, 83, 85, 86, 87, 88]
  user processes 125-125
  user threads 501-505
  session processes 66-66
  session threads 319-321
  kernel threads 113-118
  ```
  "session" is the processes in the measured user's cgroup `/user.slice/user-<uid>`; "user" every process not a kernel thread, the runner's services (`Runner.Listener`, `Runner.Worker`, `dockerd`, `containerd`, `php-fpm8.3`, …) among them.
- Coverage: `docs/research-proposal.md:79`.

### A5-10 — the dataset's file indexer and chat client, as compiled

- Copy: `dataset/archetypes.yaml` at `a7ad2f29` (last changed `a157d47b`).
- Passages: `file-indexer` (`meas-ci:background:2026-10-02b`, repeats 1–18): `:1502` "saturation 0.655-0.676 over the job, 0.891-0.919 from the miner's Initializing; the dominant thread 0.556-0.559 of the CPU"; `:1503` "share of CPU past the 10 ms boot slice 0.844-0.849"; `:1504` "the initial sleep 14.40-15.23 s, carried as the task's arrival (9.10 D71)". `chat-client` (`meas-ci:desktop:2026-09-20`, 18 repeats): `:771` "idle wakes/s 11.9830–12.5600", "idle cpu-share 0.00088–0.00114".
- Coverage: `docs/research-proposal.md:129`.

### A5-11 — Shneiderman 1984, §5 "Response time: variability", re-read

- Copy: `../task-9.11-scheduler-constants/sources/S1-07/shneiderman.pdf` · SHA-256 `7ea65246d42600afcd94835ca8e42444ad49f376c38af26a12e1d6731851bd90`, equal to 9.11 S1-07's and the registry's `shneiderman-csur84`; read with `pdftotext -layout`, pages by the running head.
- Passages: §5.3, p. 282 "In summary, modest variations in response time (plus or minus 50 percent of the mean) appear to be tolerable and to have little impact on performance. As the variability grows, there may be some decrease in performance speed. Frustration may emerge only if delays are unusually long--at least twice the anticipated time."; §5.2, pp. 281–282: Goodman and Spence, "The mean response time was set at 1.0 second"; Butler [1983], "means of 2, 4, 8, 16, and 32 seconds"; "Of the three experiments that tested response time variability, two had significant effects, which indicated that subjects who had higher variability took longer to respond."
- Coverage: `docs/research-proposal.md:700`. `:953`'s "perceived as stutter": no source in the registry or the slice's reads (`grep -i 'stutter\|frame time\|judder\|frame pacing' docs/references.md`: none).
