# Read R01: interbench, rt-app, hackbench, schbench, stress-ng, kernel build

Read performed 2026-09-13. All paths below are relative to `_dev/research/jioh/2026-09-13-verification/sources/` unless absolute. Email addresses that appear in some source lines are replaced by `[…]` inside quotations (marked omission); nothing else is altered inside quotation marks.

## Copies used

| Source id | URL / commit / capture | Date of copy (commit date) | Local path | Hash (sha256) |
|---|---|---|---|---|
| interbench (master) | https://github.com/ckolivas/interbench.git, master = `e612a65ce941028ddea804e6b45ccde2750720d2` (verified equal to `git ls-remote` HEAD on 2026-09-13; clean tree). Reused existing clone. | commit 2016-10-24 09:23:02 +1100 | `interbench/` | per-file hashes in the rows below |
| — files at e612a65 | `interbench.c` | | `interbench/interbench.c` | a381b94085427cda4169466d3833c272fe4e9672cfbad74a64897621db7f2191 |
| | `interbench.8` | | `interbench/interbench.8` | 31bc88e508bb7f81cc01a4ef632fbee4f4acb908082140427acba11ca2ee92ee |
| | `readme` | | `interbench/readme` | a67f2b8b3d92896e63f2f03e25dc3f59077eb49192fa353d56cbe0da1f7c0b29 |
| | `hackbench.c` | | `interbench/hackbench.c` | 6b9b0fe030a3115da2c1f5c25db7a67a1f468a1d2458a0ffc9a20c5408c23fa0 |
| | `interbench.h` | | `interbench/interbench.h` | 1df9bf60b48e783a983f17a268f238147d161f4ee658cc3ea42d0b20a9f28f4b |
| interbench (tag) | tag `v0.31` → `58ea031247318caa2f25b5b2a92249baf4246447` (same clone; used via `git show v0.31:…` / `git diff v0.31 HEAD`) | 2016-10-21 | `interbench/` (git objects) | — |
| interbench packaging | Repology API `https://repology.org/api/v1/project/interbench`; AUR RPC `https://aur.archlinux.org/rpc/v5/info?arg[]=interbench`; FreeBSD ports `benchmarks/interbench/Makefile` (raw.githubusercontent freebsd-ports main, last path commit d4329229, 2024-01-12); Gentoo `app-benchmarks/interbench/interbench-0.31-r1.ebuild` (gentoo/gentoo master, last path commit 0336caee, 2022-02-09); GitHub API `repos/ckolivas/interbench` | fetched 2026-09-13 | `interbench-packaging/` | repology 5fe4c1ca…6f84b; aur e3ee0e6d…fcb31; freebsd 3e834f0e…48fa; gentoo 10304d45…cd48 |
| rt-app | https://github.com/scheduler-tools/rt-app.git, master `d6f8be41107642fd6ab41bc1ab3bb01a486fd00e` | 2026-06-10 16:27:24 +0200 | `rt-app/` | tutorial.txt a3e8823ebae6fda9893327637a48ab195f98206b00ad857a8cc736414d9ee3e7; template.json 600aa1d6c65e0eefa3f0d262b4a00fa0d57702deca7796f520d43da2a4d648b3 |
| rt-tests (hackbench) | https://git.kernel.org/pub/scm/utils/rt-tests/rt-tests.git, HEAD `fd45df830803dd7f26d2ca8bdcf05fd7e0d62ae8` (matches entry's `fd45df83`) | 2026-08-31 12:37:09 -0400 | `rt-tests/` | hackbench.c 36e5b4c86aee10fa7422e16c2a3cb218e7b040a364fe52f943ad8d68b167ac3e; hackbench.8 84fe7408e1d820ee88a4114fbeb60cef600ebc70f07d27814030d728e091f3fc |
| Linux kernel (HEAD) | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git depth-1 clone, HEAD `2f0c1cf72f4682178506f513bbf015e591b1aa4a`; sparse checkout Documentation, init, tools/perf/bench, tools/perf/Documentation, kernel/sched, include/linux | 2026-09-12 16:22:25 -0700 | `linux-docs/` | — (git objects) |
| Linux kernel v6.6 | tag v6.6 → `ffc253263a1375a65fa6c9f62a893e9767fbebfa`, fetched depth 1 into same repo; `git grep` over the whole tree | 2023-10-30 | `linux-docs/` (git objects) | — |
| Linux older docs | `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/<file>?h=<tag>` for sched-design-CFS and sysctl kernel docs at v2.6.23, v2.6.32, v3.0, v4.19, v5.4, v6.6; `kernel/sched/fair.c?h=v6.5` | fetched 2026-09-13 | `linux-old/` | per-file hashes printed in session; v6.5 fair.c c3b7ee0a0bc51b9f5c39c25c97490b5c5b220b5e456a7c5eeb678463d2886188 |
| Linux autogroup commit | `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/patch/?id=5091faa449ee0b7d73bc296a93bca9540fc51d0a` | commit 2010-11-30; fetched 2026-09-13 | `linux-autogroup-commit/5091faa449ee.patch` | a37bdca3b53f4d6062746b66c141c161b198b237bb7a4c89e023e88a93dab43a |
| schbench (GitHub) | https://github.com/masoncl/schbench.git, master `24e32b8ef67cbafb0761aed68747d90a291767ae` (GitHub repo has **no tags**) | 2025-12-23 | `schbench/` | — |
| schbench v1.0 | https://git.kernel.org/pub/scm/linux/kernel/git/mason/schbench.git tag `v1.0` → `ab22f3f8766e1bf8a3e8f481c205c8f153dd200d` (fetched as remote `korg` into the GitHub clone; v1.0 is an ancestor of GitHub master) | 2023-04-17 00:12:18 -0700 | `schbench-v1.0/README.md`, `schbench-v1.0/schbench.c` (extracted with `git show v1.0:…`) | README b05bdfe9ca6f6e620dd31f476ff5fab9b4c2816b5d586b2febf845f6365bf5e4; schbench.c 2588404b0922e9a67133fef5440cbfcdcabe5b0954fd8943f635ec600a13da82 |
| stress-ng | https://github.com/ColinIanKing/stress-ng.git depth-1, master `3e6ae045c5ff4c409282f7e8f54812c732ab7828`, Makefile `VERSION=0.22.00` | 2026-09-11 18:20:05 +0100 | `stress-ng/` | stress-ng.1 3721705bf31eae4395e3b9cbc2d279bc5d23b7634c3f09b4a1036a344506447f; README.md be171abc25c5724669ee9f0b4aa0a467ded74e6c9fd1968977e3441a75ff2155 |
| LWN 725238 | https://lwn.net/Articles/725238/ "A survey of scheduler benchmarks", June 14, 2017, contributed by Matt Fleming (fresh fetch, HTTP 200) | fetched 2026-09-13 | `lwn-725238/lwn-725238.html`, `.txt` (tags stripped) | html 6fb8023dbf60e99b42bdd25908063360720d7db0f13997f441c4eca1562164e4 |
| LWN 1051430 | https://lwn.net/Articles/1051430/ "Lessons from creating a gaming-oriented scheduler", January 7, 2026, by Jake Edge (fresh fetch, HTTP 200; an older copy `lwn-1051430.html` already existed in sources and was not used) | fetched 2026-09-13 | `lwn-1051430-R01/lwn-1051430.html` | c57ee9c8cb90d8007c87c8f3c4b6d1e2d706770917b4226875d3da47b410d200 |
| helper model (mine, not a source) | Python model of interbench `periodic_schedule()`+`emulate_x()` on an ideal machine | 2026-09-13 | `_dev/research/jioh/2026-09-13-verification/r01_xsim.py` | — |

Canonical-copy notes:
- interbench entry says "v0.31 (pin master commit)". Master `e612a65` still carries `#define INTERBENCH_VERSION "0.31"`, but its code differs from tag `v0.31` (58ea031) in several load parameters (Burn thread default, Read/Write file size, Ring, Hack groups). Both are reported where they differ; master is the primary copy.
- schbench entry says "github.com/masoncl/schbench, v1.0". No `v1.0` tag exists on GitHub; the tag exists in Chris Mason's kernel.org repository and is an ancestor of GitHub master, so v1.0 was read from there; GitHub master was diffed for changes.

---

## interbench

### C-interbench-1 — Audio task: wake rate, CPU demand, RT variant

(a) Verbatim
- `interbench/interbench.8:81-87` (man page, identical text in `readme:45-51`):
  "Audio is simulated as a thread that tries to run at 50ms intervals that then requires 5% cpu. This behaviour ignores any caching that would normally be done by well designed audio applications, but has been seen as the interval used to write to audio cards by a popular linux audio player. It also ignores any of the effects of different audio drivers and audio cards. Audio is also benchmarked running SCHED_FIFO if the real time benchmarking option is used."
- `interbench/interbench.c:490-492`:
  ```
  #define AUDIO_INTERVAL	(50000)
  #define AUDIO_RUN	(AUDIO_INTERVAL / 20)
  /* We emulate audio by using 5% cpu and waking every 50ms */
  ```
- `interbench.c:503-504`: `deadline = periodic_schedule(th, AUDIO_RUN, AUDIO_INTERVAL,` / `deadline);`
- `interbench.c:112`: `{.label = "Audio", .name = emulate_audio, .bench = 1, .rtbench = 1},`
- `interbench.c:1331-1332`: `if (ud.do_rt)` / `set_thread_fifo(thi->pthread, 95);`
- `interbench.c:24` (man): "\fB-r\fR     Perform real time scheduling benchmarks (default: non-rt)" — `interbench.8:24`.

(b) Locators: as above, at commit e612a65.

(c) Reading: Period 50 ms (50 000 µs). CPU demand is specified in code as a run duration derived from the interval: `AUDIO_RUN = 50000/20 = 2500` µs of calibrated busy-loop per period, which the docs express as "5% cpu". So both are present: the docs state a percentage (5%), the code a duration (2.5 ms per 50 ms). These are fixed constants (not defaults of an option). `periodic_schedule()` burns `run_usecs` using the calibrated `loops_per_ms`, advances the deadline by the interval, counts the deadline as met if the burn finished by the deadline, and otherwise counts the whole number of missed intervals and skips them. RT variant: there is no separate audio task; with `-r`, every benchmark flagged `.rtbench` (Audio, Video, and Custom when configured) is run with its thread set to SCHED_FIFO priority 95 (`interbench.c:1331-1332`), its timekeeping thread at FIFO 96 (`:904-905`), memory locked (`:1325-1326`), and latencies reported in µs instead of ms (`:1085-1090`, `:1754-1757`). Caveat stated in text: ignores buffering/caching, drivers, sound cards.

(d) Verdict: FOUND.

### C-interbench-2 — Video task: rate and CPU demand

(a) Verbatim
- `interbench.8:89-93` (= `readme:53-57`): "Video is simulated as a thread that tries to receive cpu 60 times per second and uses 40% cpu. This would be quite a demanding video playback at 60fps. Like the audio simulator it ignores caching, drivers and video cards. As per audio, video is benchmarked with the real time option."
- `interbench.c:510-512`:
  ```
  /* We emulate video by using 40% cpu and waking for 60fps */
  #define VIDEO_INTERVAL	(1000000 / 60)
  #define VIDEO_RUN	(VIDEO_INTERVAL * 40 / 100)
  ```
- `interbench.c:113`: `{.label = "Video", .name = emulate_video, .bench = 1, .rtbench = 1, .load = 1, .rtload = 1},`

(c) Reading: Rate 60 wakeups/s; period in code `1000000/60` = 16 666 µs (integer division). CPU demand stated as "40% cpu" in docs; in code a run duration `16666*40/100` = 6 666 µs per period (integer arithmetic). Same `periodic_schedule()` mechanism as audio. Video is both a benchmark and a background load, and is RT-benchmarked under `-r`. Docs call this "quite a demanding video playback at 60fps"; caveat: ignores caching, drivers, video cards.

(d) Verdict: FOUND.

### C-interbench-3 — X task: activity emulated, CPU demand, variation, input events

(a) Verbatim
- `interbench.8:76-79` (= `readme:40-43`): "X is simulated as a thread that uses a variable amount of cpu ranging from 0 to 100%. This simulates an idle gui where a window is grabbed and then dragged across the screen."
- `interbench.c:530-554`:
  ```
  /*
   * We emulate X by running for a variable percentage of cpu from 0-100% 
   * in 1ms chunks.
   */
  void emulate_x(struct thread *th)
  ...
  	th->decasecond_deadlines = 100;
  ...
  		for (i = 0 ; i <= 100 ; i++) {
  			j = 100 - i;
  			deadline = periodic_schedule(th, i * 1000, j * 1000,
  				deadline);
  			deadline += i * 1000;
  ```
- `interbench.c:1654-1656`: `/* Make benchmark a multiple of 10 seconds for proper range of X loads */` / `if (ud.duration % 10)` / `ud.duration += 10 - ud.duration % 10;`
- `interbench.c:114`: `{.label = "X", .name = emulate_x, .bench = 1, .load = 1, .rtload = 1},` (no `.rtbench`).

(c) Reading: Emulated activity per docs: an idle GUI in which a window is grabbed and dragged. CPU demand in code: a loop over step `i = 0..100`; at step `i` the thread burns `i` ms (run) with an interval argument of `(100−i)` ms, and the base deadline then advances by a further `i` ms, so each step occupies a ~100 ms window whose busy share is `i`%. Variation rule: deterministic linear ramp from 0% to 100% in 1-percentage-point (1 ms) increments, then restart at 0 (sawtooth); no randomness. The "1ms chunks" in the comment corresponds to the 1 ms increment per step; each step's burn is a single `burn_usecs(i*1000)` call. My ideal-machine model of this exact arithmetic (`r01_xsim.py`, zero latency, exact burns/sleeps) gives one sweep ≈ 10.1 s wall time with 5 050 ms of CPU (≈50% average), 100% deadlines met — consistent with the code's `decasecond_deadlines = 100` and the rounding of run length to multiples of 10 s. Input events: the docs mention no input events and the code has none; wakeups are purely deadline/timer driven by the timekeeping thread. X is not an RT benchmark (no `.rtbench`), but is a load in both modes.

(d) Verdict: FOUND (input-event part answered: not event driven).

### C-interbench-4 — Gaming task: CPU bound, deadlines

(a) Verbatim
- `interbench.8:95-101` (= `readme:59-65`): "The cpu usage behind gaming is not at all interactive, yet games clearly are intended for interactive usage. This load simply uses as much cpu as it can get. It does not return deadlines met as there are no deadlines with an unlocked frame rate in a game. This does not accurately emulate a 3d game which is gpu bound (limited purely by the graphics card), only a cpu bound one."
- `interbench.c:556-563`:
  ```
  /* 
   * We emulate gaming by using 100% cpu and seeing how many frames (jobs
   * completed) we can do in that time. Deadlines are meaningless with 
   * unlocked frame rates. We do not use periodic schedule because for
   * this load because this never wants to sleep.
   */
  #define GAME_INTERVAL	(100000)
  #define GAME_RUN	(GAME_INTERVAL)
  ```
- `interbench.c:575-582`: `deadline = get_usecs(&myts) + GAME_INTERVAL;` / `burn_usecs(GAME_RUN);` / … / `if (current_time > deadline) {` / `latency = current_time - deadline;` / `tb->missed_burns += latency;`
- `interbench.c:115`: `{.label = "Gaming", .name = emulate_game, .nodeadlines = 1, .bench = 1},`

(c) Reading: CPU demand is unbounded (100%): it repeatedly burns 100 ms of calibrated work with no sleep. It still measures a "latency" = how much longer than 100 ms wall time each 100 ms burn took, and "% desired CPU" = burned µs / (burned µs + overrun µs). No deadlines: `.nodeadlines = 1` suppresses the "% Deadlines Met" column (`interbench.c:1106-1107`, `1760-1761`). Benchmark only, not a load, not RT-benchmarked. Caveat in text: CPU-bound game only, not GPU-bound.

(d) Verdict: FOUND.

### C-interbench-5 — Burn load

(a) Verbatim
- `interbench.8:120-121` (= `readme:84-85`): "A configurable number of threads fully cpu bound (4 by default)."
- `interbench.8:12`: "\fB\-L\fR     Use cpu load of with burn load (default: 4)"
- `interbench.c:614-626`: `/* Have ud.cpu_load threads burn cpu continuously */` … `for (i = 0 ; i < ud.cpu_load ; i++)` / `create_pthread(&burnthreads[i], NULL, burn_thread,`
- `interbench.c:604-610`: `while (1) {` / `burn_loops(ud.loops_per_ms);` / `if (!trywait_sem(s)) {`
- `interbench.c:1520`: `ud.cpu_load = sysconf(_SC_NPROCESSORS_ONLN);`
- `interbench.c:1436`: `fprintf(stderr, " -L\tUse cpu load of <int> with burn load (default: detected processors)\n");`
- tag v0.31 `interbench.c:75`: `.cpu_load = 4,` (removed at master per `git diff v0.31 HEAD`).

(c) Reading: Burn runs `ud.cpu_load` POSIX threads inside the load process; each thread loops forever calling `burn_loops(loops_per_ms)` (≈1 ms of calibrated no-op loop) and checks a stop semaphore between chunks — fully CPU-bound, never sleeps. Default count: docs (man page, readme) say 4; at tag v0.31 the code default was 4; at master e612a65 the code default is the number of online processors (`sysconf(_SC_NPROCESSORS_ONLN)`), and the usage text says "default: detected processors". Threads not processes. The same `cpu_load` value also sets the Ring thread count and Hack group count at master (see C-interbench-10).

(d) Verdict: FOUND (docs/code default discrepancy noted).

### C-interbench-6 — Write load

(a) Verbatim
- `interbench.8:123-124` (= `readme:87-88`): "A streaming write to disk repeatedly of a file the size of physical ram."
- `interbench.c:632-669`: `/* Write a file the size of ram continuously */` … `char *name = "interbench.write";` … `mem = ud.filesize / (statbuf.st_blksize / 1024);	/* kilobytes to blocks */` / `if (!(buf = calloc(1, statbuf.st_blksize)))` … `while (1) {` … `if (!(fp = fopen(name, "w")))` … `for (i = 0 ; i < mem; i++) {` / `if (fwrite(buf, statbuf.st_blksize, 1, fp) != 1)`
- `interbench.c:1189-1193`: `/* Limit filesize to 1GB */` / `if (ud.ram > 1000)` / `ud.filesize = 1000000;` / `else` / `ud.filesize = ud.ram;`
- `interbench.c:1168`: `if (sscanf(aux, "MemTotal: %lu kB", &ud.ram) )`
- `readme:189-190`: "You need free disk space in the directory it is being run in the order of 2* your physical ram for the disk loads."
- tag v0.31 `interbench.c` (from `git diff v0.31 HEAD`): `mem = ud.ram / (statbuf.st_blksize / 1024);	/* kilobytes to blocks */`

(c) Reading: Writes file `interbench.write` in the current directory, filled with zero bytes (calloc buffer) in blocks of the filesystem's `st_blksize` (min 1024 B). Access pattern: sequential streaming — reopen with mode "w" (truncate), `fwrite` block after block until the target size, close, repeat; no fsync per block; on stop the file is removed and `sync()` ×3 is called. Size vs memory: docs say "the size of physical ram"; tag v0.31 code used MemTotal (kB); master code sets `filesize = 1000000` kB (≈0.95 GiB) whenever MemTotal > 1000 kB — i.e. effectively always capped at ~1 GB, regardless of RAM size (comment: "Limit filesize to 1GB").

(d) Verdict: FOUND (docs/code discrepancy on size at master).

### C-interbench-7 — Read load

(a) Verbatim
- `interbench.8:126-128` (= `readme:90-92`): "Repeatedly reading a file from disk the size of physical ram (to avoid any caching effects)."
- `interbench.c:679-710`: `/* Read a file the size of ram continuously */` … `char *name = "interbench.read";` … `if ((tmp = open(name, O_RDONLY)) == -1)` … `bsize = statbuf.st_blksize;` … 
  ```
  		/* 
  		 * We have to read the whole file before quitting the load
  		 * to prevent the data being cached for the next read. This
  		 * is also the reason the file is the size of physical ram.
  		 */
  		while ((rd = Read(tmp , buf, bsize)) > 0);
  		if(!trywait_sem(s))
  			return;
  		if (lseek(tmp, (off_t)0, SEEK_SET) == -1)
  ```
- `interbench.c:1112-1152` `create_read_file()`: `mem = ud.filesize / (bsize / 1024);	/* kilobytes to blocks */` then `fwrite(buf, bsize, 1, fp)` loop; `interbench.c:1709` calls `create_read_file();` at startup.

(c) Reading: Reads `interbench.read` (created once at startup, zero-filled, reused across runs if its size matches) sequentially with `read()` in `st_blksize` chunks to EOF, then `lseek` to 0 and repeats; the stop check happens only after a whole pass. Page-cache avoidance: no `O_DIRECT`, `posix_fadvise`, or `drop_caches` is used; the only mechanism is file size ("the size of physical ram") so the file cannot all stay cached. At master the file size is `ud.filesize` = 1 000 000 kB (≈1 GB cap, see C-interbench-6), so on machines with more than ~1 GB RAM the size-based rationale in the comment/doc no longer holds; at tag v0.31 it was MemTotal.

(d) Verdict: FOUND (caching avoidance = file size only; size capped at master).

### C-interbench-8 — Per-block / per-operation timing for Write and Read

(a) Verbatim (the absence is shown by the full loop bodies)
- `interbench.c:661-666`: `for (i = 0 ; i < mem; i++) {` / `if (fwrite(buf, statbuf.st_blksize, 1, fp) != 1)` / `terminal_fileopen_error(fp, "fwrite");` / `if (!trywait_sem(s))` / `goto out;` / `}`
- `interbench.c:705`: `while ((rd = Read(tmp , buf, bsize)) > 0);`

(c) Reading: Neither load paces its I/O: no sleep, timer, rate or deadline appears in `emulate_write`, `emulate_read`, or `create_read_file`; blocks are issued as fast as the kernel accepts them. The only size parameter is the block size (`st_blksize`, min 1024 B for write). The docs (man page, readme) state no per-block/chunk/operation timing either; `readme:198-199` says "Future versions may add the option of setting the amount of disk throughput etc."
How searched: read `interbench.c`, `interbench.8`, `readme`, `readme.interactivity` in full; grep for `sleep|usleep|nanosleep|microsleep|interval` within the Write/Read functions (only `microsleep` users are the timekeeping thread and `bench()`).

(d) Verdict: NOT FOUND — interbench specifies no per-block timing; Write and Read are unthrottled sequential loops.

### C-interbench-9 — Compile load

(a) Verbatim
- `interbench.8:130-132` (= `readme:94-96`): "Simulating a heavy 'make -j4' compilation by running Burn, Write and Read concurrently."
- `interbench.c:770-796`: `/* We emulate a compile by running burn, write and read threads simultaneously */` … `if (!strcmp(threadlist[i].label, "Burn"))` … `"Write"` … `"Read"` … `for (i = 0 ; i < 3 ; i++) {` / `initialise_thread(threads[i]);` / `start_thread(&threadlist[threads[i]]);`

(c) Reading: Compile is composed of the Burn, Write and Read loads started together in the one load process. It does not run `make` or any compiler; it emulates. The stated parallelism "make -j4" is a label in the docs; the actual CPU parallelism is Burn's thread count (`ud.cpu_load`: 4 in docs and v0.31; online CPUs at master) plus one writer and one reader thread. No process creation/exit behaviour of a real build is emulated.

(d) Verdict: FOUND.

### C-interbench-10 — Complete list of tasks and loads

(a) Verbatim
- `interbench.c:110-124` (the authoritative table):
  ```
  	{.label = "None", .name = emulate_none, .load = 1, .rtload = 1},
  	{.label = "Audio", .name = emulate_audio, .bench = 1, .rtbench = 1},
  	{.label = "Video", .name = emulate_video, .bench = 1, .rtbench = 1, .load = 1, .rtload = 1},
  	{.label = "X", .name = emulate_x, .bench = 1, .load = 1, .rtload = 1},
  	{.label = "Gaming", .name = emulate_game, .nodeadlines = 1, .bench = 1},
  	{.label = "Burn", .name = emulate_burn, .load = 1, .rtload = 1},
  	{.label = "Write", .name = emulate_write, .load = 1, .rtload = 1},
  	{.label = "Read", .name = emulate_read, .load = 1, .rtload = 1},
  	{.label = "Ring", .name = emulate_ring, .load = 1, .rtload = 1},
  	{.label = "Compile", .name = emulate_compile, .load = 1, .rtload = 1},
  	{.label = "Memload", .name = emulate_memload, .load = 1, .rtload = 1},
  	{.label = "Hack", .name = emulate_hackbench, .load = 0, .rtload = 0},
  	{.label = "Custom", .name = emulate_custom},	/* Leave custom as last entry */
  ```
- Custom: `interbench.8:103-106`: "This load will allow you to specify your own combination of cpu percentage and intervals if you have a specific workload you are interested in and know the cpu usage and frame rate of it on the hardware you are testing." `interbench.8:26,28`: "\fB\-C\fR     Use percentage cpu as a custom load (default: no custom load)"; "\fB\-I\fR     Use microsecond intervals for custom load (needs -C as well)". `interbench.c:1633-1638`: `if (custom_cpu && ud.custom_interval) {` / `ud.custom_run = ud.custom_interval * custom_cpu / 100;` / `threadlist[CUSTOM].bench = 1;` / `threadlist[CUSTOM].load = 1;` / `threadlist[CUSTOM].rtbench = 1;` / `threadlist[CUSTOM].rtload = 1;`
- None: `interbench.8:111-112`: "Otherwise idle system."
- Video/X as loads: `interbench.8:114-118`: "The video simulation thread is also used as a background load." / "The X simulation thread is used as a load."
- Memload: `interbench.8:134-138`: "Simulating heavy memory and swap pressure by repeatedly accessing 110% of available ram and moving it around and freeing it. You need to have some swap enabled due to the nature of this load, and if it detects no swap this load is disabled." Code `interbench.c:252-263`: `unsigned long total = ud.ram + ud.swap;` / `unsigned long usage = ud.ram * 110 / 100 ;` / … `if (total - DEFAULT_RESERVE < usage)` / `usage = total - DEFAULT_RESERVE;` / `usage /= 1024;	/* to megabytes */` / `if (usage > 2930)` / `usage = 2930;`; `interbench.c:817-835`: allocate-and-`memset` 1 MB blocks (`grab_and_touch`), `memcpy(mem_block[i], mem_block[(i + touchable_mem / 2) %` … `touchable_mem], MB);`, then `free` all.
- Hack: `interbench.8:140-144`: "This repeatedly runs the benchmarking program "hackbench" as 'hackbench 50'. This is suggested as a real time load only but because of how extreme this load is it is not unusual for an out-of-memory kill to occur which will invalidate any data you get. For this reason it is disabled by default." Code `interbench.c:853`: `create_pthread(&hackthread.pthread, NULL, hackbench_thread, &ud.cpu_load);`; `interbench/hackbench.c:15-17`: `#define DATASIZE 100` / `#define LOOPS	100` / `#define NUM_FDS	20`; `hackbench.c:153-154`: `for (i = 0; i < *num_groups; i++)` / `total_children += group(*num_groups, readyfds[1], wakefds[0]);`. Commit e612a65 message: "Hackbench still frequently fails to return so disable it for the time being." Tag v0.31 `hackbench.c` (from `git show 6adccf8`): `num_groups = 50;`
- Ring: `interbench.c:745-756`: `/* Create a ring of 4 processes that wake each other up in a circle */` … `for (i = 0 ; i < RINGTHREADS ; i++) {` … `create_pthread(&ringthreads[i].pthread, NULL,`; `interbench.c:713`: `#define RINGTHREADS	(ud.cpu_load)`.

(c) Reading:
- Interactive (benchmarked) tasks: Audio (50 ms / 5%), Video (60 Hz / 40%), X (0→100% ramp), Gaming (100% CPU, no deadlines), Custom (only if both `-C` percent ≤100 and `-I` µs interval are given; run = interval × percent/100; then usable as bench, load, RT bench, RT load).
- Background loads: None, Video, X, Burn, Write, Read, Ring, Compile, Memload, Hack (disabled), Custom (if configured).
- Memload sizing: 110% of MemTotal, limited to RAM+swap − 64 kB, converted to MB, capped at 2 930 MB; allocated in 1 MB blocks (stops at first failed malloc), data shuffled by memcpy with offset n/2, freed, repeated. Disabled if MemTotal or SwapTotal is not found or zero (`interbench.c:1178-1187`).
- Hackbench-based load: docs say `hackbench 50` (50 groups). At tag v0.31 the embedded hackbench used 50 groups; at master it uses `ud.cpu_load` groups (online CPUs by default), each group forking 20 receiver + 20 sender processes over AF_UNIX socketpairs, 100 loops of 100-byte messages, repeated. At both v0.31 and master the `Hack` entry has `.load = 0, .rtload = 0`, and the main loop skips any load with those flags even if selected with `-w` (`interbench.c:1767-1770`), so it never runs.
- Ring: present in code at master, enabled, but **absent from the man page and readme**. It is `cpu_load` pthreads (the comment says "4 processes") passing a semaphore token around a circle without doing work.

(d) Verdict: FOUND (with the doc/code discrepancies above; Ring is undocumented).

### C-interbench-11 — Reported statistics, jitter threshold, default run length

(a) Verbatim
- `interbench.8:152-160` (= `readme:116-122`): "1. The average scheduling latency (time to requesting cpu till actually getting it) of deadlines met during the test period." / "2. The scheduling jitter is represented by calculating the standard deviation of the latency" / "3. The maximum latency seen during the test period" / "4. Percentage of desired cpu" / "5. Percentage of deadlines met."
- `interbench.8:207-209` (= `readme:161-163`): "When the deadlines are actually met, the average latency represents how "smooth" it would look. Average humans' limit of perception for jitter is in the order of 7ms. Trained audio observers might notice much less."
- `interbench.8:14`: "\fB\-t\fR     Seconds to run each benchmark (default: 30)"; `interbench.c:77`: `.duration = 30,`
- `interbench.c:1065-1069`: `average_latency = tbj->total_latency / tbj->nr_samples;` / `variance = (tbj->sum_latency_squared - (average_latency *` / `average_latency) / tbj->nr_samples) / (tbj->nr_samples - 1);` / `sd = sqrtl(variance);`
- `interbench.c:1079-1081`: `samples_met = (double)tbj->achieved_burns /` / `(double)(tbj->achieved_burns + tbj->missed_burns) * 100;`
- `interbench.c:1094-1095`: `deadlines_met = (double)tbj->deadlines_met /` / `(double)(tbj->missed_deadlines + tbj->deadlines_met) * 100;`
- `interbench.c:1085`: `/* When benchmarking rt we represent the data in us */`
- `readme:190-191`: "A default run in v0.21 takes about 15 minutes to complete, longer if your disk is slow."

(c) Reading: Per (benchmark task, load) pair, one row: mean latency, "SD", max latency (ms in normal mode, µs with `-r`), % desired CPU (achieved burns / (achieved + missed)), % deadlines met (omitted for Gaming). Code caveats: (1) the mean is over all samples, and missed intervals add `intervals × interval` to latency (`interbench.c:450-455`), not only "deadlines met" as the docs say; (2) the variance expression divides x̄² by n instead of multiplying (standard sample variance is (Σx² − n·x̄²)/(n−1)), so the printed "SD" is close to root-mean-square latency — consistent with the sample output where "+/-" ≈ mean (e.g. `interbench.8:170` "None      0.495 +/- 0.495"). Human-perception jitter threshold: "in the order of 7ms" (average humans), with trained audio observers noticing less; no source is cited for it. Default run length: 30 s per benchmark/load pair, rounded up to a multiple of 10 s (`interbench.c:1655-1656`), plus a 1 s delay after starting the load before starting the benchmark (`interbench.c:1391-1392`). Whole default run in v0.21: "about 15 minutes".

(d) Verdict: FOUND.

### C-interbench-12 — How tasks are combined with loads

(a) Verbatim
- `interbench.8:54-57`: "It is designed to emulate the cpu scheduling behaviour of interactive tasks and measure their scheduling latency and jitter. It does this with the tasks on their own and then in the presence of various background loads, both with configurable nice levels and the benchmarked tasks can be real time."
- `interbench.8:71-72`: "Each benchmarked simulation runs as a separate process with its own threads, and the background load (if any) also runs as a separate process."
- `interbench.c:1764-1773`: `for (j = 0 ; j < THREADS ; j++) {` … `if (j == i || !bit_is_on(selected_loads, j) ||` / `(!threadlist[j].load && !ud.do_rt) ||` / `(!threadlist[j].rtload && ud.do_rt))` / `continue;` … `bench(i, j);`
- `interbench.c:1383-1397`: `set_fifo(99);` / `set_mlock();` / `/* Wakeup the load process */` … `/* After a small delay, wake up the benched process */` / `sleep(1);` / `wakeup_with(m2b[1]);` … `microsleep(ud.duration * 1000000);`

(c) Reading: Full pairwise sweep, one pair at a time: for each selected benchmark task i (Audio, Video, X, Gaming; Custom if set; RT mode uses the `rtbench` subset), for each selected load j ≠ i, fork a load process (nice `-N`) and a benchmark process (nice `-B`), start the load, wait 1 s, run the benchmark for the duration, stop both, print a row. "None" is one of the loads, giving the unloaded baseline. A task is never paired with itself (e.g., Video is not tested against the Video load). Only one load at a time (Compile is itself the composite Burn+Write+Read). Loads/benches can be narrowed with `-w/-x/-W/-X`. The main process runs SCHED_FIFO 99 while coordinating.

(d) Verdict: FOUND.

### C-interbench-13 — Author, repository, license, version, packaging

(a) Verbatim
- `interbench.c:5`: ` * Author:  Con Kolivas […]`; `interbench.8:211-212`: "Written by Con Kolivas."
- `interbench.c:7-10`: " * This program is free software; you can redistribute it and/or modify" / " * it under the terms of the GNU General Public License as published by" / " * the Free Software Foundation; either version 2 of the License, or" / " * (at your option) any later version."
- `interbench/COPYING:1-2`: "GNU GENERAL PUBLIC LICENSE" / "Version 2, June 1991"; `interbench/LICENSE:1-2`: "GNU GENERAL PUBLIC LICENSE" / "Version 3, 29 June 2007" (added in commit 28b6640 "Initial commit", 2016-10-21).
- `interbench.c:25`: `#define INTERBENCH_VERSION	"0.31"`; `interbench.8:1`: `.TH interbench "8" "March 2006" "Interbench 0.31" "System Commands"`
- `interbench.8:214-215`: "This manual page was written for the Debian system by" / "Julien Valroff […]."; `interbench.8:224`: "http://interbench.kolivas.org"
- GitHub API (repos/ckolivas/interbench): `'license': {'key': 'gpl-3.0', …}`, `'created_at': '2016-10-21T02:26:15Z'`, `'description': 'Interactivity benchmark'`.
- FreeBSD `interbench-packaging/freebsd-Makefile`: "PORTVERSION=	0.31", "LICENSE=	GPLv2", "WWW=		http://users.on.net/~ckolivas/interbench/".
- Gentoo `interbench-0.31-r1.ebuild:9,13`: `HOMEPAGE="https://github.com/ckolivas/interbench/"`, `LICENSE="GPL-2+"`.
- AUR RPC: `"Name":"interbench"`, `"Version":"0.31-4"`, `"License":["GPLv2"]`.
- Repology API lists repos: `"aosc"`, `"aur"`, `"freebsd"`, `"gentoo"`, `"gnuguix"`, `"liguros_stable"`, `"liguros_develop"`, `"opensuse_leap_15_5"`, `"opensuse_leap_15_6"`, `"void_x86_64"`, all `"version":"0.31"`.

(c) Reading: Author Con Kolivas. Repository github.com/ckolivas/interbench (created 2016-10-21 from the 0.31 release; earlier home pages interbench.kolivas.org / users.on.net/~ckolivas). Version string "0.31" (man page dated March 2006). License: source header = GPL version 2 or (at your option) any later version; COPYING = GPLv2 text; a separate LICENSE file = GPLv3 text, which is what GitHub's API reports. So "GPL-2.0" in the entry matches the header/COPYING but the header grants "or later", and GitHub displays GPL-3.0. Packaging: packaged at 0.31 in AUR, FreeBSD ports, Gentoo, GNU Guix, openSUSE Leap 15.5/15.6, Void, AOSC, LiGurOS (Repology, confirmed at primary for AUR, FreeBSD, Gentoo). Debian: the man page was written for Debian, but no current or historical Debian source package was found (sources.debian.org API `{"error":404}`, tracker.debian.org HTTP 404, snapshot.debian.org "No such source package").

(d) Verdict: FOUND.

---

## rt-app

### C-rt-app-1 — JSON format: fields and time units

(a) Verbatim (`rt-app/doc/tutorial.txt` at d6f8be4)
- `:25-30`: "The json file that describes a workload is made on 3 main objects: tasks, resources and global objects. Only tasks object is mandatory; default value will be used if global object is not defined and resources object is kept for backward compatibility with old version of rt-app but it doesn't give any benefit to declare it as the resources are now dynamically created by rt-app when it parses the file."
- Global, `:36-37`: "* duration : Integer. Duration of the use case in seconds. All the threads will be killed once the duration has elapsed."
- Global default object `:111-125`:
  ```
  	"global" : {
  		"duration" : -1,
  		"calibration" : "CPU0",
  		"default_policy" : "SCHED_OTHER",
  		"pi_enabled" : false,
  		"lock_pages" : false,
  		"logdir" : "./",
  		"log_size" : "file",
  		"log_basename" : "rt-app",
  		"ftrace" : "none",
  		"gnuplot" : false,
  		"io_device" : "/dev/null"
  		"mem_buffer_size" : 4194304,
  		"cumulative_slack" : false
  	}
  ```
- Thread, `:152-157`: "* instance : Integer. Define the number of threads that will be created with the properties of this thread object. Default value is 1." … "* delay: Integer. Initial delay before a thread starts execution. The unit is usec."
- `:192-197`: "* loop: Integer. Define the number of times the parent object must be run. … The default value is -1 for thread object and 1 for phases."
- `:208-215`: policy values "SCHED_OTHER", "SCHED_BATCH", "SCHED_IDLE", "SCHED_RR", "SCHED_FIFO", "SCHED_DEADLINE"; `:217`: "* priority : Integer."
- `:221-222`: "* dl-runtime : Integer: Define the runtime budget for deadline scheduling class. Default value is 0. The unit is usec." `:229-230`: "* dl-period : Integer. Define the period duration for deadline scheduling class. Default value is runtime. The unit is usec." `:233-234`: "* dl-deadline : … Default value is period. The unit is usec."
- `:239`: "* cpus: Array of Integer."; `:281`: "util_min: Integer."; `:285`: "util_max: Integer."; `:291`: "* nodes_membind: Array of Integer."; `:332`: "* taskgroup: String."
- Events: `:350-351`: "* run : Integer. Emulate the execution of a load. The duration is defined in usec but the run event will effectively run a number of time a loop that waste cpu cycles."; `:361`: "* runtime : Integer.  The duration is define in usec."; `:366-367`: "* sleep : Integer. Emulate the sleep of a task. The duration is defined in usec."; `:369` "* mem : Integer." (bytes); `:373` "* iorun : Integer." (bytes); `:377` "* memrun : Object."; `:447` "* timer : Object."; plus `lock`, `unlock`, `wait`, `signal`, `broad`, `sync`, `barrier`, `suspend`, `resume`, `sem_post`, `sem_wait`, `yield`, `fork` (`:571-666`).
- Code confirms keys: `rt-app/src/rt-app_parse_config.c:1508-1609` (`"duration"`, `"gnuplot"`, `"default_policy"`, `"calibration"`, `"log_size"`, `"logdir"`, `"log_basename"`, `"ftrace"`, `"lock_pages"`, `"pi_enabled"`, `"io_device"`, `"mem_buffer_size"`, `"cumulative_slack"`); thread `:1372` `"delay"`, `:1376` `"instance"`, `:1407` `"loop"` default -1, `:1379` `"phases"`; phase `:1281` `"loop"` default 1; `:1134-1188` `"policy"`, `"priority"`, `"dl-runtime"`, `"dl-period"`, `"dl-deadline"`, `"util_min"`, `"util_max"`, legacy `"runtime"`, `"period"`, `"deadline"`; `:1050` `"cpus"`, `:1085` `"nodes_membind"`, `:1216` `"taskgroup"`; top-level `:1625-1632` `"global"`, `"tasks"`, `"resources"`.

(c) Reading: Top level: `tasks` (required), `global` (optional), `resources` (legacy). Global fields: duration, calibration, default_policy, pi_enabled, lock_pages, logdir, log_basename, log_size, ftrace, gnuplot, io_device, mem_buffer_size, cumulative_slack. Thread fields: instance, delay, loop, phases, plus per-thread/phase scheduling (policy, priority, dl-runtime/period/deadline), cpus, nodes_membind, util_min/max, taskgroup, and the ordered event list. Units: global `duration` in **seconds** (−1 = unbounded); `run`, `runtime`, `sleep`, timer `period`, `delay`, `dl-*` in **microseconds**; `mem`, `iorun`, `mem_buffer_size`, memrun size in **bytes**; `log_size` integer in **MB**. `run` is work-based (n = floor(t·1000/pLoad) calibrated loops, so wall time varies with CPU speed); `runtime` is wall-time-based. Inconsistencies within the tutorial/code: `lock_pages` text says "Default value is True" (`:55-56`) while the default-object shows `false`; code default is `1` (true) (`parse_config.c:1603`). `log_basename` text says `"rt-app-"` (`:62`), default object and code say `"rt-app"`.

(d) Verdict: FOUND.

### C-rt-app-2 — `timer` event semantics

(a) Verbatim
- `tutorial.txt:447-452`: "* timer : Object. Emulate the wake up of the thread by a timer. Timer differs from sleep event by the start time of the timer duration. Sleep duration starts at the beginning of the sleep event whereas timer duration starts at the end of the last use of the timer. So Timer event are immunized against preemption, frequency scaling and computing capacity of a CPU. The initial starting time of the timer is set during the 1st use of the latter."
- `tutorial.txt:468-470`: "We can see that task B period stays to 19 even if the run event is delayed because of scheduling preemption whereas the period of task A starts at 15 but increases to 19 because of the scheduling delay."
- `tutorial.txt:472-475`: ""unique" timer device: When a thread that uses a timer is instantiated, the timer will be shared across the thread instance which disturbs the original sequence. In order to have 1 timer per instance, you can use the "unique" prefix so a new timer will be created for each instance."
- `tutorial.txt:507-509`: "Timers can work with a "relative" or an "absolute" reference. By default they work in "relative" mode, but this mode can also be explicitly specified as the following:"
- `tutorial.txt:518-522`: ""relative" mode means that the reference for setting the next timer event is relative to the end of the current phase. This in turn means that if, for some reason (i.e., clock frequency was too low), events in a certain phase took too long to execute and the timer of that phase couldn't actually fire at all, the next phase won't be affected."
- `tutorial.txt:548-553`: ""absolute" mode means that the reference for setting the next timer event is fixed and always consider the starting time of the first phase. This means that if, for some reason (i.e., clock frequency was too low), events in a certain phase took too long to execute and the timer of that phase couldn't actually fire at all, the next phase (and potentially other subsequent phases) _will_ be affected."
- Code `src/rt-app.c:577-598`:
  ```
  			if (rdata->res.timer.init == 0) {
  				rdata->res.timer.init = 1;
  				rdata->res.timer.t_next = *t_first;
  			}

  			rdata->res.timer.t_next = timespec_add(&rdata->res.timer.t_next, &t_period);
  			clock_gettime(CLOCK_MONOTONIC, &t_now);
  			t_slack = timespec_sub(&rdata->res.timer.t_next, &t_now);
  ...
  			if (timespec_lower(&t_now, &rdata->res.timer.t_next)) {
  				clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &rdata->res.timer.t_next, NULL);
  				clock_gettime(CLOCK_MONOTONIC, &t_now);
  				t_wu = timespec_sub(&t_now, &rdata->res.timer.t_next);
  				ldata->wu_latency += timespec_to_usec(&t_wu);
  			} else {
  				if (rdata->res.timer.relative)
  					clock_gettime(CLOCK_MONOTONIC, &rdata->res.timer.t_next);
  				ldata->wu_latency = 0UL;
  			}
  ```
- `src/rt-app_parse_config.c:838-864`: `tmp = get_string_value_from(obj, "ref", TRUE, "unknown");` / `if (!strncmp(tmp, "unique", strlen("unique"))) {` … `data->duration = get_int_value_from(obj, "period", TRUE, 0);` … `tmp = get_string_value_from(obj, "mode", TRUE, "relative");` / `if (!strncmp(tmp, "absolute", strlen("absolute")))` / `rdata->res.timer.relative = 0;`; `:213` `data->res.timer.relative = 1;`

(c) Reading: `ref` names the timer resource; threads/phases that use the same name share one timer; a name starting with "unique" makes it per thread instance (shared across that thread's phases if the same unique name is reused). `period` is the timer period in µs (default 0). Wake times (code): the first target is the thread's start reference `t_first` + period; each subsequent target = previous *target* + period, and the thread sleeps with `clock_nanosleep(..., TIMER_ABSTIME, ...)` — i.e. absolute wake times on a drift-free grid, not relative to when the thread actually woke or finished. Wakeup latency (actual wake − target) is accumulated into `wu_lat`; `slack` = target − now at the timer event. Overrun (now ≥ target when the timer event is reached): no sleep; in the default `"relative"` mode the grid is re-anchored to *now* (next target = now + period on the next use); in `"absolute"` mode the target is left unchanged, so later iterations also run without sleeping until they catch up with the original grid. In the overrun branch `wu_latency` is set to 0 (overwrites, not adds). Wording caveat: the tutorial describes relative mode as "relative to the end of the current phase" in general, but in code the re-anchoring only happens on overrun; when on time, both modes follow the same absolute grid.

(d) Verdict: FOUND.

### C-rt-app-3 — Example template configuration

(a) Verbatim — `rt-app/doc/examples/template.json:1-34` (whole file):
```
{
	/*
	 * Simple use case which creates 10% load
	 * for 6 seconds.
	 * A "sleep" : 0 has been added so the file can be used by tune_json.py to
	 * use a sleep event instead of the timer. In this latter case, you need
	 * to set the timer's period to 0
	 */
	"tasks" : {
		/* no 'loop' value at task level means loop indefinitely (-1) */
		"thread0" : {
			"instance" : 1,  /* number of threads to be created */
			"loop" : -1,  /* loop forever (see 'duration' below) */

			"run" :   10000,  /* create load [us]: when awaken,
				execute `floor (10000*1000 / pLoad[ns])` loops */

			"sleep" : 0, /* sleep 0s - which is somewhat useless */

			"timer" : { "ref" : "unique", "period" : 100000 }
			/* wake up thread every 100000 us */
		}
	},
	"global" : {
		"duration" : 6,  /* run for a maximum of 6s total */
		"calibration" : "CPU0",   /* calibrate on CPU0 */
		"default_policy" : "SCHED_OTHER",
		"pi_enabled" : false,
		"lock_pages" : false,
		"logdir" : "./",
		"log_basename" : "rt-app2",
		"gnuplot" : true
	}
}
```

(c) Reading: One thread `thread0`, 1 instance, infinite loop bounded by a 6 s global duration; each iteration: run 10 000 µs of calibrated work, sleep 0, then a unique timer with 100 000 µs period → 10 ms per 100 ms = the "10% load" in the comment. SCHED_OTHER, calibrate on CPU0, no PI, no page locking, logs to ./ with basename "rt-app2", gnuplot output on. The file contains C-style comments, which are not strict JSON (the tutorial says the workgen script normalises such files).

(d) Verdict: FOUND.

### C-rt-app-4 — Maintainer organization, license, kernel documentation reference

(a) Verbatim
- `rt-app/README.in:7-12`: "rt-app is a test application that starts multiple periodic threads in order to simulate a real-time periodic load." / "Code is currently maintained on GitHub:" / "http://github.com/scheduler-tools/rt-app"
- `rt-app/src/rt-app.c:2-10`: "This file is part of rt-app - https://launchpad.net/rt-app" / "Copyright (C) 2010  Giacomo Bagnoli […]" / "Copyright (C) 2014  Juri Lelli […]" / "Copyright (C) 2014  Vincent Guittot […]" / … "modify it under the terms of the GNU General Public License" / "as published by the Free Software Foundation; either version 2" / "of the License, or (at your option) any later version."
- `rt-app/COPYING.in:1-2`: "GNU GENERAL PUBLIC LICENSE" / "Version 2, June 1991"
- GitHub API: repos/scheduler-tools/rt-app `'license': {'key': 'gpl-2.0', …}`, `'description': 'rt-app emulates typical mobile and real-time systems use cases and gives runtime information'`, owner type `Organization`; orgs/scheduler-tools: `'name': None, 'description': ''`.
- Linux `Documentation/scheduler/sched-deadline.rst:745-759` at HEAD 2f0c1cf: "Appendix A. Test suite" / … "The SCHED_DEADLINE policy can be easily tested using two applications that are part of a wider Linux Scheduler validation suite. The suite is available as a GitHub repository: https://github.com/scheduler-tools." / "The first testing application is called rt-app and can be used to start multiple threads with specific parameters. rt-app supports SCHED_{OTHER,FIFO,RR,DEADLINE} scheduling policies and their related parameters (e.g., niceness, priority, runtime/deadline/period). rt-app is a valuable tool, as it can be used to synthetically recreate certain workloads (maybe mimicking real use-cases) and evaluate how the scheduler behaves under such workloads. In this way, results are easily reproducible. rt-app is available at: https://github.com/scheduler-tools/rt-app."
- `sched-deadline.rst:761-762`: "rt-app does not accept command line arguments, and instead reads from a JSON configuration file." (followed by an example config, `:764-785`).
- Secondary context, LWN 725238: "Today, ARM and Linaro are using rt-app to trigger specific scheduler code paths."

(c) Reading: Maintained under the GitHub organization "scheduler-tools" (no further organisational description on GitHub; the kernel doc calls it "a wider Linux Scheduler validation suite"). Historic home launchpad.net/rt-app; copyright holders are individuals (2010, 2014). No company is named as maintainer in the repo; LWN (secondary) names ARM and Linaro as users. License: GPLv2 text in COPYING.in; source headers GPL version 2 or later; GitHub reports GPL-2.0. Kernel documentation references rt-app: yes, `Documentation/scheduler/sched-deadline.rst` Appendix A (URL, description, example JSON). Only other "rtapp" hit in Documentation/ is the unrelated RV monitor `Documentation/trace/rv/monitor_rtapp.rst`.

(d) Verdict: FOUND.

---

## hackbench

### C-hackbench-1 — Defaults, task count, output, distribution

(a) Verbatim
- `rt-tests/src/hackbench/hackbench.c:37-40`: `static unsigned int datasize = 100;` / `static unsigned int loops = 100;` / `static unsigned int num_groups = 10;` / `static unsigned int num_fds = 20;`
- `hackbench.c:49`: `static unsigned int process_mode = PROCESS_MODE;`; `:51-52`: `static int use_pipes = 0;` / `static int use_inet = 0;`
- `hackbench.c:504-507`: `printf("Running in %s mode with %d groups using %d file descriptors each (== %d tasks)\n",` / `(process_mode == THREAD_MODE ? "threaded" : "process"),` / `num_groups, 2*num_fds, num_groups*(num_fds*2));` / `printf("Each sender will pass %d messages of %d bytes\n", loops, datasize);`
- `hackbench.c:570`: `printf("Time: %lu.%03lu\n", diff.tv_sec, diff.tv_usec/1000);`
- `hackbench.c:1`: `// SPDX-License-Identifier: GPL-2.0-or-later`
- `rt-tests/src/hackbench/hackbench.8:1`: `.TH "hackbench" "8" "September  19, 2020" "" ""`; `:18-22`: "Hackbench is both a benchmark and a stress test for the Linux kernel scheduler. It's main job is to create a specified number of pairs of schedulable entities (either threads or traditional processes) which communicate via either sockets or pipes and time how long it takes for each pair to send data back and forth."
- `hackbench.8:63-72`: "Running hackbench without any options will give default behaviour, using fork() and sending data between senders and receivers via sockets." / "user@host: ~ $ hackbench" / "Running in process mode with 10 groups using 40 file descriptors each (== 400 tasks)" / "Each sender will pass 100 messages of 100 bytes" / "Time: 0.890"
- `hackbench.8:96`: "hackbench was written by Rusty Russell […]"
- perf: `linux-docs/tools/perf/bench/sched-messaging.c:6-9` (HEAD 2f0c1cf): " * messaging: Benchmark for scheduler and IPC mechanisms" / " *" / " * Based on hackbench by Rusty Russell […]" / " * Ported to perf by Hitoshi Mitake […]"; `:36` `static unsigned int nr_loops = 100;`, `:38` `static unsigned int num_groups = 10;`, `:296` `unsigned int num_fds = 20;`, `:33` `#define DATASIZE 100`.
- `linux-docs/tools/perf/Documentation/perf-bench.txt:78-80`: "*messaging*::" / "Suite for evaluating performance of scheduler and IPC mechanisms." / "Based on hackbench by Rusty Russell."; `:104-106`: "% perf bench sched messaging                 # run with default" / "options (20 sender and receiver processes per group)" / "(10 groups == 400 processes run)"
- Git: `src/hackbench/hackbench.c` last commit cadd661f 2024-05-22 13:16:15 −0400; `hackbench.8` last commit cf75a538 2023-10-27 (its .TH date is 2020-09-19); rt-tests `Makefile:4` `VERSION = 2.10`.

(c) Reading: Defaults (rt-tests): 10 groups; 20 fds per child (reported as "40 file descriptors each" since sender and receiver each open 20); 100 loops (messages per sender per receiver); 100-byte messages; process mode (fork); AF_UNIX stream socketpairs (pipes with `-p`, TCP with `-i`). Tasks: groups × 2 × fds = 10 × 40 = 400 processes. Each sender writes `loops` messages to each of the 20 receivers in its group. Reported: a header line with mode/groups/fds/tasks, message count/size, then a single wall-clock "Time: s.mmm" from the start signal to reaping all children (no per-message latency, no distribution). Distribution: in rt-tests (`src/hackbench/`), and a port in the Linux tree as `perf bench sched messaging` (`tools/perf/bench/sched-messaging.c`) with the same defaults (10 groups, 20 senders+20 receivers per group, 100 loops, 100 B → 400 processes). The entry's metadata (HEAD fd45df83, hackbench.c 2024-05-22, man date 2020-09-19) matches my copy; license is GPL-2.0-**or-later** per SPDX (COPYING is GPLv2 text).

(d) Verdict: FOUND.

### C-hackbench-2 — "the wording of the LWN article at that number about hackbench"

(a) Verbatim
- The hackbench bibliographic entry in the input is: "hackbench, in rt-tests. git.kernel.org/pub/scm/utils/rt-tests/rt-tests.git (`src/hackbench/hackbench.c`, `src/hackbench/hackbench.8`), GPL-2.0. Repository HEAD `fd45df83` at access; `hackbench.c` last modified 2024-05-22, man page dated 2020-09-19 (accessed 2026-09-12)." It contains no LWN article or number.
- Candidate 1, LWN 725238 "A survey of scheduler benchmarks" (June 14, 2017; "This article was contributed by Matt Fleming"), section "Hackbench" (`lwn-725238/lwn-725238.txt:25-32`): "is a message-passing scheduler benchmark that allows developers to configure both the communication mechanism (pipes or sockets) and the task configuration (POSIX threads or processes). This benchmark is a stalwart of kernel scheduler testing, and has had more versions than the Batman franchise. It was originally created in 2001 by Rusty Russell to demonstrate the improved performance of the multi-queue scheduler patch series." Continues (`:32-35`): "Over the years, many people have added their contributions to Russell's version, including Ingo Molnar, Yanmin Zhang, and David Sommerseth. Hitoshi Mitake added the most recent incarnation to the kernel source tree as part of the perf-bench tool in 2009." And (`:50-53`): "The output of the benchmark is the average scheduler wakeup latency — the duration between telling a task it needs to wake up to perform work and that task running on a CPU." And (`:60-63`): "Because hackbench calculates an average latency for communicating a fixed amount of data between two tasks, it is most often used by developers who are making changes to the scheduler's load-balancing code."
- Candidate 2, LWN 1051430 "Lessons from creating a gaming-oriented scheduler" (January 7, 2026, by Jake Edge), fresh copy: "So, microbenchmarks are of interest as well, but most of the ones he has found for schedulers (e.g. stress-ng and hackbench) are focused on stressing schedulers and measuring the scheduling overhead. That is useful, but improving those numbers does not always lead to better game performance."

(c) Reading: The topic presupposes an LWN article number carried by the entry; the entry has none, so I cannot say which article is meant. The two LWN articles found that discuss hackbench are quoted above. Note on candidate 1: its example output under the hackbench heading is `perf bench sched pipe`, and a reader comment on the same page (Apr 22, 2020) says: ""pipe" is based on pipe-test-1m.c by Ingo Molnar" / ""hackbench" reincarnated in perf as "messaging" -- perf bench sched messaging". Its claim that hackbench outputs "the average scheduler wakeup latency" differs from the rt-tests code, which prints only total elapsed "Time:" (C-hackbench-1). Candidate 2's statement is the speaker's view (Changwoo Min's talk), reported by LWN.
How searched: WebSearch restricted to lwn.net for "hackbench scheduler benchmark"; checked hackbench mentions in both fetched articles.

(d) Verdict: PREMISE NOT IN SOURCE (the entry gives no LWN number; candidate passages given above).

---

## schbench

### C-schbench-1 — Thread structure, request, latencies/percentiles, version, author

(a) Verbatim (v1.0 = kernel.org tag ab22f3f)
- `schbench-v1.0/README.md:4`: "schbench is meant to reproduce the scheduler characteristics of our production web workload with a relatively simple benchmark.  It's really targeting three things:"
- `README.md:12-13`: "schbench uses messaging threads and worker threads.  Workers perform an artificial " / "request comprised of two usleeps (simulating network/disk/locking) and some matrix math.  Messaging threads just queue up the work and wait for results."
- `README.md:15-19`: "Results are recorded for three primary metrics:" / "- Wakeup latency: messaging threads record the time a worker is posted, and workers compare this with the time when they start running." / "- Request latency: time required to complete our fake request." / "- Requests per second: total number of requests all the threads are able to complete."
- `README.md:23`: "Instead of trying to reproduce all of that, schbench just makes preemption expensive.   A per-cpu spinlock that is taken while performing our matrix math, and is released whenever the math is done."
- `README.md:120-133`: "-m (--message-threads): number of message threads (def: 1)" / "One message thread per NUMA node seems best." / "-t (--threads): worker threads per message thread (def: num_cpus)" / … "-r (--runtime): How long to run before exiting (seconds, def: 30)" / "-F (--cache_footprint): cache footprint (kb, def: 256)" / … "-n (--operations): think time operations to perform (def: 5)"
- `schbench-v1.0/schbench.c:1-7`: " * schbench.c" / " *" / " * Copyright (C) 2016 Facebook" / " * Chris Mason […]" / " *" / " * GPLv2, portions copied from the kernel and from Jens Axboe's fio"
- `schbench.c:104`: `static double plist[PLAT_LIST_MAX] = { 20.0, 50.0, 90.0, 99.0, 99.9 };`; `:101-102`: `#define PLIST_FOR_LAT (PLIST_50 | PLIST_90 | PLIST_99 | PLIST_999)` / `#define PLIST_FOR_RPS (PLIST_20 | PLIST_50 | PLIST_90)`
- `schbench.c:1064-1078`:
  ```
  				if (calibrate_only) {
  					/*
  					 * in calibration mode, don't include the
  					 * usleep in the timing
  					 */
  					usleep(100);
  					gettimeofday(&work_start, NULL);
  				} else {
  					/*
  					 * lets start off with some simulated networking,
  					 * and also make sure we get a fresh clean timeslice
  					 */
  					gettimeofday(&work_start, NULL);
  					usleep(100);
  				}
  				do_work(td);
  ```
- `schbench.c:1022-1033` (`do_work`): `if (!skip_locking)` / `lock = lock_this_cpu();` / `for (i = 0; i < operations; i++)` / `do_some_math(td);` / `if (!skip_locking)` / `pthread_mutex_unlock(lock);`
- `schbench.c:716-721`: `fwait(&td->futex, NULL);` … `delta = tvdelta(&td->wake_time, &now);` … `add_lat(&td->wakeup_stats, delta);`
- `schbench.c:1405-1412`: `show_latencies(&wakeup_stats, "Wakeup Latencies", "usec", runtime,` / `PLIST_FOR_LAT, PLIST_99);` / `show_latencies(&request_stats, "Request Latencies", "usec", runtime,` / `PLIST_FOR_LAT, PLIST_99);` / `show_latencies(&rps_stats, "RPS", "requests", runtime,` / `PLIST_FOR_RPS, PLIST_50);` / `if (!auto_rps)` / `fprintf(stderr, "average rps: %.2f\n",`

(c) Reading: Structure: `-m` message threads (default 1), each owning `-t` worker threads (default = number of CPUs). Workers post to their message thread and block on a futex; the message thread records the post time and wakes them. A request (non-calibration mode) in the v1.0 code = `usleep(100)` (100 µs, "simulated networking") followed by `do_work`: take a per-CPU lock (unless `-L`), run `operations` (default 5) rounds of matrix math sized by the cache footprint (default 256 KB), release the lock. Code has one usleep per request; the README says "two usleeps" (README/code mismatch at v1.0). Metrics: wakeup latency (µs, post time → worker running), request latency (µs, request start → work done; includes the usleep except in `--calibrate`), RPS. Percentiles: latencies print p50, p90, p99 (starred), p99.9 plus min/max; RPS prints p20, p50 (starred), p90; pipe mode adds p20 for wakeup; also "average rps". Periodic reports every `-i` s (default 10), warm-up `-w` 5 s, runtime `-r` 30 s. Author: Chris Mason, copyright 2016 Facebook; license "GPLv2" (header). Version: no version string in source or README; "v1.0" exists only as a git tag in the kernel.org repository (2023-04-17), not on the GitHub repo named in the entry. GitHub master (2025-12) has since changed README formatting and added code (`git diff v1.0 HEAD --stat`: schbench.c +746/−…), including extra `usleep(sleep_usec)` paths; the percentile list is unchanged (`plist` = 20, 50, 90, 99, 99.9).

(d) Verdict: FOUND (version-location and "two usleeps" caveats noted).

---

## stress-ng

### C-stress-ng-1 — Author, licence, stressor categories, application-timing modelling

(a) Verbatim (commit 3e6ae04, VERSION 0.22.00)
- `stress-ng/stress-ng.c:2-8`: " * Copyright (C) 2013-2021 Canonical, Ltd." / " * Copyright (C) 2021-2026 Colin Ian King" / … " * modify it under the terms of the GNU General Public License" / " * as published by the Free Software Foundation; either version 2" / " * of the License, or (at your option) any later version."
- `stress-ng/COPYING:1-2`: "GNU GENERAL PUBLIC LICENSE" / "Version 2, June 1991"
- `stress-ng.1:12438-12439`: "is a clean room re-implementation and extension of the original stress tool by Amos Waterland." (preceded at `:12437` by "stress\-ng was written by Colin Ian King […] and")
- `stress-ng.1:116-120`: "specify the class of stressors to run. Stressors are classified into one or more of the following classes: compute, cpu, cpu\-cache, device, fp, gpu, hot, interrupt, integer, ipc, io, filesystem, memory, network, os, pipe, scheduler, search, signal, sort, tlb, vector and vm."
- `stress-ng.c:322-345` class table includes `{ CLASS_SECURITY,	"security" },` in addition to the man-page list.
- `README.md:7-9`: "stress-ng will stress test a computer system in various selectable ways. It was designed to exercise various physical subsystems of a computer as well as the various operating system kernel interfaces."
- `README.md:26-29`: "stress-ng was originally intended to make a machine work hard and trip hardware issues such as thermal overruns as well as operating system bugs that only occur when a system is being thrashed hard."
- `README.md:32-35`: "stress-ng can also measure test throughput rates; this can be useful to observe performance changes across different operating system releases or types of hardware. However, it has never been intended to be used as a precise benchmark test suite, so do NOT use it in this manner."
- `README.md:11-15`: "* 380+ stress tests" / "* 100+ CPU specific stress tests that exercise floating point, integer, bit manipulation and control flow" / "* 60+ virtual memory stress tests" / "* 80+ file system stress tests" / "* 50+ memory/CPU cache stress tests"
- `stress-ng.1:11779-11796` (scheduler workload stressor): "start N workers that exercise the scheduler with items of work that are started at random times with random sleep delays between work items. By default a 100000 microsecond slice of time has 100 work items that start at random times during the slice. The work items by default run for a quanta of 1000 microseconds scaled by the percentage work load (default of 30%)." … "This emulates bursty scheduled compute, such as handling input packets where one may have lots of work items bunched together or with random unpredictable delays between work items."
- `stress-ng.1:2556-2560` (cpu methods): "Note that some of these methods try to exercise the CPU with computations found in some real world use cases. However, the code has not been optimised on a per-architecture basis, so may be a sub-optimal compared to hand-optimised code used in some applications. They do try to represent the typical instruction mixes found in these use cases."

(c) Reading: Author Colin Ian King (copyright Canonical 2013-2021, King 2021-2026); a clean-room reimplementation of Amos Waterland's `stress`. Licence GPL version 2 or later (header), GPLv2 text in COPYING. Categories ("classes"): man page lists 23 — compute, cpu, cpu-cache, device, fp, gpu, hot, interrupt, integer, ipc, io, filesystem, memory, network, os, pipe, scheduler, search, signal, sort, tlb, vector, vm; the code's class table also has "security". Timing of real application behaviour: the docs describe stress-ng as a stress tool for exercising hardware and kernel interfaces, "never been intended to be used as a precise benchmark". I found no claim that it models the timing of real applications. Two narrower statements exist: the `workload` stressor uses random start times/sleeps and says it "emulates bursty scheduled compute, such as handling input packets"; some CPU methods "try to represent the typical instruction mixes" of real-world computations (instruction mix, not timing).
How searched: README.md in full for intent; stress-ng.1 grep for `real.world|realistic|real application|application behav|mimic|emulat|simulat`, DESCRIPTION section, `--class`, AUTHOR/COPYRIGHT.

(d) Verdict: PARTIAL (author, licence, categories found; no statement about modelling real-application timing, only the workload-stressor emulation note).

---

## kernelbuild

### C-kernelbuild-1 — `sched_child_runs_first`, `SCHED_AUTOGROUP` in kernel docs; parallel-build motivation

(a) Verbatim
- `linux-docs/init/Kconfig:1492-1502` at HEAD 2f0c1cf (identical at v6.6 `init/Kconfig:1261-1271`):
  ```
  config SCHED_AUTOGROUP
  	bool "Automatic process group scheduling"
  	select CGROUPS
  	select CGROUP_SCHED
  	select FAIR_GROUP_SCHED
  	help
  	  This option optimizes the scheduler for common desktop workloads by
  	  automatically creating and populating task groups.  This separation
  	  of workloads isolates aggressive CPU burners (like build jobs) from
  	  desktop applications.  Task group autogeneration is currently based
  	  upon task session.
  ```
- `Documentation/admin-guide/kernel-parameters.txt:4479` (HEAD): "noautogroup	Disable scheduler automatic task group creation."
- Autogroup commit 5091faa449ee (Mike Galbraith, 2010-11-30), commit message (`linux-autogroup-commit/5091faa449ee.patch:7-11`): "A recurring complaint from CFS users is that parallel kbuild has a negative impact on desktop interactivity.  This patch implements an idea from Linus, to automatically create task groups.  Currently, only per session autogroups are implemented, but the patch leaves the way open for enhancement."
- Same message `:14-18`: "When a task calls setsid(), a new task group is created, the process is moved into the new task group, and a reference to the preveious task group is dropped.  Child processes inherit this task group thereafter, and increase it's refcount."
- `sched_child_runs_first`, v6.5 `kernel/sched/fair.c:109-113` (`linux-old/v6.5-kernel_sched_fair.c`): "/*" / " * After fork, child runs first. If set to 0 (default) then" / " * parent will (try to) run first." / " */" / "unsigned int sysctl_sched_child_runs_first __read_mostly;"; `:189` `.procname       = "sched_child_runs_first",`; `:12183` `if (sysctl_sched_child_runs_first && curr && entity_before(curr, se)) {`
- v6.6 `kernel/sched/fair.c:81-85` has the same comment and variable; `git grep child_runs_first v6.6` hits only `kernel/sched/debug.c:867`, `kernel/sched/fair.c:85,149,150`, `kernel/sched/sched.h:112` (no use in `task_fork_fair`, `fair.c:12410-12426`).

(c) Reading: `SCHED_AUTOGROUP` is a Kconfig option that automatically creates per-session task groups for CFS so that "aggressive CPU burners (like build jobs)" are isolated from desktop applications; it can be disabled at boot with `noautogroup`. The in-tree documentation (Kconfig help) motivates it with "build jobs" — it does not say "parallel". The originating commit message (kernel history, not Documentation/) explicitly cites "parallel kbuild" hurting desktop interactivity. `sched_child_runs_first` is a sysctl (`/proc/sys/kernel/sched_child_runs_first`) that, per its source comment, makes the child run first after fork when non-zero (default 0: parent tries to run first); in v6.5 it acted in `task_fork_fair`; in v6.6 the variable and sysctl remain but the code has no functional use; at HEAD 2f0c1cf it is absent from the whole tree. It is not described anywhere in `Documentation/`, so the documentation does not motivate it with builds (or anything). The source comment gives no motivation either.
How searched: `git grep` over the entire HEAD tree and the entire v6.6 tree for `child_runs_first` and `autogroup`; fetched and grepped `sched-design-CFS` and sysctl `kernel` docs at v2.6.23, v2.6.32, v3.0, v4.19, v5.4, v6.6 (0 hits for either term).

(d) Verdict: PARTIAL (SCHED_AUTOGROUP found with "build jobs" motivation; `sched_child_runs_first` not in kernel Documentation/ at any version checked — only in source).

### C-kernelbuild-2 — Whether scheduler evaluations commonly use a kernel build; process structure described

(a) Verbatim (related passages found; none answers the question)
- Autogroup commit message (above): "A recurring complaint from CFS users is that parallel kbuild has a negative impact on desktop interactivity."
- `init/Kconfig:1500`: "of workloads isolates aggressive CPU burners (like build jobs) from"
- `Documentation/scheduler/sched-util-clamp.rst:589-592` (HEAD): "If you want to prevent your laptop from heating up while on the go from compiling the kernel and happy to sacrifice performance to save power, but still would like to keep your browser performance intact, uclamp makes it possible."
- interbench `interbench.8:130-132`: "Simulating a heavy 'make -j4' compilation by running Burn, Write and Read concurrently."
- LWN 725238 (survey of scheduler benchmarks) covers hackbench, schbench, Adrestia, rt-app; no kernel-build benchmark section.

(c) Reading: No source read here states that scheduler evaluations commonly use a kernel build, and none describes a build's process structure (short-lived compiler processes versus long-lived make/linker processes). The kernel sources use builds as a motivating example of a CPU-heavy background workload (autogroup commit, Kconfig, uclamp doc); interbench replaces a build with CPU-burn threads plus sequential file I/O, with no process creation. "Commonly" is a survey claim that no single source here supports; the input gives no cited source for this topic.
How searched: `git grep -i "compil|kbuild|kernel build|build|make -j|short-lived|short lived"` in `Documentation/scheduler` at HEAD and v6.6; read the autogroup commit message; checked interbench docs, both LWN articles, the rt-app tutorial, the schbench README, and the stress-ng man page (its `--daemon` stressor mentions "short lived processes" but not builds).

(d) Verdict: NOT FOUND (related build mentions quoted; no source here gives prevalence or a process-structure description).

---

## Verdict counts

- FOUND: 18 (interbench 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13; rt-app 1, 2, 3, 4; hackbench 1; schbench 1)
- PARTIAL: 2 (stress-ng 1; kernelbuild 1)
- NOT FOUND: 2 (interbench 8; kernelbuild 2)
- PREMISE NOT IN SOURCE: 1 (hackbench 2)
- COPY UNREACHABLE: 0

Requests that returned errors or no record (none blocked a topic): sources.debian.org `/api/src/interbench/` → `{"error":404}`; tracker.debian.org/pkg/interbench → HTTP 404; snapshot.debian.org/mr/package/interbench/ → "No such source package"; repology.org API → HTTP 403 with a browser User-Agent (succeeded with a plain tool User-Agent). The Linux kernel.org clone ignored `--filter=blob:none` (full blobs downloaded; no effect on content).
